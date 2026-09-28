"""Constraint module for aries_integrated_plant__plant_ledger__balances_ok__9af2e85b5e4e5535 (Item 7 / D2/D3/D9).

Effective predicate: aries_integrated_plant::plant_ledger::balances_ok in owner instance aries_integrated_plant__plant_ledger.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from aries_integrated.schemas.constraint_types import ConstraintEvaluation
from aries_integrated.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_integrated_heat_electricity__integrated_ledger_balanced


class PlantLedgerBalancesOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    magnitude_in: float
    tolerance_in: float


class PlantLedgerBalancesOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class PlantLedgerBalancesOkConstraintModule(ModuleBase[PlantLedgerBalancesOkConstraintInput, PlantLedgerBalancesOkConstraintOutput]):
    name: str = "aries_integrated_plant__plant_ledger__balances_ok__9af2e85b5e4e5535"
    version: str = "v0.1"

    CONSTRAINT_ID = "aries_integrated_plant__plant_ledger__balances_ok__9af2e85b5e4e5535"

    def run(self, magnitude_in: float, tolerance_in: float) -> ModuleResult[PlantLedgerBalancesOkConstraintOutput]:
        PlantLedgerBalancesOkConstraintInput(magnitude_in=magnitude_in, tolerance_in=tolerance_in)  # validate every resolved formal
        body = constraint_pred_definition_integrated_heat_electricity__integrated_ledger_balanced(magnitude_in=magnitude_in, tolerance_in=tolerance_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=PlantLedgerBalancesOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"magnitude_in": float(magnitude_in), "tolerance_in": float(tolerance_in)},
                )
            )
        )
