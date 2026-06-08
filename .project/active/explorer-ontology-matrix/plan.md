# Implementation Plan: The Living Ontology Matrix (B1)

**Status:** Complete (Phases 1–4 done)
**Created:** 2026-06-07
**Last Updated:** 2026-06-07

## Source Documents
- **Spec:** `.project/active/explorer-ontology-matrix/spec.md`
- **Design:** `.project/active/explorer-ontology-matrix/design.md` ← component details, architecture, invariants, gotchas, field/facet join map
- **Branch:** cut `feat/explorer-ontology-matrix` from `feat/explorer-identity-spine` (Theme A is not on `main` yet)

## Implementation Strategy

**Phasing Rationale:** Clear the highest-coupling risk first (the page swap + the `test_server` index assertion), which also yields a running page that loads the new modules — the substrate every later phase needs. Then build the read-only heart (`matrix_data.js` + static render) before any interaction, so correctness of the join/grouping/cells is proven before filter/sort logic rides on top. Interactions split into filter+regroup (Phase 3) and sort+hover+polish (Phase 4) to keep each phase one-session sized.

**Critical Path:** scaffold/relocate (P1) → data core + static render (P2) → filter + regroup (P3) → sort + hover + density (P4).

**First Proof Point:** P1 — `/` renders the matrix shell, `/pipeline` preserves the grid, and the client join yields exactly one row per served concept with a clean console.

**Overall Validation Approach** (project pattern — there is **no JS unit runner**; see `test_identity_frontend.py`):
- **pytest grep-guards** (static, write-first) — structural invariants: matrix modules import the 5 Theme A authorities; no `--onto-`/hex literals; no LCOE/cost column.
- **pytest server tests** — routing (`/`→matrix, `/pipeline`→grid) + full-suite regression.
- **browser-inspect** (`scripts/browser_inspect.py`, see `.claude/skills/browser-inspect/SKILL.md`) — behavioral acceptance incl. `--eval` against the live `project()`, and the no-refetch network check.

---

## Phase 1: Scaffold + Relocate the Grid

### Goal
`/` serves the matrix page shell; the existing Approved/In-Progress card grid is preserved verbatim at `/pipeline`; nav updated. `matrix_page.js` fetches the three endpoints and joins them into `rows[]` (logged, not yet rendered). See `design.md#architecture` (server + client blocks).

### Assumption Under Test
The three existing endpoints join cleanly by `concept_id` into one row per served concept, and repointing `/` does not break routing or the existing grid.

### Test Stencil (Write This First)
```python
# tests/test_server.py — extend
def test_matrix_is_home(client_with_pages):
    resp = client_with_pages.get("/")
    assert resp.status_code == 200
    assert "matrix" in resp.text  # dist/matrix.html served at /

def test_pipeline_serves_grid(client_with_pages):
    resp = client_with_pages.get("/pipeline")
    assert resp.status_code == 200  # relocated card grid (dist/index.html)
```

### Changes Required

**See `design.md` for:** server block + nav touch-point → `design.md#architecture`; route/name decision → `design.md#key-bets--decisions` (Decision 5).

**Specific file changes:**

#### 1. Server tests (write first)
**File:** `exploration/concept_explorer/tests/test_server.py`
- [x] Update the `client_with_pages` fixture to render/write both `dist/matrix.html` and `dist/index.html`
- [x] Add `test_matrix_is_home` and `test_pipeline_serves_grid` (stencil above) — also repointed the existing `test_index_page_returns_200` (which asserted `/`→"index", now wrong) to become `test_matrix_is_home` + `test_pipeline_serves_grid`

#### 2. Server routing + template render
**File:** `exploration/concept_explorer/server.py`
- [x] `_render_templates`: render `matrix.html.j2` → `dist/matrix.html` (`active_nav="matrix"`); render `index.html.j2` → `dist/index.html` with `active_nav="pipeline"`; concept pages now `active_nav="matrix"`
- [x] Renamed `index_page` → `matrix_page` (serves `dist/matrix.html`); added `pipeline_page` serving `dist/index.html`
- [x] Registered `app.get("/")(matrix_page)` + `app.get("/pipeline")(pipeline_page)`

