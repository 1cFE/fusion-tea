"""Find (spec R14, design D39): exact path, exact segment, exact calc name, then substring; one
match navigates, several report the count by kind, none says so."""

import overlay_oracle as oracle
from viewer2_harness import (
    collapsed_occurrences,
    load_snapshot,
    search,
    search_status,
    selected,
    zoom,
)

SNAP = oracle.load_fixture()
MAGNET = oracle.occ_of(SNAP, "magnet")


def test_exact_segment_beats_substring_calc(v2_page, fixture_path):
    page = v2_page
    assert load_snapshot(page, fixture_path) == "ready"
    page.click("[data-action=collapse-all]")
    assert oracle.find_matches(SNAP, "coil") == ([oracle.identity(oracle.occ_of(SNAP, "coil"))], [])
    search(page, "coil")
    assert selected(page) == {"kind": "part", "occurrenceId": oracle.occ_of(SNAP, "coil")}
    assert search_status(page) == ""
    assert collapsed_occurrences(page) == oracle.collapse_all(SNAP) - {MAGNET}
    assert zoom(page) >= 1.0


def test_exact_calc_name_opens_only_its_part(v2_page, fixture_path):
    page = v2_page
    assert load_snapshot(page, fixture_path) == "ready"
    page.click("[data-action=collapse-all]")
    wp_stress = oracle.calc_id(SNAP, "wp_stress")
    assert oracle.find_matches(SNAP, "wp_stress") == ([], [wp_stress])
    assert oracle.scope_part(SNAP)[wp_stress] == MAGNET
    search(page, "WP_Stress")
    key = page.evaluate("id => window.modelVizApp.model.keyByNodeId.get(id)", wp_stress)
    assert selected(page) == {"kind": "calc", "key": key}
    assert collapsed_occurrences(page) == oracle.collapse_all(SNAP) - {MAGNET}
    assert page.get_attribute("[data-role=panel]", "data-calc-node-id") == wp_stress


def test_several_matches_report_the_count_by_kind(reset_v2):
    page = reset_v2
    page.evaluate("() => window.modelVizApp.clearSelection()")
    parts, calcs = oracle.find_matches(SNAP, "cas")
    assert (len(parts), len(calcs)) == (1, 9)
    search(page, "cas")
    assert search_status(page) == "10 matches (1 part, 9 calcs)"
    assert selected(page) is None


def test_no_match(reset_v2):
    page = reset_v2
    assert oracle.find_matches(SNAP, "nothing_here") == ([], [])
    search(page, "nothing_here")
    assert search_status(page) == "no part or calc matches"


def test_datalist_holds_every_path_and_name(loaded_v2_page):
    options = loaded_v2_page.eval_on_selector_all(
        "datalist[data-role=find-list] option", "os => os.map(o => o.value)"
    )
    paths = {oracle.part_path(SNAP, p) for p in oracle.all_parts(SNAP)}
    names = {c["display_name"] for c in oracle.calcs(SNAP)}
    assert len(options) == 100 and set(options) == paths | names
    assert len(paths) == 23 and len(names) == 77
