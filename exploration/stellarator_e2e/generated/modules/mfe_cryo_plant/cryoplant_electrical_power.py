"""Cryoplant_Electrical_PowerModule Module Wrapper

TEAx module for Cryoplant_Electrical_Power calculation.

Cryoplant wall-plug electrical power [MW] from the cold-mass heat
load (WI-024). Steady-state refrigeration power balance:
    p_cold = (q_nuc * vol_cold * 1e-6 + p_fixed) * f_uplift
    COP    = f_carnot * T_cold / (T_amb - T_cold)   (Carnot x fraction)
    p_elec = p_cold / COP + p_direct
p_direct is an additive direct term for concepts that specify the
cryoplant electrical outright (no chain); with zero heat inputs the
calc passes p_direct through exactly. f_uplift names the seam for
heat loads missing from the inventory (>= 1). Dormant-safe defaults:
an unbound concept computes p_elec = 0; f_carnot defaults 1.0 (not 0)
so the dormant COP stays defined — the mode is selected by the heat
inputs, never by the efficiency (WI-022 T_i0 precedent).
Output feeds the power-balance p_cryo slot ("cryogenic system
power"), which 1costingFE's own defaults document as the cryoplant
wall-plug electrical.
*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/physics.py
*Ref**: physics.py:321-323 (p_cryo in the recirculating sum);
steady_state_dipole.yaml:52-53 (slot semantics: "Cryogenic
wall-plug power" = heat load x plant efficiency — semantics
witness only, value inadmissible)
*Basis**: reversed-Carnot reference cycle x fraction-of-Carnot;
concept-agnostic (MR-3) — all values bound by instances

Inputs:
    - q_nuc: q_nuc parameter
    - vol_cold: vol_cold parameter
    - p_fixed: p_fixed parameter
    - f_uplift: f_uplift parameter
    - T_cold: T_cold parameter
    - T_amb: T_amb parameter
    - f_carnot: f_carnot parameter
    - p_direct: p_direct parameter

Outputs:
    - p_elec: p_elec result

SysML Source: /home/reid/1cfe/fusion-tea-stellarator-mbse-demo/exploration/stellarator_e2e/models/analyses/mfe_cryo_plant.sysml:4

SysML Source: /home/reid/1cfe/fusion-tea-stellarator-mbse-demo/exploration/stellarator_e2e/models/analyses/mfe_cryo_plant.sysml:4

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_cryo_plant/cryoplant_electrical_power_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float


class Cryoplant_Electrical_PowerInput(BaseModel):
    """Input model for Cryoplant_Electrical_PowerModule.

    Attributes:
        q_nuc: q_nuc input
        vol_cold: vol_cold input
        p_fixed: p_fixed input
        f_uplift: f_uplift input
        T_cold: T_cold input
        T_amb: T_amb input
        f_carnot: f_carnot input
        p_direct: p_direct input
    """
    q_nuc: float = Field(..., description="q_nuc input")
    vol_cold: float = Field(..., description="vol_cold input")
    p_fixed: float = Field(..., description="p_fixed input")
    f_uplift: float = Field(..., description="f_uplift input")
    T_cold: float = Field(..., description="T_cold input")
    T_amb: float = Field(..., description="T_amb input")
    f_carnot: float = Field(..., description="f_carnot input")
    p_direct: float = Field(..., description="p_direct input")


class Cryoplant_Electrical_PowerModule(ModuleBase[Cryoplant_Electrical_PowerInput, Float]):
    """TEAx module for Cryoplant_Electrical_Power calculation.

Cryoplant wall-plug electrical power [MW] from the cold-mass heat
load (WI-024). Steady-state refrigeration power balance:
    p_cold = (q_nuc * vol_cold * 1e-6 + p_fixed) * f_uplift
    COP    = f_carnot * T_cold / (T_amb - T_cold)   (Carnot x fraction)
    p_elec = p_cold / COP + p_direct
