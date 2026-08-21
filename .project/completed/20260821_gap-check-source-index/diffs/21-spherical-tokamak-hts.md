# Diff: 21-spherical-tokamak-hts

**Generated:** 2026-05-22T10:45:08-07:00

## Counts

| field | baseline | new | Δ |
|-------|----------|-----|---|
| blocking_count   | 3 | 4 | 1 |
| important_count  | 8 | 7 | - |
| overall_rating   | Mostly Ready | Mostly Ready | - |

## Fleet-source citations (new only — grep `knowledge/sources/` or `PyFECONS`)

```
25:- Fleet-wide D-T MFE TEA analog available: Araiinejad & Shirvan (2025), Applied Energy — `knowledge/sources/tea_dt_mfe_cost_analysis/` — covers D-T MFE tokamak LCOE range ($140–550/MWh), CAS cost structure, overnight capital cost range ($8800–22200/kW) for a compact HTS tokamak. Concept is ARC-class (high-field compact) not ST-geometry, but the CAS framework and relative cost weights are applicable.
123:| Fleet-wide D-T MFE LCOE analog | $140–550/MWh | `knowledge/sources/tea_dt_mfe_cost_analysis/` | low (ARC-class, not ST geometry) |
124:| Fleet-wide overnight capital cost analog | $8800–22200/kW | `knowledge/sources/tea_dt_mfe_cost_analysis/` | low (ARC-class) |
```

## Blocking-tier lines (baseline)

```
36:- Q value — `proprietary` / `truly-unknown` — **blocking** for LCOE: must assume or bound-estimate from power output targets
129:| Q value / fusion gain | proprietary | blocking | 450-750 MWe net implies burning plasma; Q can be bounded assuming ~30-40% thermal efficiency and estimated recirculating power |
130:| Fusion power (Rev D) | proprietary | blocking | Not stated in DPP 2025 abstract; must derive from Q + heating power assumptions |
133:| Capital cost by subsystem | proprietary | blocking | No cost estimates in any source; must use analogue scaling from tokamak plant studies (e.g., ARIES, EUROfusion DEMO, STEP) |
```

## Blocking-tier lines (new)

```
35:- Q value not publicly stated — `proprietary` — **blocking** for recirculating power fraction and Qplant calculation
56:- Qplant / engineering Q — `proprietary` — **blocking** for net plant efficiency and recirculating power calculation
131:| Q (fusion gain, Qplasma) | proprietary | blocking | Required to compute alpha heating fraction and recirculating power. Can be roughly estimated via scaling but very uncertain |
132:| Qplant (engineering Q) | proprietary | blocking | Net plant efficiency depends on EC heating efficiency + cryo loads; not derivable without Q |
133:| Thermal cycle type (steam vs sCO2) and efficiency | proprietary | blocking | Cannot compute gross→net electric without assumed cycle efficiency |
134:| Capacity factor / availability | not-yet-sourced | blocking | DPP 2025 says "compatible with reactor-level performance and availability" but no number given |
135:| Capital cost breakdown (any CAS level) | not-yet-sourced | blocking | No concept-specific estimates; ARIES-ST would be the appropriate analog; ARC-class analog available but ST geometry differs significantly |
```

## Full unified diff (truncated to 400 lines)

