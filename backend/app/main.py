"""Main FastAPI application for Veyra backend."""

from app.api.routes_chat import router as chat_router
from app.ingestion.indexing import load_indexed_chunks
from app.retrieval.chunk_registry import register_chunks
from app.retrieval.graph_utils import index_entities
from app.retrieval.keyword_index import build_bm25_index
from app.api.routes_chat_langchain import router as chat_langchain_router
from app.api.routes_docs import router as docs_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Veyra Backend",
    version="0.0.0",
    description="Backend API for Veyra multi-document research assistant.",
)

                              
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

                 
app.include_router(chat_router, prefix="/chat")
app.include_router(docs_router, prefix="/docs")
app.include_router(chat_langchain_router, prefix="/chat")


@app.on_event("startup")
def restore_retrieval_indexes() -> None:
    """Restore in-memory retrieval indexes from persisted Qdrant payloads."""
    chunks = load_indexed_chunks()
    if not chunks:
        return
    register_chunks(chunks)
    index_entities(chunks)
    build_bm25_index(chunks)
