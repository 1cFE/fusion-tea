"""Constraint module for aries_nominal_brayton__heater_capacity__capacity_ok__ab792e2afb3f95b9 (Item 7 / D2/D3/D9).

Effective predicate: aries_nominal_brayton::heater_capacity::capacity_ok in owner instance aries_nominal_brayton__heater_capacity.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from brayton_tea.schemas.constraint_types import ConstraintEvaluation
from brayton_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_mfe_viability__offered_equipment_capacity


class HeaterCapacityCapacityOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    margin_in: float
    defined_in: float


class HeaterCapacityCapacityOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class HeaterCapacityCapacityOkConstraintModule(ModuleBase[HeaterCapacityCapacityOkConstraintInput, HeaterCapacityCapacityOkConstraintOutput]):
    name: str = "aries_nominal_brayton__heater_capacity__capacity_ok__ab792e2afb3f95b9"
    version: str = "v0.1"

    CONSTRAINT_ID = "aries_nominal_brayton__heater_capacity__capacity_ok__ab792e2afb3f95b9"

    def run(self, margin_in: float, defined_in: float) -> ModuleResult[HeaterCapacityCapacityOkConstraintOutput]:
        HeaterCapacityCapacityOkConstraintInput(margin_in=margin_in, defined_in=defined_in)  # validate every resolved formal
        body = constraint_pred_definition_mfe_viability__offered_equipment_capacity(defined_in=defined_in, margin_in=margin_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=HeaterCapacityCapacityOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"defined_in": float(defined_in), "margin_in": float(margin_in)},
                )
            )
        )
