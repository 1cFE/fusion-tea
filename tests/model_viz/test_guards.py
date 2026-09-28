"""Guard criteria U1–U2 on synthetic snapshots: an unresolvable producer, occurrence grouping."""

import viewer_snapshots as vs
from edge_oracle import (
    calcs,
    displayed_edges,
    expected_edges,
    expected_occurrence_edges,
    group_paths,
    load_fixture,
)
from panel_dom import panel_dump
from viewer_harness import calc_node_count, css_str, load_snapshot, show_calc


def test_unresolvable_producer(viewer_page, tmp_path):
    fixture = load_fixture()
    snap, removed = vs.remove_most_consumed_calc(fixture)
    consumers = vs.consumers_of(fixture, removed)
    assert len({c for c, _ in consumers}) > 1
    path = vs.write(snap, tmp_path / "removed.json")
    assert load_snapshot(viewer_page, path) == "ready"
    viewer_page.click("[data-action=expand-all]")
    assert calc_node_count(viewer_page) == 76  # WI-057 (2026-09-13): feat/demo-maturation's WI-050 operating_heat (+1 calc, +3 outputs, +2 bound attributes)

    got = displayed_edges(viewer_page)
    assert got == expected_edges(snap, collapsed_paths=set())
    assert removed not in {end for pair in got for end in pair}
    assert viewer_page.evaluate(
        """() => window.modelVizApp.cy.edges()
             .every(e => e.source().nonempty() && e.target().nonempty())"""
    )

    for consumer, input_name in consumers:
        show_calc(viewer_page, consumer)
        row = viewer_page.query_selector(
            f"[data-input-kind=producer][data-input-name={css_str(input_name)}][data-unresolved]"
        )
        assert row is not None, (consumer, input_name)
        assert row.get_attribute("data-producer-node-id") == removed
        warning = row.query_selector(".warning")
        assert warning is not None and warning.is_visible()
        assert removed in row.text_content()


def test_undeclared_output_and_unknown_input_kind(viewer_page, tmp_path):
    snap, picked = vs.undeclared_output_and_unknown_kind(load_fixture())
    path = vs.write(snap, tmp_path / "odd_ports.json")
    assert load_snapshot(viewer_page, path) == "ready"
    viewer_page.click("[data-action=expand-all]")
    assert displayed_edges(viewer_page) == expected_edges(snap, collapsed_paths=set())

    consumer, input_name, producer = picked["producer_input"]
    show_calc(viewer_page, consumer)
    row = next(r for r in panel_dump(viewer_page)["inputs"] if r["name"] == input_name)
    assert row["kind"] == "producer" and row["outputId"] == "undeclared-output-id"
    assert "undeclared output" in row["text"] and row["hasWarning"]

    show_calc(viewer_page, producer)
    undeclared = [o for o in panel_dump(viewer_page)["outputs"] if o["undeclared"]]
    assert [
        (o["outputId"], [(c["nodeId"], c["inputName"]) for c in o["consumers"]]) for o in undeclared
    ] == [("undeclared-output-id", [(consumer, input_name)])]

    calc_id, unknown_name = picked["unknown_input"]
    show_calc(viewer_page, calc_id)
    row = next(r for r in panel_dump(viewer_page)["inputs"] if r["name"] == unknown_name)
    assert row["kind"] == "unknown" and "unknown input kind: wire" in row["text"]


_PARENT_CHAINS_JS = """
() => {
  const cy = window.modelVizApp.cy;
  const out = {};
  cy.nodes('[kind="calc"]').forEach(n => {
    const chain = [];
    for (let p = n.parent(); p.nonempty(); p = p.parent()) {
      chain.push({id: p.id(), occurrence: p.data('occurrence_id'), mode: p.data('mode')});
    }
    out[n.data('node_id')] = {
      chain,
      hasBothFields: 'source_group' in n.data() && 'occurrence_id' in n.data(),
      sourceGroup: n.data('source_group'),
      occurrence: n.data('occurrence_id'),
    };
  });
  return out;
}
"""


