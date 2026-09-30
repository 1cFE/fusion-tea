"""Constraint module for magnet_subsystem__subsystem__rebco__steel_ok__4f587fec2c667312 (Item 7 / D2/D3/D9).

Effective predicate: magnet_subsystem::subsystem::rebco::steel_ok in owner instance magnet_subsystem__subsystem__rebco.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from magnet_materials_tea.schemas.constraint_types import ConstraintEvaluation
from magnet_materials_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_magnet_conductor_alternatives__structural_steel_allowance


class SubsystemRebcoSteelOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    steel_margin_in: float


class SubsystemRebcoSteelOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class SubsystemRebcoSteelOkConstraintModule(ModuleBase[SubsystemRebcoSteelOkConstraintInput, SubsystemRebcoSteelOkConstraintOutput]):
    name: str = "magnet_subsystem__subsystem__rebco__steel_ok__4f587fec2c667312"
    version: str = "v0.1"

    CONSTRAINT_ID = "magnet_subsystem__subsystem__rebco__steel_ok__4f587fec2c667312"

    def run(self, steel_margin_in: float) -> ModuleResult[SubsystemRebcoSteelOkConstraintOutput]:
        SubsystemRebcoSteelOkConstraintInput(steel_margin_in=steel_margin_in)  # validate every resolved formal
        body = constraint_pred_definition_magnet_conductor_alternatives__structural_steel_allowance(steel_margin_in=steel_margin_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=SubsystemRebcoSteelOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"steel_margin_in": float(steel_margin_in)},
                )
            )
        )
