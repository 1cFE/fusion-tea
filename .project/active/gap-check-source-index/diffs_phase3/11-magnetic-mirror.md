# Phase 3 diff: 11-magnetic-mirror

**Generated:** 2026-05-22T14:03:14-07:00

## Counts (Phase 2 -> Phase 3 strict-read regen)

| field | phase2 | phase3 | Δ |
|-------|--------|--------|---|
| blocking_count   | 3 | 6 | 3 |
| important_count  | 8 | 7 | - |
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
I have all the information needed. Here is the full gap assessment report:
```

## Blocking-tier lines (new)

```
96:| Fusion thermal power output (Pfus, Pth) | proprietary | blocking | 7 MW/m × 50 m = ~350 MW rough estimate, but not published; Hammir design paper needed |
97:| Gross/net electric output (Pnet) | proprietary | blocking | Only "≥ 50 MWe" target stated; actual value not given |
98:| Thermal conversion efficiency (Rankine/sCO2 cycle) | proprietary | blocking | Thermal cycle unspecified; standard steam (~33%) vs. sCO2 (~45%) would materially affect LCOE |
99:| DEC conversion efficiency for Hammir | proprietary | blocking | No published value; MARS 54% is an unvalidated analog from a different design era |
100:| NBI wall-plug efficiency | not-yet-sourced | blocking | Determines circulating power fraction; ITER-heritage negative-ion NBI ~28–30% wall-plug efficiency plausible but not confirmed for Hammir |
101:| Capital cost breakdown by subsystem (CAS) | proprietary | blocking | No plant study published; ARPA-E ALPHA provides modular D-T MFE analog but mirror-specific cost structure (DEC, simpler magnets, linear blanket) differs |
```

## Full unified diff (truncated to 400 lines)

```diff
--- /tmp/gap_phase2_state/11-magnetic-mirror.md	2026-05-22 12:59:21.065273719 -0700
+++ /home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/11-magnetic-mirror/gap_report.md	2026-05-22 14:03:14.614857800 -0700
@@ -1,19 +1,10 @@
-I have enough information from the concept-scoped sources to write the assessment. Let me also note which fleet-wide sources are applicable before writing.
-
-From the source index, the applicable fleet-wide sources for Magnetic Mirror (D-T) are:
-- **TEA D-T MFE Cost Analysis** — D-T MFE LCOE methodology and CAS breakdowns
-- **Revisit of the 2017 Costing for Four ARPA-E ALPHA Concepts** — multi-concept CAS costing framework (alternative fusion concepts, same budget era)
-- **ARIES Cost Account Documentation** — CAS hierarchy reference
-
-I'll now write the gap assessment.
-
----
+I have all the information needed. Here is the full gap assessment report:
 
 # Gap Assessment: Magnetic Mirror (D-T)
 
 ## Overall Readiness
-**Rating**: Mostly Ready  
-**Summary**: The qualitative sections are well-supported by a combination of Realta's published physics paper, two interviews, a conference talk, and the WHAM experiment website. Physics operating points, technology roadmap, stability challenges, and the hybrid energy capture architecture are all documented with reasonable confidence. The LCOE parameter extraction section is the weak spot: no plant-level capital cost breakdown, no O&M estimates, and no BOP thermal cycle details have been published by Realta. The historical MARS study and fleet-wide MFE TEA sources provide partial analogues but cannot substitute for a Realta-specific plant study.
+**Rating**: Significant Gaps
+**Summary**: The concept has solid physics-basis documentation and a credible technology roadmap, with peer-reviewed modeling (arXiv 2411.06644) establishing Q > 5 as feasible for a 50 m center cell and a clear three-step development path (WHAM → Anvil → Hammir). However, no plant-level design study for Hammir has been published — Realta has confirmed a pre-conceptual design paper is expected in 2026 but it is not yet available. This means the core quantitative LCOE inputs (fusion thermal power, conversion efficiency chain, capital cost by subsystem) are absent or must be estimated from fleet-wide analogs. The qualitative sections (system function challenges, subsystem maturity, materials considerations) are well-supported for a D1+ analysis; the LCOE parameter table will require explicit assumptions flagged with low confidence until the Hammir design paper appears.
 
 ---
 
@@ -22,166 +13,142 @@
 ### 1. Availability of Data
 **Coverage**: Partial
 
