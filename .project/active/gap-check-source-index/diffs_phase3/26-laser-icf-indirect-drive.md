# Phase 3 diff: 26-laser-icf-indirect-drive

**Generated:** 2026-05-22T15:30:55-07:00

## Counts (Phase 2 -> Phase 3 strict-read regen)

| field | phase2 | phase3 | Δ |
|-------|--------|--------|---|
| blocking_count   | 2 | 2 | 0 |
| important_count  | 7 | 7 | - |
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
# Gap Assessment: Laser ICF - Indirect Drive (D-T)
```

## Blocking-tier lines (new)

```
107:| Xcimer KrF laser cost breakdown by component at nth-of-a-kind | not-yet-sourced | blocking | <$100/J is a company claim without published component-level cost analysis; required to build credible capital cost model for Xcimer track |
108:| Driver rep-rate O&M cost (laser component replacement at commercial rep rate) | not-yet-sourced | blocking | NIF $40M/yr at <1 shot/day provides extreme upper bound; no rep-rated lifetime data for KrF or DPSSL amplifiers |
```

## Full unified diff (truncated to 400 lines)

```diff
--- /tmp/gap_phase2_state/26-laser-icf-indirect-drive.md	2026-05-22 12:59:21.082728984 -0700
+++ /home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/26-laser-icf-indirect-drive/gap_report.md	2026-05-22 15:30:55.004063425 -0700
@@ -1,176 +1,144 @@
-I now have sufficient information to write the comprehensive gap assessment.
-
----
-
 # Gap Assessment: Laser ICF - Indirect Drive (D-T)
 
 ## Overall Readiness
 **Rating**: Mostly Ready
-
-**Summary**: This concept benefits from the deepest physics validation base of any private fusion concept — 10 demonstrated ignition experiments at NIF, with peak gain of 4.13 (April 2025). Xcimer has also published a detailed commercialization whitepaper (Feb 2026) with explicit cost comparisons, and the SOMBRERO study (1992) provides a complete CAS-level economic analysis for a KrF laser-driven IFE plant. The main gaps are (1) no contemporary full-plant CAS-breakdown study exists; all numbers must be synthesized from multiple partial sources; and (2) Inertia's Thunderwall DPSSL plant details are almost entirely unpublished, limiting comparative analysis to Xcimer's approach.
+**Summary**: The Xcimer Energy track has sufficient published material (commercialization whitepaper, Physics of Plasmas HDD paper, HYLIFE-III nuclear analysis, and company documentation) to support a first-pass LCOE model with wide uncertainty ranges. The Inertia Enterprises track lacks any published plant design document, but the DPSSL architecture can be proxied through SOMBRERO/OSIRIS analogs. Two foundational physics gaps — commercial-scale target gain not yet demonstrated above NIF G~4, and no rep-rated private-sector laser operation — limit confidence but do not prevent parameterization of a bounded LCOE model.
 
 ---
 
 ## Section Coverage
 
 ### 1. Availability of Data
-**Coverage**: Good (Xcimer) / Poor (Inertia)
+**Coverage**: Good
+
+**Available**: The NIF experimental record (10 ignitions Dec 2022–Oct 2025, peak yield 8.6 MJ from 2.08 MJ input, gain 4.13 — from `iter-02/sources/nif-ignition-updates-2025.md`) provides the most comprehensive demonstrated physics database for any fusion concept. Xcimer's 2026 commercialization whitepaper (`knowledge/sources/commercialization_of_laser_fusion_energy/output.md`) is exceptionally transparent: it covers driver cost arguments (<$100/J KrF vs. $700–1000/J DPSSL), chamber design rationale (HYLIFE-III liquid wall), and deployment roadmap. The Xcimer HDD Physics of Plasmas paper (`iter-02/sources/xcimer-hybrid-direct-drive-evolution.md`) provides target physics design values (G=65 at 4 MJ, 97% laser absorption). The SOMBRERO/OSIRIS IFE design study (`iter-03/sources/osti-servlets-purl-833813.md`) provides the only publicly available full IFE power plant economics at conceptual design level for a KrF laser-driven plant (SOMBRERO COE 6.67 ¢/kWh in 1992 dollars, 1000 MWe, net efficiency 35%). Hawker's 14-parameter IFE LCOE model (`knowledge/sources/a_simplified_economic_model_for_inertial_fusion/output.md`) provides the best available framework for parameterizing IFE cost, with Monte Carlo exploration showing competitive LCOE ($25–100/MWh) under optimistic assumptions. Inertia's $450M Series A press release and website describe Thunderwall architecture (10 kJ × 10 Hz × 10% efficiency), tritium approach (liquid Li pipes), and founding team credentials.
 
