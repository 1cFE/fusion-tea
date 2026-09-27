"""The picture's content (spec § The picture's content, C1–C4): parts, calcs, edges and labels drawn
by v2 equal the independent oracle in every collapse state, with the fixture anchors beside it."""

from collections import Counter

import overlay_oracle as oracle
import pytest
import viewer2_snapshots
from viewer2_harness import (
    click_node,
    drawn_calcs,
    drawn_edge_weights,
    drawn_edges,
    drawn_labels,
    drawn_parts,
    is_closed,
    load_snapshot,
    node_id_of,
    panel_toggle,
    search,
    selected,
    toggle,
)

SNAP = oracle.load_fixture()
ROOT = oracle.roots(SNAP)[0]
MAGNET = oracle.occ_of(SNAP, "magnet")


def collapse_set(state: str) -> set[str]:
    return {
        "open": set(),
        "magnet": {MAGNET},
        "collapse_all": oracle.collapse_all(SNAP),
        "root_children": set(oracle.children(SNAP)[ROOT]),
        "root": {ROOT},
    }[state]


def set_collapse_state(page, state: str) -> None:
    """From all open, reach a collapse state the way the plan names: the handle's toggle, or the
    Collapse all button."""
    if state == "collapse_all":
        page.click("[data-action=collapse-all]")
        return
    for occ in sorted(collapse_set(state)):
        toggle(page, oracle.identity(occ))


def test_oracle_anchors():
    assert len(oracle.all_parts(SNAP)) == 23 and len(oracle.calcs(SNAP)) == 77
    assert len(oracle.producer_bindings(SNAP)) == 152 and oracle.unresolved_bindings(SNAP) == 0
    ranks = oracle.rank(SNAP)
    assert (min(ranks.values()), max(ranks.values())) == (0, 20)
    assert sum(1 for r in ranks.values() if r == 7) == 21
    root_calcs = oracle.direct_calcs(SNAP)[ROOT]
    assert len(root_calcs) == 33 and len({ranks[c] for c in root_calcs}) == 18
    assert len(oracle.collapsible(SNAP)) == 20 and len(oracle.collapse_all(SNAP)) == 19
    assert oracle.occ_of(SNAP, "first_wall") in oracle.collapse_all(SNAP)
    assert len(set(oracle.group_tags(SNAP).values())) == 17
    assert len(oracle.children(SNAP)[ROOT]) == 18


def test_parts_and_parents(reset_v2):
    page = reset_v2
    parts = drawn_parts(page)
    assert parts == oracle.visible_parts(SNAP, set())
    assert len(parts) == 23
    calc_less = {p for p in oracle.all_parts(SNAP) if p not in oracle.collapsible(SNAP)}
    assert sorted(oracle.depths(SNAP)[p] for p in calc_less) == [2, 2, 2]
    assert {oracle.part_name(SNAP, p) for p in calc_less} == {"casing", "coil", "winding_pack"}
    for part in calc_less:
        assert parts[oracle.identity(part)] == oracle.identity(MAGNET)


def test_calcs_in_scope_parts(reset_v2):
    page = reset_v2
    calcs = drawn_calcs(page)
    assert calcs == oracle.visible_calcs(SNAP, set())
    counts = Counter(calcs.values())
    names = {oracle.identity(p): oracle.part_name(SNAP, p) for p in oracle.all_parts(SNAP)}
    assert len(calcs) == 77
    assert counts[oracle.identity(ROOT)] == 33 and counts[oracle.identity(MAGNET)] == 13
    by_name = {names[ident]: n for ident, n in counts.items()}
    assert (by_name["plasma"], by_name["first_wall"], by_name["fuel_cycle"]) == (4, 3, 3)
    assert len([n for n in counts.values() if n in (1, 2)]) == 15
    assert len(counts) == 20


EDGE_ANCHORS = {
    "open": (142, 0),
    "magnet": (128, 12),
    "collapse_all": (116, 21),
    "root_children": (116, 21),
    "root": (0, 152),
}


@pytest.mark.parametrize("state", list(EDGE_ANCHORS))
def test_edges_match_oracle(reset_v2, state):
    page = reset_v2
    set_collapse_state(page, state)
    collapsed = collapse_set(state)
    edges = drawn_edges(page)
    assert edges == oracle.edges(SNAP, collapsed)
    weights = drawn_edge_weights(page)
    assert sum(1 for w in weights if w > 1) == oracle.multi_binding_edges(SNAP, collapsed)
    assert 152 - sum(weights) == oracle.hidden_bindings(SNAP, collapsed)
    assert (len(edges), 152 - sum(weights)) == EDGE_ANCHORS[state]
    if state == "open":
        assert sum(1 for w in weights if w > 1) == 7


