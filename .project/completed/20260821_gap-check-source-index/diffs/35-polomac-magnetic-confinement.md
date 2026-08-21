# Diff: 35-polomac-magnetic-confinement

**Generated:** 2026-05-22T11:23:59-07:00

## Counts

| field | baseline | new | Δ |
|-------|----------|-----|---|
| blocking_count   | 9 | 12 | 3 |
| important_count  | 4 | 6 | - |
| overall_rating   | Insufficient Data | Insufficient Data | - |

## Fleet-source citations (new only — grep `knowledge/sources/` or `PyFECONS`)

```
161:5. **ARIES cost account documentation** (`knowledge/sources/aries_cost_account_documentation/`) — applicable fleet-wide source for CAS structure. If a D-T PoloMac case is attempted, ARIES CAS accounts for MFE (accounts 20–27) provide the framework. Does not resolve concept-specific gaps but enables cost analog structuring.
163:6. **TEA D-T MFE Cost Analysis** (`knowledge/sources/tea_dt_mfe_cost_analysis/`) — applicable as a D-T MFE cost analog. Could provide ballpark BOP, O&M, and magnet cost ranges as bounding estimates if the analysis is labeled as highly speculative. Not a substitute for concept-specific data.
165:7. **Revisit of ARPA-E ALPHA costing** (`knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`) — includes novel MFE concepts costed at ~$43/MWh. Could provide rough order-of-magnitude LCOE context for early-stage MFE concepts, but should not be directly applied to PoloMac.
```

## Blocking-tier lines (baseline)

```
29:- Full paper content for 2014 FED and 2024 JTSP — `not-yet-sourced` — **blocking**: the extracted summaries omit the technical derivations needed for any assessment beyond the abstract
51:- Plasma heating specification — `proprietary` or `truly-unknown` — **blocking**: without knowing the heating approach, the plasma physics and plant energy balance cannot be assessed
52:- Plasma confinement scaling — `truly-unknown` — **blocking**: no experimental data exists for this geometry at any scale
53:- Beta inconsistency resolution — `not-yet-sourced` — **blocking**: the two papers report fundamentally different beta values with no explanation available
54:- Power balance / Q — `truly-unknown` — **blocking**: no Q estimate exists in any available source
78:| Magnetic tunnel concept | TRL 2–3 (concept/paper design) | `not-yet-sourced` (prototype status) | blocking |
81:| Plasma heating | TRL 1 (not selected) | `truly-unknown` | blocking |
82:| D-D plasma physics | TRL 1 (no experiments) | `truly-unknown` | blocking |
130:| Fusion power output (MW) | `truly-unknown` | blocking | No plant power target published |
131:| Fusion gain Q | `truly-unknown` | blocking | No Q estimate in any source |
132:| Plasma heating power and method | `truly-unknown` | blocking | No heating approach specified |
133:| Recirculating power fraction | `derivable` | blocking | Requires Q and heating method first |
134:| Thermal conversion efficiency | `truly-unknown` | blocking | Power cycle not specified |
135:| Net electrical output (MWe) | `truly-unknown` | blocking | Requires Q, heating, conversion |
136:| Capital cost (any subsystem) | `truly-unknown` | blocking | No cost data published anywhere |
137:| First wall lifetime / replacement cost | `truly-unknown` | blocking | No design exists |
138:| Operating costs (O&M, fuel, staffing) | `truly-unknown` | blocking | No plant study |
```

## Blocking-tier lines (new)

