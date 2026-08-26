"""Phase 3 — the index writer's two profiles and its fixed anchor (design D5, D6)."""

import re

import pytest
from zotero_ingest import append_source_index_entry

SEAM_KWARGS = dict(
    profile="seam",
    title="Coil Note",
    slug="coil_note",
    source_kind="url",
    source_url="http://127.0.0.1:1/coil.html",
    use_for="Winding-pack current density for the Nb3Sn arm; serves RQ-1.",
    validation="Cross-check the current against Fig. 1 of the source.",
    caveat="Conference preprint; not peer reviewed.",
    source_id="e" * 64,
    raw_sha256="e" * 64,
    raw_artifact_sha256="f" * 64,
    extract_sha256="0" * 64,
)

FIELD_RE = re.compile(r"^- \*\*(?P<name>[^*]+)\*\*:", re.MULTILINE)


def _block_for(tree, title: str) -> str:
    return tree.index.read_text().split(f"### {title}", 1)[1]


@pytest.mark.parametrize("blank", ["use_for", "validation", "caveat"])
def test_seam_profile_refuses_blank_prose_fields(knowledge_tree, blank):
    kwargs = SEAM_KWARGS | {blank: "  "}
    with pytest.raises(ValueError, match=blank):
        append_source_index_entry(**kwargs)
    assert knowledge_tree.index.read_text().count("### Coil Note") == 0


def test_seam_profile_refuses_without_a_source_url_or_origin(knowledge_tree):
    kwargs = {k: v for k, v in SEAM_KWARGS.items() if k != "source_url"}
    with pytest.raises(ValueError, match="source_url"):
        append_source_index_entry(**kwargs)


def test_seam_block_field_order(knowledge_tree):
    append_source_index_entry(**SEAM_KWARGS)
    assert FIELD_RE.findall(_block_for(knowledge_tree, "Coil Note")) == [
        "Type", "Location", "Use for", "Validation", "Caveat",
        "Source URL", "Source ID", "Raw SHA256", "Raw Artifact SHA256",
        "Extracted Path", "Extract SHA256", "Date Added",
    ]


def test_local_pdf_seam_block_uses_origin_path(knowledge_tree):
    kwargs = {k: v for k, v in SEAM_KWARGS.items() if k != "source_url"}
    kwargs |= {"source_kind": "local_pdf", "origin_path": "knowledge/raw/coil_note.pdf"}
    append_source_index_entry(**kwargs)
    block = _block_for(knowledge_tree, "Coil Note")
    assert "- **Origin Path**: knowledge/raw/coil_note.pdf" in block
    assert "Source URL" not in FIELD_RE.findall(block)


def test_seam_block_inserted_before_how_sources_are_used(knowledge_tree):
    append_source_index_entry(**SEAM_KWARGS)
    body = knowledge_tree.index.read_text()
    assert body.index("### Coil Note") < body.index("## How Sources Are Used")


def test_zotero_batch_block_also_lands_before_the_anchor(knowledge_tree):
    """The characterization test pins the block's fields; this pins its new position."""
    append_source_index_entry(title="T", slug="t", item_key="ABC",
                              pdf_sha256="a" * 64, extract_sha256="b" * 64)
    body = knowledge_tree.index.read_text()
    assert body.index("### T") < body.index("## How Sources Are Used")


def test_missing_anchor_raises_and_writes_nothing(knowledge_tree):
    knowledge_tree.index.write_text("# Source Index\n")
    with pytest.raises(RuntimeError, match="How Sources Are Used"):
        append_source_index_entry(**SEAM_KWARGS)
    assert knowledge_tree.index.read_text() == "# Source Index\n"


def test_two_seam_blocks_stack_in_write_order(knowledge_tree):
    append_source_index_entry(**SEAM_KWARGS)
    append_source_index_entry(**(SEAM_KWARGS | {"title": "Second", "slug": "second"}))
    body = knowledge_tree.index.read_text()
    assert (body.index("### Coil Note")
            < body.index("### Second")
            < body.index("## How Sources Are Used"))
