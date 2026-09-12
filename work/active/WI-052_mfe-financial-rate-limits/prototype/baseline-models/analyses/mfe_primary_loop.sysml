package mfe_primary_loop {
    private import ScalarValues::*;

    calc def 'Primary Coolant Loop' {
        doc /*
        Representative helium primary circuit in sized-flow mode (WI-045, goal
        plant-closure; the research 20260907-163520_primary-loop-cycle-closure-prework
        section 2). One hydraulic path stands for the circuit; the loop count
        scales it. Dependency order: source heat -> flow -> per-path loss at the
        reference's nominal density -> compressor -> fluid work -> electrical
        draw -> IHX duty. There is no edge from the plant's thermal power back to
        the flow.

          mdot        = q_source * 1e6 / (cp * dT_blanket)            [kg/s]
          T_out       = T_in + dT_blanket                             [K]
          mdot_loop   = mdot / n_loops                                [kg/s]
          dp_loop     = f_loss * dp_loop_ref * (mdot_loop/mdot_loop_ref)^2  [Pa]
          r_comp      = p_loop / (p_loop - dp_loop)                   [1]
          T_comp_in   = T_in / (1 + (r_comp^((gamma-1)/gamma) - 1)/eta_is)  [K]
          w_fluid     = mdot * cp * (T_in - T_comp_in) / 1e6          [MW]
          p_elec      = w_fluid / eta_drive                           [MW]
          q_ihx       = q_source + w_fluid                            [MW]
          p_pump_total       = loop_live * p_elec + p_pump_direct     [MW]
          q_recovered_total  = loop_live * w_fluid + eta_p_direct * p_pump_direct [MW]

        THE LOSS LAW is a constant loss coefficient about the reference layout
        at its nominal density: the reference's per-path loss scaled by the
        square of the per-loop flow ratio, rho_ref/rho taken as 1 (the loop is
        held at the reference's pressure and temperature window). It computes
        loss from flow; it is NOT a fraction of thermal power (the form the
        owner rejected 2026-08-28). A broad R/a extrapolation of the law is
        unsupported: the circuit's geometry is the reference's, held.

        THE COMPRESSOR is isentropic compression from the compressor inlet at
        the isentropic efficiency eta_is, with the blanket inlet T_in held by
        the secondary-side cooling; T_comp_in is what the IHX must deliver, not
        evidence that it can (the exchanger is not sized here).

        ALL FLUID WORK IS RECOVERED into the IHX duty (the reference's own
        energy check: IHX duty 2231.1 - blanket heat 2101.7 = 129.4 MW against
        130.8 MW printed circulator power). eta_drive converts fluid work to
        electrical draw; an instance binding it to 1.0 reads the source's
        printed circulator figure as the boundary and its draw as a LOWER
        BOUND on the true electrical draw (drive losses a surfaced missing input).

        DORMANCY (packet section 3): loop_live 0 with the direct terms at the
        old held scalars gives p_pump_total = 0.0 * p_elec + p_pump_direct and
        q_recovered_total = 0.0 * w_fluid + eta_p_direct * p_pump_direct, which
        are the old scalars to the bit for finite p_elec and w_fluid; the power
        balance then reproduces the pre-WI-045 accounting exactly. The chain
        always evaluates; only what it hands to the power balance is switched.

        Constant ideal-gas helium properties (cp, gamma) over the reference
        window; the reference's own implied cp is 0.10 % under ideal helium.

        **Source**: knowledge/sources/progress_in_the_design_development_of_eu_demo_helium_cooled/output.md
            (Moscato et al., EUROfusion WPBOP-CPR(18) 20276); NASA compressor thermodynamics
            (w = cp T_in (r^((gamma-1)/gamma) - 1)/eta_is); NIST helium cp
        **Ref**: output.md:79 (8 MPa, 300-500 C), :81 (2101.7 MW, 2025.7 kg/s), :89-91 (9 loops),
            Table 1 :105-113 (two compressors per loop), Table 2 :128 (IHX duties), Table 3 :151-154
            (per-path losses, circulator power); raw.pdf p. 6 Table 3 (kPa basis)
        **Basis**: sized-flow representative circuit with a constant loss coefficient and an
            isentropic compressor; concept-agnostic (MR-3) -- every fact bound by instances
        */

        // reactor source heat, no pump credit [MW]
        in attribute q_source_in : Real;
        // blanket inlet (compressor discharge) temperature [K]
        in attribute T_in_in : Real;
        // blanket temperature rise [K], > 0
        in attribute dT_blanket_in : Real;
        // coolant specific heat [J/(kg K)], > 0
        in attribute cp_in : Real;
        // ratio of specific heats [1]
        in attribute gamma_in : Real;
        // loop nominal (compressor discharge) pressure [Pa], > dp_loop
        in attribute p_loop_in : Real;
        // number of parallel loops [1], an instance integer sized at the design point
        in attribute n_loops_in : Real;
        // reference per-loop flow [kg/s] -- the loss law's anchor and the rated capacity
        in attribute mdot_loop_ref_in : Real;
        // reference per-path pressure loss at the reference per-loop flow [Pa]
        in attribute dp_loop_ref_in : Real;
        // loss multiplier [1] (a study lever; 1.0 is the reference)
        in attribute f_loss_in : Real default 1.0;
        // compressor isentropic efficiency [1], 0 < eta_is <= 1
        in attribute eta_is_in : Real;
        // fluid-work to electrical-draw conversion [1], 0 < eta_drive <= 1
        in attribute eta_drive_in : Real default 1.0;
        // 1.0 = the loop feeds the power balance; 0.0 = dormant
        in attribute loop_live_in : Real default 0.0;
        // dormant-mode pump electrical draw [MW]
        in attribute p_pump_direct_in : Real default 0.0;
        // dormant-mode recovered fraction of that draw [1]
        in attribute eta_p_direct_in : Real default 0.0;

        out attribute mdot : Real = q_source_in * 1.0e6 / (cp_in * dT_blanket_in);
        out attribute T_out : Real = T_in_in + dT_blanket_in;
        out attribute mdot_loop : Real = mdot / n_loops_in;
        out attribute dp_loop : Real =
            f_loss_in * dp_loop_ref_in * (mdot_loop / mdot_loop_ref_in) ** 2;
        out attribute p_loop_margin : Real = p_loop_in - dp_loop;
        out attribute r_comp : Real = p_loop_in / (p_loop_in - dp_loop);
        attribute k_isen : Real = (gamma_in - 1.0) / gamma_in;
        out attribute T_comp_in : Real =
            T_in_in / (1.0 + (r_comp ** k_isen - 1.0) / eta_is_in);
        out attribute w_fluid : Real = mdot * cp_in * (T_in_in - T_comp_in) / 1.0e6;
        out attribute p_elec : Real = w_fluid / eta_drive_in;
        out attribute q_ihx : Real = q_source_in + w_fluid;
        out attribute capacity_margin : Real = mdot_loop_ref_in - mdot_loop;
        out attribute p_pump_total : Real = loop_live_in * p_elec + p_pump_direct_in;
        out attribute q_recovered_total : Real =
            loop_live_in * w_fluid + eta_p_direct_in * p_pump_direct_in;
    }
}
