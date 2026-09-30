"""Constraint module for stellarator_09_materials__nb3sn_material__burn_hold_ok__8a46a7e0aeda985a (Item 7 / D2/D3/D9).

Effective predicate: stellarator_09_materials::nb3sn_material::burn_hold_ok in owner instance stellarator_09_materials__nb3sn_material.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_nb3sn_tea.schemas.constraint_types import ConstraintEvaluation
from stellarator_materials_nb3sn_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_mfe_viability__burn_hold


class Nb3snMaterialBurnHoldOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    p_aux_required_in: float


class Nb3snMaterialBurnHoldOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class Nb3snMaterialBurnHoldOkConstraintModule(ModuleBase[Nb3snMaterialBurnHoldOkConstraintInput, Nb3snMaterialBurnHoldOkConstraintOutput]):
    name: str = "stellarator_09_materials__nb3sn_material__burn_hold_ok__8a46a7e0aeda985a"
    version: str = "v0.1"

    CONSTRAINT_ID = "stellarator_09_materials__nb3sn_material__burn_hold_ok__8a46a7e0aeda985a"

    def run(self, p_aux_required_in: float) -> ModuleResult[Nb3snMaterialBurnHoldOkConstraintOutput]:
        Nb3snMaterialBurnHoldOkConstraintInput(p_aux_required_in=p_aux_required_in)  # validate every resolved formal
        body = constraint_pred_definition_mfe_viability__burn_hold(p_aux_required_in=p_aux_required_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=Nb3snMaterialBurnHoldOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"p_aux_required_in": float(p_aux_required_in)},
                )
            )
        )
