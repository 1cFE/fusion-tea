# Spec: Concept Taxonomy and Similarity

**Status:** Complete
**Owner:** Reid W
**Created:** 2026-03-29 15:01 PDT
**Complexity:** HIGH
**Branch:** ralph/concept-explorer

---

## Business Goals

### Why This Matters

The concept explorer currently shows individual concept economics (LCOE, CAS breakdowns, sensitivity analysis) but has no structured way to answer relational questions: "What is this concept like?", "Which concepts should I compare side-by-side?", and "Where exactly do two concepts diverge?" The taxonomy table (`table_v2.csv`) contains 38 fusion concepts described across 17 design columns — rich relational data locked in a flat CSV with no structured access, no typed models, and no computational layer.

The existing comparison view (Section 7.1 of README) is "structurally complete but analytically empty — it shows the same data twice, not the relationship between the data." This feature builds the analytical infrastructure to make comparisons that teach.

### Success Criteria

- [ ] SC-1: A user viewing any concept can see where it sits in the design-space hierarchy (decision tree) and which other concepts are its nearest neighbors by design similarity
- [ ] SC-2: Similarity is decomposed by functional dimension — a user can see "70% like concept A overall, but in the dimensions where they differ, more like concepts B and C"
- [ ] SC-3: The decision tree is navigable as an interactive visualization in the explorer UX, with concepts at leaf nodes
- [ ] SC-4: All 38 concepts from table_v2 are represented in the canonical registry with typed, validated attributes
- [ ] SC-5: The concept registry JSON and decision tree JSON are the single sources of truth — table_v2.csv is a seed, not an authority

### Priority

New exploratory infrastructure. Not blocking other work, but directly serves the "cross-concept comparison tooling" idea in the backlog. Relates to the broader investigation goal of enabling cross-concept comparison (RQ-3 in OVERVIEW.md).

---

## Problem Statement

### Current State

- **Taxonomy data** exists only as `exploration/phase_1b_v2/table_v2.csv` — a flat file with no schema, no validation, no API access
- **Concept explorer** has 4 analyzed concepts (04, 05, 06, 08) with cost models but no design-attribute data beyond `confinement_family`
- **Comparison view** aligns tornado charts side-by-side but provides no analytical guidance on *which* concepts to compare or *where* they differ
- **No similarity computation** exists — a user must manually scan the CSV to find related concepts
- **No decision tree** — the hierarchical structure (Family > Topology > Sub-type) is implicit in the CSV's N/A patterns, not explicit or navigable

### Desired Outcome

A structured data layer that makes the taxonomy computationally accessible: typed models for concept attributes, canonical JSON files as single sources of truth, a similarity engine that decomposes relatedness by functional dimension, and interactive visualizations (tree navigator, similarity cards, concept constellation) integrated into the explorer UX.

---

## Scope

### In Scope

1. **Pydantic data models** for concept taxonomy attributes (typed enums, structured fields)
2. **Concept registry** — canonical JSON (`data/concept_registry.json`) with all 38 concepts, seeded from table_v2.csv
3. **Decision tree** — canonical JSON (`data/decision_tree.json`) encoding the hierarchical classification structure
4. **Seed script** — one-time migration from table_v2.csv to the canonical JSON files
5. **Similarity engine** — Python module computing pairwise similarity with dimension decomposition
6. **API endpoints** — serve tree, registry, and similarity data to the frontend
7. **Interactive tree view** — collapsible decision tree visualization in the explorer
8. **Similarity visualizations** — similarity decomposition cards, concept constellation (2D scatter)
9. **Concept taxonomy cards** — new card type showing design attributes (distinct from existing cost-model cards, may merge later)

### Out of Scope

