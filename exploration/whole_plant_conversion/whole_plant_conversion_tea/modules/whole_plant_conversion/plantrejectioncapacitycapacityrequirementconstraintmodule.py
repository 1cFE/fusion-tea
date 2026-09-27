"""Constraint module for whole_plant_conversion__plant__rejection_capacity__capacity_requirement__af7714dda178b8f0 (Item 7 / D2/D3/D9).

Effective predicate: whole_plant_conversion::plant::rejection_capacity::capacity_requirement in owner instance whole_plant_conversion__plant__rejection_capacity.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from whole_plant_conversion_tea.schemas.constraint_types import ConstraintEvaluation
from whole_plant_conversion_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_mfe_viability__offered_equipment_capacity


class PlantRejectionCapacityCapacityRequirementConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    margin_in: float
    defined_in: float


class PlantRejectionCapacityCapacityRequirementConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class PlantRejectionCapacityCapacityRequirementConstraintModule(ModuleBase[PlantRejectionCapacityCapacityRequirementConstraintInput, PlantRejectionCapacityCapacityRequirementConstraintOutput]):
    name: str = "whole_plant_conversion__plant__rejection_capacity__capacity_requirement__af7714dda178b8f0"
    version: str = "v0.1"

    CONSTRAINT_ID = "whole_plant_conversion__plant__rejection_capacity__capacity_requirement__af7714dda178b8f0"

    def run(self, margin_in: float, defined_in: float) -> ModuleResult[PlantRejectionCapacityCapacityRequirementConstraintOutput]:
        PlantRejectionCapacityCapacityRequirementConstraintInput(margin_in=margin_in, defined_in=defined_in)  # validate every resolved formal
        body = constraint_pred_definition_mfe_viability__offered_equipment_capacity(defined_in=defined_in, margin_in=margin_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=PlantRejectionCapacityCapacityRequirementConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"defined_in": float(defined_in), "margin_in": float(margin_in)},
                )
            )
        )
