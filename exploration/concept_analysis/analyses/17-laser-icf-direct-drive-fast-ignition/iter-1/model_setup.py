"""Laser ICF - Fast Ignition (D-T): 1costingfe model setup.

Concept: Proton fast ignition (Focused Energy). DPSSL compression laser
(~400 kJ/shot) + petawatt ignition laser (~150 kJ/shot) drive a cone-in-shell
D-T capsule at 10 Hz. Energy conversion via conventional Rankine steam cycle.

Modeling approach:
  - Uses LASER_IFE concept with DT fuel. All IFE-specific CAS22 accounts
    (target factory, driver, chamber) are driven by the framework defaults.
  - NOAK scenario is modeled as the long-run commercial case. FOAK is
    structurally unviable — fast ignition has not demonstrated gain > 1.
  - Net electric target is 1 GWe ("gigawatt-scale" per Callahan interview).
    This is the concept's native design point, so no result_1gw is needed.

Key deviations from framework defaults:
  1. availability = 0.75: HYLIFE-II IFE conservative baseline (vs. 0.85 MFE
     default). Focused Energy has not published an availability target.
  2. eta_th = 0.40: Conventional steam Rankine, explicitly confirmed by
     Focused Energy. No sCO2 or combined cycle.
  3. q_eng = 4.0: Framework IFE default retained. HIGHLY UNCERTAIN — fast
     ignition has not demonstrated gain > 1 at any scale. Commercial
     viability requires η_wp × G > 10; at η_wp=10% this requires G > 100.
     Focused Energy targets G = 50–100, which is marginal to non-viable at
     the commercial threshold.
  4. Dual-laser system (DPSSL compression + petawatt ignition): the
     framework models a single driver cost via driver_laser_per_mw.
     The petawatt ignition laser adds ~35–50% more driver capital with no
     published cost. This is NOT captured in the model — treat CAS22 as a
     lower bound on the true dual-driver cost.

Usage:
    uv run python model_setup.py              # print results to terminal
    uv run python model_setup.py | tee model_output.txt  # also save for synthesis stage
"""

from costingfe import ConfinementConcept, CostModel, Fuel

# ── Model construction ──────────────────────────────────────────────
model = CostModel(concept=ConfinementConcept.LASER_IFE, fuel=Fuel.DT)

# ── Plant configuration ─────────────────────────────────────────────

# Commercial power target.
# Source: focused-energy-callahan-interview.md §Power plant scale —
#   "gigawatt-scale" only; no specific number published. 1 GWe chosen
#   as the 1costingfe standard comparison point.
NET_ELECTRIC_MW = 1000.0

# Availability: HYLIFE-II conservative baseline (75%).
# Source: osti-biblio-7021072.md §HYLIFE-II baseline — 75% conservative,
#   85% sensitivity case; Focused Energy has not disclosed an availability
#   target. Using 75% given higher operational complexity (10 Hz, dual laser).
AVAILABILITY = 0.75

# Plant lifetime.
# DEFAULT: IFE analogue; Focused Energy has not published a plant lifetime.
LIFETIME_YR = 30

# DPSSL wall-plug efficiency target.
# Source: focused-energy-callahan-interview.md §Laser efficiency —
#   "one of the big thrusts for our company is to develop more efficient
#   lasers that are driven by diodes"; target ~10%.
# Confidence: medium — target stated, not demonstrated at 10 Hz / plant scale.
ETA_PIN = 0.10

# Thermal cycle efficiency (Rankine steam).
# Source: focused-energy-callahan-interview.md §Steam cycle —
#   "We will use a conventional steam cycle to convert the heat into
#   electricity." Explicitly confirmed. Rankine preset ≈ 40%.
ETA_TH = 0.40

