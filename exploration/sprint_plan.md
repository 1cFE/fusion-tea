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

### 1b. Minimum Discriminating Set

### 1c. N/A Density Analysis

**Known issue — disguised N/As in Column 9 (Magnet Type):** The 1a schema encodes "no magnets" as the value `None (IFE)` rather than `N/A`, suppressing the N/A count for 10+ IFE concepts. The same logical pattern ("upstream choice makes this dimension structurally inapplicable") is encoded as `N/A` in other columns (Tritium Breeding for aneutronic fuels, Repetition Rate for steady-state). Phase 1c must either reclassify `None (IFE)` as N/A before measurement, or run the analysis both ways (as-encoded vs. corrected) to show the sensitivity. `Self-confined` (2 cells) is borderline — Z-pinch has self-generated magnetic confinement (real answer), but MTF pneumatic has no magnets at all.

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
