"""Panels (spec § Panels, P1–P3; design D38, D45): v2's calc and part panels equal v1's once v2's
named additions are removed, the toggle sits on exactly the collapsible parts, and a toggle
re-renders the panel without moving anything."""

import copy

import overlay_oracle as oracle
import pytest
from viewer2_harness import (
    has_clear_control,
    load_snapshot,
    panel_toggle,
    reach_section,
    show_calc,
    show_part,
    toggle,
)

from tests.model_viz.panel_dom import panel_dump
from tests.model_viz.part_panel_dom import part_panel_dump

SNAP = oracle.load_fixture()
V2_CALC_SECTIONS = ("reach", "trace")
# D37's reach colours as the browser reports them; the headings are the canvas key (A9).
UPSTREAM_COLOUR = "rgb(25, 113, 194)"
DOWNSTREAM_COLOUR = "rgb(47, 158, 68)"


def without_v2_calc_additions(dump: dict) -> dict:
    """D45: drop exactly the reach and trace sections from a calc dump."""
    out = copy.deepcopy(dump)
    out["sections"] = [s for s in out["sections"] if s not in V2_CALC_SECTIONS]
    for name in V2_CALC_SECTIONS:
        out["sectionText"].pop(name, None)
    return out


def reach_section_text(page) -> str | None:
    return page.text_content("[data-role=panel] section[data-section=reach]")


def test_calc_panels_match_v1(v1_loaded, loaded_v2_page):
    page = loaded_v2_page
    checked = 0
    for calc in oracle.calcs(SNAP):
        node_id = calc["node_id"]
        show_calc(v1_loaded, node_id)
        show_calc(page, node_id)
        v2 = panel_dump(page)
        assert "reach" in v2["sections"] and "trace" not in v2["sections"], node_id
        assert v2["sections"].index("reach") == v2["sections"].index("outputs") + 1, node_id
        assert has_clear_control(page), node_id
        assert without_v2_calc_additions(v2) == panel_dump(v1_loaded), node_id
        checked += 1
    assert checked == 77


def test_part_panels_match_v1(v1_loaded, loaded_v2_page):
    page = loaded_v2_page
    v1_loaded.evaluate("() => window.modelVizApp.setView('structure')")
    v1_loaded.click("[data-action=expand-all]")
    page.evaluate("() => window.modelVizApp.expandAll()")
    collapsible = oracle.collapsible(SNAP)
    kids = oracle.children(SNAP)
    calc_only = 0
    for part in oracle.all_parts(SNAP):
        show_part(v1_loaded, part)
        show_part(page, part)
        v2 = part_panel_dump(page)
        assert reach_section_text(page) is not None
        assert has_clear_control(page), part
        if part in collapsible and not kids[part]:
            assert v2["toggle"] == {"text": "Collapse", "collapsed": "false"}, part
            v2["toggle"] = None
            calc_only += 1
        assert v2 == part_panel_dump(v1_loaded), part
    assert calc_only == 17


def test_toggle_button_on_exactly_the_collapsible_parts(loaded_v2_page):
    page = loaded_v2_page
    page.evaluate("() => window.modelVizApp.expandAll()")
    with_button = set()
    for part in oracle.all_parts(SNAP):
        show_part(page, part)
        button = panel_toggle(page)
        if button is not None:
            assert button == {"text": "Collapse", "collapsed": "false"}, part
            with_button.add(part)
    assert with_button == oracle.collapsible(SNAP) and len(with_button) == 20
    for part in sorted(oracle.collapse_all(SNAP)):
        toggle(page, oracle.identity(part))
        show_part(page, part)
        assert panel_toggle(page) == {"text": "Expand", "collapsed": "true"}, part
    page.evaluate("() => window.modelVizApp.expandAll()")


@pytest.mark.usefixtures("fixture_path")
def test_toggle_rerenders_panel(v2_page, fixture_path):
    page = v2_page
    assert load_snapshot(page, fixture_path) == "ready"
    page.click("[data-action=expand-all]")
    magnet = oracle.occ_of(SNAP, "magnet")
    show_part(page, magnet)
    assert panel_toggle(page) == {"text": "Collapse", "collapsed": "false"}
    page.click("[data-role=panel] button[data-action=toggle-part]")
    assert panel_toggle(page) == {"text": "Expand", "collapsed": "true"}
    assert magnet in set(page.evaluate("() => window.modelVizApp.state.collapsedOccurrences"))
    assert reach_section_text(page) is not None
    assert page.query_selector("[data-role=panel] [data-role=panel-bar]") is not None
    assert page.evaluate("() => window.modelVizApp.state.selected") == {
        "kind": "part",
        "occurrenceId": magnet,
    }
    page.click("[data-role=panel] button[data-action=toggle-part]")
    assert panel_toggle(page) == {"text": "Collapse", "collapsed": "false"}
    assert page.evaluate("() => window.modelVizApp.state.selected") == {
        "kind": "part",
        "occurrenceId": magnet,
    }


def test_reach_section_groups(loaded_v2_page, reset_v2):
    """D38, A9: the reach section lists each direction's calcs grouped by their owning part, in
    drawn tree order, with the canvas colours on the headings."""
    page = loaded_v2_page
    for sel in [("calc", "geom"), ("calc", "lcoe_calc"), ("part", "magnet")]:
        kind, name = sel
        if kind == "calc":
            show_calc(page, oracle.calc_id(SNAP, name))
        else:
            show_part(page, oracle.occ_of(SNAP, name))
        got = reach_section(page)
        want = oracle.reach_lists(SNAP, sel)
        for direction, colour in (
            ("upstream", UPSTREAM_COLOUR),
            ("downstream", DOWNSTREAM_COLOUR),
        ):
            total = sum(len(group["calcs"]) for group in want[direction])
            title = direction.capitalize()
            assert got[direction]["heading"] == f"{title} ({total})", (sel, direction)
            assert got[direction]["colour"] == colour, (sel, direction)
            assert got[direction]["groups"] == want[direction], (sel, direction)
