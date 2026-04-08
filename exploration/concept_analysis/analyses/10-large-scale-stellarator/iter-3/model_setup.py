"""Large-Scale Stellarator (Gauss Fusion GIGA) — LCOE estimate.

Modeling approach:
    FOAK-anchored free-form model. The only public cost reference for GIGA is a
    single FOAK figure (€15–18B); no CAS account breakdown or NOAK projection is
    published. The model therefore tests the FOAK-to-NOAK learning hypothesis,
    parameterized as noak_fraction (NOAK overnight cost as a fraction of FOAK),
    rather than validating a bottom-up cost build. The noak_fraction sweep is the
    primary modeling contribution. The central LCOE (~$186/MWh at 55% NOAK
    fraction) reflects this learning hypothesis applied to the FOAK midpoint.

Concept rationale:
    GIGA is a quasi-isodynamic (QI) non-planar-coil stellarator at 18 m major
    radius, derived from the HELIAS HSR4/18 reactor study (IPP Garching heritage).
    Key TEA differentiators vs. a conventional tokamak: inherent steady-state
    operation (~88% capacity factor), no current drive (ECRH only for startup/
    profile control), no disruption risk. Key penalties: 3× larger machine radius
    than ITER, 80+ unique blanket segment shapes (3D geometry), complex non-planar
    coil manufacturing at scale with no precedent above W7-X (5.5 m).

Key deviations from stellarator defaults (mfe_stellarator.yaml):
    - R0 = 18.0 m (vs. default 5.5 m — GIGA design point from HSR4/18 heritage)
    - plasma_t = 1.7 m (vs. default 1.8 m — stated GIGA minor radius)
    - plasma_volume = 1500.0 m³ (vs. default 800 m³ — stated GIGA plasma volume)
    - B = 6.0 T (vs. default 5.0 T — stated on-axis field; peak coil 12–13 T)
    - p_cryo = 90.0 MW (vs. default 0.8 MW — WISTELL-D analog scaling;
      UNCERTAIN: represents ~3% of fusion power as lower bound for GIGA scale)
    - p_input = 75.0 MW (vs. default 30.0 MW — ECRH for profile control only;
      no current drive required; UNCERTAIN: range 50–100 MW)
    - eta_th = 0.35 (vs. default 0.46 — HCPB/steam Rankine; UNCERTAIN pending
      blanket type disclosure; DCLL option would yield ~0.40)
    - construction_time_yr = 10.0 (vs. default 8.0 — 18 m scale penalty)
    - CAS22 overridden from FOAK reference × noak_fraction (see below)
    - CAS27 overridden to 200.0 M$ for HCPB beryllium neutron multiplier

Addressing assessment feedback F-2 (blanket geometry complexity):
    The 3D blanket segment diversity (80+ unique shapes vs. ~2 for a tokamak)
    is GIGA's most distinctive cost-penalty differentiator. A
    blanket_complexity_multiplier parameter is introduced and swept over 1.0–2.5×,
    applied to the blanket/VV sub-component of CAS22. This makes the fabrication
    cost risk visible in the output rather than hidden in the aggregate noak_fraction.

Usage:
    uv run python model_setup.py              # print results to terminal
    uv run python model_setup.py | tee model_output.txt  # also save for synthesis stage
"""

from costingfe import ConfinementConcept, CostModel, Fuel

# ── FOAK-to-NOAK cost anchor ────────────────────────────────────────────────
#
# GIGA FOAK: €15–18B (midpoint €16.5B, analysis.md §Section 2 Challenge 1)
# Source: gauss-fusion-technical-summary.md §Funding
# "The GIGA fusion plant has an estimated cost of €15–18 billion for its
#  first-of-a-kind commercial reactor."
#
# Currency conversion: 1.10 USD/EUR (approximate; UNCERTAIN)
FOAK_COST_EUR_B = 16.5        # €B midpoint of stated €15–18B range
EUR_TO_USD = 1.10             # UNCERTAIN: exchange rate assumption
FOAK_OVERNIGHT_USD_M = FOAK_COST_EUR_B * EUR_TO_USD * 1e3  # M$ (= $18,150 M)

