"""Large-Scale Stellarator (Gauss Fusion GIGA) — LCOE model setup.

Modeling approach
-----------------
This script builds an NOAK LCOE estimate for Gauss Fusion's GIGA plant, a
quasi-isodynamic stellarator derived from the HELIAS HSR4/18 reactor study.
The concept is modeled with ConfinementConcept.STELLARATOR / Fuel.DT.

Key deviations from framework stellarator defaults
---------------------------------------------------
• Machine scale: R0 = 18 m (3× the default 5.5 m and 3× W7-X) — the single
  largest departure from defaults, driving much larger CAS22 values.
• Plasma volume: 1,500 m³ (vs. default 800 m³ for a generic 5.5 m stellarator).
• Gross thermal efficiency: 35% (HCPB/steam Rankine; default stellarator uses 46%).
  Net (1 GWe / 3 GWth) = 33.3%; a gross→net gap of ~5–7 pp is absorbed by the
  recirculating power terms (p_input, p_cryo, p_coils, etc.).
• p_input = 75 MW: ECRH for startup and profile control only (no current drive).
  Stellarators do not need sustained NBI/ECRH for current drive — a significant
  recirculating-power advantage over pulsed or driven tokamaks.
• p_cryo = 20 MW (UNCERTAIN): Large LTS/HTS coil system (~35,000 t SC coil mass)
  requires substantially more cryoplant capacity than the default 0.8 MW.
• construction_time_yr = 10 (UNCERTAIN): Conservative NOAK estimate for a
  machine 3× ITER's minor radius and 40 non-planar 300-tonne coils. ITER
  construction (6.2 m, tokamak geometry) took >10 years.
• lifetime_yr = 40: Magnet and vacuum vessel design life per Gauss disclosure.
• CAS27 override = $200 M: HCPB blanket uses beryllium neutron multiplier
  (~40 mm pebble beds); per costing_constants.yaml guidance.

FOAK reality check
------------------
Gauss Fusion states FOAK cost at €15–18 B (analysis.md §S5, §S2 challenge 1).
At ~1.09 USD/EUR (2024), this is ~$16–20 B overnight for 1 GWe = $16,000–20,000/kW.
The NOAK output from this model should be substantially lower and represents
a fleet-learning projection. No NOAK figure has been published by Gauss Fusion.
The FOAK figure should not be interpreted as the model output — this script
models NOAK economics, and the FOAK range is a bounding sanity check.

Biggest uncertainties (in order of LCOE impact)
------------------------------------------------
1. NOAK capital cost (no published projection; FOAK >>NOAK by factor ~2–3×)
2. Capacity factor (no published target; 85% used as stellarator ceiling)
3. Blanket type (HCPB vs. DCLL undisclosed; affects eta_th ±5 pp, CAS27)
4. Construction time (10 yr used; large-scale complexity could extend further)
5. Cryogenic power (large SC system; 20 MW is an order-of-magnitude estimate)

Usage:
    uv run python model_setup.py              # print results to terminal
    uv run python model_setup.py | tee model_output.txt  # also save for synthesis stage
"""

from costingfe import ConfinementConcept, CostModel, Fuel

# ── Model instantiation ──────────────────────────────────────────────
model = CostModel(concept=ConfinementConcept.STELLARATOR, fuel=Fuel.DT)

# ── Plant configuration constants ────────────────────────────────────
# Customer-level (top of the costing pyramid)
NET_ELECTRIC_MW = 1000.0   # 1 GWe; analysis.md §S5 — stated design target
                            # Source: gauss-fusion-technical-summary.md §GIGA Power Plant

AVAILABILITY = 0.85        # UNCERTAIN: no published capacity-factor target from Gauss Fusion
                            # Stellarators are disruption-free → in principle higher CF than
                            # pulsed tokamaks, but complex 3D blanket maintenance may
                            # offset this. 85% used as optimistic steady-state ceiling.
                            # analysis.md §S2 challenge 6, §S6 gap #2

LIFETIME_YR = 40.0         # Magnet and vacuum vessel design life
                            # Source: gauss-fusion-technical-summary.md §GIGA Power Plant
                            # analysis.md §S5 "Magnet and vacuum vessel life"

