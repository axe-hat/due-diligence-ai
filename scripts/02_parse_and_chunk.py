#!/usr/bin/env python3
"""Parse downloaded filings and chunk them."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import RAW_DIR, PROCESSED_DIR
from src.ingestion.pdf_parser import extract_from_filing_dir
from src.ingestion.chunker import chunk_text


def find_filing_dirs(raw_dir: Path) -> list[dict]:
    """Walk the sec-edgar-downloader output structure and find filing directories."""
    filings = []
    for ticker_dir in sorted(raw_dir.iterdir()):
        if not ticker_dir.is_dir():
            continue
        ticker = ticker_dir.name
        for type_dir in sorted(ticker_dir.iterdir()):
            if not type_dir.is_dir():
                continue
            filing_type = type_dir.name
            for filing_dir in sorted(type_dir.iterdir()):
                if filing_dir.is_dir():
                    filings.append({
                        "ticker": ticker,
                        "filing_type": filing_type,
                        "path": filing_dir,
                        "name": filing_dir.name,
                    })
    return filings


if __name__ == "__main__":
    print("=" * 60)
    print("Step 2: Parsing and chunking filings")
    print("=" * 60)

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    if not RAW_DIR.exists():
        print(f"ERROR: {RAW_DIR} does not exist. Run 01_download_filings.py first.")
        sys.exit(1)

    filings = find_filing_dirs(RAW_DIR)
    print(f"Found {len(filings)} filing directories.\n")

    total_chunks = 0
    for f in filings:
        print(f"Processing {f['ticker']} / {f['filing_type']} / {f['name']}...")
        text = extract_from_filing_dir(str(f["path"]))
        if not text or len(text) < 500:
            print(f"  Skipped (too little text: {len(text)} chars)")
            continue

        chunks = chunk_text(
            full_text=text,
            ticker=f["ticker"],
            filing_type=f["filing_type"],
            filing_date=f["name"],
            source_file=str(f["path"]),
        )
        total_chunks += len(chunks)
        print(f"  -> {len(chunks)} chunks ({len(text):,} chars)")

        out_file = PROCESSED_DIR / f"{f['ticker']}_{f['filing_type']}_{f['name']}.json"
        with open(out_file, "w") as fp:
            json.dump(chunks, fp, indent=2)

    print(f"\nDone: {total_chunks} total chunks across {len(filings)} filings.")
