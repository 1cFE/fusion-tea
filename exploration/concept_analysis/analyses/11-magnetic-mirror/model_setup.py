"""1costingfe model: Magnetic Mirror (Realta Fusion / CoSMo) (Realta Fusion).

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
    # Central cell geometry
    l_c=50.0,           # analysis.md §5, Table: center cell length (m)
    a_c=0.54,           # analysis.md §5, Table: center cell plasma radius (m)
    B_0c=3.0,           # analysis.md §5, Table: center cell magnetic field (T)

    # End plug geometry
    l_p=4.5,            # analysis.md §5, Table: end plug length per plug (m)
    a_m=0.15,           # analysis.md §5, Table: mirror throat radius (m)
    B_m=25.0,           # analysis.md §5, Table: peak magnetic field at mirror throat (T)
    B_0=4.0,            # analysis.md §5, Table: end plug central field (T)

    # Plasma parameters
    beta_c=0.6,         # analysis.md §5, Table: center cell beta
    n_c=7.5e19,         # analysis.md §5, Table: center cell density (m^-3)
    T_ic=50.0,          # analysis.md §5, Table: ion temperature (keV)
    T_ec=100.0,         # analysis.md §5, Table: electron temperature (keV)

    # End plug plasma
    beta_p0=0.58,       # analysis.md §5, Table: end plug beta
    n_p0=1.66e20,       # analysis.md §5, Table: end plug density (m^-3)

    # Heating
    P_NBI=30.0,         # analysis.md §5, Table: total NBI power both end plugs (MW)
    E_NBI=240.0,        # analysis.md §5, Table: NBI energy (keV)

    # Fusion power
    P_fus=175.0,        # analysis.md §5, Table: fusion power (MW)
)
P_native = 50          # MWe — copied from the analysis Design Point block

# 2. Model.
model = CostModel(concept=ConfinementConcept.MIRROR, fuel=Fuel.DT)

# 2b. Generic forward — overrides OFF, design-point scale (forward 1 of 3). The
#     library's bare answer for a reactor this size, and the reference a relative
#     override is written against. ALWAYS emit this line (it is mandatory, even
#     when no override references it).
generic = generic_reference(model, spec, P_native)

# 3. Override registry — six fields per entry, transcribed from Section 5b.
#    Section 5b states: "zero enabled overrides" due to lack of company-grounded
#    cost data. All cost modeling relies on library defaults and analogues.
overrides = []

# 4. Overrides-on forwards via the shared helper (native + 1 GWe NOAK projection).
native, result_1gw = run_native_and_1gw(
    model, spec=spec, overrides=overrides, p_native=P_native,
)

print_cas_breakdown(generic, native, result_1gw, overrides)
