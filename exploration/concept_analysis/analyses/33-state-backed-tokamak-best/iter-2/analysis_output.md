# D1+ Analysis: State-Backed Tokamak - BEST (Neo Fusion)

**Concept**: BEST (Burning Plasma Experimental Superconducting Tokamak) — D-T fuel
**Company**: Neo Fusion (Fusion Energy Technology Co., Ltd / 聚变新能); operated by ASIPP (Institute of Plasma Physics, Chinese Academy of Sciences)
**Device**: Mid-size tokamak under construction at Hefei, China; first plasma targeted late 2027
**Confinement Family**: MFE — Tokamak (conventional aspect ratio)

---

## Section 1: Availability of Data

**Rating: Moderate**

BEST occupies an unusual position in this analysis: the experimental device itself is exceptionally well-documented, but the commercial power plant descendants (CFEDR → PFPP) that are the actual TEA target are barely specified. The BEST Research Plan v1.1 (EUROfusion/ASIPP, November 2025) is a 200-page public document covering machine parameters, magnet design, heating and current drive systems, first-wall engineering, blanket test module program, plasma scenarios, and scientific objectives in detail rarely seen for a pre-construction fusion device. For characterizing BEST as an experimental device, data availability is rich. For characterizing China's commercial fusion program in the TEA framework, data availability is limited.

**Primary technical source:**
The BEST Research Plan v1.1 is the authoritative reference for all machine parameters:

> "BEST is positioned between EAST/JET and ITER in scale" with "R₀ = 3.6 m, a = 1.1 m, B₀ = 6.15 T" and is "predicted to generate more than 50 MW of fusion power with Q ≈ 1 — approximately three times the historical fusion power record achieved at JET"
> — best-research-plan-v1.1-summary.md, §Executive Summary

> "ASIPP is responsible for more than 70% of China's procurement packages for ITER, covering components such as superconducting conductors, magnet feeders, correction coils, power supply systems and diagnostics"
> — best-research-plan-v1.1-summary.md, §Section 1.1

This ASIPP supply chain context is significant: BEST is built by the same organization that manufactured most of China's ITER components, giving the project engineering credibility and a direct connection to validated procurement.

**Power conversion studies:**
Three published papers (2021, 2024, 2025) on sCO2 Brayton cycle selection for China's fusion lineage provide downstream energy conversion parameters:

> "Due to the large density and small volume of S–CO2, both compression power and the size of the key components can be greatly reduced. Therefore, S–CO2 cycle is characterized by high efficiency, compact structure and low cost."
> — cfetr-power-conversion-studies.md, §Cycle Layout and Results

These studies report 34.7% cycle efficiency for sCO2 vs. 26.4% for conventional Rankine, representing a clear technology preference for China's downstream commercial program.

**Company disclosure:**
The Neo Fusion company profile (neo-fusion-company-profile.md) is a single-page corporate document confirming company identity, ownership (CNPC + CAS majority state ownership, $214M funding), and a 20-year commercialization timeline. It contains no technical or economic detail. Neo Fusion is effectively a commercial vehicle for the state fusion program rather than an independent developer.

**Independent analyses:**
The most relevant independent cost study is Chen et al. (2015) on preliminary cost assessment for CFETR — the next step after BEST [referenced in 01-hts-compact-tokamak exemplar]. This predates BEST's current design but provides the only published Chinese fusion cost decomposition. ARIES studies and PROCESS code outputs for conventional-aspect-ratio tokamaks provide useful analogues for machine scaling.

**Phase 1a dossier completeness:**
After two research iterations, all 14 taxonomy columns are at high confidence except Energy Capture (medium, TBM-only experimental device with no power conversion) and Plasma State (medium, "burning" reflects the advanced scenario target, not initial operations). The dossier notes the BEST Research Plan v1.1 was "an exceptionally comprehensive source that resolved most questions in a single iteration" [dossier.md, §Remaining Gaps].

**Key data gaps limiting this analysis:**
1. CFEDR/PFPP commercial design point — plant size, fusion power, Q value, thermal efficiency not specified
2. Capital cost estimates for any Chinese commercial fusion reactor — not published in accessible sources
3. Blanket technology for commercial PFPP not selected (three TBM concepts competing)
4. Capacity factor target for PFPP and maintenance strategy unknown
5. Regulatory cost framework for Chinese commercial fusion plant uncharacterized

---

## Section 2: Challenges in Capturing System Function

BEST presents an unusual TEA modeling challenge: it is unambiguously an experimental device, not a power plant. Any LCOE estimate must extrapolate across two additional steps in China's roadmap (CFEDR → PFPP) that are poorly specified. Challenges are ranked by LCOE impact.

**1. Experimental device extrapolation: no direct commercial analog (Impact: Critical)**

BEST's mission is plasma science and technology validation, not electricity generation. It has no power conversion system, targets Q ≥ 1 (scientific breakeven, not commercial viability), and is licensed for only 110g of tritium — a fraction of what a commercial reactor would consume. The TEA-relevant question is: what does China's PFPP (Prototype Fusion Power Plant) look like, and how does BEST de-risk it? This question has no published answer. Unlike private-sector concepts where the developer is building toward a specific commercial product, China's fusion roadmap involves a sequence of government research devices (EAST → BEST → CFEDR → PFPP) with the commercial end-state unspecified. LCOE modeling requires parametric assumptions about the commercial descendant rather than stated design parameters.

**2. State cost accounting: Chinese construction economics differ from Western analogues (Impact: High)**

China's fusion program is majority state-owned and operates within Chinese construction cost norms that differ fundamentally from Western nuclear project economics. Chinese infrastructure construction typically achieves costs 2-4× lower than comparable Western projects due to lower labor rates, domestic equipment supply chains, and streamlined regulatory timelines. However, Chinese nuclear regulatory cost burdens, quality assurance requirements, and operational cost accounting are less transparent than in the US or EU. The Stewart & Shirvan (2022) 2.2× building cost factor for fission-style regulation (cited in 01-hts-compact-tokamak exemplar) may not apply in a Chinese regulatory context, but no alternative estimate exists. This creates a fundamental uncertainty in the capital cost basis.

**3. LTS magnet cost structure: larger machine, lower per-unit-length cost (Impact: High)**

BEST uses primarily ITER-heritage LTS conductors (Nb3Sn, NbTi) with YBCO only in the CS high-field sub-coils. This magnet approach is well-characterized in cost terms from ITER procurement but implies a larger machine than achievable with full-HTS. At B₀ = 6.15 T, a commercial plasma physics-equivalent device would need R₀ >> 6 m to achieve the burning plasma conditions that compact HTS designs achieve at R₀ ≈ 1.85–3.6 m. The cost of Nb3Sn conductor ($2–10/kA-m) is substantially lower than REBCO ($30–100/kA-m), but the total conductor and structural steel mass scales with machine volume, partially or fully offsetting this advantage. Whether the LTS route yields lower total capital cost per kWe than HTS routes is not settled — it depends on magnetic field strength, plasma performance extrapolation, and manufacturing scale assumptions.

