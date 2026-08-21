# Spec: Scoring V2 — Component-Level Modularity Slice

**Status:** Implementation Complete (pending user-side reference concept data)
**Owner:** Reid W
**Created:** 2026-05-17 21:04 PDT
**Complexity:** MEDIUM
**Branch:** concept-downselect

---

## Work Item Summary

Extend `exploration/scoring_v2/` with the **`component_modularity` embedding group** — the seven-subsystem chain from `Fusion_Modularity_Score.xlsx` — wired alongside the existing `plant_level_modularity` group into Manufacturability & Scale-Out. The slice's central acceptance test is the **xlsx-collapse hypothesis** from the upstream design: if the seven subsystem embeddings are fine-grained enough, the xlsx's per-family "inherent-modularity multiplier" should fall out of the embeddings rather than be applied as a separate factor — i.e. scoring the xlsx's six worked-example concepts through the new embeddings (no family multiplier) should reproduce the xlsx's final 1–5 scores within tolerance. "Done" means the embeddings hit that bar (or we have evidence in hand that they don't, with a concrete decision recorded).

## Why This Matters Now

Slice 1 stencil-tested the V2 architecture against a small, taxonomy-only embedding group. It proved orchestration, layer separation, and iteration affordances — but on the easy half of the problem. The xlsx-collapse test is what the upstream design (`scoring-v2-design.md`) named as **the** first risk to de-risk for the V2 framework as a whole: it is the empirical check that fine-grained embeddings can replace a category-multiplier lookup. If they can, V2 is the right framework for the remaining ~15 embeddings. If they can't, we need to revisit the granularity claim before adding any more.

In addition, this slice retires three slice-1 deferrals that the architecture has not yet exercised:
- the `cost_model` extractor interface (per-subsystem capex weight shares),
- the `evidence/corpus.yaml` file (the xlsx's worked-example scores as cited world-facts),
- mixed-confidence aggregation (taxonomy `high` + cost-model `medium` + manual `medium` features feeding the same dimension).

## Key Bets / Constraints

- **Bet:** Seven subsystem embeddings, each consuming a few features and applying the xlsx's 1–5 lookup criteria, are fine-grained enough that the xlsx's family multiplier (range 0.75–1.20) is reproduced *implicitly* by the embedding bands themselves. We test this directly. A negative result is informative — it tells us where the granularity gap is.
- **Bet:** Per-family capex weight shares (W1..W7) live in a small lookup keyed by `confinement_family` + topology, sourced via the `cost_model` extractor with a per-concept override path for concepts that have an actual cost model in `models/designs/`. This is the slice that proves the dispatcher's `(concept_id, feature_name, schema_entry) → (value, provenance, confidence)` contract holds across two extractor types feeding the same embedding.
- **Bet:** The xlsx's six worked-example concepts (ITER, NIF, CFS ARC-class, Type One Energy stellarator, Helion, Inertia/LIFE-class DPSSL) are the right calibration set. Three already exist in `table.csv` (CFS, Type One, Helion). The other three (ITER, NIF, Inertia/LIFE) are added as the framework's first non-taxonomy reference concepts — explicitly exercising the slice-1 architectural reservation that `features/*.yaml` filenames, not `table.csv` rows, define the concept universe.
- **Constraint:** Slice-1 code is not refactored. New code is additive: more entries in `schema.yaml`, more embeddings in `rulebook.py`, more keys in `weights/default.yaml`, new files in `lib/extractors/` and `evidence/`. The `extract.py` and `score.py` CLIs gain no new flags they don't need.
- **Constraint:** The `plant_level_modularity` slice-1 acceptance bar (Helion ≈4.80, CFS ≈2.90, Stellarator ≈1.50) **must continue to hold**. Adding component-modularity embeddings to the M&SO dimension changes M&SO numbers; the *contribution from the plant-level group alone* must stay stable, and the combined M&SO ordering for those three concepts must remain Helion > CFS > Stellarator.
- **Constraint:** The schema/embedding versioning policy that slice 1 deferred (design.md "Tentative, revisit when N>1 embedding groups exist") becomes due. This slice settles it or records a deliberate further deferral with a date.
- **Non-goal:** Embeddings outside `component_modularity`. Capacity factor, triple-product gap, capital density, etc. are later slices.
- **Non-goal:** Bringing existing `models/designs/{generic_ife, hif_ife}` cost models under the scoring framework. They are inspected for the `cost_model` extractor interface design but not consumed in this slice.
- **Non-goal:** A second weight scenario (`bet_*.yaml`). The framework supports it; this slice does not produce one.
- **Non-goal:** Replacing or modifying the xlsx as a reference. The xlsx remains the calibration target.

---

## Business Goals

### Why This Matters

The framework's central architectural claim is that *judgement decomposes into independently-weightable rules*. Slice 1 demonstrated the mechanics of that decomposition on a small group. Slice 2 tests whether the decomposition *carries information* — whether a chain of seven small rules can stand in for a category-lookup-plus-multiplier without losing the discrimination the multiplier was doing. Until that question is answered, we cannot tell future reviewers whether disagreements about a score should be debated at the feature level, the embedding level, or the (currently absent) family-multiplier level. The xlsx is the cleanest available ground truth for that question because it represents a domain expert's prior take, with explicit numbers we can diff against.

### Success Criteria

- [ ] A reviewer can read the score table and see Manufacturability & Scale-Out populated by *both* embedding groups (`plant_level_modularity` and `component_modularity`) for the 38 taxonomy concepts plus the three added xlsx-reference concepts.
- [ ] For the six xlsx worked-example concepts, the slice-2 final M&SO score (using only the seven `component_modularity` embeddings, with the xlsx's family multiplier excluded) matches the xlsx's "Final Modularity Score" within ±0.4 on the 1–5 scale.
- [ ] A reviewer can edit one component-modularity feature for one concept, re-run `score.py`, and see exactly the band shift the xlsx's lookup table would predict — debuggable to one cell in one embedding.
- [ ] A reviewer can edit the relative weight between `plant_level_modularity` and `component_modularity` groups in `weights/default.yaml` and re-run without any LLM call.
- [ ] The framework reports per-dimension evidence quality that is no longer uniformly `high` once cost-model-extracted features appear, surfacing the mixed-confidence-aggregation behavior we deferred in slice 1.
- [ ] V1 pipeline is unmodified. Slice-1 acceptance bars still pass.

### Priority

P0 — this is the de-risk gate the upstream design named for the whole V2 framework. Subsequent embedding work waits on this slice landing or producing a documented redirect.

---

## Problem Statement

### Current State

Slice 1 shipped a working V2 pipeline whose only embeddings are the four `plant_level_modularity` rules. All of them consume taxonomy categoricals; none reaches into cost-structure detail; none cites shared world-facts; the evidence-quality column is uniformly `high`. The architecture's three deferred surfaces (`cost_model` extractor, evidence corpus, mixed-confidence aggregation) have no test coverage. The xlsx — a domain expert's documented decomposition of factory-buildability across seven subsystems — sits next to the framework as a reference artifact, not yet expressed inside the framework.

### Desired Outcome

The seven xlsx subsystems exist as registered embeddings in `rulebook.py`, sharing a `component_modularity` group label. Their features are populated by a mix of `taxonomy`, `cost_model`, and `manual` extractors; the dispatcher's two unimplemented branches collapse to one. The xlsx's six worked examples score in the framework; we have a side-by-side comparison vs. the xlsx's final numbers, and a one-paragraph judgement on whether the xlsx-collapse hypothesis held. The first three non-taxonomy concepts (ITER, NIF, Inertia/LIFE) exist as `features/*.yaml` files outside `table.csv`, exercising the slice-1 architectural reservation in earnest.

---

## Scope

### In Scope

**Schema and extractor extensions:**
- Additional features in `schema.yaml` covering the inputs of the seven subsystem embeddings. Feature names, types, and per-feature extractor declarations are decided in design; the spec only fixes that the *set* of new features MUST be sufficient for the seven embeddings to evaluate against every existing scoring concept plus the three added reference concepts.
- Implementation of the `cost_model` extractor in `lib/extractors/cost_model.py` to the same `(concept_id, feature_name, schema_entry) → (value, provenance, confidence)` signature as `taxonomy`. The extractor MUST handle the "no cost model exists for this concept" case by falling back to a family-default lookup with reduced confidence, not by raising.
- The `manual` extractor (already implemented in slice 1) is exercised here for the first time, on features for the three added reference concepts where neither taxonomy nor a cost model is available.

**Evidence corpus:**
- New file `exploration/scoring_v2/evidence/corpus.yaml` containing the six xlsx worked-example final-scores as cited world-facts (one entry per concept, with `id`, `value`, `source`, `date`).
- An embedding (or test fixture) that references the corpus entries to verify the xlsx-collapse hypothesis. Whether this lives in `rulebook.py` (as an acceptance embedding) or in `tests/scoring_v2/` (as an out-of-band check) is a design decision.

**Embeddings:**
- Seven embeddings in `rulebook.py` under the `component_modularity` group label, one per xlsx subsystem:
  1. `core_vessel_modularity` (Core / Vessel / Target chamber)
  2. `driver_coil_modularity` (Driver / Coils / Pulsed-power)
  3. `blanket_first_wall_modularity` (Blanket & First Wall)
  4. `power_conversion_bop_modularity` (Power Conversion / BOP)
  5. `fuel_cycle_modularity` (Fuel Cycle / Tritium Plant)
  6. `auxiliaries_modularity` (Auxiliaries — H&CD, cryo, vacuum)
  7. `civil_shielding_modularity` (Civil / Building / Shielding)
- Each embedding maps its declared features to a 1–5 scalar following the xlsx's lookup criteria. The exact feature decomposition and if/elif structure is a design call.

**Weight wiring:**
- The seven embeddings receive weights under Manufacturability & Scale-Out in `weights/default.yaml`. Per-concept variation in weight shares (the xlsx's per-family W1..W7) is handled by either (a) treating the weight shares themselves as features extracted per-concept and folded into each embedding's output, or (b) keeping the weight matrix flat and letting embeddings absorb the family variation. The choice is a design decision; the spec only requires that whichever choice is made preserves the xlsx-collapse test and the slice-1 acceptance bar.

**Non-taxonomy reference concepts:**
- Three new `features/*.yaml` files added for ITER, NIF, and Inertia/LIFE (concept IDs to be decided in design — recommend `00a-iter`, `00b-nif`, `00c-inertia-life` or similar to keep them sorted out of band from the 38 taxonomy rows). These are populated by the `manual` extractor exclusively. They exist to score, not to compete in the broader portfolio.

**Acceptance evidence:**
- Side-by-side comparison table of slice-2 score vs. xlsx final score for all six worked examples, included in the slice's implementation notes when complete.
- Combined-M&SO check: Helion, CFS, and Stellarator final M&SO values change (component-modularity contribution is now nonzero), but their relative ordering MUST be preserved and the plant-level-only contribution MUST equal slice 1's published values (4.80 / 2.90 / 1.50) when computed in isolation.

**Versioning policy decision:**
- Either add a `version` argument to the `@embedding` decorator with a defined bump policy, OR record an explicit further deferral with the date and the slice it is bound to. No silent deferral.

### Out of Scope

- `component_modularity` rules for fuels or confinement geometries that do not appear in `table.csv` plus the three added reference concepts.
- Migration of `plant_level_modularity` embeddings to use the `cost_model` extractor (they currently use only `taxonomy`; no value in changing that here).
- Any UI, dashboard, or HTML rendering of the score table. CSV stays the only consumer.
- Alternative weight scenarios (`bet_*.yaml`). Architecture supports them; this slice produces none.
- Re-extraction of the slice-1 feature files. Adding features is additive; existing feature blocks remain untouched on re-run of `--bulk-taxonomy`.
- Audit or refactor of `exploration/concept_analysis/` (V1). Untouched.

### Edge Cases & Considerations

- **The xlsx-collapse hypothesis may fail.** If the seven embeddings cannot reproduce the xlsx's family-multiplier discrimination within ±0.4, the slice still counts as "done" provided a clear write-up identifies *where* the gap is (which embedding under-discriminates, on which feature axis) and proposes either a finer-grained embedding decomposition or a deliberate decision to retain a family multiplier in the scoring layer. A negative result is acceptable evidence, not a failure of the slice.
- **Per-family weight shares might genuinely need to vary per concept.** The xlsx ships eleven distinct weight rows. If the design folds these into per-concept features (extractor = `cost_model` with fallback to family lookup), the `cost_model` extractor's interface gets exercised even without real cost models — the fallback path itself is the test surface.
- **Mixed-confidence aggregation may surface that min-confidence is too conservative.** Slice 1 design noted that the min rule is tentative; this is where it becomes empirically testable. If the M&SO `mso_evidence` column flips to `medium` for every concept the moment `cost_model` (fallback path) features land, the readout has no useful discrimination. The slice should record whether min-confidence stays or is replaced.
- **Non-taxonomy concepts in alphabetical CSV order.** Slice 1 sorts by `concept_id`. ITER/NIF/Inertia at `00a-/00b-/00c-` sort to the top, which is informative for the reference comparison but may visually clutter the rest of the table. The design may instead want to suppress reference concepts from the live `scores/table.csv` and emit them only to a side-by-side `scores/xlsx_comparison.csv`. Either is fine; the decision is in design's hands.
- **Manual-extractor confidence semantics.** Slice 1 returns the on-disk confidence verbatim. For the three reference concepts, the analyst sets `confidence: medium` or `low` to honestly reflect "this was looked up from xlsx, not derived from a dossier." This will be the first non-`high` confidence in the feature corpus and may flip the evidence-quality column.

---

## Requirement Selection Notes

Normative requirements below cover the framework-level invariants this slice must satisfy and the empirical acceptance bar against the xlsx. Feature names, exact embedding logic, cost-model file parsing, the storage form of the corpus, and whether per-family weight shares are features-vs-weights are deliberately deferred to design — they are real choices with real tradeoffs and prescribing them here would prejudge the work.

---

## Requirements

### Functional Requirements

1. **FR-1**: The slice MUST add exactly seven embeddings under the `component_modularity` group label, one per xlsx subsystem (Core/Vessel, Driver/Coils, Blanket/FW, BOP, Fuel Cycle, Auxiliaries, Civil/Shielding). Each MUST return a 1–5 scalar.
2. **FR-2**: The `cost_model` extractor MUST be implemented to the same dispatcher signature as `taxonomy` and `manual`. When invoked for a concept whose `models/designs/{concept_id}/` directory does not exist, the extractor MUST return a family-default value with reduced confidence rather than raise.
3. **FR-3**: An evidence corpus file at `exploration/scoring_v2/evidence/corpus.yaml` MUST be created containing one entry per xlsx worked example (six entries), each carrying `id`, `value`, `source`, and `date`. Embeddings or tests that read the corpus MUST resolve references by ID through the corpus file, not by inlining xlsx values into code.
4. **FR-4**: Three non-taxonomy reference concepts (ITER, NIF, Inertia/LIFE) MUST exist as `features/*.yaml` files. Their features MUST be populated by the `manual` extractor. Their concept IDs MUST follow the slice-1 slug pattern `^[0-9]{2}[a-z]?-[a-z0-9-]+$`.
5. **FR-5**: For all six xlsx worked examples (three pre-existing + three reference concepts added in this slice), the slice-2 final Manufacturability & Scale-Out score derived from the `component_modularity` group alone (no family multiplier applied) MUST match the xlsx's "Final Modularity Score" within ±0.4 on the 1–5 scale — OR, if it does not, an implementation note MUST document the gap with embedding-level diagnosis and a proposed resolution.
6. **FR-6**: The slice-1 acceptance bar MUST continue to hold. Specifically: when the `component_modularity` group's weights are set to zero, the M&SO column for `01-hts-compact-tokamak`, `08-frc-w-direct-conversion`, and `10-large-scale-stellarator` MUST equal the slice-1 published values 2.90 / 4.80 / 1.50 within ±0.01.
7. **FR-7**: A schema and embedding versioning policy MUST be either implemented (e.g. a `version` field on `@embedding`, a documented bump rule) or explicitly deferred to a named future slice with rationale recorded in this slice's `design.md`.
8. **FR-8**: `score.py` MUST remain deterministic and LLM-free per slice-1 invariants. Two consecutive runs over unchanged inputs MUST produce byte-identical output. `embeddings/rulebook.py`, `score.py`, `lib/schema.py`, `lib/feature_io.py`, and the new `lib/extractors/cost_model.py` MUST NOT import any LLM client.
9. **FR-9**: The existing `extract.py --bulk-taxonomy` MUST continue to work additively against the slice-1 feature files — adding new taxonomy-derived features to existing files without overwriting any pre-existing feature block.

### Non-Functional Requirements

- **NFR-1**: `score.py` runtime SHOULD remain under 10 seconds across the now-larger concept set (38 taxonomy + 3 reference = 41) per the slice-1 soft target. Bulk-taxonomy extraction time is not constrained.
- **NFR-2**: Code uses `uv` for Python execution per project convention.

---

## Acceptance Criteria

### Core Functionality
- [ ] `uv run python exploration/scoring_v2/score.py` runs to completion against 41 concepts (38 taxonomy + 3 xlsx reference) and writes a CSV score table.
- [ ] The CSV's Manufacturability & Scale-Out column reflects contributions from both the `plant_level_modularity` and `component_modularity` groups for every concept.
- [ ] For the six xlsx worked examples, slice-2 score and xlsx final score appear side by side in the slice's implementation notes; deviations are inside ±0.4 OR documented with embedding-level diagnosis.
- [ ] When the `component_modularity` weights are zeroed in `weights/default.yaml`, M&SO for the three slice-1 reference concepts equals 2.90 / 4.80 / 1.50 within ±0.01.
- [ ] The `mso_evidence` column is no longer uniformly `high` for every concept once `cost_model`-fallback features land. (Discrimination is the test, not a specific distribution.)
- [ ] Two consecutive `score.py` runs over unchanged inputs produce byte-identical output.

### Quality & Integration
- [ ] All slice-1 tests under `tests/scoring_v2/test_extract.py`, `test_score_framework.py`, `test_embeddings.py` continue to pass.
- [ ] New tests cover: (a) the `cost_model` extractor's fallback path; (b) per-subsystem embedding band correctness on at least one worked example per subsystem; (c) the xlsx-collapse acceptance assertion (FR-5); (d) the slice-1-preservation assertion (FR-6); (e) evidence-quality column non-uniformity (FR / Success Criterion).
- [ ] V1 (`exploration/concept_analysis/`) untouched.
- [ ] Schema validator catches a deliberately malformed new feature in a test.

---

## Next-Stage Handoff

**Settled in this spec:**
- Seven embeddings, one per xlsx subsystem, grouped under the `component_modularity` label.
- The xlsx-collapse test (no family multiplier; embeddings must reproduce xlsx final scores within ±0.4) is the slice's empirical acceptance bar.
- `cost_model` extractor lands here; the dispatcher's unimplemented set collapses from two to one (`llm` remains).
- The evidence corpus lands here, populated with the six xlsx worked-example final scores.
- Three non-taxonomy reference concepts (ITER, NIF, Inertia/LIFE) land as the first exercise of the slice-1 architectural reservation that the concept universe is `features/*.yaml`, not `table.csv`.
- Slice-1 acceptance bars must continue to hold when component-modularity weights are zeroed.
- Versioning policy is decided or deferred-with-rationale this slice; no silent deferral.

**Design must figure out:**
- The feature decomposition for each of the seven subsystem embeddings — which features each consumes, types/enums, and which extractor (`taxonomy`, `cost_model`, `manual`) populates each.
- Whether per-family capex weight shares (the xlsx's W1..W7) are encoded as features absorbed into embedding outputs OR as a per-concept weight overlay; if the latter, what the file format looks like.
- The `cost_model` extractor's read path: what files in `models/designs/{concept_id}/` it parses (`model_setup.py` parameters, `model_output.md` CAS line items, or both), what fallback rule it uses when those files don't exist, and what confidence value the fallback returns.
- Whether the xlsx-collapse assertion is implemented as an embedding that consumes corpus entries OR as a pytest assertion against the corpus file — and where the comparison table is materialized for human review.
- Whether the three reference concepts appear in the live `scores/table.csv` or are routed to a separate `scores/xlsx_comparison.csv`.
- The shape of the `version` field on `@embedding` if versioning is adopted, and the bump rule if so.
- Concept IDs for the three reference concepts (slug-compatible with the existing pattern).

**Watch-outs for design:**
- The seven xlsx subsystems are not perfectly orthogonal — for instance, both "Driver / Coils" and "Auxiliaries" can be affected by HTS adoption. The slice-1 four-embedding rationale paragraphs (which explicitly named what each embedding did NOT cover) are the model to follow here. Without that discipline, double-counting between subsystems will silently inflate concept scores.
- Avoid letting `cost_model` become a second, parallel taxonomy. Its job is to make per-concept cost-structure data influence scoring *when it exists*, not to be a duplicate source for features that taxonomy already covers. The fallback case is the common case in this slice; the real case is the one slice 3+ will exercise — design the interface for that future, not for this slice's stubs.
- The xlsx's family multiplier is not a number to reverse-engineer. It is the *signal* of granularity gap. If your embeddings predict ITER too high (because the xlsx penalized it via the 0.85 multiplier), the right response is "which embedding should have caught more of that penalty," not "let's just multiply in 0.85."
- The first non-`high` confidence values land here. The min-confidence rule will flip evidence columns. Whether this is informative or noisy is judgement that should be recorded — slice 1 marked it tentative and the moment to revisit is now.
- The three reference concepts have no dossier and no V1 score. They exist purely to anchor the xlsx comparison. Resist the temptation to score them on dimensions beyond modularity in this slice; their other features should be `manual` with `confidence: low` and their other dimensions left at zero.

---

## Related Artifacts

- **Slice 1 (predecessor):** `.project/active/scoring-v2-modularity-slice/` — spec, design, plan, implementation notes. Slice-1 acceptance bars are constraints for this slice.
- **Design concept:** `.project/concepts/scoring-v2-design.md` — three-layer architecture, the original "first risk to de-risk" statement on xlsx-collapse.
- **Upstream concept:** `.project/concepts/scoring-framework-v2.md`.
- **Source of truth for embedding bands:** `.project/concepts/determinstic-scoring/Fusion_Modularity_Score.xlsx` (Driver Lookups, Worked Examples, Concept Multipliers tabs).
- **Outline:** `.project/concepts/determinstic-scoring/Deterministic Concept Scoring Outline 361aa1d01f24800588f5efaf3e6bc419.md`.
- **Existing cost-model designs (for `cost_model` extractor interface):** `models/designs/generic_ife/`, `models/designs/hif_ife/`. Neither is a scoring concept this slice; they are reference shapes for what the extractor will eventually parse.
- **V1 deterministic lookups (reference, not ported):** `exploration/concept_analysis/scripts/lib/scoring.py` — `detect_c2_category()` etc.
- **Design (to be created):** `.project/active/scoring-v2-component-modularity-slice/design.md`.
- **Plan (to be created):** `.project/active/scoring-v2-component-modularity-slice/plan.md`.

---

**Next Steps:** After approval, proceed to `/_my_design`.
