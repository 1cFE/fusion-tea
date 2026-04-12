"""Magnetic Mirror (D-T) — Realta Fusion CoSMo/Hammir LCOE model.

Usage:
    uv run python model_setup.py              # print results to terminal
    uv run python model_setup.py | tee model_output.txt  # also save for synthesis stage

Modeling Approach
-----------------
Commercial-scale axisymmetric tandem magnetic mirror (CoSMo) with D-T fuel,
HTS REBCO solenoid magnets, and hybrid thermal blanket + venetian-blind direct
energy conversion (DEC). Steady-state plasma in a linear open-ended center cell.

Concept Choice Rationale
------------------------
Realta Fusion (UW-Madison spinout, 2022) is the most active private-sector magnetic
mirror program. Their economic thesis is linear center-cell scaling: each additional
meter adds ~7 MWt at roughly constant end-plug hardware cost, potentially enabling
high-Q plants at smaller scale than tokamaks. The 1costingfe MIRROR/DT concept covers
the key physics: cylindrical geometry, solenoid coils, DEC on end-loss ions, and lower
thermal efficiency due to open-ended end losses.

Key Deviations from mfe_mirror.yaml Defaults
---------------------------------------------
- chamber_length: 70 m (commercial scale; 50 m pilot targets Q>5; 70 m → Q~8-10)
  Source: arxiv-2411-06644-confinement-predictions.md §Hammir Design
- p_input: 70 MW (midpoint of 40–100 MW uncertainty range from two prior model runs)
  Source: analysis.md §Section 2, Challenge 3; §Section 5, Missing Parameters
- eta_th: 0.38 (MARS 1983 steam Rankine achieved ~36%; 0.38 reflects modest improvement)
  Source: analysis.md §Section 5 (MARS analogue); blanket/cycle type undisclosed
- eta_de: 0.54 (MARS 1983 gridless DEC; venetian-blind design uncharacterized)
  Source: analysis.md §Section 5, DEC efficiency; MARS Logan 1983
- f_dec: 0.20 (D-T physics: 20% alpha fraction vs 80% neutron — hard physical limit)
  Source: realta-fusion-hub-spotlight.md §Fuel & Reaction; analysis.md §S2 Challenge 4
- p_coils: 10 MW, p_cryo: 2 MW (elevated for larger HTS magnet set at commercial scale)
- No cost overrides: zero Realta-specific cost data available for any CAS account

Data Quality Warning
--------------------
HIGHLY UNCERTAIN: Realta has published no plant-level engineering parameters, capital
cost estimates, or LCOE projections. Nearly every parameter is either analysis-inferred
from historical analogues (MARS 1983) or framework default. LCOE output is an
order-of-magnitude structural estimate only. Data availability rating: Limited.
Source: analysis.md §Section 1
"""

from costingfe import ConfinementConcept, CostModel, Fuel

# ── Model instantiation ───────────────────────────────────────────────────────
model = CostModel(concept=ConfinementConcept.MIRROR, fuel=Fuel.DT)

# ── Plant configuration constants ─────────────────────────────────────────────

# --- Plant scale ---
# Hammir pilot target: >50 MWe net electricity for 3+ hours continuously
# Source: aps-dpp-2025-sutherland.md §Hammir Facility (Pilot Plant)
# Commercial plant: UNCERTAIN — no Realta commercial size target published.
# 500 MWe modeled for economic viability comparison with other fusion concepts.
NET_ELECTRIC_MW = 500.0  # UNCERTAIN: commercial scale; pilot target >50 MWe only

# Availability: no Realta availability target published.
# UNCERTAIN: 0.85 is consistent with framework baseline; DEC electrode lifetime
# is an unresolved concern (thin uncooled electrodes in fusion exhaust stream).
# Source: analysis.md §Section 3, DEC subsystem — no survivability data exists
AVAILABILITY = 0.85  # UNCERTAIN: DEC electrode lifetime unknown; using framework default

LIFETIME_YR = 30         # DEFAULT: standard fusion plant design life
CONSTRUCTION_TIME_YR = 5.0  # DEFAULT: mfe_mirror.yaml (linear geometry simpler
                             # than tokamak; modular center-cell assembly possible)
INTEREST_RATE = 0.07     # DEFAULT: 7% real discount rate
INFLATION_RATE = 0.02    # DEFAULT
NOAK = True              # Nth-of-a-kind (commercial fleet cost floor)

# --- Mirror geometry (cylindrical center cell) ---
R0 = 0.0  # Not used for cylindrical mirror (no toroidal axis offset)

