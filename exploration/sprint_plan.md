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

### 1b+1c v2. Confinement Hierarchy Restructuring

Phase 1b+1c found that Confinement Concept was a near-ID column (29 unique values for 38 rows), making the morphological analysis collapse to a lookup. The root cause: a hierarchical tree was crammed into a single flat column.

v2 replaces the 2 confinement columns (Confinement Family, Confinement Concept) with an 8-column hierarchical tree. Each column is a real morphological dimension — a genuine question with comparable values — that applies within its scope and is N/A outside it. The more granular the question, the more N/A density increases, directly measuring the context-dependence the flat table hid.

**Results**: Minimum discriminating set went from 2 → 4 columns (near-ID problem eliminated). N/A density went from 9.6% → 36.7%, with a clean monotonic granularity progression (10.5% → 27.7% → 36.7%). Every N/A is structurally justified and aligns with family boundaries.

**Plan**: [`exploration/phase_1b_v2/plan.md`](phase_1b_v2/plan.md)

**Exit criteria**:
- Confinement Concept replaced with family-specific columns (no near-ID column)
- N/A density measured at multiple granularity levels
- Granularity progression confirms context-dependence hypothesis
- v1 → v2 comparison documented

---

### 1d. Qualitative Assessment

Phase 1b_v2 established that the v2 table (38 concepts × 18 columns) has proper discrimination (min discriminating set = 4 columns, no near-ID), structurally justified N/A at 36.7%, and a clean monotonic granularity progression confirming context-dependence. The quantitative structure is sound.

Phase 1d asks: **is this a design space or a classification scheme?** The table describes *what* each concept chose, but does it capture *why*, and could it generate *new* viable concepts? Five tests probe this from different angles.

**Plan**: [`exploration/phase_1d/sprint_plan_1d.md`](phase_1d/sprint_plan_1d.md)

#### Five Tests

1. **Vocabulary Completeness Audit** — For each column, is the controlled vocabulary exhaustive of physically plausible options, or just empirically observed from the 38-concept sample? Identifies open vs. closed vocabularies and missing candidates.

2. **Generative Coherence** — Generate 30 random rows by sampling from the controlled vocabulary (with structural N/A rules applied). Score each for physical coherence and engineering plausibility. The coherence rate measures how much implicit constraint the table hides — low rates mean tightly coupled columns, confirming classification over design space.

3. **Constraint Density Matrix** — Derived from Test 2 failures + systematic review. For each column pair, estimate the fraction of value combinations that are physically forbidden. Produces a coupling heat map showing which columns are genuinely independent dimensions vs. correlated choices.

4. **Blind Row — Design Thesis Recoverability** — Present 5 rows (stripped of name/company) and score on a 4-dimension rubric: physics thesis, hard problems, trade-off rationale, differentiation. Measures whether the table carries descriptive vs. explanatory information.

5. **Concept Initiation Gap Analysis** — For 3 concepts across families, enumerate what additional information (scale parameters, performance targets, physics parameters, economic framing) a systems engineer would need to begin a pre-conceptual design. Identifies the gap between classification and design specification.

#### Deliverables

- `exploration/phase_1d/report.md` — synthesis report covering all five tests
- `exploration/phase_1d/generate_random_concepts.py` — random row generation script (Test 2)
- Vocabulary completeness table, constraint density matrix, scored rubrics, gap analysis

#### Exit Criteria

- All 18 columns assessed for vocabulary completeness (open/closed + missing candidates)
- ≥30 random combinations assessed for coherence with failure reasons
- Constraint density matrix identifies all moderately/strongly coupled column pairs
- 5 concepts scored on the explanatory power rubric
- 3 concepts analyzed for concept initiation gaps
- Clear verdict: classification scheme vs. design space, with evidence
- Recommendations for Chunk 2 informed by both quantitative (1b_v2) and qualitative (1d) evidence

---

## Chunk 2: Prototype Representation

Deliverables:

### 2a. Tree or AND/OR Graph for 3 Concepts

### 2b. Cross-Concept Transfer Test
Can we find a sub-problem that appears on multiple branches and write a "pattern card"?

### 2c. Analysis Report
Do we see shapes forming?
