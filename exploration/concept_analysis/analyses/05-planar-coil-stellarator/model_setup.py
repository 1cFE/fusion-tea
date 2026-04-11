"""Planar Coil Stellarator (Thea Energy — Helios) LCOE Model Setup.

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
    - availability=0.88 (Helios states 88%; default may differ)
    - noak=False (FOAK: first plant is the modeled scenario per $150/MWh target)
    - f_dec=0.0 (pure steam Rankine; no direct energy conversion)

Usage:
    uv run python model_setup.py              # print results to terminal
    uv run python model_setup.py | tee model_output.txt  # also save for synthesis stage
"""

from costingfe import ConfinementConcept, CostModel, Fuel

# ── Model Initialization ─────────────────────────────────────────────────────
model = CostModel(concept=ConfinementConcept.STELLARATOR, fuel=Fuel.DT)

# ── Plant Configuration Constants ────────────────────────────────────────────
# All values sourced from analysis.md §Section 5 unless noted.
# Sources:
#   [A] analysis.md §Section 5: LCOE-Relevant Parameters table
#   [B] thea-energy-helios-arxiv-2512-08027.md (Helios preconceptual design)
#   [C] analysis.md §Section 2 (challenges) and §Section 5 (missing params)
#   [D] mfe_stellarator.yaml framework defaults (used where no Helios data exists)

NET_ELECTRIC_MW = 390.0    # [A] "Net electric to grid: 390 MWe"
AVAILABILITY     = 0.88    # [A] "Capacity factor: 88%"; maintenance-limited,
                           #      84-day biennial maintenance cycle [B §Operations]
LIFETIME_YR      = 40      # [A] "Magnet design lifetime: 40+ years" [B §Magnets]
CONSTRUCTION_YR  = 8.0     # DEFAULT [D]: no published Helios construction timeline;
                           # UNCERTAIN: planar coil simplifies winding but FOAK complexity
INTEREST_RATE    = 0.07    # DEFAULT: standard LCOE financial assumption
INFLATION_RATE   = 0.0245  # DEFAULT: standard LCOE financial assumption

# Geometry — Helios preconceptual design [B §Plasma & Configuration]
R0          = 8.0    # [A] "Major radius: 8 m"
PLASMA_T    = 1.8    # [A] "Minor radius: 1.8 m" (aspect ratio 4.5)
ELON        = 1.0    # QA stellarator ≈ circular cross-section [B §Plasma & Configuration]
BLANKET_T   = 0.50   # [B §Blanket & Tritium Breeding] Blanket thickness 50 cm — directly stated in Helios source.

