"""Magnet_Structure_CostModule Module Wrapper

TEAx module for Magnet_Structure_Cost calculation.

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

Inputs:
    - m_casing: m_casing parameter
    - steel_price: steel_price parameter
    - n_coils: n_coils parameter
    - f_steel_fab: f_steel_fab parameter

Outputs:
    - cost: cost result

SysML Source: root-0/analyses/mfe_magnet_cost.sysml:103

SysML Source: root-0/analyses/mfe_magnet_cost.sysml:103

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_magnet_cost/magnet_structure_cost_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float


class Magnet_Structure_CostInput(BaseModel):
    """Input model for Magnet_Structure_CostModule.

    Attributes:
        m_casing: m_casing input
        steel_price: steel_price input
        n_coils: n_coils input
        f_steel_fab: f_steel_fab input
    """
    m_casing: float = Field(..., description="m_casing input")
    steel_price: float = Field(..., description="steel_price input")
    n_coils: float = Field(..., description="n_coils input")
    f_steel_fab: float = Field(..., description="f_steel_fab input")


class Magnet_Structure_CostModule(ModuleBase[Magnet_Structure_CostInput, Float]):
    """TEAx module for Magnet_Structure_Cost calculation.

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

Inputs:
    - m_casing: m_casing parameter
    - steel_price: steel_price parameter
    - n_coils: n_coils parameter
    - f_steel_fab: f_steel_fab parameter

Outputs:
    - cost: cost result

SysML Source: root-0/analyses/mfe_magnet_cost.sysml:103

    SysML Source: root-0/analyses/mfe_magnet_cost.sysml:103

    Calculation Specification:
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

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_magnet_cost.magnet_structure_cost_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "Magnet_Structure_CostModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, m_casing: float, steel_price: float, n_coils: float, f_steel_fab: float    ) -> Magnet_Structure_CostInput:
        """Validate inputs and fill defaults.

        Args:
            m_casing: m_casing input
            steel_price: steel_price input
            n_coils: n_coils input
            f_steel_fab: f_steel_fab input

        Returns:
            Validated input model
        """
        return Magnet_Structure_CostInput(m_casing=m_casing, steel_price=steel_price, n_coils=n_coils, f_steel_fab=f_steel_fab)

    def run(
        self, m_casing: float, steel_price: float, n_coils: float, f_steel_fab: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            m_casing: m_casing input
            steel_price: steel_price input
            n_coils: n_coils input
            f_steel_fab: f_steel_fab input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(m_casing, steel_price, n_coils, f_steel_fab)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_magnet_cost.magnet_structure_cost_impl import (
            run_magnet_structure_cost,
        )

        # Execute implementation - returns single value
        cost = run_magnet_structure_cost(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(cost))
