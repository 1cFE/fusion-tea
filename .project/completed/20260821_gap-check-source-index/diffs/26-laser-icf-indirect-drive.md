# Diff: 26-laser-icf-indirect-drive

**Generated:** 2026-05-22T11:01:32-07:00

## Counts

| field | baseline | new | Δ |
|-------|----------|-----|---|
| blocking_count   | 2 | 2 | 0 |
| important_count  | 7 | 7 | - |
| overall_rating   | Mostly Ready | Mostly Ready | - |

## Fleet-source citations (new only — grep `knowledge/sources/` or `PyFECONS`)

```
22:- Xcimer commercialization whitepaper (Feb 2026): covers laser cost comparison (DPSSL at $700–1,000/J floor vs. KrF target <$100/J), chamber architecture (HYLIFE), and deployment roadmap (`knowledge/sources/commercialization_of_laser_fusion_energy/`).
27:- Technology-agnostic LCOE model: Hawker (2020) 14-parameter model, Monte Carlo parameter space, LCOE as low as $25/MWh under optimistic assumptions (`iter-03/sources/pmc-articles-pmc7658748.md`; also at `knowledge/sources/a_simplified_economic_model_for_inertial_fusion/`).
45:- The Xcimer whitepaper provides a detailed account of why NIF architecture is not commercially scalable (optics damage, laser efficiency, chamber wall replacement), and explicitly frames all three major system-function challenges: confinement performance, materials/chamber survivability, and cost (`knowledge/sources/commercialization_of_laser_fusion_energy/`).
```

## Blocking-tier lines (baseline)

```
138:| Capital cost by CAS subsystem | not-yet-sourced | blocking | LIFE power plant study (~2010–2012 LLNL) and HYLIFE-II cost study are primary analogues; ASPEN IFE Workshop slide deck may contain Xcimer-specific estimates |
139:| Full plant capital cost ($/kWe) | not-yet-sourced | blocking | LIFE study cited ~$7B for a 1 GWe plant (pre-ignition era estimate) — needs verification and adjustment |
```

## Blocking-tier lines (new)

```
80:- Mass-production target fabrication at rep-rate (500,000/day for 10 Hz): no demonstrated capability — `truly-unknown` at production scale — **blocking** for capacity factor assumptions
147:| Capital cost breakdown by CAS category (contemporary) | not-yet-sourced | blocking | SOMBRERO (1992) has this but for different technology; LIFE (2011) likely has it but not ingested |
148:| Laser capital cost (Inertia Thunderwall, 10 MJ DPSSL) | proprietary | blocking | Company has not published engineering cost analysis; only aspiration-level claims |
```

## Full unified diff (truncated to 400 lines)