```
31:- No plant-level engineering design study — `truly-unknown` — **blocking**: prevents any structured cost or performance analysis
32:- No external/independent technical validation — `truly-unknown` — **blocking**: all physics claims are self-reported with no benchmark
55:- MHD stability analysis not yet completed — `truly-unknown` — **blocking**: fundamental viability of the geometry is unestablished
56:- Particle loss through tunnels not quantified — `truly-unknown` — **blocking**: determines whether confinement claims are physically achievable
57:- Confinement time scaling unestablished — `truly-unknown` — **blocking**: τE = 20–40 s target for D-D has no experimental or simulation basis
58:- Copper-coil ohmic loss problem (700 MW) unresolved at reactor scale — `truly-unknown` — **blocking**: steady-state operation without superconductors is infeasible; superconductor path not defined
59:- Heating mechanism to reach D-D temperatures (100–200 keV) not specified — `truly-unknown` — **blocking**
81:- Superconducting magnet type and design undefined for commercial path — `proprietary`/`truly-unknown` — **blocking**: determines magnet cost and feasibility at scale
82:- Blanket/shielding not designed — `truly-unknown` — **blocking**: determines both neutron handling and tritium-free D-D path feasibility
83:- Power conversion system absent — `truly-unknown` — **blocking**
136:| Fusion power output (net electric) | truly-unknown | blocking | No plant study; no net power target specified |
137:| Capital cost estimates (any subsystem) | truly-unknown | blocking | No costing performed at any level |
138:| Balance of plant costs | truly-unknown | blocking | No power conversion cycle designed |
139:| O&M costs | truly-unknown | blocking | No operational plant design exists |
140:| Energy conversion efficiency (thermal cycle) | truly-unknown | blocking | Power conversion approach not specified |
141:| Capacity factor / availability | truly-unknown | blocking | No operational experience; in-vessel coil maintenance scheme not designed |
142:| Q (plasma energy gain) | truly-unknown | blocking | No burning plasma analysis; physics simulations incomplete |
143:| Recirculating power fraction | truly-unknown | blocking | 700 MW ohmic losses in 2014 copper design signal severe recirculating power problem; superconducting path undefined |
144:| Blanket / shielding capital cost | truly-unknown | blocking | No design exists |
145:| Magnet capital cost | truly-unknown | blocking | Superconductor type not specified; no costing possible |
```

## Full unified diff (truncated to 400 lines)

