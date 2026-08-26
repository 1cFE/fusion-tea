"""Phase 5 — `register --run` writes a receipt per attempt and honours max_captures (D8)."""

import json

import pytest
import source_registry
from source_registry import SourceMetadata, UrlSource

METADATA = SourceMetadata(
    title="Widget Coil Note",
    use_for="Synthetic winding-pack geometry; exercises receipts.",
    validation="Compare against the fixture page itself.",
    caveat="A test fixture.",
)


@pytest.fixture
def run_dir(tmp_path):
    def _make(max_captures: int = 2):
        directory = tmp_path / "run"
        (directory / "receipts").mkdir(parents=True)
        (directory / "run.json").write_text(json.dumps({
            "request_id": "REQ-001",
            "request_key": "k" * 64,
            "limits": {"max_searches": 3, "max_captures": max_captures},
        }))
        return directory

    return _make


def _receipts(directory) -> list[dict]:
    return [json.loads(p.read_text())
            for p in sorted((directory / "receipts").iterdir())]


def _register(tree, run, url, title=None):
    from dataclasses import replace

    metadata = METADATA if title is None else replace(METADATA, title=title)
    return source_registry.register(
        UrlSource(url=url), metadata, paths=tree.paths, run_dir=run
    )


def test_a_receipt_is_written_for_a_successful_registration(local_site, knowledge_tree, run_dir):
    run = run_dir()
    result = _register(knowledge_tree, run, local_site.url("utf8.html"))

    (receipt,) = _receipts(run)
    assert receipt["outcome"] == "registered" == result.outcome
    assert receipt["attempt"] == 1
    assert receipt["candidate"] == local_site.url("utf8.html")
    assert receipt["slug"] == result.slug
    assert receipt["path"] == result.location
    assert receipt["source_id"] == result.source_id
    assert receipt["triage"] == "keeper"
    assert receipt["captured"] is True
    assert receipt["at"].endswith("+00:00")


def test_a_receipt_is_written_for_a_refusal_too(knowledge_tree, run_dir):
    run = run_dir()
    result = _register(knowledge_tree, run, "http://127.0.0.1:1/nothing.html")

    (receipt,) = _receipts(run)
    assert receipt["outcome"] == "capture_failed" == result.outcome
    assert receipt["reason"]
    assert receipt["slug"] is None


def test_a_pre_capture_refusal_does_not_spend_a_capture(knowledge_tree, run_dir):
    run = run_dir()
    _register(knowledge_tree, run, "https://example.org/mirror/08-FST-Lyon.pdf")

    (receipt,) = _receipts(run)
    assert receipt["outcome"] == "holdout_hit"
    assert receipt["captured"] is False
    assert receipt["rule_id"]


def test_the_capture_after_the_limit_is_refused_and_named(local_site, knowledge_tree, run_dir):
    run = run_dir(max_captures=1)
    first = _register(knowledge_tree, run, local_site.url("utf8.html"))
    second = _register(knowledge_tree, run, local_site.url("latin1.html"), title="Cable Note")

    assert first.outcome == "registered"
    assert second.outcome == "limit_reached"
    assert "max_captures" in second.reason
    assert len(knowledge_tree.manifest.read_text().strip().splitlines()) == 1
    assert [r["outcome"] for r in _receipts(run)] == ["registered", "limit_reached"]


def test_a_run_dir_is_optional_so_the_standalone_operation_is_unaffected(
    local_site, knowledge_tree
):
    """R-B0 / SC2: a direct call registers with no run directory in sight."""
    result = source_registry.register(
        UrlSource(url=local_site.url("utf8.html")), METADATA, paths=knowledge_tree.paths
    )
    assert result.outcome == "registered"
