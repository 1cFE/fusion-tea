"""Auto-generated implementation for Magnet_Structure_Cost.

AUTO_IMPLEMENTED = True

SysML Source: root-0/analyses/mfe_magnet_cost.sysml:103

SysML Expressions:
    cost = n_coils * m_casing * steel_price * f_steel_fab
    
Documentation:
Magnet casing-structure capital [$] on a steel-mass basis (WI-035 D5):

  cost = n_coils * m_casing * steel_price * f_steel_fab

Covers the COIL CASINGS only; inter-coil plates, support rings, and
legs remain CAS22.1.5 primary structure ('Structure Cost') -- the
boundary that prevents double counting. m_casing is bound per
instance; for Stellaris the printed cast-part floor is used as a
knowing lower bound with the seam named in the binding doc.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml (pin 0254385);
knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md
*Ref**: costing_constants.yaml:52-53 (coil_steel_price_per_kg 6.0,
coil_steel_fab_markup 3.0 "coil-case / inter-coil support
fabrication"); raw.pdf sec. 2.10 (casing cast parts 63-200 t;
AISI 316LN)
*Basis**: casing steel mass x fabricated-steel rate x fabrication
markup; concept-agnostic (MR-3)
"""

AUTO_IMPLEMENTED = True

from stellarator_tea.modules.mfe_magnet_cost.magnet_structure_cost import Magnet_Structure_CostInput


def run_magnet_structure_cost(inputs: Magnet_Structure_CostInput) -> float:
    """Execute Magnet_Structure_Cost calculation.

Magnet casing-structure capital [$] on a steel-mass basis (WI-035 D5):

  cost = n_coils * m_casing * steel_price * f_steel_fab

Covers the COIL CASINGS only; inter-coil plates, support rings, and
legs remain CAS22.1.5 primary structure ('Structure Cost') -- the
boundary that prevents double counting. m_casing is bound per
instance; for Stellaris the printed cast-part floor is used as a
knowing lower bound with the seam named in the binding doc.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml (pin 0254385);
knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md
*Ref**: costing_constants.yaml:52-53 (coil_steel_price_per_kg 6.0,
coil_steel_fab_markup 3.0 "coil-case / inter-coil support
fabrication"); raw.pdf sec. 2.10 (casing cast parts 63-200 t;
AISI 316LN)
*Basis**: casing steel mass x fabricated-steel rate x fabrication
markup; concept-agnostic (MR-3)

SysML Source: root-0/analyses/mfe_magnet_cost.sysml:103

SysML Expressions:
    cost = n_coils * m_casing * steel_price * f_steel_fab
    
Documentation:
Magnet casing-structure capital [$] on a steel-mass basis (WI-035 D5):

  cost = n_coils * m_casing * steel_price * f_steel_fab

Covers the COIL CASINGS only; inter-coil plates, support rings, and
legs remain CAS22.1.5 primary structure ('Structure Cost') -- the
boundary that prevents double counting. m_casing is bound per
instance; for Stellaris the printed cast-part floor is used as a
knowing lower bound with the seam named in the binding doc.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml (pin 0254385);
knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md
*Ref**: costing_constants.yaml:52-53 (coil_steel_price_per_kg 6.0,
coil_steel_fab_markup 3.0 "coil-case / inter-coil support
fabrication"); raw.pdf sec. 2.10 (casing cast parts 63-200 t;
AISI 316LN)
*Basis**: casing steel mass x fabricated-steel rate x fabrication
markup; concept-agnostic (MR-3)

Args:
    inputs: Input parameters validated against Magnet_Structure_CostInput schema

Returns:
    float: cost

Example:
    >>> inputs = Magnet_Structure_CostInput(...)
    >>> result = run_magnet_structure_cost(inputs)
    """
    return (((inputs.n_coils * inputs.m_casing) * inputs.steel_price) * inputs.f_steel_fab)
