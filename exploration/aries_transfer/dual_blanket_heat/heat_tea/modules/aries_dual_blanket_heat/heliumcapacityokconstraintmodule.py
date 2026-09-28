"""Constraint module for aries_dual_blanket_heat__helium__capacity_ok__1ebe7a3e536db96a (Item 7 / D2/D3/D9).

Effective predicate: aries_dual_blanket_heat::helium::capacity_ok in owner instance aries_dual_blanket_heat__helium.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from heat_tea.schemas.constraint_types import ConstraintEvaluation
from heat_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_mfe_viability__offered_equipment_capacity


class HeliumCapacityOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    margin_in: float
    defined_in: float


class HeliumCapacityOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class HeliumCapacityOkConstraintModule(ModuleBase[HeliumCapacityOkConstraintInput, HeliumCapacityOkConstraintOutput]):
    name: str = "aries_dual_blanket_heat__helium__capacity_ok__1ebe7a3e536db96a"
    version: str = "v0.1"

    CONSTRAINT_ID = "aries_dual_blanket_heat__helium__capacity_ok__1ebe7a3e536db96a"

    def run(self, margin_in: float, defined_in: float) -> ModuleResult[HeliumCapacityOkConstraintOutput]:
        HeliumCapacityOkConstraintInput(margin_in=margin_in, defined_in=defined_in)  # validate every resolved formal
        body = constraint_pred_definition_mfe_viability__offered_equipment_capacity(defined_in=defined_in, margin_in=margin_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=HeliumCapacityOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"defined_in": float(defined_in), "margin_in": float(margin_in)},
                )
            )
        )
