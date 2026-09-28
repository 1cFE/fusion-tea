"""Constraint module for whole_plant_conversion__plant__gas_loss_water__cooling_approach_ok_required__8223dadecc4964f5 (Item 7 / D2/D3/D9).

Effective predicate: whole_plant_conversion::plant::gas_loss_water::cooling_approach_ok_required in owner instance whole_plant_conversion__plant__gas_loss_water.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from whole_plant_conversion_tea.schemas.constraint_types import ConstraintEvaluation
from whole_plant_conversion_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_mfe_viability__offered_equipment_capacity


class PlantGasLossWaterCoolingApproachOkRequiredConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    margin_in: float
    defined_in: float


class PlantGasLossWaterCoolingApproachOkRequiredConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class PlantGasLossWaterCoolingApproachOkRequiredConstraintModule(ModuleBase[PlantGasLossWaterCoolingApproachOkRequiredConstraintInput, PlantGasLossWaterCoolingApproachOkRequiredConstraintOutput]):
    name: str = "whole_plant_conversion__plant__gas_loss_water__cooling_approach_ok_required__8223dadecc4964f5"
    version: str = "v0.1"

    CONSTRAINT_ID = "whole_plant_conversion__plant__gas_loss_water__cooling_approach_ok_required__8223dadecc4964f5"

    def run(self, margin_in: float, defined_in: float) -> ModuleResult[PlantGasLossWaterCoolingApproachOkRequiredConstraintOutput]:
        PlantGasLossWaterCoolingApproachOkRequiredConstraintInput(margin_in=margin_in, defined_in=defined_in)  # validate every resolved formal
        body = constraint_pred_definition_mfe_viability__offered_equipment_capacity(defined_in=defined_in, margin_in=margin_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=PlantGasLossWaterCoolingApproachOkRequiredConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"defined_in": float(defined_in), "margin_in": float(margin_in)},
                )
            )
        )
