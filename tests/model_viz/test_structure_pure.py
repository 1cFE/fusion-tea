"""The structure view's pure layer called through page.evaluate on hand-built input: the model's
occurrence additions, the shared visibility rule, and the structure layout on edge cases."""

import json
from itertools import combinations

import pytest


def wire(*segments):
    return json.dumps([[s, None] for s in segments])


def occurrence(path, display_segment=None, **extra):
    """An occurrence record for a slash path such as 'r/a/a1'; its parent is the path minus the
    last segment."""
    segments = path.split("/")
    record = {
        "occurrence_id": wire(*segments),
        "parent_id": wire(*segments[:-1]) if len(segments) > 1 else None,
        "display_segment": segments[-1] if display_segment is None else display_segment,
    }
    record.update(extra)
    return record


def calc(node_id, path):
    return {
        "node_id": node_id,
        "display_name": node_id,
        "source_file": "f.sysml",
        "source_line": 1,
        "scope": {"kind": "occurrence", "wire": wire(*path.split("/"))},
        "calc_expressions": [],
        "doc_comment": None,
        "expression_ir": None,
        "inputs": [],
        "outputs": [{"name": "o", "port": {"calculation": node_id, "output": "o"}}],
    }


def snapshot(occurrences, calcs):
    return {
        "instance_graph": {
            "schema_version": "instance-graph/v3",
            "graph": {"occurrences": occurrences, "attrs": [], "calcs": calcs},
        }
    }


# r holds a and b; a holds a1 and a2; a1 holds a1x.
# Listed children-first, as the fixture lists its root last.
NESTED = snapshot(
    [
        occurrence("r/a/a1/a1x"),
        occurrence("r/a/a1"),
        occurrence("r/b", effective_type_ids=["t2", "t9"]),
        occurrence("r/a"),
        occurrence("r/a/a2"),
        occurrence("r", package_display="pkg", effective_type_ids=["t1"]),
    ],
    [
        calc("c_leaf", "r/a/a1/a1x"),
        calc("c_a2", "r/a/a2"),
        calc("c_b", "r/b"),
        calc("c_r", "r"),
        calc("c_r2", "r"),
    ],
)

BUILD_JS = "snap => ModelViz.model.buildModel(ModelViz.model.readSnapshot(JSON.stringify(snap)))"


def test_model_occurrence_additions(viewer_page):
    got = viewer_page.evaluate(
        f"""snap => {{
          const model = ({BUILD_JS})(snap);
          const seg = id => model.occurrences.get(id).segment;
          return [...model.occurrences.values()].map(o => ({{
            seg: o.segment, depth: o.depth, children: o.childIds.map(seg),
            calcs: o.calcKeys.map(k => model.byKey.get(k).name),
            pkg: o.packageDisplay, types: o.typeIds,
          }}));
        }}""",
        NESTED,
    )
    assert got == [
        {"seg": "a1x", "depth": 3, "children": [], "calcs": ["c_leaf"], "pkg": None, "types": None},
        {"seg": "a1", "depth": 2, "children": ["a1x"], "calcs": [], "pkg": None, "types": None},
        {
            "seg": "b",
            "depth": 1,
            "children": [],
            "calcs": ["c_b"],
            "pkg": None,
            "types": ["t2", "t9"],
        },
        {"seg": "a", "depth": 1, "children": ["a1", "a2"], "calcs": [], "pkg": None, "types": None},
        {"seg": "a2", "depth": 2, "children": [], "calcs": ["c_a2"], "pkg": None, "types": None},
        {
            "seg": "r",
            "depth": 0,
            "children": ["b", "a"],
            "calcs": ["c_r", "c_r2"],
            "pkg": "pkg",
            "types": ["t1"],
        },
    ]


VISIBLE_JS = f"""([snap, collapsedSegments]) => {{
  const model = ({BUILD_JS})(snap);
  const tree = ModelViz.view.containerTree(model, "occurrence");
  const idOf = seg => [...tree.containers.values()].find(c => c.label === seg).id;
  const shown = ModelViz.view.visibleContainers(tree, new Set(collapsedSegments.map(idOf)));
  return shown.map(c => c.label);
}}"""


