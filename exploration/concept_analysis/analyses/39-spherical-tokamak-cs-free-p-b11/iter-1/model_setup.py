"""Spherical Tokamak - CS-free p-B11 (ENN Energy) — SPECULATIVE LCOE placeholder.

Modeling approach
-----------------
SPECULATIVE PLACEHOLDER — ENN has published no commercial plant study.  All
plant-level parameters (major radius, net electric output, Q value, fuel cycle
details) are analyst assumptions built from scaled ST geometry (EHL-2 reference),
p-B11 physics analogues, and cross-concept comparison with analysis
21-spherical-tokamak-hts.

The p-B11 Lawson criterion is unresolved experimentally (analysis.md §Section 2,
Challenge 1); this model cannot be validated against any plant study.  Results
represent a best-case scenario in which BOTH p-B11 ignition AND direct energy
conversion are achieved.  LCOE figures carry fundamental physics uncertainty and
should be interpreted only as an order-of-magnitude bound, not a forecast.

Key deviations from a standard D-T tokamak
-------------------------------------------
- No breeding blanket (blanket_t = 0.05 m, minimal shielding only)
- Direct energy conversion (f_dec=0.85, eta_de=0.80) replaces steam Rankine cycle
  for the charged-particle (alpha) energy fraction
- Radiation fraction (15%) captured thermally at eta_th=0.35
- No tritium processing (p_trit=0); p-B11 aneutronic fuel cycle
- Large ECRH recirculating power for CS-free non-inductive current drive (200 MW)
- Copper resistive coil ohmic loss penalty (50 MW; optimistic — see note below)
- All engineering parameters UNCERTAIN at commercial scale

Concept choice rationale
------------------------
ConfinementConcept.TOKAMAK for spherical tokamak geometry.
Fuel.PB11 for proton-boron-11 aneutronic fuel cycle.
Native design point: 500 MWe (analyst assumption; no ENN plant study exists).

Usage:
    uv run python model_setup.py              # print results to terminal
    uv run python model_setup.py | tee model_output.txt  # also save for synthesis stage
"""

from costingfe import ConfinementConcept, CostModel, Fuel

# ── Model instantiation ──────────────────────────────────────────────
model = CostModel(concept=ConfinementConcept.TOKAMAK, fuel=Fuel.PB11)

# ── Plant configuration ──────────────────────────────────────────────
# All values SPECULATIVE — ENN has published no commercial plant design.
# analysis.md §Section 1: data rating "Opaque"; §Section 5: all LCOE inputs
# are classified "truly-unknown / blocking".

# ── Customer-level requirements ──────────────────────────────────────

NET_ELECTRIC_MW = 500.0     # UNCERTAIN: analyst assumption — no ENN plant study exists
                            # analysis.md §Section 5: commercial plant net output truly-unknown

AVAILABILITY = 0.80         # UNCERTAIN: steady-state intent is favorable (CS-free ECRH
                            # enables continuous operation), but novel technology and direct
                            # energy converter maintenance lower confidence vs. mature D-T MCF
                            # analysis.md §Section 5, Missing Parameters: capacity factor truly-unknown

LIFETIME_YR = 30            # DEFAULT: standard fusion plant lifetime assumption
CONSTRUCTION_TIME_YR = 7.0  # UNCERTAIN: novel technology premium; no published schedule

# ── Geometry (speculative commercial ST) ─────────────────────────────
# Scaled up from EHL-2 (R₀=1.05 m, A=1.85) to a notional commercial device.
# analysis.md §Section 5: EHL-2 R₀=1.05 m is a physics verification device.
# Cross-reference: 21-spherical-tokamak-hts uses R0=5.0 m, A=2.3 for a larger
# commercial ST; ENN's concept assumed smaller (more compact) given CS-free constraint.

R0 = 3.5                    # m — UNCERTAIN: speculative commercial major radius
                            # analysis.md §Section 5: no commercial design point exists;
                            # chosen as a plausible mid-scale ST between EHL-2 (1.05 m)
                            # and Tokamak Energy ST-E1 (5.0 m)
ASPECT_RATIO = 1.8          # UNCERTAIN: spherical tokamak regime; EHL-2: A=1.85
                            # analysis.md §Section 5 (enn-roadmap-pb11-arxiv-2401.11338.md)
