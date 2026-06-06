# Implementation Plan: Explorer Slider Override Semantics

**Status:** Complete (Phases 1–3 implemented and validated)
**Created:** 2026-06-06
**Last Updated:** 2026-06-06

## Source Documents
- **Spec:** `.project/active/explorer-slider-override-semantics/spec.md`
- **Design:** `.project/active/explorer-slider-override-semantics/design.md` ← component details, bets, invariants, gotchas

**Locked decisions** (confirmed before planning):
- **Decision A:** toggling resets sliders to baseline (mode switch); preserving drag positions is deferred.
- **Bet 3:** repurpose `CostModelData.sensitivities` to hold *applied*; add `sensitivities_bare`. `/api/parameter_index` becomes applied-based (documented in the README addition).

## Implementation Strategy

**Phasing Rationale:** Backend correctness first (the one load-bearing claim), then the data layer that feeds the UI, then the UI. Each phase is independently testable; Phases 1 and 2 are technically independent but Phase 1 carries the project's only real correctness risk, so it goes first.

**Critical Path:** Phase 1 (compute re-applies registry, reproduces `result_1gw`) → Phase 2 (payload carries both sensitivities + count) → Phase 3 (toggle reads both, rebinds atomically).

**First Proof Point:** Phase 1 FR-SO1 regression — `compute(concept="01", overrides={}, apply=True).headline.lcoe_per_mwh` ≈ stored `cost_model.headline.lcoe_per_mwh`, asserted against the live module.

**Overall Validation Approach:** test-first each phase; full `pytest` suite as a no-regression gate; Phase 3 manual validation via the `browser-inspect` skill. Env per CLAUDE.md (`uv run …`).

---

## Phase 1: Compute-Path Correctness (registry re-application + flag)

### Goal
Make `/api/compute` re-apply the analyst registry under `apply_analyst_overrides=True` so a no-op compute reproduces the stored headline, and thread the flag end-to-end. Backend only — no UI.

### Assumption Under Test
The recompute can mirror `run_native_and_1gw` exactly from `result_1gw.params` + the module's `overrides`/`P_native` (INV-1), and the LRU key stays correct under the new flag (INV-4).

### Test Stencil (Write This First)
```python
# tests/test_slider_override_semantics.py (NEW)
def test_fr_so1_noop_compute_matches_headline(client):
    concept = load_concept("01")
    stored = concept.cost_model.headline.lcoe_per_mwh           # applied (~155.17)
    applied = compute(concept_id="01", overrides={}, apply_analyst_overrides=True)
    bare    = compute(concept_id="01", overrides={}, apply_analyst_overrides=False)
    assert applied.headline.lcoe_per_mwh == pytest.approx(stored, rel=1e-6)
    assert bare.headline.lcoe_per_mwh < stored                   # registry dropped (~127.53)
```

### Changes Required
**See design.md for:** compute flow → `design.md#architecture`; re-application gotchas → `design.md#implementation-notes`; INV-1/4 → `design.md#required-invariants`.

- [x] `tests/` — add `test_slider_override_semantics.py` with the FR-SO1 stencil + a cache-key test (same overrides, differing flag → distinct results).
- [x] `models.py` — `ComputeRequest` and `ExplorerState` gain `apply_analyst_overrides: bool = True`.
- [x] `server.py:143` — `_forward_with_overrides` gains `cost_overrides=None`, `override_reference_mw=None` kwargs; pass them to `model.forward(...)`. Confirm neither leaks into `**extra`.
- [x] `server.py:561` — `_compute_cached` gains the flag; when on, read `module.overrides` → `enabled_overrides(...)` and `module.P_native`; extend LRU key to `(concept_id, frozenset(overrides), apply_analyst_overrides)`.
- [x] `server.py:603` — `compute` passes `body.apply_analyst_overrides` through.

### Validation
**Automated:**
- [x] `uv run python -m pytest tests/test_slider_override_semantics.py` → FR-SO1 + cache-key pass. (5/5 pass)
- [x] `uv run python -m pytest` (full suite) → no regressions. (227 passed; the 6 `test_extract_adapter` failures are pre-existing — identical on a clean `git stash` of these changes.)