#### 3. Nav + templates
**File:** `exploration/concept_explorer/templates/base.html.j2`
- [x] Added "Pipeline" nav link (`/pipeline`); home link `/` now keys off `active_nav == 'matrix'`; new "Pipeline" link keys off `active_nav == 'pipeline'`. Home link label kept as "All Concepts" (the matrix *is* the all-concepts field view).

**File:** `exploration/concept_explorer/templates/index.html.j2`
- [x] No content change (it *is* the relocated grid); renders correctly under `active_nav="pipeline"`

#### 4. Matrix page shell + bootstrap
**File:** `exploration/concept_explorer/templates/matrix.html.j2` (NEW)
- [x] Loading/error/content states (mirror `index.html.j2`); empty controls-bar + filter-panel + active-filters + `<table>` containers; script includes: `concept_label.js`, `caveat_marker.js`, `ontology_palette.js`, `matrix_data.js`, `matrix_page.js`

**File:** `exploration/concept_explorer/static/js/matrix_data.js` (NEW)
- [x] `joinConcepts(manifest, registry)` → flat `rows[]` (manifest spine + 7 registry ontology fields). **Deviation:** dropped the `tree` param from the plan's `joinConcepts(manifest, registry, tree)` signature — the tree plays no role in the per-row flat join; it's threaded into `project()`'s grouping stage in Phase 2 instead. Exposed `REGISTRY_FIELDS` for reuse.

**File:** `exploration/concept_explorer/static/js/matrix_page.js` (NEW)
- [x] `Promise.all` the three fetches → `joinConcepts(...)` → `console.log` (rows + registry + tree counts); loading→content atomic swap

### Validation
**Automated:**
- [x] `uv run python -m pytest exploration/concept_explorer/tests/test_server.py` → 27 passed (new + existing)
- [x] `uv run python -m pytest exploration/concept_explorer/tests/` → no new failures (6 pre-existing `test_extract_adapter` failures + 39 `*_manual.py` errors confirmed identical with changes stashed — Playwright `page` fixture absent + extract `n_mod` validation, both unrelated to B1)

**Manual (browser-inspect, port 8422):**
- [x] `--goto /` → matrix shell renders (nav: Taxonomy / All Concepts·active / Pipeline / Compare), console clean (`page_errors: []`), join log `rows: 36`; **exactly 3 GETs** (`manifest`, `taxonomy/registry`, `taxonomy/tree`) and `rows.length == 36 == manifest count`
- [x] `--goto /pipeline` → card grid intact (36 cards, Approved empty-state + In Progress); nav has both links, both routes 200

**What We Know Works After This Phase:** the home/grid swap is live, the three endpoints join 1:1, and the new modules load on a clean page.

---

## Phase 2: Data Core + Static Matrix Render

### Goal
Implement `matrix_data.js` (`facetValuesFor`, `project`) and render the full field as a `<table>` grouped by the family tree (flat path-labeled bands), identity column via `conceptLabel`, the 8 dimension chip columns via `ontologyPalette`/`facetModel`, with the three honest cell states. No interactions yet. See `design.md#architecture`, `design.md#component-overview`, `design.md#appendix--fieldfacet-join-map`.

### Assumption Under Test
`facetModel`-driven rendering yields correct chips/colors and honest states for every cell; the tree→bands traversal (plus the orphan band) places every served concept in exactly one band.

### Test Stencil (Write This First)
```python
# tests/test_matrix_frontend.py (NEW) — static grep-guards, mirror test_identity_frontend.py
def test_matrix_imports_theme_a_authorities():
    src = (JS_DIR / "matrix_page.js").read_text() + (JS_DIR / "matrix_data.js").read_text()
    for sym in ("conceptLabel(", "caveatMarker(", "ontologyPalette", "facetModel", "filterState"):
        assert sym in src

def test_matrix_has_no_color_literals_or_lcoe_column():
    src = (JS_DIR / "matrix_data.js").read_text() + (JS_DIR / "matrix_page.js").read_text()
    assert "--onto-" not in src and not re.search(r"#[0-9a-fA-F]{6}", src)
    assert "lcoe" not in src.lower()  # FR-B1.9: no cost column/sort/color
```

### Changes Required
**See `design.md` for:** cell render + grouping vs cell `N/A`/`TBD` treatment + tree→bands → `design.md#implementation-notes`; honest-state taxonomy + column set → `design.md#appendix--fieldfacet-join-map`; invariants → `design.md#required-invariants`.

