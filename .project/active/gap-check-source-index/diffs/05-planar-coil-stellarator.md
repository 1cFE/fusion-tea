# Diff: 05-planar-coil-stellarator

**Generated:** 2026-05-22T09:37:25-07:00

## Counts

| field | baseline | new | Δ |
|-------|----------|-----|---|
| blocking_count   | 3 | 3 | 0 |
| important_count  | 8 | 8 | - |
| overall_rating   | Mostly Ready | Mostly Ready | - |

## Fleet-source citations (new only — grep `knowledge/sources/` or `PyFECONS`)

```
154:2. **Read `knowledge/sources/tea_dt_mfe_cost_analysis/`** — this fleet-wide source covers TEA methodology for D-T MFE with detailed CAS cost breakdowns. It is directly applicable to Helios as a D-T MFE steady-state plant. Use for BOP cost analogs, O&M estimates, and LCOE methodology. The ARIES-CS stellarator costing in that study (if present) is the closest analog.
156:3. **Read `knowledge/sources/aries_cost_account_documentation/`** — essential for assigning CAS numbers and applying standard fusion costing algorithms to Helios. ARIES-CS (compact stellarator, similar scale to Helios) is the most directly applicable prior stellarator plant study and likely contains cost estimates usable as analogs.
160:5. **Check `knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`** — multi-concept costing in a common CAS framework. While none of the four concepts is a stellarator, the O&M methodology and indirect cost fractions are applicable.
```

## Blocking-tier lines (baseline)

```
137:| Capital cost by subsystem (CAS structure) | not-yet-sourced | blocking | Full Helios paper may contain; extraction was partial |
138:| Total overnight capital cost ($/kWe or $B) | not-yet-sourced / proprietary | blocking | $150/MWh LCOE stated without cost basis |
139:| Magnet system cost (REBCO tape × length × $/m) | derivable | blocking | Coil geometry known; tape pricing from commercial data |
```

## Blocking-tier lines (new)

```
33:- Quantitative cost model or LCOE derivation — `proprietary` — **blocking** (LCOE section requires this)
103:- REBCO tape cost at scale — `not-yet-sourced` — **blocking** (coil cost is a primary capital cost driver; fleet-wide sources may have per-kA·m pricing estimates)
136:| Capital cost (total, by CAS) | proprietary | blocking | No CAS-level breakdown in arXiv paper; DOE Milestone report may contain it; ARIES-CS analog available as fleet-wide proxy |
137:| HTS coil cost (total) | not-yet-sourced | blocking | Dominant capital cost driver; depends on REBCO $/kA·m × tape length; Grant & Sheahen (2002) cited in paper but not extracted |
139:| O&M cost (annual, staffing + consumables) | not-yet-sourced | blocking | No estimate in public sources; comparable to a ~400 MWe nuclear plant baseline is the likely analog |
144:| LCOE derivation / methodology | proprietary | blocking | $150/$60 targets cited in dossier without traceable citation; presumed from internal Thea analysis |
```

## Full unified diff (truncated to 400 lines)

