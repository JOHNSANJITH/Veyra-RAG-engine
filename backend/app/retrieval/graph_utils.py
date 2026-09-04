"""Graph utilities for adaptive Graph-RAG."""

from collections import defaultdict
from typing import Dict, Iterable, List, Set

import networkx as nx
from app.models.ingestion import Chunk

_ENTITY_TO_CHUNKS: Dict[str, Set[str]] = defaultdict(set)
_GRAPH: nx.Graph = nx.Graph()
_INDEXED_CHUNK_IDS: Set[str] = set()


def index_entities(chunks: List[Chunk]) -> None:
    """Add chunk/entity relationships and update the shared concept graph."""
    for chunk in chunks:
        _INDEXED_CHUNK_IDS.add(chunk.chunk_id)
        concepts = list(dict.fromkeys(chunk.entities))
        for concept in concepts:
            _ENTITY_TO_CHUNKS[concept].add(chunk.chunk_id)
            _GRAPH.add_node(concept)

        for i, c1 in enumerate(concepts):
            for c2 in concepts[i + 1 :]:
                current_weight = _GRAPH.get_edge_data(c1, c2, {}).get("weight", 0)
                _GRAPH.add_edge(c1, c2, weight=current_weight + 1)


def remove_chunks(chunk_ids: Set[str]) -> None:
    """Remove chunk/entity relationships and rebuild affected graph edges."""
    if not chunk_ids:
        return

    affected_entities: Set[str] = set()
    _INDEXED_CHUNK_IDS.difference_update(chunk_ids)

    for entity, indexed_ids in list(_ENTITY_TO_CHUNKS.items()):
        removed = indexed_ids.intersection(chunk_ids)
        if removed:
            indexed_ids.difference_update(removed)
            affected_entities.add(entity)
        if not indexed_ids:
            _ENTITY_TO_CHUNKS.pop(entity, None)

                                                                                
                                                                   
    _GRAPH.clear()
    for entity, chunk_ids_for_entity in _ENTITY_TO_CHUNKS.items():
        _GRAPH.add_node(entity)

                                                                            
                                                              
    from app.retrieval.chunk_registry import get_chunks

    for chunk in get_chunks():
        if chunk.chunk_id in chunk_ids:
            continue
        concepts = list(dict.fromkeys(chunk.entities))
        for i, c1 in enumerate(concepts):
            for c2 in concepts[i + 1 :]:
                current_weight = _GRAPH.get_edge_data(c1, c2, {}).get("weight", 0)
                _GRAPH.add_edge(c1, c2, weight=current_weight + 1)


def build_graph(chunks: List[Chunk]) -> nx.Graph:
    """Return the maintained graph; rebuild it when explicitly given chunks."""
                                                                                
                                                                         
    if not chunks:
        return _GRAPH

    expected_ids = {chunk.chunk_id for chunk in chunks}
    indexed_ids = {
        chunk_id
        for chunk_ids_for_entity in _ENTITY_TO_CHUNKS.values()
        for chunk_id in chunk_ids_for_entity
    }
    if expected_ids != _INDEXED_CHUNK_IDS:
        _ENTITY_TO_CHUNKS.clear()
        _GRAPH.clear()
        _INDEXED_CHUNK_IDS.clear()
        index_entities(chunks)

    return _GRAPH


def get_graph() -> nx.Graph:
    """Return the maintained concept co-occurrence graph."""
    return _GRAPH


def extract_query_entities(text: str, nlp) -> Set[str]:
    """Extract high-signal concepts from a user query."""
    doc = nlp(text)

    concepts: Set[str] = set()

    for ent in doc.ents:
        if ent.label_ in {"ORG", "PRODUCT", "WORK_OF_ART"}:
            concepts.add(ent.text.lower())

    for token in doc:
        if token.pos_ in {"NOUN", "PROPN"}:
            if not token.is_stop and len(token.text) >= 4:
                concepts.add(token.lemma_.lower())

    return concepts


def adaptive_hops(num_entities: int) -> int:
    """Decide graph expansion depth."""
    if num_entities <= 1:
        return 0
    if num_entities <= 3:
        return 1
    return 2


def expand_entities(
    graph: nx.Graph,
    entities: Iterable[str],
    hops: int,
) -> Set[str]:
    """Expand entities via graph traversal."""
    expanded = set(entities)

    for _ in range(hops):
        neighbors = set()
        for entity in expanded:
            if entity in graph:
                neighbors.update(graph.neighbors(entity))
        expanded |= neighbors

    return expanded


def chunks_from_entities(
    chunks: List[Chunk],
    entities: Set[str],
) -> List[Chunk]:
    """Recall chunks mentioning expanded entities."""
    matched_ids: Set[str] = set()

    for entity in entities:
        matched_ids |= _ENTITY_TO_CHUNKS.get(entity, set())

    return [chunk for chunk in chunks if chunk.chunk_id in matched_ids]


def clear_graph() -> None:
    """Clear graph state, useful for tests."""
    _ENTITY_TO_CHUNKS.clear()
    _GRAPH.clear()
    _INDEXED_CHUNK_IDS.clear()
