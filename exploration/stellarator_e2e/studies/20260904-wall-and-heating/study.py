"""Study definition for `20260904-wall-and-heating` (goal `wall-and-heating` round 2, T-004).

Four arms against the WI-041 pin `c1b0f0d1…` -- the first package in which the wall-load
fence compares like with like: a computed PEAK (the circular-torus average times a
calibration computed from six printed Stellaris facts, 1.316441) against the printed
4.05 MW/m^2 peak, and the same peak sets the fluence-limited in-vessel lifetime CAS72 prices.

WHY THIS STUDY EXISTS: goal.md section Answered when (b)(ii) -- does a feasible region exist
at the printed heating level under the honest fence over the levers that reach wall load
(R with its tie, a, n_e0, T_i0, with I_coil), what is its LCOE, and what does the machine
pay to get under the wall through wall load -> lifetime -> CAS72; and, the strategy's second
question, where round 1's 267.159 optimum at 220 MW goes under the honest fence.

REVISED after the pre-execution framing critique returned MAJOR (evidence
`work/orchestration/goals/wall-and-heating/evidence/round2_T-004_precritique.md`; the
scope amendment of 2026-09-04 in the goal trail). All ten findings accepted; four reshape
what the study may claim:

* **F1. The one-sided sustainment fence passes IGNITED points.** `sustainment_ok` asserts
  p_aux_required <= p_coupled and nothing else, so a point whose alpha heating exceeds its
  losses (p_aux_required below zero) passes it -- and at (n, T) past the ignition line the
  plasma as modeled has no steady state at any non-negative installed power (the critique's
  T-transect: p_aux +35.8 -> -263 MW over 15 -> 22 keV with the peak 3.24 -> 6.92). In the
  a = 2.0 / 2.2 slices 59% of the "feasible" points are ignited. Every (b)(ii) claim is
  therefore made on `feasible_driven` = feasible AND p_aux_required >= 0; the ignited set is
  counted separately; the one-sided fence is filed as a model finding.
* **F2. The a-reversal that opens the printed level rests on held design-point transport
  facts.** With the WI-037 converged ash balance the wall load FALLS with `a` past 1.3
  (ash dilution outpaces the volume growth: He/n_e 0.074 / 0.137 / 0.185 over a 1.3 / 1.8 /
  2.2 at the best column), but the SIGN of that response is set by the held product
  f_suppr_ash x tau_ratio_ash = 0.5 x 8 = 4.0 and by iota_23 = 0.92 -- Stellaris Table-4
  facts at a = 1.3, A = 9.8, carried unchanged to A = 6.5. At tau*/tau_E = 4 the peak RISES
  with a and no 100 MW point survives; at 16 it falls further but sustainment blocks
  everything. So `arm-transect-ash` sweeps tau_ratio_ash 2..16 through the scan's best point
  at each level and through the design column, framed SENSITIVITY (an assumption's
  fragility test, not a design lever -- the scope amendment says so), and f_suppr_ash and
  iota_23 are declared as traced, declined groups. He/n_e is exported per point.
* **F3. The magnet account is blind to `a`.** The winding length is k_coil x R0 (WI-036 D3),
  the casing mass is held and B_peak is B_axis x a held ratio, so the magnet rollup (37% of
  overnight) does not move with `a` at all; the 1cfe-form comparison channel, which scales
  with r_coil = a + 2.25, rises 5,749 -> 7,473 M$ over a 1.3 -> 2.2. `points.csv` carries
  `lcoe_magnet_shadow`: the executed LCOE with the rollup's level scaled by the 1cfe form's
  shape in (R, a) -- a labelled shadow beside the executed number, never a replacement --
  and the blindness is filed as a model finding (20260830-stress-fence#1 re-sighted on a).
* **F4. "The wall costs 94 $/MWh" was unsound.** The cheapest wall-alone-blocked scan point
  is a plant 2.45x the size of the cheapest feasible one; most of the gap is plant size
  (LCOE ~ p_net^-0.52 across the scan). The wall's price is read per point as the LIFETIME
  CHARGE above the limit -- (CAS72 at the executed peak - CAS72 the same core would cost at
  a peak of exactly 4.05) / annual MWh -- and on size-matched pairs; the sound finding is
  that the lifetime chain prices the wall far too weakly to bound it (a point 2.7x over the
  limit pays ~27 $/MWh and stays cheapest), and that replacements cost no availability.
* F5: the re-read arm runs round 1's full 220 MW grid at all four of its efficiencies (the
  predecessor's committed grid, not a new sweep) so c0550 is re-executed. F6: the all-blocked
  R 9.7 and T 13 keV rows are dropped from the executed grids -- bracketed by the committed
  transects. F7: the geometry grid keeps its (R 12.7, a 1.3) column; the re-read arm cites
  the 24 shared cases. F8/F9/F10: statements in the record.

The arms:

- `arm-fence-p100`: (R+tie, a, I_coil, T_i0, n_e0) at 100 MW wall-plug -- the printed
  50 MW coupled at the held eta_source 0.50 and eta_couple 1.00; plus the pinned baseline
  as an explicit member. The (b)(ii) question proper.
- `arm-search-p220`: the same grid at 220 MW wall-plug (110 MW coupled).
- `arm-reread-p220`: round 1's exact 220 MW grid (R 12.7, a 1.3; I 14.0..15.25 at 0.25 MA;
  T 14.63/16/17/18; n 0.8..1.1x; eta 0.45/0.50/0.55/0.60; 384 points) re-executed at this
  pin, less the 24 members that coincide with the geometry grid at eta 0.50 -- those are
  read from `arm-search-p220`'s cases. The point-by-point crossing of the WI-041 boundary.
- `arm-transect-ash`: tau_ratio_ash 2 / 4 / 6 / 12 / 16 through three anchors -- the scan's
  best point at 100 MW (R 14.2, a 1.8, I 14 MA, T 16, n 0.8x), at 220 MW (R 14.2, a 1.8,
  I 14 MA, T 14.63, n 0.9x) and the design column (the baseline point) -- 15 points; each
  anchor's tau = 8 member is a grid or baseline case, cited rather than duplicated.

WINDOWS are fixed from the oracle scan (`results/window_scan.json`) and the edge transects
(`results/window_edges.json`); provenance `engineered`; how they were chosen is
record.md section 11.

Held per proposal (every key explicit): availability 0.85, discount_rate 0.07, j_wp
118.8271604938272, eta_source_heat 0.50 (except the re-read arm's four values), eta_couple
1.00, both dormant direct heating terms 0.0, tau_ratio_ash 8.0 (except the transect arm),
and the six wall_peak_* reference facts at their bound values (the source anchor; not in a
proposal, checked per case through the store's calibration channel).

THE SHADOW COLUMNS. (i) The wall anchor: the peak re-read at round 1's external band (net
1.15x and 1.83x on the average) beside the executed fence -- it bounds the anchor's VALUE,
not its constancy over (R, a), and the shadow rows' LCOE and CAS72 stay at the executed
calibration's lifetime. (ii) The magnet: `lcoe_magnet_shadow` as above.

THE CONSEQUENCE CHAIN, per point: the executed peak; the fluence-limited core life and
replacement count re-derived from it exactly as 'Levelized Replacement Cost' clips them;
the store's CAS72; CAS72 at a peak of exactly the limit for the same core; and the
lifetime charge above the limit in $/MWh.

Lessons applied: store beside the record; the oracle evaluated ONCE per case and fed to
both exports; multi-field module outputs (pb__*, sustain__*, heat__*) exported oracle-side
and never declared as store channels; `points.csv` carries `case_id`; arms tagged at
construction; no two arms share a point (`proposals()` raises); the evaluability
pre-screen disclosed, never silent.
"""

