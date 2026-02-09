#!/usr/bin/env python3
"""Batch-ingest Zotero sources into the knowledge base.

Queries the 1cfe Zotero group library for items tagged 'new' (but not
'extracted'), downloads their PDFs, runs agentic-mbse extract, appends
entries to SOURCE_INDEX.md, and tags items as 'extracted'.

Usage:
    uv run python scripts/zotero_ingest.py
    uv run python scripts/zotero_ingest.py --dry-run
    uv run python scripts/zotero_ingest.py --no-enhance
    uv run python scripts/zotero_ingest.py --local-pdf knowledge/raw/some_paper.pdf

Requires .env with:
    ZOTERO_KEY=<api-key>  (not needed for --local-pdf)
"""

import argparse
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

from zotero_lib import (
    GROUP_ID,
    RAW_DIR,
    SOURCE_INDEX_PATH,
    SOURCES_DIR,
    connect,
    download_pdf,
    find_pdf_attachment,
    load_api_key,
    sha256_of,
    slugify,
    tag_extracted,
)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Batch-ingest Zotero sources into the knowledge base."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List pending items without processing",
    )
    parser.add_argument(
        "--local-pdf",
        type=Path,
        help="Process a local PDF (bypass Zotero query)",
    )
    parser.add_argument(
        "--no-enhance",
        action="store_true",
        help="Disable --enhance (use basic extraction only)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=RAW_DIR,
        help=f"Override raw PDF download dir (default: {RAW_DIR})",
    )
    return parser.parse_args()


