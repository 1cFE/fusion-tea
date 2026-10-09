"""Constraint module for stellarator_09_materials__nb3sn_material__facility_geometry_ok__14b78dfe909c8501 (Item 7 / D2/D3/D9).

Effective predicate: mfe_plant::'MFE Power Plant'::facility_geometry_ok in owner instance stellarator_09_materials__nb3sn_material.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_nb3sn_tea.schemas.constraint_types import ConstraintEvaluation
from stellarator_materials_nb3sn_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_mfe_facilities__facility_nonnegative_margin


class Nb3snMaterialFacilityGeometryOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    margin_in: float


class Nb3snMaterialFacilityGeometryOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class Nb3snMaterialFacilityGeometryOkConstraintModule(ModuleBase[Nb3snMaterialFacilityGeometryOkConstraintInput, Nb3snMaterialFacilityGeometryOkConstraintOutput]):
    name: str = "stellarator_09_materials__nb3sn_material__facility_geometry_ok__14b78dfe909c8501"
    version: str = "v0.1"

    CONSTRAINT_ID = "stellarator_09_materials__nb3sn_material__facility_geometry_ok__14b78dfe909c8501"

    def run(self, margin_in: float) -> ModuleResult[Nb3snMaterialFacilityGeometryOkConstraintOutput]:
        Nb3snMaterialFacilityGeometryOkConstraintInput(margin_in=margin_in)  # validate every resolved formal
        body = constraint_pred_definition_mfe_facilities__facility_nonnegative_margin(margin_in=margin_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=Nb3snMaterialFacilityGeometryOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"margin_in": float(margin_in)},
                )
            )
        )
