"""Staged_Static_LoadsModule Module Wrapper

TEAx module for Staged_Static_Loads calculation.

The plant's own static cold and intercept terms, evaluated for Round 1's cold-stage load without the 10-30 K guard of the plant's thermal-inventory body. area_cold = n_coils_in * c_coil_in * 4 * (wp_side_in + 2 * t_case_in) (m2); q_radiation = area_cold * eps_eff_in * sigma_SB_in * (T_shield_in^4 - T_cold_in^4) (W, at the design's cold temperature); conduction_ref = n_coils_in * g_per_coil_in * k_c_in * (T_shield_in - T_conduction_ref_in) (W, support conduction on the k_c segment basis, which the cold-stage load scales by the NIST 316 integral ratio); shield_static = shield_area_ratio_in * area_cold * q_MLI_in - q_radiation + n_coils_in * g_per_coil_in * k_s_in * (T_amb_in - T_shield_in) - conduction_ref (W, the intercept's static load); p_joint_ref = p_fixed_MW_in * 1e6 (W, joint losses at the reference current). Nuclear heating of the cold mass (coordinator amendment A2): q_structure_nuclear = q_nuc_structure_in * m_support_in / rho_structure_in (W, the plant's structure-nuclear term, models/library/analyses/mfe_cryo_inventory.sysml 'Cold Load Sum'); nuclear_density_eff = q_nuc_in + q_structure_nuclear / vol_cold_in (W/m3 over the winding-pack cold volume), so the cold-stage load's nuclear term nuclear_density_eff * vol_cold equals the winding-pack term plus the structure term, and equals q_nuc * vol_cold exactly when q_nuc_structure is zero. At 20 K and the Stellaris design these reproduce the pinned inventory's 266.68 W radiation, 590.28 W conduction and 7,561.69 W intercept static load. **Source**: models/library/analyses/mfe_cryo_inventory.sysml **Reference**: 'Coil Thermal Inventory' equations, lines 11-16 (WI-059 D3-D4); WI-100 design section 2.4. **Basis**: [AGENT] reviewed design; plant equations reused unchanged. **Last Updated**: 2026-09-30

Inputs:
    - T_shield_in: T_shield_in parameter
    - q_nuc_structure_in: q_nuc_structure_in parameter
    - T_cold_in: T_cold_in parameter
    - wp_side_in: wp_side_in parameter
    - T_amb_in: T_amb_in parameter
    - k_s_in: k_s_in parameter
    - k_c_in: k_c_in parameter
    - m_support_in: m_support_in parameter
    - eps_eff_in: eps_eff_in parameter
    - t_case_in: t_case_in parameter
    - g_per_coil_in: g_per_coil_in parameter
    - q_MLI_in: q_MLI_in parameter
    - c_coil_in: c_coil_in parameter
    - p_fixed_MW_in: p_fixed_MW_in parameter
    - n_coils_in: n_coils_in parameter
    - T_conduction_ref_in: T_conduction_ref_in parameter
    - sigma_SB_in: sigma_SB_in parameter
    - vol_cold_in: vol_cold_in parameter
    - rho_structure_in: rho_structure_in parameter
    - q_nuc_in: q_nuc_in parameter
    - shield_area_ratio_in: shield_area_ratio_in parameter

Outputs:
    - nuclear_density_eff: nuclear_density_eff result
    - q_structure_nuclear: q_structure_nuclear result
    - conduction_ref: conduction_ref result
    - area_cold: area_cold result
    - p_joint_ref: p_joint_ref result
    - q_radiation: q_radiation result
    - shield_static: shield_static result

SysML Source: root-0/analyses/magnet_material_variants.sysml:48

SysML Source: root-0/analyses/magnet_material_variants.sysml:48

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/magnet_material_variants/staged_static_loads_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_nb3sn_tea.primitives import Float
from stellarator_materials_nb3sn_tea.schemas.staged_static_loads_output import Staged_Static_LoadsOutput


class Staged_Static_LoadsInput(BaseModel):
    """Input model for Staged_Static_LoadsModule.

    Attributes:
        T_shield_in: T_shield_in input
        q_nuc_structure_in: q_nuc_structure_in input
        T_cold_in: T_cold_in input
        wp_side_in: wp_side_in input
        T_amb_in: T_amb_in input
        k_s_in: k_s_in input
        k_c_in: k_c_in input
        m_support_in: m_support_in input
        eps_eff_in: eps_eff_in input
        t_case_in: t_case_in input
        g_per_coil_in: g_per_coil_in input
        q_MLI_in: q_MLI_in input
        c_coil_in: c_coil_in input
        p_fixed_MW_in: p_fixed_MW_in input
        n_coils_in: n_coils_in input
        T_conduction_ref_in: T_conduction_ref_in input
        sigma_SB_in: sigma_SB_in input
        vol_cold_in: vol_cold_in input
        rho_structure_in: rho_structure_in input
        q_nuc_in: q_nuc_in input
        shield_area_ratio_in: shield_area_ratio_in input
    """
    T_shield_in: float = Field(..., description="T_shield_in input")
    q_nuc_structure_in: float = Field(..., description="q_nuc_structure_in input")
    T_cold_in: float = Field(..., description="T_cold_in input")
    wp_side_in: float = Field(..., description="wp_side_in input")
    T_amb_in: float = Field(..., description="T_amb_in input")
    k_s_in: float = Field(..., description="k_s_in input")
    k_c_in: float = Field(..., description="k_c_in input")
    m_support_in: float = Field(..., description="m_support_in input")
    eps_eff_in: float = Field(..., description="eps_eff_in input")
    t_case_in: float = Field(..., description="t_case_in input")
    g_per_coil_in: float = Field(..., description="g_per_coil_in input")
    q_MLI_in: float = Field(..., description="q_MLI_in input")
    c_coil_in: float = Field(..., description="c_coil_in input")
    p_fixed_MW_in: float = Field(..., description="p_fixed_MW_in input")
    n_coils_in: float = Field(..., description="n_coils_in input")
    T_conduction_ref_in: float = Field(..., description="T_conduction_ref_in input")
    sigma_SB_in: float = Field(..., description="sigma_SB_in input")
    vol_cold_in: float = Field(..., description="vol_cold_in input")
    rho_structure_in: float = Field(..., description="rho_structure_in input")
    q_nuc_in: float = Field(..., description="q_nuc_in input")
    shield_area_ratio_in: float = Field(..., description="shield_area_ratio_in input")


class Staged_Static_LoadsModule(ModuleBase[Staged_Static_LoadsInput, Staged_Static_LoadsOutput]):
    """TEAx module for Staged_Static_Loads calculation.

