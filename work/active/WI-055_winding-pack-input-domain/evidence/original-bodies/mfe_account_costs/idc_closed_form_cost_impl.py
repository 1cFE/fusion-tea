"""Typed completion of the native IDC_Closed_Form_Cost equations.

Source: models/library/analyses/mfe_account_costs.sysml, 'IDC Closed-Form Cost'.
Ref: work/active/WI-052_mfe-financial-rate-limits/design.md, Numerical method and justification.
Basis: stable factors with unchanged cash-flow timing and currency; annual cost
returns (levelized, crf), the emitted public wrapper order.
Last Updated: 2026-09-12 (native equations and wrapper verified).
"""
import math
from stellarator_tea.modules.mfe_account_costs.idc_closed_form_cost import IDC_Closed_Form_CostInput
from stellarator_tea.handwritten.mfe_account_costs.financial_factors import crf, annuity_pv, idc

AUTO_IMPLEMENTED = False

def run_idc_closed_form_cost(inputs: IDC_Closed_Form_CostInput) -> float:
    return idc(inputs.interest_rate, inputs.construction_years_in) * inputs.overnight_cost
