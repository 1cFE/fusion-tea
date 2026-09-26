"""Constraint module for combinations_loop_brayton__loop_brayton__rejection_capacity__capacity_ok__f641e3674fbef65a (Item 7 / D2/D3/D9).

Effective predicate: combinations_loop_brayton::loop_brayton::rejection_capacity::capacity_ok in owner instance combinations_loop_brayton__loop_brayton__rejection_capacity.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from combinations_tea.schemas.constraint_types import ConstraintEvaluation
from combinations_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_mfe_viability__offered_equipment_capacity


class LoopBraytonRejectionCapacityCapacityOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    margin_in: float
    defined_in: float


class LoopBraytonRejectionCapacityCapacityOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class LoopBraytonRejectionCapacityCapacityOkConstraintModule(ModuleBase[LoopBraytonRejectionCapacityCapacityOkConstraintInput, LoopBraytonRejectionCapacityCapacityOkConstraintOutput]):
    name: str = "combinations_loop_brayton__loop_brayton__rejection_capacity__capacity_ok__f641e3674fbef65a"
    version: str = "v0.1"

    CONSTRAINT_ID = "combinations_loop_brayton__loop_brayton__rejection_capacity__capacity_ok__f641e3674fbef65a"

    def run(self, margin_in: float, defined_in: float) -> ModuleResult[LoopBraytonRejectionCapacityCapacityOkConstraintOutput]:
        LoopBraytonRejectionCapacityCapacityOkConstraintInput(margin_in=margin_in, defined_in=defined_in)  # validate every resolved formal
        body = constraint_pred_definition_mfe_viability__offered_equipment_capacity(defined_in=defined_in, margin_in=margin_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=LoopBraytonRejectionCapacityCapacityOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"defined_in": float(defined_in), "margin_in": float(margin_in)},
                )
            )
        )
