"""MagLIF (D-T) — 1costingfe costing model setup.

Usage:
    uv run python model_setup.py              # print results to terminal
    uv run python model_setup.py | tee model_output.txt  # also save for synthesis stage

Concept: Magnetized Liner Inertial Fusion — pulsed power implosion of magnetized D-T fuel.
Companies: Pacific Fusion (Santa Cruz, CA); Fuse Energy Technologies (San Leandro, CA).
Confinement family: MIF (Magneto-Inertial Fusion).
ConfinementConcept: MAG_TARGET  |  Fuel: DT

=== MODELING APPROACH AND KEY DEVIATIONS ===

This model uses 1costingfe's MAG_TARGET concept as the framework skeleton, but
MagLIF's cost structure is fundamentally different from any MFE concept in the
framework's training data. The analysis.md (§Section 2) explicitly concludes:

  "Reference-class scaling approaches (1costingfe, ARIES-analogous tools, PROCESS)
   are not applicable to MagLIF because the dominant cost categories — pulsed power
   driver capital, per-shot consumables, rep-rated chamber clearing — have no
   analogues in the databases those tools are built on."

Nevertheless, this script provides a structured cost estimate for cross-concept
comparison purposes, using the Z-IFE SAND2006-7148 study as the primary quantitative
source for all overridable cost accounts. All outputs carry very high uncertainty
(±50-100%+ on capital cost; factor-of-several uncertainty on LCOE).

DESIGN POINT: Z-IFE single-chamber, 0.5 Hz scenario (7.0 ¢/kWeh reference).
This is the "optimistic near-term" case: rep rate beyond baseline (0.1 Hz) but
short of the minimum-COE target (1.0–1.8 Hz) described as "beyond reach of RTL."

KEY DEVIATIONS FROM 1costingfe MAG_TARGET DEFAULTS:

  Power balance:
    - eta_th = 0.42 (Combined Brayton-Rankine, steel chamber; vs 0.40 default)
    - eta_pin = 0.60 (LTD driver wall-plug efficiency; vs 0.30 default)
    - p_cryo = 0.0 (no HTS superconducting magnets; pulsed Cu coils only)
    - p_coils = 0.5 (pre-magnetization coils; small for self-magnetizing target path)
    - p_target = 5.0 (frozen-FLiBe RTL factory load; eliminates 170 MWe steel RTL remanufacturing)

  CAS22 overrides (reactor plant equipment):
    - C220103 = $5M  — Cu pre-magnetization coils (vs HTS ~$100M+ default)
    - C220104 = $372M — pulsed power LTD driver (Z-IFE median; novel cost category)
    - C220109 = $0   — no direct energy conversion (D-T uses thermal cycle, not DEC)

  Geometry:
    - plasma_t = 4.0 m (Z-IFE 4 m radius spherical chamber)
    - blanket_t = 0.80 m (FLiBe thick liquid wall, Z-IFE baseline)
    - R0 = 0.0 (spherical chamber, no toroidal major radius)

  Unchanged from defaults:
    - C220108 (target/RTL factory): kept at framework default ($244M at 1 GWe) —
      Z-IFE costed RTL factory separately but gave no sub-account breakdown
      comparable to 1costingfe's target_factory_base.
    - CAS21 (buildings): kept at framework default — pulsed power halls
      partially offset the cryogenics building removal; net uncertain.
    - CAS70 (O&M): kept at DT default — MagLIF-specific consumable O&M
      (per-shot liner + RTL) not captured; true O&M is likely higher.

SOURCES:
  [Z-IFE] Olson et al. SAND2006-7148, "Z-Inertial Fusion Energy Power Plant Final
          Report," 2006. The only published plant-level systems code for MagLIF class.
          iter-02/sources/z-ife-sand2006-7148-thermal-cycles.md
  [PMF]   Ellison et al. arXiv:2408.15206, "Opportunities in Pulsed Magnetic Fusion
          Energy," 2025. Multi-institutional roadmap including Pacific Fusion/Sandia.
          iter-01/sources/arxiv-2408-15206-pulsed-magnetic-fusion.md
  [PF]    Pacific Fusion / The Fusion Report interview (DS architecture specs).
          iter-02/sources/pacific-fusion-interview-fusion-report.md
"""

from costingfe import ConfinementConcept, CostModel, Fuel

model = CostModel(concept=ConfinementConcept.MAG_TARGET, fuel=Fuel.DT)

