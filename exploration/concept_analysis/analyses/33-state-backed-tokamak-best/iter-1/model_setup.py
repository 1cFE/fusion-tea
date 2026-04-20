"""1costingfe model: State-Backed Tokamak - BEST (Neo Fusion) — Commercial PFPP Analogue.

Usage:
    uv run python model_setup.py              # print results to terminal
    uv run python model_setup.py | tee model_output.txt  # also save for synthesis stage

Modeling approach:
    BEST (Burning Plasma Experimental Superconducting Tokamak) is an experimental
    device — it generates no electricity and is not itself the TEA target. This model
    represents the commercial PFPP (Prototype Fusion Power Plant) descendant that
    China's fusion roadmap (EAST → BEST → CFEDR → PFPP) aims to produce.

Concept rationale:
    The commercial PFPP is characterized by analogy to ARIES-AT (R₀ = 5.2 m,
    B₀ = 5.9 T, A ≈ 4), the closest published plant study to a conventional-
    aspect-ratio D-T tokamak at commercial scale with LTS-primary magnets.
    BEST parameters (R₀ = 3.6 m, B₀ = 6.15 T, Ip = 7 MA) constrain the
    experimental device, not the commercial end-state.

Key deviations from framework defaults:
    - eta_th = 0.347: sCO2 Brayton efficiency from published CFETR/BEST lineage
      studies (cfetr-power-conversion-studies.md); overrides framework preset of 0.47
    - R0 = 5.2 m, plasma_t = 1.3 m: ARIES-AT analogue for commercial PFPP scale
    - p_input = 200 MW: Q~10 estimate for commercial PFPP (P_fusion/Q ≈ 2200/10)
    - p_cryo = 8.0 MW: LTS Nb3Sn TF/PF coils at 4.5 K; substantially larger than
      HTS designs (which operate at 20 K or 77 K); scaled from ITER cryoplant
    - eta_pin = 0.60: weighted average of BEST 4-method H&CD portfolio (NBI 65%,
      ECRH 52%, ICRH 75%, LHCD 52%)
    - availability = 0.80: central estimate from 75–90% D-T MCF analogue range

CRITICAL UNCERTAINTY: The PFPP design point is completely unpublished. All machine
    parameters, cost overrides, and efficiency assumptions are by analogy. The LCOE
    output should be treated as a parameterized estimate with very low confidence.
    The Chinese construction cost advantage (2–4× lower than Western baseline) is NOT
    applied as a hard override — its magnitude in fusion context is uncharacterized.
"""

from costingfe import ConfinementConcept, CostModel, Fuel, PowerCycle

# ── Model creation ────────────────────────────────────────────────────────────
# sCO2 Brayton power cycle: sets appropriate CAS23/CAS26 BOP cost coefficients
# for compact, high-efficiency turbomachinery. eta_th overridden below to the
# published CFETR study value (34.7%) rather than the framework preset (47%).
# Source: cfetr-power-conversion-studies.md §Conclusions
model = CostModel(
    concept=ConfinementConcept.TOKAMAK,
    fuel=Fuel.DT,
    power_cycle=PowerCycle.BRAYTON_SCO2,
)

# ── Plant configuration ───────────────────────────────────────────────────────

# Commercial PFPP target: 1 GW net electric
# Source: analysis.md §S5 "Chinese program targets 1 GW class"; analogue to DEMO-class
# Confidence: low — no published PFPP design point
NET_ELECTRIC_MW = 1000.0

# Availability: central estimate from Araiinejad & Shirvan (2025) 75–90% range
# Source: analysis.md §S5, cross-referenced from 21-spherical-tokamak-hts §S5
# UNCERTAIN: Quasi-steady long-pulse operation implies different outage patterns;
# no Chinese program estimate exists
AVAILABILITY = 0.80

LIFETIME_YR = 30         # Standard commercial plant assumption; DEFAULT
INTEREST_RATE = 0.07     # 7% real discount rate; DEFAULT
INFLATION_RATE = 0.0245  # DEFAULT

# Construction time: 8 years — large LTS tokamak with ITER-lessons but
# Chinese construction efficiency assumed; ITER itself took 20+ years
# UNCERTAIN: No PFPP schedule published
CONSTRUCTION_TIME_YR = 8.0

# NOAK = True: modeling the mature commercial PFPP, not a prototype or FOAK device
NOAK = True

# ── Shared kwargs ─────────────────────────────────────────────────────────────
# Factored here for clarity; passed directly to model.forward()

