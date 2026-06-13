#!/usr/bin/env python3
"""Quick demo — runs all three generation modes on a sample company."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.vectorstore.chroma_store import collection_stats
from src.retrieval.retriever import get_available_companies
from src.generation.qa_chain import answer_question
from src.generation.risk_assessor import assess_risk
from src.generation.executive_summary import generate_executive_summary


def main():
    stats = collection_stats()
    companies = get_available_companies()

    print("=" * 60)
    print(f"DueDiligenceAI Demo")
    print(f"Chunks indexed: {stats['total_chunks']}")
    print(f"Companies: {', '.join(companies)}")
    print("=" * 60)

    if not companies:
        print("\nNo data indexed. Run scripts 01-03 first.")
        return

    company = companies[0]
    print(f"\nRunning demo for: {company}\n")

    # 1. Q&A
    print("-" * 40)
    print("1. Question Answering")
    print("-" * 40)
    result = answer_question(f"What are {company}'s top risk factors?", company=company)
    print(f"Confidence: {result['confidence']:.1%}")
    print(f"Answer: {result['answer'][:500]}...")
    print(f"Sources: {len(result['sources'])}")

    # 2. Risk Assessment
    print(f"\n{'-' * 40}")
    print("2. Risk Assessment")
    print("-" * 40)
    risk = assess_risk(company)
    print(f"Chunks analyzed: {risk['chunks_analyzed']}")
    print(f"Assessment: {risk['assessment'][:500]}...")

    # 3. Executive Summary
    print(f"\n{'-' * 40}")
    print("3. Executive Summary")
    print("-" * 40)
    summary = generate_executive_summary(company)
    print(f"Chunks analyzed: {summary['chunks_analyzed']}")
    print(f"Summary: {summary['summary'][:500]}...")

    print(f"\n{'=' * 60}")
    print("Demo complete.")


if __name__ == "__main__":
    main()
