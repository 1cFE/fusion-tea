# Phase 3 diff: 04-laser-icf

**Generated:** 2026-05-22T13:20:51-07:00

## Counts (Phase 2 -> Phase 3 strict-read regen)

| field | phase2 | phase3 | Δ |
|-------|--------|--------|---|
| blocking_count   | 7 | 3 | -4 |
| important_count  | 8 | 6 | - |
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
I now have all the information I need to write the gap assessment report.
```

## Blocking-tier lines (new)

```
53:- Combined two-laser scheme (kT-field + ps PW) never experimentally tested — truly-unknown — **blocking**
132:| Capital cost by subsystem (CAS 20–27: laser arrays, chamber/vessel, target handling, energy conversion, BOP) | truly-unknown | **blocking** | No plant study or published cost estimates for any HB11-specific subsystem; ARIES CAS framework (knowledge/sources/aries_cost_account_documentation/) provides category definitions from 1992 IFE designs but HB11-specific values must be estimated from scratch |
133:| Net fusion gain (G) demonstrated or reliably extrapolated from combined two-laser scheme | truly-unknown | **blocking** | Current experiments are single-laser; combined ns kT-field + ps PW scheme never tested; ~4 orders of magnitude from breakeven using best available single-laser experiments; any LCOE model must parameterize G explicitly |
134:| Commercial rep-rated laser system cost and architecture (30 kJ ps PW at 1 Hz) | truly-unknown | **blocking** | DPSSL at $700–1,000/J (Xcimer paper) provides upper-bound analog for HB11's CPA petawatt laser; HB11's eventual "arrays of commercial lasers" architecture targets lower cost but no commercial rep-rated PW laser at this scale exists; at DPSSL costs a 30 kJ system costs $21–30M per shot-energy-equivalent |
```

## Full unified diff (truncated to 400 lines)

```diff
--- /tmp/gap_phase2_state/04-laser-icf.md	2026-05-22 12:59:21.058220936 -0700
+++ /home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/04-laser-icf/gap_report.md	2026-05-22 13:20:51.788643176 -0700
@@ -1,36 +1,35 @@
-I have enough information to write the full gap assessment now.
+I now have all the information I need to write the gap assessment report.
 
 # Gap Assessment: Laser ICF (p-B11)
 
 ## Overall Readiness
 **Rating**: Significant Gaps
-**Summary**: HB11 Energy is 4 orders of magnitude from breakeven and has not yet published a plant study, CAS-level cost breakdown, or any peer-reviewed LCOE analysis. The one quantitative TEA source (McKenzie et al., J. Fusion Energy 2023) provides a useful power-balance framework with several key parameters but contains no subsystem cost estimates or capital cost structure. A qualitative analysis is feasible with honest uncertainty framing; a quantitative LCOE model is possible only in a parameterized "what would need to be true" mode using IFE analogs from the fleet-wide source pool, with wide confidence intervals throughout.
+**Summary**: HB11 Energy's concept has a clear theoretical basis and a useful high-level technoeconomic framework published in McKenzie et al. 2023 (Journal of Fusion Energy), but the concept is approximately four orders of magnitude from net energy gain in any published experiment, the combined two-laser scheme has never been tested together, and no CAS-level capital cost breakdown or plant study exists. Sections 1–4 (qualitative analysis) are feasible with available data and stated assumptions; a meaningful quantitative LCOE model requires parametric treatment of gain and several cost analogues borrowed from other IFE sources.
 
 ---
 
 ## Section Coverage
 
 ### 1. Availability of Data
-**Coverage**: Poor
+**Coverage**: Partial
 
 **Available**:
