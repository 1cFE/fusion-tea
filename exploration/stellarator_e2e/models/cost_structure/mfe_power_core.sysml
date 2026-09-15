package mfe_power_core {
    private import ScalarValues::*;
    private import mfe_interfaces::*;
    private import mfe_plasma_scaling::*;
    private import mfe_magnet_field::*;
    private import mfe_magnet_cost::*;
    private import mfe_winding_pack_cost::*;
    private import mfe_conductor_grade::*;
    private import mfe_winding_pack_fit::*;
    private import mfe_heating_chain::*;
    private import mfe_divertor_heat::*;
    private import mfe_account_costs::*;
    private import cas_hierarchy::'CAS22 Power Core';
    private import economic_parameter::'CAS Scope';
    private import mfe_magnet_parts::*;

    // =========================================================================
    // MFE-divergent CAS22 sub-account TYPES
    //
    // CAS22 (Power Core) is the IFE/MFE divergence point (DI-002). Sub-accounts
    // 22.1.3 (magnets), 22.1.4 (heating & current drive), and 22.1.8 (divertor)
    // have completely different cost structures by confinement approach; each is
    // tagged `mfe_divergent` here, mirroring the IFE side. These are concept-
    // agnostic TYPES -- no tokamak/stellarator values (MR-WI009-8); WI-011 sets
    // concept values on the costed components below.
    // =========================================================================

    part def 'CAS22.1.3 Magnet System' :> 'CAS22 Power Core' {
        doc /*
        CAS Account 22.1.3 (MFE): Magnet System. The MFE analogue of the IFE
        driver -- the dominant MFE power-core cost driver (RQ-1). Superconducting
        or resistive confinement coils (TF/CS/PF for tokamaks, modular coils for
        stellarators).

        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
        **Ref**: cas22.py:271-444 (C220103 coil costing)
        **Basis**: DI-002 -- CAS22.1.3 is MFE-divergent; coils replace the IFE driver
        */
        :>> scope = 'CAS Scope'::mfe_divergent;
    }

    part def 'CAS22.1.4 Heating and Current Drive' :> 'CAS22 Power Core' {
        doc /*
        CAS Account 22.1.4 (MFE): Supplementary Heating and Current Drive
        (NBI, ICRF, ECRH, LHCD). The MFE analogue of IFE ignition/target energy.

        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
        **Ref**: cas22.py:446-459 (C220104 supplementary heating, per-MW costs)
        **Basis**: DI-002 -- CAS22.1.4 is MFE-divergent (heating vs ignition)
        */
        :>> scope = 'CAS Scope'::mfe_divergent;
    }

    part def 'CAS22.1.8 Divertor' :> 'CAS22 Power Core' {
        doc /*
        CAS Account 22.1.8 (MFE): Divertor (W monoblock cassettes on CuCrZr heat
        sinks). The MFE analogue of the IFE target factory.

        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
        **Ref**: cas22.py:556-570 (C220108 divertor, power-scaled)
        **Basis**: DI-002 -- CAS22.1.8 is MFE-divergent (divertor vs target factory)
        */
        :>> scope = 'CAS Scope'::mfe_divergent;
    }

    // =========================================================================
    // Concept-agnostic costed components
    //
    // Specialization chain (SV-022):
    //   'Magnet System' -> 'CAS22.1.3 Magnet System' -> 'CAS22 Power Core'
    //     -> 'CAS Account' -> 'Costed Component'
    // 'Costed Component' provides capital_cost + cas_code; 'CAS Account' adds
    // account_name + scope.
    // =========================================================================

    part def 'Magnet System' :> 'CAS22.1.3 Magnet System' {
        doc /*
        Concept-agnostic magnet/coil system, decomposed since WI-057 into the physical parts
        its calcs price -- 'Modular Coil', 'Winding Pack', 'Coil Casing' (mfe_magnet_parts) -- and
        carrying the coil-cost parameters
        for the bilinear toroidal conductor model. All parameters are inputs --
        WI-011 binds tokamak/stellarator values. `capital_cost` is populated by
        the 'Magnet Coil Cost' calc (mfe_magnet_cost.sysml).

        Parameters (all concept-set, MR-WI009-8):
          B            -- field at the loop center (axis) [T]
          R0           -- major radius [m]
          r_coil       -- coil-bore radius [m]
          G            -- geometry factor (tokamak 4*pi^2, stellarator 8*pi^2)
          coil_markup  -- conductor -> installed magnet manufacturing markup
          cost_per_kAm -- conductor cost [$/kA-m], by coil material
          peak_ratio   -- peak-on-winding / axis-averaged field ratio at the
                          reference geometry (WI-030; bore-normalised since WI-044)
          B_max        -- conductor peak-field ceiling [T] (WI-030)

        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
        **Ref**: cas22.py:427 (total_kAm), cas22.py:440-444 (SC coil cost)
        **Basis**: MFE coil conductor-quantity model; parameterized for any MFE concept
        */
        // ---- ports (WI-057): the exchanges this part takes part in; declarative, see mfe_interfaces ----
        port cold_mass : 'Cryogenic Load Port';   // -> cryoplant.heat_load_in (winding_pack.q_nuc_cryo, vol_cold_total)
        // WI-035: the axis field is COMPUTED from the coil-set current
        // (reference redefinition, WI-021 pattern); B is no longer settable.
        attribute B : Real = field_calc.B_axis;
        attribute r_coil : Real;
        attribute gap2_t : Real default 0.10;
        attribute vol_cold_cryo : Real default 0.0;
        attribute c_support : Real default 0.0;
        attribute e_support : Real default 0.78;
        attribute legacy_casing_fraction : Real default 1.0;
        attribute m_support : Real = support_mass.m_support;
        calc support_mass : 'Magnet Support Mass' {
            in W_mag = stored_energy.W_mag;
            in c_support = 'Magnet System'::c_support;
            in e_support = 'Magnet System'::e_support;
        }
        // the physical parts the magnet calcs price (WI-057)
        part coil : 'Modular Coil' {
            :>> c_coil = coil_length.c_coil;
        }
        part winding_pack : 'Winding Pack' {
            :>> wp_side = wp_sizing.wp_side;
            :>> conductor_quantity_factor = conductor_grade.quantity_factor;
            :>> j_wp_effective = conductor_grade.j_wp_effective;
        }
        part casing : 'Coil Casing' {
            :>> m_casing = casing_mass.m_casing;
        }
        // ---- inputs the plant wires (WI-057): values produced elsewhere, read here by name ----
        attribute r_coil_centre : Real;   // <- rb.r_coil_centre
        // ---- EXPOSEs (WI-057): this part's calc outputs, readable outside as <part>.<name> ----
        attribute B_peak : Real = peak_field_calc.B_peak;
        attribute capital_cost_1cfe : Real = magnet_cost.capital_cost;
        attribute eps_cond : Real = cond_strain.eps_cond;
        attribute sigma_wp : Real = wp_stress.sigma_wp;
        attribute vol_cold_total : Real = wp_volume.vol_cold_total;
        // SWAP SEAM: declared `default` so a variant definition may point it at its own calc (design D5, D9)
        attribute winding_cost : Real default winding_procurement.cost;
        attribute winding_cost_legacy : Real = winding_pack_cost.cost;
        attribute winding_material_cost : Real = material_inventory.material_cost;
        attribute winding_fabrication_cost : Real = winding_procurement.winding_fabrication_cost;
        attribute tape_procurement_cost : Real = winding_procurement.tape_cost;
        attribute tape_length : Real = winding_procurement.tape_length;
        // SWAP SEAM: declared `default` so a variant definition may point it at its own calc (design D5, D9)
        attribute structure_cost : Real default magnet_structure_cost.cost;
        :>> capital_cost = magnet_capital_rollup.capital_cost;
        // ---- template calcs (WI-057): the analyses this part owns ----
        // Peak field on the winding (WI-030), compared against the conductor
        // ceiling by peak_field_ok below.
        // WI-035: axis field derived from the coil-set current (inversion
        // ruling 2026-08-30); EXPOSEd into magnet.B above, so beta_calc,
        // peak_field_calc, and magnet_cost read the computed field unchanged.
        calc field_calc : 'Coil Set Axis Field' {
            in n_coils = coil.n_coils;
            in I_coil = coil.I_coil;
            in k_link = coil.k_link;
            in R0 = coil.R0;
        }
        // WI-044: the peak field sees the coil bore -- the eq.-39 factor
        // R / (R - a_coil), normalised at the reference geometry so the
        // printed ratio is reproduced exactly there. a_coil is the radial
        // build's coil-centre radius (design D1).
        calc peak_field_calc : 'Conductor Peak Field' {
            in B_axis_in = B;
            in peak_ratio_in = coil.peak_ratio;
            in R_in = coil.R0;
            in a_coil_in = r_coil_centre;
            in R_ref_in = coil.R_ref;
            in a_coil_ref_in = coil.a_coil_ref;
        }
        // WI-044: stored magnetic energy from the coil-set inductance shape
        // (thesis eq. 2.82, W = 1/2 L I^2), anchored at the printed reference.
        calc stored_energy : 'Coil Set Stored Energy' {
            in I_coil = coil.I_coil;
            in a_coil = r_coil_centre;
            in R0 = coil.R0;
            in W_mag_ref = casing.W_mag_ref;
            in I_ref = coil.I_ref;
            in a_coil_ref = coil.a_coil_ref;
            in R_ref = coil.R_ref;
        }
        // WI-044: casing mass from stored energy (Lion 2021 eq. 56), anchored
        // at the instance's reference mass; feeds 'Magnet Structure Cost'
        // through magnet.casing.m_casing.
        calc casing_mass : 'Magnet Casing Mass' {
            in W_mag = stored_energy.W_mag;
            in W_mag_ref = casing.W_mag_ref;
            in m_casing_ref = casing.m_casing_ref;
        }
        // WI-038: installed envelope changes quantity; demand remains B_peak.
        calc conductor_grade : 'Conductor Field Capability' {
            in B_design = winding_pack.B_max;
            in B_reference = winding_pack.B_grade_ref;
            in field_exponent = winding_pack.field_exponent;
            in j_reference = winding_pack.j_wp;
        }
        // WI-036: the winding pack is sized by the current it carries, so
        // wp_side stops being an entry point and becomes a consequence of
        // coil current and the chosen winding-pack current density.
        calc wp_sizing : 'Winding Pack Sizing' {
            in I_coil = coil.I_coil;
            in j_wp = winding_pack.j_wp_effective;
        }
        calc wp_fit : 'Winding Pack Casing Fit' {
            in wp_side = winding_pack.wp_side;
            in aspect_ratio = winding_pack.fit_aspect_ratio;
            in internal_fraction_x = winding_pack.internal_build_x;
            in internal_fraction_y = winding_pack.internal_build_y;
            in ground_insulation = winding_pack.ground_insulation;
            in radial_allocation = coil.coil_t;
            in interior_y = casing.interior_y;
            in wall_thickness = casing.wall_thickness;
            in assembly_clearance = casing.assembly_clearance;
        }
        attribute fit_nominal_x : Real = wp_fit.nominal_x;
        attribute fit_nominal_y : Real = wp_fit.nominal_y;
        attribute fit_internal_x : Real = wp_fit.internal_x;
        attribute fit_internal_y : Real = wp_fit.internal_y;
        attribute fit_pack_x : Real = wp_fit.pack_x;
        attribute fit_pack_y : Real = wp_fit.pack_y;
        attribute fit_insulated_x : Real = wp_fit.insulated_x;
        attribute fit_insulated_y : Real = wp_fit.insulated_y;
        attribute fit_required_x : Real = wp_fit.required_x;
        attribute fit_required_y : Real = wp_fit.required_y;
        attribute fit_cavity_x : Real = wp_fit.cavity_x;
        attribute fit_cavity_y : Real = wp_fit.cavity_y;
        attribute fit_exterior_x : Real = wp_fit.exterior_x;
        attribute fit_exterior_y : Real = wp_fit.exterior_y;
        attribute fit_margin_x : Real = wp_fit.margin_x;
        attribute fit_margin_y : Real = wp_fit.margin_y;
        attribute fit_minimum_margin : Real = wp_fit.minimum_margin;
        // WI-058: the winding length follows the coil bore the radial build
        // sets (the coil-centre radius WI-044 introduced), anchored at the
        // printed circumference; the major radius no longer enters. WI-036's
        // k_coil*R0 agrees only when normalized bore and major-radius ratios
        // agree; fixed plasma aspect ratio alone is insufficient with the
        // held1.85m non-plasma radial stack.
        calc coil_length : 'Coil Winding Length' {
            in a_coil = r_coil_centre;
            in c_coil_ref = coil.c_coil_ref;
            in a_coil_ref = coil.a_coil_ref;
        }
        // WI-036: a wider winding pack now costs cold mass -- this feeds the
        // WI-024 cryoplant chain, which already reaches cryoplant capital.
        calc wp_volume : 'Winding Pack Cold Volume' {
            in n_coils = coil.n_coils;
            in wp_side = wp_sizing.wp_side;
            in c_coil = coil_length.c_coil;
            in f_wp_vol = winding_pack.f_wp_vol;
            // WI-036: vol_cold_cryo stays a live settable slot and enters here
            // as an ADDITIVE term, so modelling the winding-pack chain does not
            // retire it (the standing [OWNER 2026-08-27] WI-032 ruling bars
            // retiring the input, not modelling the chain behind it).
            in vol_extra = vol_cold_cryo;
        }
        // WI-035 stress operand, now consuming the WI-036 computed wp_side.
        calc wp_stress : 'Winding Pack Stress' {
            in I_coil = coil.I_coil;
            in B_peak_in = peak_field_calc.B_peak;
            in wp_side = wp_sizing.wp_side;
            in k_sigma = winding_pack.k_sigma;
        }
        // WI-036: the conductor's own operand, checked separately from the
        // structure's -- the second of the two checks every surveyed HTS
        // fusion design performs.
        calc cond_strain : 'Conductor Strain' {
            in sigma_wp = wp_stress.sigma_wp;
            in E_wp = winding_pack.E_wp;
            in f_cond = winding_pack.f_cond;
        }
        // Magnet (CAS22.1.3). WI-035: 'Magnet Coil Cost' is retained as the
        // 1cfe-form COMPARISON channel (magnet_capital_1cfe); the rollup reads
        // the decomposed sub-accounts below.
        calc magnet_cost : 'Magnet Coil Cost' {
            in G = coil.G;
            in B = 'Magnet System'::B;
            in R0 = coil.R0;
            in r_coil = 'Magnet System'::r_coil;
            in cost_per_kAm = coil.cost_per_kAm;
            in coil_markup = coil.coil_markup;
        }
        // WI-040 explicit non-tape procurement: only geometric winding-pack volume.
        calc material_inventory : 'Winding Pack Material Inventory' {
            in volume_in = wp_volume.vol_winding_pack;
            in f_copper = winding_pack.f_copper;
            in f_solder = winding_pack.f_solder;
            in f_steel = winding_pack.f_steel;
            in f_helium = winding_pack.f_helium;
            in rho_copper = winding_pack.rho_copper;
            in rho_solder = winding_pack.rho_solder;
            in rho_steel = winding_pack.rho_steel;
            in price_copper = winding_pack.price_copper;
            in price_solder = winding_pack.price_solder;
            in price_steel = winding_pack.price_steel;
            in price_helium = winding_pack.price_helium;
            in helium_pressure = winding_pack.helium_pressure;
            in temperature = winding_pack.T_inventory;
            in helium_gas_constant = winding_pack.helium_gas_constant;
        }
        calc winding_procurement : 'Winding Pack Procurement Cost' {
            in n_coils = coil.n_coils;
            in I_coil = coil.I_coil;
            in f_set = coil.f_set;
            in c_coil = coil.c_coil;
            in tape_volume_in = material_inventory.tape_volume;
            in tape_width = winding_pack.tape_width;
            in tape_thickness = winding_pack.tape_thickness;
            in tape_price_per_m = winding_pack.tape_price_per_m;
            in turn_current = coil.turn_current;
            in winding_rate_1990 = winding_pack.winding_rate_1990;
            in cost_escalation = winding_pack.cost_escalation;
            in nonplanar_factor = winding_pack.nonplanar_factor;
            in material_cost_in = material_inventory.material_cost;
        }
        // Legacy unsplit winding-pack account retained for comparison (WI-035 D4).
        calc winding_pack_cost : 'Winding Pack Cost' {
            in n_coils = coil.n_coils;
            in I_coil = coil.I_coil;
            in f_set = coil.f_set;
            in c_coil = coil.c_coil;
            in cost_per_kAm = coil.cost_per_kAm;
            in f_wp_fab = winding_pack.f_wp_fab;
        }
        // WI-059 electromagnetic support account: total supports or legacy
        // casing basis, selected by the explicit coefficient and fraction.
        // Total-support mode allocates a separate nonmagnet residual CAS22.1.5.
        calc magnet_structure_cost : 'Magnet Structure Cost' {
            in m_support = 'Magnet System'::m_support;
            in legacy_casing_fraction = 'Magnet System'::legacy_casing_fraction;
            in n_coils = coil.n_coils;
            in m_casing = casing.m_casing;   // WI-044: computed (casing_mass)
            in steel_price = casing.steel_price;
            in f_steel_fab = casing.f_steel_fab;
        }
        // CAS22.1.3 rollup (WI-035 D6): reference-binding envelope.
        calc magnet_capital_rollup : 'Magnet Capital' {
            in winding_cost = 'Magnet System'::winding_cost;
            in structure_cost_in = structure_cost;
        }
    }

    part def 'Heating and CD' :> 'CAS22.1.4 Heating and Current Drive' {
        // ---- ports (WI-057): the exchanges this part takes part in; declarative, see mfe_interfaces ----
        port electric_in : ~'Electric Port';   // <- electric_plant.recirculating (pb.p_wallplug_in)
        port power_to_plasma : 'Thermal Port';   // -> plasma.heat_in (heat.p_coupled)
        // WI-057: the heating's own facts, moved from the plant (formerly plant-level inputs)
        // Heating power chain (WI-039). Dormant by default, on the WI-024
        // cryoplant pattern: a concept that knows its heating powers outright
        // binds the direct terms and leaves the chain unbound; a concept
        // deriving them binds the chain and zeroes the direct terms. The
        // efficiencies default to 1.0 (not 0) so a dormant chain's effective
        // efficiency stays defined -- the mode is selected by the powers,
        // never by an efficiency.
        // installed wall-plug electrical power for heating [MW]
        attribute p_wallplug_heat : Real default 0.0;
        // wall-plug -> source output conversion efficiency [1]
        attribute eta_source_heat : Real default 1.0;
        // source output -> plasma-coupled fraction [1] (deposition assumption)
        attribute eta_couple_heat : Real default 1.0;
        // directly-specified source-output heating power [MW] (dormant path)
        attribute p_delivered_direct_heat : Real default 0.0;
        // directly-specified plasma-coupled heating power [MW] (dormant path)
        attribute p_coupled_direct_heat : Real default 0.0;
        // Heating & CD (CAS22.1.4) -- WI-009 carrier has no drivers; the heating
        // mix (per-MW rates + delivered powers) is supplied here (WI-011).
        attribute heating_nbi_per_mw : Real;
        attribute p_nbi : Real;
        attribute heating_icrf_per_mw : Real;
        attribute p_icrf : Real;
        attribute heating_ecrh_per_mw : Real;
        attribute heating_lhcd_per_mw : Real;
        attribute p_lhcd : Real;
        doc /*
        Concept-agnostic supplementary heating / current-drive costed component.
        Carries `capital_cost` (inherited from 'Costed Component'); the per-MW
        heating mix and its cost are set per concept in WI-011.

        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
        **Ref**: cas22.py:453-459 (C220104 per-MW heating costs)
        **Basis**: MFE heating/current-drive account; concept-agnostic carrier
        */
        // ---- EXPOSEs (WI-057): this part's calc outputs, readable outside as <part>.<name> ----
        attribute p_coupled : Real = heat.p_coupled;
        attribute p_wallplug_total : Real = heat.p_wallplug_total;
        :>> capital_cost = heating_cost.cost;
        // ---- template calcs (WI-057): the analyses this part owns ----
        calc heat : 'Heating Power Chain' {
            in p_wallplug = p_wallplug_heat;
            in eta_source = eta_source_heat;
            in eta_couple = eta_couple_heat;
            in p_delivered_direct = p_delivered_direct_heat;
            in p_coupled_direct = p_coupled_direct_heat;
        }
        calc heating_cost : 'Heating Cost' {
            in nbi_per_mw = heating_nbi_per_mw;
            in p_nbi_in = p_nbi;
            in icrf_per_mw = heating_icrf_per_mw;
            in p_icrf_in = p_icrf;
            in ecrh_per_mw = heating_ecrh_per_mw;
            in p_ecrh_in = heat.p_delivered;
            in lhcd_per_mw = heating_lhcd_per_mw;
            in p_lhcd_in = p_lhcd;
        }
    }

    part def 'Divertor' :> 'CAS22.1.8 Divertor' {
        // ---- ports (WI-057): the exchanges this part takes part in; declarative, see mfe_interfaces ----
        port heat_in : ~'Thermal Port';   // <- plasma.alpha_out (divheat)
        // WI-057: the divertor's own facts, moved from the plant (formerly plant-level inputs)
        // Divertor (CAS22.1.8) -- WI-009 carrier has no drivers; supplied here.
        // divertor cost at 1 GWth [$] (WI-011)
        attribute divertor_base : Real;
        // ---- Divertor surface-heat ledger (WI-047) on the INSTALLED heating
        // basis (the thermal sum's own operand) -- round 1 of goal plant-closure.
        // Dormant-safe: q_target_ref 0 and p_nonrad_ref 1 give a zero peak and a
        // satisfied fence for a concept binding nothing.
        attribute f_rad_total : Real default 0.0;
        attribute q_target_ref : Real default 0.0;
        attribute p_nonrad_ref : Real default 1.0;
        attribute q_target_limit : Real default 1.0;
        attribute R_ref_divertor : Real default 1.0;
        doc /*
        Concept-agnostic divertor costed component. Carries `capital_cost`
        (inherited from 'Costed Component'); the power-scaled divertor cost is
        set per concept in WI-011.

        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
        **Ref**: cas22.py:570 (C220108 divertor, power-scaled)
        **Basis**: MFE divertor account; concept-agnostic carrier
        */
        // ---- inputs the plant wires (WI-057): values produced elsewhere, read here by name ----
        attribute R : Real;   // <- plasma.R
        attribute p_alpha_heat : Real;   // <- plasma.p_alpha_heat
        attribute p_aux_required : Real;   // <- plasma.p_aux_required
        attribute p_coupled : Real;   // <- operating_heat.p_coupled (WI-050: the operating demand)
        attribute p_installed_coupled : Real;   // <- heating.p_coupled (WI-050: the installed delivery)
        attribute p_rad : Real;   // <- plasma.p_rad
        attribute p_th : Real;   // <- pb.p_th
        // ---- EXPOSEs (WI-057): this part's calc outputs, readable outside as <part>.<name> ----
        attribute q_target_peak : Real = divheat.q_target_peak;
        :>> capital_cost = divertor_cost.cost;
        // ---- template calcs (WI-057): the analyses this part owns ----
        calc divertor_cost : 'Divertor Cost' {
            in base = divertor_base;
            in p_th_in = p_th;
        }
        calc divheat : 'Divertor Heat Ledger' {
            in p_alpha_heat_in = p_alpha_heat;
            in p_coupled_in = p_coupled;
            in p_aux_required_in = p_aux_required;
            in p_installed_coupled_in = p_installed_coupled;
            in p_rad_core_in = p_rad;
            in f_rad_total_in = f_rad_total;
            in q_target_ref_in = q_target_ref;
            in p_nonrad_ref_in = p_nonrad_ref;
            in q_target_limit_in = q_target_limit;
            in R_in = R;
            in R_ref_in = R_ref_divertor;
        }
    }
}
