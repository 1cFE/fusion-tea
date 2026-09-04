"""Study definition for `20260903-wall-and-heating` (goal `wall-and-heating` round 1, T-004).

Four arms against the WI-039 pin `2649e0ea…` -- the first package in which the heating
system is a computed chain rather than three held constants. Installed wall-plug electrical
power is the entry point; source-output power (the cost driver) and plasma-coupled power
(the physics driver, and the installed side of the sustainment fence) are derived from it
through a source efficiency and a stated coupling assumption.

WHY THIS STUDY EXISTS: to find out whether heating-technology efficiency is an economic
lever, now that it can reach anything at all.

REVISED after the pre-execution framing critique returned MAJOR (evidence
`work/orchestration/goals/wall-and-heating/evidence/T-004_precritique.md`). All nine
findings accepted; four reshaped the study, and two of them killed claims the first design
would have published:

* **F1. There is no interior efficiency optimum, and the first design said there was.**
  The first design read "0.55 beats 0.60" off the scan and built a transect to resolve an
  optimum. That compared the *best point at each efficiency*, which are different
  (I, T, n) points -- a fence-edge artifact, not an optimum. At fixed (I, T, n) LCOE is
  **strictly monotone increasing** in `eta_source_heat`, for a structural reason: at fixed
  wall-plug power the recirculating term is `p_wallplug_total` = the wall-plug key itself,
  so it does not move with efficiency at all, while heating capital = rate x p_wallplug x
  eta_source rises exactly linearly. Efficiency at fixed wall-plug buys **feasibility and
  never economics**. Verified against the oracle at the transect anchor: LCOE 269.823 to
  273.675 monotone over eta 0.35 to 0.65, with `p_wallplug_total` = 220.0 at every one.
* **F1, the consequence: `arm-couple-110` exists.** Asking "does efficiency pay" only at
  fixed wall-plug asks it in the one parameterization where the answer is forced. At fixed
  *coupled* power the arithmetic inverts: `p_delivered = p_wallplug x eta_source =
  P_coupled` is constant, so heating capital is constant and the whole effect of efficiency
  lands on the wall-plug draw and hence on recirculating power. That is where efficiency
  can pay, and it is the honest place to ask.
* **F3. The structural claim was inflated; the true version is smaller and cleaner.** The
  first design said "both efficiencies and the wall-plug power now reach `sustainment_ok`".
  `pre_wi039_indicators.json` shows the pre-change `p_input+tie` **already reached it**.
  The one new reach in the entire comparison is **`eta_source_heat` to `sustainment_ok`**,
  and it reaches it through the installed side of the inequality only: `eta_source_heat`'s
  reachable objectives are identical to the old `eta_pin`'s, and the oracle confirms
  `p_fus`, wall load, beta and `p_aux_required` are bit-identical across eta 0.40 to 0.60
  at fixed (I, T, n). **Fusion performance does not respond to heating anywhere in this
  package.**
* **F4. The scan's I band was a 0.5 MA grid artifact on both ends.** 14.25 MA is feasible
  and cheaper than the scan's "best" point, and feasibility continues past 15.0. The first
  design's window would have reported its optimum on its own lower edge with nothing below
  it -- exactly the `20260903-priced-levers#5` failure the goal invariant bars. `I_P220`
  now brackets: 14.0 (wall-blocked, so a fence catches the bottom) through 15.25.

The arms:

- `arm-fence-p100`: (eta_source_heat, I_coil, T_i0, n_e0) at 100 MW wall-plug -- the
  printed 50 MW coupled at eta_source 0.50, restated. FENCE ANATOMY, not a search: the
  scan pre-registers the feasible set as empty (0 of 3080). **The negative is absolute,
  not window-limited** (F5): across the 245 points blocked by sustainment alone the
  minimum required auxiliary power is 92.00 MW, so the printed heating level opens only at
  `eta_source >= 0.92`. No gyrotron is within a factor of 1.5 of that.
- `arm-search-p220`: the same axes at 220 MW wall-plug (110 MW coupled at 0.50), where a
  feasible region exists, with I bracketed 14.0..15.25 MA at 0.25 MA.
- `arm-transect-eta`: a 1-D source-efficiency transect at fixed wall-plug. NOT an optimum
  hunt -- it locates the **sustainment crossing**, whose analytic value at the anchor is
  `eta* = p_aux_required / p_wallplug = 115.24 / 220 = 0.52382`, and shows the monotone
  LCOE rise on either side of it.
- `arm-couple-110`: the constant-coupled-power transect. `p_wallplug = 110 / eta_source`,
  so delivered power and heating capital are held and only the wall-plug draw moves. This
  is the arm that can answer the headline question.

**A scope extension, stated plainly rather than slipped in.** `trail.md` § T-004 scope
authorizes `p_wallplug_heat` "at the two levels the predecessor study used".
`arm-couple-110` sweeps it continuously as the reciprocal of efficiency, which is a third
level set and therefore outside the scope as written. It is added because the critique
showed the scope as written could only produce a forced answer to the study's own
question, and running hundreds of points to report "efficiency does not pay" from a
parameterization where it structurally cannot would be the worse outcome. Both axes it
moves are authorized; only their joint pattern is new. Recorded here and in the trail so
the round review sees the extension rather than discovering it.

NOT swept, and traced as declined groups in `axes.json` with their indicators:
`eta_couple_heat`, `R`+tie and `a` (the wall half's levers, round 2's), `B_max` (still
unpriced; WI-038 is its vehicle, after WI-040), and `j_wp` (checked by the critique and
found inert: a 53% swing moves LCOE by 0.03% and moves B_peak, wall load and
p_aux_required not at all).

**On `eta_couple_heat`** (F6): the first design declined it on the argument that sweeping
an unmeasured assumption "reads as knowledge the model does not have". That argument is
wrong -- a sensitivity to an assumption is how fragility is shown. The real reason is
**degeneracy**: the two efficiencies enter the fence only as their product, so sweeping
`eta_source` over 0.40..0.60 at `eta_couple = 1.0` already delivers the whole `eta_pin`
0.40..0.60 fence sensitivity. What must travel with every result instead: **1.00 is the
optimistic end of that assumption**, so every feasibility claim here is made at the most
generous possible coupling.

**THE CAVEAT THAT TRAVELS WITH EVERY CLAIM THIS STUDY MAKES AT 220 MW** -- not only its
fence claims (F2). `wall_load_ok` compares a flat-wall AVERAGE operand to the source's
printed PEAK limit. At 220 MW the LCOE optimum, the feasible band and the efficiency
threshold are **all** set by the wall and nothing else: LCOE falls monotonically with
density, with temperature and with decreasing current, and the only thing that stops it is
the wall. The best feasible point sits at wall load 3.949 against the 4.05 limit -- 97.5%
of it. Round 1's own research (T-001) registered three sources establishing that a
stellarator first wall is 15-30% larger in area than the circular torus this model
integrates over on the same wall-side radius, and that the peak-to-average factor is
1.5-2.1 against a shaped-wall average; combined, that is a net 1.15x to 1.83x on the
current operand. At the LOW end the best point reads 4.54 against 4.05 and is violated.
`points.csv` therefore carries shadow columns at both bounds with their verdicts, so this
is data a later reader can act on rather than a caveat they must remember.

Held per proposal (every key explicit): a = 1.3, availability = 0.85, discount_rate = 0.07,
R = 12.7 (+ R0 tie), j_wp = 118.8271604938272, eta_couple_heat = 1.0, and both dormant
direct heating terms at 0.0 (the chain is live, so they are zeroed -- coexisting would
double-count). All seven are asserted per case in `export()`, not merely intended (F7).

Three of the nine verdict columns carry no information at this pin (F8): `cond_strain_ok`
never fires across 6160 scanned candidates, `wp_stress_ok` fires 280 times but never
alone, and `tbr_ok` is unreachable from every declared axis. Four fences decide anything
here, and effectively two -- sustainment and the wall.

Lessons applied: store beside the record (`20260821-power-cycle-ab#11`); oracle-side pb and
sustainment operands exported (`#10`, `20260901-sustainment-fence#3`); `points.csv` carries
`case_id` (`20260823-magnet-technology-ab#6`); arms tagged AT CONSTRUCTION, never inferred
by value-matching afterwards (`20260903-priced-levers` critique MINOR 5); evaluability
pre-screen disclosed, never silent (`20260829-p-pump-fence`) -- and disclosed here to
exclude nothing, since `net_positive` never fires in 6160 candidates; an oracle exception
during the screen is a recorded reason, never a crash.
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
ARM_COUPLE = "arm-couple-110"
P = route.P

HELD = {"a": 1.3, "availability": 0.85, "discount_rate": 0.07, "R": 12.7,
        "j_wp": 118.8271604938272, "eta_couple_heat": 1.0,
        "p_delivered_direct_heat": 0.0, "p_coupled_direct_heat": 0.0}
BASE = {"I_coil": 15.4e6, "n_e0": 5.06e20, "T_i0": 14.63,
        "p_wallplug_heat": 100.0, "eta_source_heat": 0.50}
NE0 = 5.06e20
WALL_LOAD_LIMIT = float(json.loads(
    (route.PACKAGE_DIR / "inputs" / "stellarator_plant_params.json").read_text()
)[f"{P}wall_load_limit"])

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
I_P220 = [14.0e6, 14.25e6, 14.5e6, 14.75e6, 15.0e6, 15.25e6]  # BRACKETED (F4)
T_P100 = [14.63, 17.0, 19.0, 22.0]
T_P220 = [14.63, 16.0, 17.0, 18.0]
NE_P100 = [0.9, 1.0, 1.1, 1.2]
NE_P220 = [0.8, 0.9, 1.0, 1.1]
# The fixed-wall-plug transect brackets the SUSTAINMENT CROSSING, not an optimum (F1).
# eta* = p_aux_required / p_wallplug = 115.24 / 220 = 0.52382 at the anchor, so the list
# straddles it and shows the monotone LCOE rise on both sides.
ETA_TRANSECT = [0.35, 0.425, 0.475, 0.525, 0.575, 0.625, 0.65]   # disjoint from ETA_P220
TRANSECT_AT = {"I_coil": 14.5e6, "T_i0": 16.0, "ne_mult": 1.0, "wallplug": 220.0}

# The constant-COUPLED-power arm (F1's consequence). p_wallplug = COUPLE_TARGET / eta, so
# delivered power and heating capital are held and only the wall-plug draw moves. This is
# the parameterization in which source efficiency can actually pay, and the one the study's
# headline question needs. Anchored at the search arm's cheapest feasible point.
COUPLE_TARGET = 110.0
ETA_COUPLE = [0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70]
COUPLE_AT = {"I_coil": 14.25e6, "T_i0": 16.0, "ne_mult": 1.0}


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
    out += [point(eta, COUPLE_AT["I_coil"], NE0 * COUPLE_AT["ne_mult"],
                  COUPLE_AT["T_i0"], COUPLE_TARGET / eta, ARM_COUPLE)
            for eta in ETA_COUPLE]
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
    reason, never a crash.

    Goes through `evaluate`, the seam's published surface, rather than the private
    `_compute` the first design reached for (F9). `oracle_entry.py`'s own docstring says
    two surfaces and nothing else, and `evaluate` is the layer that fails closed on an
    unmapped output -- which is exactly the protection a pre-screen wants."""
    import oracle_entry as oe
    named = {"p_aux_required": f"{P}sustain__p_aux_required", "tau_E": f"{P}sustain__tau_E",
             "p_rad": f"{P}sustain__p_rad", "heat_coupled": f"{P}heat__p_coupled",
             "heat_delivered": f"{P}heat__p_delivered",
             "heat_wallplug_total": f"{P}heat__p_wallplug_total",
             "heat_eta_pin_eff": f"{P}heat__eta_pin_eff"}
    try:
        ch = oe.evaluate(pt)
        return ch[f"{P}pb__p_net"], {k: ch[v] for k, v in named.items()}, None
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
        for key in ("eta_couple_heat", "p_delivered_direct_heat", "p_coupled_direct_heat"):
            if abs(float(inp[f"{P}{key}"]) - HELD[key]) > 1e-12:
                raise route.RouteError(f"case moved a held heating key ({key}): {inp}")
        if abs(float(inp[f"{P}magnet__j_wp"]) - HELD["j_wp"]) > 1e-9:
            raise route.RouteError(f"case moved the declined j_wp: {inp}")
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
        # F2: the wall fence compares a flat-wall AVERAGE operand to a printed PEAK limit.
        # T-001 registered three sources bounding the correction at 1.15x to 1.83x on this
        # operand (shaped area 1.15-1.30x larger, peak-to-shaped-average 1.5-2.1). These
        # shadow columns carry that correction as DATA rather than as a caveat a reader has
        # to remember. They are NOT a claim about the honest fence -- choosing its form is
        # round 2's work on T-001's evidence.
        wl = row.get("wall_load")
        if wl is not None:
            for label, factor in (("lo", 1.15), ("hi", 1.83)):
                shadow = float(wl) * factor
                row[f"wall_load_shadow_{label}"] = shadow
                row[f"wall_load_ok_shadow_{label}"] = (
                    "satisfied" if shadow <= WALL_LOAD_LIMIT else "violated")
            row["feasible_shadow_lo"] = (
                row["feasible"] and row["wall_load_ok_shadow_lo"] == "satisfied")
        rows.append(row)
    rows.sort(key=lambda r: (r["arm_id"], r["p_wallplug_heat_MW"], r["eta_source_heat"],
                             r["I_coil_A"], r["T_i0_keV"], r["n_e0"]))
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader(); writer.writerows(rows)
    return path


