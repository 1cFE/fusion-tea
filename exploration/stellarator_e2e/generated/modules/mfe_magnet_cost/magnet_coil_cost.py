"""Magnet_Coil_CostModule Module Wrapper

TEAx module for Magnet_Coil_Cost calculation.

Superconducting magnet/coil capital cost from the bilinear toroidal
conductor-quantity model, concept-agnostic across MFE approaches.

  total_kAm = G * B * R0 * r_coil / (mu0 * 1000)
  capital_cost = total_kAm * cost_per_kAm * coil_markup

The ampere-meter quantity follows Ampere's law around the torus
(ampere-turns ~ B*R0) times the conductor length per turn (~ coil-bore
radius r_coil). The expensive superconductor dominates SC coil cost, so
cost = conductor quantity * $/kA-m * a manufacturing markup (winding,
quench protection, cryostat, testing).

Fully parameterized (MR-WI009-8): G, B, R0, r_coil, cost_per_kAm, and
coil_markup are all inputs -- the concept sets them in WI-011. See the
reconciliation note below for the current 1costingFE values.

Note on units: the 1costingFE source divides the conductor cost by 1e6
to express M$ (cas22.py:442). This calc omits that conversion, so
capital_cost inherits the units of cost_per_kAm (i.e. $ when
cost_per_kAm is $/kA-m). Apply the M$ scaling downstream if desired.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
*Ref**: cas22.py:427 (total_kAm), cas22.py:441-444 (SC coil cost)
*Basis**: MFE coil conductor-quantity cost model; magnet cost rises
with B, R0, r_coil (SV-018)

Inputs:
    - coil_markup: coil_markup parameter
    - mu0: mu0 parameter
    - cost_per_kAm: cost_per_kAm parameter
    - G: G parameter
    - r_coil: r_coil parameter
    - B: B parameter
    - R0: R0 parameter

Outputs:
    - capital_cost: capital_cost result

SysML Source: root-0/analyses/mfe_magnet_cost.sysml:4

SysML Source: root-0/analyses/mfe_magnet_cost.sysml:4

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_magnet_cost/magnet_coil_cost_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float


class Magnet_Coil_CostInput(BaseModel):
    """Input model for Magnet_Coil_CostModule.

    Attributes:
        coil_markup: coil_markup input
        mu0: mu0 input
        cost_per_kAm: cost_per_kAm input
        G: G input
        r_coil: r_coil input
        B: B input
        R0: R0 input
    """
    coil_markup: float = Field(..., description="coil_markup input")
    mu0: float = Field(..., description="mu0 input")
    cost_per_kAm: float = Field(..., description="cost_per_kAm input")
    G: float = Field(..., description="G input")
    r_coil: float = Field(..., description="r_coil input")
    B: float = Field(..., description="B input")
    R0: float = Field(..., description="R0 input")


class Magnet_Coil_CostModule(ModuleBase[Magnet_Coil_CostInput, Float]):
    """TEAx module for Magnet_Coil_Cost calculation.

Superconducting magnet/coil capital cost from the bilinear toroidal
conductor-quantity model, concept-agnostic across MFE approaches.

  total_kAm = G * B * R0 * r_coil / (mu0 * 1000)
  capital_cost = total_kAm * cost_per_kAm * coil_markup

The ampere-meter quantity follows Ampere's law around the torus
(ampere-turns ~ B*R0) times the conductor length per turn (~ coil-bore
radius r_coil). The expensive superconductor dominates SC coil cost, so
cost = conductor quantity * $/kA-m * a manufacturing markup (winding,
quench protection, cryostat, testing).

Fully parameterized (MR-WI009-8): G, B, R0, r_coil, cost_per_kAm, and
coil_markup are all inputs -- the concept sets them in WI-011. See the
reconciliation note below for the current 1costingFE values.

Note on units: the 1costingFE source divides the conductor cost by 1e6
to express M$ (cas22.py:442). This calc omits that conversion, so
capital_cost inherits the units of cost_per_kAm (i.e. $ when
cost_per_kAm is $/kA-m). Apply the M$ scaling downstream if desired.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
*Ref**: cas22.py:427 (total_kAm), cas22.py:441-444 (SC coil cost)
*Basis**: MFE coil conductor-quantity cost model; magnet cost rises
with B, R0, r_coil (SV-018)

Inputs:
    - coil_markup: coil_markup parameter
    - mu0: mu0 parameter
    - cost_per_kAm: cost_per_kAm parameter
    - G: G parameter
    - r_coil: r_coil parameter
    - B: B parameter
    - R0: R0 parameter

Outputs:
    - capital_cost: capital_cost result

SysML Source: root-0/analyses/mfe_magnet_cost.sysml:4

    SysML Source: root-0/analyses/mfe_magnet_cost.sysml:4

    Calculation Specification:
        mu0 = 1.25663706212e-06
        total_kAm = G * B * R0 * r_coil / (mu0 * 1000.0)
        capital_cost = total_kAm * cost_per_kAm * coil_markup
        
Documentation:
Superconducting magnet/coil capital cost from the bilinear toroidal
conductor-quantity model, concept-agnostic across MFE approaches.

  total_kAm = G * B * R0 * r_coil / (mu0 * 1000)
  capital_cost = total_kAm * cost_per_kAm * coil_markup

The ampere-meter quantity follows Ampere's law around the torus
(ampere-turns ~ B*R0) times the conductor length per turn (~ coil-bore
radius r_coil). The expensive superconductor dominates SC coil cost, so
cost = conductor quantity * $/kA-m * a manufacturing markup (winding,
quench protection, cryostat, testing).

Fully parameterized (MR-WI009-8): G, B, R0, r_coil, cost_per_kAm, and
coil_markup are all inputs -- the concept sets them in WI-011. See the
reconciliation note below for the current 1costingFE values.

Note on units: the 1costingFE source divides the conductor cost by 1e6
to express M$ (cas22.py:442). This calc omits that conversion, so
capital_cost inherits the units of cost_per_kAm (i.e. $ when
cost_per_kAm is $/kA-m). Apply the M$ scaling downstream if desired.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
*Ref**: cas22.py:427 (total_kAm), cas22.py:441-444 (SC coil cost)
*Basis**: MFE coil conductor-quantity cost model; magnet cost rises
with B, R0, r_coil (SV-018)

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_magnet_cost.magnet_coil_cost_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "Magnet_Coil_CostModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, coil_markup: float, mu0: float, cost_per_kAm: float, G: float, r_coil: float, B: float, R0: float    ) -> Magnet_Coil_CostInput:
        """Validate inputs and fill defaults.

        Args:
            coil_markup: coil_markup input
            mu0: mu0 input
            cost_per_kAm: cost_per_kAm input
            G: G input
            r_coil: r_coil input
            B: B input
            R0: R0 input

        Returns:
            Validated input model
        """
        return Magnet_Coil_CostInput(coil_markup=coil_markup, mu0=mu0, cost_per_kAm=cost_per_kAm, G=G, r_coil=r_coil, B=B, R0=R0)

    def run(
        self, coil_markup: float, mu0: float, cost_per_kAm: float, G: float, r_coil: float, B: float, R0: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            coil_markup: coil_markup input
            mu0: mu0 input
            cost_per_kAm: cost_per_kAm input
            G: G input
            r_coil: r_coil input
            B: B input
            R0: R0 input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(coil_markup, mu0, cost_per_kAm, G, r_coil, B, R0)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_magnet_cost.magnet_coil_cost_impl import (
            run_magnet_coil_cost,
        )

        # Execute implementation - returns single value
        capital_cost = run_magnet_coil_cost(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(capital_cost))
