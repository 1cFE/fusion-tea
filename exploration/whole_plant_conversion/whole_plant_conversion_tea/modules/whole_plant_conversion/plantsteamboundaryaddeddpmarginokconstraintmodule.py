"""Constraint module for whole_plant_conversion__plant__steam_boundary__added_dp_margin_ok__36cb21eac5ff1b89 (Item 7 / D2/D3/D9).

Effective predicate: whole_plant_conversion::plant::steam_boundary::added_dp_margin_ok in owner instance whole_plant_conversion__plant__steam_boundary.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from whole_plant_conversion_tea.schemas.constraint_types import ConstraintEvaluation
from whole_plant_conversion_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_component_alternatives_thermal__nonnegative_margin


class PlantSteamBoundaryAddedDpMarginOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    margin_in: float


class PlantSteamBoundaryAddedDpMarginOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class PlantSteamBoundaryAddedDpMarginOkConstraintModule(ModuleBase[PlantSteamBoundaryAddedDpMarginOkConstraintInput, PlantSteamBoundaryAddedDpMarginOkConstraintOutput]):
    name: str = "whole_plant_conversion__plant__steam_boundary__added_dp_margin_ok__36cb21eac5ff1b89"
    version: str = "v0.1"

    CONSTRAINT_ID = "whole_plant_conversion__plant__steam_boundary__added_dp_margin_ok__36cb21eac5ff1b89"

    def run(self, margin_in: float) -> ModuleResult[PlantSteamBoundaryAddedDpMarginOkConstraintOutput]:
        PlantSteamBoundaryAddedDpMarginOkConstraintInput(margin_in=margin_in)  # validate every resolved formal
        body = constraint_pred_definition_component_alternatives_thermal__nonnegative_margin(margin_in=margin_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=PlantSteamBoundaryAddedDpMarginOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"margin_in": float(margin_in)},
                )
            )
        )
