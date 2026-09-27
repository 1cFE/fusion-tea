"""Constraint module for component_alternatives__plant__water_ic1__flow_margin_ok__2ca46da8d6c9fc06 (Item 7 / D2/D3/D9).

Effective predicate: component_alternatives::plant::water_ic1::flow_margin_ok in owner instance component_alternatives__plant__water_ic1.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from component_alternatives_tea.schemas.constraint_types import ConstraintEvaluation
from component_alternatives_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_component_alternatives_thermal__nonnegative_margin


class PlantWaterIc1FlowMarginOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    margin_in: float


class PlantWaterIc1FlowMarginOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class PlantWaterIc1FlowMarginOkConstraintModule(ModuleBase[PlantWaterIc1FlowMarginOkConstraintInput, PlantWaterIc1FlowMarginOkConstraintOutput]):
    name: str = "component_alternatives__plant__water_ic1__flow_margin_ok__2ca46da8d6c9fc06"
    version: str = "v0.1"

    CONSTRAINT_ID = "component_alternatives__plant__water_ic1__flow_margin_ok__2ca46da8d6c9fc06"

    def run(self, margin_in: float) -> ModuleResult[PlantWaterIc1FlowMarginOkConstraintOutput]:
        PlantWaterIc1FlowMarginOkConstraintInput(margin_in=margin_in)  # validate every resolved formal
        body = constraint_pred_definition_component_alternatives_thermal__nonnegative_margin(margin_in=margin_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=PlantWaterIc1FlowMarginOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"margin_in": float(margin_in)},
                )
            )
        )
