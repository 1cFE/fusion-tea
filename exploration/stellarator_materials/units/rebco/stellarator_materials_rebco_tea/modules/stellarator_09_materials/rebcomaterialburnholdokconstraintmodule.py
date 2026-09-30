"""Constraint module for stellarator_09_materials__rebco_material__burn_hold_ok__b5da7626bab05382 (Item 7 / D2/D3/D9).

Effective predicate: stellarator_09_materials::rebco_material::burn_hold_ok in owner instance stellarator_09_materials__rebco_material.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_rebco_tea.schemas.constraint_types import ConstraintEvaluation
from stellarator_materials_rebco_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_mfe_viability__burn_hold


class RebcoMaterialBurnHoldOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    p_aux_required_in: float


class RebcoMaterialBurnHoldOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class RebcoMaterialBurnHoldOkConstraintModule(ModuleBase[RebcoMaterialBurnHoldOkConstraintInput, RebcoMaterialBurnHoldOkConstraintOutput]):
    name: str = "stellarator_09_materials__rebco_material__burn_hold_ok__b5da7626bab05382"
    version: str = "v0.1"

    CONSTRAINT_ID = "stellarator_09_materials__rebco_material__burn_hold_ok__b5da7626bab05382"

    def run(self, p_aux_required_in: float) -> ModuleResult[RebcoMaterialBurnHoldOkConstraintOutput]:
        RebcoMaterialBurnHoldOkConstraintInput(p_aux_required_in=p_aux_required_in)  # validate every resolved formal
        body = constraint_pred_definition_mfe_viability__burn_hold(p_aux_required_in=p_aux_required_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=RebcoMaterialBurnHoldOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"p_aux_required_in": float(p_aux_required_in)},
                )
            )
        )
