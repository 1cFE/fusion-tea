# STALE: analysis-rewritten-by-force
"""Magnetic Mirror (D-T) — Realta Fusion LCOE model setup.

Usage:
    uv run python model_setup.py              # print results to terminal
    uv run python model_setup.py | tee model_output.txt  # also save for synthesis stage

Modeling Approach
-----------------
This script models a commercial-scale axisymmetric tandem magnetic mirror power plant
using D-T fuel, informed by Realta Fusion's Hammir pre-conceptual design targets.
The 1costingfe framework is used with the MIRROR/DT concept type.

Concept Choice Rationale
------------------------
Realta Fusion (UW-Madison spin-out, founded 2022) pursues an axisymmetric tandem
magnetic mirror with HTS (REBCO) end-plug magnets and a venetian-blind direct energy
conversion (DEC) system. The key economic thesis is linear center-cell scaling:
commercial power is achieved by lengthening the center cell (~7 MWt/m) while holding
end-plug hardware and input power approximately constant.

Key Deviations from Framework Defaults
---------------------------------------
- eta_th retained at framework default of 0.40 (MARS 1983 overall plant efficiency was
  ~36%; 0.40 reflects modest modern improvement)
- eta_de set to 0.54 (MARS 1983 gridless DEC efficiency; Realta venetian-blind DEC
  is uncharacterized — this is a historical lower-bound proxy)
- f_dec set to 0.20 (D-T physics: 80% of fusion energy in neutrons captured by
  blanket, 20% in alpha particles available for DEC — DT physics constant)
- chamber_length = 70.0 m (commercial scale; Hammir pilot targets 50m for Q > 5;
  70m represents a Q ~8–10 commercial variant)
- p_input elevated to 100.0 MW (commercial scale NBI+ECH estimate for Q_plasma ~10;
  specific power requirements for Hammir are proprietary)
- No cost overrides: no plant-level cost data exists for Realta at any stage; all
  capital accounts use framework defaults with appropriate UNCERTAIN flags
- p_cryo elevated to 2.0 MW (larger REBCO magnet set at commercial scale)
- p_coils elevated to 10.0 MW (end-plug HTS + center-cell solenoid array at scale)

Data Quality Warning
--------------------
This model is HIGHLY UNCERTAIN. Realta has published no plant-level engineering
parameters, capital cost estimates, or LCOE projections. Almost every parameter
is either:
  - UNCERTAIN (analysis-inferred): derived from partial or historical data
  - DEFAULT: framework default with no concept-specific data to override
The LCOE output should be treated as an order-of-magnitude structural estimate only.
"""

from costingfe import ConfinementConcept, CostModel, Fuel

# ── Model instantiation ───────────────────────────────────────────────────────
model = CostModel(concept=ConfinementConcept.MIRROR, fuel=Fuel.DT)

# ── Plant configuration ───────────────────────────────────────────────────────

# --- Commercial plant targets ---
NET_ELECTRIC_MW = 500.0     # Commercial scale; Hammir pilot targets >50 MWe
                            # Source: aps-dpp-2025-sutherland.md §Hammir Facility
                            # UNCERTAIN: commercial plant size undisclosed; 500 MWe
                            # assumed for economic relevance (pilot is not viable at 50 MWe)

AVAILABILITY = 0.85         # DEFAULT: no availability model published for mirror geometry
                            # Open linear geometry may simplify maintenance access
                            # (analysis.md §S7: "direct physical access along center cell")
                            # but no maintenance schedule exists

LIFETIME_YR = 30            # DEFAULT: standard fusion plant design life
CONSTRUCTION_TIME_YR = 5.0  # DEFAULT: mirror geometry simpler than tokamak;
                            # mfe_mirror.yaml default; reflects linear assembly
INTEREST_RATE = 0.07        # DEFAULT: 7% real discount rate (standard industry)
INFLATION_RATE = 0.02       # DEFAULT
N_MOD = 1                   # Single commercial unit

NOAK = True                 # Nth-of-a-kind assumption for cost floor estimate

