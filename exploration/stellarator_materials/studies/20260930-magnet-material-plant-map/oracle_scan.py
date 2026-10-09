"""Step 7: scan the declared case list with the independent oracle and record what the scan shows.

The candidate set is the declared case list (studies/cases.json, 2,921 cases): the scan fixes nothing. Each case is
evaluated with the oracle (`oracle_glue.evaluate_material_case` through oracle_entry.py) on the proposal the package
will receive (the case's inputs less the Nb3Sn package constant `magnet__eps_min`, which the oracle holds at the same
value), and its contract section 7 status is derived from the oracle's own verdicts and channels (statuses.py).
Counts by status, cell, material, offer kind and variant, the near-threshold counts, the flags, and the agreement of
the derived status with the policy's recorded `status_expected` go to results/oracle_scan_summary.json; the per-case
rows to results/oracle_scan.json (machine-local; digest in the snapshot).

    .codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" exec python <record>/oracle_scan.py [--workers N]'
"""
from __future__ import annotations

import argparse
import multiprocessing as mp
import time
import traceback
from collections import Counter, defaultdict

import record_common as rc
import statuses as st
from exploration.stellarator_materials.studies.interface_data import INTERFACE

KEY_CHANNELS = ("lcoe_calc__lcoe", "plasma__fusion__p_fus", "plasma__sustain__p_aux_required", "plasma__beta_calc__beta",
                "magnet__peak_field_calc__B_peak", "pb__p_net", "magnet__stored_energy__W_mag",
                "magnet__pack_field__R_over_sqrt_A_wp", "total_capital__total_capital")


def proposal(case: dict) -> dict:
    """The case as the package receives it: every declared input that is an entry key of its unit."""
    unit = case["labels"]["material"]
    U = INTERFACE["units"][unit]
    out = {}
    for key, value in case["inputs"].items():
        if key in U["entry_keys"]:
            out[key] = value
        elif key in U["constant_channels"] and float(value) == float(U["constant_channels"][key]["value"]):
            continue
        else:
            raise KeyError(f"{case['case_id']}: {key} is neither an entry key nor its package constant")
    return out


_ORACLE = None


def _scan(args):
    case, op_class = args
    global _ORACLE
    if _ORACLE is None:
        _ORACLE = rc.oracle()
    unit = case["labels"]["material"]
    P = INTERFACE["units"][unit]["prefix"]
    row = {"case_id": case["case_id"], "unit": unit, "labels": {k: v for k, v in case["labels"].items() if k != "expected"},
           "status_expected": case["status_expected"], "op_class": op_class}
    try:
        r = _ORACLE.evaluate_full(proposal(case))
    except Exception as exc:  # a domain refusal is a result (design K25), recorded with its text
        row.update(refusal=f"{type(exc).__name__}: {exc}", status=st.status(unit, f"{type(exc).__name__}: {exc}",
                                                                              None, None, {}, op_class)[0])
        row["reasons"] = ["domain refusal: " + row["refusal"]]
        return row
    ch = {k[len(P):]: v for k, v in r["channels"].items()}
    inputs = r["resolved"]
    status, reasons = st.status(unit, None, ch, r["verdicts"], inputs, op_class)
    row.update(refusal=None, status=status, reasons=reasons,
               violated=sorted(k for k, s in r["verdicts"].items() if s != "satisfied"),
               channels={k: ch[k] for k in KEY_CHANNELS},
               flags=st.flags(unit, ch, r["verdicts"], inputs, case),
               near_threshold=st.near_threshold(unit, ch, inputs),
               structure_mass_residual=r["checks"]["structure_mass"]["relative_residual"])
    return row


def summarize(rows: list[dict]) -> dict:
    def tally(key):
        out = defaultdict(Counter)
        for r in rows:
            out[key(r)][r["status"]] += 1
        return {k if isinstance(k, str) else "|".join(map(str, k)): dict(v) for k, v in sorted(out.items(), key=lambda i: str(i[0]))}
    near = defaultdict(Counter)
    for r in rows:
        for name in r.get("near_threshold", []):
            near[r["unit"]][name] += 1
    flag_counts = defaultdict(Counter)
    for r in rows:
        for name, value in (r.get("flags") or {}).items():
            if isinstance(value, bool) and value:
                flag_counts[r["unit"]][name] += 1
        if (r.get("flags") or {}).get("power_short"):
            flag_counts[r["unit"]]["power_short"] += 1
    mismatch = [{"case_id": r["case_id"], "derived": r["status"], "policy": r["status_expected"]}
                for r in rows if r["status"] != r["status_expected"]]
    ignited_check = [r["case_id"] for r in rows if r["status"] == "ignited"
                     and not r["channels"]["plasma__sustain__p_aux_required"] < 0.0]
    return {
        "cases": len(rows),
        "by_status": dict(Counter(r["status"] for r in rows)),
        "by_material": tally(lambda r: r["unit"]),
        "by_cell_material": tally(lambda r: (r["labels"]["cell_geometry"], r["labels"]["cell_f_ren"], r["unit"])),
        "by_offer_kind": tally(lambda r: (r["unit"], r["labels"]["offer_kind"])),
        "by_variant": tally(lambda r: (r["unit"], r["labels"]["variant"])),
        "refusals": [{"case_id": r["case_id"], "text": r["refusal"]} for r in rows if r["refusal"]],
        "near_threshold_rule": "|operand - threshold| <= 0.02 x scale per status-deciding check (statuses.py)",
        "near_threshold_counts": {u: dict(c) for u, c in near.items()},
        "near_threshold_cases": {u: sum(1 for r in rows if r["unit"] == u and r.get("near_threshold")) for u in rc.MATERIALS},
        "flag_counts": {u: dict(c) for u, c in flag_counts.items()},
        "status_vs_policy_mismatches": mismatch,
        "ignited_without_negative_heating": ignited_check,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workers", type=int, default=8)
    args = parser.parse_args()
    data = rc.load_cases()
    by_id = {c["case_id"]: c for c in data["cases"]}
    work = [(c, st.operating_point_class(c, by_id)) for c in data["cases"]]
    started = time.time()
    with mp.get_context("fork").Pool(args.workers) as pool:
        try:
            rows = pool.map(_scan, work, chunksize=8)
        except Exception:
            traceback.print_exc()
            raise
    elapsed = time.time() - started
    summary = summarize(rows)
    summary.update(elapsed_seconds=round(elapsed, 1), workers=args.workers,
                   cases_file={"path": str(rc.CASES.relative_to(rc.REPO)), "sha256": rc.CASES_SHA256},
                   oracle={"module": rc.ORACLE_MODULE, "oracle_glue_sha256":
                           rc.sha256(rc.REPO / "exploration/stellarator_materials/oracle_glue.py")})
    rc.write_json({"study_id": rc.STUDY_ID, "rows": rows}, rc.RESULTS / "oracle_scan.json")
    rc.write_json(summary, rc.RESULTS / "oracle_scan_summary.json")
    print({k: summary[k] for k in ("cases", "by_status", "elapsed_seconds")}, "mismatches",
          len(summary["status_vs_policy_mismatches"]), "ignited check", len(summary["ignited_without_negative_heating"]))
