# Explorer UX v2 — Concept Document

**Status:** Concept approved, ready for detailed design
**Date:** 2026-04-05
**Scope:** Rebuild of concept explorer comparison UX + taxonomy→TEA bridge

---

## Motivation

Two use cases drive this work:
1. **Sanity-checking**: As concept analyses complete, the explorer is the primary tool for reviewing results before formal approval
2. **Sharing**: Once all analyses are complete, the explorer becomes the shareable artifact

Current problems:
- **Taxonomy ↔ TEA chasm**: No way to go from exploring taxonomy relationships to comparing economics
- **Poor quality cost model views**: Current comparison tabs (sensitivity, CAS, headline) need full rebuild

---

## Design Decisions

### 1. Selection Tray (Bottom Bar)

A persistent bottom bar on all taxonomy pages that bridges taxonomy exploration → TEA comparison.

**Elements:**
- **Clear All** button (left side)
- **Concept chips**: Family-colored badge + name + `×` remove button
- **Two action buttons** (right side):
  - "Integrated Comparison" — enabled when `MIN_INTEGRATED ≤ count ≤ MAX_INTEGRATED`
  - "Landscape Comparison" — enabled when `MIN_LANDSCAPE ≤ count ≤ MAX_LANDSCAPE`

**Default config (tunable constants):**
```
MIN_INTEGRATED = 1
MAX_INTEGRATED = 3
MIN_LANDSCAPE = 1
MAX_LANDSCAPE = 6
```

**Adding concepts:** Ctrl+click on any concept element (tree leaf, constellation dot, graph node) opens a small popover anchored to the element: "Add [Concept Name] to comparison?" with single-click confirm. Popover shows current selection count ("3 of 6 selected").

**Removing concepts:** `×` on chip in tray, or Ctrl+click on already-selected concept toggles it off.

### 2. TEA Comparison — Two Modes

#### Integrated Mode (1–3 concepts)
- **Layout**: Two-panel side-by-side split
- **Each panel** has an independent view selector dropdown
- **Constraint**: Panels must show different views (mutual exclusion — selecting a view in one panel grays it out in the other)
- **Charts are truly integrated** — merged onto shared axes (grouped bars, overlaid tornado lines, etc.)

#### Landscape Mode (1–6 concepts)
- **Layout**: Single view selector at top, grid of concept panels below
- **Auto-layout**: 2-up for 2–3 concepts, 3-up for 4–6
- **Each concept gets its own chart instance** with synchronized axes (shared scale, shared category order)

**URL**: Must encode mode + selected concepts for shareability. Implementation detail (single page with toggle vs. separate routes) deferred to detailed design.

### 3. Four View Types

Available in both Integrated and Landscape modes:

| View | Purpose | Notes |
|------|---------|-------|
| **Categorical** | Taxonomy comparison table (relocated from taxonomy view) | Correlate descriptive differences to economic differences. Useful when launching from taxonomy. |
| **Summary** | LCOE driver breakdown | Focus on what drives LCOE: capital contribution, O&M, energy generation, Q, capacity factor. Uses `HeadlineEconomics` data model (will be refined alongside costing models). |
| **CapEx** | CAS structure comparison | Deeper capital cost drill-down. CAS22 detail expandable. |
| **Sensitivity** | Tornado plots | Integrated mode: overlaid on shared axes. Landscape: synced axes per concept. |

### 4. Summary View — LCOE Driver Focus

**Top section**: Visualization showing LCOE breakdown into major components (capital, O&M, energy-related). Format TBD — stacked bar, waterfall, or grouped bar depending on what `HeadlineEconomics` can provide after data model refinement.

**Below**: Key driver metrics table:
- LCOE ($/MWh)
- Overnight Cost ($/kW)
- P_net (MW)
- Q_eng
- Capacity Factor
- Top CAS driver (name + % of total) — hint toward CapEx view

Data model dependency: `HeadlineEconomics` will need refinement to support the LCOE decomposition. Exact fields TBD, designed alongside costing model work.

### 5. Sensitivity View — Design Principles

Detailed layout deferred to design phase. Guiding principles:
- **Prioritize high-sensitivity parameters** (minimum threshold or max-N cap, tunable)
- **Prioritize overlap** between concepts (shared parameters shown prominently)
- **No strict requirement for overlap** on every parameter — must convey each concept's sensitivities faithfully
- **Don't show all values** — filter to meaningful sensitivities only

### 6. CapEx View

Detailed design deferred. Must improve on current stacked bars which are hard to compare across concepts. Candidates: waterfall, grouped horizontal bars, treemap. CAS22 sub-account detail should be expandable.

---

## What's NOT Changing

- **Taxonomy views**: Tree, constellation, neighborhood graph stay as-is structurally. They gain a selection layer (Ctrl+click to add) but no visual redesign.
- **Individual concept page** (`/concept/{id}`): Not in scope for this iteration.
- **Data pipeline**: `extract_explorer_data.py`, `seed_registry.py`, data models stay the same (except `HeadlineEconomics` refinement noted above).
- **Server architecture**: API endpoints may be added but existing ones don't change.

---

## Open Items for Detailed Design

1. Navigation: Single page with mode toggle vs. separate routes (must preserve URL shareability either way)
2. Summary visualization format (depends on `HeadlineEconomics` data model refinement)
3. Sensitivity tornado layout — overlap vs. union, threshold/cap tuning
4. CapEx chart type selection
5. Responsive behavior of two-panel integrated layout
6. Whether selection tray also appears on the compare page itself (for quick edits without going back to taxonomy)
