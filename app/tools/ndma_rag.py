import json
import pathlib

from qdrant_client.models import Distance, VectorParams, PointStruct
from tools.rag import _get_qdrant, get_embedding

NDMA_COLLECTION = "ndma_docs"
CHUNKS_FILE = pathlib.Path(__file__).parent / "ndma_chunks.json"


def index_ndma():
    client = _get_qdrant()
    existing = [c.name for c in client.get_collections().collections]
    if NDMA_COLLECTION not in existing:
        client.create_collection(
            collection_name=NDMA_COLLECTION,
            vectors_config=VectorParams(size=768, distance=Distance.COSINE),
        )
    if client.count(collection_name=NDMA_COLLECTION).count > 0:
        print("[NDMA] already indexed")
        return
    chunks = json.loads(CHUNKS_FILE.read_text())
    points = []
    for i, ch in enumerate(chunks, 1):
        points.append(PointStruct(
            id=i, vector=get_embedding(ch["text"]), payload=ch))
        if len(points) >= 64:
            client.upsert(collection_name=NDMA_COLLECTION, points=points)
            points = []
            print(f"[NDMA] indexed {i}/{len(chunks)}")
    if points:
        client.upsert(collection_name=NDMA_COLLECTION, points=points)
    print(
        f"[NDMA] done: {client.count(collection_name=NDMA_COLLECTION).count} chunks")


def retrieve_ndma(query: str, k: int = 3):
    client = _get_qdrant()
    hits = client.search(collection_name=NDMA_COLLECTION,
                         query_vector=get_embedding(query), limit=k)
    return [{"source": h.payload.get("source"),
             "text": h.payload.get("text")} for h in hits]


if __name__ == "__main__":
    index_ndma()
    print("\n--- retrieval test ---")
    for r in retrieve_ndma("immediate response priorities during severe flooding"):
        print(r["source"], "::", r["text"][:150], "\n")
