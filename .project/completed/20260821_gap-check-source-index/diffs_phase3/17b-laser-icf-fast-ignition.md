# Phase 3 diff: 17b-laser-icf-fast-ignition

**Generated:** 2026-05-22T14:36:01-07:00

## Counts (Phase 2 -> Phase 3 strict-read regen)

| field | phase2 | phase3 | Δ |
|-------|--------|--------|---|
| blocking_count   | 6 | 5 | -1 |
| important_count  | 8 | 7 | - |
| overall_rating   | Significant Gaps | Significant Gaps | - |

## Fleet-source dispositions in new report

```
```

## Forbidden-phrase check (should be empty)

```
(none — good)
```

## First line of new report (should start with `# Gap Assessment`)

```
# Gap Assessment: Laser ICF - Direct Drive Fast Ignition (D-T)
```

## Blocking-tier lines (new)

```
19:- Focused Energy plant study (J. Fusion Energy 2023) not ingested — not-yet-sourced — **blocking** (primary resolver for most quantitative gaps)
33:- Proton fast ignition coupling physics at ignition-relevant conditions not experimentally demonstrated — truly-unknown — **blocking** (fundamental to system function and gain curves)
47:- Proton fast ignition subsystem: physics TRL 2, ignition-scale demonstration absent — truly-unknown — **blocking**
96:| Net electrical output (MWe) | proprietary | blocking | "Gigawatt-scale" unquantified; no plant study |
97:| Gross thermal power (MWth) | proprietary | blocking | Required to compute efficiency and capital/kWe |
98:| Capital cost by CAS (direct costs, subsystem) | proprietary | blocking | No plant study; Meier 2006 total ~$3.9B for 1000 MWe CI (FI ~$2.7B analog) is severely dated |
99:| Combined wall-plug efficiency (compression + ignition laser) | not-yet-sourced | blocking | Two separate laser systems; FI uses 0.6–0.9 MJ compression + ~150 kJ ignitor; net η unclear |
100:| Target cost at Focused Energy design point (10 Hz, small yield, proton FI) | proprietary | blocking | FI target includes intermediate proton-generating target; Meier 2006 analog (17¢ for 6 Hz, 350 MJ) may not apply |
```

## Full unified diff (truncated to 400 lines)

