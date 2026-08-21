# Implementation Plan: Scoring V2 — `component_modularity` Embedding Group (Slice 2)

**Status:** Complete (with user-side reference concepts pending)
**Created:** 2026-05-17
**Last Updated:** 2026-05-17

## Source Documents
- **Spec:** `.project/active/scoring-v2-component-modularity-slice/spec.md`
- **Design:** `.project/active/scoring-v2-component-modularity-slice/design.md` ← all rating logic, CAS dict, weight wiring, invariants

## Implementation Strategy

**Phasing Rationale.** The slice has two genuinely uncertain bets (the `cost_model` extractor on real `model_output.txt` files, and the xlsx-collapse hypothesis) and a lot of mechanical transcription (seven rating functions, schema additions, weight YAML). Order phases so the cost-model parser and one end-to-end rating land before the bulk of the if/elif transcription, then validate xlsx-collapse last when everything is wired.

**Critical Path.**
1. Schema + taxonomy additions (`primary_heating`, `energy_capture`, seven `w_*`).
2. `cost_model` extractor parses one real `model_output.txt` and the `w_*` invariant holds (sum = 1.0).
3. One rating function (`vessel_rating`) wired end-to-end → score table contains a `component_modularity_aggregate` column for one concept.
4. Remaining six rating functions transcribed.
5. Weight wiring + slice-1 preservation test.
6. Reference concepts (ITER, NIF, Inertia/LIFE) added; xlsx-collapse acceptance test runs.

**First Proof Point.** Phase 2 — `cost_model` extractor produces seven `w_*` values for `01-hts-compact-tokamak` that sum to 1.0 ± 1e-6. If the CAS dict is wrong or `model_output.txt` is shaped differently than assumed, we find out before writing any embedding code.

**Overall Validation.** Each phase begins with a test stencil. Slice-1 tests (`test_extract.py`, `test_score_framework.py`, `test_embeddings.py`) are run after every phase to catch regressions. The two empirical bars (FR-5 xlsx-collapse, FR-6 slice-1 preservation) are asserted as pytest in `tests/scoring_v2/test_component_modularity.py`.

---

## Phase 1: Schema & taxonomy extension

### Goal
Register the new feature names (`primary_heating`, `energy_capture`, seven `w_*`) in `schema.yaml` and have the `taxonomy` extractor populate the two new taxonomy features. Nothing scores yet; this is the surface the next phases attach to.

### Assumption Under Test
The slice-1 schema and `extract.py --bulk-taxonomy` are additive in practice — adding entries to `schema.yaml` does not perturb existing feature blocks (FR-9).

### Test Stencil (Write First)
```python
# tests/scoring_v2/test_extract.py (extend)
def test_bulk_taxonomy_adds_new_features_without_touching_existing():
    # snapshot one feature file, run --bulk-taxonomy, diff
    before = read_features("01-hts-compact-tokamak")
    run_bulk_taxonomy()
    after = read_features("01-hts-compact-tokamak")
    assert after["primary_heating"]["value"] is not None
    assert after["energy_capture"]["value"] is not None
    # untouched fields preserved verbatim
    for k in before:
        assert after[k] == before[k]
```

### Changes Required
**See `design.md#features-per-concept` for the full feature list.**

- [ ] `exploration/scoring_v2/schema.yaml`: add `primary_heating`, `energy_capture` (extractor=taxonomy), and seven `w_vessel`/…/`w_civil` (extractor=cost_model, type=float, range [0,1]).
- [ ] `exploration/scoring_v2/lib/extractors/taxonomy.py`: ensure the two new taxonomy fields map to the right columns of `exploration/concept_analysis/table.csv` (inspect column headers; add column-name mapping if needed).
- [ ] Run `uv run python exploration/scoring_v2/extract.py --bulk-taxonomy` to populate the two new fields across all existing feature files.