from __future__ import annotations

import csv
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
STUDIES = HERE.parent
if str(STUDIES) not in sys.path:
    sys.path.insert(0, str(STUDIES))

import study_route as route  # noqa: E402

STUDY_ID = "20260904-wall-and-heating"
ARM_P100 = "arm-fence-p100"
ARM_P220 = "arm-search-p220"
ARM_REREAD = "arm-reread-p220"
ARM_ASH = "arm-transect-ash"
P = route.P

HELD = {"availability": 0.85, "discount_rate": 0.07, "j_wp": 118.8271604938272,
        "eta_source_heat": 0.50, "eta_couple_heat": 1.0,
        "p_delivered_direct_heat": 0.0, "p_coupled_direct_heat": 0.0,
        "tau_ratio_ash": 8.0}
BASE = {"R": 12.7, "a": 1.3, "I_coil": 15.4e6, "n_e0": 5.06e20, "T_i0": 14.63,
        "p_wallplug_heat": 100.0}
NE0 = 5.06e20
_PLANT = json.loads((route.PACKAGE_DIR / "inputs" / "stellarator_plant_params.json").read_text())
WALL_LOAD_LIMIT = float(_PLANT[f"{P}wall_load_limit"])
FLUENCE_LIMIT = float(_PLANT[f"{P}fluence_limit"])
OPERATIONAL_YEARS = float(_PLANT[f"{P}operational_years"])
CONSTRUCTION_YEARS = float(_PLANT[f"{P}construction_years"])
SHADOW = {"lo": 1.15, "hi": 1.83}   # the round-1 external band on the AVERAGE
BUILD_STACK_M = 2.25                # ANNEX Validity masks: R > a + 2.25

