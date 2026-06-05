"""1costingfe model: MTF Pneumatic Compression (General Fusion) (General Fusion).

Usage:
    uv run python model_setup.py              # print results
    uv run python model_setup.py | tee model_output.txt
"""
import sys
from pathlib import Path

# Make the shared three-forward helper importable regardless of where this file
# lives (concept dir or iter-N/ dir): walk up to the scripts/ root.
_SCRIPTS = next(
    p / "scripts"
    for p in Path(__file__).resolve().parents
    if (p / "scripts" / "lib" / "model_setup_helpers.py").exists()
)
sys.path.insert(0, str(_SCRIPTS))

from costingfe import ConfinementConcept, CostModel, Fuel
from lib.model_setup_helpers import (
    generic_reference, run_native_and_1gw, print_cas_breakdown,
)

# 1. Specification — design-point inputs only, at native scale.
#
#    GF MTF commercial plant: 150 MWe per module, two-module architecture
#    (Krotez et al. 2023 SOFE). Modelling one 150 MWe module.
#
#    The MAG_TARGET archetype uses spherical chamber geometry (R0=0.0).
#    plasma_t is the chamber radius, not the tokamak minor radius.
#
#    Key data gaps: fusion power (MWth), Q, and p_input are all unpublished.
#    q_eng (engineering gain) is therefore unknown — library default (3.0) used.
#    eta_th is ENUM-owned (PowerCycle) and cannot appear in spec.
#    eta_pin is a wall-plug efficiency and cannot appear in spec per contract.
#    p_input is not in the MIF forward() signature.
#
#    Published design-point parameters mapped to canonical spec keys:
spec = dict(
    plasma_t=2.0,     # m — chamber radius: 4 m cavity diameter / 2
                      #   (general-fusion-fst-2025-fuel-cycles.md §Abstract:
                      #   "large (~4 m diameter) cavity formed in liquid metal")
    blanket_t=1.5,    # m — liquid metal blanket thickness at 4π coverage
                      #   (general-fusion-fst-2025-fuel-cycles.md §1 Introduction:
                      #   "1.5 m thick liquid metal blanket with 4π coverage")
    f_rep=1.0,        # Hz — commercial repetition rate
                      #   (general-fusion-technical-details.md §Introduction:
                      #   "repeats once per second in a commercial plant")
)
P_native = 150  # MWe — copied from analysis Design Point block (per module)

# 2. Model.
model = CostModel(concept=ConfinementConcept.MAG_TARGET, fuel=Fuel.DT)

# 2b. Generic forward — overrides OFF, design-point scale (forward 1 of 3). The
#     library's bare answer for a reactor this size, and the reference a relative
#     override is written against. ALWAYS emit this line (it is mandatory, even
#     when no override references it).
generic = generic_reference(model, spec, P_native)

