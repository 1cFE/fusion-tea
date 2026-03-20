Now I have everything I need. Let me write the gap assessment.

---

# Gap Assessment: Planar Coil Stellarator

## Overall Readiness
**Rating**: Mostly Ready

**Summary**: The Helios preconceptual design paper (arXiv:2512.08027) is an unusually thorough public document for a private fusion company — ~200 pages, DOE-certified, with detailed plasma physics, power balance, subsystem specifications, and operational parameters. Physics performance and qualitative system coverage are excellent. The primary gap is cost breakdown detail: the LCOE target ($150/MWh → $60/MWh) is stated without a capital cost decomposition, and the Phase 1a extraction captured only a portion of the full paper. A focused read of the Helios paper's cost/economics sections would likely close most remaining gaps. Proceed to analysis with awareness of the LCOE cost-structure gaps.

---

## Section Coverage

### 1. Availability of Data
**Coverage**: Good

**Available**:
- Full preconceptual design report (arXiv:2512.08027, ~200 pages, DOE Milestone-certified January 2026). Covers plasma physics, magnets, blanket, divertor, first wall, energy conversion, maintenance, and operations.
- Canis prototype paper (arXiv:2503.18960): Confirms REBCO conductor, validates planar coil field control approach.
- Eos design published in Nuclear Fusion (Jan 2025), 4 peer-reviewed papers on the planar coil approach.
- Website/press: Company stage, funding, timeline, LCOE targets.
- Key parameters are explicitly stated with engineering justification — unusually transparent for a private company at this stage.

**Missing**:
- The 4 Nuclear Fusion (Jan 2025) papers were not individually extracted in Phase 1a (referenced via press release only). These cover coil optimization, fast ion confinement, and Eos plasma physics.
- Cost/economics section of the 200-page Helios paper was not captured in the Phase 1a extraction (extraction covers ~100 lines; 200-page paper likely contains cost modeling sections).

**Gaps**:
- Nuclear Fusion Jan 2025 papers not individually sourced — `not-yet-sourced` — important (subsystem physics detail)
- Helios cost/economics section not extracted — `not-yet-sourced` — blocking for LCOE section

---

### 2. Challenges in Capturing System Function
**Coverage**: Good

**Available**:
- Core challenge is well-defined: software-controlled field from 324 independent planar coils is entirely novel — no cost analogue exists at this scale. Paper acknowledges this explicitly ("complexity transferred from hardware to software").
- ISS04 confinement scaling required enhancement factor 1.4 (reference) / 1.33 (gyrokinetic) — stated assumption, meaning physics performance relies on an extrapolation from W7-X (30 m³) to Helios (500 m³, ~17× larger plasma volume).
- 6.6% alpha particle loss fraction documented (ASCOT5 code). Higher than typical tokamak assumptions (~2–3%), though source document notes it is within acceptable range.
- Ignited operation (Q → ∞) assumed — no burning plasma experiment has validated this for stellarators.
- Novel X-point divertor: First for an optimized stellarator, no operational heritage. Helios paper treats this as a design innovation.
- Maintaining field accuracy across 324 independent coils during full-power operation is a novel controls challenge.

**Missing**:
- No quantified uncertainty bounds on ISS04 enhancement factor — how much LCOE changes if it drops from 1.4 to 1.2 is not documented.
- No degraded-performance fallback scenario discussed in sources.

**Gaps**:
- Confinement scaling uncertainty range — `truly-unknown` (Thea has not published sensitivity bounds) — important
- Alpha loss sensitivity to plasma optimization — `not-yet-sourced` (fast ion confinement paper in Jan 2025 Nuclear Fusion set not extracted) — important

---

### 3. Maturity of Key Subsystems and Components
**Coverage**: Partial

**Available** (from sources):

