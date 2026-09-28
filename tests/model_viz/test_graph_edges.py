"""Graph criteria G1–G7: nodes, groups and the displayed edges in every collapse state.

Edges are read from the live Cytoscape instance and compared with edge_oracle, never with the
viewer's own projection.
"""

from edge_oracle import (
    assert_unique_edge_ids,
    calcs,
    displayed_edges,
    expected_edges,
    group_paths,
    load_fixture,
    producer_bindings,
    two_way_group_pairs,
)
from viewer_harness import calc_node_count, toggle_group

ACCOUNT_COSTS = "root-0/analyses/mfe_account_costs.sysml"
GENERIC_PLANT = "root-0/designs/generic_mfe/mfe_plant.sysml"
STELLARATOR_PLANT = "root-0/designs/stellarator_09/stellarator_plant.sysml"
TWO_WAY_PAIRS = {
    frozenset((f"group:{ACCOUNT_COSTS}", f"group:{GENERIC_PLANT}")),
    frozenset(
        (
            "group:root-0/analyses/mfe_plasma_scaling.sysml",
            "group:root-0/analyses/mfe_plasma_sustainment.sysml",
        )
    ),
    frozenset(
        (
            "group:root-0/analyses/mfe_magnet_field.sysml",
            "group:root-0/analyses/mfe_plasma_scaling.sysml",
        )
    ),
    frozenset(
        (
            "group:root-0/analyses/mfe_power_balance.sysml",
            "group:root-0/analyses/mfe_primary_loop.sysml",
        )
    ),
}


def containers(page) -> list[dict]:
    return page.evaluate(
        """() => window.modelVizApp.cy.nodes('[kind="container"]').map(n => ({
             path: n.data('group_path'), kind: n.data('container_kind'),
             count: n.data('member_count'), collapsed: n.data('collapsed')}))"""
    )


def test_calc_nodes(fixture_page):
    fixture_page.click("[data-action=expand-all]")
    assert calc_node_count(fixture_page) == 77  # WI-057 (2026-09-13): feat/demo-maturation's WI-050 operating_heat (+1 calc, +3 outputs, +2 bound attributes)
    drawn = fixture_page.evaluate(
        "() => window.modelVizApp.cy.nodes('[kind=\"calc\"]').map(n => n.data('node_id'))"
    )
    assert sorted(drawn) == sorted(c["node_id"] for c in calcs(load_fixture()))


def test_source_groups(fixture_page):
    snap = load_fixture()
    drawn = containers(fixture_page)
    assert len(drawn) == 17
    assert sorted(d["path"] for d in drawn) == sorted(group_paths(snap))
    assert all(d["collapsed"] for d in drawn), "every group starts collapsed (D5)"
    by_path = {d["path"]: d for d in drawn}
    for path in group_paths(snap):
        assert by_path[path]["count"] == sum(1 for c in calcs(snap) if c["source_file"] == path)
    assert by_path[ACCOUNT_COSTS]["count"] == 33
    design = {d["path"]: d["count"] for d in drawn if d["kind"] == "design"}
    assert design == {GENERIC_PLANT: 10, STELLARATOR_PLANT: 1}
    assert {d["kind"] for d in drawn if d["path"] not in design} == {"analysis"}


def test_all_expanded_edges(fixture_page):
    snap = load_fixture()
    fixture_page.click("[data-action=expand-all]")
    got = displayed_edges(fixture_page)
    assert got == expected_edges(snap, collapsed_paths=set())
    assert len(got) == 142  # WI-057 (2026-09-13): feat/demo-maturation's WI-050 operating_heat (+1 calc, +3 outputs, +2 bound attributes)
    assert_unique_edge_ids(fixture_page)
    binding_pairs = {(producer, consumer) for consumer, _, producer, _ in producer_bindings(snap)}
    assert set(got) <= binding_pairs, "every drawn edge points producer -> consumer of a binding"


