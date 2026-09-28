"""Constraint module for combinations_loop_brayton__loop_brayton__checks__net_positive__d22e3a3d83be3d66 (Item 7 / D2/D3/D9).

Effective predicate: combinations_loop_brayton::loop_brayton::checks::net_positive in owner instance combinations_loop_brayton__loop_brayton__checks.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from combinations_tea.schemas.constraint_types import ConstraintEvaluation
from combinations_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_mfe_viability__net_power_positive


class LoopBraytonChecksNetPositiveConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    net_electric: float


class LoopBraytonChecksNetPositiveConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class LoopBraytonChecksNetPositiveConstraintModule(ModuleBase[LoopBraytonChecksNetPositiveConstraintInput, LoopBraytonChecksNetPositiveConstraintOutput]):
    name: str = "combinations_loop_brayton__loop_brayton__checks__net_positive__d22e3a3d83be3d66"
    version: str = "v0.1"

    CONSTRAINT_ID = "combinations_loop_brayton__loop_brayton__checks__net_positive__d22e3a3d83be3d66"

    def run(self, net_electric: float) -> ModuleResult[LoopBraytonChecksNetPositiveConstraintOutput]:
        LoopBraytonChecksNetPositiveConstraintInput(net_electric=net_electric)  # validate every resolved formal
        body = constraint_pred_definition_mfe_viability__net_power_positive(net_electric=net_electric)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=LoopBraytonChecksNetPositiveConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"net_electric": float(net_electric)},
                )
            )
        )
