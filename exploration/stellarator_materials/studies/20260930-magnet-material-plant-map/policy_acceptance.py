"""Step 10 (policy acceptance, contract r5 section 5; design section 6.2): run the acceptance tests on every recorded
design, on the package's own recorded values (the study evaluated each supplied design without the policy).

Recorded designs are the offer policy's reference and companion offers, first pass and design variants (889). For
each, from results/cases_<unit>.json (the store's export):

1. reproduction: the package reproduces the policy's recorded p_fus, p_aux_required, B_peak and beta, every recorded
   expectation channel and the violated-verdict list, under the r5a clause (1e-9 relative or 1e-9 absolute); and the
   contract's own looser tolerances (p_fus 0.5 %, B_peak 0.1 T) are reported beside it;
2. matched designs within 0.5 % of the pinned 2,652.56 MW (power-short designs below it); own-sized designs within
   0.1 T of their target;
3. re-supplied quantities equal the package channels they were read from (design D18): heating rule, structure-mass
   rule, cryo list ratings, the 22 power classes (under the r5a clause: the policy read the oracle's powers, the
   package recomputes them to the last bits; bit-identical matches are counted beside), every screened rating at 1.05 x demand, offered states, purchased
   masses, purchase costs at exponent 0.7, the IHX count rule and the cooling facilities that follow it;
4. MR-7: every insufficient offer fails `acceptance_ok`, every generous offer at a supported field passes it (package
   verdicts); equal-duty REBCO designs carry their Nb3Sn pair's turns and current exactly.

The rules are imported from studies/offer_policy.py (its published constants and helpers); no rule is restated here.
Writes results/policy_acceptance.json.

    .codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" exec python <record>/policy_acceptance.py'
"""
from __future__ import annotations

import json
import math
from collections import Counter

import record_common as rc
from exploration.stellarator_materials import oracle_glue as og
from exploration.stellarator_materials.studies import offer_policy as op
from exploration.stellarator_materials.studies.interface_data import INTERFACE

REL, ABS = 1e-9, 1e-9


def close(a, b, rel=REL, abs_=ABS) -> bool:
    a, b = float(a), float(b)
    if not (math.isfinite(a) and math.isfinite(b)):
        return (math.isnan(a) and math.isnan(b)) or a == b
    return abs(a - b) <= max(rel * abs(b), abs_)


