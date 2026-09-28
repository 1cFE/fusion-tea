"""Constraint module for costed_loop_brayton__plant__compressor_capacity__capacity_ok__6e46ae5b5c0061be (Item 7 / D2/D3/D9).

Effective predicate: costed_loop_brayton::plant::compressor_capacity::capacity_ok in owner instance costed_loop_brayton__plant__compressor_capacity.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from costed_loop_brayton_tea.schemas.constraint_types import ConstraintEvaluation
from costed_loop_brayton_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_mfe_viability__offered_equipment_capacity


class PlantCompressorCapacityCapacityOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    margin_in: float
    defined_in: float


class PlantCompressorCapacityCapacityOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class PlantCompressorCapacityCapacityOkConstraintModule(ModuleBase[PlantCompressorCapacityCapacityOkConstraintInput, PlantCompressorCapacityCapacityOkConstraintOutput]):
    name: str = "costed_loop_brayton__plant__compressor_capacity__capacity_ok__6e46ae5b5c0061be"
    version: str = "v0.1"

    CONSTRAINT_ID = "costed_loop_brayton__plant__compressor_capacity__capacity_ok__6e46ae5b5c0061be"

    def run(self, margin_in: float, defined_in: float) -> ModuleResult[PlantCompressorCapacityCapacityOkConstraintOutput]:
        PlantCompressorCapacityCapacityOkConstraintInput(margin_in=margin_in, defined_in=defined_in)  # validate every resolved formal
        body = constraint_pred_definition_mfe_viability__offered_equipment_capacity(defined_in=defined_in, margin_in=margin_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=PlantCompressorCapacityCapacityOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"defined_in": float(defined_in), "margin_in": float(margin_in)},
                )
            )
        )
