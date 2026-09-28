"""Constraint module for costed_loop_brayton__plant__checks__loop_capacity_ok__9c561de0cd1f50b3 (Item 7 / D2/D3/D9).

Effective predicate: costed_loop_brayton::plant::checks::loop_capacity_ok in owner instance costed_loop_brayton__plant__checks.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from costed_loop_brayton_tea.schemas.constraint_types import ConstraintEvaluation
from costed_loop_brayton_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_mfe_viability__loop_capacity


class PlantChecksLoopCapacityOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    mdot_loop_rated_in: float
    mdot_loop_in: float


class PlantChecksLoopCapacityOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class PlantChecksLoopCapacityOkConstraintModule(ModuleBase[PlantChecksLoopCapacityOkConstraintInput, PlantChecksLoopCapacityOkConstraintOutput]):
    name: str = "costed_loop_brayton__plant__checks__loop_capacity_ok__9c561de0cd1f50b3"
    version: str = "v0.1"

    CONSTRAINT_ID = "costed_loop_brayton__plant__checks__loop_capacity_ok__9c561de0cd1f50b3"

    def run(self, mdot_loop_rated_in: float, mdot_loop_in: float) -> ModuleResult[PlantChecksLoopCapacityOkConstraintOutput]:
        PlantChecksLoopCapacityOkConstraintInput(mdot_loop_rated_in=mdot_loop_rated_in, mdot_loop_in=mdot_loop_in)  # validate every resolved formal
        body = constraint_pred_definition_mfe_viability__loop_capacity(mdot_loop_in=mdot_loop_in, mdot_loop_rated_in=mdot_loop_rated_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=PlantChecksLoopCapacityOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"mdot_loop_in": float(mdot_loop_in), "mdot_loop_rated_in": float(mdot_loop_rated_in)},
                )
            )
        )
