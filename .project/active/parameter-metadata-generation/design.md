# Design: Concept Page Sensitivity Restructure

**Status:** In Progress
**Owner:** Reid W
**Created:** 2026-04-26
**Updated:** 2026-04-26 (tornado DOM spike complete, design de-risked)
**Branch:** sensitivity-sliders
**Commit:** 6345555

## Overview

Restructure the costingfe concept profile page so the sensitivity sliders earn their place: tornado bars and sliders share rows, the headline economics stay pinned at the top while the user drags, and surrounding sections collapse out of the way. A small shared registry adds human-readable labels and units for the parameters that actually appear in the tornado top-15.

The data plumbing — generating `ParameterMetadata` from extraction so sliders have ranges and baselines — was completed in Phase 1 of this work item. This design covers Phase 2: the UI restructure that turns 47 unusable sliders into a tight, ranked, integrated what-if surface.

**Authoritative reference:** `mockup_v2.html` is the canonical visual / interaction spec. Treat the mockup as the design for layout details. This document explains *why* and lists the structural decisions; the mockup is *what* we build.

## Related Artifacts

- **Spec:** `.project/active/parameter-metadata-generation/spec.md`
- **UI mockup (canonical):** `.project/active/parameter-metadata-generation/mockup_v2.html`
- **UI mockup (initial sketch, sliders + tornado on rows):** `.project/active/parameter-metadata-generation/mockup.html`
- **Research:** `.project/research/20260426-134728_sensitivity-analysis-state.md`
- **Spec 12 (compute API):** `exploration/concept_explorer/docs/specs/12-computation-api.md`
- **Tornado today:** `exploration/concept_explorer/static/js/tornado.js`
- **Slider rendering today:** `exploration/concept_explorer/static/js/concept_page.js:222-510`
- **Headline today:** `exploration/concept_explorer/templates/concept.html.j2:34-47`
- **Phase 1 deliverable:** `exploration/concept_explorer/extract_explorer_data.py:152-204` — `generate_parameter_metadata()`

## Phase 1 — Done

For context: `generate_parameter_metadata()` in the extractor now produces a `ParameterMetadata` entry per sensitivity parameter, derived from `SensitivityAnalysis` baselines. Range = `baseline ± 30%`, clamped to `[0, ∞)`, with an additional `[0, 1]` clamp for parameters detected as fractional via name heuristics. The merge layers in `extract_costingfe()` are `{**generated, **per_concept_yaml}` (per-concept yaml wins on collision). 8 unit tests pass; 52 extraction tests green. Commit `5c3fe70`, fixed-up imports in this branch (`extract_explorer_data.py:39-50`).

This phase is closed. The remaining work in this work item is all UI.

## What was wrong with the live page (motivation)

After Phase 1 landed, the page renders 47 sliders below the headline economics, below the CAS table, with auto-generated labels (`Eta Th`, `Mn`, `Dhe3 Dd Frac`) and no units. Three failures stack:

1. **Slider → result decoupled.** The user drags `availability`; the LCOE updates 6 viewport-heights above, invisible. Live recompute works (POST /api/compute fires correctly) but the feedback isn't visible from where the action happens.
2. **Too many sliders, undifferentiated.** 24 of 47 params have `|elasticity| < 0.001` — derived constants and pinned values that move LCOE by zero. Showing them as full-width sliders alongside the genuinely-impactful ones flattens the signal.
3. **Auto-generated labels are unreadable.** "Mn", "F Sub", "Dhe3 Dd Frac", "P Trit" are Python identifiers, not parameter names. No units means "P Coils 2.000" is dimensionally ambiguous.

## Three Decisions

### Decision A — Sliders co-locate with tornado bars (single integrated grid)

**What changes.** Today: tornado chart and "Parameter What-If" sliders are two separate sections rendering the same parameter list. New: one integrated component — each row is `[name | sensitivity bar | slider | value]`. The tornado **is** the slider list.

