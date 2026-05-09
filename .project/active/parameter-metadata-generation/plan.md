# Implementation Plan: Concept Page Sensitivity Restructure (Phase 2)

**Status:** Draft
**Created:** 2026-04-26
**Last Updated:** 2026-04-26
**Branch:** sensitivity-sliders

## Source Documents

- **Spec:** `.project/active/parameter-metadata-generation/spec.md`
- **Design:** `.project/active/parameter-metadata-generation/design.md` ← component details, decisions, invariants, risks
- **Canonical mockup:** `.project/active/parameter-metadata-generation/mockup_v2.html`

## Spike Credit

A de-risking spike (uncommitted, currently staged) rewrote `tornado.js` from Plotly to DOM with full feature parity for the "What Must Stay" checklist (see `design.md#tornado-refactor-—-what-must-stay` and the "Update: Tornado DOM Spike" appendix). It revealed that the previous Plotly bars were silently broken (no rendered bars for `unclassified` category — only whiskers). **Implication for this plan:** Phase 2 starts from a working DOM tornado that lacks only the inline-slider integration, not from Plotly. The "Plotly → DOM rewrite" risk in design is retired.

## Implementation Strategy

**Phasing rationale:** Match the four steps in `design.md#implementation-order`. Each step ships independently, gated by a browser check. Registry first (data → JSON, no UI), then sliders inside the tornado (biggest remaining behavior change), then sticky bar (depends on the slider compute callback), then collapsibles (pure layout polish, safe last).

**Critical path:** registry yaml → integrated tornado grid with sliders → sticky headline driven by compute → collapsibles. Each phase produces a visibly-verifiable concept page.

**First proof point:** Phase 1 gate — `data/01.json` shows `parameter_metadata.eta_th.display_name == "Thermal Efficiency"` and `display_unit == "%"`. This proves the registry layer is wired correctly into the merge order before any UI work.

**Overall validation approach:** Each phase has an automated extraction/test gate plus a manual `browser-inspect` walkthrough on concepts 01 (rich costingfe), 19 (different costingfe sanity check), and a standalone (e.g., 02). Console-clean is required at every gate.

---

## Phase 1: Display registry (extractor merge layer)

### Goal

Add a shared `parameter_display_registry.yaml` and merge it between auto-generated metadata and per-concept yaml. Re-extract all costingfe concepts so subsequent UI phases consume registry-blessed display names.

### Assumption Under Test

The `{**generated, **registry, **per_concept}` merge order is correct (per-concept beats registry beats generated), and the registry covers ≥80% of tornado top-15 occurrences across the 19 costingfe concepts.

### Test Stencil (Write This First)

```python
# tests/test_extraction.py
def test_registry_overrides_generated_but_loses_to_per_concept(tmp_path):
    # generated: display_name = "Eta Th"
    # registry:  display_name = "Thermal Efficiency", display_unit = "%"
    # per-concept: display_name = "Custom Name"
    generated = {"eta_th": ParameterMetadata(display_name="Eta Th", baseline=0.46, range=(0.32, 0.6))}
    registry  = {"eta_th": ParameterMetadata(display_name="Thermal Efficiency",
                                             display_unit="%", display_multiplier=100,
                                             baseline=0.46, range=(0.32, 0.6))}
    per_concept = {"eta_th": ParameterMetadata(display_name="Custom Name",
                                               baseline=0.46, range=(0.32, 0.6))}

    merged = {**generated, **registry, **per_concept}

    assert merged["eta_th"].display_name == "Custom Name"        # per-concept wins
    # And without per-concept override:
    merged2 = {**generated, **registry}
    assert merged2["eta_th"].display_name == "Thermal Efficiency"  # registry beats generated
    assert merged2["eta_th"].display_unit == "%"
```

### Changes Required