# ── Forward computation ─────────────────────────────────────────────
result = model.forward(
    net_electric_mw=NET_ELECTRIC_MW,
    availability=AVAILABILITY,
    lifetime_yr=LIFETIME_YR,
    construction_time_yr=5.0,    # DEFAULT: IFE default (shorter than MFE, no magnets)
    interest_rate=0.07,          # DEFAULT: standard WACC
    inflation_rate=0.0245,       # DEFAULT: US CPI long-run average
    noak=True,                   # NOAK: long-run commercial scenario (FOAK not modeled;
                                 #   fast ignition physics undemonstrated)

    # ── Physics / power balance ──────────────────────────────────────
    # Engineering gain. HIGHLY UNCERTAIN. Framework IFE default retained.
    # Commercial threshold: η_wp × G > 10. At η_wp=10%, requires G > 100.
    # Focused Energy targets G = 50–100; marginal at threshold.
    # Source: osti-servlets-purl-2561299.md §Energetics —
    #   "η_wp × G > 10 required for cost competitive fusion power plant."
    # Source: focused-energy-callahan-interview.md §Gain targets —
    #   "significantly higher gains of more like 50 to 100."
    q_eng=4.0,                   # UNCERTAIN: placeholder; physics not validated

    # Repetition rate [Hz]. Commercial plant target.
    # Source: focused-energy-callahan-interview.md §Rep rate —
    #   "900,000 targets a day" → 10.4 Hz. T-STAR facility at 1 shot/60 s
    #   currently; commercial target is 10 Hz.
    # Confidence: high for target, low for demonstrated achievement.
    f_rep=10.0,

    # Laser wall-plug efficiency.
    # Source: focused-energy-callahan-interview.md §Laser efficiency.
    eta_pin=ETA_PIN,

    # Thermal conversion efficiency.
    # Source: focused-energy-callahan-interview.md §Steam cycle.
    eta_th=ETA_TH,

    # Neutron energy multiplier (Li blanket breeding reaction).
    # DEFAULT: standard IFE DT value. Blanket type undisclosed by Focused
    #   Energy; Li confirmed: focused-energy-callahan-interview.md §Tritium.
    mn=1.1,

    # Radiation fraction of fusion energy (pulsed IFE default).
    # DEFAULT: pulsed_laser_ife.yaml — f_rad=0.10.
    f_rad=0.10,

    # Subsystem / housekeeping power fractions [MW].
    # DEFAULT: pulsed_laser_ife.yaml defaults. Focused Energy has published
    #   no plant-level power balance.
    f_sub=0.03,       # Subsystem power fraction
    p_pump=1.0,       # Coolant pumping [MW]
    p_trit=10.0,      # Tritium processing [MW]
    p_house=4.0,      # Housekeeping [MW]
    p_cryo=0.5,       # Cryogenic systems [MW]
    p_target=1.0,     # Target factory auxiliary power [MW]

    # ── Radial build geometry (spherical chamber) ─────────────────────
    # Chamber radius (plasma_t for IFE = chamber inner radius).
    # DEFAULT: pulsed_laser_ife.yaml — 4.0 m. No chamber design disclosed
    #   by Focused Energy.
    plasma_t=4.0,

    # Blanket thickness.
    # DEFAULT: pulsed_laser_ife.yaml — 0.80 m. Blanket type undisclosed.
    blanket_t=0.80,

    # High-temperature shield.
    # DEFAULT: pulsed_laser_ife.yaml — 0.25 m.
    ht_shield_t=0.25,

    # Primary structure thickness.
    # DEFAULT: pulsed_laser_ife.yaml — 0.15 m.
    structure_t=0.15,

    # Vacuum vessel thickness.
    # DEFAULT: pulsed_laser_ife.yaml — 0.10 m.
    vessel_t=0.10,

    # ── Cost overrides ────────────────────────────────────────────────
    # No CAS-level overrides applied. All costs derive from framework
    # NOAK defaults. Key notes:
    #
    # CAS22 driver (driver_laser_per_mw default = 8.0 M$/MW):
    #   Calibrated to NOAK DPSSL (~$80/J laser energy at 10% WPE).
    #   This is a LOWER BOUND for Focused Energy because:
    #   (a) The petawatt ignition laser (~150 kJ/shot, ~37% of total driver
    #       energy) has no commercial analog and likely costs more per joule
    #       than the DPSSL compression laser. No cost estimate published.
    #       Source: analysis.md §Challenge 2.
    #   (b) FOAK DPSSL cost class: $700–1,000/J (XEC white paper).
    #       Source: xec-20260224-commercialization-of-lfe-whtppr-shared-24-feb.md
    #       §DPSSL costs. NOAK requires ~10× diode cost learning to reach $80/J.
    #   (c) Diode cost floor requirement: $0.01/W wall-plug.
    #       Source: osti-servlets-purl-2561299.md §Laser driver requirements.
    #
    # CAS22 target factory (target_factory_base default = 244 M$ at 1 GWe):
    #   Pearl™ cone-in-shell geometry is more complex than symmetric CHS
    #   targets, likely more expensive per unit. No Focused Energy cost
    #   estimate published. Source: analysis.md §Challenge 4.
    #
    # CAS70 O&M:
    #   Framework default (52 M$/yr at 1 GWe for DT) is UNCERTAIN for laser
    #   IFE. Laser optics replacement at 10 Hz, final optics damage
    #   accumulation, and pulsed power maintenance drive higher O&M.
    #   IFE analogue estimate: 5–8% of direct capital/year.
    #   Source: osti-servlets-purl-6137961.md §Summary.
    #   At assumed direct CAPEX ~$3B, this implies $150–240 M$/yr O&M,
    #   significantly higher than framework default.
)

