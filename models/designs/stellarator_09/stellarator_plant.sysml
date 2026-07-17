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
        evaluated at operating point A. The Stellaris design target is 2700 MW
        fusion; the 0D model computes ~2145 MW at the corrected plasma volume
        (see the sigma_v note — the gap is the 0D single-temperature limitation,
        item 2).

        STELLARATOR FAMILY CHOICES (applied inline, not concept-specific numbers):
          - Density is a direct input (no tokamak Greenwald closure) — already the
            generic plant's behaviour (n_e is a plain input to 'DT Fusion Power').
          - ECRH-only heating, no current drive: p_nbi = p_icrf = p_lhcd = 0 and
            their per-MW costs = 0 (QI stellarator is intrinsically steady-state).
          - No separate poloidal-field coil set: p_pf = 0, p_pfcool = 0 (3D
            modular coils only).
          - Stellarator coil geometry factor G = 8*pi^2 (vs tokamak 4*pi^2), bound
            on the magnet subsystem.

        HEADLINE FORWARD-PASS RESULT (WI-020 stellarator-correct geometry;
        executed cross-check in exploration/stellarator_e2e/run_stellaris.py):
        plasma volume 448 m^3 (shape factor 0.7943 on the torus 564), fusion
        power ~2145 MW (computed at the unchanged sigma_v — Decision A, no
        re-solve), gross electric 845 MW, net electric 578 MW, recirculating
        fraction 0.316, q_eng 3.16, total overnight capital ~$9.68B, LCOE
        ~$247/MWh (FOAK). Magnet-dominated (~$4.4B, 45.4% — power-independent,
        so unchanged) at the stellarator 5.87 REBCO markup.
        (History: WI-018 lossy balance net 575, ~$251/MWh; WI-019 faithful
        balance at torus volume net 786, ~$189/MWh; WI-020 corrects the volume,
        dropping fusion power ~20%, so net electric and LCOE land back near the
        WI-018 range — WI-019's power gain and this volume correction nearly
        cancel. The old 2700 MW / $189 headline is recoverable at sigma_v =
        7.535e-23, left as a visible input choice, not baked in.)

        THREE MAPPING TRAPS (documented at their bindings below): r_coil (coil
        bore = radial-build vessel outer radius, not a guess), sigma_v (D-T
        reactivity — Bosch-Hale can't run in SysML), and B (coil-cost field is the
        5.86 T loop-center value, NOT the 24.9 T peak-on-winding).

        **Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md
        **Ref**: Table 2 (line 227), Table 3 (line 283), Table 5 (line 720)
        **Basis**: Stellaris design point A + 1costingFE stellarator cost defaults
        */

        // ---------------------------------------------------------------------
        // MAGNET SUBSYSTEM (CAS22.1.3)
        // ---------------------------------------------------------------------
        part :>> magnet {
            doc /*
            Stellaris HTS modular-coil system.

            MAPPING TRAP (B vs b_center): the coil-cost field is the loop-center
            (on-axis) field 5.86 T, NOT the 24.9 T peak field on the winding pack.
            The ampere-meter conductor-quantity model uses the field at the loop
            center; the peak-on-winding is a conductor-grade concern, not a
            cost-quantity term.

            MAPPING TRAP (r_coil): the coil-bore radius = the radial-build vessel
            outer radius (vessel_or). From the stellarator radial build:
              vessel_or = a + vacuum_t + firstwall_t + blanket_t + reflector_t
                          + ht_shield_t + structure_t + gap1_t + vessel_t
                        = 1.5 + 0.10 + 0.05 + 0.80 + 0.20 + 0.20 + 0.15 + 0.10 + 0.10
                        = 3.20 m
            The blanket/shield/structure/vessel thicknesses are the 1costingFE
            stellarator defaults; the vacuum/firstwall/reflector/gap thicknesses
            are the RadialBuild dataclass defaults; a = 1.5 m is the Stellaris
            minor radius. Verified against costingfe.layers.geometry.
            compute_geometry(STELLARATOR): vessel_or = 3.2000 m.

            **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/geometry.py
            **Ref**: geometry.py:106-114 (vessel_or radial-build sum);
                steady_state_stellarator.yaml:39-42 (blanket/shield/structure/
                vessel thickness); stellaris-design-details.md line 228 (a=1.5 m);
                stellaris-design-details.md Table 3 line 289 (B_0 = 5.86 T)
            **Basis**: coil bore = radial-build vessel_or; on-axis field for cost
            */

            // G = 8*pi^2 stellarator geometry factor (family constant).
            // Source: costing_constants.yaml coil geometry (stellarator G=8pi^2);
            //   literal to stay in the codegen envelope (no redef expr drop).
            :>> G = 78.95683520871486;
            // On-axis (loop-center) field [T]. Source: stellaris-design-details.md
            //   Table 3 line 289 (B_0 = 5.86 T). NOT the 24.9 T peak-on-winding.
            :>> B = 5.86;
            // Major radius [m]. Source: stellaris-design-details.md Table 2 /
            //   line 251 (R ~= 12.7 m).
            :>> R0 = 12.7;
            // Coil-bore radius [m] = radial-build vessel_or. Forward-computed
            // (WI-021): the generic plant binds magnet.r_coil = rb.r_coil, so
            // r_coil = 3.20 m falls out of the radial build (was an injected
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
        // PASS-THROUGH DIRECT ACCOUNTS ($) — computed from the admissible
        // 1costingFE account functions at the Stellaris design-point powers
        // (documented initial-model pass-throughs; deepened in Stage 3).
        // ---------------------------------------------------------------------
        part :>> buildings {
            doc /*
            CAS21 buildings, raw (pre-contingency). Computed via costingfe.layers.
            costs.cas21_buildings for a DT stellarator (SC coil -> cryoplant
            building included) at p_et=896.8, p_the=896.8, p_th=2693.1,
            p_fus=2700, n_mod=1: 613.650 M$ -> $. The per-building fuel-keyed base
            costs + scaling bases are a dict loop (out of the codegen envelope),
            so the total is a pass-through here.
            STALE BASIS (surfaced at WI-019 close, updated WI-020): the 613.650
            M$ was computed at the pre-WI-019 powers (p_et=896.8, p_th=2693.1).
            The current WI-020 powers are p_et=845.2, p_th=2538.0 (fusion power
            fell to ~2145 MW when the volume was corrected). Recomputing this
            pass-through at the current powers belongs to the Stage-3
            pass-through-scope item, not WI-020. (Note: the WI-020 powers are
            closer to the 896.8 basis than the WI-019 powers were, so the drift
            is smaller than at WI-019 close.)
            **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py
            **Ref**: costs.py:83-144 (cas21_buildings); costing_constants.yaml:175-197
            **Basis**: CAS21 buildings total at the Stellaris design point
            */
            :>> capital_cost = 613650000.0;
        }

        // Physics geometry inputs.
        // PLASMA SHAPING (WI-020): the QI stellarator plasma is a shaped, twisted
        // column, not a smooth elongated torus. The torus term 2*pi^2*R*a^2*kappa
        // over-predicts its volume: at R=12.7, a=1.5, kappa=1.0 it gives 564 m^3,
        // but the Stellaris source tabulates 448 m^3 (Table 2 line 230). The
        // shape factor f_shape = 448/564 = 0.7943 (bound below) corrects it.
        // f_shape is an EMPIRICAL packing factor reconciling the model's geometry
        // inputs to the tabulated volume, NOT a first-principles shaping
        // coefficient: it bundles the ~16% physical QI shaping (448/533 at the
        // source's own Table-2 R=12) with the source's internal inconsistency
        // (Table 2 R=12 vs prose line 251 R~=12.7; a second tabulated volume
        // 425 m^3 appears in the Fig. 2 text, line 253). Owner ruled 2026-07-17
        // to target the Table-2 headline 448 m^3 at the model's R=12.7.
        // (Supersedes the pre-WI-020 note that mis-attributed the gap to "R/a
        // rounding" — arithmetically wrong: torus at R=12, a=1.5 = 533, not 448.)
        :>> R = 12.7 {        // major radius [m]. Source: details.md line 251.
            doc /* **Source**: stellaris-design-details.md **Ref**: line 251 (R ~= 12.7 m) **Basis**: Stellaris major radius */
        }
        :>> a = 1.5 {         // minor radius [m]. Source: details.md line 228.
            doc /* **Source**: stellaris-design-details.md **Ref**: Table 2 line 228 (a = 1.5 m) **Basis**: Stellaris minor radius */
        }
        :>> kappa = 1.0 {     // elongation. QI stellarator ~ circular average.
            doc /* **Source**: stellaris-design-details.md **Ref**: line 251 (near-circular avg cross-section); analyst-patch-spec-anchors.md line 30 (elon=1.0) **Basis**: stellarator ~circular average cross-section */
        }
        :>> f_shape = 0.794259 {  // stellarator shape/packing factor [1].
            doc /* **Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md **Ref**: Table 2 line 230 (plasma volume = 448 m^3) **Basis**: empirical shape factor = tabulated V (448) / elongated-torus V (564.05) at R=12.7, a=1.5, kappa=1.0; corrects the smooth-torus over-prediction of the shaped QI plasma volume */
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
        :>> n_e = 3.37e20 {   // vol-avg electron density [m^-3], point A.
            doc /* **Source**: stellaris-design-details.md **Ref**: Table 5 line 731 (vol-avg n_e = 3.37e20 m^-3, point A) **Basis**: Stellaris operating point A */
        }
        :>> sigma_v = 5.985e-23 {  // D-T reactivity <sigma*v> [m^3/s].
            doc /*
            MAPPING TRAP (sigma_v): Bosch-Hale reactivity cannot run in SysML
            (needs exp()). This is the 1costingFE Bosch-Hale D-T reactivity
            (costingfe.layers.reactivity.sigv_dt) at an effective 0D temperature
            T_eff ~= 7.9 keV — a genuine point on the sigv_dt curve, NOT a value
            back-solved to a target power.

            FUSION POWER IS A COMPUTED OUTPUT (WI-020, owner Decision A: do not
            re-solve sigma_v). At the stellarator-corrected volume 448 m^3 (the
            f_shape factor above) and the volume-averaged density n_e = 3.37e20,
            this reactivity yields p_fus ~= 2145 MW — BELOW the Stellaris 2700 MW
            design point (Table 5 line 742). The gap is the honest 0D
            single-temperature limitation: the real (peaked) n and T profiles
            concentrate fusion in the hot core, so a single volume-averaged
            (density, temperature) pair under-predicts the profile-integrated
            power. Closing that gap is item 2 (predictive confinement); it is
            left VISIBLE here, not papered over with a back-solve.

            (Pre-WI-020, sigma_v was justified as the value that reproduced
            2700 MW at the torus volume 564 m^3. That back-solve is removed: the
            volume is now correct at 448, sigma_v is a plain physical input, and
            fusion power falls out. Various sigma_v / effective-temperature
            inputs can be swept at the codegen execution phase.)

            Why not the peak temperature: sigv_dt at the peak ion temperature
            T_i0 = 24.6 keV is 5.56e-22 m^3/s (~9x larger); pairing it with the
            volume-averaged density would grossly overestimate fusion power
            (~20 GW). The single-temperature reactivity consistent with the
            volume-averaged density is far below the peak value.

            **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/reactivity.py
            **Ref**: reactivity.py:54-70 (sigv_dt Bosch-Hale D-T, the curve this
                T_eff ~= 7.9 keV point lies on); stellaris-design-details.md
                Table 5 line 742 (P_fus = 2700 MW design point, now shown unmet
                by the 0D model), line 738-739 (peak T_e0/T_i0 = 15.4/24.6 keV)
            **Basis**: unchanged 0D-effective D-T reactivity; fusion power is
                computed at the corrected volume, and the design-point gap is
                left visible for item 2
            */
        }
        :>> E_fus = 2.817e-12 {  // per-event D-T fusion energy [J].
            doc /* **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/physics.py **Ref**: physics.py:31 (Q_DT = 17.58 MeV x 1.602176634e-13 J/MeV = 2.817e-12 J) **Basis**: D-T fusion Q-value */
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
        :>> p_tf = 111.0 {    // coil power [MW] (conduction power to coils).
            doc /*
            Coil-system recirculating power, mapped from the Stellaris "conduction
            power to coils" (111 MW). For SC modular coils this is the cold-mass
            heat load driving the coil/cryo recirculating power; the spec directs
            it to the p_tf coil-power slot (p_pf = 0, no PF coils). A finer
            cold-mass -> cryo-electrical (COP) treatment is a Stage-3 item.
            **Source**: stellaris-design-details.md **Ref**: Table 2 line 235 (conduction power to coils = 111 MW) **Basis**: Stellaris coil-system recirculating power
            */
        }
        :>> p_tfcool = 15.0 { // coil cooling power [MW].
            doc /* **Source**: /home/reid/1cfe/1costingfe/src/costingfe/data/defaults/steady_state_stellarator.yaml **Ref**: steady_state_stellarator.yaml:20 (p_cool = 15.0) **Basis**: 1costingFE stellarator cooling power */
        }
        :>> p_trit = 10.0 {   // tritium systems power [MW].
            doc /* **Source**: /home/reid/1cfe/1costingfe/src/costingfe/data/defaults/steady_state_stellarator.yaml **Ref**: steady_state_stellarator.yaml:22 (p_trit = 10.0) **Basis**: 1costingFE stellarator tritium-processing power */
        }
        :>> p_house = 4.0 {   // housekeeping power [MW].
            doc /* **Source**: /home/reid/1cfe/1costingfe/src/costingfe/data/defaults/steady_state_stellarator.yaml **Ref**: steady_state_stellarator.yaml:23 (p_house = 4.0) **Basis**: 1costingFE stellarator housekeeping power */
        }
        :>> p_cryo = 0.8 {    // cryogenic pumping power [MW].
            doc /* **Source**: /home/reid/1cfe/1costingfe/src/costingfe/data/defaults/steady_state_stellarator.yaml **Ref**: steady_state_stellarator.yaml:24 (p_cryo = 0.8) **Basis**: 1costingFE stellarator cryogenic power */
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

        // Pass-through capitals (CAS10 preconstruction, CAS27 special materials).
        :>> preconstruction_capital = 33896000.0 {
            doc /*
            CAS10 preconstruction subtotal (land + permits + licensing + FOAK
            studies + reports + other), pre-contingency, at P_net = 575.3 MW:
            33.896 M$ -> $. Computed via the costing_constants land/permit/
            licensing constants (land scales as sqrt(P_net x ref)). Supplied
            without CAS10's own contingency to avoid double-counting the plant's
            CAS29 contingency.
            STALE BASIS (surfaced at WI-019 close, updated WI-020): P_net = 575.3
            was the WI-018 value. WI-019 moved it to 786.1; WI-020 (volume
            correction, fusion power ~2145 MW) brings it back to 578.0 — nearly
            the 575.3 basis this pass-through was computed at, so it is now
            almost on-basis again. Recomputation still belongs to the Stage-3
            pass-through-scope item, not WI-020.
            **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py
            **Ref**: costs.py:52-80 (cas10_preconstruction); costing_constants.yaml:15-30
            **Basis**: CAS10 preconstruction subtotal at the Stellaris design point
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
        :>> annual_om = 41641000.0 {   // annual O&M [$/yr].
            doc /*
            CAS70 O&M = om_cost_dt x (P_net/1 GWe)^0.5 = 54.9 x (575.3/1000)^0.5 =
            41.641 M$/yr -> $. Inflation and scheduled-replacement (CAS72)
            refinements are a Stage-3 item.
            STALE BASIS (surfaced at WI-019 close, updated WI-020): P_net = 575.3
            was the WI-018 value. WI-019 moved it to 786.1; WI-020 (volume
            correction, fusion power ~2145 MW) brings it back to 578.0 — nearly
            the 575.3 basis this pass-through was computed at, so it is now
            almost on-basis again. Recomputation still belongs to the Stage-3
            pass-through-scope item, not WI-020.
            **Source**: /home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml
            **Ref**: costing_constants.yaml:272 (om_cost_dt = 54.9 M$/yr at 1 GWe); costs.py:319-347 (power-law 0.5)
            **Basis**: staffing-based DT O&M, power-law scaled
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
        // the first-wall standoff radius (vacuum_or = a + vacuum_t = 1.60 m),
        // = 802.201 m^2 at the Stellaris build (R=12.7, a=1.5, kappa=1.0). Bound
        // directly into wall_load_calc (the `in V = geom.V` idiom) so it forward-
        // computes through codegen without a top-level derived-attribute offender.
        // 1costingFE torus geometry, no shape factor on material geometry (owner
        // Option 1, WI-021). Was an injected constant 802.201.
        // CROSS-CHECK: wall load = p_fus x (1 - 0.2002) / 802.201 ~= 2.14 MW/m^2
        // at the WI-020 p_fus ~= 2145 MW — below the Stellaris 2.87 avg (line 747)
        // and the 4.95 peak limit; wall_load_ok passes. The gap to 2.87 tracks the
        // 0D fusion-power under-prediction (2145 vs 2700; item 2). (The earlier
        // plasma-surface-area basis, 327 m^2, was the wrong area; corrected.)
        // Source: geometry.py _torus_surface_area / compute_geometry firstwall_area;
        //   stellaris-design-details.md Table 5 line 747 (avg 2.87 MW/m^2).
        attribute wall_load_limit : Real = 4.95 {  // first-wall design limit [MW/m^2].
            doc /* **Source**: stellaris-design-details.md **Ref**: Table 5 line 748 (peak neutron wall power 4.95 MW/m^2) **Basis**: Stellaris first-wall design neutron-load limit */
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

        // Asserted viability constraints.
        assert constraint beta_ok : 'Beta Limit' {
            in beta = beta;
            in beta_limit = beta_limit;
        }
        assert constraint wall_load_ok : 'Neutron Wall Load Limit' {
            in wall_load = wall_load_calc.wall_load;
            in wall_load_limit = wall_load_limit;
        }
        assert constraint tbr_ok : 'TBR Floor' {
            in tbr = tbr;
            in tbr_floor = tbr_floor;
        }

        // Exposed neutron wall load (headline physics output).
        attribute neutron_wall_load : Real = wall_load_calc.wall_load;
    }
}
