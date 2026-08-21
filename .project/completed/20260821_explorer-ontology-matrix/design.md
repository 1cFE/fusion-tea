# Design: The Living Ontology Matrix (B1)

**Status:** Implemented (2026-06-07, branch `feat/explorer-ontology-matrix`)
**Owner:** Reid W
**Created:** 2026-06-07 10:02 PDT
**Complexity:** MEDIUM
**Branch:** feat/explorer-ontology-matrix (branch off `feat/explorer-identity-spine` — B1 consumes Theme A, not yet on `main`)
**Commit at design:** f1a430ad (`main`); Theme A spine lives on `feat/explorer-identity-spine`

## Overview

Replace the explorer's landing page with a dense, interactive **ontology matrix**: ~40 concepts as rows grouped under the family decision tree, the 8 ontology dimensions as color-chip columns, with click-to-filter, live re-group, sort-within-group, and hover-to-explain. The card grid moves to its own `/pipeline` page. The matrix is a **pure client-side projection** of three endpoints that already exist; it adds no server data and re-uses Theme A's shared authorities for color, identity, facets, and caveats.

## Related Artifacts

- **Spec:** `.project/active/explorer-ontology-matrix/spec.md`
- **Epic:** `.project/backlog/epic_explorer_ux_v3.md` — Theme B, B1 (lines 228–231); ontology-first reversal (line 204)
- **Theme A (the spine consumed):** `.project/active/explorer-identity-spine/{spec.md,design.md}` (on `feat/explorer-identity-spine`)
- **Research:** `.project/research/20260605-150329_concept-explorer-ux-user-journeys.md` — J1 orientation
- **Ontology image (made live):** `.project/research/concept_ontology_v3.png`

## Research Findings

**Theme A already shipped the matrix's vocabulary** (read from `feat/explorer-identity-spine`):

- `static/js/ontology_palette.js` exports three globals: `ontologyPalette` (family + per-dimension color maps, sourced from CSS `:root --onto-*` tokens), **`facetModel`** (10 facets, each `{key, label, field, values:[{value,label,color}]}`), and **`filterState`** (`create/toggle/isEmpty/matches`; AND across facets, OR within). The matrix's columns, cell colors, filter panel, and group-by options are *all derivable from `facetModel`* — it is effectively the column/facet spec already written.
- `static/js/concept_label.js` → `conceptLabel(payload)` → `{code, name, codeText, text, codeChip()}`. The identity-cell authority.
- `static/js/caveat_marker.js` → `caveatMarker({asterisk, fitGrade, missing})` → `{any, title, element(), html()}`. The hover/caveat authority, including the honest `missing` ("… not recorded") variant.

**Two data layers, joined by `concept_id` (this is the join the matrix owns):**

- `/api/manifest` → `ConceptManifestEntry` (`models.py:485`): `concept_id, name` (canonical, A1-stamped), `confinement_family, company, status, illustration, has_cost_model, has_sensitivities, lcoe_per_mwh, confidence, asterisk_in_comparison, fit_grade`. This is the **served set** (omit-list already applied server-side) — the row spine.
- `/api/taxonomy/registry` → `ConceptTaxonomy` (`taxonomy_models.py:202`): the **7 ontology dimensions** — `fuel, magnet_type, driver_type, energy_capture, blanket_config, operation_mode, repetition_rate` — plus `confinement_family` and the sub-family hierarchy. These live *only* on the registry, not the manifest.
- `/api/taxonomy/tree` → nested `{field, label, value, children[], concepts[]}`; leaves carry `concepts: [id,...]`. Already pruned by `prune_decision_tree` server-side (`taxonomy_models.py:363`). Multi-level (e.g. MFE → `mfe_topology` → `stellarator_type` → leaf).

The `facetModel` `field` names line up exactly with these payload attributes — so a flat per-row object `{...manifestEntry, ...registryFields}` lets `filterState.matches`, cell coloring, and grouping all read `row[facet.field]` uniformly.

**Existing render/route patterns to mirror** (all on the branch):