### Validation
**Automated:**
- [ ] `uv run pytest tests/scoring_v2/test_extract.py` → all pass including new test.
- [ ] `uv run python exploration/scoring_v2/score.py` → still produces a CSV; M&SO column for slice-1 concepts unchanged (no new embeddings yet).

**Manual:**
- [ ] `git diff exploration/scoring_v2/features/` — only additions, no overwrites.

**What We Know Works After This Phase:** schema can grow; taxonomy extractor has the two new columns; slice-1 features untouched.

---

## Phase 2: `cost_model` extractor

### Goal
Parse `analyses/{cid}/model_output.txt` into seven `w_*` features using the design's `CAS_TO_SUBSYSTEM` dict. Sum-to-1 invariant proven on at least one real cost model.

### Assumption Under Test
The CAS dict transcribed from `01-hts-compact-tokamak/model_output.txt` actually maps every line item we care about, and the `$` parsing is robust enough for that file shape.

### Test Stencil (Write First)
```python
# tests/scoring_v2/test_cost_model.py (new)
def test_cost_model_extractor_sums_to_one():
    from exploration.scoring_v2.lib.extractors import cost_model
    weights = cost_model.compute_weights("01-hts-compact-tokamak")
    assert set(weights) == {"vessel","coils","blanket","bop","fuel_cycle","aux","civil"}
    assert abs(sum(weights.values()) - 1.0) < 1e-6

def test_cost_model_missing_file_returns_nothing():
    # design: writes nothing, no fallback
    assert cost_model.compute_weights("99-nonexistent") is None
```

### Changes Required
**See `design.md#the-cas--subsystem-dict` for the CAS dict and parser behavior.**

- [ ] `exploration/scoring_v2/lib/extractors/cost_model.py` (NEW): `CAS_TO_SUBSYSTEM`, `compute_weights(concept_id) -> dict|None`, dispatcher `extract(concept_id, feature_name, schema_entry) -> (value, provenance, confidence)`.
- [ ] Register `cost_model` in `lib/extractors/__init__.py` dispatcher.
- [ ] `extract.py` invocation path: enable `cost_model` extractor in the bulk-extraction loop (mirror slice-1 taxonomy path).
- [ ] Run extraction for the three concepts with cost models (`01-hts-compact-tokamak`, plus any others under `analyses/`).
- [ ] Log unrecognized CAS codes per design risk note.

### Validation
**Automated:**
- [ ] `uv run pytest tests/scoring_v2/test_cost_model.py` → pass.
- [ ] Existing tests still pass.

**Manual:**
- [ ] Inspect `features/01-hts-compact-tokamak.yaml` — seven `w_*` present, sum ≈ 1.0.
- [ ] Inspect extractor log for unrecognized codes; if any, decide ignore-vs-add-to-dict.

**What We Know Works After This Phase:** cost-model parser produces a valid weight vector for at least one real concept; missing-file case is silent (no fallback).

---

## Phase 3: Rating embeddings + aggregate

### Goal
All seven `*_rating` functions plus `component_modularity_aggregate` registered in `rulebook.py`. Each rating returns an int in [1,5]. Aggregate returns `None` when any `w_*` is absent.

### Assumption Under Test
The if/elif structure in design.md is consistent — no rating reads a field that isn't in the schema; band coverage hits every concept in `table.csv`.

### Test Stencil (Write First)
```python
# tests/scoring_v2/test_component_modularity.py (new)
@pytest.mark.parametrize("rating_name", [
    "vessel_rating","coils_rating","blanket_rating","bop_rating",
    "fuel_cycle_rating","aux_rating","civil_rating"])
def test_rating_in_band(rating_name):
    from exploration.scoring_v2.embeddings import rulebook
    fn = rulebook.REGISTRY[rating_name]
    for cid in all_taxonomy_concepts():
        val = call_with_features(fn, cid)
        assert isinstance(val, int) and 1 <= val <= 5

def test_aggregate_none_when_weights_missing():
    # concept with no model_output.txt → aggregate is None
    assert score_one("10-large-scale-stellarator", "component_modularity_aggregate") is None
```