-**Available**:
-- NIF ignition physics: extensively documented through Oct 2025 with 10 experiments (`iter-01/sources/nif-ignition-achievements.md`, `iter-02/sources/nif-ignition-updates-2025.md`). Peak yield 8.6 MJ, gain 4.13 (Apr 2025).
-- Xcimer physics: HDD target paper in *Phys. Plasmas* 31(11) (2024) — full radiation-hydrodynamic design with gain = 65 at 4 MJ input (`iter-02/sources/xcimer-hybrid-direct-drive-evolution.md`).
-- Xcimer commercialization whitepaper (Feb 2026): covers laser cost comparison (DPSSL at $700–1,000/J floor vs. KrF target <$100/J), chamber architecture (HYLIFE), and deployment roadmap (`knowledge/sources/commercialization_of_laser_fusion_energy/`).
-- Xcimer hardware milestone: LPK platform completed June 2025, first private-sector e-beam excimer laser in 20+ years (`iter-02/sources/xcimer-laser-milestones-2025.md`).
-- SOMBRERO plant study (1992): full 1000 MWe KrF laser IFE plant, including CAS-level economic assessment, driver design (3.4 MJ, 6.7 Hz, 7.5% efficiency), blanket, and target systems (`iter-03/sources/osti-servlets-purl-833813.md`).
-- HYLIFE-II tritium management (1992): tritium inventory (~190 g), FLiBe vacuum disengager design, total system cost $92M (`iter-03/sources/osti-biblio-10179076.md`).
-- Target fabrication: Goodin 2007 paper with cost estimates (~$0.17/target nth-of-kind for 500,000/day) (`iter-03/sources/fire-fpa07-goodin-icf-fuel.md`).
-- Technology-agnostic LCOE model: Hawker (2020) 14-parameter model, Monte Carlo parameter space, LCOE as low as $25/MWh under optimistic assumptions (`iter-03/sources/pmc-articles-pmc7658748.md`; also at `knowledge/sources/a_simplified_economic_model_for_inertial_fusion/`).
-- Inertia: $450M Series A announcement (Feb 2026) with high-level plant description — 10 kJ × 1000–4000 beamlines, 10 Hz, <$1/target target (`iter-02/sources/inertia-enterprises-2026-update.md`).
-
-**Missing**:
-- Inertia has no published plant design study, blanket engineering details, or detailed cost data.
-- The LIFE concept (the closest NIF-derived indirect-drive IFE plant study, LLNL 2011) was captured only by reference in the Xcimer whitepaper, not ingested as a primary source.
-- No post-2010 full plant study for pure indirect-drive laser IFE exists in the source set.
+**Missing**: Inertia has no published power plant design study. HYLIFE-III FuE&D paper is cited but not extracted. Xcimer's Phoenix laser hardware characterization data (completion June 2025) is described at milestone level only — no rep-rate performance data published. No published Xcimer ASPEN IFE Workshop 2022 document in the repo (cited in dossier but not extracted).
 
 **Gaps**:
-- No published Inertia plant design — `proprietary` — **important**: limits comparative analysis to Xcimer's approach
-- LIFE (2011) plant study not ingested — `not-yet-sourced` — **important**: only direct NIF-heritage IFE plant study ever published
+- Inertia power plant design document — proprietary — important
+- Xcimer Phoenix laser performance characterization (beyond milestone press release) — not-yet-sourced — important
+- HYLIFE-III Fusion Engineering and Design 2024 paper (FLiBe TBR, detailed blanket nuclear analysis) — not-yet-sourced — nice-to-have (TBR>1.2 is already confirmed at dossier level)
 
 ---
 
 ### 2. Challenges in Capturing System Function
-**Coverage**: Good (physics and challenges well characterized)
+**Coverage**: Partial
+
+**Available**: The fundamental system function challenge is clearly documented across multiple sources. The Xcimer commercialization whitepaper explicitly identifies three core engineering challenges: (1) coupling efficiency (NIF indirect drive wastes ~88% of laser energy in hohlraum; HDD targets 90%+ coupling), (2) chamber survivability at sustained rep rate (liquid wall required; solid first wall replacement becomes prohibitive at >1 Hz), (3) driver cost (NIF optics: $40M/yr refurbishment at <<1 Hz shot rate; gas amplifiers offer improved lifetime). The gap between NIF wall-plug gain (~0.01) and required commercial gain (~10) is quantified in `knowledge/sources/commercialization_of_laser_fusion_energy/output.md`. Physics of Plasmas HDD paper provides radiation-hydrodynamic simulation data establishing the hybrid drive concept as a viable path to commercial gain. The OSIRIS/SOMBRERO study documents RAM (reliability, availability, maintainability) assessment — total system availability 75%, driver system availability 93% for SOMBRERO KrF design.
 
