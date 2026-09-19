"""Auto-generated implementation for Cooling_Energy_Addition.

AUTO_IMPLEMENTED = True

SysML Source: root-0/analyses/mfe_cooling_accounts.sysml:42

SysML Expressions:
    electric_total = primary_electric_in + secondary_mode_in * salt_electric_in
    recovered_total = primary_recovered_in + secondary_mode_in * salt_shaft_in
    
Documentation:
Add intermediate pump electricity and recovered shaft work together.
This producer has no cost inputs: the legacy cost reads plant net power,
so combining its inputs with this producer would create a dependency cycle.
Source: work/active/WI-067_installed-cooling-equipment-costs/combined-design.md
Ref: Corrective review details; Basis: separate acyclic energy ownership.
"""

AUTO_IMPLEMENTED = True

from stellarator_tea.modules.mfe_cooling_accounts.cooling_energy_addition import Cooling_Energy_AdditionInput


def run_cooling_energy_addition(inputs: Cooling_Energy_AdditionInput) -> tuple[float, float]:
    """Execute Cooling_Energy_Addition calculation.

Add intermediate pump electricity and recovered shaft work together.
This producer has no cost inputs: the legacy cost reads plant net power,
so combining its inputs with this producer would create a dependency cycle.
Source: work/active/WI-067_installed-cooling-equipment-costs/combined-design.md
Ref: Corrective review details; Basis: separate acyclic energy ownership.

SysML Source: root-0/analyses/mfe_cooling_accounts.sysml:42

SysML Expressions:
    electric_total = primary_electric_in + secondary_mode_in * salt_electric_in
    recovered_total = primary_recovered_in + secondary_mode_in * salt_shaft_in
    
Documentation:
Add intermediate pump electricity and recovered shaft work together.
This producer has no cost inputs: the legacy cost reads plant net power,
so combining its inputs with this producer would create a dependency cycle.
Source: work/active/WI-067_installed-cooling-equipment-costs/combined-design.md
Ref: Corrective review details; Basis: separate acyclic energy ownership.

Args:
    inputs: Input parameters validated against Cooling_Energy_AdditionInput schema

Returns:
    tuple[float, ...]: (electric_total, recovered_total)

Example:
    >>> inputs = Cooling_Energy_AdditionInput(...)
    >>> electric_total, recovered_total = run_cooling_energy_addition(inputs)
    """
    return (
        (inputs.primary_electric_in + (inputs.secondary_mode_in * inputs.salt_electric_in)),  # electric_total
        (inputs.primary_recovered_in + (inputs.secondary_mode_in * inputs.salt_shaft_in)),  # recovered_total
    )
