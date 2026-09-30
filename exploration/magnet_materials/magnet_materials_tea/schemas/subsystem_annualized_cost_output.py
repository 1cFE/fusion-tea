from pydantic import Field
from simkit.config.schema import MultiOutput

class Subsystem_Annualized_CostOutput(MultiOutput):
    """Multi-output container for Subsystem_Annualized_Cost.

capital_total = winding_capital + refrigerator_capital; annual_electricity = p_in_total_MW*hours*availability*electricity_price (USD/MWh); annualized_cost = crf*capital_total + annual_electricity. **Source**: work/active/WI-099_magnet-conductor-alternatives/design.md **Reference**: section 2.7; contract section 7. **Basis**: [AGENT] capital recovery factor and electricity price are case inputs; partial accounting within the evaluated categories. Body: exploration/magnet_materials/bodies/magnet_conductor_alternatives/subsystem_annualized_cost_impl.py. **Last Updated**: 2026-09-29

SysML Source: root-0/magnet_conductor_alternatives.sysml:233
    """
    capital_total: float = Field(description="capital_total output")
    annualized_cost: float = Field(description="annualized_cost output")
    annual_electricity: float = Field(description="annual_electricity output")
