# Gap Assessment: Planar Coil Stellarator (D-T)

## Overall Readiness
**Rating**: Mostly Ready
**Summary**: Thea Energy's Helios preconceptual design (arXiv:2512.08027, DOE Milestone-certified January 2026) is one of the most thoroughly documented private fusion concepts in the public domain. Physics, engineering, and system-level performance parameters are available at exceptional detail for a preconceptual design. The primary gap for a quantitative LCOE model is the complete absence of capital cost estimates from any concept-scoped source — subsystem costs must be derived from geometry, material specifications, and fleet-wide analogs. All qualitative sections (1–4) can be executed with high confidence; the quantitative LCOE model (§5) will require a full bottom-up construction from available data.

## Section Coverage

### 1. Availability of Data
**Coverage**: Good

**Available**: The Helios overview paper (arXiv:2512.08027, ~200 pages, submitted to Fusion Engineering and Design) provides a complete preconceptual design reviewed and certified by a DOE expert panel in January 2026. This is backed by 14 companion papers submitted concurrently to the same journal covering each subsystem in detail. Four earlier Nuclear Fusion papers (January 2025) document the planar coil stellarator architecture foundation. The Canis prototype paper (arXiv:2503.18960) provides direct experimental demonstration of HTS planar shaping coil arrays. Company website and press releases fill context on the development roadmap. All core physics and engineering parameters are stated explicitly, with high-fidelity simulation results (ASCOT5, GENE/T3D, M3D-C1, OpenMC) substantiating the design assumptions.

**Missing**: Thea Energy has not published any capital cost estimates, construction cost projections, or detailed LCOE calculations. The 200-page DOE report is not publicly available; only the overview arxiv paper has been released. Eos design details are covered in the four Nuclear Fusion papers (referenced, not individually fetched). No supply chain analysis has been published.

**Gaps**:
- No capital cost estimates published for any Helios subsystem — derivable — blocking (for §5 quantitative model)
- Eos design details (Nuclear Fusion, Jan 2025) not individually fetched — not-yet-sourced — nice-to-have

### 2. Challenges in Capturing System Function
**Coverage**: Good

**Available**: The Helios paper is unusually self-aware about its own limitations. Key modeling challenges are directly discussed: (1) the software-defined field control system (450+ independent coil variables) is explicitly noted to have 450+ control variables with no precedent in prior stellarators; (2) the novel X-point divertor is flagged explicitly as requiring "additional consideration" for heat flux management at power scale (§3.7: "some combination of radiative impurity seeding, or detachment... [is required]"); (3) alpha particle loss at 6.6% to the first wall is noted as higher than academic literature and is an area of ongoing optimization; (4) the ISS04 confinement enhancement factor H=1.4 (based on W7-X QI data) is used for a QA equilibrium, acknowledged as an extrapolation — the paper validates this with gyrokinetic calculations and finds H=1.33 self-consistently; (5) V-4Cr-4Ti is used as first wall material for its 15 full-power year lifetime, but with "significant uncertainties with respect to suitability of materials for fusion environments" (§4.2); (6) D-T ice pellet fueling with mixed isotopes is noted as demonstrated only for single-isotope species in limited-duration discharges.

**Missing**: The cost modeling implications of the software control stack (450+ variables, GPU/FPGA control architecture) are not assessed — this is a novel O&M complexity driver with no analog. Heat management of 4 MW/m² peak alpha-particle heat flux is flagged but not resolved.

**Gaps**:
- Software control system O&M complexity — truly-unknown — important (no analog for 324-coil independent control system at commercial scale)
- Mixed D-T pellet fueling system at steady-state power scale — not-yet-sourced — important
- Novel X-point divertor power handling validation — truly-unknown — important (first stellarator to claim this topology; no experimental validation at power plant scale)

### 3. Maturity of Key Subsystems and Components
**Coverage**: Partial