# 3. Override registry — six fields per entry, transcribed from Section 5b.
#    Analysis Section 5b: 6 enabled overrides (within expected 3–8 band for Med
#    archetype-fit).
overrides = [
    # C220103 — Confinement magnets: GF MTF has NO external confinement magnets.
    # The plasma is a self-confined compact toroid; compression is mechanical.
    {"account": "C220103", "value": 0.0, "enabled": True,
     "cost_basis": "noak", "provenance": "direct",
     "source": "en-wiki-general-fusion/output.md §Technology",
     "rationale": (
         "GF MTF uses no external confinement magnets. The plasma is a self-confined "
         "compact toroid with magnetic fields sustained by internal plasma currents. "
         "Compression is mechanical (pneumatic pistons), not magnetic. The library "
         "default prices HTS-REBCO guide-field solenoids; this concept has zero "
         "magnet cost."
     )},

    # C220108 — Target factory: GF MTF has no manufactured consumables per shot.
    # The liquid metal liner is recycled, not destroyed.
    {"account": "C220108", "value": 0.0, "enabled": True,
     "cost_basis": "noak", "provenance": "direct",
     "source": "general-fusion-fst-2025-fuel-cycles.md §1 Introduction",
     "rationale": (
         "GF MTF explicitly has 'a pulsed system without manufactured consumables.' "
         "The liquid metal liner is recycled, not destroyed per shot. There is no "
         "target factory. Unlike laser ICF (hohlraum/capsule) or MagLIF (liner + RTL), "
         "GF MTF has zero per-shot consumable hardware. A few milligrams of D-T gas "
         "per pulse is the only consumable, covered by CAS80."
     )},

    # C220104 — Primary pulsed driver: pneumatic piston array replaces laser/pulsed-power.
    # GF positions pistons as fundamentally cheaper than lasers or superconducting magnets.
    {"account": "C220104",
     "value": 0.15 * generic.cas22_detail["C220104"],
     "enabled": True,
     "cost_basis": "noak", "provenance": "derived",
     "source": ("general-fusion-technical-details.md §LM26 section; "
                "en-wiki-general-fusion/output.md §Technology"),
     "rationale": (
         "The primary driver is a pneumatic piston array — steam-driven mechanical "
         "hammers around a sphere. GF positions this as fundamentally cheaper than "
         "lasers or pulsed-power drivers: 'other fusion methods rely on "
         "superconducting coils, lasers, or other expensive equipment.' No dollar "
         "figure is published, but the piston system uses commodity industrial "
         "components (steel hammers, pneumatic cylinders, steam valves, digital "
         "servo controls). The library default for C220104 prices a laser or "
         "pulsed-power driver at $/J; pneumatic pistons are qualitatively a fraction "
         "of this. 15% of the library default is an aggressive but directionally "
         "correct estimate given the architectural simplification. The exact fraction "
         "is highly uncertain. NOAK: steam piston arrays at this scale are commodity "
         "industrial hardware with mature manufacturing; no learning-curve adjustment "
         "needed beyond the library's NOAK baseline."
     )},

    # C220107 — Power supplies / pulsed-power bank: GF MTF is mechanically driven.
    # Only the plasma injector (Marshall gun) needs electrical pulsed power.
    {"account": "C220107",
     "value": 0.10 * generic.cas22_detail["C220107"],
     "enabled": True,
     "cost_basis": "noak", "provenance": "derived",
     "source": "en-wiki-general-fusion/output.md §Technology",
     "rationale": (
         "The library default for C220107 prices a pulsed-power capacitor bank "
         "($/J stored) as the dominant driver cost for electrically-driven pulsed "
         "schemes. GF MTF is mechanically driven — the main compression energy comes "
         "from steam pistons, not electrical pulsed power. The only electrical pulsed "
         "system is the plasma injector capacitor bank (ionizes a few mg of gas via "
         "Marshall gun). This is a small fraction of the pulsed-power cost assumed "
         "for electrically driven concepts. 10% of the library default reflects that "
         "only the injector subsystem draws from this account. NOAK: standard "
         "capacitor bank technology at a small fraction of the reference scale."
     )},

    # C220101 — First wall, blanket & neutron multiplier: flowing liquid metal replaces
    # solid structured blanket. No solid first wall, no solid blanket modules.
    {"account": "C220101",
     "value": 0.40 * generic.cas22_detail["C220101"],
     "enabled": True,
     "cost_basis": "noak", "provenance": "derived",
     "source": "general-fusion-fst-2025-fuel-cycles.md §1 Introduction",
     "rationale": (
         "The GF MTF design replaces a solid structured breeding blanket with a "
         "flowing liquid metal that serves as liner, blanket, breeder, and shield. "
         "No solid first wall, no solid blanket modules, no neutron multiplier "
         "structure. The library default prices solid blanket fabrication (e.g., "
         "HCPB or liquid metal channels in a structured module). The GF approach "
         "needs only a liquid metal containment vessel and pumping infrastructure, "
         "which is structurally simpler. 40% of library default reflects the "
         "remaining cost of the containment vessel, liquid metal piping, and pump "
         "systems, while removing the solid blanket/FW fabrication premium. NOAK: "
         "liquid metal containment and piping is mature industrial technology."
     )},

    # CAS27 — Special materials (initial liquid metal fill).
    {"account": "CAS27", "value": 3.0, "enabled": True,
     "cost_basis": "noak", "provenance": "derived",
     "source": ("general-fusion-fst-2025-fuel-cycles.md §1 Introduction; "
                "en-wiki-general-fusion/output.md §Technology"),
     "rationale": (
         "Initial liquid metal fill for a ~3.5 m outer radius sphere (2 m cavity + "
         "1.5 m blanket) ≈ 146 m³. For pure lithium at ~512 kg/m³ = ~75 tonnes at "
         "~$30/kg ≈ $2.25M. For LLE at ~9400 kg/m³ = ~1370 tonnes at ~$10/kg ≈ "
         "$13.7M. Taking the lithium case (which appears to be the leading candidate "
         "given plasma contamination concerns with LLE), $3M is a reasonable estimate "
         "including procurement and initial charging. This is likely lower than the "
         "library default for special materials ($15M for DT concepts). NOAK: lithium "
         "is a commodity material; $3M reflects market pricing."
     )},
]

