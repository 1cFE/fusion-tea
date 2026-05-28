# Diff: 11-magnetic-mirror

**Generated:** 2026-05-22T10:02:14-07:00

## Counts

| field | baseline | new | Δ |
|-------|----------|-----|---|
| blocking_count   | 4 | 3 | -1 |
| important_count  | 7 | 8 | - |
| overall_rating   | Significant Gaps | Mostly Ready | - |

## Fleet-source citations (new only — grep `knowledge/sources/` or `PyFECONS`)

```
155:2. **Revisit of 2017 ARPA-E ALPHA costing** (`knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`) — Already ingested. Relevant as a CAS-framework cost analog for alternative fusion concepts (~$43/MWh average, 500 MWe plants). Check whether any of the four costed concepts (FRC-based or mirror-adjacent) overlap with magnetic mirror architecture for blanket and BOP cost fractions.
157:3. **TEA D-T MFE Cost Analysis** (`knowledge/sources/tea_dt_mfe_cost_analysis/`) — Already ingested. Provides CAS-level D-T MFE cost methodology. Applicable to CAS22 (magnets), CAS23 (power conditioning), CAS26 (heat transport), CAS27 (fuel handling) as structural analogs, even though tokamak-derived.
```

## Blocking-tier lines (baseline)

```
34:- Hammir design paper — `not-yet-sourced` (pending publication) — **blocking** for anchored cost estimates
35:- Published plant cost study — `truly-unknown` at this stage; no one has done a full MARS-equivalent for a modern tandem mirror — **blocking** for capital cost model
59:- DCLC/AIC stability at reactor-relevant parameters — `truly-unknown` experimentally — **blocking** for physics confidence
85:- DEC (venetian blinds) technology readiness — `truly-unknown` at pilot scale — **blocking** for Qe and LCOE calculation
```

## Blocking-tier lines (new)

```
136:| Capital cost by subsystem (magnets, blanket, NBI, BOP, vacuum vessel) | proprietary | blocking | No plant-level cost breakdown from Realta or independent source |
137:| Total installed cost ($/kWe) | proprietary / truly-unknown | blocking | No FOAK or NOAK cost estimate published |
138:| O&M annual cost ($/kWe-yr or $/MWh) | proprietary | blocking | No published estimate; no analogous modern mirror plant exists |
```

## Full unified diff (truncated to 400 lines)

