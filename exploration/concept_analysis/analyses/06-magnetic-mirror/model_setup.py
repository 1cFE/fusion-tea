"""Magnetic Mirror (p-B11) — Pale Blue Fusion (CHARM).

Modeling approach:
    Uses the MFE MIRROR / PB11 model as the closest available framework analog for the
    CHARM (Centrifugal Hybrid Axisymmetric Rotating Mirror) concept. The framework's
    p-B11 fuel defaults drive blanket, licensing, tritium, and remote handling costs
    to their near-aneutronic values. Power balance parameters are heavily adjusted to
    reflect (a) the dominance of direct energy conversion over the thermal cycle for
    an aneutronic plasma, and (b) the large recirculating power required to sustain
    plasma rotation.

Concept choice rationale:
    ConfinementConcept.MIRROR captures the cylindrical geometry, solenoid coil cost
    model, and DEC-capable power balance that are structurally correct for CHARM.
    Fuel.PB11 activates the correct near-aneutronic cost scaling: blanket_unit_cost_pb11
    (X-ray capture only), no tritium processing, minimal remote handling, near-zero
    licensing costs.

Key deviations from DT mirror defaults:
    - Near-aneutronic power balance: mn ≈ 1.0, f_dec high (≈0.85), eta_th low (≈0.20)
    - Very high recirculating power: rotation sustainment and RF alpha channeling add
      ~60 MW of auxiliary load (truly unknown — central estimate only)
    - No tritium processing: p_trit = 0.0
    - DEC efficiency raised to 0.70 (speculative based on PRX Energy 2025 physics limits)
    - All key plasma parameters are truly-unknown blocking gaps (see analysis.md §Section 5)
    - This script is a best-estimate placeholder, not a validated design point

WARNING — DATA QUALITY:
    Every quantitative plasma/engineering parameter is truly unknown or based on
    analogous concepts (CMFX, Realta Hammir). The LCOE output is indicative only and
    should not be cited as a Pale Blue Fusion estimate. See analysis.md §Section 5–6
    for the full blocking data gap inventory.

Usage:
    uv run python model_setup.py              # print results to terminal
    uv run python model_setup.py | tee model_output.txt  # also save for synthesis stage
"""

from costingfe import ConfinementConcept, CostModel, Fuel

# ── Model instantiation ────────────────────────────────────────────────────
model = CostModel(concept=ConfinementConcept.MIRROR, fuel=Fuel.PB11)

# ── Plant configuration ────────────────────────────────────────────────────
# Net electric output
# UNCERTAIN: No published design point. No reactor concept study from Pale Blue.
# 500 MWe used as reference scale, consistent with DT mirror example.
# Source: analysis.md §Section 5, "Missing Parameters — Net electric output (plant)"
_NATIVE_MW = 500.0

