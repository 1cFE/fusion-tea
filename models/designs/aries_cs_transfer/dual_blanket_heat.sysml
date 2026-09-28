package aries_dual_blanket_heat {
    private import ScalarValues::*;
    private import dual_circuit_heat_accounting::*;
    private import mfe_viability::*;

    part inter_coolant_exchange {
        doc /* One owned internal transfer, from PbLi to helium. Source: work/active/WI-086_aries-dual-blanket-heat-accounting/evidence/raffray-p734.png. Ref: Table II, approximately111MW conducted power. Basis: supplied source boundary, not predicted conductance. Last Updated: 2026-09-21. */
        attribute transferred_heat_mw : Real = 111.0;
        // Same-part identity: topology's absent directions are computed zero, not independent inputs.
        attribute absent_boundary_exchange_mw : Real = transferred_heat_mw - transferred_heat_mw;
    }
    part helium {
        doc /* Source: work/active/WI-086_aries-dual-blanket-heat-accounting/evidence/raffray-p734.png. Ref: Table II; spec.md for conditional capacity interpretation. Basis: 940 = printed1192 - printed111 - printed141; source-derived accounting boundary, not nuclear deposition prediction. Printed156MW pump electricity is separate and not fed into thermal duty. Offered rating is an independently supplied AGENT scenario, not ARIES installed hardware. Last Updated: 2026-09-21. */
        attribute deposited_heat_mw : Real = 940.0;
        attribute recovered_friction_mw : Real = 141.0;
        attribute offered_duty_mw : Real = 1250.0;
        attribute assumed_conditions_supported : Boolean = true;
        attribute scenario_applicable : Boolean = true;
        attribute duty_available : Boolean = true;
        calc heat : 'Coolant Branch Heat' {
            in deposited_heat_in = deposited_heat_mw;
            in received_exchange_in = inter_coolant_exchange.transferred_heat_mw;
            in exported_exchange_in = inter_coolant_exchange.absent_boundary_exchange_mw;
            in recovered_friction_in = recovered_friction_mw;
        }
        attribute delivered_heat_mw : Real = heat.delivered_heat;
        calc capacity : 'Offered Capacity Screen' {
            in rating_in = offered_duty_mw;
            in demand_in = delivered_heat_mw;
            in applicable_in = scenario_applicable;
            in conditions_supported_in = assumed_conditions_supported;
            in demand_available_in = duty_available;
        }
        attribute capacity_margin_mw : Real = capacity.margin;
        attribute capacity_defined : Real = capacity.evaluation_defined;
        assert constraint capacity_ok : 'Offered Equipment Capacity' {
            in defined_in = capacity_defined;
            in margin_in = capacity_margin_mw;
        }
    }
    part pbli {
        doc /* Source: work/active/WI-086_aries-dual-blanket-heat-accounting/evidence/raffray-p734.png. Ref: Table II; spec.md for conditional capacity interpretation. Basis: 1555 = printed1444 + printed111; source-derived accounting boundary. AGENT zero recovered-friction approximation neglects source1-10kW PbLi pump term; not zero physical pumping. Offered rating is an independently supplied AGENT scenario, not ARIES installed hardware. Last Updated: 2026-09-21. */
        attribute deposited_heat_mw : Real = 1555.0;
        attribute recovered_friction_mw : Real = 0.0;
        attribute offered_duty_mw : Real = 1500.0;
        attribute assumed_conditions_supported : Boolean = true;
        attribute scenario_applicable : Boolean = true;
        attribute duty_available : Boolean = true;
        calc heat : 'Coolant Branch Heat' {
            in deposited_heat_in = deposited_heat_mw;
            in received_exchange_in = inter_coolant_exchange.absent_boundary_exchange_mw;
            in exported_exchange_in = inter_coolant_exchange.transferred_heat_mw;
            in recovered_friction_in = recovered_friction_mw;
        }
        attribute delivered_heat_mw : Real = heat.delivered_heat;
        calc capacity : 'Offered Capacity Screen' {
            in rating_in = offered_duty_mw;
            in demand_in = delivered_heat_mw;
            in applicable_in = scenario_applicable;
            in conditions_supported_in = assumed_conditions_supported;
            in demand_available_in = duty_available;
        }
        attribute capacity_margin_mw : Real = capacity.margin;
        attribute capacity_defined : Real = capacity.evaluation_defined;
        assert constraint capacity_ok : 'Offered Equipment Capacity' {
            in defined_in = capacity_defined;
            in margin_in = capacity_margin_mw;
        }
    }
    part blanket_ledger {
        doc /* Source: work/active/WI-086_aries-dual-blanket-heat-accounting/spec.md. Ref: bounded two-blanket-circuit assembly, excluding divertor heat. Basis: sums actual branch outputs and checks internal accounting; no power-cycle or full-plant claim. Last Updated: 2026-09-21. */
        calc energy : 'Dual Circuit Heat Ledger' {
            in duty_1_in = helium.delivered_heat_mw;
            in duty_2_in = pbli.delivered_heat_mw;
            in deposition_1_in = helium.deposited_heat_mw;
            in deposition_2_in = pbli.deposited_heat_mw;
            in friction_1_in = helium.recovered_friction_mw;
            in friction_2_in = pbli.recovered_friction_mw;
        }
    }
}
