"""Constraint module for combinations_lumped_fit__lumped_fit__pbli_fit__domain_ok__f30925cbe487ee4d (Item 7 / D2/D3/D9).

Effective predicate: combinations_lumped_fit::lumped_fit::pbli_fit::domain_ok in owner instance combinations_lumped_fit__lumped_fit__pbli_fit.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from combinations_tea.schemas.constraint_types import ConstraintEvaluation
from combinations_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_mfe_viability__cycle_fit_domain


class LumpedFitPbliFitDomainOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    domain_product_in: float


class LumpedFitPbliFitDomainOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class LumpedFitPbliFitDomainOkConstraintModule(ModuleBase[LumpedFitPbliFitDomainOkConstraintInput, LumpedFitPbliFitDomainOkConstraintOutput]):
    name: str = "combinations_lumped_fit__lumped_fit__pbli_fit__domain_ok__f30925cbe487ee4d"
    version: str = "v0.1"

    CONSTRAINT_ID = "combinations_lumped_fit__lumped_fit__pbli_fit__domain_ok__f30925cbe487ee4d"

    def run(self, domain_product_in: float) -> ModuleResult[LumpedFitPbliFitDomainOkConstraintOutput]:
        LumpedFitPbliFitDomainOkConstraintInput(domain_product_in=domain_product_in)  # validate every resolved formal
        body = constraint_pred_definition_mfe_viability__cycle_fit_domain(domain_product_in=domain_product_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=LumpedFitPbliFitDomainOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"domain_product_in": float(domain_product_in)},
                )
            )
        )
