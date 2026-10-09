"""Auto-generated implementation for Staged_Static_Loads.

AUTO_IMPLEMENTED = True

SysML Source: root-0/analyses/magnet_material_variants.sysml:48

SysML Expressions:
    n_coils_in = 0.0
    c_coil_in = 0.0
    wp_side_in = 0.0
    t_case_in = 0.0
    shield_area_ratio_in = 1.0
    eps_eff_in = 0.0
    sigma_SB_in = 0.0
    q_MLI_in = 0.0
    g_per_coil_in = 0.0
    k_c_in = 0.0
    k_s_in = 0.0
    T_cold_in = 0.0
    T_shield_in = 77.0
    T_amb_in = 300.0
    T_conduction_ref_in = 0.0
    p_fixed_MW_in = 0.0
    q_nuc_in = 0.0
    vol_cold_in = 1.0
    q_nuc_structure_in = 0.0
    m_support_in = 0.0
    rho_structure_in = 1.0
    area_cold = n_coils_in * c_coil_in * 4.0 * (wp_side_in + 2.0 * t_case_in)
    q_radiation = area_cold * eps_eff_in * sigma_SB_in * (T_shield_in ** 4 - T_cold_in ** 4)
    conduction_ref = n_coils_in * g_per_coil_in * k_c_in * (T_shield_in - T_conduction_ref_in)
    shield_static = shield_area_ratio_in * area_cold * q_MLI_in - q_radiation + n_coils_in * g_per_coil_in * k_s_in * (T_amb_in - T_shield_in) - conduction_ref
    p_joint_ref = p_fixed_MW_in * 1000000.0
    q_structure_nuclear = q_nuc_structure_in * m_support_in / rho_structure_in
    nuclear_density_eff = q_nuc_in + q_structure_nuclear / vol_cold_in
    
Documentation:
The plant's own static cold and intercept terms, evaluated for Round 1's cold-stage load without the 10-30 K guard of the plant's thermal-inventory body. area_cold = n_coils_in * c_coil_in * 4 * (wp_side_in + 2 * t_case_in) (m2); q_radiation = area_cold * eps_eff_in * sigma_SB_in * (T_shield_in^4 - T_cold_in^4) (W, at the design's cold temperature); conduction_ref = n_coils_in * g_per_coil_in * k_c_in * (T_shield_in - T_conduction_ref_in) (W, support conduction on the k_c segment basis, which the cold-stage load scales by the NIST 316 integral ratio); shield_static = shield_area_ratio_in * area_cold * q_MLI_in - q_radiation + n_coils_in * g_per_coil_in * k_s_in * (T_amb_in - T_shield_in) - conduction_ref (W, the intercept's static load); p_joint_ref = p_fixed_MW_in * 1e6 (W, joint losses at the reference current). Nuclear heating of the cold mass (coordinator amendment A2): q_structure_nuclear = q_nuc_structure_in * m_support_in / rho_structure_in (W, the plant's structure-nuclear term, models/library/analyses/mfe_cryo_inventory.sysml 'Cold Load Sum'); nuclear_density_eff = q_nuc_in + q_structure_nuclear / vol_cold_in (W/m3 over the winding-pack cold volume), so the cold-stage load's nuclear term nuclear_density_eff * vol_cold equals the winding-pack term plus the structure term, and equals q_nuc * vol_cold exactly when q_nuc_structure is zero. At 20 K and the Stellaris design these reproduce the pinned inventory's 266.68 W radiation, 590.28 W conduction and 7,561.69 W intercept static load. **Source**: models/library/analyses/mfe_cryo_inventory.sysml **Reference**: 'Coil Thermal Inventory' equations, lines 11-16 (WI-059 D3-D4); WI-100 design section 2.4. **Basis**: [AGENT] reviewed design; plant equations reused unchanged. **Last Updated**: 2026-09-30
"""

AUTO_IMPLEMENTED = True