def run_extraction(pdf_path: Path, output_dir: Path, enhance: bool) -> bool:
    """Run agentic-mbse extract on a PDF. Returns True on success.

    After extraction, flattens the output if agentic-mbse created a nested
    subdirectory (its default behavior)."""
    cmd = [
        "uv", "run", "agentic-mbse", "extract", str(pdf_path),
        "--output", str(output_dir),
        "--index", "--summarize",
    ]
    if enhance:
        cmd.append("--enhance")

    print(f"  Extracting: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
    if result.returncode != 0:
        print(f"  Extraction failed (exit {result.returncode})")
        if result.stderr:
            for line in result.stderr.strip().splitlines()[-5:]:
                print(f"    {line}")
        return False

    _flatten_extraction_output(output_dir)
    return True


def _flatten_extraction_output(output_dir: Path) -> None:
    """If agentic-mbse extract created a single nested subdir, move contents up."""
    if (output_dir / "full_document.md").exists():
        return  # already flat
    subdirs = [d for d in output_dir.iterdir() if d.is_dir()]
    if len(subdirs) == 1 and (subdirs[0] / "full_document.md").exists():
        nested = subdirs[0]
        for item in nested.iterdir():
            dest = output_dir / item.name
            if dest.exists():
                # Don't overwrite existing files
                continue
            item.rename(dest)
        # Remove the now-empty nested dir (may still have conflicts left)
        if not any(nested.iterdir()):
            nested.rmdir()
        print(f"  Flattened extraction output from {nested.name}/")


def resolve_slug(slug: str, item_key: str | None) -> str:
    """Resolve slug collision against knowledge/sources/.
    Zotero items: append _<item_key>. Local PDFs: append _2, _3, etc."""
    if not (SOURCES_DIR / slug).exists():
        return slug

    if item_key is not None:
        return f"{slug}_{item_key}"

    # Numeric suffix for local PDFs
    n = 2
    while (SOURCES_DIR / f"{slug}_{n}").exists():
        n += 1
    return f"{slug}_{n}"


def append_source_index_entry(
    title: str,
    slug: str,
    item_key: str | None,
    pdf_sha256: str,
    extract_sha256: str,
) -> None:
    """Append a new entry to SOURCE_INDEX.md before the 'How MBSE Commands Use This File' section."""
    today = date.today().isoformat()

    lines = [
        f"### {title}",
        "- **Type**: documentation",
        f"- **Location**: knowledge/sources/{slug}/",
        "- **Use for**:",
        "- **Validation**:",
        "",
        "#### Extended Metadata",
    ]

    if item_key is not None:
        lines.append(f"- **Zotero Key**: {GROUP_ID}:{item_key}")

    lines.extend([
        f"- **Raw SHA256**: {pdf_sha256}",
        f"- **Extracted Path**: knowledge/sources/{slug}/",
        f"- **Extract SHA256**: {extract_sha256}",
        f"- **Date Added**: {today}",
    ])

    entry_block = "\n".join(lines)

    content = SOURCE_INDEX_PATH.read_text()
    marker = "\n## How MBSE Commands Use This File"
    if marker in content:
        content = content.replace(marker, f"\n{entry_block}\n{marker}")
    else:
        print("  WARNING: '## How MBSE Commands Use This File' not found, appending to end")
        content = content.rstrip() + f"\n\n{entry_block}\n"

    SOURCE_INDEX_PATH.write_text(content)
    print(f"  Appended SOURCE_INDEX.md entry: {title}")


def process_zotero_item(zot, item: dict, args) -> str:
    """Process a single Zotero item through the full pipeline.
    Returns 'extracted', 'skipped', or 'failed'."""
    title = item["data"].get("title", "(no title)")
    item_key = item["key"]

    print(f"\n--- {title} [{item_key}] ---")

    # Step 1-2: Find PDF attachment
    pdf_child = find_pdf_attachment(zot, item_key)
    if pdf_child is None:
        print(f"  No PDF attachment — skipping")
        return "skipped"

    # Step 3: Download PDF
    try:
        result = download_pdf(zot, item_key, args.output_dir)
    except RuntimeError as e:
        print(f"  Download failed: {e}")
        return "failed"

    # Step 4-5: Generate and resolve slug
    slug = slugify(title)
    slug = resolve_slug(slug, item_key)
    output_dir = SOURCES_DIR / slug

    # Step 6: Run extraction
    try:
        ok = run_extraction(result.path, output_dir, enhance=not args.no_enhance)
    except subprocess.TimeoutExpired:
        print(f"  Extraction timed out")
        return "failed"
    if not ok:
        return "failed"

    # Step 7: Compute SHA256 of full_document.md
    full_doc = output_dir / "full_document.md"
    if not full_doc.exists():
        print(f"  WARNING: full_document.md not found at {full_doc}")
        extract_sha = "(not found)"
    else:
        extract_sha = sha256_of(full_doc)

    # Step 8: Append SOURCE_INDEX.md entry
    try:
        append_source_index_entry(title, slug, item_key, result.sha256, extract_sha)
    except Exception as e:
        print(f"  Failed to update SOURCE_INDEX.md: {e}")
        return "failed"

    # Step 9: Tag item as extracted
    try:
        tag_extracted(zot, item_key)
    except Exception as e:
        print(f"  WARNING: Tagging failed: {e}")
        # Still count as extracted since files are in place

    # Step 10: Success
    return "extracted"


def print_dry_run(zot, items: list) -> None:
    """List pending items without processing."""
    if not items:
        print("0 items found matching tag=['new', '-extracted']")
        return

    print(f"{len(items)} item(s) pending:\n")
    for item in items:
        title = item["data"].get("title", "(no title)")
        item_key = item["key"]
        pdf_child = find_pdf_attachment(zot, item_key)
        if pdf_child:
            filename = pdf_child["data"]["filename"]
            print(f"  [{item_key}] {title}")
            print(f"           PDF: {filename}")
        else:
            print(f"  [{item_key}] {title}")
            print(f"           (no PDF — will skip)")


def print_summary(stats: dict) -> None:
    """Print batch processing summary."""
    parts = [
        f"{stats['found']} found",
        f"{stats['extracted']} extracted",
        f"{stats['skipped']} skipped (no PDF)",
        f"{stats['failed']} failed",
    ]
    print(f"\nSummary: {', '.join(parts)}")


def process_local_pdf(args) -> None:
    """Process a local PDF without Zotero."""
    pdf_path = args.local_pdf
    if not pdf_path.exists():
        print(f"ERROR: File not found: {pdf_path}")
        sys.exit(1)

    title = " ".join(pdf_path.stem.replace("_", " ").replace("-", " ").split()).title()
    slug = slugify(pdf_path.stem)
    slug = resolve_slug(slug, item_key=None)
    output_dir = SOURCES_DIR / slug

    print(f"\n--- {title} (local PDF) ---")

    # Copy to raw dir if not already there
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    raw_copy = RAW_DIR / pdf_path.name
    if pdf_path.resolve() == raw_copy.resolve():
        print(f"  Source is already in {RAW_DIR}: {pdf_path.name}")
    elif not raw_copy.exists():
        shutil.copy2(pdf_path, raw_copy)
        print(f"  Copied to {raw_copy}")
    else:
        print(f"  Already in {RAW_DIR}: {pdf_path.name}")

    pdf_sha256 = sha256_of(raw_copy)

    # Run extraction
    try:
        ok = run_extraction(raw_copy, output_dir, enhance=not args.no_enhance)
    except subprocess.TimeoutExpired:
        print(f"  Extraction timed out")
        print(f"\nSummary: 1 found, 0 extracted, 0 skipped (no PDF), 1 failed")
        sys.exit(1)
    if not ok:
        print(f"\nSummary: 1 found, 0 extracted, 0 skipped (no PDF), 1 failed")
        sys.exit(1)

    # Compute extract SHA256
    full_doc = output_dir / "full_document.md"
    if not full_doc.exists():
        print(f"  WARNING: full_document.md not found at {full_doc}")
        extract_sha = "(not found)"
    else:
        extract_sha = sha256_of(full_doc)

    # Append SOURCE_INDEX.md entry (no Zotero key)
    append_source_index_entry(title, slug, item_key=None, pdf_sha256=pdf_sha256, extract_sha256=extract_sha)

    print(f"\nSummary: 1 found, 1 extracted, 0 skipped (no PDF), 0 failed")


def main():
    args = parse_args()

    if args.local_pdf:
        process_local_pdf(args)
        return

    try:
        api_key = load_api_key()
    except ValueError as e:
        print(f"ERROR: {e}")
        sys.exit(1)

    zot = connect(api_key)

    # Smart pull: items tagged 'new' but NOT 'extracted'
    print("Querying Zotero for items tagged 'new' (not 'extracted')...")
    items = zot.everything(zot.top(tag=["new", "-extracted"]))
    print(f"Found {len(items)} item(s)")

    if args.dry_run:
        print_dry_run(zot, items)
        return

    stats = {"found": len(items), "extracted": 0, "skipped": 0, "failed": 0}

    for item in items:
        result = process_zotero_item(zot, item, args)
        stats[result] += 1

    print_summary(stats)


if __name__ == "__main__":
    main()
