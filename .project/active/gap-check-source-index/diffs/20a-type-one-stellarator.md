# Diff: 20a-type-one-stellarator

**Generated:** 2026-05-22T10:39:07-07:00

## Counts

| field | baseline | new | Δ |
|-------|----------|-----|---|
| blocking_count   | 3 | 4 | 1 |
| important_count  | 8 | 8 | - |
| overall_rating   | Mostly Ready (with sourcing gap) | Mostly Ready | - |

## Fleet-source citations (new only — grep `knowledge/sources/` or `PyFECONS`)

```
21:- Helios preconceptual design (arxiv-2512.08027, also in fleet-wide index at knowledge/sources/overview_of_the_helios_design_a_practical_planar_coil/) — a comparable HTS stellarator with detailed engineering design (390 MWe, 88% CF, 40% thermal efficiency, blanket/BOP/maintenance data)
22:- TEA D-T MFE cost analysis (knowledge/sources/tea_dt_mfe_cost_analysis/): $140–550/MWh LCOE range and $8,800–22,200/kW OCC for a 350 MWe MFE tokamak — CAS methodology applicable as a fleet-wide bound
147:1. **ARIES-CS cost study** (`knowledge/sources/aries_cost_account_documentation/` + external ARIES-CS system study reports): The most relevant historical stellarator analog for CAS-level cost breakdown. ARIES-CS was a QI compact stellarator; cost accounts documented. Search OSTI for "ARIES-CS cost analysis" or "ARIES compact stellarator economics." — `unverified — confirm existence before searching`
149:2. **Helios full papers** (`knowledge/sources/overview_of_the_helios_design_a_practical_planar_coil/` — already extracted): The Helios overview paper was read (abstract only via arxiv-2512.08027 source); the full extracted output.md in the fleet-wide source is available and covers thermal cycle, BOP, capacity factor (88%), maintenance architecture, and magnet engineering. Use this as the primary stellarator analog for engineering and O&M parameters.
151:3. **TEA D-T MFE cost analysis** (`knowledge/sources/tea_dt_mfe_cost_analysis/`): CAS-level cost breakdown for 350 MWe D-T MFE plant (tokamak); provides OCC range as upper/lower bound for MFE. Direct stellarator-to-tokamak comparison needed (stellarator likely lower fuel cycle cost, higher magnet complexity cost). Already ingested.
```

## Blocking-tier lines (baseline)

```
30:- Primary sources not ingested — `not-yet-sourced` — **blocking** for LCOE parameter extraction from primary literature
54:- Gross electrical / recirculating power breakdown — `proprietary` likely, may be `not-yet-sourced` in E65 — **blocking** for quantitative LCOE
136:| Capital cost by subsystem (magnets, blanket, vessel, BOP) | proprietary | blocking | No published cost estimates exist |
137:| Gross electrical output | not-yet-sourced | blocking | Need to reconcile 350 MWe net; likely in E65 |
138:| Recirculating power fraction | not-yet-sourced / proprietary | blocking | Cryoplant + ECRH + pumping; needed for Q_eng |
```

## Blocking-tier lines (new)

```
78:- HTS 3D non-planar coil manufacturing TRL and cost — `proprietary` / `not-yet-sourced` — **blocking**: dominant capital cost driver; no published data; Infinity One will validate concept but not yet built
131:| Over-night capital cost (OCC) total | proprietary | blocking | No published estimate; fleet-wide analog: $8,800–22,200/kW for 350 MWe MFE tokamak (TEA D-T MFE source) |
132:| Capital cost by CAS account | proprietary | blocking | No CAS breakdown published; Helios and ARIES-CS can provide stellarator structural analogs |
133:| HTS coil capital cost | proprietary | blocking | Dominant cost driver; CFS manufactures but no pricing for Infinity Two geometry |
134:| Annual O&M cost rate | not-yet-sourced | blocking | No published O&M estimate; ARIES-CS, Helios can provide analog range |
```

## Full unified diff (truncated to 400 lines)