**4. Multi-method H&CD system costs and recirculating power (Impact: Moderate)**

BEST operates four concurrent heating systems (ECRH 15 MW + ICRH 10 MW + LHCD 10 MW + NBI 12 MW). A commercial PFPP may simplify or concentrate this portfolio. The capital cost of a 50 MW, four-method H&CD system is substantially higher than a single-technology approach. Wall-plug efficiency varies significantly: NBI achieves ~60–70%, ICRH ~70–80%, ECRH/LHW ~50–55%. For a commercial reactor, auxiliary heating is a recirculating power cost that directly affects Q_engineering. Without knowing which H&CD methods PFPP retains and at what power level, the recirculating power fraction is unconstrained. BEST's LHCD choice (4.6 GHz, which drives efficient current at lower electron temperatures) may not transfer to a burning plasma where electron temperature is much higher and LHCD penetration depth is limited. CFETR Phase I physics simulations quantify this risk: the EC+LH-only scenario (NBI removed) achieves Q = 1.2 vs. Q = 2.0 for NB+EC at identical fusion power, because NBI provides plasma rotation to suppress turbulence transport and direct ion heating that EC/LH cannot replicate [osti-pages-servlets-purl-1465662.md §Section 3.2 — The flattop phase]. This confirms that LHCD alone is insufficient to reach commercially relevant Q values; NBI cannot be eliminated from the H&CD portfolio without significant Q penalty.

**5. Blanket technology selection drives blanket cost, efficiency, and TBR (Impact: Moderate)**

Three TBM concepts are under test at BEST: COOL (CO2-cooled LiPb), WCCB (water-cooled ceramic breeder), and European alternatives (WCLL, HCPB, WLCB). These represent fundamentally different blanket engineering approaches with different tritium breeding characteristics, coolant costs, structural material requirements, and thermal efficiency outcomes. The commercial PFPP blanket technology is undecided. This is not a data gap that additional literature search can resolve — it is a genuine technology decision pending experimental results from the TBM program. Until this choice is made, blanket cost, tritium breeding margin, and power conversion cycle selection are all unanchored [best-research-plan-v1.1-summary.md, §Section 3.2.13].

**Key testable hypotheses for PFPP cost modeling:**
- **H1**: If the Chinese 2× construction cost discount holds for fusion, PFPP LCOE drops from ~140 $/MWh to ~80 $/MWh (capital cost halved at ~70% capital share of LCOE).
- **H2**: COOL/sCO2 route achieves ~9% lower LCOE than WCCB/Rankine, due to 34.7% vs. 26.4% thermal efficiency at otherwise equal capital cost.
- **H3**: If PFPP inherits CFETR's pulsed regime (duty cycle 0.3–0.5) rather than quasi-steady-state operation, LCOE increases 1.5–3× relative to the quasi-steady-state 75–90% CF assumption.

**6. Power conversion cycle: sCO2 preferred but not committed (Impact: Moderate)**

Published CFETR/BEST lineage studies favor sCO2 Brayton at 34.7% efficiency [cfetr-power-conversion-studies.md, §Conclusions]. This is higher than conventional steam Rankine (26.4%) and substantially higher than He Brayton + ORC (23.7%). However, BEST itself generates no electricity and the CFEDR/PFPP formal design point has not adopted sCO2 as a committed baseline. The sCO2 advantage is meaningful for LCOE: ~9 percentage points of thermal efficiency correspond to significant reductions in plant footprint and capital cost per net MWe.

**O&M cost placeholder:**
No O&M cost breakdown for China's PFPP has been published. BEST Research Plan v1.1 focuses on construction and plasma physics; operating costs for the experimental device (staffing, maintenance, tritium handling) are not discussed. For the commercial analog, O&M costs should be estimated using ARIES/PROCESS conventions (typically 3–5% of overnight capital cost per year) as a placeholder, with high uncertainty. Remote handling maintenance cost is a particularly uncertain element given the full-tungsten first wall and lack of a published PFPP maintenance scheme.

---

## Section 3: Maturity of Key Subsystems and Components

Ordered from least mature (highest risk to commercial LCOE) to most mature.

---

**Tritium Breeding Blanket for Commercial Reactor — TRL 2–4**

- **Demonstrated**: BEST hosts three TBM test ports (0.6 × 1 m² each) for prototype blanket testing under fusion neutron conditions. ITER's TBM program provides direct methodological precedent. COOL TBM (CO2-cooled LiPb) couples naturally to sCO2 power conversion. WCCB (water-cooled ceramic breeder with Li4SiO4/Li2TiO3 pebble beds and Be12Ti multiplier) represents the HCPB heritage path used in EU-DEMO blanket concepts.
- **On paper only**: Full-coverage, self-sufficient tritium breeding blanket achieving TBR > 1.1 for a commercial fusion reactor. BEST's TBM program tests ~0.15 MW/m² NWL — far below CFEDR requirements (>1 MW/m² for commercial relevance).
- **Missing at scale**: 14 MeV neutron testing at full CFEDR/PFPP fluences (target >1 dpa/yr). Industrial-scale Li ceramic pebble fabrication. Tritium extraction from LiPb or solid breeder at kg/day plant-scale rates. RAFM steel structural qualification under combined fusion conditions (neutron + heat + tritium). The BEST Research Plan explicitly acknowledges: "While the neutron fluence in BEST is limited for a full demonstration of tritium breeding, the TBM programme will support intermediate steps" [best-research-plan-v1.1-summary.md, §Section 1.4].

---

**Tritium Fuel Cycle (External Supply → Self-Sufficiency Transition) — TRL 3–5**

- **Demonstrated**: BEST cryogenic fuel cycle infrastructure in design phase. Direct Internal Recycling (DIR) technology demonstrated at sub-gram scale. JET and TFTR operated D-T with gram-scale inventories, providing operational precedents. ASIPP has tritium handling infrastructure from EAST and ITER manufacturing.
- **On paper only**: Self-sufficient closed tritium breeding-extraction-processing cycle for a commercial plant. BEST operates at 110g licensed inventory — a tiny fraction of commercial plant requirements. The BEST Research Plan notes: "Global recovery time and efficiency will be derived from the measurement results" [best-research-plan-v1.1-summary.md, §Section 3.3.1].
- **Missing at scale**: kg/day tritium processing plant for commercial PFPP. Demonstrated TBR > 1 under operational conditions with realistic blanket penetrations. Tritium accountability in primary blanket circuits (PbLi or ceramic).

---

**Plasma Scenarios for Commercial Operation (Q >> 1) — TRL 4–6**

