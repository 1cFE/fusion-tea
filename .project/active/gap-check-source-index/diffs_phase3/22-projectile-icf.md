# Phase 3 diff: 22-projectile-icf

**Generated:** 2026-05-22T15:10:34-07:00

## Counts (Phase 2 -> Phase 3 strict-read regen)

| field | phase2 | phase3 | Δ |
|-------|--------|--------|---|
| blocking_count   | 5 | 5 | 0 |
| important_count  | 7 | 5 | - |
| overall_rating   | Mostly Ready | Significant Gaps | - |

## Fleet-source dispositions in new report

```
```

## Forbidden-phrase check (should be empty)

```
(none — good)
```

## First line of new report (should start with `# Gap Assessment`)

```
I have read all concept-scoped sources and the most relevant fleet-wide sources. Now I'll write the gap assessment report.
```

## Blocking-tier lines (new)

```
21:- No published conceptual design study (power core, BOP, economics in CAS format) — `truly-unknown` — **blocking** for quantitative LCOE model, **important** for qualitative analysis
35:- Gain physics validation gap: current demonstrated result (~50 neutrons) is far below commercial-minimum G=200; path to gain undemonstrated and unverified — `truly-unknown` — **blocking**
36:- Rep-rated EM gun operation at 60+ km/s projectile velocity: no precedent, Machine 4 cancelled — `truly-unknown` — **blocking**
99:| Target cost per shot (manufacturing at scale) | proprietary | **blocking** | Hawker 2020 identifies target cost as a top-3 LCOE driver; FLF's target is core IP; current prototype costs are irrelevant; required range is $1–100/target |
100:| Rep-rated EM gun driver capital cost | truly-unknown | **blocking** | Machine 4 (100 MJ, 60 km/s) was cancelled; no rep-rated gain-scale EM gun exists anywhere; Machine 3 cost ($1.7/J) is for non-rep-rated device |
101:| Driver efficiency (wall-plug to kinetic energy) | proprietary/derivable | **blocking** | Critical for recirculating power fraction; Machine 3 specs (6.5 km/s, 2.5 MJ bank) do not disclose electrical efficiency |
102:| Plant availability / capacity factor | truly-unknown | **blocking** | No rep-rated IFE driver anywhere near commercial operation; no experimental basis for projecting availability at sub-Hz rates |
103:| Target manufacturing volume and cost trajectory | proprietary | **blocking** | FLF's "consumables business model" depends on mass-manufactured targets; trajectory from bespoke prototype to volume production completely uncharacterized |
117:- **`knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`** — Integrated in §5 as IFE/MIF cost analog. The four ARPA-E ALPHA concepts (Plasma-Jet MIF, Stabilized Liner Compressor, Staged Z-Pinch, Flow-stabilized Z-Pinch) are pulsed-power approaches at ~500 MWe scale costed in a CAS framework. Average LCOE $43/MWh, CapEx $2.4/W, TCC ~$1.2B provide a plausible range anchor for projectile ICF BOP costs. Construction time 3 years (centralized manufacturing). This source downgraded the "BOP capital cost breakdown" gap from **blocking** to **important** — a credible CAS-level analog now exists.
```

## Full unified diff (truncated to 400 lines)

