"""Meier_COEModule Module Wrapper

TEAx module for Meier_COE calculation.

Cost of Electricity from Meier's engineering-economic model.
Combines fixed charge rate (8.3%) and O&M rate (3%) into a
single capital charge rate (11.3%), then divides by annual
energy production.

Constants: 0.113 = R + M (8.3% fixed charge + 3% O&M),
0.0876 = GW-to-$/kWh conversion (8760 hr/yr * 1e6 kW/GW / 100 cents/$).

*Source**: knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/output.md
*Ref**: Eq. 1 (lines 76-102)
*Basis**: Meier 1986 COE formula. Year-dollars: 1988$.

Inputs:
    - total_capital_billions: total_capital_billions parameter
    - availability: availability parameter
    - net_electric_power_gw: net_electric_power_gw parameter

Outputs:
    - coe_cents_kwh: coe_cents_kwh result

SysML Source: /home/reid/1cfe/fusion-tea/exploration/ife_e2e/models/analyses/hif_economics.sysml:84

SysML Source: /home/reid/1cfe/fusion-tea/exploration/ife_e2e/models/analyses/hif_economics.sysml:84

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/hif_economics/meier_coe_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from ife_tea.primitives import Float


class Meier_COEInput(BaseModel):
    """Input model for Meier_COEModule.

    Attributes:
        total_capital_billions: total_capital_billions input
        availability: availability input
        net_electric_power_gw: net_electric_power_gw input
    """
    total_capital_billions: float = Field(..., description="total_capital_billions input")
    availability: float = Field(..., description="availability input")
    net_electric_power_gw: float = Field(..., description="net_electric_power_gw input")


class Meier_COEModule(ModuleBase[Meier_COEInput, Float]):
    """TEAx module for Meier_COE calculation.

Cost of Electricity from Meier's engineering-economic model.
Combines fixed charge rate (8.3%) and O&M rate (3%) into a
single capital charge rate (11.3%), then divides by annual
energy production.

Constants: 0.113 = R + M (8.3% fixed charge + 3% O&M),
0.0876 = GW-to-$/kWh conversion (8760 hr/yr * 1e6 kW/GW / 100 cents/$).

*Source**: knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/output.md
*Ref**: Eq. 1 (lines 76-102)
*Basis**: Meier 1986 COE formula. Year-dollars: 1988$.

Inputs:
    - total_capital_billions: total_capital_billions parameter
    - availability: availability parameter
    - net_electric_power_gw: net_electric_power_gw parameter

Outputs:
    - coe_cents_kwh: coe_cents_kwh result

SysML Source: /home/reid/1cfe/fusion-tea/exploration/ife_e2e/models/analyses/hif_economics.sysml:84

    SysML Source: /home/reid/1cfe/fusion-tea/exploration/ife_e2e/models/analyses/hif_economics.sysml:84

    Calculation Specification:
        coe_cents_kwh = 0.113 * total_capital_billions / (0.0876 * availability * net_electric_power_gw)
        
Documentation:
Cost of Electricity from Meier's engineering-economic model.
Combines fixed charge rate (8.3%) and O&M rate (3%) into a
single capital charge rate (11.3%), then divides by annual
energy production.

Constants: 0.113 = R + M (8.3% fixed charge + 3% O&M),
0.0876 = GW-to-$/kWh conversion (8760 hr/yr * 1e6 kW/GW / 100 cents/$).

*Source**: knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/output.md
*Ref**: Eq. 1 (lines 76-102)
*Basis**: Meier 1986 COE formula. Year-dollars: 1988$.

    IMPLEMENTATION: See ife_tea.handwritten.hif_economics.meier_coe_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "Meier_COEModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, total_capital_billions: float, availability: float, net_electric_power_gw: float    ) -> Meier_COEInput:
        """Validate inputs and fill defaults.

        Args:
            total_capital_billions: total_capital_billions input
            availability: availability input
            net_electric_power_gw: net_electric_power_gw input

        Returns:
            Validated input model
        """
        return Meier_COEInput(total_capital_billions=total_capital_billions, availability=availability, net_electric_power_gw=net_electric_power_gw)

    def run(
        self, total_capital_billions: float, availability: float, net_electric_power_gw: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            total_capital_billions: total_capital_billions input
            availability: availability input
            net_electric_power_gw: net_electric_power_gw input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(total_capital_billions, availability, net_electric_power_gw)

        # Import handwritten implementation
        from ife_tea.handwritten.hif_economics.meier_coe_impl import (
            run_meier_coe,
        )

        # Execute implementation - returns single value
        coe_cents_kwh = run_meier_coe(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(coe_cents_kwh))
