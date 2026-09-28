"""Export criteria for v2: the viewer flag, and several snapshots inside one standalone file.

The default output (no flag, and `--viewer v1`) must stay byte-identical, so the six v1 export
tests in `tests/model_viz/test_export.py` keep describing the same file (plan PD6).
"""

import json
import subprocess
import sys

import pytest
import viewer2_snapshots as vs2
from viewer2_harness import REPO, VIEWPORT, PageProblemsV2, drawn_calcs, drawn_labels

EXPORTER = REPO / "src/model_viz/export.py"
CALC_COUNT = 77
SIZE_LIMIT_BYTES = 3_000_000
SELECT = "[data-role=snapshot-select]"


def run_exporter(output, snapshots, *flags) -> subprocess.CompletedProcess:
    return subprocess.run(
        [
            sys.executable,
            str(EXPORTER),
            *[str(path) for path in snapshots],
            "-o",
            str(output),
            *flags,
        ],
        capture_output=True,
        text=True,
        check=False,
    )


def export(output, snapshots, *flags):
    result = run_exporter(output, snapshots, *flags)
    assert result.returncode == 0, result.stderr
    return output


def open_export(browser, path):
    """The exported file opened from file://, policed like every other v2 page (PD11)."""
    page = browser.new_page(viewport=VIEWPORT)
    page.set_default_timeout(15000)
    problems = PageProblemsV2(page)
    page.goto(path.as_uri(), wait_until="load")
    page.wait_for_function("() => window.modelVizApp !== undefined", timeout=5000)
    return page, problems


def choose(page, index: int) -> None:
    """Pick an embedded snapshot from the Model select and wait for it to load."""
    seq = int(page.get_attribute("body", "data-load-seq"))
    page.select_option(SELECT, str(index))
    page.wait_for_function("s => Number(document.body.dataset.loadSeq) > s", arg=seq)


def option_labels(page) -> list[str]:
    return page.evaluate(
        f"() => Array.from(document.querySelectorAll('{SELECT} option'), o => o.textContent)"
    )


def v1_calc_labels(page) -> list[str]:
    """v1 draws calcs only once the source-file groups are open."""
    page.click("[data-action=expand-all]")
    return page.evaluate("() => window.modelVizApp.cy.nodes().map(n => n.data('label'))")


@pytest.fixture(scope="module")
def renamed_snapshot(tmp_path_factory, fixture_path):
    """A second, distinguishable snapshot file whose model name is `renamed`."""
    snap = vs2.renamed(json.loads(fixture_path.read_text(encoding="utf-8")))
    return vs2.write(tmp_path_factory.mktemp("snapshots"), "renamed.snapshot.json", snap)


@pytest.fixture(scope="module")
def exported_v2(tmp_path_factory, fixture_path):
    return export(
        tmp_path_factory.mktemp("export_v2") / "v2.html", [fixture_path], "--viewer", "v2"
    )


@pytest.fixture(scope="module")
def exported_pair_v2(tmp_path_factory, fixture_path, renamed_snapshot):
    output = tmp_path_factory.mktemp("export_pair_v2") / "pair_v2.html"
    return export(output, [fixture_path, renamed_snapshot], "--viewer", "v2")


@pytest.fixture(scope="module")
def exported_pair_v1(tmp_path_factory, fixture_path, renamed_snapshot):
    output = tmp_path_factory.mktemp("export_pair_v1") / "pair_v1.html"
    return export(output, [fixture_path, renamed_snapshot])


def test_default_export_is_the_v1_export(tmp_path, fixture_path):
    """PD6: the no-flag output and `--viewer v1` are the same bytes."""
    plain, v1 = tmp_path / "plain.html", tmp_path / "v1.html"
    export(plain, [fixture_path])
    export(v1, [fixture_path], "--viewer", "v1")
    assert plain.read_bytes() == v1.read_bytes()


