#!/usr/bin/env python3
"""Batch-ingest Zotero sources into the knowledge base.

Determines pending items by diffing the Zotero library against a git-side
manifest (knowledge/MANIFEST.jsonl). Downloads PDFs, runs agentic-mbse
extract, appends entries to SOURCE_INDEX.md, and records to the manifest.
Zotero tagging is deferred to a separate --sync-tags step.

Usage:
    uv run python scripts/zotero_ingest.py              # process all pending
    uv run python scripts/zotero_ingest.py --dry-run     # list pending items
    uv run python scripts/zotero_ingest.py --limit 5     # process at most 5
    uv run python scripts/zotero_ingest.py --tag new      # only items tagged 'new'
    uv run python scripts/zotero_ingest.py --sync-tags    # tag manifested items in Zotero
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
    MANIFEST_PATH,
    RAW_DIR,
    SOURCE_INDEX_PATH,
    SOURCES_DIR,
    append_manifest_entry,
    connect,
    download_pdf_from_info,
    load_api_key,
    load_manifest,
    manifest_keys,
    resolve_pdf_info,
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
    parser.add_argument(
        "--limit",
        type=int,
        help="Process at most N items per run",
    )
    parser.add_argument(
        "--tag",
        type=str,
        help="Only process items with this Zotero tag (e.g. --tag new)",
    )
    parser.add_argument(
        "--sync-tags",
        action="store_true",
        help="Tag all manifested items as 'extracted' in Zotero (run after committing)",
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


def fetch_all_processable_items(zot) -> list[dict]:
    """Fetch all Zotero items that could be processed.

    Returns parent items (from zot.top()) combined with standalone PDF
    attachments (itemType='attachment', contentType='application/pdf',
    no parentItem).
    """
    print("Fetching top-level items...")
    parent_items = zot.everything(zot.top())
    print(f"  {len(parent_items)} top-level items")

    print("Fetching standalone PDF attachments...")
    all_attachments = zot.everything(zot.items(itemType="attachment"))
    standalone_pdfs = [
        a for a in all_attachments
        if a["data"].get("contentType") == "application/pdf"
        and not a["data"].get("parentItem")
    ]
    print(f"  {len(standalone_pdfs)} standalone PDFs")

    # Dedup: standalone PDFs may also appear in zot.top()
    seen_keys = {i["key"] for i in parent_items}
    new_standalone = [a for a in standalone_pdfs if a["key"] not in seen_keys]
    if len(new_standalone) < len(standalone_pdfs):
        print(f"  ({len(standalone_pdfs) - len(new_standalone)} already in top-level, deduped)")

    return parent_items + new_standalone


def compute_pending_queue(all_items: list[dict], known_keys: set[str]) -> list[dict]:
    """Filter items to those not in the manifest."""
    return [i for i in all_items if i["key"] not in known_keys]


def sync_tags_command(zot) -> None:
    """Tag all manifested items as 'extracted' in Zotero."""
    manifest = load_manifest()
    if not manifest:
        print("Manifest is empty — nothing to sync.")
        return
    print(f"Syncing tags for {len(manifest)} manifest entries...")
    newly_tagged = 0
    already_tagged = 0
    for key in manifest:
        try:
            if tag_extracted(zot, key):
                newly_tagged += 1
            else:
                already_tagged += 1
        except Exception as e:
            print(f"  WARNING: Failed to tag {key}: {e}")
    print(f"Done. {newly_tagged} newly tagged, {already_tagged} already tagged.")


def process_zotero_item(zot, item: dict, args) -> str:
    """Process a single Zotero item through the full pipeline.
    Returns 'extracted', 'skipped', or 'failed'."""
    item_key = item["key"]

    # Step 1-2: Resolve PDF info (handles both parent items and standalone attachments)
    pdf_info = resolve_pdf_info(zot, item)
    if pdf_info is None:
        print(f"\n--- {item['data'].get('title', '(no title)')} [{item_key}] ---")
        print(f"  No PDF attachment — skipping")
        return "skipped"

    title = pdf_info.title
    print(f"\n--- {title} [{item_key}] ---")

    # Step 3: Download PDF
    try:
        result = download_pdf_from_info(zot, pdf_info, args.output_dir)
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

    # Step 9: Append to manifest (immediately, crash-safe)
    append_manifest_entry(item_key, slug, title)
    print(f"  Manifest updated: {item_key} → {slug}")

    return "extracted"


def print_dry_run(zot, items: list, total_items: int, known_count: int) -> None:
    """List pending items without processing."""
    print(f"\nLibrary: {total_items} total, {known_count} already extracted, {len(items)} pending\n")
    if not items:
        print("Nothing to process.")
        return

    for item in items:
        item_key = item["key"]
        pdf_info = resolve_pdf_info(zot, item)
        if pdf_info:
            print(f"  [{item_key}] {pdf_info.title}")
            print(f"           PDF: {pdf_info.filename}"
                  + (" (standalone)" if pdf_info.is_standalone else ""))
        else:
            title = item["data"].get("title", "(no title)")
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

    # Handle --sync-tags early exit
    if args.sync_tags:
        sync_tags_command(zot)
        return

    # Build queue by diffing Zotero library against manifest
    all_items = fetch_all_processable_items(zot)
    known = manifest_keys()
    pending = compute_pending_queue(all_items, known)

    # Optional tag filter
    if args.tag:
        pending = [
            i for i in pending
            if args.tag in [t["tag"] for t in i["data"].get("tags", [])]
        ]
        print(f"After --tag '{args.tag}' filter: {len(pending)} item(s)")

    # Optional batch limit
    if args.limit:
        pending = pending[:args.limit]
        print(f"After --limit {args.limit}: {len(pending)} item(s)")

    if args.dry_run:
        print_dry_run(zot, pending, total_items=len(all_items), known_count=len(known))
        return

    print(f"\n{len(pending)} item(s) to process")

    stats = {"found": len(pending), "extracted": 0, "skipped": 0, "failed": 0}

    for item in pending:
        result = process_zotero_item(zot, item, args)
        stats[result] += 1

    print_summary(stats)


if __name__ == "__main__":
    main()
