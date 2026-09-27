"""Constraint module for component_alternatives__plant__steam_transport__pump_size_ok_required__b3af0a8e326050b1 (Item 7 / D2/D3/D9).

Effective predicate: component_alternatives::plant::steam_transport::pump_size_ok_required in owner instance component_alternatives__plant__steam_transport.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from component_alternatives_tea.schemas.constraint_types import ConstraintEvaluation
from component_alternatives_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_mfe_viability__offered_equipment_capacity


class PlantSteamTransportPumpSizeOkRequiredConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    margin_in: float
    defined_in: float


class PlantSteamTransportPumpSizeOkRequiredConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class PlantSteamTransportPumpSizeOkRequiredConstraintModule(ModuleBase[PlantSteamTransportPumpSizeOkRequiredConstraintInput, PlantSteamTransportPumpSizeOkRequiredConstraintOutput]):
    name: str = "component_alternatives__plant__steam_transport__pump_size_ok_required__b3af0a8e326050b1"
    version: str = "v0.1"

    CONSTRAINT_ID = "component_alternatives__plant__steam_transport__pump_size_ok_required__b3af0a8e326050b1"

    def run(self, margin_in: float, defined_in: float) -> ModuleResult[PlantSteamTransportPumpSizeOkRequiredConstraintOutput]:
        PlantSteamTransportPumpSizeOkRequiredConstraintInput(margin_in=margin_in, defined_in=defined_in)  # validate every resolved formal
        body = constraint_pred_definition_mfe_viability__offered_equipment_capacity(defined_in=defined_in, margin_in=margin_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=PlantSteamTransportPumpSizeOkRequiredConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"defined_in": float(defined_in), "margin_in": float(margin_in)},
                )
            )
        )