# NOAK fraction (H1 — the primary modeling lever)
# Analysis §Key Hypotheses H1: "If NOAK capital cost reaches 50–60% of FOAK,
# LCOE falls below ~$100/MWh." Range 0.40–0.70; central 0.55.
# Source: analysis.md §Modeling Framework, §Key Hypotheses H1
NOAK_FRACTION_CENTRAL = 0.55

# CAS22 allocation fraction: 65% of overnight cost is a common fusion reference
# (no CAS-level breakdown published for GIGA). Assumption only.
CAS22_FRAC_OF_OVERNIGHT = 0.65  # UNCERTAIN: assumed allocation

# CAS22 sub-allocation (assumption — no sub-account data exists for GIGA):
#   40% coil system (C220103) — dominant cost for 40 × 300-tonne non-planar coils
#   40% blanket/VV (C220101 + C220106) — 3D HELIAS geometry, 640 unique segments
#   20% other (heating, structure, power supplies, remote handling, I&C, etc.)
CAS22_COIL_FRAC = 0.40         # UNCERTAIN
CAS22_BLANKET_FRAC = 0.40      # UNCERTAIN — the focus of blanket complexity analysis
CAS22_OTHER_FRAC = 0.20        # UNCERTAIN

# Blanket complexity multiplier (F-2 assessment finding)
# The 3D blanket segment diversity (80+ unique shapes vs. ~2 for tokamak) is rated
# "High" TEA impact with no analogue in tokamak cost literature.
# Source: analysis.md §Section 2 Challenge 3; §Section 5 Missing Parameters
# Range: 1.0 (no premium, tokamak-equivalent fabrication) to 2.5 (extreme penalty)
# Central: 1.5 (moderate premium for 40× segment diversity vs. tokamak)
BLANKET_COMPLEXITY_MULTIPLIER_CENTRAL = 1.5  # UNCERTAIN: truly-unknown gap


def compute_cas22_override(noak_fraction: float, blanket_complexity_multiplier: float) -> float:
    """Compute CAS22 override (M$) from FOAK reference + learning + complexity.

    Splits NOAK CAS22 into coil / blanket / other sub-components, then applies
    blanket_complexity_multiplier to the blanket/VV sub-component before summing.
    This makes GIGA's most distinctive cost-penalty differentiator explicit.
    """
    noak_overnight = FOAK_OVERNIGHT_USD_M * noak_fraction
    base_cas22 = noak_overnight * CAS22_FRAC_OF_OVERNIGHT

    coil_m = base_cas22 * CAS22_COIL_FRAC
    blanket_m = base_cas22 * CAS22_BLANKET_FRAC
    other_m = base_cas22 * CAS22_OTHER_FRAC

    adjusted_blanket_m = blanket_m * blanket_complexity_multiplier
    return coil_m + adjusted_blanket_m + other_m


# ── Plant configuration constants ───────────────────────────────────────────

NET_ELECTRIC_MW = 1000.0        # Net electrical output [MWe]
                                # Source: gauss-fusion-technical-summary.md §GIGA Power Plant
                                # "1 GWe design target"

AVAILABILITY = 0.88             # Capacity factor [fraction]
                                # Analog: Helios/Thea Energy QA stellarator (88%)
                                # based on biennial 84-day outage.
                                # Source: arxiv-2512-08027v1.md §2 Summary of the design
                                # UNCERTAIN for GIGA: GIGA's 3D blanket may push lower.
                                # Model range 0.85–0.90.

LIFETIME_YR = 40.0              # Plant lifetime [yr]
                                # Source: gauss-fusion-technical-summary.md §GIGA Power Plant
                                # "Magnet and vacuum vessel design life: 40 years"