- **Demonstrated**: EAST (ASIPP predecessor team, same facility location) achieved >1000-second plasma durations in H/D at low power. ASIPP has extensive long-pulse tokamak operations experience. JET D-T campaigns (2021–2023) validated D-T burning physics at modest Q values and provide direct scenario precedents.
- **On paper only**: Q ≥ 1 burning plasma at BEST parameters (target ~2030). Q~5 advanced scenario (target 2032–2035) — at these conditions, alpha self-heating becomes significant and plasma control becomes more challenging. Simultaneous Q~5 and pulse length >1000s operation, which may compete for plasma current profiles.
- **Missing at scale**: Full-W first wall + divertor under D-T burning plasma at Q~5 — no prior experiment in this combination. AI/ML plasma control for disruption mitigation under burning plasma conditions with W impurities. The BEST Research Plan flags: "The high concentration of high-Z impurities presents particular challenges...tungsten impurity control methods not yet fully demonstrated" [best-research-plan-v1.1-summary.md, §Section 2.2.2].

---

**Test Blanket Module Program (COOL/WCCB/EU) — TRL 4–6**

- **Demonstrated**: TBM engineering design under way. Three concepts progressing through design reviews aligned with BEST construction schedule. RAFM steel, Li ceramics, PbLi, and SiCf/SiC components under laboratory development at ASIPP and EU partners. ITER TBM experience provides direct methodological transfer.
- **On paper only**: Integrated TBM operation in BEST D-T neutron environment. Materials traceability and certification pipeline for TBM structural components.
- **Missing at scale**: Full manufacturing qualification of TBM materials (RAFM steel at nuclear grade, Li ceramic pebbles in bulk). Post-irradiation examination database under fusion neutrons. Commercial-scale blanket manufacturing derived from TBM outcomes.

---

**Multi-Method H&CD System (ECRH + ICRH + LHCD + NBI) — TRL 6–8**

- **Demonstrated**: All four H&CD technologies are individually mature: ECRH at 170 GHz is ITER-baseline; ICRH systems operated on JET, EAST; LHCD at 4.6 GHz demonstrated on EAST and Tore Supra; NBI at 120 kV positive-ion (ITER beam energy). ASIPP has operated all four on EAST, giving the BEST team direct integration experience. BEST's 50 MW total (15+10+10+12 MW) is a step up from EAST but within established ranges.
- **On paper only**: CW, high-reliability operation of all four systems in D-T neutron and gamma environment. Portfolio optimization for Q maximization in long-pulse operation. LHCD applicability in high-temperature burning plasma (lower-hybrid wave accessibility is electron-temperature limited, potentially constraining its use in high-Q scenarios).
- **Missing at scale**: Long-pulse CW gyrotrons at 15 MW ECRH scale with high reliability. Radiation-hardened launcher/antenna designs for D-T operations (activated vacuum vessel environment during maintenance). Demonstrated synergy of all four systems in simultaneously long-pulse AND high-Q operation.

---

**Hybrid LTS+HTS Magnet System (Nb3Sn/NbTi TF/PF + YBCO CS) — TRL 7–8**

- **Demonstrated**: Nb3Sn cable-in-conduit TF coils are ITER-qualified — the ITER TF coils are the same technology class and are now manufactured and being assembled. NbTi PF coils are the most mature superconductor technology in fusion. YBCO (REBCO class) CS sub-coils achieving 18.8T peak field: ASIPP has HTS R&D and ITER correction coil fabrication experience. Total magnet mass ~2000t — comparable in scale to ITER (~10,000t total cold mass, but TF alone is ~6,000t).
- **On paper only**: Complete 16 TF + 7 PF + 8 correction coil + ferromagnetic insert system at BEST scale. YBCO CS sub-coil performance under 18.8T cyclic thermal and mechanical loads over device lifetime.
- **Missing at scale**: Long-term irradiation behavior of the YBCO CS sub-coils under D-T neutron flux at BEST neutron wall loading (~0.04 dpa over device lifetime — modest, but still requires characterization). Integration of ferromagnetic inserts to reduce TF ripple with full magnet assembly.

---

**First Wall and Divertor (Full-Tungsten) — TRL 6–8**

- **Demonstrated**: Full-tungsten first wall is a BEST design priority and is actively pioneered at WEST (France), JET (all-W divertor from 2011), EAST (W divertor). 240 first-wall modules (W-coated CuCrZr tiles, water-cooled at 4 MPa/70°C). 48 divertor cassettes rated to 10–15 MW/m². ASIPP has tungsten armor manufacturing experience from ITER divertor dome components.

> "A unique demonstration of D-T operation under full-tungsten wall environment, delivering comprehensive information about plasma-wall interactions, plasma impurity control, and material migration under fusion-relevant conditions"
> — best-research-plan-v1.1-summary.md, §Section 1.2

- **On paper only**: Full-W first wall + divertor integration in D-T burning plasma at Q~1–5. Heat flux management at BEST's 10–15 MW/m² divertor rating during high-power burning plasma pulses. W impurity control strategy validated in burning plasma (EAST experience at lower power provides partial precedent).
- **Missing at scale**: ELM (Edge-Localized Mode) mitigation in full-W D-T burning plasma — high ELM loads risk W armor melting, and "ELM mitigation strategies are essential and will be tested" [best-research-plan-v1.1-summary.md, §Section 6]. Remote replacement system for W divertor cassettes in activated D-T environment.

---

**Balance of Plant (sCO2 Power Conversion — Downstream Commercial) — TRL 7–9 (BOP) / TRL 3–5 (Fusion Integration)**

- **Demonstrated**: sCO2 Brayton cycles at 34.7% efficiency are approaching commercial maturity in concentrated solar power applications. Multiple published CFETR-lineage studies confirm sCO2 as the preferred power conversion technology: "S–CO2 Brayton cycle is superior" in combined efficiency, compactness, and cost among the three cycles evaluated [cfetr-power-conversion-studies.md, §Conclusions]. BEST's COOL TBM directly couples to sCO2 (CO2-cooled LiPb). This creates a coherent technology thread from TBM to downstream power conversion.
- **On paper only**: sCO2 Brayton integration with fusion-specific heat sources. Tritium permeation barriers in sCO2-facing heat exchangers (CO2 is an oxidizing medium, requiring different permeation barrier strategy than inert He coolant).
- **Missing at scale**: Complete sCO2 power conversion system designed for fusion pulsed heat source characteristics. Formal PFPP commitment to sCO2 (currently preferred but not committed). Tritium accountability in CO2 coolant circuit (tritium permeation from LiPb through steel into CO2 is a known concern in EU-DEMO WCLL studies, requiring permeation barriers or tritium extraction from CO2).

---

## Section 4: Key Materials and Supply Chain Considerations

