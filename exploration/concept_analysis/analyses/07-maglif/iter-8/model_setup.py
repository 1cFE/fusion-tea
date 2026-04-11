"""MagLIF (D-T) — 1costingfe cost model setup.

Concept: Magnetized Liner Inertial Fusion (MagLIF), D-T fuel.
Companies: Pacific Fusion (Santa Cruz, CA), Fuse Energy Technologies (San Leandro, CA).

Modeling Approach
-----------------
MagLIF is a pulsed MIF concept whose dominant cost categories — pulsed power driver
capital, per-shot consumables (liner + RTL), and rep-rated chamber clearing — have no
equivalents in the MFE database that underpins 1costingfe's reference scaling laws.
The framework is therefore used in a constrained mode:

  - ConfinementConcept.MAG_TARGET provides the structural skeleton (MIF/MagLIF layout).
  - cost_overrides inject Z-IFE reference values for the driver and consumable accounts
    that have no framework analogue.
  - All other CAS accounts (buildings, BOP, financial) are computed by the framework
    at the Z-IFE reference design point (1000 MWe, 0.5 Hz frozen-FLiBe RTL).

Key Deviations from Framework Defaults
---------------------------------------
1. Driver capital (C220104): overridden to $372M (Z-IFE LTD median); the default
   "heating & CD" account has no physical meaning for a pulsed power driver.
2. RTL + target factory (target_factory in CAS22): framework default $244M applies to
   laser IFE scale; for MagLIF the RTL factory capital is captured by overriding
   C220600 (other equipment) to carry a Z-IFE-analogous estimate.
3. Blanket (C220101): overridden to Z-IFE reference FLiBe thick-liquid-wall design
   estimate; the framework's PbLi volume-based cost does not apply.
4. Coils (C220103): zeroed — MagLIF has no superconducting magnets; the axial field
   coils are pulsed copper (cost embedded in driver account).
5. DEC (C220109): zeroed — no direct energy conversion in baseline D-T MagLIF.

Reference Design Point
-----------------------
  - Z-IFE "best LTD case": 1000 MWe net, single chamber, 0.5 Hz, frozen-FLiBe RTL.
  - Source: z-ife-sand2006-7148-thermal-cycles.md §3.1.1 and §3.1.2.
  - COE from source: 7.0 ¢/kWeh. Target LCOE from this script: comparable range.

Usage:
    uv run python model_setup.py              # print results to terminal
    uv run python model_setup.py | tee model_output.txt  # also save for synthesis stage
"""

import sys

from costingfe import ConfinementConcept, CostModel, Fuel

# ── Model creation ──────────────────────────────────────────────────────────
model = CostModel(concept=ConfinementConcept.MAG_TARGET, fuel=Fuel.DT)

# ── Plant configuration ──────────────────────────────────────────────────────
# Z-IFE reference design (z-ife-sand2006-7148-thermal-cycles.md §3.1.1)

# Customer requirements
NET_ELECTRIC_MW = 1000.0    # MWe; Z-IFE reference plant size
                             # Source: z-ife-sand2006-7148-thermal-cycles.md §3.1.1

# UNCERTAIN: availability.  Z-IFE assumes 85% without attribution.
# If thick-liquid-wall solid replacement is eliminated, 85-90% is plausible;
# if chamber clearing or RTL issues arise, 60-75% is more realistic.
AVAILABILITY = 0.85         # UNCERTAIN: analysis.md §Section 5 (capacity factor row);
                             # used because it is the only published assumption

LIFETIME_YR = 30            # DEFAULT: consistent with fusion plant finance conventions;
                             # no MagLIF-specific data
CONSTRUCTION_TIME_YR = 4.0  # DEFAULT: from mif_mag_target.yaml; plausible for a
                             # modular pulsed-power plant with simpler magnetics

INTEREST_RATE = 0.0966      # Fixed charge rate 9.66%;
                             # Source: z-ife-sand2006-7148-thermal-cycles.md §3.1.1
INFLATION_RATE = 0.0245     # DEFAULT: consistent with tokamak reference example
NOAK = False                # FOAK — first commercial plant in the 2030s per Pacific
                             # Fusion timeline; no learning curve applicable yet

# ── Power balance ────────────────────────────────────────────────────────────
# Driver and thermal parameters from Z-IFE study

