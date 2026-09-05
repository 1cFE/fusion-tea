package stellarator_09 {
    private import ScalarValues::*;
    private import mfe_plant::*;
    private import mfe_plasma_scaling::*;
    private import mfe_viability::*;

    // =========================================================================
    // CONCRETE INSTANCE -- concept-09 Proxima "Stellaris" QI stellarator
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
    // intermediate abstract def -- a `part x : 'Stellarator Plant'` reports
    // types ['Stellarator Plant', 'Part', ...] and never 'MFE Power Plant', so
    // the two-level chain leaves 'MFE Power Plant' flagged NO_INSTANTIATION
    // (its template calcs would be dropped at extraction). Typing the instance
    // directly on 'MFE Power Plant' (the hif_plant idiom) clears the flag. The
    // stellarator family choices (density-direct, ECRH-only/no current drive, no
    // separate PF coils, G = 8*pi^2) are applied inline and marked below.
    // =========================================================================

    part stellaris : 'MFE Power Plant' {
        doc /*
        Proxima Fusion "Stellaris" -- concept-09 QI stellarator HTS power plant,
        evaluated at operating point A. The Stellaris design point is 2700 MW
        fusion; the model computes 2748 MW (+1.8%) by integrating the
        Bosch-Hale reactivity over the source's own profiles (WI-022 -- every
        profile parameter fixed from the source's figure and printed tables,
        blind to the power; see the sigma_v note).

        STELLARATOR FAMILY CHOICES (applied inline, not concept-specific numbers):
          - Density is a direct input (no tokamak Greenwald closure) -- already the
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
        printed 9.0 T -- 5.86 was a phantom text row -- and zeroed the phantom
        p_tf = 111, which the paper prints only as stored magnetic energy in
        GJ, not a power, net 915.145, ~$201.46/MWh; WI-024 derived the cryo
        parasitic load from the winding-pack heat inventory, retired the
        0.8 MW 1costingFE default, and rescoped p_tf to a modeled zero,
        ~$201.47/MWh; WI-025 forward-computed the last three pass-through
        cost accounts -- CAS21 buildings, CAS10 preconstruction, CAS70 annual
        O&M -- from the model's computed powers, retiring the final STALE
        BASIS annotations, total $12.60B -> $12.64B, ~$203.65/MWh.)

        THREE MAPPING TRAPS (documented at their bindings below): r_coil (coil
        bore = radial-build vessel outer radius, not a guess), sigma_v (0D
        bypass input -- sigma_v = 0 here selects the profile-integrated
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
            table image and from the published paper -- raw.pdf-confirmed, WI-023.)

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
            // Axis-averaged field [T]: COMPUTED (WI-035, inversion ruling
            // 2026-08-30). The held ':>> B = 9.0' is retired; the generic plant
            // EXPOSEs field_calc.B_axis into magnet.B from the coil-set current
            // below. The printed 9.0 T (Table 2 image page_002_table_0.png;
            // Table 5 image page_009_table_0.png Points A/B) remains the
            // cross-check: computed B_axis = 9.0 T minus one ulp
            // (8.999999999999998), low side bound so peak_field_ok cannot
            // flip on rounding (WI-035 design D2).
            // Major radius [m]. Source: stellaris-design-details.md Table 2 /
            //   line 251 (R ~= 12.7 m).
            :>> R0 = 12.7;
            // Coil-bore radius [m] = radial-build vessel_or. Forward-computed
            // (WI-021): the generic plant binds magnet.r_coil = rb.r_coil, so
            // r_coil = 3.00 m falls out of the radial build (was an injected
            // constant here).
            // REBCO HTS conductor [$/kA-m]. Source: costing_constants.yaml:57
            //   (conductor_cost_rebco = 50.0). NOT x1e6 -- already $/kA-m; the
            //   magnet formula omits the /1e6 M$ conversion and yields $.
            :>> cost_per_kAm = 50.0;
            // Stellarator conductor->installed markup. Source: costing_constants.
            //   yaml:75 (coil_markup.stellarator = 5.87).
            :>> coil_markup = 5.87;
            // Peak-on-winding / axis-averaged field ratio [1] = 24.9 / 9.0 written
            // as its IEEE-754 double so that 9.0 * peak_ratio == 24.9 exactly and
            // peak_field_ok reads margin 0.0 at the design point (2.7667 would
            // read 24.9003, violated). A redefinition expression is dropped by the
            // pinned codegen, hence the literal (WI-030).
            :>> peak_ratio = 2.7666666666666666 {
                doc /* **Source**: stellaris-design-details.md **Ref**: Table 2 image (images/page_002_table_0.png: peak conductor magnetic field strength 24.9 T; axis av. magnetic field strength 9.0 T) **Basis**: Stellaris coil-set peak/axis field ratio, 24.9/9.0 */
            }
            // Conductor peak-field ceiling [T]. [OWNER 2026-08-21]: the field
            // Stellaris designs to (Table 2), not 1costingFE's REBCO engineering
            // ceiling of 23.0 T (defaults.py:611), which the Stellaris winding
            // exceeds by 1.9 T; the disagreement is disclosed, the design value
            // is bound (WI-030).
            :>> B_max = 24.9 {
                doc /* **Source**: stellaris-design-details.md; /home/reid/1cfe/1costingfe/src/costingfe/defaults.py (pin 0254385) **Ref**: Table 2 image (images/page_002_table_0.png: peak conductor magnetic field strength 24.9 T); defaults.py:605-612 (MAGNET_TABLE rebco_hts b_max = 23.0, not bound -- owner ruling 2026-08-21) **Basis**: Stellaris REBCO design peak field; the HTS arm's ceiling for the Item 6 A/B */
            }

            // ----------------- WI-035 coil-set current, limit, cost -----------------
            // Number of toroidal field coils [1].
            :>> n_coils = 48.0 {
                doc /* **Source**: stellaris-design-details.md **Ref**: Table 2 image (images/page_002_table_0.png: "Number of toroidal field coils [1] 48"); raw.pdf sec. 2.9 (48 = 4 periods x (6 independent + 6 mirrored)) **Basis**: Stellaris coil count */
            }
            // Peak single-coil current [A].
            :>> I_coil = 15400000.0 {
                doc /* **Source**: stellaris-design-details.md **Ref**: Table 2 image (images/page_002_table_0.png: "Peak coil current (single coil) [MA] 15.4"); Table 8 image (images/page_022_table_0.png: coil 0, I = 15.4 MA) **Basis**: Stellaris peak coil current -- the WI-035 design lever */
            }
            // Coil-set transfer fact [1], float64 of the printed set: (2*pi*R0*B/mu0)/(n_coils*I_coil)
            // = 571.4999996889 MA / 739.2 MA at (9.0 T, 12.7 m, 48, 15.4 MA). Decomposes as
            // set-distribution 643.2/739.2 = 0.870 (Table 8) x axis-linkage 571.5/643.2 = 0.888
            // (the modular-coil shaping current that does not link the axis, WI-032). No float64
            // value reproduces 9.0 T exactly; this one gives 9.0 minus one ulp (low side, WI-035 D2).
            :>> k_link = 0.7731331164622419 {
                doc /* **Source**: stellaris-design-details.md; work/completed/20260827_WI-032_cold-volume-basis/spec.md **Ref**: Table 2 image (page_002_table_0.png: 9.0 T, 15.4 MA, 48 coils, R 12.7 m); Table 8 image (page_022_table_0.png: per-coil ampere-turns 15.4/14.6/13.8/12.9/12.5/11.2 MA x 8) **Basis**: coil-set geometry fact from the printed pair (peak_ratio convention, WI-030) */
            }
            // Set-mean over peak coil current [1] = (8 x 80.4 MA)/(48 x 15.4 MA) = 643.2/739.2.
            :>> f_set = 0.8701298701298701 {
                doc /* **Source**: stellaris-design-details.md **Ref**: Table 8 image (images/page_022_table_0.png: per-coil ampere-turns, image-verified -- the iter-01 text table misprints coils 1 and 4) **Basis**: Stellaris coil-set current distribution */
            }
            // Coil-shape factor [1] = typical circumference / major radius
            // = 25.0 / 12.7 as its IEEE-754 double, so c_coil reproduces the
            // printed 25 m exactly at R0 = 12.7 m. WI-036 D3: winding length
            // now responds to machine scale; the SHAPE stays held because
            // per-coil circumferences are unprinted. This is the residual held
            // quantity the WI-036 mint record predicted -- "one held constant
            // traded for a smaller one" -- and it is named here, not buried.
            // c_coil itself is computed (mfe_plant.sysml, coil_length calc).
            :>> k_coil = 1.9685039370078741 {
                doc /* **Source**: stellaris-design-details.md **Ref**: raw.pdf sec. 2.9 ("typical circumference of 25 m"; coils approximately 7 x 5 x 10 m); images/page_002_table_0.png (Table 2: major radius 12.7 m) **Basis**: coil circumference over major radius at the printed pair (25.0 / 12.7); the printed circumference is "typical but approximate", the same weak link the pre-WI-036 held value carried */
            }
            // Winding-pack current density [A/mm^2], worst coil (coil 0).
            // Bound as the float64 of the printed pair (15.4 MA, 360 mm) so
            // that wp_side reproduces 0.360000 m exactly; the printed j_WP is
            // 119 A/mm^2 (Table 8), and the design range across the six unique
            // coils is 112-124. WI-036 D1: this is the sizing LEVER that
            // replaced the held wp_side -- the pack is now sized by the current
            // it carries, so stress grows as sqrt(I_coil * j_wp) rather than
            // linearly in current, and a wider pack costs cold mass through
            // the cryo chain. wp_side itself is computed (mfe_plant.sysml).
            :>> j_wp = 118.8271604938272 {
                doc /* **Source**: stellaris-design-details.md **Ref**: Table 8 image (images/page_022_table_0.png, image-verified -- the markdown extraction of this table is garbled: j_WP 119/112/120/112/122/124 A/mm^2; I total amp-turns 15.4/14.6/13.8/12.9/12.5/11.2 MA; cross-section side 360/360/340/340/320/300 mm, coil 0 the highest-force coil at 174 MN/m) **Basis**: Stellaris worst-coil winding-pack current density; the relation I = j_wp * side^2 closes across all six unique coils to better than 1% (-0.58% .. +0.52%) */
            }
            // Winding-pack set-distribution factor [1] = printed total winding-pack
            // volume over the worst-coil-uniform reference = 136.56 / (48 * 0.36^2 * 25)
            // = 136.56 / 155.52. WI-036 D2: the model carries one winding pack while
            // the machine has six unique cross-sections; this is the same shape as the
            // f_set coil-current distribution fact, and it moves the six-cross-section
            // arithmetic out of a doc comment and into model content.
            :>> f_wp_vol = 0.8780864197530865 {
                doc /* **Source**: stellaris-design-details.md **Ref**: Table 8 image (images/page_022_table_0.png: cross-section side lengths 360/360/340/340/320/300 mm, image-verified); raw.pdf sec. 2.9 (48 coils = 4 periods x 12, so 8 occurrences of each of six unique coils; typical circumference 25 m) **Basis**: sum over the six unique coils of side^2 x 8 x 25 m = 136.56 m^3, expressed as a distribution factor on the worst coil */
            }
            // Stress concentration fact [1] = float64 of sigma_anchor*wp_side/(I_coil*B_peak)
            // at the printed worst-coil pair (650e6 Pa x 0.36 m)/(15.4e6 A x 24.9 T); the
            // printed "<650" bound taken AS the value (conservative). Roundtrip: exactly 650 MPa.
            :>> k_sigma = 0.6102331403536223 {
                doc /* **Source**: stellaris-design-details.md **Ref**: Table 8 image (images/page_022_table_0.png: "Peak stress on WP [MPa] <650"); raw.pdf sec. 2.9 structural analysis (peak ~600 MPa) **Basis**: coil-set structural fact from the printed pair (peak_ratio convention) */
            }
            // Structural allowable stress [Pa].
            :>> sigma_allow = 800000000.0 {
                doc /* **Source**: stellaris-design-details.md **Ref**: raw.pdf sec. 2.10 ("design limit of 800 MPa for cryogenic AISI 316LN", Fig. 49; von Mises as membrane+bending proxy, ASME BPVC VIII-2 / Eurocode framing; yield ~1000 MPa at 20-30 K) **Basis**: Stellaris support-structure design stress limit */
            }
            // ---- WI-036 conductor check: the SECOND of the two checks ----
            // Winding-pack effective elastic modulus [Pa]. Cryogenic AISI 316LN,
            // the load-bearing constituent of the pack (radial plates and casing).
            :>> E_wp = 200000000000.0 {
                doc /* **Source**: stellaris-design-details.md **Ref**: raw.pdf sec. 2.10 (AISI 316LN chosen as the support-structure material; yield ~1000 MPa at the 20-30 K operating range) **Basis**: austenitic stainless elastic modulus at cryogenic temperature, the pack's load-bearing constituent */
            }
            // Conductor load-sharing factor [1] = HTS stack strain over
            // pack-average strain, from the source's own reported pair:
            // 0.002 / (600e6 / 200e9) = 2/3. The tape stack sees less strain
            // than the pack average because the soldered Cu jacket offloads it.
            // Both anchors are printed BOUNDS taken as values ("<0.2%", and the
            // paired k_sigma anchor is "<650"), so the operand OVER-estimates
            // strain -- conservative, disclosed, and not corrected, because
            // correcting it needs numbers the source does not print. This is a
            // composition standing in for an FE result, calibrated from the
            // source's own numbers rather than assumed (the k_sigma convention).
            :>> f_cond = 0.6666666666666666 {
                doc /* **Source**: stellaris-design-details.md **Ref**: raw.pdf p. 24 (winding-pack peak von Mises "in the range of 600 MPa"; "The peak strain on the HTS stack due to the deformation of the winding pack is below 0.2%, which is within acceptable limits, even when adding strain from bending") **Basis**: stack strain over pack-average strain at the printed pair, both figures taken at their printed bounds */
            }
            // Conductor strain limit [1]. 0.4% -- the strain below which the
            // registered measurements report no discernible effect on any of
            // five commercial tapes. SETTABLE and deliberately so: the band
            // practitioners enforce spans 0.2% to 0.4%, and SuperOx (the tape
            // this design specifies) is the WEAKEST of the five measured, with
            // its irreversible limit at 0.45-0.47%. At this limit the structure
            // binds first (the operand reads 0.217% at the design point and
            // 0.267% at the 800 MPa stress fence, binding at 1200 MPa); at a
            // 0.2% choice the conductor would bind first.
            :>> eps_cond_allow = 0.004 {
                doc /* **Source**: knowledge/sources/electro_mechanical_properties_of_rebco_coated_conductors/ **Ref**: output.md:197 ("Remaining below 0.4% strain, there are no discernible differences in the samples' strain dependencies"; irreversible stress limits 740-840 MPa at 4.2 K/19 T); output.md:173 (irreversible strain at 4.2 K/19 T: Bruker 0.70-0.72%, SuNAM 0.67-0.69%, SuperPower 0.66-0.68%, Fujikura 0.55-0.57%, SuperOx 0.45-0.47%; Fujikura and SuperOx fully de-laminate, "indicating an interfacial weakness") **Basis**: axial irreversible strain limit for commercial REBCO coated conductor, taken at the no-discernible-effect bound; measured at 4.2 K and 77 K, which the source states bracket identically -- the 20 K operating point is bracketed, not measured (the one source measuring through 20 K, Pierro et al. 2019, is paywalled and recorded as a queued research gap) */
            }
            // Winding fabrication markup [1] = 3.5 (winding/insulation/cooling/jointing/test)
            // x 1.9 (documented NCSX non-planar production penalty). Content-mapped: no casing,
            // cryostat, or quench content (casings are the account below; NI quench protection
            // is passive, printed sec. 2.9).
            :>> f_wp_fab = 6.65 {
                doc /* **Source**: /home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml (pin 0254385) **Ref**: costing_constants.yaml:50 (coil_cu_fab_markup 3.5, content list); :60-72 (stellarator 5.87 = 3.09 x 1.9 NCSX overrun; winding path handled separately) **Basis**: content-mapped fabrication build-up on the conductor base (WI-035 D4) */
            }
            // Casing steel mass per coil [kg]: the PRINTED FLOOR of the sec. 2.10 cast-part
            // range (63-200 t) -- a KNOWING LOWER BOUND (f_uplift_cryo pattern): no total is
            // printed, so the lightest cast part per casing bounds from below; band
            // [$54.4M, $172.8M] disclosed in WI-035 design D5. The parameter names the seam.
            :>> m_casing = 63000.0 {
                doc /* **Source**: stellaris-design-details.md; WI-035 design ruling D5 (2026-08-30) **Ref**: raw.pdf sec. 2.10 ("cast with parts weighing between 63 tons and 200 tons") **Basis**: explicit lower-bound assumption parameter -- printed floor, seam named */
            }
            // Fabricated structural steel price [$/kg].
            :>> steel_price = 6.0 {
                doc /* **Source**: /home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml (pin 0254385) **Ref**: costing_constants.yaml:52 (coil_steel_price_per_kg = 6.0) **Basis**: fabricated structural steel rate at the pin */
            }
            // Casing fabrication markup [1].
            :>> f_steel_fab = 3.0 {
                doc /* **Source**: /home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml (pin 0254385) **Ref**: costing_constants.yaml:53 (coil_steel_fab_markup = 3.0, "coil-case / inter-coil support fabrication") **Basis**: coil-case fabrication build-up at the pin */
            }
        }

        // ---------------------------------------------------------------------
        // SHARED POWER-CORE SUBSYSTEMS (CAS22.1.x) -- cost drivers ($, volumes m^3)
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
        // BALANCE OF PLANT (CAS23-26) -- per-MW rates ($/MW), Rankine steam cycle
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
        // CAS21 BUILDINGS ($) -- forward-computed (WI-025): buildings_cost tracks
        // the model's p_fus/p_the/p_th/p_et (p_the = p_et, no DEC -- costs.py:104).
        // The six base sums below are the exact grouped collapse of the
        // 18-building DT column (every building linear in exactly one scaling
        // basis), cryogenics included (SC coils, REBCO HTS -- costs.py:137);
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
            scales as p_the x n_mod / 1100 (costs.py:104,124 -- p_the = p_et,
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
            alpha_n/alpha_T referents below) -- the model's realization of the
            source's 0.5D volume-integrated power balance (Appendix A). The
            reactivity physics executes at the handwritten codegen stage
            (Rung B, owner-ratified) and is guarded bit-exact by the oracle.

            This closes the former "0D gap": pre-WI-022 the injected
            0D-effective reactivity (5.985e-23 at T_eff ~= 7.9 keV) gave
            ~2145 MW vs the 2700 MW design point, the visible 0D
            single-temperature limitation. The profile integral computes
            ~2748 MW at the printed volume 425 m^3 -- within ~2% of the design
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
        // densities -- quasineutrality closes at the peak: 2x1.96 (fuel) +
        // 2x0.56 (He ash) ~= 5.06 = printed peak n_e.
        // WI-037 retirement note: the held fuel peaks n_D0 = n_T0 = 1.96e20
        // (Table 5 image, Point A) retire as entry points -- the sustainment
        // chain computes them by quasi-neutrality with the converged A.5/A.6
        // ash (computed 1.945e20 at this lever point, -0.8% vs the retired
        // referents; the printed pair remains the cross-check, not an input).
        :>> T_i0 = 14.63 {    // peak ion temperature [keV] (operating-point lever).
            doc /* **Source**: stellaris-design-details.md **Ref**: Table 5 image (images/page_009_table_0.png: peak ion temperature 14.63 keV, Point A; the extracted text "24.60" is an extraction artifact) **Basis**: Stellaris Point-A peak ion temperature */
        }
        :>> alpha_n = 0.33 {  // fuel density profile exponent [1].
            doc /* **Source**: stellaris-design-details.md Fig. 16 density panel **Ref**: images/stellaris-high-field-quasi-isodynamic-stellarator.pdf-9-0.png, digitized fit (prototype/digitize_fig16.py; D and T curves, rms log-residual 0.006) **Basis**: n(rho) = n0*(1-rho^2)^alpha_n (Eq. 3, image-verified) fuel-profile exponent, fixed blind to the fusion power */
        }
        :>> alpha_T = 1.19 {  // temperature profile exponent [1].
            doc /* **Source**: stellaris-design-details.md Fig. 16 temperature panel **Ref**: images/stellaris-high-field-quasi-isodynamic-stellarator.pdf-9-1.png, digitized fit (prototype/digitize_fig16.py; all three species, rms log-residual 0.02); corroborated by a/L_T ~= 2.25 at rho=0.6 (line 714) and the rho=0.8 Dirichlet values 4.2/5.2 keV (line 762) **Basis**: T(rho) = T0*(1-rho^2)^alpha_T (Eq. 2, image-verified) exponent, fixed blind to the fusion power */
        }

        // Beta and density referents (WI-030; WI-042). The peak electron
        // density is the operating-point lever, from the Table 5 image. The
        // electron density profile is DERIVED (WI-042): the ash follows the
        // fusion-rate profile (Eq. A.5 pointwise) and the electrons close by
        // quasi-neutrality, so the point-A exponent 0.596 that WI-030 bound
        // from the printed vol-av/peak pair (3.17e20 / 5.06e20, Table 5 image:
        // <n>/n0 = 1/(1+alpha) for a power law) retires as an entry point and
        // becomes the cross-check: the derived profile gives
        // sustain.alpha_n_e_eff = 0.5953 and sustain.n_e_volav = 3.172e20 at
        // this lever point (SV row, WI-042). The computed beta (beta_calc)
        // reads the same volume-averaged pressure as W_th and is 0.02531 at
        // this point against the printed 2.76 % -- thermal, fast-particle
        // pressure excluded; and the printed 2.76 % is inconsistent with the
        // printed 504.65 MJ at the only field the paper names (goal
        // stored-energy-basis L-002), so the pair is a cross-check with a
        // stated caveat, not a target. Quasineutrality at the peak:
        // 2 x 1.96 + 2 x 0.56 = 5.04 ~= 5.06.
        :>> n_e0 = 5.06e20 {  // peak electron density [m^-3].
            doc /* **Source**: stellaris-design-details.md **Ref**: Table 5 image (images/page_009_table_0.png: peak el. density 5.06e20 m^-3, Point A; the extracted text "4.55" is an extraction artifact) **Basis**: Stellaris Point-A peak electron density */
        }
        // WI-037 retirement note: the held T_e0 = 15.40 keV and n_He0 =
        // 0.56e20 (Table 5 image, Point A) retire as entry points -- T_e0 is
        // computed from the T_i0 lever through the held 0.95 ratio (ratio-exact
        // at this point) and n_He0 from the converged A.5/A.6 ash balance
        // (computed 5.80e19 at WI-037; 6.04e19 after WI-042, +8% vs the
        // retired referent, because tau_E rises 7% at the lower W; goal
        // evidence work/orchestration/goals/operating-point-closure/evidence/
        // T-002_prototype/NOTES.md and work/active/WI-042_sourced-helium-ash-
        // profile/prototype/). The printed pair remains the cross-check.
        // WI-042 retirement note: alpha_n_e = 0.596 (bound 2026-08-21 from
        // the printed vol-av/peak pair) retires -- see the referent comment
        // above; the derived profile reproduces the pair it was bound from.

        // Sustainment held facts (WI-037). Every value image-verified against
        // the raw PDF or page images in goal round 1 (evidence NOTES.md);
        // the iter-01 AND iter-02 text extractions of these tables are
        // corrupted -- the raw PDF and images govern.
        :>> iota_23 = 0.92 {  // rotational transform at s = 2/3 [1].
            doc /* **Source**: stellaris-design-details.md **Ref**: iter-02 raw PDF p.7 Fig. 11(a) (iota(s) at s = 2/3 on the <beta>_V ~= 3% curve, read 0.92 +/- 0.01 -- the WI-022 figure-digitization precedent), bracketed by raw PDF Table 3 (axis 0.86, edge 0.98; the iter-02 output.md extraction of Table 3 prints axis 0.98 / edge 0.80 and is garbled). The 0.41 ISS04 exponent makes the read tolerance +/-0.45% in tau_E. **Basis**: rotational transform at the ISS04 reference surface */
        }
        :>> f_ren = 1.0 {     // ISS04 renormalization multiplier [1].
            doc /* **Source**: stellaris-design-details.md **Ref**: Table 4 image (images/page_008_table_0.png: f_ren 1.0) and Table 5 image (images/page_009_table_0.png: f_ren 1.0, both operating points) **Basis**: Stellaris ISS04 confinement fidelity at the operating points; never a calibration knob */
        }
        :>> f_alpha_fast = 0.95 { // fast-particle (alpha) confinement [1].
            doc /* **Source**: stellaris-design-details.md **Ref**: Table 4 image (images/page_008_table_0.png: f_alpha 0.95); raw PDF sec. 2.5 ("conservative value of the fast particle confinement of 95%") **Basis**: alpha heating fraction retained in the core */
        }
        :>> tau_ratio_ash = 8.0 { // tau_star/tau_E [1].
            doc /* **Source**: stellaris-design-details.md **Ref**: Table 4 image (images/page_008_table_0.png: tau_star/tau_E 8.0); Table 5 image (ratio 8.00, both points) **Basis**: particle-to-energy confinement time ratio for the A.5 helium balance */
        }
        :>> f_suppr_ash = 0.5 { // helium suppression factor [1].
            doc /* **Source**: stellaris-design-details.md **Ref**: Table 4 image (images/page_008_table_0.png: f_suppr 0.5); raw PDF appendix A ("choosing a value of f_suppr = 1/2" -- the extracted text "= 12" is an artifact) **Basis**: Eq. A.6 ash suppression (birth vs thermalization displacement) */
        }
        :>> Z_eff_core = 1.20 { // core effective charge [1].
            doc /* **Source**: stellaris-design-details.md **Ref**: Table 5 image (images/page_009_table_0.png: Vol av. Z_eff (core) 1.20, Point A) **Basis**: Stellaris core Z_eff for bremsstrahlung */
        }
        :>> f_W_core = 7.76e-6 { // core tungsten fraction n_W/n_e [1].
            doc /* **Source**: stellaris-design-details.md **Ref**: Table 5 image (images/page_009_table_0.png: Rel. tungsten fraction core 7.76e-6, Point A) **Basis**: Stellaris core tungsten content for line radiation (1costingFE W cooling-curve fit, radiation.py:83-96) */
        }
        :>> Ti_over_Te = 0.95 { // T_i0/T_e0 [1].
            doc /* **Source**: stellaris-design-details.md **Ref**: raw PDF sec. 2.5 ("fixed ion-to-electron temperature ratio of 0.95"); cross-check: printed Point-A pair 14.63/15.40 = 0.950 (Table 5 image) **Basis**: Stellaris fixed ion-to-electron temperature ratio */
        }

        // Power-balance inputs.
        // Heating power chain (WI-039). The installed wall-plug draw is the
        // entry point; source-output power (the cost driver) and plasma-coupled
        // power (the physics driver, and what sustainment_ok compares against
        // the plasma's requirement) are computed from it.
        :>> p_wallplug_heat = 100.0 {
            doc /*
            Installed wall-plug electrical power for ECRH [MW].

            The source prints the *coupled* figure, not this one: Table 2 image
            "Required plasma-coupled ECRH power [MW] 50" (raw PDF sec. 2.5, 50 MW
            to reach point A). 100.0 is that printed 50 MW divided by this chain's
            own stated efficiencies (eta_source_heat 0.50 x eta_couple_heat 1.00
            = 0.50). It is an exact algebraic restatement of a sourced value under
            stated assumptions, not a new number.

            WI-037's correction is preserved and now lives in the chain: the 50 MW
            is plasma-coupled power, not wall-plug, and sustainment_ok compares it
            coupled-to-coupled (heat.p_coupled into p_aux_installed_in below).

            Consequence, recorded so it is not later mistaken for a lost anchor
            (WI-039 design D1): with wall-plug as the entry point, a study that
            sweeps eta_source_heat moves coupled power off the printed 50 MW. That
            is the chain deriving something, which is the point of it.

            **Source**: stellaris-design-details.md
            **Ref**: Table 2 image (images/page_002_table_0.png: "Required
                plasma-coupled ECRH power [MW] 50"); raw PDF sec. 2.5
            **Basis**: Stellaris installed plasma-coupled ECRH power, divided by
                the chain's stated wall-plug-to-plasma efficiency (WI-039 D1)
            */
        }
        :>> eta_source_heat = 0.50 {
            doc /* **Source**: /home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml **Ref**: costing_constants.yaml:105 (eta_source_ecrh = 0.50); defaults.py:104-108 (per-method wall-plug source efficiency, "wall-plug -> delivered power, before plasma coupling") **Basis**: gyrotron wall-plug efficiency, ITER-procurement-calibrated */
        }
        :>> eta_couple_heat = 1.00 {
            doc /*
            Source output -> plasma-coupled fraction [1]. THE DEPOSITION
            ASSUMPTION, stated rather than defaulted (WI-039 MR-WI039-3).

            What it asserts: all power leaving the gyrotrons reaches the plasma.
            No transmission-line loss, no window loss, no shine-through, no
            unabsorbed first pass.

            Its status: this is the pinned 1costingFE per-concept value for ECRH
            (steady_state_stellarator.yaml:15, "ECRH coupling; eta_pin = 0.50 x
            1.0 = 0.50"). It is an idealisation, not a measurement.

            Its direction: optimistic. A real ECRH chain's transmission and
            single-pass absorption losses would put it below 1.0, which would
            raise both the wall-plug draw and the recirculating power for the
            same coupled power. The model carries no admissible source for either
            loss, so the gap is named here rather than guessed at (a missing
            input is surfaced, never defaulted).

            If a coupling figure is later sourced it enters at this one attribute
            and the whole chain re-derives.

            **Source**: /home/reid/1cfe/1costingfe/src/costingfe/data/defaults/steady_state_stellarator.yaml
            **Ref**: steady_state_stellarator.yaml:15 (eta_couple = 1.0)
            **Basis**: pinned 1costingFE per-concept ECRH coupling value, carried
                as a stated assumption (WI-039 design D2)
            */
        }
        :>> p_delivered_direct_heat = 0.0 {
            doc /* **Source**: WI-039 design D4 **Ref**: work/completed/20260904_WI-039_heating-system-structure/design.md (dormancy by additive direct terms) **Basis**: the chain is live, so the direct source-output term is zeroed -- coexisting would double-count (the p_cryo = 0.0 precedent below) */
        }
        :>> p_coupled_direct_heat = 0.0 {
            doc /* **Source**: WI-039 design D4 **Ref**: work/completed/20260904_WI-039_heating-system-structure/design.md (dormancy by additive direct terms) **Basis**: the chain is live, so the direct plasma-coupled term is zeroed -- coexisting would double-count */
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
        :>> p_pump = 195.0 {  // primary coolant pumping power [MW] -- helium-primary circulator basis (WI-033).
            doc /*
            Re-based from the 1costingFE default 1.0 MW -- a ~150x understatement
            for a helium-cooled ~3240 MWth plant (DI-008, amended 2026-08-28) --
            to 6% of the baseline computed p_th (3238.1 MW -> 194.3), landed
            rounded at 195.0 [OWNER 2026-08-28]. HELD, SETTABLE INPUT by owner
            ruling (goal p-pump-basis, trail, Goal close Ruling 2): a computed
            fraction of p_th would assert a linearity across swept (R, a) that
            no source establishes, and would retire a study lever in two
            committed studies. Re-derive the scalar when the design point moves.
            KNOWING TRACEABILITY-FIRST CHOICE (Ruling 3): the documented lower
            bound is ~130 MW (~4% of blanket thermal -- Moscato's near-term
            8-loop design, 16 compressors x 5.9/5.2 MW = 83-94 MW at
            2101.7 MWth; the f_uplift_cryo exclude-with-documented-bound
            pattern). Cismondi's ~150 MW (~6.3% of the 2389 MW deposited; the
            2017 9-loop layout reconstructs as 3x2x6.8 + 6x2x7.5 = 130.8 MW
            from Moscato Table 3) is a preliminary figure for one unoptimized
            layout its own authors expect to fall (larger pipes: ~9 km of loop
            piping -> ~3 km).
            **Source**: knowledge/sources/progress_in_eu_breeding_blanket_design_and_integration/ (Cismondi et al., EUROfusion WPPMI-CPR(17) 17709); knowledge/sources/progress_in_the_design_development_of_eu_demo_helium_cooled/ (Moscato et al., EUROfusion WPBOP-CPR(18) 20276)
            **Ref**: Cismondi output.md:174 (helium pumping power ~150MW, one order of magnitude above water ~15MW; 9km->3km pipe lever), :172 (HCPB PHTS representative for HCLL); Moscato output.md:81 (2101.7 MW blanket thermal), :89-:91 (9 loops: 3 IB + 6 OB), :145/:154 (Table 3: circulator power 6.8 IB / 7.5 OB MW, 2 compressors per loop per Table 1); Moscato raw.pdf p.7 Table 4 (near-term 5.9 STHE / 5.2 CWHE MW -- table body absent from output.md, re-derived from the registered raw PDF)
            **Basis**: 6% of the baseline computed p_th = 3238.1 MW (goal p-pump-basis trail:149, baseline_result.json@ffa5c54c), rounded to 195.0 [OWNER 2026-08-28]; ~130 MW recorded as documented lower bound per Ruling 3
            */
        }
        :>> f_sub = 0.03 {    // subsystem/control power fraction.
            doc /* **Source**: /home/reid/1cfe/1costingfe/src/costingfe/data/defaults/steady_state_stellarator.yaml **Ref**: steady_state_stellarator.yaml:17 (f_sub = 0.03) **Basis**: 1costingFE stellarator subsystem power fraction */
        }
        :>> p_tf = 0.0 {      // coil electrical drive power [MW] -- modeled zero for the SC coil set (WI-024).
            doc /*
            Coil electrical drive power: modeled 0.0. The Stellaris coil set is
            superconducting and operates steady-state DC -- no resistive drive
            power; 1costingFE's own superconductor model agrees
            (recirc_power_factor = 0.0 for every SC conductor grade,
            defaults.py:611-614; the resistive recirc model is copper-only). The
            one printed steady-state electrical dissipation -- ~7.5 kW
            resistive-joint losses, "negligible" (sec. 2.9) -- is counted as heat
            at 20 K inside the WI-024 cryoplant chain (p_fixed_cryo below), not
            as coil electrical. Current-lead and power-supply standing losses
            are unprinted in any admissible source and are part of the chain's
            documented lower bound (f_uplift_cryo). (History: the pre-WI-023
            111.0 mapped a phantom "conduction power to coils" text row -- the
            paper prints 111 only as stored magnetic energy [GJ]; WI-023 zeroed
            it as a deferral stopgap; WI-024 rescopes the zero from stopgap to
            modeled value.)
            **Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-02/sources/publikationen-1000179851-172386752/tmpissrtbos/raw.pdf
            **Ref**: sec. 2.9 (10 W per joint -> ~7.5 kW coil-set steady-state, "negligible"); /home/reid/1cfe/1costingfe/src/costingfe/defaults.py:611-614 (recirc_power_factor = 0.0 for superconductors)
            **Basis**: modeled zero for a superconducting coil set -- coil-adjacent parasitic load carried by the derived p_cryo (WI-024 design D1/D2, 2026-07-18)
            */
        }
        :>> p_tfcool = 15.0 { // coil cooling power [MW].
            doc /*
            1costingFE stellarator cooling power, kept at the source default.
            Post-WI-024 coverage (MR-WI024-3): read as the non-cryogenic
            cooling-system electrical (component / room-temperature cooling
            loops), disjoint from the 20 K cryoplant wall-plug now derived into
            p_cryo -- 1costingFE's own stellarator defaults carry p_cool = 15.0
            and p_cryo = 0.8 side by side (steady_state_stellarator.yaml:20,24),
            so in the source's intent they are distinct loads. The slot's
            upstream composition is undocumented; any cryo-compressor share it
            contains would overlap the derived p_cryo -- a conservative-direction
            residual (recirc overstated, LCOE up), documented here rather than
            silently resolved.
            **Source**: /home/reid/1cfe/1costingfe/src/costingfe/data/defaults/steady_state_stellarator.yaml
            **Ref**: steady_state_stellarator.yaml:20 (p_cool = 15.0); :24 (p_cryo = 0.8 carried side by side -- disjoint in the source's intent)
            **Basis**: 1costingFE stellarator cooling power; disjoint read vs the WI-024 derived cryoplant electrical (design D2, 2026-07-18)
            */
        }
        :>> p_trit = 10.0 {   // tritium systems power [MW].
            doc /* **Source**: /home/reid/1cfe/1costingfe/src/costingfe/data/defaults/steady_state_stellarator.yaml **Ref**: steady_state_stellarator.yaml:22 (p_trit = 10.0) **Basis**: 1costingFE stellarator tritium-processing power */
        }
        :>> p_house = 4.0 {   // housekeeping power [MW].
            doc /* **Source**: /home/reid/1cfe/1costingfe/src/costingfe/data/defaults/steady_state_stellarator.yaml **Ref**: steady_state_stellarator.yaml:23 (p_house = 4.0) **Basis**: 1costingFE stellarator housekeeping power */
        }
        :>> p_cryo = 0.0 {    // direct cryo-electrical term [MW] -- zeroed; chain derives the slot (WI-024).
            doc /*
            The 1costingFE generic default 0.8 MW (steady_state_stellarator.yaml:24)
            is retired: it and the WI-024 derivation are the same physical quantity
            (cryoplant wall-plug electrical -- 1cfe's own dipole defaults document
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
        :>> vol_cold_cryo = 0.0 {  // ADDITIONAL cold volume [m^3] beyond the winding pack.
            doc /*
            WI-036: the winding-pack cold volume is now COMPUTED IN THE MODEL
            (mfe_magnet_field 'Winding Pack Cold Volume'), from the sized pack
            cross-section, the computed winding length and the held set-distribution
            factor f_wp_vol -- reproducing the 136.56 m^3 this slot previously held
            as a literal. The arithmetic below was correct; it lived in this doc
            comment rather than in the model, which is exactly the defect WI-036
            closes. A wider winding pack now raises cryogenic load and cryoplant
            capital instead of being free.

            This slot is NOT retired. The plant sums the computed winding-pack
            volume with this attribute (mfe_plant.sysml, cryo_elec), so it stays a
            live settable entry point for cold mass beyond the winding pack, and a
            concept that knows its cold volume directly can bind it and zero
            f_wp_vol. The standing [OWNER 2026-08-27] WI-032 ruling bars retiring
            vol_cold_cryo as a settable input; it does not bar modelling the chain
            behind it -- the same width the owner drew for p_pump ("stays a held
            settable input -- the ruling bars only the fixed-fraction form, not
            loop modelling"). Bound to zero here because the winding pack IS the
            whole of this machine's printed cold mass; any non-zero value would
            double-count it.

            The retired arithmetic, kept for the record: six unique square winding-pack
            cross-sections (Table 8 image side lengths 360/360/340/340/320/300 mm)
            x 8 occurrences each (sec. 2.9: 48 coils = 4 periods x (6 independent
            + 6 mirrored)) x 25 m typical circumference. Sum of side^2 = 2x0.36^2
            + 2x0.34^2 + 0.32^2 + 0.30^2 = 0.6828 m^2; x8 x25 = 136.56 m^3.
            Cross-checks: each side^2 equals turns x (20 mm)^2 exactly (sec. 2.9
            unit cell; Table 8 turns row); Table 8 no-casing masses (128.7 t x 8
            = 1029.6 t) imply ~7540 kg/m^3, consistent with the Table 7 material mix.
            **Source**: stellaris-design-details.md
            **Ref**: Table 8 image (images/page_022_table_0.png: side lengths, turns, masses); raw.pdf sec. 2.9 (square winding pack; 20 mm x 20 mm unit cell; 25 m typical circumference; 48 = 4 x (6+6) symmetry); Table 7 image (images/page_021_table_0.png: material fractions)
            **Basis**: additive non-winding-pack cold volume; zero for this machine because the computed winding-pack chain now carries the whole printed cold mass
            */
        }
        :>> p_fixed_cryo = 0.0075 {  // resistive-joint losses [MW] at 20 K.
            doc /* **Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-02/sources/publikationen-1000179851-172386752/tmpissrtbos/raw.pdf **Ref**: sec. 2.9 (10 W per joint -> ~7.5 kW steady-state for the entire coil set, "negligible ... within the cooling capacity of existing cryocooler designs") **Basis**: printed coil-set joint dissipation, counted as heat at 20 K */
        }
        :>> f_uplift_cryo = 1.0 {   // unprinted-loads multiplier -- explicit lower bound (WI-024 D6).
            doc /*
            Bound 1.0 = printed loads only, a KNOWING LOWER BOUND: the paper defers
            casing, coil-case, and 20 K support-structure nuclear heating ("will be
            examined in future studies", sec. 2.9 raw.pdf), and current-lead /
            radiation loads are unprinted. No admissible uplift value exists; the
            parameter names the seam so the owner can raise it. Cited to the design
            ruling, not a source.
            **Source**: WI-024 design ruling (D6, 2026-07-18; sanctioned by spec Checkpoint Ruling 2)
            **Ref**: raw.pdf sec. 2.9 (the future-studies deferral)
            **Basis**: explicit assumption parameter -- exclude-with-documented-bound
            */
        }
        :>> T_cold_cryo = 20.0 {    // coil operating temperature [K].
            doc /* **Source**: raw.pdf **Ref**: sec. 2.9 ("cooled to 20 K using supercritical helium at 15-20 bar"; Top set to 20 K); sec. 2.8; corroborated by 1costingFE defaults.py:611 (rebco_hts cryo_temp_k = 20.0) **Basis**: Stellaris HTS coil operating temperature */
        }
        :>> T_amb_cryo = 300.0 {    // heat-rejection reference temperature [K].
            doc /* **Source**: WI-024 design ruling (D4, 2026-07-18) **Ref**: standard ambient reference for the Carnot COP **Basis**: explicit assumption parameter (standard engineering reference) */
        }
        :>> f_carnot_cryo = 0.20 {  // fraction-of-Carnot plant efficiency -- THE assumption (WI-024 D4).
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
            **Basis**: explicit assumption parameter -- fraction of Carnot, general practice band
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

        // Heating mix -- ECRH only (nbi/icrf/lhcd zeroed above).
        :>> heating_ecrh_per_mw = 5282900.0 {  // ECRH capital [$/MW].
            doc /* **Source**: /home/reid/1cfe/1costingfe/src/costingfe/defaults.py **Ref**: defaults.py:98-100 (heating_ecrh_per_mw = 5.2829 M$/MW) x 1e6 **Basis**: gyrotron ECRH per-MW capital */
        }
        // p_ecrh retired as a held value (WI-039): the heating cost account now
        // reads the chain's source-output power (heat.p_delivered), so installed
        // ECRH power and plasma-coupled power descend from one wall-plug input
        // instead of being two constants kept equal by a study-layer declaration.
        // Table 2 line 237 (ECRD/ECRH power = 50 MW) remains the source of record
        // for that power; it is now reproduced, not asserted.

        // Divertor (CAS22.1.8) driver.
        :>> divertor_base = 60000000.0 {  // divertor cost at 1 GWth [$].
            doc /* **Source**: /home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml **Ref**: costing_constants.yaml:97 (divertor_base = 60.0 M$) x 1e6 **Basis**: power-scaled divertor cost */
        }

        // CAS10 preconstruction -- forward-computed (WI-025); CAS27 special
        // materials -- forward-computed (WI-021).
        :>> precon_fixed_base = 16000000.0 {  // CAS10 fixed adders [$] (WI-025; WI-029 NOAK fix).
            doc /*
            16 M$ x 1e6 = site_permits 3 + licensing_cost_dt 5 (DT frozen) +
            plant_permits 2 + plant_studies_noak 4 + plant_reports 1 +
            other_precon 1. preconstruction_capital tracks the computed p_net
            via precon_cost (land ~ sqrt(p_net x 1000 x 1)); bound
            pre-contingency (CAS29 applies once -- convention preserved).

            WI-029 CORRECTION (one clean error, owner ruling 4): this base was
            32 M$, carrying plant_studies at the FOAK 20.0 while every sibling
            constant runs NOAK. Only plant_studies (foak 20 / noak 4) and
            contingency_rate (foak 0.10 / noak 0.0) are FOAK/NOAK-sensitive
            here, and the model's contingency handling is already NOAK-correct
            (deferred to CAS29 = 0), so studies 20 -> 4 is the whole error.
            The fix reconstructs 1cfe's CAS10 exactly at the handshake point:
            land 0.25 x sqrt(1000 x 1 x 1000) x 10000 / 1e6 = 2.5, plus fixed
            16.0, = 18.5 M$, residual 0.0. Because the fixed adders are
            power-independent, the design-point total capital drops by exactly
            $16M too -- recorded as a re-baseline, not asserted unchanged.
            Stale basis retired: the old $33.896M literal was computed at
            p_net = 575.3 (WI-018).
            **Source**: /home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml
            **Ref**: costing_constants.yaml:15-23 (plant_studies_noak = 4.0);
                costs.py:52-80 (cas10_preconstruction; :79 contingency not carried)
            **Basis**: CAS10 fixed adders at the NOAK DT design point
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

        // ---------------------------------------------------------------------
        // WI-028 CAS22 tail + CAS40 owner + CAS50 supplementary + CAS28 bases
        // ($) -- dollar conversions (x1e6 where the 1cfe constant is M$) of the
        // pinned DT/toroidal constants at 0254385. concept_scale = 1.0
        // (STELLARATOR) is bound HERE (instance), never a library default (MR-3).
        // p_cryo is wired in the generic plant (cryo_elec.p_elec). Reference
        // powers/exponents are library defaults / account-structural literals.
        // ---------------------------------------------------------------------
        :>> remote_handling_base = 150000000.0 {  // C220110 rh_base[DT] [$].
            doc /* 150.0 M$ x 1e6. **Source**: /home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml **Ref**: costing_constants.yaml:131 (remote_handling_dt_base = 150.0); cas22.py:645 **Basis**: DT remote-handling base at ref_gross */
        }
        :>> concept_scale = 1.0 {  // C220110 toroidal (STELLARATOR) scale.
            doc /* **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py **Ref**: cas22.py:641 (ConfinementConcept.STELLARATOR: 1.0; end-access geometries 0.55) **Basis**: toroidal remote-handling concept scale */
        }
        :>> installation_frac = 0.14 {  // C220111 fraction of reactor subtotal.
            doc /* **Source**: /home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml **Ref**: costing_constants.yaml:137 (installation_frac = 0.14); cas22.py:652-664 **Basis**: installation labor fraction of C220101..110 */
        }
        :>> coolant_primary_base = 166000000.0 {  // C220200 primary coolant [$].
            doc /* 166.0 M$ x 1e6 (linear in plant-total net). **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py **Ref**: cas22.py:684 (c220201 = 166.0 * p_net_total/ref_net) **Basis**: primary coolant loop */
        }
        :>> coolant_intermediate_base = 40600000.0 {  // C220200 intermediate [$].
            doc /* 40.6 M$ x 1e6 (power-law in plant-total thermal, a=0.55). **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py **Ref**: cas22.py:685 (c220202 = 40.6 * (p_th_total/3500)**0.55) **Basis**: intermediate coolant loop */
        }
        :>> aux_per_mw = 1100.0 {  // C220300 aux coolant [$/MW_th].
            doc /* 1.10e-3 M$/MW x 1e6 = 1100 $/MW (linear in plant-total thermal). **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py **Ref**: cas22.py:693 (c220301 = 1.10e-3 * p_th_total) **Basis**: auxiliary coolant per MW thermal */
        }
        :>> aux_cryo_base = 200000000.0 {  // C220300 cryoplant [$].
            doc /* 200.0 M$ x 1e6 (power-law in per-module p_cryo, ref 30, a=0.7). **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py **Ref**: cas22.py:694 (c220302 = 200.0 * (p_cryo/30)**0.7) **Basis**: cryoplant base at 30 MW */
        }
        :>> waste_base = 1960000.0 {  // C220400 radwaste [$].
            doc /* 1.96 M$ x 1e6 (linear in plant-total thermal, a=1.0). **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py **Ref**: cas22.py:702 (c220400 = 1.96 * p_th_total/1000) **Basis**: radwaste handling */
        }
        :>> fuel_handling_base = 120000000.0 {  // C220500 fuel handling DT [$].
            doc /* 120.0 M$ x 1e6 (power-law in plant-total net, a=0.7). **Source**: /home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml **Ref**: costing_constants.yaml:165 (fuel_handling_dt_base = 120.0); cas22.py:718 **Basis**: DT tritium processing + containment */
        }
        :>> other_rpe_base = 11500000.0 {  // C220600 other reactor plant [$].
            doc /* 11.5 M$ x 1e6 (power-law in plant-total net, a=0.8). **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py **Ref**: cas22.py:724 (c220600 = 11.5 * (p_net_total/1000)**0.8) **Basis**: other reactor-plant equipment */
        }
        :>> inc_base = 85000000.0 {  // C220700 instrumentation & control [$].
            doc /* 85.0 M$ x 1e6 (power-law in plant-total thermal, ref 3500, a=0.65). **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py **Ref**: cas22.py:731 (c220700 = 85.0 * (p_th_total/3500)**0.65) **Basis**: reactor I&C */
        }
        :>> owner_base = 41200000.0 {  // CAS40 owner cost DT [$].
            doc /* 41.2 M$ x 1e6 (power-law in plant-total net, ref 1000, a=0.5). **Source**: /home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml **Ref**: costing_constants.yaml:245 (owner_cost_dt = 41.2); costs.py:256 **Basis**: DT owner's cost (117 staff, pre-op training) */
        }
        :>> supplementary_spares_frac = 0.03 {  // CAS50 spare parts frac (DT).
            doc /* fraction of CAS23..28. **Source**: /home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml **Ref**: costing_constants.yaml:253 (spare_parts_frac_dt = 0.03); costs.py:274 **Basis**: activated-component spares */
        }
        :>> supplementary_startup_base = 40000000.0 {  // CAS50 startup fuel DT [$].
            doc /* 40.0 M$ x 1e6 (linear in plant-total net). **Source**: /home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml **Ref**: costing_constants.yaml:259 (startup_fuel_dt = 40.0); costs.py:277 **Basis**: tritium startup inventory */
        }
        :>> supplementary_decom_base = 272000000.0 {  // CAS50 decom provision DT [$].
            doc /* 272.0 M$ x 1e6 (linear in plant-total net). **Source**: /home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml **Ref**: costing_constants.yaml:263 (decom_provision_dt = 272.0); costs.py:278 **Basis**: PV decommissioning provision */
        }
        :>> cas28_capital = 5000000.0 {  // CAS28 digital twin [$] (F-2).
            doc /* 5.0 M$ x 1e6. **Source**: /home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml **Ref**: costing_constants.yaml:229 (digital_twin = 5.0); model.py:1479 **Basis**: digital-twin capital, part of c23..c28 */
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
            p_net via om_cost (x sqrt(p_net/1000)); unlevelized -- CAS71
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
        // ANNUAL-COST SIDE INPUTS -- CAS71 / CAS72 / CAS80 (WI-029)
        // Every constant below is an INSTANCE binding, not a library default
        // (MR-3): the fuel chemistry, the fluence limit, and the escalation
        // rate all belong to the concept, not to the concept-agnostic calcs.
        // ---------------------------------------------------------------------

        :>> inflation_rate = 0.02 {    // escalation rate g for CAS71/CAS80 levelization.
            doc /* **Source**: /home/reid/1cfe/1costingfe/src/costingfe/adapter.py **Ref**: adapter.py (inflation_rate = 0.02); emit_1cfe_point.py:10 (the handshake point runs inflation_rate = 0.02) **Basis**: 1costingFE reference escalation rate */
        }

        // ---- CAS80 DT fuel chemistry (costs.py:476-544 DT branch) ----
        :>> fuel_cost_per_rxn = 1.7260641119988767e-23 {  // $/reaction.
            doc /*
            M_DEUTERIUM_KG * u_deuterium + M_LI6_KG * u_li6
              = 3.3435837768e-27 kg * 2175 $/kg
              + 6.015122795 * 1.66053906892e-27 kg * 1000 $/kg
              = 1.7260641119988767e-23 $/rxn.
            One deuteron plus one Li-6 atom (bred to tritium in the blanket)
            per D-T event; the enriched Li-6 is the tritium feedstock.
            **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/physics.py (pin 0254385)
            **Ref**: physics.py:13-20 (M_DEUTERIUM_KG, M_LI6_KG, _ATOMIC_MASS);
                costing_constants.yaml:282 (u_deuterium 2175), :283 (u_li6 1000);
                costs.py:477 (cost_per_rxn, DT branch)
            **Basis**: Blended D + Li-6 feedstock cost per D-T fusion event
            */
        }
        :>> fuel_q_eff = 17.58 {       // per-reaction energy Q_DT [MeV].
            doc /* **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/physics.py **Ref**: physics.py:33 (Q_DT = 17.58) **Basis**: D-T fusion Q-value */
        }
        :>> mev_to_joules = 1.6021766339999998e-13 {  // 1 MeV in J.
            doc /* **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/physics.py **Ref**: physics.py:13,16 (MEV_TO_JOULES = _EV * 1e6, _EV = 1.602176634e-19 exact by the 2019 SI redefinition) **Basis**: CODATA 2018 / SI-exact energy conversion */
        }
        :>> burn_fraction = 0.05 {     // single-pass burn fraction (MFE-class).
            doc /* **Source**: /home/reid/1cfe/1costingfe/src/costingfe/data/defaults/steady_state_stellarator.yaml **Ref**: steady_state_stellarator.yaml:64 (burn_fraction = 0.05) **Basis**: 1costingFE steady-state stellarator single-pass burn fraction */
        }
        :>> fuel_recovery = 0.99 {     // unburned-fuel recovery fraction (NOAK).
            doc /* **Source**: /home/reid/1cfe/1costingfe/src/costingfe/data/defaults/steady_state_stellarator.yaml **Ref**: steady_state_stellarator.yaml:65 (fuel_recovery = 0.99) **Basis**: 1costingFE NOAK unburned-fuel recycle fraction */
        }

        // ---- CAS72 scheduled-replacement inputs ----
        :>> fluence_limit = 18.0 {     // core fluence limit [MW-yr/m^2], DT.
            doc /* **Source**: /home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml **Ref**: costing_constants.yaml:153 (fluence_limit_dt = 18.0, "ARIES FS 200 dpa = 18 MW yr/m^2") **Basis**: DT first-wall/blanket neutron-fluence replacement limit */
        }
        // WI-041 retired the exact ash_frac binding (E_ALPHA_DT / Q_DT =
        // 0.2002275...) that fed the CAS72 chain's own neutron power: the chain
        // now reads the peak wall load, whose average carries the calc's 0.2002
        // default. The exact binding's purpose -- a 1e-6 A-2 comparison against
        // 1costingFE's CAS72 -- is moot: that handshake has been broken since
        // the migration, and the peak operand departs from 1cfe's average-based
        // chain by design. The convention change is 3.4e-5 relative on the
        // operand, folded into the declared CAS72 move (WI-041 plan, restatement).

        // ---------------------------------------------------------------------
        // VIABILITY CONSTRAINTS (WI-018 additions: beta, wall load, TBR)
        // ---------------------------------------------------------------------

        // Beta (WI-030): computed by beta_calc ('Volume-Averaged Beta') from the
        // profile referents above and magnet.B. The printed Table 5 value,
        // vol. av. beta 2.76 % (Point A) / 2.81 % (Point B), is the cross-check,
        // not an input: computed 0.026834 / 0.028691 (SV-036). The former bound
        // beta = 0.0276 (analyst-patch-spec-anchors.md line 44) is retired.
        // design/optimization beta target.
        attribute beta_limit : Real = 0.05 {
            doc /* **Source**: stellaris-design-details.md **Ref**: line 273 (coils + boundary optimized at <beta>_V = 5%) **Basis**: Stellaris design beta target */
        }

        // Neutron wall load -- the AVERAGE, the source-anchored PEAK, and the fence
        // (WI-021 forward computation; WI-041 source-anchored peak).
        // The generic plant's wall_load_calc forward-computes the circular-torus
        // average over rb.wall_area = kappa*4*pi^2*R*vacuum_or at the first-wall
        // standoff radius (vacuum_or = a + vacuum_t = 1.40 m), = 701.926 m^2 at the
        // Stellaris build (R = 12.7, a = 1.3, kappa = 1.0). 1costingFE torus
        // geometry, no shape factor on material geometry (owner Option 1, WI-021).
        // vacuum_t = 0.10 m is the source's MINIMUM plasma-to-wall distance (line
        // 1295: "a minimum distance of 100 mm"); the source's averaged SOL gap is
        // 16.6 cm (Fig. 34 image, pdf-17-2.png). The calibration below absorbs the
        // difference at the design point.
        //
        // WHAT THE SOURCE PRINTS (every figure confirmed against its page image;
        // the extracted text of Tables 2, 5 and 6 was rewritten by the extraction
        // and is not trusted -- decisions.json pages 2, 9, 20 `claude_replace`):
        //   - peak neutron wall load 4.05 MW/m^2 at ~2700 MW, Table 2 image
        //     (page_002_table_0.png), a 3D value on the design's own CAD first
        //     wall by the method of Lion 2022 [240] (lines 1606-1607; Fig. 33 image
        //     pdf-17-1.png, colour scale 0-4 MW/m^2). The ONLY printed peak: the
        //     Table 5 image (page_009_table_0.png) has no peak row, and the
        //     extracted "4.95" (line 748) is an artifact.
        //   - "Av. neutron wall power" 2.87 MW/m^2, Table 5 image. Its basis is
        //     NOT STATED. By the source's own cited definition (neutron power per
        //     first-wall area) it cannot be an average over the Fig. 33 wall: neutron
        //     power over the printed 940 m^2 plasma surface is already only 2.30,
        //     and the source's damage map (Fig. 38: peak 3.9 / mean 2.2 DPA/GWf/yr)
        //     puts the wall average near 2.28. It equals fusion power over the
        //     printed plasma surface, 2700 / 940 = 2.872, to three figures. It is a
        //     REPORTED COMPARAND of unstated basis, never a limit, and 4.05 / 2.87 =
        //     1.41 is NOT a peaking factor. The model's average, 3.105 MW/m^2, is
        //     on a different basis (the circular torus at the minimum standoff) and
        //     is not comparable to it.
        // THE FENCE (WI-041): wall_load_ok compares the computed PEAK -- the average
        // times wall_peak_calibration, 1.316441, computed by the generic plant's
        // wall_peak_cal from the six reference facts bound below -- against the
        // printed 4.05. At the source's own design point the peak equals 4.05 by
        // construction; at this baseline, whose p_fus (2725.4 MW) sits 0.94% above
        // the source's 2700, the peak reads 4.05 x 2725.363 / 2700 = 4.088 MW/m^2:
        // EXPECTED VIOLATED, disclosed here and never tuned (goal wall-and-heating
        // § Invariants, on the sustainment_ok precedent). The same peak sets the
        // CAS72 lifetime (cas72_calc.q_n_in): 18 / 4.088 = 4.40 FPY, beside the
        // source's own ~4 FPY (Table 6 image; text lines 1811-1813).
        // Evidence of record: work/orchestration/goals/wall-and-heating/evidence/
        //   round2_T-001_source_basis.md; WI-041 spec, design D1-D5.

        // The source's printed peak [MW/m^2] -- the anchor of the calibration.
        :>> wall_peak_q_ref = 4.05 {
            doc /*
            Peak neutron wall load on the design's own first wall at ~2700 MW,
            computed on the CAD wall (minimum 100 mm from the plasma) with the
            3D method of Lion 2022 [240]. The calibration this anchors,
            1.316441 = 4.05 x 701.926 / (2700 x 0.7998), decomposes as
            p_f x (A_torus / A_wall); it is carried as ONE computed quantity
            (WI-041 design D3) and the decomposition is a cross-check only:
            the source's own damage peaking 3.9 / 2.2 = 1.77 (Fig. 38 caption,
            lines 1783-1786; Lion 2022 line 366 calls the wall load a relative
            indicator of dpa) implies a wall area of ~945 m^2 -- the printed
            940 m^2 plasma surface plus a standoff; the round-1 external band
            p_f = 1.5-2.1 (Lion, Haeussler, Beidler; unoptimised equidistant
            walls) implies 800-1120 m^2. Both bracket the wall the source
            describes. CONSTANCY (design D4): the calibration is fixed at this
            design point and carried unchanged over sweeps of R, a, n_e0, T_i0
            and I_coil -- a sweep of R or a moves the peak through the model's
            own wall_area while the wall's shape is assumed to scale with it;
            a re-shaped wall would need a new anchor.
            **Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md
            **Ref**: Table 2 image (images/page_002_table_0.png: "Peak neutron wall load 4.05"); Fig. 33 image (images/stellaris-high-field-quasi-isodynamic-stellarator.pdf-17-1.png, caption lines 1579-1580); lines 1606-1607 (the method), 1295 (the standoff)
            **Basis**: Stellaris 3D first-wall peak neutron load at 2700 MW
            */
        }
        // The source's fusion power at that peak [MW].
        :>> wall_peak_p_fus_ref = 2700.0 {
            doc /* **Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md **Ref**: Table 2 image (images/page_002_table_0.png: "Peak fusion power ~2700"); Fig. 33 caption lines 1579-1580 ("at 2700 MW fusion power") **Basis**: the fusion power the printed peak belongs to */
        }
        // The source's radii [m], elongation [1] and minimum standoff [m]: the
        // model's own wall-area convention evaluated at the source's design point.
        :>> wall_peak_R_ref = 12.7 {
            doc /* **Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md **Ref**: Table 2 image (images/page_002_table_0.png: "Major plasma radius 12.7"); Table 1 image (images/page_001_table_0.png) **Basis**: Stellaris major radius; equals the model's R */
        }
        :>> wall_peak_a_ref = 1.3 {
            doc /* **Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md **Ref**: Table 2 image (images/page_002_table_0.png: "Minor plasma radius 1.3"); Table 1 and Table 5 images agree; the extracted text's "1.5" is a rewrite artifact **Basis**: Stellaris minor radius; equals the model's a */
        }
        :>> wall_peak_kappa_ref = 1.0 {
            doc /* **Source**: models/designs/stellarator_09/stellarator_plant.sysml **Ref**: kappa = 1.0 (QI stellarator ~ circular average; the model's own convention) **Basis**: the model's wall-area convention at the source's point */
        }
        :>> wall_peak_standoff_ref = 0.10 {
            doc /* **Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md **Ref**: line 1295 ("the first wall is positioned at a minimum distance of 100 mm from the plasma"); the averaged SOL gap is 16.6 cm (Fig. 34 image, pdf-17-2.png) -- the model's vacuum_t is the minimum, and the calibration absorbs the difference at the design point **Basis**: Stellaris minimum plasma-to-wall standoff; equals the model's vacuum_t */
        }
        // The chain is live: the direct term is zeroed (WI-041 design D1; the
        // p_cryo = 0.0 and p_coupled_direct_heat = 0.0 precedents).
        :>> wall_peak_calibration_direct = 0.0 {
            doc /* **Source**: WI-041 design D1 **Ref**: work/active/WI-041_source-anchored-wall-load-fence/design.md (dormancy by an additive direct term) **Basis**: the calibration is anchored, so the dormant direct term is zeroed */
        }

        // first-wall PEAK design limit [MW/m^2] (WI-022; WI-041 confirmed).
        attribute wall_load_limit : Real = 4.05 {
            doc /* **Source**: stellaris-design-details.md **Ref**: Table 2 image (images/page_002_table_0.png: "Peak neutron wall load 4.05"); the Table 5 image (images/page_009_table_0.png) prints no peak row, so the extracted "4.95" (line 748) is a rewrite artifact of that page (decisions.json page 9) **Basis**: Stellaris first-wall peak neutron-load design value, the only printed peak */
        }

        // TBR.
        // achieved tritium breeding ratio.
        attribute tbr : Real = 1.074 {
            doc /* **Source**: stellaris-design-details.md **Ref**: line 1659 (final TBR = 1.074) **Basis**: Stellaris 3D-neutronics TBR */
        }
        // self-sufficiency floor.
        attribute tbr_floor : Real = 1.05 {
            doc /* **Source**: stellaris-design-details.md **Ref**: line 1530 (TBR > 1.05 self-sufficiency target) **Basis**: D-T tritium self-sufficiency floor */
        }

        // Asserted viability constraints.
        assert constraint beta_ok : 'Beta Limit' {
            in beta_in = beta_calc.beta;
            in beta_limit_in = beta_limit;
        }
        // Wall load (WI-041): the computed PEAK against the printed peak. At this
        // baseline the verdict is EXPECTED VIOLATED (4.088 against 4.05, by the
        // model's 0.94% fusion-power excess over the source's 2700 MW) -- the
        // disclosed, explained verdict change of the WI-041 increment, never
        // tuned. Before WI-041 the operand was the circular-torus average.
        assert constraint wall_load_ok : 'Neutron Wall Load Limit' {
            in wall_load = wall_peak_calc.wall_load_peak;
            in wall_load_limit_in = wall_load_limit;
        }
        assert constraint tbr_ok : 'TBR Floor' {
            in tbr_in = tbr;
            in tbr_floor_in = tbr_floor;
        }
        // Sustainment (WI-037): required sustained plasma-coupled heating vs
        // installed. The operand is fully computed (ISS04 closed form, composed
        // radiation, converged ash) and responds to field, heating, density,
        // temperature, and geometry. At this lever point the verdict is
        // EXPECTED SATISFIED by about 0.9 MW (p_aux_required ~= 49.1 MW vs
        // 50 coupled) since WI-042 put the helium ash on the source's own
        // profile rule with the electrons by quasi-neutrality (W 551 -> 520 MJ;
        // it read VIOLATED at ~90 MW under the WI-037 profile family, whose
        // ash carried the fuel's exponent -- goal stored-energy-basis L-003).
        // The margin is inside the source's own 2.7 % residual on its printed
        // stored energy (L-002): the design point's sustainment is
        // undetermined within the source's precision -- on the boundary --
        // and nothing here is tuned (goal stored-energy-basis, owner ruling
        // 2026-09-05; WI-042 design § Expected baseline behaviour).
        assert constraint sustainment_ok : 'Sustainment Limit' {
            in p_aux_required_in = sustain.p_aux_required;
            in p_aux_installed_in = heat.p_coupled;
        }

        // Exposed neutron wall load (headline physics output): the circular-torus
        // average, unchanged by WI-041 and retained as the reported quantity.
        attribute neutron_wall_load : Real = wall_load_calc.wall_load;
        // Exposed source-anchored peak and its calibration (WI-041).
        attribute neutron_wall_load_peak : Real = wall_peak_calc.wall_load_peak;
        attribute wall_peak_calibration : Real = wall_peak_cal.calibration;
    }
}