CONSTRUCTION_TIME_YR = 10.0     # Construction time [yr]
                                # UNCERTAIN: no GIGA estimate published.
                                # Basis: 18 m machine is 3× ITER scale; ITER construction
                                # has taken ~20 yr; serial-production GIGA assumed faster
                                # but still more complex than compact concepts (default 8 yr).
                                # Analysis §Section 2 Challenge 4 (scale extrapolation).

INTEREST_RATE = 0.07            # Discount / interest rate [fraction]
INFLATION_RATE = 0.0245         # Inflation rate [fraction]

# ── Model creation ──────────────────────────────────────────────────────────

model = CostModel(concept=ConfinementConcept.STELLARATOR, fuel=Fuel.DT)

# ── Compute central CAS22 override ──────────────────────────────────────────

cas22_central = compute_cas22_override(
    NOAK_FRACTION_CENTRAL, BLANKET_COMPLEXITY_MULTIPLIER_CENTRAL
)

# ── model.forward() ─────────────────────────────────────────────────────────

result = model.forward(
    net_electric_mw=NET_ELECTRIC_MW,
    availability=AVAILABILITY,
    lifetime_yr=LIFETIME_YR,
    n_mod=1,
    construction_time_yr=CONSTRUCTION_TIME_YR,
    interest_rate=INTEREST_RATE,
    inflation_rate=INFLATION_RATE,
    noak=True,  # NOAK scenario; noak_fraction baked into CAS22 override above

    # ── Geometry (GIGA stated parameters) ──────────────────────────────────
    R0=18.0,                # Major radius [m]
                            # Source: gauss-fusion-technical-summary.md §GIGA Power Plant
                            # "HSR4/18 heritage (4 field periods, R = 18 m)"
    plasma_t=1.7,           # Minor radius [m]
                            # Source: gauss-fusion-technical-summary.md §GIGA Power Plant
    elon=1.0,               # Elongation (near-circular stellarator cross-section)
                            # DEFAULT: standard stellarator approximation
    blanket_t=0.60,         # Blanket thickness [m]; DEFAULT: mfe_stellarator.yaml
    ht_shield_t=0.20,       # HT shield thickness [m]; DEFAULT
    structure_t=0.15,       # Structure thickness [m]; DEFAULT
    vessel_t=0.10,          # Vacuum vessel thickness [m]; DEFAULT

    # ── Plasma parameters ──────────────────────────────────────────────────
    plasma_volume=1500.0,   # Plasma volume [m³]
                            # Source: gauss-fusion-technical-summary.md §GIGA Power Plant
    B=6.0,                  # On-axis magnetic field [T]
                            # Source: dossier.md §Driver Technology
                            # Peak coil field: 12–13 T (requires Nb3Sn or REBCO)
    n_e=1.0e20,             # Electron density [m⁻³]; DEFAULT
    T_e=12.0,               # Electron temperature [keV]; DEFAULT
    Z_eff=1.3,              # Effective charge; DEFAULT stellarator (W7-X heritage)
    R_w=0.6,                # Wall reflectivity for synchrotron; DEFAULT (metallic W)
    wall_material="W",      # Tungsten first wall
                            # Source: helias-blanket-studies.md §3.2 "2 mm W armor"
    T_edge=0.05,            # Edge ion temperature [keV] (50 eV island divertor)
    tau_ratio=3.0,          # Impurity confinement / energy confinement time; DEFAULT

    # ── Power balance ──────────────────────────────────────────────────────
    p_input=75.0,           # ECRH heating power [MW]
                            # UNCERTAIN: analysis.md §Section 5 Missing Parameters
                            # "ECRH startup/profile power: ~50–100 MW range, unstated"
                            # No current drive needed — rotational transform is geometric.
                            # Source: analysis.md §Section 2 Challenge 6 (ECRH section)
    mn=1.1,                 # Neutron energy multiplier; DEFAULT for DT blanket
    eta_th=0.35,            # Gross thermal conversion efficiency [fraction]
                            # UNCERTAIN: analysis.md §Section 2 Challenge 2
                            # HCPB/steam Rankine ~35%; DCLL/advanced Brayton ~40%+
                            # Source: helias-reactor-context.md §7 "~35% standard"
                            # Net 33.3% (1 GWe / 3 GWth) consistent with 35% gross
                            # minus ~5–7% recirculating power total.
    eta_p=0.50,             # Pumping efficiency; DEFAULT
    eta_pin=0.50,           # ECRH wall-plug efficiency [fraction]
                            # Source: analysis.md §Section 3 ECRH Heating Systems
                            # "current wall-plug efficiency ~50–55%"
    eta_de=0.0,             # Direct energy conversion efficiency; not applicable
                            # (stellarators do not use DEC)
    f_sub=0.03,             # Subsystem power fraction; DEFAULT
    f_dec=0.0,              # DEC fraction; not applicable
    p_coils=3.0,            # Coil system auxiliary power [MW]; DEFAULT stellarator
                            # Joint ohmic loss: ~1 nΩ × (100 kA)² × 10,000 joints
                            # = 100 W total — negligible; dominant term is coil
                            # control/protection electronics.
                            # Source: gauss-fusion-technical-summary.md §Magnet System
    p_cool=15.0,            # Coolant pumping power [MW]
                            # Source: helias-blanket-studies.md §Table 5
                            # He coolant at 8.0 MPa / 445–485°C; DEFAULT
    p_pump=1.0,             # Other pumping power [MW]; DEFAULT
    p_trit=10.0,            # Tritium processing power [MW]; DEFAULT DT
    p_house=4.0,            # Housekeeping power [MW]; DEFAULT
    p_cryo=90.0,            # Cryogenic system power [MW]
                            # UNCERTAIN: analysis.md §Section 2 "Cryogenic Parasitic
                            # Power Load" and §Section 5 Missing Parameters
                            # WISTELL-D analog (10.1 m QI, 2113 MWth): 152 kW magnet
                            # nuclear heating → 63.3 MWe cryogenic load (~3% of fusion
                            # power). GIGA at 18 m / 3000 MWth: lower bound ~3% ×
                            # 3000 MWth / thermal-to-electric = ~90 MWe (conservative).
                            # Source: frontiersin-journals-nuclear-engineering-articles-
                            # 10-3389.md §Discussion; analysis.md §Section 5

    # ── Cost overrides ─────────────────────────────────────────────────────
    cost_overrides={
        "CAS22": cas22_central,
        # CAS22 = $7,788 M at central assumptions (noak_fraction=0.55,
        # blanket_complexity_multiplier=1.5, cas22_frac=65% of overnight).
        # Derivation:
        #   FOAK: €16.5B × 1.10 = $18.15B overnight
        #   NOAK (55% of FOAK): $9.98B
        #   CAS22 (65% of NOAK): $6.49B base
        #   Blanket/VV sub-component (40% of base): $2,596M × 1.5 = $3,894M
        #   Coil sub-component (40% of base): $2,596M
        #   Other (20% of base): $1,298M
        #   Total CAS22 with blanket complexity: $7,788M
        # Source: gauss-fusion-technical-summary.md §Funding; analysis.md §S2 Ch.1, §S5

        "CAS27": 200.0,
        # HCPB blanket option: beryllium pebble beds as neutron multiplier
        # (~40 mm Be layer per blanket ring; costing_constants.yaml note:
        # "For HCPB concepts with beryllium neutron multiplier, override to ~$200M")
        # UNCERTAIN: blanket type (HCPB vs. DCLL) is proprietary and blocking.
        # If DCLL chosen, CAS27 reverts to framework default (~$15M for PbLi fill).
        # Source: helias-blanket-studies.md §3.2; analysis.md §Section 2 Challenge 2
    },
)

