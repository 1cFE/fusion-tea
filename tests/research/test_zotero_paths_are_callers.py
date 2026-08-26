"""Phase 6 — the Zotero and local-PDF paths go through the one write door.

`process_zotero_item` is driven against a stub Zotero client, so the path that
had no test at all now has one, with no network involved.
"""

import json
from pathlib import Path
from types import SimpleNamespace

import pytest
import zotero_ingest

ITEM_KEY = "ABCD1234"


class StubZotero:
    """Just enough of pyzotero for `resolve_pdf_info` and `download_pdf_from_info`."""

    def __init__(self, pdf: Path, title: str):
        self._pdf = pdf
        self._title = title

    def item(self, key):
        return {"key": key, "data": {"itemType": "journalArticle", "title": self._title}}

    def children(self, key):
        return [{"key": f"{key}-PDF",
                 "data": {"contentType": "application/pdf", "filename": self._pdf.name}}]

    def dump(self, child_key, filename, directory):
        Path(directory).mkdir(parents=True, exist_ok=True)
        (Path(directory) / filename).write_bytes(self._pdf.read_bytes())


@pytest.fixture
def batch_args(knowledge_tree):
    return SimpleNamespace(budget=0.0, model="opus", output_dir=knowledge_tree.raw)


@pytest.mark.slow
def test_zotero_item_registers_through_the_door(knowledge_tree, generated_pdf, batch_args):
    zot = StubZotero(generated_pdf, "Widget Coil Note From Zotero")
    item = zot.item(ITEM_KEY)

    assert zotero_ingest.process_zotero_item(zot, item, batch_args) == "extracted"

    row = json.loads(knowledge_tree.manifest.read_text().strip())
    assert row["zotero_key"] == ITEM_KEY
    assert row["source_kind"] == "zotero"
    assert row["source_id"] == row["raw_sha256"]      # R-B3: durable identity, not just a key
    assert row["extract_sha256"]

    block = knowledge_tree.index.read_text().split("### Widget Coil Note From Zotero", 1)[1]
    assert f"- **Zotero Key**: {zotero_ingest.GROUP_ID}:{ITEM_KEY}" in block
    assert "- **Use for**:\n" in block                # batch profile keeps today's empty fields


@pytest.mark.slow
def test_a_second_pass_over_the_same_item_is_a_duplicate(knowledge_tree, generated_pdf, batch_args):
    zot = StubZotero(generated_pdf, "Widget Coil Note From Zotero")
    item = zot.item(ITEM_KEY)

    assert zotero_ingest.process_zotero_item(zot, item, batch_args) == "extracted"
    assert zotero_ingest.process_zotero_item(zot, item, batch_args) == "skipped"
    assert len(knowledge_tree.manifest.read_text().strip().splitlines()) == 1


def test_item_without_a_pdf_is_skipped(knowledge_tree, batch_args):
    class NoPdf(StubZotero):
        def children(self, key):
            return []

    zot = NoPdf(knowledge_tree.raw, "No Attachment")
    item = {"key": ITEM_KEY, "data": {"itemType": "journalArticle", "title": "No Attachment"}}
    assert zotero_ingest.process_zotero_item(zot, item, batch_args) == "skipped"
    assert knowledge_tree.manifest.read_text() == ""


def test_local_pdf_without_metadata_flags_names_all_three(knowledge_tree, generated_pdf, capsys):
    """D6: `--local-pdf` moved to the seam profile, a deliberate breaking change."""
    args = SimpleNamespace(local_pdf=generated_pdf, budget=0.0, model="opus",
                           use_for=None, validation=None, caveat=None, title=None)
    with pytest.raises(SystemExit):
        zotero_ingest.process_local_pdf(args)
    message = capsys.readouterr().out
    for flag in ("--use-for", "--validation", "--caveat"):
        assert flag in message


@pytest.mark.slow
def test_local_pdf_with_metadata_gets_a_manifest_row(knowledge_tree, generated_pdf, capsys):
    """R-B1a: the local-PDF path wrote no manifest row at all before this item."""
    args = SimpleNamespace(local_pdf=generated_pdf, budget=0.0, model="opus",
                           use_for="Synthetic geometry.", validation="Compare to the fixture.",
                           caveat="A test fixture.", title=None)
    zotero_ingest.process_local_pdf(args)

    row = json.loads(knowledge_tree.manifest.read_text().strip())
    assert row["source_kind"] == "local_pdf"
    assert row["origin_path"] == str(generated_pdf)
    assert (knowledge_tree.paths.sources / row["slug"] / "output.md").is_file()
