"""
Laser ICF — Liquid Jet Target (D-D) — First-Pass LCOE Model
=============================================================
1cFE First Pass Concept Analysis
Concept: Plasmonic Nanoshell IFE — Femtosecond Laser on D₂O-filled Gold Nanoshells
Company: Cortex Fusion Systems (New York, NY — founded 2021, $2.6M funding)

CRITICAL CAVEAT: This model is a speculative corridor map only. Cortex Fusion
Systems has published zero experimental fusion results. The concept rests entirely
on a theoretical preprint (arXiv:2503.15531, unreviewed as of this analysis) that
projects Q~100 from an undemonstrated plasmonic field-enhancement mechanism. The
paper explicitly acknowledges the fundamental barrier: deuteron fusion mean free
path λ_f ~ cm vs. nanoshell radius ~ 100 nm, meaning nearly all deuterons pass
through without fusing. Every BLOCKING unknown below is a structural absence in
the public record, not a measurement uncertainty.

This script answers "what would LCOE be IF the physics and engineering worked at
commercial scale" — it is NOT a projection or endorsement of feasibility.

Framework mapping: LASER_IFE concept (ConfinementConcept.LASER_IFE), DD fuel.
This is an imperfect fit — the Cortex concept is a non-implosion variant. It relies
on direct in-situ deuteron acceleration inside gold nanoshells rather than hot-spot
compression. LASER_IFE is the closest available 1cFE archetype. Sub-accounts for
hohlraum and cryogenic target fabrication are NOT applicable and are zeroed.

Key deviations from standard laser IFE (e.g., NIF, IFX):
  - No high-energy DPSSL or KrF driver: femtosecond laser at modest average power
  - No hohlraum, no cryogenic D-T pellet: D₂O liquid jet + suspended gold nanoshells
  - Q~100 projected (NIF achieved Q~1.5 at ignition after decades of development)
  - No magnetic confinement, no breeding blanket (D-D fuel)
  - Energy capture architecture: COMPLETELY UNSPECIFIED — eta_th is a placeholder
  - No superconducting or resistive magnets anywhere in the system

Critical unresolved gaps (analysis.md §Section 6):
  [BLOCKING] Energy capture architecture — not described anywhere in Cortex sources
  [BLOCKING] Experimental validation of plasmonic D-D fusion — zero published results
  [BLOCKING] Mean free path problem — λ_f ~ cm vs. nanoshell radius ~ 100 nm; paper
             acknowledges but does not resolve: nearly all deuterons escape unfused
  [BLOCKING] Gold nanoshell delivery and recovery at MHz rates
  [BLOCKING] Capital cost — no plant design or cost estimate of any kind published
  [BLOCKING] Capacity factor — no maintenance model, no operational experience

Usage:
    uv run python model_setup.py              # print results to terminal
    uv run python model_setup.py | tee model_output.txt  # also save for synthesis stage
"""

from costingfe import ConfinementConcept, CostModel, Fuel

# ── Model instantiation ──────────────────────────────────────────────────────
model = CostModel(concept=ConfinementConcept.LASER_IFE, fuel=Fuel.DD)

# ═══════════════════════════════════════════════════════════════════════════════
# PLANT CONFIGURATION CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════

# ── Scale and economics ───────────────────────────────────────────────────────

NET_ELECTRIC_MW = 1000.0
# Target net electric output [MW] — standard CAS reference scale for account
# comparability across concepts in this study.
# analysis.md §Section 5: paper projects ~1 MW fusion from a 3 kW laser input at Q~100.
# UNCERTAIN: Commercial plant would require aggregating many modules or scaling the
# concept — neither is disclosed. 1 GWe used solely as framework reference, NOT as
# a validated capacity target.

AVAILABILITY = 0.40
# UNCERTAIN (BLOCKING): Capacity factor [fraction].
# analysis.md §Section 5 Missing Params: "truly-unknown, blocking — no operational
# experience, no maintenance model."
# 0.40 is a pessimistic proxy consistent with TRL 1 physics basis and complete
# absence of engineering validation. Standard mature IFE projections: 0.85–0.90.

