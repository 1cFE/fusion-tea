package stellarator_09 {
    private import ScalarValues::*;
    private import mfe_plant::*;
    private import mfe_plasma_scaling::*;
    private import mfe_viability::*;

    // =========================================================================
    // CONCRETE INSTANCE — concept-09 Proxima "Stellaris" QI stellarator
    //
    // Binds the Stellaris design point. Physics/geometry cite the admissible
    // Stellaris sources; engineering and cost inputs cite 1costingFE defaults
    // (steady_state_stellarator.yaml + costing_constants.yaml), converted M$ ->
    // $ (x 1e6) to match the plant's dollar rollup. This concrete `part`
    // instantiates 'MFE Power Plant' DIRECTLY, which clears the abstract-layer
    // L6 flag (WI-015 codegen lesson).
    //
    // FAMILY-LAYER NOTE: WI-018 originally introduced an intermediate
    // `abstract part def 'Stellarator Plant' :> 'MFE Power Plant'` (spec item A,
    // marked optional). It was collapsed into this concrete instance because
    // syside's PartUsage.types does not surface a grandparent through an
    // intermediate abstract def — a `part x : 'Stellarator Plant'` reports
    // types ['Stellarator Plant', 'Part', ...] and never 'MFE Power Plant', so
    // the two-level chain leaves 'MFE Power Plant' flagged NO_INSTANTIATION
    // (its template calcs would be dropped at extraction). Typing the instance
    // directly on 'MFE Power Plant' (the hif_plant idiom) clears the flag. The
    // stellarator family choices (density-direct, ECRH-only/no current drive, no
    // separate PF coils, G = 8*pi^2) are applied inline and marked below.
    // =========================================================================

    part stellaris : 'MFE Power Plant' {
        doc /*
        Proxima Fusion "Stellaris" — concept-09 QI stellarator HTS power plant,
        evaluated at operating point A. The Stellaris design point is 2700 MW
        fusion; the model computes 2748 MW (+1.8%) by integrating the
        Bosch-Hale reactivity over the source's own profiles (WI-022 — every
        profile parameter fixed from the source's figure and printed tables,
        blind to the power; see the sigma_v note).

        STELLARATOR FAMILY CHOICES (applied inline, not concept-specific numbers):
          - Density is a direct input (no tokamak Greenwald closure) — already the
            generic plant's behaviour (n_e is a plain input to 'DT Fusion Power').
          - ECRH-only heating, no current drive: p_nbi = p_icrf = p_lhcd = 0 and
            their per-MW costs = 0 (QI stellarator is intrinsically steady-state).
          - No separate poloidal-field coil set: p_pf = 0, p_pfcool = 0 (3D
            modular coils only).
          - Stellarator coil geometry factor G = 8*pi^2 (vs tokamak 4*pi^2), bound
            on the magnet subsystem.

        HEADLINE FORWARD-PASS RESULT (WI-025 stale-basis pass-through recompute;
        executed in exploration/stellarator_e2e/run_stellaris.py):
        plasma volume 425 m^3 (printed value; a = 1.3), fusion power 2748.1 MW
        (profile-integrated, +1.8% vs the 2700 design point), thermal power
        3238 MW, gross electric 1078 MW, net electric 915.081 MW, recirculating
        fraction 0.15136, q_eng 6.6067, total overnight capital $12.64B, LCOE
        $203.647/MWh (FOAK). Magnet $6.32B (50.03%) at the printed axis-averaged
        B_0 = 9.0 T and the stellarator 5.87 REBCO markup.
        (History: WI-018 lossy balance net 575, ~$251/MWh; WI-019 faithful
        balance at torus volume net 786, ~$189/MWh; WI-020 corrected the
        volume to the then-tabulated 448, net 578, ~$247/MWh; WI-022 replaced
        the 0D reactivity with the sourced profile integral and rebound the
        geometry to the image-verified a = 1.3 / V = 425, net 804.1,
        ~$176/MWh, magnet 42.9%; WI-023 rebound the magnet field to the
        printed 9.0 T — 5.86 was a phantom text row — and zeroed the phantom
        p_tf = 111, which the paper prints only as stored magnetic energy in
        GJ, not a power, net 915.145, ~$201.46/MWh; WI-024 derived the cryo
        parasitic load from the winding-pack heat inventory, retired the
        0.8 MW 1costingFE default, and rescoped p_tf to a modeled zero,
        ~$201.47/MWh; WI-025 forward-computed the last three pass-through
        cost accounts — CAS21 buildings, CAS10 preconstruction, CAS70 annual
        O&M — from the model's computed powers, retiring the final STALE
        BASIS annotations, total $12.60B -> $12.64B, ~$203.65/MWh.)

        THREE MAPPING TRAPS (documented at their bindings below): r_coil (coil
        bore = radial-build vessel outer radius, not a guess), sigma_v (0D
        bypass input — sigma_v = 0 here selects the profile-integrated
        reactivity in the handwritten codegen stage), and B (coil-cost field is
        the axis-averaged B_0 = 9.0 T printed in the Table 2/5 images, NOT the
        24.9 T peak-on-winding).

        **Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md
        **Ref**: Table 2 image (images/page_002_table_0.png), Table 5 image
            (images/page_009_table_0.png), Fig. 16 panels (digitized,
            work/active/WI-022_predictive-confinement/prototype/)
        **Basis**: Stellaris design point A + 1costingFE stellarator cost defaults
        */

        // ---------------------------------------------------------------------
        // MAGNET SUBSYSTEM (CAS22.1.3)
        // ---------------------------------------------------------------------
        part :>> magnet {
            doc /*
            Stellaris HTS modular-coil system.

            MAPPING TRAP (B vs b_center): the coil-cost field is the axis-averaged
            (loop-center) field 9.0 T, NOT the 24.9 T peak field on the winding
            pack printed beside it in Table 2. The ampere-meter conductor-quantity
            model uses the field at the loop center; the peak-on-winding is a
            conductor-grade concern, not a cost-quantity term.
            (History: the prior B = 5.86 cited a Table 3 text row absent from the
            table image and from the published paper — raw.pdf-confirmed, WI-023.)

            MAPPING TRAP (r_coil): the coil-bore radius = the radial-build vessel
            outer radius (vessel_or). From the stellarator radial build:
              vessel_or = a + vacuum_t + firstwall_t + blanket_t + reflector_t
                          + ht_shield_t + structure_t + gap1_t + vessel_t
                        = 1.3 + 0.10 + 0.05 + 0.80 + 0.20 + 0.20 + 0.15 + 0.10 + 0.10
                        = 3.00 m
            The blanket/shield/structure/vessel thicknesses are the 1costingFE
            stellarator defaults; the vacuum/firstwall/reflector/gap thicknesses
            are the RadialBuild dataclass defaults; a = 1.3 m is the Stellaris
            minor radius (Table 2 image, WI-022 errata rebind). Layer-sum formula
            verified against costingfe.layers.geometry (geometry.py:106-114).

            **Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md
            **Ref**: Table 2 image (images/page_002_table_0.png: axis av. field 9.0 T; peak
                conductor 24.9 T); Table 5 image (images/page_009_table_0.png: axis-averaged
                B_0 9.0 T, Points A/B); phantom 5.86 refuted vs knowledge/concept_research/
                09-qi-stellarator-hts/iter-02/sources/publikationen-1000179851-172386752/
                tmpissrtbos/raw.pdf (no "5.86" in the published paper; Table 3 has no field
                row); geometry.py:106-114 (vessel_or layer sum);
                steady_state_stellarator.yaml:39-42 (thicknesses)
            **Basis**: coil bore = radial-build vessel_or; axis-averaged on-axis field for cost
            */

            // G = 8*pi^2 stellarator geometry factor (family constant).
            // Source: costing_constants.yaml coil geometry (stellarator G=8pi^2);
            //   literal to stay in the codegen envelope (no redef expr drop).
            :>> G = 78.95683520871486;
            // Axis-averaged (loop-center) field [T]. Source: Table 2 image
            //   (page_002_table_0.png: "Axis av. magnetic field strength [T] 9.0") and
            //   Table 5 image (page_009_table_0.png: "Axis averaged B_0 [T] 9.0", Points
            //   A and B). NOT the 24.9 T peak-on-winding printed beside it in Table 2.
            :>> B = 9.0;
            // Major radius [m]. Source: stellaris-design-details.md Table 2 /
            //   line 251 (R ~= 12.7 m).
            :>> R0 = 12.7;
            // Coil-bore radius [m] = radial-build vessel_or. Forward-computed
            // (WI-021): the generic plant binds magnet.r_coil = rb.r_coil, so
            // r_coil = 3.00 m falls out of the radial build (was an injected
            // constant here).
            // REBCO HTS conductor [$/kA-m]. Source: costing_constants.yaml:57
            //   (conductor_cost_rebco = 50.0). NOT x1e6 — already $/kA-m; the
            //   magnet formula omits the /1e6 M$ conversion and yields $.
            :>> cost_per_kAm = 50.0;
            // Stellarator conductor->installed markup. Source: costing_constants.
            //   yaml:75 (coil_markup.stellarator = 5.87).
            :>> coil_markup = 5.87;
        }

        // ---------------------------------------------------------------------
        // SHARED POWER-CORE SUBSYSTEMS (CAS22.1.x) — cost drivers ($, volumes m^3)
        // Volumes from costingfe.layers.geometry.compute_geometry(STELLARATOR)
        // at the Stellaris radial build; unit costs are 1costingFE M$ x 1e6.
        // ---------------------------------------------------------------------
        part :>> blanket {
            doc /*
            HCLL (helium-cooled lithium-lead / PbLi) breeding blanket.
            unit_cost: costing_constants.yaml:37 (blanket_unit_cost_dt = 0.60 M$/m^3) x 1e6.
            structure_factor: types.py:153 (LIQUID_METAL = 1.0).
            blanket_vol = firstwall_vol + blanket_vol + reflector_vol = 1118.695 m^3.
              Forward-computed (WI-021): the generic plant binds
              blanket.blanket_vol = rb.blanket_vol from the radial build, so this
              value falls out of the layer thicknesses (was an injected constant).
            **Source**: /home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml
            **Ref**: costing_constants.yaml:37; types.py:152-157; geometry.py:157-160; model.py:1205
            **Basis**: volume-based blanket cost; Stellaris HCLL PbLi (details.md line 1342)
            */
            :>> unit_cost = 600000.0;
            :>> structure_factor = 1.0;
        }
        part :>> shield {
            doc /*
            unit_cost: costing_constants.yaml:43 (shield_unit_cost = 0.74 M$/m^3) x 1e6.
            shield_scale: cas22.py:262 (DT = 1.0).
            shield_vol = ht_shield_vol + lt_shield_vol = 552.140 m^3. Forward-
              computed (WI-021): generic plant binds shield.shield_vol =
              rb.shield_vol from the radial build (was an injected constant).
            **Source**: /home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml
            **Ref**: costing_constants.yaml:43; cas22.py:261-266; geometry.py:161,164; model.py:1206
            **Basis**: volume-based shield cost, DT neutron-load scale
            */
            :>> unit_cost = 740000.0;
            :>> shield_scale = 1.0;
        }
        part :>> structure {
            doc /*
            unit_cost: costing_constants.yaml:46 (structure_unit_cost = 0.15 M$/m^3) x 1e6.
            structure_vol = 219.979 m^3. Forward-computed (WI-021): generic plant
              binds structure.structure_vol = rb.structure_vol from the radial
              build (was an injected constant).
            **Source**: /home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml
            **Ref**: costing_constants.yaml:46; geometry.py:162; model.py:1207
            **Basis**: volume-based primary-structure cost
            */
            :>> unit_cost = 150000.0;
        }
        part :>> vessel {
            doc /*
            unit_cost: costing_constants.yaml:83 (vessel_unit_cost = 0.72 M$/m^3) x 1e6.
            vessel_vol = 157.933 m^3 = vol(gap1_or, vessel_or). Forward-computed
              (WI-021): generic plant binds vessel.vessel_vol = rb.vessel_vol from
              the radial build (was an injected constant).
            **Source**: /home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml
            **Ref**: costing_constants.yaml:83; geometry.py:163; model.py:1208
            **Basis**: volume-based vacuum-vessel shell cost
            */
            :>> unit_cost = 720000.0;
        }
        part :>> power_supplies {
            doc /*
            base: costing_constants.yaml:96 (power_supplies_base = 80.0 M$ at 1 GWe) x 1e6.
            **Source**: /home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml
            **Ref**: costing_constants.yaml:96
            **Basis**: power-scaled power-supply cost
            */
            :>> base = 80000000.0;
        }

        // ---------------------------------------------------------------------
        // BALANCE OF PLANT (CAS23-26) — per-MW rates ($/MW), Rankine steam cycle
        // ---------------------------------------------------------------------
        part :>> turbine {
            doc /*
            cost_per_mw: defaults.py:580 (POWER_CYCLE_DEFAULTS RANKINE turbine_per_mw
            = 0.20284 M$/MW) x 1e6. Stellaris uses a steam (Rankine) cycle at
            eta_th = 1/3 (details.md line 251).
            **Source**: /home/reid/1cfe/1costingfe/src/costingfe/defaults.py
            **Ref**: defaults.py:578-581 (RANKINE preset)
            **Basis**: turbine plant linear in thermal-electric power
            */
            :>> cost_per_mw = 202840.0;
        }
        part :>> electric_plant {
            doc /*
            cost_per_mw: costing_constants.yaml:222 (electric_per_mw = 0.08640 M$/MW) x 1e6.
            **Source**: /home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml
            **Ref**: costing_constants.yaml:222
            **Basis**: electric plant linear in gross electric
            */
            :>> cost_per_mw = 86400.0;
        }
        part :>> heat_rejection {
            doc /*
            cost_per_mw: defaults.py:581 (RANKINE heat_rej_per_mw = 0.03506 M$/MW) x 1e6.
            **Source**: /home/reid/1cfe/1costingfe/src/costingfe/defaults.py
            **Ref**: defaults.py:578-581 (RANKINE preset)
            **Basis**: heat rejection linear in total thermal power
            */
            :>> cost_per_mw = 35060.0;
        }
        part :>> misc_plant {
            doc /*
            cost_per_mw: costing_constants.yaml:223 (misc_per_mw = 0.05259 M$/MW) x 1e6.
            **Source**: /home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml
            **Ref**: costing_constants.yaml:223
            **Basis**: miscellaneous plant linear in gross electric
            */
            :>> cost_per_mw = 52590.0;
        }

        // ---------------------------------------------------------------------
        // CAS21 BUILDINGS ($) — forward-computed (WI-025): buildings_cost tracks
        // the model's p_fus/p_the/p_th/p_et (p_the = p_et, no DEC — costs.py:104).
        // The six base sums below are the exact grouped collapse of the
        // 18-building DT column (every building linear in exactly one scaling
        // basis), cryogenics included (SC coils, REBCO HTS — costs.py:137);
        // DT and n_mod = 1 frozen at the design point. Stale basis retired:
        // the old $613.65M literal was computed at pre-WI-019 powers
        // (p_et 896.8 / p_th 2693.1).
        // ---------------------------------------------------------------------
        :>> bldg_fixed_base = 168500000.0 {  // fixed-basis base costs [$].
            doc /* 168.5 M$ x 1e6 = site_improvements 85 + fuel_storage 9 +
            control_room 14 + security 3.5 + maintenance 17 + site_services 5 +
            cryogenics 14 (SC-gated, applies: REBCO HTS, costs.py:137) +
            assembly_hall 21 (all DT column).
            **Source**: /home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml
            **Ref**: costing_constants.yaml:177,183-185,188-189,195,197
            **Basis**: exact grouped sum, fixed-scaling buildings (WI-025 D1) */
        }
        :>> bldg_fus_base = 288000000.0 {  // p_fus-scaled base costs [$].
            doc /* 288 M$ x 1e6 = reactor_building 138 + hot_cell 104 +
            reactor_auxiliaries 29 + ventilation_hvac 17 (DT column); scales
            as p_fus x n_mod / 2300 (costs.py:106,126).
            **Source**: /home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml
            **Ref**: costing_constants.yaml:179-181,186
            **Basis**: exact grouped sum, p_fus-scaled buildings (WI-025 D1) */
        }
        :>> bldg_staff_base = 9000000.0 {  // staff-scaled base costs [$].
            doc /* 9 M$ x 1e6 = administration 9 (DT column); staff-driven,
            scales as sqrt(p_et x n_mod / 1100) (costs.py:127-129).
            **Source**: /home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml
            **Ref**: costing_constants.yaml:187; costs.py:127-129
            **Basis**: exact grouped sum, staff-scaled buildings (WI-025 D1) */
        }
        :>> bldg_the_base = 58000000.0 {  // p_the-scaled base costs [$].
            doc /* 58 M$ x 1e6 = turbine_building 58 (fuel-independent);
            scales as p_the x n_mod / 1100 (costs.py:104,124 — p_the = p_et,
            no DEC; ref_gross costing_constants.yaml:12).
            **Source**: /home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml
            **Ref**: costing_constants.yaml:191
            **Basis**: exact grouped sum, p_the-scaled buildings (WI-025 D1) */
        }
        :>> bldg_th_base = 26000000.0 {  // p_th-scaled base costs [$].
            doc /* 26 M$ x 1e6 = heat_exchanger 17 + service_water 9
            (fuel-independent); scales as p_th x n_mod / 2500 (costs.py:105,125).
            **Source**: /home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml
            **Ref**: costing_constants.yaml:192,196
            **Basis**: exact grouped sum, p_th-scaled buildings (WI-025 D1) */
        }
        :>> bldg_et_base = 29000000.0 {  // p_et-scaled base costs [$].
            doc /* 29 M$ x 1e6 = power_supply 17 + onsite_ac 12
            (fuel-independent); scales as p_et x n_mod / 1100 (costs.py:103,123;
            ref_gross costing_constants.yaml:12).
            **Source**: /home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml
            **Ref**: costing_constants.yaml:193-194
            **Basis**: exact grouped sum, p_et-scaled buildings (WI-025 D1) */
        }

        // Physics geometry inputs.
        // PLASMA GEOMETRY (WI-022 errata rebind, owner-amended ruling 2026-07-18):
        // the printed Stellaris geometry is a = 1.3 m with plasma volume
        // 425-428 m^3 (Table 2 image: a = 1.3, V = 428; Table 5 image: V = 425
        // at R = 12.74). The circular torus at the model's R = 12.7 gives
        // 2*pi^2*12.7*1.3^2 = 423.66 m^3, so the QI shaping correction is ~0.3%
        // (f_shape below targets the printed 425). The pre-WI-022 bindings
        // (a = 1.5, V = 448, f_shape = 0.7943) were built on garbled
        // text-extraction rows of Tables 2/5; the WI-020 "empirical packing
        // factor" reconciled one extraction artifact against another. R stays
        // 12.7 (Table 2 image; magnet R0 consistency).
        :>> R = 12.7 {        // major radius [m].
            doc /* **Source**: stellaris-design-details.md **Ref**: Table 2 image (images/page_002_table_0.png: major plasma radius 12.7 m); prose line 251 **Basis**: Stellaris major radius */
        }
        :>> a = 1.3 {         // minor radius [m] (WI-022 errata rebind).
            doc /* **Source**: stellaris-design-details.md **Ref**: Table 2 image (images/page_002_table_0.png: minor plasma radius 1.3 m; the extracted text row "a = 1.5" is an extraction artifact) **Basis**: Stellaris plasma minor radius */
        }
        :>> kappa = 1.0 {     // elongation. QI stellarator ~ circular average.
            doc /* **Source**: stellaris-design-details.md **Ref**: line 251 (near-circular avg cross-section); analyst-patch-spec-anchors.md line 30 (elon=1.0) **Basis**: stellarator ~circular average cross-section */
        }
        :>> f_shape = 1.0031567 {  // QI shaping correction [1] (WI-022).
            doc /* **Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details/images/page_009_table_0.png (Table 5: plasma volume 425 m^3); images/page_002_table_0.png (Table 2: 428 m^3) **Ref**: printed V = 425 / torus V(R=12.7, a=1.3, kappa=1.0) = 425/423.663 = 1.0031567 **Basis**: residual QI shaping correction (~0.3%) reconciling the circular torus to the printed plasma volume; supersedes the empirical 0.7943 built on garbled extraction rows */
        }

        // Radial-build layer thicknesses [m] (WI-021). The Stellaris stellarator
        // build: blanket_t/ht_shield_t/structure_t/vessel_t from 1costingFE's
        // steady_state_stellarator.yaml; the remaining layers from the RadialBuild
        // dataclass defaults. Bound explicitly (not left to the generic-plant
        // defaults) so the generated snapshot carries the correct rb__*_t values
        // and every thickness names its source. rb forward-computes the four CAS22
        // volumes, the first-wall area, and the coil bore from these.
        :>> blanket_t = 0.80 {
            doc /* **Source**: /home/reid/1cfe/1costingfe/src/costingfe/data/defaults/steady_state_stellarator.yaml **Ref**: steady_state_stellarator.yaml:39 (blanket_t = 0.80) **Basis**: Stellaris breeding-blanket thickness */
        }
        :>> ht_shield_t = 0.20 {
            doc /* **Source**: /home/reid/1cfe/1costingfe/src/costingfe/data/defaults/steady_state_stellarator.yaml **Ref**: steady_state_stellarator.yaml:40 (ht_shield_t = 0.20) **Basis**: Stellaris high-temp shield thickness */
        }
        :>> structure_t = 0.15 {
            doc /* **Source**: /home/reid/1cfe/1costingfe/src/costingfe/data/defaults/steady_state_stellarator.yaml **Ref**: steady_state_stellarator.yaml:41 (structure_t = 0.15) **Basis**: Stellaris primary-structure thickness */
        }
        :>> vessel_t = 0.10 {
            doc /* **Source**: /home/reid/1cfe/1costingfe/src/costingfe/data/defaults/steady_state_stellarator.yaml **Ref**: steady_state_stellarator.yaml:42 (vessel_t = 0.10) **Basis**: Stellaris vacuum-vessel wall thickness */
        }
        :>> vacuum_t = 0.10 {
            doc /* **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/geometry.py **Ref**: geometry.py:29 (RadialBuild.vacuum_t = 0.10 default) **Basis**: radial-build vacuum-gap default */
        }
        :>> firstwall_t = 0.05 {
            doc /* **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/geometry.py **Ref**: geometry.py:30 (RadialBuild.firstwall_t = 0.05 default) **Basis**: radial-build first-wall default */
        }
        :>> reflector_t = 0.20 {
            doc /* **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/geometry.py **Ref**: geometry.py:32 (RadialBuild.reflector_t = 0.20 default) **Basis**: radial-build reflector default */
        }
        :>> gap1_t = 0.10 {
            doc /* **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/geometry.py **Ref**: geometry.py:35 (RadialBuild.gap1_t = 0.10 default) **Basis**: radial-build assembly-gap default */
        }
        :>> coil_t = 0.30 {
            doc /* **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/geometry.py **Ref**: geometry.py:37 (RadialBuild.coil_t = 0.30 default) **Basis**: radial-build coil-pack default */
        }
        :>> gap2_t = 0.10 {
            doc /* **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/geometry.py **Ref**: geometry.py:38 (RadialBuild.gap2_t = 0.10 default) **Basis**: radial-build outer-gap default */
        }
        :>> lt_shield_t = 0.15 {
            doc /* **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/geometry.py **Ref**: geometry.py:39 (RadialBuild.lt_shield_t = 0.15 default) **Basis**: radial-build low-temp shield default */
        }

        // Fusion-power inputs.
        :>> n_e = 3.17e20 {   // vol-avg electron density [m^-3], point A (WI-022 corrected).
            doc /* **Source**: stellaris-design-details.md **Ref**: Table 5 image (images/page_009_table_0.png: vol.-av. el. density 3.17e20 m^-3, Point A; the extracted text "3.37" is an extraction artifact) **Basis**: Stellaris operating point A. Reference/handshake-only in profile mode (sigma_v = 0 below): the profile path computes fusion from the peak fuel densities, not n_e. */
        }
        :>> sigma_v = 0.0 {  // 0D bypass OFF -> profile-integrated reactivity (WI-022).
            doc /*
            sigma_v = 0 selects the profile-integrated path of 'DT Fusion
            Power': fusion power is computed by integrating the Bosch-Hale
            reactivity over the source's own profiles (the n_D0/n_T0/T_i0/
            alpha_n/alpha_T referents below) — the model's realization of the
            source's 0.5D volume-integrated power balance (Appendix A). The
            reactivity physics executes at the handwritten codegen stage
            (Rung B, owner-ratified) and is guarded bit-exact by the oracle.

            This closes the former "0D gap": pre-WI-022 the injected
            0D-effective reactivity (5.985e-23 at T_eff ~= 7.9 keV) gave
            ~2145 MW vs the 2700 MW design point, the visible 0D
            single-temperature limitation. The profile integral computes
            ~2748 MW at the printed volume 425 m^3 — within ~2% of the design
            point, with every parameter fixed from the source's own figure and
            tables blind to the power (Decision A: honest physics, not tuned).

            The Anchor A handshake still injects sigma_v > 0, which selects
            the exact legacy 0D form (0.25*n_e^2*sigma_v*E_fus*V) and
            reproduces 1costingFE's 0D point unchanged.

            **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/reactivity.py
            **Ref**: reactivity.py:54-70 (sigv_dt Bosch-Hale D-T, realized in
                the handwritten impl); stellaris-design-details.md Appendix A
                line 2912 (0.5D volume-integrated power balance); Table 5 image
                (images/page_009_table_0.png: fusion power 2700 MW, Point A)
            **Basis**: profile-integrated reactivity replaces the 0D-effective
                constant; sigma_v = 0 disables the bypass on this instance
            */
        }
        :>> E_fus = 2.817e-12 {  // per-event D-T fusion energy [J].
            doc /* **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/physics.py **Ref**: physics.py:31 (Q_DT = 17.58 MeV x 1.602176634e-13 J/MeV = 2.817e-12 J) **Basis**: D-T fusion Q-value */
        }

        // Profile referents (WI-022, Decision C): derived from the source's own
        // primary data, fixed blind to the fusion power. Exponents are digitized
        // fits of the Fig. 16 panels (work/active/WI-022_predictive-confinement/
        // prototype/digitize_fig16.py: alpha_T = 1.19 all species rms 0.02;
        // alpha_n(fuel) = 0.33 rms 0.006), corroborated by the a/L_T ~= 2.25
        // gradient quote (line 714) and the rho = 0.8 GENE/TANGO boundary values
        // (line 762). The extracted Fig.-16 caption "alpha_n = 1.2, alpha_T =
        // 3.0" is an extraction artifact refuted by the figure it captions
        // (spec errata). The fuel term is n_D*n_T with the diluted peak fuel
        // densities — quasineutrality closes at the peak: 2x1.96 (fuel) +
        // 2x0.56 (He ash) ~= 5.06 = printed peak n_e.
        :>> n_D0 = 1.96e20 {  // peak deuterium density [m^-3].
            doc /* **Source**: stellaris-design-details.md **Ref**: Table 5 image (images/page_009_table_0.png: peak D density 1.96e20, Point A) **Basis**: Stellaris Point-A peak deuterium density (ash/impurity-diluted) */
        }
        :>> n_T0 = 1.96e20 {  // peak tritium density [m^-3].
            doc /* **Source**: stellaris-design-details.md **Ref**: Table 5 image (images/page_009_table_0.png: peak T density 1.96e20, Point A) **Basis**: Stellaris Point-A peak tritium density (50:50 fuel mix) */
        }
        :>> T_i0 = 14.63 {    // peak ion temperature [keV].
            doc /* **Source**: stellaris-design-details.md **Ref**: Table 5 image (images/page_009_table_0.png: peak ion temperature 14.63 keV, Point A; the extracted text "24.60" is an extraction artifact) **Basis**: Stellaris Point-A peak ion temperature */
        }
        :>> alpha_n = 0.33 {  // fuel density profile exponent [1].
            doc /* **Source**: stellaris-design-details.md Fig. 16 density panel **Ref**: images/stellaris-high-field-quasi-isodynamic-stellarator.pdf-9-0.png, digitized fit (prototype/digitize_fig16.py; D and T curves, rms log-residual 0.006) **Basis**: n(rho) = n0*(1-rho^2)^alpha_n (Eq. 3, image-verified) fuel-profile exponent, fixed blind to the fusion power */
        }
        :>> alpha_T = 1.19 {  // temperature profile exponent [1].
            doc /* **Source**: stellaris-design-details.md Fig. 16 temperature panel **Ref**: images/stellaris-high-field-quasi-isodynamic-stellarator.pdf-9-1.png, digitized fit (prototype/digitize_fig16.py; all three species, rms log-residual 0.02); corroborated by a/L_T ~= 2.25 at rho=0.6 (line 714) and the rho=0.8 Dirichlet values 4.2/5.2 keV (line 762) **Basis**: T(rho) = T0*(1-rho^2)^alpha_T (Eq. 2, image-verified) exponent, fixed blind to the fusion power */
        }

        // Power-balance inputs.
        :>> p_input = 50.0 {  // plasma heating power [MW] (ECRH wallplug).
            doc /* **Source**: stellaris-design-details.md **Ref**: line 237 / line 710 (50 MW ECRH to reach point A); analyst-patch-spec-anchors.md line 29 **Basis**: Stellaris auxiliary heating power */
        }
        :>> mn = 1.2 {        // blanket neutron energy multiplier.
            doc /* **Source**: stellaris-design-details.md **Ref**: line 1664/1831 (power multiplication 1.20, HCLL blanket) **Basis**: Stellaris HCLL blanket energy multiplication */
        }
        :>> eta_th = 0.333 {  // thermal-to-electric efficiency (1/3).
            doc /* **Source**: stellaris-design-details.md **Ref**: line 251 (single-element conversion efficiency 1/3) **Basis**: Stellaris steam-cycle thermal efficiency */
        }
        :>> eta_p = 0.5 {     // pumping-power capture efficiency.
            doc /* **Source**: /home/reid/1cfe/1costingfe/src/costingfe/data/defaults/steady_state_stellarator.yaml **Ref**: steady_state_stellarator.yaml:14 (eta_p = 0.5) **Basis**: 1costingFE stellarator pumping efficiency */
        }
        :>> eta_pin = 0.5 {   // input-power wall-plug efficiency (ECRH).
            doc /* **Source**: /home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml **Ref**: costing_constants.yaml:105 (eta_source_ecrh = 0.50) x steady_state_stellarator.yaml:15 (eta_couple = 1.0) = 0.50 **Basis**: gyrotron wall-plug x ECRH coupling */
        }
        :>> p_pump = 1.0 {    // primary coolant pumping power [MW].
            doc /* **Source**: /home/reid/1cfe/1costingfe/src/costingfe/data/defaults/steady_state_stellarator.yaml **Ref**: steady_state_stellarator.yaml:21 (p_pump = 1.0) **Basis**: 1costingFE stellarator primary-coolant pumping power */
        }
        :>> f_sub = 0.03 {    // subsystem/control power fraction.
            doc /* **Source**: /home/reid/1cfe/1costingfe/src/costingfe/data/defaults/steady_state_stellarator.yaml **Ref**: steady_state_stellarator.yaml:17 (f_sub = 0.03) **Basis**: 1costingFE stellarator subsystem power fraction */
        }
        :>> p_tf = 0.0 {      // coil electrical drive power [MW] — modeled zero for the SC coil set (WI-024).
            doc /*
            Coil electrical drive power: modeled 0.0. The Stellaris coil set is
            superconducting and operates steady-state DC — no resistive drive
            power; 1costingFE's own superconductor model agrees
            (recirc_power_factor = 0.0 for every SC conductor grade,
            defaults.py:611-614; the resistive recirc model is copper-only). The
            one printed steady-state electrical dissipation — ~7.5 kW
            resistive-joint losses, "negligible" (sec. 2.9) — is counted as heat
            at 20 K inside the WI-024 cryoplant chain (p_fixed_cryo below), not
            as coil electrical. Current-lead and power-supply standing losses
            are unprinted in any admissible source and are part of the chain's
            documented lower bound (f_uplift_cryo). (History: the pre-WI-023
            111.0 mapped a phantom "conduction power to coils" text row — the
            paper prints 111 only as stored magnetic energy [GJ]; WI-023 zeroed
            it as a deferral stopgap; WI-024 rescopes the zero from stopgap to
            modeled value.)
            **Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-02/sources/publikationen-1000179851-172386752/tmpissrtbos/raw.pdf
            **Ref**: sec. 2.9 (10 W per joint -> ~7.5 kW coil-set steady-state, "negligible"); /home/reid/1cfe/1costingfe/src/costingfe/defaults.py:611-614 (recirc_power_factor = 0.0 for superconductors)
            **Basis**: modeled zero for a superconducting coil set — coil-adjacent parasitic load carried by the derived p_cryo (WI-024 design D1/D2, 2026-07-18)
            */
        }
        :>> p_tfcool = 15.0 { // coil cooling power [MW].
            doc /*
            1costingFE stellarator cooling power, kept at the source default.
            Post-WI-024 coverage (MR-WI024-3): read as the non-cryogenic
            cooling-system electrical (component / room-temperature cooling
            loops), disjoint from the 20 K cryoplant wall-plug now derived into
            p_cryo — 1costingFE's own stellarator defaults carry p_cool = 15.0
            and p_cryo = 0.8 side by side (steady_state_stellarator.yaml:20,24),
            so in the source's intent they are distinct loads. The slot's
            upstream composition is undocumented; any cryo-compressor share it
            contains would overlap the derived p_cryo — a conservative-direction
            residual (recirc overstated, LCOE up), documented here rather than
            silently resolved.
            **Source**: /home/reid/1cfe/1costingfe/src/costingfe/data/defaults/steady_state_stellarator.yaml
            **Ref**: steady_state_stellarator.yaml:20 (p_cool = 15.0); :24 (p_cryo = 0.8 carried side by side — disjoint in the source's intent)
            **Basis**: 1costingFE stellarator cooling power; disjoint read vs the WI-024 derived cryoplant electrical (design D2, 2026-07-18)
            */
        }
        :>> p_trit = 10.0 {   // tritium systems power [MW].
            doc /* **Source**: /home/reid/1cfe/1costingfe/src/costingfe/data/defaults/steady_state_stellarator.yaml **Ref**: steady_state_stellarator.yaml:22 (p_trit = 10.0) **Basis**: 1costingFE stellarator tritium-processing power */
        }
        :>> p_house = 4.0 {   // housekeeping power [MW].
            doc /* **Source**: /home/reid/1cfe/1costingfe/src/costingfe/data/defaults/steady_state_stellarator.yaml **Ref**: steady_state_stellarator.yaml:23 (p_house = 4.0) **Basis**: 1costingFE stellarator housekeeping power */
        }
        :>> p_cryo = 0.0 {    // direct cryo-electrical term [MW] — zeroed; chain derives the slot (WI-024).
            doc /*
            The 1costingFE generic default 0.8 MW (steady_state_stellarator.yaml:24)
            is retired: it and the WI-024 derivation are the same physical quantity
            (cryoplant wall-plug electrical — 1cfe's own dipole defaults document
            the p_cryo slot as "Cryogenic wall-plug power"), so coexisting would
            double-count. The power-balance p_cryo slot now receives
            cryo_elec.p_elec, derived from the winding-pack heat load below.
            **Source**: /home/reid/1cfe/1costingfe/src/costingfe/data/defaults/steady_state_dipole.yaml
            **Ref**: steady_state_dipole.yaml:52-53 (slot semantics witness); steady_state_stellarator.yaml:24 (the retired generic default)
            **Basis**: double-counting resolution, WI-024 design D2 (2026-07-18)
            */
        }
        :>> q_nuc_cryo = 35.5 {   // winding-pack mean nuclear heating [W/m^3].
            doc /* **Source**: stellaris-design-details.md **Ref**: Table 6 image (images/page_020_table_0.png: "Mean cryogenic nuclear heating (winding pack) [W/m^3] 35.5"); sec. 2.8 raw.pdf (magnets at 20 K; EU DEMO ~50 W/m^3 as viability reference) **Basis**: Stellaris winding-pack volumetric nuclear heating at 20 K */
        }
        :>> vol_cold_cryo = 136.56 {  // total winding-pack volume [m^3] (COMPUTED).
            doc /*
            Computed from sourced geometry (WI-024 design D5): six unique square
            winding-pack cross-sections (Table 8 image side lengths 360/360/340/340/
            320/300 mm) x 8 occurrences each (sec. 2.9: 48 coils = 4 periods x
            (6 independent + 6 mirrored)) x 25 m typical circumference (sec. 2.9,
            printed but approximate — per-coil circumferences are not printed; the
            documented weak link). Sum of side^2 = 2x0.36^2 + 2x0.34^2 + 0.32^2
            + 0.30^2 = 0.6828 m^2; x8 x25 = 136.56 m^3. Cross-checks: each side^2
            equals turns x (20 mm)^2 exactly (sec. 2.9 unit cell; Table 8 turns
            row); Table 8 no-casing masses (128.7 t x 8 = 1029.6 t) imply
            ~7540 kg/m^3, consistent with the Table 7 material mix.
            **Source**: stellaris-design-details.md
            **Ref**: Table 8 image (images/page_022_table_0.png: side lengths, turns, masses); raw.pdf sec. 2.9 (square winding pack; 20 mm x 20 mm unit cell; 25 m typical circumference; 48 = 4 x (6+6) symmetry); Table 7 image (images/page_021_table_0.png: material fractions)
            **Basis**: cross-section x circumference x symmetry; mass cross-checked
            */
        }
        :>> p_fixed_cryo = 0.0075 {  // resistive-joint losses [MW] at 20 K.
            doc /* **Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-02/sources/publikationen-1000179851-172386752/tmpissrtbos/raw.pdf **Ref**: sec. 2.9 (10 W per joint -> ~7.5 kW steady-state for the entire coil set, "negligible ... within the cooling capacity of existing cryocooler designs") **Basis**: printed coil-set joint dissipation, counted as heat at 20 K */
        }
        :>> f_uplift_cryo = 1.0 {   // unprinted-loads multiplier — explicit lower bound (WI-024 D6).
            doc /*
            Bound 1.0 = printed loads only, a KNOWING LOWER BOUND: the paper defers
            casing, coil-case, and 20 K support-structure nuclear heating ("will be
            examined in future studies", sec. 2.9 raw.pdf), and current-lead /
            radiation loads are unprinted. No admissible uplift value exists; the
            parameter names the seam so the owner can raise it. Cited to the design
            ruling, not a source.
            **Source**: WI-024 design ruling (D6, 2026-07-18; sanctioned by spec Checkpoint Ruling 2)
            **Ref**: raw.pdf sec. 2.9 (the future-studies deferral)
            **Basis**: explicit assumption parameter — exclude-with-documented-bound
            */
        }
        :>> T_cold_cryo = 20.0 {    // coil operating temperature [K].
            doc /* **Source**: raw.pdf **Ref**: sec. 2.9 ("cooled to 20 K using supercritical helium at 15-20 bar"; Top set to 20 K); sec. 2.8; corroborated by 1costingFE defaults.py:611 (rebco_hts cryo_temp_k = 20.0) **Basis**: Stellaris HTS coil operating temperature */
        }
        :>> T_amb_cryo = 300.0 {    // heat-rejection reference temperature [K].
            doc /* **Source**: WI-024 design ruling (D4, 2026-07-18) **Ref**: standard ambient reference for the Carnot COP **Basis**: explicit assumption parameter (standard engineering reference) */
        }
        :>> f_carnot_cryo = 0.20 {  // fraction-of-Carnot plant efficiency — THE assumption (WI-024 D4).
            doc /*
            Explicit owner-visible assumption (spec Checkpoint Ruling 2 delegated
            value-setting to design; ruled 2026-07-18): no admissible source prints
            a 20 K COP or specific power (sec. 2.8 is qualitative; W7-X and the
            1costingFE dipole eta_cryo comment are value-inadmissible, shape only).
            Basis, general cryogenic engineering practice: large cryoplants achieve
            roughly 15-30% of Carnot; 0.20 taken at the conservative end. Yields
            COP = 0.20 x 20/280 = 1/70, i.e. 70 W_e per W at 20 K.
            **Source**: WI-024 design ruling (D4, 2026-07-18)
            **Ref**: spec sec. Evidence link A4 (the no-admissible-value finding)
            **Basis**: explicit assumption parameter — fraction of Carnot, general practice band
            */
        }

        // Stellarator family choices (inline; see the instance doc).
        // No separate PF coil set (3D modular coils only).
        :>> p_pf = 0.0 {
            doc /* **Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md **Ref**: line 249 (modular coils, minimized plasma current) **Basis**: stellarator has no separate poloidal-field coil set */
        }
        :>> p_pfcool = 0.0 {
            doc /* **Source**: stellaris-design-details.md **Ref**: line 249 (modular coils only) **Basis**: no PF coil set to cool */
        }
        // ECRH-only heating: no current drive.
        :>> p_nbi = 0.0 {
            doc /* **Source**: stellaris-design-details.md **Ref**: Table 2 line 237 (ECRD/ECRH heating only) **Basis**: QI stellarator, no NBI current drive */
        }
        :>> p_icrf = 0.0 {
            doc /* **Source**: stellaris-design-details.md **Ref**: Table 2 line 237 (ECRH only) **Basis**: QI stellarator, no ICRF */
        }
        :>> p_lhcd = 0.0 {
            doc /* **Source**: stellaris-design-details.md **Ref**: Table 2 line 237 (ECRH only) **Basis**: QI stellarator, no LHCD current drive */
        }
        :>> heating_nbi_per_mw = 0.0 {
            doc /* **Source**: stellaris-design-details.md **Ref**: Table 2 line 237 (ECRH only) **Basis**: no NBI installed (power = 0) */
        }
        :>> heating_icrf_per_mw = 0.0 {
            doc /* **Source**: stellaris-design-details.md **Ref**: Table 2 line 237 (ECRH only) **Basis**: no ICRF installed (power = 0) */
        }
        :>> heating_lhcd_per_mw = 0.0 {
            doc /* **Source**: stellaris-design-details.md **Ref**: Table 2 line 237 (ECRH only) **Basis**: no LHCD installed (power = 0) */
        }

        // Heating mix — ECRH only (nbi/icrf/lhcd zeroed above).
        :>> heating_ecrh_per_mw = 5282900.0 {  // ECRH capital [$/MW].
            doc /* **Source**: /home/reid/1cfe/1costingfe/src/costingfe/defaults.py **Ref**: defaults.py:98-100 (heating_ecrh_per_mw = 5.2829 M$/MW) x 1e6 **Basis**: gyrotron ECRH per-MW capital */
        }
        :>> p_ecrh = 50.0 {   // delivered ECRH power [MW].
            doc /* **Source**: stellaris-design-details.md **Ref**: Table 2 line 237 (ECRD/ECRH power = 50 MW) **Basis**: Stellaris ECRH installed power */
        }

        // Divertor (CAS22.1.8) driver.
        :>> divertor_base = 60000000.0 {  // divertor cost at 1 GWth [$].
            doc /* **Source**: /home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml **Ref**: costing_constants.yaml:97 (divertor_base = 60.0 M$) x 1e6 **Basis**: power-scaled divertor cost */
        }

        // CAS10 preconstruction — forward-computed (WI-025); CAS27 special
        // materials — forward-computed (WI-021).
        :>> precon_fixed_base = 32000000.0 {  // CAS10 fixed adders [$] (WI-025).
            doc /*
            32 M$ x 1e6 = site_permits 3 + licensing_cost_dt 5 (DT frozen) +
            plant_permits 2 + plant_studies_foak 20 (FOAK frozen) +
            plant_reports 1 + other_precon 1. preconstruction_capital now
            tracks the computed p_net via precon_cost (land ~
            sqrt(p_net x 1000 x 1)); bound pre-contingency (CAS29 applies
            once — convention preserved). Stale basis retired: the old
            $33.896M literal was computed at p_net = 575.3 (WI-018).
            **Source**: /home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml
            **Ref**: costing_constants.yaml:15-23; costs.py:52-80 (:79 contingency not carried)
            **Basis**: CAS10 fixed adders at the frozen DT/FOAK design point
            */
        }
        :>> special_materials_capital = rb.blanket_vol * 0.50 * 9400.0 * 5.0 {
            doc /*
            CAS27 initial PbLi blanket-fill inventory = blanket_vol x vol_frac x
            density x price = blanket_vol x 0.50 x 9400 x 5.0 [$] (the M$/1e6 and
            $-conversion x1e6 cancel). Forward-computed (WI-021): keyed to the
            radial-build blanket_vol (blanket.blanket_vol = rb.blanket_vol =
            1118.695 m^3), = 26.289 M$ -> $. Was an injected constant 26289000.0;
            the rebind makes it track the computed blanket volume (~26,289,332,
            a ~$332 refinement over the rounded constant, invisible at headline
            precision).
            **Source**: /home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml
            **Ref**: costing_constants.yaml:208 (pbli: density 9400, vol_frac 0.50, price 5.0); costs.py:182-202 (cas27_special_materials)
            **Basis**: volume-based PbLi inventory keyed to the blanket volume
            */
        }

        // Rollup rates (CAS29 contingency, CAS30 indirect, construction time).
        :>> contingency_rate = 0.10 {  // FOAK contingency on direct.
            doc /* **Source**: /home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml **Ref**: costing_constants.yaml:234 (contingency_rate_foak = 0.10) **Basis**: Gen-IV EMWG FOAK contingency */
        }
        :>> indirect_fraction = 0.20 {  // CAS30 indirect fraction of direct.
            doc /* **Source**: /home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml **Ref**: costing_constants.yaml:238 (indirect_fraction = 0.20) **Basis**: CAS30 indirect service fraction */
        }
        :>> construction_years = 8.0 {  // Yc [yr].
            doc /* **Source**: /home/reid/1cfe/1costingfe/src/costingfe/data/defaults/steady_state_stellarator.yaml **Ref**: steady_state_stellarator.yaml:46 (construction_time_yr = 8.0) **Basis**: 1costingFE stellarator construction time (complex 3D coils) */
        }

        // LCOE inputs (CAS70 O&M + financing).
        :>> om_annual_ref = 54900000.0 {  // CAS70 O&M at 1 GWe, DT [$/yr] (WI-025).
            doc /*
            om_cost_dt 54.9 M$/yr x 1e6. annual_om now tracks the computed
            p_net via om_cost (x sqrt(p_net/1000)); unlevelized — CAS71
            inflation and CAS72 scheduled replacement remain documented
            Stage-3 refinements (convention preserved). Stale basis retired:
            the old $41.641M/yr literal was computed at p_net = 575.3 (WI-018).
            **Source**: /home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml
            **Ref**: costing_constants.yaml:272; costs.py:319-357 (annual line :353)
            **Basis**: staffing-based DT O&M, power-law scaled, unlevelized
            */
        }
        :>> availability = 0.85 {      // capacity factor.
            doc /* **Source**: /home/reid/1cfe/1costingfe/src/costingfe/backcasting_bridge.py **Ref**: backcasting_bridge.py:48 (availability = 0.85) **Basis**: 1costingFE reference availability */
        }
        :>> discount_rate = 0.07 {     // discount / interest rate [1/yr].
            doc /* **Source**: /home/reid/1cfe/1costingfe/src/costingfe/adapter.py **Ref**: adapter.py:36 (interest_rate = 0.07); validation.py:92 **Basis**: 1costingFE reference interest rate */
        }
        :>> operational_years = 30.0 { // operating lifetime N [yr].
            doc /* **Source**: /home/reid/1cfe/1costingfe/src/costingfe/backcasting_bridge.py **Ref**: backcasting_bridge.py:49 (lifetime_yr = 30) **Basis**: 1costingFE reference plant lifetime */
        }

        // ---------------------------------------------------------------------
        // VIABILITY CONSTRAINTS (WI-018 additions: beta, wall load, TBR)
        // ---------------------------------------------------------------------

        // Beta.
        attribute beta : Real = 0.0276 {  // volume-averaged plasma beta.
            doc /* **Source**: stellaris-design-details.md / analyst-patch-spec-anchors.md **Ref**: analyst-patch-spec-anchors.md line 44 (beta = 0.0276, details.md 2.3) **Basis**: Stellaris vol-avg operating beta */
        }
        attribute beta_limit : Real = 0.05 {  // design/optimization beta target.
            doc /* **Source**: stellaris-design-details.md **Ref**: line 273 (coils + boundary optimized at <beta>_V = 5%) **Basis**: Stellaris design beta target */
        }

        // Neutron wall load (forward-computed from fusion power + first-wall area).
        // First-wall area [m^2] is the physically correct reference area (neutron
        // flux crosses the first wall, which stands off outboard of the plasma).
        // Forward-computed (WI-021) as rb.wall_area = kappa*4*pi^2*R*vacuum_or over
        // the first-wall standoff radius (vacuum_or = a + vacuum_t = 1.40 m at the
        // WI-022 a = 1.3), = 701.926 m^2 at the Stellaris build (R=12.7, kappa=1.0).
        // Bound directly into wall_load_calc (the `in V = geom.V` idiom) so it
        // forward-computes through codegen without a top-level derived-attribute
        // offender. 1costingFE torus geometry, no shape factor on material geometry
        // (owner Option 1, WI-021).
        // CROSS-CHECK: wall load = p_fus x (1 - 0.2002) / 701.926 ~= 3.13 MW/m^2
        // at the WI-022 profile-integrated p_fus ~= 2748 MW — above the printed
        // 2.87 avg (Table 5 image; the model's flat-wall average vs the source's
        // shaped-wall average) and below the 4.05 printed peak limit;
        // wall_load_ok passes.
        // Source: geometry.py _torus_surface_area / compute_geometry firstwall_area;
        //   stellaris-design-details.md Table 5 image (avg 2.87 MW/m^2).
        attribute wall_load_limit : Real = 4.05 {  // first-wall design limit [MW/m^2] (WI-022 corrected).
            doc /* **Source**: stellaris-design-details.md **Ref**: Table 2 image (images/page_002_table_0.png: peak neutron wall load 4.05 MW/m^2; the extracted text row "Table 5 ... 4.95" has no counterpart in the printed Table 5 image — extraction artifact) **Basis**: Stellaris first-wall peak neutron-load design value */
        }

        calc wall_load_calc : 'Neutron Wall Load' {
            in p_fus = fusion.p_fus;
            in wall_area = rb.wall_area;
        }

        // TBR.
        attribute tbr : Real = 1.074 {   // achieved tritium breeding ratio.
            doc /* **Source**: stellaris-design-details.md **Ref**: line 1659 (final TBR = 1.074) **Basis**: Stellaris 3D-neutronics TBR */
        }
        attribute tbr_floor : Real = 1.05 {  // self-sufficiency floor.
            doc /* **Source**: stellaris-design-details.md **Ref**: line 1530 (TBR > 1.05 self-sufficiency target) **Basis**: D-T tritium self-sufficiency floor */
        }

        // Asserted viability constraints — removed in this staged demo copy
        // (see mfe_plant.sysml DEMO NOTE): codegen strict-mode constraint
        // resolution aborts on plain design-attribute actuals. Stage-4 scope.
        // assert constraint beta_ok : 'Beta Limit' { in beta = beta; in beta_limit = beta_limit; }
        // assert constraint wall_load_ok : 'Neutron Wall Load Limit' { in wall_load = wall_load_calc.wall_load; in wall_load_limit = wall_load_limit; }
        // assert constraint tbr_ok : 'TBR Floor' { in tbr = tbr; in tbr_floor = tbr_floor; }

        // Exposed neutron wall load (headline physics output).
        attribute neutron_wall_load : Real = wall_load_calc.wall_load;
    }
}
