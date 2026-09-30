"""Constraint module for stellarator_09__stellaris__reference_conductor_current_ok__3cf239a7cdc0f2f0 (Item 7 / D2/D3/D9).

Effective predicate: stellarator_09::stellaris::reference_conductor_current_ok in owner instance stellarator_09__stellaris.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_reference_tea.schemas.constraint_types import ConstraintEvaluation
from stellarator_materials_reference_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_mfe_conductor_current__reference_conductor_current_margin


class StellarisReferenceConductorCurrentOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    margin_fraction_in: float


class StellarisReferenceConductorCurrentOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class StellarisReferenceConductorCurrentOkConstraintModule(ModuleBase[StellarisReferenceConductorCurrentOkConstraintInput, StellarisReferenceConductorCurrentOkConstraintOutput]):
    name: str = "stellarator_09__stellaris__reference_conductor_current_ok__3cf239a7cdc0f2f0"
    version: str = "v0.1"

    CONSTRAINT_ID = "stellarator_09__stellaris__reference_conductor_current_ok__3cf239a7cdc0f2f0"

    def run(self, margin_fraction_in: float) -> ModuleResult[StellarisReferenceConductorCurrentOkConstraintOutput]:
        StellarisReferenceConductorCurrentOkConstraintInput(margin_fraction_in=margin_fraction_in)  # validate every resolved formal
        body = constraint_pred_definition_mfe_conductor_current__reference_conductor_current_margin(margin_fraction_in=margin_fraction_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=StellarisReferenceConductorCurrentOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"margin_fraction_in": float(margin_fraction_in)},
                )
            )
        )
