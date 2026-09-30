"""Magnet_Cold_Stage_LoadModule Module Wrapper

TEAx module for Magnet_Cold_Stage_Load calculation.

Cold-stage and 77 K intercept loads at the supply temperature. K(T) = integral from T to T_shield of k_316 dT, with log10 k = sum_i c_i*(log10 T)^i over the NIST coefficients k_a..k_i (i = 0..8), integrated by composite Simpson over 2000 intervals in ln T. q_conduction = conduction_ref*K(T_supply)/K(T_conduction_ref); q_radiation = radiation_ref (temperature-independent from the 77 K shield); q_nuclear = nuclear_density*cold_volume; q_leads = f_lead*n_leads*|I|*sqrt(L0*(T_shield^2 - T_supply^2)); q_joints = p_joint_ref*(I/I_joint_ref)^2; q_cold = load_multiplier*(q_nuclear + q_radiation + q_conduction + q_leads + q_joints); q_shield = shield_static + f_lead*n_leads*|I|*sqrt(L0*(T_amb^2 - T_shield^2)); k_integral = K(T_supply) in W/m. Circulator work, helium inventory and AC losses are excluded (contract section 6). **Source**: knowledge/sources/nist_316_stainless_cryogenic_material_properties/output.md; knowledge/sources/current_leads_and_superconducting_links_ballarino_cern/; knowledge/sources/koncar_et_al_2017_heat_loads_and_design_temperature/ **Reference**: NIST 316 conductivity fit coefficients a-i (output.md:24-32, data range 4-300 K); Ballarino slide 14 minimum-heat-leak form; Končar Eq. 1 and Table 1 (PDF pp.3-5); work/active/WI-099_magnet-conductor-alternatives/design.md section 2.5; contract section 6. **Basis**: [AGENT] staged static and nuclear cold-load inventory; resistive-lead optimum applied equally to both materials. Body: exploration/magnet_materials/bodies/magnet_conductor_alternatives/magnet_cold_stage_load_impl.py. **Last Updated**: 2026-09-29

Inputs:
    - load_multiplier_in: load_multiplier_in parameter
    - k_f_in: k_f_in parameter
    - T_supply_in: T_supply_in parameter
    - k_e_in: k_e_in parameter
    - turn_current_in: turn_current_in parameter
    - k_a_in: k_a_in parameter
    - T_shield_in: T_shield_in parameter
    - nuclear_density_in: nuclear_density_in parameter
    - k_i_in: k_i_in parameter
    - k_g_in: k_g_in parameter
    - radiation_ref_in: radiation_ref_in parameter
    - cold_volume_in: cold_volume_in parameter
    - p_joint_ref_in: p_joint_ref_in parameter
    - f_lead_in: f_lead_in parameter
    - I_joint_ref_in: I_joint_ref_in parameter
    - conduction_ref_in: conduction_ref_in parameter
    - shield_static_in: shield_static_in parameter
    - T_amb_in: T_amb_in parameter
    - L0_in: L0_in parameter
    - k_c_in: k_c_in parameter
    - T_conduction_ref_in: T_conduction_ref_in parameter
    - k_h_in: k_h_in parameter
    - n_leads_in: n_leads_in parameter
    - k_d_in: k_d_in parameter
    - k_b_in: k_b_in parameter

Outputs:
    - q_cold: q_cold result
    - q_conduction: q_conduction result
    - q_shield: q_shield result
    - q_nuclear: q_nuclear result
    - q_radiation: q_radiation result
    - q_leads: q_leads result
    - k_integral: k_integral result
    - q_joints: q_joints result

SysML Source: root-0/magnet_conductor_alternatives.sysml:166

SysML Source: root-0/magnet_conductor_alternatives.sysml:166

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/magnet_conductor_alternatives/magnet_cold_stage_load_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from magnet_materials_tea.primitives import Float
from magnet_materials_tea.schemas.magnet_cold_stage_load_output import Magnet_Cold_Stage_LoadOutput


class Magnet_Cold_Stage_LoadInput(BaseModel):
    """Input model for Magnet_Cold_Stage_LoadModule.

    Attributes:
        load_multiplier_in: load_multiplier_in input
        k_f_in: k_f_in input
        T_supply_in: T_supply_in input
        k_e_in: k_e_in input
        turn_current_in: turn_current_in input
        k_a_in: k_a_in input
        T_shield_in: T_shield_in input
        nuclear_density_in: nuclear_density_in input
        k_i_in: k_i_in input
        k_g_in: k_g_in input
        radiation_ref_in: radiation_ref_in input
        cold_volume_in: cold_volume_in input
        p_joint_ref_in: p_joint_ref_in input
        f_lead_in: f_lead_in input
        I_joint_ref_in: I_joint_ref_in input
        conduction_ref_in: conduction_ref_in input
        shield_static_in: shield_static_in input
        T_amb_in: T_amb_in input
        L0_in: L0_in input
        k_c_in: k_c_in input
        T_conduction_ref_in: T_conduction_ref_in input
        k_h_in: k_h_in input
        n_leads_in: n_leads_in input
        k_d_in: k_d_in input
        k_b_in: k_b_in input
    """
    load_multiplier_in: float = Field(..., description="load_multiplier_in input")
    k_f_in: float = Field(..., description="k_f_in input")
    T_supply_in: float = Field(..., description="T_supply_in input")
    k_e_in: float = Field(..., description="k_e_in input")
    turn_current_in: float = Field(..., description="turn_current_in input")
    k_a_in: float = Field(..., description="k_a_in input")
    T_shield_in: float = Field(..., description="T_shield_in input")
    nuclear_density_in: float = Field(..., description="nuclear_density_in input")
    k_i_in: float = Field(..., description="k_i_in input")
    k_g_in: float = Field(..., description="k_g_in input")
    radiation_ref_in: float = Field(..., description="radiation_ref_in input")
    cold_volume_in: float = Field(..., description="cold_volume_in input")
    p_joint_ref_in: float = Field(..., description="p_joint_ref_in input")
    f_lead_in: float = Field(..., description="f_lead_in input")
    I_joint_ref_in: float = Field(..., description="I_joint_ref_in input")
    conduction_ref_in: float = Field(..., description="conduction_ref_in input")
    shield_static_in: float = Field(..., description="shield_static_in input")
    T_amb_in: float = Field(..., description="T_amb_in input")
    L0_in: float = Field(..., description="L0_in input")
    k_c_in: float = Field(..., description="k_c_in input")
    T_conduction_ref_in: float = Field(..., description="T_conduction_ref_in input")
    k_h_in: float = Field(..., description="k_h_in input")
    n_leads_in: float = Field(..., description="n_leads_in input")
    k_d_in: float = Field(..., description="k_d_in input")
    k_b_in: float = Field(..., description="k_b_in input")


class Magnet_Cold_Stage_LoadModule(ModuleBase[Magnet_Cold_Stage_LoadInput, Magnet_Cold_Stage_LoadOutput]):
    """TEAx module for Magnet_Cold_Stage_Load calculation.

