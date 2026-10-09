"""Staged_Drive_PowerModule Module Wrapper

TEAx module for Staged_Drive_Power calculation.

Lead and joint drive power of the staged cold load, in MW: p_drive = (q_leads_in + (q_shield_in - shield_static_in) + joint_drive_fraction_in * q_joints_in) * 1e-6, with the cold-segment lead heat, the warm-segment lead heat (the intercept load less its static part) and the joint losses in W. It is the plant's drive definition on the staged loads and reproduces the pinned 0.0502673 MW at 20 K. **Source**: models/library/analyses/mfe_cryo_inventory.sysml **Reference**: 'Coil Thermal Inventory' p_drive, line 17; WI-100 design section 2.4. **Basis**: [AGENT] reviewed design. **Last Updated**: 2026-09-30

Inputs:
    - shield_static_in: shield_static_in parameter
    - q_leads_in: q_leads_in parameter
    - q_shield_in: q_shield_in parameter
    - joint_drive_fraction_in: joint_drive_fraction_in parameter
    - q_joints_in: q_joints_in parameter

Outputs:
    - p_drive: p_drive result

SysML Source: root-0/analyses/magnet_material_variants.sysml:80

SysML Source: root-0/analyses/magnet_material_variants.sysml:80

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/magnet_material_variants/staged_drive_power_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_nb3sn_tea.primitives import Float


class Staged_Drive_PowerInput(BaseModel):
    """Input model for Staged_Drive_PowerModule.

    Attributes:
        shield_static_in: shield_static_in input
        q_leads_in: q_leads_in input
        q_shield_in: q_shield_in input
        joint_drive_fraction_in: joint_drive_fraction_in input
        q_joints_in: q_joints_in input
    """
    shield_static_in: float = Field(..., description="shield_static_in input")
    q_leads_in: float = Field(..., description="q_leads_in input")
    q_shield_in: float = Field(..., description="q_shield_in input")
    joint_drive_fraction_in: float = Field(..., description="joint_drive_fraction_in input")
    q_joints_in: float = Field(..., description="q_joints_in input")


class Staged_Drive_PowerModule(ModuleBase[Staged_Drive_PowerInput, Float]):
    """TEAx module for Staged_Drive_Power calculation.

Lead and joint drive power of the staged cold load, in MW: p_drive = (q_leads_in + (q_shield_in - shield_static_in) + joint_drive_fraction_in * q_joints_in) * 1e-6, with the cold-segment lead heat, the warm-segment lead heat (the intercept load less its static part) and the joint losses in W. It is the plant's drive definition on the staged loads and reproduces the pinned 0.0502673 MW at 20 K. **Source**: models/library/analyses/mfe_cryo_inventory.sysml **Reference**: 'Coil Thermal Inventory' p_drive, line 17; WI-100 design section 2.4. **Basis**: [AGENT] reviewed design. **Last Updated**: 2026-09-30

Inputs:
    - shield_static_in: shield_static_in parameter
    - q_leads_in: q_leads_in parameter
    - q_shield_in: q_shield_in parameter
    - joint_drive_fraction_in: joint_drive_fraction_in parameter
    - q_joints_in: q_joints_in parameter

Outputs:
    - p_drive: p_drive result

SysML Source: root-0/analyses/magnet_material_variants.sysml:80

    SysML Source: root-0/analyses/magnet_material_variants.sysml:80

    Calculation Specification:
        q_leads_in = 0.0
        q_shield_in = 0.0
        shield_static_in = 0.0
        q_joints_in = 0.0
        joint_drive_fraction_in = 0.0
        p_drive = (q_leads_in + (q_shield_in - shield_static_in) + joint_drive_fraction_in * q_joints_in) * 1e-06
        
Documentation:
Lead and joint drive power of the staged cold load, in MW: p_drive = (q_leads_in + (q_shield_in - shield_static_in) + joint_drive_fraction_in * q_joints_in) * 1e-6, with the cold-segment lead heat, the warm-segment lead heat (the intercept load less its static part) and the joint losses in W. It is the plant's drive definition on the staged loads and reproduces the pinned 0.0502673 MW at 20 K. **Source**: models/library/analyses/mfe_cryo_inventory.sysml **Reference**: 'Coil Thermal Inventory' p_drive, line 17; WI-100 design section 2.4. **Basis**: [AGENT] reviewed design. **Last Updated**: 2026-09-30

    IMPLEMENTATION: See stellarator_materials_nb3sn_tea.handwritten.magnet_material_variants.staged_drive_power_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "Staged_Drive_PowerModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, shield_static_in: float, q_leads_in: float, q_shield_in: float, joint_drive_fraction_in: float, q_joints_in: float    ) -> Staged_Drive_PowerInput:
        """Validate inputs and fill defaults.

        Args:
            shield_static_in: shield_static_in input
            q_leads_in: q_leads_in input
            q_shield_in: q_shield_in input
            joint_drive_fraction_in: joint_drive_fraction_in input
            q_joints_in: q_joints_in input

        Returns:
            Validated input model
        """
        return Staged_Drive_PowerInput(shield_static_in=shield_static_in, q_leads_in=q_leads_in, q_shield_in=q_shield_in, joint_drive_fraction_in=joint_drive_fraction_in, q_joints_in=q_joints_in)

    def run(
        self, shield_static_in: float, q_leads_in: float, q_shield_in: float, joint_drive_fraction_in: float, q_joints_in: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            shield_static_in: shield_static_in input
            q_leads_in: q_leads_in input
            q_shield_in: q_shield_in input
            joint_drive_fraction_in: joint_drive_fraction_in input
            q_joints_in: q_joints_in input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(shield_static_in, q_leads_in, q_shield_in, joint_drive_fraction_in, q_joints_in)

        # Import handwritten implementation
        from stellarator_materials_nb3sn_tea.handwritten.magnet_material_variants.staged_drive_power_impl import (
            run_staged_drive_power,
        )

        # Execute implementation - returns single value
        p_drive = run_staged_drive_power(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(p_drive))