```diff
--- /tmp/gap_baselines_2026-05-22/26-laser-icf-indirect-drive.md	2026-05-22 09:21:13.874053170 -0700
+++ /home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/26-laser-icf-indirect-drive/gap_report.md	2026-05-22 11:01:32.346962306 -0700
@@ -1,4 +1,4 @@
-I have all the materials I need. Let me write the gap assessment now.
+I now have sufficient information to write the comprehensive gap assessment.
 
 ---
 
@@ -7,81 +7,79 @@
 ## Overall Readiness
 **Rating**: Mostly Ready
 
-**Summary**: The physics basis for this concept is unusually well-documented due to NIF's 10 successful ignition experiments and Xcimer's published plant studies (ASPEN, HYLIFE-III). The primary readiness constraint is the asymmetry between the two companies: Xcimer has published technical depth sufficient for most D1+ sections, while Inertia has only high-level public materials with no plant design document. LCOE modeling is feasible using HYLIFE-III and LIFE-era analogues, but will require explicit extrapolation assumptions for capital cost structure and target economics.
+**Summary**: This concept benefits from the deepest physics validation base of any private fusion concept — 10 demonstrated ignition experiments at NIF, with peak gain of 4.13 (April 2025). Xcimer has also published a detailed commercialization whitepaper (Feb 2026) with explicit cost comparisons, and the SOMBRERO study (1992) provides a complete CAS-level economic analysis for a KrF laser-driven IFE plant. The main gaps are (1) no contemporary full-plant CAS-breakdown study exists; all numbers must be synthesized from multiple partial sources; and (2) Inertia's Thunderwall DPSSL plant details are almost entirely unpublished, limiting comparative analysis to Xcimer's approach.
 
 ---
 
 ## Section Coverage
 
 ### 1. Availability of Data
-**Coverage**: Moderate-to-Good
+**Coverage**: Good (Xcimer) / Poor (Inertia)
 
 **Available**:
-- NIF ignition results (10 experiments, Dec 2022–Oct 2025, peak 8.6 MJ yield at gain ~4.1) — well-documented via LLNL public pages; reproducibility data (gain variance across shots) directly relevant to capacity factor analysis
-- Xcimer ASPEN laser architecture: $5–10/J hardware cost claim, 2 amplifiers → 12 MJ, KrF 248 nm UV, sub-Hz (ASPEN IFE Workshop 2022 presentation)
-- Xcimer HYLIFE-III nuclear engineering: FLiBe blanket, TBR > 1.2 (Fusion Engineering and Design 2024); liquid first wall concept; 30-year structural lifetime claim
-- Xcimer HDD target physics: Physics of Plasmas 31(11), 112708 (2024) — energy coupling mechanisms
-- Inertia Enterprises: Thunderwall specs (10 kJ/beam, 10 Hz, 10% wallplug efficiency, 1000–4000 beamlines), target cost claim (<$1 each), pilot plant output (50 MWe), commercial target (>1 GWe); all from website/interviews/press releases
-- LIFE power plant concept (LLNL, 2010–2013) — **not yet sourced** but known to contain full capital cost breakdowns for an indirect-drive IFE plant; most directly applicable LCOE analogue available
-- HYLIFE-II / HYLIFE-III chamber studies — **partially sourced** (HYLIFE-III nuclear paper is in sources; HYLIFE-II cost study not yet retrieved)
+- NIF ignition physics: extensively documented through Oct 2025 with 10 experiments (`iter-01/sources/nif-ignition-achievements.md`, `iter-02/sources/nif-ignition-updates-2025.md`). Peak yield 8.6 MJ, gain 4.13 (Apr 2025).
+- Xcimer physics: HDD target paper in *Phys. Plasmas* 31(11) (2024) — full radiation-hydrodynamic design with gain = 65 at 4 MJ input (`iter-02/sources/xcimer-hybrid-direct-drive-evolution.md`).
+- Xcimer commercialization whitepaper (Feb 2026): covers laser cost comparison (DPSSL at $700–1,000/J floor vs. KrF target <$100/J), chamber architecture (HYLIFE), and deployment roadmap (`knowledge/sources/commercialization_of_laser_fusion_energy/`).
+- Xcimer hardware milestone: LPK platform completed June 2025, first private-sector e-beam excimer laser in 20+ years (`iter-02/sources/xcimer-laser-milestones-2025.md`).
+- SOMBRERO plant study (1992): full 1000 MWe KrF laser IFE plant, including CAS-level economic assessment, driver design (3.4 MJ, 6.7 Hz, 7.5% efficiency), blanket, and target systems (`iter-03/sources/osti-servlets-purl-833813.md`).
+- HYLIFE-II tritium management (1992): tritium inventory (~190 g), FLiBe vacuum disengager design, total system cost $92M (`iter-03/sources/osti-biblio-10179076.md`).
+- Target fabrication: Goodin 2007 paper with cost estimates (~$0.17/target nth-of-kind for 500,000/day) (`iter-03/sources/fire-fpa07-goodin-icf-fuel.md`).
+- Technology-agnostic LCOE model: Hawker (2020) 14-parameter model, Monte Carlo parameter space, LCOE as low as $25/MWh under optimistic assumptions (`iter-03/sources/pmc-articles-pmc7658748.md`; also at `knowledge/sources/a_simplified_economic_model_for_inertial_fusion/`).
+- Inertia: $450M Series A announcement (Feb 2026) with high-level plant description — 10 kJ × 1000–4000 beamlines, 10 Hz, <$1/target target (`iter-02/sources/inertia-enterprises-2026-update.md`).
 
 **Missing**:
-- Inertia published plant design document (equivalent of a LIFE or HYLIFE study)
-- Full LLNL LIFE power plant cost study (~2010–2012 reports)
-- HYLIFE-II chamber cost estimates (older but relevant)
-- Fusion power plant economics studies from IFE workshop proceedings (IAEA, FPA)
+- Inertia has no published plant design study, blanket engineering details, or detailed cost data.
+- The LIFE concept (the closest NIF-derived indirect-drive IFE plant study, LLNL 2011) was captured only by reference in the Xcimer whitepaper, not ingested as a primary source.
+- No post-2010 full plant study for pure indirect-drive laser IFE exists in the source set.
 
 **Gaps**:
-- No published reactor design document for Inertia — `proprietary` (likely exists internally; $450M Series A suggests detailed internal engineering, none public) — **important**
-- LIFE and HYLIFE-II cost studies not yet retrieved — `not-yet-sourced` — **important for LCOE**
-- Xcimer's ASPEN IFE Workshop 2022 slide deck cited in dossier but not extracted as a source document — `not-yet-sourced` — **blocking for capital cost structure**
+- No published Inertia plant design — `proprietary` — **important**: limits comparative analysis to Xcimer's approach
+- LIFE (2011) plant study not ingested — `not-yet-sourced` — **important**: only direct NIF-heritage IFE plant study ever published
 
 ---
 
 ### 2. Challenges in Capturing System Function
-**Coverage**: Good
+**Coverage**: Good (physics and challenges well characterized)
 
 **Available**:
-- Laser–target coupling physics well-understood from NIF heritage; hohlraum X-ray conversion efficiency and capsule implosion physics published extensively
-- Gain variability documented: NIF shots ranged from gain ~1.5 to ~4.1 across 10 experiments; yield sensitivity to target manufacturing and laser delivery precision is a documented challenge (NIF ignition updates source)
-- Power plant gain requirements understood conceptually: need target gain ×60–100 for energy-positive power plant given laser wallplug efficiency (~10%) and thermal conversion efficiency (~40–45%)
-- Thunderwall's modular architecture described (1000–4000 beamlines); parallelism as a failure-tolerance mechanism implicit in design
-- Sub-Hz vs. 10 Hz rep rate divergence is a documented design choice with different chamber clearing and target injection implications
-- HYLIFE-III liquid wall concept addresses neutron damage and chamber clearing simultaneously — published mechanism
+- The Xcimer whitepaper provides a detailed account of why NIF architecture is not commercially scalable (optics damage, laser efficiency, chamber wall replacement), and explicitly frames all three major system-function challenges: confinement performance, materials/chamber survivability, and cost (`knowledge/sources/commercialization_of_laser_fusion_energy/`).
+- The HDD paper quantifies the energy budget chain from wall-plug to target gain: laser absorption 97%, hydrodynamic efficiency 8%, target gain 65 at 4 MJ input (`iter-02/sources/xcimer-hybrid-direct-drive-evolution.md`). The wall-plug gain requirement (~10) is explicitly derived.
+- NIF's energy flow is quantified in the Xcimer science page: 400 MJ from grid → 2 MJ laser → 250 kJ to capsule → 5 MJ fusion energy (0.5% wallplug NIF) (`iter-03/sources/xcimer-science.md`).
+- Chamber clearing time as a driver of rep-rate ceiling is addressed; the liquid wall requires <1 Hz to allow flow recovery.
+- Modeling challenges: radiation-hydrodynamic simulation fidelity, laser-plasma instabilities (LPI), cross-beam energy transfer (CBET) and how HDD geometry mitigates them — all covered in the HDD paper.
 
 **Missing**:
-- Quantified target injection and tracking performance at 10 Hz (Inertia) — no demonstrated system at this rate
-- Chamber clearing time between shots at sub-Hz (Xcimer) — HYLIFE concept addresses this but no experimental data
-- Laser–plasma interaction (LPI) risks at power plant scale — mentioned in NIF context but not quantified for ASPEN/Thunderwall energy levels
+- No detailed analysis of what target implosion performance must scale to for commercial operation (gain >100 requirement vs. demonstrated gain ~65 in simulation at 4 MJ).
+- Inertia's "10x efficiency vs NIF" claim (10% wallplug stated) is stated but not derived from published engineering analysis.
+- Chamber debris clearing dynamics (gas/plasma recovery between shots) are not quantified for Inertia's 10 Hz architecture.
 
 **Gaps**:
-- Target injection/tracking at 10 Hz: no demonstrated system exists anywhere — `truly-unknown` for this rep rate — **important**
-- Power plant gain target achievability: commercial targets need ×60–100 gain vs. NIF's best of ×4.1 — this gap is well-known but its resolution is uncertain — `truly-unknown` until new experiments — **important (not blocking for qualitative analysis, but critical for quantitative)**
-- LPI characterization at 10–12 MJ laser energy: extrapolation from NIF's 2 MJ is uncertain — `not-yet-sourced` (simulation papers exist in OSTI) — **nice-to-have**
+- Inertia chamber clearing dynamics at 10 Hz: unresolved — `not-yet-sourced` — **important**: determines whether 10 Hz rep-rate is feasible with a liquid wall or requires a dry wall
+- Target gain scaling from 65 (simulation) to commercial requirement (>100–150): basis established but not fully characterized — `derivable` — **nice-to-have**
 
 ---
 
 ### 3. Maturity of Key Subsystems and Components
-**Coverage**: Partial
+**Coverage**: Partial (Xcimer well-characterized, Inertia sparse)
 
 **Available**:
-- **Target physics (NIF heritage)**: TRL 5–6 for the ignition implosion itself; NIF targets manufactured at small scale with high precision
-- **Xcimer Phoenix laser**: TRL 4 for KrF excimer laser hardware (first private-sector e-beam excimer, record pulse length Jun 2025); TRL 2–3 for full ASPEN scale (12 MJ, 2 amplifiers, not yet built)
-- **Inertia Thunderwall**: TRL 2–3; prototype in development as of early 2026; no hardware demonstrated
-- **HYLIFE-III chamber concept**: TRL 3; engineering design published; no experimental chamber
-- **FLiBe tritium breeding**: TRL 3–4; extensive HYLIFE-II/III analysis; no operating IFE tritium blanket
-- **Liquid Li tritium extraction (Inertia)**: TRL 2; "still an area of active development" per company
+- **KrF excimer laser (Xcimer)**: LPK platform completed June 2025, record 3 µs pulse length achieved. Phoenix prototype on track for 2026. Vulcan (12 MJ) targeted 2030. TRL 3–4 for the laser subsystem (`iter-02/sources/xcimer-laser-milestones-2025.md`).
+- **DPSSL (Inertia Thunderwall)**: Described as pre-hardware as of Mar 2026. Semiconductor diode technology mature at small scale but 10 MJ/10 Hz DPSSL has no demonstrated hardware. TRL 1–2.
+- **Hohlraum/target physics**: NIF has demonstrated 10 ignitions with indirect drive, gain up to 4.13. TRL 6 for physics, TRL 2–3 for production-rate target manufacturing.
+- **Target fabrication**: All process steps identified (Goodin 2007), but mass production (500,000 targets/day) undemonstrated. TRL 2–3 (`iter-03/sources/fire-fpa07-goodin-icf-fuel.md`).
+- **FLiBe blanket (Xcimer/HYLIFE-III)**: Nuclear analysis published in *Fusion Engineering and Design* (2024), TBR > 1.2 confirmed. Structural engineering and vacuum disengager at conceptual stage. TRL 2–3.
+- **Tritium management**: HYLIFE-II conceptual design exists with engineering detail ($92M system cost, 2 TBq/s tritium bred). Experiment needed to validate vacuum disengager. TRL 2.
+- **Target injection / tracking**: Conceptual designs exist (SOMBRERO 1992, section 4.2–4.3); no rep-rate validated hardware.
 
 **Missing**:
-- TRL breakdown for target mass manufacturing at <$1/target — this is the most critical unquantified subsystem for IFE economics
-- TRL for target injection and tracking systems at 10 Hz
-- TRL for final optics protection (laser enters chamber — debris/neutron damage issue specific to IFE)
-- DPSSL at GW-class average power — no TRL data for 100 MW average power laser (Thunderwall commercial: 10 MJ × 10 Hz = 100 MW)
+- Inertia's liquid lithium chamber design has no published engineering basis.
+- No publicly demonstrated rep-rate laser ICF target injection system.
+- Chamber wall survivability under sustained pulsed load: HYLIFE concept studies exist but no prototyped hardware.
 
 **Gaps**:
-- Target mass manufacturing at <$1/target, 10/second: no demonstrated process — `truly-unknown` at commercial scale — **blocking for ICF economics credibility**
-- Final optic lifetime under repetitive fusion neutron/debris flux: known IFE challenge, no solution demonstrated — `not-yet-sourced` (IAEA/FPA reports discuss this) — **important**
-- DPSSL at 100 MW average power: extrapolation from existing ~kW-class DPSSL systems; no roadmap published — `not-yet-sourced` — **important**
+- Mass-production target fabrication at rep-rate (500,000/day for 10 Hz): no demonstrated capability — `truly-unknown` at production scale — **blocking** for capacity factor assumptions
+- Target injection and tracking at >0.25 Hz: undemonstrated — `truly-unknown` at power-plant rates — **important**
+- Inertia Thunderwall DPSSL at 10 kJ × 10 Hz × 1000+ beamlines: no hardware, no published roadmap beyond $450M Series A — `proprietary` — **important**
 
 ---
 
@@ -89,22 +87,24 @@
 **Coverage**: Partial
 
 **Available**:
-- **Tritium**: Startup supply from U.S. government stockpiles (Inertia confirms); operational inventory ~few hundred grams on-site; breeding path through lithium blanket; startup challenge well-documented in fusion literature
-- **Lithium**: Both companies need flowing liquid Li or FLiBe; Inertia quantifies as "15–20 EV batteries" worth per plant; low criticality for supply (lithium is not scarce)
-- **FLiBe (Xcimer)**: Beryllium in FLiBe is a supply/cost concern; not addressed in sources
-- **KrF gas (Xcimer)**: Krypton and fluorine gas supplies for excimer medium; not addressed in sources
-- **DPSSL diode arrays (Inertia)**: Semiconductor laser diode arrays at GW-scale average power — no published supply chain analysis
+- **Tritium**: Inertia explicitly notes startup tritium from U.S. government stockpiles; on-site inventory "few hundred grams"; lithium equivalent of ~15 EVs per plant (`iter-01/sources/inertia-enterprises-website-and-faq.md`, `dossier.md`). TBR > 1.2 for Xcimer/HYLIFE-III FLiBe blanket.
+- **FLiBe (Xcimer blanket)**: Li₂BeF₄ uses both beryllium (limited mining capacity) and enriched lithium. Li-6 enrichment supply chains are limited but exist (government enrichment programs). Xcimer explicitly says their approach uses "commercially available materials" due to liquid first wall protection (`iter-02/sources/xcimer-laser-milestones-2025.md`, commercialization whitepaper).
+- **Hohlraum materials**: NIF uses gold; HDD design may reduce or eliminate hohlraum mass per shot (lower-Z baffle materials mentioned in HDD paper). Gold is expensive but manageable at ICF target quantities.
+- **DPSSL laser diodes**: Xcimer whitepaper calculates a floor cost of $7–10B for 10 MJ DPSSL laser in diodes alone, with current supply chains requiring order-of-magnitude scale-up. This is a fundamental supply chain bottleneck for Inertia's architecture.
+- **KrF excimer gas medium**: Krypton (rare gas) and fluorine chemistry — industrial supply chains exist from semiconductor lithography, but not at fusion-laser scale.
+- **Carbon-carbon structural materials**: SOMBRERO used C/C first wall (1992); Xcimer uses liquid FLiBe protection of steel → avoids exotic materials for structure.
 
 **Missing**:
-- Beryllium supply and cost (FLiBe component) — known concern in fusion blanket community, not addressed in Phase 1a sources
-- Semiconductor diode supply chain for Thunderwall at 1000–4000 beamline scale
-- Target capsule materials (hohlraum gold/depleted uranium, capsule ablator materials) at mass-manufacturing scale
+- No dedicated supply chain analysis for KrF gas at fusion-plant scale (how many tons of Kr/F₂ per year for a 12 MJ system).
+- Li-6 enrichment demand and supply chain at multi-GW scale not analyzed.
+- Beryllium supply (FLiBe contains Be) not addressed.
+- Hohlraum material per shot at power plant rate (target → consumption rate of gold or substitute) not quantified.
 
 **Gaps**:
-- Beryllium supply/cost for FLiBe blanket — `not-yet-sourced` (published in blanket/materials literature) — **important for Xcimer cost model**
-- Gold/DU hohlraum material supply at 864,000 shots/day (10 Hz): not addressed anywhere — `truly-unknown` at commercial scale — **important**
-- Diode array supply chain for Thunderwall — `not-yet-sourced` — **important for Inertia capital cost**
-- Capsule ablator material (e.g., HDC diamond, CH polymer) at commercial scale — `not-yet-sourced` — **important**
+- KrF/excimer gas supply chain at plant scale: not analyzed — `not-yet-sourced` — **nice-to-have**
+- Li-6 enrichment supply chain for multi-GW FLiBe deployment: not analyzed — `not-yet-sourced` — **important** for long-term scale-up analysis
+- Beryllium supply constraints for FLiBe at GW scale: not analyzed — `not-yet-sourced` — **nice-to-have**
+- Laser diode supply chain (Inertia DPSSL): cost floor quantified in whitepaper, but supply chain development pathway not published — `proprietary` — **important** for Inertia LCOE
 
 ---
 
@@ -112,68 +112,67 @@
 **Coverage**: Partial
 
 **Available Parameters**:
+
 | Parameter | Value/Range | Source | Confidence |
-|-----------|-------------|--------|------------|
-| Net electrical output (pilot) | 50 MWe | Inertia 2026 update | m |
-| Net electrical output (commercial) | >1 GWe / 1.5 GW | Inertia website, ENR interview | m |
-| Target gain (prototype) | 18× | Inertia 2026 update | m |
-| Target gain (commercial) | >30× | Inertia 2026 update | m |
-| NIF demonstrated gain | 1.5–4.1 (10 shots) | NIF ignition updates | h |
-| Laser wallplug efficiency (Inertia) | ~10% | Inertia website | m |
-| Laser wallplug efficiency (Xcimer) | >10× NIF (~5–10%) | Xcimer website | m |
-| Laser hardware cost (Xcimer ASPEN) | $5–10/J | Xcimer website | m |
-| Rep rate (Inertia) | 10 Hz | Inertia website | h |
-| Rep rate (Xcimer) | <1 Hz (0.25 Hz baseline) | Xcimer website / ASPEN presentation | h |
-| Target cost (Inertia) | <$1 per target | Inertia website | m-l |
-| Wall-plug gain target (Xcimer) | ~10 | Xcimer science page | m |
-| Thermal efficiency (HYLIFE-III) | ~45% (helium Brayton per 2022 ASPEN presentation) | ASPEN IFE Workshop 2022 | m |
-| Tritium breeding ratio (Xcimer) | TBR > 1.2 | HYLIFE-III FED paper (2024) | h |
-| Chamber lifetime goal (Xcimer) | 30 years | Xcimer website | l |
-| Vulcan laser energy | 12 MJ | Xcimer website | h |
-| Thunderwall laser energy | 10 MJ | Inertia website | h |
+|---|---|---|---|
+| Target gain (HDD simulation) | 65 (4 MJ), >200 (8 MJ projected) | Xcimer HDD Phys. Plasmas 2024 | m |
+| Target gain (NIF demonstrated) | 1.7–4.1 (2022–2025) | NIF ignition updates | h |
+| Laser wall-plug efficiency (NIF) | ~0.5% (flashlamp) | Xcimer science page | h |
+| Laser wall-plug efficiency (DPSSL, expected) | ~15% | Xcimer whitepaper | m |
+| Laser wall-plug efficiency (KrF excimer, target) | ≥12% | HDD paper, whitepaper | m |
+| Required wall-plug gain for commercial operation | ~10 | Xcimer whitepaper | m |
+| Plant electric output (Xcimer target) | GW-class (unspecified) | Dossier | l |
+| Plant electric output (Inertia) | ~1.5 GW | Inertia ENR interview | l |
+| Rep rate (Xcimer) | 0.25–1 Hz | Xcimer/ASPEN | h |
+| Rep rate (Inertia) | ~10 Hz | Inertia website | h |
+| Thermal conversion (Xcimer, website) | Steam turbine | Xcimer science page | m |
+| Thermal conversion (HYLIFE-III) | Helium Brayton, 45% efficiency | ASPEN 2022 presentation | m |
+| SOMBRERO net plant efficiency | 35% (including laser power) | SOMBRERO 1992 OSTI | m |
+| SOMBRERO laser power consumption | 304 MWe of 1000 MWe gross | SOMBRERO 1992 OSTI | m |
+| SOMBRERO availability assessment | Detailed (Chapter 6) | SOMBRERO 1992 OSTI | m |
+| DPSSL laser capital cost floor | $700–$1,000/J (10 MJ → $7–10B) | Xcimer whitepaper 2026 | h |
+| KrF excimer laser cost target | <$100/J | Xcimer whitepaper 2026 | l (projected) |
+| NIF facility cost | ~$3.5–7B (2 MJ) | Xcimer whitepaper | h |
+| Tritium management system (HYLIFE-II) | $92M system cost | OSTI 10179076 | m |
+| Target cost (Inertia aspiration) | <$1/target | Inertia website | l (unvalidated) |
+| Target cost (Goodin 2007, nth-of-kind) | ~$0.17/target | Goodin 2007 paper | m (dated) |
+| TBR (Xcimer/HYLIFE-III FLiBe) | >1.2 | HYLIFE-III FusEngDes 2024 | h |
+| LCOE range (Hawker model, optimistic) | $25–100/MWh | Hawker 2020 PMC | m |
+| IFE driver cost sensitivity | Dominant cost lever | Hawker 2020 model | h |
 
 **Missing Parameters**:
+
 | Parameter | Gap Type | Criticality | Notes |
-|-----------|----------|-------------|-------|
-| Capital cost by CAS subsystem | not-yet-sourced | blocking | LIFE power plant study (~2010–2012 LLNL) and HYLIFE-II cost study are primary analogues; ASPEN IFE Workshop slide deck may contain Xcimer-specific estimates |
-| Full plant capital cost ($/kWe) | not-yet-sourced | blocking | LIFE study cited ~$7B for a 1 GWe plant (pre-ignition era estimate) — needs verification and adjustment |
-| Operating cost: first wall replacement schedule | not-yet-sourced | important | Liquid wall concept (HYLIFE) claims no first-wall replacement; solid first wall is standard IFE challenge |
-| Operating cost: target fabrication cost at scale | derivable | important | <$1/target × 10 Hz × 8760 hr/yr ≈ $315M/yr for 1 GWe plant; plausible to estimate from stated values |
-| Thermal efficiency (Inertia) | not-yet-sourced | important | Only "steam" stated; steam Rankine is ~33–38% vs. HYLIFE-III helium Brayton at 45% |
-| Capacity factor / availability | derivable | important | Can be estimated from rep rate, shot-to-shot gain variance, and maintenance assumptions; no published value |
-| Fuel cost (tritium acquisition cost) | derivable | important | Government stockpile startup cost; breeding during operation is low ongoing cost |
-| Laser replacement cost / lifetime | not-yet-sourced | important | KrF gas lifetime, DPSSL diode replacement; not published for either company |
-| Q_target for commercial power plant | derivable | important | Derivable from stated wallplug efficiency, thermal efficiency, and plant gain targets |
-| Balance of plant cost | not-yet-sourced | nice-to-have | Should be similar to steam/gas turbine power plant; LIFE study provides estimates |
+|---|---|---|---|
+| Capital cost breakdown by CAS category (contemporary) | not-yet-sourced | blocking | SOMBRERO (1992) has this but for different technology; LIFE (2011) likely has it but not ingested |
+| Laser capital cost (Inertia Thunderwall, 10 MJ DPSSL) | proprietary | blocking | Company has not published engineering cost analysis; only aspiration-level claims |
+| Chamber capital cost (Xcimer HYLIFE-III, detailed) | not-yet-sourced | important | HYLIFE-III FusEngDes paper covers nuclear analysis, not full capital cost breakdown |
+| O&M cost estimates (any contemporary IFE design) | not-yet-sourced | important | SOMBRERO Chapter 8 covers this; not yet extracted at detail level |
+| Capacity factor / availability target | not-yet-sourced | important | SOMBRERO Chapter 6 addresses this; no contemporary estimate available |
+| Target injection system capital cost | not-yet-sourced | important | Goodin 2007 covers fabrication, not injection system cost |
+| Fuel cost (Li-6, tritium startup) | derivable | important | Can be estimated from inventory (~few hundred grams T, market price) |
+| First-wall replacement cost and schedule (Inertia dry-wall or semi-liquid) | proprietary/unknown | important | Xcimer liquid wall avoids this; Inertia's architecture unspecified |
+| Rep-rate laser O&M (optics replacement at 10 Hz for Inertia) | truly-unknown | important | Xcimer whitepaper quantifies NIF problem ($40M/yr at rare shots); no 10 Hz projection |
+| Balance of plant costs (steam/Brayton cycle) | derivable | nice-to-have | Standard power plant economics apply; ARIES documentation applicable |
 
 ---
 
 ## Source Recommendations
 
-1. **LLNL LIFE Power Plant Study reports (~2010–2012)** — `not-yet-sourced` — Search OSTI (`osti.gov`) for "LIFE laser inertial fusion energy power plant cost" or "Moses LIFE plant design." These contain full capital cost breakdowns for an indirect-drive IFE plant. Primary analogue for capital cost structure. *Note: pre-ignition era; cost estimates may be pessimistic but structure is relevant.*
-
-2. **Xcimer ASPEN IFE Workshop 2022 slide deck** — `not-yet-sourced` — Cited in dossier; URL listed as `lasers.llnl.gov/sites/lasers/files/2023-11/galloway-xcimer-IFE-workshop-2022_0.pdf`. Contains power plant architecture details including chamber design and possibly cost estimates for laser system. Should be extracted as a full source document. *Flag: unverified that the URL is still live — confirm existence before fetching.*
-
-3. **HYLIFE-II cost study** — `not-yet-sourced` — HYLIFE-II (1991 LLNL report by Moir et al.) contained detailed chamber cost estimates. Search OSTI for "HYLIFE-II lithium injection fusion energy Moir." Relevant to Xcimer's chamber concept even though dated.
-
-4. **IFE Workshop proceedings (IAEA/FPA, 2022–2025)** — `not-yet-sourced` — Annual IFE Workshop proceedings contain laser cost reduction roadmaps, target economics analysis, and chamber engineering updates. Search DOE Office of Science for "IFE Workshop 2023/2024 proceedings" or check `ifs.utexas.edu` for archived talks. Specific value: target cost roadmap and laser cost per joule projections.
-
-5. **Fusion Power Associates (FPA) annual conference papers on IFE economics** — `not-yet-sourced` — FPA meetings regularly include IFE plant economics papers. Search for "IFE laser power plant economics 2020–2025."
-
-6. **Final optic damage / debris mitigation literature** — `not-yet-sourced` — Search OSTI for "IFE final optic lifetime" or "ICF laser optic neutron damage." This is a known system function challenge; papers from LLE Rochester and LLNL address it. *Unverified — confirm existence before searching.*
-
-7. **Target mass manufacturing cost roadmap** — `not-yet-sourced` — NRL, GA, and Schafer Corporation have published target fabrication cost analyses. Search OSTI for "IFE target fabrication cost" or "ICF target mass production." Key parameter for operating cost model.
+1. **LIFE plant study (Meier et al., LLNL/Dunne, 2011)**: "Timely Delivery of Laser Inertial Fusion Energy (LIFE)," *Fusion Science and Technology* 60(1). This is the only published NIF-heritage indirect-drive IFE plant study with CAS-level cost data. Cited in Xcimer whitepaper as reference [18]. Search OSTI or FST for this paper. — `not-yet-sourced` — **highly recommended** for capital cost CAS breakdown
+2. **SOMBRERO economic section (Chapter 8)**: The full SOMBRERO/OSIRIS report is already ingested at `iter-03/sources/osti-servlets-purl-833813.md` but only the table of contents and executive summary were read. The economic assessment (Chapter 8, pages 8-1 through 8-45) contains detailed COE calculations and CAS-level breakdown. **Read existing source more deeply** before ingesting new sources.
+3. **Xcimer ASPEN IFE Workshop 2022 presentation**: Referenced in dossier as https://lasers.llnl.gov/sites/lasers/files/2023-11/galloway-xcimer-IFE-workshop-2022_0.pdf. Contains ASPEN architecture, HYLIFE-III chamber design, and helium Brayton cycle details. Likely available as PDF. — `not-yet-sourced` — **recommended** for thermal cycle and capacity factor clarity.
+4. **HYLIFE-III FusEngDes 2024 paper** (ScienceDirect): Xcimer's FLiBe blanket nuclear analysis (TBR, tritium management). Cited in dossier. Should be ingested for detailed blanket and tritium parameters. — `not-yet-sourced` — **recommended** for tritium/blanket cost parameters.
+5. **Xcimer SPIE Photonics West 2026 presentation** (mentioned in dossier): Mike Dunne/Inertia may have presented plant design details here. — `not-yet-sourced` — **unverified — confirm existence before searching**.
+6. **McDougall et al. 2026 SPIE**: "Semiconductor Laser Costs for Inertial Fusion Energy Applications" — explicitly cited in Xcimer whitepaper (footnote 23/25). Directly relevant to DPSSL capital cost. — `not-yet-sourced` — **recommended** for Inertia LCOE.
 
 ---
 
 ## Summary
 
-**Proceed to full analysis with stated caveats.** The data available is sufficient to construct a credible D1+ qualitative write-up and a first-pass LCOE model, but with important structural gaps in capital cost data. Recommended approach:
+Proceed to full analysis with Xcimer's approach as the primary case and SOMBRERO (1992) as historical analog. The analysis can produce credible LCOE estimates for Xcimer's KrF IFE design using: (a) Xcimer whitepaper for laser cost (<$100/J target, quantified DPSSL baseline), (b) SOMBRERO Chapter 8 for CAS-level cost structure (read deeper into existing source), (c) Hawker 14-parameter model for sensitivity framing, and (d) HDD physics paper for target gain. Inertia's DPSSL approach should be modeled parametrically with stated assumptions, clearly flagged as pre-hardware with no published plant study. Two specific source acquisitions are recommended before the analysis: ingest the LIFE (2011) plant study and the HYLIFE-III FusEngDes (2024) paper, both of which would significantly reduce the blocking gap on capital cost structure.
 
-1. **Proceed now** on qualitative sections 1–4 using available sources; the physics and technology landscape are well-documented.
-2. **For LCOE modeling**: Use LIFE power plant cost structure as the primary capital cost analogue (adjusted for modern laser efficiency improvements), HYLIFE-III for chamber/blanket costs, and stated per-target cost for operating cost. Flag all such extrapolations explicitly.
-3. **Before or during analysis**: Retrieve the ASPEN IFE Workshop 2022 slide deck (URL confirmed in dossier) and search for the LIFE power plant cost reports on OSTI — these are the two most impactful `not-yet-sourced` documents for LCOE parameter completeness.
-4. The Xcimer/Inertia asymmetry in published detail is itself an analysis finding: the concept's cost modeling basis is substantially stronger on the Xcimer/HYLIFE-III side than on the Inertia side. This should be called out explicitly in the analysis.
+---
 
 ## Structured summary (machine-readable)
 
@@ -181,11 +180,11 @@
 overall_rating: "Mostly Ready"
 blocking_count: 2
 important_count: 7
-counting_method: "section_5_missing_parameters"
+counting_method: "section_5_missing_parameters plus section_3_gaps deduplicated; blocking = capital_cost_cas_breakdown (no contemporary plant study ingested) + inertia_laser_capital_cost (proprietary); important = chamber_capital_cost, OM_cost_estimates, capacity_factor, target_injection_cost, fuel_cost, first_wall_replacement_inertia, rep_rate_laser_om_inertia"
 section_coverage:
-  availability_of_data:       "Moderate-to-Good"
+  availability_of_data:       "Good"
   system_function:            "Good"
   subsystem_maturity:         "Partial"
   materials_supply_chain:     "Partial"
   lcoe_parameter_extraction:  "Partial"
-```
+```
\ No newline at end of file
```

## Acceptance notes (fill during Phase 3)

- Deviation class (1-6 per plan.md): 
- Justified by fleet source? 
- Notes: 
