# Diff: 17b-laser-icf-fast-ignition

**Generated:** 2026-05-22T10:29:07-07:00

## Counts

| field | baseline | new | Δ |
|-------|----------|-----|---|
| blocking_count   | 6 | 6 | 0 |
| important_count  | 7 | 8 | - |
| overall_rating   | Significant Gaps | Significant Gaps | - |

## Fleet-source citations (new only — grep `knowledge/sources/` or `PyFECONS`)

```
183:7. **Xcimer Energy commercialization whitepaper** (`knowledge/sources/commercialization_of_laser_fusion_energy/`): already registered in the fleet-wide source index. Provides the most current (2026) laser cost breakdown by component ($<100/J for KrF, vs. $700–1000/J for DPSSL heritage systems). Use as an upper-bound analog for DPSSL cost — noting KrF is a different architecture — to constrain the laser capital cost uncertainty. — **read this fleet-wide source**
185:8. **ARIES Cost Account Documentation** (`knowledge/sources/aries_cost_account_documentation/`): already registered. Use to populate the CAS structure for a Focused Energy plant study analog (accounts 20–27 direct, 90–98 indirect). Essential for the capital cost breakdown section. — **read this fleet-wide source for CAS framework application**
```

## Blocking-tier lines (baseline)

```
34:- J. Fusion Energy 2023 paper content — `not-yet-sourced` — **blocking**: this is the primary peer-reviewed technical disclosure and likely contains chamber design, gain calculations, and subsystem details
57:- Laser energy per shot (compression) — `proprietary` (or in the 2023 paper) — **blocking**: without this, fusion yield per shot cannot be computed, and plant power cannot be derived
58:- Proton fast ignition coupling efficiency — `not-yet-sourced` — **blocking**: fundamental to whether gain >50 is achievable; some data may exist in HEDP literature (e.g., Nuckolls, Tabak, or Roth group publications)
80:- 10 Hz petawatt laser — `truly-unknown` (at this scale, doesn't exist anywhere) — **blocking** for viability assessment; need to note as critical long-pole
81:- High-throughput target factory (900k targets/day) — `truly-unknown` at production scale — **blocking** for LCOE (target cost is a dominant operating cost driver for IFE)
104:- Pearl capsule + cone (if fast ignition) fabrication at 900k/day — `truly-unknown` at that volume — **blocking**: this is one of the hardest unsolved problems in IFE economics; no factory exists; estimated costs in academic literature range from $0.10–$1.00+/target
```

## Blocking-tier lines (new)

```
39:- Concept-specific plant study — `not-yet-sourced` (J. Fusion Energy 2023 is paywalled; DOE Milestone-program reports may be public) — **blocking**
62:- Proton fast ignition coupling efficiency and experimental status — `not-yet-sourced` / `truly-unknown` (fundamental physics not yet resolved at relevant scale) — **blocking**
63:- Target geometry/coupling design — `proprietary` — **blocking**
88:- Proton FI ignition coupling TRL — `truly-unknown` at power-plant-relevant scale — **blocking**
```

## Full unified diff (truncated to 400 lines)