# ── Print results ────────────────────────────────────────────────────────────

c = result.costs
pt = result.power_table

print("Large-Scale Stellarator (Gauss Fusion GIGA) — 1 GWe, 88% CF, 40 yr")
print(f"LCOE: {c.lcoe:.1f} $/MWh | Overnight: {c.overnight_cost:.0f} $/kW")
print(f"Fusion: {pt.p_fus:.0f} MW | Net: {pt.p_net:.0f} MW | Q_eng: {pt.q_eng:.2f}")
print()

# ── CAS breakdown ────────────────────────────────────────────────────────────

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

print(f"{'Code':<8} {'Account':<30} {'M$':>10}")
print("-" * 50)
for code, name, val in cas:
    print(f"{code:<8} {name:<30} {float(val):>10.1f}")
print("-" * 50)
print(f"{'':8} {'Total Capital':<30} {float(c.total_capital):>10.1f}")

# ── CAS22 sub-account detail (computed assumptions, not framework sub-accounts) ──

noak_overnight_central = FOAK_OVERNIGHT_USD_M * NOAK_FRACTION_CENTRAL
base_cas22_central = noak_overnight_central * CAS22_FRAC_OF_OVERNIGHT
coil_sub = base_cas22_central * CAS22_COIL_FRAC
blanket_sub_base = base_cas22_central * CAS22_BLANKET_FRAC
other_sub = base_cas22_central * CAS22_OTHER_FRAC
blanket_sub_adj = blanket_sub_base * BLANKET_COMPLEXITY_MULTIPLIER_CENTRAL

