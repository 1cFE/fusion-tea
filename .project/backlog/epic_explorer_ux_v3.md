# Epic: Explorer UX v3 — Provenance & Coherence

**Epic ID**: EXPLORER-UX-V3
**Status**: Active
**Priority**: P1
**Created**: 2026-06-06
**Estimated Effort**: Phase 1 ~3–3.5 days (2 items); later phases TBD

---

## Executive Summary

Turn the concept explorer from a browser of pipeline *state* into an instrument for *investigating* the numbers — honest about its own uncertainty. The `concept_analysis` rework produced a rich, source-cited corpus (override registry with provenance/rationale, design points, archetype-fit grades, layered maturity, comparables), but the explorer ingests a thin slice of it and re-buries the single richest artifact — the override registry — behind one boolean `overridden: true` star. This epic surfaces that data and fixes the seams that make the quantitative-investigation journey untrustworthy under known-stale numbers.

The driving research is [`.project/research/20260605-150329_concept-explorer-ux-user-journeys.md`](../research/20260605-150329_concept-explorer-ux-user-journeys.md), which frames six user journeys (J1–J6) and twelve improvement ideas across four tiers.

**Phase 1** builds the J2/J3 spine — *"why is this number what it is, and can I trust it?"* — the explorer's real value proposition while the LCOE numbers are asterisked. It is the two highest-leverage Tier-1 items: slider/tornado/headline coherence, then the override-inspection surface.

**Critical Success Factor**: A user can drag a slider and trust that the curve they're perturbing is the curve the headline number sits on — and can click any ★ to read what the analyst changed, to what, from what, and why.

---

## Why This Epic?

**Current State**:
- The override registry — six fields per entry (`account`, `value`, `provenance`, `source`, `rationale`, `cost_basis`), the artifact the whole rework was built to produce — reaches the UI as exactly one bit: a ★ glyph. The "why" is discarded at the extractor boundary.
- The slider, tornado, and headline describe **three different LCOE functions**. The first slider touch silently drops the analyst's overrides, collapsing concept 01 from 155.17 → 127.53 $/MWh (−17.8%) on a half-percent availability nudge the user didn't make. The tornado is also overrides-off; it agrees with the slider and both disagree with the hero number. You cannot debug a number by perturbing a different number.
- Under known-stale data, *traceability* is the product — and it is exactly the layer the explorer omits.

**Future State (Phase 1)**:
- One `apply_analyst_overrides` toggle drives slider recompute, tornado source, and headline in lockstep. No phantom discontinuity. The toggle itself teaches "what is the analyst's judgment worth here?" (~$28/MWh on concept 01).
- Every ★ in the system — CAS rows, treemap tiles, CapEx compare bars, and the toggle's count chip — becomes the entry point of the provenance journey: a panel showing each override's account, value, provenance, source, and rationale, including the disabled-but-`blocked_by` entries that are the most interesting debugging signal.

---

## Success Criteria (Phase 1)

- [x] No spurious LCOE discontinuity on first slider touch: a no-op `overrides={}` compute at default UI state matches the stored headline (FR-SO1). *(Item 1)*
- [x] Slider, tornado, and headline are sourced from the same LCOE function at any moment, in whichever toggle state (FR-SO2); toggling swaps all three in lockstep with no partial-update frame (FR-SO5). *(Item 1)*
- [x] Extractor emits both `sensitivities_bare` and `sensitivities_applied` per costingfe concept (FR-SO4). *(Item 1)*
- [x] The toggle is hidden/disabled — never a dead control — for freeform, empty-registry, and `fit_grade=None` concepts (FR-SO6). *(Item 1)*
- [x] Clicking the toggle's count chip (or any ★ on a CAS row / treemap tile / CapEx compare bar) surfaces the override's `account`, `value`, `provenance`, `source`, and `rationale` without leaving the page (FR-SO7). *(Item 2)*
- [x] Disabled (`enabled: false`) overrides render visually distinct and tagged with `blocked_by`. *(Item 2)*
- [x] Surfaces degrade *honestly* when a field is absent (say so — do not silently vanish). *(Item 2)*
- [x] Existing test suite passes; new regression test for FR-SO1 against concept 01. *(Item 1)*

---

## Phase 1 Decisions (settled 2026-06-06)

These were settled in discussion before decomposition; specs/designs inherit them:

1. **Slider semantics = option (c)** from the slider spec: expose both LCOE functions via a single toggle, default on. (Design phase may still reverse with written rationale, but the burden has shifted — both functions are interpretively legitimate.)
2. **Toggle placement = hero block** (next to the LCOE number). Reads as "*this number* is the analyst's," which is the trustworthiness question the headline raises.
3. **Split into two items, not one.** Item 1 ships the toggle with an **inert** "(N entries)" count; Item 2 makes that count a **clickable** panel trigger and extends the panel across the other ★ sites. The inert-count intermediate state is honest and strictly better than today's silent ★, so it clears the "leaves UX in a good state" bar. **FR-SO7 (the inspection affordance) moves out of the slider spec and into Item 2** so each item is one cohesive theme.
4. **Disabled overrides are included** in Item 2's inspection panel — shown visually distinct (greyed/struck) and tagged with `blocked_by`. They are the cleanest physics-debugging signal ("a departure we'd make but an upstream bug blocks").

---

## Backlog Items

### Phase 1

