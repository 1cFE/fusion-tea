"""Selected_Stock_AtomsModule Module Wrapper

TEAx module for Selected_Stock_Atoms calculation.

*Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22.

Inputs:
    - stock_kg_in: stock_kg_in parameter
    - atom_mass_in: atom_mass_in parameter

Outputs:
    - stock_kg: stock_kg result
    - atoms: atoms result

SysML Source: root-0/integrated_equipment_costs.sysml:37

SysML Source: root-0/integrated_equipment_costs.sysml:37

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/integrated_equipment_costs/selected_stock_atoms_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from combinations_tea.primitives import Float
from combinations_tea.schemas.selected_stock_atoms_output import Selected_Stock_AtomsOutput


class Selected_Stock_AtomsInput(BaseModel):
    """Input model for Selected_Stock_AtomsModule.

    Attributes:
        stock_kg_in: stock_kg_in input
        atom_mass_in: atom_mass_in input
    """
    stock_kg_in: float = Field(..., description="stock_kg_in input")
    atom_mass_in: float = Field(..., description="atom_mass_in input")


class Selected_Stock_AtomsModule(ModuleBase[Selected_Stock_AtomsInput, Selected_Stock_AtomsOutput]):
    """TEAx module for Selected_Stock_Atoms calculation.

*Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22.

Inputs:
    - stock_kg_in: stock_kg_in parameter
    - atom_mass_in: atom_mass_in parameter

Outputs:
    - stock_kg: stock_kg result
    - atoms: atoms result

SysML Source: root-0/integrated_equipment_costs.sysml:37

    SysML Source: root-0/integrated_equipment_costs.sysml:37

    Calculation Specification:
        See documentation:
*Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22.

    IMPLEMENTATION: See combinations_tea.handwritten.integrated_equipment_costs.selected_stock_atoms_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts stock_kg, atoms fields to separate channels.
    """

    name: str = "Selected_Stock_AtomsModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, stock_kg_in: float, atom_mass_in: float    ) -> Selected_Stock_AtomsInput:
        """Validate inputs and fill defaults.

        Args:
            stock_kg_in: stock_kg_in input
            atom_mass_in: atom_mass_in input

        Returns:
            Validated input model
        """
        return Selected_Stock_AtomsInput(stock_kg_in=stock_kg_in, atom_mass_in=atom_mass_in)

    def run(
        self, stock_kg_in: float, atom_mass_in: float    ) -> ModuleResult[Selected_Stock_AtomsOutput]:
        """Execute calculation.

        Args:
            stock_kg_in: stock_kg_in input
            atom_mass_in: atom_mass_in input

        Returns:
            Module result with Selected_Stock_AtomsOutput (stock_kg, atoms)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(stock_kg_in, atom_mass_in)

        # Import handwritten implementation
        from combinations_tea.handwritten.integrated_equipment_costs.selected_stock_atoms_impl import (
            run_selected_stock_atoms,
        )

        # Execute implementation - returns tuple of values
        stock_kg, atoms = run_selected_stock_atoms(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Selected_Stock_AtomsOutput(
                stock_kg=stock_kg,
                atoms=atoms,
            )
        )
