"""Constraint module for whole_plant_conversion__plant__steam_boundary__controller_capacity_ok_ok__f143197b782aea8e (Item 7 / D2/D3/D9).

Effective predicate: whole_plant_conversion::plant::steam_boundary::controller_capacity_ok_ok in owner instance whole_plant_conversion__plant__steam_boundary.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from whole_plant_conversion_tea.schemas.constraint_types import ConstraintEvaluation
from whole_plant_conversion_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_component_alternatives_thermal__required_flag


class PlantSteamBoundaryControllerCapacityOkOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    flag_in: float


class PlantSteamBoundaryControllerCapacityOkOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class PlantSteamBoundaryControllerCapacityOkOkConstraintModule(ModuleBase[PlantSteamBoundaryControllerCapacityOkOkConstraintInput, PlantSteamBoundaryControllerCapacityOkOkConstraintOutput]):
    name: str = "whole_plant_conversion__plant__steam_boundary__controller_capacity_ok_ok__f143197b782aea8e"
    version: str = "v0.1"

    CONSTRAINT_ID = "whole_plant_conversion__plant__steam_boundary__controller_capacity_ok_ok__f143197b782aea8e"

    def run(self, flag_in: float) -> ModuleResult[PlantSteamBoundaryControllerCapacityOkOkConstraintOutput]:
        PlantSteamBoundaryControllerCapacityOkOkConstraintInput(flag_in=flag_in)  # validate every resolved formal
        body = constraint_pred_definition_component_alternatives_thermal__required_flag(flag_in=flag_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=PlantSteamBoundaryControllerCapacityOkOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"flag_in": float(flag_in)},
                )
            )
        )