def test_visible_containers_nested(viewer_page):
    def visible(collapsed):
        return viewer_page.evaluate(VISIBLE_JS, [NESTED, collapsed])

    # Parents first by depth, snapshot order within a depth.
    everything = ["r", "b", "a", "a1", "a2", "a1x"]
    assert visible([]) == everything
    # A collapsed middle node stays drawn and hides its descendants only; its sibling branch stays.
    assert visible(["a"]) == ["r", "b", "a"]
    assert visible(["a1"]) == ["r", "b", "a", "a1", "a2"]
    # Nested collapses: the outer one decides, and collapsing a leaf hides nothing.
    assert visible(["a", "a1"]) == ["r", "b", "a"]
    assert visible(["a1x"]) == everything
    assert visible(["r"]) == ["r"]


# --- structure.js: tree, start state, elements -------------------------------------------------

DESIGN_CONSTANTS = {
    "FONT_PX": 12,
    "LINE_H": 16,
    "CHAR_W": 7.2,
    "LINES": 2,
    "PAD": 8,
    "MIN_W": 60,
    "PARENT_PAD": 12,
    "LABEL_BAND": 36,
    "GAP": 20,
    "ROW_WIDTH": 5,
}

TREE_JS = f"""snap => {{
  const tree = ModelViz.structure.structuralTree(({BUILD_JS})(snap));
  return {{
    parts: [...tree.containers.values()].map(p =>
      [p.id, p.parent, p.label, p.path, p.depth, p.childCount, p.memberCount, p.calcCount]),
    start: [...ModelViz.structure.startCollapsed(tree)].sort(),
    collapsible: [...ModelViz.structure.collapsibleParts(tree)].sort(),
    byOccurrence: tree.idByOccurrence.get(snap.instance_graph.graph.occurrences[0].occurrence_id),
  }};
}}"""


def test_constants_match_design(viewer_page):
    assert viewer_page.evaluate("() => ModelViz.structure.constants") == DESIGN_CONSTANTS


def test_structural_tree_nested(viewer_page):
    got = viewer_page.evaluate(TREE_JS, NESTED)
    # Ids follow snapshot order (p0 is a1x); containers are ordered parents first.
    assert got["parts"] == [
        ["p5", None, "pkg::r", "r", 0, 2, 5, 2],
        ["p2", "p5", "b", "r/b", 1, 0, 0, 1],
        ["p3", "p5", "a", "r/a", 1, 2, 3, 0],
        ["p1", "p3", "a1", "r/a/a1", 2, 1, 1, 0],
        ["p4", "p3", "a2", "r/a/a2", 2, 0, 0, 1],
        ["p0", "p1", "a1x", "r/a/a1/a1x", 3, 0, 0, 1],
    ]
    assert got["start"] == ["p1", "p3"]
    assert got["collapsible"] == ["p1", "p3", "p5"]
    assert got["byOccurrence"] == "p0"


def test_structural_tree_missing_names_labelled(viewer_page):
    snap = json.loads(json.dumps(NESTED))
    occs = snap["instance_graph"]["graph"]["occurrences"]
    del occs[5]["package_display"]  # the root: no package, so the label is the segment alone
    occs[3]["display_segment"] = None  # a
    got = viewer_page.evaluate(TREE_JS, snap)
    labels = {part[0]: (part[2], part[3]) for part in got["parts"]}
    assert labels["p5"] == ("r", "r")
    assert labels["p3"] == ("segment not recorded", "r/segment not recorded")
    assert labels["p1"] == ("a1", "r/segment not recorded/a1")


ELEMENTS_JS = f"""([snap, collapsed]) => {{
  const S = ModelViz.structure;
  const tree = S.structuralTree(({BUILD_JS})(snap));
  const set = collapsed === null ? S.startCollapsed(tree) : new Set(collapsed);
  try {{
    return S.structureElements(tree, set);
  }} catch (err) {{
    return {{error: err.message}};
  }}
}}"""


