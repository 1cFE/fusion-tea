"""Constraint module for combinations_loop_brayton__loop_brayton__checks__loop_capacity_ok__42cc45f771fa6628 (Item 7 / D2/D3/D9).

Effective predicate: combinations_loop_brayton::loop_brayton::checks::loop_capacity_ok in owner instance combinations_loop_brayton__loop_brayton__checks.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from combinations_tea.schemas.constraint_types import ConstraintEvaluation
from combinations_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_mfe_viability__loop_capacity


class LoopBraytonChecksLoopCapacityOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    mdot_loop_rated_in: float
    mdot_loop_in: float


class LoopBraytonChecksLoopCapacityOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class LoopBraytonChecksLoopCapacityOkConstraintModule(ModuleBase[LoopBraytonChecksLoopCapacityOkConstraintInput, LoopBraytonChecksLoopCapacityOkConstraintOutput]):
    name: str = "combinations_loop_brayton__loop_brayton__checks__loop_capacity_ok__42cc45f771fa6628"
    version: str = "v0.1"

    CONSTRAINT_ID = "combinations_loop_brayton__loop_brayton__checks__loop_capacity_ok__42cc45f771fa6628"

    def run(self, mdot_loop_rated_in: float, mdot_loop_in: float) -> ModuleResult[LoopBraytonChecksLoopCapacityOkConstraintOutput]:
        LoopBraytonChecksLoopCapacityOkConstraintInput(mdot_loop_rated_in=mdot_loop_rated_in, mdot_loop_in=mdot_loop_in)  # validate every resolved formal
        body = constraint_pred_definition_mfe_viability__loop_capacity(mdot_loop_in=mdot_loop_in, mdot_loop_rated_in=mdot_loop_rated_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=LoopBraytonChecksLoopCapacityOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"mdot_loop_in": float(mdot_loop_in), "mdot_loop_rated_in": float(mdot_loop_rated_in)},
                )
            )
        )
