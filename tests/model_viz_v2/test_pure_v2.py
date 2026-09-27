"""The pure layer over hand-built input (plan Phase 1 § 2): ranks, flow order, collapsible set,
tags, labels and overlayElements, all through page.evaluate on window.ModelViz.

The packer's room rules and the taxi router went with the band packer (owner ruling 2026-09-15);
the pure layer now produces elements with no geometry at all, and dagre places them."""

import json

import pytest

# A small snapshot: root R holds calcs a (rank 0) and d (rank 2); child part P holds b and c
# (a diamond: a -> b, a -> c, b -> d, c -> d); Q is a calc-less leaf under P; E is a calc-less
# part with a calc-less child, so it is collapsible while its child is not.
ROOT_WIRE = '[["r",null]]'


def wire(*segments: str) -> str:
    return json.dumps([["r", None], *[[s, None] for s in segments]], separators=(",", ":"))


def occurrence(wire_id: str, parent: str | None, segment: str) -> dict:
    return {
        "occurrence_id": wire_id,
        "parent_id": parent,
        "display_segment": segment,
        "package_display": "pkg" if parent is None else None,
        "effective_type_ids": [],
    }


def calc(node_id: str, scope: str, source: str, producers: list[str]) -> dict:
    return {
        "node_id": node_id,
        "display_name": node_id,
        "source_file": source,
        "source_line": 1,
        "scope": {"kind": "occurrence", "wire": scope},
        "calc_expressions": [],
        "doc_comment": "",
        "inputs": [
            {
                "name": f"in_{p}",
                "port": {},
                "metadata": {},
                "edge": {"kind": "producer", "target": {"calculation": p, "output": "out"}},
            }
            for p in producers
        ],
        "outputs": [
            {"name": "out", "declaration": "", "port": {"calculation": node_id, "output": "out"}}
        ],
    }


def small_snapshot() -> dict:
    p, q, e, f = wire("P"), wire("P", "Q"), wire("E"), wire("E", "F")
    return {
        "format": "test",
        "instance_graph": {
            "schema_version": "instance-graph/v3",
            "fingerprint": "0" * 64,
            "graph": {
                "occurrences": [
                    occurrence(ROOT_WIRE, None, "r"),
                    occurrence(p, ROOT_WIRE, "P"),
                    occurrence(q, p, "Q"),
                    occurrence(e, ROOT_WIRE, "E"),
                    occurrence(f, e, "F"),
                ],
                "attrs": [],
                "calcs": [
                    calc("a", ROOT_WIRE, "root-0/analyses/mfe_one.sysml", []),
                    calc("b", p, "root-0/analyses/mfe_two.sysml", ["a"]),
                    calc("c", p, "root-0/analyses/mfe_two.sysml", ["a"]),
                    calc("d", ROOT_WIRE, "root-0/designs/x/plant.sysml", ["b", "c"]),
                ],
                "constraints": [],
            },
        },
        "sources": {"files": []},
    }


BUILD = """(text) => {
  const model = ModelViz.model.buildModel(ModelViz.model.readSnapshot(text));
  const tree = ModelViz.overlay.overlayTree(model);
  const byName = Object.fromEntries(model.calcs.map(c => [c.name, c.key]));
  const bySeg = Object.fromEntries([...tree.containers.values()].map(p => [p.segment, p.id]));
  return { model, tree, byName, bySeg };
}"""


@pytest.fixture(scope="module")
def built(loaded_v2_page):
    """Build the small snapshot's tree and layout once on the loaded page; return a probe."""
    text = json.dumps(small_snapshot())

    def probe(body: str):
        return loaded_v2_page.evaluate(
            f"(text) => {{ const build = {BUILD}; const S = build(text); {body} }}", text
        )

    return probe


def test_ranks_chain_and_diamond(built):
    ranks = built(
        "return Object.fromEntries("
        "Object.entries(S.byName).map(([n, k]) => [n, S.tree.rank.get(k)]));"
    )
    assert ranks == {"a": 0, "b": 1, "c": 1, "d": 2}


