"""F1 regression — one attempt's staging must survive another attempt running.

The sweep exists so unscanned captured bytes never persist across invocations
(design-F3). It must not achieve that by deleting a live attempt's working
directory: `register` is a standalone operator door, an agent-driven step and
the Zotero batch's writer, all against the same staging root.
"""

import os
import threading
import time
from dataclasses import replace
from pathlib import Path

import pytest
import source_registry
from source_registry import LocalPdfSource, SourceMetadata, UrlSource

METADATA = SourceMetadata(
    title="Widget Coil Note",
    use_for="Synthetic winding-pack geometry; exercises staging concurrency.",
    validation="Compare against the fixture page itself.",
    caveat="A test fixture.",
)


def _live_staging(tree, name: str = "inflight") -> Path:
    """A staging directory standing in for another attempt that is mid-capture."""
    directory = tree.paths.staging / name
    (directory / ".rawin").mkdir(parents=True)
    (directory / ".rawin" / "widget.pdf").write_bytes(b"%PDF-1.4 in flight\n")
    return directory


def _age(path: Path, seconds: int) -> None:
    past = time.time() - seconds
    os.utime(path, (past, past))


def _rows(tree) -> list[str]:
    return [line for line in tree.manifest.read_text().splitlines() if line.strip()]


def test_a_refusing_register_does_not_touch_a_live_staging_dir(knowledge_tree, tmp_path):
    """The auditor's reproduction: a no-op call used to delete everything."""
    inflight = _live_staging(knowledge_tree)

    for _ in range(5):
        result = source_registry.register(
            LocalPdfSource(path=tmp_path / "absent.pdf"), METADATA,
            paths=knowledge_tree.paths,
        )
        assert result.outcome == "precondition_failed"

    assert (inflight / ".rawin" / "widget.pdf").is_file()


def test_a_successful_register_does_not_touch_a_live_staging_dir(local_site, knowledge_tree):
    inflight = _live_staging(knowledge_tree)

    result = source_registry.register(
        UrlSource(url=local_site.url("utf8.html")), METADATA, paths=knowledge_tree.paths
    )
    assert result.outcome == "registered", result.reason
    assert (inflight / ".rawin" / "widget.pdf").is_file()


def test_a_demonstrably_stale_staging_dir_is_swept(local_site, knowledge_tree):
    """design-F3 still holds: leftovers from a killed run do not persist."""
    stale = _live_staging(knowledge_tree, name="stale")
    _age(stale, source_registry.STALE_STAGING_AGE_S + 60)

    result = source_registry.register(
        UrlSource(url=local_site.url("utf8.html")), METADATA, paths=knowledge_tree.paths
    )
    assert result.outcome == "registered", result.reason
    assert not stale.exists()


def test_a_stale_dir_is_swept_even_when_the_attempt_refuses(knowledge_tree, tmp_path):
    """Sweeping cannot depend on reaching commit, or leftovers would accumulate."""
    stale = _live_staging(knowledge_tree, name="stale")
    _age(stale, source_registry.STALE_STAGING_AGE_S + 60)

    result = source_registry.register(
        LocalPdfSource(path=tmp_path / "absent.pdf"), METADATA, paths=knowledge_tree.paths
    )
    assert result.outcome == "precondition_failed"
    assert not stale.exists()


def test_the_stale_threshold_cannot_reach_a_live_capture():
    """A live attempt is bounded by the capture timeout; the threshold is well past it."""
    assert source_registry.STALE_STAGING_AGE_S >= 4 * source_registry.CAPTURE_TIMEOUT_S


def test_concurrent_registers_do_not_interfere(local_site, knowledge_tree, tmp_path):
    """A real registration runs while a stream of refusing calls hammers the same root."""
    stop = threading.Event()
    noise_outcomes = []

    def noise():
        while not stop.is_set():
            noise_outcomes.append(source_registry.register(
                LocalPdfSource(path=tmp_path / "absent.pdf"), METADATA,
                paths=knowledge_tree.paths,
            ).outcome)

    hammer = threading.Thread(target=noise, daemon=True)
    hammer.start()
    try:
        result = source_registry.register(
            UrlSource(url=local_site.url("utf8.html")), METADATA, paths=knowledge_tree.paths
        )
    finally:
        stop.set()
        hammer.join(timeout=30)

    assert result.outcome == "registered", result.reason
    assert (result.path / "output.md").is_file()
    assert set(noise_outcomes) == {"precondition_failed"}
    assert len(_rows(knowledge_tree)) == 1


@pytest.mark.slow
def test_two_concurrent_registrations_both_land(local_site, knowledge_tree):
    """Two different sources captured at the same time both reach the registry."""
    results = {}

    def run(page: str, title: str) -> None:
        results[title] = source_registry.register(
            UrlSource(url=local_site.url(page)), replace(METADATA, title=title),
            paths=knowledge_tree.paths,
        )

    threads = [
        threading.Thread(target=run, args=("utf8.html", "Widget Coil Note")),
        threading.Thread(target=run, args=("latin1.html", "Cable Note")),
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(timeout=120)

    assert {r.outcome for r in results.values()} == {"registered"}
    assert len(_rows(knowledge_tree)) == 2
    body = knowledge_tree.index.read_text()
    assert body.count("### Widget Coil Note") == 1
    assert body.count("### Cable Note") == 1