```diff
--- /tmp/gap_phase2_state/22-projectile-icf.md	2026-05-22 12:59:21.078539721 -0700
+++ /home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/22-projectile-icf/gap_report.md	2026-05-22 15:10:34.178911941 -0700
@@ -1,170 +1,167 @@
-I have now read all the available sources. Let me compile the gap assessment.
+I have read all concept-scoped sources and the most relevant fleet-wide sources. Now I'll write the gap assessment report.
 
 # Gap Assessment: Projectile ICF (D-T)
 
 ## Overall Readiness
-**Rating**: Mostly Ready
-**Summary**: First Light Fusion published a peer-reviewed IFE LCOE model (Hawker 2020, PMC7658748) that is specific to this concept and provides a workable 14-parameter framework. The power plant architecture (liquid Li blanket, TBR 1.8, steam Rankine, 333 MWe) is well-documented and has received two independent third-party validations. The blocking constraints for a D1+ analysis are the complete absence of any demonstrated gain and unknown target cost at production scale — both of which the Hawker model treats explicitly as free parameters, making parameterized analysis feasible despite these gaps.
+**Rating**: Significant Gaps
+**Summary**: Taxonomy columns are essentially complete at high confidence, underpinned by First Light Fusion's (FLF) unusually transparent public disclosures before their September 2025 pivot to FLARE. However, the concept is now orphaned — no company is actively pursuing pure projectile ICF — which caps what can be learned from new research. The economic analysis layer is thin: FLF published a peer-reviewed LCOE model (Hawker 2020, co-founder-authored) with technology-agnostic 14-parameter structure and parameter ranges, but all three of the model's most sensitive inputs (target cost, driver cost, capacity factor) are either proprietary or truly unknown because no rep-rated demonstration at fusion-relevant projectile velocities has ever been conducted. A qualitative concept analysis is achievable; a quantitative LCOE model is not credibly constructable without extensive analogy-based assumptions that must be explicitly flagged.
 
 ---
 
 ## Section Coverage
 
 ### 1. Availability of Data
-**Coverage**: Good
+**Coverage**: Partial
+
+**Available**: FLF made unusually detailed public disclosures across its operational lifetime (2011–2025): power plant architecture (333 MWe, liquid Li blanket, steam Rankine), TBR 1.8 independently validated by TUV SUD UK (Feb 2026), tritium surplus projections (25 kg/yr net), driver cost data ($1.7/J for Machine 3, $2/J estimated for FLARE demonstration facility), target LCOE (<$50/MWh, peer-reviewed in Hawker 2020 *Phil. Trans. R. Soc. A*), and fusion demonstration result (April 2022, validated by UKAEA). The IP Group September 2025 press release provides the most recent consolidated technical disclosure including the FLARE pivot rationale. The Hawker 2020 paper (PMC7658748, read as concept-scoped source) is both the primary LCOE framework document and the fleet-wide "A simplified economic model for inertial fusion" — authored by FLF's co-founder, it provides the 14-parameter IFE LCOE model with Monte Carlo analysis showing LCOE as low as $25/MWh under optimistic-but-plausible assumptions. HYLIFE-era ICF plant design data is available via OSTI-6780071 (HYLIFE-II heat transport study, ~1000 MWe, direct capital cost $2,632M excluding IHX) and OSTI-6360934 (EM pumping of liquid Li in ICF, ~800 tonnes Li, flow rates 44–66 m³/s/chamber), providing hardware-level analog data for the liquid-Li blanket subsystem.
 
-**Available**:
-- Peer-reviewed LCOE paper by Nicholas Hawker (First Light co-founder): 14-parameter IFE LCOE model with Monte Carlo analysis, explicit cost anchors from Machine Three ($1.7/J, 2.5 MJ bank), HYLIFE analog ($3600/kWe in 2020 dollars), and competitive LCOE path to <$50/MWh (`pmc-articles-pmc7658748.md`).
-- Fusion milestone press release (April 2022, UKAEA-validated): Confirms 6.5 km/s driver, 70 km/s fuel implosion, 10 TPa, ~50 neutrons, pilot plant target of ~150 MW at <$1B in the 2030s (`prnewswire-first-light-achieves-world-first.md`).
-- TBR validation: TUV SUD UK confirmed TBR = 1.8 for the 333 MWe FLARE/FLF plant geometry (`theengineer-content-news-first-light-fusion-claims-tritium.md`).
-- FLARE pivot announcement (September 2025): Contains cost comparators — demo facility $100M–$200M ($2/J), vs. $6/J for high-intensity pulsed power, $13/J for NIF; energy delivery 1/10th cost of prior fast ignition schemes (`ipgroupplc-news-and-events...2025-09-19.md`).
-- HYLIFE-II plant design (1990 LLNL/UC Davis, OSTI 6780071): Liquid-wall IFE plant with COE model, BOP parameters, Flibe/Li primary loop flows — directly applicable as a plant-architecture analog.
-- HYLIFE EM pumping study (1983 LLNL, OSTI 6360934): Liquid Li EM pump design parameters for ICF reactors — subsystem-level analog.
-
-**Missing**:
-- No published plant study specifically for the pure projectile ICF power plant (distinct from FLARE). The power plant architecture is documented only at a concept level, not as a full system engineering study.
-- No independent cost analysis beyond First Light's own numbers.
-- No NearStar quantitative disclosures beyond press release claims.
+**Missing**: No full conceptual design study for a projectile ICF power plant exists (unlike HYLIFE for liquid-wall ICF or ARIES for MFE). No third-party cost analysis of the FLF concept has been published. NearStar Fusion's MTIF approach is represented in sources but is arguably a separate MIF concept. Post-pivot (Sep 2025), FLF is no longer developing a power plant and is pursuing technology licensing — future public disclosures about commercial plant design are unlikely.
 
 **Gaps**:
-- Independent techno-economic plant study — `not-yet-sourced` — important (would confirm First Light's <$1B pilot claim)
-- Future data: concept has no active commercial pursuer since September 2025 pivot — `truly-unknown` — nice-to-have (no resolution path)
+- No published conceptual design study (power core, BOP, economics in CAS format) — `truly-unknown` — **blocking** for quantitative LCOE model, **important** for qualitative analysis
+- Post-pivot documentation of FLARE plant economics is marketing-level only ($100M–$200M demonstration facility, ~400 MW reactor) without engineering backup — `proprietary` — **important**
+- NearStar MTIF classification ambiguity (MIF vs. IFE) — `derivable` — **nice-to-have** (taxonomy decision upstream)
 
 ---
 
 ### 2. Challenges in Capturing System Function
 **Coverage**: Partial
 
-**Available**:
-- The Hawker 2020 model (`pmc-articles-pmc7658748.md`) explicitly acknowledges the key modeling uncertainties: gain, target cost, driver efficiency, and driver lifetime are all treated as parameters rather than solved quantities. This gives a framework for bounding uncertainty.
-- The power plant architecture downstream of the driver is well-characterized: liquid Li absorbs neutrons/heat, EM pump circulates Li to heat exchanger, steam Rankine cycle. HYLIFE-II provides engineering parameters for analogous systems.
-- The rep rate / available capacity relationship is documented: 30 s between shots (0.033 Hz) at 150 MW pilot; the sub-Hz operation is enabled by high yield per shot.
-
-**Missing**:
-- The target amplification physics (multi-cavity design that accelerates fuel to 70 km/s) is proprietary. The simulation capability is claimed but not published in open literature.
-- Commercial-scale EM gun physics (Machine 4 target: 60 km/s, 100 MJ bank) was never demonstrated — the physics extrapolation from 6.5 km/s (Machine 3) to 60 km/s involves unsolved engineering.
-- Gain has not been demonstrated at any level; the 200–1000 projections are model outputs, not experimental results.
-- Liquid Li dynamics (thermal recovery between shots, curtain reformation timing) are not quantitatively published.
+**Available**: The system architecture is well described at a conceptual level: hypervelocity projectile (6.5 km/s demonstrated, 60+ km/s required for gain) compresses a multi-cavity target, implosion focuses energy to ~10 TPa and <100 µm fuel volume, neutron pulse heats flowing liquid lithium curtain, heat exchanger drives steam Rankine cycle. The target design is the key amplification element — FLF's "controlled amplification technology" boosts projectile impact by >20× through multi-cavity pressure focusing. The system's defining complexity shift relative to laser IFE is moving sophistication from the driver (simple EM gun) to the target (complex multi-cavity design). The Hawker 2020 LCOE model captures the sub-Hz timing constraint (0.033–0.1 Hz) and its effect on economics: lower rep rate enables higher gain requirements but reduces target cost burden. The HYLIFE studies (OSTI sources) document the engineering challenges of liquid-Li-walled ICF chambers including pressure pulse management, EM pump design, and vacuum system requirements.
+
+**Missing**: The gain physics for the projectile ICF approach is fundamentally undemonstrated — FLF achieved ~50 neutrons (fusion, not gain), and the path from this to G=200 is analytically claimed but not validated. The specific amplification mechanism in the multi-cavity target is proprietary IP. The FLARE pivot introduces fast ignition physics (separate compression + ignition stages) as an additional undemonstrated element. Rep-rated operation of an EM gun at fusion-relevant energies (100 MJ scale) is an unresolved engineering problem: Machine 4 (targeting 60 km/s, 100 MJ stored energy) was cancelled in February 2025. The projectile delivery mechanism into the reaction chamber at sub-Hz rates, including reload mechanics for falling-target geometry, has no published engineering analysis.
 
 **Gaps**:
-- Target amplification physics and gain pathway — `proprietary` — blocking (gain is the single most important LCOE driver; Hawker 2020 explicitly states "gain of at least 200 needed for commercial competitiveness")
-- EM gun scaling from 6.5 km/s to 60 km/s — `truly-unknown` (Machine 4 cancelled before this was addressed) — blocking for driver cost modeling
-- Li curtain dynamics at sub-Hz rep rate — `not-yet-sourced` (HYLIFE papers may contain partial analog data) — important
+- Gain physics validation gap: current demonstrated result (~50 neutrons) is far below commercial-minimum G=200; path to gain undemonstrated and unverified — `truly-unknown` — **blocking**
+- Rep-rated EM gun operation at 60+ km/s projectile velocity: no precedent, Machine 4 cancelled — `truly-unknown` — **blocking**
+- Target amplification mechanism details: proprietary, published only as "multi-cavity" concept without geometry or material specifics — `proprietary` — **important**
+- FLARE fast-ignition integration with projectile compression: described only in white paper without physics calculation disclosure — `proprietary` — **important**
 
 ---
 
 ### 3. Maturity of Key Subsystems and Components
 **Coverage**: Partial
 
-**Available**:
-- **Driver (EM gun)**: Machine 3 (two-stage gas gun, 6.5 km/s, 2.5 MJ, $4.3M) demonstrated and costed. TRL ~3 for commercial-scale projectile driver.
-- **Target**: Fusion demonstrated (April 2022, ~50 neutrons, UKAEA validated). Target physics simulation capability claimed. TRL ~3–4 for target physics; TRL ~1–2 for mass-manufactured target production.
-- **Liquid Li blanket**: TBR = 1.8 validated analytically by TUV SUD UK (February 2026). No hardware demonstration. HYLIFE-I/II provide engineering analog. TRL ~3.
-- **BOP (steam Rankine)**: Mature industrial technology. TRL 9. First Light explicitly cites "150-year-old steam turbine technology."
-- **EM pumping**: 1983 HYLIFE LLNL report provides detailed EM pump design for Li at relevant flow rates (8.08 m³/s at 82.5 kPa). Hardware analogs exist (sodium pumps validated). TRL ~5 for this subsystem class.
-
-**Missing**:
-- No TRL assessment for rep-rated EM gun (reload and firing cycle, barrel wear at sub-Hz rates).
-- No experimental data on target fabrication at production scale or cost per unit.
-- No hardware prototype of the liquid Li reaction chamber at scale.
+**Available**: FLF provided TRL-relevant milestones in public disclosures: Machine 3 achieved 6.5 km/s projectile velocity (TRL 4–5 for sub-fusion-scale EM launcher), fusion neutrons detected and validated by UKAEA (April 2022, TRL 3–4 for target physics at fusion conditions), TBR 1.8 validated by TUV SUD UK via neutronics modeling (Feb 2026, TRL 4 for blanket design validation). The steam Rankine cycle (TRL 9) is standard existing technology. Liquid Li blanket technology has been studied at TRL 3–5 in HYLIFE program. The Wurzel & Hsu (2021) Lawson criterion compilation in the project's meta-analysis (`knowledge/meta_analysis/progress_toward_fusion_breakeven_lawson_criterion/`) would independently benchmark FLF's neutron yield against the broader IFE field, though this source was not read in detail.
+
+**Missing**: No TRL assessment has been published for the rep-rated EM gun system. Machine 4 (which would have been the gain-scale driver) was cancelled. The overall system TRL for gain-capable projectile ICF is approximately TRL 2–3 (concept and analytical credibility established, single-shot fusion demonstrated, no integrated gain experiment). The specific TRL for mass-manufactured targets is unknown — current targets are individually fabricated prototypes costing far more than the $1–100/target range the Hawker model requires for competitive LCOE.
 
 **Gaps**:
-- Rep-rated EM gun / barrel lifetime — `truly-unknown` — blocking (driver shot lifetime `Nd` is a key LCOE parameter)
-- Production-scale target fabrication — `truly-unknown` — blocking (target cost `δ` is a key LCOE parameter)
-- Integrated chamber experiments (Li curtain + target + driver) — `truly-unknown` — important
+| Subsystem | Available TRL | Gaps |
+|-----------|--------------|------|
+| EM gun driver (gain-scale, rep-rated) | TRL 2–3 | No rep-rated gain-scale machine existed; Machine 4 cancelled — `truly-unknown` |
+| Target design (gain-capable) | TRL 2–3 | Gain-positive target never demonstrated; proprietary geometry — `proprietary` |
+| Liquid Li blanket (operational) | TRL 3–4 | Neutronics validated, no dynamic operational testing — `not-yet-sourced` |
+| Steam Rankine + BOP | TRL 9 | No gaps |
+| Tritium processing | TRL 4–5 | Analogous to MFE programs; FLF claims 1-week self-sufficiency — `derivable` |
+| Target manufacturing at scale | TRL 1–2 | No manufacturing process defined; key business model uncertainty — `proprietary` |
 
 ---
 
 ### 4. Key Materials and Supply Chain Considerations
 **Coverage**: Partial
 
-**Available**:
-- **Lithium**: Natural lithium (not enriched) sufficient per TBR = 1.8 result. First Light cites $70M/reactor for natural Li, vs. $143M–$451M for enriched alternatives (`ipgroupplc-news-and-events...2025-09-19.md`). This is a significant cost advantage over concepts requiring Li-6 enrichment.
-- **Tritium**: D-T fuel cycle with self-sufficient breeding claimed within one week of operation. Net surplus of 25 kg/year at 333 MWe — potential revenue stream at $30,000/g. Global tritium stock ~20 kg is not a blocking constraint given TBR = 1.8.
-- **Steel / conventional materials**: First Light's power plant explicitly relies on conventional materials post-chamber; no advanced materials R&D required for BOP.
-- **Target materials**: Current targets are complex multi-layer structures (few-mm fuel capsule within a multi-cavity amplifier). Materials not publicly disclosed. Currently bespoke prototypes.
-
-**Missing**:
-- Target material composition and manufacturing bill-of-materials are proprietary.
-- EM gun barrel materials at 60 km/s launch velocity — not documented for projectile ICF.
-- Chamber wall materials under long-term liquid Li exposure — HYLIFE provides partial analog but for Flibe, not pure Li.
+**Available**: Liquid lithium is the dominant material concern. FLF explicitly costed natural lithium at ~$70M per reactor (vs. $143M–$451M for enriched Li-6 alternatives), confirming a natural Li design that avoids isotopic enrichment bottlenecks. The TBR 1.8 result means tritium self-sufficiency in as little as one week and a net surplus of 25 kg/yr at 333 MWe — substantially reducing tritium procurement complexity vs. other D-T concepts. HYLIFE-II design used ~800–960 tonnes of Flibe/liquid Li as blanket inventory (comparable scale). The EM gun uses conventional electromagnetic engineering materials (copper windings, structural steel, high-strength barrel materials). FLF explicitly claimed COTS technology reliance for the driver ("existing technologies," "existing supply chains"). The steam turbine supply chain is standard.
+
+**Missing**: Target material composition is entirely proprietary — the multi-cavity target design is FLF's core IP and its material requirements are not disclosed. Barrel erosion rates for the EM gun at fusion-relevant kinetic energies are unknown (no rep-rated high-velocity EM gun exists at this scale). Lithium metal at the 800+ tonne scale per plant would stress current lithium supply chains; no supply analysis specific to projectile ICF has been published.
 
 **Gaps**:
-- Target bill-of-materials — `proprietary` — important (sets floor on target cost)
-- EM gun barrel materials/wear at commercial scale — `truly-unknown` — important
-- Long-term Li compatibility with chamber wall materials — `not-yet-sourced` (search HYLIFE literature and LLNL liquid-metal materials studies) — important
+- Target material composition and supply chain: entirely proprietary — `proprietary` — **important**
+- EM gun barrel erosion/lifetime at 0.033+ Hz rep rate and >60 km/s projectile velocity: no experimental data — `truly-unknown` — **important**
+- Lithium supply chain stress analysis for multi-plant deployment: no published analysis for this concept — `not-yet-sourced` — **nice-to-have**
 
 ---
 
 ### 5. LCOE Parameter Extraction
-**Coverage**: Partial
-
 **Available Parameters**:
 | Parameter | Value/Range | Source | Confidence |
 |-----------|-------------|--------|------------|
-| LCOE target | <$50/MWh | Hawker 2020 (pmc7658748) | medium |
-| Plant cost constant (α) | $3600/kWe (HYLIFE analog, 2020$) | Hawker 2020 | medium |
-| Driver cost constant (γ) | $1.7/J (Machine 3, prototype, non-rep-rated) | Hawker 2020 | low (prototype, not commercial) |
-| Driver energy (Ed) | 2.5 MJ (Machine 3); ~100 MJ (Machine 4 target, cancelled) | prnewswire 2022 / dossier | low for commercial scale |
-| Repetition rate (f) | 0.033 Hz (1 shot/30 s) at 150 MW | prnewswire 2022 | medium |
-| Net electrical output | 333 MWe (FLARE design point) | theengineer TBR article | medium |
-| Gain threshold (commercial) | ≥200 | ipgroupplc 2025, Hawker 2020 | medium |
-| Thermal efficiency | ~35–40% (steam Rankine, sub-critical) | HYLIFE-II analog (osti-6780071) | medium |
-| TBR | 1.8 | theengineer article, TUV SUD UK validated | high |
-| Li cost | $70M/reactor (natural Li) | ipgroupplc 2025 | medium |
-| Pilot plant capital | ~$1B, 150 MW | prnewswire 2022 | low (aspirational) |
-| Demo facility cost | $100M–$200M ($2/J) | ipgroupplc 2025 | medium |
-| O&M cost (ε) | $10–$100/kWe-yr (bounds from Hawker 2020) | Hawker 2020 | low (bounding only) |
-| Construction time | 5 years | Hawker 2020 | medium |
-| Plant lifetime | 40 years | Hawker 2020 | medium |
-| Availability | Parameter in model; no concept-specific estimate | Hawker 2020 | low |
+| Net electric output | 333 MWe (commercial); ~150 MWe (pilot) | IP Group/FLF press release Sep 2025; PRNewswire Apr 2022 | m |
+| Target gain (commercial minimum) | G ≥ 200; G = 1000 (target) | FLF FLARE white paper, IP Group Sep 2025 | m |
+| Repetition rate | 0.033 Hz (30 s/shot, pilot); 0.1 Hz (10 s/shot, 500 MW) | PRNewswire Apr 2022 | m-l (conflicting figures across sources) |
+| Driver cost (non-rep-rated Machine 3) | $1.7/J (2.5 MJ bank, $4.3M cost) | Hawker 2020, PMC7658748 | m |
+| FLARE demonstration facility cost | $100M–$200M at ~$2/J stored energy | IP Group news Sep 2025 | m |
+| Tritium breeding ratio | 1.8 (independently validated) | The Engineer / TUV SUD UK, Feb 2026 | h |
+| Thermal conversion cycle | Steam Rankine; standard existing BOP | FLF technology pages; PRNewswire Apr 2022 | h |
+| Li blanket cost (materials) | ~$70M natural Li per reactor | IP Group Sep 2025 | m |
+| Target LCOE objective | <$50/MWh | Hawker 2020 (Phil Trans R Soc 2020) | m |
+| Plant cost analog (HYLIFE) | ~$3,600/kWe (2020$); $2,632M total direct capital for single-chamber ~1000 MWe | Hawker 2020; OSTI-6780071 | m-l (dated analog) |
+| ARPA-E modular IFE/MIF LCOE analog | $43/MWh avg ($34–54 range); $2.4/W CapEx; ~$1.2B TCC for ~500 MWe | `knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/` | m (different driver technologies) |
+| Blanket energy multiple | 0.6–1.4 | Hawker 2020 | m |
+| Yield cost bound (Li-based) | $70k–$44M/GJ | Hawker 2020 | m |
+| Driver cost range (IFE analogs) | $1.7–$9.5/J (Machine 3 to NIF) | Hawker 2020 | m |
+| O&M cost range (IFE analogs) | $10–100/kWe-yr | Hawker 2020 | m |
+| Thermal efficiency (expected range) | 30–60% | Hawker 2020 | m |
 
 **Missing Parameters**:
 | Parameter | Gap Type | Criticality | Notes |
 |-----------|----------|-------------|-------|
-| Target gain G (achieved) | truly-unknown | blocking | No gain experiment conducted; G ≥ 200 needed for commercial competitiveness; single largest LCOE driver |
-| Target cost (δ, $/target at production scale) | truly-unknown | blocking | Explicitly treated as free parameter in Hawker 2020; bespoke prototypes only |
-| Driver efficiency (wall-plug to target) | proprietary | blocking | Not disclosed; sets recirculating power fraction |
-| Driver lifetime Nd (shots before replacement) | truly-unknown | blocking | Machine 3 shot count not published; sub-Hz rep rate means replacement frequency is tractable but unknown |
-| EM gun commercial-scale cost | truly-unknown | blocking | Machine 4 (100 MJ, 60 km/s) cancelled; no cost data for commercial-scale driver |
-| Yield per shot (Ef) | truly-unknown | important | Not demonstrated; derivable from gain + driver energy once gain is known |
-| Blanket multiple | derivable | important | Derivable from TBR = 1.8 and tritium self-sufficiency requirement |
-| Capacity factor / availability | not-yet-sourced | important | Sub-Hz rep rate simplifies scheduling maintenance; analogues from pulsed facilities |
-| CAS-level capital cost breakdown | not-yet-sourced | important | Hawker model bundles into α ($/kWe); no CAS10-structured breakdown published |
+| Target cost per shot (manufacturing at scale) | proprietary | **blocking** | Hawker 2020 identifies target cost as a top-3 LCOE driver; FLF's target is core IP; current prototype costs are irrelevant; required range is $1–100/target |
+| Rep-rated EM gun driver capital cost | truly-unknown | **blocking** | Machine 4 (100 MJ, 60 km/s) was cancelled; no rep-rated gain-scale EM gun exists anywhere; Machine 3 cost ($1.7/J) is for non-rep-rated device |
+| Driver efficiency (wall-plug to kinetic energy) | proprietary/derivable | **blocking** | Critical for recirculating power fraction; Machine 3 specs (6.5 km/s, 2.5 MJ bank) do not disclose electrical efficiency |
+| Plant availability / capacity factor | truly-unknown | **blocking** | No rep-rated IFE driver anywhere near commercial operation; no experimental basis for projecting availability at sub-Hz rates |
+| Target manufacturing volume and cost trajectory | proprietary | **blocking** | FLF's "consumables business model" depends on mass-manufactured targets; trajectory from bespoke prototype to volume production completely uncharacterized |
+| EM gun driver lifetime (shots to replacement) | truly-unknown | **important** | Hawker 2020 shows driver lifetime is a significant LCOE sensitivity; no data for rep-rated EM guns |
+| O&M (EM gun maintenance, Li system) | truly-unknown | **important** | No published O&M data for projectile ICF; Hawker model range ($10–100/kWe-yr) spans an order of magnitude |
+| BOP capital cost breakdown (by CAS account) | derivable | **important** | Rankine cycle BOP can be estimated from ARPA-E ALPHA Revisit ($43/MWh, $2.4/W) but no concept-specific CAS breakdown |
+| Decommissioning cost | derivable | nice-to-have | Analogous to IFE programs |
 
 ---
 
 ## Source Recommendations
 
-- **Hawker 2020 IFE LCOE model** (`knowledge/concept_research/22-projectile-icf/iter-03/sources/pmc-articles-pmc7658748.md`) — already sourced; this is the primary quantitative framework. Read the full paper for Monte Carlo parameter distributions.
-- **HYLIFE-II heat transport and COE study** (`knowledge/concept_research/22-projectile-icf/iter-03/sources/osti-servlets-purl-6780071.md`) — already sourced; read fully for COE formula, BOP parameters, and IHX cost scaling — directly analogous to First Light's liquid-wall plant architecture.
-- **Fleet-wide analog: `knowledge/sources/a_simplified_economic_model_for_inertial_fusion/`** — same paper as pmc7658748 (Hawker 2020 is registered fleet-wide). Use the fleet-wide extract if it's higher quality than the concept-scoped extraction.
-- **Fleet-wide analog: `knowledge/sources/energy_from_inertial_fusion/`** — 1992 IAEA IFE review; covers light-ion and projectile-class driver concepts and may contain driver efficiency or target cost estimates applicable as bounding values. Worth skimming the driver technology chapter. `unverified — confirm existence before searching`.
-- **Search OSTI for HYLIFE liquid-lithium materials compatibility studies** — for chamber wall lifetime under liquid Li exposure. Search terms: "HYLIFE lithium corrosion first wall" or "liquid lithium compatibility structural material ICF." `not-yet-sourced`.
-- **First Light Fusion white paper on FLARE (September 2025)** — cited in the FLARE pivot press releases but not yet ingested. Contains detailed gain model and power plant architecture data that would fill several important gaps. URL: `https://firstlightfusion.com/flare/`. Priority: high. `not-yet-sourced`.
-- **PyFECONS** (`/home/reid/PyFECONS`) — if it implements IFE CAS cost accounting, could be used to generate a CAS-structured cost breakdown analogous to this concept's plant. Check whether it handles liquid-wall IFE configurations.
+**Integration notes (fleet-wide sources read and integrated):**
+
+- **`knowledge/sources/a_simplified_economic_model_for_inertial_fusion/` (Hawker 2020)** — Integrated throughout §5. This is the co-founder's peer-reviewed LCOE model (PMC7658748, also present as concept-scoped source). It directly addresses the methodology gap and provides bounding ranges for all 14 LCOE parameters. It confirms target cost and gain as the dominant cost levers at sub-Hz rep rates, grounding the blocking/important gap classification above. The Monte Carlo finding that LCOE <$25/MWh is achievable with G>500 and yield>5 GJ directly characterizes the FLF design point economics.
+
+- **`knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`** — Integrated in §5 as IFE/MIF cost analog. The four ARPA-E ALPHA concepts (Plasma-Jet MIF, Stabilized Liner Compressor, Staged Z-Pinch, Flow-stabilized Z-Pinch) are pulsed-power approaches at ~500 MWe scale costed in a CAS framework. Average LCOE $43/MWh, CapEx $2.4/W, TCC ~$1.2B provide a plausible range anchor for projectile ICF BOP costs. Construction time 3 years (centralized manufacturing). This source downgraded the "BOP capital cost breakdown" gap from **blocking** to **important** — a credible CAS-level analog now exists.
+
+- **`knowledge/sources/affordable_manageable_practical_and_scalable_amps_high/`** — Read. Pacific Fusion's MagLIF-based pulser IFE is a different physical approach (electromagnetically driven liner compression vs. hypervelocity projectile impact), but §4 of the AMPS paper addresses engineering requirements for commercial power (component lifetime, chamber maintenance, tritium breeding) at a similar technology readiness level. The AMPS paper does not provide explicit commercial plant cost figures in the sections read. Does not resolve any blocking gaps for projectile ICF given driver technology difference. Classified as contextual analog only — does not change gap criticality ratings.
+
+**Disqualifications (fleet-wide sources reviewed and ruled out):**
+
+- **`knowledge/sources/energy_from_inertial_fusion/`** — The 1992 IAEA review covers laser, heavy-ion, and light-ion IFE driver concepts. The hypervelocity EM-launcher approach pioneered by First Light Fusion (founded 2011) postdates this review entirely; it contains no projectile/EM-gun driver cost content and its 1992 target cost and driver efficiency data do not translate to a 2030s projectile ICF design. Disqualified.
+
+- **`knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/`** — Heavy-ion driver economics are dominated by accelerator cost scaling (cost per Joule scales with accelerator length and current). The EM gun driver in projectile ICF has a fundamentally different cost structure (pulsed energy storage, barrel replacement, projectile manufacturing) that does not map to HIF accelerator scaling. Disqualified.
+
+- **`knowledge/sources/tea_dt_mfe_cost_analysis/`** — D-T MFE (tokamak) cost methodology. Confinement architecture is incompatible with projectile ICF cost structure; steady-state plasma assumptions, magnet costs, and plasma heating system costs do not apply. BOP costs (steam Rankine) are already covered by ARPA-E ALPHA Revisit and HYLIFE-II. Disqualified.
+
+- **`knowledge/sources/aries_cost_account_documentation/`** — CAS framework reference. The CAS account structure (20–27 direct, 90–98 indirect) is already represented in the ARPA-E ALPHA Revisit which applies this framework to compact modular concepts comparable to projectile ICF in scale and development stage. No marginal value beyond what ARPA-E ALPHA Revisit provides. Disqualified.
+
+- **`knowledge/sources/commercialization_of_laser_fusion_energy/`** — Xcimer Energy's KrF excimer laser IFE whitepaper. Laser driver cost breakdown is specific to optical systems (~$100/J laser capital cost); this does not translate to EM gun drivers. Chamber and BOP analogy is marginal given the already available ARPA-E ALPHA Revisit. Disqualified.
+
+- **`knowledge/sources/overview_of_the_helios_design_a_practical_planar_coil/`** — Stellarator (MFE). Different confinement family. Disqualified.
+
+- **`knowledge/sources/an_assessment_of_the_economics_of_future_electric_power/`** — ORNL historical benchmarking of fusion LCOE against competing electricity sources. No concept-specific content for projectile ICF. Disqualified.
+
+**Not-yet-sourced gaps — search recommendations:**
+
+1. **Rep-rated electromagnetic launcher performance data**: Search OSTI for "electromagnetic launcher repetition rate inertial fusion" and "railgun repetition rate pulsed power" — legacy LLNL HYLIFE-era work may exist. Search IEEE Transactions on Plasma Science for EM launcher survivability. Flag: `unverified — confirm existence before searching`.
+2. **Target manufacturing cost trajectory for IFE**: Search OSTI for "IFE target fabrication cost" or "laser target mass production" — NIF target program has published cost analyses which could anchor the lower bound for FLF's projectile targets. Flag: `unverified`.
+3. **First Light Fusion grant applications or UKAEA program documents**: UK EPSRC, UKAEA Fusion Industry Program, and InnovateUK may have public project summaries with engineering specification data. Flag: `unverified`.
+4. **HYLIFE IFE reactor design study (Moir et al., 1990)** — Referenced multiple times in OSTI-6780071; the full HYLIFE design study would provide a complete CAS-level cost model for liquid-Li-walled ICF that is the closest analog to First Light's power plant architecture. Search OSTI for "HYLIFE reactor design" and "Moir 1990." Flag: `unverified — confirm existence before searching`.
 
 ---
 
 ## Summary
 