LIFETIME_YR = 30
# Plant economic lifetime [yr].
# DEFAULT: 1costingfe costing framework convention; no Cortex-specific information.

CONSTRUCTION_TIME_YR = 5.0
# DEFAULT: ife_laser_ife.yaml construction_time_yr = 5.0.
# Comment in YAML: "No magnets, simpler." Applicable here — Cortex has no magnet
# infrastructure, though the novel nanoshell supply chain may offset.


# ── Power balance ─────────────────────────────────────────────────────────────
# Derived from: Q~100 projection (arXiv:2503.15531), eta_th=0.35, eta_pin=0.10.
# To deliver 1 GWe net at these efficiencies, rough steady-state balance:
#   p_fus ≈ NET_ELECTRIC / (eta_th - 1/Q/eta_pin) ≈ 1000 / (0.35 - 0.10) ≈ 4000 MW
#   p_implosion (laser output) = p_fus / Q_plasma ≈ 4000 / 100 ≈ 40 MW
#   Q_eng = p_gross / p_recirc_elec = (4000×0.35) / (40/0.10) = 1400/400 ≈ 3.5
# All intermediate values UNCERTAIN — power balance is a framework-level estimate.

P_IMPLOSION_MW = 40.0
# UNCERTAIN: Aggregate femtosecond laser output power [MW] at 1 GWe scale.
# analysis.md §Section 5: "Laser input power at Q~100: ~3 kW" for ~1 MW fusion.
# Scaled to plant: 40 MW laser output → ~4 GW fusion → ~1 GWe gross at eta_th=0.35.
# This is a rough order-of-magnitude scale; actual scaling path is undemonstrated.

P_IGNITION_MW = 0.0
# No separate ignition pulse in the Cortex architecture — single femtosecond OAM
# beam serves as both driver and igniter (plasmonic in-situ mechanism).
# ife_laser_ife.yaml default: 0.1 MW — overridden to 0.


ETA_P = 0.5
# DEFAULT: Pumping efficiency. ife_laser_ife.yaml.


MN = 1.05
# UNCERTAIN: Neutron energy multiplier (blanket energy multiplication factor).
# D-D produces 2.45 MeV neutrons — lower than D-T 14.1 MeV; no breeding blanket
# architecture disclosed. Using 1.05 (negligible multiplication) as lower bound.
# ife_laser_ife.yaml default: 1.1 — reduced here for absent blanket design.
# analysis.md §Section 2, Challenge 4: neutron management "completely unaddressed."

F_SUB = 0.03
# DEFAULT: Subsystem power fraction. ife_laser_ife.yaml.

P_PUMP = 1.0
# DEFAULT: Pumping power [MW]. ife_laser_ife.yaml.

P_HOUSE = 4.0
# DEFAULT: Housekeeping power [MW]. ife_laser_ife.yaml.

P_CRYO = 0.0
# No cryogenic systems required. D-D fuel cycle — no superconducting magnets,
# no cryogenic target preparation (D₂O liquid jet at ambient or near-ambient temperature).
# ife_laser_ife.yaml default: 0.5 — zeroed here.
# analysis.md §Section 3: "No magnets... no cryogenics."

P_TRIT = 0.0
# No tritium processing plant required for D-D fuel cycle.
# analysis.md §Section 4, Heavy Water: "No tritium supply or breeding required —
# eliminating the most critical supply chain constraint in D-T concepts."
# ife_laser_ife.yaml default: 10.0 — zeroed here.

P_TARGET = 2.0
# UNCERTAIN: Nanoshell + liquid jet target factory power [MW].
# ife_laser_ife.yaml default: 1.0 — doubled to 2.0 to reflect unknowns in
# gold nanoshell synthesis at industrial scale and MHz-rate liquid jet operation.
# analysis.md §Section 4, Gold for Nanoshells: "Gold nanoshell synthesis at
# industrial scale is not characterized in any Cortex source." Key cost risk:
# if nanoshells are not recycled, gold consumption ≈ 60 mg/s at 1 MHz → ~$18,000/hr at $85k/kg.
# ASSUMES near-complete nanoshell recycling — entirely undemonstrated.