**Specific file changes:**
- [x] `tests/test_matrix_frontend.py` (NEW): the two grep-guards above
- [x] `matrix_data.js`: `facetValuesFor(row)`; `project(rows, viewState, tree)` with tree grouping (flat path-labeled leaf bands + `"— ungrouped"` orphan band); `byCode` within-band sort; `COLUMN_FACET_KEYS`; `GROUP_OPTIONS`
- [x] `matrix_page.js`: controls-bar summary stub + the `<table>` (sticky thead/identity col), band header rows, identity cell (`conceptLabel`), 8 dimension cells (chip / grey-na / "not recorded" per the three states); `inkClassFor` contrast helper
- [x] `static/css/explorer.css`: matrix table + chip + band styles using existing `:root` tokens (no new hexes)

### Validation
**Automated:**
- [x] `uv run python -m pytest exploration/concept_explorer/tests/test_matrix_frontend.py` → 2 passed
- [x] Full matrix+server+identity+palette suite → 58 passed (no new failures vs Phase 1 baseline)

**Manual (browser-inspect, port 8422):**
- [x] `--goto /` → whole field: 36 rows in 25 family-tree bands, path-labeled (e.g. "Magnetic Fusion Energy › Stellarator › Modular"), chips colored, sticky header
- [x] Spot-check 01 / 17a / 24: correct `#code Name (Fuel)` + cells (01 = MFE/D-T/HTS (wound)/…/repRate **not recorded**; 17a = IFE, magnet **not recorded**, suffix variant distinct row; 24 = family cell **Magnetic (MFE)** under the **Non-Standard** tree band — the documented two-family disagreement)
- [x] Honest states: 288 = 36×8 dimension cells, **every cell has a chip (none blank)**; 40 "not recorded" chips; verified 01 repRate cell `isMissing=True`, title "Repetition Rate not recorded."
- [x] Banding: band-count sum **36 = row count 36**, **zero "— ungrouped" orphans** → no-silent-drop holds; every concept in exactly one band
- [x] Band rails follow the **tree hierarchy** (MFE blue / IFE purple / MIF amber / Non-Standard grey), NOT the flat enum (spec watch-out, line 178)

**What We Know Works After This Phase:** the read-only matrix is correct — join, family-tree banding, honest cells, hierarchy-faithful band color — through Theme A authorities only.

---

## Phase 3: Filter + Re-group

### Goal
Click-to-filter via `filterState` (AND across dimensions, OR within), an active-filter bar with clear; a group-by control offering `tree` + the 8 dimensions + flat `family`, with the explicit `"— unspecified"` band. All client-side. See `design.md#core-concept` (the pipeline), `design.md#implementation-notes` (group-by enumeration, unspecified folding).

### Assumption Under Test
Every interaction is pure recomputation over the single `rows[]` — filtering and regrouping never refetch, and the unspecified band collects `{null, N/A, TBD, Unknown}` when grouping.

### Test Stencil (Write This First)
```python
# tests/test_matrix_frontend.py — extend
def test_matrix_uses_filterstate_and_groups():
    src = (JS_DIR / "matrix_page.js").read_text() + (JS_DIR / "matrix_data.js").read_text()
    assert "filterState.toggle" in src and "filterState.matches" in src
    assert "unspecified" in src.lower()  # explicit band (FR-B1.5)
```

### Changes Required
**See `design.md` for:** filter semantics + no-refetch invariant → `design.md#required-invariants`; `facetValuesFor` coercion (`has_cost_model`) → `design.md#implementation-notes`.

- [x] `matrix_data.js`: filter stage in `project` (`filterState.matches(state, facetValuesFor(row))`); `groupByDimension` for the 8 dims + flat family with `isUnspecifiedGroupValue(v)` folding (covers `null`/`N/A*`/`TBD`/`Unknown`), bands ordered by the facet's declared value order
- [x] `matrix_page.js`: lifted state to closure (`rows`/`tree`/`viewState`) + single `applyView()` re-render entry; chip click → `filterState.toggle` → re-`project` → re-render; filter panel (all 10 facets, toggle chips + selected ring) behind a "Filters" toggle; active-filter bar (removable pills + Clear all); group-by `<select>` wired to `viewState.groupBy`; cell chips click-to-filter; `test_matrix_uses_filterstate_and_groups` grep-guard
- [x] `static/css/explorer.css`: controls/select/button, filter panel, filter-group, toggle/clickable/selected chip states, active-filter pills + clear button (existing tokens only)

