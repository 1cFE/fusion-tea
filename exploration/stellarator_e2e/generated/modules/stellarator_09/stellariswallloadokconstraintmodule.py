"""Constraint module for stellarator_09__stellaris__wall_load_ok__ab2c790419af93bb (Item 7 / D2/D3/D9).

Effective predicate: stellarator_09::stellaris::wall_load_ok in owner instance stellarator_09__stellaris.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.schemas.constraint_types import ConstraintEvaluation
from stellarator_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_mfe_viability__neutron_wall_load_limit


class StellarisWallLoadOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    wall_load: float
    wall_load_limit: float


class StellarisWallLoadOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class StellarisWallLoadOkConstraintModule(ModuleBase[StellarisWallLoadOkConstraintInput, StellarisWallLoadOkConstraintOutput]):
    name: str = "stellarator_09__stellaris__wall_load_ok__ab2c790419af93bb"
    version: str = "v0.1"

    CONSTRAINT_ID = "stellarator_09__stellaris__wall_load_ok__ab2c790419af93bb"

    def run(self, wall_load: float, wall_load_limit: float) -> ModuleResult[StellarisWallLoadOkConstraintOutput]:
        StellarisWallLoadOkConstraintInput(wall_load=wall_load, wall_load_limit=wall_load_limit)  # validate every resolved formal
        body = constraint_pred_definition_mfe_viability__neutron_wall_load_limit(wall_load=wall_load, wall_load_limit=wall_load_limit)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=StellarisWallLoadOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"wall_load": float(wall_load), "wall_load_limit": float(wall_load_limit)},
                )
            )
        )
