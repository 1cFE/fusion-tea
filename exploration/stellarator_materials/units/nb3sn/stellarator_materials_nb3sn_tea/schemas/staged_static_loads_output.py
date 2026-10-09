from pydantic import Field
from simkit.config.schema import MultiOutput

class Staged_Static_LoadsOutput(MultiOutput):
    """Multi-output container for Staged_Static_Loads.

The plant's own static cold and intercept terms, evaluated for Round 1's cold-stage load without the 10-30 K guard of the plant's thermal-inventory body. area_cold = n_coils_in * c_coil_in * 4 * (wp_side_in + 2 * t_case_in) (m2); q_radiation = area_cold * eps_eff_in * sigma_SB_in * (T_shield_in^4 - T_cold_in^4) (W, at the design's cold temperature); conduction_ref = n_coils_in * g_per_coil_in * k_c_in * (T_shield_in - T_conduction_ref_in) (W, support conduction on the k_c segment basis, which the cold-stage load scales by the NIST 316 integral ratio); shield_static = shield_area_ratio_in * area_cold * q_MLI_in - q_radiation + n_coils_in * g_per_coil_in * k_s_in * (T_amb_in - T_shield_in) - conduction_ref (W, the intercept's static load); p_joint_ref = p_fixed_MW_in * 1e6 (W, joint losses at the reference current). Nuclear heating of the cold mass (coordinator amendment A2): q_structure_nuclear = q_nuc_structure_in * m_support_in / rho_structure_in (W, the plant's structure-nuclear term, models/library/analyses/mfe_cryo_inventory.sysml 'Cold Load Sum'); nuclear_density_eff = q_nuc_in + q_structure_nuclear / vol_cold_in (W/m3 over the winding-pack cold volume), so the cold-stage load's nuclear term nuclear_density_eff * vol_cold equals the winding-pack term plus the structure term, and equals q_nuc * vol_cold exactly when q_nuc_structure is zero. At 20 K and the Stellaris design these reproduce the pinned inventory's 266.68 W radiation, 590.28 W conduction and 7,561.69 W intercept static load. **Source**: models/library/analyses/mfe_cryo_inventory.sysml **Reference**: 'Coil Thermal Inventory' equations, lines 11-16 (WI-059 D3-D4); WI-100 design section 2.4. **Basis**: [AGENT] reviewed design; plant equations reused unchanged. **Last Updated**: 2026-09-30

SysML Source: root-0/analyses/magnet_material_variants.sysml:48
    """
    nuclear_density_eff: float = Field(description="nuclear_density_eff output")
    q_structure_nuclear: float = Field(description="q_structure_nuclear output")
    conduction_ref: float = Field(description="conduction_ref output")
    area_cold: float = Field(description="area_cold output")
    p_joint_ref: float = Field(description="p_joint_ref output")
    q_radiation: float = Field(description="q_radiation output")
    shield_static: float = Field(description="shield_static output")
