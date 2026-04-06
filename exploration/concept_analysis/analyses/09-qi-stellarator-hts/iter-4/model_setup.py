"""QI Stellarator — HTS (Proxima Fusion Stellaris) — LCOE estimate.

Usage:
    uv run python model_setup.py              # print results to terminal
    uv run python model_setup.py | tee model_output.txt  # also save for synthesis stage

Modeling approach:
    Uses 1costingfe CostModel (STELLARATOR / DT) with the framework's ARIES-calibrated
    stellarator defaults as the base structure. Proxima Fusion has not released capital
    cost data for Stellaris, so no CAS22 sub-account overrides are applied. The model
    relies on published plasma and power-balance parameters from analysis.md §5 to set
    boundary conditions; all capital cost accounts are computed from framework defaults.

    The analysis recommends a "CAS-modified tokamak reference" delta approach
    (analysis.md §2, Recommended Modeling Approach): use the HTS compact tokamak
    (01-hts-compact-tokamak) as the base, then apply account-level multipliers for
    stellarator-specific differences. This delta is documented qualitatively in
    Key Assumptions below (§10) but is NOT implemented as explicit overrides — no
    source data exists to anchor the absolute coil cost.

    Key structural limitation:
    The 3D non-planar HTS coil manufacturing premium (C220103) — the dominant LCOE
    uncertainty for Stellaris (analysis.md §2, Challenge 1) — is NOT captured in the
    framework defaults. Framework calibration uses wound-coil (tokamak-style) geometry.
    The model output should be interpreted as a LOWER BOUND on coil capital cost.
    A coil-cost multiplier sweep (1.0×–5.0×) is included to bracket the range from
    Brown (2018) and analysis.md §7.

    Two operational scenarios are run:
    (A) H4-true (ignited): ECRH reduces to ~5 MW steady-state after alpha self-heating.
        Represents the optimistic case where QI maximum-j optimization enables adequate
        alpha confinement and the H&CD account becomes a large negative delta vs. tokamak.
        Based on Helios analogue (1 MW ignited; helios-stellarator-comparison.md §3.1).
    (B) H4-false (sustained ECRH): 50 MW ECRH required in steady-state — the value
        published in Stellaris Table 3. If full burning plasma is not achieved, this is
        the base case and the H&CD cost advantage largely disappears.

    Geometry:
    Major radius and plasma volume are not published (blocking gap; analysis.md §6 Gap 2).
    R0 and plasma_t are estimated from published average power density (6.1 MW/m³) and
    fusion power (2,700 MW), assuming aspect ratio R0/a ≈ 10 (W7-X heritage: R0/a = 10.4):
        plasma volume = 2700 MW / 6.1 MW/m³ ≈ 443 m³
        V ≈ 2π²R0a², R0/a = 10  →  20π²a³ = 443  →  a ≈ 1.31 m, R0 ≈ 13.1 m

    Thermal efficiency:
    Stellaris uses WCLL blanket with EUROFER97 structural steel (550°C operating limit),
    constraining steam Rankine to ~500°C. Gross thermal efficiency ≈ 38% (lower than
    Helios's 40% which uses vanadium alloy at 635°C; analysis.md §3). Net plant efficiency
    ~32% (1,000 MWe / 3,100 MWth; analysis.md §5) after recirculating power deduction.

Concept choice rationale:
    ConfinementConcept.STELLARATOR / Fuel.DT — maps to Stellaris's quasi-isodynamic (QI)
    stellarator configuration with D-T fuel. The STELLARATOR concept uses steady-state
    defaults (no disruptions, no CS coil, complex 3D coil assumptions) consistent with
    QI physics. No current drive is needed; p_input is ECRH only.

Key deviations from dt_tokamak.py reference:
    - Larger machine: R0 ≈ 13 m estimated (vs. 3–6 m for compact tokamaks).
    - No current drive: stellarators are current-free by design.
    - Dominant recirculating load: p_coils = 111 MW (coil system conduction power
      from Stellaris Table 3; far exceeds tokamak 2–3 MW default).
    - Capacity factor: 88% (Helios analogue; disruption-free operation).
    - eta_th = 0.38 (EUROFER97-constrained steam Rankine; lower than ARC's 0.46).
    - mn = 1.2 (WCLL PbLi neutron multiplication; vs. default 1.1).
    - No cost overrides: framework defaults used; C220103 is a lower bound.
"""

