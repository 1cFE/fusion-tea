# Phase 3 diff: 25-heavy-ion-beam-icf

**Generated:** 2026-05-22T15:24:54-07:00

## Counts (Phase 2 -> Phase 3 strict-read regen)

| field | phase2 | phase3 | Δ |
|-------|--------|--------|---|
| blocking_count   | 0 | 0 | 0 |
| important_count  | 9 | 8 | - |
| overall_rating   | Mostly Ready | Mostly Ready | - |

## Fleet-source dispositions in new report

```
```

## Forbidden-phrase check (should be empty)

```
(none — good)
```

## First line of new report (should start with `# Gap Assessment`)

```
I now have all the information needed to write the complete assessment.
```

## Blocking-tier lines (new)

```
175:The analysis should acknowledge three systematic limitations: (1) all detailed cost data is 1980s–1990s vintage and requires explicit escalation using the GDP IPD methodology from `aries_cost_account_documentation`; (2) no ion-beam-driven ignition has been demonstrated — physics TRL remains ≤4, making the gain assumption (G~70) a paper extrapolation; and (3) the target injection and rep-rate challenge (10–15 Hz) has no experimental validation, creating a speculative floor on capacity factor. These are `important` qualifications, not `blocking` gaps — the available data is sufficient for a bracketed parametric LCOE estimate with appropriately stated uncertainty ranges.
```

## Full unified diff (truncated to 400 lines)

