# Spec: Explorer Rework Unblock (Concept-Analysis Rework, Item 10 Phases 3-5)

**Status:** Implemented
**Owner:** Reid W
**Created:** 2026-06-05
**Complexity:** LOW (revised from MEDIUM after FR-A4 removal — see design Appendix A)
**Branch:** TBD (single PR off `main`)
**Epic:** [`epic_concept_analysis_rework.md`](../../backlog/epic_concept_analysis_rework.md), Item 10 (deferred Phases 3-5)
**Research:** [`20260605-081423_explorer-rework-dependency-gap-map.md`](../../research/20260605-081423_explorer-rework-dependency-gap-map.md)

---

## Work Item Summary

Make the concept explorer's data layer compatible with the post-rework `model_setup.py` shape so that extraction and slider recompute work again. Today both `extract_explorer_data.py` and `server.py`'s `/api/compute` require a module-level `result` object that the three-forward contract deliberately removed; every concept fails at the first check. This work item is the narrow unblock: switch the explorer's authoritative result to `result_1gw`, fix the slider's `forward()` call to match Item 4's two-knob library API, and tolerate the 12 still-old-shape concepts (those with `review.md` instead of `analysis.md`) with a warning rather than a hard fail. No new ConceptData fields, no UI changes, no new artifacts ingested — that's Item B (`explorer-rework-enrich`).

## Why This Matters Now

The concept-analysis rework merged in PR #44 and was further refreshed in PR #46. The explorer was Phase-1-2 adapted as part of Item 10 (it knows about `result_1gw`, `Comparison-Status`, `P-Native`, and `verify_two_knob`), but Phases 3-5 — the cleanup that *removes* the legacy `result` requirement and finishes the compute-path migration — were deferred. The explorer is now broken on every concept including ones that were already passing pre-rework. Running `uv run python exploration/concept_explorer/extract_explorer_data.py` fails on concept 01 with `ERROR: 01: model_setup.py must define module-level 'model' and 'result'`. Until this lands, the explorer ships zero data, and any work that depends on the explorer (comparison view, parameter index, taxonomy similarity reports) is blocked.

## Key Bets / Constraints

- **Bet:** `result_1gw` is the right single authoritative result for the explorer — the cross-concept 1 GWe NOAK projection. `generic` and `native` are analyst-internal (shown in `print_cas_breakdown` stdout) and not surfaced in the JSON.
- **Constraint:** The three-forward contract is the contract. The explorer adapts to the helper-defined shape; the helper does not change.
- **Constraint:** Item 4's library API is the source of truth for `forward()`. The server's `_forward_with_overrides` must match: non-integer `n_mod` allowed.
- **Constraint:** The 12 `review.md` (old-shape) concepts (04, 05, 06, 07, 08, 09, 10, 11, 12, 13, 18, 20a) are tolerated with a UserWarning naming the missing frontmatter fields — they extract, they just carry the defaults (Confinement-Family=NONSTANDARD, name=dir name, etc.). They are not required to be regenerated as a prerequisite for this work item.
- **Non-goal:** Ingest any of the new rework-era artifacts (`design-points/baseline.yaml`, `critic_review_*.md`, the `tables/*.csv` files). That is the additive Item B (`explorer-rework-enrich`).
- **Non-goal:** Any UI change. The frontend keeps reading the same ConceptData shape it does today. UI work follows separately after both data-layer items land.
- **Non-goal:** Regeneration of the 12 old-shape concepts (Item 11 of the rework epic).
- **Non-goal:** Slider-semantics redesign. This spec preserves the current slider mental model — moving a sensitivity parameter re-runs `forward()` with that param overridden, base params taken from `result_1gw.params`, **and the analyst's `cost_overrides` registry is not re-applied** (matches `model.sensitivity()` baseline; pre-existing behavior). Under the rework this produces a visible discontinuity between the JSON's headline LCOE and the first slider-recomputed LCOE for any concept with a non-trivial override registry. Deliberately deferred to follow-up spec [`explorer-slider-override-semantics`](../explorer-slider-override-semantics/spec.md).

---

## Business Goals

### Why This Matters

The explorer is the primary surface for cross-concept comparison and the data layer for downstream work (taxonomy similarity, comparison view, parameter index). With it broken, every consumer of `data/*.json` is stale and any work product that depends on apples-to-apples LCOE comparison stalls. The rework epic itself implicitly relies on the explorer working — the "every concept's `result_1gw` is reached by the same two-knob mechanism" success criterion is only observable through the explorer.

### Success Criteria

- [ ] `uv run python exploration/concept_explorer/extract_explorer_data.py --skip-narrative` runs to completion on all 40 concepts under `exploration/concept_analysis/analyses/` with no fatal errors. Per-concept warnings are acceptable.
- [ ] Server starts (`uv run python exploration/concept_explorer/server.py`) and serves `/api/manifest`, `/api/concepts/{id}`, and `/api/parameter_index` for the loaded set.
- [ ] `/api/compute` returns a 200 with a recomputed `CostModelData` for at least one costingfe-backed concept (concept 01 is the canonical check).
- [ ] The 12 old-shape concepts (04, 05, 06, 07, 08, 09, 10, 11, 12, 13, 18, 20a) extract successfully and emit a clear UserWarning naming the missing frontmatter (no `analysis.md` present).
- [ ] No regression in existing test suite (`uv run python -m pytest exploration/concept_explorer/tests/ -v`).

