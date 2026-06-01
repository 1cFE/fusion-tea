"""Helical Coil Stellarator (Helical Fusion HESTIA) — LCOE estimate.

Usage:
    uv run python model_setup.py              # print results to terminal
    uv run python model_setup.py | tee model_output.txt  # also save for synthesis stage

Modeling approach:
    Uses 1costingfe CostModel (STELLARATOR / DT / BRAYTON_SCO2) with the framework's
    ARIES-calibrated stellarator defaults as the base cost structure. No CAS-level overrides
    are applied — the published direct construction cost (~$5B at 1990s prices, requiring ×2+
    inflation correction → ~$10B in 2023 USD for 70.4 MWe) carries "low" source confidence
    and lacks the CAS sub-account breakdown needed for account-level injection. The framework
    output is an internally consistent structural lower bound anchored to published physics
    parameters; it should be read alongside the $10B published anchor (Key Assumption #1).

    Native design point: 70.4 MWe (HESTIA FPP; Miyazawa & Goto 2023, Table I).
    Because this is not 1000 MWe, a second forward pass at 1 GWe is produced for
    cross-concept comparison using the dual-result pattern (override_reference_mw=70.4).

    Key structural features of this model:
    - sCO₂ Brayton cycle targeting >50% thermal efficiency (central case: 50%) is the
      LOAD-BEARING ASSUMPTION for Q_eng=2.0 at Q~13; efficiency scenario sweep is primary
    - 20 MW absorbed ECRH via 60 gyrotrons × 1 MW / 3 per beam; effective η = 1/3
    - Liquid metal (Sn-In-Pb-Li) blanket; pump power "quite unknown" — default placeholder
    - Continuous helical HTS coils (WISE REBCO); harder than modular → 10-yr construction
    - Steady-state operation: ~1-year burn + ~3-month maintenance → ~80% structural ceiling

    Critical model limitation:
    The inflation-adjusted published cost ($10B) implies ~$143B/GWe — far above any concept
    in the portfolio. The framework does NOT reproduce this from ARIES scaling. The LCOE
    reported here is a structural lower bound; the $10B figure implies LCOE in the
    several-$/kWh range at FOAK (excluded O&M and financing would make it higher still).
    The economic thesis for HESTIA rests on fleet manufacturing learning curves that are
    entirely speculative at current funding levels ($35.3M through late 2025).

Concept choice rationale:
    ConfinementConcept.STELLARATOR / Fuel.DT — maps to the heliotron (HESTIA) configuration.
    The STELLARATOR concept uses steady-state defaults (no disruptions, ECRH primary heating,
    complex 3D coil assumptions). BRAYTON_SCO2 power cycle selects sCO₂ BOP cost coefficients;
    eta_th is overridden to 0.50 (conservative within the >50% published target).

Key deviations from dt_stellarator.py reference:
    - Small native scale: 70.4 MWe (vs. 1000 MWe reference) → dual-result pattern
    - sCO₂ Brayton cycle (BRAYTON_SCO2 preset; eta_th overridden to 0.50)
    - Low effective heating system efficiency (eta_pin=0.333; 60 MW wall-plug / 20 MW absorbed)
    - 10-year construction time (continuous helical coil >> modular stellarator 8 yr default)
    - LM pump power unknown; p_cool uses stellarator default (blocking data gap)
    - No cost overrides: framework ARIES defaults only; C220103 is a lower bound
"""

from costingfe import ConfinementConcept, CostModel, Fuel, PowerCycle

# ── Model creation ────────────────────────────────────────────────────────────

model = CostModel(
    concept=ConfinementConcept.STELLARATOR,
    fuel=Fuel.DT,
    power_cycle=PowerCycle.BRAYTON_SCO2,   # sCO₂ Brayton BOP cost coefficients
)

# ── Plant configuration constants ─────────────────────────────────────────────

# Native net electric output (FPP design point)
# Source: aip-2023-paper-abstract.md §Table I
_NATIVE_MWE = 70.4  # MWe