```diff
--- /tmp/gap_baselines_2026-05-22/17b-laser-icf-fast-ignition.md	2026-05-22 09:21:13.858421242 -0700
+++ /home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/17b-laser-icf-fast-ignition/gap_report.md	2026-05-22 10:29:07.066352167 -0700
@@ -1,184 +1,212 @@
-I have all the information I need. Let me write the gap assessment report.
+I have all the information needed. Here is the gap assessment:
 
 ---
 
-# Gap Assessment: Laser ICF - Fast Ignition (D-T)
+# Gap Assessment: Laser ICF — Direct Drive Fast Ignition (D-T)
+**Company**: Focused Energy | **Concept ID**: 17b-laser-icf-fast-ignition
+
+---
 
 ## Overall Readiness
+
 **Rating**: Significant Gaps
 
-**Summary**: Focused Energy's fast ignition concept has reasonable public disclosure on its physics approach, laser technology, and high-level power plant targets, but is missing nearly all quantitative plant-level parameters needed for LCOE modeling. The chamber design, target fabrication costs, capital cost structure, and net efficiency are either proprietary or not yet surfaced from available sources. Enough scaffolding exists for a qualitative write-up and a heavily assumption-laden quantitative model, but the analysis will carry large stated uncertainties throughout.
+**Summary**: The available corpus is strong on concept-level description, physics framing, and general IFE economics methodology, but has near-zero Focused Energy-specific quantitative plant data. The central physics innovation — proton fast ignition coupling from laser-accelerated proton beams to a compressed core — has not been experimentally demonstrated at ignition-relevant scale. No public Focused Energy plant study exists; the closest analogs are the 2006 Meier HAPL/FI systems model and the Hawker 14-parameter IFE LCOE framework. A D1+ analysis is writable with explicit uncertainty framing and parametric bounding, but cannot produce well-grounded Focused Energy-specific cost estimates without additional sources.
 
 ---
 
 ## Section Coverage
 
 ### 1. Availability of Data
+
 **Coverage**: Partial
 
 **Available**:
-- Physics approach (DPSSL compression + petawatt proton fast ignition) is clearly documented in `focused-energy-technology.md` and the Callahan interview
-- Company technology page and interview cover: target gain requirement (>50), rep rate (~10 Hz), wall-plug efficiency (~10%), energy conversion (steam cycle), fuel (D-T), target geometry (Pearl capsule, ~4 mm)
-- Lab demonstration basis: OMEGA (direct drive ICF), CSU (proton fast ignition milestone per DOE program)
-- Roadmap timeline: T-STAR facility (2028), LightHouse pilot plant (end of 2030s)
-- Amplitude partnership details ($40M, DPSSL development)
-- DOE milestone completion: high-gain target design report
+- Company-level concept description from the Focused Energy technology page (`iter-01/sources/focused-energy-technology`), the Callahan Physics World interview (`iter-02/sources/focused-energy-callahan-interview`), and the LaserFocusWorld profile (`iter-03/sources/laserfocusworld-…can-high`): establishes D-T fuel, two-pulse proton-FI architecture, ~10 Hz rep rate, steam cycle BOP, Li blanket with SRNL collaboration, and a 2030s pilot plant target.
+- PRNewswire 2024 (`iter-03/sources/prnewswire-…focused-energy-and-amplitude-enter`): >$175M raised, DOE Milestone-program participant (two milestones completed), $40M Amplitude DPSSL partnership, $65M Laser Development Facility in Bay Area.
+- Meier 2006 (`iter-03/sources/osti-servlets-purl-1438678`): the only publicly available economic systems model specifically studying FI laser IFE. Provides COE parametrics, target gain curves, driver cost assumptions ($400/J 2005 dollars), and a direct comparison of FI vs. CI economics under HAPL program assumptions.
+- Hawker LCOE model (`iter-03/sources/pmc-articles-pmc7658748`): technology-agnostic 14-parameter Monte Carlo IFE LCOE framework; directly applicable as an upper-envelope analysis.
+- Betti 2024 review (`iter-03/sources/osti-servlets-purl-2561299`): IFE physics requirements and laser driver technology landscape.
+- Optica OPN 2023 (`iter-03/sources/optica-opn-…features`): confirms Focused Energy timeline and fast ignition context relative to broader laser-fusion landscape.
 
 **Missing**:
-- Full text of Focused Energy J. Fusion Energy 2023 paper (accessed abstract only, behind Springer paywall) — likely the primary technical reference
-- FE ALP conference roadmap PDF (listed in dossier key sources but not extracted)
-- World Nuclear News DOE milestones article (not extracted)
-- Any published plant study or system code output
+- Focused Energy J. Fusion Energy 2023 paper (Springer paywall): most likely best single public source for company-specific blanket chemistry, chamber, and plant-level parameters.
+- Any Focused Energy plant study or internal system model. No plant-scale techno-economic analysis for the Focused Energy approach exists in the public corpus.
+- Focused Energy ALP conference 2023 roadmap presentation (referenced externally).
+- World Nuclear News article on DOE Milestone-program progress (referenced in PRNewswire).
 
 **Gaps**:
-- J. Fusion Energy 2023 paper content — `not-yet-sourced` — **blocking**: this is the primary peer-reviewed technical disclosure and likely contains chamber design, gain calculations, and subsystem details
-- ALP roadmap PDF — `not-yet-sourced` — **important**: may contain quantitative milestones, target energy, and subsystem TRLs
-- Any IFE plant study using fast ignition driver (academic or HEDP community) — `not-yet-sourced` — **important**
+- Concept-specific plant study — `not-yet-sourced` (J. Fusion Energy 2023 is paywalled; DOE Milestone-program reports may be public) — **blocking**
+- Roadmap detail for phased development (pre-pilot → pilot → commercial) — `proprietary` — **important**
 
 ---
 
 ### 2. Challenges in Capturing System Function
+
 **Coverage**: Partial
 
 **Available**:
-- The two-step fast ignition physics (separate compression + ignition) is well explained in public sources; the Callahan interview provides the conceptual narrative
-- The key physics requirement (gain >50, rep rate ~10 Hz, WPE ~10%) is quantified
-- Proton fast ignition as ignition mechanism is described; lab demonstrations cited (CSU)
-- The "separation of compression from ignition" as the central architectural claim is clearly stated
+- Two-pulse architecture is well-described: long-pulse DPSSL compression beams (400 kJ, 10 ns) + short-pulse CPA petawatt ignitor (150 kJ, ~100 fs) hitting a "nearby target" to produce a proton burst that ignites the compressed fuel.
+- Fundamental IFE system function challenges are covered by Betti and the Optica OPN review: laser-plasma instabilities in direct drive, chamber clearing at 10 Hz, target injection and tracking, final optics survivability.
+- Meier 2006 quantifies how recirculating power fraction (laser power draw) and target yield interact to determine net power and COE.
+- Callahan interview explicitly flags: chamber clearing at 10 Hz, target mass production at 10/second, and chamber materials as engineering challenges.
 
 **Missing**:
-- Compression laser energy per shot (needed to compute fusion yield = gain × laser energy)
-- Proton beam parameters (energy, current, focal spot diameter) — fast ignition coupling efficiency depends critically on these
-- Cone-in-shell target geometry details (implied by proton fast ignition but not explicitly confirmed)
-- Quantified ignition energy threshold vs. achievable proton delivery
-- Recirculating power fraction (laser WPE determines how much plant output is recycled)
+- The fast ignition coupling mechanism (laser-accelerated proton beam coupling efficiency to the compressed core) is the core system function differentiator, and it remains experimentally unvalidated at ignition-relevant scale. The CSU proton-acceleration experiments (completed as DOE Milestone 2, per PRNewswire) are small-scale coupling tests, not ignition-scale validation.
+- Actual Focused Energy target geometry (cone-in-shell vs. flat foil vs. alternative) is not disclosed in the public corpus. The dossier notes it as a "nearby target" geometry without specifying the coupling geometry.
+- Chamber clearing mechanism and approach: no public disclosure.
+- Final optics protection strategy under neutron/debris exposure at 10 Hz: not addressed in Focused Energy-specific materials.
+- Beam-pointing precision required for the dual-beam (compression + ignition) architecture, and the tolerance budget between compression and ignition pulse timing.
 
 **Gaps**:
-- Laser energy per shot (compression) — `proprietary` (or in the 2023 paper) — **blocking**: without this, fusion yield per shot cannot be computed, and plant power cannot be derived
-- Proton fast ignition coupling efficiency — `not-yet-sourced` — **blocking**: fundamental to whether gain >50 is achievable; some data may exist in HEDP literature (e.g., Nuckolls, Tabak, or Roth group publications)
-- Recirculating power / net electrical fraction — `derivable` with assumptions — **important**: at 10% WPE and gain 50, recirculating power is a major fraction of gross output
+- Proton fast ignition coupling efficiency and experimental status — `not-yet-sourced` / `truly-unknown` (fundamental physics not yet resolved at relevant scale) — **blocking**
+- Target geometry/coupling design — `proprietary` — **blocking**
+- Chamber clearing mechanism — `proprietary` — **important**
+- Final optics survivability approach — `not-yet-sourced` — **important**
 
 ---
 
 ### 3. Maturity of Key Subsystems and Components
+
 **Coverage**: Partial
 
 **Available**:
-- DPSSL (compression): 10% WPE confirmed as target, Amplitude partnership established, 3 kJ demonstrator planned — early TRL (3-4)
-- Petawatt ignition laser: class exists commercially (e.g., Amplitude's Sequoia), but 10 Hz petawatt operation is not demonstrated anywhere — TRL 2-3
-- Target (Pearl capsule): ~4 mm, D-T fill, direct-drive geometry — ICF target fabrication is demonstrated at lab scale (NIF, LLE) but not at 10 Hz/~900k/day volume — TRL 2
-- Energy conversion (steam cycle): conventional technology once heat is available — TRL 9 in isolation
-- Tritium breeding: SRNL partnership confirmed, but no blanket design disclosed — TRL unknown
+- Compression DPSSL (Nd:glass): mature technology for single-shot operation; kJ-class rep-rated systems being developed via Amplitude partnership (1 shot/60 seconds demonstrated, 10 Hz required for power plant). Technology target is "by the 2030s" (Ditmire, LaserFocusWorld).
+- CPA petawatt ignitor: 140 J / >10 PW demonstrated at Texas Petawatt; 2 kJ demonstrated at ELI Beamlines. Scaling to 150 kJ at rep rates is undemonstrated.
+- Target production: Pearl capsule in development at Darmstadt lab. General Atomics target factory cost studies (cited in Meier 2006) provide manufacturing cost scaling reference for direct-drive targets, not proton-FI geometry.
+- BOP (steam cycle): TRL 9, mature.
+- Tritium breeding/extraction: SRNL collaboration active; general Li-blanket tritium breeding is well-understood at laboratory scale; Focused Energy-specific blanket configuration unvalidated.
+- Proton fast ignition physics: Roth et al. 2001 established the concept; Focused Energy's CSU experiments completed (Milestone 2) but at demonstration scale far below ignition-relevant energy.
 
 **Missing**:
-- TRL assessment for chamber/first wall (nothing disclosed)
-- TRL for target injection/tracking system at 10 Hz (no public data)
-- TRL for tritium extraction from whatever blanket type is chosen
-- Any demonstrated fast ignition yield at relevant scale (CSU experiment details are sparse in available sources)
+- Formal TRL assessment for any Focused Energy subsystem — not published.
+- Rep-rated petawatt laser at 10 Hz with 150 kJ: not demonstrated anywhere; current best is ~1 shot/minute at kJ class.
+- Target mass production at 10/second rate: not demonstrated (NIF does ~400 shots/year; Focused Energy needs ~900,000/day).
+- Target injection and tracking at 10 Hz and the precision required: preliminary scoping studies only (Betti review notes linear induction accelerators at ~50 m/s and gas guns at ~400 m/s under investigation).
 
 **Gaps**:
-- 10 Hz petawatt laser — `truly-unknown` (at this scale, doesn't exist anywhere) — **blocking** for viability assessment; need to note as critical long-pole
-- High-throughput target factory (900k targets/day) — `truly-unknown` at production scale — **blocking** for LCOE (target cost is a dominant operating cost driver for IFE)
-- Chamber / first wall design — `proprietary` — **important**: FE hasn't disclosed their chamber concept; no HYLIFE analogue applies here unlike Xcimer
-- Target injection & tracking at 10 Hz — `not-yet-sourced` — **important**: academic IFE systems studies (e.g., LIFE plant study from LLNL) may have estimates
+- Proton FI ignition coupling TRL — `truly-unknown` at power-plant-relevant scale — **blocking**
+- Rep-rated petawatt laser TRL — `not-yet-sourced` / `derivable` from laser community publications — **important**
+- Target mass production TRL and cost-reduction pathway — `proprietary` + `not-yet-sourced` — **important**
+- Target injection/tracking TRL at 10 Hz — `not-yet-sourced` — **important**
 
 ---
 
 ### 4. Key Materials and Supply Chain Considerations
+
 **Coverage**: Poor
 
 **Available**:
-- D-T fuel origin stated (seawater deuterium + lithium for tritium breeding) — supply chain generally understood
-- Lithium blanket confirmed (with SRNL collaboration) — Li-6 enrichment requirements derivable but blanket type unknown
-- DPSSL uses Nd:glass gain media — commercially available, scaling is a manufacturing challenge at high rep rate
-- Amplitude as laser supply partner established
+- D fuel: seawater deuterium, no supply constraint.
+- T fuel: bred from Li; SRNL collaboration on extraction systems; tritium inventory and breeding ratio acknowledged as challenges.
+- Nd:glass gain medium: established supply chain for single-shot systems; 10 Hz thermal management requires active cooling (noted by Ditmire).
+- Laser diodes: identified as dominant capital cost driver for DPSSL power plants; Betti cites ~$0.01/W as required price point (current market ~$0.1–0.5/W, requiring ~10–50× cost reduction). Amplitude partnership represents supply chain development.
+- Target capsule: Pearl capsule development at Darmstadt; mass production at ~900,000/day is a stated engineering challenge.
 
 **Missing**:
-- Specific blanket material (FLiBe, LiPb, liquid Li) — determines Li-6 enrichment demand, tritium extraction complexity, pumping requirements
-- Cone-in-shell target materials (if applicable) — gold cones, complex nano-fabrication likely
-- First wall material (no chamber design disclosed)
-- Diode pump module supply chain at scale needed for 10 Hz DPSSL
+- Pearl capsule material composition (ablator material, DT ice layer thickness): proprietary.
+- First-wall material specification: Meier 2006 HAPL reference uses W-armor-coated ferritic steel for dry-wall chambers, which may be an applicable analog, but Focused Energy-specific design is undisclosed.
+- Blanket chemistry: specifically whether liquid Li, FLiBe, PbLi, or other form is used — proprietary per dossier.
+- Final optics supply chain: gratings, turning mirrors, and final optical components must withstand neutron flux and target debris at 10 Hz for ~30-year plant lifetime. No Focused Energy-specific data.
+- Optical component lifetime under neutron bombardment: a fundamental materials challenge noted in IFE literature but not addressed in Focused Energy-specific sources.
 
 **Gaps**:
-- Blanket material specification — `proprietary` — **important**: different blankets have very different material supply chains and costs
-- Pearl capsule + cone (if fast ignition) fabrication at 900k/day — `truly-unknown` at that volume — **blocking**: this is one of the hardest unsolved problems in IFE economics; no factory exists; estimated costs in academic literature range from $0.10–$1.00+/target
-- High-rep-rate petawatt laser diode supply chain — `not-yet-sourced` — **important**: terawatt-class diode pump arrays at 10 Hz are a significant manufacturing challenge with no current production base
+- Blanket chemistry — `proprietary` — **important**
+- First-wall material and design — `not-yet-sourced` (HAPL analog available) — **important**
+- Final optics survivability / supply chain — `not-yet-sourced` — **important**
+- Laser diode cost reduction pathway and supply chain scalability — `not-yet-sourced` — **important**
+- Target capsule materials and mass production supply chain — `proprietary` — **important**
 
 ---
 
 ### 5. LCOE Parameter Extraction
-**Coverage**: Poor
 
 **Available Parameters**:
+
 | Parameter | Value/Range | Source | Confidence |
-|-----------|-------------|--------|------------|
-| Target gain | >50 (commercial target: 50–100) | Callahan interview | m |
-| Rep rate | ~10 Hz (~900k shots/day) | Callahan interview | h |
-| DPSSL wall-plug efficiency | ~10% | FE technology page, Callahan interview | m |
-| Energy conversion cycle | Conventional steam | Callahan interview | h |
-| Tritium source | Li blanket + SRNL | Callahan interview | m |
-| Target size | ~4 mm Pearl capsule | FE technology page | h |
-| Timeline | LightHouse pilot end of 2030s | Callahan interview | m |
-| Laser partner cost signal | $40M Amplitude agreement (development, not production) | FE press release | l |
-| Lab basis | OMEGA, CSU proton FI milestone | FE technology page | h |
+|---|---|---|---|
+| Rep rate | ~10 Hz | Callahan interview | h |
+| Energy capture mode | Conventional steam cycle | Callahan interview | h |
+| Laser wall-plug efficiency (target) | ~10% (DPSSL) | Callahan + Betti | m |
+| Brayton cycle efficiency (HAPL reference) | 48% | Meier 2006 | l (analog, not FE-specific) |
+| Target gain requirement (min) | >50–100 (general IFE); FI theoretically 3–4× CI | Callahan + Meier 2006 | m |
+| FI plant COE reference (HAPL model) | ~5.9–6.1 ¢/kWeh at 10 Hz, ~0.9 MJ driver energy | Meier 2006 | l (2006, HAPL params) |
+| Laser capital cost reference | $400/J (2005 dollars, DPSSL) | Meier 2006 | l (dated) |
+| Target factory capital cost (GA study) | $136M for 350 MJ targets at 6 Hz (~1 GWe) | Meier 2006 (citing GA) | l (different yield, Hz, dated) |
+| Target cost threshold (cost-competitive) | ~$10/target | Hawker | m (generic model bound) |
+| Plant cost analogy (BOP) | $1,000–6,000/kWe | Hawker | l (wide range) |
+| O&M cost range (generic IFE) | $10–100/kWe-yr | Hawker | l (wide range) |
+| Auxiliary recirculating power | ~4% of gross electric (HAPL reference) | Meier 2006 | l (analog) |
+| Capacity factor (HAPL assumption) | 85% | Meier 2006 | l (assumption) |
+| Indirect capital cost multiplier | 1.936× direct capital cost | Meier 2006 | m (standard CAS convention) |
+| Fixed charge rate | 9.66% | Meier 2006 | m (standard; choice-dependent) |
+| Total investment raised (2024) | >$175M | PRNewswire | h |
+| Facility cost (ignition, rough estimate) | ~$3 billion | LaserFocusWorld / Ditmire | l (rough; ignition facility, not power plant) |
+| Driver energy optimum (FI, Meier model) | 0.6–0.9 MJ (at 10–21 Hz) | Meier 2006 | l (2006 parameters) |
+| Plant size reference | 750–1,250 MWe range | Meier 2006 | l (parametric range, not FE-specific) |
 
 **Missing Parameters**:
+
 | Parameter | Gap Type | Criticality | Notes |
-|-----------|----------|-------------|-------|
-| Compression laser energy per shot (MJ) | proprietary / not-yet-sourced | Blocking | Required to compute yield per shot; may be in 2023 paper |
-| Fusion yield per shot (MJ) | derivable | Blocking | = gain × laser energy; can estimate once energy known |
-| Plant electrical output (MWe) | derivable | Blocking | Needs yield, rep rate, steam efficiency, recirculating power |
-| Laser capital cost ($/J or $/W) | not-yet-sourced | Blocking | Some IFE system study analogues exist (LIFE, HAPL program) |
-| Target fabrication cost ($/target) | not-yet-sourced | Blocking | Academic estimates range widely; no FE-specific data |
-| Target injection/tracking system cost | truly-unknown | Blocking | No industrial analog at 900k/day |
-| Chamber / first wall capital cost | proprietary | Important | No FE chamber design disclosed |
-| Blanket/tritium system capital cost | proprietary | Important | No FE blanket design |
-| O&M cost (total $/yr) | truly-unknown | Important | No plant study; laser optics replacement a known cost driver |
-| Capacity factor / availability | derivable | Important | Rep rate gives theoretical max; actual limited by laser maintenance |
-| Net plant efficiency (%) | derivable | Important | Steam ~32–35% × (1 − recirculating fraction) |
-| First wall / optic replacement schedule | truly-unknown | Important | Neutron damage + laser optic degradation, no FE data |
-| Petawatt laser capital cost | not-yet-sourced | Important | OMEGA EP / Amplitude Sequoia pricing analogues may exist |
+|---|---|---|---|
+| Target yield per shot (MJ fusion per shot) | `proprietary` | Blocking | Central driver of LCOE; "lower yield per shot" stated but no value. Determines chamber design, target factory, and rep-rate economics |
+| Target gain at power plant conditions | `proprietary` | Blocking | FI gain ×3–4 over CI is generic; Focused Energy-specific gain curve not public |
+| Gross/net electrical output | `proprietary` + `not-yet-sourced` | Blocking | "Gigawatt-scale" cited without specifics; no plant study exists |
+| Net plant efficiency (steam + recirculating) | `derivable` (analogs available) | Blocking | Can bound using Meier 2006 assumptions; Focused Energy-specific unknown |
+| Capital cost breakdown by CAS subsystem | `not-yet-sourced` | Blocking | Meier 2006 provides structure for FI laser IFE; needs Focused Energy-specific driver/chamber adaptation |
+| DPSSL cost $/J at 10 Hz (current era) | `not-yet-sourced` | Blocking | Meier 2006's $400/J is ~20 years old; laser diode cost has dropped but DPSSL system cost curve at 10 Hz for power plant not re-established publicly |
+| Target cost at mass production scale | `proprietary` + `derivable` | Blocking | Target cost is the #3 LCOE driver (Hawker); mass production cost for proton-FI target geometry completely uncharacterized publicly |
+| Blanket TBR and tritium self-sufficiency margin | `proprietary` | Important | Affects startup tritium inventory and plant economics |
+| Blanket capital cost | `not-yet-sourced` | Important | Meier 2006 uses liquid Li coolant/breeder; Focused Energy chemistry unknown |
+| First-wall replacement schedule and cost | `not-yet-sourced` | Important | Neutron damage to dry wall is a key O&M cost driver |
+| Chamber cost scaling | `derivable` (HAPL analog) | Important | Meier 2006 dry-wall chamber cost scaling with yield is best available analog |
+| O&M cost (Focused Energy-specific) | `derivable` (analogs) | Important | IFE ranges from Hawker ($10–100/kWe-yr) and Meier 2006 can bound this |
+| Capacity factor (first plant) | `derivable` | Important | 85% (Meier 2006) is likely optimistic for early plant; 70–80% more realistic |
+| Decommissioning cost | `derivable` | Nice-to-have | Standard fusion decommissioning conventions applicable |
 
 ---
 
 ## Source Recommendations
 
-1. **Focused Energy J. Fusion Energy 2023** (Springer, DOI: 10.1007/s10894-023-00363-x) — the primary peer-reviewed concept disclosure. Likely contains chamber architecture, gain physics, and possibly energy-per-shot details. Access abstract first to confirm content, then seek full text. `not-yet-sourced — access required before analysis`
+1. **Focused Energy J. Fusion Energy 2023** (Springer, paywalled): Most important single gap-filling document for blanket chemistry, chamber specifics, and plant-level parameters. Search: `site:springer.com "Focused Energy" "inertial fusion"` or via DOI lookup. Alternatively, contact authors directly. — `not-yet-sourced`; **exists, confirm access via interlibrary loan**
+
+2. **LLNL Generalized Economics Model (GEM) for IFE** (referenced in `iter-03/sources/llnl-53961-…`): GEM is publicly downloadable at `lift.llnl.gov/resources/gem`. Designed for DPSSL + dry-wall IFE with liquid Li breeder — directly applicable to the Focused Energy architecture as a parametric economic tool. This is a free tool that could provide the updated (post-2006) IFE cost model. — **confirmed to exist; download and apply**
 
-2. **FE ALP Conference Roadmap PDF** (`asso-alp.fr/wp-content/uploads/2023/07/2.7-Roadmap-of-Focused-Energy-Vaisseau.pdf`) — company roadmap with subsystem milestones. Listed in dossier as key source but not extracted. `not-yet-sourced — fetch recommended`
+3. **LLNL Integrated Process Model (IPM) for IFE** (mentioned in same source): a more full-featured version of GEM available for purchase via software licensing. May provide Focused Energy-architecture-level detail for system cost by CAS account. — `unverified — confirm scope before purchasing`
 
-3. **HAPL (High Average Power Laser) Program reports** — DARPA/DOE program from 2000s that developed laser IFE systems engineering including target fabrication cost models, chamber design, and laser cost targets. Search OSTI for "HAPL IFE systems study" or "high average power laser fusion power plant." `not-yet-sourced — search OSTI; existence likely, specific papers unverified`
+4. **Meier & Hogan 2006, "Power Plant and Chamber Considerations for Fast Ignition," Fus. Sci. Technol. 49:532**: Companion to Meier 2006 in corpus; explicitly addresses chamber design for FI power plants. Search OSTI for UCRL document number. — `not-yet-sourced`; **high value — directly FI-specific**
 
-4. **LIFE Plant Study (LLNL, 2010–2012)** — Laser Inertial Fusion Engine, the most detailed published IFE plant study with cost breakdowns by CAS. Uses NIF-heritage indirect drive but the laser system, chamber, and balance-of-plant cost structures are directly analogous for cross-concept estimation. Search OSTI or Lawrence Livermore publications. `not-yet-sourced — high confidence this exists, specific OSTI accession unverified`
+5. **DOE Milestone-Based Fusion Development Program technical reports for Focused Energy**: DOE Milestone-program requires public milestone reports. Focused Energy has completed at least 2 milestones. Search at `fusionenergy.energy.gov` or DOE OSTI for Focused Energy milestone reports. — `not-yet-sourced`; **may contain target design and physics validation data**
 
-5. **Academic fast ignition physics papers (Tabak, Roth, Temporal groups)** — for proton fast ignition coupling efficiency and ignition energy threshold at relevant compressed core conditions. Search: "proton fast ignition coupling efficiency D-T" on Google Scholar or OSTI. `not-yet-sourced — general search strategy, specific papers unverified`
+6. **Roth et al. 2001 (Phys. Rev. Lett. 86:436)** "Fast ignition by intense laser-accelerated proton beam" and **Tabak et al. 2005 (Phys. Plasmas 12:057305)** "Review of progress in Fast Ignition": foundational fast ignition physics references cited in the corpus but not ingested. Needed for physics-basis and coupling efficiency context. — `not-yet-sourced`; **confirmed to exist**
 
-6. **IFE target factory cost studies** — GAO/IAEA/DOE reports on ICF target fabrication cost-per-target at production volume. The National Academy of Sciences 2021 IFE report (DOE-commissioned) likely addresses target fabrication economics. `not-yet-sourced — NAS 2021 report confirmed to exist (cited in other fusion analyses); IFE-specific cost appendix may be available`
+7. **Xcimer Energy commercialization whitepaper** (`knowledge/sources/commercialization_of_laser_fusion_energy/`): already registered in the fleet-wide source index. Provides the most current (2026) laser cost breakdown by component ($<100/J for KrF, vs. $700–1000/J for DPSSL heritage systems). Use as an upper-bound analog for DPSSL cost — noting KrF is a different architecture — to constrain the laser capital cost uncertainty. — **read this fleet-wide source**
+
+8. **ARIES Cost Account Documentation** (`knowledge/sources/aries_cost_account_documentation/`): already registered. Use to populate the CAS structure for a Focused Energy plant study analog (accounts 20–27 direct, 90–98 indirect). Essential for the capital cost breakdown section. — **read this fleet-wide source for CAS framework application**
 
 ---
 
 ## Summary
 
-**Proceed with analysis, but flag heavy assumption load.** The Focused Energy fast ignition concept has enough public data to produce a coherent qualitative write-up and a parameterized LCOE model skeleton, but the model will be driven primarily by analogues and assumptions rather than company-disclosed values. The most critical missing data — compression laser energy per shot, target fabrication cost, and chamber design — are either proprietary or buried in sources not yet extracted.
+The available corpus supports a D1+ analysis at the level of **a well-bounded parametric estimate with high uncertainty on all concept-specific inputs.** The strongest assets are: (1) Meier 2006, which provides the only published FI-specific economic systems model and can be adapted as an analog; (2) the Hawker 14-parameter model, which establishes what drives IFE LCOE without concept-specific inputs; and (3) the PRNewswire/Callahan/LaserFocusWorld sources, which establish the architecture and development trajectory.
+
+The principal gap is that **Focused Energy has no public plant study**, and its central physics claim — proton fast ignition coupling efficiency at ignition-relevant scale — is **pre-experimental validation**. This makes the concept simultaneously interesting (the FI gain advantage, if achieved, meaningfully reduces COE per Meier 2006) and fundamentally uncertain (the gain advantage depends on physics not yet demonstrated).
 
-**Before writing the analysis**, the following should be retrieved first:
-1. The FE J. Fusion Energy 2023 paper (full text or detailed abstract) — highest priority
-2. The ALP roadmap PDF — quick fetch, high return
-3. At least one IFE systems cost study (LIFE or HAPL) for capital cost analogues
+**Recommended path before analysis**: Download the LLNL GEM tool (confirmed public) and attempt to obtain the Focused Energy J. Fusion Energy 2023 paper. If the J. Fusion Energy paper cannot be obtained, proceed with Meier 2006 as the primary analog, explicitly flagging that all quantitative LCOE outputs carry ±50% uncertainty due to missing Focused Energy-specific parameters.
 
-Without these, the quantitative model will require so many undisclosed inputs to be assumed that the back-solve to $0.01/kWh will be largely an exercise in assumption propagation rather than concept-specific analysis. The qualitative sections can be written now with the data in hand.
+---
 
 ## Structured summary (machine-readable)
 
 ```yaml
 overall_rating: "Significant Gaps"
 blocking_count: 6
-important_count: 7
-counting_method: "section_5_missing_parameters"
+important_count: 8
+counting_method: "all_sections_deduplicated — blocking: (1) proton FI coupling physics unvalidated, (2) target gain/yield specifics proprietary, (3) gross/net electrical output unknown, (4) net plant efficiency derivable only from aged analogs, (5) capital cost by CAS subsystem (no FE plant study), (6) DPSSL cost $/J current era not-yet-sourced; important: blanket chemistry, first-wall design, rep-rated PW laser TRL, target mass production TRL, target injection/tracking TRL, blanket capital cost, first-wall O&M cost, DPSSL diode supply chain"
 section_coverage:
   availability_of_data:       "Partial"
   system_function:            "Partial"
   subsystem_maturity:         "Partial"
   materials_supply_chain:     "Poor"
-  lcoe_parameter_extraction:  "Poor"
-```
+  lcoe_parameter_extraction:  "Partial"
+```
\ No newline at end of file
```

## Acceptance notes (fill during Phase 3)

- Deviation class (1-6 per plan.md): 
- Justified by fleet source? 
- Notes: 
