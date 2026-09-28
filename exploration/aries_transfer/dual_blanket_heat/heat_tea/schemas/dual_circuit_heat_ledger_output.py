from pydantic import Field
from simkit.config.schema import MultiOutput

class Dual_Circuit_Heat_LedgerOutput(MultiOutput):
    """Multi-output container for Dual_Circuit_Heat_Ledger.

delivered_total = duty_1_in + duty_2_in; deposited_total = deposition_1_in + deposition_2_in; friction_total = friction_1_in + friction_2_in; energy_residual = delivered_total - deposited_total - friction_total. All quantities MW. Source: work/active/WI-086_aries-dual-blanket-heat-accounting/spec.md. Ref: two-branch control boundary with internal exchange canceling once. Basis: generic energy accounting; native completion rejects nonfinite/negative supplied heat and nonfinite outputs, but preserves signed residuals without clamping or forcing closure. A nonzero residual is a diagnostic, not an equipment adequacy claim. Independent source comparison belongs in the analysis record, not this physical producer. Last Updated: 2026-09-21.

SysML Source: root-0/dual_circuit_heat_accounting.sysml:13
    """
    friction_total: float = Field(description="friction_total output")
    deposited_total: float = Field(description="deposited_total output")
    delivered_total: float = Field(description="delivered_total output")
    energy_residual: float = Field(description="energy_residual output")
