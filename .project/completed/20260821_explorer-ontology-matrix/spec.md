# Spec: The Living Ontology Matrix (B1)

**Status:** Implementation Complete (2026-06-07, branch `feat/explorer-ontology-matrix`)
**Owner:** Reid W
**Created:** 2026-06-07 09:25 PDT
**Complexity:** MEDIUM
**Branch:** feat/explorer-identity-spine (B1 to branch separately)

---

## Work Item Summary

B1 is the headline Phase-2 reframe of the concept explorer: replace the landing page's Approved/In-Progress card-grid split with a dense, interactive **ontology matrix** — `concept_ontology_v3.png` made live. Rows are the ~40 concepts grouped under the family tree; columns are the ontology design dimensions (fuel, magnet, driver, capture, blanket, op-mode, rep-rate, family); cells are color-coded category chips in the v3 palette. The user can **filter** by clicking chips, **re-group** the rows under any dimension (flip the organizing hierarchy live), **sort within a group**, **hover** a cell to read its value + caveat, and click a row to open the concept page. The matrix becomes the new home (`/`); the existing card grid moves to its own page as the pipeline-status/approvals view. "Done" means a researcher's first question — *"what is the space of fusion approaches, and where does my concept sit in it?"* — is answered on the first page, grounded in well-supported categorical data rather than the asterisked LCOE numbers.

## Why This Matters Now

