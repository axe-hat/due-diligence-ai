"""Extract text from SEC filing PDFs and HTML documents."""

import fitz  # PyMuPDF
from pathlib import Path


def extract_text_from_pdf(pdf_path: str) -> list[dict]:
    doc = fitz.open(pdf_path)
    pages = []
    for i, page in enumerate(doc):
        text = page.get_text().strip()
        if text:
            pages.append({
                "page_num": i + 1,
                "text": text,
                "source": str(pdf_path),
            })
    doc.close()
    return pages


def extract_text_from_html(html_path: str) -> str:
    """SEC EDGAR often stores filings as .htm/.html. Extract plain text."""
    path = Path(html_path)
    raw = path.read_text(errors="ignore")
    # Simple tag stripping — good enough for SEC filings
    import re
    text = re.sub(r"<[^>]+>", " ", raw)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def extract_from_filing_dir(filing_dir: str) -> str:
    """Given a directory with SEC filing files, extract all text."""
    p = Path(filing_dir)
    all_text = []

    for f in sorted(p.rglob("*")):
        if f.suffix.lower() == ".pdf":
            pages = extract_text_from_pdf(str(f))
            all_text.extend([pg["text"] for pg in pages])
        elif f.suffix.lower() in (".htm", ".html", ".txt"):
            text = extract_text_from_html(str(f)) if f.suffix.lower() in (".htm", ".html") else f.read_text(errors="ignore")
            if len(text) > 200:  # skip tiny boilerplate files
                all_text.append(text)

    return "\n\n".join(all_text)
