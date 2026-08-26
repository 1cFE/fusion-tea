"""Phase 4, first proof point — a URL goes from loopback fixture to registry entry.

The real `agentic-mbse extract` subprocess runs; nothing about capture is stubbed.
This is what proves design D1 (two hashes with two jobs), bet B2 (the extract
contract) and bet B5 (an offline fixture set predicts live behaviour) together.
"""

import hashlib
import json
import re

import pytest
import source_registry
from source_registry import SourceMetadata, UrlSource

FRONTMATTER_HASH = re.compile(r'^content_hash_sha256: "([0-9a-f]{64})"', re.MULTILINE)

METADATA = SourceMetadata(
    title="Widget Coil Note",
    use_for="Synthetic winding-pack geometry; exercises the URL capture chain.",
    validation="Compare the quoted dimensions against the fixture page itself.",
    caveat="A test fixture. It states nothing about any real machine.",
)


def _only_row(tree) -> dict:
    rows = [json.loads(line) for line in tree.manifest.read_text().splitlines() if line.strip()]
    assert len(rows) == 1, rows
    return rows[0]


def _block_for(tree, title: str) -> str:
    body = tree.index.read_text()
    return body.split(f"### {title}", 1)[1].split("\n## ", 1)[0]


def _register(local_site, tree, page="utf8.html", metadata=METADATA):
    return source_registry.register(
        UrlSource(url=local_site.url(page)), metadata, paths=tree.paths
    )


def test_utf8_page_registers_with_full_provenance(local_site, knowledge_tree):
    result = _register(local_site, knowledge_tree)
    assert result.outcome == "registered", result.reason

    row = _only_row(knowledge_tree)
    frontmatter_hash = FRONTMATTER_HASH.search((result.path / "output.md").read_text()).group(1)

    assert row["source_kind"] == "url"
    assert row["source_id"] == row["raw_sha256"] == frontmatter_hash
    assert row["raw_artifact_sha256"] == hashlib.sha256(
        (result.path / "raw.html").read_bytes()).hexdigest()
    assert row["extract_sha256"] == hashlib.sha256(
        (result.path / "output.md").read_bytes()).hexdigest()
    assert row["source_url"] == local_site.url("utf8.html")
    assert "origin_path" not in row and "zotero_key" not in row
    assert row["slug"] == result.slug and row["title"] == METADATA.title


def test_registered_source_id_is_the_digest_of_the_bytes_as_fetched(local_site, knowledge_tree):
    result = _register(local_site, knowledge_tree)
    served = hashlib.sha256(local_site.fetched_bytes("utf8.html")).hexdigest()
    assert result.source_id == served


def test_latin1_page_registers_and_the_two_hashes_differ(local_site, knowledge_tree):
    """C1/B5: `raw.html` is written re-encoded, so identity and integrity part ways."""
    result = _register(local_site, knowledge_tree, page="latin1.html")
    assert result.outcome == "registered", result.reason

    row = _only_row(knowledge_tree)
    served = hashlib.sha256(local_site.fetched_bytes("latin1.html")).hexdigest()
    stored = hashlib.sha256((result.path / "raw.html").read_bytes()).hexdigest()

    assert row["raw_sha256"] == served
    assert row["raw_artifact_sha256"] == stored
    assert row["raw_sha256"] != row["raw_artifact_sha256"]


def test_index_block_carries_every_required_field(local_site, knowledge_tree):
    result = _register(local_site, knowledge_tree)
    block = _block_for(knowledge_tree, METADATA.title)
    for field, value in [
        ("Use for", METADATA.use_for),
        ("Validation", METADATA.validation),
        ("Caveat", METADATA.caveat),
        ("Source URL", local_site.url("utf8.html")),
        ("Source ID", result.source_id),
        ("Raw SHA256", result.raw_sha256),
        ("Raw Artifact SHA256", result.raw_artifact_sha256),
        ("Extract SHA256", result.extract_sha256),
    ]:
        assert f"- **{field}**: {value}" in block


def test_location_resolves_on_disk(local_site, knowledge_tree):
    """R-B2 / MR-4: the entry names a path a later reader can open."""
    result = _register(local_site, knowledge_tree)
    block = _block_for(knowledge_tree, METADATA.title)
    assert f"- **Location**: {result.location}" in block
    assert result.location == f"knowledge/sources/{result.slug}/"
    assert (result.path / "output.md").is_file()


def test_staging_is_empty_after_a_successful_registration(local_site, knowledge_tree):
    _register(local_site, knowledge_tree)
    assert not list(knowledge_tree.paths.staging.iterdir())


def test_registration_writes_exactly_one_block_and_one_row(local_site, knowledge_tree):
    _register(local_site, knowledge_tree)
    assert knowledge_tree.index.read_text().count(f"### {METADATA.title}") == 1
    assert len(knowledge_tree.manifest.read_text().strip().splitlines()) == 1


@pytest.mark.parametrize("field", ["title", "use_for", "validation", "caveat"])
def test_missing_caller_metadata_is_a_precondition_failure(local_site, knowledge_tree, field):
    """D10: a missing title is refused, never guessed from the URL or the page."""
    from dataclasses import replace

    result = _register(local_site, knowledge_tree,
                       metadata=replace(METADATA, **{field: "  "}))
    assert result.outcome == "precondition_failed"
    assert field in result.reason
    assert not list(knowledge_tree.paths.sources.iterdir())
    assert knowledge_tree.manifest.read_text() == ""


def test_slug_collision_gets_a_numeric_suffix(local_site, knowledge_tree):
    (knowledge_tree.paths.sources / "widget_coil_note").mkdir()
    result = _register(local_site, knowledge_tree)
    assert result.slug == "widget_coil_note_2"


def test_unreachable_url_is_a_capture_failure_leaving_nothing(knowledge_tree):
    result = source_registry.register(
        UrlSource(url="http://127.0.0.1:1/nothing.html"), METADATA, paths=knowledge_tree.paths
    )
    assert result.outcome == "capture_failed"
    assert not list(knowledge_tree.paths.sources.iterdir())
    assert not list(knowledge_tree.paths.staging.iterdir())
    assert knowledge_tree.manifest.read_text() == ""


def test_manifest_and_index_carry_the_same_raw_artifact_hash(local_site, knowledge_tree):
    """F7: one value, one derivation, handed to both writers."""
    result = _register(local_site, knowledge_tree, page="latin1.html",
                       metadata=METADATA)
    row = _only_row(knowledge_tree)
    block = _block_for(knowledge_tree, METADATA.title)
    assert f"- **Raw Artifact SHA256**: {row['raw_artifact_sha256']}" in block
    assert result.raw_artifact_sha256 == row["raw_artifact_sha256"]
