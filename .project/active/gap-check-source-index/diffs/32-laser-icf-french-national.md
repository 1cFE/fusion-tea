# Diff: 32-laser-icf-french-national

**Generated:** 2026-05-22T11:21:44-07:00

## Counts

| field | baseline | new | Δ |
|-------|----------|-----|---|
| blocking_count   | 6 | 6 | 0 |
| important_count  | 5 | 9 | - |
| overall_rating   | Significant Gaps | Significant Gaps | - |

## Fleet-source citations (new only — grep `knowledge/sources/` or `PyFECONS`)

```
151:1. **Xcimer Energy whitepaper** (`knowledge/sources/commercialization_of_laser_fusion_energy/`) — contains the most detailed laser cost breakdown available: KrF at <$100/J vs. DPSSL baseline at $700–1000/J. Open and read this source to bound the laser capital cost for the quantitative model. `confirmed in SOURCE_INDEX`
153:2. **Hawker simplified IFE economic model** (`knowledge/sources/a_simplified_economic_model_for_inertial_fusion/`) — 14-parameter Monte Carlo LCOE model for technology-agnostic IFE. Directly applicable as the parametric framework for this concept. Gives LCOE sensitivity to gain, driver efficiency, rep rate, and target cost. `confirmed in SOURCE_INDEX`
161:6. **Energy from Inertial Fusion** (`knowledge/sources/energy_from_inertial_fusion/`) — 1992 IAEA textbook (Hogan et al., cited as Ref. 53 throughout Ribeyre — the primary reference for the reactor model). Contains IFE plant cost modeling frameworks from the 1990s. `confirmed in SOURCE_INDEX`. Likely contains capital cost estimates for direct-drive IFE reactors.
```

## Blocking-tier lines (baseline)

```
31:- Published plant study — `truly-unknown` — **blocking**: none exists yet; GenF is in Phase 1 simulation
105:- First wall material — `not-yet-sourced` (IFSA25 paper #6) / `proprietary` — **blocking**: determines replacement schedule and O&M cost; can use analogue materials (tungsten, SiC composites) from broader IFE/ITER literature
134:| Laser capital cost ($/kJ or total system) | not-yet-sourced | blocking | Dominant capital cost driver; use European IFE roadmap (HiPER) or NIF analogue scaled to 10 Hz DPSSL; DPSSL cost projections exist in EUROfusion IFE literature |
135:| Number of beamlines and energy per beamline | not-yet-sourced | blocking | Determines laser system scale; European IFE consensus ~10 kJ/beamline but not confirmed for GenF |
136:| Laser wall-plug efficiency | not-yet-sourced | blocking | DPSSL ~10–20% wall-plug efficiency; critical for recirculating power fraction |
138:| First wall replacement schedule | not-yet-sourced/proprietary | blocking | Driven by neutron fluence; no first wall material yet chosen; use ITER/IFE analogue |
139:| Target fabrication cost per shot | truly-unknown | blocking | No public estimate exists for any IFE concept at 10 Hz commercial scale; must estimate from NIF target cost + learning curve |
144:| Net electrical output (after recirculating power) | derivable | blocking | Depends heavily on laser wall-plug efficiency and gain; at gain=100, laser WPE=15%, recirculating fraction ~67% — net output severely constrained |
```

## Blocking-tier lines (new)

```
36:- No plant-level cost study exists — `proprietary` (too early in development even for internal use) — **blocking** for quantitative LCOE
61:- Final optics survivability lifetime not established — `truly-unknown` — **blocking** for capacity factor estimation
83:- TBR>1 not demonstrated anywhere; required before commercial viability — `truly-unknown` — **blocking** for concept viability (but for TEA analysis purposes, can be treated as a required assumption)
135:| Capital cost — laser system (total, per GWe) | `not-yet-sourced` | blocking | Xcimer cites $100/J for KrF, $700–1000/J for DPSSL baseline; LIFE studies provide DPSSL analog |
136:| Capital cost — reaction chamber | `not-yet-sourced` | blocking | ARIES IFE / Sirius-P studies may have analog; no GenF-specific data |
137:| Capital cost — target factory | `not-yet-sourced` | blocking | No published estimate for >10 Hz cryogenic target factory |
139:| Operating cost — target manufacturing ($/shot) | `truly-unknown` | blocking | No published cost for cryogenic DT targets at production scale |
140:| Operating cost — first wall/final optics replacement | `truly-unknown` | blocking | Replacement schedule/cost not established (material unresolved) |
142:| Capacity factor | `not-yet-sourced` | blocking | No maintenance model; only "10 Hz" rep rate given; no planned outage analysis |
145:| LCOE from plant study | `proprietary` | blocking | GenF has not published any economic analysis; internal to Phase 1 modeling |
```

