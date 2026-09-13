"""Constraint module for stellarator_09__stellaris__heating_source_upper_ok__14ddae450a8eda6f (Item 7 / D2/D3/D9).

Effective predicate: mfe_plant::'MFE Power Plant'::heating_source_upper_ok in owner instance stellarator_09__stellaris.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.schemas.constraint_types import ConstraintEvaluation
from stellarator_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_mfe_heating_chain__heating_efficiency_upper


class StellarisHeatingSourceUpperOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    efficiency: float


class StellarisHeatingSourceUpperOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class StellarisHeatingSourceUpperOkConstraintModule(ModuleBase[StellarisHeatingSourceUpperOkConstraintInput, StellarisHeatingSourceUpperOkConstraintOutput]):
    name: str = "stellarator_09__stellaris__heating_source_upper_ok__14ddae450a8eda6f"
    version: str = "v0.1"

    CONSTRAINT_ID = "stellarator_09__stellaris__heating_source_upper_ok__14ddae450a8eda6f"

    def run(self, efficiency: float) -> ModuleResult[StellarisHeatingSourceUpperOkConstraintOutput]:
        StellarisHeatingSourceUpperOkConstraintInput(efficiency=efficiency)  # validate every resolved formal
        body = constraint_pred_definition_mfe_heating_chain__heating_efficiency_upper(efficiency=efficiency)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=StellarisHeatingSourceUpperOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"efficiency": float(efficiency)},
                )
            )
        )
