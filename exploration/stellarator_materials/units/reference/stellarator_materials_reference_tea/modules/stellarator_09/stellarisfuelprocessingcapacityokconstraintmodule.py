"""Constraint module for stellarator_09__stellaris__fuel_processing_capacity_ok__ddb8525b2bda8f0a (Item 7 / D2/D3/D9).

Effective predicate: stellarator_09::stellaris::fuel_processing_capacity_ok in owner instance stellarator_09__stellaris.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_reference_tea.schemas.constraint_types import ConstraintEvaluation
from stellarator_materials_reference_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_mfe_fuel_cycle__fuel_processing_capacity


class StellarisFuelProcessingCapacityOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    margin_in: float
    defined_in: float


class StellarisFuelProcessingCapacityOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class StellarisFuelProcessingCapacityOkConstraintModule(ModuleBase[StellarisFuelProcessingCapacityOkConstraintInput, StellarisFuelProcessingCapacityOkConstraintOutput]):
    name: str = "stellarator_09__stellaris__fuel_processing_capacity_ok__ddb8525b2bda8f0a"
    version: str = "v0.1"

    CONSTRAINT_ID = "stellarator_09__stellaris__fuel_processing_capacity_ok__ddb8525b2bda8f0a"

    def run(self, margin_in: float, defined_in: float) -> ModuleResult[StellarisFuelProcessingCapacityOkConstraintOutput]:
        StellarisFuelProcessingCapacityOkConstraintInput(margin_in=margin_in, defined_in=defined_in)  # validate every resolved formal
        body = constraint_pred_definition_mfe_fuel_cycle__fuel_processing_capacity(defined_in=defined_in, margin_in=margin_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=StellarisFuelProcessingCapacityOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"defined_in": float(defined_in), "margin_in": float(margin_in)},
                )
            )
        )
