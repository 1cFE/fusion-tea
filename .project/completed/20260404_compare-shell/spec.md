# Spec: Comparison Page Shell — Routing, Modes & Layout

**Status:** Complete
**Owner:** Reid W
**Created:** 2026-04-05 18:48 PDT
**Complexity:** MEDIUM
**Branch:** ralph/concept-explorer
**Epic:** EXPLORER-UX-V2, Item 2

---

## Business Goals

### Why This Matters

The current comparison page (`/compare`) is a flat 4-concept picker with 3 tabs (sensitivity, CAS, headline). It mixes concept selection and display on one page. The new UX separates selection (taxonomy-side tray, Item 1) from display (this comparison page), and introduces two purpose-built modes for different analytical tasks:

- **Integrated mode** (1–3 concepts): Deep side-by-side comparison with two panels showing different views simultaneously
- **Landscape mode** (1–6 concepts): Broad survey with a single view rendered across a responsive grid of concept panels

This item builds the structural shell — routing, layout, mode switching, and view selector UI — that Items 3a and 3b plug actual view renderers into.

### Success Criteria

- [ ] A user can navigate to a URL with mode + concepts and see the correct layout immediately
- [ ] Integrated mode enables simultaneous viewing of two different analytical perspectives
- [ ] Landscape mode enables at-a-glance comparison across up to 6 concepts
- [ ] The shell is ready for Items 3a/3b to drop in real view renderers with no structural changes

### Priority

High — on the critical path (Item 2 → 3a → 3b → 4). Can be developed in parallel with Item 1.

---

## Problem Statement

### Current State

- `/compare` serves a static page with an inline concept picker (max 4) and 3 tab-switched views
- No concept of modes (Integrated vs. Landscape)
- No dual-panel layout with independent view selectors
- No grid layout with per-concept panels
- Selection tray (Item 1) already generates URLs in the format `/compare?mode=integrated&concepts=id1,id2` — but the comparison page doesn't parse them

### Desired Outcome

A new comparison page that:
1. Parses `?mode=...&concepts=...` from the URL and renders the appropriate layout
2. Provides two distinct layouts optimized for different concept counts and analytical tasks
3. Exposes view selector dropdowns that Items 3a/3b will wire to real renderers
4. Preserves the existing `conceptCache` and manifest-loading infrastructure

---

## Scope

### In Scope

- URL parsing and encoding (`mode`, `concepts` query params)
- Mode switching (auto-select + manual toggle)
- Integrated layout: two side-by-side panels with independent view selector dropdowns
- Landscape layout: single view selector, responsive concept grid
- View selector UI with four options (Categorical, Summary, CapEx, Sensitivity)
- Placeholder panel content (confirming correct concept data per slot)
- Concept data loading (carry over `fetchManifest`, `fetchConcept`, `conceptCache`)
- Rewritten `compare.html.j2` template
- Server route update if needed
- CSS for dual-panel and grid layouts

### Out of Scope

- Actual chart/table rendering for any view type (Items 3a/3b)
- Responsive/mobile layout
- Changes to concept profile pages, taxonomy views, or other existing pages
- Changes to `ExplorerState` or `/api/state` endpoint

### Edge Cases & Considerations

- URL with no query params → empty state with guidance message
- URL with concepts but no mode → auto-select mode based on count
- URL with invalid concept IDs → skip invalid, render valid ones, show warning
- URL with mode=integrated but >3 concepts → auto-switch to landscape
- URL with 0 valid concepts after filtering → empty state
- Browser back/forward → `popstate` listener updates layout without full reload
- View selector state in URL: decide in design whether URL encodes selected views (e.g., `&left=summary&right=capex`) for shareability, or only encodes mode + concepts (recipients see defaults). Trade-off: richer URLs vs. simpler scheme. Low priority but affects shareability fidelity.

---

## Requirements

### Functional Requirements

> Requirements below are from user's request unless marked [INFERRED].

**URL Scheme**

1. **FR-1**: The page MUST parse `mode` and `concepts` from URL query parameters on load. Format: `/compare?mode=integrated&concepts=id1,id2,id3`
2. **FR-2**: The page MUST update the URL via `history.replaceState` when mode or concept set changes, keeping URLs bookmarkable and shareable
3. **FR-3**: Navigating to a URL with valid query params MUST load the correct mode and concepts without user interaction

**Mode Selection**

