"""Constraint module for magnet_subsystem__subsystem__nb3sn__copper_ok__a4ff5a6abedecdd2 (Item 7 / D2/D3/D9).

Effective predicate: magnet_subsystem::subsystem::nb3sn::copper_ok in owner instance magnet_subsystem__subsystem__nb3sn.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from magnet_materials_tea.schemas.constraint_types import ConstraintEvaluation
from magnet_materials_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_magnet_conductor_alternatives__protection_copper_allowance


class SubsystemNb3snCopperOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    cu_margin_in: float


class SubsystemNb3snCopperOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class SubsystemNb3snCopperOkConstraintModule(ModuleBase[SubsystemNb3snCopperOkConstraintInput, SubsystemNb3snCopperOkConstraintOutput]):
    name: str = "magnet_subsystem__subsystem__nb3sn__copper_ok__a4ff5a6abedecdd2"
    version: str = "v0.1"

    CONSTRAINT_ID = "magnet_subsystem__subsystem__nb3sn__copper_ok__a4ff5a6abedecdd2"

    def run(self, cu_margin_in: float) -> ModuleResult[SubsystemNb3snCopperOkConstraintOutput]:
        SubsystemNb3snCopperOkConstraintInput(cu_margin_in=cu_margin_in)  # validate every resolved formal
        body = constraint_pred_definition_magnet_conductor_alternatives__protection_copper_allowance(cu_margin_in=cu_margin_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=SubsystemNb3snCopperOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"cu_margin_in": float(cu_margin_in)},
                )
            )
        )
