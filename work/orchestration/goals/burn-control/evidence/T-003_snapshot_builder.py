"""Build `snapshot.json` for the re-reading study `20260907-burn-control` (runbook step 15; goal burn-control T-003),
mirroring the committed `20260905-stored-energy-basis` snapshot's shape field for field (its builder,
work/orchestration/goals/stored-energy-basis/evidence/round2_T-003_snapshot_builder.py, adapted: the join target,
the counterfactual digests dropped, the ten-verdict counts added). There is no
snapshot builder tool; this script is the one this study used, deposited as goal evidence so the
snapshot's every value can be re-derived. Run AFTER verification (step 10) and the exports:
    python T-003_snapshot_builder.py <record_dir> <store_db_path> <repo_commit>
Every digest is computed over the current tree by the study tools' own helpers
(`scripts/study/manifest.py::sha256_file`, `scripts/study/common.py::tool_source_digest`); the tool
and oracle source-file LISTS are taken from the committed snapshot (they name the same files) and
the digests recomputed, never copied.
"""
import csv, json, subprocess, sys
from collections import Counter
from pathlib import Path
ROOT = Path(__file__).resolve().parents[5]   # work/orchestration/goals/<goal>/evidence/<this file> -> the repository root
sys.path.insert(0, str(ROOT))
from scripts.study import manifest as m
from scripts.study import common

record = Path(sys.argv[1]).resolve(); store_db = Path(sys.argv[2]); repo_commit = sys.argv[3]
rel = lambda p: str(Path(p).resolve().relative_to(ROOT))
STUDY_ID = record.name
PKG = ROOT / "exploration/stellarator_e2e/pkg/stellarator_tea"
MAN = ROOT / "exploration/stellarator_e2e/studies/manifest.json"
committed_snap = json.load(open(ROOT / "exploration/stellarator_e2e/studies/20260905-stored-energy-basis/snapshot.json"))
man = json.load(open(MAN))
ident = json.load(open(record / "results/package_identity.json"))
ver = json.load(open(record / "results/verification_summary.json"))
pre = json.load(open(record / "results/preflight_results.json"))
ind = json.load(open(record / "indicators.json"))
pts = list(csv.DictReader((record / "results/points.csv").open()))
exc = list(csv.DictReader((record / "results/excluded_points.csv").open()))
b = lambda x: str(x).strip().lower() == "true"
git_clean = subprocess.run(["git", "status", "--porcelain", "--", rel(PKG.resolve())], capture_output=True, text=True, cwd=ROOT).stdout.strip() == ""
ind_fp = m.indicator_input_fingerprint(PKG)
sealed = ident.get("digest") or ident.get("identity", {}).get("digest")
store = ver["stores"][0]
arms = ["arm-fence-p100", "arm-search-p220", "arm-reread-p220", "arm-transect-ash"]
by_arm = Counter(p["arm_id"] for p in pts)
feas = Counter(p["arm_id"] for p in pts if b(p["feasible"]))
driven = Counter(p["arm_id"] for p in pts if b(p["feasible_driven"]))
feas9 = Counter(p["arm_id"] for p in pts if b(p["feasible_nine"]))
burn_viol = Counter(p["arm_id"] for p in pts if p["burn_hold_ok"] == "violated")
sv059 = Counter(p["arm_id"] for p in pts if b(p["sv059_feasible_equals_driven"]) and b(p["sv059_verdict_equals_sign"]))
falling = Counter(p["arm_id"] for p in pts if p.get("branch_oracle") == "falling")
rising = Counter(p["arm_id"] for p in pts if p.get("branch_oracle") == "rising")
ign = Counter(p["arm_id"] for p in pts if b(p["ignited"]))
lo = Counter(p["arm_id"] for p in pts if b(p["feasible_shadow_lo"]))
hi = Counter(p["arm_id"] for p in pts if b(p["feasible_shadow_hi"]))
newrows = Counter(p["arm_id"] for p in pts if p["class_vs_committed"] == "not_proposed_by_committed")
GEOM = {"R_m": [11.2, 12.7, 14.2, 15.7, 17.2], "a_m": [1.3, 1.5, 1.7, 1.8, 2.0, 2.2], "I_coil_MA": [13.0, 14.0, 15.0, 16.0, 18.0],
        "T_i0_keV": [13.0, 14.63, 16.0, 17.0, 18.0], "n_e0_mult": [0.6, 0.7, 0.8, 0.9, 1.0], "validity_mask": "R > a + 2.25 (ANNEX section Validity masks)"}
