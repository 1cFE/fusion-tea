"""Auto-generated implementation for PermittingCostCalc.

AUTO_IMPLEMENTED = True

SysML Source: models/tests/solar_battery/library.sysml:210

SysML Expressions:
    cost_per_kw = 187.5
    material_cost = 0.0
    fab_cost = 0.0
    install_cost = 0.0
    total_cost = system_capacity_kw * cost_per_kw
    idiot_index = 0.0
    
Documentation:
Cost calculation for permitting and interconnection.
Soft cost — no material/fabrication/installation split.
Total cost is purely based on system capacity.

*Source**: Solar industry cost modeling
*Last Updated**: 2026-02-01
"""

AUTO_IMPLEMENTED = True

from solar_battery_v2.modules.solarbatterylibrary.permittingcostcalc import PermittingCostCalcInput


def run_permittingcostcalc(inputs: PermittingCostCalcInput) -> tuple[float, float, float, float, float]:
    """Execute PermittingCostCalc calculation.

Cost calculation for permitting and interconnection.
Soft cost — no material/fabrication/installation split.
Total cost is purely based on system capacity.

*Source**: Solar industry cost modeling
*Last Updated**: 2026-02-01

SysML Source: models/tests/solar_battery/library.sysml:210

SysML Expressions:
    cost_per_kw = 187.5
    material_cost = 0.0
    fab_cost = 0.0
    install_cost = 0.0
    total_cost = system_capacity_kw * cost_per_kw
    idiot_index = 0.0
    
Documentation:
Cost calculation for permitting and interconnection.
Soft cost — no material/fabrication/installation split.
Total cost is purely based on system capacity.

*Source**: Solar industry cost modeling
*Last Updated**: 2026-02-01

Args:
    inputs: Input parameters validated against PermittingCostCalcInput schema

Returns:
    tuple[float, ...]: (material_cost, fab_cost, install_cost, total_cost, idiot_index)

Example:
    >>> inputs = PermittingCostCalcInput(...)
    >>> material_cost, fab_cost, install_cost, total_cost, idiot_index = run_permittingcostcalc(inputs)
    """
    return (
        0.0,  # material_cost
        0.0,  # fab_cost
        0.0,  # install_cost
        (inputs.system_capacity_kw * inputs.cost_per_kw),  # total_cost
        0.0,  # idiot_index
    )