**Manual:**
- [x] Through the real FastAPI stack (TestClient on the real concept 01 module): `apply=True` → 155.17 (+0.000% vs stored headline); `apply=False` → 127.53 (−17.82%). Matches the spec's figures exactly.

**What We Know Works After This Phase:** the slider's recompute can describe the analyst-applied LCOE with the registry scaled correctly; the discontinuity is gone at the data layer; cache is correct under the flag.

---

## Phase 2: Dual Sensitivities + Override Count (data layer)

### Goal
Emit `sensitivities` (applied), `sensitivities_bare`, and `analyst_override_count` per costingfe concept so the frontend can swap the tornado client-side and label the toggle.

### Assumption Under Test
`model.sensitivity(cost_overrides=enabled)` differs from the bare call for ≥1 parameter (INV-3), and an empty registry yields `sensitivities == sensitivities_bare` (INV-6).

### Test Stencil (Write This First)
```python
def test_fr_so4_both_sensitivities_present_and_differ():
    cd = extract_costingfe(concept_dir_01)
    cm = cd.cost_model
    assert cm.sensitivities is not None and cm.sensitivities_bare is not None
    keys = set(cm.sensitivities.engineering) | set(cm.sensitivities.financial)
    assert any(cm.sensitivities.engineering.get(k) != cm.sensitivities_bare.engineering.get(k)
               for k in keys)                                    # applied ≠ bare somewhere
    assert cd.analyst_override_count == len(enabled_overrides(module_01.overrides))
```

### Changes Required
**See design.md for:** schema delta → `design.md#component-overview`; INV-3/6 → `design.md#required-invariants`; Bet 3/4 → `design.md#key-bets--decisions`.

- [x] `models.py` — `CostModelData` gains `sensitivities_bare: SensitivityAnalysis | None = None`; `ConceptData` gains `analyst_override_count: int = 0`.
- [x] `extract_explorer_data.py:178` — `build_sensitivity_analysis(model, result, cost_overrides=None)`.
- [x] `extract_explorer_data.py:288` — in `extract_costingfe`: compute `enabled`, then `sensitivities`=applied, `sensitivities_bare`=bare; set `analyst_override_count=len(enabled)`; wire both into `CostModelData`/`ConceptData`.
- [x] Re-extract: `uv run python exploration/concept_explorer/extract_explorer_data.py --skip-narrative` → `data/*.json` regenerate; server loads cleanly.

### Validation
**Automated:**
- [x] `uv run python -m pytest tests/test_slider_override_semantics.py::test_fr_so4_*` → pass (live concept 01 + mock wiring).
- [x] `uv run python -m pytest` → no regressions. 229 passed; the same 6 pre-existing `test_extract_adapter` failures remain. (Fixed a real test-fixture bug along the way — `_Model.sensitivity` in `test_extract_adapter.py` had to accept `cost_overrides` now that the production signature carries it.)

**Manual:**
- [x] Inspect regenerated data: `01` → `analyst_override_count=1`, `24` → 7, `17a` → 8; `sensitivities_bare` present on all; concept 01 applied vs bare elasticities differ across many engineering keys.
- [x] `create_app` (TestClient over the real data dir) boots clean; `/api/health`, `/api/manifest`, `/api/parameter_index` (120 params, now applied-based), `/api/concepts/01` all 200.

**What We Know Works After This Phase:** the payload exposes both LCOE functions' sensitivities and the registry size; the tornado and label have their data.

---

## Phase 3: Hero Toggle + Atomic Rebind (UI)

### Goal
Add the hero-block toggle and wire it so headline + CAS + tornado swap in lockstep on toggle, with client-side sensitivity selection and INV-5 hide/disable.

### Assumption Under Test
Toggling (sliders untouched) swaps all three surfaces with no partial-update frame (FR-SO5/INV-2), and the toggle is correctly hidden/disabled for freeform/empty-registry concepts (FR-SO6/INV-5).

### Test Stencil (Write This First)
```
# Manual, via browser-inspect skill (no JS unit harness in this app):
# 1. open /concept/01 → toggle present, label "Apply analyst cost adjustments (N entries)", checked
# 2. uncheck → headline drops to bare AND tornado bars change AND CAS updates — together, one frame
# 3. open a freeform concept → no toggle rendered; console clean (read JSON sidecar)
```