-The data is sufficient to proceed to a D1+ qualitative analysis and a parameterized LCOE model, but not to a high-confidence quantitative estimate. The Hawker 2020 peer-reviewed LCOE model (authored by First Light's co-founder) provides the analytical framework; the 14-parameter structure was specifically designed for cases like this where gain and target cost are unknown. The power plant architecture is well-documented at a concept level, two independent third-party validations exist (UKAEA for physics, TUV SUD UK for TBR), and cost anchors exist for the driver and plant.
+Proceed to full qualitative analysis with caveats. The concept's technology description, system architecture, and taxonomy classification are well-supported by an unusually detailed public record from First Light Fusion. A D1+ analysis can credibly cover sections 1–4 and partial section 5. However, a standalone quantitative LCOE model for Projectile ICF (D-T) is not constructable from available data: the three most LCOE-sensitive parameters (target cost per shot, rep-rated driver capital cost, capacity factor) are either proprietary to a company that has since pivoted or genuinely unknown because no rep-rated gain-scale projectile ICF driver has ever existed. Any quantitative LCOE estimate must explicitly use Hawker 2020's 14-parameter bounding framework and flag the result as "parameter-space exploration" rather than a design-point projection. The ARPA-E ALPHA Revisit ($34–54/MWh range for comparable-scale compact pulsed IFE) provides a useful independent cross-check.
 
-The five blocking gaps — demonstrated gain, production-scale target cost, driver efficiency, commercial-scale driver cost, and driver shot lifetime — are all genuinely unknown and cannot be resolved from public sources. They should be treated as uncertainty parameters in the LCOE model rather than waiting for resolution. The FLARE white paper (not yet ingested) is the single highest-value missing source and should be acquired before writing the full analysis.
+The concept's orphaned status (no active commercial pursuer since Sep 2025) means additional research iterations are unlikely to close the economic gaps — the data simply was never published and the company has changed direction. A follow-up gap with NearStar Fusion may warrant a separate MIF concept row rather than inclusion here.
 
 ---
 
 ## Structured summary (machine-readable)
 
 ```yaml
-overall_rating: "Mostly Ready"
+overall_rating: "Significant Gaps"
 blocking_count: 5
-important_count: 7
-counting_method: "section_5_missing_parameters (5 blocking) plus sections 1-4 gaps classified blocking/important, deduplicated across all sections"
+important_count: 5
+counting_method: "unique_thematic_gaps_deduplicated_across_all_sections: (1) gain demonstration gap, (2) rep-rated EM gun driver performance/cost, (3) target manufacturing cost per shot, (4) plant availability/capacity factor, (5) driver efficiency; important: (1) target design details, (2) EM gun lifetime/O&M, (3) system-level O&M costs, (4) BOP CAS cost breakdown, (5) target supply chain"
 section_coverage:
-  availability_of_data:       "Good"
+  availability_of_data:       "Partial"
   system_function:            "Partial"
   subsystem_maturity:         "Partial"
   materials_supply_chain:     "Partial"
-  lcoe_parameter_extraction:  "Partial"
+  lcoe_parameter_extraction:  "Poor"
 ```
\ No newline at end of file
```
