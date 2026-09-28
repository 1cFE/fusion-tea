"""Constraint module for whole_plant_conversion__plant__gas_ledger__balance__d86d965fca008ca2 (Item 7 / D2/D3/D9).

Effective predicate: whole_plant_conversion::plant::gas_ledger::balance in owner instance whole_plant_conversion__plant__gas_ledger.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from whole_plant_conversion_tea.schemas.constraint_types import ConstraintEvaluation
from whole_plant_conversion_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_component_alternatives_thermal__numerical_residual


class PlantGasLedgerBalanceConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    tolerance_in: float
    residual_in: float


class PlantGasLedgerBalanceConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class PlantGasLedgerBalanceConstraintModule(ModuleBase[PlantGasLedgerBalanceConstraintInput, PlantGasLedgerBalanceConstraintOutput]):
    name: str = "whole_plant_conversion__plant__gas_ledger__balance__d86d965fca008ca2"
    version: str = "v0.1"

    CONSTRAINT_ID = "whole_plant_conversion__plant__gas_ledger__balance__d86d965fca008ca2"

    def run(self, tolerance_in: float, residual_in: float) -> ModuleResult[PlantGasLedgerBalanceConstraintOutput]:
        PlantGasLedgerBalanceConstraintInput(tolerance_in=tolerance_in, residual_in=residual_in)  # validate every resolved formal
        body = constraint_pred_definition_component_alternatives_thermal__numerical_residual(residual_in=residual_in, tolerance_in=tolerance_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=PlantGasLedgerBalanceConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"residual_in": float(residual_in), "tolerance_in": float(tolerance_in)},
                )
            )
        )
