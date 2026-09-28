"""Constraint module for aries_integrated_plant__heat_exchangers__pbli_state_ok__4664e5e1ddbb7ac5 (Item 7 / D2/D3/D9).

Effective predicate: aries_integrated_plant::heat_exchangers::pbli_state_ok in owner instance aries_integrated_plant__heat_exchangers.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from exchanger_architecture_thermal_tea.schemas.constraint_types import ConstraintEvaluation
from exchanger_architecture_thermal_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_controlled_exchanger_closure__thermal_state_defined


class HeatExchangersPbliStateOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    defined_in: float


class HeatExchangersPbliStateOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class HeatExchangersPbliStateOkConstraintModule(ModuleBase[HeatExchangersPbliStateOkConstraintInput, HeatExchangersPbliStateOkConstraintOutput]):
    name: str = "aries_integrated_plant__heat_exchangers__pbli_state_ok__4664e5e1ddbb7ac5"
    version: str = "v0.1"

    CONSTRAINT_ID = "aries_integrated_plant__heat_exchangers__pbli_state_ok__4664e5e1ddbb7ac5"

    def run(self, defined_in: float) -> ModuleResult[HeatExchangersPbliStateOkConstraintOutput]:
        HeatExchangersPbliStateOkConstraintInput(defined_in=defined_in)  # validate every resolved formal
        body = constraint_pred_definition_controlled_exchanger_closure__thermal_state_defined(defined_in=defined_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=HeatExchangersPbliStateOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"defined_in": float(defined_in)},
                )
            )
        )
