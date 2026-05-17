"""Planar Coil Stellarator (Thea Energy — Helios) LCOE Model Setup.

Usage:
    uv run python model_setup.py              # print results to terminal
    uv run python model_setup.py | tee model_output.txt  # also save for synthesis stage

Modeling approach:
    costingfe STELLARATOR/DT concept. Parameters are taken directly from the
    Helios preconceptual design (arXiv:2512.08027), DOE-certified January 2026.
    Cost accounts use framework defaults throughout — Thea Energy has published
    no bottom-up capital cost breakdown; only an asserted LCOE target range
    ($150/MWh FOAK → $60/MWh at scale) is available in public sources.

Concept choice rationale:
    Helios is a quasi-axisymmetric (QA), 2-field-period stellarator operating
    in steady-state. ConfinementConcept.STELLARATOR is the correct mapping.
    The planar coil innovation (324 individually-controlled REBCO shaping coils)
    lowers manufacturing complexity per coil vs. conventional 3D stellarators
    but increases total coil count and control infrastructure complexity — net
    effect on capital cost is highly uncertain without a published cost account.

Key deviations from stellarator defaults:
    - R0=8.0m, plasma_t=1.8m (Helios is larger than the 5.5m/1.8m defaults)
    - eta_th=0.40 (three-stage steam Rankine at 635°C; default=0.46 is optimistic)
    - p_input=1.0 MW (ignited plasma; only 1 MW operational ECRH for impurity control)
    - p_cryo=15.0 MW (UNCERTAIN: 336 REBCO coils at 20 K is the dominant auxiliary load)
    - availability=0.88 (Helios states 88%; biennial 84-day maintenance cycle)
    - noak=False (FOAK: first plant is the modeled scenario per $150/MWh target)
    - f_dec=0.0 (pure steam Rankine; no direct energy conversion)
"""

from costingfe import ConfinementConcept, CostModel, Fuel

# ── Model Initialization ─────────────────────────────────────────────────────
model = CostModel(concept=ConfinementConcept.STELLARATOR, fuel=Fuel.DT)

# ── Shared kwargs (native 390 MWe and scaled 1 GWe forward calls) ────────────
# All values sourced from analysis.md §Section 5 unless noted.
# Sources:
#   [A] analysis.md §Section 5: LCOE-Relevant Parameters table
#   [B] thea-energy-helios-arxiv-2512-08027.md (Helios preconceptual design)
#   [C] analysis.md §Section 2 (challenges) and §Section 5 (missing params)
#   [D] steady_state_stellarator.yaml framework defaults (where no Helios data exists)

