# Diff: 22-projectile-icf

**Generated:** 2026-05-22T10:48:15-07:00

## Counts

| field | baseline | new | Δ |
|-------|----------|-----|---|
| blocking_count   | 7 | 5 | -2 |
| important_count  | 6 | 7 | - |
| overall_rating   | Mostly Ready (with important caveats) | Mostly Ready | - |

## Fleet-source citations (new only — grep `knowledge/sources/` or `PyFECONS`)

```
141:- **Fleet-wide analog: `knowledge/sources/a_simplified_economic_model_for_inertial_fusion/`** — same paper as pmc7658748 (Hawker 2020 is registered fleet-wide). Use the fleet-wide extract if it's higher quality than the concept-scoped extraction.
142:- **Fleet-wide analog: `knowledge/sources/energy_from_inertial_fusion/`** — 1992 IAEA IFE review; covers light-ion and projectile-class driver concepts and may contain driver efficiency or target cost estimates applicable as bounding values. Worth skimming the driver technology chapter. `unverified — confirm existence before searching`.
145:- **PyFECONS** (`/home/reid/PyFECONS`) — if it implements IFE CAS cost accounting, could be used to generate a CAS-structured cost breakdown analogous to this concept's plant. Check whether it handles liquid-wall IFE configurations.
```

## Blocking-tier lines (baseline)

```
53:- Driver wall-plug efficiency — `proprietary` — **blocking** for LCOE model (determines recirculating power; must be assumed)
54:- Target amplifier physics detail — `proprietary` — **blocking** for gain credibility assessment (must use stated range with large uncertainty)
55:- Demonstrated Q or credible Q roadmap — `not-yet-sourced` / `truly-unknown` — **blocking** (search for any First Light arxiv papers on target compression physics; `unverified — confirm existence before searching`)
76:- Target fabrication at commercial rep rate — `proprietary` — **blocking** (no information on target manufacturing process, cost, or scalability)
77:- EM driver scaling pathway (6.5 → 60 km/s) — `not-yet-sourced` / `truly-unknown` — **blocking** (Machine 4 was cancelled; this problem is unresolved)
99:- Target production volume and manufacturing process — `proprietary` — **blocking** for operating cost model (target cost/shot is often the dominant IFE operating cost)
131:| Capital cost by subsystem (CAS breakdown) | proprietary | blocking | Only total cost targets stated; no subsystem breakdown |
132:| Driver (EM gun) capital cost | proprietary | blocking | No figure for the projectile driver specifically |
133:| Target cost per shot | proprietary | blocking | Most sensitive IFE operating cost; entirely unknown |
134:| Annual target production volume | derivable | blocking | Derivable from rep rate × hours/year |
135:| Driver wall-plug efficiency | proprietary | blocking | Determines recirculating power fraction |
136:| Recirculating power (gross→net) | derivable | blocking | Need driver efficiency first; else must assume |
138:| Q (target fusion gain, demonstrated) | truly-unknown | blocking | Machine 3 achieved Q<<1; commercial needs 200–1000× |
```

## Blocking-tier lines (new)

```
125:| Target gain G (achieved) | truly-unknown | blocking | No gain experiment conducted; G ≥ 200 needed for commercial competitiveness; single largest LCOE driver |
126:| Target cost (δ, $/target at production scale) | truly-unknown | blocking | Explicitly treated as free parameter in Hawker 2020; bespoke prototypes only |
127:| Driver efficiency (wall-plug to target) | proprietary | blocking | Not disclosed; sets recirculating power fraction |
128:| Driver lifetime Nd (shots before replacement) | truly-unknown | blocking | Machine 3 shot count not published; sub-Hz rep rate means replacement frequency is tractable but unknown |
129:| EM gun commercial-scale cost | truly-unknown | blocking | Machine 4 (100 MJ, 60 km/s) cancelled; no cost data for commercial-scale driver |
```

## Full unified diff (truncated to 400 lines)