def main():
    declared = {c["case_id"]: c for c in rc.load_cases()["cases"]}
    rows = {}
    for unit in rc.MATERIALS:
        for r in json.loads((rc.RESULTS / f"cases_{unit}.json").read_text())["cases"]:
            rows[r["case_id"]] = r
    failures, counts = [], Counter()
    worst = {"p_fus_rel": 0.0, "p_aux_abs": 0.0, "B_peak_abs": 0.0}

    def check(name, ok, case_id, detail=None):
        counts[(name, bool(ok))] += 1
        if not ok:
            failures.append({"check": name, "case_id": case_id, "detail": detail})

    designs = [c for c in declared.values() if c["labels"]["offer_kind"] in ("reference", "companion")
               and c.get("expected") and (c["labels"]["variant"] == "none" or c["labels"]["variant"] in op.DESIGN_VARIANTS)]
    for c in designs:
        unit = c["labels"]["material"]
        P = INTERFACE["units"][unit]["prefix"]
        r = rows[c["case_id"]]
        check("evaluated", r["state"] == "completed", c["case_id"], r.get("refusal"))
        if r["state"] != "completed":
            continue
        ch = {k[len(P):]: v for k, v in r["outputs"].items()}
        d = {k[len(P):]: v for k, v in c["inputs"].items()}
        exp = c["expected"]
        for rec, channel in (("p_fus", "plasma__fusion__p_fus"), ("p_aux_required", "plasma__sustain__p_aux_required"),
                             ("B_peak", "magnet__peak_field_calc__B_peak"), ("beta", "plasma__beta_calc__beta")):
            check(f"reproduces {rec} (r5a clause)", close(ch[channel], exp[rec]), c["case_id"], [ch[channel], exp[rec]])
        worst["p_fus_rel"] = max(worst["p_fus_rel"], abs(ch["plasma__fusion__p_fus"] / exp["p_fus"] - 1.0))
        worst["p_aux_abs"] = max(worst["p_aux_abs"], abs(ch["plasma__sustain__p_aux_required"] - exp["p_aux_required"]))
        worst["B_peak_abs"] = max(worst["B_peak_abs"], abs(ch["magnet__peak_field_calc__B_peak"] - exp["B_peak"]))
        check("reproduces p_fus within 0.5 %", abs(ch["plasma__fusion__p_fus"] / exp["p_fus"] - 1.0) <= op.TOL_P_FUS,
              c["case_id"])
        check("reproduces B_peak within 0.1 T", abs(ch["magnet__peak_field_calc__B_peak"] - exp["B_peak"]) <= op.TOL_B_PEAK,
              c["case_id"])
        for channel, value in exp["channels"].items():
            check("reproduces recorded channel (r5a clause)", close(ch[channel], value), c["case_id"], channel)
        violated = sorted(("magnet__" if k in ("acceptance_ok", "copper_ok", "steel_ok", "pack_area_ok", "ampere_floor_ok")
                           else "cryoplant__" if k == "capacity_ok" else "") + k
                          for k, s in r["verdicts"].items() if s != "satisfied")
        check("reproduces violated-verdict list", violated == exp["violated"], c["case_id"], [violated, exp["violated"]])
        p_fus = ch["plasma__fusion__p_fus"]
        if c["policy"]["power_short"]:
            check("power-short below matched power", p_fus < op.P_FUS_MATCH * (1.0 + op.TOL_P_FUS), c["case_id"], p_fus)
        else:
            check("matched power within 0.5 %", abs(p_fus / op.P_FUS_MATCH - 1.0) <= op.TOL_P_FUS, c["case_id"], p_fus)
        if not c["labels"]["equal_duty"]:
            err = ch["magnet__peak_field_calc__B_peak"] - c["labels"]["B_peak_target"]
            check("own-sized B_peak within 0.1 T of target", abs(err) <= op.TOL_B_PEAK, c["case_id"], err)
        # D18 read-back on the package's channels
        check("heating rule", d["heating__p_wallplug_heat"] == op.heating_rule(ch["plasma__sustain__p_aux_required"]),
              c["case_id"])
        check("structure-mass rule", close(d["magnet__m_support"], og.structure_mass_rule(ch["magnet__stored_energy__W_mag"]),
                                           rel=1e-12, abs_=0.0), c["case_id"])
        check("cold rating from list", d["cryoplant__rated_cold_W"] == op.list_rating(ch["cryoplant__cold_stage__q_cold"])[0],
              c["case_id"])
        check("intercept rating from list",
              d["cryoplant__rated_intercept_W"] == op.list_rating(ch["cryoplant__cold_stage__q_shield"])[0], c["case_id"])
        for key, channel in op.CLASS_MAP.items():
            # The policy set each class from the oracle's power; the package's recomputed power can differ at the
            # last bits, so the read-back uses the r5a clause and the exact-equality misses are counted beside it.
            check("power class (r5a clause)", close(d[key], max(ch[channel], 0.0)), c["case_id"], key)
            counts[("power class bit-identical (information)", d[key] == max(ch[channel], 0.0))] += 1
        for key, margin in op.SCREENED_RATINGS:
            if ch[margin.replace("__margin", "__applicable")] != 1.0:
                continue
            check("screened rating at 1.05 x demand", close(d[key], op.PACKAGE_MARGIN * (d[key] - ch[margin]), abs_=1e-12),
                  c["case_id"], key)
        for key, channel in op.OFFERED_STATES:
            check("offered state", d[key] == ch[channel], c["case_id"], key)
        for key, channel in op.PURCHASED_MASSES:
            check("purchased mass", close(d[key], op.PACKAGE_MARGIN * ch[channel]), c["case_id"], key)
        for name, (purchase, rating) in op.PURCHASES.items():
            expected = op.PIN[purchase] if rating is None else \
                op.PIN[purchase] * (d[rating] / op.PIN[rating]) ** op.PURCHASE_EXPONENT
            check("purchase cost at exponent 0.7", close(d[purchase], expected), c["case_id"], name)
        n = d[op.IHX_COUNT_KEY]
        req, inst = ch["heat_transport__equipment__ihx_required_area"], ch["heat_transport__equipment__ihx_installed_area"]
        floor = c["policy"]["trace"]["ihx_floor"]
        check("IHX count rule", n == int(n) >= 1 and op.PACKAGE_MARGIN * req <= inst
              and n == max(math.ceil(op.PACKAGE_MARGIN * n * req / inst - 1e-9), floor, 1), c["case_id"], [n, req, inst])
        check("cooling hall follows IHX count", close(d["buildings__selected_cooling_hall_length"],
                                                     op.PACKAGE_MARGIN * ch["buildings__layout__cooling_hall_required_length"]),
              c["case_id"])
        for state in ("clean", "dirty"):
            for kind in op.COOLING_KINDS:
                check("cooling spare positions", d[f"buildings__cooling_{state}_{kind}_positions"] == math.ceil(
                    op.PACKAGE_MARGIN * ch[f"buildings__layout__cooling_{state}_{kind}_required"] - 1e-9), c["case_id"])
        check("magnet sized to its checks", ch["magnet__conductor__acceptance_margin"] >= 0.0
              and ch["magnet__area__fit_margin"] >= 0.0 and ch["magnet__wp_fit__minimum_margin"] >= 0.0, c["case_id"])
    # MR-7 offers, on the package's verdicts
    for c in declared.values():
        kind = c["labels"]["offer_kind"]
        if kind not in ("insufficient", "generous"):
            continue
        r = rows[c["case_id"]]
        if r["state"] != "completed":
            check(f"MR-7 {kind} evaluated", False, c["case_id"], r.get("refusal"))
            continue
        P = INTERFACE["units"][c["labels"]["material"]]["prefix"]
        if kind == "insufficient":
            check("MR-7 insufficient fails acceptance_ok", r["verdicts"]["acceptance_ok"] == "violated", c["case_id"])
        elif r["outputs"][P + "magnet__conductor__status_code"] != 0.0:
            check("MR-7 generous passes acceptance_ok", r["verdicts"]["acceptance_ok"] == "satisfied", c["case_id"])
    # equal-duty pairs (inputs)
    nb = {}
    for c in declared.values():
        lb = c["labels"]
        if lb["material"] == "nb3sn" and lb["offer_kind"] == "reference" and c["inputs"] and \
                (lb["variant"] == "none" or lb["variant"] in op.DESIGN_VARIANTS):
            P = INTERFACE["units"]["nb3sn"]["prefix"]
            nb[(lb["cell_geometry"], lb["cell_f_ren"], lb["B_peak_target"], lb["R"], lb["a"], lb["variant"])] = \
                (c["inputs"][P + "magnet__coil__reference_turns"], c["inputs"][P + "magnet__coil__turn_current"])
    for c in declared.values():
        lb = c["labels"]
        if lb["material"] == "rebco" and lb["equal_duty"] and lb["offer_kind"] == "reference" and c["inputs"] and \
                (lb["variant"] == "none" or lb["variant"] in op.DESIGN_VARIANTS):
            P = INTERFACE["units"]["rebco"]["prefix"]
            variant = lb["variant"] if lb["variant"] != "common-P" else "none"
            pair = nb[(lb["cell_geometry"], lb["cell_f_ren"], lb["B_peak_target"], lb["R"], lb["a"], variant)]
            check("equal-duty pair shares turns and current",
                  (c["inputs"][P + "magnet__coil__reference_turns"], c["inputs"][P + "magnet__coil__turn_current"]) == pair,
                  c["case_id"])
    by_check = {}
    for (name, ok), n in counts.items():
        by_check.setdefault(name, {"pass": 0, "fail": 0})["pass" if ok else "fail"] += n
    document = {"recorded_designs": len(designs), "checks": dict(sorted(by_check.items())), "worst": worst,
                "failures": failures, "outcome": "pass" if not failures else "fail",
                "policy_sha256": rc.sha256(rc.PACKAGE_STUDIES / "offer_policy.py")}
    rc.write_json(document, rc.RESULTS / "policy_acceptance.json")
    print({"recorded_designs": len(designs), "outcome": document["outcome"], "failures": len(failures), "worst": worst})
    for f in failures[:10]:
        print(" ", f)


if __name__ == "__main__":
    main()
