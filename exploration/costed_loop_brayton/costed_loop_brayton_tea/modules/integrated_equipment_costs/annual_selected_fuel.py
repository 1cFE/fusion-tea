"""Annual_Selected_FuelModule Module Wrapper

TEAx module for Annual_Selected_Fuel calculation.

*Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22.

Inputs:
    - seconds_in: seconds_in parameter
    - burn_in: burn_in parameter
    - availability_in: availability_in parameter
    - stock_kg_in: stock_kg_in parameter
    - exhaust_in: exhaust_in parameter
    - tritium_price_in: tritium_price_in parameter
    - residence_in: residence_in parameter
    - decay_in: decay_in parameter
    - loss_in: loss_in parameter
    - atom_mass_in: atom_mass_in parameter
    - annual_recovery_in: annual_recovery_in parameter

Outputs:
    - annual_loss: annual_loss result
    - annual_cost: annual_cost result
    - annual_burn: annual_burn result
    - annual_recovery: annual_recovery result
    - annual_decay: annual_decay result
    - annual_external: annual_external result
    - required_stock: required_stock result
    - breeding_supported: breeding_supported result

SysML Source: root-0/integrated_equipment_costs.sysml:44

SysML Source: root-0/integrated_equipment_costs.sysml:44

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/integrated_equipment_costs/annual_selected_fuel_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from costed_loop_brayton_tea.primitives import Float
from costed_loop_brayton_tea.schemas.annual_selected_fuel_output import Annual_Selected_FuelOutput


class Annual_Selected_FuelInput(BaseModel):
    """Input model for Annual_Selected_FuelModule.

    Attributes:
        seconds_in: seconds_in input
        burn_in: burn_in input
        availability_in: availability_in input
        stock_kg_in: stock_kg_in input
        exhaust_in: exhaust_in input
        tritium_price_in: tritium_price_in input
        residence_in: residence_in input
        decay_in: decay_in input
        loss_in: loss_in input
        atom_mass_in: atom_mass_in input
        annual_recovery_in: annual_recovery_in input
    """
    seconds_in: float = Field(..., description="seconds_in input")
    burn_in: float = Field(..., description="burn_in input")
    availability_in: float = Field(..., description="availability_in input")
    stock_kg_in: float = Field(..., description="stock_kg_in input")
    exhaust_in: float = Field(..., description="exhaust_in input")
    tritium_price_in: float = Field(..., description="tritium_price_in input")
    residence_in: float = Field(..., description="residence_in input")
    decay_in: float = Field(..., description="decay_in input")
    loss_in: float = Field(..., description="loss_in input")
    atom_mass_in: float = Field(..., description="atom_mass_in input")
    annual_recovery_in: float = Field(..., description="annual_recovery_in input")


class Annual_Selected_FuelModule(ModuleBase[Annual_Selected_FuelInput, Annual_Selected_FuelOutput]):
    """TEAx module for Annual_Selected_Fuel calculation.

*Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22.

Inputs:
    - seconds_in: seconds_in parameter
    - burn_in: burn_in parameter
    - availability_in: availability_in parameter
    - stock_kg_in: stock_kg_in parameter
    - exhaust_in: exhaust_in parameter
    - tritium_price_in: tritium_price_in parameter
    - residence_in: residence_in parameter
    - decay_in: decay_in parameter
    - loss_in: loss_in parameter
    - atom_mass_in: atom_mass_in parameter
    - annual_recovery_in: annual_recovery_in parameter

Outputs:
    - annual_loss: annual_loss result
    - annual_cost: annual_cost result
    - annual_burn: annual_burn result
    - annual_recovery: annual_recovery result
    - annual_decay: annual_decay result
    - annual_external: annual_external result
    - required_stock: required_stock result
    - breeding_supported: breeding_supported result

SysML Source: root-0/integrated_equipment_costs.sysml:44

    SysML Source: root-0/integrated_equipment_costs.sysml:44

    Calculation Specification:
        See documentation:
*Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22.

    IMPLEMENTATION: See costed_loop_brayton_tea.handwritten.integrated_equipment_costs.annual_selected_fuel_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts annual_loss, annual_cost, annual_burn, annual_recovery, annual_decay, annual_external, required_stock, breeding_supported fields to separate channels.
    """

    name: str = "Annual_Selected_FuelModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, seconds_in: float, burn_in: float, availability_in: float, stock_kg_in: float, exhaust_in: float, tritium_price_in: float, residence_in: float, decay_in: float, loss_in: float, atom_mass_in: float, annual_recovery_in: float    ) -> Annual_Selected_FuelInput:
        """Validate inputs and fill defaults.

        Args:
            seconds_in: seconds_in input
            burn_in: burn_in input
            availability_in: availability_in input
            stock_kg_in: stock_kg_in input
            exhaust_in: exhaust_in input
            tritium_price_in: tritium_price_in input
            residence_in: residence_in input
            decay_in: decay_in input
            loss_in: loss_in input
            atom_mass_in: atom_mass_in input
            annual_recovery_in: annual_recovery_in input

        Returns:
            Validated input model
        """
        return Annual_Selected_FuelInput(seconds_in=seconds_in, burn_in=burn_in, availability_in=availability_in, stock_kg_in=stock_kg_in, exhaust_in=exhaust_in, tritium_price_in=tritium_price_in, residence_in=residence_in, decay_in=decay_in, loss_in=loss_in, atom_mass_in=atom_mass_in, annual_recovery_in=annual_recovery_in)

    def run(
        self, seconds_in: float, burn_in: float, availability_in: float, stock_kg_in: float, exhaust_in: float, tritium_price_in: float, residence_in: float, decay_in: float, loss_in: float, atom_mass_in: float, annual_recovery_in: float    ) -> ModuleResult[Annual_Selected_FuelOutput]:
        """Execute calculation.

        Args:
            seconds_in: seconds_in input
            burn_in: burn_in input
            availability_in: availability_in input
            stock_kg_in: stock_kg_in input
            exhaust_in: exhaust_in input
            tritium_price_in: tritium_price_in input
            residence_in: residence_in input
            decay_in: decay_in input
            loss_in: loss_in input
            atom_mass_in: atom_mass_in input
            annual_recovery_in: annual_recovery_in input

        Returns:
            Module result with Annual_Selected_FuelOutput (annual_loss, annual_cost, annual_burn, annual_recovery, annual_decay, annual_external, required_stock, breeding_supported)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(seconds_in, burn_in, availability_in, stock_kg_in, exhaust_in, tritium_price_in, residence_in, decay_in, loss_in, atom_mass_in, annual_recovery_in)

        # Import handwritten implementation
        from costed_loop_brayton_tea.handwritten.integrated_equipment_costs.annual_selected_fuel_impl import (
            run_annual_selected_fuel,
        )

        # Execute implementation - returns tuple of values
        annual_loss, annual_cost, annual_burn, annual_recovery, annual_decay, annual_external, required_stock, breeding_supported = run_annual_selected_fuel(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Annual_Selected_FuelOutput(
                annual_loss=annual_loss,
                annual_cost=annual_cost,
                annual_burn=annual_burn,
                annual_recovery=annual_recovery,
                annual_decay=annual_decay,
                annual_external=annual_external,
                required_stock=required_stock,
                breeding_supported=breeding_supported,
            )
        )
