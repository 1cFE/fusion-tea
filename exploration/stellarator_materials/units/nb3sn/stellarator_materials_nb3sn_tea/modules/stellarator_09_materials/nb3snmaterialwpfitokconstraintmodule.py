"""Constraint module for stellarator_09_materials__nb3sn_material__wp_fit_ok__11c66596aad579df (Item 7 / D2/D3/D9).

Effective predicate: stellarator_09_materials::nb3sn_material::wp_fit_ok in owner instance stellarator_09_materials__nb3sn_material.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_nb3sn_tea.schemas.constraint_types import ConstraintEvaluation
from stellarator_materials_nb3sn_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_mfe_winding_pack_fit__winding_pack_fits_casing


class Nb3snMaterialWpFitOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    minimum_margin_in: float


class Nb3snMaterialWpFitOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class Nb3snMaterialWpFitOkConstraintModule(ModuleBase[Nb3snMaterialWpFitOkConstraintInput, Nb3snMaterialWpFitOkConstraintOutput]):
    name: str = "stellarator_09_materials__nb3sn_material__wp_fit_ok__11c66596aad579df"
    version: str = "v0.1"

    CONSTRAINT_ID = "stellarator_09_materials__nb3sn_material__wp_fit_ok__11c66596aad579df"

    def run(self, minimum_margin_in: float) -> ModuleResult[Nb3snMaterialWpFitOkConstraintOutput]:
        Nb3snMaterialWpFitOkConstraintInput(minimum_margin_in=minimum_margin_in)  # validate every resolved formal
        body = constraint_pred_definition_mfe_winding_pack_fit__winding_pack_fits_casing(minimum_margin_in=minimum_margin_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=Nb3snMaterialWpFitOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"minimum_margin_in": float(minimum_margin_in)},
                )
            )
        )