# ---- WINDOWS (record.md section 11). Provenance: `engineered`. ----
# R: bottom bracketed by the conductor ceiling (every current in the window exceeds 24.9 T
#    at 9.7 m -- B_peak depends on (I, R) only, so the 9.7 row is known before execution and
#    is carried by results/window_edges.json, not executed: critique F6); top caught by the
#    wall, sustainment and beta together at 15.7-17.2.
# a: bottom caught by sustainment and the wall (1.3-1.6); TOP NOT CAUGHT -- feasibility and
#    falling LCOE continue to 2.2 with the plasma igniting past ~2.0; nothing in the model
#    bounds the minor radius (no aspect-ratio, coil-space or shaping fence) and the magnet
#    account does not price it (F3); the window stops at 2.2 by choice, disclosed.
# I: bottom caught by the wall and sustainment (13 MA), top by the ceiling (18 MA).
# T: bottom bracketed by sustainment (13 keV: 0 feasible in the critique's 240-point probe;
#    carried by the transects, not executed -- F6), top caught by the wall (17-18 keV).
# n: bottom caught by sustainment or recirc (0.6x), top by the wall (1.0x).
R_GRID = [11.2, 12.7, 14.2, 15.7, 17.2]
A_GRID = [1.3, 1.5, 1.7, 1.8, 2.0, 2.2]
I_GRID = [13.0e6, 14.0e6, 15.0e6, 16.0e6, 18.0e6]
T_GRID = [14.63, 16.0, 17.0, 18.0]
NE_GRID = [0.6, 0.7, 0.8, 0.9, 1.0]
# Round 1's 220 MW grid (20260903-wall-and-heating arm-search-p220), all four efficiencies.
I_REREAD = [14.0e6, 14.25e6, 14.5e6, 14.75e6, 15.0e6, 15.25e6]
T_REREAD = [14.63, 16.0, 17.0, 18.0]
NE_REREAD = [0.8, 0.9, 1.0, 1.1]
ETA_REREAD = [0.45, 0.50, 0.55, 0.60]
# The ash transect (F2): tau*/tau_E through three anchors; 8.0 is each anchor's grid or
# baseline case and is cited, not duplicated.
TAU_TRANSECT = [2.0, 4.0, 6.0, 12.0, 16.0]
ASH_ANCHORS = [
    dict(R=14.2, a=1.8, I=14.0e6, T=16.0, n=0.8, wallplug=100.0),    # scan's best at 100 MW
    dict(R=14.2, a=1.8, I=14.0e6, T=14.63, n=0.9, wallplug=220.0),   # scan's best at 220 MW
    dict(R=12.7, a=1.3, I=15.4e6, T=14.63, n=1.0, wallplug=100.0),   # the design column
]


def point(R, a, I, ne, T, wallplug, arm, eta=HELD["eta_source_heat"], tau=HELD["tau_ratio_ash"]):
    """One complete proposal, TAGGED WITH ITS ARM at construction. Every swept axis, the
    declared R tie, and every held key explicit."""
    proposal = {
        f"{P}R": R,
        f"{P}magnet__R0": R,                    # declared tie rides with R
        f"{P}a": a,
        f"{P}availability": HELD["availability"],
        f"{P}discount_rate": HELD["discount_rate"],
        f"{P}magnet__j_wp": HELD["j_wp"],
        f"{P}T_i0": T,
        f"{P}magnet__I_coil": I,
        f"{P}n_e0": ne,
        f"{P}p_wallplug_heat": wallplug,
        f"{P}eta_source_heat": eta,
        f"{P}eta_couple_heat": HELD["eta_couple_heat"],
        f"{P}p_delivered_direct_heat": HELD["p_delivered_direct_heat"],
        f"{P}p_coupled_direct_heat": HELD["p_coupled_direct_heat"],
        f"{P}tau_ratio_ash": tau,
    }
    return arm, proposal