The landing page is the entry point, and today it answers the wrong question: it splits ~40 concepts into "Approved / In Progress" (an internal pipeline distinction the user doesn't care about) with no families, no filter, no sort, no sense of the design space. The one spatial full-field view (the constellation) is buried on `/taxonomy`, undiscoverable from home. J1 — orientation — is the journey every user hits first and the one the current home serves worst. B1 is also the first surface to *spend* the Theme A spine: A2 shipped a per-dimension palette and a facet/filter-state model with no on-screen home until this matrix exists. Under known-stale LCOE numbers, leading with the design space (the well-grounded categorical data) is the trustworthy first orientation; cost is demoted to a later ride-along (B3), not the spatial driver.

## Key Bets / Constraints

- **Bet:** the ontology matrix — the whole field (~40 concepts × ~8 dimensions) on one screen — is a better home than a card grid, because density + structure is exactly what orientation (J1) needs and the cards can't provide.
- **Bet:** B1 is **mostly UI wiring**, not new data. Theme A already shipped the identity helper, the palette, the facet/filter-state model, and the caveat marker; every ontology attribute already lives on the taxonomy registry, the family hierarchy on the decision tree, and the LCOE/caveat flags on the manifest. B1 joins three existing endpoints and renders.
- **Constraint:** the organizing principle is the **ontology (design space), not cost**. LCOE is **not** a column and **not** a sort/color key in B1 (that is B3). This is the deliberate reversal of the research doc's economics-first framing.
- **Constraint:** honest degradation is a hard rule (carried from Phase 1 / Theme A): `N/A` / `TBD` / not-recorded cells say so via the shared caveat vocabulary; they never blank-vanish, and a concept that is `N/A`/`TBD` on the active grouping dimension lands in an explicit "—/unspecified" band, never silently dropped.
- **Constraint:** the matrix consumes Theme A's shared components (`conceptLabel`, `ontologyPalette`, `facetModel`, `filterState`, `caveatMarker`) — it does not re-invent identity, color, facet, or caveat logic.
- **Non-goal:** the parallel-categories "flows" lens (B2) and economics-as-ride-along columns (B3) — deferred, design leaves clean hooks.
- **Non-goal:** the constellation rebrand/refocus (C1), the family/comparables comparison entry (C2), any concept-page provenance/maturity depth (Theme D).

---

## Business Goals

### Why This Matters

A researcher or enthusiast arriving at the explorer should immediately see the field — how many concepts, grouped how, and where their concept of interest sits among its peers — and be able to narrow it down by the attributes they care about (aneutronic fuels, HTS magnets, pulsed operation). Today the home page can't do any of this; the user has to already know concept IDs and assemble understanding by hand across pages. B1 puts orientation on the first page, organized around the design space the field actually varies on, and makes that orientation trustworthy by leading with categorical data that is well-grounded rather than LCOE numbers that are asterisked.

### Success Criteria

- [ ] On first load of `/`, a user sees the whole field of concepts at once, grouped by family, with each concept's ontology attributes visible as color-coded cells — no clicking required to get oriented.
- [ ] A user can narrow the field by clicking attribute chips (e.g. show only p-B11 concepts) and the visible set updates to match.
- [ ] A user can re-group the rows by a different dimension (e.g. group by fuel instead of family) and immediately see which concepts share that attribute and what else they have in common.
- [ ] A user can read what any cell means (its value + any caveat) and jump from a row to that concept's page.
- [ ] Missing/unspecified attributes announce themselves honestly; nothing silently vanishes.
- [ ] The previous Approved/In-Progress card grid is still reachable as its own page for viewing pipeline/approval status.

### Priority

P1, the headline item of Phase 2 ("Theme B is the headline reframe and the current focus"). Depends on Theme A (landed). Independent of the remaining Phase-1 loose ends (Item 2-FU) and of B2/B3/C/D.

---

## Problem Statement

### Current State

- **Home page** (`/`, `index_page.js`): fetches `/api/manifest`, splits concepts into `#grid-approved` / `#grid-in-progress` by `status`, renders cards (illustration, `#NN Name (Fuel)`, family badge, company, caveat, LCOE, confidence, Σ glyph). Only interaction is click-through. No families, no filter, no sort, no search. The Approved/In-Progress split is a pipeline-internal state, not a user question.
- **Ontology data is collected and served but unsurfaced as a field view.** Every concept's ontology dimensions live on `ConceptTaxonomy` via `/api/taxonomy/registry`; the family hierarchy is `decision_tree.json` via `/api/taxonomy/tree` (with `tree_view.js` rendering and `prune_decision_tree` already in place). The only place this data is shown is the taxonomy card (7 of ~25 fields) and the constellation — both on `/taxonomy`, both per-focused-concept, neither a full-field matrix.
- **Theme A's palette and facet model have no on-screen home.** `ontology_palette.js` ships `ontologyPalette` (all 8 dimensions + family colors, traceable to the PNG), `facetModel` (10 facets with `{key, label, field, values}`), and `filterState` (`create/toggle/isEmpty/matches`) — all client-side, all currently unconsumed by any filtering UI.

### Desired Outcome

The matrix is the home page: the full field on one screen, rows grouped by the family tree by default and re-groupable under any dimension, columns = the ontology dimensions as v3-palette chips, with click-to-filter, sort-within-group, hover-to-explain (value + caveat), and row→concept navigation. The card grid is preserved as a separate pipeline/approvals page. No new extraction, no new server data model — the matrix joins the existing manifest + registry + tree and renders through Theme A's shared components.

---

## Scope

### In Scope

- **New landing page = the matrix** at `/`. Rows = concepts; columns = the ontology dimensions; leftmost column = `#NN Name (Fuel)` via `conceptLabel()`; cells = color-coded category chips via `ontologyPalette`.
- **Default row grouping = the existing decision tree** (`/api/taxonomy/tree`), reusing the established hierarchy (and `prune_decision_tree` for omitted concepts). Collapsible group bands.
- **Re-grouping**: a group-by control lets the user re-cluster rows under any ontology dimension's categories (flip the organizing hierarchy live). Concepts that are `N/A`/`TBD`/unspecified on the active grouping dimension land in an explicit "unspecified" band.
- **Filter by clicking** a cell/chip — consume `filterState` (AND across dimensions, OR within a dimension); the visible row set updates; a way to see and clear active filters.
- **Sort within a group** (e.g. by name/code, or by a chosen column's category order); sort state is sensible across re-groupings.
- **Hover a cell → value + source/caveat** via `caveatMarker()` / the shared caveat vocabulary.
- **Row → concept page** navigation; the `#NN` code is the visible stable handle (A1).
- **Honest degradation**: `N/A`/`TBD`/not-recorded cells render an explicit marker, never blank.
- **Card grid relocated** to its own page (e.g. `/approvals`) preserving the Approved/In-Progress status view; nav updated so it remains reachable.
- The column set is the **8 ontology dimensions** (family, fuel, magnet, driver, capture, blanket, op-mode, rep-rate). Which of `facetModel`'s non-dimension facets (fit-grade, has-cost-model) appear as columns vs. filter-only is a design call.

### Out of Scope

- **B2** — parallel-categories "flows" lens (secondary view toggle). Design leaves a hook; no implementation.
- **B3** — economics as ride-along (LCOE/confidence columns to sort/color by). Explicitly excluded from B1; LCOE is neither a column nor a sort/color key here. Design leaves a hook.
- **C1/C2** — constellation rebrand/refocus, family/comparables comparison entry.
- **Theme D** — concept-page provenance/maturity depth.
- **Free-text search** by name/company (research idea 5) — not required for B1; may be a fast-follow.
- New server endpoints, new extraction, or changes to the concept-analysis data files. B1 joins existing `/api/manifest` + `/api/taxonomy/registry` + `/api/taxonomy/tree`.
- Changing the underlying taxonomy attribute data or the decision-tree structure.

### Edge Cases & Considerations

- **Two family notions disagree**: `ConfinementFamily` enum (MFE/IFE/MIF/NONSTANDARD; ARC is NONSTANDARD) vs. the richer `decision_tree.json` hierarchy. The default grouping uses the **decision tree** (settled); the flat enum may be offered as one re-group option. Design picks how the group-by control enumerates available grouping dimensions.
- **Concepts omitted/pruned** from the served set must be handled consistently with `prune_decision_tree` so the tree grouping doesn't show empty branches or orphan rows.
- **`N/A` vs `TBD` vs absent** are distinct in the taxonomy enums (e.g. `MagnetType.NA` vs `.TBD`, `BlanketConfig` has two `N/A` variants). The cell rendering and the "unspecified" grouping band need a defined, honest treatment for each — not a single catch-all blank.
- **Suffix-variant concepts** (17a/17b, 20a/20b) are distinct rows with distinct `#code`s and names (already handled by Theme A identity).
- **Data join**: ontology attributes live on the **registry**, not the thin manifest; LCOE/caveat/has-cost-model/illustration flags live on the **manifest**. B1 must join registry + tree + manifest per concept — design owns the join strategy (client-side merge vs. a thin server view).
- **Density/performance**: ~40 rows × ~8–10 columns of chips, with live filter/regroup/sort. Should remain responsive; avoid full re-fetch on every interaction (data loads once, interactions are client-side).
- **Multi-valued attributes**: some fields are `+`-joined combos (e.g. `heating_type` parsed to a list). Design decides whether such a cell shows multiple chips and how it filters/groups.

---

## Requirement Selection Notes

The normative requirements below fix what we have actually decided: the matrix replaces the home page; the four interactions (filter, re-group, sort, hover) are all in v1; the default grouping is the decision tree; cost stays out of the organizing principle; honest degradation is mandatory; Theme A's components are reused rather than re-implemented; and the card grid is preserved elsewhere. They deliberately do **not** fix: the exact column set's treatment of the non-dimension facets, the group-by control's UI, the data-join mechanism (client merge vs. server view), the sort model's precise behavior across regroupings, the cell rendering of multi-valued/`N/A`/`TBD` states, or whether free-text search is added — those are design decisions. No requirements are written for B2/B3 since they are out of scope.

---

## Requirements

### Functional Requirements

> From the user's request and the epic's B1 definition unless marked [INFERRED].

1. **FR-B1.1**: The landing page (`/`) MUST present the served concepts as a single matrix — rows = concepts, columns = the ontology design dimensions, cells = category chips colored from the shared `ontologyPalette` (v3, PNG-traceable) — showing the whole field on one screen without per-concept drill-in.
2. **FR-B1.2**: The leftmost row identity MUST render the concept's `#NN` code and `Name (Fuel)` via the shared `conceptLabel()` helper, and a row MUST link to that concept's page.
3. **FR-B1.3**: Rows MUST be grouped by default under the existing family **decision tree** (`/api/taxonomy/tree`), respecting the existing pruning of omitted concepts, with collapsible group bands.
4. **FR-B1.4**: The user MUST be able to **re-group** the rows live under any offered ontology dimension's categories (not only the family tree), without leaving or reloading the page.
5. **FR-B1.5** [INFERRED]: When re-grouping by a dimension, concepts whose value on that dimension is `N/A`/`TBD`/unspecified MUST be collected into an explicit, labeled "unspecified" band — never silently dropped.
6. **FR-B1.6**: The user MUST be able to **filter** the visible concepts by clicking a cell/chip, consuming the shared `filterState` model (AND across dimensions, OR within a dimension), with a visible way to see and clear active filters.
7. **FR-B1.7**: The user MUST be able to **sort** concepts within a group.
8. **FR-B1.8**: Hovering (or otherwise inspecting) a cell MUST surface that cell's value and any caveat via the shared caveat vocabulary (`caveatMarker()`), including an explicit treatment for `N/A`/`TBD`/not-recorded — a cell MUST NOT silently vanish or read as blank.
9. **FR-B1.9**: B1 MUST NOT use LCOE/cost as a column, a grouping dimension, or a sort/color key (economics ride-along is deferred to B3); the organizing principle is the ontology.
10. **FR-B1.10**: The previous Approved/In-Progress card grid MUST be preserved as its own reachable page (a pipeline/approvals view), and navigation MUST be updated so it remains discoverable.
11. **FR-B1.11** [INFERRED]: The matrix MUST consume Theme A's shared components (`conceptLabel`, `ontologyPalette`, `facetModel`, `filterState`, `caveatMarker`) rather than re-implementing identity, color, facet, or caveat logic.

### Non-Functional Requirements

- Concept data SHOULD load once; filter/re-group/sort interactions SHOULD be client-side with no per-interaction refetch (carried from the Phase-1 "no jank / preload" practice).
- The matrix SHOULD remain responsive at the full field size (~40 concepts × ~8–10 dimensions) under live filtering/regrouping.

---

## Acceptance Criteria

### Core Functionality

- [ ] Loading `/` shows the matrix: all served concepts as rows grouped by family, ontology dimensions as columns, cells as v3-palette chips. *(FR-B1.1, FR-B1.3)*
- [ ] The leftmost column shows `#NN Name (Fuel)` for every row and clicking a row opens that concept's page. *(FR-B1.2)*
- [ ] Selecting a different group-by dimension (e.g. fuel) re-clusters the rows live; concepts unspecified on that dimension appear in a labeled "unspecified" band. *(FR-B1.4, FR-B1.5)*
- [ ] Clicking attribute chips filters the visible concepts (verified: a single-dimension filter and a two-dimension stacked filter each narrow correctly); filters can be seen and cleared. *(FR-B1.6)*
- [ ] Concepts can be sorted within a group. *(FR-B1.7)*
- [ ] Hovering a cell shows its value + caveat; an `N/A`/`TBD`/unrecorded cell shows an explicit state, not a blank. *(FR-B1.8)*
- [ ] No LCOE/cost column, grouping, or sort key appears on the matrix. *(FR-B1.9)*
- [ ] The Approved/In-Progress card grid is reachable on its own page and linked from the nav. *(FR-B1.10)*

### Quality & Integration

- [ ] Existing test suite continues to pass.
- [ ] The matrix renders through the Theme A shared components (no duplicated identity/color/facet/caveat logic introduced). *(FR-B1.11)*
- [ ] Browser-inspect validation on ≥3 concepts spanning families (e.g. 01, 24, 17a): correct identity, correct cells, filter/regroup/sort behave, console clean.
- [ ] Data loads once; filter/regroup/sort do not refetch (verified in the network panel / via browser-inspect).

---

## Next-Stage Handoff

**Settled in this spec:**
- The matrix replaces the home page at `/`; the card grid moves to its own pipeline/approvals page.
- All four interactions — filter, re-group, sort, hover — are in B1's v1.
- Default row grouping = the existing decision tree; the flat `ConfinementFamily` enum may be one re-group option.
- Columns are the 8 ontology dimensions; cost is excluded as column/group/sort/color (B3 deferred).
- Theme A's components are consumed, not re-implemented; no new extraction or endpoints required.
- Honest degradation is mandatory, including an explicit "unspecified" band when grouping.

**Design must figure out:**
- The data-join mechanism: client-side merge of `/api/manifest` + `/api/taxonomy/registry` + `/api/taxonomy/tree`, vs. a thin server view that pre-joins them.
- The group-by control: which dimensions it offers (the 8 ontology facets + the flat family enum?), and how it enumerates them from `facetModel`.
- Whether the non-dimension facets (fit-grade, has-cost-model) appear as columns, filter-only, or not in B1.
- The sort model: sort keys offered, and how sort state behaves across re-groupings.
- Cell rendering for multi-valued attributes (`+`-joined heating, parsed lists) and the distinct `N/A` vs `TBD` vs absent states.
- The card grid's new route/name and nav placement.
- Layout/density approach for ~40×~10 chips that stays responsive (sticky headers, collapsible bands, virtualization if needed).

**Watch-outs for design:**
- Don't let the matrix re-derive colors/identity/caveats — it must go through Theme A's authorities (the whole point of building the spine first).
- The `N/A`/`TBD`/unspecified handling is the easy thing to get wrong (the explorer's legacy "silent vanish" habit is exactly what to avoid).
- Two family notions disagree — keep the decision tree as the default grouping and don't accidentally key cell/group colors off the flat enum where the rich hierarchy is meant.
- Pruned/omitted concepts must not produce empty tree branches or orphan rows.
- Keep B3 (economics) genuinely out — the temptation to "just add an LCOE column" reintroduces the economics-first framing this reframe deliberately reversed.

---

## Related Artifacts

- **Epic:** `.project/backlog/epic_explorer_ux_v3.md` — "Phase 2+ Vision", Theme B (B1 definition, lines 228–231), and the ontology-first reversal rationale (line 204).
- **Research:** `.project/research/20260605-150329_concept-explorer-ux-user-journeys.md` — J1 (orientation) and ideas 4–6 (note the economics-first framing was reversed; B1 is the ontology-first version).
- **Theme A (the spine B1 consumes):** `.project/active/explorer-identity-spine/{spec.md,design.md}` — `conceptLabel`, `ontologyPalette`, `facetModel`, `filterState`, `caveatMarker`.
- **Ontology image (the artifact made live):** `.project/research/concept_ontology_v3.png`.
- **Design:** `.project/active/explorer-ontology-matrix/design.md` (to be created).

---

**Next Steps:** After approval, proceed to `/_my_design`.
