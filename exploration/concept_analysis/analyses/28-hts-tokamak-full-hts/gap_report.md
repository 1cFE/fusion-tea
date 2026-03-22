# Gap Assessment: HTS Tokamak - Full HTS

## Overall Readiness
**Rating**: Significant Gaps

**Summary**: Energy Singularity has a well-documented prototype (HH70) and magnet demonstration (Jingtian) with strong media coverage, but almost no engineering data relevant to a power plant. The company is at a very early stage — HH380 (the demo power plant) is post-2030 and has zero published specifications. The qualitative write-up is achievable with significant use of analogues and inference, but the quantitative LCOE model will rely heavily on SPARC/ARC scaling rather than any Energy Singularity-specific data.

---

## Section Coverage

### 1. Availability of Data
**Coverage**: Partial

**Available**:
- HH70 prototype parameters (major/minor radius, magnet specs, coil count, field strength, plasma records) — well-documented across multiple media sources and FusionEnergyBase
- Jingtian magnet: 21.7–22.4 T peak field, dimensions, winding pack details, published in IEEE TAS 2025
- HH170 roadmap: Q > 10 target, ~14 T on-axis, ~70% SPARC volume, 25 T magnet target, 2027 completion
- Company funding: ~$110M raised, seeking $500M for HH170
- Construction timeline: HH70 built in under 2 years, >96% domestic component sourcing
- Two paywalled ScienceDirect papers covering HH70 commissioning and magnet system construction (not accessed)

**Missing**:
- HH380 power plant: zero public engineering specifications
- Thermal/power conversion system design
- Blanket design and tritium breeding approach
- Detailed plasma parameters (temperature, density, confinement time)
- Detailed heating systems for HH170

**Gaps**:
- HH380 engineering specs — `proprietary` + `truly-unknown` (not yet designed) — **blocking** for power-plant-specific LCOE
- Paywalled HH70 commissioning paper (Fusion Engineering and Design, 2025) — `not-yet-sourced` — **important** (may contain plasma parameters and heating details not in media coverage)
- Paywalled HH70 magnet paper (Superconductivity, 2024) — `not-yet-sourced` — **important** (likely has detailed magnet cost-relevant manufacturing data)
- Chinese-language technical publications beyond media — `not-yet-sourced` — **nice-to-have**

---

### 2. Challenges in Capturing System Function
**Coverage**: Partial

**Available**:
- The full-HTS differentiator is well-understood: all TF, PF, and CS coils are REBCO, which is unique among public tokamak programs
- AI-based plasma control system noted; 100 shots/day vs. 20–30/day at JET suggests operational efficiency
- Steady-state operation demonstrated at prototype scale (1,337 s)
- "D-T equivalent" Q > 10 framing for HH170 suggests the machine may not actually burn D-T — this complicates the cost model baseline

**Missing**:
- No cost analogues for all-REBCO coil sets at power-plant scale (HTS-only is genuinely novel)
- Physics basis for Q > 10 claim is not publicly detailed — no published confinement scaling analysis
- Whether HH170 actually burns D-T or achieves "D-T equivalent" via other means is ambiguous
- No published system-level integration analysis connecting magnet field → plasma gain → electrical output

**Gaps**:
- HTS coil cost scaling law for full-HTS vs. hybrid HTS designs — `not-yet-sourced` — **important** (CFS/SPARC literature has some REBCO cost modeling that could be adapted)
- Q claim validation / physics basis — `not-yet-sourced` — **important** (SPARC/ARC physics papers could provide analogue; Energy Singularity-specific basis not published)
- "D-T equivalent" operating mode clarification — `proprietary` — **important** (affects fuel cycle and neutron load assumptions)

---

### 3. Maturity of Key Subsystems and Components
**Coverage**: Partial