# plasma_t: plasma radius [m]
# arXiv Table 3 gives 0.54 m (Optimum) to 0.78 m (Alternate) for the 50 m pilot.
# Using 0.75 m as a central estimate for a 70 m commercial design; commercial radius
# may be modestly larger if power density is maintained.
# Source: arxiv-2411-06644-confinement-predictions.md Table 3
PLASMA_T = 0.75  # arXiv Table 3: 0.54 m (Optimum) / 0.78 m (Alternate) for 50 m pilot

# chamber_length: commercial center cell length [m]
# Hammir pilot: 50 m → Q_plasma > 5 (modeled, not demonstrated)
# Source: arxiv-2411-06644-confinement-predictions.md §Hammir Design
# "Q > 10 possible with longer center cell" — length unspecified
# Source: fusion-report-interview-realta.md (secondary-source characterization of
#         arXiv scaling behavior; arXiv itself demonstrates Q = 5.8 at 50 m only)
# Using 70 m for a Q~8–10 commercial variant; at ~7 MWt/m → ~490 MWt fusion power
# Source: fusion-report-interview-realta.md §Performance Scaling
CHAMBER_LENGTH = 70.0  # UNCERTAIN: commercial length not published; extrapolated
                        # from 50 m pilot and Q > 10 projection

# Radial build thicknesses [m] — no Realta blanket/shield data available
BLANKET_T = 0.60    # DEFAULT: thinner blanket for linear geometry (neutron path)
                    # MARS used LiPb blanket (TBR 1.15) in similar cylindrical geometry
                    # Source: dossier.md §Key Sources (MARS study, Logan 1983)
HT_SHIELD_T = 0.20  # DEFAULT
STRUCTURE_T = 0.15  # DEFAULT
VESSEL_T = 0.10     # DEFAULT

# ── Forward model ─────────────────────────────────────────────────────────────
result = model.forward(
    # No cost overrides: Realta has published zero plant-level cost data.
    # The only published cost signal: "$50M in REBCO tape for WHAM++" (pre-commercial).
    # Source: realta-fusion-hub-spotlight.md §Magnet Specifications
    # This cannot be extrapolated to a commercial Hammir CAS22 without magnet specs.
    cost_overrides={},

    # --- Customer requirements ---
    net_electric_mw=NET_ELECTRIC_MW,
    availability=AVAILABILITY,
    lifetime_yr=LIFETIME_YR,
    n_mod=1,
    construction_time_yr=CONSTRUCTION_TIME_YR,
    interest_rate=INTEREST_RATE,
    inflation_rate=INFLATION_RATE,
    noak=NOAK,

    # --- Mirror geometry ---
    R0=R0,
    plasma_t=PLASMA_T,
    chamber_length=CHAMBER_LENGTH,  # UNCERTAIN: see above
    blanket_t=BLANKET_T,
    ht_shield_t=HT_SHIELD_T,
    structure_t=STRUCTURE_T,
    vessel_t=VESSEL_T,

    # --- Power balance (tandem mirror with DEC) ---

    # NBI + ECH total heating power [MW]
    # UNCERTAIN: handwritten model used 40 MW; automated pipeline used 100 MW
    # Source: analysis.md §Section 2, Challenge 3 (two prior model run comparison)
    # Source: analysis.md §Section 5, Missing Parameters — "blocking" gap
    # No Hammir input power published by Realta; proprietary.
    #
    # arXiv-anchored estimate: arXiv Table 3 (P_fusion=175 MW, Q=5.8) → P_input ≈ 30 MW
    # for the 50 m pilot. 30–40 MW is the arXiv-derived range (present in full output.md).
    # Source: arxiv-2411-06644-confinement-predictions.md Table 3
    #
    # Conservative case: 70 MW (midpoint of 40–100 MW uncertainty range from prior runs).
    # At 70 MW input and ~490 MWt fusion power: Q_plasma ≈ 7 — physically plausible.
    # An optimistic bracket at p_input = 35 MW (arXiv midpoint extrapolation) would
    # give Q_plasma ≈ 14 at 70 m, providing a lower-LCOE arXiv-anchored scenario.
    p_input=70.0,  # UNCERTAIN: conservative 70 MW; arXiv-anchored estimate is 30–40 MW

    mn=1.1,  # Blanket neutron energy multiplier; DEFAULT: MARS LiPb analogy
             # Source: mfe_mirror.yaml default

    # Thermal conversion efficiency
    # UNCERTAIN: blanket type and thermal cycle undisclosed by Realta
    # MARS 1983 steam Rankine achieved ~36% overall plant efficiency
    # Source: analysis.md §Section 5, Thermal efficiency row (MARS analogue)
    # Modern sCO2 could reach 40–45%; 0.38 is intermediate conservative estimate.
    # Source: analysis.md §Section 2, Challenge 5 (thermal cycle undisclosed)
    eta_th=0.38,  # UNCERTAIN: MARS baseline 36%; sCO2 potential 40–45%

    eta_p=0.50,   # Pumping efficiency; DEFAULT

    # Heating system wall-plug efficiency (NBI + ECH blended)
    # ECH gyrotrons (110 GHz, WHAM): ~45–55% wall-plug efficiency
    # NBI efficiency: ~50%; blended estimate for NBI+ECH mix
    # Source: analysis.md §Section 3, ECH and NBI subsystems
    eta_pin=0.50,  # DEFAULT; consistent with NBI/gyrotron mix estimate

    # DEC efficiency on end-loss ions
    # UNCERTAIN: Realta venetian-blind DEC design is uncharacterized at fusion conditions
    # Source: analysis.md §Section 3, Direct Energy Conversion (TRL 4–5)
    # Only historical analogue: MARS 1983 gridless direct converters ~54%
    # Source: analysis.md §Section 5, DEC efficiency row
    # "analysis.md §S2 Challenge 4: MARS achieved ~54% DEC efficiency"
    # Note: venetian blind ≠ gridless; this is a structural analogue only
    eta_de=0.54,  # UNCERTAIN: MARS analogue; Realta venetian-blind design not characterized

    f_sub=0.03,  # BOP subsystem power fraction; DEFAULT

    # Fraction of end-loss transport power captured by DEC
    # D-T physics hard limit: 80% of fusion energy in 14.1 MeV neutrons (blanket),
    # 20% in 3.5 MeV alpha particles (capturable by DEC at open ends)
    # Source: realta-fusion-hub-spotlight.md §Fuel & Reaction
    # Source: analysis.md §Section 2, Challenge 4 — "20% alpha, 80% neutron"
    # f_dec = 0.20 reflects the alpha physics directly; 80% of alphas to DEC
    # (remainder deposited on wall/divertor structures)
    f_dec=0.20,   # UNCERTAIN: D-T alpha fraction ~20%; fraction actually reaching DEC unknown

    # Solenoid + end-plug coil power [MW]
    # UNCERTAIN: no coil power published for any Realta device.
    # Elevated from default (5 MW) for larger commercial REBCO magnet set:
    # two end-mirror coils (≥ WHAM scale, 17 T HTS) + 70 m of center-cell solenoids.
    # Source: wham-experiment-details.md §Magnet System (REBCO, 17 T in-bore)
    p_coils=10.0,  # UNCERTAIN: inferred from commercial magnet set scale

    p_cool=25.0,   # Cooling system [MW]; elevated from default (20 MW) for 70 m center-cell
    p_pump=2.0,    # Coolant pumping [MW]; DEFAULT
    p_trit=12.0,   # Tritium processing [MW]; elevated for open-ended exhaust management
                   # Li blanket confirmed; type undisclosed
                   # Source: fusion-report-interview-realta.md §Energy Conversion
    p_house=5.0,   # Housekeeping [MW]; elevated for 70 m linear plant
    p_cryo=2.0,    # Cryogenic [MW]; elevated for larger REBCO magnet array at commercial scale
                   # REBCO operates at ~20 K (not 4 K as for LTS) — modest cryo load
                   # Source: wham-experiment-details.md §Magnet System
)