# Major radius: direct from HESTIA Table I (high confidence)
# Source: aip-2023-paper-abstract.md §II-B, Table I
_R0 = 7.8  # m

# Minor radius: UNCERTAIN — estimated from fusion power and plasma volume
# p_fus ≈ Q × p_absorbed ≈ 13 × 20 MW ≈ 260 MW; assume power density ~0.5 MW/m³
# → plasma volume V ≈ 520 m³; V = 2π²R₀a² → a ≈ sqrt(520 / (2π²×7.8)) ≈ 1.83 m
# Source: aip-2023-paper-abstract.md §Abstract (Q~13, §Table I fusion power 260 MW implied)
_A = 1.8  # m — UNCERTAIN

# Absorbed ECRH heating power: 60 gyrotrons × 1 MW / 3 per ECH beam = 20 MW to plasma
# Source: aip-2023-paper-abstract.md §II-D
_P_INPUT_MW = 20.0  # MW

# Effective heating system efficiency (wall-plug → plasma): 20/60 = 1/3
# 60 gyrotrons × 1 MW each = 60 MW electrical; 20 MW absorbed → η = 1/3
# UNCERTAIN: 250 GHz / 1 MW CW gyrotrons do not exist (TRL 1–2); analogue from 154–170 GHz
# Source: inferred from aip-2023-paper-abstract.md §II-D; analysis.md §3 (250 GHz gyrotrons)
_ETA_PIN = 20.0 / 60.0  # ≈ 0.333

# sCO₂ Brayton central efficiency: conservative lower end of >50% target
# Overrides BRAYTON_SCO2 preset (0.47) with HESTIA-specific aspirational target
# UNCERTAIN: 20 kWe demo at 20% only; no fusion-coupled sCO₂ demonstration exists
# Source: aip-2023-paper-abstract.md §II-F; helical-fusion-2025-2026-updates.md §sCO₂
_ETA_TH_CENTRAL = 0.50

# Availability: central estimate (FPP target range >80–85%)
# 1-year burn + ~3-month maintenance → structural ceiling ~80%; derate for novel-subsystem risk
# UNCERTAIN: no operational precedent; 0.83 mid-range of published 80–85% FPP target
# Source: aip-2023-paper-abstract.md §Table I; analysis.md §5 (availability row)
_AVAILABILITY = 0.83

# Construction time: 10 yr — above 8-yr modular stellarator default
# Continuous helical WISE REBCO coil winding is harder than modular (no joints; reactor scale
# is orders of magnitude beyond the Oct 2025 >4 m prototype)
# Source: analysis.md §3 (WISE HTS Helical Coil, TRL 3–5); §2, Challenge 1
_CONSTRUCTION_YR = 10.0

# ── Shared forward-pass parameters ───────────────────────────────────────────