The plant's own static cold and intercept terms, evaluated for Round 1's cold-stage load without the 10-30 K guard of the plant's thermal-inventory body. area_cold = n_coils_in * c_coil_in * 4 * (wp_side_in + 2 * t_case_in) (m2); q_radiation = area_cold * eps_eff_in * sigma_SB_in * (T_shield_in^4 - T_cold_in^4) (W, at the design's cold temperature); conduction_ref = n_coils_in * g_per_coil_in * k_c_in * (T_shield_in - T_conduction_ref_in) (W, support conduction on the k_c segment basis, which the cold-stage load scales by the NIST 316 integral ratio); shield_static = shield_area_ratio_in * area_cold * q_MLI_in - q_radiation + n_coils_in * g_per_coil_in * k_s_in * (T_amb_in - T_shield_in) - conduction_ref (W, the intercept's static load); p_joint_ref = p_fixed_MW_in * 1e6 (W, joint losses at the reference current). Nuclear heating of the cold mass (coordinator amendment A2): q_structure_nuclear = q_nuc_structure_in * m_support_in / rho_structure_in (W, the plant's structure-nuclear term, models/library/analyses/mfe_cryo_inventory.sysml 'Cold Load Sum'); nuclear_density_eff = q_nuc_in + q_structure_nuclear / vol_cold_in (W/m3 over the winding-pack cold volume), so the cold-stage load's nuclear term nuclear_density_eff * vol_cold equals the winding-pack term plus the structure term, and equals q_nuc * vol_cold exactly when q_nuc_structure is zero. At 20 K and the Stellaris design these reproduce the pinned inventory's 266.68 W radiation, 590.28 W conduction and 7,561.69 W intercept static load. **Source**: models/library/analyses/mfe_cryo_inventory.sysml **Reference**: 'Coil Thermal Inventory' equations, lines 11-16 (WI-059 D3-D4); WI-100 design section 2.4. **Basis**: [AGENT] reviewed design; plant equations reused unchanged. **Last Updated**: 2026-09-30

