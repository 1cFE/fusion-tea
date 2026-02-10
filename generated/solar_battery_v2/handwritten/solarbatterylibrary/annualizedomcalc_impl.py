"""Auto-generated implementation for AnnualizedOMCalc.

AUTO_IMPLEMENTED = True

SysML Source: models/tests/solar_battery/library.sysml:283

SysML Expressions:
    annual_om_cost = om_rate_per_kw_year * p_net_kw
    
Documentation:
Annualized operations and maintenance cost.
Matches PyFECONS cas70_annualized_om.py: om_rate * p_net_kw.

*Source**: PyFECONS /home/reid/PyFECONS/pyfecons/costing/calculations/cas70_annualized_om.py:10
*Last Updated**: 2026-02-01
"""

AUTO_IMPLEMENTED = True

from solar_battery_v2.modules.solarbatterylibrary.annualizedomcalc import AnnualizedOMCalcInput


def run_annualizedomcalc(inputs: AnnualizedOMCalcInput) -> float:
    """Execute AnnualizedOMCalc calculation.

Annualized operations and maintenance cost.
Matches PyFECONS cas70_annualized_om.py: om_rate * p_net_kw.

*Source**: PyFECONS /home/reid/PyFECONS/pyfecons/costing/calculations/cas70_annualized_om.py:10
*Last Updated**: 2026-02-01

SysML Source: models/tests/solar_battery/library.sysml:283

SysML Expressions:
    annual_om_cost = om_rate_per_kw_year * p_net_kw
    
Documentation:
Annualized operations and maintenance cost.
Matches PyFECONS cas70_annualized_om.py: om_rate * p_net_kw.

*Source**: PyFECONS /home/reid/PyFECONS/pyfecons/costing/calculations/cas70_annualized_om.py:10
*Last Updated**: 2026-02-01

Args:
    inputs: Input parameters validated against AnnualizedOMCalcInput schema

Returns:
    float: annual_om_cost

Example:
    >>> inputs = AnnualizedOMCalcInput(...)
    >>> result = run_annualizedomcalc(inputs)
    """
    return (inputs.om_rate_per_kw_year * inputs.p_net_kw)
