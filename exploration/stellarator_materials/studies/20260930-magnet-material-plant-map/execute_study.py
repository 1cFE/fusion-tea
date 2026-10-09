"""Step 9: run every declared case of one material unit through the stock TEAx lifecycle via the package route.

Refuses unless the unit's integration return is a CANDIDATE naming this unit's sealed fingerprints and the record
manifest's pin, the package is git-clean, and the manifest pin recomputes. The proposals are the declared cases'
inputs less the Nb3Sn package constant `magnet__eps_min` (checked equal, oracle_scan.proposal); no two cases carry
the same proposal. `study_route.run_points` (StudyRunner + PreparedListStrategy, one store per unit) evaluates each
once; failed evaluations (domain refusals, design K25) stay in the store as execution_failed with their text.

Exports: results/native/<unit>/ (store and runner artifacts; machine-local), results/cases_<unit>.json (every case:
labels, candidate id, state, refusal text, verdicts by source-local identity, inputs and every published channel;
machine-local), results/constraint_catalog_<unit>.json, results/integration_return_used_<unit>.json and
results/execution-context_<unit>.json.

    .codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" exec python <record>/execute_study.py --unit rebco --integration-return <out-dir>/integration_return.json'
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

import record_common as rc
from oracle_scan import proposal
from exploration.stellarator_materials.studies import study_route as route
from exploration.stellarator_materials.studies.interface_data import INTERFACE
from scripts.study import common, manifest


def execute(unit: str, integration_return: Path, limit: int | None = None, out_root: Path | None = None) -> dict:
    results = Path(out_root or rc.RESULTS)
    integration = json.loads(Path(integration_return).read_text())
    identity = INTERFACE["units"][unit]
    loaded = manifest.load(rc.manifest_path(unit))
    if integration.get("class") != "CANDIDATE":
        raise route.RouteError(f"{unit}: study requires the unit's integration CANDIDATE")
    for key, expected in (("executable_fingerprint", identity["executable_fingerprint"]),
                          ("semantic_fingerprint", identity["semantic_fingerprint"]), ("pin", loaded.pinned_digest)):
        if integration["candidate"].get(key) != expected:
            raise route.RouteError(f"{unit}: integration candidate has a different {key}")
    if integration["candidate"]["manifest"] != manifest.repo_relative_posix(rc.manifest_path(unit)):
        raise route.RouteError(f"{unit}: integration candidate names another manifest")
    package = route.unit_of(unit).package_dir
    common.assert_tree_clean(package)
    manifest.assert_pin_matches(loaded, manifest.indicator_input_fingerprint(package))
    declared = [c for c in rc.load_cases()["cases"] if c["labels"]["material"] == unit][:limit]
    proposals = [proposal(c) for c in declared]
    validate = route.proposal_validator(unit)
    keys = [json.dumps(validate(p), sort_keys=True) for p in proposals]
    if len(set(keys)) != len(keys):
        raise route.RouteError(f"{unit}: two declared cases carry the same proposal")
    study_id = f"{rc.STUDY_ID}-{unit}"
    native = results / "native" / unit
    started = time.time()
    cases, db = route.run_points(unit, study_id, proposals, native)
    elapsed = time.time() - started
    failures = route.failure_texts(db)
    by_key = {k: c for k, c in zip(keys, declared)}
    rows = []
    for case in cases:
        key = json.dumps(dict(case.inputs), sort_keys=True)
        if key not in by_key:
            raise route.RouteError(f"{unit}: stored point {case.candidate_id} differs from every declared case")
        c = by_key.pop(key)
        failure = failures.get(case.candidate_id)
        rows.append({"case_id": c["case_id"], "labels": {k: v for k, v in c["labels"].items() if k != "expected"},
                     "candidate_id": case.candidate_id, "state": case.state,
                     "refusal": (failure or {}).get("cause") if failure else None,
                     "failure": failure,
                     "verdicts": route.short_verdicts(unit, case) if case.state == "completed" else None,
                     "inputs": dict(case.inputs), "outputs": dict(case.outputs),
                     "executable_fingerprint": case.executable_fingerprint, "evidence_digest": case.evidence_digest})
    if by_key:
        raise route.RouteError(f"{unit}: declared cases without a stored point: {[c['case_id'] for c in by_key.values()][:5]}")
    order = {c["case_id"]: i for i, c in enumerate(declared)}
    rows.sort(key=lambda r: order[r["case_id"]])
    rc.write_json({"study_id": study_id, "unit": unit, "store": manifest.repo_relative_posix(db), "cases": rows},
                  results / f"cases_{unit}.json", compact=True)
    rc.write_json(route._catalog_by_constraint_id(package), results / f"constraint_catalog_{unit}.json")
    rc.write_json(integration, results / f"integration_return_used_{unit}.json")
    common.assert_tree_clean(package)
    context = {
        "study_id": study_id, "unit": unit, "command": ["execute_study.py", *sys.argv[1:]],
        "repo_commit": subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip(),
        "integration_return": manifest.repo_relative_posix(integration_return), "integration_class": integration["class"],
        "executable_fingerprint": identity["executable_fingerprint"], "semantic_fingerprint": identity["semantic_fingerprint"],
        "pin": loaded.pinned_digest, "manifest_sha256": loaded.digest, "store": manifest.repo_relative_posix(db),
        "elapsed_seconds": round(elapsed, 1), "declared_cases": len(declared), "stored_cases": len(cases),
        "completed": sum(r["state"] == "completed" for r in rows),
        "execution_failed": sum(r["state"] == "execution_failed" for r in rows),
        "other_states": sorted({r["state"] for r in rows} - {"completed", "execution_failed"}),
        "route": "exploration/stellarator_materials/studies/study_route.py:run_points (stock StudyRunner + PreparedListStrategy)",
        "proposal_mapping": "Nb3Sn magnet__eps_min dropped after checking it equals the package constant (oracle_scan.proposal)",
    }
    rc.write_json(context, results / f"execution-context_{unit}.json")
    print(json.dumps({k: v for k, v in context.items() if k != "command"}))
    if context["other_states"]:
        raise route.RouteError(f"{unit}: unexpected case states {context['other_states']}; evidence retained")
    return context


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--unit", choices=rc.MATERIALS, required=True)
    parser.add_argument("--integration-return", type=Path, required=True)
    parser.add_argument("--limit", type=int, help="test aid: first N cases only (never for the record)")
    parser.add_argument("--out-root", type=Path, help="test aid: write outside results/ (never for the record)")
    args = parser.parse_args()
    execute(args.unit, args.integration_return, args.limit, args.out_root)