# ── Plant configuration constants ────────────────────────────────────────────
# Design point: Z-IFE single-chamber, ~0.5 Hz, 1000 MWe.
# Source: z-ife-sand2006-7148-thermal-cycles.md §3.1.1 (reference plant).

NET_ELECTRIC_MW = 1000.0  # 1 GWe — Z-IFE single-chamber reference plant [Z-IFE §3.1.1]
AVAILABILITY = 0.85       # 85% capacity factor — Z-IFE assumption for thick-liquid-wall
                           # success scenario; UNCERTAIN: depends on undemonstrated
                           # chamber clearing at 0.5 Hz and liquid-wall regeneration.
                           # analysis.md §5: capacity factor 85–90% (success) vs 60–75% (failure)
LIFETIME_YR = 30           # DEFAULT: standard fusion plant lifetime assumption
CONSTRUCTION_YR = 5.0     # UNCERTAIN: 4–6 yr range; longer than compact modular
                           # (no factory-build path yet) but shorter than ITER-class.

# ── Model forward pass ───────────────────────────────────────────────────────

result = model.forward(
    # Customer requirements
    net_electric_mw=NET_ELECTRIC_MW,
    availability=AVAILABILITY,
    lifetime_yr=LIFETIME_YR,
    n_mod=1,                    # Single chamber — Z-IFE single-chamber baseline [Z-IFE §3.1.1.6]
    construction_time_yr=CONSTRUCTION_YR,
    interest_rate=0.07,         # DEFAULT: standard fusion finance rate
    inflation_rate=0.02,        # DEFAULT
    noak=True,                  # NOAK: assuming volume-production driver hardware

    # ── Power balance ────────────────────────────────────────────────────────
    # Z-IFE 0.5 Hz scenario: ~5 GJ/shot fusion yield, ~50 MJ driver energy/shot.
    # Time-averaged driver output: 50 MJ × 0.5 Hz = 25 MW average delivered to target.
    p_driver=25.0,  # Time-averaged pulsed power delivered to target [MW]
                    # UNCERTAIN: derived from yield/gain estimates; Z-IFE scenario-specific.
                    # Source: analysis.md §5, inferred from COE=7.0 ¢/kWeh at 0.5 Hz

    mn=1.1,         # Neutron energy multiplier — FLiBe blanket (Be-9 → 2n)
                    # DEFAULT: same as standard DT blanket
                    # Source: analysis.md §5 / standard DT blanket assumption

    eta_th=0.42,    # Thermal conversion efficiency — Combined Brayton-Rankine, steel chamber
                    # Source: z-ife-sand2006-7148-thermal-cycles.md §3.2
                    # "Combined Brayton-Rankine (recommended) achieves ~42% efficiency"
                    # NOTE: 50% possible with C-C composite chamber [Z-IFE §3.2] but
                    # requires high-T materials not commercially available; analysis.md §3.

    eta_p=0.50,     # DEFAULT: pumping efficiency

    eta_pin=0.60,   # Pulsed power wall-plug efficiency — LTD driver
                    # Source: z-ife-sand2006-7148-thermal-cycles.md §3.1.1.5
                    # "2005 workshop LTD efficiency estimate: 60%"
                    # NOTE: IMG claims ~90% [PMF §3.2] but not verified at plant scale.
                    # analysis.md §5 (Driver efficiency row)

    f_sub=0.03,     # DEFAULT: subsystem power fraction
    f_dec=0.0,      # No direct energy conversion — D-T thermal cycle only (no DEC pathway)
                    # Source: analysis.md §Section 2 (cost disposition table)

    # Parasitic loads
    p_coils=0.5,    # Pre-magnetization coil average power [MW]
                    # Small: Pacific Fusion Oct 2025 self-magnetizing target demonstration
                    # showed external Helmholtz coils can be eliminated entirely.
                    # Source: analysis.md §3 (Target Physics TRL 3-4)
                    # UNCERTAIN: near-zero if self-magnetizing path scales; up to a few MW
                    # if conventional external coils retained.

    p_pump=2.0,     # FLiBe primary loop pumping [MW]
                    # Slightly higher than default (1.0 MW) — FLiBe is a viscous
                    # high-density molten salt requiring larger pumps than aqueous.
                    # Source: analysis.md §3 (Energy Conversion / BOP TRL 6-7)

    p_trit=10.0,    # DEFAULT: tritium processing power [MW]
                    # Standard D-T tritium processing plant.
                    # Source: analysis.md §4 (D-T fuel cycle)

    p_house=4.0,    # DEFAULT: housekeeping power [MW]

    p_cryo=0.0,     # No cryogenic power — no HTS superconducting magnets.
                    # MagLIF uses pulsed copper coils (or none, self-magnetizing).
                    # Key supply-chain advantage vs. all tokamak/stellarator concepts.
                    # Source: analysis.md §Key Differentiators (No superconducting magnets)

    p_target=5.0,   # RTL/liner factory parasitic electrical load [MW]
                    # Z-IFE steel RTL remanufacturing consumed 170 MWe (17% recirculating
                    # power) — forcing adoption of frozen-FLiBe RTL as base case.
                    # Frozen-FLiBe RTL eliminates this burden; residual: cryo-cooling
                    # and automated fabrication of the frozen-FLiBe RTL assemblies.
                    # Source: z-ife-sand2006-7148-thermal-cycles.md §3.1.1.3
                    # UNCERTAIN: no published estimate for frozen-FLiBe RTL factory load.

    # ── Geometry — Z-IFE spherical chamber ──────────────────────────────────
    # Source: z-ife-power-plant-concept.md §Abstract and
    #         z-ife-sand2006-7148-thermal-cycles.md §3.1.1 (chamber dimensions)
    R0=0.0,           # No toroidal major radius — spherical chamber geometry
    plasma_t=4.0,     # Chamber inner radius [m] — "4 m radius chamber" [Z-IFE]
    blanket_t=0.80,   # FLiBe thick liquid wall thickness [m] — "80 cm FLiBe" [Z-IFE]
    ht_shield_t=0.20, # High-temperature shield [m] — DEFAULT order of magnitude
    structure_t=0.15, # Primary structure [m] — DEFAULT
    vessel_t=0.10,    # Vacuum/pressure vessel [m] — DEFAULT

    # ── Cost overrides — CAS22 reactor plant equipment ───────────────────────
    cost_overrides={
        # C220103: Pre-magnetization coils — copper, not superconducting.
        # MagLIF requires only a modest pre-magnetization B-field (~10 T axial),
        # delivered by conventional copper pulsed coils. With Pacific Fusion's
        # self-magnetizing targets (Oct 2025), even these may be eliminated.
        # Compare: HTS superconducting coil default in framework >> $100M.
        # Source: analysis.md §Key Differentiators (No superconducting magnets)
        "C220103": 5.0,  # Copper pre-magnetization coils [M$] — UNCERTAIN: $2-20M range

        # C220104: Pulsed power driver — the dominant novel capital cost item.
        # In MagLIF, the pulsed power driver performs the function of heating/CD
        # systems in a tokamak: it compresses, heats, and implodes the fuel target.
        # Z-IFE bottom-up cost model: $372M median ($862M 95th pctile) for 1 PW LTD.
        # This is for LTD (linear transformer driver) architecture.
        # Modern IMG (Imploding Metal Geometry) architecture — pursued by Pacific Fusion
        # and Fuse Energy — is claimed to be 5-10× cheaper per joule [PMF §3.2.4]
        # but no published plant-scale cost estimate exists for IMG.
        # Using LTD reference as the CONSERVATIVE upper bound.
        # Source: z-ife-sand2006-7148-thermal-cycles.md §3.1.2
        #   "Driver cost $372M median; LTD cavities $358M of that; 12,600 cavities at ~$28k each"
        # UNCERTAIN: ±100%; IMG may be 2-5× lower if component cost targets met.
        "C220104": 372.0,  # Pulsed power driver [M$] — LTD Z-IFE median

        # C220109: Direct Energy Conversion — not applicable.
        # D-T fuel cycle uses a steam/Brayton thermal cycle, not DEC.
        # (DEC is relevant for D-He3 and aneutronic concepts only.)
        "C220109": 0.0,   # No DEC [M$]
    },
    # NOTE — accounts left at defaults with rationale:
    #
    # C220101 (Blanket/FW): FLiBe thick liquid wall. Framework uses volume-based
    #   solid blanket unit costs, which likely OVERestimates FLiBe capital (no
    #   structured breeding assembly required). However, FLiBe handling systems
    #   and freeze/thaw infrastructure may offset. Kept at default as placeholder.
    #
    # C220108 (Target/RTL Factory): RTL + liner fabrication facility.
    #   Z-IFE treated this as a separate direct capital account, but gave no
    #   sub-account breakdown. Framework default $244M at 1 GWe is used as
    #   order-of-magnitude placeholder. UNCERTAIN: cryo ice-layer target production
    #   may cost dramatically more; self-magnetizing non-cryo targets may cost less.
    #
    # CAS21 (Buildings): Pulsed power capacitor banks require large halls
    #   (partially offset by removing cryogenics building). Net change uncertain;
    #   left at DT default (~$800M at 1 GWe).
    #
    # CAS70 (O&M): Framework DT baseline (~$52M/yr at 1 GWe). MagLIF's
    #   per-shot consumable O&M (liner destruction at ~$0.70-10+/shot, RTL at
    #   ~28M assemblies/yr at 1 Hz) is NOT captured here — a major omission.
    #   At $1/shot × 0.5 Hz × 3.15×10^7 s/yr ≈ $15.75M/yr additional O&M.
    #   Source: analysis.md §5 (RTL unit cost ~$0.70/shot historical estimate)
    #   UNCERTAIN: cryo target cost could be $10-10,000+/shot currently.
)

