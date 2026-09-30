"""Coil_Thermal_InventoryModule Module Wrapper

TEAx module for Coil_Thermal_Inventory calculation.

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

Inputs:
    - T_amb: T_amb parameter
    - shield_area_ratio: shield_area_ratio parameter
    - f_carnot_cold: f_carnot_cold parameter
    - eps_eff: eps_eff parameter
    - g_per_coil: g_per_coil parameter
    - n_coils: n_coils parameter
    - L0: L0 parameter
    - k_s: k_s parameter
    - T_cold: T_cold parameter
    - c_coil: c_coil parameter
    - T_shield: T_shield parameter
    - I_turn: I_turn parameter
    - wp_side: wp_side parameter
    - q_MLI: q_MLI parameter
    - f_lead: f_lead parameter
    - k_c: k_c parameter
    - inventory_enabled: inventory_enabled parameter
    - n_leads: n_leads parameter
    - t_case: t_case parameter
    - f_carnot_shield: f_carnot_shield parameter
    - joint_drive_fraction: joint_drive_fraction parameter
    - p_joint: p_joint parameter
    - sigma_SB: sigma_SB parameter

Outputs:
    - q_rad_cold: q_rad_cold result
    - q_rad_shield: q_rad_shield result
    - q_lead_shield: q_lead_shield result
    - q_support_cold: q_support_cold result
    - q_inventory_shield: q_inventory_shield result
    - q_lead_cold: q_lead_cold result
    - area_shield: area_shield result
    - q_support_shield: q_support_shield result
    - q_inventory_cold: q_inventory_cold result
    - area_cold: area_cold result
    - p_drive: p_drive result

SysML Source: root-0/analyses/mfe_cryo_inventory.sysml:3

SysML Source: root-0/analyses/mfe_cryo_inventory.sysml:3

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_cryo_inventory/coil_thermal_inventory_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_rebco_tea.primitives import Float
from stellarator_materials_rebco_tea.schemas.coil_thermal_inventory_output import Coil_Thermal_InventoryOutput


class Coil_Thermal_InventoryInput(BaseModel):
    """Input model for Coil_Thermal_InventoryModule.

    Attributes:
        T_amb: T_amb input
        shield_area_ratio: shield_area_ratio input
        f_carnot_cold: f_carnot_cold input
        eps_eff: eps_eff input
        g_per_coil: g_per_coil input
        n_coils: n_coils input
        L0: L0 input
        k_s: k_s input
        T_cold: T_cold input
        c_coil: c_coil input
        T_shield: T_shield input
        I_turn: I_turn input
        wp_side: wp_side input
        q_MLI: q_MLI input
        f_lead: f_lead input
        k_c: k_c input
        inventory_enabled: inventory_enabled input
        n_leads: n_leads input
        t_case: t_case input
        f_carnot_shield: f_carnot_shield input
        joint_drive_fraction: joint_drive_fraction input
        p_joint: p_joint input
        sigma_SB: sigma_SB input
    """
    T_amb: float = Field(..., description="T_amb input")
    shield_area_ratio: float = Field(..., description="shield_area_ratio input")
    f_carnot_cold: float = Field(..., description="f_carnot_cold input")
    eps_eff: float = Field(..., description="eps_eff input")
    g_per_coil: float = Field(..., description="g_per_coil input")
    n_coils: float = Field(..., description="n_coils input")
    L0: float = Field(..., description="L0 input")
    k_s: float = Field(..., description="k_s input")
    T_cold: float = Field(..., description="T_cold input")
    c_coil: float = Field(..., description="c_coil input")
    T_shield: float = Field(..., description="T_shield input")
    I_turn: float = Field(..., description="I_turn input")
    wp_side: float = Field(..., description="wp_side input")
    q_MLI: float = Field(..., description="q_MLI input")
    f_lead: float = Field(..., description="f_lead input")
    k_c: float = Field(..., description="k_c input")
    inventory_enabled: bool = Field(..., description="inventory_enabled input")
    n_leads: float = Field(..., description="n_leads input")
    t_case: float = Field(..., description="t_case input")
    f_carnot_shield: float = Field(..., description="f_carnot_shield input")
    joint_drive_fraction: float = Field(..., description="joint_drive_fraction input")
    p_joint: float = Field(..., description="p_joint input")
    sigma_SB: float = Field(..., description="sigma_SB input")


class Coil_Thermal_InventoryModule(ModuleBase[Coil_Thermal_InventoryInput, Coil_Thermal_InventoryOutput]):
    """TEAx module for Coil_Thermal_Inventory calculation.

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