-- One semi-quantitative TEA review paper: McKenzie et al. (J. Fusion Energy, 2023) — power loop model, recirculating power fraction formula, economic targets, key parameter ranges (`iter-03/sources/link-10-1007-s10894-023-00349-9.md`)
-- Conceptual reactor patent US10410752B2 (2018): fuel geometry, two-laser architecture, 1 Hz rep rate, 1 GW target, early direct-conversion design (`iter-01/sources/hb11-patent-reactor-design.md`)
-- Peer-reviewed physics paper: Margarone et al. (Appl. Sci. 2022) — 10^10 α/sr Osaka LFEX demonstration (`iter-01/sources/hb11-osaka-experiment-2022.md`)
-- Company technology pages (2019–2025): high-level reactor concept, energy conversion pivot, laser architecture vision (`iter-01/sources/hb11-technology-page.md`, `iter-02/sources/hb11-technology-page-2025.md`, `iter-03/sources/hb11-our-technology.md`)
-- News and PR compilations: funding, milestones, TINEX membership, ELI ERIC partnership (`iter-02/sources/hb11-recent-developments-2024-2025.md`, multiple iter-03 sources)
+- Company website (HB11 Technology Page 2025, iter-02/sources/hb11-technology-page-2025.md) and 2018 patent (US10410752B2, iter-01/sources/hb11-patent-reactor-design.md) give reactor geometry, laser parameters, fuel dimensions, rep rate, and two energy conversion designs.
+- McKenzie et al. 2023 ("HB11—Understanding Hydrogen-Boron Fusion as a New Clean Energy Source," Journal of Fusion Energy 42:17; iter-03/sources/link-10-1007-s10894-023-00349-9.md) is the primary technoeconomic reference: laser efficiency target (20%), recirculating power fraction (f = 1/εηG), target gain requirement (100–300), conversion efficiency range (36–64%), diode cost/lifetime assumptions, 25-year plant lifetime, and LCOE market constraint ($35/MWh target).
+- Margarone et al. 2022 (Applied Sciences 12:1444; iter-01/sources/hb11-osaka-experiment-2022.md) documents best experimental result: ~10^10 α/sr at LFEX, 0.005% laser-to-alpha energy efficiency, ~4 orders of magnitude below breakeven.
+- News and media sources (iter-02, iter-03) document DOE INFUSE grant, TINEX membership (globenewswire, iter-03), Adelaide USPL partnership (A$8.2M), and 12 published experiments at three facilities.
+- Hawker 2020 (knowledge/sources/a_simplified_economic_model_for_inertial_fusion/) provides a technology-agnostic 14-parameter IFE LCOE model directly applicable to HB11: parameters G, yield/shot, driver efficiency η, conversion efficiency ε, rep rate, target cost, O&M, plant size, and discount rate all map to McKenzie 2023's framework. Hawker finds LCOE as low as $25/MWh with G > 500 and yield > 5 GJ/shot — providing quantitative benchmarks for how far HB11's targets are from competitive operation.
 
 **Missing**:
-- No plant study or system code output (HYLIFE-II, SOMBRERO, etc.)
-- No CAS-level capital cost breakdown
-- No published LCOE sensitivity analysis
-- Phys. Rev. Research 2025 paper on novel targets not extracted (`dossier.md` notes as "not extracted")
-- Mehlhorn (2024, Physics of Plasmas) — historical/personal perspective, not extracted
+- No published plant study or detailed engineering design report
+- Phys. Rev. Research 2025 paper (alpha particle production from novel targets) not extracted — dossier flags this as an important recent result
+- Mehlhorn 2024 (Physics of Plasmas 31(2), "From KMS Fusion to HB11 Energy, a personal 50-year IFE perspective") not extracted — likely contains technoeconomic context and historical cost perspectives
+- Total funding (~A$12.8M) is very small relative to the concept's required development; company is pre-revenue and non-transparent about internal R&D milestones
 
 **Gaps**:
-- No plant study of any form — `truly-unknown` — **blocking** (no cost structure baseline)
-- Company holds internal techno-economic model (`link-10-1007...` references it exists) but details are unpublished — `proprietary` — **blocking** for subsystem-level cost
-- Phys. Rev. Research (2025) content unavailable — `not-yet-sourced` — **important** (most recent experimental physics data)
+- Phys. Rev. Research 2025 and Mehlhorn 2024 not extracted — not-yet-sourced — important
+- No published plant study or detailed cost breakdown — proprietary — important
+- Company is opaque on internal target designs and experimental roadmap — proprietary — important
 
 ---
 
@@ -38,23 +37,22 @@
 **Coverage**: Partial
 
 **Available**:
-- Physics deficit quantified: 4 orders of magnitude from breakeven in terms of α-particle yield per kJ (`iter-03/sources/link-10-1007-s10894-023-00349-9.md`)
-- Required gain target stated: G = 100–300 at laser efficiency η = 20% for economic viability (`link-10-1007...`)
-- Power amplifier model described: f = 1/(εηG), with engineering breakeven at f = 1 and commercial target f ≤ 0.25 (`link-10-1007...`)
-- Known physics uncertainties catalogued: p-B11 cross-section at low energies poorly measured, avalanche mechanism debated, bremsstrahlung loss severity, degenerate plasma behavior (`link-10-1007...`)
-- Energy conversion pivot documented: patent (2018) described direct electrostatic conversion at −1.4 MV; 2025 website states conventional steam cycle — design not stabilized (`dossier.md`, `iter-02/sources/hb11-technology-page-2025.md`)
+- McKenzie 2023 explicitly describes three challenges for the LCOE model: (1) laser efficiency, (2) target gain, (3) target fabrication cost. It quantifies the recirculating power fraction (f = 1/εηG) and derives the ηG > 10 rule of thumb for viability, and ηG > 20 for 10% recirculating fraction.
+- McKenzie 2023 discusses competing energy conversion pathways: direct electrostatic (patent, TRL 1), direct conversion via photon intermediate (~45%), direct electrodynamic conversion (~50%), and MHD + Rankine hybrid (~64%). Current company website (2025) states "conventional steam cycle generator" — a significant pivot from the 2018 patent's direct electrostatic design.
+- The Osaka experiment confirms that the dominant physics challenge is proton-boron fusion yield enhancement: the conversion efficiency from laser energy to alpha-particle energy is 0.005%, requiring ~10^8 improvement to reach commercial targets.
+- McKenzie 2023 identifies the avalanche mechanism, bremsstrahlung reduction, degenerate plasma effects, non-equilibrium burn, and novel target geometry as the key physics levers — none of which have been experimentally validated for gain enhancement at the relevant scale.
+- The Xcimer paper (knowledge/sources/commercialization_of_laser_fusion_energy/) clarifies that the key IFE system challenge is laser efficiency × scientific gain > 10; Xcimer's KrF excimer laser targets <$100/J vs. DPSSL at $700–1,000/J — the latter being the current benchmark for HB11's CPA petawatt laser architecture.
 
 **Missing**:
-- No simulations or code outputs for hybrid burn target gain projections
-- No analysis of how "thousands of commercial lasers" at 1 Hz aggregate to 1 GW baseload
-- No chamber design or debris management analysis (TINEX addresses this generically for IFE)
-- No quantified driver efficiency roadmap (20% WP efficiency is a target, not demonstrated)
+- The combined two-laser scheme (ns kT-field laser + ps PW ignition laser acting simultaneously) has never been tested experimentally. All published experiments use one-laser configurations (either pitcher-catcher or in-target). This is the core HB11 concept and its physics is entirely unvalidated in the lab.
+- Energy conversion design is unsettled: the 2018 patent describes direct electrostatic at −1.4 MV, the 2020 public messaging described direct charged-particle collection, and the 2025 website now states conventional steam cycle. No rationale for the pivot is published, and the engineering trade-off is unresolved.
+- The avalanche mechanism that underpins many of HB11's optimistic gain projections remains contested in the literature (Belloni 2021, McKenzie 2023 acknowledge this debate).
+- p-B11 cross-section at sub-100 keV and >3 MeV — the energy ranges most relevant to HB11's laser-accelerated proton scheme — remains uncertain (Sikora and Weller 2016 revised cross-sections upward at >10 MeV; McKenzie 2023 explicitly flags this as a blocking research challenge).
 
 **Gaps**:
-- Fundamental fusion gain not yet demonstrated at any scale — `truly-unknown` — **blocking** (the entire LCOE depends on achievable G, which is undemonstrated and 4 orders of magnitude from needed range)
-- Energy conversion architecture not finalized — `proprietary` / `truly-unknown` — **blocking** (efficiency ε swings from ~40% steam to ~50–64% advanced; choice determines recirculating power fraction)
-- Avalanche mechanism magnitude is physically contested — `truly-unknown` — **important** (if avalanche is significant it enables lower gain requirements; if absent, gain requirements are much more severe)
-- Laser architecture at 1 Hz, 30 kJ, >10% WP efficiency is beyond current capability — `truly-unknown` — **blocking** (no laser system in existence meets all three requirements simultaneously)
+- Combined two-laser scheme (kT-field + ps PW) never experimentally tested — truly-unknown — **blocking**
+- Energy conversion design unsettled (direct vs. steam cycle, efficiency range 36–64%) — proprietary/uncertain — important
+- p-B11 cross-section at laser-relevant energies partially unknown — not-yet-sourced — important
 
 ---
 
@@ -62,26 +60,23 @@
 **Coverage**: Partial
 
 **Available**:
-- Fusion physics demonstrations: 12 experiments at LFEX (Osaka), TARANIS (Belfast), PALS (Prague) — all TRL 2–3 (`dossier.md`, `iter-01/sources/hb11-osaka-experiment-2022.md`)
-- Petawatt CPA laser technology: commercially available at single-shot scale (Nobel 2018), TRL 5–6 for the laser itself; not demonstrated at fusion-relevant rep rates or wall-plug efficiency
-- Capacitor-coil kT field generation: demonstrated in laboratory settings (`link-10-1007...`), TRL ~3–4
-- Boron-nitride targets: manufactured and tested, TRL 4–5 for current experimental targets
-- Novel target materials (borophene, "white graphene"): in early development, TRL 1–2 (`link-10-1007...`)
-- DOE INFUSE grant (LLE/Rochester collaboration) ongoing for H2-boron fuel target development
-- TINEX membership: participating in DOE-funded target injection/chamber engineering program (`iter-03/sources/globenewswire-news-release-2025-02-10-3023820-0-en-general.md`)
+- Petawatt CPA laser (ps): TRL ~6–7 at single-shot laboratory scale (Osaka LFEX, Belfast TARANIS, PALS Prague); not rep-rated. Adelaide USPL partnership (A$8.2M, 2025) targeting >10% wall-plug efficiency for commercial lasers — first Australian sovereign USPL manufacturing capability.
+- Nanosecond laser for kT magnetic field (Fujioka-type capacitor-coil target): TRL ~4 (demonstrated at Osaka, producing sub-kT fields; single-shot, consumable target). kT-scale fields reported at laser facilities.
+- p-B11 fuel target: TRL ~3 (BN targets used in experiments, but HB11's proprietary target designs — white graphene, borophene, modified BN with higher H content — are in early material research per McKenzie 2023).
+- Energy conversion system: TRL ~1–2 (two competing designs, neither demonstrated at any scale; direct electrostatic at −1.4 MV never built; steam cycle not designed for fusion-specific chamber environment).
+- Target injection and automated loading at 1 Hz: TRL ~1 (conceptual description in patent, no prototype demonstrated). TINEX collaboration (GA, SLAC, CSU, UCSD, LLNL — with HB11 as industry council member per globenewswire 2025) is developing target injection solutions for IFE broadly.
+- Balance of plant (steam cycle): TRL ~8–9 for generic steam cycle; TRL ~2–3 for fusion-specific chamber integration.
 
 **Missing**:
-- No TRL assessment document
-- No laser system rep-rate demonstration at fusion-relevant parameters
-- No chamber design for alpha particle collection/energy conversion
-- No target injection system at 1 Hz demonstrated
-- No first wall or chamber material study for alpha bombardment damage
+- No rep-rated demonstration of any laser + target combination at even 0.01 Hz
+- No prototype automated target loading system for the HB11 disposable capacitor-coil module
+- No chamber survivability data for repeated shots (target debris, shock loading of spherical vessel, optical window damage)
+- Wall-plug efficiency for the combined ns + ps laser system at commercial power levels not demonstrated
 
 **Gaps**:
-- No subsystem has been demonstrated at power-plant-relevant parameters — `truly-unknown` — **blocking** for TRL completeness
-- High-rep-rate DPSSL at >10% WP efficiency — `truly-unknown` — **important** (Adelaide A$8.2M grant is working on this but results unpublished)
-- Alpha energy collection system (DEC or MHD or steam) — `truly-unknown` at engineering level — **important**
-- Target fabrication at hundreds of millions shots per year scale — `truly-unknown` — **important**
+- Rep-rated operation (1 Hz) not demonstrated at any scale for any component — truly-unknown — important
+- Automated target injection and loading at commercial scale — truly-unknown — important
+- Chamber survivability (debris, shock, optical windows) under repetitive operation — truly-unknown — important
 
 ---
 
@@ -89,86 +84,86 @@
 **Coverage**: Partial
 
 **Available**:
-- Boron-11 fuel: natural abundance ~80%, no enrichment required, ~10^9 ton confirmed global reserves — explicitly analyzed in `link-10-1007...` TEA paper as adequate for global deployment
-- No tritium required → eliminates entire tritium breeding/handling supply chain
-- No superconducting magnets required
-- Laser diode replacement identified as key cost driver: $1/W cost, 2.2 billion shot lifetime assumed (`link-10-1007...`)
-- High-power laser diodes: industrial supply chain exists for telecom/materials processing; fusion-scale manufacturing would require scale-up
+- McKenzie 2023 quantifies boron availability: world reserves ~10^9 tons, of which 80% is B-11; annual consumption for a global HB11 energy economy estimated at <10^6 tons/year (1,000× less than confirmed reserves). No supply chain bottleneck.
+- Hydrogen (proton source): effectively unlimited. Solid-state HB11 fuel cylinder eliminates cryogenic tritium handling — a major manufacturing simplification versus D-T ICF.
+- Diode lifetime assumption (2.2 billion shots, $1/W replacement cost) is the key stated laser O&M driver in McKenzie 2023.
+- Silver cover layer (patent): minor quantity per target (3 laser vacuum wavelengths = sub-micron thickness on 1 cm × 0.2 mm cylinder ≈ nanograms per target). Supply chain not a concern.
+- Novel target materials (white graphene, borophene): McKenzie 2023 notes these allow solution-based manufacturing "amenable to large-scale manufacturing" — a favorable indicator, though TRL is very low.
 
 **Missing**:
-- No analysis of laser glass or optical component supply chain (if DPSSL)
-- No materials study for chamber wall alpha irradiation damage and replacement rate
-- No analysis of target substrate materials (borophene, white graphene) supply and manufacturing
-- No cost breakdown for laser diode supply at scale (total diode count for 500 MW plant)
+- Per-shot consumable capacitor-coil module manufacturing at 1 Hz scale: each shot destroys the magnetic field device (nickel plates, coil, quartz fiber support, fuel body). At 1 Hz, a 1 GW plant requires ~31.5 million target-plus-coil assemblies per year. No published cost estimate or manufacturing process design exists for this volume.
+- Laser glass and optical component supply chain for rep-rated PW lasers at commercial scale: current petawatt lasers rely on large-aperture optical components that are not commercially available at the rep-rate or quantity a power plant would require.
+- Boron isotopic enrichment (B-11 purity requirement): McKenzie 2023 flags that isotopically pure B-11 may be needed to truly achieve aneutronic operation; enrichment costs and supply chain not quantified.
 
 **Gaps**:
-- Laser diode supply chain at fusion scale (gigawatts of installed diode capacity) — `not-yet-sourced` — **important** (search: fusion laser diode manufacturing scale-up, DPSSL diode cost trends)
-- Novel target material supply chain (borophene is not commercially produced) — `truly-unknown` for commercial scale — **important** (would block hybrid burn approach)
-- Chamber wall materials for alpha irradiation — `not-yet-sourced` — **nice-to-have** at this stage given pre-net-gain status
+- Per-shot target module (capacitor-coil + fuel) manufacturing at 31.5M units/year — derivable with large uncertainty — important
+- Optical components for rep-rated PW laser at commercial volume — not-yet-sourced — important
+- B-11 isotopic enrichment cost if required for aneutronic purity — derivable — nice-to-have
 
 ---
 
 ### 5. LCOE Parameter Extraction
-**Coverage**: Poor
-
 **Available Parameters**:
+
 | Parameter | Value/Range | Source | Confidence |
-|---|---|---|---|
-| Recirculating power fraction formula | f = 1/(εηG) | `link-10-1007...` McKenzie 2023 | h |
-| Target gain required (economic) | G = 100–300 | `link-10-1007...` | m |
-| Laser wall-plug efficiency target | η = 20% (DPSSL) | `link-10-1007...` | m (undemonstrated) |
-| Thermal conversion efficiency (steam) | ε = 36–40% | `link-10-1007...` | m |
-| Advanced conversion efficiency (DEC) | ε = 45–64% | `link-10-1007...` | l (theoretical) |
-| Commercial LCOE target | ≤ $35/MWh | `link-10-1007...` | h (constraint) |
-| Diode replacement cost | $1/W | `link-10-1007...` | l (assumed) |
-| Diode shot lifetime | 2.2 × 10^9 shots | `link-10-1007...` | l (assumed) |
-| Target cost (hybrid burn, G=200) | ~few $/target (acceptable) | `link-10-1007...` | l (estimated) |
-| Rep rate | ~1 Hz | `dossier.md`, patent | h |
-| Plant output target | ~500 MWe | `link-10-1007...` | m |
-| Reactor lifetime | 25 years | `link-10-1007...` | l (assumed) |
-| Pellet geometry | 1 cm × 0.2 mm HB11 cylinder | patent | m |
-| Boron fuel cost | Negligible (abundant) | `link-10-1007...` | h |
-| Current physics gain | ~10^−4 (4 OOM from breakeven) | `iter-01/sources/hb11-osaka-experiment-2022.md` | h |
+|-----------|-------------|--------|------------|
+| Rep rate (target) | ~1 Hz | Patent US10410752B2; HB11 website | h |
+| Target gain required for viability | G = 100–300 (assuming η=20%) | McKenzie et al. 2023 (iter-03/sources/link-10-1007-s10894-023-00349-9.md) | m |
+| Laser wall-plug efficiency (target) | 20% (DPSSL) | McKenzie et al. 2023 | m |
+| Recirculating power fraction target | ≤10% (competitive); 25% (minimum viable) | McKenzie et al. 2023 | m |
+| Conversion efficiency (steam) | 36–40% | McKenzie et al. 2023 | m |
+| Conversion efficiency (direct) | 45–50% (electrodynamic); 64% (MHD+Rankine) | McKenzie et al. 2023 | l |
+| Plant lifetime | 25 years (assumed, not neutron-limited) | McKenzie et al. 2023 | m |
+| Laser diode replacement cost | $1/W; 2.2 billion shot lifetime | McKenzie et al. 2023 | l |
+| DPSSL laser cost baseline | $700–1,000/J (current technology) | Xcimer whitepaper (knowledge/sources/commercialization_of_laser_fusion_energy/) | m |
+| IFE cost-competitive laser cost target | <$100/J (KrF excimer, Xcimer) | Xcimer whitepaper | m |
+| Minimum competitive LCOE (IFE parametric) | ~$25/MWh (G>500, yield >5 GJ/shot) | Hawker 2020 (knowledge/sources/a_simplified_economic_model_for_inertial_fusion/) | m |
+| LCOE market constraint tested | $35/MWh target, $350/MWh upper limit | McKenzie et al. 2023 | m |
+| Fusion energy per shot (patent claim) | ~1 GJ (G≈33,000 from 30 kJ input) | Patent US10410752B2 | l |
+| Fusion energy per shot (best experimental) | ~0.1 J per kJ laser energy (G ≈ 10^-4) | Margarone et al. 2022 | h |
+| Fuel cycle cost | Near-zero (no tritium, no cryogenics, boron abundant) | McKenzie et al. 2023 | h |
+| Neutron management cost | Minimal — aneutronic; thin shielding only | McKenzie et al. 2023 | h |
+| LCOE framework (14-parameter IFE model) | Directly applicable; same recirculating power formulation | Hawker 2020 (knowledge/sources/a_simplified_economic_model_for_inertial_fusion/) | h |
 
 **Missing Parameters**:
+
 | Parameter | Gap Type | Criticality | Notes |
-|---|---|---|---|
-| Capital cost by subsystem (CAS20–27) | truly-unknown | blocking | No plant study; no analogous p-B11 design published anywhere |
-| Total laser system installed cost | truly-unknown / proprietary | blocking | Adelaide grant hints at laser cost work; not published |
-| Laser cost per joule (for hybrid burn DPSSL) | not-yet-sourced | blocking | Xcimer has KrF data at <$100/J; DPSSL baseline from NIF era is $700–1000/J — but HB11 targets "commercial lasers" at unknown cost |
-| Balance of plant cost | derivable | important | Can use fleet-wide analogs (TEA D-T MFE, ARIES) — IFE BoP structurally similar |
-| O&M costs (beyond diode replacement) | derivable | important | Can estimate from fission/IFE analogs; no HB11-specific data |
-| Capacity factor / availability | truly-unknown | blocking | No maintenance schedule, no downtime analysis; target "baseload" but no quantification |
-| Fusion power per shot (Joules) | truly-unknown | blocking | Depends on G (undemonstrated); can only parameterize |
-| Chamber/first wall cost and replacement | truly-unknown | important | Alpha bombardment damage rate unknown; no materials data |
-| Target fabrication cost at scale | derivable/proprietary | blocking | "Few dollars/target" mentioned but not derived; 1 Hz × 500 MW implies ~$600M/yr at $1/target — very sensitive |
-| Actual laser energy on target required | truly-unknown | important | 30 kJ mentioned in patent but "hybrid burn" parameters unspecified |
+|-----------|----------|-------------|-------|
+| Capital cost by subsystem (CAS 20–27: laser arrays, chamber/vessel, target handling, energy conversion, BOP) | truly-unknown | **blocking** | No plant study or published cost estimates for any HB11-specific subsystem; ARIES CAS framework (knowledge/sources/aries_cost_account_documentation/) provides category definitions from 1992 IFE designs but HB11-specific values must be estimated from scratch |
+| Net fusion gain (G) demonstrated or reliably extrapolated from combined two-laser scheme | truly-unknown | **blocking** | Current experiments are single-laser; combined ns kT-field + ps PW scheme never tested; ~4 orders of magnitude from breakeven using best available single-laser experiments; any LCOE model must parameterize G explicitly |
+| Commercial rep-rated laser system cost and architecture (30 kJ ps PW at 1 Hz) | truly-unknown | **blocking** | DPSSL at $700–1,000/J (Xcimer paper) provides upper-bound analog for HB11's CPA petawatt laser; HB11's eventual "arrays of commercial lasers" architecture targets lower cost but no commercial rep-rated PW laser at this scale exists; at DPSSL costs a 30 kJ system costs $21–30M per shot-energy-equivalent |
+| Target (capacitor-coil module) unit cost at production volume | derivable | important | McKenzie 2023 states "several dollars per target acceptable" at G=200; no manufacturing process or supply chain cost model published |
+| O&M costs beyond laser diode replacement | truly-unknown | important | Laser gas, optics, vacuum systems, target injection mechanism, chamber debris removal, diagnostics — not quantified |
+| Capacity factor / system availability | derivable | important | No rep-rated operation demonstrated; IFE analogues (Hawker) assume ~85% availability but this has no experimental basis for the HB11 configuration |
+| Energy conversion efficiency (validated design) | proprietary | important | Range known (36–64%) but chosen architecture unsettled; steam cycle vs. direct conversion affects both CAPEX and η |
 
 ---
 
 ## Source Recommendations
 
-1. **Hawker (fleet-wide) IFE simplified economic model** (`knowledge/sources/a_simplified_economic_model_for_inertial_fusion/`) — directly applicable as structural analog. The 14-parameter model covers gain, efficiency, rep rate, and driver cost sensitivity in a technology-agnostic IFE framework. Use this to build the parameterized LCOE model skeleton for HB11 even where HB11-specific values are missing. `not-yet-sourced` for HB11-specific analysis.
-
-2. **Xcimer Energy commercialization whitepaper** (`knowledge/sources/commercialization_of_laser_fusion_energy/`) — provides laser cost breakdown by component for KrF excimer architecture (<$100/J). Serves as laser cost lower bound; HB11's DPSSL will be more expensive per joule but less power is needed per shot (30 kJ vs. MJ-class). Use as analog with noted differences. `not-yet-sourced` relative to HB11 analysis.
+- **Phys. Rev. Research 7, 013230 (2025)** — "Alpha particle production from novel targets in laser-driven p-B fusion" (identified in dossier, PDF not extracted). Most recent HB11 experimental results with novel target materials. Recommend R2 pull and agentic-mbse extraction. Not-yet-sourced — confirm DOI `10.1103/PhysRevResearch.7.013230` before retrieving.
 
-3. **ARIES cost accounts** (`knowledge/sources/aries_cost_account_documentation/`) — provides CAS framework (accounts 20–27) that can structure the capital cost estimate even without HB11-specific values. Use for BoP, direct costs, indirect cost conventions.
+- **Mehlhorn 2024, Physics of Plasmas 31(2)** — "From KMS Fusion to HB11 Energy, a personal 50-year IFE perspective." Co-author is HB11 Chief Science Advisor; likely contains historical cost and technoeconomic context. Not-yet-sourced — confirm existence via DOI `10.1063/5.0170661`.
 
-4. **Mehlhorn (2024), Physics of Plasmas** — "From KMS Fusion to HB11 Energy, a personal 50-year IFE perspective" — listed in dossier but not extracted. May contain the most detailed techno-economic discussion from HB11's own team. Flag: `not-yet-sourced` — **search OSTI/DOI 10.1063/5.0170661 and extract**. High priority.
+- **Laser & Particle Beams special issue (2023)** — Thirteen papers on H2-boron fusion mentioned in INFUSE grant press release (iter-02/sources/hb11-recent-developments-2024-2025.md). This volume likely contains the most current physics-of-gain results. Search OSTI/Cambridge Core for "Laser and Particle Beams 2023 proton boron special issue." Not-yet-sourced — unverified, confirm existence before searching.
 
-5. **Phys. Rev. Research (2025), PhysRevResearch.7.013230** — "Alpha particle production, novel targets, laser-driven PB fusion" — listed in dossier but not extracted. Contains most recent experimental physics data needed to update the current-state-of-the-art section. `not-yet-sourced` — extract from open-access source.
+- **ARIES 1992 IFE plant designs (Prometheus-L, Osiris, Sombrero)** — Referenced in ARIES cost account documentation (knowledge/sources/aries_cost_account_documentation/). These are costed IFE laser-driven plant designs from 1992 with CAS-level breakdowns that could provide order-of-magnitude analogues for HB11's non-laser subsystems (chamber, BOP, auxiliary systems). The ARIES cost account document itself was opened and confirms these designs exist and include IFE-specific cost algorithms. Search OSTI for UCID-21533 (Sombrero) and related reports.
 
-6. **DOE INFUSE/FIRE target design publications from LLE collaboration** — HB11's DOE INFUSE project with LLE/Rochester on H2-boron fuel targets may have produced technical reports or preprints. `not-yet-sourced` — search arXiv and OSTI for "proton boron fuel target" + Sefkow/Mehlhorn. `unverified — confirm existence before searching`.
+- **For capital cost analogue (laser arrays)**: The Xcimer whitepaper (knowledge/sources/commercialization_of_laser_fusion_energy/) opened and read — confirms DPSSL at $700–1,000/J and KrF target of <$100/J. These provide upper/target bounds for HB11's laser capital cost. No further search needed for laser cost bounding.
 
-7. **Hora et al. (Optical Engineering, 2021)** — "Green energy generation via optical laser pressure initiated nonthermal nuclear fusion" — cited in the J. Fusion Energy paper, likely contains reactor model details from the theoretical side. `not-yet-sourced` — DOI: 10.1117/1.OE.61.2.021004. `unverified — confirm existence before searching`.
+**Fleet-wide source disqualifications:**
+- `knowledge/sources/affordable_manageable_practical_and_scalable_amps_high/` (AMPS/Pacific Fusion): Opened and read. Pacific Fusion's pulser-driven MagLIF approach uses pulsed-power drivers and DT fuel — fundamentally different from HB11's laser + p-B11 architecture. Driver costs (pulser modules, water transmission lines), target physics (cryogenic DT liner), and tritium breeding are inapplicable. The paper's main value is contrasting laser IFE vs. pulser IFE efficiency, confirming that laser IFE has structural disadvantages at current driver efficiencies — useful context but adds no quantitative inputs for HB11.
+- `knowledge/sources/energy_from_inertial_fusion/` (Hogan et al. 1992): Opened and read. A 1992 Physics Today overview article focused on DT laser IFE and heavy-ion IFE using 1980s–early-1990s technology, predating chirped pulse amplification and the entire non-thermal laser fusion program that HB11 is based on. Contains no p-B11 economics data and no cost estimates relevant to CPA-laser architectures. Does not add materially to what is already available from Hawker (2020), Xcimer (2026), and McKenzie (2023).
+- `knowledge/sources/tea_dt_mfe_cost_analysis/` (TEA D-T MFE): Not opened — MFE-specific cost structure (magnetic coils, divertors, blankets, tritium breeding) is structurally incompatible with IFE cost accounts; BOP analogue would be swamped by concept-specific differences. Disqualified without opening based on scope mismatch (MFE vs. IFE).
+- `knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/` (ARPA-E ALPHA revisit): Not opened — the four ALPHA concepts are MIF/compact MFE variants (MSNW FRC, Helion, General Fusion MTF, Princeton FRC), not laser IFE. CAS framework is broadly applicable but concept-specific costs inapplicable. Disqualified based on concept family mismatch.
 
 ---
 
 ## Summary
 
-Proceed to full qualitative analysis with explicit caveats. The McKenzie/Batani (2023) J. Fusion Energy paper, the patent, and the Osaka experiment paper together provide enough material for a D1-level write-up covering system function, subsystem maturity, and supply chain. The materials and supply chain section benefits strongly from the aneutronic advantage (no tritium, no HTS magnets) which is well-documented.
+A D1+ analysis of HB11 is feasible as a qualitative exercise supported by parametric quantitative modeling, but carries unusually high fundamental uncertainty. The concept is approximately four orders of magnitude from net energy gain in any published experiment, the core two-laser scheme has never been tested together, and no plant-level capital cost estimates exist for any subsystem. The McKenzie et al. 2023 paper provides the only published TEA framework (gain requirement of 100–300, laser efficiency 20%, recirculating power fraction ≤10%) and the Hawker 2020 14-parameter IFE LCOE model provides a directly applicable methodology scaffold. Together, these allow a parametric LCOE model to be built, but the model will necessarily span many orders of magnitude in its uncertainty range.
 
-For the quantitative LCOE model: build a parameterized IFE power-balance model using the Hawker 14-parameter framework from the fleet-wide sources, populated where possible with HB11-specific values from `link-10-1007...` (η=20%, G=100–300, ε=36–40%). The model is necessarily a "what would need to be true" tool with gain G as the dominant free variable. Capital cost structure should borrow from Xcimer (laser cost $/J) and ARIES (BoP) with clear analog notes. Two missing sources should be extracted before finalizing: Mehlhorn (2024) and PhysRevResearch (2025).
+**Recommended approach**: Proceed to analysis, treating target gain (G) as the central free parameter and back-solving from LCOE targets. Use Hawker's 14-parameter framework with McKenzie 2023's stated parameters as inputs. For capital costs, borrow DPSSL laser costs from Xcimer ($700–1,000/J as baseline, <$100/J as target) and use ARIES 1992 IFE BOP analogues for non-laser subsystems. Flag all inputs as "assumed" or "analog-based" given the absence of any plant study. Acquiring Phys. Rev. Research 2025 and Mehlhorn 2024 before writing would improve the experimental status section, but is not blocking for the analysis structure.
 
 ---
 
@@ -176,11 +171,11 @@
 
 ```yaml
 overall_rating: "Significant Gaps"
-blocking_count: 7
-important_count: 8
-counting_method: "deduplicated across all sections — blocking gaps are those where no analog or derivation path exists and which prevent any credible value from being assigned to a model parameter; important gaps are those where analog-based estimates are possible but carry major uncertainty"
+blocking_count: 3
+important_count: 6
+counting_method: "all_sections_deduplicated — blocking: (1) net fusion gain / combined two-laser scheme unvalidated, (2) CAS-level capital cost absent, (3) commercial rep-rated laser system cost/architecture unknown; important: (1) energy conversion pathway unsettled, (2) target unit cost at scale, (3) O&M beyond diodes, (4) capacity factor/availability, (5) two most recent experimental papers not extracted, (6) automated target injection not developed"
 section_coverage:
-  availability_of_data:       "Poor"
+  availability_of_data:       "Partial"
   system_function:            "Partial"
   subsystem_maturity:         "Partial"
   materials_supply_chain:     "Partial"
```
