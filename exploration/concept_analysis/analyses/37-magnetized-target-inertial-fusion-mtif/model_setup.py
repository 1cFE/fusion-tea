"""Magnetized Target Impact Fusion — MTIF (D-D) — NearStar Fusion.

Modeling approach:
    NearStar uses a plasma-armature railgun to accelerate a pre-magnetized 50 g D-D
    fuel capsule at ~10 km/s (Mach 30) into a molten-Pb target chamber at 1 Hz.
    The Pb pool absorbs kinetic and fusion energy, driving a steam Rankine cycle via
    an intermediate heat exchanger — consistent with the company's coal-plant retrofit
    framing. No external confinement magnets; the target pellet carries a seed
    magnetic field embedded at manufacture.

    D-D fuel eliminates the tritium startup inventory and breeding blanket required
    by all D-T concepts, but raises the ignition threshold by ~100× relative to D-T
    at the same temperature. No NearStar experimental results, gain targets, or
    capital cost estimates are publicly available. This model is therefore driven
    almost entirely by framework defaults with UNCERTAIN flags on every parameter
    that lacks a public source anchor.

Concept choice rationale:
    ConfinementConcept.MAG_TARGET is the closest framework match: pulsed,
    spherical-chamber geometry, liquid-metal first wall, no steady-state magnets,
    IFE/MIF target factory cost structure.

Key deviations from framework defaults:
    1. eta_th = 0.35  — subcritical steam Rankine (coal-plant retrofit analogue)
                         instead of default 0.40 supercritical Rankine.
    2. eta_pin = 0.25 — railgun wall-plug efficiency, midpoint of 20–40 % range
                         documented for experimental plasma-armature systems;
                         no NearStar-specific value is available.
    3. p_coils = 0.0  — no external confinement coils; seed field is pellet-embedded.
    4. p_trit  = 1.0  — secondary D-D tritium handling only (not primary fuel).
    5. availability = 0.40 — rail replacement at 1 Hz severely constrains uptime;
                         documented defense-program upper bound is ~400 shots per
                         rail (contested; early systems: ~12 shots), implying
                         replacement every ~7 min (400 s) of 1 Hz operation.
                         0.40 is highly optimistic and may be unachievable at
                         any realistic rail life.
    6. Native design point: 200 MWe (SPECULATIVE — no NearStar power target exists;
                         chosen as minimum plausible commercial scale given 1 Hz
                         driver; actual achievability depends on undemonstrated D-D
                         gain of ~100–300).
    7. blanket_t adjusted for molten-Pb non-breeding first wall (no TBR requirement).

Usage:
    uv run python model_setup.py              # print results to terminal
    uv run python model_setup.py | tee model_output.txt  # also save for synthesis stage
"""

from costingfe import ConfinementConcept, CostModel, Fuel

# ── Model instantiation ─────────────────────────────────────────────────────
model = CostModel(concept=ConfinementConcept.MAG_TARGET, fuel=Fuel.DD)

# ── Plant configuration ─────────────────────────────────────────────────────
# Native design point: 200 MWe
# UNCERTAIN: NearStar discloses no design-point power. 200 MWe is the minimum
# plausible commercial scale for a 1 Hz / >1 MJ-kinetic-energy driver.
# At required gain of ~100–300 (analysis.md §Section 2, Challenge 2), the
# implied fusion yield per shot is ~200–600 MJ — far beyond any demonstrated
# D-D inertial confinement performance.
_NATIVE_MWE = 200.0

