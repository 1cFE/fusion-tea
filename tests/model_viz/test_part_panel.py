"""Part panel criteria P1–P4: header, type name, exact attribute lists, owners, sources and value
kinds, read from the rendered panel of every part and compared with the raw snapshot."""

from collections import Counter

import pytest
import viewer_snapshots as vs
from edge_oracle import load_fixture
from part_panel_dom import part_panel_dump
from structure_oracle import (
    attributes_of,
    calc_count,
    children,
    occurrences,
    oracle_type_names,
    path_of,
    short_path,
)
from viewer_harness import calc_key, load_snapshot, switch_view

TYPE_NAMES = {
    "stellaris": "mfe_plant::'MFE Power Plant'",
    "blanket/first_wall": "mfe_radial_build_parts::'First Wall'",
    "cryoplant": "mfe_plant_systems::Cryoplant",
    "fuel_cycle": "mfe_plant_systems::'Fuel Cycle'",
    "heat_transport": "mfe_plant_systems::'Primary Heat Transport'",
    "vacuum_pumping": "mfe_plant_systems::'Vacuum Pumping'",
    "plasma": "mfe_plasma::Plasma",
    "magnet/casing": "mfe_magnet_parts::'Coil Casing'",
    "magnet/coil": "mfe_magnet_parts::'Modular Coil'",
    "magnet/winding_pack": "mfe_magnet_parts::'Winding Pack'",
}
NOT_RECORDED = [
    "blanket",
    "buildings",
    "divertor",
    "electric_plant",
    "heat_rejection",
    "heating",
    "magnet",
    "misc_plant",
    "power_supplies",
    "shield",
    "structure",
    "turbine",
    "vessel",
]
# Spec § Success Criteria, the per-part table (attributes owned directly).
ATTR_COUNTS = {
    "stellaris": 77,
    "blanket": 18,
    "blanket/first_wall": 15,
    "buildings": 14,
    "cryoplant": 17,
    "divertor": 18,
    "electric_plant": 7,
    "fuel_cycle": 22,
    "heat_rejection": 7,
    "heat_transport": 26,
    "heating": 18,
    "magnet": 16,
    "magnet/casing": 6,
    "magnet/coil": 16,
    "magnet/winding_pack": 10,
    "misc_plant": 7,
    "plasma": 25,
    "power_supplies": 8,
    "shield": 10,
    "structure": 8,
    "turbine": 19,
    "vacuum_pumping": 4,
    "vessel": 9,
}


@pytest.fixture(scope="module")
def parts(loaded_fixture_page):
    """{short path: panel dump} from one sweep of showPart over every occurrence (plan PD4)."""
    snap = load_fixture()
    page = loaded_fixture_page
    switch_view(page, "structure")
    out = {}
    for occ in occurrences(snap):
        page.evaluate("id => window.modelVizApp.showPart(id)", occ["occurrence_id"])
        out[short_path(snap, occ["occurrence_id"])] = part_panel_dump(page)
    return out


def rows_of(panel) -> list[dict]:
    return [row for group in panel["groups"] for row in group["rows"]]


def occurrence_by_short_path(snap) -> dict[str, str]:
    return {short_path(snap, o["occurrence_id"]): o["occurrence_id"] for o in occurrences(snap)}


def test_not_recorded_list_is_the_complement():
    snap = load_fixture()
    assert sorted(set(occurrence_by_short_path(snap)) - set(TYPE_NAMES)) == NOT_RECORDED
    assert set(ATTR_COUNTS) == set(occurrence_by_short_path(snap))


def test_header_every_part(parts):
    snap = load_fixture()
    counts = calc_count(snap)
    kids = children(snap)
    assert len(parts) == 23
    for short, occ in occurrence_by_short_path(snap).items():
        panel = parts[short]
        assert panel["occurrenceId"] == occ and panel["calcNodeId"] is None
        assert panel["name"] == short.split("/")[-1]
        assert panel["path"] == path_of(snap, occ)
        n = counts[occ]
        assert panel["calcCount"] == ("1 calc" if n == 1 else f"{n} calcs")
        assert len(panel["calcLinks"]) == n
        if n == 0:
            assert "this part owns no calcs" in panel["calcsText"]
        if kids[occ]:
            assert panel["toggle"] is not None, short
        else:
            assert panel["toggle"] is None, short
    with_toggle = sorted(short for short, panel in parts.items() if panel["toggle"] is not None)
    assert with_toggle == ["blanket", "magnet", "stellaris"]
    # From the start state: the root is expanded, magnet and blanket are collapsed (D16).
    assert parts["stellaris"]["toggle"] == {"text": "Collapse", "collapsed": "false"}
    assert parts["magnet"]["toggle"] == {"text": "Expand", "collapsed": "true"}


def test_part_calc_links_in_snapshot_order(parts, loaded_fixture_page):
    snap = load_fixture()
    for short, occ in occurrence_by_short_path(snap).items():
        expected = [
            (calc_key(loaded_fixture_page, c["node_id"]), c["display_name"])
            for c in snap["instance_graph"]["graph"]["calcs"]
            if c["scope"]["wire"] == occ
        ]
        assert [(link["key"], link["text"]) for link in parts[short]["calcLinks"]] == expected