**Why.** The tornado already curates the meaningful parameters (top-N by `|elasticity|`). Re-rendering them as sliders below adds visual noise without adding signal. Co-locating answers three questions in one glance per row: *what is this · how much does it matter · what value is it at*. See `mockup_v2.html` for exact layout.

**Consequence for tornado.js.** Today it renders Plotly bars. New: it renders an HTML/CSS grid. A canvas-based Plotly chart can't host an `<input type=range>` inline with each bar, so the implementation moves to native DOM. The user has explicitly chosen this path knowing the cost (per "leave that, I want them on the same lines"). Same public API (`renderTornado(container, options)`); same category color encoding; preserved click → parameter card behavior. The list of capabilities to preserve is in "Tornado Refactor — What Must Stay" below.

**Consequence for `concept_page.js`.** `renderSliders()` (lines 234-305) goes away as a separate function. The tornado component handles slider lifecycle, debouncing, and the `onSliderChange` callback. `concept_page.js` becomes responsible only for wiring `onSliderChange` to `POST /api/compute` and updating the sticky bar.

### Decision B — Sticky compact headline (replaces in-flow `headline-card`)

**What changes.** Today: `headline-card` is a normal section that scrolls off. New: a slim sticky bar pinned below the topnav with the same four stats (LCOE / Overnight / Net Power / Capacity Factor), concept name + family badge on the left, Reset button on the right. The big in-flow `Economics` section is removed from the template.

**Why.** With sliders co-located in the sensitivity grid, the only output the user is hunting for while dragging is the LCOE delta. Pinning that delta makes the slider→result feedback loop instantaneous regardless of scroll position. Reset visibility tracks override state — clear escape hatch that's also an "is anything changed?" indicator.

**Visual constraints (from mockup_v2):**
- Single row, ~52px tall, translucent blur background, sits below the existing topnav (`top: 44px`).
- Each stat shows `value + unit + delta-since-baseline` inline. Delta colored green (LCOE down) / orange (LCOE up) / hidden when zero.
- Concept name + MFE/IFE/MIF badge + company on the left.
- Reset button on the right; disabled when no overrides exist.

### Decision C — All major sections become collapsible

**What changes.** Today: every section is always open, all stacking vertically. New: each major section has a clickable header with chevron + content preview; body collapses on click. Defaults match the user's likely focus.

**Default state per section:**

| Section | Default | Why |
|---|---|---|
| Sensitivity & What-If | Expanded | The interactive part |
| Narrative | Collapsed | Descriptive, not load-bearing for slider work |
| Risks | Collapsed | Reference info, surfaced when needed |
| CAS Cost Breakdown | Collapsed | Less central than sensitivity |
| Sources & Methodology | Collapsed | Footer-tier |

**Header preview pattern.** Each collapsed header carries a short hint:
- `Risks` → `3 risks · 1 high`
- `CAS Cost Breakdown` → `Total Capital: 16,975 M$`
- `Narrative` → `Key bets · eliminated costs · novel costs`
- `Sensitivity & What-If` (collapsed) → `2 CHANGED` pill if overrides exist, else `Drag any slider…`

**No persistence.** Defaults reset on every navigation. Predictable state, no stale "I collapsed everything 3 weeks ago" surprises.

## Display Registry

A small shared YAML, **not** per-concept authoring. Lives at `exploration/concept_explorer/data/parameter_display_registry.yaml`, loaded once at extraction time, applied as a layer between auto-generated metadata and per-concept yaml:

```
load order (later wins):
  1. generate_parameter_metadata()           # auto: baseline + range + auto display_name
  2. parameter_display_registry.yaml         # NEW: shared display_name + display_unit + display_multiplier
  3. {concept}/model_metadata.yaml           # per-concept overrides (still supported)
```

**Scope.** Cover the parameters that appear in the tornado top-15 across costingfe concepts (~25 entries). The long tail keeps auto-generated names. Concrete starter set:

| Param key | display_name | display_unit | display_multiplier |
|-----------|--------------|--------------|-------------------|
| `availability` | Availability | % | 100 |
| `interest_rate` | Interest Rate | % | 100 |
| `inflation_rate` | Inflation Rate | % | 100 |
| `eta_th` | Thermal Efficiency | % | 100 |
| `eta_pin` | Pinj Efficiency | % | 100 |
| `R0` | Major Radius | m | 1 |
| `r_coil` | Coil Radius | m | 1 |
| `b_max` | Peak Magnetic Field | T | 1 |
| `construction_time_yr` | Construction Time | yr | 1 |
| `mn` | Energy Multiplication | — | 1 |
| `p_nbi` | NBI Power | MW | 1 |
| `plasma_t` | Plasma Temperature | keV | 1 |
| `blanket_t` | Blanket Thickness | m | 1 |
| `vessel_t` | Vessel Thickness | m | 1 |
| `elon` | Elongation | — | 1 |

Final list to be filled during implementation by surveying tornado top-15 across all 19 costingfe concepts.

**Why a registry, not per-concept yaml.** `availability` shows up in 19 concepts. Authoring it 19 times is the synchronization problem we ruled out earlier — except this time we pay it once for ~25 params, then never again. Per-concept yaml remains the override path for genuinely concept-specific naming.

## Architecture

### Page structure (replaces concept.html.j2 layout)

```
<topnav> (existing, unchanged)
<sticky-headline>
  identity (name + badge + company)
  4 stat-pills (LCOE / Overnight / Net Power / Capacity Factor)
  reset button
</sticky-headline>

<page>
  <hero>      — concept identity (no big economics — those are in the sticky bar now)
  <section narrative collapsed>
  <section risks collapsed>
  <section cas collapsed>
  <section sensitivity expanded>
    <integrated-grid>
      one row per top-N parameter:
      [ name dot · display_name · ε ]   [ |―bar―|axis|―bar―| ]   [ slider ]   [ value ]
    </integrated-grid>
  </section>
  <section sources collapsed>
</page>
```

The `Economics` section is removed; its content moves to the sticky bar.

### JS module changes

| File | Today | New |
|---|---|---|
| `tornado.js` | Plotly bars, click → parameter card, whiskers via `error_x` | Native DOM grid; sliders inline; same public API; whiskers as inline `<svg>` per row |
| `concept_page.js` | Calls `renderTornado` and `renderSliders` separately; manages slider state itself | Calls `renderTornado` only (which owns sliders); wires its `onSliderChange` to compute + sticky bar update; manages collapse state |
| New: `sticky_headline.js` | — | Renders sticky bar; takes `(initial_headline, parameterMetadata)`; exposes `update(newHeadline)` for `concept_page.js` to call after compute |
| New: `collapsible.js` (or inline) | — | Click→toggle helper; minimal, can live inline in `concept_page.js` if simple enough |

### Tornado Refactor — What Must Stay

Today's `tornado.js` does these things via Plotly. The new DOM implementation must preserve all of them:

1. Top-N filter by `|elasticity|`, sorted descending.
2. Per-bar category color encoding (5 categories, see `TORNADO_CATEGORY_COLORS`).
3. Confidence opacity (high=1.0, medium=0.8, low=0.6).
4. Hatched fill for low-confidence bars (CSS `repeating-linear-gradient` instead of Plotly fillpattern).
5. Population-range whiskers from `parameterIndex` — `[min, max]` across concepts, secondary visual weight.
6. Click → `onParameterClick(paramName, meta)` callback (already used by parameter card popover).
7. Tooltip on hover with parameter name, elasticity, category, confidence (use native `title` or a small custom tooltip).
8. Standalone-concept placeholder: when `sensitivities === null`, show "No sensitivity data — standalone cost model" instead of the grid.
9. Responsive layout — degrade gracefully at narrow widths (sliders get smaller; bar stays visible).

### Data flow on slider drag

```
user drags input[type=range] inside a row
  → tornado.js debounce (200 ms)
  → onSliderChange({ ...currentOverrides })
  → concept_page.js fetch(POST /api/compute)
  → server returns CostModelData
  → concept_page.js: stickyHeadline.update(newCostModel.headline)
                     casBreakdown.rerender(newCostModel)
                     (tornado bars do NOT update — baseline elasticity stays, per spec 12)
```