# ── Shared kwargs (all parameters common to both forward() calls) ──────────
_SHARED_KWARGS = dict(
    # ── Financial / lifecycle ─────────────────────────────────────────────
    availability=0.80,
    # UNCERTAIN: No published capacity factor or maintenance philosophy.
    # Open-ended geometry may enable simpler maintenance than toroids (analysis §S5),
    # but p-B11 plasma conditions have never been sustained — reliability unknown.
    # Using 0.80 (slightly below DT mirror) to reflect greater operational uncertainty.
    lifetime_yr=30,             # Standard reference; no concept-specific data
    n_mod=1,
    construction_time_yr=5.0,  # DEFAULT: mirror geometry simpler than tokamak; mfe_mirror.yaml
    interest_rate=0.07,         # DEFAULT: standard reference
    inflation_rate=0.02,        # DEFAULT: standard reference
    noak=True,

    # ── Mirror geometry (cylindrical) ─────────────────────────────────────
    R0=0.0,                 # No axis offset — cylinder; mfe_mirror.yaml default
    plasma_t=1.5,           # Plasma radius [m]; DEFAULT from mfe_mirror.yaml
                            # UNCERTAIN: No published machine radius for CHARM.
                            # CMFX experiment: small bore, ~0.1-0.2 m radius.
                            # Reactor scale unspecified; 1.5 m is the framework default.
    chamber_length=30.0,    # UNCERTAIN: Multi-chamber CHARM architecture requires a longer
                            # device than a simple mirror. CMFX is 6.7 m; a reactor would
                            # be substantially larger. 30 m is a conservative upscale with no
                            # published basis. Source: analysis.md §S3, §S5 "Machine size
                            # (plasma radius, length): truly-unknown / blocking"
    blanket_t=0.30,         # Very thin "blanket" — X-ray capture wall only.
                            # p-B11 is near-aneutronic (<1% neutron energy fraction);
                            # no neutron breeding blanket needed.
                            # Source: analysis.md §S5 "Neutron energy fraction: <1%"
                            # analysis.md §S4 "No First-Wall Neutron Damage or Activation"
    ht_shield_t=0.10,       # Minimal shielding — no 14.1 MeV neutron flux.
                            # Source: analysis.md §S4; costing_constants.yaml shield_unit_cost
    structure_t=0.15,       # DEFAULT: mfe_mirror.yaml
    vessel_t=0.10,          # DEFAULT: mfe_mirror.yaml

    # ── p-B11 aneutronic power balance ────────────────────────────────────
    p_input=60.0,           # UNCERTAIN: Total auxiliary power [MW].
                            # Includes: RF for alpha channeling (~20 MW est.), rotation
                            # sustainment via biased electrode (~30 MW est.), misc RF (~10 MW).
                            # Rotation sustainment power is a key blocking unknown.
                            # Source: analysis.md §S2 Challenge 4 "Unknown Recirculating Power"
                            # Electrode voltage up to 100 kV @ CMFX: technical-papers-summary.md §CMFX
    mn=1.0,                 # Neutron energy multiplier.
                            # p-B11 is near-aneutronic: <1% of fusion energy in neutrons.
                            # Blanket neutron multiplication is negligible — set to 1.0.
                            # Source: analysis.md §S5 "Neutron energy fraction: <1%"
                            # arpa-e-fisch-2025-presentation.md §Why p-B11?
    eta_th=0.20,            # Thermal conversion efficiency.
                            # Very low — only synchrotron radiation and bremsstrahlung losses
                            # are captured thermally; the dominant energy channel is DEC.
                            # 0.20 is speculative; reflects that only ~15-25% of fusion power
                            # is expected to appear as thermal (radiation) rather than DEC.
                            # UNCERTAIN: No power balance numbers published.
                            # Source: analysis.md §S2 Challenge 5; §S5 "Thermal vs. direct
                            # conversion energy split: truly-unknown / important"
    eta_p=0.5,              # Pumping efficiency; DEFAULT: mfe_mirror.yaml
    eta_pin=0.60,           # Heating wall-plug efficiency.
                            # UNCERTAIN: Covers RF system (alpha channeling antennas) and
                            # biased electrode power supply efficiency. ICRF systems
                            # typically 50-70% wall-plug efficiency. Central estimate 60%.
                            # Source: analysis.md §S3 "RF Heating / Wave Launch: TRL 4-5 (generic)"
    eta_de=0.70,            # DEC efficiency for rotation energy recovery.
                            # UNCERTAIN — this is a speculative estimate.
                            # Rax, Kolmes, Fisch (PRX Energy 4, 013007, 2025) establishes
                            # physics efficiency upper bounds for adiabatic DEC in axisymmetric
                            # fields; no engineering efficiency or hardware design published.
                            # 0.70 is within range of physics limits but not validated.
                            # Historical MARS gridless DEC measured ~54% (1983 MARS study);
                            # eta_de=0.70 is above this empirical reference. See analysis.md §S7.
                            # Source: analysis.md §S2 Challenge 5; §S3 "DEC: TRL 2-3"
                            # technical-papers-summary.md §Related: Direct Energy Conversion
    f_sub=0.03,             # BOP subsystem fraction; DEFAULT: mfe_mirror.yaml
    f_dec=0.85,             # Fraction of transport power going to DEC.
                            # UNCERTAIN: Near-aneutronic p-B11 puts ~99% of fusion energy
                            # in charged alpha particles. A large fraction is available for
                            # direct conversion. 0.85 is an optimistic estimate reflecting
                            # that rotation DEC captures most charged-particle power, with
                            # ~15% captured as radiation (synchrotron + bremsstrahlung → thermal).
                            # Source: analysis.md §S5 "Thermal vs. direct conversion energy split:
                            # truly-unknown / important"; §S2 Challenge 1 (bremsstrahlung losses)
    p_coils=8.0,            # Superconducting solenoid coil power [MW].
                            # UNCERTAIN: Slightly above DT mirror default (5 MW) to account
                            # for multi-chamber geometry with inner and outer coil sets visible
                            # in ARPA-E slide schematic. Conductor type not specified by Pale Blue.
                            # Source: analysis.md §S3 "Magnet System: TRL Indeterminate"
                            # arpa-e-2025-fisch-presentation-notes.md §Device Details
    p_cool=15.0,            # Cooling power [MW].
                            # Reduced vs DT mirror (20 MW default): no tritium cooling loop,
                            # no high-neutron-flux first wall active cooling required.
                            # Source: analysis.md §S4 "No First-Wall Neutron Damage or Activation"
    p_pump=1.5,             # Pumping power [MW]; DEFAULT: mfe_mirror.yaml
    p_trit=0.0,             # Tritium processing power [MW].
                            # Zero — p-B11 is aneutronic; no tritium is produced or consumed.
                            # Source: arpa-e-fisch-2025-presentation.md §Why p-B11?
                            # analysis.md §S4 "No Tritium, No Lithium, No Breeding Blanket"
    p_house=5.0,            # Housekeeping [MW]; slight increase for electrode power supplies
                            # and multi-chamber monitoring systems. UNCERTAIN.
    p_cryo=2.0,             # Cryogenic power [MW].
                            # Slightly above default: multi-chamber solenoid array likely
                            # requires more cryogenic infrastructure than a simple tandem mirror.
                            # Source: analysis.md §S3 "Magnet System: TRL Indeterminate"

    # ── Cost overrides ────────────────────────────────────────────────────
    # No fuel-cycle cost overrides needed: Fuel.PB11 activates correct framework defaults:
    #   blanket_unit_cost_pb11 = 0.05 M$/m³ (X-ray only — costing_constants.yaml)
    #   fuel_handling_pb11_base = 15.0 M$ (boron powder injection — costing_constants.yaml)
    #   remote_handling_pb11_base = 20.0 M$ (conventional maintenance — costing_constants.yaml)
    #   licensing_cost_pb11 = 0.1 M$, licensing_time_pb11 = 0.0 yr (costing_constants.yaml)
    #   om_cost_pb11 = 24.0 M$/yr (aneutronic, RSO-only — costing_constants.yaml)
    #   decom_provision_pb11 = 53.0 M$ at 1 GWe (costing_constants.yaml)
    #
    # Buildings: applying a modest reduction vs DT to reflect absence of hot cell,
    # tritium building, and large remote handling facility. Using 200 M$ (vs DT default
    # of ~250-300 M$). UNCERTAIN — no plant design study available.
    # Source: analysis.md §S4; costing_constants.yaml §building_costs_per_kw
    cost_overrides={"CAS21": 200.0},
)

