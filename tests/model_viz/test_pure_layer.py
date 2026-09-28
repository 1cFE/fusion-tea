"""The pure layer called directly through page.evaluate: formula printer, doc-repeat test,
snapshot reading, and the visible-edge rule on a small hand-built snapshot."""

import pytest

PRINT_JS = "ir => ModelViz.formula.printExpression(ir)"


def ref(name):
    return {"kind": "feature_ref", "reference": {"source_name": name}}


def lit(value):
    return {"kind": "literal", "literal": {"kind": "LiteralRational", "value": value}}


def op(operator, *operands):
    return {"kind": "operator", "operator": operator, "operands": list(operands)}


@pytest.mark.parametrize(
    ("tree", "printed"),
    [
        (op("+", ref("a"), ref("b"), ref("c")), "a + b + c"),
        (op("*", ref("k"), op("+", ref("a"), ref("b"))), "k * (a + b)"),
        (op("+", ref("a"), op("*", ref("k"), ref("b"))), "a + k * b"),
        (op("+", ref("magnet.capital_cost"), lit(9400.0)), "magnet.capital_cost + 9400"),
        (op("*", lit(0.5), ref("x")), "0.5 * x"),
        (op("/", ref("a"), ref("b")), None),
        (op("+", ref("a"), op("/", ref("b"), ref("c"))), None),
        (op("+", ref("a")), None),
        (op("+", ref("a"), lit(None)), None),
        (op("+", ref("a"), lit("3")), None),
        (op("+", ref("a"), ref("")), None),
        ({"kind": "operator", "operator": "+"}, None),
        ({"kind": "call", "name": "sqrt"}, None),
        (None, None),
    ],
)
def test_print_expression(viewer_page, tree, printed):
    assert viewer_page.evaluate(PRINT_JS, tree) == printed


@pytest.mark.parametrize(
    ("entry", "doc", "expected"),
    [
        ("x = a + b\n\nDocumentation:\nAdds things.", "Adds things.", True),
        ("See documentation:\nAdds things.", "Adds things.", True),
        ("x = a + b", "Adds things.", False),
        ("x = a + b", "", False),
        ("x = a + b", None, False),
    ],
)
def test_ends_with_doc(viewer_page, entry, doc, expected):
    got = viewer_page.evaluate("([e, d]) => ModelViz.formula.endsWithDoc(e, d)", [entry, doc])
    assert got is expected


READ_JS = """text => {
  try { ModelViz.model.readSnapshot(text); return {ok: true}; }
  catch (err) { return {ok: false, name: err.name, message: err.message}; }
}"""


def test_read_snapshot_refuses_wrong_version(viewer_page):
    got = viewer_page.evaluate(
        READ_JS, '{"instance_graph": {"schema_version": "instance-graph/v2", "graph": {}}}'
    )
    assert got["ok"] is False and got["name"] == "SnapshotError"
    assert "instance-graph/v3" in got["message"] and "instance-graph/v2" in got["message"]


# A small snapshot: two source files, three nested occurrences, a two-way file pair.
ROOT, SUB, LEAF = '[["r",null]]', '[["r",null],["a",null]]', '[["r",null],["a",null],["b",null]]'


def calc(node_id, source_file, wire, inputs):
    return {
        "node_id": node_id,
        "display_name": node_id,
        "source_file": source_file,
        "source_line": 1,
        "scope": {"kind": "occurrence", "wire": wire},
        "calc_expressions": [],
        "doc_comment": None,
        "expression_ir": None,
        "inputs": [
            {
                "name": f"in_{producer}",
                "metadata": {},
                "edge": {"kind": "producer", "target": {"calculation": producer, "output": "o"}},
            }
            for producer in inputs
        ],
        "outputs": [{"name": "o", "port": {"calculation": node_id, "output": "o"}}],
    }


SMALL = {
    "instance_graph": {
        "schema_version": "instance-graph/v3",
        "graph": {
            "occurrences": [
                {"occurrence_id": ROOT, "parent_id": None, "display_segment": "root"},
                {"occurrence_id": SUB, "parent_id": ROOT, "display_segment": "sub"},
                {"occurrence_id": LEAF, "parent_id": SUB, "display_segment": "leaf"},
            ],
            "attrs": [],
            "calcs": [
                calc("p", "f1.sysml", LEAF, []),
                calc("q", "f1.sysml", SUB, ["p", "s"]),
                calc("r", "f2.sysml", ROOT, ["q", "p"]),
                calc("s", "f2.sysml", ROOT, ["r"]),
            ],
        },
    }
}

VIEW_JS = """([snap, mode, collapsedIds]) => {
  const model = ModelViz.model.buildModel(ModelViz.model.readSnapshot(JSON.stringify(snap)));
  const tree = ModelViz.view.containerTree(model, mode);
  const els = ModelViz.view.visibleElements(model, tree, new Set(collapsedIds));
  const name = id => model.byKey.has(id) ? model.byKey.get(id).name : id;
  const bindingEnds = id => {
    const b = model.bindingById.get(id);
    return [model.byKey.get(b.producer).name, model.byKey.get(b.consumer).name];
  };
  const bindingIdentity = id => {
    const b = model.bindingById.get(id);
    return [model.byKey.get(b.consumer).name, b.inputName];
  };
  return {
    containers: [...tree.containers.values()].map(c => [c.id, c.parent, c.label, c.memberCount]),
    edgesById: els.filter(e => e.group === 'edges').map(e =>
      [name(e.data.source), name(e.data.target), e.data.bindings.map(bindingIdentity)]),
    nodes: els.filter(e => e.group === 'nodes').map(e => name(e.data.id)).sort(),
    edges: els.filter(e => e.group === 'edges').map(e =>
      [name(e.data.source), name(e.data.target), e.data.bindings.map(bindingEnds)]),
  };
}"""


