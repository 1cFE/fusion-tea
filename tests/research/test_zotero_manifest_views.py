"""The Zotero views of the manifest: `zotero_lib.load_manifest` and `manifest_keys`.

They read the registry's rows through `agentic_mbse.research.load_manifest_rows`
and keep only rows carrying a `zotero_key`, because they are the Zotero library
diff, not the whole registry. Rows registered another way carry no key and are
skipped.
"""

import json

from zotero_lib import load_manifest, manifest_keys


def _write_rows(tree, *rows: dict) -> None:
    tree.manifest.write_text("".join(json.dumps(row) + "\n" for row in rows))


def test_views_skip_rows_without_a_zotero_key(knowledge_tree):
    url_row = {
        "source_id": "a" * 64,
        "source_kind": "url",
        "slug": "s",
        "source_url": "https://example.org/s",
    }
    zotero_row = {"zotero_key": "ABC", "slug": "t", "title": "T", "date_extracted": "2026-01-01"}
    _write_rows(knowledge_tree, url_row, zotero_row)

    assert manifest_keys() == {"ABC"}
    assert load_manifest() == {"ABC": zotero_row}


def test_views_read_pre_seam_and_keyed_rows_alike(knowledge_tree):
    """A four-field row from before the seam and a row registered as a keyed source both count."""
    pre_seam = {"zotero_key": "OLD1", "slug": "old", "title": "Old", "date_extracted": "2026-01-01"}
    keyed = {
        "source_id": "b" * 64,
        "source_kind": "zotero",
        "slug": "new",
        "title": "New",
        "zotero_key": "NEW1",
        "raw_sha256": "b" * 64,
        "raw_artifact_sha256": "c" * 64,
        "extract_sha256": "d" * 64,
        "date_extracted": "2026-10-12",
    }
    _write_rows(knowledge_tree, pre_seam, keyed)

    assert manifest_keys() == {"OLD1", "NEW1"}
    assert load_manifest()["NEW1"] == keyed


def test_views_are_empty_without_a_manifest(knowledge_tree):
    knowledge_tree.manifest.unlink()

    assert load_manifest() == {}
    assert manifest_keys() == set()
