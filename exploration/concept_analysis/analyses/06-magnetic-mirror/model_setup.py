"""1costingfe model: Magnetic Mirror (Pale Blue).

WARNING: This concept has NO published reactor design. The analysis (Section 5)
documents that "the 'Pale Blue Fusion CHARM commercial notional plant (150 MWe)'
specified in the design point metadata does not exist in any available source."
No geometry, power balance, materials selections, or subsystem specifications
have been disclosed.

The model below applies 11 bounded-estimate overrides (Section 5b) correcting
systematic mismatches between the library's D-T mirror archetype and CHARM's
p-B11 fuel cycle. Overrides address: eliminated blanket/divertor/tritium/turbine,
reduced shielding, increased RF heating systems, multi-chamber vacuum vessel,
p-B11-specific DEC, and reduced remote handling. All overrides are `derived` from
the family-delta analysis (Section 7) quantifying cost differences vs. D-T mirrors.

LCOE values remain LOW CONFIDENCE due to absent reactor design. The overrides
correct known archetype errors but cannot address unknown parameters (geometry,
power balance, magnet specs, alpha channeling efficiency, DEC efficiency).

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
#    The analysis documents zero published reactor specifications. No geometry,
#    plasma parameters, magnetic field strength, or power balance disclosed.
#    The spec dict is empty because no design parameters exist to transcribe.
spec = dict(
    # No parameters — the CHARM concept has no published reactor design.
    # Section 5 (Design Point Parameters) lists 35 "truly-unknown" blocking gaps.
)
P_native = 150.0  # MWe — orchestrator-assigned for modeling (no company target published)

# 2. Model.
# ConfinementConcept.MIRROR and Fuel.PB11 per the prompt's concept mapping.
# The library's MIRROR archetype likely assumes D-T fuel cycle, which is
# structurally incompatible with p-B11 (no blanket, no divertor, DEC instead
# of thermal cycle, alpha channeling RF systems). The model output will be
# misleading.
model = CostModel(concept=ConfinementConcept.MIRROR, fuel=Fuel.PB11)

# 2b. Generic forward — overrides OFF, design-point scale (forward 1 of 3). The
#     library's bare answer for a reactor this size, and the reference a relative
#     override is written against. ALWAYS emit this line (it is mandatory, even
#     when no override references it).
generic = generic_reference(model, spec, P_native)

# 3. Override registry — six fields per entry, transcribed from Section 5b.
#    Section 5b analysis: "Archetype mismatch requires bounded-estimate overrides"
#    — the MIRROR archetype's D-T baseline includes subsystems that don't exist
#    for p-B11 (blanket, divertor, tritium, thermal cycle) and omits subsystems
#    essential for p-B11 (alpha channeling RF, multi-chamber vessel, DEC for all
#    fusion energy). 10 overrides correct the systematic library errors identified
#    in the family-delta analysis (Section 7).
overrides = [
    # C220101: Blanket — aneutronic p-B11 eliminates tritium breeding
    {
        "account": "C220101",
        "value": 0.20 * generic.cas22_detail["C220101"],
        "enabled": True,
        "cost_basis": "noak", "provenance": "derived",
        "source": "analysis.md §1 (aneutronic), §4 (fuel), §7 (blanket eliminated row)",
        "rationale": (
            "Library's D-T mirror baseline prices tritium-breeding blanket with "
            "lithium + neutron multipliers. CHARM's p-B11 is aneutronic (<1% neutron "
            "energy, Section 1). Only first-wall heat collection remains — thin SS "
            "shell with cooling for bremsstrahlung X-rays (Section 4). 0.20 factor "
            "(80% reduction) reflects elimination of breeding materials, neutron "
            "multipliers, tritium extraction piping. Section 7: ~$200M–$500M savings "
            "vs. D-T tokamak blanket, scaled to 150 MWe."
        ),
    },
    # C220102: Shielding — minimal neutron flux, X-rays only
    {
        "account": "C220102",
        "value": 0.10 * generic.cas22_detail["C220102"],
        "enabled": True,
        "cost_basis": "noak", "provenance": "derived",
        "source": "analysis.md §1 (neutron <1%), §4 (aneutronic), §7 (shielding savings)",
        "rationale": (
            "Library's D-T baseline prices thick neutron shielding (borated steel, "
            "water, concrete) for 14 MeV neutrons. CHARM produces <1% neutron energy "
            "(Section 1). Dominant radiation is bremsstrahlung X-rays, requiring only "
            "thin Pb/W shielding — orders of magnitude less mass. 0.10 factor (90% "
            "reduction) for minimal shielding. Section 7: ~$50M–$150M savings vs. D-T."
        ),
    },
    # C220104: Heating — continuous alpha channeling RF + ponderomotive barriers
    {
        "account": "C220104",
        "value": 3.0 * generic.cas22_detail["C220104"],
        "enabled": True,
        "cost_basis": "noak", "provenance": "derived",
        "source": "analysis.md §2 (RF systems), §3 (Alpha Channeling TRL), §4 (RF supply), §7 (heating penalty)",
        "rationale": (
            "Library's D-T baseline prices NBI/ECRH for startup + sustainment. CHARM "
            "requires continuous alpha channeling RF (MW to 10s MW) extracting He "
            "energy and recycling to protons (Section 2). Section 4: 10–50 gyrotrons "
            "at $2M–$5M each = $50M–$200M RF hardware. Section 7: +$100M–$300M penalty "
            "vs. D-T. 3.0× factor (200% increase) bounds this — alpha channeling RF "
            "operates continuously (not just startup), higher power handling, more "
            "complex than standard ECRH."
        ),
    },
    # C220106: Vacuum — multi-chamber architecture + high-flux helium pumping
    {
        "account": "C220106",
        "value": 2.0 * generic.cas22_detail["C220106"],
        "enabled": True,
        "cost_basis": "noak", "provenance": "derived",
        "source": "analysis.md §2 (multi-chamber), §3 (Vacuum Vessel subsystem), §4 (He pumping), §7 (vessel penalty)",
        "rationale": (
            "Library's D-T baseline prices single-chamber vessel. CHARM's multi-chamber "
            "architecture (fusion + heat exchange + plug, Section 2) requires three "
            "interconnected chambers with plasma flow, RF port penetrations, high-flux "
            "He pumping (Section 4: 550 kg/day for 150 MWe). Section 7: 1.5–3× cost "
            "increase; 2.0× midpoint. Penalty for additional chamber fabrication, port "
            "complexity, vacuum pumping sized for p-B11's 3× He production vs. D-T."
        ),
    },
    # C220108: Divertor — mirrors have axial exhaust, not divertors
    {
        "account": "C220108",
        "value": 0.0,
        "enabled": True,
        "cost_basis": "noak", "provenance": "derived",
        "source": "analysis.md §7 (family-delta, confinement penalty paragraph), dossier.md (mirror confinement)",
        "rationale": (
            "Library may price divertor if assuming closed-field confinement. Magnetic "
            "mirrors have open field lines with axial plasma exhaust (Section 7) — no "
            "divertor. Helium ash removed via axial flow + vacuum pumping (Section 3). "
            "Zero out divertor for mirror geometry. If MIRROR archetype already sets "
            "C220108=0, this override is redundant but harmless."
        ),
    },
    # C220109: DEC — p-B11's 100% charged-particle energy requires DEC for all fusion power
    {
        "account": "C220109",
        "value": 80.0,  # M$ — fixed cost estimate
        "enabled": True,
        "cost_basis": "noak", "provenance": "derived",
        "source": "analysis.md §2 (DEC efficiency), §3 (DEC subsystem TRL), §4 (DEC hardware cost), §7 (DEC penalty)",
        "rationale": (
            "Library's D-T baseline may price small DEC for alphas (~11% fusion power, "
            "Venetian blind) or pure thermal (DEC=0). CHARM's p-B11 produces 100% "
            "charged-particle energy, requiring DEC for all fusion energy (Section 2). "
            "Section 4: $10M–$50M for adiabatic DEC (electrodes + vacuum) or $100M+ "
            "for SWDEC (RF-based, cost unknown). Section 7: $10M–$100M range. Fixed "
            "$80M — upper end of adiabatic range, accounting for higher particle flux "
            "(3 alphas per reaction vs. 1 for D-T) and integration complexity."
        ),
    },
    # CAS23: Turbine — direct conversion only, no thermal cycle
    {
        "account": "CAS23",
        "value": 0.0,
        "enabled": True,
        "cost_basis": "noak", "provenance": "derived",
        "source": "analysis.md §2 (DEC replaces thermal), §7 (turbine eliminated), dossier.md (Energy Capture: Direct)",
        "rationale": (
            "Library's mirror archetype may include thermal cycle (steam turbine) if "
            "assuming some fusion energy captured thermally. CHARM uses DEC only — no "
            "thermal cycle (Section 2, Challenge 4). Dossier confirms 'Energy Capture: "
            "Direct (charged particle)'. Section 7: ~$100M–$150M turbine savings for "
            "150 MWe. Zero out turbine. All fusion energy converted via DEC (C220109) "
            "or lost to bremsstrahlung X-rays (rejected via cooling towers, not turbine)."
        ),
    },
    # CAS27: Special Materials — no tritium inventory for aneutronic fuel
    {
        "account": "CAS27",
        "value": 0.0,
        "enabled": True,
        "cost_basis": "noak", "provenance": "derived",
        "source": "analysis.md §1 (aneutronic), §4 (fuel supply, no tritium), §7 (tritium eliminated), dossier.md (Tritium: N/A)",
        "rationale": (
            "Library's D-T baseline prices initial tritium inventory + blanket fill "
            "(Li compounds, Be). CHARM's p-B11 produces no tritium, requires no breeding "
            "(Section 1, 4). Dossier confirms 'Tritium Breeding: N/A (aneutronic)'. "
            "Section 7: ~$50M capital savings from eliminated tritium systems. Zero out "
            "special materials for p-B11. Only 'special' inventory is boron-11 (natural "
            "boron, cheap) + hydrogen (water electrolysis) — negligible (<$1M/year)."
        ),
    },
    # CAS80: Fuel Cost — p-B11 fuel is abundant and cheap (protons + boron)
    {
        "account": "CAS80",
        "value": 1.0,  # M$/year — fixed annual cost
        "enabled": True,
        "cost_basis": "noak", "provenance": "derived",
        "source": "analysis.md §4 (fuel supply — boron and protons), §7 (tritium eliminated row)",
        "rationale": (
            "Library's D-T baseline prices tritium procurement, deuterium, tritium "
            "processing. CHARM's p-B11 fuel is protons (H from water) + boron-11 "
            "(natural boron, 80% B-11, no enrichment per Section 4). Both abundant and "
            "cheap. Section 4: 'Fuel cost <$1M/year for GWe-class plant'. For 150 MWe, "
            "scales to ~$150k/year, rounded to $1M/year for procurement, storage, "
            "injection. 1–2 orders of magnitude lower than D-T. Section 7: ~$10M–$20M/year "
            "operating cost savings vs. tritium systems."
        ),
    },
    # C220107: Power Supplies — additional RF power supply infrastructure
    {
        "account": "C220107",
        "value": 1.5 * generic.cas22_detail["C220107"],
        "enabled": True,
        "cost_basis": "noak", "provenance": "derived",
        "source": "analysis.md §3 (Alpha Channeling RF), §4 (RF equipment), §7 (heating penalty, RF supplies)",
        "rationale": (
            "Library's baseline prices DC supplies for steady-state SC magnets. CHARM "
            "requires additional power supplies for continuous alpha channeling RF "
            "(10–50 MW RF, Section 3 and 4). RF power supplies + switchgear included "
            "in C220104 equipment cost, but high-voltage, high-frequency power "
            "conditioning adds to C220107 account. 1.5× factor (50% increase) for "
            "additional RF power supply infrastructure beyond library's magnet-only "
            "baseline. Modest vs. 3× heating penalty (C220104) because power supplies "
            "scale sublinearly with RF power (bulk switchgear, not per-gyrotron)."
        ),
    },
    # C220110: Remote Handling — minimal activation, simpler maintenance
    {
        "account": "C220110",
        "value": 0.50 * generic.cas22_detail["C220110"],
        "enabled": True,
        "cost_basis": "noak", "provenance": "derived",
        "source": "analysis.md §3 (First Wall — minimal activation), §4 (aneutronic materials), §7 (remote handling savings)",
        "rationale": (
            "Library's D-T baseline prices rad-hardened remote handling for activated "
            "components (blanket, divertor). CHARM's aneutronic p-B11 produces minimal "
            "activation (<1% neutron flux, Section 1). Section 3: 'minimal activation, "
            "simpler maintenance' for first wall. Section 7: ~$20M–$50M remote handling "
            "savings vs. D-T. 0.50 factor (50% reduction) for elimination of hot-cell "
            "blanket handling and tritium-contaminated component processing. Some remote "
            "handling remains for RF antenna maintenance + first-wall inspection, but "
            "rad-hardening tier far lower than D-T reactors."
        ),
    },
]

# 4. Overrides-on forwards via the shared helper (native + 1 GWe NOAK projection).
native, result_1gw = run_native_and_1gw(
    model, spec=spec, overrides=overrides, p_native=P_native,
)

print_cas_breakdown(generic, native, result_1gw, overrides)

# ── Data Gap Summary ──────────────────────────────────────────────────────────
# The analysis (Section 6) identifies 18 blocking data gaps, including:
#  1. No published reactor design (geometry, power level, materials)
#  2. No power balance or Q_eng target
#  3. No alpha channeling efficiency specification
#  4. No direct energy conversion technology selection or efficiency target
#  5. No bremsstrahlung power fraction estimate
#  6. No magnet conductor type disclosed (HTS, LTS, resistive)
#  7. No mirror geometry (length, radius, aspect ratio)
#  8. No RF wave power requirements (alpha channeling + ponderomotive barriers)
#  9. No vacuum pumping requirements
# 10. No first wall / chamber materials disclosed
# 11. No X-ray shielding or heat rejection requirements
# 12. No capacity factor or availability target
#
# Without these, LCOE modeling is impossible. The values above are library-
# generated placeholders for a generic magnetic mirror, not the CHARM concept.
