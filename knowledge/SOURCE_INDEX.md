# Source Index

Registered domain knowledge sources for the Fusion TEA investigation. Each source is extracted and stored locally. Sources are selected iteratively as the investigation identifies data needs (see `modeling_project/OVERVIEW.md`, Source Strategy).

Research questions (RQ-1 through RQ-5) are defined in `modeling_project/OVERVIEW.md`.

## Primary Sources

### PyFECONS
- **Type**: codebase
- **Location**: /home/reid/PyFECONS
- **Use for**: Reference implementation of fusion costing algorithms (MFE + IFE), CAS hierarchy implementation, LCOE computation, physics calculations. Serves RQ-1 (cost drivers), RQ-3 (shared vs. divergent structure — ~60% shared modules across reactor types).
- **Validation**: Compare model cost outputs against PyFECONS calculations for equivalent configurations

### TEA D-T MFE Cost Analysis
- **Type**: documentation
- **Location**: knowledge/sources/tea_dt_mfe_cost_analysis/
- **Use for**: TEA methodology for D-T MFE, detailed CAS cost breakdowns, LCOE calculation approach, fusion power plant economics. Serves RQ-1 (MFE cost drivers), RQ-2 (MFE LCOE range and assumptions).
- **Validation**: Compare cost model structure and assumptions against this reference study

#### Extended Metadata
- **Zotero Key**: 5428393:PMXLGPKG
- **Raw SHA256**: 58d6e64c6e822645ed30f81c570396b6a4f20a66c969f65cb599d6084644e68b
- **Extracted Path**: knowledge/sources/tea_dt_mfe_cost_analysis/
- **Extract SHA256**: 9d8a160c4dfe6cbe39c2e804979799d7f3b41d39bde983bd6d61c4830147ce63
- **Date Added**: 2026-02-08

### A simplified economic model for inertial fusion
- **Type**: documentation
- **Location**: knowledge/sources/a_simplified_economic_model_for_inertial_fusion/
- **Use for**: Monte Carlo exploration of 14 technology-agnostic LCOE parameters across IFE variants. Identifies which physics and target cost parameters drive economics. Serves RQ-1 (IFE cost drivers), RQ-2 (IFE LCOE ranges — competitive at ~$25/MWh under optimistic assumptions), RQ-5 (high-sensitivity parameters: gain, fusion energy per shot).
- **Validation**: Compare IFE parameter sensitivity rankings against our sensitivity-risk analysis

#### Extended Metadata
- **Zotero Key**: 5428393:LCZMWLYM
- **Raw SHA256**: 5a25c0e0e7978ad7a15f8087b7882c429aa93b52300d93cbc80be1c32b0149c7
- **Extracted Path**: knowledge/sources/a_simplified_economic_model_for_inertial_fusion/
- **Extract SHA256**: fabac3cfe8b198b9c9f228ecff46f87f770fe84aaf80823966af7ea8bfda1c7a
- **Date Added**: 2026-02-09

### Overview of the Helios Design: A Practical Planar Coil Stellarator Fusion Power Plant
- **Type**: documentation
- **Location**: knowledge/sources/overview_of_the_helios_design_a_practical_planar_coil/
- **Use for**: Preconceptual stellarator design (390 MWe, 6T HTS, planar coils). Exemplifies steady-state MFE architecture differences from tokamaks — natural stability, thick shielding, sector maintenance, relaxed manufacturing tolerances. Serves RQ-1 (stellarator cost drivers), RQ-3 (shared vs. divergent structure — stellarator vs. tokamak BOP/power core differences).
- **Validation**: Compare stellarator-specific subsystem assumptions against tokamak equivalents

#### Extended Metadata
- **Zotero Key**: 5428393:7E42ICWG
- **Raw SHA256**: 2fb8762385abe5804b812a6f65e2977c92be56a21f84f0b923e92ba39d476990
- **Extracted Path**: knowledge/sources/overview_of_the_helios_design_a_practical_planar_coil/
- **Extract SHA256**: d79a182e0612701a9691506037b81682dc6ad21abec871fa190c685ae7dce50f
- **Date Added**: 2026-02-09