Cold-stage and 77 K intercept loads at the supply temperature. K(T) = integral from T to T_shield of k_316 dT, with log10 k = sum_i c_i*(log10 T)^i over the NIST coefficients k_a..k_i (i = 0..8), integrated by composite Simpson over 2000 intervals in ln T. q_conduction = conduction_ref*K(T_supply)/K(T_conduction_ref); q_radiation = radiation_ref (temperature-independent from the 77 K shield); q_nuclear = nuclear_density*cold_volume; q_leads = f_lead*n_leads*|I|*sqrt(L0*(T_shield^2 - T_supply^2)); q_joints = p_joint_ref*(I/I_joint_ref)^2; q_cold = load_multiplier*(q_nuclear + q_radiation + q_conduction + q_leads + q_joints); q_shield = shield_static + f_lead*n_leads*|I|*sqrt(L0*(T_amb^2 - T_shield^2)); k_integral = K(T_supply) in W/m. Circulator work, helium inventory and AC losses are excluded (contract section 6). **Source**: knowledge/sources/nist_316_stainless_cryogenic_material_properties/output.md; knowledge/sources/current_leads_and_superconducting_links_ballarino_cern/; knowledge/sources/koncar_et_al_2017_heat_loads_and_design_temperature/ **Reference**: NIST 316 conductivity fit coefficients a-i (output.md:24-32, data range 4-300 K); Ballarino slide 14 minimum-heat-leak form; Končar Eq. 1 and Table 1 (PDF pp.3-5); work/active/WI-099_magnet-conductor-alternatives/design.md section 2.5; contract section 6. **Basis**: [AGENT] staged static and nuclear cold-load inventory; resistive-lead optimum applied equally to both materials. Body: exploration/magnet_materials/bodies/magnet_conductor_alternatives/magnet_cold_stage_load_impl.py. **Last Updated**: 2026-09-29

