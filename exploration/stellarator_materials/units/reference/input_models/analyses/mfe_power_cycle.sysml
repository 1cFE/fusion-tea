package mfe_power_cycle {
    private import ScalarValues::*;

    calc def 'Power Cycle Efficiency' {
        doc /*
        Secondary-cycle efficiency from the primary loop's outlet temperature by a
        printed fit (WI-045, goal plant-closure):

          T2_C           = T_hot - dT_approach - 273.15          [C]  (physical conversion)
          eta_fit        = a_fit * ln(T2_C + T_offset_fit) - b_fit - delta_eta   [1]
          eta_th         = cycle_live * eta_fit + eta_th_direct  [1]
          margin_low     = T2_C - T2_min                         [C]
          margin_high    = T2_max - T2_C                         [C]
          domain_product = margin_low * margin_high              [C^2]

        THE FIT'S VERSION CONTRACT: the printed Kovari et al. 2016 Table 4 form
        uses the literal 273 inside the logarithm (T_offset_fit); the physical
        273.15 converts the loop's kelvin outlet to the fit's Celsius argument.
        They are different numbers on purpose (the research section D). The
        fit is used literally; delta_eta is the printed low-temperature-divertor
        correction, bound 0 by an instance that carries no divertor loop, said so
        at the binding. The fit is a correlation on other codes' cycle modelling
        (Dostal, with the 0.0179 benchmark adjustment already inside the printed
        coefficients), not a measured plant efficiency.

        FAIL CLOSED: outside [T2_min, T2_max] the paired 'Cycle Fit Domain'
        constraint reads violated on domain_product; eta_fit is still published,
        never clamped or extrapolated silently. A non-positive logarithm argument
        raises in the executable.

        DORMANCY (packet section 3): cycle_live 0 with eta_th_direct at the old
        held efficiency gives eta_th = 0.0 * eta_fit + eta_th_direct, the old
        scalar to the bit.

        EXECUTABLE SEMANTIC (Rung B, the WI-029 CAS72 pattern): the logarithm is
        outside the codegen arithmetic envelope (+ - * / ** only), so this calc
        routes to the handwritten codegen stage (manual_required). The generated
        handwritten impl is normative and is guarded bit-exact (rel 1e-9) by the
        oracle mirror in verify_stellaris.py. The outputs are declared without
        expressions (a manual interface); the chain above is the model-resident
        statement.

        **Source**: knowledge/sources/process_a_systems_code_for_fusion_power_plants_part_2/output.md
            (Kovari et al. 2016, FED 104, 9-20, DOI 10.1016/j.fusengdes.2016.01.007)
        **Ref**: output.md:355 (Table 4: the fitting functions, T2 ranges, T1-T2 approach);
            journal p. 17 render work/orchestration/goals/plant-closure/evidence/grounding_sources/kovari2016_p9_table4.png
        **Basis**: printed secondary-cycle efficiency correlation on the turbine-inlet temperature;
            concept-agnostic (MR-3) -- coefficients, domain and approach bound by instances
        */

        // primary loop outlet temperature [K]
        in attribute T_hot_in : Real;
        // primary-to-secondary approach at the hot end [K]
        in attribute dT_approach_in : Real;
        // fit slope [1]
        in attribute a_fit_in : Real;
        // fit intercept [1]
        in attribute b_fit_in : Real;
        // the fit's literal Kelvin offset [1] (273 as printed)
        in attribute T_offset_fit_in : Real;
        // fit domain, lower turbine-inlet temperature [C]
        in attribute T2_min_in : Real;
        // fit domain, upper turbine-inlet temperature [C]
        in attribute T2_max_in : Real;
        // low-temperature divertor correction [1] (0 when no divertor loop is modelled)
        in attribute delta_eta_in : Real default 0.0;
        // 1.0 = the fit feeds the power balance; 0.0 = dormant
        in attribute cycle_live_in : Real default 0.0;
        // dormant-mode thermal efficiency [1]
        in attribute eta_th_direct_in : Real default 0.0;

        // Manual interface on the exact route (see EXECUTABLE SEMANTIC in the doc).
        out attribute T2_C : Real;
        out attribute eta_fit : Real;
        out attribute eta_th : Real;
        out attribute margin_low : Real;
        out attribute margin_high : Real;
        out attribute domain_product : Real;
    }
}