- Modifying existing cost model pipeline or extraction (`extract_explorer_data.py`)
- Modifying existing concept profile pages, tornado charts, CAS breakdowns, or slider recompute
- Automated ingestion from external data sources (registry is manually curated)
- Economic similarity (LCOE/capital cost comparisons) — this is *design attribute* similarity only
- Merging taxonomy cards with existing cost-model concept cards (deferred — may happen later)

### Edge Cases & Considerations

- **Multi-valued cells**: Some CSV values are compound ("RF + NBI", "LTS+HTS", "Hybrid (thermal + direct)"). The semantics (OR vs AND/hybrid) vary by column. Design MUST establish a pattern: lists for OR-alternatives, distinct values for true hybrids. Deferred to design phase.
- **TBD/Unknown values**: MUST be treated as missing data (excluded from similarity computation). These are gaps to be filled in later, not a meaningful category.
- **N/A values**: Structurally meaningful — they indicate a column does not apply to this concept's confinement family. MUST be distinguished from TBD/Unknown.
- **Sparse coverage**: Only 4 of 38 concepts have cost models in the explorer. Taxonomy cards MUST work for all 38, independent of whether a cost model exists.
- **Registry evolution**: The registry will be edited over time (correcting values, filling TBD, adding new concepts). The format MUST support human editing of JSON.

---

## Requirements

### Functional Requirements — Data Models

> Requirements below are from user's request unless marked [INFERRED].

1. **FR-1**: The system MUST define Pydantic models for concept taxonomy attributes with typed enums for semantically meaningful columns (ConfinementFamily, FuelType, etc.)

2. **FR-2**: The data models MUST enforce comparison consistency — where two concepts share a column, the values MUST be drawn from the same enum/vocabulary so that equality comparison is meaningful

3. **FR-3**: The models MUST distinguish between N/A (column does not apply), TBD/Unknown (column applies but value not yet determined), and actual values

4. **FR-4**: [INFERRED] The models MUST be sufficient to construct concept taxonomy cards — each card shows the concept's full set of design attributes with their typed values

### Functional Requirements — Sources of Truth

5. **FR-5**: The system MUST produce a canonical concept registry JSON file (`data/concept_registry.json`) containing all 38 concepts with their typed design attributes

6. **FR-6**: The system MUST produce a canonical decision tree JSON file (`data/decision_tree.json`) encoding the hierarchical classification (Family > Topology/Driver/Method > Sub-type) with concept IDs at leaf nodes

7. **FR-7**: The concept registry and decision tree JSON files MUST be the single sources of truth for taxonomy data. `table_v2.csv` is a seed artifact only.

8. **FR-8**: A seed script MUST perform the one-time migration from `table_v2.csv` to the canonical JSON files, applying the Pydantic models for validation

9. **FR-9**: The JSON files MUST be human-editable — format and structure SHOULD support direct editing for corrections, TBD resolution, and new concept additions

### Functional Requirements — Similarity Engine

10. **FR-10**: The system MUST compute pairwise similarity between all concepts using the cross-cutting design-choice columns (fuel, primary heating, energy capture, plasma state, magnet type, tritium breeding, neutron management, operation mode, repetition rate, driver technology)

11. **FR-11**: Similarity MUST be decomposed by functional dimension groupings:
    - **Plasma physics**: Fuel, Primary Heating, Plasma State
    - **Engineering**: Magnet Type, Energy Capture, Driver Technology
    - **Fuel cycle**: Tritium Breeding, Neutron Management
    - **Operations**: Operation Mode, Repetition Rate

12. **FR-12**: For any given concept, the system MUST produce a ranked list of most-similar concepts with per-dimension similarity scores

13. **FR-13**: For any pair of concepts, the system MUST identify the dimensions where they match and the dimensions where they differ, and for each differing dimension, identify which *other* concepts are most similar to the query concept in that dimension

14. **FR-14**: Similarity computation MUST exclude TBD/Unknown values (treat as missing data) and MUST exclude N/A values (column not applicable). Similarity is computed only over columns where both concepts have actual values.

