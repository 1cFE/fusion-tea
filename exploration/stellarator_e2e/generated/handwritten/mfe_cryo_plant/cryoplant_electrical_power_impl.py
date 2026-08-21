"""Auto-generated implementation for Cryoplant_Electrical_Power.

AUTO_IMPLEMENTED = True

SysML Source: root-0/analyses/mfe_cryo_plant.sysml:4

SysML Expressions:
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
"""

AUTO_IMPLEMENTED = True

from stellarator_tea.modules.mfe_cryo_plant.cryoplant_electrical_power import Cryoplant_Electrical_PowerInput


def run_cryoplant_electrical_power(inputs: Cryoplant_Electrical_PowerInput) -> float:
    """Execute Cryoplant_Electrical_Power calculation.

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

SysML Source: root-0/analyses/mfe_cryo_plant.sysml:4

SysML Expressions:
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

Args:
    inputs: Input parameters validated against Cryoplant_Electrical_PowerInput schema

Returns:
    float: p_elec

Example:
    >>> inputs = Cryoplant_Electrical_PowerInput(...)
    >>> result = run_cryoplant_electrical_power(inputs)
    """
    cop_carnot = (inputs.T_cold / (inputs.T_amb - inputs.T_cold))
    cop = (inputs.f_carnot * cop_carnot)
    p_cold = ((((inputs.q_nuc * inputs.vol_cold) * 1e-06) + inputs.p_fixed) * inputs.f_uplift)
    return ((p_cold / cop) + inputs.p_direct)
