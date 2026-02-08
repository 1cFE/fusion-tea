# Source Index

This file tells MBSE commands where to find domain knowledge for fusion power plant modeling.

## Primary Sources

### PyFECONS
- **Type**: codebase
- **Location**: /home/reid/PyFECONS
- **Use for**: Fusion costing algorithms, physics calculations, economic models, LCOE computation, subsystem cost breakdowns
- **Validation**: Compare model cost outputs against PyFECONS calculations for equivalent configurations

### TEA D-T MFE Cost Analysis
- **Type**: documentation
- **Location**: knowledge/sources/tea_dt_mfe_cost_analysis/
- **Use for**: Techno-economic analysis methodology, D-T MFE cost breakdowns, LCOE calculation approach, fusion power plant economics
- **Validation**: Compare cost model structure and assumptions against this reference study

#### Extended Metadata
- **Zotero Key**: 5428393:PMXLGPKG
- **Raw SHA256**: 58d6e64c6e822645ed30f81c570396b6a4f20a66c969f65cb599d6084644e68b
- **Extracted Path**: knowledge/sources/tea_dt_mfe_cost_analysis/
- **Extract SHA256**: 9d8a160c4dfe6cbe39c2e804979799d7f3b41d39bde983bd6d61c4830147ce63
- **Date Added**: 2026-02-08

## How MBSE Commands Use This File

When you run commands like `/design-model` or `/audit-models`, they:

1. **Read this file** to discover what reference sources exist
2. **Explore sources** to find relevant patterns, formulas, parameters
3. **Validate outputs** by comparing against authoritative sources

### Source Types Explained

- **codebase**: Source code to extract patterns, formulas, implementations
  - Example: Reference implementation with physics calculations
  - Claude can read and analyze the code

- **documentation**: PDFs, papers, specs that define requirements or physics
  - Example: Design specification, academic paper
  - Claude can read if path is accessible

- **database**: Data files, CSVs, parameter databases
  - Example: Material properties, cost factors
  - Claude can read and extract values

- **reference**: General reference material
  - Example: Standards documents, textbooks
  - Provides context and definitions

### Adding More Sources

Use `/manage-sources` to add, remove, or update sources, or edit this file directly.

Good sources to consider for fusion modeling:
- ARIES studies and reports
- ITER design documentation
- Fusion power plant conceptual design studies
- Material property databases for fusion-relevant materials
