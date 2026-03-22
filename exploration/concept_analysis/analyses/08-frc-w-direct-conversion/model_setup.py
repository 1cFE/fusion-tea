"""FRC w/ Direct Conversion (Helion Energy) — 1costingfe LCOE Model.

Usage:
    uv run python model_setup.py              # print results to terminal
    uv run python model_setup.py | tee model_output.txt  # also save for synthesis stage

Models a pulsed colliding Field-Reversed Configuration power plant (Helion Energy)
operating on D-He3 fuel with direct electromagnetic energy recovery.

Concept: Helion Energy's commercial FRC concept, targeting Orion (50 MWe, Malaga, WA)
as the first commercial plant (Microsoft PPA, 2028 target). Future fleet: modular
~50 MWe units scaling toward ~500 MWe installations (Nucor partnership).
Sources: helion-milestones-feb2026.md §Orion Specifications;
         helion-website-technology.md §Power Output

Architecture:
  - Bilateral linear machine: two FRC plasmoids formed at opposing ends, accelerated
    by magnetic rail-gun effect, collide at center to merge and heat via reconnection,
    then compressed to fusion conditions. Plasma expansion directly recovers electricity.
    Source: handwritten/08-frc-w-direct-conversion.md §Device Description
  - Modular array of factory-built pulsed FRC generators (~50 MWe each)
  - Direct EM energy recovery (no steam cycle) at ~90% round-trip efficiency
  - Aluminum electromagnetic coils — NOT superconductors, NOT copper.
    Source: contrary-research-helion.md ("regular aluminum magnets," CEO direct quote);
            helion-website-technology.md §Magnets/Coils (~720 miles coaxial cables);
            analysis.md §Section 4 Key Materials
  - D-He3 fuel with ~5% neutron fraction from DD side reactions
    Source: helion-website-technology.md §Fuel; analysis.md §S5 parameter table
  - Sub-ignition operation: high circuit efficiency replaces high Q requirement
  - ARPA-E design point: 50 MW at 2 Hz per module; 40 T reactor compression field
    Source: docslib-helion-arpa-e-presentation.md §Power and Repetition; §Magnetic Fields

Modeling approach:
  Uses the MIF (magneto-inertial fusion) power balance with eta_th=0.90 to represent
  the direct electromagnetic conversion efficiency. f_dec is left at 0 (MIF has no
  DEC pathway); instead, the 90% "thermal" efficiency mimics the round-trip circuit
  efficiency of the expanding-FRC energy recovery mechanism.

  Approximation: the ~5% neutron power deposits in the walls and would NOT be
  recovered at 90% by the EM pathway, but since the neutron fraction is small
  the error is minor.
  Source: analysis.md §S5 (neutron fraction ~5%); dhe3_pulsed_frc.py modeling note

  The MIF cost defaults assume IFE-like architecture (HTS coils, NBI heating, target
  factory). Extensive cost_overrides are required to represent the FRC's aluminum
  pulsed EM coils, capacitor-bank driver, in-situ plasmoid formation, and elimination
  of the steam cycle.

Key deviations from 1costingfe MIF defaults:
  Coil material: aluminum EM coils (not copper, not HTS).
    Source: contrary-research-helion.md; analysis.md §S4 Key Materials.
    Note: Coil cost ($5M/module) covers pulsed aluminum solenoids; structurally
    similar per-module cost to the copper coil estimate in dhe3_pulsed_frc.py.

  Fuel utilization:
    - burn_fraction = 0.10 (vs 0.05 default) — FRC compression burn
    - fuel_recovery = 0.95 — efficient exhaust gas recycling

  Power balance:
    - eta_th = 0.90 (vs 0.40) — direct EM recovery (see UNCERTAIN note in forward())
    - eta_pin = 0.95 (vs 0.30) — modern solid-state IGBT pulsed power
    - mn = 1.0 (vs 1.1) — no breeding blanket (D-He3 eliminates tritium blanket)
    - p_cryo = 0.0 — aluminum coils, no superconductors
    - p_target = 0.0 — FRC plasmoids formed in-situ, not manufactured targets
    - p_trit = 0.5 MW — tritium monitoring from DD side reactions only (not D-T processing)

  Cost overrides (per-module CAS22 sub-accounts):
    - C220103 = $5M  — aluminum pulsed EM coils (vs $516M HTS w/ tokamak markup)
    - C220104 = $10M — capacitor bank + solid-state IGBT switches (vs $353M NBI)
    - C220107 = $3M  — aux power supplies only (main driver is in C220104)
    - C220108 = $0   — no target factory (in-situ FRC plasmoid formation from gas)
    - C220111 = $4M  — installation labor (14% of adjusted reactor subtotal)

  Cost overrides (plant-wide):
    - CAS21 = $400M — no turbine hall, no cryogenics bldg, reduced hot cell,
      added capacitor bank storage + power electronics buildings.
      NOTE: Derived from dhe3_pulsed_frc.py baseline (out of scope); no Helion-specific
      buildings cost source exists. High uncertainty; order-of-magnitude placeholder.
    - CAS23 = $0    — no steam turbine plant (direct EM conversion)
    - CAS26 = $7M   — reduced heat rejection (only ~10% conversion losses)
    - C220200 = $30M — minimal coolant (no steam loop; only coil cooling,
      neutron wall heating ~5%, and EM circuit losses)
"""