### Changes Required
**See `design.md#the-7-rating-functions` and `design.md#the-aggregate-embedding-and-the-mso-blend` for the full code.**

- [ ] `exploration/scoring_v2/embeddings/rulebook.py`: add the seven `@embedding` rating functions under group `component_modularity`, transcribed verbatim from design.
- [ ] Add `component_modularity_aggregate` embedding (consumes seven ratings + seven `w_*`, returns weighted sum or `None`).
- [ ] Drop `primary_heating` from the feature set if no rating consumes it (per design risk note).

### Validation
**Automated:**
- [ ] `uv run pytest tests/scoring_v2/test_component_modularity.py::test_rating_in_band` → pass.
- [ ] All slice-1 tests still pass.
- [ ] `uv run python exploration/scoring_v2/score.py` → CSV has new columns; aggregate is `None`/blank for concepts without `model_output.txt`.

**Manual:**
- [ ] Spot-check one concept per confinement family (MFE/IFE/MIF) for plausible band values.

**What We Know Works After This Phase:** rating layer end-to-end; aggregate composes ratings × weights; `None` propagation correct.

---

## Phase 4: Weight wiring + slice-1 preservation

### Goal
`weights/default.yaml` updated for the 50/50 blend; slice-1 preservation bar passes byte-identically when `component_modularity_aggregate` weight is zeroed and slice-1 plant-level weights are restored.

### Assumption Under Test
The blend in `design.md#the-aggregate-embedding-and-the-mso-blend` does not perturb slice-1 acceptance numbers (Helion 4.80, CFS 2.90, Stellarator 1.50) when the aggregate weight is set to 0.

### Test Stencil (Write First)
```python
def test_slice1_preservation_when_component_modularity_zeroed():
    with patched_weights({"component_modularity_aggregate": 0.0,
                          "min_viable_device_scale": 0.30,
                          "hardware_topology_complexity": 0.30,
                          "unit_multiplicity": 0.20,
                          "subsystem_stack_burden": 0.20}):
        row = score_concept("01-hts-compact-tokamak")
        assert abs(row["manufacturability_scale_out"] - 2.90) < 0.01
        # similarly Helion 4.80, Stellarator 1.50

def test_score_determinism():
    run1 = run_score_py()
    run2 = run_score_py()
    assert run1 == run2
```

### Changes Required
**See `design.md#the-aggregate-embedding-and-the-mso-blend` for the YAML structure.**

- [ ] `exploration/scoring_v2/weights/default.yaml`: add `component_modularity_aggregate: 0.50`, halve slice-1 weights to 0.15/0.15/0.10/0.10.

### Validation
**Automated:**
- [ ] `uv run pytest tests/scoring_v2/test_component_modularity.py::test_slice1_preservation_when_component_modularity_zeroed` → pass.
- [ ] Determinism test → pass.

**Manual:**
- [ ] `uv run python exploration/scoring_v2/score.py` and inspect `scores/table.csv` — M&SO for the three slice-1 concepts is different from slice-1 baseline (expected) but reasonable.

**What We Know Works After This Phase:** FR-6 holds. Slice-1 results are recoverable by weight edit alone.

---

## Phase 5: Reference concepts + xlsx-collapse acceptance

### Goal
Three reference concepts added to `table.csv` and `analyses/`. xlsx-collapse test runs against six worked examples and either passes within ±0.4 or produces a documented negative-result write-up.

### Assumption Under Test
The xlsx-collapse hypothesis: the seven embeddings reproduce the xlsx's final score within ±0.4 *without* applying the family multiplier.