def test_structure_elements_start_state(viewer_page):
    elements = viewer_page.evaluate(ELEMENTS_JS, [NESTED, None])
    by_id = {e["data"]["id"]: e for e in elements}
    assert list(by_id) == ["p5", "p2", "p3"]  # a's descendants are hidden under collapsed a
    assert all(e["group"] == "nodes" and e["data"]["kind"] == "part" for e in elements)
    root, b, a = by_id["p5"], by_id["p2"], by_id["p3"]
    assert root["data"]["label"] == "pkg::r\n2 calcs"
    assert b["data"]["label"] == "b\n1 calc"
    assert a["data"]["label"] == "a (3 parts)\n0 calcs"
    assert (root["data"]["collapsed"], b["data"]["collapsed"], a["data"]["collapsed"]) == (
        False,
        False,
        True,
    )
    assert (
        "parent" not in root["data"] and b["data"]["parent"] == "p5" and a["data"]["parent"] == "p5"
    )
    # The compound carries no size and no position; Cytoscape sizes it from its children (D26).
    assert "width" not in root["data"] and "position" not in root
    for box in (b, a):
        assert {"width", "height"} <= set(box["data"]) and set(box["position"]) == {"x", "y"}
    assert (
        root["data"]["occurrence_id"]
        == NESTED["instance_graph"]["graph"]["occurrences"][5]["occurrence_id"]
    )
    assert (
        a["data"]["path"],
        a["data"]["depth"],
        a["data"]["child_count"],
        a["data"]["member_count"],
        a["data"]["calc_count"],
    ) == ("r/a", 1, 2, 3, 0)


def test_structure_elements_one_part_label(viewer_page):
    elements = viewer_page.evaluate(ELEMENTS_JS, [NESTED, ["p1"]])
    labels = {e["data"]["id"]: e["data"]["label"] for e in elements}
    assert labels["p1"] == "a1 (1 part)\n0 calcs"
    assert "p0" not in labels and "p4" in labels


def test_structure_elements_refuse_a_collapsed_leaf(viewer_page):
    got = viewer_page.evaluate(ELEMENTS_JS, [NESTED, ["p0"]])
    assert got == {"error": "Part p0 has no children, so it cannot be collapsed."}


def test_box_size(viewer_page):
    got = viewer_page.evaluate(
        "labels => labels.map(l => ModelViz.structure.boxSize(l))",
        ["ab\n1 calc", "heat_transport\n2 calcs"],
    )
    c = DESIGN_CONSTANTS
    height = c["LINES"] * c["LINE_H"] + 2 * c["PAD"]
    assert got[0] == {"width": c["MIN_W"], "height": height}
    assert got[1] == {"width": pytest.approx(14 * c["CHAR_W"] + 2 * c["PAD"]), "height": height}


# --- structure.js: layout ------------------------------------------------------------------------

LAYOUT_JS = """spec => {
  const S = ModelViz.structure;
  const elements = spec.map(([id, parent, label]) => {
    const data = {id, kind: 'part', label};
    if (parent !== null) data.parent = parent;
    return {group: 'nodes', data};
  });
  const sizes = new Map(spec.filter(s => s[3]).map(([id, , label]) => [id, S.boxSize(label)]));
  const out = S.structureLayout(elements, sizes);
  return {positions: out.positions, parents: out.parents, sizes: Object.fromEntries(sizes)};
}"""


def blocks(spec, got):
    """Each drawn part's allocated block (x1, y1, x2, y2), rebuilt from the layout's output.

    A box node's block is its box. A compound's block is its box plus the label band above, widened
    to its label."""
    c = DESIGN_CONSTANTS
    out = {}
    for part_id, _parent, label, is_box in spec:
        if is_box:
            pos, size = got["positions"][part_id], got["sizes"][part_id]
            out[part_id] = (
                pos["x"] - size["width"] / 2,
                pos["y"] - size["height"] / 2,
                pos["x"] + size["width"] / 2,
                pos["y"] + size["height"] / 2,
            )
        else:
            box = got["parents"][part_id]
            half = max(box["width"], max(len(line) for line in label.split("\n")) * c["CHAR_W"]) / 2
            out[part_id] = (
                box["x"] - half,
                box["y"] - box["height"] / 2 - c["LABEL_BAND"],
                box["x"] + half,
                box["y"] + box["height"] / 2,
            )
    return out


