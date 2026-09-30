"""Constraint module for stellarator_09_materials__rebco_material__divertor_heat_ok__4848b02ea1557c2d (Item 7 / D2/D3/D9).

Effective predicate: mfe_plant::'MFE Power Plant'::divertor_heat_ok in owner instance stellarator_09_materials__rebco_material.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_rebco_tea.schemas.constraint_types import ConstraintEvaluation
from stellarator_materials_rebco_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_mfe_viability__divertor_target_heat_limit


class RebcoMaterialDivertorHeatOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    q_target_peak_in: float
    q_target_limit_in: float


class RebcoMaterialDivertorHeatOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class RebcoMaterialDivertorHeatOkConstraintModule(ModuleBase[RebcoMaterialDivertorHeatOkConstraintInput, RebcoMaterialDivertorHeatOkConstraintOutput]):
    name: str = "stellarator_09_materials__rebco_material__divertor_heat_ok__4848b02ea1557c2d"
    version: str = "v0.1"

    CONSTRAINT_ID = "stellarator_09_materials__rebco_material__divertor_heat_ok__4848b02ea1557c2d"

    def run(self, q_target_peak_in: float, q_target_limit_in: float) -> ModuleResult[RebcoMaterialDivertorHeatOkConstraintOutput]:
        RebcoMaterialDivertorHeatOkConstraintInput(q_target_peak_in=q_target_peak_in, q_target_limit_in=q_target_limit_in)  # validate every resolved formal
        body = constraint_pred_definition_mfe_viability__divertor_target_heat_limit(q_target_peak_in=q_target_peak_in, q_target_limit_in=q_target_limit_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=RebcoMaterialDivertorHeatOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"q_target_peak_in": float(q_target_peak_in), "q_target_limit_in": float(q_target_limit_in)},
                )
            )
        )
