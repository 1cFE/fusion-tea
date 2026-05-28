# Gap Assessment: State-Backed Tokamak - BEST (D-T)

## Overall Readiness
**Rating**: Mostly Ready
**Summary**: The BEST Research Plan v1.1 is an exceptionally detailed source that resolves virtually all technical and physics parameters. The core challenge for this concept analysis is not data availability for BEST itself — it is the experimental-device framing: BEST is a construction-phase tokamak with no power conversion system, so LCOE analysis must be extrapolated forward through the CFEDR → PFPP lineage. Fleet-wide analogs (TEA D-T MFE, ARIES-ACT) provide a usable cost framework, but no published capital cost or economic study exists for CFEDR or the PFPP commercial endpoint. A D1+ analysis is feasible with clearly stated analog assumptions, limited by one blocking gap in the LCOE section.

---

## Section Coverage

### 1. Availability of Data
**Coverage**: Good

**Available**:
- **BEST Research Plan v1.1** (`iter-01/sources/best-research-plan-v1.1-summary.md`, 440 KB): Comprehensive joint ASIPP/EUROfusion/UKAEA document covering all machine parameters (R=3.6m, B=6.15T, Ip≤7 MA), magnet system details, 12-chapter physics/technology program, timeline through Q~5 burning plasma, TBM testing program, tritium inventory (110g), and CFEDR bridge role.
- **Neo Fusion company profile** (`iter-01/sources/neo-fusion-company-profile.md`): Ownership structure (CNPC ~20%, CAS/Hefei Science Island), registered capital increased to 14.5 billion yuan (~$2B), founding history, relationship to ASIPP. Confirms state-backed majority ownership.
- **CFETR power conversion studies** (`iter-02/sources/cfetr-power-conversion-studies.md`): sCO2 Brayton cycle analysis for CFETR-lineage reactors. Key result: sCO2 achieves 34.7% efficiency vs. 26.4% for steam Rankine and 23.7% for He-Brayton. BEST's COOL TBM uses sCO2 coolant, directly coupling to downstream power conversion choice.
- **CFETR scenario physics papers** (`iter-02/sources/arxiv-1907-11919.md`, `iter-02/sources/osti-pages-servlets-purl-1465662.md`): Integrated modeling for CFETR baseline (Q=3.2, Pfus=171 MW, R=6.6m, BT=6T) and high-performance (Q>20, Pfus>1 GW) scenarios. Establish the downstream device's physics basis.
- **ARIES-ACT study** (`iter-02/sources/osti-servlets-purl-1178069.md`): Full D-T tokamak power plant study (ACT1: R=6.25m, 6T, 1000 MWe; ACT2: R=9.75m, 8.75T, 1000 MWe). Contains detailed physics, engineering, and cost analog data for conventional-aspect-ratio D-T tokamaks.
- **Tritium breeding blanket assessment** (`iter-02/sources/osti-servlets-purl-1305833.md`): System engineering analysis for DCLL breeding blanket in MFE tokamaks — relevant to BEST's TBM validation mission.
- **TEA D-T MFE Cost Analysis** (`knowledge/sources/tea_dt_mfe_cost_analysis/`): Bottom-up LCOE framework for D-T MFE power plants (ARAI-FPP, 350 MWe). OCC $8,800–$22,200/kW, LCOE $140–$550/MWh NOAK. Full CAS methodology, subsystem breakdowns, regulatory cost drivers. Directly applicable as a cost analog for CFEDR/PFPP.
- **ARIES Cost Account Documentation** (`knowledge/sources/aries_cost_account_documentation/`): Definitive CAS framework reference (accounts 20–27 direct, 90–98 indirect), historical escalation methodology from Starfire (1980) through ARIES series.
- **Lawson criterion progress** (`knowledge/meta_analysis/progress_toward_fusion_breakeven_lawson_criterion/`): Cross-concept physics benchmarking. Tokamak-class devices (JET, TFTR, JT-60SA) define the state of the art against which BEST's Q≥1 target is calibrated.

