#!/usr/bin/env python3
"""Run evaluation on the curated dataset."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.evaluation.eval_dataset import EVAL_QUESTIONS
from src.evaluation.metrics import evaluate_batch
from src.generation.qa_chain import answer_question


if __name__ == "__main__":
    print("=" * 60)
    print("Running evaluation")
    print("=" * 60)

    results = []
    for i, item in enumerate(EVAL_QUESTIONS):
        print(f"  [{i+1}/{len(EVAL_QUESTIONS)}] {item['question'][:60]}...")
        try:
            result = answer_question(item["question"], company=item["company"])
            results.append(result)
        except Exception as e:
            print(f"    ERROR: {e}")
            results.append({"answer": "", "sources": [], "confidence": 0.0})

    report = evaluate_batch(results, EVAL_QUESTIONS)

    print(f"\n{'=' * 60}")
    print(f"Avg Keyword Recall:  {report['avg_keyword_recall']:.1%}")
    print(f"Avg Source Coverage: {report['avg_source_coverage']:.1%}")
    print(f"Avg Confidence:      {report['avg_confidence']:.1%}")
    print(f"{'=' * 60}")

    out_path = Path(__file__).parent.parent / "data" / "eval_report.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(report, f, indent=2)
    print(f"\nFull report saved to {out_path}")
