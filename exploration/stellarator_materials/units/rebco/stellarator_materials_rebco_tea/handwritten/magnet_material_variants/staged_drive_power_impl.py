"""Auto-generated implementation for Staged_Drive_Power.

AUTO_IMPLEMENTED = True

SysML Source: root-0/analyses/magnet_material_variants.sysml:80

SysML Expressions:
    q_leads_in = 0.0
    q_shield_in = 0.0
    shield_static_in = 0.0
    q_joints_in = 0.0
    joint_drive_fraction_in = 0.0
    p_drive = (q_leads_in + (q_shield_in - shield_static_in) + joint_drive_fraction_in * q_joints_in) * 1e-06
    
Documentation:
Lead and joint drive power of the staged cold load, in MW: p_drive = (q_leads_in + (q_shield_in - shield_static_in) + joint_drive_fraction_in * q_joints_in) * 1e-6, with the cold-segment lead heat, the warm-segment lead heat (the intercept load less its static part) and the joint losses in W. It is the plant's drive definition on the staged loads and reproduces the pinned 0.0502673 MW at 20 K. **Source**: models/library/analyses/mfe_cryo_inventory.sysml **Reference**: 'Coil Thermal Inventory' p_drive, line 17; WI-100 design section 2.4. **Basis**: [AGENT] reviewed design. **Last Updated**: 2026-09-30
"""

AUTO_IMPLEMENTED = True

from stellarator_materials_rebco_tea.modules.magnet_material_variants.staged_drive_power import Staged_Drive_PowerInput


def run_staged_drive_power(inputs: Staged_Drive_PowerInput) -> float:
    """Execute Staged_Drive_Power calculation.

Lead and joint drive power of the staged cold load, in MW: p_drive = (q_leads_in + (q_shield_in - shield_static_in) + joint_drive_fraction_in * q_joints_in) * 1e-6, with the cold-segment lead heat, the warm-segment lead heat (the intercept load less its static part) and the joint losses in W. It is the plant's drive definition on the staged loads and reproduces the pinned 0.0502673 MW at 20 K. **Source**: models/library/analyses/mfe_cryo_inventory.sysml **Reference**: 'Coil Thermal Inventory' p_drive, line 17; WI-100 design section 2.4. **Basis**: [AGENT] reviewed design. **Last Updated**: 2026-09-30

SysML Source: root-0/analyses/magnet_material_variants.sysml:80

SysML Expressions:
    q_leads_in = 0.0
    q_shield_in = 0.0
    shield_static_in = 0.0
    q_joints_in = 0.0
    joint_drive_fraction_in = 0.0
    p_drive = (q_leads_in + (q_shield_in - shield_static_in) + joint_drive_fraction_in * q_joints_in) * 1e-06
    
Documentation:
Lead and joint drive power of the staged cold load, in MW: p_drive = (q_leads_in + (q_shield_in - shield_static_in) + joint_drive_fraction_in * q_joints_in) * 1e-6, with the cold-segment lead heat, the warm-segment lead heat (the intercept load less its static part) and the joint losses in W. It is the plant's drive definition on the staged loads and reproduces the pinned 0.0502673 MW at 20 K. **Source**: models/library/analyses/mfe_cryo_inventory.sysml **Reference**: 'Coil Thermal Inventory' p_drive, line 17; WI-100 design section 2.4. **Basis**: [AGENT] reviewed design. **Last Updated**: 2026-09-30

Args:
    inputs: Input parameters validated against Staged_Drive_PowerInput schema

Returns:
    float: p_drive

Example:
    >>> inputs = Staged_Drive_PowerInput(...)
    >>> result = run_staged_drive_power(inputs)
    """
    return (((inputs.q_leads_in + (inputs.q_shield_in - inputs.shield_static_in)) + (inputs.joint_drive_fraction_in * inputs.q_joints_in)) * 1e-06)
