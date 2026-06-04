"""1costingfe model: Type One Stellarator (Type One Energy).

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
    R0=12.5,             # major radius [m] — cambridge-core-services-aop-cambridge-core-content-view.md §2.4 Table 1
    plasma_t=1.25,       # minor radius [m] — cambridge-core-services-aop-cambridge-core-content-view.md §2.4 Table 1
    B=9.0,               # on-axis magnetic field [T] — cambridge-core-services-aop-cambridge-core-content-view.md §2.4 Table 1
    p_input=20.0,        # auxiliary ECRH power [MW] — cambridge-core-services-aop-cambridge-core-content-view.md §2.4 Table 1
    elon=1.0,            # elongation — stellarators typically ~1 (not specified in sources)
    # NOTE: p_house is library-default (housekeeping ~4 MW for a stellarator). Prior
    # regen mis-set p_house = 800 MW with comment "fusion power" — a transcription
    # error of fusion power into the housekeeping slot, same class of bug as
    # concepts 05/09 p_input. p_house/P_native = 2.3 was driving every p_th-scaled
    # CAS22 account upward and inflating LCOE to $285. F9 ratio validator will be
    # extended to cover p_house and prevent regressions.
)
P_native = 350.0         # MWe — copied from the analysis Design Point block

# 2. Model.
model = CostModel(concept=ConfinementConcept.STELLARATOR, fuel=Fuel.DT)

# 2b. Generic forward — overrides OFF, design-point scale (forward 1 of 3). The
#     library's bare answer for a reactor this size, and the reference a relative
#     override is written against. ALWAYS emit this line (it is mandatory, even
#     when no override references it).
generic = generic_reference(model, spec, P_native)

# 3. Override registry — six fields per entry, transcribed from Section 5b.
overrides = []

# 4. Overrides-on forwards via the shared helper (native + 1 GWe NOAK projection).
native, result_1gw = run_native_and_1gw(
    model, spec=spec, overrides=overrides, p_native=P_native,
)

print_cas_breakdown(generic, native, result_1gw, overrides)