Inputs:
    - load_multiplier_in: load_multiplier_in parameter
    - k_f_in: k_f_in parameter
    - T_supply_in: T_supply_in parameter
    - k_e_in: k_e_in parameter
    - turn_current_in: turn_current_in parameter
    - k_a_in: k_a_in parameter
    - T_shield_in: T_shield_in parameter
    - nuclear_density_in: nuclear_density_in parameter
    - k_i_in: k_i_in parameter
    - k_g_in: k_g_in parameter
    - radiation_ref_in: radiation_ref_in parameter
    - cold_volume_in: cold_volume_in parameter
    - p_joint_ref_in: p_joint_ref_in parameter
    - f_lead_in: f_lead_in parameter
    - I_joint_ref_in: I_joint_ref_in parameter
    - conduction_ref_in: conduction_ref_in parameter
    - shield_static_in: shield_static_in parameter
    - T_amb_in: T_amb_in parameter
    - L0_in: L0_in parameter
    - k_c_in: k_c_in parameter
    - T_conduction_ref_in: T_conduction_ref_in parameter
    - k_h_in: k_h_in parameter
    - n_leads_in: n_leads_in parameter
    - k_d_in: k_d_in parameter
    - k_b_in: k_b_in parameter

Outputs:
    - q_cold: q_cold result
    - q_conduction: q_conduction result
    - q_shield: q_shield result
    - q_nuclear: q_nuclear result
    - q_radiation: q_radiation result
    - q_leads: q_leads result
    - k_integral: k_integral result
    - q_joints: q_joints result

SysML Source: root-0/magnet_conductor_alternatives.sysml:166

    SysML Source: root-0/magnet_conductor_alternatives.sysml:166

    Calculation Specification:
        T_supply_in = 0.0
        T_shield_in = 0.0
        T_amb_in = 0.0
        turn_current_in = 0.0
        nuclear_density_in = 0.0
        cold_volume_in = 0.0
        radiation_ref_in = 0.0
        conduction_ref_in = 0.0
        T_conduction_ref_in = 0.0
        k_a_in = 0.0
        k_b_in = 0.0
        k_c_in = 0.0
        k_d_in = 0.0
        k_e_in = 0.0
        k_f_in = 0.0
        k_g_in = 0.0
        k_h_in = 0.0
        k_i_in = 0.0
        n_leads_in = 0.0
        f_lead_in = 1.0
        L0_in = 0.0
        p_joint_ref_in = 0.0
        I_joint_ref_in = 1.0
        shield_static_in = 0.0
        load_multiplier_in = 1.0
        
