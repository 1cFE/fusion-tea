# Spec: Scoring V2 Framework Stencil + Modularity Slice

**Status:** Implementation Complete
**Owner:** Reid W
**Created:** 2026-05-17 13:50 PDT
**Complexity:** MEDIUM
**Branch:** concept-downselect

---

## Work Item Summary

Stencil the V2 deterministic scoring framework and prove it works end-to-end by implementing the `plant_level_modularity` embedding group as the first complete chain — feature extraction through embeddings through weight matrix to score table. The work delivers a parallel pipeline at `exploration/scoring_v2/` that does not disturb V1. "Done" means a reviewer can re-score under a different weight matrix in seconds, with no LLM invocation, and the framework's iteration affordances are demonstrated rather than only designed.

## Why This Matters Now

The V2 design (`.project/concepts/scoring-v2-design.md`) commits to multi-layer separation whose iteration-cost claims are unverified. The design's "First risk to de-risk" is exactly this slice: build one chain end-to-end on a small set of contrasting concepts and see whether the architecture holds before we build out twenty embeddings and a feature schema covering thirty-eight concepts. Failing here is cheap; failing two months in is not.

## Key Bets / Constraints

- **Bet:** Three concepts spanning the modularity range (FRC → HTS compact tokamak → large stellarator) are enough to surface architecture problems if any exist. If the framework can produce sensible, ordered outputs for these three, it generalizes.
- **Bet:** `plant_level_modularity` is best implemented as a *group of fine-grained embeddings* (scale, geometry, multiplicity, subsystem-stack burden) rather than a single category lookup. A single category lookup would collapse several distinct judgements into one opaque number and defeat the slice's interpretability goal — see design.md for the decomposition.
- **Constraint:** V1 stays frozen. Nothing under `exploration/concept_analysis/` is modified. New code lives under `exploration/scoring_v2/`.
- **Constraint:** Rules defined here are new and clear, not ports of V1. V1 prompt templates and scoring pipeline are referenced for shape comparison, not copied.
- **Non-goal:** `component_modularity` (the 7-subsystem chain) — that is the next slice, gated on this one succeeding.
- **Non-goal:** Migration tooling, UI, evidence corpus content, scenarios beyond `default.yaml`.

---

## Business Goals

### Why This Matters

The V2 design separates features, embeddings, and weights into independently editable artifacts and claims this will make iteration cheap and disputes localizable. Until at least one chain runs end-to-end, those claims are unverified architecture. A working slice gives us evidence to either commit to the framework for all 20+ embeddings or rethink granularity before sinking more effort in.

### Success Criteria

- [ ] A reviewer can read the score table CSV and see Manufacturability & Scale-Out populated for the three concepts based on the `plant_level_modularity` embedding group.
- [ ] A reviewer can edit the weight on any of the group's four embeddings in `default.yaml` and re-run `score.py` in seconds with no LLM call invoked.
- [ ] A reviewer can change the value of one feature in one concept's feature file and see the score change deterministically.
- [ ] The three concepts produce qualitatively correct ordering on Manufacturability & Scale-Out (Helion > CFS ARC-class > large stellarator).
- [ ] Running `score.py` twice in succession produces byte-identical output.

### Priority

Highest — gates whether we continue with the V2 framework as designed or rethink. No other V2 work item should start until this lands.

---

## Problem Statement

### Current State

V1 scoring (`exploration/concept_analysis/`) entangles fact extraction, judgement, and aggregation in a single LLM pass per concept. Re-scoring under different weights requires re-running the full pipeline (~2 hours for 38 concepts). There is no shared feature representation across concepts, no separately editable weight matrix, and no way to localize a score disagreement to a specific layer. The V2 design fixes this conceptually; the framework code does not yet exist.

### Desired Outcome

