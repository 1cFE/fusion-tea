# Epic: Explorer UX v2

**Epic ID**: EXPLORER-UX-V2
**Status**: Active
**Priority**: High
**Created**: 2026-04-05
**Estimated Effort**: 6–9 days

---

## Executive Summary

Rebuild the concept explorer's comparison experience to bridge taxonomy exploration and TEA comparison. Adds a persistent selection tray across taxonomy pages, replaces the current comparison page with two purpose-built modes (Integrated for deep 1–3 concept comparison, Landscape for broader 1–6 concept survey), and introduces two new view types (Categorical, Summary) alongside rebuilt versions of CapEx and Sensitivity.

**Critical Success Factor**: A user can select concepts on any taxonomy view, then launch a comparison that shows integrated economics on shared axes — without leaving the explorer.

---

## Why This Epic?

**Current State**:
- Taxonomy views (tree, constellation, neighborhood graph) and comparison page are disconnected — no way to flow from exploration to economics
- Comparison page is a flat 4-concept picker with tabs for sensitivity, CAS, and headline — no integrated charting on shared axes
- No Categorical view (taxonomy attributes alongside economics)
- No Summary/LCOE-driver view
- Sensitivity and CAS charts are functional but not designed for cross-concept comparison (separate charts, not shared axes)

**Future State**:
- Selection tray on all taxonomy pages enables fluid concept collection during exploration
- Two comparison modes optimized for different analytical tasks (deep vs. broad)
- Four view types covering the full analysis workflow: categorical context → summary economics → capital drill-down → sensitivity ranking
- URL-encoded selections for shareability

---

## Success Criteria

- [ ] Selection interaction on tree leaf, constellation dot, or graph node adds concept to tray
- [ ] Selection tray appears on all taxonomy pages with family-colored chips
- [ ] Integrated mode renders two side-by-side panels with independent view selectors (mutual exclusion)
- [ ] Landscape mode renders grid of concept panels with synchronized axes
- [ ] All four view types (Categorical, Summary, CapEx, Sensitivity) render in both modes
- [ ] URL encodes mode + selected concepts (shareable, bookmarkable)
- [ ] Existing taxonomy views (tree, constellation, neighborhood graph) continue to work unchanged
- [ ] Existing concept profile pages unaffected

---

## Backlog Items

### Item 1: Selection Tray & Taxonomy Integration [1–1.5 days]

**Type**: Implementation

**Objective**: Add a persistent bottom-bar selection tray to all taxonomy pages with selection interactions on tree, constellation, and neighborhood graph elements.

**Current State**:
- ✅ Taxonomy page exists with tree, constellation, and neighborhood graph views
- ✅ Click/double-click interactions exist on all three views (navigate to concept, compare pair)
- ❌ No selection mechanism across taxonomy views
- ❌ No persistent selection state (tray)
- ❌ No add-to-comparison interaction on any taxonomy element

**Scope**:
1. **Selection tray component** (`selection_tray.js`):
   - Bottom bar with Clear All, concept chips (family-colored), action buttons
   - "Integrated Comparison" button (enabled when `MIN_INTEGRATED ≤ count ≤ MAX_INTEGRATED`)
   - "Landscape Comparison" button (enabled when `MIN_LANDSCAPE ≤ count ≤ MAX_LANDSCAPE`)
   - Constants tunable at top of file
2. **Selection interaction** on all three taxonomy views:
   - Tree leaf nodes (`tree_view.js`)
   - Constellation dots (`constellation.js`)
   - Neighborhood graph nodes (`neighborhood_graph.js`)
   - Each opens anchored popover: "Add [Name] to comparison?" with confirm
   - Toggle behavior: interacting on already-selected concept removes it
3. **Interaction mechanism — must decide in design phase**:
   - Option A: Modifier+click (Cmd on Mac, Ctrl on Windows) — compact but invisible affordance
   - Option B: Hover-revealed `+` icon on concept elements — visible affordance, no modifier conflict
   - Option C: Both (modifier as power-user shortcut, icon as discoverable path)
   - **Key constraint**: Ctrl+click = right-click on macOS. Must not break existing interactions.
