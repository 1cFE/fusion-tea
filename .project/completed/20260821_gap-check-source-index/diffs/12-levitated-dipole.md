# Diff: 12-levitated-dipole

**Generated:** 2026-05-22T10:06:16-07:00

## Counts

| field | baseline | new | Δ |
|-------|----------|-----|---|
| blocking_count   | 4 | 0 | -4 |
| important_count  | 8 | 5 | - |
| overall_rating   | Mostly Ready | Mostly Ready | - |

## Fleet-source citations (new only — grep `knowledge/sources/` or `PyFECONS`)

```
68:- Tritium processing and handling systems — `derivable` from D-T analogues (tea_dt_mfe_cost_analysis, PyFECONS) — important for O&M
120:| Capital cost per CAS component (absolute $) | proprietary | important | Paper uses relative costs only; derive from masses × $/tonne analogues using ARIES documentation or PyFECONS |
122:| Fixed O&M annual cost | not-yet-sourced | important | Use MFE fleet-wide analogue from tea_dt_mfe_cost_analysis or PyFECONS |
134:1. **`knowledge/sources/tea_dt_mfe_cost_analysis/`** — Read first for CAS-level cost fractions and O&M rates applicable to D-T MFE. Should provide BOP, indirect, and O&M analogues to fill the largest LCOE gaps. (not-yet-sourced for this concept; fleet-wide analogue)
136:2. **`knowledge/sources/aries_cost_account_documentation/`** — Use to map component masses to CAS accounts (CAS 21-27 direct costs). Provides $/tonne algorithms for magnet systems, vacuum vessels, blankets, and BOP. (not-yet-sourced; methodology reference)
138:3. **`/home/reid/PyFECONS`** — Apply magnet cost algorithms and LCOE calculation to the published component masses. Reactor A is comparable in magnet size to ARC class tokamaks (core magnet outer radius 7.1 m, 20.8 GJ stored energy, 4,320 km REBCO), so ARIES/PyFECONS magnet costing functions should apply. (derivable; validation cross-check)
140:4. **`knowledge/sources/revisit_of_the_2017_costing/`** — Check for modular/novel MFE costing methodology. The ARPA-E ALPHA re-costing includes some compact/non-tokamak concepts that may have useful cost methodology analogues for a novel magnet-centric concept. (not-yet-sourced; analogue)
150:Proceed to full analysis. The Simpson et al. (2026) plant study provides a sufficient parameter set for a quantitative first-pass LCOE model: net power, efficiency chain, duty cycle, component masses, and magnet replacement cadence are all published. The main modeling challenge is that absolute capital costs are not published — analysts must construct CAS-level cost estimates from published component masses using cost/tonne analogues from `tea_dt_mfe_cost_analysis`, `aries_cost_account_documentation`, or PyFECONS. The deeper physics uncertainty (confinement scaling, edge pedestal formation) should be handled via sensitivity analysis on Q_sci (range 10–20) rather than treated as a blocking gap. The back-solve to $0.01/kWh exercise will be particularly illuminating here, as the concept's economics are explicitly driven by the core magnet cost and the REBCO tape supply chain.
```

## Blocking-tier lines (baseline)

```
34:- Confinement scaling validation — `truly-unknown` (no fusion-relevant dipole data exists) — **blocking** for verifying Q=15, but design can proceed with stated assumption
55:- Confinement scaling law — `truly-unknown` — **blocking** for validating Q=15 (but stated assumption enables LCOE model construction)
113:- REBCO tape production scale-up — `not-yet-sourced` — **blocking** for supply chain assessment (search OSTI/IEEE for REBCO market analyses; industry roadmaps from SuperOx, American Superconductor, Faraday Factory)
```

## Blocking-tier lines (new)

```
(none)
```

## Full unified diff (truncated to 400 lines)