```diff
--- /tmp/gap_baselines_2026-05-22/05-planar-coil-stellarator.md	2026-05-22 09:21:13.836024530 -0700
+++ /home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/05-planar-coil-stellarator/gap_report.md	2026-05-22 09:37:25.250581614 -0700
@@ -1,13 +1,13 @@
-Now I have everything I need. Let me write the gap assessment.
+I now have sufficient data to write the gap assessment. Let me compile the report.
 
 ---
 
-# Gap Assessment: Planar Coil Stellarator
+# Gap Assessment: Planar Coil Stellarator (D-T)
 
 ## Overall Readiness
 **Rating**: Mostly Ready
 
-**Summary**: The Helios preconceptual design paper (arXiv:2512.08027) is an unusually thorough public document for a private fusion company — ~200 pages, DOE-certified, with detailed plasma physics, power balance, subsystem specifications, and operational parameters. Physics performance and qualitative system coverage are excellent. The primary gap is cost breakdown detail: the LCOE target ($150/MWh → $60/MWh) is stated without a capital cost decomposition, and the Phase 1a extraction captured only a portion of the full paper. A focused read of the Helios paper's cost/economics sections would likely close most remaining gaps. Proceed to analysis with awareness of the LCOE cost-structure gaps.
+**Summary**: The Helios preconceptual design paper (arXiv:2512.08027, ~200 pages, DOE Milestone-certified January 2026) provides exceptional technical depth for a private-sector fusion concept at this stage. Physics performance, engineering architecture, materials, maintenance scheme, and power flows are comprehensively documented with full confidence. The critical gap is cost: the public paper includes no CAS-level capital cost breakdown, no O&M dollar estimates, and no detailed LCOE derivation — only high-level targets ($150/MWh → $60/MWh at scale) that appear in the dossier without a traceable citation. Fleet-wide analogs (TEA D-T MFE, ARIES cost accounts) can partially fill this gap, but quantitative cost estimates for this concept will require either accessing the full DOE Milestone report or using scaled analogs from ARIES-CS.
 
 ---
 
@@ -17,19 +17,20 @@
 **Coverage**: Good
 
 **Available**:
-- Full preconceptual design report (arXiv:2512.08027, ~200 pages, DOE Milestone-certified January 2026). Covers plasma physics, magnets, blanket, divertor, first wall, energy conversion, maintenance, and operations.
-- Canis prototype paper (arXiv:2503.18960): Confirms REBCO conductor, validates planar coil field control approach.
-- Eos design published in Nuclear Fusion (Jan 2025), 4 peer-reviewed papers on the planar coil approach.
-- Website/press: Company stage, funding, timeline, LCOE targets.
-- Key parameters are explicitly stated with engineering justification — unusually transparent for a private company at this stage.
+- Full preconceptual design report as arXiv preprint (arXiv:2512.08027), submitted to *Fusion Engineering and Design*, DOE Milestone-certified January 13, 2026. Covers all major subsystems with engineering-level detail.
+- 4 peer-reviewed companion papers in *Nuclear Fusion* (Jan 2025) covering coil optimization methods, Eos plasma physics, fast ion confinement, and the stellarator systems architecture.
+- Canis prototype paper (arXiv:2503.18960) confirming REBCO HTS manufacturing process and field-shaping control.
+- DOE Milestone program certification press release with independent expert review statement.
+- ANS news article and Thea press releases confirming design milestones and roadmap.
 
 **Missing**:
-- The 4 Nuclear Fusion (Jan 2025) papers were not individually extracted in Phase 1a (referenced via press release only). These cover coil optimization, fast ion confinement, and Eos plasma physics.
-- Cost/economics section of the 200-page Helios paper was not captured in the Phase 1a extraction (extraction covers ~100 lines; 200-page paper likely contains cost modeling sections).
+- Full 200-page DOE Milestone report (referenced but not public; contains more system-level detail than the arXiv overview paper).
+- Detailed LCOE / TEA companion study (not published; Thea mentions discussions with "power offtakers and hyperscalers" suggesting internal cost models exist).
+- 4 Nuclear Fusion companion papers on specific components — not individually fetched in Phase 1a.
 
 **Gaps**:
-- Nuclear Fusion Jan 2025 papers not individually sourced — `not-yet-sourced` — important (subsystem physics detail)
-- Helios cost/economics section not extracted — `not-yet-sourced` — blocking for LCOE section
+- Full DOE Milestone report content — `proprietary` — **nice-to-have** (the arXiv paper captures the key engineering parameters; additional detail would improve fidelity)
+- Quantitative cost model or LCOE derivation — `proprietary` — **blocking** (LCOE section requires this)
 
 ---
 
@@ -37,48 +38,47 @@
 **Coverage**: Good
 
 **Available**:
-- Core challenge is well-defined: software-controlled field from 324 independent planar coils is entirely novel — no cost analogue exists at this scale. Paper acknowledges this explicitly ("complexity transferred from hardware to software").
-- ISS04 confinement scaling required enhancement factor 1.4 (reference) / 1.33 (gyrokinetic) — stated assumption, meaning physics performance relies on an extrapolation from W7-X (30 m³) to Helios (500 m³, ~17× larger plasma volume).
-- 6.6% alpha particle loss fraction documented (ASCOT5 code). Higher than typical tokamak assumptions (~2–3%), though source document notes it is within acceptable range.
-- Ignited operation (Q → ∞) assumed — no burning plasma experiment has validated this for stellarators.
-- Novel X-point divertor: First for an optimized stellarator, no operational heritage. Helios paper treats this as a design innovation.
-- Maintaining field accuracy across 324 independent coils during full-power operation is a novel controls challenge.
+- Novel planar coil stellarator architecture well-documented: 12 encircling + 324 shaping coils, software-controlled with 450+ independent variables. The "hardware-to-software complexity transfer" is the primary architectural innovation.
+- QA stellarator equilibrium physics: ISS04 transport scaling with H_ISS04 = 1.4 (verified by GENE/Trinity gyrokinetic simulations), MHD stability via TERPSICHORE and M3D-C1, energetic particle confinement via ASCOT5 (6.6% alpha loss to wall).
+- Novel X-point divertor for a stellarator: first-of-kind tokamak-like X-point in a stellarator power plant design; physics basis documented.
+- Bootstrap current management: 2/3 of rotational transform from bootstrap current — controlled via individually-addressable shaping coils.
+- Startup scenario: POPCON analysis, 2-hour startup, 10 MW ECRH → ignition at <1 MW.
+- Power balance: 958 MW fusion → 1,094 MW thermal → 438 MWe gross → 390 MWe net; recirculating power <3%.
 
 **Missing**:
-- No quantified uncertainty bounds on ISS04 enhancement factor — how much LCOE changes if it drops from 1.4 to 1.2 is not documented.
-- No degraded-performance fallback scenario discussed in sources.
+- Experimental validation of the X-point divertor in a stellarator plasma (Eos must demonstrate this first).
+- Experimental validation of closed-loop control at Eos scale with dozens of coils (Canis only demonstrated 9 coils).
+- Bootstrap current steady-state control over operational timescales (hours to days).
 
 **Gaps**:
-- Confinement scaling uncertainty range — `truly-unknown` (Thea has not published sensitivity bounds) — important
-- Alpha loss sensitivity to plasma optimization — `not-yet-sourced` (fast ion confinement paper in Jan 2025 Nuclear Fusion set not extracted) — important
+- X-point divertor in stellarator — no experimental precedent — `truly-unknown` at Helios scale — **important** (the design is modeled but undemonstrated; adds uncertainty to plasma-wall interaction modeling and heat load estimates)
+- Confinement enhancement H_ISS04 = 1.4 in QA configuration — `not-yet-sourced` (W7-X is QI, not QA; QA at this parameter is extrapolated) — **important** (affects fusion power and thus LCOE sensitively)
+- Software-defined stellarator field control at scale — `truly-unknown` (Canis proved principle; Eos-scale has 50+ coils; Helios has 324) — **nice-to-have** (risk flag for cost estimation uncertainty)
 
 ---
 
 ### 3. Maturity of Key Subsystems and Components
 **Coverage**: Partial
 
-**Available** (from sources):
-
-| Subsystem | Status from Sources | Approximate TRL |
-|-----------|--------------------|----|
-| HTS planar coil array | Canis 3×3 prototype demonstrated (2025), 1% field control accuracy, REBCO confirmed | TRL 4 |
-| ECRH heating (170 GHz) | ITER-specification gyrotrons; technology mature | TRL 7–8 |
-| Steam Rankine cycle (635°C) | Conventional power plant technology | TRL 9 |
-| QA stellarator plasma | W7-X demonstrates quasi-isodynamic; QA at Helios scale undemonstrated | TRL 3–4 |
-| X-point stellarator divertor | Described as "world first" — no operational experience | TRL 2–3 |
-| LiPb tritium breeding blanket | DEMO-class design, not yet built or operated | TRL 3–4 |
-| Vanadium first wall (V-4Cr-4Ti) | Material characterized; no full-scale neutron-irradiated operational experience | TRL 3–4 |
-| Sector-based remote maintenance | Conceptual design; Thea cites it as an innovation advantage | TRL 2–3 |
+**Available**:
+- **HTS coil system (encircling)**: TRL 4–5. REBCO at 20 T, 20 K demonstrated in large-bore magnets (MIT SPARC TFMC). Planar encircling coil design documented with FEA stress analysis. 40-year lifetime modeled.
+- **HTS shaping coils**: TRL 3–4. Canis (2025) demonstrated 9-coil REBCO array with closed-loop field control to <1% RMS error at 20 K. Manufacturing process (soldered metal insulation, ≤1 day/DP takt time) validated.
+- **Tritium breeding blanket (LiPb)**: TRL 4. LiPb blanket design well-documented: 50 cm thick, Pb-17Li, 65% Li-6 enrichment, EUROFER97 structure, SiC MHD inserts, He-cooled. TBR = 1.3 (idealized). No full-scale LiPb blanket module tested yet; HCLL designs from EU DEMO program are comparable.
+- **Vanadium first wall (V-4Cr-4Ti)**: TRL 4. Choice justified by 15-year neutron survival time. Referenced against prior fusion materials research. Not used in current operating devices.
+- **Thermal cycle (steam Rankine)**: TRL 9. 635°C superheated steam, three-stage turbines, 40.2% efficiency. Fully mature industrial technology.
+- **ECRH (startup heating)**: TRL 7. ITER-spec 170 GHz gyrotrons at 10 MW for startup; mature technology.
+- **Sector-based maintenance**: TRL 2–3. Architecture is designed and analyzed (84 days per 2-year cycle), but no stellarator has implemented this maintenance scheme. Novelty is a key cost and schedule uncertainty.
+- **X-point divertor for stellarator**: TRL 2–3. Documented in design, modeled in simulation, but no experimental precedent.
 
 **Missing**:
-- No TRL self-assessment in sources for most subsystems.
-- Divertor heat flux handling (10 MW/m²) at full scale — no prototype data.
-- SiC MHD inserts for LiPb blanket: Manufacturing readiness not discussed.
+- TRL assessments are inferred from context; Helios paper doesn't present a formal TRL matrix.
+- No published test data for V-4Cr-4Ti under D-T neutron fluence at scale.
+- No demonstrated sector-based maintenance at any prototype.
 
 **Gaps**:
-- Divertor thermal qualification — `truly-unknown` at this stage — important
-- SiC MHD insert manufacturing at scale — `not-yet-sourced` — important
-- Full stellarator sector remote maintenance prototype — `proprietary` (likely internal conceptual) — nice-to-have for LCOE modeling
+- Formal TRL matrix for all subsystems — `not-yet-sourced` (Thea's DOE Milestone report may contain this) — **important**
+- V-4Cr-4Ti neutron irradiation qualification at target fluence — `truly-unknown` — **important** (could force first-wall lifetime revision; 15-year lifetime is a key assumption)
+- Sector maintenance at any scale — `truly-unknown` — **nice-to-have** (risk factor, not cost-blocking)
 
 ---
 
@@ -86,25 +86,24 @@
 **Coverage**: Partial
 
 **Available**:
-- REBCO confirmed as conductor (Canis paper); three commercial suppliers demonstrated — shows manufacturing flexibility but does not quantify tape requirements or cost per meter.
-- Li-6 enrichment specified: 65%; total LiPb volume derivable from blanket geometry (50 cm thick, 8 m major radius).
-- Startup tritium: 1–2 kg specified.
-- First wall material: V-4Cr-4Ti; lifetime 15 full-power years.
-- Structural: EUROFER97.
-- Divertor tiles: Tungsten (51,000 hexagonal tiles, 2.5 cm).
+- REBCO HTS tape: commercially available from multiple suppliers (Canis paper tested tapes from 3 suppliers including YBCO and GdBCO variants). Current supply adequate for experiments; scaling to 336 full-scale coils requires HTS production ramp-up. Referenced cost projection study (Grant & Sheahen, arXiv:cond-mat/0202386) cited in Helios paper.
+- V-4Cr-4Ti vanadium alloy: 15-year first-wall lifetime documented; material referenced against Smith et al. (2000) and Sparks et al. (2022). Supply chain not discussed in published sources.
+- Pb-17Li breeder with 65% Li-6 enrichment: Li-6 enrichment is the key bottleneck — current global Li-6 enrichment capacity is limited (primarily Russia/China historical capability, with new US program underway via ORNL). Paper specifies 65% enrichment and 1.3 TBR but doesn't quantify enrichment cost.
+- Tungsten divertor targets: mature material, commercially available, standard in fusion devices.
+- EUROFER97 structural steel: EU-developed reduced-activation ferritic-martensitic steel, produced in limited quantities for fusion R&D.
+- SiC MHD inserts for blanket: specialty ceramic, limited production scale.
 
 **Missing**:
-- Total REBCO tape length required for 12 + 324 coils — not calculated in sources. Would need coil geometry to estimate.
-- Li-6 enrichment supply chain: Global production capacity and pricing not discussed.
-- Tritium availability on Helios timeline not analyzed (global ~25 kg inventory, committed to ITER/Eos pipeline).
-- No discussion of EUROFER97 or V-4Cr-4Ti production scale relative to demand.
-- Vanadium alloy is not commercially produced at power plant scale; weld qualification is open.
+- REBCO tape cost projections specific to Helios scale (336 coils × hundreds of km of tape).
+- Li-6 enrichment cost and supply chain analysis.
+- V-4Cr-4Ti production capacity and cost.
+- EUROFER97 production scaling.
 
 **Gaps**:
-- REBCO tape quantity estimate and cost/meter — `derivable` from coil geometry + commercial tape pricing — important for capital cost
-- Li-6 enrichment global supply chain readiness — `not-yet-sourced` — important
-- Tritium startup availability for Helios on 2030s timeline — `derivable` from published tritium balance models — important
-- V-4Cr-4Ti production scalability — `not-yet-sourced` — nice-to-have
+- REBCO tape cost at scale — `not-yet-sourced` — **blocking** (coil cost is a primary capital cost driver; fleet-wide sources may have per-kA·m pricing estimates)
+- Li-6 enrichment cost and supply security — `not-yet-sourced` — **important** (tritium breeding depends on enriched Li; cost is non-trivial)
+- V-4Cr-4Ti supply chain — `not-yet-sourced` — **important** (alternative vanadium alloy sourcing not discussed; US production capacity is limited)
+- EUROFER97 scaling — `not-yet-sourced` — **nice-to-have** (DEMO program producing it; likely not a blocking gap for cost estimation)
 
 ---
 
@@ -114,60 +113,65 @@
 **Available Parameters**:
 | Parameter | Value/Range | Source | Confidence |
 |-----------|-------------|--------|------------|
-| Net electrical output | 390 MWe | arXiv:2512.08027 | high |
-| Gross electrical output | 438 MWe | arXiv:2512.08027 | high |
-| Fusion power | 958 MW | arXiv:2512.08027 | high |
-| Total thermal power | 1,094 MW | arXiv:2512.08027 | high |
-| Thermal conversion efficiency | ~40.2% | arXiv:2512.08027 | high |
-| Recirculating power fraction | <3% (~48 MWe) | arXiv:2512.08027 | high |
-| Capacity factor | 88% | arXiv:2512.08027 | high |
-| Maintenance cycle | 84 days biennial | arXiv:2512.08027 | high |
-| First wall lifetime | 15 full-power years | arXiv:2512.08027 | high |
-| ECRH operational power | 2.5 MW | arXiv:2512.08027 | high |
-| LCOE target (early plant) | $150/MWh | thea.energy website | medium |
-| LCOE target (at scale) | $60/MWh | thea.energy website | medium |
-| Machine major radius | 8 m | arXiv:2512.08027 | high |
-| Magnet operating temperature | 20 K | arXiv:2512.08027 | high |
-| Coil count | 12 encircling + 324 shaping | arXiv:2512.08027 | high |
-| Max coil field | 20 T | arXiv:2512.08027 | high |
+| Net electric power | 390 MWe | arXiv:2512.08027 Table 1 | high |
+| Fusion power | 958 MW | arXiv:2512.08027 Table 1 | high |
+| Thermal power | 1,094 MW | arXiv:2512.08027 Table 1 | high |
+| Thermal efficiency (gross) | 40.2% | arXiv:2512.08027 §4.4 | high |
+| Net efficiency (net/thermal) | ~35.6% | Derived: 390/1094 | high |
+| Capacity factor | 88% | arXiv:2512.08027 Abstract, §2 | high |
+| Maintenance cycle | 84 days / 2 years | arXiv:2512.08027 §4.5 | high |
+| Plant design lifetime | 40 years | arXiv:2512.08027 §2 | high |
+| First wall lifetime | 15 full-power years | arXiv:2512.08027 §2 | high |
+| Coil lifetime | 40 years (plant lifetime) | arXiv:2512.08027 §2 | high |
+| ECRH recirculating power (ignited) | ~1 MW | arXiv:2512.08027 §3.1 | high |
+| ECRH recirculating power (startup) | 10 MW | arXiv:2512.08027 §3.1 | high |
+| Cryogenic cooling load | Not explicitly stated | — | low |
+| Tritium startup inventory | 1–2 kg | arXiv:2512.08027 Table 1 | high |
+| LCOE target (first plant) | ~$150/MWh | Dossier metadata (source uncertain) | low |
+| LCOE target (at scale) | ~$60/MWh | Dossier metadata (source uncertain) | low |
 
 **Missing Parameters**:
 | Parameter | Gap Type | Criticality | Notes |
 |-----------|----------|-------------|-------|
-| Capital cost by subsystem (CAS structure) | not-yet-sourced | blocking | Full Helios paper may contain; extraction was partial |
-| Total overnight capital cost ($/kWe or $B) | not-yet-sourced / proprietary | blocking | $150/MWh LCOE stated without cost basis |
-| Magnet system cost (REBCO tape × length × $/m) | derivable | blocking | Coil geometry known; tape pricing from commercial data |
-| Blanket replacement schedule and cost | not-yet-sourced | important | First wall = 15 FPY; blanket replacement interval unstated |
-| O&M cost breakdown ($/MWh or $/yr) | proprietary | important | Not in any source |
-| Facility labor cost / headcount | truly-unknown | important | No staffing model in sources |
-| Li-6 enrichment procurement cost | derivable | important | Enrichment pricing exists in open literature |
-| Tritium startup cost | derivable | important | 1–2 kg at ~$30k/g → $30–60M; stated assumption |
-| Divertor replacement schedule | not-yet-sourced | important | 51,000 W tiles; W erosion rate depends on heat flux and time |
-| ECRH capital cost (10 MW startup system) | derivable | nice-to-have | ITER gyrotron pricing exists; 10 MW system = ~$50–100M estimate |
-| Balance of plant cost | derivable | important | Steam Rankine at this scale has commercial analogues |
-| Indirect costs, construction, contingency | truly-unknown | important | Standard preconceptual design gap |
+| Capital cost (total, by CAS) | proprietary | blocking | No CAS-level breakdown in arXiv paper; DOE Milestone report may contain it; ARIES-CS analog available as fleet-wide proxy |
+| HTS coil cost (total) | not-yet-sourced | blocking | Dominant capital cost driver; depends on REBCO $/kA·m × tape length; Grant & Sheahen (2002) cited in paper but not extracted |
+| Balance of plant cost (turbine island, heat exchangers) | derivable | important | Standard steam Rankine at 390 MWe; TEA D-T MFE source and ARIES cost accounts can provide analogs |
+| O&M cost (annual, staffing + consumables) | not-yet-sourced | blocking | No estimate in public sources; comparable to a ~400 MWe nuclear plant baseline is the likely analog |
+| First wall replacement cost (per 15-year cycle) | derivable | important | V-4Cr-4Ti blanket modules; sector maintenance scheme enables cost estimation if component costs known |
+| Cryogenic system operating cost | not-yet-sourced | important | 20 K operation for 336 REBCO coils; non-trivial parasitic load; not quantified |
+| Control system capital cost (software + hardware) | truly-unknown | important | 450+ independent variables, novel software stack; no published cost estimate |
+| Li-6 enrichment cost | not-yet-sourced | important | 65% enrichment for LiPb blanket; DOE/ORNL enrichment program data needed |
+| LCOE derivation / methodology | proprietary | blocking | $150/$60 targets cited in dossier without traceable citation; presumed from internal Thea analysis |
+| Fuel cost (D-T annual) | derivable | nice-to-have | Low relative to capital; standard D-T fuel cost methodology applies |
+| Decommissioning cost estimate | derivable | nice-to-have | CAS 90s approach from ARIES cost account documentation applicable |
 
 ---
 
 ## Source Recommendations
 
-1. **Full Helios paper cost/economics sections** — Read arXiv:2512.08027 PDF in full, specifically sections covering economic analysis, cost estimates, and LCOE calculation. The Phase 1a extraction is a partial summary; the 200-page document almost certainly contains more. `not-yet-sourced` — high priority, confirmed to exist.
+1. **Access the 4 Nuclear Fusion companion papers** (Jan 2025, Nuclear Fusion vol. 65 issue 2) — `not-yet-sourced` — the companion papers on Eos scoping and fast ion confinement likely contain more quantitative detail on transport assumptions that affect LCOE sensitivity. Publicly available via IOP Science.
+
+2. **Read `knowledge/sources/tea_dt_mfe_cost_analysis/`** — this fleet-wide source covers TEA methodology for D-T MFE with detailed CAS cost breakdowns. It is directly applicable to Helios as a D-T MFE steady-state plant. Use for BOP cost analogs, O&M estimates, and LCOE methodology. The ARIES-CS stellarator costing in that study (if present) is the closest analog.
 
-2. **Nuclear Fusion Jan 2025 papers (4 papers)** — Individually extract the 4 peer-reviewed papers announced via Thea's press release. The fast ion confinement paper is particularly relevant for alpha loss sensitivity. `not-yet-sourced` — confirmed to exist, DOIs likely resolvable via Thea press release URLs.
+3. **Read `knowledge/sources/aries_cost_account_documentation/`** — essential for assigning CAS numbers and applying standard fusion costing algorithms to Helios. ARIES-CS (compact stellarator, similar scale to Helios) is the most directly applicable prior stellarator plant study and likely contains cost estimates usable as analogs.
 
-3. **REBCO tape cost and supply data** — Search OSTI or Google Scholar for "REBCO tape cost projection," "HTS tape manufacturing cost fusion," or "2G HTS conductor market." NREL and ORNL have published HTS cost roadmaps. `not-yet-sourced` — unverified specific papers, suggest search strategy.
+4. **Search for ARIES-CS cost data** — ARIES-CS was a compact stellarator plant study at similar scale (R~7.7 m, 1 GW thermal). It has a detailed cost breakdown. Thea explicitly compares Helios to ARIES-CS in the paper. Search OSTI for "ARIES-CS cost" or "compact stellarator power plant economics." `unverified — confirm existence before searching`.
 
-4. **LiPb blanket cost analogues from DEMO/ITER** — European DEMO documentation (EUROfusion) includes LiPb blanket cost estimates. The Helios blanket is EUROFER97-structured LiPb, which is close to DEMO WCLL/HCLL concepts. Search EUROfusion DEMO documentation. `not-yet-sourced` — `unverified — confirm existence before searching`.
+5. **Check `knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`** — multi-concept costing in a common CAS framework. While none of the four concepts is a stellarator, the O&M methodology and indirect cost fractions are applicable.
 
-5. **Tritium supply chain analysis** — Kovari et al. (2021) "Tritium resources available for fusion reactors" and associated papers quantify tritium availability on fusion development timelines. Relevant for startup inventory cost and availability risk. `not-yet-sourced` — paper likely exists; `unverified — confirm exact citation before searching`.
+6. **REBCO tape cost projection** — Grant & Sheahen (2002) is already cited in the Helios paper (ref [49]). More current REBCO cost projections exist through Commonwealth Fusion Systems and SuperPower Inc. announcements. Search OSTI or Google Scholar for "REBCO cost projection fusion" for 2020–2025 estimates. `unverified — confirm existence before searching`.
 
-6. **V-4Cr-4Ti availability and weld qualification** — Search ORNL publications on vanadium alloy for fusion first walls. ORNL has historically led V-alloy fusion research. `not-yet-sourced` — `unverified — confirm existence before searching`.
+7. **Li-6 enrichment cost** — ORNL's Li-6 Enrichment Program (Milestone-program adjacent) likely has public cost-per-gram estimates. Search DOE/ORNL NNSA publications. `unverified — confirm existence before searching`.
 
 ---
 
 ## Summary
 
-**Proceed to full analysis.** The Helios preconceptual design is one of the most well-documented pre-commercial fusion concepts available — the qualitative sections (data availability, system function challenges, subsystem maturity, materials) can be written to high quality from existing sources. The single blocking action before the quantitative LCOE model is reading the full Helios PDF for cost/economics sections, which are almost certainly present in the 200-page document but were not captured in Phase 1a's partial extraction. Secondary priority is extracting the 4 Nuclear Fusion (Jan 2025) papers for subsystem physics depth. With those two actions, this concept moves from "Mostly Ready" to "Ready."
+**Proceed to full analysis with the fleet-wide TEA source as cost scaffold.** The Helios preconceptual design provides the most detailed technical foundation available for any private fusion concept at this stage — physics is well-characterized with high-fidelity simulations, engineering architecture is documented at a level sufficient for subsystem-level cost estimation, and key performance parameters (390 MWe, 88% CF, 40.2% thermal efficiency, 40-year plant life) are firm. 
+
+The capital cost and O&M gaps are significant but **bridgeable**: Thea explicitly compares Helios to ARIES-CS, making ARIES-CS cost data the natural analog for the magnet system and structural costs. The TEA D-T MFE fleet-wide source covers BOP and O&M methodology directly applicable to a 400 MWe D-T MFE plant. The two main technical uncertainties that affect LCOE sensitivity — REBCO tape cost at scale and HTS coil lifetime under neutron flux — are real but have published partial data. The analysis should proceed with cost estimates derived from ARIES-CS and ARIES cost account analogs, with explicit uncertainty bounds on REBCO cost and V-4Cr-4Ti replacement frequency.
+
+---
 
 ## Structured summary (machine-readable)
 
@@ -175,11 +179,11 @@
 overall_rating: "Mostly Ready"
 blocking_count: 3
 important_count: 8
-counting_method: "section_5_missing_parameters"
+counting_method: "deduplicated across all sections; blocking = capital cost breakdown, O&M cost quantification, LCOE derivation/methodology; important = H_ISS04 in QA stellarator, TRL formal matrix, V-4Cr-4Ti qualification, REBCO cost at scale, Li-6 enrichment cost, V-4Cr-4Ti supply chain, HTS coil cost, cryogenic operating cost, balance of plant cost, first wall replacement cost, control system cost (collapsed to 8 distinct items)"
 section_coverage:
   availability_of_data:       "Good"
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
