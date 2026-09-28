from pydantic import Field
from simkit.config.schema import MultiOutput

class Supplied_Source_BasisOutput(MultiOutput):
    """Multi-output container for Supplied_Source_Basis.

*Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Complete normative numerical semantics: exploration/whole_plant_conversion/bodies/whole_plant_conversion_accounts/supplied_source_basis_impl.py; reviewed equations in design/configuration.

SysML Source: root-0/whole_plant_conversion_accounts.sysml:141
    """
    heating_loss_MW: float = Field(description="heating_loss_MW output")
    heating_wall_margin: float = Field(description="heating_wall_margin output")
    domain_supported: float = Field(description="domain_supported output")
    divertor_load: float = Field(description="divertor_load output")
    heating_coupled_margin: float = Field(description="heating_coupled_margin output")
    source_qualified: float = Field(description="source_qualified output")
    fusion_envelope_margin: float = Field(description="fusion_envelope_margin output")
    divertor_margin: float = Field(description="divertor_margin output")
    wall_load: float = Field(description="wall_load output")
    reconstructed_source_MW: float = Field(description="reconstructed_source_MW output")
    fusion_MW: float = Field(description="fusion_MW output")
    heating_wall_MW: float = Field(description="heating_wall_MW output")
    source_residual: float = Field(description="source_residual output")
