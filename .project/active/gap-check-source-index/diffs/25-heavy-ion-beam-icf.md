# Diff: 25-heavy-ion-beam-icf

**Generated:** 2026-05-22T10:57:50-07:00

## Counts

| field | baseline | new | Δ |
|-------|----------|-----|---|
| blocking_count   | 2 | 0 | -2 |
| important_count  | 6 | 9 | - |
| overall_rating   | Mostly Ready | Mostly Ready | - |

## Fleet-source citations (new only — grep `knowledge/sources/` or `PyFECONS`)

```
22:- Parametric COE model: Meier et al. 1986 (LLNL/UCRL-94335) at `knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/` — three-part capital cost model (reactor + driver + target factory), COE formula with explicit financial assumptions.
32:- Modern (post-2000) HIF plant design study — `not-yet-sourced` — **important** (PyFECONS IFE modules and ARIES cost framework may serve as partial substitutes)
140:| Full CAS-structured breakdown (CAS 20-27) | not-yet-sourced | important | Only three-part model exists (reactor/driver/factory); PyFECONS IFE module likely has CAS mapping |
150:3. **PyFECONS IFE modules** (`/home/reid/PyFECONS`) — this codebase likely implements driver cost scaling and IFE-specific CAS mapping that could translate Meier 1986 formulas into a modern CAS structure and update dollar figures via built-in escalation. Directly applicable for CAS-structured cost gap.
154:5. **Hawker 2020 IFE LCOE model** (`knowledge/sources/a_simplified_economic_model_for_inertial_fusion/`) — the 14-parameter technology-agnostic IFE LCOE model directly applicable to HIF. Provides methodology for handling missing parameters (gain, target cost, rep rate sensitivity). Already in the repo — read for LCOE methodology section.
156:6. **ARIES cost accounts** (`knowledge/sources/aries_cost_account_documentation/`) — provides the CAS hierarchy (accounts 20-27) that can structure the three-part Meier cost model into a full CAS breakdown for cross-concept comparability.
162:The analysis can proceed to D1+ without additional source acquisition. The concept is exceptionally well-documented for a pre-commercial fusion approach: two full power plant designs (HIBALL, HYLIFE-II), a parametric economic model (Meier 1986), and multi-source confirmation of key physics parameters. The primary analytical work required is: (1) inflating 1986/1990s cost figures to contemporary dollars using CEPCI or GDP deflator, (2) mapping the Meier three-part cost model onto the CAS hierarchy using ARIES accounts (both sources already in the repo), (3) selecting a capacity factor assumption (~75-85%) with explicit justification, and (4) noting throughout that no current company exists and all design-choice parameters (blanket type, conversion cycle) reflect historical national lab selections rather than a committed design. PyFECONS IFE modules should be consulted before writing the capital cost section to avoid re-deriving what's already implemented.
```

## Blocking-tier lines (baseline)

```
49:- Final focus / beam transport cost uncertainty — `not-yet-sourced` — **blocking** (search LBNL HIF program reports; this is the key physics gap between current experiments and power plant)
70:- Target fabrication manufacturing TRL and cost — `not-yet-sourced` — **blocking** for LCOE (this is likely the largest unknown cost item; search NIF/IFE target fabrication cost studies as analogue)
121:| Target fabrication cost (per target, at scale) | not-yet-sourced | blocking | Likely the largest single unknown O&M cost; NIF target cost analogue is ~$1-10/target at scale, but HIF targets are simpler |
122:| Capital cost breakdown by CAS subsystem | not-yet-sourced | blocking | HYLIFE-II final report likely contains this detail; our sources are summaries only — read OSTI 7021072 directly |
```

## Blocking-tier lines (new)

```
(none)
```

## Full unified diff (truncated to 400 lines)

