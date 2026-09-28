"""Constraint module for whole_plant_conversion__plant__steam_boundary__source_adequate_ok__d29edbaf0da24311 (Item 7 / D2/D3/D9).

Effective predicate: whole_plant_conversion::plant::steam_boundary::source_adequate_ok in owner instance whole_plant_conversion__plant__steam_boundary.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from whole_plant_conversion_tea.schemas.constraint_types import ConstraintEvaluation
from whole_plant_conversion_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_component_alternatives_thermal__required_flag


class PlantSteamBoundarySourceAdequateOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    flag_in: float


class PlantSteamBoundarySourceAdequateOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class PlantSteamBoundarySourceAdequateOkConstraintModule(ModuleBase[PlantSteamBoundarySourceAdequateOkConstraintInput, PlantSteamBoundarySourceAdequateOkConstraintOutput]):
    name: str = "whole_plant_conversion__plant__steam_boundary__source_adequate_ok__d29edbaf0da24311"
    version: str = "v0.1"

    CONSTRAINT_ID = "whole_plant_conversion__plant__steam_boundary__source_adequate_ok__d29edbaf0da24311"

    def run(self, flag_in: float) -> ModuleResult[PlantSteamBoundarySourceAdequateOkConstraintOutput]:
        PlantSteamBoundarySourceAdequateOkConstraintInput(flag_in=flag_in)  # validate every resolved formal
        body = constraint_pred_definition_component_alternatives_thermal__required_flag(flag_in=flag_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=PlantSteamBoundarySourceAdequateOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"flag_in": float(flag_in)},
                )
            )
        )
