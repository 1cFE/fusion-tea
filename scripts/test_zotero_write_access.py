#!/usr/bin/env python3
"""Test that the Zotero API key has write access to the group library.

Verifies we can add and remove tags on items, which is required for the
ingestion pipeline to mark documents as 'extracted' after processing.

Usage:
    uv run python scripts/test_zotero_write_access.py

Requires .env with:
    ZOTERO_KEY=<api-key>
"""

import sys
from pathlib import Path

# scripts/ lives next to the project root; ensure zotero_lib is importable
sys.path.insert(0, str(Path(__file__).parent))

from zotero_lib import connect, load_api_key, GROUP_ID

TEST_TAG = "_write_access_test"


def get_item_tags(zot, item_key: str) -> list[str]:
    """Fetch current tags for an item from the API."""
    item = zot.item(item_key)
    return [t["tag"] for t in item["data"].get("tags", [])]


def add_test_tag(zot, item) -> None:
    """Add the test tag to an item."""
    zot.add_tags(item, TEST_TAG)


def remove_test_tag(zot, item_key: str) -> None:
    """Remove the test tag from an item, preserving all other tags."""
    item = zot.item(item_key)
    tags = item["data"].get("tags", [])
    updated_tags = [t for t in tags if t["tag"] != TEST_TAG]
    item["data"]["tags"] = updated_tags
    zot.update_item(item)


def main():
    print("=== Zotero Write Access Test ===\n")

    # Step 1: Connect
    try:
        api_key = load_api_key()
    except ValueError as e:
        print(f"FAIL: {e}")
        sys.exit(1)

    zot = connect(api_key)
    print(f"Connected to group library {GROUP_ID}")

    # Step 2: Find an item to test with
    items = zot.top(limit=5)
    if not items:
        print("FAIL: Library is empty -- need at least one item to test tagging")
        sys.exit(1)

    target = items[0]
    item_key = target["key"]
    title = target["data"].get("title", "(no title)")
    print(f"Test item: [{item_key}] {title}")

    # Record original tags so we can verify cleanup
    original_tags = get_item_tags(zot, item_key)
    print(f"Original tags: {original_tags}")

    if TEST_TAG in original_tags:
        print(f"  (stale test tag found -- will clean up first)")
        remove_test_tag(zot, item_key)
        original_tags = get_item_tags(zot, item_key)
        print(f"  Cleaned. Tags now: {original_tags}")

    # Step 3: Add test tag
    print(f"\nAdding tag '{TEST_TAG}'...")
    try:
        add_test_tag(zot, target)
    except Exception as e:
        print(f"FAIL: Could not add tag -- {e}")
        print("  The API key likely does not have write access to the group library.")
        sys.exit(1)

    # Step 4: Verify the tag persisted
    updated_tags = get_item_tags(zot, item_key)
    print(f"Tags after add: {updated_tags}")

    if TEST_TAG not in updated_tags:
        print(f"FAIL: Tag '{TEST_TAG}' was not found after add_tags call.")
        print("  The API may have silently rejected the write.")
        sys.exit(1)

    print(f"  PASSED: Tag '{TEST_TAG}' confirmed on server.")

    # Step 5: Clean up -- remove the test tag
    print(f"\nCleaning up: removing '{TEST_TAG}'...")
    try:
        remove_test_tag(zot, item_key)
    except Exception as e:
        print(f"WARNING: Cleanup failed -- {e}")
        print(f"  You may need to manually remove the '{TEST_TAG}' tag from [{item_key}]")
        # Still count as passed since the write succeeded
        print("\n=== RESULT: PASSED (with cleanup warning) ===")
        return

    final_tags = get_item_tags(zot, item_key)
    print(f"Tags after cleanup: {final_tags}")

    if TEST_TAG in final_tags:
        print(f"WARNING: Tag '{TEST_TAG}' still present after cleanup attempt")
    else:
        print(f"  Cleanup confirmed.")

    # Step 6: Also verify tag_extracted would work (dry check)
    print(f"\n--- Verifying tag_extracted() compatibility ---")
    from zotero_lib import tag_extracted
    try:
        # Add 'extracted' tag, then immediately remove it
        tag_extracted(zot, item_key)
        post_tags = get_item_tags(zot, item_key)
        if "extracted" in post_tags and "extracted" not in original_tags:
            # Remove it since it wasn't there originally
            item = zot.item(item_key)
            item["data"]["tags"] = [t for t in item["data"]["tags"] if t["tag"] != "extracted"]
            zot.update_item(item)
            print(f"  tag_extracted() works. Cleaned up 'extracted' tag.")
        elif "extracted" in original_tags:
            print(f"  Item already had 'extracted' tag -- tag_extracted() ran (no-op path).")
        else:
            print(f"  WARNING: 'extracted' tag not found after tag_extracted() call")
    except Exception as e:
        print(f"  WARNING: tag_extracted() raised: {e}")

    print("\n=== RESULT: PASSED -- Write access confirmed ===")
    print("The API key can add/remove tags on group library items.")
    print("The ingestion pipeline can now mark documents as 'extracted'.")


if __name__ == "__main__":
    main()
