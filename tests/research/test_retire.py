"""`retire` — the one removal door (T-010 brief, R1–R5).

Removes exactly one entry's four artifacts together, or nothing; leaves one durable
RETIRED.jsonl line; and `verify` then treats the slug as expected-absent and reports
it if it reappears. Sources are registered through the real capture chain against the
loopback fixture, so what is retired is what `register` actually wrote.
"""

import hashlib
import json
from dataclasses import replace
from datetime import datetime, timezone

import pytest
import source_registry
from source_registry import RetirementError, SourceMetadata, UrlSource

METADATA = SourceMetadata(
    title="Widget Coil Note",
    use_for="Synthetic winding-pack geometry; exercises retirement.",
    validation="Compare against the fixture page itself.",
    caveat="A test fixture.",
)
REASON = "Captured content is a fixture, not a paper (test)."

RUNGS = {
    "after_park": "_write_manifest_without",
    "after_manifest": "_write_index_without",
    "after_index": "_append_retired_line",
}


def _snapshot(tree) -> tuple:
    return (
        tree.index.read_bytes(),
        tree.manifest.read_bytes(),
        sorted(p.name for p in tree.paths.sources.iterdir()),
        sorted(p.name for p in tree.paths.raw.iterdir()),
        tree.paths.retired.read_bytes() if tree.paths.retired.exists() else None,
    )


def _rows(tree) -> list[dict]:
    return [json.loads(l) for l in tree.manifest.read_text().splitlines() if l.strip()]


def _block_text(tree, slug: str) -> str:
    """The block as the writer wrote it: heading through last metadata line."""
    blocks = [b for b in source_registry._index_blocks(tree.index.read_text()) if b.slug == slug]
    assert len(blocks) == 1
    return blocks[0].text


def _register(local_site, tree, page, title):
    result = source_registry.register(
        UrlSource(url=local_site.url(page)), replace(METADATA, title=title), paths=tree.paths
    )
    assert result.outcome == "registered", result.reason
    return result


@pytest.fixture
def two_sources(local_site, knowledge_tree):
    """Two registered entries and the registry snapshot taken between them."""
    kept = _register(local_site, knowledge_tree, "utf8.html", "Widget Coil Note")
    after_first = _snapshot(knowledge_tree)
    gone = _register(local_site, knowledge_tree, "latin1.html", "Cable Note")
    return kept, gone, after_first


# --- R1 / R2: happy path ------------------------------------------------------


def test_retire_removes_all_four_artifacts_and_records_one_line(knowledge_tree, two_sources):
    kept, gone, after_first = two_sources
    block = _block_text(knowledge_tree, gone.slug)
    row = next(r for r in _rows(knowledge_tree) if r["slug"] == gone.slug)
    before = datetime.now(timezone.utc)

    result = source_registry.retire(gone.slug, REASON, paths=knowledge_tree.paths)

    assert result.outcome == "retired" and result.slug == gone.slug
    assert not gone.path.exists()
    assert gone.slug not in {r["slug"] for r in _rows(knowledge_tree)}
    assert f"knowledge/sources/{gone.slug}/" not in knowledge_tree.index.read_text()
    assert not list(knowledge_tree.paths.staging.iterdir())
    # The registry is byte-identical to its state before the retired entry was registered.
    assert _snapshot(knowledge_tree)[:4] == after_first[:4]
    assert (kept.path / "output.md").is_file()

    lines = [json.loads(l) for l in knowledge_tree.paths.retired.read_text().splitlines()]
    assert len(lines) == 1 and lines[0] == result.retired_line
    line = lines[0]
    assert line["slug"] == gone.slug and line["row"] == row and line["reason"] == REASON
    assert line["index_block_sha256"] == hashlib.sha256(block.encode("utf-8")).hexdigest()
    retired_at = datetime.fromisoformat(line["retired_at"])
    assert retired_at.tzinfo is not None and before <= retired_at <= datetime.now(timezone.utc)

    assert result.removed["manifest_row"] == row
    assert result.removed["index_block"] == block
    assert result.removed["source_dir"] == f"knowledge/sources/{gone.slug}/"
    assert result.removed["raw_copy"] is None  # a URL source stores raw.html inside its directory

    report = source_registry.verify(knowledge_tree.paths)
    assert report.findings == [] and not report.has_faults