**Missing**:
- No published techno-economic analysis or capital cost study exists for CFEDR or PFPP (China's commercial endpoint)
- Minimal English-language information on CNPC/CAS investment structure beyond the $214M initial round
- No published timeline or design-point parameters for PFPP

**Gaps**:
- No published CFEDR/PFPP cost study — not-yet-sourced (may be proprietary or not yet performed) — important
- English-language business/regulatory filings for Neo Fusion — proprietary — nice-to-have

---

### 2. Challenges in Capturing System Function
**Coverage**: Partial

**Available**:
- BEST Research Plan documents all functional subsystems: superconducting magnets, H&CD (4-method), full-W PFCs, tritium fuel cycle, TBM ports, remote handling, diagnostics. The device-level system function is very well characterized.
- CFETR scenario physics papers provide integrated operational scenarios (NB+EC, NB+LH, LH+EC) for the next-step device, establishing what BEST must demonstrate.
- sCO2 power conversion studies establish the thermal conversion pathway for downstream reactors.
- ARIES-ACT provides detailed engineering characterization of the steady-state tokamak power plant configuration, including blanket thermofluids, divertor heat management, tritium breeding, and recirculating power accounting.

**Missing**:
- No published engineering design or system architecture for CFEDR (the bridge device between BEST and PFPP)
- Blanket technology selection for CFEDR is unresolved — BEST is simultaneously testing COOL (CO2-cooled LiPb), WCCB (water-cooled ceramic breeder), and potential European TBM variants. The choice for CFEDR affects every downstream cost and performance calculation.
- No integrated plant model covering BEST → CFEDR → PFPP systems evolution
- Tritium self-sufficiency demonstration details are preliminary (BEST provides TBM test platform but doesn't breed its own tritium)

**Gaps**:
- Blanket concept selection for CFEDR — not-yet-sourced (decision depends on BEST TBM campaign results, 2028+) — important
- Integrated CFEDR system engineering design — not-yet-sourced — important
- Recirculating power budget for CFEDR/PFPP — derivable from ARIES-ACT analogs but concept-specific data absent — important

---

### 3. Maturity of Key Subsystems and Components
**Coverage**: Partial

**Available**:
- **Magnets**: TF coils (Nb3Sn ITER-heritage, well-established), PF coils (Nb3Sn/NbTi), CS (hybrid Nb3Sn + YBCO). ARIES-ACT confirms Nb3Sn at 16T is a design assumption for near-term power plants. YBCO used only in CS high-field subcoils — limited deployment, less proven at this scale.
- **Plasma-facing components**: Full-W first wall and divertor (W-coated CuCrZr heat sinks, 48 cassettes, 10–15 MW/m² rated). ITER-heritage design well-documented.
- **Heating and current drive**: 4-method system (ECRH 15 MW, ICRH 10 MW, LHCD 10 MW, NBI 12 MW). CRAFT facility already demonstrated H⁻ beam at 202 keV, 2.3 MW for 120s. All methods ITER-proven at component level.
- **Tritium fuel cycle**: External supply (110g), direct internal recycling target, detritiation systems. BEST builds on JET DTE2/DTE3 experience.
- **Lawson criterion benchmarking**: JET, JT-60SA, TFTR data establishes that Q≥1 in BEST is credible extrapolation from the current tokamak experimental record.

**Missing**:
- Formal TRL assessments per subsystem — BEST research plan describes technology goals but does not assign TRL numbers to specific components
- YBCO manufacturing TRL at BEST CS scale (18.8 T, 46.5 kA, 180-ton CS, hybrid CCIC) — no published industrial readiness data
- Reactor-grade blanket/shield TRL for CFEDR-relevant neutron fluences — BEST provides validation platform, but fusion neutron exposure data is pre-operational
- Remote handling system maturity for D-T activation environment — concept-level only

**Gaps**:
- Formal per-subsystem TRL assessments — not-yet-sourced — important
- YBCO CS manufacturing TRL at required scale — not-yet-sourced — important
- Blanket/first-wall neutron fluence performance validation — not-yet-sourced (requires operational D-T data from BEST, 2030+) — nice-to-have for current analysis

---

### 4. Key Materials and Supply Chain Considerations
**Coverage**: Partial

**Available**:
- **Nb3Sn**: ITER-grade supply chain established; BEST uses same specification. Well-understood cost and availability.
- **NbTi**: Commodity superconductor; no supply chain concerns.
- **YBCO (RE-BCO)**: Growing global supply chain. Used in CS subcoils only (not full-HTS design). CRAFT campus co-located with BEST supports in-house development.
- **Tungsten**: Industrial-grade supply established. W-coated CuCrZr tiles for first wall — ITER-heritage, supply chain exists.
- **Tritium**: External supply from fission reactor byproducts or CANDU reactors. China's supply strategy not detailed in available sources.

**Missing**:
- Tritium supply strategy and cost for China's D-T program — no source addresses China's specific tritium acquisition plan at the 110g → multi-kg scale needed for CFEDR
- Lithium-6 enrichment supply chain for breeding blankets — not addressed in any available source
- Cost data for YBCO production at scale (CS requires ~180 tons of magnet assembly)
- RAFM steel supply chain for CFEDR-scale blanket structural material — not addressed

**Gaps**:
- Tritium supply strategy for China's program — proprietary/not-yet-sourced — important
- Lithium-6 enrichment supply chain and cost — not-yet-sourced — important
- YBCO cost per kA·m at BEST CS scale — not-yet-sourced — nice-to-have

---

### 5. LCOE Parameter Extraction
**Coverage**: Partial

**Note**: BEST is an experimental device with no power conversion system. LCOE is not applicable to BEST directly. The analysis must project forward to CFEDR (demonstration) and PFPP (commercial), using BEST physics targets as the basis and fleet-wide analogs for cost structure.

**Available Parameters**:

| Parameter | Value/Range | Source | Confidence |
|-----------|-------------|--------|------------|
| Plasma Q target (BEST) | Q≥1 (T1), Q~5 (T3) | BEST Research Plan v1.1 | high |
| Fusion power (CFETR Phase I) | 171–200 MW | arxiv-1907-11919, osti-1465662 | medium |
| Fusion power (CFETR Phase II) | >1 GW | arxiv-1907-11919 | medium |
| Fusion gain Q (CFETR Phase II) | >20 | arxiv-1907-11919 | medium |
| Thermal-to-electric efficiency (sCO2 Brayton) | 34.7% | CFETR power conversion studies | medium |
| Thermal-to-electric efficiency (Rankine) | 26.4% | CFETR power conversion studies | medium |
| H&CD wall-plug efficiency (assumed, ARIES analog) | ~40% | osti-1178069 | low (analog) |
| NOAK OCC for D-T MFE (analog) | $8,800–$22,200/kW | tea_dt_mfe_cost_analysis | medium (analog) |
| NOAK LCOE for D-T MFE (analog) | $140–$550/MWh | tea_dt_mfe_cost_analysis | medium (analog) |
| ARIES-ACT1 plant size | 1000 MWe, R=6.25m, 6T | osti-1178069 | high (analog) |
| ARIES-ACT H&CD power requirement | 42.7 MW (ACT1), 105.5 MW (ACT2) | osti-1178069 | high (analog) |
| Divertor heat flux limit | 10–15 MW/m² | BEST Research Plan, osti-1178069 | high |
| Neutron wall loading (CFETR Phase I) | ~0.19 MW/m² | arxiv-1907-11919 | medium |
| Operating voltage/current for CS | 46.5 kA, peak field 18.8 T | BEST Research Plan v1.1 | high |
| Magnet system mass | ~2,000 tons | BEST Research Plan v1.1 | high |
| Tritium inventory (BEST) | 110 g | BEST Research Plan v1.1 | high |
| CFETR major radius / toroidal field | R=6.6m, BT=6T | arxiv-1907-11919 | medium |

**Missing Parameters**:

| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| CFEDR/PFPP capital cost estimate | not-yet-sourced | blocking | No published cost study for China's demonstration or commercial tokamak; Western analogs (ARIES-ACT, TEA D-T MFE at $8,800–22,200/kW OCC) can provide a proxy but with large uncertainty and no China-specific validation |
| PFPP design parameters (output, size, timeline) | truly-unknown | important | PFPP does not yet have a published design study; CFEDR is still in early conceptual phase |
| Capacity factor / availability for CFEDR/PFPP | not-yet-sourced | important | ARIES-ACT uses ~85% availability as a goal; China's program has not published a target; derivable from PROCESS-analog scaling but not validated |
| O&M cost fraction specific to this lineage | not-yet-sourced | important | TEA D-T MFE provides Western estimates but Chinese labor/regulatory costs would differ substantially |
| Net electric output target for PFPP | truly-unknown | important | CFEDR aims to demonstrate net electricity but no design-point MWe figure is published |
| Blanket replacement schedule / fluence lifetime | not-yet-sourced | important | Depends on blanket selection (unresolved) and CFEDR neutron wall loading targets |
| Tritium supply cost for multi-kg scale | not-yet-sourced | important | Critical for fuel cycle costs; no Chinese procurement data available |
| Cost breakdown by CAS account for CFEDR analog | derivable | nice-to-have | Can be constructed from ARIES-ACT and TEA D-T MFE CAS structures with stated assumptions |

---

## Source Recommendations

1. **CFEDR conceptual design reports** — search OSTI/IAEA for "CFEDR conceptual design" or "China fusion engineering demonstration reactor parameters" — likely published in Chinese journals (Nuclear Fusion and Plasma Physics, etc.) or international conference proceedings (SOFT, FEC). `not-yet-sourced` — confirm existence before searching; may be limited to Chinese-language publications.

2. **CFETR economics / cost studies** — search for "CFETR system code" or "CFETR cost of electricity" in Fusion Engineering and Design journal. Integrated system code analyses for CFETR (e.g., using GASC or a China-developed systems code) may contain cost breakdowns. `not-yet-sourced — confirm existence before searching`.

3. **BEST nuclear licensing documentation** — BEST requires a nuclear license for D-T operations. Chinese NNS (National Nuclear Safety Administration) documents, if public, would establish the regulatory framework and cost escalation context. `not-yet-sourced — likely proprietary`.

4. **CRAFT technology program reports** — CRAFT campus co-located with BEST hosts ~20 test platforms. Reports on CRAFT results (especially superconducting magnet, blanket, tritium technology platforms) would provide current TRL data for BEST subsystems. Search ASIPP publications or IAEA Fusion Research webpages. `not-yet-sourced`.

5. **ARIES-ACT detailed cost paper** — The main ARIES-ACT summary paper (`osti-1178069`) references companion cost papers in the same journal issue. Reading those (particularly Waganer's cost paper in the same Fusion Science and Technology issue) would add ARIES-ACT direct cost breakdowns by CAS account. These are likely accessible from the same OSTI source path. `not-yet-sourced`.

6. **ORNL/Fusion assessment of economics** (`knowledge/sources/an_assessment_of_the_economics_of_future_electric_power/`): This historical ORNL benchmarking source was not read for this assessment. Given that BEST/CFEDR/PFPP follows the conventional D-T MFE pathway, it would provide historical benchmarking context but is unlikely to contain concept-specific data. **Disqualified**: this source addresses the generic economics positioning of fusion vs. competing technologies (coal, nuclear, wind), not CFEDR/PFPP-specific cost parameters. It cannot downgrade any blocking or important gap for this concept.

7. **ARPA-E ALPHA Revisit** (`knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`): ALPHA concepts are MIF/compact fusion approaches (not conventional large-aspect-ratio D-T tokamaks like BEST/CFEDR). **Disqualified**: CAS-level costs for ALPHA-class concepts differ structurally from CFEDR (no large superconducting magnet systems, different plasma scales) and cannot provide applicable LCOE analogs.

---

## Summary

Proceed to full D1+ analysis. The BEST Research Plan v1.1 is among the most comprehensive experimental device design documents available in Phase 1a research, resolving all taxonomy parameters at high or medium confidence. The physics basis is rich — CFETR modeling papers establish the downstream device's performance envelope, and sCO2 power conversion efficiency is documented.

The analysis should be framed explicitly as an extrapolated-lineage assessment: BEST itself has no LCOE; the analysis projects CFEDR/PFPP economic parameters using TEA D-T MFE ($140–$550/MWh, $8,800–$22,200/kW OCC) and ARIES-ACT as Western analogs, with the caveat that no China-specific cost study exists for CFEDR or PFPP. The one blocking gap (no CFEDR/PFPP capital cost study) does not prevent analysis but requires explicit analog-proxy framing with wide uncertainty bounds. This is a well-understood and standard limitation for pre-DEMO-class fusion programs worldwide.

---

## Structured summary (machine-readable)

```yaml
overall_rating: "Mostly Ready"
blocking_count: 1
important_count: 8
counting_method: "all_sections_deduplicated — one blocking gap (no CFEDR/PFPP capital cost study) counted once; important gaps counted across §1-5 with deduplication of overlapping formulations (CFEDR design parameters, capacity factor, O&M, blanket selection, formal TRL, YBCO scale, tritium supply, net electric output target)"
section_coverage:
  availability_of_data:       "Good"
  system_function:            "Partial"
  subsystem_maturity:         "Partial"
  materials_supply_chain:     "Partial"
  lcoe_parameter_extraction:  "Partial"
```