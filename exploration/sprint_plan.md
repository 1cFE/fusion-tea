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

Phase 1b+1c established two quantitative findings:
1. **N/A density is ~9%** — the table is structurally "almost flat" at the cell level
2. **The columns are almost perfectly correlated** — removing any 9 of 12 CV columns collapses only 1 pair of concepts

But the N/A metric misses a key form of context-dependence: **vocabulary disjointness**. Confinement Concept values under MFE (Tokamak, Stellarator, FRC, ...) answer a fundamentally different question than values under IFE (Laser ICF, Projectile ICF, ...). This is context-dependence that doesn't produce N/A cells — it produces *different semantics in the same column*.

Phase 1d asks the qualitative question these numbers point to: **is this a design space or a classification scheme?**

#### Two Tests

**Test 1: Generative Coherence — Can the table produce viable new concepts?**

Generate 20 random rows by sampling from the v2 controlled vocabulary. Apply known N/A constraints (Class=Inertial → Magnet Type=N/A, etc.) but NO other filtering. For each generated row, assess:
- **Physical coherence**: Are the column values mutually compatible?
- **Engineering plausibility**: Could this combination be a real concept?
- **Failure reason**: If incoherent, which column pair(s) conflict and why?

The coherence rate directly measures how much implicit constraint the table hides. If <10% of random rows are coherent, the columns are highly coupled and the table is a classification scheme, not a combinatorial design space. The failure reasons map the inter-column constraint structure that any richer representation (AND/OR graph, CCA) would need to encode.

Method: Python script generates random rows; LLM assesses coherence. No web search needed — assessment is based on physics reasoning.

**Test 2: Explanatory Power — The "blind row" test**

Present 5 table rows (stripped of concept name and company) and ask: what is this concept's thesis, what are its hard problems, and what trade-offs motivated these choices? Score how much is recoverable from the columns alone vs. requiring external domain knowledge.

This is lighter-weight than Test 1 — a structured brainstorming exercise, not a quantitative analysis. Its value is in identifying *what information the table doesn't carry* (motivations, sensitivities, key parameters, risk profile) that matters for downstream modeling.

#### Deliverables

A short analysis report (`exploration/phase_1d/report.md`) covering:
1. Random-combination coherence results (20 samples) with failure analysis
2. Implicit constraint map derived from failure reasons
3. Blind-row assessment for 5 concepts
4. Synthesis: what the table is, what it isn't, and what Chunk 2 should build

#### Exit Criteria

- At least 20 random combinations assessed for coherence
- Coherence rate computed with confidence
- Clear answer to: "Is this a design space or a classification scheme?"
- Inter-column constraint structure documented (which pairs conflict and why)
- Recommendations for Chunk 2 informed by both quantitative (1b+1c) and qualitative (1d) evidence

---

## Chunk 2: Prototype Representation

Deliverables:

### 2a. Tree or AND/OR Graph for 3 Concepts

### 2b. Cross-Concept Transfer Test
Can we find a sub-problem that appears on multiple branches and write a "pattern card"?

### 2c. Analysis Report
Do we see shapes forming?