-**Available**:
-- Company transparency is above average for an early-stage fusion startup. Realta has published a peer-reviewed physics paper (arxiv-2411-06644), an APS DPP 2025 conference presentation, two detailed public interviews (Fusion Hub, The Fusion Report), and a DOE Milestone award (ARPA-E).
-- Technology roadmap (WHAM → Anvil → Hammir) with specific milestones (Qe > 1, Pe,out > 50 MWe, 3 hr continuous) is well-documented (`aps-dpp-2025-sutherland.md`, `arxiv-2411-06644`).
-- Funding history is traceable: $10M ARPA-E → $36M Series A (May 2025) → $9.5M SVB debt facility (Feb 2026) (`realta-svb-funding-feb2026.md`).
-- The MARS study (1980s, cited in dossier) provides an older-generation tandem mirror plant study with blanket, shielding, and DEC architecture details — useful as a structural analog even if cost figures require escalation and technology adjustment.
-- Historical GDT (Russia) and Gamma-10 (Japan) mirror experiments provide physics validation data cited in the arxiv paper.
-
-**Missing**:
-- No published plant-level engineering study or techno-economic analysis from Realta. The Hammir pre-conceptual design paper is stated to be expected in 2026 but not yet available.
-- No cost estimates (capital or operating) from Realta or from any independent study of the modern tandem mirror concept.
-- No third-party validation or review of Realta's physics modeling outputs.
+**Available**: Physics modeling paper (arXiv 2411.06644) provides integrated transport and equilibrium model for Hammir, demonstrating Q > 5 with 50 m center cell and Q > 10 with longer center cell, with a publicly-available POPCON technique for tandem mirrors. The Fusion Hub spotlight provides detailed physics explanation covering confinement mechanisms, instability challenges, and the DEC concept. The Fusion Report interview confirms D-T fuel, lithium-based tritium breeding, ~7 MW/m power scaling, and identifies industrial heat as the primary market. APS DPP 2025 abstract (Sutherland) confirms the Hammir pilot plant targets (Qe > 1, > 50 MWe, ≥ 3 hours). Funding disclosures (SVB $9.5M debt, $36M Series A) confirm ongoing company viability. The dossier summarizes WHAM experiment results (17 T HTS, first plasma July 2024). Fleet-wide analog sources supply CAS-level cost frameworks: the ARPA-E ALPHA re-costing (`knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`) provides complete line-item capital costs for four modular compact fusion concepts averaging ~$1.2B total capital and LCOE 34–54 $/MWh for ~500 MWe NOAK plants, directly applicable as a BOP analog; the TEA D-T MFE source (`knowledge/sources/tea_dt_mfe_cost_analysis/`) provides a bottom-up CAS cost framework for an HTS D-T MFE plant with LCOE $140–550/MWh and capital $8,800–22,200/kW.
+
+**Missing**: No published Hammir pre-conceptual design report. No detailed neutronics study for the linear mirror geometry. MARS study (cited in dossier as a key historical reference with LiPb blanket, 36% plant efficiency, TBR 1.15) is not ingested as a source.
 
 **Gaps**:
-- Hammir pre-conceptual design paper — `not-yet-sourced` — **important**: would resolve blanket type, BOP architecture, NBI power budgets
-- Independent techno-economic study of modern tandem mirror — `truly-unknown` — **important**: no published independent cost analysis exists for this concept generation
+- Hammir pre-conceptual design paper — proprietary/not-yet-sourced — blocking (this paper is the primary vehicle for plant-level data)
+- MARS Mirror Advanced Reactor Study — not-yet-sourced — important (historical mirror plant study with TBR, efficiency, and DEC data)
 
 ---
 
 ### 2. Challenges in Capturing System Function
-**Coverage**: Good
+**Coverage**: Partial
+
+**Available**: The sources collectively identify and partially characterize the key functional challenges. The physics paper (arXiv 2411.06644) identifies DCLC instability management as an open item and notes that kinetic stability modeling via Hybrid-VPIC integration is "in preparation." The Fusion Hub source covers MHD stability (vortex/sheared-flow stabilization for interchange modes, exploiting good curvature in expander regions), kinetic instability management (sloshing ions to fill ambipolar hole), impurity accumulation in tandem vs. simple mirror configurations, and low electron temperature as a historical challenge now addressed by ECH. The dossier notes that the Anvil end-plug demonstrator is specifically designed to validate stabilization concepts before Hammir is built. The hybrid energy capture architecture (thermal blanket + venetian blind DEC) is described qualitatively; the MARS study achieved ~54% DEC efficiency (referenced in dossier) but this is an unverified analog for Hammir's design. The 7 MW/m power-per-meter scaling law captures center cell performance but leaves end-plug power accounting incompletely specified.
 