The `currentOverrides` map lives inside the tornado component (it owns the sliders). On Reset, `concept_page.js` calls `tornado.reset()` (new method), which clears overrides, returns sliders to baseline, fires one final `onSliderChange({})`, and the sticky bar reverts.

## Required Invariants

1. **yaml chain order**: `{**generated, **registry, **per_concept_yaml}`. Per-concept always wins; registry beats auto-generated.
2. **Sticky bar reflects current overrides**: post-compute LCOE / Overnight values show in the sticky bar. Net Power and Capacity Factor are derived from the same compute response.
3. **Section collapse does not affect compute**: collapsing Sensitivity does NOT clear overrides. The sticky bar still shows the override-driven delta. Only Reset clears overrides.
4. **Reset is the single un-do**: clears overrides AND removes deltas in the sticky bar. Section collapse state is independent of Reset.
5. **Top-N is the single source of truth**: there is one filter that decides which parameters get rendered. No separate slider list.
6. **Tornado API stability**: `renderTornado(container, options)` keeps its current signature — `concept_page.js` callers shouldn't need to change beyond passing one extra option for slider control.
7. **Standalone concepts render**: if `sensitivities === null` or no model_setup, the page still loads. Sticky bar shows static headline (no deltas, no Reset). Sensitivity section shows the placeholder. Other sections collapse normally.

## Implementation Order

Each step is independently shippable and reviewable in the browser before moving on.

### Step 1 — Display registry (no UI yet)
- Create `exploration/concept_explorer/data/parameter_display_registry.yaml` with the starter ~15 entries above; expand by surveying tornado top-15 across concepts.
- Add a registry loader (similar to `load_parameter_metadata`) and merge it between `generate_parameter_metadata()` and per-concept yaml in `extract_costingfe()`.
- Re-extract all costingfe concepts.
- **Gate:** spot-check `data/01.json` shows `parameter_metadata.eta_th.display_name == "Thermal Efficiency"` and `display_unit == "%"`.

### Step 2 — Integrated tornado grid (replaces tornado.js + slider rendering)
- Rewrite `tornado.js` from Plotly to DOM. Match `mockup_v2.html` row layout. Wire `<input type=range>` per row.
- Preserve all "What Must Stay" capabilities (whiskers, click, color, opacity, hatching).
- Remove `renderSliders()` from `concept_page.js`; route `onSliderChange` to compute.
- Update tests in `tests/test_views_manual.py` if they target Plotly DOM (likely none).
- **Gate:** click a row's slider → LCOE updates; click a bar → parameter card opens; collapse-then-expand the section → state preserved.

### Step 3 — Sticky headline + Reset
- New `sticky_headline.js`. Render at the top of `concept-content` (or above it).
- Remove the `headline-section` div from the template. Its data flows into the sticky bar instead.
- Wire `concept_page.js` slider compute callback to `stickyHeadline.update(newHeadline)`.
- Reset button: disabled at baseline, enabled once any slider has moved; click → `tornado.reset()` + `stickyHeadline.update(baselineHeadline)`.
- **Gate:** drag → sticky updates with delta; Reset → sticky reverts and button disables.

### Step 4 — Collapsible sections
- Wrap Narrative, Risks, CAS, Sensitivity, Sources in a section component with chevron + body.
- Defaults per Decision C.
- Add the changed-count hint to the Sensitivity header (visible when collapsed).
- **Gate:** all sections collapse/expand; defaults match the matrix; changed-count appears when sliders are moved.

## Out of Scope (Phase 2)

- Animating sticky-bar value transitions on update.
- Keyboard shortcuts (`R` for reset, arrow keys to nudge sliders).
- Saving named scenarios. Per spec 12, deferred.
- Per-concept registry editing through the UI. Still yaml-authored.
- Comparison-view slider integration. Per spec 12, deferred.
- Re-implementing parameter card popover styling — the existing component continues to work as long as `onParameterClick` fires.