def export_oracle_operands(cases, arms, path):
    """The operands the store does not record, oracle-derived and labelled, plus every
    constraint bound a fence claim is judged against.

    The pb__* and sustain__* fields are fields of multi-field modules and the evidence
    layer records only single-field float channels (ANNEX Oracle;
    `20260901-sustainment-fence#3`), so they are exported here rather than declared as
    store channels -- declaring them would yield a silent blank column. The WI-039
    heat__* channels are NOT in that category: they are single-field and do appear in
    the store, so they are in `points.csv` where they belong.
    """
    import oracle_entry as oe

    plant = json.loads((route.PACKAGE_DIR / "inputs" / "stellarator_plant_params.json").read_text())
    mfe_plant = json.loads((route.PACKAGE_DIR / "inputs" / "mfe_plant_params.json").read_text())
    bounds = {
        "beta_limit": plant[f"{P}beta_limit"],
        "wall_load_limit": plant[f"{P}wall_load_limit"],
        "B_max_T": plant[f"{P}magnet__B_max"],
        "sigma_allow_Pa": plant[f"{P}magnet__sigma_allow"],
        "recirc_threshold": mfe_plant[f"{P}recirc_ok__threshold"],
        "eps_cond_allow": plant[f"{P}magnet__eps_cond_allow"],
    }
    rows = []
    for case in cases:
        ch = oe.evaluate(dict(case.inputs))
        coupled = ch[f"{P}heat__p_coupled"]
        required = ch[f"{P}sustain__p_aux_required"]
        rows.append({
            "case_id": case.candidate_id,
            "arm_id": arms[_key(case.inputs)],
            "eta_source_heat": float(case.inputs[f"{P}eta_source_heat"]),
            "p_wallplug_heat_MW": float(case.inputs[f"{P}p_wallplug_heat"]),
            "I_coil_A": float(case.inputs[f"{P}magnet__I_coil"]),
            "n_e0": float(case.inputs[f"{P}n_e0"]),
            "T_i0_keV": float(case.inputs[f"{P}T_i0"]),
            "source": "oracle (verify_stellaris via oracle_entry); bounds from generated/inputs",
            "p_net_MW": ch[f"{P}pb__p_net"],
            "rec_frac": ch[f"{P}pb__rec_frac"],
            "q_eng": ch[f"{P}pb__q_eng"],
            "p_th_MW": ch[f"{P}pb__p_th"],
            # Both sides of the sustainment fence, which is computed-vs-COMPUTED since
            # WI-039: the installed side is the chain's coupled power, not a held key.
            "p_aux_required_MW": required,
            "p_coupled_installed_MW": coupled,
            "sustainment_margin_MW": coupled - required,
            "eta_source_crossing": (required / float(case.inputs[f"{P}p_wallplug_heat"])),
            "p_delivered_MW": ch[f"{P}heat__p_delivered"],
            "p_wallplug_total_MW": ch[f"{P}heat__p_wallplug_total"],
            "eta_pin_eff": ch[f"{P}heat__eta_pin_eff"],
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
    rows.sort(key=lambda r: (r["arm_id"], r["p_wallplug_heat_MW"], r["eta_source_heat"],
                             r["I_coil_A"], r["T_i0_keV"], r["n_e0"]))
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader(); writer.writerows(rows)
    return path


def run(record_dir: Path = HERE):
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
