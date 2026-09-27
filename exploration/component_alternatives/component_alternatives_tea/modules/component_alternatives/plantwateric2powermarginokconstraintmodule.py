"""Constraint module for component_alternatives__plant__water_ic2__power_margin_ok__9155c8131175c99b (Item 7 / D2/D3/D9).

Effective predicate: component_alternatives::plant::water_ic2::power_margin_ok in owner instance component_alternatives__plant__water_ic2.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from component_alternatives_tea.schemas.constraint_types import ConstraintEvaluation
from component_alternatives_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_component_alternatives_thermal__nonnegative_margin


class PlantWaterIc2PowerMarginOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    margin_in: float


class PlantWaterIc2PowerMarginOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class PlantWaterIc2PowerMarginOkConstraintModule(ModuleBase[PlantWaterIc2PowerMarginOkConstraintInput, PlantWaterIc2PowerMarginOkConstraintOutput]):
    name: str = "component_alternatives__plant__water_ic2__power_margin_ok__9155c8131175c99b"
    version: str = "v0.1"

    CONSTRAINT_ID = "component_alternatives__plant__water_ic2__power_margin_ok__9155c8131175c99b"

    def run(self, margin_in: float) -> ModuleResult[PlantWaterIc2PowerMarginOkConstraintOutput]:
        PlantWaterIc2PowerMarginOkConstraintInput(margin_in=margin_in)  # validate every resolved formal
        body = constraint_pred_definition_component_alternatives_thermal__nonnegative_margin(margin_in=margin_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=PlantWaterIc2PowerMarginOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"margin_in": float(margin_in)},
                )
            )
        )