## Risks

**Risk: tornado refactor regresses Plotly behavior.** Hover tooltips, whiskers, click handlers, hatched fills all need parity. **Mitigation:** the "What Must Stay" list is the regression checklist. Step 2 has a manual gate before moving on.

**Risk: registry merge order bug shadows per-concept yaml.** A subtle merge implementation could let registry beat per-concept (wrong direction). **Mitigation:** Step 1 spot-check explicitly verifies a per-concept override still wins (write a test fixture with both layers).

**Risk: sticky bar overlaps content on narrow viewports.** The mockup uses `position: sticky` with `backdrop-filter: blur`. On older browsers or narrow viewports the readability could degrade. **Mitigation:** keep the sticky bar height tight; provide a non-blur fallback background. Verify on a 1024px-wide viewport.

**Risk: collapsed-by-default hides Risks from users who don't know to expand.** A user landing on the page may not realize Risks exist. **Mitigation:** the collapsed header preview shows risk count + severity, which is a sufficient teaser. Re-evaluate after a few users have clicked through.

**Risk: standalone concepts use the same template.** If we remove `headline-section` and the standalone path expects it, the page breaks. **Mitigation:** Standalone path needs explicit handling — sticky bar still renders (with static headline), but no sliders, no Reset. Test on at least one standalone concept (e.g., `02`).

## Validation Approach

1. **Unit / integration tests** (where existing): registry loader, merge order, post-compute headline propagation. Update `tests/test_extraction.py` if registry-loading is testable as a pure function.
2. **Manual browser verification** at each step's gate, using `browser-inspect` skill:
   - Concept 01 (costingfe with rich sensitivity): full flow — drag, sticky update, Reset, collapse all sections, expand Sensitivity, drag again.
   - Concept 19 (different costingfe concept): sanity check that registry covers its top-15.
   - Concept 02 or another standalone: page loads, sticky bar shows static headline, no slider section.
3. **No regressions**: `pytest exploration/concept_explorer/tests/` continues to pass.
4. **Console clean**: no errors on any of the three test concepts.

## Next-Stage Handoff

**Fixed (do not revisit in plan):**
- Step ordering: registry → grid → sticky → collapsibles.
- Tornado refactor target: native DOM, same public API.
- Layout reference: `mockup_v2.html`.
- Registry path: `exploration/concept_explorer/data/parameter_display_registry.yaml`.
- Defaults: Sensitivity expanded; Narrative / Risks / CAS / Sources collapsed.

**Open (plan should decide):**
- Whether `collapsible.js` becomes its own file or stays inline in `concept_page.js`.
- Final list of registry entries (driven by surveying tornado top-15 in all 19 costingfe concepts).
- Whether to keep the `text-muted` placeholder for standalone concepts inside the new tornado component or move it to `concept_page.js` gating.

**De-risk first:**
- Build the new tornado in a sandbox HTML page first (same approach as `mockup_v2.html`) to confirm the slider-inline-with-bar layout works at production data scale. The mockup already validates 15 rows; verify it's still readable when a concept has 47 sensitivity entries (only 15 render, but confirm filter respects that).

---

## Update: Tornado DOM Spike (2026-04-26)

A de-risking spike was performed to validate the Plotly → DOM migration in-place on the live concept explorer, before committing to the full implementation plan.

### Approach

Rewrote `tornado.js` from Plotly to pure DOM (HTML/CSS grid) while keeping the same `renderTornado(container, options)` public API. Tested on concept 01 (HTS Compact Tokamak) with the server running locally.

### Critical finding: Plotly bars were already broken

The existing Plotly implementation had a latent bug: **no bars rendered at all**. Only the population-range whisker trace was visible. Root cause: all parameters in the current data have `category: "unclassified"`, but `TORNADO_CATEGORY_ORDER` only listed the 5 named categories (`shared-baseline`, `well-established`, etc.). The `_buildBarTraces` loop iterated over `TORNADO_CATEGORY_ORDER` and skipped `unclassified`, producing zero bar traces. The chart appeared functional at a glance because the whiskers gave it visual content, but the primary data visualization (elasticity bars) was absent.

