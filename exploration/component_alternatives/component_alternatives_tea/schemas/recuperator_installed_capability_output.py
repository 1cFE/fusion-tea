from pydantic import Field
from simkit.config.schema import MultiOutput

class Recuperator_Installed_CapabilityOutput(MultiOutput):
    """Multi-output container for Recuperator_Installed_Capability.

*Source**: work/active/WI-096_matched-conversion-subsystems/design.md. **Reference**: reviewed fourth submission, sections 2-8. **Basis**: [AGENT] conditional component offer and explicitly reviewed equations; hydraulic, price and loss-sink qualification remain unverified. **Last Updated**: 2026-09-26. Numerical semantics are the complete calculate function in exploration/component_alternatives/bodies/component_alternatives_thermal/recuperator_installed_capability_impl.py; units MW, K/degC, kg/s, Pa, MW/K, USD2025 and years as named.

SysML Source: root-0/component_alternatives_thermal.sysml:115
    """
    capacity_rate: float = Field(description="capacity_rate output")
    effectiveness: float = Field(description="effectiveness output")
