# Design: Cost Landscape Page (Theme F)

**Status:** Draft
**Owner:** Reid W
**Created:** 2026-06-07 13:28 PDT
**Branch:** `feat/explorer-cost-landscape` (off `feat/explorer-ontology-matrix` / PR #59)

## Overview

A new explorer page that renders every costed concept as a stacked bar — height = headline LCOE, segments = the annualized cost components (Capital / Fixed-O&M / Replacement / Fuel) that sum to it — with live re-grouping by ontology facet and a fixed cheapest-first sort within each group.

## Related Artifacts

- **Spec:** `.project/active/explorer-cost-landscape/spec.md`
- **Research:** `.project/research/20260605-150329_concept-explorer-ux-user-journeys.md`
- **Epic:** `.project/backlog/epic_explorer_ux_v3.md` (Theme F)
- **Reuse:** `explorer-identity-spine` (A1/A2/A3), `explorer-ontology-matrix` (B1 grouping), `explorer-override-inspection` (Item 2 records/panel)

## Research Findings

**Page build/serve** (FastAPI + Jinja → static `dist/`): a page = a `templates/*.html.j2` + a render call in `_render_templates()` (`server.py:520`) + a `FileResponse` route in `create_app()` (`server.py:~887`) + a nav `<a>` in `base.html.j2:13-37` keyed on `active_nav`. The matrix page is the exact template to mirror (`matrix_page()` `server.py:704`).

**Grouping is already solved by B1 and reusable.** `matrix_data.js` is a pure data core: `joinConcepts(manifest, registry)` (`:47`) → flat rows with ontology facets; `project(rows, viewState, tree)` (`:314`) filters → groups (`groupByTree` `:140` / `groupByDimension` `:210`) → sorts (`makeComparator` `:256`). `GROUP_OPTIONS` (`:337`) is the facet dropdown source. The Cost landscape needs the *same* rows + grouping; only the cell render differs (a bar, not a matrix row).

**Theme A authorities** (drop-in): `conceptLabel(c)` → `{code, codeText, text, codeChip()}` (`concept_label.js:35`); `caveatMarker({asterisk, fitGrade, missing})` → `{any, title, html()}` (`caveat_marker.js:49`); `ontologyPalette` + `facetModel` (10 facets incl. family/fuel/driver/capture/opMode) + `filterState`, all reading `:root` tokens (`ontology_palette.js`). Colors MUST trace to `:root`; no hex in JS (A2 invariant).

**Plotly** is vendored (`static/vendor/plotly-basic.min.js`, loaded in `base.html.j2:9`). `view_capex.js:195-355` is the reference bar pattern: traces with `customdata` (stable codes, not display strings), `hovertemplate: "%{hovertext}<extra></extra>"` + `hovertext[]`, `plotly_click` → `curveNumber`/`customdata` lookup, theme constants `PLOTLY_THEME` (`view_capex.js:44`).

**Cost data is NOT in the lightweight manifest.** `ConceptManifestEntry` (`models.py:477`) carries `lcoe_per_mwh`, `has_cost_model`, `asterisk_in_comparison`, `fit_grade`, `confinement_family` — but not the cas components or overrides. Those live in full `ConceptData` / `CostModelData` (`models.py:128`), held in server memory (`state.concepts`). The decomposition components `cas90`/`cas80` are emitted today; `cas71`/`cas72` are NOT (only combined `cas70`) — the one extractor gap (FR-F11). The freeform pathway already emits cas71/72 (`extract_explorer_data.py:511-512`); the costingfe pathway (`from_forward_result` `models.py:210`) must add them.

## Core Concept

**The Cost landscape is the matrix's data spine with a different cell.** It reuses B1's exact rows-and-grouping machinery (concepts joined to ontology facets, grouped by family-tree or any facet, filtered by the shared filter state) and swaps the per-concept *matrix row* for a per-concept *stacked bar* whose height is the headline LCOE and whose segments are the four annualized cost components that provably sum to it. One server-side aggregate (`/api/cost-landscape`) supplies the decomposition + a compact override narrative per concept; everything else — identity, color, caveat, grouping, sort — is existing authority. The page adds **no new vocabulary and no new grouping logic**; it adds a bar renderer and a thin cost aggregate. The insight that makes it honest: only the *annualized* components (CAS90/71/72/80, in $/MWh) are additive to LCOE, so the bar stacks those and nothing else — CapEx-by-account (M$) is a different unit and stays off this axis.

## Key Bets

- **B1.** The four annualized components decompose LCOE *exactly* (component $/MWh = component-share-of-annualized × LCOE). *If false → the stacked bar's segments don't sum to the headline and the whole chart is a lie.* (Verified against 01/05/24 in spec Appendix A — this is arithmetic from `economics.py:78`, low risk.)
- **B2.** B1's `matrix_data.js` rows/grouping can be reused for a non-matrix surface without forking. *If false → we duplicate grouping logic and the "set a grouping once, it means the same everywhere" promise breaks.*
- **B3.** Per-segment override depth is better served by a summary-on-hover + deep-link-to-concept-page than by cramming rationale into a Plotly tooltip. *If false → users can't get the "why" without leaving the page and the J3 provenance journey stalls here.* (This is the hover-depth decision below.)

## Key Decisions

- **D1. Data delivery = one new server aggregate `/api/cost-landscape`, joined client-side to matrix-style rows.** The page fetches `manifest` + `registry` + `tree` (reusing `matrix_data.joinConcepts`/`groupByTree` verbatim for rows, facets, caveat, family grouping) **plus** `/api/cost-landscape` for the cost decomposition and compact overrides, joined by `concept_id`. *Rejected: per-concept `/api/concepts/{id}` fan-out (~17 fetches + client-side account→component roll-up duplicated in JS); rejected: bloating the lightweight manifest with components + override records (it has other consumers — entry grid, compare picker).* The aggregate is built from in-memory `ConceptData`, so the roll-up (account→component) lives server-side, in one tested place.
- **D2. Decompose shares in JS, not the extractor.** The extractor emits raw `cas71/72` (+ existing 90/80); the page computes `$/MWh = casX/(cas70+cas80+cas90) × lcoe`. *Rejected: precomputing component $/MWh in the extractor (couples the extractor to a presentation form; the raw components are more reusable and the math is trivial).*
- **D3. Color = four new `:root` cost-component tokens read via `ontologyPalette`'s `tok()` pattern.** *Rejected: reusing `cas_breakdown.js` `CAS_COLORS` (those are per-CAS-account, 16 colors, wrong granularity) or hard-coding hex (violates the A2 single-color-authority invariant).*
- **D4. Vertical bars, concepts on x (per spec); grouping bands along x; fixed LCOE-ascending sort within band.** Reuses `makeComparator` with a fixed `sortKey=lcoe`.
- **D5. Outlier axis = focused linear range with annotated overflow** (settled 2026-06-07). Exclude non-finite/freeform pathological LCOE (e.g. 03) from the chart entirely (counted in the "N excluded" note); **linear** axis (log breaks additive stacking); default y-range focused on the readable majority (~0 to a percentile cap, ~400 $/MWh); bars exceeding the range are drawn to the cap with an explicit **"↑ <true LCOE>" annotation + caveat marker** and remain reachable via Plotly zoom. *Rejected: log scale (non-additive stacking); hard-excluding legitimate high concepts (16/23/36 are real data, not errors); broken-axis two-panel (more complexity than the payoff).*
- **D6. Hover depth = summary + deep-link** (settled 2026-06-07). Segment hover shows component, $/MWh, %, and an override summary ("★N adjustments · source label"); the **bar click navigates to the concept page** where Item 2's full override panel carries the multi-paragraph rationale. *Rejected: full/truncated rationale in the Plotly tooltip (rationales are multi-paragraph; a tooltip can't hold them and truncation misleads).*
- **D7. Commit the Taxonomy → "Design Space Viz" rename in this item** (settled 2026-06-07). The nav label ships as "Design Space Viz" here; Theme C1's deeper page refocus inherits it.

