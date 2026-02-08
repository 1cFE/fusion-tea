#!/usr/bin/env python3
"""Download a PDF from the 1cfe Zotero group library.

Usage:
    uv run python scripts/zotero_group_download.py PMXLGPKG
    uv run python scripts/zotero_group_download.py PMXLGPKG --tag-extracted
    uv run python scripts/zotero_group_download.py PMXLGPKG --tag-only

Requires .env with:
    ZOTERO_KEY=<api-key>
"""

import argparse
import hashlib
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from pyzotero import zotero

GROUP_ID = 5428393


def parse_args():
    parser = argparse.ArgumentParser(
        description="Download a PDF from the 1cfe Zotero group library."
    )
    parser.add_argument("item_key", help="Zotero item key to download")
    parser.add_argument(
        "--tag-extracted",
        action="store_true",
        help="Tag the item as 'extracted' after successful download",
    )
    parser.add_argument(
        "--tag-only",
        action="store_true",
        help="Skip download, just tag the item as 'extracted'",
    )
    parser.add_argument(
        "--output-dir",
        default="knowledge/raw/",
        help="Download destination (default: knowledge/raw/)",
    )
    return parser.parse_args()


def get_api_key():
    load_dotenv()
    api_key = os.environ.get("ZOTERO_KEY")
    if not api_key:
        print("ERROR: ZOTERO_KEY must be set in .env")
        sys.exit(1)
    return api_key


def find_pdf_attachment(zot, item_key):
    """Find the PDF child attachment for an item."""
    children = zot.children(item_key)
    pdfs = [
        c for c in children
        if c["data"].get("contentType") == "application/pdf"
    ]
    if not pdfs:
        print(f"ERROR: No PDF attachment found for item {item_key}")
        sys.exit(1)
    return pdfs[0]


def download_pdf(zot, item_key, output_dir):
    """Download PDF and return (filepath, metadata)."""
    item = zot.item(item_key)
    title = item["data"].get("title", "(no title)")
    pdf_child = find_pdf_attachment(zot, item_key)
    filename = pdf_child["data"]["filename"]
    child_key = pdf_child["key"]

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    filepath = output_path / filename

    if filepath.exists() and filepath.stat().st_size > 0:
        print(f"Already exists, skipping download: {filepath}")
    else:
        zot.dump(child_key, filename, str(output_path))

    if not filepath.exists() or filepath.stat().st_size == 0:
        print(f"ERROR: Download failed — file missing or empty at {filepath}")
        sys.exit(1)

    sha256 = hashlib.sha256(filepath.read_bytes()).hexdigest()
    size = filepath.stat().st_size

    print(f"Title: {title}")
    print(f"Zotero Key: {GROUP_ID}:{item_key}")
    print(f"Filename: {filename}")
    print(f"Size: {size:,} bytes")
    print(f"SHA256: {sha256}")
    print(f"Saved to: {filepath}")

    return filepath, title


def tag_item(zot, item_key):
    """Tag a Zotero item as 'extracted'."""
    item = zot.item(item_key)
    existing_tags = item["data"].get("tags", [])
    if any(t["tag"] == "extracted" for t in existing_tags):
        print(f"Item {item_key} already has tag 'extracted', skipping")
        return
    zot.add_tags(item, "extracted")
    print(f"Tagged {GROUP_ID}:{item_key} as 'extracted'")


def main():
    args = parse_args()
    api_key = get_api_key()

    zot = zotero.Zotero(GROUP_ID, "group", api_key)

    if args.tag_only:
        tag_item(zot, args.item_key)
        return

    download_pdf(zot, args.item_key, args.output_dir)

    if args.tag_extracted:
        tag_item(zot, args.item_key)


if __name__ == "__main__":
    main()