_SHARED_KWARGS = dict(
    # ── Economic boundary conditions ────────────────────────────────────────
    availability=0.40,          # UNCERTAIN: at documented defense-program upper bound
                                # of ~400 shots/rail, replacement is required every
                                # ~7 min (400 s) of continuous 1 Hz operation.
                                # 0.40 is highly optimistic; actual availability
                                # depends on replacement time vs. firing window.
                                # Source: en-wiki-railgun.md; analysis.md §S2 Ch.3
    lifetime_yr=30,             # DEFAULT: standard fusion plant economic lifetime
    n_mod=1,
    construction_time_yr=4.0,  # DEFAULT: pulsed_mag_target.yaml; compact chamber,
                                # no superconducting magnet assembly bottleneck

    # ── Power balance ───────────────────────────────────────────────────────
    eta_pin=0.25,               # UNCERTAIN: railgun wall-plug (kinetic) efficiency.
                                # Experimental plasma-armature railguns: 20–40 %.
                                # No NearStar-specific value disclosed.
                                # Source: analysis.md §S5, Missing Parameters
                                # "Railgun wall-plug electrical efficiency"
    f_rep=1.0,                  # Repetition rate [Hz] — confirmed.
                                # Source: nearstar-website-summary.md §Concept
                                # ("once per second")
    mn=1.1,                     # DEFAULT: neutron energy multiplier (molten-Pb blanket
                                # captures 2.45 MeV D-D neutrons; no tritium breeding)
    f_rad=0.08,                 # DEFAULT for DD (pulsed): from costing_constants.yaml
    f_sub=0.03,                 # DEFAULT: subsystem power fraction
    p_coils=0.0,                # No external confinement magnets; seed field is
                                # embedded in pre-magnetized pellet.
                                # Source: dossier.md §Magnet Type; analysis.md §S5
                                # "Magnet type: None (external confinement)"
    p_trit=1.0,                 # D-D secondary tritium handling only; small relative
                                # to D-T tritium plant (~10 MW). No primary tritium
                                # breeding or containment required.
                                # Source: analysis.md §S3 "Tritium Handling (TRL N/A)"
    p_target=2.0,               # DEFAULT: target/liner factory power [MW];
                                # capsule fabrication at 1 Hz (28M/yr) requires
                                # automated production line — cost structure unknown
    p_pump=1.0,                 # DEFAULT: Pb primary loop and feedwater pumping
    p_house=4.0,                # DEFAULT: housekeeping (controls, lighting, HVAC)
    p_cryo=0.0,                 # No cryogenic magnets; seed-field pellets do not
                                # require plant-scale cryogenics
                                # Source: analysis.md §S3 "Pellet Pre-Magnetization"

    # ── Radial build (spherical chamber geometry) ───────────────────────────
    R0=0.0,                     # Not used for spherical chamber
    plasma_t=3.0,               # DEFAULT: chamber radius [m]; pulsed_mag_target.yaml
    blanket_t=0.80,             # DEFAULT: first-wall + molten-Pb zone thickness [m];
                                # no tritium breeding required (D-D fuel) but Pb pool
                                # must provide neutron shielding and heat extraction.
                                # Source: nearstar-website-summary.md §Concept
                                # (molten Pb first wall confirmed)
    ht_shield_t=0.20,           # DEFAULT: high-temperature shield
    structure_t=0.15,           # DEFAULT: primary structure
    vessel_t=0.10,              # DEFAULT: outer vessel

    # ── No cost_overrides — all CAS accounts use framework defaults ─────────
    # No capital cost data exists for any NearStar subsystem.
    # Source: analysis.md §S5, Missing Parameters "Capital cost: truly-unknown"
    # The driver cost is computed via driver_mag_target_per_mw ($3 M$/MW_driver,
    # calibrated for pneumatic-piston MIF — a potentially low estimate for
    # a plasma-armature railgun; no NearStar-specific railgun capital data exists).
)

# ── Forward pass: native design point (200 MWe) ─────────────────────────────
result = model.forward(net_electric_mw=_NATIVE_MWE, **_SHARED_KWARGS)

# ── Forward pass: scaled to 1 GWe ───────────────────────────────────────────
# override_reference_mw tells the framework that cost_overrides (none here)
# are calibrated at _NATIVE_MWE, and to scale them to 1000 MWe using
# per-account scaling laws.
result_1gw = model.forward(
    net_electric_mw=1000.0,
    override_reference_mw=_NATIVE_MWE,
    **_SHARED_KWARGS,
)