### An Assessment of the Economics of Future Electric Power Generation Options and the Implications for Fusion
- **Type**: documentation
- **Location**: knowledge/sources/an_assessment_of_the_economics_of_future_electric_power/
- **Use for**: Historical ORNL assessment positioning fusion LCOE against competing power generation (coal, nuclear, wind, etc.). Establishes benchmarking framework and early maturity baseline for fusion cost estimates. Serves RQ-2 (LCOE credibility ranges in broader energy context), RQ-4 (cost estimation maturity — historical baseline).
- **Validation**: Compare contemporary fusion LCOE estimates against this historical benchmark

#### Extended Metadata
- **Zotero Key**: 5428393:XH2I672M
- **Raw SHA256**: 46840aa731c28627b769024aca23f09a22ccf5bfec122f9caf3f529390dae133
- **Extracted Path**: knowledge/sources/an_assessment_of_the_economics_of_future_electric_power/
- **Extract SHA256**: c82d4e1bb4b838b2b1472f50f32d0f86ff9650457b47224ca418888f5713a56a
- **Date Added**: 2026-02-09

### Revisit of the 2017 Costing for Four ARPA-E ALPHA Concepts
- **Type**: documentation
- **Location**: knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/
- **Use for**: Re-costing of four ARPA-E ALPHA modular fusion concepts using updated CAS assumptions and cost-sensitivity analysis. Reports ~$43/MWh average LCOE ($34-54 range) for ~500 MWe plants. Strongest multi-concept source — four different approaches costed in the same CAS framework. Serves RQ-1 (cost drivers across concepts), RQ-2 (LCOE ranges), RQ-3 (shared structure via common CAS), RQ-4 (estimation maturity with expert reviews), RQ-5 (sensitivity analysis included).
- **Validation**: Compare CAS-level cost breakdowns across the four concepts; validate our cross-concept methodology against theirs

#### Extended Metadata
- **Zotero Key**: 5428393:6I8Z5PBZ
- **Raw SHA256**: 4792c584b9e7a70cbbfa033471048694651e8b51d82b21f40879ff006b7b4067
- **Extracted Path**: knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/
- **Extract SHA256**: bcf0a9b20c8353f4b91d7a8397c7e358fb88b354205b78b96e9ee7b59a0d8e00
- **Date Added**: 2026-02-09

### ARIES Cost Account Documentation
- **Type**: documentation
- **Location**: knowledge/sources/aries_cost_account_documentation/
- **Use for**: Definitive reference for fusion CAS framework — accounts 20-27 (direct) and 90-98 (indirect), tracing lineage from Starfire (1980) through ARIES series. Documents standardized costing algorithms, escalation methodology, contingency conventions. Foundational for MR-1 (CAS hierarchy requirement). Serves RQ-1 (cost driver structure), RQ-3 (shared cost structure across approaches), RQ-4 (estimation maturity — documents methodology evolution over 30+ years).
- **Validation**: CAS category definitions in our models must align with this reference

#### Extended Metadata
- **Zotero Key**: 5428393:HJMWLC47
- **Raw SHA256**: dbf5fe5b4607465301cf3abdd9f77b72d8924c7bba1963b9cc92d6e47e4706c5
- **Extracted Path**: knowledge/sources/aries_cost_account_documentation/
- **Extract SHA256**: 7ab8d40958efd4dc1f03b7064bff2b111a05a2034a75cc5b75a7124d8c11eb71
- **Date Added**: 2026-02-09

### Economic studies for heavy-ion-fusion electric power plants
- **Type**: documentation
- **Location**: knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/
- **Use for**: Parametric economic studies for HIF electric power plants from LLNL. COE model as function of driver pulse rate, reactor/driver/target factory cost scaling, multi-unit plant economics. Key result: 1.5–3 GWe HIF plants competitive with nuclear/coal at 5–10 Hz. Serves RQ-1 (HIF cost drivers — driver cost dominates), RQ-2 (COE projections: 3.9–5.8 ¢/kWh range), RQ-5 (sensitivity to pulse rate, driver cost, target gain, conversion efficiency).
- **Validation**: Compare HIF cost scaling relationships against PyFECONS driver cost models

#### Extended Metadata
- **Zotero Key**: 5428393:GI92TAS2
- **Raw SHA256**: f5b969b9b56e4f45f8ba888538cf327afc224bafdb76407d117a0d15518fc63c
- **Extracted Path**: knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/
- **Extract SHA256**: 03abe48dd230228b993f56be468bd4c93d11c2a20602c55a2fee0c46355513e6
- **Date Added**: 2026-03-02

