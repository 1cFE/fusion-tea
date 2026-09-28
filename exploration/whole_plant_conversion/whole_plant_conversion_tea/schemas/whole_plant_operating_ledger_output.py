from pydantic import Field
from simkit.config.schema import MultiOutput

class Whole_Plant_Operating_LedgerOutput(MultiOutput):
    """Multi-output container for Whole_Plant_Operating_Ledger.

*Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Complete normative numerical semantics: exploration/whole_plant_conversion/bodies/whole_plant_conversion_accounts/whole_plant_operating_ledger_impl.py; reviewed equations in design/configuration.

SysML Source: root-0/whole_plant_conversion_accounts.sysml:321
    """
    auxiliary_margin_MW: float = Field(description="auxiliary_margin_MW output")
    annual_net_grid_MWh: float = Field(description="annual_net_grid_MWh output")
    domain_supported: float = Field(description="domain_supported output")
    annual_import_MWh: float = Field(description="annual_import_MWh output")
    power_residual: float = Field(description="power_residual output")
    annual_export_MWh: float = Field(description="annual_export_MWh output")
    annual_import_cost: float = Field(description="annual_import_cost output")
    net_export_MW: float = Field(description="net_export_MW output")
    standby_MW: float = Field(description="standby_MW output")
    primary_motor_loss_MW: float = Field(description="primary_motor_loss_MW output")
    upstream_electric_MW: float = Field(description="upstream_electric_MW output")
    auxiliary_heat_MW: float = Field(description="auxiliary_heat_MW output")
