"""1costingfe model setup — MagLIF (D-T), Pacific Fusion / Fuse Energy Technologies.

Modeling Approach
-----------------
MagLIF is a Magnetized Liner Inertial Fusion (MIF) concept operated as a pulsed
power plant. The dominant cost structure differs fundamentally from MFE tokamaks:

  1. Pulsed power driver (≈96% of direct driver CapEx) replaces superconducting magnets
  2. No divertor — thick liquid FLiBe wall absorbs neutron and X-ray flux
  3. Rep rate × yield/shot (not capacity factor) is the primary LCOE lever
  4. Per-shot consumables (liner + RTL) create a novel variable O&M cost category

Framework Fit and Limitations
------------------------------
1costingfe's MAG_TARGET concept provides the closest structural match, but three
dominant MagLIF cost categories have no framework analogues:
  - Pulsed power driver capital (mapped to C220104 "heating" override)
  - RTL/target consumable O&M (absorbed into framework O&M defaults — UNCERTAIN)
  - Rep-rate-driven power balance (approximated via p_driver = rep_rate × E_driver)

The analysis (analysis.md §Section 2) explicitly states that "reference-class scaling
approaches (1costingfe, ARIES-analogous tools, PROCESS) are not applicable to MagLIF
because the dominant cost categories have no analogues in the databases those tools are
built on." This script is therefore a constrained best-effort estimate, not a validated
system code result. Uncertainty bands on all outputs should be treated as ±50%+.

Primary Reference
-----------------
All quantitative parameters derive from the Z-IFE SAND2006-7148 study (Olson et al.,
2006) — the only published systems-level cost model for a MagLIF-class power plant.
This study used LTD (linear transformer driver) architecture, not the modern IMG
architecture pursued by Pacific Fusion / Fuse Energy. No IMG plant-scale cost study
has been published. Z-IFE results carry ±50%+ uncertainty when applied to IMG.

Scenario
--------
Primary: 0.5 Hz single-chamber stretch case (7.0 ¢/kWeh in Z-IFE), 1000 MWe.
  - Frozen-FLiBe RTL baseline (eliminates 170 MWe steel RTL remanufacturing load)
  - Combined Brayton-Rankine thermal cycle (steel chamber), η_th = 42%
  - IMG wall-plug efficiency 90% (vs. LTD 60%)
  - Z-IFE gain formula: G = 30.15 × (E − 1.22)^2.038 → ~4,600 MJ at 42 MJ driver
  - Average driver power: 42 MJ × 0.5 Hz = 21 MW

Usage:
    uv run python model_setup.py              # print results to terminal
    uv run python model_setup.py | tee model_output.txt  # also save for synthesis stage
"""

# ── Imports ─────────────────────────────────────────────────────────────────
from costingfe import ConfinementConcept, CostModel, Fuel

# ── Model Instantiation ──────────────────────────────────────────────────────
model = CostModel(concept=ConfinementConcept.MAG_TARGET, fuel=Fuel.DT)

# ============================================================================
# Plant Configuration Constants
# All values from analysis.md Section 5 (LCOE-Relevant Parameters) unless noted.
# Source tag key: [§5] = analysis.md §Section 5; [§2] = analysis.md §Section 2
# ============================================================================

# ── Top-level plant requirements ─────────────────────────────────────────────
NET_ELECTRIC_MW = 1000.0     # Z-IFE reference single-chamber configuration
                             # Source: z-ife-sand2006-7148-thermal-cycles.md §3.1.1 [§5]

AVAILABILITY = 0.85          # Z-IFE 85% assumption; presupposes thick liquid wall
                             # success (no scheduled solid first-wall replacement)
                             # UNCERTAIN: no rep-rated system has demonstrated this
                             # Source: z-ife-sand2006-7148-thermal-cycles.md §3.1.1.5 [§5]
                             # Failure scenario: 60–75% if chamber replacement required [§5]

LIFETIME_YR = 30             # DEFAULT: standard fusion plant lifetime
                             # No MagLIF-specific lifetime study exists

