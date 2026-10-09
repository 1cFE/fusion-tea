"""Constraint module for stellarator_09_materials__nb3sn_material__facility_occupancy_ok__e81ea8f8cf26823a (Item 7 / D2/D3/D9).

Effective predicate: mfe_plant::'MFE Power Plant'::facility_occupancy_ok in owner instance stellarator_09_materials__nb3sn_material.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_nb3sn_tea.schemas.constraint_types import ConstraintEvaluation
from stellarator_materials_nb3sn_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_mfe_facilities__facility_nonnegative_margin


class Nb3snMaterialFacilityOccupancyOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    margin_in: float


class Nb3snMaterialFacilityOccupancyOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class Nb3snMaterialFacilityOccupancyOkConstraintModule(ModuleBase[Nb3snMaterialFacilityOccupancyOkConstraintInput, Nb3snMaterialFacilityOccupancyOkConstraintOutput]):
    name: str = "stellarator_09_materials__nb3sn_material__facility_occupancy_ok__e81ea8f8cf26823a"
    version: str = "v0.1"

    CONSTRAINT_ID = "stellarator_09_materials__nb3sn_material__facility_occupancy_ok__e81ea8f8cf26823a"

    def run(self, margin_in: float) -> ModuleResult[Nb3snMaterialFacilityOccupancyOkConstraintOutput]:
        Nb3snMaterialFacilityOccupancyOkConstraintInput(margin_in=margin_in)  # validate every resolved formal
        body = constraint_pred_definition_mfe_facilities__facility_nonnegative_margin(margin_in=margin_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=Nb3snMaterialFacilityOccupancyOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"margin_in": float(margin_in)},
                )
            )
        )