def grid(wallplug, arm):
    out = []
    for R in R_GRID:
        for a in A_GRID:
            if not (R > a + BUILD_STACK_M):
                continue   # derived geometric bound from held-fixed inputs (ANNEX)
            for I in I_GRID:
                for T in T_GRID:
                    for nf in NE_GRID:
                        out.append(point(R, a, I, NE0 * nf, T, wallplug, arm))
    return out


def _in_geometry_grid_220(I, T, nf, eta):
    return (abs(eta - HELD["eta_source_heat"]) < 1e-12 and any(abs(I - g) < 1e-6 for g in I_GRID)
            and any(abs(T - g) < 1e-9 for g in T_GRID) and any(abs(nf - g) < 1e-9 for g in NE_GRID))


def proposals():
    out = []
    out += grid(100.0, ARM_P100)
    # The pinned baseline point is a member of arm-fence-p100 by construction (I 15.4 MA
    # is not a grid value), so the store carries it and `is_baseline_point` is true once.
    out.append(point(BASE["R"], BASE["a"], BASE["I_coil"], BASE["n_e0"], BASE["T_i0"],
                     BASE["p_wallplug_heat"], ARM_P100))
    out += grid(220.0, ARM_P220)
    # Round 1's grid, less the 24 members the geometry grid already carries (critique F7:
    # keep the (12.7, 1.3) column in the search arm; cite the shared cases from there).
    out += [point(12.7, 1.3, I, NE0 * nf, T, 220.0, ARM_REREAD, eta=eta)
            for eta in ETA_REREAD for I in I_REREAD for T in T_REREAD for nf in NE_REREAD
            if not _in_geometry_grid_220(I, T, nf, eta)]
    out += [point(A["R"], A["a"], A["I"], NE0 * A["n"], A["T"], A["wallplug"], ARM_ASH, tau=tau)
            for A in ASH_ANCHORS for tau in TAU_TRANSECT]
    seen = {}
    for arm, proposal in out:
        key = _key(proposal)
        if key in seen and seen[key] != arm:
            raise route.RouteError(
                f"arms {seen[key]!r} and {arm!r} share a point; arm tagging would be "
                f"ambiguous. Exclude it from one arm and cite the other's case instead.")
        if key in seen:
            raise route.RouteError(f"duplicate point inside {arm!r}: {proposal}")
        seen[key] = arm
    return out


def _arms_by_id(tagged):
    return {_key(inp): arm for arm, inp in tagged}


def _key(inp):
    return tuple(round(float(inp[k]), 9) for k in sorted(inp))


def _is_baseline(inp):
    return (abs(float(inp[f"{P}R"]) - BASE["R"]) < 1e-9
            and abs(float(inp[f"{P}a"]) - BASE["a"]) < 1e-9
            and abs(float(inp[f"{P}magnet__I_coil"]) - BASE["I_coil"]) < 1e-6
            and abs(float(inp[f"{P}n_e0"]) - BASE["n_e0"]) < 1e6
            and abs(float(inp[f"{P}T_i0"]) - BASE["T_i0"]) < 1e-9
            and abs(float(inp[f"{P}p_wallplug_heat"]) - BASE["p_wallplug_heat"]) < 1e-9
            and abs(float(inp[f"{P}eta_source_heat"]) - HELD["eta_source_heat"]) < 1e-12
            and abs(float(inp[f"{P}tau_ratio_ash"]) - HELD["tau_ratio_ash"]) < 1e-12)


# --- The CAS72 chain, re-derived oracle-side from a peak (as the calc clips it) ---

def core_life(peak, availability):
    fpy = min(max(FLUENCE_LIMIT / max(peak, 1e-6), 0.5), OPERATIONAL_YEARS * availability)
    cal = fpy / availability
    n_rep = max(0.0, float(math.ceil(OPERATIONAL_YEARS / cal)) - 1.0)
    return fpy, n_rep


def cas72_at(peak, cost_per_event, availability, i):
    fpy, n_rep = core_life(peak, availability)
    cal = fpy / availability
    s = (1.0 + i) ** (-cal)
    pv = cost_per_event * s * (1.0 - s ** n_rep) / (1.0 - s)
    disc = (1.0 + i) ** OPERATIONAL_YEARS
    crf = i * disc / (disc - 1.0)
    return crf * pv


def crf_idc(i):
    disc = (1.0 + i) ** OPERATIONAL_YEARS
    return i * disc / (disc - 1.0) * (1.0 + i) ** (CONSTRUCTION_YEARS / 2.0)


# --- Evaluability pre-screen (`20260829-p-pump-fence` pattern, exception-hardened) ---