-**Available**:
-- The Xcimer whitepaper provides a detailed account of why NIF architecture is not commercially scalable (optics damage, laser efficiency, chamber wall replacement), and explicitly frames all three major system-function challenges: confinement performance, materials/chamber survivability, and cost (`knowledge/sources/commercialization_of_laser_fusion_energy/`).
-- The HDD paper quantifies the energy budget chain from wall-plug to target gain: laser absorption 97%, hydrodynamic efficiency 8%, target gain 65 at 4 MJ input (`iter-02/sources/xcimer-hybrid-direct-drive-evolution.md`). The wall-plug gain requirement (~10) is explicitly derived.
-- NIF's energy flow is quantified in the Xcimer science page: 400 MJ from grid → 2 MJ laser → 250 kJ to capsule → 5 MJ fusion energy (0.5% wallplug NIF) (`iter-03/sources/xcimer-science.md`).
-- Chamber clearing time as a driver of rep-rate ceiling is addressed; the liquid wall requires <1 Hz to allow flow recovery.
-- Modeling challenges: radiation-hydrodynamic simulation fidelity, laser-plasma instabilities (LPI), cross-beam energy transfer (CBET) and how HDD geometry mitigates them — all covered in the HDD paper.
-
-**Missing**:
-- No detailed analysis of what target implosion performance must scale to for commercial operation (gain >100 requirement vs. demonstrated gain ~65 in simulation at 4 MJ).
-- Inertia's "10x efficiency vs NIF" claim (10% wallplug stated) is stated but not derived from published engineering analysis.
-- Chamber debris clearing dynamics (gas/plasma recovery between shots) are not quantified for Inertia's 10 Hz architecture.
+**Missing**: No integrated systems model has been published for the Xcimer or Inertia power plant architectures. The interaction between chamber clearing dynamics and rep-rate performance has been modeled for HYLIFE-II but not validated experimentally. Target injection tracking accuracy at full rep rate is undemonstrated (HAPL program achieved ~125 µm accuracy at ~5 m/s, compared to the required 20 µm; `iter-03/sources/fire-fpa07-goodin-icf-fuel.md`).
 
 **Gaps**:
-- Inertia chamber clearing dynamics at 10 Hz: unresolved — `not-yet-sourced` — **important**: determines whether 10 Hz rep-rate is feasible with a liquid wall or requires a dry wall
-- Target gain scaling from 65 (simulation) to commercial requirement (>100–150): basis established but not fully characterized — `derivable` — **nice-to-have**
+- Integrated driver-chamber-target system performance under rep-rated conditions — not-yet-sourced — blocking (no experimental data; SOMBRERO design study provides modeled estimate only)
+- Thermal hydraulics of HYLIFE-III chamber at 0.25–1 Hz rep rate — not-yet-sourced — important
+- Target injection accuracy at commercial rep rate and velocity — not-yet-sourced — important
 
 ---
 
 ### 3. Maturity of Key Subsystems and Components
-**Coverage**: Partial (Xcimer well-characterized, Inertia sparse)
+**Coverage**: Partial
+
+**Available**: Ignition physics (NIF indirect drive): TRL 6 — demonstrated repeatedly at lab scale (10 events, G up to 4.1). KrF excimer laser hardware (Xcimer Phoenix): TRL 4 — first private-sector e-beam pumped excimer laser completed June 2025, record 3 µs pulse length demonstrated (single-shot, not rep-rated). SOMBRERO KrF design study from 1992 documented "low" technical credibility for the driver with "high" development needs. CD foam target capsule (General Atomics): TRL 3-4 — fabrication process demonstrated at lab scale (HAPL program), mass production not demonstrated. Target injection at low rep rate: TRL 3-4 — HAPL demonstrated gas-gun injection at 150 m/s, tracking accuracy ~125 µm (goal: 20 µm). Steam turbine power conversion: TRL 9 — fully commercial. FLiBe liquid wall (HYLIFE-III concept): TRL 3-4 — nuclear analysis complete (TBR>1.2), no rep-rated chamber dynamics experiment. Hohlraum fabrication for HIF targets: TRL 3-4 per Goodin 2007 — LCVD process demonstrated for HIF hohlraums; laser ICF Inertia Hybrid-E hohlraum at similar maturity.
 
-**Available**:
-- **KrF excimer laser (Xcimer)**: LPK platform completed June 2025, record 3 µs pulse length achieved. Phoenix prototype on track for 2026. Vulcan (12 MJ) targeted 2030. TRL 3–4 for the laser subsystem (`iter-02/sources/xcimer-laser-milestones-2025.md`).
-- **DPSSL (Inertia Thunderwall)**: Described as pre-hardware as of Mar 2026. Semiconductor diode technology mature at small scale but 10 MJ/10 Hz DPSSL has no demonstrated hardware. TRL 1–2.
-- **Hohlraum/target physics**: NIF has demonstrated 10 ignitions with indirect drive, gain up to 4.13. TRL 6 for physics, TRL 2–3 for production-rate target manufacturing.
-- **Target fabrication**: All process steps identified (Goodin 2007), but mass production (500,000 targets/day) undemonstrated. TRL 2–3 (`iter-03/sources/fire-fpa07-goodin-icf-fuel.md`).
-- **FLiBe blanket (Xcimer/HYLIFE-III)**: Nuclear analysis published in *Fusion Engineering and Design* (2024), TBR > 1.2 confirmed. Structural engineering and vacuum disengager at conceptual stage. TRL 2–3.
-- **Tritium management**: HYLIFE-II conceptual design exists with engineering detail ($92M system cost, 2 TBq/s tritium bred). Experiment needed to validate vacuum disengager. TRL 2.
-- **Target injection / tracking**: Conceptual designs exist (SOMBRERO 1992, section 4.2–4.3); no rep-rate validated hardware.
-
-**Missing**:
-- Inertia's liquid lithium chamber design has no published engineering basis.
-- No publicly demonstrated rep-rate laser ICF target injection system.
-- Chamber wall survivability under sustained pulsed load: HYLIFE concept studies exist but no prototyped hardware.
+**Missing**: Rep-rate performance data for any subsystem at commercial conditions. Xcimer Vulcan (12 MJ) scheduled for 2030 — this is the first system that could demonstrate integrated operation. Inertia Thunderwall has no hardware demonstrated as of March 2026.
 
 **Gaps**:
-- Mass-production target fabrication at rep-rate (500,000/day for 10 Hz): no demonstrated capability — `truly-unknown` at production scale — **blocking** for capacity factor assumptions
-- Target injection and tracking at >0.25 Hz: undemonstrated — `truly-unknown` at power-plant rates — **important**
-- Inertia Thunderwall DPSSL at 10 kJ × 10 Hz × 1000+ beamlines: no hardware, no published roadmap beyond $450M Series A — `proprietary` — **important**
+- Rep-rated laser performance (thermal management, e-beam cathode lifetime) — not-yet-sourced — blocking for Xcimer O&M cost anchor
+- Mass production target fabrication at 500,000+ targets/day — not-yet-sourced — important
+- Cryogenic target injection at commercial accuracy (20 µm) and velocity — not-yet-sourced — important
+- DPSSL (Inertia Thunderwall) prototype TRL — proprietary/not-yet-sourced — important
+- First structural wall lifetime under neutron flux with liquid protection — not-yet-sourced — important
 
 ---
 
 ### 4. Key Materials and Supply Chain Considerations
 **Coverage**: Partial
 
-**Available**:
-- **Tritium**: Inertia explicitly notes startup tritium from U.S. government stockpiles; on-site inventory "few hundred grams"; lithium equivalent of ~15 EVs per plant (`iter-01/sources/inertia-enterprises-website-and-faq.md`, `dossier.md`). TBR > 1.2 for Xcimer/HYLIFE-III FLiBe blanket.
-- **FLiBe (Xcimer blanket)**: Li₂BeF₄ uses both beryllium (limited mining capacity) and enriched lithium. Li-6 enrichment supply chains are limited but exist (government enrichment programs). Xcimer explicitly says their approach uses "commercially available materials" due to liquid first wall protection (`iter-02/sources/xcimer-laser-milestones-2025.md`, commercialization whitepaper).
-- **Hohlraum materials**: NIF uses gold; HDD design may reduce or eliminate hohlraum mass per shot (lower-Z baffle materials mentioned in HDD paper). Gold is expensive but manageable at ICF target quantities.
-- **DPSSL laser diodes**: Xcimer whitepaper calculates a floor cost of $7–10B for 10 MJ DPSSL laser in diodes alone, with current supply chains requiring order-of-magnitude scale-up. This is a fundamental supply chain bottleneck for Inertia's architecture.
-- **KrF excimer gas medium**: Krypton (rare gas) and fluorine chemistry — industrial supply chains exist from semiconductor lithography, but not at fusion-laser scale.
-- **Carbon-carbon structural materials**: SOMBRERO used C/C first wall (1992); Xcimer uses liquid FLiBe protection of steel → avoids exotic materials for structure.
-
-**Missing**:
-- No dedicated supply chain analysis for KrF gas at fusion-plant scale (how many tons of Kr/F₂ per year for a 12 MJ system).
-- Li-6 enrichment demand and supply chain at multi-GW scale not analyzed.
-- Beryllium supply (FLiBe contains Be) not addressed.
-- Hohlraum material per shot at power plant rate (target → consumption rate of gold or substitute) not quantified.
+**Available**: Tritium: startup supply from US government stockpiles confirmed (dossier), total inventory ~300 g (Inertia, dossier; SOMBRERO target factory 300 g, `osti-servlets-purl-833813.md`). Lithium: natural Li sufficient for FLiBe/Li blankets — no enrichment requirement for thick-wall designs (Xcimer commercialization whitepaper notes commercial-steel compatibility). Fluorine for KrF: industrial supply available, not a constraint. CD foam ablator material: General Atomics demonstrated capability (Physics of Plasmas HDD paper, citation). DT-wetted foam: reduces tritium inventory vs. DT ice layers, simplifies target layering (HDD paper, `iter-02/sources/xcimer-hybrid-direct-drive-evolution.md`). Beryllium (in FLiBe): hazardous material with established industrial supply; handling infrastructure exists from NIF target program. Hohlraum materials (Au for NIF, Pb-Hf for HIF): Au is available at laboratory scale; scale-up to 500,000 targets/day represents a manufacturing bottleneck.
+
+**Missing**: Inertia's liquid lithium chamber design has no published inventory analysis (dossier notes ~15 EV equivalent but no mass flow analysis). No published supply chain analysis for the scale of laser glass, nonlinear optical media, or e-beam cathode materials needed for a commercial Xcimer plant. Hohlraum manufacturing cost and supply chain for mass production (500,000/day at 10 Hz = ~$0.17/target from Goodin 2007 analysis, updated cost needed).
 
 **Gaps**:
