"""Study definition for `20260903-priced-levers` (goal `priced-levers` round 1, T-007).

Three arms against the WI-036 pin `6262dbf4…` -- the first package whose winding pack is
SIZED by the current it carries (wp_side = sqrt(I_coil / j_wp)), whose cold volume drives
the cryoplant, and whose conductor carries its own strain check alongside the structure's.

REVISED after the pre-execution framing critique returned MAJOR (evidence
`work/orchestration/goals/priced-levers/evidence/T-007_precritique.md`). All eight findings
accepted; the two that reshaped the study:

* **The winding-pack lever is barely priced.** `j_wp` reaches NO magnet capital: conductor
  cost is ampere-metre-proportional and blind to cross-section, so sweeping the pack 2.3x
  moves magnet capital by exactly zero and LCOE by 0.10%, and the stress relief that matters
  costs 0.026 $/MWh. The pack's 85% non-conductor mass (steel, insulation, copper, helium)
  has no cost home -- disclosed in WI-036 design D8 and then contradicted by this study's
  first framing. `arm-transect-jwp` therefore MEASURES how little the priced chain charges
  for pack sizing; it does not price it.
* **`T_i0` is swept, and the first design's fence conclusion was an artifact of holding it.**
  At the printed 50 MW with T and n free there are points BELOW the conductor ceiling whose
  only violated fence is the neutron wall load -- two of them self-sustaining at negative
  required auxiliary heating. So `arm-fence-p50` is a FENCE-ANATOMY arm, not a search: its
  empty feasible set is pre-registered and already committed by the predecessor, and its
  deliverable is which fence actually survives and what relieving each one costs.

The arms:

- `arm-fence-p50`: (I_coil, j_wp, T_i0, n_e0) at the printed 50 MW installed heating.
  Framing `search` by structure but reported as fence anatomy: the feasible set is
  pre-registered empty, and the result of record is the surviving-fence identity.
- `arm-search-p110`: the same axes at 110 MW, where the predecessor found a feasible region,
  with I refined to 0.2 MA over the band (critique MINOR 6: the band is ~0.8 MA wide against
  the first design's 1.0 MA step, so it could not have been resolved).
- `arm-transect-jwp`: a 1-D winding-pack current-density transect at baseline levers.

NOT swept, and traced as declined groups in `axes.json` with their indicators (critique
MINOR 4): `B_max`, `sigma_allow`, `eps_cond_allow`, `R`+tie, `a`. The first three each reach
exactly one constraint and zero objectives in `indicators.json` -- structural evidence that
they are pure fence-relaxers with no cost consequence, which is precisely why sweeping them
would manufacture free feasibility.

Held per proposal (every key explicit): a = 1.3, availability = 0.85, discount_rate = 0.07,
R = 12.7 (+ R0 tie). Sustainment and conductor held facts (iota_23, f_ren, E_wp, f_cond,
f_wp_vol, k_coil, k_sigma) are package-held sourced values; sensitivities in f_ren and
eps_cond_allow are named future work.

Arms are tagged AT CONSTRUCTION (critique MINOR 5: the first design inferred the arm by
value-matching and mislabelled three transect points into a grid arm, carrying an off-window
current column -- the one sitting exactly on the conductor ceiling).

Lessons applied: store beside the record (`20260821-power-cycle-ab#11`); oracle-side pb and
sustainment operands + bounds exported (`#10`, `20260901-sustainment-fence#3`); `points.csv`
carries `case_id` (`20260823-magnet-technology-ab#6`); evaluability pre-screen disclosed,
never silent (`20260829-p-pump-fence`); an oracle exception during the screen is a recorded
reason, never a crash.
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
ARM_P50 = "arm-fence-p50"
ARM_P110 = "arm-search-p110"
ARM_J = "arm-transect-jwp"
P110 = 110.0
P = route.P

HELD = {"a": 1.3, "availability": 0.85, "discount_rate": 0.07, "R": 12.7, "T_i0": 14.63}
BASE = {"I_coil": 15.4e6, "n_e0": 5.06e20, "p_input": 50.0, "j_wp": 118.8271604938272}

# Windows fixed from the oracle scan over ALL FOUR candidate axes
# (results/window_scan.json, 6144 candidates, 8 oracle errors). Provenance: `engineered`.
# What the scan fixed: at p=50 the feasible set is empty (0/3072) with 70 points blocked by
# the conductor ceiling alone and 40 by the wall load alone -- BOTH fences are independently
# binding, which is why the p50 arm samples both regions. At p=110 there are 28 feasible
# candidates in a band at I = 15.0 MA (0.5 MA scan resolution), T 14.63..17, n 0.8..1.1x.
# The density window reaches beta 0.0906 against the 0.05 limit, so beta_ok is testable --
# the first design's 0.9..1.1x window could not have tested it (critique MAJOR 3).
I_P50 = [15.0e6, 15.4e6, 16.0e6, 17.0e6, 18.0e6]
I_P110 = [14.8e6, 15.0e6, 15.2e6, 15.4e6]            # 0.2 MA over the band (critique MINOR 6)
J_VALUES = [90.0, 118.8271604938272, 130.0]          # design 118.83; source coil set 112..124
T_P50 = [14.63, 17.0, 18.0, 19.0]                    # the predecessor slice + the wall-limited band
T_P110 = [14.63, 16.0, 17.0, 18.0]
NE_P50 = [1.0, 1.1, 1.2, 1.4]                        # x n_e0 baseline; 1.4 reaches the beta limit
NE_P110 = [0.8, 0.9, 1.0, 1.1]
J_TRANSECT = [60.0, 70.0, 80.0, 100.0, 110.0, 120.0, 140.0]   # disjoint from J_VALUES (critique MINOR 5)
NE0 = 5.06e20

def point(I: float, ne: float, j: float, T: float, pin: float, arm: str) -> tuple[str, dict[str, float]]:
    """One complete proposal, TAGGED WITH ITS ARM at construction (critique MINOR 5).
    The swept axes, both declared ties, every held key."""
    proposal = {
        f"{P}R": HELD["R"],
        f"{P}magnet__R0": HELD["R"],            # declared tie rides with R
        f"{P}a": HELD["a"],
        f"{P}availability": HELD["availability"],
        f"{P}discount_rate": HELD["discount_rate"],
        f"{P}T_i0": T,
        f"{P}magnet__I_coil": I,
        f"{P}magnet__j_wp": j,
        f"{P}n_e0": ne,
        f"{P}p_input": pin,
        f"{P}p_ecrh": pin,                      # declared tie rides with p_input
    }
    return arm, proposal


def proposals() -> list[tuple[str, dict[str, float]]]:
    """Every proposal, each already carrying its arm id. Arms are tagged HERE, never
    inferred from values afterwards (critique MINOR 5)."""
    out: list[tuple[str, dict[str, float]]] = []
    out += [point(I, NE0 * nf, j, T, BASE["p_input"], ARM_P50)
            for I in I_P50 for j in J_VALUES for T in T_P50 for nf in NE_P50]
    out += [point(I, NE0 * nf, j, T, P110, ARM_P110)
            for I in I_P110 for j in J_VALUES for T in T_P110 for nf in NE_P110]
    out += [point(BASE["I_coil"], BASE["n_e0"], j, HELD["T_i0"], P110, ARM_J)
            for j in J_TRANSECT]
    # The pinned baseline point (I 15.4 MA, j_wp 118.83, T 14.63, n 1.0x, p 50) is already
    # a member of the p50 grid by construction -- appending it again would duplicate a
    # candidate identity. `_is_baseline` flags it in the export instead.
    return out


def _arms_by_id(tagged) -> dict[str, str]:
    """candidate identity -> arm id, keyed by the proposal's own frozen input tuple."""
    return {_key(inp): arm for arm, inp in tagged}