from costingfe import ConfinementConcept, CostModel, Fuel
from costingfe.defaults import load_costing_constants

cc = load_costing_constants().replace(
    burn_fraction=0.10,  # FRC compression burn per pulse.
                         # UNCERTAIN: No public Helion burn fraction data.
                         # ARPA-E energy balance (η·Gain=0.2×1.2) implies modest burn;
                         # 10% adopted from dhe3_pulsed_frc.py (same architecture).
                         # Source: analysis.md §S2 Challenge 1;
                         #         docslib-helion-arpa-e-presentation.md §Energy Efficiency
    fuel_recovery=0.95,  # 95% of unburned D-He3 recovered from exhaust.
                         # Standard efficient gas recycling assumption for pulsed FRC.
                         # Source: dhe3_pulsed_frc.py (Helion concept baseline)
)
model = CostModel(
    concept=ConfinementConcept.MAG_TARGET,  # FRC not natively supported in framework.
                                            # MAG_TARGET is architecturally closest:
                                            # pulsed EM driver, compressed plasma, linear geometry.
                                            # Source: model_setup_prompt.md §Concept Mapping;
                                            #         dhe3_pulsed_frc.py
    fuel=Fuel.DHE3,  # D-He3 commercial fuel target. Self-breeding via DD side reactions.
                     # Source: helion-website-technology.md §Fuel;
                     #         analysis.md §S3 (D-He3 Physics, He3 Self-Breeding)
    costing_constants=cc,
)

# ── Plant configuration ──────────────────────────────────────────────
# ARPA-E design point: 50 MW at 2 Hz per module (fusion power output).
# Source: docslib-helion-arpa-e-presentation.md §Power and Repetition
#
# Orion (first commercial plant): 50 MWe+ net; under construction Malaga, WA.
# Source: helion-milestones-feb2026.md §Orion Specifications
#
# This model uses 20 modules x 50 MWe = 1 GWe for normalized cross-concept
# comparison. Orion is a single-module 50 MWe deployment (earliest commercial unit).

N_MODULES = 20
NET_ELECTRIC_MW = 1000.0  # 20 x 50 MWe; normalized fleet-scale for comparison

