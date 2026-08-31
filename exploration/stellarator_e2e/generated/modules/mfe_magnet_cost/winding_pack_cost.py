"""Winding_Pack_CostModule Module Wrapper

TEAx module for Winding_Pack_Cost calculation.

Winding-pack capital [$] over the REAL winding length (WI-035 D4):

  kAm_wind = n_coils * I_coil * f_set * c_coil / 1000
  cost     = kAm_wind * cost_per_kAm * f_wp_fab

Replaces the proxy length 4*pi*r_coil (a bore-radius stand-in,
WI-032) with the coil count x set-mean current x printed typical
circumference. f_wp_fab is the winding fabrication markup
(content: winding, insulation, cooling, jointing, test --
costing_constants.yaml:50 -- times the documented NCSX non-planar
production penalty, yaml:60-66). Quench protection carries no
separate account: the NI coils are passively protected (printed,
sec. 2.9).

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml (pin 0254385);
knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md
*Ref**: costing_constants.yaml:50 (fab content), :60-72 (5.87 =
3.09 x 1.9 NCSX penalty; path factor separate); cas22.py:34
("conductor is ~10-15% of finished magnet cost" -- cross-check);
images/page_022_table_0.png (Table 8 per-coil currents);
raw.pdf sec. 2.9 (25 m typical circumference; NI passive quench
protection)
*Basis**: conductor quantity over real winding length x $/kA-m x
content-mapped fabrication markup; concept-agnostic (MR-3)

Inputs:
    - I_coil: I_coil parameter
    - c_coil: c_coil parameter
    - cost_per_kAm: cost_per_kAm parameter
    - n_coils: n_coils parameter
    - f_set: f_set parameter
    - f_wp_fab: f_wp_fab parameter

Outputs:
    - cost: cost result

SysML Source: root-0/analyses/mfe_magnet_cost.sysml:56

SysML Source: root-0/analyses/mfe_magnet_cost.sysml:56

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_magnet_cost/winding_pack_cost_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float


class Winding_Pack_CostInput(BaseModel):
    """Input model for Winding_Pack_CostModule.

    Attributes:
        I_coil: I_coil input
        c_coil: c_coil input
        cost_per_kAm: cost_per_kAm input
        n_coils: n_coils input
        f_set: f_set input
        f_wp_fab: f_wp_fab input
    """
    I_coil: float = Field(..., description="I_coil input")
    c_coil: float = Field(..., description="c_coil input")
    cost_per_kAm: float = Field(..., description="cost_per_kAm input")
    n_coils: float = Field(..., description="n_coils input")
    f_set: float = Field(..., description="f_set input")
    f_wp_fab: float = Field(..., description="f_wp_fab input")


class Winding_Pack_CostModule(ModuleBase[Winding_Pack_CostInput, Float]):
    """TEAx module for Winding_Pack_Cost calculation.

Winding-pack capital [$] over the REAL winding length (WI-035 D4):

  kAm_wind = n_coils * I_coil * f_set * c_coil / 1000
  cost     = kAm_wind * cost_per_kAm * f_wp_fab

Replaces the proxy length 4*pi*r_coil (a bore-radius stand-in,
WI-032) with the coil count x set-mean current x printed typical
circumference. f_wp_fab is the winding fabrication markup
(content: winding, insulation, cooling, jointing, test --
costing_constants.yaml:50 -- times the documented NCSX non-planar
production penalty, yaml:60-66). Quench protection carries no
separate account: the NI coils are passively protected (printed,
sec. 2.9).

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml (pin 0254385);
knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md
*Ref**: costing_constants.yaml:50 (fab content), :60-72 (5.87 =
3.09 x 1.9 NCSX penalty; path factor separate); cas22.py:34
("conductor is ~10-15% of finished magnet cost" -- cross-check);
images/page_022_table_0.png (Table 8 per-coil currents);
raw.pdf sec. 2.9 (25 m typical circumference; NI passive quench
protection)
*Basis**: conductor quantity over real winding length x $/kA-m x
content-mapped fabrication markup; concept-agnostic (MR-3)

Inputs:
    - I_coil: I_coil parameter
    - c_coil: c_coil parameter
    - cost_per_kAm: cost_per_kAm parameter
    - n_coils: n_coils parameter
    - f_set: f_set parameter
    - f_wp_fab: f_wp_fab parameter

Outputs:
    - cost: cost result

SysML Source: root-0/analyses/mfe_magnet_cost.sysml:56

    SysML Source: root-0/analyses/mfe_magnet_cost.sysml:56

    Calculation Specification:
        kAm_wind = n_coils * I_coil * f_set * c_coil / 1000.0
        cost = kAm_wind * cost_per_kAm * f_wp_fab
        
Documentation:
Winding-pack capital [$] over the REAL winding length (WI-035 D4):

  kAm_wind = n_coils * I_coil * f_set * c_coil / 1000
  cost     = kAm_wind * cost_per_kAm * f_wp_fab

Replaces the proxy length 4*pi*r_coil (a bore-radius stand-in,
WI-032) with the coil count x set-mean current x printed typical
circumference. f_wp_fab is the winding fabrication markup
(content: winding, insulation, cooling, jointing, test --
costing_constants.yaml:50 -- times the documented NCSX non-planar
production penalty, yaml:60-66). Quench protection carries no
separate account: the NI coils are passively protected (printed,
sec. 2.9).

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml (pin 0254385);
knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md
*Ref**: costing_constants.yaml:50 (fab content), :60-72 (5.87 =
3.09 x 1.9 NCSX penalty; path factor separate); cas22.py:34
("conductor is ~10-15% of finished magnet cost" -- cross-check);
images/page_022_table_0.png (Table 8 per-coil currents);
raw.pdf sec. 2.9 (25 m typical circumference; NI passive quench
protection)
*Basis**: conductor quantity over real winding length x $/kA-m x
content-mapped fabrication markup; concept-agnostic (MR-3)

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_magnet_cost.winding_pack_cost_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "Winding_Pack_CostModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, I_coil: float, c_coil: float, cost_per_kAm: float, n_coils: float, f_set: float, f_wp_fab: float    ) -> Winding_Pack_CostInput:
        """Validate inputs and fill defaults.

        Args:
            I_coil: I_coil input
            c_coil: c_coil input
            cost_per_kAm: cost_per_kAm input
            n_coils: n_coils input
            f_set: f_set input
            f_wp_fab: f_wp_fab input

        Returns:
            Validated input model
        """
        return Winding_Pack_CostInput(I_coil=I_coil, c_coil=c_coil, cost_per_kAm=cost_per_kAm, n_coils=n_coils, f_set=f_set, f_wp_fab=f_wp_fab)

    def run(
        self, I_coil: float, c_coil: float, cost_per_kAm: float, n_coils: float, f_set: float, f_wp_fab: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            I_coil: I_coil input
            c_coil: c_coil input
            cost_per_kAm: cost_per_kAm input
            n_coils: n_coils input
            f_set: f_set input
            f_wp_fab: f_wp_fab input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(I_coil, c_coil, cost_per_kAm, n_coils, f_set, f_wp_fab)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_magnet_cost.winding_pack_cost_impl import (
            run_winding_pack_cost,
        )

        # Execute implementation - returns single value
        cost = run_winding_pack_cost(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(cost))