print()
print("CAS22 Sub-allocation (assumed; no published CAS breakdown for GIGA):")
print(f"  {'Coil system (C220103)':<35} {coil_sub:>10.1f} M$  (40% of base CAS22)")
print(f"  {'Blanket/VV (C220101+C220106) base':<35} {blanket_sub_base:>10.1f} M$  (40% of base)")
print(f"  {'Blanket complexity ×{:.1f} penalty'.format(BLANKET_COMPLEXITY_MULTIPLIER_CENTRAL):<35} {blanket_sub_adj - blanket_sub_base:>10.1f} M$  (added cost from 3D geometry)")
print(f"  {'Blanket/VV adjusted':<35} {blanket_sub_adj:>10.1f} M$")
print(f"  {'Other sub-accounts':<35} {other_sub:>10.1f} M$  (20% of base)")
print(f"  {'CAS22 total (overridden)':<35} {float(c.cas22):>10.1f} M$")

# ── Key assumptions ──────────────────────────────────────────────────────────

print()
print("=" * 60)
print("Key Assumptions")
print("=" * 60)
print(f"  FOAK capital:            €{FOAK_COST_EUR_B:.1f}B (midpoint of €15–18B stated range)")
print(f"  EUR/USD:                 {EUR_TO_USD:.2f} (assumed)")
print(f"  NOAK fraction (central): {NOAK_FRACTION_CENTRAL:.0%} of FOAK overnight")
print(f"  NOAK overnight (central): ${noak_overnight_central/1e3:.2f}B = ${noak_overnight_central/NET_ELECTRIC_MW:.0f}/kWe")
print(f"  CAS22 / overnight:       {CAS22_FRAC_OF_OVERNIGHT:.0%} (assumed allocation)")
print(f"  Blanket complexity mult: {BLANKET_COMPLEXITY_MULTIPLIER_CENTRAL:.1f}× (central; range 1.0–2.5)")
print(f"  eta_th (gross):          35.0%  [UNCERTAIN: HCPB assumption; DCLL ~40%]")
print(f"  p_cryo:                  90 MW  [UNCERTAIN: WISTELL-D analog lower bound]")
print(f"  p_input (ECRH):          75 MW  [UNCERTAIN: profile control only]")
print(f"  Availability:            {AVAILABILITY:.0%}    [Helios analog; GIGA-specific undisclosed]")
print(f"  Blanket type:            HCPB assumed (blocking gap; DCLL alternative)")

# ── Sensitivity analysis ─────────────────────────────────────────────────────
#
# Three sweeps:
#   1. Engineering/financial elasticities (model.sensitivity — over model params)
#   2. noak_fraction sweep 0.40–0.70 (primary LCOE driver; H1 hypothesis)
#   3. blanket_complexity_multiplier sweep 1.0–2.5 (F-2 finding; made explicit)