```diff
--- /tmp/gap_baselines_2026-05-22/12-levitated-dipole.md	2026-05-22 09:21:13.848013606 -0700
+++ /home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/12-levitated-dipole/gap_report.md	2026-05-22 10:06:16.831063840 -0700
@@ -1,4 +1,4 @@
-I now have enough to write the full gap assessment. Let me compile it.
+I now have comprehensive information to write the gap assessment. Let me produce the report.
 
 ---
 
@@ -6,207 +6,162 @@
 
 ## Overall Readiness
 **Rating**: Mostly Ready
-
-**Summary**: OpenStar has published one of the most detailed first-principles power plant study of any private fusion startup (arXiv 2602.20564), providing comprehensive physics, engineering, and reactor parameter data for two design points (208 MWe and 75 MWe). The primary gaps are: (1) no dollar-denominated cost data — the paper explicitly defers this to a future publication; (2) no balance-of-plant thermal cycle specification; and (3) plasma confinement scaling is genuinely unknown, leaving Q=15 unvalidated at any fusion-relevant device scale. These gaps are real but do not block a D1+ analysis — enough data exists to structure a quantitative LCOE model with transparent assumptions, with clearly flagged unknowns.
+**Summary**: This is one of the best-documented fusion startup concepts in the Phase 1a dataset, anchored by a detailed 2026 plant study (Simpson et al., arXiv 2602.20564) that includes full power balance, component masses, neutronics (OpenMC), magnet structural analysis, and TBR calculations. The concept is analysis-ready for all qualitative sections and for a quantitative LCOE model with analogue-derived costs. The primary gaps are the absence of published absolute capital costs (deliberately withheld as preliminary) and an unspecified thermal cycle — both are derivable from available data with stated assumptions.
 
 ---
 
 ## Section Coverage
 
 ### 1. Availability of Data
-**Coverage**: Rich
+**Coverage**: Good
+
+**Available**: OpenStar is exceptionally transparent by fusion startup standards. Two peer-reviewed arxiv papers (2602.20564 and 2508.17691) cover the power plant design and the Junior prototype respectively, with full technical detail. Bloomberg, IEEE Spectrum, RNZ, NucNet, and World Nuclear News provide company milestones, funding rounds, and prototype roadmap. The power plant paper is the main primary source: it contains a 0D power balance, differential evolution reactor optimization, REBCO coil FEA, OpenMC neutron transport, TBR calculations, and a full energy Sankey diagram. This is unusual depth for a FOAK concept at this stage of development.
 
-**Available**:
-- arXiv 2602.20564 (Simpson et al., 2026): Full peer-reviewed power plant study with two FOAK design points, 0D power balance, plasma equilibrium, neutron transport (OpenMC), coil FEA, material mass inventories, and quantified duty cycle. Most detailed published plant study of any MFE startup.
-- arXiv 2508.17691 (Chisholm et al., 2026): Detailed Junior prototype paper: HTS coil specs, flux pump results, plasma heating systems, first plasma results.
-- OpenStar website / news coverage (IEEE Spectrum, Bloomberg, RNZ, NucNet): Company milestones, roadmap (Junior → Tahi → Maui → Tama Nui), funding (~NZD 35M + USD 21M), headcount (~80).
-- Wikipedia / LDX heritage literature: Physics heritage and experimental record from MIT LDX (2004–2014).
-
-**Missing**:
-- No published LCOE estimates or overnight capital cost values — paper explicitly states it is "in the process of developing" this model and will publish it as future work.
-- No published balance-of-plant design (thermal cycle, cooling water systems, power conversion unit).
-- No detailed blanket engineering design (beyond Li₂O baseline with TBR 1.1).
-- No Tahi design paper (planned, per §5 of 2602.20564).
+**Missing**: Absolute capital cost numbers (deliberately not published, paper explicitly states "we avoid quoting specific values here" pending finalization of their proprietary cost model). Company financials and internal cost models are not public.
 
 **Gaps**:
-- Dollar-denominated cost model — `proprietary` (OpenStar has a preliminary model, per the paper) — **important** (needed for LCOE, can be estimated by analogy)
-- Balance-of-plant specifics — `truly-unknown` (not published anywhere) — **important** (thermal efficiency can be assumed at 40% from the paper's Table 2)
-- Confinement scaling validation — `truly-unknown` (no fusion-relevant dipole data exists) — **blocking** for verifying Q=15, but design can proceed with stated assumption
+- Absolute capital cost breakdown — `proprietary` — important (can be derived from published component masses with $/tonne analogues)
+- Specific thermal cycle (Rankine vs. sCO2) — `proprietary` — nice-to-have (40% efficiency is already stated; cycle choice affects BOP design detail but not first-pass LCOE materially)
 
 ---
 
 ### 2. Challenges in Capturing System Function
-**Coverage**: Good (challenges are well-articulated in the paper itself)
+**Coverage**: Partial
 
-**Available**:
-- Paper explicitly acknowledges the key physics unknown: energy confinement time scaling. No empirical dipole scaling law exists (unlike H-98 for tokamaks). The paper uses Bohm vs. gyro-Bohm scaling as bounding assumptions.
-- The paper notes that alpha heating in the good-curvature region "is an ongoing area of active research" and its treatment in the power balance is approximate.
-- Good-curvature alpha energy is assumed to be fully radiated — simplified assumption, explicitly flagged.
-- Edge pedestal physics is unknown ("the physics defining viable conditions at the plasma edge is not well understood") — treated with tokamak I-mode upper bounds.
-- Plasma edge conditions affect confinement and wall loading but are unbenchmarked.
-- Duty cycle model is explicitly approximate (5-min dock time is an engineering target, not a demonstrated result).
-
-**Missing**:
-- No validated confinement scaling law for dipoles. The LDX data gives one data point at low temperature — extrapolation to 10 keV spans orders of magnitude.
-- Alpha particle transport in good-curvature region is estimated, not modeled fully.
-- No system code (e.g., PROCESS) output for this concept — the optimization is done in the paper's bespoke code.
+**Available**: The Simpson et al. paper explicitly addresses the key modeling challenges. The power balance (Eq. 9–11) is fully parameterized. Energy routing through the plasma, shield, first wall, and blanket is traced in detail (Table 9, Figure 21 Sankey). The plasma physics basis — marginal interchange stability driving p ∝ R⁻²⁰/³ peaked profiles, alpha particle confinement (ASCOT5 particle tracing showing 85% deposited in bad-curvature region), bremsstrahlung losses, and radiation from the good-curvature region — is documented. The concept's inherent MHD stability and quasi-steady operation mode eliminate disruption risks and simplify some modeling assumptions. The paper also honestly flags that no validated confinement scaling law exists for dipoles, and explicitly avoids extrapolating from existing devices — instead using a reverse approach (design reactor, back-calculate what a demo device must show).
+
+**Missing**: 
+- No empirical confinement scaling law for levitated dipoles. The paper assumes Bohm-like scaling as conservative and derives a `device index` (ξ_α), but this is an engineering design constraint, not measured data. Whether the concept actually achieves Bohm or gyro-Bohm scaling is unknown until Tahi data is available (~2028).
+- Edge pedestal physics is uncharacterized. The paper assumes pedestal-like conditions at the plasma edge (T_lcfs = 790 eV, p_lcfs = 10³ Pa) analogized to I-mode tokamaks, but explicitly acknowledges "the physics defining viable conditions at the plasma edge is not well understood."
+- ICRH antenna wave propagation in dipole geometry has "greater scientific uncertainty in predicting heating performance" per the paper.
 
 **Gaps**:
-- Confinement scaling law — `truly-unknown` — **blocking** for validating Q=15 (but stated assumption enables LCOE model construction)
-- Good-curvature alpha transport — `truly-unknown` — **important** for power balance accuracy
-- Edge pedestal physics — `truly-unknown` — **important** (bounded in the model, so tractable)
-- No independent system code validation — `not-yet-sourced` — **nice-to-have** (PROCESS or similar has not been applied to this concept)
+- Confinement scaling validation — `truly-unknown` (requires Tahi data) — important (directly sets required auxiliary heating, Q_sci achievability, and efficiency of the plasma)
+- Edge pedestal physics — `truly-unknown` (requires fusion-relevant dipole experiment) — important (affects auxiliary power fraction and net electric output)
+- ICRH coupling efficiency in dipole geometry — `truly-unknown` (preliminary results from Wallace et al. 2025, referenced but not published) — important (affects recirculating power and net electric output sensitivity)
 
 ---
 
 ### 3. Maturity of Key Subsystems and Components
-**Coverage**: Partial (TRLs not formally stated, but implied by the published record)
+**Coverage**: Partial
+
+**Available**: Subsystem maturity is well-differentiated in the published literature. The core magnet is the most advanced subsystem: 5.6 T REBCO coil demonstrated in Junior (Feb 2026 levitation milestone); 23 T target for power plant designed and structurally verified with COMSOL FEA; flux pump demonstrated at 170 kJ world record; neon slush cooling concept specified with materials parameters. Neutron shielding is modeled in depth (OpenMC): W+B₄C layered structure, 475 mm thickness for Reactor A, achieving ~10 kW cryogenic heating, 1.2-year sacrificial coil lifetime. The paper compares shield performance against WB (tungsten boride) and confirms feasibility with conventional materials.
 
-**Available**:
+**Missing**: Several subsystems receive only high-level treatment in the paper because they are "not spatially constrained nor coupled to the core magnet, resulting in greatly reduced complexity and risk." This is reasonable design philosophy but leaves gaps for LCOE modeling.
 
-| Subsystem | Status | TRL (Implied) | Source |
-|-----------|--------|---------------|--------|
-| HTS core magnet (REBCO, ~5.6 T) | Demonstrated (Junior, Feb 2026) | TRL 4 | arXiv 2508.17691 |
-| On-board superconducting flux pump | Demonstrated at 170 kJ world record | TRL 4 | arXiv 2508.17691 |
-| Magnetic levitation system | Demonstrated (Feb 2026) | TRL 4 | Bloomberg, IEEE Spectrum |
-| Neon slush cryo reservoir | Conceptual design; no demonstration | TRL 2-3 | arXiv 2602.20564 §2.2.3 |
-| 23 T REBCO coil (power plant scale) | Conceptual design; Tahi targets 20 T | TRL 1-2 | arXiv 2602.20564 |
-| On-board neutron shield (W/B₄C) | Conceptual; OpenMC modeled | TRL 2 | arXiv 2602.20564 §4.3 |
-| CICC REBCO cable (30 kA) | Design concept; not manufactured | TRL 2-3 | arXiv 2602.20564 §4.1 |
-| Li₂O tritium breeding blanket | Baseline selection; no engineering design | TRL 2 | arXiv 2602.20564 §2.2.6 |
-| Reinforced concrete vacuum vessel | Conceptual design; structural engineering feasible | TRL 2-3 | arXiv 2602.20564 |
-| ICRH heating system (power plant) | Design target; Junior uses ECRH only | TRL 3 (in fusion context) | arXiv 2602.20564 §2.2.7 |
-| Sacrificial coil replacement system | Conceptual; modular dock/undock design | TRL 2 | arXiv 2602.20564 §2.3.1 |
-
-**Missing**:
-- No formal TRL assessment published by OpenStar or any external reviewer.
-- No engineering design for tritium extraction and processing system.
-- No cryogenic system engineering at power-plant scale (neon slush infrastructure).
-- Blanket cooling scheme is explicitly unspecified.
+| Subsystem | TRL | Coverage | Notes |
+|-----------|-----|----------|-------|
+| REBCO core magnet (concept) | 4 | Good | Levitation demonstrated, flux pump at prototype scale; 23 T target modeled |
+| Neutron shield (W+B₄C) | 3 | Good | OpenMC validated, thermal COMSOL model, materials specified |
+| On-board superconducting flux pump | 4 | Good | 170 kJ demonstrated in Junior |
+| Neon slush cryogenic reservoir | 3 | Partial | Concept specified with materials properties; scale-up undemonstrated |
+| ICRH heating system | 2-3 | Poor | Only concept-level in paper; antenna design for dipole geometry unsolved |
+| Tritium breeding blanket (Li₂O) | 2 | Poor | TBR=1.1 confirmed by OpenMC; cooling scheme, neutron multiplier, and module design all TBD |
+| Balance of plant (thermal cycle) | 5 (generic) | Poor | 40% efficiency assumed but cycle type (Rankine/sCO2) unspecified; use generic analogue |
+| Concrete vacuum vessel | 4 | Partial | Analogized to NASA Space Power Facility; no cost design published |
+| First wall (Inconel+W coating) | 4 | Partial | Mass specified (325 tonnes Inconel); replacement schedule addressed qualitatively |
+| Tritium processing/handling | 3 | Not addressed | Standard D-T infrastructure; rely entirely on fleet-wide analogues |
 
 **Gaps**:
-- Formal TRL assignments — `not-yet-sourced` — **nice-to-have** (can be inferred from published record)
-- Tritium processing system design — `truly-unknown` — **important** (can borrow from ITER/ARC analogues)
-- Neon supply/cryo infrastructure — `derivable` — **important** (paper flags hydrogen as an alternative if neon procurement is difficult)
-- Blanket cooling scheme — `truly-unknown` — **important** but doesn't block first-pass analysis
+- ICRH antenna design for dipole geometry — `not-yet-sourced` — important (see Wallace et al. 2025, cited but unpublished/not captured)
+- Blanket cooling scheme and neutron multiplier — `proprietary/not-yet-sourced` — nice-to-have (TBR is confirmed; blanket cost estimate requires cooling detail)
+- Tritium processing and handling systems — `derivable` from D-T analogues (tea_dt_mfe_cost_analysis, PyFECONS) — important for O&M
 
 ---
 
 ### 4. Key Materials and Supply Chain Considerations
 **Coverage**: Partial
 
-**Available**:
-- REBCO tape: Paper gives full tape mass inventory. Reactor A requires **4,320 km** of REBCO tape; Reactor B requires 2,550 km. Paper cites current-generation SuperOx tape and upcoming Faraday Factory "Mirai" REBCO (~30% improvement in engineering current density). These figures allow direct comparison to current production volumes.
-- Tungsten: Reactor A uses **1,760 tonnes** of W tiles. Large but commercially available; no fundamental scarcity issue.
-- Li₂O: Reactor A blanket requires **3,490 tonnes** Li₂O. Requires enriched Li-6 (natural Li is ~7.5% Li-6). Li-6 enrichment is a supply chain concern — global enrichment capacity is limited and primarily defense-sector.
-- B₄C shield: Reactor A requires **82.3 tonnes** — commercially available, no supply concern.
-- Inconel 718 inner vessel: 325 tonnes — commercially available.
-- Reinforced concrete outer vessel: 38,700 tonnes — no supply concern.
-- Neon (cryogen): Paper acknowledges procurement risk and flags hydrogen as alternative. Neon is a byproduct of steel production; supply is geographically concentrated.
-
-**Missing**:
-- No analysis of REBCO tape production scale-up requirements. Current global REBCO production is estimated at ~1,000–2,000 km/year; Reactor A requires 4,320 km. This is a potentially severe manufacturing bottleneck. The paper does not address this.
-- No Li-6 enrichment supply chain analysis.
-- No tritium startup inventory analysis (initial tritium load, external supply from CANDU/ITER).
+**Available**: Component material masses are published in Table 5 of Simpson et al.: 4,320 km REBCO tape, 1,760 tonnes tungsten, 82.3 tonnes B₄C, 3,490 tonnes Li₂O, 38,700 tonnes reinforced concrete, 325 tonnes Inconel 718. This mass data enables cost estimation with published material cost rates. REBCO tape degradation under neutron flux is characterized (3×10¹⁸ cm⁻² fast neutron fluence limit for 5% Ic degradation). The paper discusses tungsten recrystallization, creep mechanisms, and tile lifetime, plus B₄C tritium production from ¹⁰B(n,α)³H. Faraday Factory "Mirai" tape with >1000 A/mm² engineering Jc is referenced as a key supply chain development.
+
+**Missing**: No direct citation of current REBCO tape market pricing or production capacity. The paper notes that 4,320 km of tape is comparable to the global annual REBCO production (unverified — this comparison appears in the startup commentary sphere but is not explicitly cited). No formal supply chain risk analysis is published.
 
 **Gaps**:
-- REBCO tape production scale-up — `not-yet-sourced` — **blocking** for supply chain assessment (search OSTI/IEEE for REBCO market analyses; industry roadmaps from SuperOx, American Superconductor, Faraday Factory)
-- Li-6 enrichment capacity — `not-yet-sourced` — **important** (search for fusion Li-6 supply studies; IAEA reports)
-- Tritium startup inventory — `derivable` — **important** (can estimate from fusion power × breeding ratio × startup time using published methods e.g., Abdou et al.)
-- D supply — `derivable` — **nice-to-have** (deuterium is abundant; not a practical constraint)
+- REBCO tape cost at the required scale (4,320 km/reactor) — `not-yet-sourced` — important (dominant capital cost driver; search OSTI/Superconductor Science for current REBCO tape cost scaling, manufacturer price lists; unverified — confirm existence before searching)
+- Neon supply availability and procurement cost at plant scale — `derivable` from industrial gas market data — nice-to-have
+- B₄C tritium production (¹⁰B transmutation) — partially addressed in paper; full lifetime and disposal cost assessment — `not-yet-sourced` — nice-to-have
+- Tungsten tile manufacturing at scale (1,760 tonnes, high-purity W tiles operating at 1950 K) — `not-yet-sourced` — nice-to-have (search for tungsten tile supplier qualification data for fusion applications)
 
 ---
 
 ### 5. LCOE Parameter Extraction
-**Coverage**: Good on physics/performance parameters; zero on dollar costs
+**Coverage**: Partial
 
 **Available Parameters**:
 
 | Parameter | Value/Range | Source | Confidence |
 |-----------|-------------|--------|------------|
-| Net electric power (Reactor A) | 208 MW | arXiv 2602.20564, Table 5/9 | High |
-| Net electric power (Reactor B) | 74.5 MW | arXiv 2602.20564, Table 5/9 | High |
-| Fusion power (Reactor A) | 667 MW | arXiv 2602.20564, Table 9 | High |
-| Fusion power (Reactor B) | 237 MW | arXiv 2602.20564, Table 9 | High |
-| Thermal power (Reactor A) | 741 MW | arXiv 2602.20564, Table 9 | High |
-| Thermal conversion efficiency (η_th) | 40% (assumed) | arXiv 2602.20564, Table 2 | Medium (assumed, not specified) |
-| ICRH efficiency (η_aux) | 70% | arXiv 2602.20564, Table 2 | Medium |
-| Cryogenic system efficiency (η_cryo) | 1.25% | arXiv 2602.20564, Table 2 | Medium |
-| Auxiliary heating power (Reactor A) | 44.5 MW (electrical draw: ~63.6 MW) | arXiv 2602.20564, Table 9 | High |
-| Sci Q | 15 (assumed target) | arXiv 2602.20564, §3.3 | Low (unvalidated) |
-| Core magnet duty cycle (f_d) | 90.1% (Reactor A), 90.2% (Reactor B) | arXiv 2602.20564, Table 5 | Medium |
-| Plant availability factor | 96% | arXiv 2602.20564, Table 5 | Medium |
-| Annual maintenance downtime | <2 weeks/year | arXiv 2602.20564, §2.3 | Medium |
-| Core magnet dock time | 5 min (design target) | arXiv 2602.20564, §3.2.5 | Low |
-| Sacrificial coil lifetime | ~1 year (Reactor A), ~1.4 yr (Reactor B) | arXiv 2602.20564, Table 8 | Medium |
-| Semi-permanent coil lifetime | ~12 years (Reactor A) | arXiv 2602.20564, Table 8 | Medium |
-| First wall lifetime | ~1.3 yr outboard (W tiles) | arXiv 2602.20564, §4.3 | Medium |
-| REBCO tape mass (Reactor A) | 4,320 km / 2,560 tonnes CM | arXiv 2602.20564, Table 5 | High |
-| Outer VV mass | 38,700 tonnes reinforced concrete | arXiv 2602.20564, Table 5 | High |
-| TBR | 1.1 | arXiv 2602.20564, §3.3 | Medium |
-| Core magnet stored energy | 20.8 GJ (Reactor A) | arXiv 2602.20564, §4.1 | High |
-| First wall radius | 20.6 m (Reactor A) | arXiv 2602.20564, Table 5 | High |
-| Junior prototype cost | < $10M USD | arXiv 2508.17691 | High |
+| Net electric output | 208 MWe (A), 74.5 MWe (B) | arXiv 2602.20564 Table 5 | h |
+| Fusion power | 667 MW (A), 237 MW (B) | arXiv 2602.20564 Table 6 | h |
+| Q_sci (assumed) | 15 | arXiv 2602.20564 §3.3 | m (unvalidated; requires Tahi data) |
+| Thermal efficiency | 40% | arXiv 2602.20564 Table 2 | m (assumed; cycle unspecified) |
+| ICRH wall-plug efficiency | 70% | arXiv 2602.20564 §2.2.7 | h |
+| Cryogenic system efficiency | 1.25% | arXiv 2602.20564 Table 2 | m |
+| Duty cycle (core magnet) | 90.1% (A), 90.2% (B) | arXiv 2602.20564 Table 5 | m (model-dependent) |
+| Plant availability factor | 96% | arXiv 2602.20564 Table 5 | m |
+| Auxiliary heating power | 44.5 MW (A), 15.8 MW (B) | arXiv 2602.20564 Table 9 | m |
+| Recirculating power (ICRH electrical) | 63.6 MW (A), 22.6 MW (B) | arXiv 2602.20564 Table 9 | m |
+| Cryogenic cooling electrical load | 1.31 MW (A), 0.80 MW (B) | arXiv 2602.20564 Table 9 | m |
+| Magnet replacement cadence | ~1 yr (sacrificial), ~10 yr (permanent) | arXiv 2602.20564 §2.3.1, Table 8 | m |
+| Downtime per replacement | <2 weeks/year | arXiv 2602.20564 §2.3.1 | m |
+| REBCO tape required | 4,320 km (A), 2,550 km (B) | arXiv 2602.20564 Table 5 | m |
+| Tungsten shield mass | 1,760 tonnes (A), 1,100 tonnes (B) | arXiv 2602.20564 Table 5 | m |
+| Concrete outer vessel | 38,700 tonnes (A), 23,400 tonnes (B) | arXiv 2602.20564 Table 5 | m |
+| Li₂O blanket mass | 3,490 tonnes (A), 2,340 tonnes (B) | arXiv 2602.20564 Table 5 | m |
+| Tritium breeding ratio | 1.1 | arXiv 2602.20564 §2.2.6 | m |
+| First wall radius | 20.6 m (A), 16.9 m (B) | arXiv 2602.20564 Table 5 | h |
+| Core magnet stored energy | 20.8 GJ (A), 9.47 GJ (B) | arXiv 2602.20564 Table 7 | h |
+| Float time between docking | 45.5 min (A), 46.1 min (B) | arXiv 2602.20564 Table 7 | m |
 
 **Missing Parameters**:
 
 | Parameter | Gap Type | Criticality | Notes |
 |-----------|----------|-------------|-------|
-| Overnight capital cost ($/kW or $total) | `proprietary` | Blocking | Paper explicitly defers to future publication; preliminary model exists at OpenStar |
-| LCOE ($/MWh) | `proprietary` | Blocking | Same — OpenStar has preliminary model |
-| REBCO tape unit cost ($/m at scale) | `not-yet-sourced` | Blocking | Key cost driver; current ~$50–100/m but scale matters; search SuperPower/American Superconductor pricing |
-| Core magnet fabrication cost | `derivable` | Blocking | Can estimate from tape mass × unit cost + structural materials |
-| Vacuum vessel construction cost | `derivable` | Important | Concrete VV is unusual — analogues from large civil engineering projects |
-| Balance of plant cost | `not-yet-sourced` | Important | No BoP design exists; use generic fusion BoP fractions from ARIES/PROCESS |
-| Tritium cycle operating cost | `not-yet-sourced` | Important | Annual T₂ consumption, breeding efficiency, processing cost — use ITER/ARC analogues |
-| Thermal cycle specification | `truly-unknown` | Important | η_th=40% is assumed in model; no Rankine vs sCO₂ decision published |
-| Blanket replacement cost & schedule | `truly-unknown` | Important | No engineering design; Li₂O blanket lifetime not specified |
-| ICRH system capital cost | `not-yet-sourced` | Important | Use ITER ICRH analogues; ~44.5 MW installed, ~70% efficiency |
-| First wall replacement cost | `derivable` | Important | Tungsten tiles ~1.3 yr outboard lifetime; can estimate from W mass × unit cost |
-| Staffing/O&M cost | `not-yet-sourced` | Important | No published estimate; use fusion plant analogue (ARIES, DEMO studies) |
-| Li-6 enrichment cost | `not-yet-sourced` | Nice-to-have | Annual tritium production; Li-6 is specialty enriched material |
+| Capital cost per CAS component (absolute $) | proprietary | important | Paper uses relative costs only; derive from masses × $/tonne analogues using ARIES documentation or PyFECONS |
+| Total overnight capital cost ($) | proprietary | important | Same; back-calculate from CAS analogues |
+| Fixed O&M annual cost | not-yet-sourced | important | Use MFE fleet-wide analogue from tea_dt_mfe_cost_analysis or PyFECONS |
+| Variable O&M (REBCO tape, tungsten tiles) | derivable | important | REBCO replacement ~20% of 4,320 km tape/year × current tape price; tungsten tiles replaceable at 1 MW-yr/m² limit |
+| Specific thermal cycle type | proprietary | nice-to-have | 40% efficiency specified; assume sCO2 at this temperature range or standard steam Rankine |
+| ICRH system capital cost | not-yet-sourced | important | Novel dipole geometry; search for ITER/ARC ICRH system cost analogues (unverified — confirm existence) |
+| Plant life assumption | not-yet-sourced | important | Not stated; assume 30-40 year standard; sensitivity test |
+| Decommissioning cost | derivable | nice-to-have | Use D-T fusion fleet-wide analogue |
+| Tritium startup inventory and procurement | derivable | important | Standard D-T: ~1-2 kg startup; use fleet-wide D-T analogue |
 
 ---
 
 ## Source Recommendations
 
-1. **REBCO tape unit cost and production roadmap**: Search for market analyses from SuperPower, American Superconductor, Faraday Factory, or academic studies on HTS tape economics. Relevant search terms: "REBCO tape cost learning curve", "2G HTS tape production capacity". `unverified — confirm existence before searching`
+1. **`knowledge/sources/tea_dt_mfe_cost_analysis/`** — Read first for CAS-level cost fractions and O&M rates applicable to D-T MFE. Should provide BOP, indirect, and O&M analogues to fill the largest LCOE gaps. (not-yet-sourced for this concept; fleet-wide analogue)
 
-2. **Fusion BoP cost fractions**: ARIES and PROCESS/DEMO studies (e.g., Kovari et al., Franza et al.) provide generic BoP cost fractions (~25–40% of plant capital) that can be applied as analogues. These exist in the OSTI database. Search: "PROCESS fusion power plant cost model", "ARIES-ACT balance of plant".
+2. **`knowledge/sources/aries_cost_account_documentation/`** — Use to map component masses to CAS accounts (CAS 21-27 direct costs). Provides $/tonne algorithms for magnet systems, vacuum vessels, blankets, and BOP. (not-yet-sourced; methodology reference)
 
-3. **Li-6 enrichment supply chain**: IAEA reports on tritium and Li-6. Search IAEA PRIS or IAEA-TECDOC series. Also: Abdou et al. tritium self-sufficiency studies (several published in Nuclear Fusion journal). `unverified — confirm exact papers before citing`
+3. **`/home/reid/PyFECONS`** — Apply magnet cost algorithms and LCOE calculation to the published component masses. Reactor A is comparable in magnet size to ARC class tokamaks (core magnet outer radius 7.1 m, 20.8 GJ stored energy, 4,320 km REBCO), so ARIES/PyFECONS magnet costing functions should apply. (derivable; validation cross-check)
 
-4. **Tritium startup inventory**: Abdou et al. (2021), "Physics and technology considerations for the deuterium-tritium fuel cycle and conditions for tritium fuel self sufficiency," Nuclear Fusion — cited in the OpenStar paper as ref [58] (Sawan & Abdou 2006 version). Directly applicable for T inventory estimation.
+4. **`knowledge/sources/revisit_of_the_2017_costing/`** — Check for modular/novel MFE costing methodology. The ARPA-E ALPHA re-costing includes some compact/non-tokamak concepts that may have useful cost methodology analogues for a novel magnet-centric concept. (not-yet-sourced; analogue)
 
-5. **ICRH capital cost analogues**: ITER ICRH system documentation (ITER Design Report, CDA) provides costed subsystem breakdowns. Search ITER.org technical reports.
+5. **Wallace et al. (2025), "Ion Cyclotron Heating in a Levitated Dipole Fusion Reactor"** — Cited in 2602.20564 as in-progress but not yet captured. This paper would address ICRH coupling efficiency in dipole geometry — the key heating performance uncertainty. **Search: OSTI/arXiv for "ion cyclotron heating levitated dipole 2025 Wallace." Unverified — confirm existence before searching.**
 
-6. **Dipole confinement scaling**: No published empirical scaling law exists. The LDX papers (Boxer et al. 2010, Davis et al. 2014) are the closest available data — both cited in arXiv 2602.20564. These are the only external validation points for the confinement assumption.
+6. **Faraday Factory "Mirai" REBCO tape pricing and production roadmap** — Key supply chain data for the dominant capital cost component. Company is based in Japan. **Search Faraday Factory website, press releases, or supplier data for tape cost/km at volume. Unverified — confirm existence before searching.**
 
 ---
 
 ## Summary
 
-**Proceed to full analysis.** The OpenStar arXiv 2602.20564 paper is exceptional for a TRL 2–4 concept — it provides reactor-scale design points, detailed material inventories, quantified power balance, neutron transport, and explicit discussion of key unknowns. This is sufficient to support a D1+ analysis structured as:
-
-1. **Qualitative narrative**: Well-supported. Physics, engineering design, prototype status, roadmap, and key challenges are all publicly documented.
+Proceed to full analysis. The Simpson et al. (2026) plant study provides a sufficient parameter set for a quantitative first-pass LCOE model: net power, efficiency chain, duty cycle, component masses, and magnet replacement cadence are all published. The main modeling challenge is that absolute capital costs are not published — analysts must construct CAS-level cost estimates from published component masses using cost/tonne analogues from `tea_dt_mfe_cost_analysis`, `aries_cost_account_documentation`, or PyFECONS. The deeper physics uncertainty (confinement scaling, edge pedestal formation) should be handled via sensitivity analysis on Q_sci (range 10–20) rather than treated as a blocking gap. The back-solve to $0.01/kWh exercise will be particularly illuminating here, as the concept's economics are explicitly driven by the core magnet cost and the REBCO tape supply chain.
 
-2. **Quantitative LCOE model**: Requires analogue-based cost estimation for capital items. The key missing input is REBCO tape cost at scale (most sensitive parameter given 4,320 km for Reactor A). All performance/efficiency parameters needed for a 0D LCOE model are directly available from Table 2, Table 5, and Table 9 of the paper.
-
-3. **Back-solve to $0.01/kWh**: Feasible. The largest sensitivities are: (a) REBCO tape cost learning curve, (b) annual sacrificial coil replacement cost, (c) whether η_th can exceed the assumed 40%, and (d) whether Q=15 is achievable under Bohm-like scaling. These can all be varied parametrically.
-
-**The one structural caution**: the paper explicitly avoids quoting specific capital costs or LCOE values, and OpenStar's own cost model is described as preliminary and unpublished. Any dollar estimates in the D1+ model will be analyst-constructed analogues, not OpenStar-endorsed figures. This should be stated clearly in the analysis.
+---
 
 ## Structured summary (machine-readable)
 
 ```yaml
 overall_rating: "Mostly Ready"
-blocking_count: 4
-important_count: 8
-counting_method: "section_5_missing_parameters"
+blocking_count: 0
+important_count: 5
+counting_method: "deduplicated across all sections: (1) absolute capital costs by CAS, (2) confinement scaling law validation, (3) O&M cost structure, (4) REBCO tape cost at scale, (5) ICRH coupling efficiency in dipole geometry"
 section_coverage:
-  availability_of_data:       "Rich"
-  system_function:            "Good (challenges are well-articulated in the paper itself)"
-  subsystem_maturity:         "Partial (TRLs not formally stated, but implied by the published record)"
+  availability_of_data:       "Good"
+  system_function:            "Partial"
+  subsystem_maturity:         "Partial"
   materials_supply_chain:     "Partial"
-  lcoe_parameter_extraction:  "Good on physics/performance parameters; zero on dollar costs"
-```
+  lcoe_parameter_extraction:  "Partial"
+```
\ No newline at end of file
```

## Acceptance notes (fill during Phase 3)

- Deviation class (1-6 per plan.md): 
- Justified by fleet source? 
- Notes: 
