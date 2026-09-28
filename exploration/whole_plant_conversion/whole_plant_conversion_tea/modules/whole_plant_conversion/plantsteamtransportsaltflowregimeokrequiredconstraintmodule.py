"""Constraint module for whole_plant_conversion__plant__steam_transport__salt_flow_regime_ok_required__4214cdcb871abc4e (Item 7 / D2/D3/D9).

Effective predicate: whole_plant_conversion::plant::steam_transport::salt_flow_regime_ok_required in owner instance whole_plant_conversion__plant__steam_transport.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from whole_plant_conversion_tea.schemas.constraint_types import ConstraintEvaluation
from whole_plant_conversion_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_mfe_viability__offered_equipment_capacity


class PlantSteamTransportSaltFlowRegimeOkRequiredConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    margin_in: float
    defined_in: float


class PlantSteamTransportSaltFlowRegimeOkRequiredConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class PlantSteamTransportSaltFlowRegimeOkRequiredConstraintModule(ModuleBase[PlantSteamTransportSaltFlowRegimeOkRequiredConstraintInput, PlantSteamTransportSaltFlowRegimeOkRequiredConstraintOutput]):
    name: str = "whole_plant_conversion__plant__steam_transport__salt_flow_regime_ok_required__4214cdcb871abc4e"
    version: str = "v0.1"

    CONSTRAINT_ID = "whole_plant_conversion__plant__steam_transport__salt_flow_regime_ok_required__4214cdcb871abc4e"

    def run(self, margin_in: float, defined_in: float) -> ModuleResult[PlantSteamTransportSaltFlowRegimeOkRequiredConstraintOutput]:
        PlantSteamTransportSaltFlowRegimeOkRequiredConstraintInput(margin_in=margin_in, defined_in=defined_in)  # validate every resolved formal
        body = constraint_pred_definition_mfe_viability__offered_equipment_capacity(defined_in=defined_in, margin_in=margin_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=PlantSteamTransportSaltFlowRegimeOkRequiredConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"defined_in": float(defined_in), "margin_in": float(margin_in)},
                )
            )
        )