from costingfe import ConfinementConcept, CostModel, Fuel

# ── Model creation ────────────────────────────────────────────────────────

model = CostModel(concept=ConfinementConcept.STELLARATOR, fuel=Fuel.DT)

# ── Geometry constants (UNCERTAIN — major radius not published) ───────────
# Derived from: plasma volume = P_fus / power_density = 2700 MW / 6.1 MW/m³ ≈ 443 m³
# Assumed aspect ratio R0/a ≈ 10 (W7-X heritage: R0/a = 10.4; analysis.md §2 notes
# machine is larger than compact tokamak due to low-beta penalty at 2.76%).
# V ≈ 2π²R0a² → 443 = 20π²a³ → a ≈ 1.31 m, R0 ≈ 13.1 m (rounded to 13.0 m).
# UNCERTAIN: Full Stellaris paper (paywalled) contains actual major radius.
# Source: stellaris-design-details.md Table 3 (power density 6.1 MW/m³, fusion power 2700 MW);
#         analysis.md §6, Gap 2 (major radius = blocking gap)
_R0_ESTIMATED = 13.0   # m — UNCERTAIN: estimated from published power density
_A_ESTIMATED  = 1.30   # m — UNCERTAIN: minor radius; R0/a ≈ 10 assumed

# ── Shared forward-pass parameters ───────────────────────────────────────
# Used in both Scenario A and Scenario B to avoid duplication.
_SHARED = dict(
    # Net electrical: 1,000 MWe (Stellaris design target)
    # Source: dossier.md §Summary; stellaris-design-details.md Table 3
    net_electric_mw=1000.0,

    # Capacity factor: 88% (Helios analogue; disruption-free steady-state argument)
    # "enabling an 88% capacity factor" — helios-stellarator-comparison.md §2
    # W7-X demonstrated >97% experimental run-time; plant availability will be lower
    # due to scheduled blanket/divertor maintenance. Analysis range: 85–95%.
    # UNCERTAIN: Proxima has not published a Stellaris capacity factor target.
    # Source: analysis.md §5 (capacity factor row); analysis.md §2, H2;
    #         helios-stellarator-comparison.md §2
    availability=0.88,

    lifetime_yr=30,             # Standard 30-yr plant lifetime; DEFAULT
                                # NOTE: REBCO magnet lifetime ~10 FPY at 2.7 GW (neutron
                                # fluence limit 3×10²² m⁻²). Magnet replacement is a planned
                                # lifecycle event — cost not modeled here.
                                # Source: stellaris-design-details.md §2.8; analysis.md §5
    n_mod=1,                    # Single-module plant
    construction_time_yr=8.0,   # Stellarator default: complex 3D coil fabrication + assembly
                                # Source: mfe_stellarator.yaml default
    interest_rate=0.07,         # DEFAULT — standard capital cost rate
    inflation_rate=0.0245,      # DEFAULT
    noak=True,                  # NOAK central estimate

    # ── Geometry (estimated; not published) ──────────────────────────────
    # See geometry derivation in module docstring.
    # UNCERTAIN: major radius and plasma volume are blocking data gaps.
    # Source: analysis.md §6, Gap 2; stellaris-design-details.md Table 3 (power density)
    R0=_R0_ESTIMATED,           # [m] UNCERTAIN — derived from power density + fusion power
    plasma_t=_A_ESTIMATED,      # [m] UNCERTAIN — derived minor radius; R0/a ≈ 10 assumed
    elon=1.0,                   # Near-circular cross-section; stellarator default
    blanket_t=0.60,             # DEFAULT — WCLL blanket thickness
    ht_shield_t=0.20,           # DEFAULT
    structure_t=0.15,           # DEFAULT
    vessel_t=0.10,              # DEFAULT

    # ── Power balance ─────────────────────────────────────────────────────
    # Neutron energy multiplier: inferred from peak thermal / peak fusion power ratio
    # 3,300 MW thermal / 2,700 MW fusion ≈ 1.22 → WCLL PbLi Pb(n,2n) reactions
    # Source: stellaris-design-details.md Table 3; analysis.md §5
    mn=1.2,

    # Gross thermal efficiency: ~38% for steam Rankine at EUROFER97 temperature limit
    # Helios (vanadium alloy FW, 635°C steam): 40% — helios-stellarator-comparison.md §2
    # Stellaris (EUROFER97, 550°C limit → ~500°C steam): ~38% (lower than Helios).
    # Net plant efficiency ~32% (1,000 MWe / 3,100 MWth; analysis.md §5).
    # Source: analysis.md §3 (Balance of Plant, Steam Rankine paragraph);
    #         helios-stellarator-comparison.md §2
    eta_th=0.38,

    eta_p=0.5,                  # DEFAULT pumping efficiency
    eta_pin=0.5,                # DEFAULT ECRH wall-plug efficiency
                                # Current gyrotron state: ~50%; >60% possible with
                                # multi-stage depressed collectors (future improvement)
                                # Source: stellaris-design-details.md §2 (gyrotron note)
    eta_de=0.85,                # DEFAULT
    f_sub=0.03,                 # DEFAULT subsystem power fraction
    f_dec=0.0,                  # Thermal Rankine only; no direct energy conversion
                                # Source: dossier.md §Energy Capture

    # Coil system power: 111 MW conduction load from Stellaris Table 3
    # Published as "Conduction power to coils" — nuclear heating + thermal conduction
    # into the coil structure. Treated as an electrical recirculating power contribution
    # alongside ECRH and BOP pumping (~211–256 MW total in steady-state).
    # UNCERTAIN: May be nuclear heating removed by an intermediate coolant loop
    # (not requiring full cryogenic COP penalty) rather than a direct cryogenic load.
    # In either interpretation, the analysis treats this as 111 MW recirculating.
    # Source: stellaris-design-details.md Table 3; analysis.md §5 (recirculating breakdown)
    p_coils=111.0,              # [MW] from Table 3; much larger than tokamak default (2–3 MW)

    # WCLL coolant pumping: analysis.md §5 estimates ~50 MW total BOP pumping
    # (PbLi primary loop + water secondary loop in WCLL blanket).
    # Split: p_cool = 40 MW primary pumping, p_pump = 10 MW auxiliary.
    # Source: analysis.md §5 (recirculating power breakdown: "pumping ~50 MW")
    p_cool=40.0,                # [MW] WCLL primary pumping (PbLi + water); analysis.md §5
    p_pump=10.0,                # [MW] auxiliary pumping; analysis.md §5

    p_trit=10.0,                # DEFAULT tritium processing power [MW]; WCLL PbLi extraction
    p_house=4.0,                # DEFAULT housekeeping power [MW]

    # Cryogenic power: HTS coils at 20–40 K; upgraded from default 0.8 MW
    # Large coil system (111 GJ stored energy) requires larger cryo infrastructure.
    # ECRH superconducting transmission may also contribute.
    # Source: stellaris-design-details.md Table 3 (111 GJ stored magnetic energy);
    #         mfe_stellarator.yaml default 0.8 MW
    p_cryo=2.0,                 # [MW] upgraded from 0.8 MW default for larger coil system
)