PLASMA_T = R0 / ASPECT_RATIO  # ~1.94 m minor radius; derived from R0/A

ELON = 2.5                  # UNCERTAIN: typical spherical tokamak elongation; unpublished

BLANKET_T = 0.05            # m — minimal thin shield; NO breeding blanket for p-B11
                            # analysis.md §Section 4: no FLiBe/Be/Li-6 needed; shielding
                            # retained for secondary neutrons from side reactions
HT_SHIELD_T = 0.30          # m — UNCERTAIN: slightly thicker than D-T default due to
                            # all-charged-particle heat load and alpha particle management
STRUCTURE_T = 0.20          # m — DEFAULT
VESSEL_T = 0.20             # m — DEFAULT

# ── Power balance (p-B11 direct energy conversion) ───────────────────
# Primary reaction: p + ¹¹B → 3α, ~8.7 MeV total (no neutrons)
# analysis.md §Section 5: p-B11 reaction energy = ~8.7 MeV (3α, ~2.9 MeV each)
# f_rad_pb11=0.15 (costing_constants.yaml): bremsstrahlung from Z=5 boron
# → 85% of fusion energy in charged alphas available for direct energy conversion

F_DEC = 0.85                # fraction of fusion power to DEC (alpha-heated fraction)
                            # analysis.md §Section 5: p-B11 all-charged-particle; bremsstrahlung 15%

ETA_DE = 0.80               # UNCERTAIN: direct conversion efficiency
                            # analysis.md §Section 2, Challenge 2: theoretical 70–90%
                            # No engineering design published (TRL 1–2); 0.80 is optimistic
                            # dossier.md §Energy Capture: stated intent, no hardware

ETA_TH = 0.35               # Fallback thermal efficiency for radiation fraction (15%)
                            # analysis.md §Section 7: fallback thermal cycle if DEC not realized
                            # DEFAULT: steam Rankine analogue; cross-reference 21-spherical-tokamak-hts

ETA_PIN = 0.50              # Gyrotron wall-plug efficiency for ECRH current drive
                            # analysis.md §Section 7 (via cross-reference 21-spherical-tokamak-hts §S5)
                            # EXL-50 demonstrated ~1 A/W ECRH efficiency; gyrotron WPE ~50–55%
                            # dossier.md §Driver Technology (arXiv:2104.14844)

# ECRH recirculating power — the largest single LCOE uncertainty
# analysis.md §Section 2, Challenge 3: commercial plasma current >> 3 MA (EHL-2)
# EXL-50: ~1 A/W ECRH current drive efficiency; dossier.md §Driver Technology
# At 50% gyrotron WPE, CS-free current drive for >10 MA plasma → hundreds of MW
# 200 MW is an optimistic commercial estimate (analysis.md §Section 2, Challenge 3)
P_INPUT_MW = 200.0          # MW — UNCERTAIN: ECRH for CS-free current drive at reactor scale
                            # analysis.md §Section 5 (Gap 6): ECRH recirculating power truly-unknown

# Copper resistive coil ohmic loss
# analysis.md §Section 4: ITER-scale copper coils ≈300 MW ohmic loss at commercial scale;
# ENN commercial plant almost certainly requires HTS transition (not yet announced)
# 50 MW is optimistic — actual value likely 5–10× higher without HTS
P_COILS_MW = 50.0           # MW — UNCERTAIN: copper resistive coil recirculating power
                            # analysis.md §Section 4 (copper vs HTS note); dossier.md §Magnet Type

P_COOL_MW = 5.0             # MW — reduced vs D-T (no liquid metal blanket circuit)
                            # analysis.md §Section 4: no FLiBe/liquid Li circuit for p-B11
P_PUMP_MW = 1.0             # MW — DEFAULT: coolant pump
P_TRIT_MW = 0.0             # NO tritium processing — p-B11 aneutronic
                            # analysis.md §Section 4: no tritium supply chain for p-B11
P_HOUSE_MW = 4.0            # MW — DEFAULT: house loads
P_CRYO_MW = 0.0             # MW — no cryogenics assumed for copper resistive coils
                            # analysis.md §Section 5, dossier.md §Magnet Type: EXL-50U copper coils

