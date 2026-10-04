"""Steps 9/13: factual summary of the executed and verified study, from the stores' exports only.

Reads results/cases_<unit>.json (package values), the declared case labels and results/baseline_result_<unit>.json.
Every number traces to a stored case id. Statuses and flags are re-derived from the package's recorded verdicts,
inputs and channels (statuses.py, contract r5 section 7). No interpretation; the goal-level reading is the
coordinator's. Writes results/summary.json and results/cases.csv.

Definitions ([AGENT] where the contract leaves a choice):
* base designs of a cell: the offer policy's reference and companion offers with variant `none` (REBCO 80 USD/m,
  Nb3Sn 8 USD/m); design variants and re-evaluations are reported separately;
* best supported design per material and cell: the supported base design with the lowest LCOE (contract section 7);
  the best divertor-passing supported design beside it (section 8); with no supported design, the nearest design:
  the lowest-LCOE non-supported base design with positive net power (policy-notes Q15's rule);
* LCOE decomposition (section 8 groups): oracle_glue.lcoe_breakdown applied to the package's recorded channels; a
  REBCO - Nb3Sn difference is split exactly into per-group capital and annual terms at the REBCO design's energy plus
  one net-electricity (denominator) term, LCOE_Nb3Sn x (E_Nb3Sn / E_REBCO - 1);
* break-even REBCO price (section 8, F15): LCOE is affine in the tape price at a fixed design, so each supported base
  REBCO design's slope is measured from its evaluations at 80 and 30 USD/m; the cell's break-even price is the highest
  price at which some supported REBCO design reaches the best Nb3Sn LCOE; the 10 USD/m evaluation checks the affine
  law on every design, and one package evaluation at the solved price (breakeven_verify.py) verifies each crossing.
"""
from __future__ import annotations

import csv
import json
import math
from collections import Counter, defaultdict

import record_common as rc
import statuses as st
from exploration.stellarator_materials import oracle_glue as og
from exploration.stellarator_materials.studies.interface_data import INTERFACE

CELLS = [(g, f) for g in ("anchored", "helias", "arm") for f in (1.0, 1.4, 1.8)]
GROUP_ORDER = list(og.CAPITAL_GROUPS) + list(og.ANNUAL_GROUPS)
KEY = {"lcoe": "lcoe_calc__lcoe", "p_net": "pb__p_net", "p_fus": "plasma__fusion__p_fus",
       "p_aux": "plasma__sustain__p_aux_required", "B_peak": "magnet__peak_field_calc__B_peak",
       "beta": "plasma__beta_calc__beta", "W_mag": "magnet__stored_energy__W_mag",
       "cryo_MW": "cryoplant__refrigeration__p_in_total_MW", "heat_MW": "operating_heat__p_wallplug",
       "total_capital": "total_capital__total_capital"}
DESIGN_INPUTS = ("plasma__R", "plasma__a", "plasma__T_i0", "plasma__n_e0", "magnet__coil__reference_turns",
                 "magnet__coil__turn_current", "magnet__n_elements", "magnet__winding_pack__wp_side",
                 "magnet__coil__coil_t", "magnet__m_support", "heating__p_wallplug_heat", "cryoplant__rated_cold_W",
                 "magnet__element_price_per_m")


def load():
    declared = {c["case_id"]: c for c in rc.load_cases()["cases"]}
    rows = {}
    for unit in rc.MATERIALS:
        U = INTERFACE["units"][unit]
        P = U["prefix"]
        defaults = {k[len(P):]: v for k, v in U["baseline_point"].items()}
        for r in json.loads((rc.RESULTS / f"cases_{unit}.json").read_text())["cases"]:
            c = declared[r["case_id"]]
            inputs = dict(defaults, **{k[len(P):]: v for k, v in r["inputs"].items()})
            op_class = st.operating_point_class(c, declared)
            row = {"case_id": r["case_id"], "unit": unit, "labels": r["labels"], "candidate_id": r["candidate_id"],
                   "state": r["state"], "refusal": r["refusal"], "op_class": op_class, "inputs": inputs,
                   "base_case": (c.get("policy") or {}).get("base_case")}
            if r["state"] == "completed":
                ch = {k[len(P):]: v for k, v in r["outputs"].items()}
                row["ch"] = ch
                row["verdicts"] = r["verdicts"]
                row["status"], row["reasons"] = st.status(unit, None, ch, r["verdicts"], inputs, op_class)
                row["flags"] = st.flags(unit, ch, r["verdicts"], inputs, c)
                row["flags"]["free_capacity"] = (c.get("flags") or {}).get("free_capacity")
            else:
                row["status"], row["reasons"] = st.status(unit, r["refusal"] or "execution_failed", None, None, {}, op_class)
            rows[r["case_id"]] = row
    return declared, rows


