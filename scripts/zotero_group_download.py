#!/usr/bin/env python3
"""Download a PDF from the 1cfe Zotero group library.

Usage:
    uv run python scripts/zotero_group_download.py PMXLGPKG
    uv run python scripts/zotero_group_download.py PMXLGPKG --tag-extracted
    uv run python scripts/zotero_group_download.py PMXLGPKG --tag-only

Requires .env with:
    ZOTERO_KEY=<api-key>
"""

import sys
from pathlib import Path

from pyzotero.errors import PyZoteroError

from zotero_lib import (
    GROUP_ID,
    connect,
    download_pdf,
    find_pdf_attachment,
    load_api_key,
    tag_extracted,
)


def parse_args():
    import argparse

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


def main():
    args = parse_args()

    try:
        api_key = load_api_key()
    except ValueError as e:
        print(f"ERROR: {e}")
        sys.exit(1)

    zot = connect(api_key)

    try:
        if args.tag_only:
            tag_extracted(zot, args.item_key)
            return

        pdf_child = find_pdf_attachment(zot, args.item_key)
        if pdf_child is None:
            print(f"ERROR: No PDF attachment found for item {args.item_key}")
            sys.exit(1)

        result = download_pdf(zot, args.item_key, Path(args.output_dir))
    except (RuntimeError, PyZoteroError) as e:
        print(f"ERROR: {e}")
        sys.exit(1)

    print(f"Title: {result.title}")
    print(f"Zotero Key: {GROUP_ID}:{args.item_key}")
    print(f"Filename: {result.path.name}")
    print(f"Size: {result.path.stat().st_size:,} bytes")
    print(f"SHA256: {result.sha256}")
    print(f"Saved to: {result.path}")

    if args.tag_extracted:
        try:
            tag_extracted(zot, args.item_key)
        except PyZoteroError as e:
            print(f"ERROR: Failed to tag item: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()
