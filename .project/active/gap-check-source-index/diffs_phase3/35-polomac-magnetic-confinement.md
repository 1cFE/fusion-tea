# Phase 3 diff: 35-polomac-magnetic-confinement

**Generated:** 2026-05-22T16:08:00-07:00

## Counts (Phase 2 -> Phase 3 strict-read regen)

| field | phase2 | phase3 | Δ |
|-------|--------|--------|---|
| blocking_count   | 12 | 5 | -7 |
| important_count  | 6 | 4 | - |
| overall_rating   | Insufficient Data | Insufficient Data | - |

## Fleet-source dispositions in new report

```
142:- `knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`: **Integrated** as cost-analog range ($34–54/MWh for non-tokamak MFE at ~500 MWe) and as the applicable CAS methodology framework for a future PoloMac plant study. Does not resolve any current blocking gap because no PoloMac plant design exists to apply it to.
143:- `knowledge/sources/aries_cost_account_documentation/`: **Integrated** as CAS structural framework (accounts 20–27, 90–98) and escalation methodology reference. Cannot resolve concept-specific gaps without a plant design.
144:- `knowledge/meta_analysis/progress_toward_fusion_breakeven_lawson_criterion/`: **Integrated** — the absence of any dipole or PoloMac entries in this peer-reviewed Lawson compilation confirms TRL ~1–2 and the absence of publishable experimental physics results for this concept family.
145:- `knowledge/sources/a_simplified_economic_model_for_inertial_fusion/`: **Disqualified** — IFE-specific (Monte Carlo over target gain, driver efficiency, rep rate). No overlap with MFE dipole confinement economics.
146:- `knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/`: **Disqualified** — heavy-ion IFE driver economics. Entirely different confinement family and cost structure from PoloMac.
147:- `knowledge/sources/energy_from_inertial_fusion/`: **Disqualified** — comprehensive IFE review. No applicability to poloidal MFE.
148:- `knowledge/sources/accelerators_for_inertial_fusion_energy_production/`: **Disqualified** — IFE accelerator drivers only. Not applicable.
149:- `knowledge/sources/affordable_manageable_practical_and_scalable_amps_high/`: **Disqualified** — pulser-driven IFE. Not applicable.
150:- `knowledge/sources/commercialization_of_laser_fusion_energy/`: **Disqualified** — KrF laser IFE. Not applicable.
```

## Forbidden-phrase check (should be empty)

```
(none — good)
```

## First line of new report (should start with `# Gap Assessment`)

```
# Gap Assessment: PoloMac Magnetic Confinement
```

## Blocking-tier lines (new)

```
121:| Net electric power output | truly-unknown | blocking | No reactor design; 2014 paper is an electromagnetics sketch only |
122:| Capital cost (any CAS account) | truly-unknown | blocking | No plant study exists; copper-coil 700 MW ohmic loss makes 2014 design non-viable |
123:| Energy conversion efficiency / cycle type | truly-unknown | blocking | Not disclosed; D-D neutron spectrum at 2.45 MeV requires different blanket from D-T |
124:| Capacity factor / availability | truly-unknown | blocking | Steady-state claimed but no plasma confinement demonstrated |
125:| O&M costs (any component) | truly-unknown | blocking | No engineering design from which to derive maintenance schedule |
126:| Q or gain factor | truly-unknown | blocking | No experimental data; D-D condition factor 142× above D-T Lawson threshold unachieved |
127:| Magnet power recirculation fraction | truly-unknown | blocking | SC path acknowledged but not designed; copper baseline non-viable |
```

## Full unified diff (truncated to 400 lines)

