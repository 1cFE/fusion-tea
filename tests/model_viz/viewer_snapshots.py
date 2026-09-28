"""Synthetic snapshots derived from the fixture. Every builder deep-copies its input; the fixture
file is never modified. write() puts the result under a test's tmp_path."""

import copy
import json
from collections import Counter
from pathlib import Path

from edge_oracle import calcs


def write(snap: dict, path: Path) -> Path:
    path.write_text(json.dumps(snap), encoding="utf-8")
    return path


def write_bytes(data: bytes, path: Path) -> Path:
    path.write_bytes(data)
    return path


def wrong_version(snap: dict) -> dict:
    out = copy.deepcopy(snap)
    out["instance_graph"]["schema_version"] = "instance-graph/v2"
    return out


def no_version(snap: dict) -> dict:
    out = copy.deepcopy(snap)
    del out["instance_graph"]["schema_version"]
    return out


def no_calcs_list(snap: dict) -> dict:
    out = copy.deepcopy(snap)
    del out["instance_graph"]["graph"]["calcs"]
    return out


def calc_without_node_id(snap: dict, index: int) -> dict:
    out = copy.deepcopy(snap)
    del calcs(out)[index]["node_id"]
    return out


def null_calc_entry(snap: dict, index: int) -> dict:
    out = copy.deepcopy(snap)
    calcs(out)[index] = None
    return out


def earlier_entry_ends_with_doc(snap: dict) -> tuple[dict, str]:
    """Make an earlier calc_expressions entry also end with the doc comment, on the first calc
    with at least two entries and a doc comment; return that calc's node_id."""
    out = copy.deepcopy(snap)
    calc = next(c for c in calcs(out) if len(c["calc_expressions"]) >= 2 and c["doc_comment"])
    calc["calc_expressions"][0] = calc["calc_expressions"][0] + "\n" + calc["doc_comment"]
    return out, calc["node_id"]


def non_json_bytes() -> bytes:
    return b"%PDF-1.7\n%\xe2\xe3\xcf\xd3\n1 0 obj\n<< /Type /Catalog >>\nendobj\n"


def renamed(snap: dict) -> dict:
    out = copy.deepcopy(snap)
    for calc in calcs(out):
        calc["display_name"] = "renamed_" + calc["display_name"]
    return out


PREFIX = "renamed_"


def renamed_everything(snap: dict) -> dict:
    """Prefix every name either view or panel shows: calc display_name and output name, occurrence
    display_segment and package_display, attribute display_name and owner_qualified_name."""
    out = copy.deepcopy(snap)
    graph = out["instance_graph"]["graph"]
    for calc in graph["calcs"]:
        calc["display_name"] = PREFIX + calc["display_name"]
        for output in calc["outputs"]:
            output["name"] = PREFIX + output["name"]
    for occ in graph["occurrences"]:
        occ["display_segment"] = PREFIX + occ["display_segment"]
        if occ["package_display"] is not None:
            occ["package_display"] = PREFIX + occ["package_display"]
    for attr in graph["attrs"]:
        attr["display_name"] = PREFIX + attr["display_name"]
        # Each qualified-name segment, so the root's own usage owner still reads
        # package_display::display_segment after the rename.
        attr["owner_qualified_name"] = "::".join(
            PREFIX + segment for segment in attr["owner_qualified_name"].split("::")
        )
    return out


def shown_names(snap: dict) -> set[str]:
    """Every name renamed_everything prefixes, as it stands in the given snapshot."""
    graph = snap["instance_graph"]["graph"]
    names = set()
    for calc in graph["calcs"]:
        names.add(calc["display_name"])
        names.update(output["name"] for output in calc["outputs"])
    for occ in graph["occurrences"]:
        names.add(occ["display_segment"])
        if occ["package_display"] is not None:
            names.add(occ["package_display"])
    for attr in graph["attrs"]:
        names.update((attr["display_name"], attr["owner_qualified_name"]))
    return names


def consumers_of(snap: dict, producer_node_id: str) -> list[tuple[str, str]]:
    """(consumer node_id, input name) for every producer input pointing at the calc."""
    return [
        (calc["node_id"], inp["name"])
        for calc in calcs(snap)
        for inp in calc["inputs"]
        if inp["edge"] is not None
        and inp["edge"]["kind"] == "producer"
        and inp["edge"]["target"]["calculation"] == producer_node_id
    ]