_SHARED_KWARGS = dict(
    # ── Plant requirements ──────────────────────────────────────────────────
    availability=0.88,       # DEVIATION: from canonical 0.85 (MCF steady-state, D-T) per
                             #   scoring_framework.md §"Plant availability".
                             # Source: [A] analysis.md §Section 5 ("Capacity factor: 88%"),
                             #   citing [B] thea-energy-helios-arxiv-2512-08027.md §Operations.
                             # Basis: published 84-day biennial maintenance cycle for the
                             #   Helios/Thea Energy QA stellarator preconceptual design.
    lifetime_yr=40,          # DEVIATION: per scoring_framework.md §"Plant lifetime"
                             #   (canonical 30 yr). Sourced design life: [A] "Magnet
                             #   design lifetime: 40+ years" [B §Magnets], Helios/Thea
                             #   Energy QA stellarator preconceptual design.
    n_mod=1,                 # Single-module plant
    construction_time_yr=8.0,  # DEFAULT [D]: no Helios-specific timeline published;
                               # UNCERTAIN: planar coil winding is simpler than 3D coils
                               # but FOAK complexity keeps estimate at 8 yr
    interest_rate=0.07,      # DEFAULT: standard LCOE financial assumption
    inflation_rate=0.0245,   # DEFAULT: standard LCOE financial assumption
    noak=False,              # FOAK: first-plant scenario; Thea LCOE target is $150/MWh
                             # for first plant [A: "LCOE target (first plant): $150/MWh"]

    # ── Helios geometry ─────────────────────────────────────────────────────
    # Source: thea-energy-helios-arxiv-2512-08027.md §Plasma & Configuration
    R0=8.0,                  # [A] "Major radius: 8 m"
    plasma_t=1.8,            # [A] "Minor radius: 1.8 m" (aspect ratio 4.5)
    elon=1.0,                # QA stellarator ≈ circular cross-section [B §Plasma & Configuration]
    blanket_t=0.50,          # [B §Blanket & Tritium Breeding] "50 cm blanket thickness"
    ht_shield_t=0.20,        # DEFAULT [D]: no Helios-specific shield thickness published
    structure_t=0.15,        # DEFAULT [D]
    vessel_t=0.10,           # DEFAULT [D]

    # ── Power balance ────────────────────────────────────────────────────────
    # Helios is effectively ignited (Q_plasma ≈ 958) [A: "Plasma gain: ~958"]
    # Total thermal: 1,094 MW; gross electric: 438 MWe; net: 390 MWe [A]
    # Total facility/auxiliary load: ~48 MWe [A: "Auxiliary / facility power: ~48 MWe"]
    p_input=1.0,             # [A] "Operational ECRH power: 1 MW" — impurity control only;
                             #      plasma self-heats via alpha particles; 10 MW ECRH only
                             #      at startup [B §Heating]; plasma is ignited (Q~958)
    mn=1.1,                  # DEFAULT [D]: standard D-T neutron energy multiplier
    eta_th=0.35,              # standardized from 0.4 per scoring_framework.md (Energy Capture: Thermal (steam))
                             #        superheated steam [B §Energy Conversion];
                             #        slightly below default 0.46 (Helios-specific value)
    eta_p=0.5,               # DEFAULT [D]: pumping efficiency
    eta_pin=0.5,             # DEFAULT [D]: ECRH gyrotron wall-plug efficiency
                             #               (standard for 170 GHz ITER-spec gyrotrons)
    eta_de=0.85,             # DEFAULT [D]: DEC efficiency; unused (f_dec=0.0)
    f_sub=0.03,              # DEFAULT [D]: miscellaneous subsystem fraction; bulk of
                             #               48 MWe facility load captured in p_xxx below
    f_dec=0.0,               # Pure steam Rankine; no DEC [A: recirculating power is
                             #               parasitic only]

    # Individual auxiliary loads — components of the 48 MWe facility total [A]
    p_coils=2.0,             # UNCERTAIN: 324 individually addressable HTS power supply
                             #             units; REBCO has negligible resistive loss but
                             #             supply electronics have losses; no published
                             #             figure [C §S5 gap: coil MTBF]
    p_cool=8.0,              # UNCERTAIN: helium blanket loop blowers + heat exchangers
                             #             (He→steam IHX); He-cooled primary loop is less
                             #             well-characterized than H₂O; no published
                             #             breakdown [C §S3: He coolant BOP]
    p_pump=3.0,              # UNCERTAIN: LiPb circulation at 6.6 cm/s [B §Blanket];
                             #             estimated from MHD-limited flow against ~6T
                             #             field; derivable but not published [C §S5 gap #14]
    p_trit=10.0,             # DEFAULT [D]: tritium extraction and processing
                             #               (~300 g/day at 958 MW fusion, 5% burn fraction)
    p_house=5.0,             # UNCERTAIN: facility controls + 450+ variable real-time
                             #             control system + HVAC + instrumentation;
                             #             slightly above 4 MW default given software-
                             #             intensive 324-coil infrastructure [C §S2 Ch. 4]
    p_cryo=15.0,             # UNCERTAIN: 336 REBCO coils at 20 K [A/B §Magnets];
                             #             Carnot COP at 20 K ≈ 0.07 → large refrigeration
                             #             demand; analysis.md §S5 gap #14 estimates
                             #             "5–15 MWe"; using 15 MW (upper bound)
)

