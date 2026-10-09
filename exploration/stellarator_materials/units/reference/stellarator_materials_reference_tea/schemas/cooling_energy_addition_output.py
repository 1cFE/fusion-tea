from pydantic import Field
from simkit.config.schema import MultiOutput

class Cooling_Energy_AdditionOutput(MultiOutput):
    """Multi-output container for Cooling_Energy_Addition.

Add intermediate pump electricity and recovered shaft work together.
This producer has no cost inputs: the legacy cost reads plant net power,
so combining its inputs with this producer would create a dependency cycle.
Source: work/active/WI-067_installed-cooling-equipment-costs/combined-design.md
Ref: Corrective review details; Basis: separate acyclic energy ownership.

SysML Source: root-0/analyses/mfe_cooling_accounts.sysml:42
    """
    electric_total: float = Field(description="electric_total output")
    recovered_total: float = Field(description="recovered_total output")
