"""Structure view criteria S1–S7 and the start state (D16), read from the live renderer and compared
with structure_oracle's reading of the raw snapshot."""

import viewer_snapshots as vs
from edge_oracle import load_fixture
from structure_oracle import (
    calc_count,
    depth_counts,
    descendants,
    displayed_parts,
    expected_parts,
    occurrences,
    start_collapsed,
)
from viewer_harness import load_snapshot, switch_view, toggle_part


def occurrence_by_segment(snap, segment: str) -> str:
    (found,) = [o["occurrence_id"] for o in occurrences(snap) if o["display_segment"] == segment]
    return found


def calcs_line(count: int) -> str:
    return "1 calc" if count == 1 else f"{count} calcs"


def test_every_occurrence_is_a_part(fixture_page):
    snap = load_fixture()
    page = fixture_page
    switch_view(page, "structure")
    page.click("[data-action=expand-all]")
    drawn = page.evaluate(
        "() => window.modelVizApp.cy.nodes('[kind=\"part\"]').map(n => n.data('occurrence_id'))"
    )
    assert len(drawn) == 23
    assert sorted(drawn) == sorted(o["occurrence_id"] for o in occurrences(snap))


def test_containment_matches_snapshot(fixture_page):
    snap = load_fixture()
    page = fixture_page
    switch_view(page, "structure")
    page.click("[data-action=expand-all]")
    got = displayed_parts(page)
    assert got == expected_parts(snap, collapsed=set())
    assert len([p for p in got if p[1] is not None]) == 22
    assert depth_counts(page) == {0: 1, 1: 18, 2: 4}


def test_start_state(fixture_page):
    snap = load_fixture()
    page = fixture_page
    switch_view(page, "structure")
    assert start_collapsed(snap) == {
        occurrence_by_segment(snap, "magnet"),
        occurrence_by_segment(snap, "blanket"),
    }
    got = displayed_parts(page)
    assert len(got) == 19
    assert got == expected_parts(snap, start_collapsed(snap))
    flagged = page.evaluate(
        """() => window.modelVizApp.cy.nodes('[kind="part"]')
             .filter(n => n.data('collapsed')).map(n => n.data('occurrence_id'))"""
    )
    assert set(flagged) == start_collapsed(snap)


def test_same_segment_siblings(viewer_page, tmp_path):
    snap, _expected, (twin_a, twin_b) = vs.overlay(load_fixture())
    plant = occurrence_by_segment(snap, "plant")
    assert load_snapshot(viewer_page, vs.write(snap, tmp_path / "overlay.json")) == "ready"
    switch_view(viewer_page, "structure")
    viewer_page.click("[data-action=expand-all]")
    got = displayed_parts(viewer_page)
    assert got == expected_parts(snap, set())
    assert (twin_a, plant) in got and (twin_b, plant) in got
    names = viewer_page.evaluate(
        """([a, b]) => window.modelVizApp.cy.nodes('[kind="part"]')
             .filter(n => n.data('occurrence_id') === a || n.data('occurrence_id') === b)
             .map(n => [n.id(), n.data('label').split('\\n')[0]])""",
        [twin_a, twin_b],
    )
    assert len({node_id for node_id, _ in names}) == 2
    assert [name for _, name in names] == ["twin", "twin"]


def test_no_calcs_and_calc_counts(fixture_page):
    snap = load_fixture()
    page = fixture_page
    switch_view(page, "structure")
    page.click("[data-action=expand-all]")
    assert page.evaluate("() => window.modelVizApp.cy.nodes('[kind!=\"part\"]').length") == 0
    assert page.evaluate("() => window.modelVizApp.cy.edges().length") == 0
    lines = dict(
        page.evaluate(
            """() => window.modelVizApp.cy.nodes('[kind="part"]')
                 .map(n => [n.data('occurrence_id'), n.data('label').split('\\n')])"""
        )
    )
    counts = calc_count(snap)
    assert {occ: label[1] for occ, label in lines.items()} == {
        occ: calcs_line(n) for occ, n in counts.items()
    }
    magnet = occurrence_by_segment(snap, "magnet")
    for segment in ("casing", "coil", "winding_pack"):
        occ = occurrence_by_segment(snap, segment)
        assert (
            next(o["parent_id"] for o in occurrences(snap) if o["occurrence_id"] == occ) == magnet
        )
        assert lines[occ][1] == "0 calcs"


def parts_with_children(snap) -> set[str]:
    return {o["parent_id"] for o in occurrences(snap) if o["parent_id"] is not None}


def test_collapse_round_trip(fixture_page):
    """S5: expand all, collapse all, expand all, by toolbar clicks from the start state."""
    snap = load_fixture()
    page = fixture_page
    switch_view(page, "structure")
    page.click("[data-action=expand-all]")
    first = displayed_parts(page)
    assert first == expected_parts(snap, set())
    page.click("[data-action=collapse-all]")
    (root,) = [o["occurrence_id"] for o in occurrences(snap) if o["parent_id"] is None]
    assert displayed_parts(page) == expected_parts(snap, parts_with_children(snap))
    assert displayed_parts(page) == [(root, None)]
    page.click("[data-action=expand-all]")
    assert displayed_parts(page) == expected_parts(snap, set())
    assert displayed_parts(page) == first


def test_per_part_round_trip(fixture_page):
    """S6: from all open, each part with children collapses and expands back."""
    snap = load_fixture()
    page = fixture_page
    switch_view(page, "structure")
    page.click("[data-action=expand-all]")
    everything = displayed_parts(page)
    below = descendants(snap)
    for segment in ("stellaris", "magnet", "blanket"):
        occ = occurrence_by_segment(snap, segment)
        assert below[occ], segment
        toggle_part(page, occ)
        collapsed = displayed_parts(page)
        assert collapsed == expected_parts(snap, {occ}), segment
        drawn = {part for part, _parent in collapsed}
        assert occ in drawn and not drawn & below[occ], segment  # stays drawn, descendants gone
        toggle_part(page, occ)
        assert displayed_parts(page) == everything, segment


def test_nested_round_trip(fixture_page):
    """S7: collapse magnet, collapse stellaris, expand stellaris, expand magnet."""
    snap = load_fixture()
    page = fixture_page
    switch_view(page, "structure")
    page.click("[data-action=expand-all]")
    start = displayed_parts(page)
    collapsed: set[str] = set()
    steps = [
        ("collapse", "magnet"),
        ("collapse", "stellaris"),
        ("expand", "stellaris"),
        ("expand", "magnet"),
    ]
    for action, segment in steps:
        occ = occurrence_by_segment(snap, segment)
        toggle_part(page, occ)
        if action == "collapse":
            collapsed.add(occ)
        else:
            collapsed.discard(occ)
        assert displayed_parts(page) == expected_parts(snap, collapsed), (action, segment)
    assert displayed_parts(page) == start
