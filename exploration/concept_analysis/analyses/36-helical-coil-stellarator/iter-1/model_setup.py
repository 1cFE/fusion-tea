"""1costingfe model: Helical-Coil Stellarator (HESTIA) (Helical Fusion).

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
#    From analysis.md Section 5, Design Point Parameters table.
spec = dict(
    R0=7.8,           # Major radius (m) — aip-2023-paper-abstract.md Table I, R_c row, HESTIA column
    plasma_t=1.87,    # Minor radius (m) — aip-2023-paper-abstract.md Table I, a_0 row, HESTIA column
    elon=1.0,         # Elongation — assumed circular for heliotron (no value stated in paper)
    B=9.0,            # On-axis magnetic field (T) — aip-2023-paper-abstract.md Table I (9 T at plasma center stated in text)
    p_input=20.0,     # Auxiliary heating wall-plug (MW) — aip-2023-paper-abstract.md Table I, P_ECH row, HESTIA column
)
P_native = 70.4       # MWe — aip-2023-paper-abstract.md Table I line 163

# Design point notes (for documentation only, not spec kwargs):
# - P_fus = 250 MW (fusion power, back-solved by library) — Table I
# - Q_eng = 2.0 (engineering gain) — Table I
# - Q_plasma ~ 13 (fusion gain inferred from P_fus / P_ECH ≈ 250/20 = 12.5)
# - P_gross = 139 MWe, P_net = 70.4 MWe — Table I
# - Availability target >80% (steady-state stellarator, no disruptions)
# - Confinement enhancement H = 1.3 × γ_CEPI = 1.18 (unvalidated, requires HESTIA-Primary prototype)
# - 60× 250 GHz, 1 MW CW gyrotrons (do not exist yet; library ECRH default applies)
# - Liquid metal blanket (tin-indium-lead-lithium) eliminates separate divertor
# - sCO2 Brayton cycle targeting >50% thermal efficiency (aspirational; Oroshhi-2 demo at 20%)

# 2. Model.
model = CostModel(concept=ConfinementConcept.STELLARATOR, fuel=Fuel.DT)

# 2b. Generic forward — overrides OFF, design-point scale (forward 1 of 3). The
#     library's bare answer for a reactor this size, and the reference a relative
#     override is written against. ALWAYS emit this line (it is mandatory, even
#     when no override references it).
generic = generic_reference(model, spec, P_native)

# 3. Override registry — six fields per entry, transcribed from Section 5b.
#    Analysis §5b identifies one enabled override: C220108 (divertor) = 0.
overrides = [
    {"account": "C220108", "value": 0.0, "enabled": True,
     "provenance": "direct", "source": "aip-2023-paper-abstract.md §II.C, lines 81-84, 234-236",
     "rationale": "Individual divertor systems are not required in HESTIA. The liquid metal "
                  "free-surface first wall serves the divertor function by flowing over the "
                  "plasma-facing surfaces and absorbing heat/particle fluxes. No separate tungsten "
                  "monoblock divertor cassettes are installed. C220108 (divertor) cost = 0. The "
                  "divertor functionality is embedded in C220101 (blanket).",
     "cost_basis": "noak"},
]

# 4. Overrides-on forwards via the shared helper (native + 1 GWe NOAK projection).
native, result_1gw = run_native_and_1gw(
    model, spec=spec, overrides=overrides, p_native=P_native,
)

print_cas_breakdown(generic, native, result_1gw, overrides)
