"""Constraint module for magnet_subsystem__subsystem__nb3sn__steel_ok__5d849655e24deaf4 (Item 7 / D2/D3/D9).

Effective predicate: magnet_subsystem::subsystem::nb3sn::steel_ok in owner instance magnet_subsystem__subsystem__nb3sn.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from magnet_materials_tea.schemas.constraint_types import ConstraintEvaluation
from magnet_materials_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_magnet_conductor_alternatives__structural_steel_allowance


class SubsystemNb3snSteelOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    steel_margin_in: float


class SubsystemNb3snSteelOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class SubsystemNb3snSteelOkConstraintModule(ModuleBase[SubsystemNb3snSteelOkConstraintInput, SubsystemNb3snSteelOkConstraintOutput]):
    name: str = "magnet_subsystem__subsystem__nb3sn__steel_ok__5d849655e24deaf4"
    version: str = "v0.1"

    CONSTRAINT_ID = "magnet_subsystem__subsystem__nb3sn__steel_ok__5d849655e24deaf4"

    def run(self, steel_margin_in: float) -> ModuleResult[SubsystemNb3snSteelOkConstraintOutput]:
        SubsystemNb3snSteelOkConstraintInput(steel_margin_in=steel_margin_in)  # validate every resolved formal
        body = constraint_pred_definition_magnet_conductor_alternatives__structural_steel_allowance(steel_margin_in=steel_margin_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=SubsystemNb3snSteelOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"steel_margin_in": float(steel_margin_in)},
                )
            )
        )