_SHARED_KWARGS = dict(
    # Availability: 83% central (structural ceiling ~80% from burn/maintenance cycle)
    # Source: aip-2023-paper-abstract.md §Table I; analysis.md §5
    availability=_AVAILABILITY,

    lifetime_yr=30,          # DEFAULT standard 30-yr plant lifetime

    n_mod=1,                 # Single-module plant

    # 10 yr: continuous helical coil winding harder than modular stellarator (8 yr default)
    # First-of-kind WISE coil at reactor scale; Oct 2025 milestone = >4 m prototype only
    # Source: analysis.md §3 (WISE HTS Helical Coil, TRL 3–5); §2, Challenge 1
    construction_time_yr=_CONSTRUCTION_YR,

    interest_rate=0.07,      # DEFAULT standard WACC
    inflation_rate=0.0245,   # DEFAULT
    noak=True,               # NOAK central estimate (fleet manufacturing learning assumed)

    # ── Geometry ──────────────────────────────────────────────────────────────
    # R₀=7.8 m: direct from Table I (high confidence)
    # Source: aip-2023-paper-abstract.md §II-B, Table I
    R0=_R0,

    # plasma_t=1.8 m: UNCERTAIN — estimated; paper does not publish minor radius
    # Source: analysis.md §5 (fusion power ~260 MW); derivation in _A constant above
    plasma_t=_A,

    elon=1.0,          # Near-circular effective cross-section (heliotron stellarator default)
    blanket_t=0.80,    # DEFAULT — DT breeding blanket thickness [m]
    ht_shield_t=0.20,  # DEFAULT
    structure_t=0.15,  # DEFAULT
    vessel_t=0.10,     # DEFAULT

    # ── Power balance ─────────────────────────────────────────────────────────
    # Neutron multiplier: standard DT (Sn-In-Pb-Li LM blanket; no strong Pb(n,2n) assumed)
    # DEFAULT: no published mn for this alloy composition; tin/indium may reduce vs. PbLi
    mn=1.1,

    # Thermal efficiency: sCO₂ Brayton central case (overrides BRAYTON_SCO2 preset of 0.47)
    # UNCERTAIN: only 20 kWe demo at 20% efficiency; 50% is the aspirational target
    # Source: aip-2023-paper-abstract.md §II-F; helical-fusion-2025-2026-updates.md §sCO₂;
    #         analysis.md §2, Challenge 4 (load-bearing assumption for Q_eng=2.0)
    eta_th=_ETA_TH_CENTRAL,

    eta_p=0.5,         # DEFAULT pumping efficiency
    eta_de=0.85,       # DEFAULT (no DEC in Brayton cycle design)
    f_sub=0.03,        # DEFAULT subsystem power fraction
    f_dec=0.0,         # No direct energy conversion; all thermal Brayton
                       # Source: dossier.md §Energy Capture (sCO₂ Brayton)

    # Effective gyrotron system efficiency (electrical → plasma): 20 MW / 60 MW = 1/3
    # 60 gyrotrons × 1 MW each wall-plug; 3 gyrotrons per ECH beam; 20 beams × 1 MW absorbed
    # UNCERTAIN: 250 GHz / 1 MW CW gyrotrons do not exist; TRL 1–2; analogue efficiency
    # Source: inferred from aip-2023-paper-abstract.md §II-D; analysis.md §6, Gap 15
    eta_pin=_ETA_PIN,

    # Absorbed ECRH heating power (all heating is ECRH; no current drive needed)
    # Source: aip-2023-paper-abstract.md §II-D ("60 gyrotrons × 1 MW / 3 = 20 MW to plasma")
    p_input=_P_INPUT_MW,
    p_ecrh=_P_INPUT_MW,   # All ECRH (steady-state, no plasma current → no NBI needed)
    p_nbi=0.0,            # No NBI (heliotron is inherently current-free)
    p_icrf=0.0,           # No ICRF
    p_lhcd=0.0,           # No LHCD

    # HTS coil cryogenic power: gas He at 20 K (vs. liquid He at 4 K for LTS)
    # Dramatically reduced cryo load relative to LTS; HESTIA cites He scarcity as motivation
    # DEFAULT retained (0.8 MW) as appropriate for HTS-at-20K design; two large helical coils
    # Source: aip-2023-paper-abstract.md §II-B (HTS at 20 K, gas He cooling)
    p_coils=3.0,    # [MW] DEFAULT — WISE REBCO at 20 K gas He; complex coil with few joints
    p_cryo=0.8,     # [MW] DEFAULT — gas He refrigeration (lower than LTS liquid He at 4 K)

    # Liquid metal blanket pump power: "QUITE UNKNOWN AT THIS MOMENT" — direct AIP paper quote
    # GALOP gas-driven pump eliminates rotating parts but plant-scale power is unquantified
    # This is a BLOCKING DATA GAP; affects true Q_eng at 70 MWe tight power balance
    # Using stellarator defaults as placeholder; may be significantly different
    # Source: aip-2023-paper-abstract.md §II-C; analysis.md §2, Challenge 3; §6, Gap 3
    p_cool=15.0,    # [MW] DEFAULT — UNCERTAIN: LM pump power at 90-module scale unknown
    p_pump=1.0,     # [MW] DEFAULT — UNCERTAIN: auxiliary pumping placeholder

    p_trit=10.0,    # [MW] DEFAULT — tritium processing
    p_house=4.0,    # [MW] DEFAULT — housekeeping
)

