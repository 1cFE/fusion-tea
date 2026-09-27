"""Constraint module for whole_plant_conversion__plant__gas_actual_approach__hot_gap_ok__5e9b6647fc4988da (Item 7 / D2/D3/D9).

Effective predicate: whole_plant_conversion::plant::gas_actual_approach::hot_gap_ok in owner instance whole_plant_conversion__plant__gas_actual_approach.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from whole_plant_conversion_tea.schemas.constraint_types import ConstraintEvaluation
from whole_plant_conversion_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_whole_plant_conversion_accounts__whole_plant_positive


class PlantGasActualApproachHotGapOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    metric_in: float


class PlantGasActualApproachHotGapOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class PlantGasActualApproachHotGapOkConstraintModule(ModuleBase[PlantGasActualApproachHotGapOkConstraintInput, PlantGasActualApproachHotGapOkConstraintOutput]):
    name: str = "whole_plant_conversion__plant__gas_actual_approach__hot_gap_ok__5e9b6647fc4988da"
    version: str = "v0.1"

    CONSTRAINT_ID = "whole_plant_conversion__plant__gas_actual_approach__hot_gap_ok__5e9b6647fc4988da"

    def run(self, metric_in: float) -> ModuleResult[PlantGasActualApproachHotGapOkConstraintOutput]:
        PlantGasActualApproachHotGapOkConstraintInput(metric_in=metric_in)  # validate every resolved formal
        body = constraint_pred_definition_whole_plant_conversion_accounts__whole_plant_positive(metric_in=metric_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=PlantGasActualApproachHotGapOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"metric_in": float(metric_in)},
                )
            )
        )
