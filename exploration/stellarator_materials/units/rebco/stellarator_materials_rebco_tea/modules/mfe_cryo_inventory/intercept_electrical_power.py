"""Intercept_Electrical_PowerModule Module Wrapper

TEAx module for Intercept_Electrical_Power calculation.

Warm refrigerator MW=q_shield*1e-6*(T_amb-T_shield)/(f_carnot*T_shield).
Disabled inventory returns zero before arithmetic; active temperatures
and Carnot domain are enforced by native manual completion.
*Source**: work/active/WI-059_coil-thermal-and-total-support-inventory/design.md **Reference**: D4-D5.
*Basis**: fraction-of-Carnot refrigerator. **Last Updated**: 2026-09-15

Inputs:
    - T_amb: T_amb parameter
    - f_carnot: f_carnot parameter
    - inventory_enabled: inventory_enabled parameter
    - q_shield: q_shield parameter
    - T_shield: T_shield parameter

Outputs:
    - p_elec: p_elec result

SysML Source: root-0/analyses/mfe_cryo_inventory.sysml:89

SysML Source: root-0/analyses/mfe_cryo_inventory.sysml:89

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_cryo_inventory/intercept_electrical_power_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_rebco_tea.primitives import Float


class Intercept_Electrical_PowerInput(BaseModel):
    """Input model for Intercept_Electrical_PowerModule.

    Attributes:
        T_amb: T_amb input
        f_carnot: f_carnot input
        inventory_enabled: inventory_enabled input
        q_shield: q_shield input
        T_shield: T_shield input
    """
    T_amb: float = Field(..., description="T_amb input")
    f_carnot: float = Field(..., description="f_carnot input")
    inventory_enabled: bool = Field(..., description="inventory_enabled input")
    q_shield: float = Field(..., description="q_shield input")
    T_shield: float = Field(..., description="T_shield input")


class Intercept_Electrical_PowerModule(ModuleBase[Intercept_Electrical_PowerInput, Float]):
    """TEAx module for Intercept_Electrical_Power calculation.

Warm refrigerator MW=q_shield*1e-6*(T_amb-T_shield)/(f_carnot*T_shield).
Disabled inventory returns zero before arithmetic; active temperatures
and Carnot domain are enforced by native manual completion.
*Source**: work/active/WI-059_coil-thermal-and-total-support-inventory/design.md **Reference**: D4-D5.
*Basis**: fraction-of-Carnot refrigerator. **Last Updated**: 2026-09-15

Inputs:
    - T_amb: T_amb parameter
    - f_carnot: f_carnot parameter
    - inventory_enabled: inventory_enabled parameter
    - q_shield: q_shield parameter
    - T_shield: T_shield parameter

Outputs:
    - p_elec: p_elec result

SysML Source: root-0/analyses/mfe_cryo_inventory.sysml:89

    SysML Source: root-0/analyses/mfe_cryo_inventory.sysml:89

    Calculation Specification:
        inventory_enabled = false
        q_shield = 0.0
        T_shield = 77.0
        T_amb = 300.0
        f_carnot = 1.0
        
Documentation:
Warm refrigerator MW=q_shield*1e-6*(T_amb-T_shield)/(f_carnot*T_shield).
Disabled inventory returns zero before arithmetic; active temperatures
and Carnot domain are enforced by native manual completion.
*Source**: work/active/WI-059_coil-thermal-and-total-support-inventory/design.md **Reference**: D4-D5.
*Basis**: fraction-of-Carnot refrigerator. **Last Updated**: 2026-09-15

    IMPLEMENTATION: See stellarator_materials_rebco_tea.handwritten.mfe_cryo_inventory.intercept_electrical_power_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "Intercept_Electrical_PowerModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, T_amb: float, f_carnot: float, inventory_enabled: bool, q_shield: float, T_shield: float    ) -> Intercept_Electrical_PowerInput:
        """Validate inputs and fill defaults.

        Args:
            T_amb: T_amb input
            f_carnot: f_carnot input
            inventory_enabled: inventory_enabled input
            q_shield: q_shield input
            T_shield: T_shield input

        Returns:
            Validated input model
        """
        return Intercept_Electrical_PowerInput(T_amb=T_amb, f_carnot=f_carnot, inventory_enabled=inventory_enabled, q_shield=q_shield, T_shield=T_shield)

    def run(
        self, T_amb: float, f_carnot: float, inventory_enabled: bool, q_shield: float, T_shield: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            T_amb: T_amb input
            f_carnot: f_carnot input
            inventory_enabled: inventory_enabled input
            q_shield: q_shield input
            T_shield: T_shield input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(T_amb, f_carnot, inventory_enabled, q_shield, T_shield)

        # Import handwritten implementation
        from stellarator_materials_rebco_tea.handwritten.mfe_cryo_inventory.intercept_electrical_power_impl import (
            run_intercept_electrical_power,
        )

        # Execute implementation - returns single value
        p_elec = run_intercept_electrical_power(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(p_elec))
