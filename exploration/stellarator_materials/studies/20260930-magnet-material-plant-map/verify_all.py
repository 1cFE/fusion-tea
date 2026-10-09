"""Step 10 (full): verify every channel and every verdict of every stored case against the independent oracle.

For each material unit's store (results/native/<unit>/), every case is re-evaluated with the oracle
(oracle_entry.evaluate_full) on the inputs the store recorded, in a worker pool:

* channels: every published non-constant channel compared under contract r5a section 9 (1e-9 relative or 1e-9
  absolute per unit of the channel, whichever is looser; nonfinite values must match exactly). Constant channels are
  excluded and listed; package channels the oracle has no leg for are listed, with the executor's identity check on
  them (not an oracle comparison).
* verdicts: every recorded verdict re-derived from the oracle's own operands through the package's predicate IR and
  the published operand bindings (scripts/study/verify.derive_verdict), and also compared with the oracle's own
  Kleene verdict; a nonfinite operand must be recorded `indeterminate` on both sides.
* refusals: a case the package recorded execution_failed must be refused by the oracle too; both texts are kept.
* statuses: the contract section 7 status re-derived from the recorded verdicts, recorded inputs and channels and the
  design's operating-point class (statuses.py), compared with the oracle-derived status of the scan.

Any disagreement is recorded, never adjusted; the outcome is `fail` if any exists. Writes
results/verification_summary.json (the summary) and results/oracle_verification.json (per-case worst deviations;
machine-local).

    .codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" exec python <record>/verify_all.py [--workers N]'
"""
from __future__ import annotations

import argparse
import json
import math
import multiprocessing as mp
import time
from collections import Counter, defaultdict
from pathlib import Path

import record_common as rc
import statuses as st
from exploration.stellarator_materials.studies import study_route as route
from exploration.stellarator_materials.studies.interface_data import INTERFACE
from scripts.study import manifest as manifest_mod
from scripts.study import verify

REL, ABS = 1e-9, 1e-9
_ORACLE = None


def agree(native, oracle) -> tuple[bool, float, float]:
    native, oracle = float(native), float(oracle)
    if not (math.isfinite(native) and math.isfinite(oracle)):
        same = (math.isnan(native) and math.isnan(oracle)) or native == oracle
        return same, (0.0 if same else math.inf), (0.0 if same else math.inf)
    err = abs(native - oracle)
    return err <= max(REL * abs(oracle), ABS), err / max(abs(oracle), 1e-30), err


def _oracle_eval(item):
    cid, inputs = item
    global _ORACLE
    if _ORACLE is None:
        _ORACLE = rc.oracle()
    try:
        r = _ORACLE.evaluate_full(inputs)
    except Exception as exc:
        return cid, {"refusal": f"{type(exc).__name__}: {exc}"}
    return cid, {"refusal": None, "channels": r["channels"], "verdicts": r["verdicts"]}


def load_store(unit: str, root: Path):
    from simkit.study.query import StudyQuery
    from simkit.study.store import StudyStore

    db = root / "native" / unit / f"{rc.STUDY_ID}-{unit}.db"
    store = StudyStore(db)
    try:
        cases = StudyQuery(store, route.unit_of(unit).package_dir.resolve()).cases()
    finally:
        store.close()
    return cases, db