4. **Visual indicators** on selected concepts (subtle highlight/outline on tree leaves, constellation dots, graph nodes)
5. **CSS** for tray positioning, chip styling, popover
6. **Selection state management**: In-memory array, synced to URL query params

**Out of Scope**:
- Comparison page rendering (Items 2, 3a, 3b)
- Any changes to existing click/double-click interactions (navigate, compare pair)
- Server-side changes

**Success Criteria**:
- [ ] Tray renders on taxonomy page, persists across tab switches (tree ↔ constellation ↔ graph)
- [ ] Selection interaction on any concept element in any view adds/removes from tray
- [ ] Chips show family-colored badges with remove (×) button
- [ ] Action buttons enable/disable based on selection count and configured limits
- [ ] Selecting an already-selected concept removes it (toggle)
- [ ] Clear All empties selection
- [ ] Selection state survives taxonomy tab switching
- [ ] No conflict with macOS Ctrl+click (right-click) behavior

**Estimated Effort**: 1.5 days (spec 1h, design 2h, plan 1h, execute 8h)

**Location**: `.project/active/selection-tray/`

**Dependencies**: None

**Deliverables**:
- `.project/active/selection-tray/spec.md`
- `.project/active/selection-tray/design.md`
- `.project/active/selection-tray/plan.md`
- `exploration/concept_explorer/static/js/selection_tray.js`
- Modifications to `tree_view.js`, `constellation.js`, `neighborhood_graph.js`, `taxonomy.js`
- CSS additions to `explorer.css`

---

### Item 2: Comparison Page Shell — Routing, Modes & Layout [1–1.5 days] ✅ COMPLETE

**Type**: Implementation
**Completed**: 2026-04-05

**Objective**: Replace the current comparison page with the new two-mode (Integrated/Landscape) shell — routing, URL encoding, mode switching, panel layout, and view selector UI. View content rendering is stubbed (placeholder panels).

**Current State**:
- ✅ `/compare` route exists with flat 4-concept picker and 3 tabs
- ✅ `comparison.js` has concept caching, manifest loading, chip rendering
- ⚠️ Current page mixes selection and display — new design separates selection (tray on taxonomy) from display (comparison page)
- ❌ No mode concept (Integrated vs. Landscape)
- ❌ No dual-panel layout with independent view selectors
- ❌ No grid layout with synchronized axes

**Scope**:
1. **URL scheme**: Encode mode + concept IDs (e.g., `/compare?mode=integrated&concepts=arc,sparc,iter`)
   - Parse on page load, populate selection from URL
   - Update URL on mode/concept changes (history.replaceState)
2. **Mode switching**: Toggle or auto-select based on concept count
3. **Integrated layout**: Two-panel side-by-side with independent view selector dropdowns
   - Mutual exclusion: selecting a view in one panel disables it in the other
   - Panel sizing (50/50 or configurable)
4. **Landscape layout**: Single view selector at top, responsive grid below
   - Auto-layout: 2-up for 2–3 concepts, 3-up for 4–6
5. **View selector dropdowns**: Four options (Categorical, Summary, CapEx, Sensitivity)
   - Panels render placeholder content until Item 3 implements actual views
6. **Concept data loading**: Carry over `comparison.js` caching (`conceptCache`) and manifest loading logic. The concept picker UI and tab-switching logic will be discarded — selection now lives in the tray (Item 1), and view selection is per-panel dropdowns rather than tabs.
7. **Template**: New or rewritten `compare.html.j2`
8. **Server route**: Update `/compare` endpoint if needed (likely just template swap)

