from pydantic import Field
from simkit.config.schema import MultiOutput

class Coil_Thermal_InventoryOutput(MultiOutput):
    """Multi-output container for Coil_Thermal_Inventory.

Explicit two-stage coil thermal inventory. All q outputs are W,
areas m^2 and p_drive MW. Native manual completion returns zero outputs
before arithmetic when inventory_enabled=false. Active domain:
T_shield=77, T_amb=300, 10<=T_cold<=30 K, both Carnot fractions (0,1].
Active numeric inputs finite; L0/sigma_SB positive; geometry/load factors
nonnegative, signed current permitted through abs; emissivity and joint
drive fraction in [0,1], derived loads finite.
A_c=n_coils*c_coil*4*(wp_side+2*t_case); A_s=shield_area_ratio*A_c.
Qlead=f_lead*n_leads*abs(I_turn)*sqrt(L0*(Th^2-Tl^2)) per segment.
Qrad_c=A_c*eps_eff*sigma_SB*(Ts^4-Tc^4); Qrad_s=A_s*q_MLI-Qrad_c.
G=n_coils*g_per_coil; Qsup_c=G*k_c*(Ts-Tc);
Qsup_s=G*k_s*(Ta-Ts)-Qsup_c. Reject total warm net heat
Qlead_s+Qrad_s+Qsup_s<0; individual signed transfers may be negative.
p_drive=(Qlead_c+Qlead_s)*1e-6+joint_drive_fraction*p_joint.
*Source**: knowledge/sources/current_leads_and_superconducting_links_ballarino_cern/;
knowledge/sources/nist_316_stainless_cryogenic_material_properties/;
knowledge/sources/layered_thermal_insulation_systems_for_cryogenic/
*Reference**: CERN slide14; NIST conductivity table; NASA slides20-21;
work/active/WI-059_coil-thermal-and-total-support-inventory/design.md D3-D4.
*Basis**: [AGENT] ideal-segment lead scenario with excess factor;
316 proxy for316LN and fixed segment means, cold10-30K approximation;
thermal bridge and surface geometry unqualified, not local stress sizing.
*Last Updated**: 2026-09-15

SysML Source: root-0/analyses/mfe_cryo_inventory.sysml:3
    """
    q_rad_cold: float = Field(description="q_rad_cold output")
    q_rad_shield: float = Field(description="q_rad_shield output")
    q_lead_shield: float = Field(description="q_lead_shield output")
    q_support_cold: float = Field(description="q_support_cold output")
    q_inventory_shield: float = Field(description="q_inventory_shield output")
    q_lead_cold: float = Field(description="q_lead_cold output")
    area_shield: float = Field(description="area_shield output")
    q_support_shield: float = Field(description="q_support_shield output")
    q_inventory_cold: float = Field(description="q_inventory_cold output")
    area_cold: float = Field(description="area_cold output")
    p_drive: float = Field(description="p_drive output")