| Subsystem | Status from Sources | Approximate TRL |
|-----------|--------------------|----|
| HTS planar coil array | Canis 3×3 prototype demonstrated (2025), 1% field control accuracy, REBCO confirmed | TRL 4 |
| ECRH heating (170 GHz) | ITER-specification gyrotrons; technology mature | TRL 7–8 |
| Steam Rankine cycle (635°C) | Conventional power plant technology | TRL 9 |
| QA stellarator plasma | W7-X demonstrates quasi-isodynamic; QA at Helios scale undemonstrated | TRL 3–4 |
| X-point stellarator divertor | Described as "world first" — no operational experience | TRL 2–3 |
| LiPb tritium breeding blanket | DEMO-class design, not yet built or operated | TRL 3–4 |
| Vanadium first wall (V-4Cr-4Ti) | Material characterized; no full-scale neutron-irradiated operational experience | TRL 3–4 |
| Sector-based remote maintenance | Conceptual design; Thea cites it as an innovation advantage | TRL 2–3 |

**Missing**:
- No TRL self-assessment in sources for most subsystems.
- Divertor heat flux handling (10 MW/m²) at full scale — no prototype data.
- SiC MHD inserts for LiPb blanket: Manufacturing readiness not discussed.

**Gaps**:
- Divertor thermal qualification — `truly-unknown` at this stage — important
- SiC MHD insert manufacturing at scale — `not-yet-sourced` — important
- Full stellarator sector remote maintenance prototype — `proprietary` (likely internal conceptual) — nice-to-have for LCOE modeling

---

### 4. Key Materials and Supply Chain Considerations
**Coverage**: Partial

**Available**:
- REBCO confirmed as conductor (Canis paper); three commercial suppliers demonstrated — shows manufacturing flexibility but does not quantify tape requirements or cost per meter.
- Li-6 enrichment specified: 65%; total LiPb volume derivable from blanket geometry (50 cm thick, 8 m major radius).
- Startup tritium: 1–2 kg specified.
- First wall material: V-4Cr-4Ti; lifetime 15 full-power years.
- Structural: EUROFER97.
- Divertor tiles: Tungsten (51,000 hexagonal tiles, 2.5 cm).

**Missing**:
- Total REBCO tape length required for 12 + 324 coils — not calculated in sources. Would need coil geometry to estimate.
- Li-6 enrichment supply chain: Global production capacity and pricing not discussed.
- Tritium availability on Helios timeline not analyzed (global ~25 kg inventory, committed to ITER/Eos pipeline).
- No discussion of EUROFER97 or V-4Cr-4Ti production scale relative to demand.
- Vanadium alloy is not commercially produced at power plant scale; weld qualification is open.

**Gaps**:
- REBCO tape quantity estimate and cost/meter — `derivable` from coil geometry + commercial tape pricing — important for capital cost
- Li-6 enrichment global supply chain readiness — `not-yet-sourced` — important
- Tritium startup availability for Helios on 2030s timeline — `derivable` from published tritium balance models — important
- V-4Cr-4Ti production scalability — `not-yet-sourced` — nice-to-have

---

### 5. LCOE Parameter Extraction
**Coverage**: Partial

**Available Parameters**:
| Parameter | Value/Range | Source | Confidence |
|-----------|-------------|--------|------------|
| Net electrical output | 390 MWe | arXiv:2512.08027 | high |
| Gross electrical output | 438 MWe | arXiv:2512.08027 | high |
| Fusion power | 958 MW | arXiv:2512.08027 | high |
| Total thermal power | 1,094 MW | arXiv:2512.08027 | high |
| Thermal conversion efficiency | ~40.2% | arXiv:2512.08027 | high |
| Recirculating power fraction | <3% (~48 MWe) | arXiv:2512.08027 | high |
| Capacity factor | 88% | arXiv:2512.08027 | high |
| Maintenance cycle | 84 days biennial | arXiv:2512.08027 | high |
| First wall lifetime | 15 full-power years | arXiv:2512.08027 | high |
| ECRH operational power | 2.5 MW | arXiv:2512.08027 | high |
| LCOE target (early plant) | $150/MWh | thea.energy website | medium |
| LCOE target (at scale) | $60/MWh | thea.energy website | medium |
| Machine major radius | 8 m | arXiv:2512.08027 | high |
| Magnet operating temperature | 20 K | arXiv:2512.08027 | high |
| Coil count | 12 encircling + 324 shaping | arXiv:2512.08027 | high |
| Max coil field | 20 T | arXiv:2512.08027 | high |

