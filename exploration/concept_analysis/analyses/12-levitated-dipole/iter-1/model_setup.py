"""1costingfe model: Levitated Dipole (OpenStar Technologies).

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
#    Geometry / physics / power. NO library-default re-passing.
spec = dict(
    R0=5.3,              # arxiv-2602-20564-dt-dipole-power-plants.md §Table 7
    B=6.26,              # arxiv-2602-20564-dt-dipole-power-plants.md §Table 7 (B_center)
    p_input=44.5,        # arxiv-2602-20564-dt-dipole-power-plants.md §Table 5 (ICRH wallplug)
    mn=1.11,             # arxiv-2602-20564-dt-dipole-power-plants.md §Table 2 (blanket multiplication)
    # NOTE: availability (0.96 per Simpson §Table 5) is intentionally OMITTED —
    # library-owned, sourced by the helper from default_availability(concept).
    #
    # NOTE: plasma_volume is intentionally OMITTED per DIPOLE archetype-specific
    # blocklist (see contract Rule 3). The geometric volume is 13,600 m³ (Simpson
    # Table 7), but 1costingFE's uniform-density radiation calc treats it as a
    # tokamak integrator (n_e² × V), producing radiation × 68 over-estimate for
    # a dipole's highly peaked n ∝ R⁻⁴ profile. Library uses effective 200 m³
    # default to keep p_fus sane. Proper fix: radiation_peaking_factor field
    # (1cFE/1costingfe#24).
    #
    # NOTE: eta_th is intentionally OMITTED per power-conversion efficiency policy
    # (Rule 3). Simpson §Table 2 reports eta_th = 0.40 (40% thermal-to-electric),
    # but conversion efficiencies are framework-owned defaults to keep cross-concept
    # LCOE comparisons apples-to-apples. Accept the library's DIPOLE default.
    #
    # NOTE: fusion_power (667 MW per Simpson Table 5) is NOT a spec key — p_fus
    # is back-solved by the library from p_input + plasma params via inverse
    # power balance. Documented here for reference only.
)
P_native = 208.0     # MWe — arxiv-2602-20564-dt-dipole-power-plants.md §Table 5

# 2. Model.
model = CostModel(concept=ConfinementConcept.DIPOLE, fuel=Fuel.DT)

# 2b. Generic forward — overrides OFF, design-point scale (forward 1 of 3).
#     Mandatory reference frame for relative overrides. See contract Rule 2b.
generic = generic_reference(model, spec, P_native)

# 3. Override registry — six fields per entry, transcribed from Section 5b.
overrides = [
    {
        "account": "C220104",
        "value": 0.70 * generic.cas22_detail["C220104"],
        "enabled": True,
        "provenance": "direct",
        "source": "arxiv-2602-20564-dt-dipole-power-plants.md §Table 2; §Table 5",
        "rationale": (
            "Reactor A uses ICRH at 70% source efficiency (Simpson Table 2), delivering "
            "44.5 MW wallplug auxiliary heating (Table 5). The library's generic heating "
            "system efficiency is ~50% (tokamak NBI/ECRH average). ICRH at 70% is more "
            "efficient than baseline, reducing the heating system capital cost per installed MW. "
            "The override represents 70% of the library's per-module heating system cost for "
            "this dipole's modular fleet. The library default assumes lower-efficiency heating; "
            "ICRH's higher efficiency allows smaller, cheaper RF power supplies and less waste "
            "heat rejection. At the 1 GWe fleet headline (n_mod modules of Reactor A), each "
            "module needs 44.5 MW ICRH wallplug. The 0.70 multiplier applies to the library's "
            "per-module heating cost, and the ×n_mod scaling happens in the CAS22 rollup, not "
            "in this detail row."
        ),
        "cost_basis": "noak",
    },
    {
        "account": "C220108",
        "value": 0.5 * generic.cas22_detail["C220108"],
        "enabled": True,
        "provenance": "derived",
        "source": "arxiv-2602-20564-dt-dipole-power-plants.md §Table 8",
        "rationale": (
            "Reactor A achieves peak neutron wall loading of 0.753 MW/m² (Simpson Table 8), "
            "30-70% lower than tokamak designs (1-2.5 MW/m²). The library's divertor cost "
            "scales with wall loading and heat flux. Lower wall loading reduces divertor heat "
            "sink mass, coolant flow rates, and replacement frequency. The dipole has no "
            "conventional divertor — plasma losses exit through magnetic cusps at the vessel "
            "top/bottom. However, those regions still require heat-handling components analogous "
            "to divertor tiles. The 0.5 multiplier reflects: (a) Lower heat flux per unit area "
            "(50% reduction vs. tokamak), (b) Distributed loss pattern (no single high-heat-flux "
            "strike point), (c) Steady-state operation (no ELM transients). Relative to the "
            "library's 1 GWe modular-fleet divertor cost (which assumes tokamak-level heat flux), "
            "this dipole's per-module heat-handling hardware is approximately half the cost. The "
            "fleet-level cost is this per-module value ×n_mod."
        ),
        "cost_basis": "noak",
    },
]

# 4. Overrides-on forwards via the shared helper (native + 1 GWe NOAK projection).
native, result_1gw = run_native_and_1gw(
    model, spec=spec, overrides=overrides, p_native=P_native,
)

print_cas_breakdown(generic, native, result_1gw, overrides)
