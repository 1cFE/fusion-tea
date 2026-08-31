"""Constraint module for stellarator_09__stellaris__wp_stress_ok__f38a102195da1dd0 (Item 7 / D2/D3/D9).

Effective predicate: mfe_plant::'MFE Power Plant'::wp_stress_ok in owner instance stellarator_09__stellaris.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.schemas.constraint_types import ConstraintEvaluation
from stellarator_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_mfe_viability__winding_pack_stress_limit


class StellarisWpStressOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    sigma_in: float
    sigma_allow_in: float


class StellarisWpStressOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class StellarisWpStressOkConstraintModule(ModuleBase[StellarisWpStressOkConstraintInput, StellarisWpStressOkConstraintOutput]):
    name: str = "stellarator_09__stellaris__wp_stress_ok__f38a102195da1dd0"
    version: str = "v0.1"

    CONSTRAINT_ID = "stellarator_09__stellaris__wp_stress_ok__f38a102195da1dd0"

    def run(self, sigma_in: float, sigma_allow_in: float) -> ModuleResult[StellarisWpStressOkConstraintOutput]:
        StellarisWpStressOkConstraintInput(sigma_in=sigma_in, sigma_allow_in=sigma_allow_in)  # validate every resolved formal
        body = constraint_pred_definition_mfe_viability__winding_pack_stress_limit(sigma_in=sigma_in, sigma_allow_in=sigma_allow_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=StellarisWpStressOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"sigma_in": float(sigma_in), "sigma_allow_in": float(sigma_allow_in)},
                )
            )
        )
