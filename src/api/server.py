"""FastAPI backend for DueDiligenceAI."""

from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import Optional

from src.retrieval.retriever import retrieve, get_available_companies
from src.generation.qa_chain import answer_question
from src.generation.risk_assessor import assess_risk
from src.generation.executive_summary import generate_executive_summary
from src.vectorstore.chroma_store import collection_stats

app = FastAPI(
    title="DueDiligenceAI",
    description="AI-powered due diligence over SEC filings",
    version="1.0.0",
)


class QueryRequest(BaseModel):
    question: str
    company: Optional[str] = None
    filing_type: Optional[str] = None


@app.get("/api/health")
async def health():
    stats = collection_stats()
    return {"status": "healthy", "chunks_indexed": stats["total_chunks"]}


@app.get("/api/companies")
async def list_companies():
    companies = get_available_companies()
    return {"companies": companies, "count": len(companies)}


@app.post("/api/query")
async def query(request: QueryRequest):
    """Ask a question about any ingested company."""
    result = answer_question(
        request.question,
        company=request.company,
        filing_type=request.filing_type,
    )
    return result


@app.post("/api/risk-assessment/{company}")
async def risk_assessment(company: str):
    """Generate risk assessment for a company."""
    companies = get_available_companies()
    if company not in companies:
        raise HTTPException(404, f"Company '{company}' not found. Available: {companies}")
    return assess_risk(company)


@app.post("/api/executive-summary/{company}")
async def executive_summary(company: str):
    """Generate 1-page due diligence summary."""
    companies = get_available_companies()
    if company not in companies:
        raise HTTPException(404, f"Company '{company}' not found. Available: {companies}")
    return generate_executive_summary(company)


@app.post("/api/search")
async def search(request: QueryRequest):
    """Search for relevant chunks without LLM generation."""
    chunks = retrieve(
        request.question,
        company=request.company,
        filing_type=request.filing_type,
    )
    return {"query": request.question, "results": chunks, "count": len(chunks)}
