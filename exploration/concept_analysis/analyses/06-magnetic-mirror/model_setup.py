"""1costingfe model: Magnetic Mirror (Pale Blue) (Pale Blue).

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
#
# NOTE: The analysis Section 5 states "no quantitative reactor parameters
# (geometry, fields, densities, temperatures, confinement times, fusion power)
# are disclosed for the CHARM commercial plant." The design point is
# operator-authored with no public specifications. The spec dict is empty
# because no design-point inputs are available.
spec = dict(
    r_bore=2.75,         # = plasma_t (1.5m library default) + radial build
                         # (blanket_t 0.6 + ht_shield_t 0.25 + structure_t 0.15
                         # + vessel_t 0.1 = 1.10m). Axisymmetric solenoidal
                         # coils for an open-ended mirror; library defaults
                         # r_bore to 1.85m which under-sizes the coil bore.
)
P_native = 150.0         # MWe — Design Point specification

# 2. Model.
model = CostModel(concept=ConfinementConcept.MIRROR, fuel=Fuel.PB11)

# 2b. Generic forward — overrides OFF, design-point scale (forward 1 of 3). The
#     library's bare answer for a reactor this size, and the reference a relative
#     override is written against. ALWAYS emit this line (it is mandatory, even
#     when no override references it).
generic = generic_reference(model, spec, P_native)

# 3. Override registry — six fields per entry, transcribed from Section 5b.
overrides = [
    {
        "account": "C220101",
        "value": 0.0,
        "enabled": True,
        "cost_basis": "noak",
        "provenance": "derived",
        "source": "dossier.md §Tritium Breeding; p-B11 fuel cycle physics",
        "rationale": (
            "This account costs the tritium-breeding blanket. CHARM uses p-B11 fuel, which produces "
            "no tritium and requires no breeding blanket. The aneutronic reaction produces 3 alpha "
            "particles per fusion event with <1% neutron energy from side reactions. No blanket "
            "structure is required for tritium breeding or neutron energy capture (DEC captures "
            "charged particle energy directly). Cost is zero."
        ),
    },
    {
        "account": "C220102",
        "value": 0.01 * generic.cas22_detail["C220102"],
        "enabled": True,
        "cost_basis": "noak",
        "provenance": "derived",
        "source": "dossier.md §Neutron Management; p-B11 reaction physics",
        "rationale": (
            "This account costs the radiation shield sized to neutron wall loading. p-B11 is truly "
            "aneutronic (<1% neutron energy from side reactions vs 80% for D-T). Shielding requirements "
            "are minimal — primarily for x-ray bremsstrahlung and trace side-reaction neutrons. The "
            "library default assumes 14.1 MeV D-T neutron shielding; this concept requires ~1% of that "
            "mass. Override to 1% of library value."
        ),
    },
    {
        "account": "C220108",
        "value": 0.0,
        "enabled": True,
        "cost_basis": "noak",
        "provenance": "derived",
        "source": "dossier.md §Operation Mode (steady-state); multi-chamber architecture",
        "rationale": (
            "This account costs the divertor (W monoblock cassettes for steady-state heat/particle "
            "exhaust in D-T mirrors). CHARM uses a multi-chamber architecture where helium ash is "
            "extracted via wave-induced diffusion to a separate heat exchange chamber, then removed "
            "from the system. The presentation states 'Helium is extracted from heat exchange chamber "
            "using waves' (arpa-e-2025-fisch-presentation-notes.md). This is not a divertor in the "
            "conventional sense. The heat exchange chamber may have cost, but it is not captured by "
            "the divertor account. Cost is zero; heat exchange chamber should be a custom override "
            "if data becomes available."
        ),
    },
    {
        "account": "C220109",
        "value": 0.0,
        "enabled": False,
        "cost_basis": "noak",
        "provenance": "derived",
        "source": "dossier.md §Energy Capture; PRX Energy 2025 paper; SWDEC patent US20230298771",
        "rationale": (
            "This account costs direct energy conversion hardware. CHARM absolutely requires DEC "
            "(charged particle exhaust → electricity), but the technology choice (adiabatic DEC vs "
            "SWDEC vs electrostatic collectors) and cost are completely unspecified. The library "
            "has no default for novel DEC hardware. Placeholder disabled until Pale Blue discloses "
            "DEC technology and provides cost estimate or analogue. This is a CRITICAL missing override."
        ),
        "blocked_by": "1cFE/1costingfe#104",
    },
    {
        "account": "CAS23",
        "value": 0.0,
        "enabled": True,
        "cost_basis": "noak",
        "provenance": "derived",
        "source": "dossier.md §Energy Capture (Direct charged particle)",
        "rationale": (
            "This account costs turbine plant equipment (thermal cycle). CHARM uses direct energy "
            "conversion; there is no steam or sCO2 thermal cycle. Fusion energy is captured as "
            "charged particle kinetic energy and converted to electricity via DEC (account C220109). "
            "Turbine cost is zero."
        ),
    },
    {
        "account": "CAS27",
        "value": 0.0,
        "enabled": True,
        "cost_basis": "noak",
        "provenance": "derived",
        "source": "dossier.md §Tritium Breeding (N/A aneutronic); p-B11 fuel cycle",
        "rationale": (
            "This account costs special materials (initial reactor material inventory / blanket fill). "
            "For D-T, this is FLiBe or liquid metal breeder inventory. CHARM has no breeder. Boron "
            "fuel inventory is negligible cost (commodity material, ~$2-5/kg). Cost is zero."
        ),
    },
    {
        "account": "CAS80",
        "value": 0.0,
        "enabled": True,
        "cost_basis": "noak",
        "provenance": "derived",
        "source": "princeton-arpa-e-funding-2022.md §A different kind of fusion reaction",
        "rationale": (
            "This account costs annualized fuel (D-T consumables and enriched-isotope procurement). "
            "p-B11 fuel is commodity hydrogen and natural boron. The source states 'both protons and "
            "boron-11 are readily available, naturally and cheaply.' At any reasonable plant scale, "
            "annual fuel cost is <$1M and negligible vs capital. Override to zero."
        ),
    },
]

# 4. Overrides-on forwards via the shared helper (native + 1 GWe NOAK projection).
native, result_1gw = run_native_and_1gw(
    model, spec=spec, overrides=overrides, p_native=P_native,
)

print_cas_breakdown(generic, native, result_1gw, overrides, data_grounded=False)
# data_grounded=False: Pale Blue Fusion has disclosed no quantitative reactor
# parameters for the CHARM commercial plant (geometry, fields, densities,
# temperatures, confinement times, fusion power per analysis.md §5). The spec
# dict is empty by necessity, so the LCOE would otherwise reflect pure MIRROR
# YAML defaults rather than CHARM's actual design. Headline LCOE lines emit
# (NOT ENOUGH DATA FOR THIS CONCEPT); CAS22 breakdown below still prints so
# a reviewer can see what library defaults produced.
