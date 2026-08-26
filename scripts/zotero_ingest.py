#!/usr/bin/env python3
"""Batch-ingest Zotero sources into the knowledge base.

Determines pending items by diffing the Zotero library against a git-side
manifest (knowledge/MANIFEST.jsonl). Downloads PDFs, runs agentic-mbse
extract, appends entries to SOURCE_INDEX.md, and records to the manifest.
Zotero tagging is deferred to a separate --sync-tags step.

Usage:
    uv run python scripts/zotero_ingest.py                    # process all pending
    uv run python scripts/zotero_ingest.py --dry-run           # list pending items
    uv run python scripts/zotero_ingest.py --budget 0          # no Claude enhancement
    uv run python scripts/zotero_ingest.py --model sonnet      # use sonnet instead of opus
    uv run python scripts/zotero_ingest.py --re-extract        # re-extract existing sources
    uv run python scripts/zotero_ingest.py --local-pdf path.pdf
    uv run python scripts/zotero_ingest.py --sync-tags         # tag manifested items in Zotero

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
    add_tag,
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

# -- agentic-mbse extraction interface --
# These reflect the agentic-mbse CLI contract. Update here if upstream changes.
EXTRACT_OUTPUT = "output.md"
EXTRACT_LEGACY_FILES = ("full_document.md", "summary.json", "style.json")
DEFAULT_BUDGET = 50.0
DEFAULT_MODEL = "opus"


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
        "--budget", type=float, default=DEFAULT_BUDGET,
        help=f"Claude budget in USD per document (default: {DEFAULT_BUDGET}, 0 = no Claude)",
    )
    parser.add_argument(
        "--model", choices=["opus", "sonnet", "haiku"], default=DEFAULT_MODEL,
        help=f"Claude model for enhancement (default: {DEFAULT_MODEL})",
    )
    parser.add_argument(
        "--re-extract", action="store_true",
        help="Re-extract all manifested sources (uses --force, cleans up legacy files)",
    )
    parser.add_argument(
        "--keep-legacy", action="store_true",
        help="Keep old extraction files (full_document.md, etc.) for comparison",
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
    parser.add_argument(
        "--add-tag",
        nargs="+",
        metavar=("TAG", "KEY"),
        help="Add a tag to specific Zotero items: --add-tag TAG KEY1 KEY2 ...",
    )
    return parser.parse_args()


def run_extraction(
    pdf_path: Path, output_dir: Path, *,
    budget: float = DEFAULT_BUDGET, model: str = DEFAULT_MODEL, force: bool = False,
) -> bool:
    """Run agentic-mbse extract on a PDF. Returns True on success.

    After extraction, flattens the output if agentic-mbse created a nested
    subdirectory (its default behavior)."""
    cmd = [
        "uv", "run", "agentic-mbse", "extract", str(pdf_path),
        "--output", str(output_dir),
        "--index", "--summarize",
        "--budget", str(budget),
        "--model", model,
    ]
    if force:
        cmd.append("--force")

    # NOTE: This must be run from a terminal, not from within Claude Code.
    # The extraction pipeline invokes `claude` CLI for --summarize and
    # enhancement. Claude CLI refuses to run inside another Claude Code
    # session (detects CLAUDECODE env var). Symptoms: --summarize silently
    # fails, --check produces no output. See extraction-validation results.md.
    print(f"  Extracting: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
    if result.returncode != 0:
        print(f"  Extraction failed (exit {result.returncode})")
        if result.stderr:
            for line in result.stderr.strip().splitlines()[-5:]:
                print(f"    {line}")
        return False

    # Surface pipeline warnings (Claude failures, output rejection, summary)
    if result.stderr:
        for line in result.stderr.strip().splitlines():
            if "WARNING" in line:
                print(f"  {line.strip()}")

    _flatten_extraction_output(output_dir)
    return True


def _flatten_extraction_output(output_dir: Path) -> None:
    """If agentic-mbse extract created a nested subdir, move contents up.

    Handles re-extraction: even if output.md already exists at the parent level,
    a nested subdir with a newer output.md means new extraction output needs
    to be flattened (overwriting old files)."""
    # Find subdirs containing extraction output (may be >1 subdir during re-extraction
    # when old dirs like images/ already exist)
    subdirs = [d for d in output_dir.iterdir() if d.is_dir()]
    candidates = [d for d in subdirs if (d / EXTRACT_OUTPUT).exists()]
    if len(candidates) != 1:
        return  # already flat, or ambiguous (shouldn't happen)
    nested = candidates[0]
    for item in nested.iterdir():
        dest = output_dir / item.name
        if item.is_file():
            item.rename(dest)  # atomically replaces existing files on Linux
        elif not dest.exists():
            item.rename(dest)
    # Remove the now-empty nested dir
    if not any(nested.iterdir()):
        nested.rmdir()
    print(f"  Flattened extraction output from {nested.name}/")


def _cleanup_legacy_files(output_dir: Path) -> None:
    """Remove legacy extraction files if new output exists."""
    if not (output_dir / EXTRACT_OUTPUT).exists():
        return
    for name in EXTRACT_LEGACY_FILES:
        legacy = output_dir / name
        if legacy.exists():
            legacy.unlink()
            print(f"  Removed legacy file: {name}")


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


SEAM_ANCHOR = "\n## How Sources Are Used"


def append_source_index_entry(
    title: str,
    slug: str,
    extract_sha256: str,
    *,
    profile: str = "zotero-batch",
    item_key: str | None = None,
    pdf_sha256: str | None = None,
    source_kind: str | None = None,
    source_url: str | None = None,
    origin_path: str | None = None,
    use_for: str | None = None,
    validation: str | None = None,
    caveat: str | None = None,
    source_id: str | None = None,
    raw_sha256: str | None = None,
    raw_artifact_sha256: str | None = None,
) -> None:
    """Insert one SOURCE_INDEX.md block before the 'How Sources Are Used' section.

    Two profiles, one writer (design D6). `zotero-batch` reproduces the block the
    unattended Zotero ingest has always written, empty `Use for`/`Validation`
    included, because a batch caller has no per-item prose to supply. `seam`
    requires the prose fields and an origin, and refuses without them.

    Raises RuntimeError if the anchor heading is absent — a missing anchor means
    the index is not the file this writer was built for, and appending at the end
    would put new sources after the explanatory section (design D5).
    """
    if profile == "seam":
        lines = _seam_block_lines(
            title=title, slug=slug, source_kind=source_kind, source_url=source_url,
            origin_path=origin_path, use_for=use_for, validation=validation,
            caveat=caveat, source_id=source_id, raw_sha256=raw_sha256,
            raw_artifact_sha256=raw_artifact_sha256, extract_sha256=extract_sha256,
        )
    elif profile == "zotero-batch":
        lines = _zotero_batch_block_lines(
            title=title, slug=slug, item_key=item_key,
            pdf_sha256=pdf_sha256, extract_sha256=extract_sha256,
        )
    else:
        raise ValueError(f"unknown index-block profile: {profile!r}")

    entry_block = "\n".join(lines)
    content = SOURCE_INDEX_PATH.read_text()
    if SEAM_ANCHOR not in content:
        raise RuntimeError(
            f"{SOURCE_INDEX_PATH}: anchor '## How Sources Are Used' not found; "
            "refusing to write an index block into a file this writer does not recognise"
        )
    SOURCE_INDEX_PATH.write_text(
        content.replace(SEAM_ANCHOR, f"\n{entry_block}\n{SEAM_ANCHOR}", 1)
    )
    print(f"  Appended SOURCE_INDEX.md entry: {title}")


def _zotero_batch_block_lines(
    *, title: str, slug: str, item_key: str | None,
    pdf_sha256: str | None, extract_sha256: str,
) -> list[str]:
    """Today's block, unchanged. `Use for` and `Validation` stay empty by design."""
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
        f"- **Date Added**: {date.today().isoformat()}",
    ])
    return lines


