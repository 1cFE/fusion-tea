"""Constraint module for whole_plant_conversion__plant__gas_boundary__exchanger_flow_margin_ok__396e8f7ff4b4cd78 (Item 7 / D2/D3/D9).

Effective predicate: whole_plant_conversion::plant::gas_boundary::exchanger_flow_margin_ok in owner instance whole_plant_conversion__plant__gas_boundary.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from whole_plant_conversion_tea.schemas.constraint_types import ConstraintEvaluation
from whole_plant_conversion_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_component_alternatives_thermal__nonnegative_margin


class PlantGasBoundaryExchangerFlowMarginOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    margin_in: float


class PlantGasBoundaryExchangerFlowMarginOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class PlantGasBoundaryExchangerFlowMarginOkConstraintModule(ModuleBase[PlantGasBoundaryExchangerFlowMarginOkConstraintInput, PlantGasBoundaryExchangerFlowMarginOkConstraintOutput]):
    name: str = "whole_plant_conversion__plant__gas_boundary__exchanger_flow_margin_ok__396e8f7ff4b4cd78"
    version: str = "v0.1"

    CONSTRAINT_ID = "whole_plant_conversion__plant__gas_boundary__exchanger_flow_margin_ok__396e8f7ff4b4cd78"

    def run(self, margin_in: float) -> ModuleResult[PlantGasBoundaryExchangerFlowMarginOkConstraintOutput]:
        PlantGasBoundaryExchangerFlowMarginOkConstraintInput(margin_in=margin_in)  # validate every resolved formal
        body = constraint_pred_definition_component_alternatives_thermal__nonnegative_margin(margin_in=margin_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=PlantGasBoundaryExchangerFlowMarginOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"margin_in": float(margin_in)},
                )
            )
        )