def is_base(r):
    return r["labels"]["variant"] == "none" and r["labels"]["offer_kind"] in ("reference", "companion")


def design_view(r) -> dict:
    out = {"case_id": r["case_id"], "status": r["status"], "reasons": r["reasons"],
           "offer_kind": r["labels"]["offer_kind"], "B_peak_target": r["labels"]["B_peak_target"],
           "equal_duty": r["labels"]["equal_duty"], "T_i0_ladder": r["labels"]["T_i0_ladder"]}
    if "ch" in r:
        out.update({k: r["ch"][v] for k, v in KEY.items()})
        out["inputs"] = {k: r["inputs"][k] for k in DESIGN_INPUTS}
        out["flags"] = {k: v for k, v in r["flags"].items() if k != "free_capacity"}
        out["free_capacity_count"] = len(r["flags"].get("free_capacity") or [])
    return out


def breakdown(r) -> dict:
    return og.lcoe_breakdown(r["ch"], r["inputs"])


def difference(rebco, nb3sn) -> dict:
    """Exact split of LCOE(REBCO) - LCOE(Nb3Sn) into group terms at REBCO's energy plus a denominator term."""
    br, bn = breakdown(rebco), breakdown(nb3sn)
    ratio = bn["energy_MWh"] / br["energy_MWh"]
    terms = {g: br["contributions"][g] - bn["contributions"][g] * ratio for g in GROUP_ORDER}
    terms["net_electricity_denominator"] = bn["lcoe_sum"] * (ratio - 1.0)
    total = math.fsum(terms.values())
    return {"lcoe_difference": rebco["ch"][KEY["lcoe"]] - nb3sn["ch"][KEY["lcoe"]], "terms": terms,
            "terms_sum": total, "closure": {"rebco": br["relative_residual"], "nb3sn": bn["relative_residual"]},
            "p_net_MW": [rebco["ch"]["pb__p_net"], nb3sn["ch"]["pb__p_net"]],
            "cryo_electricity_MW": [rebco["ch"][KEY["cryo_MW"]], nb3sn["ch"][KEY["cryo_MW"]]],
            "heating_wallplug_MW": [rebco["ch"][KEY["heat_MW"]], nb3sn["ch"][KEY["heat_MW"]]]}


def best(rows, pred):
    cands = [r for r in rows if pred(r)]
    return min(cands, key=lambda r: r["ch"][KEY["lcoe"]]) if cands else None


def nearest(rows):
    cands = [r for r in rows if r["status"] != "supported" and "ch" in r and r["ch"]["pb__p_net"] > 0]
    return min(cands, key=lambda r: r["ch"][KEY["lcoe"]]) if cands else None


def price_variants(rows_by_id, declared):
    """base case id -> {price variant label: row} for REBCO re-evaluations."""
    out = defaultdict(dict)
    for r in rows_by_id.values():
        v = r["labels"]["variant"]
        if r["unit"] == "rebco" and r["base_case"] and (v.endswith("price_30") or v.endswith("price_10")
                                                        or v == "cpi_2021_2026"):
            out[r["base_case"]][v.split("+")[-1]] = r
    return out


