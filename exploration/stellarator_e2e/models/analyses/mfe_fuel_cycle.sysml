package mfe_fuel_cycle {
    private import ScalarValues::*;

    calc def 'Fuel Cycle Flows' {
        doc /*
        Tritium flows of a D-T plant, reduced to conservation (WI-047):

          E_fus_J         = q_eff * mev_to_joules                        [J]
          burn_rate       = p_fus * 1e6 / E_fus_J                       [atoms/s]
          inject_rate     = burn_rate / burn_fraction                    [atoms/s]
          exhaust_rate    = inject_rate - burn_rate                      [atoms/s]
          loss_rate       = (1 - t_recycle) * exhaust_rate               [atoms/s]
          tbr_required    = (burn_rate + loss_rate + lambda_T * I_total + G_stock)
                            / (eta_extract * burn_rate)                  [1]
          tbr_margin      = tbr_available - tbr_required                 [1]
          burn_kg_per_fpy = burn_rate * m_T_kg * s_per_fpy               [kg per full-power year]

        One D-T reaction burns one tritium atom; the fusion power fixes the burn,
        the single-pass burn fraction fixes the circulating stream, and the recovery
        of the unburned stream fixes the permanent loss. The required breeding ratio
        is the tritium that must be bred per atom burned to replace burn, permanent
        loss, decay of the held inventory and any stock growth, divided by the
        extraction efficiency from breeder to usable supply. The margin against the
        ACHIEVED ratio a concept binds is a reported margin. In the WI-066
        stellarator, a separate adequacy calculation compares computed breeding
        with this requirement and the retained design floor. Its validity flag
        also governs interpretation of this raw margin when transport is undefined.
        Recovery remains an explicit conditional scenario, not a measured efficiency.

        Inventory is supplied through I_total. WI-069 computes the stellarator stock
        through the separate Fuel Inventory calculation; other instances may retain
        dormant held inventory. G_stock remains an explicit stock-growth input. A duty factor multiplies operating burns
        and flows in the plant (the calendar's productive time); stock decays through
        calendar time too -- the two clocks are the lifecycle calc's, not this one's.

        This calc computes REQUIRED breeding; achieved neutronics comes through
        the blanket-owned tbr interface. 'DT Fuel Cost' (mfe_account_costs)
        keeps its own burn correction on the same burn_fraction and the same
        recovery number read as a feedstock cost factor; the two calcs read the
        same inputs and mean different things, and say so.

        Flat-Real (+ - * /) -- lowers to generated arithmetic; no manual stage.

        **Source**: knowledge/research/pending/20260907-163520_demo-breadth-disposition-prework.md
        **Ref**: lines 43-54 (the conservation equations in T atoms/s), 56 (the NIST
            half-life 4500 +/- 8 d, Lucas and Unterweger, J. Res. NIST 105 (2000) 541),
            58 (startup as a residence-time balance, not computed here), 60 (the
            conditional 1.19 finding)
        **Basis**: Tritium conservation on the burned, circulating and bred streams
        */

        // fusion power [MW]
        in attribute p_fus_in : Real;
        // per-reaction energy [MeV] and the MeV -> J conversion -- the same two
        // formals 'DT Fuel Cost' takes, so the burn and the fuel cost count the same
        // reactions (the product is formed here; a product on a calc-input binding
        // is not a resolvable reference on the exact route -- WI-047 phase 1)
        in attribute q_eff_in : Real;
        in attribute mev_to_joules_in : Real;
        // single-pass burn fraction [1], 0 < burn_fraction_in <= 1
        in attribute burn_fraction_in : Real;
        // recovery fraction of the unburned tritium stream [1], 0 <= t_recycle_in <= 1
        in attribute t_recycle_in : Real;
        // achieved tritium breeding ratio [1]; source/transport applicability belongs to the producer
        in attribute tbr_available_in : Real;
        // breeder-to-supply extraction efficiency [1], 0 < eta_extract_in <= 1 (dormant 1.0)
        in attribute eta_extract_in : Real;
        // tritium decay constant [1/s] (an instance input derived from the half-life)
        in attribute lambda_T_in : Real;
        // total held tritium inventory [atoms] (held or computed by the owning fuel system)
        in attribute I_total_in : Real;
        // required stock growth [atoms/s] (dormant 0.0: a single mature plant)
        in attribute G_stock_in : Real;
        // tritium atomic mass [kg] (an instance input with its derivation)
        in attribute m_T_kg_in : Real;
        // seconds per full-power year [s]: 8760 h x 3600 s, the model's own year
        // ('LCOE DCF' 8760.0; 'DT Fuel Cost' 3600.0 * 8760.0)
        in attribute s_per_fpy_in : Real default 31536000.0;

        // energy per D-T reaction [J]
        attribute E_fus_J : Real = q_eff_in * mev_to_joules_in;

        out attribute burn_rate : Real = p_fus_in * 1.0e6 / E_fus_J;
        out attribute inject_rate : Real = burn_rate / burn_fraction_in;
        out attribute exhaust_rate : Real = inject_rate - burn_rate;
        out attribute loss_rate : Real = (1.0 - t_recycle_in) * exhaust_rate;
        out attribute tbr_required : Real =
            (burn_rate + loss_rate + lambda_T_in * I_total_in + G_stock_in) / (eta_extract_in * burn_rate);
        out attribute tbr_margin : Real = tbr_available_in - tbr_required;
        out attribute burn_kg_per_fpy : Real = burn_rate * m_T_kg_in * s_per_fpy_in;
    }

    calc def 'Fuel Inventory' {
        doc /* Nominal stage inventory and deterministic-delay commissioning supply; typed manual completion.
        B=P*1e6/(Q*c), F=B/f, U=F-B, R=rU, L=(1-r)U, J=TBR*B, S=eta*J [T atoms/s].
        Feed=F*tau_feed; plasma=n_T0*V/(1+alpha_n); processor=U*tau_process;
        blanket=J*tau_blanket; extraction=J*tau_extract; buffer=F*tau_buffer;
        reserve=F*q*tau_reserve [T atoms]. I_work=sum(first six); I_total=I_work+reserve.
        Processor loss occurs once at its outlet; extraction efficiency acts once at final breeder outlet.
        Feed, plasma, buffer and reserve start prefilled; processor, breeder zone and extraction start empty.
        Recycle delay=tau_process; breeder delay=tau_blanket+tau_extract; H=max(delays)+extension.
        D(t)=F*t-R*max(t-tau_process,0)-S*max(t-tau_blanket-tau_extract,0).
        d=max(D at 0, each return delay and H); prefill=feed+plasma+buffer;
        M0=prefill+reserve+d. The other stage fills are inside d, not purchased again.
        k=lambda*H must be <1. A=k*(M0+J*H)/(1-k); conservative startup=M0+A.
        This protects decay including extra startup stock itself, under an abstract usable supply boundary.
        It is not an exact transient minimum or qualified ignition/ramp design; source compartment residence
        estimates are transferred to deterministic delays. Decay-free nominal stage stocks use separate
        replacement demand lambda*I_total. max_decay_residence=max(lambda*each of the five residence inputs),
        excluding the reserve interruption duration, reports approximation scale without imposing a qualification threshold.
        All atom stocks multiply m_T for kg. T rates export kg/s and 86400 times that for kg/day.
        D+T injection/exhaust use equal isotope atom rates times (m_D+m_T), excluding ash and carrier mass.
        Annual running amounts multiply availability*s_per_year. Annual decay uses all s_per_year.
        Signed operating makeup=(B+L-S+lambda*I_total)*m_T; external shortfall=max(signed,0).
        Annual signed makeup=((B+L-S)*availability+lambda*I_total)*m_T*s_per_year.
        Passive shutdown loss=-expm1(-lambda*t_shutdown)*I_total*m_T; remaining=exp(-lambda*t_shutdown)*I_total*m_T to retain small positive late stock.
        Maintained nominal inventory persists through shutdown; passive remaining is a separate policy.
        Active: finite inputs/intermediates; positive power, energy, masses, year; f,eta in (0,1]; r,q,
        availability in [0,1]; alpha_n>-1; nonnegative TBR, density, volume, times and decay; G_stock=0.
        Invalid arithmetic/fractions raise ValueError. Undefined breeding flag 0 preserves finite diagnostic
        carriers (J=0 when breeding_defined=0) and non-breeding stocks/flows, but production-dependent stocks, total/startup and supply
        are physically undefined, never a zero-production prediction. defined_flag propagates that status.
        Dormant enabled=false forwards held_inventory into total_atoms and returns other zero carriers
        with defined_flag=0; no active stock claim. Generic legacy flow arithmetic remains unchanged.
        Unsupported wall retention, permeation, detritiation, impurities and bypass remain omitted limitations.
        **Source**: work/active/WI-069_fuel-inventory-and-startup/design.md
        **Reference**: knowledge/research/pending/20260919-074901_fuel-inventory-residence-startup.md; evidence/proposed-abi.md
        **Basis**: independently reviewed conditional scenario; source-derived residence cases, explicit storage policy.
        Input units (flat Real ABI; explicit physical meaning):
        in attribute enabled_in : Boolean default := false; 1; activation
        in attribute held_inventory_in : Real default := 0.0; T atoms; dormant legacy amount
        in attribute p_fus_in : Real; MW
        in attribute q_eff_in : Real; MeV/reaction
        in attribute mev_to_joules_in : Real; J/MeV
        in attribute burn_fraction_in : Real; 1; (0,1]
        in attribute t_recycle_in : Real; 1; [0,1]
        in attribute tbr_available_in : Real; T atoms/reaction
        in attribute breeding_defined_in : Real default := 1.0; 1; exact 0/1
        in attribute eta_extract_in : Real; 1; (0,1]
        in attribute lambda_T_in : Real; 1/s
        in attribute G_stock_in : Real; T atoms/s; active zero
        in attribute m_T_kg_in : Real; kg/T atom
        in attribute m_D_kg_in : Real default := 0.0; kg/D atom
        in attribute plasma_volume_in : Real default := 0.0; m^3
        in attribute n_T0_in : Real default := 0.0; T atoms/m^3
        in attribute alpha_n_in : Real default := 0.0; 1; > -1
        in attribute tau_feed_in : Real default := 0.0; s
        in attribute tau_process_in : Real default := 0.0; s
        in attribute tau_blanket_in : Real default := 0.0; s
        in attribute tau_extract_in : Real default := 0.0; s
        in attribute tau_buffer_in : Real default := 0.0; s
        in attribute tau_reserve_in : Real default := 0.0; s
        in attribute startup_extension_in : Real default := 0.0; s
        in attribute shutdown_duration_in : Real default := 0.0; s
        in attribute reserve_fraction_in : Real default := 0.0; 1; [0,1]
        in attribute availability_in : Real; 1; calendar productive fraction
        in attribute s_per_year_in : Real default := 31536000.0; s/year; existing model 8760-hour year
        **Last Updated**: 2026-09-19 */
        in attribute enabled_in : Boolean default := false;
        in attribute held_inventory_in : Real default := 0.0;
        in attribute p_fus_in : Real;
        in attribute q_eff_in : Real;
        in attribute mev_to_joules_in : Real;
        in attribute burn_fraction_in : Real;
        in attribute t_recycle_in : Real;
        in attribute tbr_available_in : Real;
        in attribute breeding_defined_in : Real default := 1.0;
        in attribute eta_extract_in : Real;
        in attribute lambda_T_in : Real;
        in attribute G_stock_in : Real;
        in attribute m_T_kg_in : Real;
        in attribute m_D_kg_in : Real default := 0.0;
        in attribute plasma_volume_in : Real default := 0.0;
        in attribute n_T0_in : Real default := 0.0;
        in attribute alpha_n_in : Real default := 0.0;
        in attribute tau_feed_in : Real default := 0.0;
        in attribute tau_process_in : Real default := 0.0;
        in attribute tau_blanket_in : Real default := 0.0;
        in attribute tau_extract_in : Real default := 0.0;
        in attribute tau_buffer_in : Real default := 0.0;
        in attribute tau_reserve_in : Real default := 0.0;
        in attribute startup_extension_in : Real default := 0.0;
        in attribute shutdown_duration_in : Real default := 0.0;
        in attribute reserve_fraction_in : Real default := 0.0;
        in attribute availability_in : Real;
        in attribute s_per_year_in : Real default := 31536000.0;
        out attribute feed_atoms : Real; // T atoms
        out attribute feed_kg : Real; // kg T
        out attribute plasma_atoms : Real; // T atoms
        out attribute plasma_kg : Real; // kg T
        out attribute processor_atoms : Real; // T atoms
        out attribute processor_kg : Real; // kg T
        out attribute blanket_atoms : Real; // T atoms
        out attribute blanket_kg : Real; // kg T
        out attribute extraction_atoms : Real; // T atoms
        out attribute extraction_kg : Real; // kg T
        out attribute buffer_atoms : Real; // T atoms
        out attribute buffer_kg : Real; // kg T
        out attribute reserve_atoms : Real; // T atoms
        out attribute reserve_kg : Real; // kg T
        out attribute working_atoms : Real; // T atoms
        out attribute working_kg : Real; // kg T
        out attribute total_atoms : Real; // T atoms
        out attribute total_kg : Real; // kg T
        out attribute prefill_atoms : Real; // T atoms
        out attribute prefill_kg : Real; // kg T
        out attribute startup_deficit_atoms : Real; // T atoms
        out attribute startup_deficit_kg : Real; // kg T
        out attribute startup_minimum_atoms : Real; // T atoms
        out attribute startup_minimum_kg : Real; // kg T
        out attribute startup_decay_allowance_atoms : Real; // T atoms
        out attribute startup_decay_allowance_kg : Real; // kg T
        out attribute startup_conservative_atoms : Real; // T atoms
        out attribute startup_conservative_kg : Real; // kg T
        out attribute recycle_delay_s : Real; // s
        out attribute breeding_delay_s : Real; // s
        out attribute startup_horizon_s : Real; // s
        out attribute max_decay_residence : Real; // 1; max(lambda_T * individual process/buffer residence time)
        out attribute burn_kg_s : Real; // kg T/s; full power
        out attribute burn_kg_day : Real; // kg T/day; full power
        out attribute annual_burn_kg : Real; // kg T/calendar year; productive time
        out attribute injection_kg_s : Real; // kg T/s; full power
        out attribute injection_kg_day : Real; // kg T/day; full power
        out attribute annual_injection_kg : Real; // kg T/calendar year; productive time
        out attribute exhaust_kg_s : Real; // kg T/s; full power
        out attribute exhaust_kg_day : Real; // kg T/day; full power
        out attribute annual_exhaust_kg : Real; // kg T/calendar year; productive time
        out attribute recycle_kg_s : Real; // kg T/s; full power
        out attribute recycle_kg_day : Real; // kg T/day; full power
        out attribute annual_recycle_kg : Real; // kg T/calendar year; productive time
        out attribute production_kg_s : Real; // kg T/s; full power
        out attribute production_kg_day : Real; // kg T/day; full power
        out attribute annual_production_kg : Real; // kg T/calendar year; productive time
        out attribute extracted_kg_s : Real; // kg T/s; full power
        out attribute extracted_kg_day : Real; // kg T/day; full power
        out attribute annual_extracted_kg : Real; // kg T/calendar year; productive time
        out attribute recycle_loss_kg_s : Real; // kg T/s; full power
        out attribute recycle_loss_kg_day : Real; // kg T/day; full power
        out attribute annual_recycle_loss_kg : Real; // kg T/calendar year; productive time
        out attribute extraction_loss_kg_s : Real; // kg T/s; full power
        out attribute extraction_loss_kg_day : Real; // kg T/day; full power
        out attribute annual_extraction_loss_kg : Real; // kg T/calendar year; productive time
        out attribute dt_injection_kg_s : Real; // kg (D+T)/s; full power
        out attribute dt_injection_kg_day : Real; // kg (D+T)/day; full power
        out attribute dt_processor_kg_s : Real; // kg (D+T)/s; full power
        out attribute dt_processor_kg_day : Real; // kg (D+T)/day; full power
        out attribute decay_kg_s : Real; // kg T/s; calendar_processor is calendar average, others operating
        out attribute makeup_signed_kg_s : Real; // kg T/s; calendar_processor is calendar average, others operating
        out attribute external_shortfall_kg_s : Real; // kg T/s; calendar_processor is calendar average, others operating
        out attribute calendar_processor_kg_s : Real; // kg T/s; calendar_processor is calendar average, others operating
        out attribute annual_decay_kg : Real; // kg T/calendar year; decay uses all calendar seconds
        out attribute annual_makeup_signed_kg : Real; // kg T/calendar year; decay uses all calendar seconds
        out attribute annual_external_shortfall_kg : Real; // kg T/calendar year; decay uses all calendar seconds
        out attribute shutdown_remaining_kg : Real; // kg T; passive shutdown, distinct from maintained design inventory
        out attribute shutdown_decay_loss_kg : Real; // kg T; passive shutdown, distinct from maintained design inventory
        out attribute defined_flag : Real; // 1; exact 0/1, conditional inventory interpretation
    }
    calc def 'Fuel Processing Cost' {
        doc /* Conditional conventional D+T exhaust processing, four subsystem rows and direct installation.
        Source: knowledge/sources/bartlit_1983_tsta_subsystem_costs_original_osti_paper/output.md, Table II and Section III; knowledge/sources/etr_iter_systems_code_ornl_fedc_87_7_1988/output.md, fuel-processing relation.
        Reference: work/active/WI-070_throughput-based-fuel-processing-costs/design.md and evidence/account-reconciliation.md; reviewed price and transfer records in goal evidence.
        Basis: near-equimolar D/T, source-like impurities, cleaned feed below 1 ppm noncondensibles, atmospheric cryogenic separation and 20 K refrigeration. Conditional 99 percent functional recovery is inherited, not established by this price. CPI is purchasing power, not current procurement. Per-module running inlet, identical independent trains times module count; no shared discount or certified capacity. Source-like conditions are declared, not measured. Included local controls belong exclusively to C220500. Limited purchased containment; no full building, storage, blanket extraction, added specialized fuel instrumentation or source installation design/inspection claim. */
        in attribute flow_in : Real;
        in attribute inventory_enabled_in : Boolean;
        in attribute n_mod_in : Real;
        in attribute legacy_cost_in : Real;
        in attribute enabled_in : Boolean;
        in attribute source_conditions_in : Boolean;
        in attribute capacity_margin_in : Real;
        in attribute price_multiplier_in : Real;
        in attribute reference_flow_in : Real;
        in attribute exponent_in : Real;
        in attribute target_cpi_in : Real;
        in attribute transfer_cpi_in : Real;
        in attribute transfer_capital_in : Real;
        in attribute transfer_installation_in : Real;
        in attribute cleanup_cpi_in : Real;
        in attribute cleanup_capital_in : Real;
        in attribute cleanup_installation_in : Real;
        in attribute distiller_cpi_in : Real;
        in attribute distiller_capital_in : Real;
        in attribute distiller_installation_in : Real;
        in attribute containment_cpi_in : Real;
        in attribute containment_capital_in : Real;
        in attribute containment_installation_in : Real;
        out attribute flow_kg_s : Real;
        out attribute capacity_kg_s : Real;
        out attribute plant_capacity_kg_s : Real;
        out attribute flow_ratio : Real;
        out attribute scaling_factor : Real;
        out attribute transfer_reference_capital : Real;
        out attribute transfer_reference_installation : Real;
        out attribute transfer_capital : Real;
        out attribute transfer_installation : Real;
        out attribute cleanup_reference_capital : Real;
        out attribute cleanup_reference_installation : Real;
        out attribute cleanup_capital : Real;
        out attribute cleanup_installation : Real;
        out attribute distiller_reference_capital : Real;
        out attribute distiller_reference_installation : Real;
        out attribute distiller_capital : Real;
        out attribute distiller_installation : Real;
        out attribute containment_reference_capital : Real;
        out attribute containment_reference_installation : Real;
        out attribute containment_capital : Real;
        out attribute containment_installation : Real;
        out attribute equipment_total : Real;
        out attribute installation_total : Real;
        out attribute module_total : Real;
        out attribute new_total : Real;
        out attribute cost : Real;
        out attribute defined_flag : Real;
    }
}
