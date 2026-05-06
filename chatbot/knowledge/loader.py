import os
from pathlib import Path


def load_documents(directory):
    """Load documents from a directory. Supports .txt, .md, .pdf"""
    docs = []
    directory = Path(directory)

    for file_path in directory.rglob("*"):
        if file_path.suffix in (".txt", ".md"):
            text = file_path.read_text(encoding="utf-8", errors="ignore")
            docs.append({"content": text, "source": str(file_path), "type": file_path.suffix})
        elif file_path.suffix == ".pdf":
            docs.append({"content": _load_pdf(file_path), "source": str(file_path), "type": ".pdf"})

    return docs


def _load_pdf(path):
    from pypdf import PdfReader
    reader = PdfReader(str(path))
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def chunk_text(text, chunk_size=500, overlap=50):
    """Split text into overlapping chunks."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks
