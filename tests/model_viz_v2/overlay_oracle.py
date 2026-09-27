"""Independent Python oracle for model viewer v2: parts, calcs, ranks, edges and labels.

Reads the raw snapshot JSON only and shares no code or data with the viewer, so a test that
compares the page with this oracle cannot pass by construction (design § Validation Approach).
It may import tests.model_viz.structure_oracle, which is itself independent of the viewer.

Identities (design § Validation Approach): a calc is its node_id; a part is occ:<occurrence_id>;
the synthetic part for calcs whose scope names no occurrence is the literal "unscoped" (D44).
Collapse sets are sets of occurrence ids, plus "unscoped" when that part is closed.
"""

import json
from collections import Counter
from functools import cache

from tests.model_viz import structure_oracle
from tests.model_viz.viewer_harness import FIXTURE

UNSCOPED = "unscoped"


@cache
def _fixture_text() -> str:
    return FIXTURE.read_text(encoding="utf-8")


def load_fixture() -> dict:
    """A fresh parse of the fixture; callers may mutate it."""
    return json.loads(_fixture_text())


def calcs(snap) -> list[dict]:
    return snap["instance_graph"]["graph"]["calcs"]


def occurrences(snap) -> list[dict]:
    return structure_oracle.occurrences(snap)


parent_of = structure_oracle.parent_of
children = structure_oracle.children
descendants = structure_oracle.descendants
depths = structure_oracle.depths


def identity(part: str) -> str:
    """A part's test identity from its occurrence id, or the literal unscoped."""
    return UNSCOPED if part == UNSCOPED else f"occ:{part}"


def calc_id(snap, name: str) -> str:
    found = [c["node_id"] for c in calcs(snap) if c["display_name"] == name]
    assert len(found) == 1, f"expected one calc named {name}, found {len(found)}"
    return found[0]


def occ_of(snap, segment: str) -> str:
    found = [o["occurrence_id"] for o in occurrences(snap) if o["display_segment"] == segment]
    assert len(found) == 1, f"expected one occurrence with segment {segment}, found {len(found)}"
    return found[0]


def roots(snap) -> list[str]:
    return [o["occurrence_id"] for o in occurrences(snap) if o["parent_id"] is None]


def scope_part(snap) -> dict[str, str]:
    """Calc node_id -> the occurrence id its scope.wire names, or unscoped."""
    known = {o["occurrence_id"] for o in occurrences(snap)}
    out = {}
    for calc in calcs(snap):
        scope = calc.get("scope")
        wire = scope.get("wire") if isinstance(scope, dict) else None
        out[calc["node_id"]] = wire if wire in known else UNSCOPED
    return out


def has_unscoped(snap) -> bool:
    return UNSCOPED in scope_part(snap).values()


def all_parts(snap) -> list[str]:
    """Occurrence ids, then unscoped when some calc needs it."""
    parts = [o["occurrence_id"] for o in occurrences(snap)]
    return parts + [UNSCOPED] if has_unscoped(snap) else parts


def part_parent(snap) -> dict[str, str | None]:
    out = dict(parent_of(snap))
    if has_unscoped(snap):
        out[UNSCOPED] = None
    return out


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


def unresolved_bindings(snap) -> int:
    known = {c["node_id"] for c in calcs(snap)}
    return sum(
        1
        for calc in calcs(snap)
        for inp in calc["inputs"]
        if inp["edge"] is not None
        and inp["edge"]["kind"] == "producer"
        and inp["edge"]["target"]["calculation"] not in known
    )


def rank(snap) -> dict[str, int]:
    """Calc node_id -> the length of the longest chain of calcs feeding it."""
    producers: dict[str, set[str]] = {c["node_id"]: set() for c in calcs(snap)}
    for consumer, _name, producer, _output in producer_bindings(snap):
        producers[consumer].add(producer)
    out: dict[str, int] = {}

    def of(node_id, seen=()):
        if node_id in out:
            return out[node_id]
        assert node_id not in seen, f"producer cycle through {node_id}"
        out[node_id] = max((of(p, (*seen, node_id)) + 1 for p in producers[node_id]), default=0)
        return out[node_id]

    for node_id in producers:
        of(node_id)
    return out