```diff
--- /tmp/gap_phase2_state/17b-laser-icf-fast-ignition.md	2026-05-22 12:59:21.072602015 -0700
+++ /home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/17b-laser-icf-fast-ignition/gap_report.md	2026-05-22 14:36:01.225617816 -0700
@@ -1,198 +1,140 @@
-I have all the information needed. Here is the gap assessment:
-
----
-
-# Gap Assessment: Laser ICF — Direct Drive Fast Ignition (D-T)
-**Company**: Focused Energy | **Concept ID**: 17b-laser-icf-fast-ignition
-
----
+# Gap Assessment: Laser ICF - Direct Drive Fast Ignition (D-T)
 
 ## Overall Readiness
-
 **Rating**: Significant Gaps
-
-**Summary**: The available corpus is strong on concept-level description, physics framing, and general IFE economics methodology, but has near-zero Focused Energy-specific quantitative plant data. The central physics innovation — proton fast ignition coupling from laser-accelerated proton beams to a compressed core — has not been experimentally demonstrated at ignition-relevant scale. No public Focused Energy plant study exists; the closest analogs are the 2006 Meier HAPL/FI systems model and the Hawker 14-parameter IFE LCOE framework. A D1+ analysis is writable with explicit uncertainty framing and parametric bounding, but cannot produce well-grounded Focused Energy-specific cost estimates without additional sources.
+**Summary**: The available corpus covers system classification and qualitative architecture well (Callahan interview, LaserFocusWorld, PRNewswire) and provides a usable fast-ignition economics analog through Meier 2006 (LLNL HAPL systems code) and the technology-agnostic Hawker LCOE framework. However, Focused Energy has published no plant study, no capital cost breakdown, and no quantitative efficiency targets; the proton fast ignition mechanism has not been demonstrated at ignition-relevant scale; and most LCOE parameters must be inferred from 2006-era academic analogs. A D1+ qualitative analysis is feasible with stated assumptions; a quantitative LCOE model would require extensive acknowledged extrapolation.
 
 ---
 
 ## Section Coverage
 
 ### 1. Availability of Data
-
 **Coverage**: Partial
 
-**Available**:
-- Company-level concept description from the Focused Energy technology page (`iter-01/sources/focused-energy-technology`), the Callahan Physics World interview (`iter-02/sources/focused-energy-callahan-interview`), and the LaserFocusWorld profile (`iter-03/sources/laserfocusworld-…can-high`): establishes D-T fuel, two-pulse proton-FI architecture, ~10 Hz rep rate, steam cycle BOP, Li blanket with SRNL collaboration, and a 2030s pilot plant target.
-- PRNewswire 2024 (`iter-03/sources/prnewswire-…focused-energy-and-amplitude-enter`): >$175M raised, DOE Milestone-program participant (two milestones completed), $40M Amplitude DPSSL partnership, $65M Laser Development Facility in Bay Area.
-- Meier 2006 (`iter-03/sources/osti-servlets-purl-1438678`): the only publicly available economic systems model specifically studying FI laser IFE. Provides COE parametrics, target gain curves, driver cost assumptions ($400/J 2005 dollars), and a direct comparison of FI vs. CI economics under HAPL program assumptions.
-- Hawker LCOE model (`iter-03/sources/pmc-articles-pmc7658748`): technology-agnostic 14-parameter Monte Carlo IFE LCOE framework; directly applicable as an upper-envelope analysis.
-- Betti 2024 review (`iter-03/sources/osti-servlets-purl-2561299`): IFE physics requirements and laser driver technology landscape.
-- Optica OPN 2023 (`iter-03/sources/optica-opn-…features`): confirms Focused Energy timeline and fast ignition context relative to broader laser-fusion landscape.
-
-**Missing**:
-- Focused Energy J. Fusion Energy 2023 paper (Springer paywall): most likely best single public source for company-specific blanket chemistry, chamber, and plant-level parameters.
-- Any Focused Energy plant study or internal system model. No plant-scale techno-economic analysis for the Focused Energy approach exists in the public corpus.
-- Focused Energy ALP conference 2023 roadmap presentation (referenced externally).
-- World Nuclear News article on DOE Milestone-program progress (referenced in PRNewswire).
+**Available**: Public company communications establish the architectural envelope: direct-drive compression (DPSSL, Nd:glass) + short-pulse CPA proton ignition, D-T fuel, steam BOP, ~10 Hz rep rate, lithium blanket with SRNL tritium-extraction collaboration, and a pilot plant timeline of late 2030s (`iter-02/sources/focused-energy-callahan-interview.md`). The $40M Amplitude DPSSL partnership and $65M Laser Development Facility in the SF Bay Area confirm active DPSSL procurement (`iter-03/sources/prnewswire-…focused-energy-and-amplitude-enter.md`). The DOE Milestone-Based Fusion Development Program placement confirms institutional recognition. Academic IFE literature provides physics context (Betti 2024 status paper; Optica OPN June 2023) and one directly relevant fast-ignition economics study (Meier 2006, LLNL HAPL systems code, `iter-03/sources/osti-servlets-purl-1438678.md`). The technology-agnostic Hawker LCOE framework (`knowledge/sources/a_simplified_economic_model_for_inertial_fusion/output.md`) provides 14 parameterizable LCOE inputs that can be populated with analog values.
+
+**Missing**: Focused Energy has published no plant study with quantitative parameters. The referenced J. Fusion Energy 2023 Focused Energy concept paper (Springer paywall) is the most likely source for chamber geometry, blanket chemistry, and plant performance targets, but has not been ingested. No publicly accessible documents from Focused Energy specify net electrical output, thermal efficiency, capital cost structure, or first-wall design.
 
 **Gaps**:
-- Concept-specific plant study — `not-yet-sourced` (J. Fusion Energy 2023 is paywalled; DOE Milestone-program reports may be public) — **blocking**
-- Roadmap detail for phased development (pre-pilot → pilot → commercial) — `proprietary` — **important**
+- Focused Energy plant study (J. Fusion Energy 2023) not ingested — not-yet-sourced — **blocking** (primary resolver for most quantitative gaps)
+- APS DPP conference presentations and Focused Energy roadmap presentation (ALP 2023) referenced but not captured — not-yet-sourced — **important**
+- DOE Milestone-program technical reports (milestones 1 and 2 completed) not publicly available — proprietary — **important**
 
 ---
 
 ### 2. Challenges in Capturing System Function
-
 **Coverage**: Partial
 
-**Available**:
-- Two-pulse architecture is well-described: long-pulse DPSSL compression beams (400 kJ, 10 ns) + short-pulse CPA petawatt ignitor (150 kJ, ~100 fs) hitting a "nearby target" to produce a proton burst that ignites the compressed fuel.
-- Fundamental IFE system function challenges are covered by Betti and the Optica OPN review: laser-plasma instabilities in direct drive, chamber clearing at 10 Hz, target injection and tracking, final optics survivability.
-- Meier 2006 quantifies how recirculating power fraction (laser power draw) and target yield interact to determine net power and COE.
-- Callahan interview explicitly flags: chamber clearing at 10 Hz, target mass production at 10/second, and chamber materials as engineering challenges.
-
-**Missing**:
-- The fast ignition coupling mechanism (laser-accelerated proton beam coupling efficiency to the compressed core) is the core system function differentiator, and it remains experimentally unvalidated at ignition-relevant scale. The CSU proton-acceleration experiments (completed as DOE Milestone 2, per PRNewswire) are small-scale coupling tests, not ignition-scale validation.
-- Actual Focused Energy target geometry (cone-in-shell vs. flat foil vs. alternative) is not disclosed in the public corpus. The dossier notes it as a "nearby target" geometry without specifying the coupling geometry.
-- Chamber clearing mechanism and approach: no public disclosure.
-- Final optics protection strategy under neutron/debris exposure at 10 Hz: not addressed in Focused Energy-specific materials.
-- Beam-pointing precision required for the dual-beam (compression + ignition) architecture, and the tolerance budget between compression and ignition pulse timing.
+**Available**: The two-pulse architecture is qualitatively characterized: compression DPSSL beams + a separate 150 kJ short-pulse CPA ignitor that generates protons from a nearby target to heat the compressed fuel (`iter-03/sources/laserfocusworld-…can-high.md`; `iter-03/sources/osti-servlets-purl-1438678.md`). This "proton fast ignition" decouples compression uniformity from ignition energy deposition, in principle relaxing symmetry requirements relative to central ignition. The Meier 2006 HAPL systems code quantifies the economic implications of this two-system architecture: FI achieves ~15% lower COE than central ignition at 10 Hz (FI COE ~6.1 ¢/kWeh vs CI ~7.2 ¢/kWeh at 10 Hz, 3ω DPSSL), attributable to higher gain per unit driver energy. The Xcimer 2026 whitepaper (`knowledge/sources/commercialization_of_laser_fusion_energy/output.md`) identifies the specific engineering difficulties of DPSSL architectures at 10 Hz: multiple chamber penetrations (hundreds of beams) preclude thick-liquid-wall protection, driving toward a solid first-wall that accumulates ~10-20 dpa/year and requires 1-2 year replacement cycles. The Betti 2024 review (`iter-03/sources/osti-servlets-purl-2561299.md`) identifies chamber clearing at 10 Hz as a major unresolved challenge for IFE.
+
+**Missing**: Proton fast ignition coupling efficiency (how much of the proton energy reaches the compressed core) is not experimentally characterized at relevant scale — the CSU milestone demonstrated proton acceleration optimization, not coupling to a compressed target. The intermediate target geometry (often described as "cone-in-shell" in the academic literature) is not detailed in public Focused Energy materials. The interplay between the CPA pulse timing and the DPSSL compression pulse adds a synchronization challenge absent from central ignition concepts.
 
 **Gaps**:
-- Proton fast ignition coupling efficiency and experimental status — `not-yet-sourced` / `truly-unknown` (fundamental physics not yet resolved at relevant scale) — **blocking**
-- Target geometry/coupling design — `proprietary` — **blocking**
-- Chamber clearing mechanism — `proprietary` — **important**
-- Final optics survivability approach — `not-yet-sourced` — **important**
+- Proton fast ignition coupling physics at ignition-relevant conditions not experimentally demonstrated — truly-unknown — **blocking** (fundamental to system function and gain curves)
+- Intermediate target (proton-generating) geometry and integration not publicly specified — proprietary — **important**
+- 10 Hz chamber clearing dynamics with DPSSL beam ports not characterized for this specific architecture — not-yet-sourced — **important**
 
 ---
 
 ### 3. Maturity of Key Subsystems and Components
-
 **Coverage**: Partial
 
-**Available**:
-- Compression DPSSL (Nd:glass): mature technology for single-shot operation; kJ-class rep-rated systems being developed via Amplitude partnership (1 shot/60 seconds demonstrated, 10 Hz required for power plant). Technology target is "by the 2030s" (Ditmire, LaserFocusWorld).
-- CPA petawatt ignitor: 140 J / >10 PW demonstrated at Texas Petawatt; 2 kJ demonstrated at ELI Beamlines. Scaling to 150 kJ at rep rates is undemonstrated.
-- Target production: Pearl capsule in development at Darmstadt lab. General Atomics target factory cost studies (cited in Meier 2006) provide manufacturing cost scaling reference for direct-drive targets, not proton-FI geometry.
-- BOP (steam cycle): TRL 9, mature.
-- Tritium breeding/extraction: SRNL collaboration active; general Li-blanket tritium breeding is well-understood at laboratory scale; Focused Energy-specific blanket configuration unvalidated.
-- Proton fast ignition physics: Roth et al. 2001 established the concept; Focused Energy's CSU experiments completed (Milestone 2) but at demonstration scale far below ignition-relevant energy.
-
-**Missing**:
-- Formal TRL assessment for any Focused Energy subsystem — not published.
-- Rep-rated petawatt laser at 10 Hz with 150 kJ: not demonstrated anywhere; current best is ~1 shot/minute at kJ class.
-- Target mass production at 10/second rate: not demonstrated (NIF does ~400 shots/year; Focused Energy needs ~900,000/day).
-- Target injection and tracking at 10 Hz and the precision required: preliminary scoping studies only (Betti review notes linear induction accelerators at ~50 m/s and gas guns at ~400 m/s under investigation).
+**Available**: TRL context can be assembled from Betti 2024, Meier 2006, and Optica OPN 2023. DPSSL compression laser technology is at TRL 3-4: diode-pumped Nd:glass at IFE-relevant energy scales and repetition rates is the focus of the Amplitude partnership ($40M) but has not been demonstrated at power-plant parameters. Steam BOP is TRL 9 (conventional technology). Lithium tritium-breeding blankets have TRL 4-5 in fission programs; IFE-specific geometry validation has not been done. The Betti 2024 review explicitly states that target injection/tracking is "currently under initial stages of development" with only "preliminary scoping studies" completed, and that mass-production of wet-foam or liquid-DT targets is at TRL 2-3.
+
+**Missing**: The short-pulse CPA ignitor laser (150 kJ class, petawatt, high-rep-rate DPSSL) has no demonstrated analog at power-plant rep-rates. Current petawatt systems (ELI Beamlines, Texas Petawatt) fire at sub-Hz rates; the Focused Energy development facility aims for 1 shot per minute, still far from the 10 Hz power-plant target. No public TRL self-assessment from Focused Energy exists.
 
 **Gaps**:
-- Proton FI ignition coupling TRL — `truly-unknown` at power-plant-relevant scale — **blocking**
-- Rep-rated petawatt laser TRL — `not-yet-sourced` / `derivable` from laser community publications — **important**
-- Target mass production TRL and cost-reduction pathway — `proprietary` + `not-yet-sourced` — **important**
-- Target injection/tracking TRL at 10 Hz — `not-yet-sourced` — **important**
+- Proton fast ignition subsystem: physics TRL 2, ignition-scale demonstration absent — truly-unknown — **blocking**
+- Short-pulse CPA ignitor laser at 10 Hz rep-rate: TRL 2-3; no demonstrated path from current 1/min facility target to 10 Hz power plant — not-yet-sourced — **important**
+- Target injection and tracking at 10 Hz: TRL 1-2; preliminary scoping only (Betti 2024) — not-yet-sourced — **important**
+- Target mass-production at 900,000/day: TRL 2-3; no IFE company has demonstrated beyond lab-scale fabrication — not-yet-sourced — **important**
 
 ---
 
 ### 4. Key Materials and Supply Chain Considerations
-
 **Coverage**: Poor
 
-**Available**:
-- D fuel: seawater deuterium, no supply constraint.
-- T fuel: bred from Li; SRNL collaboration on extraction systems; tritium inventory and breeding ratio acknowledged as challenges.
-- Nd:glass gain medium: established supply chain for single-shot systems; 10 Hz thermal management requires active cooling (noted by Ditmire).
-- Laser diodes: identified as dominant capital cost driver for DPSSL power plants; Betti cites ~$0.01/W as required price point (current market ~$0.1–0.5/W, requiring ~10–50× cost reduction). Amplitude partnership represents supply chain development.
-- Target capsule: Pearl capsule development at Darmstadt; mass production at ~900,000/day is a stated engineering challenge.
-
-**Missing**:
-- Pearl capsule material composition (ablator material, DT ice layer thickness): proprietary.
-- First-wall material specification: Meier 2006 HAPL reference uses W-armor-coated ferritic steel for dry-wall chambers, which may be an applicable analog, but Focused Energy-specific design is undisclosed.
-- Blanket chemistry: specifically whether liquid Li, FLiBe, PbLi, or other form is used — proprietary per dossier.
-- Final optics supply chain: gratings, turning mirrors, and final optical components must withstand neutron flux and target debris at 10 Hz for ~30-year plant lifetime. No Focused Energy-specific data.
-- Optical component lifetime under neutron bombardment: a fundamental materials challenge noted in IFE literature but not addressed in Focused Energy-specific sources.
+**Available**: The Xcimer 2026 whitepaper (`knowledge/sources/commercialization_of_laser_fusion_energy/output.md`) provides the clearest available framing of DPSSL supply chain economics: diode-pumped solid-state lasers currently cost approximately $700–$1,000 per joule on-target, and Xcimer explicitly argues this makes DPSSL-based plants economically challenged. The Betti 2024 review (`iter-03/sources/osti-servlets-purl-2561299.md`) states that a diode cost of ~$0.01/W is required for cost-competitive DPSSL fusion, compared to current commercial diode prices of roughly $0.05–$0.10/W. Lithium supply for tritium breeding is a commodity-scale concern but not a critical constraint at initial deployment scale. Nd:glass gain media supply chain is mature from NIF/defense optics programs.
+
+**Missing**: Focused Energy has not disclosed target material specifications (ablator material, capsule shell composition), which are relevant to mass-production feasibility and supply chain. The blanket coolant/breeder chemistry (FLiBe, LiPb, liquid Li) is undisclosed; each carries different materials challenges (FLiBe requires beryllium supply; LiPb requires lead; liquid Li is flammable). Diode laser manufacturing scale-up roadmap (Amplitude partnership scope) not publicly detailed.
 
 **Gaps**:
-- Blanket chemistry — `proprietary` — **important**
-- First-wall material and design — `not-yet-sourced` (HAPL analog available) — **important**
-- Final optics survivability / supply chain — `not-yet-sourced` — **important**
-- Laser diode cost reduction pathway and supply chain scalability — `not-yet-sourced` — **important**
-- Target capsule materials and mass production supply chain — `proprietary` — **important**
+- DPSSL diode laser cost reduction pathway to $0.01/W not documented for Focused Energy's timeline — proprietary — **important**
+- Target ablator and shell material specifications not public — proprietary — **important**
+- Blanket chemistry (FLiBe vs LiPb vs liquid Li) undisclosed; each has distinct Be, Pb, or Li supply chain and activation implications — proprietary — **important**
+- Frequency-doubling crystal supply (KDP/DKDP) for DPSSL compression beams at 10 Hz and multi-MJ scale not addressed — not-yet-sourced — **nice-to-have**
 
 ---
 
 ### 5. LCOE Parameter Extraction
+**Coverage**: Poor
 
 **Available Parameters**:
 
 | Parameter | Value/Range | Source | Confidence |
-|---|---|---|---|
-| Rep rate | ~10 Hz | Callahan interview | h |
-| Energy capture mode | Conventional steam cycle | Callahan interview | h |
-| Laser wall-plug efficiency (target) | ~10% (DPSSL) | Callahan + Betti | m |
-| Brayton cycle efficiency (HAPL reference) | 48% | Meier 2006 | l (analog, not FE-specific) |
-| Target gain requirement (min) | >50–100 (general IFE); FI theoretically 3–4× CI | Callahan + Meier 2006 | m |
-| FI plant COE reference (HAPL model) | ~5.9–6.1 ¢/kWeh at 10 Hz, ~0.9 MJ driver energy | Meier 2006 | l (2006, HAPL params) |
-| Laser capital cost reference | $400/J (2005 dollars, DPSSL) | Meier 2006 | l (dated) |
-| Target factory capital cost (GA study) | $136M for 350 MJ targets at 6 Hz (~1 GWe) | Meier 2006 (citing GA) | l (different yield, Hz, dated) |
-| Target cost threshold (cost-competitive) | ~$10/target | Hawker | m (generic model bound) |
-| Plant cost analogy (BOP) | $1,000–6,000/kWe | Hawker | l (wide range) |
-| O&M cost range (generic IFE) | $10–100/kWe-yr | Hawker | l (wide range) |
-| Auxiliary recirculating power | ~4% of gross electric (HAPL reference) | Meier 2006 | l (analog) |
-| Capacity factor (HAPL assumption) | 85% | Meier 2006 | l (assumption) |
-| Indirect capital cost multiplier | 1.936× direct capital cost | Meier 2006 | m (standard CAS convention) |
-| Fixed charge rate | 9.66% | Meier 2006 | m (standard; choice-dependent) |
-| Total investment raised (2024) | >$175M | PRNewswire | h |
-| Facility cost (ignition, rough estimate) | ~$3 billion | LaserFocusWorld / Ditmire | l (rough; ignition facility, not power plant) |
-| Driver energy optimum (FI, Meier model) | 0.6–0.9 MJ (at 10–21 Hz) | Meier 2006 | l (2006 parameters) |
-| Plant size reference | 750–1,250 MWe range | Meier 2006 | l (parametric range, not FE-specific) |
+|-----------|-------------|--------|------------|
+| Rep rate (power plant) | ~10 Hz | Callahan interview (`iter-02`) | h |
+| Energy conversion | Steam (conventional) | Callahan interview (`iter-02`) | h |
+| Target gain required (plant) | 50–100 | Callahan interview (`iter-02`) | h |
+| Driver wall-plug efficiency target | ~10% | Callahan interview (`iter-02`); Betti 2024 (`iter-03`) | m |
+| ηwp × G product required | >10 | Betti 2024 (`iter-03`) | h |
+| Fast ignition COE analog (2006$) | ~5.9–6.1 ¢/kWeh at 10 Hz, 1000 MWe, 3ω DPSSL | Meier 2006 (`iter-03`) | l (dated analog) |
+| FI optimal driver energy | 0.6 MJ unconstrained / 0.9 MJ at 10 Hz limit | Meier 2006 (`iter-03`) | l (analog) |
+| DPSSL laser cost (HAPL reference) | $400/J (2006$) | Meier 2006 (`iter-03`) | l (2006 estimate) |
+| DPSSL laser cost (modern, DPSSL) | $700–1,000/J | Xcimer 2026 (`knowledge/sources/commercialization_of_laser_fusion_energy/`) | m |
+| Target factory cost analog (6 Hz, 350 MJ) | $136M capital; ~17¢/target at 6 Hz | Meier 2006 (`iter-03`) | l (analog, dated) |
+| Plant capacity factor (HAPL assumed) | 85% | Meier 2006 (`iter-03`) | m (IFE convention) |
+| Brayton cycle efficiency (HAPL analog) | 48% | Meier 2006 (`iter-03`) | l (for steam cycle, override to ~35%) |
+| Steam cycle expected efficiency | ~33–38% (conventional) | General BOP knowledge | m |
+| Plant scale claim | "gigawatt-scale" | Callahan interview (`iter-02`) | l (unquantified) |
+| Total funding raised | >$175M | PRNewswire 2024 (`iter-03`) | h |
 
 **Missing Parameters**:
 
 | Parameter | Gap Type | Criticality | Notes |
-|---|---|---|---|
-| Target yield per shot (MJ fusion per shot) | `proprietary` | Blocking | Central driver of LCOE; "lower yield per shot" stated but no value. Determines chamber design, target factory, and rep-rate economics |
-| Target gain at power plant conditions | `proprietary` | Blocking | FI gain ×3–4 over CI is generic; Focused Energy-specific gain curve not public |
-| Gross/net electrical output | `proprietary` + `not-yet-sourced` | Blocking | "Gigawatt-scale" cited without specifics; no plant study exists |
-| Net plant efficiency (steam + recirculating) | `derivable` (analogs available) | Blocking | Can bound using Meier 2006 assumptions; Focused Energy-specific unknown |
-| Capital cost breakdown by CAS subsystem | `not-yet-sourced` | Blocking | Meier 2006 provides structure for FI laser IFE; needs Focused Energy-specific driver/chamber adaptation |
-| DPSSL cost $/J at 10 Hz (current era) | `not-yet-sourced` | Blocking | Meier 2006's $400/J is ~20 years old; laser diode cost has dropped but DPSSL system cost curve at 10 Hz for power plant not re-established publicly |
-| Target cost at mass production scale | `proprietary` + `derivable` | Blocking | Target cost is the #3 LCOE driver (Hawker); mass production cost for proton-FI target geometry completely uncharacterized publicly |
-| Blanket TBR and tritium self-sufficiency margin | `proprietary` | Important | Affects startup tritium inventory and plant economics |
-| Blanket capital cost | `not-yet-sourced` | Important | Meier 2006 uses liquid Li coolant/breeder; Focused Energy chemistry unknown |
-| First-wall replacement schedule and cost | `not-yet-sourced` | Important | Neutron damage to dry wall is a key O&M cost driver |
-| Chamber cost scaling | `derivable` (HAPL analog) | Important | Meier 2006 dry-wall chamber cost scaling with yield is best available analog |
-| O&M cost (Focused Energy-specific) | `derivable` (analogs) | Important | IFE ranges from Hawker ($10–100/kWe-yr) and Meier 2006 can bound this |
-| Capacity factor (first plant) | `derivable` | Important | 85% (Meier 2006) is likely optimistic for early plant; 70–80% more realistic |
-| Decommissioning cost | `derivable` | Nice-to-have | Standard fusion decommissioning conventions applicable |
+|-----------|----------|-------------|-------|
+| Net electrical output (MWe) | proprietary | blocking | "Gigawatt-scale" unquantified; no plant study |
+| Gross thermal power (MWth) | proprietary | blocking | Required to compute efficiency and capital/kWe |
+| Capital cost by CAS (direct costs, subsystem) | proprietary | blocking | No plant study; Meier 2006 total ~$3.9B for 1000 MWe CI (FI ~$2.7B analog) is severely dated |
+| Combined wall-plug efficiency (compression + ignition laser) | not-yet-sourced | blocking | Two separate laser systems; FI uses 0.6–0.9 MJ compression + ~150 kJ ignitor; net η unclear |
+| Target cost at Focused Energy design point (10 Hz, small yield, proton FI) | proprietary | blocking | FI target includes intermediate proton-generating target; Meier 2006 analog (17¢ for 6 Hz, 350 MJ) may not apply |
+| Laser cost $/J for Focused Energy's DPSSL architecture | proprietary | important | Xcimer gives $700–1000/J bound for DPSSL; this partially closes the gap but does not provide FE's cost projection — downgraded from blocking given Xcimer analog |
+| First-wall material and replacement schedule | proprietary | important | Dry-wall expected; Xcimer quantifies 1–2 year replacement cycle for dry-wall IFE at 10 Hz |
+| O&M cost ($/kWe-yr) | proprietary | important | No published FE data; Meier 2006 states O&M dominates target factory costs |
+| Blanket multiplier and TBR | proprietary | important | Blanket chemistry undisclosed; TBR > 1 required (Betti 2024) |
+| Construction cost and timeline | proprietary | important | Pilot plant "late 2030s"; no costing disclosed |
 
 ---
 
 ## Source Recommendations
 
-1. **Focused Energy J. Fusion Energy 2023** (Springer, paywalled): Most important single gap-filling document for blanket chemistry, chamber specifics, and plant-level parameters. Search: `site:springer.com "Focused Energy" "inertial fusion"` or via DOI lookup. Alternatively, contact authors directly. — `not-yet-sourced`; **exists, confirm access via interlibrary loan**
+**Fleet-wide sources integrated into this assessment:**
+
+- `knowledge/sources/a_simplified_economic_model_for_inertial_fusion/` (Hawker 2020) — **Integrated.** The 14-parameter technology-agnostic IFE LCOE model is directly applicable to Focused Energy. Key insight: LCOE as low as $25/MWh requires gain >500 and yield >5 GJ per shot — parameters well above Focused Energy's ~10 Hz / lower-yield approach. This framework allows populating an LCOE estimate with available analog values, but identifies gain and yield per shot as the most sensitive parameters that Focused Energy has not quantified publicly. Does not address the proton fast ignition gap; partially closes LCOE framework gap (not a blocking resolver).
 
-2. **LLNL Generalized Economics Model (GEM) for IFE** (referenced in `iter-03/sources/llnl-53961-…`): GEM is publicly downloadable at `lift.llnl.gov/resources/gem`. Designed for DPSSL + dry-wall IFE with liquid Li breeder — directly applicable to the Focused Energy architecture as a parametric economic tool. This is a free tool that could provide the updated (post-2006) IFE cost model. — **confirmed to exist; download and apply**
+- `knowledge/sources/commercialization_of_laser_fusion_energy/` (Xcimer 2026) — **Integrated.** Provides the most current quantification of DPSSL laser costs ($700–1,000/J on-target), the physical constraints on solid-state laser IFE at 10 Hz (hundreds of beam ports preclude thick-liquid walls; solid first-wall replacement every 1–2 years), and an explicit explanation of why DPSSL supply chains face commercialization challenges. This source directly addresses the laser cost gap for Focused Energy's DPSSL architecture, downgrading the laser cost $/J gap from blocking to important, since a defensible upper bound ($700–1000/J) can now be cited.
 
-3. **LLNL Integrated Process Model (IPM) for IFE** (mentioned in same source): a more full-featured version of GEM available for purchase via software licensing. May provide Focused Energy-architecture-level detail for system cost by CAS account. — `unverified — confirm scope before purchasing`
+- `knowledge/sources/affordable_manageable_practical_and_scalable_amps_high/` (Pacific Fusion 2025) — **Disqualified.** This paper covers pulser-driven (MagLIF) IFE, not laser fast ignition. It benchmarks NIF and discusses pulsed-power architectures but provides no laser cost data, DPSSL parameters, or fast-ignition subsystem information relevant to Focused Energy's concept. It does not address any gap in sections 1–5 of this assessment.
 
-4. **Meier & Hogan 2006, "Power Plant and Chamber Considerations for Fast Ignition," Fus. Sci. Technol. 49:532**: Companion to Meier 2006 in corpus; explicitly addresses chamber design for FI power plants. Search OSTI for UCRL document number. — `not-yet-sourced`; **high value — directly FI-specific**
+**Gap-specific source recommendations:**
 
-5. **DOE Milestone-Based Fusion Development Program technical reports for Focused Energy**: DOE Milestone-program requires public milestone reports. Focused Energy has completed at least 2 milestones. Search at `fusionenergy.energy.gov` or DOE OSTI for Focused Energy milestone reports. — `not-yet-sourced`; **may contain target design and physics validation data**
+- **Focused Energy J. Fusion Energy 2023 (Springer paywall)**: The highest-priority gap resolver. Likely contains blanket chemistry, chamber design, and plant performance targets. *Recommendation*: Acquire via institutional access or author request. `not-yet-sourced — confirm existence before searching` (referenced in dossier as known paywalled source).
 
-6. **Roth et al. 2001 (Phys. Rev. Lett. 86:436)** "Fast ignition by intense laser-accelerated proton beam" and **Tabak et al. 2005 (Phys. Plasmas 12:057305)** "Review of progress in Fast Ignition": foundational fast ignition physics references cited in the corpus but not ingested. Needed for physics-basis and coupling efficiency context. — `not-yet-sourced`; **confirmed to exist**
+- **LLNL GEM (Generalized Economics Model for Fusion Technology)**: Publicly available Excel spreadsheet tool (`iter-03/sources/llnl-53961-llnl-releases-generalized-economics-model-fusion.md`). Calibrated to DPSSL/dry-wall/liquid-Li IFE with HAPL heritage. Running GEM with fast-ignition gain curve assumptions (from Meier 2006 FI curves) would produce a plant-level LCOE estimate that could serve as a structured analog. The GEM user guide PDF should be downloaded from `lift.llnl.gov/resources/gem` and assessed for FI parameter inputs.
 
-7. **Xcimer Energy commercialization whitepaper** (`knowledge/sources/commercialization_of_laser_fusion_energy/`): already registered in the fleet-wide source index. Provides the most current (2026) laser cost breakdown by component ($<100/J for KrF, vs. $700–1000/J for DPSSL heritage systems). Use as an upper-bound analog for DPSSL cost — noting KrF is a different architecture — to constrain the laser capital cost uncertainty. — **read this fleet-wide source**
+- **HAPL program IFE power plant design reports**: The Meier 2006 reference cites HAPL design work (Sethian et al. 2003; Meier & Hogan 2006 chamber paper) with more detailed FI chamber and BOP assumptions. Search OSTI for "High Average Power Laser fast ignition power plant." `not-yet-sourced — likely exists, unverified`.
 
-8. **ARIES Cost Account Documentation** (`knowledge/sources/aries_cost_account_documentation/`): already registered. Use to populate the CAS structure for a Focused Energy plant study analog (accounts 20–27 direct, 90–98 indirect). Essential for the capital cost breakdown section. — **read this fleet-wide source for CAS framework application**
+- **Focused Energy DOE Milestone technical reports**: DOE Milestone-Based Fusion Development Program milestone reports are sometimes publicly released. Search DOE's LIFT/FES portal for Focused Energy milestone submissions. `not-yet-sourced — confirm availability`.
+
+- **Amplitude DPSSL development specifications**: The $40M Focused Energy–Amplitude agreement may have produced public technical briefings specifying DPSSL kilo-joule class parameters, rep rate, and cost projections. Search conference proceedings (SPIE High Power Laser Science, ICUIL 2024-2025). `not-yet-sourced — confirm existence before searching`.
 
 ---
 
 ## Summary
 
-The available corpus supports a D1+ analysis at the level of **a well-bounded parametric estimate with high uncertainty on all concept-specific inputs.** The strongest assets are: (1) Meier 2006, which provides the only published FI-specific economic systems model and can be adapted as an analog; (2) the Hawker 14-parameter model, which establishes what drives IFE LCOE without concept-specific inputs; and (3) the PRNewswire/Callahan/LaserFocusWorld sources, which establish the architecture and development trajectory.
-
-The principal gap is that **Focused Energy has no public plant study**, and its central physics claim — proton fast ignition coupling efficiency at ignition-relevant scale — is **pre-experimental validation**. This makes the concept simultaneously interesting (the FI gain advantage, if achieved, meaningfully reduces COE per Meier 2006) and fundamentally uncertain (the gain advantage depends on physics not yet demonstrated).
+The corpus is sufficient for a D1+ qualitative analysis covering system description, architecture classification, physics challenges, subsystem maturity, and a high-level LCOE sensitivity framework (using Meier 2006 fast-ignition analog values and the Hawker 14-parameter model structure). The concept's taxonomy columns are well-supported. However, five blocking gaps prevent a credible quantitative LCOE estimate without significant stated assumptions: (1) no accessible plant study; (2) net electrical output and thermal power unknown; (3) combined wall-plug efficiency for the two-system laser architecture undetermined; (4) proton fast ignition not demonstrated at ignition-relevant scale, making FI gain curves speculative; and (5) target cost at the Focused Energy design point (small yield, two-component target, 10 Hz) not published.
 
-**Recommended path before analysis**: Download the LLNL GEM tool (confirmed public) and attempt to obtain the Focused Energy J. Fusion Energy 2023 paper. If the J. Fusion Energy paper cannot be obtained, proceed with Meier 2006 as the primary analog, explicitly flagging that all quantitative LCOE outputs carry ±50% uncertainty due to missing Focused Energy-specific parameters.
+**Recommendation**: Proceed to full D1+ analysis with the following structure: (a) qualitative and maturity sections can be completed with high confidence from current sources; (b) LCOE section should use Meier 2006 FI economics as the primary analog with Xcimer DPSSL cost framing as an upper bound, explicitly flagging all values as analogs with stated vintage and deviation risk; (c) acquire the Focused Energy J. Fusion Energy 2023 paper and download the LLNL GEM tool before attempting to produce a quantitative capital cost breakdown.
 
 ---
 
@@ -200,13 +142,13 @@
 
 ```yaml
 overall_rating: "Significant Gaps"
