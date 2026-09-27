"""Constraint module for component_alternatives__plant__water_ic1__power_margin_ok__ceac76348e0eb2b6 (Item 7 / D2/D3/D9).

Effective predicate: component_alternatives::plant::water_ic1::power_margin_ok in owner instance component_alternatives__plant__water_ic1.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from component_alternatives_tea.schemas.constraint_types import ConstraintEvaluation
from component_alternatives_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_component_alternatives_thermal__nonnegative_margin


class PlantWaterIc1PowerMarginOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    margin_in: float


class PlantWaterIc1PowerMarginOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class PlantWaterIc1PowerMarginOkConstraintModule(ModuleBase[PlantWaterIc1PowerMarginOkConstraintInput, PlantWaterIc1PowerMarginOkConstraintOutput]):
    name: str = "component_alternatives__plant__water_ic1__power_margin_ok__ceac76348e0eb2b6"
    version: str = "v0.1"

    CONSTRAINT_ID = "component_alternatives__plant__water_ic1__power_margin_ok__ceac76348e0eb2b6"

    def run(self, margin_in: float) -> ModuleResult[PlantWaterIc1PowerMarginOkConstraintOutput]:
        PlantWaterIc1PowerMarginOkConstraintInput(margin_in=margin_in)  # validate every resolved formal
        body = constraint_pred_definition_component_alternatives_thermal__nonnegative_margin(margin_in=margin_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=PlantWaterIc1PowerMarginOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"margin_in": float(margin_in)},
                )
            )
        )