# ── Scenario A: H4-true (ignited, ~5 MW ECRH steady-state) ──────────────
# ECRH reduces to nominal level after alpha self-heating takes over.
# "Only nominal heating (1 MW) is required once the plasma self-heats in the ignited phase"
# — helios-stellarator-comparison.md §3.1 (Helios analogue; QA/QI family, same physics)
# Using 5 MW (vs. Helios 1 MW) as conservative margin for Stellaris's larger plasma.
# Hypothesis H4: QI maximum-j optimization yields ~0.8% alpha energy loss
# (ANTS code; stellaris-design-details.md §2.2), sufficient for self-heating.
# UNCERTAIN: Burning plasma alpha confinement validation requires Alpha device (~2031).
# Source: helios-stellarator-comparison.md §3.1; analysis.md §2, Challenge 3a, H4

result_h4true = model.forward(
    p_input=5.0,                # [MW] H4-true: ignited; Helios analogue ~1 MW
                                # Source: helios-stellarator-comparison.md §3.1
    **_SHARED,
    # No cost overrides: no published Stellaris cost data.
    # C220103 (coils) = framework default = LOWER BOUND.
    # Analysis.md §7: stellarator C220103 is 1.5–5× the tokamak reference (Brown 2018).
    # Source: analysis.md §2, Challenge 1; §7 (CAS-level cost delta, CAS21 row)
)

