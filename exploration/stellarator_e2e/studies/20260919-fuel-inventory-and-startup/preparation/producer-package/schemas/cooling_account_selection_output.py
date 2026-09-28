from pydantic import Field
from simkit.config.schema import MultiOutput

class Cooling_Account_SelectionOutput(MultiOutput):
    """Multi-output container for Cooling_Account_Selection.

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
    """
    cost: float = Field(description="cost output")
    shipping_exclusion: float = Field(description="shipping_exclusion output")
    consumables_annual: float = Field(description="consumables_annual output")
    replacement_annual: float = Field(description="replacement_annual output")