### Changes Required
**See design.md for:** rebind sequencing → `design.md#architecture` + `design.md#implementation-notes` (atomicity); placement/label → `spec.md#ux-requirements-for-the-design-phase`; INV-5 → `design.md#required-invariants`.

- [x] `templates/concept.html.j2` — hero-block toggle markup (checkbox + label + inert `(N entries)` count + subtitle), default checked. *(Built in JS via `mountOverrideToggle` into the JS-rendered `#hero`, consistent with how the whole hero is built — see deviation note.)*
- [x] `static/js/concept_page.js:434` — include `apply_analyst_overrides` in the `/api/compute` body; toggle `onChange` → `onModeSwitch` re-issues compute with `overrides={}` and, in the response handler, updates sticky headline + `renderCASBreakdown` + re-`renderTornado` (selected sensitivity set) together; sliders reset to baseline (Decision A).
- [x] `static/js/concept_page.js:462` — `_selectedSensitivities()` selects `sensitivities` (applied) vs `sensitivities_bare` by toggle state when (re)rendering the tornado.
- [x] `static/js/concept_page.js` — `mountOverrideToggle` only called when `sources.model_setup != null` (freeform → no toggle); disabled (with hover text) when `analyst_override_count == 0` (INV-5).
- [x] `static/css/explorer.css` — toggle + low-emphasis count-chip styling (label, not button).
- [x] `README` (explorer) — added "Analyst-override semantics" subsection: toggle selects the LCOE function + parameter-index is applied-based (FR-SO3).

### Validation
**Automated:**
- [x] `uv run python -m pytest` → no regressions (229 passed; same 6 pre-existing `test_extract_adapter` failures).

**Manual (browser-inspect skill, ephemeral playwright over the live server):**
- [x] FR-SO5: `/concept/01` toggle off → headline 155.2→127.5, tornado top-row elasticity −0.909→−0.890, CAS total 14,574→11,623 M$ — all together; delta empty (no phantom delta, INV-2); console 0 / page_errors 0. Concept 24 likewise (8.5→21.0, tornado re-ordered), console clean.
- [x] FR-SO2: `availability` 0.70→0.95 sweep — applied `[184.6→140.9]`, bare `[151.0→116.2]`, both monotone-decreasing, slope sign matches the negative availability elasticity in each mode.
- [x] FR-SO6: freeform concept 03 → 0 toggles rendered (hero still renders); empty-registry costingfe concept 05 → toggle present but `--disabled`, checkbox disabled, "(0 entries)", hover text shown.
- [x] Smoke: concepts 01 / 24 / 05 render fully, 15 sliders present, no lag, no new console errors. (The only console output anywhere is pre-existing `[tornado] Missing parameterMetadata` warnings on standalone concept 03.)

**What We Know Works After This Phase:** the headline ↔ slider ↔ tornado triple is coherent and toggle-selected; the toggle teaches the registry's aggregate weight; the "(N entries)" count is visible and inert (Item 2 makes it clickable).

---

## Environment Setup

**See CLAUDE.md** — all Python via `uv run …`; explorer served by `uv run python exploration/concept_explorer/server.py`; UI checks via the `browser-inspect` skill (read the JSON sidecar for console errors).

## Risk Management

**See `design.md#potential-risks`.**

**Phase-Specific Mitigations:**
- **Phase 1:** assert FR-SO1 against the *live module*, never a hardcoded 155.17 — guards param drift.
- **Phase 2:** full suite gate catches the `_warn_on_uncovered_sensitivity_keys` validator firing on applied keys; check it doesn't error.
- **Phase 3:** do the three DOM updates inside the single resolved compute handler — never update the tornado optimistically.

## Implementation Notes

[TO BE FILLED DURING IMPLEMENTATION]

### Phase 1 Completion
**Completed:** 2026-06-06

