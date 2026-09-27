"""Constraint module for aries_integrated_plant__heat_exchangers__he_control_ok__f48454bb1d6f0e91 (Item 7 / D2/D3/D9).

Effective predicate: aries_integrated_plant::heat_exchangers::he_control_ok in owner instance aries_integrated_plant__heat_exchangers.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from exchanger_architecture_thermal_tea.schemas.constraint_types import ConstraintEvaluation
from exchanger_architecture_thermal_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_controlled_exchanger_closure__thermal_nonnegative_margin


class HeatExchangersHeControlOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    margin_in: float


class HeatExchangersHeControlOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class HeatExchangersHeControlOkConstraintModule(ModuleBase[HeatExchangersHeControlOkConstraintInput, HeatExchangersHeControlOkConstraintOutput]):
    name: str = "aries_integrated_plant__heat_exchangers__he_control_ok__f48454bb1d6f0e91"
    version: str = "v0.1"

    CONSTRAINT_ID = "aries_integrated_plant__heat_exchangers__he_control_ok__f48454bb1d6f0e91"

    def run(self, margin_in: float) -> ModuleResult[HeatExchangersHeControlOkConstraintOutput]:
        HeatExchangersHeControlOkConstraintInput(margin_in=margin_in)  # validate every resolved formal
        body = constraint_pred_definition_controlled_exchanger_closure__thermal_nonnegative_margin(margin_in=margin_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=HeatExchangersHeControlOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"margin_in": float(margin_in)},
                )
            )
        )