def test_v2_export_references_nothing_outside_itself(exported_v2):
    text = exported_v2.read_text(encoding="utf-8")
    assert "<script src=" not in text
    assert '<link rel="stylesheet"' not in text
    assert "<link" not in text
    assert text.count('<script type="application/json" id="model-viz-snapshot">') == 1
    assert exported_v2.stat().st_size < SIZE_LIMIT_BYTES


def test_v2_export_opens_loaded(browser, exported_v2):
    page, problems = open_export(browser, exported_v2)
    try:
        assert page.get_attribute("body", "data-load-state") == "ready"
        assert page.get_attribute("body", "data-load-seq") == "1"
        assert page.is_hidden("[data-role=error-banner]")
        # The picture opens with the subsystems closed (owner ruling 2026-09-15).
        page.click("[data-action=expand-all]")
        assert len(drawn_calcs(page)) == CALC_COUNT
        assert page.title() == "stellarator"
        assert "stellarator.snapshot.json" in page.text_content(".toolbar [data-role=export-note]")
        assert page.query_selector(SELECT) is None
    finally:
        page.close()
    problems.assert_clean()


def test_v2_export_switches_between_two_snapshots(browser, exported_pair_v2):
    text = exported_pair_v2.read_text(encoding="utf-8")
    assert text.count('<script type="application/json" id="model-viz-snapshot-0">') == 1
    assert text.count('<script type="application/json" id="model-viz-snapshot-1">') == 1

    page, problems = open_export(browser, exported_pair_v2)
    try:
        assert page.get_attribute("body", "data-load-state") == "ready"
        assert page.get_attribute("body", "data-load-seq") == "1"
        assert page.title() == "stellarator"
        assert option_labels(page) == ["stellarator", "renamed"]
        page.click("[data-action=expand-all]")
        calcs = drawn_calcs(page)
        assert len(calcs) == CALC_COUNT
        labels = drawn_labels(page)
        assert not any(labels[ident].startswith(vs2.RENAME_PREFIX) for ident in calcs)

        choose(page, 1)
        assert page.get_attribute("body", "data-load-state") == "ready"
        assert page.get_attribute("body", "data-load-seq") == "2"
        assert page.title() == "renamed"
        assert "renamed.snapshot.json" in page.text_content(".toolbar [data-role=export-note]")
        page.click("[data-action=expand-all]")
        calcs = drawn_calcs(page)
        labels = drawn_labels(page)
        assert len(calcs) == CALC_COUNT
        assert all(labels[ident].startswith(vs2.RENAME_PREFIX) for ident in calcs)
    finally:
        page.close()
    problems.assert_clean()


def test_v1_export_switches_between_two_snapshots(browser, exported_pair_v1):
    page, problems = open_export(browser, exported_pair_v1)
    try:
        assert page.get_attribute("body", "data-load-state") == "ready"
        assert page.title() == "stellarator"
        assert option_labels(page) == ["stellarator", "renamed"]
        before = v1_calc_labels(page)
        assert sum(label.startswith(vs2.RENAME_PREFIX) for label in before) == 0

        choose(page, 1)
        assert page.get_attribute("body", "data-load-seq") == "2"
        assert page.title() == "renamed"
        after = v1_calc_labels(page)
        assert sum(label.startswith(vs2.RENAME_PREFIX) for label in after) == CALC_COUNT
    finally:
        page.close()
    problems.assert_clean()


def test_export_refuses_an_unknown_viewer(tmp_path, fixture_path):
    output = tmp_path / "out.html"
    result = run_exporter(output, [fixture_path], "--viewer", "v3")
    assert result.returncode != 0
    assert not output.exists()


def test_export_refuses_the_whole_set_before_writing(tmp_path, fixture_path):
    """One unreadable snapshot in the set means no file at all."""
    bad = vs2.write_bytes(tmp_path, "picked_by_mistake.pdf", vs2.non_json_bytes())
    output = tmp_path / "out.html"
    result = run_exporter(output, [fixture_path, bad])
    assert result.returncode == 1
    assert str(bad) in result.stderr and "not a JSON file" in result.stderr
    assert not output.exists()