**Nb3Sn Superconductor (TF Coils) — ITER-Qualified Supply Chain, China Domestically Capable**

BEST's TF coils use ITER-heritage Nb3Sn cable-in-conduit conductor. This is the most mature high-performance superconductor technology in fusion. ASIPP manufactures >70% of China's ITER procurement packages including superconducting conductors, meaning the supply chain is domestically established. Global Nb3Sn conductor cost ($2–10/kA-m depending on strand specifications) is 5–10× lower than REBCO HTS tape, providing a cost advantage per unit length — though the lower achievable field (B₀ = 6.15 T at plasma center vs. 12–20 T for HTS designs) requires a larger machine, partially offsetting this advantage. At commercial PFPP scale (R₀ likely 5–8 m for adequate fusion power with this field), total conductor demand will be in the multi-thousand-kilometer range, within the capacity of established Nb3Sn producers (Europa Superconductors, Furukawa, ASIPP-affiliated manufacturers). No supply chain bottleneck is anticipated for Nb3Sn.

**YBCO HTS (CS Sub-Coils Only) — Limited Demand, Not a Bottleneck**

BEST uses YBCO only in the CS high-field sub-coils achieving 18.8T peak field. Unlike full-HTS designs (CFS SPARC at 20T, Tokamak Energy ST-E1 at 5.25T using REBCO for all coils), BEST's HTS demand is limited and site-specific. Total YBCO tape length for BEST's CS sub-coils is substantially less than the 5,000+ km needed for an ARC-class full-HTS machine. This is not a supply chain bottleneck — it is a manageable procurement from established REBCO producers. For commercial PFPP, if China elects to maintain the LTS-primary approach, YBCO demand remains modest.

**Tungsten (First Wall, Divertor) — Domestically Advantaged, Manufacturing Challenge**

China produces >80% of global tungsten, eliminating any supply scarcity risk for W armor material. ASIPP has direct W fabrication experience through ITER divertor dome component manufacturing. The engineering challenge is manufacturing quality and reliability (large-area W tile fabrication, consistent bonding to CuCrZr heat sinks, thermal fatigue resistance under fusion pulsed loads) rather than material availability. Remote handling and replacement of activated W modules adds operational complexity and cost.

**Tritium (External Supply, Long-Term Self-Sufficiency Challenge)**

BEST's licensed 110g inventory is modest relative to any commercial plant requirement (~1 kg per reactor startup). China is not a major CANDU heavy water reactor operator — the primary global tritium source. China's tritium access relies on:
(a) Small amounts produced in research reactors (CNIC, CIAE fission programs)
(b) International procurement
(c) Future self-breeding from BEST's TBM program (technology validation, not production)
The global tritium inventory (~25–30 kg) is shared across all D-T programs. As CANDU reactors retire, this constraint tightens for all concepts. China's commercial PFPP would require demonstrated TBR > 1.1 from the TBM program before committing to self-sufficient breeding — a dependency that could delay commercial operation if TBM results are disappointing [best-research-plan-v1.1-summary.md, §Section 1.4].

**TBM Materials (RAFM Steel, Li Ceramics, PbLi, SiCf/SiC) — Technology Qualification Gap**

The three TBM programs require advanced materials not currently produced at nuclear-qualified commercial scale:
- **RAFM steel** (e.g., F82H, EUROFER 97): ~1–10 tonne per TBM, under development; must meet ASME/RCC-MRx nuclear code or Chinese equivalent; not yet commercially available at these grades from Chinese producers
- **Li ceramics** (Li4SiO4, Li2TiO3 pebble beds): fabrication scalability to plant-level quantities (tonnes per blanket segment) not demonstrated; pebble crush strength and sintering consistency require production-scale development
- **SiCf/SiC composites**: for flow channel inserts in COOL TBM; manufacturing maturity is TRL 3–4 globally; very limited producers (SAFRAN, Ceramic/Coorstek in West; ASIPP/NPU in China at small scale)
- **PbLi eutectic**: commercially available but fusion-qualified supply chain not established; isotopic composition (natural Li) may need enrichment for commercial TBR

The BEST Research Plan acknowledges these as active development requirements: "structural and functional materials used in TBMs shall be authorized and qualified with an adequate and reliable supporting database" and manufacturing technologies "shall be developed and validated under non-nuclear environment before use" [best-research-plan-v1.1-summary.md, §Section 3.2.13].

**Helium (Magnet Cooling) — Shared LTS Vulnerability**

Nb3Sn TF coils operate at ~4.5 K requiring large-scale liquid helium refrigeration — the same requirement as ITER's ~40 kW of 4.5K cooling power. China remains partially import-dependent for helium despite active development of domestic extraction from natural gas fields (Sichuan province). Global helium supply constraints (primary sources: US, Qatar, Russia/Algeria) represent a shared vulnerability for any LTS fusion device. At BEST scale, helium refrigeration demand is ITER-comparable in cooling capacity; the associated capital and operating cost is well-understood from ITER procurement.

---

## Section 5: LCOE-Relevant Parameters

### Available Parameters

**BEST Machine Parameters (Experimental Device)**

