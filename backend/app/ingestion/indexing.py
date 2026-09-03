"""Index document chunks into Qdrant."""

from typing import List

from app.config import settings
from app.core.embeddings import embed_texts
from app.models.ingestion import Chunk
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

COLLECTION_NAME = "veyra_chunks"


def get_qdrant_client() -> QdrantClient:
    """Create a Qdrant client."""
    return QdrantClient(path=settings.qdrant_path)


def index_chunks(chunks: List[Chunk]) -> None:
    """Embed and index chunks into Qdrant."""
    if not chunks:
        return

    client = get_qdrant_client()

    texts = [chunk.text for chunk in chunks]
    vectors = embed_texts(texts)

                                           
    if not client.collection_exists(COLLECTION_NAME):
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=len(vectors[0]),
                distance=Distance.COSINE,
            ),
        )

    points: List[PointStruct] = []
    for chunk, vector in zip(chunks, vectors):
        points.append(
            PointStruct(
                id=chunk.chunk_id,
                vector=vector,
                payload={
                    "doc_id": chunk.doc_id,
                    "page_start": chunk.page_start,
                    "page_end": chunk.page_end,
                    "text": chunk.text,
                    "entities": chunk.entities,
                },
            )
        )

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points,
    )


def load_indexed_chunks() -> List[Chunk]:
    """Load all persisted chunk payloads from Qdrant."""
    client = get_qdrant_client()
    if not client.collection_exists(COLLECTION_NAME):
        return []

    chunks: List[Chunk] = []
    offset = None
    while True:
        points, next_offset = client.scroll(
            collection_name=COLLECTION_NAME,
            limit=256,
            offset=offset,
            with_payload=True,
            with_vectors=False,
        )
        for point in points:
            payload = point.payload or {}
            if not {"doc_id", "page_start", "page_end", "text"}.issubset(payload):
                continue
            chunks.append(
                Chunk(
                    chunk_id=str(point.id),
                    doc_id=str(payload["doc_id"]),
                    page_start=int(payload["page_start"]),
                    page_end=int(payload["page_end"]),
                    text=str(payload["text"]),
                    entities=list(payload.get("entities", [])),
                )
            )
        if next_offset is None:
            break
        offset = next_offset

    return chunks