N_MOD = 1                   # Single-chamber, 0.5 Hz stretch scenario
                             # Z-IFE also studied 10-chamber 0.1 Hz (COE ~20 ¢/kWeh)
                             # Source: z-ife-sand2006-7148-thermal-cycles.md §3.1.1.6 [§5]

CONSTRUCTION_TIME_YR = 5.0   # UNCERTAIN: DEFAULT for MIF class; no MagLIF plant built
                             # Simpler than tokamak (no SC magnet assembly) but
                             # novel pulsed power facility; plausible range 4–7 yr

# ── Financial parameters ──────────────────────────────────────────────────────
INTEREST_RATE = 0.0966       # 9.66% fixed charge rate — Z-IFE study assumption
                             # Source: z-ife-sand2006-7148-thermal-cycles.md §3.1.1 [§5]
                             # "consistent with fusion plant finance assumptions"

INFLATION_RATE = 0.0245      # DEFAULT: framework standard GDP deflator

NOAK = False                 # FOAK — technology is pre-commercial; neither Pacific
                             # Fusion nor Fuse Energy has built a power plant

# ── Physics / power balance ───────────────────────────────────────────────────
ETA_TH = 0.42                # Combined Brayton-Rankine thermal efficiency (steel chamber)
                             # Source: z-ife-sand2006-7148-thermal-cycles.md §3.2 [§5]
                             # Upper bound 50% with C-C composite at >900 K (not
                             # commercially available); 42% is achievable near-term

ETA_PIN = 0.90               # IMG wall-plug efficiency (pulsed power → stored energy)
                             # Source: arxiv-2408-15206-pulsed-magnetic-fusion.md §3.2 [§5]
                             # "90% energy efficiency" vs. NIF ~15%, LTD ~60%
                             # UNCERTAIN: claimed at prototype scale; not validated at GW

P_DRIVER_MW = 21.0           # Average pulsed power driver charging load [MW]
                             # = 42 MJ stored energy × 0.5 Hz rep rate
                             # 42 MJ driver energy from gain formula:
                             #   G = 30.15 × (E − 1.22)^2.038; G×42MJ → ~4,600 MJ yield
                             # Source: z-ife-sand2006-7148-thermal-cycles.md §3.1.1.5 [§5]
                             # Note: enters thermal balance AND recirculating power
                             # (p_th includes p_driver; recirc = p_driver / eta_pin)

MN = 1.1                     # DEFAULT: neutron energy multiplier; framework default
                             # FLiBe blanket has Li multiplication but no explicit
                             # Z-IFE value given — using MIF class default

ETA_P = 0.5                  # DEFAULT: pumping efficiency

F_SUB = 0.03                 # DEFAULT: subsystem power fraction

# ── Auxiliary power loads ─────────────────────────────────────────────────────
P_PUMP = 1.0                 # DEFAULT: FLiBe primary coolant pumping power [MW]
                             # Z-IFE uses FLiBe primary loop; pump power not specified

P_TRIT = 10.0                # DEFAULT: tritium processing [MW] — standard D-T load
                             # FLiBe circuit vacuum degassing for T extraction;
                             # may be simpler than solid breeder pebble extraction
                             # Source: z-ife-sand2006-7148-thermal-cycles.md §3.3 [§5]

P_HOUSE = 4.0                # DEFAULT: housekeeping / lighting / HVAC [MW]

P_CRYO = 0.0                 # No cryogenic systems — NO superconducting magnets required
                             # Key differentiator: MagLIF uses no REBCO tape or Nb₃Sn
                             # Source: analysis.md §Key Differentiators
                             # Frozen-FLiBe RTL requires some cryo cooling but
                             # no published estimate; setting to 0 (conservative)

P_TARGET = 2.0               # DEFAULT: target/liner factory power [MW]
                             # Self-magnetizing composite targets (plastic + Al)
                             # ambient temperature — no cryo target power needed
                             # (Pacific Fusion breakthrough Oct 2025, 4 shots at 22 MA)
                             # Source: analysis.md §Section 3 (Target Fabrication)

