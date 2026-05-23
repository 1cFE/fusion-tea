# Gap Assessment: HTS Compact Tokamak (D-T)

## Overall Readiness
**Rating**: Mostly Ready
**Summary**: CFS/ARC is among the most thoroughly documented fusion concepts: a full conceptual design paper, dedicated NOAK TEA study modeled directly on ARC, power conversion cycle analysis, and a complete physics basis published in the J. Plasma Phys. 2020 special issue. All five D1+ qualitative sections can be written with good-to-partial coverage. One blocking gap (tritium start-up inventory cost, dependent on unvalidated FLiBe extraction rates) and six important gaps (detailed CAS breakdown, capacity factor, blanket replacement schedule, FLiBe T-extraction at scale, divertor design, first-wall/VV fusion-neutron lifetime) limit quantitative precision but do not prevent a first-pass analysis. Proceed to full analysis.

---

## Section Coverage

### 1. Availability of Data
**Coverage**: Good

**Available**:
- **Full ARC conceptual design** (Sorbom et al. 2015, `arc-reactor-specifications.md`): 30+ pages covering plasma physics, magnets, blanket/neutron shielding, heating systems, and Section 6 rough costing (~$5.56B total fabricated cost by material-volume scaling, versus ~$24B ITER by same method). Plasma parameters, engineering constraints, and R&D requirements all documented.
- **SPARC overview** (Creely et al. 2020, referenced in dossier): device parameters including B_t=12.2 T, R=1.85 m, a=0.57 m, Q≥2 target. SPARC construction confirmed under way, first magnet installed January 2026 per `cfs-2025-2026-updates.md`.
- **Power conversion analysis** (`arc-power-conversion-studies.md`, Colliva et al. 2024, Sapienza/Eni): GateCycle™ simulation of three cycles for ARC FNSF phase (645 MW_th input). Rankine: 46% net efficiency, 297 MWe net. CO₂ Brayton: 40.3%. He Brayton: 32%. Rankine identified as most promising on efficiency and commercial availability.
- **ARC original Brayton baseline** (`arc-reactor-specifications.md`): He Brayton at 900 K → 40% efficiency (190 MWe, FNSF), up to 50% efficiency at 1200 K (261 MWe, aggressive pilot).
- **Dedicated NOAK TEA** (`knowledge/sources/tea_dt_mfe_cost_analysis/output.md`, Araiinejad & Shirvan 2025, MIT Applied Energy): ARAI-FPP is explicitly a 350 MWe tokamak modeled on the MIT ARC concept. NOAK overnight capital costs $8,800–$22,200/kW; LCOE $140–$550/MWh. Finds fusion reactor equipment is dominant cost driver, consistent with ARC Section 6.
- **REBCO tape supply chain** (`sciencedirect-science-article-pii-s2772830725000390.md`): PLD-REBCO at >200 A/4mm @20 K, 20 T; current pricing $20/m; global production >3,000 km/yr-12 mm (>50% of world HTS wire output). Directly constrains ARC magnet cost modeling.
- **Li-6 supply paper** (`sciencedirect-science-article-pii-s092037961930835x.md`): European DEMO-oriented ICOMAX process for Li-6 enrichment; confirms Li-6 is not commercially available at required scale.
- **Costing methodology** (`arxiv-2601-21724.md`, Woodruff 2026, pyFECONs framework; `arxiv-2602-19389.md`, CATF IWG 2026): Both read. The CATF paper explicitly covers HTS magnet cost modeling as Account 22.1.3 "swap-point" for MFE, with TRL-based maturity uncertainty and learning-rate uncertainty propagation. Provides methodology to build an ARC-like cost model. Cited FOAK LCOE range for compact tokamaks: 150–200 $/MWh; NOAK at 60–100 $/MWh.
- **ARPA-E ALPHA revisit** (`knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/output.md`): CAS-level cost breakdown for four compact MIF concepts (~500 MWe). Average total capital cost $1.2B; BOP structure (CAS 21, 22.2, 22.5, 23, 24, 25, 26) provides analogues applicable to ARC. Note: CAS 22.1.3 coils average only $5.9M because these are non-magnet concepts — magnet costs not transferable. Fuel processing (CAS 22.5) average $124M is applicable.
- **Maintenance optimization study** (`arxiv-2405-01514.md`, Schwartz et al. 2024): Tokamak maintenance strategy valuation in decarbonized US grid. Uses 85% net/gross ratio (5% active + 10% passive parasitic); shows 80% availability retains 87–91% of capacity value. Provides quantitative framework for ARC capacity factor assumption.