### Priority

P0. Blocks all explorer-dependent work.

---

## Problem Statement

### Current State

- `extract_explorer_data.py:301-306` requires module-level `result`. The three-forward contract removed `result`; concepts now expose `model`, `generic`, `native`, `result_1gw`. Every concept fails this check.
- `server.py:553-555` (`_compute_cached`) requires the same `result` symbol. `/api/compute` is fully broken.
- `server.py:_forward_with_overrides` (lines 141-165) integer-casts `n_mod` at line 159 (`int(float(params.get("n_mod", 1)))`), but Item 4 made the library accept non-integer `n_mod`. (The cast happens to be safe today — the helper rounds `n_mod` before it lands in `result_1gw.params` — but the cast is a stale hardcoding worth removing as hygiene.)
- The 12 concepts that still have `review.md` instead of `analysis.md` have no frontmatter at all. The extractor today would silently fall through to defaults (which is the desired behavior), but the assumption is undocumented and produces no signal that the concept is in a degraded state.

### Desired Outcome

The extractor and server treat `result_1gw` as the authoritative `ForwardResult` for every concept. The compute endpoint's `forward()` call matches Item 4's library API: non-integer `n_mod` is preserved. Old-shape concepts extract with a warning that names the missing frontmatter so the degraded state is visible to whoever runs extraction.

---

## Scope

### In Scope

- `exploration/concept_explorer/extract_explorer_data.py`:
  - Remove the module-level `result` requirement (currently lines 301-306).
  - `result_1gw` is the single result the extractor reads. The `effective_result = result_1gw` assignment at line 324 stays.
  - Emit a single concise UserWarning per concept missing `analysis.md` that names what fell back to defaults (name, Confinement-Family, Comparison-Status, P-Native).
- `exploration/concept_explorer/server.py`:
  - `_compute_cached` (lines 530-567) reads `result_1gw`, not `result`. `base_params = result_1gw.params`.
  - `_forward_with_overrides` (lines 141-165): drop the integer cast on `n_mod` at line 159. (Hygiene — today the helper rounds before this point, so the cast is a no-op; removing it eliminates a stale hardcoding.)
- Tests under `exploration/concept_explorer/tests/`: existing tests updated to the new contract; one new test (or extension) that loads a real concept (01) end-to-end and asserts `_compute_cached` returns successfully.

### Out of Scope

- Any new `ConceptData` field (archetype, archetype_fit, grounding_confidence, design_point_*, fit_rationale, etc.) — these belong to Item B (`explorer-rework-enrich`).
- Ingesting `design-points/baseline.yaml`, `critic_review_*.md`, or any of the `exploration/concept_analysis/tables/*.csv` files.
- UI changes (templates, JS, asterisk styling, comparison view, parameter cards).
- Regenerating the 12 old-shape concepts onto the new analysis.md shape (Item 11 of the rework epic).
- Reconsidering slider semantics under the two-knob mechanism. The mental model stays "drag a sensitivity parameter → forward() recomputes with that override." If that turns out to be the wrong UX, address it as follow-up after both A and B land.

### Edge Cases & Considerations

- A concept whose `P_native > 1000` (e.g. Helias-class at 1500 MWe) collapses to `n_mod = 1` for `result_1gw` per the helper (`model_setup_helpers.py:169`). The compute path must not double-clamp.
- Freeform concepts (concept 03 and others routed `freeform-deferred`) go through `extract_standalone`, not `extract_costingfe`, and have `result_1gw = None` at module level. That path is unaffected by this work item; verify no regression.
- Concept 03's `Comparison-Status` is `freeform-deferred` per frontmatter. Routing at lines 904-918 must continue to work; this work item should not perturb it.
- A concept with `analysis.md` present but missing `P-Native` in frontmatter: `verify_two_knob` is gated on `if p_native is not None` (line 321) and skipped. Preserve that tolerance — it's how the 12 old-shape concepts (once they get `analysis.md` regenerated but without P-Native) would degrade gracefully.

---

## Requirement Selection Notes

Requirements below capture the four things that *must* be true for the explorer to work again under the rework contract: read `result_1gw` not `result` (extractor and server), drop the stale integer cast on `n_mod`, and warn on missing frontmatter. Anything else (new fields, new artifacts, UI, slider rework) is intentionally deferred to a later spec so this PR stays narrow and reviewable.

**FR-A4 (override_reference_mw passthrough) was removed in revision 2** after verification showed the library does not reflect `override_reference_mw` back into `result.params`, making any "pass it through if present" branch unreachable in production. The motivating concern — that slider recompute would mis-scale analyst overrides — is real but pre-existing and orthogonal: slider recompute does not re-apply `cost_overrides` at all (matches `model.sensitivity()` baseline), so `override_reference_mw` would have nothing to scale even if it were available. The full discontinuity issue is tracked in [`explorer-slider-override-semantics`](../explorer-slider-override-semantics/spec.md).