# ── Post-hoc scaling to 1000 MWe (cross-concept comparison) ─────────────
_ALPHA = 0.6
_p_native = float(result.power_table.p_net)
_factor = (_p_native / 1000.0) ** (1.0 - _ALPHA)

scaled_headline = {
    "p_net_mw": 1000.0,
    "lcoe_per_mwh": float(result.costs.lcoe) * _factor,
    "overnight_per_kw": float(result.costs.overnight_cost) * _factor,
}

# ── Results ───────────────────────────────────────────────────────────────────
c = result.costs
pt = result.power_table

print("=" * 60)
print("Magnetic Mirror (D-T) — Realta Fusion / CoSMo Hammir")
print(f"Net electric: {NET_ELECTRIC_MW:.0f} MWe | Availability: {AVAILABILITY:.0%} | Lifetime: {LIFETIME_YR} yr")
print(f"Center cell: {CHAMBER_LENGTH:.0f} m | p_input: 70 MW | NOAK")
print("=" * 60)

lcoe_ckwh = float(c.lcoe) / 10
print(
    f"LCOE: {c.lcoe:.1f} $/MWh ({lcoe_ckwh:.2f} ¢/kWh)"
    f" | Overnight: {c.overnight_cost:.0f} $/kW"
)
print(f"\nScaled headline (1000 MWe, \u03b1={_ALPHA}): LCOE {scaled_headline['lcoe_per_mwh']:.1f} $/MWh | "
      f"Overnight {scaled_headline['overnight_per_kw']:.0f} $/kW")