WINDOWS = {
    "arm-fence-p100": {"p_wallplug_heat_MW": 100.0, **GEOM, "note": "the committed 20260905 arm-fence-p100 grid (the 20260904 grid plus the pinned baseline, with the T 13 keV row restored), inherited unchanged"},
    "arm-search-p220": {"p_wallplug_heat_MW": 220.0, **GEOM, "note": "the committed 20260905 arm-search-p220 grid (the T 13 keV row restored), inherited unchanged"},
    "arm-reread-p220": {"p_wallplug_heat_MW": 220.0, "R_m": [12.7], "a_m": [1.3], "I_coil_MA": [14.0, 14.25, 14.5, 14.75, 15.0, 15.25], "T_i0_keV": [14.63, 16.0, 17.0, 18.0], "n_e0_mult": [0.8, 0.9, 1.0, 1.1], "eta_source_heat": [0.45, 0.50, 0.55, 0.60], "note": "round 1's 220 MW grid as the committed re-read arm carried it, less the 24 points the geometry grid carries; unchanged"},
    "arm-transect-ash": {"tau_ratio_ash": [2.0, 4.0, 6.0, 12.0, 16.0], "anchors": "the committed three (scan best at 100 MW; scan best at 220 MW; the design column); unchanged"},
}
fixed_from = ("inherited unchanged from the committed 20260905-stored-energy-basis record (700bfe6d; itself the 20260904-wall-and-heating windows with the 13 keV rows restored; provenance engineered there), "
              "as the re-read's object; the edges re-read at the WI-043 pin with the tenth fence beside the nine in results/window_edges.json (edges.py, the same three anchors) -- record.md section 11")
verify_cmd = ver.get("command") if isinstance(ver.get("command"), str) else " ".join(ver.get("command", []))
arm_entries = []
for a in arms:
    arm_entries.append({
        "arm_id": a, "store_id": STUDY_ID,
        "effective_executable_fingerprint": {"value": sealed, "inputs": None, "no_adapter": True,
                                             "note": "no adapter exists; the sealed fingerprint is the identity (results/package_identity.json digest)"},
        "entry_models": committed_snap["arms"][0]["entry_models"],
        "strategy": "prepared-list/v1",
        "evaluated": by_arm[a], "feasible": feas[a], "feasible_nine": feas9[a], "feasible_driven": driven[a], "ignited": ign[a],
        "burn_hold_violated": burn_viol[a], "sv059_both_identities_hold": sv059[a], "branch_falling": falling[a], "branch_rising": rising[a],
        "not_proposed_by_committed": newrows[a],
        "feasible_under_wall_shadow_lo": lo[a], "feasible_under_wall_shadow_hi": hi[a],
        "window": {"provenance": "engineered", "fixed_from": fixed_from, "values": WINDOWS[a]},
        "verification": {"command": verify_cmd, "tool_revision": ver["tool"]["source_digest"]["digest"] if isinstance(ver.get("tool"), dict) else str(ver.get("tool")),
                          "sampling_scheme": (ver.get("stores", [{}])[0].get("sampling", {}) or {}).get("scheme", "stratified-by-verdict-combination/v1"),
                          "tolerance": str(ver.get("tolerance")), "summary_sha256": m.sha256_file(record / "results/verification_summary.json"),
                          "note": "one store, one verification run over all four arms; the sample is stratified over the verdict combinations the whole study produced"},
        "glue_ledger": [], "glue_ledger_none": True,
        "artifacts": [{"path": rel(record / "results" / f), "sha256": m.sha256_file(record / "results" / f)} for f in ("points.csv", "oracle_operands.csv", "excluded_points.csv", "verification_summary.json")],
    })
results_artifacts = {f"results/{f.name}": m.sha256_file(f) for f in sorted((record / "results").glob("*")) if f.is_file()}
tools = []
for t in committed_snap["tools"]:
    files = tuple(e["path"] for e in t["source_digest"]["files"])
    tools.append({"path": t["path"], "source_digest": common.tool_source_digest(files)})
