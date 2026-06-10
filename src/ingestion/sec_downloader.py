"""Download SEC EDGAR filings (10-K, 10-Q) for target companies."""

from sec_edgar_downloader import Downloader
from src.config import RAW_DIR, SEC_AGENT_NAME, SEC_AGENT_EMAIL

TICKERS = ["AAPL", "TSLA", "GOOGL", "MSFT", "NVDA", "AMZN", "META", "JPM"]


def download_filings(tickers: list[str] = None, filing_types: list[str] = None,
                     limit: int = 2):
    tickers = tickers or TICKERS
    filing_types = filing_types or ["10-K"]

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    dl = Downloader(SEC_AGENT_NAME, SEC_AGENT_EMAIL, str(RAW_DIR))

    results = []
    for ticker in tickers:
        for ft in filing_types:
            try:
                dl.get(ft, ticker, limit=limit)
                results.append({"ticker": ticker, "type": ft, "status": "ok"})
                print(f"  Downloaded {ft} for {ticker}")
            except Exception as e:
                results.append({"ticker": ticker, "type": ft, "status": str(e)})
                print(f"  FAILED {ft} for {ticker}: {e}")
    return results


if __name__ == "__main__":
    print("Downloading SEC filings...")
    download_filings()
    print("Done.")
