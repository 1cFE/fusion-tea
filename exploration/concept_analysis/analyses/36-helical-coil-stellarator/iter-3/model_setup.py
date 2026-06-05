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
    R0=7.8,           # Major radius (m) — aip-2023-paper-abstract.md Table I line 129, R_c row, HESTIA column; also §II line 88 "helical coil major radius, R_0, is 7.8 m"
    plasma_t=1.87,    # Minor radius (m) — aip-2023-paper-abstract.md Table I line 130, a_0 row, HESTIA column (helical coil minor radius ac)
    elon=1.0,         # Elongation — assumed circular for heliotron (no value stated in paper)
    B=9.0,            # On-axis magnetic field (T) — aip-2023-paper-abstract.md §II lines 81, 214 "approximately 9 T at the plasma center"
    p_input=20.0,     # Auxiliary heating delivered to plasma (MW) — aip-2023-paper-abstract.md Table I line 155, P_VCM = 20 MW; §II.D line 264 "operated alternately to inject 20MW of ECH power continuously". Note: 40 MW wall-plug is required (line 269), but library expects delivered power here, not wall-plug.
)
P_native = 70.4       # MWe — aip-2023-paper-abstract.md Table I line 163

# Design point notes (for documentation only, not spec kwargs):
# - Geometry: R0 = 7.8 m, a = 1.87 m per Table I lines 129-130.
# - P_fus = 250 MW (fusion power, back-solved by library) — Table I line 156
# - Q_eng = 2.0 (engineering gain) — Table I (implicit from P_net/P_fus ratio)
# - Q_plasma ~ 13 (fusion gain: P_fus / P_ECH_delivered ≈ 250/20 = 12.5)
# - P_gross = 139 MWe, P_net = 70.4 MWe — Table I line 163
# - ECH system: 60× 250 GHz, 1 MW CW gyrotrons operated alternately → 20 MW continuous delivery, 40 MW wall-plug (50% efficiency) — §II.D lines 264, 269. p_input uses the 20 MW delivered value per Table I.
# - Availability target >80% (steady-state stellarator, no disruptions)
# - Confinement enhancement H = 1.3 × γ_CEPI = 1.18 (unvalidated, requires HESTIA-Primary prototype)
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
