"""Auto-generated implementation for Meier_Total_Capital_Cost.

AUTO_IMPLEMENTED = True

SysML Source: /home/reid/1cfe/fusion-tea/exploration/ife_e2e/models/analyses/hif_economics.sysml:65

SysML Expressions:
    total_capital_billions = LiteralRationalEvaluation() * reactor_cost + driver_cost + target_factory_cost
    
Documentation:
Total plant capital cost including indirect cost multiplier.
Factor 1.83 = total-to-direct cost ratio (midway between coal
at 1.53 and nuclear-best at 2.07).

*Source**: knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/output.md
*Ref**: Eq. 2 (lines 102-117)
*Basis**: Meier 1986 indirect cost multiplier. Year-dollars: 1988$.
"""

AUTO_IMPLEMENTED = True

from ife_tea.modules.hif_economics.meier_total_capital_cost import Meier_Total_Capital_CostInput


def run_meier_total_capital_cost(inputs: Meier_Total_Capital_CostInput) -> float:
    """Execute Meier_Total_Capital_Cost calculation.

Total plant capital cost including indirect cost multiplier.
Factor 1.83 = total-to-direct cost ratio (midway between coal
at 1.53 and nuclear-best at 2.07).

*Source**: knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/output.md
*Ref**: Eq. 2 (lines 102-117)
*Basis**: Meier 1986 indirect cost multiplier. Year-dollars: 1988$.

SysML Source: /home/reid/1cfe/fusion-tea/exploration/ife_e2e/models/analyses/hif_economics.sysml:65

SysML Expressions:
    total_capital_billions = LiteralRationalEvaluation() * reactor_cost + driver_cost + target_factory_cost
    
Documentation:
Total plant capital cost including indirect cost multiplier.
Factor 1.83 = total-to-direct cost ratio (midway between coal
at 1.53 and nuclear-best at 2.07).

*Source**: knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/output.md
*Ref**: Eq. 2 (lines 102-117)
*Basis**: Meier 1986 indirect cost multiplier. Year-dollars: 1988$.

Args:
    inputs: Input parameters validated against Meier_Total_Capital_CostInput schema

Returns:
    float: total_capital_billions

Example:
    >>> inputs = Meier_Total_Capital_CostInput(...)
    >>> result = run_meier_total_capital_cost(inputs)
    """
    return (1.83 * ((inputs.reactor_cost + inputs.driver_cost) + inputs.target_factory_cost))