```diff
--- /tmp/gap_baselines_2026-05-22/25-heavy-ion-beam-icf.md	2026-05-22 09:21:13.872585162 -0700
+++ /home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/25-heavy-ion-beam-icf/gap_report.md	2026-05-22 10:57:50.427229740 -0700
@@ -1,9 +1,12 @@
+I have sufficient information to write the assessment. The OSTI source (osti-servlets-purl-901970) is Z-IFE (z-pinch), not HIF — useful as an IFE BOP/power-conversion analog. The Giegerich source covers Li-6 enrichment supply chain, directly relevant to HIF tritium breeding.
+
+---
+
 # Gap Assessment: Heavy Ion Beam ICF (D-T)
 
 ## Overall Readiness
 **Rating**: Mostly Ready
-
-**Summary**: Heavy ion beam ICF is unusually well-documented for a pre-commercial concept, owing to two detailed national lab power plant studies (HIBALL 1985, HYLIFE-II ~1994) that include costed subsystem breakdowns and LCOE estimates. The fundamental physics and cost structure are characterizable from open literature. The primary limitation is that the assigned company ("Intensity Energy") is almost certainly a placeholder — no commercial actor exists — meaning any analysis describes the national lab/academic program rather than a specific company's design. Data gaps are physics-uncertainty gaps, not data-availability gaps.
+**Summary**: Heavy ion beam ICF is exceptionally well-characterized in the published literature relative to most emerging fusion concepts — two detailed power plant designs (HIBALL, HYLIFE-II) and a parametric economic model (Meier 1986, LLNL) exist from sustained national lab programs. The primary limitations are that all primary cost and design data is 35-40 years old, no private company is actively developing this approach (making company-specific design choices unresolvable), and subsystem TRL data must be assembled from component-level sources rather than any systematic assessment. A D1+ analysis can proceed with clear confidence bounds on the data vintage.
 
 ---
 
@@ -13,42 +16,43 @@
 **Coverage**: Good
 
 **Available**:
-- Two full power plant design studies with cost estimates: HIBALL (KfK-3202, 1985) and HYLIFE-II (OSTI 7021072, ~1994). Both include engineering layouts, subsystem designs, and LCOE calculations.
-- A 2020 academic review (arxiv 2005.07520) synthesizing driver efficiency, rep rate requirements, and target gain parameters across the HIF literature.
-- Active experimental platforms: NDCX-II (LBNL) and FAIR/SIS100 (GSI) provide current-program context.
-- FIA 2025 survey of 53 companies confirms no private HIF actor exists.
+- Two complete power plant conceptual designs: HIBALL (KfK-3202, 1985) and HYLIFE-II (OSTI 7021072, early 1990s), both with subsystem descriptions, cost estimates, and performance parameters. `iter-01/sources/hif-technology-overview.md` compiles key parameters from these.
+- HIF physics review (arxiv 1511.06508, 2015): driver efficiency, target gain requirements, implosion physics, RT instability treatment.
+- Driver and target parameter confirmation: rep rate, beam energy, driver efficiency confirmed across multiple sources (arxiv 2005.07520 cited in dossier, hif-recent-research-compilation.md).
+- Parametric COE model: Meier et al. 1986 (LLNL/UCRL-94335) at `knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/` — three-part capital cost model (reactor + driver + target factory), COE formula with explicit financial assumptions.
+- Multi-unit plant concept (OSTI 10170594 referenced in iter-02 sources): evaluated multiple chambers sharing one driver.
+- Experimental platforms (NDCX-II, FAIR/SIS100) documented for current R&D status.
+- "Intensity Energy" company: definitively unverifiable — not in FIA 2025 survey (53 companies), Crunchbase, DOE award databases, or any fusion news. No private company is known to pursue HIF commercially.
 
 **Missing**:
-- Any company data — "Intensity Energy" is unverifiable (documented exhaustively in iter-01 and iter-02 sources). No company transparency to assess because no company exists.
-- Post-2000 updated plant studies with modern cost accounting (the HIBALL/HYLIFE-II studies are 30-40 years old).
-- Any DOE or ARPA-E program-level cost target documents for HIF revival (if any exist post-2010).
+- Post-2000 updated HIF plant studies with modern financial assumptions (1986/1990s costs require inflation adjustments and re-benchmarking).
+- Academic/national lab publications from the 2000s-2010s HIF program wind-down that may contain updated parameter estimates.
 
 **Gaps**:
-- Modern cost estimates in current dollars — `not-yet-sourced` — **important** (HYLIFE-II costs are late-1980s dollars; require escalation or updated study)
-- Company-level design transparency — `truly-unknown` — **nice-to-have** (no company exists to be transparent)
-- Post-2010 US program cost basis — `not-yet-sourced` — **nice-to-have** (search OSTI for DOE HIF program reviews post-2010)
+- Modern (post-2000) HIF plant design study — `not-yet-sourced` — **important** (PyFECONS IFE modules and ARIES cost framework may serve as partial substitutes)
+- Company design data (blanket type, energy conversion choice, target design) — `truly-unknown` — **important** (no company exists; must rely on historical designs and note the absence explicitly)
 
 ---
 
 ### 2. Challenges in Capturing System Function
-**Coverage**: Partial
+**Coverage**: Good
 
 **Available**:
-- Driver physics well-characterized: wall-plug efficiency 30-40%, beam energy 3-8 MJ/shot, ion species trade-offs documented (Bi²⁺ baseline).
-- Target physics and gain requirements stated: gain ~50-70 needed for 1 GWe; HYLIFE-II achieves gain ~70 at 5 MJ.
-- Energy conversion pathway documented: steam Rankine in both major designs; MHD hybrid evaluated in multi-unit HYLIFE-II study (OSTI 10170594).
-- Liquid wall chamber concept (FLiBe) addresses first wall lifetime problem by design.
+- Driver-target coupling physics: volumetric energy deposition, stopping range ~0.5-1 mm, RT instability discussed in arxiv 1511.06508 (abstract confirms large density-gradient-scale length helps reduce RT growth rate).
+- Target implosion requirements: gain ~50-70 for 1 GWe, compression ~1000x solid density — established across multiple sources.
+- Thick-liquid-wall chamber function: HYLIFE-II FLiBe jets providing simultaneous neutron shielding, tritium breeding, and first-wall protection; 30-year chamber lifetime implication documented.
+- Target injection and repetitive-rate mechanics: identified as a key engineering challenge in iter-02 sources (target must be delivered to chamber center at precise timing, 10 Hz → 864K targets/day per chamber).
+- Power conversion: steam Rankine baseline from both HIBALL and HYLIFE-II; sCO2 and combined cycles analyzed in analogous Z-IFE study (SAND2006-7148 at `osti-servlets-purl-901970.md`) — applicable as IFE power conversion analog.
+- Multi-unit plant economies documented (HYLIFE-II multi-unit study, Meier 1986 Eq. 3 scaling).
 
 **Missing**:
-- **Final focus optics**: How heavy ion beams are focused to ~few mm spot size at 5-10 m standoff distance remains a major unresolved physics challenge. Sources do not quantify the cost uncertainty this introduces.
-- **Chamber clearing dynamics**: FLiBe jet recovery time between shots (at 6-10 Hz) is a systems engineering constraint that propagates into rep rate achievability. Not quantified in available sources.
-- **Target injection and tracking**: Injecting and tracking ~10 Hz cryogenic DT targets in a live chamber environment is not modeled in cost terms in the sources.
-- **Ignition demonstration**: No HIF target has achieved ignition. Gain requirements are extrapolated from simulation, not experimental validation.
+- Quantitative rep-rate-limited chamber clearing time (how fast the FLiBe jet structure resets between shots) — not explicitly given in sources.
+- Modern beam physics calculations for final focusing (critical for target coupling efficiency at power-plant scale) — referenced in arxiv but not quantified in sources.
 
 **Gaps**:
-- Final focus / beam transport cost uncertainty — `not-yet-sourced` — **blocking** (search LBNL HIF program reports; this is the key physics gap between current experiments and power plant)
-- Target injection system cost model — `not-yet-sourced` — **important** (HYLIFE-II report likely contains this; sources only summarize)
-- Chamber hydrodynamics between shots — `derivable` from first principles / CFD literature — **important**
+- Chamber clearing dynamics / rep-rate ceiling — `not-yet-sourced` — **important** (HYLIFE-II final report likely contains this; search OSTI for HYLIFE-II companion reports)
+- Final focus beam physics at plant-relevant beam intensity — `not-yet-sourced` — **important** (search LBNL HIF program publications, arxiv 2005.07520 full text)
+- Target injection/tracking engineering at 10 Hz — `truly-unknown` (no demonstration facility exists at power-plant rep rate) — **important**
 
 ---
 
@@ -56,20 +60,21 @@
 **Coverage**: Partial
 
 **Available**:
-- Driver (induction linac): NDCX-II is operational; demonstrates beam compression principle. TRL ~4 at relevant parameter ranges.
-- Blanket technology (FLiBe, LiPb): Materials from fission industry experience. TRL ~4-5 as standalone material; HIF-integrated system is TRL ~2-3.
-- Energy conversion (steam Rankine): Mature industrial technology. TRL ~9.
-- Superconducting quadrupole magnets for beam transport: LTS technology well-demonstrated (TRL ~6-7 in accelerator context).
+- Driver (induction linac): NDCX-II operational at LBNL (Li⁺ at 3.5 MeV, beam compression demonstrated); FAIR/SIS100 commissioning 2025 for HIF-relevant heavy ion pulses. Identified as TRL 3-4 in dossier context; substantial gap between NDCX-II scale and power plant driver scale (~3 km linac, GeV-scale ions).
+- Target fabrication: no ignition demonstrated, gain > 1 not achieved; TRL 2-3 implied by dossier and physics status.
+- Thick-liquid-wall chamber: HYLIFE-II FLiBe jet design studies and shock mitigation experiments documented; TRL 3-4 (paper design with limited experimental validation).
+- Experimental programs (NDCX-II, FAIR, HIAF China, KEK Japan) documented as active or near-term.
+- Superconducting quadrupole magnets for beam transport: LTS (NbTi/Nb₃Sn) designs mature in accelerator physics; HTS upgrade path noted.
 
 **Missing**:
-- **Target fabrication at scale**: ~10 Hz × 3.15×10⁷ s/yr ≈ 315 million targets/year. No manufacturing process exists at this scale. TRL ~2. Sources do not assess this gap explicitly.
-- **HIF target ignition TRL**: No ignition demonstrated. Gain requirement is modeled, not proven. Sources state the requirement (50-70) but do not assess readiness vs. requirement.
-- **Final focus optics system**: Plasma lens or other neutralization/focusing scheme at reactor geometry has not been experimentally validated at required parameters. TRL ~2-3.
+- No systematic per-subsystem TRL table in any source.
+- No documented program timeline from current experiments to engineering demonstration.
+- Target factory (mass production at 10 Hz → ~864K targets/day): no analogue facility exists; only semiconductor chip manufacturing cited as rough analogy (Meier 1986) — this is the weakest subsystem maturity area.
 
 **Gaps**:
-- Target fabrication manufacturing TRL and cost — `not-yet-sourced` — **blocking** for LCOE (this is likely the largest unknown cost item; search NIF/IFE target fabrication cost studies as analogue)
-- Final focus subsystem TRL — `not-yet-sourced` — **important** (LBNL program reports; conference papers from HIFS-VNL)
-- Integrated system TRL for chamber/blanket/driver coupling — `derivable` from subsystem TRLs — **important**
+- Systematic TRL assessment by subsystem — `derivable` — **important** (can be assembled from component-level literature and experimental program descriptions, but requires judgment)
+- Target factory at power-plant-scale rep rate — `truly-unknown` — **important** (acknowledged gap in Meier 1986 itself: "currently no definitive studies on target factory costs")
+- Driver scale-up roadmap from NDCX-II to power plant — `not-yet-sourced` — **nice-to-have** (search LBNL HIF program review reports, 2008-2013 era)
 
 ---
 
@@ -77,92 +82,98 @@
 **Coverage**: Partial
 
 **Available**:
-- Tritium: D-T fuel requires breeding; both HIBALL (LiPb, TBR ~1.195) and HYLIFE-II (FLiBe) document breeding approaches. Tritium inventory quantified for HYLIFE-II (0.5 g in salt, 140 g in structural metal).
-- Bismuth (ion species): Not a scarce material; routine industrial production.
-- Lithium: Required for blanket breeding; Li-6 enrichment needed. Standard IFE supply chain consideration.
-- FLiBe: Contains beryllium — a known supply and toxicity concern.
+- Tritium breeding material options: LiPb (HIBALL, TBR ~1.195) and FLiBe (HYLIFE-II, TBR sufficient for self-sufficiency) both documented.
+- Li-6 enrichment supply chain: Giegerich et al. 2019 (KIT, `transat-h2020-wp-content-uploads-2019-11-giegerich.md`) — comprehensive analysis of Li-6 supply for fusion reactors. Key findings: no global facility currently capable of producing fusion-grade Li-6 at scale (~tens of tons needed); current market price ~53k€/kg (95% enriched); ICOMAX process proposed as viable route. This is directly applicable to HIF tritium breeding material needs.
+- Ion species (Bi²⁺, Pb) for driver: natural abundance, commercial availability, no exotic supply risk noted in sources.
+- LTS magnet materials (NbTi/Nb₃Sn): mature supply chain from accelerator industry.
+- DT fuel: tritium breeding required from blanket; no external tritium purchase possible at scale (standard D-T fusion constraint).
 
 **Missing**:
-- **Beryllium supply chain**: FLiBe contains ~9 wt% Be. Beryllium has limited global production and is classified as a critical mineral. Sources do not quantify FLiBe volume requirements or Be supply implications.
-- **Target material supply**: Precision hollow DT-ice targets require gold or lead tamper layers and cryogenic DT filling. At 315M targets/year, material throughput and precision manufacturing infrastructure are unstated.
-- **Li-6 enrichment**: Both designs rely on lithium blankets. Li-6 enrichment capacity globally is limited (primarily China post-USEC shutdown). Not addressed in sources.
+- FLiBe supply chain at power-plant scale: BeF₂ (beryllium fluoride) is the limiting component — beryllium is expensive, strategically controlled, and environmentally sensitive; not addressed in sources.
+- Target material supply: outer tamper of Pb or Au at ~864K targets/day represents a significant recurring material cost; not quantified.
+- Radiation damage to accelerator beamline components (pulsed neutron exposure to final focusing elements) — not addressed in sources.
 
 **Gaps**:
-- Beryllium supply for FLiBe blanket — `not-yet-sourced` — **important** (analogue studies from MSR/molten salt reactor literature; Be criticality assessments)
-- Target material throughput at scale — `derivable` from target geometry + rep rate — **important**
-- Li-6 enrichment supply chain — `not-yet-sourced` — **important** (applicable to all D-T IFE; search ORNL or DOE Li-6 supply assessments)
+- Li-6 enrichment supply chain at scale — partially covered (Giegerich), but fusion-grade supply does not yet exist — `truly-unknown` for timeline/cost — **important**
+- Beryllium supply chain for FLiBe blanket — `not-yet-sourced` — **important** (search for FLiBe material studies; EU DEMO reports cover this)
+- Target material recurring cost at production scale — `not-yet-sourced` — **nice-to-have**
+- Neutron damage to final focus elements — `not-yet-sourced` — **nice-to-have**
 
 ---
 
 ### 5. LCOE Parameter Extraction
-**Coverage**: Good (for a 30-40 year old design)
+**Coverage**: Partial
 
 **Available Parameters**:
+
 | Parameter | Value/Range | Source | Confidence |
 |-----------|-------------|--------|------------|
-| Baseline LCOE (HYLIFE-II) | 6.5 c/kWh (940 MWe) | OSTI 7021072 | m |
-| Scale LCOE (HYLIFE-II) | 4.5 c/kWh (2 GWe) | OSTI 7021072 | m |
-| Driver capital cost | $570M direct (RIA) | OSTI 7021072 | m |
-| Net electric output | 940 MWe (baseline), 3.8 GWe (HIBALL) | OSTI 7021072; KfK-3202 | m |
-| Driver wall-plug efficiency | 30–40% | arxiv 2005.07520 | h |
-| Target gain (requirement) | 50–70 for 1 GWe | arxiv 2005.07520 | h |
-| Target gain (HYLIFE-II nominal) | ~70 at 5 MJ | OSTI 7021072 | m |
-| Rep rate | 6 Hz (HYLIFE-II), 5 Hz (HIBALL/chamber) | OSTI 7021072; KfK-3202 | h |
-| Energy conversion type | Steam Rankine | OSTI 7021072; KfK-3202 | h |
-| Power recirculation fraction | ~15% | KfK-3202 (HIBALL) | m |
-| Chamber lifetime | 30 years (HYLIFE-II thick liquid wall) | OSTI 7021072 | m |
-| Tritium inventory | 140 g structural + 0.5 g FLiBe | OSTI 7021072 | m |
-
-*Confidence note: all "m" values from 30-40 year old studies; not adjusted for inflation or modern cost basis.*
+| Net electric power | 940 MWe (baseline), 1934 MWe (scaled), 3.8 GWe (HIBALL) | HYLIFE-II (OSTI 7021072); HIBALL (KfK-3202) | h |
+| COE estimate | 6.5 c/kWh baseline; 4.5 c/kWh at 2 GWe scale (HYLIFE-II, 1990s $) | `hif-technology-overview.md` | m |
+| COE range | 3.9–5.8 c/kWh for 1.5–3 GWe at 5-10 Hz (1986 $) | Meier et al. 1986 (`economic_studies_for_heavy_ion_fusion_electric_power_plants/`) | m |
+| Driver direct cost | ~$570M (HYLIFE-II RIA driver, 1990s $) | `hif-technology-overview.md` | m |
+| Reactor direct cost | $0.66B for Cascade design at 1.67 GWt / 0.905 GWe (1986 $) | Meier et al. 1986 | m |
+| Target factory direct cost | ~$0.1B (constant, pulse-rate-independent assumed baseline) | Meier et al. 1986 | l |
+| Total capital multiplier | 1.83× direct capital cost (midpoint coal/nuclear) | Meier et al. 1986 | m |
+| O&M cost | 3% of total capital per year | Meier et al. 1986 | m |
+| Fuel cycle cost | Negligible (assumed) | Meier et al. 1986 | m |
+| Fixed charge rate | 8.3%/yr (constant dollar, 1986 methodology) | Meier et al. 1986 | l |
+| Driver efficiency | 30–40% wall-plug | Multiple sources (dossier, arxiv 1511.06508) | h |
+| Target gain | ~50-70 required; HYLIFE-II nominal ~70 at 5 MJ | `hif-technology-overview.md`; arxiv abstract | h |
+| Driver energy per shot | 3–8 MJ (HIBALL 10 GeV Bi²⁺; HYLIFE-II 5 MJ) | Dossier | h |
+| Repetition rate | ~10–15 Hz (power plant target); HYLIFE-II 6 Hz | Dossier; iter-02 sources | h |
+| Power recirculation | 15% (HIBALL); implied ~25–30% for HYLIFE-II | `hif-technology-overview.md` | m |
+| Thermal conversion efficiency | ~30-35% (steam Rankine, conventional) | Inferred from HIBALL/HYLIFE-II design; not stated explicitly | l |
+| TBR | ~1.195 (HIBALL LiPb) | Dossier | m |
 
 **Missing Parameters**:
+
 | Parameter | Gap Type | Criticality | Notes |
 |-----------|----------|-------------|-------|
-| Target fabrication cost (per target, at scale) | not-yet-sourced | blocking | Likely the largest single unknown O&M cost; NIF target cost analogue is ~$1-10/target at scale, but HIF targets are simpler |
-| Capital cost breakdown by CAS subsystem | not-yet-sourced | blocking | HYLIFE-II final report likely contains this detail; our sources are summaries only — read OSTI 7021072 directly |
-| Thermal cycle efficiency (explicit %) | not-yet-sourced | important | Steam Rankine type confirmed but efficiency % not in sources; ~33-38% is standard assumption |
-| Capacity factor / plant availability | not-yet-sourced | important | HYLIFE-II likely addresses maintenance schedules; not captured in current sources |
-| Blanket replacement schedule and cost | not-yet-sourced | important | HYLIFE-II claims 30-yr chamber lifetime (no replacement) — O&M driver implications are significant but not quantified |
-| O&M cost estimate | not-yet-sourced | important | Not in current source summaries; HYLIFE-II report likely has this |
-| Modern cost escalation basis | derivable | important | Escalate HYLIFE-II costs from ~1990 dollars using construction cost indices |
-| Final focus optics capital cost | not-yet-sourced | important | Not addressed in current sources; significant driver subsystem element |
-| Q (fusion energy gain) vs. driver Q | derivable | nice-to-have | Derivable from gain × driver efficiency |
+| Plant availability / capacity factor | derivable | important | Not stated in sources; standard assumption ~75-85% for baseload fusion; use IFE convention |
+| Inflation-adjusted cost estimates | derivable | important | 1986 and 1990s dollar figures; need escalation to 2024$ via CEPCI or GDP deflator; no modern study provides this |
+| Thermal-to-electric conversion efficiency (explicit) | derivable | important | Steam Rankine ~30-35% is reasonable estimate, but sCO2 option (as in Z-IFE analog) would be ~45%; must choose and document |
+| Blanket/tritium processing cost (CAS 22.01) | not-yet-sourced | important | Not broken out in Meier 1986 three-part model; ARIES cost accounts framework applicable |
+| Decommissioning cost | derivable | nice-to-have | Standard IFE assumption; not concept-specific |
+| Construction time | not-yet-sourced | nice-to-have | Meier 1986 uses 8.3% FCR without explicit construction time; HYLIFE-II doesn't state it |
+| Target unit cost at production scale | truly-unknown | important | Meier 1986 explicitly acknowledges "no definitive studies"; semiconductor chip analogy only |
+| Full CAS-structured breakdown (CAS 20-27) | not-yet-sourced | important | Only three-part model exists (reactor/driver/factory); PyFECONS IFE module likely has CAS mapping |
 
 ---
 
 ## Source Recommendations
 
-1. **Read OSTI 7021072 (HYLIFE-II Final Report) directly** — `not-yet-sourced` — almost certainly contains CAS-level capital cost breakdown, O&M estimates, capacity factor assumptions, and thermal efficiency. Current sources are summaries. This is the highest-priority action. (*Search: OSTI 7021072, or "HYLIFE-II final report" on osti.gov*)
+1. **HYLIFE-II Full Final Report** (OSTI 7021072) — the full report likely contains detailed cost breakdowns, plant availability assumptions, and heat transport efficiency data not captured in the dossier summary. — `not-yet-sourced` — Search OSTI for OSTI:7021072 and companion reports (OSTI:7368768 "Improved heat transport system and steam power plant"). Confirm existence before searching.
 
-2. **Read KfK-3202 (HIBALL) directly** — `not-yet-sourced` — German/US plant study from 1985; likely contains analogous cost structure to HYLIFE-II. Provides cross-check and alternative design point. (*Search: "KfK-3202" or "HIBALL heavy ion fusion" on OSTI or academia.edu — one copy found at academia.edu/61216305 in iter-01*)
+2. **HIBALL Study** (KfK-3202, 1985) — full German/US report likely contains CAS-style cost breakdown and capacity factor assumptions not in the compiled overview. — `not-yet-sourced` — Search OSTI or European nuclear library for KfK-3202.
 
-3. **Search for NIF/IFE target fabrication cost literature** as analogue for HIF target cost — `not-yet-sourced` — HIF targets are simpler than laser ICF targets but share fabrication challenge at scale. (*Search: OSTI for "IFE target fabrication cost" or "laser target factory"; LLNL reports from IFE program c. 2010-2015*)
+3. **PyFECONS IFE modules** (`/home/reid/PyFECONS`) — this codebase likely implements driver cost scaling and IFE-specific CAS mapping that could translate Meier 1986 formulas into a modern CAS structure and update dollar figures via built-in escalation. Directly applicable for CAS-structured cost gap.
 
-4. **Search for HYLIFE-II multi-unit plant study (OSTI 10170594)** — referenced in iter-02 but not yet extracted — evaluates learning curve and MHD hybrid energy conversion. May contain updated cost estimates. (*`unverified — confirm existence before searching`*)
+4. **HIF Systems Assessment Project reports** (LBNL, ~1979-1992) — series of reports that culminated in HYLIFE-II; intermediate reports may contain detailed subsystem TRLs and cost breakdowns. — `not-yet-sourced` — `unverified — confirm existence before searching`; search OSTI for "heavy ion fusion systems assessment."
 
-5. **Search for DOE HIF program review post-2010** — `not-yet-sourced` — if the US HIF program produced any post-2005 cost or roadmap documents before LBNL program ended, these would provide more recent cost basis. (*Search: OSTI for "heavy ion fusion energy" + "program review" or "roadmap"; also ARPA-E ALPHA program documents*)
+5. **Hawker 2020 IFE LCOE model** (`knowledge/sources/a_simplified_economic_model_for_inertial_fusion/`) — the 14-parameter technology-agnostic IFE LCOE model directly applicable to HIF. Provides methodology for handling missing parameters (gain, target cost, rep rate sensitivity). Already in the repo — read for LCOE methodology section.
 
-6. **Beryllium supply chain assessment** — `not-yet-sourced` — for FLiBe blanket design. (*Search: DOE Critical Minerals assessments; ORNL MSR/FLiBe literature; Be supply data from USGS mineral surveys*)
+6. **ARIES cost accounts** (`knowledge/sources/aries_cost_account_documentation/`) — provides the CAS hierarchy (accounts 20-27) that can structure the three-part Meier cost model into a full CAS breakdown for cross-concept comparability.
 
 ---
 
 ## Summary
 
-**Proceed to full analysis.** The data foundation is sufficient for a D1+ qualitative write-up and a parameterized LCOE model. Two detailed power plant studies provide subsystem-level cost structure, LCOE estimates, energy conversion details, and plant parameters — more than most pre-commercial concepts offer. The key action before writing is to **read OSTI 7021072 directly** (not just the current summary) to extract CAS-level capital costs, O&M breakdown, and capacity factor assumptions that are almost certainly in the full report but not captured in current source summaries.
+The analysis can proceed to D1+ without additional source acquisition. The concept is exceptionally well-documented for a pre-commercial fusion approach: two full power plant designs (HIBALL, HYLIFE-II), a parametric economic model (Meier 1986), and multi-source confirmation of key physics parameters. The primary analytical work required is: (1) inflating 1986/1990s cost figures to contemporary dollars using CEPCI or GDP deflator, (2) mapping the Meier three-part cost model onto the CAS hierarchy using ARIES accounts (both sources already in the repo), (3) selecting a capacity factor assumption (~75-85%) with explicit justification, and (4) noting throughout that no current company exists and all design-choice parameters (blanket type, conversion cycle) reflect historical national lab selections rather than a committed design. PyFECONS IFE modules should be consulted before writing the capital cost section to avoid re-deriving what's already implemented.
 
-The most important analytical framing issue: there is no company, so the analysis should be structured as "national lab reference design (HYLIFE-II baseline)" rather than a company assessment. The "Intensity Energy" placeholder should be flagged explicitly. Physics uncertainties (final focus, target fabrication at scale, ignition demonstration) are the real risk factors, and the back-solve to $0.01/kWh will quickly reveal how sensitive LCOE is to the target fabrication cost assumption and driver capital cost — both well-characterized from HYLIFE-II.
+---
 
 ## Structured summary (machine-readable)
 
 ```yaml
 overall_rating: "Mostly Ready"
-blocking_count: 2
-important_count: 6
-counting_method: "section_5_missing_parameters"
+blocking_count: 0
+important_count: 9
+counting_method: "all_sections_deduplicated — counting distinct important/blocking gaps across all 5 sections: (1) no modern cost study, (2) company non-existence, (3) chamber clearing dynamics, (4) target injection at rep rate, (5) systematic TRL assessment, (6) target factory cost at scale, (7) Li-6 supply chain timeline/cost, (8) Be supply chain for FLiBe, (9) plant availability/capacity factor assumption"
 section_coverage:
   availability_of_data:       "Good"
-  system_function:            "Partial"
+  system_function:            "Good"
   subsystem_maturity:         "Partial"
   materials_supply_chain:     "Partial"
-  lcoe_parameter_extraction:  "Good (for a 30-40 year old design)"
-```
+  lcoe_parameter_extraction:  "Partial"
+```
\ No newline at end of file
```

## Acceptance notes (fill during Phase 3)

- Deviation class (1-6 per plan.md): 
- Justified by fleet source? 
- Notes: 
