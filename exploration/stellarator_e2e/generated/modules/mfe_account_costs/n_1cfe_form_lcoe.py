"""n_1cfe_Form_LCOEModule Module Wrapper

TEAx module for n_1cfe_Form_LCOE calculation.

LCOE in 1costingFE's form -- the comparison channel that pairs with
'1cfe-Form Capital Charge' (WI-029 Option ii):

  lcoe = (cas90 + cas70 + cas80) / (8760 * net_electric_mw * n_mod * availability)

Money-unit transparent: with the cost inputs in $ the result is $/MWh.
This is NOT the design-point headline -- 'LCOE DCF' remains the headline
and its convention is untouched. Both channels coexist by design.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/economics.py (pin 0254385)
*Ref**: economics.py:88-92 (compute_lcoe)
*Basis**: Annual cost over annual energy sold, 1costingFE denominator form

Inputs:
    - cas70: cas70 parameter
    - cas80: cas80 parameter
    - n_mod_in: n_mod_in parameter
    - availability_in: availability_in parameter
    - cas90: cas90 parameter
    - net_electric_mw: net_electric_mw parameter

Outputs:
    - lcoe: lcoe result

SysML Source: root-0/analyses/mfe_account_costs.sysml:951

SysML Source: root-0/analyses/mfe_account_costs.sysml:951

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_account_costs/n_1cfe_form_lcoe_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float


class n_1cfe_Form_LCOEInput(BaseModel):
    """Input model for n_1cfe_Form_LCOEModule.

    Attributes:
        cas70: cas70 input
        cas80: cas80 input
        n_mod_in: n_mod_in input
        availability_in: availability_in input
        cas90: cas90 input
        net_electric_mw: net_electric_mw input
    """
    cas70: float = Field(..., description="cas70 input")
    cas80: float = Field(..., description="cas80 input")
    n_mod_in: float = Field(..., description="n_mod_in input")
    availability_in: float = Field(..., description="availability_in input")
    cas90: float = Field(..., description="cas90 input")
    net_electric_mw: float = Field(..., description="net_electric_mw input")


class n_1cfe_Form_LCOEModule(ModuleBase[n_1cfe_Form_LCOEInput, Float]):
    """TEAx module for n_1cfe_Form_LCOE calculation.

LCOE in 1costingFE's form -- the comparison channel that pairs with
'1cfe-Form Capital Charge' (WI-029 Option ii):

  lcoe = (cas90 + cas70 + cas80) / (8760 * net_electric_mw * n_mod * availability)

Money-unit transparent: with the cost inputs in $ the result is $/MWh.
This is NOT the design-point headline -- 'LCOE DCF' remains the headline
and its convention is untouched. Both channels coexist by design.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/economics.py (pin 0254385)
*Ref**: economics.py:88-92 (compute_lcoe)
*Basis**: Annual cost over annual energy sold, 1costingFE denominator form

Inputs:
    - cas70: cas70 parameter
    - cas80: cas80 parameter
    - n_mod_in: n_mod_in parameter
    - availability_in: availability_in parameter
    - cas90: cas90 parameter
    - net_electric_mw: net_electric_mw parameter

Outputs:
    - lcoe: lcoe result

SysML Source: root-0/analyses/mfe_account_costs.sysml:951

    SysML Source: root-0/analyses/mfe_account_costs.sysml:951

    Calculation Specification:
        n_mod_in = 1.0
        annual_energy_mwh = 8760.0 * net_electric_mw * n_mod_in * availability_in
        lcoe = (cas90 + cas70 + cas80) / annual_energy_mwh
        
Documentation:
LCOE in 1costingFE's form -- the comparison channel that pairs with
'1cfe-Form Capital Charge' (WI-029 Option ii):

  lcoe = (cas90 + cas70 + cas80) / (8760 * net_electric_mw * n_mod * availability)

Money-unit transparent: with the cost inputs in $ the result is $/MWh.
This is NOT the design-point headline -- 'LCOE DCF' remains the headline
and its convention is untouched. Both channels coexist by design.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/economics.py (pin 0254385)
*Ref**: economics.py:88-92 (compute_lcoe)
*Basis**: Annual cost over annual energy sold, 1costingFE denominator form

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_account_costs.n_1cfe_form_lcoe_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "n_1cfe_Form_LCOEModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, cas70: float, cas80: float, n_mod_in: float, availability_in: float, cas90: float, net_electric_mw: float    ) -> n_1cfe_Form_LCOEInput:
        """Validate inputs and fill defaults.

        Args:
            cas70: cas70 input
            cas80: cas80 input
            n_mod_in: n_mod_in input
            availability_in: availability_in input
            cas90: cas90 input
            net_electric_mw: net_electric_mw input

        Returns:
            Validated input model
        """
        return n_1cfe_Form_LCOEInput(cas70=cas70, cas80=cas80, n_mod_in=n_mod_in, availability_in=availability_in, cas90=cas90, net_electric_mw=net_electric_mw)

    def run(
        self, cas70: float, cas80: float, n_mod_in: float, availability_in: float, cas90: float, net_electric_mw: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            cas70: cas70 input
            cas80: cas80 input
            n_mod_in: n_mod_in input
            availability_in: availability_in input
            cas90: cas90 input
            net_electric_mw: net_electric_mw input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(cas70, cas80, n_mod_in, availability_in, cas90, net_electric_mw)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_account_costs.n_1cfe_form_lcoe_impl import (
            run_n_1cfe_form_lcoe,
        )

        # Execute implementation - returns single value
        lcoe = run_n_1cfe_form_lcoe(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(lcoe))
