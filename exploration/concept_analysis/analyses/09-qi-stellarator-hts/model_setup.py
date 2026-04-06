# STALE: analysis-updated-iter-8
"""QI Stellarator — HTS (Proxima Fusion Stellaris) — LCOE estimate.

Usage:
    uv run python model_setup.py              # print results to terminal
    uv run python model_setup.py | tee model_output.txt  # also save for synthesis stage

Modeling approach:
    Uses 1costingfe CostModel (STELLARATOR / DT) with the framework's ARIES-calibrated
    stellarator defaults as the base cost structure. Proxima Fusion has not released capital
    cost data for Stellaris, so no CAS22 sub-account overrides are applied. The model relies
    on published plasma and power-balance parameters from analysis.md §5 to set boundary
    conditions; all capital cost accounts are computed from framework defaults.

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

    CAS account structure note:
    The framework uses the standard ARIES/fusion CAS20X convention. CAS22 (Reactor Plant
    Equipment) is the super-account containing all nuclear island sub-accounts. The coil
    system lives at C220103 and heating at C220104 — both within CAS22, not at a separate
    CAS21. CAS21 in this model is Buildings (~$930M), not magnets. This differs from
    PROCESS-style per-subsystem top-level numbering (analysis.md §7, CAS account structure
    note).

    Periodic magnet replacement — lifetime cost:
    REBCO neutron fluence limit (~3×10²² m⁻²) constrains the coil system lifetime to
    approximately 10 full-power years (FPY) at 2,700 MW fusion power. Two coil replacements
    are required over a 30-year plant lifetime. This adds a deferred CAPEX component unique
    to the stellarator on this timeline (compact HTS tokamaks are not on the same 10-yr
    coil replacement schedule). The CAS72 framework sub-account models blanket/divertor
    replacement only; coil replacement must be computed separately and is displayed
    explicitly in the output as a replacement-inclusive LCOE. The raw initial-build LCOE
    (without replacement) is a lower bound and biases the cross-concept comparison if
    reported alone. (analysis.md §7 Cross-Concept Notes, final table footnote)

    Three operational/design scenarios are run:
    (A) H4-true (ignited): ECRH reduces to ~5 MW steady-state after alpha self-heating.
        Represents the optimistic case where QI maximum-j optimization enables adequate
        alpha confinement and the H&CD account becomes a large negative delta vs. tokamak.
        Based on Helios analogue (1 MW ignited; helios-stellarator-comparison.md §3.1).
    (B) H4-false (sustained ECRH): 50 MW ECRH required in steady-state — the value
        published in Stellaris Table 3. If full burning plasma is not achieved, this is
        the base case and the H&CD cost advantage largely disappears.
    (H2a) Higher-beta QI design [next-gen QI, not Stellaris v1]: follow-on 4% beta
        scenario per CIEMAT-QI4X finding (arXiv:2512.08825, December 2025). At 4% beta
        vs. 2.76%, plasma volume at fixed fusion power density scales down by ~31%,
        reducing first wall area, blanket mass, and vacuum vessel scale proportionally.
        H4-true ECRH assumption used. This is a scenario branch for next-generation QI
        designs, NOT a Stellaris v1 variant.
        Source: analysis.md §2, Challenge 2, H2a; arxiv-2512-08825.md (CIEMAT-QI4X)

    Geometry:
    Major radius and plasma volume are not published (blocking gap; analysis.md §6 Gap 2).
    R0 and plasma_t are estimated from published average power density (6.1 MW/m³) and
    fusion power (2,700 MW), assuming aspect ratio R0/a ≈ 10 (W7-X heritage: R0/a = 10.4):
        plasma volume = 2700 MW / 6.1 MW/m³ ≈ 443 m³
        V ≈ 2π²R0a², R0/a = 10  →  20π²a³ = 443  →  a ≈ 1.31 m, R0 ≈ 13.1 m

    H2a geometry scaling:
    At 4% beta vs. 2.76%, plasma volume scales linearly with beta at fixed fusion power
    and power density: V_H2a = 443 × (2.76/4.0) ≈ 306 m³ (~31% reduction).
    New minor radius: 20π²a³ = 306 → a ≈ 1.16 m, R0 ≈ 11.6 m.
    Source: analysis.md §2, H2a; arxiv-2512-08825.md (CIEMAT-QI4X, β up to 4% demonstrated)

    Thermal efficiency:
    Stellaris uses WCLL blanket with EUROFER97 structural steel (550°C operating limit),
    constraining steam Rankine to ~500°C. Gross thermal efficiency ≈ 38% (lower than
    Helios's 40% which uses vanadium alloy at 635°C; analysis.md §3). Net plant efficiency
    ~32% (1,000 MWe / 3,100 MWth; analysis.md §5) after recirculating power deduction.

    iter-8 updates vs. iter-7 (review feedback PA-1 through F-3):
    CF-F1: Blanket/divertor replacement interval (1–4 yr from Queral et al. 2025,
        arxiv-2501-04640.md) added as a causal anchor for the 85–95% capacity factor lower
        bound. The 85% floor is now explicitly grounded in maintenance physics: at a 4-week
        outage per 1-year replacement interval, availability ceiling is ~92%; the 85% floor
        allows for more frequent or longer outages. Source: feedback.md F-1 (source integration);
        analysis.md §5 (Capacity Factor row, Blanket/divertor replacement interval row).
    CF-H2: H2 hypothesis baseline corrected from "conventional disruption-limited tokamak
        (83–85% CF)" to "HTS compact tokamak reference (01-hts-compact-tokamak)." The ARC-class
        reference employs active disruption prediction and may target 87–90% CF. If true, the
        Stellaris advantage at 88% CF shrinks to 0–1 percentage points — insufficient to offset
        the 3D coil manufacturing premium. H2 cannot be evaluated quantitatively until the 01
        analysis provides a comparable CF estimate. Key Assumption #2 updated accordingly.
        Source: feedback.md Carried-Forward F-1; analysis.md §2, H2.
    CF-CT: Construction time added explicitly as a sensitivity lever (elasticity +0.40, ranked
        third among engineering parameters). The machine scale penalty (R0 ≈ 13 m, 3D coil
        installation) plausibly extends the first-of-kind construction schedule vs. ARC-class
        compact tokamaks (R0 ≈ 3–4 m). A 20% schedule extension adds ~8% to LCOE through IDC
        (CAS60 is among the largest single cost accounts). Key Assumption #14 added.
        Source: feedback.md Carried-Forward F-2; analysis.md §2, Recommended Modeling Approach.
    CF-CAS21: CAS21 (Buildings) updated from "0 (neutral)" to "Small +" in Key Assumption #11.
        Site reuse (Gundremmingen) reduces land/permitting cost but not reactor building volume.
        A QI stellarator with R0 ≈ 13 m requires a substantially larger assembly/containment
        building than an ARC-class compact tokamak (R0 ≈ 3–4 m).
        Source: feedback.md Carried-Forward F-3; analysis.md §7 (CAS21 row).

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
_R0_V1 = 13.0   # m — UNCERTAIN: Stellaris v1 (2.76% beta)
_A_V1  =  1.30  # m — UNCERTAIN: minor radius; R0/a ≈ 10 assumed

# H2a geometry: 4% beta follow-on design — plasma volume scales to ~306 m³ (~31% less)
# "At 4% beta vs. 2.76%, plasma volume at fixed fusion power density scales down by ~31%"
# — analysis.md §2, H2a; confirmed by CIEMAT-QI4X (arXiv:2512.08825, β up to 4%)
# 20π²a³ = 306 → a ≈ 1.16 m, R0 ≈ 11.6 m (R0/a = 10 preserved)
_R0_H2A = 11.6  # m — UNCERTAIN: H2a higher-beta scenario [next-gen QI, not Stellaris v1]
_A_H2A  =  1.16 # m — UNCERTAIN: H2a minor radius

# ── Magnet replacement lifecycle constants ────────────────────────────────
# REBCO neutron fluence limit: ~3×10²² m⁻² → ~10 FPY at 2,700 MW fusion power.
# "The magnet system would have a lifetime of approximately 10 full power years at a
# fusion power of 2700 MW" — stellaris-design-details.md §2.8
# Two replacements over a 30-year plant life (at ~yr 10 and ~yr 20).
# Annualized replacement cost = (N_replacements × C220103) / lifetime_yr
# Annual energy output = P_net × availability × 8760 hr/yr
# Source: stellaris-design-details.md §2.8; analysis.md §5 (REBCO magnet lifetime row)
_PLANT_LIFE_YR     = 30      # years
_N_REPLACEMENTS    =  2      # replacements over plant life (yr ~10 and ~20)
_P_NET_MWE         = 1000.0  # MWe net output
_AVAILABILITY_BASE =  0.88   # capacity factor (central estimate; matches _SHARED below)


def _annual_energy_gwh(availability: float) -> float:
    """Annual energy output [GWh/yr] for a given capacity factor."""
    return _P_NET_MWE * availability * 8760.0 / 1e3


def _repl_lcoe(c220103_m: float, availability: float = _AVAILABILITY_BASE) -> float:
    """$/MWh contribution from periodic coil replacement (two replacements, 30-yr life)."""
    annual_repl_cost_m = (_N_REPLACEMENTS * c220103_m) / _PLANT_LIFE_YR  # M$/yr
    return annual_repl_cost_m * 1e6 / (_annual_energy_gwh(availability) * 1e3)  # $/MWh


# ── Shared forward-pass parameters ───────────────────────────────────────
# Used across scenarios to avoid duplication.
_SHARED = dict(
    # Net electrical: 1,000 MWe (Stellaris design target)
    # Source: dossier.md §Summary; stellaris-design-details.md Table 3
    net_electric_mw=1000.0,

    # Capacity factor: 88% (Helios analogue; disruption-free steady-state argument)
    # "enabling an 88% capacity factor" — helios-stellarator-comparison.md §2
    # W7-X demonstrated >97% experimental run-time; plant availability will be lower
    # due to scheduled blanket/divertor maintenance. Analysis range: 85–95%.
    # Lower bound calibration (CF-F1 iter-8): Queral et al. (2025) give blanket/divertor
    # replacement interval of ~1–4 years for stellarator reactors (HSR3 context).
    # At a 4-week outage per 1-year interval → availability ceiling ~92%; 85% floor
    # allows for more frequent or longer outages. Source: arxiv-2501-04640.md (abstract).
    # UNCERTAIN: Proxima has not published a Stellaris capacity factor target.
    # Source: analysis.md §5 (capacity factor row); analysis.md §2, H2;
    #         helios-stellarator-comparison.md §2; arxiv-2501-04640.md (replacement interval)
    availability=0.88,

    lifetime_yr=30,              # Standard 30-yr plant lifetime; DEFAULT
                                 # NOTE: REBCO magnet lifetime ~10 FPY at 2.7 GW (neutron
                                 # fluence limit 3×10²² m⁻²). Magnet replacement is a planned
                                 # lifecycle event — modeled separately below; NOT in CAS72.
                                 # Source: stellaris-design-details.md §2.8; analysis.md §5
    n_mod=1,                     # Single-module plant
    construction_time_yr=8.0,    # Stellarator default: complex 3D coil fabrication + assembly
                                 # Source: mfe_stellarator.yaml default
                                 # NOTE (CF-CT iter-8): construction_time_yr has elasticity
                                 # +0.40 — third-highest engineering lever. A 13 m major radius
                                 # machine with complex 3D non-planar coil installation likely
                                 # has a longer first-of-kind schedule than an ARC-class device
                                 # (R0 ≈ 3–4 m). IDC (CAS60) is among the largest single cost
                                 # accounts. A 20% schedule extension adds ~8% to LCOE.
                                 # Source: feedback.md CF-F2; analysis.md §2 (construction time)
    interest_rate=0.07,          # DEFAULT — standard capital cost rate
    inflation_rate=0.0245,       # DEFAULT
    noak=True,                   # NOAK central estimate

    # ── Geometry — Stellaris v1 (2.76% beta; see H2a scenario for 4% variant) ──
    # UNCERTAIN: major radius and plasma volume are blocking data gaps.
    # Source: analysis.md §6, Gap 2; stellaris-design-details.md Table 3 (power density)
    R0=_R0_V1,                   # [m] UNCERTAIN — derived from power density + fusion power
    plasma_t=_A_V1,              # [m] UNCERTAIN — derived minor radius; R0/a ≈ 10 assumed
    elon=1.0,                    # Near-circular cross-section; stellarator default
    blanket_t=0.60,              # DEFAULT — WCLL blanket thickness
    ht_shield_t=0.20,            # DEFAULT
    structure_t=0.15,            # DEFAULT
    vessel_t=0.10,               # DEFAULT

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

    eta_p=0.5,                   # DEFAULT pumping efficiency
    eta_pin=0.5,                 # DEFAULT ECRH wall-plug efficiency
                                 # Current gyrotron state: ~50%; >60% possible with
                                 # multi-stage depressed collectors (future improvement)
                                 # Source: stellaris-design-details.md §2 (gyrotron note)
    eta_de=0.85,                 # DEFAULT
    f_sub=0.03,                  # DEFAULT subsystem power fraction
    f_dec=0.0,                   # Thermal Rankine only; no direct energy conversion
                                 # Source: dossier.md §Energy Capture

    # Coil system power: 111 MW conduction load from Stellaris Table 3
    # Published as "Conduction power to coils" — nuclear heating + thermal conduction
    # into the coil structure. Treated as an electrical recirculating power contribution
    # alongside ECRH and BOP pumping (~161–211 MW total recirculating in steady-state).
    # UNCERTAIN: May be nuclear heating removed by an intermediate coolant loop
    # (not requiring full cryogenic COP penalty) rather than a direct cryogenic load.
    # NOTE: The coincidence of 111 GJ (stored magnetic energy) and 111 MW (conduction power)
    # in Table 3 may reflect a transcription artifact — both values sourced independently.
    # Source: stellaris-design-details.md Table 3; analysis.md §5 (recirculating breakdown)
    p_coils=111.0,               # [MW] from Table 3; much larger than tokamak default (2–3 MW)

    # WCLL coolant pumping: analysis.md §5 estimates ~50 MW total BOP pumping
    # (PbLi primary loop + water secondary loop in WCLL blanket).
    # Split: p_cool = 40 MW primary pumping, p_pump = 10 MW auxiliary.
    # Source: analysis.md §5 (recirculating power breakdown: "pumping ~50 MW")
    p_cool=40.0,                 # [MW] WCLL primary pumping (PbLi + water); analysis.md §5
    p_pump=10.0,                 # [MW] auxiliary pumping; analysis.md §5

    p_trit=10.0,                 # DEFAULT tritium processing power [MW]; WCLL PbLi extraction
    p_house=4.0,                 # DEFAULT housekeeping power [MW]

    # Cryogenic power: HTS coils at 20–40 K; upgraded from default 0.8 MW
    # Large coil system (111 GJ stored energy) requires larger cryo infrastructure.
    # Source: stellaris-design-details.md Table 3 (111 GJ stored magnetic energy);
    #         mfe_stellarator.yaml default 0.8 MW
    p_cryo=2.0,                  # [MW] upgraded from 0.8 MW default for larger coil system
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
    p_input=5.0,                 # [MW] H4-true: ignited; Helios analogue ~1 MW
                                 # Source: helios-stellarator-comparison.md §3.1
    **_SHARED,
    # No cost overrides: no published Stellaris cost data.
    # C220103 (coils) = framework default = LOWER BOUND.
    # analysis.md §7: stellarator C220103 is 1.5–5× the tokamak reference (Brown 2018).
    # Source: analysis.md §2, Challenge 1; §7 (C220103 row)
)

# ── Results — Scenario A ──────────────────────────────────────────────────

c_a  = result_h4true.costs
pt_a = result_h4true.power_table
_c220103_base = float(result_h4true.cas22_detail.get("C220103", 0.0))
_repl_a = _repl_lcoe(_c220103_base)

print("QI Stellarator — HTS (Proxima Fusion Stellaris) — 1 GWe, NOAK")
print("Scenario A: H4-true (ignited, 5 MW ECRH steady-state), 88% capacity factor")
print(f"LCOE (initial-build only):     {c_a.lcoe:.1f} $/MWh  [LOWER BOUND — excl. coil replacement]")
print(f"LCOE (replacement-inclusive):  {c_a.lcoe + _repl_a:.1f} $/MWh  [2 coil replacements, DEFAULT C220103]")
print(f"Overnight cost: {c_a.overnight_cost:.0f} $/kW | Fusion: {pt_a.p_fus:.0f} MW | Net: {pt_a.p_net:.0f} MW | Q_eng: {pt_a.q_eng:.1f}")
print(f"NOTE: C220103 coil cost uses framework defaults (wound-coil calibration — LOWER BOUND;")
print(f"      3D non-planar manufacturing premium not modeled; see Key Assumptions #3 and sweep)")
print(f"NOTE: Framework calibrated to ARIES-CS (QA stellarator); Stellaris is QI — topology")
print(f"      difference may affect C220103 coil account; direction of bias unknown. (Assumption #13)")
print(f"NOTE: CAS22 (${float(c_a.cas22):.0f} M) contains coils at C220103 and heating at C220104.")
print(f"      CAS21 (${float(c_a.cas21):.0f} M) = Buildings only, per ARIES CAS20X convention.")
print(f"      CAS21 rated 'Small +' vs. HTS compact tokamak reference (R0≈3–4 m) due to larger")
print(f"      reactor building footprint at R0≈13 m (partially offset by Gundremmingen site reuse).")
print(f"      Source: analysis.md §7, CAS account structure note; feedback.md CF-CAS21.")
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
        note = "[DEFAULT — LOWER BOUND; 3D manufacturing premium not modeled]"
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
# analysis.md §2, Challenge 3: "It is unclear whether this 50 MW is a conservative
# operational assumption or reflects that Stellaris does not reach full ignition."
# Source: stellaris-design-details.md Table 3; analysis.md §2, H4

result_h4false = model.forward(
    p_input=50.0,                # [MW] per stellaris-design-details.md Table 3 (stated value)
    **_SHARED,
)

cf  = result_h4false.costs
ptf = result_h4false.power_table

print(f"\nScenario B: H4-false (50 MW sustained ECRH; per Stellaris Table 3 stated value)")
print(f"  LCOE (initial-build):        {cf.lcoe:.1f} $/MWh | Overnight: {cf.overnight_cost:.0f} $/kW")
print(f"  LCOE (replacement-incl.):    {cf.lcoe + _repl_a:.1f} $/MWh [same coil cost, DEFAULT C220103]")
print(f"  Fusion: {ptf.p_fus:.0f} MW | Net: {ptf.p_net:.0f} MW | Q_eng: {ptf.q_eng:.1f}")
print(f"  LCOE delta vs. Scenario A (initial-build): {cf.lcoe - c_a.lcoe:+.1f} $/MWh")
print(f"  Source: stellaris-design-details.md Table 3 (H&CD column); analysis.md §2, H4")

# ── Scenario H2a: Higher-beta QI design (4% beta, smaller machine) ───────
# [next-gen QI, not Stellaris v1]
# CIEMAT-QI4X (arXiv:2512.08825, December 2025) demonstrates a QI stellarator
# configuration maintaining all key properties (island divertor compatibility, alpha
# confinement, small bootstrap current) at beta up to 4% — ~45% above Stellaris v1.
# "CIEMAT-QI4X has a 4/4 island chain at the edge that is resilient at least up to
# β=4%, even when the bootstrap current is included" — arxiv-2512-08825.md, abstract
#
# This is a SCENARIO BRANCH for next-generation QI designs. It is NOT a variant of
# Stellaris v1 (which targets 2.76% beta). Proxima has stated "more commercially
# attractive designs are possible" — this scenario quantifies the machine size reduction
# that would follow from a 4% beta operating point.
#
# Geometry at 4% beta (H4-true ECRH assumption):
# Plasma volume scales linearly: V_H2a = 443 × (2.76/4.0) ≈ 306 m³ (~31% reduction)
# R0 ≈ 11.6 m, a ≈ 1.16 m (R0/a = 10 preserved)
# Source: analysis.md §2, H2a; arxiv-2512-08825.md; proxima-fusion-technology-page.md

_SHARED_H2A = {k: v for k, v in _SHARED.items()}
_SHARED_H2A["R0"]       = _R0_H2A   # [m] H2a: 4% beta scenario; analysis.md §2, H2a
_SHARED_H2A["plasma_t"] = _A_H2A    # [m] H2a minor radius; ~31% smaller plasma volume

result_h2a = model.forward(
    p_input=5.0,                 # [MW] H4-true assumed (ignited, as Scenario A)
    **_SHARED_H2A,
)

c_h2a  = result_h2a.costs
pt_h2a = result_h2a.power_table
_c220103_h2a = float(result_h2a.cas22_detail.get("C220103", 0.0))
_repl_h2a = _repl_lcoe(_c220103_h2a)

print(f"\nScenario H2a: Higher-Beta QI (4% Beta, R0≈{_R0_H2A} m, Smaller Machine)"
      f" [next-gen QI, not Stellaris v1]")
print(f"  LCOE (initial-build):        {c_h2a.lcoe:.1f} $/MWh | Overnight: {c_h2a.overnight_cost:.0f} $/kW")
print(f"  LCOE (replacement-incl.):    {c_h2a.lcoe + _repl_h2a:.1f} $/MWh [DEFAULT C220103]")
print(f"  Fusion: {pt_h2a.p_fus:.0f} MW | Net: {pt_h2a.p_net:.0f} MW | Q_eng: {pt_h2a.q_eng:.1f}")
print(f"  LCOE delta vs. Scenario A (initial-build): {c_h2a.lcoe - c_a.lcoe:+.1f} $/MWh")
print(f"  Source: analysis.md §2, H2a; arxiv-2512-08825.md (CIEMAT-QI4X beta ceiling 4%)")
print(f"  NOTE: C220103 coil cost still LOWER BOUND; 3D premium not modeled in this scenario.")
print(f"  NOTE: This scenario represents a future QI design lineage, NOT a Stellaris v1 variant.")
print(f"        Do not interpret H2a as the upper end of a Stellaris design range.")

# ── Coil cost multiplier sweep (3D manufacturing premium) ────────────────
# C220103 in Scenario A reflects wound-coil (tokamak-style) framework defaults.
# The actual Stellaris coil cost is 1.5–5× that reference (Brown 2018; analysis.md §7).
# This sweep shows the LCOE sensitivity to the 3D HTS coil manufacturing premium —
# the single most important unknown for Stellaris competitiveness.
# Replacement-inclusive LCOE is reported for each multiplier point, making the total
# lifecycle cost visible for cross-concept comparison.
# Source: analysis.md §2, Challenge 1; §7 (C220103 row); analysis.md §2, H1;
#         analysis.md §7 (footnote: "omitting replacement biases cross-concept comparison")

print(f"\nCoil cost multiplier sweep (C220103 3D manufacturing premium):")
print(f"Base C220103 (framework default): {_c220103_base:.0f} M$ (wound-coil calibration)")
print(f"Source: analysis.md §7 (C220103 row); Brown (2018) IEEE TPS; analysis.md §2, H1")
print(f"{'Multiplier':<14} {'C220103 (M$)':>14} {'Init. LCOE':>12} {'Repl $/MWh':>12} {'Incl.Repl LCOE':>16}")
print("-" * 72)

for mult in [1.0, 1.5, 2.5, 5.0]:
    _c220103_override = round(_c220103_base * mult, 1)
    _repl = _repl_lcoe(_c220103_override)
    _r = model.forward(
        p_input=5.0,
        cost_overrides={"C220103": _c220103_override},
        **_SHARED,
    )
    _label = "DEFAULT" if mult == 1.0 else f"{mult}×"
    print(f"  {_label:<12} {_c220103_override:>14.0f} {float(_r.costs.lcoe):>11.1f}"
          f" {_repl:>11.1f}  {float(_r.costs.lcoe) + _repl:>14.1f}")

print("  (1.5× = optimistic; 5× = pessimistic; SMC demo 2027 = first data point)")
print("  Replacement-inclusive LCOE is the economically complete figure for cross-concept")
print("  comparison. The initial-build figure does not appear in the compact HTS tokamak")
print("  reference on the same 10-yr coil replacement schedule.")
print("  Source: analysis.md §2, H1 (H1: premium < 2× is viability threshold);")
print("          stellaris-design-details.md §2.8 (REBCO fluence limit → ~10 FPY at 2,700 MW)")

# ── Capacity factor range sweep ───────────────────────────────────────────
# Sensitivity shows availability elasticity of −0.89 — the dominant engineering lever.
# The published range is 85–95% (analysis.md §5). The LCOE consequence of this range
# is comparable in magnitude to the H4 branching effect ($3.9/MWh) and must be
# explicit, not only derivable from elasticity × range width.
# Three points: 85% (floor — blanket/divertor maintenance limits), 88% (central —
# Helios analogue), 95% (optimistic — disruption-free + high-availability blanket).
# Scenario A (H4-true, 5 MW ECRH), DEFAULT C220103 coil cost.
#
# CF-F1 iter-8 note: blanket/divertor replacement interval calibration:
# Queral et al. (2025) arxiv-2501-04640.md — "blankets and divertor modules will have
# to be replaced periodically (about each 1–4 years depending on the design)." At a
# 4-week outage per 1-year interval, availability ceiling ~92%; 4-week per 4-year
# interval gives ~98%. The 85% floor accommodates more frequent or longer outages.
# Source: review.md §PA-1; analysis.md §5 (capacity factor row); analysis.md §2, H2;
#         helios-stellarator-comparison.md §2; en-wiki-wendelstein-7-x.md (>97% run-time);
#         arxiv-2501-04640.md (blanket replacement interval, CF-F1 iter-8)

print(f"\nCapacity factor range sweep (Scenario A — H4-true, DEFAULT C220103):")
print(f"Source: analysis.md §5 (range 85–95%); availability elasticity = −0.89")
print(f"CF-F1: Lower bound (85%) calibrated to ~1–4 yr blanket replacement interval")
print(f"       (Queral et al. 2025; arxiv-2501-04640.md abstract)")
print(f"{'CF':<8} {'Init. LCOE':>12} {'Repl $/MWh':>12} {'Incl.Repl LCOE':>16}  {'Note'}")
print("-" * 72)

_cf_cases = [
    (0.85, "floor (maintenance limits; ~1-yr replacement interval)"),
    (0.88, "central — Helios analogue"),
    (0.95, "optimistic — disruption-free"),
]
for _cf, _cf_note in _cf_cases:
    _shared_cf = {k: v for k, v in _SHARED.items()}
    _shared_cf["availability"] = _cf
    _r_cf = model.forward(p_input=5.0, **_shared_cf)
    _repl_cf = _repl_lcoe(_c220103_base, availability=_cf)
    print(f"  {_cf:.0%}   {float(_r_cf.costs.lcoe):>11.1f} {_repl_cf:>11.1f}  "
          f"{float(_r_cf.costs.lcoe) + _repl_cf:>14.1f}  {_cf_note}")

print("  UNCERTAIN: Proxima has not published a Stellaris capacity factor target.")
print("  The 85–95% range comes from the Helios analogue (88%), W7-X experimental run-time")
print("  (>97%, plant lower due to scheduled maintenance), and the disruption-free argument.")
print("  This sweep is the primary continuous LCOE lever; coil cost defines viability envelope.")
print("  Source: analysis.md §5 (capacity factor row); analysis.md §2, H2 (viability threshold)")
print()
print("  CF-H2 iter-8 NOTE: H2 viability threshold must be evaluated against the actual HTS")
print("  compact tokamak reference CF (01-hts-compact-tokamak), NOT a conventional disruption-")
print("  limited tokamak (~83–85%). ARC-class designs employ active disruption prediction;")
print("  if the 01 reference achieves 87–90% CF, the Stellaris advantage at 88% shrinks to")
print("  0–1 percentage points — insufficient to offset the 3D coil manufacturing premium.")
print("  H2 gate cannot be evaluated quantitatively until the 01 analysis provides a")
print("  comparable CF estimate. Source: feedback.md CF-H2; analysis.md §2, H2.")

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
   CF-F1 (iter-8): Lower bound (85%) is now causally grounded in the blanket/divertor
   replacement interval of ~1–4 years (Queral et al. 2025; arxiv-2501-04640.md, abstract;
   HSR3 context). At a 4-week outage per 1-year interval → ~92% ceiling; 85% floor
   accommodates more frequent or longer outages. This is a general stellarator reactor
   constraint, not Stellaris-specific.
   CF-H2 (iter-8): CRITICAL — the H2 viability threshold is relative to the HTS compact
   tokamak reference (01-hts-compact-tokamak / CFS ARC-class), NOT to a conventional
   disruption-limited tokamak. If the ARC-class reference targets 87–90% CF (via active
   disruption prediction and avoidance), Stellaris's 88% advantage is 0–1 percentage
   points — insufficient to offset the 3D coil manufacturing premium. The H2 gate cannot
   be evaluated quantitatively until the 01 analysis provides a comparable CF estimate.
   UNCERTAIN: Proxima has not published a capacity factor target for Stellaris.
   Source: analysis.md §5 (capacity factor row); analysis.md §2, H2;
           helios-stellarator-comparison.md §2; arxiv-2501-04640.md (replacement interval);
           feedback.md CF-F1, CF-H2.

3. C220103 (coils) — LOWER BOUND; 3D manufacturing premium NOT modeled [PRIMARY CAVEAT]
   Framework C220103 defaults calibrate to wound-coil (tokamak-style) geometry.
   Stellaris uses complex 3D non-planar HTS coils — no commercial manufacturing precedent.
   analysis.md §7 (citing Brown 2018 IEEE TPS): stellarator coil cost is 1.5–5× the
   equivalent wound-coil tokamak reference. The framework output is the lower end of this
   range. The coil multiplier sweep above brackets the competitive uncertainty:
     - H1 (analysis.md §2): premium < 2× per kAm is the viability threshold. If false
       (>2×), stellarator CAPEX is unlikely to be competitive against compact HTS tokamaks
       regardless of capacity factor advantage.
     - First real data point: Stellarator Model Coil (SMC) demo targeted for 2027.
   Source: analysis.md §2, Challenge 1, H1; §7 (C220103 row); Brown (2018) IEEE TPS.

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

9. Magnet replacement lifecycle cost: modeled separately (NOT in CAS72)
   REBCO neutron fluence limit: 3×10²² m⁻² → ~10 full-power years at 2,700 MW.
   "The magnet system would have a lifetime of approximately 10 full power years at a
   fusion power of 2700 MW" — stellaris-design-details.md §2.8.
   At least two magnet replacements are required over a 30-yr plant lifetime. This adds a
   deferred CAPEX component unique among the concepts analyzed (coil replacement at scale
   not shared by compact HTS tokamaks on the same fluence timeline).
   Annualized replacement cost = (2 × C220103) / 30 yr = C220103 / 15 yr.
   CAS72 (framework sub-account) models blanket/divertor replacement only (C220101 +
   C220108) — coil replacement must be computed and reported separately.
   The replacement-inclusive LCOE is the economically complete figure; the initial-build
   LCOE omits a stellarator-specific lifecycle cost and biases cross-concept comparison.
   Source: stellaris-design-details.md §2.8; analysis.md §5 (REBCO magnet lifetime row);
           analysis.md §7 (Cross-Concept Notes, final table footnote).

10. CAS account structure (ARIES CAS20X convention):
    CAS22 = Reactor Plant Equipment super-account (contains ALL nuclear island sub-accounts).
    C220103 (coils) and C220104 (heating) are sub-accounts within CAS22 — not at CAS21.
    CAS21 = Buildings and site improvements (not magnets).
    This differs from PROCESS-style numbering where magnets may appear at a top-level CAS.
    Source: analysis.md §7 (CAS account structure note); costing_constants.yaml.

11. CAS-level directional deltas vs. 01-hts-compact-tokamak reference (analysis.md §7):
    C220103 (coils, within CAS22): Large +  (1.5–5×; Brown 2018; 3D coil geometry premium)
    C220104 (H&CD / ECRH, CAS22): Large −  (−50 to −80%; conditional on H4 = true)
    C220101 (first wall / blanket): Small +  (5–15%; 3D tungsten tile fabrication premium)
    CAS24 (heat transport):         Small −  (~−10%; WCLL water cooling vs. FLiBe)
    CAS25 (power conversion):       Small −  (~−5–10%; water Rankine cheaper per GWth than
                                    sCO₂ Brayton, partially offset by larger thermal throughput
                                    at lower efficiency — direction could be neutral)
    CAS21 (Buildings):              Small +  (CF-CAS21 iter-8): reactor building volume scales
                                    with machine footprint — a QI stellarator at R0≈13 m requires
                                    a substantially larger containment and assembly building than
                                    an ARC-class compact tokamak (R0≈3–4 m). Gundremmingen site
                                    reuse reduces land acquisition and permitting cost but not
                                    reactor building volume. Net: Small + (not neutral as in iter-7).
                                    Source: feedback.md CF-CAS21; analysis.md §7 (CAS21 row).
    O&M (CAS70):                    Structural + (direction only; magnitude unknown): stellarator
                                    coil geometry structurally limits blanket and divertor module
                                    size relative to tokamaks — "relatively small ports for in-vessel
                                    access and maintenance, i.e. in comparison with tokamaks"
                                    (Queral et al. 2025; arxiv-2501-04640.md, abstract). This is a
                                    generic consequence of modular stellarator coil architecture,
                                    not a Stellaris-specific design choice.
                                    Source: feedback.md CF-F2; analysis.md §7 (O&M delta paragraph).
    Net: uncertain; competitiveness depends on C220103 premium vs. H&CD saving + CF advantage.

12. Scenario H2a: next-generation QI design branch — NOT a Stellaris v1 variant
    CIEMAT-QI4X (arXiv:2512.08825) demonstrates 4% beta feasibility in a QI configuration.
    Proxima stated "more commercially attractive designs are possible" — H2a quantifies
    the machine size reduction (−31% plasma volume) from moving to 4% beta.
    H2a uses the same D-T fuel, HTS REBCO, and H4-true (ignited) ECRH assumption.
    In cross-concept comparison tables, H2a represents a different design generation from
    Stellaris v1 and should not be used as the upper bound of a Stellaris range.
    Source: analysis.md §2, H2a; arxiv-2512-08825.md; review.md §PA-3.

13. Framework calibration: ARIES-CS (QA stellarator) applied to QI configuration
    The 1costingfe stellarator cost baseline is calibrated to ARIES-CS, which studied
    quasi-axisymmetric (QA) stellarator configurations. Stellaris is quasi-isodynamic (QI).
    These two symmetry classes may have different coil topology costs: QI requires
    specific non-planar winding laws that differ from QA optimized coils. The direction
    and magnitude of this cost bias are unknown — it may inflate or deflate C220103
    relative to the actual QI coil cost.
    This caveat appears in analysis.md §1 and propagates into C220103 uncertainty.
    The Brown (2018) multiplier range (1.5–5×) accounts for stellarator vs. tokamak geometry
    but does not separately model QA vs. QI topology differences.
    Source: analysis.md §1 (ARIES-CS discussion); review.md §PA-2; Brown (2018) IEEE TPS.

14. Construction time: 8 years (framework default; elasticity +0.40) [CF-CT iter-8]
    Construction_time_yr has the third-highest engineering elasticity (+0.40), ranking above
    R0 (+0.31). IDC (CAS60) is among the largest single cost accounts — a 20% schedule
    extension adds ~8% to LCOE. The 8-year stellarator default is conceptually plausible
    for a 13 m major radius machine requiring complex 3D coil fabrication and precision
    installation, versus an ARC-class compact tokamak (R0≈3–4 m) which may target 6–7 yr.
    Construction time is the financial expression of the machine scale penalty: the low-beta
    scale penalty (Challenge 2) propagates not just into nuclear island capital accounts but
    also into the construction schedule, which compounds the cost through IDC.
    No Stellaris-specific construction schedule has been published. The 8-year default is
    used without override; sensitivity to this parameter is visible in the model's autodiff.
    Source: feedback.md CF-CT; analysis.md §2 (Recommended Modeling Approach, sensitivity
            parameter list); mfe_stellarator.yaml (default construction_time_yr=8.0).
""")

# ── Sensitivity Analysis ──────────────────────────────────────────────────
# Uses JAX autodiff on the Scenario A (H4-true) result parameters.
# Availability elasticity ~−0.89 is the dominant lever; confirms capacity factor sweep
# results are the primary optimization target within a viable design.
# Construction_time_yr ranks third at +0.40 (CF-CT iter-8: now explicitly noted in
# Key Assumptions #14 and analysis.md §2 sensitivity parameter list).
# Source: analysis.md §2, Sensitivity Axes (primary continuous parameter = availability)

sens = model.sensitivity(result_h4true.params)

print("Sensitivity (elasticity = %LCOE / %param) — Scenario A (H4-true)")
print("-" * 48)

print("\nEngineering levers:")
for k, v in sorted(sens["engineering"].items(), key=lambda x: abs(x[1]), reverse=True):
    print(f"  {k:<28} {v:+.4f}")

print("\nFinancial:")
for k, v in sorted(sens["financial"].items(), key=lambda x: abs(x[1]), reverse=True):
    print(f"  {k:<28} {v:+.4f}")
