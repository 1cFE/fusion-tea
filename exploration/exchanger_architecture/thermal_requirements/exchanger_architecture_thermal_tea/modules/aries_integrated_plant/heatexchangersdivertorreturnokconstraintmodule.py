"""Constraint module for aries_integrated_plant__heat_exchangers__divertor_return_ok__f69c5310bdcc41d7 (Item 7 / D2/D3/D9).

Effective predicate: aries_integrated_plant::heat_exchangers::divertor_return_ok in owner instance aries_integrated_plant__heat_exchangers.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from exchanger_architecture_thermal_tea.schemas.constraint_types import ConstraintEvaluation
from exchanger_architecture_thermal_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_controlled_exchanger_closure__thermal_return_held


class HeatExchangersDivertorReturnOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    tolerance_in: float
    residual_magnitude_in: float


class HeatExchangersDivertorReturnOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class HeatExchangersDivertorReturnOkConstraintModule(ModuleBase[HeatExchangersDivertorReturnOkConstraintInput, HeatExchangersDivertorReturnOkConstraintOutput]):
    name: str = "aries_integrated_plant__heat_exchangers__divertor_return_ok__f69c5310bdcc41d7"
    version: str = "v0.1"

    CONSTRAINT_ID = "aries_integrated_plant__heat_exchangers__divertor_return_ok__f69c5310bdcc41d7"

    def run(self, tolerance_in: float, residual_magnitude_in: float) -> ModuleResult[HeatExchangersDivertorReturnOkConstraintOutput]:
        HeatExchangersDivertorReturnOkConstraintInput(tolerance_in=tolerance_in, residual_magnitude_in=residual_magnitude_in)  # validate every resolved formal
        body = constraint_pred_definition_controlled_exchanger_closure__thermal_return_held(residual_magnitude_in=residual_magnitude_in, tolerance_in=tolerance_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=HeatExchangersDivertorReturnOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"residual_magnitude_in": float(residual_magnitude_in), "tolerance_in": float(tolerance_in)},
                )
            )
        )
