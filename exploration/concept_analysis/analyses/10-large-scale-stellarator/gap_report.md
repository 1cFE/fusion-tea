# Gap Assessment: Large-Scale Stellarator (D-T)

## Overall Readiness
**Rating**: Mostly Ready
**Summary**: Gauss Fusion's GIGA concept is unusually well-documented for a fusion startup: a 1,000+ page CDR was validated by an independent 13-person expert panel in January 2026, and the HELIAS heritage provides decades of plasma physics and blanket engineering literature. Plant-level parameters (geometry, power output, magnet system, supply chain mass budget) are publicly established. The primary gaps are proprietary CDR content — specifically the blanket type, power conversion cycle, and itemized capital cost breakdown — which must be substituted with HELIAS/ARIES-CS analogs for LCOE estimation. Qualitative analysis and TRL assessment can proceed now; quantitative LCOE modeling requires explicit analog assumptions for 2 key parameters.

---

## Section Coverage

### 1. Availability of Data
**Coverage**: Good

**Available**:
- Plant-level parameters are publicly documented across multiple sources: 3 GW thermal / 1 GW electric, 18 m major radius, 1.7 m minor radius, 1500 m³ plasma volume, 40 non-planar modular coils (5 shapes × 8), 6 T on-axis / 12–13 T on-coil, 1 MW/m² first-wall neutron load, 5-year blanket life, 40-year magnet life (`iter-01/sources/gauss-fusion-technical-summary.md`).
- HELIAS heritage (HSR4/18, HSR5/22) provides deep plasma physics literature: transport scaling (LGS and ISS95), MHD stability up to β=4.3%, alpha-particle loss rate (~2.5%), coil mass and geometry estimates, blanket weight estimates for HCPB (~7,080 t) and WCLL (~14,450 t) concepts, and ~35% thermal efficiency for Rankine cycle (`iter-01/sources/helias-reactor-context.md`).
- Supply chain bill of materials published: ~10,000 t vacuum vessel steel, ~35,000 t SC coils, ~800 t LTS + 26M m HTS, ~75 t lithium, RAFM steel, tungsten, beryllium (`iter-01/sources/gauss-fusion-technical-summary.md`).
- Partnership structure confirms active blanket (KIT/FZJ/IDOM/Alsymex), magnet (ENEA/ICAS/Tokamak Energy), and tritium cycle (F4E) work is in progress (`iter-02/sources/gauss-fusion-partnerships-2025.md`).
- Expert panel confirmation of CDR: overall architecture, system interfaces, central technical solutions reviewed and approved (`iter-02/sources/gauss-fusion-cdr-review-2026.md`).
- HELIAS 5-B HCPB blanket study provides detailed mechanical design and TBR analysis (~1.39 in idealistic model) for HCPB concept applicable to GIGA geometry (`iter-02/sources/helias-blanket-studies.md`).
- FOAK total cost estimate of €15–18B published (`iter-01/sources/gauss-fusion-technical-summary.md`).

**Missing**:
- CDR full technical content is behind a download gate; blanket type, power conversion cycle, tritium extraction scheme, and CAS-level cost breakdown are proprietary.
- No published LCOE or itemized capital cost analysis for GIGA.
- Gauss Fusion has made limited technical disclosures at conferences (MT29 magnet abstract is the most detailed public technical document).

**Gaps**:
- CDR blanket type and power conversion specifics — proprietary — important (affects thermal efficiency and capital cost structure)
- GIGA-specific LCOE / capital cost breakdown — proprietary — blocking (no public analog within Gauss publications)

---

### 2. Challenges in Capturing System Function
**Coverage**: Partial

**Available**:
- Steady-state plasma physics well understood via W7-X and HELIAS heritage: no disruptions, no current drive required, neoclassical transport minimized in QI configuration. Alpha particle losses ~2.5% tolerable for ignition balance (`iter-01/sources/helias-reactor-context.md`).
- Stellarator-specific operational advantages vs. tokamak are well documented: inherent steady-state, no Greenwald density limit, no disruption risk (`iter-02/sources/arxiv-2512-08027v1.md`, Thea Helios).
- Power balance structure: 3 GW fusion power with alpha-dominated heating; ECRH required only for startup/profile control (~50–100 MW estimated); this is confirmed by analogy with Thea Helios (10 MW ECRH startup, <1 MW ignited).
- Divertor concept: HELIAS uses island divertor concept (4/4-island topology, W7-X-derived); porthole maintenance with 8 portholes per period identified (`iter-01/sources/helias-reactor-context.md`). ARIES-CS maintenance analysis confirms porthole approach with ~85% plant availability (`iter-02/sources/core-outputs-100308302.md`).
- 3D geometry challenges for blanket design documented: many different blanket segment shapes required vs. only 2 for tokamak; complex non-planar access geometry requires ParaStell-type tools (`iter-02/sources/frontiersin-journals-nuclear-engineering-articles-10-3389.md`).
- Demountable joints: ~250 per coil at ~1 nΩ target resistance; allows sector-based maintenance (`iter-01/sources/gauss-fusion-technical-summary.md`).

