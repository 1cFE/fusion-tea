# Spec: Selection Tray & Taxonomy Integration

**Status:** Complete
**Owner:** Reid W
**Created:** 2026-04-05 17:10
**Complexity:** MEDIUM
**Branch:** ralph/concept-explorer
**Epic:** EXPLORER-UX-V2, Item 1

---

## Business Goals

### Why This Matters

The concept explorer's taxonomy views (tree, constellation, neighborhood graph) and comparison page are completely disconnected. Users discover interesting concepts through taxonomy exploration but have no mechanism to collect them for economic comparison — they must leave the taxonomy, navigate to the compare page, and re-select concepts from scratch. This breaks the analytical flow that the explorer is meant to support.

The selection tray bridges taxonomy exploration and TEA comparison by letting users accumulate concept selections across any taxonomy view, then launch directly into a comparison mode.

### Success Criteria

- [ ] Users can collect concepts during taxonomy exploration without leaving the taxonomy page
- [ ] Selection persists across taxonomy view switches (tree ↔ constellation ↔ graph)
- [ ] Users can launch either Integrated or Landscape comparison directly from the tray
- [ ] Existing taxonomy interactions (click, double-click, keyboard) are completely unaffected

### Priority

High — this is the bridge component connecting taxonomy exploration to TEA comparison. On the critical path for the full Explorer UX v2 flow. Can be built in parallel with Item 2 (Compare Shell).

---

## Problem Statement

### Current State

- Taxonomy views support exploration (focus, compare neighbors, bridge analysis) but have no concept collection mechanism
- The compare page has its own inline concept picker, completely separate from taxonomy
- No way to flow from "I found these interesting concepts in the taxonomy" to "show me their economics side-by-side"

### Desired Outcome

A persistent selection tray on the taxonomy page that accumulates concept selections via Ctrl+click across all three views, displays them as family-colored chips, and provides action buttons to launch comparison modes with the selected concepts.

---

## Scope

### In Scope

- Selection tray component (always-visible bottom bar)
- Ctrl+click handlers on tree leaves, constellation dots, and neighborhood graph nodes
- Anchored popover on Ctrl+click with confirm action and selection count
- Toggle behavior (Ctrl+click on selected concept removes it)
- Visual indicators on selected concepts in each view
- Family-colored chips with remove (×) button
- Action buttons with configurable count-based enable/disable
- Selection state in memory, synced to URL query params
- CSS for tray, chips, popover, and selection indicators

### Out of Scope

