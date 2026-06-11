"""Risk assessment engine — extracts red/amber/green flags from filings."""

from src.generation.llm import call_llm
from src.retrieval.retriever import retrieve

RISK_PROMPT = """You are a senior financial due diligence analyst. Analyze the following excerpts from {company}'s SEC filings and identify risk signals.

Categorize each finding as:
- RED FLAG: Significant risks, liabilities, declining metrics, legal issues, debt concerns
- GREEN FLAG: Growth signals, competitive advantages, strong financials, market leadership
- AMBER FLAG: Uncertainties, pending items, mixed signals, things to watch

For each flag provide:
1. Category: financial / legal / operational / market / regulatory
2. Severity: high / medium / low
3. Finding: one-sentence description
4. Evidence: direct quote or reference from the source

Format as structured list. Be specific, not generic.

Context from {company} filings:
{context}

Risk Assessment:"""


def assess_risk(company: str) -> dict:
    # Retrieve risk-related chunks
    risk_queries = [
        f"What are the main risk factors for {company}?",
        f"{company} legal proceedings liabilities debt",
        f"{company} revenue growth competitive advantage market position",
        f"{company} regulatory compliance issues",
    ]

    all_chunks = []
    seen_ids = set()
    for q in risk_queries:
        chunks = retrieve(q, company=company, n_results=5)
        for c in chunks:
            cid = c["metadata"].get("chunk_id", "")
            if cid not in seen_ids:
                seen_ids.add(cid)
                all_chunks.append(c)

    if not all_chunks:
        return {"company": company, "assessment": "No data available.", "flags": []}

    # Keep top 12 by relevance
    all_chunks.sort(key=lambda x: x["score"], reverse=True)
    top_chunks = all_chunks[:12]

    context = "\n\n".join(
        f"[{c['metadata'].get('section', 'General')}]: {c['text']}"
        for c in top_chunks
    )

    prompt = RISK_PROMPT.format(company=company, context=context)
    assessment = call_llm(prompt, max_tokens=3000)

    return {
        "company": company,
        "assessment": assessment,
        "chunks_analyzed": len(top_chunks),
        "avg_relevance": round(sum(c["score"] for c in top_chunks) / len(top_chunks), 3),
    }