#### Item 1: Slider / Tornado / Headline Coherence [1.5–2 days]

**Type**: Code/Integration

**Objective**: A single `apply_analyst_overrides` toggle (default on, in the hero block) drives slider recompute, tornado source, and the headline in lockstep, so the three never describe different LCOE functions. Resolves the −17.8% phantom discontinuity.

**Current State**:
- ✅ Spec already exists (draft) at `.project/active/explorer-slider-override-semantics/spec.md` with options (a)/(b)/(c) analyzed and (c) recommended.
- ✅ Three-forward contract (`generic`/`native`/`result_1gw`) and `enabled_overrides()` available at module level (`model_setup_helpers.py`).
- ⚠️ `_forward_with_overrides` (server.py:143) deliberately drops `cost_overrides` on recompute.
- ⚠️ Tornado built `cost_overrides=None` (`extract_explorer_data.py:184`, library-bare).
- ❌ No `apply_analyst_overrides` in `ExplorerState`; LRU key is `(concept_id, frozenset(overrides))`.

**Scope**:
1. **Compute path**: `_forward_with_overrides` re-applies `enabled_overrides(module.overrides)` and passes `override_reference_mw=P_native` when the toggle is on (re-import via the already-cached `_load_model_module`; no new IO). When off, current behavior. Extend the LRU key to `(concept_id, frozenset(overrides), apply_analyst_overrides)`.
2. **Extractor**: emit two precomputed sensitivities — `sensitivities_bare` (`cost_overrides=None`) and `sensitivities_applied` (`cost_overrides=enabled_overrides(...)`), computed via two honest `model.sensitivity()` calls (do not derive one from the other — `_scale_overrides` keeps a rescaled shape). Equal registries store one.
3. **State**: add per-concept `apply_analyst_overrides: bool = True` to `ExplorerState`; thread through `/api/compute` and tornado source selection.
4. **UI (hero toggle)**: checkbox "Apply analyst cost adjustments (N entries)" + plain-language subtitle ("On: the analyst's accountable cost story. Off: the costing library's bare answer for this architecture."). Toggling updates headline + slider baseline + tornado atomically. The "(N entries)" count is **inert text** here (Item 2 makes it clickable). Hidden/disabled for freeform / empty-registry / `fit_grade=None` concepts.
5. **Docs**: record chosen semantics in an inline doc comment on `_forward_with_overrides` and/or the explorer README.

**Out of Scope**:
- The override-inspection panel (FR-SO7) — that is Item 2.
- Per-account `generic`/`native`/`result_1gw` delta decomposition (future phase, research idea 9).
- Editing the registry from the UI.
- Any landing-page / family / comparables work.

**Status**: ✅ Complete (implemented + browser-validated 2026-06-06). See `.project/active/explorer-slider-override-semantics/plan.md` for the full implementation record.

