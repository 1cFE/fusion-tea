"""Discover a clean native package and pin its reviewed development baseline.

No evaluations or physical calculations occur here. The baseline receipt, headline,
and numerical tolerance classes must exist before this writes a study manifest.
"""
from __future__ import annotations

import argparse
import importlib
import json
import pprint
from pathlib import Path

from scripts.study import common, indicators, manifest

HERE = Path(__file__).resolve().parent
PACKAGE = HERE.parent / "whole_plant_conversion_tea"
MODULE = "exploration.whole_plant_conversion.studies"


def discover(package: Path) -> dict:
    """Read stock pipeline and contract metadata without importing generated code."""
    parsed = indicators.read_pipelines(package)
    graph = indicators.build_graph(parsed)
    contract = indicators.read_model_contract(package)
    entries = {}
    for module in parsed.modules.values():
        if module.module_type != "EntryPoint":
            continue
        for group, port in module.inputs.items():
            values = common.read_json((module.file.parent / port.ref).resolve(), "entry defaults")
            for key in values:
                if key in entries:
                    raise ValueError(f"duplicate entry key: {key}")
                entries[key] = group
    if set(entries) != set(graph.input_keys):
        raise ValueError("entry map differs from native graph")
    return {
        "entry_keys": dict(sorted(entries.items())),
        "constraints": {
            e["constraint_id"]: e["source_local_identity"]
            for e in contract.concrete_entries
        },
        "fingerprints": {
            "indicator_inputs": manifest.indicator_input_fingerprint(package),
            "recorded_provenance": {
                "executable_fingerprint": manifest.read_executable_fingerprint(package),
                "semantic_fingerprint": contract.semantic_fingerprint,
            },
        },
    }


def normalize_receipt(document: dict, case: str | None = None) -> dict:
    """Map the development runner's native result; preserve its actual statuses."""
    if "cases" in document:
        found = [row for row in document["cases"] if row["case"] == case]
        if len(found) != 1:
            raise ValueError("select exactly one named development case with --case")
        document = found[0]
    if document.get("state") == "completed":
        outputs = dict(document["outputs"])
        if "constraint_report" in document:
            outputs["constraint_report"] = document["constraint_report"]
        if "constraint_report" not in outputs:
            outputs["constraint_report"] = {"results": [
                {"constraint_id": key, "status": value}
                for key, value in document["responses"].items() if key != "headline"]}
        return {"status": "evaluated", "fingerprint": document["executable_fingerprint"],
                "effective_inputs": document["inputs"], "outputs": outputs}
    return document


def prepare(receipt_path: Path, phase: str, headline: str | None, tolerances: Path | None, case: str | None = None):
    common.assert_tree_clean(PACKAGE)
    inventory = discover(PACKAGE.resolve())
    receipt = normalize_receipt(common.read_json(receipt_path, "native development receipt"), case)
    if receipt.get("status") != "evaluated":
        raise ValueError("baseline receipt did not evaluate")
    fingerprints = inventory["fingerprints"]
    provenance = fingerprints["recorded_provenance"]
    if receipt["fingerprint"] != provenance["executable_fingerprint"]:
        raise ValueError("receipt belongs to another executable")
    channels = {
        key: key for key, value in receipt["outputs"].items()
        if isinstance(value, (int, float))
    }
    interface = provenance | {
        "entry_keys": inventory["entry_keys"],
        "channels": channels,
        "constraints": inventory["constraints"],
    }
    if phase == "interface":
        (HERE / "interface_data.py").write_text(
            '"""Discovered native metadata; no physical arithmetic."""\n'
            + "INTERFACE = " + pprint.pformat(interface, sort_dicts=True) + "\n"
        )
        return {"phase": phase, "entries": len(interface["entry_keys"]),
                "channels": len(channels), "constraints": len(interface["constraints"])}
    if not headline or tolerances is None:
        raise ValueError("manifest phase requires --headline and --tolerances")
    if headline not in channels:
        raise ValueError("headline is not a published scalar")
    recorded = importlib.import_module(MODULE + ".interface_data").INTERFACE
    if recorded != interface:
        raise ValueError("interface metadata is stale")
    oracle = importlib.import_module(MODULE + ".oracle_entry")
    catalog = sorted(set(oracle.comparison_catalog()))
    if not catalog or not set(catalog) <= set(channels):
        raise ValueError("independent comparison catalog is empty or unpublished")
    bindings = oracle.operand_bindings()
    if set(bindings) != set(interface["constraints"]):
        raise ValueError("oracle must bind every executing constraint")
    for cid, operands in bindings.items():
        for formal, binding in operands.items():
            allowed = channels if binding["kind"] == "channel" else interface["entry_keys"]
            if binding["kind"] not in ("channel", "input") or binding["key"] not in allowed:
                raise ValueError(f"unknown operand binding: {cid}/{formal}")
    point = {key: float(value) for key, value in receipt["effective_inputs"].items()}
    if set(point) != set(interface["entry_keys"]):
        raise ValueError("baseline lacks complete effective inputs")
    by_local = {}
    rows = receipt["outputs"]["constraint_report"]["results"]
    if {row["constraint_id"] for row in rows} != set(interface["constraints"]):
        raise ValueError("receipt does not cover the exact constraint catalog")
    for row in rows:
        local = interface["constraints"][row["constraint_id"]]
        status = row["status"]
        if local in by_local and by_local[local] != status:
            raise ValueError(f"baseline has different verdicts for reused local identity {local}")
        by_local[local] = status
    fingerprints["indicator_inputs"]["files"] = [
        row["path"] for row in fingerprints["indicator_inputs"]["files"]
    ]
    document = {
        "schema_version": manifest.MANIFEST_SCHEMA_VERSION,
        "package": {"name": manifest.read_package_name(PACKAGE),
                    "path": manifest.repo_relative_posix(PACKAGE)},
        "fingerprints": fingerprints,
        "objective_catalog": [{"name": key, "channel": key} for key in catalog],
        "ties": [],
        "baseline": {
            "point": point,
            "headline": {"channel": headline, "value": float(receipt["outputs"][headline])},
            "verdicts": [{"source_local_identity": key, "expected": value}
                         for key, value in sorted(by_local.items())],
        },
        "oracle": {"kind": "python_callable", "module": MODULE + ".oracle_entry",
                   "callable": "evaluate", "sys_path": "."},
        "absolute_tolerances": common.read_json(tolerances, "predeclared tolerance classes"),
    }
    manifest.validate(document)
    common.write_document(document, HERE / "manifest.json")
    return {"phase": phase, "catalog": len(catalog), "headline": document["baseline"]["headline"]}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--phase", choices=("interface", "manifest"), required=True)
    parser.add_argument("--headline")
    parser.add_argument("--tolerances", type=Path)
    parser.add_argument("--case", help="Exact case label when --receipt contains a native cases list")
    args = parser.parse_args()
    print(json.dumps(prepare(args.receipt, args.phase, args.headline, args.tolerances, args.case)))
