"""Auto-generated implementation for Magnet_Coil_Cost.

AUTO_IMPLEMENTED = True

SysML Source: root-0/analyses/mfe_magnet_cost.sysml:4

SysML Expressions:
    mu0 = 1.25663706212e-06
    total_kAm = G * B * R0 * r_coil / (mu0 * 1000.0)
    capital_cost = total_kAm * cost_per_kAm * coil_markup
    
Documentation:
Superconducting magnet/coil capital cost from the bilinear toroidal
conductor-quantity model, concept-agnostic across MFE approaches.

  total_kAm = G * B * R0 * r_coil / (mu0 * 1000)
  capital_cost = total_kAm * cost_per_kAm * coil_markup

The ampere-meter quantity follows Ampere's law around the torus
(ampere-turns ~ B*R0) times the conductor length per turn (~ coil-bore
radius r_coil). The expensive superconductor dominates SC coil cost, so
cost = conductor quantity * $/kA-m * a manufacturing markup (winding,
quench protection, cryostat, testing).

Fully parameterized (MR-WI009-8): G, B, R0, r_coil, cost_per_kAm, and
coil_markup are all inputs -- the concept sets them in WI-011. See the
reconciliation note below for the current 1costingFE values.

Note on units: the 1costingFE source divides the conductor cost by 1e6
to express M$ (cas22.py:442). This calc omits that conversion, so
capital_cost inherits the units of cost_per_kAm (i.e. $ when
cost_per_kAm is $/kA-m). Apply the M$ scaling downstream if desired.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
*Ref**: cas22.py:427 (total_kAm), cas22.py:441-444 (SC coil cost)
*Basis**: MFE coil conductor-quantity cost model; magnet cost rises
with B, R0, r_coil (SV-018)
"""

AUTO_IMPLEMENTED = True

from stellarator_tea.modules.mfe_magnet_cost.magnet_coil_cost import Magnet_Coil_CostInput


def run_magnet_coil_cost(inputs: Magnet_Coil_CostInput) -> float:
    """Execute Magnet_Coil_Cost calculation.

Superconducting magnet/coil capital cost from the bilinear toroidal
conductor-quantity model, concept-agnostic across MFE approaches.

  total_kAm = G * B * R0 * r_coil / (mu0 * 1000)
  capital_cost = total_kAm * cost_per_kAm * coil_markup

The ampere-meter quantity follows Ampere's law around the torus
(ampere-turns ~ B*R0) times the conductor length per turn (~ coil-bore
radius r_coil). The expensive superconductor dominates SC coil cost, so
cost = conductor quantity * $/kA-m * a manufacturing markup (winding,
quench protection, cryostat, testing).

Fully parameterized (MR-WI009-8): G, B, R0, r_coil, cost_per_kAm, and
coil_markup are all inputs -- the concept sets them in WI-011. See the
reconciliation note below for the current 1costingFE values.

Note on units: the 1costingFE source divides the conductor cost by 1e6
to express M$ (cas22.py:442). This calc omits that conversion, so
capital_cost inherits the units of cost_per_kAm (i.e. $ when
cost_per_kAm is $/kA-m). Apply the M$ scaling downstream if desired.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
*Ref**: cas22.py:427 (total_kAm), cas22.py:441-444 (SC coil cost)
*Basis**: MFE coil conductor-quantity cost model; magnet cost rises
with B, R0, r_coil (SV-018)

SysML Source: root-0/analyses/mfe_magnet_cost.sysml:4

SysML Expressions:
    mu0 = 1.25663706212e-06
    total_kAm = G * B * R0 * r_coil / (mu0 * 1000.0)
    capital_cost = total_kAm * cost_per_kAm * coil_markup
    
Documentation:
Superconducting magnet/coil capital cost from the bilinear toroidal
conductor-quantity model, concept-agnostic across MFE approaches.

  total_kAm = G * B * R0 * r_coil / (mu0 * 1000)
  capital_cost = total_kAm * cost_per_kAm * coil_markup

The ampere-meter quantity follows Ampere's law around the torus
(ampere-turns ~ B*R0) times the conductor length per turn (~ coil-bore
radius r_coil). The expensive superconductor dominates SC coil cost, so
cost = conductor quantity * $/kA-m * a manufacturing markup (winding,
quench protection, cryostat, testing).

Fully parameterized (MR-WI009-8): G, B, R0, r_coil, cost_per_kAm, and
coil_markup are all inputs -- the concept sets them in WI-011. See the
reconciliation note below for the current 1costingFE values.

Note on units: the 1costingFE source divides the conductor cost by 1e6
to express M$ (cas22.py:442). This calc omits that conversion, so
capital_cost inherits the units of cost_per_kAm (i.e. $ when
cost_per_kAm is $/kA-m). Apply the M$ scaling downstream if desired.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
*Ref**: cas22.py:427 (total_kAm), cas22.py:441-444 (SC coil cost)
*Basis**: MFE coil conductor-quantity cost model; magnet cost rises
with B, R0, r_coil (SV-018)

Args:
    inputs: Input parameters validated against Magnet_Coil_CostInput schema

Returns:
    float: capital_cost

Example:
    >>> inputs = Magnet_Coil_CostInput(...)
    >>> result = run_magnet_coil_cost(inputs)
    """
    total_kAm = ((((inputs.G * inputs.B) * inputs.R0) * inputs.r_coil) / (inputs.mu0 * 1000.0))
    return ((total_kAm * inputs.cost_per_kAm) * inputs.coil_markup)