def remove_most_consumed_calc(snap: dict) -> tuple[dict, str]:
    """Remove the calc with the most distinct consumer calcs (ties: snapshot order)."""
    counts = Counter()
    for calc in calcs(snap):
        counts[calc["node_id"]] = len({c for c, _ in consumers_of(snap, calc["node_id"])})
    removed = max(calcs(snap), key=lambda c: counts[c["node_id"]])["node_id"]
    assert counts[removed] > 0
    out = copy.deepcopy(snap)
    out["instance_graph"]["graph"]["calcs"] = [c for c in calcs(out) if c["node_id"] != removed]
    return out, removed


def unrenderable_tree(snap: dict) -> tuple[dict, str]:
    """Set the root operator of the first expression_ir tree to '/'; return the calc's node_id."""
    out = copy.deepcopy(snap)
    calc = next(c for c in calcs(out) if c["expression_ir"] is not None)
    assert calc["expression_ir"]["kind"] == "operator"
    calc["expression_ir"]["operator"] = "/"
    return out, calc["node_id"]


def undeclared_output_and_unknown_kind(snap: dict) -> tuple[dict, dict]:
    """Point the first producer input at an output id its producer does not declare, and give
    the first literal input an edge kind outside the four known kinds."""
    out = copy.deepcopy(snap)
    producer_input = None
    unknown_input = None
    for calc in calcs(out):
        for inp in calc["inputs"]:
            edge = inp["edge"]
            if producer_input is None and edge is not None and edge["kind"] == "producer":
                edge["target"]["output"] = "undeclared-output-id"
                producer_input = (calc["node_id"], inp["name"], edge["target"]["calculation"])
            if unknown_input is None and edge is not None and edge["kind"] == "literal":
                inp["edge"] = {"kind": "wire", "value": edge["value"]}
                unknown_input = (calc["node_id"], inp["name"])
    assert producer_input is not None and unknown_input is not None
    return out, {"producer_input": producer_input, "unknown_input": unknown_input}


OVERLAY_SPLIT_FILE = "root-0/analyses/mfe_magnet_cost.sysml"


def overlay(snap: dict) -> tuple[dict, dict[str, str], tuple[str, str]]:
    """Add a parent occurrence under the root with two children sharing one display_segment,
    and split one source file's calcs across the two children.

    Returns the snapshot, the expected node_id -> occurrence_id for every calc, and the two
    sibling occurrence ids.
    """
    out = copy.deepcopy(snap)
    graph = out["instance_graph"]["graph"]
    (root,) = [o for o in graph["occurrences"] if o["parent_id"] is None]
    root_wire = json.loads(root["occurrence_id"])
    parent_id = json.dumps(root_wire + [["overlay-parent", None]])
    twin_a = json.dumps(root_wire + [["overlay-parent", None], ["twin-a", None]])
    twin_b = json.dumps(root_wire + [["overlay-parent", None], ["twin-b", None]])
    graph["occurrences"] += [
        {
            "occurrence_id": parent_id,
            "parent_id": root["occurrence_id"],
            "display_segment": "plant",
        },
        {"occurrence_id": twin_a, "parent_id": parent_id, "display_segment": "twin"},
        {"occurrence_id": twin_b, "parent_id": parent_id, "display_segment": "twin"},
    ]
    split = [c for c in calcs(out) if c["source_file"] == OVERLAY_SPLIT_FILE]
    assert len(split) >= 2
    for i, calc in enumerate(split):
        calc["scope"]["wire"] = twin_a if i < len(split) // 2 + 1 else twin_b
    expected = {c["node_id"]: c["scope"]["wire"] for c in calcs(out)}

    ids = {o["occurrence_id"] for o in graph["occurrences"]}
    assert all(o["parent_id"] is None or o["parent_id"] in ids for o in graph["occurrences"])
    assert twin_a != twin_b
    # WI-057 (2026-09-13): calcs now scope to the parts that own them, so the untouched calcs keep
    # their own occurrences; the overlay asserts only that the split file lands on the two twins.
    assert {twin_a, twin_b} <= set(expected.values())
    assert all(expected[c["node_id"]] in (twin_a, twin_b) for c in calcs(out) if c["source_file"] == OVERLAY_SPLIT_FILE)
    return out, expected, (twin_a, twin_b)


def occurrence_chain(snap: dict, occurrence_id: str) -> list[str]:
    """The occurrence and its ancestors, innermost first."""
    parents = {
        o["occurrence_id"]: o["parent_id"] for o in snap["instance_graph"]["graph"]["occurrences"]
    }
    chain = []
    current = occurrence_id
    while current is not None:
        chain.append(current)
        current = parents[current]
    return chain
