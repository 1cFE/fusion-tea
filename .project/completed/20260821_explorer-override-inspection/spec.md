# Spec: Override-Inspection Surface

**Status:** Implemented (2026-06-06)
**Owner:** Reid W
**Created:** 2026-06-06 12:46 PDT
**Complexity:** MEDIUM
**Branch:** feat/concept-explorer-omit-list
**Epic:** EXPLORER-UX-V3 (Phase 1, Item 2) — `.project/backlog/epic_explorer_ux_v3.md`
**Depends on:** Item 1 (`explorer-slider-override-semantics`) — landed; ships the hero checkbox and the "(N entries)" count this item makes clickable.

---

## Work Item Summary

When the analyst changes a cost number in a concept's model, the explorer marks it with a ★ and nothing else — you can see *that* a number was changed, but not what it was, what it became, or why. The full reasoning exists, but only in the concept's `model_setup.py` file, which nobody opens while using the explorer.

This item brings that reasoning into the page. It does two things: (1) carry the full content of each override through to the explorer's data, instead of only counting the overrides, and (2) add a panel that shows that content — opened by clicking a ★ next to a changed cost line, or by clicking the "(N entries)" text next to the hero checkbox. "Done" means a user can click any ★ and read what the analyst changed, to what, and why, without leaving the page.

## Why This Matters Now

The whole point of the analysis rework was to make every cost change one accountable, sourced, written-down decision instead of a magic number buried in code. The explorer currently undoes that: it takes all of that reasoning and throws it away at the data step, surfacing it as a single ★. Under data we already know is provisional, the analyst's reasoning *is* the product — it's the thing that lets someone judge whether a number is trustworthy. Right now it's the one layer the explorer drops.

Item 1 already made the aggregate honest (the hero checkbox shows "(N entries)" and lets you toggle the overrides on and off). This item makes the individual reasoning readable, which is the other half of the same idea.

## Key Bets / Constraints

- **Bet:** The data is already correct and already being read. The fix is to stop discarding it — carry each entry's content through and show it. No change to the source `model_setup.py` files.
- **Constraint:** The panel must use data that loads with the concept page. It must not fetch from the server every time someone clicks a ★.
- **Constraint:** An override's `value` is recorded at the concept's *native* per-module scale, which is not the same scale the cost tables display (those are at the standardized 1 GWe projection). The panel must label the value's scale so the two numbers don't look like a contradiction.
- **Non-goal:** A "library said X, analyst said Y, and here's the difference" side-by-side. That's a later phase.
- **Non-goal:** Editing overrides from the UI. The overrides are analyst-authored and version-controlled; the explorer only reads them.
- **Non-goal:** Any landing-page, family, or comparables work.

---

## Business Goals

### Why This Matters

A researcher using the explorer to sanity-check or debug a number needs to see the analyst's reasoning, not just a marker that reasoning happened. Today that means leaving the tool and reading code — at which point the explorer added nothing. Making the reasoning one click away is what turns the explorer into a place you can actually interrogate a number.

### Success Criteria

- [x] A user can click a ★ on a changed cost line and read that override's account, value, source, and reasoning, on the page.
- [x] A user can click the "(N entries)" text in the hero and see all of the concept's overrides in one place.
- [x] Overrides the analyst worked out but chose not to apply are visible too, clearly marked as not applied, with the reason.
- [x] Where a piece of an override wasn't recorded, the panel says so plainly instead of showing a blank or hiding the entry.

### Priority

