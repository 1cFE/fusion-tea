# Implementation Plan: CapEx & Sensitivity Views

**Status:** Complete
**Created:** 2026-04-06
**Last Updated:** 2026-04-06

## Source Documents
- **Spec:** `.project/active/views-capex-sensitivity/spec.md`
- **Design:** `.project/active/views-capex-sensitivity/design.md` — See here for component details, dependencies, architecture

## Implementation Strategy

**Phasing Rationale:**
Phase 1 de-risks the hardest Plotly layout (grouped horizontal bars) and wires the template. Phase 2 builds the second view on the same foundation. Phase 3 adds acceptance tests and catches integration issues.

**Overall Validation Approach:**
- Phases 1-2: manual browser validation after each (server must be running)
- Phase 3: Playwright acceptance tests extend existing `test_views_manual.py`
- All phases: no JS console errors, no regressions on existing views

---

## Phase 1: Template + CapEx View

### Goal
Wire `cas_breakdown.js` and `tornado.js` on the compare page for global constants, then implement `view_capex.js` with both Integrated and Landscape modes and CAS22 drill-down. This is first because the grouped horizontal bar layout is the riskiest Plotly configuration (untested in this codebase).

### Changes Required

**See `design.md` for:**
- Architecture overview → `design.md#architecture-overview`
- CapEx component details → `design.md#component-1-capex-view-view_capexjs`
- Script loading order → `design.md#component-3-script-loading`
- CSS classes → `design.md#css-additions-to-explorercss`

**Specific file changes:**

#### 1. Template — Script Tags
**File:** `exploration/concept_explorer/templates/compare.html.j2:87` (EDIT)
- [x] Add `<script src="/static/js/cas_breakdown.js"></script>` before `comparison.js`
- [x] Add `<script src="/static/js/tornado.js"></script>` before `comparison.js`
- [x] Add `<script src="/static/js/view_capex.js"></script>` after `view_summary.js`
- [x] Add `<script src="/static/js/view_sensitivity.js"></script>` after `view_capex.js` (placeholder — file created in Phase 2)

#### 2. CapEx View
**File:** `exploration/concept_explorer/static/js/view_capex.js` (NEW)
- [x] IIFE wrapper with local helpers (`el`, `append`, `FAMILY_COLORS`, `assignColors`, `rgba`, `purgeCharts`) — same pattern as `view_summary.js:14-77`
- [x] Module-scoped `showSubAccounts = false` flag
- [x] `computeSharedMaxAccount(concepts)` — max single-account cost across all concepts, 10% padding, see `design.md#landscape-mode--per-concept-bars`
- [x] `buildCategoryOrder(showSubAccounts)` — returns reversed y-axis category array (CAS10 at top), with CAS22 sub-accounts inserted when expanded
- [x] `renderIntegrated(container, concepts)`:
  - `purgeCharts(container)`, clear container
  - Filter to concepts with cost models; if none, show `.view-no-data` placeholder
  - Build one Plotly trace per concept (see `design.md` pseudocode): family-colored with opacity stepping, all CAS accounts as y categories
  - Hover text: account name, cost M$, % of total, "★ overridden" when applicable
  - Layout: `barmode: "group"`, `orientation: "h"`, `categoryorder: "array"`, chart height `Math.min(900, Math.max(400, numCategories * 28 + 120))`
  - Total cost summary line below chart using `.capex-totals` CSS
  - CAS22 toggle button using `.capex-toggle` CSS; click handler toggles `showSubAccounts` and re-calls `renderIntegrated`
- [x] `renderLandscape(container, concept, syncContext)`:
  - `purgeCharts(container)`, clear container
  - No cost model → `.view-no-data` placeholder
  - Compute shared max from `syncContext.allConcepts` via `computeSharedMaxAccount`
  - Single trace with `CAS_COLORS` per-account coloring (see `design.md#landscape--design-choice`)
  - Overridden accounts: star annotation via Plotly annotation (single-concept, not noisy)
  - `xaxis.range = [0, sharedMax]`
  - CAS22 toggle button (same shared `showSubAccounts` flag)
- [x] Register: `window.VIEW_REGISTRY.capex.renderIntegrated = renderIntegrated`
- [x] Register: `window.VIEW_REGISTRY.capex.renderLandscape = renderLandscape`

#### 3. CSS
**File:** `exploration/concept_explorer/static/css/explorer.css` (APPEND)
- [x] `.capex-totals`, `.capex-totals__item`, `.capex-totals__value` — total cost summary line
- [x] `.capex-toggle`, `.capex-toggle:hover` — CAS22 expand/collapse button

