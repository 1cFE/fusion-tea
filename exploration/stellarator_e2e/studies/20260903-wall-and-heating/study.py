"""Study definition for `20260903-wall-and-heating` (goal `wall-and-heating` round 1, T-004).

Three arms against the WI-039 pin `2649e0ea…` -- the first package in which the heating
system is a computed chain rather than three held constants. Installed wall-plug electrical
power is the entry point; source-output power (the cost driver) and plasma-coupled power
(the physics driver, and the installed side of the sustainment fence) are derived from it
through a source efficiency and a stated coupling assumption.

WHY THIS STUDY EXISTS, in one sentence: to find out whether heating-technology efficiency
is an economic lever at all, now that it can be one.

Before WI-039 it could not be. The lumped `eta_pin` was a held constant whose only
appearance in the model was a division inside the recirculating sum, and the indicator
tool measures exactly that: `eta_pin` reached `net_positive` and `recirc_ok` and nothing
else (`pre_wi039_indicators.json`, generated from the pre-change package in a scratch
worktree -- measured, not assumed). Through the chain, both efficiencies and the wall-plug
power reach `sustainment_ok` as well, because coupled power is no longer independent of
them. The scan says the reach is not merely structural: at 220 MW wall-plug the feasible
count runs 0, 1, 7, 11, 16 across eta_source 0.40 to 0.60.

The arms:

- `arm-fence-p100`: (eta_source_heat, I_coil, T_i0, n_e0) at 100 MW wall-plug -- the
  printed 50 MW coupled at eta_source 0.50, restated. FENCE ANATOMY, not a search: the
  scan pre-registers the feasible set as empty (0 of 3080 candidates, at every efficiency
  from 0.40 to 0.60), so the deliverable is which fence survives and whether buying better
  gyrotrons moves it. The predecessor found the same emptiness at the same heating level.
- `arm-search-p220`: the same axes at 220 MW wall-plug (110 MW coupled at 0.50), where the
  scan finds 35 feasible candidates, with I refined to 0.25 MA over the 14.5..15.0 MA band
  the scan located.
- `arm-transect-eta`: a 1-D source-efficiency transect at the scan's best feasible point,
  to resolve the interior optimum the scan hints at -- 0.55 reads a LOWER LCOE than 0.60
  (272.412 against 273.046), which if it survives execution means better gyrotrons stop
  paying before they stop working.

NOT swept, and traced as declined groups in `axes.json` with their indicators:
`eta_couple_heat` (the stated deposition assumption -- sweeping a number nobody measured
reads as knowledge the model does not have), `R`+tie and `a` (the wall half's levers, round
2's), and `B_max` (still unpriced; WI-038 is its vehicle, after WI-040).

THE CAVEAT THAT TRAVELS WITH EVERY FENCE CLAIM IN THIS STUDY: `wall_load_ok` compares a
flat-wall AVERAGE operand to the source's printed PEAK limit. Round 1's own research
(T-001) registered three sources establishing that a stellarator first wall is 15-30%
larger in area than the circular torus this model integrates over, on the same wall-side
radius, and that the peak-to-average factor is 1.5-2.1 against a shaped-wall average. So
"the wall blocks here" is a statement about the fence as bound, not about the machine.
Making it honest is round 2's work and this study does not touch it.

Held per proposal (every key explicit): a = 1.3, availability = 0.85, discount_rate = 0.07,
R = 12.7 (+ R0 tie), j_wp = 118.8271604938272, eta_couple_heat = 1.0, and both dormant
direct heating terms at 0.0 (the chain is live, so they are zeroed -- coexisting would
double-count).

Lessons applied: store beside the record (`20260821-power-cycle-ab#11`); oracle-side pb and
sustainment operands exported (`#10`, `20260901-sustainment-fence#3`); `points.csv` carries
`case_id` (`20260823-magnet-technology-ab#6`); arms tagged AT CONSTRUCTION, never inferred
by value-matching afterwards (`20260903-priced-levers` critique MINOR 5); evaluability
pre-screen disclosed, never silent (`20260829-p-pump-fence`); an oracle exception during
the screen is a recorded reason, never a crash.
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

STUDY_ID = "20260903-wall-and-heating"
ARM_P100 = "arm-fence-p100"
ARM_P220 = "arm-search-p220"
ARM_ETA = "arm-transect-eta"
P = route.P

HELD = {"a": 1.3, "availability": 0.85, "discount_rate": 0.07, "R": 12.7,
        "j_wp": 118.8271604938272, "eta_couple_heat": 1.0,
        "p_delivered_direct_heat": 0.0, "p_coupled_direct_heat": 0.0}
BASE = {"I_coil": 15.4e6, "n_e0": 5.06e20, "T_i0": 14.63,
        "p_wallplug_heat": 100.0, "eta_source_heat": 0.50}
NE0 = 5.06e20

# Windows fixed from the oracle scan over all five candidate axes
# (results/window_scan.json, 6160 candidates, 0 oracle errors). Provenance: `engineered`.
# What the scan fixed:
#   * At 100 MW wall-plug the feasible set is EMPTY (0/3080) at every efficiency scanned,
#     0.40 through 0.60 -- buying better gyrotrons does not open the printed heating level.
#     Blocked-alone counts there: sustain 245, field 118, wall 46.
#   * At 220 MW wall-plug there are 35 feasible candidates in a band at I 14.5..15.0 MA
#     (0.5 MA scan resolution, refined here), T 14.63..18, n 0.8..1.1x, and the feasible
#     count rises with efficiency: 0, 1, 7, 11, 16 across 0.40..0.60.
#   * The density window reaches beta 0.05+ so beta_ok is testable rather than inert.
#   * T is swept to 24 keV in the scan -- past the predecessor's window edge (#5). Nothing
#     feasible appears above 18 keV at either heating level, so the executed window stops
#     at 19-22 rather than carrying dead range.
ETA_P100 = [0.40, 0.50, 0.60]
ETA_P220 = [0.45, 0.50, 0.55, 0.60]
I_P100 = [14.0e6, 15.0e6, 15.4e6, 16.0e6, 17.0e6]
I_P220 = [14.25e6, 14.5e6, 14.75e6, 15.0e6]       # 0.25 MA over the scan's band
T_P100 = [14.63, 17.0, 19.0, 22.0]
T_P220 = [14.63, 16.0, 17.0, 18.0]
NE_P100 = [0.9, 1.0, 1.1, 1.2]
NE_P220 = [0.8, 0.9, 1.0, 1.1]
# The transect sits at the scan's best feasible point and reaches BELOW and ABOVE the
# scanned efficiency range, so an interior optimum is bracketed rather than assumed.
ETA_TRANSECT = [0.35, 0.425, 0.475, 0.525, 0.575, 0.625, 0.65]   # disjoint from ETA_P220
TRANSECT_AT = {"I_coil": 14.5e6, "T_i0": 16.0, "ne_mult": 1.0, "wallplug": 220.0}


def point(eta, I, ne, T, wallplug, arm):
    """One complete proposal, TAGGED WITH ITS ARM at construction. Every swept axis, the
    declared R tie, and every held key explicit."""
    proposal = {
        f"{P}R": HELD["R"],
        f"{P}magnet__R0": HELD["R"],            # declared tie rides with R
        f"{P}a": HELD["a"],
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
    }
    return arm, proposal


def proposals():
    out = []
    out += [point(eta, I, NE0 * nf, T, 100.0, ARM_P100)
            for eta in ETA_P100 for I in I_P100 for T in T_P100 for nf in NE_P100]
    out += [point(eta, I, NE0 * nf, T, 220.0, ARM_P220)
            for eta in ETA_P220 for I in I_P220 for T in T_P220 for nf in NE_P220]
    out += [point(eta, TRANSECT_AT["I_coil"], NE0 * TRANSECT_AT["ne_mult"],
                  TRANSECT_AT["T_i0"], TRANSECT_AT["wallplug"], ARM_ETA)
            for eta in ETA_TRANSECT]
    return out


def _arms_by_id(tagged):
    return {_key(inp): arm for arm, inp in tagged}


def _key(inp):
    return tuple(round(float(inp[k]), 9) for k in sorted(inp))


def _is_baseline(inp):
    """The pinned baseline point: 100 MW wall-plug, eta_source 0.50, design I/n/T.
    It is a member of the p100 grid by construction (I 15.4, n 1.0x, T 14.63)."""
    return (abs(float(inp[f"{P}magnet__I_coil"]) - BASE["I_coil"]) < 1e-6
            and abs(float(inp[f"{P}n_e0"]) - BASE["n_e0"]) < 1e6
            and abs(float(inp[f"{P}T_i0"]) - BASE["T_i0"]) < 1e-9
            and abs(float(inp[f"{P}p_wallplug_heat"]) - BASE["p_wallplug_heat"]) < 1e-9
            and abs(float(inp[f"{P}eta_source_heat"]) - BASE["eta_source_heat"]) < 1e-9)


# --- Evaluability pre-screen (`20260829-p-pump-fence` pattern, exception-hardened) ---

def oracle_probe(pt):
    """(p_net, heating/sustainment operands, error) -- an oracle exception is a recorded
    reason, never a crash."""
    import oracle_entry as oe
    try:
        r = oe._compute(oe._oracle_overrides(pt))
        ops = {k: r[k] for k in ("p_aux_required", "tau_E", "p_rad",
                                 "heat_coupled", "heat_delivered",
                                 "heat_wallplug_total", "heat_eta_pin_eff")}
        return r["p_net"], ops, None
    except Exception as exc:
        return None, None, f"{type(exc).__name__}: {exc}"


def screen(tagged):
    evaluable, unevaluable = [], []
    for arm, candidate in tagged:
        p_net, ops, err = oracle_probe(candidate)
        ok = err is None and isinstance(p_net, float) and p_net > 0.0
        (evaluable if ok else unevaluable).append((arm, candidate, p_net, ops, err))
    return [(a, c) for a, c, _, _, _ in evaluable], unevaluable


def export_excluded(unevaluable, path):
    rows = []
    for arm, candidate, p_net, ops, err in unevaluable:
        rows.append({
            "arm_id": arm,
            "eta_source_heat": candidate[f"{P}eta_source_heat"],
            "p_wallplug_heat_MW": candidate[f"{P}p_wallplug_heat"],
            "I_coil_A": candidate[f"{P}magnet__I_coil"],
            "n_e0": candidate[f"{P}n_e0"], "T_i0_keV": candidate[f"{P}T_i0"],
            "reason": (err or "oracle p_net <= 0; the CAS10 land term takes sqrt(p_net) (WI-034 pending)"),
            "source": "oracle (verify_stellaris via oracle_entry), pre-screen before execution",
            "p_net_MW": (p_net.real if isinstance(p_net, complex) else p_net),
            "p_net_is_complex": isinstance(p_net, complex),
            "p_coupled_MW": (ops or {}).get("heat_coupled"),
            "p_aux_required_MW": (ops or {}).get("p_aux_required"),
            "tau_E_s": (ops or {}).get("tau_E"), "p_rad_MW": (ops or {}).get("p_rad"),
        })
    rows.sort(key=lambda r: (r["arm_id"], r["p_wallplug_heat_MW"], r["eta_source_heat"],
                             r["I_coil_A"], r["T_i0_keV"], r["n_e0"]))
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["arm_id", "eta_source_heat", "p_wallplug_heat_MW", "I_coil_A", "n_e0",
                  "T_i0_keV", "reason", "source", "p_net_MW", "p_net_is_complex",
                  "p_coupled_MW", "p_aux_required_MW", "tau_E_s", "p_rad_MW"]
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
    "eps_cond": f"{P}cond_strain__eps_cond",
    # WI-039 heating-chain channels. These ARE single-field float channels and do
    # appear in the store -- unlike the pb__* and sustain__* fields, which are fields
    # of multi-field modules (ANNEX Oracle; 20260901-sustainment-fence#3) and are
    # exported oracle-side in oracle_operands.csv instead.
    "heat_coupled": f"{P}heat__p_coupled",
    "heat_delivered": f"{P}heat__p_delivered",
    "heat_wallplug_total": f"{P}heat__p_wallplug_total",
    "heat_eta_pin_eff": f"{P}heat__eta_pin_eff",
    "heating_capital": f"{P}heating_cost__cost",
    "total_capital": f"{P}total_capital__total_capital",
    "magnet_capital": f"{P}magnet_capital_rollup__capital_cost",
    "overnight_capital": f"{P}overnight_capital__overnight_capital",
    "cas72": f"{P}cas72_calc__cost",
    "fuel": f"{P}fuel_calc__annual_fuel",
    "p_cryo": f"{P}cryo_elec__p_elec",
    "vol_cold": f"{P}wp_volume__vol_cold_total",
}


def export(cases, arms, path):
    """`points.csv` with `case_id` and `arm_id`; declined-axis keys asserted per case."""
    rows = []
    for case in cases:
        inp = case.inputs
        for axis in ("a", "availability", "discount_rate", "R"):
            key = {"R": f"{P}R"}.get(axis, f"{P}{axis}")
            if abs(float(inp[key]) - HELD[axis]) > 1e-12:
                raise route.RouteError(f"case moved a declined axis ({axis}): {inp}")
        if abs(float(inp[f"{P}eta_couple_heat"]) - HELD["eta_couple_heat"]) > 1e-12:
            raise route.RouteError(f"case moved the declined eta_couple_heat: {inp}")
        row = {
            "case_id": case.candidate_id,
            "arm_id": arms[_key(inp)],
            "eta_source_heat": float(inp[f"{P}eta_source_heat"]),
            "p_wallplug_heat_MW": float(inp[f"{P}p_wallplug_heat"]),
            "I_coil_A": float(inp[f"{P}magnet__I_coil"]),
            "n_e0": float(inp[f"{P}n_e0"]),
            "T_i0_keV": float(inp[f"{P}T_i0"]),
            "is_baseline_point": _is_baseline(inp),
            "R": float(inp[f"{P}R"]), "a": float(inp[f"{P}a"]),
            "j_wp": float(inp[f"{P}magnet__j_wp"]),
            "eta_couple_heat": float(inp[f"{P}eta_couple_heat"]),
            "availability": float(inp[f"{P}availability"]),
            "discount_rate": float(inp[f"{P}discount_rate"]),
        }
        for name, channel in CHANNELS.items():
            row[name] = case.outputs.get(channel)
        verdicts = route.short_verdicts(case)
        row.update(verdicts)
        row["feasible"] = all(status == "satisfied" for status in verdicts.values())
        rows.append(row)
    rows.sort(key=lambda r: (r["arm_id"], r["p_wallplug_heat_MW"], r["eta_source_heat"],
                             r["I_coil_A"], r["T_i0_keV"], r["n_e0"]))
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader(); writer.writerows(rows)
    return path