# ── Results — Scenario A ──────────────────────────────────────────────────

c_a  = result_h4true.costs
pt_a = result_h4true.power_table

print("QI Stellarator — HTS (Proxima Fusion Stellaris) — 1 GWe, NOAK")
print("Scenario A: H4-true (ignited, 5 MW ECRH steady-state), 88% capacity factor")
print(f"LCOE: {c_a.lcoe:.1f} $/MWh | Overnight: {c_a.overnight_cost:.0f} $/kW")
print(f"Fusion: {pt_a.p_fus:.0f} MW | Net: {pt_a.p_net:.0f} MW | Q_eng: {pt_a.q_eng:.1f}")
print(f"NOTE: C220103 coil cost uses framework defaults (LOWER BOUND; 3D premium not modeled)")
print()

cas_rows = [
    ("CAS10", "Preconstruction",          c_a.cas10),
    ("CAS21", "Buildings",                c_a.cas21),
    ("CAS22", "Reactor Plant Equipment",  c_a.cas22),
    ("CAS23", "Turbine Plant",            c_a.cas23),
    ("CAS24", "Electrical Plant",         c_a.cas24),
    ("CAS25", "Miscellaneous",            c_a.cas25),
    ("CAS26", "Heat Rejection",           c_a.cas26),
    ("CAS27", "Special Materials",        c_a.cas27),
    ("CAS28", "Digital Twin",             c_a.cas28),
    ("CAS29", "Contingency",              c_a.cas29),
    ("CAS30", "Indirect Costs",           c_a.cas30),
    ("CAS40", "Owner's Costs",            c_a.cas40),
    ("CAS50", "Supplementary",            c_a.cas50),
    ("CAS60", "IDC",                      c_a.cas60),
    ("CAS70", "O&M (annualized)",         c_a.cas70),
    ("CAS80", "Fuel (annualized)",        c_a.cas80),
    ("CAS90", "Financial",                c_a.cas90),
]

print(f"{'Code':<8} {'Account':<28} {'M$':>10}")
print("-" * 48)
for code, name, val in cas_rows:
    print(f"{code:<8} {name:<28} {float(val):>10.1f}")
print("-" * 48)
print(f"{'':8} {'Total Capital':<28} {float(c_a.total_capital):>10.1f}")

# ── CAS22 sub-account detail ──────────────────────────────────────────────

print("\nCAS22 Sub-accounts (Reactor Plant Equipment) — Scenario A (H4-true):")
print(f"{'Code':<12} {'Account':<34} {'M$':>8}  {'Note'}")
print("-" * 78)

cas22_labels = {
    "C220101": "First Wall + WCLL Blanket",
    "C220102": "Shield",
    "C220103": "Coils (3D HTS — LOWER BOUND)",
    "C220104": "Heating System (ECRH, 5 MW)",
    "C220105": "Primary Structure",
    "C220106": "Vacuum Vessel",
    "C220107": "Power Supplies",
    "C220108": "Divertor (island divertor)",
    "C220109": "DEC",
    "C220111": "Installation",
    "C220112": "Isotope Separation",
    "C220200": "Coolant (WCLL circuits)",
    "C220300": "Aux Cooling",
    "C220400": "Rad Waste",
    "C220500": "Fuel Handling (tritium)",
    "C220600": "Other Equipment",
    "C220700": "I&C",
}

