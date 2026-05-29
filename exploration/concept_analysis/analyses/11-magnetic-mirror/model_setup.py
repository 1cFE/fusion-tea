"""Magnetic Mirror (D-T) — Realta Fusion (CoSMo / Hammir).

Modeling approach:
    Uses the MFE MIRROR / DT model for Realta's CoSMo (Compact, Scalable, Modular)
    axisymmetric tandem mirror concept. The commercial design point is extrapolated
    beyond the Hammir pilot plant (Pe > 50 MWe) to a 500 MWe commercial-scale plant,
    consistent with Realta's linear scaling thesis (~7 MWt/m center cell).

    Power balance reflects:
      - Steady-state NBI + ECH heating with approximately constant end-plug input
        power (Realta's core economic argument: input power fixed while output scales
        with center cell length)
      - Dual energy conversion: thermal blanket (80% neutron energy) + venetian-blind
        DEC on alpha particles (20% of fusion energy at ~54% MARS efficiency)
      - D-T fuel cycle with LiPb-analogue breeding blanket (MARS as closest cost model)

Concept choice rationale:
    ConfinementConcept.MIRROR captures the cylindrical solenoid geometry, DEC-capable
    power balance, and solenoid coil cost model appropriate for an axisymmetric tandem
    mirror. Fuel.DT activates the correct D-T cost scaling: full breeding blanket,
    tritium processing, heavy neutron shielding, and full remote handling suite.

Key deviations from steady_state_mirror.yaml defaults:
    - plasma_t = 0.75 m (arXiv Table 3: 0.54–0.78 m range for 50 m pilot;
      commercial scale slightly larger)
      Source: arxiv-2411-06644-confinement-predictions.md §Hammir Design, Table 3
    - chamber_length = 70 m (commercial extrapolation beyond 50 m Hammir pilot;
      at ~7 MWt/m → ~490 MWt fusion power; Q > 10 projected for longer cells)
      Source: fusion-report-interview-realta.md §Performance Scaling;
              arxiv-2411-06644-confinement-predictions.md §Hammir Design
    - p_input = 40 MW (arXiv-anchored: 30–40 MW for 50 m pilot; commercial extrapolation
      assumes constant end-plug power per linear scaling thesis)
      Source: arxiv-2411-06644-confinement-predictions.md Table 3 (derived);
              analysis.md §Section 5 (NBI+ECH input power ≈30–40 MW, medium confidence)
    - eta_th = 0.36 (MARS 1983 steam Rankine plant efficiency ~36%; sCO2 could reach
      40–45% but blanket/cycle type undisclosed by Realta)
      Source: analysis.md §Section 5 (MARS analogue, low confidence)
    - eta_de = 0.54 (MARS 1983 gridless DEC; venetian-blind design uncharacterized)
      Source: analysis.md §Section 5 (DEC efficiency, low confidence)
    - f_dec = 0.20 (D-T nuclear physics hard limit: 20% alpha fraction)
      Source: analysis.md §Section 2, Challenge 4; realta-fusion-hub-spotlight.md
    - p_coils = 8 MW, p_cryo = 2 MW (elevated for 70 m commercial REBCO magnet set)
      Source: wham-experiment-details.md §Magnet System (17 T HTS solenoids, CFS-built)
    - No cost overrides: zero Realta-specific capital cost data is available for any account

WARNING — DATA QUALITY:
    Realta has published no plant-level engineering parameters, capital cost estimates,
    or LCOE projections for Hammir or any commercial design. Nearly every parameter is
    inferred from arXiv:2411.06644 (pilot physics), MARS 1983 (historical analogue), or
    framework defaults. End-plug confinement at commercial Q has never been experimentally
    validated. LCOE output is an order-of-magnitude structural estimate only.
    Data availability rating: Limited (analysis.md §Section 1).

Usage:
    uv run python model_setup.py              # print results to terminal
    uv run python model_setup.py | tee model_output.txt  # also save for synthesis stage
"""

from costingfe import ConfinementConcept, CostModel, Fuel

# ── Model instantiation ────────────────────────────────────────────────────
model = CostModel(concept=ConfinementConcept.MIRROR, fuel=Fuel.DT)