# 4. Overrides-on forwards via the shared helper (native + 1 GWe NOAK projection).
native, result_1gw = run_native_and_1gw(
    model, spec=spec, overrides=overrides, p_native=P_native,
)

print_cas_breakdown(generic, native, result_1gw, overrides)

# =============================================================================
# Interpretive Notes for GF MTF Pneumatic Compression
# =============================================================================
print("\n" + "=" * 72)
print("INTERPRETATION OF 1 GWe PROJECTION")
print("=" * 72)
print("""
The 1 GWe LCOE projection above represents the General Fusion MTF
commercial plant conceptual design (Krotez et al. 2023 SOFE), modelled as
one 150 MWe module replicated to ~1 GWe.

This projection reflects:
  • 150 MWe per module, ~7 modules to reach 1 GWe
  • 1 Hz repetition rate (commercial target)
  • D-T fuel with liquid metal blanket (LLE or Li, undecided)
  • Pneumatic piston compression of recycled liquid metal liner
  • Steam Rankine thermal conversion (eta_th from library default)
  • No external confinement magnets (C220103 = $0)
  • No per-shot consumables / target factory (C220108 = $0)

**Critical context (analysis.md §2):**
  1. Fusion power (MWth), energy gain Q, and recirculating power are all
     unpublished. The library's q_eng default (3.0) drives the power
     balance — this is a library assumption, not a company-disclosed value.

  2. LM26 uses electromagnetic theta-pinch compression of a solid lithium
     liner, while the commercial plant uses pneumatic piston compression of
     a liquid metal liner. The compression mechanism, liner state, and
     driver technology differ fundamentally.

  3. The piston system cost override (15% of library C220104) is aggressive
     but directionally grounded in GF's claim that pneumatic pistons are
     "low-cost" relative to lasers and superconducting magnets. No dollar
     figure is published.

  4. The 1 Hz repetition rate requires vacuum re-establishment, liquid
     metal vortex reformation, and piston recharge within ~1 second — none
     demonstrated at commercial scale. The gap between LM26 (1 pulse/day)
     and commercial (1 pulse/second) is a factor of 86,400.

**Data gaps (analysis.md §6):**
  • Fusion power, Q, p_input (blocking) — library defaults drive results
  • Piston system capital cost (important) — no published figure
  • Liquid metal composition undecided (important)
  • O&M breakdown (important) — piston wear, seal replacement unknown
  • Vacuum re-establishment at 1 Hz (important) — undemonstrated
""")
print("=" * 72)
