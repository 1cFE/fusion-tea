package mfe_steam_cycle_components {
    private import ScalarValues::*;
    private import mfe_interfaces::*;
    part def 'Steam State Component' {
        doc /* **Source**: work/orchestration/goals/current-model-comparison-readiness/evidence/round2/cycle-proposal-v2.md **Reference**: WI-073 design.md and interface-inventory.md; original NIST tables and independent physical review. **Basis**: [AGENT] reviewed reduced extraction/reheat cycle and conditional cooling-water scenario; equipment and installed cost unqualified. **Last Updated**: 2026-09-19 No individual installed price is implied by this physical occurrence. */
        port inlet : ~'Water State Port';
        port outlet : 'Water State Port';
        attribute p_in_MPa : Real;
        attribute h_in_kJ_kg : Real;
        attribute flow_in_kg_s : Real;
        attribute p_out_MPa : Real;
        attribute h_out_kJ_kg : Real;
        attribute flow_out_kg_s : Real;
    }
    part def 'Steam Heat Exchanger' :> 'Steam State Component' {
        doc /* **Source**: work/orchestration/goals/current-model-comparison-readiness/evidence/round2/cycle-proposal-v2.md **Reference**: WI-073 design.md and interface-inventory.md; original NIST tables and independent physical review. **Basis**: [AGENT] reviewed reduced extraction/reheat cycle and conditional cooling-water scenario; equipment and installed cost unqualified. **Last Updated**: 2026-09-19 No individual installed price is implied by this physical occurrence. */
        port salt : ~'Thermal Port';
        attribute pressure_MPa : Real;
        attribute outlet_temperature_C : Real;
        attribute heat_MW : Real;
        attribute minimum_gap_K : Real;
        attribute required_UA_MW_K : Real;
        attribute salt_flow_kg_s : Real;
    }
    part def 'Steam Expansion' :> 'Steam State Component' {
        doc /* **Source**: work/orchestration/goals/current-model-comparison-readiness/evidence/round2/cycle-proposal-v2.md **Reference**: WI-073 design.md and interface-inventory.md; original NIST tables and independent physical review. **Basis**: [AGENT] reviewed reduced extraction/reheat cycle and conditional cooling-water scenario; equipment and installed cost unqualified. **Last Updated**: 2026-09-19 No individual installed price is implied by this physical occurrence. */
        port shaft_out : 'Shaft Power Port';
        attribute efficiency : Real;
        attribute shaft_MW : Real;
    }
    part def 'Steam Feed Heater' :> 'Steam State Component' {
        doc /* **Source**: work/orchestration/goals/current-model-comparison-readiness/evidence/round2/cycle-proposal-v2.md **Reference**: WI-073 design.md and interface-inventory.md; original NIST tables and independent physical review. **Basis**: [AGENT] reviewed reduced extraction/reheat cycle and conditional cooling-water scenario; equipment and installed cost unqualified. **Last Updated**: 2026-09-19 No individual installed price is implied by this physical occurrence. */
        port bleed_in : ~'Water State Port';
        attribute pressure_MPa : Real;
        attribute bleed_flow_kg_s : Real;
        attribute bleed_h_kJ_kg : Real;
        attribute mass_residual_kg_s : Real;
        attribute energy_residual_MW : Real;
    }
    part def 'Steam Condenser' :> 'Steam State Component' {
        doc /* **Source**: work/orchestration/goals/current-model-comparison-readiness/evidence/round2/cycle-proposal-v2.md **Reference**: WI-073 design.md and interface-inventory.md; original NIST tables and independent physical review. **Basis**: [AGENT] reviewed reduced extraction/reheat cycle and conditional cooling-water scenario; equipment and installed cost unqualified. **Last Updated**: 2026-09-19 No individual installed price is implied by this physical occurrence. */
        port rejection : 'Heat Duty Port';
        attribute temperature_C : Real;
        attribute rejected_MW : Real;
    }
    part def 'Steam Liquid Pump' :> 'Steam State Component' {
        doc /* **Source**: work/orchestration/goals/current-model-comparison-readiness/evidence/round2/cycle-proposal-v2.md **Reference**: WI-073 design.md and interface-inventory.md; original NIST tables and independent physical review. **Basis**: [AGENT] reviewed reduced extraction/reheat cycle and conditional cooling-water scenario; equipment and installed cost unqualified. **Last Updated**: 2026-09-19 No individual installed price is implied by this physical occurrence. */
        port electric_in : ~'Electric Port';
        attribute efficiency : Real;
        attribute shaft_MW : Real;
        attribute electric_MW : Real;
    }
    part def 'Steam Generator Machine' {
        doc /* **Source**: work/orchestration/goals/current-model-comparison-readiness/evidence/round2/cycle-proposal-v2.md **Reference**: WI-073 design.md and interface-inventory.md; original NIST tables and independent physical review. **Basis**: [AGENT] reviewed reduced extraction/reheat cycle and conditional cooling-water scenario; equipment and installed cost unqualified. **Last Updated**: 2026-09-19 No individual installed price is implied by this physical occurrence. */
        port hp_shaft : ~'Shaft Power Port';
        port lp_shaft : ~'Shaft Power Port';
        port electric_out : 'Electric Port';
        attribute mechanical_efficiency : Real;
        attribute generator_efficiency : Real;
        attribute hp_shaft_MW : Real;
        attribute lp_shaft_MW : Real;
        attribute gross_MW : Real;
        attribute mechanical_loss_MW : Real;
        attribute generator_loss_MW : Real;
    }
    part def 'Circulating Water Pump' {
        doc /* **Source**: work/orchestration/goals/current-model-comparison-readiness/evidence/round2/cycle-proposal-v2.md **Reference**: WI-073 design.md and interface-inventory.md; original NIST tables and independent physical review. **Basis**: [AGENT] reviewed reduced extraction/reheat cycle and conditional cooling-water scenario; equipment and installed cost unqualified. **Last Updated**: 2026-09-19 No individual installed price is implied by this physical occurrence. */
        port electric_in : ~'Electric Port';
        attribute head_m : Real;
        attribute efficiency : Real;
        attribute motor_efficiency : Real;
        attribute flow_kg_s : Real;
        attribute shaft_MW : Real;
        attribute electric_MW : Real;
    }
    part def 'Steam Extraction Splitter' {
        doc /* WI-073 ideal extraction junction. Both branches retain HP outlet pressure and enthalpy; mass flow divides explicitly. */
        port inlet : ~'Water State Port';
        port reheat_out : 'Water State Port';
        port bleed_out : 'Water State Port';
        attribute total_flow_kg_s : Real;
        attribute reheat_flow_kg_s : Real;
        attribute bleed_flow_kg_s : Real;
        attribute pressure_MPa : Real;
        attribute enthalpy_kJ_kg : Real;
    }
    part def 'Salt Branch Distributor' {
        doc /* WI-073 parallel salt branches. Paired Thermal Ports split the hot supply and join the equal-temperature cold returns. Temperatures below use Celsius; generic port temperature is Kelvin. Pressure loss is outside this cycle model. */
        port supply_return : ~'Thermal Port';
        port main_branch : 'Thermal Port';
        port reheat_branch : 'Thermal Port';
        attribute total_flow_kg_s : Real;
        attribute main_flow_kg_s : Real;
        attribute reheat_flow_kg_s : Real;
        attribute hot_C : Real;
        attribute return_C : Real;
    }
}