# ── Results: native design point ────────────────────────────────────────────
c = result.costs
pt = result.power_table

print("=" * 65)
print("MTIF D-D — NearStar Fusion")
print("(MAG_TARGET / DD — native 200 MWe, 40 % availability, 30 yr)")
print("=" * 65)
print()
print("*** ALL RESULTS HIGHLY SPECULATIVE — see Key Assumptions ***")
print("*** D-D ignition physics for this geometry is undemonstrated ***")
print()
print(f"LCOE:            {c.lcoe:.1f} $/MWh")
print(f"Overnight cost:  {c.overnight_cost:.0f} $/kW")
print(f"Fusion power:    {pt.p_fus:.0f} MW")
print(f"Net electric:    {pt.p_net:.0f} MWe")
print(f"Q_eng:           {pt.q_eng:.2f}")
print()

cas = [
    ("CAS10", "Preconstruction",          c.cas10),
    ("CAS21", "Buildings",                c.cas21),
    ("CAS22", "Reactor Plant Equipment",  c.cas22),
    ("CAS23", "Turbine Plant",            c.cas23),
    ("CAS24", "Electrical Plant",         c.cas24),
    ("CAS25", "Miscellaneous",            c.cas25),
    ("CAS26", "Heat Rejection",           c.cas26),
    ("CAS27", "Special Materials",        c.cas27),
    ("CAS28", "Digital Twin",             c.cas28),
    ("CAS29", "Contingency",              c.cas29),
    ("CAS30", "Indirect Costs",           c.cas30),
    ("CAS40", "Owner's Costs",            c.cas40),
    ("CAS50", "Supplementary",            c.cas50),
    ("CAS60", "IDC",                      c.cas60),
    ("CAS70", "O&M (annualized)",         c.cas70),
    ("CAS80", "Fuel (annualized)",        c.cas80),
    ("CAS90", "Financial",                c.cas90),
]

print(f"{'Code':<8} {'Account':<28} {'M$':>10}")
print("-" * 48)
for code, name, val in cas:
    print(f"{code:<8} {name:<28} {float(val):>10.1f}")
print("-" * 48)
print(f"{'':8} {'Total Capital':<28} {float(c.total_capital):>10.1f}")
print()

# ── CAS22 detail ─────────────────────────────────────────────────────────
print("CAS22 sub-accounts:")
for k, v in result.cas22_detail.items():
    print(f"  {k}  {float(v):>10.1f} M$")
print()

# ── Scaled 1 GWe result ───────────────────────────────────────────────────
c1 = result_1gw.costs
pt1 = result_1gw.power_table
print("=" * 65)
print("Scaled to 1 GWe (per-account scaling from 200 MWe native)")
print("=" * 65)
print(f"LCOE:            {c1.lcoe:.1f} $/MWh")
print(f"Overnight cost:  {c1.overnight_cost:.0f} $/kW")
print(f"Fusion power:    {pt1.p_fus:.0f} MW")
print(f"Net electric:    {pt1.p_net:.0f} MWe")
print(f"Q_eng:           {pt1.q_eng:.2f}")
print()

