"""Constraint module for stellarator_09_materials__nb3sn_material__loop_capacity_ok__a12ef69878182648 (Item 7 / D2/D3/D9).

Effective predicate: mfe_plant::'MFE Power Plant'::loop_capacity_ok in owner instance stellarator_09_materials__nb3sn_material.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_nb3sn_tea.schemas.constraint_types import ConstraintEvaluation
from stellarator_materials_nb3sn_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_mfe_viability__loop_capacity


class Nb3snMaterialLoopCapacityOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    mdot_loop_rated_in: float
    mdot_loop_in: float


class Nb3snMaterialLoopCapacityOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class Nb3snMaterialLoopCapacityOkConstraintModule(ModuleBase[Nb3snMaterialLoopCapacityOkConstraintInput, Nb3snMaterialLoopCapacityOkConstraintOutput]):
    name: str = "stellarator_09_materials__nb3sn_material__loop_capacity_ok__a12ef69878182648"
    version: str = "v0.1"

    CONSTRAINT_ID = "stellarator_09_materials__nb3sn_material__loop_capacity_ok__a12ef69878182648"

    def run(self, mdot_loop_rated_in: float, mdot_loop_in: float) -> ModuleResult[Nb3snMaterialLoopCapacityOkConstraintOutput]:
        Nb3snMaterialLoopCapacityOkConstraintInput(mdot_loop_rated_in=mdot_loop_rated_in, mdot_loop_in=mdot_loop_in)  # validate every resolved formal
        body = constraint_pred_definition_mfe_viability__loop_capacity(mdot_loop_in=mdot_loop_in, mdot_loop_rated_in=mdot_loop_rated_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=Nb3snMaterialLoopCapacityOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"mdot_loop_in": float(mdot_loop_in), "mdot_loop_rated_in": float(mdot_loop_rated_in)},
                )
            )
        )