- Pages are Jinja2 templates rendered to `dist/` at startup (`server.py:_render_templates`), served by thin file routes; nav is centralized in `templates/base.html.j2` and highlighted via the `active_nav` context var (single touch-point). `index_page.js` is the canonical fetch→build-DOM→atomic-swap pattern (loading/error/content states; `el()` helper; `conceptLabel`/`caveatMarker` already wired into the cards).
- `tree_view.js` already walks the nested tree recursively (`countConcepts`, `buildBranch`) — the traversal needed to turn the tree into ordered bands.
- `test_server.py` asserts `/` returns 200 with body containing "index" via a `client_with_pages` fixture that writes `dist/index.html`. Relocating the grid must keep `/` 200 and add coverage for `/pipeline`.

## Core Concept

The matrix is **one in-memory table projected through a pure pipeline**. On load we fetch the three endpoints **once**, left-join them by `concept_id` into a flat `rows[]` array (manifest entry is the spine; registry fields merged in). All four interactions are then pure transforms over that array plus a small `viewState` — no refetch, ever:

```
rows[] ──filter(filterState)──▶ group(groupBy)──▶ sort(sortKey,dir) within band ──▶ bands[] ──render──▶ DOM
```

The key insight is that **Theme A's `facetModel` already _is_ the matrix specification**: the columns are the 8 dimension facets, each cell's color/label is `facet.values.find(v => v.value === row[facet.field])`, the filter panel is one toggle group per facet, the group-by menu is "tree" + the dimension facets, and filtering is literally `filterState.matches`. So B1 writes almost no new domain logic — it writes a *renderer over facetModel* and a *projection function*, and wires events that mutate `viewState` and re-run the pipeline. That is what "B1 is mostly UI wiring" means, made concrete: identity, color, facet membership, and caveats are all imported, not re-derived.

## Key Bets & Decisions

### Decision 1 — Data join: client-side merge *(recommended; low controversy)*

**Options.** (A) Client-side merge: fetch manifest + registry + tree, join in JS. (B) New thin server endpoint `/api/matrix` returning pre-joined rows.

**Recommendation: A (client merge).** The spec lists "New server endpoints" as explicitly out of scope, and all three endpoints already exist and are already consumed elsewhere. Three parallel GETs once on load, joined by `concept_id`, keeps the server untouched and the join logic unit-testable as a pure JS function. (B) would centralize the join but spend server surface the spec told us not to spend, for no payoff at this data size (~40 rows).

### Decision 2 — Tree grouping: flat path-labeled bands *(needs your call)*

The decision tree is multi-level; the matrix needs group **bands**. The flat dimension re-groupings (fuel, magnet, …) are naturally single-level. We need one band model that serves both.

- **Option A — Flat path-labeled bands (recommended).** Walk the tree to its leaves (reusing `tree_view.js`'s traversal); each leaf becomes one band whose label shows its path (e.g. `MFE › Stellarator › Modular`) and whose header color is the top-level family. Bands are ordered by tree traversal. Dimension re-groupings produce the same shape: one band per category value. **One band renderer, one collapse behavior, uniform across all groupings.** Loses live *nested* expand/collapse of intermediate tree levels.
- **Option B — Nested collapsible bands.** Mirror `tree_view.js` exactly: recursive, intermediate family/topology levels each collapsible. More faithful to the tree, but introduces a second, recursive band model that the flat dimension groupings can't share, and complicates filter/sort interaction with nesting.

**Recommendation: A.** The matrix's job is orientation across the whole field, not tree navigation (that's what `/taxonomy` is for). Flat path-labeled bands keep the hierarchy *legible* (the path label) while keeping a single, simple band abstraction that every grouping reuses. Confirm before I commit — it's the one genuinely user-visible structural choice.

### Decision 3 — Non-dimension facets are filter-only *(recommended)*