-- KrF/excimer gas supply chain at plant scale: not analyzed — `not-yet-sourced` — **nice-to-have**
-- Li-6 enrichment supply chain for multi-GW FLiBe deployment: not analyzed — `not-yet-sourced` — **important** for long-term scale-up analysis
-- Beryllium supply constraints for FLiBe at GW scale: not analyzed — `not-yet-sourced` — **nice-to-have**
-- Laser diode supply chain (Inertia DPSSL): cost floor quantified in whitepaper, but supply chain development pathway not published — `proprietary` — **important** for Inertia LCOE
+- Tritium breed-up time and doubling time for each specific blanket design — derivable — important
+- E-beam cathode lifetime and replacement supply chain for KrF amplifiers — not-yet-sourced — important
+- Hohlraum gold/Au supply chain at mass-production scale — not-yet-sourced — important
+- Liquid lithium inventory and pump system engineering for Inertia design — proprietary/not-yet-sourced — nice-to-have
 
 ---
 
 ### 5. LCOE Parameter Extraction
-**Coverage**: Partial
-
 **Available Parameters**:
 
 | Parameter | Value/Range | Source | Confidence |
-|---|---|---|---|
-| Target gain (HDD simulation) | 65 (4 MJ), >200 (8 MJ projected) | Xcimer HDD Phys. Plasmas 2024 | m |
-| Target gain (NIF demonstrated) | 1.7–4.1 (2022–2025) | NIF ignition updates | h |
-| Laser wall-plug efficiency (NIF) | ~0.5% (flashlamp) | Xcimer science page | h |
-| Laser wall-plug efficiency (DPSSL, expected) | ~15% | Xcimer whitepaper | m |
-| Laser wall-plug efficiency (KrF excimer, target) | ≥12% | HDD paper, whitepaper | m |
-| Required wall-plug gain for commercial operation | ~10 | Xcimer whitepaper | m |
-| Plant electric output (Xcimer target) | GW-class (unspecified) | Dossier | l |
-| Plant electric output (Inertia) | ~1.5 GW | Inertia ENR interview | l |
-| Rep rate (Xcimer) | 0.25–1 Hz | Xcimer/ASPEN | h |
-| Rep rate (Inertia) | ~10 Hz | Inertia website | h |
-| Thermal conversion (Xcimer, website) | Steam turbine | Xcimer science page | m |
-| Thermal conversion (HYLIFE-III) | Helium Brayton, 45% efficiency | ASPEN 2022 presentation | m |
-| SOMBRERO net plant efficiency | 35% (including laser power) | SOMBRERO 1992 OSTI | m |
-| SOMBRERO laser power consumption | 304 MWe of 1000 MWe gross | SOMBRERO 1992 OSTI | m |
-| SOMBRERO availability assessment | Detailed (Chapter 6) | SOMBRERO 1992 OSTI | m |
-| DPSSL laser capital cost floor | $700–$1,000/J (10 MJ → $7–10B) | Xcimer whitepaper 2026 | h |
-| KrF excimer laser cost target | <$100/J | Xcimer whitepaper 2026 | l (projected) |
-| NIF facility cost | ~$3.5–7B (2 MJ) | Xcimer whitepaper | h |
-| Tritium management system (HYLIFE-II) | $92M system cost | OSTI 10179076 | m |
-| Target cost (Inertia aspiration) | <$1/target | Inertia website | l (unvalidated) |
-| Target cost (Goodin 2007, nth-of-kind) | ~$0.17/target | Goodin 2007 paper | m (dated) |
-| TBR (Xcimer/HYLIFE-III FLiBe) | >1.2 | HYLIFE-III FusEngDes 2024 | h |
-| LCOE range (Hawker model, optimistic) | $25–100/MWh | Hawker 2020 PMC | m |
-| IFE driver cost sensitivity | Dominant cost lever | Hawker 2020 model | h |
+|-----------|-------------|--------|------------|
+| Target gain (NIF demonstrated) | G = 1.7–4.1 at 1.9–2.2 MJ | nif-ignition-updates-2025.md | high |
+| Target gain (HDD simulation, 4 MJ) | G = 65 | xcimer-hybrid-direct-drive-evolution.md | medium |
+| Target gain (commercial scale, 10–12 MJ) | G = 200+ (projected) | commercialization_of_laser_fusion_energy | low |
+| Driver efficiency (KrF excimer, Xcimer) | ≥12% (design target) | xcimer-hybrid-direct-drive-evolution.md; SOMBRERO 7.5% actual | low-medium |
+| Driver efficiency (DPSSL, Inertia) | ~10% wallplug (claim) | inertia-enterprises-2026-update.md | low |
+| Driver energy on target | 10–12 MJ (commercial design) | dossier; commercialization_of_laser_fusion_energy | medium |
+| Rep rate (Xcimer) | 0.25–1 Hz | dossier | medium |
+| Rep rate (Inertia) | ~10 Hz | dossier | medium |
+| Thermal cycle efficiency | 35–47% | osti-servlets-purl-833813.md (SOMBRERO 35%, OSIRIS 45%) | medium |
+| BOP cost analog | ~$3,600/kWe (2020$) | a_simplified_economic_model_for_inertial_fusion (Hawker 2020, HYLIFE basis) | medium |
+| Driver cost (DPSSL) | $700–1,000/J | commercialization_of_laser_fusion_energy | medium |
+| Driver cost (KrF excimer, Xcimer claim) | <$100/J | commercialization_of_laser_fusion_energy | low |
+| Driver cost (SOMBRERO KrF, 1992 design) | ~$120/J (HIF beam basis) | osti-servlets-purl-833813.md | medium |
+| Target cost (nth-of-a-kind, laser IFE) | ~$0.17/target | fire-fpa07-goodin-icf-fuel.md (2007$) | low-medium |
+| Target cost (HIF baseline) | ~$0.41/target | fire-fpa07-goodin-icf-fuel.md (2007$) | medium |
+| Plant capacity factor / availability | ~75% | osti-servlets-purl-833813.md (SOMBRERO/OSIRIS RAM study) | medium |
+| Net plant electrical output | ~1,000 MWe | osti-servlets-purl-833813.md; dossier | medium |
+| Fusion power | ~2,000–2,700 MWt | osti-servlets-purl-833813.md | medium |
+| COE analog (SOMBRERO KrF, 1992$) | 6.67 ¢/kWh | osti-servlets-purl-833813.md | medium |
+| COE analog (OSIRIS HIF, 1992$) | 5.61 ¢/kWh | osti-servlets-purl-833813.md | medium |
+| Competitive LCOE range (Hawker model) | $25–100/MWh (optimistic) | a_simplified_economic_model_for_inertial_fusion | medium |
+| NIF facility cost (2 MJ, 192 beamlines) | ~$3.5B | xcimer-science.md | high |
+| NIF optics refurbishment (O&M analog) | >$40M/yr | xcimer-science.md | high |
+| Tritium inventory (target factory) | ~300 g | osti-servlets-purl-833813.md; dossier | medium |
+| Target injection velocity | 150 m/s | osti-servlets-purl-833813.md (SOMBRERO gas gun) | medium |
+| Energy multiplication (blanket) | 1.08–1.26 | osti-servlets-purl-833813.md | medium |
+| Tritium breeding ratio | >1.2 (FLiBe) | dossier (HYLIFE-III) | medium |
 
 **Missing Parameters**:
 
 | Parameter | Gap Type | Criticality | Notes |