def test_only_producer_inputs_make_edges(fixture_page):
    snap = load_fixture()
    fixture_page.click("[data-action=expand-all]")
    got = set(displayed_edges(fixture_page))
    attr_ids = {a["node_id"] for a in snap["instance_graph"]["graph"]["attrs"]}
    assert not {end for pair in got for end in pair} & attr_ids

    producer_pairs = set()
    other_pairs = set()
    for calc in calcs(snap):
        for inp in calc["inputs"]:
            edge = inp["edge"]
            if edge is None:
                other_pairs.add(("default:" + inp["name"], calc["node_id"]))
            elif edge["kind"] == "producer":
                producer_pairs.add((edge["target"]["calculation"], calc["node_id"]))
            elif edge["kind"] == "node":
                other_pairs.add((edge["target"], calc["node_id"]))
            else:
                other_pairs.add((f"literal:{edge['value']}", calc["node_id"]))
    assert len(other_pairs) > 0
    assert got == producer_pairs
    assert not got & (other_pairs - producer_pairs)


def test_all_collapsed_edges(fixture_page):
    snap = load_fixture()
    fixture_page.click("[data-action=expand-all]")
    fixture_page.click("[data-action=collapse-all]")
    got = displayed_edges(fixture_page)
    assert got == expected_edges(snap, collapsed_paths=set(group_paths(snap)))
    assert len(got) == 36  # WI-057 (2026-09-13): feat/demo-maturation's WI-050 operating_heat (+1 calc, +3 outputs, +2 bound attributes)
    assert all(s != t for s, t in got), "no self-loops"
    assert two_way_group_pairs(snap) == TWO_WAY_PAIRS
    for pair in TWO_WAY_PAIRS:
        a, b = sorted(pair)
        assert (a, b) in got and (b, a) in got
    assert_unique_edge_ids(fixture_page)


def test_round_trip_every_group(fixture_page):
    snap = load_fixture()
    fixture_page.click("[data-action=expand-all]")
    start = displayed_edges(fixture_page)
    assert start == expected_edges(snap, collapsed_paths=set())
    for path in group_paths(snap):
        toggle_group(fixture_page, path)
        assert displayed_edges(fixture_page) == expected_edges(snap, collapsed_paths={path}), path
        assert_unique_edge_ids(fixture_page)
        toggle_group(fixture_page, path)
        assert displayed_edges(fixture_page) == start, path


def test_round_trip_interleaved(fixture_page):
    snap = load_fixture()
    fixture_page.click("[data-action=expand-all]")
    start = displayed_edges(fixture_page)
    collapsed_paths: set[str] = set()
    steps = [
        ("collapse", ACCOUNT_COSTS),
        ("collapse", GENERIC_PLANT),
        ("expand", ACCOUNT_COSTS),
        ("expand", GENERIC_PLANT),
    ]
    for action, path in steps:
        toggle_group(fixture_page, path)
        if action == "collapse":
            collapsed_paths.add(path)
        else:
            collapsed_paths.discard(path)
        want = expected_edges(snap, collapsed_paths)
        assert displayed_edges(fixture_page) == want, (action, path)
        assert_unique_edge_ids(fixture_page)
    assert displayed_edges(fixture_page) == start


def test_no_calc_output_reaches_a_calc_through_an_attribute(fixture_path):
    """Fixture premise behind I4 (design § Non-Goals): only producer bindings become edges.

    If a calc output fed an attribute that another calc reads as a parameter, the viewer would
    draw no edge for that dependency: the consumer's input record is a `node` edge to the
    attribute, not a `producer` edge to the calc. In the snapshot, an attribute fed by a calc is
    an alias whose `alias_target` is a producer binding. So the premise holds when no parameter
    input targets an alias attribute. A regenerated fixture that breaks this needs a follow-on
    item, not a silent change to the edge rule.
    """
    snap = load_fixture()
    attrs = {a["node_id"]: a for a in snap["instance_graph"]["graph"]["attrs"]}
    calc_fed = {
        node_id
        for node_id, a in attrs.items()
        if a["is_alias"] and (a["alias_target"] or {}).get("kind") == "producer"
    }
    assert len(calc_fed) > 0, "the snapshot does record calc-fed attributes, as aliases"
    parameter_targets = [
        inp["edge"]["target"]
        for calc in calcs(snap)
        for inp in calc["inputs"]
        if inp["edge"] is not None and inp["edge"]["kind"] == "node"
    ]
    assert len(parameter_targets) == 236  # WI-057 (2026-09-13): feat/demo-maturation's WI-050 operating_heat (+1 calc, +3 outputs, +2 bound attributes)
    assert all(target in attrs for target in parameter_targets)
    assert not [t for t in parameter_targets if t in calc_fed or attrs[t]["is_alias"]]