def run_view(page, mode, collapsed):
    return page.evaluate(VIEW_JS, [SMALL, mode, collapsed])


def edge_map(result):
    return {(s, t): sorted(tuple(b) for b in bs) for s, t, bs in result["edges"]}


def test_view_all_expanded_one_edge_per_calc_pair(viewer_page):
    got = run_view(viewer_page, "source", [])
    assert edge_map(got) == {
        ("p", "q"): [("p", "q")],
        ("s", "q"): [("s", "q")],
        ("q", "r"): [("q", "r")],
        ("p", "r"): [("p", "r")],
        ("r", "s"): [("r", "s")],
    }


def test_view_collapsed_group_drops_self_loop_and_merges(viewer_page):
    # g0 is f1.sysml (p, q). p -> q is inside it and vanishes; q -> r and p -> r merge.
    got = run_view(viewer_page, "source", ["g0"])
    assert got["nodes"] == ["g0", "g1", "r", "s"]
    assert edge_map(got) == {
        ("g0", "r"): [("p", "r"), ("q", "r")],
        ("r", "s"): [("r", "s")],
        ("s", "g0"): [("s", "q")],
    }


def test_view_two_way_pair_gives_two_edges(viewer_page):
    got = run_view(viewer_page, "source", ["g0", "g1"])
    assert got["nodes"] == ["g0", "g1"]
    assert edge_map(got) == {
        ("g0", "g1"): [("p", "r"), ("q", "r")],
        ("g1", "g0"): [("s", "q")],
    }


def test_view_occurrence_tree_nests_by_parent(viewer_page):
    got = run_view(viewer_page, "occurrence", [])
    assert got["containers"] == [
        ["o0", None, "root", 4],
        ["o1", "o0", "sub", 2],
        ["o2", "o1", "leaf", 1],
    ]


def test_view_nested_collapse_maps_to_outermost_collapsed(viewer_page):
    # Collapsing both sub (o1) and leaf (o2): p and q are represented by o1, the outer one.
    got = run_view(viewer_page, "occurrence", ["o1", "o2"])
    assert got["nodes"] == ["o0", "o1", "r", "s"]
    assert edge_map(got) == {
        ("o1", "r"): [("p", "r"), ("q", "r")],
        ("r", "s"): [("r", "s")],
        ("s", "o1"): [("s", "q")],
    }


# Container ids the viewer assigns on SMALL, and what each contains, written out by hand:
# source groups in first-appearance order; occurrences in snapshot order.
SOURCE_CONTAINER = {"g0": "f1.sysml", "g1": "f2.sysml"}
OCCURRENCE_CONTAINER = {"o0": ROOT, "o1": SUB, "o2": LEAF}
OCCURRENCE_PARENT = {ROOT: None, SUB: ROOT, LEAF: SUB}


def small_representative(calc_raw, mode, collapsed):
    """Outermost collapsed container on the calc's chain (by viewer id), else the calc's name."""
    if mode == "source":
        chain = [cid for cid, path in SOURCE_CONTAINER.items() if path == calc_raw["source_file"]]
    else:
        by_occurrence = {occ: cid for cid, occ in OCCURRENCE_CONTAINER.items()}
        chain, occurrence = [], calc_raw["scope"]["wire"]
        while occurrence is not None:
            chain.append(by_occurrence[occurrence])
            occurrence = OCCURRENCE_PARENT[occurrence]
    outermost = [cid for cid in chain if cid in collapsed]
    return outermost[-1] if outermost else calc_raw["node_id"]


def small_expected_edges(mode, collapsed):
    """{(source, target): sorted [(consumer, input name)]} computed from SMALL in Python."""
    raw = {c["node_id"]: c for c in SMALL["instance_graph"]["graph"]["calcs"]}
    expected: dict[tuple[str, str], list[tuple[str, str]]] = {}
    for consumer in raw.values():
        for inp in consumer["inputs"]:
            producer = raw[inp["edge"]["target"]["calculation"]]
            source = small_representative(producer, mode, collapsed)
            target = small_representative(consumer, mode, collapsed)
            if source != target:
                expected.setdefault((source, target), []).append((consumer["node_id"], inp["name"]))
    return {ends: sorted(bindings) for ends, bindings in expected.items()}


def test_view_every_binding_on_exactly_one_edge_or_none(viewer_page):
    """I2 and I3 across every collapse subset of the small snapshot, both modes.

    I2: every drawn edge lists at least one binding, and each listed binding's representatives
    are the edge's two ends. I3: every binding whose representatives differ is listed on exactly
    one edge; bindings with equal representatives are on none. Both follow from the drawn edge map
    equalling the map computed in Python, with bindings identified by (consumer, input name).
    """
    for mode, ids in (
        ("source", list(SOURCE_CONTAINER)),
        ("occurrence", list(OCCURRENCE_CONTAINER)),
    ):
        for mask in range(1 << len(ids)):
            collapsed = [cid for i, cid in enumerate(ids) if mask & (1 << i)]
            got = run_view(viewer_page, mode, collapsed)
            drawn: dict[tuple[str, str], list[tuple[str, str]]] = {}
            for source, target, bindings in got["edgesById"]:
                assert (source, target) not in drawn, (mode, collapsed, source, target)
                assert bindings, (mode, collapsed, source, target)
                drawn[(source, target)] = sorted(tuple(b) for b in bindings)
            listed = [b for bindings in drawn.values() for b in bindings]
            assert len(listed) == len(set(listed)), (mode, collapsed)
            assert drawn == small_expected_edges(mode, set(collapsed)), (mode, collapsed)
