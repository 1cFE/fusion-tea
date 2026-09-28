"""What a toggle, a tap and a navigation must keep (owner ruling 2026-09-15).

The band packer's pinned geometry is gone: dagre re-runs on every expand and collapse, so boxes
move and the viewport re-fits, exactly as v1's calc graph does. What is still guaranteed is the
content (the drawn parts, calcs and merged edges), the selection, the panel, and where a navigation
lands: the target inside the pane at zoom >= 1, or fitted when its box is too big for that.
"""

import overlay_oracle as oracle
from viewer2_harness import (
    body_boxes,
    click_empty_part_area,
    click_label,
    click_node,
    click_rendered_point,
    collapsed_occurrences,
    css_str,
    drawn_calcs,
    drawn_edges,
    drawn_parts,
    fits_pane,
    focus,
    fully_inside_pane,
    has_clear_control,
    is_closed,
    load_snapshot,
    panel_placeholder,
    panel_toggle,
    selected,
    set_zoom,
    show_calc,
    show_part,
    toggle,
    zoom,
)

from tests.model_viz import structure_oracle

SNAP = oracle.load_fixture()
MAGNET = oracle.occ_of(SNAP, "magnet")
ROOT = oracle.roots(SNAP)[0]


def test_start_state_is_the_subsystem_flow(v2_page, fixture_path):
    """The picture opens with every collapsible part below a root closed, fitted, as v1 starts."""
    page = v2_page
    assert load_snapshot(page, fixture_path) == "ready"
    assert collapsed_occurrences(page) == oracle.collapse_all(SNAP)
    assert drawn_edges(page) == oracle.edges(SNAP, oracle.collapse_all(SNAP))
    assert len(drawn_calcs(page)) == 33
    fitted = page.evaluate(
        """() => { const cy = window.modelVizApp.cy;
             const b = cy.elements().renderedBoundingBox();
             return b.x1 >= -1 && b.y1 >= -1 && b.x2 <= cy.width() + 1
               && b.y2 <= cy.height() + 1; }"""
    )
    assert fitted


def test_toolbar_routes(v2_page, fixture_path):
    page = v2_page
    assert load_snapshot(page, fixture_path) == "ready"
    page.click("[data-action=expand-all]")
    assert drawn_edges(page) == oracle.edges(SNAP, set())

    page.click("[data-action=collapse-all]")
    assert drawn_edges(page) == oracle.edges(SNAP, oracle.collapse_all(SNAP))
    assert not is_closed(page, oracle.identity(ROOT))
    # first_wall is closed too (D29), but it sits inside the closed blanket, so it is not drawn.
    first_wall = oracle.occ_of(SNAP, "first_wall")
    assert oracle.identity(first_wall) not in drawn_parts(page)
    assert first_wall in collapsed_occurrences(page)
    root_calcs = [c for c, parent in drawn_calcs(page).items() if parent == oracle.identity(ROOT)]
    assert len(root_calcs) == 33 and len(drawn_calcs(page)) == 33

    click_node(page, oracle.identity(MAGNET))
    assert not is_closed(page, oracle.identity(MAGNET))
    assert selected(page) == {"kind": "part", "occurrenceId": MAGNET}

    page.click("[data-action=expand-all]")
    assert drawn_edges(page) == oracle.edges(SNAP, set())


def test_tap_open_part_and_label(v2_page, fixture_path):
    page = v2_page
    assert load_snapshot(page, fixture_path) == "ready"
    page.click("[data-action=expand-all]")
    click_empty_part_area(page, oracle.identity(MAGNET))
    assert selected(page) == {"kind": "part", "occurrenceId": MAGNET}
    assert page.evaluate("() => window.modelVizApp.state.collapsed") == []
    assert page.get_attribute("[data-role=panel]", "data-part-occurrence-id") == MAGNET
    page.evaluate("() => window.modelVizApp.clearSelection()")
    # A closed part's label sits inside its box, so a click on it is a tap on the part. An *open*
    # part's label sits in the band above its body, where the pixel belongs to whatever is drawn
    # there — v1 draws an expanded group the same way, and you tap its body.
    toggle(page, oracle.identity(MAGNET))
    focus(page, oracle.identity(MAGNET))
    click_label(page, oracle.identity(MAGNET))
    assert selected(page) == {"kind": "part", "occurrenceId": MAGNET}
    assert not is_closed(page, oracle.identity(MAGNET))
    assert page.get_attribute("[data-role=panel]", "data-part-occurrence-id") == MAGNET