**Available**: The Helios paper provides explicit TRL-relevant descriptions for each subsystem:
- **REBCO HTS magnets (encircling)**: TRL 4–5 — comparable to SPARC TFMC/CSMC demonstrated in large-bore coils at 20 T (cited in Canis paper §I). The planar winding approach is simpler than NoT cable architectures.
- **REBCO HTS planar shaping coils**: TRL 4 — the Canis 3×3 array (9 coils) was successfully operated at 20 K with closed-loop field control to <1% RMS error at 20 K (arXiv:2503.18960). Manufacturing at ≤1 day per double-pancake takt time demonstrated. Scaling to 324 coils is not demonstrated.
- **QA stellarator plasma physics**: TRL 5 — W7-X has demonstrated H_ISS04=1.4 and the physics basis is mature for QI configurations. QA specific to Thea/Eos architecture remains to be plasma-tested; physics is analyzed at high fidelity computationally.
- **Novel X-point divertor**: TRL 2 — "first time to our knowledge that a stellarator equilibrium has explicitly been designed to include such a divertor" (§3.7). Modeled with FLARE code; no experimental validation.
- **LiPb tritium breeding blanket**: TRL 4 — ARIES-CS, EU-DEMO, Stellaris heritage. Helios design uses 50 cm thick Pb-17Li with 65% Li-6 enrichment, EUROFER97 structure, SiC/SiC inserts, He gas coolant.
- **V-4Cr-4Ti first wall**: TRL 3–4 — irradiation data exist from fission sources; 15 full-power year lifetime is extrapolated. Paper explicitly cites "immature supply chain."
- **ECRH / 170 GHz gyrotrons**: TRL 8 — ITER-specification gyrotrons. Standard technology.
- **Steam Rankine cycle (635°C, 3 turbines)**: TRL 9 — conventional thermal plant technology.
- **Tritium fuel cycle**: TRL 4 — modeled with TMAP8 using ITER-based assumptions; "estimates are likely of the correct order of magnitude for present technology."
- **Sector-based remote maintenance**: TRL 3 — conceptual design with hardware-informed constraints; no full-scale demonstration.
- **Field-shaping units (FSUs)**: TRL 3 — grouping of shaping coils with integrated services; Canis demonstrates coil but not FSU assembly.
- **Cryogenic system**: TRL 7 — expander cycle at 10 MW electrical, 40 kW cold mass load; based on established industrial equipment.

**Missing**: TRL assessments for the field-control software stack (650+ coil current channels with GPU/FPGA real-time control) and the 51,000-tile He-cooled tungsten divertor target system are not discussed in terms of technology readiness in the paper.

**Gaps**:
- Novel X-point stellarator divertor: no experimental data — truly-unknown — important
- V-4Cr-4Ti at FPP-scale neutron fluence: limited irradiation database — not-yet-sourced — important
- FSU assembly and integration at 324-coil scale — not-yet-sourced — important (derivable from Canis data but not demonstrated)
- 51,000-piece He-cooled W tile divertor manufacturing at scale — not-yet-sourced — nice-to-have

### 4. Key Materials and Supply Chain Considerations
**Coverage**: Partial

**Available**:
- **REBCO tape**: The Canis paper confirmed manufacturing from three separate REBCO suppliers (including YBCO and GdBCO variants), demonstrating multi-supplier independence. Commercial availability is confirmed. Large-bore HTS coils at 20 T have been achieved (cited in §3.6). The Canis team demonstrated ≤1 day DP takt time.
- **Structural steel (SS316L)**: Standard, well-characterized supply chain.
- **EUROFER97**: Well-developed material for European fusion programs; blanket structure in Helios.
- **Tungsten**: 51,000 hex tiles at 2.5 cm width for divertor; standard supply chain for tungsten but fusion-scale manufacturing not demonstrated at this tile count.
- **Lead-lithium (Pb-17Li)**: Lead supply chain established. Lithium enrichment to 65% Li-6 is a gap explicitly flagged in the ARIES cost account documentation: "there is no effective large production capability of enriched lithium in the U.S." as of 2013; only small government production in the 1950s–1960s using COLEX process (which was environmentally damaging). Knowledge/sources/aries_cost_account_documentation/ confirms this remains an open supply chain challenge.
- **V-4Cr-4Ti**: The Helios paper (§4.2) explicitly states "immature supply chain" as a contraindicating consideration. Used for first wall and vacuum vessel; no large-scale industrial production exists.

