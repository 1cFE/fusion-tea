"""Constraint module for stellarator_09_materials__nb3sn_material__net_positive__2ff2061dd70a24f7 (Item 7 / D2/D3/D9).

Effective predicate: mfe_plant::'MFE Power Plant'::net_positive in owner instance stellarator_09_materials__nb3sn_material.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_nb3sn_tea.schemas.constraint_types import ConstraintEvaluation
from stellarator_materials_nb3sn_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_mfe_viability__net_power_positive


class Nb3snMaterialNetPositiveConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    net_electric: float


class Nb3snMaterialNetPositiveConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class Nb3snMaterialNetPositiveConstraintModule(ModuleBase[Nb3snMaterialNetPositiveConstraintInput, Nb3snMaterialNetPositiveConstraintOutput]):
    name: str = "stellarator_09_materials__nb3sn_material__net_positive__2ff2061dd70a24f7"
    version: str = "v0.1"

    CONSTRAINT_ID = "stellarator_09_materials__nb3sn_material__net_positive__2ff2061dd70a24f7"

    def run(self, net_electric: float) -> ModuleResult[Nb3snMaterialNetPositiveConstraintOutput]:
        Nb3snMaterialNetPositiveConstraintInput(net_electric=net_electric)  # validate every resolved formal
        body = constraint_pred_definition_mfe_viability__net_power_positive(net_electric=net_electric)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=Nb3snMaterialNetPositiveConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"net_electric": float(net_electric)},
                )
            )
        )