# ── Radial build (spherical chamber geometry) ─────────────────────────────────
# No Cortex chamber design has been disclosed.
# Using IFE framework defaults as geometry placeholders — these drive volume-based
# CAS22 accounts (blanket, shield, structure, vessel). All are DEFAULT.

PLASMA_T    = 4.0   # DEFAULT: Spherical chamber radius [m]. ife_laser_ife.yaml.
BLANKET_T   = 0.80  # DEFAULT: Blanket thickness [m]. ife_laser_ife.yaml.
                     # NOTE: No blanket architecture disclosed. analysis.md §S2, §S3.
HT_SHIELD_T = 0.25  # DEFAULT: High-temperature shield [m]. ife_laser_ife.yaml.
STRUCTURE_T = 0.15  # DEFAULT: Primary structure [m]. ife_laser_ife.yaml.
VESSEL_T    = 0.10  # DEFAULT: Vacuum vessel [m]. ife_laser_ife.yaml.

# ═══════════════════════════════════════════════════════════════════════════════
# COST OVERRIDES
# ═══════════════════════════════════════════════════════════════════════════════
# Only accounts with clear justification from analysis.md are overridden.
# All other CAS accounts use framework defaults — see §Anti-Hallucination above.

COST_OVERRIDES = {
    # C220103 — Coils/magnets: $0
    # No superconducting or resistive magnets in the Cortex concept.
    # Laser IFE inherits no coil requirement; zeroed to prevent any MFE heritage bleed.
    # analysis.md §Section 7: "No external magnets... Cortex's cost structure would
    # be fundamentally different from MFE concepts."
    "C220103": 0.0,

    # C220108 — Divertor: $0
    # No divertor architecture exists or is applicable to an IFE pulsed concept.
    # IFE concepts do not have steady-state plasma exhaust requiring a divertor.
    # Zeroed to avoid MFE/tokamak default values carrying through.
    "C220108": 0.0,

    # C220112 — Isotope separation: $0
    # No Li-6 enrichment or tritium isotope separation required for D-D fuel cycle.
    # analysis.md §Section 4, Heavy Water: D₂O is the fuel medium; commercially
    # available from CANDU operations at ~$300–600/kg. No isotope separation plant needed.
    "C220112": 0.0,
}

# ═══════════════════════════════════════════════════════════════════════════════
# FORWARD MODEL
# ═══════════════════════════════════════════════════════════════════════════════

result = model.forward(
    # Customer requirements
    net_electric_mw=NET_ELECTRIC_MW,
    availability=AVAILABILITY,
    lifetime_yr=LIFETIME_YR,
    n_mod=1,
    # Financial
    construction_time_yr=CONSTRUCTION_TIME_YR,
    # Power balance
    p_implosion=P_IMPLOSION_MW,
    p_ignition=P_IGNITION_MW,
    mn=MN,
    eta_p=ETA_P,
    f_sub=F_SUB,
    p_pump=P_PUMP,
    p_trit=P_TRIT,
    p_house=P_HOUSE,
    p_cryo=P_CRYO,
    p_target=P_TARGET,
    # Radial build (spherical chamber)
    plasma_t=PLASMA_T,
    blanket_t=BLANKET_T,
    ht_shield_t=HT_SHIELD_T,
    structure_t=STRUCTURE_T,
    vessel_t=VESSEL_T,
    # Cost overrides (see rationale block above)
    cost_overrides=COST_OVERRIDES,
)

# ═══════════════════════════════════════════════════════════════════════════════
# RESULTS
# ═══════════════════════════════════════════════════════════════════════════════

c  = result.costs
pt = result.power_table

print("=" * 65)
print("Laser ICF — Liquid Jet Target, D-D (Cortex Fusion Systems)")
print("SPECULATIVE CORRIDOR MODEL — TRL 1 physics, framework defaults")
print("=" * 65)
print(f"LCOE:          {c.lcoe:.1f} $/MWh")
print(f"Overnight:     {c.overnight_cost:.0f} $/kW")
print(f"Fusion power:  {pt.p_fus:.0f} MW")
print(f"Gross elec:    {pt.p_et:.0f} MW")
print(f"Net elec:      {pt.p_net:.0f} MW")
print(f"Thermal power: {pt.p_th:.0f} MW")
print(f"Recirc frac:   {pt.rec_frac:.3f}")
print(f"Q_eng:         {pt.q_eng:.2f}")
print(f"Q_sci:         {pt.q_sci:.2f}")
print()

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