This significantly lowers the migration risk — we aren't replacing a working Plotly chart with an equivalent DOM chart; we're replacing a broken Plotly chart with a working DOM chart.

### Feature parity checklist

| # | Feature | Plotly (before) | DOM (after) | Notes |
|---|---------|----------------|-------------|-------|
| 1 | Top-N filter by \|elasticity\|, sorted descending | Working | Working | Same logic, no change |
| 2 | Per-bar category color encoding | **Broken** (no bars for `unclassified`) | Working | DOM version adds `unclassified` to category maps |
| 3 | Confidence opacity (high=1.0, medium=0.8, low=0.6) | N/A (bars absent) | Working | Added `unknown: 0.8` mapping for current data |
| 4 | Hatched fill for low-confidence bars | N/A (bars absent) | Working | CSS `repeating-linear-gradient` at 45° |
| 5 | Population-range whiskers | Working | Working | End caps + horizontal line, same visual weight |
| 6 | Click → `onParameterClick(paramName, meta)` | Working (via `plotly_click`) | Working (via row `click` listener) | Parameter card popover confirmed opening on click |
| 7 | Tooltip on hover | Working (Plotly hover template) | Working (native `title`) | Simpler but sufficient; custom tooltip possible later |
| 8 | Standalone-concept placeholder | Working | Working | Same markup |
| 9 | Responsive layout | Plotly `responsive: true` | CSS percentage widths | Needs viewport testing but fundamentally sound |

### What changed in the spike

- `tornado.js`: Full rewrite, ~270 lines (was ~410). No Plotly dependency.
- Added `"unclassified"` to `TORNADO_CATEGORY_COLORS`, `TORNADO_CATEGORY_LABELS`, `TORNADO_CATEGORY_ORDER`.
- Added `unknown: 0.8` to `TORNADO_CONFIDENCE_OPACITY`.
- Bar rendering: positioned absolutely within a relative container, `left` and `width` as percentages of `maxAbs` extent.
- Whiskers: positioned the same way, rendered as thin `div` elements with end caps.
- Legend: only shows categories actually present in the data + population range.

### What was NOT changed

- `concept_page.js` — zero changes needed. The public API (`renderTornado(container, options)`) is identical.
- `concept.html.j2` — no template changes.
- `explorer.css` — no CSS changes (all styles are inline in the generated DOM; design system variables not yet wired).
- `base.html.j2` — Plotly `<script>` tag still present (can be removed in the real implementation once comparison view is also migrated).

### Screenshots

Before/after screenshots taken via Playwright element capture of `#tornado-mount`:

- **Before**: Only whisker lines visible, no colored bars, sparse visual (Plotly bug).
- **After**: All 15 bars visible with correct direction (negative left, positive right), category dots, whiskers behind bars, elasticity values on right, legend at bottom.

### Risk assessment update

**Risk: tornado refactor regresses Plotly behavior** — **DOWNGRADED**. The Plotly chart was already non-functional for its primary purpose (bars). The DOM version is a strict improvement over current state. The "What Must Stay" checklist items 1–8 are all confirmed working in the spike.

**New risk identified: comparison view (`view_sensitivity.js`)** — imports `TORNADO_CATEGORY_COLORS`, `TORNADO_CATEGORY_LABELS`, `TORNADO_CATEGORY_ORDER` from `tornado.js` as globals. These constants are preserved in the DOM version, so the comparison view should continue to work. However, `view_sensitivity.js` may also call Plotly directly for its own grouped tornado rendering — this needs verification before removing the Plotly vendor file.

### Disposition

The spike confirms the DOM migration is safe and lower-risk than originally assessed. The spike code is intentionally rough (inline styles, no slider integration yet) — it validates the approach, not the final implementation. Recommend proceeding to `plan.md` with confidence.

---

Next Step: After approval → update `plan.md` for Phase 2 work items, then `/_my_implement`.
