"""Constraint module for aries_integrated_plant__plant_ledger__heat_removal_ok__695378663bcd8d07 (Item 7 / D2/D3/D9).

Effective predicate: aries_integrated_plant::plant_ledger::heat_removal_ok in owner instance aries_integrated_plant__plant_ledger.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from aries_integrated.schemas.constraint_types import ConstraintEvaluation
from aries_integrated.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_integrated_heat_electricity__heat_removal_adequate


class PlantLedgerHeatRemovalOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    tolerance_in: float
    unmet_in: float


class PlantLedgerHeatRemovalOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class PlantLedgerHeatRemovalOkConstraintModule(ModuleBase[PlantLedgerHeatRemovalOkConstraintInput, PlantLedgerHeatRemovalOkConstraintOutput]):
    name: str = "aries_integrated_plant__plant_ledger__heat_removal_ok__695378663bcd8d07"
    version: str = "v0.1"

    CONSTRAINT_ID = "aries_integrated_plant__plant_ledger__heat_removal_ok__695378663bcd8d07"

    def run(self, tolerance_in: float, unmet_in: float) -> ModuleResult[PlantLedgerHeatRemovalOkConstraintOutput]:
        PlantLedgerHeatRemovalOkConstraintInput(tolerance_in=tolerance_in, unmet_in=unmet_in)  # validate every resolved formal
        body = constraint_pred_definition_integrated_heat_electricity__heat_removal_adequate(unmet_in=unmet_in, tolerance_in=tolerance_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=PlantLedgerHeatRemovalOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"unmet_in": float(unmet_in), "tolerance_in": float(tolerance_in)},
                )
            )
        )
