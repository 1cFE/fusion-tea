"""Step 15: resolve every snapshot value at this moment and write snapshot.json (record-template appendix shape).

Three arms, one per unit. Everything that differs between arms (package, fingerprints, manifest, indicators,
integration, store, verification, artifacts) is arm-scoped; stores are named once in stores[] and referenced by id.

    .codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" exec python <record>/build_snapshot.py'
"""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

import record_common as rc
from exploration.stellarator_materials.studies.interface_data import INTERFACE
from scripts.study import common
from scripts.study import manifest as manifest_mod
from scripts.study import verify

ROOT = rc.REPO
EV = ROOT / "work/orchestration/goals/magnet-material-comparison/evidence"
rel = manifest_mod.repo_relative_posix
sha = manifest_mod.sha256_file
MACHINE_LOCAL = ("results/native/", "results/_work/", "results/oracle_scan.json", "results/cases_rebco.json",
                 "results/cases_nb3sn.json", "results/oracle_verification.json")
RECORD_SCRIPTS = ("record_common.py", "declare_axes.py", "write_manifests.py", "run_indicators.py", "run_baseline.py",
                  "route_entry.py", "oracle_entry.py", "oracle_reference.py", "oracle_rebco.py", "oracle_nb3sn.py",
                  "statuses.py", "oracle_scan.py", "diagnose_tolerance.py", "execute_study.py", "verify_all.py",
                  "policy_acceptance.py", "summarize.py", "breakeven_verify.py", "build_snapshot.py")


def flatten(block, prefix=""):
    names = []
    for key, value in block.items():
        name = f"{prefix}{key}"
        if isinstance(value, dict) and "digest" not in value:
            names += flatten(value, name + ".")
        else:
            names.append(name)
    return names


def store_entry(store_id: str, path: Path) -> dict:
    from simkit.study.store import StudyStore

    store = StudyStore(path)
    try:
        digest, fields = verify.compatibility_digest(store)
        rows = store.conn.execute("SELECT state, COUNT(*) FROM cases GROUP BY state").fetchall()
    finally:
        store.close()
    return {"store_id": store_id, "path": rel(path), "sha256": sha(path), "bytes": path.stat().st_size,
            "compatibility_digest": digest, "compatibility_tuple": fields, "cases_by_state": dict(rows)}


def aggregate(files) -> dict:
    files = sorted(files)
    return {"sha256": hashlib.sha256("".join(f"{f.name} {sha(f)}\n" for f in files).encode()).hexdigest(),
            "recipe": "sha256 over '<name> <sha256>\\n' lines sorted by name", "files": len(files),
            "bytes": sum(f.stat().st_size for f in files)}


