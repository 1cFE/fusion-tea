"""Study definition for `20260830-stress-fence` (goal `magnet-closure` round 1, T-005).

Two arms against the WI-035 pin (the first package whose magnet field is computed from
the coil-set current and whose winding-pack stress limit executes):

- `arm-grid-R-I`: a (R, I_coil) design-search grid at the comparand's a = 1.3 m row —
  R reuses `study_route`'s own `R_VALUES` so fence positions in R subtract exactly
  against `20260829-p-pump-fence`; I_coil spans 2.0–26.0 MA so the window-scan's
  predicted structure (beta floor, conductor ceiling, stress ceiling, and the
  stress-overtakes-conductor crossover near R ≈ 15.6 m) sits in frame.
- `arm-transect-wp-side`: a 1-D winding-pack-side transect at the baseline point,
  bracketing the scan's predicted `wp_stress_ok` flip between 0.28 and 0.30 m.

Held per proposal (every key explicit, so a case is attributable from its own inputs):
a = 1.3, availability = 0.85, discount_rate = 0.07 (comparand values), and wp_side =
0.36 in the grid arm / (R, I_coil) = baseline in the transect arm. The winding-pack
cost's f_set and c_coil are package-held facts, disclosed in the record: the decomposed
magnet capital responds to I_coil but not to R.

Lessons applied: store beside the record (`20260821-power-cycle-ab#11`); oracle-side
pb operands exported as a labelled artifact (`#10`); `points.csv` carries `case_id`
(`20260823-magnet-technology-ab#6`); evaluability pre-screen disclosed, never silent
(`20260829-p-pump-fence` pattern).
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
STUDIES = HERE.parent
if str(STUDIES) not in sys.path:
    sys.path.insert(0, str(STUDIES))

import study_route as route  # noqa: E402

STUDY_ID = "20260830-stress-fence"
ARM_GRID = "arm-grid-R-I"
ARM_TRANSECT = "arm-transect-wp-side"
P = route.P

HELD = {"a": 1.3, "availability": 0.85, "discount_rate": 0.07}
BASELINE = {"R": 12.7, "I_coil": 15.4e6, "wp_side": 0.36}

R_VALUES = route.R_VALUES                                  # 4.0 .. 20.0 step 0.5 (33)
I_VALUES = [round(2.0e6 + 0.5e6 * i, 1) for i in range(49)]  # 2.0 .. 26.0 MA step 0.5
SIDE_VALUES = [round(0.20 + 0.02 * i, 2) for i in range(17)]  # 0.20 .. 0.52 m
BUILD_STACK_M = route.BUILD_STACK_M                        # R > a + 2.25 validity mask


def point(R: float, I: float, side: float) -> dict[str, float]:
    """One complete proposal: both grid axes, the declared tie, every held key."""
    return {
        f"{P}R": R,
        f"{P}magnet__R0": R,                    # declared tie rides with R
        f"{P}a": HELD["a"],
        f"{P}availability": HELD["availability"],
        f"{P}discount_rate": HELD["discount_rate"],
        f"{P}magnet__I_coil": I,
        f"{P}magnet__wp_side": side,
    }


def proposals() -> list[dict[str, float]]:
    """Grid arm row-major over (R, I), then the baseline point, then the transect.

    The baseline (R 12.7, I 15.4 MA, side 0.36) is off-grid in I (15.4 falls between
    nodes) and doubles as the transect's side = 0.36 member, so it appears exactly once.
    """
    grid = [point(R, I, BASELINE["wp_side"])
            for R in R_VALUES for I in I_VALUES
            if R > HELD["a"] + BUILD_STACK_M]
    grid.append(point(BASELINE["R"], BASELINE["I_coil"], BASELINE["wp_side"]))
    transect = [point(BASELINE["R"], BASELINE["I_coil"], side)
                for side in SIDE_VALUES if side != BASELINE["wp_side"]]
    return grid + transect


def arm_of(inp: dict) -> str:
    return ARM_TRANSECT if abs(float(inp[f"{P}magnet__wp_side"]) - BASELINE["wp_side"]) > 1e-12 else ARM_GRID


def _is_baseline(inp: dict) -> bool:
    return (abs(float(inp[f"{P}R"]) - BASELINE["R"]) < 1e-12
            and abs(float(inp[f"{P}magnet__I_coil"]) - BASELINE["I_coil"]) < 1e-9
            and abs(float(inp[f"{P}magnet__wp_side"]) - BASELINE["wp_side"]) < 1e-12)


# --- Evaluability pre-screen (the `20260829-p-pump-fence` pattern) ------------------

def oracle_p_net(pt: dict[str, float]) -> float:
    import oracle_entry as oe
    return oe._compute(oe._oracle_overrides(pt))["p_net"]


def screen(candidates: list[dict[str, float]]) -> tuple[list[dict], list[dict]]:
    evaluable, unevaluable = [], []
    for candidate in candidates:
        p_net = oracle_p_net(candidate)
        (evaluable if isinstance(p_net, float) and p_net > 0.0 else unevaluable).append(candidate)
    return evaluable, unevaluable


def export_excluded(unevaluable: list[dict[str, float]], path: Path) -> Path:
    rows = []
    for candidate in unevaluable:
        p_net = oracle_p_net(candidate)
        rows.append({
            "R": candidate[f"{P}R"], "I_coil_A": candidate[f"{P}magnet__I_coil"],
            "wp_side_m": candidate[f"{P}magnet__wp_side"],
            "reason": "oracle p_net <= 0; the CAS10 land term takes sqrt(p_net) (WI-034 pending)",
            "source": "oracle (verify_stellaris via oracle_entry), pre-screen before execution",
            "p_net_MW": p_net.real if isinstance(p_net, complex) else p_net,
            "p_net_is_complex": isinstance(p_net, complex),
        })
    rows.sort(key=lambda r: (r["R"], r["I_coil_A"], r["wp_side_m"]))
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    if rows:
        with path.open("w", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
            writer.writeheader(); writer.writerows(rows)
    else:
        path.write_text("R,I_coil_A,wp_side_m,reason,source,p_net_MW,p_net_is_complex\n")
    return path


CHANNELS = {
    "lcoe": f"{P}lcoe_calc__lcoe",
    "lcoe_1cfe": f"{P}lcoe_1cfe_calc__lcoe",
    "wall_load": f"{P}wall_load_calc__wall_load",
    "p_fus": f"{P}fusion__p_fus",
    "plasma_volume": f"{P}geom__V",
    "beta": f"{P}beta_calc__beta",
    "B_axis": f"{P}field_calc__B_axis",
    "B_peak": f"{P}peak_field_calc__B_peak",
    "sigma_wp": f"{P}wp_stress__sigma_wp",
    "total_capital": f"{P}total_capital__total_capital",
    "magnet_capital": f"{P}magnet_capital_rollup__capital_cost",
    "magnet_capital_1cfe": f"{P}magnet_cost__capital_cost",
    "winding_pack": f"{P}winding_pack_cost__cost",
    "magnet_structure": f"{P}magnet_structure_cost__cost",
    "overnight_capital": f"{P}overnight_capital__overnight_capital",
    "cas72": f"{P}cas72_calc__cost",
    "fuel": f"{P}fuel_calc__annual_fuel",
}


def export(cases, path: Path) -> Path:
    """`points.csv` with `case_id` and `arm_id`; held keys asserted per case."""
    rows = []
    for case in cases:
        inp = case.inputs
        for axis in ("a", "availability", "discount_rate"):
            if abs(float(inp[f"{P}{axis}"]) - HELD[axis]) > 1e-12:
                raise route.RouteError(f"case moved a declined axis ({axis}): {inp}")
        row = {
            "case_id": case.candidate_id,
            "arm_id": arm_of(inp),
            "R": float(inp[f"{P}R"]),
            "I_coil_A": float(inp[f"{P}magnet__I_coil"]),
            "wp_side_m": float(inp[f"{P}magnet__wp_side"]),
            "is_baseline_point": _is_baseline(inp),
            "a": float(inp[f"{P}a"]),
            "availability": float(inp[f"{P}availability"]),
            "discount_rate": float(inp[f"{P}discount_rate"]),
        }
        for name, channel in CHANNELS.items():
            row[name] = case.outputs.get(channel)
        verdicts = route.short_verdicts(case)
        row.update(verdicts)
        row["feasible"] = all(status == "satisfied" for status in verdicts.values())
        rows.append(row)
    rows.sort(key=lambda r: (r["arm_id"], r["is_baseline_point"], r["R"], r["I_coil_A"], r["wp_side_m"]))
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader(); writer.writerows(rows)
    return path


def export_oracle_operands(cases, path: Path) -> Path:
    """The pb operands the store does not record, oracle-derived and labelled as such,
    plus every constraint bound a fence claim is judged against."""
    import oracle_entry as oe

    plant = json.loads((route.PACKAGE_DIR / "inputs" / "stellarator_plant_params.json").read_text())
    bounds = {
        "beta_limit": plant[f"{P}beta_limit"],
        "wall_load_limit": plant[f"{P}wall_load_limit"],
        "B_max_T": plant[f"{P}magnet__B_max"],
        "sigma_allow_Pa": plant[f"{P}magnet__sigma_allow"],
        "recirc_threshold": 0.5,
    }
    rows = []
    for case in cases:
        ch = oe.evaluate(dict(case.inputs))
        rows.append({
            "case_id": case.candidate_id,
            "arm_id": arm_of(case.inputs),
            "R": float(case.inputs[f"{P}R"]),
            "I_coil_A": float(case.inputs[f"{P}magnet__I_coil"]),
            "wp_side_m": float(case.inputs[f"{P}magnet__wp_side"]),
            "source": "oracle (verify_stellaris via oracle_entry); bounds from generated/inputs",
            "p_net_MW": ch[f"{P}pb__p_net"],
            "rec_frac": ch[f"{P}pb__rec_frac"],
            "q_eng": ch[f"{P}pb__q_eng"],
            **bounds,
        })
    rows.sort(key=lambda r: (r["arm_id"], r["R"], r["I_coil_A"], r["wp_side_m"]))
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader(); writer.writerows(rows)
    return path


def run(record_dir: Path = HERE) -> dict[str, object]:
    record_dir = Path(record_dir)
    work_dir = record_dir.parent / "_work" / STUDY_ID       # beside the record (#11)

    evaluable, unevaluable = screen(proposals())
    excluded_path = export_excluded(unevaluable, record_dir / "results" / "excluded_points.csv")

    cases, db = route.run_points(STUDY_ID, evaluable, work_dir)
    completed = route._completed(cases, STUDY_ID)
    return {
        "points": export(completed, record_dir / "results" / "points.csv"),
        "oracle_operands": export_oracle_operands(
            completed, record_dir / "results" / "oracle_operands.csv"),
        "excluded": excluded_path,
        "store": db,
        "counts": {"proposed": len(evaluable) + len(unevaluable),
                   "evaluated": len(completed), "excluded": len(unevaluable)},
    }


if __name__ == "__main__":
    print(run())
