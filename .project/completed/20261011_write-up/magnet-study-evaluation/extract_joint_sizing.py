"""Extract and independently recheck the 15 September joint magnet-sizing evidence.

Read-only. Reads the sealed study record and writes compact data under ./data/.
Run from the repository root:

    uv run python .project/active/write-up/magnet-study-evaluation/extract_joint_sizing.py

Every recomputation below uses only native inputs/outputs and the equations
printed in the study answer and the model source; it does not import the
generated package or the study's own oracle.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
STUDY = REPO / "exploration/stellarator_e2e/studies/20260915-joint-magnet-sizing"
OUT = Path(__file__).resolve().parent / "data"
P = "stellarator_09__stellaris__"

# Held construction values stated in the answer and protocol (checked against inputs below).
TURN_CURRENT_A = 50_000.0
ALLOWABLE_FRACTION = 0.80
TAPE_W_M, TAPE_T_M = 6e-3, 56e-6
TAPE_FRACTION = 0.09
FIELD_CEILING_T = 24.9
R_REF, A_COIL_REF = 12.7, 3.15  # stellarator_plant.sysml:249,278

CASES = {
    "reference": "Original inventory, original allocation",
    "g-12.7-1.3-1.54e+07-0.3": "Current-sized inventory, original allocation",
    "g-12.7-1.3-1.54e+07-0.6": "Current-sized inventory, enlarged allocation",
}


def short(key: str) -> str:
    return key.replace(P, "")


def load_cases() -> dict[str, dict]:
    native = json.loads((STUDY / "results/native-cases.json").read_text())
    return {c["proposal_id"]: c for c in native}


def case_row(c: dict) -> dict:
    i = {short(k): v for k, v in c["inputs"].items()}
    o = {short(k): v for k, v in c["outputs"].items()}
    v = {short(k).rsplit("__", 1)[0]: s for k, s in c["verdicts"].items()}
    return {
        "proposal_id": c["proposal_id"],
        "candidate_id": c["candidate_id"],
        "sizing_mode": i["magnet__winding_pack__sizing_mode"],
        "inventory_multiplier": i["magnet__winding_pack__inventory_multiplier"],
        "radial_allocation_m": i["magnet__coil__coil_t"],
        "transverse_cavity_m": i["magnet__casing__interior_y"],
        "coil_ampere_turns_A": i["magnet__coil__I_coil"],
        "R_m": i["plasma__R"],
        "a_m": i["plasma__a"],
        "coil_centre_radius_m": o["rb__r_coil_centre"],
        "B_axis_T": o["magnet__field_calc__B_axis"],
        "B_peak_T": o["magnet__peak_field_calc__B_peak"],
        "field_ceiling_T": i["magnet__winding_pack__B_max"],
        "field_extrapolated_flag": o["magnet__conductor_current__field_extrapolated"],
        "tape_current_A": o["magnet__conductor_current__tape_critical_current"],
        "required_tapes_ref": o["magnet__current_sizing__required_tapes"],
        "installed_tapes_ref": o["magnet__conductor_current__parallel_tapes_reference"],
        "installed_tapes_set": o["magnet__conductor_current__parallel_tapes_set"],
        "operating_fraction_ref": o["magnet__conductor_current__operating_fraction_reference"],
        "pack_side_m": o["magnet__wp_sizing__wp_side"],
        "required_x_m": o["magnet__wp_fit__required_x"],
        "required_y_m": o["magnet__wp_fit__required_y"],
        "cavity_x_m": o["magnet__wp_fit__cavity_x"],
        "cavity_y_m": o["magnet__wp_fit__cavity_y"],
        "fit_margin_x_m": o["magnet__wp_fit__margin_x"],
        "fit_margin_y_m": o["magnet__wp_fit__margin_y"],
        "conductor_length_m": o["magnet__winding_procurement__conductor_length"],
        "tape_length_m": o["magnet__winding_procurement__tape_length"],
        "tape_cost_usd": o["magnet__winding_procurement__tape_cost"],
        "magnet_priced_subtotal_usd": o["magnet__magnet_capital_rollup__capital_cost"],
        "stored_energy_J": o["magnet__stored_energy__W_mag"],
        "lcoe_usd_per_MWh": o["lcoe_calc__lcoe"],
        "current_verdict": v["reference_conductor_current_ok"],
        "fit_verdict": v["wp_fit_ok"],
        "field_verdict": v["peak_field_ok"],
        "divertor_verdict": v["divertor_heat_ok"],
        "violated": ";".join(sorted(k for k, s in v.items() if s != "satisfied")),
    }


def recheck(row: dict) -> dict:
    """Independent recomputation of the headline identities for one case."""
    turns = row["coil_ampere_turns_A"] / TURN_CURRENT_A
    tape_area = TAPE_W_M * TAPE_T_M
    req = TURN_CURRENT_A / (ALLOWABLE_FRACTION * row["tape_current_A"])
    installed = row["installed_tapes_ref"]
    pack_area = turns * installed * tape_area / TAPE_FRACTION
    bore = (R_REF - A_COIL_REF) / (row["R_m"] - row["coil_centre_radius_m"])
    b_peak = 9.0 * (FIELD_CEILING_T / 9.0) * bore  # anchor ratio 24.9/9.0 at reference
    return {
        "turns": turns,
        "required_tapes_recomputed": req,
        "required_tapes_rel_err": req / row["required_tapes_ref"] - 1,
        "installed_over_required": installed / row["required_tapes_ref"],
        "operating_fraction_recomputed": TURN_CURRENT_A / (installed * row["tape_current_A"]),
        "pack_area_recomputed_m2": pack_area,
        "pack_side_recomputed_m": math.sqrt(pack_area),
        "pack_side_rel_err": math.sqrt(pack_area) / row["pack_side_m"] - 1,
        "effective_density_A_per_mm2": row["coil_ampere_turns_A"] / pack_area / 1e6,
        "bore_factor": bore,
        "B_peak_recomputed_T": b_peak,
        "B_peak_rel_err": b_peak / row["B_peak_T"] - 1,
        "field_margin_T": row["field_ceiling_T"] - row["B_peak_T"],
        "fit_margin_x_recomputed_m": row["cavity_x_m"] - row["required_x_m"],
    }


def omitted_pack_term_threshold(a_before: float, a_after: float, bore_ratio: float) -> float:
    """Share x of the eq.-39 configuration term carried by the winding-pack term at the
    reference, above which including that term would make the net peak field fall.

    Configuration term (a0 + R*a1/sqrt(A)); with x = (R*a1/sqrt(A_before)) / term,
    its ratio after/before is 1 - x*(1 - sqrt(A_before/A_after)). Net field ratio is
    bore_ratio times that. Returns x where the net ratio equals 1.
    """
    shrink = 1 - math.sqrt(a_before / a_after)
    return (1 - 1 / bore_ratio) / shrink


def cohort_counts(native: dict[str, dict]) -> dict:
    """Recount default-cohort passes directly from native verdicts.

    Default cohort definition (report.md): current-sizing mode, 1.01 reserve, unit
    performance factors, 24.9 T ceiling, square pack. The analysis flag list is
    compared, not trusted.
    """
    analysis = json.loads((STUDY / "results/analysis.json").read_text())
    flagged = set(analysis["default_cases"]["case_ids"])
    mine = []
    for c in native.values():
        i = {short(k): v for k, v in c["inputs"].items()}
        wp = "magnet__winding_pack__"
        if (
            i[wp + "sizing_mode"] == 1.0
            and i[wp + "inventory_multiplier"] == 1.01
            and all(i[wp + f] == 1.0 for f in ("material_factor", "orientation_factor", "cabling_factor", "degradation_factor", "sharing_factor", "fit_aspect_ratio"))
            and i[wp + "B_max"] == 24.9
        ):
            mine.append(c)
    all_pass = [c for c in mine if all(s == "satisfied" for s in c["verdicts"].values())]
    per_pred = {}
    for c in mine:
        for k, s in c["verdicts"].items():
            name = short(k).rsplit("__", 1)[0]
            per_pred.setdefault(name, 0)
            per_pred[name] += s != "satisfied"
    ids_mine = {c["candidate_id"] for c in mine} | {c["proposal_id"] for c in mine}
    return {
        "default_cases_by_input_rule": len(mine),
        "analysis_flagged_default_ids": len(flagged),
        "flag_ids_matched": len(flagged & ids_mine),
        "default_all20_passes": len(all_pass),
        "default_violation_counts": dict(sorted(per_pred.items(), key=lambda kv: -kv[1])),
        "all_unique_native_cases": len(native),
        "all_cases_all20_passes": sum(all(s == "satisfied" for s in c["verdicts"].values()) for c in native.values()),
    }


def main() -> None:
    OUT.mkdir(exist_ok=True)
    native = load_cases()
    rows = []
    for pid, label in CASES.items():
        row = {"label": label, **case_row(native[pid])}
        row.update(recheck(row))
        rows.append(row)

    with (OUT / "joint-sizing-three-cases.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    ref, sized, accom = rows
    pack_before = ref["pack_side_m"] ** 2
    pack_after = accom["pack_side_m"] ** 2
    summary = {
        "source": str(STUDY.relative_to(REPO)),
        # The answer's snapshot digest is the file's SHA-256, not a field inside it.
        "snapshot_file_sha256": hashlib.sha256((STUDY / "snapshot.json").read_bytes()).hexdigest(),
        "tapes_entering_to_installed": [ref["installed_tapes_ref"], sized["installed_tapes_ref"]],
        "tape_length_ratio": sized["tape_length_m"] / ref["tape_length_m"],
        "tape_count_ratio": sized["installed_tapes_ref"] / ref["installed_tapes_ref"],
        "magnet_subtotal_delta_usd": [sized["magnet_priced_subtotal_usd"] - ref["magnet_priced_subtotal_usd"], accom["magnet_priced_subtotal_usd"] - sized["magnet_priced_subtotal_usd"]],
        "lcoe_delta_usd_per_MWh": [sized["lcoe_usd_per_MWh"] - ref["lcoe_usd_per_MWh"], accom["lcoe_usd_per_MWh"] - sized["lcoe_usd_per_MWh"]],
        "reference_field_margin_T": ref["field_margin_T"],
        "accommodated_field_excess_T": -accom["field_margin_T"],
        "bore_ratio_accommodated": accom["bore_factor"],
        "omitted_pack_term_share_reversing_field_step": omitted_pack_term_threshold(pack_before, pack_after, accom["bore_factor"]),
        "pack_area_m2_entering_to_accommodated": [pack_before, pack_after],
        "cohort": cohort_counts(native),
    }
    (OUT / "joint-sizing-recheck.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    for r in rows:
        print(r["label"], {k: r[k] for k in ("required_tapes_rel_err", "pack_side_rel_err", "B_peak_rel_err", "operating_fraction_recomputed", "effective_density_A_per_mm2")})


if __name__ == "__main__":
    main()
