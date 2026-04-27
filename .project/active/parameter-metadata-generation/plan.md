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
**Completed:**
**Actual Changes:**
**Issues:**
**Deviations:**

### Phase 2 Completion
**Completed:**
**Actual Changes:**
**Issues:**
**Deviations:**

### Phase 3 Completion
**Completed:**
**Actual Changes:**
**Issues:**
**Deviations:**

### Phase 4 Completion
**Completed:**
**Actual Changes:**
**Issues:**
**Deviations:**

---

**Status**: Draft → In Progress → Complete
