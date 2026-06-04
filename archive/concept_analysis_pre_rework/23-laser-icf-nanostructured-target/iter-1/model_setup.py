"""Laser ICF — Nanostructured Target (p-B11): 1costingfe model setup.

Modeling approach:
    Marvel Fusion design point (100 MW pilot, 2033 EU CORDIS target). Physics
    is entirely undemonstrated at gain-relevant scales; q_eng is the primary
    free parameter — treat all LCOE outputs as contingent on ignition. Primary
    result uses conservative 40% thermal efficiency (steam Rankine path) rather
    than Marvel's unvalidated 70% hybrid claim. HB11 Energy (1 Hz, steam,
    ~1 GW) included as a comparison scenario.

Concept choice rationale:
    LASER_IFE / PB11: aneutronic (>99% energy in charged alphas), room-
    temperature silicon nanowire targets, no tritium breeding, no heavy
    shielding, no superconducting magnets. Framework PB11 fuel defaults
    correctly reflect reduced blanket/shield/remote handling vs D-T baseline.

Key deviations from framework defaults:
    - eta_pin=0.10 (HB11 stated WPE target; Marvel unpublished; UNCERTAIN)
    - eta_th=0.40 (conservative steam; Marvel hybrid 70% is unvalidated)
    - q_eng=5.0 (UNCERTAIN: physics not demonstrated; 4 OOM gap for HB11)
    - availability=0.75 (no pulsed laser IFE plant operational analogue)
    - mn=1.0 (aneutronic: no neutron energy multiplication)
    - p_trit=0.0, p_cryo=0.0 (no tritium, no superconducting magnets)
    - blanket_t=0.20, ht_shield_t=0.10 (minimal: no breeding or heavy shielding)

Usage:
    uv run python model_setup.py              # print results to terminal
    uv run python model_setup.py | tee model_output.txt  # also save for synthesis stage
"""

from costingfe import ConfinementConcept, CostModel, Fuel

# ── Model ─────────────────────────────────────────────────────────────
model = CostModel(concept=ConfinementConcept.LASER_IFE, fuel=Fuel.PB11)

# ── Plant Configuration Constants ─────────────────────────────────────

# Native design point: Marvel Fusion pilot plant
# Source: marvel-fusion-2025-updates.md §Objective; EU CORDIS Project ID 101189082
NATIVE_MW = 100.0

# UNCERTAIN: Engineering gain — physics undemonstrated at any scale.
# HB11 experimental: ~0.005% laser-to-alpha efficiency (~4 OOM from Q_eng>1).
# Marvel has published no yield data from any facility.
# Source: newatlas-energy-hb11-laser-fusion-demonstration.md; analysis.md §S1, §S2
# Value below assumes physics eventually works; do not treat as validated.
Q_ENG = 5.0

# Repetition rate: Marvel commercial target, confirmed by ATLAS facility design
# Source: analysis.md §5; optics-news-16-4-4.md; optics-news-15-10-4.md
F_REP_MARVEL = 10.0  # Hz

# UNCERTAIN: Laser wall-plug efficiency
# HB11 stated target: ~10% vs <1% for conventional high-power lasers.
# Marvel has not characterized WPE in any public source.
# 10% at 10 Hz with petawatt-class pulses is undemonstrated.
# Source: energynewsbulletin-energy-transition-features-articles.md; analysis.md §S2 Challenge 2
ETA_PIN = 0.10

# UNCERTAIN: Thermal-to-electric efficiency — conservative (steam Rankine path)
# Marvel claims hybrid magnetic + electrostatic + steam "up to ~70%" — marketing
# claim, no engineering detail, no demonstrated analogue (TRL 2).
# HB11 explicitly pivoted to steam cycle (~35-40%) as direct conversion not yet
# tractable at scale. Using 0.40 as conservative primary estimate.
# Source: dossier.md §Energy Capture; analysis.md §S2 Challenge 3; hb11-energy-technology.md
ETA_TH_CONSERVATIVE = 0.40

# UNCERTAIN: Plant availability — no pulsed laser IFE plant operational analogue.
# Lower than D-T baseline (0.85) given higher TRL uncertainty on all subsystems.
# Source: analysis.md §5 Missing Parameters
AVAILABILITY_MARVEL = 0.75

