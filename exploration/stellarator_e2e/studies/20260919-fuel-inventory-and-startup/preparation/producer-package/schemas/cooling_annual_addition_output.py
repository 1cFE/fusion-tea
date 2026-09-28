from pydantic import Field
from simkit.config.schema import MultiOutput

class Cooling_Annual_AdditionOutput(MultiOutput):
    """Multi-output container for Cooling_Annual_Addition.

Add new cooling annual expenses to their distinct existing owners.
Routine service labor remains in inherited O&M; cooling consumable make-up
enters before the existing annual-cost levelization. Dated cooling major
replacements are already annualized and enter CAS72 after that calculation.
Source: work/active/WI-067_installed-cooling-equipment-costs/combined-design.md
Ref: Lifecycle; models/library/analyses/mfe_lifecycle.sysml (annualized replacement convention)
Basis: sum each annual expense once before its existing consumer.

SysML Source: root-0/analyses/mfe_cooling_accounts.sysml:57
    """
    cas72_total: float = Field(description="cas72_total output")
    annual_om: float = Field(description="annual_om output")
