"""Constraint module for stellarator_09_materials__nb3sn_material__magnet__ampere_floor_ok__bbe387e1eb85f9b9 (Item 7 / D2/D3/D9).

Effective predicate: magnet_material_variants::'Nb3Sn Magnet System'::ampere_floor_ok in owner instance stellarator_09_materials__nb3sn_material__magnet.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_nb3sn_tea.schemas.constraint_types import ConstraintEvaluation
from stellarator_materials_nb3sn_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_magnet_material_variants__ampere_floor


class Nb3snMaterialMagnetAmpereFloorOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    margin_in: float


class Nb3snMaterialMagnetAmpereFloorOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class Nb3snMaterialMagnetAmpereFloorOkConstraintModule(ModuleBase[Nb3snMaterialMagnetAmpereFloorOkConstraintInput, Nb3snMaterialMagnetAmpereFloorOkConstraintOutput]):
    name: str = "stellarator_09_materials__nb3sn_material__magnet__ampere_floor_ok__bbe387e1eb85f9b9"
    version: str = "v0.1"

    CONSTRAINT_ID = "stellarator_09_materials__nb3sn_material__magnet__ampere_floor_ok__bbe387e1eb85f9b9"

    def run(self, margin_in: float) -> ModuleResult[Nb3snMaterialMagnetAmpereFloorOkConstraintOutput]:
        Nb3snMaterialMagnetAmpereFloorOkConstraintInput(margin_in=margin_in)  # validate every resolved formal
        body = constraint_pred_definition_magnet_material_variants__ampere_floor(margin_in=margin_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=Nb3snMaterialMagnetAmpereFloorOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"margin_in": float(margin_in)},
                )
            )
        )
