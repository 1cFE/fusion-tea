"""Constraint module for stellarator_09_materials__rebco_material__facility_capacity_ok__c0747ad3c5d93311 (Item 7 / D2/D3/D9).

Effective predicate: mfe_plant::'MFE Power Plant'::facility_capacity_ok in owner instance stellarator_09_materials__rebco_material.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_rebco_tea.schemas.constraint_types import ConstraintEvaluation
from stellarator_materials_rebco_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_mfe_facilities__facility_nonnegative_margin


class RebcoMaterialFacilityCapacityOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    margin_in: float


class RebcoMaterialFacilityCapacityOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class RebcoMaterialFacilityCapacityOkConstraintModule(ModuleBase[RebcoMaterialFacilityCapacityOkConstraintInput, RebcoMaterialFacilityCapacityOkConstraintOutput]):
    name: str = "stellarator_09_materials__rebco_material__facility_capacity_ok__c0747ad3c5d93311"
    version: str = "v0.1"

    CONSTRAINT_ID = "stellarator_09_materials__rebco_material__facility_capacity_ok__c0747ad3c5d93311"

    def run(self, margin_in: float) -> ModuleResult[RebcoMaterialFacilityCapacityOkConstraintOutput]:
        RebcoMaterialFacilityCapacityOkConstraintInput(margin_in=margin_in)  # validate every resolved formal
        body = constraint_pred_definition_mfe_facilities__facility_nonnegative_margin(margin_in=margin_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=RebcoMaterialFacilityCapacityOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"margin_in": float(margin_in)},
                )
            )
        )
