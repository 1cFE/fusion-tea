from pydantic import Field
from simkit.config.schema import MultiOutput

class Conversion_Subsystem_LedgerOutput(MultiOutput):
    """Multi-output container for Conversion_Subsystem_Ledger.

*Source**: work/active/WI-096_matched-conversion-subsystems/design.md. **Reference**: reviewed fourth submission, sections 2-8. **Basis**: [AGENT] conditional component offer and explicitly reviewed equations; hydraulic, price and loss-sink qualification remain unverified. **Last Updated**: 2026-09-26. Numerical semantics are the complete calculate function in exploration/component_alternatives/bodies/component_alternatives_thermal/conversion_subsystem_ledger_impl.py; units MW, K/degC, kg/s, Pa, MW/K, USD2025 and years as named.

SysML Source: root-0/component_alternatives_thermal.sysml:3
    """
    annual_energy: float = Field(description="annual_energy output")
    cost_per_net_MWh: float = Field(description="cost_per_net_MWh output")
    capital_10: float = Field(description="capital_10 output")
    gross_electric: float = Field(description="gross_electric output")
    conversion_energy_residual: float = Field(description="conversion_energy_residual output")
    energy_residual: float = Field(description="energy_residual output")
    replacement_pv: float = Field(description="replacement_pv output")
    capital_3: float = Field(description="capital_3 output")
    economic_defined: float = Field(description="economic_defined output")
    electrical_load: float = Field(description="electrical_load output")
    accounted_pv: float = Field(description="accounted_pv output")
    capital_4: float = Field(description="capital_4 output")
    capital_1: float = Field(description="capital_1 output")
    annual_service: float = Field(description="annual_service output")
    total_rejected: float = Field(description="total_rejected output")
    recurring_base: float = Field(description="recurring_base output")
    unremoved_heat: float = Field(description="unremoved_heat output")
    capital_9: float = Field(description="capital_9 output")
    corrected_pv: float = Field(description="corrected_pv output")
    machine_replacement_pv: float = Field(description="machine_replacement_pv output")
    capital_7: float = Field(description="capital_7 output")
    net_electric: float = Field(description="net_electric output")
    annuity_factor: float = Field(description="annuity_factor output")
    capital_2: float = Field(description="capital_2 output")
    conversion_energy_residual_magnitude: float = Field(description="conversion_energy_residual_magnitude output")
    capital_6: float = Field(description="capital_6 output")
    annual_makeup: float = Field(description="annual_makeup output")
    bundle_replacement_pv: float = Field(description="bundle_replacement_pv output")
    conversion_replacement_pv: float = Field(description="conversion_replacement_pv output")
    capital_5: float = Field(description="capital_5 output")
    capital_8: float = Field(description="capital_8 output")
    energy_tolerance: float = Field(description="energy_tolerance output")
    discounted_energy: float = Field(description="discounted_energy output")
    capital_total: float = Field(description="capital_total output")
