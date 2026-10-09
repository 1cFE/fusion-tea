"""Auto-generated implementation for special_materials_capital.

AUTO_IMPLEMENTED = True

SysML Source: root-0/designs/stellarator_09_materials/nb3sn_material.sysml:2129

SysML Expressions:
"""

AUTO_IMPLEMENTED = True

from stellarator_materials_nb3sn_tea.modules.stellarator_09_materials.nb3sn_material.special_materials_capital import special_materials_capitalInput


def run_special_materials_capital(inputs: special_materials_capitalInput) -> float:
    """Execute special_materials_capital calculation.

SysML Source: root-0/designs/stellarator_09_materials/nb3sn_material.sysml:2129

Args:
    inputs: Input parameters validated against special_materials_capitalInput schema

Returns:
    float: special_materials_capital

Example:
    >>> inputs = special_materials_capitalInput(...)
    >>> result = run_special_materials_capital(inputs)
    """
    return (((inputs.blanket_vol * 0.5) * 9400.0) * 5.0)
