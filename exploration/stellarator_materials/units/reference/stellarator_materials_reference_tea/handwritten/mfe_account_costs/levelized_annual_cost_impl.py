"""Typed completion of the native Levelized_Annual_Cost equations.

Source: models/library/analyses/mfe_account_costs.sysml, 'Levelized Annual Cost'.
Ref: work/active/WI-052_mfe-financial-rate-limits/design.md, Numerical method and justification.
Basis: stable factors with unchanged cash-flow timing and currency; annual cost
returns (levelized, crf), the emitted public wrapper order.
Last Updated: 2026-09-12 (native equations and wrapper verified).
"""
import math
from stellarator_materials_reference_tea.modules.mfe_account_costs.levelized_annual_cost import Levelized_Annual_CostInput
from stellarator_materials_reference_tea.handwritten.mfe_account_costs.financial_factors import crf, annuity_pv, idc

AUTO_IMPLEMENTED = False

def run_levelized_annual_cost(inputs: Levelized_Annual_CostInput) -> tuple[float, float]:
    c = crf(inputs.interest_rate, inputs.operational_years_in)
    pv = annuity_pv(inputs.annual_cost, inputs.interest_rate, inputs.inflation_rate_in, inputs.operational_years_in, inputs.project_time)
    return c * pv, c
