"""Phase 4 — the local-PDF half of the chain (spec R-E2, SC1).

Marked slow: the PDF pipeline loads table-detection weights on every run.
"""

import hashlib
import json
import re

import pytest
import source_registry
from source_registry import LocalPdfSource, SourceMetadata

FRONTMATTER_HASH = re.compile(r'^content_hash_sha256: "([0-9a-f]{64})"', re.MULTILINE)

METADATA = SourceMetadata(
    title="Widget Coil Note PDF",
    use_for="Synthetic PDF; exercises the local-PDF capture chain.",
    validation="Compare against the generated fixture PDF itself.",
    caveat="A test fixture. It states nothing about any real machine.",
)


@pytest.fixture
def registered_pdf(knowledge_tree, generated_pdf):
    return source_registry.register(
        LocalPdfSource(path=generated_pdf), METADATA, paths=knowledge_tree.paths
    )


@pytest.mark.slow
def test_local_pdf_registers_flattened_with_full_provenance(
    knowledge_tree, generated_pdf, registered_pdf
):
    result = registered_pdf
    assert result.outcome == "registered", result.reason

    row = json.loads(knowledge_tree.manifest.read_text().strip())
    frontmatter_hash = FRONTMATTER_HASH.search((result.path / "output.md").read_text()).group(1)
    input_hash = hashlib.sha256(generated_pdf.read_bytes()).hexdigest()

    assert row["source_kind"] == "local_pdf"
    assert row["source_id"] == row["raw_sha256"] == frontmatter_hash == input_hash
    assert "source_url" not in row and "zotero_key" not in row

    # Flattened: output.md sits at the top of the source dir, not under a stem dir.
    assert (result.path / "output.md").is_file()
    assert not (result.path / generated_pdf.stem).exists()


@pytest.mark.slow
def test_raw_copy_lands_in_knowledge_raw_only_after_commit(
    knowledge_tree, generated_pdf, registered_pdf
):
    """`--save-source` writes no raw.pdf on this path, so the seam stages a copy itself."""
    result = registered_pdf
    raw_copy = knowledge_tree.raw / generated_pdf.name
    assert raw_copy.is_file()
    assert raw_copy.read_bytes() == generated_pdf.read_bytes()

    row = json.loads(knowledge_tree.manifest.read_text().strip())
    assert row["raw_artifact_sha256"] == hashlib.sha256(raw_copy.read_bytes()).hexdigest()
    assert row["origin_path"] == str(generated_pdf)
    assert not (result.path / generated_pdf.name).exists()   # moved out of the source dir


@pytest.mark.slow
def test_pdf_index_block_uses_origin_path_not_source_url(
    knowledge_tree, generated_pdf, registered_pdf
):
    block = knowledge_tree.index.read_text().split(f"### {METADATA.title}", 1)[1]
    assert f"- **Origin Path**: {generated_pdf}" in block
    assert "- **Source URL**" not in block


def test_missing_local_pdf_is_a_precondition_failure(knowledge_tree, tmp_path):
    result = source_registry.register(
        LocalPdfSource(path=tmp_path / "absent.pdf"), METADATA, paths=knowledge_tree.paths
    )
    assert result.outcome == "precondition_failed" and "absent.pdf" in result.reason
    assert not list(knowledge_tree.paths.sources.iterdir())