A working `exploration/scoring_v2/` directory whose first end-to-end chain (the four embeddings of the `plant_level_modularity` group → Manufacturability & Scale-Out column) demonstrates the design's iteration affordances on three concepts. The slice does not need broad coverage; it needs to be deep enough that the architectural bets are tested — including the central multi-embedding-aggregation bet.

---

## Scope

### In Scope

**Stage 1 — Framework stencil under `exploration/scoring_v2/`:**
- Directory structure per the design doc: `features/`, `embeddings/`, `weights/`, plus top-level `extract.py`, `score.py`, and a schema definition for features. (No `evidence/` directory this slice — no embedding consumes a corpus entry; the directory and its file land in slice 2.)
- Feature schema file declaring feature names, types, enumerations, required vs optional, and the declared extractor (`taxonomy` / `cost_model` / `llm` / `manual`) for each feature.
- Schema validator that checks any `features/{concept_id}.yaml` against the schema.
- `extract.py` dispatcher that recognizes all four extractor enum values (`taxonomy`, `manual`, `cost_model`, `llm`). `taxonomy` and `manual` fully implemented; `cost_model` and `llm` are NOT scaffolded — invoking the dispatcher with either raises `NotImplementedError` with a "will be implemented in a later slice" message. Slice 2 adds those modules when they are needed.
- `score.py` that loads features, evidence, the embedding registry, and a named weight matrix, evaluates registered embeddings, applies weights, and writes a CSV score table with one row per concept.
- Empty `embeddings/rulebook.py` with the registration mechanism in place.
- Minimal `weights/default.yaml` with the three dimensions declared.
- Stage 1 exit: `score.py` runs against all 38 concepts and emits a zero-valued score table without errors.

**Stage 2 — `plant_level_modularity` embedding group end-to-end on three concepts:**
- Concepts: `01-hts-compact-tokamak` (CFS ARC-class, HTS compact tokamak), `08-frc-w-direct-conversion` (Helion-shape FRC), `10-large-scale-stellarator` (Gauss-class large stellarator). All three are existing taxonomy rows; selected to span the modularity range (high / mid / low) for FR-9.
- Define the features the group's embeddings consume. Feature names, types, and extractors are decided during design/implementation, informed by the V1 references but defined fresh. All four embeddings consume only taxonomy columns from `table.csv`.
- Populate `features/{concept_id}.yaml` for all 38 concepts via the taxonomy extractor (one bulk run). All embeddings in this slice consume only taxonomy-sourced features; no per-concept hand-review beyond the bulk run is required to satisfy FR-9.
- Implement the four embeddings of the `plant_level_modularity` group in `embeddings/rulebook.py`: `min_viable_device_scale`, `hardware_topology_complexity`, `unit_multiplicity`, `subsystem_stack_burden`. Embedding definitions are new and clear, defined here — not ported from V1.
- Add each embedding's weight under Manufacturability & Scale-Out in `default.yaml`.
- Run end-to-end; capture the score table.

### Out of Scope

- `component_modularity` (7-subsystem chain) — next slice.
- Any other embedding (capacity factor, triple-product gap, capital density, etc.).
- Feature files for the other 35 concepts beyond zero-valued stubs needed for `score.py` to iterate.
- Evidence corpus — no `evidence/corpus.yaml` file is created this slice; the `plant_level_modularity` group consumes no corpus IDs.
- Alternative scenario weight matrices (no `bet_*.yaml` files in this slice).
- Migration of V1 deterministic lookups (C2, C6, η_th) into the new framework.
- Any UI, visualization, or dashboard beyond the CSV score table.

### Edge Cases & Considerations

- Three concepts are not enough to validate the embeddings themselves across the full 38-concept range. The slice validates the *framework*; embedding-correctness validation is a separate concern.
- All 38 concepts get full taxonomy-extracted feature files in Stage 1 (since the four embeddings only consume taxonomy columns); no per-concept hand-review beyond that is required this slice.
- `cost_model` and `llm` extractors are scaffolded but not exercised in this slice. The design must ensure their interfaces are real enough that the next slice can plug in real handlers without refactoring the dispatcher.
- The "qualitatively correct" ordering check (Helion > CFS ARC > large stellarator) is a sanity test, not proof of correctness. A wrong ordering is a clear fail; a right ordering is necessary but not sufficient.

