package loop_return_control {
    private import ScalarValues::*;
    calc def 'Primary Bypass Control' {
        doc /*
        Primary-side bypass control that holds a heat-driven loop's return
        requirement at a counterflow exchanger (WI-095, goal design-study-parameters,
        the owner's direction of 2026-09-26). The loop delivers the duty q at the
        primary temperature T_out with heat capacity rate C_h = primary_flow * primary_cp
        / 1e6 [MW/K] and requires the helium back at required_return = T_out - q / C_h
        (the 'Primary Coolant Loop' T_comp_in). A fraction f of the primary flow
        bypasses the exchanger at T_out and mixes with the exchanger outlet; the
        exchanger sees C_h(f) = (1 - f) * C_h against the secondary rate
        C_s = secondary_flow * secondary_cp / 1e6 entering at secondary_inlet, with
        conductance UA [MW/K]:
          C_min = min(C_h(f), C_s), C_max = max(C_h(f), C_s), C_r = C_min / C_max,
          NTU = UA / C_min,
          eps = NTU / (1 + NTU)                                   if |1 - C_r| < 1e-10,
          eps = (1 - exp(-NTU (1 - C_r))) / (1 - C_r exp(-NTU (1 - C_r)))   otherwise,
          capability(f) = eps * C_min * max(T_out - secondary_inlet, 0)   [MW]
        (the closure body's form, so capability(0) equals the closure's stage capability).
        capability decreases strictly in f: with u = UA / C_h(f) - UA / C_s the
        counterflow form is capability = UA (T_out - secondary_inlet) / (u / (1 - exp(-u))
        + UA / C_s), u / (1 - exp(-u)) increases in u and u increases as C_h(f) falls;
        capability tends to 0 as f tends to 1, so the root is unique. The control solves
        capability(f) = q for f in [0, 1) by bisection (|capability - q| <= 1e-9 MW or an
        interval below 1e-15, at most 200 iterations); a bracket that is not decreasing
        and bisection exhaustion both raise (a refusal, never a returned value). Outputs:
          feasible                = 1 if capability(0) >= q else 0
          capability_open         = capability(0)
          bypass_fraction         = f (0 when infeasible)
          capability_at_solution  = capability(f)                          [MW]
          exchanger_primary_flow  = (1 - f) * primary_flow                 [kg/s]
          exchanger_return        = T_out - capability(f) / C_h(f)         [K]
            (the outlet the exchanger reaches, never computed from q; f = 0 when infeasible)
          mixed_return            = f * T_out + (1 - f) * exchanger_return
                                  = T_out - capability(f) / C_h               [K]
          return_residual         = mixed_return - required_return         [K]
          return_residual_magnitude = |return_residual|                     [K]
          effectiveness_at_solution, ntu_at_solution at f (at 0 when infeasible)
        The residual is (q - capability(f)) / C_h plus the loop-side identity
        T_out - q / C_h - required_return (zero when the exchanger cp equals the loop cp):
        about 1e-10 K at the solve tolerance when feasible, the physical deficit
        (q - capability(0)) / C_h when infeasible, so 'Return Condition Held' at 1e-6 K
        is the root-solve closure and fails every infeasible case. The bypass's own pressure loss, valve
        hardware and cost are not modeled. Domain: primary_flow, primary_cp,
        secondary_flow, secondary_cp > 0; UA >= 0; q >= 0; 0 <= max_bypass <= 1;
        tolerance > 0; a stage with T_out <= secondary_inlet has capability 0.
        **Source**: work/active/WI-095_loop-return-control/design.md section 1-3
        **Ref**: models/library/analyses/mfe_primary_loop.sysml (T_comp_in requirement);
            the 'Network Heat Driven Closure' body stage arithmetic
        **Basis**: [AGENT] explicit control model of a stated requirement; concept-agnostic (MR-3)
        */
        in attribute ua_in : Real;
        in attribute primary_flow_in : Real;
        in attribute primary_cp_in : Real;
        in attribute secondary_flow_in : Real;
        in attribute secondary_cp_in : Real;
        in attribute primary_limit_in : Real;
        in attribute secondary_inlet_in : Real;
        in attribute duty_in : Real;
        in attribute required_return_in : Real;
        in attribute max_bypass_in : Real;
        in attribute tolerance_in : Real;
        out attribute bypass_fraction : Real;
        out attribute feasible : Real;
        out attribute capability_open : Real;
        out attribute capability_at_solution : Real;
        out attribute exchanger_primary_flow : Real;
        out attribute exchanger_return : Real;
        out attribute mixed_return : Real;
        out attribute return_residual : Real;
        out attribute return_residual_magnitude : Real;
        out attribute effectiveness_at_solution : Real;
        out attribute ntu_at_solution : Real;
    }
    constraint def 'Return Condition Held' {
        doc /* The mixed return equals the loop's required return within the root-solve closure tolerance (1e-6 K in the assembly); an infeasible bypass carries the physical deficit and fails. **Source**: work/active/WI-095_loop-return-control/design.md section 3. **Last Updated**: 2026-09-26. */
        in return_residual_magnitude_in : Real;
        in tolerance_in : Real;
        return_residual_magnitude_in <= tolerance_in
    }
    constraint def 'Bypass Within Limit' {
        doc /* The bypass fraction does not exceed the chosen maximum (1.0 = no design limit declared). **Source**: work/active/WI-095_loop-return-control/design.md section 3. **Last Updated**: 2026-09-26. */
        in bypass_fraction_in : Real;
        in max_bypass_in : Real;
        bypass_fraction_in <= max_bypass_in
    }
}
