"""Constraint module for component_alternatives__plant__steam_reheat_ua_capacity__capacity_requirement__ff5775187764fbbd (Item 7 / D2/D3/D9).

Effective predicate: component_alternatives::plant::steam_reheat_ua_capacity::capacity_requirement in owner instance component_alternatives__plant__steam_reheat_ua_capacity.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from component_alternatives_tea.schemas.constraint_types import ConstraintEvaluation
from component_alternatives_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_mfe_viability__offered_equipment_capacity


class PlantSteamReheatUaCapacityCapacityRequirementConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    margin_in: float
    defined_in: float


class PlantSteamReheatUaCapacityCapacityRequirementConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class PlantSteamReheatUaCapacityCapacityRequirementConstraintModule(ModuleBase[PlantSteamReheatUaCapacityCapacityRequirementConstraintInput, PlantSteamReheatUaCapacityCapacityRequirementConstraintOutput]):
    name: str = "component_alternatives__plant__steam_reheat_ua_capacity__capacity_requirement__ff5775187764fbbd"
    version: str = "v0.1"

    CONSTRAINT_ID = "component_alternatives__plant__steam_reheat_ua_capacity__capacity_requirement__ff5775187764fbbd"

    def run(self, margin_in: float, defined_in: float) -> ModuleResult[PlantSteamReheatUaCapacityCapacityRequirementConstraintOutput]:
        PlantSteamReheatUaCapacityCapacityRequirementConstraintInput(margin_in=margin_in, defined_in=defined_in)  # validate every resolved formal
        body = constraint_pred_definition_mfe_viability__offered_equipment_capacity(defined_in=defined_in, margin_in=margin_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=PlantSteamReheatUaCapacityCapacityRequirementConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"defined_in": float(defined_in), "margin_in": float(margin_in)},
                )
            )
        )
