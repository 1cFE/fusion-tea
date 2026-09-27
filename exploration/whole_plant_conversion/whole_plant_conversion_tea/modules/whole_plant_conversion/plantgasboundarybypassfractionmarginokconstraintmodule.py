"""Constraint module for whole_plant_conversion__plant__gas_boundary__bypass_fraction_margin_ok__c17576ed428ad624 (Item 7 / D2/D3/D9).

Effective predicate: whole_plant_conversion::plant::gas_boundary::bypass_fraction_margin_ok in owner instance whole_plant_conversion__plant__gas_boundary.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from whole_plant_conversion_tea.schemas.constraint_types import ConstraintEvaluation
from whole_plant_conversion_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_component_alternatives_thermal__nonnegative_margin


class PlantGasBoundaryBypassFractionMarginOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    margin_in: float


class PlantGasBoundaryBypassFractionMarginOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class PlantGasBoundaryBypassFractionMarginOkConstraintModule(ModuleBase[PlantGasBoundaryBypassFractionMarginOkConstraintInput, PlantGasBoundaryBypassFractionMarginOkConstraintOutput]):
    name: str = "whole_plant_conversion__plant__gas_boundary__bypass_fraction_margin_ok__c17576ed428ad624"
    version: str = "v0.1"

    CONSTRAINT_ID = "whole_plant_conversion__plant__gas_boundary__bypass_fraction_margin_ok__c17576ed428ad624"

    def run(self, margin_in: float) -> ModuleResult[PlantGasBoundaryBypassFractionMarginOkConstraintOutput]:
        PlantGasBoundaryBypassFractionMarginOkConstraintInput(margin_in=margin_in)  # validate every resolved formal
        body = constraint_pred_definition_component_alternatives_thermal__nonnegative_margin(margin_in=margin_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=PlantGasBoundaryBypassFractionMarginOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"margin_in": float(margin_in)},
                )
            )
        )