| Parameter | Value/Range | Source | Confidence | Notes |
|-----------|-------------|--------|------------|-------|
| Major radius | 3.6 m | best-research-plan-v1.1-summary.md §Section 1.3 | high | Confirmed design value |
| Minor radius | 1.1 m | best-research-plan-v1.1-summary.md §Section 1.3 | high | Aspect ratio A = 3.27 |
| Toroidal field | 6.15 T | best-research-plan-v1.1-summary.md §Section 1.3 | high | On-axis at plasma center |
| Plasma current (max) | 7 MA | best-research-plan-v1.1-summary.md §Section 1.3 | high | Maximum rated current |
| Elongation / triangularity | κ = 1.88 / δ = 0.49 | best-research-plan-v1.1-summary.md §Section 1.3 | high | Plasma shaping parameters |
| Plasma volume | ~142 m³ | best-research-plan-v1.1-summary.md §Section 1.3 | high | Intermediate between JET (~90 m³) and ITER (~840 m³) |
| Auxiliary heating power | 50 MW total | best-research-plan-v1.1-summary.md §Section 1.3 | high | ECRH 15MW + ICRH 10MW + LHCD 10MW + NBI 12MW; upgrade to ~71 MW planned |
| Target fusion power (Q≈1) | >50 MW | best-research-plan-v1.1-summary.md §Executive Summary | high | Primary mission objective; ~3× JET D-T record |
| Target Q value (baseline) | ≥ 1 | best-research-plan-v1.1-summary.md §Section 2.4 | high | Scientific breakeven; target by ~2030 |
| Target Q value (advanced) | ~5 | best-research-plan-v1.1-summary.md §Section 2.4 | medium | Burning plasma studies 2032–2035; alpha self-heating significant |
| Fusion power at Q~5 | [inferred] ~200–250 MW | [inferred: Q=5 × P_aux ≈ 40–50 MW] | low | Advanced burning plasma scenario; auxiliary power not specified for this mode |
| Long-pulse target | >1000 s | best-research-plan-v1.1-summary.md §Section 1.3 | high | Timeline T2 objective |
| Neutron wall loading (baseline) | 0.05–0.1 MW/m² | best-research-plan-v1.1-summary.md §Section 1.3 | high | Long-pulse operations at 10–20 MW fusion power |
| Neutron wall loading (TBM operational) | 0.15 MW/m² at 40 MW fusion power | best-research-plan-v1.1-summary.md §Section 3.2.12 | high | TBM test conditions |
| Neutron wall loading (high-perf) | >0.4 MW/m² | best-research-plan-v1.1-summary.md §Section 1.3 | high | Advanced scenarios, >100 MW fusion power |
| First wall heat flux | 0.3 MW/m² at 40 MW fusion power | best-research-plan-v1.1-summary.md §Section 1.3 | high | Nominal design heat flux |
| Divertor heat flux rating | 10–15 MW/m² | best-research-plan-v1.1-summary.md §Section 1.3 | high | 48 cassette assemblies |
| CS peak field | 18.8 T (YBCO sub-coils) | best-research-plan-v1.1-summary.md §Section 1.3 | high | Hybrid Nb3Sn+YBCO CS design |
| Total magnet mass | ~2000 t | best-research-plan-v1.1-summary.md §Section 1.3 | high | All coils combined |
| Tritium inventory (licensed) | 110 g | best-research-plan-v1.1-summary.md §Section 1.3 | high | Starting inventory; well below commercial reactor requirements |
| First plasma target | Late 2027 | best-research-plan-v1.1-summary.md §Section 1.3 | high | Under construction at Hefei |
| Q ≥ 1 target date | ~2030 | dossier.md §Summary | high | Primary scientific milestone |
| Cumulative neutron fluence (device lifetime) | >10²⁶ neutrons | best-research-plan-v1.1-summary.md §Section 1.3 | medium | Corresponds to ~0.04 dpa lifetime in BEST first wall |
| Neo Fusion funding | $214M | neo-fusion-company-profile.md | high | State-backed; CNPC + CAS majority ownership |

**CFETR Phase I Parameters (Intermediate Step — Published)**

| Parameter | Value/Range | Source | Confidence | Notes |
|-----------|-------------|--------|------------|-------|
| Major radius (CFETR Phase I) | 5.7 m | osti-pages-servlets-purl-1465662.md §Section 2.2 | medium | First step beyond BEST; aspect ratio A = 3.56 |
| Minor radius (CFETR Phase I) | 1.6 m | osti-pages-servlets-purl-1465662.md §Section 2.2 | medium | |
| Toroidal field (CFETR Phase I) | 5 T | osti-pages-servlets-purl-1465662.md §Section 2.2 | medium | On-axis at plasma center |
| Plasma current (CFETR Phase I) | 10 MA | osti-pages-servlets-purl-1465662.md §Section 2.2 | medium | |
| Target fusion power (CFETR Phase I) | 200 MW | osti-pages-servlets-purl-1465662.md §Section 2.2 | medium | Phase I design objective |
| Duty cycle (CFETR Phase I) | 0.3–0.5 | osti-pages-servlets-purl-1465662.md §Introduction | medium | Pulsed operation; key constraint for PFPP CF assumption |
| Q — NB+EC scenario | ~2.0 | osti-pages-servlets-purl-1465662.md §Section 3.2 | medium | At 200 MW; NBI required for this Q |
| Q — EC+LH only (no NBI) | ~1.2 | osti-pages-servlets-purl-1465662.md §Section 3.2 | medium | Q degrades 40% without NBI — loss of plasma rotation and direct ion heating |

**Power Conversion Parameters (CFETR/PFPP Downstream Lineage)**

| Parameter | Value/Range | Source | Confidence | Notes |
|-----------|-------------|--------|------------|-------|
| Preferred power conversion cycle | sCO2 Brayton | cfetr-power-conversion-studies.md §Conclusions | medium | Preferred in published studies; not formally committed for PFPP |
| sCO2 Brayton thermal efficiency | 34.7% | cfetr-power-conversion-studies.md §Conclusions | medium | Compared to 26.4% Rankine, 23.7% He Brayton+ORC |
| sCO2 efficiency (literature range) | 42.8–53.7% | cfetr-power-conversion-studies.md §Introduction (Linares et al., Ma et al.) | low | Advanced configurations; optimistic upper bound |
| Net electrical output (commercial PFPP) | [estimated] 500–1000 MWe | [analogue: CFETR, DEMO-class devices; Chinese program targets 1 GW class] | low | Consistent with UKAEA sweet spot 500 MW–1.2 GW net electric [scientific-publications-wp-content-uploads-extrapolating.md §Conclusion] |
| Gross-to-net electric ratio (plant-size dependent) | 17% at 100 MWe → 42% at 1.2 GWe | scientific-publications-wp-content-uploads-extrapolating.md §Results | low | From UKAEA/PROCESS scan; recirculating power dominates at small plant sizes; first-of-kind PFPP at 500 MWe likely 25–35% gross-to-net |
| Overnight capital cost (PFPP) | [estimated] $5–15B | [analogue: ITER ~$25B at 500 MWth, scaled to commercial plant; Chinese construction discount ~2–4×] | low | Wide uncertainty reflecting complete absence of published estimates |
| Q value (commercial PFPP) | [estimated] 5–15 | [analogue: ARIES-AT Q≈5–8; EU-DEMO Q≈10; assuming burning plasma design] | low | Commercial PFPP must substantially exceed BEST's Q≤5 target |
| Capacity factor — Scenario A (quasi-steady-state PFPP) | [analogue] 75–90% | Araiinejad & Shirvan (2025) D-T MCF analogue; 21-spherical-tokamak-hts analysis §S5 | low | Assumption requires explicit justification — applies only if commercial PFPP is designed for quasi-steady-state operation distinct from CFETR Phase I |
| Capacity factor — Scenario B (pulsed PFPP, CFETR-like) | 30–50% duty cycle | osti-pages-servlets-purl-1465662.md §Introduction | medium | CFETR Phase I physics simulation target: "steady-state operation with a duty cycle of 0.3~0.5"; if PFPP inherits this regime, LCOE increases 1.5–3× vs Scenario A |
| LCOE (PFPP, very rough order of magnitude) | [estimated] 50–300 $/MWh | [estimated: assuming capital dominance at ~70%, 8% discount rate, 75–90% CF, 34.7% thermal efficiency; wide range reflects PFPP design unknown] | very low | Parametric estimate only; not an anchored LCOE calculation |