def direct_calcs(snap) -> dict[str, list[str]]:
    """Part -> calc node_ids it owns directly, snapshot order."""
    out: dict[str, list[str]] = {p: [] for p in all_parts(snap)}
    for node_id, part in scope_part(snap).items():
        out[part].append(node_id)
    return out


def collapsible(snap) -> set[str]:
    """Parts that own calcs or have children."""
    kids = children(snap)
    owned = direct_calcs(snap)
    return {p for p in all_parts(snap) if owned[p] or kids.get(p)}


def collapse_all(snap) -> set[str]:
    """Every collapsible part below a root; the roots and unscoped stay open."""
    return collapsible(snap) - set(roots(snap)) - {UNSCOPED}


def _part_ancestors(snap) -> dict[str, list[str]]:
    """Part -> its ancestors from the parent outwards."""
    parents = part_parent(snap)
    out = {}
    for part in parents:
        chain = []
        current = parents[part]
        while current is not None:
            chain.append(current)
            current = parents[current]
        out[part] = chain
    return out


def visible_parts(snap, collapsed: set[str]) -> dict[str, str | None]:
    """Part identity -> parent identity for every part none of whose ancestors is closed."""
    parents = part_parent(snap)
    return {
        identity(p): None if parents[p] is None else identity(parents[p])
        for p, above in _part_ancestors(snap).items()
        if not set(above) & collapsed
    }


def visible_calcs(snap, collapsed: set[str]) -> dict[str, str]:
    """Calc node_id -> parent part identity, for every calc no closed part hides."""
    chains = _part_ancestors(snap)
    return {
        node_id: identity(part)
        for node_id, part in scope_part(snap).items()
        if not ({part} | set(chains[part])) & collapsed
    }


def rep(snap, collapsed: set[str]) -> dict[str, str]:
    """Calc node_id -> itself, or the identity of its outermost closed containing part."""
    chains = _part_ancestors(snap)
    out = {}
    for node_id, part in scope_part(snap).items():
        closed = [p for p in [part, *chains[part]] if p in collapsed]
        out[node_id] = identity(closed[-1]) if closed else node_id
    return out


def _edge_bindings(snap, collapsed: set[str]) -> tuple[Counter, int]:
    reps = rep(snap, collapsed)
    pairs: Counter = Counter()
    hidden = 0
    for consumer, _name, producer, _output in producer_bindings(snap):
        source, target = reps[producer], reps[consumer]
        if source == target:
            hidden += 1
        else:
            pairs[(source, target)] += 1
    return pairs, hidden


def edges(snap, collapsed: set[str]) -> list[tuple[str, str]]:
    """Sorted distinct (source identity, target identity) under the visible-edge rule."""
    return sorted(_edge_bindings(snap, collapsed)[0])


def hidden_bindings(snap, collapsed: set[str]) -> int:
    return _edge_bindings(snap, collapsed)[1]


def multi_binding_edges(snap, collapsed: set[str]) -> int:
    return sum(1 for n in _edge_bindings(snap, collapsed)[0].values() if n > 1)


# --- labels -----------------------------------------------------------------------------------


def _group_paths(snap) -> list[str | None]:
    paths = list(
        dict.fromkeys(c["source_file"] for c in calcs(snap) if c["source_file"] is not None)
    )
    if any(c["source_file"] is None for c in calcs(snap)):
        paths.append(None)
    return paths


def _v1_group_labels(paths: list[str | None]) -> dict[str | None, str]:
    """v1's D8 rule: base name without .sysml, the parent directory prefixed on collision."""

    def base(path):
        name = path.split("/")[-1]
        return name[: -len(".sysml")] if name.endswith(".sysml") else name

    real = [p for p in paths if p is not None]
    counts = Counter(base(p) for p in real)
    out: dict[str | None, str] = {}
    for p in real:
        segments = p.split("/")
        out[p] = (
            base(p) if counts[base(p)] == 1 or len(segments) < 2 else f"{segments[-2]}/{base(p)}"
        )
    if None in paths:
        out[None] = "ungrouped"
    return out


