"""Step 10 (baselines): every channel of the three pinned baseline points against the oracle under the r5a clause.

The reference arm executes only its pinned point, and the REBCO pinned point is the basis bridge; verify_all.py covers
the declared cases of the material stores. This compares every published non-constant channel of
results/baseline_result_<unit>.json with the oracle (evaluate_reference_case for the reference, evaluate_material_case
for the material units) and writes results/verification_baselines.json.

    .codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" exec python <record>/verify_baselines.py'
"""
from __future__ import annotations

import json

import record_common as rc
from verify_all import agree

if __name__ == "__main__":
    oracle = rc.oracle()
    out = {}
    for unit in rc.UNITS:
        b = json.loads((rc.RESULTS / f"baseline_result_{unit}.json").read_text())
        channels = oracle.evaluate_full(b["point"])["channels"]
        constants = set(oracle.constant_channels(unit))
        worst, bad, uncovered, compared = (0.0, None), [], [], 0
        for name, value in b["channels"].items():
            if name in constants:
                continue
            if name not in channels:
                uncovered.append(name)
                continue
            ok, rel, err = agree(value, channels[name])
            compared += 1
            if rel > worst[0]:
                worst = (rel, name)
            if not ok:
                bad.append({"channel": name, "package": value, "oracle": channels[name], "relative": rel, "absolute": err})
        out[unit] = {"compared": compared, "uncovered": sorted(uncovered), "disagreements": bad,
                     "worst_relative": {"value": worst[0], "channel": worst[1]}}
        print(unit, compared, "compared,", len(bad), "disagreements, uncovered", len(uncovered), "worst", worst)
    rc.write_json({"rule": "|d| <= max(1e-9 |oracle|, 1e-9) (r5a)", "units": out,
                   "outcome": "pass" if not any(u["disagreements"] for u in out.values()) else "fail"},
                  rc.RESULTS / "verification_baselines.json")
