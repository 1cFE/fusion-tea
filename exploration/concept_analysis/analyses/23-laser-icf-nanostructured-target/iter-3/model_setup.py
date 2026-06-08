"""1costingfe model: Laser ICF Nanostructured Target (Marvel Fusion) (Marvel Fusion).

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
#    From analysis.md Section 5 Design Point Parameters.
#    Marvel Fusion CFE-NANO Pilot Plant (100 MWe, 2033 milestone).
#
#    Archetype-Fit: Low — LASER_IFE is the closest available ConfinementConcept
#    but Marvel's femtosecond DPSSL + nanostructured p-B11 targets depart
#    significantly from the library's nanosecond DT-ICF archetype. Published
#    design-point data is extremely limited (see analysis.md Section 1).
#
#    p_input is unknown: Marvel has published no driver wallplug power figure.
#    The analysis notes that at commercial scale (~500 lasers × kJ-class × 10 Hz
#    / 0.10 WPE), wallplug power would far exceed 100 MWe net output. The pilot
#    laser count is unpublished. We rely on the library's inverse power balance
#    via q_eng (engineering gain) to derive the recirculating power.
#
#    eta_pin: library default 0.10 (10% WPE). LLNL/HB11 cite same target for
#    DPSSL systems. Marvel has not published a WPE target. Femtosecond systems
#    may differ, but eta_pin is ENUM-driven and cannot be overridden in spec.
spec = dict(
    # No p_input: unknown for this concept. Library derives from q_eng.

    # Chamber geometry — no published chamber dimensions from Marvel.
    # Library default plasma_t=4.0m for LASER_IFE is adequate pending data.
    plasma_t=4.0,  # Chamber radius [m] — library default

    # Blanket and shielding geometry — library defaults
    blanket_t=0.80,    # Blanket thickness [m]
    ht_shield_t=0.25,  # Shield thickness [m]

    # Auxiliary power loads
    p_trit=0.0,     # No tritium processing for p-B11 (aneutronic)
    p_cryo=0.0,     # No cryogenics: room-temp solid Si targets, no magnets
    p_target=1.0,   # Target factory power [MW] — library default

    # Target fabrication cost — semiconductor lithography Si nanowire arrays.
    # Marvel patent: ~5,000 targets per 300mm wafer. Per-target cost not
    # published but CEO contrasts favorably vs NIF hohlraum costs. At wafer
    # processing cost ~$3,000/wafer ÷ 5,000 targets = $0.60/target.
    # Library default $0.40/shot is in the right ballpark; use $0.60 to
    # reflect the nanostructured lithography step.
    target_unit_cost=0.60,  # $/shot — derived from wafer cost analogy
)

P_native = 100  # MWe — CORDIS CFE-NANO project record, analysis Design Point

# Helper: number of modules in the 1 GWe fleet (= 10 for P_native=100 MWe).
# Used to express fixed whole-plant costs as per-module values so that the
# framework's ×n_mod CAS22 replication restores the intended plant-level total.
_n_mod_1gw = round(1000 / P_native)

# 2. Model.
model = CostModel(concept=ConfinementConcept.LASER_IFE, fuel=Fuel.PB11)

# 2b. Generic forward — overrides OFF, design-point scale (forward 1 of 3).
generic = generic_reference(model, spec, P_native)

# 3. Override registry — six fields per entry, transcribed from Section 5b.
#    Archetype-Fit: Low → expected 6–12 enabled overrides. Analysis produced 8.
#    All overrides are analyst-derived (provenance: derived); Marvel has published
#    no capital cost estimates.
overrides = [
    # C220101: Blanket — aneutronic energy capture only (no tritium breeding)
    # Frame: per-module (Class U). Anchored to generic.cas22_detail["C220101"] (per-module M$).
    # Framework multiplies by n_mod → fleet total scales correctly.
    {
        "enabled": True,
        "account": "C220101",
        "value": generic.cas22_detail["C220101"] * 0.70,
        "provenance": "derived",
        "source": (
            "dossier.md §Tritium Breeding; "
            "hb11-2025-08-04-assoc-prof-patrick-burr-leads-unsw-team-to/output.md"
        ),
        "rationale": (
            "Aneutronic p-B11 eliminates the tritium-breeding function of the blanket "
            "entirely. No lithium ceramics, no liquid metal breeder, no tritium extraction "
            "loops. The blanket/first-wall must still serve as an energy capture surface "
            "(thermalizing alpha particles) and structural boundary. Dossier: 'p-B11 fuel "
            "cycle produces no tritium and requires no tritium breeding.' UNSW confirms "
            "steel construction for the reaction chamber. 30% cost reduction reflects "
            "elimination of breeding subsystems while retaining the full thermal management "
            "structure (alpha thermalization walls, coolant routing, structural support). "
            "Aligned with concept 04-laser-icf (0.70× on the same account): both concepts "
            "share the identical p-B11 aneutronic fuel cycle and the same physical reasoning "
            "— no tritium breeding, but energy capture blanket structure is retained."
        ),
        "cost_basis": "noak",
    },
    # C220102: Radiation shield — p-B11 produces <1% neutron energy
    # Frame: per-module (Class U). Anchored to generic.cas22_detail["C220102"] (per-module M$).
    # Framework multiplies by n_mod → fleet total scales correctly.
    {
        "enabled": True,
        "account": "C220102",
        "value": generic.cas22_detail["C220102"] * 0.20,
        "provenance": "derived",
        "source": (
            "dossier.md §Neutron Management; "
            "energynewsbulletin-energy-transition-features-articles/output.md §Materials"
        ),
        "rationale": (
            "p-B11 produces <1% neutron energy from side reactions — roughly 2 orders of "
            "magnitude lower neutron flux than D-T. Dossier: 'Thin shielding for secondary "
            "neutrons and X-rays. Hands-on maintenance possible.' The library default sizes "
            "the radiation shield for 14.1 MeV DT neutrons at high wall loading. With ~100x "
            "lower neutron flux, shielding mass and cost scale down drastically. Residual "
            "shielding for secondary neutrons, X-rays from alpha particle thermalization, and "
            "personnel protection still required. 80% cost reduction (more aggressive than "
            "04-laser-icf's 70%) reflects the 10 Hz Marvel design where time-averaged neutron "
            "flux is even more dilute at 100 MWe pilot scale."
        ),
        "cost_basis": "noak",
    },
    # C220104: Femtosecond DPSSL driver — fixed whole-plant cost, expressed per module.
    # Frame: whole-plant fixed (Class U account — framework multiplies by n_mod=10).
    # The laser driver does NOT replicate per module; there is one shared driver per plant.
    # To hold the fleet value flat at $2,000M, the per-module value is $2,000M / n_mod
    # so that framework replication (×n_mod) restores the intended plant total.
    {
        "enabled": True,
        "account": "C220104",
        "value": 2000.0 / _n_mod_1gw,  # $200M/module × 10 modules = $2,000M fleet
        "provenance": "derived",
        "source": (
            "osti-servlets-purl-3008974/output.md §Section 3; "
            "optics-news-16-4-4/output.md §500 lasers needed; "
            "osti-servlets-purl-15013230/output.md §IFE Driver Requirements"
        ),
        "rationale": (
            "Frame: whole-plant fixed. The laser driver does not replicate per module; "
            "the 1 GWe plant requires one shared driver array (~500 beamlines) costing "
            "$2,000M in total. C220104 is a Class U account — the framework multiplies "
            "the per-module value by n_mod=10 to reach the fleet cost. Dividing by "
            "n_mod ($2,000M / 10 = $200M/module) ensures the fleet total stays at "
            "$2,000M rather than scaling to ~$20B. "
            "Marvel's driver uses ~500 femtosecond DPSSL beamlines at kJ-class energy "
            "and 10 Hz. LLNL IFE driver cost target: <$1.5B for a GW-class plant "
            "(osti-servlets-purl-15013230 §Introduction). Marvel's femtosecond CPA "
            "architecture uses a less mature manufacturing base (Ti:sapphire-class gain "
            "media, CPA gratings) with no established IFE-scale production — applying a "
            "1.3–2× technology immaturity premium over the LLNL benchmark. Midpoint: "
            "$1.5B × 1.33 ≈ $2,000M fleet. Sensitivity range: $1,500M–$3,000M. At "
            "500 beamlines this implies $3–6M per beamline (NOAK), consistent with "
            "LLNL analysis showing diodes account for 33–50% of beamline cost at IFE "
            "scale (osti-servlets-purl-3008974 §Section 3). "
            "Note: This override replaces the library's $/J-based driver calculation, "
            "which cannot capture the femtosecond CPA architecture."
        ),
        "cost_basis": "noak",
    },
    # C220106: Vacuum system — simplified IFE chamber, no magnets
    # Frame: per-module (Class U). Anchored to generic.cas22_detail["C220106"] (per-module M$).
    # Framework multiplies by n_mod → fleet total scales correctly.
    {
        "enabled": True,
        "account": "C220106",
        "value": generic.cas22_detail["C220106"] * 0.50,
        "provenance": "derived",
        "source": (
            "dossier.md §Magnet Type; "
            "newatlas-energy-hb11-hydrogen-boron-fusion-clean-energy/output.md §Reactor Design"
        ),
        "rationale": (
            "IFE concepts require a vacuum chamber but not the complex port structures, "
            "cryopumps, or magnet-compatible vacuum vessel of MFE designs. The Marvel "
            "design has no external magnets (eliminating cryopumping for magnet vacuum) "
            "and uses a 'largely empty' reaction chamber. However, at 10 Hz with silicon "
            "nanostructured targets, the vacuum system must handle significant debris "
            "clearing between shots. 50% reduction from the library's IFE default reflects "
            "the simplified geometry (no magnets, no tritium-compatible double containment) "
            "partially offset by debris management requirements."
        ),
        "cost_basis": "noak",
    },
    # C220108: Target factory — semiconductor lithography Si nanowire arrays, 1 GWe scale.
    # Frame: whole-plant fixed (Class U account — framework multiplies by n_mod=10).
    # One centralized factory serves the entire 1 GWe plant; it does NOT replicate per module.
    # To hold the fleet value flat at $200M, the per-module value is $200M / n_mod
    # so that framework replication (×n_mod) restores the intended plant total.
    {
        "enabled": True,
        "account": "C220108",
        "value": 200.0 / _n_mod_1gw,  # $20M/module × 10 modules = $200M fleet
        "provenance": "derived",
        "source": (
            "dossier.md §Driver Technology; "
            "optics-news-15-10-4/output.md §Silicon fuel"
        ),
        "rationale": (
            "Frame: whole-plant fixed. One centralized target factory serves the entire "
            "1 GWe plant; it does not replicate per module. C220108 is a Class U account "
            "— the framework multiplies the per-module value by n_mod=10 to reach the "
            "fleet cost. Dividing by n_mod ($200M / 10 = $20M/module) ensures the fleet "
            "total stays at $200M rather than scaling to ~$2B. "
            "Derivation: At 1 GWe (10 modules, 10 Hz each): 3.15B targets/year = 630,000 "
            "wafers/year (at 5,000 targets/wafer per dossier §Driver Technology). By "
            "semiconductor industry standards, 630,000 wafers/year is a mid-size fab "
            "(modern fabs process 50,000–100,000 wafers/month). A dedicated clean-room "
            "line at this throughput costs $150–300M CAPEX (not a leading-edge logic fab "
            "— the nanostructure geometry uses mature lithography nodes). Midpoint: $200M "
            "fleet total. Per-target CAPEX: $200M / 3.15B targets = $0.063/target. "
            "Contrast with 04-laser-icf: HB11's target factory (complex capacitor-coil "
            "assemblies at ~$5/target) is estimated at $157.5M for a 500 MWe plant. "
            "Marvel's silicon wafer targets eliminate per-target electromagnet assemblies "
            "and cryogenics, but the 10× higher rep rate (10 Hz vs 1 Hz) requires 10× "
            "throughput. Sensitivity range: $150M–$300M fleet."
        ),
        "cost_basis": "noak",
    },
    # CAS21: Buildings — no tritium or cryogenic infrastructure
    # Frame: whole-plant fixed (Class S). Anchored to generic.costs.cas21 (whole-plant M$).
    # CAS21 is charged once per site — does not multiply by n_mod. Scales correctly.
    {
        "enabled": True,
        "account": "CAS21",
        "value": generic.costs.cas21 * 0.75,
        "provenance": "derived",
        "source": (
            "dossier.md §Tritium Breeding; "
            "marvel-fusion-2025-updates.md §Objective"
        ),
        "rationale": (
            "Aneutronic p-B11 eliminates tritium processing buildings, hot cells for blanket "
            "handling under tritium containment, atmospheric recovery systems, radioactive "
            "waste storage structures, and cryogenic target handling facilities. The reactor "
            "building and turbine hall remain (hybrid thermal + direct conversion requires "
            "both). Support building footprint is reduced. Siemens Energy co-developing "
            "'fully integrated fusion power plant' design suggests conventional BOP building "
            "standards where applicable. 25% cost reduction vs. library's DT-ICF building "
            "model reflects eliminated tritium and cryogenic infrastructure. Slightly less "
            "aggressive than 04-laser-icf (20% reduction) because Marvel's 10 Hz target "
            "injection and debris management may require additional facility infrastructure."
        ),
        "cost_basis": "noak",
    },
    # CAS27: Special materials — p-B11 fuel inventory only
    # Frame: per-module (Class P, power-proportional). Value is negligible ($0.5M/module);
    # framework multiplies by n_mod → fleet total $5M, which is still negligible.
    # No material impact either way; per-module framing is correct for initial inventory.
    {
        "enabled": True,
        "account": "CAS27",
        "value": 0.5,
        "provenance": "derived",
        "source": (
            "dossier.md §Fuel; "
            "energynewsbulletin-energy-transition-features-articles/output.md §Fuel"
        ),
        "rationale": (
            "Special materials inventory for p-B11: initial boron-11 fuel load and hydrogen "
            "supply only. Natural boron is 80% B-11, commodity cost ~$1-2/kg. At microgram-to-"
            "milligram quantities per target x startup inventory for 1 week at 10 Hz = 6.048M "
            "targets, total boron mass is negligible (< 100 kg at ~0.01 mg/target estimate, "
            "yielding < $200 material cost). Round to $500k ($0.5M) including handling, "
            "storage, buffer inventory, and hydrogen supply infrastructure. Negligible "
            "compared to DT tritium inventory costs (~$30k/g x kg quantities). No lithium "
            "blanket inventory, no enriched materials."
        ),
        "cost_basis": "noak",
    },
    # CAS70: O&M — reduced activation-driven replacement, modular laser maintenance
    # Frame: whole-plant (Class S). NOTE: CAS70 overrides are silently dropped by the
    # framework today (1cFE/1costingfe#106) — this entry has no effect on the headline.
    # Retained in the registry so the analytical intent is documented and a future
    # override surface will pick it up without requiring a model revision.
    {
        "enabled": True,
        "account": "CAS70",
        "value": generic.costs.cas70 * 0.80,
        "provenance": "derived",
        "source": (
            "energynewsbulletin-energy-transition-features-articles/output.md §Materials; "
            "dossier.md §Neutron Management"
        ),
        "rationale": (
            "Aneutronic operation eliminates activation-driven first-wall and blanket "
            "replacement — the dominant O&M cost driver in DT fusion. Dossier: 'Hands-on "
            "maintenance possible.' Chamber walls may last the full plant lifetime if alpha "
            "particle erosion is manageable (unverified assumption). No tritium handling O&M "
            "(extraction, purification, accountability). However, the laser driver system "
            "requires periodic diode bar replacement (the LLNL paper flags diode lifetime as "
            "a 'critical cost driver' with 3-20 Gshot requirement). At 10 Hz, 1 Gshot = "
            "~3.2 years — replacement intervals of 10-64 years depending on achieved "
            "lifetime. Laser optics also degrade under operation. 20% O&M reduction vs. "
            "library DT-ICF model reflects lower activation-driven replacement, partially "
            "offset by laser subsystem maintenance. Consistent with concept 04-laser-icf "
            "approach (15% reduction; Marvel gets slightly larger reduction due to higher "
            "rep rate amortizing fixed O&M costs more efficiently)."
        ),
        "cost_basis": "noak",
    },
]

# 4. Overrides-on forwards via the shared helper (native + 1 GWe NOAK projection).
native, result_1gw = run_native_and_1gw(
    model, spec=spec, overrides=overrides, p_native=P_native,
)

print_cas_breakdown(generic, native, result_1gw, overrides)
