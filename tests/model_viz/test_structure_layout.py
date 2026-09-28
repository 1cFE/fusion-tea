"""The layout gate (design § Validation Approach).

At 1400 x 900 the structure view's part boxes, labels included, never overlap unless nested, and
the fit zoom keeps 12 px labels at 9 px or more."""

from itertools import combinations

import pytest
from edge_oracle import load_fixture
from structure_oracle import ancestors
from viewer_harness import load_snapshot, open_viewer, switch_view

GATE_VIEWPORT = {"width": 1400, "height": 900}
LABEL_PX = 12
MIN_RENDERED_LABEL_PX = 9


def intersects(a: dict, b: dict) -> bool:
    """Two bounding boxes share interior area; touching along an edge is not an intersection."""
    return a["x1"] < b["x2"] and b["x1"] < a["x2"] and a["y1"] < b["y2"] and b["y1"] < a["y2"]


def pairs_not_nested(boxes: list[dict], above: dict[str, set[str]]):
    """Every pair of drawn parts where neither is an ancestor of the other."""
    for a, b in combinations(boxes, 2):
        if a["occ"] not in above[b["occ"]] and b["occ"] not in above[a["occ"]]:
            yield a, b


def test_intersects_edges_only_touching():
    box = {"x1": 0, "y1": 0, "x2": 10, "y2": 10}
    assert not intersects(box, {"x1": 10, "y1": 0, "x2": 20, "y2": 10})
    assert not intersects(box, {"x1": 0, "y1": 10, "x2": 10, "y2": 20})
    assert intersects(box, {"x1": 9, "y1": 9, "x2": 20, "y2": 20})


@pytest.mark.parametrize("state", ["start", "all_open"])
def test_layout_gate(browser, fixture_path, state):
    page, problems = open_viewer(browser, viewport=GATE_VIEWPORT)
    assert load_snapshot(page, fixture_path) == "ready"
    switch_view(page, "structure")
    if state == "all_open":
        page.click("[data-action=expand-all]")
    boxes = page.evaluate(
        """() => window.modelVizApp.cy.nodes('[kind="part"]').map(n =>
             ({occ: n.data('occurrence_id'), label: n.data('label'), bb: n.boundingBox()}))"""
    )  # boundingBox() includes labels by default
    assert len(boxes) == (19 if state == "start" else 23)
    flat = [{"occ": b["occ"], "label": b["label"], **b["bb"]} for b in boxes]
    overlaps = [
        (a["label"], b["label"])
        for a, b in pairs_not_nested(flat, ancestors(load_fixture()))
        if intersects(a, b)
    ]
    assert overlaps == []
    zoom = page.evaluate("() => window.modelVizApp.cy.zoom()")
    assert zoom * LABEL_PX >= MIN_RENDERED_LABEL_PX, f"fit zoom {zoom:.3f}"
    page.close()
    problems.assert_clean()
