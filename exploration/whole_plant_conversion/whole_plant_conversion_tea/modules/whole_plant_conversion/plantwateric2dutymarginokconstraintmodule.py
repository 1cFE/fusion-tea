"""Constraint module for whole_plant_conversion__plant__water_ic2__duty_margin_ok__143f9ca6200e6779 (Item 7 / D2/D3/D9).

Effective predicate: whole_plant_conversion::plant::water_ic2::duty_margin_ok in owner instance whole_plant_conversion__plant__water_ic2.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from whole_plant_conversion_tea.schemas.constraint_types import ConstraintEvaluation
from whole_plant_conversion_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_component_alternatives_thermal__nonnegative_margin


class PlantWaterIc2DutyMarginOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    margin_in: float


class PlantWaterIc2DutyMarginOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class PlantWaterIc2DutyMarginOkConstraintModule(ModuleBase[PlantWaterIc2DutyMarginOkConstraintInput, PlantWaterIc2DutyMarginOkConstraintOutput]):
    name: str = "whole_plant_conversion__plant__water_ic2__duty_margin_ok__143f9ca6200e6779"
    version: str = "v0.1"

    CONSTRAINT_ID = "whole_plant_conversion__plant__water_ic2__duty_margin_ok__143f9ca6200e6779"

    def run(self, margin_in: float) -> ModuleResult[PlantWaterIc2DutyMarginOkConstraintOutput]:
        PlantWaterIc2DutyMarginOkConstraintInput(margin_in=margin_in)  # validate every resolved formal
        body = constraint_pred_definition_component_alternatives_thermal__nonnegative_margin(margin_in=margin_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=PlantWaterIc2DutyMarginOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"margin_in": float(margin_in)},
                )
            )
        )
