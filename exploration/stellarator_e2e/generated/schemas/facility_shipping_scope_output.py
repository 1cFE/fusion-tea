from pydantic import Field
from simkit.config.schema import MultiOutput

class Facility_Shipping_ScopeOutput(MultiOutput):
    """Multi-output container for Facility_Shipping_Scope.

Source: work/active/WI-068_layout-based-facilities/design.md; layout-capacity-design.md; evidence/facility-contract.md. Ref: released geometry, capacity, exact civil takeoff and account boundary. Basis: conditional conceptual scenario; unqualified shielding/loading/transport and explicit provisional equipment envelopes. Reject negative/nonfinite exclusions or sum exceedingCAS20, never clamp.

SysML Source: root-0/analyses/mfe_facilities.sysml:690
    """
    facility_exclusion: float = Field(description="facility_exclusion output")
    cooling_exclusion: float = Field(description="cooling_exclusion output")
    fuel_installation_exclusion: float = Field(description="fuel_installation_exclusion output")
    remaining_shipping_base: float = Field(description="remaining_shipping_base output")
