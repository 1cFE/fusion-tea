"""Constraint module for whole_plant_conversion__plant__steam_feed_flow_capacity__capacity_requirement__5d9d76d0749190a1 (Item 7 / D2/D3/D9).

Effective predicate: whole_plant_conversion::plant::steam_feed_flow_capacity::capacity_requirement in owner instance whole_plant_conversion__plant__steam_feed_flow_capacity.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from whole_plant_conversion_tea.schemas.constraint_types import ConstraintEvaluation
from whole_plant_conversion_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_mfe_viability__offered_equipment_capacity


class PlantSteamFeedFlowCapacityCapacityRequirementConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    margin_in: float
    defined_in: float


class PlantSteamFeedFlowCapacityCapacityRequirementConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class PlantSteamFeedFlowCapacityCapacityRequirementConstraintModule(ModuleBase[PlantSteamFeedFlowCapacityCapacityRequirementConstraintInput, PlantSteamFeedFlowCapacityCapacityRequirementConstraintOutput]):
    name: str = "whole_plant_conversion__plant__steam_feed_flow_capacity__capacity_requirement__5d9d76d0749190a1"
    version: str = "v0.1"

    CONSTRAINT_ID = "whole_plant_conversion__plant__steam_feed_flow_capacity__capacity_requirement__5d9d76d0749190a1"

    def run(self, margin_in: float, defined_in: float) -> ModuleResult[PlantSteamFeedFlowCapacityCapacityRequirementConstraintOutput]:
        PlantSteamFeedFlowCapacityCapacityRequirementConstraintInput(margin_in=margin_in, defined_in=defined_in)  # validate every resolved formal
        body = constraint_pred_definition_mfe_viability__offered_equipment_capacity(defined_in=defined_in, margin_in=margin_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=PlantSteamFeedFlowCapacityCapacityRequirementConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"defined_in": float(defined_in), "margin_in": float(margin_in)},
                )
            )
        )
