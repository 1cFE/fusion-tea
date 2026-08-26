"""Characterization test — pins today's Zotero-path output before the refactor.

Written against unmodified `zotero_ingest` / `zotero_lib`. It fixes the index
block's field names and order, the manifest row's shape, and Zotero-key dedupe,
so the seam refactor cannot drift them (spec R-B1c, R-E5).

Insertion *position* is pinned in `test_index_writer.py` instead: today's
position is the warn-then-append fallback that design D5 removes.
"""

import json
import re

import pytest

from zotero_ingest import append_source_index_entry
from zotero_lib import append_manifest_entry, load_manifest, manifest_keys

FIELD_RE = re.compile(r"^- \*\*(?P<name>[^*]+)\*\*:", re.MULTILINE)


def _field_order(block: str) -> list[str]:
    return FIELD_RE.findall(block)


def _block_for(tree, title: str) -> str:
    return tree.index.read_text().split(f"### {title}", 1)[1]


def test_zotero_index_block_field_names_and_order(knowledge_tree):
    append_source_index_entry(
        title="T", slug="t", item_key="ABC",
        pdf_sha256="a" * 64, extract_sha256="b" * 64,
    )
    assert _field_order(_block_for(knowledge_tree, "T")) == [
        "Type", "Location", "Use for", "Validation",
        "Zotero Key", "Raw SHA256", "Extracted Path", "Extract SHA256", "Date Added",
    ]


def test_zotero_block_values_are_unchanged(knowledge_tree):
    append_source_index_entry(
        title="T", slug="t", item_key="ABC",
        pdf_sha256="a" * 64, extract_sha256="b" * 64,
    )
    block = _block_for(knowledge_tree, "T")
    assert "- **Type**: documentation" in block
    assert "- **Location**: knowledge/sources/t/" in block
    assert "- **Use for**:\n" in block          # deliberately empty in this profile
    assert "- **Validation**:\n" in block
    assert "- **Zotero Key**: 5428393:ABC" in block
    assert "#### Extended Metadata" in block


def test_local_pdf_block_omits_zotero_key(knowledge_tree):
    append_source_index_entry(
        title="Local", slug="local", item_key=None,
        pdf_sha256="c" * 64, extract_sha256="d" * 64,
    )
    assert "Zotero Key" not in _field_order(_block_for(knowledge_tree, "Local"))


def test_manifest_row_shape_and_zotero_dedupe(knowledge_tree):
    append_manifest_entry("ABC", "t", "T")
    row = json.loads(knowledge_tree.manifest.read_text().strip())
    assert set(row) == {"zotero_key", "slug", "title", "date_extracted"}
    assert manifest_keys() == {"ABC"}
    assert load_manifest()["ABC"] == row


def test_loaders_tolerate_rows_without_zotero_key(knowledge_tree):
    knowledge_tree.manifest.write_text(
        json.dumps({"source_id": "a" * 64, "slug": "s"}) + "\n"
        + json.dumps({"zotero_key": "ABC", "slug": "t", "title": "T"}) + "\n"
    )
    assert manifest_keys() == {"ABC"}
    assert set(load_manifest()) == {"ABC"}


def test_load_manifest_rows_returns_every_row(knowledge_tree):
    from zotero_lib import load_manifest_rows

    knowledge_tree.manifest.write_text(
        json.dumps({"source_id": "a" * 64, "slug": "s"}) + "\n"
        + json.dumps({"zotero_key": "ABC", "slug": "t"}) + "\n"
    )
    rows = load_manifest_rows(knowledge_tree.paths)
    assert [r["slug"] for r in rows] == ["s", "t"]


def test_truncate_manifest_restores_recorded_byte_length(knowledge_tree):
    from zotero_lib import truncate_manifest

    append_manifest_entry("ABC", "t", "T")
    mark = knowledge_tree.manifest.stat().st_size
    append_manifest_entry("DEF", "u", "U")
    truncate_manifest(mark, knowledge_tree.paths)
    assert manifest_keys() == {"ABC"}


@pytest.mark.parametrize("missing", ["title", "slug"])
def test_manifest_row_keeps_its_keys_for_existing_rows(knowledge_tree, missing):
    """Existing four-key rows are never rewritten (plan, Field spellings)."""
    append_manifest_entry("ABC", "t", "T")
    row = json.loads(knowledge_tree.manifest.read_text().strip())
    assert missing in row