_SHARED_KWARGS = dict(
    # ── Economics ─────────────────────────────────────────────────────────────
    availability=AVAILABILITY,
    lifetime_yr=LIFETIME_YR,
    n_mod=1,
    construction_time_yr=CONSTRUCTION_TIME_YR,
    interest_rate=INTEREST_RATE,
    inflation_rate=INFLATION_RATE,
    noak=NOAK,

    # ── Geometry: ARIES-AT analogue for conventional-aspect-ratio LTS tokamak ─
    # Source: ARIES-AT: R₀ = 5.2 m, a = 1.3 m (A ≈ 4.0), κ = 1.7
    # Rationale: closest published plant study to PFPP lineage physics parameters
    # (B₀ ≈ 5.9 T, conventional aspect ratio, D-T, LTS-primary magnets)
    # UNCERTAIN: Commercial PFPP geometry completely unspecified; B₀ ≈ 6–8 T likely
    R0=5.2,              # Major radius [m]; ARIES-AT analogue; analysis.md §S7
    plasma_t=1.3,        # Minor radius a [m]; A ≈ 4.0; ARIES-AT analogue
    elon=1.7,            # Elongation κ; conventional aspect ratio; ARIES-AT analogue
    blanket_t=0.80,      # Blanket thickness [m]; DEFAULT — PFPP blanket tech undecided
                         # UNCERTAIN: COOL/WCCB/WCLL TBM result will set this; analysis.md §S2
    ht_shield_t=0.30,    # High-T shield [m]; slightly thicker for LTS protection
    structure_t=0.20,    # Primary structure [m]; DEFAULT
    vessel_t=0.20,       # Vacuum vessel [m]; DEFAULT

    # ── Magnet parameters: LTS Nb3Sn TF + NbTi PF (ITER-heritage) ────────────
    # Source: best-research-plan-v1.1-summary.md §Section 1.3
    # B₀ = 6.15 T (BEST); PFPP likely 6–8 T at plasma center
    # Peak TF conductor field: Nb3Sn operational limit ≈ 13–16 T
    b_max=13.0,          # Peak conductor field [T]; Nb3Sn hard limit; analysis.md §S3
    r_coil=3.0,          # Winding bore radius [m]; scaled from R₀ = 5.2 m, A ≈ 4

    # ── Power balance ─────────────────────────────────────────────────────────
    # Heating power: Q~10 commercial PFPP estimate
    # P_fusion ≈ 2200 MWth (for 1 GWe at 34.7% eff, mn=1.1)
    # P_aux = P_fusion / Q ≈ 2200 / 10 ≈ 220 MW → rounded to 200 MW
    # Source: analysis.md §S2 "Q value (commercial PFPP): estimated 5–15"
    # UNCERTAIN: Q value and P_aux completely unanchored for PFPP
    p_input=200.0,       # Auxiliary heating power [MW]; Q~10 analogue; analysis.md §S5

    mn=1.1,              # Neutron energy multiplier; DEFAULT for D-T blanket

    # Thermal efficiency: sCO2 Brayton at 34.7% from CFETR/BEST lineage studies
    # Source: cfetr-power-conversion-studies.md §Conclusions
    # Preferred cycle in published studies; not formally committed for PFPP
    # Literature range: 34.7% (preliminary) to 42.8–53.7% (advanced recompression)
    # UNCERTAIN: sCO2 not formally adopted; blanket coolant choice affects this
    eta_th=0.347,        # Thermal efficiency; analysis.md §S2 Challenge 6, §S5

    # Heating system wall-plug efficiency: weighted average of BEST 4-method portfolio
    # NBI (60–70%) + ECRH (50–55%) + ICRH (70–80%) + LHCD (50–55%)
    # Mix at BEST: 12MW NBI + 15MW ECRH + 10MW ICRH + 10MW LHCD
    # Weighted avg = (12×0.65 + 15×0.52 + 10×0.75 + 10×0.52) / 47 ≈ 0.60
    # UNCERTAIN: Commercial PFPP H&CD portfolio unspecified; LHCD may not penetrate
    # burning plasma (high-T cutoff); analysis.md §S2 Challenge 4
    eta_pin=0.60,        # H&CD wall-plug efficiency; analysis.md §S2 Challenge 4

    eta_p=0.5,           # Pumping efficiency; DEFAULT
    eta_de=0.85,         # DEC efficiency; DEFAULT (no DEC for tokamak, f_dec=0)
    f_sub=0.04,          # Subsystem power fraction; slightly elevated for LTS
                         # support infrastructure; analysis.md §S3 Magnet System
    f_dec=0.0,           # No direct energy conversion for tokamak; DEFAULT

    # Parasitic power consumers
    p_coils=5.0,         # Coil power [MW]; superconducting but quench protection,
                         # switching, bus joints; scaled from ITER experience; DEFAULT+
    p_cool=25.0,         # Cooling systems [MW]; large machine with active W first-wall
                         # cooling (4 MPa water, 240 modules); analysis.md §S3 FW
    p_pump=2.0,          # Pumping power [MW]; scaled for larger machine; DEFAULT+
    p_trit=10.0,         # Tritium processing [MW]; DEFAULT — T fuel cycle at plant scale
    p_house=5.0,         # Housekeeping [MW]; scaled for commercial plant; DEFAULT+

    # Cryogenic system: LTS Nb3Sn/NbTi coils at 4.5 K — significant parasitic load
    # ITER cryoplant: ~36 MW electrical for ~40 kW@4.5K cooling / ~10,000t cold mass
    # PFPP cold mass estimate ~3000t (15% of ITER) → ~6–8 MW electrical equivalent
    # Source: analysis.md §S4 "Helium (Magnet Cooling)"; analysis.md §S2 Challenge 3
    p_cryo=8.0,          # Cryogenic power [MW]; LTS 4.5K; analysis.md §S4

    # ── Plasma parameters ────────────────────────────────────────────────────
    # Burning plasma regime for commercial PFPP (Q~10, T_e~20 keV)
    n_e=1.0e20,          # Electron density [m⁻³]; DEFAULT
    T_e=20.0,            # Electron temperature [keV]; elevated for burning plasma
                         # regime; cf. BEST target Q~5: T_e ~ 15–25 keV; DEFAULT+
    Z_eff=1.5,           # Effective charge; full-W first wall; analysis.md §S3 FW
    plasma_volume=295.0, # Plasma volume [m³]; derived: 2π²R₀a²κ = 2π²×5.2×1.69×1.7
    B=6.5,               # Magnetic field at plasma center [T]; PFPP analogue,
                         # above BEST's 6.15 T; analysis.md §S5
    wall_material="W",   # Full-tungsten FW; analysis.md §S3 FW
    T_edge=0.05,         # Edge temperature [keV]; detached divertor; DEFAULT
    tau_ratio=3.0,       # Impurity confinement / energy confinement; DEFAULT

    # ── Cost overrides: none applied ─────────────────────────────────────────
    # No published capital cost data exists for BEST, CFEDR, or PFPP.
    # The PFPP overnight cost estimate ($5–15B for 500–1000 MWe) in analysis.md §S5
    # is too uncertain to anchor any CAS account.
    #
    # KEY UNMODELED FACTOR — Chinese construction cost discount (analysis.md §S2):
    #   CAS21 (buildings): likely 2–4× lower than Western baseline (labor + supply chain)
    #   This discount is NOT applied here; its fusion-specific magnitude is unknown.
    #   Run a sensitivity: cost_overrides={"CAS21": <base_cas21>/2} for 2× discount.
    #
    # KEY UNMODELED FACTOR — Blanket technology (analysis.md §S2, §S5):
    #   COOL (CO2-cooled LiPb): CAS27 ≈ default $15M (PbLi fill)
    #   WCCB (water-cooled ceramic breeder, Be12Ti multiplier): CAS27 ≈ $200M
    #   Decision awaits BEST TBM experimental results (~2030s)
    #
    # KEY UNMODELED FACTOR — Stewart & Shirvan 2.2× regulatory building cost factor:
    #   The 21-spherical-tokamak-hts analysis applied this as an upper-bound scenario.
    #   May not apply in Chinese regulatory context (analysis.md §S2 Challenge 2).
    #   Upper-bound scenario: cost_overrides={"CAS21": <base_cas21> * 2.2}
)

