# Phase 3 diff: 16-muon-catalyzed-fusion

**Generated:** 2026-05-22T14:24:14-07:00

## Counts (Phase 2 -> Phase 3 strict-read regen)

| field | phase2 | phase3 | Δ |
|-------|--------|--------|---|
| blocking_count   | 5 | 3 | -2 |
| important_count  | 6 | 5 | - |
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
# Gap Assessment: Muon-Catalyzed Fusion (D-T)
```

## Blocking-tier lines (new)

```
123:| Accelerator capital cost (dominant cost driver) | proprietary / truly-unknown | blocking | No published cost for novel active-target design; conventional accelerators (PSI) cost tens of millions for research-scale; commercial-scale unknown |
124:| Fusion cell capital cost | truly-unknown | blocking | No power-plant-scale cell design exists; diamond anvil cell is not a cost analog |
125:| Validated system energy balance | proprietary | blocking | 47% recirculating power claim and 300 fusions/muon target are unvalidated simulation results; current state gives 14% net electrical efficiency (Kelly 2021) |
```

## Full unified diff (truncated to 400 lines)

```diff
--- /tmp/gap_phase2_state/16-muon-catalyzed-fusion.md	2026-05-22 12:59:21.070617347 -0700
+++ /home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/16-muon-catalyzed-fusion/gap_report.md	2026-05-22 14:24:14.890275402 -0700
@@ -1,12 +1,8 @@
-I have all the information needed. The OSTI source is about the SNS SRF accelerator at ORNL (a useful TRL analog for the muon source), not a fusion economics study. No fleet-wide sources offer useful cost analogs for the dominant cost driver (muon production accelerator). Now I'll write the assessment.
-
----
-
 # Gap Assessment: Muon-Catalyzed Fusion (D-T)
 
 ## Overall Readiness
 **Rating**: Significant Gaps
-**Summary**: The physics of muon-catalyzed fusion is well-documented in peer-reviewed literature, and Acceleron's ARPA-E 2025 presentation provides a credible (if unvalidated) system-level LCOE target and key performance parameters. However, no plant-level engineering design or capital cost breakdown has been published — the concept sits at TRL 2–3 for commercial scale — making quantitative LCOE extraction reliant on high-level approximation rather than traceable parameter chains. A rich qualitative analysis is possible; a defensible quantitative LCOE requires explicitly flagging its speculative basis.
+**Summary**: The physics of muon-catalyzed fusion is well-documented in decades of experimental literature, and Acceleron's ARPA-E presentation (2025) provides a credible system architecture sketch with a single LCOE target ($0.025/kWh). However, Acceleron is a pre-breakeven startup (~2030 planned breakeven test at Brookhaven), its two key innovations — the novel active-target muon source and the commercial-scale fusion cell — have no published hardware validation or cost breakdown. A qualitative analysis of concept physics, challenges, and subsystem maturity is feasible; a quantitative LCOE model would rest almost entirely on unvalidated company claims and cannot be meaningfully constructed without additional sources.
 
 ---
 
@@ -16,24 +12,22 @@
 **Coverage**: Partial
 
 **Available**:
