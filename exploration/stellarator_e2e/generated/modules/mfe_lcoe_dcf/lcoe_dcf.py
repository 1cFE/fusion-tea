"""LCOE_DCFModule Module Wrapper

TEAx module for LCOE_DCF calculation.

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

Inputs:
    - discount_rate_in: discount_rate_in parameter
    - availability_in: availability_in parameter
    - construction_years_in: construction_years_in parameter
    - net_electric_mw: net_electric_mw parameter
    - annual_om_in: annual_om_in parameter
    - operational_years_in: operational_years_in parameter
    - total_capital_in: total_capital_in parameter

Outputs:
    - lcoe: lcoe result

SysML Source: root-0/analyses/mfe_lcoe_dcf.sysml:4

SysML Source: root-0/analyses/mfe_lcoe_dcf.sysml:4

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_lcoe_dcf/lcoe_dcf_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float


class LCOE_DCFInput(BaseModel):
    """Input model for LCOE_DCFModule.

    Attributes:
        discount_rate_in: discount_rate_in input
        availability_in: availability_in input
        construction_years_in: construction_years_in input
        net_electric_mw: net_electric_mw input
        annual_om_in: annual_om_in input
        operational_years_in: operational_years_in input
        total_capital_in: total_capital_in input
    """
    discount_rate_in: float = Field(..., description="discount_rate_in input")
    availability_in: float = Field(..., description="availability_in input")
    construction_years_in: float = Field(..., description="construction_years_in input")
    net_electric_mw: float = Field(..., description="net_electric_mw input")
    annual_om_in: float = Field(..., description="annual_om_in input")
    operational_years_in: float = Field(..., description="operational_years_in input")
    total_capital_in: float = Field(..., description="total_capital_in input")


class LCOE_DCFModule(ModuleBase[LCOE_DCFInput, Float]):
    """TEAx module for LCOE_DCF calculation.

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

Inputs:
    - discount_rate_in: discount_rate_in parameter
    - availability_in: availability_in parameter
    - construction_years_in: construction_years_in parameter
    - net_electric_mw: net_electric_mw parameter
    - annual_om_in: annual_om_in parameter
    - operational_years_in: operational_years_in parameter
    - total_capital_in: total_capital_in parameter

Outputs:
    - lcoe: lcoe result

SysML Source: root-0/analyses/mfe_lcoe_dcf.sysml:4

    SysML Source: root-0/analyses/mfe_lcoe_dcf.sysml:4

    Calculation Specification:
        discount_pow_n = (1.0 + discount_rate_in) ** operational_years_in
        crf = discount_rate_in * discount_pow_n / (discount_pow_n - 1.0)
        idc_factor = (1.0 + discount_rate_in) ** (construction_years_in / 2.0)
        annual_capital = total_capital_in * idc_factor * crf
        annual_energy_mwh = 8760.0 * net_electric_mw * availability_in
        lcoe = (annual_capital + annual_om_in) / annual_energy_mwh
        
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

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_lcoe_dcf.lcoe_dcf_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "LCOE_DCFModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, discount_rate_in: float, availability_in: float, construction_years_in: float, net_electric_mw: float, annual_om_in: float, operational_years_in: float, total_capital_in: float    ) -> LCOE_DCFInput:
        """Validate inputs and fill defaults.

        Args:
            discount_rate_in: discount_rate_in input
            availability_in: availability_in input
            construction_years_in: construction_years_in input
            net_electric_mw: net_electric_mw input
            annual_om_in: annual_om_in input
            operational_years_in: operational_years_in input
            total_capital_in: total_capital_in input

        Returns:
            Validated input model
        """
        return LCOE_DCFInput(discount_rate_in=discount_rate_in, availability_in=availability_in, construction_years_in=construction_years_in, net_electric_mw=net_electric_mw, annual_om_in=annual_om_in, operational_years_in=operational_years_in, total_capital_in=total_capital_in)

    def run(
        self, discount_rate_in: float, availability_in: float, construction_years_in: float, net_electric_mw: float, annual_om_in: float, operational_years_in: float, total_capital_in: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            discount_rate_in: discount_rate_in input
            availability_in: availability_in input
            construction_years_in: construction_years_in input
            net_electric_mw: net_electric_mw input
            annual_om_in: annual_om_in input
            operational_years_in: operational_years_in input
            total_capital_in: total_capital_in input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(discount_rate_in, availability_in, construction_years_in, net_electric_mw, annual_om_in, operational_years_in, total_capital_in)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_lcoe_dcf.lcoe_dcf_impl import (
            run_lcoe_dcf,
        )

        # Execute implementation - returns single value
        lcoe = run_lcoe_dcf(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(lcoe))