print(f"Fusion: {pt.p_fus:.0f} MW | Net: {pt.p_net:.0f} MW | Q_eng: {pt.q_eng:.1f}")
print(f"Recirculating fraction: {pt.rec_frac:.1%}")
print()

# ── CAS cost breakdown ────────────────────────────────────────────────────────
cas = [
    ("CAS10", "Preconstruction",         c.cas10),
    ("CAS21", "Buildings",               c.cas21),
    ("CAS22", "Reactor Plant Equipment", c.cas22),
    ("CAS23", "Turbine Plant",           c.cas23),
    ("CAS24", "Electrical Plant",        c.cas24),
    ("CAS25", "Miscellaneous",           c.cas25),
    ("CAS26", "Heat Rejection",          c.cas26),
    ("CAS28", "Digital Twin",            c.cas28),
    ("CAS29", "Contingency",             c.cas29),
    ("CAS30", "Indirect Costs",          c.cas30),
    ("CAS40", "Owner's Costs",           c.cas40),
    ("CAS50", "Supplementary",           c.cas50),
    ("CAS60", "IDC",                     c.cas60),
    ("CAS70", "O&M (annualized)",        c.cas70),
    ("CAS80", "Fuel (annualized)",       c.cas80),
    ("CAS90", "Financial",               c.cas90),
]

print(f"{'Code':<8} {'Account':<28} {'M$':>10}")
print("-" * 48)
for code, name, val in cas:
    print(f"{code:<8} {name:<28} {float(val):>10.1f}")
print("-" * 48)
print(f"{'':8} {'Total Capital':<28} {float(c.total_capital):>10.1f}")

# ── CAS22 sub-account detail ──────────────────────────────────────────────────
print("\nCAS22 Reactor Plant Equipment Breakdown:")
print("-" * 48)
for k, v in sorted(result.cas22_detail.items()):
    if float(v) > 0:
        print(f"  {k:<28} {float(v):>10.1f} M$")

# ── Key assumptions summary ───────────────────────────────────────────────────
print()
print("=" * 60)
print("KEY ASSUMPTIONS AND UNCERTAINTIES")
print("=" * 60)
print("""
HIGHLY UNCERTAIN MODEL — no plant-level cost data published by Realta.
Data quality: Limited (analysis.md §Section 1).

Physics basis:
  Q_plasma > 5 at 50 m center cell (modeled, not experimentally validated)
    Source: arxiv-2411-06644-confinement-predictions.md §Hammir Design
  ~7 MWt/m center-cell thermal power scaling law
    Source: fusion-report-interview-realta.md §Performance Scaling
  70 m commercial center cell assumed → ~490 MWt, Q_plasma ~ 7 at 70 MW input
  Hammir pilot electrical target: Qe > 1, Pe > 50 MWe for 3+ hours
    Source: aps-dpp-2025-sutherland.md §Hammir Facility

Key uncertainties ranked by LCOE impact:
  1. BLOCKING — end-plug confinement physics: Anvil demonstrator (~2028) required
     to validate stable high-Q end-plug at commercial conditions
  2. BLOCKING — commercial plant size: only 50 MWe pilot target published
  3. BLOCKING — p_input = 70 MW (UNCERTAIN: range 40–100 MW; truly unknown)
     analysis.md §Section 2, Challenge 3
  4. CRITICAL — thermal efficiency (eta_th=0.38): cycle type undisclosed
     MARS 1983 baseline ~36%; sCO2 potential 40–45%
  5. CRITICAL — recirculating power fraction: couples p_input uncertainty to Qe
  6. HIGH — DEC efficiency (eta_de=0.54): MARS 1983 gridless analogue only
     Venetian-blind design uncharacterized; TRL 4–5 for DEC class
  7. HIGH — f_dec = 0.20: D-T alpha fraction is physics-determined (20%),
     but fraction actually captured at electrodes is unknown

Not captured by this model (framework limitation):
  - REBCO supply chain premium: $50M tape cost for WHAM++ alone
    (realta-fusion-hub-spotlight.md §Magnet Specifications)
  - End-plug confinement failure risk (→ higher p_input, lower Qe)
  - DEC electrode replacement cost / availability penalty
  - Hot-cell remote handling complexity for linear 70 m machine
""")

# ── Sensitivity analysis ──────────────────────────────────────────────────────
sens = model.sensitivity(result.params)

print("SENSITIVITY ANALYSIS (elasticity = %LCOE / %param)")
print("=" * 60)

print("\nEngineering levers:")
for k, v in sorted(sens["engineering"].items(), key=lambda x: abs(x[1]), reverse=True):
    print(f"  {k:<28} {v:+.4f}")

print("\nFinancial:")
for k, v in sorted(sens["financial"].items(), key=lambda x: abs(x[1]), reverse=True):
    print(f"  {k:<28} {v:+.4f}")