def _key(inp: dict) -> tuple:
    return tuple(round(float(inp[k]), 9) for k in sorted(inp))


def _is_baseline(inp: dict) -> bool:
    return (abs(float(inp[f"{P}magnet__I_coil"]) - BASE["I_coil"]) < 1e-6
            and abs(float(inp[f"{P}n_e0"]) - BASE["n_e0"]) < 1e6
            and abs(float(inp[f"{P}magnet__j_wp"]) - BASE["j_wp"]) < 1e-9
            and abs(float(inp[f"{P}T_i0"]) - HELD["T_i0"]) < 1e-9
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


def screen(tagged):
    evaluable, unevaluable = [], []
    for arm, candidate in tagged:
        p_net, sust, err = oracle_probe(candidate)
        ok = err is None and isinstance(p_net, float) and p_net > 0.0
        (evaluable if ok else unevaluable).append((arm, candidate, p_net, sust, err))
    return [(a, c) for a, c, _, _, _ in evaluable], unevaluable


def export_excluded(unevaluable, path: Path) -> Path:
    rows = []
    for arm, candidate, p_net, sust, err in unevaluable:
        rows.append({
            "arm_id": arm,
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
    fieldnames = ["arm_id", "I_coil_A", "n_e0", "j_wp", "p_input_MW", "reason", "source",
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
    # `aux_cooling__cryo_cost` is NOT here: it is a field of one multi-field module and the
    # evidence store records only single-field float channels -- the documented pb__*
    # limitation (ANNEX Oracle; 20260901-sustainment-fence#3). It is exported oracle-side in
    # oracle_operands.csv, labelled as such, exactly as p_net/rec_frac/q_eng are. Declaring
    # it here produced an empty column on the first execution; that is the finding, not a
    # value to invent.
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


def export(cases, arms, path: Path) -> Path:
    """`points.csv` with `case_id` and `arm_id`; held keys asserted per case."""
    rows = []
    for case in cases:
        inp = case.inputs
        for axis in ("a", "availability", "discount_rate", "R"):
            key = {"R": f"{P}R"}.get(axis, f"{P}{axis}")
            if abs(float(inp[key]) - HELD[axis]) > 1e-12:
                raise route.RouteError(f"case moved a declined axis ({axis}): {inp}")
        row = {
            "case_id": case.candidate_id,
            "arm_id": arms[_key(inp)],
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


def export_oracle_operands(cases, arms, path: Path) -> Path:
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
            "arm_id": arms[_key(case.inputs)],
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
            "cryo_cost_USD": ch[f"{P}aux_cooling__cryo_cost"],
            "aux_cost_USD": ch[f"{P}aux_cooling__aux_cost"],
            "magnet_capital_USD": ch[f"{P}magnet_capital_rollup__capital_cost"],
            "wall_load": ch[f"{P}wall_load_calc__wall_load"],
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

    tagged = proposals()
    arms = _arms_by_id(tagged)
    evaluable, unevaluable = screen(tagged)
    excluded_path = export_excluded(unevaluable, record_dir / "results" / "excluded_points.csv")

    cases, db = route.run_points(STUDY_ID, [c for _, c in evaluable], work_dir)
    completed = route._completed(cases, STUDY_ID)
    return {
        "points": export(completed, arms, record_dir / "results" / "points.csv"),
        "oracle_operands": export_oracle_operands(
            completed, arms, record_dir / "results" / "oracle_operands.csv"),
        "excluded": excluded_path,
        "store": db,
        "counts": {"proposed": len(evaluable) + len(unevaluable),
                   "evaluated": len(completed), "excluded": len(unevaluable)},
    }


if __name__ == "__main__":
    print(run())