**Missing**:
- Current ARC commercial design (400 MWe, Virginia site) not yet fully published by CFS — proprietary
- CFS has not disclosed detailed capital cost breakdown for ARC by subsystem — proprietary

**Gaps**:
- Detailed CAS cost breakdown for ARC/SPARC from CFS — proprietary — important
- Post-2021 ARC design documentation (evolved from 200→400 MWe) — proprietary — important

---

### 2. Challenges in Capturing System Function
**Coverage**: Partial

**Available**:
- **I-mode confinement uncertainty**: ARC paper explicitly quantifies sensitivity to H₉₈ (design point H₉₈~2.8, well above standard H-mode ~1.0; FNSF mission achievable at H₈₉~2.2). ARC exploits weak degradation of I-mode with heating power (τ_E ∝ P_heat^−0.27 vs. H-mode −0.69). Physics arguments for achievability documented, but I-mode at ARC scale is extrapolated from C-Mod.
- **Non-inductive scenario**: ACCOME code modeling of bootstrap (63%) + LHCD (25 MW) + ICRF (13.6 MW) combination; sensitivity analysis shows self-consistent operating point accessible. SPARC ICRF design documented in `sparc-icrf-heating-paper.md` at SPARC-specific parameters (120 MHz, 25 MW, 3He minority + 2nd harmonic T).
- **FLiBe blanket complexity**: ARC paper discusses: (a) magnetic field effects on FLiBe flow/heat transfer are computationally investigated but not experimentally validated in fusion environment; (b) radiation-assisted corrosion of Inconel 718 in FLiBe not tested in D-T environment; (c) tritium extraction turnaround time not experimentally established at required scale.
- **Pulsed operation / grid integration**: Colliva 2024 paper explicitly includes energy storage system (ESS) in FLiBe intermediate circuit to provide constant turbine load during dwell phases. ESS architecture identified but sizing not costed.
- **Demountable joints**: ARC paper identifies joints as key R&D item; bench-top tests exist but reactor-level fields (23 T, ~8 MA) not yet demonstrated. PIT VIPER (pulsed magnet technology) now demonstrated at CFS for PF/CS.

**Missing**:
- Divertor design: explicitly deferred in ARC 2015 paper ("left for later study"). No divertor design published.
- Quantitative disruption frequency and mitigation design: qualitative discussion only
- Quantitative tritium extraction turnaround time from FLiBe

**Gaps**:
- Divertor design: heat exhaust at ARC power density (~30 MW/m² scrape-off) — not-yet-sourced (no ARC divertor paper published) — important
- FLiBe tritium extraction rate / inventory requirements — truly-unknown at ARC scale — important
- I-mode scaling from C-Mod to ARC (x5 linear scale-up) — derivable (using published scaling + uncertainty bounds) — important
- ESS (thermal storage) cost and sizing for pulsed operation — not-yet-sourced — nice-to-have

---

### 3. Maturity of Key Subsystems and Components
**Coverage**: Partial