# ── Key Assumptions ───────────────────────────────────────────────────────
print("=" * 65)
print("Key Assumptions (all HIGHLY UNCERTAIN)")
print("=" * 65)
print("""
PHYSICS (blocking gaps — concept viability not established):
  D-D ignition:    Undemonstrated for railgun-driven magnetized target.
                   D-D cross-section ~100x lower than D-T at 10–30 keV.
                   No NearStar gain target, simulation, or experiment published.
  Required gain:   ~100–300 target fusion gain implied by energy balance at
                   1 Hz, >1 MJ driver, ~35% thermal efficiency.
                   (analysis.md §S2, Challenge 2)
  Rail lifetime:   Documented defense-program rail life: ~12 shots (early systems)
                   to a contested ~400 shots at unconfirmed full power; Navy 3,000-shot
                   development target not achieved before program cancellation (2021).
                   Plant requirement: ~840 million shots over 30 years (1 Hz, 40% CF).
                   Gap: 6–7 orders of magnitude vs. demonstrated; 5 orders vs. target.
                   Source: en-wiki-railgun.md; analysis.md §S2, Challenge 3

ASSUMED (no public source):
  Net power:       200 MWe — speculative; no NearStar design-point disclosed.
  eta_pin:         0.25 — midpoint of 20–40% experimental railgun range.
  Availability:    0.40 — dominated by rail replacement (pessimistic estimate).
  eta_th:          0.35 — subcritical Rankine, inferred from coal retrofit framing.
  All capital costs: framework defaults (no NearStar subsystem data available).
  Driver cost:     driver_mag_target_per_mw default ($3 M$/MW_driver, pneumatic
                   piston calibration) — likely underestimates railgun capital.

GENUINE ADVANTAGES (relative to D-T concepts):
  No tritium startup inventory (~1 kg at >$35,000/g avoided).
  No REBCO superconducting tape (no external magnets).
  No lithium-6 enrichment or breeding blanket.
  No beryllium neutron multiplier.
  Secondary D-D tritium inventory is small (no primary T breeding cycle).
""")

# ── Sensitivity analysis ──────────────────────────────────────────────────
sens = model.sensitivity(result.params)

print("=" * 65)
print("Sensitivity (elasticity = %ΔLCOE / %Δparam) — native 200 MWe")
print("=" * 65)

print("\nEngineering levers:")
for k, v in sorted(sens["engineering"].items(), key=lambda x: abs(x[1]), reverse=True):
    print(f"  {k:<36} {v:+.4f}")

print("\nFinancial:")
for k, v in sorted(sens["financial"].items(), key=lambda x: abs(x[1]), reverse=True):
    print(f"  {k:<36} {v:+.4f}")

print("\nCosting constants (top 15):")
costing = sorted(sens["costing"].items(), key=lambda x: abs(x[1]), reverse=True)
for k, v in costing[:15]:
    print(f"  {k:<36} {v:+.4f}")

# ── Rail Consumable O&M Sweep (CF-F1) ────────────────────────────────────────
# The framework's CAS70 (~$25 M/yr) reflects generic fusion O&M scaling.
# Rail replacement is a concept-specific consumable that dominates OPEX but
# has no explicit cost line in the framework.  This sweep quantifies the
# delta-LCOE penalty as a function of two independently uncertain inputs:
#   rail_replacement_cost ($) — material + labour per rail swap
#   rail_life_shots          — shots per rail before replacement
#
# Documented range: 12 shots (early Navy tests) → contested 400 shots at
# unconfirmed full power (en-wiki-railgun.md).  3,000-shot target was never
# achieved.  100,000 shots is aspirational / pre-cancellation goal.
#
# delta_LCOE ($/MWh) = rail_cost_per_shot * shots_per_year / energy_mwh_per_year
#   rail_cost_per_shot   = rail_replacement_cost / rail_life_shots
#   shots_per_year       = f_rep * seconds_per_year * availability
#   energy_mwh_per_year  = net_electric_mw * 8760 * availability

_AVAIL = 0.40
_F_REP = 1.0   # Hz
_SHOTS_PER_YEAR = _F_REP * 365.25 * 24 * 3600 * _AVAIL   # ~12.6 M shots/yr
_ENERGY_MWH_YR  = _NATIVE_MWE * 8760 * _AVAIL             # ~700,800 MWh/yr

_RAIL_COSTS = [1_000, 10_000, 100_000, 1_000_000]   # $/replacement
_RAIL_LIVES = [12, 400, 3_000, 100_000]              # shots/replacement before service

