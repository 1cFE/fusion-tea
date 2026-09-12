"""Constraint module for stellarator_09__stellaris__divertor_heat_ok__26b4658f9fdfd7b7 (Item 7 / D2/D3/D9).

Effective predicate: mfe_plant::'MFE Power Plant'::divertor_heat_ok in owner instance stellarator_09__stellaris.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from wi052_probe.schemas.constraint_types import ConstraintEvaluation
from wi052_probe.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_mfe_viability__divertor_target_heat_limit


class StellarisDivertorHeatOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    q_target_peak_in: float
    q_target_limit_in: float


class StellarisDivertorHeatOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class StellarisDivertorHeatOkConstraintModule(ModuleBase[StellarisDivertorHeatOkConstraintInput, StellarisDivertorHeatOkConstraintOutput]):
    name: str = "stellarator_09__stellaris__divertor_heat_ok__26b4658f9fdfd7b7"
    version: str = "v0.1"

    CONSTRAINT_ID = "stellarator_09__stellaris__divertor_heat_ok__26b4658f9fdfd7b7"

    def run(self, q_target_peak_in: float, q_target_limit_in: float) -> ModuleResult[StellarisDivertorHeatOkConstraintOutput]:
        StellarisDivertorHeatOkConstraintInput(q_target_peak_in=q_target_peak_in, q_target_limit_in=q_target_limit_in)  # validate every resolved formal
        body = constraint_pred_definition_mfe_viability__divertor_target_heat_limit(q_target_peak_in=q_target_peak_in, q_target_limit_in=q_target_limit_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=StellarisDivertorHeatOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"q_target_peak_in": float(q_target_peak_in), "q_target_limit_in": float(q_target_limit_in)},
                )
            )
        )