## Full unified diff (truncated to 400 lines)

```diff
--- /tmp/gap_baselines_2026-05-22/32-laser-icf-french-national.md	2026-05-22 09:21:13.882832735 -0700
+++ /home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/32-laser-icf-french-national/gap_report.md	2026-05-22 11:21:44.399198857 -0700
@@ -1,60 +1,65 @@
-# Gap Assessment: Laser ICF - French National Direct Drive (D-T)
+I now have all the information needed to write the gap assessment. Let me compile the report.
+
+---
+
+# Gap Assessment: Laser ICF - French National (D-T)
 
 ## Overall Readiness
 **Rating**: Significant Gaps
 
-**Summary**: GenF Systems is an extremely early-stage company (founded January 2025, currently in Phase 1 modeling and simulation through 2027). Public information is limited to commercial website messaging, project funding announcements, and one paywalled peer-reviewed paper. Enough is available for a credible qualitative narrative and a rough-order-of-magnitude LCOE skeleton, but nearly all quantitative parameters require analogues borrowed from the broader European IFE literature rather than GenF-specific data. No plant study exists.
+**Summary**: The technical physics characterization of the GenF/TARANIS concept is surprisingly strong for a company founded in early 2025 — the Ribeyre et al. (2025) AIP paper (co-authored by GenF and CEA) provides a complete reactor system model with quantified performance parameters (driver efficiency, thermal efficiency, blanket gain, target gain, rep rate, chamber radius). However, the economics side is essentially empty: no capital cost estimates, no CAS breakdown, no operating cost data, and no LCOE analysis exists in any concept-specific source. The physics parameters are sufficient to parameterize an LCOE model, but all cost coefficients must be borrowed from IFE analogues (LIFE, Xcimer, Hawker's simplified model) — none of which are direct matches for DPSSL-driven direct-drive IFE at this scale.
 
 ---
 
 ## Section Coverage
 
 ### 1. Availability of Data
-**Coverage**: Limited
+**Coverage**: Partial
 
 **Available**:
-- GenF website pages (`genf-website-technology.md`, `genf-icf-article.md`): commercial-level description of concept, 10 Hz rep rate, 1 GW target, DT fuel, lithium blanket, direct drive rationale
-- TARANIS project details (`taranis-project-details.md`): funding by phase (€12–18.5M Phase 1, €200M Phase 2, €600M Phase 3), roadmap to 2050, partner roster (Thales, CEA, CNRS LULI/CELIA, Assystem, École Polytechnique)
-- Ribeyre et al. AIP Advances (2025) (`aip-advances-ribeyre-2025.md`): confirms liquid lithium blanket, tritium breeding reactions, co-authored by GenF/CEA researchers — **paywalled; only abstract-level details captured**
-- IFSA25 conference (Sept 2025): GenF presented 7 papers including implosion design, reactor system modeling, foam targets, first wall challenges — **titles captured but no paper content**
-- No published plant study. No system code outputs (though IFSA25 paper #7, "Inertial fusion reactor system modeling: precursor to a digital twin," suggests one is in progress)
+- Ribeyre et al. (2025) AIP Advances 15, 095013 — a 9-page peer-reviewed reactor system paper by GenF/CEA authors, fully extracted. Provides reactor model, performance parameter equations, hydro-scaled target gain curves, energy split fractions, chamber radius estimates, tritium consumption rates, and a qualitative cost discussion.
+- GenF website content — high-level ICF overview, reactor diagram, commercial target (1 GWe, 2050), rep rate (10 Hz), Thales partnership, fuel cycle description.
+- CNRS TARANIS announcement — three-phase roadmap (Phase 1: 2024–2027/28 modeling/digital twin; Phase 2: 2028–2035 technology validation; Phase 3: 2035+ demonstrator; first MWe ~2040; commercial ~2050).
+- ARPA-E Zuegel DPSSL presentation — top-level IFE DPSSL requirements (≥10% wall-plug efficiency, MJ-class, 1–10 Hz, $0.01/W diode cost target), current DPSSL demonstrations (LUCIA 14J/2Hz, Mercury, HALNA, DiPOLE-100X), TRL analysis.
+- Scott et al. (2021) PRL — shock ignition LPI physics at ignition scale. Documents hot-electron coupling (1–2.5% energy, 35–45 keV temperature) and encouraging result that fuel preheat should not impede shock ignition at MJ scale.
+- Li-6/Li-7 supply chain articles (NEI Magazine, Power Technology) — quantified global Li-6 supply constraints, CANDU tritium production (<2 kg/yr), ITER Li demand (~200 kg enriched Li for test blanket module), DEMO demand (>60 t/GW).
 
 **Missing**:
-- Full text of Ribeyre et al. AIP Advances 2025
-- IFSA25 conference paper content (7 papers)
-- Any GenF/CEA system code results or plant design reports
-- Details from LMJ experimental campaigns (classified or unpublished)
+- No published plant study or system code output for GenF/TARANIS.
+- No LCOE analysis from any GenF-affiliated source.
+- No CAS-level cost breakdown.
+- First wall material selection result (IFSA25 presentation by Ialovega referenced but not extracted).
+- Phase 2/3 technical specifications (conceptual design expected post-2027).
+- Full Ribeyre AIP paper is now available (CC BY license), so no paywall barrier.
 
 **Gaps**:
-- Full Ribeyre et al. paper text — `not-yet-sourced` — **important**: this is the most authoritative technical document; paywall is the only barrier
-- IFSA25 conference proceedings — `not-yet-sourced` — **blocking for quantitative work**: the reactor system modeling and implosion design papers likely contain the most relevant technical parameters
-- Published plant study — `truly-unknown` — **blocking**: none exists yet; GenF is in Phase 1 simulation
+- No plant-level cost study exists — `proprietary` (too early in development even for internal use) — **blocking** for quantitative LCOE
+- IFSA25 first-wall materials presentation not extracted — `not-yet-sourced` — **important**
+- Phase 2 engineering specifications not public — `proprietary` (not yet developed) — **important**
 
 ---
 
 ### 2. Challenges in Capturing System Function
-**Coverage**: Partial
+**Coverage**: Good (for physics challenges); Poor (for cost propagation from physics uncertainties)
 
 **Available**:
-- Direct-drive selection rationale: 4–5x better laser coupling efficiency vs. indirect drive; no hohlraum (removes X-ray conversion losses)
-- Key physics challenges named: laser-plasma instabilities (LPI), hydrodynamic instabilities; these are the canonical IFE challenges and are well-documented in public literature
-- IFSA25 title #1 ("Implosion and illumination design for laser driven fusion energy") confirms active implosion optimization work
-- Target: ~2mm capsule, up to 30% burn fraction, gain >100, up to 100+ MJ per implosion
-- First wall challenge acknowledged: dedicated IFSA25 paper (#6 by Ialovega) — no content available
-- Reactor system modeling: IFSA25 paper #7 ("precursor to a digital twin") by Chesneau — existence known, content not available
+- Ribeyre et al. explains the key functional challenges comprehensively: (1) insufficient fusion gain at NIF efficiency requiring DPSSL η_d ≈ 10%; (2) rep-rate operation at 10 Hz requiring active cooling of laser amplifiers; (3) heat extraction and tritium breeding.
+- The paper shows target gain sensitivity: at 10 Hz, 3 MJ, G ≈ 120 for the shock-augmented ignition scheme. This sensitivity analysis (G vs. E_d, η_d, rr) is the quantitative core of the physics case.
+- Identifies key open questions: ignition scheme choice (standard vs. shock vs. shock-augmented) remains unresolved; laser wavelength (3ω vs. 2ω) choice is open; LPI mitigation at high intensity is an active research area.
+- Scott et al. (2021) documents that shock ignition LPI at ignition scale produces manageable hot-electron coupling (~2.5%), giving qualified optimism but acknowledging the physics is not closed.
+- The CNRS document confirms CELIA contributes "patented innovations" for high-rep-rate laser cooling — implies 10 Hz operation is a solved problem at sub-MJ scale, not at MJ-class scale.
+- Ribeyre explicitly notes cryogenic target injection challenges: 40–160 m/s in-flight velocity, 100–1000g acceleration tolerance, survival in hot chamber environment — no solution presented.
 
 **Missing**:
-- Quantified gain curve (Qfusion vs. laser energy input)
-- Laser-to-target coupling efficiency for their specific illumination scheme
-- Specific LPI mitigation approach (beam smoothing, wavelength, pulse shaping)
-- Neutron flux to first wall (determines materials damage rate)
-- Chamber clearing time between shots (determines achievable rep rate and availability)
+- How LPI uncertainties propagate into cost uncertainty — no sensitivity analysis linking physics variance to economic variance.
+- Final optics survivability at 10 Hz under neutron/x-ray/ion bombardment (referenced as open problem in Ribeyre, no resolution in any extracted source).
+- Target tracking and pointing system architecture.
+- Vacuum pumping and tritium isotope separation system design (described schematically in Ribeyre Fig. 1 but no engineering detail).
 
 **Gaps**:
-- Gain curve / ignition threshold — `proprietary` (in Phase 1 simulation, not published) — **important**: can substitute with CELIA/LULI or ELI Beamlines analogue literature
-- First wall neutron fluence model — `not-yet-sourced` (IFSA25 paper #6) — **important**: determines first wall replacement schedule, which drives O&M cost
-- Illumination geometry details — `not-yet-sourced` (IFSA25 paper #1) — **important**: determines number of beamlines and laser architecture scale
-- Chamber clearing physics — `truly-unknown` at this stage — **nice-to-have**
+- LPI uncertainty→cost propagation chain not addressable from current sources — `truly-unknown` (active research area, no published connection) — **important**
+- Final optics survivability lifetime not established — `truly-unknown` — **blocking** for capacity factor estimation
+- Cryogenic target injection at 10 Hz undemonstrated and unresolved — `truly-unknown` — **important**
 
 ---
 
@@ -62,126 +67,122 @@
 **Coverage**: Partial
 
 **Available**:
-- Overall program TRL: early — Phase 1 is modeling/simulation only (2024–2027); no integrated system demo
-- Laser driver: Thales is a leading DPSSL manufacturer; CELIA has patented active cooling for 10 Hz operation — TRL ~3–4 for high-rep-rate IFE-class DPSSL
-- ELI Beamlines experimental campaign (Aug 2025, 550 shots with L4n ns-kJ Nd:glass laser): calibration experiments — TRL ~3 for implosion physics validation
-- Cryogenic target production: named as Phase 2 (2027–2035) development milestone — TRL ~2–3
-- First wall: active CEA/GenF research (IFSA25 paper) — TRL ~1–2
-- Tritium breeding blanket: liquid Li mentioned; Phase 2 development — TRL ~2–3
-- Target injection at 10 Hz: named Phase 2 challenge — TRL ~1–2
+- **Driver (DPSSL)**: Zuegel presentation gives TRL assessments (slide image only — values not extractable). Confirmed demonstrations: LUCIA (14 J/2 Hz, η=13%), Mercury (160 J, η=13%), HALNA (η=11.7%), DiPOLE-100X (100 J/10 Hz). Target for IFE: ≥10% efficiency. Ribeyre uses η_d = 10% as "realistic industrial projection." GenF used ELI Beamlines L4n ns-kJ (Nd:glass) laser for 550-shot experimental campaign — this is a flash-lamp system, not DPSSL; it is a physics probe, not representative of the commercial driver.
+- **Target fabrication**: Not addressed in any extracted source beyond noting 86,400 targets/day would be needed. Ribeyre cites this as a challenge with no resolution.
+- **Chamber/first wall**: Ribeyre mentions tungsten shows significant lifetime reduction from thermal load; Ialovega et al. (referenced in Ribeyre, paper cited as Ref. 69 on tantalum coatings) presents cold-spray tantalum as a candidate. No validated solution.
+- **Blanket**: Ribeyre confirms liquid lithium blanket with G_b ≈ 1.2 standard value. Notes highest achieved TBR is 3.57×10⁻⁴ — five orders of magnitude below what's needed.
+- **Power conversion**: Ribeyre implicitly assumes Rankine cycle; cites η_th = 40–55% range from prior LIFE and Sirius-P reactor studies. No GenF-specific cycle design.
 
 **Missing**:
-- Explicit TRL ratings from GenF or program assessments
-- Laser energy per beamline and number of beamlines for commercial system
-- Specific DPSSL architecture for the commercial reactor
-- Status of foam target fabrication (IFSA25 paper #3 on 2-photon polymerization — promising but content unavailable)
-- Cryogenic target production rate requirements and current demonstrated throughput
+- DPSSL TRL numbers from the Zuegel slide (image, not readable from text extraction).
+- Any detail on cryogenic target fabrication industrialization.
+- Any detail on target injection system.
 
 **Gaps**:
-- Subsystem TRL table — `derivable` from European IFE roadmap literature (Euro Fusion IFE roadmap, HIPER study) combined with GenF-specific status — **important**: needed for qualitative write-up
-- Laser beamline count and energy per beamline — `not-yet-sourced` (IFSA25 papers or European IFE roadmap) — **important**: dominant capital cost driver
-- Foam target fabrication scalability — `not-yet-sourced` (IFSA25 paper #3) — **nice-to-have**
-- 10 Hz target injection TRL — `truly-unknown` at this stage — **important** for capacity factor
+- MJ-class DPSSL at 10 Hz does not exist; ~50x scaling from current state-of-art required — TRL ≈ 3–4 — `truly-unknown` (timeline/cost of the scaling unclear) — **important**
+- TBR>1 not demonstrated anywhere; required before commercial viability — `truly-unknown` — **blocking** for concept viability (but for TEA analysis purposes, can be treated as a required assumption)
+- Cryogenic target factory at 10 Hz / 86,400 targets/day — TRL ≈ 2 — `truly-unknown` — **important**
 
 ---
 
 ### 4. Key Materials and Supply Chain Considerations
-**Coverage**: Poor
+**Coverage**: Good (for tritium and Li-6); Poor (for laser materials and target capsule supply chain)
 
 **Available**:
-- Fuel: D-T confirmed; tritium breeding via lithium blanket is the supply strategy
-- Blanket material: "lithium-based compound" (website) / "liquid lithium" (Ribeyre et al.) — specific alloy/compound not confirmed
-- Target: ~2mm spherical DT capsule with foam structure (IFSA25 paper #3 on 2-photon polymerization foam targets suggests polymer foam shell)
-- No critical materials beyond DT fuel cycle are discussed in available sources
+- **Tritium**: Global inventory ~30 kg (2020–2035). CANDU produces <2 kg/yr. A 10 Hz IFE reactor consumes >1 kg/day (360 kg/year). The gap is ~180× current production rate. Ribeyre confirms TBR>1 is mandatory and currently unachieved (best TBR = 3.57×10⁻⁴). UK UKAEA has initiated a multi-million-pound tritium breeding project (2025).
+- **Li-6**: Required for tritium breeding (n + ⁶Li → T + ⁴He; exothermic, gives G_b boost to 1.2). Only Russia and China actively produce Li-6/Li-7 commercially and supply is not available to Western programs. ITER test blanket: ~200 kg needed. DEMO: >60 t/GW. Fusion pilot plants: tens of tonnes; commercial: hundreds of tonnes per reactor-year. Hexium (US AVLIS startup) and UKAEA have initiatives but at early stage. NEI Magazine and Power Technology articles document this in detail.
+- **Laser gain media**: Yb:YAG or Nd:phosphate glass (both cited in Zuegel) — these materials exist at commercial scale but mass production for thousands of IFE beamlines is unestablished.
+- **Pump diodes**: Zuegel identifies $0.01/W as the target cost for economically competitive IFE diode pumps; current cost is significantly higher. Mass production is the key bottleneck.
 
 **Missing**:
-- Li-6 enrichment requirement and supply chain assessment
-- First wall material specification (active research, not resolved)
-- DPSSL gain medium material (Yb:YAG or similar) at scale for commercial rep rate
-- Tritium inventory requirements and self-sufficiency timeline
-- Target factory cost and throughput requirements (10 Hz → 864,000 targets/day)
+- DT capsule manufacturing supply chain (target shell fabrication, surface smoothness tolerances). No source addresses this for GenF.
+- Final optics material supply (large-aperture fused silica, KDP crystals) at IFE scale.
+- Laser diode cost and supply chain scaling from current DPSSL production to IFE fleet requirements.
 
 **Gaps**:
-- First wall material — `not-yet-sourced` (IFSA25 paper #6) / `proprietary` — **blocking**: determines replacement schedule and O&M cost; can use analogue materials (tungsten, SiC composites) from broader IFE/ITER literature
-- Li-6 enrichment supply chain — `not-yet-sourced` — **important**: standard concern for all D-T concepts; search ORNL/EUROfusion blanket literature
-- Target fabrication at 10 Hz scale — `truly-unknown` for this concept; IFE community broadly acknowledges this as unsolved — **blocking for operating cost**: 10 targets/second is an undemonstrated manufacturing challenge
-- DPSSL gain medium supply chain — `not-yet-sourced` — **nice-to-have**: can use Thales analogues or European laser industry assessments
+- Li-6 enrichment supply chain gap is a hard constraint for all D-T fusion in Western countries — `not-yet-sourced` (policy/supply chain papers exist; ITER TRANSAT report cited in sources) — **important**
+- Pump diode cost path from current to $0.01/W — `not-yet-sourced` — **important**
+- Cryogenic target capsule manufacturing supply chain — `truly-unknown` (no published analysis at IFE production rates) — **important**
 
 ---
 
 ### 5. LCOE Parameter Extraction
-**Coverage**: Poor (skeletal only)
+**Coverage**: Poor
+
+**Available Parameters** (from Ribeyre et al. and GenF sources):
 
-**Available Parameters**:
 | Parameter | Value/Range | Source | Confidence |
 |-----------|-------------|--------|------------|
-| Plant electrical output | 1000 MW | GenF technology page | high |
-| Repetition rate | 10 Hz | GenF technology page | high |
-| Fuel per shot | ~1 mg DT | GenF ICF page | high |
-| Target diameter | ~2 mm | GenF ICF page, TARANIS details | high |
-| Target gain (claimed) | >100 | TARANIS details / GenF ICF page | medium |
-| Fusion energy per shot (claimed) | up to 100+ MJ | GenF ICF page | medium |
-| Fuel burn fraction | up to 30% | GenF ICF page | medium |
-| Program Phase 1 cost | €12–18.5M | TARANIS details | high |
-| Program Phase 2 cost | ~€200M | TARANIS details | medium |
-| Program Phase 3 cost | ~€600M | TARANIS details | medium |
-| Commercial target date | 2050 | GenF technology page | high |
-| Blanket concept | Liquid Li | Ribeyre et al. 2025 | medium |
+| Plant electrical output | 1 GWe (target) | GenF website | m |
+| Repetition rate | 10 Hz | GenF website, Ribeyre | h |
+| Laser energy per shot | ~3 MJ (baseline) | Ribeyre Fig. 3 | m |
+| Driver efficiency (η_d) | 10% (DPSSL projection) | Ribeyre Sec. III | m |
+| Thermal-to-electric efficiency (η_th) | 40–55%; 40% used in model | Ribeyre Sec. III, LIFE refs | m |
+| Target gain (G) | ~120 at E_d = 3 MJ, 10 Hz | Ribeyre Fig. 3b | m |
+| Blanket gain (G_b) | 1.2 (Li-6 standard value) | Ribeyre Sec. III | m |
+| Auxiliary power fraction | 5% of grid output | Ribeyre Eq. (1) | m |
+| DT per target | ~4 mg (at 25% burn fraction) | Ribeyre Sec. III | m |
+| Chamber radius | ~8 m | Ribeyre Sec. III | m |
+| Fusion energy per shot | ~360 MJ (at G=120, E_d=3 MJ) | Ribeyre | m |
+| Energy split (neutrons/x-rays/ions) | 75%/6%/19% (Sirius); 71%/1-2%/27% (HiPER) | Ribeyre Sec. III | m |
+| Tritium burn fraction | 25–30% | Ribeyre | m |
+| Target DT mass | ~1 mg fuel / ~2 mm diameter | GenF website, Ribeyre | h |
 
 **Missing Parameters**:
+
 | Parameter | Gap Type | Criticality | Notes |
 |-----------|----------|-------------|-------|
-| Laser capital cost ($/kJ or total system) | not-yet-sourced | blocking | Dominant capital cost driver; use European IFE roadmap (HiPER) or NIF analogue scaled to 10 Hz DPSSL; DPSSL cost projections exist in EUROfusion IFE literature |
-| Number of beamlines and energy per beamline | not-yet-sourced | blocking | Determines laser system scale; European IFE consensus ~10 kJ/beamline but not confirmed for GenF |
-| Laser wall-plug efficiency | not-yet-sourced | blocking | DPSSL ~10–20% wall-plug efficiency; critical for recirculating power fraction |
-| Thermal/electrical conversion efficiency | derivable | important | "Traditional power plant methods" suggests steam Rankine ~33–38%; sCO2 Brayton ~45% possible but unconfirmed |
-| First wall replacement schedule | not-yet-sourced/proprietary | blocking | Driven by neutron fluence; no first wall material yet chosen; use ITER/IFE analogue |
-| Target fabrication cost per shot | truly-unknown | blocking | No public estimate exists for any IFE concept at 10 Hz commercial scale; must estimate from NIF target cost + learning curve |
-| O&M cost rate | truly-unknown | important | No plant study; must derive from nuclear plant analogues |
-| Capacity factor / availability | derivable | important | 10 Hz op mode assumed continuous; maintenance-limited availability unknown; can estimate from analogue nuclear plants |
-| Tritium breeding ratio (TBR) and inventory | not-yet-sourced | important | Liquid Li TBR ~1.3–1.5 (from open literature); GenF-specific not published |
-| Balance of plant cost | derivable | important | Can use conventional nuclear BOP analogues scaled to 1 GW |
-| Net electrical output (after recirculating power) | derivable | blocking | Depends heavily on laser wall-plug efficiency and gain; at gain=100, laser WPE=15%, recirculating fraction ~67% — net output severely constrained |
+| Capital cost — laser system (total, per GWe) | `not-yet-sourced` | blocking | Xcimer cites $100/J for KrF, $700–1000/J for DPSSL baseline; LIFE studies provide DPSSL analog |
+| Capital cost — reaction chamber | `not-yet-sourced` | blocking | ARIES IFE / Sirius-P studies may have analog; no GenF-specific data |
+| Capital cost — target factory | `not-yet-sourced` | blocking | No published estimate for >10 Hz cryogenic target factory |
+| Capital cost — balance of plant | `derivable` | important | Standard steam Rankine BOP costs applicable from fission analogs |
+| Operating cost — target manufacturing ($/shot) | `truly-unknown` | blocking | No published cost for cryogenic DT targets at production scale |
+| Operating cost — first wall/final optics replacement | `truly-unknown` | blocking | Replacement schedule/cost not established (material unresolved) |
+| Operating cost — O&M labor | `derivable` | important | Can use IFE plant-level analog from LIFE or Sirius studies |
+| Capacity factor | `not-yet-sourced` | blocking | No maintenance model; only "10 Hz" rep rate given; no planned outage analysis |
+| Laser availability / MTTF (gigashots requirement) | `truly-unknown` | important | Zuegel notes gigashot lifetime requirement but no demonstrated value |
+| Capital cost — tritium processing system | `not-yet-sourced` | important | Vacuum pumps, isotope separation, closed fuel cycle (shown schematically in Ribeyre) |
+| LCOE from plant study | `proprietary` | blocking | GenF has not published any economic analysis; internal to Phase 1 modeling |
 
 ---
 
 ## Source Recommendations
 
-1. **Ribeyre et al. AIP Advances 2025 (full text)** — `not-yet-sourced` — obtain via institutional access or interlibrary loan; this is the highest-priority source; expected to contain reactor system parameters, gain curves, and blanket design specifics
+1. **Xcimer Energy whitepaper** (`knowledge/sources/commercialization_of_laser_fusion_energy/`) — contains the most detailed laser cost breakdown available: KrF at <$100/J vs. DPSSL baseline at $700–1000/J. Open and read this source to bound the laser capital cost for the quantitative model. `confirmed in SOURCE_INDEX`
 
-2. **IFSA25 conference proceedings** — `not-yet-sourced` — search IAEA INIS database, ResearchGate, or author pages for any of the 7 GenF/CEA papers; Hugo Chesneau's reactor system modeling paper (#7) and Barlow's implosion design paper (#1) are highest priority; `unverified — confirm proceedings publication before searching`
+2. **Hawker simplified IFE economic model** (`knowledge/sources/a_simplified_economic_model_for_inertial_fusion/`) — 14-parameter Monte Carlo LCOE model for technology-agnostic IFE. Directly applicable as the parametric framework for this concept. Gives LCOE sensitivity to gain, driver efficiency, rep rate, and target cost. `confirmed in SOURCE_INDEX`
 
-3. **HiPER project reports and European IFE roadmap** — `not-yet-sourced` — these define the European consensus on DPSSL driver costs, target specifications, and plant design for laser direct-drive IFE; directly applicable as a technology-class analogue; search OSTI or EUROfusion publications portal
+3. **OSTI / LLNL LIFE reactor studies** — Meier et al. (2014) "Fusion technology aspects of laser inertial fusion energy (LIFE)" and related Dunne et al. 2021 encyclopedia article (both cited in Ribeyre Refs. 63–64). These are DPSSL-driven IFE cost analogs. **Search OSTI for these citations** — `unverified — confirm existence before searching`; Ribeyre cites them as Refs. 63 and 64.
 
-4. **IAEA FEC (Fusion Energy Conference) and NRL/CELIA high-rep-rate laser publications** — `not-yet-sourced` — for laser wall-plug efficiency, beamline architecture, and 10 Hz driver scaling; search IAEA INIS for "DPSSL IFE driver" or "high average power laser fusion"
+4. **Sirius / Sirius-P reactor design reports** (Badger et al. 1984, UMFDM-568; Sviatoslavsky et al. 1993, UMFDM-950) — direct-drive laser IFE reactor cost studies from University of Wisconsin Fusion Technology Institute. Cited in Ribeyre. CAS-level cost breakdowns likely available. **Search OSTI for UMFDM-568 and UMFDM-950** — `unverified — confirm existence before searching`
 
-5. **EUROfusion IFE conceptual design / LIFE plant study analogues** — `not-yet-sourced` — LLNL's LIFE concept (now discontinued) produced detailed plant cost breakdowns for laser IFE at 10 Hz that remain the most detailed public analogues; search OSTI for "LIFE laser IFE" or "Moses LIFE" papers; `unverified — confirm OSTI availability`
+5. **HiPER European IFE project** — European direct-drive IFE design study, referenced throughout Ribeyre. French/European institutional context makes this the most directly analogous to GenF's approach. Search for "HiPER conceptual design report" or HiPER fusion engineering design. `unverified — confirm existence before searching`
 
-6. **CNRS CELIA publications on high-rep-rate laser active cooling** — `not-yet-sourced` — CELIA holds patents on active cooling enabling 10 Hz DPSSL operation; their publications would clarify driver architecture; search Google Scholar for CELIA CNRS fusion laser; `unverified — confirm relevance`
-
-7. **NIF/OMEGA target fabrication cost estimates** — `not-yet-sourced` — NIF program published some target cost data; useful for bounding the target fabrication O&M term; search OSTI for "ICF target cost fabrication"
+6. **Energy from Inertial Fusion** (`knowledge/sources/energy_from_inertial_fusion/`) — 1992 IAEA textbook (Hogan et al., cited as Ref. 53 throughout Ribeyre — the primary reference for the reactor model). Contains IFE plant cost modeling frameworks from the 1990s. `confirmed in SOURCE_INDEX`. Likely contains capital cost estimates for direct-drive IFE reactors.
 
 ---
 
 ## Summary
 
-**Proceed to analysis, with important caveats.** The available data is sufficient to write a credible qualitative narrative for Sections 1–3, drawing heavily on what is known about laser IFE as a technology class, with GenF-specific framing around their direct-drive choice, TARANIS partnership structure, and development roadmap. The narrative should be explicit that this is an extremely early-stage concept (Phase 1, no experimental ignition results, no plant study) and that most performance claims are simulation-based targets.
+**Proceed to analysis with supplementation from fleet-wide IFE cost sources.** The physics characterization is unusually strong for a company this young — the Ribeyre AIP paper provides a complete, self-consistent reactor system model with all key performance parameters (η_d, η_th, G_b, G, rr, E_d) needed to parameterize an LCOE model. However, concept-specific cost data is essentially absent: GenF is in Phase 1, no plant study exists, and no CAS breakdown or LCOE estimate has been published by any member of the TARANIS consortium.
+
+A D1+ qualitative and quantitative analysis is feasible if fleet-wide IFE cost analogs are incorporated — particularly the Hawker simplified IFE model, the Xcimer laser cost data, and the Ribeyre-cited LIFE/Sirius reactor studies. The quantitative LCOE model will be heavily analogue-based on the cost side and should be explicitly caveated as such. The qualitative analysis can be strong on physics challenges, maturity, and supply chain based on existing sources.
 
-For the quantitative LCOE model, a meaningful skeleton can be constructed using the confirmed parameters (1 GW plant, 10 Hz, gain >100 claimed) combined with European IFE analogue parameters for laser capital cost, DPSSL efficiency, and target fabrication. The **recirculating power fraction** will be the most important sensitivity: at gain=100 and ~15% laser wall-plug efficiency, recirculating power could consume ~60–70% of gross output, making net LCOE extremely sensitive to actual laser efficiency. This is a known binding constraint for laser IFE and should be the centerpiece of the back-solve analysis.
+The most critical conceptual insight for any analysis: GenF's Phase 1 target (2027/2028) is to define the reactor operating point via digital twin — meaning the concept is still pre-design. The Ribeyre paper's operating point (3 MJ DPSSL @ 10 Hz → 1 GWe) is the current best estimate, but all subsystem designs remain open questions.
 
-**Before finalizing the analysis**, acquiring the Ribeyre et al. full text and any available IFSA25 proceedings would substantially improve confidence on blanket design, implosion gain curve, and reactor system integration parameters. These are the highest-leverage source gaps.
+---
 
 ## Structured summary (machine-readable)
 
 ```yaml
 overall_rating: "Significant Gaps"
 blocking_count: 6