### Validation
**Automated:**
- [x] `test_matrix_frontend.py` → 3 passed (incl. new filter/group guard); full matrix+server+identity+palette+caveat suite → 77 passed

**Manual (browser-inspect, port 8422):**
- [x] Single-dimension filter (fuel = p-B11) → 36→**5 rows**, all fuel "p-B11", 1 active-filter pill; two-dimension stacked (+ family = MFE) → **1 row** (#24, the only MFE∧p-B11), AND-across/OR-within confirmed; **Clear all** → restores 36
- [x] Regroup by fuel → bands recluster to `[D-T, D-D, D-He3, p-B11]`, rows span families within a band; regroup by repRate → explicit **`"— unspecified"` band (20 concepts, neutral rail)**; band-count sums = 36 (no silent drop)
- [x] **Network panel shows no request** on filter/regroup — API request count stays **3** throughout (the no-refetch acceptance criterion); zero page errors
- [x] Filter panel shows all 10 facets (8 dims + Archetype Fit + Cost Model as filter-only, Decision 3); selected chips ringed

**What We Know Works After This Phase:** filter + re-group behave correctly and entirely client-side, with honest unspecified handling.

---

## Phase 4: Sort, Hover, Density Polish + Acceptance

### Goal
Sort-within-group (`code` / `name` / by-column, persists across regroupings), hover→value+caveat via `caveatMarker`, collapsible bands, and the sticky/density CSS. Final acceptance sweep. See `design.md#implementation-notes` (sort model, sticky layout) and the spec's acceptance criteria.

### Assumption Under Test
Sort is orthogonal to grouping (state survives regroup), and hover surfaces value + caveat for every cell including the honest `N/A`/`TBD`/not-recorded states.

### Test Stencil (Write This First)
```python
# tests/test_matrix_frontend.py — extend
def test_matrix_sort_and_caveat_hover():
    src = (JS_DIR / "matrix_page.js").read_text() + (JS_DIR / "matrix_data.js").read_text()
    assert "sortKey" in src and "sortDir" in src
    assert "caveatMarker(" in src  # hover/caveat through the one authority
```

### Changes Required
**See `design.md` for:** sort model + sticky layout → `design.md#implementation-notes`; validation sweep → `design.md#validation-approach`.

- [x] `matrix_data.js`: `makeComparator(sortKey, sortDir)` + sort stage in `project` (within band; dimension sort by `facet.values[]` palette order, `undefined`/absent last; code tiebreak; persists across `groupBy`). Name sort routes through `conceptLabel(row).name` (the identity authority — not a raw `.name` read).
- [x] `matrix_page.js`: Sort `<select>` (Code/Name + 8 dims) + direction button + clickable column headers with active-sort arrow (`setSort`/`syncControls`); identity-cell concept caveat marker (`caveatMarker({asterisk, fitGrade})`); collapsible bands (header toggle hides `data-band` rows); cell tooltips carry value + honest-state caveat
- [x] `static/css/explorer.css`: sortable-header cursor, band toggle glyph, `.matrix-row--hidden`, tightened band-cell density (sticky thead/identity col already from Phase 2)

### Validation
**Manual (browser-inspect, port 8422) — full acceptance against spec:**
- [x] Sort within a group: **code** (default), **name** (asc + desc verified on a 25-concept band), **by-column** (magnet → palette order `[3,3,6]`, via header click → arrow shown); **re-group → sort preserved** (name sort survived tree→fuel regroup)
- [x] Hover: cell tooltips show value + affordance ("Fuel: D-T · click to filter"); **TBD** → "Driver: TBD"; **not-recorded** → "Repetition Rate not recorded."; **N/A** shares the verified TBD code path (no served concept has an N/A value — concept 39 is registry-only, not in the 36-served manifest); **10 identity caveat markers** with concept-level tooltips ("Archetype fit: None…")
- [x] **No LCOE/cost** column, group, or sort key anywhere (FR-B1.9) — verified absent from table + controls
- [x] `/pipeline` reachable from nav (clicked nav link → 36 cards); **console clean on both pages** (zero page errors); **data loads once** (3 API GETs, no refetch on any interaction); ≥3 concepts spanning families verified (01 MFE, 17a IFE, 24 Non-Standard)
- [x] Collapsible bands: header click hides the band's rows (glyph ▸), click again restores
**Automated:**
- [x] Full matrix+identity+caveat+server+palette suite → **92 passed**; full explorer suite → 6 failed / 39 errored (all pre-existing, unchanged from baseline) + 300 passed; all 4 matrix grep-guards pass

**What We Know Works After This Phase:** all four interactions, honest degradation, density, and the preserved grid — the full B1 acceptance set.

---

## Environment Setup
**See CLAUDE.md** — always `uv run python ...`; tests `uv run python -m pytest exploration/concept_explorer/tests/`; server `uv run python exploration/concept_explorer/server.py` (port 8421); browser-inspect per `.claude/skills/browser-inspect/SKILL.md`.

## Risk Management
**See `design.md#potential-risks`.** Phase-specific:
- **P1:** Theme A unmerged → branch off `feat/explorer-identity-spine`. Relocating `/` breaking the index test → fixture renders both pages + new route tests.
- **P2:** economics creep → grep-guard asserts no LCOE/hex/`--onto-` literals; honest-state correctness via browser-inspect on absent/`N/A`/`TBD`.
- **P3:** hidden refetch → explicit network-panel check; orphan/unspecified bands via `--eval`.
- **P4:** density/readability → sticky headers + collapsible bands; data size needs no virtualization.

## Implementation Notes
[TO BE FILLED DURING IMPLEMENTATION]

### Phase 1 Completion
**Completed:** 2026-06-07
**Branch:** `feat/explorer-ontology-matrix` (cut from `feat/explorer-identity-spine`; Theme A still unmerged on `main`)

**Changes Made:**
- `tests/test_server.py`: added `dist/matrix.html` to the `base_dir_with_pages` fixture; replaced `test_index_page_returns_200` with `test_matrix_is_home` (`/`→"matrix") and `test_pipeline_serves_grid` (`/pipeline`→"index").
- `server.py`: `_render_templates` now renders `matrix.html.j2`→`dist/matrix.html` (`active_nav="matrix"`) and `index.html.j2`→`dist/index.html` (`active_nav="pipeline"`); concept pages → `active_nav="matrix"`. Renamed handler `index_page`→`matrix_page` (serves matrix.html), added `pipeline_page` (serves index.html); routes `/`→matrix, `/pipeline`→grid.
- `templates/base.html.j2`: home link keys off `active_nav=='matrix'`; added "Pipeline" link (`active_nav=='pipeline'`).
- `templates/matrix.html.j2` (NEW): loading/content/error shell + empty controls/filter/active-filter/table containers; loads the 3 Theme A authorities + the 2 new modules.
- `static/js/matrix_data.js` (NEW): pure `joinConcepts(manifest, registry)` + `REGISTRY_FIELDS`.
- `static/js/matrix_page.js` (NEW): 3-fetch `Promise.all` → join → console log → atomic loading→content swap.

**Verified (browser-inspect, /tmp/browser_inspect/b1-phase1):**
- `/` join = 36 rows == manifest count (36); registry served 37, tree root has 6 family branches. Exactly 3 API GETs. Console clean, zero page errors. Theme A authorities (`matrixData`, `facetModel`, `conceptLabel`, `caveatMarker`, `filterState`) all loaded.
- `/pipeline` renders all 36 cards verbatim; nav `['Taxonomy','All Concepts','Pipeline','Compare']`, both routes 200.

**Issues Encountered:**
- A stale server from a prior session held port 8421 (`address already in use`) → my server rendered templates but failed to bind, so early curls hit old code. Resolved by killing the stale process; validated on port 8422.
- `--wait-for "#matrix-content"` timed out because the Phase-1 content div is empty (zero height → Playwright treats it as not-visible). The swap *does* happen (`display:""`); used `--wait` + direct `style.display` eval instead. Not a code issue — render lands in Phase 2.

**Deviations from Plan:**
- `joinConcepts` signature is `(manifest, registry)`, not the plan's `(manifest, registry, tree)` — the tree isn't part of the flat per-row join; it's consumed by `project()`'s grouping in Phase 2.
- Observed registry (37) > manifest (36) served sets by 1 — the opposite of the design's "missing registry row" risk and equally harmless: the extra registry concept simply isn't in the manifest spine, so it's not rendered. Join stays 1:1 over the served set.

### Phase 2 Completion
**Completed:** 2026-06-07

**Changes Made:**
- `static/js/matrix_data.js`: added `COLUMN_FACET_KEYS` (the 8 columns, keys into `facetModel`), `facetValuesFor(row)` (with `hasCostModel` String-coercion), `byCode` numeric-aware comparator, `groupByTree` (flat path-labeled bands + `"— ungrouped"` orphan band, top-level family threaded for color), `project(rows, viewState, tree)` (filter→group→sort pipeline; filter/sort default to no-op/code-asc until P3/P4), `GROUP_OPTIONS`.
- `static/js/matrix_page.js`: rewrote to render — `el()` helper, `columnFacets()` from `facetModel`, `inkClassFor` (luminance→text-contrast class), `chip`, `buildDimCell` (3 honest states), `buildIdentityCell` (`conceptLabel`→link), `buildHead`, `buildBandHeader` (family-colored rail), `render`, controls-bar summary stub.
- `static/css/explorer.css`: appended the B1 matrix section — scroll-wrap (owns both axes for sticky), sticky thead + identity column, band header rail, `.onto-chip` + `--ink`/`--paper`/`--na`/`--missing`. All via `:root` tokens; chip/band colors set inline from `ontologyPalette`.
- `tests/test_matrix_frontend.py` (NEW): `test_matrix_imports_theme_a_authorities`, `test_matrix_has_no_color_literals_or_lcoe_column`.

**Issues Encountered:**
- **Self-inflicted, caught & fixed:** the first Edit to `matrix_data.js` accidentally dropped the `joinConcepts` function body while replacing its block → `matrixData is not defined` at load (browser-inspect page_errors caught it; the grep-guard pytest passed because it only checks for the export *reference*). Re-added the function. Lesson: the static grep-guards don't catch a load-time ReferenceError — browser-inspect's sidecar is what caught it.
- `--wait-for ".matrix-row"` is the right readiness signal now (rows have height), unlike Phase 1's empty container.

**Deviations from Plan:**
- **Band color follows the tree's top-level family, not member `confinement_family`.** The plan/design said "header color = top-level family"; my first pass keyed it off `bandRows[0].confinement_family` (the flat enum), which mis-colored the DPF Non-Standard band MFE-blue (enum says MFE, tree says Non-Standard). Fixed to thread the top-level tree family down `groupByTree`, validated against `ontologyPalette.family` keys (non-standard branches → `NONSTANDARD`). This honors the spec watch-out (line 178) against keying group color off the flat enum.
- `project` signature is `(rows, viewState, tree)` — the tree is a third arg (consistent with the Phase-1 decision to keep it out of `joinConcepts`).

**Data observation (no action — faithful render of existing data):**
- Concept 24 (Dense Plasma Focus) has manifest `confinement_family = "MFE"` but the decision tree files it under "Other Non-Standard › Plasma focus". The matrix shows the flat enum in the cell and groups/colors by the tree — exactly the spec's documented disagreement case. Not a B1 defect; a taxonomy-data question outside scope.

### Phase 3 Completion
**Completed:** 2026-06-07

**Changes Made:**
- `static/js/matrix_data.js`: added `isUnspecifiedGroupValue(v)` (`null`/`N/A*`/`TBD`/`Unknown`) and `groupByDimension(rows, key)` (declared value order + trailing `"— unspecified"` band + unexpected-enum bands); `project` now dispatches tree vs. dimension grouping. The filter stage (`filterState.matches` over `facetValuesFor`) was already present from Phase 2.
- `static/js/matrix_page.js`: lifted `rows`/`tree`/`viewState` to closure scope; single `applyView()` (project → render → summary → active-filters → sync-panel) is the one re-render path. Added `toggleFilter`, `buildControls` (group-by select + Filters toggle + summary), `buildFilterPanel` (10 facets), `syncFilterPanel`, `updateActiveFilters`, `updateSummary`; cell chips are click-to-filter. Replaced the Phase-2 `renderControlsStub`.
- `static/css/explorer.css`: matrix controls/select/button, collapsible `.matrix-filter-panel`, `.filter-group`, chip `--toggle`/`--clickable`/`--selected` states, `.active-filter` pills + `.matrix-clear-btn`. Existing tokens only.
- `tests/test_matrix_frontend.py`: added `test_matrix_uses_filterstate_and_groups`.

**Verified (browser-inspect):** single→two-dim filtering narrows correctly (5 then 1 of 36), clear restores; regroup by fuel reclusters across families; regroup by repRate produces the explicit 20-concept unspecified band; **API request count stays at 3** across every filter/regroup (no-refetch invariant); selected chips ring, active pills + clear work; zero page errors.

**Deviations from Plan:** none. (Cell-chip click-to-filter and the filter-panel toggle were the natural reading of "filter by clicking a cell/chip" + "filter panel (all 10 facets)".)

### Phase 4 Completion
**Completed:** 2026-06-07

**Changes Made:**
- `static/js/matrix_data.js`: `makeComparator(sortKey, sortDir)` — code / name (via `conceptLabel`) / dimension (palette value order, absent last, code tiebreak); `project` applies it per band, so sort is orthogonal to `groupBy` and persists across regroupings.
- `static/js/matrix_page.js`: `sortArrow`/`setSort`/`sortOptions`/`syncControls`; Sort `<select>` + direction button in the controls bar; clickable sortable column headers with an active-sort arrow; identity cell now appends `caveatMarker({asterisk, fitGrade}).element()`; collapsible band headers (toggle glyph + `data-band` row hiding).
- `static/css/explorer.css`: `.matrix-head--sortable`, `.matrix-band__toggle`, `.matrix-row--hidden`, denser band-cell padding.
- `tests/test_matrix_frontend.py`: added `test_matrix_sort_and_caveat_hover`.

**Issues Encountered (self-inflicted, caught by the full suite & fixed):**
- The name comparator's raw `a.name`/`b.name` reads tripped Theme A's `test_no_raw_name_label_render` grep-guard → rerouted through `conceptLabel(row).name` (same value, honors the single-naming-authority rule).
- A literal ⚠ glyph in a JSDoc comment tripped `test_caveat.py::test_marker_markup_authored_only_in_caveat_marker` (it greps raw text incl. comments) → reworded the comment. Both fixed; full suite back to the 6-fail/39-err pre-existing baseline.

**Deviations from Plan:** none material. Sort is exposed two ways (a Sort select offering code/name/columns, and clickable column headers) kept in sync via `syncControls` — the natural reading of "sort control + clickable column headers." Band collapse state is ephemeral (resets on any re-projection — filter/sort/regroup rebuild the table); persisting it across regroup wasn't required and band identity changes on regroup anyway.

---

## B1 Acceptance Summary (all four phases complete)

Against the spec's Acceptance Criteria:
- ✅ `/` shows the matrix: 36 concepts as rows in 25 family-tree bands, 8 ontology columns, v3-palette chips (FR-B1.1/B1.3)
- ✅ Leftmost column = `#NN Name (Fuel)` via `conceptLabel`, row links to the concept page (FR-B1.2)
- ✅ Re-group by any of 8 dimensions (+ flat family) live; unspecified → explicit "— unspecified" band (FR-B1.4/B1.5)
- ✅ Click-to-filter (cell chips + filter panel), AND across / OR within, see + clear active filters (FR-B1.6)
- ✅ Sort within group by code / name / column, persists across regroup (FR-B1.7)
- ✅ Hover → value + caveat; N/A·TBD·not-recorded all explicit, never blank (FR-B1.8)
- ✅ No LCOE/cost column, group, or sort key (FR-B1.9)
- ✅ Card grid preserved at `/pipeline`, linked from nav (FR-B1.10)
- ✅ Renders through Theme A authorities only — grep-guards enforce no duplicated identity/color/facet/caveat logic, no color literals (FR-B1.11)
- ✅ Data loads once (3 GETs); no refetch on filter/regroup/sort; console clean

**Branch:** `feat/explorer-ontology-matrix` (off `feat/explorer-identity-spine`; do not target `main` until Theme A lands). **Not yet committed.**

**Suggested next:** `/_my_audit_implementation` against this plan before committing.

---

**Status**: Draft → In Progress → **Complete**
