"""Shared Zotero utilities for the 1cfe group library.

Functions return values or raise exceptions instead of calling sys.exit(),
making them suitable for both single-item and batch processing.
"""

import hashlib
import os
import re
from pathlib import Path
from typing import NamedTuple

from dotenv import load_dotenv
from pyzotero import zotero

GROUP_ID = 5428393
RAW_DIR = Path("knowledge/raw")
SOURCES_DIR = Path("knowledge/sources")
SOURCE_INDEX_PATH = Path("knowledge/SOURCE_INDEX.md")


def load_api_key() -> str:
    """Load ZOTERO_KEY from .env. Raises ValueError if missing."""
    load_dotenv()
    api_key = os.environ.get("ZOTERO_KEY")
    if not api_key:
        raise ValueError("ZOTERO_KEY must be set in .env")
    return api_key


def connect(api_key: str) -> zotero.Zotero:
    """Return a pyzotero client for the 1cfe group library."""
    return zotero.Zotero(GROUP_ID, "group", api_key)


def find_pdf_attachment(zot, item_key: str) -> dict | None:
    """Find first PDF child attachment. Returns None if no PDF found."""
    children = zot.children(item_key)
    pdfs = [
        c for c in children
        if c["data"].get("contentType") == "application/pdf"
    ]
    if not pdfs:
        return None
    return pdfs[0]


class DownloadResult(NamedTuple):
    path: Path
    sha256: str
    title: str


def download_pdf(
    zot, item_key: str, output_dir: Path, pdf_child: dict | None = None
) -> DownloadResult:
    """Download PDF, return DownloadResult. Skips if file already exists.
    Pass pdf_child to avoid a redundant find_pdf_attachment API call.
    Raises RuntimeError on download failure."""
    item = zot.item(item_key)
    title = item["data"].get("title", "(no title)")
    if pdf_child is None:
        pdf_child = find_pdf_attachment(zot, item_key)
    if pdf_child is None:
        raise RuntimeError(f"No PDF attachment found for item {item_key}")
    filename = pdf_child["data"]["filename"]
    child_key = pdf_child["key"]

    output_dir.mkdir(parents=True, exist_ok=True)
    filepath = output_dir / filename

    if filepath.exists() and filepath.stat().st_size > 0:
        print(f"Already exists, skipping download: {filepath}")
    else:
        zot.dump(child_key, filename, str(output_dir))

    if not filepath.exists() or filepath.stat().st_size == 0:
        raise RuntimeError(f"Download failed — file missing or empty at {filepath}")

    file_sha256 = sha256_of(filepath)
    return DownloadResult(path=filepath, sha256=file_sha256, title=title)


def sha256_of(path: Path) -> str:
    """Compute SHA256 hex digest of a file."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tag_extracted(zot, item_key: str) -> None:
    """Tag a Zotero item as 'extracted'. Skips if already tagged."""
    item = zot.item(item_key)
    existing_tags = item["data"].get("tags", [])
    if any(t["tag"] == "extracted" for t in existing_tags):
        print(f"Item {item_key} already has tag 'extracted', skipping")
        return
    zot.add_tags(item, "extracted")
    print(f"Tagged {GROUP_ID}:{item_key} as 'extracted'")


def slugify(title: str, max_len: int = 60) -> str:
    """Convert title to filesystem-safe slug.
    Lowercase, spaces/non-alnum to underscores, collapse runs, strip edges.
    Truncates at word boundaries to avoid mid-word breaks."""
    slug = title.lower()
    slug = re.sub(r"[^a-z0-9]+", "_", slug)
    slug = re.sub(r"_+", "_", slug)
    slug = slug.strip("_")
    if len(slug) <= max_len:
        return slug
    # Truncate at last underscore before max_len to avoid mid-word break
    truncated = slug[:max_len]
    last_sep = truncated.rfind("_")
    if last_sep > max_len // 2:
        return truncated[:last_sep]
    return truncated