## Architecture

```
Build time:  extract_explorer_data.py → data/NN.json   (adds cas71, cas72)
Server:      state.concepts (ConceptData) ──> build_cost_landscape() ──> GET /api/cost-landscape
                                          └─> build_manifest()       ──> GET /api/manifest
             taxonomy ──> GET /api/taxonomy/{registry,tree}
Page load:   cost_landscape_page.js
               fetch manifest + registry + tree  ──> matrixData.joinConcepts → rows (facets, caveat, family)
               fetch /api/cost-landscape          ──> costByConcept{ id → {lcoe, components, overrides} }
               join by concept_id → costRows (only has_cost_model & finite LCOE)
Re-render:   applyView()  (no refetch)
               matrixData.project(costRows, viewState, tree) → bands   [reused grouping/sort/filter]
               renderLandscape(bands) → Plotly stacked bars
                 trace per component (4 traces, barmode:"stack")
                 x = ordered concept codes within bands; customdata = concept_id
                 hovertext = component $/MWh + % + override summary
               plotly_click → navigate to /concept/{id}
```

**Boundaries:** `matrix_data.js` stays the grouping authority (unchanged, reused). New `cost_landscape_page.js` owns only fetch-join-render-and-controls. New `build_cost_landscape()` (server) owns the decomposition-source + account→component roll-up. Controls bar (group-by dropdown + filter chips) mirrors `buildControls()` (`matrix_page.js:225`) — ideally factored to a shared helper, but duplicating the small dropdown is acceptable if sharing risks B1.