```diff
--- /tmp/gap_baselines_2026-05-22/22-projectile-icf.md	2026-05-22 09:21:13.868197019 -0700
+++ /home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/22-projectile-icf/gap_report.md	2026-05-22 10:48:15.916460842 -0700
@@ -1,35 +1,34 @@
-Now I have everything I need. Let me write the assessment.
-
----
+I have now read all the available sources. Let me compile the gap assessment.
 
 # Gap Assessment: Projectile ICF (D-T)
 
 ## Overall Readiness
-**Rating**: Mostly Ready (with important caveats)
-**Summary**: First Light Fusion's extensive public disclosures provide enough architecture, performance targets, and cost anchors for a credible qualitative analysis and first-pass LCOE model. However, this concept has a fundamental structural problem: it has no active commercial pursuer (First Light pivoted to FLARE in Sept 2025; NearStar is properly MIF, not projectile ICF). The qualitative write-up must lead with this context. Quantitative modeling is feasible but will be heavily assumption-driven — subsystem cost breakdown data is absent, driver efficiency is unpublished, and the claimed gain (200–1000×) has never been demonstrated, creating compounding physics-to-cost uncertainty.
+**Rating**: Mostly Ready
+**Summary**: First Light Fusion published a peer-reviewed IFE LCOE model (Hawker 2020, PMC7658748) that is specific to this concept and provides a workable 14-parameter framework. The power plant architecture (liquid Li blanket, TBR 1.8, steam Rankine, 333 MWe) is well-documented and has received two independent third-party validations. The blocking constraints for a D1+ analysis are the complete absence of any demonstrated gain and unknown target cost at production scale — both of which the Hawker model treats explicitly as free parameters, making parameterized analysis feasible despite these gaps.
 
 ---
 
 ## Section Coverage
 
 ### 1. Availability of Data
-**Coverage**: Moderate
+**Coverage**: Good
 
 **Available**:
-- First Light Fusion published a substantial body of technical and commercial detail between 2011–2025, captured across all four source documents. This includes power plant architecture, TBR data (independently validated), cost targets, rep rate ranges, plant size targets, and the strategic pivot narrative.
-- First Light stated LCOE target (<$50/MWh), pilot plant cost target (<$1B for 150 MWe), and commercial plant cost (<$5B for ~500 MWe) — rare top-line cost disclosures for a fusion startup (`first-light-fusion-technology.md`).
-- TBR 1.8 was independently verified by TÜV SÜD UK (Feb 2026), giving the tritium breeding claim unusual credibility.
-- NearStar's public disclosures are thinner but captured (`nearstar-fusion-technology.md`, `nearstar-fusion-2025-update.md`): driver specs, fuel preference, modularity pitch, and funding stage.
+- Peer-reviewed LCOE paper by Nicholas Hawker (First Light co-founder): 14-parameter IFE LCOE model with Monte Carlo analysis, explicit cost anchors from Machine Three ($1.7/J, 2.5 MJ bank), HYLIFE analog ($3600/kWe in 2020 dollars), and competitive LCOE path to <$50/MWh (`pmc-articles-pmc7658748.md`).
+- Fusion milestone press release (April 2022, UKAEA-validated): Confirms 6.5 km/s driver, 70 km/s fuel implosion, 10 TPa, ~50 neutrons, pilot plant target of ~150 MW at <$1B in the 2030s (`prnewswire-first-light-achieves-world-first.md`).
+- TBR validation: TUV SUD UK confirmed TBR = 1.8 for the 333 MWe FLARE/FLF plant geometry (`theengineer-content-news-first-light-fusion-claims-tritium.md`).
+- FLARE pivot announcement (September 2025): Contains cost comparators — demo facility $100M–$200M ($2/J), vs. $6/J for high-intensity pulsed power, $13/J for NIF; energy delivery 1/10th cost of prior fast ignition schemes (`ipgroupplc-news-and-events...2025-09-19.md`).
+- HYLIFE-II plant design (1990 LLNL/UC Davis, OSTI 6780071): Liquid-wall IFE plant with COE model, BOP parameters, Flibe/Li primary loop flows — directly applicable as a plant-architecture analog.
+- HYLIFE EM pumping study (1983 LLNL, OSTI 6360934): Liquid Li EM pump design parameters for ICF reactors — subsystem-level analog.
 
 **Missing**:
-- Peer-reviewed publications on projectile ICF gain physics (First Light published some target physics work; these are not captured in Phase 1a sources)
-- Any independent plant study or system code output for the projectile ICF concept
-- Published techno-economic analysis from any third party
+- No published plant study specifically for the pure projectile ICF power plant (distinct from FLARE). The power plant architecture is documented only at a concept level, not as a full system engineering study.
+- No independent cost analysis beyond First Light's own numbers.
+- No NearStar quantitative disclosures beyond press release claims.
 
 **Gaps**:
-- Peer-reviewed target physics papers — `not-yet-sourced` — important (would constrain gain credibility)
-- Independent TEA or LCOE study — `truly-unknown` — nice-to-have (unlikely to exist; concept is abandoned)
-- Active commercial development data post-pivot — `truly-unknown` — blocking for near-term commercial projections (concept is orphaned)
+- Independent techno-economic plant study — `not-yet-sourced` — important (would confirm First Light's <$1B pilot claim)
+- Future data: concept has no active commercial pursuer since September 2025 pivot — `truly-unknown` — nice-to-have (no resolution path)
 
 ---
 
@@ -37,45 +36,42 @@
 **Coverage**: Partial
 
 **Available**:
-- The system architecture is well described: EM gun driver → hypervelocity projectile → proprietary amplifier target → D-T implosion → liquid Li neutron absorption/tritium breeding → steam Rankine BOP. This chain is sufficient to structure an LCOE model.
-- The gain requirement (200–1000×) is stated and its commercial significance explained.
-- The "decoupled" nature of driver and BOP is clearly articulated: "after the lithium heat exchanger, the plant is identical to many other already working facilities."
-- The abandonment of Machine 4 (which would have been the gain-demonstration machine at 60 km/s / 100 MJ) is documented — this is the key physics gap that killed the concept.
+- The Hawker 2020 model (`pmc-articles-pmc7658748.md`) explicitly acknowledges the key modeling uncertainties: gain, target cost, driver efficiency, and driver lifetime are all treated as parameters rather than solved quantities. This gives a framework for bounding uncertainty.
+- The power plant architecture downstream of the driver is well-characterized: liquid Li absorbs neutrons/heat, EM pump circulates Li to heat exchanger, steam Rankine cycle. HYLIFE-II provides engineering parameters for analogous systems.
+- The rep rate / available capacity relationship is documented: 30 s between shots (0.033 Hz) at 150 MW pilot; the sub-Hz operation is enabled by high yield per shot.
 
 **Missing**:
-- Driver wall-plug efficiency: how much grid electricity is consumed per shot to accelerate the projectile? Not disclosed anywhere in the sources.
-- Recirculating power fraction: closely related to driver efficiency; absent.
-- Fusion-energy-to-driver-energy coupling path: what fraction of fusion yield is captured vs. lost?
-- Target physics credibility: the "amplifier" that converts 6.5 km/s projectile to >70 km/s internal fuel velocity is entirely proprietary. The physics of this gain mechanism is the central uncertainty and not described in enough detail to evaluate.
-- Demonstrated Q: First Light achieved fusion (neutrons detected) but never Q>1. The gap between Q<0.001 (demonstrated) and Q=200–1000 (commercial claim) is enormous and unvalidated.
+- The target amplification physics (multi-cavity design that accelerates fuel to 70 km/s) is proprietary. The simulation capability is claimed but not published in open literature.
+- Commercial-scale EM gun physics (Machine 4 target: 60 km/s, 100 MJ bank) was never demonstrated — the physics extrapolation from 6.5 km/s (Machine 3) to 60 km/s involves unsolved engineering.
+- Gain has not been demonstrated at any level; the 200–1000 projections are model outputs, not experimental results.
+- Liquid Li dynamics (thermal recovery between shots, curtain reformation timing) are not quantitatively published.
 
 **Gaps**:
-- Driver wall-plug efficiency — `proprietary` — **blocking** for LCOE model (determines recirculating power; must be assumed)
-- Target amplifier physics detail — `proprietary` — **blocking** for gain credibility assessment (must use stated range with large uncertainty)
-- Demonstrated Q or credible Q roadmap — `not-yet-sourced` / `truly-unknown` — **blocking** (search for any First Light arxiv papers on target compression physics; `unverified — confirm existence before searching`)
-- Recirculating power fraction — `derivable` — important (can be estimated from gain × driver efficiency with stated assumptions)
+- Target amplification physics and gain pathway — `proprietary` — blocking (gain is the single most important LCOE driver; Hawker 2020 explicitly states "gain of at least 200 needed for commercial competitiveness")
+- EM gun scaling from 6.5 km/s to 60 km/s — `truly-unknown` (Machine 4 cancelled before this was addressed) — blocking for driver cost modeling
+- Li curtain dynamics at sub-Hz rep rate — `not-yet-sourced` (HYLIFE papers may contain partial analog data) — important
 
 ---
 
 ### 3. Maturity of Key Subsystems and Components
 **Coverage**: Partial
 
-**Available from sources**:
-- **EM launcher (driver)**: TRL 4–5. Machine 3 demonstrated 6.5 km/s. Machine 4 (targeting 60 km/s, commercially relevant) was cancelled before construction. The 10× velocity gap is the unresolved engineering challenge.
-- **Target / amplifier**: TRL 3–4. Fusion demonstrated (UKAEA validated, 2022). Gain demonstrated at what NIF calls record is ~4×; First Light needs 200–1000×. This is the biggest TRL gap in the entire concept.
-- **Liquid lithium blanket/breeding**: TRL 3–4. Design is detailed, TBR independently validated, but not built at any scale. Liquid metal handling at this scale is a known engineering challenge shared with other IFE/MFE concepts.
-- **Tritium handling systems**: TRL 5–6 (via ITER and fission industry experience, applicable here).
-- **Steam Rankine BOP**: TRL 9. Mature commercial technology; sources confirm "identical to many other already working facilities."
+**Available**:
+- **Driver (EM gun)**: Machine 3 (two-stage gas gun, 6.5 km/s, 2.5 MJ, $4.3M) demonstrated and costed. TRL ~3 for commercial-scale projectile driver.
+- **Target**: Fusion demonstrated (April 2022, ~50 neutrons, UKAEA validated). Target physics simulation capability claimed. TRL ~3–4 for target physics; TRL ~1–2 for mass-manufactured target production.
+- **Liquid Li blanket**: TBR = 1.8 validated analytically by TUV SUD UK (February 2026). No hardware demonstration. HYLIFE-I/II provide engineering analog. TRL ~3.
+- **BOP (steam Rankine)**: Mature industrial technology. TRL 9. First Light explicitly cites "150-year-old steam turbine technology."
+- **EM pumping**: 1983 HYLIFE LLNL report provides detailed EM pump design for Li at relevant flow rates (8.08 m³/s at 82.5 kPa). Hardware analogs exist (sodium pumps validated). TRL ~5 for this subsystem class.
 
 **Missing**:
-- TRL breakdown explicitly stated for any subsystem (these are inferred from source descriptions)
-- Any Materials and Components Readiness Level (McRL) assessment
-- Target fabrication at repetition rate (even sub-Hz): how are the ~1 cm cubic targets with multi-cavity proprietary amplifier structure manufactured at commercial scale? Not addressed in any source.
+- No TRL assessment for rep-rated EM gun (reload and firing cycle, barrel wear at sub-Hz rates).
+- No experimental data on target fabrication at production scale or cost per unit.
+- No hardware prototype of the liquid Li reaction chamber at scale.
 
 **Gaps**:
-- Target fabrication at commercial rep rate — `proprietary` — **blocking** (no information on target manufacturing process, cost, or scalability)
-- EM driver scaling pathway (6.5 → 60 km/s) — `not-yet-sourced` / `truly-unknown` — **blocking** (Machine 4 was cancelled; this problem is unresolved)
-- Liquid Li system engineering challenges at scale — `not-yet-sourced` — important (search MHD pump literature, fission Li-cooled reactor experience; `unverified — confirm existence before searching`)
+- Rep-rated EM gun / barrel lifetime — `truly-unknown` — blocking (driver shot lifetime `Nd` is a key LCOE parameter)
+- Production-scale target fabrication — `truly-unknown` — blocking (target cost `δ` is a key LCOE parameter)
+- Integrated chamber experiments (Li curtain + target + driver) — `truly-unknown` — important
 
 ---
 
@@ -83,22 +79,20 @@
 **Coverage**: Partial
 
 **Available**:
-- **Lithium**: Liquid lithium is the primary blanket/breeding material. Large volumetric quantity needed (1-meter-thick flowing curtains). Li-6 enrichment needed for TBR optimization (though TBR 1.8 may allow natural lithium; not specified in sources).
-- **Tritium startup inventory**: D-T fuel requires initial tritium purchase before plant achieves self-sufficiency. At 333 MWe with 25 kg/yr net surplus, startup inventory requirements are non-trivial. Sources state self-sufficiency achievable "in as little as one week" which seems physically unrealistic and may reflect a misstatement.
-- **Target materials**: The "amplifier" target is cubic, ~1 cm, proprietary multi-cavity design. Materials not specified. Standard IFE targets use beryllium, diamond, or plastic ablators — none of these are explicitly mentioned.
-- **Conventional BOP**: No exotic materials in the steam Rankine cycle.
+- **Lithium**: Natural lithium (not enriched) sufficient per TBR = 1.8 result. First Light cites $70M/reactor for natural Li, vs. $143M–$451M for enriched alternatives (`ipgroupplc-news-and-events...2025-09-19.md`). This is a significant cost advantage over concepts requiring Li-6 enrichment.
+- **Tritium**: D-T fuel cycle with self-sufficient breeding claimed within one week of operation. Net surplus of 25 kg/year at 333 MWe — potential revenue stream at $30,000/g. Global tritium stock ~20 kg is not a blocking constraint given TBR = 1.8.
+- **Steel / conventional materials**: First Light's power plant explicitly relies on conventional materials post-chamber; no advanced materials R&D required for BOP.
+- **Target materials**: Current targets are complex multi-layer structures (few-mm fuel capsule within a multi-cavity amplifier). Materials not publicly disclosed. Currently bespoke prototypes.
 
 **Missing**:
-- Target material composition (entirely proprietary)
-- Li-6 enrichment fraction required
-- Annual target production volume (shots/year at 0.033 Hz ≈ ~1M shots/year for 333 MWe — this is the scale question)
-- Tritium startup inventory quantification
+- Target material composition and manufacturing bill-of-materials are proprietary.
+- EM gun barrel materials at 60 km/s launch velocity — not documented for projectile ICF.
+- Chamber wall materials under long-term liquid Li exposure — HYLIFE provides partial analog but for Flibe, not pure Li.
 
 **Gaps**:
-- Target material composition — `proprietary` — **important** (could affect cost significantly; must use analogue from NIF/hohlraum targets)
-- Target production volume and manufacturing process — `proprietary` — **blocking** for operating cost model (target cost/shot is often the dominant IFE operating cost)
-- Li-6 enrichment requirements and supply chain — `not-yet-sourced` — important (search ORNL or DOE Li isotope separation literature)
-- Tritium startup inventory — `derivable` — important (can be estimated from D-T burn rate at target Q and rep rate)
+- Target bill-of-materials — `proprietary` — important (sets floor on target cost)
+- EM gun barrel materials/wear at commercial scale — `truly-unknown` — important
+- Long-term Li compatibility with chamber wall materials — `not-yet-sourced` (search HYLIFE literature and LLNL liquid-metal materials studies) — important
 
 ---
 
@@ -106,84 +100,71 @@
 **Coverage**: Partial
 
 **Available Parameters**:
-
 | Parameter | Value/Range | Source | Confidence |
-|---|---|---|---|
-| Plant electrical output (pilot) | ~150 MWe | first-light-fusion-technology.md | m |
-| Plant electrical output (commercial) | ~333–500 MWe | first-light-fusion-technology.md | m |
-| Total capital cost (pilot) | <$1B | first-light-fusion-technology.md | l (company target) |
-| Total capital cost (commercial) | <$5B | first-light-fusion-technology.md | l (company target) |
-| LCOE target | <$50/MWh | first-light-fusion-technology.md | l (company target) |
-| Claimed fusion gain | 200–1000× | first-light-fusion-technology.md | l (undemonstrated) |
-| Rep rate | 0.011–0.1 Hz (sub-Hz) | dossier.md | m |
-| Energy conversion pathway | Steam Rankine cycle | first-light-fusion-technology.md | h |
-| Thermal efficiency (steam Rankine) | ~33–38% | derivable from standard steam cycle | m (analogue) |
-| TBR | 1.8 | first-light-flare-pivot-update.md | h (independently validated) |
-| Net tritium surplus | 25 kg/yr at 333 MWe | first-light-fusion-technology.md | m |
-| Vessel replacement schedule | Lifetime-of-plant | first-light-fusion-technology.md | m (unvalidated claim) |
-| Driver cost per joule (FLARE, not projectile) | $2/J | first-light-flare-pivot-update.md | l (FLARE, not applicable directly) |
-| Demonstrator cost (FLARE) | $100–200M | first-light-flare-pivot-update.md | l (FLARE, not projectile) |
+|-----------|-------------|--------|------------|
+| LCOE target | <$50/MWh | Hawker 2020 (pmc7658748) | medium |
+| Plant cost constant (α) | $3600/kWe (HYLIFE analog, 2020$) | Hawker 2020 | medium |
+| Driver cost constant (γ) | $1.7/J (Machine 3, prototype, non-rep-rated) | Hawker 2020 | low (prototype, not commercial) |
+| Driver energy (Ed) | 2.5 MJ (Machine 3); ~100 MJ (Machine 4 target, cancelled) | prnewswire 2022 / dossier | low for commercial scale |
+| Repetition rate (f) | 0.033 Hz (1 shot/30 s) at 150 MW | prnewswire 2022 | medium |
+| Net electrical output | 333 MWe (FLARE design point) | theengineer TBR article | medium |
+| Gain threshold (commercial) | ≥200 | ipgroupplc 2025, Hawker 2020 | medium |
+| Thermal efficiency | ~35–40% (steam Rankine, sub-critical) | HYLIFE-II analog (osti-6780071) | medium |
+| TBR | 1.8 | theengineer article, TUV SUD UK validated | high |
+| Li cost | $70M/reactor (natural Li) | ipgroupplc 2025 | medium |
+| Pilot plant capital | ~$1B, 150 MW | prnewswire 2022 | low (aspirational) |
+| Demo facility cost | $100M–$200M ($2/J) | ipgroupplc 2025 | medium |
+| O&M cost (ε) | $10–$100/kWe-yr (bounds from Hawker 2020) | Hawker 2020 | low (bounding only) |
+| Construction time | 5 years | Hawker 2020 | medium |
+| Plant lifetime | 40 years | Hawker 2020 | medium |
+| Availability | Parameter in model; no concept-specific estimate | Hawker 2020 | low |
 
 **Missing Parameters**:
-
 | Parameter | Gap Type | Criticality | Notes |
-|---|---|---|---|
-| Capital cost by subsystem (CAS breakdown) | proprietary | blocking | Only total cost targets stated; no subsystem breakdown |
-| Driver (EM gun) capital cost | proprietary | blocking | No figure for the projectile driver specifically |
-| Target cost per shot | proprietary | blocking | Most sensitive IFE operating cost; entirely unknown |
-| Annual target production volume | derivable | blocking | Derivable from rep rate × hours/year |
-| Driver wall-plug efficiency | proprietary | blocking | Determines recirculating power fraction |
-| Recirculating power (gross→net) | derivable | blocking | Need driver efficiency first; else must assume |
-| Capacity factor / availability | not-yet-sourced | important | Not stated; pulsed IFE analogues could inform |
-| Q (target fusion gain, demonstrated) | truly-unknown | blocking | Machine 3 achieved Q<<1; commercial needs 200–1000× |
-| D-T fuel cost (pre-self-sufficiency) | derivable | important | Tritium spot market ~$30k/g; derivable from burn rate |
-| O&M cost (non-fuel) | not-yet-sourced | important | No data; could use IFE plant study analogues |
-| Blanket/Li loop capital cost | not-yet-sourced | important | Analogues available from other liquid-metal blanket designs |
-| Thermal conversion efficiency (actual) | derivable | important | Steam Rankine ~33–38%; can be assumed with note |
-| First wall replacement cost | not applicable | — | Liquid Li blanket eliminates this cost item |
-| EM driver maintenance/replacement | truly-unknown | important | No data on EM launcher maintenance at commercial scale |
+|-----------|----------|-------------|-------|
+| Target gain G (achieved) | truly-unknown | blocking | No gain experiment conducted; G ≥ 200 needed for commercial competitiveness; single largest LCOE driver |
+| Target cost (δ, $/target at production scale) | truly-unknown | blocking | Explicitly treated as free parameter in Hawker 2020; bespoke prototypes only |
+| Driver efficiency (wall-plug to target) | proprietary | blocking | Not disclosed; sets recirculating power fraction |
+| Driver lifetime Nd (shots before replacement) | truly-unknown | blocking | Machine 3 shot count not published; sub-Hz rep rate means replacement frequency is tractable but unknown |
+| EM gun commercial-scale cost | truly-unknown | blocking | Machine 4 (100 MJ, 60 km/s) cancelled; no cost data for commercial-scale driver |
+| Yield per shot (Ef) | truly-unknown | important | Not demonstrated; derivable from gain + driver energy once gain is known |
+| Blanket multiple | derivable | important | Derivable from TBR = 1.8 and tritium self-sufficiency requirement |
+| Capacity factor / availability | not-yet-sourced | important | Sub-Hz rep rate simplifies scheduling maintenance; analogues from pulsed facilities |
+| CAS-level capital cost breakdown | not-yet-sourced | important | Hawker model bundles into α ($/kWe); no CAS10-structured breakdown published |
 
 ---
 
 ## Source Recommendations
 
-1. **First Light Fusion arxiv/journal publications** on target physics and compression gain — `not-yet-sourced` — search arxiv for "First Light Fusion" or "projectile inertial confinement"; may include peer-reviewed work on amplifier target physics. `unverified — confirm existence before searching`
-
-2. **IFE plant studies (laser ICF analogues)** for capital cost structure and target cost — `not-yet-sourced` — the SOMBRERO, HYLIFE-II, or Prometheus-L plant studies from the 1990s contain CAS-level cost breakdowns for IFE concepts that can serve as structural analogues. These are in OSTI. Available via OSTI/DOE.
-
-3. **Electrothermal / electromagnetic launcher literature** for driver cost and efficiency — `not-yet-sourced` — railgun and coilgun cost-per-joule literature from DoD/DARPA programs could inform EM driver capital and wall-plug efficiency. Search DTIC or IEEE for "electromagnetic launcher efficiency commercial."  `unverified — confirm existence before searching`
-
-4. **Liquid lithium loop engineering literature** for blanket capital cost — `not-yet-sourced` — ITER liquid metal blanket module cost estimates, or fission Li-cooled reactor (MSRE, FFTF) O&M analogues. Search IAEA or ORNL reports.
-
-5. **IFE target cost studies** — `not-yet-sourced` — DOE has funded IFE target fabrication cost studies (especially for NIF/laser ICF); these could anchor target cost/shot estimates even if the amplifier geometry differs. Search OSTI for "IFE target fabrication cost." `unverified — confirm existence before searching`
-
-6. **NearStar Fusion 2025 concept paper** — `not-yet-sourced` — sources indicate NearStar planned to publish experimental results and a detailed concept paper in 2025. If published, it may contain driver specs and power plant economics. Search for NearStar Fusion publications or SBIR final report.
+- **Hawker 2020 IFE LCOE model** (`knowledge/concept_research/22-projectile-icf/iter-03/sources/pmc-articles-pmc7658748.md`) — already sourced; this is the primary quantitative framework. Read the full paper for Monte Carlo parameter distributions.
+- **HYLIFE-II heat transport and COE study** (`knowledge/concept_research/22-projectile-icf/iter-03/sources/osti-servlets-purl-6780071.md`) — already sourced; read fully for COE formula, BOP parameters, and IHX cost scaling — directly analogous to First Light's liquid-wall plant architecture.
+- **Fleet-wide analog: `knowledge/sources/a_simplified_economic_model_for_inertial_fusion/`** — same paper as pmc7658748 (Hawker 2020 is registered fleet-wide). Use the fleet-wide extract if it's higher quality than the concept-scoped extraction.
+- **Fleet-wide analog: `knowledge/sources/energy_from_inertial_fusion/`** — 1992 IAEA IFE review; covers light-ion and projectile-class driver concepts and may contain driver efficiency or target cost estimates applicable as bounding values. Worth skimming the driver technology chapter. `unverified — confirm existence before searching`.
+- **Search OSTI for HYLIFE liquid-lithium materials compatibility studies** — for chamber wall lifetime under liquid Li exposure. Search terms: "HYLIFE lithium corrosion first wall" or "liquid lithium compatibility structural material ICF." `not-yet-sourced`.
+- **First Light Fusion white paper on FLARE (September 2025)** — cited in the FLARE pivot press releases but not yet ingested. Contains detailed gain model and power plant architecture data that would fill several important gaps. URL: `https://firstlightfusion.com/flare/`. Priority: high. `not-yet-sourced`.
+- **PyFECONS** (`/home/reid/PyFECONS`) — if it implements IFE CAS cost accounting, could be used to generate a CAS-structured cost breakdown analogous to this concept's plant. Check whether it handles liquid-wall IFE configurations.
 
 ---
 
 ## Summary
 