def overlap(a, b) -> bool:
    return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]


def assert_layout_invariants(spec, got):
    """I16: no two blocks overlap unless one part holds the other, and every child's block lies
    inside its parent's box, inset by the compound padding (so below the parent's label band)."""
    c = DESIGN_CONSTANTS
    eps = 1e-9
    parent = {part_id: p for part_id, p, _label, _box in spec}
    held = {part_id: set() for part_id in parent}
    for part_id in parent:
        up = parent[part_id]
        while up is not None:
            held[part_id].add(up)
            up = parent[up]
    got_blocks = blocks(spec, got)
    for a, b in combinations(got_blocks, 2):
        if a not in held[b] and b not in held[a]:
            assert not overlap(got_blocks[a], got_blocks[b]), (a, b)
    for part_id, up in parent.items():
        if up is None:
            continue
        box = got["parents"][up]
        x1, y1, x2, y2 = got_blocks[part_id]
        assert x1 >= box["x"] - box["width"] / 2 + c["PARENT_PAD"] - eps, part_id
        assert x2 <= box["x"] + box["width"] / 2 - c["PARENT_PAD"] + eps, part_id
        assert y1 >= box["y"] - box["height"] / 2 + c["PARENT_PAD"] - eps, part_id
        assert y2 <= box["y"] + box["height"] / 2 - c["PARENT_PAD"] + eps, part_id
    return got_blocks


def test_layout_twelve_children_and_a_nested_parent(viewer_page):
    spec = [["root", None, "root\n3 calcs", False]]
    for i in range(12):
        if i == 4:
            spec.append(["c4", "root", "nested_parent\n1 calc", False])
            spec += [
                [f"c4{k}", "c4", f"inner_{k}{'y' * (3 * n)}\n0 calcs", True]
                for n, k in enumerate("abc")
            ]
            spec[-2][2] = "inner_b_with_a_long_name\n2 calcs"
        else:
            spec.append([f"c{i}", "root", f"child_{i}{'x' * i}\n{i} calcs", True])
    got = viewer_page.evaluate(LAYOUT_JS, spec)
    assert set(got["positions"]) == {s[0] for s in spec if s[3]}
    assert set(got["parents"]) == {"root", "c4"}
    got_blocks = assert_layout_invariants(spec, got)
    # The root's children are top-aligned, so equal block tops form a row of at most ROW_WIDTH.
    tops = {}
    for part_id, parent, _label, _box in spec:
        if parent == "root":
            tops.setdefault(round(got_blocks[part_id][1], 6), []).append(part_id)
    assert sorted(len(row) for row in tops.values()) == [2, 5, 5]
    assert [row for _top, row in sorted(tops.items())][0] == ["c0", "c1", "c2", "c3", "c4"]


def test_layout_parent_label_wider_than_children(viewer_page):
    """PD2: a 40-character parent over one short child gets a block as wide as its label."""
    long_name = "L" * 40
    spec = [
        ["root", None, "root\n0 calcs", False],
        ["long", "root", f"{long_name}\n0 calcs", False],
        ["abc", "long", "abc\n0 calcs", True],
        ["sib", "root", "sib\n0 calcs", True],
    ]
    got = viewer_page.evaluate(LAYOUT_JS, spec)
    got_blocks = assert_layout_invariants(spec, got)
    long_block = got_blocks["long"]
    assert long_block[2] - long_block[0] >= 40 * DESIGN_CONSTANTS["CHAR_W"]
    assert (
        got["parents"]["long"]["width"] < 40 * DESIGN_CONSTANTS["CHAR_W"]
    )  # the case PD2 exists for
    assert got_blocks["sib"][0] >= long_block[2]


