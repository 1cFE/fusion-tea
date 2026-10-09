from pydantic import Field
from simkit.config.schema import MultiOutput

class Magnet_Cold_Stage_LoadOutput(MultiOutput):
    """Multi-output container for Magnet_Cold_Stage_Load.

Cold-stage and 77 K intercept loads at the supply temperature. K(T) = integral from T to T_shield of k_316 dT, with log10 k = sum_i c_i*(log10 T)^i over the NIST coefficients k_a..k_i (i = 0..8), integrated by composite Simpson over 2000 intervals in ln T. q_conduction = conduction_ref*K(T_supply)/K(T_conduction_ref); q_radiation = radiation_ref (temperature-independent from the 77 K shield); q_nuclear = nuclear_density*cold_volume; q_leads = f_lead*n_leads*|I|*sqrt(L0*(T_shield^2 - T_supply^2)); q_joints = p_joint_ref*(I/I_joint_ref)^2; q_cold = load_multiplier*(q_nuclear + q_radiation + q_conduction + q_leads + q_joints); q_shield = shield_static + f_lead*n_leads*|I|*sqrt(L0*(T_amb^2 - T_shield^2)); k_integral = K(T_supply) in W/m. Circulator work, helium inventory and AC losses are excluded (contract section 6). **Source**: knowledge/sources/nist_316_stainless_cryogenic_material_properties/output.md; knowledge/sources/current_leads_and_superconducting_links_ballarino_cern/; knowledge/sources/koncar_et_al_2017_heat_loads_and_design_temperature/ **Reference**: NIST 316 conductivity fit coefficients a-i (output.md:24-32, data range 4-300 K); Ballarino slide 14 minimum-heat-leak form; Končar Eq. 1 and Table 1 (PDF pp.3-5); work/active/WI-099_magnet-conductor-alternatives/design.md section 2.5; contract section 6. **Basis**: [AGENT] staged static and nuclear cold-load inventory; resistive-lead optimum applied equally to both materials. Body: exploration/magnet_materials/bodies/magnet_conductor_alternatives/magnet_cold_stage_load_impl.py. **Last Updated**: 2026-09-29

SysML Source: root-0/analyses/magnet_conductor_alternatives.sysml:166
    """
    q_cold: float = Field(description="q_cold output")
    q_conduction: float = Field(description="q_conduction output")
    q_shield: float = Field(description="q_shield output")
    q_nuclear: float = Field(description="q_nuclear output")
    q_radiation: float = Field(description="q_radiation output")
    q_leads: float = Field(description="q_leads output")
    k_integral: float = Field(description="k_integral output")
    q_joints: float = Field(description="q_joints output")
