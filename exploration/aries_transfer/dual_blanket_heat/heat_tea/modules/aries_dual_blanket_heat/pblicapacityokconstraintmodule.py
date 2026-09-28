"""Constraint module for aries_dual_blanket_heat__pbli__capacity_ok__24d83956889b2fa6 (Item 7 / D2/D3/D9).

Effective predicate: aries_dual_blanket_heat::pbli::capacity_ok in owner instance aries_dual_blanket_heat__pbli.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from heat_tea.schemas.constraint_types import ConstraintEvaluation
from heat_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_mfe_viability__offered_equipment_capacity


class PbliCapacityOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    margin_in: float
    defined_in: float


class PbliCapacityOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class PbliCapacityOkConstraintModule(ModuleBase[PbliCapacityOkConstraintInput, PbliCapacityOkConstraintOutput]):
    name: str = "aries_dual_blanket_heat__pbli__capacity_ok__24d83956889b2fa6"
    version: str = "v0.1"

    CONSTRAINT_ID = "aries_dual_blanket_heat__pbli__capacity_ok__24d83956889b2fa6"

    def run(self, margin_in: float, defined_in: float) -> ModuleResult[PbliCapacityOkConstraintOutput]:
        PbliCapacityOkConstraintInput(margin_in=margin_in, defined_in=defined_in)  # validate every resolved formal
        body = constraint_pred_definition_mfe_viability__offered_equipment_capacity(defined_in=defined_in, margin_in=margin_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=PbliCapacityOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"defined_in": float(defined_in), "margin_in": float(margin_in)},
                )
            )
        )