-|---|---|---|---|
-| Capital cost breakdown by CAS category (contemporary) | not-yet-sourced | blocking | SOMBRERO (1992) has this but for different technology; LIFE (2011) likely has it but not ingested |
-| Laser capital cost (Inertia Thunderwall, 10 MJ DPSSL) | proprietary | blocking | Company has not published engineering cost analysis; only aspiration-level claims |
-| Chamber capital cost (Xcimer HYLIFE-III, detailed) | not-yet-sourced | important | HYLIFE-III FusEngDes paper covers nuclear analysis, not full capital cost breakdown |
-| O&M cost estimates (any contemporary IFE design) | not-yet-sourced | important | SOMBRERO Chapter 8 covers this; not yet extracted at detail level |
-| Capacity factor / availability target | not-yet-sourced | important | SOMBRERO Chapter 6 addresses this; no contemporary estimate available |
-| Target injection system capital cost | not-yet-sourced | important | Goodin 2007 covers fabrication, not injection system cost |
-| Fuel cost (Li-6, tritium startup) | derivable | important | Can be estimated from inventory (~few hundred grams T, market price) |
-| First-wall replacement cost and schedule (Inertia dry-wall or semi-liquid) | proprietary/unknown | important | Xcimer liquid wall avoids this; Inertia's architecture unspecified |
-| Rep-rate laser O&M (optics replacement at 10 Hz for Inertia) | truly-unknown | important | Xcimer whitepaper quantifies NIF problem ($40M/yr at rare shots); no 10 Hz projection |
-| Balance of plant costs (steam/Brayton cycle) | derivable | nice-to-have | Standard power plant economics apply; ARIES documentation applicable |
+|-----------|----------|-------------|-------|
+| Xcimer KrF laser cost breakdown by component at nth-of-a-kind | not-yet-sourced | blocking | <$100/J is a company claim without published component-level cost analysis; required to build credible capital cost model for Xcimer track |
+| Driver rep-rate O&M cost (laser component replacement at commercial rep rate) | not-yet-sourced | blocking | NIF $40M/yr at <1 shot/day provides extreme upper bound; no rep-rated lifetime data for KrF or DPSSL amplifiers |
+| Inertia power plant design (DPSSL architecture, chamber, BOP) | proprietary | important | Can proxy using SOMBRERO KrF analog; however capital cost structure differs significantly for 10 Hz vs. <1 Hz design |
+| Commercial-scale target gain validation (G > 50 at 10+ MJ) | derivable | important | Simulation gives G=65 (4 MJ) to G>200 (10 MJ); not yet experimentally validated. Xcimer Vulcan (2030 target) is first experimental test |
+| Xcimer-specific O&M cost model | not-yet-sourced | important | SOMBRERO/OSIRIS gives 75% availability; IFE-specific O&M drivers (optics, chamber, target supply) not broken out at Xcimer plant level |
+| Chamber clearing time vs. rep rate for HYLIFE-III + Xcimer design | not-yet-sourced | important | Governs maximum Xcimer rep rate; published HYLIFE design assumes 0.25 Hz; higher rates not validated |
+| First wall lifetime (liquid protection quantitative model for neutron flux) | not-yet-sourced | important | Xcimer claims structural lifetime enabled by liquid wall; no quantitative dpa calculation published for their specific design |
 
 ---
 
 ## Source Recommendations
 
