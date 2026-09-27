"""Constraint module for whole_plant_conversion__plant__gas_ledger__net_positive__41d28cae11b1dbd6 (Item 7 / D2/D3/D9).

Effective predicate: whole_plant_conversion::plant::gas_ledger::net_positive in owner instance whole_plant_conversion__plant__gas_ledger.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from whole_plant_conversion_tea.schemas.constraint_types import ConstraintEvaluation
from whole_plant_conversion_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_mfe_viability__net_power_positive


class PlantGasLedgerNetPositiveConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    net_electric: float


class PlantGasLedgerNetPositiveConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class PlantGasLedgerNetPositiveConstraintModule(ModuleBase[PlantGasLedgerNetPositiveConstraintInput, PlantGasLedgerNetPositiveConstraintOutput]):
    name: str = "whole_plant_conversion__plant__gas_ledger__net_positive__41d28cae11b1dbd6"
    version: str = "v0.1"

    CONSTRAINT_ID = "whole_plant_conversion__plant__gas_ledger__net_positive__41d28cae11b1dbd6"

    def run(self, net_electric: float) -> ModuleResult[PlantGasLedgerNetPositiveConstraintOutput]:
        PlantGasLedgerNetPositiveConstraintInput(net_electric=net_electric)  # validate every resolved formal
        body = constraint_pred_definition_mfe_viability__net_power_positive(net_electric=net_electric)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=PlantGasLedgerNetPositiveConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"net_electric": float(net_electric)},
                )
            )
        )