print()
print("=" * 65)
print("Rail Consumable O&M — delta-LCOE ($/MWh) above framework CAS70")
print("Native 200 MWe, 40% availability, 1 Hz, 30 yr plant life")
print(f"Shots/yr: {_SHOTS_PER_YEAR:,.0f}   Energy/yr: {_ENERGY_MWH_YR:,.0f} MWh")
print("=" * 65)
print(f"  {'Replacement cost':>18}  {'Rail life (shots/rail)':>24}")
print(f"  {'':>18}  {'12':>8} {'400':>8} {'3,000':>8} {'100k':>8}")
print(f"  {'':>18}  {'(early)':>8} {'(doc ub)':>8} {'(target)':>8} {'(aspire)':>8}")
print("-" * 65)
for rc in _RAIL_COSTS:
    row = []
    for rl in _RAIL_LIVES:
        delta = (rc / rl) * _SHOTS_PER_YEAR / _ENERGY_MWH_YR
        row.append(f"{delta:>8,.0f}")
    tag = f"${rc:>10,.0f}/swap"
    print(f"  {tag}  {''.join(row)}")
print()
print("  Framework CAS70 (baseline O&M):  ~25 M$/yr → ~36 $/MWh at 200 MWe, 40% CF")
print("  Breakeven rail life for +10 $/MWh penalty at $10k/swap:")
_breakeven = (10_000 * _SHOTS_PER_YEAR) / (10.0 * _ENERGY_MWH_YR)
print(f"    {_breakeven:,.0f} shots/rail  (vs. documented max ~400 shots)")

# ── Driver Cost Scenarios (CF-F2) ─────────────────────────────────────────────
# The framework default `driver_mag_target_per_mw` ($3 M$/MW_driver) is
# calibrated for pneumatic-piston MIF (General Fusion analogue).  Plasma-
# armature railguns at 10 km/s require pulsed-power infrastructure, high-
# current switching, and precision firing circuits — a qualitatively different
# capital topology with no NOAK cost basis.
#
# Defense EML programs (Navy, DARPA) operated at $10s–100s M$ per
# installation at much lower duty cycles than commercial fusion requires.
# This scenario sweep spans 1×–10× of the pneumatic baseline to bound the
# uncertainty.
#
# Sensitivity of LCOE to driver_mag_target_per_mw is reported in the
# costing-constants sensitivity block above (look for "driver_mag_target_per_mw").

_DRIVER_BASELINE_PER_MW = 3.0   # M$/MW_driver — pneumatic piston default
_DRIVER_MULTS = [1, 2, 5, 10]

print()
print("=" * 65)
print("Driver Capital Cost Scenarios — Railgun vs. Pneumatic Piston Baseline")
print("Native 200 MWe; all other parameters held at baseline values")
print(f"Baseline: driver_mag_target_per_mw = {_DRIVER_BASELINE_PER_MW} M$/MW_driver")
print("=" * 65)
print(f"  {'Mult':>6}  {'M$/MW_driver':>14}  {'LCOE ($/MWh)':>14}  {'ΔLCOE':>10}")
print("-" * 55)
_baseline_lcoe = float(result.costs.lcoe)
for mult in _DRIVER_MULTS:
    _r = model.forward(
        net_electric_mw=_NATIVE_MWE,
        driver_mag_target_per_mw=_DRIVER_BASELINE_PER_MW * mult,
        **_SHARED_KWARGS,
    )
    _lcoe = float(_r.costs.lcoe)
    _delta = _lcoe - _baseline_lcoe
    _note = "  [pneumatic piston baseline]" if mult == 1 else f"  +{_delta:.1f} $/MWh"
    print(f"  {mult}×{'':<4}  {_DRIVER_BASELINE_PER_MW * mult:>14.1f}  {_lcoe:>14.1f}{_note}")
print()
print("  Railgun analog: BAE/GA EML systems cost $10s–100s M$ per installation")
print("  at << 1 Hz duty cycle. NearStar requires 1 Hz continuous: 5–10× may")
print("  underestimate long-run NOAK railgun capital at commercial duty cycle.")
