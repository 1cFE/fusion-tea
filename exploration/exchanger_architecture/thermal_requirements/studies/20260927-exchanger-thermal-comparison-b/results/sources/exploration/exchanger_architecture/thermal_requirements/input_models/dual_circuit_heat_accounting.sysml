package dual_circuit_heat_accounting {
    private import ScalarValues::*;

    calc def 'Coolant Branch Heat' {
        doc /* delivered_heat = deposited_heat_in + received_exchange_in - exported_exchange_in + recovered_friction_in. All quantities are MW. Source: work/active/WI-086_aries-dual-blanket-heat-accounting/spec.md. Ref: conservation on a supplied coolant-branch boundary; topology evidence Raffray Fig12 retained in that item's evidence/raffray-p736.png. Basis: generic steady energy accounting, not flow, hydraulic or exchanger performance prediction. Typed native completion rejects nonfinite/negative supplied heat, negative delivered heat and overflow; zero heat is valid. Last Updated: 2026-09-21. */
        in attribute deposited_heat_in : Real;
        in attribute received_exchange_in : Real;
        in attribute exported_exchange_in : Real;
        in attribute recovered_friction_in : Real;
        out attribute delivered_heat : Real;
    }

    calc def 'Dual Circuit Heat Ledger' {
        doc /* delivered_total = duty_1_in + duty_2_in; deposited_total = deposition_1_in + deposition_2_in; friction_total = friction_1_in + friction_2_in; energy_residual = delivered_total - deposited_total - friction_total. All quantities MW. Source: work/active/WI-086_aries-dual-blanket-heat-accounting/spec.md. Ref: two-branch control boundary with internal exchange canceling once. Basis: generic energy accounting; native completion rejects nonfinite/negative supplied heat and nonfinite outputs, but preserves signed residuals without clamping or forcing closure. A nonzero residual is a diagnostic, not an equipment adequacy claim. Independent source comparison belongs in the analysis record, not this physical producer. Last Updated: 2026-09-21. */
        in attribute duty_1_in : Real;
        in attribute duty_2_in : Real;
        in attribute deposition_1_in : Real;
        in attribute deposition_2_in : Real;
        in attribute friction_1_in : Real;
        in attribute friction_2_in : Real;
        out attribute delivered_total : Real;
        out attribute deposited_total : Real;
        out attribute friction_total : Real;
        out attribute energy_residual : Real;
    }
}
