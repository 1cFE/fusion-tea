# Domain Knowledge

Curated domain insights that have passed through the research approval gate or been captured inline during modeling work. Each entry is a structured record of something we know about the domain that affects how we model it.

This file is the actionable feed for modeling work. Raw research lives in `knowledge/research/`; only approved, structured insights belong here.

---

*No entries yet. Domain insights (DI-XXX) will be derived from research conducted under the investigation-driven workflow.*

*Previous entries (DI-001 through DI-014) archived to `archive/knowledge/KNOWLEDGE.md`.*

### DI-001: IFE Fusion Cycle Gain Viability Threshold
- **Source**: EIF-1992, Accel-2013, Xcimer-2026
- **Context**: The product eta*G (driver efficiency times target gain) must exceed ~10 for economically viable IFE. This creates fundamentally different gain requirements by driver type: heavy-ion needs G>33 (at 30% eta), lasers need G>140 (at 7% eta), pulsers need G>100 (at 10% eta).
- **Model implications**: The gain requirement constraint should be a validation check in all IFE concept models
- **Analysis implications**: Concepts below the eta*G>10 threshold should be flagged as requiring breakthrough physics
- **Status**: captured

### DI-002: CAS22 is the IFE-MFE Divergence Point
- **Source**: ARIES-2013, PyFECONS, Hawker-2020
- **Context**: The CAS framework (20-99) is universal across fusion approaches. MFE and IFE share CAS20-21, 23-27, and 91-99. All concept-specific differences concentrate in CAS22 sub-accounts: 22.1.3 (magnets to driver), 22.1.4 (heating to ignition), 22.1.8 (divertor to target factory). PyFECONS confirms via polymorphic Union types.
- **Model implications**: Library components for CAS23-27 and indirect costs are fully reusable across MFE and IFE
- **Analysis implications**: Cross-concept comparison at CAS-level should normalize CAS22 sub-accounts by function
- **Status**: captured

### DI-003: IFE Target Cost is a Unique Operating Cost Category
- **Source**: Hawker-2020, HIF-1986, PyFECONS
- **Context**: IFE has a per-shot consumable cost (manufactured targets at $0.19-100 each) with no MFE parallel. Hawker shows target cost has stronger LCOE correlation (+0.186) than driver cost (+0.075), with a threshold effect: below ~$10/target, further reduction provides limited benefit.
- **Model implications**: IFE cost models must include target manufacturing as an operating cost separate from driver capital cost
- **Analysis implications**: The $10/target threshold is a key competitiveness indicator for IFE concepts
- **Status**: captured

### DI-004: IFE Driver Cost Reference Points
- **Source**: Hawker-2020, Xcimer-2026, AMPS-2025, HIF-1986
- **Context**: Driver cost per joule spans 3 orders of magnitude: NIF $9.5/J, DPSSL $700-1000/J (floor), Xcimer KrF-NLO $60-120/J FOAK, pulsed-power $1.7-6/J. Heavy-ion induction linacs fall in between. These reference points anchor cost model calibration.
- **Model implications**: Driver cost parameter ranges must be set per-driver-type, not as a single universal range
- **Analysis implications**: The $100/J threshold identified by Xcimer appears to be a rough dividing line between economically viable and non-viable laser IFE
- **Status**: captured

### DI-005: Hawker 14-Parameter IFE LCOE Model
- **Source**: Hawker-2020
- **Context**: Hawker identifies 14 technology-agnostic parameters sufficient to characterize IFE LCOE. Top sensitivities by Pearson correlation: discount rate (+0.247), plant cost (+0.210), target cost (+0.186), gain (-0.164), driver lifetime (-0.134), availability (-0.127). The frequency-yield trade-off is the most important interaction: high yield + low frequency unlocks the lowest LCOE designs.
- **Model implications**: All 14 parameters should be captured as model attributes with ranges; the model should support parametric variation across them
- **Analysis implications**: Sensitivity analysis should explore 2D interactions (especially frequency vs. yield), not just 1D parameter sweeps
- **Status**: captured

### DI-006: LCOE nonlinearity: center-of-range defaults ≠ center LCOE
- **Source**: work-item:WI-007/verify_ife_lcoe.py
- **Context**: Hawker's 14 Monte Carlo parameter defaults (center of uniform distributions) produce LCOE=$252.30/MWh — far above the $25-120/MWh range reported by Hawker. This is because LCOE is highly nonlinear: low frequency (0.2 Hz) yields a 44 MW plant where capital costs dominate. Realistic HIF parameters (f=5Hz, eta=0.25) give $68.69/MWh. *(Figures corrected 2026-07-04 — a digit corruption had dropped the leading "2"s; verified against `scripts/verify_ife_lcoe.py`. See WI-016 `retro_capture_hawker.md`.)*
- **Model implications**: SV-008 verified at realistic design points, not Monte Carlo centers. Default parameters in ife_cost_parameters.sysml represent distribution ranges for Monte Carlo, not an optimized design.
- **Analysis implications**: When running parametric sweeps, report LCOE distribution statistics rather than evaluating at parameter midpoints. Small plant sizes (<100 MW) amplify capital cost impact.
- **Status**: captured

