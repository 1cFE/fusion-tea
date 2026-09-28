"""Constraint module for stellarator_09__stellaris__sustainment_ok__77add152ed8eafce (Item 7 / D2/D3/D9).

Effective predicate: stellarator_09::stellaris::sustainment_ok in owner instance stellarator_09__stellaris.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.schemas.constraint_types import ConstraintEvaluation
from stellarator_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_mfe_viability__sustainment_limit


class StellarisSustainmentOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    p_aux_required_in: float
    p_aux_installed_in: float


class StellarisSustainmentOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class StellarisSustainmentOkConstraintModule(ModuleBase[StellarisSustainmentOkConstraintInput, StellarisSustainmentOkConstraintOutput]):
    name: str = "stellarator_09__stellaris__sustainment_ok__77add152ed8eafce"
    version: str = "v0.1"

    CONSTRAINT_ID = "stellarator_09__stellaris__sustainment_ok__77add152ed8eafce"

    def run(self, p_aux_required_in: float, p_aux_installed_in: float) -> ModuleResult[StellarisSustainmentOkConstraintOutput]:
        StellarisSustainmentOkConstraintInput(p_aux_required_in=p_aux_required_in, p_aux_installed_in=p_aux_installed_in)  # validate every resolved formal
        body = constraint_pred_definition_mfe_viability__sustainment_limit(p_aux_required_in=p_aux_required_in, p_aux_installed_in=p_aux_installed_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=StellarisSustainmentOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"p_aux_required_in": float(p_aux_required_in), "p_aux_installed_in": float(p_aux_installed_in)},
                )
            )
        )