Documentation:
Cold-stage and 77 K intercept loads at the supply temperature. K(T) = integral from T to T_shield of k_316 dT, with log10 k = sum_i c_i*(log10 T)^i over the NIST coefficients k_a..k_i (i = 0..8), integrated by composite Simpson over 2000 intervals in ln T. q_conduction = conduction_ref*K(T_supply)/K(T_conduction_ref); q_radiation = radiation_ref (temperature-independent from the 77 K shield); q_nuclear = nuclear_density*cold_volume; q_leads = f_lead*n_leads*|I|*sqrt(L0*(T_shield^2 - T_supply^2)); q_joints = p_joint_ref*(I/I_joint_ref)^2; q_cold = load_multiplier*(q_nuclear + q_radiation + q_conduction + q_leads + q_joints); q_shield = shield_static + f_lead*n_leads*|I|*sqrt(L0*(T_amb^2 - T_shield^2)); k_integral = K(T_supply) in W/m. Circulator work, helium inventory and AC losses are excluded (contract section 6). **Source**: knowledge/sources/nist_316_stainless_cryogenic_material_properties/output.md; knowledge/sources/current_leads_and_superconducting_links_ballarino_cern/; knowledge/sources/koncar_et_al_2017_heat_loads_and_design_temperature/ **Reference**: NIST 316 conductivity fit coefficients a-i (output.md:24-32, data range 4-300 K); Ballarino slide 14 minimum-heat-leak form; Končar Eq. 1 and Table 1 (PDF pp.3-5); work/active/WI-099_magnet-conductor-alternatives/design.md section 2.5; contract section 6. **Basis**: [AGENT] staged static and nuclear cold-load inventory; resistive-lead optimum applied equally to both materials. Body: exploration/magnet_materials/bodies/magnet_conductor_alternatives/magnet_cold_stage_load_impl.py. **Last Updated**: 2026-09-29

    IMPLEMENTATION: See magnet_materials_tea.handwritten.magnet_conductor_alternatives.magnet_cold_stage_load_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts q_cold, q_conduction, q_shield, q_nuclear, q_radiation, q_leads, k_integral, q_joints fields to separate channels.
    """

    name: str = "Magnet_Cold_Stage_LoadModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, load_multiplier_in: float, k_f_in: float, T_supply_in: float, k_e_in: float, turn_current_in: float, k_a_in: float, T_shield_in: float, nuclear_density_in: float, k_i_in: float, k_g_in: float, radiation_ref_in: float, cold_volume_in: float, p_joint_ref_in: float, f_lead_in: float, I_joint_ref_in: float, conduction_ref_in: float, shield_static_in: float, T_amb_in: float, L0_in: float, k_c_in: float, T_conduction_ref_in: float, k_h_in: float, n_leads_in: float, k_d_in: float, k_b_in: float    ) -> Magnet_Cold_Stage_LoadInput:
        """Validate inputs and fill defaults.

        Args:
            load_multiplier_in: load_multiplier_in input
            k_f_in: k_f_in input
            T_supply_in: T_supply_in input
            k_e_in: k_e_in input
            turn_current_in: turn_current_in input
            k_a_in: k_a_in input
            T_shield_in: T_shield_in input
            nuclear_density_in: nuclear_density_in input
            k_i_in: k_i_in input
            k_g_in: k_g_in input
            radiation_ref_in: radiation_ref_in input
            cold_volume_in: cold_volume_in input
            p_joint_ref_in: p_joint_ref_in input
            f_lead_in: f_lead_in input
            I_joint_ref_in: I_joint_ref_in input
            conduction_ref_in: conduction_ref_in input
            shield_static_in: shield_static_in input
            T_amb_in: T_amb_in input
            L0_in: L0_in input
            k_c_in: k_c_in input
            T_conduction_ref_in: T_conduction_ref_in input
            k_h_in: k_h_in input
            n_leads_in: n_leads_in input
            k_d_in: k_d_in input
            k_b_in: k_b_in input

        Returns:
            Validated input model
        """
        return Magnet_Cold_Stage_LoadInput(load_multiplier_in=load_multiplier_in, k_f_in=k_f_in, T_supply_in=T_supply_in, k_e_in=k_e_in, turn_current_in=turn_current_in, k_a_in=k_a_in, T_shield_in=T_shield_in, nuclear_density_in=nuclear_density_in, k_i_in=k_i_in, k_g_in=k_g_in, radiation_ref_in=radiation_ref_in, cold_volume_in=cold_volume_in, p_joint_ref_in=p_joint_ref_in, f_lead_in=f_lead_in, I_joint_ref_in=I_joint_ref_in, conduction_ref_in=conduction_ref_in, shield_static_in=shield_static_in, T_amb_in=T_amb_in, L0_in=L0_in, k_c_in=k_c_in, T_conduction_ref_in=T_conduction_ref_in, k_h_in=k_h_in, n_leads_in=n_leads_in, k_d_in=k_d_in, k_b_in=k_b_in)

    def run(
        self, load_multiplier_in: float, k_f_in: float, T_supply_in: float, k_e_in: float, turn_current_in: float, k_a_in: float, T_shield_in: float, nuclear_density_in: float, k_i_in: float, k_g_in: float, radiation_ref_in: float, cold_volume_in: float, p_joint_ref_in: float, f_lead_in: float, I_joint_ref_in: float, conduction_ref_in: float, shield_static_in: float, T_amb_in: float, L0_in: float, k_c_in: float, T_conduction_ref_in: float, k_h_in: float, n_leads_in: float, k_d_in: float, k_b_in: float    ) -> ModuleResult[Magnet_Cold_Stage_LoadOutput]:
        """Execute calculation.

        Args:
            load_multiplier_in: load_multiplier_in input
            k_f_in: k_f_in input
            T_supply_in: T_supply_in input
            k_e_in: k_e_in input
            turn_current_in: turn_current_in input
            k_a_in: k_a_in input
            T_shield_in: T_shield_in input
            nuclear_density_in: nuclear_density_in input
            k_i_in: k_i_in input
            k_g_in: k_g_in input
            radiation_ref_in: radiation_ref_in input
            cold_volume_in: cold_volume_in input
            p_joint_ref_in: p_joint_ref_in input
            f_lead_in: f_lead_in input
            I_joint_ref_in: I_joint_ref_in input
            conduction_ref_in: conduction_ref_in input
            shield_static_in: shield_static_in input
            T_amb_in: T_amb_in input
            L0_in: L0_in input
            k_c_in: k_c_in input
            T_conduction_ref_in: T_conduction_ref_in input
            k_h_in: k_h_in input
            n_leads_in: n_leads_in input
            k_d_in: k_d_in input
            k_b_in: k_b_in input

        Returns:
            Module result with Magnet_Cold_Stage_LoadOutput (q_cold, q_conduction, q_shield, q_nuclear, q_radiation, q_leads, k_integral, q_joints)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(load_multiplier_in, k_f_in, T_supply_in, k_e_in, turn_current_in, k_a_in, T_shield_in, nuclear_density_in, k_i_in, k_g_in, radiation_ref_in, cold_volume_in, p_joint_ref_in, f_lead_in, I_joint_ref_in, conduction_ref_in, shield_static_in, T_amb_in, L0_in, k_c_in, T_conduction_ref_in, k_h_in, n_leads_in, k_d_in, k_b_in)

        # Import handwritten implementation
        from magnet_materials_tea.handwritten.magnet_conductor_alternatives.magnet_cold_stage_load_impl import (
            run_magnet_cold_stage_load,
        )

        # Execute implementation - returns tuple of values
        q_cold, q_conduction, q_shield, q_nuclear, q_radiation, q_leads, k_integral, q_joints = run_magnet_cold_stage_load(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Magnet_Cold_Stage_LoadOutput(
                q_cold=q_cold,
                q_conduction=q_conduction,
                q_shield=q_shield,
                q_nuclear=q_nuclear,
                q_radiation=q_radiation,
                q_leads=q_leads,
                k_integral=k_integral,
                q_joints=q_joints,
            )
        )
