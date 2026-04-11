# Phase 1d: Qualitative Assessment Sprint Plan

**Goal**: Determine whether the v2 differentiation table is a *design space* (generative, spanning, sufficient for concept initiation) or a *classification scheme* (descriptive, empirical, useful for organizing known concepts but not for exploring new ones). Measure the gap precisely and identify what Chunk 2 must add.

**Input**: `exploration/phase_1b_v2/table_v2.csv` — 38 concepts × 18 differentiation columns (+ 2 metadata columns)

**Dependencies**: Phase 1b_v2 results (discrimination analysis, N/A density, granularity progression)

---

## Test 1: Vocabulary Completeness Audit

**Question**: For each column, does the controlled vocabulary span the *physically plausible* design space, or just the choices observed in the 38-concept sample?

**Method**: For each of the 18 differentiation columns:

1. List the current vocabulary (unique non-N/A values)
2. Classify the vocabulary as **closed** (exhaustive of physically plausible options) or **open** (sample-dependent, plausible values missing)
3. For open vocabularies, list 1-3 physically plausible values not represented by any current concept
4. Assess whether the missing values represent:
   - (a) Historical approaches no startup has revived (e.g., magnetic mirror with gas-dynamic confinement)
   - (b) Theoretically valid but never attempted (e.g., MHD direct energy conversion)
   - (c) Values that exist but were lumped into a coarser label (e.g., multiple RF heating schemes collapsed to "RF")

**Deliverable**: Table with columns: Column Name | Vocabulary Size | Open/Closed | Missing Candidates | Gap Type

**Assessment basis**: Physics reasoning + domain knowledge. No web search needed — the question is about physical plausibility, not startup coverage.

**Exit criteria**:
- All 18 columns assessed
- Each open vocabulary has at least 1 concrete missing candidate with justification

---

## Test 2: Generative Coherence

**Question**: Can the table produce viable new concepts by random combination, or are the columns so tightly coupled that most random rows are physically incoherent?

**Method**:

1. **Generate** random concepts from the v2 vocabulary:
   - `generate_random_concepts.py` reads `table_v2.csv`, extracts per-column vocabularies, and samples uniformly with structural N/A rules applied
   - N/A rules encode the confinement hierarchy (family → sub-type → shape/type/approach) and non-confinement conditionals (fuel → tritium breeding, operation mode → repetition rate)

2. **Assess** each concept independently via headless Claude call:
   - `assess_coherence.py` reads the generated concepts, fills `test2-prompt.md` with each row's values, and calls `claude -p` per concept
   - The prompt (`test2-prompt.md`) includes a column glossary, assessment criteria, and a JSON output schema
   - Each assessment scores: physical coherence (bool), engineering plausibility (bool), failure reasons (column pairs + explanation), nearest real concept, novelty classification

3. **Summarize** results with quantitative stats + qualitative synthesis:
   - `summarize.py` computes coherence/plausibility rates, failure pair frequencies, coherence-by-family breakdown
   - Then calls `claude -p` with all assessment data for qualitative synthesis: constraint density matrix, independent vs. coupled dimensions, failure pattern analysis, verdict

**Execution**:

```bash
# Step 1: Generate 30 random concepts (deterministic, seed=42)
uv run python exploration/phase_1d/generate_random_concepts.py
# -> exploration/phase_1d/random_concepts.json

# Step 2: Assess each concept via claude -p (30 sequential calls, ~5-10 min)
uv run python exploration/phase_1d/assess_coherence.py --model sonnet
# -> exploration/phase_1d/assessments.json (written incrementally, resumable)

# Step 3: Compute stats + qualitative synthesis via claude -p
uv run python exploration/phase_1d/summarize.py --model sonnet
# -> exploration/phase_1d/summary.json + exploration/phase_1d/summary.md
```

Resume support: `assess_coherence.py` writes after each assessment and skips already-assessed IDs on rerun. Use `--start N` to begin from concept #N.

**Deliverable**:
- `generate_random_concepts.py` — generation script
- `test2-prompt.md` — prompt template for per-concept assessment
- `assess_coherence.py` — assessment runner
- `summarize.py` — stats + qualitative synthesis
- `random_concepts.json` → `assessments.json` → `summary.json` + `summary.md`

**Interpretation**:
- Coherence rate <10% → columns are tightly coupled; table is a classification scheme, not a combinatorial design space
- Coherence rate 10-50% → moderate coupling; some independent dimensions, some correlated
- Coherence rate >50% → columns are largely independent; table approximates a true design space

**Exit criteria**:
- ≥30 random combinations assessed
- Coherence and plausibility rates computed
- Failure reasons categorized by column pair

---

## Test 3: Constraint Density Matrix

**Question**: Which column pairs are tightly coupled (many forbidden combinations) vs. loosely coupled (nearly independent)?

**Method**:

