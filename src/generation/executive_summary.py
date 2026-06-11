"""Executive summary generator — 1-page due diligence brief."""

from src.generation.llm import call_llm
from src.retrieval.retriever import retrieve

SUMMARY_PROMPT = """Generate a concise executive due diligence summary for {company} based on the retrieved SEC filing excerpts.

Structure your response exactly as follows:

## Company Overview
(2-3 sentences: what the company does, market position)

## Financial Health
(Revenue trends, profit margins, debt levels, cash position — cite specific numbers if available)

## Key Risks (Top 3)
1. [Risk] — severity: high/medium/low
2. [Risk] — severity: high/medium/low
3. [Risk] — severity: high/medium/low

## Growth Opportunities (Top 3)
1. [Opportunity]
2. [Opportunity]
3. [Opportunity]

## Recommendation
**PROCEED / CAUTION / AVOID** — (2-3 sentence reasoning)

All claims must reference the source filings. If data is insufficient for any section, state that clearly.

Context from {company} SEC filings:
{context}

Executive Due Diligence Summary:"""


def generate_executive_summary(company: str) -> dict:
    queries = [
        f"{company} business overview revenue market position",
        f"{company} financial performance profit margins debt",
        f"{company} risk factors challenges threats",
        f"{company} growth strategy opportunities investments",
    ]

    all_chunks = []
    seen_ids = set()
    for q in queries:
        chunks = retrieve(q, company=company, n_results=5)
        for c in chunks:
            cid = c["metadata"].get("chunk_id", "")
            if cid not in seen_ids:
                seen_ids.add(cid)
                all_chunks.append(c)

    if not all_chunks:
        return {"company": company, "summary": "No data available for this company."}

    all_chunks.sort(key=lambda x: x["score"], reverse=True)
    top_chunks = all_chunks[:15]

    context = "\n\n".join(
        f"[{c['metadata'].get('filing_type', '?')} | {c['metadata'].get('section', 'General')}]: {c['text']}"
        for c in top_chunks
    )

    prompt = SUMMARY_PROMPT.format(company=company, context=context)
    summary = call_llm(prompt, max_tokens=3000)

    return {
        "company": company,
        "summary": summary,
        "chunks_analyzed": len(top_chunks),
    }
