"""Constraint module for magnet_subsystem__subsystem__rebco__acceptance_ok__904ca5528ef92aa4 (Item 7 / D2/D3/D9).

Effective predicate: magnet_subsystem::subsystem::rebco::acceptance_ok in owner instance magnet_subsystem__subsystem__rebco.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from magnet_materials_tea.schemas.constraint_types import ConstraintEvaluation
from magnet_materials_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_magnet_conductor_alternatives__conductor_acceptance


class SubsystemRebcoAcceptanceOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    margin_in: float
    supported_in: float


class SubsystemRebcoAcceptanceOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class SubsystemRebcoAcceptanceOkConstraintModule(ModuleBase[SubsystemRebcoAcceptanceOkConstraintInput, SubsystemRebcoAcceptanceOkConstraintOutput]):
    name: str = "magnet_subsystem__subsystem__rebco__acceptance_ok__904ca5528ef92aa4"
    version: str = "v0.1"

    CONSTRAINT_ID = "magnet_subsystem__subsystem__rebco__acceptance_ok__904ca5528ef92aa4"

    def run(self, margin_in: float, supported_in: float) -> ModuleResult[SubsystemRebcoAcceptanceOkConstraintOutput]:
        SubsystemRebcoAcceptanceOkConstraintInput(margin_in=margin_in, supported_in=supported_in)  # validate every resolved formal
        body = constraint_pred_definition_magnet_conductor_alternatives__conductor_acceptance(supported_in=supported_in, margin_in=margin_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=SubsystemRebcoAcceptanceOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"supported_in": float(supported_in), "margin_in": float(margin_in)},
                )
            )
        )
