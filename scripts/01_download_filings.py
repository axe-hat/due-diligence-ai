#!/usr/bin/env python3
"""Download SEC EDGAR filings for target companies."""

import sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent.parent))

from src.ingestion.sec_downloader import download_filings

if __name__ == "__main__":
    print("=" * 60)
    print("Step 1: Downloading SEC EDGAR filings")
    print("=" * 60)

    results = download_filings(
        tickers=["AAPL", "TSLA", "GOOGL", "MSFT", "NVDA", "AMZN", "META", "JPM"],
        filing_types=["10-K"],
        limit=2,
    )

    ok = sum(1 for r in results if r["status"] == "ok")
    print(f"\nDone: {ok}/{len(results)} successful downloads.")