p_direct is an additive direct term for concepts that specify the
cryoplant electrical outright (no chain); with zero heat inputs the
calc passes p_direct through exactly. f_uplift names the seam for
heat loads missing from the inventory (>= 1). Dormant-safe defaults:
an unbound concept computes p_elec = 0; f_carnot defaults 1.0 (not 0)
so the dormant COP stays defined — the mode is selected by the heat
inputs, never by the efficiency (WI-022 T_i0 precedent).
Output feeds the power-balance p_cryo slot ("cryogenic system
power"), which 1costingFE's own defaults document as the cryoplant
wall-plug electrical.
*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/physics.py
*Ref**: physics.py:321-323 (p_cryo in the recirculating sum);
steady_state_dipole.yaml:52-53 (slot semantics: "Cryogenic
wall-plug power" = heat load x plant efficiency — semantics
witness only, value inadmissible)
*Basis**: reversed-Carnot reference cycle x fraction-of-Carnot;
concept-agnostic (MR-3) — all values bound by instances

Inputs:
    - q_nuc: q_nuc parameter
    - vol_cold: vol_cold parameter
    - p_fixed: p_fixed parameter
    - f_uplift: f_uplift parameter
    - T_cold: T_cold parameter
    - T_amb: T_amb parameter
    - f_carnot: f_carnot parameter
    - p_direct: p_direct parameter

Outputs:
    - p_elec: p_elec result

SysML Source: /home/reid/1cfe/fusion-tea-stellarator-mbse-demo/exploration/stellarator_e2e/models/analyses/mfe_cryo_plant.sysml:4

    SysML Source: /home/reid/1cfe/fusion-tea-stellarator-mbse-demo/exploration/stellarator_e2e/models/analyses/mfe_cryo_plant.sysml:4

    Calculation Specification:
        q_nuc = 0.0
        vol_cold = 0.0
        p_fixed = 0.0
        f_uplift = 1.0
        T_cold = 20.0
        T_amb = 300.0
        f_carnot = 1.0
        p_direct = 0.0
        p_cold = (q_nuc * vol_cold * 1e-06 + p_fixed) * f_uplift
        cop_carnot = T_cold / (T_amb - T_cold)
        cop = f_carnot * cop_carnot
        p_elec = p_cold / cop + p_direct
        
Documentation:
Cryoplant wall-plug electrical power [MW] from the cold-mass heat
load (WI-024). Steady-state refrigeration power balance:
    p_cold = (q_nuc * vol_cold * 1e-6 + p_fixed) * f_uplift
    COP    = f_carnot * T_cold / (T_amb - T_cold)   (Carnot x fraction)
    p_elec = p_cold / COP + p_direct
p_direct is an additive direct term for concepts that specify the
cryoplant electrical outright (no chain); with zero heat inputs the
calc passes p_direct through exactly. f_uplift names the seam for
heat loads missing from the inventory (>= 1). Dormant-safe defaults:
an unbound concept computes p_elec = 0; f_carnot defaults 1.0 (not 0)
so the dormant COP stays defined — the mode is selected by the heat
inputs, never by the efficiency (WI-022 T_i0 precedent).
Output feeds the power-balance p_cryo slot ("cryogenic system
power"), which 1costingFE's own defaults document as the cryoplant
wall-plug electrical.
*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/physics.py
*Ref**: physics.py:321-323 (p_cryo in the recirculating sum);
steady_state_dipole.yaml:52-53 (slot semantics: "Cryogenic
wall-plug power" = heat load x plant efficiency — semantics
witness only, value inadmissible)
*Basis**: reversed-Carnot reference cycle x fraction-of-Carnot;
concept-agnostic (MR-3) — all values bound by instances

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_cryo_plant.cryoplant_electrical_power_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "Cryoplant_Electrical_PowerModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, q_nuc: float, vol_cold: float, p_fixed: float, f_uplift: float, T_cold: float, T_amb: float, f_carnot: float, p_direct: float    ) -> Cryoplant_Electrical_PowerInput:
        """Validate inputs and fill defaults.

        Args:
            q_nuc: q_nuc input
            vol_cold: vol_cold input
            p_fixed: p_fixed input
            f_uplift: f_uplift input
            T_cold: T_cold input
            T_amb: T_amb input
            f_carnot: f_carnot input
            p_direct: p_direct input

        Returns:
            Validated input model
        """
        return Cryoplant_Electrical_PowerInput(q_nuc=q_nuc, vol_cold=vol_cold, p_fixed=p_fixed, f_uplift=f_uplift, T_cold=T_cold, T_amb=T_amb, f_carnot=f_carnot, p_direct=p_direct)

    def run(
        self, q_nuc: float, vol_cold: float, p_fixed: float, f_uplift: float, T_cold: float, T_amb: float, f_carnot: float, p_direct: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            q_nuc: q_nuc input
            vol_cold: vol_cold input
            p_fixed: p_fixed input
            f_uplift: f_uplift input
            T_cold: T_cold input
            T_amb: T_amb input
            f_carnot: f_carnot input
            p_direct: p_direct input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(q_nuc, vol_cold, p_fixed, f_uplift, T_cold, T_amb, f_carnot, p_direct)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_cryo_plant.cryoplant_electrical_power_impl import (
            run_cryoplant_electrical_power,
        )

        # Execute implementation - returns single value
        p_elec = run_cryoplant_electrical_power(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(p_elec))
