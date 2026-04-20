# D1+ Analysis: Compact Spherical Tokamak - India (Pranos Fusion)

**Concept**: Compact Spherical Tokamak — D-T fuel, modular 50 MW target
**Company**: Pranos Fusion (Bengaluru, India; founded May 2024)
**Confinement Family**: MFE — Spherical Tokamak
**Nearest neighbor**: 21-spherical-tokamak-hts (Tokamak Energy)

---

## Section 1: Availability of Data

**Rating: Opaque**

Pranos Fusion is among the least documented concepts in the analysis portfolio. Two sources were identified and ingested across two research iterations. Neither contains technical data adequate to anchor an LCOE model.

**Source 1 — Company overview compiled from web research** (`pranos-fusion-overview.md`):
Provides founding date (May 2024), seed round (USD 417K from Industrial47 and Startup India, May 14, 2025), team backgrounds, and vision. The document explicitly flags: "Extremely limited. No published specifications for: Magnet type (HTS vs LTS vs resistive); Heating method; Blanket/tritium breeding approach; Energy conversion method; Plasma parameters (temperature, density, confinement time); Machine dimensions or aspect ratio." No patents, preprints, or conference presentations were found. The company website is JavaScript-rendered and unsearchable.

**Source 2 — IAEA FUSE Portal profile** (`iaea-fuse-pranos-profile.md`):
The most authoritative available source. Confirms D-T fuel, compact spherical tokamak architecture, and a staged experimental program with three configurations named (Ragya, Pragya, PraniQ). Confirms completed TF coil engineering designs (stress analysis + CAD). Confirms the "Jenga" digital twin platform integrating MHD, transport, neutronics, thermal-structural, PMI, and plant-level systems engineering modules. Does not provide plasma parameters, machine dimensions, magnet material, heating method, or blanket approach.

**Peer-reviewed publications**: None found for Pranos Fusion specifically. One arXiv preprint (arxiv-2603-11549, submitted March 12 2026, not yet peer-reviewed) describes the PRAGYA vacuum vessel: "Design and mechanical analysis of the PRAGYA tokamak vacuum vessel" by Gupta, Koneru, Sarkar, Ansumali, Kuley, George, and Kaushal. This is the first published technical document for any Pranos hardware — it covers the experimental precursor device (PRAGYA), not the commercial 50 MW module.

**Independent analyses**: None covering Pranos specifically. The broader spherical tokamak literature (UKAEA PROCESS-based studies, Hidalgo-Salaverri et al. 2025, Brown 2018) provides ST cost structure templates but cannot be directly applied without any Pranos machine parameters.

**National fusion context**: India's Institute for Plasma Research (IPR, Gandhinagar) operates SST-1 (superconducting tokamak) and Aditya-U (air-cooled conventional tokamak). The SS-ST spherical tokamak at IPR was commissioned December 2025. Pranos co-founder Shaurya Kaushal has prior UKAEA experience. The company claims Atal Innovation Mission support and operates from JNCASR Bengaluru, where preliminary plasma experiments are described as "working with plasma in a glass globe." No formal affiliation with IPR or access to its facilities is documented.

**PRAGYA experimental device (Source 3 — arxiv-2603-11549)**: The March 2026 arXiv preprint provides confirmed geometry for PRAGYA — India's first privately developed low-aspect-ratio tokamak: major radius R₀ = 0.4 m, minor radius a > 0.18 m (aspect ratio A ≈ 2.2), toroidal field B_T = 0.1 T, plasma current Ip ≤ 25 kA. The paper presents 3D FEM structural analysis of the vacuum vessel under combined self-weight, atmospheric pressure, and thermal baking loads, confirming safety margins are satisfied and the device is ready for "subsequent plasma operations." These are experimental-device parameters (PRAGYA), not the commercial 50 MW module. B_T = 0.1 T is far below any commercial operating point; the aspect ratio A ≈ 2.2 confirms ST family classification, consistent with the nearest neighbor (21-spherical-tokamak-hts, A ≈ 2.3). Magnet type, coil material, and heating method are not discussed in the preprint.

**Phase 1a dossier completeness**: High confidence on confinement family, confinement concept (spherical tokamak), fuel (D-T), and operation mode (steady-state). PRAGYA parameters now provide a first experimental geometry baseline (R₀, a, A, B_T, Ip). Low confidence on magnet type, primary heating, plasma state, and tritium breeding approach remain. Driver technology is unknown. Most commercial-design gaps are structural — the company is in the computational design phase and has published no commercial-scale specifications.

**Key data gaps limiting this analysis**:
1. Commercial design plasma parameters unknown — PRAGYA experimental parameters are now published (R₀=0.4 m, B_T=0.1 T, Ip≤25 kA) but describe a low-field proof-of-concept, not the commercial 50 MW module; Q, fusion power, and confinement time are unknown for both
2. Commercial machine geometry (R, A, B_T) not disclosed — PRAGYA geometry (A≈2.2) confirms ST family but cannot anchor a commercial LCOE model
3. Magnet type unknown — determines the dominant capital cost item
4. Heating method not specified — determines recirculating power and Q_engineering
5. No blanket or tritium breeding approach specified
6. No cost estimates, plant studies, or system code outputs exist for this concept

