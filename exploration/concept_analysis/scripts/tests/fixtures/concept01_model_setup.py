"""Three-forward model_setup.py fixture — concept 01-hts-compact-tokamak (ARC).

A faithful three-forward conversion of the Phase 0 prototype, used by the
integration test (test_validators.py) to prove the shape the model-setup prompt
instructs passes BOTH AST gates: validate_model_setup_contract(strict) and
validate_override_registry. It binds the four contract names — model, generic,
native, result_1gw — and carries the four ARC overrides plus one relative
override (referencing `generic`) so the generic-frame path is exercised.

Runnable: `uv run python tests/fixtures/concept01_model_setup.py` (Item 4 landed
the float-`n_mod` library change, so no runtime patch is needed).
"""
import sys
from pathlib import Path

# Make the shared three-forward helper importable regardless of cwd.
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
spec = dict(
    R0=3.3,
    plasma_t=1.13,
    elon=1.84,
    p_input=38.6,
)
P_native = 233.0   # MWe — ARC 2015 conservative Pilot phase (Sorbom Table 1)

# 2. Model.
model = CostModel(concept=ConfinementConcept.TOKAMAK, fuel=Fuel.DT)

# 2b. Generic forward — overrides OFF, design-point scale (forward 1 of 3). The
#     reference a relative override is written against.
generic = generic_reference(model, spec, P_native)

# 3. Override registry — six-field entries.
overrides = [
    {"account": "C220103", "value": 6901.0, "enabled": True,
     "provenance": "derived", "source": "arc-reactor-specifications.md §6 (Sorbom 2015)",
     "rationale": "Magnet+structure fabricated cost, 2014 USD inflated x1.34."},
    {"account": "C220106", "value": 123.0, "enabled": True,
     "provenance": "derived", "source": "arc-reactor-specifications.md §6 (Sorbom 2015)",
     "rationale": "Double-walled Inconel-718 vacuum vessel, $92M 2014 x1.34."},
    {"account": "CAS27", "value": 146.0, "enabled": True,
     "provenance": "derived", "source": "arc-reactor-specifications.md §6; Araiinejad 2025",
     "rationale": "950 t FLiBe x $154/kg NOAK = $146M."},
    # Relative override — references the mandatory `generic` line (overrides-off
    # library value), exercising the generic-frame rule.
    {"account": "C220101", "value": 0.70 * generic.costs.cas21, "enabled": True,
     "provenance": "derived", "source": "arc-reactor-specifications.md §6 (Sorbom 2015)",
     "rationale": "30% structure-cost reduction from modular fab; 0.70 x library CAS21."},
]

# 4. Overrides-on forwards via the shared helper (native + 1 GWe NOAK projection).
native, result_1gw = run_native_and_1gw(
    model, spec=spec, overrides=overrides, p_native=P_native,
)

print_cas_breakdown(generic, native, result_1gw, overrides)