# ── Shared kwargs (Marvel design point) ───────────────────────────────
_SHARED_KWARGS = dict(
    availability=AVAILABILITY_MARVEL,  # UNCERTAIN; analysis.md §5 Missing Parameters
    lifetime_yr=30,                    # DEFAULT: standard 30-yr project life
    construction_time_yr=5.0,          # No large magnets; pulsed_laser_ife.yaml default
    interest_rate=0.07,                # DEFAULT: standard WACC
    inflation_rate=0.0245,             # DEFAULT: US CPI baseline
    noak=True,
    # ── Power balance ──────────────────────────────────────────────────
    q_eng=Q_ENG,                       # UNCERTAIN; see constant above
    f_rep=F_REP_MARVEL,                # 10 Hz; analysis.md §5; optics-news-16-4-4.md
    eta_pin=ETA_PIN,                   # UNCERTAIN; analysis.md §5
    eta_th=ETA_TH_CONSERVATIVE,        # UNCERTAIN; conservative steam estimate
    mn=1.0,                            # Aneutronic: no neutron multiplication
                                       # Source: dossier.md §Neutron Management; analysis.md §4
    f_sub=0.03,                        # DEFAULT: subsystem power fraction
    p_pump=1.0,                        # DEFAULT
    p_trit=0.0,                        # No tritium processing; p-B11 aneutronic
                                       # Source: analysis.md §4 (no tritium in fuel cycle)
    p_house=4.0,                       # DEFAULT
    p_cryo=0.0,                        # No superconducting magnets
                                       # Source: analysis.md §4 (no external confinement)
    p_target=2.0,                      # Elevated vs default: 10 Hz target factory power load
                                       # UNCERTAIN: no published data; conservative estimate
    # ── Chamber geometry (spherical) ───────────────────────────────────
    plasma_t=3.5,                      # DEFAULT: spherical chamber radius ~3.5 m
    blanket_t=0.20,                    # Minimal: no breeding blanket (aneutronic)
                                       # Source: analysis.md §4; dossier.md §Neutron Management
    ht_shield_t=0.10,                  # Minimal: no heavy neutron shielding
                                       # Source: hb11-2025-08-04-assoc-prof-patrick-burr.md
    structure_t=0.15,                  # DEFAULT: conventional steel (aneutronic environment)
    vessel_t=0.10,                     # DEFAULT
    # No cost_overrides: no published cost data exists for either company.
    # analysis.md §5: "Capital cost by subsystem — proprietary, blocking"
    # Framework pb11 fuel defaults handle reduced blanket/shield/remote handling.
)

# ── Primary result: Marvel pilot at native 100 MWe ────────────────────
result = model.forward(net_electric_mw=NATIVE_MW, **_SHARED_KWARGS)

# ── 1 GW result: scale from 100 MWe reference ─────────────────────────
# No cost_overrides supplied at 100 MWe, so override_reference_mw enables
# per-account power-law scaling from native to 1 GWe.
result_1gw = model.forward(
    net_electric_mw=1000.0,
    override_reference_mw=NATIVE_MW,
    **_SHARED_KWARGS,
)

# ── Comparison: HB11 Energy design point (steam, 1 Hz, ~1 GW) ─────────
# More defensible design: validated fusion (single-shot), steam cycle,
# conventional steel. Still assumes physics gap is closed.
# Source: hb11-energy-technology.md; analysis.md §S7
result_hb11 = model.forward(
    net_electric_mw=1000.0,           # HB11 targets ~1 GW baseload; analysis.md §5
    availability=0.80,                 # UNCERTAIN; 1 Hz simpler maintenance than 10 Hz
    lifetime_yr=30,
    construction_time_yr=5.0,
    interest_rate=0.07,
    inflation_rate=0.0245,
    noak=True,
    q_eng=4.0,                        # UNCERTAIN; slightly lower Q for lower-rep design
    f_rep=1.0,                        # HB11 rep rate; hb11-energy-technology.md; analysis.md §5
    eta_pin=0.10,                     # UNCERTAIN; HB11 stated target
    eta_th=0.38,                      # Steam Rankine; HB11 explicit choice; analysis.md §S2 Ch.3
    mn=1.0,
    f_sub=0.03,
    p_pump=1.0,
    p_trit=0.0,
    p_house=4.0,
    p_cryo=0.0,
    p_target=1.0,                     # 1 Hz: ~86k targets/day vs Marvel's 864k/day
    plasma_t=3.5,
    blanket_t=0.20,
    ht_shield_t=0.10,
    structure_t=0.15,
    vessel_t=0.10,
)

# ── Results ────────────────────────────────────────────────────────────
c = result.costs
pt = result.power_table
c1 = result_1gw.costs
pt1 = result_1gw.power_table
c_hb11 = result_hb11.costs
pt_hb11 = result_hb11.power_table

print("=" * 72)
print("Laser ICF — Nanostructured Target (p-B11)")
print("** ALL LCOE VALUES CONTINGENT ON UNDEMONSTRATED IGNITION PHYSICS **")
print("=" * 72)

print(f"\n── Marvel Pilot (100 MWe, 10 Hz, eta_th=40%, eta_pin=10%) ──")
print(f"LCOE:      {c.lcoe:.1f} $/MWh   |  Overnight: {c.overnight_cost:.0f} $/kW")
print(f"Fusion:    {pt.p_fus:.0f} MW     |  Net: {pt.p_net:.0f} MW   |  Q_eng: {pt.q_eng:.1f}")
print(f"Q_sci:     {pt.q_sci:.1f}         |  Recirc frac: {pt.rec_frac:.2%}")