---

## Section 2: Challenges in Capturing System Function

The absence of any published design parameters means that all LCOE modeling for Pranos must rely on ST analogue assumptions with no concept-specific anchors. Challenges are ranked by LCOE impact.

**1. Modular 50 MW target — non-standard scale with severe cost penalty (Impact: Critical)**

The Pranos vision of 2,500 × 50 MW modular reactors producing 125 GW collectively is categorically different from every other tokamak design in the analysis portfolio. All existing fusion TEA frameworks (ARIES, PROCESS-based models, Araiinejad & Shirvan 2025, Hidalgo-Salaverri et al. 2025) are calibrated for 250–1,000 MWe plant-scale output. Applying these frameworks to a 50 MWe unit requires extrapolation across a factor of 5–20 in output, where economies of scale are most punishing.

The problem is structural: key fusion plant cost elements have large fixed or sublinearly-scaling components that do not shrink proportionally with output. The tritium fuel cycle (isotope separation, accountability, storage) has fixed infrastructure cost regardless of machine size. Center stack shielding in a spherical tokamak requires ~30 cm of radial depth to protect HTS magnets from neutron irradiation — this radial fraction becomes proportionally larger in a small machine, consuming prime plasma volume. Building and site infrastructure costs are largely fixed per unit. The ARIES-ST study found that ST capital cost scales approximately as $/kWe ∝ P^{-0.4} relative to a reference plant [analogue from ARIES-ST cost scaling, cited in 21-spherical-tokamak-hts analysis §Section 2]; at 50 MWe vs. 500 MWe, this implies a ~2.5–3× specific capital cost penalty relative to plant-scale output.

The offsetting argument for modularity is factory learning: with 2,500 units, learning-curve effects (typically 15–20% cost reduction per doubling of cumulative production) could in principle compress per-unit costs dramatically. However, this requires a functioning first-of-kind plant to validate performance before committing to fleet production — a staging problem the company has not addressed in any public documentation. The small modular fission reactor (SMR) industry has encountered exactly this tension and found the economics challenging even with an established physics base.

**2. Unknown machine parameters — no physics anchor (Impact: Critical)**

