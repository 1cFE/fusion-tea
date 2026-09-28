"""Study definition for `20260823-magnet-technology-ab` (RUN-STUDY Item 6, study 1).

Two arms (REBCO as built; Nb3Sn at 1costingFE's sourced conductor values with a
DI-010-derived cold volume), the same (B, density) window in each, one store. Route
mechanics come from the package-owned route `studies/study_route.py`; nothing here
touches the package or any tool under `scripts/study/`.

Lessons from study 20260821-power-cycle-ab applied here: the store lives beside the
record directory (finding #11), and the two power-balance operands the store does not
record (`pb__p_net`, `pb__rec_frac`) are emitted from the oracle as a separate,
labelled artifact, `results/oracle_operands.csv`, before verification (finding #10).

A proposal carries every key explicitly -- geometry and the economic levers at their
baseline values, the density ties, and the arm's block -- so a case is attributable to
its arm from its own inputs alone.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
STUDIES = HERE.parent
if str(STUDIES) not in sys.path:
    sys.path.insert(0, str(STUDIES))

import study_route as route  # noqa: E402

STUDY_ID = "20260823-magnet-technology-ab"
P = route.P

# --- Arms: the conductor block -------------------------------------------------------
# REBCO: the package as built (Stellaris, WI-030; B_max 24.9 T per the owner's ruling).
# Nb3Sn: defaults.py:613 (b_max 13.0, cryo_temp_k 4.5), costing_constants.yaml:57 (7 $/kA-m);
# vol_cold from DI-010 at the ampere-turns arm B can actually reach: Stellaris
# 136.56 m^3 x (118 / 21.5) [J_eng ratio, equal ampere-turns] x (4.69 / 9.0) [ampere-turns
# scale with B; arm B's ceiling is 4.69 T] = 390 m^3 (range 285-570 for the 4-8x band).
# Held at that value over the whole sweep: overstates arm B's cryo load below 4.69 T
# (where volume would be smaller still) and is exact at its ceiling. See record.md
# section 2 and finding in section 15 (winding volume should follow ampere-turns in
# the model; a B-dependent tie here would be harness physics, policy section 5.3).
BLOCK_KEYS = (f"{P}magnet__cost_per_kAm", f"{P}T_cold_cryo", f"{P}magnet__B_max", f"{P}vol_cold_cryo")
ARMS: dict[str, dict[str, float]] = {
    "arm-rebco": {BLOCK_KEYS[0]: 50.0, BLOCK_KEYS[1]: 20.0, BLOCK_KEYS[2]: 24.9, BLOCK_KEYS[3]: 136.56},
    "arm-nb3sn": {BLOCK_KEYS[0]: 7.0, BLOCK_KEYS[1]: 4.5, BLOCK_KEYS[2]: 13.0, BLOCK_KEYS[3]: 390.0},
}

# --- Axes and windows ----------------------------------------------------------------
# Density is one scale factor on the four species peaks (Point A, Table 5 image);
# quasineutrality at the peak is scale-invariant, so the four move together.
PEAKS = {"n_D0": 1.96e20, "n_T0": 1.96e20, "n_e0": 5.06e20, "n_He0": 0.56e20}
HELD = {"R": 12.7, "a": 1.3, "availability": 0.85, "discount_rate": 0.07}

# 3.0 .. 10.0 T step 0.125, densified to 0.05 across 4.0-5.0 T (the Nb3Sn ceiling
# band) and with the exact Nb3Sn ceiling node 4.69 T (13.0 / 2.7667 = 4.6988; 4.70
# reads violated). The REBCO ceiling 9.0 T is on the base grid.
B_VALUES = sorted({round(3.0 + 0.125 * i, 3) for i in range(57)} | {round(4.0 + 0.05 * i, 3) for i in range(21)} | {4.69})
# Density scale: 0.36 .. 1.26 step 0.02, plus every hundredth across the 0.40-0.60
# band where the beta and recirculation fences cross (oracle scan, record.md section 11).
# The floor 0.36 is the package's evaluability limit: below ~0.35 the net power goes
# negative and the CAS10 land term (sqrt of p_net) makes the point execution_failed
# in the package (complex in the oracle). Not a design screen -- a disclosed bound.
DENSITY_SCALES = sorted({round(0.36 + 0.02 * i, 2) for i in range(46)} | {round(0.40 + 0.01 * i, 2) for i in range(21)})
DENSITY_FLOOR = 0.36


def point(arm: str, B: float, scale: float) -> dict[str, float]:
    p = {f"{P}R": HELD["R"], f"{P}magnet__R0": HELD["R"], f"{P}a": HELD["a"],
         f"{P}availability": HELD["availability"], f"{P}discount_rate": HELD["discount_rate"],
         f"{P}magnet__B": B}
    p.update({f"{P}{k}": v * scale for k, v in PEAKS.items()})
    p.update(ARMS[arm])
    return p


def proposals() -> list[tuple[str, dict[str, float]]]:
    """(arm_id, proposal), arm-major then row-major over (B, density)."""
    return [(arm, point(arm, B, s)) for arm in ARMS for B in B_VALUES for s in DENSITY_SCALES]


def arm_of(inputs: dict) -> str:
    for arm, block in ARMS.items():
        if all(abs(float(inputs[k]) - v) < 1e-9 for k, v in block.items()):
            return arm
    raise route.RouteError(f"case inputs match no arm block: {inputs}")


def density_scale_of(inputs: dict) -> float:
    scales = {round(float(inputs[f"{P}{k}"]) / v, 6) for k, v in PEAKS.items()}
    if len(scales) != 1:
        raise route.RouteError(f"density ties disagree: {scales}")
    return round(scales.pop(), 2)


CHANNELS = {
    "lcoe": f"{P}lcoe_calc__lcoe", "lcoe_1cfe": f"{P}lcoe_1cfe_calc__lcoe",
    "beta": f"{P}beta_calc__beta", "B_peak": f"{P}peak_field_calc__B_peak",
    "p_fus": f"{P}fusion__p_fus", "wall_load": f"{P}wall_load_calc__wall_load",
    "magnet_capital": f"{P}magnet_cost__capital_cost", "p_cryo": f"{P}cryo_elec__p_elec",
    "total_capital": f"{P}total_capital__total_capital", "cas72": f"{P}cas72_calc__cost",
    "fuel": f"{P}fuel_calc__annual_fuel",
}


def export(cases, path: Path) -> Path:
    rows = []
    for case in cases:
        inp = case.inputs
        row = {"arm_id": arm_of(inp), "B": float(inp[f"{P}magnet__B"]), "density_scale": density_scale_of(inp)}
        row.update(route.required_outputs(case, CHANNELS))
        verdicts = route.short_verdicts(case)
        row.update(verdicts)
        row["feasible"] = all(s == "satisfied" for s in verdicts.values())
        rows.append(row)
    rows.sort(key=lambda r: (r["arm_id"], r["B"], r["density_scale"]))
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    return path


def export_oracle_operands(cases, path: Path) -> Path:
    """Finding #10: recompute power-balance operands independently for each case.

    Historical v2 evidence omitted these fields; v3 publishes them. This export
    remains labelled as oracle-derived rather than recovered package evidence.
    """
    import oracle_entry as oe  # the seam, beside the route

    import json

    # The bound values the verdicts are judged against, read from the package's own
    # inputs (study-2 finding #7: the record carried verdicts but not their bounds).
    plant = json.loads((route.PACKAGE_DIR / "inputs" / "stellarator_plant_params.json").read_text())
    bounds = {"beta_limit": plant[f"{P}beta_limit"], "wall_load_limit": plant[f"{P}wall_load_limit"],
              "tbr": plant[f"{P}tbr"], "tbr_floor": plant[f"{P}tbr_floor"]}
    rows = []
    for case in cases:
        ch = oe.evaluate(dict(case.inputs))
        rows.append({"case_id": case.candidate_id, "arm_id": arm_of(case.inputs), "source": "oracle (verify_stellaris via oracle_entry); bounds from generated/inputs",
                     "p_net_MW": ch[f"{P}pb__p_net"], "rec_frac": ch[f"{P}pb__rec_frac"], "q_eng": ch[f"{P}pb__q_eng"],
                     "p_et_MW": ch[f"{P}pb__p_et"], "p_th_MW": ch[f"{P}pb__p_th"],
                     "recirc_threshold": 0.5, "B_max": case.inputs[f"{P}magnet__B_max"], **bounds})
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    return path


def run(record_dir: Path = HERE) -> dict[str, Path]:
    """Every proposal through the stock lifecycle, one store beside the record, then exports."""
    record_dir = Path(record_dir)
    work_dir = record_dir.parent / "_work" / STUDY_ID          # beside the record (finding #11)
    cases, db = route.run_points(
        STUDY_ID, [p for _, p in proposals()], work_dir, required_channels=CHANNELS,
    )
    completed = route._completed(cases, STUDY_ID)
    return {
        "points": export(completed, record_dir / "results" / "points.csv"),
        "oracle_operands": export_oracle_operands(completed, record_dir / "results" / "oracle_operands.csv"),
        "store": db,
    }


if __name__ == "__main__":
    print(run())