**Missing**:
- Gauss Fusion's specific divertor design is not publicly disclosed. The W7-X island divertor does not scale to a power plant without major redesign — this is an acknowledged open problem in stellarator physics. Thea Helios solved this with a novel QA X-point divertor, but GIGA's QI geometry requires a different solution.
- Recirculating power breakdown not available: cryogenic load, auxiliary heating, tritium processing, vacuum pumping power are all unknown.
- Power conversion cycle architecture unknown (He/steam Rankine for HCPB vs. higher-efficiency options for DCLL).

**Gaps**:
- Divertor architecture and heat exhaust solution at power plant scale — proprietary/not-yet-sourced — important (open physics problem for stellarators; GIGA's solution is CDR-only)
- Recirculating power breakdown — derivable/proprietary — important (needed for gross-to-net efficiency and LCOE numerics)
- Power conversion cycle type — proprietary — important (determines thermal efficiency: 33% HCPB → steam vs. ~40% DCLL advanced cycle)

---

### 3. Maturity of Key Subsystems and Components
**Coverage**: Partial

**Available**:
- **Plasma physics (TRL 4–5)**: W7-X has achieved ISS04 enhancement factor H=1.4 at reactor-relevant conditions; alpha-particle confinement analytically validated in HSR4/18; MHD stability limit established at <β>=4.2–4.3%. Physics basis is the most mature subsystem.
- **LTS coil technology (TRL 4–5)**: ITER TF coils (Nb3Sn, ~300 t each, ~30–35 m perimeter) directly analogous in scale and field to GIGA coils. ICAS partnership for LTS cable manufacturing is active. Modular non-planar geometry is more complex than ITER.
- **HTS coil development (TRL 3–4)**: REBCO HTS cable/joint development in active collaboration with Tokamak Energy and ENEA. Demountable joints at ~1 nΩ are the critical innovation; this resistance target has been demonstrated in laboratory conditions but not at GIGA coil scale (~100 kA current).
- **HCPB blanket for HELIAS geometry (TRL 2–3)**: Homogeneous and heterogeneous mechanical models developed for HELIAS 5-B (`iter-02/sources/helias-blanket-studies.md`); TBR ~1.39 in idealized model. Critical: HELIAS 5-B is 5-period while GIGA is 4-period; direct transferability is partial. Prototype sub-assemblies being fabricated by Alsymex.
- **Tritium handling (TRL 2–3)**: F4E collaboration ongoing; no stellarator has ever handled tritium at power plant scale.
- **First wall/armor (TRL 4–5)**: EUROFER97 RAFM steel and W armor well-studied from DEMO program. 5-year replacement cycle feasible.
- **ECRH heating (TRL 5–6)**: W7-X uses 140 GHz ECRH; ITER-spec gyrotrons at 170 GHz are production-ready.

**Missing**:
- No published TRL-by-subsystem assessment from Gauss Fusion or an independent reviewer.
- Divertor concept for GIGA not disclosed; W7-X island divertor TRL is high (5–6) but it doesn't scale to power plant.
- Demountable SC joint performance at 100 kA / 12–13 T has not been demonstrated; prototype status unknown.

**Gaps**:
- Demountable joint validation at power plant scale — proprietary — important (de-risks the maintenance approach; CDR likely has test plan)
- Stellarator divertor at power plant scale — truly-unknown/not-yet-sourced — important (active research problem; GIGA's solution hidden in CDR)
- Per-subsystem TRL matrix (Gauss-specific) — proprietary — nice-to-have (can be estimated from heritage and published analogs)

---

### 4. Key Materials and Supply Chain Considerations
**Coverage**: Partial

**Available**:
- Mass budget is publicly documented: ~35,000 t SC coils, ~10,000 t VV steel, ~800 t LTS + 26M m HTS tape, ~75 t Li (for breeding), tungsten, RAFM steel, beryllium (`iter-01/sources/gauss-fusion-technical-summary.md`).
- HTS supply chain: 26M meters of REBCO tape is a massive procurement (~10× ITER's HTS content). Current global HTS production is ~5–10M m/year. Significant scale-up required. Partnerships with ENEA/ICAS/Tokamak Energy directly target this (`iter-02/sources/gauss-fusion-partnerships-2025.md`).
- LTS supply chain: Nb3Sn is industrially available via ITER supply chain. ICAS (ENEA/Criotec/Tratos consortium) is manufacturing LTS cables for GIGA.
- Beryllium: Critical material for neutron multiplication in HCPB blanket concept; European supply limited, strategic concern.
- Li-6 enrichment: ~75 t total Li inventory; commercial enrichment feasible but requires coordination. Only a few global facilities enrich Li-6 to >90%.
- RAFM steel (EUROFER97): Active European supply chain from DEMO program; ITER-scale manufacturing base established.
- Tungsten: Standard industrial material; no supply chain risk at planned quantities.

**Missing**:
- No published cost-per-unit estimates for critical materials in GIGA context.
- HTS supply chain ramp-up timeline and cost structure not public.
- Beryllium supply chain analysis (if HCPB blanket is selected) not published.

**Gaps**:
- HTS tape supply chain cost and ramp-up timeline — not-yet-sourced — important (26M m is a market-defining quantity; cost per unit drives CAS 22 magnet cost)
- RAFM steel fabrication cost at GIGA scale (stellarator-specific complex shapes) — not-yet-sourced — important
- Beryllium cost and supply chain risk (if HCPB) — not-yet-sourced — nice-to-have (conditional on blanket type)

---

### 5. LCOE Parameter Extraction
**Available Parameters**:
| Parameter | Value/Range | Source | Confidence |
|-----------|-------------|--------|------------|
| Net electric output | ~1 GWe | gauss-fusion-technical-summary.md | H |
| Thermal output | 3 GW | gauss-fusion-technical-summary.md | H |
| Major radius | 18 m | gauss-fusion-technical-summary.md | H |
| Plasma volume | 1,500 m³ | gauss-fusion-technical-summary.md | H |
| First wall neutron load | 1 MW/m² | gauss-fusion-technical-summary.md | H |
| Blanket/FW replacement interval | 5 years | gauss-fusion-technical-summary.md | H |
| Magnet/VV design lifetime | 40 years | gauss-fusion-technical-summary.md | H |
| SC coil mass | ~35,000 t | gauss-fusion-technical-summary.md | M |
| VV steel mass | ~10,000 t | gauss-fusion-technical-summary.md | M |
| LTS conductor mass | ~800 t | gauss-fusion-technical-summary.md | M |
| HTS tape length | ~26M m | gauss-fusion-technical-summary.md | M |
| Lithium inventory | ~75 t | gauss-fusion-technical-summary.md | M |
| FOAK total cost estimate | €15–18B | gauss-fusion-technical-summary.md | L |
| Thermal efficiency (Rankine analog) | 33–40% | helias-reactor-context.md (35%), Thea Helios (40.2%) [knowledge/sources/overview_of_the_helios_design_a_practical_planar_coil/] | M |
| Capacity factor (analog) | 85–88% | ARIES-CS (core-outputs-100308302.md, 85%), Thea Helios (88%) | M |
| LCOE range (D-T MFE analog) | $140–$550/MWh | tea_dt_mfe_cost_analysis (Araiinejad & Shirvan, 2025): $8,800–$22,200/kW OCC for 350 MWe ARC | L |

**Missing Parameters**:
| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Power conversion cycle type and efficiency | proprietary | blocking | HCPB → He/steam ~33–35%; DCLL → advanced Rankine ~40%; 7 pp spread is meaningful for LCOE. CDR specifies this. Thea Helios achieves 40.2% with Pb-Li + Rankine — usable as upper-bound analog. |
| Capital cost by CAS account (CAS 21–27) | proprietary | blocking | No public CAS breakdown for GIGA; must use ARIES-CS as analog (ARIES cost account framework from knowledge/sources/aries_cost_account_documentation/ provides the CAS structure but not GIGA-specific values) |
| Blanket type (HCPB vs. DCLL) | proprietary | important | Determines efficiency, material costs, and TBR; active partnerships but not disclosed. Thea Helios uses DCLL as direct stellarator analog. |
| Recirculating power breakdown | derivable | important | Cryogenic + auxiliary heating + pumping; can be estimated from analogs (~10–15% of gross electric) |
| O&M annual cost | not-yet-sourced | important | ARIES-CS has published O&M estimates; no GIGA-specific values |
| Tritium breeding and fuel cost | derivable | important | Standard D-T assumptions applicable; Li-6 cost and tritium processing cost not specified |
| Capacity factor (GIGA-specific) | derivable | important | Demountable joints may enable higher availability than ARIES-CS (85%); Thea Helios achieves 88% with biennial maintenance; bracket at 85–90% |
| NOAK cost scaling from FOAK | derivable | important | €15–18B is FOAK; standard learning curve methodology applicable but no Gauss-specific data |
| Decommissioning cost | derivable | nice-to-have | Standard ARIES CAS 93 methodology applicable |

---

## Source Recommendations

1. **CDR Executive Summary** (Gauss Fusion, gauss-fusion.com/cdr-executive-summary): Most critical source. Would resolve blanket type, power conversion cycle, heating system specifics, and possibly a high-level cost estimate. Listed as publicly downloadable after registration; not captured in Phase 1a. Suggested action: access CDR executive summary directly. *Existence confirmed — Gauss Fusion CDR was submitted to German government in October 2025 and reviewed January 2026.*

2. **ARIES-CS Power Plant Study** (Najmabadi et al., Fusion Engineering and Design, 2008): Definitive stellarator power plant cost study in the ARIES CAS framework. Provides capital cost breakdown for a QA compact stellarator (R=7.75 m, P_net~1 GW) using the same CAS 20-27 structure as the ARIES Cost Account Documentation. Search OSTI for "ARIES-CS" — confirmed exists as peer-reviewed publication. *Not-yet-sourced.*

3. **HSR4/18 Costing Studies** (IPP Garching, various 1999–2005): HELIAS predecessor design studies may include parametric cost estimates for the coil system and blanket. Search IPP report series (IPP-Report III/xxx) and SOFT conference proceedings. *Existence unverified — confirm before searching.* `unverified — confirm existence before searching`

4. **PROCESS Stellarator Module Documentation** (UKAEA): The PROCESS systems code has a stellarator module that outputs cost estimates for HELIAS-type configurations. UKAEA GitHub and associated publications may contain cost outputs for HSR-like parameterizations. *Not-yet-sourced.*

5. **KIT/FZJ HCPB and DCLL Blanket Studies for HELIAS geometry**: More recent publications beyond the HELIAS 5-B HCPB paper already captured. KIT has ongoing HELIAS blanket work under EUROfusion. Search OSTI or KIT repository for "HELIAS blanket 2022–2026." *Not-yet-sourced.*

6. **Disqualified fleet sources**: All IFE-focused sources (laser ICF, heavy-ion, AMPS, Xcimer, accelerators) do not apply to stellarator MFE economics and are disqualified. The ARPA-E ALPHA revisit (`knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`) covers non-stellarator MIF/MTF concepts (mirror, Z-pinch, FRC, MTF variants) and provides no stellarator-specific cost data — disqualified. The Wurzel & Hsu progress-toward-breakeven meta-analysis (`knowledge/meta_analysis/progress_toward_fusion_breakeven_lawson_criterion/`) provides physics performance benchmarks but the concept-scoped sources already establish the W7-X / HELIAS physics basis adequately — disqualified for this assessment. The historical ORNL economics assessment (`knowledge/sources/an_assessment_of_the_economics_of_future_electric_power/`) is a historical benchmarking document; the TEA D-T MFE analysis (Araiinejad & Shirvan 2025, read above) is more current and directly applicable — ORNL source disqualified.

---

## Summary

Proceed to full analysis with explicit analog assumptions for two blocking parameters. For power conversion efficiency: bracket at 33–40% using HCPB (helias-reactor-context.md, ~35%) and DCLL analogs (Thea Helios: 40.2% in `knowledge/sources/overview_of_the_helios_design_a_practical_planar_coil/`). For capital cost structure: use ARIES-CS as the primary cost analog within the ARIES CAS framework (`knowledge/sources/aries_cost_account_documentation/`), noting that GIGA's larger scale (R=18 m vs R=7.75 m), non-planar modular coil geometry, and demountable joints will diverge from ARIES-CS. The qualitative sections (system function, subsystem maturity, materials/supply chain) can be written at high quality from available sources. Attempting to acquire the CDR executive summary before LCOE modeling would reduce the two blocking gaps to important or resolved.

---

## Structured summary (machine-readable)

```yaml
overall_rating: "Mostly Ready"
blocking_count: 2
important_count: 8
counting_method: "all_sections_deduplicated: §1 CDR cost breakdown (blocking), §5 power conversion cycle (blocking); §2 divertor/recirculating power/blanket type (3 important); §3 demountable joint validation/divertor TRL (2 important, blanket type already counted); §4 HTS supply chain/RAFM fabrication cost (2 important); §5 capacity factor/O&M/NOAK scaling/tritium cost (4 important, blanket type and divertor already counted); net deduplicated: 8 important"
section_coverage:
  availability_of_data:       "Good"
  system_function:            "Partial"
  subsystem_maturity:         "Partial"
  materials_supply_chain:     "Partial"
  lcoe_parameter_extraction:  "Partial"
```