# ── Forward model ─────────────────────────────────────────────────────────────
# Native design point is 1000 MWe — no result_1gw needed.
result = model.forward(net_electric_mw=NET_ELECTRIC_MW, **_SHARED_KWARGS)

# ── Results printing ──────────────────────────────────────────────────────────
c = result.costs
pt = result.power_table

print("State-Backed Tokamak - BEST → Commercial PFPP Analogue (Neo Fusion / ASIPP)")
print("ARIES-AT geometry | sCO2 Brayton 34.7% | Q~10 | LTS Nb3Sn | NOAK")
print(f"LCOE: {c.lcoe:.1f} $/MWh | Overnight: {c.overnight_cost:.0f} $/kW")
print(f"Fusion: {pt.p_fus:.0f} MW | Net: {pt.p_net:.0f} MW | Q_eng: {pt.q_eng:.2f}")
print()

cas_accounts = [
    ("CAS10", "Preconstruction",            c.cas10),
    ("CAS21", "Buildings",                  c.cas21),
    ("CAS22", "Reactor Plant Equipment",    c.cas22),
    ("CAS23", "Turbine Plant",              c.cas23),
    ("CAS24", "Electrical Plant",           c.cas24),
    ("CAS25", "Miscellaneous",              c.cas25),
    ("CAS26", "Heat Rejection",             c.cas26),
    ("CAS27", "Special Materials",          c.cas27),
    ("CAS28", "Digital Twin",               c.cas28),
    ("CAS29", "Contingency",               c.cas29),
    ("CAS30", "Indirect Costs",             c.cas30),
    ("CAS40", "Owner's Costs",              c.cas40),
    ("CAS50", "Supplementary",              c.cas50),
    ("CAS60", "IDC",                        c.cas60),
    ("CAS70", "O&M (annualized)",           c.cas70),
    ("CAS80", "Fuel (annualized)",          c.cas80),
    ("CAS90", "Financial",                  c.cas90),
]