```diff
--- /tmp/gap_baselines_2026-05-22/21-spherical-tokamak-hts.md	2026-05-22 09:21:13.866679553 -0700
+++ /home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/21-spherical-tokamak-hts/gap_report.md	2026-05-22 10:45:08.874990838 -0700
@@ -1,62 +1,62 @@
-Now I have everything I need. Let me write the assessment.
+I have enough data to write the gap assessment now.
 
 ---
 
-# Gap Assessment: Spherical Tokamak - HTS
+# Gap Assessment: Spherical Tokamak - HTS (D-T)
 
 ## Overall Readiness
 **Rating**: Mostly Ready
-
-**Summary**: Tokamak Energy is one of the more transparent private fusion companies, and three research iterations have produced solid coverage of machine parameters, magnet technology, heating approach, blanket concept, and roadmap. The major gaps for LCOE analysis are Q value (deliberately unpublished), power conversion cycle selection (not yet made or disclosed), capital cost breakdown (proprietary), and EC heating power level for the pilot plant. These gaps are characteristic of a pre-conceptual design at this stage — they can be partially bridged with analogues from conventional tokamak power plant studies and the broader spherical tokamak literature (STEP programme). The analysis can proceed with clearly flagged assumptions.
+**Summary**: The qualitative foundations for sections 1–4 are solid: machine parameters (R=5.0m, A=2.3, B=5.25T, 450–750 MWe net), magnet technology (Demo4 validated), blanket architecture (outboard-only liquid Li, TBR=1.2), heating (EC-only flat-top), and pulsed operation rationale are all documented by credible sources. The LCOE model will require significant assumption-making — Q value and capital costs are unpublished and will need to be bridged via fleet-wide D-T MFE analogs and derivation. A D1+ analysis can proceed, but the quantitative section should be clearly flagged as analog-dependent.
 
 ---
 
 ## Section Coverage
 
 ### 1. Availability of Data
-**Coverage**: Moderate
+**Coverage**: Partial
 
 **Available**:
-- Machine parameters for ST-E1 Rev D are public: R=5.0 m, A=2.3, B=5.25 T on-axis, 450-750 MWe net, outboard-only liquid Li blanket TBR=1.2 (DPP 2025 abstract; `dpp2025-abstract.md`)
-- Design evolution from initial (2023) through Rev D (2025) is documented, showing significant growth in both machine size and power ambition (`st-e1-design-evolution.md`)
-- Magnet system: REBCO HTS, Demo4 complete 14 TF + 2 PF coil set validated at 11.8 T (`tokamak-energy-demo4-magnets.md`)
-- Heating: EC-only flat-top operation confirmed in peer-reviewed EPJ 2026 paper (`tokamak-energy-ec-heating-pilot-plant.md`)
-- Center-stack shielding: WC cermet in ~32 cm radial envelope, peer-reviewed 2019 study (`spherical-tokamak-center-stack-shielding.md`)
-- Pulsed operation rationale and 15-minute pulse target documented (`pulsed-spherical-tokamak-paper.md`, `tokamak-energy-roadmap.md`)
-- Company transparency: Tokamak Energy is part of the US DOE Milestone-Based Fusion Development Program, which requires regular public reporting. More disclosure than most private companies, but still pre-conceptual level detail.
+- Machine parameters: ST-E1 Revision D pre-conceptual design point is publicly disclosed (DPP 2025 abstract, `iter-03/sources/tokamak-energy-st-e1-dpp2025-abstract.md`): R=5.0m, A=2.3, B=5.25T on-axis, net power 450–750 MWe, outboard-only liquid Li blanket with TBR=1.2. The design evolution history is documented (`iter-02/sources/tokamak-energy-st-e1-design-evolution.md`).
+- Magnet system: Demo4 validated (14 TF + 2 PF coils, 11.8T, 30K) — `iter-03/sources/tokamak-energy-demo4-magnets.md`. Complete system-level test, not just single coil.
+- Heating: EC-only flat-top confirmed by peer-reviewed EPJ paper (Alieva et al. 2026), `iter-03/sources/tokamak-energy-ec-heating-pilot-plant.md`.
+- Shielding: WC cermet center-stack shielding physics well covered (`iter-02/sources/spherical-tokamak-center-stack-shielding.md`, Humphry-Baker & Smith 2019, 100KB).
+- Pulsed operation physics and rationale: thorough treatment in `iter-01/sources/pulsed-spherical-tokamak-paper.md` (Gryaznevich et al., 42KB).
+- Company overview, roadmap, and partnerships: `iter-04/sources/tokamakenergy-about-us-fusion-energy-high-temperature.md`, `iter-02/sources/tokamak-energy-roadmap.md`.
+- Fleet-wide D-T MFE TEA analog available: Araiinejad & Shirvan (2025), Applied Energy — `knowledge/sources/tea_dt_mfe_cost_analysis/` — covers D-T MFE tokamak LCOE range ($140–550/MWh), CAS cost structure, overnight capital cost range ($8800–22200/kW) for a compact HTS tokamak. Concept is ARC-class (high-field compact) not ST-geometry, but the CAS framework and relative cost weights are applicable.
 
 **Missing**:
-- No published plant study with cost breakdown (nothing comparable to a GASC/PROCESS system code output)
-- Q value for Rev D design not stated anywhere
-- Plasma current (Ip) for Rev D not stated (only pre-Rev D value of 13.6 MA available from disruption paper)
-- No capital cost estimates, even rough, from Tokamak Energy
+- Full plant study (only an APS DPP 2025 abstract is captured; full paper not yet sourced)
+- Q value / fusion gain — deliberately withheld
+- Any economic or cost estimate from Tokamak Energy
+- No ARIES-ST (spherical torus) plant study in the source index, which would be the closest geometry analog for plant-level costing
 
 **Gaps**:
-- Capital cost data — `proprietary` — **important**: can use analogue from conventional tokamak studies and STEP programme estimates
-- Q value — `proprietary` / `truly-unknown` — **blocking** for LCOE: must assume or bound-estimate from power output targets
-- Published plant study — `not-yet-sourced` — **important**: STEP programme (UK UKAEA spherical tokamak power plant) may have comparable published system code outputs
+- No full-length ST-E1 design paper (only DPP abstract) — `not-yet-sourced` — **important**: a full paper or milestone report may exist from the DOE Milestone-Based program
+- Q value not publicly stated — `proprietary` — **blocking** for recirculating power fraction and Qplant calculation
+- ARIES-ST cost study not captured — `not-yet-sourced` — **important**: strongest cost analog for spherical tokamak geometry
 
 ---
 
 ### 2. Challenges in Capturing System Function
-**Coverage**: Good (challenges well-characterized)
+**Coverage**: Partial
 
 **Available**:
-- Asymmetric blanket/shielding architecture is well-understood: outboard blanket covers fusion-relevant surface; inboard center-stack uses WC cermet shield with no tritium breeding. This is a fundamental ST cost/performance challenge documented in the literature.
-- EC-only heating for flat-top is documented as a design choice with physics rationale (O-mode efficiency, ray-tracing optimization). Power level for the pilot plant is undisclosed, but the approach is clear.
-- Pulsed operation and its implications for power conversion (need for thermal energy storage) are noted, with molten salt buffering as a referenced approach.
-- Center stack engineering challenge is well-documented: 32 cm shielding envelope, WC cermet candidates, radiation damage to HTS tapes.
-- Design volatility is observable: the major power target change from 85 MWe to 450-750 MWe between initial (2023) and Rev D (2025) illustrates that the design is immature and uncertainty bands on performance are wide.
+- Pulsed operation physics: well described (pulsed ST paper). Pulse duration ~15+ min for ST80-HTS, commercially attractive pulse of 1.5–2h for eventual plant — CS volt-second budget, BV ramp-up, bootstrap overdrive discussed. Thermal energy storage challenge acknowledged but not costed.
+- EC heating and current drive: ray-tracing simulations confirm EC-only flat-top is viable for three plasma scenarios (Alieva et al. 2026). However, no power plant–scale EC system engineering or cost data.
+- Center-stack shielding: the asymmetric geometry (outboard blanket, inboard WC cermet shield) is well described. The HTS irradiation damage limit under fusion neutron spectra is explicitly flagged as unknown in the literature.
+- Limited central solenoid space: acknowledged design constraint with documented mitigation strategy (bootstrap overdrive + BV ramp-up).
 
 **Missing**:
-- Thermal energy storage (TES) system design and cost — not covered in any source
-- Disruption frequency and energy management approach for pilot plant — only pre-Rev D disruption modelling available (arxiv:2512.16604 using old parameters)
-- Quantified recirculating power fraction — EC heating typically has low wall-plug efficiency (~30-40%), and the EC power needed for a 450-750 MWe plant is unknown
+- Engineering Q (Qplant): recirculating power balance (EC heating efficiency, magnet cryogenic load, cryoplant power) not published
+- Pulsed duty cycle: interpulse duration and thermal energy storage approach not documented
+- Divertor heat flux handling in spherical tokamak geometry: edge physics at power-plant scale poorly sourced
+- Tritium self-sufficiency dynamics for outboard-only blanket during pulsed operation not addressed
 
 **Gaps**:
-- Recirculating power / EC system wall-plug efficiency — `derivable` from analogues — **important**: EC current drive recirculating power fraction strongly affects net electric output
-- TES system for pulsed operation — `not-yet-sourced` — **nice-to-have**: STEP and DEMO studies have addressed this
-- Disruption handling for Rev D parameters — `not-yet-sourced` — **nice-to-have**
+- Qplant / engineering Q — `proprietary` — **blocking** for net plant efficiency and recirculating power calculation
+- Pulsed duty cycle and thermal storage approach — `not-yet-sourced` — **important**: needed for capacity factor and auxiliary power cost
+- Divertor design at power-plant scale — `not-yet-sourced` — **important**: heat exhaust is a defining constraint for ST geometry at high power density
+- HTS magnet irradiation tolerance under fusion neutron spectrum — `truly-unknown` (per Humphry-Baker, "maximum irradiation level that HTS tape can accommodate without degrading is not yet known") — **important**: drives center-stack replacement schedule and lifetime costing
 
 ---
 
@@ -64,23 +64,22 @@
 **Coverage**: Partial
 
 **Available**:
-- **HTS magnets (REBCO)**: TRL 5-6 — Demo4 validated complete 14 TF + 2 PF system at 11.8 T (Nov 2025). World-first for a complete tokamak coil set. Beyond single-coil demos (CFS, 20 T in 2021).
-- **ST40 experimental device**: operational, demonstrated 100M°C plasma ion temperature (2022), highest triple product of private fusion companies.
-- **ST80-HTS**: under construction, build completion ~2026. First large-scale HTS spherical tokamak. TRL 4-5 system level.
-- **EC heating (gyrotrons)**: TRL 6-7 — 1 MW gyrotron from Kyoto Fusioneering installed on ST40. Commercial gyrotron technology exists; integration at pilot plant scale is the challenge.
-- **WC cermet center-stack shielding**: TRL 3-4 — material properties characterized (2019 paper), but irradiation damage under fusion neutrons not characterized. Manufacturing at scale for 32 cm annular center stack is untested.
-- **Liquid lithium blanket (outboard)**: TRL 3-4 — concept well-defined, TBR=1.2 targeted. No prototype at reactor scale for any tokamak concept.
-- **Tritium breeding/processing system**: TRL 3-4 — no pilot-scale lithium blanket with T extraction demonstrated for any fusion concept.
+- HTS magnet system: Demo4 (Nov 2025) validated a complete 14 TF + 2 PF coil set at 11.8T, 30K — TRL ~5–6 for the full coil system. This is the strongest TRL data point in the dossier and represents a major milestone.
+- ST40 experimental platform: confirmed 100M°C plasma ion temperature, highest triple product of any private fusion company (per PR Newswire 2022). D-T burning plasma not yet demonstrated anywhere at reactor-relevant scale.
+- EC heating: 1 MW gyrotron installed on ST40 (`iter-01/sources/st40-heating-systems.md`). At-scale (40+ MW class) EC system for a pilot plant: TRL ~3–4.
+- Center-stack shielding (WC cermet): materials R&D at TRL 2–3. WC-FeCr cermet is a candidate; irradiation behavior at fusion-relevant neutron energies not validated.
+- Outboard liquid Li blanket: material selection and TBR target documented. No tokamak-integrated demonstration. TRL ~2–3.
 
 **Missing**:
-- TRL assessment for power conversion system (steam/sCO2 — not yet selected)
-- TRL for vacuum vessel / first wall at pilot plant scale
-- TRL for remote maintenance systems (noted as an early design priority but no details)
+- ST80-HTS: planned build completion 2026 (`iter-02/sources/tokamak-energy-roadmap.md`). Results not yet captured — this device is the critical bridging experiment between ST40 and ST-E1.
+- Divertor: TRL not assessed in available sources.
+- Power conversion system: not assessed; cycle type unknown.
 
 **Gaps**:
-- First wall / divertor TRL and lifetime — `not-yet-sourced` — **important**: W or W-alloy first wall replacement schedule drives maintenance costs; ITER/DEMO analogue literature exists
-- Remote maintenance system TRL — `not-yet-sourced` — **important**: DPP 2025 notes maintenance was an "early-stage priority" but no technical details published
-- Power conversion system TRL — `derivable` (depends on cycle selection) — **important** but not blocking
+- ST80-HTS experimental results — `not-yet-sourced` — **important**: 2026 results will be the key data point for ST-E1 design validation; worth re-sourcing after device operates
+- Liquid Li blanket TRL — `not-yet-sourced` (broader fusion blanket literature exists) — **important**: blanket is dominant capital cost item in D-T tokamaks
+- Center-stack HTS irradiation test data under fusion-relevant spectra — `truly-unknown` — **important**: determines magnet replacement schedule
+- EC power plant–scale heating system TRL — `not-yet-sourced` — **important** for capital and O&M costing
 
 ---
 
@@ -88,92 +87,100 @@
 **Coverage**: Partial
 
 **Available**:
-- **REBCO HTS tape**: identified as key material. 12 mm wide, <0.1 mm thick. ~200× current density of copper. Supply chain is a known bottleneck for the entire fusion-HTS sector (shared with CFS, TAE, and others). Current global REBCO production is far below what pilot plants would require.
-- **Tritium supply**: D-T fuel cycle identified; no tritium supply analysis in sources. This is a known industry-wide constraint — civilian tritium supply is currently ~5-10 kg/year globally (CANDU reactors), and startup tritium inventory requirements are uncertain.
-- **Tungsten carbide (WC cermet)**: center-stack shielding material. WC is an established industrial material, but fusion-grade WC cermet in the specific form factor has no supply chain.
-- **Liquid lithium**: outboard blanket coolant/breeder. Lithium supply is adequate; Li-6 enrichment capacity is the bottleneck if natural Li is insufficient.
+- REBCO tape supply: Furukawa Electric partnership confirmed (`iter-04/sources/tokamakenergy-about-us-fusion-energy-high-temperature.md`) as HTS tape supplier. General Atomics MOU for large-scale HTS magnet manufacturing.
+- WC cermet materials: Humphry-Baker & Smith (2019) covers WC-FeCr properties, Co-free binder development, processing challenges. No cost or manufacturing scalability data.
+- Tritium: standard D-T challenge — Li-6 enrichment for blanket needed; not discussed in concept-specific sources.
+- Tungsten and REBCO activation concerns: discussed in Humphry-Baker as "low activation elements" constraint.
 
 **Missing**:
-- Quantified REBCO tape requirements for ST-E1 magnet system
-- Any supply chain analysis or manufacturing readiness assessment
-- Tritium startup inventory estimate for the ST-E1 plant size
+- REBCO tape production volumes needed for an ST-E1-scale magnet system (estimate based on ST-E1 coil dimensions)
+- WC cermet industrial fabrication cost and scalability
+- Li-6 enrichment supply chain for outboard-only Li blanket
+- Tritium initial inventory and breeding lead time
 
 **Gaps**:
-- REBCO tape quantity and cost for full magnet system — `proprietary` / `not-yet-sourced` — **important**: industry scaling estimates exist (e.g., from CFS arc magnet costing studies), unverified for this geometry; flag as `unverified — confirm existence before searching`
-- Tritium startup inventory — `derivable` — **important**: can be estimated from fusion power, tritium consumption rate, TBR, and buildup time; analogue from ITER/DEMO tritium studies
-- Li-6 enrichment requirements — `derivable` — **nice-to-have**
-- WC cermet manufacturing readiness — `truly-unknown` — **nice-to-have**: insufficient irradiation data is noted in the 2019 paper itself
+- REBCO tape quantity requirement and production scaling — `not-yet-sourced` — **important**: HTS tape supply is an industry-wide bottleneck flagged across fusion programs; specific ST-E1 tape length estimate would resolve this
+- WC cermet manufacturing at scale — `truly-unknown` (research-grade only) — **important**: this is a novel fusion material with no commercial supply chain
+- Li-6 enrichment for liquid Li blanket — `not-yet-sourced` — **nice-to-have**: standard D-T concern but not concept-blocking
+- Initial tritium inventory source and cost — `derivable` from standard D-T plant models — **nice-to-have**
 
 ---
 
 ### 5. LCOE Parameter Extraction
+**Coverage**: Poor
 
 **Available Parameters**:
+
 | Parameter | Value/Range | Source | Confidence |
-|-----------|-------------|--------|------------|
-| Net electric output | 450-750 MWe | DPP 2025 abstract | medium (wide range reflects physics/tech uncertainty) |
+|---|---|---|---|
+| Net electrical output | 450–750 MWe | DPP 2025 abstract (`iter-03`) | medium (pre-conceptual, range reflects physics/tech uncertainty) |
 | Major radius | 5.0 m | DPP 2025 abstract | high |
 | Aspect ratio | 2.3 | DPP 2025 abstract | high |
 | On-axis toroidal field | 5.25 T | DPP 2025 abstract | high |
-| Blanket concept | Outboard liquid Li, TBR=1.2 | DPP 2025 abstract | high |
-| Operation mode | Quasi-steady, 15+ min pulses | Multiple sources | high |
-| Primary heating (flat-top) | EC only | EPJ 2026 | high |
-| Magnet material | REBCO HTS, 11.8 T at coil validated | Demo4 (Nov 2025) | high |
-| Timeline | Mid-2030s pilot plant | Multiple sources | medium |
-| Center-stack shielding | WC cermet, ~32 cm radial | Humphry-Baker & Smith 2019 | medium (smaller device) |
-| Fusion power (initial design) | 800 MW | DPP 2024 (pre-Rev D) | low (superseded) |
+| TBR | 1.2 | DPP 2025 abstract | high |
+| Pulse duration (bridging device) | ~15 min (ST80-HTS target) | `iter-02/sources/tokamak-energy-roadmap.md` | medium |
+| Commercially attractive pulse | 1.5–2 h | Gryaznevich et al. (pulsed ST paper) | medium (theoretical target, not ST-E1-specific) |
+| Fleet-wide D-T MFE LCOE analog | $140–550/MWh | `knowledge/sources/tea_dt_mfe_cost_analysis/` | low (ARC-class, not ST geometry) |
+| Fleet-wide overnight capital cost analog | $8800–22200/kW | `knowledge/sources/tea_dt_mfe_cost_analysis/` | low (ARC-class) |
+| HTS magnet validated field | 11.8 T (at coil, Demo4) | `iter-03/sources/tokamak-energy-demo4-magnets.md` | high |
 
 **Missing Parameters**:
+
 | Parameter | Gap Type | Criticality | Notes |
-|-----------|----------|-------------|-------|
-| Q value / fusion gain | proprietary | blocking | 450-750 MWe net implies burning plasma; Q can be bounded assuming ~30-40% thermal efficiency and estimated recirculating power |
-| Fusion power (Rev D) | proprietary | blocking | Not stated in DPP 2025 abstract; must derive from Q + heating power assumptions |
-| Thermal efficiency / power conversion cycle | not-yet-sourced | important | Steam Rankine vs. sCO2 not selected; STEP programme evaluations may bound this; ~33-40% is a reasonable analogue range |
-| EC heating power level for ST-E1 | proprietary | important | Drives recirculating power fraction; can be partially bounded by requiring Q×P_fusion > P_EC + parasitic loads |
-| Capital cost by subsystem | proprietary | blocking | No cost estimates in any source; must use analogue scaling from tokamak plant studies (e.g., ARIES, EUROfusion DEMO, STEP) |
-| First wall / divertor lifetime | not-yet-sourced | important | Determines blanket/wall replacement frequency and maintenance cost contribution |
-| Availability factor | not-yet-sourced | important | DPP 2025 notes "demonstrated compatibility with reactor-level performance and availability factor" but no number given |
-| Capacity factor target | not-yet-sourced | important | Likely 85-90% based on design intent but not stated |
-| Annual O&M cost | truly-unknown | important | No data; analogue from nuclear power plant O&M per GWe |
-| REBCO tape cost at scale | not-yet-sourced | important | Current market price ~$10-50/m (highly variable); required quantity unknown |
-| Tritium startup inventory | derivable | important | Estimable from fusion power and breeding curve assumptions |
-| Plant construction timeline | derivable | nice-to-have | Drives financing costs in LCOE |
+|---|---|---|---|
+| Q (fusion gain, Qplasma) | proprietary | blocking | Required to compute alpha heating fraction and recirculating power. Can be roughly estimated via scaling but very uncertain |
+| Qplant (engineering Q) | proprietary | blocking | Net plant efficiency depends on EC heating efficiency + cryo loads; not derivable without Q |
+| Thermal cycle type (steam vs sCO2) and efficiency | proprietary | blocking | Cannot compute gross→net electric without assumed cycle efficiency |
+| Capacity factor / availability | not-yet-sourced | blocking | DPP 2025 says "compatible with reactor-level performance and availability" but no number given |
+| Capital cost breakdown (any CAS level) | not-yet-sourced | blocking | No concept-specific estimates; ARIES-ST would be the appropriate analog; ARC-class analog available but ST geometry differs significantly |
+| First wall / blanket lifetime (full power years) | not-yet-sourced | important | Determines replacement schedule and replacement cost contribution to LCOE |
+| HTS magnet lifetime (center stack) under neutron flux | truly-unknown | important | Irradiation tolerance not established; Humphry-Baker flags this explicitly |
+| O&M cost rate ($/MWh or % of capital/year) | not-yet-sourced | important | No concept-specific data; fleet-wide D-T MFE O&M analogs applicable |
+| EC heating system capital cost (40+ MW scale) | not-yet-sourced | important | No engineering estimate for pilot plant–scale EC system |
+| Remote handling / maintenance capital cost | not-yet-sourced | important | DPP 2025 confirms maintenance scheme was designed in, but no cost |
+| Recirculating power fraction | derivable | important | Depends on Q and EC efficiency; can be estimated |
+| Thermal-to-electric efficiency | derivable | important | Can be assumed 35–40% pending cycle type disclosure |
+| Decommissioning cost | derivable | nice-to-have | Standard nuclear analog applicable |
 
 ---
 
 ## Source Recommendations
 
-1. **STEP programme system code outputs / plant studies** — `not-yet-sourced` — UKAEA's Spherical Tokamak for Energy Production programme is the closest public analogue. Published system code (PROCESS) results for STEP may provide capital cost scaling, thermal efficiency, and availability assumptions applicable to ST-E1. Search: OSTI/UKAEA publications, "STEP PROCESS power plant study" — *unverified — confirm existence before searching*.
+1. **ARIES-ST plant study** — `not-yet-sourced` — the ARIES-ST (Advanced Research Innovation and Evaluation Study – Spherical Torus) study is the only published power plant costing exercise for a spherical tokamak. It is referenced in the Araiinejad & Shirvan fleet-wide source and in the pulsed ST paper. Search: OSTI or DOE Technical Reports for "ARIES-ST" — *unverified: confirm existence before searching; it is expected to exist as an ARIES program output.*
 
-2. **ARIES / EUROfusion DEMO capital cost databases** — `not-yet-sourced` — Conventional tokamak plant studies (ARIES-AT, EU DEMO) have detailed CAS breakdowns that can serve as analogues for magnet, blanket, vacuum vessel, and balance-of-plant costs. These are publicly available and well-established. Scaling to ST geometry requires care (different aspect ratio, no inboard blanket).
+2. **DOE Milestone-Based Fusion Development Program reports for Tokamak Energy** — `not-yet-sourced` — the DOE program requires milestone deliverables. Public summaries may include performance targets or design reports. Search: DOE Office of Science / Fusion Energy Sciences program pages for Tokamak Energy milestones.
 
-3. **Fusion power output for Rev D** — the DPP 2025 full presentation (not just abstract) likely contains more parameters than the abstract extracted in Phase 1a. The full talk by Erik Maartensson (APS DPP 2025, gm12/8) may have been recorded or slides may be available — *unverified — confirm existence before searching*.
+3. **ST-E1 design papers (beyond DPP 2025 abstract)** — `not-yet-sourced` — Maartensson et al. DPP 2025 is likely to result in a journal or conference paper. Search: Nuclear Fusion, Fusion Engineering and Design, or EPJ Web of Conferences for "ST-E1" or "Tokamak Energy pilot plant."
 
-4. **REBCO tape supply chain and cost scaling** — CFS has published some information on HTS tape quantities and costs for their magnet system. Search: "REBCO tape cost fusion magnet" or CFS ARC/SPARC magnet costing publications — *unverified — confirm existence before searching*.
+4. **STEP (Spherical Tokamak for Energy Production) plant studies** — `not-yet-sourced` — UKAEA's STEP programme shares the spherical tokamak geometry and D-T fuel. Published design and cost studies from STEP may provide the best geometry-matched cost analog. Search: OSTI, Nuclear Fusion, or UKAEA publications for "STEP fusion plant cost" or "STEP LCOE."
 
-5. **Pulsed tokamak power conversion and thermal storage** — Academic literature on molten salt thermal energy storage for pulsed tokamaks likely contains efficiency and cost data relevant to the ST-E1 thermal cycle problem. Search: "molten salt thermal energy storage pulsed tokamak" — *unverified — confirm existence before searching*.
+5. **Liquid lithium first wall and blanket studies for tokamaks** — `not-yet-sourced` — ORNL collaboration with Tokamak Energy on liquid lithium systems is mentioned in the about-us page. Search: OSTI for "liquid lithium tokamak blanket" or "INFUSE lithium Tokamak Energy."
 
-6. **Tritium startup inventory and breeding curve** — The tritium fuel cycle challenge is covered in ITER and DEMO tritium studies. The "tritium start-up problem" literature (Abdou et al., various) provides conservative and optimistic scenarios. Search OSTI for "fusion tritium startup inventory breeding" — well-established published literature.
+6. **Gyrotron capital cost and EC system cost scaling** — `not-yet-sourced` — for the ~40 MW class EC heating system required for ST-E1. Search: fusion technology papers on gyrotron cost scaling or EC H&CD system engineering estimates.
 
 ---
 
 ## Summary
 
-**Proceed to full analysis.** The available data is sufficient for a D1+ qualitative write-up and a first-pass quantitative LCOE model with clearly stated assumptions. The key blocking gaps — Q value, fusion power, capital costs — are all amenable to bounded estimation using analogues from the broader tokamak plant study literature (ARIES, EUROfusion DEMO, STEP). Tokamak Energy's transparency on machine parameters, magnet technology, heating approach, and blanket concept gives a stronger foundation than most private fusion concepts at comparable development stage.
+**Proceed to full analysis with stated caveats.** The qualitative sections (data availability, system function, subsystem maturity, materials/supply chain) have enough sourced content for a thorough D1+ write-up. The concept is technically well-characterized at the pre-conceptual level — machine parameters, HTS magnet validation, pulsed physics rationale, and blanket/shield architecture are all documented.
+
+The quantitative LCOE model will require significant assumption-making: Q value, thermal efficiency, capacity factor, and capital cost breakdown are all unavailable from concept-specific sources. The analysis should source these from (a) fleet-wide D-T MFE analogs (Araiinejad & Shirvan for CAS cost structure; ARIES-ST if obtainable for geometry), (b) derivable estimates with clearly stated basis (thermal efficiency 35–40%; capacity factor 80–90% by analogy with plant studies claiming "reactor-level availability"), and (c) sensitivity sweeps on Q and capacity factor as the highest-leverage unknowns. The "back-solve to $0.01/kWh" exercise will be particularly diagnostic for this concept given the HTS magnet cost question.
 
-The two most important analogue sources to acquire before writing the quantitative model are: (1) a STEP or EU DEMO system code output for capital cost scaling, and (2) an estimate of EC heating power requirements at pilot plant scale to constrain the recirculating power fraction. Both are tractable with targeted literature search. The analysis should note that the 450-750 MWe output range is explicitly tied to "technology and physics assumptions" per Tokamak Energy — this 40% uncertainty band should be reflected directly in the LCOE sensitivity sweep.
+The most valuable pre-analysis source acquisition would be an ARIES-ST cost study and any published STEP plant economics, both of which are the closest geometry-matched cost analogs available.
+
+---
 
 ## Structured summary (machine-readable)
 
 ```yaml
 overall_rating: "Mostly Ready"
-blocking_count: 3
-important_count: 8
-counting_method: "section_5_missing_parameters"
+blocking_count: 4
+important_count: 7
+counting_method: "section_5_missing_parameters_blocking + key_gaps_in_sections_2_3_important; deduplicated across sections"
 section_coverage:
-  availability_of_data:       "Moderate"
-  system_function:            "Good (challenges well-characterized)"
+  availability_of_data:       "Partial"
+  system_function:            "Partial"
   subsystem_maturity:         "Partial"
   materials_supply_chain:     "Partial"
-  lcoe_parameter_extraction:  "Unknown"
-```
+  lcoe_parameter_extraction:  "Poor"
+```
\ No newline at end of file
```

## Acceptance notes (fill during Phase 3)

- Deviation class (1-6 per plan.md): 
- Justified by fleet source? 
- Notes: 