`facetModel` has two non-dimension facets: `fitGrade` and `hasCostModel`. **Recommendation: neither is a matrix column.** The 8 columns are exactly the 8 ontology dimensions (matches the v3 PNG and keeps FR-B1.9's economics-out rule clean — `has_cost_model` is cost-adjacent and belongs nowhere near the columns). Both remain available as **filter-only** groups in the filter panel, and `fit_grade`/`asterisk` continue to surface on the identity cell through `caveatMarker` (exactly as the cards do today). This is the spec's stated "design call."

### Bet 4 — Single source of truth, imported not rebuilt

Every color comes from `ontologyPalette`; every name/code from `conceptLabel`; every caveat/hover from `caveatMarker`; every filter decision from `filterState`; the column/facet/group-by/cell-label vocabulary from `facetModel`. The matrix introduces **zero** new color hexes, name formatting, caveat strings, or facet definitions. This is the whole point of building the spine first, and it's an enforceable invariant (grep guard).

### Decision 5 — Relocated grid route = `/pipeline` *(recommended, trivially changeable)*

The card grid moves to `/pipeline` (nav label "Pipeline"), since it shows the Approved/In-Progress *pipeline* status. The matrix takes `/`. (Spec floated `/approvals`; either is fine — one string.)

## Architecture

**Client (new):** two JS modules plus one template.

```
matrix.html.j2 ── renders ──▶ dist/matrix.html  (served at /)
  loads: concept_label.js, caveat_marker.js, ontology_palette.js,  ← Theme A authorities
         matrix_data.js, matrix_page.js                            ← new

matrix_data.js (pure, no DOM, unit-testable):
  joinConcepts(manifest, registry, tree) ─▶ rows[]   (flat: manifest ∪ registry fields, by id)
  facetValuesFor(row)                    ─▶ {facetKey: value}   (for filterState.matches)
  project(rows, viewState)               ─▶ bands[]  (filter ▶ group ▶ sort-in-band)
  GROUP_OPTIONS  = ["tree"] + 8 dimension facet keys (+ flat "family")

matrix_page.js (DOM + events):
  init(): Promise.all(3 fetches) → rows = joinConcepts(...) → render(project(rows, viewState))
  viewState = { groupBy:"tree", sortKey:"code", sortDir:"asc", filter: filterState.create() }
  renders: controls bar (group-by select, sort control), filter panel + active-filter chips,
           the matrix <table> (sticky thead + sticky identity col), collapsible band rows
  every interaction: mutate viewState → re-render from the SAME rows[] (no refetch)
```

**Server (minimal, on the branch's patterns):**

```
_render_templates:  + matrix.html.j2 → dist/matrix.html (active_nav="matrix")
                      index.html.j2  → dist/index.html  (active_nav="pipeline")  [grid, relocated]
routes:             /          → serve dist/matrix.html   (repointed)
                    /pipeline  → serve dist/index.html    (new)
base.html.j2 nav:   add "Pipeline" link; home link → matrix; active_nav values updated
```

No new API endpoints, no model changes, no extraction, no data-file changes.

**Data flow per interaction (all client-side):** click chip → `filterState.toggle` → `project` → re-render; change group-by → set `viewState.groupBy` → `project` → re-render; click column header → set `sortKey/Dir` → `project` → re-render. `rows[]` is fetched once and never re-fetched.

## Required Invariants

- **One fetch.** Exactly three GETs (manifest, registry, tree) on load; zero network on filter/regroup/sort (verifiable in the network panel — an acceptance criterion).
- **No silent drop.** Every served (manifest) concept appears in exactly one band under every grouping. When grouping by a dimension, a row whose value is absent / `N/A*` / `TBD` / `Unknown` lands in the explicit `"— unspecified"` band (FR-B1.5). A concept absent from every tree leaf lands in an `"— ungrouped"` band under tree grouping (pruning/orphan safety).
- **No blank cell.** Every cell renders either a palette chip (recorded value, including grey `N/A`/`TBD` chips) or an explicit "not recorded" chip; never empty (FR-B1.8).
- **Imported authorities only.** No color hex, name format, caveat string, or facet list is authored in the matrix code. (Grep guard: no `--onto-`/hex literals and no `.name`-direct label render in `matrix_*.js`.)
- **No economics.** No LCOE/cost/`has_cost_model` column, group key, sort key, or color key on the matrix (FR-B1.9).
- **Served-set spine.** Rows derive from the manifest (the omit-list-applied served set); the pruned tree is used for tree grouping.

## Component Overview

- **`matrix.html.j2`** (new template) — controls bar, filter panel, active-filter bar, `<table>` skeleton, loading/error/content states; script includes (Theme A authorities + the two new modules). Mirrors `index.html.j2`'s state-swap structure.
- **`matrix_data.js`** (new, pure) — `joinConcepts`, `facetValuesFor`, `project` (filter→group→sort), `GROUP_OPTIONS`. No DOM; the testable core.
- **`matrix_page.js`** (new, DOM+events) — fetch/init, `viewState`, table + band + chip rendering via `el()`, control/filter/sort event wiring. The only place DOM is touched.
- **`server.py`** (edit) — `_render_templates` renders matrix.html; repoint `/`, add `/pipeline`.
- **`templates/base.html.j2`** (edit) — nav link + `active_nav` for the relocated grid and the matrix home.
- **`templates/index.html.j2`** (edit) — `active_nav` only (content unchanged; it *is* the relocated grid). `index_page.js` unchanged.

## Non-Goals

- B2 (parcats "flows" lens), B3 (economics ride-along columns / LCOE sort/color), C1/C2 (constellation, comparison entry), Theme D (provenance depth). Design leaves clean hooks: a second view-toggle slot in the controls bar (B2), and `project`/column-list extension points that B3 would add a column to — but B1 implements none.
- Free-text search (research idea 5) — possible fast-follow; not in B1.
- Multi-valued cells — none of the 8 chosen columns is multi-valued (`heating_type`, the only `+`-joined field, is deliberately not a column); deferred with the column that would require it.
- Virtualization — ~40×8 ≈ 320 cells renders instantly; not needed.

## Implementation Notes

- **Flat-row join key.** Build each row as `{...manifestEntry, fuel, magnet_type, driver_type, energy_capture, blanket_config, operation_mode, repetition_rate}` from the registry by `concept_id`. `confinement_family` exists on both — they agree (registry is identity source); prefer manifest's. A manifest concept missing from the registry → ontology fields `undefined` → cells render "not recorded" honestly.
- **`facetValuesFor` coercion.** `filterState.matches` compares `sel.has(facetValues[key])`. `has_cost_model` is boolean but its facet values are strings `"true"/"false"` — coerce with `String(...)`. Absent ontology fields → `undefined` (won't match any selected chip; correct).
- **Cell render.** `const v = row[facet.field]; const hit = facet.values.find(o => o.value === v);` → if `hit`: chip `background: hit.color`, label `hit.label`, hover = label + value caveat. If `v != null` but no `hit` (unexpected enum): grey `--onto-na` chip + raw `v` + caveat. If `v == null`: "not recorded" chip via `caveatMarker({missing: facet.label})`.
- **Grouping vs. cell treatment of `N/A`/`TBD`.** As a *cell*, `N/A`/`TBD`/`Unknown` are honest recorded values → their own grey chips. As a *grouping key*, they fold into the `"— unspecified"` band per FR-B1.5 (one helper `isUnspecifiedGroupValue(v)` covers `null`, `N/A*`, `TBD`, `Unknown`). Keep these two behaviors distinct — easy to conflate.
- **Tree → bands.** Reuse `tree_view.js`'s recursion shape to emit ordered `{label: path, family, conceptIds}` leaf bands; do not import the renderer (it builds tree DOM, not table bands).
- **Sort model.** `sortKey ∈ {code, name, <dimension facet key>}`, `sortDir ∈ {asc,desc}`; applied *within* each band (bands themselves are ordered by the grouping). Dimension sort orders by the facet's declared `values[]` order (the palette/category order), `undefined` last. Sort state persists across regroupings (it's orthogonal to `groupBy`). Default `code asc`.
- **Sticky layout.** Real `<table>`; `thead th { position: sticky; top: 0 }` and identity `th { position: sticky; left: 0 }`. Band header = a full-width `<tr>` with a toggle that hides its band's rows (CSS class, like `tree-node__children--open`). New CSS lives in `explorer.css` using existing tokens.
- **Group-by enumeration.** `GROUP_OPTIONS` = `"tree"` (default) + the 8 dimension facet keys, derived from `facetModel` by key (so adding a facet upstream surfaces here for free). The flat `family` facet may appear as a distinct "Family (flat)" option (spec edge case) — include it; it's free from `facetModel`.

## Potential Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Theme A not yet merged to `main`; B1 branches off it | Med | Branch B1 from `feat/explorer-identity-spine`; note the dependency; do not target `main` until A lands. |
| Registry/manifest served sets diverge (omit-list timing) | Low | Manifest is the row spine; missing registry rows degrade to "not recorded" cells, never crash. |
| Concept in manifest but in no tree leaf → orphan under tree grouping | Med | Explicit `"— ungrouped"` band; covered by the no-silent-drop invariant + a test. |
| Density/readability at ~40×8 chips | Low | Sticky headers, collapsible bands, compact chip styling; data size needs no virtualization. |
| "Just add an LCOE column" creep | Med | FR-B1.9 invariant + grep guard; B3 hook is documented but unimplemented. |
| Relocating `/` breaks the `test_server` index assertion | Low | Keep `/` → 200; update the fixture to render both `matrix.html` and `index.html`; add `/pipeline` test. |

## Integration Strategy

**Replaces:** the Approved/In-Progress split as the home page (the grid is preserved verbatim at `/pipeline`; `index_page.js` is untouched). **Complements:** `/taxonomy` (per-concept tree/constellation) and `/compare` — the matrix is the field-level entry that those drill *from*. **Consumes:** all five Theme A authorities directly. **Sets up:** B2 (view-toggle slot), B3 (column/sort extension point), C1/C2 (shared facet/filter state could later sync to the constellation).

## Validation Approach

- **Unit (pure JS in `matrix_data.js`):** `joinConcepts` (normal, missing-registry, suffix-variant 17a/20a); `project` (filter AND/OR semantics via `filterState`; group-by tree + a dimension; unspecified band collects `null`/`N/A`/`TBD`; sort within band; orphan → ungrouped band).
- **Server (pytest, mirror `test_server.py`):** `/` returns 200 (matrix); `/pipeline` returns 200 (grid); existing suite green.
- **Browser-inspect (acceptance):** load `/` — whole field grouped by family, chips colored; pick 01 / 24 / 17a spanning families → correct identity + cells; re-group by fuel → unspecified band present; single- and two-dimension filters narrow correctly + clear; sort within a group; hover shows value + caveat; an `N/A`/`TBD`/absent cell shows an explicit state; **network panel shows no refetch** on interactions; console clean; `/pipeline` reachable from nav.

## Next-Stage Handoff

**Fixed:** matrix at `/`, grid at `/pipeline`; client-side join of the three existing endpoints; columns = the 8 ontology dimensions; non-dimension facets are filter-only; all color/identity/caveat/facet/filter logic imported from Theme A; honest degradation + explicit unspecified/ungrouped bands; no economics; one fetch / client-only interactions; branch off `feat/explorer-identity-spine`.

**Settled (2026-06-07):** Decision 2 = **A, flat path-labeled bands** (one band model shared by tree + dimension groupings; path label keeps the hierarchy legible). Decision 5 = **`/pipeline`** (nav label "Pipeline").

**De-risk first:** the `project()` pure pipeline + `joinConcepts` (the heart of the feature) — write and unit-test these before any DOM, since every interaction and every invariant rides on them.

## Appendix — Field/Facet Join Map

| facet `key` | `label` | payload `field` | source layer | column? | group-by? |
|---|---|---|---|---|---|
| family | Confinement Family | `confinement_family` | manifest+registry | ✅ | ✅ (+ tree default) |
| fuel | Fuel | `fuel` | registry | ✅ | ✅ |
| magnet | Magnet | `magnet_type` | registry | ✅ | ✅ |
| driver | Driver | `driver_type` | registry | ✅ | ✅ |
| capture | Energy Capture | `energy_capture` | registry | ✅ | ✅ |
| blanket | Blanket | `blanket_config` | registry | ✅ | ✅ |
| opMode | Operation Mode | `operation_mode` | registry | ✅ | ✅ |
| repRate | Repetition Rate | `repetition_rate` | registry | ✅ | ✅ |
| fitGrade | Archetype Fit | `fit_grade` | manifest | ❌ filter-only | ❌ |
| hasCostModel | Cost Model | `has_cost_model` | manifest | ❌ filter-only | ❌ |

Honest-state taxonomy per cell: **recorded value** → palette chip (incl. grey `N/A`/`TBD`/`Unknown` chips); **unexpected enum** → grey `--onto-na` chip + raw value + caveat; **absent (`null`)** → "not recorded" chip via `caveatMarker({missing})`. Grouping folds `{null, N/A*, TBD, Unknown}` into `"— unspecified"`.

---
Next Step: After you confirm Decisions 2 and 5 → `/_my_plan`.