**Success Criteria**:
- [x] FR-SO1: no-op compute at default state matches stored headline for ≥3 concepts spanning fit-grade tiers (01 ✓, 17a ✓, 24 ✓ — verified through the server compute path). *Note: `data/24.json` was found stale during this verification (8.51 vs the module's 16.05) and re-extracted; see plan Phase 2 notes + FU2 below.*
- [x] FR-SO2: an `availability` sweep produces a monotone LCOE curve whose slope sign matches the tornado's elasticity sign, verified in each toggle state (applied 184.6→140.9, bare 151.0→116.2 on concept 01).
- [x] FR-SO4: concept 01's `sensitivities_bare` and `sensitivities_applied` differ for ≥1 parameter; both present in the extracted JSON.
- [x] FR-SO5: toggling without moving a slider swaps headline + slider baseline + tornado in lockstep (no partial-update frame) — verified via browser-inspect on 01 and 24, console clean.
- [x] FR-SO6: a freeform concept (03) renders no toggle; an empty-registry costingfe concept (05) renders it disabled with a hover explanation.
- [x] Existing tests pass (229 passed; 6 pre-existing `test_extract_adapter` failures unrelated); new FR-SO1 regression test against concept 01.
- [x] No visible `/api/compute` latency regression (cached, sub-200 ms; no measurable change in smoke testing).

**Estimated Effort**: 1.5–2 days (spec exists; design ~3h to lock option (c) + cache/`P_native` provisioning, plan ~1h, execute ~8–10h)

**Location**: `.project/active/explorer-slider-override-semantics/`

**Dependencies**: `explorer-rework-unblock` (landed). Independent of Item 2's data layer.

**Deliverables**:
- `.project/active/explorer-slider-override-semantics/{design.md,plan.md}` (spec exists)
- Changes to `server.py` (`_forward_with_overrides`, LRU key, compute), `extract_explorer_data.py` (dual sensitivities), `models.py`/`ExplorerState`, concept-page JS (hero toggle + lockstep), `explorer.css`
- FR-SO1 regression test

---

#### Item 2: Override-Inspection Surface [1.5 days]

**Type**: Implementation (data-layer schema emit + reusable UI panel)

**Objective**: Emit the full override-registry narrative into the concept JSON and surface it as one reusable inspection panel, triggered from the toggle's count chip and from every ★ in the system. Converts each ★ from a dead-end marker into the entry point of the J3 provenance journey.

**Current State**:
- ✅ The registry's six fields (+ optional `blocked_by`) are already evaluated in each concept's `model_setup.py` (`Override` TypedDict, `model_setup_helpers.py:46`).
- ✅ Item 1 ships the hero toggle with an inert "(N entries)" count — the primary trigger lives there.
- ⚠️ Registry reaches the front-end only as `overridden: bool` → ★ (`models.py:254`, `cas_breakdown.js:277`).
- ❌ No `overrides` records in `ConceptData`; no inspection component; ★ on CAS rows / treemap tiles / CapEx compare bars carry no "why."

**Scope**:
1. **Extractor schema**: emit `overrides: list[OverrideRecord]` into `ConceptData` — `account`, `value`, `enabled`, `provenance`, `source`, `rationale`, `cost_basis`, `blocked_by`. Preloaded with the concept payload (bounded, per-concept; never fetched per render).
2. **Inspection panel component** (one component, reused): per enabled override shows account + human-readable name (e.g. "C220103 — Reactor Equipment"), `value` formatted in M$ at native scale, `provenance`, `source` (clickable citation where the data layer permits), `rationale` (1–2 sentences).
3. **Disabled overrides** (`enabled: false`): shown visually distinct (greyed/struck) and tagged with `blocked_by`.
4. **Trigger sites**: make Item 1's "(N entries)" count chip clickable → panel; attach the same panel to ★ CAS-breakdown rows, ★ treemap tiles, and ★ CapEx compare bars (the per-account trigger scopes the panel to that one account).
5. **Honest degradation**: a concept/override missing `rationale` or `source` says so — never the explorer's existing "silent vanish" pattern.

**Out of Scope**:
- Per-account "library says X, analyst says Y, because…" delta decomposition (future phase, research idea 9 — consumes `generic`/`native`/`result_1gw`).
- Editing the registry from the UI.
- Family/comparables comparison entry (future phase).

**Success Criteria**:
- [x] FR-SO7: clicking the count chip for concept 01 surfaces its enabled overrides with `account`, `value`, `provenance`, `source`, `rationale` readable on the page.
- [x] The same panel opens from a ★ CAS row, a ★ treemap tile, and a ★ CapEx compare bar, scoped to that account.
- [x] Disabled overrides render distinct and tagged with `blocked_by`.
- [x] A concept with a missing `source`/`rationale` field shows an explicit "not recorded" state, not a blank/vanished panel.
- [x] `overrides` records present in the extracted JSON for all registry-bearing concepts (17 served concepts re-extracted; 37 & 39 blocked by pre-existing concept-side `model_setup.py` bugs — see below).
- [x] Existing tests pass; panel does not fetch on every render (preloaded with payload).

**Status**: ✅ Complete (implemented + browser-validated + review-hardened 2026-06-06). Panel form = **fixed drawer**; `source` = plain text (link-ification deferred). Code-review follow-ups M1/m1/m2/m3 resolved (CapEx-bar match moved to Plotly `customdata` so the trigger no longer couples the Python/JS name maps). See `.project/active/explorer-override-inspection/{design.md,spec.md}`.

**Estimated Effort**: 1.5 days (spec ~1h, design ~2h — panel form: drawer vs popover vs expand, plan ~1h, execute ~7h)

**Location**: `.project/active/explorer-override-inspection/`

**Dependencies**: Item 1 (the hero toggle + count chip is the primary trigger). Item 1's compute change and Item 2's schema emission are independent reads of the registry, so only the UI trigger creates the ordering.

**Deliverables**:
- `.project/active/explorer-override-inspection/{spec.md,design.md,plan.md}`
- Changes to `extract_explorer_data.py` + `models.py` (`OverrideRecord` schema), new inspection-panel JS, edits to `cas_breakdown.js` / treemap / CapEx compare view, `explorer.css`

---

### Follow-ups Discovered During Implementation

#### Item 1-FU1: CAS section header hint goes stale on recompute [trivial, ~0.5–1h]

**Type**: Bug fix (UI)

**Discovered**: During Item 1 (`explorer-slider-override-semantics`) browser validation, 2026-06-06.

**Symptom**: The collapsible CAS section's right-aligned **header hint** — "Total Capital: N M$" — is computed once at page load from the extraction-time applied model and never refreshed. It therefore shows the load-time value while the live state has moved: after a slider drag, after an `apply_analyst_overrides` toggle (e.g. concept 24's hint reads "872 M$" while the bare-mode breakdown is much higher), and it never reflects either. The CAS *breakdown content* (`#cas-mount`) updates correctly via `renderCASBreakdown`; only the section-header summary text is stale.

**Root cause**: `setSectionHint(sections.cas, 'Total Capital: …')` is called exactly once in `concept_page.js` init (from `concept.cost_model`). Neither `onSliderChange` nor `onModeSwitch` (nor `onReset`) re-calls it — the recompute paths update the sticky headline and the breakdown content but were never wired to refresh the header hint. **Pre-existing** (predates Item 1): slider drag already left it stale. Item 1 deliberately did **not** half-fix it on only the toggle path, because that would make the slider and toggle paths disagree about whether the hint tracks live state — worse than consistent staleness.