def main():
    out = rc.RECORD / "snapshot.json"
    if out.exists():
        raise SystemExit("snapshot.json exists; a changed snapshot is a different study")
    repo_commit = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True,
                                 cwd=ROOT).stdout.strip()
    full = json.loads((rc.RESULTS / "verification_summary.json").read_text())
    stores = []
    arms = []
    oracle_digest = common.tool_source_digest(tuple(
        ["exploration/stellarator_materials/oracle_glue.py", "exploration/stellarator_materials/oracle-reuse.json",
         "exploration/magnet_materials/oracle.py", "exploration/stellarator_e2e/verify_stellaris.py",
         "exploration/stellarator_e2e/studies/oracle_entry.py"]
        + [rel(rc.RECORD / p) for p in ("oracle_entry.py", "oracle_reference.py", "oracle_rebco.py", "oracle_nb3sn.py")]))
    for unit in rc.UNITS:
        manifest = json.loads(rc.manifest_path(unit).read_text())
        package = ROOT / manifest["package"]["path"]
        indicators = json.loads((rc.RECORD / f"indicators_{unit}.json").read_text())
        integration_path = EV / f"integration-r3-{unit}" / "integration_return.json"
        integration = json.loads(integration_path.read_text())
        names = flatten(manifest["fingerprints"])
        fingerprints = {
            "indicator_inputs": indicators["package"]["indicator_input_fingerprint"],
            "recorded_provenance.executable_fingerprint": manifest["fingerprints"]["recorded_provenance"]["executable_fingerprint"],
            "recorded_provenance.semantic_fingerprint": manifest["fingerprints"]["recorded_provenance"]["semantic_fingerprint"],
        }
        assert set(names) == set(fingerprints)
        if unit == "reference":
            store_path = rc.RESULTS / "_work" / "stellarator-materials-reference-baseline-r3.db"
        else:
            store_path = rc.NATIVE / unit / f"{rc.STUDY_ID}-{unit}.db"
        store_id = f"store-{unit}"
        stores.append(store_entry(store_id, store_path))
        if unit != "reference":
            stores.append(store_entry(f"store-{unit}-baseline",
                                      rc.RESULTS / "_work" / f"stellarator-materials-{unit}-baseline-r3.db"))
        entry_models = {}
        for key, model in INTERFACE["units"][unit]["entry_keys"].items():
            entry_models.setdefault(model, []).append(key)
        artifacts = []
        for path in sorted(rc.RESULTS.iterdir()):
            if path.is_file() and (unit in path.name or unit == "reference" and not any(u in path.name for u in rc.MATERIALS)):
                entry = {"path": f"results/{path.name}", "sha256": sha(path), "bytes": path.stat().st_size}
                if any(entry["path"] == m for m in MACHINE_LOCAL):
                    entry["in_git"] = False
                artifacts.append(entry)
        if unit != "reference":
            art = rc.NATIVE / unit / "artifacts"
            artifacts.append({"path": f"results/native/{unit}/artifacts/", **aggregate(art.glob("*.json")), "in_git": False})
        stock = rc.RESULTS / f"verify_stock_{unit}.json"
        stock_doc = json.loads(stock.read_text()) if stock.exists() else None
        arm = {
            "arm_id": rc.ARMS[unit], "unit": unit, "store_id": store_id,
            "package": {"path": manifest["package"]["path"], "package_name": manifest["package"]["name"],
                        "repo_commit": repo_commit, "git_clean": common.git_status_porcelain(package) == ""},
            "fingerprints": fingerprints,
            "manifest": {
                "path": rel(rc.manifest_path(unit)), "schema_version": manifest["schema_version"],
                "digest": sha(rc.manifest_path(unit)),
                "stock_manifest": ({"path": f"exploration/stellarator_materials/studies/{unit}/manifest.json",
                                    "digest": sha(rc.PACKAGE_STUDIES / unit / "manifest.json"),
                                    "differs_in": ["oracle (record-local per-unit binding)"]
                                    + (["absolute_tolerances (r5a, 4 channels)"] if unit != "reference" else [])}
                                   if unit != "nb3sn" else {"path": None, "note": "no stock Nb3Sn manifest exists "
                                                            "(implementation notes deviation 4); written by write_manifests.py"}),
                "content_used": {"fingerprint_names": names, "ties": manifest["ties"],
                                 "objective_catalog": manifest["objective_catalog"],
                                 "baseline": {"point_keys": len(manifest["baseline"]["point"]),
                                              "point_sha256": hashlib.sha256(json.dumps(manifest["baseline"]["point"],
                                                                                        sort_keys=True).encode()).hexdigest(),
                                              "headline": manifest["baseline"]["headline"],
                                              "verdicts": manifest["baseline"]["verdicts"]},
                                 "absolute_tolerances": manifest.get("absolute_tolerances", []),
                                 "oracle": {**manifest["oracle"], "source_digest": oracle_digest}},
            },
            "effective_executable_fingerprint": {"value": fingerprints["recorded_provenance.executable_fingerprint"],
                                                 "inputs": None, "no_adapter": True,
                                                 "note": "no adapter exists; the sealed fingerprint is the identity"},
            "entry_models": {m: sorted(k) for m, k in sorted(entry_models.items())},
            "strategy": next(e for e in stores if e["store_id"] == store_id)["compatibility_tuple"].get("strategy_identity"),
            "window": ({"bounds": {"points": "the manifest's pinned baseline point only (reference instance is pinned)"},
                        "provenance": "engineered"} if unit == "reference" else
                       {"bounds": {"cells": {"geometry": ["anchored", "helias", "arm"], "f_ren": [1.0, 1.4, 1.8]},
                                   "sizes_R_a": [[10.0, 1.0], [11.0, 1.1], [12.7, 1.3], [15.0, 1.5], [18.0, 1.8],
                                                 [22.0, 1.8], [22.0, 2.2]],
                                   "B_peak_target_T": [10, 11, 12, 13] if unit == "nb3sn" else [10, 11, 12, 18, 20, 22, 24.9],
                                   "T_i0_ladder_keV": [11, 13, 14.63, 16, 18],
                                   "generating_rule": f"exploration/stellarator_materials/studies/declare_cases.py over "
                                                      f"offer_policy.py; cases.json sha256 {rc.CASES_SHA256}",
                                   "declared_cases": sum(1 for c in json.loads((rc.RESULTS / f'cases_{unit}.json').read_text())['cases'])},
                        "provenance": "engineered"}),
            "verification": {
                "command": ["verify_all.py"], "tool_revision": sha(rc.RECORD / "verify_all.py"),
                "sampling_scheme": "every stored case (no sampling)" if unit != "reference" else "the one stored point",
                "tolerance": full["tolerance"]["rule"],
                "summary_sha256": sha(rc.RESULTS / "verification_summary.json"),
                "outcome": (full["units"].get(unit) or {}).get("disagreements") == [] if unit != "reference" else None,
                "stock_verify": ({"path": rel(stock), "sha256": sha(stock), "command": stock_doc["command"],
                                  "tool_revision": stock_doc["tool"]["source_digest"]["digest"],
                                  "sampling": stock_doc["stores"][0]["sampling"],
                                  "worst_channel_rel_dev": stock_doc["worst_channel_rel_dev"],
                                  "outcome": stock_doc["outcome"]} if stock_doc else None),
            },
            "glue_ledger": [], "glue_ledger_none": True,
            "proposal_mapping": (["magnet__eps_min dropped from every case proposal after checking it equals the package "
                                  "constant -0.01 (finding #4)"] if unit == "nb3sn" else []),
            "indicators": {"path": f"indicators_{unit}.json", "sha256": sha(rc.RECORD / f"indicators_{unit}.json"),
                           "output_schema_version": indicators["schema_version"],
                           "axis_declaration": indicators["axis_declaration"],
                           "shim": {"path": "run_indicators.py", "sha256": sha(rc.RECORD / "run_indicators.py"),
                                    "aliases": json.loads((rc.RECORD / f"indicators_{unit}.aliases.json").read_text())["aliases"]}},
            "integration": {"return": rel(integration_path), "sha256": sha(integration_path), "class": integration["class"],
                            "candidate": integration["candidate"], "audited_work": integration["request"]["audited_work"],
                            "gates": [{"gate": g["gate"], "status": g["status"]} for g in integration["gates"]],
                            "expected_teax_revision": integration["request"]["expected"]["teax_revision"]},
            "artifacts": artifacts,
        }
        if unit == "nb3sn":
            first = EV / "integration-r3-nb3sn/blocker-run/integration_return.json"
            fd = json.loads(first.read_text())
            arm["integration"]["first_attempt"] = {"return": rel(first), "sha256": sha(first), "class": fd["class"],
                                                   "blocker": {k: fd["blocker"][k] for k in ("gate", "scope", "mode", "condition")},
                                                   "audited_work": fd["request"]["audited_work"],
                                                   "resolved_by": "contract r5a section 9 (97fabad31): 1e-9 relative or "
                                                                  "1e-9 absolute per unit; manifest absolute_tolerances"}
        if unit == "rebco":
            first = EV / "integration-r3-rebco/first-run/integration_return.json"
            arm["integration"]["first_run"] = {"return": rel(first), "sha256": sha(first),
                                               "class": json.loads(first.read_text())["class"],
                                               "superseded_because": "manifest gained r5a absolute_tolerances; re-run so "
                                                                     "the CANDIDATE names the manifest bytes the study used"}
            be = rc.NATIVE / "breakeven" / f"{rc.STUDY_ID}-breakeven.db"
            if be.exists():
                stores.append(store_entry("store-rebco-breakeven", be))
                arm["supplementary_store_ids"] = ["store-rebco-breakeven", "store-rebco-baseline"]
        elif unit == "nb3sn":
            arm["supplementary_store_ids"] = ["store-nb3sn-baseline"]
        arms.append(arm)
    for name in ("tolerance-diagnostic-rebco", "tolerance-diagnostic-nb3sn"):
        stores.append(store_entry(f"store-{name}", rc.RESULTS / "_work" / f"{name}.db"))
    tools = []
    for tool, files in (("scripts/study/indicators.py", None), ("scripts/study/preflight.py", None),
                        ("scripts/study/verify.py", None), ("scripts/integrate.py", None)):
        tools.append({"path": tool, "source_digest": common.tool_source_digest((tool,))})
    tools.append({"path": "exploration/stellarator_materials/studies/study_route.py", "source_digest": common.tool_source_digest(
        ("exploration/stellarator_materials/studies/study_route.py", "exploration/stellarator_materials/studies/interface_data.py"))})
    tools.append({"path": rel(rc.RECORD), "source_digest": common.tool_source_digest(tuple(rel(rc.RECORD / p) for p in RECORD_SCRIPTS))})
    snapshot = {
        "snapshot_schema_version": "1", "study_id": rc.STUDY_ID,
        "status": "executed and verified against the three integration CANDIDATE pins (contract r5a clause)",
        "integration_pin_issued": True,
        "machine_local_artifacts": {"paths": list(MACHINE_LOCAL),
                                    "note": "kept out of git by the record's .gitignore and studies/.gitignore (**/_work/); "
                                            "digests here; the declared case list studies/cases.json is also ignored "
                                            f"(repository .gitignore:104; sha256 {rc.CASES_SHA256})"},
        "cases": {"path": rel(rc.CASES), "sha256": rc.CASES_SHA256, "n_cases": 2921},
        "stores": stores, "arms": arms, "tools": tools,
        "teax": {"revision": arms[0]["integration"]["expected_teax_revision"], "era_pin": None},
        "superseded": sorted(f"superseded/{p.name}" for p in (rc.RECORD / "superseded").iterdir()),
    }
    common.write_document(snapshot, out)
    print("wrote", out, "sha256", sha(out))


if __name__ == "__main__":
    main()
