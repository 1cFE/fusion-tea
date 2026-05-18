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

# ── DEC failure scenario (F-1) ────────────────────────────────────────
# Tests the primary economic hypothesis: is p-B11 viable without DEC?
# eta_de = 0.0 models total DEC failure — the f_dec=0.85 alpha fraction
# produces no net electricity; only the bremsstrahlung fraction (15%)
# captured at eta_th=0.35 contributes.  To reach NET_ELECTRIC_MW, the
# framework requires much greater fusion power → larger, costlier plant.
result_dec_failure = model.forward(
    net_electric_mw=NET_ELECTRIC_MW,
    **{**_SHARED_KWARGS, "eta_de": 0.0},
)

# ── DEC failure — fixed fusion power variant (CF-F-1) ────────────────
# The DEC_failure scenario above scales UP fusion (and plant size) to reach
# 500 MWe with eta_de=0, producing only +4% LCOE — operationally misleading
# because it silently assumes the undemonstrated p-B11 Lawson criterion can
# be met at 60% higher fusion power in the same machine.
#
# This analytical variant holds P_fus at the base case value and computes
# what the SAME machine outputs when DEC fails:
#   - alpha fraction (85%) that fed DEC now routes to fallback thermal at η_th
#   - radiation fraction (15%) unchanged through thermal
#   - all parasitic loads (ECRH wall-plug, coils, aux) remain unchanged
# Capital costs are fixed (same geometry); only net output changes.
# LCOE approximation: LCOE_dff ≈ LCOE_base × (P_net_base / P_net_dff)
# (capital-dominated estimate; slightly underestimates LCOE vs. full calc)

# ── Results ───────────────────────────────────────────────────────────
c = result.costs
pt = result.power_table

# Derive fixed-fusion DEC failure metrics from base power table
_p_fus_base = pt.p_fus
_p_gross_base = pt.p_gross
_p_net_base = pt.p_net
_p_parasitic_base = _p_gross_base - _p_net_base   # all base loads (ECRH + coils + aux)
_gross_dff = ETA_TH * _p_fus_base                  # 100% fusion through fallback thermal
_net_dff = _gross_dff - _p_parasitic_base           # same parasitic, degraded gross
_lcoe_dff_approx = c.lcoe * (_p_net_base / max(1.0, _net_dff))  # capital-scaling estimate

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

c_dec = result_dec_failure.costs
pt_dec = result_dec_failure.power_table
print("DEC_failure scenario (eta_de=0.0 → no DEC; only 15% radiation fraction at η_th=0.35):")
print(f"  LCOE:    {c_dec.lcoe:.1f} $/MWh | Overnight: {c_dec.overnight_cost:.0f} $/kW")
print(f"  Fusion:  {pt_dec.p_fus:.0f} MW | Net: {pt_dec.p_net:.0f} MW | Q_eng: {pt_dec.q_eng:.2f}")
print(f"  vs. base case: LCOE {c.lcoe:.1f} → {c_dec.lcoe:.1f} $/MWh "
      f"({(c_dec.lcoe / c.lcoe - 1) * 100:+.0f}% change)")
print()

# DEC_failure_fixed_fusion: same machine, degraded output (CF-F-1)
print("DEC_failure_fixed_fusion (hold P_fus at base, eta_de=0 → thermal-only recovery):")
print(f"  P_fus = {_p_fus_base:.0f} MW (fixed) | Gross (thermal-only) = {_gross_dff:.0f} MWe | "
      f"Parasitic = {_p_parasitic_base:.0f} MWe | Net ≈ {_net_dff:.0f} MWe")
print(f"  LCOE (approx): {_lcoe_dff_approx:.1f} $/MWh  [capital-scaling estimate; same geometry as base]")
print(f"  vs. DEC_failure_fixed_net: {c_dec.lcoe:.1f} $/MWh (+{(c_dec.lcoe/c.lcoe-1)*100:.0f}%) "
      f"— scale-up variant masks DEC go/no-go by assuming 60% higher P_fus in same machine")
print(f"  Interpretation: DEC failure is NOT +{(c_dec.lcoe/c.lcoe-1)*100:.0f}%; "
      f"same machine yields ~{_net_dff:.0f} MWe, LCOE ~{_lcoe_dff_approx:.0f} $/MWh")
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

# CF-F-3: patch NaN for interest_rate via finite-difference (IDC compounds non-analytically)
_ir_raw = sens["financial"].get("interest_rate", float("nan"))
if _ir_raw != _ir_raw:  # NaN check (NaN != NaN)
    _ir_delta = 0.01  # 1 percentage point perturbation
    _r_ir_lo = model.forward(
        net_electric_mw=NET_ELECTRIC_MW,
        **{**_SHARED_KWARGS, "interest_rate": INTEREST_RATE - _ir_delta},
    )
    _r_ir_hi = model.forward(
        net_electric_mw=NET_ELECTRIC_MW,
        **{**_SHARED_KWARGS, "interest_rate": INTEREST_RATE + _ir_delta},
    )
    # ε = (dLCOE/dr) × (r / LCOE) ≈ ((LCOE_hi - LCOE_lo) / (2Δr)) × (r / LCOE_base)
    _ir_elasticity = (
        (_r_ir_hi.costs.lcoe - _r_ir_lo.costs.lcoe) / (2 * _ir_delta)
    ) * (INTEREST_RATE / c.lcoe)
    sens["financial"]["interest_rate"] = _ir_elasticity

print("\nFinancial:")
for k, v in sorted(sens["financial"].items(), key=lambda x: abs(x[1]), reverse=True):
    print(f"  {k:<36} {v:+.4f}")

