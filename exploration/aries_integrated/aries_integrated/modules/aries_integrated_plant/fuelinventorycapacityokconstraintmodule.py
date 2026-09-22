"""Constraint module for aries_integrated_plant__fuel_inventory__capacity_ok__37f4667fbfb616d0 (Item 7 / D2/D3/D9).

Effective predicate: aries_integrated_plant::fuel_inventory::capacity_ok in owner instance aries_integrated_plant__fuel_inventory.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from aries_integrated.schemas.constraint_types import ConstraintEvaluation
from aries_integrated.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_mfe_viability__offered_equipment_capacity


class FuelInventoryCapacityOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    margin_in: float
    defined_in: float


class FuelInventoryCapacityOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class FuelInventoryCapacityOkConstraintModule(ModuleBase[FuelInventoryCapacityOkConstraintInput, FuelInventoryCapacityOkConstraintOutput]):
    name: str = "aries_integrated_plant__fuel_inventory__capacity_ok__37f4667fbfb616d0"
    version: str = "v0.1"

    CONSTRAINT_ID = "aries_integrated_plant__fuel_inventory__capacity_ok__37f4667fbfb616d0"

    def run(self, margin_in: float, defined_in: float) -> ModuleResult[FuelInventoryCapacityOkConstraintOutput]:
        FuelInventoryCapacityOkConstraintInput(margin_in=margin_in, defined_in=defined_in)  # validate every resolved formal
        body = constraint_pred_definition_mfe_viability__offered_equipment_capacity(defined_in=defined_in, margin_in=margin_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=FuelInventoryCapacityOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"defined_in": float(defined_in), "margin_in": float(margin_in)},
                )
            )
        )
