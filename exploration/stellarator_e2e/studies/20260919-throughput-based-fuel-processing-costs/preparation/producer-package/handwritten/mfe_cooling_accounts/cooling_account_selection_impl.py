"""Auto-generated implementation for Cooling_Account_Selection.

AUTO_IMPLEMENTED = True

SysML Source: root-0/analyses/mfe_cooling_accounts.sysml:19

SysML Expressions:
    cost = (1.0 - cost_mode_in) * legacy_cost_in + cost_mode_in * equipment_cost_in
    shipping_exclusion = cost_mode_in * delivered_in
    replacement_annual = cost_mode_in * replacements_in
    consumables_annual = cost_mode_in * consumables_in
    
Documentation:
Select independently sized cooling accounts or the retained legacy
allowance. Cost mode and secondary energy mode are binary scenario inputs
(0 or 1), not continuous blending controls. Each energy selector applies
to both electricity and recovered shaft heat. Primary IHX duty remains
upstream of secondary work, avoiding a feedback edge. New equipment
amounts are plant-total for the supported single-module scenario.
Source: work/active/WI-067_installed-cooling-equipment-costs/combined-design.md
Ref: Account boundaries; Intermediate equipment and energy; Corrective review details
Basis: explicit accounting identities, independent of equipment price models.
"""

AUTO_IMPLEMENTED = True

from stellarator_tea.modules.mfe_cooling_accounts.cooling_account_selection import Cooling_Account_SelectionInput


def run_cooling_account_selection(inputs: Cooling_Account_SelectionInput) -> tuple[float, float, float, float]:
    """Execute Cooling_Account_Selection calculation.

Select independently sized cooling accounts or the retained legacy
allowance. Cost mode and secondary energy mode are binary scenario inputs
(0 or 1), not continuous blending controls. Each energy selector applies
to both electricity and recovered shaft heat. Primary IHX duty remains
upstream of secondary work, avoiding a feedback edge. New equipment
amounts are plant-total for the supported single-module scenario.
Source: work/active/WI-067_installed-cooling-equipment-costs/combined-design.md
Ref: Account boundaries; Intermediate equipment and energy; Corrective review details
Basis: explicit accounting identities, independent of equipment price models.

SysML Source: root-0/analyses/mfe_cooling_accounts.sysml:19

SysML Expressions:
    cost = (1.0 - cost_mode_in) * legacy_cost_in + cost_mode_in * equipment_cost_in
    shipping_exclusion = cost_mode_in * delivered_in
    replacement_annual = cost_mode_in * replacements_in
    consumables_annual = cost_mode_in * consumables_in
    
Documentation:
Select independently sized cooling accounts or the retained legacy
allowance. Cost mode and secondary energy mode are binary scenario inputs
(0 or 1), not continuous blending controls. Each energy selector applies
to both electricity and recovered shaft heat. Primary IHX duty remains
upstream of secondary work, avoiding a feedback edge. New equipment
amounts are plant-total for the supported single-module scenario.
Source: work/active/WI-067_installed-cooling-equipment-costs/combined-design.md
Ref: Account boundaries; Intermediate equipment and energy; Corrective review details
Basis: explicit accounting identities, independent of equipment price models.

Args:
    inputs: Input parameters validated against Cooling_Account_SelectionInput schema

Returns:
    tuple[float, ...]: (cost, shipping_exclusion, consumables_annual, replacement_annual)

Example:
    >>> inputs = Cooling_Account_SelectionInput(...)
    >>> cost, shipping_exclusion, consumables_annual, replacement_annual = run_cooling_account_selection(inputs)
    """
    return (
        (((1.0 - inputs.cost_mode_in) * inputs.legacy_cost_in) + (inputs.cost_mode_in * inputs.equipment_cost_in)),  # cost
        (inputs.cost_mode_in * inputs.delivered_in),  # shipping_exclusion
        (inputs.cost_mode_in * inputs.consumables_in),  # consumables_annual
        (inputs.cost_mode_in * inputs.replacements_in),  # replacement_annual
    )
