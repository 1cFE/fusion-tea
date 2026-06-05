# Design: Explorer Rework Unblock

**Status:** Implemented
**Owner:** Reid W
**Created:** 2026-06-05
**Complexity:** LOW (revised from MEDIUM — see Appendix A)
**Branch:** `fix/explorer-rework-unblock`
**Branch:** TBD (single PR off `main`)

## Overview

Rename the `ForwardResult` symbol the explorer reads from `result` to `result_1gw` at the two read sites (extractor and server), drop a stale integer cast on `n_mod`, and add one warning when a concept lacks `analysis.md`. No new abstractions, no restructure, no new fields. ~10 lines of production code change plus test-fixture updates.

## Related Artifacts

- **Spec:** [`spec.md`](./spec.md) (revision 2 — FR-A4 removed after verification)
- **Research:** [`../../research/20260605-081423_explorer-rework-dependency-gap-map.md`](../../research/20260605-081423_explorer-rework-dependency-gap-map.md)
- **Epic:** [`../../backlog/epic_concept_analysis_rework.md`](../../backlog/epic_concept_analysis_rework.md), Item 10 Phases 3-5
- **Deferred follow-up:** [`../explorer-slider-override-semantics/spec.md`](../explorer-slider-override-semantics/spec.md) (slider/registry discontinuity)
- **Helper contract:** `exploration/concept_analysis/scripts/lib/model_setup_helpers.py:1-31`

## Research Findings

Verified at the keyboard (concept 01 imported live):

- `result_1gw.params` carries the *engineering* spec keys (`R0`, `B`, `availability`, `lifetime_yr`, `n_mod=4`, `net_electric_mw=1000.0`, ...) but **not** `override_reference_mw` and **not** `cost_overrides`. The library does not reflect those particular kwargs back into `params`.
- `n_mod` in `result_1gw.params` is an integer-valued Python `int` (helper line 169 rounds before forward()). The existing `int(float(...))` cast at `server.py:159` is a redundant safety net, not load-bearing.
- The extractor at `extract_explorer_data.py` already assigns `effective_result = result_1gw` at line 324 and uses only that downstream. Lines 308-315 already require `result_1gw` to be present and call `verify_two_knob`. Lines 301-306 are the dead-weight `result` guard.
- Server `_compute_cached` (`server.py:530-567`) is the only other read site. Lines 553-555 still demand `result`; line 557 reads `result.params`.
- Tests stub `result` in four places in `test_extraction.py` (lines 166, 266, 293, 318) and define an explicit assertion against the current error text in `test_missing_model_attribute_raises` (line 336-344). The compute-path fixture in `test_state_and_compute.py` (lines 33-130) defines `result` at the bottom of a fake `model_setup.py` source.

## Core Concept

Two pieces of code — `extract_costingfe` and `_compute_cached` — independently look up the same module-level symbol from a concept's `model_setup.py`. The symbol's name changed in the rework (`result` → `result_1gw`); both lookups need to match. There is no abstraction to share, no helper to extract, no kwargs-flow to redesign. The whole change is a coordinated rename plus a defensive warning for the case where a concept's `analysis.md` doesn't exist yet.

The reason this is right (and not just expedient): the previous design tried to anticipate Item-4-library plumbing (`override_reference_mw`) that the explorer doesn't actually receive from the library at compute time. Once that anticipation is dropped, the only real change is contract-name drift. A larger refactor here would solve a problem the spec doesn't have.

## Key Bets & Decisions

- **Bet 1:** `result_1gw` is the explorer's one authoritative `ForwardResult`. Both read sites use it; neither retains a fallback to `result`.
- **Bet 2:** The `_forward_with_overrides` structure stays as-is. The dual explicit-args + `**extra` shape works correctly for everything that's actually in `result_1gw.params` today. Restructuring to a single-kwargs-dict would solve a problem we no longer have (see Reflection in Appendix A).
- **Decision (n_mod precision):** Drop the explicit `int()` cast at `server.py:159`. Pass `float(params.get("n_mod", 1))`. Library accepts numeric `n_mod`; helper rounds upstream; the cast is stale and would silently quantize if a future caller passes a fractional value. Removing it is hygiene with zero behavioral change today.
- **Decision (empty-frontmatter warning):** Emit one `UserWarning` per concept in `run_extraction`'s dispatcher, named-field enumeration as the spec asks. Warning fires when `model_setup.py` exists but `analysis.md` does not. Existing default fall-throughs in `_to_confinement_family`, the `frontmatter.get("Concept", concept_dir.name)` pattern, etc. continue to provide the actual default values.
- **Decision (deliberately not done):** No `_FORWARD_NAMED` fallback edit. The hardcoded fallback set (lines 96-107) is for test environments without `costingfe` installed; nothing in this work item touches a knob that would invalidate it. The introspection path is primary and already correct.

