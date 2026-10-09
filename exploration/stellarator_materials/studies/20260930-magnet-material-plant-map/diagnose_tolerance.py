"""Stop diagnostic (not study evidence): package against oracle on a stratified sample of declared cases.

Written after the Nb3Sn baseline failed the relative 1e-9 comparison on `magnet__conductor__acceptance_margin`
(the stop condition of brief t017). It characterizes the disagreement for the coordinator's ruling: which channels
exceed the tolerance clause of oracle_entry.agree, on how many sampled cases, the worst case with both values, and
whether the Tcs root itself and every verdict agree. One case per (status_expected, cell geometry, variant family)
stratum per material, seeded; stores go to results/_work/ (machine-local). Adjusts neither side.

    .codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" exec python <record>/diagnose_tolerance.py'
"""
from __future__ import annotations

import random
from collections import Counter, defaultdict

import record_common as rc
from oracle_scan import proposal
from exploration.stellarator_materials.studies import study_route as route
from exploration.stellarator_materials.studies.interface_data import INTERFACE

SEED = 20260930

if __name__ == "__main__":
    oracle = rc.oracle()
    cases = rc.load_cases()["cases"]
    rng = random.Random(SEED)
    report = {"seed": SEED, "rule": "oracle_entry.agree: |d| <= 1e-9 |oracle|, or |d| <= 1e-12 absolute", "units": {}}
    for unit in rc.MATERIALS:
        P = INTERFACE["units"][unit]["prefix"]
        strata = defaultdict(list)
        for c in cases:
            if c["labels"]["material"] == unit:
                strata[(c["status_expected"], c["labels"]["cell_geometry"], c["labels"]["variant"].split("+")[0])].append(c)
        sample = [rng.choice(members) for _, members in sorted(strata.items())]
        stored, _db = route.run_points(unit, f"tolerance-diagnostic-{unit}", [proposal(c) for c in sample],
                                       rc.RESULTS / "_work")
        failing, worst, states, verdict_mismatch, clause = Counter(), {}, Counter(), [], Counter()
        tcs = {"max_relative": 0.0, "max_absolute_K": 0.0}
        for c, k in zip(sample, stored):
            states[k.state] += 1
            try:
                r = oracle.evaluate_full(dict(k.inputs))
            except Exception as exc:
                states["oracle refused" + (" (both)" if k.state == "execution_failed" else " (package evaluated)")] += 1
                continue
            if k.state != "completed":
                states["package refused, oracle evaluated"] += 1
                continue
            for ch, value in k.outputs.items():
                if ch not in r["channels"]:
                    continue
                ok, rel, err, used = oracle.agree(value, r["channels"][ch])
                clause[used] += 1
                if not ok:
                    name = ch[len(P):]
                    failing[name] += 1
                    if name not in worst or err > worst[name]["absolute"]:
                        worst[name] = {"case_id": c["case_id"], "package": value, "oracle": r["channels"][ch],
                                       "relative": rel, "absolute": err}
            if unit == "nb3sn":
                a, b = k.outputs[P + "magnet__conductor__T_cs"], r["channels"][P + "magnet__conductor__T_cs"]
                tcs["max_relative"] = max(tcs["max_relative"], abs(a - b) / abs(b))
                tcs["max_absolute_K"] = max(tcs["max_absolute_K"], abs(a - b))
            for local, status in route.short_verdicts(unit, k).items():
                if r["verdicts"][local] != status:
                    verdict_mismatch.append({"case_id": c["case_id"], "check": local, "package": status,
                                             "oracle": r["verdicts"][local]})
        report["units"][unit] = {"sampled": len(sample), "states": dict(states), "channels_failing": dict(failing),
                                 "worst": worst, "clause_counts": dict(clause), "verdict_mismatches": verdict_mismatch,
                                 "T_cs": tcs if unit == "nb3sn" else None,
                                 "sample": [c["case_id"] for c in sample]}
        print(unit, len(sample), dict(states), dict(failing), len(verdict_mismatch), tcs if unit == "nb3sn" else "")
    rc.write_json(report, rc.RESULTS / "tolerance_diagnostic.json")
