"""Question answering with source citations."""

from src.generation.llm import call_llm
from src.retrieval.retriever import retrieve

QA_PROMPT = """You are a financial due diligence analyst. Answer the question based ONLY on the provided context.

Rules:
- Cite every claim using [Source: company, filing_type, section]
- If the context doesn't contain enough information, say so explicitly
- Be concise but thorough
- Use bullet points for multiple findings

Context:
{context}

Question: {question}

Answer with citations:"""


def format_context(chunks: list[dict]) -> str:
    parts = []
    for i, c in enumerate(chunks):
        meta = c.get("metadata", {})
        header = f"[{meta.get('company', '?')} | {meta.get('filing_type', '?')} | {meta.get('section', '?')}]"
        parts.append(f"--- Source {i+1}: {header} ---\n{c['text']}")
    return "\n\n".join(parts)


def answer_question(question: str, company: str = None,
                    filing_type: str = None) -> dict:
    chunks = retrieve(question, company=company, filing_type=filing_type)

    if not chunks:
        return {
            "answer": "No relevant documents found. Please ingest some filings first.",
            "sources": [],
            "confidence": 0.0,
        }

    context = format_context(chunks)
    prompt = QA_PROMPT.format(context=context, question=question)
    answer = call_llm(prompt)

    avg_score = sum(c["score"] for c in chunks) / len(chunks) if chunks else 0
    sources = [
        {
            "company": c["metadata"].get("company", ""),
            "filing_type": c["metadata"].get("filing_type", ""),
            "section": c["metadata"].get("section", ""),
            "relevance": c["score"],
            "excerpt": c["text"][:200] + "...",
        }
        for c in chunks
    ]

    return {
        "answer": answer,
        "sources": sources,
        "confidence": round(avg_score, 3),
    }