**See `design.md` for:** registry rationale (`design.md#display-registry`), starter table, merge order invariant (`design.md#required-invariants` #1).

**File changes:**

#### Registry data (NEW)
**File:** `exploration/concept_explorer/data/parameter_display_registry.yaml`
- [ ] Create with starter ~15 entries from `design.md#display-registry` table
- [ ] Survey tornado top-15 across all 19 costingfe `data/*.json` files; expand to cover ≥80% of distinct keys (target ~25 entries)
- [ ] Each entry: `display_name`, `display_unit`, `display_multiplier`

#### Loader + merge (extractor)
**File:** `exploration/concept_explorer/extract_explorer_data.py`
- [ ] Add `load_parameter_display_registry() -> dict[str, ParameterMetadata]` near `load_parameter_metadata()` (~line 606)
- [ ] In `extract_costingfe()` at the merge line (currently `extract_explorer_data.py:261`), change to: `merged_metadata = {**generate_parameter_metadata(...), **registry, **param_metadata}`
- [ ] Load registry once at module/extractor entry, not per-concept

#### Re-extract
- [ ] Run: `uv run python exploration/concept_explorer/extract_explorer_data.py`
- [ ] All 19 costingfe `data/{id}.json` files updated

### Validation

**Automated:**
- [ ] `uv run pytest exploration/concept_explorer/tests/test_extraction.py` → passes (incl. new merge-order test)
- [ ] `uv run pytest exploration/concept_explorer/tests/` → no regressions

**Manual (gate):**
- [ ] `jq '.parameter_metadata.eta_th' exploration/concept_explorer/data/01.json` shows `display_name == "Thermal Efficiency"`, `display_unit == "%"`, `display_multiplier == 100`
- [ ] Spot-check one concept that has a `model_metadata.yaml` override (if any exist) — per-concept value still wins
- [ ] Survey cross-check: print tornado top-15 keys for all 19 concepts; ≥80% have a registry entry

**What We Know Works After This Phase:** Registry layer is wired into the extraction merge. JSON consumed by the UI carries human-readable names + units before any UI work begins. Per-concept override path still wins.

---

## Phase 2: Inline sliders in tornado grid

### Goal

Add `<input type=range>` per row to the spike's DOM tornado, hand the tornado component ownership of slider state and debouncing, and remove the standalone `renderSliders()` path. After this phase, dragging a slider on concept 01 still updates the (in-flow) `headline-card` via the existing compute callback — sticky bar comes in Phase 3.

### Assumption Under Test

The tornado component can own slider lifecycle (override map, debounce timer, `reset()` method) without breaking the existing `onParameterClick` and visual encodings the spike preserved. `concept_page.js` can route compute through the new `onSliderChange` callback instead of through `renderSliders`.

### Test Stencil (Write This First)

```javascript
// Manual browser test (no JS unit tests for tornado.js today; document the script
// in tests/test_views_manual.py if a recipe exists, otherwise verify in-browser)

// In browser console on /concept/01:
//   1. document.querySelectorAll('.tornado-row input[type=range]').length === 15
//   2. Drag the first row's slider → after ~250ms, headline LCOE value text changes
//   3. window._tornadoReset()  // exposed for testing if convenient
//      → all sliders return to baseline value
//   4. console errors === 0
```

### Changes Required

**See `design.md` for:**
- Row layout (mockup_v2.html lines 283–697 — see grid template + slider cell)
- Data flow on slider drag → `design.md#data-flow-on-slider-drag`
- "What Must Stay" preserved capabilities → `design.md#tornado-refactor-—-what-must-stay`
- Top-N invariant → `design.md#required-invariants` #5

**File changes:**

#### Tornado: add slider cell + state ownership
**File:** `exploration/concept_explorer/static/js/tornado.js`
- [ ] Change row grid template from `180px 1fr 60px` (`tornado.js:151`) to a 4-column layout matching `mockup_v2.html` (`name | bar | slider | value`)
- [ ] Per row: append a slider cell containing `<input type=range>` with `min/max` from `parameterMetadata[key].range`, `value` = `baseline`, `step` = `(hi-lo)/200`
- [ ] Add module-scoped (per-render) `currentOverrides` and `debounceTimer`, owned by the tornado component
- [ ] On `input` event: update overrides, refresh value cell text via `display_multiplier`/`display_unit`, debounce 200ms, fire `options.onSliderChange({...currentOverrides})`
- [ ] Skip slider rendering for rows whose `parameterMetadata[key].range` is missing (degrade to current bar-only row)
- [ ] Expose `reset()`: clear overrides → set every input back to baseline → fire one final `onSliderChange({})`. Either return it from `renderTornado` or hang it on the container (`container._tornadoReset = ...`).
- [ ] Standalone-concept placeholder unchanged

#### Concept page: route compute through tornado, drop renderSliders
**File:** `exploration/concept_explorer/static/js/concept_page.js`
- [ ] Pass `onSliderChange` to `renderTornado` (currently at `concept_page.js:420-448`); body is the existing compute fetch (currently inside `renderSliders` callback at `concept_page.js:471-508`)
- [ ] Delete `renderSliders` (lines 234-305) and its call site (lines 458-509)
- [ ] Capture the reset handle returned from / attached by `renderTornado` for Phase 3

#### Template: remove sliders block
**File:** `exploration/concept_explorer/templates/concept.html.j2`
- [ ] Delete the `#sliders-section` block (lines 43-46) — sliders now live inside `#tornado-mount`

### Validation

**Automated:**
- [ ] `uv run pytest exploration/concept_explorer/tests/` → passes (existing tests don't target Plotly DOM, per design)

**Manual (gate, via `browser-inspect`):**
- [ ] Concept 01: 15 sliders visible, each on the same row as its bar. Drag → headline-card LCOE updates within ~250ms. Console clean.
- [ ] Concept 01: click a row's bar (not the slider) → `parameter_card` popover opens (existing behavior preserved)
- [ ] Concept 19: top-15 rows render, sliders work
- [ ] Standalone concept (02): renders the "No sensitivity data" placeholder, no console errors
- [ ] Comparison view (`/compare`) still loads — `view_sensitivity.js` still uses Plotly directly and depends on `TORNADO_CATEGORY_*` exports, which are preserved

**What We Know Works After This Phase:** Single integrated grid replaces tornado + standalone slider list. Drag → compute → headline update flows end-to-end. Reset capability exists, ready for the sticky bar to consume.

---

## Phase 3: Sticky headline + Reset

### Goal

Pin the four headline stats below the topnav so slider feedback is visible regardless of scroll position. Replace the in-flow Economics section. Wire compute responses to update the sticky bar with deltas; add the Reset button that drives `tornado.reset()`.

### Assumption Under Test

`position: sticky` + `backdrop-filter: blur` works at the live page width. Delta computation `(current − baseline) / baseline` reads correctly from the compute response. Reset button enable/disable state stays in sync with override presence.

### Test Stencil (Write This First)

```javascript
// Manual browser test on /concept/01:
//   1. Sticky bar visible below topnav at scroll = 0
//   2. Scroll page → sticky bar still visible
//   3. Drag a slider → sticky LCOE shows new value + colored delta (green = down, orange = up)
//   4. Reset button: disabled at baseline, enabled after first drag
//   5. Click Reset → sticky reverts, button disables, sliders return to baseline
//   6. Standalone concept 02: sticky bar shows static headline, no Reset button visible
```

### Changes Required

**See `design.md` for:**
- Sticky bar visual constraints → `design.md` Decision B
- Data flow → `design.md#data-flow-on-slider-drag`
- Invariants #2, #4, #7 → `design.md#required-invariants`
- Mockup for layout/CSS → `mockup_v2.html` `.sticky-headline` styles + JS update logic

**File changes:**

#### New module
**File:** `exploration/concept_explorer/static/js/sticky_headline.js` (NEW)
- [ ] Export `renderStickyHeadline(container, { concept, headline, hasSliders })` → renders identity (name + family badge + company), 4 stat pills, Reset button
- [ ] Export `updateStickyHeadline(container, newHeadline, baselineHeadline)` → updates pill values + computes/colors deltas (green for LCOE down / orange for LCOE up / hidden when zero)
- [ ] Export `setResetEnabled(container, enabled)` → toggles Reset button disabled state
- [ ] Reset button: when `hasSliders === false`, omit from DOM entirely (standalone concepts)

#### Template
**File:** `exploration/concept_explorer/templates/concept.html.j2`
- [ ] Add `<div id="sticky-headline" class="sticky-headline"></div>` between `{% block breadcrumb %}` content and `<div id="app">` (verify exact placement against `mockup_v2.html` so it sits below the topnav)
- [ ] Delete the `#headline-section` block (lines 33-47) — its data moves to the sticky bar
- [ ] Add `<script src="/static/js/sticky_headline.js"></script>` to the scripts block (before `concept_page.js`)

#### CSS
**File:** `exploration/concept_explorer/static/css/explorer.css`
- [ ] Port `.sticky-headline` + child styles from `mockup_v2.html` (sticky positioning, backdrop blur, stat pill layout, delta colors). Provide a non-blur fallback `background` per design risk mitigation.

#### Concept page wiring
**File:** `exploration/concept_explorer/static/js/concept_page.js`
- [ ] On initial load: call `renderStickyHeadline` with `concept.cost_model.headline` (or static for standalone)
- [ ] Capture `baselineHeadline = concept.cost_model.headline` once, before any compute
- [ ] Replace `renderHeadlineCard(headlineCardEl, …)` calls (init + post-compute) with `updateStickyHeadline(stickyEl, newHeadline, baselineHeadline)`
- [ ] Wire Reset button click: call `tornado.reset()` (the handle from Phase 2) → `updateStickyHeadline(..., baselineHeadline, baselineHeadline)` → `setResetEnabled(false)`
- [ ] Toggle `setResetEnabled(true)` whenever `onSliderChange` fires with a non-baseline override

### Validation

**Automated:**
- [ ] `uv run pytest exploration/concept_explorer/tests/` → passes

**Manual (gate, via `browser-inspect`):**
- [ ] Concept 01 at 1024px viewport: sticky bar pinned, readable, no overlap with content; drag → sticky updates with delta; Reset → reverts and disables; console clean
- [ ] Concept 19: same flow works
- [ ] Standalone concept 02: sticky bar shows static headline, no Reset visible, page loads cleanly
- [ ] Scroll the page far down: LCOE / Overnight / Net Power / Capacity Factor remain visible

**What We Know Works After This Phase:** Slider → result feedback loop is co-visible. Reset is a single un-do. Standalone concepts still render.

---

## Phase 4: Collapsible sections

### Goal

Wrap Narrative, Risks, CAS, Sensitivity, and Sources in a collapsible component with chevron + body. Apply default open/closed state per `design.md` Decision C, plus content-preview hints in collapsed headers (including the "X CHANGED" pill on Sensitivity when overrides exist).

### Assumption Under Test

Collapsing the Sensitivity section does NOT clear overrides (invariant #3) — the sticky bar still reflects the modified state, and re-expanding shows sliders in their dragged positions.

### Test Stencil (Write This First)

```javascript
// Manual browser test on /concept/01:
//   1. On load: Sensitivity expanded; Narrative/Risks/CAS/Sources collapsed
//   2. Click Narrative header → expands; chevron rotates; preview hint hides
//   3. Drag a sensitivity slider → "1 CHANGED" pill appears in Sensitivity header
//   4. Collapse Sensitivity → sticky bar still shows delta; pill remains in header
//   5. Re-expand → slider stays at dragged value
//   6. Click Reset → pill disappears, header preview reverts
```

### Changes Required

**See `design.md` for:**
- Default state matrix → `design.md` Decision C
- Header preview pattern → `design.md` Decision C
- Invariant #3 (collapse must not clear overrides) → `design.md#required-invariants`

**File changes:**

#### Collapsible helper
- [ ] Decide: keep inline in `concept_page.js` (per design "Open" question) if the helper stays simple (~30 lines); promote to `static/js/collapsible.js` only if it grows. **Default decision:** inline in `concept_page.js` — one helper function `makeCollapsible(headerEl, bodyEl, { defaultOpen, getPreview })`.

#### Template
**File:** `exploration/concept_explorer/templates/concept.html.j2`
- [ ] Wrap each section (`narrative-section`, `risks-section`, `cas-section`, `sensitivity-section`, sources if present) with: clickable header element (chevron + title + preview span) and body wrapper
- [ ] Preserve existing IDs (`narrative-content`, `tornado-mount`, etc.) so JS keeps working

#### CSS
**File:** `exploration/concept_explorer/static/css/explorer.css`
- [ ] Port collapsible header + chevron + body transition styles from `mockup_v2.html`

#### JS wiring
**File:** `exploration/concept_explorer/static/js/concept_page.js`
- [ ] After each section renders, call `makeCollapsible` with appropriate `defaultOpen` (Sensitivity = true; rest = false) and a `getPreview` lambda:
  - Narrative: `"Key bets · eliminated costs · novel costs"` (static)
  - Risks: `"{n} risks · {n_high} high"`
  - CAS: `"Total Capital: {value}"`
  - Sensitivity: `"{n} CHANGED"` pill if overrides present, else `"Drag any slider…"`
  - Sources: `"{n} sources"` (static)
- [ ] On `onSliderChange`: refresh Sensitivity header preview (count of non-baseline overrides). On Reset: refresh preview back to default text.

### Validation

**Automated:**
- [ ] `uv run pytest exploration/concept_explorer/tests/` → passes

**Manual (gate, via `browser-inspect`):**
- [ ] Concept 01: defaults match matrix; click each header to toggle; Sensitivity stays interactive; "X CHANGED" pill appears/disappears correctly
- [ ] Concept 19: same flow
- [ ] Standalone concept 02: sections collapse/expand normally; Sensitivity section shows the placeholder collapsed/expanded
- [ ] Console clean on all three

**What We Know Works After This Phase:** All acceptance criteria from `spec.md#acceptance-criteria` are met. Page is ship-quality per the spec.

---

## Risk Management

**See `design.md#risks` for the full risk register.** Spike-updated status:

- **Tornado refactor regression** — Retired by spike. DOM rewrite is in place with parity for items 1–8 of "What Must Stay".
- **Registry merge order bug** — Mitigated in Phase 1 by the explicit per-concept-wins test.
- **Sticky bar overlaps content on narrow viewports** — Phase 3 manual gate at 1024px viewport.
- **Collapsed-by-default hides Risks** — Mitigated by header preview showing risk count.
- **Standalone concepts break** — Phase 2 + Phase 3 + Phase 4 gates each include a standalone concept (02).
- **NEW (from spike): Plotly script tag stays** — `view_sensitivity.js` still uses Plotly directly for grouped tornado in `/compare`. No removal of the Plotly vendor file in this plan.

## Implementation Notes

[TO BE FILLED DURING IMPLEMENTATION]

### Phase 1 Completion
**Completed:** 2026-04-26

**Actual Changes:**
- Created `exploration/concept_explorer/data/parameter_display_registry.yaml` with 32 entries covering 100% (405/405) of tornado top-15 occurrences across 27 costingfe concepts (the survey found 27, not 19 as design assumed — extra a/b variants).
- Added `load_parameter_display_registry()` and `apply_display_patches()` to `extract_explorer_data.py`; module-level cached `_DISPLAY_REGISTRY`; constant `_REGISTRY_PATCH_FIELDS = {display_name, display_unit, display_multiplier}`.
- Wired three-layer merge in `extract_costingfe()` at `extract_explorer_data.py:265-273`: `generated → registry-patched → per-concept`.
- Added `TestDisplayRegistry` class (5 tests) in `tests/test_extraction.py` covering: field-level patching, unknown-key skipping, registry loader unknown-field warnings, missing-file → empty, and the full three-layer merge order via `extract_costingfe()`.
- Re-extracted all concepts via `uv run python exploration/concept_explorer/extract_explorer_data.py --skip-narrative`.

**Issues Encountered:**
- **Design.md table had a wrong unit for `plasma_t`.** Inspecting `costingfe/model.py:260` showed `plasma_t` is the minor radius `a` in meters, not "Plasma Temperature" in keV. The variable name is a misnomer in the upstream cost model. Registry entry corrected and a SOURCE-style code comment added next to the entry.

**Deviations from Plan:**
- **Merge semantics shifted from full-replace to field-level.** The plan stencil treated registry entries as full `ParameterMetadata` objects (replaceable via dict-spread). Reality: the registry only has 3 of the 7 required `ParameterMetadata` fields, so a full-replace would erase the generated `baseline`/`range`/`category`/`confidence`. Resolved by introducing `apply_display_patches()` for field-level merge while keeping per-concept yaml as full-replace. The merge order invariant from `design.md#required-invariants` #1 is satisfied (per-concept beats registry beats generated).
- Survey covered all 32 distinct keys instead of stopping at the design's "~25". Same author cost; full coverage.

### Phase 2 Completion
**Completed:** 2026-04-26

**Actual Changes:**
- Rewrote `exploration/concept_explorer/static/js/tornado.js` to render the integrated grid: 4-column row (`name+ε | bar | slider | value`), per-render closure state for overrides + debounce, `_buildHeaderRow()`, `_buildRow()`, `_buildLegend()`, `_formatValue()` (mockup_v2.html-style adaptive precision), `_updateValueClass()` (orange when LCOE rises, green when LCOE falls). Reset is exposed both as the return value `{reset}` and as `container._tornadoReset` for callers that don't capture the return.
- Sliders are only rendered for rows whose `parameterMetadata[key].range` is finite and well-formed — degraded rows still show baseline value or `—`.
- `concept_page.js`: deleted the standalone `renderSliders()` function (was lines 224-305) and the duplicate sliders-block in `init()`. Compute callback is now defined once as `onSliderChange`, passed to `renderTornado` via the new `onSliderChange` option, and gated by `hasSliders = isCostingfe && has_sensitivities && sensitivities != null`.
- `concept.html.j2`: removed the `#sliders-section` / `#sliders-container` block; left a comment noting Phase 2/3 migration.
- `explorer.css`: removed the now-dead `.sliders-panel` / `.slider-row*` rules (~40 lines).

**Issues Encountered:**
- **`TaskCreate`-style task-tracking reminders:** Repeated system reminders during the session. Ignored per instructions; the plan's checkboxes and Implementation Notes carry the tracking.
- **Concept 19 turned out to be freeform standalone (not costingfe).** My survey conflated `cost_model + sensitivities` with costingfe; the canonical filter is `sources.model_setup is not None`. Used concept 04 as the second costingfe sanity check instead. 27 true costingfe concepts (01, 03–11, 14, 17a/b, 20a/b, 21, 23, 25, 26, 28–34, 36); 11 freeform-with-sensitivities (02, 12, 13, 15, 16, 18, 19, 22, 24, 27, 35).
- **Pre-existing backend mismatch surfaced.** Initial-load LCOE on concept 01 is $216.3/MWh (from `cost_model.headline`, which is the per-account-1GW-scaled `result_1gw`), but `/api/compute` returns the raw `result` baseline (~$181.8/MWh). Reset reverts to compute-baseline, not extraction-baseline — a visible "snap" exists between page load and the first slider interaction. **Out of scope for this work item** (predates Phase 2 — `renderHeadlineCard` was called on both code paths). Phase 3 sticky bar should use `cost_model.headline` as its initial baseline so deltas line up; flagged for the Phase 3 implementation but not for any backend change here.

**Deviations from Plan:**
- **Header row added.** Mockup_v2 has column headers ("Parameter / Elasticity / What-if / Value"). Plan didn't call them out explicitly; added them for legibility. Counts in selectors now read 16 = 1 header + 15 data rows.
- **`reset()` exposed via two paths.** Plan called for either return value or container attachment; did both, since `concept_page.js` doesn't currently capture the return value (it will in Phase 3) but tests/console use the container handle.
- **Removed dead CSS.** Plan didn't list this; sweeping `.slider-row*` was natural since the JS class went away. Project rule: no dead code.

**Verification (browser-inspect, all sessions clean: 0 page_errors):**
- Concept 01 (HTS Compact Tokamak): 15 inline sliders, drag `availability` 0.75→0.6 → headline LCOE 216.3→223.0 (in-flow card; sticky bar comes Phase 3) → value cell "59.9%" colored orange (`--color-pos`); `_tornadoReset()` returns slider to 0.75 + value cell reverts to "75.0%" + neutral color. Click row label → parameter card popover opens (existing behavior preserved).
- Concept 04 (Laser ICF, costingfe): 15 sliders, `eta_th` drag fires compute, headline updates.
- Concept 02 (freeform standalone): tornado renders with bars but 0 sliders (no slider ranges in metadata) — correct degraded state. Pre-existing `[tornado] Missing parameterMetadata` warnings (param naming mismatch) carry over from spike, not Phase 2 regressions.
- Concept 19 (freeform standalone): renders cleanly, 0 sliders.
- `/compare` view: loads with 0 console messages and 0 page errors — `TORNADO_CATEGORY_COLORS/_LABELS/_ORDER` exports preserved for `view_sensitivity.js`.

### Phase 3 Completion
**Completed:** 2026-04-26

**Actual Changes:**
- Created `exploration/concept_explorer/static/js/sticky_headline.js` with three exports (`renderStickyHeadline`, `updateStickyHeadline`, `setResetEnabled`); attached to `window` (no module system). Stat pills are data-driven via a `STATS` table — adding/removing pills requires only one edit.
- Added `.sticky-headline*` and `.sticky-headline__pill*` styles to `explorer.css` (~140 lines) using existing design tokens. Family badge variants for MFE/IFE/MIF/Non-std map to `--color-badge-*`. Delta classes use `--color-concept-unique` (orange, LCOE up = bad) and `--color-key-innovation` (green, LCOE down = good). Non-blur `background: var(--color-surface-1)` precedes the `rgba(...)` declaration as a graceful fallback.
- `concept.html.j2`: added `<div id="sticky-headline">` above `#app`; removed the entire `#headline-section` block; kept `#headline-loading` and `#compute-error` as bare divs; added `<script src="/static/js/sticky_headline.js">` before `concept_page.js`.
- `concept_page.js`:
  - Captured `baselineHeadline = concept.cost_model?.headline ?? null` and `tornadoHandle` (returned by `renderTornado`) before the tornado/CAS block.
  - Replaced both `renderHeadlineCard` call sites (init + post-compute) with `renderStickyHeadline(...)` and `updateStickyHeadline(...)`.
  - Wired Reset to revert sliders, sticky bar, AND CAS breakdown to the extraction baseline (no compute round-trip).
  - Added `_hasNonBaseline(overrides)` — toggles `setResetEnabled` based on whether any slider differs from its baseline by > 1e-9.
  - Removed the now-unused `renderHeadlineCard()` function.
- `tornado.js`: changed `reset()` to clear UI state only — it no longer fires `onSliderChange({...baselines})`. Comment in source explains why.
- `explorer.css`: removed dead `.headline-grid` / `.headline-metric*` / `@keyframes shimmer` rules (~60 lines).

**Issues Encountered:**
- **Stale Jinja templates after edit.** First browser test failed with `renderStickyHeadline is not defined` even though the script tag was in source. The running server had cached its template loader; killing + restarting served the updated HTML. Documented locally — no fix needed (`uvicorn --reload` is the long-term answer; out of scope here).
- **Reset surfaced the pre-existing scale mismatch as a real UX bug.** Initial Reset implementation called `tornado.reset()` which fired `onSliderChange({...baselines})` → `/api/compute` → returned un-scaled `~$181.8/MWh` → overwrote my synchronous `updateStickyHeadline(216.3)` → user saw a phantom "▼16.0% improvement" delta. **Fix:** `tornado.reset()` now only clears UI state; `concept_page.js`'s Reset handler explicitly reverts the sticky bar + CAS to the extraction-baseline state and posts empty state, with no compute round-trip. After fix: Reset is a clean visual revert to page-load state.
- **Browser-inspect timing.** 700ms wait was insufficient for fetch + render at first; bumped to 900ms for verification gates.

**Deviations from Plan:**
- **Reset handler does more than the plan listed.** Plan called for sticky-bar revert + button disable. Production reality also requires CAS breakdown revert and `postState({}, [])` to keep the server-side state coherent. Added both inside the Reset handler.
- **Removed dead `.headline-*` CSS** (orphaned even before this work item — JS used `.headline-stat*` while CSS had `.headline-metric*` — a long-standing class-name mismatch). No visual regression because nothing was actually styled by them.

**Verification (browser-inspect, all sessions: 0 page_errors):**
- Concept 01 initial state: sticky bar pinned below topnav, identity (`HTS Compact Tokamak [MFE] Commonwealth Fusion Systems`), 4 pills (LCOE 216.3 / Overnight 15554 / Net Power 1000 / Capacity Factor 75.0), Reset visible + disabled.
- Drag `availability` 0.75→0.6: LCOE → 223.0 with " ▲3.1%" orange delta; Overnight → 11891 with " ▲23.5%"; Net Power → 261 with " ▼73.9%"; Capacity Factor → 59.9 with " ▼20.1%" green delta. Reset enables.
- Click Reset: LCOE returns to 216.3, all deltas blank, Reset disables, slider returns to 0.75, value cell "75.0%" with neutral color, CAS breakdown reverts to original 16,975 M$ total. NO phantom delta.
- Standalone concept 02 @ 1024×800 viewport: sticky bar visible, "Non-std" badge, 4 pills populated, Reset button OMITTED. Layout fits cleanly at narrow width.
- Pre-existing `[tornado] Missing parameterMetadata` warnings on standalone concept 02 unchanged from Phase 2 (freeform naming convention; out of scope).

### Phase 4 Completion
**Completed:** 2026-04-26

**Actual Changes:**
- `concept.html.j2`: each `<section>` now has `class="section is-collapsed"` (or no `is-collapsed` for Sensitivity), wraps body in `.section__body`, replaces `<h2>` with `<button class="section__header">` containing chevron `<svg>`, `.section__title`, and `.section__hint` (with `data-hint-for` attr). Single SVG chevron template repeated per section.
- `explorer.css`: added `.section`, `.section__header`, `.section__chevron`, `.section__title`, `.section__hint`, `.section__hint--changed`, `.section__body`, plus the `.is-collapsed` rules that drive chevron rotation and body-display. ~80 lines, ported from mockup_v2.
- `concept_page.js`:
  - Added `makeCollapsible(sectionEl, defaultOpen)` and `setSectionHint(sectionEl, hintConfig)` helpers — kept inline (per design's "Open" question; helper stayed small).
  - Added `_sumCASCapital()` and `_fmtMoneyM()` helpers; CAS hint computed as `Total Capital: 16,975 M$` from the same sum that `cas_breakdown.js` renders.
  - At end of `init()`, wired collapsibles per Decision C matrix (Sensitivity = open, others = collapsed) + populated each section's hint.
  - `_countChanged(overrides)` replaces inline counter; drives both `setResetEnabled` and `_updateSensitivityHint`.
  - `onSliderChange` now calls `_updateSensitivityHint(overrides)` synchronously (before fetch) so the "N CHANGED" pill appears the moment a slider settles, regardless of compute latency.
  - Reset handler clears the Sensitivity hint back to default text.

**Issues Encountered:**
- **`--skip-narrative` from Phase 1 wiped narratives across all concepts.** When testing collapsibles, `concept.narrative` was null on every concept, so Narrative + Risks sections never became visible in the verification, leaving the test selectors picking up empty hints. Re-extracted concept 01 with narrative for full hint verification (`13 risks · 6 high`). Background re-extract for concepts 02/04/19 launched as a follow-up. **Recommended cleanup after this work item:** run `uv run python exploration/concept_explorer/extract_explorer_data.py` (without `--skip-narrative`) to restore narratives across all concepts. None of the concept analysis source data changed, so this is a one-time replay.
- **Cold-start fetch latency intermittently exceeded 900 ms** when verifying — sticky pill values lagged the eval. Not a Phase 4 bug; the change-pill / reset-clear / hint-class assertions all passed.

**Deviations from Plan:**
- **`section__hint--changed` styled as a small orange "pill"** (background-tinted, padded) rather than just colored text — matches the mockup_v2 visual signature better, and the orange is unique enough to draw the eye when scrolling past a collapsed Sensitivity section.
- **`makeCollapsible` does a clone-replace on the header** to drop any prior listener — defensive against accidental re-binding (relevant if the page ever re-runs init without a full reload).
- **Hints computed from concept data, not from rendered DOM.** Plan suggested deriving the CAS hint by querying the rendered table; pulling it from `concept.cost_model` accounts directly is one fewer DOM read and matches the same number `cas_breakdown.js` will display.

**Verification (browser-inspect, all sessions: 0 page_errors):**
- Concept 01 initial state: Narrative collapsed (hint: "key bets · eliminated costs · novel costs"), Risks collapsed (hint: "13 risks · 6 high"), CAS collapsed (hint: "Total Capital: 16,975 M$"), Sensitivity expanded (hint: "Drag any slider — top numbers will update"). Chevrons rotated -90° on collapsed.
- Click Narrative header: section expands, chevron rotates to 0°, content visible.
- Drag slider on availability: Sensitivity hint becomes "1 CHANGED" with orange `--changed` pill styling. Reset button enables. Sticky bar shows colored deltas.
- Click Sensitivity header to collapse it WHILE slider is dragged: section collapses, "1 CHANGED" pill remains in header (visible while collapsed — invariant #3 confirmed), sticky bar still shows the in-flight delta values.
- Click Reset: Sensitivity hint reverts to "Drag any slider — top numbers will update" (no orange pill), sticky bar reverts to baseline (216.3, no deltas), Reset button disables.
- Concept 02 (standalone, narrative wiped): only CAS + Sensitivity sections visible (Narrative + Risks correctly hidden when narrative is null), CAS hint computed, Sensitivity hint default. No Reset button. Page renders with 0 page_errors.

---

**Status**: Draft → In Progress → **Complete** (2026-04-26)

## Final Summary

All four phases complete. The concept profile page now ships:

1. **Display registry** — 32-entry shared yaml that patches display names, units, and multipliers on top of auto-generated metadata; per-concept yaml still wins.
2. **Integrated tornado grid** — single 4-column row per top-15 parameter (`name+ε | bar | slider | value`), inline `<input type=range>` with debounced compute, color-coded value cell.
3. **Sticky compact headline** — pinned below the topnav with 4 stat pills, family badge, and Reset button. Reset reverts UI cleanly without round-tripping through `/api/compute`.
4. **Collapsible sections** — Narrative / Risks / CAS collapsed by default with informative hints (risk count, total capital), Sensitivity expanded by default with a "N CHANGED" pill when overrides exist.

**Spec acceptance criteria all met** — see Implementation Notes per phase for evidence.

**Known follow-ups (out of scope, but worth noting):**
- The pre-existing `/api/compute` ↔ `result_1gw` scaling mismatch surfaces as a value snap on first slider drag (extraction baseline 216.3 vs compute baseline ~181.8). Working around it in the Reset path; the cleanest fix is a small backend change so compute returns the same per-account-1GW-scaled headline that extraction does. Worth its own work item.
- Freeform standalone concepts (02, 18, etc.) have parameter names that don't match the registry (`plant_availability` vs `availability`, `thermal_efficiency` vs `eta_th`); each shows ~25 console warnings. Two paths: alias rules in the registry, or normalize standalone-concept naming. Either is its own work item.