### Validation

**Manual (server running on 127.0.0.1:8765):**
- [x] Navigate to `/compare?concepts=05,04&left=capex` — grouped horizontal bars render, 2 concepts side-by-side per CAS account
- [x] Click "Expand CAS22 Detail" — chart re-renders with 14 sub-accounts replacing CAS22 aggregate
- [x] Click "Collapse CAS22 Detail" — returns to 17-account view
- [x] Total cost summary line shows correct values below chart
- [x] Hover on a bar → tooltip shows account name, cost, %, overridden flag
- [x] Switch to Landscape mode → per-concept bar charts with CAS-colored bars, synced x-axis
- [x] Navigate to `/compare?concepts=05,04&left=capex&right=summary` — CapEx left, Summary right, both render
- [x] Select CapEx in right panel dropdown → renders (mutual exclusion prevents both panels showing CapEx)
- [x] No JS console errors
- [x] Concept profile page (`/concept/05`) → CAS chart still works (regression)

**What We Know Works After This Phase:**
- Template wiring complete (all script tags in place)
- Grouped horizontal bar chart layout works in Plotly
- CAS22 toggle works in both modes
- Axis sync works for Landscape mode
- No-cost-model placeholder works

---

## Phase 2: Sensitivity View

### Goal
Implement `view_sensitivity.js` with both Integrated (union top-8, shared-first sort, divider) and Landscape (per-concept top-8, confidence encoding, synced axes) modes.

### Changes Required

**See `design.md` for:**
- Sensitivity component details → `design.md#component-2-sensitivity-view-view_sensitivityjs`
- Core data processing (`mergeAndRank`) → `design.md#core-data-processing`
- Union parameter construction (`buildUnionParams`) → `design.md#integrated-mode--grouped-tornado`
- Landscape confidence encoding → `design.md#landscape-mode--per-concept-tornado`

**Specific file changes:**

#### 1. Sensitivity View
**File:** `exploration/concept_explorer/static/js/view_sensitivity.js` (NEW)
- [x] IIFE wrapper with local helpers (same set as CapEx view)
- [x] `TOP_N = 8` constant
- [x] `mergeAndRank(sensitivities, topN)` — merge engineering + financial, sort by |elasticity|, take top-N (see `design.md#core-data-processing`)
- [x] `buildUnionParams(concepts)` — returns `{ params, sharedSet }` with shared-first sorting (see `design.md` for full algorithm)
- [x] `computeSharedElasticityRange(concepts)` — symmetric max |elasticity| with 10% padding (see `design.md#landscape-mode--per-concept-tornado`)
- [x] `displayName(paramName, ...metadataSources)` — resolve display name from parameter_metadata, fallback to raw param name
- [x] `renderIntegrated(container, concepts)`:
  - `purgeCharts(container)`, clear container
  - Filter to concepts with sensitivities; if none, show `.view-no-data` placeholder
  - Call `buildUnionParams` to get sorted union parameter set
  - Build one trace per concept: family-colored with opacity stepping, all union params as y categories, 0 for missing params
  - Hover text: param display name, elasticity, baseline value, concept name
  - No confidence encoding on bars (opacity channel used for concept differentiation) — confidence in hover only
  - Layout: `barmode: "group"`, `orientation: "h"`, zeroline at x=0, `categoryorder: "array"` (reversed union order)
  - Dotted line divider shape between shared and unique sections (see `design.md` shapes snippet)
  - Chart height: `Math.max(300, unionParams.length * 28 + 120)`
- [x] `renderLandscape(container, concept, syncContext)`:
  - `purgeCharts(container)`, clear container
  - No sensitivities → `.view-no-data` placeholder
  - Call `mergeAndRank` for this concept's top-8
  - Compute shared elasticity range from `syncContext.allConcepts`
  - Build traces with confidence encoding: category colors from `TORNADO_CATEGORY_COLORS` when metadata available, opacity per `TORNADO_CONFIDENCE_OPACITY`, hatch fill for low-confidence (adapted from `tornado.js:318-395`)
  - `xaxis.range = [-sharedMax, sharedMax]`
- [x] Register: `window.VIEW_REGISTRY.sensitivity.renderIntegrated = renderIntegrated`
- [x] Register: `window.VIEW_REGISTRY.sensitivity.renderLandscape = renderLandscape`

#### 2. CSS
**File:** `exploration/concept_explorer/static/css/explorer.css` (APPEND)
- [x] `.sensitivity-divider` — NOT NEEDED: divider implemented as Plotly shape, not DOM element

### Validation