print(f"\n── Marvel Scaled to 1 GWe (from 100 MWe reference, per-account scaling) ──")
print(f"LCOE:      {c1.lcoe:.1f} $/MWh  |  Overnight: {c1.overnight_cost:.0f} $/kW")
print(f"Fusion:    {pt1.p_fus:.0f} MW   |  Net: {pt1.p_net:.0f} MW   |  Q_eng: {pt1.q_eng:.1f}")

print(f"\n── HB11 Energy (1 GWe, 1 Hz, steam cycle, eta_th=38%) ──")
print(f"LCOE:      {c_hb11.lcoe:.1f} $/MWh  |  Overnight: {c_hb11.overnight_cost:.0f} $/kW")
print(f"Fusion:    {pt_hb11.p_fus:.0f} MW   |  Net: {pt_hb11.p_net:.0f} MW   |  Q_eng: {pt_hb11.q_eng:.1f}")

# ── CAS Breakdown ──────────────────────────────────────────────────────
print("\n── CAS Breakdown: Marvel 100 MWe pilot ──")
cas = [
    ("CAS10", "Preconstruction",          c.cas10),
    ("CAS21", "Buildings",                c.cas21),
    ("CAS22", "Reactor Plant Equipment",  c.cas22),
    ("CAS23", "Turbine Plant",            c.cas23),
    ("CAS24", "Electrical Plant",         c.cas24),
    ("CAS25", "Miscellaneous",            c.cas25),
    ("CAS26", "Heat Rejection",           c.cas26),
    ("CAS27", "Special Materials",        c.cas27),
    ("CAS28", "Digital Twin",             c.cas28),
    ("CAS29", "Contingency",              c.cas29),
    ("CAS30", "Indirect Costs",           c.cas30),
    ("CAS40", "Owner's Costs",            c.cas40),
    ("CAS50", "Supplementary",            c.cas50),
    ("CAS60", "IDC",                      c.cas60),
    ("CAS70", "O&M (annualized)",         c.cas70),
    ("CAS80", "Fuel (annualized)",        c.cas80),
    ("CAS90", "Financial",                c.cas90),
]

print(f"\n{'Code':<8} {'Account':<28} {'M$':>10}")
print("-" * 48)
for code, name, val in cas:
    print(f"{code:<8} {name:<28} {float(val):>10.1f}")
print("-" * 48)
print(f"{'':8} {'Total Capital':<28} {float(c.total_capital):>10.1f}")

# ── CAS22 Detail ──────────────────────────────────────────────────────
print("\n── CAS22 Sub-accounts (Marvel 100 MWe) ──")
for key, val in result.cas22_detail.items():
    if float(val) > 0:
        print(f"  {key}: {float(val):.1f} M$")

# ── Key Assumptions ───────────────────────────────────────────────────
print("""
── Key Assumptions / Data Quality ──────────────────────────────────────
CRITICAL UNCERTAIN — physics not demonstrated:
  q_eng = 5.0     ASSUMED. HB11 data: ~0.005% laser-to-alpha efficiency
                  (~4 OOM from net energy gain). Marvel: no yield data.
                  All LCOE results are contingent on ignition being achieved.

  eta_pin = 10%   UNCERTAIN. HB11 stated target; Marvel unpublished.
                  10 Hz continuous at PW-class energies is undemonstrated.

  eta_th = 40%    CONSERVATIVE. Marvel claims hybrid "up to ~70%" with
                  no engineering detail (TRL 2). HB11 uses ~38% steam.
                  Primary result uses steam-only assumption.

MEDIUM CONFIDENCE:
  f_rep = 10 Hz   Marvel ATLAS facility design; not yet at commercial scale.
  availability=75% No pulsed laser IFE plant analogue; placeholder.
  p-B11 aneutronic No blanket/tritium/heavy shielding confirmed.

FRAMEWORK DEFAULTS (no override data available):
  Laser driver    8.0 M$/MW_driver (NOAK DPSSL; no Marvel/HB11 cost data)
  Target factory  244 M$ at 1 GWe ref (Goodin et al. analogue)
  O&M             24 M$/yr base (pb11, aneutronic, no tritium)
  B-11 fuel cost  75 $/kg NOAK (industrial estimate; enrichment need unconfirmed)

SUPPLY CHAIN ADVANTAGES vs D-T:
  No tritium → no breeding blanket, no TBR constraint, no tritium startup cost
  No HTS tape → no superconducting magnet supply chain risk
  No beryllium/Li-6 → no exotic breeder materials
  Standard steel construction viable (UNSW collaboration confirms)
""")

# ── Sensitivity Analysis ──────────────────────────────────────────────
sens = model.sensitivity(result.params)

print("── Sensitivity (elasticity = %LCOE / %param) — Marvel 100 MWe ──")
print("-" * 56)

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