def breakeven(rebco_rows, nb_best, pv):
    """Per supported REBCO design: slope from 80 and 30; crossing with the best Nb3Sn LCOE; affine check at 10."""
    if nb_best is None:
        return None
    L_N = nb_best["ch"][KEY["lcoe"]]
    per = []
    for r in rebco_rows:
        v = pv.get(r["case_id"], {})
        if "price_30" not in v or "ch" not in v["price_30"]:
            continue
        L80, L30 = r["ch"][KEY["lcoe"]], v["price_30"]["ch"][KEY["lcoe"]]
        p80, p30 = r["inputs"]["magnet__element_price_per_m"], v["price_30"]["inputs"]["magnet__element_price_per_m"]
        slope = (L80 - L30) / (p80 - p30)
        crossing = p80 + (L_N - L80) / slope
        affine = None
        if "price_10" in v and "ch" in v["price_10"]:
            p10 = v["price_10"]["inputs"]["magnet__element_price_per_m"]
            predicted = L80 + slope * (p10 - p80)
            affine = (v["price_10"]["ch"][KEY["lcoe"]] - predicted) / abs(v["price_10"]["ch"][KEY["lcoe"]])
        per.append({"case_id": r["case_id"], "slope_per_USD_m": slope, "crossing_USD_m": crossing,
                    "lcoe": {"80": L80, "30": L30, "10": v.get("price_10", {}).get("ch", {}).get(KEY["lcoe"])},
                    "affine_residual_at_10": affine})
    if not per:
        return None
    top = max(per, key=lambda e: e["crossing_USD_m"])
    reselect = {}
    for label, price_key in (("80", None), ("30", "price_30"), ("10", "price_10")):
        cand = []
        for r in rebco_rows:
            rr = r if price_key is None else pv.get(r["case_id"], {}).get(price_key)
            if rr is not None and "ch" in rr:
                cand.append((rr["ch"][KEY["lcoe"]], r["case_id"]))
        if cand:
            L, cid = min(cand)
            reselect[label] = {"best_rebco": cid, "lcoe": L, "gap_vs_best_nb3sn": L - L_N,
                               "winner": "REBCO" if L < L_N else "Nb3Sn"}
    return {"best_nb3sn": nb_best["case_id"], "best_nb3sn_lcoe": L_N, "breakeven_USD_m": top["crossing_USD_m"],
            "at_design": top["case_id"], "designs": sorted(per, key=lambda e: -e["crossing_USD_m"]),
            "max_abs_affine_residual_at_10": max((abs(e["affine_residual_at_10"]) for e in per
                                                  if e["affine_residual_at_10"] is not None), default=None),
            "reselection": reselect}


