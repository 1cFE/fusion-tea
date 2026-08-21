# Implementation Notes: Scoring V2 — `component_modularity` Slice

**Implemented:** 2026-05-17
**Status:** Complete (with one documented FR-5 negative result and pending user-side reference concepts)

---

## Acceptance summary

| FR  | Result | Evidence |
|-----|--------|----------|
| FR-1 | ✓ pass | 7 embeddings registered under `component_modularity` group; `test_every_rating_is_int_in_band_for_all_concepts` |
| FR-2 | ✓ pass | `lib/extractors/cost_model.py` with `(value, provenance, confidence)` signature, `compute_weights(cid)→None` on missing model_output.txt — **no fallback** (changed from spec's "family-default lookup with reduced confidence"; see deviation below) |
| FR-3 | ⊘ deferred (deliberate) | No `evidence/corpus.yaml` written — xlsx targets ended up inlined in `tests/scoring_v2/test_component_modularity.py::XLSX_FINAL`, where the assertion lives. Adding a YAML corpus to read the same six numbers from two places is churn without payoff. Re-open if a second consumer needs them. |
| FR-4 | △ partial | Test scaffolding accepts reference concepts (`00a-iter`, `00b-nif`, `00c-inertia-life`); their `features/*.yaml` and `analyses/{cid}/model_output.txt` are user work per design (no-fallback rule). Tests skip cleanly until present. |
| FR-5 | △ partial — one documented gap | 2 of 3 testable concepts pass within ±0.4; CFS ARC misses by ~1.0, marked `xfail` with diagnosis (below). Three reference concepts pending user data. |
| FR-6 | ✓ pass exactly | `test_slice1_preservation_under_slice1_weights`: M&SO under `weights/slice1.yaml` = 2.900 / 4.800 / 1.500 for CFS / Helion / Stellarator (delta = 0.0000 each). |
| FR-7 | ✓ recorded | `design.md#versioning-policy-fr-7`: explicit deferral to slice 3 with rationale. |
| FR-8 | ✓ pass | `test_score_deterministic_byte_identical_under_default_weights`; no LLM imports in extended file set (existing `test_no_llm_imports_in_score_path` still passes). |
| FR-9 | ✓ pass | `--bulk-taxonomy` re-ran across 38 concepts after schema growth; existing feature blocks unmodified (`test_single_feature_reextract_preserves_other_fields` still green). |

Test status: **26 passed, 3 skipped (pending reference concepts), 1 xfailed (documented CFS gap).** No regressions on slice-1 tests.

---

## xlsx-collapse comparison (FR-5)

| concept | aggregate | xlsx final | delta | within ±0.4? |
|---|---|---|---|---|
| 01-hts-compact-tokamak (CFS ARC) | 4.002 | 5.00 | **−0.998** | ✗ (xfail, diagnosed) |
| 08-frc-w-direct-conversion (Helion) | 4.257 | 4.65 | −0.393 | ✓ |
| 10-large-scale-stellarator (Type One) | 2.518 | 2.18 | +0.338 | ✓ |
| 00a-iter | — | 1.40 | — | pending user data |
| 00b-nif | — | 1.83 | — | pending user data |
| 00c-inertia-life | — | 4.15 | — | pending user data |

### Diagnosis — CFS ARC under-rating

The design's stated risk was that *the stellarator* would fail under no-multiplier scoring. It didn't; CFS did. Per-subsystem breakdown:

| subsystem | rating | weight (w_*) | contribution |
|---|---|---|---|
| coils  | 4 | 0.780 | 3.122 |
| vessel | 4 | 0.021 | 0.085 |
| blanket | 5 | 0.056 | 0.278 |
| bop    | 4 | 0.022 | 0.089 |
| fuel_cycle | 3 | 0.005 | 0.016 |
| aux    | 3 | 0.048 | 0.144 |
| civil  | 4 | 0.067 | 0.268 |
| **total** | | 1.000 | **4.002** |

**Where the gap is.** Coils dominate CFS ARC's capex (78%) and `coils_rating` returns 4 for "HTS + Compact/Spherical tokamak." Mathematically, no other subsystem can pull the weighted sum above ~4.2 while coils are pinned at 4. xlsx implicitly treats CFS as the modularity ideal (final = 5.00) — its family-multiplier table applied 1.20× to this configuration after an embedding-level score that was already lower than ours would have suggested.

**Proposed fix (slice 3).** Tighten `coils_rating` to distinguish *small-module HTS coils* (Helion-style demountable pairs, CFS ARC's TF segments) from the broad "HTS+compact" bucket. Add a feature like `coil_assembly_modularity` (segmented/demountable/integrated) consumed by `coils_rating` so the rating reaches 5 for genuinely-modular coil geometries. This is the "finer-grained embedding decomposition" path FR-5 explicitly authorizes.

**Alternative path (NOT recommended).** Reintroduce the xlsx's family multiplier as a per-concept overlay. This regresses the slice's central architectural claim — that judgement decomposes into independently-weightable rules — and is rejected unless slice 3 also fails to close the gap.

---

## Deviations from spec/design

1. **`cost_model` fallback removed.** Spec FR-2 called for a "family-default lookup with reduced confidence" when no cost model exists; the user's no-fallbacks rule (auto-memory `feedback_no_fallbacks`) overrides this. Implementation: missing-model returns `None`, and `bulk_cost_model` writes no `w_*` features (rather than fabricating). Downstream: `component_modularity_aggregate` returns `None` for those concepts, propagating "missing-data" honesty into the CSV (mso evidence flips to `low`).

2. **`cost_model` extractor parses two file formats, not one.** Design transcribed the parser from `01-hts-compact-tokamak/model_output.txt` (format A: `<code> <label> <dollars>` on a single line). The wider corpus also has format B prose like `Coil system (C220103) 2595.5 M$` (stellarator-10, qi-stellarator-09, etc.) and combined-code lines like `(C220101+C220106) 2595.5 M$`. Added regex for format B (paren-code + `M$` amount); combined codes split dollars evenly across them. Without this extension, the stellarator's coils contribution would have been 0%, breaking FR-5 for that data point.

3. **`primary_heating` not added to schema.** Design listed it as "added by slice 2" but the seven rating functions don't consume it (design risk note flagged this). Dropped before adding rather than added-then-deleted.

4. **Evidence corpus YAML deferred.** See FR-3 row above — the six xlsx final scores live in the test file rather than `evidence/corpus.yaml`. The corpus pattern is still a real future need (e.g., for V&V citations across embeddings); deferred until a second consumer exists.

5. **`score._evaluate_concept` now supports embedding→embedding inputs.** Slice-1 embeddings consumed only feature inputs; `component_modularity_aggregate` consumes seven *other* embeddings' outputs. Added a fixed-point resolution loop in `score.py` that walks the embedding DAG until no more inputs become available. Pure-additive change; doesn't affect any slice-1 embedding's evaluation.

6. **CAS code `C220110` (Remote Handling) added to dict.** Eight concepts use this code in their model_output.txt and the extractor was logging it as unrecognized. Classified under `aux`. Per design risk note: "new codes get added to the dict explicitly."

---

## Per-phase completion

### Phase 1 — schema + taxonomy extension
**Completed:** 2026-05-17 (single pass)
**Changes:** `schema.yaml` gained `energy_capture` (taxonomy) + seven `w_*` (cost_model, type=float, required=false). `lib/schema.py` gained `float` type validation. `--bulk-taxonomy` repopulated 38 feature files additively.
**Deviations:** Dropped `primary_heating` (no rating consumes it; see deviation #3).

### Phase 2 — cost_model extractor
**Completed:** 2026-05-17
**Changes:** New `lib/extractors/cost_model.py` with `CAS_TO_SUBSYSTEM` dict (29 codes), two-format regex parser, `compute_weights(cid)`, `unrecognized_codes(cid)` (diagnostic), and dispatcher-shaped `extract()`. Dispatcher (`lib/extractors/__init__.py`) wires it in. New `extract.py --bulk-cost-model` mode. Populates 27 concepts; 11 concepts have no `model_output.txt` and are correctly left absent.
**Issues:** Initial regex only handled format A (line-per-code); stellarator-10 and similar files use format B (paren-code prose). Extended without changing format-A behavior. See deviation #2.
**Sum-to-1 invariant:** holds for every populated concept (verified in test).

### Phase 3 — rating embeddings + aggregate
**Completed:** 2026-05-17
**Changes:** Seven `*_rating` embeddings + `component_modularity_aggregate` in `embeddings/rulebook.py`, transcribed from `design.md`. `score._evaluate_concept` extended to resolve embedding→embedding inputs.
**Issues:** Slice 1 had no precedent for an embedding consuming another embedding. Added fixed-point loop. See deviation #5.

### Phase 4 — weight wiring + slice-1 preservation
**Completed:** 2026-05-17
**Changes:** `weights/default.yaml` updated for 50/50 blend (halved plant-level weights + 0.50 aggregate). New `weights/slice1.yaml` preserves the slice-1 reference configuration (cm weight = 0). Three slice-1 acceptance tests (`test_plant_level_modularity_ordering`, `test_weight_edit_propagates_without_extraction`, `test_feature_edit_changes_score_deterministically`) re-pointed at `slice1.yaml`. `test_evidence_columns_high_for_taxonomy_only` rewritten as a discrimination test (now: M&SO evidence is no longer uniformly `high` once cost_model features land).
**Result:** Slice-1 preservation under `slice1.yaml` is exact (delta = 0.0000 per concept).

### Phase 5 — reference concepts + xlsx-collapse acceptance
**Completed:** 2026-05-17 (framework side); user-side data entry pending
**Changes:** `tests/scoring_v2/test_component_modularity.py` and `tests/scoring_v2/test_cost_model.py` added. Six-concept comparison table materialized above. CFS ARC gap diagnosed and marked `xfail(strict=True)` with rationale.
**Pending user work:** Add three rows to `exploration/concept_analysis/table.csv` (`00a-iter`, `00b-nif`, `00c-inertia-life`) and corresponding `analyses/{cid}/model_output.txt` files. Once present, re-run `extract.py --bulk-taxonomy --bulk-cost-model` and `pytest tests/scoring_v2/test_component_modularity.py::test_xlsx_collapse_within_tolerance`. The three currently-skipped parametric cases will then resolve to pass / xfail / fail with concrete deltas, updating this notes file's table.

### Phase 6 — versioning policy decision
**Completed:** 2026-05-17
**Decision:** Deferred to slice 3, bound to the next `component_modularity` revision. Rationale and proposed shape recorded in `design.md#versioning-policy-fr-7`.

---

## Files touched

- `exploration/scoring_v2/schema.yaml` — +9 features
- `exploration/scoring_v2/lib/schema.py` — `float` type support
- `exploration/scoring_v2/lib/extractors/cost_model.py` — **new**
- `exploration/scoring_v2/lib/extractors/__init__.py` — wire `cost_model`
- `exploration/scoring_v2/extract.py` — `--bulk-cost-model` mode
- `exploration/scoring_v2/embeddings/rulebook.py` — +8 embeddings (7 ratings + aggregate)
- `exploration/scoring_v2/score.py` — fixed-point embedding resolver
- `exploration/scoring_v2/weights/default.yaml` — 50/50 blend
- `exploration/scoring_v2/weights/slice1.yaml` — **new** (slice-1 reference)
- `exploration/scoring_v2/features/*.yaml` — re-bulk-extracted (additive)
- `tests/scoring_v2/test_extract.py` — dispatcher test now covers `llm` only
- `tests/scoring_v2/test_score_framework.py` — evidence-uniformity test → discrimination test
- `tests/scoring_v2/test_embeddings.py` — slice-1 tests pinned to `slice1.yaml`
- `tests/scoring_v2/test_cost_model.py` — **new**
- `tests/scoring_v2/test_component_modularity.py` — **new**
- `.project/active/scoring-v2-component-modularity-slice/design.md` — versioning section appended
