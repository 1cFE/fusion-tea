"""Constraint module for combinations_loop_brayton__loop_brayton__checks__heat_removal_ok__c7a2f9638fd1e56b (Item 7 / D2/D3/D9).

Effective predicate: combinations_loop_brayton::loop_brayton::checks::heat_removal_ok in owner instance combinations_loop_brayton__loop_brayton__checks.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from combinations_tea.schemas.constraint_types import ConstraintEvaluation
from combinations_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_integrated_heat_electricity__heat_removal_adequate


class LoopBraytonChecksHeatRemovalOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    tolerance_in: float
    unmet_in: float


class LoopBraytonChecksHeatRemovalOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class LoopBraytonChecksHeatRemovalOkConstraintModule(ModuleBase[LoopBraytonChecksHeatRemovalOkConstraintInput, LoopBraytonChecksHeatRemovalOkConstraintOutput]):
    name: str = "combinations_loop_brayton__loop_brayton__checks__heat_removal_ok__c7a2f9638fd1e56b"
    version: str = "v0.1"

    CONSTRAINT_ID = "combinations_loop_brayton__loop_brayton__checks__heat_removal_ok__c7a2f9638fd1e56b"

    def run(self, tolerance_in: float, unmet_in: float) -> ModuleResult[LoopBraytonChecksHeatRemovalOkConstraintOutput]:
        LoopBraytonChecksHeatRemovalOkConstraintInput(tolerance_in=tolerance_in, unmet_in=unmet_in)  # validate every resolved formal
        body = constraint_pred_definition_integrated_heat_electricity__heat_removal_adequate(unmet_in=unmet_in, tolerance_in=tolerance_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=LoopBraytonChecksHeatRemovalOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"unmet_in": float(unmet_in), "tolerance_in": float(tolerance_in)},
                )
            )
        )