15. **FR-15**: [INFERRED] The similarity engine MUST produce results as structured data (Pydantic models), not just raw matrices, so the API can serve them and the frontend can render them

### Functional Requirements — API

16. **FR-16**: The server MUST expose API endpoints to serve:
    - The decision tree structure
    - The concept registry (full or per-concept)
    - Similarity results for a given concept (nearest neighbors with decomposition)
    - The full similarity matrix (for constellation visualization)

### Functional Requirements — Visualizations

17. **FR-17**: The system MUST provide an interactive decision tree view:
    - Collapsible/expandable tree nodes
    - Concepts displayed at leaf nodes
    - Design-attribute annotations visible at leaves (compact badge strip showing key choices)
    - Integrated into the explorer UX (accessible from navigation)

18. **FR-18**: The system MUST provide a similarity decomposition card for each concept showing:
    - Top-N most similar concepts with overall similarity score
    - Per-dimension match/mismatch breakdown (e.g., "Plasma Physics: 3/3 match, Operations: 0/2 match")
    - For dimensions where the primary similar concept differs, which other concepts match in that dimension

19. **FR-19**: The system MUST provide a concept constellation visualization:
    - 2D scatter plot of all 38 concepts projected from the similarity matrix (MDS or UMAP)
    - Color-coded by confinement family
    - Interactive — click a concept to see its similarity card or navigate to its profile
    - Lines or proximity indicators to nearest neighbors

20. **FR-20**: The system MUST provide concept taxonomy cards:
    - One card per concept showing all design attributes from the registry
    - Distinct from existing cost-model cards (separate component, separate view context)
    - Sufficient to enable meaningful side-by-side comparison of design choices

---

## Acceptance Criteria

### Core Data Layer
- [ ] All 38 concepts from table_v2.csv are present in `data/concept_registry.json` with validated, typed attributes
- [ ] Decision tree JSON correctly encodes the full hierarchy with all concepts placed at appropriate leaf nodes
- [ ] Pydantic models validate the registry — loading the JSON through the models raises no errors
- [ ] Seed script successfully transforms table_v2.csv into both JSON files

### Similarity
- [ ] Pairwise similarity produces sensible results: concepts within the same sub-family (e.g., two QI stellarators) score highest; aneutronic concepts (p-B11 FRC, p-B11 laser, DPF) cluster across families
- [ ] Dimension decomposition correctly identifies which functional areas drive similarity and difference
- [ ] "In the dimensions where A and B differ, X is more like C" queries produce meaningful results
- [ ] TBD/Unknown values are excluded from similarity computation; N/A values are excluded as non-applicable

### Visualizations
- [ ] Decision tree renders as an interactive collapsible tree in the explorer
- [ ] Similarity cards show decomposed nearest-neighbor data for each concept
- [ ] Constellation plot renders all 38 concepts in 2D with family-colored points
- [ ] All visualizations are navigable — clicking a concept links to further detail

### Quality & Integration
- [ ] Existing tests continue to pass
- [ ] New Pydantic models have unit tests for validation, enum coverage, N/A/TBD handling
- [ ] Similarity engine has unit tests verifying known relationships (e.g., two tokamaks more similar than a tokamak and a laser IFE concept)
- [ ] Registry and tree JSON files are version-controlled and human-readable

---

## Related Artifacts

- **Seed data:** `exploration/phase_1b_v2/table_v2.csv`
- **Existing models:** `exploration/concept_explorer/models.py` (ConfinementFamily, FuelType enums already exist)
- **Existing explorer:** `exploration/concept_explorer/` (server, templates, JS components)
- **Phase 2a tree:** `exploration/phase_2a/tree.json` (different purpose — generative reasoning tree — but similar JSON tree structure)
- **Design:** `.project/active/concept-taxonomy-and-similarity/design.md` (to be created)

---

**Next Steps:** After approval, proceed to `/_my_design`