- Comparison page rendering (Items 2 & 3)
- Changes to existing non-Ctrl-click interactions
- Server-side changes or new API endpoints
- Selection tray on the compare page (deferred, concept.md open item #6)
- Mobile/responsive layout

### Edge Cases & Considerations

- **Ctrl vs Cmd**: macOS uses Cmd for modifier clicks; MUST detect `e.metaKey || e.ctrlKey`
- **Constellation click debounce**: Existing 300ms debounce for single/double-click detection — Ctrl+click must be detected within this existing handler, not add a parallel handler
- **Graph node types**: Only neighbor and center nodes should be selectable, not bridge nodes (bridges are intermediate concepts, not analysis targets)
- **State machine interaction**: Tray must work across all three taxonomy states (OVERVIEW, FOCUSED, COMPARING) without interfering with state transitions
- **Concept identity**: Use `concept_id` as the selection key; display `name` and `confinement_family` on chips
- **Max selection enforcement**: Popover SHOULD show count and indicate when max is reached; action buttons disable beyond max

---

## Requirements

### Functional Requirements

> Requirements below are from user's concept document and epic unless marked [INFERRED].

**Selection Tray Component**

1. **FR-1**: Tray MUST be a persistent bottom bar on the taxonomy page, always visible (empty state when no concepts selected)
2. **FR-2**: Tray MUST contain a Clear All button (left side), concept chips (center), and two action buttons (right side)
3. **FR-3**: Action buttons MUST be "Integrated Comparison" and "Landscape Comparison"
4. **FR-4**: "Integrated Comparison" button MUST be enabled only when `MIN_INTEGRATED <= count <= MAX_INTEGRATED`
5. **FR-5**: "Landscape Comparison" button MUST be enabled only when `MIN_LANDSCAPE <= count <= MAX_LANDSCAPE`
6. **FR-6**: Default limits: `MIN_INTEGRATED = 1`, `MAX_INTEGRATED = 3`, `MIN_LANDSCAPE = 1`, `MAX_LANDSCAPE = 6`. All MUST be tunable constants at top of file.
7. **FR-7**: Concept chips MUST show family-colored badge + concept name + × remove button
8. **FR-8**: Clicking × on a chip MUST remove the concept from the selection
9. **FR-9**: Clear All MUST empty the entire selection
10. **FR-10**: Clicking an enabled action button MUST navigate to the comparison page with mode and selected concept IDs encoded in the URL (URL format is Item 2's concern; this item is responsible for constructing and navigating to it)

**Ctrl+Click Selection**

11. **FR-11**: Ctrl+click (or Cmd+click on macOS) on a tree leaf, constellation dot, or neighborhood graph node MUST open an anchored popover
12. **FR-12**: Popover MUST show "Add [Concept Name] to comparison?" with a single-click confirm button
13. **FR-13**: Popover MUST show current selection count (e.g., "3 of 6 selected")
14. **FR-14**: Popover SHOULD indicate whether the concept has a cost model (via `analysis_id` presence) — e.g., "No cost model — Categorical view only"
15. **FR-15**: Ctrl+click on an already-selected concept MUST remove it from the selection (toggle behavior) — no popover needed for removal
16. **FR-16**: [INFERRED] Popover MUST dismiss on click outside, Escape, or confirm
17. **FR-17**: [INFERRED] Only one popover may be open at a time

**Visual Indicators**

18. **FR-18**: Selected concepts MUST have a visible indicator in their respective view (subtle highlight, outline, or badge on tree leaves, constellation dots, graph nodes)
19. **FR-19**: Visual indicators MUST update immediately when selection changes (add or remove)
20. **FR-20**: Concept chips SHOULD visually distinguish concepts with cost models from those without (e.g., subtle icon or dimmed styling)

**State Management**

21. **FR-21**: Selection MUST persist across taxonomy tab switches (tree ↔ constellation ↔ graph)
22. **FR-22**: Selection MUST be synced to URL query params (bookmarkable/shareable)
23. **FR-23**: On page load, selection MUST be initialized from URL query params if present (e.g., `/taxonomy?selected=04,05,17b` populates the tray)
24. **FR-24**: [INFERRED] Selection state MUST survive taxonomy state transitions (OVERVIEW → FOCUSED → COMPARING and back)

**Non-Interference**

25. **FR-25**: Existing click behavior (single-click focus, double-click navigate) MUST be completely unchanged when Ctrl/Cmd is not held
26. **FR-26**: Existing keyboard interactions (Enter/Space on tree leaves) MUST be unaffected
27. **FR-27**: [INFERRED] Graph bridge nodes MUST NOT be selectable (only center and neighbor nodes)

### Non-Functional Requirements

- **NFR-1**: Tray MUST not obscure taxonomy content — taxonomy layout MUST account for tray height
- **NFR-2**: Popover positioning MUST not overflow viewport — anchor to element with viewport-aware placement

---

## Acceptance Criteria

### Core Functionality

- [ ] Tray renders on taxonomy page in empty state on initial load
- [ ] Ctrl+click on tree leaf opens popover anchored to the leaf
- [ ] Ctrl+click on constellation dot opens popover anchored to the dot
- [ ] Ctrl+click on neighborhood graph node opens popover anchored to the node
- [ ] Confirming popover adds concept chip to tray with correct family color
- [ ] Ctrl+click on already-selected concept removes it (no popover)
- [ ] × button on chip removes concept from selection
- [ ] Clear All empties all chips
- [ ] Integrated button enables/disables per configured limits
- [ ] Landscape button enables/disables per configured limits
- [ ] Clicking enabled action button navigates to comparison page with correct URL params
- [ ] Selection persists when switching taxonomy tabs
- [ ] Selection persists across taxonomy state transitions (OVERVIEW ↔ FOCUSED ↔ COMPARING)
- [ ] URL query params reflect current selection
- [ ] Navigating to `/taxonomy?selected=id1,id2` populates tray from URL on page load

### Visual & Interaction Quality

- [ ] Family-colored chips use existing CSS color variables (`--color-badge-mfe`, etc.)
- [ ] Selected concepts show visual indicator in each view type
- [ ] Popover dismisses on click outside, Escape, or confirm
- [ ] Only one popover open at a time
- [ ] Popover indicates cost model availability for the concept
- [ ] Chips visually distinguish concepts with vs. without cost models

### Non-Regression

- [ ] Single-click on tree leaf still focuses concept (no Ctrl held)
- [ ] Double-click on constellation dot still focuses concept
- [ ] Single-click on graph neighbor still shows bridges
- [ ] Double-click on graph neighbor still re-centers
- [ ] Keyboard navigation on tree still works
- [ ] Existing tooltip/hover behavior on graph unchanged

---

## Related Artifacts

- **Concept:** `.project/active/explorer-ux-v2/concept.md`
- **Epic:** `.project/backlog/epic_explorer_ux_v2.md` (Item 1)
- **Design:** `.project/active/selection-tray/design.md` (to be created)

---

**Next Steps:** After approval, proceed to `/_my_design`
