"""Step 15: resolve every snapshot value at this moment and write snapshot.json (record-template appendix shape).

    .codex-test/run bash -c 'PYTHONPATH="$PWD" exec python <record>/build_snapshot.py'
"""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

from scripts.study import common
from scripts.study import manifest as manifest_mod
from exploration.magnet_materials.studies import interface_data

RECORD = Path(__file__).resolve().parent
ROOT = manifest_mod.repo_root()
rel = lambda p: manifest_mod.repo_relative_posix(p)
sha = lambda p: manifest_mod.sha256_file(p)


def source_digest(paths):
    return common.tool_source_digest(tuple(paths))


def main():
    out = RECORD / "snapshot.json"
    if out.exists():
        raise SystemExit("snapshot.json exists; a changed snapshot is a different study")
    manifest = json.loads((RECORD / "manifest.json").read_text())
    indicators = json.loads((RECORD / "indicators.json").read_text())
    axes = json.loads((RECORD / "axes.json").read_text())
    preflight = json.loads((RECORD / "results" / "preflight_results.json").read_text())
    verification = json.loads((RECORD / "results" / "verification_summary.json").read_text())
    full = json.loads((RECORD / "results" / "verification_full.json").read_text())
    context = json.loads((RECORD / "results" / "execution-context.json").read_text())
    integration = json.loads((RECORD / "results" / "integration_return_used.json").read_text())
    if integration.get("class") != "CANDIDATE":
        raise SystemExit("snapshot requires the CANDIDATE integration return used by execute_study.py")
    first_attempt = ROOT / "work/orchestration/goals/magnet-material-comparison/evidence/integration-r1/integration_return.json"
    first = json.loads(first_attempt.read_text())
    machine_local = ("results/cases.json", "results/oracle_scan.json", "results/native/", "results/_work/")
    declared = json.loads((RECORD / "results" / "cases_declared.json").read_text())
    package_root = ROOT / manifest["package"]["path"]
    git_clean = common.git_status_porcelain(package_root) == ""
    repo_commit = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True, cwd=ROOT).stdout.strip()

    def flatten(block, prefix=""):
        names = []
        for key, value in block.items():
            name = f"{prefix}{key}"
            if isinstance(value, dict) and "digest" not in value:
                names += flatten(value, name + ".")
            else:
                names.append(name)
        return names

    fingerprint_names = flatten(manifest["fingerprints"])
    fingerprints = {
        "indicator_inputs": indicators["package"]["indicator_input_fingerprint"],
        "recorded_provenance.executable_fingerprint": manifest["fingerprints"]["recorded_provenance"]["executable_fingerprint"],
        "recorded_provenance.semantic_fingerprint": manifest["fingerprints"]["recorded_provenance"]["semantic_fingerprint"],
    }
    assert set(fingerprint_names) == set(fingerprints)

    stores = []
    for store_id, summary in zip(("native", "baseline"), verification["stores"]):
        tuple_ = {k: v for k, v in summary["compatibility"].items() if k != "digest"}
        stores.append({"store_id": store_id, "path": summary["path"], "compatibility_digest": summary["compatibility"]["digest"],
                       "compatibility_tuple": tuple_, "cases_total": summary["cases_total"], "cases_completed": summary["cases_completed"]})

    entry_models = {}
    for key, model in interface_data.INTERFACE["entry_keys"].items():
        entry_models.setdefault(model, []).append(key)
    entry_models = {model: sorted(keys) for model, keys in sorted(entry_models.items())}

    artifacts = []
    for path in sorted((RECORD / "results").iterdir()):
        if path.is_file():
            entry = {"path": f"results/{path.name}", "sha256": sha(path), "bytes": path.stat().st_size}
            if entry["path"] in machine_local:
                entry["in_git"] = False
            artifacts.append(entry)
    for sub in ("native", "_work"):
        for path in sorted((RECORD / "results" / sub).glob("*.db")):
            artifacts.append({"path": f"results/{sub}/{path.name}", "sha256": sha(path), "bytes": path.stat().st_size, "in_git": False})
        files = sorted((RECORD / "results" / sub / "artifacts").glob("*.json"))
        aggregate = hashlib.sha256("".join(f"{f.name} {sha(f)}\n" for f in files).encode()).hexdigest()
        artifacts.append({"path": f"results/{sub}/artifacts/", "sha256": aggregate, "recipe": "sha256 over '<name> <sha256>\\n' lines sorted by name",
                          "files": len(files), "bytes": sum(f.stat().st_size for f in files), "in_git": False})

    window_bounds = {
        "anchor": ["D", "S"],
        "B_peak_T": {"D": [8, 9, 10, 11, 12, 13, 14, 16, 18, 20], "S": [8, 9, 10, 11, 12, 13]},
        "pairing": ["common-P", "native", "common-C"],
        "rule_family": ["reference", "both-temperature", "both-fraction"],
        "offer_kind": ["reference", "insufficient (floor 0.9 n)", "generous (ceil 1.2 n)", "variant-offer"],
        "refrigerator_kind": ["reference (smallest listed rating >= demand)", "insufficient (next lower listed rating)"],
        "variants": sorted(declared["header"]["counts"]["variant"]),
        "generating_rule": "exploration/magnet_materials/studies/declare_cases.py over offer_policy.py; cases.json sha256 " + declared["sha256"],
        "declared_cases": declared["n_cases"], "distinct_points": context["unique_points"],
    }

    snapshot = {
        "snapshot_schema_version": "1",
        "study_id": RECORD.name,
        "status": "executed and verified against the integration CANDIDATE pin",
        "integration_pin_issued": True,
        "machine_local_artifacts": {"paths": list(machine_local),
                                    "note": ".gitignore (commit c4195090a) keeps these out of git; their digests are in arms[].artifacts and they stay on the machine that ran the study, with the declared case list exploration/magnet_materials/studies/cases.json (also ignored; sha256 in results/cases_declared.json, regenerated by declare_cases.py)"},
        "package": {"path": manifest["package"]["path"], "package_name": manifest["package"]["name"],
                    "repo_commit": repo_commit, "git_clean": git_clean},
        "fingerprints": fingerprints,
        "manifest": {
            "path": rel(RECORD / "manifest.json"), "schema_version": manifest["schema_version"], "digest": sha(RECORD / "manifest.json"),
            "stock_manifest": {"path": "exploration/magnet_materials/studies/manifest.json", "digest": sha(ROOT / "exploration/magnet_materials/studies/manifest.json"),
                               "differs_in": ["oracle (record-local adapter binding)", "absolute_tolerances (16 channels, contract r3 section 8)"]},
            "content_used": {
                "fingerprint_names": fingerprint_names,
                "ties": manifest["ties"],
                "objective_catalog": manifest["objective_catalog"],
                "baseline": manifest["baseline"],
                "absolute_tolerances": manifest["absolute_tolerances"],
                "oracle": {**{k: manifest["oracle"][k] for k in ("kind", "module", "callable", "sys_path", "note")},
                           "source_digest": source_digest([
                               "exploration/magnet_materials/oracle.py",
                               rel(RECORD / "oracle_entry.py"),
                               "exploration/magnet_materials/studies/interface_data.py"]),
                           "operand_bindings_digest": verification["oracle"]["operand_bindings_digest"]},
            },
        },
        "stores": stores,
        "arms": [{
            "arm_id": "arm-declared-cases", "store_id": "native",
            "effective_executable_fingerprint": {"value": fingerprints["recorded_provenance.executable_fingerprint"], "inputs": None,
                                                 "no_adapter": True, "note": "no adapter exists; the sealed fingerprint is the identity"},
            "entry_models": entry_models,
            "strategy": stores[0]["compatibility_tuple"]["strategy_identity"],
            "window": {"bounds": window_bounds, "provenance": "engineered"},
            "verification": {
                "command": verification["command"],
                "tool_revision": verification["tool"]["source_digest"]["digest"],
                "sampling_scheme": verification["stores"][0]["sampling"]["scheme"] + " with --sample-size 2310 (every stored point sampled; 34 strata)",
                "tolerance": "rel < 1e-9 or declared absolute 1e-9 per unit on 16 objective/operand channels (stock); rel < 1e-9 or abs < 1e-9 on all 128 non-constant channels (full)",
                "summary_sha256": sha(RECORD / "results" / "verification_summary.json"),
                "full_verification": {"path": "results/verification_full.json", "sha256": sha(RECORD / "results" / "verification_full.json"),
                                      "tool": rel(RECORD / "verify_all.py"), "tool_sha256": sha(RECORD / "verify_all.py"),
                                      "channels_checked": full["channels_checked"], "stored_points": full["stored_points_verified"],
                                      "outcome": full["outcome"], "worst_relative_deviation": full["worst_relative_deviation"],
                                      "worst_absolute_error": full["worst_absolute_error"],
                                      "constant_channels_excluded": full["constant_channels_excluded"]},
            },
            "glue_ledger": [], "glue_ledger_none": True,
            "execution": {"context": "results/execution-context.json", "without_candidate": context["without_candidate"],
                          "elapsed_seconds": context["elapsed_seconds"], "declared_cases": context["cases"],
                          "distinct_points": context["unique_points"], "completed": context["completed"]},
            "artifacts": artifacts,
        }],
        "tools": [
            {"path": "scripts/study/indicators.py", "source_digest": indicators["tool"]["source_digest"]},
            {"path": "scripts/study/preflight.py", "source_digest": preflight["tool"]["source_digest"]},
            {"path": "scripts/study/verify.py", "source_digest": verification["tool"]["source_digest"]},
            {"path": "scripts/integrate.py", "source_digest": integration["tool"]["source_digest"]},
            {"path": "exploration/magnet_materials/studies/study_route.py", "source_digest": source_digest([
                "exploration/magnet_materials/studies/study_route.py", "exploration/magnet_materials/studies/interface_data.py"])},
            {"path": rel(RECORD / "execute_study.py"), "source_digest": source_digest([rel(RECORD / p) for p in (
                "declare_axes.py", "run_baseline.py", "oracle_scan.py", "execute_study.py", "oracle_entry.py", "verify_all.py", "summarize.py", "build_snapshot.py")])},
        ],
        "teax": {"revision": integration["toolchain"].get("teax_revision") if isinstance(integration.get("toolchain"), dict) else None,
                 "era_pin": None},
        "indicators": {"path": "indicators.json", "sha256": sha(RECORD / "indicators.json"),
                       "output_schema_version": indicators["schema_version"],
                       "axis_declaration": indicators["axis_declaration"]},
        "integration": {"return": rel(ROOT / "work/orchestration/goals/magnet-material-comparison/evidence/integration-r2/integration_return.json"),
                        "sha256": sha(RECORD / "results" / "integration_return_used.json"),
                        "class": integration["class"], "exit_code": integration["exit_code"],
                        "candidate": integration["candidate"],
                        "audited_work": integration["request"]["audited_work"],
                        "gates": [{"gate": g["gate"], "status": g["status"]} for g in integration["gates"]],
                        "expected_teax_revision": next(a for i, a in enumerate(integration["command"]) if integration["command"][i - 1] == "--expected-teax-revision"),
                        "first_attempt": {"return": rel(first_attempt), "sha256": sha(first_attempt), "class": first["class"],
                                          "blocker": {k: first["blocker"][k] for k in ("gate", "scope", "mode", "condition")},
                                          "audited_work": first["request"]["audited_work"],
                                          "resolved_by": "c4195090a (tests/model_families.py registers SOURCE_COLLECTIONS[\"magnet_materials\"]; package bytes unchanged)"}},
    }
    if snapshot["teax"]["revision"] is None:
        snapshot["teax"]["revision"] = snapshot["integration"]["expected_teax_revision"]
    common.write_document(snapshot, out)
    print("wrote", out, "sha256", sha(out))


if __name__ == "__main__":
    main()
