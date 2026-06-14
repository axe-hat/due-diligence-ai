"""Tests for the ingestion pipeline."""

import pytest
from src.ingestion.chunker import chunk_text, _detect_section


def test_chunk_text_basic():
    text = "This is paragraph one.\n\nThis is paragraph two.\n\nThis is paragraph three."
    chunks = chunk_text(text, ticker="TEST", filing_type="10-K")
    assert len(chunks) >= 1
    assert all("metadata" in c for c in chunks)
    assert all(c["metadata"]["ticker"] == "TEST" for c in chunks)


def test_chunk_text_with_sections():
    text = (
        "ITEM 1A. RISK FACTORS\n\n"
        "The company faces several risks including market volatility.\n\n"
        "ITEM 7. MANAGEMENT'S DISCUSSION AND ANALYSIS\n\n"
        "Revenue increased by 15% year over year."
    )
    chunks = chunk_text(text, ticker="AAPL", filing_type="10-K")
    assert len(chunks) >= 1


def test_detect_section():
    text = "Some intro text. ITEM 1A. RISK FACTORS Here are the risks."
    section = _detect_section(text)
    assert "risk" in section.lower()


def test_chunk_metadata_fields():
    text = "A " * 600  # long enough to create a chunk
    chunks = chunk_text(text, ticker="TSLA", filing_type="10-Q",
                        filing_date="2025-09-30", source_file="test.pdf")
    if chunks:
        meta = chunks[0]["metadata"]
        assert meta["ticker"] == "TSLA"
        assert meta["filing_type"] == "10-Q"
        assert "chunk_id" in meta


def test_empty_text():
    chunks = chunk_text("", ticker="X", filing_type="10-K")
    assert chunks == []
