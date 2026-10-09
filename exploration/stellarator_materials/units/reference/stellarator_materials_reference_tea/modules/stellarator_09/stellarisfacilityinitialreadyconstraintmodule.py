"""Constraint module for stellarator_09__stellaris__facility_initial_ready__d3a5b04c428ef75f (Item 7 / D2/D3/D9).

Effective predicate: mfe_plant::'MFE Power Plant'::facility_initial_ready in owner instance stellarator_09__stellaris.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_reference_tea.schemas.constraint_types import ConstraintEvaluation
from stellarator_materials_reference_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_mfe_facilities__facility_nonnegative_margin


class StellarisFacilityInitialReadyConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    margin_in: float


class StellarisFacilityInitialReadyConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class StellarisFacilityInitialReadyConstraintModule(ModuleBase[StellarisFacilityInitialReadyConstraintInput, StellarisFacilityInitialReadyConstraintOutput]):
    name: str = "stellarator_09__stellaris__facility_initial_ready__d3a5b04c428ef75f"
    version: str = "v0.1"

    CONSTRAINT_ID = "stellarator_09__stellaris__facility_initial_ready__d3a5b04c428ef75f"

    def run(self, margin_in: float) -> ModuleResult[StellarisFacilityInitialReadyConstraintOutput]:
        StellarisFacilityInitialReadyConstraintInput(margin_in=margin_in)  # validate every resolved formal
        body = constraint_pred_definition_mfe_facilities__facility_nonnegative_margin(margin_in=margin_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=StellarisFacilityInitialReadyConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"margin_in": float(margin_in)},
                )
            )
        )