# ── Results ─────────────────────────────────────────────────────────
c = result.costs
pt = result.power_table

print("Laser ICF — Fast Ignition D-T (Focused Energy)")
print("NOAK | 1 GWe | 75% availability | 30 yr | Rankine steam")
print(f"LCOE: {c.lcoe:.1f} $/MWh | Overnight: {c.overnight_cost:.0f} $/kW")
print(f"Fusion: {pt.p_fus:.0f} MW | Net: {pt.p_net:.0f} MW | Q_eng: {pt.q_eng:.1f}")
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

# ── CAS22 detail ─────────────────────────────────────────────────────
print("\nCAS22 sub-account detail:")
print(f"  {'Account':<16} {'M$':>10}")
print("  " + "-" * 28)
for key, val in sorted(result.cas22_detail.items()):
    if key != "C220000":
        print(f"  {key:<16} {float(val):>10.1f}")
print("  " + "-" * 28)
print(f"  {'C220000 Total':<16} {float(result.cas22_detail.get('C220000', c.cas22)):>10.1f}")

# ── Key Assumptions ──────────────────────────────────────────────────
print("""
Key Assumptions:
  1. q_eng = 4.0: HIGHLY UNCERTAIN. Fast ignition has not demonstrated
     gain > 1. Commercial threshold requires G > 100 at 10% WPE.
     If G = 50 (Focused Energy minimum target), q_eng < 1.
  2. Dual-laser cost not modeled: petawatt ignition laser (~150 kJ/shot)
     adds ~35–50% more driver capital vs. a single DPSSL system.
     CAS22 driver is a LOWER BOUND on the true dual-driver cost.
  3. NOAK diode cost learning assumed: framework default (8.0 M$/MW)
     requires ~10× diode cost reduction from current FOAK ($700–1,000/J).
  4. eta_th = 0.40 (Rankine): confirmed by Focused Energy; no exotic cycle.
  5. availability = 0.75: HYLIFE-II IFE conservative analogue.
     Final optics replacement at 10 Hz is an unresolved engineering problem.
  6. O&M likely underestimated: laser optics replacement cycle not modeled.
     IFE analogues suggest 5–8% of direct CAPEX/yr vs. ~2% framework default.
  7. Pearl™ cone-in-shell target fabrication at 900,000/day undemonstrated.
     Target cost uncertainty: $0.10–$1.00/target; not included as variable cost.
""")

# ── Sensitivity Analysis ─────────────────────────────────────────────
sens = model.sensitivity(result.params)

print("Sensitivity (elasticity = %LCOE / %param)")
print("-" * 48)

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