result = model.forward(
    # ── Plant requirements ──────────────────────────────────────────────────
    net_electric_mw=NET_ELECTRIC_MW,
    availability=AVAILABILITY,
    lifetime_yr=LIFETIME_YR,
    n_mod=1,
    construction_time_yr=CONSTRUCTION_YR,
    interest_rate=INTEREST_RATE,
    inflation_rate=INFLATION_RATE,
    noak=False,         # FOAK: first-plant scenario; Thea LCOE target is $150/MWh
                        #        for first plant [A: "LCOE target (first plant): $150/MWh"]

    # ── Helios geometry ─────────────────────────────────────────────────────
    R0=R0,
    plasma_t=PLASMA_T,
    elon=ELON,
    blanket_t=BLANKET_T,
    ht_shield_t=0.20,   # DEFAULT [D]; no Helios-specific shield thickness published
    structure_t=0.15,   # DEFAULT [D]
    vessel_t=0.10,      # DEFAULT [D]

    # ── Power balance ────────────────────────────────────────────────────────
    # Helios is effectively ignited (Q_plasma ≈ 958) [A: "Plasma gain: ~958"]
    # Total thermal: 1,094 MW; gross electric: 438 MWe; net: 390 MWe [A]
    # Total facility/auxiliary load: ~48 MWe [A: "Auxiliary / facility power: ~48 MWe"]
    p_input=1.0,        # [A] "Operational ECRH power: 1 MW" — impurity control only;
                        #      plasma self-heats via alpha particles; 10 MW ECRH only at startup
    mn=1.1,             # DEFAULT [D]: standard D-T neutron energy multiplier (1 + ~10% via n reactions)
    eta_th=0.40,        # [A/B] "~40.2% (gross)" — three-stage steam Rankine, 635°C superheated steam
                        #        [B §Energy Conversion]; slightly below default 0.46 (Helios-specific)
    eta_p=0.5,          # DEFAULT [D]: pumping efficiency
    eta_pin=0.5,        # DEFAULT [D]: ECRH gyrotron wall-plug efficiency (standard for 170 GHz gyrotrons)
    eta_de=0.85,        # DEFAULT [D]: no direct energy conversion used; value unused (f_dec=0.0)
    f_sub=0.03,         # DEFAULT [D]: miscellaneous subsystem fraction; bulk of 48 MWe facility load
                        #               captured in explicit p_xxx terms below
    f_dec=0.0,          # Pure steam Rankine; no DEC; [A: recirculating power is parasitic only]

    # Individual auxiliary loads — components of the 48 MWe facility total [A]
    p_coils=2.0,        # UNCERTAIN: 324 individually addressable HTS power supply units;
                        #             REBCO has negligible resistive loss but supply electronics
                        #             have losses; no published figure [C §S5 gap: coil MTBF]
    p_cool=8.0,         # UNCERTAIN: helium blanket loop blowers + heat exchangers (He→steam IHX);
                        #             He-cooled primary loop is less well-characterized than H₂O;
                        #             no published breakdown [C §S3: He coolant BOP]
    p_pump=3.0,         # UNCERTAIN: LiPb circulation at 6.6 cm/s [B §Blanket & Tritium Breeding];
                        #             estimated from MHD-limited flow against ~6T field; derivable
                        #             but not published [C §S5 gap #14]
    p_trit=10.0,        # DEFAULT [D]: tritium extraction and processing (~300 g/day at 958 MW fusion,
                        #              5% burn fraction); consistent with DT baseline
    p_house=5.0,        # UNCERTAIN: facility controls, 450+ variable real-time control system,
                        #             HVAC, instrumentation; slightly above 4.0 MW default given
                        #             software-intensive 324-coil control infrastructure [C §S2 Challenge 4]
    p_cryo=15.0,        # UNCERTAIN: 336 REBCO coils at 20 K operating temperature [A/B §Magnets];
                        #             Carnot COP at 20 K ≈ 0.07 → large refrigeration demand;
                        #             analysis.md §S5 gap #14 estimates "5–15 MWe" for cryo plant;
                        #             using 15 MW (upper bound) as most likely given coil count
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
print()

# ── Key Assumptions Summary ────────────────────────────────────────────────────
print("Key Assumptions")
print("  Physics  : ISS04 H=1.4 sustained (analysis.md §S2 Challenge 1 — not yet")
print("             experimentally demonstrated in any QA stellarator; Eos 2030)")
print("  Geometry : R0=8m, a=1.8m, 2-field-period QA, 6T on-axis [Helios arXiv:2512.08027]")
print("  Power    : Net 390 MWe, 88% availability, 40-yr life, FOAK (noak=False)")
print("  Thermal  : eta_th=0.40 (three-stage Rankine, 635°C steam, 40.2% gross)")
print("  Heating  : p_input=1 MW operational ECRH (plasma ignited, Q~958)")
print("  Cryo     : p_cryo=15 MW UNCERTAIN (336 REBCO coils at 20K; upper-bound estimate)")
print("  Divertor : Novel QA X-point divertor, TRL 1-2, no hardware precedent")
print("             [analysis.md §S2 Challenge 2] — cost uses framework default (60 M$ base)")
print("  Magnets  : 12 encircling + 324 shaping planar REBCO coils, 20T max on-coil")
print("             [analysis.md §S5] — NO published cost account; framework default only")
print("  Cost basis: Framework defaults throughout (ARIES-CS analogue structure)")
print("              Thea Energy has NOT published a bottom-up capital cost breakdown")
print("  LCOE gap : Thea target $150/MWh FOAK; model result above is the costingfe")
print("             parametric estimate — gap reflects unmodeled magnet cost premium")
print()

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