Inputs:
    - T_shield_in: T_shield_in parameter
    - q_nuc_structure_in: q_nuc_structure_in parameter
    - T_cold_in: T_cold_in parameter
    - wp_side_in: wp_side_in parameter
    - T_amb_in: T_amb_in parameter
    - k_s_in: k_s_in parameter
    - k_c_in: k_c_in parameter
    - m_support_in: m_support_in parameter
    - eps_eff_in: eps_eff_in parameter
    - t_case_in: t_case_in parameter
    - g_per_coil_in: g_per_coil_in parameter
    - q_MLI_in: q_MLI_in parameter
    - c_coil_in: c_coil_in parameter
    - p_fixed_MW_in: p_fixed_MW_in parameter
    - n_coils_in: n_coils_in parameter
    - T_conduction_ref_in: T_conduction_ref_in parameter
    - sigma_SB_in: sigma_SB_in parameter
    - vol_cold_in: vol_cold_in parameter
    - rho_structure_in: rho_structure_in parameter
    - q_nuc_in: q_nuc_in parameter
    - shield_area_ratio_in: shield_area_ratio_in parameter

Outputs:
    - nuclear_density_eff: nuclear_density_eff result
    - q_structure_nuclear: q_structure_nuclear result
    - conduction_ref: conduction_ref result
    - area_cold: area_cold result
    - p_joint_ref: p_joint_ref result
    - q_radiation: q_radiation result
    - shield_static: shield_static result

