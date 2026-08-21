"""Auto-generated implementation for n_1cfe_Form_Capital_Charge.

AUTO_IMPLEMENTED = True

SysML Source: root-0/analyses/mfe_account_costs.sysml:871

SysML Expressions:
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
"""

AUTO_IMPLEMENTED = True

from stellarator_tea.modules.mfe_account_costs.n_1cfe_form_capital_charge import n_1cfe_Form_Capital_ChargeInput


def run_n_1cfe_form_capital_charge(inputs: n_1cfe_Form_Capital_ChargeInput) -> float:
    """Execute n_1cfe_Form_Capital_Charge calculation.

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

SysML Source: root-0/analyses/mfe_account_costs.sysml:871

SysML Expressions:
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

Args:
    inputs: Input parameters validated against n_1cfe_Form_Capital_ChargeInput schema

Returns:
    float: cas90

Example:
    >>> inputs = n_1cfe_Form_Capital_ChargeInput(...)
    >>> result = run_n_1cfe_form_capital_charge(inputs)
    """
    return (inputs.crf * (inputs.overnight_cost + inputs.idc_cost))
