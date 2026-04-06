"""Magnetized Target Fusion - Pneumatic Compression (D-T) — LCOE model.
General Fusion commercial concept.

Modeling approach:
  Anchors on the 300 MWe commercial target (the only publicly stated plant-
  level output figure) and works backward through an assumed Rankine steam
  cycle. Because fusion gain Q, thermal efficiency, and recirculating power
  fraction are all undisclosed, the three primary sensitivity dimensions are:
    1. availability (capacity factor) — dominant LCOE multiplier; mechanical
       system maintenance schedule completely unknown
    2. eta_th (thermal efficiency) — steam Rankine at unknown liquid metal
       exit temperature; range 33–40%
    3. p_driver (average piston + plasma injector power) — proxy for
       recirculating power; no experimental basis at commercial scale

Concept choice rationale:
  ConfinementConcept.MAG_TARGET / Fuel.DT matches the General Fusion MTF-
  pneumatic architecture: pulsed magnetized target compressed by a liquid
  metal driver, D-T fuel cycle with tritium bred in the liquid metal wall.

Key deviations from MAG_TARGET defaults (mif_mag_target.yaml):
  Power balance:
    - eta_th = 0.35 (vs 0.40 default) — conservative Rankine steam; liquid
      metal outlet temperature not published; 33–40% range per analogues
    - eta_pin = 0.80 (vs 0.30) — steam-driven reciprocating pistons are
      mechanical (~70–85% efficient), not electrical pulsed power
    - p_cryo = 0.0 — no superconducting coils in commercial design; liquid
      metal pressure provides confinement; CT injector uses Cu coils
    - p_target = 0.0 — no consumable targets; liquid metal liner is self-
      renewing (reforms each pulse, unlike MagLIF's solid RTL targets)

  Geometry:
    - plasma_t = 2.0 m — commercial cavity radius from 4 m cavity diameter
      (confirmed in peer-reviewed FST 2025 paper)
    - blanket_t = 1.0 m — liquid metal shell thickness (combined breeder +
      heat carrier); no separate blanket structure

  Cost overrides:
    - C220103 = $10M — minimal guide field coils only (CT injector uses small
      normal-conducting Cu coils; no HTS, no cryoplant)
    - C220104 = $180M (UNCERTAIN) — pneumatic compression driver capital:
      piston array, steam supply infrastructure, liquid metal flow control.
      Novel architecture; no published cost; bounded from analogous industrial
      machinery as floor estimate. This is likely the dominant non-blanket
      capital account.
    - C220108 = $0 — no target factory; liquid metal is self-renewing

  Scale / plant:
    - net_electric_mw = 300.0 — stated commercial target
    - noak = False — TRL 2–3 for compression system; FOAK premium applies

Explicit failure modes (binary gates, NOT captured as cost parameters):
  FM-1: If 12:1 cavity compression cannot be achieved in flowing liquid metal
        (water tests show 8:1 vs 12:1 target), the plasma cannot reach fusion
        temperatures — concept-level physics failure.
  FM-2: If synchronized piston operation in liquid metal environment is
        mechanically infeasible, no fallback compression mechanism exists.

Usage:
    uv run python model_setup.py              # print results to terminal
    uv run python model_setup.py | tee model_output.txt  # also save for synthesis stage
"""

from costingfe import ConfinementConcept, CostModel, Fuel

model = CostModel(concept=ConfinementConcept.MAG_TARGET, fuel=Fuel.DT)

# ── Plant configuration constants ────────────────────────────────────────────
# analysis.md §Section 5: Available Parameters Table

NET_ELECTRIC_MW = 300.0
# Stated commercial target.
# Source: general-fusion-lm26-milestones-2025.md §Commercial Target;
#         dossier §Power Output — "~150,000 Canadian homes"; single plant target.
# Confidence: high (all public sources converge on 300 MWe).

AVAILABILITY = 0.80
# UNCERTAIN: mechanical compression system maintenance schedule completely
# unpublished; no industrial precedent for piston array at this scale + duty.
# Analogue range 75–90% from 01-hts-compact-tokamak §Capacity Factor Sensitivity
# (Araiinejad & Shirvan 2025). Using 80% as midpoint; sensitivity below shows
# the impact of the full range.
# Source: analysis.md §Section 5 Table (capacity factor row).

LIFETIME_YR = 30
# Standard fusion plant lifetime; framework default; no GF-specific disclosure.

CONSTRUCTION_TIME_YR = 5.0
# No HTS magnet installation or cryoplant commissioning (shortens vs tokamak),
# but novel pneumatic compression system and liquid metal plumbing add time.
# DEFAULT: intermediate between 4 yr (no-magnet modular) and 6 yr (tokamak).

