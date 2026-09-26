"""Constraint module for costed_loop_brayton__plant__checks__return_condition_ok__53e3282ac7398a73 (Item 7 / D2/D3/D9).

Effective predicate: costed_loop_brayton::plant::checks::return_condition_ok in owner instance costed_loop_brayton__plant__checks.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from costed_loop_brayton_tea.schemas.constraint_types import ConstraintEvaluation
from costed_loop_brayton_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_loop_return_control__return_condition_held


class PlantChecksReturnConditionOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    return_residual_magnitude_in: float
    tolerance_in: float


class PlantChecksReturnConditionOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class PlantChecksReturnConditionOkConstraintModule(ModuleBase[PlantChecksReturnConditionOkConstraintInput, PlantChecksReturnConditionOkConstraintOutput]):
    name: str = "costed_loop_brayton__plant__checks__return_condition_ok__53e3282ac7398a73"
    version: str = "v0.1"

    CONSTRAINT_ID = "costed_loop_brayton__plant__checks__return_condition_ok__53e3282ac7398a73"

    def run(self, return_residual_magnitude_in: float, tolerance_in: float) -> ModuleResult[PlantChecksReturnConditionOkConstraintOutput]:
        PlantChecksReturnConditionOkConstraintInput(return_residual_magnitude_in=return_residual_magnitude_in, tolerance_in=tolerance_in)  # validate every resolved formal
        body = constraint_pred_definition_loop_return_control__return_condition_held(return_residual_magnitude_in=return_residual_magnitude_in, tolerance_in=tolerance_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=PlantChecksReturnConditionOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"return_residual_magnitude_in": float(return_residual_magnitude_in), "tolerance_in": float(tolerance_in)},
                )
            )
        )