# ── Forward call ─────────────────────────────────────────────────────
result = model.forward(
    # ── Customer requirements ──────────────────────────────────────
    net_electric_mw=NET_ELECTRIC_MW,
    availability=AVAILABILITY,
    lifetime_yr=LIFETIME_YR,
    n_mod=1,                        # Single-unit GIGA plant (no modular fleet assumed)
    construction_time_yr=10.0,      # UNCERTAIN: large-scale construction; ITER (6.2 m tokamak)
                                    # took 10+ yr; GIGA at 18 m is 3× ITER minor radius.
                                    # Default stellarator is 8 yr; 10 yr used for NOAK.
                                    # analysis.md §S2 challenge 4, §S3 (scale extrapolation)
    interest_rate=0.07,             # DEFAULT: standard 7% WACC (no Gauss-specific disclosure)
    inflation_rate=0.0245,          # DEFAULT: 2.45% US CPI (framework default)
    noak=True,                      # NOAK analysis — FOAK €15–18B is not model output
                                    # analysis.md §S5 "FOAK capital cost", §S6 gap #1

    # ── GIGA geometry ──────────────────────────────────────────────
    # HSR4/18 heritage: 4 field periods, 18 m major radius
    # Source: gauss-fusion-technical-summary.md §GIGA Power Plant; dossier.md §Driver Technology
    R0=18.0,                        # Major radius [m]; analysis.md §S5 — high confidence
    plasma_t=1.7,                   # Minor radius a [m]; analysis.md §S5 — high confidence
                                    # Source: gauss-fusion-technical-summary.md §GIGA Power Plant
    elon=1.0,                       # DEFAULT: effective elongation for cost geometry;
                                    # quasi-isodynamic stellarators have non-circular cross-
                                    # section but the CAS volume scaling uses 1.0 as default.
    blanket_t=0.60,                 # DEFAULT stellarator blanket thickness [m]; consistent
                                    # with HCPB HELIAS design (~600 mm radial build)
                                    # Source: helias-blanket-studies.md §3.2 (material layers)
    ht_shield_t=0.20,               # DEFAULT: high-temperature shield thickness [m]
    structure_t=0.15,               # DEFAULT: primary structure thickness [m]
    vessel_t=0.10,                  # DEFAULT: vacuum vessel shell thickness [m]

    # ── Power balance ──────────────────────────────────────────────
    # Gross thermal output ~3 GWth at 35% efficiency → 1,050 MWe gross (≈1 GWe net)
    # Net efficiency = 1 GWe / 3 GWth = 33.3%; gross ~35% (HCPB/steam Rankine)
    p_input=75.0,                   # UNCERTAIN: ECRH power [MW] for startup + profile control
                                    # No current drive needed — rotational transform is geometric.
                                    # Range: 50–100 MW stated in analysis.md §S2 challenge 6,
                                    # §S7 "Current drive vs. ECRH-only flat-top"
                                    # This is the key steady-state advantage over driven tokamaks.
    mn=1.1,                         # DEFAULT: neutron energy multiplier (blanket Q; standard DT)
    eta_th=0.35,                    # HCPB/steam Rankine gross thermal efficiency
                                    # HELIAS reference: ~35% standard, >40% TAURO advanced
                                    # Source: helias-reactor-context.md §7 "The Helias Reactor
                                    # as a Power Plant"; analysis.md §S5 "Gross thermal efficiency"
                                    # UNCERTAIN: DCLL blanket could reach ~40%; blanket type undisclosed
                                    # analysis.md §S2 challenge 2, §S6 gap #3, #6
    eta_p=0.5,                      # DEFAULT: pumping efficiency
    eta_pin=0.5,                    # DEFAULT: ECRH wall-plug efficiency (~50–55% for gyrotrons)
                                    # Source: analysis.md §S3 "ECRH Heating Systems — TRL 6–7"
                                    # Note: improvement to >60% stated as needed for full NOAK
    eta_de=0.85,                    # DEFAULT: DEC efficiency (not used for DT stellarator)
    f_sub=0.03,                     # DEFAULT: subsystem power fraction
    f_dec=0.0,                      # No direct energy conversion in stellarator DT config

    # Parasitic loads — all values UNCERTAIN; no GIGA-specific breakdown published
    p_coils=5.0,                    # UNCERTAIN: coil power [MW]; default is 3.0 MW for
                                    # generic stellarator. 40 non-planar coils at 300t each
                                    # with ~250 demountable joints per coil (~10,000 joints
                                    # at 1 nΩ × (100kA)² = 10 W/joint → 0.1 MW ohmic loss).
                                    # The 5 MW accounts for control magnets, correction coils.
                                    # Source: gauss-fusion-technical-summary.md §Magnet System;
                                    # analysis.md §S5 "Demountable joint resistance target"
    p_cool=20.0,                    # UNCERTAIN: primary coolant pumping [MW]; scaled up from
                                    # default 15 MW for larger HCPB coolant circuit (8 MPa He)
                                    # Source: helias-blanket-studies.md §Table 5 (8.0 MPa He)
    p_pump=2.0,                     # UNCERTAIN: auxiliary pumping [MW]; larger system than default
    p_trit=15.0,                    # UNCERTAIN: tritium processing power [MW]; GIGA requires
                                    # ~55 kg/yr tritium throughput (1 GWe D-T plant); larger
                                    # than default 10 MW for the higher throughput.
                                    # analysis.md §S3 "Tritium Fuel Cycle"
    p_house=5.0,                    # UNCERTAIN: housekeeping power [MW]; larger plant than default
    p_cryo=20.0,                    # UNCERTAIN: cryogenic power [MW]; default is 0.8 MW for
                                    # generic ~5.5 m stellarator. GIGA SC coil mass ~35,000t
                                    # (vs. W7-X ~250t @ 0.6 MW cryoplant).
                                    # Order-of-magnitude estimate; actual cryoplant design
                                    # not published. analysis.md §S3, §S4

    # ── Plasma / impurity parameters ──────────────────────────────
    plasma_volume=1500.0,           # Plasma volume [m³]; analysis.md §S5 — high confidence
                                    # Source: gauss-fusion-technical-summary.md §GIGA Power Plant
    B=6.0,                          # On-axis magnetic field [T]; analysis.md §S5 — high confidence
                                    # Source: dossier.md §Driver Technology
    n_e=1.0e20,                     # DEFAULT: electron density [m⁻³]; HELIAS design point
    T_e=12.0,                       # DEFAULT: electron temperature [keV]; HELIAS design point
    Z_eff=1.3,                      # DEFAULT: effective charge
    wall_material="W",              # DEFAULT: tungsten first wall; standard for HELIAS/GIGA
                                    # Source: helias-blanket-studies.md §3.2 "2 mm W armor"
    T_edge=0.05,                    # DEFAULT: edge temperature [keV] at island divertor
    tau_ratio=3.0,                  # DEFAULT: impurity confinement / energy confinement ratio
    R_w=0.6,                        # DEFAULT: wall reflectivity for synchrotron (metallic)

    # ── Cost overrides ─────────────────────────────────────────────
    cost_overrides={
        # CAS27 — Special Materials: HCPB beryllium neutron multiplier
        # HCPB blanket uses Be pebble beds (~40 mm thick per layer) as neutron
        # multiplier. Default CAS27 assumes PbLi fill ($15M). HCPB Be requirement
        # is substantially higher. Override per costing_constants.yaml guidance:
        # "For HCPB concepts with beryllium neutron multiplier, override CAS27 to ~$200M"
        # Source: helias-blanket-studies.md §3.2; costing_constants.yaml comment;
        # analysis.md §S4 "Beryllium (HCPB Neutron Multiplier) — Constrained Supply"
        # UNCERTAIN: DCLL blanket would reduce this to ~$20–30M (no Be, LiPb only)
        "CAS27": 200.0,
    },
)

