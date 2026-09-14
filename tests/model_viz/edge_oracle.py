"""Independent Python oracle for the viewer's graph: bindings, groups and expected edges.

Computed straight from the raw snapshot JSON. Shares no code or data with the viewer, so a test
that compares the page with this oracle cannot pass by construction (design § Validation Approach).
"""

import json
from functools import cache

from viewer_harness import FIXTURE


@cache
def _fixture_text() -> str:
    return FIXTURE.read_text(encoding="utf-8")


def load_fixture() -> dict:
    """A fresh parse of the fixture; callers may mutate it."""
    return json.loads(_fixture_text())


def calcs(snap) -> list[dict]:
    return snap["instance_graph"]["graph"]["calcs"]


def calc_by_name(snap, name: str) -> dict:
    found = [c for c in calcs(snap) if c["display_name"] == name]
    assert len(found) == 1, f"expected one calc named {name}, found {len(found)}"
    return found[0]


def group_paths(snap) -> list[str]:
    """Distinct full source_file paths, in first-appearance order."""
    return list(dict.fromkeys(c["source_file"] for c in calcs(snap)))


def path_of(snap, node_id: str) -> str:
    return next(c["source_file"] for c in calcs(snap) if c["node_id"] == node_id)


def producer_bindings(snap) -> list[tuple[str, str, str, str]]:
    """(consumer node_id, input name, producer node_id, output id) for every resolved binding."""
    known = {c["node_id"] for c in calcs(snap)}
    out = []
    for calc in calcs(snap):
        for inp in calc["inputs"]:
            edge = inp["edge"]
            if edge is None or edge["kind"] != "producer":
                continue
            producer = edge["target"]["calculation"]
            if producer in known:
                out.append((calc["node_id"], inp["name"], producer, edge["target"]["output"]))
    return out


def expected_edges(snap, collapsed_paths: set[str]) -> list[tuple[str, str]]:
    """Sorted distinct directed pairs under the visible-edge rule, in source-file grouping.

    A calc is represented by group:<path> when its group is collapsed, else by its node_id.
    Bindings whose two representatives are equal are hidden.
    """
    path_by_id = {c["node_id"]: c["source_file"] for c in calcs(snap)}

    def rep(node_id):
        path = path_by_id[node_id]
        return f"group:{path}" if path in collapsed_paths else node_id

    pairs = set()
    for consumer, _name, producer, _output in producer_bindings(snap):
        source, target = rep(producer), rep(consumer)
        if source != target:
            pairs.add((source, target))
    return sorted(pairs)


def expected_occurrence_edges(snap, collapsed_occurrences: set[str]) -> list[tuple[str, str]]:
    """Sorted distinct directed pairs under the visible-edge rule, in occurrence grouping.

    A calc is represented by occ:<id> for the outermost collapsed occurrence among its scope
    occurrence and that occurrence's ancestors, else by its node_id.
    """
    graph = snap["instance_graph"]["graph"]
    parent = {o["occurrence_id"]: o["parent_id"] for o in graph["occurrences"]}
    wire_by_id = {c["node_id"]: c["scope"]["wire"] for c in calcs(snap)}

    def rep(node_id):
        outermost = None
        occurrence = wire_by_id[node_id]
        while occurrence is not None:
            if occurrence in collapsed_occurrences:
                outermost = occurrence
            occurrence = parent[occurrence]
        return node_id if outermost is None else f"occ:{outermost}"

    pairs = set()
    for consumer, _name, producer, _output in producer_bindings(snap):
        source, target = rep(producer), rep(consumer)
        if source != target:
            pairs.add((source, target))
    return sorted(pairs)


def two_way_group_pairs(snap) -> set[frozenset[str]]:
    edges = set(expected_edges(snap, set(group_paths(snap))))
    return {frozenset((s, t)) for s, t in edges if (t, s) in edges}


_DISPLAYED_EDGES_JS = """
() => {
  const cy = window.modelVizApp.cy;
  const identity = (n) => {
    if (n.data('kind') === 'calc') return n.data('node_id');
    return n.data('mode') === 'source'
      ? 'group:' + n.data('group_path')
      : 'occ:' + n.data('occurrence_id');
  };
  return cy.edges().map(e => [identity(e.source()), identity(e.target())]);
}
"""


def displayed_edges(page) -> list[tuple[str, str]]:
    """One (source identity, target identity) per drawn edge, read from cy, sorted, no dedupe."""
    return sorted((s, t) for s, t in page.evaluate(_DISPLAYED_EDGES_JS))


def assert_unique_edge_ids(page) -> None:
    ids = page.evaluate("() => window.modelVizApp.cy.edges().map(e => e.id())")
    assert len(ids) == len(set(ids)), "duplicate edge ids drawn"
