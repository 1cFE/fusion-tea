from pydantic import Field
from simkit.config.schema import MultiOutput

class Cycle_Mode_SelectionOutput(MultiOutput):
    """Multi-output container for Cycle_Mode_Selection.

*Source**: work/orchestration/goals/current-model-comparison-readiness/evidence/round2/cycle-proposal-v2.md **Reference**: WI-073 design.md and interface-inventory.md; original NIST tables and independent physical review. **Basis**: [AGENT] reviewed reduced extraction/reheat cycle and conditional cooling-water scenario; equipment and installed cost unqualified. **Last Updated**: 2026-09-19 Numerical semantic: the normative handwritten implementation executes the exact state/work equations in the cited design. Disabled modes branch before property access; no extrapolation. Units are given by the scalar names and interface inventory.

SysML Source: root-0/analyses/mfe_matched_steam_cycle.sysml:130
    """
    matched_domain_applicable: bool = Field(description="matched_domain_applicable output")
    legacy_domain_applicable: bool = Field(description="legacy_domain_applicable output")
    eta_selected: float = Field(description="eta_selected output")
