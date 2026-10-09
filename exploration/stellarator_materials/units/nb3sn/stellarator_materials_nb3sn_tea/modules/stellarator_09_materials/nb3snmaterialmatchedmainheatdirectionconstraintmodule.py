"""Constraint module for stellarator_09_materials__nb3sn_material__matched_main_heat_direction__67f41575de96bd94 (Item 7 / D2/D3/D9).

Effective predicate: mfe_plant::'MFE Power Plant'::matched_main_heat_direction in owner instance stellarator_09_materials__nb3sn_material.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_nb3sn_tea.schemas.constraint_types import ConstraintEvaluation
from stellarator_materials_nb3sn_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_mfe_matched_steam_cycle__active_steam_heat_direction


class Nb3snMaterialMatchedMainHeatDirectionConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    enabled_in: float
    gap_in: float


class Nb3snMaterialMatchedMainHeatDirectionConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class Nb3snMaterialMatchedMainHeatDirectionConstraintModule(ModuleBase[Nb3snMaterialMatchedMainHeatDirectionConstraintInput, Nb3snMaterialMatchedMainHeatDirectionConstraintOutput]):
    name: str = "stellarator_09_materials__nb3sn_material__matched_main_heat_direction__67f41575de96bd94"
    version: str = "v0.1"

    CONSTRAINT_ID = "stellarator_09_materials__nb3sn_material__matched_main_heat_direction__67f41575de96bd94"

    def run(self, enabled_in: float, gap_in: float) -> ModuleResult[Nb3snMaterialMatchedMainHeatDirectionConstraintOutput]:
        Nb3snMaterialMatchedMainHeatDirectionConstraintInput(enabled_in=enabled_in, gap_in=gap_in)  # validate every resolved formal
        body = constraint_pred_definition_mfe_matched_steam_cycle__active_steam_heat_direction(enabled_in=enabled_in, gap_in=gap_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=Nb3snMaterialMatchedMainHeatDirectionConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"enabled_in": float(enabled_in), "gap_in": float(gap_in)},
                )
            )
        )