oracle_files = tuple(e["path"] for e in committed_snap["manifest"]["content_used"]["oracle"]["source_digest"]["files"])
snap = {
    "snapshot_schema_version": "1", "study_id": STUDY_ID,
    "package": {"path": rel(PKG), "package_name": "stellarator_tea", "repo_commit": repo_commit,
                "repo_commit_note": "the commit the study executed against; the record itself lands in the next commit", "git_clean": git_clean},
    "fingerprints": {"indicator_inputs": ind_fp,
                     "recorded_provenance.executable_fingerprint": man["fingerprints"]["recorded_provenance"]["executable_fingerprint"],
                     "recorded_provenance.semantic_fingerprint": man["fingerprints"]["recorded_provenance"]["semantic_fingerprint"],
                     "sealed_executable_fingerprint": sealed},
    "manifest": {"path": rel(MAN), "schema_version": man["schema_version"], "digest": m.sha256_file(MAN),
                 "content_used": {"fingerprint_names": sorted(man["fingerprints"].keys()) + ["recorded_provenance.executable_fingerprint", "recorded_provenance.semantic_fingerprint"],
                                  "ties": man["ties"], "ties_note": "one declared tie (magnet__R0 rides with R); swept in every arm; unchanged since WI-039",
                                  "objective_catalog": man["objective_catalog"], "baseline": man["baseline"],
                                  "oracle": {**man["oracle"], "source_digest": common.tool_source_digest(oracle_files)}}},
    "stores": [{"store_id": STUDY_ID, "path": rel(store_db), "committed": False,
                "note": "uncommitted per the study-store convention (**/_work/ is gitignored); results/*.csv carry every value this record cites",
                "compatibility_tuple": store["compatibility"], "cases_total": store["cases_total"], "cases_completed": store["cases_completed"]}],
    "arms": arm_entries,
    "glue_ledger": "none -- no adapter on this route (sealed package, stock teax); stated per arm as glue_ledger_none",
    "results_artifacts": results_artifacts,
    "indicators": {"path": "indicators.json", "digest": m.sha256_file(record / "indicators.json"), "output_schema_version": ind["schema_version"],
                   "groups": len(ind["groups"]), "subset": bool(ind.get("subset")),
                   "axis_declaration": {"path": rel(record / "axes.json"), "schema_version": json.load(open(record / "axes.json"))["schema_version"],
                                        "digest": m.sha256_file(record / "axes.json"), "groups_declared": sorted(g["axis"] for g in ind["groups"]), "subset": bool(ind.get("subset"))}},
    "axes_declaration": {"path": rel(record / "axes.json"), "digest": m.sha256_file(record / "axes.json")},
    "study_definition": {"path": rel(record / "study.py"), "digest": m.sha256_file(record / "study.py")},
    "scan": {"path": rel(record / "scan.py"), "digest": m.sha256_file(record / "scan.py"), "note": "the committed scan's probe library, inherited verbatim; its full scan was not re-run (the window is inherited)"},
    "edges": {"path": rel(record / "edges.py"), "digest": m.sha256_file(record / "edges.py")},
    "committed_record_joined": {"study_id": "20260905-stored-energy-basis", "commit": "700bfe6d",
                                "results_joined": {f: m.sha256_file(ROOT / "exploration/stellarator_e2e/studies/20260905-stored-energy-basis/results" / f) for f in ("points.csv", "oracle_operands.csv", "excluded_points.csv")},
                                "note": "the committed_* columns of results/points.csv are read from these files by coordinates, never recomputed (record.md section 12); no counterfactual columns in this record"},
    "tools": tools,
    "preflight": {"gates_run": len(pre.get("gates", pre.get("results", []))), "outcome": pre.get("outcome", pre.get("status")),
                  "gates": [{"gate": g.get("gate", g.get("name")), "status": g.get("status", g.get("outcome"))} for g in pre.get("gates", pre.get("results", []))]},
    "counts": {"proposed": len(pts) + len(exc), "evaluated": len(pts), "excluded": len(exc), "feasible_total": sum(feas.values()), "feasible_driven_total": sum(driven.values()),
               "ignited_total": sum(ign.values()), "feasible_nine_total": sum(feas9.values()), "burn_hold_violated_total": sum(burn_viol.values()), "sv059_both_identities_hold_total": sum(sv059.values()), "branch_falling_total": sum(falling.values()), "branch_rising_total": sum(rising.values()),
               "by_arm": dict(by_arm), "feasible_by_arm": dict(feas), "feasible_nine_by_arm": dict(feas9), "feasible_driven_by_arm": dict(driven), "ignited_by_arm": dict(ign), "burn_hold_violated_by_arm": dict(burn_viol),
               "not_proposed_by_committed_by_arm": dict(newrows),
               "feasible_under_wall_shadow_lo_by_arm": dict(lo), "feasible_under_wall_shadow_hi_by_arm": dict(hi),
               "classes_vs_committed": dict(Counter(p["class_vs_committed"] for p in pts)), "excluded_classes_vs_committed": dict(Counter(e["class_vs_committed"] for e in exc))},
    "teax": {"revision": subprocess.run(["git", "-C", str(Path.home() / "1cfe/teax"), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip(), "era_pin": None,
             "revision_source": "git -C $STOP_PARSER_TEAX_ROOT rev-parse HEAD at build time; the round's integration return (work/orchestration/goals/burn-control/evidence/T-002_integration_return.json) names the same revision"},
}
(record / "snapshot.json").write_text(json.dumps(snap, indent=1) + "\n")
print("snapshot.json written:", m.sha256_file(record / "snapshot.json"))