print()
print("=" * 60)
print("Sensitivity 1: Engineering and Financial Elasticities")
print("(Elasticity = %%LCOE / %%param, with CAS22 overridden = 0 gradient)")
print("=" * 60)

sens = model.sensitivity(result.params, cost_overrides={
    "CAS22": cas22_central,
    "CAS27": 200.0,
})

print("\nEngineering levers:")
for k, v in sorted(sens["engineering"].items(), key=lambda x: abs(x[1]), reverse=True):
    print(f"  {k:<28} {v:+.4f}")

print("\nFinancial:")
for k, v in sorted(sens["financial"].items(), key=lambda x: abs(x[1]), reverse=True):
    print(f"  {k:<28} {v:+.4f}")

# ── noak_fraction sweep ──────────────────────────────────────────────────────

print()
print("=" * 60)
print("Sensitivity 2: NOAK Fraction Sweep (H1 — primary LCOE lever)")
print(f"  blanket_complexity_multiplier fixed at {BLANKET_COMPLEXITY_MULTIPLIER_CENTRAL:.1f}×")
print("=" * 60)
print(f"  {'noak_fraction':<16} {'NOAK $/kWe':>12} {'CAS22 M$':>12} {'LCOE $/MWh':>12}")
print("  " + "-" * 54)

noak_fractions = [0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70]
for nf in noak_fractions:
    cas22_nf = compute_cas22_override(nf, BLANKET_COMPLEXITY_MULTIPLIER_CENTRAL)
    r_nf = model.forward(
        net_electric_mw=NET_ELECTRIC_MW,
        availability=AVAILABILITY,
        lifetime_yr=LIFETIME_YR,
        n_mod=1,
        construction_time_yr=CONSTRUCTION_TIME_YR,
        interest_rate=INTEREST_RATE,
        inflation_rate=INFLATION_RATE,
        noak=True,
        R0=18.0, plasma_t=1.7, elon=1.0,
        blanket_t=0.60, ht_shield_t=0.20, structure_t=0.15, vessel_t=0.10,
        plasma_volume=1500.0, B=6.0, n_e=1.0e20, T_e=12.0, Z_eff=1.3,
        R_w=0.6, wall_material="W", T_edge=0.05, tau_ratio=3.0,
        p_input=75.0, mn=1.1, eta_th=0.35,
        eta_p=0.50, eta_pin=0.50, eta_de=0.0,
        f_sub=0.03, f_dec=0.0,
        p_coils=3.0, p_cool=15.0, p_pump=1.0,
        p_trit=10.0, p_house=4.0, p_cryo=90.0,
        cost_overrides={"CAS22": cas22_nf, "CAS27": 200.0},
    )
    noak_spec = FOAK_OVERNIGHT_USD_M * nf / NET_ELECTRIC_MW * 1000.0  # $/kWe
    marker = " ← central" if nf == NOAK_FRACTION_CENTRAL else ""
    print(f"  {nf:<16.2f} {noak_spec:>12.0f} {cas22_nf:>12.0f} {float(r_nf.costs.lcoe):>12.1f}{marker}")

# ── blanket_complexity_multiplier sweep ─────────────────────────────────────

print()
print("=" * 60)
print("Sensitivity 3: Blanket Complexity Multiplier Sweep (F-2 finding)")
print(f"  noak_fraction fixed at {NOAK_FRACTION_CENTRAL:.0%}")
print("  Range: 1.0 (tokamak-equivalent) → 2.5 (extreme 3D geometry premium)")
print("  Applied to blanket/VV sub-component (40% of base CAS22)")
print("=" * 60)
print(f"  {'multiplier':<14} {'CAS22 M$':>12} {'blanket M$':>12} {'LCOE $/MWh':>12}")
print("  " + "-" * 52)