**Available**:
- **HTS magnets (TF)**: TRL ~5–6. Jingtian demonstrated 21.7 T at sub-coil scale; HH170 TF coil design in progress. Published IEEE TAS paper.
- **HTS magnets (PF/CS)**: TRL ~4–5. HH70 prototype demonstrated full coil set at low field (0.6–1 T). High-field CS is less demonstrated.
- **Plasma control system**: TRL ~6. AI-based system demonstrated on HH70 with 5,755 shots and long-pulse capability.
- **ICRF heating**: TRL ~7. Standard technology, demonstrated on HH70. Scale-up for HH170 unclear.

**Missing**:
- **Blanket / tritium breeding system**: TRL 1 (not yet conceptually designed at Energy Singularity)
- **First wall / plasma-facing components**: TRL unknown — no public information
- **Energy conversion / balance of plant**: TRL unknown — not disclosed
- **Vacuum vessel at HH380 scale**: TRL unknown
- **Tritium handling and processing systems**: TRL unknown

**Gaps**:
- Blanket TRL and design approach — `truly-unknown` (company stage) — **blocking** for completeness; manageable via CFETR/ITER blanket analogues for the write-up
- First wall material and replacement schedule — `not-yet-sourced` — **important** (tungsten PFC experience from ITER/EAST applicable; search OSTI/FDS for compact tokamak PFC studies)
- Balance of plant TRL — `not-yet-sourced` — **important** (use generic D-T steam cycle as analogue)

---

### 4. Key Materials and Supply Chain Considerations
**Coverage**: Partial

**Available**:
- REBCO tape is the dominant material; supplier is Shanghai Superconductor (domestic)
- >96% domestic component localization confirmed — significant China supply chain concentration
- HH70 TF coil uses 450 m of HTS conductor per coil, ~480 μm total conductor thickness
- REBCO = Rare Earth Barium Copper Oxide → rare earth supply dependency (yttrium, barium)
- China has dominant global rare earth production position

**Missing**:
- REBCO tape production capacity at power-plant scale (how many km of tape for HH380?)
- Cost per meter of REBCO tape (Energy Singularity-specific — likely negotiated proprietary pricing)
- Manufacturing capacity for 25 T D-shaped magnets at the required quantity for a power plant
- Tritium supply chain (standard D-T issue, not Energy Singularity-specific)
- Any Li-6 enrichment details for eventual blanket

**Gaps**:
- REBCO tape cost and supply chain capacity — `not-yet-sourced` — **important** (SuperPower, Fujikura, AMSC published capacity data; CFS ARC study has REBCO cost estimates that could be adapted; search "REBCO tape manufacturing scale" and "HTS cost projections 2030")
- HH380 magnet tape requirements (total conductor length) — `derivable` from HH70 scaling — **important**
- Rare earth supply chain concentration risk quantification — `not-yet-sourced` — **nice-to-have** (USGS critical materials reports)
- Li-6 isotope enrichment supply — `not-yet-sourced` — **nice-to-have** (generic D-T blanket literature)

---

### 5. LCOE Parameter Extraction
**Coverage**: Poor

**Available Parameters**:
| Parameter | Value/Range | Source | Confidence |
|-----------|-------------|--------|------------|
| Fusion gain target (Q) | >10 (HH170 target) | dossier / iter-01 | m |
| Machine size (HH170) | ~70% SPARC volume, ~14 T on-axis | dossier / iter-02 | m |
| Magnet peak field (HH170) | 25 T (target) | dossier | m |
| Magnet peak field (demonstrated) | 21.7–22.4 T (Jingtian) | dossier | h |
| Operation mode | Steady-state | dossier | h |
| Commercialization target | Before 2035 | iter-01 | l |
| HH170 funding | ~$500M sought | iter-01 | m |
| HH70 funding | ~$110M raised | iter-01 | m |
| Domestic supply chain | >96% | iter-02 | h |

