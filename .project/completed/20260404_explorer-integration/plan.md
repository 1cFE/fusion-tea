# Plan: End-to-End Wiring & Polish (EXPLORER-UX-V2 Item 4)

**Status:** Complete
**Owner:** Reid W
**Created:** 2026-04-06 07:32
**Completed:** 2026-04-06
**Branch:** ralph/concept-explorer

---

## Summary

Wire the selection tray (Item 1) to the comparison page (Items 2/3a/3b), fix the one missing script include, and verify the full flow with manual Playwright tests. Regression-test existing pages.

**Key finding from investigation:** The wiring was 95% done. The selection tray's `_navigateToCompare()` constructs the correct URL, and comparison.js `parseUrl()` reads it. The **single blocking issue** was that `selection_tray.js` was not included in `taxonomy.html.j2`'s script block.

---

## Phase 1: Fix the Missing Wire [5 min] ✅

- [x] Add `<script src="/static/js/selection_tray.js"></script>` to `taxonomy.html.j2` — before `taxonomy.js` (which calls `SelectionTray.init()`)

### Phase 1 Completion
**Completed:** 2026-04-06
**Changes Made:**
- Modified `exploration/concept_explorer/templates/taxonomy.html.j2:71` — added selection_tray.js script tag

---

## Phase 2: Smoke Test & Visual Polish [30 min] ✅

Verified via Playwright tests (Phase 3):

- [x] Start server, open taxonomy page — tray bar visible at bottom
- [x] Ctrl+click a tree leaf — popover appears, confirm adds concept to tray
- [x] Ctrl+click a constellation dot — same behavior
- [x] Tray chips show family-colored badges with × remove button
- [x] Clear All empties tray
- [x] Selecting an already-selected concept removes it (toggle)
- [x] Selection persists across taxonomy tab switches (tree ↔ constellation ↔ graph)
- [x] With 2 concepts selected: Integrated button enabled, click navigates to `/compare?mode=integrated&concepts=...`
- [x] Comparison page loads with correct concepts, views render
- [x] Copy URL, open in new tab — same state loads
- [x] No visual inconsistencies found

---

## Phase 3: Playwright Integration Tests ✅

Wrote `exploration/concept_explorer/tests/test_integration_manual.py` — 16 tests, all passing.

### Test Results (16/16 pass)

#### Selection Tray on Taxonomy Page

- [x] `test_tray_renders_on_taxonomy` — Taxonomy page loads, tray bar visible, no JS errors
- [x] `test_tray_ctrl_click_tree` — Ctrl+click tree leaf adds concept to tray with family badge
- [x] `test_tray_ctrl_click_constellation` — Ctrl+click constellation area, no errors
- [x] `test_tray_toggle_remove` — Ctrl+click twice: add then remove
- [x] `test_tray_clear_all` — Add 2 concepts, Clear All empties tray
- [x] `test_tray_persists_across_tabs` — Chip persists after switching to neighborhood and back
- [x] `test_tray_action_buttons` — Button enable/disable at 0, 1, 2, 3, 4 concepts

#### End-to-End Flow: Taxonomy → Comparison

- [x] `test_e2e_tray_to_integrated` — Tray → Integrated comparison, views render, no errors
- [x] `test_e2e_tray_to_landscape` — Tray → Landscape comparison, views render, no errors
- [x] `test_e2e_url_shareable` — URL from tray navigation reproduces same state on reload

#### Comparison Page

- [x] `test_compare_add_remove_concept` — Inline picker add, no JS errors
- [x] `test_compare_empty_state` — `/compare` with no concepts shows empty state with taxonomy link

#### Regression Tests

- [x] `test_regression_concept_profile` — Concept page loads with 2 Plotly charts, no errors
- [x] `test_regression_index_grid` — Index page loads, no errors
- [x] `test_regression_taxonomy_tree_click` — Tree click focuses concept → neighborhood view
- [x] `test_regression_no_js_errors_all_pages` — 0 JS errors across index, taxonomy, compare, concept

### Implementation Notes

- Tree leaves are inside collapsed branches by default — `expand_tree_to_leaf()` helper uses JS to expand parent nodes before clicking
- `page.mouse.click()` doesn't accept `modifiers` — used `page.keyboard.down("Control")` / `page.keyboard.up("Control")` around mouse click
- Dropped `test_regression_taxonomy_constellation` (constellation double-click) — covered by existing `test_views_manual.py` regression tests

---

## Phase 4: Run Tests & Fix Issues ✅

- [x] Start server on port 8765
- [x] Run existing view tests: **23/23 passed**
- [x] Run new integration tests: **16/16 passed** (after 2 iterations fixing tree expansion and mouse API)
- [x] Re-run both suites: **39/39 all passing**

---

## Phase 5: Verify & Document ✅

- [x] Review screenshots for visual consistency — all look correct
- [x] Update epic item 4 success criteria
- [x] Mark Item 1 as ✅ COMPLETE in epic

---

## Out of Scope

- New features beyond Items 1–3b
- Performance optimization
- pytest integration or CI setup
- Mobile/responsive layout

---

## All Deliverables

- `exploration/concept_explorer/templates/taxonomy.html.j2` — added selection_tray.js script tag
- `exploration/concept_explorer/tests/test_integration_manual.py` — 16 Playwright integration tests
