# Phase 3 diff: 01-hts-compact-tokamak

**Generated:** 2026-05-22T13:05:55-07:00

## Counts (Phase 2 -> Phase 3 strict-read regen)

| field | phase2 | phase3 | Δ |
|-------|--------|--------|---|
| blocking_count   | 0 | 1 | 1 |
| important_count  | 7 | 6 | - |
| overall_rating   | Mostly Ready | Mostly Ready | - |

## Fleet-source dispositions in new report

```
151:- **Progress toward fusion breakeven (Wurzel & Hsu 2021)** at `knowledge/meta_analysis/progress_toward_fusion_breakeven_lawson_criterion/`: Not read in this assessment. After opening: this meta-analysis covers achieved nτE across MCF, ICF, MIF. For HTS Compact Tokamak, it would benchmark SPARC's projected performance (estimated nτE ~10²⁰ keV·s/m³) against historical devices. However, the physics state-of-the-art for tokamaks is already thoroughly documented in concept-scoped sources. This source adds marginal value for §3 (maturity) but does not address any of the six important gaps. **Disqualified** for this assessment — does not cover ARC/SPARC economic or engineering parameters and adds no new information to any current gap.
```

## Forbidden-phrase check (should be empty)

```
(none — good)
```

## First line of new report (should start with `# Gap Assessment`)

```
# Gap Assessment: HTS Compact Tokamak (D-T)
```

## Blocking-tier lines (new)

```
134:| Tritium startup inventory (kg, cost) | truly-unknown | blocking | FLiBe extraction turnaround time uncharacterized; inventory could range from kg-tens of kg; cost $M–$B range. No ARC-specific published data. |
```

## Full unified diff (truncated to 400 lines)

