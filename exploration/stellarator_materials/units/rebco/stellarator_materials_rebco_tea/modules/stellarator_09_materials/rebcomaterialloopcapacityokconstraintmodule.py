"""Constraint module for stellarator_09_materials__rebco_material__loop_capacity_ok__d6532a89816fb7e2 (Item 7 / D2/D3/D9).

Effective predicate: mfe_plant::'MFE Power Plant'::loop_capacity_ok in owner instance stellarator_09_materials__rebco_material.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_rebco_tea.schemas.constraint_types import ConstraintEvaluation
from stellarator_materials_rebco_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_mfe_viability__loop_capacity


class RebcoMaterialLoopCapacityOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    mdot_loop_rated_in: float
    mdot_loop_in: float


class RebcoMaterialLoopCapacityOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class RebcoMaterialLoopCapacityOkConstraintModule(ModuleBase[RebcoMaterialLoopCapacityOkConstraintInput, RebcoMaterialLoopCapacityOkConstraintOutput]):
    name: str = "stellarator_09_materials__rebco_material__loop_capacity_ok__d6532a89816fb7e2"
    version: str = "v0.1"

    CONSTRAINT_ID = "stellarator_09_materials__rebco_material__loop_capacity_ok__d6532a89816fb7e2"

    def run(self, mdot_loop_rated_in: float, mdot_loop_in: float) -> ModuleResult[RebcoMaterialLoopCapacityOkConstraintOutput]:
        RebcoMaterialLoopCapacityOkConstraintInput(mdot_loop_rated_in=mdot_loop_rated_in, mdot_loop_in=mdot_loop_in)  # validate every resolved formal
        body = constraint_pred_definition_mfe_viability__loop_capacity(mdot_loop_in=mdot_loop_in, mdot_loop_rated_in=mdot_loop_rated_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=RebcoMaterialLoopCapacityOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"mdot_loop_in": float(mdot_loop_in), "mdot_loop_rated_in": float(mdot_loop_rated_in)},
                )
            )
        )