def test_type_names_exact(parts):
    named = {p: v["typeText"] for p, v in parts.items() if v["typeRecorded"] == "true"}
    assert named == TYPE_NAMES
    not_recorded = [p for p, v in parts.items() if v["typeRecorded"] == "false"]
    assert sorted(not_recorded) == NOT_RECORDED
    assert all(parts[p]["typeText"] == "type not recorded" for p in not_recorded)
    assert all(parts[p]["typeReason"] for p in not_recorded)
    assert all(parts[p]["typeReason"] is None for p in named)
    assert named == oracle_type_names(load_fixture())


def test_attribute_lists_exact(parts):
    snap = load_fixture()
    for short, occ in occurrence_by_short_path(snap).items():
        panel = parts[short]
        expected = attributes_of(snap, occ)
        rows = rows_of(panel)
        assert Counter(r["nodeId"] for r in rows) == Counter(r["node_id"] for r in expected)
        assert panel["attrCount"] == str(ATTR_COUNTS[short]) == str(len(expected))
        # Owner groups in first-appearance order; rows in snapshot order within each group.
        owners = list(dict.fromkeys(r["owner"] for r in expected))
        assert [g["owner"] for g in panel["groups"]] == owners
        for group in panel["groups"]:
            want = [r["node_id"] for r in expected if r["owner"] == group["owner"]]
            assert [r["nodeId"] for r in group["rows"]] == want
    assert parts["blanket"]["attrCount"] == "18"
    root_groups = {g["owner"]: g["heading"] for g in parts["stellaris"]["groups"]}
    assert root_groups["stellarator_09::stellaris"].endswith("declared on this part")
    assert not root_groups["mfe_plant::'MFE Power Plant'"].endswith("declared on this part")


def test_row_owner_and_source(parts):
    snap = load_fixture()
    total = 0
    for short, occ in occurrence_by_short_path(snap).items():
        expected = {r["node_id"]: r for r in attributes_of(snap, occ)}
        for row in rows_of(parts[short]):
            want = expected[row["nodeId"]]
            assert (row["name"], row["owner"], row["source"]) == (
                want["name"],
                want["owner"],
                want["source"],
            )
            assert row["sourceText"] == want["source"]
            total += 1
    assert total == 377


def assert_value_cell(row, want, page):
    kind = want["kind"]
    if kind == "recorded":
        if isinstance(want["value"], str):
            assert row["value"] == want["value"]
        else:
            assert float(row["value"]) == want["value"]
        assert row["cellText"] == row["value"]
    elif kind == "calc-bound":
        binding = want["binding"]
        assert row["cellText"] == f"bound to {binding['text']}"
        assert row["calcKey"] == calc_key(page, binding["calc_node_id"])
        assert row["outputId"] == binding["output_id"]
        assert not row["undeclaredOutput"]
    elif kind == "attr-bound":
        binding = want["binding"]
        assert row["cellText"] == f"bound to {binding['text']}"
        assert row["targetOccurrenceId"] == binding["target_occurrence_id"]
        assert row["targetAttrNodeId"] == binding["target_attr_node_id"]
    elif kind == "none":
        assert row["cellText"] == "no value in the snapshot"
        assert row["hasWarning"]
    else:
        raise AssertionError(f"unexpected oracle kind {kind}")


def test_value_kinds_and_totals(parts, loaded_fixture_page):
    snap = load_fixture()
    kinds = Counter()
    recorded_types = Counter()
    for short, occ in occurrence_by_short_path(snap).items():
        expected = {r["node_id"]: r for r in attributes_of(snap, occ)}
        for row in rows_of(parts[short]):
            want = expected[row["nodeId"]]
            assert row["kind"] == want["kind"], (short, row["name"])
            assert row["cellText"].strip() != "", (short, row["name"])
            assert_value_cell(row, want, loaded_fixture_page)
            kinds[row["kind"]] += 1
            if row["kind"] == "recorded":
                recorded_types[type(want["value"]).__name__] += 1
    assert kinds == {"recorded": 196, "calc-bound": 143, "attr-bound": 12, "none": 26}
    assert kinds["unresolved"] == 0
    assert recorded_types == {"float": 183, "str": 13}


def test_part_without_attributes_or_types(viewer_page, tmp_path):
    snap, _expected, _twins = vs.overlay(load_fixture())
    assert load_snapshot(viewer_page, vs.write(snap, tmp_path / "overlay.json")) == "ready"
    (plant,) = [o["occurrence_id"] for o in occurrences(snap) if o["display_segment"] == "plant"]
    viewer_page.evaluate("id => window.modelVizApp.showPart(id)", plant)
    panel = part_panel_dump(viewer_page)
    assert panel["name"] == "plant" and panel["path"] == "stellaris/plant"
    assert panel["attrCount"] == "0"
    assert panel["noAttributes"] == "no attributes recorded"
    assert panel["groups"] == []
    assert (panel["typeRecorded"], panel["typeText"]) == ("false", "type not recorded")
    assert panel["typeReason"] == "no type ids recorded"
    assert panel["toggle"] == {"text": "Expand", "collapsed": "true"}  # depth 1 with children (D16)