# --- app.js: collapse guards in the structure view -----------------------------------------------

TOGGLE_JS = """id => {
  try { window.modelVizApp.toggleContainer(id); return null; }
  catch (err) { return err.message; }
}"""

FIRST_LEAF_JS = """() => window.modelVizApp.cy.nodes('[kind="part"][child_count=0]').first().id()"""


def test_toggle_container_guards_in_structure_view(fixture_page):
    page = fixture_page
    page.select_option("[data-role=view-select]", "structure")
    before = page.evaluate("() => window.modelVizApp.state.structure")
    leaf = page.evaluate(FIRST_LEAF_JS)
    assert "part has no children" in page.evaluate(TOGGLE_JS, leaf)
    assert page.evaluate(TOGGLE_JS, "g0").startswith("No container g0")
    assert page.evaluate("() => window.modelVizApp.state.structure") == before


# --- structure.js: type name, part detail and part search (Phase 3) ------------------------------


def attr(node_id, path, owner, value=None, **extra):
    """An attribute record scoped to the occurrence at a slash path."""
    record = {
        "node_id": node_id,
        "display_name": node_id,
        "scope": {"kind": "occurrence", "wire": wire(*path.split("/"))},
        "owner_qualified_name": owner,
        "source_file": "parts.sysml",
        "source_line": 7,
        "value": value,
        "is_alias": False,
        "alias_target": None,
    }
    record.update(extra)
    return record


def producer(calc_node_id, output_id):
    return {"kind": "producer", "target": {"calculation": calc_node_id, "output": output_id}}


def with_attrs(snap, attrs):
    out = json.loads(json.dumps(snap))
    out["instance_graph"]["graph"]["attrs"] = attrs
    return out


TYPE_JS = f"""([snap, ids]) => {{
  const model = ({BUILD_JS})(snap);
  return ids.map(id => ModelViz.structure.typeName(model, id));
}}"""

DETAIL_JS = f"""([snap, id]) => ModelViz.structure.partDetail(({BUILD_JS})(snap), id)"""


def type_names(page, snap, paths):
    got = page.evaluate(TYPE_JS, [snap, [wire(*path.split("/")) for path in paths]])
    return dict(zip(paths, got, strict=True))


def part_detail(page, snap, path):
    return page.evaluate(DETAIL_JS, [snap, wire(*path.split("/"))])


def test_type_name_rule(viewer_page):
    snap = with_attrs(
        NESTED,
        [
            # r: one type id, package pkg; its own usage owner pkg::r is set aside (D23).
            attr("r1", "r", "defs::Plant"),
            attr("r2", "r", "pkg::r"),
            attr("r3", "r", "defs::Plant"),
            # b: two type ids, one owner.
            attr("b1", "r/b", "defs::B"),
        ],
    )
    occs = snap["instance_graph"]["graph"]["occurrences"]
    occs[1]["effective_type_ids"] = ["t_a1"]  # a1: one id, two owners
    occs[3]["effective_type_ids"] = ["t_a"]  # a: one id, a null owner
    occs[4]["effective_type_ids"] = ["t_a2"]  # a2: one id, no attributes
    occs[0]["effective_type_ids"] = []  # a1x: an empty closure
    snap["instance_graph"]["graph"]["attrs"] += [
        attr("a1_1", "r/a/a1", "defs::A1"),
        attr("a1_2", "r/a/a1", "defs::Costed"),
        attr("a_1", "r/a", "defs::A"),
        attr("a_2", "r/a", None),
    ]
    got = type_names(viewer_page, snap, ["r", "r/b", "r/a", "r/a/a1", "r/a/a2", "r/a/a1/a1x"])
    assert got["r"] == {"name": "defs::Plant"}
    assert got["r/b"] == {
        "name": None,
        "reason": "the snapshot lists 2 type ids and does not record which is the part's own type",
    }
    assert got["r/a"] == {"name": None, "reason": "an attribute has no declaring owner recorded"}
    assert got["r/a/a1"] == {"name": None, "reason": "attributes come from 2 declaring owners"}
    assert got["r/a/a2"] == {
        "name": None,
        "reason": "no attribute declared by a definition names the type",
    }
    assert got["r/a/a1/a1x"] == {"name": None, "reason": "no type ids recorded"}

    # Without package_display there is no usage owner to set aside, so the root has two owners.
    del snap["instance_graph"]["graph"]["occurrences"][5]["package_display"]
    got = type_names(viewer_page, snap, ["r"])
    assert got["r"] == {"name": None, "reason": "attributes come from 2 declaring owners"}