# ── Results ──────────────────────────────────────────────────────────────────
c = result.costs
pt = result.power_table

lcoe_ckwh = float(c.lcoe) / 10

print("MagLIF (D-T) — Pacific Fusion / Fuse Energy Technologies")
print("Z-IFE reference: single chamber, ~0.5 Hz, 1 GWe, thick liquid FLiBe wall")
print("Driver: LTD pulsed power ($372M); eta_pin=60%; eta_th=42% (Brayton-Rankine)")
print()
print(f"LCOE:          {c.lcoe:.1f} $/MWh  ({lcoe_ckwh:.2f} c/kWh)")
print(f"Overnight:     {c.overnight_cost:.0f} $/kW")
print(f"Fusion power:  {pt.p_fus:.0f} MW  |  Net electric: {pt.p_net:.0f} MW")
print(f"Q_eng:         {pt.q_eng:.2f}  |  Q_sci: {pt.q_sci:.1f}")
print(f"Recirc frac:   {pt.rec_frac:.1%}")
print()
print("Z-IFE reference COEs for comparison:")
print("  10-chamber, 0.1 Hz: ~20.0 c/kWh  [Z-IFE §3.1.1.6]  ← baseline scenario")
print("  1-chamber,  0.5 Hz:  ~7.0 c/kWh  [Z-IFE §3.1.1.6]  ← this design point")
print("  2-chamber,  0.5 Hz:  ~5.7 c/kWh  [Z-IFE §3.1.1.6]  ← scale economy case")
print("  Advanced fission:   4–6 c/kWh    [Z-IFE §3.1.1.6]  ← competitive threshold")
print()