# Pulsed power driver for MagLIF acts as both "input power" and "primary energy source";
# in MIF pulsed mode, p_driver is the sustained equivalent electrical power into the driver.
# UNCERTAIN: the framework's p_input maps to continuous driver power draw;
# for a pulsed system this is rep_rate × E_stored / eta_pin.
# At 0.5 Hz, 42 MJ stored, 60% LTD efficiency: p_driver ≈ 35 MW parasitic draw.
P_DRIVER_MW = 35.0          # UNCERTAIN: derived from Z-IFE §3.1.1.5 (42 MJ stored,
                             # 0.5 Hz, 60% LTD efficiency → 42×0.5/0.6 ≈ 35 MW)

ETA_TH = 0.42               # Thermal conversion efficiency, combined Brayton-Rankine,
                             # steel chamber baseline (near-term achievable);
                             # Source: z-ife-sand2006-7148-thermal-cycles.md §3.2

ETA_PIN = 0.60              # LTD driver wall-plug efficiency;
                             # Source: z-ife-sand2006-7148-thermal-cycles.md §3.1.1.5
                             # (2005 workshop estimate: 60%)
                             # NOTE: IMG architecture claims ~90% efficiency
                             # (analysis.md §Section 5; arxiv-2408-15206 §3.2),
                             # but this is unverified at plant scale.

MN = 1.1                    # DEFAULT: standard D-T neutron energy multiplier;
                             # no MagLIF-specific blanket multiplier published

# RTL steel remanufacturing parasitic load was 170 MWe for steel RTL baseline;
# frozen-FLiBe RTL eliminates this. In 0.5 Hz frozen-FLiBe baseline: no RTL factory
# parasitic load. f_sub captures remaining recirculating power fraction.
F_SUB = 0.03                # DEFAULT: residual recirculating power fraction;
                             # steel RTL 170 MWe penalty is NOT present in this scenario
                             # Source: z-ife-sand2006-7148-thermal-cycles.md §3.1.1.3
                             # (steel RTL case eliminated by frozen-FLiBe selection)

# UNCERTAIN: target factory power. Frozen-FLiBe RTL factory power not quantified.
# z-ife uses p_target = 2 MW as a small ancillary load. Used here as placeholder.
P_TARGET_MW = 2.0           # UNCERTAIN: from mif_mag_target.yaml default;
                             # actual Z-IFE frozen-FLiBe factory power not published

P_TRIT = 10.0               # DEFAULT: standard D-T tritium processing power [MW]
P_HOUSE = 4.0               # DEFAULT from mif_mag_target.yaml
P_PUMP = 1.0                # DEFAULT from mif_mag_target.yaml; FLiBe pump power
P_CRYO = 0.2                # DEFAULT from mif_mag_target.yaml; minimal cryo
P_COILS = 0.0               # Zero — no superconducting magnets; pulsed copper coils
                             # are part of driver energy budget, not a separate AC load;
                             # analysis.md §Key Differentiators: "No superconducting magnets"

# ── Chamber geometry ─────────────────────────────────────────────────────────
# Z-IFE reference: 4 m radius spherical chamber, 80 cm FLiBe blanket, 20 cm Al wall
# Source: z-ife-power-plant-concept.md §Abstract (cited in analysis.md §Section 5)
PLASMA_T = 4.0              # Chamber radius [m]; Z-IFE 4 m radius
                             # Source: analysis.md §Section 5, blanket geometry row
BLANKET_T = 0.80            # FLiBe thick-liquid-wall blanket thickness [m];
                             # Source: z-ife-sand2006-7148-thermal-cycles.md (via analysis.md §Section 5)
HT_SHIELD_T = 0.20          # 20 cm 6061-T6 Al first-wall structural wall;
                             # Source: z-ife-power-plant-concept.md §Abstract
STRUCTURE_T = 0.15          # DEFAULT from mif_mag_target.yaml
VESSEL_T = 0.10             # DEFAULT from mif_mag_target.yaml
R0 = 0.0                    # Not used for spherical chamber (mag_target concept)

# ── CAS account cost overrides ───────────────────────────────────────────────
# All overrides in M$ (2024$), unless noted.
# Basis: Z-IFE direct capital decomposition (z-ife-sand2006-7148-thermal-cycles.md §3.1.2)
# and analysis.md §Section 2 "CAS-level cost structure" table.