print("\nCosting constants (top 15):")
costing = sorted(sens["costing"].items(), key=lambda x: abs(x[1]), reverse=True)
for k, v in costing[:15]:
    print(f"  {k:<36} {v:+.4f}")

# ── ECRH recirculating power sweep (F-3) ─────────────────────────────
# Analysis §Section 2, Challenge 3: CS-free current drive could represent
# 30–50%+ of gross output. Base case 200 MW ≈ 13% of ~1488 MWe gross —
# optimistic. Upper concern bound is 600–700 MW (40–47% of gross output).
print()
print("ECRH p_input sweep (CS-free concern range: 13%→47% of gross output):")
print(f"  {'p_input (MW)':<16} {'% of ~1488 MWe gross':<24} {'LCOE ($/MWh)':>14}")
print("-" * 58)
_BASE_GROSS_MW = 1488.0  # base gross from power table (200 MW ≈ 13%)
for _p_in in [200, 400, 600, 700]:
    _r = model.forward(
        net_electric_mw=NET_ELECTRIC_MW,
        **{**_SHARED_KWARGS, "p_input": _p_in},
    )
    print(f"  {_p_in:<16.0f} {_p_in / _BASE_GROSS_MW * 100:<24.1f}% {_r.costs.lcoe:>12.1f}")
print("  (200 MW = optimistic base; 600–700 MW = analysis §S2 concern bound)")

# ── Copper coil recirculating power sweep (CF-F-2) ────────────────────
# Model flags p_coils = 50 MW as OPTIMISTIC. Analysis §S3 states commercial-scale
# copper coils could consume ~300 MW. ECRH sweep exists but no p_coils sweep does.
# At p_coils elasticity ≈ +0.019, the 50→500 MW range is material (~17% LCOE impact).
print()
print("Copper coil recirculating power range (HTS-less scenario, CF-F-2):")
print(f"  {'p_coils (MW)':<16} {'LCOE ($/MWh)':>14} {'vs. base':>10}")
print("-" * 44)
for _p_c in [50, 150, 300, 500]:
    _r_c = model.forward(
        net_electric_mw=NET_ELECTRIC_MW,
        **{**_SHARED_KWARGS, "p_coils": _p_c},
    )
    _delta_pct = (_r_c.costs.lcoe / c.lcoe - 1) * 100
    print(f"  {_p_c:<16.0f} {_r_c.costs.lcoe:>12.1f}  {_delta_pct:>+8.1f}%")
print("  (50 MW = optimistic base; 300–500 MW = ITER-scale copper coils per §S3)")
print("  Note: at p_coils > 300 MW, ohmic loss exceeds the ECRH concern midpoint (300 MW),")
print("  making combined recirculating fraction a compounding risk")

# ── Hot ion mode heating burden — H4 (F-3, Li 2024) ─────────────────
# Li (2024) [arxiv-2406-15495]: under fusion self-heating, achievable Ti/Te ≈ 0.57
# (not the required ~4). Maintaining Ti/Te = 4 requires external heating power
# P_heating = (k-1) × P_fusion, with k = 5–20 from Li's calculation.
# This is a distinct load from ECRH current drive (p_input): it is plasma-state
# maintenance power, not current drive. k=1 = "physics solved" base case (no burden).
#
# This sweep is analytical (same plant geometry = same capital costs).
# P_hotmion_electrical = (k-1) × P_fus / ETA_PIN [MWe wall-plug for each k]
# Net degrades: P_net_H4 = P_gross_base - P_parasitic_base - P_hotmion_electrical

print()
print("Hot ion mode heating burden — H4 (Li 2024, arxiv-2406-15495):")
print(f"  Maintaining Ti/Te = 4 requires P_heating = (k-1) × P_fusion (Li 2024)")
print(f"  Base: P_fus = {_p_fus_base:.0f} MW | P_gross = {_p_gross_base:.0f} MWe | "
      f"P_parasitic = {_p_parasitic_base:.0f} MWe | P_net = {_p_net_base:.0f} MWe")
print(f"  k=1: physics solved (base case — no extra heating); k=5–20: Li calculated range")
print()
print(f"  {'k':<6} {'P_hotmion (MW)':<18} {'Elec cost (MWe)':<18} {'P_net (MWe)':<14} {'Status'}")
print("-" * 72)
_goNogo_k = 1.0 + _p_net_base * ETA_PIN / _p_fus_base  # k at which P_net_H4 = 0
for _k in [1, 1.1, 1.5, 2, 5, 10, 20]:
    _p_hotmion_thermal = (_k - 1) * _p_fus_base           # MW thermal (Li's definition)
    _p_hotmion_elec = _p_hotmion_thermal / ETA_PIN         # MWe wall-plug
    _p_net_h4 = _p_gross_base - _p_parasitic_base - _p_hotmion_elec
    if _k == 1:
        _status = "base case (physics solved)"
    elif _p_net_h4 <= 0:
        _status = "Q_eng < 0 — concept non-viable"
    else:
        _status = f"viable ({_p_net_h4:.0f} MWe)"
    print(f"  {_k:<6.1f} {_p_hotmion_thermal:<18.0f} {_p_hotmion_elec:<18.0f} "
          f"{_p_net_h4:<14.0f} {_status}")
print()
print(f"  Go/no-go threshold: k ≈ {_goNogo_k:.2f}  "
      f"(any heating burden > {(_goNogo_k-1)*100:.0f}% of fusion power eliminates net output)")
print(f"  Li (2024) minimum k = 5 is {(5-_goNogo_k)/(max(0.01,_goNogo_k-1)):.0f}× beyond break-even")
print(f"  Conclusion: hot ion mode heating burden represents a pre-engineering go/no-go gate")
print(f"  that collapses the model at k > {_goNogo_k:.2f}, independent of DEC efficiency or ECRH design")