def test_flow_order_and_collapsible(built):
    out = built(
        """const root = S.bySeg.r;
           return {
             kids: S.tree.childrenOf.get(root).map(id => S.tree.containers.get(id).segment),
             flow: [S.tree.flowRank.get(S.bySeg.P), S.tree.flowRank.get(S.bySeg.E)],
             collapsible: [...S.tree.collapsible]
               .map(id => S.tree.containers.get(id).segment).sort(),
             collapseAll: [...ModelViz.overlay.collapseAllSet(S.tree)]
               .map(id => S.tree.containers.get(id).segment).sort(),
           };"""
    )
    # P (calcs, mean rank 1) precedes E (no calcs anywhere below it, sorts last).
    assert out["kids"] == ["P", "E"]
    assert out["flow"] == [1, None]
    assert out["collapsible"] == ["E", "P", "r"]
    assert out["collapseAll"] == ["E", "P"]


def test_tags_drop_the_shared_word_and_keep_collisions(built):
    tags = built(
        """return Object.fromEntries(
             S.model.calcs.map(c => [c.name, S.tree.tags.get(c.sourceGroup)]));"""
    )
    # mfe_ leads 2 of 3 groups (a majority), so it is dropped; the design file keeps its label.
    assert tags == {"a": "one", "b": "two", "c": "two", "d": "plant"}
    collide = built(
        """const m = S.model; const groups = new Map(m.groups);
           groups.set('g-x', {gid: 'g-x', path: 'p/mfe_one.sysml', label: 'p/mfe_one',
                              kind: 'analysis'});
           groups.set('g-y', {gid: 'g-y', path: 'q/one.sysml', label: 'q/one',
                              kind: 'analysis'});
           const model2 = {...m, groups};
           const tree2 = ModelViz.overlay.overlayTree(model2);
           return [tree2.tags.get('g-x'), tree2.tags.get('g-y')];"""
    )
    # Both would shorten to "one", so each keeps v1's full label (A4c).
    assert collide == ["p/mfe_one", "q/one"]


def test_labels(built):
    out = built(
        """const P = S.tree.containers.get(S.bySeg.P), E = S.tree.containers.get(S.bySeg.E);
           const F = S.tree.containers.get(S.bySeg.F), r = S.tree.containers.get(S.bySeg.r);
           const o = ModelViz.overlay;
           return [o.openPartLabel(P), o.closedPartLabel(P), o.closedPartLabel(E),
                   o.leafPartLabel(F), o.closedPartLabel(r),
                   o.calcLabel(S.model, S.tree, S.byName.d)];"""
    )
    assert out == [
        "P · 2 calcs",
        "P (1 part)\n2 calcs",
        "E (1 part)\n0 calcs",
        "F\n0 calcs",
        "pkg::r (4 parts)\n2 calcs",  # the root carries its package (v1 D15)
        "d\nplant",
    ]