cost_overrides = {
    # C220103 — Coils / Magnet System
    # MagLIF has NO superconducting magnets. Framework default computes HTS coil cost
    # from geometry, which is irrelevant. Zeroed.
    # Source: analysis.md §Key Differentiators ("No superconducting magnets")
    "C220103": 0.0,

    # C220104 — Driver / Heating & Current Drive
    # In MagLIF, this account is the pulsed power driver (capacitor banks, switches,
    # transmission lines). Z-IFE LTD median estimate: $372M for a 1 PW LTD driver.
    # Scaling: C = 372 × (TW/1000)^0.6 M$ from z-ife §3.1.2.
    # Modern IMG architecture (Pacific Fusion DS) may be 5–10× cheaper (analysis.md §S2,
    # Challenge 3), but no published plant-scale estimate exists.
    # Using Z-IFE LTD median as a conservative reference case.
    # Source: z-ife-sand2006-7148-thermal-cycles.md §3.1.2 (analysis.md §Section 5)
    "C220104": 372.0,           # M$; LTD architecture median; UNCERTAIN ±50%

    # C220101 — First Wall + Blanket
    # Z-IFE: FLiBe thick-liquid-wall blanket, 80 cm, spherical, 4 m radius.
    # Framework default uses PbLi volume-based unit cost, which does not apply.
    # Z-IFE chamber + first-wall cost (steel) estimated at ~$46M from the study's
    # direct capital split: Total direct ≈ $575M; driver $372M; chamber ~$46M;
    # BOP ~$157M (applying proportions from the Z-IFE §3.1.2 discussion).
    # UNCERTAIN: the Z-IFE breakdown does not separately itemize blanket vs. FW.
    # Using $50M as representative of the FLiBe blanket + Al first-wall account.
    "C220101": 50.0,            # UNCERTAIN: M$; Z-IFE chamber analogue; ±40%
                                 # Source: z-ife-sand2006-7148-thermal-cycles.md §3.1.2

    # C220108 — Divertor
    # MagLIF has no divertor. The spherical thick-liquid-wall chamber handles plasma
    # exhaust and debris removal between shots. The framework default computes a
    # divertor cost that is physically absent in this concept.
    # Source: analysis.md §Key Differentiators ("pulsed operation, not continuous")
    "C220108": 0.0,

    # C220109 — Direct Energy Conversion
    # No DEC in baseline D-T MagLIF (unlike Helion D-He3 which recovers EM energy).
    # Source: analysis.md §Key Differentiators vs. Helion (DEC not present for MagLIF DT)
    "C220109": 0.0,

    # C220600 — Other Reactor Plant Equipment
    # In MagLIF, this is the primary home for the RTL/target factory capital
    # and any remaining pulsed-power auxiliaries not captured in C220104.
    # Z-IFE frozen-FLiBe RTL factory cost not separately itemized; the study notes
    # it eliminates the 170 MWe steel remanufacturing plant. As a proxy:
    # analogous laser IFE target factory at 1 GWe ref = $244M (framework default);
    # MagLIF RTL factory is simpler (mm tolerances, metallic liner, no cryo for
    # frozen-FLiBe variant) → use ~50% of laser IFE target factory: $120M.
    # UNCERTAIN: cryo ice-layer target factory cost is unknown and could be larger.
    "C220600": 120.0,           # UNCERTAIN: M$; RTL + target factory capital;
                                 # ±100% (no published estimate for frozen-FLiBe RTL factory)
                                 # analysis.md §Section 2, Challenge 2
}

# ── Forward pass ─────────────────────────────────────────────────────────────
result = model.forward(
    net_electric_mw=NET_ELECTRIC_MW,
    availability=AVAILABILITY,
    lifetime_yr=LIFETIME_YR,
    n_mod=1,
    construction_time_yr=CONSTRUCTION_TIME_YR,
    interest_rate=INTEREST_RATE,
    inflation_rate=INFLATION_RATE,
    noak=NOAK,
    # Chamber geometry (Z-IFE reference spherical chamber)
    R0=R0,
    plasma_t=PLASMA_T,
    blanket_t=BLANKET_T,
    ht_shield_t=HT_SHIELD_T,
    structure_t=STRUCTURE_T,
    vessel_t=VESSEL_T,
    # Power balance
    p_input=P_DRIVER_MW,
    mn=MN,
    eta_th=ETA_TH,
    eta_pin=ETA_PIN,
    f_sub=F_SUB,
    f_dec=0.0,          # No DEC; analysis.md §Key Differentiators vs. Helion
    p_coils=P_COILS,
    p_pump=P_PUMP,
    p_trit=P_TRIT,
    p_house=P_HOUSE,
    p_cryo=P_CRYO,
    p_target=P_TARGET_MW,
    cost_overrides=cost_overrides,
)

