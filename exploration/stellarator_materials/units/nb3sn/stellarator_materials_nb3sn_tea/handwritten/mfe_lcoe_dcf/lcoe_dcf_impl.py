"""Typed completion of the native LCOE_DCF equations.

Source: models/library/analyses/mfe_lcoe_dcf.sysml, 'LCOE DCF'.
Ref: work/active/WI-052_mfe-financial-rate-limits/design.md, Numerical method and justification.
Basis: stable factors with unchanged cash-flow timing and currency; annual cost
returns (levelized, crf), the emitted public wrapper order.
Last Updated: 2026-09-12 (native equations and wrapper verified).
"""
import math
from stellarator_materials_nb3sn_tea.modules.mfe_lcoe_dcf.lcoe_dcf import LCOE_DCFInput
from stellarator_materials_nb3sn_tea.handwritten.mfe_account_costs.financial_factors import crf, annuity_pv, idc

AUTO_IMPLEMENTED = False

def run_lcoe_dcf(inputs: LCOE_DCFInput) -> float:
    c = crf(inputs.discount_rate_in, inputs.operational_years_in)
    midpoint = math.exp(inputs.construction_years_in / 2.0 * math.log1p(inputs.discount_rate_in))
    annual_capital = inputs.total_capital_in * midpoint * c
    annual_energy = 8760.0 * inputs.net_electric_mw * inputs.availability_in
    numerator = annual_capital + inputs.annual_om_in
    return numerator / annual_energy