**Missing**: No quantitative supply chain analysis has been published by Thea Energy. The scale of REBCO production needed for 336 coils (total tape length not stated) has not been compared against current commercial production capacity. Tritium supply chain (1-2 kg startup, then self-sufficient) is not analyzed for startup cost.

**Gaps**:
- V-4Cr-4Ti at FPP scale: no commercial production exists — truly-unknown — important (blocking cost driver if not resolved)
- Li-6 enrichment at 65% for multi-tonne LiPb inventory: no large-scale US production capability confirmed — truly-unknown — important (knowledge/sources/aries_cost_account_documentation/ confirms this gap; enrichment cost described as "completely unknown")
- REBCO tape production capacity vs. demand for 336 Helios coils — not-yet-sourced — important (search: REBCO production capacity surveys, CFS scaling analyses)
- SiC/SiC MHD inserts (blanket flow channels) at fusion-relevant scale: low TRL in neutron environment — not-yet-sourced — nice-to-have
- Tritium startup procurement cost (1-2 kg): not quantified — not-yet-sourced — nice-to-have

### 5. LCOE Parameter Extraction
**Available Parameters**:
| Parameter | Value/Range | Source | Confidence |
|-----------|-------------|--------|------------|
| Net electric power | 390 MWe | arXiv:2512.08027 Table 1 | h |
| Gross electric power | 438 MWe | arXiv:2512.08027 §4.4 | h |
| Total thermal power | 1,094 MW | arXiv:2512.08027 §4.4 | h |
| Fusion power | 958 MW | arXiv:2512.08027 Table 1 | h |
| Thermal efficiency (Rankine) | ~40.2% | arXiv:2512.08027 §4.4 | h |
| Capacity factor | 88% | arXiv:2512.08027 §4.5, abstract | m |
| Planned maintenance cycle | 84 days every 2 years | arXiv:2512.08027 §4.5 | m |
| Recirculating auxiliary power | ~70 MW (~18% of gross) | arXiv:2512.08027 §4.6 | m |
| Cryogenic system electric power | ~10 MW at 25% Carnot efficiency | arXiv:2512.08027 §4.5 | m |
| ECRH power (ignited operation) | 2.5 MW (1 MW plasma + overhead) | arXiv:2512.08027 §4.6 | h |
| Magnet operating temperature | 20 K | arXiv:2512.08027 Table 1 | h |
| First wall lifetime | 15 full-power years | arXiv:2512.08027 §4.2 | m |
| HTS coil lifetime | 40+ years (full plant life) | arXiv:2512.08027 §2 | m |
| Tritium startup inventory | 1–2 kg | arXiv:2512.08027 Table 1 | m |
| Steam cycle temperature | 635°C superheated | arXiv:2512.08027 §4.4 | h |
| Plant electrical output (Q effectively ∞) | Ignited, recirculating power fraction <3% | arXiv:2512.08027 §1 | h |
| LCOE company target (FOAK → NOAK) | $150 → $60/MWh | Dossier (thea.energy) | l |
| LCOE analog (D-T MFE NOAK tokamak) | $140–$550/MWh | knowledge/sources/tea_dt_mfe_cost_analysis/ | l |
| ARIES-CS LiPb blanket cost | ~$171M (2009$) | knowledge/sources/aries_cost_account_documentation/ | l |
| Material cost: V-4Cr-4Ti | $37/kg | knowledge/sources/tea_dt_mfe_cost_analysis/ Table 4 | l |
| Material cost: SS316 LN | $10/kg | knowledge/sources/tea_dt_mfe_cost_analysis/ Table 4 | l |
| Material cost: Tungsten | $29/kg | knowledge/sources/tea_dt_mfe_cost_analysis/ Table 4 | l |
| Supplemental heating system cost | ~$2.5/W | knowledge/sources/tea_dt_mfe_cost_analysis/ §2.2.2 | l |
| Cryosystem unit cost | ~$300/kW at 20K | knowledge/sources/tea_dt_mfe_cost_analysis/ §2.2.2 | l |
| O&M staffing (analog) | 50–95 FTE | knowledge/sources/tea_dt_mfe_cost_analysis/ §2.4 | l |
| O&M annual maintenance fraction | 9% of reactor plant equipment cost | knowledge/sources/tea_dt_mfe_cost_analysis/ §2.4 | l |
| Decommissioning cost (analog) | 5% of total capital | knowledge/sources/tea_dt_mfe_cost_analysis/ §2.5 | l |