# ── Forward model ─────────────────────────────────────────────────────────────
result = model.forward(
    # No cost overrides: Realta has published zero plant-level cost data.
    # The only proxy is "$50M in REBCO tape alone for WHAM++" (pre-commercial device);
    # this cannot be extrapolated to a commercial Hammir CAS22 estimate.
    # Source: realta-fusion-hub-spotlight.md §Magnet Specifications
    cost_overrides={},

    # --- Customer requirements ---
    net_electric_mw=NET_ELECTRIC_MW,
    availability=AVAILABILITY,
    lifetime_yr=LIFETIME_YR,
    n_mod=N_MOD,
    construction_time_yr=CONSTRUCTION_TIME_YR,
    interest_rate=INTEREST_RATE,
    inflation_rate=INFLATION_RATE,
    noak=NOAK,

    # --- Mirror geometry (cylindrical center cell) ---
    R0=0.0,                 # No axis offset — cylindrical geometry, not toroidal
    plasma_t=1.5,           # Plasma radius [m]; DEFAULT: consistent with Hammir pilot scale
                            # Source: mfe_mirror.yaml default
    chamber_length=70.0,    # Center cell length [m]; UNCERTAIN: 50m is minimum for Q>5
                            # (arxiv-2411-06644-confinement-predictions.md §Hammir Design);
                            # 70m represents a Q~8–10 commercial variant consistent with
                            # "Q>10 possible with longer cell" projection
                            # Source: fusion-report-interview-realta.md §Performance Scaling
    blanket_t=0.60,         # DEFAULT: standard blanket thickness; linear geometry allows
                            # cylindrical blanket — MARS used LiPb (TBR=1.15) in this geometry
                            # Source: dossier.md §Key Sources (MARS study, OSTI 5981974)
    ht_shield_t=0.20,       # DEFAULT
    structure_t=0.15,       # DEFAULT
    vessel_t=0.10,          # DEFAULT

    # --- Power balance (tandem mirror with DEC) ---
    p_input=100.0,          # NBI + ECH heating [MW]; UNCERTAIN: proprietary for Hammir
                            # Estimated for commercial scale Q~5 (consistent with 70m
                            # center cell at ~7 MWt/m ≈ 490 MWt); P_input=100 MW is
                            # consistent with this fusion power target. If Q~10 were
                            # targeted, chamber_length would need to be ~140m and/or
                            # P_input reduced to ~50 MW.
                            # Source: arxiv-2411-06644-confinement-predictions.md §Hammir
                            # Design (50m→Q>5); fusion-report-interview-realta.md
                            # §Performance Scaling (~7 MWt/m)
    mn=1.1,                 # Neutron energy multiplier; DEFAULT: MARS LiPb blanket analogy
                            # Source: mfe_mirror.yaml default
    eta_th=0.40,            # Thermal conversion efficiency; UNCERTAIN: undisclosed
                            # MARS 1983 copper-magnet design showed ~36% overall efficiency
                            # Source: dossier.md §Key Sources (MARS study)
                            # Modern steam cycle may reach 40–45%; 0.40 is conservative middle
                            # Note: thermal cycle type (steam vs. sCO2) undisclosed
                            # Source: analysis.md §S5 Missing Parameters
    eta_p=0.50,             # Pumping efficiency; DEFAULT
    eta_pin=0.50,           # Heating system wall-plug efficiency; UNCERTAIN
                            # ECH gyrotrons (110 GHz on WHAM): ~45–55% wall-plug efficiency
                            # NBI efficiency: ~50%; blended estimate
                            # Source: analysis.md §S3 NBI+ECH subsystem
    eta_de=0.54,            # DEC efficiency on end-loss ions; UNCERTAIN
                            # Only historical data: MARS 1983 gridless direct converters ~54%
                            # Source: dossier.md §Key Sources (MARS study, Logan 1983)
                            # Realta venetian-blind DEC design uncharacterized (TRL 2–3)
                            # Source: analysis.md §S2 Challenge 2; §S3 DEC subsystem
                            # This is a historical LOWER BOUND — actual performance unknown
    f_sub=0.03,             # BOP subsystem power fraction; DEFAULT
    f_dec=0.20,             # Fraction of transport power to DEC; UNCERTAIN
                            # D-T physics: 80% of fusion energy in 14.1 MeV neutrons
                            # (captured in blanket), 20% in 3.5 MeV alpha particles
                            # Alphas escape through open ends and are available for DEC
                            # Source: realta-fusion-hub-spotlight.md §Fuel & Reaction
                            #   "80% of output energy in neutrons"
                            # analysis.md §S2 Challenge 2: "DEC efficiency ~54% applies
                            # to ~20% of fusion energy" — alpha fraction only
    p_coils=10.0,           # Solenoid + end-plug coil power [MW]; UNCERTAIN
                            # UNCERTAIN: no coil power published for Hammir or any
                            # mirror-scale HTS system. Elevated from mfe_mirror.yaml
                            # default (5 MW) based on inference: larger commercial REBCO
                            # array (end plugs ≥ WHAM scale + 70m center-cell solenoids)
                            # will draw more cooling and control power than the default.
                            # Source for rationale: wham-experiment-details.md §Magnet
                            # System (REBCO material and scale). No quantitative source
                            # exists.
    p_cool=25.0,            # Cooling system power [MW]; UNCERTAIN
                            # Elevated from default (20 MW) for 70m center-cell cooling load
    p_pump=2.0,             # Primary coolant pumping [MW]; DEFAULT
    p_trit=12.0,            # Tritium processing [MW]; UNCERTAIN
                            # Li blanket breeding confirmed; type undisclosed
                            # Source: fusion-report-interview-realta.md §Energy Conversion
                            # Elevated from default (10 MW) for open-ended exhaust management
    p_house=5.0,            # Housekeeping power [MW]; DEFAULT (elevated for 70m plant)
    p_cryo=2.0,             # Cryogenic power [MW]; UNCERTAIN
                            # End-plug HTS magnets (REBCO) + center-cell solenoid cryostat
                            # Elevated from default (1 MW) for larger magnet set at commercial scale
                            # HTS cryo loads are modest vs. LTS (REBCO operates at 20 K vs. 4 K)
                            # Source: wham-experiment-details.md §Magnet System (REBCO at 20 K)
)

