from pydantic import Field
from simkit.config.schema import MultiOutput

class Actual_Exchanger_ApproachesOutput(MultiOutput):
    """Multi-output container for Actual_Exchanger_Approaches.

*Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Complete normative numerical semantics: exploration/whole_plant_conversion/bodies/whole_plant_conversion_accounts/actual_exchanger_approaches_impl.py; reviewed equations in design/configuration.

SysML Source: root-0/whole_plant_conversion_accounts.sysml:5
    """
    cold_gap: float = Field(description="cold_gap output")
    hot_gap: float = Field(description="hot_gap output")