-blocking_count: 6
-important_count: 8
-counting_method: "all_sections_deduplicated — blocking: (1) proton FI coupling physics unvalidated, (2) target gain/yield specifics proprietary, (3) gross/net electrical output unknown, (4) net plant efficiency derivable only from aged analogs, (5) capital cost by CAS subsystem (no FE plant study), (6) DPSSL cost $/J current era not-yet-sourced; important: blanket chemistry, first-wall design, rep-rated PW laser TRL, target mass production TRL, target injection/tracking TRL, blanket capital cost, first-wall O&M cost, DPSSL diode supply chain"
+blocking_count: 5
+important_count: 7
+counting_method: "all_sections_deduplicated — five blocking gaps: (1) no plant study/capital cost, (2) net electrical output, (3) combined wall-plug efficiency two-system, (4) proton FI physics unvalidated, (5) target cost at FE design point; seven important gaps: laser cost $/J (DPSSL upper bound from Xcimer reduces from blocking), O&M cost, short-pulse ignitor architecture, first-wall material/replacement, blanket chemistry, DPSSL diode supply chain, target material specs"
 section_coverage:
   availability_of_data:       "Partial"
   system_function:            "Partial"
   subsystem_maturity:         "Partial"
   materials_supply_chain:     "Poor"
-  lcoe_parameter_extraction:  "Partial"
+  lcoe_parameter_extraction:  "Poor"
 ```
\ No newline at end of file
```
