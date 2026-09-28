"""Constraint module for costed_loop_brayton__plant__checks__bypass_within_limit__b98df08f1f21c757 (Item 7 / D2/D3/D9).

Effective predicate: costed_loop_brayton::plant::checks::bypass_within_limit in owner instance costed_loop_brayton__plant__checks.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from costed_loop_brayton_tea.schemas.constraint_types import ConstraintEvaluation
from costed_loop_brayton_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_loop_return_control__bypass_within_limit


class PlantChecksBypassWithinLimitConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    max_bypass_in: float
    bypass_fraction_in: float


class PlantChecksBypassWithinLimitConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class PlantChecksBypassWithinLimitConstraintModule(ModuleBase[PlantChecksBypassWithinLimitConstraintInput, PlantChecksBypassWithinLimitConstraintOutput]):
    name: str = "costed_loop_brayton__plant__checks__bypass_within_limit__b98df08f1f21c757"
    version: str = "v0.1"

    CONSTRAINT_ID = "costed_loop_brayton__plant__checks__bypass_within_limit__b98df08f1f21c757"

    def run(self, max_bypass_in: float, bypass_fraction_in: float) -> ModuleResult[PlantChecksBypassWithinLimitConstraintOutput]:
        PlantChecksBypassWithinLimitConstraintInput(max_bypass_in=max_bypass_in, bypass_fraction_in=bypass_fraction_in)  # validate every resolved formal
        body = constraint_pred_definition_loop_return_control__bypass_within_limit(bypass_fraction_in=bypass_fraction_in, max_bypass_in=max_bypass_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=PlantChecksBypassWithinLimitConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"bypass_fraction_in": float(bypass_fraction_in), "max_bypass_in": float(max_bypass_in)},
                )
            )
        )
