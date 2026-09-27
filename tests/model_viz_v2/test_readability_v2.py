"""Readability of the dagre picture (owner ruling 2026-09-15).

The picture is v1's calc graph laid out by dagre, left to right, so the gates are v1's: nothing
overlaps, no child leaves its open parent, and the edge-occlusion and crossing counts stay at the
level the spike measured. The spec's 9 px fitted-font gate (R-a) is superseded by the ruling — v1's
fitted picture reads at 2.58 px too, and the owner's answer to that was "you pan and zoom".
"""

import overlay_oracle as oracle
import pytest
from viewer2_harness import (
    crossings,
    drawn_parts,
    edges_behind_boxes,
    load_snapshot,
    overlaps_and_outside,
    toggle,
    viewport,
)

SNAP = oracle.load_fixture()
SIX = ["magnet", "blanket", "plasma", "fuel_cycle", "divertor", "heat_transport"]

# Measured on this fixture, all open, with the tripwire at the measurement plus 10 %. The spike
# measured v1's calc graph at 58 edges behind bodies and 338 crossings over the same 142 edges
# (.project/active/model-viz-v2/spike-elk-flow-findings.md), so v2's picture is a little cleaner
# than the one the owner picked.
EDGES_BEHIND_BOXES = 42
EDGES_BEHIND_BOXES_MAX = 47
CROSSINGS = 285
CROSSINGS_MAX = 314


def test_graph_pane_is_980_by_862(loaded_v2_page):
    size = loaded_v2_page.evaluate(
        "() => [window.modelVizApp.cy.width(), window.modelVizApp.cy.height()]"
    )
    assert abs(size[0] - 980) <= 2 and abs(size[1] - 862) <= 2, size


def test_calc_font_is_v1s_ten_px(reset_v2):
    """The style size, not the fitted size: the ruling retired the fitted-font floor."""
    fonts = reset_v2.evaluate(
        """() => window.modelVizApp.cy.nodes('[kind="calc"]')
             .map(n => parseFloat(n.style('font-size')))"""
    )
    assert len(fonts) == 77
    assert set(fonts) == {10.0}


@pytest.mark.parametrize("state", ["start", "all_open", "six_closed"])
def test_no_overlaps(reset_v2, state):
    """No two drawn boxes overlap, and every child sits inside its open parent."""
    page = reset_v2
    if state == "start":
        page.click("[data-action=collapse-all]")
    if state == "six_closed":
        for segment in SIX:
            toggle(page, oracle.identity(oracle.occ_of(SNAP, segment)))
    overlaps, outside = overlaps_and_outside(page)
    print(
        f"{state}: {len(drawn_parts(page))} parts, {len(overlaps)} overlaps, {len(outside)} outside"
    )
    assert overlaps == [] and outside == []


def test_edges_behind_boxes(reset_v2):
    count = edges_behind_boxes(reset_v2)
    print(f"edges behind calc bodies {count} (tripwire {EDGES_BEHIND_BOXES_MAX}, v1 dagre 58)")
    assert count <= EDGES_BEHIND_BOXES_MAX


def test_crossings(reset_v2):
    count = crossings(reset_v2)
    print(f"edge crossings {count} (tripwire {CROSSINGS_MAX}, v1 dagre 338)")
    assert count <= CROSSINGS_MAX


def test_fit_fits(v2_page, fixture_path):
    """Fit puts the whole picture in the pane, and the start state is already fitted."""
    page = v2_page
    assert load_snapshot(page, fixture_path) == "ready"
    start = viewport(page)
    page.evaluate(
        """() => { const cy = window.modelVizApp.cy;
             cy.zoom(2); cy.panBy({x: 200, y: 200}); }"""
    )
    assert viewport(page) != start
    page.click("[data-action=fit]")
    assert viewport(page) == start
    inside = page.evaluate(
        """() => { const cy = window.modelVizApp.cy;
             const b = cy.elements().renderedBoundingBox();
             return b.x1 >= -1 && b.y1 >= -1 && b.x2 <= cy.width() + 1
               && b.y2 <= cy.height() + 1; }"""
    )
    assert inside