4. **FR-4**: Mode MUST auto-select based on concept count: ≤3 → Integrated, >3 → Landscape
5. **FR-5**: A manual mode toggle MUST be available. Integrated MUST be disabled when concept count > MAX_INTEGRATED (3). Landscape is always available. This matches the selection tray's button enable/disable logic.
6. **FR-6**: If URL specifies `mode=integrated` with >3 concepts, the page MUST auto-correct to Landscape mode on load (URL correction, not user-facing error)

**Integrated Layout**

7. **FR-7**: Integrated mode MUST render two side-by-side panels, each with an independent view selector dropdown
8. **FR-8**: View selectors MUST enforce mutual exclusion — selecting a view in one panel disables it in the other's dropdown
9. **FR-9**: Panels MUST default to Categorical (left) and Summary (right) on initial load
10. **FR-10**: [INFERRED] Panel sizing SHOULD be 50/50 split

**Landscape Layout**

11. **FR-11**: Landscape mode MUST render a single view selector at the top and a responsive grid of concept panels below
12. **FR-12**: Grid MUST auto-layout: 2-up for 1–3 concepts, 3-up for 4–6 concepts
13. **FR-13**: [INFERRED] Landscape view selector SHOULD default to Categorical on initial load

**View Selectors**

14. **FR-14**: All view selector dropdowns MUST offer four options: Categorical, Summary, CapEx, Sensitivity
15. **FR-15**: Selecting a view MUST render placeholder content in the corresponding panel(s) until Items 3a/3b provide real renderers
16. **FR-16**: [INFERRED] Placeholder content SHOULD confirm concept identity (show concept name, ID, and selected view name) to verify correct data routing

**Data Loading**

17. **FR-17**: The page MUST carry over `fetchManifest()`, `fetchConcept()`, and `conceptCache` from the current `comparison.js`
18. **FR-18**: The page MUST fetch full concept data for all concepts in the URL on load
19. **FR-19**: [INFERRED] Loading state SHOULD display while concept data is being fetched

**Concept Editing**

20. **FR-20**: The comparison page MUST provide a way to modify the concept set without returning to taxonomy. This SHOULD be a lightweight concept picker (add/remove) accessible from the page header area.
21. **FR-21**: Adding or removing a concept MUST update the URL, re-evaluate mode availability (FR-5 constraints), and re-render the active layout
22. **FR-22**: [INFERRED] The picker SHOULD reuse the manifest data and family-colored badges from the existing concept picker pattern

**Navigation**

23. **FR-23**: [INFERRED] Browser back/forward SHOULD update the layout via `popstate` listener without full page reload

---

## Acceptance Criteria

### Core Functionality

- [ ] URL encodes mode + concepts and is bookmarkable
- [ ] Navigating to URL with query params loads correct mode and concepts
- [ ] Integrated mode shows two panels with independent view selectors
- [ ] View mutual exclusion works in Integrated mode (selecting a view in one panel disables it in the other)
- [ ] Integrated panels default to Categorical (left) and Summary (right)
- [ ] Landscape mode shows responsive grid (2-up for ≤3, 3-up for 4–6)
- [ ] Mode auto-selects based on concept count (≤3 → Integrated, >3 → Landscape)
- [ ] Mode toggle disables Integrated when concept count > 3; Landscape always available
- [ ] Mode=integrated with >3 concepts auto-corrects to Landscape on load
- [ ] Concept picker allows adding/removing concepts without leaving the page
- [ ] Adding/removing concepts updates URL and re-evaluates mode availability
- [ ] Placeholder panels confirm correct concept data routing (show concept name + view name)

### Error & Edge Cases

- [ ] URL with no params shows empty state with guidance
- [ ] URL with invalid concept IDs skips them and shows warning
- [ ] URL with 0 valid concepts shows empty state
- [ ] URL with concepts but no mode auto-selects mode

### Quality & Integration

- [ ] Existing taxonomy views (tree, constellation, neighborhood graph) unaffected
- [ ] Existing concept profile pages unaffected
- [ ] Selection tray (Item 1) URLs (`/compare?mode=...&concepts=...`) work correctly with this page
- [ ] `conceptCache` and manifest loading work as before

---

## Related Artifacts

- **Epic:** `.project/backlog/epic_explorer_ux_v2.md` (Item 2)
- **Item 1 (Selection Tray):** `.project/active/selection-tray/` — generates the URLs this page parses
- **Design:** `.project/active/compare-shell/design.md` (to be created)
- **Current comparison.js:** `exploration/concept_explorer/static/js/comparison.js`
- **Current template:** `exploration/concept_explorer/templates/compare.html.j2`
- **Selection tray:** `exploration/concept_explorer/static/js/selection_tray.js`

---

**Next Steps:** After approval, proceed to `/_my_design`