---

## Requirement Selection Notes

Requirements below capture only what must be true for this slice to count as done. Embedding definitions, extractor implementation details, feature names, file formats beyond YAML/CSV/Python, and the schema validator's specific check set are intentionally deferred to design. The framework's internal interfaces (embedding registration, dispatcher signature, score-table column order) are also design decisions, not requirements here.

---

## Requirements

### Functional Requirements

1. **FR-1**: The framework MUST live entirely under `exploration/scoring_v2/` and MUST NOT modify any file under `exploration/concept_analysis/`.
2. **FR-2**: The feature schema MUST be a single declarative file that, for every feature, specifies name, type, valid values (if categorical), required vs optional status, and declared extractor.
3. **FR-3**: `extract.py` MUST dispatch to the declared extractor for the requested feature and MUST be re-runnable per (concept, feature) pair without side effects on other features.
4. **FR-4**: `score.py` MUST be deterministic — two consecutive runs over unchanged inputs MUST produce byte-identical output.
5. **FR-5**: `score.py` MUST NOT invoke any LLM. All LLM work MUST be confined to `extract.py`.
6. **FR-6**: The weight matrix `weights/default.yaml` MUST be editable as plain text; changing a weight and re-running `score.py` MUST update the output without any other action.
7. **FR-7**: The score table MUST include one column per dimension (Economic Potential, Technical Feasibility, Manufacturability & Scale-Out) and one row per concept, plus a per-dimension evidence-quality readout column derived from input feature confidences.
8. **FR-8**: Stage 1 MUST produce a valid score table for all 38 concepts (values MAY be zero where embeddings are unimplemented).
9. **FR-9**: Stage 2 MUST produce non-zero, ordered Manufacturability & Scale-Out scores for the three named concepts based on the four embeddings of the `plant_level_modularity` group. The qualitative ordering `08-frc-w-direct-conversion` > `01-hts-compact-tokamak` > `10-large-scale-stellarator` MUST hold.
10. **FR-10**: Embeddings defined in this slice MUST be new and clearly specified within `embeddings/rulebook.py`. The V1 prompt templates and scoring pipeline (listed under Related Artifacts) MAY be referenced for context but MUST NOT be ported verbatim.
11. **FR-11**: Schema validation MUST run as part of `score.py` invocation and MUST fail loudly on any feature file that violates the schema.

### Non-Functional Requirements

- **NFR-1**: `score.py` SHOULD complete in under 10 seconds for 38 concepts. This is a soft target; the point is "fast enough to iterate," not a specific number.
- **NFR-2**: Code uses `uv` for Python execution per project convention.

---

## Acceptance Criteria

### Core Functionality
- [ ] `uv run python exploration/scoring_v2/score.py` runs to completion against all 38 concepts and writes a CSV score table.
- [ ] The score table includes Economic Potential, Technical Feasibility, Manufacturability & Scale-Out, plus an evidence-quality column.
- [ ] For `01-hts-compact-tokamak`, `08-frc-w-direct-conversion`, and `10-large-scale-stellarator`, Manufacturability & Scale-Out is non-zero and ordered `08-frc-w-direct-conversion` > `01-hts-compact-tokamak` > `10-large-scale-stellarator`.
- [ ] `uv run python exploration/scoring_v2/extract.py <concept_id> <feature_name>` updates exactly the one (concept, feature) cell.
- [ ] Editing a weight in `weights/default.yaml` and re-running `score.py` produces an updated table without any LLM invocation.
- [ ] Two consecutive `score.py` runs over unchanged inputs produce byte-identical output.