**Manual (server running on 127.0.0.1:8765):**
- [x] Navigate to `/compare?concepts=05,04&left=sensitivity` — grouped tornado chart renders, parameters as y-axis, concepts side-by-side
- [x] Shared parameters appear at the top, dotted divider separates from unique parameters
- [x] Parameters unique to one concept show a single bar (not filtered out)
- [x] Hover shows param name, elasticity, baseline, concept
- [x] Switch to Landscape mode → per-concept top-8 tornado charts with synced x-axis
- [x] Landscape bars show confidence encoding (opacity + hatch for low-confidence)
- [x] Navigate to `/compare?concepts=05,04,08&left=sensitivity` — 3-concept integrated tornado, union of all top-8s
- [x] Switch to `/compare?concepts=05,04&left=capex&right=sensitivity` — both views render side-by-side
- [x] No JS console errors
- [x] Concept profile page (`/concept/05`) → tornado chart still works (regression)

**What We Know Works After This Phase:**
- Union top-8 parameter logic works correctly
- Shared-first sorting and divider render
- Confidence encoding works in Landscape mode
- Symmetric axis sync works
- All four views (Categorical, Summary, CapEx, Sensitivity) render in both modes

---

## Phase 3: Playwright Acceptance Tests + Polish

### Goal
Extend the existing `test_views_manual.py` with CapEx and Sensitivity test cases covering all acceptance criteria. Fix any visual or integration issues found during testing.

### Test Stencil (Write This First)
```python
def test_capex_integrated(page: Page):
    """CapEx integrated: grouped bars, 2 concepts, CAS accounts as categories."""
    page.goto(f"{BASE}/compare?concepts={MFE_1},{IFE}&left=capex")
    wait_for_compare(page)
    time.sleep(2)
    left = page.locator("#content-left")
    assert left.locator(".js-plotly-plot").count() >= 1
    assert left.locator(".capex-toggle").count() == 1
    assert left.locator(".capex-totals").count() == 1

def test_capex_cas22_toggle(page: Page):
    """CAS22 expand/collapse via toggle button."""
    page.goto(f"{BASE}/compare?concepts={MFE_1},{IFE}&left=capex")
    wait_for_compare(page)
    time.sleep(2)
    page.click(".capex-toggle")
    time.sleep(1)
    # Verify sub-account labels appear in chart
    # Click again to collapse
    page.click(".capex-toggle")
    time.sleep(1)

def test_capex_landscape(page: Page):
    """CapEx landscape: per-concept charts with synced axes."""
    page.goto(f"{BASE}/compare?concepts={MFE_1},{IFE},{MIF}&view=capex&mode=landscape")
    wait_for_compare(page)
    time.sleep(2)
    grid = page.locator("#landscape-grid")
    assert grid.locator(".js-plotly-plot").count() >= 3

def test_sensitivity_integrated(page: Page):
    """Sensitivity integrated: grouped tornado, shared params at top."""
    page.goto(f"{BASE}/compare?concepts={MFE_1},{IFE}&left=sensitivity")
    wait_for_compare(page)
    time.sleep(2)
    left = page.locator("#content-left")
    assert left.locator(".js-plotly-plot").count() >= 1

def test_sensitivity_landscape(page: Page):
    """Sensitivity landscape: per-concept tornado with confidence encoding."""
    page.goto(f"{BASE}/compare?concepts={MFE_1},{IFE},{MIF}&view=sensitivity&mode=landscape")
    wait_for_compare(page)
    time.sleep(2)
    grid = page.locator("#landscape-grid")
    assert grid.locator(".js-plotly-plot").count() >= 3

def test_all_four_views_switching(page: Page):
    """Cycle through all 4 views in both panels, no JS errors."""
    # Extended version of existing test_view_switching_no_errors
```

### Changes Required

#### 1. Acceptance Tests
**File:** `exploration/concept_explorer/tests/test_views_manual.py` (EDIT)
- [x] Add `test_capex_integrated` — grouped bars render, totals line, toggle button present
- [x] Add `test_capex_cas22_toggle` — expand shows sub-accounts, collapse returns to aggregate
- [x] Add `test_capex_landscape` — per-concept charts render, synced axes
- [x] Add `test_sensitivity_integrated` — grouped tornado renders, parameters visible
- [x] Add `test_sensitivity_landscape` — per-concept tornadoes render
- [x] Add `test_all_four_views_switching` — cycle all views in both panels + mode toggle, no JS errors
- [x] `test_view_switching_no_errors` already includes capex/sensitivity in rotation (existing test already covered this)
- [x] Add tests to `main()` test list
- [x] Update existing `test_full_flow_4_concepts` to also test landscape with capex/sensitivity views
- [x] Add `test_sensitivity_integrated_3_concepts` — 3-concept union top-8
- [x] Add `test_capex_sensitivity_side_by_side` — both new views simultaneously
- [x] Add `test_full_flow_3_concepts_integrated` — 3 concepts with capex+sensitivity in integrated mode