```diff
--- /tmp/gap_phase2_state/35-polomac-magnetic-confinement.md	2026-05-22 12:59:21.090124400 -0700
+++ /home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/35-polomac-magnetic-confinement/gap_report.md	2026-05-22 16:08:00.852500228 -0700
@@ -1,13 +1,8 @@
-Now I have a full picture of all available sources. Let me write the gap assessment.
-
 # Gap Assessment: PoloMac Magnetic Confinement
 
 ## Overall Readiness
 **Rating**: Insufficient Data
-
-**Summary**: PoloMac (Deutelio) is a conceptual-stage magnetic confinement concept with only two technical papers (2014, 2024) and a company profile as public documentation. No plant study exists, no prototype has been built, the plasma physics has not been experimentally validated, and the core MHD and stability analyses are explicitly incomplete. No economic parameters — capital cost, O&M, energy conversion, capacity factor — can be sourced from any available material. The concept is at TRL 2–3 and has not crossed thresholds that would make quantitative LCOE analysis meaningful.
-
----
+**Summary**: PoloMac is an extremely early-stage concept backed by two technical papers (one paywalled) and a pre-prototype startup with no built hardware. The available literature establishes the magnetic design philosophy and a qualitative development roadmap but contains no experimental plasma results, no reactor-scale engineering study, no energy conversion design, and no economic data of any kind. A D1+ concept analysis cannot be responsibly produced at this time; all five assessment sections are either poor or empty.
 
 ## Section Coverage
 
@@ -15,22 +10,21 @@
 **Coverage**: Poor
 
 **Available**:
-- Elio (2014, FED) — foundational magnetic field design paper; describes coil geometry, magnetic breach shaping, and preliminary reactor-scale dimensions (plasma volume ~1300 m³, R ≈ 7.5 m, field ~2 T from copper coils). Only available as section snippets (full text paywalled).
-- Elio et al. (2024, JTSP) — full-text accessible; describes prototype design parameters, D-T and D-D Lawson criterion analysis, and development roadmap. Most substantive technical source.
-- Deutelio company profile — roadmap stages, team, competition results, funding status.
-- No external independent assessments or reviews beyond a 2024 fusion company tier list rating Deutelio C−.
+- *2024 JTSP paper* (full text): jtsp-jtsp-article-download-32-28.md — full concept description, prototype design parameters, Lawson criterion calculations for D-T and D-D conditions, development roadmap. Primary quantitative source.
+- *2014 FED paper* (abstract + snippets only — paywalled): elio-2014-fed-poloidal-confinement.md — original PoloMac proposal, 3D magnetic field analysis, plasma volume ~1300 m³, coil design at ~2 T, ohmic losses ~700 MW. Section content beyond snippets is inaccessible.
+- *Company profile*: deutelio-company-profile.md — team, seed round status, Boldbrain placement (4th, 10,000 CHF), three-step roadmap (prototype → heat generators → electric plant with SC magnets). No technical detail.
+- *JTSP abstract*: jtsp-2024-polomac-technical-report.md — confirms D-T at 3× lower field than tokamak, D-D possibility with same high field. No new content beyond full-text paper.
+- The Lawson progress compilation (`knowledge/meta_analysis/progress_toward_fusion_breakeven_lawson_criterion/`) does not include dipole or PoloMac experiments — no experimentally achieved nτE or triple product data exists for this concept or its closest relatives in the peer-reviewed physics literature. This confirms the concept has not produced publishable plasma physics results.
 
 **Missing**:
-- Independent peer review of the physics claims
-- Experimental validation at any scale
-- Any plant study or preconceptual design report
-- Detailed reactor engineering design (beyond 2014 sketches)
-- Conference papers or proceedings that may expand on the published content
+- Full text of 2014 FED paper (paywalled; Fusion Engineering and Design vol. 89, pp. 806–811)
+- Any second-generation technical publications (patent applications, conference proceedings, internal Deutelio reports)
+- Boldbrain 2024 pitch materials (likely non-technical but may contain roadmap detail)
 
 **Gaps**:
-- No plant-level engineering design study — `truly-unknown` — **blocking**: prevents any structured cost or performance analysis
-- No external/independent technical validation — `truly-unknown` — **blocking**: all physics claims are self-reported with no benchmark
-- Possible additional Deutelio materials (conference presentations, grant applications, investor materials) not captured in Phase 1a — `not-yet-sourced` — **important**
+- Paywalled 2014 FED paper limits access to foundational magnetic design analysis — not-yet-sourced — important
+- No reactor-scale design study has been published — truly-unknown (concept is pre-prototype) — blocking
+- No second-iteration publications exist as of the research period — proprietary — blocking
 
 ---
 
@@ -38,25 +32,24 @@
 **Coverage**: Poor
 
 **Available**:
-- 2024 JTSP paper explicitly states: MHD stability analysis is future work ("will be committed to plasma specialists after completing the verification of the above steps"); the custom Deutelio MHD code has not been validated against benchmarks; particle path analysis contracted to Paul Scherrer Institute but results not yet published.
-- Qualitative argument that past poloidal experiments showed no instabilities is the basis for stability confidence.
-- D-D Lawson criterion analysis is provided analytically (factor of 142 harder than D-T), with target conditions: 100–200 keV ion temperature, density ~10²¹ m⁻³, τE = 20–40 s. These conditions far exceed any demonstrated poloidal confinement performance.
-- The 2014 paper notes that the copper-coil reactor-scale design consumes 700 MW in ohmic losses from the coils — "excessive for steady operation." This fundamental power-balance problem is acknowledged but not resolved.
+- 2024 JTSP paper documents that MHD codes written for toroidal coordinates (Tokamak/Stellarator standard tools) are inapplicable to PoloMac because the azimuthal domain is discontinuous at the tunnel locations. Deutelio is developing a custom (x,y,z) 3D MHD code — results are not yet validated or published.
+- Particle path analysis is underway; systematic study contracted to Paul Scherrer Institute (Villigen, CH) — unpublished.
+- Stability analysis is explicitly deferred: "Stability analysis will be committed to plasma specialists after completing the verification of the above steps."
+- ECRH heating at 5–10 kW, 4 GHz is specified for the prototype (targeting ~100 eV hydrogen plasma). No heating method for fusion-scale operation (100–200 keV for D-D) is disclosed anywhere.
+- Magnetic tunnel concept is analytically established via 2D and 3D FEM for static field shaping; plasma interaction with tunnels under real plasma conditions is unvalidated.
 
 **Missing**:
-- Validated confinement time scaling law for the PoloMac geometry
-- MHD stability analysis (explicitly incomplete)
-- Particle loss quantification through the magnetic tunnels (PSI analysis contracted but unpublished)
-- Heating scheme capable of reaching D-D ignition temperatures (100–200 keV)
-- Resolved path from prototype (100 eV hydrogen plasma) to fusion-relevant conditions
-- Power balance analysis for the reactor (700 MW copper ohmic loss is unresolved)
+- Validated MHD equilibrium and stability analysis in PoloMac geometry
+- Systematic particle confinement and loss characterization
+- Heating and current drive scheme for fusion-scale temperatures (D-D requires ~100–200 keV)
+- Any quantitative confinement time estimate or scaling prediction
+- Assessment of null-point particle losses (acknowledged but unquantified in the 2024 JTSP paper)
 
 **Gaps**:
-- MHD stability analysis not yet completed — `truly-unknown` — **blocking**: fundamental viability of the geometry is unestablished
-- Particle loss through tunnels not quantified — `truly-unknown` — **blocking**: determines whether confinement claims are physically achievable
-- Confinement time scaling unestablished — `truly-unknown` — **blocking**: τE = 20–40 s target for D-D has no experimental or simulation basis
-- Copper-coil ohmic loss problem (700 MW) unresolved at reactor scale — `truly-unknown` — **blocking**: steady-state operation without superconductors is infeasible; superconductor path not defined
-- Heating mechanism to reach D-D temperatures (100–200 keV) not specified — `truly-unknown` — **blocking**
+- Custom MHD code for PoloMac geometry unvalidated; standard codes inapplicable — truly-unknown — blocking
+- No plasma stability analysis completed or published — truly-unknown — blocking
+- No heating method specified for fusion-scale operation — truly-unknown / proprietary — blocking
+- Particle loss rates near tunnel regions unquantified — truly-unknown — important
 
 ---
 
@@ -64,25 +57,24 @@
 **Coverage**: Poor
 
 **Available**:
-- **Magnetic tunnel coil configuration**: Conceptual design with 3D FEM magnetic field analysis completed. Analytically demonstrated field shaping is plausible. TRL ~2.
-- **Small prototype design**: Fully described (30 cm cylinder, 150 dm³ plasma, 0.2–0.3 T copper coils, ECRH at 2–8 GHz / 5–10 kW, hydrogen plasma at 100 eV). Not yet built. TRL ~3 (detailed design phase).
-- **ECRH heating**: For prototype, heating method (ECRH 5–10 kW, 4 GHz) is specified. Conventional and at low TRL for D-D scale application.
-- **Vacuum vessel**: Described for prototype (304LN steel, 400 kg). Standard technology.
+- Prototype design is detailed in 2024 JTSP paper (Table 1): plasma volume 150 dm³, B = 0.2–0.3 T, copper coils, ECRH 5–10 kW, vessel 304LN stainless. Ohmic losses 750 kW. Status as of Oct 2024: "expects to build prototype in 1 year."
+- Company profile confirms the plan: 3 years to fine-tune prototype, then heat generators, then electric plants with superconducting magnets.
+- SC magnets are acknowledged as the commercial path but no HTS/LTS selection, field targets, or engineering basis is given.
+- 2014 FED paper (snippets): reactor-scale design uses copper coils at ~2 T with 700 MW ohmic losses — clearly not a viable power plant configuration; this represents a conceptual electromagnetics study, not an engineering design.
 
 **Missing**:
-- Superconducting magnet design for commercial-scale reactor (type — HTS/LTS — not specified; current density and field requirements not designed)
-- Internal coil cooling and support structure at reactor scale (coil thermal load not analyzed; 2014 paper leaves this as future work)
-- Blanket/shielding design at any scale
-- Power conversion system (not mentioned anywhere)
-- Fueling and plasma exhaust systems
-- Maintenance and replacement scheme for the in-vessel dipole coil
+- Any experimental results (plasma confinement, tunnel performance, particle loss measurements)
+- Superconducting magnet architecture (HTS vs. LTS, field target, operating temperature)
+- First wall and blanket concept (no D-T blanket needed for D-D, but shielding design required)
+- Energy conversion system (turbine cycle, power conversion unit)
+- Maintenance and remote handling concept
+- TRL estimates for any subsystem beyond coil electromagnetics (TRL 2–3 at best)
 
 **Gaps**:
-- Superconducting magnet type and design undefined for commercial path — `proprietary`/`truly-unknown` — **blocking**: determines magnet cost and feasibility at scale
-- Blanket/shielding not designed — `truly-unknown` — **blocking**: determines both neutron handling and tritium-free D-D path feasibility
-- Power conversion system absent — `truly-unknown` — **blocking**
-- Internal coil cooling at reactor scale unresolved — `truly-unknown` — **important**
-- No prototype built yet — status `truly-unknown` until experiment runs — **important**: all TRL claims are analytical only
+- Prototype not yet built; zero experimental results — truly-unknown — blocking
+- No commercial-scale engineering design (magnet, first wall, blanket, power conversion) — truly-unknown — blocking
+- SC magnet technology and field targets unspecified — proprietary — important
+- No maintenance / RAMI assessment — truly-unknown — important
 
 ---
 
@@ -90,89 +82,85 @@
 **Coverage**: Poor
 
 **Available**:
-- D-D fuel cycle eliminates the need for lithium blanket and tritium breeding, simplifying one major supply chain concern vs. D-T concepts.
-- Prototype uses standard materials: 304LN steel, water-cooled copper coils. No supply chain issues at prototype scale.
-- Company profile confirms superconducting magnets are planned for the commercial electrical generation stage, but no specification given (HTS vs. LTS).
+- Fuel: deuterium, extracted from seawater. No supply chain concern — effectively unlimited at any plausible fusion power scale.
+- D-D does not require tritium breeding, eliminating the lithium blanket supply concern present in D-T concepts.
+- Vessel material: 304LN stainless identified for the prototype (standard, no supply concern at prototype scale).
 
 **Missing**:
-- Superconducting conductor type for commercial reactor (HTS REBCO, LTS Nb₃Sn, or other) — determines procurement risk, cost, and supply chain maturity
-- Shielding and structural material specification for high-neutron-flux D-D environment
-- Vacuum vessel material for full-scale reactor
-- First-wall material specification
-- Analysis of in-vessel coil material compatibility with plasma environment and radiation exposure
+- Neutron shielding material design (D-D generates 2.45 MeV neutrons from 50% of reactions; high-flux steady-state operation still requires substantial radiation shielding)
+- First wall material selection for steady-state D-D neutron and heat flux
+- SC conductor material (REBCO tape vs. Nb₃Sn vs. other) and associated critical material dependencies
+- Any structural material assessment at reactor scale
 
 **Gaps**:
-- HTS vs. LTS selection for reactor-scale coils — `proprietary` — **important**: REBCO HTS tape would position differently vs. LTS in cost and supply chain
-- First-wall and structural materials in D-D radiation environment — `not-yet-sourced` — **important**: D-D neutrons at 2.45 MeV are less damaging per neutron than D-T but high-flux operation still requires activation analysis; analogue sources (ARIES, Helios stellarator) could partially inform this
-- No critical material dependencies identified yet — `derivable` from MFE analogues once superconductor type is specified — **important**
+- Neutron shielding materials and design absent — truly-unknown (no reactor design exists) — important
+- SC magnet conductor and critical material dependencies unspecified — proprietary / not-yet-sourced — important
+- First wall material selection absent — truly-unknown — important
+- No supply chain or manufacturing bottleneck assessment — truly-unknown — nice-to-have (premature at this stage)
 
 ---
 
 ### 5. LCOE Parameter Extraction
-**Coverage**: Poor
-
 **Available Parameters**:
-
 | Parameter | Value/Range | Source | Confidence |
 |-----------|-------------|--------|------------|
-| Confinement family | MFE, poloidal/dipole | 2014 FED, 2024 JTSP | high |
-| Fuel cycle | D-D | 2024 JTSP | high |
-| Operation mode | Steady-state | 2024 JTSP | high |
-| Target plasma field (D-T) | 2–3 T | 2024 JTSP | low |
-| Target plasma field (D-D) | ~5–6 T (implied: "same as Tokamak") | 2024 JTSP | low |
-| Target ion temperature (D-D) | 100–200 keV | 2024 JTSP | low |
-| Target density (D-D) | ~10²¹ m⁻³ | 2024 JTSP | low |
-| Target τE (D-D) | 20–40 s | 2024 JTSP | low |
-| Beta (claimed) | 20–30% | 2014 FED | low |
-| Reactor plasma volume (2014 design) | ~1300 m³ | 2014 FED (snippet) | low |
-| Prototype plasma volume | 150 dm³ | 2024 JTSP | high |
-| Prototype magnetic field | 0.2–0.3 T | 2024 JTSP | high |
-| Copper coil ohmic losses (2014 reactor design) | 700 MW | 2014 FED (snippet) | medium |
+| Fuel (D-D from seawater) | Negligible cost | Physics knowledge | high |
+| Prototype plasma volume | 150 dm³ | jtsp-jtsp-article-download-32-28.md | high |
+| Prototype magnetic field | 0.2–0.3 T (copper coils) | jtsp-jtsp-article-download-32-28.md | high |
+| Prototype ohmic losses | 750 kW | jtsp-jtsp-article-download-32-28.md | high |
+| Conceptual reactor-scale plasma volume (2014 sketch) | ~1300 m³ | elio-2014-fed-poloidal-confinement.md (snippets) | low |
+| Conceptual reactor-scale ohmic losses (copper, not viable) | 700 MW | elio-2014-fed-poloidal-confinement.md (snippets) | low |
+| Required D-D triple product (from Lawson calc in paper) | nTτE ~142× D-T condition | jtsp-jtsp-article-download-32-28.md | medium |
+| MFE LCOE analog range (ARPA-E ALPHA, 4 non-tokamak concepts) | $34–54/MWh for ~500 MWe | knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/ | low (analog only, no PoloMac design) |
 
-**Missing Parameters**:
+The ARPA-E ALPHA revisit (`knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`) documents a costing methodology and average LCOE of $43/MWh (range $34–54/MWh) for four compact MFE concepts at ~500 MWe using a CAS framework. This provides the best available cost-analog range for a non-tokamak MFE plant but cannot be applied to PoloMac because no PoloMac reactor design exists. It would be the appropriate starting framework once a plant design is available. The ARIES Cost Account Documentation (`knowledge/sources/aries_cost_account_documentation/`) provides the CAS hierarchy (accounts 20–27 direct, 90–98 indirect) and escalation methodology that would govern any future PoloMac cost model.
 
+**Missing Parameters**:
 | Parameter | Gap Type | Criticality | Notes |
 |-----------|----------|-------------|-------|
-| Fusion power output (net electric) | truly-unknown | blocking | No plant study; no net power target specified |
-| Capital cost estimates (any subsystem) | truly-unknown | blocking | No costing performed at any level |
-| Balance of plant costs | truly-unknown | blocking | No power conversion cycle designed |
-| O&M costs | truly-unknown | blocking | No operational plant design exists |
-| Energy conversion efficiency (thermal cycle) | truly-unknown | blocking | Power conversion approach not specified |
-| Capacity factor / availability | truly-unknown | blocking | No operational experience; in-vessel coil maintenance scheme not designed |
-| Q (plasma energy gain) | truly-unknown | blocking | No burning plasma analysis; physics simulations incomplete |
-| Recirculating power fraction | truly-unknown | blocking | 700 MW ohmic losses in 2014 copper design signal severe recirculating power problem; superconducting path undefined |
-| Blanket / shielding capital cost | truly-unknown | blocking | No design exists |
-| Magnet capital cost | truly-unknown | blocking | Superconductor type not specified; no costing possible |
-| Fuel cost (D-D) | derivable | nice-to-have | D₂ fuel cost is negligible vs. other costs; easily estimated from fleet-wide sources |
-| Decommissioning cost | derivable | nice-to-have | Analogous to other steady-state MFE concepts once plant size is known |
+| Net electric power output | truly-unknown | blocking | No reactor design; 2014 paper is an electromagnetics sketch only |
+| Capital cost (any CAS account) | truly-unknown | blocking | No plant study exists; copper-coil 700 MW ohmic loss makes 2014 design non-viable |
+| Energy conversion efficiency / cycle type | truly-unknown | blocking | Not disclosed; D-D neutron spectrum at 2.45 MeV requires different blanket from D-T |
+| Capacity factor / availability | truly-unknown | blocking | Steady-state claimed but no plasma confinement demonstrated |
+| O&M costs (any component) | truly-unknown | blocking | No engineering design from which to derive maintenance schedule |
+| Q or gain factor | truly-unknown | blocking | No experimental data; D-D condition factor 142× above D-T Lawson threshold unachieved |
+| Magnet power recirculation fraction | truly-unknown | blocking | SC path acknowledged but not designed; copper baseline non-viable |
+| Blanket / first wall lifetime | truly-unknown | important | D-D neutron fluence acceptable but design absent |
+| Plant construction timeline and cost | truly-unknown | important | No design basis; ARPA-E ALPHA 3-year construction analog is speculative |
 
 ---
 
 ## Source Recommendations
 
-1. **2014 FED full text** — the available extract is paywalled snippets only; full-text access to Elio (2014, FED 89:806–811) would likely reveal the complete reactor-scale parameter table and design details. *Search: ScienceDirect or institutional access to DOI 10.1016/j.fusengdes.2014.05.013.* — `not-yet-sourced`
-
-2. **Paul Scherrer Institute particle analysis** — the 2024 paper states PSI was contracted for systematic particle path analysis. Check PSI publication database for any output from this collaboration. — `not-yet-sourced` — `unverified — confirm existence before searching`
-
-3. **Bo Lehnert INTRAP / poloidal confinement literature (1968–1982)** — the 2024 JTSP paper cites Lehnert's 1975 paper on confinement with magnetically shielded supports and the 1982 INTRAP concept. These earlier works may contain experimental performance data (even if at low beta/temperature) useful for benchmarking confinement claims. — `not-yet-sourced`
-
-4. **LDX (Levitated Dipole Experiment) publications** — the closest experimentally demonstrated analog to PoloMac physics. LDX results (MIT/Columbia, 2000s) established dipole confinement properties; cited in 2014 FED. Garnier et al. (2006) Phys. Plasmas is already referenced. Additional LDX transport and confinement papers could provide the only available proxy for confinement time scaling. — `not-yet-sourced`
-
-5. **ARIES cost account documentation** (`knowledge/sources/aries_cost_account_documentation/`) — applicable fleet-wide source for CAS structure. If a D-T PoloMac case is attempted, ARIES CAS accounts for MFE (accounts 20–27) provide the framework. Does not resolve concept-specific gaps but enables cost analog structuring.
-
-6. **TEA D-T MFE Cost Analysis** (`knowledge/sources/tea_dt_mfe_cost_analysis/`) — applicable as a D-T MFE cost analog. Could provide ballpark BOP, O&M, and magnet cost ranges as bounding estimates if the analysis is labeled as highly speculative. Not a substitute for concept-specific data.
-
-7. **Revisit of ARPA-E ALPHA costing** (`knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`) — includes novel MFE concepts costed at ~$43/MWh. Could provide rough order-of-magnitude LCOE context for early-stage MFE concepts, but should not be directly applied to PoloMac.
-
-8. **Deutelio investor materials or grant applications** — Innosuisse funding and a seed round are mentioned. Swiss national research database (SNF/Innosuisse) may have public project descriptions with technical detail. — `not-yet-sourced` — `unverified — confirm existence before searching`
+**Concept-scoped — not-yet-sourced gaps:**
+- Full text of Elio 2014, *Fusion Engineering and Design* 89:806–811 — institutional library access or author request. Contains the only published reactor-scale magnetic design analysis; the snippet version misses figures and quantitative tables. Flag as `unverified — confirm institutional access before searching`.
+- Any Deutelio conference presentations post-2024 (e.g., EPS Plasma Physics, IAEA FEC, or private investor materials) — search IAEA INIS and ResearchGate for author "F. Elio" or "Filippo Elio". Flag as `unverified — confirm existence before searching`.
+- Paul Scherrer Institute particle path analysis results — search PSI preprint server or contact PSI directly; 2024 JTSP paper states this was contracted out. Flag as `unverified — work may be in progress or not yet published`.
+- Levitated Dipole Experiment (LDX) publications on confinement scaling — LDX (MIT/Columbia, 2000s) is the closest experimental analog for dipole confinement physics. Searching OSTI or APS for LDX confinement time scaling could provide physics bounds. Not a cost source but addresses the most critical blocking gap (plasma physics unknowns).
+
+**Fleet-wide sources — integration and disqualification:**
+- `knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`: **Integrated** as cost-analog range ($34–54/MWh for non-tokamak MFE at ~500 MWe) and as the applicable CAS methodology framework for a future PoloMac plant study. Does not resolve any current blocking gap because no PoloMac plant design exists to apply it to.
+- `knowledge/sources/aries_cost_account_documentation/`: **Integrated** as CAS structural framework (accounts 20–27, 90–98) and escalation methodology reference. Cannot resolve concept-specific gaps without a plant design.
+- `knowledge/meta_analysis/progress_toward_fusion_breakeven_lawson_criterion/`: **Integrated** — the absence of any dipole or PoloMac entries in this peer-reviewed Lawson compilation confirms TRL ~1–2 and the absence of publishable experimental physics results for this concept family.
+- `knowledge/sources/a_simplified_economic_model_for_inertial_fusion/`: **Disqualified** — IFE-specific (Monte Carlo over target gain, driver efficiency, rep rate). No overlap with MFE dipole confinement economics.
+- `knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/`: **Disqualified** — heavy-ion IFE driver economics. Entirely different confinement family and cost structure from PoloMac.
+- `knowledge/sources/energy_from_inertial_fusion/`: **Disqualified** — comprehensive IFE review. No applicability to poloidal MFE.
+- `knowledge/sources/accelerators_for_inertial_fusion_energy_production/`: **Disqualified** — IFE accelerator drivers only. Not applicable.
+- `knowledge/sources/affordable_manageable_practical_and_scalable_amps_high/`: **Disqualified** — pulser-driven IFE. Not applicable.
+- `knowledge/sources/commercialization_of_laser_fusion_energy/`: **Disqualified** — KrF laser IFE. Not applicable.
+- `knowledge/sources/tea_dt_mfe_cost_analysis/`: Not opened — assessed as D-T MFE specific and applicable only once a PoloMac plant design exists. At that point it would provide BOP cost structure analogs. Not read because no PoloMac plant design exists to apply it against; reading it now would not resolve any blocking gap.
+- `knowledge/sources/overview_of_the_helios_design_a_practical_planar_coil/`: Not opened — stellarator BOP analog. Could provide steady-state MFE plant structure comparisons in future but cannot address PoloMac's pre-design-stage gaps.
+- `knowledge/sources/an_assessment_of_the_economics_of_future_electric_power/`: Not opened — historical LCOE benchmarking. Provides competitive context only; does not address any concept-specific gap.
 
 ---
 
 ## Summary
 
-**Do not proceed to full quantitative D1+ analysis.** The data is insufficient for any credible LCOE or subsystem cost analysis. The concept has no demonstrated plasma physics, no validated confinement time scaling, incomplete MHD analysis, no prototype built, and zero economic data. A qualitative analysis of the concept's theoretical differentiation (poloidal geometry, magnetic tunnel innovation, D-D pathway) and a physics-readiness assessment are feasible and would be appropriate. Quantitative LCOE work would require either (a) obtaining the full-text 2014 FED paper plus any PSI confinement analysis outputs, or (b) accepting that all numbers are fleet-wide analogs with very large uncertainty bounds — which should be explicitly labeled as such rather than treated as concept-specific estimates.
+**Do not proceed to full D1+ analysis at this time.** PoloMac (Deutelio) is pre-prototype: the hardware has not been built, no plasma confinement measurements exist, the plasma physics codes for this geometry are under development and unvalidated, and no reactor-scale design has been published. All LCOE parameters are unknown at the blocking level. The concept is rated C− in independent assessments (Kunimune fusion tier list), consistent with the extremely thin published technical corpus.
+
+The minimum prerequisites for a useful D1+ analysis are: (1) experimental plasma confinement results from the prototype, (2) validated MHD/stability analysis for the PoloMac geometry, and (3) a preliminary reactor-scale engineering study with power output and magnet technology targets. None of these exist in the current literature. The ARPA-E ALPHA cost methodology and ARIES CAS framework are available for eventual application, but cannot be meaningfully applied to a concept without a plant design.
 
-The single most productive step before analysis would be full-text access to the 2014 FED paper (currently paywalled) and a search for any LDX-derived confinement scaling that could bound the τE claims.
+Recommended action: **park this concept at Insufficient Data; revisit if Deutelio publishes prototype results or a reactor design study after ~2026–2027.**
 
 ---
 
@@ -180,9 +168,9 @@
 
 ```yaml
 overall_rating: "Insufficient Data"
-blocking_count: 12
-important_count: 6
-counting_method: "deduplicated across all sections: blocking gaps are physics/engineering fundamentals with no available data (MHD stability, particle loss, confinement scaling, heating path, copper ohmic loss, superconductor undefined, no blanket/power conversion, no capital cost, no O&M, no conversion efficiency, no capacity factor, no Q/net power); important gaps are non-blocking but material for a thorough analysis (HTS/LTS selection, first-wall materials, internal coil cooling, prototype unbuilt, PSI analysis unpublished, additional Deutelio materials not sourced)"
+blocking_count: 5
+important_count: 4
+counting_method: "all_sections_deduplicated — blocking: (1) no validated MHD/stability analysis, (2) no heating method for fusion-scale operation, (3) no experimental results from built hardware, (4) no reactor-scale engineering design, (5) no LCOE parameters of any kind (capital cost, O&M, capacity factor, Q, power output). Important: (1) 2014 FED paper paywalled, (2) SC magnet technology unspecified, (3) neutron shielding design absent, (4) energy conversion pathway unspecified."
 section_coverage:
   availability_of_data:       "Poor"
   system_function:            "Poor"
```
