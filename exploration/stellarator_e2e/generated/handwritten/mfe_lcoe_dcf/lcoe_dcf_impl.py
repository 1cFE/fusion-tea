"""Auto-generated implementation for LCOE_DCF.

AUTO_IMPLEMENTED = True

SysML Source: /home/reid/1cfe/fusion-tea-stellarator-mbse-demo/exploration/stellarator_e2e/models/analyses/mfe_lcoe_dcf.sysml:4

SysML Expressions:
    discount_pow_n = (1.0 + discount_rate) ** operational_years
    crf = discount_rate * discount_pow_n / (discount_pow_n - 1.0)
    idc_factor = (1.0 + discount_rate) ** (construction_years / 2.0)
    annual_capital = total_capital * idc_factor * crf
    annual_energy_mwh = 8760.0 * net_electric_mw * availability
    lcoe = (annual_capital + annual_om) / annual_energy_mwh
    
Documentation:
Generic discounted-cash-flow LCOE core [$/MWh]. Concept-agnostic: it
takes an already-rolled-up total capital and annual O&M plus the plant
performance and financing terms, and returns levelized cost of
electricity. Unlike 'IFE LCOE' (which bundles IFE-specific cost
categories), this is a clean DCF core reusable by any concept.

  CRF        = d*(1+d)^N / ((1+d)^N - 1)      (capital recovery factor)
  IDC factor = (1+d)^(Yc/2)                    (interest during
                                                construction, midpoint)
  annual capital = total_capital * IDC * CRF
  annual energy  = 8760 * P_net * availability [MWh/yr]
  LCOE = (annual capital + annual O&M) / annual energy

The IDC term compounds construction spend to commissioning using the
even-spend midpoint convention (Yc/2), a standard TEA financing
adjustment. CRF and the annual-energy denominator follow 1costingFE.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/economics.py
*Ref**: economics.py:6-10 (compute_crf), economics.py:88-92 (compute_lcoe)
*Basis**: Standard DCF LCOE; annuitized capital + O&M over energy sold
"""

AUTO_IMPLEMENTED = True

from stellarator_tea.modules.mfe_lcoe_dcf.lcoe_dcf import LCOE_DCFInput


def run_lcoe_dcf(inputs: LCOE_DCFInput) -> float:
    """Execute LCOE_DCF calculation.

Generic discounted-cash-flow LCOE core [$/MWh]. Concept-agnostic: it
takes an already-rolled-up total capital and annual O&M plus the plant
performance and financing terms, and returns levelized cost of
electricity. Unlike 'IFE LCOE' (which bundles IFE-specific cost
categories), this is a clean DCF core reusable by any concept.

  CRF        = d*(1+d)^N / ((1+d)^N - 1)      (capital recovery factor)
  IDC factor = (1+d)^(Yc/2)                    (interest during
                                                construction, midpoint)
  annual capital = total_capital * IDC * CRF
  annual energy  = 8760 * P_net * availability [MWh/yr]
  LCOE = (annual capital + annual O&M) / annual energy

The IDC term compounds construction spend to commissioning using the
even-spend midpoint convention (Yc/2), a standard TEA financing
adjustment. CRF and the annual-energy denominator follow 1costingFE.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/economics.py
*Ref**: economics.py:6-10 (compute_crf), economics.py:88-92 (compute_lcoe)
*Basis**: Standard DCF LCOE; annuitized capital + O&M over energy sold

SysML Source: /home/reid/1cfe/fusion-tea-stellarator-mbse-demo/exploration/stellarator_e2e/models/analyses/mfe_lcoe_dcf.sysml:4

SysML Expressions:
    discount_pow_n = (1.0 + discount_rate) ** operational_years
    crf = discount_rate * discount_pow_n / (discount_pow_n - 1.0)
    idc_factor = (1.0 + discount_rate) ** (construction_years / 2.0)
    annual_capital = total_capital * idc_factor * crf
    annual_energy_mwh = 8760.0 * net_electric_mw * availability
    lcoe = (annual_capital + annual_om) / annual_energy_mwh
    
Documentation:
Generic discounted-cash-flow LCOE core [$/MWh]. Concept-agnostic: it
takes an already-rolled-up total capital and annual O&M plus the plant
performance and financing terms, and returns levelized cost of
electricity. Unlike 'IFE LCOE' (which bundles IFE-specific cost
categories), this is a clean DCF core reusable by any concept.

  CRF        = d*(1+d)^N / ((1+d)^N - 1)      (capital recovery factor)
  IDC factor = (1+d)^(Yc/2)                    (interest during
                                                construction, midpoint)
  annual capital = total_capital * IDC * CRF
  annual energy  = 8760 * P_net * availability [MWh/yr]
  LCOE = (annual capital + annual O&M) / annual energy

The IDC term compounds construction spend to commissioning using the
even-spend midpoint convention (Yc/2), a standard TEA financing
adjustment. CRF and the annual-energy denominator follow 1costingFE.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/economics.py
*Ref**: economics.py:6-10 (compute_crf), economics.py:88-92 (compute_lcoe)
*Basis**: Standard DCF LCOE; annuitized capital + O&M over energy sold

Args:
    inputs: Input parameters validated against LCOE_DCFInput schema

Returns:
    float: lcoe

Example:
    >>> inputs = LCOE_DCFInput(...)
    >>> result = run_lcoe_dcf(inputs)
    """
    annual_energy_mwh = ((8760.0 * inputs.net_electric_mw) * inputs.availability)
    discount_pow_n = ((1.0 + inputs.discount_rate) ** inputs.operational_years)
    crf = ((inputs.discount_rate * discount_pow_n) / (discount_pow_n - 1.0))
    idc_factor = ((1.0 + inputs.discount_rate) ** (inputs.construction_years / 2.0))
    annual_capital = ((inputs.total_capital * idc_factor) * crf)
    return ((annual_capital + inputs.annual_om) / annual_energy_mwh)
