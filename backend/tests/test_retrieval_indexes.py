"""Regression tests for multi-document BM25/graph index consistency."""

from app.models.ingestion import Chunk
from app.retrieval import graph_utils, keyword_index
from app.retrieval.chunk_registry import clear_chunks, register_chunks


def _chunk(chunk_id: str, doc_id: str, text: str, entities: list[str]) -> Chunk:
    return Chunk(
        chunk_id=chunk_id,
        doc_id=doc_id,
        page_start=1,
        page_end=1,
        text=text,
        entities=entities,
    )


def setup_function() -> None:
    clear_chunks()
    keyword_index.build_bm25_index([])
    graph_utils.clear_graph()


def test_bm25_keeps_multiple_documents() -> None:
    a = _chunk("a", "doc-a", "alpha retrieval system", ["alpha"])
    b = _chunk("b", "doc-b", "beta retrieval system", ["beta"])
    register_chunks([a, b])
    keyword_index.build_bm25_index([a, b])

    result = keyword_index.bm25_search("beta", top_k=5)

    assert [item.chunk.doc_id for item in result] == ["doc-b"]


def test_bm25_removes_deleted_document_chunks() -> None:
    a = _chunk("a", "doc-a", "alpha retrieval system", ["alpha"])
    b = _chunk("b", "doc-b", "beta retrieval system", ["beta"])
    keyword_index.build_bm25_index([a, b])

    keyword_index.remove_chunks({"a"})
    result = keyword_index.bm25_search("alpha", top_k=5)

    assert result == []


def test_graph_index_removes_deleted_chunks() -> None:
    a = _chunk("a", "doc-a", "alpha beta", ["alpha", "beta"])
    b = _chunk("b", "doc-b", "alpha gamma", ["alpha", "gamma"])
    register_chunks([a, b])
    graph_utils.index_entities([a, b])

    remove_ids = {"a"}
    from app.retrieval.chunk_registry import _CHUNKS
    _CHUNKS.pop("a")
    graph_utils.remove_chunks(remove_ids)

    graph = graph_utils.get_graph()
    assert "beta" not in graph
    assert "gamma" in graph
