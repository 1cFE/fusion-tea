package mfe_divertor_heat {
    private import ScalarValues::*;

    calc def 'Divertor Heat Ledger' {
        doc /*
        Divertor surface-heat ledger, reduced to conservation and one sourced
        fixed-geometry case (WI-047):

          p_heat_abs        = p_alpha_heat + p_coupled                       [MW]
          p_sep             = p_heat_abs - p_rad_core                         [MW]
          f_rad_edge        = (f_rad_total * p_heat_abs - p_rad_core) / p_sep  [1]
          f_rad_edge_in_range = f_rad_edge * (1 - f_rad_edge)                 [1] (>= 0 iff in [0, 1])
          p_target_nonrad   = p_heat_abs - f_rad_total * p_heat_abs           [MW]
          q_target_peak     = q_target_ref * p_target_nonrad / p_nonrad_ref   [MW/m^2]
          q_target_peak_area_scaled = q_target_peak * R_ref / R               [MW/m^2] (reported shadow)
          q_target_margin   = q_target_limit - q_target_peak                  [MW/m^2]
          p_heat_operating_minus_installed = p_aux_required - p_installed_coupled [MW]

        The absorbed heating is the alpha heating retained in the plasma plus the
        sustained operating coupled auxiliary heating, also used by the thermal sum.
        The signed required-minus-installed diagnostic uses a separate installed
        capacity operand; it does not change the operating heat ledger.
        Radiation is a DESTINATION of that heating, never added to it: the core
        radiation the sustainment chain composes leaves through the first wall; the
        source's radiated fraction f_rad_total is a TOTAL (core plus edge), so the
        edge share is derived and reported, not clamped -- a value outside [0, 1]
        means the held total and the computed core radiation are inconsistent at
        that point, and the in-range channel lets a study count such points.

        The peak target flux is the source's own case scaled linearly in the
        non-radiated load at FIXED target geometry and transport (q_target_ref at
        p_nonrad_ref): no target area, wetted fraction, emissivity, view factor,
        erosion or transient enters. A machine of another size keeps the source's
        target; the R-scaled output publishes what a target whose wetted length grows
        with the major radius would read, and nothing asserts on it. The limit a
        concept binds is an adopted steady-state threshold, not an irradiated-
        component lifetime. The source's divertor case (a total radiated fraction)
        and its first-wall cooling case (100 % radiated) are two load cases and are
        never summed. Written p_heat_abs - f * p_heat_abs so the source's own numbers
        reproduce to the double (500 - 450 = 50).

        WI-065 normative typed manual completion extends the above equations:
          p_rad_total = f_rad_total * p_heat_abs [MW]
          p_rad_edge = p_rad_total - p_rad_core [MW]
          p_target_deposited = target_capture_fraction * p_target_nonrad [MW]
          p_nonrad_uncaptured = p_target_nonrad - p_target_deposited [MW]
          peak_equivalent_area = target_capture_fraction * p_nonrad_ref / q_target_ref [m^2] when q_target_ref > 0, otherwise carrier 0
          peak_equivalent_area_defined = 1 iff q_target_ref > 0, otherwise 0
          f_rad_edge_defined = 1 iff p_sep > 0, otherwise 0 with f_rad_edge carrier 0
          power_account_valid = 1 iff p_rad_edge >= 0 and p_coupled >= 0, otherwise 0
        Conservation: p_heat_abs = p_rad_core + p_rad_edge + p_target_deposited + p_nonrad_uncaptured. The existing p_target_nonrad denotes incoming non-radiated transport before target capture, not target deposition.
        Every input/intermediate/output must be finite. Alpha, core and installed powers, reference peak and limit are nonnegative; p_coupled and p_aux_required are signed. Require p_heat_abs >= 0. Negative operating auxiliary demand is the existing burn-hold diagnostic, not physical negative heating; report it with account-valid 0. Fractions lie in [0,1]; p_nonrad_ref, R and R_ref are positive; p_rad_core <= p_heat_abs. Active q_target_ref requires positive capture and finite positive equivalent area. Refuse underflow losing expected positive power, area or peak. Negative edge radiation is reported unchanged with account-valid 0. Signed margins remain valid failure diagnostics.
        Capture is paired reference-profile metadata: 0.99 with 9.5 MW/m^2 or 0.97 with 5 MW/m^2, each at 50 MW. Changing capture alone changes deposited power and equivalent area together, never multiplies the sourced peak again. The peak-equivalent area is A_wet/k_peak, not separately measured wetted area or peaking factor. For target groups j, deposited share D_j=s_j*D, q_avg,j=D_j/A_wet,j, q_peak,j=k_j*q_avg,j, and the reported global peak is max_j(q_peak,j), with sum(s_j)=1. No independent s_j, A_wet,j or k_j is established, so these are not executable geometry levers. D/peak_equivalent_area reconstructs the peak only for an active source pair.
        The source is a resonant island divertor. The R-scaled shadow is conditional on footprint length proportional to R with held width, sharing and profile. Neither output is an average. A physical interpretation requires area-defined 1, account-valid 1 and a supported paired profile. Dormant q_target_ref=0 has no physical zero-area interpretation. The 10 MW/m^2 predicate is a necessary non-radiated transport screen; omitted radiation surface deposition prevents total target-load qualification.
        Retained alpha in this ledger differs from the plant's total alpha boundary, including the inherited alpha-fraction rounding difference. Destinations do not add plant generation. No divertor coolant loop or area-based cost is implied; the inherited power-scaled cost is unchanged.

        **Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md
        **Ref**: lines 1219-1246 (90 % of the net core heating radiated; 500 MW ->
            50 MW; the two transport cases (100 eV, 3 m^2/s) 97 % / 5 MW/m^2 and
            (200 eV, 1 m^2/s) 99 % / 9.5 MW/m^2; "remain below 10 MW/m^2"; ~200 mm
            strike width); 1135-1137 (recycling, ash removal, neutral compression and
            erosion left for later work); 1244-1250 (the values hinge on the radiated
            fraction; transients for future study); 1284 (the first-wall case at
            100 %, a different load case); page render
            work/orchestration/goals/plant-closure/evidence/grounding_sources/stellaris_p15_divertor.png
        **Basis**: Heat conservation from absorbed heating to the target on the
            source's fixed-geometry case, scaled in load only
        */

        // alpha heating retained in the plasma [MW] (the sustainment chain's)
        in attribute p_alpha_heat_in : Real;
        // signed operating plasma-coupled auxiliary demand [MW]; negative is a burn-hold diagnostic
        in attribute p_coupled_in : Real;
        // required sustained coupled heating [MW] (the sustainment chain's; reported difference only)
        in attribute p_aux_required_in : Real;
        // installed plasma-coupled heating capacity [MW], diagnostic ceiling
        in attribute p_installed_coupled_in : Real;
        // composed core radiation [MW] (bremsstrahlung + line + synchrotron)
        in attribute p_rad_core_in : Real;
        // total radiated fraction of the absorbed heating [1], 0 <= f <= 1 (a source assumption)
        in attribute f_rad_total_in : Real;
        // the source case's peak target flux [MW/m^2] at p_nonrad_ref_in
        in attribute q_target_ref_in : Real;
        // the source case's non-radiated load [MW], > 0
        in attribute p_nonrad_ref_in : Real;
        // adopted steady-state target-flux threshold [MW/m^2]
        in attribute q_target_limit_in : Real;
        // major radius [m] and the source case's major radius [m], > 0 (the shadow only)
        in attribute R_in : Real;
        in attribute R_ref_in : Real;

        // Capture attached to the reference profile, not an independent geometry gain [1].
        in attribute target_capture_fraction_in : Real;

        out attribute p_heat_abs : Real;
        out attribute p_sep : Real;
        out attribute f_rad_edge : Real;
        out attribute f_rad_edge_in_range : Real;
        out attribute p_target_nonrad : Real;
        out attribute q_target_peak : Real;
        out attribute q_target_peak_area_scaled : Real;
        out attribute q_target_margin : Real;
        out attribute p_heat_operating_minus_installed : Real;
        out attribute p_rad_total : Real;
        out attribute p_rad_edge : Real;
        out attribute p_target_deposited : Real;
        out attribute p_nonrad_uncaptured : Real;
        out attribute peak_equivalent_area : Real;
        out attribute peak_equivalent_area_defined : Real;
        out attribute f_rad_edge_defined : Real;
        out attribute power_account_valid : Real;
    }
}
