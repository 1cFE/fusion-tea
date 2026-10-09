"""Constraint module for stellarator_09_materials__nb3sn_material__fuel_processing_capacity_ok__d36667b777c42fe9 (Item 7 / D2/D3/D9).

Effective predicate: stellarator_09_materials::nb3sn_material::fuel_processing_capacity_ok in owner instance stellarator_09_materials__nb3sn_material.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_nb3sn_tea.schemas.constraint_types import ConstraintEvaluation
from stellarator_materials_nb3sn_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_mfe_fuel_cycle__fuel_processing_capacity


class Nb3snMaterialFuelProcessingCapacityOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    margin_in: float
    defined_in: float


class Nb3snMaterialFuelProcessingCapacityOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class Nb3snMaterialFuelProcessingCapacityOkConstraintModule(ModuleBase[Nb3snMaterialFuelProcessingCapacityOkConstraintInput, Nb3snMaterialFuelProcessingCapacityOkConstraintOutput]):
    name: str = "stellarator_09_materials__nb3sn_material__fuel_processing_capacity_ok__d36667b777c42fe9"
    version: str = "v0.1"

    CONSTRAINT_ID = "stellarator_09_materials__nb3sn_material__fuel_processing_capacity_ok__d36667b777c42fe9"

    def run(self, margin_in: float, defined_in: float) -> ModuleResult[Nb3snMaterialFuelProcessingCapacityOkConstraintOutput]:
        Nb3snMaterialFuelProcessingCapacityOkConstraintInput(margin_in=margin_in, defined_in=defined_in)  # validate every resolved formal
        body = constraint_pred_definition_mfe_fuel_cycle__fuel_processing_capacity(defined_in=defined_in, margin_in=margin_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=Nb3snMaterialFuelProcessingCapacityOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"defined_in": float(defined_in), "margin_in": float(margin_in)},
                )
            )
        )
