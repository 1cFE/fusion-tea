# Fusion Concept Space Sprint Plan

**Duration**: ~2 weeks, split into two gated chunks
**Goal**: Build meaningful artifacts for categorizing fusion concepts, and test whether a flat morphological matrix is the right representation — or whether a richer structure (tree, graph) adds value for SysML modeling and concept exploration.

---

## Chunk 1: Empirical Test

**Gate**: Results determine whether Chunk 2 is worth the investment.

Deliverables:

### 1a. Completed Differentiation Table

A cited, controlled-vocabulary table covering all ~36+ fusion concepts across 12 differentiation columns (confinement family/concept, fuel, heating, energy capture, plasma state, magnet type, tritium breeding, neutron management, operation mode, repetition rate, driver technology). Every cell is filled, N/A with justification, or TBD with explanation. Per-cell citations and confidence ratings tracked in a separate registry.

**Plan**: [`exploration/phase_1a/sprint_plan_1a.md`](phase_1a/sprint_plan_1a.md)

**Exit criteria**:
- >85% of applicable cells filled (not TBD)
- >60% of filled cells have gold or silver citations
- 100% of N/A cells have structural justification
- Every row is uniquely distinguishable (no two identical)

### 1b+1c. Minimum Discriminating Set & N/A Density Analysis (Combined)

A combined computational analysis of the Phase 1a table. No LLM calls — pure Python script consuming `table.csv`.

**1b (Discriminating Set):** Find the minimum column subset that uniquely identifies all 38 concepts. Brute-force enumeration of all 2^12 = 4,096 column subsets, plus greedy ranking, per-column entropy, and confusion analysis (which concepts collapse when each column is removed).

**1c (N/A Density):** Measure the context-sensitivity of the design space. Per-column, per-row, and per-block N/A rates. Block structure detection (do N/As cluster by confinement family or fuel?). Structural N/A chain tracing. This is the empirical test of the core hypothesis from `context/context_dependent_design_spaces.md`.

**Data preparation:** Reclassify `None (IFE)` in Magnet Type (11 cells) as `N/A` — this is a disguised structural inapplicability. Original table preserved as frozen snapshot. `Self-confined` (3 cells: Z-pinch, MTF, DPF) kept as a real value with sensitivity noted.

**Plan**: [`exploration/phase_1b/sprint_plan_1b.md`](phase_1b/sprint_plan_1b.md)

**Exit criteria**:
- All minimum discriminating sets enumerated exhaustively
- N/A density computed with block structure (per-column, per-row, per-block)
- Core hypothesis answered with evidence (flat table vs. context-dependent)
- Implications for Phase 1d and Chunk 2 documented

### 1d. Qualitative Assessment
How well does the data in the different rows capture the concept — e.g. what the technique is most sensitive to, the hard problems people are working on, etc.

---

## Chunk 2: Prototype Representation

Deliverables:

### 2a. Tree or AND/OR Graph for 3 Concepts

### 2b. Cross-Concept Transfer Test
Can we find a sub-problem that appears on multiple branches and write a "pattern card"?

### 2c. Analysis Report
Do we see shapes forming?