# ── Results ───────────────────────────────────────────────────────────────────
c = result.costs
pt = result.power_table

print("=" * 60)
print("Magnetic Mirror (D-T) — Realta Fusion / Hammir Commercial")
print(f"Net electric: {NET_ELECTRIC_MW:.0f} MWe | Availability: {AVAILABILITY:.0%} | Lifetime: {LIFETIME_YR} yr")
print("=" * 60)

lcoe_ckwh = float(c.lcoe) / 10
print(
    f"LCOE: {c.lcoe:.1f} $/MWh ({lcoe_ckwh:.2f} ¢/kWh)"
    f" | Overnight: {c.overnight_cost:.0f} $/kW"
)
print(f"Fusion: {pt.p_fus:.0f} MW | Net: {pt.p_net:.0f} MW | Q_eng: {pt.q_eng:.1f}")
print(f"Recirculating fraction: {pt.rec_frac:.1%}")
print()

# ── CAS cost breakdown ────────────────────────────────────────────────────────
cas = [
    ("CAS10", "Preconstruction", c.cas10),
    ("CAS21", "Buildings", c.cas21),
    ("CAS22", "Reactor Plant Equipment", c.cas22),
    ("CAS23", "Turbine Plant", c.cas23),
    ("CAS24", "Electrical Plant", c.cas24),
    ("CAS25", "Miscellaneous", c.cas25),
    ("CAS26", "Heat Rejection", c.cas26),
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

# ── CAS22 sub-account detail ─────────────────────────────────────────────────
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
Data quality rating: Limited (analysis.md §S1).

Physics basis:
  - Q_plasma > 5 at 50m center cell (simulation only, not experimentally validated)
    Source: arxiv-2411-06644-confinement-predictions.md §Hammir Design
  - 70m commercial center cell assumed for Q ~ 8–10
    Source: fusion-report-interview-realta.md §Performance Scaling ("Q>10 possible")
  - ~7 MWt/m center-cell thermal power scaling
    Source: fusion-report-interview-realta.md §Performance Scaling

Key uncertainties (by impact on LCOE):
  1. Commercial plant scale: only pilot (>50 MWe) published
  2. Thermal efficiency (eta_th=0.40): thermal cycle type undisclosed
     MARS 1983 historical baseline: ~36% overall plant efficiency
  3. Recirculating power (p_input=100 MW): NBI+ECH requirements proprietary
  4. DEC efficiency (eta_de=0.54): Realta venetian-blind design uncharacterized
     Only MARS 1983 historical gridless DEC data available (~54%)
  5. DEC capital cost: truly-unknown; venetian-blind design TRL 2–3
     (Not capturable as cost override — no precedent data)
  6. REBCO tape cost: $50M for WHAM++ alone (pre-commercial intermediate device)
     Hammir-scale REBCO: likely $100–500M range (no published coil spec)
     Source: realta-fusion-hub-spotlight.md §Magnet Specifications
  7. End-plug confinement physics: undemonstrated in tandem configuration
     Anvil (next step) not yet built; physics gap comparable to
     claiming Q=10 before achieving burning plasma

Not captured by this model:
  - DEC capital cost uncertainty (no override data → framework default used)
  - REBCO supply chain premium (shared with tokamak analyses; no concept-specific
    override possible without published magnet specifications)
  - End-plug confinement physics failure risk (would manifest as higher p_input)
  - Regulatory pathway uncertainty for open linear geometry
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