# ── Forward model — native design point ───────────────────────────────────
result = model.forward(net_electric_mw=_NATIVE_MW, **_SHARED_KWARGS)

# ── Forward model — 1 GWe comparison point ────────────────────────────────
# Scales cost_overrides from the 500 MWe native point to 1000 MWe using
# per-account scaling laws. Preserves physics consistency at the native point.
result_1gw = model.forward(
    net_electric_mw=1000.0,
    override_reference_mw=_NATIVE_MW,
    **_SHARED_KWARGS,
)

# ── Results ────────────────────────────────────────────────────────────────
c = result.costs
pt = result.power_table

print("Magnetic Mirror (p-B11) — Pale Blue Fusion (CHARM)")
print("500 MWe target | 80% availability | 30 yr lifetime | NOAK")
print("WARNING: All plasma parameters are truly-unknown estimates (see analysis.md §5-6)")
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

# ── Cost breakdown ─────────────────────────────────────────────────────────
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

# ── CAS22 sub-account detail ───────────────────────────────────────────────
print("\nCAS22 Reactor Plant Equipment Breakdown:")
print("-" * 48)
for k, v in sorted(result.cas22_detail.items()):
    if float(v) > 0:
        print(f"  {k:<28} {float(v):>10.1f} M$")

# ── Key Assumptions ───────────────────────────────────────────────────────
print("\nKey Assumptions (all UNCERTAIN — no published design point):")
print("-" * 48)
print("  p-B11 near-aneutronic power balance:   mn=1.0, f_dec=0.85, eta_th=0.20")
print("  DEC efficiency:                         eta_de=0.70  [physics limit per PRX Energy 2025]")
print("  Total auxiliary power:                  p_input=60 MW  [rotation + RF alpha channeling]")
print("  No tritium processing:                  p_trit=0.0")
print("  Machine geometry:                       plasma_t=1.5 m, chamber_length=30 m [no design point]")
print("  Net electric target:                    500 MWe  [framework reference scale]")
print("  Availability:                           80%  [no maintenance study]")
print()
print("Blocking gaps (from analysis.md §Section 6):")
print("  - No published plant design or engineering parameters of any kind")
print("  - Alpha channeling efficiency η_α: analytical only, never measured experimentally")
print("  - Rotation sustainment power (recirculating fraction): not characterized")
print("  - DEC efficiency for rotation energy recovery: physics bounds only")
print("  - p-B11 nonthermal plasma never demonstrated in any experiment")
print("  - CHARM multi-chamber architecture never tested")

# ── Sensitivity Analysis ──────────────────────────────────────────────────
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
