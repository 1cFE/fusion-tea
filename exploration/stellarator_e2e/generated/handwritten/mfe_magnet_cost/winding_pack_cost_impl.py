"""Auto-generated implementation for Winding_Pack_Cost.

AUTO_IMPLEMENTED = True

SysML Source: root-0/analyses/mfe_magnet_cost.sysml:56

SysML Expressions:
    kAm_wind = n_coils * I_coil * f_set * c_coil / 1000.0
    cost = kAm_wind * cost_per_kAm * f_wp_fab
    
Documentation:
Winding-pack capital [$] over the REAL winding length (WI-035 D4):

  kAm_wind = n_coils * I_coil * f_set * c_coil / 1000
  cost     = kAm_wind * cost_per_kAm * f_wp_fab

Replaces the proxy length 4*pi*r_coil (a bore-radius stand-in,
WI-032) with the coil count x set-mean current x printed typical
circumference. f_wp_fab is the winding fabrication markup
(content: winding, insulation, cooling, jointing, test --
costing_constants.yaml:50 -- times the documented NCSX non-planar
production penalty, yaml:60-66). Quench protection carries no
separate account: the NI coils are passively protected (printed,
sec. 2.9).

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml (pin 0254385);
knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md
*Ref**: costing_constants.yaml:50 (fab content), :60-72 (5.87 =
3.09 x 1.9 NCSX penalty; path factor separate); cas22.py:34
("conductor is ~10-15% of finished magnet cost" -- cross-check);
images/page_022_table_0.png (Table 8 per-coil currents);
raw.pdf sec. 2.9 (25 m typical circumference; NI passive quench
protection)
*Basis**: conductor quantity over real winding length x $/kA-m x
content-mapped fabrication markup; concept-agnostic (MR-3)
"""

AUTO_IMPLEMENTED = True

from stellarator_tea.modules.mfe_magnet_cost.winding_pack_cost import Winding_Pack_CostInput


def run_winding_pack_cost(inputs: Winding_Pack_CostInput) -> float:
    """Execute Winding_Pack_Cost calculation.

Winding-pack capital [$] over the REAL winding length (WI-035 D4):

  kAm_wind = n_coils * I_coil * f_set * c_coil / 1000
  cost     = kAm_wind * cost_per_kAm * f_wp_fab

Replaces the proxy length 4*pi*r_coil (a bore-radius stand-in,
WI-032) with the coil count x set-mean current x printed typical
circumference. f_wp_fab is the winding fabrication markup
(content: winding, insulation, cooling, jointing, test --
costing_constants.yaml:50 -- times the documented NCSX non-planar
production penalty, yaml:60-66). Quench protection carries no
separate account: the NI coils are passively protected (printed,
sec. 2.9).

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml (pin 0254385);
knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md
*Ref**: costing_constants.yaml:50 (fab content), :60-72 (5.87 =
3.09 x 1.9 NCSX penalty; path factor separate); cas22.py:34
("conductor is ~10-15% of finished magnet cost" -- cross-check);
images/page_022_table_0.png (Table 8 per-coil currents);
raw.pdf sec. 2.9 (25 m typical circumference; NI passive quench
protection)
*Basis**: conductor quantity over real winding length x $/kA-m x
content-mapped fabrication markup; concept-agnostic (MR-3)

SysML Source: root-0/analyses/mfe_magnet_cost.sysml:56

SysML Expressions:
    kAm_wind = n_coils * I_coil * f_set * c_coil / 1000.0
    cost = kAm_wind * cost_per_kAm * f_wp_fab
    
Documentation:
Winding-pack capital [$] over the REAL winding length (WI-035 D4):

  kAm_wind = n_coils * I_coil * f_set * c_coil / 1000
  cost     = kAm_wind * cost_per_kAm * f_wp_fab

Replaces the proxy length 4*pi*r_coil (a bore-radius stand-in,
WI-032) with the coil count x set-mean current x printed typical
circumference. f_wp_fab is the winding fabrication markup
(content: winding, insulation, cooling, jointing, test --
costing_constants.yaml:50 -- times the documented NCSX non-planar
production penalty, yaml:60-66). Quench protection carries no
separate account: the NI coils are passively protected (printed,
sec. 2.9).

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml (pin 0254385);
knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md
*Ref**: costing_constants.yaml:50 (fab content), :60-72 (5.87 =
3.09 x 1.9 NCSX penalty; path factor separate); cas22.py:34
("conductor is ~10-15% of finished magnet cost" -- cross-check);
images/page_022_table_0.png (Table 8 per-coil currents);
raw.pdf sec. 2.9 (25 m typical circumference; NI passive quench
protection)
*Basis**: conductor quantity over real winding length x $/kA-m x
content-mapped fabrication markup; concept-agnostic (MR-3)

Args:
    inputs: Input parameters validated against Winding_Pack_CostInput schema

Returns:
    float: cost

Example:
    >>> inputs = Winding_Pack_CostInput(...)
    >>> result = run_winding_pack_cost(inputs)
    """
    kAm_wind = ((((inputs.n_coils * inputs.I_coil) * inputs.f_set) * inputs.c_coil) / 1000.0)
    return ((kAm_wind * inputs.cost_per_kAm) * inputs.f_wp_fab)