# ── Financial parameters ──────────────────────────────────────────────
INTEREST_RATE = 0.07        # DEFAULT: standard project finance assumption
INFLATION_RATE = 0.0245     # DEFAULT: US long-run CPI target
NOAK = True                 # NOAK reference case

# ── Cost overrides ────────────────────────────────────────────────────
# None applied — framework pb11 defaults used throughout:
#   C220101 (blanket): blanket_unit_cost_pb11=0.05 M$/m³ (minimal shielding)
#   C220109 (DEC):     dec_base=$125M at 400 MWe DEC output — framework's DEC cost basis
#   CAS27:             special_materials_pb11=0 (no special materials)
#   CAS80:             u_b11_noak=$75/kg NOAK enriched B-11 (costing_constants.yaml)
#   CAS10:             licensing_cost_pb11=$0.1M (no NRC neutron license)
# analysis.md §Section 1: no published cost estimates exist; no override justified

# ── Shared kwargs ─────────────────────────────────────────────────────

_SHARED_KWARGS = dict(
    availability=AVAILABILITY,
    lifetime_yr=LIFETIME_YR,
    n_mod=1,
    construction_time_yr=CONSTRUCTION_TIME_YR,
    interest_rate=INTEREST_RATE,
    inflation_rate=INFLATION_RATE,
    noak=NOAK,

    # Speculative commercial ST geometry
    R0=R0,                          # 3.5 m — UNCERTAIN (scaled from EHL-2)
    plasma_t=PLASMA_T,              # 1.94 m — derived R0/A
    elon=ELON,                      # 2.5 — UNCERTAIN (ST analogue)
    blanket_t=BLANKET_T,            # 0.05 m — minimal shield, no breeding
    ht_shield_t=HT_SHIELD_T,        # 0.30 m — UNCERTAIN (alpha heat management)
    structure_t=STRUCTURE_T,        # 0.20 m — DEFAULT
    vessel_t=VESSEL_T,              # 0.20 m — DEFAULT

    # Power balance (p-B11 + DEC)
    p_input=P_INPUT_MW,             # 200 MW — UNCERTAIN (CS-free ECRH current drive)
    mn=1.0,                         # no neutron energy multiplication (aneutronic)
                                    # analysis.md §Section 5: primary reaction produces no neutrons
    eta_th=ETA_TH,                  # 0.35 — DEFAULT (fallback thermal for radiation fraction)
    eta_p=0.5,                      # DEFAULT: pumping efficiency
    eta_pin=ETA_PIN,                # 0.50 — gyrotron wall-plug efficiency
    eta_de=ETA_DE,                  # 0.80 — UNCERTAIN (DEC theoretical efficiency)
    f_sub=0.03,                     # DEFAULT: subsystem power fraction
    f_dec=F_DEC,                    # 0.85 — alpha particle fraction to DEC
    p_coils=P_COILS_MW,             # 50 MW — UNCERTAIN (copper resistive coil ohmic)
    p_cool=P_COOL_MW,               # 5 MW — reduced (no liquid metal circuit)
    p_pump=P_PUMP_MW,               # 1 MW — DEFAULT
    p_trit=P_TRIT_MW,               # 0 MW — aneutronic, no tritium
    p_house=P_HOUSE_MW,             # 4 MW — DEFAULT
    p_cryo=P_CRYO_MW,               # 0 MW — copper coils, no cryo
)

# ── Model forward passes ──────────────────────────────────────────────

# Native design point: 500 MWe (analyst assumption; no ENN plant study)
result = model.forward(net_electric_mw=NET_ELECTRIC_MW, **_SHARED_KWARGS)

# Self-consistent 1 GW result for cross-concept comparison.
# override_reference_mw tells the framework that engineering parameters
# are valid at 500 MWe and should scale to 1000 MWe via per-account laws.
result_1gw = model.forward(
    net_electric_mw=1000.0,
    override_reference_mw=NET_ELECTRIC_MW,
    **_SHARED_KWARGS,
)

# ── Results ───────────────────────────────────────────────────────────
c = result.costs
pt = result.power_table

