"""Record-local exact-full-numeric-map export; native StudyRunner unchanged."""
from __future__ import annotations

import argparse
import csv
import json
import hashlib
from pathlib import Path

from scripts.study import common, manifest
from exploration.aries_integrated.studies import study_route as route


def numeric_key(point):
    normalized = route.validate_proposal(point)
    if normalized is None:
        raise route.RouteError("export requires the complete finite numeric map")
    return tuple(sorted(normalized.items()))


def persistent_hashes(root):
    return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in root.rglob('*') if p.is_file() and 'pkg_link' not in p.parts
            and not p.name.endswith(('-wal', '-shm'))}


def execute(record: Path, integration_return: Path):
    record = record.resolve()
    integration = common.read_json(integration_return, "integration return")
    if integration.get("class") != "CANDIDATE" or integration.get("exit_code") != 0:
        raise route.RouteError("study requires a successful native integration CANDIDATE")
    candidate = integration["candidate"]
    loaded = manifest.load(route.MANIFEST_PATH)
    identity = route.interface()
    for key, expected in (("executable_fingerprint", identity["executable_fingerprint"]),
                          ("semantic_fingerprint", identity["semantic_fingerprint"]),
                          ("pin", loaded.pinned_digest)):
        if candidate.get(key) != expected:
            raise route.RouteError(f"integration candidate has a different {key}")
    common.assert_tree_clean(route.PACKAGE_DIR)
    manifest.assert_pin_matches(loaded, manifest.indicator_input_fingerprint(route.PACKAGE_DIR))
    proposals = common.read_json(record / "proposed-points.json", "declared complete points")["cases"]
    labels = {numeric_key(row["point"]): row["case"] for row in proposals}
    if len(labels) != len(proposals):
        raise route.RouteError("declared points are duplicated")
    results = record / "results"
    if results.exists():
        raise route.RouteError("results already exist; preserve evidence and explicitly plan any resume")
    results.mkdir()
    common.write_document(integration, results / "integration_return_used.json")
    common.write_document(loaded.data, results / "manifest_used.json")
    common.write_document(route._catalog_by_constraint_id(route.PACKAGE_DIR),
                          results / "constraint_catalog.json")
    cases, db = route.run_points(record.name, [row["point"] for row in proposals], results / "native")
    stored_hashes = persistent_hashes(results / "native")
    rows = []
    for case in cases:
        key = numeric_key(dict(case.inputs))
        if key not in labels:
            raise route.RouteError("stored point differs from every complete declared proposal")
        rows.append({"case": labels[key], "candidate_id": case.candidate_id,
                     "state": case.state, "inputs": dict(case.inputs),
                     "outputs": dict(case.outputs), "verdicts": dict(case.verdicts),
                     "executable_fingerprint": case.executable_fingerprint,
                     "evidence_digest": case.evidence_digest,
                     "headline": case.headline, "disposition": case.disposition,
                     "full_numeric_map_equal": True})
    common.write_document({"store": manifest.repo_relative_posix(db), "cases": rows}, results / "cases.json")
    columns = ["case", "candidate_id", "state", *sorted(identity["channels"]), *sorted(identity["constraints"])]
    with (results / "cases.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=columns)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row[key] for key in ("case", "candidate_id", "state")} |
                            {key: row["outputs"].get(channel) for key, channel in identity["channels"].items()} |
                            row["verdicts"])
    after_hashes = persistent_hashes(results / "native")
    if after_hashes != stored_hashes:
        raise route.RouteError("persistent native evidence changed during export")
    common.write_document({"persistent_sha256": stored_hashes, "unchanged_after_export": True,
                           "matching": "exact complete numeric map equality", "evaluations_during_export": 0},
                          results / "export-proof.json")
    common.assert_tree_clean(route.PACKAGE_DIR)
    if len(rows) != len(proposals) or any(row["state"] != "completed" for row in rows):
        raise route.RouteError("not every declared point completed; stored and exported evidence retained")
    print(json.dumps({"cases": len(rows), "completed": sum(row["state"] == "completed" for row in rows),
                      "store": str(db), "results": str(results)}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--record", type=Path, required=True)
    parser.add_argument("--integration-return", type=Path, required=True)
    args = parser.parse_args()
    execute(args.record, args.integration_return)
