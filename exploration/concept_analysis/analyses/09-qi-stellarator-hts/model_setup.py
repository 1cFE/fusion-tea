"""1costingfe model: QI Stellarator HTS (Proxima Fusion / Stellaris).

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
    R0=12.0,             # major radius [m] — stellaris-design-details.md §Table 1
    B=5.86,              # on-axis magnetic field [T] — stellaris-design-details.md §Table 3
    plasma_volume=448.0, # plasma volume [m³] — stellaris-design-details.md §Table 1
    elon=1.0,            # elongation — stellarators typically ~1 (analysis §5 parameter table)
    eta_p=0.0276,        # plasma beta (2.76%) — stellaris-design-details.md §2.3
    p_input=50.0,        # auxiliary heating wallplug [MW] — stellaris-design-
                         # details.md §2.6, Table 1 (50 MW ECRH at 230-240 GHz).
                         # NOT fusion power: p_fus is computed by the library
                         # via the inverse power balance and is not settable
                         # through spec. Prior regen mis-set this to fusion
                         # power 2700 MW, which back-solved to p_fus ≈ 13 GW
                         # for a 1000 MWe plant and inflated LCOE to ~$303/MWh.
                         # F9 now blocks p_input/P_native > 0.5.
)
P_native = 1000.0        # MWe — copied from the analysis Design Point block

# 2. Model.
model = CostModel(concept=ConfinementConcept.STELLARATOR, fuel=Fuel.DT)

# 2b. Generic forward — overrides OFF, design-point scale (forward 1 of 3). The
#     library's bare answer for a reactor this size, and the reference a relative
#     override is written against. ALWAYS emit this line (it is mandatory, even
#     when no override references it).
generic = generic_reference(model, spec, P_native)

# 3. Override registry — six fields per entry, transcribed from Section 5b.
overrides = [
    {"account": "C220103", "value": 0.0, "enabled": False,
     "cost_basis": "noak",
     "provenance": "derived", "source": "stellaris-design-details.md §2.9 Magnets, Table 7",
     "rationale": "Stellaris requires 668-777 km of REBCO HTS tape (6mm width, stacked configuration) "
                  "across 18 non-planar modular coils. The library default for HTS magnets is scaled "
                  "from tokamak TF coil experience (CFS ARC: 156 tonnes HTS at ~$44k/kg CPI-adjusted "
                  "= $6.9B for magnets). Stellaris uses comparable tape length but in complex 3D coil "
                  "geometry never previously manufactured at scale. "
                  "Override formula would be: (tape_length_km × cost_per_km_kA × avg_critical_current_kA) "
                  "+ (coil_structure_mass_tonnes × fabrication_cost_per_tonne_3D_premium). "
                  "This override is DISABLED pending: (1) Proxima or tape suppliers publish $/km pricing "
                  "for NOAK REBCO at 20 T application, (2) SMC demo (2027) provides 3D coil fabrication "
                  "cost data, or (3) Alpha demo (2031) provides validated magnet system cost breakdown. "
                  "Current status: Stellaris paper explicitly notes 'detailed cost analysis of large-scale "
                  "HTS tape production' as a key gap. Until resolved, library default (tokamak-derived) "
                  "is the best available estimate, though it likely underestimates stellarator 3D coil "
                  "complexity premium.",
     "blocked_by": "1cFE/1costingfe#103"},

    {"account": "C220104", "value": 50.0, "enabled": True,
     "cost_basis": "noak",
     "provenance": "direct", "source": "stellaris-design-details.md §2.6 Heating systems, Table 1",
     "rationale": "Stellaris specifies 50 MW ECRH (Electron Cyclotron Resonance Heating) at 230-240 GHz "
                  "for auxiliary heating. This is a direct published value from the design study (Table 1: "
                  "'50 MW ECRH', §2.6: 'X1 mode from high-field side injection'). The library default "
                  "for supplementary heating scales generically with plasma volume and confinement; "
                  "Stellaris provides an explicit design-point heating power. "
                  "The value 50.0 represents MW of installed ECRH capacity. Library costing for C220104 "
                  "uses ITER-era gyrotron costs (~$5-10M/MW for ECRH systems). Stellaris' 230-240 GHz "
                  "requirement is beyond current ITER baseline (170 GHz), which may add R&D premium, "
                  "but the paper assumes 50% gyrotron efficiency (ITER baseline, §2.6), suggesting they "
                  "expect evolutionary rather than revolutionary gyrotron development. "
                  "Note: Helios (Thea Energy QI stellarator, comparable design) uses only 10 MW ECRH "
                  "for startup and 1 MW in ignited phase. Stellaris' 50 MW may reflect more conservative "
                  "plasma confinement assumptions (lower Q_eng target) or different ignition strategy."},

    {"account": "C220108", "value": 0.0, "enabled": False,
     "cost_basis": "noak",
     "provenance": "derived", "source": "stellaris-design-details.md §2.5 Divertor",
     "rationale": "Stellaris uses an island divertor (based on W7-X heritage, leveraging 4/4 magnetic "
                  "island chain at plasma edge) rather than a tokamak-style scrape-off-layer (SOL) "
                  "divertor with X-point. The paper notes this provides 'larger wetted area than tokamak "
                  "Eich-scaling divertor' — a potential advantage for heat handling. "
                  "The library default for C220108 (divertor) is derived from tokamak DEMO designs "
                  "(ITER-style W monoblock cassettes on CuCrZr heat sinks). Island divertor geometry "
                  "differs: targets are distributed around the island chain (larger surface area), "
                  "heat flux may be lower per unit area, but total target area is larger. Manufacturing "
                  "complexity may be comparable (still tungsten tiles with cooling, remote handling), "
                  "but geometry is stellarator-specific. "
                  "This override is DISABLED because: (1) Stellaris paper does not provide divertor "
                  "cost estimate or mass breakdown, (2) W7-X island divertor is at experimental scale "
                  "(~2 t tungsten), not power-plant scale (Stellaris likely 50-100 t), and (3) no "
                  "comparative cost study (island vs SOL divertor at power-plant scale) exists in the "
                  "literature. "
                  "Until W7-X scaling data or Alpha demo provides stellarator divertor cost benchmarks, "
                  "the library default (tokamak SOL divertor cost scaled to surface area) is a reasonable "
                  "proxy. The 'larger wetted area' suggests stellarator divertor may be *more expensive* "
                  "(more tungsten tiles, more remote-handling complexity), not less, so the library "
                  "default may actually underestimate.",
     "blocked_by": "1cFE/1costingfe#104"},
]

# 4. Overrides-on forwards via the shared helper (native + 1 GWe NOAK projection).
native, result_1gw = run_native_and_1gw(
    model, spec=spec, overrides=overrides, p_native=P_native,
)

print_cas_breakdown(generic, native, result_1gw, overrides)