print("Spherical Tokamak - CS-free p-B11 (ENN Energy) [SPECULATIVE PLACEHOLDER]")
print(f"  Config: {NET_ELECTRIC_MW:.0f} MWe net | {AVAILABILITY:.0%} availability | {LIFETIME_YR} yr | NOAK")
print(f"  Geometry: R0={R0} m, A={ASPECT_RATIO}, a={PLASMA_T:.2f} m, κ={ELON}")
print(f"  Power: ECRH p_input={P_INPUT_MW:.0f} MW (CS-free) | η_pin={ETA_PIN} | η_de={ETA_DE} | f_dec={F_DEC}")
print(f"  Coils: copper resistive p_coils={P_COILS_MW:.0f} MW (OPTIMISTIC — likely 5-10x higher)")
print(f"  WARNING: p-B11 ignition unresolved; DEC TRL 1-2; all parameters speculative")
print()
print(f"LCOE:       {c.lcoe:.1f} $/MWh")
print(f"Overnight:  {c.overnight_cost:.0f} $/kW")
print(f"Fusion:     {pt.p_fus:.0f} MW | Net: {pt.p_net:.0f} MW | Q_eng: {pt.q_eng:.2f}")
print()
print(f"1 GW scaled (cross-concept): LCOE {result_1gw.costs.lcoe:.1f} $/MWh | "
      f"Overnight {result_1gw.costs.overnight_cost:.0f} $/kW")
print()

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

print(f"{'Code':<8} {'Account':<28} {'M$':>10}")
print("-" * 48)
for code, name, val in cas:
    print(f"{code:<8} {name:<28} {float(val):>10.1f}")
print("-" * 48)
print(f"{'':8} {'Total Capital':<28} {float(c.total_capital):>10.1f}")

# ── CAS22 sub-account detail ──────────────────────────────────────────
print()
print("CAS22 sub-account detail:")
print(f"{'Code':<12} {'M$':>10}")
print("-" * 24)
for k, v in sorted(result.cas22_detail.items()):
    print(f"  {k:<10} {float(v):>10.1f}")

# ── Key assumptions summary ───────────────────────────────────────────
print()
print("=" * 60)
print("Key Assumptions and Data Quality")
print("=" * 60)
print(f"  Net electric (analyst assumption):             {NET_ELECTRIC_MW:.0f} MWe   [UNCERTAIN — no plant study]")
print(f"  Major radius R0:                               {R0} m    [UNCERTAIN — scaled from EHL-2 1.05 m]")
print(f"  Aspect ratio A → minor radius:                 {ASPECT_RATIO} → {PLASMA_T:.2f} m [UNCERTAIN — analogue]")
print(f"  Elongation κ:                                  {ELON}     [UNCERTAIN — ST analogue]")
print(f"  Direct conversion efficiency η_de:             {ETA_DE}    [UNCERTAIN — theoretical 70-90%, TRL 1-2]")
print(f"  DEC power fraction f_dec:                      {F_DEC}    [UNCERTAIN — 1-f_rad_pb11=0.85]")
print(f"  Fallback thermal efficiency η_th:              {ETA_TH}   [DEFAULT — steam Rankine for radiation fraction]")
print(f"  ECRH wall-plug η_pin:                          {ETA_PIN}   [MEDIUM — gyrotron analogue; cross-ref 21-ST-HTS]")
print(f"  Auxiliary input power (ECRH):                  {P_INPUT_MW:.0f} MW  [UNCERTAIN — CS-free current drive]")
print(f"  Copper coil ohmic loss:                        {P_COILS_MW:.0f} MW  [UNCERTAIN — optimistic; HTS transition needed]")
print(f"  Tritium processing power:                      {P_TRIT_MW:.0f} MW    [CONFIRMED — aneutronic, no tritium]")
print(f"  Availability:                                  {AVAILABILITY:.0%}   [UNCERTAIN — steady-state intent; novel tech]")
print(f"  Blanket: minimal thin shield only, no breeding          [CONFIRMED — p-B11 aneutronic]")
print(f"  p-B11 ignition physics:                        UNRESOLVED — Lawson criterion not demonstrated")
print(f"  Direct energy converter:                       TRL 1-2 — no engineering design published")
print(f"  All capital costs:                             FRAMEWORK DEFAULTS (no published cost data)")

# ── Sensitivity analysis ──────────────────────────────────────────────
sens = model.sensitivity(result.params)

print()
print("Sensitivity (elasticity = %LCOE / %param)")
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
