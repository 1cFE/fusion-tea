from pydantic import Field
from simkit.config.schema import MultiOutput

class AnnualizedFinancialCalcOutput(MultiOutput):
    """Multi-output container for AnnualizedFinancialCalc.

Annualized financial cost using Capital Recovery Factor.
CRF = r * (1+r)^n / ((1+r)^n - 1)
Computes CRF from discount_rate and plant_lifetime rather than using
PyFECONS's hardcoded 0.09 default.

*Source**: PyFECONS /home/reid/PyFECONS/pyfecons/costing/calculations/cas90_annualized_financial.py:14
*Last Updated**: 2026-02-01

SysML Source: solar_battery_model/library.sysml:314
    """
    capital_recovery_factor: float = Field(description="capital_recovery_factor output")
    annualized_capital_cost: float = Field(description="annualized_capital_cost output")