# ── Model forward pass ──────────────────────────────────────────────────────
result = model.forward(
    net_electric_mw=NET_ELECTRIC_MW,
    # Source: general-fusion-lm26-milestones-2025.md §Commercial Target
    availability=AVAILABILITY,
    # Source: analysis.md §Section 5 (capacity factor row); UNCERTAIN — see above
    lifetime_yr=LIFETIME_YR,
    n_mod=1,
    # Single-plant architecture; no modular decomposition published by GF.
    construction_time_yr=CONSTRUCTION_TIME_YR,
    interest_rate=0.07,
    # DEFAULT: standard fusion project WACC; no GF-specific financing disclosed.
    inflation_rate=0.0245,
    # DEFAULT: US CPI long-run average; framework standard.
    noak=False,
    # FOAK: TRL 2–3 for pneumatic compression system and liquid metal tritium
    # extraction (analysis.md §Section 3). No prior commercial plant of this
    # architecture exists. Contingency rate = 10% (framework FOAK default).

    # ── Geometry (spherical chamber) ──────────────────────────────────────
    R0=0.0,
    # Not used for spherical geometry.
    plasma_t=2.0,
    # Commercial cavity radius: ~4 m cavity diameter → 2 m radius.
    # Source: general-fusion-fst-2025-fuel-cycles.md §Cavity Geometry;
    #         confirmed in peer-reviewed FST 2025 paper (DOI: 10.1080/15361055.2025.2526266).
    # Confidence: high.
    blanket_t=1.0,
    # Liquid metal shell thickness (Li or PbLi). Acts as combined breeder +
    # heat carrier + neutron absorber. No separate blanket structure exists.
    # Source: analysis.md §Section 7 TEA Implications (liquid metal wall row);
    #         4π solid-angle coverage provides superior breeding geometry vs
    #         outboard tokamak blanket. Thickness is inferred from mass
    #         estimates (~50–100 t Li at ~4 m cavity); not published directly.
    # Confidence: low (rough geometric inference).
    ht_shield_t=0.20,
    # DEFAULT: framework default for MIF mag target.
    structure_t=0.20,
    # DEFAULT: framework default.
    vessel_t=0.15,
    # Pressure vessel for ~4 m spherical cavity; steam pressures from piston
    # recharge. Slightly reduced from tokamak default (no vacuum requirement;
    # liquid metal fills cavity between shots). DEFAULT adjusted.

    # ── Power balance ──────────────────────────────────────────────────────
    p_driver=50.0,
    # UNCERTAIN: time-averaged piston recharge + plasma injector power [MW].
    # LM26 (surrogate, EM theta-pinch, 50% plasma scale) uses 18 MJ/shot.
    # Commercial: 2× plasma scale → ~8× volume → driver energy scales roughly
    # as cavity volume compressed. Very rough upper-bound estimate ~50 MW avg.
    # No published design-point driver energy for commercial pneumatic system.
    # Source: general-fusion-technical-details.md §Compression System (LM26
    #         energy reference only; commercial system not analogous).
    # Confidence: very low — order-of-magnitude placeholder only.
    mn=1.1,
    # Neutron energy multiplier for Li or PbLi liquid metal wall.
    # Li blanket: negligible multiplication. PbLi: Pb provides ~10% boost.
    # Using 1.1 as midpoint; TBR target ~1.5 confirmed.
    # Source: dossier §Tritium Breeding; general-fusion-fst-2025-fuel-cycles.md
    #         §TBR Analysis. DEFAULT framework value for DT MIF.
    eta_th=0.35,
    # UNCERTAIN: Rankine steam cycle thermal efficiency.
    # Published range: 33–40% (analysis.md §Section 5, thermal efficiency row).
    # Liquid metal outlet temperature not disclosed; pure Li → need IHX
    # (intermediate heat exchanger) to isolate reactive Li from steam, reducing
    # effective temperature and efficiency vs direct steam contact.
    # Midpoint 35% used; sensitivity sweeps 0.33–0.40 below.
    # Source: analysis.md §Section 2 Challenge #6; analogue from
    #         07-maglif §Power Conversion (~40% Brayton-Rankine cited).
    # Confidence: low.
    eta_p=0.5,
    # DEFAULT: pumping efficiency for liquid metal + auxiliary circuits.
    eta_pin=0.80,
    # Steam-driven reciprocating pistons: mechanical efficiency ~70–85%.
    # Higher than pulsed electrical power (0.30 default) because mechanical
    # energy transfer via steam is more efficient than pulsed power electronics.
    # Source: analysis.md §Section 7 (pneumatic compression row); industrial
    #         reciprocating compressor analogues (Dresser-Rand, Atlas Copco).
    # Confidence: medium.
    f_sub=0.03,
    # DEFAULT: subsystem parasitic power fraction (diagnostics, control, aux).
    f_dec=0.0,
    # No direct energy conversion; all output via Rankine steam turbine.
    p_coils=0.5,
    # CT (compact toroid) injector guide field coils; small normal-conducting
    # Cu solenoids. Very low power vs HTS coil systems.
    # Source: dossier §Magnet Type; analysis.md §Section 7 (no HTS row).
    p_pump=3.0,
    # Liquid metal circulation pumps (Li or PbLi primary loop). Higher than
    # framework default due to large liquid metal inventory and flow rates
    # required for heat extraction at 1 Hz rep rate.
    # UNCERTAIN: flow rate and pump head not disclosed.
    # Source: analysis.md §Section 2 Challenge #6 (liquid metal thermal circuit).
    # DEFAULT adjusted upward from mif_mag_target.yaml (p_pump=1.0).
    p_trit=10.0,
    # D-T tritium processing system power; standard for D-T fusion plants.
    # DEFAULT: framework DT standard.
    p_house=4.0,
    # DEFAULT: housekeeping/auxiliary plant power.
    p_cryo=0.0,
    # No superconducting coils → no cryoplant required.
    # This is a confirmed design feature: liquid metal pressure provides
    # confinement; CT injector uses normal-conducting Cu coils.
    # Source: dossier §Magnet Type; analysis.md §Section 7 (no HTS/cryoplant row).
    # Confidence: high.
    p_target=0.0,
    # No manufactured target consumption: liquid metal liner is self-renewing
    # (reforms each pulse). Eliminates MagLIF-style target factory OPEX.
    # Source: analysis.md §Section 5 Table (consumable cost row);
    #         §Section 7 (no per-shot consumables row).
    # Confidence: high.

    # ── Cost overrides ─────────────────────────────────────────────────────
    cost_overrides={
        # C220103: Coils / Magnet System
        # Commercial design has NO superconducting magnets.
        # Only normal-conducting Cu guide field coils for the CT injector.
        # Eliminates REBCO tape (~$30–100/kA-m) and HTS manufacturing overhead.
        # $10M estimate for Cu injector coils at this scale.
        # Source: analysis.md §Section 7 TEA Implications (no HTS magnet row),
        #         §Section 5 Table (CAS22 ≈ $0 row).
        # Contrast with HTS tokamak CAS22 ~$500–1000M (01-hts-compact-tokamak
        #         §Capital Cost Structure).
        # Confidence: medium (rough Cu coil estimate; no HTS is certain).
        "C220103": 10.0,  # M$ — minimal CT injector Cu guide field coils

        # C220104: Pulsed Power Driver / Compression System
        # UNCERTAIN — no published cost; analysis.md §Section 5 Table notes
        # "truly-unknown" for compression system capital.
        # Modeling hypothesis H1 (analysis.md §Section 5): "the pneumatic
        # compression system will constitute the dominant non-blanket capital
        # account." Floor estimate via industrial analogues:
        #   - Large reciprocating compressor systems: ~$5–20M/MW at scale
        #   - Novel precision engineering premium for fusion environment: 3–5×
        #   - Total piston array + steam supply + liquid metal flow control: $150–400M
        # Using $180M as central estimate; extremely wide uncertainty range.
        # Source: analysis.md §Section 2 Challenge #1 (compression system);
        #         §Section 7 TEA Implications (pneumatic compression row).
        # Confidence: very low — order-of-magnitude only.
        "C220104": 180.0,  # M$ — UNCERTAIN: pneumatic piston array + steam supply capital

        # C220108: Target Factory
        # Eliminated entirely: liquid metal liner is self-renewing.
        # No targets are manufactured or consumed per shot.
        # Contrast with MagLIF (07-maglif) where $0.10–0.25/target × 28M
        # shots/year is a primary cost driver.
        # Source: analysis.md §Section 5 Table (consumable cost row);
        #         §Section 7 TEA Implications (no per-shot consumables row).
        # Confidence: high.
        "C220108": 0.0,  # M$ — no target factory
    },
)

