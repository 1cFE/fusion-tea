"""AnnualizedOMCalcModule Module Wrapper

TEAx module for AnnualizedOMCalc calculation.

Annualized operations and maintenance cost.
Matches PyFECONS cas70_annualized_om.py: om_rate * p_net_kw.

*Source**: PyFECONS /home/reid/PyFECONS/pyfecons/costing/calculations/cas70_annualized_om.py:10
*Last Updated**: 2026-02-01

Inputs:
    - om_rate_per_kw_year: om_rate_per_kw_year parameter
    - p_net_kw: p_net_kw parameter

Outputs:
    - annual_om_cost: annual_om_cost result

SysML Source: models/tests/solar_battery/library.sysml:283

SysML Source: models/tests/solar_battery/library.sysml:283

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/solarbatterylibrary/annualizedomcalc_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from solar_battery_v2.primitives import Float


class AnnualizedOMCalcInput(BaseModel):
    """Input model for AnnualizedOMCalcModule.

    Attributes:
        om_rate_per_kw_year: om_rate_per_kw_year input
        p_net_kw: p_net_kw input
    """
    om_rate_per_kw_year: float = Field(..., description="om_rate_per_kw_year input")
    p_net_kw: float = Field(..., description="p_net_kw input")


class AnnualizedOMCalcModule(ModuleBase[AnnualizedOMCalcInput, Float]):
    """TEAx module for AnnualizedOMCalc calculation.

Annualized operations and maintenance cost.
Matches PyFECONS cas70_annualized_om.py: om_rate * p_net_kw.

*Source**: PyFECONS /home/reid/PyFECONS/pyfecons/costing/calculations/cas70_annualized_om.py:10
*Last Updated**: 2026-02-01

Inputs:
    - om_rate_per_kw_year: om_rate_per_kw_year parameter
    - p_net_kw: p_net_kw parameter

Outputs:
    - annual_om_cost: annual_om_cost result

SysML Source: models/tests/solar_battery/library.sysml:283

    SysML Source: models/tests/solar_battery/library.sysml:283

    Calculation Specification:
        annual_om_cost = om_rate_per_kw_year * p_net_kw
        
Documentation:
Annualized operations and maintenance cost.
Matches PyFECONS cas70_annualized_om.py: om_rate * p_net_kw.

*Source**: PyFECONS /home/reid/PyFECONS/pyfecons/costing/calculations/cas70_annualized_om.py:10
*Last Updated**: 2026-02-01

    IMPLEMENTATION: See solar_battery_v2.handwritten.solarbatterylibrary.annualizedomcalc_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "AnnualizedOMCalcModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, om_rate_per_kw_year: float, p_net_kw: float    ) -> AnnualizedOMCalcInput:
        """Validate inputs and fill defaults.

        Args:
            om_rate_per_kw_year: om_rate_per_kw_year input
            p_net_kw: p_net_kw input

        Returns:
            Validated input model
        """
        return AnnualizedOMCalcInput(om_rate_per_kw_year=om_rate_per_kw_year, p_net_kw=p_net_kw)

    def run(
        self, om_rate_per_kw_year: float, p_net_kw: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            om_rate_per_kw_year: om_rate_per_kw_year input
            p_net_kw: p_net_kw input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(om_rate_per_kw_year, p_net_kw)

        # Import handwritten implementation
        from solar_battery_v2.handwritten.solarbatterylibrary.annualizedomcalc_impl import (
            run_annualizedomcalc,
        )

        # Execute implementation - returns single value
        annual_om_cost = run_annualizedomcalc(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(annual_om_cost))