from stellarator_materials_nb3sn_tea.modules.magnet_material_variants.staged_static_loads import Staged_Static_LoadsInput


def run_staged_static_loads(inputs: Staged_Static_LoadsInput) -> tuple[float, float, float, float, float, float, float]:
    """Execute Staged_Static_Loads calculation.

The plant's own static cold and intercept terms, evaluated for Round 1's cold-stage load without the 10-30 K guard of the plant's thermal-inventory body. area_cold = n_coils_in * c_coil_in * 4 * (wp_side_in + 2 * t_case_in) (m2); q_radiation = area_cold * eps_eff_in * sigma_SB_in * (T_shield_in^4 - T_cold_in^4) (W, at the design's cold temperature); conduction_ref = n_coils_in * g_per_coil_in * k_c_in * (T_shield_in - T_conduction_ref_in) (W, support conduction on the k_c segment basis, which the cold-stage load scales by the NIST 316 integral ratio); shield_static = shield_area_ratio_in * area_cold * q_MLI_in - q_radiation + n_coils_in * g_per_coil_in * k_s_in * (T_amb_in - T_shield_in) - conduction_ref (W, the intercept's static load); p_joint_ref = p_fixed_MW_in * 1e6 (W, joint losses at the reference current). Nuclear heating of the cold mass (coordinator amendment A2): q_structure_nuclear = q_nuc_structure_in * m_support_in / rho_structure_in (W, the plant's structure-nuclear term, models/library/analyses/mfe_cryo_inventory.sysml 'Cold Load Sum'); nuclear_density_eff = q_nuc_in + q_structure_nuclear / vol_cold_in (W/m3 over the winding-pack cold volume), so the cold-stage load's nuclear term nuclear_density_eff * vol_cold equals the winding-pack term plus the structure term, and equals q_nuc * vol_cold exactly when q_nuc_structure is zero. At 20 K and the Stellaris design these reproduce the pinned inventory's 266.68 W radiation, 590.28 W conduction and 7,561.69 W intercept static load. **Source**: models/library/analyses/mfe_cryo_inventory.sysml **Reference**: 'Coil Thermal Inventory' equations, lines 11-16 (WI-059 D3-D4); WI-100 design section 2.4. **Basis**: [AGENT] reviewed design; plant equations reused unchanged. **Last Updated**: 2026-09-30

SysML Source: root-0/analyses/magnet_material_variants.sysml:48

SysML Expressions:
    n_coils_in = 0.0
    c_coil_in = 0.0
    wp_side_in = 0.0
    t_case_in = 0.0
    shield_area_ratio_in = 1.0
    eps_eff_in = 0.0
    sigma_SB_in = 0.0
    q_MLI_in = 0.0
    g_per_coil_in = 0.0
    k_c_in = 0.0
    k_s_in = 0.0
    T_cold_in = 0.0
    T_shield_in = 77.0
    T_amb_in = 300.0
    T_conduction_ref_in = 0.0
    p_fixed_MW_in = 0.0
    q_nuc_in = 0.0
    vol_cold_in = 1.0
    q_nuc_structure_in = 0.0
    m_support_in = 0.0
    rho_structure_in = 1.0
    area_cold = n_coils_in * c_coil_in * 4.0 * (wp_side_in + 2.0 * t_case_in)
    q_radiation = area_cold * eps_eff_in * sigma_SB_in * (T_shield_in ** 4 - T_cold_in ** 4)
    conduction_ref = n_coils_in * g_per_coil_in * k_c_in * (T_shield_in - T_conduction_ref_in)
    shield_static = shield_area_ratio_in * area_cold * q_MLI_in - q_radiation + n_coils_in * g_per_coil_in * k_s_in * (T_amb_in - T_shield_in) - conduction_ref
    p_joint_ref = p_fixed_MW_in * 1000000.0
    q_structure_nuclear = q_nuc_structure_in * m_support_in / rho_structure_in
    nuclear_density_eff = q_nuc_in + q_structure_nuclear / vol_cold_in
    
Documentation:
The plant's own static cold and intercept terms, evaluated for Round 1's cold-stage load without the 10-30 K guard of the plant's thermal-inventory body. area_cold = n_coils_in * c_coil_in * 4 * (wp_side_in + 2 * t_case_in) (m2); q_radiation = area_cold * eps_eff_in * sigma_SB_in * (T_shield_in^4 - T_cold_in^4) (W, at the design's cold temperature); conduction_ref = n_coils_in * g_per_coil_in * k_c_in * (T_shield_in - T_conduction_ref_in) (W, support conduction on the k_c segment basis, which the cold-stage load scales by the NIST 316 integral ratio); shield_static = shield_area_ratio_in * area_cold * q_MLI_in - q_radiation + n_coils_in * g_per_coil_in * k_s_in * (T_amb_in - T_shield_in) - conduction_ref (W, the intercept's static load); p_joint_ref = p_fixed_MW_in * 1e6 (W, joint losses at the reference current). Nuclear heating of the cold mass (coordinator amendment A2): q_structure_nuclear = q_nuc_structure_in * m_support_in / rho_structure_in (W, the plant's structure-nuclear term, models/library/analyses/mfe_cryo_inventory.sysml 'Cold Load Sum'); nuclear_density_eff = q_nuc_in + q_structure_nuclear / vol_cold_in (W/m3 over the winding-pack cold volume), so the cold-stage load's nuclear term nuclear_density_eff * vol_cold equals the winding-pack term plus the structure term, and equals q_nuc * vol_cold exactly when q_nuc_structure is zero. At 20 K and the Stellaris design these reproduce the pinned inventory's 266.68 W radiation, 590.28 W conduction and 7,561.69 W intercept static load. **Source**: models/library/analyses/mfe_cryo_inventory.sysml **Reference**: 'Coil Thermal Inventory' equations, lines 11-16 (WI-059 D3-D4); WI-100 design section 2.4. **Basis**: [AGENT] reviewed design; plant equations reused unchanged. **Last Updated**: 2026-09-30

Args:
    inputs: Input parameters validated against Staged_Static_LoadsInput schema

Returns:
    tuple[float, ...]: (nuclear_density_eff, q_structure_nuclear, conduction_ref, area_cold, p_joint_ref, q_radiation, shield_static)

Example:
    >>> inputs = Staged_Static_LoadsInput(...)
    >>> nuclear_density_eff, q_structure_nuclear, conduction_ref, area_cold, p_joint_ref, q_radiation, shield_static = run_staged_static_loads(inputs)
    """
    q_structure_nuclear = ((inputs.q_nuc_structure_in * inputs.m_support_in) / inputs.rho_structure_in)
    conduction_ref = (((inputs.n_coils_in * inputs.g_per_coil_in) * inputs.k_c_in) * (inputs.T_shield_in - inputs.T_conduction_ref_in))
    area_cold = (((inputs.n_coils_in * inputs.c_coil_in) * 4.0) * (inputs.wp_side_in + (2.0 * inputs.t_case_in)))
    q_radiation = (((area_cold * inputs.eps_eff_in) * inputs.sigma_SB_in) * ((inputs.T_shield_in ** 4) - (inputs.T_cold_in ** 4)))
    return (
        (inputs.q_nuc_in + (q_structure_nuclear / inputs.vol_cold_in)),  # nuclear_density_eff
        q_structure_nuclear,
        conduction_ref,
        area_cold,
        (inputs.p_fixed_MW_in * 1000000.0),  # p_joint_ref
        q_radiation,
        (((((inputs.shield_area_ratio_in * area_cold) * inputs.q_MLI_in) - q_radiation) + (((inputs.n_coils_in * inputs.g_per_coil_in) * inputs.k_s_in) * (inputs.T_amb_in - inputs.T_shield_in))) - conduction_ref),  # shield_static
    )