P1. Second item in EXPLORER-UX-V3 Phase 1, directly after Item 1 (whose checkbox and count are this item's main entry point).

---

## Problem Statement

### Current State

- Each concept's `model_setup.py` has an `overrides` list. Each entry records one cost change with: `account` (the CAS code), `value` (the number, at native per-module scale), `enabled` (whether it's actually applied), `provenance` ("direct" or "derived"), `source` (a citation), `rationale` (the written reasoning), `cost_basis`, and — on entries the analyst chose not to apply — `blocked_by` (a pointer to the open question that's holding them back).
- The explorer's extractor (`extract_explorer_data.py`) already imports that module and reads the `overrides` list, but only to count the applied entries (`analyst_override_count`). The per-entry content is dropped — the explorer's data format (`ConceptData` in `models.py`) has no field to hold it.
- In the UI, the content reaches the front-end as one bit per account: a ★ (`cas_breakdown.js`, `view_capex.js`). The ★ has no "why."

### Desired Outcome

- The explorer's data carries the full content of every override entry, loaded with the concept payload.
- A reusable panel shows that content. It opens from a ★ on a changed cost line (focused on that one account) or from the hero's "(N entries)" text (showing all of the concept's overrides).
- Entries the analyst chose not to apply show up too, marked as not applied, with the reason they're on hold.

---

## Scope

### In Scope

1. **Data:** Add a place in the explorer's data format (`models.py`) to hold the override records, and a step in the extractor (`extract_explorer_data.py`) that copies each entry's full content into it. Read from the `overrides` list already loaded from each concept's `model_setup.py`. Loaded with the concept payload — never fetched per click.
2. **Panel:** One reusable panel that displays, per override: the account code plus its human-readable name (e.g. "C220103 — Magnets / Coils"), the value with its scale labeled, the provenance, the source, and the reasoning.
3. **Not-applied entries:** Overrides with `enabled: false` are shown in the panel, visually distinct (greyed/struck), marked as not applied, and showing their `blocked_by` reference.
4. **Trigger sites:** Make the hero's "(N entries)" text clickable (opens the panel with all of the concept's overrides). Make the ★ clickable on the cost-breakdown rows, the treemap tiles, and the CapEx comparison bars (opens the panel focused on that one account).
5. **Missing fields:** If an override is missing a field, the panel says so explicitly ("not recorded") rather than hiding it or showing a blank.

### Out of Scope

- "Library said X, analyst said Y, here's the gap" per-account comparison (later phase).
- Editing overrides from the UI.
- Landing-page / family / comparables work.

### Edge Cases & Considerations

- A concept with no overrides: no ★, no clickable count (Item 1 already hides/disables the checkbox here). The panel never opens.
- An override's `value` is at native per-module scale; the cost tables show the standardized 1 GWe scale. The two numbers will differ for the same account — the panel must label the scale so this reads as "different views of the same thing," not a bug.
- Not-applied entries leave the library's default in the cost table, so those cost lines carry **no ★**. The only way to reach a not-applied entry is the hero "(N entries)" panel (the all-overrides view). The per-line ★ only ever shows applied entries.
- The CapEx comparison bars live on a *different* page (`/compare`) that loads several concepts at once. Reusing the panel there depends on each concept's override records being available in that page's data — see watch-outs.

---

## Requirement Selection Notes

The normative requirements below cover what must be true for this item to be done: the data carried through, the panel content, the trigger sites, the not-applied display, and honest handling of missing fields. The *form* of the panel (drawer vs popover vs inline expand) and the exact wording/styling are left to design — they don't change what the item is.

---

## Requirements

### Functional Requirements

1. **FR-1**: The explorer's extracted data SHALL include, for every concept with an override registry, the full content of each entry in that concept's `overrides` list: `account`, `value`, `enabled`, `provenance`, `source`, `rationale`, `cost_basis`, and `blocked_by` (when present). The records SHALL be read from the `overrides` list already loaded from the concept's `model_setup.py` and SHALL be loaded with the concept payload (not fetched per render).
2. **FR-2**: Clicking the hero's "(N entries)" count SHALL open a panel listing all of that concept's overrides.
3. **FR-3**: Clicking a ★ on a cost-breakdown row, a treemap tile, or a CapEx comparison bar SHALL open the same panel, focused on the override for that one account.
4. **FR-4**: For each override, the panel SHALL show the account code and its human-readable name, the `value` with its scale labeled, the `provenance`, the `source`, and the `rationale`.
5. **FR-5**: Overrides with `enabled: false` SHALL be shown in the panel, visually distinct from applied ones, marked as not applied, and showing their `blocked_by` reference.
6. **FR-6**: When an override is missing a field the panel would otherwise show, the panel SHALL state that the field was not recorded — it SHALL NOT hide the entry or render a blank.