```diff
--- /tmp/gap_phase2_state/01-hts-compact-tokamak.md	2026-05-22 12:59:21.055252424 -0700
+++ /home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/01-hts-compact-tokamak/gap_report.md	2026-05-22 13:05:55.156252143 -0700
@@ -1,10 +1,8 @@
-I now have sufficient information from all sources to write the complete gap assessment.
-
 # Gap Assessment: HTS Compact Tokamak (D-T)
 
 ## Overall Readiness
 **Rating**: Mostly Ready
-**Summary**: The CFS/ARC concept is one of the best-documented private fusion concepts in existence. The 2015 ARC conceptual design provides full physics and preliminary economics; the 2025 MIT/ARAI TEA study (read via `knowledge/sources/tea_dt_mfe_cost_analysis/`) delivers an ARC-based LCOE estimate of $140–550/MWh directly applicable to this concept. No blocking gaps exist — all five D1+ sections can be written with data in hand. Seven important gaps remain, primarily around operating costs, blanket replacement scheduling, the power cycle commitment, and Li-6/tritium startup supply chain.
+**Summary**: CFS/ARC is among the most thoroughly documented fusion concepts: a full conceptual design paper, dedicated NOAK TEA study modeled directly on ARC, power conversion cycle analysis, and a complete physics basis published in the J. Plasma Phys. 2020 special issue. All five D1+ qualitative sections can be written with good-to-partial coverage. One blocking gap (tritium start-up inventory cost, dependent on unvalidated FLiBe extraction rates) and six important gaps (detailed CAS breakdown, capacity factor, blanket replacement schedule, FLiBe T-extraction at scale, divertor design, first-wall/VV fusion-neutron lifetime) limit quantitative precision but do not prevent a first-pass analysis. Proceed to full analysis.
 
 ---
 
@@ -13,140 +11,149 @@
 ### 1. Availability of Data
 **Coverage**: Good
 
-**Available**: CFS has produced an unusually rich public literature for a private company. The 2015 Sorbom et al. ARC paper (`arc-reactor-specifications.md`, 172 KB) provides a peer-reviewed conceptual design covering plasma physics, magnets, blanket, neutronics, and a preliminary materials costing. The 2020 SPARC special issue (J. Plasma Physics, referenced in dossier but not extracted) deepens the physics basis. Colliva et al. 2024 (`arc-power-conversion-studies.md`) independently analyzed three power conversion cycles for ARC. The Schwartz et al. 2024 paper (`arxiv-2405-01514.md`) quantifies maintenance value and parasitic loads for fusion plants in decarbonized grids. The MIT ARAI study (2025, `knowledge/sources/tea_dt_mfe_cost_analysis/output.md`) is an ARC-based LCOE TEA estimating $140–550/MWh and $8,800–22,200/kW overnight capital costs. CFS press releases confirm SPARC under construction (first plasma 2027), ARC site in Chesterfield, Virginia, 400 MWe output, Google/Eni PPAs fully subscribing capacity.
-
-**Missing**: Updated commercial-scale ARC design parameters (400 MWe, as opposed to the published 200–250 MWe from 2015) are not in a peer-reviewed source — only press releases. The SPARC special issue papers (Creely et al. 2020 and the full set of 2020 JPP subsystem papers) are referenced in the dossier but not extracted as sources.
+**Available**:
+- **Full ARC conceptual design** (Sorbom et al. 2015, `arc-reactor-specifications.md`): 30+ pages covering plasma physics, magnets, blanket/neutron shielding, heating systems, and Section 6 rough costing (~$5.56B total fabricated cost by material-volume scaling, versus ~$24B ITER by same method). Plasma parameters, engineering constraints, and R&D requirements all documented.
+- **SPARC overview** (Creely et al. 2020, referenced in dossier): device parameters including B_t=12.2 T, R=1.85 m, a=0.57 m, Q≥2 target. SPARC construction confirmed under way, first magnet installed January 2026 per `cfs-2025-2026-updates.md`.
+- **Power conversion analysis** (`arc-power-conversion-studies.md`, Colliva et al. 2024, Sapienza/Eni): GateCycle™ simulation of three cycles for ARC FNSF phase (645 MW_th input). Rankine: 46% net efficiency, 297 MWe net. CO₂ Brayton: 40.3%. He Brayton: 32%. Rankine identified as most promising on efficiency and commercial availability.
+- **ARC original Brayton baseline** (`arc-reactor-specifications.md`): He Brayton at 900 K → 40% efficiency (190 MWe, FNSF), up to 50% efficiency at 1200 K (261 MWe, aggressive pilot).
+- **Dedicated NOAK TEA** (`knowledge/sources/tea_dt_mfe_cost_analysis/output.md`, Araiinejad & Shirvan 2025, MIT Applied Energy): ARAI-FPP is explicitly a 350 MWe tokamak modeled on the MIT ARC concept. NOAK overnight capital costs $8,800–$22,200/kW; LCOE $140–$550/MWh. Finds fusion reactor equipment is dominant cost driver, consistent with ARC Section 6.
+- **REBCO tape supply chain** (`sciencedirect-science-article-pii-s2772830725000390.md`): PLD-REBCO at >200 A/4mm @20 K, 20 T; current pricing $20/m; global production >3,000 km/yr-12 mm (>50% of world HTS wire output). Directly constrains ARC magnet cost modeling.
+- **Li-6 supply paper** (`sciencedirect-science-article-pii-s092037961930835x.md`): European DEMO-oriented ICOMAX process for Li-6 enrichment; confirms Li-6 is not commercially available at required scale.
+- **Costing methodology** (`arxiv-2601-21724.md`, Woodruff 2026, pyFECONs framework; `arxiv-2602-19389.md`, CATF IWG 2026): Both read. The CATF paper explicitly covers HTS magnet cost modeling as Account 22.1.3 "swap-point" for MFE, with TRL-based maturity uncertainty and learning-rate uncertainty propagation. Provides methodology to build an ARC-like cost model. Cited FOAK LCOE range for compact tokamaks: 150–200 $/MWh; NOAK at 60–100 $/MWh.
+- **ARPA-E ALPHA revisit** (`knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/output.md`): CAS-level cost breakdown for four compact MIF concepts (~500 MWe). Average total capital cost $1.2B; BOP structure (CAS 21, 22.2, 22.5, 23, 24, 25, 26) provides analogues applicable to ARC. Note: CAS 22.1.3 coils average only $5.9M because these are non-magnet concepts — magnet costs not transferable. Fuel processing (CAS 22.5) average $124M is applicable.
+- **Maintenance optimization study** (`arxiv-2405-01514.md`, Schwartz et al. 2024): Tokamak maintenance strategy valuation in decarbonized US grid. Uses 85% net/gross ratio (5% active + 10% passive parasitic); shows 80% availability retains 87–91% of capacity value. Provides quantitative framework for ARC capacity factor assumption.
+
+**Missing**:
+- Current ARC commercial design (400 MWe, Virginia site) not yet fully published by CFS — proprietary
+- CFS has not disclosed detailed capital cost breakdown for ARC by subsystem — proprietary
 
 **Gaps**:
-- Updated commercial ARC design (400 MWe) not published in peer-reviewed literature — proprietary — important
-- SPARC 2020 subsystem papers not extracted — not-yet-sourced — nice-to-have (ARC 2015 + ARAI 2025 cover the needed scope)
+- Detailed CAS cost breakdown for ARC/SPARC from CFS — proprietary — important
+- Post-2021 ARC design documentation (evolved from 200→400 MWe) — proprietary — important
 
 ---
 
 ### 2. Challenges in Capturing System Function
-**Coverage**: Good
-
-**Available**: The ARC paper explicitly documents open R&D challenges (Section 7): I-mode confinement scaling to burning plasma, 8 GHz LHCD system not yet demonstrated (industry standard is 6 GHz), REBCO demountable joint performance at full scale, FLiBe tritium extraction timescales not demonstrated at commercial scale, radiation-assisted corrosion of Inconel in FLiBe under neutron flux, and vacuum vessel/blanket materials behavior. Disruption management is flagged: ARC's small size means high thermal quench loading per unit area. The I-mode confinement requirement (H98=2.8, approximately 40% above standard H-mode) is required but relies on extrapolated scaling from Alcator C-Mod, whose operating point at 5.4T is far from ARC's 9.2T.
-
-Power conversion system uncertainty is well-characterized: the ARC 2015 baseline used a He Brayton cycle at 40–50% efficiency (900–1200 K blanket temp phases); Colliva et al. 2024 found supercritical steam Rankine is the better choice for the FNSF phase, but CFS has not publicly committed to a cycle for the commercial plant. The pulsed/quasi-steady nature (burns of "tens of minutes") requires an energy storage system (ESS) in the intermediate FLiBe circuit to smooth grid output — Colliva 2024 identifies this but does not model its cost.
+**Coverage**: Partial
 
-**Missing**: No quantified sensitivity analysis for confinement degradation paths (what does LCOE look like at H98=2.2 vs. 2.8?). ESS sizing and cost not published.
+**Available**:
+- **I-mode confinement uncertainty**: ARC paper explicitly quantifies sensitivity to H₉₈ (design point H₉₈~2.8, well above standard H-mode ~1.0; FNSF mission achievable at H₈₉~2.2). ARC exploits weak degradation of I-mode with heating power (τ_E ∝ P_heat^−0.27 vs. H-mode −0.69). Physics arguments for achievability documented, but I-mode at ARC scale is extrapolated from C-Mod.
+- **Non-inductive scenario**: ACCOME code modeling of bootstrap (63%) + LHCD (25 MW) + ICRF (13.6 MW) combination; sensitivity analysis shows self-consistent operating point accessible. SPARC ICRF design documented in `sparc-icrf-heating-paper.md` at SPARC-specific parameters (120 MHz, 25 MW, 3He minority + 2nd harmonic T).
+- **FLiBe blanket complexity**: ARC paper discusses: (a) magnetic field effects on FLiBe flow/heat transfer are computationally investigated but not experimentally validated in fusion environment; (b) radiation-assisted corrosion of Inconel 718 in FLiBe not tested in D-T environment; (c) tritium extraction turnaround time not experimentally established at required scale.
+- **Pulsed operation / grid integration**: Colliva 2024 paper explicitly includes energy storage system (ESS) in FLiBe intermediate circuit to provide constant turbine load during dwell phases. ESS architecture identified but sizing not costed.
+- **Demountable joints**: ARC paper identifies joints as key R&D item; bench-top tests exist but reactor-level fields (23 T, ~8 MA) not yet demonstrated. PIT VIPER (pulsed magnet technology) now demonstrated at CFS for PF/CS.
+
+**Missing**:
+- Divertor design: explicitly deferred in ARC 2015 paper ("left for later study"). No divertor design published.
+- Quantitative disruption frequency and mitigation design: qualitative discussion only
+- Quantitative tritium extraction turnaround time from FLiBe
 
 **Gaps**:
-- Final power conversion cycle not committed by CFS — proprietary — important
-- ESS cost for quasi-steady → steady grid output not quantified in any source — not-yet-sourced — important
-- I-mode confinement extrapolation uncertainty not propagated into cost/LCOE uncertainty — derivable — important
-- 8 GHz LHCD system technology readiness not demonstrated — truly-unknown (lab scale only) — nice-to-have (this affects O&M not capital cost directly)
+- Divertor design: heat exhaust at ARC power density (~30 MW/m² scrape-off) — not-yet-sourced (no ARC divertor paper published) — important
+- FLiBe tritium extraction rate / inventory requirements — truly-unknown at ARC scale — important
+- I-mode scaling from C-Mod to ARC (x5 linear scale-up) — derivable (using published scaling + uncertainty bounds) — important
+- ESS (thermal storage) cost and sizing for pulsed operation — not-yet-sourced — nice-to-have
 
 ---
 
 ### 3. Maturity of Key Subsystems and Components
-**Coverage**: Good
-
-**Available**: TRL assessments can be constructed from the ARC paper and SPARC updates:
-- **HTS REBCO TF magnets**: TRL 5–6. 20 T large-bore magnet demonstrated September 2021 (CFS milestone). SPARC is the first full coil system build. Demountable joints tested at bench scale; full-reactor-scale joints not yet demonstrated.
-- **FLiBe liquid immersion blanket**: TRL 3–4. FLiBe chemistry well-characterized from molten salt fission reactor programs. Tritium extraction from FLiBe not demonstrated at reactor-relevant flow rates; MCNP shows TBR ≥ 1.1 achievable.
-- **ICRF heating (primary)**: TRL 7–8 for the technology class; SPARC-specific 120 MHz / 25 MW system under development.
-- **LHCD (current drive)**: TRL 5 at 8 GHz. Industry standard klystrons operate at 6 GHz; 8 GHz not yet demonstrated.
-- **First wall / vacuum vessel (Inconel 718)**: TRL 3–4 in fusion neutron environment. Static corrosion in FLiBe tested at 873 K; radiation-assisted corrosion unknown. VV lifetime ~6–12 months per ARC MCNP (Table 9: inner VV at 44 DPA, 280 ppm He in 1 FPY).
-- **Blanket tank**: TRL 3–4. Estimated lifetime 1 FPY (limited by helium production rate for rewelding).
-- **TF coil neutron lifetime**: ≥9 FPY per ARC MCNP.
-- **Power conversion (steam Rankine with FLiBe intermediate loop)**: TRL 5. Steam Rankine itself is TRL 9; integration with FLiBe intermediate circuit is novel.
+**Coverage**: Partial
 
-**Missing**: Detailed TRL assessment for divertor (explicitly left open in ARC 2015). Tritium processing system for FLiBe at power plant scale.
+**Available**:
+- **HTS TF magnets (TRL 5–6)**: 20 T large-bore REBCO magnet demonstrated September 2021; SPARC TF coils manufactured and first one installed January 2026. Full-scale demountable joint demonstration pending SPARC assembly.
+- **ICRF heating system (TRL 6–7)**: SPARC ICRF fully designed (`sparc-icrf-heating-paper.md`); 120 MHz fast wave system based on C-Mod heritage; 25 MW specified; megawatt-level RF sources within reach of present technology. Antenna impurity control addressed.
+- **REBCO tape production (TRL 7–8)**: $20/m, >3,000 km/yr global supply, PLD process well established (`sciencedirect-science-article-pii-s2772830725000390.md`). Adequate for SPARC; ARC fleet would require significant scale-up.
+- **Thermal power conversion (TRL 7–8)**: Supercritical steam Rankine cycle is commercial technology; Colliva 2024 confirms no new turbine technology needed for ARC FNSF phase.
+- **PF/CS magnets (TRL 5)**: PIT VIPER pulsed superconducting technology demonstrated by CFS for pulsed poloidal coils.
+
+**Missing**:
+- FLiBe blanket integrated with fusion neutron flux: TRL 2–3. The LLNL TBB assessment (`osti-servlets-purl-1305833.md`) covers DCLL blanket for generic MFE tokamak — not FLiBe specific. FLiBe has fission reactor heritage (MSRE, AHTR studies) but no fusion-integrated test.
+- Tritium extraction from FLiBe at scale: TRL 2–3. ARC paper cites only two references for possible extraction schemes; LLNL report notes no experiments have been built to assess turnover time.
+- Vacuum vessel/first wall (Inconel 718) in D-T neutron environment: TRL 3. REBCO fluence limit conservatively 9 FPY per MCNP; but Inconel 718 chromium transport under radiation-assisted corrosion in FLiBe uncharacterized.
+- LHCD at 8 GHz: TRL 4 (standard klystron sources at 5–6 GHz; 8 GHz not yet demonstrated). JAERI LHCD review (`osti-etdeweb-servlets-purl-10149275.md`) covers existing LHCD physics but does not address 8 GHz system specifically.
+- Remote maintenance with demountable coils at reactor scale: TRL 3–4 (concept demonstrated at bench scale with Vulcan, full-reactor demount pending SPARC)
 
 **Gaps**:
-- Divertor design and cost not published — not-yet-sourced — nice-to-have
-- REBCO performance under fusion neutron fluence (cumulative REBCO never tested to failure) — truly-unknown — important (bounds magnet lifetime and replacement cost)
-- Tritium extraction from FLiBe at power plant scale — truly-unknown — important
+- FLiBe blanket integrated test in fusion neutron environment — truly-unknown — important
+- Tritium extraction from FLiBe at required throughput — truly-unknown — important (relates to blocking gap §5)
+- First wall / Inconel 718 fusion neutron + FLiBe compatibility — truly-unknown — important
+- 8 GHz LHCD klystron demonstration — not-yet-sourced — nice-to-have
+- Demountable joint operation at 23 T, reactor scale — not-yet-sourced (SPARC will validate) — important
 
 ---
 
 ### 4. Key Materials and Supply Chain Considerations
 **Coverage**: Partial
 
-**Available**: The ARC paper (Table 10) provides 2014 material costs: REBCO tape $36–198/m depending on volume; FLiBe $154/kg; beryllium $257/kg; Inconel 718 $56/kg; TiH₂ $26.4/kg; tungsten $29/kg. ARC requires 5,730 km of REBCO tape, ~950 tonnes of FLiBe in blanket + heat exchanger, 3.82 tonnes of beryllium in the multiplier, and 380 tonnes of TiH₂. CFS has internalized REBCO production (producing its own tape for SPARC magnets). Beryllium neutron multiplier is expensive (~$990k materials, $4.1M fabricated) and health-hazardous, limiting suppliers. Structural materials (Inconel, SS316LN, copper) have established global supply chains.
-
-**Missing**: Li-6 enrichment supply chain not characterized in any source. Natural lithium is only ~7.5% Li-6; FLiBe for a commercial plant requires enriched Li-6 to achieve TBR ≥ 1.1. The enrichment capacity available globally (primarily from ORNL isotope separation and Russia) is not sized against ARC commercial deployment needs. Tritium startup supply is not addressed: D-T plants need ~2–3 kg tritium at first fire, available only from operating fission reactors (CANDU fleet depleting over time).
+**Available**:
+- **REBCO tape**: $20/m, >3,000 km-12mm/yr global production (`sciencedirect-science-article-pii-s2772830725000390.md`). PLD process provides excellent in-field performance (>200 A/4mm @ 20 K, 20 T). Challenges remain in further cost reduction and process stability. ARC tape inventory is large but manageable given current production rates.
+- **FLiBe (LiF-BeF2)**: Long heritage from molten salt fission research (MSRE, AHTR). LiF is a commodity chemical. BeF2 production is specialty; beryllium sourcing (US and Kazakhstan producers) has well-characterized constraints.
+- **Li-6 enrichment**: Not commercially available at DEMO/ARC fleet scale (`sciencedirect-science-article-pii-s092037961930835x.md`). ICOMAX (mercury amalgam) process proposed as path for DEMO supply; requires decade-scale lead time. Current lithium isotope separation capacity insufficient for fleet deployment.
+- **Inconel 718 (vacuum vessel)**: Commercially available, well-characterized at ambient and elevated temperatures. ARC paper notes high nickel content increases activation — important for waste classification.
+- **TiH2 (neutron shielding)**: Powder form; ARC paper notes limited experimental data in fusion environment.
+
+**Missing**:
+- REBCO tape scale-up for full ARC fleet (single ARC unit likely requires >100–200 km tape given SPARC scale); learning curve data at fleet scale
+- Beryllium sourcing and BeF2 availability for FLiBe inventory (full blanket + heat exchanger = ~500 m³ per ARC)
+- Tritium startup inventory supply: natural production from CANDU reactors and fission is limited; ARC-scale startup inventory requirements unknown pending FLiBe extraction data
 
 **Gaps**:
-- Li-6 enrichment supply and cost at commercial scale — not-yet-sourced — important
-- Tritium startup inventory source and cost (~$30,000/g → ~$60–90M for startup) — not-yet-sourced — important
-- REBCO tape at-scale production cost trajectory (CFS currently producing internally; cost-down curve not published) — proprietary — important
-- Beryllium supply concentration risk (toxic, ~3 major suppliers globally) — not-yet-sourced — nice-to-have
+- BeF2 supply chain at ARC fleet scale — not-yet-sourced — important
+- Li-6 enrichment at ARC fleet scale (ICOMAX not yet commercial) — derivable (DEMO studies apply) — important
+- Tritium startup procurement timeline and cost — truly-unknown (depends on FLiBe extraction rate and therefore inventory size) — blocking (contributes to §5 blocking gap)
+- REBCO tape fleet manufacturing scale-up cost trajectory — derivable (use learning rate from PLD paper + pyFECONs) — nice-to-have
+- Activated FLiBe waste management / classification — derivable — nice-to-have
 
 ---
 
 ### 5. LCOE Parameter Extraction
-**Coverage**: Partial
-
 **Available Parameters**:
 | Parameter | Value/Range | Source | Confidence |
 |-----------|-------------|--------|------------|
-| Fusion power | 525 MW | `arc-reactor-specifications.md` (ARC 2015, Table 1) | h |
-| Plasma gain Qp | ~13.6 | `arc-reactor-specifications.md` (ARC 2015) | h |
-| On-axis B field | 9.2 T | `arc-reactor-specifications.md` (ARC 2015) | h |
-| Major radius | 3.3 m | `arc-reactor-specifications.md` (ARC 2015) | h |
-| Gross thermal output | ~645 MWth (FNSF pulse phase) | `arc-power-conversion-studies.md` (Colliva 2024) | m |
-| Thermal efficiency | 40% (He Brayton, 900K) / 40.3% (sCO2) / 41.5% (steam, Colliva best) | `arc-power-conversion-studies.md`; `arc-reactor-specifications.md` | m |
-| Net electrical output | 190–261 MWe (ARC 2015) / 400 MWe (current CFS plans) | `arc-reactor-specifications.md`; `cfs-2025-2026-updates.md` | m |
-| REBCO tape length needed | 5,730 km | `arc-reactor-specifications.md` (ARC 2015, Table 11) | m |
-| REBCO tape cost | $36–198/m (volume-dependent, 2014 USD) | `arc-reactor-specifications.md` (ARC 2015, Table 10) | m |
-| Magnet/structure fabricated cost | $5.1–5.2B | `arc-reactor-specifications.md` (ARC 2015, Table 11, crude scaling) | l |
-| Blanket fabricated cost | ~$260M | `arc-reactor-specifications.md` (ARC 2015, Table 11) | l |
-| Replaceable VV fabricated cost | ~$92M per replacement | `arc-reactor-specifications.md` (ARC 2015, Table 11) | l |
-| Total reactor fabricated cost (excl. BOP) | $5.5–5.6B (FY2014, crude scaling) | `arc-reactor-specifications.md` (ARC 2015) | l |
-| Overnight capital cost (ARC-based TEA) | $8,800–22,200/kW for 350 MWe | `knowledge/sources/tea_dt_mfe_cost_analysis/output.md` (ARAI/MIT 2025) | m |
-| LCOE (ARC-based TEA) | $140–550/MWh | `knowledge/sources/tea_dt_mfe_cost_analysis/output.md` (ARAI/MIT 2025) | m |
-| Compact modular fusion CAS LCOE analog | 43 $/MWh avg ($34–54) for ~500 MWe | `knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/output.md` (Woodruff 2020) | l (different concepts) |
-| Tritium breeding ratio | ≥1.1 (up to ~1.22) | `arc-reactor-specifications.md` (ARC 2015) | h |
-| TF coil neutron lifetime | ≥9 FPY | `arc-reactor-specifications.md` (ARC 2015, neutronics) | m |
-| Inner VV lifetime | ~6–12 months before replacement (1 FPY DPA limit) | `arc-reactor-specifications.md` (ARC 2015, §5.6) | l |
-| External heating power | 38.6 MW (25 MW LHCD + 13.6 MW ICRF) | `arc-reactor-specifications.md` (ARC 2015) | h |
-| Parasitic recirculating power | ~5% active + ~10% passive = 15% gross | `arxiv-2405-01514.md` (Schwartz 2024, generic fusion plant proxy) | m |
-| Maintenance value (80% availability) | ~91% of maintenance-free plant value | `arxiv-2405-01514.md` (Schwartz 2024) | m |
+| Fusion power | 525 MW (ARC 2015) | `arc-reactor-specifications.md`, Table 1 | h |
+| Plasma gain Q_p | ~13.6 | `arc-reactor-specifications.md`, abstract | h |
+| Net electric output | 190–261 MWe (2015 design); 400 MWe (current target) | ARC paper §2; `cfs-2025-2026-updates.md` | m |
+| On-axis field B₀ | 9.2 T (ARC); 12.2 T (SPARC) | ARC paper Table 1; `sparc-icrf-heating-paper.md` | h |
+| Thermal efficiency (He Brayton, FNSF) | ~40% (900 K outlet) | `arc-reactor-specifications.md` §2 | m |
+| Thermal efficiency (Rankine, FNSF) | 46% net (645 MW_th in) | `arc-power-conversion-studies.md`, Table 6 | m |
+| Blanket TBR | ≥1.1 (baseline); up to 1.22 | ARC paper §5 | h |
+| Bootstrap fraction | 63% | ARC paper §3.4 | h |
+| REBCO tape price | ~$20/m | `sciencedirect...s2772830725000390.md` | m |
+| Component fabricated cost (2015 scaling) | ~$5.56B total | ARC paper §6 | l |
+| NOAK overnight capital cost (ARC-based) | $8,800–$22,200/kW | `tea_dt_mfe_cost_analysis/output.md`, Araiinejad 2025 | m |
+| NOAK LCOE (ARC-based) | $140–$550/MWh | `tea_dt_mfe_cost_analysis/output.md`, Araiinejad 2025 | m |
+| FOAK LCOE (compact tokamaks, industry) | 150–200 $/MWh | `arxiv-2602-19389.md` §2.1.5 | l |
+| Fuel processing (CAS 22.5) analogue | ~$124M | `knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/output.md` | l |
+| O&M costs analogue | ~$48M/yr | `knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/output.md` | l |
+| Optimal maintenance availability | 75–85% | `arxiv-2405-01514.md`, Schwartz 2024 | m |
+| First wall lifetime (TF coil fluence limit) | ≥9 FPY | ARC paper §5.2 | l |
 
 **Missing Parameters**:
 | Parameter | Gap Type | Criticality | Notes |
 |-----------|----------|-------------|-------|
-| Commercial ARC CAS-level cost breakdown (400 MWe) | proprietary | important | CFS has not published; ARAI 2025 ($8800-22200/kW) is best available proxy for 350 MWe |
-| O&M costs specific to ARC | not-yet-sourced | important | ARPA-E ALPHA analog gives ~$48M/yr for ~500 MWe but those are MIF concepts with different cost drivers; ARC O&M dominated by VV/blanket replacement schedule |
-| Capacity factor / availability | derivable | important | ARC 2015 gives VV lifetime ~6–12 months, blanket tank ~1 FPY; overall availability derivable ~75–90%; Schwartz 2024 provides maintenance optimization framework |
-| VV and blanket replacement duration (downtime) | not-yet-sourced | important | ARC's demountable coil concept enables faster VV swap than sector maintenance, but swap time not published for commercial ARC scale |
-| Energy storage system cost for quasi-steady operation | not-yet-sourced | important | Colliva 2024 identifies ESS requirement for grid-smooth output but does not model its capital cost; could be 5–15% adder to BOP |
-| Li-6 enrichment cost and commercial supply | not-yet-sourced | important | Required for FLiBe blanket TBR ≥ 1.1; supply chain sizing vs. commercial ARC fleet not characterized |
-| Tritium startup inventory cost | not-yet-sourced | important | ~2–3 kg at ~$30,000/g = $60–90M one-time; CANDU availability declining |
-| FOAK construction and contingency premium | derivable | important | ARAI 2025 LCOE range ($140–550/MWh) captures this via regulatory/manufacturing scenario spread; not decomposed |
-| Divertor design and cost | not-yet-sourced | nice-to-have | Explicitly left open in ARC 2015; rough estimate $17.5M (tungsten, materials scaling) |
-| Decommissioning cost | derivable | nice-to-have | Low activation advantage of liquid blanket; rough estimate from fission analogs |
-| Updated REBCO production cost trajectory | proprietary | nice-to-have | CFS self-producing tape; learning curve rate not published |
+| Tritium startup inventory (kg, cost) | truly-unknown | blocking | FLiBe extraction turnaround time uncharacterized; inventory could range from kg-tens of kg; cost $M–$B range. No ARC-specific published data. |
+| ARC-specific capacity factor | proprietary / derivable | important | CFS has not published; Schwartz 2024 supports 75–85% analogue assumption |
+| Detailed CAS breakdown for ARC | proprietary | important | Only total NOAK range known from Araiinejad 2025; subsystem allocation (magnets, blanket, BOP) requires inference from ARIES/pyFECONs framework |
+| Blanket replacement schedule / FPY lifetime | proprietary / derivable | important | FLiBe VV not published; 9 FPY TF fluence limit gives upper bound; actual schedule likely shorter |
+| FOAK vs. NOAK cost differential for ARC | derivable | important | Use pyFECONs CATF methodology and reference class forecasting (1.5–3× uplift) |
+| Divertor cost and replacement | not-yet-sourced | important | Divertor not designed in ARC 2015; no published ARC divertor cost estimate |
+| First wall / Inconel 718 replacement cost | truly-unknown | important | Radiation-assisted corrosion in FLiBe uncharacterized; lifetime uncertain |
 
 ---
 
 ## Source Recommendations
 
-- **ARC 2015 costing is intentionally crude** (volume-scaling from FIRE/BPX/PCASTS/ARIES-RS per unit mass at $1.06M/tonne). Search OSTI/arXiv for subsequent CFS-supported or MIT PSFC system studies refining the ARC costing — search "ARC reactor cost estimate 2020–2026" or "SPARC pilot plant economics". `unverified — confirm existence before searching`
-
-- **O&M costs for ARC-class tokamak**: The PROCESS systems code outputs for DEMO-class tokamaks include O&M components; Eurofusion published O&M cost breakdowns for DEMO. Search "DEMO operations and maintenance cost" in EUROfusion publications as an upper bound analog. Published; `confirmed source type`.
-
-- **Li-6 enrichment supply**: DOE isotope program reports and IAEA isotope production surveys cover enriched lithium supply. Search OSTI for "lithium-6 enrichment fusion supply." `unverified — confirm existence before searching`
-
-- **Tritium startup**: NRC/DOE tritium supply studies (e.g., Abdou et al. on tritium self-sufficiency) published in Fusion Engineering and Design. Search "tritium startup inventory fusion" on OSTI. `not-yet-sourced`
-
-- **Fleet-wide source integration notes**:
-  - `knowledge/sources/tea_dt_mfe_cost_analysis/output.md` (ARAI/MIT 2025) — **Integrated**. This is an ARC-based LCOE TEA (350 MWe "ARAI" concept). OCC $8,800–22,200/kW, LCOE $140–550/MWh. Direct cost driver is fusion reactor equipment (matches ARC magnets as dominant cost). Downgrade the CAS-breakdown gap from blocking → important (ARAI provides a usable proxy).
-  - `knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/output.md` (Woodruff 2020) — **Integrated as partial analog**. Contains full CAS breakdown for four MIF/MIE compact modular concepts at ~500 MWe: average LCOE 43 $/MWh ($34–54 range), CapEx ~2.4 $/W, O&M ~$48M/yr. These are magnetized target / Z-pinch concepts, not tokamaks — the 22.1.3 magnet account is minimal ($5.9M avg) vs. ARC's dominant magnet cost. Valid as methodology reference and lower-bound LCOE data point only. Does not resolve ARC-specific capital or O&M gaps.
-  - `knowledge/sources/overview_of_the_helios_design_a_practical_planar_coil/output.md` — **Disqualified**. Stellarator design (Helios, 390 MWe, planar HTS coils). Different confinement geometry, different maintenance scheme, different blanket concept. Does not address any ARC-specific cost, materials, or physics gap.
-  - All IFE sources (`a_simplified_economic_model_for_inertial_fusion`, `energy_from_inertial_fusion`, `commercialization_of_laser_fusion_energy`, `affordable_manageable_practical_and_scalable_amps_high`, `economic_studies_for_heavy_ion_fusion_electric_power_plants`, `accelerators_for_inertial_fusion_energy_production`) — **Disqualified**. IFE driver/target economics are fundamentally different from MFE tokamak economics; none addresses ARC cost drivers, materials, or operating parameters.
-  - `knowledge/sources/an_assessment_of_the_economics_of_future_electric_power/output.md` — **Disqualified for gap resolution**. ORNL historical LCOE benchmarking paper; positions fusion against coal/nuclear/wind in a broad energy context. Does not provide ARC-specific cost data or close any identified gap.
-  - `knowledge/sources/aries_cost_account_documentation/output.md` — **Disqualified for direct integration** (not opened; applies only as methodology reference noted in pyFECONs papers already integrated). Covers CAS 20–27 and 90–98 algorithms; useful for CAS alignment in the analysis but not a source of ARC-specific quantitative values.
-  - `knowledge/meta_analysis/progress_toward_fusion_breakeven_lawson_criterion/output.md` — **Disqualified for LCOE gaps**. Wurzel & Hsu TRL/physics progress tracker. Useful for §3 TRL context but does not resolve any cost or operating parameter gap.
+- **ARC divertor design**: Search OSTI / J. Fusion Engineering and Design for "ARC divertor" or "high-field-side divertor compact tokamak 2020-2026." A 2022–2025 PSFC study may exist. `unverified — confirm existence before searching`
+- **FLiBe tritium extraction turnaround time**: Search for "FLiBe tritium extraction" in OSTI, IAEA, and molten salt fission literature (ORNL MSR heritage). ORNL TM reports on MSRE tritium behavior are partially applicable. `not-yet-sourced — ORNL CF-71-8-10 and related documents exist in archive`
+- **CFS ARC detailed cost study**: Commonwealth Fusion Systems has not publicly released a CAS-level breakdown. Monitor CFS publications and conference papers (EPS, IAEA FEC, SOFE) for ARC economic analyses. `proprietary — no public disclosure expected before ARC FOAK construction`
+- **REBCO tape learning curve for fusion scale**: Search IEEE Transactions on Applied Superconductivity and SuperPower/Fujikura production cost publications for learning-rate quantification. `not-yet-sourced`
+- **Li-6 supply at ARC fleet scale**: The ICOMAX paper (cited in §4 sciencedirect source) directly addresses DEMO-scale supply; also check IAEA DEMO tritium breeding studies. Already partially addressed by `sciencedirect-science-article-pii-s092037961930835x.md`.
+- **Progress toward fusion breakeven (Wurzel & Hsu 2021)** at `knowledge/meta_analysis/progress_toward_fusion_breakeven_lawson_criterion/`: Not read in this assessment. After opening: this meta-analysis covers achieved nτE across MCF, ICF, MIF. For HTS Compact Tokamak, it would benchmark SPARC's projected performance (estimated nτE ~10²⁰ keV·s/m³) against historical devices. However, the physics state-of-the-art for tokamaks is already thoroughly documented in concept-scoped sources. This source adds marginal value for §3 (maturity) but does not address any of the six important gaps. **Disqualified** for this assessment — does not cover ARC/SPARC economic or engineering parameters and adds no new information to any current gap.
 
 ---
 
 ## Summary
-
-Proceed to full analysis. The CFS/ARC concept has the richest publicly available dataset of any private fusion company, supported by a direct ARC-based TEA from MIT (2025) yielding LCOE $140–550/MWh. All five D1+ sections can be written with data in hand; the wide LCOE range ($140–550/MWh) is itself a key finding driven by regulatory and manufacturing assumption uncertainty, not by absent data. The seven important gaps (power cycle commitment, O&M, capacity factor, VV/blanket replacement schedule, Li-6 supply, tritium startup, ESS cost) should be addressed through stated assumptions with analog references rather than deferred to future sourcing.
+Proceed to full analysis. The HTS Compact Tokamak (D-T) has the richest public data of any advanced fusion startup concept: a full peer-reviewed conceptual design, a dedicated 2025 MIT TEA study explicitly modeled on ARC (Araiinejad & Shirvan), a power conversion cycle analysis (Colliva 2024), comprehensive SPARC physics basis papers, and the pyFECONs/CATF costing framework applicable to MFE HTS tokamaks. The one blocking gap — tritium startup inventory cost, gated on unpublished FLiBe extraction rates — can be handled in analysis by presenting a range using bounding assumptions from molten-salt fission experience. All other gaps are bridgeable with stated assumptions and fleet-wide analogues. The LCOE model can be constructed using: 400 MWe net output, 46% thermal efficiency (Rankine, Colliva 2024), $8,800–$22,200/kW capital cost (Araiinejad 2025), 75–85% capacity factor (Schwartz 2024 analogue), and ~$48–80M/yr O&M (ALPHA costing with HTS magnet cryo adder).
 
 ---
 
@@ -154,13 +161,13 @@
 
 ```yaml
 overall_rating: "Mostly Ready"
-blocking_count: 0
-important_count: 7
-counting_method: "all_sections_deduplicated — seven distinct important gaps: (1) power cycle not finalized, (2) commercial ARC O&M costs not published, (3) capacity factor/availability not published, (4) VV/blanket replacement duration and schedule, (5) ESS cost for quasi-steady operation, (6) Li-6 enrichment supply chain, (7) tritium startup inventory cost"
+blocking_count: 1
+important_count: 6
+counting_method: "all_sections_deduplicated — one blocking gap (tritium startup inventory cost, gated on unvalidated FLiBe extraction rate); six important gaps (detailed ARC CAS breakdown, ARC-specific capacity factor, blanket replacement schedule, FLiBe T-extraction at integrated scale, divertor design/cost, first wall / VV fusion-neutron lifetime)"
 section_coverage:
   availability_of_data:       "Good"
-  system_function:            "Good"
-  subsystem_maturity:         "Good"
+  system_function:            "Partial"
+  subsystem_maturity:         "Partial"
   materials_supply_chain:     "Partial"
   lcoe_parameter_extraction:  "Partial"
 ```
\ No newline at end of file
```
