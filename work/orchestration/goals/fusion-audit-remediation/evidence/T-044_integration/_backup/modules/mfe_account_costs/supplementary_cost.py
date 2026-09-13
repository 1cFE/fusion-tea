"""Supplementary_CostModule Module Wrapper

TEAx module for Supplementary_Cost calculation.

CAS50 supplementary account:

  cost = (shipping*cas20 + spares*cas23_to_28 + tax*cas20
          + insurance*(cas20+cas30)
          + startup*(n_mod*p_net/ref) + decom*(n_mod*p_net/ref))
(1 + contingency_rate)

cas20 is CAS20 WITH contingency; cas23_to_28 is c23+c24+c25+c26+c27+c28
(1cfe's param is misnamed cas22_to_28 but model.py:1492 feeds c23..c28 --
WI-028 finding F-1). c59 internal contingency applies to the CAS50
subtotal (NOAK 0).

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py (pin 0254385)
*Ref**: costs.py:259-283 (cas50_supplementary); model.py:1492 (spares base = c23..c28)
*Basis**: Fraction-of-aggregate supplementary cost with internal contingency

Inputs:
    - spares_frac: spares_frac parameter
    - cas23_to_28: cas23_to_28 parameter
    - ref_net_power: ref_net_power parameter
    - cas30: cas30 parameter
    - shipping_frac: shipping_frac parameter
    - p_net: p_net parameter
    - tax_frac: tax_frac parameter
    - decom_base: decom_base parameter
    - cas20: cas20 parameter
    - n_mod_in: n_mod_in parameter
    - insurance_frac: insurance_frac parameter
    - startup_fuel_base: startup_fuel_base parameter
    - contingency_rate_in: contingency_rate_in parameter

Outputs:
    - cost: cost result

SysML Source: root-0/analyses/mfe_account_costs.sysml:593

SysML Source: root-0/analyses/mfe_account_costs.sysml:593

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_account_costs/supplementary_cost_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float


class Supplementary_CostInput(BaseModel):
    """Input model for Supplementary_CostModule.

    Attributes:
        spares_frac: spares_frac input
        cas23_to_28: cas23_to_28 input
        ref_net_power: ref_net_power input
        cas30: cas30 input
        shipping_frac: shipping_frac input
        p_net: p_net input
        tax_frac: tax_frac input
        decom_base: decom_base input
        cas20: cas20 input
        n_mod_in: n_mod_in input
        insurance_frac: insurance_frac input
        startup_fuel_base: startup_fuel_base input
        contingency_rate_in: contingency_rate_in input
    """
    spares_frac: float = Field(..., description="spares_frac input")
    cas23_to_28: float = Field(..., description="cas23_to_28 input")
    ref_net_power: float = Field(..., description="ref_net_power input")
    cas30: float = Field(..., description="cas30 input")
    shipping_frac: float = Field(..., description="shipping_frac input")
    p_net: float = Field(..., description="p_net input")
    tax_frac: float = Field(..., description="tax_frac input")
    decom_base: float = Field(..., description="decom_base input")
    cas20: float = Field(..., description="cas20 input")
    n_mod_in: float = Field(..., description="n_mod_in input")
    insurance_frac: float = Field(..., description="insurance_frac input")
    startup_fuel_base: float = Field(..., description="startup_fuel_base input")
    contingency_rate_in: float = Field(..., description="contingency_rate_in input")


class Supplementary_CostModule(ModuleBase[Supplementary_CostInput, Float]):
    """TEAx module for Supplementary_Cost calculation.

CAS50 supplementary account:

  cost = (shipping*cas20 + spares*cas23_to_28 + tax*cas20
          + insurance*(cas20+cas30)
          + startup*(n_mod*p_net/ref) + decom*(n_mod*p_net/ref))
(1 + contingency_rate)

cas20 is CAS20 WITH contingency; cas23_to_28 is c23+c24+c25+c26+c27+c28
(1cfe's param is misnamed cas22_to_28 but model.py:1492 feeds c23..c28 --
WI-028 finding F-1). c59 internal contingency applies to the CAS50
subtotal (NOAK 0).

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py (pin 0254385)
*Ref**: costs.py:259-283 (cas50_supplementary); model.py:1492 (spares base = c23..c28)
*Basis**: Fraction-of-aggregate supplementary cost with internal contingency

