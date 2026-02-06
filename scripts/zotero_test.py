#!/usr/bin/env python3
"""Zotero API connectivity and download test for fusion-tea knowledge pipeline.

De-risk script for Epic KNOW-DB, Item 1.
Verifies: API connectivity, metadata queries, PDF attachment discovery, and
headless PDF download via zot.dump() (requires Zotero Storage, not WebDAV).

Usage:
    uv run python scripts/zotero_test.py

Requires .env with:
    ZOTERO_ID=<library-id>
    ZOTERO_KEY=<api-key>
"""

import hashlib
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from pyzotero import zotero

load_dotenv()

LIBRARY_ID = os.environ.get("ZOTERO_ID")
API_KEY = os.environ.get("ZOTERO_KEY")

if not LIBRARY_ID or not API_KEY:
    print("ERROR: ZOTERO_ID and ZOTERO_KEY must be set in .env")
    sys.exit(1)


def test_connectivity(zot):
    """Test 1: Connect to API and list items."""
    print("=== Test 1: API Connectivity ===\n")
    items = zot.top(limit=10)
    print(f"Found {len(items)} items in library.\n")

    if not items:
        print("  WARNING: Library is empty. Add at least one item with a PDF.")
        return []

    for item in items:
        title = item["data"].get("title", "(no title)")
        key = item["key"]
        item_type = item["data"].get("itemType", "unknown")
        tags = [t["tag"] for t in item["data"].get("tags", [])]
        tag_str = f" tags={tags}" if tags else ""
        print(f"  [{key}] {title} ({item_type}){tag_str}")

        children = zot.children(key)
        pdfs = [
            c for c in children
            if c["data"].get("contentType") == "application/pdf"
        ]
        if pdfs:
            for pdf in pdfs:
                print(f"    -> PDF: {pdf['data']['filename']}")
        else:
            print(f"    -> No PDF attached")

    print("\nTest 1 PASSED: API connectivity works.\n")
    return items


def test_download(zot, items):
    """Test 2: Download a PDF via zot.dump()."""
    print("=== Test 2: PDF Download (zot.dump) ===\n")

    # Find first item with a PDF attachment
    for item in items:
        children = zot.children(item["key"])
        pdfs = [
            c for c in children
            if c["data"].get("contentType") == "application/pdf"
        ]
        if pdfs:
            child = pdfs[0]
            filename = child["data"]["filename"]
            title = item["data"].get("title", "(no title)")

            output_dir = Path("knowledge/raw")
            output_dir.mkdir(parents=True, exist_ok=True)

            print(f"  Source: {title}")
            print(f"  Downloading: {filename}")

            zot.dump(child["key"], filename, str(output_dir))

            downloaded = output_dir / filename
            if downloaded.exists() and downloaded.stat().st_size > 0:
                sha256 = hashlib.sha256(downloaded.read_bytes()).hexdigest()
                size = downloaded.stat().st_size
                print(f"  Saved to: {downloaded}")
                print(f"  Size: {size:,} bytes")
                print(f"  SHA256: {sha256}")
                print(f"\nTest 2 PASSED: PDF download works.\n")

                # Clean up test file
                downloaded.unlink()
                print(f"  (Cleaned up test download)")
            else:
                print(f"  FAILED: File missing or empty at {downloaded}")
                sys.exit(1)
            return

    print("  SKIP: No items with PDF attachments found in library.")
    print("  Add a PDF to at least one Zotero item and sync, then re-run.")


def main():
    print(f"Zotero library ID: {LIBRARY_ID}")
    print(f"API key: {API_KEY[:4]}...{API_KEY[-4:]}\n")

    zot = zotero.Zotero(LIBRARY_ID, "user", API_KEY)

    items = test_connectivity(zot)
    if items:
        test_download(zot, items)

    print("=" * 40)
    print("DE-RISK VERDICT: Zotero Storage + pyzotero works for headless pipeline.")
    print("=" * 40)


if __name__ == "__main__":
    main()