def main():
    declared, rows = load()
    all_rows = list(rows.values())
    counts = {
        "by_status": dict(Counter(r["status"] for r in all_rows)),
        "by_material": {u: dict(Counter(r["status"] for r in all_rows if r["unit"] == u)) for u in rc.MATERIALS},
        "by_cell_material": {f"{g}|{f}|{u}": dict(Counter(r["status"] for r in all_rows if r["unit"] == u
                                                          and r["labels"]["cell_geometry"] == g and r["labels"]["cell_f_ren"] == f))
                             for g, f in CELLS for u in rc.MATERIALS},
        "by_offer_kind": {f"{u}|{k}": dict(Counter(r["status"] for r in all_rows if r["unit"] == u
                                                   and r["labels"]["offer_kind"] == k))
                          for u in rc.MATERIALS for k in ("reference", "companion", "insufficient", "generous")},
        "by_variant": {f"{u}|{v}": dict(Counter(r["status"] for r in all_rows if r["unit"] == u and r["labels"]["variant"] == v))
                       for u in rc.MATERIALS for v in sorted({r["labels"]["variant"] for r in all_rows})},
        "refusals": [{"case_id": r["case_id"], "text": r["refusal"]} for r in all_rows if r["state"] != "completed"],
    }
    counts["by_variant"] = {k: v for k, v in counts["by_variant"].items() if v}
    near = defaultdict(Counter)
    flag_counts = defaultdict(Counter)
    for r in all_rows:
        if "ch" not in r:
            continue
        for name in st.near_threshold(r["unit"], r["ch"], r["inputs"]):
            near[r["unit"]][name] += 1
        for name, value in r["flags"].items():
            if name == "power_short":
                flag_counts[r["unit"]][name] += int(bool(value))
            elif isinstance(value, bool):
                flag_counts[r["unit"]][name] += int(value)
        failed_checks = r["reasons"] if r["status"] in ("failed", "capacity-limited") else []
        for name in failed_checks:
            flag_counts[r["unit"]]["fails:" + name] += 1
    counts["near_threshold"] = {u: dict(c) for u, c in near.items()}
    counts["flags_and_failed_checks"] = {u: dict(sorted(c.items())) for u, c in flag_counts.items()}

    pv = price_variants(rows, declared)
    cells = {}
    for g, f in CELLS:
        cell = {}
        base = {u: [r for r in all_rows if r["unit"] == u and is_base(r) and r["labels"]["cell_geometry"] == g
                    and r["labels"]["cell_f_ren"] == f] for u in rc.MATERIALS}
        for u in rc.MATERIALS:
            b = best(base[u], lambda r: r["status"] == "supported")
            bd = best(base[u], lambda r: r["status"] == "supported" and r["flags"]["divertor_pass"])
            cell[u] = {"best_supported": design_view(b) if b else None,
                       "best_supported_divertor_pass": design_view(bd) if bd else None,
                       "supported": sum(r["status"] == "supported" for r in base[u]),
                       "supported_divertor_pass": sum(r["status"] == "supported" and r["flags"]["divertor_pass"]
                                                      for r in base[u]),
                       "nearest_if_none": design_view(nearest(base[u])) if b is None and nearest(base[u]) else None}
            cell[u]["_best_row"] = b
            cell[u]["_best_div_row"] = bd
        R, N = cell["rebco"]["_best_row"], cell["nb3sn"]["_best_row"]
        if R and N:
            cell["comparison"] = {"winner_at_80": "REBCO" if R["ch"][KEY["lcoe"]] < N["ch"][KEY["lcoe"]] else "Nb3Sn",
                                  **difference(R, N)}
        else:
            cell["comparison"] = {"winner_at_80": None, "note": "no supported design for " +
                                  " and ".join(u for u in rc.MATERIALS if not cell[u]["_best_row"])}
        Rd, Nd = cell["rebco"]["_best_div_row"], cell["nb3sn"]["_best_div_row"]
        if Rd and Nd:
            cell["comparison_divertor_pass"] = {
                "winner_at_80": "REBCO" if Rd["ch"][KEY["lcoe"]] < Nd["ch"][KEY["lcoe"]] else "Nb3Sn",
                "lcoe_difference": Rd["ch"][KEY["lcoe"]] - Nd["ch"][KEY["lcoe"]]}
        supported_rebco = [r for r in base["rebco"] if r["status"] == "supported"]
        cell["breakeven"] = breakeven(supported_rebco, N, pv)
        cpi = {u: best([r for r in all_rows if r["unit"] == u and r["labels"]["variant"] == "cpi_2021_2026"
                        and r["labels"]["cell_geometry"] == g and r["labels"]["cell_f_ren"] == f],
                       lambda r: r["status"] == "supported") for u in rc.MATERIALS}
        if cpi["rebco"] and cpi["nb3sn"]:
            cell["cpi_2021_2026"] = {"best_rebco": cpi["rebco"]["case_id"], "best_nb3sn": cpi["nb3sn"]["case_id"],
                                     "lcoe": [cpi["rebco"]["ch"][KEY["lcoe"]], cpi["nb3sn"]["ch"][KEY["lcoe"]]],
                                     "winner": "REBCO" if cpi["rebco"]["ch"][KEY["lcoe"]] < cpi["nb3sn"]["ch"][KEY["lcoe"]] else "Nb3Sn"}
        for u in rc.MATERIALS:
            cell[u].pop("_best_row"), cell[u].pop("_best_div_row")
        cells[f"{g}|{f}"] = cell

    # design variants: best supported per material among each variant's own designs, per cell, with price re-evaluations
    variants = {}
    for v in ("k_link_0.95", "turn_current_86kA", "common-P", "strain_-0.6"):
        for g, f in CELLS:
            vr = {u: [r for r in all_rows if r["unit"] == u and r["labels"]["variant"] == v
                      and r["labels"]["offer_kind"] in ("reference", "companion")
                      and r["labels"]["cell_geometry"] == g and r["labels"]["cell_f_ren"] == f] for u in rc.MATERIALS}
            if not (vr["rebco"] or vr["nb3sn"]):
                continue
            entry = {}
            for u in rc.MATERIALS:
                b = best(vr[u], lambda r: r["status"] == "supported")
                entry[u] = {"designs": len(vr[u]), "statuses": dict(Counter(r["status"] for r in vr[u])),
                            "best_supported": design_view(b) if b else None}
            # compare against the variant's own Nb3Sn best, or the base Nb3Sn best where the variant is REBCO-only
            nb = best(vr["nb3sn"], lambda r: r["status"] == "supported")
            if not vr["nb3sn"]:
                nb = best([r for r in all_rows if r["unit"] == "nb3sn" and is_base(r) and r["labels"]["cell_geometry"] == g
                           and r["labels"]["cell_f_ren"] == f], lambda r: r["status"] == "supported")
                entry["nb3sn_reference_for_comparison"] = "base best supported Nb3Sn design (variant is REBCO-only)"
            entry["breakeven"] = breakeven([r for r in vr["rebco"] if r["status"] == "supported"], nb, pv)
            variants[f"{v}|{g}|{f}"] = entry
    # re-evaluation variants on held designs
    reevals = []
    for r in all_rows:
        v = r["labels"]["variant"]
        if v in ("m_support_x0.5", "m_support_x2", "purchase_exp_0.5", "purchase_exp_1.0", "nb3sn_price_5.4",
                 "nb3sn_price_13.5") and "ch" in r:
            b = rows[r["base_case"]]
            reevals.append({"case_id": r["case_id"], "variant": v, "base_case": r["base_case"], "status": r["status"],
                            "base_status": b["status"], "lcoe": r["ch"][KEY["lcoe"]],
                            "base_lcoe": b["ch"][KEY["lcoe"]] if "ch" in b else None})

    # equal-duty pairs (base, same cell, field target and size)
    nb_index = {(r["labels"]["cell_geometry"], r["labels"]["cell_f_ren"], r["labels"]["B_peak_target"], r["labels"]["R"],
                 r["labels"]["a"]): r for r in all_rows if r["unit"] == "nb3sn" and is_base(r)
                and r["labels"]["offer_kind"] == "reference"}
    pairs = []
    for r in all_rows:
        lb = r["labels"]
        if r["unit"] == "rebco" and is_base(r) and lb["equal_duty"] and lb["offer_kind"] == "reference":
            n = nb_index.get((lb["cell_geometry"], lb["cell_f_ren"], lb["B_peak_target"], lb["R"], lb["a"]))
            if n is None:
                continue
            e = {"rebco": r["case_id"], "nb3sn": n["case_id"], "statuses": [r["status"], n["status"]],
                 "B_peak": [r["ch"][KEY["B_peak"]] if "ch" in r else None, n["ch"][KEY["B_peak"]] if "ch" in n else None]}
            if "ch" in r and "ch" in n and r["ch"]["pb__p_net"] > 0 and n["ch"]["pb__p_net"] > 0:
                e.update(difference(r, n))
                e["same_operating_point"] = (r["inputs"]["plasma__T_i0"], r["inputs"]["plasma__n_e0"]) == \
                    (n["inputs"]["plasma__T_i0"], n["inputs"]["plasma__n_e0"])
            pairs.append(e)
    both_supported = [p for p in pairs if p["statuses"] == ["supported", "supported"]]
    magnet_groups = ("conductor_purchase", "other_winding_materials_and_operations", "structure", "refrigeration_capital")
    def mean_terms(sel):
        return {g: math.fsum(p["terms"][g] for p in sel) / len(sel) for g in GROUP_ORDER + ["net_electricity_denominator"]} if sel else None
    same_op = [p for p in both_supported if p.get("same_operating_point")]
    equal_duty_terms = {
        "mean_terms_both_supported": mean_terms(both_supported),
        "both_supported_same_operating_point": len(same_op),
        "max_abs_non_magnet_share_same_operating_point": max(
            (abs(p["lcoe_difference"] - math.fsum(p["terms"][g] for g in magnet_groups)) / abs(p["lcoe_difference"])
             for p in same_op), default=None),
    }
    equal_duty = {"pairs": len(pairs), "both_supported": len(both_supported), **equal_duty_terms,
                  "rebco_cheaper_both_supported": sum(p["lcoe_difference"] < 0 for p in both_supported),
                  "lcoe_difference_both_supported": sorted(p["lcoe_difference"] for p in both_supported),
                  "same_operating_point": sum(bool(p.get("same_operating_point")) for p in pairs),
                  "pairs_detail": pairs}

    # own highest field on the reference coil set: anchored x 1.0 at (12.7, 1.3)
    def find(unit, target):
        return next((r for r in all_rows if r["unit"] == unit and is_base(r) and r["labels"]["offer_kind"] == "reference"
                     and r["labels"]["cell_geometry"] == "anchored" and r["labels"]["cell_f_ren"] == 1.0
                     and r["labels"]["B_peak_target"] == target and (r["labels"]["R"], r["labels"]["a"]) == (12.7, 1.3)), None)
    hr, hn = find("rebco", 24.9), find("nb3sn", 12.0)
    own_highest = {"rebco": design_view(hr), "nb3sn": design_view(hn)}
    if hr and hn and "ch" in hr and "ch" in hn and hr["ch"]["pb__p_net"] > 0 and hn["ch"]["pb__p_net"] > 0:
        own_highest["difference"] = difference(hr, hn)
    else:
        own_highest["difference"] = None
        own_highest["note"] = "no decomposition: a design with non-positive net power has no meaningful LCOE split"

    # basis bridge: reference instance vs REBCO-material instance at the same supplied design
    ref = json.loads((rc.RESULTS / "baseline_result_reference.json").read_text())
    reb = json.loads((rc.RESULTS / "baseline_result_rebco.json").read_text())
    Pr, Pb = INTERFACE["units"]["reference"]["prefix"], INTERFACE["units"]["rebco"]["prefix"]
    rch = {k[len(Pr):]: v for k, v in ref["channels"].items()}
    rin = {k[len(Pr):]: v for k, v in ref["point"].items()}
    bch = {k[len(Pb):]: v for k, v in reb["channels"].items()}
    bin_ = {k[len(Pb):]: v for k, v in reb["point"].items()}
    br_ref = og.lcoe_breakdown(rch, rin, reference=True)
    br_reb = og.lcoe_breakdown(bch, bin_)
    ratio = br_ref["energy_MWh"] / br_reb["energy_MWh"]
    bridge = {"reference_lcoe": rch["lcoe_calc__lcoe"], "rebco_material_lcoe": bch["lcoe_calc__lcoe"],
              "difference": bch["lcoe_calc__lcoe"] - rch["lcoe_calc__lcoe"],
              "terms": {**{g: br_reb["contributions"][g] - br_ref["contributions"][g] * ratio for g in GROUP_ORDER},
                        "net_electricity_denominator": br_ref["lcoe_sum"] * (ratio - 1.0)},
              "capital_groups_USD": {g: [br_ref["capital"][g], br_reb["capital"][g]] for g in og.CAPITAL_GROUPS},
              "p_net_MW": [rch["pb__p_net"], bch["pb__p_net"]],
              "closure": {"reference": br_ref["relative_residual"], "rebco": br_reb["relative_residual"]},
              "count_basis": "REBCO bridge count 1.5 x parallel_tapes_set = 170.609 (amendment A6); the 0.991 = "
                             "f_set/f_wp_vol factor is reported, not absorbed"}

    summary = {"study_id": rc.STUDY_ID, "counts": counts, "cells": cells, "design_variants": variants,
               "reevaluation_variants": reevals, "equal_duty": {k: v for k, v in equal_duty.items() if k != "pairs_detail"},
               "equal_duty_pairs": equal_duty["pairs_detail"], "own_highest_field_reference_coil_set": own_highest,
               "basis_bridge": bridge}
    rc.write_json(summary, rc.RESULTS / "summary.json")
    columns = ["case_id", "unit", "cell_geometry", "cell_f_ren", "B_peak_target", "R", "a", "offer_kind", "variant",
               "equal_duty", "state", "status", "reasons", *KEY, "divertor_pass", "power_short", "arm_extrapolated",
               "extrapolated", "beyond_law_extents", "envelope_flag", "R_over_sqrt_A_wp", "candidate_id"]
    with (rc.RESULTS / "cases.csv").open("x", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=columns)
        writer.writeheader()
        for r in all_rows:
            lb = r["labels"]
            row = {"case_id": r["case_id"], "unit": r["unit"], "state": r["state"], "status": r["status"],
                   "reasons": ";".join(r["reasons"]), "candidate_id": r["candidate_id"],
                   **{k: lb[k] for k in ("cell_geometry", "cell_f_ren", "B_peak_target", "R", "a", "offer_kind",
                                         "variant", "equal_duty")}}
            if "ch" in r:
                row.update({k: r["ch"][v] for k, v in KEY.items()})
                row.update({k: r["flags"].get(k) for k in ("divertor_pass", "power_short", "arm_extrapolated",
                                                           "extrapolated", "beyond_law_extents", "envelope_flag",
                                                           "R_over_sqrt_A_wp")})
            writer.writerow(row)
    print(json.dumps(counts["by_status"]), json.dumps({k: (v["comparison"].get("winner_at_80"),
                                                          (v["breakeven"] or {}).get("breakeven_USD_m"))
                                                      for k, v in cells.items()}))


if __name__ == "__main__":
    main()
