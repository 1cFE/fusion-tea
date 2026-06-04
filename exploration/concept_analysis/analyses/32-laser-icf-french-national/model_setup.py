"""1costingfe model: Laser ICF French National (GenF) (GenF Systems).

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
#    GenF TARANIS commercial reactor, 2050 target (Ribeyre et al. 2025).
#    Source: analyses/32-laser-icf-french-national/analysis.md §5 Design Point Parameters
#
#    NOTE: LASER_IFE is a PULSED concept. The canonical spec keys per validation.py
#    are f_rep (Hz), eta_pin (driver efficiency), q_eng (engineering gain), and
#    p_target (target/driver power in MW). Laser energy, chamber radius, and
#    blanket multiplier are NOT exposed as settable parameters — they are either
#    internal calculations or part of the archetype YAML defaults.
spec = dict(
    # Pulsed concept parameters (required for LASER_IFE)
    f_rep=10.0,               # genf-website-technology.md: "10 times per second"
    eta_pin=0.10,             # aip-advances-ribeyre-2025.md §III: 10% DPSSL efficiency
    q_eng=8.0,                # analysis.md §5: Geng ≈ 8–10 (inferred from Fig. 3)
    # p_target is NOT set — library will back-solve from P_native and q_eng

    # NOTE: laser_energy_MJ (3 MJ), chamber_radius_m (8m), and blanket_multiplier (1.2)
    # are not valid spec keys for LASER_IFE. They are part of the archetype YAML
    # defaults or internal calculations. The library does not expose them for override.
    # GenF's design point values (3 MJ laser, 8m chamber, Gb=1.2) would need to be
    # expressed via cost_overrides on CAS accounts if they differ from library defaults.
)

P_native = 1000.0  # MWe — genf-website-technology.md: "1GW of power"

# 2. Model.
model = CostModel(concept=ConfinementConcept.LASER_IFE, fuel=Fuel.DT)

# 2b. Generic forward — overrides OFF, design-point scale (forward 1 of 3). The
#     library's bare answer for a reactor this size, and the reference a relative
#     override is written against. ALWAYS emit this line (it is mandatory, even
#     when no override references it).
generic = generic_reference(model, spec, P_native)

# 3. Override registry — six fields per entry, transcribed from Section 5b.
#    Section 5b states: "no override candidates are proposed" due to absence of
#    company-grounded cost data. GenF has published no laser driver $/J, no target
#    factory cost, no chamber/blanket costs. All accounts use library defaults.
overrides = []

# 4. Overrides-on forwards via the shared helper (native + 1 GWe NOAK projection).
native, result_1gw = run_native_and_1gw(
    model, spec=spec, overrides=overrides, p_native=P_native,
)

print_cas_breakdown(generic, native, result_1gw, overrides)