def _seam_block_lines(
    *, title: str, slug: str, source_kind: str | None, source_url: str | None,
    origin_path: str | None, use_for: str | None, validation: str | None,
    caveat: str | None, source_id: str | None, raw_sha256: str | None,
    raw_artifact_sha256: str | None, extract_sha256: str,
) -> list[str]:
    """The seam block: every field required by spec R-B6, or a refusal."""
    blank = [
        name for name, value in
        (("use_for", use_for), ("validation", validation), ("caveat", caveat))
        if not (value or "").strip()
    ]
    if blank:
        raise ValueError(
            "seam-profile index block requires non-empty "
            + ", ".join(blank)
            + " (spec R-B6)"
        )
    if not (source_url or "").strip() and not (origin_path or "").strip():
        raise ValueError("seam-profile index block requires source_url or origin_path")

    origin_line = (
        f"- **Source URL**: {source_url}" if (source_url or "").strip()
        else f"- **Origin Path**: {origin_path}"
    )
    return [
        f"### {title}",
        f"- **Type**: {source_kind or 'documentation'}",
        f"- **Location**: knowledge/sources/{slug}/",
        f"- **Use for**: {use_for}",
        f"- **Validation**: {validation}",
        f"- **Caveat**: {caveat}",
        "",
        "#### Extended Metadata",
        origin_line,
        f"- **Source ID**: {source_id}",
        f"- **Raw SHA256**: {raw_sha256}",
        f"- **Raw Artifact SHA256**: {raw_artifact_sha256}",
        f"- **Extracted Path**: knowledge/sources/{slug}/",
        f"- **Extract SHA256**: {extract_sha256}",
        f"- **Date Added**: {date.today().isoformat()}",
    ]


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