-**Available**:
-- The key physics challenges are well-documented: DCLC kinetic instability (managed via sloshing ions), MHD interchange instability (managed via vortex stabilization and good-curvature expander regions), and electron temperature management via ECH (`realta-fusion-hub-spotlight.md`, `arxiv-2411-06644`).
-- The power balance architecture is described: NBI + ECH heating remains dominant at Q > 5 (i.e., not alpha-dominated), meaning recirculating power fraction is significant and DEC is critical to achieving Qe > 1 (`fusion-report-interview-realta.md`).
-- The scaling law (~7 MW per additional meter of center cell, with constant input power) is a distinctive feature that simplifies power-per-unit-length modeling (`fusion-report-interview-realta.md`).
-- The arxiv paper provides high-fidelity integrated modeling (RealTwin = CQL3D-m + Pleiades) and POPCON analysis for Hammir operating points, with quantitative parameters for the end-plug design.
-- Impurity management in tandem mirrors is acknowledged as an open challenge (higher confinement of impurities vs. simple mirrors due to end-plug potential) (`realta-fusion-hub-spotlight.md`).
-
-**Missing**:
-- Specific NBI power levels (MW input) and ECH power levels for Hammir at steady state — the arxiv paper addresses end-plug physics but doesn't clearly state total plant heating power.
-- HHFW (High Harmonic Fast Wave) role in the full Hammir design is described qualitatively for WHAM but not quantified for the pilot plant.
-- Plasma-material interaction (PMI) modeling for the linear geometry first wall — acknowledged as a challenge but unstudied publicly for Realta's design.
-- Quantitative recirculating power fraction (NBI + ECH / gross electric output) for Hammir.
+**Missing**: NBI wall-plug efficiency — critical for computing Qe from Qsci; no value published for Hammir operating conditions. DEC conversion efficiency specific to Hammir's design not published (MARS 54% is the only analog). Quantitative vortex stabilization power requirements not given. Impurity transport and radiation loss in the tandem configuration remains an acknowledged open question (Fusion Hub source notes this "remains to be seen"). Anvil physics data (which would validate end-plug stabilization) does not yet exist.
 
 **Gaps**:
-- Total steady-state heating power budget for Hammir — `proprietary` — **important**: needed to calculate recirculating power and net electric gain
-- First wall heat flux and PMI quantification — `not-yet-sourced` (may exist in MARS study or similar) — **nice-to-have**
+- NBI wall-plug efficiency for Hammir operating point — proprietary/not-yet-sourced — blocking (required to compute Qe from physics Q)
+- DEC conversion efficiency (venetian blind, Hammir-specific) — proprietary — blocking (DEC efficiency determines fraction of energy directly converted vs. thermal; assumed 54% from MARS is low confidence)
+- Impurity transport and radiation loss quantification — truly-unknown — important (acknowledged gap in published arXiv paper; affects power balance)
+- Vortex stabilization power requirement — not-yet-sourced/proprietary — important (determines parasitic heating load)
+- Anvil end-plug experimental validation — truly-unknown — important (no data until ~2028)
 
 ---
 
 ### 3. Maturity of Key Subsystems and Components
 **Coverage**: Partial
 
-**Available**:
-- **HTS mirror magnets (REBCO)**: TRL 5–6. WHAM demonstrated 17 T in a full axisymmetric mirror configuration using CFS-built REBCO coils (operational July 2024). This is hardware-demonstrated at experiment scale (`wham-experiment-details.md`, `aps-dpp-2025-sutherland.md`).
-- **NBI (neutral beam injection)**: TRL 6–7. Modern negative-ion neutral beams cited as a key enabling technology are mature from tokamak programs (ITER NBI). Not yet demonstrated in a mirror end-plug role at the required parameters.
-- **ECH (110 GHz gyrotrons)**: TRL 6–7. Gyrotron technology mature from tokamak programs; used on WHAM.
-- **Tandem mirror end-plug physics**: TRL 3–4. Axisymmetric tandem mirror end-plug physics has not been demonstrated at the required density and temperature — this is Anvil's mission (~2028 target). The arxiv paper validates modeling but not hardware.
-- **Direct energy conversion (venetian blind)**: TRL 3–4. The axisymmetric venetian blind DEC concept is described but not demonstrated at power-plant scale. MARS study achieved ~54% DEC efficiency in analysis; Realta has not published efficiency targets (`dossier.md`).
-- **Li blanket for tritium breeding + neutron capture**: TRL 4–5 (for fusion applications broadly). Specific blanket design for linear geometry not published.
-- **Pilot plant central cell (50m, full tandem)**: TRL 2. Exists only as simulation outputs (arxiv paper). Hammir as a device does not yet have a hardware design.
-
-**Missing**:
-- TRL assessment for vortex stabilization at scale (the MHD mitigation approach) — demonstrated on GDT (Russia) but not integrated into an HTS tandem mirror.
-- First-wall materials choice and lifetime estimates for Hammir neutron environment — not yet published.
-- WHAM++ (the intermediate scientific breakeven device) — described in FusionHub as needing ~$50M in REBCO tape, suggesting it may not be built and Anvil is the next step (`realta-fusion-hub-spotlight.md`). This creates a step gap in the validation ladder.
+**Available**: HTS REBCO magnets are the most mature subsystem — WHAM demonstrates 17 T in a mirror configuration (TRL 7 for magnets at this field strength, TRL 6 for mirror-geometry deployment), with CFS as an established supplier. ECH/gyrotron heating at 110 GHz is at TRL 6–7 (operational on WHAM, mature gyrotron technology from industry/ITER heritage). NBI is at TRL 5–6 (operational on WHAM for HHFW fueling; high-energy negative-ion NBI for pilot plant is a technology step beyond current WHAM operations, with heritage from JT-60 and ITER programs). Vortex stabilization via electric-field-driven sheared flow is at TRL 4–5 (demonstrated in GDT and referenced Russian/Japanese experiments, not yet demonstrated in an HTS high-field axisymmetric tandem mirror). The Fusion Hub source notes that the GDT achieved MHD stability, high electron temperatures (~1 keV), and mitigation of kinetic instabilities in axisymmetric mirrors, providing heritage.
+
+**Missing**: Direct energy conversion (venetian blind design) has no demonstrated modern prototype — TRL 2–3. Tritium blanket for a linear mirror geometry has no design study from Realta — TRL 3. First wall / plasma-facing components for the tandem mirror geometry (PMI under 14.1 MeV neutron flux) have no published study — TRL 2–3. The Anvil device (end-plug demonstrator, ~2028) is the critical next step but has not been built.
 
 **Gaps**:
-- End-plug physics demonstration (Anvil) is 2+ years out — `proprietary` — **blocking for hardware validation** but not for concept analysis; POPCON modeling gives sufficient analytical basis
-- DEC efficiency quantification for Hammir design — `not-yet-sourced` (MARS study provides 54% historical analog) — **important**
-- First-wall materials/lifetime for Hammir — `not-yet-sourced` — **nice-to-have**
+- DEC (venetian blind) subsystem maturity — truly-unknown — blocking (no published modern prototype; MARS used gridless converters, Realta's design is unspecified; TRL 2–3 with no roadmap to TRL 4 prior to Hammir)
+- First wall / plasma-facing components for tandem mirror geometry — not-yet-sourced — important (PMI with 14.1 MeV neutrons in open-ended geometry not studied for Hammir)
+- Tritium blanket design and TRL — proprietary/not-yet-sourced — important (blanket type unspecified; linear geometry simplifies design but no published study)
+- Anvil device maturity data — truly-unknown — important (device not yet built; expected ~2028 per APS DPP abstract)
 
 ---
 
 ### 4. Key Materials and Supply Chain Considerations
 **Coverage**: Partial
 
-**Available**:
-- **REBCO HTS tape**: The FusionHub article explicitly states WHAM++ would require ~$50M in REBCO tape alone, establishing REBCO as the dominant materials cost driver. Magnet supply chain is tied to CFS (Commonwealth Fusion Systems), which is an active supplier but a competitor in the fusion space (`realta-fusion-hub-spotlight.md`).
-- **Tritium**: D-T fuel cycle requires tritium breeding; Li blanket confirmed for this purpose. Tritium supply constraints are a fleet-wide issue, not specific to Realta, but apply here.
-- **Lithium**: Required for tritium breeding blanket; specific isotopic enrichment (Li-6) needs would depend on blanket design (unspecified by Realta).
-- **NBI components**: Mature supply chain (ITER, JET experience), no specific bottleneck identified for Realta's scale.
-- **Mirror coil geometry (axisymmetric)**: Described as simpler than stellarator or tokamak coils — this is a supply-chain advantage over 3D coil geometries.
-
-**Missing**:
-- REBCO tape volume estimates for Hammir (only WHAM++ estimate available; Hammir is a different configuration).
-- Tritium inventory and fueling rate for Hammir — no published estimate from Realta.
-- Supply concentration risk: CFS is currently the only named supplier of REBCO coils for Realta; no alternative supplier path described.
+**Available**: REBCO HTS tape supply chain is partially characterized. CFS is the current magnet manufacturer for Realta (WHAM magnets). The Fusion Hub source mentions ~$50M in REBCO tape alone for WHAM++ (a scale-up device), indicating the material cost is non-trivial even at pre-pilot scale. D-T fuel cycle requirements are standard for all D-T fusion and well-characterized in the literature. Lithium for tritium breeding is confirmed as the blanket material (Fusion Report interview) but the form (LiPb, FLiBe, liquid Li, HCPB) is unspecified. ARPA-E ALPHA costing (`knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`) shows special materials (primarily primary coolant liquid metal) at $103M average for modular MFE plants, indicating non-negligible supply chain exposure.
+
+**Missing**: REBCO tape volume requirement for Hammir not disclosed — the mirror geometry uses fewer magnets than tokamaks (stated advantage) but the center cell solenoid length (~50 m) and end plug magnets need coil characterization. Structural material specification (V-alloy, ferritic steel, or other) not given. Tritium-breeding blanket material unspecified — drives both TBR and activation inventory. No supply chain analysis specific to Hammir has been published.
 
 **Gaps**:
-- REBCO tape volume/cost for Hammir — `derivable` (from magnet volume and field requirements) — **important**
-- Tritium inventory requirements — `derivable` (from fusion power and tritium burn fraction, using standard formulas) — **nice-to-have**
-- Li-6 enrichment requirements — `derivable` once blanket type is known — **nice-to-have**
-- Alternative REBCO supplier path — `not-yet-sourced` — **nice-to-have**
+- REBCO tape volume requirement for Hammir — proprietary/not-yet-sourced — important (cost driver; $50M noted for WHAM++, Hammir will require more for 50m center cell + two end plugs)
+- Blanket material specification — proprietary — important (determines Li-6 enrichment need, activation, coolant choice)
+- Structural/first wall material selection — proprietary — important (drives activation inventory, maintenance schedule, replacement cost)
+- Supply chain for DEC components at scale — truly-unknown — nice-to-have
 
 ---
 
 ### 5. LCOE Parameter Extraction
-**Coverage**: Poor
-
 **Available Parameters**:
-
 | Parameter | Value/Range | Source | Confidence |
 |-----------|-------------|--------|------------|
-| Target fusion gain Q | Q > 5 (base), Q > 10 (longer cell) | arxiv-2411-06644 | medium |
-| Net electric output target | > 50 MWe | aps-dpp-2025-sutherland.md | medium |
-| Power scaling law | ~7 MW per additional meter center cell | fusion-report-interview-realta.md | medium |
-| Plant size range | 50–500 MWe | fusion-report-interview-realta.md | low |
-| Operation mode | Steady-state (continuous) | dossier.md | high |
-| Continuous operation target | ≥ 3 hours (demonstration milestone) | aps-dpp-2025-sutherland.md | high |
-| DEC efficiency (analog) | ~54% (MARS historical) | dossier.md (cited MARS) | low |
-| REBCO tape cost indicator | ~$50M for WHAM++ (smaller device) | realta-fusion-hub-spotlight.md | low |
-| Magnet technology | HTS REBCO, 17 T demonstrated | wham-experiment-details.md | high |
-| Center cell length (Hammir) | ~50m (for Q > 5) | fusion-report-interview-realta.md | medium |
-| Fuel | D-T | dossier.md | high |
-| Energy capture split | Thermal (neutron) + DEC (charged particles) | fusion-report-interview-realta.md | high |
+| Net electric power target (Hammir) | > 50 MWe | APS DPP 2025 (Sutherland); arXiv 2411.06644 | h |
+| Fusion gain Q | > 5 (50 m cell); > 10 (longer cell) | arXiv 2411.06644; Fusion Report interview | m |
+| Electric gain Qe | > 1 | APS DPP 2025 | m |
+| Power scaling law | ~7 MW/m center cell length | Fusion Report interview (Sutherland quote) | m |
+| Fuel | D-T | All concept sources | h |
+| Energy capture mode | Hybrid thermal blanket + DEC (venetian blinds) | Fusion Hub; Fusion Report interview | h |
+| DEC efficiency analog | ~54% (MARS study, historical reference) | Dossier (cited; MARS not ingested) | l |
+| Operation mode | Steady-state | All sources | h |
+| LCOE range analog (modular compact D-T MFE, NOAK) | 34–54 $/MWh | ARPA-E ALPHA (`knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`) | m |
+| Total capital cost analog (500 MWe NOAK) | ~$1.2B, ~$2.4/W | ARPA-E ALPHA | m |
+| O&M costs analog | $48M/year avg (500 MWe) | ARPA-E ALPHA | m |
+| Fuel processing capital analog | $124M (avg, 500 MWe) | ARPA-E ALPHA | m |
+| BOP capital cost analog (turbine, electric, heat rejection) | $137M + $59M + $55M = ~$251M avg | ARPA-E ALPHA | m |
+| LCOE range analog (HTS D-T tokamak, NOAK) | $140–550/MWh | TEA D-T MFE (`knowledge/sources/tea_dt_mfe_cost_analysis/`) | l (tokamak, not mirror) |
+| Capacity factor assumption (analog) | 90% | ARPA-E ALPHA | m |
+| REBCO tape cost indicator | ~$50M for WHAM++ alone | Fusion Hub spotlight | l |
 
 **Missing Parameters**:
-
 | Parameter | Gap Type | Criticality | Notes |
 |-----------|----------|-------------|-------|
-| Capital cost by subsystem (magnets, blanket, NBI, BOP, vacuum vessel) | proprietary | blocking | No plant-level cost breakdown from Realta or independent source |
-| Total installed cost ($/kWe) | proprietary / truly-unknown | blocking | No FOAK or NOAK cost estimate published |
-| O&M annual cost ($/kWe-yr or $/MWh) | proprietary | blocking | No published estimate; no analogous modern mirror plant exists |
-| BOP thermal cycle type and efficiency (steam / sCO2) | proprietary | important | Affects overall η_thermal; can be bounded by analogy but not confirmed |
-| NBI + ECH total input power for Hammir (recirculating power fraction) | proprietary | important | Needed for net Q_e calculation; arxiv paper gives end-plug details but not total system power budget |
-| Capacity factor / plant availability | not-yet-sourced / derivable | important | Steady-state favors high CF; but no maintenance schedule or first-wall replacement interval published |
-| DEC efficiency (Realta Hammir design) | proprietary / not-yet-sourced | important | MARS gives 54% analog; Realta claims improvement but no number given |
-| Blanket TBR and tritium inventory | proprietary | important | Blanket type unspecified; TBR affects tritium self-sufficiency and fuel cost |
-| First-wall replacement schedule and cost | not-yet-sourced | important | Affects O&M; no Realta-specific data; MARS analog possible |
-| LCOE estimate or cost target | truly-unknown | important | No published LCOE or cost-of-electricity target from Realta |
-| NBI capital cost for Hammir | not-yet-sourced | important | NBI is likely a major capital line item; ITER NBI costs could serve as analog |
-| HTS magnet cost for Hammir | derivable | important | Can be estimated from REBCO tape volume × cost/kg + winding + structure |
+| Fusion thermal power output (Pfus, Pth) | proprietary | blocking | 7 MW/m × 50 m = ~350 MW rough estimate, but not published; Hammir design paper needed |
+| Gross/net electric output (Pnet) | proprietary | blocking | Only "≥ 50 MWe" target stated; actual value not given |
+| Thermal conversion efficiency (Rankine/sCO2 cycle) | proprietary | blocking | Thermal cycle unspecified; standard steam (~33%) vs. sCO2 (~45%) would materially affect LCOE |
+| DEC conversion efficiency for Hammir | proprietary | blocking | No published value; MARS 54% is an unvalidated analog from a different design era |
+| NBI wall-plug efficiency | not-yet-sourced | blocking | Determines circulating power fraction; ITER-heritage negative-ion NBI ~28–30% wall-plug efficiency plausible but not confirmed for Hammir |
+| Capital cost breakdown by subsystem (CAS) | proprietary | blocking | No plant study published; ARPA-E ALPHA provides modular D-T MFE analog but mirror-specific cost structure (DEC, simpler magnets, linear blanket) differs |
+| Magnet cost for Hammir (HTS REBCO volume) | proprietary | important | Mirror uses fewer magnets than tokamak; stated cost advantage, but no published number |
+| Blanket/tritium system capital | proprietary | important | Blanket type unspecified; analog: $57M first wall/blanket and $124M fuel processing (ARPA-E ALPHA) |
+| Capacity factor / availability assumption | proprietary | important | No published value; steady-state operation is a stated advantage but no specific CF given |
+| O&M cost (scheduled replacement, staffing) | proprietary | important | No published value; ARPA-E ALPHA analog $48M/year for 500 MWe |
+| Decommissioning cost | derivable | nice-to-have | Linear geometry may simplify decommissioning; no estimate published |
+| Neutron wall loading and first wall lifetime | truly-unknown | important | Linear geometry neutronics not studied; affects replacement schedule and maintenance cost |
 
 ---
 
 ## Source Recommendations
 
-1. **MARS study (OSTI:5981974)** — `not-yet-sourced` as an extracted document in the repo (cited in dossier but not ingested). Contains blanket design (LiPb, TBR 1.15), plant thermal efficiency (~36%), DEC architecture, and cost structure for a 1980s tandem mirror. Primary analog for plant-level parameters. Recommend ingesting via `scripts/zotero_ingest.py`. *Note: this is a real published document — confirm OSTI availability before searching.*
-
-2. **Revisit of 2017 ARPA-E ALPHA costing** (`knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`) — Already ingested. Relevant as a CAS-framework cost analog for alternative fusion concepts (~$43/MWh average, 500 MWe plants). Check whether any of the four costed concepts (FRC-based or mirror-adjacent) overlap with magnetic mirror architecture for blanket and BOP cost fractions.
-
-3. **TEA D-T MFE Cost Analysis** (`knowledge/sources/tea_dt_mfe_cost_analysis/`) — Already ingested. Provides CAS-level D-T MFE cost methodology. Applicable to CAS22 (magnets), CAS23 (power conditioning), CAS26 (heat transport), CAS27 (fuel handling) as structural analogs, even though tokamak-derived.
+- **MARS Mirror Advanced Reactor Study (Logan et al., LLNL, 1983)** — not-yet-sourced — important. This is the most detailed historical mirror power plant study. The dossier cites it for LiPb blanket (TBR 1.15), 36% plant efficiency, and ~54% DEC efficiency from gridless converters. Available on OSTI (OSTI ID 5981974 per dossier). Should be ingested before LCOE parameter extraction. Contains TBR, blanket design, power balance, and DEC subsystem data that would downgrade several "important" gaps. *Verify existence via OSTI before searching — reference appears in dossier.*
 
-4. **Forest et al. 2024 — BEAM device design paper** — Cited in arxiv-2411-06644 as the predecessor to Anvil. May contain quantitative device parameters (dimensions, magnet specs, NBI power) useful for Hammir scaling. Search: `arxiv "BEAM" "break-even axisymmetric mirror" Forest 2024`. *Unverified — confirm existence before searching.*
+- **Forest et al. (2024) — BEAM (Break-even Axisymmetric Mirror) design** — not-yet-sourced — important. Referenced in arXiv 2411.06644 as the design basis for the Anvil device. May contain system-level parameters (plasma radius, field, NBI power, plasma performance) useful for scaling to Hammir. Search arXiv or Google Scholar for "Forest 2024 break-even axisymmetric mirror BEAM." *Unverified — confirm existence before searching.*
 
-5. **Logan 1983 / MARS full study** — The tandem mirror MARS study from LLNL (Logan, 1983). Multiple OSTI records exist. May contain detailed cost breakdowns, DEC efficiency analysis, and blanket design that are structurally analogous to Hammir even with technology differences. *Unverified full content — confirm OSTI availability.*
+- **Realta Fusion DCLC instability paper (announced in Fusion Report interview alongside Q > 5 paper)** — not-yet-sourced — important. A second paper (on DCLC instability engineering solutions) was announced concurrent with arXiv 2411.06644. This paper should contain power requirements for kinetic stabilization. Search arXiv for Realta Fusion DCLC 2024–2025. *Unverified — confirm existence before searching.*
 
-6. **Realta Fusion Hammir pre-conceptual design paper** — Stated in dossier as expected 2026. Monitor arXiv (search: "Hammir" OR "tandem mirror pilot plant Realta") and PRNewswire for announcement. This is the single most important missing source.
+- **GDT (Gas Dynamic Trap) experimental publications** — not-yet-sourced — nice-to-have. The Fusion Hub source identifies Russian GDT as the heritage for axisymmetric mirror stability. GDT achieved ~1 keV electron temperatures and MHD stability. Vortex stabilization data from GDT would constrain the parasitic heating load for this mechanism. Search OSTI or Google Scholar for "GDT mirror vortex stabilization" or "Bagryansky mirror 2015–2020."
 
-7. **ITER NBI cost data** — For NBI capital cost analog. Search OSTI or ITER documentation for NBI system cost breakdown. *Unverified — confirm existence before searching.*
+- **Fleet-wide sources assessed and integrated above** (ARPA-E ALPHA re-costing, TEA D-T MFE): both integrated into Section 5 parameter tables with specific values cited. See parameter table rows citing `knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/` and `knowledge/sources/tea_dt_mfe_cost_analysis/`.
+
+- **Fleet-wide sources assessed and disqualified**:
+  - *A simplified economic model for inertial fusion* (`knowledge/sources/a_simplified_economic_model_for_inertial_fusion/`): IFE-specific Monte Carlo parameter analysis (gain, rep rate, target cost). No MFE content; not applicable to magnetic mirror.
+  - *Economic studies for heavy-ion fusion electric power plants* (`knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/`): HIF driver cost analysis. Driver-dominated cost structure is not analogous to MFE. Not applicable.
+  - *Energy from Inertial Fusion* (`knowledge/sources/energy_from_inertial_fusion/`): IFE 1992 review covering laser, HIF, and light-ion IFE. Not applicable to MFE magnetic mirror.
+  - *Accelerators for Inertial Fusion Energy Production* (`knowledge/sources/accelerators_for_inertial_fusion_energy_production/`): IFE driver technology. Not applicable.
+  - *Affordable, manageable, practical and scalable (AMPS) high-yield inertial fusion* (`knowledge/sources/affordable_manageable_practical_and_scalable_amps_high/`): Pacific Fusion pulser-driven IFE. Not applicable.
+  - *Commercialization of laser fusion energy* (`knowledge/sources/commercialization_of_laser_fusion_energy/`): Xcimer KrF laser IFE. Not applicable.
+  - *Overview of the Helios Design: A Practical Planar Coil Stellarator* (`knowledge/sources/overview_of_the_helios_design_a_practical_planar_coil/`): Stellarator geometry (390 MWe, planar coils). BOP structure may be partially analogous to MFE, but the reactor core cost is stellarator-specific (3D coils, sector maintenance, thick shielding) and not applicable to the linear mirror geometry. Disqualified as an analog — ARPA-E ALPHA data already provides a better-matched modular MFE analog at similar scale.
+  - *An Assessment of the Economics of Future Electric Power Generation Options* (`knowledge/sources/an_assessment_of_the_economics_of_future_electric_power/`): ORNL historical LCOE benchmarking against coal/nuclear. Provides no fusion subsystem cost data applicable to magnetic mirror. Not applicable for this assessment.
+  - *Progress toward fusion energy breakeven and gain* (`knowledge/meta_analysis/progress_toward_fusion_breakeven_lawson_criterion/`): Wurzel & Hsu 2021. Useful for physics-state-of-the-art comparisons across fusion concepts. The paper confirms that WHAM-class mirror machines are in an early experimental phase with nτE well below ignition; the Hammir operating target has not been demonstrated experimentally. Integrated into Section 3 (subsystem maturity) as TRL context. No cost data applicable to LCOE.
 
 ---
 
 ## Summary
 
-The concept is well-described qualitatively and the physics basis is supported by a peer-reviewed paper. The analysis can proceed to produce a strong qualitative write-up across all five D1+ sections and a physics-validated operating point description. For the LCOE model, the analysis is **viable but heavily analog-dependent**: all capital cost and O&M figures will require CAS-framework analogs from fleet-wide sources (MARS, ARPA-E ALPHA revisit, TEA D-T MFE study) and clearly stated assumptions, since Realta has published nothing in this area. The recommendation is to **proceed to full analysis** with the following caveats: (a) flag LCOE estimates as ROM-level with ±50–100% uncertainty; (b) ingest the MARS study to improve plant-architecture analog fidelity; and (c) watch for the Hammir pre-conceptual design paper, which would upgrade the analysis substantially.
+Proceed to a D1+ analysis, with caveats. The qualitative sections (system function challenges, subsystem maturity, materials) are adequately supported for analysis — the physics basis, development roadmap, and engineering challenges are documented in peer-reviewed sources and public company communications. However, LCOE parameter extraction will require the analyst to apply explicit analog assumptions (ARPA-E ALPHA modular MFE and MARS historical mirror plant) for thermal output, efficiency chain, and capital costs, all flagged as low-to-medium confidence. The primary constraint is the absence of a Hammir pre-conceptual design study; the blocking LCOE gaps cannot be resolved without it. Ingest the MARS study (OSTI 5981974) before the LCOE section — it is the only mirror-specific plant study and would directly supply several missing parameters (TBR, thermal efficiency, DEC efficiency, blanket design).
 
 ---
 
 ## Structured summary (machine-readable)
 
 ```yaml
-overall_rating: "Mostly Ready"
-blocking_count: 3
-important_count: 8
-counting_method: "section_5_missing_parameters_plus_section_3_hardware_gap: capital cost breakdown, total installed cost, and O&M cost classified as blocking; BOP efficiency, recirculating power fraction, capacity factor, DEC efficiency, blanket TBR, first-wall replacement schedule, LCOE estimate, and NBI capital cost classified as important; deduplicated across all sections"
+overall_rating: "Significant Gaps"
+blocking_count: 6
+important_count: 7
+counting_method: "Deduplicated across all sections: blocking = {Hammir plant design paper, NBI wall-plug efficiency, DEC conversion efficiency for Hammir, thermal conversion efficiency, fusion thermal power output, capital cost breakdown by subsystem}; important = {MARS study not ingested, blanket type/TBR, Anvil experimental data, first wall/PMI study, REBCO volume for Hammir, capacity factor assumption, O&M cost}"
 section_coverage:
   availability_of_data:       "Partial"
-  system_function:            "Good"
+  system_function:            "Partial"
   subsystem_maturity:         "Partial"
   materials_supply_chain:     "Partial"
   lcoe_parameter_extraction:  "Poor"
```