def group_tags(snap) -> dict[str | None, str]:
    """Source path -> module tag (D31, A4c)."""
    labels = _v1_group_labels(_group_paths(snap))
    last = {p: label.split("/")[-1] for p, label in labels.items()}
    words = Counter(t.split("_")[0] for t in last.values() if "_" in t)
    common = [w for w, n in words.items() if n * 2 > len(labels)]
    shortened = {}
    for p, t in last.items():
        if common and "_" in t and t.split("_")[0] == common[0]:
            shortened[p] = t[len(common[0]) + 1 :]
        else:
            shortened[p] = t
    uses = Counter(shortened.values())
    return {p: shortened[p] if uses[shortened[p]] == 1 else labels[p] for p in labels}


def calc_tag(snap) -> dict[str, str]:
    tags = group_tags(snap)
    return {c["node_id"]: tags[c["source_file"]] for c in calcs(snap)}


def _plural(n: int, one: str, many: str) -> str:
    return f"1 {one}" if n == 1 else f"{n} {many}"


def part_name(snap, part: str) -> str:
    if part == UNSCOPED:
        return UNSCOPED
    occ = next(o for o in occurrences(snap) if o["occurrence_id"] == part)
    segment = (
        occ["display_segment"] if occ["display_segment"] is not None else "segment not recorded"
    )
    if occ["parent_id"] is None and occ.get("package_display") is not None:
        return f"{occ['package_display']}::{segment}"
    return segment


def hidden_part_count(snap) -> dict[str, int]:
    """Part -> how many parts it hides when closed: every descendant (PD8)."""
    out = {p: len(d) for p, d in descendants(snap).items()}
    if has_unscoped(snap):
        out[UNSCOPED] = 0
    return out


def open_label(snap, part: str) -> str:
    return f"{part_name(snap, part)} · {_plural(len(direct_calcs(snap)[part]), 'calc', 'calcs')}"


def closed_label(snap, part: str) -> str:
    hidden = hidden_part_count(snap)[part]
    name = part_name(snap, part) + (f" ({_plural(hidden, 'part', 'parts')})" if hidden else "")
    return f"{name}\n{_plural(len(direct_calcs(snap)[part]), 'calc', 'calcs')}"


def leaf_label(snap, part: str) -> str:
    return f"{part_name(snap, part)}\n0 calcs"


def expected_part_label(snap, part: str, collapsed: set[str]) -> str:
    """The label a visible part shows under a collapse set."""
    if part not in collapsible(snap):
        return leaf_label(snap, part)
    return closed_label(snap, part) if part in collapsed else open_label(snap, part)


def part_of_identity(ident: str) -> str:
    return UNSCOPED if ident == UNSCOPED else ident.removeprefix("occ:")


# --- find (spec R14, design D39) --------------------------------------------------------------


def part_path(snap, part: str) -> str:
    return UNSCOPED if part == UNSCOPED else structure_oracle.path_of(snap, part)


def part_segment(snap, part: str) -> str:
    return UNSCOPED if part == UNSCOPED else part_path(snap, part).split("/")[-1]


def find_matches(snap, query: str) -> tuple[list[str], list[str]]:
    """(part identities, calc node_ids) of the first non-empty step of R14's order: exact part
    path, exact part segment, exact calc name, then substring over part paths and calc names.
    Case-insensitive; each list in snapshot order."""
    q = query.strip().lower()
    parts = all_parts(snap)
    names = {c["node_id"]: c["display_name"].lower() for c in calcs(snap)}
    steps = [
        ([p for p in parts if part_path(snap, p).lower() == q], []),
        ([p for p in parts if part_segment(snap, p).lower() == q], []),
        ([], [n for n, name in names.items() if name == q]),
        (
            [p for p in parts if q in part_path(snap, p).lower()],
            [n for n, name in names.items() if q in name],
        ),
    ]
    if q == "":
        return [], []
    for found_parts, found_calcs in steps:
        if found_parts or found_calcs:
            return [identity(p) for p in found_parts], found_calcs
    return [], []


# --- reach (spec § Reach, design D37) ---------------------------------------------------------


def _producers_of(snap) -> dict[str, set[str]]:
    out: dict[str, set[str]] = {c["node_id"]: set() for c in calcs(snap)}
    for consumer, _name, producer, _output in producer_bindings(snap):
        out[consumer].add(producer)
    return out


def _consumers_of(snap) -> dict[str, set[str]]:
    out: dict[str, set[str]] = {c["node_id"]: set() for c in calcs(snap)}
    for consumer, _name, producer, _output in producer_bindings(snap):
        out[producer].add(consumer)
    return out