# CAS22 sub-account detail
print()
print("CAS22 Sub-Account Detail:")
print("-" * 48)
for k, v in result.cas22_detail.items():
    print(f"  {k:<12} {float(v):>10.1f}  M$")

if result.overridden:
    print()
    print(f"Overridden accounts (zeroed): {', '.join(result.overridden)}")

# ═══════════════════════════════════════════════════════════════════════════════
# KEY ASSUMPTIONS SUMMARY
# ═══════════════════════════════════════════════════════════════════════════════

print()
print("=" * 65)
print("KEY ASSUMPTIONS AND UNCERTAINTY FLAGS")
print("=" * 65)

assumptions = [
    # (parameter, value, flag, note)
    ("Availability",
     f"{AVAILABILITY:.2f}",
     "BLOCKING UNCERTAIN",
     "No operational data, no maintenance model; TRL 1 physics basis."),
    ("Q-factor (plasma)",
     "~100 (paper claim)",
     "SPECULATIVE / UNVALIDATED",
     "arXiv:2503.15531 — Q~100 theoretical; λ_f ~ cm >> nanoshell radius ~ 100 nm."),
    ("p_implosion (fs laser MW)",
     f"{P_IMPLOSION_MW:.0f}",
     "UNCERTAIN",
     "Scaled from 3 kW @ 1 MW fusion (Q=100) to 1 GWe. Very rough approximation."),
    ("Gold nanoshell recycling",
     "Assumed 100%",
     "BLOCKING UNCERTAIN",
     "If not recycled: ~60 mg/s gold consumed → ~$18,000/hr at $85k/kg market price."),
    ("Chamber geometry",
     "IFE YAML defaults",
     "DEFAULT / PLACEHOLDER",
     "No Cortex chamber design. Drives volume-based CAS22 accounts."),
    ("Target factory (CAS22)",
     f"{P_TARGET:.1f} MW power",
     "UNCERTAIN",
     "Nanoshell synthesis ≠ cryogenic DT targets; cost analogy is rough."),
    ("CAS22 coils (C220103)",
     "$0.0 M",
     "ZEROED",
     "No magnets of any kind in Cortex concept."),
    ("p_trit / p_cryo",
     "0 MW / 0 MW",
     "CORRECT for D-D",
     "No tritium processing, no cryogenic systems."),
    ("Net electric (scale)",
     f"{NET_ELECTRIC_MW:.0f} MW",
     "REFERENCE ONLY",
     "CAS scaling reference; not a validated commercial target for this concept."),
    ("FOAK contingency",
     "10%",
     "APPLIED",
     "TRL 1 concept with no experimental basis justifies maximum contingency."),
]

print(f"  {'Parameter':<30} {'Value':<18} {'Flag':<24} {'Note'}")
print("  " + "-" * 100)
for param, val, flag, note in assumptions:
    print(f"  {param:<30} {val:<18} {flag:<24} {note}")

# ═══════════════════════════════════════════════════════════════════════════════
# SENSITIVITY ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════

print()
print("=" * 65)
print("SENSITIVITY ANALYSIS (elasticity = %ΔLCOE / %Δparam)")
print("Note: overridden accounts (C220103, C220108, C220112) have zero gradient.")
print("=" * 65)

sens = model.sensitivity(result.params, cost_overrides=COST_OVERRIDES)

print("\nEngineering levers:")
for k, v in sorted(sens["engineering"].items(), key=lambda x: abs(x[1]), reverse=True):
    print(f"  {k:<28} {v:+.4f}")

print("\nFinancial:")
for k, v in sorted(sens["financial"].items(), key=lambda x: abs(x[1]), reverse=True):
    print(f"  {k:<28} {v:+.4f}")
