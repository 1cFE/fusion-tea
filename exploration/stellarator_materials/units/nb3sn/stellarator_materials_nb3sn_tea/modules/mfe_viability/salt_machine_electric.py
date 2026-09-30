"""Salt_Machine_ElectricModule Module Wrapper

TEAx module for Salt_Machine_Electric calculation.

Per-machine demand MW = total MW / machine count; inactive short circuits before division. Finite active arithmetic is guarded. **Source**: work/active/WI-080_supplied-thermal-equipment-capability-and-demand-checks/evidence/capability-contract.json **Reference**: MR-7 conditional rating contract. **Last Updated**: 2026-09-20

Inputs:
    - count_in: count_in parameter
    - active_in: active_in parameter
    - total_MW_in: total_MW_in parameter

Outputs:
    - demand: demand result

SysML Source: root-0/analyses/mfe_viability.sysml:99

SysML Source: root-0/analyses/mfe_viability.sysml:99

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_viability/salt_machine_electric_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_nb3sn_tea.primitives import Float


class Salt_Machine_ElectricInput(BaseModel):
    """Input model for Salt_Machine_ElectricModule.

    Attributes:
        count_in: count_in input
        active_in: active_in input
        total_MW_in: total_MW_in input
    """
    count_in: float = Field(..., description="count_in input")
    active_in: bool = Field(..., description="active_in input")
    total_MW_in: float = Field(..., description="total_MW_in input")


class Salt_Machine_ElectricModule(ModuleBase[Salt_Machine_ElectricInput, Float]):
    """TEAx module for Salt_Machine_Electric calculation.

Per-machine demand MW = total MW / machine count; inactive short circuits before division. Finite active arithmetic is guarded. **Source**: work/active/WI-080_supplied-thermal-equipment-capability-and-demand-checks/evidence/capability-contract.json **Reference**: MR-7 conditional rating contract. **Last Updated**: 2026-09-20

Inputs:
    - count_in: count_in parameter
    - active_in: active_in parameter
    - total_MW_in: total_MW_in parameter

Outputs:
    - demand: demand result

SysML Source: root-0/analyses/mfe_viability.sysml:99

    SysML Source: root-0/analyses/mfe_viability.sysml:99

    Calculation Specification:
        See documentation:
Per-machine demand MW = total MW / machine count; inactive short circuits before division. Finite active arithmetic is guarded. **Source**: work/active/WI-080_supplied-thermal-equipment-capability-and-demand-checks/evidence/capability-contract.json **Reference**: MR-7 conditional rating contract. **Last Updated**: 2026-09-20

    IMPLEMENTATION: See stellarator_materials_nb3sn_tea.handwritten.mfe_viability.salt_machine_electric_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "Salt_Machine_ElectricModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, count_in: float, active_in: bool, total_MW_in: float    ) -> Salt_Machine_ElectricInput:
        """Validate inputs and fill defaults.

        Args:
            count_in: count_in input
            active_in: active_in input
            total_MW_in: total_MW_in input

        Returns:
            Validated input model
        """
        return Salt_Machine_ElectricInput(count_in=count_in, active_in=active_in, total_MW_in=total_MW_in)

    def run(
        self, count_in: float, active_in: bool, total_MW_in: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            count_in: count_in input
            active_in: active_in input
            total_MW_in: total_MW_in input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(count_in, active_in, total_MW_in)

        # Import handwritten implementation
        from stellarator_materials_nb3sn_tea.handwritten.mfe_viability.salt_machine_electric_impl import (
            run_salt_machine_electric,
        )

        # Execute implementation - returns single value
        demand = run_salt_machine_electric(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(demand))
