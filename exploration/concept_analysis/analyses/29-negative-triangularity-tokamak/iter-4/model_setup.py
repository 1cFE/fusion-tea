"""1costingfe model: Negative-Triangularity Tokamak (Firefly Fusion).

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
#    MANTA NT Fusion Pilot Plant (Rutherford et al. 2024)
spec = dict(
    R0=4.55,           # major radius (m) — manta-reference-design.md §2, Table 1
    plasma_t=1.2,      # minor radius a (m) — manta-reference-design.md §2, Table 1
    elon=1.8,          # elongation kappa — manta-reference-design.md §2, Table 1
    # δ = -0.5 (negative triangularity, defining NT feature) — not a CostingInput field
    B=11,              # on-axis magnetic field (T) — manta-reference-design.md §2, Table 1
    p_input=40,        # ICRF auxiliary heating wallplug (MW) — manta-reference-design.md §2, Table 1
                       # Ball et al. show ohmic-only is field-strength-conditional: fails at
                       # ITER-level fields (~5 T), succeeds at SPARC-level (~12 T, Q≈80).
                       # MANTA at 11 T sits near the lower edge of the viable regime — viability
                       # depends on NT confinement scaling (H_NA = 2.0). MANTA reference retains
                       # 40 MW ICRF (110 MHz, He-3 minority heating) regardless.
    n_e=1.95e20,       # volume-averaged electron density (m^-3) — manta-reference-design.md §2, Table 1
    T_e=7.1,           # volume-averaged electron temperature (keV) — manta-reference-design.md §2, Table 1
    plasma_volume=155, # plasma volume (m³) — manta-reference-design.md §2, Table 1
    # P_fus = 450 MW reported but library back-solves from P_native + p_input
    # ip = 10 MA, betan = 1.45, fbs = 0.18 from Table 1 but checking if these are spec keys...
)
P_native = 90         # net electric power (MWe) — manta-reference-design.md §2, Table 1

# 2. Model.
model = CostModel(concept=ConfinementConcept.TOKAMAK, fuel=Fuel.DT)

# 2b. Generic forward — overrides OFF, design-point scale (forward 1 of 3). The
#     library's bare answer for a reactor this size, and the reference a relative
#     override is written against. ALWAYS emit this line (it is mandatory, even
#     when no override references it).
generic = generic_reference(model, spec, P_native)

# 3. Override registry — six fields per entry, transcribed from Section 5b.
overrides = [
    {"account": "C220103", "value": 1500.0, "enabled": True,
     "provenance": "direct", "source": "manta-reference-design.md §7.1, Table C1",
     "cost_basis": "noak",
     "rationale": "MANTA publishes TF coil cost at $1,500M for 18 demountable REBCO HTS coils. "
                  "Breakdown: REBCO tape at $40/kA·m, Inconel 718 structure, 5× fabrication "
                  "factor for superconducting components. Library default is geometry-based "
                  "and may not capture demountable joint costs or window-pane coil geometry."},

    # C220104 (auxiliary heating) not overridden: MANTA reports $370M for 40 MW ICRF,
    # but Ball et al. suggest ohmic-only operation viable at Q=500. Heating requirement
    # genuinely uncertain. Library default will compute from p_input=40 MW in spec.

    {"account": "C220108", "value": 150.0, "enabled": True,
     "provenance": "direct", "source": "manta-reference-design.md §7.1, Table C1",
     "cost_basis": "noak",
     "rationale": "MANTA publishes divertor cost at $150M for double-null tungsten monoblock "
                  "design. NT-specific geometry and reduced heat load (P_SOL = 23.5 MW vs. "
                  "~80 MW for conventional tokamaks) may reduce replacement frequency, but "
                  "capital cost is explicitly stated."},

    {"account": "CAS27", "value": 28.6, "enabled": True,
     "provenance": "direct", "source": "manta-reference-design.md §7.1, Table C4, Table 6",
     "cost_basis": "noak",
     "rationale": "MANTA FLiBe blanket: 169 t × $169/kg = $28.6M (rounded from $28.561M). "
                  "Library default uses solid breeder unit costs inappropriate for liquid "
                  "immersion blanket. This is material-only cost; fabrication/structure "
                  "in C220101. "
                  "NOTE: the library treats CAS27 as a per-site fixed charge, not a "
                  "power-proportional or per-module account, so the 1 GWe fleet cost "
                  "stays at $28.6M regardless of n_mod. Each of the ~11 fleet modules "
                  "needs its own 169-t FLiBe inventory, making the true fleet total "
                  "~$314M; the gap (~$285M, ~$3/MWh LCOE) is a known undercount pending "
                  "per-module CAS27 tracking in the framework."},

    # CAS70 (O&M) not overridden: overrides on CAS70 are silently dropped in 1costingFE
    # (1cFE/1costingfe#106). MANTA assumes ~1 person/MWe staffing at $150k/employee-yr
    # (~$15M/yr for 90 MWe), ~30% below library defaults. Library default retained.
]

# 4. Overrides-on forwards via the shared helper (native + 1 GWe NOAK projection).
native, result_1gw = run_native_and_1gw(
    model, spec=spec, overrides=overrides, p_native=P_native,
)

print_cas_breakdown(generic, native, result_1gw, overrides)
