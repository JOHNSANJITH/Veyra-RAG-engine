"""BM25 keyword-based retrieval.

The index is rebuilt incrementally from the current in-memory chunk registry so
multiple uploaded documents remain searchable together.  Keeping the source of
truth in the registry also lets document deletion remove chunks from BM25.
"""

from typing import Dict, List

from app.models.ingestion import Chunk
from app.models.retrieval import ScoredChunk
from rank_bm25 import BM25Okapi

_bm25: BM25Okapi | None = None
_chunks: List[Chunk] = []
_chunk_lookup: Dict[str, Chunk] = {}


def build_bm25_index(chunks: List[Chunk]) -> None:
    """Build or rebuild the in-memory BM25 index from all supplied chunks."""
    global _bm25, _chunks, _chunk_lookup

                                                                    
    _chunks = list(chunks)
    _chunk_lookup = {chunk.chunk_id: chunk for chunk in _chunks}

    if not _chunks:
        _bm25 = None
        return

    corpus = [chunk.text.lower().split() for chunk in _chunks]
    _bm25 = BM25Okapi(corpus)


def remove_chunks(chunk_ids: set[str]) -> None:
    """Remove chunks from the BM25 index and rebuild it."""
    if not chunk_ids:
        return

    remaining = [chunk for chunk in _chunks if chunk.chunk_id not in chunk_ids]
    build_bm25_index(remaining)


def bm25_search(query: str, top_k: int = 10) -> List[ScoredChunk]:
    """Run BM25 keyword search."""
    if _bm25 is None or not query.strip():
        return []

    tokens = query.lower().split()
    scores = _bm25.get_scores(tokens)

    scored = [
        ScoredChunk(chunk=_chunks[i], score=float(score))
        for i, score in enumerate(scores)
        if score > 0
    ]

    scored.sort(key=lambda x: x.score, reverse=True)
    return scored[:top_k]