Inputs:
    - T_amb: T_amb parameter
    - shield_area_ratio: shield_area_ratio parameter
    - f_carnot_cold: f_carnot_cold parameter
    - eps_eff: eps_eff parameter
    - g_per_coil: g_per_coil parameter
    - n_coils: n_coils parameter
    - L0: L0 parameter
    - k_s: k_s parameter
    - T_cold: T_cold parameter
    - c_coil: c_coil parameter
    - T_shield: T_shield parameter
    - I_turn: I_turn parameter
    - wp_side: wp_side parameter
    - q_MLI: q_MLI parameter
    - f_lead: f_lead parameter
    - k_c: k_c parameter
    - inventory_enabled: inventory_enabled parameter
    - n_leads: n_leads parameter
    - t_case: t_case parameter
    - f_carnot_shield: f_carnot_shield parameter
    - joint_drive_fraction: joint_drive_fraction parameter
    - p_joint: p_joint parameter
    - sigma_SB: sigma_SB parameter

Outputs:
    - q_rad_cold: q_rad_cold result
    - q_rad_shield: q_rad_shield result
    - q_lead_shield: q_lead_shield result
    - q_support_cold: q_support_cold result
    - q_inventory_shield: q_inventory_shield result
    - q_lead_cold: q_lead_cold result
    - area_shield: area_shield result
    - q_support_shield: q_support_shield result
    - q_inventory_cold: q_inventory_cold result
    - area_cold: area_cold result
    - p_drive: p_drive result

SysML Source: root-0/analyses/mfe_cryo_inventory.sysml:3

    SysML Source: root-0/analyses/mfe_cryo_inventory.sysml:3

    Calculation Specification:
        inventory_enabled = false
        n_coils = 0.0
        c_coil = 0.0
        wp_side = 0.0
        I_turn = 0.0
        n_leads = 0.0
        L0 = 0.0
        f_lead = 1.0
        T_cold = 20.0
        T_shield = 77.0
        T_amb = 300.0
        f_carnot_cold = 1.0
        f_carnot_shield = 1.0
        t_case = 0.0
        shield_area_ratio = 1.0
        eps_eff = 0.0
        sigma_SB = 0.0
        q_MLI = 0.0
        g_per_coil = 0.0
        k_c = 0.0
        k_s = 0.0
        p_joint = 0.0
        joint_drive_fraction = 0.0
        