1. From Test 2 failure reasons, extract all pairwise incompatibilities observed
2. Supplement with systematic review of the most obviously coupled pairs:
   - Fuel × Tritium Breeding (D-T requires breeding, aneutronic doesn't)
   - Fuel × Neutron Management (D-T/D-D require heavy shielding, aneutronic doesn't)
   - Confinement Family × Operation Mode (MFE mostly steady, IFE always pulsed)
   - Operation Mode × Repetition Rate (steady → N/A, pulsed → required)
   - Energy Capture × Fuel (direct conversion mainly viable for charged-particle-producing fuels)
3. For each pair, estimate constraint density: fraction of value-pair combinations that are physically forbidden
4. Produce a heat map (or ranked list) of column-pair coupling strength

**Deliverable**: Constraint density matrix (18×18, symmetric) with coupling strength estimates. Can be qualitative (none / weak / moderate / strong) rather than precise fractions — the goal is to identify structure, not exact numbers.

**Exit criteria**:
- All column pairs with moderate or strong coupling identified
- Clear distinction between independent dimensions and correlated choices

---

## Test 4: Blind Row — Design Thesis Recoverability

**Question**: If an expert sees a table row (without the concept name), how much of the concept's thesis, challenges, and design rationale can they reconstruct?

**Method**:

1. Select 5 concepts spanning different families and design philosophies:
   - 1 conventional MFE (e.g., a stellarator)
   - 1 unconventional MFE (e.g., FRC or mirror)
   - 1 IFE (e.g., a laser ICF variant)
   - 1 MIF
   - 1 non-standard / exotic

2. For each, strip the concept name and company. Present only the 18 column values.

3. Score on a rubric:

   | Dimension | 0 | 1 | 2 |
   |-----------|---|---|---|
   | **Physics thesis** | Can't tell what the concept's "bet" is | Can infer the general approach | Can articulate the specific advantage claim |
   | **Hard problems** | Can't identify key challenges | Can name the challenge category | Can name the specific engineering challenge |
   | **Trade-off rationale** | Can't tell why these choices coexist | Can see trade-offs in isolation | Can reconstruct the design logic linking choices |
   | **Differentiation** | Can't distinguish from similar concepts | Can place in the right family | Can identify what makes this specific concept unique |

   Max score per concept: 8. Max total: 40.

4. For each concept, note:
   - What information was sufficient to reconstruct
   - What information was missing but would have been critical
   - Whether the columns carry *descriptive* information (what was chosen) vs. *explanatory* information (why it was chosen)

**Deliverable**: Scored rubric table (5 concepts × 4 dimensions) + qualitative notes on information gaps

**Exit criteria**:
- 5 concepts scored
- Pattern identified: which rubric dimensions consistently score high vs. low
- Missing information categories documented

---

## Test 5: Concept Initiation Gap Analysis

**Question**: If a systems engineer received a table row, what minimum additional information would they need to begin a pre-conceptual design?

**Method**:

1. Select 3 concepts (1 MFE, 1 IFE, 1 MIF) — can overlap with Test 4 selections
2. For each, list the table row values, then enumerate:
   - **Scale parameters needed**: target power (MWe), plasma volume, magnetic field, pulse energy
   - **Performance targets needed**: Q (gain), confinement time or ρR, plasma β, temperature
   - **Key physics parameters needed**: density regime, energy confinement scaling, burn fraction
   - **Economic framing needed**: target LCOE, capex class, availability target
   - **What the table provides**: which of the above can be inferred or bounded from the row
   - **What the table cannot provide**: which require external information

3. Categorize the gaps:
   - **Quantitative parameters** the table doesn't carry (temperatures, fields, dimensions)
   - **Performance claims** the table doesn't encode (why this concept claims to be better)
   - **Constraint relationships** the table doesn't express (which choices constrain which parameters)

**Deliverable**: Gap analysis table (3 concepts × parameter categories) + synthesis of common gaps

**Exit criteria**:
- 3 concepts analyzed
- Common gap categories identified and ranked by importance for design initiation
- Clear statement of what the table is vs. what a design specification requires

---

## Synthesis Report

Combine all five tests into `exploration/phase_1d/report.md`:

1. **Vocabulary completeness**: How many columns are open vs. closed? What's missing?
2. **Generative coherence**: Coherence rate, plausibility rate, failure mode distribution
3. **Constraint structure**: Which column pairs are coupled? How far from Cartesian?
4. **Explanatory power**: What does the table carry vs. what's missing for expert legibility?
5. **Design initiation gap**: What additional information categories bridge classification → design?
6. **Verdict**: Classification scheme or design space? (Expected answer: classification scheme, with specific evidence)
7. **Recommendations for Chunk 2**: What the AND/OR graph / pattern cards need to add — constraints, rationale, parameters, scale — to move from classification toward design space

---

## Execution Notes

- Tests 1, 4, and 5 are primarily LLM reasoning — no scripts needed beyond the table data
- Test 2 requires a short Python script for random generation; assessment is LLM-assisted
- Test 3 is derived from Test 2 results + manual review — no separate script
- Tests can run in approximate order (1 → 2 → 3 → 4 → 5 → synthesis) but 4 and 5 are independent of 2-3 and could run in parallel
- Total scope: ~1 session if run sequentially, could compress with parallel execution
