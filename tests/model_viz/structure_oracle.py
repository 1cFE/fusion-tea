"""Independent Python oracle for the structure view: parts, parents, depths and calc counts.

Computed straight from the raw snapshot JSON. Shares no code or data with the viewer, so a test
that compares the page with this oracle cannot pass by construction (design § Validation Approach).
The page readers at the bottom read only what the renderer displays, through modelVizApp.cy.
"""

from collections import Counter


def occurrences(snap) -> list[dict]:
    return snap["instance_graph"]["graph"]["occurrences"]


def parent_of(snap) -> dict[str, str | None]:
    return {o["occurrence_id"]: o["parent_id"] for o in occurrences(snap)}


def ancestors(snap) -> dict[str, set[str]]:
    """Occurrence id -> the set of its ancestors' occurrence ids."""
    parents = parent_of(snap)
    out = {}
    for occ in parents:
        found = set()
        current = parents[occ]
        while current is not None:
            found.add(current)
            current = parents[current]
        out[occ] = found
    return out


def descendants(snap) -> dict[str, set[str]]:
    """Occurrence id -> the set of every occurrence below it."""
    out: dict[str, set[str]] = {o["occurrence_id"]: set() for o in occurrences(snap)}
    for occ, above in ancestors(snap).items():
        for ancestor in above:
            out[ancestor].add(occ)
    return out


def depths(snap) -> dict[str, int]:
    return {occ: len(above) for occ, above in ancestors(snap).items()}


def children(snap) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {o["occurrence_id"]: [] for o in occurrences(snap)}
    for o in occurrences(snap):
        if o["parent_id"] is not None:
            out[o["parent_id"]].append(o["occurrence_id"])
    return out


def calc_count(snap) -> dict[str, int]:
    """Calcs owned directly, by scope.wire; 0 for a part that owns none."""
    counts = Counter(c["scope"]["wire"] for c in snap["instance_graph"]["graph"]["calcs"])
    return {o["occurrence_id"]: counts[o["occurrence_id"]] for o in occurrences(snap)}


def expected_parts(snap, collapsed: set[str]) -> list[tuple[str, str | None]]:
    """Sorted (occurrence id, parent occurrence id) for every part visible under a set of collapsed
    occurrence ids: a part is visible when none of its ancestors is collapsed."""
    parents = parent_of(snap)
    return sorted(
        (occ, parents[occ]) for occ, above in ancestors(snap).items() if not above & collapsed
    )


def start_collapsed(snap) -> set[str]:
    """The design's start state (D16): every part with children below the root is collapsed."""
    kids = children(snap)
    return {occ for occ, depth in depths(snap).items() if depth > 0 and kids[occ]}


def displayed_parts(page) -> list[tuple[str, str | None]]:
    """Sorted (occurrence id, displayed parent's occurrence id) read from the drawn part nodes."""
    rows = page.evaluate(
        """() => window.modelVizApp.cy.nodes('[kind="part"]').map(n => [
             n.data('occurrence_id'),
             n.parent().nonempty() ? n.parent().data('occurrence_id') : null,
           ])"""
    )
    return sorted((occ, parent) for occ, parent in rows)


def depth_counts(page) -> dict[int, int]:
    """How many drawn parts sit at each depth, walking node.parent() in cy."""
    found = page.evaluate(
        """() => window.modelVizApp.cy.nodes('[kind="part"]').map(n => {
             let d = 0;
             for (let p = n.parent(); p.nonempty(); p = p.parent()) d++;
             return d;
           })"""
    )
    return dict(Counter(found))


# --- Part panel oracle (Phase 3) ---


def attrs(snap) -> list[dict]:
    return snap["instance_graph"]["graph"]["attrs"]


def path_of(snap, occurrence_id: str) -> str:
    """Containment path from the root, display segments joined by '/' (stellaris/magnet/coil)."""
    by_id = {o["occurrence_id"]: o for o in occurrences(snap)}
    segments = []
    current = occurrence_id
    while current is not None:
        segments.append(by_id[current]["display_segment"])
        current = by_id[current]["parent_id"]
    return "/".join(reversed(segments))


def short_path(snap, occurrence_id: str) -> str:
    """The path below the root ('magnet/coil'); the root is its own segment ('stellaris')."""
    full = path_of(snap, occurrence_id)
    return full.split("/", 1)[1] if "/" in full else full


def _binding(snap, attr) -> dict | None:
    """Where an alias's value comes from (kind, binding text, raw ids); None for a non-alias."""
    if attr["is_alias"] is not True:
        return None
    target = attr["alias_target"] or {}
    graph = snap["instance_graph"]["graph"]
    if target.get("kind") == "producer":
        calc_id, output_id = target["target"]["calculation"], target["target"]["output"]
        calc = next((c for c in graph["calcs"] if c["node_id"] == calc_id), None)
        if calc is not None:
            names = {o["port"]["output"]: o["name"] for o in calc["outputs"]}
            # An undeclared output stays calc-bound, with a warning in place of the name (D20).
            shown = names.get(output_id, f"undeclared output {output_id}")
            return {
                "kind": "calc-bound",
                "text": f"{calc['display_name']}.{shown}",
                "calc_node_id": calc_id,
                "output_id": output_id,
            }
    if target.get("kind") == "node":
        bound = next((a for a in attrs(snap) if a["node_id"] == target["target"]), None)
        if bound is not None:
            return {
                "kind": "attr-bound",
                "text": f"{path_of(snap, bound['scope']['wire'])}.{bound['display_name']}",
                "target_occurrence_id": bound["scope"]["wire"],
                "target_attr_node_id": bound["node_id"],
            }
    return {"kind": "unresolved", "text": None}


def attributes_of(snap, occurrence_id: str) -> list[dict]:
    """The part's attribute rows in snapshot order: node id, name, owner, source, value kind
    (recorded, then the binding, then none), value and binding."""
    rows = []
    for attr in attrs(snap):
        if attr["scope"]["wire"] != occurrence_id:
            continue
        binding = _binding(snap, attr)
        if attr["value"] is not None:
            kind = "recorded"
        else:
            kind = "none" if binding is None else binding["kind"]
        rows.append(
            {
                "node_id": attr["node_id"],
                "name": attr["display_name"],
                "owner": attr["owner_qualified_name"],
                "source": f"{attr['source_file']}:{attr['source_line']}",
                "kind": kind,
                "value": attr["value"],
                "binding": binding,
            }
        )
    return rows


def oracle_type_names(snap) -> dict[str, str]:
    """{short path: type name} for the parts whose type the spec's rule recovers: exactly one
    effective type id, and exactly one declaring owner once the part's own usage owner
    (package_display::display_segment) is set aside."""
    named = {}
    for occ in occurrences(snap):
        type_ids = occ.get("effective_type_ids")
        if not isinstance(type_ids, list) or len(type_ids) != 1:
            continue
        owners = [
            a["owner_qualified_name"]
            for a in attrs(snap)
            if a["scope"]["wire"] == occ["occurrence_id"]
        ]
        if None in owners:
            continue
        usage = (
            f"{occ['package_display']}::{occ['display_segment']}"
            if isinstance(occ.get("package_display"), str)
            else None
        )
        distinct = {owner for owner in owners if owner != usage}
        if len(distinct) == 1:
            named[short_path(snap, occ["occurrence_id"])] = distinct.pop()
    return named
