"""Curated evaluation dataset for benchmarking RAG quality."""

EVAL_QUESTIONS = [
    {
        "question": "What are Apple's top 3 risk factors?",
        "company": "AAPL",
        "category": "risk_assessment",
        "expected_keywords": ["supply chain", "competition", "regulation"],
    },
    {
        "question": "What is Tesla's revenue trend?",
        "company": "TSLA",
        "category": "financials",
        "expected_keywords": ["revenue", "growth", "automotive"],
    },
    {
        "question": "What legal proceedings is Google involved in?",
        "company": "GOOGL",
        "category": "legal",
        "expected_keywords": ["antitrust", "litigation", "regulatory"],
    },
    {
        "question": "What is Microsoft's cloud business performance?",
        "company": "MSFT",
        "category": "financials",
        "expected_keywords": ["Azure", "cloud", "revenue", "growth"],
    },
    {
        "question": "What are NVIDIA's main competitive advantages?",
        "company": "NVDA",
        "category": "competitive",
        "expected_keywords": ["GPU", "AI", "data center", "CUDA"],
    },
    {
        "question": "What is Amazon's debt position?",
        "company": "AMZN",
        "category": "financials",
        "expected_keywords": ["debt", "obligations", "lease", "billion"],
    },
    {
        "question": "What regulatory risks does Meta face?",
        "company": "META",
        "category": "regulatory",
        "expected_keywords": ["privacy", "data", "regulation", "FTC"],
    },
    {
        "question": "What is JPMorgan's exposure to credit risk?",
        "company": "JPM",
        "category": "risk_assessment",
        "expected_keywords": ["credit", "loan", "loss", "provision"],
    },
    {
        "question": "How does Apple manage its supply chain risks?",
        "company": "AAPL",
        "category": "operational",
        "expected_keywords": ["supplier", "manufacturing", "China", "component"],
    },
    {
        "question": "What is NVIDIA's strategy for AI market growth?",
        "company": "NVDA",
        "category": "growth",
        "expected_keywords": ["AI", "data center", "inference", "training"],
    },
]