### Test Stencil (Write First)
```python
XLSX_FINAL = {
    "01-hts-compact-tokamak": 5.0,
    "08-frc-w-direct-conversion": 4.65,
    "10-large-scale-stellarator": 2.18,
    "00a-iter": 1.4,
    "00b-nif": 1.83,
    "00c-inertia-life": 4.15,
}

@pytest.mark.parametrize("cid,xlsx", XLSX_FINAL.items())
def test_xlsx_collapse(cid, xlsx):
    score = score_concept(cid)["component_modularity_aggregate"]
    assert abs(score - xlsx) <= 0.4, f"{cid}: got {score}, xlsx {xlsx}"
```

### Changes Required
**See `design.md#the-reference-concepts-iter-nif-inertia-life` and `design.md#acceptance-test`.**

- [ ] User-side work (flagged in `design.md`): three new rows in `exploration/concept_analysis/table.csv` for `00a-iter`, `00b-nif`, `00c-inertia-life`, populated from xlsx Concept Multipliers + public info.
- [ ] User-side: `analyses/00a-iter/model_output.txt`, `analyses/00b-nif/model_output.txt`, `analyses/00c-inertia-life/model_output.txt` (per no-fallback rule).
- [ ] Re-run `extract.py --bulk-taxonomy` and `cost_model` extraction across all 41 concepts.
- [ ] Confirm xlsx final-score numbers (5.0/4.65/2.18/1.4/1.83/4.15) against the xlsx — read from the actual file before committing the test.
- [ ] Run xlsx-collapse test. If it fails for any concept, write the negative-result note in `implementation_notes.md` per FR-5 (which embedding under-discriminates, which feature axis, proposed fix or deliberate retention of family multiplier).

### Validation
**Automated:**
- [ ] `uv run pytest tests/scoring_v2/test_component_modularity.py` → xlsx-collapse passes OR is documented as deliberate negative result.
- [ ] Full slice-1 test suite still green.
- [ ] `mso_evidence` column non-uniform across concepts (success criterion).

**Manual:**
- [ ] `scores/table.csv` includes 41 rows; M&SO populated by both groups for concepts with a cost model.
- [ ] Side-by-side comparison table (slice-2 vs xlsx) appended to `implementation_notes.md`.

**What We Know Works After This Phase:** FR-5 either passes or has a documented redirect. Slice is "done" per spec.

---

## Phase 6: Versioning policy decision

### Goal
Settle FR-7: either add `version=` to `@embedding` and document the bump rule, or write the explicit deferral note (target slice, rationale).

### Changes Required
- [ ] Add `version:` field to `@embedding` decorator OR append a "Versioning deferral" section to `design.md` naming the slice this lands in. Default: defer with note, since slice 2 doesn't exercise version-skew.

### Validation
- [ ] Decision recorded in `design.md` and `implementation_notes.md`.

**What We Know Works After This Phase:** no silent deferral; FR-7 satisfied.

---

## Environment Setup

**See CLAUDE.md.** Use `uv run python …` and `uv run pytest …`.

## Risk Management

**See `design.md#risks`.**

- **Phase 2 risk:** CAS dict drift. Mitigation: log unrecognized codes; expand the dict only when a new code appears.
- **Phase 5 risk:** xlsx-collapse fails on Type One stellarator. Mitigation: documented negative result is acceptable per FR-5; diagnose at the coils/blanket rating level, propose tightening.
- **Phase 3 risk:** band coverage gap (a concept hits no `if` branch). Mitigation: every rating ends with a `return 3` default; parametrized in-band test enforces 1..5.

## Implementation Notes

Full per-phase write-up, FR-by-FR acceptance, six-concept xlsx-collapse table,
deviation log, and CFS-ARC gap diagnosis live in
[`implementation_notes.md`](implementation_notes.md).

Summary: 26 passed / 3 skipped (pending user-side reference concepts) /
1 xfailed (documented CFS gap per FR-5 negative-result path). Slice-1
preservation exact (delta = 0.0000 / concept) under `weights/slice1.yaml`.

---

**Status**: Complete (framework). Pending: user adds `00a-iter`, `00b-nif`,
`00c-inertia-life` rows and `analyses/.../model_output.txt` to resolve the
three skipped xlsx-collapse parametrizations.
