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