P_COILS = 0.0                # No external Helmholtz coils — self-magnetizing targets
                             # eliminate per-shot copper coils
                             # Source: analysis.md §Key Differentiators
                             # Pacific Fusion self-magnetizing target breakthrough
                             # (October 2025) demonstrated field penetration without coils

# ── Chamber geometry (Z-IFE reference spherical chamber) ──────────────────────
PLASMA_T = 4.0               # Spherical chamber radius [m]
                             # Source: z-ife-power-plant-concept.md §Abstract [§5]
                             # "4 m radius" cylindrical/spherical chamber geometry

BLANKET_T = 0.80             # FLiBe blanket thickness [m]
                             # Source: z-ife-power-plant-concept.md §Abstract [§5]
                             # "80 cm FLiBe sphere" blanket; freeze point 733 K,
                             # max operating temp ≤850 K

HT_SHIELD_T = 0.20           # DEFAULT: high-temperature shield thickness [m]
STRUCTURE_T = 0.15           # DEFAULT: primary structure thickness [m]
VESSEL_T = 0.10              # DEFAULT: vacuum vessel thickness [m]

# ── Cost overrides — deviations from MFE/tokamak framework defaults ───────────
#
# Three accounts require explicit override to represent MagLIF cost structure.
# All others left at framework defaults (labeled DEFAULT below).
#
# C220103: Magnet coils
#   MFE default ~516 M$ (REBCO tape TF/CS/PF system). MagLIF has NO superconducting
#   magnets — pulsed fields from driver coils; self-magnetizing target eliminates
#   external Helmholtz coils. Override to ~5 M$ for residual guide field copper coils.
#   Source: analysis.md §Key Differentiators ("No superconducting magnets")
#
# C220104: Heating / driver systems
#   MFE default ~353 M$ (NBI + ECRH + LHCD systems). For MagLIF, the pulsed power
#   driver IS the heating system — no separate plasma heating. Override to Z-IFE
#   LTD driver median bottom-up estimate.
#   UNCERTAIN: LTD architecture only; IMG architecture uncosted at plant scale.
#   "Factor of 5–10 cost reduction" required from ~$5/J to <$0.50/J commercial target.
#   Source: z-ife-sand2006-7148-thermal-cycles.md §3.1.2 [§5][6]
#
# C220108: Divertor
#   MFE default ~269 M$ (steady-state plasma scrape-off layer management). MagLIF
#   has NO divertor — thick liquid FLiBe wall absorbs all particle and heat loads.
#   Source: analysis.md §Key Differentiators ("Thick liquid wall, not solid first wall")
#
# Note: CAS22 target factory sub-account uses framework default target_factory_base
# = 244 M$. This covers the RTL fabrication and liner production facility capital.
# No better Z-IFE estimate for factory capital alone was found in Section 5.

COST_OVERRIDES = {
    "C220103": 5.0,     # No superconducting magnets; residual guide-field Cu coils only
                        # analysis.md §Key Differentiators; MFE default: ~516 M$

    "C220104": 372.0,   # Z-IFE LTD driver (pulsed power ≡ heating system)
                        # UNCERTAIN: LTD architecture; IMG may differ 5–10× in either dir.
                        # Source: z-ife-sand2006-7148-thermal-cycles.md §3.1.2 [§5][6]
                        # Scaling law: C = 372 × (TW/1000)^0.6 M$ (LTD-based)
                        # 95th percentile: $862M; P5: not stated

    "C220108": 0.0,     # No divertor; thick liquid FLiBe wall
                        # analysis.md §Key Differentiators; MFE default: ~269 M$
}

