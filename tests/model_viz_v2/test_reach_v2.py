"""Reach (spec § Reach, R9; design D37, I28, I32): what a selection feeds and is fed by, lit on the
canvas. Every class is compared with the oracle's own reading of the raw snapshot, never with the
page's projection of it."""

import overlay_oracle as oracle
import pytest
from viewer2_harness import (
    calc_key,
    collapsed_occurrences,
    css_str,
    drawn_classes,
    load_snapshot,
    rendered_centre_offset,
    selected,
    set_zoom,
    show_calc,
    show_part,
    toggle,
    zoom,
)

SNAP = oracle.load_fixture()

# The nine fixture calcs with a non-root part holding both an upstream and a downstream member of
# their reach, with those parts (spec § Reach).
BOTH_CONES = [
    ("cycle", ["blanket", "heat_transport"]),
    ("primary_loop", ["blanket"]),
    ("pb", ["blanket", "cryoplant", "heat_transport", "turbine"]),
    ("sustain", ["plasma"]),
    ("casing_mass", ["magnet"]),
    ("winding_pack_cost", ["magnet"]),
    ("magnet_structure_cost", ["magnet"]),
    ("peak_field_calc", ["magnet"]),
    ("wp_stress", ["magnet"]),
]


def select(page, sel):
    kind, name = sel
    if kind == "calc":
        show_calc(page, oracle.calc_id(SNAP, name))
    else:
        show_part(page, oracle.occ_of(SNAP, name))


def set_collapse_state(page, state):
    page.evaluate("() => window.modelVizApp.expandAll()")
    if state == "collapse_all":
        page.evaluate("() => window.modelVizApp.collapseAll()")
    elif state != "open":
        toggle(page, oracle.identity(oracle.occ_of(SNAP, state)))


def classes_of(page, kind):
    """Identity -> class for the drawn calcs (kind "calc") or parts (kind "part")."""
    nodes = drawn_classes(page)["nodes"]
    calcs = {c["node_id"] for c in oracle.calcs(SNAP)}
    return {i: c for i, c in nodes.items() if (i in calcs) == (kind == "calc")}


def count(page, name):
    return sum(1 for c in classes_of(page, "calc").values() if c == name)


def test_reach_anchors(loaded_v2_page, reset_v2):
    """The spec's anchors, read from the page's classes and from the oracle (do not edit these)."""
    page = loaded_v2_page
    scope = oracle.scope_part(SNAP)

    select(page, ("calc", "geom"))
    geom = oracle.calc_id(SNAP, "geom")
    lcoe = oracle.calc_id(SNAP, "lcoe_calc")
    assert count(page, "mv-downstream") == 57 == len(oracle.downstream(SNAP, geom))
    assert classes_of(page, "calc")[lcoe] == "mv-downstream"
    assert count(page, "mv-upstream") == 0 == len(oracle.upstream(SNAP, geom))

    select(page, ("calc", "lcoe_calc"))
    assert count(page, "mv-upstream") == 64 == len(oracle.upstream(SNAP, lcoe))
    assert classes_of(page, "calc")[geom] == "mv-upstream"

    select(page, ("part", "magnet"))
    magnet = oracle.occ_of(SNAP, "magnet")
    s_calcs = oracle.selection_calcs(SNAP, ("part", "magnet"))
    up, down = set(), set()
    for node_id in s_calcs:
        up |= oracle.upstream(SNAP, node_id)
        down |= oracle.downstream(SNAP, node_id)
    assert len(s_calcs) == 13
    assert len(down) == 67 and sum(1 for c in down if scope[c] != magnet) == 58
    assert len(up) == 10 and sum(1 for c in up if scope[c] != magnet) == 1
    assert len(up & down) == 5
    drawn = classes_of(page, "calc")
    assert {i for i, c in drawn.items() if c in ("mv-downstream", "mv-both")} == down
    assert {i for i, c in drawn.items() if c in ("mv-upstream", "mv-both")} == up
    assert count(page, "mv-both") == 5

    assert len(oracle.selection_calcs(SNAP, ("part", "blanket"))) == 5


