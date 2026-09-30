"""Step 9: run every declared case through the stock TEAx lifecycle via the package route; export the evidence.

Refuses to run unless the package is git-clean, the manifest pin recomputes, and the reviewed interface identity
matches the sealed contracts. Records the integration seam's return class beside the run: a CANDIDATE is the
expected lineage evidence; running without one is a disclosed deviation that must be requested explicitly.

    .codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" exec python <record>/execute_study.py --integration-return <dir>/integration_return.json [--without-candidate]'
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

from scripts.study import common, manifest
from exploration.magnet_materials.studies import study_route as route

RECORD = Path(__file__).resolve().parent
STUDY_ID = RECORD.name
CASES = RECORD.parent / "cases.json"


def execute(integration_return: Path, without_candidate: bool):
    integration = common.read_json(integration_return, "integration return")
    if integration.get("class") != "CANDIDATE" and not without_candidate:
        raise route.RouteError("study requires a successful native integration CANDIDATE (or an explicit --without-candidate)")
    loaded = manifest.load(RECORD / "manifest.json")
    identity = route.interface()
    contracts = route.PACKAGE_DIR / "contracts"
    if manifest.read_executable_fingerprint(route.PACKAGE_DIR) != identity["executable_fingerprint"]:
        raise route.RouteError("sealed executable fingerprint differs from the reviewed interface")
    if manifest.read_semantic_fingerprint(route.PACKAGE_DIR) != identity["semantic_fingerprint"]:
        raise route.RouteError("model contract semantic fingerprint differs from the reviewed interface")
    if integration.get("class") == "CANDIDATE":
        for key, expected in (("executable_fingerprint", identity["executable_fingerprint"]),
                              ("semantic_fingerprint", identity["semantic_fingerprint"]),
                              ("pin", loaded.pinned_digest)):
            if integration["candidate"].get(key) != expected:
                raise route.RouteError(f"integration candidate has a different {key}")
    common.assert_tree_clean(route.PACKAGE_DIR)
    manifest.assert_pin_matches(loaded, manifest.indicator_input_fingerprint(route.PACKAGE_DIR))
    raw = CASES.read_bytes()
    declared = json.loads(raw)["cases"]
    results = RECORD / "results"
    native = results / "native"
    if native.exists() or (results / "cases.json").exists():
        raise route.RouteError("native results already exist; preserve evidence and explicitly plan any resume")
    points = [route.case_point(c) for c in declared]
    # Several declared cases carry byte-identical entry maps (a variant whose value equals the pairing's own
    # reference, or an economics-only variant whose variant offer equals the re-evaluated reference offer). The
    # lifecycle evaluates each distinct point once; every declared case keeps its own row and names its aliases.
    labels: dict[str, list[str]] = {}
    unique: list[dict] = []
    for c, p in zip(declared, points):
        key = json.dumps(p, sort_keys=True)
        if key not in labels:
            labels[key] = []
            unique.append(c)
        labels[key].append(c["case_id"])
    aliases = {ids[0]: ids[1:] for ids in labels.values() if len(ids) > 1}
    common.write_document({"unique_points": len(unique), "declared_cases": len(declared),
                           "alias_groups": len(aliases), "aliased_cases": sum(len(v) for v in aliases.values()),
                           "aliases": aliases}, results / "case_aliases.json")
    common.write_document({"path": manifest.repo_relative_posix(CASES), "sha256": hashlib.sha256(raw).hexdigest(),
                           "n_cases": len(declared), "header": json.loads(raw)["header"]}, results / "cases_declared.json")
    common.write_document(integration, results / "integration_return_used.json")
    common.write_document(loaded.data, results / "manifest_used.json")
    common.write_document(route._catalog_by_constraint_id(route.PACKAGE_DIR), results / "constraint_catalog.json")
    started = time.time()
    cases, db = route.run_cases(STUDY_ID, unique, native)
    elapsed = time.time() - started
    by_id = {c["case_id"]: c for c in declared}
    rows = []
    seen = set()
    for case in cases:
        key = json.dumps(dict(case.inputs), sort_keys=True)
        if key not in labels:
            raise route.RouteError("stored point differs from every declared case")
        ids = labels[key]
        for cid in ids:
            rows.append({"case_id": cid, "labels": by_id[cid]["labels"], "candidate_id": case.candidate_id,
                         "aliases": [other for other in ids if other != cid],
                         "state": case.state, "inputs": dict(case.inputs), "outputs": dict(case.outputs),
                         "verdicts": dict(case.verdicts), "executable_fingerprint": case.executable_fingerprint,
                         "evidence_digest": case.evidence_digest, "headline": case.headline,
                         "disposition": case.disposition})
            seen.add(cid)
    if seen != set(by_id):
        raise route.RouteError(f"declared cases without a stored point: {sorted(set(by_id) - seen)[:5]}")
    order = {c["case_id"]: i for i, c in enumerate(declared)}
    rows.sort(key=lambda r: order[r["case_id"]])
    common.write_document({"study_id": STUDY_ID, "store": manifest.repo_relative_posix(db), "cases": rows},
                          results / "cases.json")
    channels = identity["channels"]
    constraints = identity["constraint_ids"]
    label_keys = ["anchor", "B_peak", "point_class", "pairing", "rule_family", "variant", "offer_kind", "refrigerator_kind"]
    columns = ["case_id", *label_keys, "candidate_id", "state", *sorted(channels), *sorted(constraints)]
    with (results / "cases.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=columns)
        writer.writeheader()
        for row in rows:
            writer.writerow({"case_id": row["case_id"], "candidate_id": row["candidate_id"], "state": row["state"]}
                            | {k: row["labels"][k] for k in label_keys}
                            | {name: row["outputs"].get(channel) for name, channel in channels.items()}
                            | {name: row["verdicts"].get(cid) for name, cid in constraints.items()})
    common.assert_tree_clean(route.PACKAGE_DIR)
    context = {
        "study_id": STUDY_ID, "command": ["execute_study.py", *sys.argv[1:]],
        "repo_commit": subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip(),
        "integration_class": integration.get("class"), "integration_return": manifest.repo_relative_posix(integration_return),
        "without_candidate": without_candidate,
        "executable_fingerprint": identity["executable_fingerprint"], "semantic_fingerprint": identity["semantic_fingerprint"],
        "pin": loaded.pinned_digest, "store": manifest.repo_relative_posix(db), "elapsed_seconds": round(elapsed, 1),
        "cases": len(rows), "unique_points": len(unique), "stored_cases": len(cases),
        "completed": sum(r["state"] == "completed" for r in rows),
        "route": "exploration/magnet_materials/studies/study_route.py:run_cases (stock StudyRunner + PreparedListStrategy)",
    }
    common.write_document(context, results / "execution-context.json")
    print(json.dumps({k: v for k, v in context.items() if k != "command"}))
    if len(rows) != len(declared) or any(r["state"] != "completed" for r in rows):
        raise route.RouteError("not every declared case completed; stored and exported evidence retained")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--integration-return", type=Path, required=True)
    parser.add_argument("--without-candidate", action="store_true",
                        help="run although the seam returned no CANDIDATE; recorded in execution-context.json")
    args = parser.parse_args()
    execute(args.integration_return, args.without_candidate)