# ── CAS breakdown ─────────────────────────────────────────────────────────────
cas = [
    ("CAS10", "Preconstruction", c.cas10),
    ("CAS21", "Buildings", c.cas21),
    ("CAS22", "Reactor Plant Equipment", c.cas22),
    ("CAS23", "Turbine Plant", c.cas23),
    ("CAS24", "Electrical Plant", c.cas24),
    ("CAS25", "Miscellaneous", c.cas25),
    ("CAS26", "Heat Rejection", c.cas26),
    ("CAS27", "Special Materials", c.cas27),
    ("CAS28", "Digital Twin", c.cas28),
    ("CAS29", "Contingency", c.cas29),
    ("CAS30", "Indirect Costs", c.cas30),
    ("CAS40", "Owner's Costs", c.cas40),
    ("CAS50", "Supplementary", c.cas50),
    ("CAS60", "IDC", c.cas60),
    ("CAS70", "O&M (annualized)", c.cas70),
    ("CAS80", "Fuel (annualized)", c.cas80),
    ("CAS90", "Financial", c.cas90),
]

print(f"{'Code':<8} {'Account':<28} {'M$':>10}")
print("-" * 48)
for code, name, val in cas:
    print(f"{code:<8} {name:<28} {float(val):>10.1f}")
print("-" * 48)
print(f"{'':8} {'Total Capital':<28} {float(c.total_capital):>10.1f}")

