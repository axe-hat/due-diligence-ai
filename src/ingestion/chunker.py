"""Section-aware chunking for SEC filings."""

import re
from src.config import CHUNK_SIZE, CHUNK_OVERLAP

# Known section headers in 10-K filings
SECTION_HEADERS = [
    "RISK FACTORS",
    "MANAGEMENT'S DISCUSSION AND ANALYSIS",
    "MANAGEMENT\u2019S DISCUSSION AND ANALYSIS",
    "FINANCIAL STATEMENTS",
    "BUSINESS",
    "LEGAL PROCEEDINGS",
    "PROPERTIES",
    "EXECUTIVE COMPENSATION",
    "SELECTED FINANCIAL DATA",
    "QUANTITATIVE AND QUALITATIVE DISCLOSURES",
    "CONTROLS AND PROCEDURES",
    "MARKET RISK",
]

_HEADER_PATTERN = re.compile(
    r"(?:ITEM\s+\d+[A-Z]?\.\s*)?" + "|".join(re.escape(h) for h in SECTION_HEADERS),
    re.IGNORECASE,
)


def _detect_section(text_before: str) -> str:
    """Find the most recent section header in preceding text."""
    matches = list(_HEADER_PATTERN.finditer(text_before))
    if matches:
        return matches[-1].group(0).strip().title()
    return "General"


def _split_into_sentences(text: str) -> list[str]:
    return re.split(r'(?<=[.!?])\s+', text)


def chunk_text(full_text: str, ticker: str, filing_type: str,
               filing_date: str = "", source_file: str = "") -> list[dict]:
    """Chunk a filing into overlapping pieces with metadata."""
    paragraphs = re.split(r'\n\s*\n', full_text)
    chunks = []
    current_chunk = ""
    chunk_idx = 0

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue

        if len(current_chunk) + len(para) < CHUNK_SIZE:
            current_chunk += "\n\n" + para if current_chunk else para
        else:
            if current_chunk:
                section = _detect_section(full_text[:full_text.find(current_chunk[:80]) + 1])
                chunks.append({
                    "text": current_chunk.strip(),
                    "metadata": {
                        "company": ticker,
                        "ticker": ticker,
                        "filing_type": filing_type,
                        "filing_date": filing_date,
                        "section": section,
                        "source_file": source_file,
                        "chunk_id": f"{ticker}_{filing_type}_{chunk_idx:04d}",
                    }
                })
                chunk_idx += 1

                # Overlap: keep last part of current chunk
                sentences = _split_into_sentences(current_chunk)
                overlap_text = " ".join(sentences[-3:]) if len(sentences) > 3 else ""
                current_chunk = overlap_text + "\n\n" + para if overlap_text else para
            else:
                current_chunk = para

    # Final chunk
    if current_chunk.strip():
        section = _detect_section(full_text[:max(0, full_text.find(current_chunk[:80]) + 1)])
        chunks.append({
            "text": current_chunk.strip(),
            "metadata": {
                "company": ticker,
                "ticker": ticker,
                "filing_type": filing_type,
                "filing_date": filing_date,
                "section": section,
                "source_file": source_file,
                "chunk_id": f"{ticker}_{filing_type}_{chunk_idx:04d}",
            }
        })

    return chunks
