"""Tests for generation modules — import checks and format validation."""

import pytest


def test_qa_chain_import():
    from src.generation.qa_chain import answer_question, QA_PROMPT
    assert callable(answer_question)
    assert "{context}" in QA_PROMPT
    assert "{question}" in QA_PROMPT


def test_risk_assessor_import():
    from src.generation.risk_assessor import assess_risk, RISK_PROMPT
    assert callable(assess_risk)
    assert "{company}" in RISK_PROMPT


def test_executive_summary_import():
    from src.generation.executive_summary import generate_executive_summary, SUMMARY_PROMPT
    assert callable(generate_executive_summary)
    assert "{company}" in SUMMARY_PROMPT


def test_llm_import():
    from src.generation.llm import call_llm
    assert callable(call_llm)


def test_format_context():
    from src.generation.qa_chain import format_context
    chunks = [
        {"text": "test text", "metadata": {"company": "AAPL", "filing_type": "10-K", "section": "Risk"}, "score": 0.9},
    ]
    result = format_context(chunks)
    assert "AAPL" in result
    assert "test text" in result