bcm_values = [1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5]
for bcm in bcm_values:
    cas22_bcm = compute_cas22_override(NOAK_FRACTION_CENTRAL, bcm)
    blanket_m_bcm = (FOAK_OVERNIGHT_USD_M * NOAK_FRACTION_CENTRAL
                     * CAS22_FRAC_OF_OVERNIGHT * CAS22_BLANKET_FRAC * bcm)
    r_bcm = model.forward(
        net_electric_mw=NET_ELECTRIC_MW,
        availability=AVAILABILITY,
        lifetime_yr=LIFETIME_YR,
        n_mod=1,
        construction_time_yr=CONSTRUCTION_TIME_YR,
        interest_rate=INTEREST_RATE,
        inflation_rate=INFLATION_RATE,
        noak=True,
        R0=18.0, plasma_t=1.7, elon=1.0,
        blanket_t=0.60, ht_shield_t=0.20, structure_t=0.15, vessel_t=0.10,
        plasma_volume=1500.0, B=6.0, n_e=1.0e20, T_e=12.0, Z_eff=1.3,
        R_w=0.6, wall_material="W", T_edge=0.05, tau_ratio=3.0,
        p_input=75.0, mn=1.1, eta_th=0.35,
        eta_p=0.50, eta_pin=0.50, eta_de=0.0,
        f_sub=0.03, f_dec=0.0,
        p_coils=3.0, p_cool=15.0, p_pump=1.0,
        p_trit=10.0, p_house=4.0, p_cryo=90.0,
        cost_overrides={"CAS22": cas22_bcm, "CAS27": 200.0},
    )
    marker = " ← central" if bcm == BLANKET_COMPLEXITY_MULTIPLIER_CENTRAL else ""
    print(f"  {bcm:<14.2f} {cas22_bcm:>12.0f} {blanket_m_bcm:>12.0f} {float(r_bcm.costs.lcoe):>12.1f}{marker}")

# ── Capacity factor sweep ────────────────────────────────────────────────────

print()
print("=" * 60)
print("Sensitivity 4: Capacity Factor Sweep (H3 — steady-state advantage)")
print(f"  noak_fraction={NOAK_FRACTION_CENTRAL:.0%}, blanket_complexity_mult={BLANKET_COMPLEXITY_MULTIPLIER_CENTRAL:.1f}×")
print("  Lower bound (pulsed tokamak analog) → Helios 88% upper anchor")
print("=" * 60)
print(f"  {'availability':<14} {'LCOE $/MWh':>12}  note")
print("  " + "-" * 50)

cf_values = [
    (0.75, "pulsed tokamak lower bound"),
    (0.80, "pulsed tokamak upper bound"),
    (0.85, "GIGA conservative"),
    (0.88, "Helios analog (central)"),
    (0.90, "GIGA optimistic"),
]
for cf, note in cf_values:
    r_cf = model.forward(
        net_electric_mw=NET_ELECTRIC_MW,
        availability=cf,
        lifetime_yr=LIFETIME_YR,
        n_mod=1,
        construction_time_yr=CONSTRUCTION_TIME_YR,
        interest_rate=INTEREST_RATE,
        inflation_rate=INFLATION_RATE,
        noak=True,
        R0=18.0, plasma_t=1.7, elon=1.0,
        blanket_t=0.60, ht_shield_t=0.20, structure_t=0.15, vessel_t=0.10,
        plasma_volume=1500.0, B=6.0, n_e=1.0e20, T_e=12.0, Z_eff=1.3,
        R_w=0.6, wall_material="W", T_edge=0.05, tau_ratio=3.0,
        p_input=75.0, mn=1.1, eta_th=0.35,
        eta_p=0.50, eta_pin=0.50, eta_de=0.0,
        f_sub=0.03, f_dec=0.0,
        p_coils=3.0, p_cool=15.0, p_pump=1.0,
        p_trit=10.0, p_house=4.0, p_cryo=90.0,
        cost_overrides={"CAS22": cas22_central, "CAS27": 200.0},
    )
    print(f"  {cf:<14.2f} {float(r_cf.costs.lcoe):>12.1f}  {note}")