def _closure(edges: dict[str, set[str]], start: str) -> set[str]:
    seen: set[str] = set()
    stack = list(edges[start])
    while stack:
        node = stack.pop()
        if node in seen:
            continue
        seen.add(node)
        stack.extend(edges[node])
    return seen


def upstream(snap, node_id: str) -> set[str]:
    """Every calc that feeds this calc, transitively, over resolved producer bindings."""
    return _closure(_producers_of(snap), node_id)


def downstream(snap, node_id: str) -> set[str]:
    """Every calc this calc feeds, transitively."""
    return _closure(_consumers_of(snap), node_id)


def subtree_calcs(snap, part: str) -> set[str]:
    """Every calc owned by a part or by a part below it (A4a)."""
    owned = direct_calcs(snap)
    below = descendants(snap).get(part, []) if part != UNSCOPED else []
    out = set(owned[part])
    for kid in below:
        out |= set(owned.get(kid, []))
    return out


def selection_calcs(snap, sel: tuple[str, str]) -> set[str]:
    """The selection's calcs S: the selected calc, or a selected part's whole subtree (A4a)."""
    kind, name = sel
    if kind == "calc":
        return {calc_id(snap, name)}
    return subtree_calcs(snap, UNSCOPED if name == UNSCOPED else occ_of(snap, name))


def selection(snap, sel: tuple[str, str]) -> tuple[str, str]:
    """(kind, node_id or part) for a ("calc", name) or ("part", segment) selection."""
    kind, name = sel
    if kind == "calc":
        return ("calc", calc_id(snap, name))
    return ("part", UNSCOPED if name == UNSCOPED else occ_of(snap, name))


def state(snap, name: str) -> set[str]:
    """A named collapse state: all open, only magnet closed, or Collapse all."""
    if name == "open":
        return set()
    if name == "collapse_all":
        return collapse_all(snap)
    return {occ_of(snap, name)}


def selected_identity(snap, collapsed: set[str], sel: tuple[str, str]) -> str:
    """The drawn element standing for the selection: itself, or its outermost closed part."""
    kind, target = selection(snap, sel)
    chains = _part_ancestors(snap)
    if kind == "calc":
        return rep(snap, collapsed)[target]
    closed = [p for p in [target, *chains[target]] if p in collapsed]
    return identity(closed[-1] if closed else target)


def part_ancestors(snap) -> dict[str, list[str]]:
    """Part -> its ancestors from the parent outwards."""
    return _part_ancestors(snap)


def _edge_ends(snap, collapsed: set[str]) -> dict[tuple[str, str], list[tuple[str, str]]]:
    """Drawn edge (source, target) identities -> the (producer, consumer) pairs it carries."""
    reps = rep(snap, collapsed)
    out: dict[tuple[str, str], list[tuple[str, str]]] = {}
    for consumer, _name, producer, _output in producer_bindings(snap):
        source, target = reps[producer], reps[consumer]
        if source == target:
            continue
        out.setdefault((source, target), []).append((producer, consumer))
    return out