**Missing Parameters**:
| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| CAS-level capital cost estimates (any subsystem) | derivable | blocking | Zero cost data in concept-scoped sources; must build bottom-up from geometry + material costs using TEA/ARIES framework; wide uncertainty expected |
| Total REBCO tape length for 336 Helios coils | derivable | important | Primary capital cost driver; Canis coil specs (4mm tape, 1500 turns per coil, 190×163×47mm winding pack) available as scaling basis but full Helios coil dimensions not stated numerically for encircling coils |
| Steel/structural mass for coil support structure | derivable | important | ARIES-CS structure was 3,000 tons; Helios is different architecture; mass estimate requires geometric reconstruction from figures |
| Blanket capital cost (Helios-specific) | derivable | important | 50cm LiPb geometry + EUROFER97 structure defined; ARIES-CS $171M (2009$) provides lower bound analog; requires scaling to Helios geometry |
| V-4Cr-4Ti first wall/VV fabrication cost | not-yet-sourced | important | Immature supply chain; $37/kg raw material cost available from TEA source but fabrication premium unknown |
| Li-6 enrichment cost for LiPb startup charge | truly-unknown | important | No large-scale commercial process; ARIES doc confirms no pricing data exists |
| REBCO tape unit cost at commercial production scale | not-yet-sourced | important | No public CFS/Thea quotes; literature suggests $5–50/m range; search: OSTI, CFS papers |
| Annual O&M cost (Helios-specific) | derivable | important | TEA source provides methodology (9% RPE cost + 50-95 FTE); applicable as first-pass |
| Power supply system capital cost | derivable | nice-to-have | 12 encircling coil PSUs (50 kA) + 324 shaping PSUs + ECRH; TEA $1.5/W power supply and $2.5/W heating analogs available |
| FSU (field shaping unit) assembly and installation cost | truly-unknown | nice-to-have | Novel manufacturing process for grouped 324-coil assembly; no analog |
| Back-solve to $0.01/kWh: specific binding constraints | derivable | nice-to-have | Can be computed once baseline LCOE is established |

## Source Recommendations

- **REBCO tape production capacity and unit cost at scale**: Search OSTI for "REBCO HTS tape cost projection" or "HTS cost roadmap." CFS SPARC papers may include REBCO cost assumptions. The 2022 Fusion Industry Association Supply Chain report is worth checking. Flag as `not-yet-sourced — confirm existence before searching`.

- **V-4Cr-4Ti supply chain analysis**: Published analyses exist from ARIES-AT and US materials program. Search OSTI for "V-4Cr-4Ti fusion supply chain" or "vanadium alloy fusion cost." Flag as `not-yet-sourced — likely exists in DOE fusion materials program literature`.