```diff
--- /tmp/gap_baselines_2026-05-22/20a-type-one-stellarator.md	2026-05-22 09:21:13.863754873 -0700
+++ /home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/20a-type-one-stellarator/gap_report.md	2026-05-22 10:39:07.429571270 -0700
@@ -1,35 +1,34 @@
-# Gap Assessment: QI Modular HTS Stellarator - Infinity Two
+I have now read all the necessary sources. Let me compile the gap assessment.
 
-## Overall Readiness
-**Rating**: Mostly Ready (with sourcing gap)
+# Gap Assessment: Type One Stellarator (D-T)
 
-**Summary**: Type One Energy is unusually transparent for a private fusion company — six peer-reviewed J. Plasma Physics papers published in 2025 provide a documented physics basis that most competitors cannot match. The primary gap is that none of these papers have been extracted into the knowledge base, meaning the detailed numerical content from the primary sources is unavailable for parameter extraction. Physics parameters and system architecture are well-characterized from dossier-level research; the major substantive gap is techno-economic data (capital costs, component replacement costs, recirculating power breakdown), which is likely absent from the physics papers and may require analogue estimation.
+## Overall Readiness
+**Rating**: Mostly Ready
+**Summary**: Type One Energy's Infinity Two has an exceptionally strong, peer-reviewed physics basis — seven papers in a JPP special issue that cover plasma performance, MHD stability, alpha confinement, blanket/tritium feasibility, and divertor design. This is the most thoroughly documented private fusion design in the dataset. The primary gaps are economic: no concept-specific capital cost estimates, O&M data, or OCC projections have been published; these must be filled with stellarator analogs (Helios, ARIES-CS) and fleet-wide MFE TEA methodology. The analysis can proceed to D1+ with clearly flagged cost-estimation uncertainty.
 
 ---
 
 ## Section Coverage
 
 ### 1. Availability of Data
-**Coverage**: Good (physics/architecture); Poor (economics)
+**Coverage**: Good
 
 **Available**:
-- 6 peer-reviewed J. Plasma Physics papers (2025 Physics Basis collection), including a "comprehensive unified baseline physics design" paper (E65) and a blanket/tritium feasibility paper (E86). This is the strongest published physics basis of any private stellarator concept.
-- Published plant-level design targets: 800 MWf / 350 MWe net, Q > 40, R = 12.5 m, A = 10, 9 T on-axis, HCPB blanket, Rankine cycle with reheat (>30% thermal efficiency), TBR = 1.30 (OpenMC verified with 300M particles).
-- Maintenance schedule: 2-year continuous power cycle, 30-day planned outages (press release, May 2025).
-- Company design review completion announcement — implies internal design maturity beyond what's publicly released.
-- CFS partnership for HTS magnet development.
-- W7-X lineage provides substantial analogue physics and engineering data (publicly available separately).
+- Seven open-access peer-reviewed JPP papers (2025) covering all major physics subsystems: baseline plasma physics design, MHD equilibrium and stability, alpha-particle confinement, core plasma performance predictions, power and particle exhaust (divertor), breeder blanket and tritium fuel cycle feasibility, and an overarching unified design basis summary (cambridge-core-journals article, cambridge-core-services PDF, modernsciences summary, typeoneenergy press release)
+- Company press releases confirming key parameters: 800 MW fusion power, 350 MWe net, D-T fuel, HCPB blanket, Rankine cycle, 2-year operating cycle with 30-day planned maintenance outages, TVA partnership (typeoneenergy-type-one-energy-issues-first-realistic.md)
+- Formal design review completion announced May 2025 (dossier)
+- DOE FES 2022 Pearson presentation covering D-T fuel cycle supply chain: tritium, Li-6, beryllium constraints applicable to Infinity Two (science-media-fes-pdf)
+- Helios preconceptual design (arxiv-2512.08027, also in fleet-wide index at knowledge/sources/overview_of_the_helios_design_a_practical_planar_coil/) — a comparable HTS stellarator with detailed engineering design (390 MWe, 88% CF, 40% thermal efficiency, blanket/BOP/maintenance data)
+- TEA D-T MFE cost analysis (knowledge/sources/tea_dt_mfe_cost_analysis/): $140–550/MWh LCOE range and $8,800–22,200/kW OCC for a 350 MWe MFE tokamak — CAS methodology applicable as a fleet-wide bound
 
 **Missing**:
-- No extracted source documents in the Phase 1a knowledge base — the 6 papers exist but their numerical content has not been ingested.
-- No published cost estimates, plant study with cost breakdown, or system code output (e.g., PROCESS-equivalent).
-- No detailed recirculating power breakdown (cryoplant, ECRH, tritium systems, pumping).
-- No divertor design specification published (island divertor implied by QI configuration, but not documented at the level of blanket design).
+- No published engineering design study equivalent to Helios or ARIES-CS: structural, thermal, and manufacturing detail for coils, blanket, and BOP
+- No published cost estimates or pre-FEED economic analysis from Type One Energy
+- No DOE program-level system study (ARIES-style) for a QI/maximum-J stellarator at this scale
 
 **Gaps**:
-- Primary sources not ingested — `not-yet-sourced` — **blocking** for LCOE parameter extraction from primary literature
-- Cost/economic data from company — `proprietary` — **important** (central analysis need)
-- System code (PROCESS-equivalent for stellarator) outputs — `not-yet-sourced` — **important**
+- Absence of concept-specific engineering/cost study — `proprietary` — **important**: design is "pre-conceptual" at engineering level; physics is solid but the techno-economic layer is thin
+- No independent third-party techno-economic assessment — `not-yet-sourced` — **nice-to-have**
 
 ---
 
@@ -37,24 +36,23 @@
 **Coverage**: Partial
 
 **Available**:
-- Energy flow skeleton is known: D-T fusion → neutron/alpha energy → HCPB blanket thermalization → Rankine steam → turbine. Standard enough to model at first pass.
-- Plasma physics basis is documented: Q > 40 burning plasma, alpha-dominated, ECRH only for startup/trim.
-- Steady-state operation with no disruption risk and no current drive power — simplifies recirculating power modeling compared to tokamaks.
-- TBR = 1.30 gives tritium self-sufficiency margin and feeds tritium processing load.
-- 2-year / 30-day maintenance cycle gives a basis for capacity factor and scheduled outage cost modeling.
+- Steady-state operation physics is well understood and confirmed: no plasma current drive, inherently disruption-free, ECRH as sole auxiliary heating (20 MW at full power)
+- Alpha-particle confinement in QI configuration: confirmed by dedicated JPP paper; good confinement in maximum-J geometry
+- Bootstrap current: <5 kA (very low), enabling stable island divertor operation
+- Divertor design challenge: explicitly quantified. Two divertor designs analyzed (classical island divertor and novel Large Island Backside Divertor, LIBD). Heat flux estimates, radiation fraction requirements, and particle exhaust efficiency estimated (cambridge-core-services PDF)
+- Island divertor particle pumping efficiency on W7-X: 0.44%–2.9%; required range for Infinity Two: 0.5%–5%; LIBD estimates 12.6% pumping efficiency in simplified slab model
+- Blanket-plasma integration: HCPB blanket with FLiBe zones; OpenMC neutronics confirms TBR=1.30 at 300M particles; sufficient room for blanket and shielding confirmed
 
 **Missing**:
-- Recirculating power breakdown: HTS magnets at 9 T require cryoplant at ~20 K; cryoplant parasitic load for a R=12.5 m machine is a significant cost driver that has not been published.
-- First wall and divertor heat loads: Power handling for an island divertor in QI geometry at 800 MWf is not publicly characterized at engineering design level.
-- Blanket-to-electricity efficiency chain: Stated ">30% thermal efficiency" but the gross electrical output, blanket energy multiplication factor (M_E, expected ~1.1–1.25 for HCPB/Be), and recirculating fraction needed to reconcile to 350 MWe net are not extracted from papers.
-- Engineering Q (Q_eng): Net electrical / recirculating electrical is not published; needed for LCOE.
-- Divertor design details: Island divertor for stellarator geometry adds non-trivial cost and maintenance complexity not captured in available data.
+- LIBD is a novel concept with no experimental validation; full EMC3-EIRENE modeling not yet completed; edge transport parameters (λ_q scaling with B and L_c) uncertain by factor of ~3 at reactor conditions
+- Compatibility of deep divertor detachment (>90% radiation fraction required) with high core plasma performance in a power plant: not yet demonstrated experimentally at reactor scale
+- Island divertor behavior at 9 T (W7-X data only at 2.5 T); no empirical scaling for Infinity Two field strength
+- 3D blanket integration around non-planar modular coil geometry: more challenging than tokamak; no detailed radial build published
 
 **Gaps**:
-- Gross electrical / recirculating power breakdown — `proprietary` likely, may be `not-yet-sourced` in E65 — **blocking** for quantitative LCOE
-- Blanket energy multiplication M_E — `not-yet-sourced` (likely in E86) — **important**
-- Island divertor heat load and design — `not-yet-sourced` or `proprietary` — **important**
-- Cryoplant parasitic load — `derivable` from first principles (scaling from W7-X or HELIAS studies) but unverified — **important**
+- Heat flux width scaling in island divertor at reactor conditions — `truly-unknown` — **important**: directly impacts divertor survival and availability; Infinity One experiment planned for 2029 but data unavailable now
+- LIBD experimental validation — `truly-unknown` — **important**: novel concept; existing W7-X data does not validate it
+- Detailed 3D radial build (coil–blanket–shield–vessel geometry) — `proprietary` — **important**: needed to assess maintenance, neutron shielding effectiveness, and component lifetimes
 
 ---
 
@@ -62,129 +60,121 @@
 **Coverage**: Partial
 
 **Available**:
-- QI stellarator physics: TRL 4–5. W7-X has demonstrated QI confinement and island divertor operation at low fusion-relevant parameters. Infinity Two configuration is optimized via 70,000+ DOE Frontier simulations — high design confidence but no plasma experiments at power-relevant parameters.
-- HCPB blanket: TRL 4–5. EU DEMO and ITER Test Blanket Module heritage. Li₄SiO₄/Li₂TiO₃ pebble bed with Be multiplier is reasonably well-characterized from European programs. The adaptation to stellarator geometry (non-cylindrical blanket segments) adds uncertainty.
-- Rankine steam cycle: TRL 9. Fully commercial technology. No maturity concern.
-- HTS REBCO magnets (wound): TRL 6–7 for tokamak geometry (CFS SPARC basis). TRL 4–5 for 3D stellarator coil geometry — this is the primary manufacturing bet.
-- Tritium systems: TRL 4–5 (no D-T facility at the scale needed has been built, though ITER will advance this).
+- **Plasma confinement/optimization** (TRL 5–6): QI/maximum-J configuration computationally optimized at exascale (Frontier); W7-X demonstrates modular coil stellarator at scale
+- **HTS magnets — planar** (TRL 7): MIT/CFS demonstrated 20 T in large-bore planar HTS coils (SPARC TFMC); licensed to Type One Energy
+- **HTS magnets — non-planar 3D stellarator** (TRL 3–4): Adaptation of HTS REBCO tape to wound-on-3D-form modular coil is novel; Riva et al. (2023) cited as development work; W7-X used LTS, not HTS
+- **ECRH heating** (TRL 8): Proven at W7-X and other stellarators; gyrotrons mature
+- **Island divertor** (TRL 5–6): Demonstrated successfully at W7-X with 10 MW heating and 110 s pulses; particle pumping efficiency lower than needed but manageable
+- **HCPB blanket** (TRL 4–5): EU DEMO heritage; solid Li₄SiO₄/Li₂TiO₃ ceramics + Be multiplier; OpenMC neutronics validated but no fusion-integrated hardware test
+- **Rankine steam cycle** (TRL 9): Fully mature technology; standard for conventional power generation
 
 **Missing**:
-- No published TRL assessment from Type One Energy for their specific subsystems.
-- HTS coil manufacturing readiness: wound REBCO on complex 3D forms at R=12.5m scale has no direct precedent. W7-X used LTS (NbTi/Nb₃Sn). CFS experience is with planar D-coils.
-- Island divertor at power-relevant heat loads: W7-X divertor operated at kW-level. Infinity Two requires handling O(100 MW) heat flux.
-- First wall materials qualification: no specific material selection documented publicly.
-- Remote maintenance system: Not documented in public sources. Complex 3D coil geometry complicates remote handling.
+- TRL for wound HTS REBCO tape on non-planar 3D coil forms at production scale: explicitly cited as development challenge in JPP papers; no publication characterizing yield, cost, or manufacturing throughput
+- Blanket integration hardware: HCPB module design for stellarator geometry (non-uniform radial access, complex blanket segmentation) not published
+- First wall / PFC materials for power-plant neutron fluence (14 MeV neutrons, multi-MW/m²): no component-level test data at fusion-relevant conditions; ITER PFCs are lower neutron fluence
+- LIBD component design and validation (TRL 2–3)
 
 **Gaps**:
-- HTS 3D stellarator coil manufacturing TRL — `not-yet-sourced` / `proprietary` — **important**
-- Island divertor at power-relevant conditions — `truly-unknown` (no experiment has approached this) — **important** (flags as risk rather than blocking analysis)
-- First wall material selection and lifetime — `not-yet-sourced` or `proprietary` — **important**
-- Remote maintenance architecture — `proprietary` — **nice-to-have** for cost modeling
+- HTS 3D non-planar coil manufacturing TRL and cost — `proprietary` / `not-yet-sourced` — **blocking**: dominant capital cost driver; no published data; Infinity One will validate concept but not yet built
+- HCPB blanket for stellarator 3D geometry — `not-yet-sourced` — **important**: EU DEMO literature covers tokamak geometry; stellarator-specific blanket integration requires engineering work not yet public
+- First wall neutron damage budget and replacement schedule — `not-yet-sourced` — **important**: affects availability and O&M cost
 
 ---
 
 ### 4. Key Materials and Supply Chain Considerations
-**Coverage**: Partial
+**Coverage**: Good (fleet-wide source covers D-T supply chain comprehensively)
 
 **Available**:
-- REBCO tape identified as magnet conductor — global supply chain is a known bottleneck. CFS partnership implies access, but tonnage requirements for 3D stellarator coil geometry at R=12.5m are not published.
-- HCPB materials (Li₄SiO₄ or Li₂TiO₃ pebbles, Be/Be₁₂Ti neutron multiplier): EU DEMO program has characterized supply requirements. Beryllium is a controlled, hazardous material with limited qualified suppliers.
-- Li-6 enrichment: Required for HCPB breeding. TBR = 1.30 implies sufficient breeding margin. Enrichment to 60–90% Li-6 needed. Supply chain exists but capacity-limited for fusion-scale deployment.
-- Tritium: Initial startup inventory required; TBR > 1 enables self-sufficiency after burnin period.
+- **Tritium**: CANDU production ~2 kg/yr; global stockpile ~30 kg (decaying); $35M/kg; supply window narrows after ~2035 as ITER and domestic programs come online; export controls on international transport (Pearson/DOE FES 2022)
+- **Lithium-6**: Near-zero commercial supply; COLEX (only historical production route) banned under Minamata Treaty; ICOMAX under development at KIT but decades to scale; need 30–90% enrichment for HCPB-type blanket (Pearson 2022)
+- **Beryllium**: Annual global production ~170 tons; one HCPB blanket requires ~170 tons (entire annual supply); Materion monopoly supplier; price ~$610/kg for alloy; export-controlled at >50% Be; toxicity makes manufacturing expensive (Pearson 2022)
+- **HTS REBCO tape**: CFS is primary industrial supplier; supply chain scaling is an acknowledged challenge across the MFE sector; Type One has licensed MIT HTS cable technology
+- General stellarator structural materials (reduced-activation ferritic steels, tungsten for divertor): well-characterized at W7-X and fusion materials programs; no specific supply gap identified
 
 **Missing**:
-- Tape length / total REBCO quantity estimate for Infinity Two coil set — not published.
-- Beryllium sourcing plan — no public documentation.
-- Specific Li-6 enrichment fraction and total Li inventory required — not extracted from E86.
-- Manufacturing process for complex 3D coil winding at scale — no public roadmap.
-- First wall material choice — not published (will determine activation and replacement supply chain).
+- Specific Li-6 enrichment strategy for Infinity Two's HCPB blanket: Pearson notes HCPB-type blankets require 30–60% Li-6 enrichment in quantities of 1–10 tonnes, but Infinity Two-specific procurement plan not published
+- HTS tape volume requirements for Infinity Two's coil set (large R=12.5 m, 9 T, modular 3D): not published; CFS supply capacity relative to Infinity Two demand unknown
+- Beryllium supply planning for pilot plant and subsequent commercial fleet: no Type One-specific assessment
 
 **Gaps**:
-- REBCO tape quantity for 3D coils at R=12.5m — `not-yet-sourced` / `proprietary` — **important** (major cost driver)
-- Beryllium quantity and supplier plan — `not-yet-sourced` (may be in E86) — **important**
-- Li-6 enrichment requirements — `not-yet-sourced` (likely in E86) — **important**
-- First wall material — `not-yet-sourced` or `proprietary` — **nice-to-have**
+- Li-6 enrichment supply chain for HCPB blanket at pilot scale — `not-yet-sourced` — **important**: no Western enrichment capacity; time to develop is decades per Pearson; but not concept-specific, affects all D-T HCPB designs
+- HTS tape volume and CFS supply capacity for Infinity Two — `proprietary` — **important**: a key cost and schedule risk
+- Beryllium procurement plan for pilot plant — `not-yet-sourced` — **nice-to-have**: Pearson notes pilot-scale quantities (~hundreds of tonnes) are achievable, but commercial fleet is a showstopper without action
 
 ---
 
 ### 5. LCOE Parameter Extraction
-**Coverage**: Poor (parameters known at concept level; quantitative values not extracted from papers)
+**Coverage**: Partial
 
 **Available Parameters**:
-
 | Parameter | Value/Range | Source | Confidence |
 |-----------|-------------|--------|------------|
-| Fusion power | 800 MW | J. Plasma Phys. E65 | high |
-| Net electrical output | 350 MWe | J. Plasma Phys. E65 | high |
-| Thermal efficiency | >30% (Rankine w/ reheat) | J. Plasma Phys. 2025 | high |
-| Major radius | 12.5 m | J. Plasma Phys. E65 | high |
-| Aspect ratio | 10 | J. Plasma Phys. E65 | high |
-| Field strength (on-axis) | 9 T | J. Plasma Phys. E65 | high |
-| Plasma gain (Q) | >40 | J. Plasma Phys. E65 | high |
-| TBR | 1.30 | J. Plasma Phys. E86 | high |
-| Planned outage schedule | 30 days / 2-year cycle | Press release May 2025 | high |
-| Capacity factor (planned only) | ~96% (730/760 days) | Derived from above | medium |
-| Blanket type | HCPB (Li₄SiO₄/Li₂TiO₃ + Be) | J. Plasma Phys. E86 | high |
-| Energy conversion | Rankine steam cycle | J. Plasma Phys. 2025 | high |
-| Field periods | 4 | J. Plasma Phys. E65 | high |
-| Plasma heating at steady-state | ECRH (small fraction at Q>40) | J. Plasma Phys. E65 | high |
+| Fusion power | 800 MW | JPP 2025 baseline + press release | h |
+| Net electric power | 350 MWe nominal | Press release, JPP overview | h |
+| Fuel | D-T | Multiple | h |
+| Plasma gain (Q) | >40 (access to ignition) | JPP E65 | h |
+| Tritium breeding ratio (TBR) | 1.30 | JPP E86 (OpenMC 300M particles) | h |
+| Blanket type | HCPB (Li₄SiO₄/Li₂TiO₃ + Be multiplier) | JPP E86 | h |
+| Coolant (blanket) | Helium | JPP E86 | h |
+| Energy conversion cycle | Rankine steam with reheat | JPP overview | h |
+| Thermal efficiency | >30% stated; Helios analog: 40% | JPP overview / Helios fleet source | m |
+| Auxiliary heating power | 20 MW ECRH at operating point | JPP E67 divertor paper | h |
+| Planned availability | 2-year cycle + 30-day planned outage (~96% planned) | Press release | m |
+| Estimated capacity factor | ~88% (Helios stellarator analog: biennial 84-day maintenance) | Helios fleet source | l (analog only) |
+| Operation mode | Steady-state (no pulsing, no current drive) | Multiple | h |
+| Magnet system | HTS REBCO, 9 T on-axis, R=12.5 m, A=10, 4-field-period | JPP papers | h |
+| Plant scale | Pilot plant (~350 MWe) | Multiple | h |
 
 **Missing Parameters**:
-
 | Parameter | Gap Type | Criticality | Notes |
 |-----------|----------|-------------|-------|
-| Capital cost by subsystem (magnets, blanket, vessel, BOP) | proprietary | blocking | No published cost estimates exist |
-| Gross electrical output | not-yet-sourced | blocking | Need to reconcile 350 MWe net; likely in E65 |
-| Recirculating power fraction | not-yet-sourced / proprietary | blocking | Cryoplant + ECRH + pumping; needed for Q_eng |
-| Blanket energy multiplication M_E | not-yet-sourced | important | Likely in E86; needed for thermal power calc |
-| First wall / blanket replacement interval | proprietary | important | Drives operating cost (major component) |
-| Coil set mass and cost estimate | proprietary | important | Primary capital cost driver; no analogue published at this scale |
-| ECRH system power and cost | not-yet-sourced | important | Small power fraction at burn but capital cost non-trivial |
-| Staffing / O&M cost analogues | derivable | important | Use ITER/DEMO O&M models as analogue |
-| Tritium startup inventory required | not-yet-sourced | important | Likely in E86 |
-| Unplanned outage rate | truly-unknown | important | No operating history; use conservative analogue (~85% availability) |
-| Cryoplant size and cost | derivable | important | Scaleable from W7-X with engineering assumptions |
-| Plant footprint / construction cost | proprietary | nice-to-have | R=12.5m stellarator will be very large; construction cost non-trivial |
+| Over-night capital cost (OCC) total | proprietary | blocking | No published estimate; fleet-wide analog: $8,800–22,200/kW for 350 MWe MFE tokamak (TEA D-T MFE source) |
+| Capital cost by CAS account | proprietary | blocking | No CAS breakdown published; Helios and ARIES-CS can provide stellarator structural analogs |
+| HTS coil capital cost | proprietary | blocking | Dominant cost driver; CFS manufactures but no pricing for Infinity Two geometry |
+| Annual O&M cost rate | not-yet-sourced | blocking | No published O&M estimate; ARIES-CS, Helios can provide analog range |
+| Blanket replacement schedule / interval | not-yet-sourced | important | First wall neutron flux: 14.1 MeV, vessel area 997 m²; specific fluence limit not published |
+| First wall lifetime (full-power-years) | not-yet-sourced | important | Material choice not fully specified (tungsten cited for divertor; first wall not stated) |
+| Gross thermal power (before recirculating) | derivable | important | Derivable from 800 MW fusion + TBR blanket energy multiplication; ~1.06–1.12 GW thermal expected |
+| Recirculating power fraction | derivable | important | ECRH at 20 MW at operating point; cryogenic load not published; rough estimate possible |
+| Decommissioning cost | not-yet-sourced | nice-to-have | Fleet-wide analog (ARIES, TEA MFE) can provide |
+| Fuel cost (deuterium, tritium startup) | derivable | nice-to-have | Tritium at $35M/kg (Pearson); startup inventory ~1–2 kg (Helios analog); D is negligible |
+| Scaling law / N-th-of-a-kind cost reduction | not-yet-sourced | nice-to-have | Only one plant proposed; NOAK trajectory not defined |
 
 ---
 
 ## Source Recommendations
 
-1. **Ingest all 6 J. Plasma Physics (2025) Physics Basis papers** — `not-yet-sourced`. These are the primary sources and almost certainly contain gross electrical, blanket energy multiplication, recirculating power fractions, and detailed geometry. The Cambridge collection URL is in the dossier. Priority: **critical before writing the analysis**.
+1. **ARIES-CS cost study** (`knowledge/sources/aries_cost_account_documentation/` + external ARIES-CS system study reports): The most relevant historical stellarator analog for CAS-level cost breakdown. ARIES-CS was a QI compact stellarator; cost accounts documented. Search OSTI for "ARIES-CS cost analysis" or "ARIES compact stellarator economics." — `unverified — confirm existence before searching`
 
-2. **HELIAS reactor studies (Beidler et al., IPP Garching)** — `not-yet-sourced`. HELIAS-5B and similar large-stellarator plant studies provide cost analogue data (coil system, cryoplant, vacuum vessel) for QI stellarators at similar scale. Search: OSTI or Fusion Engineering and Design for "HELIAS reactor study" or "HELIAS-5" — `unverified — confirm existence before searching`.
+2. **Helios full papers** (`knowledge/sources/overview_of_the_helios_design_a_practical_planar_coil/` — already extracted): The Helios overview paper was read (abstract only via arxiv-2512.08027 source); the full extracted output.md in the fleet-wide source is available and covers thermal cycle, BOP, capacity factor (88%), maintenance architecture, and magnet engineering. Use this as the primary stellarator analog for engineering and O&M parameters.
 
-3. **ARIES-CS compact stellarator study** — `not-yet-sourced`. Published ~2008, ARIES-CS is the most complete public techno-economic study for a modular stellarator. Has CAS cost breakdowns. Different geometry (A=4.5) but provides scaling basis. Search: "ARIES-CS" on OSTI — likely findable.
+3. **TEA D-T MFE cost analysis** (`knowledge/sources/tea_dt_mfe_cost_analysis/`): CAS-level cost breakdown for 350 MWe D-T MFE plant (tokamak); provides OCC range as upper/lower bound for MFE. Direct stellarator-to-tokamak comparison needed (stellarator likely lower fuel cycle cost, higher magnet complexity cost). Already ingested.
 
-4. **EU DEMO HCPB blanket cost data** — `not-yet-sourced`. EU DEMO preliminary design studies include HCPB blanket cost estimates per unit area. Relevant for Infinity Two blanket cost modeling. Search: EUROfusion reports or Fusion Engineering and Design for "DEMO HCPB blanket cost" — `unverified — confirm existence before searching`.
+4. **Infinity One design documentation** (when published): Type One Energy has stated Infinity One will be built in collaboration with TVA at the Bull Run site. Any published conceptual design report for Infinity One may reveal engineering-level detail. Search ANS/FED/IEEE TPS from 2025-onward. — `unverified — confirm existence before searching`
 
-5. **W7-X construction cost reports** — `not-yet-sourced`. W7-X (LTS) is the heritage machine. Construction costs (€1B+) provide a scaling anchor for stellarator coil complexity, even though HTS changes the conductor cost curve. Search: public IPP reports or peer-reviewed cost-of-construction analyses — `unverified — confirm existence before searching`.
+5. **W7-X experimental performance papers for capacity factor analog**: W7-X long-pulse campaigns (Grulke et al. 2024 cited in sources) can inform stellarator availability expectations. Published in Nuclear Fusion. — `not-yet-sourced`
 
-6. **CFS HTS tape cost projections** — `not-yet-sourced`. CFS has published some HTS tape cost roadmap estimates ($/kA-m) in investor and conference materials. These set the conductor cost floor for any HTS stellarator. Search: CFS white papers, IAEA FEC proceedings.
+6. **CFS HTS tape supply capacity papers or briefings**: Commonwealth Fusion Systems has published on REBCO tape procurement for SPARC. Any public briefing on tape volume and cost trajectory applies to Infinity Two (shared HTS technology). Search FED or IEEE TPS. — `unverified — confirm existence before searching`
 
 ---
 
 ## Summary
 
-**Proceed to full analysis, but extract the 6 J. Plasma Physics papers first.**
-
-Infinity Two is the best-documented private fusion concept for qualitative analysis — the physics basis is peer-reviewed and detailed, the system architecture is clear, and the key engineering bets are identifiable. The qualitative write-up can be written now with high confidence.
+Infinity Two has the strongest published physics basis of any private fusion concept in this study — seven peer-reviewed papers covering all key plasma subsystems with high-fidelity computational validation. The taxonomy-level differentiation data (all columns) is fully populated at high confidence. The primary D1+ gaps are economic: no concept-specific capital costs, O&M estimates, or OCC projection exist. These must be filled with the Helios stellarator design (best available analog: 88% CF, 40% thermal efficiency, 390 MWe) and the ARIES-CS CAS framework. Two physics-level uncertainties (LIBD experimental validation, island divertor heat flux width scaling at 9 T) are real but do not block the qualitative analysis; they become uncertainty flags in the LCOE sensitivity section. **Proceed to full D1+ analysis**, citing Helios as the primary engineering and cost analog and flagging capital cost estimates as fleet-wide bounds rather than concept-specific.
 
-For the quantitative LCOE model, the immediate blocker is that the six primary papers have not been ingested. Many of the "missing" parameters (gross electrical, blanket energy multiplication, recirculating power, tritium inventory) are likely present in E65 and E86 and can be extracted with one ingestion pass. Once extracted, the remaining gaps are primarily capital cost estimates, which must be derived from analogues (ARIES-CS, W7-X, HELIAS studies) with transparent uncertainty bounds — the `proprietary` classification applies to company-internal cost estimates, but public analogue estimation is viable and appropriate for a first-pass LCOE.
-
-The most significant substantive uncertainty (not a sourcing gap) is the HTS 3D stellarator coil manufacturing cost at R=12.5m scale. No machine of this type has been built with HTS. This is a genuine `truly-unknown` / `derivable-with-wide-uncertainty` parameter that will dominate the capital cost sensitivity analysis.
+---
 
 ## Structured summary (machine-readable)
 
 ```yaml
-overall_rating: "Mostly Ready (with sourcing gap)"
-blocking_count: 3
+overall_rating: "Mostly Ready"
+blocking_count: 4
 important_count: 8
-counting_method: "section_5_missing_parameters"
+counting_method: "section_5_missing_parameters (3 blocking: OCC, CAS breakdown, O&M) + section_3 (1 blocking: HTS 3D coil manufacturing TRL/cost); important counted across all sections deduplicated (LIBD validation, heat flux scaling, 3D blanket geometry, first wall lifetime, blanket replacement, recirculating power, gross thermal, HTS supply capacity)"
 section_coverage:
-  availability_of_data:       "Good (physics/architecture); Poor (economics)"
+  availability_of_data:       "Good"
   system_function:            "Partial"
   subsystem_maturity:         "Partial"
-  materials_supply_chain:     "Partial"
-  lcoe_parameter_extraction:  "Poor (parameters known at concept level; quantitative values not extracted from papers)"
-```
+  materials_supply_chain:     "Good"
+  lcoe_parameter_extraction:  "Partial"
+```
\ No newline at end of file
```

## Acceptance notes (fill during Phase 3)

- Deviation class (1-6 per plan.md): 
- Justified by fleet source? 
- Notes: 