# ── Cost Results by CAS ─────────────────────────────────────────────
c = result.costs
pt = result.power_table

print("Large-Scale Stellarator (Gauss Fusion GIGA) — NOAK 1 GWe")
print(f"  HELIAS HSR4/18 heritage | R0 = 18 m | Quasi-isodynamic | D-T | HCPB blanket (assumed)")
print()
print(f"LCOE: {c.lcoe:.1f} $/MWh | Overnight: {c.overnight_cost:.0f} $/kW")
print(f"Fusion: {pt.p_fus:.0f} MW | Net: {pt.p_net:.0f} MW | Q_eng: {pt.q_eng:.1f}")
print()
print(f"  FOAK reality check: €15–18B stated (Gauss CDR) = ~$16,000–20,000/kWe")
print(f"  This NOAK estimate should be significantly below the FOAK figure.")
print()

cas = [
    ("CAS10", "Preconstruction", c.cas10),
    ("CAS21", "Buildings", c.cas21),
    ("CAS22", "Reactor Plant Equipment", c.cas22),
    ("CAS23", "Turbine Plant", c.cas23),
    ("CAS24", "Electrical Plant", c.cas24),
    ("CAS25", "Miscellaneous", c.cas25),
    ("CAS26", "Heat Rejection", c.cas26),
    ("CAS27", "Special Materials", c.cas27),
    ("CAS28", "Digital Twin", c.cas28),
    ("CAS29", "Contingency", c.cas29),
    ("CAS30", "Indirect Costs", c.cas30),
    ("CAS40", "Owner's Costs", c.cas40),
    ("CAS50", "Supplementary", c.cas50),
    ("CAS60", "IDC", c.cas60),
    ("CAS70", "O&M (annualized)", c.cas70),
    ("CAS80", "Fuel (annualized)", c.cas80),
    ("CAS90", "Financial", c.cas90),
]

