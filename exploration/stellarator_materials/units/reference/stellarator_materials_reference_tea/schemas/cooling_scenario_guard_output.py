from pydantic import Field
from simkit.config.schema import MultiOutput

class Cooling_Scenario_GuardOutput(MultiOutput):
    """Multi-output container for Cooling_Scenario_Guard.

Validate supported scenario choices before using zero dormant outputs.
Both modes must be finite and exactly zero or one. If either mode is one,
equipment_enabled_in must be true; otherwise raise ValueError. Return the
validated cost_mode_in and energy_mode_in unchanged. False/zero/zero is the
generic dormant scenario. Manual completion supplies the explicit guards.
Source: work/active/WI-067_installed-cooling-equipment-costs/combined-design.md
Ref: Implementation review control-domain correction; Basis: scenario validity.

SysML Source: root-0/analyses/mfe_cooling_accounts.sysml:4
    """
    energy_mode: float = Field(description="energy_mode output")
    cost_mode: float = Field(description="cost_mode output")