print(f"{'Code':<8} {'Account':<30} {'M$':>10}")
print("-" * 50)
for code, name, val in cas_accounts:
    print(f"{code:<8} {name:<30} {float(val):>10.1f}")
print("-" * 50)
print(f"{'':8} {'Total Capital':<30} {float(c.total_capital):>10.1f}")

# ── CAS22 breakdown ───────────────────────────────────────────────────────────
print()
print("CAS22 Sub-account Detail:")
for k, v in result.cas22_detail.items():
    print(f"  {k}: {float(v):.1f} M$")

# ── Key assumptions summary ───────────────────────────────────────────────────
print()
print("Key Assumptions (PFPP Commercial Analogue — Very Low Confidence):")
print(f"  Commercial PFPP native power:    {NET_ELECTRIC_MW:.0f} MWe (no published design point)")
print(f"  Geometry analogue:               ARIES-AT (R₀=5.2m, a=1.3m, κ=1.7)")
print(f"  Magnet technology:               LTS Nb3Sn/NbTi TF/PF + YBCO CS sub-coils")
print(f"  Thermal efficiency:              {_SHARED_KWARGS['eta_th']:.3f} (sCO2 Brayton; CFETR study)")
print(f"  Availability:                    {AVAILABILITY:.0%} (Araiinejad & Shirvan 2025 analogue)")
print(f"  Q value implied (commercial):    ~10 (drives p_input = {_SHARED_KWARGS['p_input']:.0f} MW)")
print(f"  H&CD wall-plug efficiency:       {_SHARED_KWARGS['eta_pin']:.2f} (4-method portfolio avg)")
print(f"  Cryogenic load (LTS 4.5K):      {_SHARED_KWARGS['p_cryo']:.1f} MW (ITER-scaled)")
print(f"  Blanket technology:              DEFAULT (PbLi; COOL/WCCB/WCLL undecided)")
print(f"  Chinese construction discount:   NOT APPLIED (unknown magnitude in fusion context)")
print(f"  Regulatory 2.2× factor:          NOT APPLIED (Chinese context uncertain)")
print(f"  NOAK:                            {NOAK}")
print(f"  Construction time:               {CONSTRUCTION_TIME_YR:.0f} yr (UNCERTAIN)")

# ── Sensitivity analysis ──────────────────────────────────────────────────────
sens = model.sensitivity(result.params)

print()
print("Sensitivity (elasticity = %LCOE / %param)")
print("-" * 50)

print("\nEngineering levers:")
for k, v in sorted(sens["engineering"].items(), key=lambda x: abs(x[1]), reverse=True):
    print(f"  {k:<38} {v:+.4f}")

print("\nFinancial:")
for k, v in sorted(sens["financial"].items(), key=lambda x: abs(x[1]), reverse=True):
    print(f"  {k:<38} {v:+.4f}")

print("\nCosting constants (top 15):")
costing = sorted(sens["costing"].items(), key=lambda x: abs(x[1]), reverse=True)
for k, v in costing[:15]:
    print(f"  {k:<38} {v:+.4f}")
