"""Constraint module for aries_integrated_plant__heat_exchangers__he_state_ok__d5b9d58030392fe5 (Item 7 / D2/D3/D9).

Effective predicate: aries_integrated_plant::heat_exchangers::he_state_ok in owner instance aries_integrated_plant__heat_exchangers.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from exchanger_architecture_thermal_tea.schemas.constraint_types import ConstraintEvaluation
from exchanger_architecture_thermal_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_controlled_exchanger_closure__thermal_state_defined


class HeatExchangersHeStateOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    defined_in: float


class HeatExchangersHeStateOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class HeatExchangersHeStateOkConstraintModule(ModuleBase[HeatExchangersHeStateOkConstraintInput, HeatExchangersHeStateOkConstraintOutput]):
    name: str = "aries_integrated_plant__heat_exchangers__he_state_ok__d5b9d58030392fe5"
    version: str = "v0.1"

    CONSTRAINT_ID = "aries_integrated_plant__heat_exchangers__he_state_ok__d5b9d58030392fe5"

    def run(self, defined_in: float) -> ModuleResult[HeatExchangersHeStateOkConstraintOutput]:
        HeatExchangersHeStateOkConstraintInput(defined_in=defined_in)  # validate every resolved formal
        body = constraint_pred_definition_controlled_exchanger_closure__thermal_state_defined(defined_in=defined_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=HeatExchangersHeStateOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"defined_in": float(defined_in)},
                )
            )
        )