### Non-Functional Requirements

- The panel SHALL NOT trigger a server fetch on each render or each open; its data rides the concept payload.

---

## Acceptance Criteria

### Core Functionality

- [x] FR-1: the extracted JSON for concept 01 contains its override records (account, value, source, rationale, etc.), including the not-applied CAS27 entry.
- [x] FR-2: clicking "(N entries)" on concept 01 opens a panel showing its overrides.
- [x] FR-3: the same panel opens from a ★ cost-breakdown row, a ★ treemap tile, and a ★ CapEx comparison bar, focused on the clicked account.
- [x] FR-4: each override in the panel shows account + name, value (with scale labeled), provenance, source, and rationale.
- [x] FR-5: concept 01's not-applied CAS27 override renders visually distinct, marked not applied, with its `blocked_by` reference.
- [x] FR-6: an override with a missing field shows an explicit "not recorded" state, not a blank or a vanished entry.

### Quality & Integration

- [x] Existing test suite passes (234 passed, 2 skipped; 6 pre-existing `test_extract_adapter` failures unrelated, confirmed pre-existing).
- [x] The panel does not fetch on render/open (records preloaded with the payload).

---

## Next-Stage Handoff

**Settled in this spec:**
- The data source is the existing `overrides` list in each concept's `model_setup.py`; no source-data change.
- The two trigger types: hero count → all overrides; ★ → one account.
- Not-applied overrides are included, marked, and only reachable from the hero count panel.
- The value must be shown with its scale labeled.

**Design must figure out:**
- The panel's form: drawer, popover, or inline expand.
- Exact layout, wording, and styling (including the not-applied and "not recorded" treatments).
- How the same panel component is reused on the concept page and the `/compare` page.
- The account-code → human-name lookup on the front-end (the maps exist in `models.py` as `CAS_NAMES` / `CAS22_NAMES`; decide whether to emit the name with the record or mirror the map in JS).
- Whether `source` renders as a link (depends on whether it's a path, DOI, or free text).

**Watch-outs for design:**
- The `/compare` page loads several concepts and may not currently carry each concept's full override records. Wiring the CapEx-bar trigger there is likely the heaviest part of this item — confirm the data is available before assuming the panel just drops in.
- Value scale: the override `value` is native per-module M$; the cost tables are at the 1 GWe projection. Label the scale or the panel will look like it contradicts the table.
- Don't copy the explorer's existing "silent degradation" habit (whiskers vanish, sliders show "—"). Missing fields must say so (FR-6).

---

## Related Artifacts

- **Epic:** `.project/backlog/epic_explorer_ux_v3.md` — EXPLORER-UX-V3, Phase 1, Item 2.
- **Predecessor (Item 1):** `.project/active/explorer-slider-override-semantics/` — ships the hero checkbox and "(N entries)" count.
- **Research:** `.project/research/20260605-150329_concept-explorer-ux-user-journeys.md`.
- **Override registry shape:** `exploration/concept_analysis/scripts/lib/model_setup_helpers.py:46-83` (`Override` fields, `enabled_overrides`).
- **Where the count is read today:** `exploration/concept_explorer/extract_explorer_data.py:380,426`.
- **Where the ★ is rendered:** `exploration/concept_explorer/static/js/cas_breakdown.js:277` (rows/treemap), `exploration/concept_explorer/static/js/view_capex.js:208` (compare bars).
- **A real not-applied override:** `exploration/concept_analysis/analyses/01-hts-compact-tokamak/model_setup.py:101-120` (CAS27).

**Next Steps:** After approval, proceed to `/_my_design`.