#### 2. Polish (as needed based on test results)
- [x] No visual issues found
- [x] Screenshots verified correct (`/tmp/view_test_*.png`)

### Validation

**Automated:**
- [x] `uv run python exploration/concept_explorer/tests/test_views_manual.py` → 23/23 pass (server running)
- [x] Existing tests still pass (regression) — all 14 original tests pass

**Manual:**
- [x] Review screenshots in `/tmp/view_test_*.png` for visual correctness
- [x] Full acceptance criteria walkthrough from spec (completed by user in Phases 1-2)

**What We Know Works After This Phase:**
- All acceptance criteria verified by automated tests
- No regressions on existing views or pages
- URL persistence works with capex/sensitivity views
- Rapid view switching produces no errors

---

## Environment Setup

**See CLAUDE.md for full environment rules**

Run server: `cd exploration && uv run python -m concept_explorer.server` (or however the dev server starts)
Run tests: `uv run python exploration/concept_explorer/tests/test_views_manual.py` (requires server running)

---

## Risk Management

**See `design.md#potential-risks` for detailed risk analysis**

**Phase-Specific Mitigations:**
- **Phase 1**: Plotly grouped horizontal bars are the unknown. If `barmode: "group"` with `orientation: "h"` doesn't work as expected, fall back to manual trace positioning with `offset` and `base` properties.
- **Phase 2**: Union parameter set could be large. If >20 params makes the chart unreadable, reduce TOP_N from 8 to 6.
- **Phase 3**: Playwright timing — existing tests use `time.sleep()` for async renders. New tests follow the same pattern with 2s waits for Plotly charts.

## Implementation Notes

*TO BE FILLED DURING IMPLEMENTATION*

### Phase 1 Completion
**Completed:** 2026-04-06
**Actual Changes:**
- Created `exploration/concept_explorer/static/js/view_capex.js` (310 lines) — full IIFE with renderIntegrated and renderLandscape
- Edited `exploration/concept_explorer/templates/compare.html.j2` — added 4 script tags (cas_breakdown.js, tornado.js, view_capex.js, view_sensitivity.js)
- Appended to `exploration/concept_explorer/static/css/explorer.css` — .capex-totals, .capex-toggle CSS classes
**Issues:** None
**Deviations:** None — followed design.md closely

### Phase 2 Completion
**Completed:** 2026-04-06
**Actual Changes:**
- Created `exploration/concept_explorer/static/js/view_sensitivity.js` (~340 lines) — full IIFE with renderIntegrated and renderLandscape
- No CSS changes needed — shared/unique divider uses Plotly shape (dotted line), confidence encoding uses Plotly marker patterns
**Issues:** None
**Deviations:**
- Skipped `.sensitivity-divider` CSS class — Plotly shape approach is cleaner, no DOM element needed
- Landscape hatch pattern uses per-bar `fgcolor` array matching category colors (adapted from tornado.js pattern)

### Phase 3 Completion
**Completed:** 2026-04-06
**Actual Changes:**
- Edited `exploration/concept_explorer/tests/test_views_manual.py` — added 9 new test functions (23 total, up from 14)
- New tests: `test_capex_integrated`, `test_capex_cas22_toggle`, `test_capex_landscape`, `test_sensitivity_integrated`, `test_sensitivity_integrated_3_concepts`, `test_sensitivity_landscape`, `test_capex_sensitivity_side_by_side`, `test_all_four_views_switching`, `test_full_flow_3_concepts_integrated`
- Rewrote `test_full_flow_4_concepts` to properly handle MAX_INTEGRATED=3 constraint (landscape only for 4 concepts)
- Updated docstring to reflect all 4 view types
**Issues:**
- Initial test failures due to: (1) mutual exclusion disabled options in dropdowns — fixed by respecting constraint in test pairs; (2) MAX_INTEGRATED=3 prevents integrated mode with 4 concepts — fixed by splitting into landscape-only (4 concepts) and integrated (3 concepts) tests
**Deviations:**
- Added 3 extra tests beyond plan: `test_sensitivity_integrated_3_concepts`, `test_capex_sensitivity_side_by_side`, `test_full_flow_3_concepts_integrated` for better coverage

---

**Status**: Complete