**Missing Parameters**:
| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Plant net electrical output (HH380 MW_e) | truly-unknown | blocking | No HH380 specs; use SPARC/ARC analogue |
| Capital cost by CAS component | truly-unknown | blocking | No published cost data; derive from SPARC ARC study scaled to HH170/HH380 geometry |
| REBCO tape cost ($/kA-m or $/m) | not-yet-sourced | blocking | CFS/MIT ARC study has estimates; AMSC published pricing |
| Thermal cycle type and efficiency | proprietary/truly-unknown | blocking | Infer as standard Rankine or sCO2; no ES data |
| Capacity factor / availability | truly-unknown | blocking | No published target; use 80–90% analogue from tokamak literature |
| Blanket design / TBR | truly-unknown | important | Not yet designed; CFETR/DEMO analogue |
| First wall replacement schedule | not-yet-sourced | important | ITER/EAST/compact tokamak literature |
| Heating power requirement (HH380) | not-yet-sourced | important | Derive from Q target and gain framing |
| Operating cost breakdown | truly-unknown | important | No ES data; generic tokamak O&M analogue |
| Tritium cost and consumption | derivable | important | Standard D-T fuel cycle; derive from Q and P_fusion |
| Plant construction time | truly-unknown | nice-to-have | HH70 built in <2 years — not directly extrapolatable |

---

## Source Recommendations

1. **CFS/MIT ARC plant study** — for capital cost scaling, REBCO tape quantities, and balance-of-plant design by CAS category. Search: "ARC tokamak plant study Freidberg" or "SPARC cost model". `not-yet-sourced` — confirm existence before searching; ARC papers are published and accessible via OSTI.
   
2. **ScienceDirect HH70 commissioning paper** (doi:10.1016/j.fusengdes.2025.115341) — may contain plasma parameters, heating system details, and magnet cost-relevant data not in public media. `not-yet-sourced` — known to exist, paywalled; access via institutional library or Sci-Hub equivalent.

3. **ScienceDirect HH70 magnet paper** (doi:10.1016/j.supcon.2024.100119) — likely has detailed REBCO conductor specifications and manufacturing data relevant to cost scaling. `not-yet-sourced` — known to exist, paywalled.

4. **IEEE TAS Jingtian paper** (2025) — cited in IAEA World Fusion Outlook; may contain detailed magnet fabrication and cost data. `not-yet-sourced` — confirm via IEEE Xplore search for "Jingtian" or "Energy Singularity".

5. **REBCO tape cost projections** — search OSTI for "REBCO tape cost manufacturing scale 2030" or "HTS tape cost learning curve". SuperPower and AMSC have published some cost roadmap data. `not-yet-sourced` — `unverified — confirm existence before searching`.

6. **CFETR plant study** — China's domestic fusion program has published blanket and balance-of-plant studies that represent a likely analogue for what Energy Singularity would eventually adopt. Search "CFETR plant study WCCB blanket LCOE". `not-yet-sourced` — `unverified — confirm existence before searching`.

7. **Compact tokamak PFC and first wall studies** — search OSTI/IAEA for "compact tokamak first wall replacement schedule" or "ST40 PFC tungsten". `not-yet-sourced` — `unverified — confirm existence before searching`.

---

## Summary

**Proceed to full analysis with explicit analogue strategy.** The qualitative sections (data availability, system function challenges, subsystem maturity, supply chain) are well-supported by what's available — Energy Singularity's prototype work and magnet demonstrations give enough to write a substantive narrative. The key challenge is that this is an early-stage Chinese private company with limited public disclosure, and HH380 (the relevant power plant) is fully undisclosed.

For the quantitative LCOE model, proceed by:
1. Using SPARC/ARC as the primary cost analogue (similar field strength, compact tokamak geometry, HTS magnets)
2. Scaling capital cost estimates to HH170/HH380 geometry (~70% SPARC volume)
3. Applying standard D-T fuel cycle assumptions (blanket, tritium handling) as placeholder
4. Using generic Rankine or sCO2 thermal cycle assumptions for energy conversion
5. Flagging all analogue-derived values explicitly — Energy Singularity has published essentially no cost data

The two paywalled ScienceDirect papers are the highest-value unexplored sources and should be accessed if possible before the quantitative model is finalized, as they may contain plasma parameters and magnet manufacturing details that improve the cost basis beyond generic analogues.