ORACLE_NAMED = {
    "p_net": f"{P}pb__p_net", "rec_frac": f"{P}pb__rec_frac", "q_eng": f"{P}pb__q_eng",
    "p_th": f"{P}pb__p_th",
    "p_aux_required": f"{P}sustain__p_aux_required", "tau_E": f"{P}sustain__tau_E",
    "p_rad": f"{P}sustain__p_rad", "n_He0": f"{P}sustain__n_He0", "n_D0": f"{P}sustain__n_D0",
    "n_T0": f"{P}sustain__n_T0", "W_th": f"{P}sustain__W_th",
    "heat_coupled": f"{P}heat__p_coupled", "heat_delivered": f"{P}heat__p_delivered",
    "heat_wallplug_total": f"{P}heat__p_wallplug_total",
    "eps_cond": f"{P}cond_strain__eps_cond", "sigma_wp": f"{P}wp_stress__sigma_wp",
    "B_peak": f"{P}peak_field_calc__B_peak", "B_axis": f"{P}field_calc__B_axis",
    "cryo_cost": f"{P}aux_cooling__cryo_cost", "aux_cost": f"{P}aux_cooling__aux_cost",
    "magnet_capital_rollup": f"{P}magnet_capital_rollup__capital_cost",
    "wall_load": f"{P}wall_load_calc__wall_load",
    "wall_load_peak": f"{P}wall_peak_calc__wall_load_peak",
    "cas72": f"{P}cas72_calc__cost", "lcoe": f"{P}lcoe_calc__lcoe",
}


def oracle_channels(pt):
    """The oracle's named channels for one point, or (None, reason). Goes through
    `evaluate`, the seam's published surface; an exception is a recorded reason."""
    import oracle_entry as oe
    try:
        ch = oe.evaluate(pt)
        return {k: ch[v] for k, v in ORACLE_NAMED.items()}, None
    except Exception as exc:
        return None, f"{type(exc).__name__}: {exc}"


def screen(tagged):
    evaluable, unevaluable = [], []
    for n, (arm, candidate) in enumerate(tagged, 1):
        if n % 500 == 0:
            print(f"[screen] {n}/{len(tagged)}", file=sys.stderr, flush=True)
        ops, err = oracle_channels(candidate)
        p_net = None if ops is None else ops["p_net"]
        ok = err is None and isinstance(p_net, float) and p_net > 0.0
        (evaluable if ok else unevaluable).append((arm, candidate, p_net, ops, err))
    return evaluable, unevaluable


def _coords(candidate):
    return {"p_wallplug_heat_MW": float(candidate[f"{P}p_wallplug_heat"]),
            "R": float(candidate[f"{P}R"]), "a": float(candidate[f"{P}a"]),
            "I_coil_A": float(candidate[f"{P}magnet__I_coil"]),
            "n_e0": float(candidate[f"{P}n_e0"]), "T_i0_keV": float(candidate[f"{P}T_i0"]),
            "eta_source_heat": float(candidate[f"{P}eta_source_heat"]),
            "tau_ratio_ash": float(candidate[f"{P}tau_ratio_ash"])}


def export_excluded(unevaluable, path):
    rows = []
    for arm, candidate, p_net, ops, err in unevaluable:
        rows.append({
            "arm_id": arm, **_coords(candidate),
            "reason": (err or "oracle p_net <= 0; the CAS10 land term takes sqrt(p_net) (WI-034 pending)"),
            "source": "oracle (verify_stellaris via oracle_entry), pre-screen before execution",
            "p_net_MW": (p_net.real if isinstance(p_net, complex) else p_net),
            "p_net_is_complex": isinstance(p_net, complex),
            "p_coupled_MW": (ops or {}).get("heat_coupled"),
            "p_aux_required_MW": (ops or {}).get("p_aux_required"),
            "tau_E_s": (ops or {}).get("tau_E"), "p_rad_MW": (ops or {}).get("p_rad"),
        })
    rows.sort(key=lambda r: (r["arm_id"], r["p_wallplug_heat_MW"], r["R"], r["a"],
                             r["I_coil_A"], r["T_i0_keV"], r["n_e0"], r["eta_source_heat"], r["tau_ratio_ash"]))
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["arm_id", "p_wallplug_heat_MW", "R", "a", "I_coil_A", "n_e0", "T_i0_keV",
                  "eta_source_heat", "tau_ratio_ash", "reason", "source", "p_net_MW",
                  "p_net_is_complex", "p_coupled_MW", "p_aux_required_MW", "tau_E_s", "p_rad_MW"]
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader(); writer.writerows(rows)
    return path


