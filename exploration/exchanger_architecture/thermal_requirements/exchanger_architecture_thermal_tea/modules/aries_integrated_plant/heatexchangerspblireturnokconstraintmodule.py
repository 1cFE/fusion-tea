"""Constraint module for aries_integrated_plant__heat_exchangers__pbli_return_ok__100f6bf9ad61a22c (Item 7 / D2/D3/D9).

Effective predicate: aries_integrated_plant::heat_exchangers::pbli_return_ok in owner instance aries_integrated_plant__heat_exchangers.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from exchanger_architecture_thermal_tea.schemas.constraint_types import ConstraintEvaluation
from exchanger_architecture_thermal_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_controlled_exchanger_closure__thermal_return_held


class HeatExchangersPbliReturnOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    tolerance_in: float
    residual_magnitude_in: float


class HeatExchangersPbliReturnOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class HeatExchangersPbliReturnOkConstraintModule(ModuleBase[HeatExchangersPbliReturnOkConstraintInput, HeatExchangersPbliReturnOkConstraintOutput]):
    name: str = "aries_integrated_plant__heat_exchangers__pbli_return_ok__100f6bf9ad61a22c"
    version: str = "v0.1"

    CONSTRAINT_ID = "aries_integrated_plant__heat_exchangers__pbli_return_ok__100f6bf9ad61a22c"

    def run(self, tolerance_in: float, residual_magnitude_in: float) -> ModuleResult[HeatExchangersPbliReturnOkConstraintOutput]:
        HeatExchangersPbliReturnOkConstraintInput(tolerance_in=tolerance_in, residual_magnitude_in=residual_magnitude_in)  # validate every resolved formal
        body = constraint_pred_definition_controlled_exchanger_closure__thermal_return_held(residual_magnitude_in=residual_magnitude_in, tolerance_in=tolerance_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=HeatExchangersPbliReturnOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"residual_magnitude_in": float(residual_magnitude_in), "tolerance_in": float(tolerance_in)},
                )
            )
        )