# --- R3: refusals write nothing ----------------------------------------------


def test_unknown_slug_refuses_and_writes_nothing(knowledge_tree, two_sources):
    before = _snapshot(knowledge_tree)
    result = source_registry.retire("no_such_source", REASON, paths=knowledge_tree.paths)
    assert result.outcome == "unknown_slug"
    assert "no_such_source" in result.reason
    assert _snapshot(knowledge_tree) == before
    assert not knowledge_tree.paths.retired.exists()


@pytest.mark.parametrize("slug, rule_prefix", [
    ("aries_cost_account_documentation", "path:knowledge/sources/"),  # a barred registry path
    ("knowledge/holdout/aries-cs/paper.pdf", "path:knowledge/holdout/"),  # a holdout path as slug
    ("aries-cs_notes", "term:"),  # a barred term in the slug
])
def test_holdout_slug_refuses_before_anything_else(knowledge_tree, two_sources, slug, rule_prefix):
    before = _snapshot(knowledge_tree)
    result = source_registry.retire(slug, REASON, paths=knowledge_tree.paths)
    assert result.outcome == "holdout_hit"
    assert result.rule_id.startswith(rule_prefix)
    assert _snapshot(knowledge_tree) == before
    assert not knowledge_tree.paths.retired.exists()


@pytest.mark.parametrize("slug, reason, outcome", [
    ("cable_note", "   ", "precondition_failed"),
    ("../sources/cable_note", REASON, "precondition_failed"),
    ("knowledge/sources/cable_note", REASON, "precondition_failed"),
])
def test_blank_reason_or_malformed_slug_refuses(knowledge_tree, two_sources, slug, reason, outcome):
    before = _snapshot(knowledge_tree)
    result = source_registry.retire(slug, reason, paths=knowledge_tree.paths)
    assert result.outcome == outcome
    assert _snapshot(knowledge_tree) == before


def test_a_reference_from_another_entry_refuses_but_a_supersession_claim_does_not(
    knowledge_tree, two_sources
):
    kept, gone, _ = two_sources
    index = knowledge_tree.index.read_text()
    caveat = "- **Caveat**: A test fixture."
    kept_block = _block_text(knowledge_tree, kept.slug)
    assert caveat in kept_block

    dependent = kept_block.replace(caveat, f"{caveat} Read with knowledge/sources/{gone.slug}/.")
    knowledge_tree.index.write_text(index.replace(kept_block, dependent))
    before = _snapshot(knowledge_tree)
    result = source_registry.retire(gone.slug, REASON, paths=knowledge_tree.paths)
    assert result.outcome == "referenced"
    assert result.references == (f"SOURCE_INDEX.md block ({kept.slug})",)
    assert _snapshot(knowledge_tree) == before

    superseding = kept_block.replace(
        caveat, f"{caveat} Supersedes the defective registration knowledge/sources/{gone.slug}/."
    )
    knowledge_tree.index.write_text(index.replace(kept_block, superseding))
    result = source_registry.retire(gone.slug, REASON, paths=knowledge_tree.paths)
    assert result.outcome == "retired"
    assert f"knowledge/sources/{gone.slug}/" in _block_text(knowledge_tree, kept.slug)
    assert source_registry.verify(knowledge_tree.paths).findings == []


def test_a_manifest_field_referencing_the_slug_refuses(knowledge_tree, two_sources):
    kept, gone, _ = two_sources
    rows = _rows(knowledge_tree)
    for row in rows:
        if row["slug"] == kept.slug:
            row["caveat"] = f"companion to {gone.slug}"
    knowledge_tree.manifest.write_text("".join(json.dumps(r) + "\n" for r in rows))
    before = _snapshot(knowledge_tree)
    result = source_registry.retire(gone.slug, REASON, paths=knowledge_tree.paths)
    assert result.outcome == "referenced"
    assert result.references == (f"manifest row field caveat ({kept.slug})",)
    assert _snapshot(knowledge_tree) == before


