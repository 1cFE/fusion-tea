"""Auto-generated implementation for Cooling_Annual_Addition.

AUTO_IMPLEMENTED = True

SysML Source: root-0/analyses/mfe_cooling_accounts.sysml:57

SysML Expressions:
    annual_om = existing_om_in + cooling_consumables_in
    cas72_total = existing_replacements_in + cooling_replacements_in
    
Documentation:
Add new cooling annual expenses to their distinct existing owners.
Routine service labor remains in inherited O&M; cooling consumable make-up
enters before the existing annual-cost levelization. Dated cooling major
replacements are already annualized and enter CAS72 after that calculation.
Source: work/active/WI-067_installed-cooling-equipment-costs/combined-design.md
Ref: Lifecycle; models/library/analyses/mfe_lifecycle.sysml (annualized replacement convention)
Basis: sum each annual expense once before its existing consumer.
"""

AUTO_IMPLEMENTED = True

from stellarator_tea.modules.mfe_cooling_accounts.cooling_annual_addition import Cooling_Annual_AdditionInput


def run_cooling_annual_addition(inputs: Cooling_Annual_AdditionInput) -> tuple[float, float]:
    """Execute Cooling_Annual_Addition calculation.

Add new cooling annual expenses to their distinct existing owners.
Routine service labor remains in inherited O&M; cooling consumable make-up
enters before the existing annual-cost levelization. Dated cooling major
replacements are already annualized and enter CAS72 after that calculation.
Source: work/active/WI-067_installed-cooling-equipment-costs/combined-design.md
Ref: Lifecycle; models/library/analyses/mfe_lifecycle.sysml (annualized replacement convention)
Basis: sum each annual expense once before its existing consumer.

SysML Source: root-0/analyses/mfe_cooling_accounts.sysml:57

SysML Expressions:
    annual_om = existing_om_in + cooling_consumables_in
    cas72_total = existing_replacements_in + cooling_replacements_in
    
Documentation:
Add new cooling annual expenses to their distinct existing owners.
Routine service labor remains in inherited O&M; cooling consumable make-up
enters before the existing annual-cost levelization. Dated cooling major
replacements are already annualized and enter CAS72 after that calculation.
Source: work/active/WI-067_installed-cooling-equipment-costs/combined-design.md
Ref: Lifecycle; models/library/analyses/mfe_lifecycle.sysml (annualized replacement convention)
Basis: sum each annual expense once before its existing consumer.

Args:
    inputs: Input parameters validated against Cooling_Annual_AdditionInput schema

Returns:
    tuple[float, ...]: (cas72_total, annual_om)

Example:
    >>> inputs = Cooling_Annual_AdditionInput(...)
    >>> cas72_total, annual_om = run_cooling_annual_addition(inputs)
    """
    return (
        (inputs.existing_replacements_in + inputs.cooling_replacements_in),  # cas72_total
        (inputs.existing_om_in + inputs.cooling_consumables_in),  # annual_om
    )