Inputs:
    - spares_frac: spares_frac parameter
    - cas23_to_28: cas23_to_28 parameter
    - ref_net_power: ref_net_power parameter
    - cas30: cas30 parameter
    - shipping_frac: shipping_frac parameter
    - p_net: p_net parameter
    - tax_frac: tax_frac parameter
    - decom_base: decom_base parameter
    - cas20: cas20 parameter
    - n_mod_in: n_mod_in parameter
    - insurance_frac: insurance_frac parameter
    - startup_fuel_base: startup_fuel_base parameter
    - contingency_rate_in: contingency_rate_in parameter

Outputs:
    - cost: cost result

SysML Source: root-0/analyses/mfe_account_costs.sysml:593

    SysML Source: root-0/analyses/mfe_account_costs.sysml:593

    Calculation Specification:
        n_mod_in = 1.0
        shipping_frac = 0.015
        tax_frac = 0.01
        insurance_frac = 0.015
        contingency_rate_in = 0.0
        ref_net_power = 1000.0
        cost = (shipping_frac * cas20 + spares_frac * cas23_to_28 + tax_frac * cas20 + insurance_frac * (cas20 + cas30) + startup_fuel_base * (n_mod_in * p_net / ref_net_power) + decom_base * (n_mod_in * p_net / ref_net_power)) * (1.0 + contingency_rate_in)
        
Documentation:
CAS50 supplementary account:

  cost = (shipping*cas20 + spares*cas23_to_28 + tax*cas20
          + insurance*(cas20+cas30)
          + startup*(n_mod*p_net/ref) + decom*(n_mod*p_net/ref))
(1 + contingency_rate)

cas20 is CAS20 WITH contingency; cas23_to_28 is c23+c24+c25+c26+c27+c28
(1cfe's param is misnamed cas22_to_28 but model.py:1492 feeds c23..c28 --
WI-028 finding F-1). c59 internal contingency applies to the CAS50
subtotal (NOAK 0).

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py (pin 0254385)
*Ref**: costs.py:259-283 (cas50_supplementary); model.py:1492 (spares base = c23..c28)
*Basis**: Fraction-of-aggregate supplementary cost with internal contingency

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_account_costs.supplementary_cost_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "Supplementary_CostModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, spares_frac: float, cas23_to_28: float, ref_net_power: float, cas30: float, shipping_frac: float, p_net: float, tax_frac: float, decom_base: float, cas20: float, n_mod_in: float, insurance_frac: float, startup_fuel_base: float, contingency_rate_in: float    ) -> Supplementary_CostInput:
        """Validate inputs and fill defaults.

        Args:
            spares_frac: spares_frac input
            cas23_to_28: cas23_to_28 input
            ref_net_power: ref_net_power input
            cas30: cas30 input
            shipping_frac: shipping_frac input
            p_net: p_net input
            tax_frac: tax_frac input
            decom_base: decom_base input
            cas20: cas20 input
            n_mod_in: n_mod_in input
            insurance_frac: insurance_frac input
            startup_fuel_base: startup_fuel_base input
            contingency_rate_in: contingency_rate_in input

        Returns:
            Validated input model
        """
        return Supplementary_CostInput(spares_frac=spares_frac, cas23_to_28=cas23_to_28, ref_net_power=ref_net_power, cas30=cas30, shipping_frac=shipping_frac, p_net=p_net, tax_frac=tax_frac, decom_base=decom_base, cas20=cas20, n_mod_in=n_mod_in, insurance_frac=insurance_frac, startup_fuel_base=startup_fuel_base, contingency_rate_in=contingency_rate_in)

    def run(
        self, spares_frac: float, cas23_to_28: float, ref_net_power: float, cas30: float, shipping_frac: float, p_net: float, tax_frac: float, decom_base: float, cas20: float, n_mod_in: float, insurance_frac: float, startup_fuel_base: float, contingency_rate_in: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            spares_frac: spares_frac input
            cas23_to_28: cas23_to_28 input
            ref_net_power: ref_net_power input
            cas30: cas30 input
            shipping_frac: shipping_frac input
            p_net: p_net input
            tax_frac: tax_frac input
            decom_base: decom_base input
            cas20: cas20 input
            n_mod_in: n_mod_in input
            insurance_frac: insurance_frac input
            startup_fuel_base: startup_fuel_base input
            contingency_rate_in: contingency_rate_in input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(spares_frac, cas23_to_28, ref_net_power, cas30, shipping_frac, p_net, tax_frac, decom_base, cas20, n_mod_in, insurance_frac, startup_fuel_base, contingency_rate_in)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_account_costs.supplementary_cost_impl import (
            run_supplementary_cost,
        )

        # Execute implementation - returns single value
        cost = run_supplementary_cost(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(cost))