## Architecture

Read-site diff only — no module boundaries change, no new files, no data-shape changes.

```
   extract_explorer_data.py                 server.py
   ─────────────────────────                ──────────
   extract_costingfe()                      _compute_cached()
     getattr(module, "model")                 getattr(module, "model")
   - getattr(module, "result")              - getattr(module, "result")
     getattr(module, "result_1gw")          + getattr(module, "result_1gw")
     effective_result = result_1gw            base_params = result_1gw.params
     (... rest unchanged ...)                 _forward_with_overrides(...)
                                                  ^
                                                  └─ drop int() cast on n_mod
```

And in `run_extraction`'s per-concept loop, before routing:

```
   if model_setup_path.exists() and not analysis_path.exists():
       warnings.warn(<concept_id + named fields>)
```

That's the entire architectural surface of this change.

## Required Invariants

1. **Single result symbol.** Both `extract_costingfe` and `_compute_cached` read `result_1gw` from the concept's `model_setup.py`. Neither retains any path that reads or requires `result`.
2. **`n_mod` not integer-cast at the server compute site.** Whatever `result_1gw.params["n_mod"]` carries is passed verbatim (as a float) to `model.forward()`.
3. **Output JSON shape unchanged.** No new fields on `ConceptData`, `CostModelData`, or any sub-model. Item B's scope; this design does not touch it.
4. **One warning per old-shape concept per extraction run.** Names the concept ID and the fields that fell back to defaults (name, Confinement-Family, Comparison-Status, P-Native at minimum). No per-field repetition; no silent fall-through.

## Component Overview

- **`exploration/concept_explorer/extract_explorer_data.py`**
  - `extract_costingfe` — delete the `result`-required guard at lines 301-306. The lines below (308+) that already enforce `result_1gw` become the sole gate. Touch ~5 lines.
  - `run_extraction` — add the empty-frontmatter warning emission in the per-concept dispatcher loop. Touch ~5 lines.
- **`exploration/concept_explorer/server.py`**
  - `_compute_cached` — replace the `result` lookup (lines 553-555) with `result_1gw`; replace `result.params` with `result_1gw.params` (line 557); update the error message text to point at the rework epic Item 10/11. Touch ~5 lines.
  - `_forward_with_overrides` — change line 159 from `n_mod=int(float(params.get("n_mod", 1)))` to `n_mod=float(params.get("n_mod", 1))`. One line.
- **Tests**
  - `tests/test_extraction.py` — four `SimpleNamespace(model=..., result=..., result_1gw=...)` fixtures (lines 166, 266, 293, 318) drop the `result` field. `test_missing_model_attribute_raises` (line 336-344) updates its error-text assertion. New test `test_warns_on_missing_analysis_md` covers FR-A4.
  - `tests/test_state_and_compute.py` — the fake `model_setup.py` source (line 125 area) replaces `result = model.forward(...)` with `result_1gw = model.forward(...)`. Existing compute tests (lines 297-313) re-run against the new fixture.

## Non-Goals

- New `ConceptData` fields (Item B).
- Ingesting `design-points/baseline.yaml`, `critic_review_*.md`, or `tables/*.csv` (Item B).
- UI / template / JS changes.
- Slider-semantics redesign — the override-registry discontinuity is the deferred follow-up's problem.
- Regeneration of the 12 old-shape concepts (rework epic Item 11).
- Any restructure of `_forward_with_overrides` beyond the single int-cast removal.

## Implementation Notes

### Empty-frontmatter warning

Emit at the per-concept loop in `run_extraction`, right after `parse_frontmatter` returns and before the routing decisions. Pseudocode (~7 lines):

```python
if not analysis_path.exists() and model_setup_path.exists():
    warnings.warn(
        f"{concept_id}: no analysis.md — fields defaulted: "
        f"Concept (dir name), Confinement-Family (NONSTANDARD), "
        f"Comparison-Status (''), P-Native (None). See rework epic Item 11.",
        UserWarning, stacklevel=2,
    )
```

One warning per concept per run. Existing default fall-throughs in `_to_confinement_family`, `frontmatter.get("Concept", concept_dir.name)`, and the empty `Comparison-Status` handling already supply the actual default values; the warning is purely advisory.