def classes(snap, collapsed: set[str], sel: tuple[str, str] | None) -> dict:
    """D37's table, applied top to bottom, first match wins, over the drawn elements.

    Returns {"nodes": identity -> class or None, "edges": (source, target) -> class or None,
    "selected": the identity carrying mv-selected, or None}. Encoded from the raw snapshot only.
    """
    nodes: dict[str, str | None] = {}
    edges: dict[tuple[str, str], str | None] = {}
    for ident in visible_parts(snap, collapsed):
        nodes[ident] = None
    for node_id in visible_calcs(snap, collapsed):
        nodes[node_id] = None
    for pair in _edge_ends(snap, collapsed):
        edges[pair] = None
    if sel is None:
        return {"nodes": nodes, "edges": edges, "selected": None}

    s_calcs = selection_calcs(snap, sel)
    up: set[str] = set()
    down: set[str] = set()
    for node_id in s_calcs:
        up |= upstream(snap, node_id)
        down |= downstream(snap, node_id)

    reps = rep(snap, collapsed)
    hidden: dict[str, set[str]] = {}
    for node_id, where in reps.items():
        if where != node_id:
            hidden.setdefault(where, set()).add(node_id)

    drawn_calcs = visible_calcs(snap, collapsed)
    for ident in nodes:
        if ident in drawn_calcs:
            node_id = ident
            if node_id in up and node_id in down:
                nodes[ident] = "mv-both"
            elif node_id in up:
                nodes[ident] = "mv-upstream"
            elif node_id in down:
                nodes[ident] = "mv-downstream"
            elif node_id in s_calcs:
                nodes[ident] = "mv-member"
            else:
                nodes[ident] = "mv-dim"
            continue
        part = part_of_identity(ident)
        if part not in collapsed:
            continue  # an open part, or a calc-less leaf (A4b): no class
        held = hidden.get(ident, set())
        in_up, in_down, in_s = bool(held & up), bool(held & down), bool(held & s_calcs)
        if in_up and in_down:
            nodes[ident] = "mv-both"
        elif in_s and (in_up or in_down):
            nodes[ident] = "mv-both"
        elif in_up:
            nodes[ident] = "mv-upstream"
        elif in_down:
            nodes[ident] = "mv-downstream"
        elif in_s:
            nodes[ident] = "mv-member"
        else:
            nodes[ident] = "mv-dim"

    up_s, down_s = up | s_calcs, down | s_calcs
    for pair, ends in _edge_ends(snap, collapsed).items():
        lit_up = any(p in up_s and c in up_s for p, c in ends)
        lit_down = any(p in down_s and c in down_s for p, c in ends)
        if lit_up and lit_down:
            edges[pair] = "mv-both"
        elif lit_up:
            edges[pair] = "mv-upstream"
        elif lit_down:
            edges[pair] = "mv-downstream"
        else:
            edges[pair] = "mv-dim"

    chosen = selected_identity(snap, collapsed, sel)
    if nodes.get(chosen) == "mv-dim":  # I32: the selection is never dimmed
        nodes[chosen] = None
    return {"nodes": nodes, "edges": edges, "selected": chosen}


# --- the panel's reach section (design D38) ----------------------------------------------------


def _snapshot_index(snap) -> dict[str, int]:
    """Part -> its position in the snapshot's occurrence list; unscoped comes last."""
    out = {o["occurrence_id"]: i for i, o in enumerate(occurrences(snap))}
    out[UNSCOPED] = len(out)
    return out


def _flow_rank(snap) -> dict[str, float | None]:
    """Part -> the mean rank of every calc in its subtree, or None when it holds none."""
    ranks = rank(snap)
    out: dict[str, float | None] = {}
    for part in all_parts(snap):
        keys = subtree_calcs(snap, part)
        out[part] = sum(ranks[k] for k in keys) / len(keys) if keys else None
    return out


def drawn_part_order(snap) -> list[str]:
    """Parts in drawn tree order: each root, then its children by flow rank, depth first."""
    kids = children(snap)
    flow = _flow_rank(snap)
    index = _snapshot_index(snap)

    def key(part):
        return (flow[part] is None, flow[part] if flow[part] is not None else 0, index[part])

    out: list[str] = []

    def walk(part):
        out.append(part)
        for kid in sorted(kids.get(part, []), key=key):
            walk(kid)

    top = roots(snap) + ([UNSCOPED] if has_unscoped(snap) else [])
    for part in sorted(top, key=key):
        walk(part)
    return out


def reach_lists(snap, sel: tuple[str, str]) -> dict[str, list[dict]]:
    """The panel's reach section (D38): each direction's calcs grouped by the owning part, groups in
    drawn tree order, calcs by rank then snapshot order. Calc names, as the links read."""
    s_calcs = selection_calcs(snap, sel)
    cones = {"upstream": set(), "downstream": set()}
    for node_id in s_calcs:
        cones["upstream"] |= upstream(snap, node_id)
        cones["downstream"] |= downstream(snap, node_id)
    ranks = rank(snap)
    order = {c["node_id"]: i for i, c in enumerate(calcs(snap))}
    names = {c["node_id"]: c["display_name"] for c in calcs(snap)}
    owner = scope_part(snap)
    out = {}
    for name, keys in cones.items():
        groups = []
        for part in drawn_part_order(snap):
            held = sorted((k for k in keys if owner[k] == part), key=lambda k: (ranks[k], order[k]))
            if held:
                groups.append({"path": part_path(snap, part), "calcs": [names[k] for k in held]})
        out[name] = groups
    return out