def test_overlay_elements_parents_first_and_representatives(built):
    out = built(
        """const o = ModelViz.overlay;
           const openState = o.overlayElements(S.model, S.tree, new Set());
           const ids = openState.elements.filter(e => e.group === 'nodes').map(e => e.data.id);
           const parentsFirst = openState.elements.filter(e => e.group === 'nodes').every(e =>
             e.data.parent === undefined || ids.indexOf(e.data.parent) < ids.indexOf(e.data.id));
           const geometry = openState.elements.filter(e => e.position !== undefined ||
             e.data.width !== undefined || e.data.height !== undefined).map(e => e.data.id);
           const closedP = o.overlayElements(S.model, S.tree, new Set([S.bySeg.P]));
           const pNode = closedP.elements.find(e => e.data.id === S.bySeg.P);
           const closedRoot = o.overlayElements(S.model, S.tree, new Set([S.bySeg.r]));
           return {parentsFirst, geometry,
             pClosedLabel: pNode.data.label,
             repOfB: closedP.repOf.get(S.byName.b), repOfA: closedP.repOf.get(S.byName.a),
             repOfBRootClosed: closedRoot.repOf.get(S.byName.b),
             edgesWhenPClosed: closedP.elements.filter(e => e.group === 'edges')
               .map(e => [e.data.source, e.data.target, e.data.bindings.length]).sort(),
             unscopedWhenMissing: (() => { const snap = JSON.parse(text);
               snap.instance_graph.graph.calcs[0].scope.wire = '[["r",null],["nowhere",null]]';
               const S3 = build(JSON.stringify(snap));
               const u = S3.tree.containers.get(o.UNSCOPED_ID);
               if (u === undefined) return null;
               return [u.parent, u.calcCount, S3.tree.containerOf.get(S3.byName.a)]; })()};"""
    )
    assert out["parentsFirst"]
    # Nothing the pure layer emits carries geometry any more; dagre computes all of it.
    assert out["geometry"] == []
    assert out["pClosedLabel"] == "P (1 part)\n2 calcs"
    assert out["repOfB"] == out["repOfB"] and out["repOfB"] != out["repOfA"]
    assert out["repOfBRootClosed"] == out["repOfBRootClosed"]
    # With P closed: a -> P carries two bindings (a->b, a->c) and P -> d carries two (b->d, c->d).
    assert [row[2] for row in out["edgesWhenPClosed"]] == [2, 2]
    assert out["unscopedWhenMissing"] == [None, 1, "p-unscoped"]


def test_find_order(built):
    """D39: exact path, then exact segment, then exact calc name, then substring; case-insensitive;
    the counts split by kind."""
    out = built(
        """const find = (q) => { const f = ModelViz.overlay.find(S.model, S.tree, q);
             return [f.parts.map(p => p.segment), f.calcs.map(c => c.name)]; };
           return { path: find('R/P/Q'), segment: find('p'), calc: find('D'),
                    sub: find('/'), both: find(''), none: find('zzz'), blank: find('  ') };"""
    )
    assert out["path"] == [["Q"], []]
    assert out["segment"] == [["P"], []]
    assert out["calc"] == [[], ["d"]]
    # Containers come in the tree's order (parents first, by depth).
    assert out["sub"] == [["P", "E", "Q", "F"], []]
    assert out["none"] == [[], []] and out["blank"] == [[], []]


def test_find_substring_mixes_kinds(loaded_v2_page):
    """A substring query returns parts and calcs together; an exact calc name wins over a part
    whose path merely contains it."""
    snap = small_snapshot()
    snap["instance_graph"]["graph"]["calcs"].append(
        calc("q", ROOT_WIRE, "root-0/analyses/mfe_one.sysml", [])
    )
    out = loaded_v2_page.evaluate(
        f"(text) => {{ const build = {BUILD}; const S = build(text);"
        """ const find = (q) => { const f = ModelViz.overlay.find(S.model, S.tree, q);
             return [f.parts.map(p => p.segment), f.calcs.map(c => c.name)]; };
           return { exactSegment: find('Q'), sub: find('p/q') }; }""",
        json.dumps(snap),
    )
    # 'Q' is an exact part segment, so the segment step wins over the calc named q.
    assert out["exactSegment"] == [["Q"], []]
    assert out["sub"] == [["Q"], []]


CLASSIFY = """
  const R = ModelViz.reach, o = ModelViz.overlay;
  const run = (X, collapsedSegs, selection) => {
    const collapsed = new Set(collapsedSegs.map(s => X.bySeg[s]));
    const state = o.overlayElements(X.model, X.tree, collapsed);
    const reach = R.buildReach(X.model, X.tree);
    let sel = null;
    if (selection !== null) {
      if (selection.calc !== undefined) {
        const key = X.byName[selection.calc];
        sel = {kind: 'calc', key, representative: state.repOf.get(key)};
      } else {
        const id = X.bySeg[selection.part];
        let rep = id;
        for (const up of [id, ...ModelViz.view.containerAncestors(X.tree, id)])
          if (collapsed.has(up)) rep = up;
        sel = {kind: 'part', partId: id, representative: rep};
      }
    }
    const name = id => X.tree.containers.has(id)
      ? X.tree.containers.get(id).segment : X.model.byKey.get(id).name;
    const map = R.classify(reach, state.elements, state.repOf, sel);
    const out = {};
    for (const e of state.elements) {
      const key = e.group === 'edges'
        ? name(e.data.source) + '>' + name(e.data.target) : name(e.data.id);
      out[key] = map.get(e.data.id) || null;
    }
    return out;
  };"""