### DI-007: Power-cycle choice does not reach primary-coolant pumping power
- **Source**: 1costingFE @0254385 defaults.py:578-593, docs/account_justification/CAS23_26_balance_of_plant.md:163-166; Stellaris raw.pdf (publikationen-1000179851) output.md:1336; WI-031 research 20260821-165616
- **Context**: A power-cycle swap (steam Rankine vs sCO2 Brayton) changes how heat becomes electricity, not how heat leaves the blanket. With a gas-cooled blanket (Stellaris: helium at 8 MPa) the cycle working fluid is secondary-side; the sCO2 cycle's own compressor work is already inside its eta_th. 1costingFE's cycle preset carries exactly three fields: eta_th, turbine_per_mw, heat_rej_per_mw. p_pump is a concept-level engineering default with no cycle dependence.
- **Model implications**: Hold p_pump (and eta_p) identical across cycle arms; a cycle A/B is an eta_th + CAS23/CAS26-rate comparison only. Any study that varies another value 'by cycle' is inventing a dependency the upstream model does not have and must say so.
- **Analysis implications**: Record the cycle study's p_pump as 'cycle-independent by construction', not 'unsourced'. Cycle comparisons across concepts should be read as efficiency-plus-BOP-cost deltas.
- **Status**: captured

### DI-008: Helium primary-loop circulator power is 2-6% of blanket thermal power; the stellarator default understates it ~100x
- **Source**: Cismondi et al. EUROfusion WPPMI-CPR(17) 17709 (ingested, concept 31 sources :176); Kessel et al. ARIES-ACT overview (ingested, osti-servlets-purl-1178069.md:175,290); Moscato et al. SOFT 2018 WPBOP-CPR(18) 20276 (open PDF, not ingested); WI-031 research 20260821-165616
- **Context**: Gas coolant needs high flow and high pressure drop. EU DEMO HCPB (2017): ~131 MW circulator power for 2101.7 MWth (6%); near-term 8-loop design 83-94 MW (~4%); Cismondi: '~150 MW, one order of magnitude higher than water (~15 MW)'; ARIES-ACT (DCLL, He+LiPb) ~1%, 2% for helium in the divertor. 1costingFE's stellarator default p_pump = 1.0 MW (steady_state_stellarator.yaml:21) for a ~3150 MWth helium-cooled plant is ~0.03%; Stellaris itself lists pumping estimation as future work.
- **Model implications**: Re-source the stellarator p_pump from a helium-circulator basis (2-6% of blanket thermal power, ~60-190 MW for Stellaris) through a dedicated modeling item; do not fold it into an A/B study, because it moves the baseline and every arm equally.
- **Analysis implications**: Absolute LCOE and recirc_ok verdicts from the current stellarator package carry a known optimism of order 60-190 MW recirculating power. Helium-cooled concepts carry a recirculating-power penalty that water- and LiPb-cooled concepts do not; treat coolant choice as a divergence point in cross-concept comparison.
- **Status**: captured

### DI-009: Large helium cryoplants run at 0.22-0.30 of Carnot, roughly independent of 4.5 K vs 20 K
- **Source**: knowledge/sources/iter_cryoplant_iter_org/ (cryogenics/output.md:30; as_cold_as_it_gets/output.md:36: 75 kW@4.5K, 1300 kW@80K, 35 MW); CERN Courier 'CERN's giant fridge' (18 kW@4.5K per 4 MW); Dhard et al. Physics Procedia 67 (2015) W7-X (5 kW design, 1.5 MW compressor rating; search snippet). Local un-ingested PDF: Miyazawa & Goto, Phys. Plasmas 30, 050601 (2023), 2% cooling efficiency at 20 K. WI-031 research 20260821-165616
- **Context**: Fraction-of-Carnot derived with T_amb = 300 K: ITER 0.24 plant-level (0.14 if all 35 MW is charged to the 4.5 K load; the model chain has no 80 K load, so 0.24 is the like-for-like figure); LHC 0.30 (spec paper states 28%); W7-X >= 0.22 (a compressor rating bounds the draw from above). A 20 K HTS design assumption of 2% cooling efficiency corresponds to 0.28 of Carnot. Stellaris's assumed f_carnot_cryo = 0.20 sits at the conservative edge of this band at both temperatures.
- **Model implications**: The Carnot x fraction chain shape (mfe_cryo_plant.sysml) is validated: the fraction is a plant-scale property, the temperature effect belongs in the Carnot term. Hold f_carnot_cryo equal across magnet-technology arms so an A/B isolates T_cold. A sourced re-basing of 0.20 -> ~0.24 should be applied to all arms at once, after ingesting an ITER cryoplant source.
- **Analysis implications**: The 20 K vs 4.5 K cryogenic advantage is the Carnot COP ratio (~4.6x electrical per watt of heat), not a plant-efficiency difference. Cryoplant electrical for any MFE concept can be estimated from heat load, T_cold, and f ~ 0.22-0.30 when no machine-specific figure exists, with the basis stated.
- **Status**: captured

