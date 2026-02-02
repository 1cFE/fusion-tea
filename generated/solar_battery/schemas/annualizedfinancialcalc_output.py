from pydantic import Field, RootModel
from simkit.config.schema import MultiOutput

from solar_battery.primitives import Float


class AnnualizedFinancialCalcOutput(MultiOutput):
    """Multi-output container for AnnualizedFinancialCalc.

Annualized financial cost using Capital Recovery Factor.
CRF = r * (1+r)^n / ((1+r)^n - 1)
Computes CRF from discount_rate and plant_lifetime rather than using
PyFECONS's hardcoded 0.09 default.

*Source**: PyFECONS /home/reid/PyFECONS/pyfecons/costing/calculations/cas90_annualized_financial.py:14
*Last Updated**: 2026-02-01

SysML Source: models/tests/solar_battery/library.sysml:314

    NOTE: Fields use RootModel[float] (not plain float) so that MultiOutput
    channels contain serializable Pydantic models. This enables the ExitPoint
    to write individual JSON files via write_json_model().
    """
    capital_recovery_factor: Float = Field(description="capital_recovery_factor output")
    annualized_capital_cost: Float = Field(description="annualized_capital_cost output")