**Available**:
- **HTS TF magnets (TRL 5–6)**: 20 T large-bore REBCO magnet demonstrated September 2021; SPARC TF coils manufactured and first one installed January 2026. Full-scale demountable joint demonstration pending SPARC assembly.
- **ICRF heating system (TRL 6–7)**: SPARC ICRF fully designed (`sparc-icrf-heating-paper.md`); 120 MHz fast wave system based on C-Mod heritage; 25 MW specified; megawatt-level RF sources within reach of present technology. Antenna impurity control addressed.
- **REBCO tape production (TRL 7–8)**: $20/m, >3,000 km/yr global supply, PLD process well established (`sciencedirect-science-article-pii-s2772830725000390.md`). Adequate for SPARC; ARC fleet would require significant scale-up.
- **Thermal power conversion (TRL 7–8)**: Supercritical steam Rankine cycle is commercial technology; Colliva 2024 confirms no new turbine technology needed for ARC FNSF phase.
- **PF/CS magnets (TRL 5)**: PIT VIPER pulsed superconducting technology demonstrated by CFS for pulsed poloidal coils.

**Missing**:
- FLiBe blanket integrated with fusion neutron flux: TRL 2–3. The LLNL TBB assessment (`osti-servlets-purl-1305833.md`) covers DCLL blanket for generic MFE tokamak — not FLiBe specific. FLiBe has fission reactor heritage (MSRE, AHTR studies) but no fusion-integrated test.
- Tritium extraction from FLiBe at scale: TRL 2–3. ARC paper cites only two references for possible extraction schemes; LLNL report notes no experiments have been built to assess turnover time.
- Vacuum vessel/first wall (Inconel 718) in D-T neutron environment: TRL 3. REBCO fluence limit conservatively 9 FPY per MCNP; but Inconel 718 chromium transport under radiation-assisted corrosion in FLiBe uncharacterized.
- LHCD at 8 GHz: TRL 4 (standard klystron sources at 5–6 GHz; 8 GHz not yet demonstrated). JAERI LHCD review (`osti-etdeweb-servlets-purl-10149275.md`) covers existing LHCD physics but does not address 8 GHz system specifically.
- Remote maintenance with demountable coils at reactor scale: TRL 3–4 (concept demonstrated at bench scale with Vulcan, full-reactor demount pending SPARC)

**Gaps**:
- FLiBe blanket integrated test in fusion neutron environment — truly-unknown — important
- Tritium extraction from FLiBe at required throughput — truly-unknown — important (relates to blocking gap §5)
- First wall / Inconel 718 fusion neutron + FLiBe compatibility — truly-unknown — important
- 8 GHz LHCD klystron demonstration — not-yet-sourced — nice-to-have
- Demountable joint operation at 23 T, reactor scale — not-yet-sourced (SPARC will validate) — important

---

### 4. Key Materials and Supply Chain Considerations
**Coverage**: Partial

**Available**:
- **REBCO tape**: $20/m, >3,000 km-12mm/yr global production (`sciencedirect-science-article-pii-s2772830725000390.md`). PLD process provides excellent in-field performance (>200 A/4mm @ 20 K, 20 T). Challenges remain in further cost reduction and process stability. ARC tape inventory is large but manageable given current production rates.
- **FLiBe (LiF-BeF2)**: Long heritage from molten salt fission research (MSRE, AHTR). LiF is a commodity chemical. BeF2 production is specialty; beryllium sourcing (US and Kazakhstan producers) has well-characterized constraints.
- **Li-6 enrichment**: Not commercially available at DEMO/ARC fleet scale (`sciencedirect-science-article-pii-s092037961930835x.md`). ICOMAX (mercury amalgam) process proposed as path for DEMO supply; requires decade-scale lead time. Current lithium isotope separation capacity insufficient for fleet deployment.
- **Inconel 718 (vacuum vessel)**: Commercially available, well-characterized at ambient and elevated temperatures. ARC paper notes high nickel content increases activation — important for waste classification.
- **TiH2 (neutron shielding)**: Powder form; ARC paper notes limited experimental data in fusion environment.

**Missing**:
- REBCO tape scale-up for full ARC fleet (single ARC unit likely requires >100–200 km tape given SPARC scale); learning curve data at fleet scale
- Beryllium sourcing and BeF2 availability for FLiBe inventory (full blanket + heat exchanger = ~500 m³ per ARC)
- Tritium startup inventory supply: natural production from CANDU reactors and fission is limited; ARC-scale startup inventory requirements unknown pending FLiBe extraction data

