"""WI-059 native thermal inventory; authority mfe_cryo_inventory.sysml."""
import math
from stellarator_materials_reference_tea.modules.mfe_cryo_inventory.coil_thermal_inventory import Coil_Thermal_InventoryInput

AUTO_IMPLEMENTED = False


def run_coil_thermal_inventory(inputs: Coil_Thermal_InventoryInput) -> tuple[float, float, float, float, float, float, float, float, float, float, float]:
    """Return W heat, m2 area and MW direct drive in generated output order."""
    if not inputs.inventory_enabled:
        return (0.0,) * 11
    for name, value in vars(inputs).items():
        if name != "inventory_enabled" and not math.isfinite(value):
            raise ValueError(f"Coil Thermal Inventory: {name} must be finite")
    if inputs.L0 <= 0.0 or inputs.sigma_SB <= 0.0:
        raise ValueError("Coil Thermal Inventory: L0 and sigma_SB must be positive")
    nonnegative = ("n_coils", "c_coil", "wp_side", "n_leads", "f_lead", "t_case", "shield_area_ratio", "eps_eff", "q_MLI", "g_per_coil", "k_c", "k_s", "p_joint", "joint_drive_fraction")
    if any(getattr(inputs, name) < 0.0 for name in nonnegative):
        raise ValueError("Coil Thermal Inventory: geometry and load factors must be nonnegative")
    if not (inputs.T_shield == 77.0 and inputs.T_amb == 300.0 and 10.0 <= inputs.T_cold <= 30.0):
        raise ValueError("Coil Thermal Inventory: require 10 <= T_cold <= 30, T_shield=77, T_amb=300 K")
    if not (0.0 < inputs.f_carnot_cold <= 1.0 and 0.0 < inputs.f_carnot_shield <= 1.0):
        raise ValueError("Coil Thermal Inventory: require Carnot fractions in (0, 1]")
    if not 0.0 <= inputs.eps_eff <= 1.0 or not 0.0 <= inputs.joint_drive_fraction <= 1.0:
        raise ValueError("Coil Thermal Inventory: emissivity and joint fraction must be in [0, 1]")
    area_cold = inputs.n_coils * inputs.c_coil * 4.0 * (inputs.wp_side + 2.0 * inputs.t_case)
    area_shield = inputs.shield_area_ratio * area_cold
    lead_scale = inputs.f_lead * inputs.n_leads * abs(inputs.I_turn)
    q_lead_cold = lead_scale * math.sqrt(inputs.L0 * (inputs.T_shield**2 - inputs.T_cold**2))
    q_lead_shield = lead_scale * math.sqrt(inputs.L0 * (inputs.T_amb**2 - inputs.T_shield**2))
    q_rad_cold = area_cold * inputs.eps_eff * inputs.sigma_SB * (inputs.T_shield**4 - inputs.T_cold**4)
    q_rad_shield = area_shield * inputs.q_MLI - q_rad_cold
    conductance_geometry = inputs.n_coils * inputs.g_per_coil
    q_support_cold = conductance_geometry * inputs.k_c * (inputs.T_shield - inputs.T_cold)
    q_support_shield = conductance_geometry * inputs.k_s * (inputs.T_amb - inputs.T_shield) - q_support_cold
    q_inventory_cold = q_lead_cold + q_rad_cold + q_support_cold
    q_inventory_shield = q_lead_shield + q_rad_shield + q_support_shield
    if q_inventory_shield < 0.0:
        raise ValueError("Coil Thermal Inventory: negative warm net load")
    p_drive = (q_lead_cold + q_lead_shield) * 1e-6 + inputs.joint_drive_fraction * inputs.p_joint
    if not all(math.isfinite(v) for v in (area_cold, area_shield, q_inventory_cold, q_inventory_shield, p_drive)):
        raise ValueError("Coil Thermal Inventory: nonfinite derived load")
    return (q_rad_cold, q_rad_shield, q_lead_shield, q_support_cold, q_inventory_shield,
            q_lead_cold, area_shield, q_support_shield, q_inventory_cold, area_cold, p_drive)
