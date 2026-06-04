# STALE: analysis-updated-iter-2
"""1costingfe model: Polywell (EMC2) (EMC2).

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
#    CRITICAL: This concept has NO complete design point. The analysis states:
#    "No design-point row for this concept yet — selection is upstream-pending."
#    Park et al. (2025) provides theoretical physics scaling but no engineering
#    design with complete parameters. The spec dict below is EMPTY per the
#    archetype-fit guidance: "When no design point exists, populate spec with
#    only the fields that ARE published." Since Park 2025 gives physics values
#    but no canonical CostingInput mapping (no R0, no plasma_t, no geometry in
#    canonical form), we leave spec empty and rely entirely on library defaults.
#
#    From analysis Section 5: Park et al. provides:
#    - Device geometry: 1.6 m cube (but this is overall device, not R0 or plasma_t)
#    - Plasma volume: 4.1 m³ (BLOCKED from spec by DIPOLE archetype bug #24)
#    - Cusp magnetic field: 4.5 T (but this is boundary field, not b_center)
#    - Electron beam input: 78 MW (this is p_input, but uncertainty ±60% per γ factor)
#    - Fusion power: ~980 MW (p_fus is never a spec key — library back-solves)
#
#    None of these map cleanly to canonical DIPOLE/POLYWELL spec keys without
#    architectural assumptions the source doesn't support. Leaving spec empty
#    produces a generic POLYWELL cost estimate at P_native scale, which is the
#    honest answer given data availability.
spec = dict(
    # No canonical spec keys — Park et al. (2025) provides physics scaling
    # (cube geometry, plasma volume, field strength) but no mapping to
    # CostingInput's expected geometry parameters (R0, plasma_t, r_bore).
    # The 1.6 m cube is overall device dimension, not a canonical length scale.
    # plasma_volume is blocked by DIPOLE archetype bug (1cFE/1costingfe#24).
    # Electron beam 78 MW is p_input but has ±60% uncertainty from γ factor.
    # Leaving spec empty uses library YAML defaults for a generic POLYWELL.
)
P_native = 290.0  # MWe — derived in analysis Section 5 from Park et al. physics
                  # scaling: ~388 MWe gross thermal conversion - 97.5 MW e-beam
                  # wall-plug. CAUTION: uncertainty ±60% due to γ=0.1 assumption.

# 2. Model.
model = CostModel(concept=ConfinementConcept.POLYWELL, fuel=Fuel.PB11)

# 2b. Generic forward — overrides OFF, design-point scale (forward 1 of 3). The
#     library's bare answer for a reactor this size, and the reference a relative
#     override is written against. ALWAYS emit this line (it is mandatory, even
#     when no override references it).
generic = generic_reference(model, spec, P_native)

# 3. Override registry — six fields per entry, transcribed from Section 5b.
#    Analysis Section 5b states: "After walking the canonical account schema,
#    **no override candidates are proposed**." Justification: "The dossier
#    contains no company-grounded cost data, published dollar figures, or
#    engineering subsystem specifications." The concept has physics validation
#    but no power plant cost study. Zero overrides is below the Archetype-Fit:Med
#    expected band (3-8) but reflects true data availability.
overrides = [
    # No overrides — Park et al. (2025) provides physics scaling only, no cost
    # data. Analysis Section 5b: "No blanket design, no magnet engineering
    # (HTS inferred but not designed), no electron gun procurement cost, no
    # balance-of-plant specifications." Library defaults produce a generic
    # electrostatic confinement fusion plant estimate, not Polywell-specific.
]

# 4. Overrides-on forwards via the shared helper (native + 1 GWe NOAK projection).
native, result_1gw = run_native_and_1gw(
    model, spec=spec, overrides=overrides, p_native=P_native,
)

print_cas_breakdown(generic, native, result_1gw, overrides)