@pytest.mark.parametrize("state", ["open", "collapse_all"])
def test_labels_and_tags(reset_v2, state):
    page = reset_v2
    set_collapse_state(page, state)
    collapsed = collapse_set(state)
    labels = drawn_labels(page)
    tags = oracle.calc_tag(SNAP)
    names = {c["node_id"]: c["display_name"] for c in oracle.calcs(SNAP)}
    for ident in oracle.visible_calcs(SNAP, collapsed):
        assert labels[ident] == f"{names[ident]}\n{tags[ident]}", ident
    for ident in oracle.visible_parts(SNAP, collapsed):
        part = oracle.part_of_identity(ident)
        assert labels[ident] == oracle.expected_part_label(SNAP, part, collapsed), ident
    drawn_tags = page.evaluate(
        "() => [...new Set(window.modelVizApp.cy.nodes('[kind=\"calc\"]').map(n => n.data('tag')))]"
    )
    if state == "open":
        assert len(drawn_tags) == 17
        assert labels[oracle.identity(MAGNET)] == "magnet · 13 calcs"
    else:
        assert labels[oracle.identity(MAGNET)] == "magnet (3 parts)\n13 calcs"
        assert labels[oracle.identity(oracle.occ_of(SNAP, "plasma"))] == "plasma\n4 calcs"


def test_unscoped_part_drawn(v2_page, tmp_path):
    snap, moved = viewer2_snapshots.unscoped(SNAP)
    path = viewer2_snapshots.write(tmp_path, "unscoped.json", snap)
    assert load_snapshot(v2_page, path) == "ready"
    # The picture opens with the subsystems closed (owner ruling 2026-09-15); this test is about
    # the fully open content.
    v2_page.click("[data-action=expand-all]")
    parts = drawn_parts(v2_page)
    assert len(parts) == 24 and parts["unscoped"] is None
    assert parts == oracle.visible_parts(snap, set())
    assert (
        v2_page.evaluate(
            "id => window.modelVizApp.cy.getElementById(id).data('occurrence_id')",
            node_id_of(v2_page, "unscoped"),
        )
        is None
    )
    assert drawn_labels(v2_page)["unscoped"] == "unscoped · 1 calc"
    assert drawn_calcs(v2_page)[moved] == "unscoped"
    assert drawn_calcs(v2_page) == oracle.visible_calcs(snap, set())
    assert drawn_edges(v2_page) == oracle.edges(snap, set())
    v2_page.click("[data-action=collapse-all]")
    assert drawn_edges(v2_page) == oracle.edges(snap, oracle.collapse_all(snap))
    assert "unscoped" in drawn_parts(v2_page)


def test_unscoped_tap_and_panel(v2_page, tmp_path):
    """A7, D44: the part without an occurrence has a working tap, panel and Find entry."""
    snap, moved = viewer2_snapshots.unscoped(SNAP)
    path = viewer2_snapshots.write(tmp_path, "unscoped.json", snap)
    assert load_snapshot(v2_page, path) == "ready"
    v2_page.click("[data-action=expand-all]")
    # Tap it as a closed box. Under a global left-to-right layout the `unscoped` root's box
    # interleaves with the other root's, exactly as it does in v1's calc graph, so when it is open
    # the pixels inside it can belong to the box drawn over it.
    toggle(v2_page, "unscoped")
    click_node(v2_page, "unscoped")
    assert selected(v2_page) == {"kind": "part", "occurrenceId": None}
    assert not is_closed(v2_page, "unscoped")
    panel = v2_page.locator("[data-role=panel]")
    assert panel.locator("[data-role=part-name]").text_content() == "unscoped"
    assert (
        panel.locator("[data-role=unscoped-note]").text_content()
        == "These calcs have a scope that names no occurrence in this snapshot."
    )
    assert panel_toggle(v2_page) == {"text": "Collapse", "collapsed": "false"}
    links = panel.locator("section[data-section=part-calcs] [data-calc-key]")
    assert links.count() == 1
    assert panel.locator("section[data-section=attributes]").count() == 0
    assert panel.locator("section[data-section=reach]").count() == 1
    v2_page.click("[data-action=collapse-all]")
    assert not is_closed(v2_page, "unscoped")
    assert selected(v2_page) == {"kind": "part", "occurrenceId": None}
    v2_page.click("[data-role=panel] button[data-action=toggle-part]")
    assert is_closed(v2_page, "unscoped")
    assert panel_toggle(v2_page) == {"text": "Expand", "collapsed": "true"}
    v2_page.evaluate("() => window.modelVizApp.clearSelection()")
    search(v2_page, "unscoped")
    assert selected(v2_page) == {"kind": "part", "occurrenceId": None}
    links.first.click()
    assert v2_page.get_attribute("[data-role=panel]", "data-calc-node-id") == moved
    assert not is_closed(v2_page, "unscoped")