-- Acceleron ARPA-E 2025 presentation: system-level LCOE target ($0.025/kWh), recirculating power fraction (47%), muon energy cost target (3.4 GeV/muon), fusions/muon target (300), Brayton cycle BOP mention, LCOE parametric contour plot vs. beam energy and fusions/muon, revenue-from-heat-sales assumption, Brookhaven energy breakeven test timeline (~2030)
-- Acceleron company website: plant size target (~100 MW), partner labs (PSI, Fermilab, ORNL, Argonne), Series A funding ($24M closed)
-- Wikipedia physics article (`muon-catalyzed-fusion-physics.md`): comprehensive history, experimental best of 150 fusions/muon (Jones, LAMPF), alpha-sticking probability range (0.3–0.9%), conventional electrical energy cost per muon (~6 GeV), Kelly/Hart/Rose 2021 analysis (Q~130% thermal, ~14% electrical return at current parameters), Pusch recirculating-power alternative estimate (3–5× input vs. output)
-- PMC 2022 (Yamashita et al.): new kinetics model for CF in high-temperature compressed gas targets; shows cycle rate increases with temperature; directly relevant to Acceleron's high-density target concept
-- OSTI (SNS SRF Linac, ORNL): 10-year operational data for a ~1 GeV SC proton linac at 92% availability — relevant analog for the muon source accelerator; no cost data but establishes TRL reference
-- arXiv 2021 (Kamimura): sticking probability calculation 0.857%, slightly lower than literature (0.91–0.93%), relevant to fusions/muon ceiling
+- 60+ years of physics literature documenting muon-catalyzed fusion mechanisms, alpha-sticking probabilities, and catalytic cycle rates (Wikipedia: Muon-catalyzed fusion; PMC article, Yamashita et al. 2022; arXiv:2112.08399, Kamimura & Kino 2021; TRIUMF experimental program)
+- Experimental demonstration of 100–150 d-t fusions per muon achieved at LAMPF (Jones et al.); refined α-sticking probability ω₀ = 0.857% (Kamimura 2021) giving theoretical ceiling of 200–350 fusions/muon
+- Kelly, Hart & Rose (2021) μCF energy model: Q ≈ 130% thermal, 14% net electrical at current accelerator efficiency — published parametric energy balance
+- Acceleron ARPA-E BETHE presentation (July 2025): system architecture diagram, energy flow (3.4 GeV/muon, 47% recirculating power fraction), LCOE contour plot, Brayton cycle BOP, active-target muon source concept, Brookhaven breakeven roadmap
+- Acceleron company website: plant scale (~100 MW), operating temperature (500–1000°C), Series A funding, collaborations with PSI, Fermilab, ORNL, Argonne
+- OSTI/ORNL SNS SCL operation paper: 10-year operational experience with a 1 GeV superconducting proton linac (1.4 MW beam power, 90–92% facility availability, 99.5% SRF cavity availability) — directly analogous as an accelerator technology reference
 
 **Missing**:
-- No published plant design study (no ARIES- or SOMBRERO-equivalent)
-- No independent techno-economic analysis of Acceleron's approach
-- Norrønt (Norwegian competitor) technical publications not in source set
-- Pre-2021 JINR experimental data on muon energy cost (INIS record is metadata only — full content not extracted)
-- Historical accelerator cost scaling studies for proton linacs at GeV scale
+- Independent peer-reviewed cost analysis of μCF power plants (none exists)
+- Published plant study or preconceptual design report
+- Acceleron engineering publications beyond ARPA-E slides
+- Data from the second μCF company (Norrønt AS, Norway) — not captured in Phase 1a
 
 **Gaps**:
-- Plant-level engineering design document — `proprietary` — **blocking**: without a design, capital cost estimation has no anchor
-- Independent techno-economic review of Acceleron's 47% recirculating power claim — `not-yet-sourced` — **important**: Pusch/Kelly estimates suggest 300–500% recirculating power at current physics; Acceleron's claim requires validation
-- Norrønt technical publications — `not-yet-sourced` — **nice-to-have**: competitive comparison would strengthen analysis
+- No independent plant study for μCF — `truly-unknown` — blocking
+- Norrønt AS/Ultrafusion data absent — `not-yet-sourced` — important
 
 ---
 
@@ -41,22 +35,20 @@
 **Coverage**: Partial
 
 **Available**:
