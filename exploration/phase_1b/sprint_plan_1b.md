# Phase 1b+1c: Minimum Discriminating Set & N/A Density Analysis

**Sprint Plan — March 2026**

## Objective

Consume the completed Phase 1a differentiation table (38 concepts × 12 columns) and produce two analyses in a single combined report:

1. **Minimum Discriminating Set (1b)**: What is the smallest column subset that uniquely identifies every concept? How much information is lost at each reduction level?

2. **N/A Density Analysis (1c)**: How much context-sensitivity does the design space actually exhibit? Do N/As cluster by architectural branching decisions, or are they diffuse?

These two analyses share inputs and their results cross-reference naturally. The N/A density directly affects discriminating power (N/A-heavy columns discriminate poorly within the block where they're N/A), and the minimum discriminating set reveals which columns carry actual engineering information vs. which are structurally redundant.

The combined result is the empirical answer to the core hypothesis from `context/context_dependent_design_spaces.md`: is the fusion design space well-captured by a flat morphological matrix, or does it exhibit genuine context-dependence that demands a richer representation?

---

## Inputs

All inputs come from Phase 1a. No new research, LLM calls, or web searches are required.

| Input | Path | Description |
|-------|------|-------------|
| Differentiation table | `phase_1a/table.csv` | 38 rows × 15 columns (12 differentiation + 3 metadata) |
| Citations registry | `phase_1a/citations.csv` | 456 per-cell citations with confidence ratings |
| Schema | `phase_1a/schema.md` | Column definitions, controlled vocabulary (v0.2.3) |
| Concept dossiers | `phase_1a/research/*/dossier.md` | 38 per-concept structured findings (context for interpretation) |
| Checkpoint reports | `phase_1a/checkpoints/checkpoint-{01..06}.md` | Schema evolution rationale, cross-concept consistency notes |

### Phase 1a Exit Criteria Status

| Criterion | Target | Actual | Met? |
|-----------|--------|--------|------|
| Applicable cells filled (not TBD) | >85% | 89.5% (408/456) | Yes |
| N/A cells with structural justification | 100% | 100% (per checkpoint reviews) | Yes |
| Unique rows (no two identical) | 100% | 100% (verified — 0 duplicate differentiation rows) | Yes |

Citation quality (>60% gold/silver) was tracked per-cell in `citations.csv` but not aggregated across all 38 concepts. The analysis script should compute this as a side output.

---

## Data Preparation

### Copy and Reclassify

Before analysis, create a corrected copy of the table that reclassifies `None (IFE)` in Column 7 (Magnet Type) as `N/A`.

**Rationale**: The sprint plan (§1c) identified this as a "disguised N/A" — the value `None (IFE)` encodes "upstream choice (IFE) makes this dimension structurally inapplicable," which is the exact definition of N/A used in other columns. 11 IFE concepts are affected.

| File | Description |
|------|-------------|
| `phase_1b/table_original.csv` | Verbatim copy of `phase_1a/table.csv` (frozen snapshot) |
| `phase_1b/table_corrected.csv` | `None (IFE)` → `N/A` in Magnet Type column |

All analysis runs on the corrected table. The original is preserved for reference and reproducibility.

### `Self-confined` Treatment

Three concepts use `Self-confined` in Magnet Type: Zap Energy (Z-pinch), General Fusion (pneumatic MTF), and LPPFusion (dense plasma focus).

- Z-pinch and DPF have genuine self-generated magnetic confinement — `Self-confined` is a real physics answer, not a disguised N/A.
- General Fusion's pneumatic compression has no magnetic confinement at all, but the magnetized target plasma carries its own field. Borderline — but the current classification is defensible.

**Decision**: Keep `Self-confined` as a real value (not N/A) for all three. Note this as a sensitivity item in the report.

### Columns Used

The 12 differentiation columns (3–14 in `table.csv`):

| # | Column | Type |
|---|--------|------|
| 1 | Confinement Family | Controlled (5 values) |
| 2 | Confinement Concept | Semi-controlled (~25 values) |
| 3 | Fuel | Controlled (5 values used) |
| 4 | Primary Heating | Controlled (~18 values) |
| 5 | Energy Capture | Controlled (7 values) |
| 6 | Plasma State | Controlled (7 values + 1 N/A) |
| 7 | Magnet Type | Controlled (10 values + N/A, post-reclassification) |
| 8 | Tritium Breeding | Controlled (8 values + N/A) |
| 9 | Neutron Management | Controlled (5 values) |
| 10 | Operation Mode | Controlled (3 values) |
| 11 | Repetition Rate | Controlled (6 values + N/A) |
| 12 | Driver Technology | Free text |

Metadata columns (Concept Name, Company, Overall Confidence) are excluded from the discriminating set analysis — they're identifiers, not differentiation dimensions.

---

## Directory Structure

```
exploration/phase_1b/
├── sprint_plan_1b.md              # This document
├── analyze.py                     # Combined analysis script
├── table_original.csv             # Frozen copy of phase_1a/table.csv
├── table_corrected.csv            # None (IFE) → N/A reclassification
└── report.md                      # Combined 1b+1c analysis report
```

### File Ownership

| File | Written by | Mutability |
|------|-----------|------------|
| `sprint_plan_1b.md` | Human | Stable |
| `analyze.py` | Human / agent | Evolving during development, frozen after report |
| `table_original.csv` | Script (copy) | Immutable |
| `table_corrected.csv` | Script (transform) | Immutable once generated |
| `report.md` | Script (generated) | Regenerated on each run |

---

## Analysis Methodology

### Part 1: Minimum Discriminating Set (1b)

**Goal**: Find the smallest subset of the 12 columns such that every concept (row) has a unique combination of values.

#### 1.1 Brute-Force Enumeration

With 12 columns, the power set has 2^12 = 4,096 subsets. For each subset:
- Project the 38-row table onto just those columns
- Check if all 38 projected rows are distinct
- Record: subset, size, whether it discriminates, and if not, which rows collide

This is computationally trivial (< 1 second). Report all minimum-size discriminating sets.

#### 1.2 Greedy Column Ranking

Build a greedy set cover:
1. Start with the column that induces the most distinct partitions across 38 concepts
2. Add the column that resolves the most remaining collisions
3. Repeat until all rows are unique

This produces a single ordering, not the optimal set, but it reveals which columns contribute the most marginal discrimination. Report the full greedy ordering with the number of distinct groups at each step.

#### 1.3 Information-Theoretic Ranking

For each column, compute:
- **Entropy** H(column): How much information the column carries across 38 concepts. High-cardinality columns (Confinement Concept, Driver Technology) will dominate. Normalize by log2(38) for comparability.
- **Conditional entropy** H(column | other columns): How much additional information each column provides given the rest. Columns with zero conditional entropy are fully redundant.

#### 1.4 Confusion Analysis

For each column, show what happens when it's removed:
- Which concept pairs become indistinguishable?
- Are the confused pairs from the same confinement family? Same fuel? (This reveals whether the column's discrimination is within-family or cross-family.)

This is the qualitative complement to the brute-force enumeration — it shows not just *that* a column is needed, but *what specific distinctions it makes*.

#### 1.5 N/A Treatment in Discriminating Set

N/A is a valid distinguishing value for this analysis — if concept A has `N/A` and concept B has `Li blanket` in the same column, they are distinguishable. But discrimination by N/A is "cheap" (it's a structural property, not an engineering choice). The report should flag minimum sets that rely heavily on N/A-based discrimination vs. those that discriminate on engineering content.

### Part 2: N/A Density Analysis (1c)

**Goal**: Measure the context-sensitivity of the design space by analyzing the structure and density of N/A cells.

#### 2.1 Overall N/A Rate

Basic statistics on the corrected table:
- Total N/A cells / total cells
- Total N/A cells / total applicable cells (excluding metadata)
- Comparison to the hypothesis thresholds from `context_dependent_design_spaces.md`:
  - <10% → flat table works, context-dependence is minor
  - 10–20% → moderate context-dependence
  - \>20% → strong context-dependence, richer representation may be warranted

#### 2.2 Per-Column N/A Rates

For each of the 12 columns:
- Count of N/A cells
- N/A rate (count / 38)
- Which confinement families contribute the N/As

Flag columns where:
- N/A rate > 50% (column is too concept-specific for a universal table)
- N/A rate = 0% (column is universally applicable — strong candidate for the discriminating set)

#### 2.3 Per-Row N/A Rates

For each of the 38 concepts:
- Count of N/A cells (out of 12)
- N/A rate
- Rank from most to fewest N/As

Concepts with high N/A counts have the most "unique decision structure" — they face a fundamentally different set of questions than the median concept. These are the strongest evidence for context-dependence.

#### 2.4 Block Structure Detection

This is the critical measurement. If N/As cluster in identifiable blocks, the context-dependence is driven by a small number of early branching decisions (fuel, confinement family). If N/As are diffuse, the structure is more complex.

Approach:
1. Sort rows by confinement family, then by fuel within family
2. Visualize the N/A pattern as a binary matrix (N/A = 1, non-N/A = 0)
3. Compute N/A rates per block (family × fuel combinations)
4. Test: does confinement family alone predict most N/A structure? What about fuel? Family + fuel combined?

Report should include an ASCII or markdown representation of the block structure.

#### 2.5 Structural N/A Chains

For each N/A cell, trace the structural justification:
- What upstream architectural choice makes this column inapplicable?
- Do N/A chains form (choice A → N/A in column X → N/A in column Y)?

This directly tests the AND/OR graph hypothesis from the context paper: if N/As form chains triggered by specific OR-node resolutions, the lazily-evaluated graph model is justified.

Known chains to verify:
- `p-B11 fuel` → `N/A` Tritium Breeding → `Minimal (aneutronic)` Neutron Management (not N/A, but structurally determined)
- `IFE confinement` → `N/A` Magnet Type → `N/A` Repetition Rate? (no — IFE concepts DO have rep rates)
- `Steady-state operation` → `N/A` Repetition Rate

---

## Report Structure

The output `report.md` should contain:

```
# Phase 1b+1c Analysis Report

## Executive Summary
- Key findings in 3-5 bullets
- Answer to the core hypothesis: flat table or context-dependent?

## 1. Data Summary
- Table dimensions, completeness, confidence distribution
- Citation quality aggregate (gold/silver/bronze breakdown)

## 2. Minimum Discriminating Set (1b)
### 2.1 Results
- All minimum discriminating sets
- Size of minimum set
### 2.2 Greedy Column Ranking
- Full ordering with group counts at each step
### 2.3 Information Content
- Per-column entropy table
- Redundancy analysis
### 2.4 Confusion Analysis
- Per-column removal impact
- Which distinctions each column carries

## 3. N/A Density Analysis (1c)
### 3.1 Overall Density
- Aggregate rate and hypothesis assessment
### 3.2 Per-Column Analysis
- Table of N/A rates by column
### 3.3 Per-Row Analysis
- Table of N/A rates by concept
### 3.4 Block Structure
- Block diagram / matrix visualization
- Family and fuel as predictors
### 3.5 Structural Chains
- Identified N/A chains and their triggers

## 4. Implications
### 4.1 For Phase 1d (Qualitative Assessment)
- What to look for in the dossier review
### 4.2 For Chunk 2 (Prototype Representation)
- Does the evidence warrant AND/OR graph investment?
### 4.3 For Downstream Modeling
- Which columns matter for SysML model structure decisions?
- Where is cross-concept transfer likely safe?

## Appendix
- A: Full discriminating set enumeration (all minimum sets)
- B: Complete N/A matrix (38 × 12)
- C: Data preparation details (reclassification log)
```

---

## Execution

### Implementation

A single Python script (`analyze.py`) that:
1. Reads `phase_1a/table.csv`
2. Copies it to `table_original.csv`
3. Applies the `None (IFE)` → `N/A` reclassification, writes `table_corrected.csv`
4. Runs all Part 1 and Part 2 analyses on the corrected table
5. Writes `report.md`

No external dependencies beyond the Python standard library (`csv`, `itertools`, `collections`, `math`). No LLM calls.

```bash
uv run python exploration/phase_1b/analyze.py
```

The script should be idempotent — running it again overwrites the report with fresh results.

### Verification

After the script runs:
- Spot-check minimum discriminating sets against the table manually (pick 2-3 sets, verify uniqueness)
- Verify N/A counts match checkpoint-06 totals (33 N/A cells pre-reclassification, 44 post-reclassification with 11 `None (IFE)` → N/A)
- Verify no off-by-one errors in column indexing (the CSV has metadata columns before differentiation columns)

### Time Estimate

Script development + report review: a single session. The analysis is computationally trivial — the work is in structuring clear output and writing the interpretation.

---

## Exit Criteria

| Criterion | Target |
|-----------|--------|
| All minimum discriminating sets identified | Enumerated exhaustively (2^12) |
| N/A density computed with block structure | Per-column, per-row, and per-block rates |
| Core hypothesis answered | Report states whether flat table suffices or richer representation is warranted, with evidence |
| Self-confined sensitivity noted | Report discusses impact of alternative `Self-confined` classification |
| Implications for Phase 1d and Chunk 2 documented | Report includes forward-looking recommendations |

---

## Relationship to Other Phases

- **Phase 1a** (complete): Provides all inputs. No feedback loop — 1b+1c consumes 1a outputs but does not modify them.
- **Phase 1d** (next): Qualitative assessment of whether the table captures what makes each concept *distinctive*. The 1b+1c report frames the 1d analysis — columns identified as low-discrimination or high-N/A are candidates for "does this column actually matter?" inquiry. 1d requires LLM reasoning over dossiers.
- **Chunk 2** (gated): The 1b+1c report is the primary input to the gate decision. If N/A density is high with clear block structure, Chunk 2 (AND/OR graph prototyping) is justified. If N/A density is low and the flat table discriminates well, Chunk 2 may not be worth the investment.