-important_count: 5
-counting_method: "section_5_missing_parameters"
+important_count: 9
+counting_method: "all_sections_deduplicated — blocking: (1) no capital cost data for any subsystem, (2) no operating cost data (target manufacturing, maintenance), (3) no capacity factor analysis, (4) TBR not demonstrated (requires assumption for model), (5) final optics survivability lifetime not established, (6) no LCOE from any GenF-affiliated source. Important: (1) ignition scheme choice unresolved, (2) first wall material unresolved, (3) DPSSL MJ-class 10 Hz scaling undemonstrated, (4) Li-6 supply chain gap, (5) cryogenic target factory supply chain unknown, (6) pump diode cost path unknown, (7) IFSA25 first-wall paper not extracted, (8) LPI uncertainty→cost propagation not addressed, (9) cryogenic target injection at 10 Hz unresolved"
 section_coverage:
-  availability_of_data:       "Limited"
+  availability_of_data:       "Partial"
   system_function:            "Partial"
   subsystem_maturity:         "Partial"
-  materials_supply_chain:     "Poor"
-  lcoe_parameter_extraction:  "Poor (skeletal only)"
-```
+  materials_supply_chain:     "Partial"
+  lcoe_parameter_extraction:  "Poor"
+```
\ No newline at end of file
```

## Acceptance notes (fill during Phase 3)

- Deviation class (1-6 per plan.md): 
- Justified by fleet source? 
- Notes: 
