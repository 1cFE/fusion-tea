"""Auto-generated implementation for Meier_COE.

AUTO_IMPLEMENTED = True

SysML Source: /home/reid/1cfe/fusion-tea/exploration/ife_e2e/models/analyses/hif_economics.sysml:84

SysML Expressions:
    coe_cents_kwh = LiteralRationalEvaluation() * total_capital_billions / LiteralRationalEvaluation() * availability * net_electric_power_gw
    
Documentation:
Cost of Electricity from Meier's engineering-economic model.
Combines fixed charge rate (8.3%) and O&M rate (3%) into a
single capital charge rate (11.3%), then divides by annual
energy production.

Constants: 0.113 = R + M (8.3% fixed charge + 3% O&M),
0.0876 = GW-to-$/kWh conversion (8760 hr/yr * 1e6 kW/GW / 100 cents/$).

*Source**: knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/output.md
*Ref**: Eq. 1 (lines 76-102)
*Basis**: Meier 1986 COE formula. Year-dollars: 1988$.
"""

AUTO_IMPLEMENTED = True

from ife_tea.modules.hif_economics.meier_coe import Meier_COEInput


def run_meier_coe(inputs: Meier_COEInput) -> float:
    """Execute Meier_COE calculation.

Cost of Electricity from Meier's engineering-economic model.
Combines fixed charge rate (8.3%) and O&M rate (3%) into a
single capital charge rate (11.3%), then divides by annual
energy production.

Constants: 0.113 = R + M (8.3% fixed charge + 3% O&M),
0.0876 = GW-to-$/kWh conversion (8760 hr/yr * 1e6 kW/GW / 100 cents/$).

*Source**: knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/output.md
*Ref**: Eq. 1 (lines 76-102)
*Basis**: Meier 1986 COE formula. Year-dollars: 1988$.

SysML Source: /home/reid/1cfe/fusion-tea/exploration/ife_e2e/models/analyses/hif_economics.sysml:84

SysML Expressions:
    coe_cents_kwh = LiteralRationalEvaluation() * total_capital_billions / LiteralRationalEvaluation() * availability * net_electric_power_gw
    
Documentation:
Cost of Electricity from Meier's engineering-economic model.
Combines fixed charge rate (8.3%) and O&M rate (3%) into a
single capital charge rate (11.3%), then divides by annual
energy production.

Constants: 0.113 = R + M (8.3% fixed charge + 3% O&M),
0.0876 = GW-to-$/kWh conversion (8760 hr/yr * 1e6 kW/GW / 100 cents/$).

*Source**: knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/output.md
*Ref**: Eq. 1 (lines 76-102)
*Basis**: Meier 1986 COE formula. Year-dollars: 1988$.

Args:
    inputs: Input parameters validated against Meier_COEInput schema

Returns:
    float: coe_cents_kwh

Example:
    >>> inputs = Meier_COEInput(...)
    >>> result = run_meier_coe(inputs)
    """
    return ((0.113 * inputs.total_capital_billions) / ((0.0876 * inputs.availability) * inputs.net_electric_power_gw))