# ── Results ──────────────────────────────────────────────────────────────────
c = result.costs
pt = result.power_table

print("MagLIF D-T (Z-IFE LTD reference architecture) — 1000 MWe, 85% availability, 30 yr")
print(f"LCOE: {c.lcoe:.1f} $/MWh | Overnight: {c.overnight_cost:.0f} $/kW")
print(f"Fusion: {pt.p_fus:.0f} MW | Net: {pt.p_net:.0f} MW | Q_eng: {pt.q_eng:.2f}")
print(f"Overridden accounts: {result.overridden}")
print()

cas = [
    ("CAS10", "Preconstruction",           c.cas10),
    ("CAS21", "Buildings",                 c.cas21),
    ("CAS22", "Reactor Plant Equipment",   c.cas22),
    ("CAS23", "Turbine Plant",             c.cas23),
    ("CAS24", "Electrical Plant",          c.cas24),
    ("CAS25", "Miscellaneous",             c.cas25),
    ("CAS26", "Heat Rejection",            c.cas26),
    ("CAS27", "Special Materials",         c.cas27),
    ("CAS28", "Digital Twin",              c.cas28),
    ("CAS29", "Contingency",               c.cas29),
    ("CAS30", "Indirect Costs",            c.cas30),
    ("CAS40", "Owner's Costs",             c.cas40),
    ("CAS50", "Supplementary",             c.cas50),
    ("CAS60", "IDC",                       c.cas60),
    ("CAS70", "O&M (annualized)",          c.cas70),
    ("CAS80", "Fuel (annualized)",         c.cas80),
    ("CAS90", "Financial",                 c.cas90),
]

print(f"{'Code':<8} {'Account':<28} {'M$':>10}")
print("-" * 48)
for code, name, val in cas:
    print(f"{code:<8} {name:<28} {float(val):>10.1f}")
print("-" * 48)
print(f"{'':8} {'Total Capital':<28} {float(c.total_capital):>10.1f}")

# ── CAS22 detail ─────────────────────────────────────────────────────────────
print()
print("CAS22 sub-accounts (Reactor Plant Equipment):")
cas22_labels = {
    "C220000": "CAS22 total",
    "C220101": "First Wall + Blanket (FLiBe)",
    "C220102": "Shield",
    "C220103": "Coils (zeroed — no SC magnets)",
    "C220104": "Driver (pulsed power, LTD ref)",
    "C220105": "Structure",
    "C220106": "Vacuum System",
    "C220107": "Power Supplies",
    "C220108": "Divertor (zeroed — absent in MagLIF)",
    "C220109": "DEC (zeroed)",
    "C220111": "Installation",
    "C220112": "Isotope Separation",
    "C220200": "Coolant Handling",
    "C220300": "Aux Cooling",
    "C220400": "Rad Waste",
    "C220500": "Fuel Handling",
    "C220600": "RTL + Target Factory",
    "C220700": "I&C",
}
for key, label in cas22_labels.items():
    val = result.cas22_detail.get(key)
    if val is not None:
        print(f"  {key:<10} {label:<38} {float(val):>8.1f} M$")

