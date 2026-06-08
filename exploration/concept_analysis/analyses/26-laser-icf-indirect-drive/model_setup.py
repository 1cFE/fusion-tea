"""1costingfe model: Laser ICF Indirect Drive (Inertia Thunderwall) (Inertia Enterprises).

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
#    Inertia has published minimal quantitative design data beyond high-level
#    architectural description (see analysis.md §1, §5). Spec is intentionally
#    minimal; library YAML defaults for LASER_IFE archetype will provide the
#    cost structure.
#
#    NOT SPECIFIED by Inertia (relying on library defaults):
#    - Chamber geometry (radius, wall thickness, blanket config): analysis §5
#      "Chamber geometry not disclosed"
#    - Target gain: analysis §5 "unknown... back-solved from net electric power"
#    - Thermal-to-electric efficiency: analysis §5 "assumed 0.33, not stated"
#    - Capacity factor: analysis §5 "not specified"
#    - Fusion yield per shot: analysis §5 "estimated ~450 MJ, not stated"
#
#    The 10 Hz repetition rate, 10 MJ laser energy, and 10% wallplug efficiency
#    are Thunderwall specifications, but these are informational for understanding
#    driver architecture — they don't map to CostingInput spec fields. Laser
#    wallplug efficiency is eta_pin (YAML default 0.10 matches Inertia's claim).
spec = dict(
    # No design-point-specific geometry or physics overrides — Inertia has not
    # disclosed quantitative specs beyond rep rate / laser energy / efficiency
    # (which are YAML-defaulted or not spec-overridable per Hard Rule 3).
    #
    # Per-shot target consumable cost override.
    # Thunderwall inherits NIF's Hybrid-E indirect-drive geometry: cryogenic
    # D-T capsule inside a metal hohlraum. The hohlraum hardware roughly
    # doubles per-shot consumable cost vs a bare direct-drive capsule
    # ($0.27 → $0.70 NOAK, per Rickman/Goodin GA 2003 hohlraum costing).
    # The LASER_IFE library default ($0.40) is a mid-value between
    # direct-drive ($0.27) and indirect-drive ($0.70); for Inertia's
    # explicitly indirect-drive design the high end applies.
    # Source: pulsed_laser_ife.yaml + CAS80_target_consumables.md
    #   (Rickman/Goodin GA 2003 §Indirect Drive Target Costing; NAS 2013
    #   §Target Fabrication, $0.20–$0.40 direct vs $0.70 indirect bands).
    # Inertia's "<$1 per target" aspirational claim (analysis §5b) is
    # consistent with this NOAK literature value.
    target_unit_cost=0.70,  # $/shot — NIF-style indirect drive, NOAK basis
)
P_native = 1500  # MWe — analysis.md Design Point block

# 2. Model.
model = CostModel(concept=ConfinementConcept.LASER_IFE, fuel=Fuel.DT)

# 2b. Generic forward — overrides OFF, design-point scale (forward 1 of 3). The
#     library's bare answer for a reactor this size, and the reference a relative
#     override is written against. ALWAYS emit this line (it is mandatory, even
#     when no override references it).
generic = generic_reference(model, spec, P_native)

# 3. Override registry — six fields per entry, transcribed from Section 5b.
#    Analysis §5b: "zero enabled overrides... reflects the paucity of Inertia-
#    published cost data." The <$1 per target cost goal is a unit operating cost
#    (consumable), not a capital cost account override.
overrides = []

# 4. Overrides-on forwards via the shared helper (native + 1 GWe NOAK projection).
native, result_1gw = run_native_and_1gw(
    model, spec=spec, overrides=overrides, p_native=P_native,
)

print_cas_breakdown(generic, native, result_1gw, overrides)
