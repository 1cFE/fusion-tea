"""Auto-generated implementation for Material_Winding_Cost.

AUTO_IMPLEMENTED = True

SysML Source: root-0/analyses/magnet_material_variants.sysml:20

SysML Expressions:
    superconductor_cost_in = 0.0
    materials_cost_in = 0.0
    helium_cost_in = 0.0
    winding_operations_cost_in = 0.0
    cost = superconductor_cost_in + materials_cost_in + helium_cost_in + winding_operations_cost_in
    
Documentation:
One winding account on one basis: cost = superconductor_cost_in + materials_cost_in + helium_cost_in + winding_operations_cost_in (plant dollars; the conductor and construction materials from Round 1's inventory, the helium and the winding operations from the plant's own accounts). Nothing from Round 1's annualization is added. **Source**: work/active/WI-100_stellarator-material-variants/design.md **Reference**: section 2.4; contract section 6 (notes N3, N4). **Basis**: [AGENT] reviewed design. **Last Updated**: 2026-09-30
"""

AUTO_IMPLEMENTED = True

from stellarator_materials_rebco_tea.modules.magnet_material_variants.material_winding_cost import Material_Winding_CostInput


def run_material_winding_cost(inputs: Material_Winding_CostInput) -> float:
    """Execute Material_Winding_Cost calculation.

One winding account on one basis: cost = superconductor_cost_in + materials_cost_in + helium_cost_in + winding_operations_cost_in (plant dollars; the conductor and construction materials from Round 1's inventory, the helium and the winding operations from the plant's own accounts). Nothing from Round 1's annualization is added. **Source**: work/active/WI-100_stellarator-material-variants/design.md **Reference**: section 2.4; contract section 6 (notes N3, N4). **Basis**: [AGENT] reviewed design. **Last Updated**: 2026-09-30

SysML Source: root-0/analyses/magnet_material_variants.sysml:20

SysML Expressions:
    superconductor_cost_in = 0.0
    materials_cost_in = 0.0
    helium_cost_in = 0.0
    winding_operations_cost_in = 0.0
    cost = superconductor_cost_in + materials_cost_in + helium_cost_in + winding_operations_cost_in
    
Documentation:
One winding account on one basis: cost = superconductor_cost_in + materials_cost_in + helium_cost_in + winding_operations_cost_in (plant dollars; the conductor and construction materials from Round 1's inventory, the helium and the winding operations from the plant's own accounts). Nothing from Round 1's annualization is added. **Source**: work/active/WI-100_stellarator-material-variants/design.md **Reference**: section 2.4; contract section 6 (notes N3, N4). **Basis**: [AGENT] reviewed design. **Last Updated**: 2026-09-30

Args:
    inputs: Input parameters validated against Material_Winding_CostInput schema

Returns:
    float: cost

Example:
    >>> inputs = Material_Winding_CostInput(...)
    >>> result = run_material_winding_cost(inputs)
    """
    return (((inputs.superconductor_cost_in + inputs.materials_cost_in) + inputs.helium_cost_in) + inputs.winding_operations_cost_in)
