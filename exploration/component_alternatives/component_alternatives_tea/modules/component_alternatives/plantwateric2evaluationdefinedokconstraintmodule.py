"""Constraint module for component_alternatives__plant__water_ic2__evaluation_defined_ok__06ab6aea3f7f761b (Item 7 / D2/D3/D9).

Effective predicate: component_alternatives::plant::water_ic2::evaluation_defined_ok in owner instance component_alternatives__plant__water_ic2.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from component_alternatives_tea.schemas.constraint_types import ConstraintEvaluation
from component_alternatives_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_component_alternatives_thermal__required_flag


class PlantWaterIc2EvaluationDefinedOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    flag_in: float


class PlantWaterIc2EvaluationDefinedOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class PlantWaterIc2EvaluationDefinedOkConstraintModule(ModuleBase[PlantWaterIc2EvaluationDefinedOkConstraintInput, PlantWaterIc2EvaluationDefinedOkConstraintOutput]):
    name: str = "component_alternatives__plant__water_ic2__evaluation_defined_ok__06ab6aea3f7f761b"
    version: str = "v0.1"

    CONSTRAINT_ID = "component_alternatives__plant__water_ic2__evaluation_defined_ok__06ab6aea3f7f761b"

    def run(self, flag_in: float) -> ModuleResult[PlantWaterIc2EvaluationDefinedOkConstraintOutput]:
        PlantWaterIc2EvaluationDefinedOkConstraintInput(flag_in=flag_in)  # validate every resolved formal
        body = constraint_pred_definition_component_alternatives_thermal__required_flag(flag_in=flag_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=PlantWaterIc2EvaluationDefinedOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"flag_in": float(flag_in)},
                )
            )
        )