SysML Source: root-0/analyses/magnet_material_variants.sysml:48

    SysML Source: root-0/analyses/magnet_material_variants.sysml:48

    Calculation Specification:
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

    IMPLEMENTATION: See stellarator_materials_nb3sn_tea.handwritten.magnet_material_variants.staged_static_loads_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts nuclear_density_eff, q_structure_nuclear, conduction_ref, area_cold, p_joint_ref, q_radiation, shield_static fields to separate channels.
    """

    name: str = "Staged_Static_LoadsModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, T_shield_in: float, q_nuc_structure_in: float, T_cold_in: float, wp_side_in: float, T_amb_in: float, k_s_in: float, k_c_in: float, m_support_in: float, eps_eff_in: float, t_case_in: float, g_per_coil_in: float, q_MLI_in: float, c_coil_in: float, p_fixed_MW_in: float, n_coils_in: float, T_conduction_ref_in: float, sigma_SB_in: float, vol_cold_in: float, rho_structure_in: float, q_nuc_in: float, shield_area_ratio_in: float    ) -> Staged_Static_LoadsInput:
        """Validate inputs and fill defaults.

        Args:
            T_shield_in: T_shield_in input
            q_nuc_structure_in: q_nuc_structure_in input
            T_cold_in: T_cold_in input
            wp_side_in: wp_side_in input
            T_amb_in: T_amb_in input
            k_s_in: k_s_in input
            k_c_in: k_c_in input
            m_support_in: m_support_in input
            eps_eff_in: eps_eff_in input
            t_case_in: t_case_in input
            g_per_coil_in: g_per_coil_in input
            q_MLI_in: q_MLI_in input
            c_coil_in: c_coil_in input
            p_fixed_MW_in: p_fixed_MW_in input
            n_coils_in: n_coils_in input
            T_conduction_ref_in: T_conduction_ref_in input
            sigma_SB_in: sigma_SB_in input
            vol_cold_in: vol_cold_in input
            rho_structure_in: rho_structure_in input
            q_nuc_in: q_nuc_in input
            shield_area_ratio_in: shield_area_ratio_in input

        Returns:
            Validated input model
        """
        return Staged_Static_LoadsInput(T_shield_in=T_shield_in, q_nuc_structure_in=q_nuc_structure_in, T_cold_in=T_cold_in, wp_side_in=wp_side_in, T_amb_in=T_amb_in, k_s_in=k_s_in, k_c_in=k_c_in, m_support_in=m_support_in, eps_eff_in=eps_eff_in, t_case_in=t_case_in, g_per_coil_in=g_per_coil_in, q_MLI_in=q_MLI_in, c_coil_in=c_coil_in, p_fixed_MW_in=p_fixed_MW_in, n_coils_in=n_coils_in, T_conduction_ref_in=T_conduction_ref_in, sigma_SB_in=sigma_SB_in, vol_cold_in=vol_cold_in, rho_structure_in=rho_structure_in, q_nuc_in=q_nuc_in, shield_area_ratio_in=shield_area_ratio_in)

    def run(
        self, T_shield_in: float, q_nuc_structure_in: float, T_cold_in: float, wp_side_in: float, T_amb_in: float, k_s_in: float, k_c_in: float, m_support_in: float, eps_eff_in: float, t_case_in: float, g_per_coil_in: float, q_MLI_in: float, c_coil_in: float, p_fixed_MW_in: float, n_coils_in: float, T_conduction_ref_in: float, sigma_SB_in: float, vol_cold_in: float, rho_structure_in: float, q_nuc_in: float, shield_area_ratio_in: float    ) -> ModuleResult[Staged_Static_LoadsOutput]:
        """Execute calculation.

        Args:
            T_shield_in: T_shield_in input
            q_nuc_structure_in: q_nuc_structure_in input
            T_cold_in: T_cold_in input
            wp_side_in: wp_side_in input
            T_amb_in: T_amb_in input
            k_s_in: k_s_in input
            k_c_in: k_c_in input
            m_support_in: m_support_in input
            eps_eff_in: eps_eff_in input
            t_case_in: t_case_in input
            g_per_coil_in: g_per_coil_in input
            q_MLI_in: q_MLI_in input
            c_coil_in: c_coil_in input
            p_fixed_MW_in: p_fixed_MW_in input
            n_coils_in: n_coils_in input
            T_conduction_ref_in: T_conduction_ref_in input
            sigma_SB_in: sigma_SB_in input
            vol_cold_in: vol_cold_in input
            rho_structure_in: rho_structure_in input
            q_nuc_in: q_nuc_in input
            shield_area_ratio_in: shield_area_ratio_in input

        Returns:
            Module result with Staged_Static_LoadsOutput (nuclear_density_eff, q_structure_nuclear, conduction_ref, area_cold, p_joint_ref, q_radiation, shield_static)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(T_shield_in, q_nuc_structure_in, T_cold_in, wp_side_in, T_amb_in, k_s_in, k_c_in, m_support_in, eps_eff_in, t_case_in, g_per_coil_in, q_MLI_in, c_coil_in, p_fixed_MW_in, n_coils_in, T_conduction_ref_in, sigma_SB_in, vol_cold_in, rho_structure_in, q_nuc_in, shield_area_ratio_in)

        # Import handwritten implementation
        from stellarator_materials_nb3sn_tea.handwritten.magnet_material_variants.staged_static_loads_impl import (
            run_staged_static_loads,
        )

        # Execute implementation - returns tuple of values
        nuclear_density_eff, q_structure_nuclear, conduction_ref, area_cold, p_joint_ref, q_radiation, shield_static = run_staged_static_loads(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Staged_Static_LoadsOutput(
                nuclear_density_eff=nuclear_density_eff,
                q_structure_nuclear=q_structure_nuclear,
                conduction_ref=conduction_ref,
                area_cold=area_cold,
                p_joint_ref=p_joint_ref,
                q_radiation=q_radiation,
                shield_static=shield_static,
            )
        )