# ── Native design point ────────────────────────────────────────────────────
# Hammir pilot target: Pe > 50 MWe for 3+ hours continuously.
# Source: aps-dpp-2025-sutherland.md §Hammir Facility (Pilot Plant) [high confidence]
# Commercial plant is expected to be substantially larger.
# 500 MWe is used as a reference commercial scale; MARS/MINIMARS found mirror LCOE
# saturates near ~600 MWe (1983 technology analogue).
# Source: analysis.md §Section 5 "LCOE scaling saturation (historical): ~600 MWe" [low confidence]
# UNCERTAIN: Realta has published no commercial plant size target.
_NATIVE_MW = 500.0

# ── Shared kwargs (common to both forward() calls) ─────────────────────────
_SHARED_KWARGS = dict(

    # ── Financial / lifecycle ─────────────────────────────────────────────
    availability=0.85,
    # UNCERTAIN: No capacity factor published by Realta. Pilot targets "at least 3 hours
    # continuously" (aps-dpp-2025-sutherland.md §Hammir Facility) — not a commercial
    # availability target. DEC electrode replacement may reduce availability.
    # Source: analysis.md §Section 3 "Direct Energy Conversion: no fusion-condition
    #   survivability data"; §Section 5 "Capacity factor: proprietary / important"
    lifetime_yr=30,              # DEFAULT: standard fusion reference; no concept data
    n_mod=1,
    construction_time_yr=5.0,   # DEFAULT: steady_state_mirror.yaml; linear geometry
                                 # simpler than toroid; modular center-cell assembly possible

    # ── Mirror geometry (cylindrical center cell) ─────────────────────────
    R0=0.0,                  # No toroidal axis offset for cylinder; steady_state_mirror.yaml

    plasma_t=0.75,           # Plasma radius [m].
                             # arXiv Table 3: 0.54 m (Optimum) / 0.78 m (Alternate) for 50 m pilot.
                             # 0.75 m is a central estimate for a 70 m commercial design.
                             # Source: arxiv-2411-06644-confinement-predictions.md §Table 3 [medium]

    chamber_length=70.0,     # Center cell length [m].
                             # UNCERTAIN: Hammir pilot = 50 m (Q > 5 modeled, not validated).
                             # Source: arxiv-2411-06644-confinement-predictions.md §Hammir Design
                             # "Q > 10 possible with longer center cell" (length unspecified).
                             # Source: fusion-report-interview-realta.md §Performance Scaling [secondary]
                             # 70 m extrapolated for Q ~ 8–10 commercial variant; at 7 MWt/m:
                             # P_fus ≈ 490 MWt. Source: analysis.md §Section 2, Challenge 2

    blanket_t=0.80,          # Blanket thickness [m]; DEFAULT: steady_state_mirror.yaml
                             # D-T breeding blanket required; MARS used LiPb (TBR 1.15).
                             # Realta blanket type not disclosed (FLiBe/LiPb/liquid-Li/HCPB).
                             # Source: analysis.md §Section 2, Challenge 5; §Section 5 "Blanket
                             #   type: proprietary / blocking"

    ht_shield_t=0.20,        # DEFAULT: steady_state_mirror.yaml
    structure_t=0.15,        # DEFAULT: steady_state_mirror.yaml
    vessel_t=0.10,           # DEFAULT: steady_state_mirror.yaml

    # ── Power balance ─────────────────────────────────────────────────────

    p_input=40.0,            # Total NBI + ECH heating power [MW].
                             # arXiv Table 3 (50 m Optimum): P_fus=175 MW, Q=5.8
                             # → P_input ≈ 30 MW. Analysis §5 cites 35 MW as midpoint.
                             # Source: arxiv-2411-06644-confinement-predictions.md Table 3
                             #   (NBI+ECH input power: ≈30–40 MW) [medium confidence]
                             # Linear scaling thesis: "input power remains constant despite
                             # increased output" (end-plug power dominates, center cell grows).
                             # Source: fusion-report-interview-realta.md §Performance Scaling
                             # 40 MW used as conservative arXiv-anchored commercial estimate.
                             # UNCERTAIN: commercial Hammir heating power not published; prior
                             # automated pipeline used 100 MW — 2.5× spread.
                             # Source: analysis.md §Section 5 "NBI+ECH input power: blocking gap"

    mn=1.1,                  # Neutron energy multiplier; DEFAULT: steady_state_mirror.yaml
                             # Consistent with MARS LiPb blanket (TBR ~1.15).
                             # Source: analysis.md §Section 8 "MARS Study (Logan 1983)" [low]


    eta_p=0.50,              # Pumping efficiency; DEFAULT: steady_state_mirror.yaml

    eta_pin=0.50,            # Heating system wall-plug efficiency (NBI + ECH blended).
                             # ECH gyrotrons at 110 GHz: ~45–55% wall-plug efficiency.
                             # NBI systems: ~50–70% wall-plug (beam energy dependent).
                             # WHAM uses both ECH and NBI for end-plug operation.
                             # Source: wham-experiment-details.md §Heating Methods
                             # Source: analysis.md §Section 3 "ECH and HHFW: TRL 6–7"; "NBI: TRL 6–7"
                             # DEFAULT consistent with blended estimate.


    f_sub=0.03,              # BOP subsystem power fraction; DEFAULT: steady_state_mirror.yaml


    p_coils=8.0,             # Solenoid coil power [MW].
                             # Elevated from default (5 MW) for 70 m commercial REBCO magnet set:
                             # two end-mirror HTS solenoids (≥ WHAM scale, 17 T in-bore) plus
                             # a 70 m array of center-cell solenoid modules.
                             # Source: wham-experiment-details.md §Magnet System
                             #   (CFS-built REBCO, 17 T in-bore, >20 T on conductor)
                             # UNCERTAIN: commercial Hammir magnet count and field strength unpublished.

    p_cool=22.0,             # Cooling system power [MW]; modestly elevated from default (20 MW)
                             # for 70 m center-cell first wall and blanket cooling load.

    p_pump=1.5,              # Coolant pumping [MW]; DEFAULT: steady_state_mirror.yaml

    p_trit=10.0,             # Tritium processing power [MW]; DEFAULT: steady_state_mirror.yaml
                             # D-T fuel cycle with Li blanket confirmed; blanket type undisclosed.
                             # Source: fusion-report-interview-realta.md §Energy Conversion

    p_house=4.0,             # Housekeeping [MW]; DEFAULT: steady_state_mirror.yaml

    p_cryo=2.0,              # Cryogenic power [MW]; elevated from default (1 MW).
                             # REBCO operates at ~20 K — lower cryo load than 4 K LTS, but a
                             # 70 m solenoid array requires more infrastructure than the example.
                             # Source: wham-experiment-details.md §Magnet System

    # ── Cost overrides ────────────────────────────────────────────────────
    # No cost overrides. Realta has published zero plant-level cost estimates.
    # Only published cost signal: "$50M in REBCO tape for WHAM++" (sub-commercial).
    # Source: realta-fusion-hub-spotlight.md §Magnet Specifications
    # This signal cannot be extrapolated to a commercial Hammir CAS22 without
    # magnet geometry and current specifications.
    # Source: analysis.md §Section 5 "Capital cost breakdown: truly-unknown / important"
    #         §Section 6 gap #6 — no capital cost data for any Hammir subsystem.
    #
    # Framework DT defaults applied (costing_constants.yaml):
    #   blanket_unit_cost_dt    = 0.60 M$/m³  (LiPb breeding blanket)
    #   fuel_handling_dt_base   = 120 M$ at 1 GWe  (tritium processing)
    #   remote_handling_dt_base = 150 M$ at 1 GWe  (full RH suite)
    #   licensing_cost_dt       = 5 M$  (Part 30 DT)
    #   om_cost_dt              = 52 M$/yr at 1 GWe  (neutron + tritium overhead)
    #   decom_provision_dt      = 127 M$ at 1 GWe
    cost_overrides={},
)