### Quality & Integration
- [ ] V1 pipeline at `exploration/concept_analysis/` is unmodified and still runs.
- [ ] Schema validator catches a deliberately malformed feature file in a test.
- [ ] The slice produces no new dependency requirements beyond `uv add` for any new packages.

---

## Next-Stage Handoff

**Settled in this spec:**
- Directory location (`exploration/scoring_v2/`), the three concepts (`01-hts-compact-tokamak`, `08-frc-w-direct-conversion`, `10-large-scale-stellarator`), the de-risking goal (framework iteration affordances including multi-embedding aggregation), and the constraint that embeddings are new and clear (not V1 ports).
- `plant_level_modularity` is implemented as a group of four embeddings (`min_viable_device_scale`, `hardware_topology_complexity`, `unit_multiplicity`, `subsystem_stack_burden`), not a single category lookup.
- The three score dimensions and pure weighted-sum aggregation are fixed per the design doc.
- V1 stays frozen and untouched.

**Design must figure out:**
- Feature names, types, and extractor assignments for each of the group's four embeddings. The design must look at the V1 references (listed below) for context on how `table.csv` columns and other taxonomy fields are consumed today, then decide fresh.
- Each embedding's exact formulation — what features combine, in what if/elif shape, into what 1–5 output. The design must define each clearly.
- How `embeddings/rulebook.py` registers embeddings (decorator, registry dict, file-naming convention, etc.) and how `score.py` discovers them.
- The CSV score-table column order and formatting.
- The `cost_model` extractor's interface — what file it reads (`model_setup.py` parameters, `model_output.md` outputs, or both) and how it parses them. This interface MUST be real enough that the next slice can plug in handlers without refactoring.

**Watch-outs for design:**
- The temptation to over-engineer the schema for features we don't yet have. The schema should support the features the four embeddings need and the extension shape, no more.
- The temptation to also implement `component_modularity` "while we're in there." Resist — it is the next slice for a reason.
- The temptation to port a V1 embedding (e.g. `detect_c2_category`) directly. The user has explicitly asked for new, clear embedding definitions; V1 is reference, not source.
- Evidence-quality readout derivation logic — design must commit to how per-feature confidences combine into a per-dimension confidence (e.g. weighted mean, min, or a categorical roll-up). This is the first concrete instance of that aggregation.

---

## Related Artifacts

- **Design Concept:** `.project/concepts/scoring-v2-design.md` — the architectural commitment this slice implements.
- **Upstream Concept:** `.project/concepts/scoring-framework-v2.md` — the problem statement and success criteria.
- **Deterministic Scoring Outline:** `.project/concepts/determinstic-scoring/` — the source material for `plant_level_modularity`'s intent, plus the `Fusion_Modularity_Score.xlsx` (whose 7-subsystem chain is the `component_modularity` reference, deferred to slice 2).
- **V1 references (for embedding-shape context, not porting):**
  - `exploration/concept_analysis/prompt_templates/config/scoring_framework.md` — V1 criterion definitions and sub-factor language.
  - `exploration/concept_analysis/prompt_templates/calibrate.md` — V1 cross-concept calibration steps.
  - `exploration/concept_analysis/prompt_templates/synthesis.md` — V1 per-concept synthesis prompt that produces the score block.
  - `exploration/concept_analysis/scripts/run_scoring_pipeline.py` — V1 pipeline orchestration.
- **V1 deterministic lookups (NOT ported in this slice but show the pattern):** `exploration/concept_analysis/scripts/lib/scoring.py` — `detect_c2_category()`, `detect_c6_category()`, `canonical_eta_th()`.
- **Design (to be created):** `.project/active/scoring-v2-modularity-slice/design.md`
- **Plan (to be created):** `.project/active/scoring-v2-modularity-slice/plan.md`

---

**Next Steps:** After approval, proceed to `/_my_design`