**Out of Scope**:
- Actual chart rendering for any view type (Item 3)
- Selection tray on comparison page (deferred per concept.md open item #6)
- Responsive/mobile layout

**Success Criteria**:
- [x] URL encodes mode + concepts and is bookmarkable
- [x] Navigating to URL with query params loads correct mode and concepts
- [x] Integrated mode shows two panels with independent view selectors
- [x] View mutual exclusion works in Integrated mode
- [x] Landscape mode shows responsive grid (2-up or 3-up based on concept count)
- [x] Mode toggle switches layout without full page reload
- [x] Placeholder panels confirm correct concept data is available in each slot

**Estimated Effort**: 1.5 days (spec 1h, design 2h, plan 1h, execute 8h)

**Location**: `.project/active/compare-shell/`

**Dependencies**: None (can be developed in parallel with Item 1; Item 1 provides the navigation path, but this item can be tested via direct URL)

**Deliverables**:
- `.project/active/compare-shell/spec.md`
- `.project/active/compare-shell/design.md`
- `.project/active/compare-shell/plan.md`
- Rewritten `compare.html.j2`
- New or rewritten `comparison.js`
- CSS additions for dual-panel and grid layouts

---

### Item 3a: Categorical & Summary Views [1–1.5 days] ✅ COMPLETE

**Type**: Implementation
**Completed**: 2026-04-05

**Objective**: Implement the two new view types — Categorical (taxonomy attribute comparison) and Summary (LCOE driver breakdown) — for both Integrated and Landscape rendering contexts. These are the highest-value views for the immediate sanity-checking use case.

**Current State**:
- ❌ No Categorical view exists anywhere in the explorer
- ❌ No Summary/LCOE-driver view exists
- ✅ `HeadlineEconomics` model has LCOE, overnight cost, P_net, Q_eng, capacity factor
- ✅ `concept_registry.json` has taxonomy attributes for all concepts
- ✅ Item 2's shell provides panel layout and view rendering hooks

**Scope**:
1. **View rendering API contract**: Each view exports `renderIntegrated(container, concepts)` and `renderLandscape(container, concepts)` for the shell to call. Establish this contract here; Items 3b views follow the same pattern.
2. **Categorical View** (`view_categorical.js`):
   - Table comparing taxonomy attributes across selected concepts
   - Data source: `concept_registry.json` taxonomy fields
   - Integrated mode: single merged comparison table
   - Landscape mode: per-concept attribute cards
   - Graceful degradation: works for all concepts (no cost model dependency)
3. **Summary View** (`view_summary.js`):
   - LCOE driver breakdown visualization (stacked bar, waterfall, or grouped bar — decide in design)
   - Key metrics table: LCOE, overnight cost, P_net, Q_eng, capacity factor, top CAS driver
   - Data source: `HeadlineEconomics` from concept data
   - Integrated mode: grouped/overlaid on shared axes
   - Landscape mode: per-concept panels with synced scales
   - Graceful degradation: concepts without cost models show "No cost model available" placeholder (not a JS error)
4. **Axis synchronization utility**: Shared scale computation for Landscape mode panels. Build as reusable utility since Items 3b views will also need it.

**Out of Scope**:
- CapEx and Sensitivity views (Item 3b)
- `HeadlineEconomics` data model changes (current fields sufficient for v1)
- Slider-driven recomputation on comparison page

**Success Criteria**:
- [x] Categorical view renders in both modes for any selection of concepts
- [x] Summary view renders LCOE breakdown + metrics table in both modes
- [x] Summary view degrades gracefully for concepts without cost models (placeholder, no error)
- [x] Landscape mode synchronizes axes across concept panels
- [x] View rendering API contract documented and usable by Item 3b

**Estimated Effort**: 1 day (spec 1h, design 2h, plan 1h, execute 6h)

**Location**: `.project/active/views-categorical-summary/`

**Dependencies**: Item 2 (comparison shell provides layout and rendering hooks)

**Deliverables**:
- `.project/active/views-categorical-summary/spec.md`
- `.project/active/views-categorical-summary/design.md`
- `.project/active/views-categorical-summary/plan.md`
- `exploration/concept_explorer/static/js/view_categorical.js`
- `exploration/concept_explorer/static/js/view_summary.js`
- Axis sync utility (in shared module or inline)
- CSS for table and chart layouts

---

### Item 3b: CapEx & Sensitivity Views [1–1.5 days]

**Type**: Implementation

**Objective**: Rebuild the CapEx and Sensitivity views for the new comparison modes. Both are Plotly chart rebuilds that share the grouped/overlaid rendering concern and axis synchronization.

**Current State**:
- ✅ `tornado.js` renders per-concept sensitivity charts (Plotly) — functional but designed for single-concept view
- ✅ `cas_breakdown.js` renders per-concept stacked CAS bars (Plotly) — hard to compare across concepts
- ✅ Item 3a established the view rendering API contract and axis sync utility
- ⚠️ Existing charts not designed for shared-axis integrated rendering
- ❓ Chart type for CapEx TBD (waterfall, grouped horizontal, treemap — decide in design)
- ❓ Sensitivity overlap/filter logic TBD (threshold vs. top-N, shared parameter emphasis — decide in design)

**Scope**:
1. **CapEx View** (reworked `cas_breakdown.js` or new `view_capex.js`):
   - Improved CAS comparison chart (chart type decided in design phase)
   - CAS22 sub-account expandable detail
   - Integrated mode: grouped on shared axis
   - Landscape mode: per-concept charts with synced scales (using Item 3a's axis sync utility)
   - Graceful degradation: concepts without cost models show placeholder
2. **Sensitivity View** (reworked `tornado.js` or new `view_sensitivity.js`):
   - Tornado charts with overlap emphasis for shared parameters
   - High-sensitivity filter (threshold or top-N cap, decided in design)
   - Integrated mode: overlaid tornado lines on shared axes
   - Landscape mode: per-concept tornados with synced axes
   - Graceful degradation: concepts without sensitivities show "No sensitivity data" placeholder
3. **Design questions to resolve** (in this item's design phase):
   - CapEx chart type: waterfall vs. grouped horizontal bars vs. treemap
   - Sensitivity filtering: absolute threshold vs. top-N vs. both
   - Sensitivity overlap: how to visually emphasize shared vs. unique parameters

**Out of Scope**:
- Categorical and Summary views (Item 3a)
- Parameter metadata popovers in comparison context
- Population whiskers (concept profile feature, not comparison)

**Success Criteria**:
- [ ] CapEx view renders in both modes, improves on current stacked bars for cross-concept comparison
- [ ] CAS22 sub-accounts expandable in both modes
- [ ] Sensitivity view renders in both modes with filtered/prioritized parameters
- [ ] Shared parameters visually emphasized in Sensitivity Integrated mode
- [ ] Both views degrade gracefully for concepts without cost models or sensitivities
- [ ] Both views follow the rendering API contract from Item 3a

**Estimated Effort**: 1.5 days (spec 1h, design 2.5h, plan 1h, execute 7h)

**Location**: `.project/active/views-capex-sensitivity/`

**Dependencies**: Item 2 (shell), Item 3a (rendering API contract and axis sync utility)

**Deliverables**:
- `.project/active/views-capex-sensitivity/spec.md`
- `.project/active/views-capex-sensitivity/design.md`
- `.project/active/views-capex-sensitivity/plan.md`
- `exploration/concept_explorer/static/js/view_capex.js` (or reworked `cas_breakdown.js`)
- `exploration/concept_explorer/static/js/view_sensitivity.js` (or reworked `tornado.js`)
- CSS for chart layouts

---

### Item 4: End-to-End Wiring & Polish [0.5–1 day]

**Type**: Integration

**Objective**: Wire the selection tray (Item 1) to the comparison page (Items 2/3a/3b), verify end-to-end flow, URL shareability, and visual consistency. Regression-test existing pages.

**Current State**:
- ✅ Items 1, 2, 3a, 3b developed independently
- ✅ Edge case handling built into each view's success criteria (graceful degradation)
- ❓ Tray → comparison page navigation not yet wired
- ❓ Cross-page visual consistency untested

**Scope**:
1. **Tray → comparison navigation**: Wire action buttons to navigate to `/compare?mode=...&concepts=...` with correct URL params
2. **End-to-end smoke test**: Select on taxonomy → tray populates → launch comparison → views render → URL is shareable
3. **URL shareability**: Copy URL, open in new tab → same mode, concepts, and view selections load
4. **Regression testing**:
   - Concept profile page: sliders, tornado, CAS, narrative all work
   - Index grid: renders, links work
   - Taxonomy: tree, constellation, neighborhood graph — existing interactions preserved alongside new selection behavior
5. **Visual polish**: Consistent spacing, transitions between tray and comparison page, loading/empty states

**Out of Scope**:
- New features beyond what Items 1–3b deliver
- Edge case handling (owned by individual view items)
- Performance optimization (unless blocking)
- Automated test suite

**Success Criteria**:
- [ ] Full flow works: taxonomy selection → tray → comparison page → all four views
- [ ] URL copy/paste reproduces comparison state (mode + concepts + view selections)
- [ ] No regressions on concept profile, index grid, or taxonomy views
- [ ] Loading and error states display correctly
- [ ] Visual consistency across tray and comparison page

**Estimated Effort**: 0.5–1 day (no formal spec/design — plan.md with test checklist + execution)

**Location**: `.project/active/explorer-integration/`

**Dependencies**: Items 1, 2, 3a, and 3b

**Deliverables**:
- `.project/active/explorer-integration/plan.md` (test checklist)
- Bug fixes and polish commits

---

## Dependencies

**External**:
- Plotly.js (already vendored)
- Cytoscape.js (already vendored)

**Internal**:
- Concept analysis data must exist for at least 2–3 concepts to test comparison views
- `HeadlineEconomics` model is sufficient as-is for initial Summary view; refinement deferred

**Item Dependency Graph**:
```
Item 1 (Selection Tray)          Item 2 (Compare Shell)
  │  no dependency between ──────── │
  │                                 └─> Item 3a (Categorical + Summary)
  │                                       │
  │                                       └─> Item 3b (CapEx + Sensitivity)
  │                                             │
  └─────────────────────────────────────────────> Item 4 (Wiring & Polish)
```

Items 1 and 2 can be developed in parallel. Item 3a depends on Item 2's shell. Item 3b depends on 3a (for rendering API contract and axis sync). Item 4 wires everything together.

**Natural checkpoint**: After Items 1 + 2 + 3a, the explorer is usable for sanity-checking with Categorical and Summary views. Items 3b and 4 add deeper drill-downs and polish.

---

## Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Integrated shared-axis charts harder than expected (Plotly layout quirks) | Med | Prototype in design phase; fall back to aligned-but-separate charts |
| Selection interaction conflicts with OS behavior (Ctrl+click = right-click on Mac) | Med | Resolve modifier key vs. hover icon in Item 1 design phase — not deferred to integration |
| Too few concepts have cost models for meaningful comparison | Med | Categorical view works for all concepts (no cost model needed); Summary degrades gracefully |
| Summary view blocked on HeadlineEconomics refinement | Low | Current fields sufficient for v1; refinement is additive |
| CapEx/Sensitivity design questions stall Item 3b | Med | Design phase resolves chart type + filter logic before implementation; can fall back to improved versions of existing charts |

---

## Timeline

**Total Effort**: 6–7 days

| Item | Effort | Dependencies | Parallelizable |
|------|--------|--------------|----------------|
| Item 1: Selection Tray | 1–1.5 days | None | Yes (with Item 2) |
| Item 2: Compare Shell | 1–1.5 days | None | Yes (with Item 1) |
| Item 3a: Categorical + Summary | 1–1.5 days | Item 2 | No |
| Item 3b: CapEx + Sensitivity | 1–1.5 days | Item 3a | No |
| Item 4: Wiring & Polish | 0.5–1 day | Items 1, 2, 3a, 3b | No |

**Critical path**: Item 2 → Item 3a → Item 3b → Item 4

**Usable checkpoint**: After Item 2 + Item 3a (+ Item 1 for taxonomy flow), the explorer supports Categorical and Summary comparison — sufficient for sanity-checking analyses.

---

## Lessons Learned (Post-Completion)

*Fill in after epic is complete*

**What Went Well**:
- TBD

**What Could Improve**:
- TBD

**Surprises**:
- TBD

---

**Last Updated**: 2026-04-05
**Next Action**: Begin Item 3b (CapEx + Sensitivity Views)