# ── CAS22 sub-account detail ──────────────────────────────────────────────────
print("\nCAS22 Reactor Plant Equipment breakdown:")
print("-" * 56)
cas22_items = [
    ("C220101", "First Wall / FLiBe Blanket"),
    ("C220102", "Shield"),
    ("C220103", "Pre-magnetization Coils (Cu)"),
    ("C220104", "Pulsed Power Driver (LTD)"),
    ("C220105", "Primary Structure"),
    ("C220106", "Vacuum System"),
    ("C220107", "Power Supplies (aux)"),
    ("C220108", "RTL + Target Factory"),
    ("C220109", "Direct Energy Converter"),
    ("C220110", "Remote Handling"),
    ("C220111", "Installation"),
    ("C220112", "Isotope Separation"),
    ("C220200", "Coolant Systems (FLiBe)"),
    ("C220300", "Aux Cooling / Cryo"),
    ("C220400", "Rad Waste"),
    ("C220500", "Fuel Handling (DT)"),
    ("C220600", "Other Equipment"),
    ("C220700", "I&C"),
]
for key, label in cas22_items:
    v = float(result.cas22_detail.get(key, 0.0))
    if v > 0.01:
        override_flag = " [OVERRIDE]" if key in result.overridden else ""
        print(f"  {key}  {label:<30} {v:>8.1f} M${override_flag}")
print(f"\n  {'':7} {'CAS22 Total':<30} {float(c.cas22):>8.1f} M$")
print(f"\nOverridden accounts: {', '.join(result.overridden)}")

# ── Key Assumptions Summary ───────────────────────────────────────────────────
print("\n" + "=" * 60)
print("KEY ASSUMPTIONS")
print("=" * 60)
print(f"  Net electric:            {NET_ELECTRIC_MW:.0f} MWe (Z-IFE single-chamber ref)")
print(f"  Availability:            {AVAILABILITY:.0%}  (UNCERTAIN: thick-LW success)")
print(f"  Lifetime:                {LIFETIME_YR} yr")
print(f"  Thermal efficiency:      42%   (Brayton-Rankine, steel chamber)")
print(f"  Driver wall-plug eff:    60%   (LTD; IMG claims 90% but unverified)")
print(f"  Driver capital:          $372M (LTD median; IMG may be 5-10× lower)")
print(f"  Rep rate (implied):      ~0.5 Hz (Z-IFE optimized frozen-FLiBe RTL case)")
print(f"  No superconducting magnets (HTS/Nb3Sn fully eliminated)")
print(f"  Thick liquid FLiBe wall (scheduled FW replacement eliminated IF demonstrated)")
print(f"  Frozen-FLiBe RTL (eliminates 170 MWe steel RTL remanufacturing load)")
print()
print("CRITICAL UNCERTAINTIES NOT CAPTURED IN THIS ESTIMATE:")
print("  1. Rep rate achievement: COE scales ~10:1 with rep rate")
print("     (0.1 Hz → ~20 c/kWh; 1.0 Hz → ~5 c/kWh)")
print("  2. Per-shot consumable O&M: target cost must reach <$2/shot")
print("     (currently $0.70/shot historical steel estimate, cryo targets unknown)")
print("  3. Gain scaling unvalidated: GJ-class yields undemonstrated experimentally")
print("  4. IMG driver capital: may be 2-5× lower than $372M LTD reference")
print("  5. Chamber lifetime under GJ-scale repetitive shots: untested environment")
print()
print("  See analysis.md §Section 2 and §Section 6 for full gap inventory.")

# ── Sensitivity Analysis ──────────────────────────────────────────────────────
sens = model.sensitivity(result.params)

print("\n" + "=" * 60)
print("SENSITIVITY (elasticity = %LCOE / %param)")
print("=" * 60)

print("\nEngineering levers:")
for k, v in sorted(sens["engineering"].items(), key=lambda x: abs(x[1]), reverse=True):
    print(f"  {k:<30} {v:+.4f}")

print("\nFinancial:")
for k, v in sorted(sens["financial"].items(), key=lambda x: abs(x[1]), reverse=True):
    print(f"  {k:<30} {v:+.4f}")

print()
print("NOTE: The sensitivity table above reflects standard 1costingfe gradients")
print("and does NOT capture the dominant MagLIF LCOE drivers:")
print("  - Rep rate (no parameter in framework; must be swept as p_driver × scale factor)")
print("  - Per-shot target/RTL cost (not parameterized in CAS70/C220108)")
print("  - Driver capital cost uncertainty (overridden C220104; grad = 0)")
print("For MagLIF, the three dominant LCOE levers identified in analysis.md §2 are:")
print("  1. Rep rate (Hz)      — C220104 cost amortized per MWh")
print("  2. Target $/shot      — variable O&M floor")
print("  3. Driver $/J capital — C220104 scaling with IMG vs LTD architecture")