### Energy from Inertial Fusion
- **Type**: documentation
- **Location**: knowledge/sources/energy_from_inertial_fusion/
- **Use for**: Comprehensive 1992 review of IFE concepts, driver technologies (laser, heavy-ion, light-ion), target physics, and power plant designs. Covers the full IFE landscape at a pivotal moment in the program. Serves RQ-1 (IFE subsystem identification and cost structure), RQ-3 (shared vs. divergent structure across IFE driver types).
- **Validation**: Compare IFE subsystem taxonomy against our classification framework

#### Extended Metadata
- **Zotero Key**: 5428393:BQWVRWCF
- **Raw SHA256**: 43a69e2e540aeeb156b0477190428cd0da011916c5024fff99823f26e67238e6
- **Extracted Path**: knowledge/sources/energy_from_inertial_fusion/
- **Extract SHA256**: 91a6780ed4109abfeb80ad30be4ec6a0a937960290f3febbc2a871d9ea2002d8
- **Date Added**: 2026-03-02

### Accelerators for Inertial Fusion Energy Production
- **Type**: documentation
- **Location**: knowledge/sources/accelerators_for_inertial_fusion_energy_production/
- **Use for**: Review of accelerator technologies for IFE drivers — induction linacs, RF linacs, diode-pumped lasers — covering beam physics, target coupling, and technology readiness. Bridges the gap between driver R&D and power plant economics. Serves RQ-1 (driver cost as dominant IFE cost lever), RQ-3 (how driver choice shapes the rest of the plant architecture).
- **Validation**: Compare accelerator cost scaling models against HIF economics paper and PyFECONS

#### Extended Metadata
- **Zotero Key**: 5428393:VKWLFRFK
- **Raw SHA256**: 52e383bbe1d5edb98f6d3a523f3c4d16af69e9a0235fd8176205c551fde29af7
- **Extracted Path**: knowledge/sources/accelerators_for_inertial_fusion_energy_production/
- **Extract SHA256**: e05c712e0002dc71145793d93464a9bdc5b988121080fdb4e8f4752476167d53
- **Date Added**: 2026-03-02

### Affordable, manageable, practical, and scalable (AMPS) high-yield inertial fusion
- **Type**: documentation
- **Location**: knowledge/sources/affordable_manageable_practical_and_scalable_amps_high/
- **Use for**: Pacific Fusion's 2025 paper on high-yield pulser-driven IFE — physics basis for high gain (>100) at high yield (>1 GJ), practical engineering for rep-rated operation, and cost pathway to competitive electricity. Most current IFE plant design with explicit cost projections. Serves RQ-1 (modern IFE cost drivers), RQ-2 (contemporary IFE LCOE projections), RQ-5 (sensitivity to yield, rep rate, driver efficiency).
- **Validation**: Compare AMPS cost assumptions against Hawker's 14-parameter model and HIF economics

#### Extended Metadata
- **Zotero Key**: 5428393:WQVP4WBW
- **Raw SHA256**: 72bf241116109b969f8bfdede2c793909b7609d4756edcb7c4ae772de64c7589
- **Extracted Path**: knowledge/sources/affordable_manageable_practical_and_scalable_amps_high/
- **Extract SHA256**: 7492e1df4fee48030b86ba7fae868f296a063b96f634d66e81754e7c38c94d61
- **Date Added**: 2026-03-02

### Commercialization of laser fusion energy
- **Type**: documentation
- **Location**: knowledge/sources/commercialization_of_laser_fusion_energy/
- **Use for**: Xcimer Energy's 2026 whitepaper on laser IFE commercialization — KrF excimer laser architecture at <$100/J (vs. $700–1000/J for DPSSL), hybrid direct-drive targets, chamber design, and deployment roadmap. Only source with detailed laser cost breakdown by component. Serves RQ-2 (laser IFE cost pathway), RQ-4 (commercialization readiness and cost reduction trajectory).
- **Validation**: Compare Xcimer laser cost estimates against DPSSL baselines and NIF-derived scaling

#### Extended Metadata
- **Zotero Key**: 5428393:4PLGW7RA
- **Raw SHA256**: 13163ec4fa110042692ba31bebfc27bb9bf0967bcf88a5a699a4c8eb9d595956
- **Extracted Path**: knowledge/sources/commercialization_of_laser_fusion_energy/
- **Extract SHA256**: e5b23ab23f6d175920c54388e696ea4acd1f6eddf284dea1701cf7bc85c5849b
- **Date Added**: 2026-03-02