print(f"{'Code':<8} {'Account':<28} {'M$':>10}")
print("-" * 48)
for code, name, val in cas:
    print(f"{code:<8} {name:<28} {float(val):>10.1f}")
print("-" * 48)
print(f"{'':8} {'Total Capital':<28} {float(c.total_capital):>10.1f}")

# ── CAS22 Sub-account Detail ─────────────────────────────────────────
print()
print("CAS22 Sub-account Detail (Reactor Plant Equipment):")
print(f"{'Account':<12} {'M$':>10}")
print("-" * 24)
cas22_keys = [
    ("C220101", "First Wall + Blanket"),
    ("C220102", "Shield"),
    ("C220103", "Coils"),
    ("C220104", "Heating"),
    ("C220105", "Structure"),
    ("C220106", "Vacuum"),
    ("C220107", "Power Supplies"),
    ("C220108", "Divertor"),
    ("C220109", "DEC"),
    ("C220111", "Installation"),
    ("C220200", "Coolant"),
    ("C220300", "Aux Cooling"),
    ("C220400", "Rad Waste"),
    ("C220500", "Fuel Handling"),
    ("C220600", "Other Equipment"),
    ("C220700", "I&C"),
]
d = result.cas22_detail
for key, label in cas22_keys:
    if key in d:
        print(f"  {key:<10} {label:<20} {float(d[key]):>10.1f}")

# ── Key Assumptions Summary ──────────────────────────────────────────
print()
print("Key Assumptions (Large-Scale Stellarator / GIGA):")
print("  Concept       Quasi-isodynamic stellarator (HSR4/18 heritage, 4 field periods)")
print("  Company       Gauss Fusion GmbH (Munich); CDR reviewed 2025–2026")
print(f"  Scale         R0 = 18 m | a = 1.7 m | V_plasma = 1,500 m³")
print(f"  B-field       6 T on-axis | 12–13 T peak coil (Nb3Sn or REBCO required)")
print(f"  Magnets       40 non-planar coils × ~300 t each | ~250 demountable joints/coil")
print(f"  Blanket       HCPB assumed (undisclosed); eta_th = 35% (steam Rankine)")
print(f"                DCLL alternative: eta_th ~40%; blanket type is blocking gap")
print(f"  Steady-state  No current drive; ECRH ~75 MW for startup + profile control only")
print(f"  Availability  {AVAILABILITY:.0%} — no published target; disruption-free advantage")
print(f"                offset by complex 3D blanket maintenance (80 segment shapes)")
print(f"  Lifetime      {LIFETIME_YR:.0f} yr (magnet + VV design life; blanket replaced ~8× at 5 yr)")
print(f"  Costing       NOAK; FOAK = €15–18B (~$16,000–20,000/kWe) — not the model output")
print(f"  NOAK unknowns No fleet learning curve published; NOAK may be 40–60% of FOAK")
print(f"  CAS27 override $200M for HCPB Be neutron multiplier (DCLL alternative: ~$25M)")

# ── Sensitivity Analysis ─────────────────────────────────────────────
sens = model.sensitivity(result.params, cost_overrides={"CAS27": 200.0})

print("\nSensitivity (elasticity = %LCOE / %param)")
print("-" * 48)

print("\nEngineering levers:")
for k, v in sorted(sens["engineering"].items(), key=lambda x: abs(x[1]), reverse=True):
    print(f"  {k:<28} {v:+.4f}")

print("\nFinancial:")
for k, v in sorted(sens["financial"].items(), key=lambda x: abs(x[1]), reverse=True):
    print(f"  {k:<28} {v:+.4f}")
