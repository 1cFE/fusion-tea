"""n_1cfe_Form_Capital_ChargeModule Module Wrapper

TEAx module for n_1cfe_Form_Capital_Charge calculation.

CAS90 in 1costingFE's financing form — the annual capital charge on
overnight capital PLUS the closed-form CAS60 interest during
construction:

  cas90 = crf * (overnight_cost + idc_cost)

WI-029 Option (ii), owner-ruled 2026-07-25: this is a COMPARISON channel.
The model's own DCF headline keeps its even-spend idc_factor and keeps
total_capital = overnight_capital (Option C), so CAS60 never enters the
headline capital base and the two channels cannot double-count. `crf` is
supplied by the plant from the capital-recovery factor it already
computes; `idc_cost` is the Item-3 CAS60 reported line — no new IDC
arithmetic is introduced here.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py (pin 0254385)
*Ref**: costs.py:547-556 (cas90_annualized_capital = CRF * total_capital);
costs.py:286-297 (cas60_idc); model.py:1483-1605 (total_cap = overnight + c60)
*Basis**: 1costingFE annualized capital charge over overnight + IDC

Inputs:
    - crf: crf parameter
    - overnight_cost: overnight_cost parameter
    - idc_cost: idc_cost parameter

Outputs:
    - cas90: cas90 result

SysML Source: root-0/analyses/mfe_account_costs.sysml:872

SysML Source: root-0/analyses/mfe_account_costs.sysml:872

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_account_costs/n_1cfe_form_capital_charge_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float


class n_1cfe_Form_Capital_ChargeInput(BaseModel):
    """Input model for n_1cfe_Form_Capital_ChargeModule.

    Attributes:
        crf: crf input
        overnight_cost: overnight_cost input
        idc_cost: idc_cost input
    """
    crf: float = Field(..., description="crf input")
    overnight_cost: float = Field(..., description="overnight_cost input")
    idc_cost: float = Field(..., description="idc_cost input")


class n_1cfe_Form_Capital_ChargeModule(ModuleBase[n_1cfe_Form_Capital_ChargeInput, Float]):
    """TEAx module for n_1cfe_Form_Capital_Charge calculation.

CAS90 in 1costingFE's financing form — the annual capital charge on
overnight capital PLUS the closed-form CAS60 interest during
construction:

  cas90 = crf * (overnight_cost + idc_cost)

WI-029 Option (ii), owner-ruled 2026-07-25: this is a COMPARISON channel.
The model's own DCF headline keeps its even-spend idc_factor and keeps
total_capital = overnight_capital (Option C), so CAS60 never enters the
headline capital base and the two channels cannot double-count. `crf` is
supplied by the plant from the capital-recovery factor it already
computes; `idc_cost` is the Item-3 CAS60 reported line — no new IDC
arithmetic is introduced here.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py (pin 0254385)
*Ref**: costs.py:547-556 (cas90_annualized_capital = CRF * total_capital);
costs.py:286-297 (cas60_idc); model.py:1483-1605 (total_cap = overnight + c60)
*Basis**: 1costingFE annualized capital charge over overnight + IDC

Inputs:
    - crf: crf parameter
    - overnight_cost: overnight_cost parameter
    - idc_cost: idc_cost parameter

Outputs:
    - cas90: cas90 result

SysML Source: root-0/analyses/mfe_account_costs.sysml:872

    SysML Source: root-0/analyses/mfe_account_costs.sysml:872

    Calculation Specification:
        cas90 = crf * (overnight_cost + idc_cost)
        
Documentation:
CAS90 in 1costingFE's financing form — the annual capital charge on
overnight capital PLUS the closed-form CAS60 interest during
construction:

  cas90 = crf * (overnight_cost + idc_cost)

WI-029 Option (ii), owner-ruled 2026-07-25: this is a COMPARISON channel.
The model's own DCF headline keeps its even-spend idc_factor and keeps
total_capital = overnight_capital (Option C), so CAS60 never enters the
headline capital base and the two channels cannot double-count. `crf` is
supplied by the plant from the capital-recovery factor it already
computes; `idc_cost` is the Item-3 CAS60 reported line — no new IDC
arithmetic is introduced here.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py (pin 0254385)
*Ref**: costs.py:547-556 (cas90_annualized_capital = CRF * total_capital);
costs.py:286-297 (cas60_idc); model.py:1483-1605 (total_cap = overnight + c60)
*Basis**: 1costingFE annualized capital charge over overnight + IDC

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_account_costs.n_1cfe_form_capital_charge_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "n_1cfe_Form_Capital_ChargeModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, crf: float, overnight_cost: float, idc_cost: float    ) -> n_1cfe_Form_Capital_ChargeInput:
        """Validate inputs and fill defaults.

        Args:
            crf: crf input
            overnight_cost: overnight_cost input
            idc_cost: idc_cost input

        Returns:
            Validated input model
        """
        return n_1cfe_Form_Capital_ChargeInput(crf=crf, overnight_cost=overnight_cost, idc_cost=idc_cost)

    def run(
        self, crf: float, overnight_cost: float, idc_cost: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            crf: crf input
            overnight_cost: overnight_cost input
            idc_cost: idc_cost input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(crf, overnight_cost, idc_cost)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_account_costs.n_1cfe_form_capital_charge_impl import (
            run_n_1cfe_form_capital_charge,
        )

        # Execute implementation - returns single value
        cas90 = run_n_1cfe_form_capital_charge(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(cas90))