def test_overlay_occurrence_grouping(viewer_page, tmp_path):
    snap, expected, (twin_a, twin_b) = vs.overlay(load_fixture())
    path = vs.write(snap, tmp_path / "overlay.json")
    assert load_snapshot(viewer_page, path) == "ready"
    viewer_page.select_option("[data-role=mode-select]", label="Occurrence")
    collapsed = viewer_page.evaluate(
        "() => window.modelVizApp.cy.nodes('[kind=\"container\"]').map(n => n.data('collapsed'))"
    )
    assert collapsed == [True], "switching mode collapses everything; only the root is visible"
    viewer_page.click("[data-action=expand-all]")

    chains = viewer_page.evaluate(_PARENT_CHAINS_JS)
    assert set(chains) == {c["node_id"] for c in calcs(snap)}
    containers_by_occurrence: dict[str, set[str]] = {}
    for node_id, info in chains.items():
        assert info["hasBothFields"], node_id
        assert info["occurrence"] == expected[node_id]
        assert all(link["mode"] == "occurrence" for link in info["chain"])
        assert [link["occurrence"] for link in info["chain"]] == vs.occurrence_chain(
            snap, expected[node_id]
        ), node_id
        for link in info["chain"]:
            containers_by_occurrence.setdefault(link["occurrence"], set()).add(link["id"])

    # One container per occurrence id; the two same-segment siblings stay separate.
    assert all(len(ids) == 1 for ids in containers_by_occurrence.values())
    assert containers_by_occurrence[twin_a] != containers_by_occurrence[twin_b]
    labels = viewer_page.evaluate(
        """([a, b]) => window.modelVizApp.cy.nodes('[kind="container"]')
             .filter(n => n.data('occurrence_id') === a || n.data('occurrence_id') === b)
             .map(n => n.data('label'))""",
        [twin_a, twin_b],
    )
    assert labels == ["twin", "twin"]

    split = [n for n, c in chains.items() if c["occurrence"] in (twin_a, twin_b)]
    split_files = {next(c["source_file"] for c in calcs(snap) if c["node_id"] == n) for n in split}
    assert split_files == {vs.OVERLAY_SPLIT_FILE}
    assert {chains[n]["occurrence"] for n in split} == {twin_a, twin_b}
    assert len({chains[n]["sourceGroup"] for n in split}) == 1

    viewer_page.select_option("[data-role=mode-select]", label="Source file")
    groups = viewer_page.evaluate(
        """() => window.modelVizApp.cy.nodes('[kind="container"]').map(n =>
             [n.data('mode'), n.data('group_path'), n.data('collapsed')])"""
    )
    assert len(groups) == 17
    assert sorted(g[1] for g in groups) == sorted(group_paths(snap))
    assert all(mode == "source" and is_collapsed for mode, _, is_collapsed in groups)


def toggle_occurrence(page, occurrence_id: str) -> None:
    """Toggle the drawn container for an occurrence id (reads cy only to find the id)."""
    ids = page.evaluate(
        """occ => window.modelVizApp.cy.nodes('[kind="container"]')
             .filter(n => n.data('occurrence_id') === occ).map(n => n.id())""",
        occurrence_id,
    )
    assert len(ids) == 1, f"expected one drawn container for {occurrence_id}, found {ids}"
    page.evaluate("id => window.modelVizApp.toggleContainer(id)", ids[0])


def test_overlay_occurrence_edges_under_collapse(viewer_page, tmp_path):
    """The visible-edge rule in occurrence grouping, against the oracle, with nested collapses."""
    snap, _expected, (twin_a, twin_b) = vs.overlay(load_fixture())
    occurrences = snap["instance_graph"]["graph"]["occurrences"]
    (root,) = [o["occurrence_id"] for o in occurrences if o["parent_id"] is None]
    (plant,) = [o["occurrence_id"] for o in occurrences if o["display_segment"] == "plant"]
    path = vs.write(snap, tmp_path / "overlay.json")
    assert load_snapshot(viewer_page, path) == "ready"
    viewer_page.select_option("[data-role=mode-select]", label="Occurrence")
    viewer_page.click("[data-action=expand-all]")
    start = displayed_edges(viewer_page)
    assert start == expected_occurrence_edges(snap, set())
    assert any(twin_a in e for pair in expected_occurrence_edges(snap, {twin_a}) for e in pair)

    collapsed: set[str] = set()
    steps = [
        ("collapse", twin_a),
        ("collapse", twin_b),
        ("collapse", plant),  # twin_a and twin_b stay collapsed underneath; plant is outermost
        ("expand", plant),
        ("expand", twin_a),
        ("expand", twin_b),
        ("collapse", root),
        ("expand", root),
    ]
    for action, occurrence in steps:
        toggle_occurrence(viewer_page, occurrence)
        if action == "collapse":
            collapsed.add(occurrence)
        else:
            collapsed.discard(occurrence)
        want = expected_occurrence_edges(snap, collapsed)
        assert displayed_edges(viewer_page) == want, (action, occurrence)
    assert displayed_edges(viewer_page) == start