---

### Missing Parameters

| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Commercial PFPP design point (R, B, Q, P_fusion) | not-yet-sourced | blocking | CFETR Phase I is published (see Available Parameters); commercial PFPP (Phase II/DEMO-class) not yet specified — must be assumed by analogy to ARIES-AT / EU-DEMO |
| Capital cost of BEST or PFPP | proprietary / not-yet-sourced | blocking | No published cost data; Chen et al. (2015) covers CFETR only and is pre-BEST design; Chinese program costs not publicly reported |
| Blanket technology selection for PFPP | not-yet-decided | blocking | Three TBM concepts competing; selection depends on BEST experimental results (2030s) |
| Thermal efficiency and power cycle commitment for PFPP | not-yet-sourced | blocking | sCO2 preferred in literature but no formal PFPP commitment |
| Capacity factor / availability target for PFPP | truly-unknown | blocking | No published estimate; quasi-steady long-pulse operation implies different outage patterns than steady-state designs |
| H&CD portfolio for commercial PFPP | truly-unknown | important | Commercial reactor may retain subset of BEST's four-method portfolio; selection not specified |
| LHCD applicability at burning plasma temperatures | derivable | important | Lower-hybrid wave penetration is electron-temperature limited; may not work effectively in high-Q burning plasma; affects recirculating power assumption |
| Helium refrigeration capital and operating cost at PFPP scale | derivable | important | ITER-based scaling available; Nb3Sn at ~4.5K requires large refrigeration plant; cost well-characterized from ITER but PFPP-specific scaling not published |
| Tritium breeding TBR from BEST TBM program | not-yet-known (in progress) | important | TBM results from BEST (2030s) are the primary dataset; TBR must be demonstrated > 1.1 for commercial viability |
| Chinese nuclear regulatory cost framework for fusion | truly-unknown | important | Stewart & Shirvan 2.2× factor (US-centric) may not apply; China has faster regulatory track record for research devices but commercial fusion regulation not characterized |
| Component replacement schedule (first wall, divertor) for PFPP | truly-unknown | important | W first wall lifetime under commercial NWL (>1 MW/m²) not characterized; BEST operates at much lower NWL |
| LHCD efficiency in D-T plasma at BEST temperatures | not-yet-sourced | nice-to-have | LH wave accessibility limits at high electron temperature may constrain LHCD contribution to Q; affects recirculating power |

---

## Section 6: Data Gap Inventory

| # | Gap Description | Section | Gap Type | Criticality | Source Recommendation |
|---|-----------------|---------|----------|-------------|----------------------|
| 1 | Commercial PFPP design point (Phase II / DEMO-class) unspecified; CFETR Phase I is published (R₀ = 5.7 m, B₀ = 5 T, Ip = 10 MA, 200 MW fusion, duty cycle 0.3–0.5) | S1, S2, S5 | not-yet-sourced (PFPP) | blocking | CFETR Phase I confirmed in osti-pages-servlets-purl-1465662.md §Section 2.2; commercial PFPP remains unanchored — use CFETR Phase I + ARIES-AT as bounding analogues; PROCESS scan can extend to PFPP-class parameters |
| 2 | Capital cost for BEST or any Chinese commercial fusion device not published | S1, S5 | proprietary / not-yet-sourced | blocking | Chen et al. (2015) CFETR study is only public reference; apply Chinese construction cost discount (2–4×) to ARIES/PROCESS baseline as bounding estimate |
| 3 | Blanket technology for PFPP undecided (three TBM concepts competing) | S2, S3, S5 | not-yet-decided | blocking | Await BEST TBM program experimental results; use parametric sensitivity across COOL/WCCB/WCLL assumptions |
| 4 | Formal power conversion cycle commitment for PFPP not made | S2, S3, S5 | not-yet-sourced | blocking | Use sCO2 Brayton at 34.7% efficiency as central case based on published CFETR studies; flag as unconfirmed |
| 5 | Capacity factor target for PFPP absent | S2, S5 | truly-unknown | blocking | Apply Araiinejad & Shirvan (2025) 75–90% range as analogue; BEST's quasi-steady long-pulse operation suggests no fundamental availability penalty vs. conventional D-T tokamak |
| 6 | Overnight capital cost estimate for PFPP | S2, S5 | truly-unknown | blocking | Apply ARIES-AT or PROCESS-derived cost for similar plasma parameters; apply 2–4× Chinese construction discount; treat as very-low-confidence estimate |
| 7 | LHCD applicability in burning plasma scenarios — CFETR simulations show Q drops from 2.0 (NB+EC) to 1.2 (EC+LH only, no NBI) | S2, S3, S5 | derivable | important | osti-pages-servlets-purl-1465662.md §Section 3.2 quantifies the Q degradation; NBI removal reduces fusion gain 40% due to loss of plasma rotation and direct ion heating; LH drives ~2× more current than EC for same power but cannot substitute for NBI heating |
| 8 | Tritium breeding TBR > 1 demonstration from TBM program | S3, S4 | not-yet-known | important | Follow BEST TBM publications from ~2030 onward; in absence, apply ITER TBM simulated TBR values as prior |
| 9 | Chinese nuclear regulatory cost framework for commercial fusion | S2, S5 | truly-unknown | important | Compare Chinese regulatory approach to NRC baseline; consult China's NEA fusion regulatory framework documents if available |
| 10 | Helium refrigeration capital/operating cost at PFPP scale | S3, S5 | derivable | important | Scale from ITER cryogenic plant costs (~$1B for 40 kW at 4.5K); apply to PFPP cooling load estimate |
| 11 | H&CD portfolio selection and recirculating power for commercial PFPP | S2, S5 | not-yet-sourced | important | Apply ARIES-AT or DEMO H&CD efficiency assumptions; investigate whether LHCD is retained at commercial scale |
| 12 | Component replacement schedule (W first wall, divertor) under commercial NWL | S3, S5 | truly-unknown | important | ITER/DEMO design studies assume ~2-year first wall replacement intervals at commercial NWL; apply as analogue |
| 13 | SiCf/SiC composite manufacturing scalability for COOL TBM flow channel inserts | S4 | truly-unknown | nice-to-have | Monitor ASIPP SiC program; alternative: COOL TBM could eliminate SiC if Al2O3-coated steel inserts are validated |
| 14 | Tritium permeation through CO2-facing heat exchangers in COOL TBM / sCO2 circuit | S3, S4 | not-yet-sourced | nice-to-have | EU-DEMO WCLL literature on T permeation through steam generators provides partial analogy; sCO2-specific permeation data needed |
| 15 | Q_engineering (net electrical efficiency accounting for recirculating power) for PFPP | S5 | derivable | important | Derivable once H&CD portfolio and thermal efficiency are fixed; formula: Q_eng = (P_fusion × η_blanket × η_thermal - P_recirc) / P_fusion; currently unconstrained |

