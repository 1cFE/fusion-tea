"""Constraint module for component_alternatives__plant__steam_transport__motor_base_ok_required__238e695ccdaf5ebf (Item 7 / D2/D3/D9).

Effective predicate: component_alternatives::plant::steam_transport::motor_base_ok_required in owner instance component_alternatives__plant__steam_transport.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from component_alternatives_tea.schemas.constraint_types import ConstraintEvaluation
from component_alternatives_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_mfe_viability__offered_equipment_capacity


class PlantSteamTransportMotorBaseOkRequiredConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    margin_in: float
    defined_in: float


class PlantSteamTransportMotorBaseOkRequiredConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class PlantSteamTransportMotorBaseOkRequiredConstraintModule(ModuleBase[PlantSteamTransportMotorBaseOkRequiredConstraintInput, PlantSteamTransportMotorBaseOkRequiredConstraintOutput]):
    name: str = "component_alternatives__plant__steam_transport__motor_base_ok_required__238e695ccdaf5ebf"
    version: str = "v0.1"

    CONSTRAINT_ID = "component_alternatives__plant__steam_transport__motor_base_ok_required__238e695ccdaf5ebf"

    def run(self, margin_in: float, defined_in: float) -> ModuleResult[PlantSteamTransportMotorBaseOkRequiredConstraintOutput]:
        PlantSteamTransportMotorBaseOkRequiredConstraintInput(margin_in=margin_in, defined_in=defined_in)  # validate every resolved formal
        body = constraint_pred_definition_mfe_viability__offered_equipment_capacity(defined_in=defined_in, margin_in=margin_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=PlantSteamTransportMotorBaseOkRequiredConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"defined_in": float(defined_in), "margin_in": float(margin_in)},
                )
            )
        )