overridden_a = set(result_h4true.overridden) if hasattr(result_h4true, "overridden") else set()
for code, label in cas22_labels.items():
    val = result_h4true.cas22_detail.get(code, 0.0)
    if code == "C220103":
        note = "[DEFAULT — LOWER BOUND; 3D premium not modeled; see Key Assumptions #3]"
    elif code in overridden_a:
        note = "[override]"
    else:
        note = "[DEFAULT]"
    print(f"{code:<12} {label:<34} {float(val):>8.1f}  {note}")
print("-" * 78)
total22_a = result_h4true.cas22_detail.get("C220000", float(c_a.cas22))
print(f"{'C220000':<12} {'TOTAL':<34} {float(total22_a):>8.1f}")

# ── Scenario B: H4-false (50 MW ECRH sustained) ──────────────────────────
# If Stellaris does not achieve full alpha self-heating, 50 MW ECRH must be maintained
# continuously. This is the value published in Stellaris Table 3 and represents the
# conservative / status-quo operational assumption.
# Analysis.md §2, Challenge 3: "It is unclear whether this 50 MW is a conservative
# operational assumption or reflects that Stellaris does not reach full ignition."
# Source: stellaris-design-details.md Table 3; analysis.md §2, H4

result_h4false = model.forward(
    p_input=50.0,               # [MW] per stellaris-design-details.md Table 3 (stated value)
    **_SHARED,
)

cf  = result_h4false.costs
ptf = result_h4false.power_table

print(f"\nScenario B: H4-false (50 MW sustained ECRH; per Stellaris Table 3 stated value)")
print(f"  LCOE: {cf.lcoe:.1f} $/MWh | Overnight: {cf.overnight_cost:.0f} $/kW")
print(f"  Fusion: {ptf.p_fus:.0f} MW | Net: {ptf.p_net:.0f} MW | Q_eng: {ptf.q_eng:.1f}")
print(f"  LCOE delta vs. Scenario A: {cf.lcoe - c_a.lcoe:+.1f} $/MWh")
print(f"  Source: stellaris-design-details.md Table 3 (H&CD column); analysis.md §2, H4")

# ── Coil cost multiplier sweep (3D manufacturing premium) ────────────────
# C220103 in Scenario A reflects wound-coil (tokamak-style) framework defaults.
# The actual Stellaris coil cost is 1.5–5× that reference (Brown 2018; analysis.md §7).
# This sweep shows the LCOE sensitivity to the 3D HTS coil manufacturing premium —
# the single most important unknown for Stellaris competitiveness.
# Source: analysis.md §2, Challenge 1; §7 (CAS21 row); analysis.md §2, H1

_c220103_base = float(result_h4true.cas22_detail.get("C220103", 0.0))

print(f"\nCoil cost multiplier sweep (C220103 3D manufacturing premium):")
print(f"Base C220103 (framework default): {_c220103_base:.0f} M$ (wound-coil calibration)")
print(f"Source: analysis.md §7 (CAS21 row); Brown (2018) IEEE TPS; analysis.md §2, H1")
print(f"{'Multiplier':<14} {'C220103 (M$)':>14} {'LCOE ($/MWh)':>14} {'Overnight ($/kW)':>18}")
print("-" * 62)

for mult in [1.0, 1.5, 2.5, 5.0]:
    _c220103_override = round(_c220103_base * mult, 1)
    _r = model.forward(
        p_input=5.0,
        cost_overrides={"C220103": _c220103_override},
        **_SHARED,
    )
    _label = "DEFAULT" if mult == 1.0 else f"{mult}×"
    print(f"  {_label:<12} {_c220103_override:>14.0f} {float(_r.costs.lcoe):>14.1f}"
          f" {float(_r.costs.overnight_cost):>18.0f}")