**Fix**: Re-call `setSectionHint(sections.cas, \`Total Capital: ${_fmtMoneyM(_sumCASCapital(newCostModel))}\`)` in **both** `onSliderChange` and `onModeSwitch` (using the compute response's cost model), and in `onReset` (using `modeBaselineCostModel`). One shared helper called from all recompute paths so sliders and toggle stay consistent. Confirm with browser-inspect: drag a slider and toggle on concept 24 → header hint tracks the breakdown total in both cases.

**Out of scope**: any redesign of the CAS section header; only the hint-refresh wiring.

**Location**: `exploration/concept_explorer/static/js/concept_page.js` (the three recompute handlers + the existing `_sumCASCapital`/`_fmtMoneyM`/`setSectionHint` helpers).

**Dependencies**: none (Item 1 landed the handlers this touches).

**Status**: ✅ Complete (implemented + browser-validated 2026-06-06). Added a shared `_refreshCASHint(costModel)` helper in `init` (hoisted function declaration, reads the same `_sumCASCapital`/`_fmtMoneyM`) and called it from `onSliderChange` and `onModeSwitch` (compute response) and `onReset` (`modeBaselineCostModel`); routed the init-time hint through it too. Verified on concept 24, console clean: toggle off 1,676→2,203 M$ (hint tracked), `vessel_t` drag 1,676→1,683 M$ (hint tracked), reset back to 1,676 M$ (hint reverted) — hint == breakdown total in every state.

#### Item 1-FU2: Audit extract-all output consistency vs isolated extraction [investigation, ~1–2h]

**Type**: Data-integrity investigation

**Discovered**: During Item 1 FR-SO1 multi-concept verification, 2026-06-06.

**Symptom**: After the Phase 2 full `extract_explorer_data.py --skip-narrative` run, `data/24.json`'s stored headline was **8.51 $/MWh**, but the concept's `model_setup.py` `result_1gw.costs.lcoe` is **16.05** — deterministic across 3 fresh processes. Re-extracting concept 24 in isolation produced the correct 16.05. An audit of all costingfe concepts found **only 24** inconsistent among *served* concepts (26 and 34 also mismatched but are omit-listed and never served; 17b errors with no `result_1gw`). The stale 24 value did not surface in browser testing because the page shows the stored headline on load and the recompute only fires on slider/toggle.

**Hypothesis (unverified)**: the full extract-all loads ~30 `model_setup.py` modules sequentially in one process and runs `model.sensitivity()` per concept; jax global/compilation state may leak across module loads, perturbing a numerically-sensitive concept (24 has pathological physics — `Q_sci = -406`). Isolated re-extraction is clean. **Not confirmed** — could equally be a pre-existing stale file the extract-all failed to overwrite.

**Action**: (1) reproduce — run extract-all then audit every costingfe concept's stored headline against a fresh isolated `result_1gw`; (2) if extract-all is the cause, isolate each concept's extraction in a subprocess or reset jax state between concepts; (3) add the headline-vs-module audit as a post-extraction integrity check so this can't silently ship again. **No impact on Item 1's shipped behavior** — the server loads modules on demand (effectively isolated) and reproduces the correct `result_1gw`; the working tree's `data/24.json` is corrected.

**Location**: `exploration/concept_explorer/extract_explorer_data.py` (extraction loop), plus a new integrity-check step.

**Dependencies**: none.

---

### Phase 2+ Vision — Orientation around the ontology

> **Status**: Vision — settled in discussion 2026-06-06, not yet decomposed into specced items. This captures the destination for everything after the Phase 1 spine. We turn these into items incrementally; the point is a coherent direction, not a commitment to build it all at once.

**The pivot (away from the research doc's economics-first Tier 2).** The research doc originally framed the landing reframe *economics-first* — an LCOE-landscape strip as the centerpiece (its ideas 4–6). **We reversed this.** The landing page's organizing principle is now the **ontology** — the design space — not cost. LCOE is demoted to a ride-along column/overlay, never the spatial driver. Rationale: under known-stale numbers, leading with cost oversells the weakest data; leading with the design space (well-grounded categorical data) gives a trustworthy first orientation and makes cost one honest attribute among many.

#### The conceptual model — three layers

Everything below hangs off this. It also answers the "two maps that overlap" worry: the landing page and the constellation are *both* about the design space, but they show different things about it.

1. **The shared spine** *(cross-cutting — infrastructure, not a page)*. One identity and one vocabulary, used on every surface:
   - **Canonical identity** — a single display name per concept **and** the concept **code (#) shown clearly**, everywhere. Today a concept carries four-plus name strings (dir slug / CSV-with-fuel-suffix / frontmatter-with-company / extracted-JSON-name / design-point plant name), and the # is almost never visible (URL + `<title>` + one muted compare label). The # becomes the stable handle *precisely because* the prose names are unreliable.
   - **One ontology facet + color vocabulary** — the dimension colors from `concept_ontology_v3.png` drive the filter chips, the matrix cells, and every legend. Set a filter once; it means the same thing on every surface. The attribute data already exists in `taxonomy_models.py` and the ontology tables, so this is UI wiring, not new extraction.
   - **One honest-caveat device** — a single reusable marker for "low grounding / single-source / archetype-fit None / field not recorded," with a plain-language hover, applied identically wherever a value appears. Missing data *says so*; it never silently vanishes.

2. **Landing = the ontology map** — *"what is each concept made of?"* The `concept_ontology_v3.png` table made live (the **living ontology matrix**). Raw per-concept attributes, filterable and re-groupable. This is where you look things up and narrow the field.

3. **Constellation = the derived-similarity map** — *"what's near what, across families?"* Stays its own page for now, but **likely rebranded** away from "taxonomy/constellation" toward its real job: **surfacing comparison candidates across families** — concepts that are physically/economically comparable even when they sit in different branches of the tree. It shows similarity *computed from* the same attributes the matrix shows raw, which the matrix itself can't display. Shared filters (layer 1) carry over from the matrix.

**The clean semantic line:** *matrix = the data (look up & filter); constellation = the computed structure over the data (see clusters, neighbors, cross-family bridges).* The family tree appears in both — as the default row-grouping on the matrix, and as navigation on the constellation page — same hierarchy, two intentional uses, not accidental duplication.

#### Navigation & page taxonomy (settled 2026-06-07)

The top banner has **four** destinations, left → right, each with one job:

1. **All Concepts** *(far left)* — the living ontology matrix (`/`, Theme B1). The raw per-concept attribute data: look up, filter, re-group. The default home and orientation surface.
2. **Design Space Viz** — the former *Taxonomy*/constellation page (Theme C1, renamed). Now that All Concepts is the better raw taxonomy view, this page's distinct job is **finding concepts to compare head-to-head based on specific computed similarities** — the cross-family comparison-candidate finder, not a redundant taxonomy browser.
3. **Compare** — curated head-to-head comparison of a hand-picked set (existing `/compare`).
4. **Cost landscape** — the LCOE comparison surface (Theme F), **separate from and after Compare**. Cost-forward *by design*: the user arrives here having explicitly asked the cost question.

This supersedes the old three-link nav (*Taxonomy / All Concepts / Compare*). **The economics-demotion decision (above) governs the *landing* surface only (#1)**; it does not constrain the dedicated Cost landscape (#4), which the home-page reframe has already freed to be cost-first. The banner reorder + the Taxonomy→Design Space Viz rename are small and ride with the next explorer item (Theme F adds the 4th entry anyway); they need not be a standalone work item.

#### Themed items (sequencing flexible; the spine underpins the rest)

**Theme A — Identity & shared spine** *(cross-cutting prerequisite)* — ✅ **DONE (2026-06-07)** — all three (A1+A2+A3) implemented on `feat/explorer-identity-spine`; **PR #58** (→ `main`). Spec/design/plan in `.project/active/explorer-identity-spine/`.
- **A1 — Canonical naming + visible concept code.** ✅ Done. `resolve_identity()` (server) + `conceptLabel()` (JS) — one canonical `Name (Fuel)` + visible `#code`, used on every naming surface (matrix row, concept header, compare columns, constellation nodes).
- **A2 — Shared facet + color vocabulary.** ✅ Done. `ontology_palette.js` exports `ontologyPalette` + `facetModel` (10 facets) + `filterState`, colored from `:root` tokens traceable to `concept_ontology_v3.png`; the single color authority both maps consume (B1 already does).
- **A3 — Honest-caveat device** (generalizes research idea 6). ✅ Done. `caveatMarker()` — one uncertainty marker (low-grounding asterisk, archetype-fit None, "not recorded"), used identically across surfaces.

**Theme B — Landing as the living ontology map** — **status: B1 ✅ done (PR #59); B2 ⬜ not started; B3 ⬜ not started.** B1 (the centerpiece) is the only Theme B item built; B2 and B3 are deferred Phase-2 follow-ups for which B1 deliberately left clean hooks (a second view-toggle slot for B2; a `project`/column extension point for B3).
- **B1 — The living ontology matrix (centerpiece).** ✅ **DONE (2026-06-07)** — implemented on `feat/explorer-ontology-matrix` (off `feat/explorer-identity-spine`); **PR #59** (→ `main`, stacks on #58); spec/design/plan in `.project/active/explorer-ontology-matrix/`. Matrix is the new home (`/`), card grid relocated to `/pipeline`. All four interactions live (filter / re-group / sort / hover), honest degradation throughout, rendered entirely through Theme A's authorities; no refetch. Rows = concepts grouped under the collapsible family tree; columns = ontology dimensions; cells = color-coded category chips (v3 palette). Interactions: **filter by clicking** a cell/chip (stack facets across columns); **re-group** rows under any column's categories (flip the organizing hierarchy live); **sort within group**; row → concept page; hover cell → value + source/caveat. Leftmost column carries the # + canonical name (A1). Dense — the whole field (~40 concepts × ~10 dimensions) on one screen, which the card grid can't do. Replaces the Approved/In-Progress pipeline split.
- **B2 — Parallel-categories "flows" lens** ⬜ **not started** *(optional secondary view toggle on the same page)*. Dimensions as axes, ribbons = concept flows, thickness = count. Answers "how do these attributes co-occur" (do all stellarators use HTS? do pulsed concepts cluster on certain drivers?). Tradeoff: individual concepts dissolve into ribbons — good for structure, bad for find-my-concept; hence secondary, not the default. *(B1 left a view-toggle slot in the controls bar for this.)*
- **B3 — Economics as ride-along** ⬜ **not started**. LCOE / confidence appear as optional matrix columns to sort/color by — present and honest, never the organizing principle. *(Explicitly excluded from B1 per FR-B1.9; B1 left a column/sort extension point.)*

**Theme C — Constellation as the cross-family comparison map**
- **C1 — Rebrand + refocus the constellation page → "Design Space Viz"** (working name, settled 2026-06-07). Its job is no longer "browse the taxonomy" (All Concepts / the matrix does that better) but **finding concepts to compare head-to-head based on specific computed similarities** — the cross-family comparison-candidate finder. Carry the shared filters (A2) so a filtered set on the matrix arrives here. Decide the cost-as-faint-tint question (lean: tint acceptable, never cost-as-position).
- **C2 — Family / comparables comparison entry** (Tier-1 idea 3): surface the already-computed `comparables` set; "Compare with its N comparables" pre-populates `/compare`; "compare this whole family" from the matrix/constellation. The explorer computes `comparables` but never reads it.

**Theme D — Provenance & maturity depth** *(concept page; continues the Phase 1 cost spine — unaffected by economics' demotion on landing)*
- **D1 — Per-account override decomposition** (Tier-1 idea 9): for each overridden CAS account, show the `generic` (library) → `native` (analyst) delta + rationale — "library says X, analyst says Y, because…". Consumes the three-forward contract; the natural successor to Items 1–2.
- **D2 — Design-point block** (Tier-3 idea 7): "what plant did we model?" — name / maturity / `P_native` / primary source, under the hero.
- **D3 — Layered maturity panel** (Tier-3 idea 8): replace the single confidence badge with data-availability rating + grounding confidence + archetype-fit grade + least-mature key-subsystem TRL — the distinct trust questions, separated.

**Theme E — Connective tissue** *(low-priority cleanup)*
- **E1 — Continuous cross-page selection**; fix the dead "Add to Comparison" button.
- **E2 — Enrich the compare picker** with LCOE / confidence / has-cost-model / ⚠.
- **E3 — Unify the two tornado implementations.**

**Theme F — Cost landscape (within- and across-family LCOE comparison)** — ✅ **DONE (merged 2026-06-08, PR #64)** *(new dedicated page, #4 in the nav)*

The realization of the J2 journey ("why is this concept's LCOE higher than its neighbors?") at both scopes — within a family and across the whole field — on a standalone, deliberately cost-forward page. Legitimately economics-first because it is a destination the user navigates to on purpose (see Navigation & page taxonomy); the economics-demotion decision constrains only the landing surface. Reads the override-registry records already extracted in Item 2 for its "why"; the Phase-1 cost spine and Theme A's identity/caveat authorities carry over.

- **F1 — LCOE landscape (stacked-bar) page.** ✅ **DONE (merged 2026-06-08, PR #64).** Spec/design/plan in `.project/active/explorer-cost-landscape/`. *Caveat: shipped before the #84 adapter migration and the #93–#95 R0-bisection regen churn — its data and decomposition want a re-verify against current `data/*.json` (see "Post-merge status" below).*
  - **Viz**: one **stacked bar per concept**; bar height = headline LCOE ($/MWh); stack segments = LCOE **decomposed by cost category**, broken out by color. Hover a segment → that category's **LCOE contribution, its % of total, and source/override notes** for the category.
  - **X-axis**: the concept **# code** (A1), with the **same caveat marker (A3)** rendered next to the code; hover the code → the full canonical name (A1).
  - **Grouping** (reuses the matrix's control idiom — Theme A2 facets): `[no grouping]`, **Family (tree)**, **Fuel**, **Driver**, **Energy Capture**, **Operation Mode**. Re-group live, as on All Concepts.
  - **Sorting**: **always by LCOE, low→high, within each group** — fixed, not user-configurable. Grouping is the variable; sort is not.
  - **"Why" affordances**: each bar **links to its concept page**; the per-segment **source/override notes** (from the Item 2 override records) carry the rationale inline.

  *Design questions (carry into decomposition):*
  - **LCOE decomposition**: LCOE is $/MWh while the CAS accounts are capital — define the decomposition of LCOE into cost-category contributions (capital-recovery / O&M / fuel / …, or CAS top-level groups) that the stack segments represent.
  - **Bare vs. applied**: does the page respect the Phase-1 `apply_analyst_overrides` state (likely a page-level toggle), and does the override-notes tooltip change with it?
  - **Category taxonomy for the stack** — which grouping of cost lines becomes the colored segments, and does it reuse the CAS-breakdown color authority.
  - **Relationship to C2 / B3**: F1 is the dedicated cost surface; C2 (comparables pre-population into `/compare`) and B3 (LCOE as a ride-along *matrix column*) remain distinct, complementary entry points — confirm no duplication at decomposition.

#### Suggested sequencing

Theme A (spine) first or concurrent with B, since both maps consume it. **Theme B is the headline reframe and the current focus.** Theme D continues the Phase-1 cost spine and can run in parallel (independent surface — the concept page). Theme C depends on A2's shared filters. Theme E is opportunistic cleanup. None of this depends on the LCOE numbers being correct — it improves the scaffolding for investigating them.

#### Branching & PR convention (settled 2026-06-07)

Each themed item **branches off the previous feature branch** (not `main`), opens **its own PR into `main`**, and the PRs are **reviewed and merged sequentially** in stack order. Stacked PRs are the expected, healthy pattern here — **do not treat stack depth as a cost** or as a reason to reorder, flatten, or otherwise pick work to minimize stacking. When a parent PR merges, the child's diff collapses to just its own commits. Concretely: #58 (Theme A) → #59 (Theme B1) → the next item branches off #59, and so on. **Pick the next item by leverage (which user journey it unblocks), never by what minimizes the stack.**

#### Open questions (carry into decomposition)

- **Canonical-name source of truth** (A1): which string wins, and is the fuel suffix / company kept? Two family notions also disagree — `ConfinementFamily` enum (MFE/IFE/MIF/NONSTANDARD; ARC is NONSTANDARD) vs. the richer ontology subfamily. Which drives matrix grouping?
- **Cost-as-tint on the constellation** (C1): faint LCOE tint acceptable, or keep cost entirely off the design-space map?
- **Constellation rebrand name** (C1): tentatively **"Design Space Viz"** (settled 2026-06-07); confirm at C1 decomposition.
- **Parcats: secondary toggle vs. its own destination** (B2) — currently scoped as a toggle.
- **Synthesis-layer coverage** (D): "What Would Change My Mind" / risk verdicts exist for only 9 concepts — surface where present (honest degradation) or defer until coverage is broader?
- **Per-concept toggle vs. session-global selection** — confirm Item 1's per-concept `apply_analyst_overrides` doesn't collide with cross-page selection (E1) in `ExplorerState`.

---

## Dependencies

**External**:
- Plotly.js, Cytoscape.js (already vendored).
- The costingfe library's `model.sensitivity(cost_overrides=...)`, `override_reference_mw`, and the three-forward `model_setup.py` shape (all in place).

**Internal**:
- `explorer-rework-unblock` (landed) — the explorer must be observably running for the discontinuity to be visible and fixable.
- The "Fix 5 concept-side model_setup.py bugs + re-extract" follow-up (BACKLOG, P1) is not blocking but improves coverage of the concepts these surfaces can demonstrate on.

**Item Dependency Graph**:
```
Item 1 (Slider/Tornado/Headline Coherence)
  └─> Item 2 (Override-Inspection Surface)   [UI trigger ordering only]
        └─> Future: per-account decomposition → family/comparables → landing reframe → …
```

---

## Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Re-applying overrides on recompute mis-scales under `n_mod ≠ 1` | Med | Pass `override_reference_mw=P_native`; verify against stored headline (FR-SO1 regression). |
| `sensitivities_applied` derived incorrectly from bare | Med | Call `model.sensitivity(cost_overrides=enabled)` honestly; never post-adjust bare (spec watch-out). |
| Uneven corpus coverage — some concepts lack rationale/source | Med | Honest degradation is a success criterion, not silent vanish. |
| Inspection panel fetches per render → jank | Low | Preload `overrides` records with the concept payload. |
| Inert "(N entries)" count reads as broken before Item 2 | Low | Style as low-emphasis label, not a button; Items 1→2 land back-to-back. |

---

## Timeline

**Phase 1 Total**: ~3–3.5 days

| Item | Effort | Dependencies |
|------|--------|--------------|
| Item 1: Slider/Tornado/Headline Coherence | 1.5–2 days | `explorer-rework-unblock` (landed) |
| Item 2: Override-Inspection Surface | 1.5 days | Item 1 (UI trigger) |

**Critical path**: Item 1 → Item 2.
**Usable checkpoint**: after Item 1, the slider triple is coherent and the toggle teaches the registry's aggregate weight — a complete win before any inspection panel exists.

---

## Lessons Learned (Post-Completion)

*Fill in after Phase 1 is complete.*

**What Went Well**: TBD
**What Could Improve**: TBD
**Surprises**: TBD

---

**Last Updated**: 2026-06-28 (**1costingfe v0.1.0 migration complete + Phase 1 verified.** Library on `1costingfe@0254385`, all explorer data regenerated, FR-SO1 holds for 33/33 served concepts. The "concept 01 override 1.26%" finding is resolved — not a regression, not a bug; the recalibration raised the baseline under a frozen-by-design override. Phase 1 + Themes A/B1/F all merged. Prior: reconciled against `main`.)
**Next Action**: **Phase 1 is done and verified — pick the next Phase-2 item by leverage.** Top candidate: **D1** (per-account override decomposition — the natural successor to Items 1–2, independent concept-page surface). Other unbuilt: **C1** (Design Space Viz rebrand + shared filters), **C2** (comparables entry), **B2/B3** (parcats lens / LCOE ride-along column), **D2/D3** (design-point block / layered maturity), **E1–E3** (cleanup). Small non-blocking loose ends from the migration: concept **27** stale data (routing-config fix), the FR-SO1 test's stale `>5%` assertion, and Item 2-FU (re-extract 37 & 39). Note: the separate `feat/explorer-web-hosting` branch (Railway/Pages deployment) is a different track, not epic work.

#### Item 2-FU: Re-extract 37 & 39 after concept-side model_setup.py fixes [blocked, trivial once unblocked]

**Discovered**: During Item 2's full re-extraction, 2026-06-06.

**Symptom**: Of the served registry-bearing concepts, **37** (`TypeError: float() argument must be a string or a real number, not 'function'`) and **39** (`routing disagreement — Comparison-Status='freeform-deferred' but model_setup.py looks costingfe-shaped`) failed extraction and kept their stale pre-Item-2 JSON (no `overrides` records). 37 therefore shows no ★ and a non-clickable "(N entries)" chip; 39 is not served (no JSON). All other 17 registry-bearing served concepts carry records.

**Root cause**: Pre-existing concept-side `model_setup.py` bugs — the same class tracked by the BACKLOG "Fix 5 concept-side model_setup.py bugs + re-extract" P1 follow-up. Not an Item 2 defect.

**Action**: After those concept-side fixes land, run `uv run python exploration/concept_explorer/extract_explorer_data.py --concept 37 39 --skip-narrative` (isolated per-concept to avoid the FU2 jax-contamination batch issue). No code change in Item 2.

**Status (re-checked 2026-06-28)**: ⬜ **Still open.** `data/37.json` and `data/39.json` both still carry **0 override records** on current `main`. The concept-side `model_setup.py` fixes have not landed (or have not been re-extracted), so this remains the one Phase-1 loose end.

---

### Post-merge status (reconciled 2026-06-28)

The epic body above was written 2026-06-06/07, while Phase 1 + Themes A/B1/F were still in-flight. They have all since **merged to `main`**:

- **Item 1, Item 2, FU1** — merged (override-overlay UX through CAS header FU1 = PR #52; built on the rework infra in #44).
- **Theme A** — PR #58 (merged 2026-06-08).
- **Theme B1** — PR #59 (merged 2026-06-08).
- **Theme F1** — PR #64 (merged 2026-06-08).

**Material churn merged on top of Phase 1 (June 15–24) that touches the cost spine:**

- **PR #84 — costingfe-adapter migration** (2026-06-15): routed `model_setup.py` forwards through `costingfe.adapter` and rewrote `model_setup_helpers.py` (owner of `enabled_overrides()` + the three-forward contract Item 1 depends on). It **broke explorer slider compute.**
- **PR #90** — "restore slider compute end-to-end after PR #84 adapter migration" (re-fixed `server.py` + `concept_page.js`, i.e. Item 1's surface).
- **PR #91** — drop deprecated `b_center`/`r_bore` kwargs before `forward()`.
- **PR #92** — unblock regen + **hide plasma-physics sliders from the tornado** (Item 1's tornado).
- **Data regen** the cost surfaces read from: #74 (source-planting), #84 (adapter regen), **#93/#94/#95 (R0-bisection projection + regen, incl. a "recovery from mis-merged stack" cleanup)**.

The Phase-1 code survived all of this (verified present on `main`: `_forward_with_overrides` + `override_reference_mw`, dual `sensitivities_bare`/`sensitivities_applied`, `OverrideRecord` + `apply_analyst_overrides`).

### 1costingfe v0.1.0 migration — ✅ COMPLETE (2026-06-28)

The library was then pulled forward to **`1costingfe@0254385` (tag v0.1.0)**, which gated off the bundled 0D physics, recalibrated every cost constant (2025 USD + net/gross reference-power unification), and renamed the package. We took **Option A** (re-enable the gates from the fusion-tea side, fix the rename, regenerate all explorer data). Full writeup: [`reports/2026-06-28_1costingfe-v0.1.0-migration.md`](../../reports/2026-06-28_1costingfe-v0.1.0-migration.md) + the forensics in `.project/research/20260628-000000_reactor-island-n_mod-replication-forensics.md`.

**Outcome — the explorer works end-to-end on v0.1.0, and Phase 1 is verified:**
- **FR-SO1 holds for all 33 served costingfe concepts** (≤0.5% no-op recompute vs stored headline); the 5 gated tokamaks (01/21/28/29/33) run again. Test suite 19/20 (the one failure is a now-stale `>5%` magnitude assertion, see below — not a product regression).
- **The "concept 01 override only moves the headline 1.26%" finding is fully resolved and is NOT a problem.** The override didn't change and didn't break: it behaves exactly as designed (`_scale_overrides` applies `value × tgt/ref`; C220103's ratio is 1.0 by that account's own scaling). The v0.1.0 **recalibration raised the bare baseline** under an override value that was always frozen-by-design, so the override's *headline* premium shrank from ~$28/MWh (~18%) to ~$1.36/MWh (1.26%). It's still ~19% at the concept's native design scale. Nothing is broken; the number is just smaller at projection scale. (The one genuine `_scale_overrides` bug in this area — library-zero accounts, [1costingfe#37](https://github.com/1cFE/1costingfe/issues/37) — is a separate case and is already fixed in the library.)

**Note on the epic's premise:** the executive summary's "~$28/MWh on concept 01" was the *pre-recalibration headline* premium; post-v0.1.0 it's ~$1.36/MWh on the headline (still large at native scale). This does **not** invalidate the toggle / provenance work — the surfaces are correct and the lesson ("what is the analyst's judgment worth") is still honest; the magnitude it reveals at projection scale is just smaller. Re-baselining that framing is optional polish, not a blocker.

**Migration loose ends (small, non-blocking):**
- Concept **27** (polywell) still serves stale data — a concept-side routing-config bug (`freeform-deferred` frontmatter on a costingfe-shaped `model_setup.py`), same class as 39's old bug. Fix the config + re-extract.
- The FR-SO1 regression test's `>5%` override-impact assertion is stale (premised on the old ~18%); relax or update it.
- Housekeeping: `spike_override_semantics.py`'s printed conclusion and the two override-policy research notes don't distinguish per-module detail lines from the rollup — worth a one-paragraph fix so the next reader doesn't chase a phantom.

**Phase 1 is done and verified. Proceed to the next Phase-2 item — no further cost-spine re-verification is needed.**