---

## Section 7: Cross-Concept Notes

The only approved prior analysis available for cross-referencing is the Spherical Tokamak - HTS (Tokamak Energy, `21-spherical-tokamak-hts`). While both concepts are MFE tokamaks targeting D-T burning plasma, BEST and the Tokamak Energy ST-E1 differ substantially in geometry, magnet technology, scale, and strategic positioning. The following elements are adopted or adapted from the ST-E1 analysis.

**Reused assumptions:**

- **D-T tritium supply constraints**: Global tritium inventory (~25–30 kg, primarily CANDU-sourced), startup inventory (~1 kg at >$35,000/g), 5.5%/year decay, and the self-sufficiency sequencing constraint are identical for all D-T concepts [21-spherical-tokamak-hts analysis §Section 4]. China's PFPP faces the same constraint, with the additional complexity that China has limited access to CANDU tritium.
- **Regulatory cost uncertainty**: The Stewart & Shirvan (2022) 2.2× building cost factor for fission-style regulation applies conceptually to Chinese commercial fusion, but the actual Chinese regulatory cost burden is unknown. The ST-E1 analysis uses this as an upper-bound scenario; the same approach is adopted here with the caveat that China's faster regulatory track record for research devices may translate to lower commercial costs [21-spherical-tokamak-hts analysis §Section 2].
- **Capacity factor sensitivity range**: Araiinejad & Shirvan (2025) 75–90% range for D-T MCF plants is applied as the analogue capacity factor bracket, given no Chinese program estimate exists [21-spherical-tokamak-hts analysis §Section 5].
- **REBCO tape pricing context**: While BEST is primarily LTS (not full-HTS), the global REBCO market pricing ($30–100/kA-m, target $10/kA-m) established in the ST-E1 analysis [§Section 4] provides context for BEST's limited YBCO CS sub-coil procurement — at this scale, YBCO demand is not a bottleneck.

**Key divergences from ST-E1 analysis:**

- **Magnet technology**: ST-E1 uses REBCO HTS for all coils (5.25 T on-axis, full-HTS architecture). BEST uses ITER-heritage Nb3Sn/NbTi for TF and most PF coils, with YBCO only in CS high-field sub-coils (6.15 T on-axis, hybrid LTS+HTS). Nb3Sn supply chain is better characterized and cheaper per unit length; BEST faces no magnet supply chain bottleneck. The cost trade-off (lower cost per km vs. larger machine needed) is the central LCOE question for LTS-based commercial tokamaks.
- **Strategic positioning**: ST-E1 is positioned as a commercial pilot plant with direct revenue target. BEST is explicitly experimental, designed to de-risk CFEDR/PFPP rather than generate electricity. This fundamentally changes the TEA framing: any LCOE estimate for the BEST lineage must add an additional extrapolation step not required for private-sector commercial-intent designs.
- **Organizational context**: Tokamak Energy is a private company with investor accountability. Neo Fusion is a state vehicle with CNPC and CAS majority ownership. Cost transparency, cost accounting norms, and schedule accountability are fundamentally different. Chinese construction economics historically achieve 2–4× lower construction costs than comparable Western projects, which if it holds for fusion could represent a meaningful LCOE advantage — but this requires dedicated analysis with Chinese cost benchmarks, not direct application of ARIES/PROCESS estimates.
- **Scale and heating**: ST-E1 targets 450–750 MWe commercial output with ECRH-only flat-top. BEST targets Q~5 experimental plasma science. The commercial PFPP descendant would need to achieve substantially higher fusion power (likely 1–3 GW fusion power for commercial viability) at a machine scale well beyond BEST, requiring extrapolation from BEST parameters in ways not needed for ST-E1.
- **Data availability**: ST-E1 is limited by corporate non-disclosure (machine parameters published but Q, fusion power, cost unpublished). BEST is limited differently — the experimental device is comprehensively documented, but the commercial descendants are genuinely unspecified. The gap type is different even if the gap impact on LCOE modeling is similar.

**Positioning against structurally appropriate nearest neighbors:**

While 21-spherical-tokamak-hts is the only approved analysis available for cross-reference, BEST's structurally closest neighbors by geometry and magnet technology are **01-hts-compact-tokamak** (CFS SPARC-class, A ≈ 3, full-HTS REBCO at 20 T, R₀ ≈ 1.85 m) and **28-hts-tokamak-full-hts** (Energy Singularity, compact conventional AR, full-HTS at 25 T). Both are in-progress analyses. The central TEA question differentiating BEST from these concepts is whether lower conductor cost per unit length (Nb3Sn $2–10/kA-m vs. REBCO $30–100/kA-m) combined with Chinese construction economics (2–4× discount) offsets the larger machine volume required at lower field. CFETR Phase I parameters (R₀ = 5.7 m, B₀ = 5 T) indicate the commercial PFPP would have plasma volume roughly 7× that of a compact HTS design at 20 T — total conductor and structural steel mass scale with machine volume, partially or fully negating the per-km conductor cost advantage. Until 01-hts-compact-tokamak and 28-hts-tokamak-full-hts analyses are approved and parametric cost comparisons are available, this LTS-large-machine vs. HTS-compact-machine trade-off remains unresolved. It should be modeled explicitly as a comparative scenario — not assumed to favor either approach.

**Cross-concept positioning for TEA pipeline:**

BEST occupies the "state-backed experimental device with commercial lineage" niche that has no clear equivalent in the private-sector-dominated Western fusion landscape. The closest Western analog is the ITER → EU-DEMO pathway. BEST should be modeled in the TEA pipeline as a parameterized conventional-aspect-ratio D-T tokamak anchored to CFETR Phase I parameters (R₀ = 5.7 m, B₀ = 5 T, Ip = 10 MA, 200 MW fusion) for the intermediate step and extrapolating to a commercial PFPP at 500 MW–1.2 GW net electric — the economic sweet spot established by the UKAEA PROCESS extrapolation study [scientific-publications-wp-content-uploads-extrapolating.md §Conclusion: "the sweet spot for a commercial scale fusion power plant is between 500 MW and 1.2 GW net electric output"]. The gross-to-net ratio degradation at smaller plant sizes (17% at 100 MWe vs. 42% at 1.2 GWe) makes a first-of-kind PFPP at 500 MWe marginally viable but sensitive to recirculating power assumptions.

Key modeling parameters:
- LTS Nb3Sn as primary magnet technology (CFETR Phase I baseline)
- sCO2 Brayton power conversion at 34.7% efficiency (central case)
- Chinese construction cost discount as scenario parameter [1×, 2×, 4×]
- Blanket technology as sensitivity branch: COOL/sCO2 (34.7%) vs. WCCB/Rankine (26.4%)
- Capacity factor as dual scenario: quasi-steady-state 75–90% vs. pulsed 30–50% (CFETR duty cycle)
- Regulatory cost as scenario branch: Chinese vs. Western (2.2× factor)
- Gross-to-net ratio as a plant-size-dependent parameter (17–42% range)