**Actual Changes:**
- `exploration/concept_explorer/server.py`:
  - Added `_derive_enabled_overrides()` + module-level `_enabled_overrides` — imports the canonical `lib.model_setup_helpers.enabled_overrides` (adding `concept_analysis/scripts` to `sys.path` the same way the concept modules do), with an inline last-wins/enabled-only fallback for costingfe-free environments. Mirrors the existing `_derive_forward_named()` fallback pattern.
  - `_forward_with_overrides` gained keyword-only `cost_overrides=None`, `override_reference_mw=None`, passed straight to `model.forward(...)`. Both are forward()'s own named args (so excluded from `extra` via `_FORWARD_NAMED`) and absent from `result_1gw.params`, so no double-pass. Rewrote the stale docstring that claimed overrides are never re-applied.
  - `_compute_cached` gained a required `apply_analyst_overrides: bool` param (extends the LRU key → INV-4). When True, reads `getattr(module, "overrides", []) ` → `_enabled_overrides(...)` and `getattr(module, "P_native", None)`; when False, both None. Empty/absent registry → `{}` → reproduces bare (INV-6).
  - `compute` passes `body.apply_analyst_overrides` as the third cache arg.
- `exploration/concept_explorer/models.py`: `ComputeRequest` and `ExplorerState` each gained `apply_analyst_overrides: bool = True` (optional + default, so existing callers/tests unaffected).
- `exploration/concept_explorer/tests/test_slider_override_semantics.py` (NEW, 5 tests):
  - `test_fr_so1_noop_compute_matches_stored_headline` — **live** regression against the real concept 01 module (asserts ≈ stored, not a literal; bare lower by >5%). `importorskip("costingfe")`.
  - `test_fr_so1_default_flag_matches_explicit_true` — omitted flag defaults to True.
  - `test_fr_so1_fake_module_applied_reproduces_result_1gw`, `test_cache_key_includes_flag_no_collision`, `test_inv6_empty_registry_applied_equals_bare` — self-contained fake module (no costingfe) covering FR-SO1, the cache-key/flag separation (INV-4), and empty-registry equivalence (INV-6).

**Issues:** None functional. A `git stash`/`uv run` interaction regenerated `uv.lock` and briefly stashed the edits; recovered by discarding the working-tree `uv.lock` and popping. No code lost.

**Deviations:**
- Plan's stencil sketched `compute(concept="01", ...)` and `load_concept("01")` as illustrative helpers; the actual app has no such helpers, so the FR-SO1 proof is realized via a `TestClient` over a minimal real-concept-01 base dir (true end-to-end through `/api/compute`). Same assertion, real plumbing.
- Added the `_enabled_overrides` import-with-fallback indirection (not spelled out in the plan) so server.py stays importable in costingfe-free test envs — consistent with the existing `_derive_forward_named` precedent. Not a data fallback.
- `_compute_cached`'s flag is **required** (no default) rather than defaulted, so every call site supplies it explicitly and no two cache entries can represent the same logical key. `compute` is the only caller.

### Phase 2 Completion
**Completed:** 2026-06-06

