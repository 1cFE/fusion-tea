"""Shared Zotero utilities for the 1cfe group library.

Functions return values or raise exceptions instead of calling sys.exit(),
making them suitable for both single-item and batch processing.
"""

import hashlib
import json
import os
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import NamedTuple

from dotenv import load_dotenv
from pyzotero import zotero

GROUP_ID = 5428393
RAW_DIR = Path("knowledge/raw")
SOURCES_DIR = Path("knowledge/sources")
SOURCE_INDEX_PATH = Path("knowledge/SOURCE_INDEX.md")
MANIFEST_PATH = Path("knowledge/MANIFEST.jsonl")
STAGING_DIR = Path("knowledge/.staging")
LOCK_PATH = Path("knowledge/.registry.lock")
BASELINE_PATH = Path("knowledge/.registry_baseline.json")


@dataclass(frozen=True)
class RegistryPaths:
    """Every path the registry writes or reads, so callers can point at a temp tree.

    The module constants above stay the production values; `default_paths()`
    wraps them. Nothing in the seam reads the constants directly.
    """

    raw: Path
    sources: Path
    index: Path
    manifest: Path
    staging: Path
    lock: Path
    baseline: Path

    @classmethod
    def under(cls, knowledge_dir: Path) -> "RegistryPaths":
        return cls(
            raw=knowledge_dir / "raw",
            sources=knowledge_dir / "sources",
            index=knowledge_dir / "SOURCE_INDEX.md",
            manifest=knowledge_dir / "MANIFEST.jsonl",
            staging=knowledge_dir / ".staging",
            lock=knowledge_dir / ".registry.lock",
            baseline=knowledge_dir / ".registry_baseline.json",
        )


def default_paths() -> RegistryPaths:
    """The repository's own registry paths."""
    return RegistryPaths(
        raw=RAW_DIR,
        sources=SOURCES_DIR,
        index=SOURCE_INDEX_PATH,
        manifest=MANIFEST_PATH,
        staging=STAGING_DIR,
        lock=LOCK_PATH,
        baseline=BASELINE_PATH,
    )


def load_manifest() -> dict[str, dict]:
    """Load Zotero-sourced rows as {zotero_key: entry_dict}.

    Non-Zotero rows (URL and local-PDF sources registered through the seam)
    carry no `zotero_key` and are skipped — this view is the Zotero library
    diff, not the whole registry. Use `load_manifest_rows` for that.
    """
    return {row["zotero_key"]: row for row in _manifest_lines() if "zotero_key" in row}


def manifest_keys() -> set[str]:
    """Return set of Zotero keys present in the manifest. Non-Zotero rows are skipped."""
    return set(load_manifest())


def _manifest_lines() -> list[dict]:
    if not MANIFEST_PATH.exists():
        return []
    return [
        json.loads(line)
        for line in MANIFEST_PATH.read_text().splitlines()
        if line.strip()
    ]


def load_manifest_rows(paths: RegistryPaths) -> list[dict]:
    """Every manifest row, in file order, Zotero and non-Zotero alike."""
    if not paths.manifest.exists():
        return []
    return [
        json.loads(line)
        for line in paths.manifest.read_text().splitlines()
        if line.strip()
    ]


def truncate_manifest(byte_len: int, paths: RegistryPaths) -> None:
    """Cut the manifest back to a previously recorded length (rollback rung)."""
    with open(paths.manifest, "r+b") as f:
        f.truncate(byte_len)


def append_manifest_entry(zotero_key: str, slug: str, title: str) -> None:
    """Append a single entry to MANIFEST.jsonl."""
    entry = {
        "zotero_key": zotero_key,
        "slug": slug,
        "title": title,
        "date_extracted": date.today().isoformat(),
    }
    with open(MANIFEST_PATH, "a") as f:
        f.write(json.dumps(entry) + "\n")
        f.flush()


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


class PdfInfo(NamedTuple):
    """Resolved PDF information for download."""
    child_key: str       # Key of the attachment item to download
    filename: str        # Original filename
    title: str           # Best available title
    is_standalone: bool  # True if top-level attachment (no parent)


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


def resolve_pdf_info(zot, item: dict) -> PdfInfo | None:
    """Resolve PDF download info for any item type.

    For standalone attachments (itemType='attachment', contentType='application/pdf'):
        The item itself is the PDF — use its key directly.

    For parent items (journalArticle, book, etc.):
        Look up children, find first PDF attachment, use parent's title.

    Returns None if no PDF is available.
    """
    data = item["data"]
    if (data.get("itemType") == "attachment"
            and data.get("contentType") == "application/pdf"):
        filename = data.get("filename", "")
        # Use cleaned-up filename as title for standalone attachments
        title = data.get("title") or Path(filename).stem.replace("_", " ").title()
        return PdfInfo(
            child_key=item["key"],
            filename=filename,
            title=title,
            is_standalone=True,
        )

    # Parent item — look for PDF child
    pdf_child = find_pdf_attachment(zot, item["key"])
    if pdf_child is None:
        return None
    return PdfInfo(
        child_key=pdf_child["key"],
        filename=pdf_child["data"]["filename"],
        title=data.get("title", "(no title)"),
        is_standalone=False,
    )


def download_pdf_from_info(
    zot, pdf_info: PdfInfo, output_dir: Path
) -> DownloadResult:
    """Download PDF using resolved PdfInfo. Skips if file already exists.
    Raises RuntimeError on download failure."""
    output_dir.mkdir(parents=True, exist_ok=True)
    filepath = output_dir / pdf_info.filename

    if filepath.exists() and filepath.stat().st_size > 0:
        print(f"Already exists, skipping download: {filepath}")
    else:
        zot.dump(pdf_info.child_key, pdf_info.filename, str(output_dir))

    if not filepath.exists() or filepath.stat().st_size == 0:
        raise RuntimeError(f"Download failed — file missing or empty at {filepath}")

    file_sha256 = sha256_of(filepath)
    return DownloadResult(path=filepath, sha256=file_sha256, title=pdf_info.title)


def sha256_of(path: Path) -> str:
    """Compute SHA256 hex digest of a file."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def add_tag(zot, item_key: str, tag: str) -> bool:
    """Add a tag to a Zotero item. Skips if already tagged.
    Returns True if tag was added, False if already present."""
    item = zot.item(item_key)
    existing_tags = item["data"].get("tags", [])
    if any(t["tag"] == tag for t in existing_tags):
        print(f"  {item_key} already has tag '{tag}', skipping")
        return False
    zot.add_tags(item, tag)
    print(f"  Tagged {GROUP_ID}:{item_key} as '{tag}'")
    return True


def tag_extracted(zot, item_key: str) -> bool:
    """Tag a Zotero item as 'extracted'. Convenience wrapper around add_tag."""
    return add_tag(zot, item_key, "extracted")


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