# ── Native 390 MWe forward run (FOAK reference case) ─────────────────────────
# Helios design point: 390 MWe net to grid.
# Source: thea-energy-helios-arxiv-2512-08027.md §Power Balance
result = model.forward(net_electric_mw=390.0, **_SHARED_KWARGS)

# ── Self-consistent 1 GWe result (cross-concept comparison) ──────────────────
# Helios native 390 MWe is below the 1 GWe reference standard.
# override_reference_mw tells the framework that _SHARED_KWARGS are valid at 390 MWe
# and to scale to 1000 MWe using per-account scaling laws.
result_1gw = model.forward(
    net_electric_mw=1000.0,
    override_reference_mw=390.0,
    **_SHARED_KWARGS,
)

# ── Cost Results ─────────────────────────────────────────────────────────────
c  = result.costs
pt = result.power_table

print("Planar Coil Stellarator (Thea Energy Helios) — FOAK, 390 MWe net, 88% availability")
print(f"LCOE: {c.lcoe:.1f} $/MWh | Overnight: {c.overnight_cost:.0f} $/kW")
print(f"Fusion: {pt.p_fus:.0f} MW | Net: {pt.p_net:.0f} MW | Q_eng: {pt.q_eng:.1f}")
print(f"  (Helios targets: LCOE $150/MWh FOAK → $60/MWh at scale)")
print()

# ── CAS Cost Breakdown ────────────────────────────────────────────────────────
cas = [
    ("CAS10", "Preconstruction",            c.cas10),
    ("CAS21", "Buildings",                  c.cas21),
    ("CAS22", "Reactor Plant Equipment",    c.cas22),
    ("CAS23", "Turbine Plant",              c.cas23),
    ("CAS24", "Electrical Plant",           c.cas24),
    ("CAS25", "Miscellaneous",              c.cas25),
    ("CAS26", "Heat Rejection",             c.cas26),
    ("CAS27", "Special Materials",          c.cas27),
    ("CAS28", "Digital Twin",               c.cas28),
    ("CAS29", "Contingency",                c.cas29),
    ("CAS30", "Indirect Costs",             c.cas30),
    ("CAS40", "Owner's Costs",              c.cas40),
    ("CAS50", "Supplementary",              c.cas50),
    ("CAS60", "IDC",                        c.cas60),
    ("CAS70", "O&M (annualized)",           c.cas70),
    ("CAS80", "Fuel (annualized)",          c.cas80),
    ("CAS90", "Financial",                  c.cas90),
]

print(f"{'Code':<8} {'Account':<28} {'M$':>10}")
print("-" * 48)
for code, name, val in cas:
    print(f"{code:<8} {name:<28} {float(val):>10.1f}")
print("-" * 48)
print(f"{'':8} {'Total Capital':<28} {float(c.total_capital):>10.1f}")

# ── CAS22 Sub-account Detail ──────────────────────────────────────────────────
print("\nCAS22 Sub-accounts (Reactor Plant Equipment):")
print(f"{'Code':<12} {'Account':<32} {'M$':>8}  {'Note'}")
print("-" * 76)

cas22_labels = {
    "C220101": "First Wall + LiPb Blanket",
    "C220102": "Shield",
    "C220103": "Coils (336 planar REBCO)",
    "C220104": "Heating System (ECRH)",
    "C220105": "Primary Structure",
    "C220106": "Vacuum Vessel",
    "C220107": "Power Supplies",
    "C220108": "Divertor (novel QA X-point)",
    "C220109": "DEC",
    "C220111": "Installation",
    "C220112": "Isotope Separation",
    "C220200": "Coolant (He primary loop)",
    "C220300": "Aux Cooling",
    "C220400": "Rad Waste",
    "C220500": "Fuel Handling (tritium)",
    "C220600": "Other Equipment",
    "C220700": "I&C",
}
overridden = set(result.overridden) if hasattr(result, "overridden") else set()
for code, label in cas22_labels.items():
    val = result.cas22_detail.get(code, 0.0)
    note = "[OVERRIDE]" if code in overridden else "[DEFAULT]"
    print(f"{code:<12} {label:<32} {float(val):>8.1f}  {note}")
