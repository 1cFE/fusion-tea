"""Constraint module for stellarator_09__stellaris__beta_ok__82b78aad420730d5 (Item 7 / D2/D3/D9).

Effective predicate: stellarator_09::stellaris::beta_ok in owner instance stellarator_09__stellaris.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.schemas.constraint_types import ConstraintEvaluation
from stellarator_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_mfe_viability__beta_limit


class StellarisBetaOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    beta_in: float
    beta_limit_in: float


class StellarisBetaOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class StellarisBetaOkConstraintModule(ModuleBase[StellarisBetaOkConstraintInput, StellarisBetaOkConstraintOutput]):
    name: str = "stellarator_09__stellaris__beta_ok__82b78aad420730d5"
    version: str = "v0.1"

    CONSTRAINT_ID = "stellarator_09__stellaris__beta_ok__82b78aad420730d5"

    def run(self, beta_in: float, beta_limit_in: float) -> ModuleResult[StellarisBetaOkConstraintOutput]:
        StellarisBetaOkConstraintInput(beta_in=beta_in, beta_limit_in=beta_limit_in)  # validate every resolved formal
        body = constraint_pred_definition_mfe_viability__beta_limit(beta_in=beta_in, beta_limit_in=beta_limit_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=StellarisBetaOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"beta_in": float(beta_in), "beta_limit_in": float(beta_limit_in)},
                )
            )
        )