def test_panel_button_both_ways(v2_page, fixture_path):
    page = v2_page
    assert load_snapshot(page, fixture_path) == "ready"
    page.click("[data-action=expand-all]")
    blanket = oracle.occ_of(SNAP, "blanket")
    show_part(page, blanket)
    page.click("[data-role=panel] button[data-action=toggle-part]")
    assert is_closed(page, oracle.identity(blanket))
    assert drawn_edges(page) == oracle.edges(SNAP, {blanket})
    assert panel_toggle(page) == {"text": "Expand", "collapsed": "true"}
    assert selected(page) == {"kind": "part", "occurrenceId": blanket}
    page.click("[data-role=panel] button[data-action=toggle-part]")
    assert not is_closed(page, oracle.identity(blanket))
    assert drawn_edges(page) == oracle.edges(SNAP, set())
    assert selected(page) == {"kind": "part", "occurrenceId": blanket}


def test_clear_control(v2_page, fixture_path):
    page = v2_page
    assert load_snapshot(page, fixture_path) == "ready"
    page.click("[data-action=expand-all]")
    assert not has_clear_control(page)
    show_calc(page, oracle.calc_id(SNAP, "geom"))
    assert has_clear_control(page)
    page.click("[data-role=panel] [data-action=clear-selection]")
    assert selected(page) is None
    assert panel_placeholder(page) == "Select a calc or a part to see its details and reach."
    assert not has_clear_control(page)
    assert page.evaluate("() => window.modelVizApp.cy.elements('.mv-selected').length") == 0
    # A background tap in the fit margin clears too (D36).
    show_calc(page, oracle.calc_id(SNAP, "geom"))
    click_rendered_point(page, 4, 4)
    assert selected(page) is None and panel_placeholder(page) is not None


def producer_link(producer: str) -> str:
    """The selector of a calc panel's producer row link to a calc."""
    row = f"[data-input-kind=producer][data-producer-node-id={css_str(producer)}]"
    return f"[data-role=panel] {row} [data-calc-key]"


def _attr_rows(part: str, kind: str) -> list[dict]:
    return [r for r in structure_oracle.attributes_of(SNAP, part) if r["kind"] == kind]


def _ancestors(part: str) -> set[str]:
    return set(structure_oracle.ancestors(SNAP)[part])


def _calc_chain(part: str) -> set[str]:
    """A calc's closed ancestors are its own part and the parts above it."""
    return {part} | _ancestors(part)


def assert_arrived(page, before: set[str], opened: set[str], ident: str):
    """v1's navigation rule: only the target's closed ancestors opened, and the target is wholly
    inside the pane — centred at zoom >= 1, or fitted when its box is too big for the pane there."""
    assert collapsed_occurrences(page) == before - opened
    assert fully_inside_pane(page, ident), ident
    assert zoom(page) >= 1.0 - 1e-6 or not fits_pane(page, ident, 1.0), (ident, zoom(page))