---

## Requirements

### Functional Requirements

1. **FR-A1**: `extract_explorer_data.py` SHALL NOT require a module-level `result` symbol from any concept's `model_setup.py`. Concepts that expose `model` and `result_1gw` MUST extract successfully.
2. **FR-A2**: `server.py`'s `_compute_cached` SHALL use `result_1gw.params` as the base params for the `forward()` re-invocation. It MUST NOT require `result`.
3. **FR-A3**: `_forward_with_overrides` SHALL accept non-integer `n_mod` and pass it through to `model.forward()` unmodified (no integer cast).
4. **FR-A4**: When a concept directory has `model_setup.py` but no `analysis.md`, extraction SHALL succeed using directory-name and enum defaults, and SHALL emit a single UserWarning naming the concept ID and the fields that fell back to defaults (at minimum: name, Confinement-Family, Comparison-Status, P-Native).

### Non-Functional Requirements

- No regression in extraction wall-clock time for the costingfe pathway (the change is structural, not algorithmic).
- No new external dependencies.

---

## Acceptance Criteria

### Core Functionality

- [ ] FR-A1: extraction completes on all 28 rework-aligned concepts (those with `analysis.md`) with no fatal error.
- [ ] FR-A2 + FR-A3: `POST /api/compute` with body `{"concept_id": "01", "overrides": {"availability": 0.92}}` returns a 200 with a valid `CostModelData`. The recomputed `n_mod` is passed to `forward()` without integer casting.
- [ ] FR-A4: extraction of concept 04 (and the other 11 old-shape concepts) succeeds and emits the expected warning listing the fields that fell back to defaults.
- [ ] No regression in `/api/manifest`, `/api/concepts/{id}`, `/api/parameter_index` payload shapes.

### Quality & Integration

- [ ] Existing test suite passes: `uv run python -m pytest exploration/concept_explorer/tests/ -v`.
- [ ] At least one test exercises the end-to-end real-concept compute path (load concept 01, recompute with a small override, assert non-zero result).
- [ ] Manual smoke: launch server on port 8421, open `/` and `/concept/01`, confirm rendering doesn't 500.

---

## Next-Stage Handoff

**Settled in this spec:**
- `result_1gw` is the explorer's authoritative result.
- `generic` and `native` stay analyst-internal (print_cas_breakdown stdout only).
- Slider mental model unchanged: drag a sensitivity param → forward() recomputes.
- Old-shape concepts (12 of them) are first-class extractable with empty-frontmatter warnings.

**Design must figure out:**
- Whether `_compute_cached`'s base_params should snapshot `result_1gw.params` *as-is* (including `n_mod`) or whether `n_mod` should be treated as a slider-overridable param. (The current code allows any param to be overridden; preserve that, but flag the implication.)
- Whether the warning emitted by FR-A4 should also include a one-line hint pointing at the rework epic (Item 11) so an operator sees what to do about it.

**Watch-outs for design:**
- The LRU cache key `(concept_id, frozenset(overrides.items()))` already excludes `result_1gw.params` — the base params change between extraction time and compute time only if the concept's `model_setup.py` is re-imported. Safe today; document the assumption.
- Don't accidentally turn the warning into a per-iteration noise source. One warning per concept per extraction run.
- The narrative-extraction prompt's `model_output_section` reads `model_output.txt` (now produced by `print_cas_breakdown` rather than a freeform print). The text format is helper-owned and stable; no change needed here, but verify the prompt still receives meaningful content.

---

## Related Artifacts

- **Epic:** [`.project/backlog/epic_concept_analysis_rework.md`](../../backlog/epic_concept_analysis_rework.md) — Item 10 (Phases 3-5, deferred).
- **Research:** [`.project/research/20260605-081423_explorer-rework-dependency-gap-map.md`](../../research/20260605-081423_explorer-rework-dependency-gap-map.md) — full dependency inventory and gap matrix.
- **Prior spec (Phases 1-2):** [`.project/active/concept-rework-explorer-pilot/spec.md`](../concept-rework-explorer-pilot/spec.md).
- **Three-forward contract:** `exploration/concept_analysis/scripts/lib/model_setup_helpers.py` docstring (lines 1-31).
- **Frontmatter contract:** `exploration/concept_analysis/scripts/lib/frontmatter.py:114-173`.
- **Follow-up (additive):** [`.project/active/explorer-rework-enrich/spec.md`](../explorer-rework-enrich/spec.md) (Item B, depends on this).
- **Follow-up (deferred slider semantics):** [`.project/active/explorer-slider-override-semantics/spec.md`](../explorer-slider-override-semantics/spec.md).
- **Design:** `.project/active/explorer-rework-unblock/design.md` (to be created).

**Next Steps:** After approval, proceed to `/_my_design`.