```diff
--- /tmp/gap_baselines_2026-05-22/35-polomac-magnetic-confinement.md	2026-05-22 09:21:13.885756699 -0700
+++ /home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/35-polomac-magnetic-confinement/gap_report.md	2026-05-22 11:23:59.246752691 -0700
@@ -1,9 +1,11 @@
+Now I have a full picture of all available sources. Let me write the gap assessment.
+
 # Gap Assessment: PoloMac Magnetic Confinement
 
 ## Overall Readiness
 **Rating**: Insufficient Data
 
-**Summary**: PoloMac (Deutelio) is a pre-prototype concept with an extremely thin published record — two technical papers (available only as abstract-level summaries in Phase 1a), a startup company profile, and competition materials. The source documents contain no cost data, no plant study, no heating or power conversion specifications, and no performance validation. A D1+ analysis is possible only as a highly speculative, analogy-driven exercise with most parameters flagged as unknown or assumed. The quantitative LCOE model required for D1+ would rest almost entirely on assumptions borrowed from other MFE concepts with no concept-specific grounding.
+**Summary**: PoloMac (Deutelio) is a conceptual-stage magnetic confinement concept with only two technical papers (2014, 2024) and a company profile as public documentation. No plant study exists, no prototype has been built, the plasma physics has not been experimentally validated, and the core MHD and stability analyses are explicitly incomplete. No economic parameters — capital cost, O&M, energy conversion, capacity factor — can be sourced from any available material. The concept is at TRL 2–3 and has not crossed thresholds that would make quantitative LCOE analysis meaningful.
 
 ---
 
@@ -13,22 +15,22 @@
 **Coverage**: Poor
 
 **Available**:
-- *Elio 2014 FED*: Foundational physics paper — basic geometry (dipole radius 5.4 m, plasma volume ~1300 m³), beta 20-30%, B-field 1.4–1.8 T, steady-state operation. Available only as an abstract-level summary; full paper content was not extracted.
-- *2024 JTSP paper*: Updated concept description — magnetic tunnels, revised beta claim (70-80%), D-T and D-D operating regimes, prototype specs (0.2-0.3 T copper coils). Again, summary-level only.
-- *Deutelio company profile*: Development roadmap, team, seed round stage, Innosuisse support, 2030 energy vision.
-- *Boldbrain 2024*: Placement (4th), prize (10,000 CHF) — no technical content.
-- *Fusion company tier list*: Rated C− (kunimune.blog 2024) — editorial only.
+- Elio (2014, FED) — foundational magnetic field design paper; describes coil geometry, magnetic breach shaping, and preliminary reactor-scale dimensions (plasma volume ~1300 m³, R ≈ 7.5 m, field ~2 T from copper coils). Only available as section snippets (full text paywalled).
+- Elio et al. (2024, JTSP) — full-text accessible; describes prototype design parameters, D-T and D-D Lawson criterion analysis, and development roadmap. Most substantive technical source.
+- Deutelio company profile — roadmap stages, team, competition results, funding status.
+- No external independent assessments or reviews beyond a 2024 fusion company tier list rating Deutelio C−.
 
 **Missing**:
-- Full text of either technical paper (full methodology, assumptions, derivations)
-- Any plant study or reactor design study
-- Any peer-reviewed or independent validation of the concept
-- Conference presentations, poster materials, or preprints beyond the two papers
+- Independent peer review of the physics claims
+- Experimental validation at any scale
+- Any plant study or preconceptual design report
+- Detailed reactor engineering design (beyond 2014 sketches)
+- Conference papers or proceedings that may expand on the published content
 
 **Gaps**:
-- Full paper content for 2014 FED and 2024 JTSP — `not-yet-sourced` — **blocking**: the extracted summaries omit the technical derivations needed for any assessment beyond the abstract
-- Beta inconsistency (20-30% in 2014 vs. 70-80% in 2024) is unexplained — `not-yet-sourced` — **important**: this is a 3-5x discrepancy in a key performance parameter
-- No independent validation or review of the concept — `truly-unknown` — **important**: Deutelio is the only source for all technical claims
+- No plant-level engineering design study — `truly-unknown` — **blocking**: prevents any structured cost or performance analysis
+- No external/independent technical validation — `truly-unknown` — **blocking**: all physics claims are self-reported with no benchmark
+- Possible additional Deutelio materials (conference presentations, grant applications, investor materials) not captured in Phase 1a — `not-yet-sourced` — **important**
 
 ---
 
@@ -36,22 +38,25 @@
 **Coverage**: Poor
 
 **Available**:
-- High-level concept description: poloidal confinement, magnetic tunnel supports for internal dipole coil, steady-state D-D operation claimed
-- Qualitative design intent distinguishing PoloMac from levitated dipole (LDX) and tokamaks
+- 2024 JTSP paper explicitly states: MHD stability analysis is future work ("will be committed to plasma specialists after completing the verification of the above steps"); the custom Deutelio MHD code has not been validated against benchmarks; particle path analysis contracted to Paul Scherrer Institute but results not yet published.
+- Qualitative argument that past poloidal experiments showed no instabilities is the basis for stability confidence.
+- D-D Lawson criterion analysis is provided analytically (factor of 142 harder than D-T), with target conditions: 100–200 keV ion temperature, density ~10²¹ m⁻³, τE = 20–40 s. These conditions far exceed any demonstrated poloidal confinement performance.
+- The 2014 paper notes that the copper-coil reactor-scale design consumes 700 MW in ohmic losses from the coils — "excessive for steady operation." This fundamental power-balance problem is acknowledged but not resolved.
 
 **Missing**:
-- Plasma heating method: completely unspecified. D-D requires plasma temperatures of ~500 keV (roughly 10× D-T ignition temperature), making heating the most critical undefined subsystem.
-- Plasma confinement time and energy confinement scaling: no published confinement data, no scaling law derived for this geometry
-- Stability analysis: no published MHD stability results for the magnetic tunnel configuration
-- Power balance / Q projections: no fusion gain estimates in available sources
-- Energy conversion pathway: no specification of thermal cycle type, coolant, or BOP design
-- Magnetic tunnel physics: the core innovation is described conceptually but no detailed field topology, plasma boundary, or coil geometry is published in the extracted summaries
+- Validated confinement time scaling law for the PoloMac geometry
+- MHD stability analysis (explicitly incomplete)
+- Particle loss quantification through the magnetic tunnels (PSI analysis contracted but unpublished)
+- Heating scheme capable of reaching D-D ignition temperatures (100–200 keV)
+- Resolved path from prototype (100 eV hydrogen plasma) to fusion-relevant conditions
+- Power balance analysis for the reactor (700 MW copper ohmic loss is unresolved)
 
 **Gaps**:
-- Plasma heating specification — `proprietary` or `truly-unknown` — **blocking**: without knowing the heating approach, the plasma physics and plant energy balance cannot be assessed
-- Plasma confinement scaling — `truly-unknown` — **blocking**: no experimental data exists for this geometry at any scale
-- Beta inconsistency resolution — `not-yet-sourced` — **blocking**: the two papers report fundamentally different beta values with no explanation available
-- Power balance / Q — `truly-unknown` — **blocking**: no Q estimate exists in any available source
+- MHD stability analysis not yet completed — `truly-unknown` — **blocking**: fundamental viability of the geometry is unestablished
+- Particle loss through tunnels not quantified — `truly-unknown` — **blocking**: determines whether confinement claims are physically achievable
+- Confinement time scaling unestablished — `truly-unknown` — **blocking**: τE = 20–40 s target for D-D has no experimental or simulation basis
+- Copper-coil ohmic loss problem (700 MW) unresolved at reactor scale — `truly-unknown` — **blocking**: steady-state operation without superconductors is infeasible; superconductor path not defined
+- Heating mechanism to reach D-D temperatures (100–200 keV) not specified — `truly-unknown` — **blocking**
 
 ---
 
@@ -59,50 +64,47 @@
 **Coverage**: Poor
 
 **Available**:
-- Prototype plan: small device with water-cooled copper coils (0.2-0.3 T) to validate magnetic tunnel concept — hydrogen plasma only, no fusion
-- Commercial path described: step from prototype → D-D heat generators → SC-magnet electrical plants
-- Company founded ~2022, seed round stage as of 2024
+- **Magnetic tunnel coil configuration**: Conceptual design with 3D FEM magnetic field analysis completed. Analytically demonstrated field shaping is plausible. TRL ~2.
+- **Small prototype design**: Fully described (30 cm cylinder, 150 dm³ plasma, 0.2–0.3 T copper coils, ECRH at 2–8 GHz / 5–10 kW, hydrogen plasma at 100 eV). Not yet built. TRL ~3 (detailed design phase).
+- **ECRH heating**: For prototype, heating method (ECRH 5–10 kW, 4 GHz) is specified. Conventional and at low TRL for D-D scale application.
+- **Vacuum vessel**: Described for prototype (304LN steel, 400 kg). Standard technology.
 
 **Missing**:
-- Whether the prototype has been built or operated (no experimental results in any source)
-- TRL of any subsystem beyond the coil concept (design on paper)
-- Superconducting magnet path (HTS vs. LTS) for commercial scale — completely unspecified
-- Plasma-facing component design: no wall material, geometry, or heat flux specification
-- D-D plasma heating hardware: no technology selected
-- Shielding design: D-D neutron shielding differs from D-T but specific design absent
+- Superconducting magnet design for commercial-scale reactor (type — HTS/LTS — not specified; current density and field requirements not designed)
+- Internal coil cooling and support structure at reactor scale (coil thermal load not analyzed; 2014 paper leaves this as future work)
+- Blanket/shielding design at any scale
+- Power conversion system (not mentioned anywhere)
+- Fueling and plasma exhaust systems
+- Maintenance and replacement scheme for the in-vessel dipole coil
 
 **Gaps**:
-
-| Subsystem | Estimated TRL | Gap Type | Criticality |
-|-----------|--------------|----------|-------------|
-| Magnetic tunnel concept | TRL 2–3 (concept/paper design) | `not-yet-sourced` (prototype status) | blocking |
-| Internal dipole coil (resistive) | TRL 3–4 (prototype planned) | `proprietary` | important |
-| SC magnets for commercial | TRL 1–2 (not yet specified) | `truly-unknown` | important |
-| Plasma heating | TRL 1 (not selected) | `truly-unknown` | blocking |
-| D-D plasma physics | TRL 1 (no experiments) | `truly-unknown` | blocking |
-| Vacuum vessel / first wall | TRL 1–2 (conceptual) | `not-yet-sourced` | important |
-| Power conversion | TRL 1 (not specified) | `truly-unknown` | important |
+- Superconducting magnet type and design undefined for commercial path — `proprietary`/`truly-unknown` — **blocking**: determines magnet cost and feasibility at scale
+- Blanket/shielding not designed — `truly-unknown` — **blocking**: determines both neutron handling and tritium-free D-D path feasibility
+- Power conversion system absent — `truly-unknown` — **blocking**
+- Internal coil cooling at reactor scale unresolved — `truly-unknown` — **important**
+- No prototype built yet — status `truly-unknown` until experiment runs — **important**: all TRL claims are analytical only
 
 ---
 
 ### 4. Key Materials and Supply Chain Considerations
-**Coverage**: Partial (some inferences possible; no concept-specific data)
+**Coverage**: Poor
 
 **Available**:
-- D-D fuel: deuterium is abundant, commercially available, no supply concern
-- No tritium breeding blanket required (D-D cycle) — eliminates Li-6, tritium handling, and breeding infrastructure costs
-- Resistive copper coils for prototype: no supply concern
+- D-D fuel cycle eliminates the need for lithium blanket and tritium breeding, simplifying one major supply chain concern vs. D-T concepts.
+- Prototype uses standard materials: 304LN steel, water-cooled copper coils. No supply chain issues at prototype scale.
+- Company profile confirms superconducting magnets are planned for the commercial electrical generation stage, but no specification given (HTS vs. LTS).
 
 **Missing**:
-- SC magnet material path: if HTS (REBCO tape) is chosen for commercial scale, supply chain constraints are the same as for HTS tokamaks — but Deutelio has not specified this
-- Internal coil cooling and support structure materials: unique geometry may require novel structural materials in a high-radiation environment
-- Shielding material specification: D-D neutron flux is lower energy than D-T but still significant at commercial scale
-- First wall and plasma-facing component materials: not specified
+- Superconducting conductor type for commercial reactor (HTS REBCO, LTS Nb₃Sn, or other) — determines procurement risk, cost, and supply chain maturity
+- Shielding and structural material specification for high-neutron-flux D-D environment
+- Vacuum vessel material for full-scale reactor
+- First-wall material specification
+- Analysis of in-vessel coil material compatibility with plasma environment and radiation exposure
 
 **Gaps**:
-- SC magnet material selection — `proprietary` — **important**: REBCO vs. LTS vs. resistive determines a major cost driver and supply chain exposure
-- Radiation-tolerant structural materials for internal coil support — `truly-unknown` — **important**: the magnetic tunnel geometry places structural supports inside the plasma volume — a novel engineering challenge with no published design
-- First wall material — `truly-unknown` — **nice-to-have** at this stage
+- HTS vs. LTS selection for reactor-scale coils — `proprietary` — **important**: REBCO HTS tape would position differently vs. LTS in cost and supply chain
+- First-wall and structural materials in D-D radiation environment — `not-yet-sourced` — **important**: D-D neutrons at 2.45 MeV are less damaging per neutron than D-T but high-flux operation still requires activation analysis; analogue sources (ARIES, Helios stellarator) could partially inform this
+- No critical material dependencies identified yet — `derivable` from MFE analogues once superconductor type is specified — **important**
 
 ---
 
@@ -113,73 +115,78 @@
 
 | Parameter | Value/Range | Source | Confidence |
 |-----------|-------------|--------|------------|
-| Plasma volume | ~1300 m³ | Elio 2014 FED | medium |
-| Dipole radius | 5.4 m | Elio 2014 FED | medium |
-| Magnetic field (D-T) | 1.4–1.8 T | Elio 2014 FED | medium |
-| Beta | 20-30% (2014) / 70-80% (2024) | Both papers | low (inconsistent) |
-| Operation mode | Steady-state | Both papers | high |
-| Fuel | D-D | Both papers | high |
-| Tritium breeding needed | No | D-D physics | high |
-| Magnet type (prototype) | Resistive copper | 2024 JTSP | high |
-| Prototype B-field | 0.2–0.3 T | 2024 JTSP | high |
+| Confinement family | MFE, poloidal/dipole | 2014 FED, 2024 JTSP | high |
+| Fuel cycle | D-D | 2024 JTSP | high |
+| Operation mode | Steady-state | 2024 JTSP | high |
+| Target plasma field (D-T) | 2–3 T | 2024 JTSP | low |
+| Target plasma field (D-D) | ~5–6 T (implied: "same as Tokamak") | 2024 JTSP | low |
+| Target ion temperature (D-D) | 100–200 keV | 2024 JTSP | low |
+| Target density (D-D) | ~10²¹ m⁻³ | 2024 JTSP | low |
+| Target τE (D-D) | 20–40 s | 2024 JTSP | low |
+| Beta (claimed) | 20–30% | 2014 FED | low |
+| Reactor plasma volume (2014 design) | ~1300 m³ | 2014 FED (snippet) | low |
+| Prototype plasma volume | 150 dm³ | 2024 JTSP | high |
+| Prototype magnetic field | 0.2–0.3 T | 2024 JTSP | high |
+| Copper coil ohmic losses (2014 reactor design) | 700 MW | 2014 FED (snippet) | medium |
 
 **Missing Parameters**:
 
 | Parameter | Gap Type | Criticality | Notes |
 |-----------|----------|-------------|-------|
-| Fusion power output (MW) | `truly-unknown` | blocking | No plant power target published |
-| Fusion gain Q | `truly-unknown` | blocking | No Q estimate in any source |
-| Plasma heating power and method | `truly-unknown` | blocking | No heating approach specified |
-| Recirculating power fraction | `derivable` | blocking | Requires Q and heating method first |
-| Thermal conversion efficiency | `truly-unknown` | blocking | Power cycle not specified |
-| Net electrical output (MWe) | `truly-unknown` | blocking | Requires Q, heating, conversion |
-| Capital cost (any subsystem) | `truly-unknown` | blocking | No cost data published anywhere |
-| First wall lifetime / replacement cost | `truly-unknown` | blocking | No design exists |
-| Operating costs (O&M, fuel, staffing) | `truly-unknown` | blocking | No plant study |
-| Capacity factor | `derivable` | important | Steady-state claimed; can assume ~85% as generic MFE proxy |
-| Magnetic field (commercial D-D) | `not-yet-sourced` | important | 2024 paper implies same field as tokamak for D-D; ~5–7 T possible |
-| SC magnet cost (commercial) | `derivable` | important | Requires material choice; analogy to HTS tokamak possible |
-| Blanket/shielding cost | `derivable` | important | D-D neutron shielding — analogy to D-T with scaling factor |
+| Fusion power output (net electric) | truly-unknown | blocking | No plant study; no net power target specified |
+| Capital cost estimates (any subsystem) | truly-unknown | blocking | No costing performed at any level |
+| Balance of plant costs | truly-unknown | blocking | No power conversion cycle designed |
+| O&M costs | truly-unknown | blocking | No operational plant design exists |
+| Energy conversion efficiency (thermal cycle) | truly-unknown | blocking | Power conversion approach not specified |
+| Capacity factor / availability | truly-unknown | blocking | No operational experience; in-vessel coil maintenance scheme not designed |
+| Q (plasma energy gain) | truly-unknown | blocking | No burning plasma analysis; physics simulations incomplete |
+| Recirculating power fraction | truly-unknown | blocking | 700 MW ohmic losses in 2014 copper design signal severe recirculating power problem; superconducting path undefined |
+| Blanket / shielding capital cost | truly-unknown | blocking | No design exists |
+| Magnet capital cost | truly-unknown | blocking | Superconductor type not specified; no costing possible |
+| Fuel cost (D-D) | derivable | nice-to-have | D₂ fuel cost is negligible vs. other costs; easily estimated from fleet-wide sources |
+| Decommissioning cost | derivable | nice-to-have | Analogous to other steady-state MFE concepts once plant size is known |
 
 ---
 
 ## Source Recommendations
 
-1. **Full text of Elio 2014 FED paper** (DOI: 10.1016/j.fusengdes.2014.04.013) — `not-yet-sourced` — This is paywalled on ScienceDirect. The Phase 1a extraction only captured abstract-level content. Obtaining the full paper may clarify the beta derivation, reactor geometry details, and any power balance analysis. *Search ScienceDirect or request via institutional access.*
+1. **2014 FED full text** — the available extract is paywalled snippets only; full-text access to Elio (2014, FED 89:806–811) would likely reveal the complete reactor-scale parameter table and design details. *Search: ScienceDirect or institutional access to DOI 10.1016/j.fusengdes.2014.05.013.* — `not-yet-sourced`
 
-2. **Full text of 2024 JTSP paper** (DOI: 10.31281/med9bh43) — `not-yet-sourced` — Licensed CC-BY 4.0, so it should be freely accessible. The Phase 1a extraction captured only a summary. Full text may contain more detailed specifications, prototype design, and any power estimates. *Direct download from jtsp.eu.*
+2. **Paul Scherrer Institute particle analysis** — the 2024 paper states PSI was contracted for systematic particle path analysis. Check PSI publication database for any output from this collaboration. — `not-yet-sourced` — `unverified — confirm existence before searching`
 
-3. **Swiss Startup Association interview with Francesco Elio (2025-03-03)** — `not-yet-sourced` — The company profile references this URL. May contain roadmap details, funding status, and technology descriptions in lay language that could resolve some gaps. *Fetch directly; URL is in company profile.*
+3. **Bo Lehnert INTRAP / poloidal confinement literature (1968–1982)** — the 2024 JTSP paper cites Lehnert's 1975 paper on confinement with magnetically shielded supports and the 1982 INTRAP concept. These earlier works may contain experimental performance data (even if at low beta/temperature) useful for benchmarking confinement claims. — `not-yet-sourced`
 
-4. **Boldbrain 2024 competition materials** — `not-yet-sourced` — `unverified — confirm existence before searching`. Competition slide decks sometimes contain more technical detail than company websites. May be on the Boldbrain website.
+4. **LDX (Levitated Dipole Experiment) publications** — the closest experimentally demonstrated analog to PoloMac physics. LDX results (MIT/Columbia, 2000s) established dipole confinement properties; cited in 2014 FED. Garnier et al. (2006) Phys. Plasmas is already referenced. Additional LDX transport and confinement papers could provide the only available proxy for confinement time scaling. — `not-yet-sourced`
 
-5. **Levitated dipole / LDX literature** — `not-yet-sourced` — Since PoloMac is a variant of levitated dipole, published work on LDX (MIT/Columbia) provides the closest physics analogues: confinement scaling, beta behavior, heating approaches. These can ground LCOE parameter estimates where Deutelio-specific data is absent. *Search OSTI or Google Scholar for "levitated dipole" or "LDX" fusion.*
+5. **ARIES cost account documentation** (`knowledge/sources/aries_cost_account_documentation/`) — applicable fleet-wide source for CAS structure. If a D-T PoloMac case is attempted, ARIES CAS accounts for MFE (accounts 20–27) provide the framework. Does not resolve concept-specific gaps but enables cost analog structuring.
 
-6. **Dipole confinement cost analogues** — `derivable` — No plant study exists for PoloMac or any levitated dipole concept. The 2014 FED paper may discuss reactor size parameters that allow rough capital cost estimation by analogy with tokamak ARIES studies, scaled for the different geometry. Flag all such estimates as first-order analogues with ±50% uncertainty.
+6. **TEA D-T MFE Cost Analysis** (`knowledge/sources/tea_dt_mfe_cost_analysis/`) — applicable as a D-T MFE cost analog. Could provide ballpark BOP, O&M, and magnet cost ranges as bounding estimates if the analysis is labeled as highly speculative. Not a substitute for concept-specific data.
 
-7. **Direct contact with Deutelio** — For a company this early-stage and this opaque, direct outreach may be the only path to heating method, prototype status, and commercial design intent. Not a research search — a stakeholder engagement question.
+7. **Revisit of ARPA-E ALPHA costing** (`knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`) — includes novel MFE concepts costed at ~$43/MWh. Could provide rough order-of-magnitude LCOE context for early-stage MFE concepts, but should not be directly applied to PoloMac.
+
+8. **Deutelio investor materials or grant applications** — Innosuisse funding and a seed round are mentioned. Swiss national research database (SNF/Innosuisse) may have public project descriptions with technical detail. — `not-yet-sourced` — `unverified — confirm existence before searching`
 
 ---
 
 ## Summary
 
-**Do not proceed to full D1+ analysis with current sources alone.**
+**Do not proceed to full quantitative D1+ analysis.** The data is insufficient for any credible LCOE or subsystem cost analysis. The concept has no demonstrated plasma physics, no validated confinement time scaling, incomplete MHD analysis, no prototype built, and zero economic data. A qualitative analysis of the concept's theoretical differentiation (poloidal geometry, magnetic tunnel innovation, D-D pathway) and a physics-readiness assessment are feasible and would be appropriate. Quantitative LCOE work would require either (a) obtaining the full-text 2014 FED paper plus any PSI confinement analysis outputs, or (b) accepting that all numbers are fleet-wide analogs with very large uncertainty bounds — which should be explicitly labeled as such rather than treated as concept-specific estimates.
 
-The two extracted source documents are abstract-level summaries; the full papers — particularly the CC-BY 2024 JTSP paper — should be retrieved first. The 2024 JTSP full text is freely available and is the single highest-priority action before analysis. The 2014 FED full text would be the second priority.
+The single most productive step before analysis would be full-text access to the 2014 FED paper (currently paywalled) and a search for any LDX-derived confinement scaling that could bound the τE claims.
 
-Even with full papers in hand, PoloMac will be a "Limited/Opaque" rated concept. The quantitative LCOE model will necessarily be an analogy exercise borrowing from LDX and generic MFE plant studies, with the following parameters entirely assumed: Q, heating power, net electrical output, thermal efficiency, capital costs by subsystem, and O&M. All must be flagged explicitly as assumed, with broad uncertainty ranges (±50–100%). The concept's primary analytic value at D1+ stage is characterizing *what would need to be true* for the concept to be viable, not producing a grounded cost estimate.
+---
 
 ## Structured summary (machine-readable)
 
 ```yaml
 overall_rating: "Insufficient Data"
-blocking_count: 9
-important_count: 4
-counting_method: "section_5_missing_parameters"
+blocking_count: 12
+important_count: 6
+counting_method: "deduplicated across all sections: blocking gaps are physics/engineering fundamentals with no available data (MHD stability, particle loss, confinement scaling, heating path, copper ohmic loss, superconductor undefined, no blanket/power conversion, no capital cost, no O&M, no conversion efficiency, no capacity factor, no Q/net power); important gaps are non-blocking but material for a thorough analysis (HTS/LTS selection, first-wall materials, internal coil cooling, prototype unbuilt, PSI analysis unpublished, additional Deutelio materials not sourced)"
 section_coverage:
   availability_of_data:       "Poor"
   system_function:            "Poor"
   subsystem_maturity:         "Poor"
-  materials_supply_chain:     "Partial (some inferences possible; no concept-specific data)"
+  materials_supply_chain:     "Poor"
   lcoe_parameter_extraction:  "Poor"
-```
+```
\ No newline at end of file
```

## Acceptance notes (fill during Phase 3)

- Deviation class (1-6 per plan.md): 
- Justified by fleet source? 
- Notes: 