def test_links_to_hidden_targets(v2_page, fixture_path):
    page = v2_page
    assert load_snapshot(page, fixture_path) == "ready"
    scope = oracle.scope_part(SNAP)

    # 1. An I/O row's calc link: a root calc's producer that sits inside a closed part.
    consumer, _name, producer, _out = next(
        b for b in oracle.producer_bindings(SNAP) if scope[b[0]] == ROOT and scope[b[2]] != ROOT
    )
    page.click("[data-action=collapse-all]")
    set_zoom(page, 0.6)
    show_calc(page, consumer)
    before = collapsed_occurrences(page)
    assert scope[producer] in before
    page.click(producer_link(producer))
    assert page.get_attribute("[data-role=panel]", "data-calc-node-id") == producer
    assert_arrived(page, before, _calc_chain(scope[producer]), producer)

    # 2. A calc-bound value link from a part panel into a closed part.
    page.click("[data-action=collapse-all]")
    set_zoom(page, 0.6)
    show_part(page, ROOT)
    before = collapsed_occurrences(page)
    row = next(
        r for r in _attr_rows(ROOT, "calc-bound") if scope[r["binding"]["calc_node_id"]] != ROOT
    )
    target = row["binding"]["calc_node_id"]
    page.click(
        f"li[data-attr-node-id={css_str(row['node_id'])}] [data-role=value-cell] [data-calc-key]"
    )
    assert page.get_attribute("[data-role=panel]", "data-calc-node-id") == target
    assert_arrived(page, before, _calc_chain(scope[target]), target)

    # 3. A part's calc-list link, with the part itself closed (selected without opening).
    page.click("[data-action=collapse-all]")
    set_zoom(page, 0.6)
    show_part(page, MAGNET)
    before = collapsed_occurrences(page)
    assert MAGNET in before
    link = page.query_selector("[data-role=panel] section[data-section=part-calcs] [data-calc-key]")
    target = page.evaluate(
        "k => window.modelVizApp.model.byKey.get(k).nodeId", link.get_attribute("data-calc-key")
    )
    link.click()
    assert_arrived(page, before, _calc_chain(scope[target]), target)

    # 4. An attribute-bound value link into a closed part.
    page.click("[data-action=collapse-all]")
    set_zoom(page, 0.6)
    source, row = next(
        (p, r)
        for p in oracle.all_parts(SNAP)
        for r in _attr_rows(p, "attr-bound")
        if r["binding"]["target_occurrence_id"] not in (ROOT, p)
    )
    target = row["binding"]["target_occurrence_id"]
    show_part(page, source)
    before = collapsed_occurrences(page)
    page.click(f"li[data-attr-node-id={css_str(row['node_id'])}] [data-target-occurrence-id]")
    assert selected(page) == {"kind": "part", "occurrenceId": target}
    assert page.get_attribute("[data-role=panel]", "data-part-occurrence-id") == target
    assert_arrived(page, before, _ancestors(target), oracle.identity(target))

    # 5. A navigation to a calc that is already drawn opens nothing, so no layout runs and no fit
    # happens: the zoom the modeler was at is kept, as v1 keeps it.
    set_zoom(page, 1.5)
    before = collapsed_occurrences(page)
    page.evaluate(
        "n => { const app = window.modelVizApp; app.navigateTo(app.model.keyByNodeId.get(n)); }",
        consumer,
    )
    assert collapsed_occurrences(page) == before
    assert abs(zoom(page) - 1.5) < 1e-6
    assert fully_inside_pane(page, consumer)


def test_reversal(v2_page, fixture_path):
    """Close and reopen: the drawn content comes back to exactly what the oracle says."""
    page = v2_page
    assert load_snapshot(page, fixture_path) == "ready"
    page.click("[data-action=expand-all]")
    steps = [("close", MAGNET), ("close", ROOT), ("open", ROOT), ("open", MAGNET)]
    collapsed: set[str] = set()
    for action, part in steps:
        toggle(page, oracle.identity(part))
        collapsed = collapsed - {part} if action == "open" else collapsed | {part}
        assert collapsed_occurrences(page) == collapsed, (action, part)
        assert drawn_edges(page) == oracle.edges(SNAP, collapsed), (action, part)


def test_selection_moves_nothing(v2_page, fixture_path):
    """A10, I27: a selection's reach classes change colour and nothing else. No re-layout runs, so
    every drawn box stays exactly where it was."""
    page = v2_page
    assert load_snapshot(page, fixture_path) == "ready"
    page.click("[data-action=expand-all]")
    before = body_boxes(page)
    show_calc(page, oracle.calc_id(SNAP, "geom"))
    assert page.evaluate("() => window.modelVizApp.cy.elements('.mv-downstream').length") > 0
    assert body_boxes(page) == before
    show_part(page, MAGNET)
    assert body_boxes(page) == before
    page.evaluate("() => window.modelVizApp.clearSelection()")
    assert body_boxes(page) == before
