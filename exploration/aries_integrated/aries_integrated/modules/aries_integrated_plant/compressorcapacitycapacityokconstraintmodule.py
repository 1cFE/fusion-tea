"""Constraint module for aries_integrated_plant__compressor_capacity__capacity_ok__a45f9cf05e8aa7ab (Item 7 / D2/D3/D9).

Effective predicate: aries_integrated_plant::compressor_capacity::capacity_ok in owner instance aries_integrated_plant__compressor_capacity.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from aries_integrated.schemas.constraint_types import ConstraintEvaluation
from aries_integrated.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_mfe_viability__offered_equipment_capacity


class CompressorCapacityCapacityOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    margin_in: float
    defined_in: float


class CompressorCapacityCapacityOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class CompressorCapacityCapacityOkConstraintModule(ModuleBase[CompressorCapacityCapacityOkConstraintInput, CompressorCapacityCapacityOkConstraintOutput]):
    name: str = "aries_integrated_plant__compressor_capacity__capacity_ok__a45f9cf05e8aa7ab"
    version: str = "v0.1"

    CONSTRAINT_ID = "aries_integrated_plant__compressor_capacity__capacity_ok__a45f9cf05e8aa7ab"

    def run(self, margin_in: float, defined_in: float) -> ModuleResult[CompressorCapacityCapacityOkConstraintOutput]:
        CompressorCapacityCapacityOkConstraintInput(margin_in=margin_in, defined_in=defined_in)  # validate every resolved formal
        body = constraint_pred_definition_mfe_viability__offered_equipment_capacity(defined_in=defined_in, margin_in=margin_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=CompressorCapacityCapacityOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"defined_in": float(defined_in), "margin_in": float(margin_in)},
                )
            )
        )
