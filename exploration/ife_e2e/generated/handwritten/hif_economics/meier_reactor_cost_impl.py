"""Auto-generated implementation for Meier_Reactor_Cost.

AUTO_IMPLEMENTED = True

SysML Source: /home/reid/1cfe/fusion-tea/exploration/ife_e2e/models/analyses/hif_economics.sysml:43

SysML Expressions:
    reactor_cost_billions = LiteralRationalEvaluation() * thermal_power_gw / LiteralRationalEvaluation() ** LiteralRationalEvaluation() * LiteralRationalEvaluation() * num_units + LiteralRationalEvaluation()
    
Documentation:
HIF reactor plant direct cost (excluding driver and target factory).
Scales from the HYLIFE/Cascade reference design using thermal power
and accounts for multi-unit site savings.

Constants: C_r = $0.66B (Cascade reference at 1.67 GWt),
b = 0.49 (power scaling exponent).

*Source**: knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/output.md
*Ref**: Eq. 3 (lines 119-137)
*Basis**: Meier 1986 reactor cost scaling. Year-dollars: 1988$.
"""

AUTO_IMPLEMENTED = True

from ife_tea.modules.hif_economics.meier_reactor_cost import Meier_Reactor_CostInput


def run_meier_reactor_cost(inputs: Meier_Reactor_CostInput) -> float:
    """Execute Meier_Reactor_Cost calculation.

HIF reactor plant direct cost (excluding driver and target factory).
Scales from the HYLIFE/Cascade reference design using thermal power
and accounts for multi-unit site savings.

Constants: C_r = $0.66B (Cascade reference at 1.67 GWt),
b = 0.49 (power scaling exponent).

*Source**: knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/output.md
*Ref**: Eq. 3 (lines 119-137)
*Basis**: Meier 1986 reactor cost scaling. Year-dollars: 1988$.

SysML Source: /home/reid/1cfe/fusion-tea/exploration/ife_e2e/models/analyses/hif_economics.sysml:43

SysML Expressions:
    reactor_cost_billions = LiteralRationalEvaluation() * thermal_power_gw / LiteralRationalEvaluation() ** LiteralRationalEvaluation() * LiteralRationalEvaluation() * num_units + LiteralRationalEvaluation()
    
Documentation:
HIF reactor plant direct cost (excluding driver and target factory).
Scales from the HYLIFE/Cascade reference design using thermal power
and accounts for multi-unit site savings.

Constants: C_r = $0.66B (Cascade reference at 1.67 GWt),
b = 0.49 (power scaling exponent).

*Source**: knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/output.md
*Ref**: Eq. 3 (lines 119-137)
*Basis**: Meier 1986 reactor cost scaling. Year-dollars: 1988$.

Args:
    inputs: Input parameters validated against Meier_Reactor_CostInput schema

Returns:
    float: reactor_cost_billions

Example:
    >>> inputs = Meier_Reactor_CostInput(...)
    >>> result = run_meier_reactor_cost(inputs)
    """
    return ((0.66 * ((inputs.thermal_power_gw / 1.67) ** 0.49)) * ((0.72 * inputs.num_units) + 0.28))