result = model.forward(
    net_electric_mw=NET_ELECTRIC_MW,
    availability=0.85,        # UNCERTAIN: No published capacity factor for Orion or
                              # any Helion plant. Bank/coil maintenance schedule is
                              # the primary driver (analysis.md §S6 Gap 7: "capacity
                              # factor target for Orion not published").
                              # 85% adopted as standard fusion plant assumption.
    lifetime_yr=30,           # Standard plant lifetime assumption.
    n_mod=N_MODULES,
    construction_time_yr=4.0, # Factory-built modular assembly; compact linear geometry.
                              # Source: mif_mag_target.yaml default (4.0 yr)
    interest_rate=0.07,
    inflation_rate=0.02,
    noak=True,
    # ── Cost overrides ────────────────────────────────────────────
    #
    # The MIF CAS22 defaults assume HTS superconducting coils ($50/kAm with
    # 8x tokamak manufacturing markup), NBI heating systems ($7M/MW), and an
    # IFE-style target/liner factory ($244M base). None apply to a pulsed
    # colliding FRC with aluminum EM coils, capacitor-bank driver, and in-situ
    # plasmoid formation.
    #
    # COIL MATERIAL NOTE: Helion uses aluminum EM coils, not copper.
    # Source: contrary-research-helion.md ("regular aluminum magnets," CEO quote);
    #         helion-website-technology.md §Magnets/Coils (~720 miles coaxial cables);
    #         analysis.md §S4 Key Materials ("Helion uses aluminum electromagnetic coils").
    # The $5M/module estimate covers formation, acceleration, and compression
    # solenoids at commercial aluminum conductor pricing (~$2–3/kg).
    # Source: analysis.md §S4 Key Materials (Aluminum section)
    #
    # Per-module CAS22 sub-accounts (multiplied by n_mod internally):
    #   C220103: Aluminum pulsed EM coils — formation, acceleration, and compression.
    #            Pulsed solenoids using aluminum wire/rod at commodity pricing (~$2-3/kg).
    #            No HTS, no cryogenics required. Low manufacturing markup vs tokamak coils.
    #            Key uncertainty: coil fatigue at 40 T compression field at 1-2 Hz for
    #            30 years (~10^9 shots). analysis.md §S3 (Compression to Reactor Field TRL 3).
    #   C220104: Pulsed power driver — capacitor banks (energy storage), solid-state
    #            IGBT/GTO switches, bus work, and pulse transformers.
    #            Polaris bank: >50 MJ at tens of kV.
    #            Source: helion-website-technology.md §Capacitor Bank
    #            UNCERTAIN: At ~$5/J commercial capacitor price, Polaris-class bank ≈ $250M
    #            (Polaris: >50 MJ; experimental prototype, not a commercial module).
    #            Source: analysis.md §S4 (High-Voltage Capacitors section);
    #                    07-maglif analysis §Key Materials (~$5/J pulsed-power industry estimate)
    #            Helion's in-house manufacturing strategy targets significant cost reduction.
    #            $10M/module assumes ~20 MJ per commercial module (driver point: p_driver=12 MW
    #            at 2 Hz → ~6 MJ/pulse; bank sized at ~20 MJ for headroom) at NOAK $0.50/J.
    #            20 MJ × $0.50/J = $10M. Polaris-scale bank ($250M) is larger and experimental.
    #            Source: analysis.md §S7 Cross-Concept Notes (MagLIF capacitor cost analogy)
    #   C220107: Auxiliary power supplies only — diagnostics, control, vacuum.
    #            Main pulsed driver is costed in C220104. $3M/module.
    #   C220108: No target factory — FRC plasmoids formed in-situ from deuterium gas
    #            via field-reversed theta-pinch. Not manufactured as physical targets.
    #            Source: helion-website-technology.md §Technology (in-situ formation);
    #                    handwritten/08-frc-w-direct-conversion.md §Device Description
    #   C220111: Installation labor at 14% of adjusted reactor subtotal.
    #            Source: costing_constants.yaml installation_frac=0.14
    #
    # Plant-wide overrides:
    #   CAS21: Buildings — remove turbine hall ($54/kW), heat exchanger ($12/kW),
    #          cryogenics bldg ($15/kW). Reduce hot cell (D-He3: 2.45 MeV DD
    #          neutrons vs 14.1 MeV D-T; analysis.md §S4, Neutron Management).
    #          Add capacitor bank storage + power electronics hall.
    #          Net $400M at ~1 GW gross.
    #          Source: costing_constants.yaml building_costs_per_kw;
    #                  analysis.md §S2 Challenge 6; dhe3_pulsed_frc.py baseline
    #   CAS23: No steam turbine plant — direct EM conversion is the core innovation.
    #          "Not requiring turbines saves $127M" at 50 MWe scale.
    #          Source: handwritten/08-frc-w-direct-conversion.md §Quantitative LCOE Model;
    #                  analysis.md §S2 Challenge 6 (No Thermal Cycle)
    #   CAS26: Reduced heat rejection — only ~10% of power as waste heat (eta_th=0.90
    #          implies 10% thermal losses vs ~55% for Rankine cycle).
    #          Source: analysis.md §S2 Challenge 6
    #   C220200: Minimal coolant — no steam loop. Cooling needed for: aluminum coil
    #            resistive losses; first-wall neutron heating (~5% of P_fus from DD
    #            side reactions; analysis.md §S5 neutron fraction); EM circuit losses.
    #            Source: analysis.md §S4 (No Tritium Breeding Blanket section);
    #                    helion-website-technology.md §Neutron Management
    #
    cost_overrides={
        # Per-module reactor equipment
        "C220103": 5.0,   # Aluminum pulsed EM coils [M$/module]
                          # Source: dhe3_pulsed_frc.py; analysis.md §S4 (Al coils, ~$2-3/kg)
                          # UNCERTAIN: Fatigue life at 40 T / ~10^9 shots unvalidated
        "C220104": 10.0,  # Capacitor bank + IGBT switches [M$/module]
                          # Source: dhe3_pulsed_frc.py; analysis.md §S4 (Cap bank section)
                          # UNCERTAIN: Assumes ~20 MJ/module at NOAK $0.50/J = $10M.
                          # Today $5/J × 20 MJ = $100M/module; Polaris bank (>50 MJ) at $5/J ≈ $250M
                          # (Polaris is an experimental prototype, not a commercial module).
        "C220107": 3.0,   # Aux power supplies [M$/module]
                          # Source: dhe3_pulsed_frc.py baseline
        "C220108": 0.0,   # No target factory (in-situ FRC plasmoid formation from gas)
                          # Source: helion-website-technology.md §Technology
        "C220111": 4.0,   # Installation labor (14% of ~$29M per-module subtotal)
                          # Per-module items: $5M coils + $10M cap bank + $3M aux power
                          # + framework defaults for first wall, shield, structure, vacuum,
                          # DEC, remote handling ≈ $11M → subtotal ~$29M; 14% × $29M ≈ $4M.
                          # Source: costing_constants.yaml installation_frac=0.14
        # Plant-wide
        "C220200": 30.0,  # Minimal coolant system (no steam loop) [M$]
                          # Source: analysis.md §S4 (~5% neutron fraction, no thermal cycle)
        "CAS21": 400.0,   # Adjusted buildings (no turbine/cryo/HX halls) [M$]
                          # UNCERTAIN: $400M derives from dhe3_pulsed_frc.py baseline analogue
                          # (itself out of scope for this review), not from Helion-specific
                          # sources. No in-scope source provides a buildings cost estimate.
                          # Uncertainty is high; treat as order-of-magnitude placeholder.
                          # Source: dhe3_pulsed_frc.py; costing_constants.yaml building_costs_per_kw
        "CAS23": 0.0,     # No turbine plant (direct EM conversion)
                          # Source: handwritten §LCOE Model; analysis.md §S2 Challenge 6
        "CAS26": 7.0,     # Reduced heat rejection (~10% thermal losses) [M$]
                          # Source: analysis.md §S2 Challenge 6
    },
    # ── MIF power balance ─────────────────────────────────────────
    # p_driver: average pulsed power delivered to form, accelerate, and compress
    # FRC plasmoids. At ~1 Hz rep rate with ~12 MJ per pulse → 12 MW average.
    # Source: dhe3_pulsed_frc.py baseline (same concept architecture)
    # ARPA-E design point: 50 MW fusion output at 2 Hz per module.
    # Source: docslib-helion-arpa-e-presentation.md §Power and Repetition
    # UNCERTAIN: Actual commercial rep rate not achieved / disclosed on Polaris.
    # Source: analysis.md §S2 Challenge 2; §S6 Gap 6 ("Achieved rep rate on Polaris
    # not reported"). Trenta: ~0.002 Hz demonstrated; Polaris target: ~1 Hz.
    p_driver=12.0,   # Pulsed driver output [MW average per module] — UNCERTAIN
    mn=1.0,          # No neutron multiplier — no breeding blanket required.
                     # D-He3 fuel eliminates tritium breeding blanket entirely.
                     # Source: analysis.md §S4 Key Materials (No Tritium Breeding Blanket);
                     #         helion-website-technology.md §Fuel
    eta_th=0.90,     # UNCERTAIN: Direct EM energy recovery efficiency proxy.
                     # Three conflicting public data points:
                     #   >95% round-trip: subscale demo, >1M pulses with IGBTs.
                     #     Source: dossier.md §Energy Capture (synthesizes 2015 Helion press
                     #     release; not independently verifiable from in-scope sources)
                     #   85-95%: range stated without test conditions.
                     #     Source: contrary-research-helion.md §Energy Recovery
                     #   η=0.70: magnetic energy recovery only (ARPA-E design point).
                     #     Source: docslib-helion-arpa-e-presentation.md §Energy Efficiency
                     #   ~90%: stated in handwritten §Device Description.
                     #     Source: handwritten/08-frc-w-direct-conversion.md §Device Description
                     # 0.90 adopted as central estimate; sensitivity output shows leverage.
                     # Note: ~5% neutron power fraction also converted at 90% (small error).
                     # Source: analysis.md §S2 Challenge 1 and Challenge 6
    eta_p=0.5,       # Pumping efficiency. DEFAULT from MIF defaults.
    eta_pin=0.95,    # Pulsed power wall-plug efficiency (solid-state IGBT).
                     # Modern solid-state switching; demonstrated at subscale.
                     # Source: dossier.md §Energy Capture (IGBT demonstration);
                     #         analysis.md §S3 (Direct Inductive Energy Recovery, TRL 4-5)
    f_sub=0.03,      # Subsystem power fraction. DEFAULT.
    p_pump=0.5,      # Vacuum pumping [MW].
                     # Linear geometry reduces pumping load vs toroidal.
    p_trit=0.5,      # Tritium monitoring only [MW].
                     # D-He3 fuel → DD side reactions produce small tritium inventory.
                     # No tritium breeding blanket required (D-He3 eliminates this).
                     # Monitoring only — NOT full D-T tritium processing.
                     # Source: analysis.md §S4 (No Tritium Breeding Blanket);
                     #         helion-website-technology.md §Fuel (DD→He3 50% + T 50%)
                     # CONTRAST: MIF default = 10.0 MW for full D-T tritium processing
    p_house=2.0,     # Housekeeping [MW].
    p_cryo=0.0,      # No cryogenics — aluminum coils, no superconductors.
                     # Source: contrary-research-helion.md ("regular aluminum magnets");
                     #         analysis.md §S4 Key Materials (Aluminum section)
    p_target=0.0,    # No target manufacturing power — in-situ FRC formation from gas.
                     # Field-reversed theta-pinch forms plasmoids from D2 gas injection.
                     # Source: helion-website-technology.md §Technology;
                     #         handwritten/08-frc-w-direct-conversion.md §Device Description
    p_coils=0.5,     # Formation/acceleration coil average power [MW].
                     # Steady-state guide field coil power during inter-shot period.
    # ── Geometry (cylindrical, per module) ────────────────────────
    # Linear bilateral machine with ~50 MWe per module.
    # ARPA-E design: 20 T experiment / 40 T reactor compression field.
    # Source: docslib-helion-arpa-e-presentation.md §Magnetic Fields
    # Plasma parameters (ARPA-E design point):
    #   Formation density: 1×10²¹ m⁻³; compressed: 1×10²³ m⁻³ (100x compression)
    #   FRC velocity: >300 km/s; plasma lifetime: >1 ms per pulse
    #   Source: docslib-helion-arpa-e-presentation.md §Plasma Parameters;
    #           analysis.md §S5 parameter table
    R0=0.0,           # Linear geometry — no major radius, no toroidal machine.
    plasma_t=0.5,     # Plasma / chamber radius [m].
                      # FRC plasmoid: compact, cm-scale at Polaris; ~0.5 m at reactor scale.
                      # Source: dhe3_pulsed_frc.py baseline; analysis.md §S3
    blanket_t=0.05,   # Thin first wall only — no breeding blanket.
                      # D-He3 neutron fraction ~5% at 2.45 MeV (vs D-T 14.1 MeV).
                      # No FLiBe, no lithium enrichment, no beryllium multiplier.
                      # Source: analysis.md §S4 (No Tritium Breeding Blanket);
                      #         helion-website-technology.md §Neutron Management
    ht_shield_t=0.05, # Minimal shielding — low-energy DD neutrons (2.45 MeV), low flux.
                      # ~1 m borated poly/concrete total at plant boundary.
                      # Comparable to hospital particle beam shielding.
                      # Source: helion-website-technology.md §Neutron Management;
                      #         analysis.md §S4 Key Materials (Neutron Management section)
    structure_t=0.10, # Primary structure [m].
    vessel_t=0.10,    # Vacuum vessel [m].
)

