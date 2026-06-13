#!/usr/bin/env python3
"""Build ChromaDB vector store from processed chunks."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import PROCESSED_DIR
from src.vectorstore.chroma_store import add_chunks, collection_stats

if __name__ == "__main__":
    print("=" * 60)
    print("Step 3: Building vector store")
    print("=" * 60)

    if not PROCESSED_DIR.exists():
        print(f"ERROR: {PROCESSED_DIR} does not exist. Run 02_parse_and_chunk.py first.")
        sys.exit(1)

    json_files = sorted(PROCESSED_DIR.glob("*.json"))
    print(f"Found {len(json_files)} chunk files.\n")

    total = 0
    for jf in json_files:
        print(f"Ingesting {jf.name}...")
        with open(jf) as f:
            chunks = json.load(f)
        if chunks:
            add_chunks(chunks)
            total += len(chunks)

    stats = collection_stats()
    print(f"\nDone. Vector store: {stats['total_chunks']} chunks total.")