# ── Cost Results by CAS ──────────────────────────────────────────────────────
c = result.costs
pt = result.power_table

print("MTF Pneumatic Compression (D-T) — General Fusion concept")
print(f"  {NET_ELECTRIC_MW:.0f} MWe net, {AVAILABILITY:.0%} availability, {LIFETIME_YR} yr lifetime")
print(f"  FOAK | eta_th={0.35:.0%} | availability={AVAILABILITY:.0%}")
print()
print(f"LCOE:     {c.lcoe:.1f} $/MWh | Overnight: {c.overnight_cost:.0f} $/kW")
print(f"Fusion:   {pt.p_fus:.0f} MW  | Net: {pt.p_net:.0f} MW | Q_eng: {pt.q_eng:.1f}")
print(f"Recirculating fraction: {pt.rec_frac:.1%}")
print(f"Scientific Q (P_fus/P_driver): {pt.q_sci:.1f}")
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

# ── CAS22 sub-account detail ─────────────────────────────────────────────────
print("\nCAS22 Reactor Plant Equipment detail:")
print("-" * 56)
cas22_items = [
    ("C220101", "First Wall / Liquid Metal Wall"),
    ("C220102", "Shield"),
    ("C220103", "Coils (Cu guide field only)"),
    ("C220104", "Compression Driver [UNCERTAIN]"),
    ("C220105", "Primary Structure"),
    ("C220106", "Vacuum System"),
    ("C220107", "Aux Power Supplies"),
    ("C220108", "Target Factory [eliminated]"),
    ("C220109", "Direct Energy Converter"),
    ("C220110", "Remote Handling"),
    ("C220111", "Installation"),
    ("C220200", "Coolant / LM Heat Exchange"),
    ("C220300", "Aux Cooling + Cryo"),
    ("C220400", "Rad Waste"),
    ("C220500", "Fuel Handling (DT)"),
    ("C220600", "Other Equipment"),
    ("C220700", "I&C"),
]
for key, label in cas22_items:
    v = float(result.cas22_detail.get(key, 0.0))
    if v > 0.01:
        print(f"  {key} {label:<32} {v:>8.1f} M$")