# ============================================================================
# Forward Pass
# ============================================================================
result = model.forward(
    # Plant requirements
    net_electric_mw=NET_ELECTRIC_MW,
    availability=AVAILABILITY,
    lifetime_yr=LIFETIME_YR,
    n_mod=N_MOD,
    construction_time_yr=CONSTRUCTION_TIME_YR,
    # Financial
    interest_rate=INTEREST_RATE,
    inflation_rate=INFLATION_RATE,
    noak=NOAK,
    # Physics / power balance
    eta_th=ETA_TH,
    eta_pin=ETA_PIN,
    p_driver=P_DRIVER_MW,
    mn=MN,
    eta_p=ETA_P,
    f_sub=F_SUB,
    # Auxiliary loads
    p_pump=P_PUMP,
    p_trit=P_TRIT,
    p_house=P_HOUSE,
    p_cryo=P_CRYO,
    p_target=P_TARGET,
    p_coils=P_COILS,
    # Chamber geometry (Z-IFE spherical chamber)
    plasma_t=PLASMA_T,
    blanket_t=BLANKET_T,
    ht_shield_t=HT_SHIELD_T,
    structure_t=STRUCTURE_T,
    vessel_t=VESSEL_T,
    # Cost overrides (MagLIF-specific deviations from MFE defaults)
    cost_overrides=COST_OVERRIDES,
)

# ============================================================================
# Results
# ============================================================================
c = result.costs
pt = result.power_table

print("=" * 68)
print("MagLIF (D-T) — Pacific Fusion / Fuse Energy Technologies")
print("Z-IFE reference: 1 GWe, 0.5 Hz single-chamber, frozen-FLiBe RTL")
print("WARNING: Framework approximation — dominant cost categories not in")
print("         framework databases. Treat outputs as ±50%+ uncertain.")
print("=" * 68)
print(f"LCOE:            {c.lcoe:.1f} $/MWh")
print(f"Overnight cost:  {c.overnight_cost:.0f} $/kW")
print(f"Fusion power:    {pt.p_fus:.0f} MW")
print(f"Net electric:    {pt.p_net:.0f} MW")
print(f"Q_sci:           {pt.q_sci:.1f}  (p_fus / p_driver)")
print(f"Q_eng:           {pt.q_eng:.2f} (p_net / recirculating)")
print()

# ── CAS breakdown ─────────────────────────────────────────────────────────────
cas = [
    ("CAS10", "Preconstruction",            c.cas10),
    ("CAS21", "Buildings",                  c.cas21),
    ("CAS22", "Reactor Plant Equipment",    c.cas22),
    ("CAS23", "Turbine Plant",              c.cas23),
    ("CAS24", "Electrical Plant",           c.cas24),
    ("CAS25", "Miscellaneous",              c.cas25),
    ("CAS26", "Heat Rejection",             c.cas26),
    ("CAS27", "Special Materials",          c.cas27),
    ("CAS28", "Digital Twin",               c.cas28),
    ("CAS29", "Contingency",                c.cas29),
    ("CAS30", "Indirect Costs",             c.cas30),
    ("CAS40", "Owner's Costs",              c.cas40),
    ("CAS50", "Supplementary",              c.cas50),
    ("CAS60", "IDC",                        c.cas60),
    ("CAS70", "O&M (annualized)",           c.cas70),
    ("CAS80", "Fuel (annualized)",          c.cas80),
    ("CAS90", "Financial",                  c.cas90),
]

print(f"{'Code':<8} {'Account':<28} {'M$':>10}")
print("-" * 50)
for code, name, val in cas:
    print(f"{code:<8} {name:<28} {float(val):>10.1f}")
print("-" * 50)
print(f"{'':8} {'Total Capital':<28} {float(c.total_capital):>10.1f}")
print()