CHANNELS = {
    "lcoe": f"{P}lcoe_calc__lcoe",
    "lcoe_1cfe": f"{P}lcoe_1cfe_calc__lcoe",
    "p_fus": f"{P}fusion__p_fus",
    "wall_load": f"{P}wall_load_calc__wall_load",                  # the AVERAGE, retained
    "wall_load_peak": f"{P}wall_peak_calc__wall_load_peak",         # WI-041: the fence's operand
    "wall_peak_calibration": f"{P}wall_peak_cal__calibration",      # WI-041: constant by construction
    "beta": f"{P}beta_calc__beta",
    "B_axis": f"{P}field_calc__B_axis",
    "B_peak": f"{P}peak_field_calc__B_peak",
    "sigma_wp": f"{P}wp_stress__sigma_wp",
    "eps_cond": f"{P}cond_strain__eps_cond",
    "plasma_volume": f"{P}geom__V",
    "heating_capital": f"{P}heating_cost__cost",
    "total_capital": f"{P}total_capital__total_capital",
    "magnet_capital": f"{P}magnet_capital_rollup__capital_cost",   # the rollup that enters total_capital
    "magnet_capital_1cfe_form": f"{P}magnet_cost__capital_cost",   # F3: the a-scaling shadow's shape
    "overnight_capital": f"{P}overnight_capital__overnight_capital",
    "cas72": f"{P}cas72_calc__cost",
    "replacement_cost_per_event": f"{P}replacement_cost_per_event__replacement_cost_per_event",
    "fuel": f"{P}fuel_calc__annual_fuel",
    "p_cryo": f"{P}cryo_elec__p_elec",
    "vol_cold": f"{P}wp_volume__vol_cold_total",
    "special_materials": f"{P}special_materials_capital__special_materials_capital",
}

EXPECTED_CALIBRATION = None  # resolved at run() from the oracle at the baseline; asserted per case
BASELINE_MAGNET = None       # (rollup, 1cfe-form) at the baseline, for the magnet shadow's level