def test_part_detail_groups_and_header(viewer_page):
    snap = with_attrs(
        NESTED,
        [
            attr("r1", "r", "defs::Plant", 1.5),
            attr("r2", "r", "pkg::r", "text"),
            attr("r3", "r", "defs::Plant", None, source_line=None),
            attr("r4", "r", None, None, source_file=None, display_name=None),
            attr("b1", "r/b", "defs::B", 2),
        ],
    )
    got = part_detail(viewer_page, snap, "r")
    assert (got["name"], got["path"], got["childCount"], got["attrCount"]) == ("r", "r", 2, 4)
    assert got["type"] == {"name": None, "reason": "an attribute has no declaring owner recorded"}
    assert got["calcs"] == [{"key": "c3", "name": "c_r"}, {"key": "c4", "name": "c_r2"}]
    groups = [
        (g["owner"], g["ownPart"], [r["nodeId"] for r in g["rows"]]) for g in got["ownerGroups"]
    ]
    assert groups == [
        ("defs::Plant", False, ["r1", "r3"]),
        ("pkg::r", True, ["r2"]),
        (None, False, ["r4"]),
    ]
    rows = {r["nodeId"]: r for g in got["ownerGroups"] for r in g["rows"]}
    assert (rows["r1"]["kind"], rows["r1"]["value"]) == ("recorded", 1.5)
    assert (rows["r2"]["kind"], rows["r2"]["value"]) == ("recorded", "text")
    assert (rows["r3"]["kind"], rows["r3"]["sourceFile"], rows["r3"]["sourceLine"]) == (
        "none",
        "parts.sysml",
        None,
    )
    assert (rows["r4"]["name"], rows["r4"]["owner"], rows["r4"]["sourceFile"]) == (None, None, None)

    leaf = part_detail(viewer_page, snap, "r/a/a2")
    assert (leaf["path"], leaf["childCount"], leaf["attrCount"], leaf["ownerGroups"]) == (
        "r/a/a2",
        0,
        0,
        [],
    )


