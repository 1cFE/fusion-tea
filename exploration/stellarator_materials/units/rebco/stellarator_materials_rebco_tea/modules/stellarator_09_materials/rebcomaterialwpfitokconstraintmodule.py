"""Constraint module for stellarator_09_materials__rebco_material__wp_fit_ok__63e3c00c99928ca9 (Item 7 / D2/D3/D9).

Effective predicate: stellarator_09_materials::rebco_material::wp_fit_ok in owner instance stellarator_09_materials__rebco_material.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_rebco_tea.schemas.constraint_types import ConstraintEvaluation
from stellarator_materials_rebco_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_mfe_winding_pack_fit__winding_pack_fits_casing


class RebcoMaterialWpFitOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    minimum_margin_in: float


class RebcoMaterialWpFitOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class RebcoMaterialWpFitOkConstraintModule(ModuleBase[RebcoMaterialWpFitOkConstraintInput, RebcoMaterialWpFitOkConstraintOutput]):
    name: str = "stellarator_09_materials__rebco_material__wp_fit_ok__63e3c00c99928ca9"
    version: str = "v0.1"

    CONSTRAINT_ID = "stellarator_09_materials__rebco_material__wp_fit_ok__63e3c00c99928ca9"

    def run(self, minimum_margin_in: float) -> ModuleResult[RebcoMaterialWpFitOkConstraintOutput]:
        RebcoMaterialWpFitOkConstraintInput(minimum_margin_in=minimum_margin_in)  # validate every resolved formal
        body = constraint_pred_definition_mfe_winding_pack_fit__winding_pack_fits_casing(minimum_margin_in=minimum_margin_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=RebcoMaterialWpFitOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"minimum_margin_in": float(minimum_margin_in)},
                )
            )
        )
