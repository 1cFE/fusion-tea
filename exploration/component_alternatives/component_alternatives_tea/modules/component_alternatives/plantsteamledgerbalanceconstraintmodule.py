"""Constraint module for component_alternatives__plant__steam_ledger__balance__79e79cd29079c8e8 (Item 7 / D2/D3/D9).

Effective predicate: component_alternatives::plant::steam_ledger::balance in owner instance component_alternatives__plant__steam_ledger.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from component_alternatives_tea.schemas.constraint_types import ConstraintEvaluation
from component_alternatives_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_component_alternatives_thermal__numerical_residual


class PlantSteamLedgerBalanceConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    tolerance_in: float
    residual_in: float


class PlantSteamLedgerBalanceConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class PlantSteamLedgerBalanceConstraintModule(ModuleBase[PlantSteamLedgerBalanceConstraintInput, PlantSteamLedgerBalanceConstraintOutput]):
    name: str = "component_alternatives__plant__steam_ledger__balance__79e79cd29079c8e8"
    version: str = "v0.1"

    CONSTRAINT_ID = "component_alternatives__plant__steam_ledger__balance__79e79cd29079c8e8"

    def run(self, tolerance_in: float, residual_in: float) -> ModuleResult[PlantSteamLedgerBalanceConstraintOutput]:
        PlantSteamLedgerBalanceConstraintInput(tolerance_in=tolerance_in, residual_in=residual_in)  # validate every resolved formal
        body = constraint_pred_definition_component_alternatives_thermal__numerical_residual(residual_in=residual_in, tolerance_in=tolerance_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=PlantSteamLedgerBalanceConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"residual_in": float(residual_in), "tolerance_in": float(tolerance_in)},
                )
            )
        )
