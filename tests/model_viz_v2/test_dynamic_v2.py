"""Drag and Spacing (owner ruling 2026-09-15).

A drag is the modeler's explicit act and moves a box and its edges. Nothing pins it: the next
layout run replaces it, which is what v1's re-layout would do, and "Reset layout" runs one on
demand. The Spacing control multiplies dagre's node and rank separations and re-runs the layout.
"""

import overlay_oracle as oracle
from viewer2_harness import (
    body_boxes,
    drag_node,
    drawn_calcs,
    drawn_edges,
    drawn_parts,
    edge_endpoints,
    load_snapshot,
    overlaps_and_outside,
    reset_layout,
    selected,
    set_spacing,
    show_calc,
    spacing,
    toggle,
)

SNAP = oracle.load_fixture()
MAGNET = oracle.occ_of(SNAP, "magnet")
VESSEL_COST = oracle.calc_id(SNAP, "vessel_cost")
DX, DY = 70.0, 110.0


def test_drag_moves_a_calc_and_its_edges(v2_page, fixture_path):
    page = v2_page
    assert load_snapshot(page, fixture_path) == "ready"
    page.click("[data-action=expand-all]")
    before = body_boxes(page)
    before_edges = edge_endpoints(page)
    zoom = page.evaluate("() => window.modelVizApp.cy.zoom()")

    drag_node(page, VESSEL_COST, DX, DY)

    after = body_boxes(page)
    moved = after[VESSEL_COST]
    dx = moved["x1"] - before[VESSEL_COST]["x1"]
    dy = moved["y1"] - before[VESSEL_COST]["y1"]
    print(f"dragged {VESSEL_COST} by ({dx:.1f}, {dy:.1f}) model px at zoom {zoom:.3f}")
    assert abs(dx - DX / zoom) < 2 and abs(dy - DY / zoom) < 2

    # Its edges follow. A straight edge meets a box on the perimeter facing the other end, so the
    # endpoint does not travel the same delta as the box; what must hold is that it moved, and that
    # it still sits on the moved box.
    after_edges = edge_endpoints(page)
    touching = [k for k in before_edges if VESSEL_COST in k]
    assert touching, "vessel_cost has no drawn edges"
    margin = 2.0
    for key in touching:
        sx1, sy1, tx1, ty1 = after_edges[key]
        end = (sx1, sy1) if key[0] == VESSEL_COST else (tx1, ty1)
        was = before_edges[key][0:2] if key[0] == VESSEL_COST else before_edges[key][2:4]
        assert (end[0] - was[0]) ** 2 + (end[1] - was[1]) ** 2 > 1, (key, end, was)
        assert moved["x1"] - margin <= end[0] <= moved["x2"] + margin, (key, end)
        assert moved["y1"] - margin <= end[1] <= moved["y2"] + margin, (key, end)

    # Reset layout re-runs dagre, which is deterministic, so every box is back where it was.
    reset_layout(page)
    assert body_boxes(page) == before


def test_toggle_relayouts_and_drops_the_drag(v2_page, fixture_path):
    """A toggle re-runs the layout, exactly as v1's does, so a drag offset does not survive it."""
    page = v2_page
    assert load_snapshot(page, fixture_path) == "ready"
    page.click("[data-action=expand-all]")
    before = body_boxes(page)
    drag_node(page, VESSEL_COST, DX, DY)
    assert body_boxes(page)[VESSEL_COST] != before[VESSEL_COST]
    toggle(page, oracle.identity(MAGNET))
    toggle(page, oracle.identity(MAGNET))
    assert body_boxes(page) == before


def test_drag_keeps_the_selection_and_the_edge_set(v2_page, fixture_path):
    page = v2_page
    assert load_snapshot(page, fixture_path) == "ready"
    page.click("[data-action=expand-all]")
    show_calc(page, VESSEL_COST)
    before = selected(page)
    edges = drawn_edges(page)
    drag_node(page, VESSEL_COST, -60.0, -40.0)
    assert selected(page) == before
    assert drawn_edges(page) == edges
    assert page.evaluate("() => window.modelVizApp.cy.elements('.mv-selected').length") == 1


def test_spacing_two_then_back_to_one(v2_page, fixture_path):
    page = v2_page
    assert load_snapshot(page, fixture_path) == "ready"
    page.click("[data-action=expand-all]")
    start = body_boxes(page)
    edges = drawn_edges(page)
    show_calc(page, VESSEL_COST)
    chosen = selected(page)
    parts, calcs = len(drawn_parts(page)), len(drawn_calcs(page))

    set_spacing(page, 2)
    assert spacing(page) == 2
    overlaps, outside = overlaps_and_outside(page)
    print(f"spacing 2: {len(overlaps)} overlaps, {len(outside)} children outside their parent")
    assert overlaps == [] and outside == []
    assert drawn_edges(page) == edges
    assert len(drawn_parts(page)) == parts and len(drawn_calcs(page)) == calcs
    assert selected(page) == chosen
    # The picture really did spread out: the root's room is wider and taller than at spacing 1.
    root_id = oracle.identity(oracle.roots(SNAP)[0])
    root = body_boxes(page)[root_id]
    assert root["x2"] - root["x1"] > start[root_id]["x2"] - start[root_id]["x1"]
    assert root["y2"] - root["y1"] > start[root_id]["y2"] - start[root_id]["y1"]

    set_spacing(page, 1)
    assert spacing(page) == 1
    assert body_boxes(page) == start
    assert drawn_edges(page) == edges
    assert selected(page) == chosen


def test_spacing_keeps_the_collapse_set(v2_page, fixture_path):
    page = v2_page
    assert load_snapshot(page, fixture_path) == "ready"
    page.click("[data-action=collapse-all]")
    collapsed = page.evaluate("() => window.modelVizApp.state.collapsedOccurrences")
    edges = drawn_edges(page)
    set_spacing(page, 1.5)
    assert page.evaluate("() => window.modelVizApp.state.collapsedOccurrences") == collapsed
    assert drawn_edges(page) == edges
    overlaps, outside = overlaps_and_outside(page)
    assert overlaps == [] and outside == []
