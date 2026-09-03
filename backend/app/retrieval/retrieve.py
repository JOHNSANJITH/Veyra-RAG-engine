"""Unified Hybrid + Adaptive Graph-RAG retrieval."""

from typing import Dict, List, Set

from app.ingestion.entities import NLP
from app.models.retrieval import ScoredChunk
from app.retrieval.chunk_registry import get_chunks
from app.retrieval.graph_utils import (
    adaptive_hops,
    chunks_from_entities,
    expand_entities,
    extract_query_entities,
    get_graph,
)
from app.retrieval.keyword_index import bm25_search
from app.retrieval.reranker import CrossEncoderReranker
from app.retrieval.vector_store import vector_search

_COMPARISON_KEYWORDS = {
    "difference",
    "different",
    "compare",
    "comparison",
    "vs",
    "versus",
}

_reranker = CrossEncoderReranker()


def _fallback_query_terms(query: str) -> Set[str]:
    """Fallback entity-like terms when NER fails."""
    return {token.lower() for token in query.split() if len(token) >= 4}


def hybrid_graph_search(query: str, top_k: int) -> List[ScoredChunk]:
    """Run hybrid vector/BM25 retrieval with maintained graph expansion."""
    seed_k = max(top_k * 4, 8)

    vector_hits = vector_search(query, top_k=seed_k)
    bm25_hits = bm25_search(query, top_k=seed_k)

    combined: Dict[str, ScoredChunk] = {sc.chunk.chunk_id: sc for sc in vector_hits}
    for sc in bm25_hits:
        combined.setdefault(sc.chunk.chunk_id, sc)

    all_chunks = get_chunks()
    graph = get_graph()

    query_entities = extract_query_entities(query, NLP)
    if not query_entities:
        query_entities = _fallback_query_terms(query)

    hops = adaptive_hops(len(query_entities))
    graph_recalled: List[ScoredChunk] = []

    if hops > 0 and query_entities:
        expanded_entities = expand_entities(graph, query_entities, hops)
        graph_chunks = chunks_from_entities(all_chunks, expanded_entities)

        for chunk in graph_chunks:
            if chunk.chunk_id not in combined:
                graph_recalled.append(
                    ScoredChunk(
                        chunk=chunk,
                        score=0.20 + (0.05 * len(chunk.entities)),
                    )
                )

    candidates = list(combined.values()) + graph_recalled
    if not candidates:
        return []

    reranked = _reranker.rerank(
        query=query,
        candidates=candidates,
        top_k=max(top_k, 2),
    )

    is_comparison = any(keyword in query.lower() for keyword in _COMPARISON_KEYWORDS)
    if is_comparison:
                                                                              
        seen = set()
        final: List[ScoredChunk] = []
        for sc in reranked:
            if sc.chunk.chunk_id in seen:
                continue
            final.append(sc)
            seen.add(sc.chunk.chunk_id)
            if len(final) >= max(top_k, 2):
                break
        return final

    return reranked[:top_k]
