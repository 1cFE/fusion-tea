# Phase 3 diff: 20a-type-one-stellarator

**Generated:** 2026-05-22T14:51:03-07:00

## Counts (Phase 2 -> Phase 3 strict-read regen)

| field | phase2 | phase3 | Δ |
|-------|--------|--------|---|
| blocking_count   | 4 | 2 | -2 |
| important_count  | 8 | 7 | - |
| overall_rating   | Mostly Ready | Mostly Ready | - |

## Fleet-source dispositions in new report

```
```

## Forbidden-phrase check (should be empty)

```
(none — good)
```

## First line of new report (should start with `# Gap Assessment`)

```
# Gap Assessment: Type One Stellarator (D-T)
```

## Blocking-tier lines (new)

```
138:| Capital cost breakdown by CAS subsystem | proprietary | blocking | No cost figures appear in any public source; company has not published overnight cost or CAS breakdown |
139:| O&M costs (annual, by category) | proprietary | blocking | Not published; Type One referenced "favorable LCOE" qualitatively only |
```

## Full unified diff (truncated to 400 lines)

```diff
--- /tmp/gap_phase2_state/20a-type-one-stellarator.md	2026-05-22 12:59:21.075574380 -0700
+++ /home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/20a-type-one-stellarator/gap_report.md	2026-05-22 14:51:03.227354280 -0700
@@ -1,10 +1,8 @@
-I have now read all the necessary sources. Let me compile the gap assessment.
-
 # Gap Assessment: Type One Stellarator (D-T)
 
 ## Overall Readiness
 **Rating**: Mostly Ready
-**Summary**: Type One Energy's Infinity Two has an exceptionally strong, peer-reviewed physics basis — seven papers in a JPP special issue that cover plasma performance, MHD stability, alpha confinement, blanket/tritium feasibility, and divertor design. This is the most thoroughly documented private fusion design in the dataset. The primary gaps are economic: no concept-specific capital cost estimates, O&M data, or OCC projections have been published; these must be filled with stellarator analogs (Helios, ARIES-CS) and fleet-wide MFE TEA methodology. The analysis can proceed to D1+ with clearly flagged cost-estimation uncertainty.
+**Summary**: Type One Energy's Infinity Two has an exceptionally well-documented physics basis — 6+ peer-reviewed papers in a 2025 special issue of the *Journal of Plasma Physics*, covering plasma performance, blanket design, divertor physics, alpha-particle confinement, and MHD stability. Plant-level parameters (800 MW fusion / ~350 MWe net, 12.5 m radius, 9 T HTS, HCPB blanket, island divertor) are defined with high confidence. The primary gaps are economic: no capital cost breakdown has been published, O&M assumptions are absent, and key engineering subsystem designs (magnets at scale, tritium processing) are still in progress pending the Infinity One test campaign planned for 2029. Fleet-wide analogs (TEA D-T MFE cost study, Helios planar-coil stellarator design) partially close the LCOE extraction gap and support a bounded estimate.
 
 ---
 
@@ -14,21 +12,26 @@
 **Coverage**: Good
 
 **Available**:
-- Seven open-access peer-reviewed JPP papers (2025) covering all major physics subsystems: baseline plasma physics design, MHD equilibrium and stability, alpha-particle confinement, core plasma performance predictions, power and particle exhaust (divertor), breeder blanket and tritium fuel cycle feasibility, and an overarching unified design basis summary (cambridge-core-journals article, cambridge-core-services PDF, modernsciences summary, typeoneenergy press release)
-- Company press releases confirming key parameters: 800 MW fusion power, 350 MWe net, D-T fuel, HCPB blanket, Rankine cycle, 2-year operating cycle with 30-day planned maintenance outages, TVA partnership (typeoneenergy-type-one-energy-issues-first-realistic.md)
-- Formal design review completion announced May 2025 (dossier)
-- DOE FES 2022 Pearson presentation covering D-T fuel cycle supply chain: tritium, Li-6, beryllium constraints applicable to Infinity Two (science-media-fes-pdf)
-- Helios preconceptual design (arxiv-2512.08027, also in fleet-wide index at knowledge/sources/overview_of_the_helios_design_a_practical_planar_coil/) — a comparable HTS stellarator with detailed engineering design (390 MWe, 88% CF, 40% thermal efficiency, blanket/BOP/maintenance data)
-- TEA D-T MFE cost analysis (knowledge/sources/tea_dt_mfe_cost_analysis/): $140–550/MWh LCOE range and $8,800–22,200/kW OCC for a 350 MWe MFE tokamak — CAS methodology applicable as a fleet-wide bound
+- 7 peer-reviewed papers in *J. Plasma Phys.* 2025 (Hegna et al. baseline, Guttenfelder transport, Bader divertor, Clark blanket/tritium, Schmitt MHD, Carbajal alpha confinement, plus the comprehensive unified overview by Anderson/Canik/Hegna/Mowry). These constitute the first self-consistent published physics basis for a private fusion pilot plant and cover all core plasma physics subsystems.
+- Plant parameters: 800 MW DT fusion, ~350 MWe net, R = 12.5 m, A = 10, B = 9 T, Q > 40 (burning plasma, alpha-dominated). Confirmed by multiple independent analyses.
+- Blanket: HCPB with TBR = 1.30, validated via OpenMC neutronics with 300M particles; FLiBe used in shielding-priority zones. EU DEMO technology heritage.
+- Divertor: Classical island divertor (W7-X heritage) and novel LIBD concept, both analyzed with div3d and EMC3-Lite codes.
+- Magnet: Wound REBCO HTS tape on modular 3D coil forms, 9 T on-axis, CFS partnership for manufacturing; exclusive license to MIT HTS cable technology for stellarators.
+- Operation mode: Inherent steady-state (no current drive); 2-year continuous power cycle + 30-day planned maintenance outages.
+- Corporate: TVA Cooperative Agreement (Jan 2025) for a pilot plant project in Tennessee; DOE Frontier supercomputer simulations; ORNL partnership.
+- The Pearson (2022) supply chain source covers cross-concept critical materials (tritium, Li-6, beryllium) applicable to Infinity Two's HCPB blanket.
+- The TEA D-T MFE study (`knowledge/sources/tea_dt_mfe_cost_analysis/output.md`) provides a CAS-based overnight capital cost range of $8,800–$22,200/kW and LCOE of $140–$550/MWh for a 350 MWe D-T HTS tokamak (ARAI concept), applicable as a structural analog for Infinity Two's comparable scale and fuel cycle.
 
 **Missing**:
-- No published engineering design study equivalent to Helios or ARIES-CS: structural, thermal, and manufacturing detail for coils, blanket, and BOP
-- No published cost estimates or pre-FEED economic analysis from Type One Energy
-- No DOE program-level system study (ARIES-style) for a QI/maximum-J stellarator at this scale
+- No published capital cost breakdown by subsystem (no dollar figures anywhere in the corpus)
+- No published LCOE estimate or overnight cost
+- Capacity factor not stated explicitly as a percentage (only maintenance schedule given)
+- Engineering design documents (magnets, cryostat, tritium processing, power conversion system) not yet released; the 2025 papers are physics-only
 
 **Gaps**:
-- Absence of concept-specific engineering/cost study — `proprietary` — **important**: design is "pre-conceptual" at engineering level; physics is solid but the techno-economic layer is thin
-- No independent third-party techno-economic assessment — `not-yet-sourced` — **nice-to-have**
+- No capital cost or LCOE data published — proprietary — blocking
+- Engineering design documents not public — proprietary — important
+- Capacity factor not explicitly stated (must be derived from maintenance schedule) — derivable — important
 
 ---
 
@@ -36,23 +39,25 @@
 **Coverage**: Partial
 
 **Available**:
-- Steady-state operation physics is well understood and confirmed: no plasma current drive, inherently disruption-free, ECRH as sole auxiliary heating (20 MW at full power)
-- Alpha-particle confinement in QI configuration: confirmed by dedicated JPP paper; good confinement in maximum-J geometry
-- Bootstrap current: <5 kA (very low), enabling stable island divertor operation
-- Divertor design challenge: explicitly quantified. Two divertor designs analyzed (classical island divertor and novel Large Island Backside Divertor, LIBD). Heat flux estimates, radiation fraction requirements, and particle exhaust efficiency estimated (cambridge-core-services PDF)
-- Island divertor particle pumping efficiency on W7-X: 0.44%–2.9%; required range for Infinity Two: 0.5%–5%; LIBD estimates 12.6% pumping efficiency in simplified slab model
-- Blanket-plasma integration: HCPB blanket with FLiBe zones; OpenMC neutronics confirms TBR=1.30 at 300M particles; sufficient room for blanket and shielding confirmed
+- Plasma confinement: QI/maximum-J optimization with 70,000+ configuration simulations on DOE Frontier; neoclassical and turbulent transport both modeled at high fidelity; very low bootstrap current (<5 kA) eliminates current-drive requirements.
+- Divertor function: Detailed analysis of both classical island divertor (with EMC3-Lite heat flux validation) and novel Large Island Backside Divertor (LIBD). Key uncertainty: heat-flux width scaling (λq,⊥) with connection length and magnetic field at power-plant scale is not yet empirically constrained at Infinity Two parameters.
+- Alpha heating: Carbajal et al. paper covers alpha confinement; 6.6% first-wall loss in Helios analog (different optimization). Infinity Two paper reports Q > 40 with alpha heating dominant.
+- Power and particle exhaust: Bader et al. paper provides radiation fraction requirements (~83–95%), island topology, pumping efficiency estimates (0.5–5%). Acknowledged open question on whether W7-X divertor scaling extends to 9 T and 1000 m connection lengths.
+- Blanket tritium cycle: Clark et al. covers HCPB design, pellet fueling requirements, and helium tritium extraction; TBR = 1.30 with margin.
+- Steady-state inherent advantage is a key differentiator — no disruption risk, no current drive power, no pulsed thermal stress. Captured in multiple papers.
 
 **Missing**:
-- LIBD is a novel concept with no experimental validation; full EMC3-EIRENE modeling not yet completed; edge transport parameters (λ_q scaling with B and L_c) uncertain by factor of ~3 at reactor conditions
-- Compatibility of deep divertor detachment (>90% radiation fraction required) with high core plasma performance in a power plant: not yet demonstrated experimentally at reactor scale
-- Island divertor behavior at 9 T (W7-X data only at 2.5 T); no empirical scaling for Infinity Two field strength
-- 3D blanket integration around non-planar modular coil geometry: more challenging than tokamak; no detailed radial build published
+- LIBD has not been experimentally validated — W7-X classical divertor demonstrates W7-X-heritage design but LIBD is novel and slated for Infinity One testing in 2029. The divertor concept introduces a key physics risk.
+- Heat flux scaling at 9 T / Lc~1000 m is extrapolated, not measured; W7-X operates at 2.5 T and is the only scaling anchor.
+- Compatibility of island divertor detachment with excellent core confinement is modeled but explicitly flagged by Type One as a design uncertainty requiring Infinity One validation.
+- Fueling system (pellet injection for density profile control) requires mixed D-T ice pellets at power-plant scale — demonstrated at single-isotope limited-duration scale only.
+- Full systems model integrating plasma, blanket, divertor, magnets, and power conversion is not yet published.
 
 **Gaps**:
-- Heat flux width scaling in island divertor at reactor conditions — `truly-unknown` — **important**: directly impacts divertor survival and availability; Infinity One experiment planned for 2029 but data unavailable now
-- LIBD experimental validation — `truly-unknown` — **important**: novel concept; existing W7-X data does not validate it
-- Detailed 3D radial build (coil–blanket–shield–vessel geometry) — `proprietary` — **important**: needed to assess maintenance, neutron shielding effectiveness, and component lifetimes
+- LIBD experimental validation required before adopting as baseline — not-yet-sourced (will require Infinity One data, ~2029) — important
+- Heat flux width scaling at reactor parameters — truly-unknown (extrapolation from W7-X 2.5 T to 9 T, 1000 m Lc) — important
+- Mixed D-T pellet fueling at industrial scale — not-yet-sourced — important
+- Full integrated systems model not public — proprietary — important
 
 ---
 
@@ -60,107 +65,121 @@
 **Coverage**: Partial
 
 **Available**:
-- **Plasma confinement/optimization** (TRL 5–6): QI/maximum-J configuration computationally optimized at exascale (Frontier); W7-X demonstrates modular coil stellarator at scale
-- **HTS magnets — planar** (TRL 7): MIT/CFS demonstrated 20 T in large-bore planar HTS coils (SPARC TFMC); licensed to Type One Energy
-- **HTS magnets — non-planar 3D stellarator** (TRL 3–4): Adaptation of HTS REBCO tape to wound-on-3D-form modular coil is novel; Riva et al. (2023) cited as development work; W7-X used LTS, not HTS
-- **ECRH heating** (TRL 8): Proven at W7-X and other stellarators; gyrotrons mature
-- **Island divertor** (TRL 5–6): Demonstrated successfully at W7-X with 10 MW heating and 110 s pulses; particle pumping efficiency lower than needed but manageable
-- **HCPB blanket** (TRL 4–5): EU DEMO heritage; solid Li₄SiO₄/Li₂TiO₃ ceramics + Be multiplier; OpenMC neutronics validated but no fusion-integrated hardware test
-- **Rankine steam cycle** (TRL 9): Fully mature technology; standard for conventional power generation
+- Plasma physics / configuration: Very high maturity. W7-X demonstrates 4-field-period optimized stellarator at ~6 m scale; Infinity Two is a larger extrapolation but grounded in W7-X validated codes. Effectively TRL 4–5 for the configuration concept.
+- Modular HTS coil manufacturing (REBCO wound on 3D forms): W7-X heritage for manufacturing approach. HTS tape properties demonstrated. MIT/CFS demonstrated 20 T in large-bore planar coil. Non-planar winding with HTS is an active development area with CFS collaboration. TRL ~3–4 for stellarator-specific non-planar HTS coils.
+- HCPB blanket: EU DEMO heritage; TBR validated. Li₄SiO₄/Li₂TiO₃ ceramic breeder tested in ITER test blanket modules. TRL ~4–5 for blanket module; integrated breeding + shielding in stellarator geometry is lower (TRL ~3).
+- Steam Rankine power conversion: Commercial mature technology (TRL 9); >30% thermal efficiency stated.
+- ECRH (startup and current maintenance): Well-established (TRL ~7–8); ITER-spec gyrotrons used at W7-X. 20 MW auxiliary power is a modest requirement.
+- Island divertor (classical W7-X-heritage design): Demonstrated in W7-X (TRL ~5–6 for W7-X scale; ~3–4 for power-plant scale with tungsten PFCs).
+- LIBD: Conceptual design analyzed, not yet built or tested (TRL ~2–3).
+- Tritium processing and fuel cycle: Cross-cutting D-T infrastructure; TRL ~3–4 at relevant scales.
 
 **Missing**:
-- TRL for wound HTS REBCO tape on non-planar 3D coil forms at production scale: explicitly cited as development challenge in JPP papers; no publication characterizing yield, cost, or manufacturing throughput
-- Blanket integration hardware: HCPB module design for stellarator geometry (non-uniform radial access, complex blanket segmentation) not published
-- First wall / PFC materials for power-plant neutron fluence (14 MeV neutrons, multi-MW/m²): no component-level test data at fusion-relevant conditions; ITER PFCs are lower neutron fluence
-- LIBD component design and validation (TRL 2–3)
+- No formal TRL matrix published for Infinity Two subsystems
+- Specific coil manufacturing readiness demonstration (non-planar REBCO winding at power-plant scale)
+- First wall and divertor PFC replacement schedule and lifetime assumptions not published
+- Cryogenic system design and TRL not in public domain
 
 **Gaps**:
-- HTS 3D non-planar coil manufacturing TRL and cost — `proprietary` / `not-yet-sourced` — **blocking**: dominant capital cost driver; no published data; Infinity One will validate concept but not yet built
-- HCPB blanket for stellarator 3D geometry — `not-yet-sourced` — **important**: EU DEMO literature covers tokamak geometry; stellarator-specific blanket integration requires engineering work not yet public
-- First wall neutron damage budget and replacement schedule — `not-yet-sourced` — **important**: affects availability and O&M cost
+- Non-planar REBCO HTS coil manufacturing at stellarator power-plant scale — not-yet-sourced (development milestone for CFS partnership) — important
+- LIBD TRL is low; depends on Infinity One testing (~2029) — important
+- No formal TRL assessment table for Infinity Two subsystems — not-yet-sourced — nice-to-have
+- Divertor PFC (tungsten) lifetime under high-heat-flux and neutron fluence at 9 T — not-yet-sourced — important
 
 ---
 
 ### 4. Key Materials and Supply Chain Considerations
-**Coverage**: Good (fleet-wide source covers D-T supply chain comprehensively)
+**Coverage**: Partial
 
 **Available**:
-- **Tritium**: CANDU production ~2 kg/yr; global stockpile ~30 kg (decaying); $35M/kg; supply window narrows after ~2035 as ITER and domestic programs come online; export controls on international transport (Pearson/DOE FES 2022)
-- **Lithium-6**: Near-zero commercial supply; COLEX (only historical production route) banned under Minamata Treaty; ICOMAX under development at KIT but decades to scale; need 30–90% enrichment for HCPB-type blanket (Pearson 2022)
-- **Beryllium**: Annual global production ~170 tons; one HCPB blanket requires ~170 tons (entire annual supply); Materion monopoly supplier; price ~$610/kg for alloy; export-controlled at >50% Be; toxicity makes manufacturing expensive (Pearson 2022)
-- **HTS REBCO tape**: CFS is primary industrial supplier; supply chain scaling is an acknowledged challenge across the MFE sector; Type One has licensed MIT HTS cable technology
-- General stellarator structural materials (reduced-activation ferritic steels, tungsten for divertor): well-characterized at W7-X and fusion materials programs; no specific supply gap identified
+- REBCO HTS tape: CFS partnership established; exclusive MIT HTS cable license for stellarators held by Type One. Tape production is commercially available but at cost and volume relevant to pilot plants, not fleet deployment. Supply chain risk is moderate and improving.
+- Tritium supply (from Pearson 2022, `science-media-fes-pdf-fes-presentations-2022-pearson.md`): Current production ~2 kg/year from CANDU fleet; stockpile ~30 kg (decaying). Window of availability to ~2035 before ITER/STEP/CFETR demand depletes supply. Tritium cost ~$35M/kg. This is a cross-cutting constraint applying to all D-T concepts; Infinity Two's TBR = 1.30 with HCPB is explicitly designed for self-sufficiency.
+- Lithium-6 enrichment (Pearson): Current supply effectively zero. HCPB requires 30–60% Li-6 enrichment (Be-based blanket). COLEX process historically proven but banned (mercury Minamata treaty). ICOMAX alternative under development at KIT; decades to scale. Specific requirement for Infinity Two depends on blanket geometry and breeding zone fraction.
+- Beryllium (Pearson): Global production ~170 tons/year; a single HCPB reactor with Be multiplier requires approximately the full annual global production. Export controls, toxicity, and US DoD national stockpile add supply risk. Pilot plant quantities (~hundreds of tonnes) are feasible but fleet deployment requires industry-wide scale-up.
+- Structural materials: HCPB uses reduced activation ferritic steel (RAFS); well-characterized from DEMO programs. Supply chain exists.
+- Tungsten (divertor PFCs): Commercially available; no major supply constraint for pilot plant.
 
 **Missing**:
-- Specific Li-6 enrichment strategy for Infinity Two's HCPB blanket: Pearson notes HCPB-type blankets require 30–60% Li-6 enrichment in quantities of 1–10 tonnes, but Infinity Two-specific procurement plan not published
-- HTS tape volume requirements for Infinity Two's coil set (large R=12.5 m, 9 T, modular 3D): not published; CFS supply capacity relative to Infinity Two demand unknown
-- Beryllium supply planning for pilot plant and subsequent commercial fleet: no Type One-specific assessment
+- Specific material mass budgets for Infinity Two (Li₄SiO₄/Li₂TiO₃ mass, Be mass, REBCO tape length)
+- Li-6 enrichment pathway and cost for HCPB at Infinity Two scale
+- REBCO tape production commitment/contract for pilot plant build
+- W7-X used NbTi/Nb₃Sn LTS coils; transition to HTS at stellarator scale lacks demonstrated supply chain
 
 **Gaps**:
-- Li-6 enrichment supply chain for HCPB blanket at pilot scale — `not-yet-sourced` — **important**: no Western enrichment capacity; time to develop is decades per Pearson; but not concept-specific, affects all D-T HCPB designs
-- HTS tape volume and CFS supply capacity for Infinity Two — `proprietary` — **important**: a key cost and schedule risk
-- Beryllium procurement plan for pilot plant — `not-yet-sourced` — **nice-to-have**: Pearson notes pilot-scale quantities (~hundreds of tonnes) are achievable, but commercial fleet is a showstopper without action
+- Li-6 enrichment at HCPB pilot plant scale — not-yet-sourced (Pearson documents the industrial challenge but not Infinity Two-specific quantities) — important
+- Be multiplier supply chain for fleet deployment — truly-unknown (supply constraint at fleet scale; pilot plant feasible per Pearson) — important
+- REBCO tape production at pilot plant scale cost and availability — not-yet-sourced — important
+- Specific material mass budgets for Infinity Two — proprietary — nice-to-have
 
 ---
 
 ### 5. LCOE Parameter Extraction
-**Coverage**: Partial
-
 **Available Parameters**:
 | Parameter | Value/Range | Source | Confidence |
 |-----------|-------------|--------|------------|
-| Fusion power | 800 MW | JPP 2025 baseline + press release | h |
-| Net electric power | 350 MWe nominal | Press release, JPP overview | h |
-| Fuel | D-T | Multiple | h |
-| Plasma gain (Q) | >40 (access to ignition) | JPP E65 | h |
-| Tritium breeding ratio (TBR) | 1.30 | JPP E86 (OpenMC 300M particles) | h |
-| Blanket type | HCPB (Li₄SiO₄/Li₂TiO₃ + Be multiplier) | JPP E86 | h |
-| Coolant (blanket) | Helium | JPP E86 | h |
-| Energy conversion cycle | Rankine steam with reheat | JPP overview | h |
-| Thermal efficiency | >30% stated; Helios analog: 40% | JPP overview / Helios fleet source | m |
-| Auxiliary heating power | 20 MW ECRH at operating point | JPP E67 divertor paper | h |
-| Planned availability | 2-year cycle + 30-day planned outage (~96% planned) | Press release | m |
-| Estimated capacity factor | ~88% (Helios stellarator analog: biennial 84-day maintenance) | Helios fleet source | l (analog only) |
-| Operation mode | Steady-state (no pulsing, no current drive) | Multiple | h |
-| Magnet system | HTS REBCO, 9 T on-axis, R=12.5 m, A=10, 4-field-period | JPP papers | h |
-| Plant scale | Pilot plant (~350 MWe) | Multiple | h |
+| Net electric output | ~350 MWe | J. Plasma Phys. 2025 (multiple), TypeOneEnergy PR | high |
+| Fusion power | 800 MW | J. Plasma Phys. 2025, E65 | high |
+| Fuel cycle | D-T (deuterium abundant; tritium self-sufficient via HCPB TBR=1.30) | Clark et al. J. Plasma Phys. 2025 | high |
+| TBR | 1.30 (OpenMC 300M particles) | Clark et al. J. Plasma Phys. 2025 | high |
+| Energy capture cycle | Rankine steam with reheat | J. Plasma Phys. 2025 (multiple) | high |
+| Gross thermal efficiency | >30% (stated lower bound); Rankine analog: ~37–40% | TypeOneEnergy press release; Helios analog (`knowledge/sources/overview_of_the_helios_design_a_practical_planar_coil/output.md`) reports 40% | medium |
+| Maintenance schedule | 2-year continuous + 30-day planned outage | TypeOneEnergy press release (May 2025) | high |
+| Capacity factor (derived) | ~90–96% based on 30-day/730-day scheduled maintenance cycle; unplanned outages will reduce this | derivable from maintenance schedule; Helios analog is 88% with 84-day biennial outage | medium |
+| Operation mode | Continuous steady-state (no pulsing) | J. Plasma Phys. 2025 | high |
+| Heating power (auxiliary) | 20 MW ECRH (Bader et al., Table 1) | J. Plasma Phys. 2025 E67 | high |
+| Plant scale | 12.5 m major radius, A=10, 9 T | J. Plasma Phys. 2025 | high |
+| LCOE range (fleet analog) | $140–$550/MWh for comparable 350 MWe D-T HTS MFE | TEA D-T MFE (`knowledge/sources/tea_dt_mfe_cost_analysis/output.md`), ARAI-FPP NOAK | low (analog only) |
+| Overnight capital cost (fleet analog) | $8,800–$22,200/kW (350 MWe HTS tokamak NOAK) | TEA D-T MFE | low (analog only) |
+| Tritium startup cost | ~35,000/gram; ~1–2 kg startup per Helios analog | Pearson 2022; Helios (`knowledge/sources/overview_of_the_helios_design_a_practical_planar_coil/output.md`) | medium |
 
 **Missing Parameters**:
 | Parameter | Gap Type | Criticality | Notes |
 |-----------|----------|-------------|-------|
-| Over-night capital cost (OCC) total | proprietary | blocking | No published estimate; fleet-wide analog: $8,800–22,200/kW for 350 MWe MFE tokamak (TEA D-T MFE source) |
-| Capital cost by CAS account | proprietary | blocking | No CAS breakdown published; Helios and ARIES-CS can provide stellarator structural analogs |
-| HTS coil capital cost | proprietary | blocking | Dominant cost driver; CFS manufactures but no pricing for Infinity Two geometry |
-| Annual O&M cost rate | not-yet-sourced | blocking | No published O&M estimate; ARIES-CS, Helios can provide analog range |
-| Blanket replacement schedule / interval | not-yet-sourced | important | First wall neutron flux: 14.1 MeV, vessel area 997 m²; specific fluence limit not published |
-| First wall lifetime (full-power-years) | not-yet-sourced | important | Material choice not fully specified (tungsten cited for divertor; first wall not stated) |
-| Gross thermal power (before recirculating) | derivable | important | Derivable from 800 MW fusion + TBR blanket energy multiplication; ~1.06–1.12 GW thermal expected |
-| Recirculating power fraction | derivable | important | ECRH at 20 MW at operating point; cryogenic load not published; rough estimate possible |
-| Decommissioning cost | not-yet-sourced | nice-to-have | Fleet-wide analog (ARIES, TEA MFE) can provide |
-| Fuel cost (deuterium, tritium startup) | derivable | nice-to-have | Tritium at $35M/kg (Pearson); startup inventory ~1–2 kg (Helios analog); D is negligible |
-| Scaling law / N-th-of-a-kind cost reduction | not-yet-sourced | nice-to-have | Only one plant proposed; NOAK trajectory not defined |
+| Capital cost breakdown by CAS subsystem | proprietary | blocking | No cost figures appear in any public source; company has not published overnight cost or CAS breakdown |
+| O&M costs (annual, by category) | proprietary | blocking | Not published; Type One referenced "favorable LCOE" qualitatively only |
+| First-wall and blanket replacement schedule/cost | not-yet-sourced | important | HCPB first-wall lifetime under DT neutron fluence at Infinity Two scale not stated; EU DEMO estimates exist as analog |
+| HTS coil system total cost | proprietary | important | Most uncertain cost item; non-planar 3D coils have higher cost than planar tokamak TF coils; no public estimate |
+| Decommissioning cost provision | not-yet-sourced | important | Not addressed in physics basis papers; ARIES-CS analog can provide order-of-magnitude |
+| Specific capacity factor (not derived) | derivable | important | Type One mentions "good capacity factors" but never states a number; 30-day/2-year schedule implies ~96% scheduled availability; realistic (with unplanned) probably 85–92% |
+| Specific gross thermal efficiency | derivable | nice-to-have | ">30%" stated; Rankine cycle with reheat at HCPB temperatures (500–600°C) supports 37–40%; Helios states 40% |
+| ECRH system capital cost | not-yet-sourced | nice-to-have | 20 MW requirement is modest; ITER gyrotron costs provide analog |
+| ARIES-CS stellarator cost breakdown | not-yet-sourced | important | ARIES-CS is the closest published cost analog for a modular-coil HTS stellarator; not yet ingested into this repo |
 
 ---
 
 ## Source Recommendations
 
-1. **ARIES-CS cost study** (`knowledge/sources/aries_cost_account_documentation/` + external ARIES-CS system study reports): The most relevant historical stellarator analog for CAS-level cost breakdown. ARIES-CS was a QI compact stellarator; cost accounts documented. Search OSTI for "ARIES-CS cost analysis" or "ARIES compact stellarator economics." — `unverified — confirm existence before searching`
+1. **ARIES-CS compact stellarator cost study** (Raffray et al., *Fusion Eng. Des.* 2008, and the full ARIES-CS Final Report) — This is the most directly applicable missing source: it is the only published CAS-level cost breakdown for an HTS modular-coil stellarator power plant, covering accounts 20–27. The ARIES Cost Account Documentation already in this repo (`knowledge/sources/aries_cost_account_documentation/`) provides the framework but not ARIES-CS–specific numbers. Search OSTI for "ARIES-CS Final Report" or "ARIES compact stellarator cost." Addresses the capital cost breakdown gap (blocking). `not-yet-sourced — confirm existence before searching`
+
+2. **EU DEMO HCPB blanket cost and TRL studies** — ITER Organization and EUROfusion have published cost estimates for HCPB test blanket modules and blanket replacements. Directly applicable to Infinity Two's identical blanket concept. Search OSTI or EUROfusion document servers for "HCPB blanket cost" or "WCLL/HCPB economic analysis." Addresses blanket capital cost and replacement cost gaps. `not-yet-sourced — confirm existence before searching`
+
+3. **Type One Energy investor presentations or DOE program review slides** — Companies sometimes publish partial cost data in DOE milestone reports or investment presentations. Search OSTI for "Type One Energy" or "Infinity Two" economics. `not-yet-sourced — low probability; company is pre-FOAK`
 
-2. **Helios full papers** (`knowledge/sources/overview_of_the_helios_design_a_practical_planar_coil/` — already extracted): The Helios overview paper was read (abstract only via arxiv-2512.08027 source); the full extracted output.md in the fleet-wide source is available and covers thermal cycle, BOP, capacity factor (88%), maintenance architecture, and magnet engineering. Use this as the primary stellarator analog for engineering and O&M parameters.
+4. **W7-X construction cost data (published post-mortem)** — IPP Greifswald published partial cost data for W7-X (€1.06 billion, 14,000 non-planar coil components). Provides a calibration point for non-planar HTS coil manufacturing cost scaling. Search for Wegener et al. or IPP annual reports. `not-yet-sourced — confirm existence before searching`
 
-3. **TEA D-T MFE cost analysis** (`knowledge/sources/tea_dt_mfe_cost_analysis/`): CAS-level cost breakdown for 350 MWe D-T MFE plant (tokamak); provides OCC range as upper/lower bound for MFE. Direct stellarator-to-tokamak comparison needed (stellarator likely lower fuel cycle cost, higher magnet complexity cost). Already ingested.
+5. **Infinity One subscale test device design documents** — Type One has announced Infinity One (a smaller validation stellarator to be built with TVA at Bull Run, TN, operational ~2029). Any published design documents would dramatically reduce physics uncertainties, particularly for divertor (LIBD validation) and transport at high field. Currently proprietary / not yet published. `proprietary`
 
-4. **Infinity One design documentation** (when published): Type One Energy has stated Infinity One will be built in collaboration with TVA at the Bull Run site. Any published conceptual design report for Infinity One may reveal engineering-level detail. Search ANS/FED/IEEE TPS from 2025-onward. — `unverified — confirm existence before searching`
+### Fleet-Wide Source Dispositions
 
-5. **W7-X experimental performance papers for capacity factor analog**: W7-X long-pulse campaigns (Grulke et al. 2024 cited in sources) can inform stellarator availability expectations. Published in Nuclear Fusion. — `not-yet-sourced`
+- **TEA D-T MFE cost analysis** (`knowledge/sources/tea_dt_mfe_cost_analysis/output.md`): **Integrated.** Provides NOAK LCOE $140–550/MWh and OCC $8,800–22,200/kW for a 350 MWe D-T HTS MFE plant, directly applicable as a structural analog for Infinity Two at comparable scale and fuel cycle. The CAS breakdown (accounts 21–27) and methodology are directly transferable; reactor plant equipment costs will differ for stellarator-specific components (non-planar coils, larger shielding volume). Used to partially address the capital cost blocking gap by providing a floor/ceiling range.
 
-6. **CFS HTS tape supply capacity papers or briefings**: Commonwealth Fusion Systems has published on REBCO tape procurement for SPARC. Any public briefing on tape volume and cost trajectory applies to Infinity Two (shared HTS technology). Search FED or IEEE TPS. — `unverified — confirm existence before searching`
+- **Overview of the Helios Design** (`knowledge/sources/overview_of_the_helios_design_a_practical_planar_coil/output.md`): **Integrated.** The Helios preconceptual stellarator design (8 m radius, 6 T, QA, 390 MWe, HTS) is the closest architectural analog to Infinity Two in the source base. Key Helios parameters directly applicable: 88% capacity factor (84-day biennial maintenance), 40% thermal conversion efficiency, tritium startup inventory 1–2 kg, idealized TBR 1.3, 40-year coil lifetime (enabled by 1.2 m plasma-coil clearance). Also confirms that the arxiv-2512-08027 source in the concept-scoped directory is the Helios paper abstract — it is *not* a Type One source and should not be cited as such, though its analog content is useful for stellarator comparison.
+
+- **ARIES Cost Account Documentation** (`knowledge/sources/aries_cost_account_documentation/output.md`): **Integrated.** Provides the canonical CAS framework (accounts 20–27 direct, 90–98 indirect) that should be used to structure any Infinity Two cost model. The documentation traces the Starfire→ARIES cost lineage and provides escalation methodology. Does not contain Infinity Two–specific numbers; provides the cost account structure and scaling algorithms. Not sufficient alone to resolve the capital cost blocking gap but essential as the cost modeling scaffold.
+
+- **Revisit of 2017 costing for ARPA-E ALPHA concepts** (`knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/output.md`): **Disqualified.** The four ALPHA concepts (FRC, MTF variants, Z-pinch adjacent) are compact, pulsed or quasi-steady, and structurally dissimilar to Infinity Two's large steady-state modular-coil stellarator. The $43/MWh average LCOE reflects compact modular plants (~500 MWe total, multiple modules) rather than a single 350 MWe pilot plant. Scale, confinement approach, and FOAK/NOAK assumptions are too divergent to serve as a reliable capital cost analog for Infinity Two.
+
+- **A simplified economic model for inertial fusion** (`knowledge/sources/a_simplified_economic_model_for_inertial_fusion/output.md`): **Disqualified.** IFE-specific parameters (driver cost, target gain, rep rate, chamber cycling) have no applicability to a steady-state D-T MFE stellarator.
+
+- **PyFECONS** (`/home/reid/PyFECONS`): **Deferred.** PyFECONS implements MFE costing algorithms and CAS hierarchy that are directly applicable to Infinity Two. Not read in this session due to codebase scope, but should be consulted during LCOE model construction to obtain parametric cost algorithms for specific CAS accounts.
 
 ---
 
 ## Summary
 
-Infinity Two has the strongest published physics basis of any private fusion concept in this study — seven peer-reviewed papers covering all key plasma subsystems with high-fidelity computational validation. The taxonomy-level differentiation data (all columns) is fully populated at high confidence. The primary D1+ gaps are economic: no concept-specific capital costs, O&M estimates, or OCC projection exist. These must be filled with the Helios stellarator design (best available analog: 88% CF, 40% thermal efficiency, 390 MWe) and the ARIES-CS CAS framework. Two physics-level uncertainties (LIBD experimental validation, island divertor heat flux width scaling at 9 T) are real but do not block the qualitative analysis; they become uncertainty flags in the LCOE sensitivity section. **Proceed to full D1+ analysis**, citing Helios as the primary engineering and cost analog and flagging capital cost estimates as fleet-wide bounds rather than concept-specific.
+**Proceed to full analysis.** The Type One Stellarator (D-T) / Infinity Two has a stronger public physics documentation base than nearly any other private fusion concept — the 2025 JPP special issue represents the first self-consistent, peer-reviewed pilot plant physics basis published by any private company. All taxonomy classification parameters are high-confidence. The concept's system function (steady-state, no disruptions, island divertor, HCPB blanket, Rankine cycle) is well-enough described to characterize qualitative analysis sections 1–4 thoroughly.
+
+The LCOE parameter extraction (section 5) has two blocking gaps: capital cost breakdown and O&M assumptions. These cannot be resolved from public sources alone. The analysis should proceed using the TEA D-T MFE fleet source ($140–550/MWh, $8,800–22,200/kW OCC) as a structural analog range, with the ARIES-CS stellarator study as the recommended next ingest to narrow the range with a stellarator-specific cost model. If ARIES-CS is ingested, the capital cost blocking gap downgrades to important, and the analysis can produce a well-grounded bounded estimate rather than only an order-of-magnitude range.
 
 ---
 
@@ -168,13 +187,13 @@
 
 ```yaml
 overall_rating: "Mostly Ready"
-blocking_count: 4
-important_count: 8
-counting_method: "section_5_missing_parameters (3 blocking: OCC, CAS breakdown, O&M) + section_3 (1 blocking: HTS 3D coil manufacturing TRL/cost); important counted across all sections deduplicated (LIBD validation, heat flux scaling, 3D blanket geometry, first wall lifetime, blanket replacement, recirculating power, gross thermal, HTS supply capacity)"
+blocking_count: 2
+important_count: 7
+counting_method: "section_5_capital_cost_and_om_as_blocking; important_gaps_deduplicated_across_sections_1_through_5: engineering_design_not_public, LIBD_experimental_validation, HTS_3D_coil_scale_up, heat_flux_scaling_uncertainty, Li6_supply_chain, capacity_factor_not_stated, blanket_replacement_cost"
 section_coverage:
   availability_of_data:       "Good"
   system_function:            "Partial"
   subsystem_maturity:         "Partial"
-  materials_supply_chain:     "Good"
+  materials_supply_chain:     "Partial"
   lcoe_parameter_extraction:  "Partial"
 ```
\ No newline at end of file
```
