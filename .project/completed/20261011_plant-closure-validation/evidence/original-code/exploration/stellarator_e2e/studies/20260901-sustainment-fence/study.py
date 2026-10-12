"""Study definition for `20260901-sustainment-fence` (goal `operating-point-closure` round 2, T-005).

Three arms against the WI-037 pin (the first package whose operating point is checked
for sustainment: ISS04 tau_E from the machine, computed ash/quasi-neutral fuel, and
`sustainment_ok` = required sustained coupled heating <= installed):

- `arm-grid-I-ne`: an (I_coil, n_e0) design-search grid at the baseline machine and
  operating point (R 12.7, a 1.3, T_i0 14.63, p_input 50, wp_side 0.36) — the field
  lever against the density lever, where the sustainment relief (loss ~ B^-2.15),
  the conductor ceiling, the stress ceiling, the beta limit, and the wall-load limit
  all carve the plane. The strategy's question lives here: is field rewarded, and
  does the constrained optimum leave the beta floor?
- `arm-transect-T`: a 1-D T_i0 transect at baseline levers — the committed form of the
  round-1 required-aux curve (unstable-branch structure, sustainment margin vs T).
- `arm-transect-p-input`: a 1-D installed-heating transect at baseline levers, with
  the declared p_ecrh tie riding — where does installed heating satisfy sustainment
  (scan-predicted ~91 MW), and what does buying it cost (heating capital + recirc)?

Held per proposal (every key explicit): a = 1.3, availability = 0.85, discount_rate =
0.07, R = 12.7 (+ R0 tie), wp_side = 0.36. Sustainment held facts (iota_23, f_ren,
f_alpha_fast, tau_ratio_ash, f_suppr_ash, Z_eff_core, f_W_core, Ti_over_Te) are
package-held sourced values, not swept — a sensitivity in f_ren is future work.

Lessons applied: store beside the record (`20260821-power-cycle-ab#11`); oracle-side pb
operands + bounds exported (`#10`); `points.csv` carries `case_id`
(`20260823-magnet-technology-ab#6`); evaluability pre-screen disclosed, never silent
(`20260829-p-pump-fence`); an oracle exception during the screen is recorded as
unevaluable-with-reason, never a crash (WI-037 fail-loud ash fixed point).
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

STUDY_ID = "20260901-sustainment-fence"
ARM_GRID = "arm-grid-I-ne"
ARM_GRID_P110 = "arm-grid-I-ne-p110"   # critique finding 1: the same (I, n_e0) grid at
                                        # installed heating above the ~91 MW sustainment
                                        # flip, so the field-vs-density trade has a live
                                        # feasible region and the optimum question is
                                        # answerable rather than empty-by-construction
ARM_T = "arm-transect-T"
ARM_P = "arm-transect-p-input"
P110 = 110.0
P = route.P

HELD = {"a": 1.3, "availability": 0.85, "discount_rate": 0.07, "R": 12.7, "wp_side": 0.36}
BASE = {"I_coil": 15.4e6, "n_e0": 5.06e20, "T_i0": 14.63, "p_input": 50.0}

I_VALUES = [round(8.0e6 + 1.0e6 * i, 1) for i in range(17)]          # 8 .. 24 MA step 1
NE_VALUES = [round(5.06e20 * (0.6 + 0.1 * i), -16) for i in range(9)]  # 0.6x .. 1.4x
T_VALUES = [round(6.0 + 1.0 * i, 2) for i in range(25)]              # 6 .. 30 keV step 1
PIN_VALUES = [round(30.0 + 10.0 * i, 1) for i in range(13)]          # 30 .. 150 MW step 10


def point(I: float, ne: float, T: float, pin: float) -> dict[str, float]:
    """One complete proposal: the swept axes, both declared ties, every held key."""
    return {
        f"{P}R": HELD["R"],
        f"{P}magnet__R0": HELD["R"],            # declared tie rides with R
        f"{P}a": HELD["a"],
        f"{P}availability": HELD["availability"],
        f"{P}discount_rate": HELD["discount_rate"],
        f"{P}magnet__wp_side": HELD["wp_side"],
        f"{P}magnet__I_coil": I,
        f"{P}n_e0": ne,
        f"{P}T_i0": T,
        f"{P}p_input": pin,
        f"{P}p_ecrh": pin,                      # declared tie rides with p_input
    }


def proposals() -> list[dict[str, float]]:
    """Grid arms row-major over (I, n_e0) at p_input 50 and 110, the baseline point,
    then the two transects."""
    grid = [point(I, ne, BASE["T_i0"], BASE["p_input"]) for I in I_VALUES for ne in NE_VALUES]
    grid += [point(I, ne, BASE["T_i0"], P110) for I in I_VALUES for ne in NE_VALUES]
    grid.append(point(BASE["I_coil"], BASE["n_e0"], BASE["T_i0"], BASE["p_input"]))
    t_arm = [point(BASE["I_coil"], BASE["n_e0"], T, BASE["p_input"])
             for T in T_VALUES if abs(T - BASE["T_i0"]) > 1e-9]
    p_arm = [point(BASE["I_coil"], BASE["n_e0"], BASE["T_i0"], pin)
             for pin in PIN_VALUES if abs(pin - BASE["p_input"]) > 1e-9]
    return grid + t_arm + p_arm


def arm_of(inp: dict) -> str:
    if abs(float(inp[f"{P}T_i0"]) - BASE["T_i0"]) > 1e-9:
        return ARM_T
    if abs(float(inp[f"{P}p_input"]) - P110) < 1e-9:
        return ARM_GRID_P110
    if abs(float(inp[f"{P}p_input"]) - BASE["p_input"]) > 1e-9:
        return ARM_P
    return ARM_GRID


def _is_baseline(inp: dict) -> bool:
    return (abs(float(inp[f"{P}magnet__I_coil"]) - BASE["I_coil"]) < 1e-6
            and abs(float(inp[f"{P}n_e0"]) - BASE["n_e0"]) < 1e6
            and abs(float(inp[f"{P}T_i0"]) - BASE["T_i0"]) < 1e-9
            and abs(float(inp[f"{P}p_input"]) - BASE["p_input"]) < 1e-9)


# --- Evaluability pre-screen (`20260829-p-pump-fence` pattern, exception-hardened) ---

def oracle_probe(pt: dict[str, float]):
    """(p_net, sustainment_operands, error) — an oracle exception is a recorded
    reason, never a crash; the sustainment stage's operands are captured whenever
    that stage converges, so excluded points keep their required-aux curve
    (critique finding 3)."""
    import oracle_entry as oe
    try:
        r = oe._compute(oe._oracle_overrides(pt))
        sust = {k: r[k] for k in ("p_aux_required", "tau_E", "p_rad")}
        return r["p_net"], sust, None
    except Exception as exc:  # fail-loud chain (ash non-convergence, fuel exhaustion)
        return None, None, f"{type(exc).__name__}: {exc}"


def screen(candidates):
    evaluable, unevaluable = [], []
    for candidate in candidates:
        p_net, sust, err = oracle_probe(candidate)
        ok = err is None and isinstance(p_net, float) and p_net > 0.0
        (evaluable if ok else unevaluable).append((candidate, p_net, sust, err))
    return [c for c, _, _, _ in evaluable], unevaluable


def export_excluded(unevaluable, path: Path) -> Path:
    rows = []
    for candidate, p_net, sust, err in unevaluable:
        rows.append({
            "I_coil_A": candidate[f"{P}magnet__I_coil"], "n_e0": candidate[f"{P}n_e0"],
            "T_i0_keV": candidate[f"{P}T_i0"], "p_input_MW": candidate[f"{P}p_input"],
            "reason": (err or "oracle p_net <= 0; the CAS10 land term takes sqrt(p_net) (WI-034 pending)"),
            "source": "oracle (verify_stellaris via oracle_entry), pre-screen before execution",
            "p_net_MW": (p_net.real if isinstance(p_net, complex) else p_net),
            "p_net_is_complex": isinstance(p_net, complex),
            "p_aux_required_MW": (sust or {}).get("p_aux_required"),
            "tau_E_s": (sust or {}).get("tau_E"),
            "p_rad_MW": (sust or {}).get("p_rad"),
        })
    rows.sort(key=lambda r: (r["I_coil_A"], r["n_e0"], r["T_i0_keV"], r["p_input_MW"]))
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["I_coil_A", "n_e0", "T_i0_keV", "p_input_MW", "reason", "source",
                  "p_net_MW", "p_net_is_complex", "p_aux_required_MW", "tau_E_s", "p_rad_MW"]
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader(); writer.writerows(rows)
    return path


CHANNELS = {
    "lcoe": f"{P}lcoe_calc__lcoe",
    "lcoe_1cfe": f"{P}lcoe_1cfe_calc__lcoe",
    "p_fus": f"{P}fusion__p_fus",
    "wall_load": f"{P}wall_load_calc__wall_load",
    "beta": f"{P}beta_calc__beta",
    "B_axis": f"{P}field_calc__B_axis",
    "B_peak": f"{P}peak_field_calc__B_peak",
    "sigma_wp": f"{P}wp_stress__sigma_wp",
    # The sustainment quantities are fields of ONE multi-field module
    # ('Plasma Sustainment'), and the evidence store records only single-field
    # float channels — the documented pb__* precedent (ANNEX § Oracle). They are
    # exported oracle-side in oracle_operands.csv, labelled as such, exactly as
    # p_net/rec_frac/q_eng are.
    "total_capital": f"{P}total_capital__total_capital",
    "magnet_capital": f"{P}magnet_capital_rollup__capital_cost",
    "heating_capital": f"{P}heating_cost__cost",
    "overnight_capital": f"{P}overnight_capital__overnight_capital",
    "cas72": f"{P}cas72_calc__cost",
    "fuel": f"{P}fuel_calc__annual_fuel",
}


def export(cases, path: Path) -> Path:
    """`points.csv` with `case_id` and `arm_id`; held keys asserted per case."""
    rows = []
    for case in cases:
        inp = case.inputs
        for axis in ("a", "availability", "discount_rate", "R", "wp_side"):
            key = {"R": f"{P}R", "wp_side": f"{P}magnet__wp_side"}.get(axis, f"{P}{axis}")
            if abs(float(inp[key]) - HELD[axis]) > 1e-12:
                raise route.RouteError(f"case moved a declined axis ({axis}): {inp}")
        row = {
            "case_id": case.candidate_id,
            "arm_id": arm_of(inp),
            "I_coil_A": float(inp[f"{P}magnet__I_coil"]),
            "n_e0": float(inp[f"{P}n_e0"]),
            "T_i0_keV": float(inp[f"{P}T_i0"]),
            "p_input_MW": float(inp[f"{P}p_input"]),
            "is_baseline_point": _is_baseline(inp),
            "R": float(inp[f"{P}R"]),
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
    rows.sort(key=lambda r: (r["arm_id"], r["is_baseline_point"], r["I_coil_A"],
                             r["n_e0"], r["T_i0_keV"], r["p_input_MW"]))
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader(); writer.writerows(rows)
    return path


def export_oracle_operands(cases, path: Path) -> Path:
    """The pb operands the store does not record, oracle-derived and labelled, plus
    every constraint bound a fence claim is judged against."""
    import oracle_entry as oe

    plant = json.loads((route.PACKAGE_DIR / "inputs" / "stellarator_plant_params.json").read_text())
    mfe_plant = json.loads((route.PACKAGE_DIR / "inputs" / "mfe_plant_params.json").read_text())
    bounds = {
        "beta_limit": plant[f"{P}beta_limit"],
        "wall_load_limit": plant[f"{P}wall_load_limit"],
        "B_max_T": plant[f"{P}magnet__B_max"],
        "sigma_allow_Pa": plant[f"{P}magnet__sigma_allow"],
        "recirc_threshold": mfe_plant[f"{P}recirc_ok__threshold"],  # from the package, never hardcoded (critique 6c)
    }
    rows = []
    for case in cases:
        ch = oe.evaluate(dict(case.inputs))
        rows.append({
            "case_id": case.candidate_id,
            "arm_id": arm_of(case.inputs),
            "I_coil_A": float(case.inputs[f"{P}magnet__I_coil"]),
            "n_e0": float(case.inputs[f"{P}n_e0"]),
            "T_i0_keV": float(case.inputs[f"{P}T_i0"]),
            "p_input_MW": float(case.inputs[f"{P}p_input"]),
            "source": "oracle (verify_stellaris via oracle_entry); bounds from generated/inputs",
            "p_net_MW": ch[f"{P}pb__p_net"],
            "rec_frac": ch[f"{P}pb__rec_frac"],
            "q_eng": ch[f"{P}pb__q_eng"],
            "p_aux_required_MW": ch[f"{P}sustain__p_aux_required"],
            "p_input_installed_MW": float(case.inputs[f"{P}p_input"]),
            "tau_E_s": ch[f"{P}sustain__tau_E"],
            "p_rad_MW": ch[f"{P}sustain__p_rad"],
            "n_He0": ch[f"{P}sustain__n_He0"],
            "n_D0": ch[f"{P}sustain__n_D0"],
            "W_th_MJ": ch[f"{P}sustain__W_th"],
            **bounds,
        })
    rows.sort(key=lambda r: (r["arm_id"], r["I_coil_A"], r["n_e0"], r["T_i0_keV"], r["p_input_MW"]))
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
