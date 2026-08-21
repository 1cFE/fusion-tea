# Spec: Concept Page CapEx — Tabbed Widget (Table + Treemap)

**Status:** Implemented
**Owner:** Reid W
**Created:** 2026-04-26
**Complexity:** LOW
**Branch:** pipeline-cleanup

---

## Work Item Summary

Replace the unreadable single-stacked-bar CAS breakdown on `/concept/{id}` with a single widget that offers two views via a tab toggle: **Table** (composition stripe + ranked rows, every CAS legible) and **Treemap** (proportional tiles, click CAS22 to drill in). Move the widget **above** the Sensitivity (tornado) chart on the page.

## Why This Matters Now

Today the chart is illegible — one segment dominates and 14 others are slivers. Once parameter sliders go live, this widget becomes the live feedback loop. The widget's current position (below the tornado) also pushes the most-asked-about content below the fold; cost should come before sensitivity since it's the headline of the page.

---

## Scope

### In scope
- `exploration/concept_explorer/static/js/cas_breakdown.js` — replace `renderCASBreakdown()` body with the tabbed widget.
- `exploration/concept_explorer/templates/concept.html.j2` — move the `cas-section` block above the `sensitivity-section` block.
- Mockup at `.project/active/concept-capex-ranked-bars/mockup.html` is the visual reference.

### Out of scope
- Comparison-page CapEx (`view_capex.js`) — different file, recently rebuilt.
- Operating/financial separation, log scale, smart grouping.
- Exposing additional sub-account hierarchy beyond CAS22 (would require `costingfe` changes).
- Concept-page sections other than the two being moved relative to each other.

---

## Success Criteria

- [ ] Widget shows two views: **Table** (default) and **Treemap**, switched via a tab toggle.
- [ ] Only one view visible at a time.
- [ ] Table view: every CAS row is legible (equal vertical weight); composition stripe at top; CAS22 expands inline.
- [ ] Treemap view: tiles sized by share of total; CAS22 tile drills in to its sub-accounts; breadcrumb to navigate back.
- [ ] CAS22 expand/collapse state (table) and drill-in state (treemap) persist across re-renders so a slider drag doesn't reset them.
- [ ] Override marker (★) and hatched fill remain visible on overridden cells/tiles.
- [ ] Active tab persists across re-renders.
- [ ] CAS Cost Breakdown section sits **above** Sensitivity Analysis on the page.
- [ ] Visual approved against `mockup.html`.

---

## Related Artifacts

- **Mockup:** `.project/active/concept-capex-ranked-bars/mockup.html`
- **Current implementation:** `exploration/concept_explorer/static/js/cas_breakdown.js`
- **Current page layout:** `exploration/concept_explorer/templates/concept.html.j2`
- **Adjacent (orthogonal) work:** `.project/active/parameter-metadata-generation/design.md`

**Next Steps:** Iterate on `mockup.html`, then `/_my_design`.

---

## Implementation Notes

### Files changed
- `exploration/concept_explorer/static/js/cas_breakdown.js` — full rewrite. Replaced the Plotly stacked-bar with a pure DOM + SVG tabbed widget (Table + Treemap). Public `renderCASBreakdown(container, options)` signature preserved; `onAccountClick(casCode, accountData)` still fires for non-CAS22 rows / non-drillable treemap tiles.
- `exploration/concept_explorer/static/css/explorer.css` — appended a `cas-widget` block (~190 lines) using project design tokens (`--color-bg`, `--color-surface-*`, `--color-text-*`, `--color-border*`, `--space-*`, `--font-*`, `--radius-*`). The only non-token color is the override accent `#fcd34d` (held in a scoped `--cas-widget-override` and matching rgba hatch literals) and the link blue `#58a6ff` for the breadcrumb back-link.
- `exploration/concept_explorer/templates/concept.html.j2` — moved `#cas-section` above `#sensitivity-section`.

### Deviations from the mockup
- **State scoping.** Mockup used module-level closure vars (`activeView`, `cas22Expanded`, `drilledInto`). Production keys state by container element via a `WeakMap` so multiple widget instances on a page (or future re-mounts) stay independent and GC cleanly with their containers.
- **Theming.** Mockup hardcoded its own palette (`--bg`, `--text`, `--border`, etc.). Production uses the explorer's existing tokens (`--color-bg`, `--color-text-primary`, ...) directly. The `cas-widget` CSS block introduces only one local custom property: `--cas-widget-override` for the override accent, since the project did not already have a token for that semantic.
- **CSS namespacing.** Mockup used short class names (`.tabs`, `.stripe`, `.tile`). Production uses BEM-style `cas-widget__*` to avoid collisions with other components (the explorer already had a `.tabs` pattern in places).
- **Drill-in reset.** Added a defensive reset: if a re-render arrives where CAS22 has no detail (data shape change, e.g. switching concept context), `drilledInto` is cleared so the user isn't stranded on an empty drill view.
- **Existing public contract.** `renderCASBreakdown` previously also accepted `showSubAccounts` and `sharedScale` options. Both were unused by callers (`concept_page.js` passes only `cas` and `cas22_detail`). They're dropped in the rewrite — the param-equipped Table view always starts collapsed via stored state, and the new widget has no shared-scale concept.
- **Plotly removed from this widget.** The stacked-bar was the only remaining caller of Plotly on the concept page beyond the tornado, but tornado.js still uses it. No `plotly-basic.min.js` script tag was removed; it's still loaded for the tornado.

### Screenshot pairs (visual verification)
- `/tmp/capex_before/before_01.png` ↔ `/tmp/capex_after/after_01.png` — HTS Compact Tokamak (large, $16,975 M, CAS22 dominates, multiple overrides)
- `/tmp/capex_before/before_04.png` ↔ `/tmp/capex_after/after_04.png` — Laser ICF p-B11 ($3,017 M, mid-scale, Buildings & Structures override)
- `/tmp/capex_before/before_19.png` ↔ `/tmp/capex_after/after_19.png` — Orbital Levitated Dipole D-He3 ($352 M, small scale, with narrative + risks above)

Additional state captures under `/tmp/browser_inspect/capex_widget/`:
- `table_01.png` — default Table view
- `table_01_expanded.png` — CAS22 row expanded inline with sub-accounts under tree line; Magnets/Coils, First Wall & Blanket, Vacuum System all show ★
- `treemap_01.png` — squarified treemap of all CAS accounts; Special Materials shows ★ + hatch
- `treemap_01_drill.png` — drilled into CAS22; sub-accounts tiled, breadcrumb back-link visible
- `treemap_04.png` — concept 04 treemap; Buildings & Structures shows ★ + hatch

### Verification
- 153 tests in `exploration/concept_explorer/tests/` pass. The 39 errors are pre-existing `pytest-playwright` setup failures (`fixture 'page' not found`) in the `*_manual.py` files; not caused by this change and not in this task's scope.
- `browser_inspect` session reported 0 console errors and 0 page errors across all interactions (tab switch, table expand, treemap drill).
- Slider drag verification (state persistence) was not exercised: no concept currently has populated `parameter_metadata.range`, so the slider section never renders. The state-by-WeakMap design preserves the contract once `parameter-metadata-generation` ships.