**Gaps**:
- BeF2 supply chain at ARC fleet scale — not-yet-sourced — important
- Li-6 enrichment at ARC fleet scale (ICOMAX not yet commercial) — derivable (DEMO studies apply) — important
- Tritium startup procurement timeline and cost — truly-unknown (depends on FLiBe extraction rate and therefore inventory size) — blocking (contributes to §5 blocking gap)
- REBCO tape fleet manufacturing scale-up cost trajectory — derivable (use learning rate from PLD paper + pyFECONs) — nice-to-have
- Activated FLiBe waste management / classification — derivable — nice-to-have

---

### 5. LCOE Parameter Extraction
**Available Parameters**:
| Parameter | Value/Range | Source | Confidence |
|-----------|-------------|--------|------------|
| Fusion power | 525 MW (ARC 2015) | `arc-reactor-specifications.md`, Table 1 | h |
| Plasma gain Q_p | ~13.6 | `arc-reactor-specifications.md`, abstract | h |
| Net electric output | 190–261 MWe (2015 design); 400 MWe (current target) | ARC paper §2; `cfs-2025-2026-updates.md` | m |
| On-axis field B₀ | 9.2 T (ARC); 12.2 T (SPARC) | ARC paper Table 1; `sparc-icrf-heating-paper.md` | h |
| Thermal efficiency (He Brayton, FNSF) | ~40% (900 K outlet) | `arc-reactor-specifications.md` §2 | m |
| Thermal efficiency (Rankine, FNSF) | 46% net (645 MW_th in) | `arc-power-conversion-studies.md`, Table 6 | m |
| Blanket TBR | ≥1.1 (baseline); up to 1.22 | ARC paper §5 | h |
| Bootstrap fraction | 63% | ARC paper §3.4 | h |
| REBCO tape price | ~$20/m | `sciencedirect...s2772830725000390.md` | m |
| Component fabricated cost (2015 scaling) | ~$5.56B total | ARC paper §6 | l |
| NOAK overnight capital cost (ARC-based) | $8,800–$22,200/kW | `tea_dt_mfe_cost_analysis/output.md`, Araiinejad 2025 | m |
| NOAK LCOE (ARC-based) | $140–$550/MWh | `tea_dt_mfe_cost_analysis/output.md`, Araiinejad 2025 | m |
| FOAK LCOE (compact tokamaks, industry) | 150–200 $/MWh | `arxiv-2602-19389.md` §2.1.5 | l |
| Fuel processing (CAS 22.5) analogue | ~$124M | `knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/output.md` | l |
| O&M costs analogue | ~$48M/yr | `knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/output.md` | l |
| Optimal maintenance availability | 75–85% | `arxiv-2405-01514.md`, Schwartz 2024 | m |
| First wall lifetime (TF coil fluence limit) | ≥9 FPY | ARC paper §5.2 | l |

**Missing Parameters**:
| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Tritium startup inventory (kg, cost) | truly-unknown | blocking | FLiBe extraction turnaround time uncharacterized; inventory could range from kg-tens of kg; cost $M–$B range. No ARC-specific published data. |
| ARC-specific capacity factor | proprietary / derivable | important | CFS has not published; Schwartz 2024 supports 75–85% analogue assumption |
| Detailed CAS breakdown for ARC | proprietary | important | Only total NOAK range known from Araiinejad 2025; subsystem allocation (magnets, blanket, BOP) requires inference from ARIES/pyFECONs framework |
| Blanket replacement schedule / FPY lifetime | proprietary / derivable | important | FLiBe VV not published; 9 FPY TF fluence limit gives upper bound; actual schedule likely shorter |
| FOAK vs. NOAK cost differential for ARC | derivable | important | Use pyFECONs CATF methodology and reference class forecasting (1.5–3× uplift) |
| Divertor cost and replacement | not-yet-sourced | important | Divertor not designed in ARC 2015; no published ARC divertor cost estimate |
| First wall / Inconel 718 replacement cost | truly-unknown | important | Radiation-assisted corrosion in FLiBe uncharacterized; lifetime uncertain |