# --- R1: atomic in the design's sense — the ladder puts everything back --------


@pytest.mark.parametrize("rung", sorted(RUNGS))
def test_failure_at_each_rung_leaves_everything(rung, knowledge_tree, two_sources, monkeypatch):
    kept, gone, _ = two_sources
    before = _snapshot(knowledge_tree)

    def boom(*args, **kwargs):
        raise OSError(f"injected failure at {rung}")

    monkeypatch.setattr(source_registry, RUNGS[rung], boom)
    with pytest.raises(RetirementError, match=rung):
        source_registry.retire(gone.slug, REASON, paths=knowledge_tree.paths)

    assert _snapshot(knowledge_tree) == before
    assert (gone.path / "output.md").is_file() and (kept.path / "output.md").is_file()
    assert not list(knowledge_tree.paths.staging.iterdir())
    assert source_registry.verify(knowledge_tree.paths).findings == []


# --- R2: verify treats retired slugs as expected-absent, and reports reappearance


def test_verify_reports_each_way_a_retired_slug_can_reappear(knowledge_tree, two_sources):
    kept, gone, _ = two_sources
    block = _block_text(knowledge_tree, gone.slug)
    row = next(r for r in _rows(knowledge_tree) if r["slug"] == gone.slug)
    assert source_registry.retire(gone.slug, REASON, paths=knowledge_tree.paths).outcome == "retired"
    assert source_registry.verify(knowledge_tree.paths).findings == []

    with open(knowledge_tree.manifest, "a") as handle:
        handle.write(json.dumps(row) + "\n")
    report = source_registry.verify(knowledge_tree.paths)
    assert [(f.kind, f.klass, f.path) for f in report.findings] == [
        ("retired_reappeared", "fault", f"knowledge/sources/{gone.slug}"),
    ]
    assert "manifest row" in report.findings[0].detail and report.has_faults

    (knowledge_tree.paths.sources / gone.slug).mkdir()
    index = knowledge_tree.index.read_text()
    knowledge_tree.index.write_text(
        index.replace("\n## How Sources Are Used", f"\n{block}\n\n## How Sources Are Used", 1)
    )
    report = source_registry.verify(knowledge_tree.paths)
    assert {f.kind for f in report.findings} == {"retired_reappeared"}
    assert sorted(f.detail.split(" for ")[0] for f in report.findings) == [
        "SOURCE_INDEX.md block", "manifest row", "source directory",
    ]
    assert report.has_faults


def test_verify_still_reports_ordinary_drift_beside_retirements(knowledge_tree, two_sources):
    kept, gone, _ = two_sources
    assert source_registry.retire(gone.slug, REASON, paths=knowledge_tree.paths).outcome == "retired"
    (knowledge_tree.paths.sources / "orphan_source").mkdir()
    report = source_registry.verify(knowledge_tree.paths)
    assert [f.kind for f in report.findings] == ["orphan_source_dir"]


# --- R4: the CLI prints what it removed and the line ---------------------------


def test_cli_prints_the_removal_and_the_retired_line(knowledge_tree, two_sources, capsys):
    kept, gone, _ = two_sources
    row = next(r for r in _rows(knowledge_tree) if r["slug"] == gone.slug)
    code = source_registry.main(["retire", "--slug", gone.slug, "--reason", REASON])
    out = capsys.readouterr().out
    assert code == 0
    assert out.startswith(f"retired {gone.slug}\n")
    assert json.dumps(row) in out
    assert f"knowledge/sources/{gone.slug}/" in out and "### Cable Note" in out
    printed_line = json.loads(out.split("RETIRED.jsonl line:\n", 1)[1].strip())
    assert printed_line == json.loads(knowledge_tree.paths.retired.read_text())


def test_cli_refusal_exits_nonzero_with_the_reason(knowledge_tree, two_sources, capsys):
    code = source_registry.main(["retire", "--slug", "no_such_source", "--reason", REASON])
    payload = json.loads(capsys.readouterr().out)
    assert code == 1 and payload["outcome"] == "unknown_slug"
    assert not knowledge_tree.paths.retired.exists()