**Missing Parameters**:
| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Capital cost by subsystem (CAS structure) | not-yet-sourced | blocking | Full Helios paper may contain; extraction was partial |
| Total overnight capital cost ($/kWe or $B) | not-yet-sourced / proprietary | blocking | $150/MWh LCOE stated without cost basis |
| Magnet system cost (REBCO tape × length × $/m) | derivable | blocking | Coil geometry known; tape pricing from commercial data |
| Blanket replacement schedule and cost | not-yet-sourced | important | First wall = 15 FPY; blanket replacement interval unstated |
| O&M cost breakdown ($/MWh or $/yr) | proprietary | important | Not in any source |
| Facility labor cost / headcount | truly-unknown | important | No staffing model in sources |
| Li-6 enrichment procurement cost | derivable | important | Enrichment pricing exists in open literature |
| Tritium startup cost | derivable | important | 1–2 kg at ~$30k/g → $30–60M; stated assumption |
| Divertor replacement schedule | not-yet-sourced | important | 51,000 W tiles; W erosion rate depends on heat flux and time |
| ECRH capital cost (10 MW startup system) | derivable | nice-to-have | ITER gyrotron pricing exists; 10 MW system = ~$50–100M estimate |
| Balance of plant cost | derivable | important | Steam Rankine at this scale has commercial analogues |
| Indirect costs, construction, contingency | truly-unknown | important | Standard preconceptual design gap |

---

## Source Recommendations

1. **Full Helios paper cost/economics sections** — Read arXiv:2512.08027 PDF in full, specifically sections covering economic analysis, cost estimates, and LCOE calculation. The Phase 1a extraction is a partial summary; the 200-page document almost certainly contains more. `not-yet-sourced` — high priority, confirmed to exist.

2. **Nuclear Fusion Jan 2025 papers (4 papers)** — Individually extract the 4 peer-reviewed papers announced via Thea's press release. The fast ion confinement paper is particularly relevant for alpha loss sensitivity. `not-yet-sourced` — confirmed to exist, DOIs likely resolvable via Thea press release URLs.

3. **REBCO tape cost and supply data** — Search OSTI or Google Scholar for "REBCO tape cost projection," "HTS tape manufacturing cost fusion," or "2G HTS conductor market." NREL and ORNL have published HTS cost roadmaps. `not-yet-sourced` — unverified specific papers, suggest search strategy.

4. **LiPb blanket cost analogues from DEMO/ITER** — European DEMO documentation (EUROfusion) includes LiPb blanket cost estimates. The Helios blanket is EUROFER97-structured LiPb, which is close to DEMO WCLL/HCLL concepts. Search EUROfusion DEMO documentation. `not-yet-sourced` — `unverified — confirm existence before searching`.

5. **Tritium supply chain analysis** — Kovari et al. (2021) "Tritium resources available for fusion reactors" and associated papers quantify tritium availability on fusion development timelines. Relevant for startup inventory cost and availability risk. `not-yet-sourced` — paper likely exists; `unverified — confirm exact citation before searching`.

6. **V-4Cr-4Ti availability and weld qualification** — Search ORNL publications on vanadium alloy for fusion first walls. ORNL has historically led V-alloy fusion research. `not-yet-sourced` — `unverified — confirm existence before searching`.

---

## Summary

**Proceed to full analysis.** The Helios preconceptual design is one of the most well-documented pre-commercial fusion concepts available — the qualitative sections (data availability, system function challenges, subsystem maturity, materials) can be written to high quality from existing sources. The single blocking action before the quantitative LCOE model is reading the full Helios PDF for cost/economics sections, which are almost certainly present in the 200-page document but were not captured in Phase 1a's partial extraction. Secondary priority is extracting the 4 Nuclear Fusion (Jan 2025) papers for subsystem physics depth. With those two actions, this concept moves from "Mostly Ready" to "Ready."