def export(cases, arms, oracle, path):
    """`points.csv` with `case_id` and `arm_id`; every held key asserted per case; the
    oracle-derived columns labelled as such."""
    rows = []
    for case in cases:
        inp = case.inputs
        arm = arms[_key(inp)]
        for key, held in (("availability", HELD["availability"]),
                          ("discount_rate", HELD["discount_rate"]),
                          ("eta_couple_heat", HELD["eta_couple_heat"]),
                          ("p_delivered_direct_heat", HELD["p_delivered_direct_heat"]),
                          ("p_coupled_direct_heat", HELD["p_coupled_direct_heat"])):
            if abs(float(inp[f"{P}{key}"]) - held) > 1e-12:
                raise route.RouteError(f"case moved a held key ({key}): {inp}")
        if arm != ARM_REREAD and abs(float(inp[f"{P}eta_source_heat"]) - HELD["eta_source_heat"]) > 1e-12:
            raise route.RouteError(f"case moved the held eta_source_heat outside the re-read arm: {inp}")
        if arm != ARM_ASH and abs(float(inp[f"{P}tau_ratio_ash"]) - HELD["tau_ratio_ash"]) > 1e-12:
            raise route.RouteError(f"case moved the held tau_ratio_ash outside the ash transect: {inp}")
        if abs(float(inp[f"{P}magnet__j_wp"]) - HELD["j_wp"]) > 1e-9:
            raise route.RouteError(f"case moved the declined j_wp: {inp}")
        if abs(float(inp[f"{P}R"]) - float(inp[f"{P}magnet__R0"])) > 1e-12:
            raise route.RouteError(f"case broke the R / magnet__R0 tie: {inp}")
        row = {"case_id": case.candidate_id, "arm_id": arm, **_coords(inp),
               "is_baseline_point": _is_baseline(inp),
               "j_wp": float(inp[f"{P}magnet__j_wp"]),
               "eta_couple_heat": float(inp[f"{P}eta_couple_heat"]),
               "availability": float(inp[f"{P}availability"]),
               "discount_rate": float(inp[f"{P}discount_rate"])}
        for name, channel in CHANNELS.items():
            row[name] = case.outputs.get(channel)
        cal = row.get("wall_peak_calibration")
        if cal is None or abs(float(cal) - EXPECTED_CALIBRATION) > 1e-9:
            raise route.RouteError(
                f"calibration moved off the source anchor ({cal!r} vs {EXPECTED_CALIBRATION}): {inp}")
        verdicts = route.short_verdicts(case)
        row.update(verdicts)
        row["feasible"] = all(status == "satisfied" for status in verdicts.values())
        row["feasible_but_wall"] = all(
            status == "satisfied" for name, status in verdicts.items() if name != "wall_load_ok")
        # F1: the ignition reading, oracle-derived and labelled.
        ops = oracle[case.candidate_id]
        row["p_aux_required_MW_oracle"] = ops["p_aux_required"]
        row["ignited"] = ops["p_aux_required"] < 0.0
        row["feasible_driven"] = row["feasible"] and not row["ignited"]
        row["feasible_driven_but_wall"] = row["feasible_but_wall"] and not row["ignited"]
        row["p_net_MW_oracle"] = ops["p_net"]
        annual_mwh = 8760.0 * ops["p_net"] * HELD["availability"]
        # The consequence chain, re-derived oracle-side from the executed peak (F4).
        peak = float(row["wall_load_peak"]); avg = float(row["wall_load"])
        fpy, n_rep = core_life(peak, HELD["availability"])
        row["core_life_fpy_from_peak"] = fpy
        row["n_replacements_from_peak"] = n_rep
        row["wall_margin"] = WALL_LOAD_LIMIT - peak
        cpe = float(row["replacement_cost_per_event"])
        row["cas72_at_limit_oracle"] = cas72_at(WALL_LOAD_LIMIT, cpe, HELD["availability"], HELD["discount_rate"])
        row["cas72_from_peak_oracle"] = cas72_at(peak, cpe, HELD["availability"], HELD["discount_rate"])
        row["lifetime_charge_above_limit_per_MWh"] = (
            (float(row["cas72"]) - row["cas72_at_limit_oracle"]) / annual_mwh if annual_mwh > 0 else None)
        row["cas72_per_MWh"] = float(row["cas72"]) / annual_mwh if annual_mwh > 0 else None
        # F3: the magnet shadow -- the rollup's design-point level scaled by the 1cfe form's
        # shape in (R, a); a labelled shadow beside the executed LCOE, never a replacement.
        m_roll, m_1cfe = float(row["magnet_capital"]), float(row["magnet_capital_1cfe_form"])
        m_shadow = BASELINE_MAGNET[0] * (m_1cfe / BASELINE_MAGNET[1])
        row["magnet_capital_shadow"] = m_shadow
        row["lcoe_magnet_shadow"] = (
            float(row["lcoe"]) + (m_shadow - m_roll) * crf_idc(HELD["discount_rate"]) / annual_mwh
            if annual_mwh > 0 else None)
        # F2: the ash state.
        row["He_over_ne_oracle"] = ops["n_He0"] / float(inp[f"{P}n_e0"])
        # The wall-anchor shadow (i): round 1's external band on the AVERAGE, re-read beside
        # the executed fence. Bounds the anchor's VALUE, not its constancy over (R, a).
        for label, factor in SHADOW.items():
            shadow = avg * factor
            row[f"wall_load_shadow_{label}"] = shadow
            row[f"wall_load_ok_shadow_{label}"] = "satisfied" if shadow <= WALL_LOAD_LIMIT else "violated"
        row["feasible_shadow_lo"] = row["feasible_but_wall"] and row["wall_load_ok_shadow_lo"] == "satisfied"
        row["feasible_shadow_hi"] = row["feasible_but_wall"] and row["wall_load_ok_shadow_hi"] == "satisfied"
        rows.append(row)
    rows.sort(key=lambda r: (r["arm_id"], r["p_wallplug_heat_MW"], r["R"], r["a"],
                             r["I_coil_A"], r["T_i0_keV"], r["n_e0"], r["eta_source_heat"], r["tau_ratio_ash"]))
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader(); writer.writerows(rows)
    return path