# ── Forward model — native design point (500 MWe) ─────────────────────────
result = model.forward(net_electric_mw=_NATIVE_MW, **_SHARED_KWARGS)

# ── Forward model — 1 GWe comparison point ────────────────────────────────
# Scales from the 500 MWe native reference to 1000 MWe using per-account
# scaling laws. override_reference_mw anchors the scaling to _NATIVE_MW.
result_1gw = model.forward(
    net_electric_mw=1000.0,
    override_reference_mw=_NATIVE_MW,
    **_SHARED_KWARGS,
)

# ── Results ────────────────────────────────────────────────────────────────
c = result.costs
pt = result.power_table

print("Magnetic Mirror (D-T) — Realta Fusion (CoSMo / Hammir)")
print(f"500 MWe commercial extrapolation | 85% availability | 30 yr | NOAK")
print("UNCERTAIN: plasma params from arXiv:2411.06644 pilot + MARS 1983 analogue")
lcoe_ckwh = float(c.lcoe) / 10
print(
    f"LCOE: {c.lcoe:.1f} $/MWh ({lcoe_ckwh:.2f} ¢/kWh)"
    f" | Overnight: {c.overnight_cost:.0f} $/kW"
)
c1 = result_1gw.costs
print(
    f"1 GWe scaled: LCOE {c1.lcoe:.1f} $/MWh"
    f" | Overnight {c1.overnight_cost:.0f} $/kW"
)
print(f"Fusion: {pt.p_fus:.0f} MW | Net: {pt.p_net:.0f} MW | Q_eng: {pt.q_eng:.1f}")
print(f"Recirculating fraction: {pt.rec_frac:.1%}")
print()

