"""Retrieve relevant chunks from the vector store."""

from src.vectorstore.chroma_store import get_collection
from src.config import TOP_K


def retrieve(query: str, n_results: int = TOP_K, company: str = None,
             filing_type: str = None, collection_name: str = "financial_docs") -> list[dict]:
    collection = get_collection(collection_name)

    where_filter = None
    conditions = []
    if company:
        conditions.append({"company": company})
    if filing_type:
        conditions.append({"filing_type": filing_type})

    if len(conditions) == 1:
        where_filter = conditions[0]
    elif len(conditions) > 1:
        where_filter = {"$and": conditions}

    results = collection.query(
        query_texts=[query],
        n_results=n_results,
        where=where_filter,
    )

    chunks = []
    if results and results["documents"]:
        for i, doc in enumerate(results["documents"][0]):
            meta = results["metadatas"][0][i] if results["metadatas"] else {}
            dist = results["distances"][0][i] if results["distances"] else 0.0
            chunks.append({
                "text": doc,
                "metadata": meta,
                "score": round(1 - dist, 4),  # cosine distance to similarity
            })

    return chunks


def get_available_companies(collection_name: str = "financial_docs") -> list[str]:
    """Get list of unique companies in the collection."""
    collection = get_collection(collection_name)
    all_meta = collection.get(include=["metadatas"])
    companies = set()
    for m in all_meta["metadatas"]:
        if "company" in m:
            companies.add(m["company"])
    return sorted(companies)
