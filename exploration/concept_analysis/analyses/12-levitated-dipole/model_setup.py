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
#    Geometry / physics / power from Simpson et al. 2026, arXiv 2602.20564
spec = dict(
    R0=7.1,              # Core magnet outer radius (m) — Table 5
    plasma_volume=1.36e4,  # Plasma volume (m³) — Table 6
    p_input=44.5,        # Auxiliary heating (MW) — ICRH, Table 5
)
P_native = 208.0  # Net electric power (MWe) — Table 5, 9

# 2. Model.
model = CostModel(concept=ConfinementConcept.DIPOLE, fuel=Fuel.DT)

# 2b. Generic forward — overrides OFF, design-point scale (forward 1 of 3). The
#     library's bare answer for a reactor this size, and the reference a relative
#     override is written against. ALWAYS emit this line (it is mandatory, even
#     when no override references it).
generic = generic_reference(model, spec, P_native)

# 3. Override registry — six fields per entry, transcribed from Section 5b.
#    The original C220105 concrete-vessel override (F-1 from earlier iterations)
#    was diagnosed in fusion-tea/validation_reviews/12-openstar-1costingfe-issues.md
#    as a **unit error** (raw $20e6 instead of $20.0 M$), not a library bug. With
#    1costingfe PR#23 the DIPOLE YAML radial-build defaults are inverted to match
#    Simpson Reactor A (vessel_t=8mm Inconel, vessel_or≈20.6m), so vessel cost
#    lands correctly in C220106 (vacuum system) at ~$15.8M out-of-the-box, near
#    Simpson's $14M bottom-up. No per-concept vessel override is needed; the
#    archetype default now models the dipole VV correctly.
overrides = []

# 4. Overrides-on forwards via the shared helper (native + 1 GWe NOAK projection).
native, result_1gw = run_native_and_1gw(
    model, spec=spec, overrides=overrides, p_native=P_native,
)

print_cas_breakdown(generic, native, result_1gw, overrides)
