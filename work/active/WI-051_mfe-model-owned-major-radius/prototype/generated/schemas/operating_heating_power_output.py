from pydantic import Field
from simkit.config.schema import MultiOutput

class Operating_Heating_PowerOutput(MultiOutput):
    """Multi-output container for Operating_Heating_Power.

Sustained heating at held two-stage efficiency. Signed demand remains diagnostic outside burn hold; no clipping at zero or capacity. All powers MW, efficiencies dimensionless. **Source**: models/library/analyses/mfe_heating_chain.sysml **Ref**: Heating Power Chain two-stage identities; work/active/WI-050_mfe-coherent-operating-heating/spec.md MR-WI050-1/2 **Basis**: algebraic inverse at constant efficiencies, supported domain 0 < efficiency <= 1 **Last Updated**: 2026-09-11

SysML Source: root-0/analyses/mfe_heating_chain.sysml:79
    """
    p_wallplug: float = Field(description="p_wallplug output")
    p_coupled: float = Field(description="p_coupled output")
    p_delivered: float = Field(description="p_delivered output")