-**Proceed to full analysis with stated limitations.** The available data from First Light Fusion's public disclosures is sufficient to produce a credible qualitative write-up and a first-pass LCOE model — but both require explicit acknowledgment of the concept's unusual status: it is analytically interesting but commercially orphaned. The qualitative write-up should open with this context prominently.
+The data is sufficient to proceed to a D1+ qualitative analysis and a parameterized LCOE model, but not to a high-confidence quantitative estimate. The Hawker 2020 peer-reviewed LCOE model (authored by First Light's co-founder) provides the analytical framework; the 14-parameter structure was specifically designed for cases like this where gain and target cost are unknown. The power plant architecture is well-documented at a concept level, two independent third-party validations exist (UKAEA for physics, TUV SUD UK for TBR), and cost anchors exist for the driver and plant.
 
-For the quantitative model, the following assumptions will need to be stated explicitly due to data gaps:
-- **Driver efficiency**: assume 10–30% (electromagnetic gun wall-plug efficiency range from analogues) — this is a high-leverage uncertain parameter
-- **Target cost/shot**: assume $10–$1,000 (spanning laser IFE target analogues to speculative amplifier manufacturing) — this is likely the dominant operating cost uncertainty
-- **Capital cost structure**: use SOMBRERO/HYLIFE-II IFE plant study ratios as structural analogues, scaled to First Light's total cost targets
-- **Fusion gain**: use First Light's claimed 200–1000× range as a parameter sweep input; note no gain has been demonstrated
+The five blocking gaps — demonstrated gain, production-scale target cost, driver efficiency, commercial-scale driver cost, and driver shot lifetime — are all genuinely unknown and cannot be resolved from public sources. They should be treated as uncertainty parameters in the LCOE model rather than waiting for resolution. The FLARE white paper (not yet ingested) is the single highest-value missing source and should be acquired before writing the full analysis.
 
-The back-solve to $0.01/kWh will need to clearly flag that the binding constraint (target gain ≥200×) has never been demonstrated at any scale, and that even the $50/MWh company target appears optimistic given the absence of a credible path to Machine 4's velocity requirement.
+---
 
 ## Structured summary (machine-readable)
 
 ```yaml
-overall_rating: "Mostly Ready (with important caveats)"
-blocking_count: 7
-important_count: 6
-counting_method: "section_5_missing_parameters"
+overall_rating: "Mostly Ready"
+blocking_count: 5
+important_count: 7
+counting_method: "section_5_missing_parameters (5 blocking) plus sections 1-4 gaps classified blocking/important, deduplicated across all sections"
 section_coverage:
-  availability_of_data:       "Moderate"
+  availability_of_data:       "Good"
   system_function:            "Partial"
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