Without R, A, B_T, or plasma current, no self-consistent design point can be established. The Q value (fusion gain) is particularly critical for a small device: at 50 MW electrical output with a ~30% thermal efficiency assumption, gross thermal power is ~170 MW, implying fusion power of roughly 150–200 MW (minus blanket multiplication and recirculating losses). Achieving this from a compact spherical tokamak requires either high Q (to minimize auxiliary heating's share of gross power) or very high beta operation (to compensate for lower field). Neither has been established for the Pranos geometry. Without these parameters, the entire cost chain from fusion power → thermal power → electrical output → LCOE cannot be closed.

**3. Magnet type unknown — the largest single cost driver is uncharacterized (Impact: High)**

Magnet systems (TF + PF + CS coils) represent the dominant capital cost item in most ST designs, ranging from 20–40% of direct capital cost depending on field strength and coil complexity [analogue from Brown 2018, cited in 21-spherical-tokamak-hts §Section 2]. The choice of HTS (REBCO), LTS (Nb₃Sn or NbTi), or resistive copper magnets changes this cost element by an order of magnitude — resistive copper magnets have low upfront capital but enormous recirculating power demand; HTS has high capital but very low cryogenic load; LTS sits between. No information exists to determine which Pranos has chosen. TF coil CAD and stress analysis have been completed, but material choice is not stated in any public source.

**4. No heating method — recirculating power and Q_engineering unknown (Impact: High)**

For a 50 MWe plant, recirculating power for auxiliary heating is proportionally more important than for a large plant. If Pranos uses NBI or RF at 30–50 MW of auxiliary input to drive a 150–200 MW fusion power device, the recirculating fraction could be 15–25% of gross electric, materially degrading Q_engineering. If Q is high enough that bootstrap current dominates and auxiliary heating is minimal, the situation improves. No basis exists to assess either scenario.

**5. Blanket and tritium breeding — entirely uncharacterized (Impact: High)**

D-T fuel is confirmed, creating an unavoidable requirement for tritium self-sufficiency (TBR > 1). For a 50 MW ST, the blanket design faces the same outboard-only geometry constraint as larger STs — the center stack cannot accommodate a breeding blanket — but with even less outboard solid angle available for breeding at smaller aspect ratio. No blanket type, material, or TBR target has been disclosed.

**6. Regulatory environment — India context is uncertain (Impact: Moderate)**

India's atomic energy regulatory framework (operated by the Atomic Energy Regulatory Board, AERB) has no established pathway for private fusion energy plants. Unlike the US (NRC Part 30 decision, 2023) or UK (separate fusion regulation underway), India's fusion regulatory landscape is essentially blank for private developers. This creates permitting uncertainty analogous to the Stewart & Shirvan (2022) 2.2× building cost scenario identified for US concepts [01-hts-compact-tokamak.md, §Section 2], and may be more severe given the absence of a precedent or regulatory roadmap.

---

### Testable Modeling Hypotheses

The challenges above translate into three model hypotheses that the cost model should explore as named scenarios or sensitivity sweeps:

**H1 — HTS vs. resistive copper magnet choice (scenario branch)**
IF Pranos adopts resistive copper magnets instead of HTS (motivated by lower upfront capital and India's limited HTS supply chain), THEN recirculating power for magnet cooling rises to 30–40% of gross electric at commercial-scale field, degrading Q_engineering and potentially rendering the 50 MWe net output target infeasible. Testable by: running the model with a resistive magnet parameter set (high recirculating power, low magnet capital) vs. HTS set (low recirculating power, high magnet capital) and comparing LCOE and Q_engineering for both.

**H2 — Factory learning threshold for modular fleet viability (sensitivity sweep)**
IF cumulative production learning across 2,500 units delivers ≥20% cost reduction per doubling of units produced (Wright's Law), THEN the specific capital cost of the 2,500th unit converges toward the large-plant reference ($5,000–$8,000/kWe). Testable by: sweeping the learning curve exponent from 0 (no learning) to 0.25 (aggressive learning) and identifying the break-even exponent at which LCOE reaches a competitive threshold ($100–$150/MWh). This is the core economic thesis of the modular fleet concept.

**H3 — India regulatory scenario (scenario branch)**
IF the AERB applies a fission-style regulatory framework (no fusion-specific pathway), THEN building and civil cost accounts increase by ~2.2× per the Stewart & Shirvan (2022) scenario, pushing LCOE above $1,000/MWh at the 50 MWe scale. Testable by: applying the 2.2× building cost multiplier and showing LCOE shift vs. the base case.

---

## Section 3: Maturity of Key Subsystems and Components

Ordered from least mature (highest risk) to most mature. All assessments reflect the state of Pranos Fusion specifically; the broader ST technology base is credited where relevant but cannot substitute for company-specific demonstration.

---

**Tritium Fuel Cycle and Blanket System — TRL 1–2 (Pranos-specific)**

- **Demonstrated**: D-T fuel confirmed; no other tritium-cycle details disclosed. Broader ST literature (ITER TBM program, Pb-17Li extraction research) provides analogue data for blanket concepts generically.
- **On paper only**: No blanket type, breeder material, or tritium extraction approach has been disclosed for Pranos. The Jenga digital twin includes a neutronics module, suggesting some neutronics modeling may be in progress, but no outputs have been published.
- **Missing at scale**: A complete tritium breeding and extraction system designed around the specific Pranos geometry. Outboard-only breeding geometry (characteristic of all compact STs) requires Li-6-enriched breeder material to achieve TBR > 1 with limited solid angle — but without machine dimensions, even this requirement cannot be quantified.

---

**Heating and Current Drive System — TRL 1–2 (Pranos-specific)**

- **Demonstrated**: Not specified. The company has not disclosed a heating approach. Analogues exist for both NBI and RF heating on small spherical tokamaks (MAST-U, NSTX-U, ST40), but no Pranos-specific design or selection has been made public.
- **On paper only**: All heating system design for Pranos. Jenga platform integration of MHD and transport codes implies heating scenarios are being modeled, but no outputs or parameter targets are available.
- **Missing at scale**: Selection of heating approach (RF vs NBI), power level, and wall-plug efficiency target — all of which are needed to compute Q_engineering and recirculating power for any given design point.

---

**Magnet System (TF/PF/CS Coils) — TRL 3 (PRAGYA device, FEM validated); TRL 1–2 (commercial 50 MW)**

- **Demonstrated**: TF coil stress analysis and CAD completed for PRAGYA, per IAEA FUSE Portal. The arXiv preprint further confirms that the vacuum vessel design — which structurally integrates with the magnet system — has passed 3D FEM analysis under combined loading [arxiv-2603-11549 §Abstract]. This represents TRL 3 (experimental proof of concept validated analytically) for the experimental device. Broader context: HTS spherical tokamak magnets at pilot scale have been demonstrated by Tokamak Energy (Demo4, complete 14 TF + 2 PF coil set, 11.8 T, November 2025 [referenced in 21-spherical-tokamak-hts §Section 3]), providing technology existence proof for the HTS route — but Pranos has not confirmed they are using HTS.
- **On paper only**: Any physical magnet component for Pranos. Material selection (HTS/LTS/resistive) not disclosed. The TF coil CAD is the most advanced confirmed technical artifact.
- **Missing at scale**: Magnet procurement, fabrication, or test plan. If HTS route chosen, REBCO tape sourcing and India-specific supply chain for superconducting materials would need to be established (no domestic REBCO production at scale; import dependency from Japan, China, or US). If resistive copper, recirculating power at this scale would likely be prohibitive for commercial operation.

---

**Plasma Physics Experimental Basis — TRL 2–3 (Pranos PRAGYA device); TRL 1 (commercial 50 MW concept)**

- **Demonstrated**: PRAGYA (R₀ = 0.4 m, B_T = 0.1 T, Ip ≤ 25 kA) is in final engineering design phase with 3D FEM structural analysis of the vacuum vessel complete — combined self-weight, atmospheric pressure, and thermal baking stress analyzed, safety margins confirmed [arxiv-2603-11549 §Abstract]. The device is described as ready for "subsequent plasma operations." This is a meaningful hardware milestone beyond the earlier glass-globe description. Three experimental configurations (Ragya, Pragya, PraniQ) are named in the IAEA FUSE profile; PRAGYA is the one with published engineering data.
- **On paper only**: PRAGYA plasma commissioning. The Jenga digital twin platform (MHD, transport, neutronics, thermal-structural, PMI, plant-level integration) — no validated outputs published. Commercial-scale design point.
- **Missing at scale**: Actual plasma discharge in PRAGYA; any tokamak-relevant plasma parameters (density, temperature, confinement time); commercial 50 MW design point. The gap from PRAGYA (0.1 T experimental device) to a commercial ST (typically 2–5 T) is several decades of development time at the pace of MAST, NSTX, and ST40 — even if PRAGYA achieves first plasma promptly.

---

**Remote Maintenance System — TRL 1 (Pranos-specific) / TRL 5–6 (generic ST)**

- **Demonstrated**: Not specified for Pranos. Broader ITER program provides remote handling technology at advanced development stage for conventional tokamak geometry [01-hts-compact-tokamak.md, §Section 3].
- **On paper only**: All remote maintenance design for Pranos. Modular design concept implies some level of planned serviceability.
- **Missing at scale**: Any maintenance scheme or access concept for the specific Pranos geometry.

---

**Balance of Plant — TRL 1–2 (Pranos-specific) / TRL 7–9 (generic thermal cycle)**

- **Demonstrated**: Conventional Rankine and Brayton cycles are commercially mature at GW scale. Integration with 50 MW fusion heat sources is not addressed in any public source. Thermal efficiency and conversion cycle are undisclosed.
- **On paper only**: Complete BOP design for Pranos. The 50 MW scale may enable use of smaller industrial turbomachinery (versus utility-scale steam turbines at 500 MW+), potentially reducing BOP cost in absolute terms — but at the cost of lower thermal efficiency (smaller turbines are less thermodynamically efficient) and losing economies of scale in heat rejection.
- **Missing at scale**: Sized BOP for Pranos design; tritium-compatible heat exchangers between primary and secondary loops.

---

## Section 4: Key Materials and Supply Chain Considerations

**Tritium — Binding Constraint for All D-T Concepts**

D-T fuel is confirmed, creating the full tritium supply chain requirement. The global tritium inventory is approximately 25–30 kg, produced primarily as a CANDU heavy-water reactor byproduct, decaying at 5.5%/year [01-hts-compact-tokamak.md, §Section 4]. Startup inventory for a D-T plant is approximately 1 kg at >$35,000/g. India does not currently operate CANDU reactors and has no domestic tritium production infrastructure, creating an import dependency from Canada (CANDU operators) or Russia. For a fleet of 2,500 × 50 MW units, tritium startup inventory demands would be enormous (~2,500 kg total), requiring demonstrated self-sufficient breeding well in advance of any fleet deployment. This constraint applies identically to all D-T concepts but the fleet-scale ambition makes it acute for Pranos.

**REBCO Superconducting Tape — Critical Bottleneck if HTS Route Chosen**

If Pranos adopts HTS magnets (the most technically appropriate choice for a compact ST design, based on Tokamak Energy's demonstrated ST-HTS approach), REBCO tape supply constraints apply directly. Global production is on the order of a few thousand km/year; a single compact ST requires thousands of km depending on machine scale and field [01-hts-compact-tokamak.md, §Section 4; 21-spherical-tokamak-hts §Section 4]. India has no domestic REBCO manufacturing at scale. All tape would need to be imported from Japan (Fujikura, Sumitomo), China (Shanghai Superconductor Technology), or the US (AMSC, SuperPower). For a fleet of 2,500 units, this supply chain would need to be effectively nationalized or massively scaled — a decade-scale infrastructure challenge independent of the physics.

**Li-6 Enrichment — Supply Chain Dominated by Russia and China**

D-T breeding requires lithium enriched in the Li-6 isotope (natural abundance ~7.5%). High-Li-6 enrichment capacity is controlled by Russia and China, which use mercury amalgam processes banned in Western countries. A Western-alternative enrichment pathway (laser isotope separation, ion exchange) is under development but not yet at commercial scale [21-spherical-tokamak-hts §Section 4]. India's access to Li-6 enriched material would require either technology transfer from an established supplier or development of a domestic isotope separation capability — neither is underway at present.

**Tungsten (Plasma-Facing Components) — Adequate Global Supply, Manufacturing Challenges Shared**

First-wall and divertor tungsten supply is adequate globally. Manufacturing challenges (large-area tiles, thermal fatigue resistance) are shared with all D-T tokamak concepts and are being addressed by the ITER program. Not a supply bottleneck; an engineering challenge.

**India Domestic Supply Chain — Nascent Fusion Ecosystem**

Unlike the US (where CFS, Tokamak Energy, and others have created a growing HTS magnet supply chain) or the UK (where Tokamak Energy, First Light, and others benefit from UKAEA infrastructure), India's private fusion supply chain is essentially absent. The national fusion program (through IPR and the Institute for Plasma Research) has materials capability for conventional LTS magnets and basic vacuum hardware, but not HTS tape production, fusion-grade blanket materials, or large-scale tritium handling. Pranos would need to import most critical materials and likely manufacture specialized components abroad — creating both supply chain risk and potentially unfavorable import economics for a "distributed clean energy for India" positioning.

---

## Section 5: LCOE-Relevant Parameters

### Available Parameters

| Parameter | Value/Range | Source | Confidence | Notes |
|-----------|-------------|--------|------------|-------|
| Target electrical output per module | 50 MW | pranos-fusion-overview.md §Technology Description | medium | Company vision target; not derived from a closed design point |
| Fleet vision | 2,500 modules × 50 MW = 125 GW | pranos-fusion-overview.md §Technology Description | medium | Vision statement; "3,000 GWh daily" implies ~87% capacity factor at 125 GW |
| Fuel | D-T | iaea-fuse-pranos-profile.md §Fuel (confirmed as "Deuterium-Tritium (D-T) — explicitly stated") | high | IAEA FUSE confirmation |
| Architecture | Compact spherical tokamak | iaea-fuse-pranos-profile.md §Architecture | high | Explicitly stated; IAEA FUSE describes "compact spherical tokamak architectures" |
| Operation mode | Steady-state | pranos-fusion-overview.md §Operation | medium | Consistent with power-producing ST design intent; not explicitly confirmed |
| Experimental program stage | Pre-tokamak (glass globe plasma) | pranos-fusion-overview.md §Founders | high | Direct description of current experimental state |
| Company funding | USD 417K seed | pranos-fusion-overview.md §Funding | high | Seed round from Industrial47 and Startup India, May 2025 |
| TF coil design | Stress analysis + CAD completed | iaea-fuse-pranos-profile.md §Technical Progress | medium | Most advanced confirmed hardware-design artifact; material not disclosed |
| Digital twin platform | Jenga (MHD, transport, neutronics, thermal-structural, PMI, plant-level) | iaea-fuse-pranos-profile.md §Technology | medium | Most substantive technical capability described; no validated outputs published |
| **PRAGYA experimental device — major radius (R₀)** | 0.4 m | arxiv-2603-11549.md §Abstract | medium | Experimental precursor device; not the commercial 50 MW target |
| **PRAGYA experimental device — minor radius (a)** | >0.18 m | arxiv-2603-11549.md §Abstract | medium | Lower bound stated; exact value not given |
| **PRAGYA experimental device — aspect ratio (A)** | [inferred] ≈ 2.2 | [derived: R₀/a = 0.4/0.18 ≈ 2.2] | medium | Confirms ST family classification; consistent with nearest neighbor (21-spherical-tokamak-hts, A ≈ 2.3) |
| **PRAGYA experimental device — toroidal field (B_T)** | 0.1 T | arxiv-2603-11549.md §Abstract | medium | Far below commercial ST operating point (typically 2–5 T); experimental scale only |
| **PRAGYA experimental device — plasma current (Ip)** | ≤ 25 kA | arxiv-2603-11549.md §Abstract | medium | Upper design limit for experimental device |
| **PRAGYA vacuum vessel structural validation** | 3D FEM complete; safety margins satisfied under self-weight + atmospheric pressure + thermal baking loads | arxiv-2603-11549.md §Abstract | medium | Device "ready for subsequent plasma operations" per paper |
| Implied capacity factor from vision statement | [inferred] ~87% | [derived: 3,000 GWh/day ÷ (2,500 × 50 MW × 24 h) = 1.0; ~87% for realistic availability] | low | Back-calculation from fleet energy vision; no stated capacity factor target |
| Gross thermal power per module (estimated) | [estimated] 140–200 MW_th | [estimated: 50 MWe ÷ 30–35% thermal efficiency] | low | Assumes steam Rankine; thermal efficiency unknown |
| Implied fusion power per module (estimated) | [estimated] 120–180 MW_fusion | [estimated from gross thermal minus blanket multiplication uncertainty] | low | Requires thermal efficiency and blanket gain assumptions; both unknown |
| Specific capital cost (analogue, ST at 50 MW scale, overnight) | [analogue] $10,000–$30,000/kWe | [analogue: ARIES-ST cost scaling applied to 50 MWe; 2.5–4× penalty vs. 500 MWe ST; reference from Brown 2018 and ARIES-ST] | low | Overnight cost only; does not include IDC or India regulatory multiplier. Model output of ~$47,750/kWe represents total capital including IDC (~$525 M) and indirect cost fractions — exceeds this range. If India regulatory scenario (Stewart & Shirvan 2.2×) is applied to the building cost accounts, total capital with IDC can plausibly reach $40,000–$55,000/kWe. Both bounds carry very high uncertainty. |

### Missing Parameters

| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Major radius (R), aspect ratio (A) — **commercial design** | truly-unknown (pre-design) | blocking | PRAGYA experimental baseline now known (R₀=0.4 m, A≈2.2); commercial 50 MW design point is a separate unknown — not derivable from PRAGYA |
| On-axis toroidal field (B_T) — **commercial design** | truly-unknown (pre-design) | blocking | PRAGYA B_T = 0.1 T (experimental); commercial ST requires ~2–5 T; field determines beta, fusion power density, and magnet cost |
| Q value / fusion gain | truly-unknown (pre-design) | blocking | Company is in computational design phase; Q not yet determined |
| Plasma current | truly-unknown (pre-design) | blocking | Required for confinement time scaling and current drive requirements |
| Magnet type (HTS / LTS / resistive) | proprietary | blocking | Largest single cost item; type determines cost structure entirely |
| Heating method and auxiliary power | proprietary / not-yet-published | blocking | Determines recirculating power fraction and Q_engineering |
| Blanket type and TBR target | proprietary / not-yet-published | blocking | Required for tritium self-sufficiency assessment |
| Power conversion cycle and thermal efficiency | truly-unknown (pre-design) | blocking | All LCOE estimates require thermal efficiency assumption |
| Plant capacity factor | truly-unknown (pre-design) | blocking | Second-largest LCOE driver after CAPEX |
| Overnight capital cost | truly-unknown (pre-design) | blocking | No plant study, cost estimate, or analogue applicable without machine parameters |
| Center stack shielding design | truly-unknown (pre-design) | important | ST-specific requirement; dimensions depend on machine R and B which are unknown |
| Remote maintenance scheme | truly-unknown (pre-design) | important | Required for availability estimate; not addressed in any source |
| O&M cost breakdown | truly-unknown (pre-design) | important | Fixed vs. variable O&M, scheduled maintenance intervals — all unknown |
| Li-6 enrichment level and blanket geometry | truly-unknown (pre-design) | important | Cannot be estimated without machine dimensions |

---

## Section 6: Data Gap Inventory

| # | Gap Description | Section | Gap Type | Criticality | Source Recommendation |
|---|-----------------|---------|----------|-------------|----------------------|
| 1 | Machine geometry (R, A, B_T) not disclosed — prevents any physics-based LCOE anchor | S1, S2, S5 | proprietary / not-yet-published | blocking | Watch for conference presentations (APS DPP, IEEE SOFE, IAEA Fusion Energy Conference); Pranos UKAEA-connected co-founder may present at UK venues |
| 2 | Q value / fusion gain not established — pre-design phase | S2, S5 | truly-unknown | blocking | PROCESS or similar code run with ST analogue parameters (A=1.5–2.0, B=2–4 T) could bound Q for plausible 50 MW designs |
| 3 | Magnet type not disclosed — largest cost item uncharacterized | S2, S3, S5 | proprietary | blocking | HTS is most physically appropriate for compact ST; assume REBCO HTS for baseline analogue with sensitivity to resistive alternative |
| 4 | Heating method not disclosed — recirculating power unknown | S2, S3, S5 | proprietary / not-yet-published | blocking | Apply NBI or RF analogue from comparable small ST (MAST-U, NSTX-U) as placeholder |
| 5 | Blanket approach not disclosed — tritium self-sufficiency uncharacterized | S2, S3, S5 | proprietary / not-yet-published | blocking | Apply outboard-only liquid Li analogue from 21-spherical-tokamak-hts; flag as completely unconfirmed |
| 6 | Power conversion cycle and thermal efficiency unknown | S2, S5 | truly-unknown | blocking | Apply steam Rankine 30–33% as conservative analogue baseline |
| 7 | Plant capacity factor not published | S2, S5 | truly-unknown | blocking | Apply Araiinejad & Shirvan (2025) D-T MCF range (75–90%); no Pranos-specific basis |
| 8 | Overnight capital cost — no plant study or analogue applicable | S1, S5 | truly-unknown | blocking | Cannot estimate without machine parameters; ARIES-ST at comparable scale is the most distant usable reference |
| 9 | Modular 50 MW scale penalty — no fusion TEA framework covers this scale | S2, S5 | truly-unknown | blocking | Develop scaling analysis from ARIES-ST cost model adjusted for power output; document uncertainty explicitly |
| 10 | India regulatory framework for private fusion — no established pathway | S2 | truly-unknown | important | Monitor AERB regulatory developments; apply Stewart & Shirvan 2.2× building cost scenario as upper bound |
| 11 | Center stack neutron shielding design at 50 MW ST scale | S3 | truly-unknown | important | Humphry-Baker & Smith (2019) studied R=1.35 m ST; scaling to Pranos geometry requires machine parameters |
| 12 | India domestic supply chain for HTS tape, Li-6, tritium | S4 | truly-unknown | important | No domestic REBCO or Li-6 enrichment capacity; import dependency creates cost and geopolitical risk |
| 13 | O&M cost structure — no maintenance scheme disclosed | S2, S5 | truly-unknown | important | Apply generic D-T tokamak O&M range from Araiinejad & Shirvan (2025) as placeholder; modular design may reduce per-unit maintenance cost but this is unquantified |
| 14 | Jenga digital twin validation — no published outputs | S3 | not-yet-sourced | nice-to-have | If Pranos publishes Jenga model outputs, these could provide design point parameters; monitor preprint servers |
| 15 | Li-6 enrichment level required for TBR > 1 in compact ST outboard blanket | S4 | derivable | nice-to-have | Derivable once machine dimensions are known; sets Li import requirements |

---

## Section 7: Cross-Concept Notes

The approved analysis for Spherical Tokamak - HTS (`21-spherical-tokamak-hts`, Tokamak Energy) is the nearest neighbor for this concept. Both are compact spherical tokamaks targeting D-T power generation. The following elements from the ST-HTS analysis are conditionally reused here, subject to the caveat that Pranos has disclosed no design parameters and these assumptions may be entirely wrong.

**Conditionally reused (ST family assumptions):**

- **Center stack geometry constraint**: All compact STs face the same fundamental constraint — the center stack cannot accommodate a breeding blanket, forcing outboard-only tritium breeding [21-spherical-tokamak-hts §Section 2]. The 30 cm radial shielding requirement identified by Humphry-Baker & Smith (2019) for HTS protection applies in principle to any HTS-equipped compact ST, though the absolute dimensions depend on machine scale.
- **D-T tritium supply chain**: Global tritium inventory (~25–30 kg), startup requirements (~1 kg at >$35,000/g), and CANDU supply decline apply identically to Pranos as a D-T concept [01-hts-compact-tokamak.md §Section 4].
- **REBCO supply chain** (conditional on HTS magnet choice): If Pranos uses HTS, the global production bottleneck (~few thousand km/year), current pricing ($30–100/kA-m), and commercial viability target (~$10/kA-m) apply [21-spherical-tokamak-hts §Section 4]. This is a conditional assumption — magnet type is unconfirmed.
- **Regulatory cost uncertainty**: The Stewart & Shirvan (2022) 2.2× building cost scenario applies to any D-T fusion concept, including Pranos [01-hts-compact-tokamak.md §Section 2]. The India-specific regulatory context may amplify this uncertainty further given the absence of a fusion-specific regulatory pathway.
- **Pulsed vs. steady-state trade-off**: Pulsed spherical tokamak operation (preferred for ST geometry per Gryaznevich et al. 2023) creates a thermal energy buffering requirement absent from steady-state designs [21-spherical-tokamak-hts §Section 2]. This applies if Pranos adopts pulsed operation, but their declared "steady-state" mode may attempt to avoid this complication — at the cost of greater current drive requirements.

**Key divergences from Tokamak Energy ST-HTS:**

- **Scale**: Tokamak Energy ST-E1 targets 450–750 MWe from a single plant (R=5.0 m, A=2.3); Pranos targets 50 MWe per module with no disclosed machine geometry. This is the most fundamental divergence and drives the severe scale penalty discussed in Section 2.
- **Funding and stage**: Tokamak Energy has $335M in funding and a validated complete HTS magnet coil set (Demo4, November 2025). Pranos has $417K seed and is working with a glass globe plasma. The maturity gap is approximately 10–15 years of development and multiple orders of magnitude in funding. This is not a criticism of the concept but is essential context for any development timeline or risk assessment.
- **India context**: Tokamak Energy operates within an established UK/US HTS supply chain and benefits from UKAEA and DOE collaboration. Pranos operates in a country with no private fusion supply chain, limited HTS procurement history, and no established fusion regulatory pathway for private developers.
- **Modular fleet vs. single plant**: The economic thesis differs entirely — Tokamak Energy is pursuing a single large pilot plant leading to commercial plants; Pranos is pursuing thousands of small distributed units. These imply very different cost learning paths, financing structures, and regulatory sequencing.

**ST family cost structure patterns relevant to the TEA pipeline** (from 21-spherical-tokamak-hts §Section 7):
1. Outboard-only blanket coverage — TBR sensitivity to port fractions is higher than in 4π designs.
2. Center stack as a separate capital and O&M cost category.
3. Thermal energy storage if pulsed.
4. Lower field → different CAPEX driver mix (less magnet cost per unit fusion power, if beta target is met).

For Pranos specifically, the TEA pipeline would need a distinct module at the 50 MW scale that does not exist in any published framework. Any cost estimate must carry a "highly speculative" flag until machine parameters are published.

---

## Section 8: Sources

**1. pranos-fusion-overview.md — Company overview from web research (iter-01)**
- Contribution: Founding date, funding ($417K seed round, Industrial47 and Startup India), team backgrounds (co-founder Shaurya Kaushal, UKAEA experience, PhD computational physics), Bengaluru location, 50 MW modular vision statement, glass globe experimental stage, website accessibility notes. Primary source for company stage and team characterization.
- Location: `knowledge/concept_research/34-compact-spherical-tokamak-india/iter-01/sources/pranos-fusion-overview.md`

**2. iaea-fuse-pranos-profile.md — IAEA FUSE Portal profile for Pranos (iter-02)**
- Contribution: Most authoritative available source. Confirms D-T fuel (explicitly), compact spherical tokamak architecture, three experimental configurations (Ragya, Pragya, PraniQ), completed TF coil engineering designs (stress analysis + CAD), and Jenga digital twin platform scope (MHD, transport, neutronics, thermal-structural, PMI, plant-level). Explicitly lists what is NOT specified (plasma parameters, heating method, blanket, energy conversion, machine dimensions).
- Location: `knowledge/concept_research/34-compact-spherical-tokamak-india/iter-02/sources/iaea-fuse-pranos-profile.md`

**3. Approved D1+ Analysis: Spherical Tokamak - HTS (21-spherical-tokamak-hts)**
- Contribution: Nearest-neighbor cross-reference. ST-specific cost structure analysis (center stack shielding, outboard-only blanket, pulsed vs. steady-state trade-off, REBCO supply chain, liquid Li blanket engineering). Provides the ST family template against which Pranos deviates. Tokamak Energy's development trajectory provides a maturity benchmark for assessing Pranos's distance from commercial readiness.
- Location: `analyses/21-spherical-tokamak-hts/analysis.md`

**4. Approved D1+ Analysis: HTS Compact Tokamak (01-hts-compact-tokamak)**
- Contribution: D-T supply chain characterization (tritium inventory, REBCO tape costs and supply), regulatory cost scenario (Stewart & Shirvan 2022, 2.2× building cost), FLiBe supply chain notes. Reused via 21-spherical-tokamak-hts cross-reference for D-T shared constraints.
- Location: Referenced in `analyses/21-spherical-tokamak-hts/analysis.md §Section 7`

**5. Humphry-Baker, S.A. and Smith, G.D.W. (2019) — Center stack shielding in compact spherical tokamak**
- Full citation: Humphry-Baker, S.A. and Smith, G.D.W. (2019) "Shielding materials in the compact spherical tokamak," *Philosophical Transactions of the Royal Society A*, 377(2141). doi:10.1098/rsta.2018.0233.
- Contribution: Quantitative analysis of center stack neutron shielding constraint (~30 cm radial depth for HTS protection). Applied here as a structural ST constraint that Pranos would inherit. Referenced via 21-spherical-tokamak-hts analysis.
- Location: Referenced in `analyses/21-spherical-tokamak-hts/analysis.md §Section 3`

**6. Araiinejad, L.S. and Shirvan, K. (2025) — D-T MCF TEA**
- Full citation: Araiinejad, L.S. and Shirvan, K. (2025) "Techno-economic analysis of deuterium-tritium magnetic confinement fusion power plants," *Applied Energy*, 401(Part B), 126567. doi:10.1016/j.apenergy.2025.126567.
- Contribution: LCOE sensitivity analysis for D-T MCF plants; capacity factor uncertainty ranges (75–90%); regulatory cost scenarios. Applied here as the only available proxy for missing Pranos LCOE parameters.
- Location: Referenced in `analyses/01-hts-compact-tokamak/analysis.md §Section 4`

**7. Brown, T.G. (2018) — Spherical tokamak, standard tokamak, stellarator cost comparison**
- Full citation: Brown, T.G. (2018) "Three confinement systems — spherical tokamak, standard tokamak, and stellarator: a comparison of key component cost elements," *IEEE Transactions on Plasma Science*, 46(6), pp. 2216–2230. doi:10.1109/TPS.2018.2831148.
- Contribution: Reference framework for ST capital cost decomposition by component category. Used here as the basis for the ST-specific capital cost structure and scale penalty analysis. Provides the only published cost comparison at a conceptual level applicable to a Pranos-type design.
- Location: Referenced in `analyses/21-spherical-tokamak-hts/analysis.md §Section 7`

**8. Hidalgo-Salaverri, J. et al. (2025) — Spherical tokamak TEA**
- Full citation: Hidalgo-Salaverri, J. et al. (2025) "Hybrid hydrogen-electricity production using spherical tokamaks: a cost-driver sensitivity study and techno-economic analysis," *Nuclear Fusion*, 65, 036027. doi:10.1088/1741-4326/adaa01.
- Contribution: Most directly applicable independent TEA for spherical tokamaks. Provides cost-driver sensitivities for the ST configuration family. Applied here as the reference framework for what a functioning ST TEA would require, highlighting how far Pranos's data is from the minimum inputs needed.
- Location: Referenced in `analyses/21-spherical-tokamak-hts/analysis.md §Section 1`

**9. arxiv-2603-11549 — Design and mechanical analysis of the PRAGYA tokamak vacuum vessel (preprint, March 2026)**
- Full citation: Gupta, R.; Koneru, R.B.; Sarkar, S.R.; Ansumali, S.; Kuley, A.; George, R.; Kaushal, S. (2026) "Design and mechanical analysis of the PRAGYA tokamak vacuum vessel," arXiv preprint arXiv:2603.11549, submitted 12 March 2026. [Not yet peer-reviewed.]
- Contribution: First published technical document for any Pranos hardware. Provides PRAGYA experimental device parameters (R₀ = 0.4 m, a > 0.18 m, B_T = 0.1 T, Ip ≤ 25 kA), confirms 3D FEM structural analysis complete under combined loading (self-weight, atmospheric pressure, thermal baking), and states device is "ready for subsequent plasma operations." Does not disclose magnet material, heating method, or any commercial-scale parameters.
- Location: `knowledge/concept_research/34-compact-spherical-tokamak-india/iter-02/sources/arxiv-2603-11549.md`

**10. Stewart, R. and Shirvan, K. (2022) — Fusion regulatory cost scenario**
- Full citation: Stewart, R. and Shirvan, K. (2022) [study demonstrating 2.2× building cost markup under fission-style regulation].
- Contribution: Upper-bound regulatory cost scenario; applied here as applicable to all D-T fusion concepts operating in jurisdictions without established fusion-specific regulatory pathways — which applies with particular force to Pranos in India.
- Location: Referenced in `analyses/01-hts-compact-tokamak/analysis.md §Section 2`
