# Sample Data

This directory contains sample document chunks for quick testing and demos.

To run with real data, use the full pipeline:

```bash
python scripts/01_download_filings.py   # Download from SEC EDGAR
python scripts/02_parse_and_chunk.py     # Parse and chunk
python scripts/03_build_vectorstore.py   # Build vector store
```
