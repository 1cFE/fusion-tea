"""Study definition for `20260903-priced-levers` (goal `priced-levers` round 1, T-007).

Three arms against the WI-036 pin `6262dbf4…` -- the first package whose winding pack is
SIZED by the current it carries (wp_side = sqrt(I_coil / j_wp)), whose cold volume drives
the cryoplant, and whose conductor carries its own strain check alongside the structure's:

- `arm-grid-I-jwp-p50`: an (I_coil, j_wp, n_e0) design search at the printed 50 MW
  installed heating. The round's question lives here: with the field lever priced, does a
  feasible operating point exist at the printed installed power? The oracle window scan
  (results/window_scan.json) pre-registers the expected answer as NO -- and, more usefully,
  that the only fence left standing is the conductor ceiling.
- `arm-grid-I-jwp-p110`: the same axes at 110 MW, where the predecessor study
  (`20260901-sustainment-fence`) found a feasible region. This measures what honest pack
  sizing COSTS at a known-feasible operating point, against that study's committed
  optimum of 293.468 $/MWh -- the comparison the goal's question actually needs.
- `arm-transect-jwp`: a 1-D winding-pack current-density transect at baseline levers and
  110 MW. Prices the new lever on its own: what a wider pack buys in stress relief and
  costs in cold mass, cryoplant load and capital.

NOT swept, deliberately: `magnet__B_max`. WI-036 gave the winding pack a cost consequence
but gave the conductor GRADE none -- raising the ceiling is still free in every channel
(that is WI-038's whole purpose). Sweeping it here would manufacture feasible points that
cost nothing, which is precisely the unpriced-lever defect this goal exists to remove.
`sigma_allow` is likewise held: goal `priced-levers` T-002 established that the applicable
allowable depends on the stress category and that the conductor's own limit arrives at
almost the same place, so it is not relaxed to open a region.

Held per proposal (every key explicit): a = 1.3, availability = 0.85, discount_rate = 0.07,
R = 12.7 (+ R0 tie), T_i0 = 14.63. Sustainment and conductor held facts (iota_23, f_ren,
E_wp, f_cond, eps_cond_allow, f_wp_vol, k_coil, k_sigma) are package-held sourced values,
not swept -- sensitivities in f_ren and eps_cond_allow are named future work.

Lessons applied: store beside the record (`20260821-power-cycle-ab#11`); oracle-side pb
and sustainment operands + bounds exported (`#10`, `20260901-sustainment-fence#3`);
`points.csv` carries `case_id` (`20260823-magnet-technology-ab#6`); evaluability pre-screen
disclosed, never silent (`20260829-p-pump-fence`); an oracle exception during the screen is
a recorded reason, never a crash.
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

STUDY_ID = "20260903-priced-levers"
ARM_P50 = "arm-grid-I-jwp-p50"
ARM_P110 = "arm-grid-I-jwp-p110"
ARM_J = "arm-transect-jwp"
P110 = 110.0
P = route.P

HELD = {"a": 1.3, "availability": 0.85, "discount_rate": 0.07, "R": 12.7, "T_i0": 14.63}
BASE = {"I_coil": 15.4e6, "n_e0": 5.06e20, "p_input": 50.0, "j_wp": 118.8271604938272}

# Windows fixed from the oracle scan (results/window_scan.json), provenance `engineered`.
I_VALUES = [round(12.0e6 + 1.0e6 * i, 1) for i in range(13)]         # 12 .. 24 MA step 1
J_VALUES = [90.0, 100.0, 112.0, 118.8271604938272, 130.0]            # A/mm^2; design 118.83, source set 112..124
NE_VALUES = [round(5.06e20 * (0.9 + 0.1 * i), -16) for i in range(3)]  # 0.9x .. 1.1x
I_VALUES_P110 = [round(13.0e6 + 1.0e6 * i, 1) for i in range(8)]     # 13 .. 20 MA step 1
J_TRANSECT = [round(60.0 + 10.0 * i, 4) for i in range(9)]           # 60 .. 140 A/mm^2 step 10


def point(I: float, ne: float, j: float, pin: float) -> dict[str, float]:
    """One complete proposal: the swept axes, both declared ties, every held key."""
    return {
        f"{P}R": HELD["R"],
        f"{P}magnet__R0": HELD["R"],            # declared tie rides with R
        f"{P}a": HELD["a"],
        f"{P}availability": HELD["availability"],
        f"{P}discount_rate": HELD["discount_rate"],
        f"{P}T_i0": HELD["T_i0"],
        f"{P}magnet__I_coil": I,
        f"{P}magnet__j_wp": j,
        f"{P}n_e0": ne,
        f"{P}p_input": pin,
        f"{P}p_ecrh": pin,                      # declared tie rides with p_input
    }


def proposals() -> list[dict[str, float]]:
    """Two (I, j_wp, n_e0) grids at the printed 50 MW and at 110 MW, the baseline point,
    then the j_wp transect."""
    grid = [point(I, ne, j, BASE["p_input"])
            for I in I_VALUES for j in J_VALUES for ne in NE_VALUES]
    grid += [point(I, ne, j, P110)
             for I in I_VALUES_P110 for j in J_VALUES for ne in NE_VALUES]
    grid.append(point(BASE["I_coil"], BASE["n_e0"], BASE["j_wp"], BASE["p_input"]))
    j_arm = [point(BASE["I_coil"], BASE["n_e0"], j, P110) for j in J_TRANSECT]
    return grid + j_arm


def arm_of(inp: dict) -> str:
    j = float(inp[f"{P}magnet__j_wp"])
    at_p110 = abs(float(inp[f"{P}p_input"]) - P110) < 1e-9
    if at_p110 and j not in J_VALUES and abs(float(inp[f"{P}magnet__I_coil"]) - BASE["I_coil"]) < 1e-6:
        return ARM_J
    return ARM_P110 if at_p110 else ARM_P50


def _is_baseline(inp: dict) -> bool:
    return (abs(float(inp[f"{P}magnet__I_coil"]) - BASE["I_coil"]) < 1e-6
            and abs(float(inp[f"{P}n_e0"]) - BASE["n_e0"]) < 1e6
            and abs(float(inp[f"{P}magnet__j_wp"]) - BASE["j_wp"]) < 1e-9
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
            "j_wp": candidate[f"{P}magnet__j_wp"], "p_input_MW": candidate[f"{P}p_input"],
            "reason": (err or "oracle p_net <= 0; the CAS10 land term takes sqrt(p_net) (WI-034 pending)"),
            "source": "oracle (verify_stellaris via oracle_entry), pre-screen before execution",
            "p_net_MW": (p_net.real if isinstance(p_net, complex) else p_net),
            "p_net_is_complex": isinstance(p_net, complex),
            "p_aux_required_MW": (sust or {}).get("p_aux_required"),
            "tau_E_s": (sust or {}).get("tau_E"),
            "p_rad_MW": (sust or {}).get("p_rad"),
        })
    rows.sort(key=lambda r: (r["I_coil_A"], r["n_e0"], r["j_wp"], r["p_input_MW"]))
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["I_coil_A", "n_e0", "j_wp", "p_input_MW", "reason", "source",
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
    "eps_cond": f"{P}cond_strain__eps_cond",          # WI-036 conductor operand
    "wp_side": f"{P}wp_sizing__wp_side",              # WI-036 computed pack side
    "c_coil": f"{P}coil_length__c_coil",              # WI-036 computed winding length
    "vol_cold": f"{P}wp_volume__vol_cold_total",      # WI-036 computed cold volume
    "p_cryo": f"{P}cryo_elec__p_elec",                # the cold-mass cost channel
    "cryoplant_capital": f"{P}aux_cooling__cryo_cost",
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
        for axis in ("a", "availability", "discount_rate", "R", "T_i0"):
            key = {"R": f"{P}R"}.get(axis, f"{P}{axis}")
            if abs(float(inp[key]) - HELD[axis]) > 1e-12:
                raise route.RouteError(f"case moved a declined axis ({axis}): {inp}")
        row = {
            "case_id": case.candidate_id,
            "arm_id": arm_of(inp),
            "I_coil_A": float(inp[f"{P}magnet__I_coil"]),
            "n_e0": float(inp[f"{P}n_e0"]),
            "j_wp": float(inp[f"{P}magnet__j_wp"]),
            "p_input_MW": float(inp[f"{P}p_input"]),
            "T_i0_keV": float(inp[f"{P}T_i0"]),
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
                             r["j_wp"], r["n_e0"], r["p_input_MW"]))
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
        "eps_cond_allow": plant[f"{P}magnet__eps_cond_allow"],      # WI-036 conductor limit
    }
    rows = []
    for case in cases:
        ch = oe.evaluate(dict(case.inputs))
        rows.append({
            "case_id": case.candidate_id,
            "arm_id": arm_of(case.inputs),
            "I_coil_A": float(case.inputs[f"{P}magnet__I_coil"]),
            "n_e0": float(case.inputs[f"{P}n_e0"]),
            "j_wp": float(case.inputs[f"{P}magnet__j_wp"]),
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
            "eps_cond": ch[f"{P}cond_strain__eps_cond"],
            "sigma_wp_Pa": ch[f"{P}wp_stress__sigma_wp"],
            "B_peak_T": ch[f"{P}peak_field_calc__B_peak"],
            **bounds,
        })
    rows.sort(key=lambda r: (r["arm_id"], r["I_coil_A"], r["j_wp"], r["n_e0"], r["p_input_MW"]))
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
