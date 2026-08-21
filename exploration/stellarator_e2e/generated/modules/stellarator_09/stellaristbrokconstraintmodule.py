"""Constraint module for stellarator_09__stellaris__tbr_ok__2cd198f674d413e4 (Item 7 / D2/D3/D9).

Effective predicate: stellarator_09::stellaris::tbr_ok in owner instance stellarator_09__stellaris.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.schemas.constraint_types import ConstraintEvaluation
from stellarator_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_mfe_viability__tbr_floor


class StellarisTbrOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    tbr: float
    tbr_floor: float


class StellarisTbrOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class StellarisTbrOkConstraintModule(ModuleBase[StellarisTbrOkConstraintInput, StellarisTbrOkConstraintOutput]):
    name: str = "stellarator_09__stellaris__tbr_ok__2cd198f674d413e4"
    version: str = "v0.1"

    CONSTRAINT_ID = "stellarator_09__stellaris__tbr_ok__2cd198f674d413e4"

    def run(self, tbr: float, tbr_floor: float) -> ModuleResult[StellarisTbrOkConstraintOutput]:
        StellarisTbrOkConstraintInput(tbr=tbr, tbr_floor=tbr_floor)  # validate every resolved formal
        body = constraint_pred_definition_mfe_viability__tbr_floor(tbr=tbr, tbr_floor=tbr_floor)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=StellarisTbrOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"tbr": float(tbr), "tbr_floor": float(tbr_floor)},
                )
            )
        )
