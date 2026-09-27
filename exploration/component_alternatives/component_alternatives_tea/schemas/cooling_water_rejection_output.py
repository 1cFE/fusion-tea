from pydantic import Field
from simkit.config.schema import MultiOutput

class Cooling_Water_RejectionOutput(MultiOutput):
    """Multi-output container for Cooling_Water_Rejection.

*Source**: work/orchestration/goals/current-model-comparison-readiness/evidence/round2/cycle-proposal-v2.md **Reference**: WI-073 design.md and interface-inventory.md; original NIST tables and independent physical review. **Basis**: [AGENT] reviewed reduced extraction/reheat cycle and conditional cooling-water scenario; equipment and installed cost unqualified. **Last Updated**: 2026-09-19 Numerical semantic: the normative handwritten implementation executes the exact state/work equations in the cited design. Disabled modes branch before property access; no extrapolation. Units are given by the scalar names and interface inventory.

SysML Source: root-0/mfe_matched_steam_cycle.sysml:105
    """
    site_qualified: bool = Field(description="site_qualified output")
    cooling_approach_ok: bool = Field(description="cooling_approach_ok output")
    q_cooling_motor_loss_MW: float = Field(description="q_cooling_motor_loss_MW output")
    water_flow_kg_s: float = Field(description="water_flow_kg_s output")
    water_energy_residual_MW: float = Field(description="water_energy_residual_MW output")
    reference_scenario: bool = Field(description="reference_scenario output")
    condenser_water_gap_K: float = Field(description="condenser_water_gap_K output")
    q_total_rejection_MW: float = Field(description="q_total_rejection_MW output")
    p_cooling_pump_electric_MW: float = Field(description="p_cooling_pump_electric_MW output")
    p_cooling_pump_shaft_MW: float = Field(description="p_cooling_pump_shaft_MW output")
    water_pump_rise_K: float = Field(description="water_pump_rise_K output")
    active: bool = Field(description="active output")
    denominator_kJ_kg: float = Field(description="denominator_kJ_kg output")