def export_oracle_operands(cases, arms, oracle, path):
    """The operands the store does not record, oracle-derived and labelled, plus every
    constraint bound a fence claim is judged against."""
    mfe_plant = json.loads((route.PACKAGE_DIR / "inputs" / "mfe_plant_params.json").read_text())
    bounds = {
        "beta_limit": _PLANT[f"{P}beta_limit"], "wall_load_limit": WALL_LOAD_LIMIT,
        "fluence_limit": FLUENCE_LIMIT, "B_max_T": _PLANT[f"{P}magnet__B_max"],
        "sigma_allow_Pa": _PLANT[f"{P}magnet__sigma_allow"],
        "recirc_threshold": mfe_plant[f"{P}recirc_ok__threshold"],
        "eps_cond_allow": _PLANT[f"{P}magnet__eps_cond_allow"],
    }
    rows = []
    for case in cases:
        ops = oracle[case.candidate_id]
        rows.append({
            "case_id": case.candidate_id, "arm_id": arms[_key(case.inputs)], **_coords(case.inputs),
            "source": "oracle (verify_stellaris via oracle_entry); bounds from generated/inputs",
            "p_net_MW": ops["p_net"], "rec_frac": ops["rec_frac"], "q_eng": ops["q_eng"],
            "p_th_MW": ops["p_th"],
            "p_aux_required_MW": ops["p_aux_required"],
            "p_coupled_installed_MW": ops["heat_coupled"],
            "sustainment_margin_MW": ops["heat_coupled"] - ops["p_aux_required"],
            "ignited": ops["p_aux_required"] < 0.0,
            "p_delivered_MW": ops["heat_delivered"], "p_wallplug_total_MW": ops["heat_wallplug_total"],
            "tau_E_s": ops["tau_E"], "p_rad_MW": ops["p_rad"],
            "n_He0": ops["n_He0"], "n_D0": ops["n_D0"], "n_T0": ops["n_T0"],
            "He_over_ne": ops["n_He0"] / float(case.inputs[f"{P}n_e0"]),
            "W_th_MJ": ops["W_th"], "eps_cond": ops["eps_cond"], "sigma_wp_Pa": ops["sigma_wp"],
            "B_peak_T": ops["B_peak"], "B_axis_T": ops["B_axis"],
            "cryo_cost_USD": ops["cryo_cost"], "aux_cost_USD": ops["aux_cost"],
            "magnet_capital_USD": ops["magnet_capital_rollup"],
            "wall_load_oracle": ops["wall_load"], "wall_load_peak_oracle": ops["wall_load_peak"],
            "cas72_oracle_USD": ops["cas72"], "lcoe_oracle": ops["lcoe"],
            **bounds,
        })
    rows.sort(key=lambda r: (r["arm_id"], r["p_wallplug_heat_MW"], r["R"], r["a"],
                             r["I_coil_A"], r["T_i0_keV"], r["n_e0"], r["eta_source_heat"], r["tau_ratio_ash"]))
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader(); writer.writerows(rows)
    return path


def run(record_dir: Path = HERE):
    global EXPECTED_CALIBRATION, BASELINE_MAGNET
    record_dir = Path(record_dir)
    work_dir = record_dir.parent / "_work" / STUDY_ID       # beside the record

    tagged = proposals()
    arms = _arms_by_id(tagged)
    # The calibration every case must carry, and the magnet accounts' design-point level for
    # the F3 shadow: the pinned baseline result, deposited by the route at step 5.
    base = json.loads((record_dir / "results" / "baseline_result.json").read_text())["channels"]
    EXPECTED_CALIBRATION = float(base[CHANNELS["wall_peak_calibration"]])
    BASELINE_MAGNET = (float(base[CHANNELS["magnet_capital"]]), float(base[CHANNELS["magnet_capital_1cfe_form"]]))

    evaluable, unevaluable = screen(tagged)
    excluded_path = export_excluded(unevaluable, record_dir / "results" / "excluded_points.csv")

    print(f"[screen] done: {len(evaluable)} evaluable, {len(unevaluable)} excluded", file=sys.stderr, flush=True)
    print(f"[run_points] executing {len(evaluable)} points", file=sys.stderr, flush=True)
    cases, db = route.run_points(STUDY_ID, [c for _, c, _, _, _ in evaluable], work_dir)
    completed = route._completed(cases, STUDY_ID)
    print(f"[run_points] completed {len(completed)}; exporting", file=sys.stderr, flush=True)
    # The oracle was evaluated once per proposal in the screen; join it to the executed
    # cases by input key so neither export re-evaluates it.
    by_key = {_key(c): ops for _, c, _, ops, _ in evaluable}
    oracle = {case.candidate_id: by_key[_key(case.inputs)] for case in completed}
    return {
        "points": export(completed, arms, oracle, record_dir / "results" / "points.csv"),
        "oracle_operands": export_oracle_operands(
            completed, arms, oracle, record_dir / "results" / "oracle_operands.csv"),
        "excluded": excluded_path,
        "store": db,
        "counts": {"proposed": len(evaluable) + len(unevaluable),
                   "evaluated": len(completed), "excluded": len(unevaluable)},
    }


if __name__ == "__main__":
    print(run())