- **Li-6 enrichment cost**: No large-scale commercial production exists as of 2013 per knowledge/sources/aries_cost_account_documentation/. Search for recent IAEA or DOE reports on lithium isotope separation for fusion. This is likely still an open research gap. Flag as `not-yet-sourced, low probability of finding commercial pricing — may remain truly-unknown`.

- **ARIES-CS total capital cost and COE**: The ARIES-CS final report (Najmabadi et al., 2008, Fusion Engineering and Design) contains the full cost breakdown not covered by the ARIES cost account methodology document. This would provide the best available stellarator analog for a complete cost estimate. Available via ARIES project website. Flag as `not-yet-sourced — high probability of existence`.

- **Helios coil structural mass**: Thea Energy has not published structural masses. The ARIES-CS coil structure was 3,000 tons (Helios paper §1 reference). The Helios encircling coil structure uses SS316L cases + central support + inter-coil trusses. A rough estimate using major radius (8m) and 12 planar coils + truss geometry can serve as a first-pass proxy. `derivable`.

- **Divertor X-point heat flux management**: No external sources currently address this gap — it is a Thea Energy research-in-progress item. Any ITER detachment or impurity seeding literature (search: "detachment stellarator X-point") could bound assumptions. Flag as `not-yet-sourced — search ITER science program publications`.

**Fleet-wide source disqualifications** (per assessment protocol):

- `knowledge/sources/overview_of_the_helios_design_a_practical_planar_coil/` — Opened and read (v3 of arXiv:2512.08027). This is a later version of the same paper already captured as a concept-scoped source (v1). The content is identical in all substantively relevant sections; no additional information was found.

- `knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/` — Not plausibly applicable: per the source index, this covers four ARPA-E ALPHA concepts (FRC, IEC, MIF, compact tokamak variants), none of which are stellarators. The CAS methodology it uses is already covered by the tea_dt_mfe_cost_analysis and aries_cost_account_documentation sources already read; no marginal value for this concept.

- `knowledge/sources/an_assessment_of_the_economics_of_future_electric_power/` — Not plausibly applicable: the source index describes it as an ORNL historical LCOE benchmarking study for fusion vs. other electricity sources. It addresses none of the identified gaps (which are internal capital cost components and supply chain costs), and the LCOE benchmarking context needed here is already supplied by the tea_dt_mfe_cost_analysis ($140–550/MWh NOAK range).

- All IFE-focused sources (laser IFE, heavy-ion, inertial fusion) — Clearly not applicable to a magnetic confinement stellarator concept.

## Summary

Proceed to full analysis. The qualitative sections (§1–4) of the D1+ analysis can be executed with high confidence — the Helios preconceptual design is the most complete publicly available documentation of a private fusion concept, with DOE external validation adding credibility. For the quantitative LCOE model (§5), a defensible first-pass estimate can be constructed by combining: (a) the excellent performance parameters from Helios, (b) material unit costs from `knowledge/sources/tea_dt_mfe_cost_analysis/`, (c) the ARIES-CS blanket cost analog from `knowledge/sources/aries_cost_account_documentation/`, and (d) geometric reasoning from the Helios engineering sections to estimate component masses. Key uncertainties that will dominate the LCOE sensitivity analysis are: REBCO tape length and unit cost (magnet system ~40–60% of direct cost for HTS MFE designs), V-4Cr-4Ti fabrication cost, and Li-6 enrichment cost. The $150 → $60/MWh company LCOE target provides a sanity check but is not independently validated.

## Structured summary (machine-readable)

```yaml
overall_rating: "Mostly Ready"
blocking_count: 1
important_count: 6
counting_method: "section_5_lcoe_blocking_plus_important_across_all_sections_deduplicated"
section_coverage:
  availability_of_data:       "Good"
  system_function:            "Good"
  subsystem_maturity:         "Partial"
  materials_supply_chain:     "Partial"
  lcoe_parameter_extraction:  "Partial"
```