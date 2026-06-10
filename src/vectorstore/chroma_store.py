"""ChromaDB vector store management."""

import chromadb
from chromadb.utils import embedding_functions
from src.config import CHROMA_PATH, EMBEDDING_MODEL


def get_client() -> chromadb.PersistentClient:
    return chromadb.PersistentClient(path=CHROMA_PATH)


def get_embedding_fn():
    return embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=EMBEDDING_MODEL
    )


def get_collection(name: str = "financial_docs"):
    client = get_client()
    return client.get_or_create_collection(
        name=name,
        embedding_function=get_embedding_fn(),
        metadata={"hnsw:space": "cosine"},
    )


def add_chunks(chunks: list[dict], collection_name: str = "financial_docs",
               batch_size: int = 200):
    collection = get_collection(collection_name)

    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        collection.add(
            ids=[c["metadata"]["chunk_id"] for c in batch],
            documents=[c["text"] for c in batch],
            metadatas=[c["metadata"] for c in batch],
        )
    print(f"  Added {len(chunks)} chunks to '{collection_name}'")
    return len(chunks)


def collection_stats(collection_name: str = "financial_docs") -> dict:
    collection = get_collection(collection_name)
    count = collection.count()
    return {"collection": collection_name, "total_chunks": count}
