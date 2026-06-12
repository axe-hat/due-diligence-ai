"""Evaluation metrics for RAG quality."""


def keyword_recall(answer: str, expected_keywords: list[str]) -> float:
    """What fraction of expected keywords appear in the answer?"""
    if not expected_keywords:
        return 0.0
    answer_lower = answer.lower()
    hits = sum(1 for kw in expected_keywords if kw.lower() in answer_lower)
    return hits / len(expected_keywords)


def source_coverage(sources: list[dict], expected_company: str) -> float:
    """What fraction of returned sources are from the expected company?"""
    if not sources:
        return 0.0
    matches = sum(1 for s in sources if s.get("company") == expected_company)
    return matches / len(sources)


def confidence_check(confidence: float) -> str:
    """Classify confidence level."""
    if confidence >= 0.8:
        return "high"
    elif confidence >= 0.5:
        return "medium"
    else:
        return "low"


def evaluate_single(result: dict, eval_item: dict) -> dict:
    """Evaluate a single QA result against an eval item."""
    answer = result.get("answer", "")
    sources = result.get("sources", [])
    confidence = result.get("confidence", 0.0)

    return {
        "question": eval_item["question"],
        "company": eval_item["company"],
        "category": eval_item["category"],
        "keyword_recall": round(keyword_recall(answer, eval_item.get("expected_keywords", [])), 3),
        "source_coverage": round(source_coverage(sources, eval_item["company"]), 3),
        "confidence": round(confidence, 3),
        "confidence_level": confidence_check(confidence),
        "answer_length": len(answer),
    }


def evaluate_batch(results: list[dict], eval_items: list[dict]) -> dict:
    """Evaluate a batch of results and return aggregate metrics."""
    individual = []
    for result, item in zip(results, eval_items):
        individual.append(evaluate_single(result, item))

    n = len(individual) or 1
    return {
        "total_questions": len(individual),
        "avg_keyword_recall": round(sum(e["keyword_recall"] for e in individual) / n, 3),
        "avg_source_coverage": round(sum(e["source_coverage"] for e in individual) / n, 3),
        "avg_confidence": round(sum(e["confidence"] for e in individual) / n, 3),
        "per_question": individual,
    }