def test_classify_rows(built):
    """One case per row of D37's table, on the hand-built model (a -> b, a -> c, b -> d, c -> d)."""
    out = built(
        CLASSIFY
        + """
           const moved = JSON.parse(text);
           for (const c of moved.instance_graph.graph.calcs)
             if (c.node_id === 'd') c.scope.wire = JSON.stringify([['r', null], ['P', null]]);
           const S2 = build(JSON.stringify(moved));
           return {
             openB: run(S, [], {calc: 'b'}),
             closedP: run(S, ['P'], {calc: 'b'}),
             closedPWithD: run(S2, ['P'], {calc: 'b'}),
             closedPSelectD: run(S, ['P'], {calc: 'd'}),
             selectPart: run(S, [], {part: 'P'}),
             closedEmptyE: run(S, ['E'], {part: 'E'}),
             nothing: run(S, [], null),
           };"""
    )
    # Calcs: a feeds b (upstream), d is fed by b (downstream), c is in neither, b is the selection.
    assert out["openB"] == {
        "r": None,
        "P": None,
        "Q": None,  # A4b: a calc-less leaf under a selection stays unclassed
        "E": None,
        "F": None,
        "a": "mv-upstream",
        "b": "mv-member",
        "c": "mv-dim",
        "d": "mv-downstream",
        "a>b": "mv-upstream",
        "a>c": "mv-dim",
        "b>d": "mv-downstream",
        "c>d": "mv-dim",
    }
    # M2: P hides the selection plus one unrelated calc and no cone member.
    assert out["closedP"]["P"] == "mv-member"
    assert out["closedP"]["a"] == "mv-upstream" and out["closedP"]["d"] == "mv-downstream"
    assert out["closedP"]["a>P"] == "mv-upstream" and out["closedP"]["P>d"] == "mv-downstream"
    # With d inside it, P hides the selection and a downstream calc (R9).
    assert out["closedPWithD"]["P"] == "mv-both"
    # Selecting d: P hides b and c, both upstream, and no selection calc.
    assert out["closedPSelectD"]["P"] == "mv-upstream"
    # A4a: selecting P takes both its calcs, so a is upstream and d downstream of the pair.
    assert out["selectPart"]["b"] == "mv-member" and out["selectPart"]["c"] == "mv-member"
    assert out["selectPart"]["a"] == "mv-upstream" and out["selectPart"]["d"] == "mv-downstream"
    # I32: E holds no calc, so every row would dim it; the selected element is never dimmed.
    assert out["closedEmptyE"]["E"] is None
    assert out["closedEmptyE"]["a"] == "mv-dim" and out["closedEmptyE"]["a>b"] == "mv-dim"
    # Nothing selected: every element unclassed.
    assert set(out["nothing"].values()) == {None}


def test_state_styles_never_resize(loaded_v2_page):
    """I27: no state style changes a property Cytoscape counts in a node or a compound box."""
    offenders = loaded_v2_page.evaluate(
        """() => {
             const exact = new Set(['border-width', 'width', 'height', 'padding', 'shape',
               'line-height', 'text-margin-x', 'text-margin-y', 'text-max-width', 'text-wrap',
               'compound-sizing-wrt-labels']);
             const prefixes = ['font-', 'outline-', 'underlay-', 'min-', 'max-', 'padding-'];
             const bad = [];
             for (const rule of window.modelVizApp.cy.style().json()) {
               if (!rule.selector.includes('.mv-')) continue;
               for (const property of Object.keys(rule.style)) {
                 if (exact.has(property) || prefixes.some(p => property.startsWith(p)))
                   bad.push(rule.selector + ' { ' + property + ' }');
               }
             }
             return bad;
           }"""
    )
    assert offenders == []
