"""Constraint module for stellarator_09_materials__rebco_material__fuel_processing_capacity_ok__4ccc57f69813cb74 (Item 7 / D2/D3/D9).

Effective predicate: stellarator_09_materials::rebco_material::fuel_processing_capacity_ok in owner instance stellarator_09_materials__rebco_material.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_rebco_tea.schemas.constraint_types import ConstraintEvaluation
from stellarator_materials_rebco_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_mfe_fuel_cycle__fuel_processing_capacity


class RebcoMaterialFuelProcessingCapacityOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    margin_in: float
    defined_in: float


class RebcoMaterialFuelProcessingCapacityOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class RebcoMaterialFuelProcessingCapacityOkConstraintModule(ModuleBase[RebcoMaterialFuelProcessingCapacityOkConstraintInput, RebcoMaterialFuelProcessingCapacityOkConstraintOutput]):
    name: str = "stellarator_09_materials__rebco_material__fuel_processing_capacity_ok__4ccc57f69813cb74"
    version: str = "v0.1"

    CONSTRAINT_ID = "stellarator_09_materials__rebco_material__fuel_processing_capacity_ok__4ccc57f69813cb74"

    def run(self, margin_in: float, defined_in: float) -> ModuleResult[RebcoMaterialFuelProcessingCapacityOkConstraintOutput]:
        RebcoMaterialFuelProcessingCapacityOkConstraintInput(margin_in=margin_in, defined_in=defined_in)  # validate every resolved formal
        body = constraint_pred_definition_mfe_fuel_cycle__fuel_processing_capacity(defined_in=defined_in, margin_in=margin_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=RebcoMaterialFuelProcessingCapacityOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"defined_in": float(defined_in), "margin_in": float(margin_in)},
                )
            )
        )