-1. **LIFE plant study (Meier et al., LLNL/Dunne, 2011)**: "Timely Delivery of Laser Inertial Fusion Energy (LIFE)," *Fusion Science and Technology* 60(1). This is the only published NIF-heritage indirect-drive IFE plant study with CAS-level cost data. Cited in Xcimer whitepaper as reference [18]. Search OSTI or FST for this paper. — `not-yet-sourced` — **highly recommended** for capital cost CAS breakdown
-2. **SOMBRERO economic section (Chapter 8)**: The full SOMBRERO/OSIRIS report is already ingested at `iter-03/sources/osti-servlets-purl-833813.md` but only the table of contents and executive summary were read. The economic assessment (Chapter 8, pages 8-1 through 8-45) contains detailed COE calculations and CAS-level breakdown. **Read existing source more deeply** before ingesting new sources.
-3. **Xcimer ASPEN IFE Workshop 2022 presentation**: Referenced in dossier as https://lasers.llnl.gov/sites/lasers/files/2023-11/galloway-xcimer-IFE-workshop-2022_0.pdf. Contains ASPEN architecture, HYLIFE-III chamber design, and helium Brayton cycle details. Likely available as PDF. — `not-yet-sourced` — **recommended** for thermal cycle and capacity factor clarity.
-4. **HYLIFE-III FusEngDes 2024 paper** (ScienceDirect): Xcimer's FLiBe blanket nuclear analysis (TBR, tritium management). Cited in dossier. Should be ingested for detailed blanket and tritium parameters. — `not-yet-sourced` — **recommended** for tritium/blanket cost parameters.
-5. **Xcimer SPIE Photonics West 2026 presentation** (mentioned in dossier): Mike Dunne/Inertia may have presented plant design details here. — `not-yet-sourced` — **unverified — confirm existence before searching**.
-6. **McDougall et al. 2026 SPIE**: "Semiconductor Laser Costs for Inertial Fusion Energy Applications" — explicitly cited in Xcimer whitepaper (footnote 23/25). Directly relevant to DPSSL capital cost. — `not-yet-sourced` — **recommended** for Inertia LCOE.
+- **Driver cost at nth-of-a-kind scale**: Search OSTI for LIFE (Laser Inertial Fusion Energy) program cost reports from LLNL (~2009–2013) — this was the only published cost study for an NIF-derived IFE power plant and would provide a baseline for DPSSL cost scaling. Also search Fusion Science and Technology for HAPL (High Average Power Laser) program cost studies. `unverified — confirm existence before searching`
+
+- **Chamber clearing dynamics / rep-rate HYLIFE validation**: LLNL internal reports on HYLIFE-III dynamics simulations may be available via OSTI. Raffray et al. Fusion Science and Technology 49(1) 2006 on IFE thick liquid wall dynamics is explicitly cited in the Xcimer commercialization whitepaper and would address the chamber clearing gap. `unverified — confirm existence before searching`
+
+- **Xcimer ASPEN IFE Workshop 2022 presentation**: Available on the LLNL lasers website (https://lasers.llnl.gov/sites/lasers/files/2023-11/galloway-xcimer-IFE-workshop-2022_0.pdf) — cited in dossier but not extracted. This would provide the full ASPEN cost and design data. Should be ingested.
+
+- **HYLIFE-III Fusion Engineering and Design 2024 paper** (ScienceDirect, PIII/S0920379624001868): Nuclear analysis of FLiBe blanket (TBR>1.2) — cited in dossier. Should be extracted to resolve tritium breeding and first wall lifetime gaps. `unverified — confirm DOI resolves`
+
+- **Fleet-wide source disqualifications**:
+  - `knowledge/sources/energy_from_inertial_fusion/` — opened and read: this 1992 Physics Today overview article describes IFE subsystem categories (driver, target factory, reactor, generator) at conceptual level. It contains no quantitative cost breakdowns, availability assessments, or LCOE parameters that are not already covered in detail by the SOMBRERO/OSIRIS design study. Disqualified as redundant to the SOMBRERO source.
+  - `knowledge/sources/affordable_manageable_practical_and_scalable_amps_high/` — opened and read: the AMPS paper covers Pacific Fusion's pulser-driven IFE (MagLIF at 50–60 MA). Laser ICF appears only as a comparison foil (NIF Qf~0.016). Cost projections in this paper apply to the Pacific Fusion DS (~$5B capital), not to laser IFE systems. Disqualified as non-applicable for laser ICF cost modeling.
+  - `knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/` — index description documents HIF (heavy-ion beam) driver cost scaling (induction linac, Xe+1 ions at $120/J for OSIRIS); driver physics is fundamentally different from KrF or DPSSL lasers. The BOP and chamber cost data from this source are already represented through the SOMBRERO/OSIRIS design study which includes the OSIRIS HIF plant directly. Disqualified as redundant.
+  - `knowledge/sources/tea_dt_mfe_cost_analysis/` — MFE D-T tokamak cost analysis. IFE and MFE have fundamentally different capital cost drivers (no superconducting magnets, no steady-state plasma, driver system dominates vs. magnet system). BOP costs from MFE studies are not a reliable proxy for IFE. Disqualified as non-applicable.
+  - `knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/` — covers four ARPA-E ALPHA compact fusion concepts (MTF, FRC, compact tokamak, magnetized target). Not laser IFE. Disqualified as non-applicable.
+  - `knowledge/sources/aries_cost_account_documentation/` — CAS framework reference for MFE. The SOMBRERO/OSIRIS 1992 study already uses CAS-equivalent accounting for IFE. An IFE-specific cost account structure would differ (driver replaces magnets as the dominant CAS22 equivalent). Disqualified for this assessment; CAS methodology is addressed through SOMBRERO/OSIRIS and the Hawker model.
 
 ---
 
 ## Summary
 
-Proceed to full analysis with Xcimer's approach as the primary case and SOMBRERO (1992) as historical analog. The analysis can produce credible LCOE estimates for Xcimer's KrF IFE design using: (a) Xcimer whitepaper for laser cost (<$100/J target, quantified DPSSL baseline), (b) SOMBRERO Chapter 8 for CAS-level cost structure (read deeper into existing source), (c) Hawker 14-parameter model for sensitivity framing, and (d) HDD physics paper for target gain. Inertia's DPSSL approach should be modeled parametrically with stated assumptions, clearly flagged as pre-hardware with no published plant study. Two specific source acquisitions are recommended before the analysis: ingest the LIFE (2011) plant study and the HYLIFE-III FusEngDes (2024) paper, both of which would significantly reduce the blocking gap on capital cost structure.
+**Proceed to full analysis with the following approach**: The concept is sufficiently documented for a D1+ first-pass LCOE analysis, primarily anchored on the Xcimer track which has more published engineering detail. Use the Hawker 14-parameter IFE model (`knowledge/sources/a_simplified_economic_model_for_inertial_fusion/`) as the framework, the SOMBRERO KrF design study (`iter-03/sources/osti-servlets-purl-833813.md`) as the 1992 cost analog (COE 6.67 ¢/kWh), and the Xcimer commercialization whitepaper (`knowledge/sources/commercialization_of_laser_fusion_energy/`) for contemporary cost arguments. The Inertia track should be parameterized as a DPSSL variant with driver cost $700–1,000/J until a plant study is published.
+
+The two blocking gaps (nth-of-a-kind driver cost breakdown and rep-rated O&M cost) mean the LCOE model will span a factor of ~5–10x depending on which driver cost input is used; this uncertainty should be explicitly propagated in the model rather than treated as resolvable before the analysis begins. The `$0.01/kWh` back-solve will need to address the gain gap (commercial requirement G>50 vs. demonstrated G~4) as the most fundamental binding constraint.
 
 ---
 
@@ -180,10 +148,10 @@
 overall_rating: "Mostly Ready"
 blocking_count: 2
 important_count: 7
-counting_method: "section_5_missing_parameters plus section_3_gaps deduplicated; blocking = capital_cost_cas_breakdown (no contemporary plant study ingested) + inertia_laser_capital_cost (proprietary); important = chamber_capital_cost, OM_cost_estimates, capacity_factor, target_injection_cost, fuel_cost, first_wall_replacement_inertia, rep_rate_laser_om_inertia"
+counting_method: "all_sections_deduplicated — blocking: nth-of-a-kind driver cost breakdown (Section 5), rep-rated driver O&M cost anchor (Sections 3+5); important: Inertia plant design gap (Sections 1+5), commercial target gain unvalidated (Sections 2+5), driver lifetime at rep rate (Sections 3+5), chamber clearing validation (Sections 2+5), first wall lifetime quantitative model (Sections 3+5), E-beam cathode supply chain (Section 4), hohlraum mass-production supply chain (Section 4) — counted as 7 unique items"
 section_coverage:
   availability_of_data:       "Good"
-  system_function:            "Good"
+  system_function:            "Partial"
   subsystem_maturity:         "Partial"
   materials_supply_chain:     "Partial"
   lcoe_parameter_extraction:  "Partial"
```
