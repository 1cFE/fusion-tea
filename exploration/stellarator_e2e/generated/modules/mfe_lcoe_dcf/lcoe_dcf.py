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
    - total_capital: total_capital parameter
    - annual_om: annual_om parameter
    - net_electric_mw: net_electric_mw parameter
    - availability: availability parameter
    - discount_rate: discount_rate parameter
    - construction_years: construction_years parameter
    - operational_years: operational_years parameter

Outputs:
    - lcoe: lcoe result

SysML Source: /home/reid/1cfe/fusion-tea-stellarator-mbse-demo/exploration/stellarator_e2e/models/analyses/mfe_lcoe_dcf.sysml:4

SysML Source: /home/reid/1cfe/fusion-tea-stellarator-mbse-demo/exploration/stellarator_e2e/models/analyses/mfe_lcoe_dcf.sysml:4

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_lcoe_dcf/lcoe_dcf_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float


class LCOE_DCFInput(BaseModel):
    """Input model for LCOE_DCFModule.

    Attributes:
        total_capital: total_capital input
        annual_om: annual_om input
        net_electric_mw: net_electric_mw input
        availability: availability input
        discount_rate: discount_rate input
        construction_years: construction_years input
        operational_years: operational_years input
    """
    total_capital: float = Field(..., description="total_capital input")
    annual_om: float = Field(..., description="annual_om input")
    net_electric_mw: float = Field(..., description="net_electric_mw input")
    availability: float = Field(..., description="availability input")
    discount_rate: float = Field(..., description="discount_rate input")
    construction_years: float = Field(..., description="construction_years input")
    operational_years: float = Field(..., description="operational_years input")


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
    - total_capital: total_capital parameter
    - annual_om: annual_om parameter
    - net_electric_mw: net_electric_mw parameter
    - availability: availability parameter
    - discount_rate: discount_rate parameter
    - construction_years: construction_years parameter
    - operational_years: operational_years parameter

Outputs:
    - lcoe: lcoe result

SysML Source: /home/reid/1cfe/fusion-tea-stellarator-mbse-demo/exploration/stellarator_e2e/models/analyses/mfe_lcoe_dcf.sysml:4

    SysML Source: /home/reid/1cfe/fusion-tea-stellarator-mbse-demo/exploration/stellarator_e2e/models/analyses/mfe_lcoe_dcf.sysml:4

    Calculation Specification:
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

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_lcoe_dcf.lcoe_dcf_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "LCOE_DCFModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, total_capital: float, annual_om: float, net_electric_mw: float, availability: float, discount_rate: float, construction_years: float, operational_years: float    ) -> LCOE_DCFInput:
        """Validate inputs and fill defaults.

        Args:
            total_capital: total_capital input
            annual_om: annual_om input
            net_electric_mw: net_electric_mw input
            availability: availability input
            discount_rate: discount_rate input
            construction_years: construction_years input
            operational_years: operational_years input

        Returns:
            Validated input model
        """
        return LCOE_DCFInput(total_capital=total_capital, annual_om=annual_om, net_electric_mw=net_electric_mw, availability=availability, discount_rate=discount_rate, construction_years=construction_years, operational_years=operational_years)

    def run(
        self, total_capital: float, annual_om: float, net_electric_mw: float, availability: float, discount_rate: float, construction_years: float, operational_years: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            total_capital: total_capital input
            annual_om: annual_om input
            net_electric_mw: net_electric_mw input
            availability: availability input
            discount_rate: discount_rate input
            construction_years: construction_years input
            operational_years: operational_years input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(total_capital, annual_om, net_electric_mw, availability, discount_rate, construction_years, operational_years)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_lcoe_dcf.lcoe_dcf_impl import (
            run_lcoe_dcf,
        )

        # Execute implementation - returns single value
        lcoe = run_lcoe_dcf(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(lcoe))