print(f"\n  {'':7} {'CAS22 Total':<32} {float(c.cas22):>8.1f} M$")

# ── Overridden accounts ──────────────────────────────────────────────────────
print(f"\nOverridden: {', '.join(result.overridden)}")

# ── Key Assumptions summary ──────────────────────────────────────────────────
print("\nKey Assumptions:")
print("-" * 56)
print(f"  Net electric output:           {NET_ELECTRIC_MW:.0f} MWe (stated commercial target)")
print(f"  Availability (capacity factor): {AVAILABILITY:.0%}  [UNCERTAIN: mech. system]")
print(f"  Thermal efficiency (Rankine):   35%   [UNCERTAIN: 33–40% range]")
print(f"  Avg driver power (p_driver):    50 MW [UNCERTAIN: no design-point data]")
print(f"  Compression driver capital:     $180M [UNCERTAIN: no analogous system]")
print(f"  HTS coils / cryoplant:          None  [high confidence — no magnets in design]")
print(f"  Target factory:                 None  [high confidence — LM reforms each pulse]")
print(f"  Steam cycle (Rankine):          Yes   [shared with tokamak concepts]")
print(f"  Construction time:              {CONSTRUCTION_TIME_YR:.0f} yr")
print(f"  FOAK/NOAK:                      FOAK  [TRL 2–3 compression system]")
print()
print("Modeling notes:")
print("  - BLOCKING unknowns: Q, eta_th, recirculating power fraction.")
print("    All three must be resolved before a reliable LCOE can be derived.")
print("    This model is a scenario anchor, not a prediction.")
print("  - Rep rate (1 Hz target) is embedded in availability and p_driver")
print("    rather than as a direct parameter. Halving rep rate → halving")
print("    annual energy → doubling LCOE from identical capital.")
print("  - C220104 ($180M compression driver) is the dominant unknown.")
print("    Range: $50M (optimistic analogue) to $500M+ (novel engineering).")
print("  - Liquid metal composition (Li vs PbLi) not finalized; affects")
print("    tritium extraction cost (ISS capital) and fire/explosion safety")
print("    infrastructure. Not modeled as separate scenarios here.")
print("  - FM-1 / FM-2 (compression ratio shortfall; piston synchronization)")
print("    are binary physics/engineering failure modes, not LCOE parameters.")

# ── Sensitivity Analysis ─────────────────────────────────────────────────────
sens = model.sensitivity(result.params)

print("\nSensitivity (elasticity = %LCOE / %param)")
print("-" * 48)

print("\nEngineering levers:")
for k, v in sorted(sens["engineering"].items(), key=lambda x: abs(x[1]), reverse=True):
    print(f"  {k:<28} {v:+.4f}")

print("\nFinancial:")
for k, v in sorted(sens["financial"].items(), key=lambda x: abs(x[1]), reverse=True):
    print(f"  {k:<28} {v:+.4f}")
