"""Constraint module for stellarator_09__stellaris__heating_couple_positive_ok__697e87be76f504b7 (Item 7 / D2/D3/D9).

Effective predicate: mfe_plant::'MFE Power Plant'::heating_couple_positive_ok in owner instance stellarator_09__stellaris.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.schemas.constraint_types import ConstraintEvaluation
from stellarator_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_mfe_heating_chain__heating_efficiency_positive


class StellarisHeatingCouplePositiveOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    efficiency: float


class StellarisHeatingCouplePositiveOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class StellarisHeatingCouplePositiveOkConstraintModule(ModuleBase[StellarisHeatingCouplePositiveOkConstraintInput, StellarisHeatingCouplePositiveOkConstraintOutput]):
    name: str = "stellarator_09__stellaris__heating_couple_positive_ok__697e87be76f504b7"
    version: str = "v0.1"

    CONSTRAINT_ID = "stellarator_09__stellaris__heating_couple_positive_ok__697e87be76f504b7"

    def run(self, efficiency: float) -> ModuleResult[StellarisHeatingCouplePositiveOkConstraintOutput]:
        StellarisHeatingCouplePositiveOkConstraintInput(efficiency=efficiency)  # validate every resolved formal
        body = constraint_pred_definition_mfe_heating_chain__heating_efficiency_positive(efficiency=efficiency)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=StellarisHeatingCouplePositiveOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"efficiency": float(efficiency)},
                )
            )
        )
