"""Constraint module for stellarator_09_materials__nb3sn_material__magnet__copper_ok__be9121bc3fcdea7a (Item 7 / D2/D3/D9).

Effective predicate: magnet_material_variants::'Nb3Sn Magnet System'::copper_ok in owner instance stellarator_09_materials__nb3sn_material__magnet.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_nb3sn_tea.schemas.constraint_types import ConstraintEvaluation
from stellarator_materials_nb3sn_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_magnet_conductor_alternatives__protection_copper_allowance


class Nb3snMaterialMagnetCopperOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    cu_margin_in: float


class Nb3snMaterialMagnetCopperOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class Nb3snMaterialMagnetCopperOkConstraintModule(ModuleBase[Nb3snMaterialMagnetCopperOkConstraintInput, Nb3snMaterialMagnetCopperOkConstraintOutput]):
    name: str = "stellarator_09_materials__nb3sn_material__magnet__copper_ok__be9121bc3fcdea7a"
    version: str = "v0.1"

    CONSTRAINT_ID = "stellarator_09_materials__nb3sn_material__magnet__copper_ok__be9121bc3fcdea7a"

    def run(self, cu_margin_in: float) -> ModuleResult[Nb3snMaterialMagnetCopperOkConstraintOutput]:
        Nb3snMaterialMagnetCopperOkConstraintInput(cu_margin_in=cu_margin_in)  # validate every resolved formal
        body = constraint_pred_definition_magnet_conductor_alternatives__protection_copper_allowance(cu_margin_in=cu_margin_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=Nb3snMaterialMagnetCopperOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"cu_margin_in": float(cu_margin_in)},
                )
            )
        )