# ── Results ───────────────────────────────────────────────────────────
c = result.costs
pt = result.power_table

print(
    f"FRC w/ Direct Conversion (Helion Energy) — {N_MODULES} modules x "
    f"{NET_ELECTRIC_MW / N_MODULES:.0f} MWe"
)
print(f"  Concept: Pulsed colliding FRC, D-He3 fuel, direct EM energy recovery")
print(f"  Commercial ref: Orion (50 MWe, Malaga WA, 2028 target) — single module")
print(f"  {NET_ELECTRIC_MW:.0f} MWe net, 85% availability, 30 yr lifetime")
print()
lcoe_ckwh = float(c.lcoe) / 10
print(
    f"LCOE: {c.lcoe:.1f} $/MWh ({lcoe_ckwh:.2f} c/kWh)"
    f" | Overnight: {c.overnight_cost:.0f} $/kW"
)
print(f"Fusion: {pt.p_fus:.0f} MW | Net: {pt.p_net:.0f} MW | Q_eng: {pt.q_eng:.1f}")
print(f"Recirculating fraction: {pt.rec_frac:.1%}")
print(f"Scientific Q (P_fus/P_driver): {pt.q_sci:.1f}")
print()

# ── Cost breakdown ────────────────────────────────────────────────────
cas = [
    ("CAS10", "Preconstruction", c.cas10),
    ("CAS21", "Buildings", c.cas21),
    ("CAS22", "Reactor Plant Equipment", c.cas22),
    ("CAS23", "Turbine Plant", c.cas23),
    ("CAS24", "Electrical Plant", c.cas24),
    ("CAS25", "Miscellaneous", c.cas25),
    ("CAS26", "Heat Rejection", c.cas26),
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

# ── CAS22 sub-account detail ─────────────────────────────────────────
print(f"\nCAS22 Reactor Plant Equipment (per-module x {N_MODULES} + plant-wide):")
print("-" * 60)
per_mod_keys = [
    ("C220101", "First Wall / Blanket"),
    ("C220102", "Shield"),
    ("C220103", "Coils (Al pulsed EM)"),
    ("C220104", "Pulsed Driver (cap bank + IGBT)"),
    ("C220105", "Primary Structure"),
    ("C220106", "Vacuum System"),
    ("C220107", "Aux Power Supplies"),
    ("C220108", "Target Factory"),
    ("C220109", "Direct Energy Converter"),
    ("C220110", "Remote Handling"),
    ("C220111", "Installation"),
]
plant_keys = [
    ("C220200", "Coolant Systems"),
    ("C220300", "Aux Cooling + Cryo"),
    ("C220400", "Rad Waste"),
    ("C220500", "Fuel Handling (He-3)"),
    ("C220600", "Other Equipment"),
    ("C220700", "I&C"),
]

per_mod_total = 0.0
for key, label in per_mod_keys:
    v = float(result.cas22_detail.get(key, 0.0))
    per_mod_total += v
    if v > 0.01:
        tot = v * N_MODULES
        print(f"  {key} {label:<30} {v:>8.1f} M$/mod  x{N_MODULES} = {tot:>8.1f}")
print(
    f"  {'':7} {'Per-module subtotal':<30}"
    f" {per_mod_total:>8.1f} M$/mod  x{N_MODULES} = {per_mod_total * N_MODULES:>8.1f}"
)
print()

plant_total = 0.0
for key, label in plant_keys:
    v = float(result.cas22_detail.get(key, 0.0))
    plant_total += v
    if v > 0.01:
        print(f"  {key} {label:<30} {v:>8.1f} M$ (plant-wide)")
print(f"  {'':7} {'Plant-wide subtotal':<30} {plant_total:>8.1f} M$")
print(f"\n  {'':7} {'CAS22 Total':<30} {float(c.cas22):>8.1f} M$")

# ── Overridden accounts ──────────────────────────────────────────────
print(f"\nOverridden: {', '.join(result.overridden)}")

# ── Key assumptions summary ──────────────────────────────────────────
print("\nKey Assumptions:")
print("-" * 60)
print(f"  Direct EM conversion eff (eta_th proxy): {0.90:.0%}")
print(f"    UNCERTAIN — three conflicting public values:")
print(f"      >95% subscale demo  (dossier.md §Energy Capture)")
print(f"      85-95% range        (contrary-research-helion.md §Energy Recovery)")
print(f"      η=0.70 ARPA-E       (docslib-helion-arpa-e-presentation.md §Energy Efficiency)")
print(f"    0.90 is central estimate; see sensitivity output for leverage.")
print(f"  Pulsed power wall-plug eff (eta_pin):    {0.95:.0%}")
print(f"    Source: IGBT solid-state pulsed power (dossier.md §Energy Capture)")
print(f"  Neutron multiplier (mn):                 {1.0}")
print(f"    Source: No breeding blanket (D-He3 eliminates this requirement)")
print(f"            analysis.md §S4; helion-website-technology.md §Fuel")
print(f"  Coil material:                           Aluminum (pulsed EM coils)")
print(f"    Source: contrary-research-helion.md (CEO: 'regular aluminum magnets')")
print(f"  Modules:                                 {N_MODULES} x 50 MWe")
print(f"  Commercial reference:                    Orion = 1 module, 50 MWe")
print(f"    Source: helion-milestones-feb2026.md §Orion Specifications")
print(f"  Construction time:                       4.0 yr (factory-built modular)")
print(f"  Burn fraction:                           {cc.burn_fraction:.0%}  UNCERTAIN")
print(f"    Source: analysis.md §S2 Challenge 1; ARPA-E η·Gain=0.2×1.2")
print(f"  Fuel recovery:                           {cc.fuel_recovery:.0%}")
print(f"  Cryogenics:                              None (aluminum coils)")
print(f"    Source: contrary-research-helion.md (CEO direct quote)")
print(f"  Steam cycle:                             None (CAS23 = $0)")
print(f"    Source: analysis.md §S2 Challenge 6; handwritten §LCOE Model (~$127M/50MWe)")
print(f"  Capacitor bank cost assumption:          NOAK ~$0.50/J or better")
print(f"    UNCERTAIN: Today $5/J → Polaris bank ≈ $250M; NOAK requires ~10x reduction")
print(f"    Source: analysis.md §S4 (High-Voltage Capacitors); 07-maglif §Key Materials")
print()
print("Modeling notes:")
print("  - eta_th=0.90 approximates direct EM recovery; the ~5% neutron power")
print("    fraction is also converted at 90% instead of ~40% thermal, introducing")
print("    a small upward bias in net electric. Neutron fraction:")
print("    helion-website-technology.md §Fuel; analysis.md §S5.")
print("  - He-3 fuel cost: $2M/kg (costing_constants.yaml u_he3=2000000).")
print("    This is the optimistic self-production (self-bred He3) cost estimate.")
print("    Market spot: $2,000–15,000 per NTP liter (~$16,000–120,000/g).")
print("    Source: analysis.md §S4 Key Materials (Helium-3 section).")
print("    UNCERTAIN: He3 startup inventory requirement not published.")
print("    If significant external He3 purchase is needed before self-breeding")
print("    is established, startup fuel cost could dominate LCOE.")
print("    Source: analysis.md §S2 Challenge 4; §S6 Gap 3.")
print("  - Rep rate is the dominant LCOE lever. analysis.md §S2 Challenge 2:")
print("    '1 Hz → 2 Hz doubles energy output from identical capital.'")
print("    ARPA-E design: 2 Hz; Polaris target: ~1 Hz (not yet demonstrated publicly).")
print("    Trenta demonstrated only ~0.002 Hz (500-1000x below commercial target).")
print("    Source: analysis.md §S5; docslib-helion-arpa-e-presentation.md §Power.")
print("  - Coil cost ($5M/mod) covers aluminum pulsed EM solenoids. Key uncertainty:")
print("    fatigue life at 40 T field under ~10^9 pulsed loading cycles per module.")
print("    Source: analysis.md §S3 (Compression to Reactor Field, TRL 3).")
print("  - Capacitor bank ($10M/mod) assumes NOAK volume manufacturing ~$0.50/J.")
print("    Current commercial $5/J → Polaris-scale hardware ≈ $250M/mod.")
print("    Helion's in-house manufacturing is the mitigating strategy.")
print("    Source: analysis.md §S4 (High-Voltage Capacitors and IGBT Switches).")
print("  - No independent TEA exists for Helion (analysis.md §S7 Cross-Concept Notes).")
print("    All quantitative values derive from sparse public disclosures.")
print("    Uncertainty bounds here are substantially wider than for tokamak concepts")
print("    that have Araiinejad & Shirvan (2025) or equivalent peer-reviewed TEA.")

# ── Sensitivity Analysis ─────────────────────────────────────────────
sens = model.sensitivity(result.params)

print("\nSensitivity (elasticity = %LCOE / %param)")
print("-" * 48)

print("\nEngineering levers:")
for k, v in sorted(sens["engineering"].items(), key=lambda x: abs(x[1]), reverse=True):
    print(f"  {k:<28} {v:+.4f}")

print("\nFinancial:")
for k, v in sorted(sens["financial"].items(), key=lambda x: abs(x[1]), reverse=True):
    print(f"  {k:<28} {v:+.4f}")