print("  (1.5× = optimistic; 5× = pessimistic; SMC demo 2027 = first data point)")
print("  Source: analysis.md §2, H1 (H1: premium < 2× per kAm is viability threshold)")

# ── Key Assumptions ───────────────────────────────────────────────────────

print("""
Key Assumptions
===============
1. Net electric output: 1,000 MWe
   Source: dossier.md §Summary; stellaris-design-details.md Table 3.

2. Capacity factor: 88% (central estimate; Helios analogue + disruption-free argument)
   Helios: "enabling an 88% capacity factor" — helios-stellarator-comparison.md §2.
   W7-X demonstrated >97% experimental run-time; plant availability lower due to
   scheduled blanket/divertor maintenance. Analysis range: 85–95%.
   UNCERTAIN: Proxima has not published a capacity factor target for Stellaris.
   Source: analysis.md §5 (capacity factor row); analysis.md §2, H2.

3. C220103 (coils) — LOWER BOUND; 3D manufacturing premium NOT modeled [PRIMARY CAVEAT]
   Framework C220103 defaults calibrate to wound-coil (tokamak-style) geometry.
   Stellaris uses complex 3D non-planar HTS coils — no commercial manufacturing precedent.
   Analysis.md §7 (citing Brown 2018 IEEE TPS): stellarator coil cost is 1.5–5× the
   equivalent wound-coil tokamak reference. The framework output is the lower end of this
   range. The coil multiplier sweep above brackets the competitive uncertainty:
     - H1 (analysis.md §2): premium < 2× per kAm is the viability threshold. If false
       (>2×), stellarator CAPEX is unlikely to be competitive against compact HTS tokamaks
       regardless of capacity factor advantage.
     - First real data point: Stellarator Model Coil (SMC) demo targeted for 2027.
   Source: analysis.md §2, Challenge 1, H1; §7 (CAS21 row); Brown (2018) IEEE TPS.

4. Thermal efficiency: 38% gross (steam Rankine; EUROFER97 temperature limit ~500°C)
   EUROFER97 structural steel: 550°C operating limit → steam cycle ~500°C → ~38% gross.
   Helios analogue (vanadium alloy FW, 635°C steam): 40% — helios-stellarator-comparison.md §2.
   Net plant efficiency ~32% inferred from 1,000 MWe / 3,100 MWth (analysis.md §5).
   Note: adopting vanadium alloy (Helios approach) would recover ~2 percentage points
   of cycle efficiency but trades supply-chain maturity (analysis.md §3, Balance of Plant).
   Source: analysis.md §3 (Steam Rankine paragraph); helios-stellarator-comparison.md §2.

5. H4 hypothesis (ignition / H&CD cost): two scenarios modeled above
   Scenario A (H4-true): 5 MW ECRH steady-state (ignited); based on Helios analogue
   (1 MW ignited; helios-stellarator-comparison.md §3.1). Large negative delta vs. tokamak.
   Scenario B (H4-false): 50 MW ECRH steady-state (Stellaris Table 3 stated value).
   If Stellaris does not achieve full alpha self-heating, H&CD cost reverts to near-parity
   with the tokamak reference, and the net directional comparison in analysis.md §7 changes.
   Alpha device (Q>1, ~2031) is the first validation point for H4.
   ECRH wall-plug efficiency: current ~50%; >60% possible with depressed collectors
   (analysis.md §3, ECRH system). Modeled at default eta_pin=0.5.
   Source: stellaris-design-details.md Table 3; analysis.md §2, Challenge 3, H4;
           helios-stellarator-comparison.md §3.1.

6. Coil conduction / recirculating power: p_coils = 111 MW
   "Conduction power to coils: 111 MW" from Stellaris Table 3. Treated as the dominant
   electrical recirculating load for the coil system (nuclear heating + current lead losses
   + power supply efficiency). Combined with ECRH and ~50 MW BOP pumping: total
   recirculating ≈ 161 MW (Scenario A) to 206 MW (Scenario B), consistent with the
   ~20–25% recirculating fraction inferred in analysis.md §5.
   UNCERTAIN: Physical mechanism uncertain (cryogenic load vs. warm-structure nuclear
   heating vs. power supply losses); all interpretations produce the same p_coils treatment.
   NOTE: The coincidence of 111 GJ (stored magnetic energy) and 111 MW (conduction power)
   in Table 3 may reflect a transcription artifact — both values sourced independently.
   Source: stellaris-design-details.md Table 3; analysis.md §5 (recirculating breakdown).

7. Geometry: UNCERTAIN (blocking data gap)
   R0 ≈ 13 m, a ≈ 1.3 m estimated from power density (6.1 MW/m³) × fusion power
   (2,700 MW) = 443 m³ plasma volume, with R0/a ≈ 10 (W7-X heritage).
   Low-beta penalty (β = 2.76%) means Stellaris is larger than a compact HTS tokamak at
   equivalent fusion power (analysis.md §2, Challenge 2).
   Full Stellaris paper (paywalled) contains actual machine dimensions.
   Source: stellaris-design-details.md Table 3; analysis.md §2, Challenge 2; §6, Gap 2.

8. Neutron multiplier: mn = 1.2 (WCLL PbLi blanket)
   Inferred from peak thermal power (3,300 MW) / peak fusion power (2,700 MW) ≈ 1.22.
   Consistent with WCLL blanket neutron multiplication by Pb(n,2n) reactions.
   Source: stellaris-design-details.md Table 3; analysis.md §5.

9. Magnet replacement lifecycle cost: NOT modeled
   REBCO neutron fluence limit: 3×10²² m⁻² → ~10 full-power years at 2,700 MW.
   "The magnet system would have a lifetime of approximately 10 full power years at a
   fusion power of 2700 MW" — stellaris-design-details.md §2.8.
   At least two magnet replacements are required over a 30-yr plant lifetime. This adds a
   deferred CAPEX component unique among the concepts analyzed (coil replacement at scale
   not shared by compact HTS tokamaks on the same fluence timeline).
   Not captured by framework CAS72 (which models blanket/divertor replacement only).
   Source: stellaris-design-details.md §2.8; analysis.md §5 (REBCO magnet lifetime row).

10. CAS-level directional deltas vs. 01-hts-compact-tokamak reference (analysis.md §7):
    CAS21 (magnet system):         Large +  (1.5–5×; Brown 2018; 3D coil geometry premium)
    C220104 (H&CD / ECRH):         Large −  (−50 to −80%; conditional on H4 = true)
    C220101 (first wall / blanket): Small +  (5–15%; 3D tungsten tile fabrication premium)
    CAS24 (heat transport):         Small −  (~−10%; WCLL water cooling vs. FLiBe)
    CAS25 (power conversion):       Small −  (~−5–10%; EUROFER97 simpler BOP vs. sCO₂)
    Net directional outcome: UNCERTAIN. Dominated by CAS21 coil cost vs. C220104 saving.
    Capacity factor advantage (not a capital cost) must offset coil premium in the LCOE
    denominator. H2 (analysis.md §2): ≥88% CF is needed to offset the coil premium at the
    optimistic 1.5× multiplier; insufficient at >2.5× regardless of availability benefit.
    Source: analysis.md §7 (CAS-level cost delta table); §2, H1, H2.
""")

# ── Sensitivity analysis ──────────────────────────────────────────────────

sens = model.sensitivity(result_h4true.params)

print("Sensitivity (elasticity = %LCOE / %param) — Scenario A (H4-true, NOAK)")
print("NOTE: C220103 gradient reflects wound-coil framework defaults, not actual")
print("      3D coil cost structure. See coil multiplier sweep above for the true")
print("      primary sensitivity axis.")
print("-" * 52)

print("\nEngineering levers:")
for k, v in sorted(sens["engineering"].items(), key=lambda x: abs(x[1]), reverse=True):
    print(f"  {k:<28} {v:+.4f}")

print("\nFinancial:")
for k, v in sorted(sens["financial"].items(), key=lambda x: abs(x[1]), reverse=True):
    print(f"  {k:<28} {v:+.4f}")