Documentation:
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

    IMPLEMENTATION: See stellarator_materials_rebco_tea.handwritten.mfe_cryo_inventory.coil_thermal_inventory_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts q_rad_cold, q_rad_shield, q_lead_shield, q_support_cold, q_inventory_shield, q_lead_cold, area_shield, q_support_shield, q_inventory_cold, area_cold, p_drive fields to separate channels.
    """

    name: str = "Coil_Thermal_InventoryModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, T_amb: float, shield_area_ratio: float, f_carnot_cold: float, eps_eff: float, g_per_coil: float, n_coils: float, L0: float, k_s: float, T_cold: float, c_coil: float, T_shield: float, I_turn: float, wp_side: float, q_MLI: float, f_lead: float, k_c: float, inventory_enabled: bool, n_leads: float, t_case: float, f_carnot_shield: float, joint_drive_fraction: float, p_joint: float, sigma_SB: float    ) -> Coil_Thermal_InventoryInput:
        """Validate inputs and fill defaults.

        Args:
            T_amb: T_amb input
            shield_area_ratio: shield_area_ratio input
            f_carnot_cold: f_carnot_cold input
            eps_eff: eps_eff input
            g_per_coil: g_per_coil input
            n_coils: n_coils input
            L0: L0 input
            k_s: k_s input
            T_cold: T_cold input
            c_coil: c_coil input
            T_shield: T_shield input
            I_turn: I_turn input
            wp_side: wp_side input
            q_MLI: q_MLI input
            f_lead: f_lead input
            k_c: k_c input
            inventory_enabled: inventory_enabled input
            n_leads: n_leads input
            t_case: t_case input
            f_carnot_shield: f_carnot_shield input
            joint_drive_fraction: joint_drive_fraction input
            p_joint: p_joint input
            sigma_SB: sigma_SB input

        Returns:
            Validated input model
        """
        return Coil_Thermal_InventoryInput(T_amb=T_amb, shield_area_ratio=shield_area_ratio, f_carnot_cold=f_carnot_cold, eps_eff=eps_eff, g_per_coil=g_per_coil, n_coils=n_coils, L0=L0, k_s=k_s, T_cold=T_cold, c_coil=c_coil, T_shield=T_shield, I_turn=I_turn, wp_side=wp_side, q_MLI=q_MLI, f_lead=f_lead, k_c=k_c, inventory_enabled=inventory_enabled, n_leads=n_leads, t_case=t_case, f_carnot_shield=f_carnot_shield, joint_drive_fraction=joint_drive_fraction, p_joint=p_joint, sigma_SB=sigma_SB)

    def run(
        self, T_amb: float, shield_area_ratio: float, f_carnot_cold: float, eps_eff: float, g_per_coil: float, n_coils: float, L0: float, k_s: float, T_cold: float, c_coil: float, T_shield: float, I_turn: float, wp_side: float, q_MLI: float, f_lead: float, k_c: float, inventory_enabled: bool, n_leads: float, t_case: float, f_carnot_shield: float, joint_drive_fraction: float, p_joint: float, sigma_SB: float    ) -> ModuleResult[Coil_Thermal_InventoryOutput]:
        """Execute calculation.

        Args:
            T_amb: T_amb input
            shield_area_ratio: shield_area_ratio input
            f_carnot_cold: f_carnot_cold input
            eps_eff: eps_eff input
            g_per_coil: g_per_coil input
            n_coils: n_coils input
            L0: L0 input
            k_s: k_s input
            T_cold: T_cold input
            c_coil: c_coil input
            T_shield: T_shield input
            I_turn: I_turn input
            wp_side: wp_side input
            q_MLI: q_MLI input
            f_lead: f_lead input
            k_c: k_c input
            inventory_enabled: inventory_enabled input
            n_leads: n_leads input
            t_case: t_case input
            f_carnot_shield: f_carnot_shield input
            joint_drive_fraction: joint_drive_fraction input
            p_joint: p_joint input
            sigma_SB: sigma_SB input

        Returns:
            Module result with Coil_Thermal_InventoryOutput (q_rad_cold, q_rad_shield, q_lead_shield, q_support_cold, q_inventory_shield, q_lead_cold, area_shield, q_support_shield, q_inventory_cold, area_cold, p_drive)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(T_amb, shield_area_ratio, f_carnot_cold, eps_eff, g_per_coil, n_coils, L0, k_s, T_cold, c_coil, T_shield, I_turn, wp_side, q_MLI, f_lead, k_c, inventory_enabled, n_leads, t_case, f_carnot_shield, joint_drive_fraction, p_joint, sigma_SB)

        # Import handwritten implementation
        from stellarator_materials_rebco_tea.handwritten.mfe_cryo_inventory.coil_thermal_inventory_impl import (
            run_coil_thermal_inventory,
        )

        # Execute implementation - returns tuple of values
        q_rad_cold, q_rad_shield, q_lead_shield, q_support_cold, q_inventory_shield, q_lead_cold, area_shield, q_support_shield, q_inventory_cold, area_cold, p_drive = run_coil_thermal_inventory(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Coil_Thermal_InventoryOutput(
                q_rad_cold=q_rad_cold,
                q_rad_shield=q_rad_shield,
                q_lead_shield=q_lead_shield,
                q_support_cold=q_support_cold,
                q_inventory_shield=q_inventory_shield,
                q_lead_cold=q_lead_cold,
                area_shield=area_shield,
                q_support_shield=q_support_shield,
                q_inventory_cold=q_inventory_cold,
                area_cold=area_cold,
                p_drive=p_drive,
            )
        )
