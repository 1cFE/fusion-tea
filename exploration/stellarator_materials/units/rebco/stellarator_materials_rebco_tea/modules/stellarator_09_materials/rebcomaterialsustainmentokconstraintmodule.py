"""Constraint module for stellarator_09_materials__rebco_material__sustainment_ok__60ca4f2cb2aaa5bd (Item 7 / D2/D3/D9).

Effective predicate: stellarator_09_materials::rebco_material::sustainment_ok in owner instance stellarator_09_materials__rebco_material.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_rebco_tea.schemas.constraint_types import ConstraintEvaluation
from stellarator_materials_rebco_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_mfe_viability__sustainment_limit


class RebcoMaterialSustainmentOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    p_aux_required_in: float
    p_aux_installed_in: float


class RebcoMaterialSustainmentOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class RebcoMaterialSustainmentOkConstraintModule(ModuleBase[RebcoMaterialSustainmentOkConstraintInput, RebcoMaterialSustainmentOkConstraintOutput]):
    name: str = "stellarator_09_materials__rebco_material__sustainment_ok__60ca4f2cb2aaa5bd"
    version: str = "v0.1"

    CONSTRAINT_ID = "stellarator_09_materials__rebco_material__sustainment_ok__60ca4f2cb2aaa5bd"

    def run(self, p_aux_required_in: float, p_aux_installed_in: float) -> ModuleResult[RebcoMaterialSustainmentOkConstraintOutput]:
        RebcoMaterialSustainmentOkConstraintInput(p_aux_required_in=p_aux_required_in, p_aux_installed_in=p_aux_installed_in)  # validate every resolved formal
        body = constraint_pred_definition_mfe_viability__sustainment_limit(p_aux_required_in=p_aux_required_in, p_aux_installed_in=p_aux_installed_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=RebcoMaterialSustainmentOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"p_aux_required_in": float(p_aux_required_in), "p_aux_installed_in": float(p_aux_installed_in)},
                )
            )
        )