### Error-message update at `_compute_cached`

```python
result_1gw = getattr(module, "result_1gw", None)
if result_1gw is None:
    raise ImportError(
        f"{model_setup} does not define 'result_1gw' at module level. "
        "Rework epic Items 10/11."
    )
```

### `_forward_with_overrides` change

A one-line edit:

```python
n_mod=float(params.get("n_mod", 1)),   # was: int(float(...))
```

The library accepts numeric `n_mod`; helper already rounds to an integer-valued value upstream. This removal is hygienic.

### What's deliberately NOT changed

- `_FORWARD_SKIP` set (line 113). `cost_overrides` is never in `result_1gw.params`, so adding it to the skip set would filter nothing.
- `_FORWARD_NAMED` introspection or its fallback. Neither path is broken; both ignore the `override_reference_mw` case correctly because that key never appears in `result_1gw.params`.
- The `lru_cache` key shape. Compute identity is unchanged.

## Potential Risks

- **R1 — Test fixture coupling.** Four sites in `test_extraction.py` stub `result` and one test asserts on the existing error text. Test count is small; failures are loud; fixture edits are mechanical. Low risk.
- **R2 — `model_output.txt` content shift.** Helper-emitted `print_cas_breakdown` output now leads with the 1 GWe NOAK headline. The narrative-extraction prompt (line 791) embeds this text. The format change is upstream of this work item; verify the prompt still produces sensible `NarrativeData` on at least one concept. (If it doesn't, that's a narrative-pipeline issue, not this PR's problem.) Low risk.
- **R3 — Freeform concept regression.** Concept 03 and other freeform-routed concepts go through `extract_standalone`, not `extract_costingfe`. They have `result_1gw = None` at module level. `extract_standalone` doesn't read `result_1gw` at all. Verify by smoke test that concept 03's JSON is produced unchanged. Low risk.
- **R4 — Inactive code paths.** Once `result` is gone, any future code or test that reaches for it will fail cleanly with `AttributeError`. No silent fallback. This is intended.

## Integration Strategy

Single PR off `main`. No coordination with the analysis pipeline. Once merged:

- `uv run python exploration/concept_explorer/extract_explorer_data.py --skip-narrative` produces JSONs for all 40 concepts (28 clean, 12 with the empty-frontmatter warning).
- Server starts and `/api/compute` works for any costingfe concept.
- Frontend behaves identically — same `ConceptData` shape, same payload fields.
- Item B (`explorer-rework-enrich`) and the slider-discontinuity follow-up are unblocked.

The 12 old-shape concepts ship with warnings. Whoever runs extraction sees them and knows what to do (regenerate via Item 11 when prioritized).

## Validation Approach

### Automated

- `uv run python -m pytest exploration/concept_explorer/tests/ -v` — full suite passes after the fixture and assertion updates.
- New test `test_warns_on_missing_analysis_md` — creates a temp concept directory with `model_setup.py` but no `analysis.md`; asserts one `UserWarning` containing the concept ID and the named field list.
- Existing test `test_compute_costingfe_concept_returns_cost_model_data` (test_state_and_compute.py:297) verifies the compute path against the new fixture without modification.

### Manual

- `uv run python exploration/concept_explorer/extract_explorer_data.py --skip-narrative` end-to-end on the real repo. Expect 40 JSONs in `data/` and 12 warnings on stderr (one per old-shape concept).
- `uv run python exploration/concept_explorer/server.py` — `curl -sX POST localhost:8421/api/compute -H 'content-type: application/json' -d '{"concept_id":"01","overrides":{"availability":0.92}}'` returns 200 with a `CostModelData`.
- Spot-check the response: the no-op call `overrides:{}` will return LCOE ≈ 127.5 (library-bare, no analyst overrides). This is the slider discontinuity documented in the follow-up spec — expected here, addressed there.

### Success criteria (echoed from spec)

FR-A1 (extractor accepts concepts without `result`), FR-A2 (server reads `result_1gw.params`), FR-A3 (no `n_mod` int cast), FR-A4 (warning on empty frontmatter with field enumeration).

## Next-Stage Handoff

**Fixed for the plan:**
- `result_1gw` is the only result symbol read at either site.
- `_forward_with_overrides` keeps its current structure; only the `n_mod` cast changes.
- Empty-frontmatter warning lives in `run_extraction`'s dispatcher loop; format includes the named-field list.
- Test edits are enumerated above; no design judgment left for the implementer.

**Open for the plan:**
- Exact wording of the warning message and the updated `_compute_cached` error message — micro-copy, not architectural.
- Whether the new `test_warns_on_missing_analysis_md` lives in `test_extraction.py` alongside other dispatcher tests or in a new file. Recommend same file.

**De-risk first:**
- Run extraction on concept 01 alone (`--concept 01 --skip-narrative`) after removing the `result` guard. Two-line change verifiable in seconds.
- Then concept 04 (old shape) to confirm the warning fires and extraction proceeds.

---

## Appendix A — Reflection on the LOW complexity rating

The spec carries MEDIUM complexity. After verifying the false premise (FR-A4) and removing it, the actual change drops to:

- 2 line-edits in the extractor
- 2 line-edits in the server (one for `result_1gw`, one for `n_mod` cast)
- 1 warning emission (~7 lines)
- 4 test fixture stub updates, 1 assertion text update, 1 new test
- 1 fake-module source edit in the compute test fixture

No new helpers, no abstractions, no module reshape. This is LOW. The MEDIUM rating in the spec inherited from the pre-revision view; the design is honestly reporting what it found.

## Appendix B — File:line change inventory (as implemented)

| File | Lines | Change |
|---|---|---|
| `extract_explorer_data.py` | 301-306 | Deleted `result` guard; `model` check is now a one-liner. |
| `extract_explorer_data.py` | 137-144 | **Fixed `verify_two_knob`** to match the helper's integer-rounded `n_mod` (`max(1, round(1000/p_native))`) instead of the raw float division. Newly-reachable bug — the helper rounds at `model_setup_helpers.py:169`, but the verifier expected the unrounded value. Was unobserved because the `result` guard short-circuited before. |
| `extract_explorer_data.py` | 875-890 area | Empty-frontmatter `UserWarning` emitted in `run_extraction` dispatcher when `model_setup.py` exists but `analysis.md` does not. Enumerates the four fields that fell back. |
| `server.py` | 549-558 | `result` → `result_1gw`; `result.params` → `result_1gw.params`; updated error message. |
| `server.py` | 159 | `int(float(...))` → `float(...)`. |
| `tests/test_extraction.py` | 166, 266, 293, 318 | Dropped `result=...` from `SimpleNamespace` stubs. |
| `tests/test_extraction.py` | 336-344 | Updated assertion text. New `test_missing_result_1gw_raises`. |
| `tests/test_extraction.py` | new class | `TestEmptyFrontmatterWarning` (2 tests): warn-on-missing + no-spurious-warn. |
| `tests/test_state_and_compute.py` | 125 | `result = model.forward(...)` → `result_1gw = model.forward(...)` in fake `model_setup.py` source. |
| `tests/test_extract_adapter.py` | 172-175, 244, 263-267 | Updated `n_mod` fixture values from `1000/p_native` (unrounded) to `max(1, round(1000/p_native))` (helper-matching). |

## Appendix C — Unexpected findings (implementation notes)

- **`verify_two_knob` was wrong since Item 7**. The helper rounds `n_mod` to an integer (per its docstring: "1 GWe projection is a comparison convenience, not a real plant design point"), but the verifier still compared against `1000.0 / p_native_f` with tolerance `1e-9`. It would have rejected every real concept the first time it ran end-to-end. Unobserved because the `result` guard at the top of `extract_costingfe` short-circuited before reaching it. Fix is one line and matches the helper exactly. Tests at `test_extract_adapter.py` were similarly using the unrounded value as the "conforming" baseline; updated.
- **4 concepts fail extraction with concept-side errors** (04 stale `p_input` kwarg, 17b missing `result_1gw`, 27 & 39 routing disagreement, 38 `inf` LCOE). None are explorer bugs. Filed in BACKLOG.md under "Explorer-rework-unblock follow-ups (2026-06-05)".
- **Slider override-registry discontinuity is observable** the moment this PR ships. On concept 01: stored JSON headline = `155.17 $/MWh` (with analyst overrides); first `/api/compute` call with `overrides={}` returns `127.53 $/MWh` (library-bare, no overrides). Pre-existing behavior surfaced by the rework. Deferred follow-up: [`explorer-slider-override-semantics`](../explorer-slider-override-semantics/spec.md).

---

**Next Step:** After approval → `/_my_plan` (recommended for the multi-site coordination) or `/_my_implement` directly. Either is reasonable; this is small enough that a plan is more bookkeeping than load-bearing.
