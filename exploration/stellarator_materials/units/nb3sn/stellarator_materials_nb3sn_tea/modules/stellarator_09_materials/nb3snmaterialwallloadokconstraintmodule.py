"""Constraint module for stellarator_09_materials__nb3sn_material__wall_load_ok__41289e190845d753 (Item 7 / D2/D3/D9).

Effective predicate: stellarator_09_materials::nb3sn_material::wall_load_ok in owner instance stellarator_09_materials__nb3sn_material.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_nb3sn_tea.schemas.constraint_types import ConstraintEvaluation
from stellarator_materials_nb3sn_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_mfe_viability__neutron_wall_load_limit


class Nb3snMaterialWallLoadOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    wall_load: float
    wall_load_limit_in: float


class Nb3snMaterialWallLoadOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class Nb3snMaterialWallLoadOkConstraintModule(ModuleBase[Nb3snMaterialWallLoadOkConstraintInput, Nb3snMaterialWallLoadOkConstraintOutput]):
    name: str = "stellarator_09_materials__nb3sn_material__wall_load_ok__41289e190845d753"
    version: str = "v0.1"

    CONSTRAINT_ID = "stellarator_09_materials__nb3sn_material__wall_load_ok__41289e190845d753"

    def run(self, wall_load: float, wall_load_limit_in: float) -> ModuleResult[Nb3snMaterialWallLoadOkConstraintOutput]:
        Nb3snMaterialWallLoadOkConstraintInput(wall_load=wall_load, wall_load_limit_in=wall_load_limit_in)  # validate every resolved formal
        body = constraint_pred_definition_mfe_viability__neutron_wall_load_limit(wall_load=wall_load, wall_load_limit_in=wall_load_limit_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=Nb3snMaterialWallLoadOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"wall_load": float(wall_load), "wall_load_limit_in": float(wall_load_limit_in)},
                )
            )
        )