# ── CAS22 sub-account detail ──────────────────────────────────────────────────
print("CAS22 Sub-account Detail (Reactor Plant Equipment):")
print("-" * 50)
cas22_labels = {
    "C220101": "Blanket/First Wall (FLiBe)",
    "C220102": "Shield",
    "C220103": "Coils [OVERRIDE: ~0, no SC magnets]",
    "C220104": "Driver [OVERRIDE: Z-IFE LTD $372M]",
    "C220105": "Structure",
    "C220106": "Vacuum System",
    "C220107": "Power Supplies",
    "C220108": "Divertor [OVERRIDE: $0, no divertor]",
    "C220109": "Direct Energy Conversion",
    "C220110": "Remote Handling",
    "C220111": "Installation",
    "C220112": "Isotope Separation",
    "C220200": "Coolant Handling (FLiBe)",
    "C220300": "Aux Cooling",
    "C220400": "Radwaste",
    "C220500": "Fuel Handling (tritium)",
    "C220600": "Other Equip (target factory)",
    "C220700": "I&C",
    "C220000": "TOTAL CAS22",
}
for key, label in cas22_labels.items():
    if key in result.cas22_detail:
        val = float(result.cas22_detail[key])
        override_marker = " *" if key in COST_OVERRIDES else ""
        print(f"  {key}  {label:<38} {val:>8.1f} M${override_marker}")
print()

# ============================================================================
# Key Assumptions Summary
# ============================================================================
print("=" * 68)
print("Key Assumptions")
print("=" * 68)
print(f"  Rep rate (modeled):    0.5 Hz  (Z-IFE optimized; 0.1 Hz baseline = 10-chamber)")
print(f"  Driver energy/shot:    42 MJ   (gain formula G = 30.15*(E-1.22)^2.038)")
print(f"  Yield/shot:            ~4,600 MJ  (2D HYDRA simulation, unvalidated)")
print(f"  Driver capital:        $372M   (Z-IFE LTD; IMG uncosted; UNCERTAIN ±5x)")
print(f"  Driver efficiency:     90%     (IMG claim; LTD was 60%)")
print(f"  Thermal efficiency:    42%     (Combined Brayton-Rankine, steel chamber)")
print(f"  Capacity factor:       85%     (Z-IFE assumption; liquid wall undemonstrated)")
print(f"  No SC magnets:         C220103 overridden to $5M (self-magnetizing targets)")
print(f"  No divertor:           C220108 overridden to $0 (thick liquid FLiBe wall)")
print()
print("Critical unmodeled risks (see analysis.md §Section 2):")
print("  1. RTL consumable O&M: $0.70/shot historical steel → ~$20M/yr at 0.5 Hz")
print("     Cryo-ice-layer target cost is UNKNOWN; commercial viability req <$2/shot")
print("  2. Rep rate not demonstrated: 0.5 Hz requires 10-second cycle unvalidated")
print("     If limited to 0.1 Hz, Z-IFE shows COE ~20 ¢/kWeh (3-4x competitive threshold)")
print("  3. Driver cost cliff: commercial pulsed power ~$5/J; target <$0.50/J (10x gap)")
print("  4. Gain scaling unvalidated: chi ~ 0.1 on Z; GJ yields require 60+ MA untested")
print("  5. Chamber lifetime under repetitive GJ shock: no experimental facility exists")
print()

# ============================================================================
# Sensitivity Analysis
# ============================================================================
print("=" * 68)
print("Sensitivity Analysis (elasticity = %LCOE / %param)")
print("Overridden accounts have zero gradient by construction.")
print("=" * 68)
sens = model.sensitivity(result.params, cost_overrides=COST_OVERRIDES)

print("\nEngineering levers:")
for k, v in sorted(sens["engineering"].items(), key=lambda x: abs(x[1]), reverse=True):
    print(f"  {k:<28} {v:+.4f}")

print("\nFinancial:")
for k, v in sorted(sens["financial"].items(), key=lambda x: abs(x[1]), reverse=True):
    print(f"  {k:<28} {v:+.4f}")

print()
print("Interpretation notes:")
print("  eta_th: 42% → 50% (C-C composite) would reduce LCOE by ~elasticity factor")
print("  availability: 0.85 baseline; 0.65 failure case multiplies LCOE by ~1.3x")
print("  Note: rep_rate and p_driver are coupled — p_driver = rep_rate * E_driver")
print("        LCOE sensitivity to rep rate is approximately -1.0 (10x rep rate → 10x LCOE)")
print("        This elasticity is NOT captured in the framework sensitivity above")