def verify_unit(unit: str, pool, root: Path, scan: dict, declared: dict, by_id: dict) -> tuple[dict, dict]:
    U = INTERFACE["units"][unit]
    P = U["prefix"]
    oracle = rc.oracle()
    cases, db = load_store(unit, root)
    exported = json.loads((root / f"cases_{unit}.json").read_text())["cases"]
    case_of = {r["candidate_id"]: r["case_id"] for r in exported}
    constants = set(oracle.constant_channels(unit))
    bindings = oracle.operand_bindings(unit)
    catalog = json.loads((route.unit_of(unit).package_dir / "contracts/model_contract.json").read_text())
    entries = {e["constraint_id"]: e for e in catalog["constraint_catalog"]["concrete_entries"]}
    local_of = {cid: e["source_local_identity"] for cid, e in entries.items()}
    package_inputs = verify.package_input_values(route.unit_of(unit).package_dir)
    defaults = {k[len(P):]: v for k, v in U["baseline_point"].items()}
    failures = route.failure_texts(db)

    results = dict(pool.imap_unordered(_oracle_eval, [(c.candidate_id, dict(c.inputs)) for c in cases], chunksize=4))
    per_channel = defaultdict(lambda: {"worst_relative": 0.0, "worst_absolute": 0.0, "compared": 0,
                                       "needed_absolute": 0})
    disagreements, verdict_mismatches, refusal_mismatches, status_mismatches = [], [], [], []
    uncovered, uncovered_checks = set(), Counter()
    verdict_counts, status_counts, indeterminate = Counter(), Counter(), Counter()
    per_case = []
    worst = {"relative": (0.0, None, None), "absolute": (0.0, None, None)}
    for case in cases:
        case_id = case_of[case.candidate_id]
        o = results[case.candidate_id]
        decl = declared[case_id]
        op_class = st.operating_point_class(decl, by_id)
        if case.state != "completed":
            text = (failures.get(case.candidate_id) or {}).get("cause") or f"execution_failed ({case.state})"
            if o["refusal"] is None:
                refusal_mismatches.append({"case_id": case_id, "package": text, "oracle": "evaluated"})
            status, _ = st.status(unit, text, None, None, {}, op_class)
            status_counts[status] += 1
            if scan[case_id]["status"] != status:
                status_mismatches.append({"case_id": case_id, "package": status, "scan": scan[case_id]["status"]})
            per_case.append({"case_id": case_id, "state": case.state, "package_refusal": text,
                             "oracle_refusal": o["refusal"], "status": status})
            continue
        if o["refusal"] is not None:
            refusal_mismatches.append({"case_id": case_id, "package": "completed", "oracle": o["refusal"]})
            continue
        channels = o["channels"]
        case_worst = (0.0, None)
        for name, value in case.outputs.items():
            if name in constants:
                continue
            if name not in channels:
                uncovered.add(name)
                continue
            ok, rel, err = agree(value, channels[name])
            row = per_channel[name]
            row["compared"] += 1
            if math.isfinite(rel):
                row["worst_relative"] = max(row["worst_relative"], rel)
                row["worst_absolute"] = max(row["worst_absolute"], err)
                if rel > worst["relative"][0]:
                    worst["relative"] = (rel, case_id, name)
                if err > worst["absolute"][0]:
                    worst["absolute"] = (err, case_id, name)
                if rel > case_worst[0]:
                    case_worst = (rel, name)
            if ok and math.isfinite(rel) and err > REL * abs(float(channels[name])):
                row["needed_absolute"] += 1
            if not ok:
                disagreements.append({"case_id": case_id, "channel": name, "package": value, "oracle": channels[name],
                                      "relative": rel, "absolute": err})
        # executor identity checks on channels the oracle does not produce (not an oracle comparison)
        q_struct = case.outputs.get(P + "cryoplant__static_loads__q_structure_nuclear")
        n_eff = case.outputs.get(P + "cryoplant__static_loads__nuclear_density_eff")
        given = dict(package_inputs, **dict(case.inputs))
        q_nuc = float(given[P + "magnet__winding_pack__q_nuc_cryo"])
        uncovered_checks["input q_nuc_structure == 0"] += int(float(given[P + "cryoplant__q_nuc_structure"]) == 0.0)
        uncovered_checks["q_structure_nuclear == 0"] += int(q_struct == 0.0)
        uncovered_checks["nuclear_density_eff == winding_pack q_nuc_cryo"] += int(n_eff == q_nuc)
        uncovered_checks["cases"] += 1
        recorded_local = {}
        for cid, recorded in case.verdicts.items():
            local = local_of[cid]
            recorded_local[local] = recorded
            verdict_counts[(local, recorded)] += 1
            own = o["verdicts"][local]
            try:
                satisfied, _ = verify.derive_verdict(cid, entries[cid], bindings, dict(case.inputs), package_inputs,
                                                     channels)
                derived = "satisfied" if satisfied else "violated"
            except verify.VerifyError as exc:
                if "nonfinite" not in str(exc):
                    raise
                derived = "indeterminate"
                indeterminate[local] += 1
            if not (recorded == derived == own):
                verdict_mismatches.append({"case_id": case_id, "constraint_id": cid, "source_local_identity": local,
                                           "recorded": recorded, "rederived": derived, "oracle_kleene": own})
        ch = {k[len(P):]: v for k, v in case.outputs.items()}
        inputs = dict(defaults, **{k[len(P):]: v for k, v in dict(case.inputs).items()})
        status, reasons = st.status(unit, None, ch, recorded_local, inputs, op_class)
        status_counts[status] += 1
        if scan[case_id]["status"] != status:
            status_mismatches.append({"case_id": case_id, "package": status, "scan": scan[case_id]["status"]})
        per_case.append({"case_id": case_id, "state": case.state, "status": status, "reasons": reasons,
                         "worst_relative": case_worst[0], "worst_channel": case_worst[1]})
    summary = {
        "store": manifest_mod.repo_relative_posix(db), "cases": len(cases),
        "completed": sum(c.state == "completed" for c in cases),
        "execution_failed": sum(c.state == "execution_failed" for c in cases),
        "channels_compared": len(per_channel), "channel_comparisons": sum(r["compared"] for r in per_channel.values()),
        "constant_channels_excluded": sorted(constants), "uncovered_channels": sorted(uncovered),
        "uncovered_identity_checks": dict(uncovered_checks),
        "channels_needing_absolute_clause": {k: v["needed_absolute"] for k, v in sorted(per_channel.items())
                                             if v["needed_absolute"]},
        "worst_relative": {"value": worst["relative"][0], "case_id": worst["relative"][1], "channel": worst["relative"][2]},
        "worst_absolute": {"value": worst["absolute"][0], "case_id": worst["absolute"][1], "channel": worst["absolute"][2]},
        "worst_relative_outside_absolute_clause": max(
            (r["worst_relative"] for r in per_channel.values() if not r["needed_absolute"]), default=0.0),
        "constraints_rederived": len(entries), "verdict_counts": {f"{k}|{s}": n for (k, s), n in sorted(verdict_counts.items())},
        "indeterminate_rederived": dict(indeterminate),
        "status_counts": dict(status_counts),
        "disagreements": disagreements, "verdict_mismatches": verdict_mismatches,
        "refusal_mismatches": refusal_mismatches, "status_mismatches_against_scan": status_mismatches,
        "refusals": [{"case_id": r["case_id"], "package": r["package_refusal"], "oracle": r["oracle_refusal"]}
                     for r in per_case if r["state"] != "completed"],
    }
    return summary, {"per_channel": dict(per_channel), "per_case": per_case}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--root", type=Path, help="test aid: results root other than results/")
    args = parser.parse_args()
    root = Path(args.root or rc.RESULTS)
    data = rc.load_cases()
    declared = {c["case_id"]: c for c in data["cases"]}
    scan = {r["case_id"]: r for r in json.loads((rc.RESULTS / "oracle_scan.json").read_text())["rows"]}
    started = time.time()
    units, details = {}, {}
    with mp.get_context("fork").Pool(args.workers) as pool:
        for unit in rc.MATERIALS:
            if not (root / "native" / unit).exists():
                continue
            units[unit], details[unit] = verify_unit(unit, pool, root, scan, declared, declared)
            print(unit, {k: units[unit][k] for k in ("cases", "completed", "execution_failed", "channel_comparisons")},
                  "disagreements", len(units[unit]["disagreements"]), "verdict mismatches",
                  len(units[unit]["verdict_mismatches"]), "worst", units[unit]["worst_relative"], units[unit]["worst_absolute"])
    failed = any(u["disagreements"] or u["verdict_mismatches"] or u["refusal_mismatches"]
                 or u["status_mismatches_against_scan"] for u in units.values())
    oracle = rc.oracle()
    document = {
        "kind": "full-channel-oracle-verification/v1", "record": rc.STUDY_ID,
        "tolerance": {"relative": REL, "absolute_per_unit": ABS,
                      "rule": "agree when |d| <= max(1e-9 |oracle|, 1e-9) (plant-contract.md r5a section 9); "
                              "nonfinite values must match exactly"},
        "oracle": {"binding": "oracle_entry.py (record-local name mapping)", "binding_sha256": rc.sha256(rc.RECORD / "oracle_entry.py"),
                   "oracle_glue_sha256": rc.sha256(rc.REPO / "exploration/stellarator_materials/oracle_glue.py"),
                   "operand_bindings_digest": {u: verify.bindings_digest(oracle.operand_bindings(u)) for u in units}},
        "units": units, "elapsed_seconds": round(time.time() - started, 1),
        "outcome": "fail" if failed else "pass",
    }
    rc.write_json(document, root / "verification_summary.json")
    rc.write_json(details, root / "oracle_verification.json", compact=True)
    print("outcome", document["outcome"])
