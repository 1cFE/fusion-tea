"""Synthetic snapshot copies for the v2 tests, written to a temp folder for the file input."""

import copy
import json
from pathlib import Path


def write(tmp_path: Path, name: str, snap: dict) -> Path:
    path = tmp_path / name
    path.write_text(json.dumps(snap), encoding="utf-8")
    return path


def write_bytes(tmp_path: Path, name: str, data: bytes) -> Path:
    path = tmp_path / name
    path.write_bytes(data)
    return path


def _graph(snap: dict) -> dict:
    return snap["instance_graph"]["graph"]


def _root(snap: dict) -> dict:
    roots = [o for o in _graph(snap)["occurrences"] if o["parent_id"] is None]
    assert len(roots) == 1, f"expected one root occurrence, found {len(roots)}"
    return roots[0]


def _wire_below(wire: str, segment: str) -> str:
    return json.dumps([*json.loads(wire), [segment, None]], separators=(",", ":"))


def unscoped(snap: dict) -> tuple[dict, str]:
    """A copy with one root calc re-scoped to an occurrence the snapshot does not hold (D44).
    Returns the copy and the re-scoped calc's node_id."""
    out = copy.deepcopy(snap)
    root = _root(out)
    calc = next(c for c in _graph(out)["calcs"] if c["scope"]["wire"] == root["occurrence_id"])
    calc["scope"]["wire"] = _wire_below(root["occurrence_id"], "nowhere")
    return out, calc["node_id"]


def too_large(snap: dict) -> dict:
    """The fixture plus 400 calc-less occurrences under the root (plan PD2): no calc or binding
    changes, and the full picture no longer fits at the 9 px floor."""
    out = copy.deepcopy(snap)
    root = _root(out)
    for i in range(400):
        segment = f"filler_{i:03d}"
        _graph(out)["occurrences"].append(
            {
                "occurrence_id": _wire_below(root["occurrence_id"], segment),
                "parent_id": root["occurrence_id"],
                "display_segment": segment,
            }
        )
    return out


# --- loading (plan Phase 2, L1 and L2) --------------------------------------------------------


def wrong_version(snap: dict) -> dict:
    out = copy.deepcopy(snap)
    out["instance_graph"]["schema_version"] = "instance-graph/v2"
    return out


def no_version(snap: dict) -> dict:
    out = copy.deepcopy(snap)
    del out["instance_graph"]["schema_version"]
    return out


def non_json_bytes() -> bytes:
    return b"%PDF-1.7\n%\xe2\xe3\xcf\xd3\n1 0 obj\n<< /Type /Catalog >>\nendobj\n"


RENAME_PREFIX = "renamed_"


def renamed(snap: dict) -> dict:
    """Prefix every name the picture, the panel or the datalist shows: calc display_name, output
    name and occurrence display_segment."""
    out = copy.deepcopy(snap)
    for calc in _graph(out)["calcs"]:
        calc["display_name"] = RENAME_PREFIX + calc["display_name"]
        for output in calc["outputs"]:
            output["name"] = RENAME_PREFIX + output["name"]
    for occ in _graph(out)["occurrences"]:
        occ["display_segment"] = RENAME_PREFIX + occ["display_segment"]
    return out


def renamed_names(snap: dict) -> set[str]:
    """Every name renamed() prefixes, as it stands in the given snapshot."""
    names = set()
    for calc in _graph(snap)["calcs"]:
        names.add(calc["display_name"])
        names.update(output["name"] for output in calc["outputs"])
    names.update(occ["display_segment"] for occ in _graph(snap)["occurrences"])
    return names