def re_extract_sources(zot, args) -> None:
    """Re-extract all manifested sources with the current pipeline."""
    manifest = load_manifest()
    if not manifest:
        print("Manifest is empty — nothing to re-extract.")
        return

    items = list(manifest.values())
    if args.limit:
        items = items[:args.limit]

    if args.dry_run:
        print(f"\n{len(items)} source(s) would be re-extracted:\n")
        for entry in items:
            print(f"  [{entry['zotero_key']}] {entry['title']}")
            print(f"           slug: {entry['slug']}")
        return

    print(f"\n{len(items)} source(s) to re-extract")
    stats = {"found": len(items), "extracted": 0, "skipped": 0, "failed": 0}

    for entry in items:
        slug = entry["slug"]
        title = entry["title"]
        zotero_key = entry["zotero_key"]
        output_dir = SOURCES_DIR / slug
        print(f"\n--- {title} [{zotero_key}] ---")

        # Resolve PDF (download if not cached)
        try:
            item = zot.item(zotero_key)
        except Exception as e:
            print(f"  Failed to fetch Zotero item: {e}")
            stats["failed"] += 1
            continue

        pdf_info = resolve_pdf_info(zot, item)
        if pdf_info is None:
            print(f"  No PDF attachment — skipping")
            stats["skipped"] += 1
            continue

        try:
            dl_result = download_pdf_from_info(zot, pdf_info, args.output_dir)
        except RuntimeError as e:
            print(f"  Download failed: {e}")
            stats["failed"] += 1
            continue

        # Run extraction with --force
        try:
            ok = run_extraction(
                dl_result.path, output_dir,
                budget=args.budget, model=args.model, force=True,
            )
        except subprocess.TimeoutExpired:
            print(f"  Extraction timed out")
            stats["failed"] += 1
            continue
        if not ok:
            stats["failed"] += 1
            continue

        # Clean up legacy files
        if not args.keep_legacy:
            _cleanup_legacy_files(output_dir)

        # Report new SHA256
        extract_doc = output_dir / EXTRACT_OUTPUT
        if extract_doc.exists():
            new_sha = sha256_of(extract_doc)
            print(f"  New {EXTRACT_OUTPUT} SHA256: {new_sha[:16]}...")
        stats["extracted"] += 1

    print_summary(stats)


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
        ok = run_extraction(result.path, output_dir, budget=args.budget, model=args.model)
    except subprocess.TimeoutExpired:
        print(f"  Extraction timed out")
        return "failed"
    if not ok:
        return "failed"

    # Step 7: Compute SHA256 of output.md
    extract_doc = output_dir / EXTRACT_OUTPUT
    if not extract_doc.exists():
        print(f"  WARNING: {EXTRACT_OUTPUT} not found at {extract_doc}")
        extract_sha = "(not found)"
    else:
        extract_sha = sha256_of(extract_doc)

    # Step 8: Append SOURCE_INDEX.md entry
    try:
        append_source_index_entry(
            title=title, slug=slug, item_key=item_key,
            pdf_sha256=result.sha256, extract_sha256=extract_sha,
        )
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
        ok = run_extraction(raw_copy, output_dir, budget=args.budget, model=args.model)
    except subprocess.TimeoutExpired:
        print(f"  Extraction timed out")
        print(f"\nSummary: 1 found, 0 extracted, 0 skipped (no PDF), 1 failed")
        sys.exit(1)
    if not ok:
        print(f"\nSummary: 1 found, 0 extracted, 0 skipped (no PDF), 1 failed")
        sys.exit(1)

    # Compute extract SHA256
    extract_doc = output_dir / EXTRACT_OUTPUT
    if not extract_doc.exists():
        print(f"  WARNING: {EXTRACT_OUTPUT} not found at {extract_doc}")
        extract_sha = "(not found)"
    else:
        extract_sha = sha256_of(extract_doc)

    # Append SOURCE_INDEX.md entry (no Zotero key)
    append_source_index_entry(
        title=title, slug=slug, item_key=None,
        pdf_sha256=pdf_sha256, extract_sha256=extract_sha,
    )

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

    # Handle --add-tag early exit
    if args.add_tag:
        tag_name = args.add_tag[0]
        keys = args.add_tag[1:]
        if not keys:
            print("ERROR: --add-tag requires TAG followed by one or more KEYs")
            sys.exit(1)
        print(f"Adding tag '{tag_name}' to {len(keys)} item(s)...")
        added = 0
        for key in keys:
            try:
                if add_tag(zot, key, tag_name):
                    added += 1
            except Exception as e:
                print(f"  WARNING: Failed to tag {key}: {e}")
        print(f"Done. {added} newly tagged, {len(keys) - added} already tagged or failed.")
        return

    # Handle --sync-tags early exit
    if args.sync_tags:
        sync_tags_command(zot)
        return

    # Handle --re-extract early exit
    if args.re_extract:
        re_extract_sources(zot, args)
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