# ── Forward pass: native design point (70.4 MWe) ─────────────────────────────
# Primary result at HESTIA's published design point.
# Preserves physics consistency (Q_eng, power balance, CAS breakdown) at native scale.
# Source: aip-2023-paper-abstract.md §Table I (net electric 70.4 MWe)

result = model.forward(net_electric_mw=_NATIVE_MWE, **_SHARED_KWARGS)

# ── Forward pass: 1 GWe normalized for cross-concept comparison ──────────────
# Per-account cost scaling from 70.4 MWe reference to 1 GWe.
# NOTE: 1 GWe scaling assumes HESTIA fleet manufacturing achieves 1 GWe aggregate output.
# The economic thesis is mass production of 70 MWe units, not a single 1 GWe plant.
# Interpret result_1gw as an analytical cross-concept normalization, not a design target.
# Source: analysis.md §2, Challenge 7; §7 (cross-concept modeling note)

result_1gw = model.forward(
    net_electric_mw=1000.0,
    override_reference_mw=_NATIVE_MWE,
    **_SHARED_KWARGS,
)

# ── Results: native HESTIA FPP (70.4 MWe) ────────────────────────────────────

c  = result.costs
pt = result.power_table

print("Helical Coil Stellarator (Helical Fusion HESTIA) — 70.4 MWe FPP, NOAK")
print(f"Power cycle: sCO₂ Brayton (η_th={_ETA_TH_CENTRAL:.0%} target central case)")
print(f"Availability: {_AVAILABILITY:.0%} | Lifetime: 30 yr | Construction: {_CONSTRUCTION_YR:.0f} yr")
print()
_lcoe_ckwh = float(c.lcoe) / 10.0
print(f"LCOE (framework):  {c.lcoe:.1f} $/MWh ({_lcoe_ckwh:.2f} c/kWh)  [LOWER BOUND — see Caveat 1]")
print(f"Overnight cost:    {c.overnight_cost:.0f} $/kW")
print(f"Fusion power:      {pt.p_fus:.0f} MW")
print(f"Net electric:      {pt.p_net:.1f} MWe")
print(f"Q_eng (model):     {pt.q_eng:.2f}  [target Q_eng=2.0; sensitive to η_th and LM pump power]")
print(f"Recirculating:     {pt.rec_frac:.1%}")
print()
print("CAVEATS:")
print("  [1] Published cost: ~$5B (1990s) × 2+ inflation → ~$10B for 70.4 MWe (~$143B/GWe)")
print("      Framework ARIES scaling does NOT reproduce this figure. Framework LCOE is a")
print("      structural lower bound — $10B anchor implies LCOE in several-$/kWh range.")
print("  [2] η_th=50% is aspirational; 20 kWe sCO₂ demo at 20% is the current state.")
print("  [3] LM pump power is 'quite unknown' — p_cool=15 MW is a placeholder (Gap 3).")
print()

# ── CAS breakdown ─────────────────────────────────────────────────────────────