```diff
--- /tmp/gap_phase2_state/25-heavy-ion-beam-icf.md	2026-05-22 12:59:21.081581706 -0700
+++ /home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/25-heavy-ion-beam-icf/gap_report.md	2026-05-22 15:24:54.150711814 -0700
@@ -1,165 +1,180 @@
-I have sufficient information to write the assessment. The OSTI source (osti-servlets-purl-901970) is Z-IFE (z-pinch), not HIF — useful as an IFE BOP/power-conversion analog. The Giegerich source covers Li-6 enrichment supply chain, directly relevant to HIF tritium breeding.
-
----
+I now have all the information needed to write the complete assessment.
 
 # Gap Assessment: Heavy Ion Beam ICF (D-T)
 
 ## Overall Readiness
 **Rating**: Mostly Ready
-**Summary**: Heavy ion beam ICF is exceptionally well-characterized in the published literature relative to most emerging fusion concepts — two detailed power plant designs (HIBALL, HYLIFE-II) and a parametric economic model (Meier 1986, LLNL) exist from sustained national lab programs. The primary limitations are that all primary cost and design data is 35-40 years old, no private company is actively developing this approach (making company-specific design choices unresolvable), and subsystem TRL data must be assembled from component-level sources rather than any systematic assessment. A D1+ analysis can proceed with clear confidence bounds on the data vintage.
-
----
+**Summary**: Heavy ion beam ICF is unusually well-documented for a concept with no active private company — two detailed national-lab plant design studies (HIBALL-1985, HYLIFE-II-1990s) exist with cost estimates, and dedicated HIF economic analyses provide parametric COE formulas. The main limitations are the age of all capital cost data (1980s–1990s vintage requiring escalation) and the absence of any ion-beam-driven ignition demonstration, which limits physics TRL confidence. A D1+ analysis can proceed with appropriately stated assumptions, provided the cost vintage gap is handled explicitly.
 
 ## Section Coverage
 
 ### 1. Availability of Data
 **Coverage**: Good
-
 **Available**:
-- Two complete power plant conceptual designs: HIBALL (KfK-3202, 1985) and HYLIFE-II (OSTI 7021072, early 1990s), both with subsystem descriptions, cost estimates, and performance parameters. `iter-01/sources/hif-technology-overview.md` compiles key parameters from these.
-- HIF physics review (arxiv 1511.06508, 2015): driver efficiency, target gain requirements, implosion physics, RT instability treatment.
-- Driver and target parameter confirmation: rep rate, beam energy, driver efficiency confirmed across multiple sources (arxiv 2005.07520 cited in dossier, hif-recent-research-compilation.md).
-- Parametric COE model: Meier et al. 1986 (LLNL/UCRL-94335) at `knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/` — three-part capital cost model (reactor + driver + target factory), COE formula with explicit financial assumptions.
-- Multi-unit plant concept (OSTI 10170594 referenced in iter-02 sources): evaluated multiple chambers sharing one driver.
-- Experimental platforms (NDCX-II, FAIR/SIS100) documented for current R&D status.
-- "Intensity Energy" company: definitively unverifiable — not in FIA 2025 survey (53 companies), Crunchbase, DOE award databases, or any fusion news. No private company is known to pursue HIF commercially.
+- Two complete conceptual power plant designs: HIBALL (KfK-3202, 1985) and HYLIFE-II (OSTI 7021072, 1990s), both with detailed cost estimates and system architectures.
+- `iter-01/sources/hif-technology-overview.md`: compiled driver efficiency (30–40%), ion parameters, accelerator modularity, magnet technology.
+- `iter-02/sources/hif-recent-research-compilation.md`: confirms rep-rate targets (10–15 Hz per arxiv 2005.07520), blanket options, experimental status.
+- `iter-02/sources/arxiv-1511-06508.md`: review of HIF physics — abstract confirms target gain 50–70 requirement for 1 GWe, 10–15 Hz operating frequency, fuel compression to ~1000× solid density.
+- `knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/output.md` (Meier et al. 1986, LLNL): parametric HIF COE model with explicit cost formulas for reactor, driver, and target factory; COE range 3.9–9.8 ¢/kWh (1986$) across 0.5–1.5 GWe and 5–15 Hz.
+- `knowledge/sources/a_simplified_economic_model_for_inertial_fusion/output.md` (Hawker 2020): HYLIFE-II baseline inflated to ~$3600/kWe (2020$, driver excluded); 14-parameter technology-agnostic IFE LCOE framework directly applicable to HIF.
+- `knowledge/sources/accelerators_for_inertial_fusion_energy_production/output.md` (Bangerter et al. 2013): comprehensive review of RF and induction linacs for IFE, confirming capital cost as the fundamental challenge alongside phase-space/focusing constraints.
+- `knowledge/sources/energy_from_inertial_fusion/output.md` (Hogan et al. 1992): confirms four-component IFE plant structure (driver, target factory, reactor, generator) and Cascade reactor concept.
+- `iter-02/sources/transat-h2020-wp-content-uploads-2019-11-giegerich.md` (Giegerich 2019, KIT): Li-6 isotope supply chain — no large-scale enrichment facility currently exists; ICOMAX development underway; ~26 tons ⁶Li required per GWfus; current spot price ~53 k€/kg.
+- Company verification: definitively unverifiable — "Intensity Energy" does not appear in FIA 2025 survey of 53 companies, Crunchbase, LinkedIn, ARPA-E, or DOE award databases.
 
 **Missing**:
-- Post-2000 updated HIF plant studies with modern financial assumptions (1986/1990s costs require inflation adjustments and re-benchmarking).
-- Academic/national lab publications from the 2000s-2010s HIF program wind-down that may contain updated parameter estimates.
+- Full HIBALL report (KfK-3202) not extracted into repo — values available only via dossier summary and secondary citations.
+- Full HYLIFE-II final report (OSTI 7021072) not extracted — similarly known through secondary sources.
+- No active private company → no current design, roadmap, or funding disclosure.
 
 **Gaps**:
-- Modern (post-2000) HIF plant design study — `not-yet-sourced` — **important** (PyFECONS IFE modules and ARIES cost framework may serve as partial substitutes)
-- Company design data (blanket type, energy conversion choice, target design) — `truly-unknown` — **important** (no company exists; must rely on historical designs and note the absence explicitly)
+- Full HIBALL (KfK-3202) not in extracted sources — `not-yet-sourced` — nice-to-have (dossier already captures key values)
+- Full HYLIFE-II (OSTI 7021072) not extracted — `not-yet-sourced` — nice-to-have (values captured in dossier)
+- No active company data — `truly-unknown` — nice-to-have (no private company exists)
 
 ---
 
 ### 2. Challenges in Capturing System Function
-**Coverage**: Good
-
+**Coverage**: Partial
 **Available**:
-- Driver-target coupling physics: volumetric energy deposition, stopping range ~0.5-1 mm, RT instability discussed in arxiv 1511.06508 (abstract confirms large density-gradient-scale length helps reduce RT growth rate).
-- Target implosion requirements: gain ~50-70 for 1 GWe, compression ~1000x solid density — established across multiple sources.
-- Thick-liquid-wall chamber function: HYLIFE-II FLiBe jets providing simultaneous neutron shielding, tritium breeding, and first-wall protection; 30-year chamber lifetime implication documented.
-- Target injection and repetitive-rate mechanics: identified as a key engineering challenge in iter-02 sources (target must be delivered to chamber center at precise timing, 10 Hz → 864K targets/day per chamber).
-- Power conversion: steam Rankine baseline from both HIBALL and HYLIFE-II; sCO2 and combined cycles analyzed in analogous Z-IFE study (SAND2006-7148 at `osti-servlets-purl-901970.md`) — applicable as IFE power conversion analog.
-- Multi-unit plant economies documented (HYLIFE-II multi-unit study, Meier 1986 Eq. 3 scaling).
+- Driver physics and efficiency well-documented: induction linac wall-plug efficiency 30–40% vs. 1–15% for lasers (arxiv 2005.07520; Bangerter 2013). Multiple-beam architecture (hundreds of beamlets) and beam transport via superconducting quadrupole arrays characterized.
+- Target compression physics documented: ~1000× solid density, stopping range ~0.5–1 mm, required gain 50–70 at 5 MJ (arxiv 1511.06508; hif-technology-overview.md).
+- FLiBe chamber dynamics studied in related IFE context: `osti-servlets-purl-901970.md` (Z-IFE SAND2006-7148) characterizes thick liquid curtain jet behavior, shock mitigation, and FLiBe salt interaction with ferritic steel — directly applicable to HYLIFE-II chamber architecture even though it is a Z-pinch driver study.
+- Power conversion cycle trade-offs documented in Z-IFE source: sCO2 Brayton vs. Rankine vs. combined cycle analyzed; combined cycle found optimal. Rankine baseline efficiency ~33% at 550°C.
+- Multi-unit plant concept: OSTI 10170594 (referenced in dossier) evaluates shared single driver feeding multiple chambers, including MHD+Steam hybrid.
 
 **Missing**:
-- Quantitative rep-rate-limited chamber clearing time (how fast the FLiBe jet structure resets between shots) — not explicitly given in sources.
-- Modern beam physics calculations for final focusing (critical for target coupling efficiency at power-plant scale) — referenced in arxiv but not quantified in sources.
+- Target injection at 10–15 Hz not demonstrated at any scale — this is the largest unresolved engineering challenge. There is no analog published for a 10 Hz HIF target factory.
+- Final focus system: beam neutralization (plasma channel or thin foil) required to achieve the final focusing intensity; critical physics not demonstrated at full power and is an active research question per Bangerter 2013.
+- Chamber gas clearing and jet re-establishment between shots at 6–10 Hz: analogous to laser ICF chamber challenges but specific to thick-liquid FLiBe dynamics. Z-IFE source provides partial analog but Z-pinch chamber geometry differs.
 
 **Gaps**:
-- Chamber clearing dynamics / rep-rate ceiling — `not-yet-sourced` — **important** (HYLIFE-II final report likely contains this; search OSTI for HYLIFE-II companion reports)
-- Final focus beam physics at plant-relevant beam intensity — `not-yet-sourced` — **important** (search LBNL HIF program publications, arxiv 2005.07520 full text)
-- Target injection/tracking engineering at 10 Hz — `truly-unknown` (no demonstration facility exists at power-plant rep rate) — **important**
+- Target injection / factory operation at 10–15 Hz power-plant rep rate: no experimental demonstration — `truly-unknown` — important
+- Final-focus beam neutralization at full driver parameters — `truly-unknown` — important
+- FLiBe jet re-establishment at 6–10 Hz: Z-IFE analog only, no HIF-specific data — `not-yet-sourced` — important
 
 ---
 
 ### 3. Maturity of Key Subsystems and Components
 **Coverage**: Partial
-
 **Available**:
-- Driver (induction linac): NDCX-II operational at LBNL (Li⁺ at 3.5 MeV, beam compression demonstrated); FAIR/SIS100 commissioning 2025 for HIF-relevant heavy ion pulses. Identified as TRL 3-4 in dossier context; substantial gap between NDCX-II scale and power plant driver scale (~3 km linac, GeV-scale ions).
-- Target fabrication: no ignition demonstrated, gain > 1 not achieved; TRL 2-3 implied by dossier and physics status.
-- Thick-liquid-wall chamber: HYLIFE-II FLiBe jet design studies and shock mitigation experiments documented; TRL 3-4 (paper design with limited experimental validation).
-- Experimental programs (NDCX-II, FAIR, HIAF China, KEK Japan) documented as active or near-term.
-- Superconducting quadrupole magnets for beam transport: LTS (NbTi/Nb₃Sn) designs mature in accelerator physics; HTS upgrade path noted.
+- `knowledge/meta_analysis/progress_toward_fusion_breakeven_lawson_criterion/output.md` (Wurzel & Hsu 2021): comprehensive ICF Lawson parameter benchmarking. Laser ICF (NIF) has achieved ignition; HIF experiments (NDCX-II) remain in the warm-dense-matter physics regime, far from fusion-relevant Lawson parameters.
+- NDCX-II (LBNL): operational, compresses Li⁺ beam from 500 ns to ~1 ns in 15 m, 3.5 MeV — TRL 4 for beam compression physics, but ion energy and power are orders of magnitude below power-plant requirements.
+- FAIR/SIS100 (GSI, commissioning 2025): 5×10¹¹ uranium ions, tens of GeV, ~100 ns pulses — benchmarks driver parameter space but is a research accelerator, not a fusion driver prototype.
+- Induction linac technology: mature at low rep rates (NDCX-II, DARHT); scaling to fusion-relevant parameters is unproven.
+- FLiBe and LiPb blanket/tritium breeding: TRL 4–5 (relevant materials data from fission MSR programs, HYLIFE-II design studies, Z-IFE characterization).
+- Steam Rankine cycle: TRL 9 (commercial fission heritage).
+- HTS/LTS superconducting quadrupoles for beam transport: TRL 6–7 (used in particle accelerator programs).
+
+| Subsystem | TRL Estimate | Basis |
+|-----------|-------------|-------|
+| Induction linac driver (full power) | 3–4 | NDCX-II compressed beam, no fusion-scale demonstration |
+| Target physics (beam-driven ignition) | 3 | No beam-driven ignition; laser ICF achieved ignition |
+| Final focus / beam neutralization | 3–4 | NDCX-II neutralized drift compression demonstrated |
+| Target injection (10–15 Hz) | 2–3 | Conceptual design only |
+| Target factory (mass production) | 2–3 | No HIF-specific prototype |
+| FLiBe / LiPb blanket | 4–5 | Fission MSR heritage, HYLIFE-II/Z-IFE design studies |
+| Steam Rankine power conversion | 9 | Commercial fission |
+| Beam transport (superconducting quads) | 6–7 | Particle accelerator programs |
 
 **Missing**:
-- No systematic per-subsystem TRL table in any source.
-- No documented program timeline from current experiments to engineering demonstration.
-- Target factory (mass production at 10 Hz → ~864K targets/day): no analogue facility exists; only semiconductor chip manufacturing cited as rough analogy (Meier 1986) — this is the weakest subsystem maturity area.
+- No integrated driver prototype at fusion-relevant beam energy (5+ MJ) has been built or planned. The gap between NDCX-II and a power-plant driver is ~4 orders of magnitude in energy.
+- Target gain demonstration via heavy ion beams: none. NIF has achieved ignition via laser, validating ICF physics generally, but HIF-specific ignition physics is unconfirmed.
 
 **Gaps**:
-- Systematic TRL assessment by subsystem — `derivable` — **important** (can be assembled from component-level literature and experimental program descriptions, but requires judgment)
-- Target factory at power-plant-scale rep rate — `truly-unknown` — **important** (acknowledged gap in Meier 1986 itself: "currently no definitive studies on target factory costs")
-- Driver scale-up roadmap from NDCX-II to power plant — `not-yet-sourced` — **nice-to-have** (search LBNL HIF program review reports, 2008-2013 era)
+- No ion-beam-driven ignition demonstration — `truly-unknown` — important (fundamental physics TRL ceiling)
+- No integrated driver prototype near power-plant parameters — `truly-unknown` — important
+- Target injection / factory at rep rate: TRL 2–3, not demonstrated — `truly-unknown` — important
 
 ---
 
 ### 4. Key Materials and Supply Chain Considerations
 **Coverage**: Partial
-
 **Available**:
-- Tritium breeding material options: LiPb (HIBALL, TBR ~1.195) and FLiBe (HYLIFE-II, TBR sufficient for self-sufficiency) both documented.
-- Li-6 enrichment supply chain: Giegerich et al. 2019 (KIT, `transat-h2020-wp-content-uploads-2019-11-giegerich.md`) — comprehensive analysis of Li-6 supply for fusion reactors. Key findings: no global facility currently capable of producing fusion-grade Li-6 at scale (~tens of tons needed); current market price ~53k€/kg (95% enriched); ICOMAX process proposed as viable route. This is directly applicable to HIF tritium breeding material needs.
-- Ion species (Bi²⁺, Pb) for driver: natural abundance, commercial availability, no exotic supply risk noted in sources.
-- LTS magnet materials (NbTi/Nb₃Sn): mature supply chain from accelerator industry.
-- DT fuel: tritium breeding required from blanket; no external tritium purchase possible at scale (standard D-T fusion constraint).
+- `iter-02/sources/transat-h2020-wp-content-uploads-2019-11-giegerich.md` (Giegerich 2019): Li-6 enrichment supply chain documented in detail. Key finding: no large-scale ⁶Li enrichment facility exists worldwide. COLEX process (historical, mercury-based, classified, environmentally contaminated) no longer operational. KIT developing ICOMAX mercury-amalgam process. For a 2 GWfus WCLL blanket: 8,200 tons LiPb inventory (52 tons ⁶Li at 90% enrichment); 112 kg ⁶Li consumed per full-power year per GWfus. Current spot price ~53 k€/kg.
+- HYLIFE-II FLiBe inventory: 0.5 g tritium in molten salt, 140 g in tube wall metal. FLiBe requires Be handling facilities (beryllium is toxic).
+- HIBALL LiPb blanket: TBR ~1.195, more benign supply chain than FLiBe.
+- Bismuth (reference ion for HIBALL): industrially available, no supply constraint identified.
+- Induction cell mass production: identified as key HIF advantage — hundreds of identical cells enabling factory production (hif-technology-overview.md). No current supplier network, but concept is well-specified.
+- DT target mass production: ~190M targets/year at 6 Hz (HYLIFE-II rate). No commercial analog. Semiconductor chip fab analogy cited in Meier 1986, but cost and feasibility unquantified.
 
 **Missing**:
-- FLiBe supply chain at power-plant scale: BeF₂ (beryllium fluoride) is the limiting component — beryllium is expensive, strategically controlled, and environmentally sensitive; not addressed in sources.
-- Target material supply: outer tamper of Pb or Au at ~864K targets/day represents a significant recurring material cost; not quantified.
-- Radiation damage to accelerator beamline components (pulsed neutron exposure to final focusing elements) — not addressed in sources.
+- No modern (post-2000) Li-6 supply chain analysis specific to HIF parameters.
+- Beryllium supply chain for FLiBe: global Be production (~200 tons/year) may be limiting for fleet deployment; not analyzed in available sources.
+- DT target cryogenic assembly at ~190M targets/year: no engineering feasibility study or cost estimate found in sources.
 
 **Gaps**:
-- Li-6 enrichment supply chain at scale — partially covered (Giegerich), but fusion-grade supply does not yet exist — `truly-unknown` for timeline/cost — **important**
-- Beryllium supply chain for FLiBe blanket — `not-yet-sourced` — **important** (search for FLiBe material studies; EU DEMO reports cover this)
-- Target material recurring cost at production scale — `not-yet-sourced` — **nice-to-have**
-- Neutron damage to final focus elements — `not-yet-sourced` — **nice-to-have**
+- Li-6 enrichment at commercial scale: no current facility, KIT process at lab scale only — `not-yet-sourced` for modern HIF-specific quantification — important
+- Beryllium supply chain for FLiBe: not characterized — `not-yet-sourced` — important
+- DT target mass production at 10 Hz: no manufacturing study — `truly-unknown` — important (analogous challenge exists in laser IFE, no HIF-specific study found)
 
 ---
 
 ### 5. LCOE Parameter Extraction
-**Coverage**: Partial
-
 **Available Parameters**:
 
 | Parameter | Value/Range | Source | Confidence |
 |-----------|-------------|--------|------------|
-| Net electric power | 940 MWe (baseline), 1934 MWe (scaled), 3.8 GWe (HIBALL) | HYLIFE-II (OSTI 7021072); HIBALL (KfK-3202) | h |
-| COE estimate | 6.5 c/kWh baseline; 4.5 c/kWh at 2 GWe scale (HYLIFE-II, 1990s $) | `hif-technology-overview.md` | m |
-| COE range | 3.9–5.8 c/kWh for 1.5–3 GWe at 5-10 Hz (1986 $) | Meier et al. 1986 (`economic_studies_for_heavy_ion_fusion_electric_power_plants/`) | m |
-| Driver direct cost | ~$570M (HYLIFE-II RIA driver, 1990s $) | `hif-technology-overview.md` | m |
-| Reactor direct cost | $0.66B for Cascade design at 1.67 GWt / 0.905 GWe (1986 $) | Meier et al. 1986 | m |
-| Target factory direct cost | ~$0.1B (constant, pulse-rate-independent assumed baseline) | Meier et al. 1986 | l |
-| Total capital multiplier | 1.83× direct capital cost (midpoint coal/nuclear) | Meier et al. 1986 | m |
-| O&M cost | 3% of total capital per year | Meier et al. 1986 | m |
-| Fuel cycle cost | Negligible (assumed) | Meier et al. 1986 | m |
-| Fixed charge rate | 8.3%/yr (constant dollar, 1986 methodology) | Meier et al. 1986 | l |
-| Driver efficiency | 30–40% wall-plug | Multiple sources (dossier, arxiv 1511.06508) | h |
-| Target gain | ~50-70 required; HYLIFE-II nominal ~70 at 5 MJ | `hif-technology-overview.md`; arxiv abstract | h |
-| Driver energy per shot | 3–8 MJ (HIBALL 10 GeV Bi²⁺; HYLIFE-II 5 MJ) | Dossier | h |
-| Repetition rate | ~10–15 Hz (power plant target); HYLIFE-II 6 Hz | Dossier; iter-02 sources | h |
-| Power recirculation | 15% (HIBALL); implied ~25–30% for HYLIFE-II | `hif-technology-overview.md` | m |
-| Thermal conversion efficiency | ~30-35% (steam Rankine, conventional) | Inferred from HIBALL/HYLIFE-II design; not stated explicitly | l |
-| TBR | ~1.195 (HIBALL LiPb) | Dossier | m |
+| Net electrical output | 940 MWe (HYLIFE-II), 3.8 GWe (HIBALL), 1.0–3.0 GWe parametric | HYLIFE-II; HIBALL; Meier 1986 | h |
+| Driver direct capital cost | ~$570M (HYLIFE-II RIA, 1990s$); formula: $C_{dd} = (0.32 + 0.088E_d)(1.25 + 0.05N_c)(1 + 0.0088(\nu-5))$ B | HYLIFE-II; Meier 1986 | m |
+| Reactor/chamber direct capital cost | $0.66B at 1.67 GWt / 0.905 GWe (Cascade reference), scales as $P_t^{0.49}$ | Meier 1986 | m |
+| Target factory capital cost | $0.1B (constant, base case) | Meier 1986 | l |
+| Plant cost (non-driver BOP) | ~$3,600/kWe (2020$, HYLIFE-II baseline, driver excluded) | Hawker 2020 via `a_simplified_economic_model` | m |
+| O&M cost | 3% of total capital cost per year | Meier 1986 | l |
+| Fixed charge rate | 8.3% per year (constant dollar) | Meier 1986 | m |
+| Total capital cost multiplier | 1.83× direct costs (includes indirect costs, interest during construction) | Meier 1986 | m |
+| COE range (1986 vintage) | 3.9–9.8 ¢/kWh depending on plant size (0.5–1.5 GWe) and rep rate (5–15 Hz) | Meier 1986 | m |
+| Driver efficiency | 30–40% wall-plug (induction linac) | arxiv 2005.07520; hif-technology-overview.md | h |
+| Target gain | ~70 (HYLIFE-II nominal), 50–70 required for 1 GWe | HYLIFE-II; arxiv 1511.06508 | m |
+| Driver energy per shot | 5 MJ (HYLIFE-II), 3–8 MJ range | HYLIFE-II; hif-technology-overview.md | h |
+| Repetition rate | 6 Hz (HYLIFE-II single chamber), 10–15 Hz target | HYLIFE-II; arxiv 2005.07520 | h |
+| Thermal efficiency | ~30–33% (steam Rankine, conventional) | HYLIFE-II; Z-IFE sCO2 study (Rankine baseline) | m |
+| Capacity factor / availability | Not explicitly stated; implied 80–85% | Meier 1986 (availability factor `a`) | l |
+| Tritium breeding ratio (TBR) | ~1.195 (HIBALL LiPb); viable with FLiBe (HYLIFE-II, not quantified per source) | HIBALL (KfK-3202) via dossier | m |
+| Fusion yield per shot | 350 MJ (HYLIFE-II at gain 70, 5 MJ driver) | HYLIFE-II; hif-technology-overview.md | h |
 
 **Missing Parameters**:
 
 | Parameter | Gap Type | Criticality | Notes |
 |-----------|----------|-------------|-------|
-| Plant availability / capacity factor | derivable | important | Not stated in sources; standard assumption ~75-85% for baseload fusion; use IFE convention |
-| Inflation-adjusted cost estimates | derivable | important | 1986 and 1990s dollar figures; need escalation to 2024$ via CEPCI or GDP deflator; no modern study provides this |
-| Thermal-to-electric conversion efficiency (explicit) | derivable | important | Steam Rankine ~30-35% is reasonable estimate, but sCO2 option (as in Z-IFE analog) would be ~45%; must choose and document |
-| Blanket/tritium processing cost (CAS 22.01) | not-yet-sourced | important | Not broken out in Meier 1986 three-part model; ARIES cost accounts framework applicable |
-| Decommissioning cost | derivable | nice-to-have | Standard IFE assumption; not concept-specific |
-| Construction time | not-yet-sourced | nice-to-have | Meier 1986 uses 8.3% FCR without explicit construction time; HYLIFE-II doesn't state it |
-| Target unit cost at production scale | truly-unknown | important | Meier 1986 explicitly acknowledges "no definitive studies"; semiconductor chip analogy only |
-| Full CAS-structured breakdown (CAS 20-27) | not-yet-sourced | important | Only three-part model exists (reactor/driver/factory); PyFECONS IFE module likely has CAS mapping |
+| Target unit cost at production scale | derivable | important | $0.1B factory ÷ shots/year gives ¢/target; Meier 1986 uses constant $0.1B factory; no per-target cost stated explicitly |
+| Cost escalation from 1986$–1990s$ to current year | derivable | important | ARIES CAS documentation (`aries_cost_account_documentation/output.md`) provides GDP IPD deflators; Hawker 2020 gives HYLIFE-II 2020$ reference point |
+| Recirculating power fraction | derivable | important | Driver power = $E_d \times \nu / \eta_{driver}$; not explicitly stated as % of gross output in any source |
+| Decommissioning cost | derivable | nice-to-have | No HIF-specific estimate; 10–15% of capital by analogy to fission |
+| Advanced cycle (sCO2) thermal efficiency | not-yet-sourced | nice-to-have | Z-IFE source covers sCO2 for z-pinch IFE; could apply by analogy; no HIF design specifies sCO2 |
+| Fixed vs. variable O&M breakdown | not-yet-sourced | nice-to-have | Meier 1986 uses flat 3% of capital; no maintenance schedule or consumable breakdown available |
+| Radioactive waste volumes / disposal cost | not-yet-sourced | important | Not characterized in any available source |
+| Capacity factor with quantified availability model | not-yet-sourced | important | Meier 1986 uses generic availability factor; no rep-rate-dependent downtime model |
 
 ---
 
 ## Source Recommendations
 
-1. **HYLIFE-II Full Final Report** (OSTI 7021072) — the full report likely contains detailed cost breakdowns, plant availability assumptions, and heat transport efficiency data not captured in the dossier summary. — `not-yet-sourced` — Search OSTI for OSTI:7021072 and companion reports (OSTI:7368768 "Improved heat transport system and steam power plant"). Confirm existence before searching.
+- **Full HIBALL report (KfK-3202, 1985)**: Search OSTI, IAEA INIS, or German KfK archive for the full KfK-3202 document. Key expected content: detailed CAS breakdown, LiPb blanket design parameters, complete plant cost table. *not-yet-sourced; search OSTI with "KfK-3202" or "HIBALL heavy ion" — confirm existence before searching.*
 
-2. **HIBALL Study** (KfK-3202, 1985) — full German/US report likely contains CAS-style cost breakdown and capacity factor assumptions not in the compiled overview. — `not-yet-sourced` — Search OSTI or European nuclear library for KfK-3202.
+- **Full HYLIFE-II final report (OSTI 7021072)**: Available at OSTI. `osti.gov/servlets/purl/7021072`. Would provide primary source for 940 MWe cost estimate, full CAS breakdown, FLiBe heat transport system. *not-yet-sourced; available at OSTI — high-value read before constructing LCOE model.*
 
-3. **PyFECONS IFE modules** (`/home/reid/PyFECONS`) — this codebase likely implements driver cost scaling and IFE-specific CAS mapping that could translate Meier 1986 formulas into a modern CAS structure and update dollar figures via built-in escalation. Directly applicable for CAS-structured cost gap.
+- **Multi-unit HYLIFE-II study (OSTI 10170594)**: Cited in dossier for multi-chamber MHD+Steam hybrid study. Would provide alternative energy conversion pathway and multi-unit learning curve data. *not-yet-sourced; search OSTI — `unverified — confirm existence before searching`.*
 
-4. **HIF Systems Assessment Project reports** (LBNL, ~1979-1992) — series of reports that culminated in HYLIFE-II; intermediate reports may contain detailed subsystem TRLs and cost breakdowns. — `not-yet-sourced` — `unverified — confirm existence before searching`; search OSTI for "heavy ion fusion systems assessment."
+- **Modern HIF target cost study**: Search LBNL technical reports or HEDP/IFE conference proceedings (IFSA, APS-DPP) for target fabrication cost at rep rate. Semiconductor fab analogy in Meier 1986 is the only reference; a dedicated manufacturing study is needed. *not-yet-sourced.*
 
-5. **Hawker 2020 IFE LCOE model** (`knowledge/sources/a_simplified_economic_model_for_inertial_fusion/`) — the 14-parameter technology-agnostic IFE LCOE model directly applicable to HIF. Provides methodology for handling missing parameters (gain, target cost, rep rate sensitivity). Already in the repo — read for LCOE methodology section.
+- **Li-6 supply chain for fusion (modern)**: The Giegerich 2019 (KIT) paper is excellent for methodology; a companion search for ITER/DEMO-specific supply quantity studies (ITER Organization, EUROfusion) would quantify fleet deployment constraints. *not-yet-sourced.*
 
-6. **ARIES cost accounts** (`knowledge/sources/aries_cost_account_documentation/`) — provides the CAS hierarchy (accounts 20-27) that can structure the three-part Meier cost model into a full CAS breakdown for cross-concept comparability.
+- **Fleet-wide source disqualifications** (sources read but not providing HIF-specific gap resolution):
+  - `aries_cost_account_documentation`: Opened (`output.md`, lines 1–80). Provides general CAS framework (accounts 20–27, 90–98) and GDP deflator tables useful for cost escalation. Does not contain HIF-specific cost data beyond what the Meier 1986 and HYLIFE-II sources already provide. Integrated for escalation methodology only.
+  - `energy_from_inertial_fusion` (Hogan 1992): Opened (`output.md`, lines 1–100). Confirms four-component IFE plant structure and Cascade reactor concept; no additional HIF cost or TRL data beyond what is in the concept-scoped sources. Consistent with — but does not extend — available data.
+  - `progress_toward_fusion_breakeven_lawson_criterion` (Wurzel & Hsu 2021): Opened (`output.md`, lines 1–80). Confirms ICF Lawson parameter compilation methodology; establishes that HIF experiments (NDCX-II) are in the WDM regime far below fusion-relevant parameters. Does not provide HIF-specific cost data but resolves physics TRL assessment basis.
+  - `osti-servlets-purl-901970.md` (Z-IFE SAND2006-7148, concept-scoped): This is a Z-pinch IFE source, not HIF. Driver technology is fundamentally different (linear transformer driver, recyclable transmission line). FLiBe chamber characterization and power conversion cycle comparison (sCO2, Rankine, Brayton) are applicable by analogy to HYLIFE-II, but no HIF-specific cost data is present.
 
 ---
 
 ## Summary
 
-The analysis can proceed to D1+ without additional source acquisition. The concept is exceptionally well-documented for a pre-commercial fusion approach: two full power plant designs (HIBALL, HYLIFE-II), a parametric economic model (Meier 1986), and multi-source confirmation of key physics parameters. The primary analytical work required is: (1) inflating 1986/1990s cost figures to contemporary dollars using CEPCI or GDP deflator, (2) mapping the Meier three-part cost model onto the CAS hierarchy using ARIES accounts (both sources already in the repo), (3) selecting a capacity factor assumption (~75-85%) with explicit justification, and (4) noting throughout that no current company exists and all design-choice parameters (blanket type, conversion cycle) reflect historical national lab selections rather than a committed design. PyFECONS IFE modules should be consulted before writing the capital cost section to avoid re-deriving what's already implemented.
+**Proceed to full analysis with stated caveats.** Heavy ion beam ICF has unusually rich documentation for a pre-commercial concept: two complete power plant design studies with cost estimates (HIBALL, HYLIFE-II), a dedicated parametric HIF economics analysis (Meier 1986), and a validated IFE LCOE methodology (Hawker 2020) that explicitly applies the HYLIFE-II baseline. The driver cost formula, reactor cost scaling, and COE range (3.9–9.8 ¢/kWh in 1986$, ~$3,600/kWe in 2020$) give a credible parametric basis.
+
+The analysis should acknowledge three systematic limitations: (1) all detailed cost data is 1980s–1990s vintage and requires explicit escalation using the GDP IPD methodology from `aries_cost_account_documentation`; (2) no ion-beam-driven ignition has been demonstrated — physics TRL remains ≤4, making the gain assumption (G~70) a paper extrapolation; and (3) the target injection and rep-rate challenge (10–15 Hz) has no experimental validation, creating a speculative floor on capacity factor. These are `important` qualifications, not `blocking` gaps — the available data is sufficient for a bracketed parametric LCOE estimate with appropriately stated uncertainty ranges.
+
+Acquiring the full HYLIFE-II report (OSTI 7021072) would be the single highest-value next action before finalizing subsystem cost values.
 
 ---
 
@@ -168,12 +183,12 @@
 ```yaml
 overall_rating: "Mostly Ready"
 blocking_count: 0
-important_count: 9
-counting_method: "all_sections_deduplicated — counting distinct important/blocking gaps across all 5 sections: (1) no modern cost study, (2) company non-existence, (3) chamber clearing dynamics, (4) target injection at rep rate, (5) systematic TRL assessment, (6) target factory cost at scale, (7) Li-6 supply chain timeline/cost, (8) Be supply chain for FLiBe, (9) plant availability/capacity factor assumption"
+important_count: 8
+counting_method: "all_sections_deduplicated — counted distinct gap items across §1-5 rated important: (1) target injection/rep-rate not demonstrated, (2) final-focus beam neutralization at full parameters, (3) ion-beam ignition not demonstrated, (4) no integrated driver prototype near plant parameters, (5) Li-6 enrichment supply chain, (6) Be supply chain for FLiBe, (7) target unit cost not explicitly quantified, (8) all capital cost data 1980s-1990s vintage requiring escalation"
 section_coverage:
   availability_of_data:       "Good"
-  system_function:            "Good"
+  system_function:            "Partial"
   subsystem_maturity:         "Partial"
   materials_supply_chain:     "Partial"
-  lcoe_parameter_extraction:  "Partial"
+  lcoe_parameter_extraction:  "Good"
 ```
\ No newline at end of file
```
