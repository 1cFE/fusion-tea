"""Constraint module for combinations_plasma_chain__plasma_chain__he_pump__capacity_ok__933c88ced63feb63 (Item 7 / D2/D3/D9).

Effective predicate: combinations_plasma_chain::plasma_chain::he_pump::capacity_ok in owner instance combinations_plasma_chain__plasma_chain__he_pump.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from combinations_tea.schemas.constraint_types import ConstraintEvaluation
from combinations_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_mfe_viability__offered_equipment_capacity


class PlasmaChainHePumpCapacityOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    margin_in: float
    defined_in: float


class PlasmaChainHePumpCapacityOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class PlasmaChainHePumpCapacityOkConstraintModule(ModuleBase[PlasmaChainHePumpCapacityOkConstraintInput, PlasmaChainHePumpCapacityOkConstraintOutput]):
    name: str = "combinations_plasma_chain__plasma_chain__he_pump__capacity_ok__933c88ced63feb63"
    version: str = "v0.1"

    CONSTRAINT_ID = "combinations_plasma_chain__plasma_chain__he_pump__capacity_ok__933c88ced63feb63"

    def run(self, margin_in: float, defined_in: float) -> ModuleResult[PlasmaChainHePumpCapacityOkConstraintOutput]:
        PlasmaChainHePumpCapacityOkConstraintInput(margin_in=margin_in, defined_in=defined_in)  # validate every resolved formal
        body = constraint_pred_definition_mfe_viability__offered_equipment_capacity(defined_in=defined_in, margin_in=margin_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=PlasmaChainHePumpCapacityOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"defined_in": float(defined_in), "margin_in": float(margin_in)},
                )
            )
        )