@pytest.mark.parametrize(
    "sel", [("calc", "geom"), ("calc", "lcoe_calc"), ("part", "magnet"), ("part", "blanket")]
)
@pytest.mark.parametrize("state", ["open", "magnet", "collapse_all"])
def test_every_class_equals_oracle(loaded_v2_page, reset_v2, sel, state):
    page = loaded_v2_page
    set_collapse_state(page, state)
    select(page, sel)
    assert drawn_classes(page) == oracle.classes(SNAP, oracle.state(SNAP, state), sel)


def test_no_classes_without_a_selection(loaded_v2_page, reset_v2):
    page = loaded_v2_page
    show_calc(page, oracle.calc_id(SNAP, "geom"))
    page.evaluate("() => window.modelVizApp.clearSelection()")
    assert drawn_classes(page) == oracle.classes(SNAP, set(), None)


def test_calc_less_leaves_unclassed(loaded_v2_page, reset_v2):
    """A4b: a leaf part owning no calc carries no class, as an open part does."""
    page = loaded_v2_page
    select(page, ("calc", "geom"))
    owned = oracle.direct_calcs(SNAP)
    kids = oracle.children(SNAP)
    leaves = [p for p in oracle.all_parts(SNAP) if not owned[p] and not kids.get(p)]
    assert leaves, "the fixture has no calc-less leaf part"
    drawn = classes_of(page, "part")
    for part in leaves:
        assert drawn[oracle.identity(part)] is None, part


def test_hidden_selection(loaded_v2_page, reset_v2):
    """The selection survives the part that hides it closing: the box stands for it (D37)."""
    page = loaded_v2_page
    sustain = oracle.calc_id(SNAP, "sustain")
    select(page, ("calc", "sustain"))
    page.evaluate("() => window.modelVizApp.collapseAll()")
    collapsed = oracle.collapse_all(SNAP)
    plasma = oracle.identity(oracle.occ_of(SNAP, "plasma"))
    got = drawn_classes(page)
    assert selected(page) == {
        "kind": "calc",
        "key": page.evaluate("id => window.modelVizApp.model.keyByNodeId.get(id)", sustain),
    }
    assert got["selected"] == plasma
    assert got["nodes"][plasma] is not None
    assert got == oracle.classes(SNAP, collapsed, ("calc", "sustain"))
    assert page.get_attribute("[data-role=panel]", "data-calc-node-id") == sustain


def test_divheat_member_not_dim(loaded_v2_page, reset_v2):
    """M2, I32: divertor hides the selection plus unrelated calcs and no cone member."""
    page = loaded_v2_page
    page.evaluate("() => window.modelVizApp.collapseAll()")
    select(page, ("calc", "divheat"))
    got = drawn_classes(page)
    divertor = oracle.identity(oracle.occ_of(SNAP, "divertor"))
    assert got["nodes"][divertor] == "mv-member"
    assert got["selected"] == divertor
    assert got == oracle.classes(SNAP, oracle.collapse_all(SNAP), ("calc", "divheat"))


@pytest.mark.parametrize("name,parts", BOTH_CONES, ids=[row[0] for row in BOTH_CONES])
def test_both_cones(loaded_v2_page, reset_v2, name, parts):
    """Each named part holds an upstream and a downstream member of the calc's reach, so it is
    mv-both when closed and its members carry their own direction when open (spec § Reach)."""
    page = loaded_v2_page
    select(page, ("calc", name))
    # The test handle's toggle closes a part while the calc stays selected (spec § Reach).
    for part in parts:
        toggle(page, oracle.identity(oracle.occ_of(SNAP, part)))
    collapsed = {oracle.occ_of(SNAP, part) for part in parts}
    got = drawn_classes(page)
    for part in parts:
        assert got["nodes"][oracle.identity(oracle.occ_of(SNAP, part))] == "mv-both", part
    assert got == oracle.classes(SNAP, collapsed, ("calc", name))

    page.evaluate("() => window.modelVizApp.expandAll()")
    got = drawn_classes(page)
    assert got == oracle.classes(SNAP, set(), ("calc", name))
    owner = oracle.scope_part(SNAP)
    for part in parts:
        members = oracle.subtree_calcs(SNAP, oracle.occ_of(SNAP, part))
        held = {got["nodes"][c] for c in members}
        assert held & {"mv-upstream", "mv-both"}, (part, owner, held)
        assert held & {"mv-downstream", "mv-both"}, (part, held)


