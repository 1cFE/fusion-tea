# Phase 3 diff: 37-magnetized-target-inertial-fusion-mtif

**Generated:** 2026-05-22T16:21:16-07:00

## Counts (Phase 2 -> Phase 3 strict-read regen)

| field | phase2 | phase3 | Δ |
|-------|--------|--------|---|
| blocking_count   | 9 | 5 | -4 |
| important_count  | 6 | 7 | - |
| overall_rating   | Insufficient Data | Insufficient Data | - |

## Fleet-source dispositions in new report

```
```

## Forbidden-phrase check (should be empty)

```
1:I now have sufficient information to write the gap assessment. Let me compose it.
```

## First line of new report (should start with `# Gap Assessment`)

```
I now have sufficient information to write the gap assessment. Let me compose it.
```

## Blocking-tier lines (new)

```
32:- Peer-reviewed physics performance data — `proprietary` / `not-yet-sourced` — **blocking**: no gain, triple product, or ignition proxy measurements are publicly available; the concept cannot be assessed against the Lawson criterion.
59:- Railgun energy balance and recirculating power — `proprietary` / `not-yet-sourced` — **blocking**: net energy output depends on driver wall-plug efficiency, which is not publicly disclosed for this application.
82:- Railgun driver lifetime at fusion conditions (10 km/s, 50 g, 10^9 shot requirement) — `not-yet-sourced` — **blocking** for cost modeling: barrel replacement schedule dominates O&M cost; military experience gives upper bound on replacement frequency but doesn't resolve 10 km/s plasma armature specific wear.
130:| Target gain (G = fusion energy / driver energy) | proprietary / truly-unknown | blocking | No published measurement or simulation result. Using Hawker framework at 1 Hz and 1 MJ driver: net power = 0.35 × G − (1/μd) MW per shot; competitive LCOE requires G >> 100 for realistic μd. D-D ignition conditions are substantially harder than D-T. |
131:| Fusion yield per shot (MJ) | truly-unknown | blocking | Follows directly from G × Ed; determines power plant output and pulse chamber loading. |
132:| Driver wall-plug efficiency (μd, railgun) | proprietary / not-yet-sourced | blocking | Plasma armature railgun efficiency in military applications is 20–40%; at fusion-relevant parameters (10 km/s, 50 g) it is uncharacterized. Dominates recirculating power fraction. |
133:| Pellet/capsule production cost (δ, $/capsule) | proprietary / not-yet-sourced | blocking | At 1 Hz, ~31.5 M capsules/year needed. NAS IFE review benchmark: laser IFE targets at 10 Hz = $0.20–0.35/target. MTIF's 50 g metallic capsule has entirely different cost structure. No estimate available. |
134:| Capital cost by subsystem (CAS 22: railgun, chamber, power conditioning) | proprietary | blocking | No plant study exists. ARPA-E ALPHA MIF analog ($1.2B for 500 MWe) covers different driver technologies; railgun at fusion scale is unbounded. |
```

## Full unified diff (truncated to 400 lines)