### DI-010: Nb3Sn winding-pack engineering current density at 12 T class is ~15-28 A/mm2 vs 112-124 A/mm2 for Stellaris REBCO
- **Source**: knowledge/sources/eu_demo_rw_tf_coil_conductor_dematte_bruzzone/output.md:45-49 (Dematte & Bruzzone, EU DEMO R&W TF coil conductor): 14.9 MA-turns, 142 x 104.95 kA, WP 1296 x 411 mm (proposed) vs 226 x 66 kA, ~1240 x 821 mm (reference); OSTI 6729950 (1990 ITER CDA, 4000 A/cm2 target). In-repo: Stellaris Table 8, publikationen-1000179851 output.md:1912-1935 (j_WP 112-124 A/mm2). WI-031 research 20260821-165616
- **Context**: Overall winding-pack current density (conductor + jacket + insulation + fillers) sets coil volume for a given Amp-turn requirement. EU DEMO Nb3Sn TF: 14.6 A/mm2 (reference) to 28 A/mm2 (react-and-wind proposal at 12.04 T, 6.5 K); dated ITER-CDA target 40 A/mm2. Stellaris REBCO at 20 K: 112-124 A/mm2. At equal Amp-turns an Nb3Sn pack is 4-8x the cold volume: Stellaris vol_cold_cryo 136.56 m3 -> ~575-1100 m3. First-order only: a thicker pack also moves coil-plasma distance and the peak/axis field ratio.
- **Model implications**: An LTS magnet arm has two physical differences from REBCO, not one: the 13 T peak-field ceiling (encoded by WI-030's peak_field_ok) and 4-8x larger winding-pack volume, which should enter vol_cold_cryo (and hence nuclear heat load and cryoplant electrical) once the EPFL source is ingested; holding the REBCO volume flatters LTS.
- **Analysis implications**: Conductor swaps in cost studies must carry a volume scaling, not just $/kAm and T_cold; reported LTS-vs-HTS deltas that hold coil volume fixed understate the HTS advantage.
- **Status**: captured

### DI-011: B enters MFE physics through beta, not only magnet cost; thermal beta from a source's printed peaks sits 2-3% under its printed equilibrium beta
- **Source**: Stellaris design paper Table 5 / Table 2 page images (09-qi-stellarator-hts/iter-01/sources/stellaris-design-details/images/page_009_table_0.png, page_002_table_0.png); 1costingFE @0254385 tokamak.py:117-126, defaults.py:605-614; WI-030 verification record (work/completed/20260822_WI-030_computed-beta-peak-field/verification_record.md) and audit work/analysis/20260821-171229_audit_WI-030_computed-beta-peak-field.md
- **Context**: Before WI-030 the on-axis field B reached only the magnet cost (mfe_magnet_cost.sysml) and beta was a typed-in input, so a lower-field conductor arm cost less and lost nothing. Volume-averaged thermal beta computed from the source's own peak densities, peak temperatures, (1-rho^2)^alpha profile exponents and B (beta = 2 mu0 <p> / B^2, <p> = e_keV * sum_s n_s0 T_s0 / (1 + alpha_n,s + alpha_T)) reproduces Stellaris Point A at 0.026834 vs printed 2.76% (-2.8%) and Point B at 0.028691 vs 2.81% (+2.1%). The residual has the sign and size of the fast-particle pressure the paper's equilibrium beta includes (Table 4 f_p) and thermal beta excludes. 1costingFE's compute_beta_N uses mu0 n_e (T_e + n_i T_i)/B^2, half the standard 2 mu0 p / B^2; the printed value validates the standard form. The conductor ceiling enters as an inequality B_axis * peak_ratio <= B_max (Stellaris 24.9/9.0 = 2.767; REBCO 24.9 T design value vs 23.0 T upstream ceiling; Nb3Sn 13.0 T gives a 4.6988 T on-axis ceiling).
- **Model implications**: Any MFE instance with (1-rho^2)^alpha profiles should bind peaks and exponents and let beta be computed ('Volume-Averaged Beta'); never bind beta as an input when B is a study lever. Expect computed thermal beta 2-3% under a source's printed equilibrium beta and set cross-check tolerances accordingly (WI-030 used +/-3.5%). Pair a field lever with a conductor ceiling ('Conductor Peak Field' + 'Conductor Peak Field Limit' on the library Magnet System) so a cheaper low-field arm is rejected by the model's own verdict. Bind peak_ratio as the float64 of the printed pair so the design point reads margin 0.0.
- **Analysis implications**: Magnet-technology A/B studies are only honest when beta and the peak-field limit respond to B: at the Nb3Sn ceiling (4.69 T on axis) the Stellaris plasma reaches beta 0.099 against a 0.05 limit while LCOE falls 275 -> 198 USD/MWh, a cost-only illusion. Report both verdicts alongside LCOE in any field sweep; a beta_ok violation means the configuration cannot hold the plasma the cost model priced.
- **Status**: captured