# ── CAS cost breakdown ─────────────────────────────────────────────────────
cas = [
    ("CAS10", "Preconstruction",         c.cas10),
    ("CAS21", "Buildings",               c.cas21),
    ("CAS22", "Reactor Plant Equipment", c.cas22),
    ("CAS23", "Turbine Plant",           c.cas23),
    ("CAS24", "Electrical Plant",        c.cas24),
    ("CAS25", "Miscellaneous",           c.cas25),
    ("CAS26", "Heat Rejection",          c.cas26),
    ("CAS27", "Special Materials",       c.cas27),
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

# ── CAS22 sub-account detail ───────────────────────────────────────────────
print("\nCAS22 Reactor Plant Equipment Breakdown:")
print("-" * 48)
for k, v in sorted(result.cas22_detail.items()):
    if float(v) > 0:
        print(f"  {k:<28} {float(v):>10.1f} M$")

# ── Key assumptions summary ────────────────────────────────────────────────
print("\nKey Assumptions (confidence: low — MARS 1983 analogues + arXiv pilot physics):")
print("-" * 48)
print("  eta_th = 0.36        MARS steam Rankine analogue; cycle type undisclosed")
print("  eta_de = 0.54        MARS gridless DEC analogue; venetian-blind uncharacterized")
print("  f_dec  = 0.20        D-T alpha fraction (nuclear physics, high confidence)")
print("  p_input= 40 MW       arXiv pilot: 30–40 MW; constant end-plug thesis")
print("  L_cell = 70 m        extrapolated from 50 m Hammir pilot (Q>5)")
print("  Blanket: LiPb analogue (MARS TBR 1.15); Realta type undisclosed")
print("  Net electric: 500 MWe  commercial extrapolation; pilot target >50 MWe only")
print("  Availability: 85%  — no published target; DEC electrode lifetime unknown")
print()
print("Blocking gaps (analysis.md §Section 6):")
print("  #1  End-plug confinement at Q>5 never experimentally validated (Anvil ~2028)")
print("  #2  Commercial plant size not published (only >50 MWe pilot target)")
print("  #3  NBI+ECH input power for Hammir: blocking / proprietary")
print("  #4  Blanket type and TBR: blocking / proprietary")
print("  #5  Capital cost breakdown for any Hammir subsystem: truly-unknown")
print("  #6  DEC electrode lifetime in fusion conditions: truly-unknown")

# ── Sensitivity analysis ───────────────────────────────────────────────────
sens = model.sensitivity(result.params)

print("\nSensitivity (elasticity = %LCOE / %param)")
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