cas_rows = [
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
for code, name, val in cas_rows:
    print(f"{code:<8} {name:<28} {float(val):>10.1f}")
print("-" * 48)
print(f"{'':8} {'Total Capital':<28} {float(c.total_capital):>10.1f}")
print()

# ── CAS22 sub-account detail ──────────────────────────────────────────────────

print("CAS22 Reactor Plant Equipment Breakdown:")
print("-" * 60)
cas22_labels = {
    "C220101": "First Wall + LM Blanket (Sn-In-Pb-Li)",
    "C220102": "Shield",
    "C220103": "Coils (cont. helical WISE REBCO)",
    "C220104": "Heating (ECRH 20 MW abs.)",
    "C220105": "Primary Structure",
    "C220106": "Vacuum Vessel",
    "C220107": "Power Supplies",
    "C220108": "Divertor (LM integrated FW)",
    "C220111": "Installation",
    "C220112": "Isotope Separation",
    "C220200": "Coolant (LM circuit)",
    "C220300": "Aux Cooling",
    "C220400": "Rad Waste",
    "C220500": "Fuel Handling (tritium)",
    "C220600": "Other Equipment",
    "C220700": "I&C",
}

_overridden = set(result.overridden) if hasattr(result, "overridden") else set()
for code, label in cas22_labels.items():
    val = result.cas22_detail.get(code, 0.0)
    if float(val) > 0:
        note = "[override]" if code in _overridden else "[DEFAULT]"
        if code == "C220103":
            note = "[DEFAULT — LOWER BOUND; cont. helical premium not captured]"
        print(f"  {code:<12} {label:<38} {float(val):>8.1f}  {note}")
_total22 = result.cas22_detail.get("C220000", float(c.cas22))
print("-" * 60)
print(f"  {'C220000':<12} {'TOTAL':<38} {float(_total22):>8.1f}")
print()
print("  NOTE: C220101 (LM blanket): exotic Sn-In-Pb-Li alloy + non-magnetic structural steel")
print("        adds cost vs. standard PbLi blanket; DEFAULT used (no published breakdown).")
print("  NOTE: C220103 (coils): continuous helical winding >> modular stellarator complexity;")
print("        DEFAULT is a wound-coil calibration — likely a SIGNIFICANT underestimate.")
print("  NOTE: CAS27 (special materials): 80 at.% Li-6 enrichment required (highest in portfolio);")
print("        DEFAULT used; global enrichment capacity constraint not quantified.")
print()

# ── 1 GWe scaled result summary ──────────────────────────────────────────────

c1  = result_1gw.costs
pt1 = result_1gw.power_table
print("=" * 64)
print("Cross-Concept Normalization: Scaled to 1 GWe")
print("=" * 64)
print("Per-account scaling from 70.4 MWe native point; framework scaling laws applied.")
print("NOTE: HESTIA's economic thesis = mass manufacturing of 70 MWe units, not one 1 GWe plant.")
print(f"LCOE:           {c1.lcoe:.1f} $/MWh ({float(c1.lcoe)/10:.2f} c/kWh)  [LOWER BOUND]")
print(f"Overnight cost: {c1.overnight_cost:.0f} $/kW")
print(f"Fusion power:   {pt1.p_fus:.0f} MW | Net: {pt1.p_net:.0f} MWe | Q_eng: {pt1.q_eng:.2f}")
print()

# ── sCO₂ Efficiency Scenario Sweep ───────────────────────────────────────────
# eta_th is the LOAD-BEARING ASSUMPTION for HESTIA's economic case and Q_eng=2.0 at Q~13.
# At Q~13 with 20 MW absorbed heating:
#   - If eta_th=0.50: Q_eng ≈ 2.0 (published design target)
#   - If eta_th=0.38: steam Rankine fallback; Q_eng drops substantially, net output << 70 MWe
# Only the kW-scale demo at 20% efficiency exists; 50% is entirely aspirational.
# Source: analysis.md §2, Challenge 4; §3 (sCO₂ Brayton, TRL 3–4); §5 (eta_th row)

print("=" * 64)
print("sCO₂ EFFICIENCY SCENARIO SWEEP  [PRIMARY STRUCTURAL UNCERTAINTY]")
print("=" * 64)
print("eta_th is LOAD-BEARING: without >50% sCO₂, Q_eng < 2.0 at this plasma gain.")
print("Source: analysis.md §2, Challenge 4; §3 (TRL 3–4); §5 (thermal efficiency row)")
print()

_eta_cases = [
    (0.53, "COMBINED (gas+steam cycle)",   "aspirational — no fusion demo"),
    (0.50, "sCO₂ Brayton target (>50%)",  "HESTIA design target ← BASE"),
    (0.47, "BRAYTON_SCO2 preset",          "commercial sCO₂ (CSP, 2024)"),
    (0.40, "sCO₂ degraded (40%)",          "near-term achievable w/o full integration"),
    (0.38, "steam Rankine fallback",        "if sCO₂ development fails"),
]

print(f"  {'eta_th':>7} {'LCOE $/MWh':>12} {'Net MWe':>10} {'Q_eng':>8}  Note")
print("  " + "-" * 74)
for _eta, _label, _note in _eta_cases:
    _r = model.forward(
        net_electric_mw=_NATIVE_MWE,
        **{**_SHARED_KWARGS, "eta_th": _eta},
    )
    print(f"  {_eta:>6.0%}  {float(_r.costs.lcoe):>11.1f} {float(_r.power_table.p_net):>10.1f}"
          f" {float(_r.power_table.q_eng):>8.2f}  {_note}")
print()
print("  CRITICAL: At η_th < ~40%, recirculating power exceeds a major fraction of gross")
print("  output — the self-sufficient design margin collapses. The 20% kW-scale demo is")
print("  a factor of 2.5× below the design target. No fusion-coupled sCO₂ test exists.")
print("  Source: helical-fusion-2025-2026-updates.md §sCO₂; analysis.md §2, Challenge 4")
print()

# ── Availability Sweep ────────────────────────────────────────────────────────
# Steady-state operation (no plasma restarts) is HESTIA's primary structural advantage.
# Published target: >80–85% FPP, >90% FOAK.
# Structural ceiling ~80% from 1-year burn + ~3-month maintenance cycle.
# Novel subsystem risk (LM blanket, 250 GHz gyrotrons, sCO₂) limits realized availability.
# Source: aip-2023-paper-abstract.md §Table I; analysis.md §5; analysis.md §2, Challenge 7

print("=" * 64)
print("AVAILABILITY SWEEP  (steady-state operation advantage)")
print("=" * 64)
print("Structural ceiling ~80% from 1-yr burn + 3-month maintenance; target >80–85% FPP")
print("Source: aip-2023-paper-abstract.md §Table I; analysis.md §5 (availability row)")
print()
print(f"  {'Avail':>7} {'LCOE $/MWh':>12} {'Δ base':>9} {'Overnight $/kW':>16}  Note")
print("  " + "-" * 66)
_base_lcoe = float(c.lcoe)
_av_cases = [
    (0.70, "derated — novel-system outages"),
    (0.80, "structural ceiling (1yr burn / 3mo maint)"),
    (0.83, "central FPP estimate ← BASE"),
    (0.85, "top of FPP published target range"),
    (0.90, "FOAK published target"),
]
for _av, _av_note in _av_cases:
    _r = model.forward(
        net_electric_mw=_NATIVE_MWE,
        **{**_SHARED_KWARGS, "availability": _av},
    )
    _lc = float(_r.costs.lcoe)
    _on = float(_r.costs.overnight_cost)
    print(f"  {_av:>6.0%}  {_lc:>11.1f} {_lc - _base_lcoe:>+8.1f} {_on:>15.0f}  {_av_note}")
print()

# ── Key Assumptions ───────────────────────────────────────────────────────────

print("""Key Assumptions
===============
1. Published cost data and framework divergence  [CRITICAL CAVEAT]
   Published: ~$5B direct construction cost (Miyazawa & Goto 2023, Table I), 1990s LHD/ITER
   pricing. Authors explicitly state ×2+ inflation correction required → ~$10B in 2023 USD
   for 70.4 MWe. Specific capital: ~$143B/GWe — far above any other portfolio concept.
   Framework (ARIES-calibrated) does NOT reproduce this figure; gap is the primary output
   caveat. Framework LCOE is a structural lower bound. The $1.22/kWh Table I metric excludes
   O&M, fuel, financing, and inflation correction — it is not comparable to standard LCOE.
   Confidence: LOW (1990s price basis; no independent techno-economic assessment exists)
   Source: aip-2023-paper-abstract.md §I, §Table I; analysis.md §2, Challenge 1; §6, Gap 1

2. sCO₂ Brayton thermal efficiency: 50% central case  [PRIMARY STRUCTURAL UNCERTAINTY]
   HESTIA's η_th > 50% target at 800–1200 K is essential for Q_eng=2.0 at Q~13 plasma gain.
   Current state: 20 kWe NIFS Oroshhi-2 demonstration at 20% efficiency (feasibility study).
   No fusion-coupled sCO₂ demonstration at any scale exists anywhere.
   Efficiency scenario sweep above shows LCOE and Q_eng collapse below 50%.
   UNCERTAIN: 50% has never been demonstrated at any fusion-relevant scale.
   Source: aip-2023-paper-abstract.md §II-F; helical-fusion-2025-2026-updates.md §sCO₂;
           analysis.md §2, Challenge 4; §3 (sCO₂ Brayton TRL 3–4); §6, Gap 6

3. Absorbed heating power: 20 MW ECRH; effective η = 1/3
   60 gyrotrons × 1 MW each / 3 per ECH beam = 20 MW to plasma; 60 MW wall-plug.
   Effective system efficiency 20/60 = 0.333 (gyrotron conversion × transmission × coupling).
   UNCERTAIN: 250 GHz / 1 MW CW gyrotrons do not exist (TRL 1–2); frequency required by
   HESTIA's field/density cannot be lowered without redesigning the plasma operating point.
   Source: aip-2023-paper-abstract.md §II-D; analysis.md §3 (250 GHz gyrotrons, TRL 1–2)

4. Availability: 83% central (FPP target range >80–85%)
   1-year burn + ~3-month maintenance → structural ceiling ~80% (12/15 months).
   0.83 central = mid-range of published FPP target, derated for novel-subsystem outage risk.
   No operational precedent for any heliotron at HESTIA scale.
   Source: aip-2023-paper-abstract.md §Table I; analysis.md §5 (availability row);
           helical-fusion-technology-overview.md

5. Liquid metal pump power: DEFAULT placeholder  [BLOCKING GAP]
   AIP paper: "The LM pump power is quite unknown at this moment."
   GALOP gas-driven pump eliminates rotating parts but plant-scale power is unquantified.
   90 modular LM blanket modules at reactor scale have no engineering basis for circulation power.
   Q_eng=2.0 at 70 MWe has a tight recirculating budget; LM pump could significantly affect
   realized net output. p_cool=15 MW (stellarator default) used as placeholder.
   Source: aip-2023-paper-abstract.md §II-C; analysis.md §2, Challenge 3; §6, Gap 3

6. Plasma geometry: R₀=7.8 m (known); a≈1.8 m (estimated)
   R₀ from Table I (high confidence). Minor radius estimated from fusion power (~260 MW) and
   assumed power density (~0.5 MW/m³) → V ≈ 520 m³ → a ≈ 1.8 m (V = 2π²R₀a²).
   Paper does not publish minor radius directly in the available abstract.
   Source: aip-2023-paper-abstract.md §II-B, Table I; analysis.md §5 (R₀, fusion power)

7. C220103 coils: DEFAULT — LOWER BOUND (continuous helical coil premium not captured)
   Framework coil cost calibrated to wound-coil (tokamak-style) geometry.
   HESTIA uses two CONTINUOUS helical coils — fundamentally different from modular stellarator
   or tokamak coil sets. Longer unbroken conductor runs, complex 3D path, reactor-scale WISE
   REBCO tape demand not published. Current tape cost $30–100/kA-m; NOAK target $10/kA-m.
   C220103 is a lower bound; true coil cost likely substantially higher.
   Source: analysis.md §4 (REBCO supply chain); §3 (WISE HTS Helical Coil, TRL 3–5)

8. C220101 first wall / LM blanket: DEFAULT — cost likely higher
   Novel Sn-In-Pb-Li alloy vs. standard PbLi; non-magnetic high-Mn austenitic structural steel
   (new material, no industrial production baseline); 90 modular units.
   Indium supply constraint: ~900 tonnes/yr global production; fusion demand could be material.
   DEFAULT blanket_unit_cost_dt used (no published cost breakdown for LM alloy blanket).
   Source: analysis.md §4 (LM alloy, indium supply); §3 (LM Blanket, TRL 2–3)

9. Construction time: 10 years
   Stellarator default 8 yr (mfe_stellarator.yaml); helical coil winding is harder than modular.
   Oct 2025 milestone: >4 m prototype; reactor coils are orders of magnitude more demanding.
   10 yr estimate is above modular default to reflect first-of-kind continuous coil challenge.
   Source: analysis.md §3 (WISE HTS Helical Coil, TRL 3–5); mfe_stellarator.yaml (8 yr default)

10. NOAK assumption
    HESTIA's economic thesis depends on fleet manufacturing and learning curves.
    Current funding: ~$35.3M (through late 2025) — a fraction of peers (CFS ~$2.9B).
    No quantitative basis exists for the learning curve that would achieve NOAK costs.
    FOAK at $10B for 70.4 MWe implies LCOE >> the framework output before O&M and financing.
    Source: analysis.md §2, Challenge 7; helical-fusion-2025-2026-updates.md (funding)

11. O&M: framework DEFAULT
    No O&M cost data exists for any stellarator power plant in the public record.
    ARIES-CS analogue (~$50–70/kWe-yr fixed O&M) noted in analysis as placeholder.
    Structural advantages: steady-state (no restart costs); 90 modular LM units with crane
    access (no in-vessel robotics for module extraction — reduces planned maintenance burden).
    Source: analysis.md §2 (O&M placeholder); aip-2023-paper-abstract.md §II-C (crane access)

12. Li-6 enrichment: 80 at.% target — highest in portfolio
    Global Li-6 enrichment capacity is constrained; Western industrial-scale alternatives
    to legacy mercury-amalgam separation processes are not yet operational.
    CAS27 uses DEFAULT; enrichment cost for this purity level at 90-module scale is unknown.
    TBR 3D neutron transport calculation was NOT completed as of the 2023 paper.
    Source: aip-2023-paper-abstract.md §IV; analysis.md §4 (Li-6 enrichment); §6, Gap 4

13. H confinement factor: H=1.3 assumed above ISS04 (UNVERIFIED — blocking gap)
    HESTIA plasma design assumes H=1.3 above the ISS04 empirical stellarator scaling law.
    This is not experimentally validated; it depends on center-peaked ECH heating and
    magnetic optimization not yet demonstrated at HESTIA-class parameters.
    H=1.0 (no improvement) would require larger plasma volume → inflates all capital cost.
    Not modeled directly in the framework; captured qualitatively as cost lower-bound caveat.
    Source: aip-2023-paper-abstract.md §II-A; analysis.md §2, Challenge 2; §6, Gap 5
""")

# ── Sensitivity Analysis ──────────────────────────────────────────────────────

sens = model.sensitivity(result.params)

print("Sensitivity (elasticity = %LCOE / %param) — native 70.4 MWe design point")
print("-" * 52)

print("\nEngineering levers:")
for k, v in sorted(sens["engineering"].items(), key=lambda x: abs(x[1]), reverse=True):
    print(f"  {k:<36} {v:+.4f}")

print("\nFinancial:")
for k, v in sorted(sens["financial"].items(), key=lambda x: abs(x[1]), reverse=True):
    print(f"  {k:<36} {v:+.4f}")

print("\nCosting constants (top 15):")
_costing = sorted(sens["costing"].items(), key=lambda x: abs(x[1]), reverse=True)
for k, v in _costing[:15]:
    print(f"  {k:<36} {v:+.4f}")
