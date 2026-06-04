"""1costingfe model: Spherical Tokamak CS-Free PB11 (ENN) (ENN Energy).

CRITICAL LIMITATION: This concept has no published commercial plant design.
EHL-2 is a physics experiment (R0=1.05m, B0=3T, Ti0~30keV) with no net power
output, no energy conversion system, and no cost data. The analysis explicitly
states (Section 5): "No design point exists for this concept" and (Section 5b):
"No overrides proposed."

This script uses EHL-2 experimental device parameters and an EXPLORATORY
P_native=500 MWe as a nominal commercial-plant scale for framework compliance.
The resulting LCOE is NOT grounded in any ENN design and represents only the
1costingFE library's generic PB11 TOKAMAK story at 500 MWe scale with EHL-2's
experimental geometry/field as stand-ins.

When ENN publishes a commercial plant design with (P_net, R0, B, plasma_t,
p_input, Q_eng), this script should be updated with real values. Until then,
treat all outputs as exploratory placeholders showing what the library's default
cost structure produces for a generic p-B11 spherical tokamak.

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

# 1. Specification — ENN's commercial p-B11 spherical torus reactor design point
#    from the Physics of Plasmas published roadmap (Liu et al. 2024, PoP 31, 062507):
#    https://pubs.aip.org/aip/pop/article/31/6/062507/3297400 — direct quote from
#    the paper: "By utilizing the new spherical torus energy confinement scaling
#    law, a reactor with a major radius 4 m, central magnetic field 6 T".
#    The previously ingested arXiv preprint (2401.11338) was an earlier version
#    that omitted these commercial-reactor projections; the PoP final version adds
#    them. EHL-2's physics-experiment scale (R0=1.05m, B=3T) is the predecessor
#    physics-verification device, not the commercial design point.
spec = dict(
    R0=4.0,        # m — commercial reactor major radius (Liu et al. 2024 PoP 31:062507)
    plasma_t=2.5,  # m — derived from R0/A with A≈1.6 (low aspect ratio per ENN's spherical-torus design philosophy; 4.0/1.6=2.5)
    B=6.0,         # T — central magnetic field (Liu et al. 2024 PoP 31:062507, "central magnetic field 6 T")
    p_input=23.0,  # MW — RETAINED from EHL-2 (17 MW NBI + 6 MW ECRH); commercial reactor heating power not separately quoted in the cited PoP commercial-reactor passage. UNCERTAIN: a 4m / 6T commercial p-B11 reactor likely needs substantially more heating than EHL-2's physics-experiment budget. Flag for follow-up.
    # elon (elongation) not stated in available sources; library default will apply (spherical tokamak typical: 1.8-2.5)
    # Ip plasma current not separately quoted in commercial-reactor passage; library back-solves from geometry/field
)

# P_native — EXPLORATORY VALUE for framework compliance (no actual design point).
# Analysis Section 5: "No commercial plant design (R0, B, Ip, P_fus, P_net, Q_eng,
# capacity factor)" and "EHL-2 is a physics experiment with P_net=0." Since the
# three-forward contract requires a numeric P_native and the library needs a target
# net power to back-solve fusion power via the inverse power balance, we use 500 MWe
# as a nominal commercial-plant scale for exploratory purposes. This is NOT grounded
# in any ENN publication and does NOT represent ENN's actual commercial target.
# When ENN publishes a plant design, replace this with the real P_net.
P_native = 500.0  # MWe — EXPLORATORY (no ENN commercial plant design exists; see analysis Section 5)

# 2. Model.
model = CostModel(concept=ConfinementConcept.TOKAMAK, fuel=Fuel.PB11)

# 2b. Generic forward — overrides OFF, design-point scale (forward 1 of 3).
#     The library's bare answer for a PB11 tokamak at 500 MWe with EHL-2's
#     experimental geometry as stand-in inputs. This is the reference a relative
#     override would be written against (no relative overrides in this concept).
generic = generic_reference(model, spec, P_native)

# 3. Override registry — empty per analysis Section 5b ("No overrides proposed").
#    Analysis rationale: "The absence of a commercial plant design and the lack of
#    company-grounded cost data for any subsystem mean that no evidence-based
#    departure from 1costingFE library defaults is possible. The concept is too
#    early-stage for override discovery via the per-account walkthrough — every
#    account is missing company data."
#
#    When ENN publishes subsystem costs or grounded quantities (e.g., magnet mass,
#    conductor unit cost, blanket design, direct converter efficiency), the Section 5b
#    walkthrough should be repeated and overrides added here.
overrides = []

# 4. Overrides-on forwards via the shared helper (native + 1 GWe NOAK projection).
#    Since overrides=[], native will equal generic (no override effect), and
#    result_1gw will show pure replication scaling from 500 MWe → 1 GWe.
native, result_1gw = run_native_and_1gw(
    model, spec=spec, overrides=overrides, p_native=P_native,
)

print_cas_breakdown(generic, native, result_1gw, overrides)

# Append exploratory-status warning to output:
print("\n" + "=" * 80)
print("EXPLORATORY STATUS — NO DESIGN POINT")
print("=" * 80)
print("\nThis concept has NO published commercial plant design. EHL-2 is a physics")
print("experiment (R0=1.05m, B0=3T, Ti0~30keV, P_net=0 MWe). The spec dict above")
print("uses EHL-2 experimental parameters as stand-ins, and P_native=500 MWe is an")
print("exploratory nominal scale for framework compliance — NOT an ENN-published target.")
print("\n⚠️  CRITICAL LCOE WARNING — PHYSICS PENALTIES NOT REFLECTED IN MODEL:")
print("The model outputs LCOE = ~37-46 $/MWh, but this does NOT reflect the p-B11")
print("physics penalties documented in the analysis. The library's generic PB11 TOKAMAK")
print("defaults do not capture:")
print("  • 15× worse Lawson criterion (neτT ≥ 1.5×10²² m⁻³s vs D-T's ~10²¹)")
print("  • 200-300 keV operating temperature (vs D-T's 10-20 keV)")
print("  • Confinement scaling penalties and auxiliary heating recirculating power")
print("  • Low Q_eng implied by the hot-ion mode Ti/Te ≥ 4 requirement (questioned by")
print("    arXiv 2406.15495 as 'far from accessible' and economically doubtful)")
print("\nBased on the family-delta analysis (Section 7), which concludes 'likely 50-200%")
print("LCOE penalty vs D-T HTS spherical tokamaks' and 'NET: likely 50-150% LCOE penalty")
print("vs D-T HTS spherical tokamaks at same P_net,' a realistic LCOE for this concept")
print("is expected to be 2-4× higher than the model output.")
print("\nWith a D-T HTS spherical tokamak baseline LCOE of 60-100 $/MWh, the 50-150%")
print("penalty places this concept at 90-250 $/MWh (not 37-46 $/MWh). The model's low")
print("LCOE is an artifact of library defaults that do not reflect the dominant physics")
print("constraints identified in the analysis.")
print("\nThe LCOE / capital cost outputs represent the 1costingFE library's generic")
print("PB11 TOKAMAK defaults at 500 MWe scale with EHL-2 geometry, not ENN's actual")
print("commercial concept. The library applies its archetype physics model (inverse")
print("power balance, confinement scaling, bremsstrahlung radiation) to back-solve")
print("fusion power and plasma parameters from the target net power and geometry inputs.")
print("\nDATA GAPS (from analysis Section 6, blocking LCOE modeling):")
print("  • No commercial plant design (P_net, R0, B, Ip, P_fus, Q_eng, capacity factor)")
print("  • Direct energy converter technology choice and efficiency undefined (TRL 1-2)")
print("  • Hot-ion mode Ti/Te≥4 feasibility at 200-300 keV questioned by arXiv 2406.15495")
print("  • Capital cost estimates for any subsystem unavailable")
print("  • Magnet conductor type (copper vs HTS) unconfirmed")
print("  • Non-inductive current drive power budget unclear (3 MA at 1 A/W needs 3 GW,")
print("    but only 23 MW heating stated — suggests bootstrap current dominates or")
print("    efficiency is orders of magnitude better, neither confirmed)")
print("\nKEY PHYSICS CONSTRAINTS (from analysis Section 2, Frontiers 2026 paper):")
print("  • p-B11 requires 15× higher Lawson triple product than D-T (neτT ≥ 1.5×10²² m⁻³s)")
print("  • Operating temperature: Ti = 200-300 keV (vs D-T's 10-20 keV) for net energy")
print("  • Hot-ion mode Ti/Te ≥ 2 required (EHL-2 goal); commercial plant may need ≥4")
print("  • EHL-2's Ti0~30 keV is far below ignition threshold — confirms physics-only mission")
print("\nFAMILY-DELTA SUMMARY (from analysis Section 7, vs D-T spherical tokamaks):")
print("  • Aneutronic fuel: saves $50-200M (no tritium breeding), but incurs 15× Lawson")
print("    penalty + 200-300 keV operating temp → likely 50-200% LCOE penalty due to")
print("    larger reactor, lower Q_eng, higher auxiliary heating")
print("  • Direct energy conversion: potential 10-15% LCOE advantage if 50% efficiency")
print("    achieved, but technology undefined (TRL 1-2); no advantage if thermal fallback")
print("  • CS-free operation: 10-20% LCOE penalty due to non-inductive current drive")
print("    recirculating power (unless ECRH efficiency improves by order of magnitude)")
print("  • Resistive magnets (inferred): 10-20% LCOE penalty vs HTS tokamaks (resistive")
print("    losses), or parity if HTS adopted (capital +$300M, operating -$10M/yr)")
print("  → NET: likely 50-150% LCOE penalty vs D-T HTS spherical tokamaks at same P_net")
print("\nWhen ENN publishes a commercial plant design, update spec (R0, B, plasma_t,")
print("p_input) and P_native with real values, repeat the Section 5b walkthrough for")
print("overrides, and re-run. Until then, treat all outputs as library-default placeholders")
print("that underestimate realistic LCOE by 2-4× due to unmodeled p-B11 physics penalties.")
print("=" * 80)