def test_classes_after_toggle(loaded_v2_page, reset_v2):
    """I28: classes are recomputed on every redraw."""
    page = loaded_v2_page
    select(page, ("calc", "geom"))
    blanket = oracle.occ_of(SNAP, "blanket")
    assert drawn_classes(page) == oracle.classes(SNAP, set(), ("calc", "geom"))
    toggle(page, oracle.identity(blanket))
    assert drawn_classes(page) == oracle.classes(SNAP, {blanket}, ("calc", "geom"))
    toggle(page, oracle.identity(blanket))
    assert drawn_classes(page) == oracle.classes(SNAP, set(), ("calc", "geom"))


def test_reach_link_to_hidden_target(v2_page, fixture_path):
    """A real click on a reach-section link opens only the target's closed ancestors and lands the
    target centred at zoom >= 1, v1's navigation rule (owner ruling 2026-09-15)."""
    page = v2_page
    assert load_snapshot(page, fixture_path) == "ready"
    page.click("[data-action=collapse-all]")
    set_zoom(page, 0.6)
    show_calc(page, oracle.calc_id(SNAP, "geom"))
    before = collapsed_occurrences(page)

    target = oracle.calc_id(SNAP, "blanket_cost")
    scope = oracle.scope_part(SNAP)
    assert scope[target] in before
    key = css_str(calc_key(page, target))
    link = page.query_selector(
        f"[data-role=panel] section[data-section=reach] button.calc-link[data-calc-key={key}]"
    )
    assert link is not None, "the reach section has no link to blanket_cost"
    link.click()

    assert page.get_attribute("[data-role=panel]", "data-calc-node-id") == target
    ancestors = {scope[target], *oracle.part_ancestors(SNAP)[scope[target]]}
    assert collapsed_occurrences(page) == before - ancestors
    assert abs(zoom(page) - 1.0) < 1e-6
    dx, dy = rendered_centre_offset(page, target)
    assert abs(dx) <= 2 and abs(dy) <= 2


def test_lit_elements_are_painted(loaded_v2_page, reset_v2):
    """D37's colours reach the canvas: a class that no later stylesheet rule overrides."""
    page = loaded_v2_page
    select(page, ("calc", "geom"))
    painted = page.evaluate(
        """() => {
             const cy = window.modelVizApp.cy;
             const one = (selector, property) => {
               const ele = cy.elements(selector)[0];
               return ele === undefined ? null : ele.style(property);
             };
             return {
               calcBorder: one('node[kind="calc"].mv-downstream', 'border-color'),
               edgeLine: one('edge.mv-downstream', 'line-color'),
               edgeArrow: one('edge.mv-downstream', 'target-arrow-color'),
               edgeOpacity: one('edge.mv-downstream', 'opacity'),
               dimCalc: one('node[kind="calc"].mv-dim', 'opacity'),
               dimEdge: one('edge.mv-dim', 'opacity'),
               selected: one('node.mv-selected', 'overlay-color'),
             };
           }"""
    )
    assert painted["calcBorder"] == "rgb(47,158,68)"
    assert painted["edgeLine"] == "rgb(47,158,68)" and painted["edgeArrow"] == "rgb(47,158,68)"
    assert float(painted["edgeOpacity"]) == 1
    assert float(painted["dimCalc"]) == 0.2 and float(painted["dimEdge"]) == 0.12
    assert painted["selected"] == "rgb(217,72,15)"
