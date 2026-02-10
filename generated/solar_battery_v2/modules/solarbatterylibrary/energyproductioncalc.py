"""EnergyProductionCalcModule Module Wrapper

TEAx module for EnergyProductionCalc calculation.

Annual energy production calculation.
Matches PyFECONS lcoe.py denominator: 8760 * p_net * n_mod * plant_availability.

*Source**: PyFECONS /home/reid/PyFECONS/pyfecons/costing/calculations/lcoe.py:24
*Last Updated**: 2026-02-01

Inputs:
    - p_net_mw: p_net_mw parameter
    - n_mod: n_mod parameter
    - plant_availability: plant_availability parameter

Outputs:
    - annual_energy_mwh: annual_energy_mwh result

SysML Source: models/tests/solar_battery/library.sysml:267

SysML Source: models/tests/solar_battery/library.sysml:267

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/solarbatterylibrary/energyproductioncalc_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from solar_battery_v2.primitives import Float


class EnergyProductionCalcInput(BaseModel):
    """Input model for EnergyProductionCalcModule.

    Attributes:
        p_net_mw: p_net_mw input
        n_mod: n_mod input
        plant_availability: plant_availability input
    """
    p_net_mw: float = Field(..., description="p_net_mw input")
    n_mod: float = Field(..., description="n_mod input")
    plant_availability: float = Field(..., description="plant_availability input")


class EnergyProductionCalcModule(ModuleBase[EnergyProductionCalcInput, Float]):
    """TEAx module for EnergyProductionCalc calculation.

Annual energy production calculation.
Matches PyFECONS lcoe.py denominator: 8760 * p_net * n_mod * plant_availability.

*Source**: PyFECONS /home/reid/PyFECONS/pyfecons/costing/calculations/lcoe.py:24
*Last Updated**: 2026-02-01

Inputs:
    - p_net_mw: p_net_mw parameter
    - n_mod: n_mod parameter
    - plant_availability: plant_availability parameter

Outputs:
    - annual_energy_mwh: annual_energy_mwh result

SysML Source: models/tests/solar_battery/library.sysml:267

    SysML Source: models/tests/solar_battery/library.sysml:267

    Calculation Specification:
        annual_energy_mwh = 8760.0 * p_net_mw * n_mod * plant_availability
        
Documentation:
Annual energy production calculation.
Matches PyFECONS lcoe.py denominator: 8760 * p_net * n_mod * plant_availability.

*Source**: PyFECONS /home/reid/PyFECONS/pyfecons/costing/calculations/lcoe.py:24
*Last Updated**: 2026-02-01

    IMPLEMENTATION: See solar_battery_v2.handwritten.solarbatterylibrary.energyproductioncalc_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "EnergyProductionCalcModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, p_net_mw: float, n_mod: float, plant_availability: float    ) -> EnergyProductionCalcInput:
        """Validate inputs and fill defaults.

        Args:
            p_net_mw: p_net_mw input
            n_mod: n_mod input
            plant_availability: plant_availability input

        Returns:
            Validated input model
        """
        return EnergyProductionCalcInput(p_net_mw=p_net_mw, n_mod=n_mod, plant_availability=plant_availability)

    def run(
        self, p_net_mw: float, n_mod: float, plant_availability: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            p_net_mw: p_net_mw input
            n_mod: n_mod input
            plant_availability: plant_availability input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(p_net_mw, n_mod, plant_availability)

        # Import handwritten implementation
        from solar_battery_v2.handwritten.solarbatterylibrary.energyproductioncalc_impl import (
            run_energyproductioncalc,
        )

        # Execute implementation - returns single value
        annual_energy_mwh = run_energyproductioncalc(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(annual_energy_mwh))
