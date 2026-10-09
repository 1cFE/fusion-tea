"""Constraint module for stellarator_09_materials__rebco_material__wall_load_ok__bb886accb1fe4358 (Item 7 / D2/D3/D9).

Effective predicate: stellarator_09_materials::rebco_material::wall_load_ok in owner instance stellarator_09_materials__rebco_material.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_rebco_tea.schemas.constraint_types import ConstraintEvaluation
from stellarator_materials_rebco_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_mfe_viability__neutron_wall_load_limit


class RebcoMaterialWallLoadOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    wall_load: float
    wall_load_limit_in: float


class RebcoMaterialWallLoadOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class RebcoMaterialWallLoadOkConstraintModule(ModuleBase[RebcoMaterialWallLoadOkConstraintInput, RebcoMaterialWallLoadOkConstraintOutput]):
    name: str = "stellarator_09_materials__rebco_material__wall_load_ok__bb886accb1fe4358"
    version: str = "v0.1"

    CONSTRAINT_ID = "stellarator_09_materials__rebco_material__wall_load_ok__bb886accb1fe4358"

    def run(self, wall_load: float, wall_load_limit_in: float) -> ModuleResult[RebcoMaterialWallLoadOkConstraintOutput]:
        RebcoMaterialWallLoadOkConstraintInput(wall_load=wall_load, wall_load_limit_in=wall_load_limit_in)  # validate every resolved formal
        body = constraint_pred_definition_mfe_viability__neutron_wall_load_limit(wall_load=wall_load, wall_load_limit_in=wall_load_limit_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=RebcoMaterialWallLoadOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"wall_load": float(wall_load), "wall_load_limit_in": float(wall_load_limit_in)},
                )
            )
        )
