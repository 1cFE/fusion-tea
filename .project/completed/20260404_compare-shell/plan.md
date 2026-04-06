# Implementation Plan: Comparison Page Shell

**Status:** Complete
**Created:** 2026-04-05
**Last Updated:** 2026-04-05

## Source Documents
- **Spec:** `.project/active/compare-shell/spec.md`
- **Design:** `.project/active/compare-shell/design.md` — See here for component details, dependencies, architecture

## Implementation Strategy

**Phasing Rationale:**
URL state manager first (everything depends on it) → interactive controls second (mutate state) → layouts last (visual payoff). Each phase produces verifiable output in the browser.

**Overall Validation Approach:**
- No automated test infrastructure for frontend — validation is manual browser testing
- Each phase has a specific set of URLs to test and behaviors to verify
- Server runs via `uv run python -m exploration.concept_explorer.server` (or however it's started)

---

## Phase 1: Template + CSS + URL State Manager

### Goal
Lay the structural foundation: new template with all DOM containers, all new CSS classes, and the URL state core (`parseUrl`, `syncUrl`, `validateAndCorrect`). After this phase the page loads, parses URLs, shows loading/empty states, and corrects invalid URLs.

### Changes Required

**See `design.md` for:**
- Template structure → `design.md#template-structure`
- CSS additions → `design.md#css-additions-to-explorer-css`
- URL state manager → `design.md#component-1-url-state-manager`
- Page lifecycle → `design.md#component-7-page-lifecycle`

**Specific file changes:**

#### 1. Template
**File:** `exploration/concept_explorer/templates/compare.html.j2` (REWRITE)
- [x] Replace entire template with design.md template structure
- [x] Extends `base.html.j2`, uses `{% block body %}` and `{% block scripts %}`
- [x] All DOM containers: `#loading-state`, `#error-state`, `#warning-banner`, `#compare-content`, `#concept-bar`, `#concept-picker`, `#empty-state`, `#mode-toggle`, `#compare-integrated`, `#compare-landscape`
- [x] Only loads `comparison.js` (not tornado.js or cas_breakdown.js)

#### 2. CSS
**File:** `exploration/concept_explorer/static/css/explorer.css` (APPEND)
- [x] Append all new classes from design.md CSS section
- [x] Classes: `.mode-toggle`, `.compare-integrated`, `.compare-panel`, `.compare-panel__header`, `.compare-panel__content`, `.compare-view-select`, `.compare-landscape__header`, `.compare-landscape-grid` (`--1up`, `--2up`, `--3up`), `.compare-landscape-cell`, `.compare-landscape-cell__header`, `.compare-landscape-cell__content`, `.warning-banner`, `.compare-empty`, `.compare-placeholder`
- [x] Do not modify existing classes

#### 3. JavaScript — skeleton
**File:** `exploration/concept_explorer/static/js/comparison.js` (REWRITE)
- [x] Module constants: `MAX_INTEGRATED = 3`, `MAX_LANDSCAPE = 6`, `VALID_VIEWS`, `DEFAULT_LEFT`, `DEFAULT_RIGHT`, `DEFAULT_VIEW`
- [x] `FAMILY_META` and `CONFIDENCE_BADGE` — carry over from current file (:45-60)
- [x] `VIEW_REGISTRY` — define with all four views, null render functions
- [x] State: `let _state`, `let manifest`, `let conceptCache`
- [x] `fetchManifest()` — carry over from current file (:110-114)
- [x] `fetchConcept(conceptId)` — carry over from current file (:120-127)
- [x] `postState()` — carry over from current file (:97-108)
- [x] `parseUrl()` — new, per design.md Component 1
- [x] `syncUrl()` — new, per design.md Component 1
- [x] `validateAndCorrect(state, manifest)` — new, per design.md Component 1
- [x] `init()` — steps 1-7 from design.md lifecycle: loading state → fetchManifest → parseUrl → validateAndCorrect → fetchConcept (Promise.all) → syncUrl → postState. For now, steps 8-9 just show `#compare-content` and hide loading (no rendering yet)
- [x] Show `#empty-state` when 0 concepts, show `#warning-banner` when warnings exist
- [x] `popstate` listener — parseUrl → validateAndCorrect → syncUrl (no re-render yet)
- [x] DOMContentLoaded → init()

### Validation

**Manual:**
- [x] Navigate to `/compare` → loading spinner, then empty state with guidance text
- [x] Navigate to `/compare?concepts=arc,sparc` → loading, then content area visible (no layout yet, but no JS errors)
- [x] Navigate to `/compare?mode=integrated&concepts=arc,sparc,iter,demo,cfr` → URL auto-corrects to `mode=landscape` (check URL bar)
- [x] Navigate to `/compare?concepts=arc,INVALID_ID,sparc` → warning banner shown, URL updated to only valid concepts
- [x] Navigate to `/compare?concepts=INVALID` → empty state (0 valid concepts)
- [x] Navigate to `/compare?concepts=arc,sparc&left=capex&right=sensitivity` → URL preserved (view params kept)
- [x] Open browser console → no JS errors on any of the above
- [x] Visit `/taxonomy`, `/`, concept profile pages → all still work (no regressions)

**What We Know Works After This Phase:**
URL parsing, validation, correction, and sync. Template renders. CSS is in place. Data fetching works. Foundation is solid for Phase 2.

---

## Phase 2: Concept Bar, Picker & Mode Toggle

### Goal
Add all interactive controls: concept chips with remove, the `+` add button, inline picker dropdown, and the two-button mode toggle. After this phase the user can add/remove concepts and switch modes on the compare page — layouts still don't render, but state is fully interactive.

### Changes Required

**See `design.md` for:**
- Concept bar & picker ��� `design.md#component-2-concept-bar--picker-fr-2022`
- Mode toggle → `design.md#component-3-mode-toggle-fr-46`
- Mode re-evaluation logic → `design.md#component-2` (end of section)

**Specific file changes:**

#### 1. Concept Bar
**File:** `comparison.js` (ADD to existing skeleton)
- [x] `renderConceptBar()` — renders `.comparison-chip` per concept with family badge + name + `×` remove button. Reuses existing CSS classes. Adds `+` button (`.comparison-add-btn`) when count < MAX_LANDSCAPE. Hides `+` button at MAX_LANDSCAPE.
- [x] Remove handler: removes concept from `_state.concepts` → re-evaluates mode → `syncUrl()` → `postState()` → re-render
- [x] Wire `+` button to toggle picker

#### 2. Concept Picker
**File:** `comparison.js` (ADD)
- [x] `openPicker()` / `closePicker()` �� show/hide `#concept-picker`
- [x] `renderPickerList()` — filters manifest to exclude selected concepts. Each row: name, family badge, company info. Click calls `addConcept()`. Shows "Maximum concepts selected" when count >= MAX_LANDSCAPE. Shows "N of 6 selected" count.
- [x] `addConcept(conceptId)` — fetchConcept, push to `_state.concepts`, re-evaluate mode (auto-switch to landscape if > MAX_INTEGRATED and currently integrated), syncUrl, postState, closePicker, re-render
- [x] Click-outside listener to close picker (exclude `#concept-bar` and `#concept-picker` regions)
- [x] Wire `#close-picker` button

#### 3. Mode Toggle
**File:** `comparison.js` (ADD)
- [x] `renderModeToggle()` — shows `#mode-toggle` when concepts.length > 0. Sets active button to `.btn--primary`, other to `.btn--ghost`. Disables Integrated when count > MAX_INTEGRATED. Disables both when 0 concepts. Updates label text with count: "Integrated (N)" / "Landscape (N)".
- [x] Click handler: update `_state.mode` → `syncUrl()` → re-render

#### 4. Wire into lifecycle
**File:** `comparison.js` (MODIFY init and re-render)
- [x] `init()` step 8: call `renderConceptBar()`, `renderModeToggle()`
- [x] `renderAll()` — orchestrates concept bar + mode toggle + layout (layout still placeholder in this phase)
- [x] `popstate` listener: now calls `renderAll()` after state update

### Validation

**Manual:**
- [x] `/compare?concepts=arc,sparc` → concept bar shows 2 chips with badges + names + `×` buttons
- [x] Click `×` on a chip → chip removed, URL updates, mode toggle updates
- [x] Click `+ Add concept` → picker opens with available concepts (excluding selected)
- [x] Click a concept in picker → added to bar, picker closes, URL updates
- [x] Click outside picker → picker closes
- [x] Add 4th concept → mode toggle: Integrated disabled, Landscape active
- [x] Remove concepts down to 2 → Integrated re-enabled (stays in current mode)
- [x] Add concepts to 6 → `+` button hidden
- [x] Remove one → `+` button reappears
- [x] Mode toggle: click Landscape with 2 concepts → URL updates to `mode=landscape`
- [x] Mode toggle: click Integrated with 2 concepts → URL updates to `mode=integrated`
- [x] Open console → no JS errors during any interaction

**What We Know Works After This Phase:**
Full interactive concept management and mode switching. URL always reflects current state. postState keeps server in sync. Ready for layouts.

---

## Phase 3: Integrated & Landscape Layouts + View Registry

### Goal
Render both layout modes with view selector dropdowns dispatching to placeholder content. This completes the shell — after this phase the page is fully functional with placeholder views, ready for Items 3a/3b to plug in real renderers.

### Changes Required

**See `design.md` for:**
- Integrated layout → `design.md#component-4-integrated-layout-fr-710`
- Landscape layout → `design.md#component-5-landscape-layout-fr-1113`
- View rendering contract → `design.md#component-6-view-rendering-contract`
- Mutual exclusion → `design.md#component-4` (view selector dropdowns section)

**Specific file changes:**

#### 1. View Selector Utility
**File:** `comparison.js` (ADD)
- [x] `populateViewSelect(selectEl, selectedValue, disabledValue)` — fills `<select>` with options from `VIEW_REGISTRY`. Sets `selected` on current value. Sets `disabled` on `disabledValue` (for mutual exclusion). Used by both integrated panels and landscape.

#### 2. Integrated Layout
**File:** `comparison.js` (ADD)
- [x] `renderIntegrated()` — shows `#compare-integrated`, hides `#compare-landscape`. Populates `#select-left` and `#select-right` via `populateViewSelect()` with mutual exclusion (left's value disabled in right, right's value disabled in left). Dispatches rendering to `renderViewContent()` for each panel.
- [x] Wire `#select-left` change handler: update `_state.left` → syncUrl → update mutual exclusion on `#select-right` → re-render left panel content only
- [x] Wire `#select-right` change handler: same pattern for right
- [x] Default values: left=`_state.left` (categorical), right=`_state.right` (summary)

#### 3. Landscape Layout
**File:** `comparison.js` (ADD)
- [x] `renderLandscape()` — shows `#compare-landscape`, hides `#compare-integrated`. Populates `#select-landscape`. Builds grid in `#landscape-grid`: one `.compare-landscape-cell` per concept (header with name+badge, content area). Applies grid class: `--1up` for 1, `--2up` for 2-3, `--3up` for 4-6. Dispatches `renderViewContent()` for each cell.
- [x] Wire `#select-landscape` change handler: update `_state.view` → syncUrl → re-render all cell contents

#### 4. View Dispatch & Placeholder
**File:** `comparison.js` (ADD)
- [x] `renderViewContent(container, viewName, concepts, mode)` — checks `VIEW_REGISTRY[viewName]` for registered render function. If registered, calls it. If null, calls `renderPlaceholder()`.
- [x] `renderPlaceholder(container, viewName, concepts)` — renders `.compare-placeholder` card showing: view label as heading, list of concept names with family badges and IDs. Confirms correct data routing per FR-16.

#### 5. Wire into renderAll
**File:** `comparison.js` (MODIFY)
- [x] `renderAll()` now calls `renderIntegrated()` or `renderLandscape()` based on `_state.mode`
- [x] Show/hide `#empty-state` vs `#mode-toggle` + layout based on concept count

### Validation

**Full manual testing checklist (design.md#validation-approach):**

**URL parsing:**
- [x] `/compare` → empty state with guidance message
- [x] `/compare?concepts=arc,sparc` → Integrated mode, Categorical (left) + Summary (right), placeholder cards show concept names
- [x] `/compare?mode=landscape&concepts=arc,sparc,iter,demo` → Landscape mode, 2x2 grid, each cell shows concept name + view name
- [x] `/compare?mode=integrated&concepts=a,b,c,d,e` → auto-corrects to Landscape
- [x] `/compare?concepts=arc,INVALID,sparc` → skips invalid, warning banner, 2 concepts loaded
- [x] `/compare?mode=integrated&concepts=arc,sparc&left=capex&right=sensitivity` → custom view selections load correctly

**Mode toggle:**
- [x] 2 concepts: both modes available, click toggles layout
- [x] 4 concepts: Integrated disabled, Landscape active
- [x] Toggle does not reload page

**Concept picker:**
- [x] Add concept → layout re-renders with new concept in panels/grid
- [x] Remove concept → layout updates, mode re-evaluated
- [x] Add to 4 concepts in Integrated → auto-switches to Landscape

**View selectors (Integrated):**
- [x] Change left panel view → left content updates, right unchanged
- [x] Mutual exclusion: left=CapEx → CapEx disabled in right dropdown
- [x] Change right panel → right's old value re-enabled in left dropdown
- [x] URL updates with `&left=...&right=...`

**View selectors (Landscape):**
- [x] Change view → all cells update to new view
- [x] URL updates with `&view=...`

**Browser navigation:**
- [x] Change views, then browser Back → previous state restored
- [x] Browser Forward → returns to changed state

**Tray integration (requires Item 1):**
- [x] Select on taxonomy → tray → launch Integrated → correct mode + concepts
- [x] Select on taxonomy → tray → launch Landscape → correct mode + concepts

**Regression:**
- [x] Concept profile pages: sliders, tornado, CAS, narrative all work
- [x] Index grid: renders, links work
- [x] Taxonomy: tree, constellation, neighborhood graph all work

**What We Know Works After This Phase:**
Complete comparison shell. Both modes render. View selectors dispatch correctly. Mutual exclusion works. Placeholders confirm data routing. URL fully encodes state. Shell is ready for Items 3a/3b to register real renderers.

---

## Risk Management

**See `design.md#potential-risks` for detailed risk analysis**

**Phase-Specific Mitigations:**
- **Phase 1**: Test URL parsing thoroughly before moving on — cascading bugs here are expensive
- **Phase 2**: Carry over picker click-outside pattern from current comparison.js (:814-822) — proven to work
- **Phase 3**: If `<option disabled>` mutual exclusion feels wrong, can swap to filtering options out entirely (remove instead of disable) — easy change

---

## Implementation Notes

*TO BE FILLED DURING IMPLEMENTATION*

### Phase 1 Completion
**Completed:** 2026-04-05
**Actual Changes:**
- Rewrote `compare.html.j2` — new template with all DOM containers, only loads `comparison.js`
- Appended ~120 lines of new CSS to `explorer.css` — all layout, view selector, warning, empty, placeholder classes
- Rewrote `comparison.js` (~250 lines) — constants, FAMILY_META, CONFIDENCE_BADGE, VIEW_REGISTRY (exposed as `window.VIEW_REGISTRY`), state, carried-over API helpers, new `parseUrl`/`syncUrl`/`validateAndCorrect`, full `init()` lifecycle, `popstate` listener
**Issues:** None
**Deviations:**
- Added `window.VIEW_REGISTRY = VIEW_REGISTRY` to expose registry globally — Items 3a/3b scripts need to register renderers from separate files
- `validateAndCorrect` also enforces `MAX_LANDSCAPE` (trims to 6) — not in original plan but logical
- `init()` handles failed concept fetches gracefully via `Promise.allSettled` — removes failed concepts from state and shows warning

### Phase 2 Completion
**Completed:** 2026-04-05
**Actual Changes:**
- Added `renderConceptBar()` — chips with family badge + name + × remove + add button
- Added `openPicker()`/`closePicker()`/`renderPickerList()` — shows available concepts, count, max warning
- Added `addConcept()`/`removeConcept()` — with mode auto-switch on add, no force-switch on remove
- Added `renderModeToggle()` — labels with count, integrated disabled at >3
- Wired close-picker button, click-outside listener, mode toggle click handlers in `init()`
- `renderAll()` now orchestrates concept bar + mode toggle
**Issues:** None
**Deviations:** None — all per design

### Phase 3 Completion
**Completed:** 2026-04-05
**Actual Changes:**
- Added `populateViewSelect()` — fills <select> with VIEW_REGISTRY options, supports mutual exclusion via disabled option
- Added `getConceptDataArray()` — builds concept data array from state+cache for renderers
- Added `renderViewContent()` — dispatches to registered VIEW_REGISTRY renderer or falls back to placeholder
- Added `renderPlaceholder()` — shows view label, "not yet registered" subtitle, concept names with family badges and IDs
- Added `renderIntegrated()` — shows dual-panel layout, populates selectors with mutual exclusion, renders both panels
- Added `renderLandscape()` — shows grid layout with --1up/--2up/--3up classes, builds cells with headers, renders each cell
- Wired `#select-left`, `#select-right`, `#select-landscape` change handlers in init() — partial re-renders only
- Updated `renderAll()` — dispatches to renderIntegrated or renderLandscape based on mode
**Issues:** None
**Deviations:**
- Added `getConceptDataArray()` helper (not in plan) to avoid repeating concept data assembly in multiple functions
- Landscape view selector change handler re-renders cells by querying `.compare-landscape-cell__content` elements rather than rebuilding the entire grid — more efficient

---

**Status**: Complete
