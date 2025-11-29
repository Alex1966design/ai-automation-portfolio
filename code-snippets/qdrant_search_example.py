"""
Пример: поиск по коллекции в Qdrant с использованием OpenAI embeddings.
"""

import os
from typing import List

from dotenv import load_dotenv
from openai import OpenAI
from qdrant_client import QdrantClient

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "demo_rag_docs")

client = OpenAI(api_key=OPENAI_API_KEY)
qdrant = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY or None)

EMBED_MODEL = "text-embedding-3-small"


def embed(text: str) -> List[float]:
    resp = client.embeddings.create(model=EMBED_MODEL, input=text)
    return resp.data[0].embedding


def search(query: str, limit: int = 5):
    vec = embed(query)
    hits = qdrant.search(
        collection_name=QDRANT_COLLECTION,
        query_vector=vec,
        limit=limit,
    )
    return hits


if __name__ == "__main__":
    q = "налог на прибыль при УСН"
    for i, hit in enumerate(search(q), start=1):
        print(f"{i}. score={hit.score:.3f} text={hit.payload.get('text', '')[:120]}...")
