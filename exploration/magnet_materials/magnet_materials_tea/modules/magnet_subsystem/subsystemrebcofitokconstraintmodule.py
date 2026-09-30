"""Constraint module for magnet_subsystem__subsystem__rebco__fit_ok__977ffb782260e056 (Item 7 / D2/D3/D9).

Effective predicate: magnet_subsystem::subsystem::rebco::fit_ok in owner instance magnet_subsystem__subsystem__rebco.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from magnet_materials_tea.schemas.constraint_types import ConstraintEvaluation
from magnet_materials_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_magnet_conductor_alternatives__winding_fit


class SubsystemRebcoFitOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    fit_margin_in: float


class SubsystemRebcoFitOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class SubsystemRebcoFitOkConstraintModule(ModuleBase[SubsystemRebcoFitOkConstraintInput, SubsystemRebcoFitOkConstraintOutput]):
    name: str = "magnet_subsystem__subsystem__rebco__fit_ok__977ffb782260e056"
    version: str = "v0.1"

    CONSTRAINT_ID = "magnet_subsystem__subsystem__rebco__fit_ok__977ffb782260e056"

    def run(self, fit_margin_in: float) -> ModuleResult[SubsystemRebcoFitOkConstraintOutput]:
        SubsystemRebcoFitOkConstraintInput(fit_margin_in=fit_margin_in)  # validate every resolved formal
        body = constraint_pred_definition_magnet_conductor_alternatives__winding_fit(fit_margin_in=fit_margin_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=SubsystemRebcoFitOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"fit_margin_in": float(fit_margin_in)},
                )
            )
        )
