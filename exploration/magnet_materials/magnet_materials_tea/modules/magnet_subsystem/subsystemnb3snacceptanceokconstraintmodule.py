"""Constraint module for magnet_subsystem__subsystem__nb3sn__acceptance_ok__6ecc44a52542ba77 (Item 7 / D2/D3/D9).

Effective predicate: magnet_subsystem::subsystem::nb3sn::acceptance_ok in owner instance magnet_subsystem__subsystem__nb3sn.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from magnet_materials_tea.schemas.constraint_types import ConstraintEvaluation
from magnet_materials_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_magnet_conductor_alternatives__conductor_acceptance


class SubsystemNb3snAcceptanceOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    margin_in: float
    supported_in: float


class SubsystemNb3snAcceptanceOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class SubsystemNb3snAcceptanceOkConstraintModule(ModuleBase[SubsystemNb3snAcceptanceOkConstraintInput, SubsystemNb3snAcceptanceOkConstraintOutput]):
    name: str = "magnet_subsystem__subsystem__nb3sn__acceptance_ok__6ecc44a52542ba77"
    version: str = "v0.1"

    CONSTRAINT_ID = "magnet_subsystem__subsystem__nb3sn__acceptance_ok__6ecc44a52542ba77"

    def run(self, margin_in: float, supported_in: float) -> ModuleResult[SubsystemNb3snAcceptanceOkConstraintOutput]:
        SubsystemNb3snAcceptanceOkConstraintInput(margin_in=margin_in, supported_in=supported_in)  # validate every resolved formal
        body = constraint_pred_definition_magnet_conductor_alternatives__conductor_acceptance(supported_in=supported_in, margin_in=margin_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=SubsystemNb3snAcceptanceOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"supported_in": float(supported_in), "margin_in": float(margin_in)},
                )
            )
        )