---

## Source Recommendations

- **ARC divertor design**: Search OSTI / J. Fusion Engineering and Design for "ARC divertor" or "high-field-side divertor compact tokamak 2020-2026." A 2022–2025 PSFC study may exist. `unverified — confirm existence before searching`
- **FLiBe tritium extraction turnaround time**: Search for "FLiBe tritium extraction" in OSTI, IAEA, and molten salt fission literature (ORNL MSR heritage). ORNL TM reports on MSRE tritium behavior are partially applicable. `not-yet-sourced — ORNL CF-71-8-10 and related documents exist in archive`
- **CFS ARC detailed cost study**: Commonwealth Fusion Systems has not publicly released a CAS-level breakdown. Monitor CFS publications and conference papers (EPS, IAEA FEC, SOFE) for ARC economic analyses. `proprietary — no public disclosure expected before ARC FOAK construction`
- **REBCO tape learning curve for fusion scale**: Search IEEE Transactions on Applied Superconductivity and SuperPower/Fujikura production cost publications for learning-rate quantification. `not-yet-sourced`
- **Li-6 supply at ARC fleet scale**: The ICOMAX paper (cited in §4 sciencedirect source) directly addresses DEMO-scale supply; also check IAEA DEMO tritium breeding studies. Already partially addressed by `sciencedirect-science-article-pii-s092037961930835x.md`.
- **Progress toward fusion breakeven (Wurzel & Hsu 2021)** at `knowledge/meta_analysis/progress_toward_fusion_breakeven_lawson_criterion/`: Not read in this assessment. After opening: this meta-analysis covers achieved nτE across MCF, ICF, MIF. For HTS Compact Tokamak, it would benchmark SPARC's projected performance (estimated nτE ~10²⁰ keV·s/m³) against historical devices. However, the physics state-of-the-art for tokamaks is already thoroughly documented in concept-scoped sources. This source adds marginal value for §3 (maturity) but does not address any of the six important gaps. **Disqualified** for this assessment — does not cover ARC/SPARC economic or engineering parameters and adds no new information to any current gap.

---

## Summary
Proceed to full analysis. The HTS Compact Tokamak (D-T) has the richest public data of any advanced fusion startup concept: a full peer-reviewed conceptual design, a dedicated 2025 MIT TEA study explicitly modeled on ARC (Araiinejad & Shirvan), a power conversion cycle analysis (Colliva 2024), comprehensive SPARC physics basis papers, and the pyFECONs/CATF costing framework applicable to MFE HTS tokamaks. The one blocking gap — tritium startup inventory cost, gated on unpublished FLiBe extraction rates — can be handled in analysis by presenting a range using bounding assumptions from molten-salt fission experience. All other gaps are bridgeable with stated assumptions and fleet-wide analogues. The LCOE model can be constructed using: 400 MWe net output, 46% thermal efficiency (Rankine, Colliva 2024), $8,800–$22,200/kW capital cost (Araiinejad 2025), 75–85% capacity factor (Schwartz 2024 analogue), and ~$48–80M/yr O&M (ALPHA costing with HTS magnet cryo adder).

---

## Structured summary (machine-readable)

```yaml
overall_rating: "Mostly Ready"
blocking_count: 1
important_count: 6
counting_method: "all_sections_deduplicated — one blocking gap (tritium startup inventory cost, gated on unvalidated FLiBe extraction rate); six important gaps (detailed ARC CAS breakdown, ARC-specific capacity factor, blanket replacement schedule, FLiBe T-extraction at integrated scale, divertor design/cost, first wall / VV fusion-neutron lifetime)"
section_coverage:
  availability_of_data:       "Good"
  system_function:            "Partial"
  subsystem_maturity:         "Partial"
  materials_supply_chain:     "Partial"
  lcoe_parameter_extraction:  "Partial"
```