### Progress toward fusion energy breakeven and gain as measured against the Lawson criterion
- **Type**: documentation
- **Location**: knowledge/meta_analysis/progress_toward_fusion_breakeven_lawson_criterion/
- **Use for**: Wurzel & Hsu (ARPA-E, 2021, arXiv:2105.10954) — comprehensive peer-reviewed compilation of achieved Lawson parameter (nτ, nτE) and triple product (nTτE) values across MCF, ICF, and MIF experiments since 1955. Documents per-approach methodologies for inferring n, τ, T from experimental data. Serves RQ-4 (technology readiness — physics progress benchmark by concept), and provides cross-concept physics-state-of-the-art reference for the taxonomy (Stage 1).
- **Validation**: Compare claimed physics performance of modeled concepts against this peer-reviewed compilation

#### Extended Metadata
- **Source URL**: https://arxiv.org/pdf/2105.10954
- **Raw SHA256**: b7b3cdf0087ca3de0bdaff4127ef6cfae9718b4b367cc232264aac928fa4789c
- **Extracted Path**: knowledge/meta_analysis/progress_toward_fusion_breakeven_lawson_criterion/
- **Extract SHA256**: 44fdc3d0be2074443046df35cb0b285aa010d469b9057d3af3465d9b7d923dd8
- **Date Added**: 2026-05-15

### Concept Research Dossiers
- **Type**: research collection
- **Location**: knowledge/concept_research/
- **Use for**: Per-concept techno-economic research across 38 fusion concepts.
  Contains dossiers, source extractions (HTML/PDF with agentic-mbse), iteration
  history, and synthesis outputs. See `knowledge/concept_research/SOURCE_INDEX.md`
  for detailed per-concept source listing. Serves all RQs.

### Stellaris Design Paper (Lion et al. 2025) — KIT publikationen mirror
- **Type**: documentation
- **Location**: knowledge/concept_research/09-qi-stellarator-hts/iter-02/sources/publikationen-1000179851-172386752/ (PDF: tmpissrtbos/raw.pdf; page images: tmpissrtbos/images/)
- **Use for**: The published Stellaris design paper itself (Lion et al., Fusion Engineering and Design 2025, doi 10.1016/j.fusengdes.2025.114868) — ground-truth witness for the concept-09 QI stellarator demo model (WI-018/019/020/021/022/023). Settled the WI-023 extraction-phantom questions: "5.86" appears nowhere in the paper; Table 3 has no field row; there is no "conduction power to coils" row — 111 is stored magnetic energy in GJ. Serves RQ-1 and RQ-2 via the concept-09 demo model.
- **Validation**: Verify quantitative table values against the raw PDF or the page images directly. The iter-01 stellaris-design-details extraction's text tables are corrupted LLM reconstructions; any table value taken from an extraction must be re-checked here.
- **Caveat**: The extraction accompanying this mirror (iter-02 stellaris-paper-details) shares the same extraction lineage as iter-01 — its text tables repeat the identical phantom rows and must not be used as an independent witness. The PDF and page images are the authority.

#### Extended Metadata
- **Source Record**: KIT publikationen record 1000179851 (mirror of doi 10.1016/j.fusengdes.2025.114868)
- **Raw SHA256**: 7fd72c1242ce3a17a9c4b9a4597fcb9ff5296b942b2d8343a0b463539d8d3865
- **Raw Path**: knowledge/concept_research/09-qi-stellarator-hts/iter-02/sources/publikationen-1000179851-172386752/tmpissrtbos/raw.pdf
- **Date Added**: 2026-07-18

## How Sources Are Used

1. **Domain research** is conducted against extracted sources, producing DI-XXX entries in KNOWLEDGE.md
2. **Citations in models** use the `Source`/`Ref`/`Basis` format, pointing directly to file paths in `knowledge/sources/` (see MR-4 in REQUIREMENTS.md)
3. **Source selection is iterative** — new sources are ingested as research identifies data needs

### Source Types

- **codebase**: Source code with algorithms, formulas, implementations (Claude can read and analyze)
- **documentation**: PDFs, papers, design studies extracted via agentic-mbse v4 pipeline
- **database**: Data files, CSVs, parameter databases
- **reference**: Standards documents, textbooks, general reference

### Adding Sources

Sources flow through the Zotero → extract → register pipeline (see `scripts/zotero_ingest.py`). Sources can also be registered manually by editing this file and placing extracted documents in `knowledge/sources/`.