def test_part_detail_value_kinds(viewer_page):
    snap = with_attrs(
        NESTED,
        [
            # Declared output o on c_b: calc-bound.
            attr("bound", "r/b", "d", None, is_alias=True, alias_target=producer("c_b", "o")),
            # An alias that also carries a value is recorded, and keeps its binding.
            attr("both", "r/b", "d", 3, is_alias=True, alias_target=producer("c_b", "o")),
            # alias_target on a non-alias is ignored.
            attr("ignored", "r/b", "d", None, is_alias=False, alias_target=producer("c_b", "o")),
            # An output id the calc does not declare: still calc-bound, output name unknown.
            attr("undeclared", "r/b", "d", None, is_alias=True, alias_target=producer("c_b", "zz")),
            attr("gone_calc", "r/b", "d", None, is_alias=True, alias_target=producer("nope", "o")),
            attr("odd", "r/b", "d", None, is_alias=True, alias_target={"kind": "wire", "x": 1}),
            attr("no_target", "r/b", "d", None, is_alias=True, alias_target=None),
            attr(
                "to_attr",
                "r/b",
                "d",
                None,
                is_alias=True,
                alias_target={"kind": "node", "target": "src"},
            ),
            attr(
                "gone_attr",
                "r/b",
                "d",
                None,
                is_alias=True,
                alias_target={"kind": "node", "target": "x"},
            ),
            attr("src", "r/a/a2", "d", 9),
        ],
    )
    got = part_detail(viewer_page, snap, "r/b")
    rows = {r["nodeId"]: r for g in got["ownerGroups"] for r in g["rows"]}
    calc_binding = {
        "kind": "calc",
        "calcKey": "c2",
        "calcName": "c_b",
        "outputId": "o",
        "outputName": "o",
    }
    assert (rows["bound"]["kind"], rows["bound"]["binding"]) == ("calc-bound", calc_binding)
    assert (rows["both"]["kind"], rows["both"]["value"], rows["both"]["binding"]) == (
        "recorded",
        3,
        calc_binding,
    )
    assert (rows["ignored"]["kind"], rows["ignored"]["binding"]) == ("none", None)
    assert rows["undeclared"]["kind"] == "calc-bound"
    assert rows["undeclared"]["binding"] == {**calc_binding, "outputId": "zz", "outputName": None}
    assert (rows["gone_calc"]["kind"], rows["gone_calc"]["binding"]) == (
        "unresolved",
        {
            "kind": "unresolved",
            "reason": "the bound calc is not in this snapshot",
            "raw": "nope output o",
        },
    )
    assert rows["odd"]["binding"] == {
        "kind": "unresolved",
        "reason": "bound, but the target is not recorded",
        "raw": '{"kind":"wire","x":1}',
    }
    assert (rows["no_target"]["kind"], rows["no_target"]["binding"]["raw"]) == ("unresolved", None)
    assert (rows["to_attr"]["kind"], rows["to_attr"]["binding"]) == (
        "attr-bound",
        {
            "kind": "attr",
            "occurrenceId": wire("r", "a", "a2"),
            "attrNodeId": "src",
            "partPath": "r/a/a2",
            "attrName": "src",
        },
    )
    assert rows["gone_attr"]["binding"] == {
        "kind": "unresolved",
        "reason": "the bound attribute is not in this snapshot",
        "raw": "x",
    }


def test_part_detail_unknown_occurrence_throws(viewer_page):
    message = viewer_page.evaluate(
        f"""snap => {{
          try {{ ModelViz.structure.partDetail(({BUILD_JS})(snap), 'nope'); return null; }}
          catch (err) {{ return err.message; }}
        }}""",
        NESTED,
    )
    assert message == "No occurrence nope in the model."


def test_model_attribute_indexes(viewer_page):
    snap = with_attrs(
        NESTED,
        [
            attr("x1", "r/b", "d"),
            attr("stray", "r/zz", "d"),
            attr("x2", "r/b", "d"),
            attr("x3", "r", "d"),
        ],
    )
    got = viewer_page.evaluate(
        f"""([snap, ids]) => {{
          const model = ({BUILD_JS})(snap);
          const occ = id => model.occurrences.get(id).attrIds;
          const [b, r, a] = ids.map(occ);
          return {{b, r, a, unscoped: model.unscopedAttrIds}};
        }}""",
        [snap, [wire("r", "b"), wire("r"), wire("r", "a")]],
    )
    assert got == {"b": ["x1", "x2"], "r": ["x3"], "a": [], "unscoped": ["stray"]}


MATCH_JS = f"""([snap, query]) => {{
  const tree = ModelViz.structure.structuralTree(({BUILD_JS})(snap));
  return ModelViz.structure.matchParts(tree, query).map(p => p.path);
}}"""


def test_match_parts(viewer_page):
    snap = json.loads(json.dumps(NESTED))
    snap["instance_graph"]["graph"]["occurrences"].append(occurrence("r/b/a"))

    def match(query):
        return viewer_page.evaluate(MATCH_JS, [snap, query])

    # An exact path beats an exact segment: "r/a" is a path, and "a" is also r/b/a's segment.
    assert match("R/A") == ["r/a"]
    # An exact segment beats a substring: "a" is the segment of r/a and r/b/a, and inside "a1".
    assert match("a") == ["r/a", "r/b/a"]
    # Otherwise a substring of the path, in tree order.
    assert match("/A1") == ["r/a/a1", "r/a/a1/a1x"]
    assert match("nothing") == []
