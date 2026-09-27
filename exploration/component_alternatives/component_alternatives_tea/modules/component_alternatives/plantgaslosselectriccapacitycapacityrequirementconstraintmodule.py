"""Constraint module for component_alternatives__plant__gas_loss_electric_capacity__capacity_requirement__6a158987313c84e0 (Item 7 / D2/D3/D9).

Effective predicate: component_alternatives::plant::gas_loss_electric_capacity::capacity_requirement in owner instance component_alternatives__plant__gas_loss_electric_capacity.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from component_alternatives_tea.schemas.constraint_types import ConstraintEvaluation
from component_alternatives_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_mfe_viability__offered_equipment_capacity


class PlantGasLossElectricCapacityCapacityRequirementConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    margin_in: float
    defined_in: float


class PlantGasLossElectricCapacityCapacityRequirementConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class PlantGasLossElectricCapacityCapacityRequirementConstraintModule(ModuleBase[PlantGasLossElectricCapacityCapacityRequirementConstraintInput, PlantGasLossElectricCapacityCapacityRequirementConstraintOutput]):
    name: str = "component_alternatives__plant__gas_loss_electric_capacity__capacity_requirement__6a158987313c84e0"
    version: str = "v0.1"

    CONSTRAINT_ID = "component_alternatives__plant__gas_loss_electric_capacity__capacity_requirement__6a158987313c84e0"

    def run(self, margin_in: float, defined_in: float) -> ModuleResult[PlantGasLossElectricCapacityCapacityRequirementConstraintOutput]:
        PlantGasLossElectricCapacityCapacityRequirementConstraintInput(margin_in=margin_in, defined_in=defined_in)  # validate every resolved formal
        body = constraint_pred_definition_mfe_viability__offered_equipment_capacity(defined_in=defined_in, margin_in=margin_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=PlantGasLossElectricCapacityCapacityRequirementConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"defined_in": float(defined_in), "margin_in": float(margin_in)},
                )
            )
        )
