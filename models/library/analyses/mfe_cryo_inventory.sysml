package mfe_cryo_inventory {
    private import ScalarValues::*;
    calc def 'Coil Thermal Inventory' {
        doc /* Explicit two-stage coil thermal inventory. All q outputs are W,
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
        **Source**: knowledge/sources/current_leads_and_superconducting_links_ballarino_cern/;
        knowledge/sources/nist_316_stainless_cryogenic_material_properties/;
        knowledge/sources/layered_thermal_insulation_systems_for_cryogenic/
        **Reference**: CERN slide14; NIST conductivity table; NASA slides20-21;
        work/active/WI-059_coil-thermal-and-total-support-inventory/design.md D3-D4.
        **Basis**: [AGENT] ideal-segment lead scenario with excess factor;
        316 proxy for316LN and fixed segment means, cold10-30K approximation;
        thermal bridge and surface geometry unqualified, not local stress sizing.
        **Last Updated**: 2026-09-15 */
        in attribute inventory_enabled : Boolean default false;
        in attribute n_coils : Real default 0.0;
        in attribute c_coil : Real default 0.0;
        in attribute wp_side : Real default 0.0;
        in attribute I_turn : Real default 0.0;
        in attribute n_leads : Real default 0.0;
        in attribute L0 : Real default 0.0;
        in attribute f_lead : Real default 1.0;
        in attribute T_cold : Real default 20.0;
        in attribute T_shield : Real default 77.0;
        in attribute T_amb : Real default 300.0;
        in attribute f_carnot_cold : Real default 1.0;
        in attribute f_carnot_shield : Real default 1.0;
        in attribute t_case : Real default 0.0;
        in attribute shield_area_ratio : Real default 1.0;
        in attribute eps_eff : Real default 0.0;
        in attribute sigma_SB : Real default 0.0;
        in attribute q_MLI : Real default 0.0;
        in attribute g_per_coil : Real default 0.0;
        in attribute k_c : Real default 0.0;
        in attribute k_s : Real default 0.0;
        in attribute p_joint : Real default 0.0;
        in attribute joint_drive_fraction : Real default 0.0;
        out attribute area_cold : Real;
        out attribute area_shield : Real;
        out attribute q_lead_cold : Real;
        out attribute q_lead_shield : Real;
        out attribute q_rad_cold : Real;
        out attribute q_rad_shield : Real;
        out attribute q_support_cold : Real;
        out attribute q_support_shield : Real;
        out attribute q_inventory_cold : Real;
        out attribute q_inventory_shield : Real;
        out attribute p_drive : Real;
    }
    calc def 'Cold Load Sum' {
        doc /* Assemble cold MW once; uplift only the legacy nuclear/fixed and
        explicit structure-nuclear terms, never the enumerated inventory.
        Native completion requires finite positive rho_structure and finite
        nonnegative q_nuc_structure, m_support and q_inventory_cold.
        **Source**: work/active/WI-059_coil-thermal-and-total-support-inventory/design.md
        **Reference**: D5. **Basis**: heat balance, W to MW conversion.
        **Last Updated**: 2026-09-15 */
        in attribute q_nuc : Real default 0.0;
        in attribute vol_cold : Real default 0.0;
        in attribute p_fixed : Real default 0.0;
        in attribute f_uplift : Real default 1.0;
        in attribute q_nuc_structure : Real default 0.0;
        in attribute m_support : Real default 0.0;
        in attribute rho_structure : Real default 1.0;
        in attribute q_inventory_cold : Real default 0.0;
        out attribute q_structure_nuclear : Real = q_nuc_structure*m_support/rho_structure;
        out attribute p_cold : Real = f_uplift*(q_nuc*vol_cold*1e-6+p_fixed+q_structure_nuclear*1e-6)+q_inventory_cold*1e-6;
    }
    calc def 'Electrical Power Sum' {
        doc /* Sum electrical MW with no category conversion.
        **Source**: work/active/WI-059_coil-thermal-and-total-support-inventory/design.md **Reference**: D3/D5.
        **Basis**: additive electrical balance. **Last Updated**: 2026-09-15 */
        in attribute p_a : Real default 0.0;
        in attribute p_b : Real default 0.0;
        out attribute total : Real = p_a+p_b;
    }
    calc def 'Intercept Electrical Power' {
        doc /* Warm refrigerator MW=q_shield*1e-6*(T_amb-T_shield)/(f_carnot*T_shield).
        Disabled inventory returns zero before arithmetic; active temperatures
        and Carnot domain are enforced by native manual completion.
        **Source**: work/active/WI-059_coil-thermal-and-total-support-inventory/design.md **Reference**: D4-D5.
        **Basis**: fraction-of-Carnot refrigerator. **Last Updated**: 2026-09-15 */
        in attribute inventory_enabled : Boolean default false;
        in attribute q_shield : Real default 0.0;
        in attribute T_shield : Real default 77.0;
        in attribute T_amb : Real default 300.0;
        in attribute f_carnot : Real default 1.0;
        out attribute p_elec : Real;
    }
}