**Actual Changes:**
- `models.py`: `CostModelData` gained `sensitivities_bare: SensitivityAnalysis | None = None` (after `sensitivities`, with a Bet-3 doc comment); `from_forward_result` gained a parallel `sensitivities_bare` param (default None — server's `_compute_cached` call is unaffected). `ConceptData` gained `analyst_override_count: int = 0` (Bet 4 doc comment).
- `extract_explorer_data.py`: added the same robust `_derive_enabled_overrides()`/`_enabled_overrides` accessor as `server.py` (helper-preferred, inline fallback — keeps the extractor importable without costingfe for the mock tests). `build_sensitivity_analysis` gained `cost_overrides=None`, passed to `model.sensitivity(...)` (INV-3 doc comment). `extract_costingfe` now computes `enabled = _enabled_overrides(module.overrides)`, builds `sensitivities` (applied, the new stored default) and `sensitivities_bare` (bare) via two honest calls, passes both to `from_forward_result`, and sets `analyst_override_count=len(enabled)` on `ConceptData`.
- Re-extracted all concepts (`--skip-narrative`). Regenerated `data/*.json` now carry `sensitivities_bare` and `analyst_override_count`. Spot-check: 01→1, 24→7, 17a→8 enabled overrides.
- `tests/test_slider_override_semantics.py`: added `test_fr_so4_real_concept_01_both_sensitivities_and_count` (live: both present, differ for ≥1 param per INV-3, count == `enabled_overrides(module.overrides)`) and `test_fr_so4_mock_wiring_both_present_and_count` (no-costingfe wiring via a `side_effect` mock + registry).
- `tests/test_extract_adapter.py`: fixed the fake `_Model.sensitivity` to accept `cost_overrides=None` — its absence was a latent fixture bug exposed by the now-always-passed kwarg (the real costingfe signature has carried `cost_overrides` since before this work).

**Issues:**
- Re-extraction left 2 concepts un-refreshed — **17b** (`result_1gw` missing at module level) and **39** (stale `freeform-deferred` routing vs a costingfe-shaped `model_setup.py`). Both fail on strict-consumer checks that run *before* any Phase 2 code; 39's JSON never existed, 17b kept its prior JSON. Pre-existing concept-content debt, out of scope for this item — flagged for the user.
- **`data/24.json` was found stale during Item-1 checkbox verification** — stored headline 8.51 vs the module's deterministic `result_1gw` of 16.05. Re-extracted concept 24 in isolation to fix it (now 16.05; FR-SO1 holds for 01/17a/24). An audit confirmed all other *served* costingfe concepts already matched their modules (26/34 mismatch but are omit-listed; 17b errors). Root cause unconfirmed — possibly jax state leakage across the ~30 sequential module loads in the full extract-all. Logged as epic **Item 1-FU2** (audit + isolate extraction). No impact on shipped behavior: the server loads modules on demand and reproduces the correct `result_1gw`.

**Deviations:**
- `from_forward_result` takes `sensitivities_bare` as an explicit parallel param (mirrors the existing `sensitivities` param) rather than post-construction mutation — keeps construction in one place.
- Plan's FR-SO4 stencil (`extract_costingfe(concept_dir_01)`, bare positional) is realized with the real signature (frontmatter parsed from the live `analysis.md`); plus a mock variant so the wiring is covered without costingfe.

### Phase 3 Completion
**Completed:** 2026-06-06

**Actual Changes:**
- `static/js/concept_page.js`:
  - Captured `heroEl`; made the delta baseline mutable — `modeBaselineHeadline` / `modeBaselineCostModel` (updated on mode switch) replace the former `const baselineHeadline`, so slider deltas and Reset measure against the *current* mode's baseline and a toggle leaves no phantom delta (INV-2). Added `applyOverrides` state (default true).
  - `onSliderChange` now sends `apply_analyst_overrides` and deltas against `modeBaselineHeadline`.
  - `_selectedSensitivities()` picks applied vs bare; `renderTornadoForMode()` factors the tornado render so init and toggle share it (re-call rebuilds with sliders at baseline — Decision A). `onParameterClick` card now reflects the selected set.
  - `onModeSwitch()` — single compute (`overrides={}`) + atomic headline/CAS/tornado update in one handler (INV-2); resets Reset/hint state.
  - `mountOverrideToggle(heroEl, …)` — new function rendering the hero-block control; called only for `model_setup != null`, disabled when count 0 (INV-5).
- `static/css/explorer.css`: `.override-toggle` block (surface card, green accent checkbox, mono low-emphasis count chip styled as label-not-button, subtitle, dimmed `--disabled` state).
- `README.md`: new "Analyst-override semantics" subsection under Compute Endpoint (FR-SO3) — flag behavior, LRU key, dual sensitivities, applied-based parameter-index, Decision A.
- No `concept.html.j2` change needed — `#hero` already exists and is fully JS-rendered.

**Issues:**
- The **collapsed CAS section *header hint*** ("Total Capital: N M$") is computed once from the applied model and not refreshed on toggle — but it is *also* not refreshed on slider drag (pre-existing). The CAS *breakdown content* (`#cas-mount`) does swap correctly (verified 14,574→11,623 on 01). Left consistent with slider-drag behavior rather than special-casing the toggle; minor, flagged for the user.

**Deviations:**
- Toggle markup is built in JS (`mountOverrideToggle`), not static template markup — `renderHero` wipes `#hero`, so static markup would be erased; JS is the established hero-rendering pattern.
- Validation used `uv run --with playwright …` (ephemeral) rather than `uv add playwright`, so `pyproject.toml`/`uv.lock` stay clean on this branch. Chromium was already cached; no download.

---

**Status**: Draft → In Progress → **Complete** (all three phases implemented, tested, and browser-validated 2026-06-06)
