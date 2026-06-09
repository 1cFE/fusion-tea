"""1costingfe model: Laser ICF Fast Ignition (Focused Energy) (Focused Energy).

Usage:
    uv run python model_setup.py              # print results
    uv run python model_setup.py | tee model_output.txt

BLOCKING ISSUES - THIS SCRIPT CANNOT RUN:
    1. No P_native: Focused Energy has not disclosed net electric output.
    2. No spec parameters: No published geometry, power, or physics parameters
       at design point. Analysis Section 5 states all power-related values are
       "Not disclosed".
    3. Design point selection is upstream-pending per analysis.md line 21-22.

This script is written to satisfy the three-forward contract structure but will
fail at forward() time due to missing inputs. It serves as a template for when
design-point data becomes available.
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
#    BLOCKING: No published design point. All geometry / power / physics
#    parameters are undisclosed per analysis.md Section 5:
#    - Net electric output: "Not disclosed"
#    - Thermal power: "Not disclosed"
#    - Fusion power: "Not disclosed"
#    - Compression laser energy/shot: "Not disclosed"
#    - Repetition rate: ~10 Hz (goal, qualitative only; no design-point value)
#    - Target gain: 50-100 (goal, not demonstrated)
#
#    The only quantitative values in the dossier are technology goals, not
#    design-point specifications. Laser IFE requires at minimum:
#    - rep_rate_hz (Hz)
#    - target_gain (dimensionless)
#    - laser_pulse_energy_kJ (kJ/shot)
#    - eta_laser (wall-plug efficiency)
#    but none are specified at a committed design point.
#
#    Leaving spec empty will cause the library to fall back to pure archetype
#    YAML defaults (generic laser IFE, not Focused Energy's actual machine).
spec = dict(
    # No geometry parameters (IFE has no R0, plasma_t, etc.)
    # No power parameters (p_input unknown, p_fus unknown)
    # No rep rate at design point (10 Hz is a goal, not a specification)
    # No target gain (50-100 is a target range, not a demonstrated value)
    # No laser energy/shot (compression energy undisclosed; 150 kJ ignitor
    #                       from LaserFocusWorld is low-confidence)
)

# Native net-electric power (MWe) — BLOCKING: not disclosed.
# Analysis Section 5 line 271: "No `P_native` can be assigned; no net electric
# output is published." The "gigawatt-scale" ambition (Callahan interview) is
# qualitative. Cannot run forwards without this value.
#
# Placeholder value to satisfy Python syntax; forward() will fail or produce
# nonsense results.
P_native = None  # TODO: replace with actual MWe when disclosed

# 2. Model.
model = CostModel(concept=ConfinementConcept.LASER_IFE, fuel=Fuel.DT)

# 2b. Generic forward — overrides OFF, design-point scale (forward 1 of 3).
#     This line is mandatory even when no override references it. It establishes
#     the library's overrides-off answer at P_native, which is the reference
#     frame for relative overrides and the rescaling anchor for the fleet
#     projection.
#
#     WILL FAIL if P_native is None or if spec is insufficient for the library
#     to solve the power balance.
if P_native is None:
    raise ValueError(
        "P_native is None — cannot run generic_reference without net electric "
        "output. Focused Energy has not disclosed this value. See analysis.md "
        "Section 5, line 271."
    )
generic = generic_reference(model, spec, P_native)

# 3. Override registry — six fields per entry, transcribed from Section 5b.
#    Analysis Section 5b (line 319-328) concludes: "No justified overrides
#    discovered." The dossier provides high-level architectural features (two-
#    pulse laser, lithium blankets, 10 Hz, cone-in-shell targets) but lacks
#    quantitative cost figures, component masses, or unit prices required to
#    justify departures from library defaults.
#
#    Key blocked overrides (would be proposed if data existed):
#    1. C220104 (laser driver): Company has not disclosed beamline count, unit
#       cost, or total driver capex. This is likely the dominant cost account.
#    2. CAS27 (blanket inventory): Lithium blankets confirmed but chemistry
#       (FLiBe vs LiPb vs liquid Li) and inventory undisclosed.
#    3. C220108 (target factory): $0.80/shot per-target cost is known (analyst
#       patch), but factory capex is not. The library default factory cost may
#       underestimate cone-in-shell complexity.
overrides = []

# 4. Overrides-on forwards via the shared helper (native + 1 GWe NOAK projection).
#    WILL FAIL if P_native is None or spec is insufficient.
native, result_1gw = run_native_and_1gw(
    model, spec=spec, overrides=overrides, p_native=P_native,
)

print_cas_breakdown(generic, native, result_1gw, overrides)