## Required Invariants

- **I1.** For every rendered bar, `sum(segment $/MWh) == headline LCOE` within float tolerance (B1; a test asserts this).
- **I2.** Every color resolves through `ontologyPalette`/`:root` tokens — no hex literal in `cost_landscape_page.js` (A2).
- **I3.** Re-grouping and filtering never refetch (NFR-1): all data is in memory after load; `project()` is pure.
- **I4.** The bar stacks only annualized $/MWh components; no M$ / capital-by-account value appears on this axis.
- **I5.** Only concepts with `has_cost_model` and a finite, in-range LCOE render; excluded concepts are accounted for honestly (a visible "N excluded: …" note), never silently dropped (FR-F10).
- **I6.** Account→component roll-up is total: every override account maps to exactly one of {capital, fixed_om, replacement, fuel} (capital = CAS10-60 incl. all CAS22 sub-accounts; fixed_om = cas71; replacement = cas72; fuel = cas80).

## Component Overview

- **`build_cost_landscape(concepts)`** (server.py, new) — returns `CostLandscape` (new model): per costed concept `{concept_id, lcoe, components{capital,fixed_om,replacement,fuel}, overrides:[{account, component, source, rationale_short, enabled, blocked_by}]}`. Pure function of in-memory `ConceptData`.
- **`/api/cost-landscape`** (server.py, new route) — serves the above, like `api_get_manifest` (`server.py:582`).
- **`CostModelData` cas71/cas72** (models.py:128) — two new `CASAccount` fields + `CAS_NAMES` entries; `from_forward_result` (`:210`) builds them via the existing `_cas()` helper.
- **`cost_landscape_page.js`** (new) — fetch/join/render/controls; the only new front-end module of size.
- **`templates/cost_landscape.html.j2`** (new) — extends `base.html.j2`; controls bar + `<div>` chart mount; loads Theme-A scripts + matrix_data.js + Plotly + the new page script.
- **`base.html.j2` nav** (edit) — reorder to All Concepts · Design Space Viz · Compare · Cost landscape; add the 4th link; relabel Taxonomy.
- **CSS** — 4 `--cost-*` tokens in `:root`; a `.cost-landscape` layout block in `explorer.css`.

## Non-Goals

- Metric toggle (CapEx-by-account / OpEx-only / Production), the availability scatter, bare/applied toggle, registry editing, C2 comparables, constellation refocus (C1). Per spec.
- Sharing/refactoring `buildControls()` into a formal shared component if it risks B1 — duplicate the small dropdown instead.

## Implementation Notes

