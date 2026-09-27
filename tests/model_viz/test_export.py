"""Export criteria: one self-contained HTML per snapshot that opens loaded from file://."""

import datetime
import json
import re
import subprocess
import sys

import pytest
import viewer_snapshots as vs
from viewer_harness import REPO, PageProblems, load_snapshot, open_viewer, switch_view

EXPORTER = REPO / "src/model_viz/export.py"
SIZE_LIMIT_BYTES = 3_000_000


def run_exporter(snapshot, output) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(EXPORTER), str(snapshot), "-o", str(output)],
        capture_output=True,
        text=True,
        check=False,
    )


def drawn_node_counts(page) -> tuple[int, int]:
    """Nodes drawn in the calc view as loaded, then in the structure view after a real switch."""
    calcs = page.evaluate("() => window.modelVizApp.cy.nodes().length")
    switch_view(page, "structure")
    structure = page.evaluate("() => window.modelVizApp.cy.nodes().length")
    return calcs, structure


@pytest.fixture(scope="module")
def exported(tmp_path_factory, fixture_path):
    output = tmp_path_factory.mktemp("export") / "stellarator.html"
    result = run_exporter(fixture_path, output)
    assert result.returncode == 0, result.stderr
    return output


@pytest.fixture
def exported_page(browser, exported):
    page = browser.new_page(viewport={"width": 1600, "height": 1000})
    problems = PageProblems(page)
    page.goto(exported.as_uri(), wait_until="load")
    yield page
    page.close()
    problems.assert_clean()


def test_export_references_nothing_outside_itself(exported):
    text = exported.read_text(encoding="utf-8")
    assert re.findall(r'\b(?:src|href)="[^"]*"', text) == []
    assert "<link" not in text
    assert text.count('<script type="application/json" id="model-viz-snapshot">') == 1
    assert exported.stat().st_size < SIZE_LIMIT_BYTES


def test_export_opens_loaded_like_the_live_page(browser, fixture_path, exported_page):
    live, problems = open_viewer(browser)
    assert load_snapshot(live, fixture_path) == "ready"
    live_counts = drawn_node_counts(live)
    live.close()
    problems.assert_clean()

    assert exported_page.get_attribute("body", "data-load-state") == "ready"
    assert exported_page.get_attribute("body", "data-load-seq") == "1"
    assert exported_page.is_hidden("[data-role=error-banner]")
    assert drawn_node_counts(exported_page) == live_counts
    assert live_counts[0] > 0 and live_counts[1] > 0


def test_export_names_the_model(exported_page, fixture_path):
    fingerprint = json.loads(fixture_path.read_text())["instance_graph"]["fingerprint"]
    today = datetime.date.today().isoformat()
    assert exported_page.title() == "stellarator"
    assert exported_page.text_content(".toolbar [data-role=export-note]") == (
        f"exported from stellarator.snapshot.json on {today} · fingerprint {fingerprint[:12]}"
    )


def test_export_file_picker_still_loads(exported_page, fixture_path, tmp_path):
    renamed = vs.write(vs.renamed(json.loads(fixture_path.read_text())), tmp_path / "renamed.json")
    assert load_snapshot(exported_page, renamed) == "ready"
    assert exported_page.get_attribute("body", "data-load-seq") == "2"
    labels = exported_page.evaluate("() => window.modelVizApp.model.calcs.map(c => c.name)")
    assert labels and all(name.startswith("renamed_") for name in labels)


@pytest.mark.parametrize(
    ("name", "content", "reason"),
    [
        (
            "not_a_snapshot.json",
            json.dumps({"not": "a snapshot"}).encode(),
            "not a codegen snapshot",
        ),
        ("picked_by_mistake.pdf", vs.non_json_bytes(), "not a JSON file"),
    ],
)
def test_export_refuses_a_non_snapshot(tmp_path, name, content, reason):
    source = tmp_path / name
    source.write_bytes(content)
    output = tmp_path / "out.html"
    result = run_exporter(source, output)
    assert result.returncode == 1
    assert str(source) in result.stderr and reason in result.stderr
    assert not output.exists()