print("-" * 76)
total22 = result.cas22_detail.get("C220000", float(c.cas22))
print(f"{'C220000':<12} {'TOTAL':<32} {float(total22):>8.1f}")

# ── Key Assumptions Summary ────────────────────────────────────────────────────
print("""
Key Assumptions
===============
1. Net electric output: 390 MWe native (Helios design point).
   Source: thea-energy-helios-arxiv-2512-08027.md §Power Balance.
   Cross-concept: result_1gw scales to 1000 MWe using per-account scaling laws.

2. Availability: 88% — maintenance-limited; biennial 84-day sector-based cycle.
   Source: thea-energy-helios-arxiv-2512-08027.md §Operations.
   Uncertainty: 88% stated without supporting availability model; coil control
   failure modes could reduce effective availability [analysis.md §S2 Challenge 4].

3. Physics: ISS04 H_ISS04 = 1.4 sustained (central challenge — not demonstrated
   in any QA stellarator; W7-X achieved ~1.3–1.4 only in QI configuration).
   If H_ISS04 = 1.2 in practice, fusion power could drop 30–50%.
   Eos (first plasma 2030) is the experimental validation path.
   Source: analysis.md §S2 Challenge 1; thea-energy-helios-arxiv-2512-08027.md §Plasma.

4. Thermal efficiency: eta_th = 0.40 (three-stage steam Rankine, 635°C superheated
   steam, 40.2% gross efficiency). Helios-specific; default 0.46 is too optimistic.
   Source: thea-energy-helios-arxiv-2512-08027.md §Energy Conversion.

5. Heating: p_input = 1 MW operational ECRH only (impurity control). Plasma is
   ignited (Q~958). 10 MW startup ECRH is transient — not counted in steady-state.
   Source: thea-energy-helios-arxiv-2512-08027.md §Heating.

6. Cryogenics: p_cryo = 15 MW UNCERTAIN (upper-bound estimate for 336 REBCO coils
   at 20 K; Carnot COP ~0.07; analysis.md §S5 gap #14 estimates 5–15 MWe).
   Source: analysis.md §S2 Challenge 4; §S5 gap #14.

7. Magnet system: 12 encircling + 324 shaping planar REBCO coils, 20 T max on-coil.
   All CAS22 accounts use framework defaults — Thea Energy has NOT published a
   bottom-up capital cost breakdown. C220103 is almost certainly the largest single
   capital item but is entirely unconstrained by published data.
   Source: analysis.md §S5 Missing Parameters (capital cost rows).

8. Divertor: Novel QA X-point divertor (TRL 1–2, no hardware precedent).
   C220108 uses framework default ($60M base); actual cost is unknown.
   Source: analysis.md §S2 Challenge 2; §S3.

9. First wall lifetime: 15 full-power years (one replacement in 40-yr plant life).
   V-4Cr-4Ti vanadium alloy — extremely limited supply chain at plant scale.
   Source: thea-energy-helios-arxiv-2512-08027.md §First Wall; analysis.md §S4.

10. FOAK scenario only: noak=False. Thea's $150/MWh target applies to the first
    plant. No NOAK analogue modeled — published cost data does not exist to anchor
    a NOAK scenario for this concept.
    Source: thea-energy-website-and-press.md §Helios.
""")

# ── Sensitivity Analysis ──────────────────────────────────────────────────────
sens = model.sensitivity(result.params)

print("Sensitivity (elasticity = %LCOE / %param)")
print("-" * 48)

print("\nEngineering levers:")
for k, v in sorted(sens["engineering"].items(), key=lambda x: abs(x[1]), reverse=True):
    print(f"  {k:<28} {v:+.4f}")

print("\nFinancial:")
for k, v in sorted(sens["financial"].items(), key=lambda x: abs(x[1]), reverse=True):
    print(f"  {k:<28} {v:+.4f}")

print("\nCosting constants (top 15):")
costing = sorted(sens["costing"].items(), key=lambda x: abs(x[1]), reverse=True)
for k, v in costing[:15]:
    print(f"  {k:<28} {v:+.4f}")