- **Override→component map** (server side, I6): account prefix `cas1*/cas2*/cas3*/cas4*/cas5*/cas6*` or `C22*` → `capital`; `cas71` → `fixed_om`; `cas72` → `replacement`; `cas80` → `fuel`. Most registry overrides are capital (magnets, vessel).
- **rationale_short**: first sentence or cost_basis+provenance line; full rationale stays on the concept page (Item 2 panel). Honest-degradation: missing source/rationale → "not recorded" (reuse Item 2's wording).
- **Stacked-bar order**: Plotly `barmode:"stack"`; one trace per component (stable legend + color); within-band x-order from `makeComparator(lcoe, asc)`; band separation via x categorical gaps or annotations (see `groupByTree` band labels).
- **cas71/72 absent** (37, 39 — Item 2-FU): render combined O&M as a single "O&M" segment for that concept with a caveat, rather than fabricating a split.
- **Caveat marker on x-tick**: Plotly tick labels are plain text; render the `#code` + `⚠` as the tick (HTML not supported in tick labels → use annotations or a custom tick layer, or place the marker in hover + a colored tick). Resolve in plan.
- The extractor change must be followed by a **re-extract** of served concepts (coordinate with the active 1 GWe override-policy churn to avoid stacking stale outputs — spec watch-out).

## Potential Risks

- **LCOE outliers crush the axis (primary risk).** 03 = 37,452 (freeform/pathological), 16 = 2068, 23 = 793, 36 = 904, 29 = 496 vs a ~40–360 majority. On a naive linear axis the median concept's stack is an unreadable sliver. Mitigation = D5 (exclude pathological, focus the default range, annotate over-range bars with true value). **This is the user checkpoint.**
- **Tick-label caveat marker** (Plotly limitation) — may need an annotation layer; scoped to plan.
- **Grouping-control duplication drift** vs the matrix — mitigate by factoring a shared `buildGroupControls()` if low-risk, else accept a small duplicate and note it.
- **Stale/missing data inheritance** — page shows stored headlines (FU2 24-staleness class); tie missing/suspect values to the caveat marker, don't paper over.

## Integration Strategy

Additive: a new page + route + nav entry + one new endpoint + two new schema fields. Touches `base.html.j2` nav (shared) and `models.py`/`extract_explorer_data.py` (the cas71/72 add, which the freeform path already expects). Reuses `matrix_data.js`, Theme A authorities, Plotly pattern, and the Item 2 override semantics wholesale. No change to existing pages beyond the nav reorder.

## Validation Approach

- **Unit/data**: a test that for ≥3 concepts (01, 24, 23) the four emitted components sum to the stored headline LCOE within tolerance (I1); `cas71`/`cas72` present in re-extracted JSON (FR-F11); roll-up totality (I6).
- **Browser** (`browser-inspect`): page renders all costed concepts; re-group by each of the 6 options re-lays with no network call (I3); within-group cheapest-first; pulsed concept (17a/17b) shows Replacement+Fuel a tokamak (01) lacks; segment hover shows $/MWh+%+override summary; bar click → correct concept page; an excluded concept appears in the "N excluded" note (I5); console clean.
- **Regression**: existing test suite passes; nav reorder doesn't break other pages' `active_nav`.

## Next-Stage Handoff

**Fixed for the plan:** reuse `matrix_data.js` for rows/grouping/sort/filter; new `/api/cost-landscape` + `build_cost_landscape()`; cas71/72 schema add + re-extract; 4 `:root` cost tokens; vertical stacked Plotly bars; nav reorder + rename; decompose-in-JS.

**Open (pending user, this turn):** none — D5 (focused linear axis + annotated overflow), D6 (summary hover + deep-link), and D7 ("Design Space Viz" rename) all settled 2026-06-07.

**De-risk first in implementation:** the extractor cas71/72 add + re-extract + the I1 sum-to-LCOE test — everything downstream assumes the components exist and are exact. Then the server aggregate, then the page.

## Appendix — File inventory & decomposition reference

**New:** `templates/cost_landscape.html.j2`, `static/js/cost_landscape_page.js`, `build_cost_landscape()` + `/api/cost-landscape` + `CostLandscape` model, 4 `:root` `--cost-*` tokens + `.cost-landscape` CSS, a data/sum test.
**Edit:** `base.html.j2` (nav), `models.py` (`CostModelData.cas71/cas72`, `CAS_NAMES`, `from_forward_result`), `extract_explorer_data.py` (ensure cas71/72 on costingfe path), `server.py` (render call + route).

**Decomposition (from `1costingfe/.../economics.py:78`):** `LCOE = (CAS90+CAS70+CAS80)×1e6 / (8760·p_net·n_mod·avail)`, `CAS70=CAS71+CAS72`. Component $/MWh = `casX/(CAS70+CAS80+CAS90) × LCOE`. Served today: `headline.lcoe_per_mwh`, `cas90`, `cas80`, combined `cas70`; **missing: `cas71`, `cas72`**. See spec Appendix A (worked 01 check) and Appendix B (why availability isn't an axis).

---
**Next Step:** After approval → `/_my_plan`.
