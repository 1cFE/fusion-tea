"""Contract r5 section 8 (F15): verify each solved break-even REBCO price with one evaluation at that price.

For every break-even in results/summary.json (base cells and design-variant cells) whose solved price is
non-negative, the REBCO design that sets it is evaluated once more at the solved price through the package route
(store results/native/breakeven/; the same REBCO unit and CANDIDATE) and with the oracle. The check: the package's LCOE
at the solved price equals the best Nb3Sn LCOE it was solved against (the affine law), and package and oracle agree
under the r5a clause. A negative solved price is recorded and not evaluated (no physical price). Writes
results/breakeven_verification.json.

    .codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" exec python <record>/breakeven_verify.py'
"""
from __future__ import annotations

import json

import record_common as rc
from oracle_scan import proposal
from verify_all import agree
from exploration.stellarator_materials.studies import study_route as route
from exploration.stellarator_materials.studies.interface_data import INTERFACE
from scripts.study import common

P = INTERFACE["units"]["rebco"]["prefix"]
PRICE = P + "magnet__element_price_per_m"
LCOE = P + "lcoe_calc__lcoe"


if __name__ == "__main__":
    summary = json.loads((rc.RESULTS / "summary.json").read_text())
    declared = {c["case_id"]: c for c in rc.load_cases()["cases"]}
    targets = []
    for scope, entries in (("cell", summary["cells"]), ("design_variant", summary["design_variants"])):
        for key, entry in entries.items():
            be = entry.get("breakeven")
            if be:
                targets.append({"scope": scope, "key": key, "design": be["at_design"], "price": be["breakeven_USD_m"],
                                "best_nb3sn": be["best_nb3sn"], "target_lcoe": be["best_nb3sn_lcoe"]})
    runnable = [t for t in targets if t["price"] >= 0.0]
    proposals = []
    for t in runnable:
        p = proposal(declared[t["design"]])
        p[PRICE] = t["price"]
        proposals.append(p)
    common.assert_tree_clean(route.unit_of("rebco").package_dir)
    cases, db = route.run_points("rebco", f"{rc.STUDY_ID}-breakeven", proposals, rc.NATIVE / "breakeven")
    common.assert_tree_clean(route.unit_of("rebco").package_dir)
    oracle = rc.oracle()
    by_price = {(json.dumps({k: v for k, v in dict(c.inputs).items() if k != PRICE}, sort_keys=True),
                 float(dict(c.inputs)[PRICE])): c for c in cases}
    validate = route.proposal_validator("rebco")
    rows = []
    for t, p in zip(runnable, proposals):
        v = validate(p)
        c = by_price[(json.dumps({k: x for k, x in v.items() if k != PRICE}, sort_keys=True), float(v[PRICE]))]
        o = oracle.evaluate_full(dict(c.inputs))
        ok_all = all(agree(val, o["channels"][ch])[0] for ch, val in c.outputs.items() if ch in o["channels"]
                     and ch not in oracle.constant_channels("rebco"))
        L = c.outputs[LCOE]
        rows.append({**t, "candidate_id": c.candidate_id, "state": c.state, "lcoe_at_price": L,
                     "relative_gap_to_target": (L - t["target_lcoe"]) / abs(t["target_lcoe"]),
                     "oracle_lcoe": o["channels"][LCOE], "oracle_agrees_all_channels": ok_all})
    skipped = [dict(t, reason="negative solved price; not a physical price, not evaluated") for t in targets
               if t["price"] < 0.0]
    document = {"store": common.manifest_mod.repo_relative_posix(db), "evaluated": rows, "not_evaluated": skipped,
                "max_abs_relative_gap": max((abs(r["relative_gap_to_target"]) for r in rows), default=None),
                "all_oracle_agree": all(r["oracle_agrees_all_channels"] for r in rows)}
    rc.write_json(document, rc.RESULTS / "breakeven_verification.json")
    print({k: document[k] for k in ("max_abs_relative_gap", "all_oracle_agree")}, len(rows), "evaluated,",
          len(skipped), "negative")
