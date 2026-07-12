"""ElectricalPanelCostCalcModule Module Wrapper

TEAx module for ElectricalPanelCostCalc calculation.

Cost calculation for electrical panel and breakers.
Base cost plus per-circuit cost.

*Source**: Solar industry cost modeling
*Last Updated**: 2026-02-01

Inputs:
    - circuit_count: circuit_count parameter
    - base_cost: base_cost parameter
    - cost_per_circuit: cost_per_circuit parameter
    - fab_factor: fab_factor parameter
    - install_factor: install_factor parameter

Outputs:
    - material_cost: material_cost result
    - fab_cost: fab_cost result
    - install_cost: install_cost result
    - total_cost: total_cost result
    - idiot_index: idiot_index result

SysML Source: solar_battery_model/library.sysml:187

SysML Source: solar_battery_model/library.sysml:187

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/solarbatterylibrary/electricalpanelcostcalc_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from solar_battery_tea.primitives import Float
from solar_battery_tea.schemas.electricalpanelcostcalc_output import ElectricalPanelCostCalcOutput


class ElectricalPanelCostCalcInput(BaseModel):
    """Input model for ElectricalPanelCostCalcModule.

    Attributes:
        circuit_count: circuit_count input
        base_cost: base_cost input
        cost_per_circuit: cost_per_circuit input
        fab_factor: fab_factor input
        install_factor: install_factor input
    """
    circuit_count: float = Field(..., description="circuit_count input")
    base_cost: float = Field(..., description="base_cost input")
    cost_per_circuit: float = Field(..., description="cost_per_circuit input")
    fab_factor: float = Field(..., description="fab_factor input")
    install_factor: float = Field(..., description="install_factor input")


class ElectricalPanelCostCalcModule(ModuleBase[ElectricalPanelCostCalcInput, ElectricalPanelCostCalcOutput]):
    """TEAx module for ElectricalPanelCostCalc calculation.

Cost calculation for electrical panel and breakers.
Base cost plus per-circuit cost.

*Source**: Solar industry cost modeling
*Last Updated**: 2026-02-01

Inputs:
    - circuit_count: circuit_count parameter
    - base_cost: base_cost parameter
    - cost_per_circuit: cost_per_circuit parameter
    - fab_factor: fab_factor parameter
    - install_factor: install_factor parameter

Outputs:
    - material_cost: material_cost result
    - fab_cost: fab_cost result
    - install_cost: install_cost result
    - total_cost: total_cost result
    - idiot_index: idiot_index result

SysML Source: solar_battery_model/library.sysml:187

    SysML Source: solar_battery_model/library.sysml:187

    Calculation Specification:
        base_cost = LiteralRationalEvaluation()
        cost_per_circuit = LiteralRationalEvaluation()
        fab_factor = LiteralRationalEvaluation()
        install_factor = LiteralRationalEvaluation()
        material_cost = base_cost + circuit_count * cost_per_circuit
        fab_cost = material_cost * fab_factor
        install_cost = material_cost * install_factor
        total_cost = material_cost + fab_cost + install_cost
        idiot_index = total_cost / material_cost
        
Documentation:
Cost calculation for electrical panel and breakers.
Base cost plus per-circuit cost.

*Source**: Solar industry cost modeling
*Last Updated**: 2026-02-01

    IMPLEMENTATION: See solar_battery_tea.handwritten.solarbatterylibrary.electricalpanelcostcalc_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts material_cost, fab_cost, install_cost, total_cost, idiot_index fields to separate channels.
    """

    name: str = "ElectricalPanelCostCalcModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, circuit_count: float, base_cost: float, cost_per_circuit: float, fab_factor: float, install_factor: float    ) -> ElectricalPanelCostCalcInput:
        """Validate inputs and fill defaults.

        Args:
            circuit_count: circuit_count input
            base_cost: base_cost input
            cost_per_circuit: cost_per_circuit input
            fab_factor: fab_factor input
            install_factor: install_factor input

        Returns:
            Validated input model
        """
        return ElectricalPanelCostCalcInput(circuit_count=circuit_count, base_cost=base_cost, cost_per_circuit=cost_per_circuit, fab_factor=fab_factor, install_factor=install_factor)

    def run(
        self, circuit_count: float, base_cost: float, cost_per_circuit: float, fab_factor: float, install_factor: float    ) -> ModuleResult[ElectricalPanelCostCalcOutput]:
        """Execute calculation.

        Args:
            circuit_count: circuit_count input
            base_cost: base_cost input
            cost_per_circuit: cost_per_circuit input
            fab_factor: fab_factor input
            install_factor: install_factor input

        Returns:
            Module result with ElectricalPanelCostCalcOutput (material_cost, fab_cost, install_cost, total_cost, idiot_index)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(circuit_count, base_cost, cost_per_circuit, fab_factor, install_factor)

        # Import handwritten implementation
        from solar_battery_tea.handwritten.solarbatterylibrary.electricalpanelcostcalc_impl import (
            run_electricalpanelcostcalc,
        )

        # Execute implementation - returns tuple of values
        material_cost, fab_cost, install_cost, total_cost, idiot_index = run_electricalpanelcostcalc(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=ElectricalPanelCostCalcOutput(
                material_cost=material_cost,
                fab_cost=fab_cost,
                install_cost=install_cost,
                total_cost=total_cost,
                idiot_index=idiot_index,
            )
        )