-- Alpha-sticking physics is well-understood: 0.3–0.5% sticking means theoretical ceiling of ~200–350 fusions/muon (Wikipedia); Acceleron targets 300 but only 150 demonstrated experimentally
-- Energy balance at system level is described by Acceleron at a high level: 3.4 GeV/muon in, 47% recirculating, Brayton BOP
-- Kelly et al. (2021) parametric analysis provides an independent model of the energy balance as a function of accelerator efficiency, fusions/muon, and heat conversion efficiency — a key secondary source for checking Acceleron's claims
-- PMC (Yamashita 2022) demonstrates that higher temperatures increase cycle rate, supporting Acceleron's high-density, high-temperature target approach
-- OSTI (SNS) shows a mature reference system (pulsed SC linac at GeV scale) with known reliability characteristics — directly analogous to the muon source accelerator
+- The energy balance chain is partially documented: ion beam → active target → pion production → muon yield → muon injection into D-T cell → catalytic cycling (governed by muon lifetime 2.2 μs, formation rate, alpha-sticking) → thermal energy deposition → power conversion. ARPA-E presentation shows a high-level energy flow with 3.4 GeV beam energy and 47% recirculating power fraction.
+- The PMC article (Yamashita 2022) provides an advanced kinetics model (EVM-SPM-FIF) showing that cycle rate increases with temperature, with optimum around T = 300–500 K at LHD densities — this is relevant to the high-density compressed-gas target approach Acceleron uses (diamond anvil cell achieving 2.2 LHD in 2024 experiments)
+- The α-sticking problem is well-characterized: at standard conditions ω₀ ~ 0.9%, but at high density the reactivation fraction can bring effective sticking to 0.3–0.5%, enabling higher per-muon yield
+- The SNS linac paper provides operational lessons for high-power pulsed superconducting linacs relevant to the muon-producing accelerator
 
 **Missing**:
-- Commercial-scale D-T target design: diamond anvil cell demonstrated in lab but fundamentally unscalable; no published concept for a commercial-scale high-density D-T fusion cell
-- Detailed energy flow diagram: how fusion heat couples to Brayton cycle from a high-density D-T target is not described
-- Muon transport efficiency from source to target (beam optics losses)
-- Alpha particle heat deposition and management in the target
+- The active-target muon source design has no published technical specification beyond GEANT4 simulation sketches in ARPA-E slides; the pion-capture and muon-transport geometry is proprietary
+- The commercial fusion cell design is entirely unknown beyond the diamond anvil cell lab apparatus; no engineering concept for a continuously-operated power-scale cell has been published
+- The claimed 47% recirculating power fraction is a company simulation result; the efficiency chain (accelerator wall-plug efficiency, pion production cross-section, muon capture fraction, α-particle heat recapture) is not independently verified
 
 **Gaps**:
-- Commercial D-T target design (scalable beyond diamond anvil cell) — `truly-unknown` — **blocking**: the fusion cell is one of the two major system components; no design concept is published
-- Muon beam transport and coupling efficiency — `proprietary/not-yet-sourced` — **important**: determines effective muon utilization rate and energy balance
-- Target heat extraction mechanism and coupling to power cycle — `proprietary` — **important**: determines achievable thermal efficiency
+- Active-target muon source function not publicly described beyond concept sketches — `proprietary` — blocking
+- Fusion cell scale-up path (diamond anvil → power plant) not addressed anywhere — `truly-unknown` — blocking
+- Recirculating power fraction chain not independently verifiable — `proprietary` — important
 
 ---
 
@@ -64,103 +56,104 @@
 **Coverage**: Partial
 
 **Available**:
-- Muon source (conventional proton linac → pion target → muon beam): TRL 6–7 at facilities like PSI, TRIUMF; well-characterized technology
-- Active-target muon source (Acceleron's innovation — ML-optimized geometry): TRL 2–3; GEANT4 simulations completed, Bayesian optimization used, hardware "Muon Generation Vacuum Assembly" under test, beamline tests at PSI πE1.2 conducted (Sep 2024)
-- D-T target at high density: TRL 3; diamond anvil cell demonstrated to 2.2 LHD with DT cycling (Oct 2024 data shown in ARPA-E presentation), but this is a measurement apparatus, not a heat-extracting power target
-- Tritium breeding blanket: TRL 4–5 for D-T blanket technology generically; specific design unspecified for μCF
-- Brayton cycle power conversion: TRL 8–9; mature technology from gas turbine and sCO2 programs
-- Superconducting accelerator for commercial system: TRL 4–5 (SNS/CEBAF provide existence proof; Acceleron's specific design is not yet developed)
+- **D-T fusion physics**: TRL 6 — demonstrated repeatedly at PSI, TRIUMF, LAMPF at research scales
+- **Conventional proton/pion accelerator for muon production**: TRL 4–5 — existing research facilities (PSI πE1.2 beamline, used by Acceleron in 2024 tests); the SNS superconducting linac (OSTI source) operates at TRL 8–9 at 1 GeV/1.4 MW with 99.5% SRF cavity availability, demonstrating the accelerator technology base
+- **High-density D-T target at lab scale (diamond anvil cell)**: TRL 3 — Acceleron demonstrated compression to 2.2 LHD in solid DT (Oct 2024), with pressure/temperature cycling data shown in ARPA-E presentation
+- **Brayton cycle power conversion**: TRL 8–9 — commercially mature technology
+- **Tritium handling systems**: TRL 5–6 — well-established for D-T programs (ITER, ORNL); standard blanket TRL assessed at 4–5
+- **Neutron shielding (14 MeV, D-T)**: TRL 7–8 — no plasma confinement required; conventional radiation shielding infrastructure applies
+- **Novel active-target muon source (Acceleron's key innovation)**: TRL 2–3 — physics simulations (GEANT4 + Bayesian ML optimization), no published hardware validation of the energy cost improvement. ML-optimized geometry is at simulation stage.
 
 **Missing**:
-- TRL for the full integrated system: not formally assessed
-- Commercial fusion cell (heat-extracting, scalable): TRL 1–2, no published design
-- Energy gain (Q>1) demonstration: planned at Brookhaven ~2030
+- No published hardware validation of the active-target accelerator design; 3.4 GeV/muon claim is simulation-only (Acceleron ARPA-E 2025)
+- No TRL assessment for commercial fusion cell (power-plant scale); the diamond anvil cell is clearly TRL 3 at lab scale with no scale-up path published
+- No TRL assessment for tritium breeding blanket (type unspecified; blanket shown in system diagram without specification)
 
 **Gaps**:
-- No TRL self-assessment from Acceleron or third party — `proprietary/not-yet-sourced` — **important**: ARPA-E BETHE program context implies TRL 2–4 for key components
-- Commercial-scale fusion cell TRL — `truly-unknown` — **important**: no design path published
+- Active-target muon source TRL unvalidated (simulation-only claim at TRL 2–3) — `proprietary` — blocking
+- Commercial fusion cell TRL undefined (no power-plant design exists) — `truly-unknown` — blocking
+- Tritium breeding blanket specification absent — `proprietary` — important
 
 ---
 
 ### 4. Key Materials and Supply Chain Considerations
-**Coverage**: Poor
+**Coverage**: Partial
 
 **Available**:
-- D-T fuel: standard supply chain considerations apply (lithium-6 for tritium breeding, same as all D-T concepts)
-- Niobium for SRF cavities: SNS operational experience confirms supply chain is mature and reliable for multi-cryomodule systems
-- Diamond (current test system): diamond anvil cell used for DT compression in lab setting; clearly not a commercial supply chain item
+- **Tritium supply**: same D-T tritium supply constraints as all D-T concepts; lithium-6 breeding blanket analog well-established. Wikipedia notes lithium-6 neutron capture as the standard breeding path.
+- **Deuterium**: abundant, commercially available, no supply constraint
+- **Superconducting accelerator materials (niobium, REBCO if HTS)**: commercial supply chains exist; SNS linac (OSTI) documents 10-year operational experience with niobium SRF cavities — field emission, multipacting, and cryomodule maintenance are known failure modes
+- **Diamond anvil cell materials**: diamonds used in lab experiments are not scalable to power-plant operation; an entirely different containment approach would be needed at commercial scale
 
 **Missing**:
-- Blanket material specification (FLiBe, LiPb, solid ceramic — not disclosed)
-- Accelerator material quantities at commercial scale (niobium, cryogenic helium)
-- High-density D-T target material for commercial system (diamond anvil cell cannot scale; replacement material/geometry not specified)
-- Tritium breeding ratio (TBR) for the blanket design
+- The commercial fusion cell material requirements are undefined (no power-plant design); it is unclear whether diamond anvil cells are even part of the commercial concept or just the current experimental apparatus
+- Breeding blanket material choice (FLiBe, LiPb, solid ceramic) unspecified
+- Accelerator structural and cryogenic materials specification absent at the commercial-scale
 
 **Gaps**:
-- Blanket material and TBR — `proprietary` — **important**: determines tritium self-sufficiency
-- Commercial fusion target material — `truly-unknown` — **blocking**: current diamond anvil cell approach is explicitly a test apparatus, not a scalable approach; commercial replacement is unspecified
-- Accelerator material quantities and supply chain — `derivable` (from SNS analog + published accelerator design rules) — **nice-to-have**
+- Commercial fusion cell material requirements entirely undefined — `truly-unknown` — important
+- Tritium breeding blanket material unspecified — `proprietary` — important
+- No supply chain bottleneck analysis for novel muon source components — `not-yet-sourced` — nice-to-have
 
 ---
 
 ### 5. LCOE Parameter Extraction
-**Coverage**: Poor
-
 **Available Parameters**:
 | Parameter | Value/Range | Source | Confidence |
 |-----------|-------------|--------|------------|
-| LCOE target | $0.025/kWh | ARPA-E 2025 | low (target, not validated) |
-| Recirculating power fraction | 47% | ARPA-E 2025 | low (claimed; conflicts with Kelly et al. 2021 at current physics) |
-| Beam energy per muon | 3.4 GeV (target) | ARPA-E 2025 | low (not yet demonstrated) |
-| Fusions per muon | 300 (target) / 150 (demonstrated) | ARPA-E 2025 / Wikipedia | medium for experimental, low for target |
-| Alpha-sticking probability | 0.3–0.9% | Wikipedia / Kamimura 2021 | medium |
-| Plant electric output | ~100 MW (target) | Company website | low |
-| Energy conversion cycle | Brayton (unspecified type) | ARPA-E 2025 | low |
-| Revenue model | Heat sales included in LCOE | ARPA-E 2025 | medium |
-| Independent electrical Q | ~14% of input (current physics) | Kelly/Hart/Rose 2021 (via Wikipedia) | medium |
-| Muon source type | SC proton linac (commercial design) | ARPA-E 2025 | low |
+| LCOE target | $0.025/kWh | Acceleron ARPA-E 2025 | low |
+| Beam energy per muon | 3.4 GeV | Acceleron ARPA-E 2025 | low |
+| Fusions per muon (target) | 300 | Acceleron ARPA-E 2025 | low |
+| Fusions per muon (demonstrated) | 100–150 | LAMPF (Jones et al.), Wikipedia | high |
+| α-sticking probability | 0.3–0.9% | arXiv:2112.08399 (Kamimura 2021) | medium |
+| Recirculating power fraction | 47% | Acceleron ARPA-E 2025 | low |
+| Gross Q (thermal, Kelly 2021 model) | ~130% (current) | Wikipedia/Kelly 2021 | medium |
+| Net electrical efficiency (current) | ~14% (current) | Wikipedia/Kelly 2021 | medium |
+| Reactor scale | ~100 MW | Acceleron website | low |
+| Energy capture cycle | Brayton (unspecified subtype) | Acceleron ARPA-E 2025 | low |
+| D-T MFE BOP capital cost (analog) | $8,800–$22,200/kW (350 MWe tokamak) | `knowledge/sources/tea_dt_mfe_cost_analysis/` | medium |
+| Modular D-T fusion LCOE (analog floor) | $34–54/MWh for ~500 MWe | `knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/` | medium |
+| SRF linac availability (accelerator analog) | 99.5% SRF cavity, 90–92% facility | `knowledge/sources/osti-servlets-purl-1345779` (SNS SCL) | high |
+
+Note on fleet-source integration: The TEA D-T MFE analysis (`tea_dt_mfe_cost_analysis/`) provides capital cost structure for D-T balance-of-plant (thermal conversion, tritium breeding, shielding, O&M), applicable as an analog for μCF's non-accelerator plant costs, but does not resolve the blocking accelerator cost gap. The ARPA-E ALPHA revisit (`revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`) provides a compact modular fusion BOP cost floor (~$2.4/W, $43/MWh LCOE average for 4 plasma-based ALPHA concepts), useful as a lower-bound analog but does not include μCF. Neither source provides accelerator cost data applicable to μCF — the dominant cost driver remains completely uncharacterized.
 
 **Missing Parameters**:
 | Parameter | Gap Type | Criticality | Notes |
 |-----------|----------|-------------|-------|
-| Capital cost by subsystem (CAS structure) | proprietary | blocking | No published breakdown; accelerator dominates but no cost given |
-| O&M cost | proprietary | blocking | No plant-level operational cost estimate available |
-| Capacity factor / availability | not-yet-sourced | blocking | SNS linac achieves 92% availability as analog; μCF-specific estimate absent |
-| Thermal-to-electric efficiency (Brayton cycle) | derivable | important | sCO2 ~45–50%; not confirmed for this design |
-| Tritium breeding ratio | proprietary | important | Blanket design unspecified |
-| Muon source capital cost scaling | truly-unknown | blocking | No published cost model for active-target muon source |
-| D-T fusion cell capital cost | truly-unknown | blocking | No commercial design exists to cost |
-| Plant-level energy balance | proprietary | important | 47% recirculating is a headline number; subsystem breakdown missing |
-| Decommissioning cost | derivable | nice-to-have | Can use D-T MFE analogs |
-| Heat-sale revenue assumption | not-yet-sourced | nice-to-have | Mentioned but revenue split not defined |
+| Accelerator capital cost (dominant cost driver) | proprietary / truly-unknown | blocking | No published cost for novel active-target design; conventional accelerators (PSI) cost tens of millions for research-scale; commercial-scale unknown |
+| Fusion cell capital cost | truly-unknown | blocking | No power-plant-scale cell design exists; diamond anvil cell is not a cost analog |
+| Validated system energy balance | proprietary | blocking | 47% recirculating power claim and 300 fusions/muon target are unvalidated simulation results; current state gives 14% net electrical efficiency (Kelly 2021) |
+| Accelerator O&M cost | not-yet-sourced | important | SNS SCL paper gives operational analog; detailed O&M fractions for μCF-scale linac not derived |
+| Tritium breeding system cost | not-yet-sourced | important | D-T MFE blanket cost analogs exist in fleet sources; blanket type unspecified blocks direct application |
+| Power conversion efficiency and cost | proprietary | important | Brayton cycle mentioned; subtype, efficiency, and cost not specified |
+| Capacity factor / plant availability | truly-unknown | important | No plant study; accelerator availability analog (~90–92% for SNS) suggestive but unconfirmed for this application |
+| O&M cost structure | not-yet-sourced | important | ARPA-E ALPHA revisit BOP O&M fractions applicable as analog but not μCF-specific |
+| Net electric output per module | proprietary | important | 100 MW scale mentioned on website; not confirmed in technical documents |
 
 ---
 
 ## Source Recommendations
 
-1. **Kelly, Hart & Rose (2021), "An investigation of efficient muon production for use in muon catalyzed fusion," *J. Phys.: Energy* 3, 035003** — `not-yet-sourced`. This paper (cited in Wikipedia, DOI available) provides the most rigorous independent energy balance model for μCF. **Priority acquisition**. It directly fills the gap in validating Acceleron's recirculating power claim.
-
-2. **ARPA-E BETHE program technical reports for Acceleron** — `proprietary/not-yet-sourced`. ARPA-E publishes some progress reports for funded projects. Search ARPA-E project database for "Acceleron" or "Conditions for High-Yield Muon Catalyzed Fusion" (the BETHE project title visible in Wikipedia reference [9]). May contain more engineering detail than the public presentation.
-
-3. **Jändel, Danos & Rafelski (1988), "Active target production of muons for muon-catalyzed fusion," *Phys. Rev. C* 37, 403** — `not-yet-sourced`. This paper introduced the active-target concept that Acceleron is implementing. Would clarify physics basis and original energy cost estimates. Available via DOI in Wikipedia references.
-
-4. **SNS/CEBAF accelerator cost reports** — `not-yet-sourced`. Published DOE project reports for the Spallation Neutron Source (SNS) include capital cost breakdowns for a ~1 GeV SC proton linac, which is the closest engineering analog to Acceleron's muon source. Search OSTI for "SNS construction cost" or "SNS project baseline." `unverified — confirm existence before searching`.
-
-5. **Pusch (1996) alternative breakeven analysis and migma concept** — `not-yet-sourced`. Referenced in Wikipedia; available as a Usenet archive post. Provides an alternative energy balance model for μCF that includes target heat deposition, affecting the recirculating power estimate.
-
-6. **Norrønt AS technical publications** — `not-yet-sourced`. Second commercial μCF company. Any published materials would enable competitive comparison. `unverified — confirm existence before searching`.
+- **Norrønt AS (Norway) publications** — second μCF company; search their website and Google Scholar for any system design documents. `not-yet-sourced` — `unverified — confirm existence before searching`
+- **Kelly, Hart & Rose (2021), "An investigation of efficient muon production for use in muon catalyzed fusion," J. Phys. Energy 3(3)** — already cited in Wikipedia as the authoritative energy balance model; full paper extraction via DOI `10.1088/2515-7655/abfb4b` would provide quantitative LCOE parameter sensitivities. `not-yet-sourced`
+- **Jändel, Danos & Rafelski (1988), "Active target production of muons for muon-catalyzed fusion," Phys. Rev. C 37, 403** — the original active-target concept paper; provides theoretical basis for Acceleron's muon source design. `not-yet-sourced`
+- **ARPA-E BETHE program technical reports for Acceleron project** — search ARPA-E project database for published deliverables under "Conditions for High-Yield Muon Catalyzed Fusion" (Ara Knaian/Acceleron). `not-yet-sourced` — `unverified — confirm existence before searching`
+- **PSI muon facility operating cost literature** — PSI πE1.2 beamline operating reports could provide accelerator energy cost benchmarks (muons/kWh at existing facility). `not-yet-sourced`
+- **Disqualified fleet sources**: The following fleet-wide sources were opened and do not address μCF-specific gaps:
+  - `knowledge/sources/overview_of_the_helios_design_a_practical_planar_coil/` — stellarator-specific (planar coils, HTS magnets); no overlap with μCF's dominant cost driver (accelerator)
+  - `knowledge/sources/a_simplified_economic_model_for_inertial_fusion/` — Monte Carlo IFE LCOE model parameterized by target gain, fusion energy per shot, and driver efficiency; none of these map to μCF architecture
+  - `knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/` — HIF driver-dominated cost model; driver cost structure superficially similar but the physics (GJ-scale heavy-ion beam vs. continuous muon beam) makes it a poor analog
+  - `knowledge/sources/energy_from_inertial_fusion/` — 1992 IFE review; no μCF content
+  - `knowledge/sources/accelerators_for_inertial_fusion_energy_production/` — IFE driver review; covers induction linacs and RF linacs for target compression, not continuous muon production
+  - `knowledge/sources/commercialization_of_laser_fusion_energy/` — Xcimer KrF laser IFE; no overlap with μCF
+  - `knowledge/sources/affordable_manageable_practical_and_scalable_amps_high/` — Pacific Fusion high-yield IFE; no overlap with μCF
+  - `knowledge/sources/an_assessment_of_the_economics_of_future_electric_power/` — historical ORNL LCOE benchmarking; provides electricity cost context but no μCF-specific parameters
 
 ---
 
 ## Summary
 
-**Proceed to full qualitative + partial quantitative analysis, but flag limitations explicitly.**
-
-The physics of muon-catalyzed fusion is well-documented and can support a thorough qualitative analysis of system function, TRL, and challenges. The Kelly et al. (2021) parametric model (accessible via cited DOI) provides an independent energy balance framework superior to Acceleron's single-headline numbers. Acceleron's ARPA-E 2025 presentation gives enough parameters for a first-order LCOE sensitivity analysis against the physics space (the parametric contour plot they show is itself a useful starting point).
-
-However, quantitative LCOE extraction is blocked by the absence of any published capital cost breakdown — the muon source and fusion cell together constitute the concept-defining cost structure, and neither has a published design or cost estimate at commercial scale. The analysis should present the physics-derived parameter sensitivity (fusions/muon vs. beam energy/muon vs. LCOE) as the primary quantitative output, with a clear statement that bottom-up capital cost estimation is not possible from available sources.
-
-Acquiring the Kelly et al. (2021) paper should be the first priority before finalizing the analysis.
+Proceed to a partial D1+ analysis with explicit scope boundaries. The physics foundation is strong enough to write thorough sections on system function, subsystem maturity, and materials. The LCOE section should present Acceleron's parametric target ($0.025/kWh at 300 fusions/muon, 3.4 GeV/muon, 47% recirculating power) as an aspirational upper bound, contrast it with the Kelly 2021 model (14% net electrical efficiency at current state), and build a sensitivity framework around the two key physics parameters — fusions per muon and muon energy cost — that Acceleron's LCOE contour plot itself identifies as the pivotal variables. Additional sourcing (Kelly 2021 full paper, PSI facility operating data, ARPA-E project deliverables) would materially improve quantitative rigor but is not required to proceed with a qualified analysis.
 
 ---
 
@@ -168,13 +161,13 @@
 
 ```yaml
 overall_rating: "Significant Gaps"
-blocking_count: 5
-important_count: 6
-counting_method: "all_sections_deduplicated — blocking: (1) plant engineering design absent, (2) muon source capital cost unknown, (3) commercial fusion cell design/cost unknown, (4) O&M cost unpublished, (5) capacity factor not estimated; important: (1) Kelly et al. energy balance not sourced, (2) thermal efficiency unspecified, (3) TBR/blanket design unknown, (4) muon beam transport efficiency, (5) target heat extraction mechanism, (6) plant-level energy balance subsystem detail"
+blocking_count: 3
+important_count: 5
+counting_method: "deduplicated_across_all_sections — three unique blocking gaps: (1) novel active-target muon source unvalidated and uncosted, (2) commercial fusion cell undefined and uncosted, (3) 47%-recirculating-power / 300-fusions-per-muon energy balance unvalidated. Five unique important gaps: tritium blanket specification, power conversion specification, capacity factor, O&M structure, and alpha-sticking at operating density."
 section_coverage:
   availability_of_data:       "Partial"
   system_function:            "Partial"
   subsystem_maturity:         "Partial"
-  materials_supply_chain:     "Poor"
+  materials_supply_chain:     "Partial"
   lcoe_parameter_extraction:  "Poor"
 ```
\ No newline at end of file
```
