"""Cooling_Energy_AdditionModule Module Wrapper

TEAx module for Cooling_Energy_Addition calculation.

Add intermediate pump electricity and recovered shaft work together.
This producer has no cost inputs: the legacy cost reads plant net power,
so combining its inputs with this producer would create a dependency cycle.
Source: work/active/WI-067_installed-cooling-equipment-costs/combined-design.md
Ref: Corrective review details; Basis: separate acyclic energy ownership.

Inputs:
    - primary_recovered_in: primary_recovered_in parameter
    - secondary_mode_in: secondary_mode_in parameter
    - primary_electric_in: primary_electric_in parameter
    - salt_shaft_in: salt_shaft_in parameter
    - salt_electric_in: salt_electric_in parameter

Outputs:
    - electric_total: electric_total result
    - recovered_total: recovered_total result

SysML Source: root-0/analyses/mfe_cooling_accounts.sysml:42

SysML Source: root-0/analyses/mfe_cooling_accounts.sysml:42

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_cooling_accounts/cooling_energy_addition_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_rebco_tea.primitives import Float
from stellarator_materials_rebco_tea.schemas.cooling_energy_addition_output import Cooling_Energy_AdditionOutput


class Cooling_Energy_AdditionInput(BaseModel):
    """Input model for Cooling_Energy_AdditionModule.

    Attributes:
        primary_recovered_in: primary_recovered_in input
        secondary_mode_in: secondary_mode_in input
        primary_electric_in: primary_electric_in input
        salt_shaft_in: salt_shaft_in input
        salt_electric_in: salt_electric_in input
    """
    primary_recovered_in: float = Field(..., description="primary_recovered_in input")
    secondary_mode_in: float = Field(..., description="secondary_mode_in input")
    primary_electric_in: float = Field(..., description="primary_electric_in input")
    salt_shaft_in: float = Field(..., description="salt_shaft_in input")
    salt_electric_in: float = Field(..., description="salt_electric_in input")


class Cooling_Energy_AdditionModule(ModuleBase[Cooling_Energy_AdditionInput, Cooling_Energy_AdditionOutput]):
    """TEAx module for Cooling_Energy_Addition calculation.

Add intermediate pump electricity and recovered shaft work together.
This producer has no cost inputs: the legacy cost reads plant net power,
so combining its inputs with this producer would create a dependency cycle.
Source: work/active/WI-067_installed-cooling-equipment-costs/combined-design.md
Ref: Corrective review details; Basis: separate acyclic energy ownership.

Inputs:
    - primary_recovered_in: primary_recovered_in parameter
    - secondary_mode_in: secondary_mode_in parameter
    - primary_electric_in: primary_electric_in parameter
    - salt_shaft_in: salt_shaft_in parameter
    - salt_electric_in: salt_electric_in parameter

Outputs:
    - electric_total: electric_total result
    - recovered_total: recovered_total result

SysML Source: root-0/analyses/mfe_cooling_accounts.sysml:42

    SysML Source: root-0/analyses/mfe_cooling_accounts.sysml:42

    Calculation Specification:
        electric_total = primary_electric_in + secondary_mode_in * salt_electric_in
        recovered_total = primary_recovered_in + secondary_mode_in * salt_shaft_in
        
Documentation:
Add intermediate pump electricity and recovered shaft work together.
This producer has no cost inputs: the legacy cost reads plant net power,
so combining its inputs with this producer would create a dependency cycle.
Source: work/active/WI-067_installed-cooling-equipment-costs/combined-design.md
Ref: Corrective review details; Basis: separate acyclic energy ownership.

    IMPLEMENTATION: See stellarator_materials_rebco_tea.handwritten.mfe_cooling_accounts.cooling_energy_addition_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts electric_total, recovered_total fields to separate channels.
    """

    name: str = "Cooling_Energy_AdditionModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, primary_recovered_in: float, secondary_mode_in: float, primary_electric_in: float, salt_shaft_in: float, salt_electric_in: float    ) -> Cooling_Energy_AdditionInput:
        """Validate inputs and fill defaults.

        Args:
            primary_recovered_in: primary_recovered_in input
            secondary_mode_in: secondary_mode_in input
            primary_electric_in: primary_electric_in input
            salt_shaft_in: salt_shaft_in input
            salt_electric_in: salt_electric_in input

        Returns:
            Validated input model
        """
        return Cooling_Energy_AdditionInput(primary_recovered_in=primary_recovered_in, secondary_mode_in=secondary_mode_in, primary_electric_in=primary_electric_in, salt_shaft_in=salt_shaft_in, salt_electric_in=salt_electric_in)

    def run(
        self, primary_recovered_in: float, secondary_mode_in: float, primary_electric_in: float, salt_shaft_in: float, salt_electric_in: float    ) -> ModuleResult[Cooling_Energy_AdditionOutput]:
        """Execute calculation.

        Args:
            primary_recovered_in: primary_recovered_in input
            secondary_mode_in: secondary_mode_in input
            primary_electric_in: primary_electric_in input
            salt_shaft_in: salt_shaft_in input
            salt_electric_in: salt_electric_in input

        Returns:
            Module result with Cooling_Energy_AdditionOutput (electric_total, recovered_total)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(primary_recovered_in, secondary_mode_in, primary_electric_in, salt_shaft_in, salt_electric_in)

        # Import handwritten implementation
        from stellarator_materials_rebco_tea.handwritten.mfe_cooling_accounts.cooling_energy_addition_impl import (
            run_cooling_energy_addition,
        )

        # Execute implementation - returns tuple of values
        electric_total, recovered_total = run_cooling_energy_addition(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Cooling_Energy_AdditionOutput(
                electric_total=electric_total,
                recovered_total=recovered_total,
            )
        )