---

## Section 8: Sources

**1. BEST Research Plan v1.1 (EUROfusion/ASIPP, November 2025)**
- Full citation: EUROfusion/ASIPP, "BEST Research Plan, 1st Edition: Missions and Pathways to Realisation," Version 1.1, 27 November 2025.
- Contribution: Primary technical reference for all BEST machine parameters (R₀ = 3.6 m, B₀ = 6.15 T, Ip = 7 MA, plasma volume 142 m³), magnet system design (16 Nb3Sn TF coils, 7 PF coils, hybrid CS at 18.8 T, 2000 t total), H&CD system (50 MW four-method portfolio), first wall (240 W-coated modules), divertor (48 cassettes at 10–15 MW/m²), TBM program (COOL, WCCB, EU options), plasma scenarios (Q≥1 baseline, Q~5 advanced), timeline (first plasma 2027, Q≥1 ~2030, Q~5 2032–2035), and scientific mission.
- Location: `iter-01/sources/best-research-plan-v1.1-summary.md`

**2. CFETR Power Conversion Studies (2021, 2024, 2025)**
- Contribution: Technology selection rationale for sCO2 Brayton cycle as preferred power conversion for China's fusion reactor lineage. Key result: 34.7% cycle efficiency vs. 26.4% for water steam Rankine and 23.7% for He Brayton + ORC. Compact structure and low cost advantages articulated. Supports characterization of downstream commercial power conversion assumptions.
- Location: `iter-02/sources/cfetr-power-conversion-studies.md`

**3. Neo Fusion Company Profile (FusionXInvest / 36kr)**
- Contribution: Confirms corporate identity (Fusion Energy Technology Co., Ltd / 聚变新能), majority state ownership (CNPC + CAS), $214M funding, 20-year commercialization timeline, and relationship to ASIPP. Confirms BEST is majority state-funded, not a private commercial venture.
- Location: `iter-01/sources/neo-fusion-company-profile.md`

**4. Chen, H. et al. (2015) — CFETR Preliminary Cost Assessment**
- Full citation: Chen, H. et al. (2015) "Preliminary cost assessment and comparison of China Fusion Engineering Test Reactor," *Journal of Fusion Energy*, 34(1), pp. 1–10. doi:10.1007/s10894-014-9770-x.
- Contribution: Only publicly available cost decomposition for a Chinese fusion device in the BEST/CFETR lineage. Provides order-of-magnitude capital cost structure for CFETR (now superseded by a more advanced design, but directionally relevant). Referenced in handwritten exemplar 01-hts-compact-tokamak.md as a primary data source for Chinese fusion costs.
- Location: Referenced externally; accessed via handwritten exemplar.

**5. Araiinejad, L.S. and Shirvan, K. (2025) — D-T MCF TEA**
- Full citation: Araiinejad, L.S. and Shirvan, K. (2025) "Techno-economic analysis of deuterium-tritium magnetic confinement fusion power plants," *Applied Energy*, 401(Part B), 126567. doi:10.1016/j.apenergy.2025.126567.
- Contribution: Primary source for D-T MCF LCOE sensitivity analysis including capacity factor uncertainty (75–90%), regulatory cost scenarios (Stewart & Shirvan 2.2× factor), FLiBe cost ($154/kg NOAK). Used as analogue for missing PFPP parameters. Referenced via 21-spherical-tokamak-hts approved analysis.
- Location: Referenced via handwritten exemplar 01-hts-compact-tokamak.md and 21-spherical-tokamak-hts analysis.

**6. Approved D1+ Analysis: Spherical Tokamak - HTS (21-spherical-tokamak-hts)**
- Contribution: Cross-concept reference for D-T tritium supply chain constraints, regulatory cost scenarios, capacity factor analogue range, and REBCO market pricing. Divergences documented in Section 7. Primary value is the structured framework for D-T tokamak LCOE uncertainty characterization, applicable to BEST's commercial descendants.
- Location: `analyses/21-spherical-tokamak-hts/analysis.md`

**7. Handwritten Exemplar: HTS Compact Tokamak (01-hts-compact-tokamak)**
- Contribution: Most relevant independent D-T tokamak analysis in this project. Documents ITER/ARIES/CFETR literature landscape, key LCOE drivers (magnets, blanket, capacity factor, regulatory), and Chinese fusion program data (Chen et al. 2015 cost study). Provides cross-reference framework and supply chain characterizations.
- Location: `exploration/concept_analysis/handwritten/01-hts-compact-tokamak.md`

**8. CFETR Phase I Physics Simulation (OSTI 1465662)**
- Contribution: Establishes the published CFETR Phase I design point: R₀ = 5.7 m, a = 1.6 m, B₀ = 5 T, Ip = 10 MA, 200 MW fusion power, duty cycle 0.3–0.5. Quantifies heating scenario impact on Q: NB+EC achieves Q ≈ 2.0; EC+LH only (no NBI) achieves Q ≈ 1.2, confirming that NBI cannot be eliminated without ~40% Q degradation. Primary source for CFETR Phase I parameter anchoring and LHCD applicability quantification.
- Location: `iter-02/sources/osti-pages-servlets-purl-1465662.md`

**9. UKAEA PROCESS Extrapolation Study — Extrapolating Costs to Commercial Fusion Power Plants**
- Contribution: PROCESS-based LCOE-vs-plant-size scan from 100 MW to 2 GW net electric. Establishes economic sweet spot at 500 MW–1.2 GW net electric. Key results: gross-to-net electric ratio degrades from 42% at 1.2 GWe to 17% at 100 MWe (recirculating power dominant at small sizes); blanket fluence allowance (10–20 MW-yr/m²) is an LCOE lever via replacement frequency. Confirms PFPP output estimate in Section 5 and provides gross-to-net ratio scaling for Section 5 parameter table.
- Location: `iter-02/sources/scientific-publications-wp-content-uploads-extrapolating.md`

**10. ARIES Team (various dates, late 1990s–early 2000s) — ARIES-AT, ARIES-ST Tokamak Studies**
- Contribution: Most complete published plant-level CAS cost breakdowns for conventional-aspect-ratio D-T tokamaks (ARIES-AT: R₀ = 5.2 m, B₀ = 5.9 T, Q ≈ 5). Machine parameters closely analogous to a commercial PFPP design in BEST's lineage. ARIES-AT remains the best available parametric baseline for estimating commercial tokamak capital cost structure in the absence of published Chinese program estimates.
- Location: Referenced externally (https://qedfusion.org/DOCS/bib.shtml).
