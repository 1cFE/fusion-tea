"""Constraint module for stellarator_09__stellaris__peak_field_ok__49c6b8228a73cac5 (Item 7 / D2/D3/D9).

Effective predicate: mfe_plant::'MFE Power Plant'::peak_field_ok in owner instance stellarator_09__stellaris.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.schemas.constraint_types import ConstraintEvaluation
from stellarator_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_mfe_viability__conductor_peak_field_limit


class StellarisPeakFieldOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    B_max_in: float
    B_peak: float


class StellarisPeakFieldOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class StellarisPeakFieldOkConstraintModule(ModuleBase[StellarisPeakFieldOkConstraintInput, StellarisPeakFieldOkConstraintOutput]):
    name: str = "stellarator_09__stellaris__peak_field_ok__49c6b8228a73cac5"
    version: str = "v0.1"

    CONSTRAINT_ID = "stellarator_09__stellaris__peak_field_ok__49c6b8228a73cac5"

    def run(self, B_max_in: float, B_peak: float) -> ModuleResult[StellarisPeakFieldOkConstraintOutput]:
        StellarisPeakFieldOkConstraintInput(B_max_in=B_max_in, B_peak=B_peak)  # validate every resolved formal
        body = constraint_pred_definition_mfe_viability__conductor_peak_field_limit(B_peak=B_peak, B_max_in=B_max_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=StellarisPeakFieldOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"B_peak": float(B_peak), "B_max_in": float(B_max_in)},
                )
            )
        )