# ── Key Assumptions Summary ───────────────────────────────────────────────────
print()
print("=" * 60)
print("KEY ASSUMPTIONS SUMMARY")
print("=" * 60)
print("""
Architecture:  Z-IFE LTD reference, single chamber, 0.5 Hz,
               frozen-FLiBe RTL (best published MagLIF scenario).
               NOT the modern IMG architecture (Pacific Fusion DS).

Net output:    1000 MWe (Z-IFE reference, 4× larger than Pacific
               Fusion's 250 MWe commercial target; LCOE at 250 MWe
               will be materially higher).

Driver cost:   $372M (LTD median); if IMG achieves 5–10× reduction
               (~$40–75M), LCOE drops significantly (see sensitivity).

Driver C220104 = $372M     [Z-IFE LTD median; ±50%]
Blanket C220101 = $50M     [Z-IFE chamber/FLiBe; ±40%]
RTL factory C220600 = $120M [analogy estimate; ±100%]
Coils C220103  = $0M       [no superconducting magnets]
DEC   C220109  = $0M       [D-T, no direct conversion]

Thermal eff.:  42% (combined Brayton-Rankine, steel chamber,
               near-term achievable; C-C composite could reach 50%)

Driver eff.:   60% (LTD; IMG claims ~90% — unverified at scale)

Rep rate:      0.5 Hz (frozen-FLiBe RTL, single chamber);
               COE at 0.1 Hz (10-chamber steel RTL) = ~20 ¢/kWeh
               per Z-IFE; at 0.5 Hz (this case) = ~7 ¢/kWeh target.

Per-shot consumables: frozen-FLiBe RTL eliminates steel RTL factory
               170 MWe parasitic load. Cryo target cost at scale
               is unknown and NOT captured as an explicit O&M line.
               If cryo targets cost > $2/shot, annual O&M at 1 Hz
               exceeds $50M/yr — potential binding LCOE constraint.

References:    z-ife-sand2006-7148-thermal-cycles.md §3.1.1, §3.1.2
               analysis.md §Section 2 and §Section 5
""")

# ── Sensitivity Analysis ─────────────────────────────────────────────────────
sens = model.sensitivity(result.params, cost_overrides=cost_overrides)

print("Sensitivity (elasticity = %LCOE / %param)")
print("NOTE: Overridden accounts (driver C220104, blanket C220101,")
print("      RTL factory C220600) have zero gradient — sweep manually")
print("      via batch_lcoe or explicit cost_overrides to test their impact.")
print("-" * 55)

print("\nEngineering levers:")
for k, v in sorted(sens["engineering"].items(), key=lambda x: abs(x[1]), reverse=True):
    print(f"  {k:<30} {v:+.4f}")

print("\nFinancial:")
for k, v in sorted(sens["financial"].items(), key=lambda x: abs(x[1]), reverse=True):
    print(f"  {k:<30} {v:+.4f}")

# ── Driver cost sweep (Hypothesis 3: driver cost cliff) ──────────────────────
print()
print("=" * 60)
print("DRIVER COST SWEEP (C220104) — Hypothesis 3")
print("Evaluating LCOE as pulsed power cost per joule falls")
print("from LTD baseline to IMG target")
print("=" * 60)

driver_scenarios = [
    ("LTD ref median",       372.0, "$372M — Z-IFE LTD reference"),
    ("2× reduction",         186.0, "$186M — 2× improvement"),
    ("4× reduction",          93.0, "$93M  — 4× improvement"),
    ("5× reduction (target)", 75.0, "$75M  — 5× (IMG cost target)"),
    ("10× reduction",         37.0, "$37M  — 10× (optimistic IMG)"),
]

print(f"\n  {'Scenario':<28} {'Driver M$':>9}  {'LCOE $/MWh':>10}")
print("  " + "-" * 52)
for label, driver_m, note in driver_scenarios:
    r = model.forward(
        net_electric_mw=NET_ELECTRIC_MW,
        availability=AVAILABILITY,
        lifetime_yr=LIFETIME_YR,
        n_mod=1,
        construction_time_yr=CONSTRUCTION_TIME_YR,
        interest_rate=INTEREST_RATE,
        inflation_rate=INFLATION_RATE,
        noak=NOAK,
        R0=R0,
        plasma_t=PLASMA_T,
        blanket_t=BLANKET_T,
        ht_shield_t=HT_SHIELD_T,
        structure_t=STRUCTURE_T,
        vessel_t=VESSEL_T,
        p_input=P_DRIVER_MW,
        mn=MN,
        eta_th=ETA_TH,
        eta_pin=ETA_PIN,
        f_sub=F_SUB,
        f_dec=0.0,
        p_coils=P_COILS,
        p_pump=P_PUMP,
        p_trit=P_TRIT,
        p_house=P_HOUSE,
        p_cryo=P_CRYO,
        p_target=P_TARGET_MW,
        cost_overrides={**cost_overrides, "C220104": driver_m},
    )
    print(f"  {label:<28} {driver_m:>9.0f}  {float(r.costs.lcoe):>10.1f}  ({note})")

print()
print("Z-IFE reference COE at 0.5 Hz: 7.0 ¢/kWeh = 70 $/MWh")
print("Advanced fission threshold:     4–6 ¢/kWeh = 40–60 $/MWh")
print()
sys.stdout.flush()