```diff
--- /tmp/gap_phase2_state/37-magnetized-target-inertial-fusion-mtif.md	2026-05-22 12:59:21.092042608 -0700
+++ /home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/37-magnetized-target-inertial-fusion-mtif/gap_report.md	2026-05-22 16:21:16.268316411 -0700
@@ -1,13 +1,10 @@
-I now have sufficient material to write the assessment. The concept-scoped sources are very thin (only marketing materials), the IOP source was bot-blocked, and the National Academies chapter is a general IFE technology review with no MTIF-specific content. The Woodruff ARPA-E ALPHA source is useful for CAS/BOP cost structure analogs.
-
----
+I now have sufficient information to write the gap assessment. Let me compose it.
 
 # Gap Assessment: Magnetized Target Inertial Fusion - MTIF (D-D)
 
 ## Overall Readiness
 **Rating**: Insufficient Data
-
-**Summary**: NearStar Fusion's MTIF concept is a very early-stage private venture (founded 2021) with no published peer-reviewed physics results, no demonstrated energy gain, and no public cost or LCOE estimates of any kind. Available data is limited to company marketing materials and a few confirmed architectural parameters (fuel, driver type, rep rate, first-wall material, and heat-extraction family). Every quantitative LCOE parameter is either `truly-unknown` or `proprietary`, making a credible D1+ quantitative analysis impossible without significant additional sourcing.
+**Summary**: NearStar Fusion has released only marketing-level public disclosures. No peer-reviewed experimental results, plant design studies, or cost analyses exist in the public domain. The concept architecture is legible (railgun driver, molten Pb chamber, steam Rankine cycle, D-D fuel), but every quantitative parameter needed for LCOE estimation — fusion gain, yield per shot, driver efficiency, capital costs, target production costs — is either proprietary or simply unpublished. Sections 1–4 support a qualitative system description at low confidence; section 5 (LCOE) cannot be substantively populated from available concept-scoped sources and must rely almost entirely on MIF analogs.
 
 ---
 
@@ -17,45 +14,49 @@
 **Coverage**: Poor
 
 **Available**:
-- Company website and marketing materials (`iter-01/sources/nearstar-mtif-technical-overview.md`, `nearstar-website-summary.md`): confirm driver architecture (plasma-armature railgun, 50 g capsules at 10 km/s, >1 MJ KE), fuel (D-D), rep rate (1 Hz), first wall (molten Pb), heat-extraction strategy (steam Rankine / coal-plant retrofit), and scalability claim (50 MW–1 GW+)
-- `iter-02/sources/nearstar-energy-capture-research.md`: resolves energy-capture cycle family to thermal (steam Rankine) from coal-plant retrofit framing
-- General IFE technology review (`nationalacademies-read-18289-chapter-5.md`): covers target fabrication, liquid-wall chambers, chamber clearing at 0.1–10 Hz, pulsed-power chamber issues — applicable by analogy but not MTIF-specific
-- IOP paper (`iopscience-10-1088-1741-4326-ac2dbe.md`): **bot-blocked, zero usable content**
-- No peer-reviewed publications on NearStar MTIF physics performance, implosion modeling results, or system-level studies are available in the ingested sources or referenced in the dossier
+- NearStar Fusion company website (`iter-01/sources/nearstar-mtif-technical-overview.md`, `nearstar-website-summary.md`): top-level concept description, driver specs (50 g capsules, 10 km/s, >1 MJ, 1 Hz), fuel choice (D-D), first wall (molten Pb), energy conversion strategy (coal-plant steam turbine retrofit), scalability claim (50 MW–1 GW+), university partners (UAH modeling, Texas A&M HVIL impact experiments).
+- `iter-02/sources/nearstar-energy-capture-research.md`: confirms steam Rankine energy conversion family via brownfield retrofit framing.
+- `nationalacademies-read-18289-chapter-5.md`: comprehensive NAS review of IFE technology challenges (target fabrication/injection, chamber first-wall options including liquid metal walls, tritium issues, balance-of-plant). Provides useful background context for all five IFE subsystem categories, though not MTIF-specific.
+- `en-wiki-railgun.md`: railgun physics, performance envelope, known failure modes (rail arcing, rail wear), plasma armature technology. Militarily relevant velocity data (2–3.5 km/s typical; MTIF's 10 km/s target is well above current military demonstrations).
+- Fleet-wide: Woodruff Scientific ARPA-E ALPHA revisit (`knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`) provides cost structure and LCOE range for four MIF concepts (Plasma-Jet MIF, Stabilized Liner Compressor, Staged Z-Pinch, Flow-stabilized Z-Pinch) — closest available economic analog.
+- Fleet-wide: Hawker (2020) simplified IFE economic model (`knowledge/sources/a_simplified_economic_model_for_inertial_fusion/`) provides a technology-agnostic 14-parameter LCOE framework applicable to pulsed fusion including MTIF.
+- Fleet-wide: Wurzel & Hsu (2021) Lawson criterion compilation (`knowledge/meta_analysis/progress_toward_fusion_breakeven_lawson_criterion/`) includes MIF methodology section and characterizes MIF efficiency parameters (ηE·ηabs ≈ 0.9×0.1 = 0.09), setting the gain requirement context.
 
 **Missing**:
-- Any peer-reviewed or preprint physics paper on MTIF implosion performance, neutron yield, or compression efficiency
-- University of Alabama Huntsville (UAH) modeling results referenced by company but not published
-- Texas A&M HVIL impact experiment data referenced by company but not published
-- Fusion Energy Base profile adds no technical depth beyond the company website
+- The IOP Science article (`iopscience-10-1088-1741-4326-ac2dbe.md`) was blocked by a CAPTCHA/bot wall; its content is unavailable. This may be the most technically substantive concept-specific source.
+- No peer-reviewed publications from NearStar are in the captured source set.
+- Results from UAH modeling and Texas A&M HVIL experiments are not published.
+- StartEngine and VIPC investor materials may contain quantitative roadmap data not captured.
 
 **Gaps**:
-- No peer-reviewed physics basis for the concept — `proprietary`/`truly-unknown` — **blocking**
-- Data availability effectively opaque for all technical and economic parameters — **blocking**
+- Peer-reviewed physics performance data — `proprietary` / `not-yet-sourced` — **blocking**: no gain, triple product, or ignition proxy measurements are publicly available; the concept cannot be assessed against the Lawson criterion.
+- IOP article content — `not-yet-sourced` — **important**: the blocked IOP article (DOI: 10.1088/1741-4326/ac2dbe) likely contains the most substantive technical content on this concept; re-fetching with a different retrieval method is warranted.
+- Lab experiment reports (HVIL impact data, UAH modeling outputs) — `proprietary` — **important**: cited by NearStar but not published; would establish compression coupling efficiency.
 
 ---
 
 ### 2. Challenges in Capturing System Function
-**Coverage**: Poor
+**Coverage**: Partial
 
 **Available**:
-- Basic system architecture is clear from marketing materials: railgun launches magnetized D-D capsule into molten Pb pool; shockwave-driven implosion; thermal extraction via molten Pb intermediate loop to steam turbine
-- Liquid-wall IFE chamber analogues exist in literature (LIFE, thick liquid wall concepts in National Academies review); chamber clearing at ~1 Hz, liquid jet re-establishment, and debris management are discussed generically
-- Pulsed-power IFE analog: National Academies notes ~0.1 Hz for pulsed-power concepts; MTIF's 1 Hz is ten times faster and has no published feasibility validation
+- Fusion chain is conceptually clear: railgun accelerates a 50 g pre-magnetized D-D fuel capsule to 10 km/s; hypervelocity projectile impact on a molten Pb target generates shockwaves that simultaneously compress, heat, and further magnetize the fuel. Heritage is Sandia Z-Machine liner implosion technique applied in a free-firing geometry.
+- Molten Pb first wall doubles as neutron absorber and primary heat sink; thermal coupling to steam cycle via intermediate loop is architecturally analogous to liquid-metal-cooled designs discussed in the NAS review (wetted/thick liquid wall chambers, pp. 255–260 of chapter 5 extraction).
+- 1 Hz rep rate governs chamber clearing time, thermal pulse averaging, and target injection cadence. NAS review notes that at ~0.1 Hz (pulsed power class), chamber dynamics are less severe than at 5–16 Hz laser designs.
+- Energy conversion: steam Rankine, deriving from coal-plant retrofit framing. Thermal efficiency derivable from steam cycle thermodynamics (typically 30–38% for subcritical/supercritical Rankine).
 
 **Missing**:
-- Compression physics: magnetization seed-field geometry, convergence ratio, achievable ρR, and implosion symmetry are undisclosed
-- Energy balance: railgun input (>1 MJ electrical) vs. fusion yield — no Q value, even as a target
-- Repetitive-shot energy balance including recirculating power for the railgun power supply
-- Railgun barrel erosion and replacement cadence at 1 Hz / >1 MJ per shot over a 30-year plant life (~10⁹ shots) — unprecedented in any published railgun literature
-- Chamber clearing: resetting the molten Pb target pool between 1 Hz shots — hydrodynamics of rapid liquid refill/settling not addressed
-- Pre-magnetization mechanism for 50 g capsules at production scale (embedded coil? θ-pinch? capacitor bank?) — not disclosed
+- Pre-magnetization mechanism is entirely undisclosed (embedded coil, external θ-pinch, capacitor-driven field?). This affects both the energy balance and the cost of the target/pellet system.
+- Compression coupling efficiency: how much of the projectile kinetic energy is deposited as compressive work vs. lost to ejecta, lateral shock, and structural damage to the lead target. No published hydrodynamic simulation results.
+- Chamber dynamics at 1 Hz: clearing time for debris, condensed Pb vapor, and activated particles before next shot. The NAS review discusses this challenge for liquid wall chambers but not at MTIF's specific operating point.
+- D-D fusion produces tritium as a secondary product (D+D → T+p, 50% branching). NearStar markets as "tritium-free" but must address accumulation in the Pb blanket and off-gas handling. No disclosed strategy.
+- Recirculating power fraction: railgun wall-plug efficiency is unknown; this determines whether the system achieves net positive energy output.
 
 **Gaps**:
-- No energy gain or Q target published — `proprietary`/`truly-unknown` — **blocking**
-- Railgun durability at 1 Hz / >1 MJ shot / 10⁹-cycle plant life: no analogue in engineering literature — `truly-unknown` — **blocking**
-- Chamber clearing and molten Pb re-establishment at 1 Hz: not studied publicly — `not-yet-sourced` (analogous work exists for HIF thick liquid walls, but at ~5 Hz; 1 Hz Pb-pool filling physics differs) — **important**
-- Pre-magnetization mechanism details — `proprietary` — **important**
+- Pre-magnetization mechanism and energy budget — `proprietary` — **important**: affects driver energy balance and pellet cost.
+- Shockwave-to-compression coupling physics — `proprietary` / `not-yet-sourced` — **important**: without knowing compression efficiency, gain cannot be estimated.
+- D-D tritium byproduct handling strategy — `not-yet-sourced` — **important**: the "tritium-free" claim requires qualification; handling strategy affects O&M and regulatory category.
+- Chamber clearing dynamics at 1 Hz — `derivable` (with multi-physics simulation) — **important**: affects capacity factor assumptions.
+- Railgun energy balance and recirculating power — `proprietary` / `not-yet-sourced` — **blocking**: net energy output depends on driver wall-plug efficiency, which is not publicly disclosed for this application.
 
 ---
 
@@ -63,22 +64,25 @@
 **Coverage**: Poor
 
 **Available**:
-- Plasma-armature railguns exist at research scale (hypervelocity impact ranges like TAMU HVIL); Wikipedia railgun article (`en-wiki-railgun.md`) confirms state of art for defense and research applications but is not fusion-specific
-- Molten Pb containment is used in fission (lead-bismuth eutectic reactors, BREST-OD-300) and IFE chamber studies — materials data exists but not yet sourced for this context
-- Steam Rankine balance of plant is fully mature (TRL 9) — no gap here
-- Sandia Z-machine heritage claimed for liner implosion physics, but Z-machine is a pulsed-power machine at very different scale and configuration from a railgun-launched projectile
+- Railgun technology (general): Wikipedia railgun article confirms military railguns demonstrate ~2–3.5 km/s at 5–50 MJ muzzle energy; plasma armature configurations reach higher velocities but suffer rail wear and arcing. NearStar's 10 km/s at >1 MJ with a 50 g load exceeds demonstrated military railgun performance at this mass class.
+- Company claims COTS railgun components, heritage from Sandia Z-machine.
+- University partnerships: UAH for modeling, Texas A&M HVIL for impact experiments — suggests TRL 2–3 (concept experimentally explored).
+- NAS IFE review provides TRL context for IFE subsystems generally: target injection at adequate velocity demonstrated in lab (Conclusion 3-5), liquid wall concepts have significant R&D remaining.
+- Steam Rankine power conversion: TRL 8–9 (mature, deployed at scale in coal/nuclear plants).
 
 **Missing**:
-- Integrated MTIF system TRL assessment — no published document
-- Railgun component TRL for fusion application (barrel, armature, power supply for 1 Hz / >1 MJ at >10⁸ shots): TRL 2–3 by available evidence
-- Magnetized capsule fabrication TRL: TRL 2–3 (no fabrication process described publicly)
-- Molten Pb intermediate loop (pumps, heat exchangers, corrosion, activation management): TRL 3–4 by analogy to fission LBE reactors, but not characterized for this application
-- Fusion neutron shield geometry and first-wall structural assessment: not disclosed
+- No TRL self-assessment published by NearStar.
+- No independent TRL assessment in the captured sources.
+- Specific experiment results from UAH/HVIL not published.
+- Pellet/target design and fabrication specifications: not disclosed.
+- Railgun barrel lifetime in the fusion application regime: not addressed. Military railguns require barrel replacement after hundreds to low thousands of shots (per Wikipedia: rail erosion by plasma arc contacts is a key limitation); at 1 Hz for a 30-year plant lifetime, ~10^9 shots are required, orders of magnitude beyond current military demonstrations.
 
 **Gaps**:
-- No published TRL assessment for any MTIF subsystem — `proprietary` — **blocking**
-- Railgun durability and rep-rate TRL for fusion application: TRL 2–3, decades away from commercial readiness — `truly-unknown` — **blocking**
-- Capsule fabrication at rate (86,400/day at 1 Hz): no process described; analogous IFE target fabrication challenge is a known hard problem (National Academies Conclusion 3-9) — `not-yet-sourced` — **important**
+- System-level TRL (estimated TRL 2–3) — no published evidence — **important**: no independent assessment; concept not yet demonstrated at any scale.
+- Railgun driver lifetime at fusion conditions (10 km/s, 50 g, 10^9 shot requirement) — `not-yet-sourced` — **blocking** for cost modeling: barrel replacement schedule dominates O&M cost; military experience gives upper bound on replacement frequency but doesn't resolve 10 km/s plasma armature specific wear.
+- Magnetized pellet fabrication at production scale — `proprietary` / `not-yet-sourced` — **important**: pellet production at 31.5 M capsules/year (1 Hz, ~90% availability) is an uncharacterized manufacturing challenge.
+- Molten Pb chamber: structural integrity, pumping system, and heat extraction at 1 Hz — `not-yet-sourced` — **important**: analogous to liquid metal first wall designs in MFE (LiPb blankets at TRL 4–5) but Pb chemistry and neutron absorption at this scale is novel.
+- Experimental results from HVIL impact tests — `proprietary` — **important**: would establish shockwave coupling data.
 
 ---
 
@@ -86,75 +90,88 @@
 **Coverage**: Poor
 
 **Available**:
-- Molten Pb first wall: Pb is abundant and inexpensive; National Academies notes Pb as a candidate hohlraum/chamber material with manageable activation; not a supply-chain bottleneck
-- D-D fuel: deuterium extracted from seawater, essentially unlimited supply — not a constraint; no tritium required (NearStar's explicit rationale)
-- No HTS magnets (no external confinement) — no REBCO supply issue
-- Plasma-armature railgun barrel materials (copper or composite conductors, structural steel or composite rails) — mature industrial supply chains
+- Lead (Pb): Plentiful global supply; commodity material, not on critical minerals lists. Pb activation under D-D 2.45 MeV neutrons produces radioisotopes (primarily ^203Pb, ^205Pb) but lower activation hazard than under D-T 14.1 MeV neutrons. NAS IFE review notes daily throughput of ~4 tonnes of Pb per target per day for laser IFE (indirect drive); MTIF uses Pb at chamber scale rather than per-target scale, but total inventory still significant.
+- Copper/aluminum rails: abundant, but consumable at scale. Military railguns use copper or carbon-fiber reinforced rails; wear characteristics well-documented (Wikipedia) but not at MTIF's operating point.
+- D-D fuel (deuterium): abundant, derived from seawater. No supply chain concern.
+- No rare-earth or critical materials identified from public information.
 
 **Missing**:
-- Capsule material composition and fabrication materials — not disclosed; could involve exotic magnetizable materials or engineered microspheres
-- Railgun barrel material longevity and replacement volume at commercial scale
-- Molten Pb corrosion data for long-term structural material compatibility (steel, ceramic, or refractory liners) — published LBE fission literature is partially applicable but not yet sourced
-- Activation and waste stream characterization for Pb under 14 MeV D-D neutrons (D-D produces 2.45 MeV neutrons, not 14 MeV; activation products differ from D-T)
+- Complete bill of materials for railgun system (rail material, capacitor banks, pulse-forming network) not disclosed.
+- Capsule material composition not disclosed (casing, pre-magnetization components, fuel containment).
+- Pb replacement schedule (how much Pb is consumed or activated per shot and needs replacement) not analyzed.
+- Supply chain for COTS railgun components at fusion-plant scale (manufacturing throughput, vendor landscape).
 
 **Gaps**:
-- Capsule materials and fabrication process: `proprietary` — **important**
-- Molten Pb structural compatibility and long-term activation data for D-D neutron spectrum: `not-yet-sourced` — **important**
-- No critical material bottleneck identified (good), but no supply chain analysis published: `not-yet-sourced` — **nice-to-have**
+- Railgun rail/barrel replacement material and supply chain — `not-yet-sourced` — **important**: barrel wear is the dominant consumable cost driver in military railguns; fusion application is far more demanding.
+- Lead activation, inventory, and waste management at full scale — `derivable` (with neutronics model) — **important**: D-D neutrons activate Pb; waste classification and handling costs depend on activation inventory.
+- Pellet/capsule bill of materials and fabrication supply chain — `proprietary` — **important**: capsule cost at 1 Hz production rate is a key LCOE driver.
+- Capacitor bank / pulsed power supply lifetime and replacement — `not-yet-sourced` — **important**: pulsed power components have finite cycle lives.
 
 ---
 
 ### 5. LCOE Parameter Extraction
-**Coverage**: Poor
-
 **Available Parameters**:
 | Parameter | Value/Range | Source | Confidence |
 |-----------|-------------|--------|------------|
-| Rep rate | ~1 Hz | Company website | High |
-| Capsule KE per shot | >1 MJ | Company website | High |
-| Capsule mass | ~50 g | Company website | High |
-| Target plant size | 50 MW–1 GW+ (claim) | Company website | Low |
-| Energy conversion cycle | Thermal (steam Rankine) | Company website (coal retrofit framing) | Medium |
-| Thermal efficiency (analog) | ~33–38% | Derivable from steam Rankine assumption | Low |
-| Fuel cost (D-D) | Near-zero (deuterium from seawater) | Derivable | High |
-| BOP capital cost (analog) | ~$1–2B for ~500 MWe | `revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/` (CAS framework analog) | Low |
+| Rep rate (f) | 1 Hz | NearStar website (dossier) | high |
+| Driver kinetic energy (Ed) | >1 MJ per shot | NearStar website | high |
+| Fuel cycle | D-D | NearStar website | high |
+| Energy conversion family | Steam Rankine | `nearstar-energy-capture-research.md` | medium |
+| Thermal efficiency (μth) | 30–38% | Derivable from steam Rankine thermodynamics | medium (analog) |
+| Plant scalability target | 50 MW – 1 GW+ | NearStar website | low (unvalidated) |
+| LCOE analog (MIF concepts) | $34–54/MWh, ~500 MWe | `knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/` (Woodruff, 2020, p.62) | low (different concept) |
+| CapEx analog (MIF concepts) | ~$2.4/W, ~$1.2B for 500 MWe | Same source, Table 4 | low (different concept) |
+| BOP cost structure (CAS 21–27) | Nuclear/BWR-derived scaling | `knowledge/sources/aries_cost_account_documentation/` — turbine plant (CAS 23), structures (CAS 21) use BWR analogs | medium (BOP only) |
+| LCOE sensitivity parameters | Gain (G), driver cost (γ, $/J), target cost (δ, $/target), availability (μa) are highest sensitivity | `knowledge/sources/a_simplified_economic_model_for_inertial_fusion/` (Hawker, 2020, Table 2 and Monte Carlo analysis) | medium (framework applicable) |
 
 **Missing Parameters**:
 | Parameter | Gap Type | Criticality | Notes |
 |-----------|----------|-------------|-------|
-| Energy gain Q (fusion yield / driver input) | truly-unknown | Blocking | No target value or physics estimate published |
-| Driver wall-plug efficiency (railgun electrical → KE) | proprietary | Blocking | ~10–40% typical for railguns; fusion-relevant value undisclosed |
-| Recirculating power fraction | truly-unknown | Blocking | Depends on Q and driver efficiency; Q must be known first |
-| Capital cost by subsystem (CAS) | proprietary | Blocking | No plant study, no cost estimate of any kind published |
-| Capsule fabrication cost per shot | truly-unknown | Blocking | Process undisclosed; ~86,400/day at 1 Hz |
-| Railgun replacement/maintenance schedule | truly-unknown | Blocking | Barrel erosion at >1 MJ/shot; no analogue at this scale |
-| Capacity factor / availability | truly-unknown | Blocking | Depends on railgun reliability, chamber maintenance; not estimated |
-| O&M costs | truly-unknown | Important | No analogue study for this concept type |
-| Molten Pb loop thermal design (ΔT, flow rate) | proprietary | Important | Sets intermediate loop capital and pump costs |
-| Neutron shielding and structural costs | proprietary | Important | D-D produces fewer 14 MeV neutrons but still significant shielding required |
-| Plant power balance (gross electric, auxiliary loads) | truly-unknown | Important | Required for net electric output and capacity factor |
+| Target gain (G = fusion energy / driver energy) | proprietary / truly-unknown | blocking | No published measurement or simulation result. Using Hawker framework at 1 Hz and 1 MJ driver: net power = 0.35 × G − (1/μd) MW per shot; competitive LCOE requires G >> 100 for realistic μd. D-D ignition conditions are substantially harder than D-T. |
+| Fusion yield per shot (MJ) | truly-unknown | blocking | Follows directly from G × Ed; determines power plant output and pulse chamber loading. |
+| Driver wall-plug efficiency (μd, railgun) | proprietary / not-yet-sourced | blocking | Plasma armature railgun efficiency in military applications is 20–40%; at fusion-relevant parameters (10 km/s, 50 g) it is uncharacterized. Dominates recirculating power fraction. |
+| Pellet/capsule production cost (δ, $/capsule) | proprietary / not-yet-sourced | blocking | At 1 Hz, ~31.5 M capsules/year needed. NAS IFE review benchmark: laser IFE targets at 10 Hz = $0.20–0.35/target. MTIF's 50 g metallic capsule has entirely different cost structure. No estimate available. |
+| Capital cost by subsystem (CAS 22: railgun, chamber, power conditioning) | proprietary | blocking | No plant study exists. ARPA-E ALPHA MIF analog ($1.2B for 500 MWe) covers different driver technologies; railgun at fusion scale is unbounded. |
+| Plant availability / capacity factor (μa) | not-yet-sourced | important | No operational precedent. Hawker framework treats this as a free parameter; for first-of-kind plants availability is typically <70% initially. |
+| O&M cost (ε, $/kWe-yr) | not-yet-sourced | important | Dominated by rail/barrel replacement schedule. No data on barrel lifetime at 10 km/s, 50 g, plasma armature. |
+| Blanket/chamber replacement schedule | not-yet-sourced | important | Pb activation and structural damage determine replacement interval; neutronics model needed. |
+| D-D tritium byproduct handling cost | not-yet-sourced | important | D-D produces tritium (50% branch); Pb blanket will accumulate T over time. No stated handling strategy from NearStar. |
 
 ---
 
 ## Source Recommendations
 
-- **ARPA-E ALPHA costing revisit** (`knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`): Already ingested; applicable for CAS-structured BOP and modular-plant capital cost analogues (~$2.4/W, ~43 $/MWh at 500 MWe). The four ALPHA concepts are modular MIF/MTF-adjacent systems. Use as a cost floor analog with large uncertainty.
+**Re-fetch IOP article**: The blocked IOP Science article (DOI: 10.1088/1741-4326/ac2dbe) should be re-fetched via a direct PDF download from the journal or a preprint server (e.g., arXiv). It may be the most technically substantive concept-scoped source. `not-yet-sourced` — confirm existence and re-attempt retrieval before next iteration.
+
+**APS-DPP / IAEA fusion conference abstracts**: Search for "NearStar" or "MTIF" or "Witherspoon" in APS Division of Plasma Physics abstract archives (2022–2025) and IAEA Fusion Energy Conference proceedings. NearStar likely presented preliminary experiment results at a conference. `not-yet-sourced` — unverified; search OSTI and APS abstract books.
 
-- **Simplified IFE economic model** (`knowledge/sources/a_simplified_economic_model_for_inertial_fusion/`): Already ingested; provides 14-parameter Monte Carlo framework for IFE LCOE. Applicable to MTIF with wide parameter ranges. Most useful for back-solve analysis (which Q / driver efficiency values would be needed for competitive LCOE).
+**ARPA-E ALPHA program documentation**: NearStar lists DOE and ARPA-E as funders. ARPA-E DE-FOA-0001385 (ALPHA program) documents and related performance reports may contain technical metrics. `not-yet-sourced` — search ARPA-E Explorer for NearStar grant records.
 
-- **Search OSTI for NearStar / Witherspoon / railgun fusion papers**: Dr. Douglas Witherspoon (NearStar founder) has a prior publication record on plasma railguns and compact fusion at HyperV Technologies Corp (OSTI full-text search: "Witherspoon railgun fusion" or "HyperV railgun MTF"). Any published HyperV/Witherspoon papers from ~2008–2021 would provide physics basis for the driver architecture — `unverified — confirm existence before searching`.
+**USPTO patent search**: The dossier notes the pellet pre-magnetization mechanism is undisclosed; a USPTO assignee search for "NearStar Fusion" or inventor "Douglas Witherspoon" may yield patent filings with technical specifications. `not-yet-sourced`.
 
-- **Search APS-DPP conference proceedings for NearStar / UAH MTIF modeling**: UAH is named as a modeling partner; APS-DPP abstract database (2022–2025) may contain preliminary implosion modeling results — `unverified — confirm existence before searching`.
+**Sandia Z-Machine magnetized liner (MagLIF) literature**: MTIF claims Z-Machine heritage. MagLIF experiment series (Knauer et al., McBride et al., from SNL, published in Physical Review Letters and PRL-adjacent journals) provides the closest physics analog — magnetized D-D liner compression, neutron yields, gain measurements. Relevant for gain estimation and subsystem TRL. `not-yet-sourced` — search OSTI for "MagLIF" and "magnetized liner inertial fusion."
 
-- **LBE fission reactor materials literature** (BREST-OD-300, MYRRHA): Published data on structural material compatibility with molten lead/LBE at 400–550°C is directly applicable to the MTIF molten Pb intermediate loop. IAEA NDS or OECD NEA documents would be relevant — `unverified — confirm existence before searching`.
+**First Light Fusion technical publications**: First Light Fusion (projectile-driven IFE, UK) uses a similar hypervelocity impact concept. First Light has published plasma conditions achieved and is potentially the closest technical analog in the public literature. `not-yet-sourced` — search arXiv and Nature Energy for First Light Fusion publications.
 
-- **Search DOE ARPA-E award database**: NearStar's website claims DOE, ARPA-E, NASA, and NSF funding. Any ARPA-E award would come with a public project description and potentially a final report — `unverified — confirm existence before searching`.
+**Fleet-wide source disqualifications**:
+
+- `knowledge/sources/tea_dt_mfe_cost_analysis/`: MFE D-T tokamak cost methodology; fuel cycle assumptions (tritium breeding blanket) are inapplicable to MTIF's D-D, no-breeding architecture. Disqualified.
+- `knowledge/sources/overview_of_the_helios_design_a_practical_planar_coil/`: Stellarator with planar HTS coils and continuous plasma — no cost analogs transfer to pulsed railgun MIF. Disqualified.
+- `knowledge/sources/an_assessment_of_the_economics_of_future_electric_power/`: Historical ORNL benchmarking of fusion vs. competing power generation; provides competitive LCOE context but addresses none of MTIF's blocking gaps (no concept-specific costs or physics parameters). Disqualified.
+- `knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/`: Heavy-ion beam driver at 5–10 Hz; driver cost scaling ($/J for induction linac) does not translate to plasma armature railgun; target gain and yield operating regime differ substantially. Disqualified.
+- `knowledge/sources/energy_from_inertial_fusion/`: 1992 comprehensive IFE review opened via content search — covers laser, heavy-ion, and light-ion drivers with liquid wall chamber designs (e.g., OSIRIS with molten FLiBe); provides general liquid wall context but no railgun/MIF driver economics or D-D MTIF parameters. Disqualified as concept-specific analog.
+- `knowledge/sources/accelerators_for_inertial_fusion_energy_production/`: Reviews induction linacs, RF linacs, and diode-pumped lasers; plasma armature railguns are electromagnetically accelerated but share no cost structure with RF or induction linac driver technology. Disqualified.
+- `knowledge/sources/affordable_manageable_practical_and_scalable_amps_high/`: Pacific Fusion's high-yield pulser IFE at >1 GJ yield and >100 gain — fundamentally different operating regime (high-yield, low-rep-rate) from MTIF's 1 Hz, ~1 MJ input concept. Disqualified.
+- `knowledge/sources/commercialization_of_laser_fusion_energy/`: Xcimer KrF laser cost breakdown and hybrid direct-drive targets; driver architecture and target cost structure do not transfer to railgun/solid-projectile MIF. Disqualified.
+- `/home/reid/PyFECONS`: Requires physics inputs (gain, yield, driver cost) that are blocking unknowns for MTIF; cannot generate useful outputs without these parameters. Disqualified for this assessment.
 
 ---
 
 ## Summary
 
-The available data for MTIF (D-D) / NearStar Fusion is insufficient to produce a credible D1+ quantitative LCOE analysis. The concept is at TRL 2–3 across all non-BOP subsystems, and the company has not published any physics results, energy gain targets, cost estimates, or engineering design documents. All LCOE parameters beyond the conversion cycle family and fuel type are either `truly-unknown` or `proprietary`. The most productive path forward is to search for prior Witherspoon/HyperV publications (which may establish the physics heritage) and ARPA-E award disclosures (which may contain a project abstract with performance targets). Absent new sources, the quantitative section of the D1+ analysis must be built on very wide parameter ranges using IFE analogues from the Hawker simplified model and the Woodruff ALPHA revisit, with Q and driver efficiency as the two dominant free parameters.
+MTIF (D-D) is at too early a stage for a full quantitative D1+ analysis. The concept architecture is coherent and qualitatively describable: plasma armature railgun driver → hypervelocity impact compression of magnetized D-D pellet → molten Pb heat capture → steam Rankine electricity. However, NearStar Fusion has not published a single quantitative physics performance result — no gain measurement, no triple product, no neutron yield, no driver efficiency. Without fusion gain (G), no LCOE can be calculated. The closest published analogs are the four ARPA-E ALPHA MIF concepts ($34–54/MWh LCOE at ~500 MWe; Woodruff 2020) and the Hawker 14-parameter IFE model framework, both of which provide structure but not MTIF-specific values.
+
+**Recommended action before full analysis**: Re-fetch the blocked IOP article; search ARPA-E Explorer for NearStar grant outputs; search APS-DPP abstracts for Witherspoon/MTIF presentations; and search for First Light Fusion and MagLIF publications as physics analogs. A qualitative system-function and maturity section (D1+ sections 2–4) can be written at low confidence with current data; the LCOE section (section 5) requires at minimum a gain estimate, driver efficiency assumption, and a railgun cost model before it can be populated beyond the MIF analog range.
 
 ---
 
@@ -162,12 +179,12 @@
 
 ```yaml
 overall_rating: "Insufficient Data"
-blocking_count: 9
-important_count: 6
-counting_method: "all_sections_deduplicated — blocking: no physics basis, no Q/gain, no driver efficiency, no capital costs, no capsule fabrication process/cost, no railgun durability data, no plant study, no TRL assessment, no capacity factor; important: pre-magnetization mechanism, molten Pb loop design, capsule materials, molten Pb activation data, O&M costs, plant power balance"
+blocking_count: 5
+important_count: 7
+counting_method: "unique gap topics across all sections, deduplicated: blocking = {fusion gain G, fusion yield per shot, driver wall-plug efficiency, capsule production cost, capital cost by subsystem}; important = {plant availability/capacity factor, O&M/rail replacement cost, chamber replacement schedule, D-D tritium byproduct handling, IOP article content, railgun lifetime at 10^9 shots, lab experiment results}"
 section_coverage:
   availability_of_data:       "Poor"
-  system_function:            "Poor"
+  system_function:            "Partial"
   subsystem_maturity:         "Poor"
   materials_supply_chain:     "Poor"
   lcoe_parameter_extraction:  "Poor"
```