```diff
--- /tmp/gap_baselines_2026-05-22/11-magnetic-mirror.md	2026-05-22 09:21:13.846323535 -0700
+++ /home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/11-magnetic-mirror/gap_report.md	2026-05-22 10:02:14.773408739 -0700
@@ -1,65 +1,64 @@
-Now I have everything I need. Let me write the assessment.
+I have enough information from the concept-scoped sources to write the assessment. Let me also note which fleet-wide sources are applicable before writing.
+
+From the source index, the applicable fleet-wide sources for Magnetic Mirror (D-T) are:
+- **TEA D-T MFE Cost Analysis** — D-T MFE LCOE methodology and CAS breakdowns
+- **Revisit of the 2017 Costing for Four ARPA-E ALPHA Concepts** — multi-concept CAS costing framework (alternative fusion concepts, same budget era)
+- **ARIES Cost Account Documentation** — CAS hierarchy reference
+
+I'll now write the gap assessment.
 
 ---
 
 # Gap Assessment: Magnetic Mirror (D-T)
 
 ## Overall Readiness
-**Rating**: Significant Gaps
-
-**Summary**: Realta Fusion is unusually transparent for a private fusion startup, and the physics basis for confinement is reasonably well-documented. However, no plant-level cost study exists for Hammir or any successor design — Realta has not published capital cost estimates, blanket specifications, thermal cycle details, or operating cost projections. The LCOE model will depend heavily on historical analogues (MARS study) and engineering extrapolations, with large parametric uncertainty on the most cost-relevant subsystems. Sufficient data exists to produce a credible first-pass model with clearly bounded uncertainty, but it cannot be anchored to Realta's own design.
+**Rating**: Mostly Ready  
+**Summary**: The qualitative sections are well-supported by a combination of Realta's published physics paper, two interviews, a conference talk, and the WHAM experiment website. Physics operating points, technology roadmap, stability challenges, and the hybrid energy capture architecture are all documented with reasonable confidence. The LCOE parameter extraction section is the weak spot: no plant-level capital cost breakdown, no O&M estimates, and no BOP thermal cycle details have been published by Realta. The historical MARS study and fleet-wide MFE TEA sources provide partial analogues but cannot substitute for a Realta-specific plant study.
 
 ---
 
 ## Section Coverage
 
 ### 1. Availability of Data
-**Coverage**: Moderate
+**Coverage**: Partial
 
 **Available**:
-- Physics basis paper (arXiv 2411.06644): Q > 5 modeling, 50m center cell, confinement predictions, design parameter optimization via ML
-- APS DPP 2025 (Sutherland): development timeline, Hammir performance targets (Qe > 1, >50 MWe, 3-hour continuous), Anvil purpose
-- Fusion Hub spotlight: heating systems, magnets, DEC architecture, stabilization schemes
-- Fusion Report interview: performance scaling (~7 MW/m), dual-channel energy conversion, lithium tritium breeding confirmation
-- WHAM experiment details: 17 T REBCO magnets, ECH/NBI/HHFW, first plasma July 2024
-- SVB funding release: market focus (industrial heat, data centers), CoSMo branding — no technical depth
-- Historical analogue: MARS study (1980s) — LiPb blanket, TBR 1.15, ~36% plant efficiency, gridless direct converters (~54% DEC efficiency) — available in dossier citations but not in extracted source documents
+- Company transparency is above average for an early-stage fusion startup. Realta has published a peer-reviewed physics paper (arxiv-2411-06644), an APS DPP 2025 conference presentation, two detailed public interviews (Fusion Hub, The Fusion Report), and a DOE Milestone award (ARPA-E).
+- Technology roadmap (WHAM → Anvil → Hammir) with specific milestones (Qe > 1, Pe,out > 50 MWe, 3 hr continuous) is well-documented (`aps-dpp-2025-sutherland.md`, `arxiv-2411-06644`).
+- Funding history is traceable: $10M ARPA-E → $36M Series A (May 2025) → $9.5M SVB debt facility (Feb 2026) (`realta-svb-funding-feb2026.md`).
+- The MARS study (1980s, cited in dossier) provides an older-generation tandem mirror plant study with blanket, shielding, and DEC architecture details — useful as a structural analog even if cost figures require escalation and technology adjustment.
+- Historical GDT (Russia) and Gamma-10 (Japan) mirror experiments provide physics validation data cited in the arxiv paper.
 
 **Missing**:
-- Pre-conceptual design paper for Hammir (Realta stated expected 2026, not yet published as of research cutoff)
-- Any published plant study or system code output with cost estimates
-- Detailed engineering specifications for blanket, shield, DEC hardware
+- No published plant-level engineering study or techno-economic analysis from Realta. The Hammir pre-conceptual design paper is stated to be expected in 2026 but not yet available.
+- No cost estimates (capital or operating) from Realta or from any independent study of the modern tandem mirror concept.
+- No third-party validation or review of Realta's physics modeling outputs.
 
 **Gaps**:
-- Hammir design paper — `not-yet-sourced` (pending publication) — **blocking** for anchored cost estimates
-- Published plant cost study — `truly-unknown` at this stage; no one has done a full MARS-equivalent for a modern tandem mirror — **blocking** for capital cost model
-- Peer-reviewed journal paper expanding on arXiv preprint — `not-yet-sourced` — **important**
+- Hammir pre-conceptual design paper — `not-yet-sourced` — **important**: would resolve blanket type, BOP architecture, NBI power budgets
+- Independent techno-economic study of modern tandem mirror — `truly-unknown` — **important**: no published independent cost analysis exists for this concept generation
 
 ---
 
 ### 2. Challenges in Capturing System Function
-**Coverage**: Partial
+**Coverage**: Good
 
 **Available**:
-- Confinement physics uncertainties identified: DCLC and AIC instability management, classical radial transport quantified as a significant factor (arXiv 2411.06644)
-- DEC mechanism described (venetian blinds, axisymmetric, for escaping charged particles); MARS analogue gives ~54% efficiency as a reference
-- Performance scaling law is explicit: ~7 MW/m center cell addition at constant input power (Fusion Report interview)
-- Stabilization mechanisms described: sloshing ions (DCLC/AIC), vortex stabilization via sheared azimuthal flows, expanders with good curvature (Fusion Hub)
-- End-plug sustainment is undemonstrated — Anvil is the device to prove this
+- The key physics challenges are well-documented: DCLC kinetic instability (managed via sloshing ions), MHD interchange instability (managed via vortex stabilization and good-curvature expander regions), and electron temperature management via ECH (`realta-fusion-hub-spotlight.md`, `arxiv-2411-06644`).
+- The power balance architecture is described: NBI + ECH heating remains dominant at Q > 5 (i.e., not alpha-dominated), meaning recirculating power fraction is significant and DEC is critical to achieving Qe > 1 (`fusion-report-interview-realta.md`).
+- The scaling law (~7 MW per additional meter of center cell, with constant input power) is a distinctive feature that simplifies power-per-unit-length modeling (`fusion-report-interview-realta.md`).
+- The arxiv paper provides high-fidelity integrated modeling (RealTwin = CQL3D-m + Pleiades) and POPCON analysis for Hammir operating points, with quantitative parameters for the end-plug design.
+- Impurity management in tandem mirrors is acknowledged as an open challenge (higher confinement of impurities vs. simple mirrors due to end-plug potential) (`realta-fusion-hub-spotlight.md`).
 
 **Missing**:
-- Validation of DCLC/AIC suppression under D-T relevant density and temperature (WHAM is deuterium-only, sub-breakeven physics)
-- End-plug physics demonstration at commercial-scale field and density (Anvil device not yet built)
-- Quantification of classical transport degradation in longer center cells
-- Thermal cycle selection and system efficiency breakdown (steam vs. sCO2 unconfirmed)
-- DEC efficiency for Realta's venetian blind design vs. MARS gridless converters
-- Any modeling of recirculating power fraction (critical for Qe calculation)
+- Specific NBI power levels (MW input) and ECH power levels for Hammir at steady state — the arxiv paper addresses end-plug physics but doesn't clearly state total plant heating power.
+- HHFW (High Harmonic Fast Wave) role in the full Hammir design is described qualitatively for WHAM but not quantified for the pilot plant.
+- Plasma-material interaction (PMI) modeling for the linear geometry first wall — acknowledged as a challenge but unstudied publicly for Realta's design.
+- Quantitative recirculating power fraction (NBI + ECH / gross electric output) for Hammir.
 
 **Gaps**:
-- DCLC/AIC stability at reactor-relevant parameters — `truly-unknown` experimentally — **blocking** for physics confidence
-- End-plug sustainment validation — `proprietary` (Anvil will test this, ~2028) — **important** for model credibility
-- Recirculating power fraction and overall plant efficiency — `derivable` from Q, DEC efficiency, and thermal cycle assumptions — **important**
-- Thermal cycle type — `proprietary` — **important** for efficiency estimates (sCO2 would be ~45-50% vs steam ~35%)
+- Total steady-state heating power budget for Hammir — `proprietary` — **important**: needed to calculate recirculating power and net electric gain
+- First wall heat flux and PMI quantification — `not-yet-sourced` (may exist in MARS study or similar) — **nice-to-have**
 
 ---
 
@@ -67,122 +66,123 @@
 **Coverage**: Partial
 
 **Available**:
-- HTS mirror magnets (REBCO, 17 T): demonstrated at WHAM with CFS-built magnets — TRL ~6 for magnet hardware at WHAM scale; TRL ~3-4 for a full Hammir-scale magnet array
-- ECH (110 GHz gyrotron): mature technology, demonstrated at WHAM — TRL ~7-8
-- NBI: mature technology, demonstrated at WHAM — TRL ~7-8
-- HHFW (High Harmonic Fast Wave): demonstrated at WHAM — TRL ~6
-- Mirror physics / tandem mirror concept: WHAM first plasma July 2024 validates basic confinement; tandem mirror physics is at TRL ~3 (sub-scale, no end-plug demonstration)
-- WHAM cost: $10M ARPA-E grant; WHAM++ mentioned at "$50M in REBCO tape alone" suggesting magnet-dominated cost
+- **HTS mirror magnets (REBCO)**: TRL 5–6. WHAM demonstrated 17 T in a full axisymmetric mirror configuration using CFS-built REBCO coils (operational July 2024). This is hardware-demonstrated at experiment scale (`wham-experiment-details.md`, `aps-dpp-2025-sutherland.md`).
+- **NBI (neutral beam injection)**: TRL 6–7. Modern negative-ion neutral beams cited as a key enabling technology are mature from tokamak programs (ITER NBI). Not yet demonstrated in a mirror end-plug role at the required parameters.
+- **ECH (110 GHz gyrotrons)**: TRL 6–7. Gyrotron technology mature from tokamak programs; used on WHAM.
+- **Tandem mirror end-plug physics**: TRL 3–4. Axisymmetric tandem mirror end-plug physics has not been demonstrated at the required density and temperature — this is Anvil's mission (~2028 target). The arxiv paper validates modeling but not hardware.
+- **Direct energy conversion (venetian blind)**: TRL 3–4. The axisymmetric venetian blind DEC concept is described but not demonstrated at power-plant scale. MARS study achieved ~54% DEC efficiency in analysis; Realta has not published efficiency targets (`dossier.md`).
+- **Li blanket for tritium breeding + neutron capture**: TRL 4–5 (for fusion applications broadly). Specific blanket design for linear geometry not published.
+- **Pilot plant central cell (50m, full tandem)**: TRL 2. Exists only as simulation outputs (arxiv paper). Hammir as a device does not yet have a hardware design.
 
 **Missing**:
-- TRL for DEC (venetian blinds): no experimental demonstration at any scale — TRL ~2-3
-- TRL for tritium breeding blanket: no Realta-specific blanket design published — TRL ~2 for Realta's concept specifically
-- TRL for end-plug sustainment in tandem configuration: Anvil is the first test — TRL ~2-3
-- Stability of longer center cells (>50m) has no experimental validation
-- No data on first wall lifetime or replacement schedule under 14 MeV neutron flux
+- TRL assessment for vortex stabilization at scale (the MHD mitigation approach) — demonstrated on GDT (Russia) but not integrated into an HTS tandem mirror.
+- First-wall materials choice and lifetime estimates for Hammir neutron environment — not yet published.
+- WHAM++ (the intermediate scientific breakeven device) — described in FusionHub as needing ~$50M in REBCO tape, suggesting it may not be built and Anvil is the next step (`realta-fusion-hub-spotlight.md`). This creates a step gap in the validation ladder.
 
 **Gaps**:
-- DEC (venetian blinds) technology readiness — `truly-unknown` at pilot scale — **blocking** for Qe and LCOE calculation
-- Tritium breeding blanket TRL — `not-yet-sourced` (MARS study exists; Realta-specific design pending 2026 paper) — **important**
-- First wall lifetime under D-T neutron flux — `truly-unknown` for this geometry — **important**
-- End-plug sustainment (Anvil) — `truly-unknown` until ~2028 — **important** for technical credibility statement
+- End-plug physics demonstration (Anvil) is 2+ years out — `proprietary` — **blocking for hardware validation** but not for concept analysis; POPCON modeling gives sufficient analytical basis
+- DEC efficiency quantification for Hammir design — `not-yet-sourced` (MARS study provides 54% historical analog) — **important**
+- First-wall materials/lifetime for Hammir — `not-yet-sourced` — **nice-to-have**
 
 ---
 
 ### 4. Key Materials and Supply Chain Considerations
-**Coverage**: Poor
+**Coverage**: Partial
 
 **Available**:
-- REBCO tape: identified as critical; "$50M in REBCO tape alone for WHAM++" (Fusion Hub) — signals significant magnet cost driver
-- HTS magnet supply chain: CFS partnership confirmed for WHAM; CFS is a credible supplier
-- Lithium for tritium breeding: confirmed as blanket feedstock (Fusion Report interview); Li-6 enrichment likely required for adequate TBR
-- D-T fuel: tritium startup inventory not discussed anywhere in sources
+- **REBCO HTS tape**: The FusionHub article explicitly states WHAM++ would require ~$50M in REBCO tape alone, establishing REBCO as the dominant materials cost driver. Magnet supply chain is tied to CFS (Commonwealth Fusion Systems), which is an active supplier but a competitor in the fusion space (`realta-fusion-hub-spotlight.md`).
+- **Tritium**: D-T fuel cycle requires tritium breeding; Li blanket confirmed for this purpose. Tritium supply constraints are a fleet-wide issue, not specific to Realta, but apply here.
+- **Lithium**: Required for tritium breeding blanket; specific isotopic enrichment (Li-6) needs would depend on blanket design (unspecified by Realta).
+- **NBI components**: Mature supply chain (ITER, JET experience), no specific bottleneck identified for Realta's scale.
+- **Mirror coil geometry (axisymmetric)**: Described as simpler than stellarator or tokamak coils — this is a supply-chain advantage over 3D coil geometries.
 
 **Missing**:
-- REBCO tape quantity for Hammir (not in any source — only WHAM++ estimate available)
-- Li-6 enrichment requirements and supply availability
-- Tritium startup inventory requirement and source (CANDU reactors, DOE reserve)
-- Beryllium: not mentioned, but may be relevant for neutron multiplication depending on blanket design
-- Manufacturing scalability of venetian blind DEC electrodes
-- Cryogenic system requirements for HTS magnet cooling at Hammir scale
+- REBCO tape volume estimates for Hammir (only WHAM++ estimate available; Hammir is a different configuration).
+- Tritium inventory and fueling rate for Hammir — no published estimate from Realta.
+- Supply concentration risk: CFS is currently the only named supplier of REBCO coils for Realta; no alternative supplier path described.
 
 **Gaps**:
-- REBCO tape volume for Hammir — `derivable` (scale from WHAM++ estimate using magnet volume) — **important**
-- Li-6 enrichment requirements — `derivable` from TBR modeling (needs blanket design) — **important**
-- Tritium startup inventory — `not-yet-sourced` (industry-standard D-T startup analysis applies; search OSTI/NRC) — **important**
-- DEC electrode manufacturing — `truly-unknown` — **nice-to-have** for first pass
-- No supply chain analysis published by Realta — `proprietary` — **nice-to-have**
+- REBCO tape volume/cost for Hammir — `derivable` (from magnet volume and field requirements) — **important**
+- Tritium inventory requirements — `derivable` (from fusion power and tritium burn fraction, using standard formulas) — **nice-to-have**
+- Li-6 enrichment requirements — `derivable` once blanket type is known — **nice-to-have**
+- Alternative REBCO supplier path — `not-yet-sourced` — **nice-to-have**
 
 ---
 
 ### 5. LCOE Parameter Extraction
+**Coverage**: Poor
 
 **Available Parameters**:
+
 | Parameter | Value/Range | Source | Confidence |
 |-----------|-------------|--------|------------|
-| Fusion gain Q | >5 (50m), >10 (longer) | arXiv 2411.06644 | medium |
-| Net electric output | >50 MWe (Hammir pilot) | APS DPP 2025 | medium |
-| Electric gain Qe | >1 (Hammir target) | APS DPP 2025 | medium |
-| Performance scaling | ~7 MW/m center cell | Fusion Report interview | medium |
-| Operation mode | Steady-state, 3+ hr demonstrated | APS DPP 2025 | high |
-| Center cell length | 50m for Q>5 | arXiv 2411.06644 | medium |
-| DEC efficiency (analogue) | ~54% (MARS historical) | Dossier (MARS citation) | low |
-| Plant efficiency (analogue) | ~36% (MARS historical) | Dossier (MARS citation) | low |
-| TBR (analogue) | 1.15 (MARS, LiPb blanket) | Dossier (MARS citation) | low |
-| Magnet field strength | 17 T (WHAM) | WHAM experiment details | high |
-| REBCO tape cost signal | "$50M for WHAM++" | Fusion Hub | low |
-| Heating technologies | ECH + NBI + HHFW | WHAM, Fusion Hub | high |
+| Target fusion gain Q | Q > 5 (base), Q > 10 (longer cell) | arxiv-2411-06644 | medium |
+| Net electric output target | > 50 MWe | aps-dpp-2025-sutherland.md | medium |
+| Power scaling law | ~7 MW per additional meter center cell | fusion-report-interview-realta.md | medium |
+| Plant size range | 50–500 MWe | fusion-report-interview-realta.md | low |
+| Operation mode | Steady-state (continuous) | dossier.md | high |
+| Continuous operation target | ≥ 3 hours (demonstration milestone) | aps-dpp-2025-sutherland.md | high |
+| DEC efficiency (analog) | ~54% (MARS historical) | dossier.md (cited MARS) | low |
+| REBCO tape cost indicator | ~$50M for WHAM++ (smaller device) | realta-fusion-hub-spotlight.md | low |
+| Magnet technology | HTS REBCO, 17 T demonstrated | wham-experiment-details.md | high |
+| Center cell length (Hammir) | ~50m (for Q > 5) | fusion-report-interview-realta.md | medium |
+| Fuel | D-T | dossier.md | high |
+| Energy capture split | Thermal (neutron) + DEC (charged particles) | fusion-report-interview-realta.md | high |
 
 **Missing Parameters**:
+
 | Parameter | Gap Type | Criticality | Notes |
 |-----------|----------|-------------|-------|
-| Capital cost by subsystem (magnets, blanket, BOP, DEC, vacuum vessel) | `truly-unknown` | Blocking | No plant study exists; must use MARS analogues scaled to HTS costs |
-| Thermal cycle type and efficiency | `proprietary` | Blocking | sCO2 vs steam changes plant efficiency by ~10 pp; contact Realta or use range |
-| Recirculating power fraction | `derivable` | Blocking | Needed to go from Q to Qe; depends on heating power, DEC efficiency |
-| Operating costs (maintenance, staffing, component replacement) | `truly-unknown` | Blocking | No Realta data; use tokamak analogues with mirror-specific adjustments |
-| First wall replacement schedule | `truly-unknown` | Important | Neutron fluence limits drive O&M cost; no Hammir-specific data |
-| Capacity factor target | `derivable` | Important | Steady-state design, but availability TBD; use ~80-90% as analogue assumption |
-| Tritium startup inventory and cost | `not-yet-sourced` | Important | Industry standard ~1-2 kg; search NRC/OSTI |
-| Blanket type and TBR | `not-yet-sourced` | Important | Realta unspecified; MARS LiPb TBR=1.15 available as analogue |
-| DEC capital cost | `truly-unknown` | Important | No commercial DEC hardware exists; pure R&D extrapolation |
-| Plant footprint / modular unit size | `not-yet-sourced` | Important | CoSMo brand implies modularity; MARS geometry can bound estimate |
-| REBCO tape quantity for Hammir | `derivable` | Important | Scale from WHAM++ $50M signal + magnet geometry |
+| Capital cost by subsystem (magnets, blanket, NBI, BOP, vacuum vessel) | proprietary | blocking | No plant-level cost breakdown from Realta or independent source |
+| Total installed cost ($/kWe) | proprietary / truly-unknown | blocking | No FOAK or NOAK cost estimate published |
+| O&M annual cost ($/kWe-yr or $/MWh) | proprietary | blocking | No published estimate; no analogous modern mirror plant exists |
+| BOP thermal cycle type and efficiency (steam / sCO2) | proprietary | important | Affects overall η_thermal; can be bounded by analogy but not confirmed |
+| NBI + ECH total input power for Hammir (recirculating power fraction) | proprietary | important | Needed for net Q_e calculation; arxiv paper gives end-plug details but not total system power budget |
+| Capacity factor / plant availability | not-yet-sourced / derivable | important | Steady-state favors high CF; but no maintenance schedule or first-wall replacement interval published |
+| DEC efficiency (Realta Hammir design) | proprietary / not-yet-sourced | important | MARS gives 54% analog; Realta claims improvement but no number given |
+| Blanket TBR and tritium inventory | proprietary | important | Blanket type unspecified; TBR affects tritium self-sufficiency and fuel cost |
+| First-wall replacement schedule and cost | not-yet-sourced | important | Affects O&M; no Realta-specific data; MARS analog possible |
+| LCOE estimate or cost target | truly-unknown | important | No published LCOE or cost-of-electricity target from Realta |
+| NBI capital cost for Hammir | not-yet-sourced | important | NBI is likely a major capital line item; ITER NBI costs could serve as analog |
+| HTS magnet cost for Hammir | derivable | important | Can be estimated from REBCO tape volume × cost/kg + winding + structure |
 
 ---
 
 ## Source Recommendations
 
-1. **MARS study full text** (Logan 1984, LLNL): OSTI biblio 5981974 — best available analogue for blanket design (LiPb, TBR 1.15), direct conversion efficiency (36% thermal + DEC), and plant layout. Listed in dossier but not extracted as a source document. **Priority: high** — `not-yet-sourced`, confirmed in dossier citations.
+1. **MARS study (OSTI:5981974)** — `not-yet-sourced` as an extracted document in the repo (cited in dossier but not ingested). Contains blanket design (LiPb, TBR 1.15), plant thermal efficiency (~36%), DEC architecture, and cost structure for a 1980s tandem mirror. Primary analog for plant-level parameters. Recommend ingesting via `scripts/zotero_ingest.py`. *Note: this is a real published document — confirm OSTI availability before searching.*
+
+2. **Revisit of 2017 ARPA-E ALPHA costing** (`knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`) — Already ingested. Relevant as a CAS-framework cost analog for alternative fusion concepts (~$43/MWh average, 500 MWe plants). Check whether any of the four costed concepts (FRC-based or mirror-adjacent) overlap with magnetic mirror architecture for blanket and BOP cost fractions.
 
-2. **Hammir pre-conceptual design paper** (Realta, expected 2026): This is the single highest-value missing document. Will specify blanket type, shielding architecture, plant layout, and performance targets. Monitor arXiv (`tandem mirror`, `Realta`, `Hammir`). **Priority: high** — `not-yet-sourced`, expected soon.
+3. **TEA D-T MFE Cost Analysis** (`knowledge/sources/tea_dt_mfe_cost_analysis/`) — Already ingested. Provides CAS-level D-T MFE cost methodology. Applicable to CAS22 (magnets), CAS23 (power conditioning), CAS26 (heat transport), CAS27 (fuel handling) as structural analogs, even though tokamak-derived.
 
-3. **DCLC instability suppression papers**: The arXiv 2411.06644 preprint references prior work on sloshing ions and DCLC management. Search arXiv for Sutherland et al. follow-on papers or related UW-Madison publications on drift cyclotron loss cone stabilization. **Priority: medium** — `not-yet-sourced`, existence plausible but `unverified — confirm existence before searching`.
+4. **Forest et al. 2024 — BEAM device design paper** — Cited in arxiv-2411-06644 as the predecessor to Anvil. May contain quantitative device parameters (dimensions, magnet specs, NBI power) useful for Hammir scaling. Search: `arxiv "BEAM" "break-even axisymmetric mirror" Forest 2024`. *Unverified — confirm existence before searching.*
 
-4. **Direct energy conversion literature (mirror-specific)**: George Miley and/or post-MARS mirror DEC papers. Search OSTI for "direct energy conversion mirror fusion" or "venetian blind direct converter." **Priority: medium** — `not-yet-sourced`, MARS-era papers likely on OSTI; modern Realta-specific DEC unpublished.
+5. **Logan 1983 / MARS full study** — The tandem mirror MARS study from LLNL (Logan, 1983). Multiple OSTI records exist. May contain detailed cost breakdowns, DEC efficiency analysis, and blanket design that are structurally analogous to Hammir even with technology differences. *Unverified full content — confirm OSTI availability.*
 
-5. **Tritium startup inventory studies**: NRC/DOE reports on tritium supply for D-T fusion programs give industry-standard startup inventory estimates (~1-2 kg). Search OSTI or NRC for "tritium supply fusion startup." **Priority: medium** — `not-yet-sourced`.
+6. **Realta Fusion Hammir pre-conceptual design paper** — Stated in dossier as expected 2026. Monitor arXiv (search: "Hammir" OR "tandem mirror pilot plant Realta") and PRNewswire for announcement. This is the single most important missing source.
 
-6. **REBCO tape market and cost**: Search for HTS wire cost studies (e.g., ARPA-E SUMMIT program outputs, or CFS public filings) to anchor the magnet cost component. The $50M/WHAM++ signal is a single weak data point. **Priority: medium** — `not-yet-sourced`, `unverified — confirm existence before searching`.
+7. **ITER NBI cost data** — For NBI capital cost analog. Search OSTI or ITER documentation for NBI system cost breakdown. *Unverified — confirm existence before searching.*
 
 ---
 
 ## Summary
 
-**Proceed to full analysis with caveats.** The concept is well-enough understood to produce a first-pass LCOE model, but the model will be heavily analogue-driven. The physics layer (confinement, Q targets, DEC principle) is sufficiently documented. The cost layer is essentially empty — no plant study, no subsystem cost estimates, no thermal cycle specification. 
+The concept is well-described qualitatively and the physics basis is supported by a peer-reviewed paper. The analysis can proceed to produce a strong qualitative write-up across all five D1+ sections and a physics-validated operating point description. For the LCOE model, the analysis is **viable but heavily analog-dependent**: all capital cost and O&M figures will require CAS-framework analogs from fleet-wide sources (MARS, ARPA-E ALPHA revisit, TEA D-T MFE study) and clearly stated assumptions, since Realta has published nothing in this area. The recommendation is to **proceed to full analysis** with the following caveats: (a) flag LCOE estimates as ROM-level with ±50–100% uncertainty; (b) ingest the MARS study to improve plant-architecture analog fidelity; and (c) watch for the Hammir pre-conceptual design paper, which would upgrade the analysis substantially.
 
-The recommended approach: (1) extract the MARS study (it's in the dossier citations and on OSTI) as the primary cost analogue, applying scaling corrections for HTS magnets vs. copper coils and modern NBI vs. 1980s beamlines; (2) treat the DEC efficiency and thermal cycle efficiency as the two highest-sensitivity parameters and run sweeps; (3) treat the entire capital cost estimate as ±50% and document this explicitly. The back-solve to $0.01/kWh will be particularly illuminating here given the DEC pathway — the concept has a structural advantage in Q threshold that doesn't apply to thermal-only designs, but DEC cost and reliability are completely unvalidated.
+---
 
 ## Structured summary (machine-readable)
 
 ```yaml
-overall_rating: "Significant Gaps"
-blocking_count: 4
-important_count: 7
-counting_method: "section_5_missing_parameters"
+overall_rating: "Mostly Ready"
+blocking_count: 3
+important_count: 8
+counting_method: "section_5_missing_parameters_plus_section_3_hardware_gap: capital cost breakdown, total installed cost, and O&M cost classified as blocking; BOP efficiency, recirculating power fraction, capacity factor, DEC efficiency, blanket TBR, first-wall replacement schedule, LCOE estimate, and NBI capital cost classified as important; deduplicated across all sections"
 section_coverage:
-  availability_of_data:       "Moderate"
-  system_function:            "Partial"
+  availability_of_data:       "Partial"
+  system_function:            "Good"
   subsystem_maturity:         "Partial"
-  materials_supply_chain:     "Poor"
-  lcoe_parameter_extraction:  "Unknown"
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
