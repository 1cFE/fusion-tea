# Design: Explorer Identity & Shared Spine (Theme A)

**Status:** Draft
**Owner:** Reid W
**Created:** 2026-06-06 15:05 PDT
**Complexity:** MEDIUM
**Branch:** feat/concept-explorer-omit-list (Theme A to branch separately)

## Overview

Give every concept one canonical `Name (Fuel)` label + a visible `#code`, sourced from the CSV that already holds both; extend the existing CSS design-token system into a full ontology color/facet vocabulary traceable to `concept_ontology_v3.png`; and consolidate the six duplicated low-grounding markers into one reusable honest-caveat component.

## Related Artifacts

- **Spec:** `.project/active/explorer-identity-spine/spec.md`
- **Epic:** `.project/backlog/epic_explorer_ux_v3.md` — "Phase 2+ Vision", Theme A
- **Research:** `.project/research/20260605-150329_concept-explorer-ux-user-journeys.md`
- **Ontology image:** `.project/research/concept_ontology_v3.png`

## Research Findings

**Two data layers, two names, one already-canonical source.**

- **Explorer layer** — `ConceptData` (`models.py:383-411`), one `data/NN.json` per served concept, built by `extract_explorer_data.py`. `name` comes from `analysis.md` frontmatter `Concept:` (`extract_explorer_data.py:445`) — the *company* form (`HTS Compact Tokamak (Commonwealth Fusion / ARC)`). **No structured `fuel` field.**
- **Taxonomy layer** — `ConceptTaxonomy` (`taxonomy_models.py:202-313`), one `concept_registry.json` for all concepts, built by `seed_registry.py`. `name` comes from CSV `Concept Name` (`seed_registry.py:101`) — already the `Name (Fuel)` form — **plus a structured `fuel: FuelType` enum** (`FUEL_MAP[row["Fuel"]]`).
- **The CSV** (`exploration/concept_analysis/table.csv`) is the authored source of truth: `Concept Name` is already `Name (Fuel)` (`HTS Compact Tokamak (D-T)`, `Laser ICF (p-B11)`), and `Fuel` is a separate structured column (`D-T`, `D-D`, `D-He3`, `p-B11`).
- **Both layers load independently** in `server.py` lifespan (`_load_data` + `_load_taxonomy`); they are **never merged**, and there is **no shared "concept label" helper** — every surface reads `.name` directly (the source of the divergence).

**Existing color system (A2 starts from here, doesn't invent).**
- `explorer.css:10-43` already has a `:root` token block: family badge colors (`--color-badge-mfe: #3b82f6` …), confidence opacity, parameter-category colors.
- Family colors are **duplicated** in JS: `constellation.js:23-35` hard-codes the same hexes as `FAMILY_COLORS`; `index_page.js:17-23` / `concept_page.js` / `taxonomy_card.js` map families to `.badge-{family}` classes.
- **Only `confinement_family` and `parameter_category` are colored today** — no per-fuel/magnet/driver colors exist.

**Existing caveat marker (A3 consolidates this).**
- `.low-grounding-marker` (`explorer.css:405-414`, amber ⚠) driven by `ConceptData.asterisk_in_comparison` (`models.py:407`), set from `comparison_status == "costingfe-asterisked"` (`extract_explorer_data.py:468`). Its tooltip already reads *"company-stated or single-source"* — so **single-source is already folded into this one signal.**
- The marker is **rendered with duplicated code + duplicated tooltip string on ~6 surfaces** (`index_page.js:103`, `concept_page.js:135`, `taxonomy_card.js:81`, `comparison.js:101`, `neighborhood_graph.js:124`, graph node styling).
- Per-concept `confidence` = mode of per-parameter confidences (`models.py:568`). **Not in explorer JSON:** `fit_grade`/archetype-fit (upstream `analysis.md` frontmatter only).
- **Silent-vanish today:** missing range → no slider/section (`parameter_card.js:191`); missing baseline → "—" (`tornado.js:485`); missing taxonomy attr → "—" `--na` (`taxonomy_card.js:108`). The pattern exists but is inconsistent and unexplained.

## Core Concept

The four-names problem isn't missing data — it's that the **canonical identity already exists in the CSV** (`Name (Fuel)` + structured fuel + code) and one layer (taxonomy) uses it while the other (explorer) substitutes an analyst-authored frontmatter name. The fix is to make the CSV the **single source of truth for identity**, resolve it **once at server load** into a small identity record per concept, stamp that record onto *both* payloads as they're served, and have **one JS helper** render `{code, name}` from it. Naming can then never diverge again because every surface reads the same resolved field through the same helper.

A2 and A3 are the same move applied to two more cross-cutting concerns: A2 promotes the existing ad-hoc color usage into **one palette + facet model** (extending the `:root` tokens already there, deleting the JS duplication), and A3 promotes the six copy-pasted markers into **one caveat component** with honest degradation. None of the three adds a new subsystem — each *consolidates a thing that's already scattered* into a single authority. That's why Theme A is "the spine": it's three single-source-of-truth conversions, not three features.

## Key Bets & Decisions

### Decision 1 — Where canonical identity is resolved *(needs your call)*

The CSV name already equals `Name (Fuel)`; the question is where the explorer layer adopts it.

- **Option A — Extract-time.** Change `extract_explorer_data.py:445` to read the name from the CSV (keyed by `concept_id`) instead of frontmatter. *Pro:* `data/NN.json` becomes correct on disk. *Con:* requires re-extracting all served concepts (and the FU2 jax-contamination batch risk from the epic); two builders (extractor + registry) must both read the CSV.
- **Option B — Server-load overlay (recommended).** Keep the JSON as-is; add one server-side `resolve_identity(concept_id) → {code, name, fuel}` that reads the registry (already CSV-sourced) and stamp `name`/`code`/`fuel` onto the served `ConceptData` and `ConceptTaxonomy` at load. *Pro:* one resolution point in code; no re-extraction; the registry is already built from the CSV so identity is consistent by construction. *Con:* the persisted `data/NN.json` keeps its old `name` (cosmetic — never read raw by the UI once the overlay is in).

**Recommendation: Option B.** It centralizes identity in one function, avoids touching 40 JSON files and the batch-extraction risk, and leans on the registry as the existing CSV mirror. The frontmatter `Concept:` name is retained in the payload as a secondary field if any page wants the analyst's phrasing.

### Decision 2 — How much extraction A3 pulls in *(needs your call)*

The spec's caveat dimensions are low-grounding, single-source, archetype-fit None, field-not-recorded. Mapping to data:
- low-grounding **and** single-source → already the one `asterisk_in_comparison` signal (its tooltip says both). ✓ available.
- field-not-recorded → a UI pattern (honest "—/not recorded"). ✓ no data needed.
- archetype-fit None → needs `fit_grade`, which is **not** in the explorer JSON (frontmatter only).

- **Option A — Minimal (recommended).** Add one field, `fit_grade`, to `ConceptData` from `analysis.md` frontmatter (a single read, like `Concept`/`Company` already are). Build the caveat component to show {low-grounding/single-source via asterisk, archetype-fit via fit_grade, not-recorded via the honest-absence pattern}. Cheap; satisfies FR-A3.2.
- **Option B — Full.** Also extract per-parameter grounding and an explicit single-source flag. Heavier extractor work; single-source is redundant with the asterisk; defer.

**Recommendation: Option A.** One frontmatter field + the component. Fold single-source into the existing asterisk semantics (note this reconciliation in the tooltip copy).

### Bet 3 — A2's visible footprint in Theme A is deliberately small

Family + constellation are *already* family-colored, so A2's job here is to (a) define the **full ontology dimension → color token set** (extending `:root`) traceable to the PNG, (b) **delete the JS color duplication** so family colors flow from one source, and (c) define the **facet + filter-state model** as importable data. The new per-dimension colors have no on-screen home until B1's matrix — so Theme A's *visible* wins are A1 (names/codes) and A3 (caveats); A2 is groundwork that ships invisibly correct. We accept that rather than inventing a throwaway surface to display fuel colors early.

### Decision 4 — One work item or split *(your call; recommend one)*

A1/A2/A3 share the same ~6 render sites and the same "single authority" philosophy. Recommend **one work item, planned in three slices** (A1 identity → A3 caveat → A2 palette/facets) so each lands and is verifiable on its own.

## Architecture

**Identity (A1).** New server-side identity resolution sits between the two loaders and the route handlers:

```
table.csv ──seed_registry──▶ concept_registry.json ──┐
                                                      ▼
analysis.md ──extract──▶ data/NN.json ──▶ resolve_identity(id) ─▶ {code, name, fuel}
                                                      │   (reads registry; CSV is source of truth)
                                                      ▼
                              stamped onto served ConceptData + ConceptTaxonomy
                                                      ▼
                              JS conceptLabel(payload) → renders "#NN  Name (Fuel)"
```

**Color/facets (A2).** One palette module is the authority; CSS and JS both consume it:

```
ontology palette (CSS :root tokens, traceable to v3 PNG)
   ├─ CSS .badge-* / dimension classes  (existing family badges re-sourced)
   └─ shared JS color map (constellation + future matrix import; JS dup deleted)
facet model (dimensions + value→{label,color}) ─┐
filter-state model (selected facets schema)     ┴─ exported for B1/C1 (no widget here)
```

**Caveat (A3).** One component replaces six call sites:

```
caveat inputs: {asterisk_in_comparison, fit_grade, <field-present?>}
   └─ caveatMarker(inputs) → consistent glyph + plain-language hover
       rendered at the same 6 surfaces, plus the honest-absence variant
```

## Required Invariants

- Every surface that names a concept renders it through `conceptLabel()` — no surface reads `.name` directly. (Grep guard: a test asserts no remaining direct `.name` label renders in the touched files.)
- `resolve_identity()` returns a value for every *served* concept; a served concept absent from the registry degrades to its stored name + code, honestly (never throws, never blank).
- Family colors have exactly one definition; `constellation.js` no longer hard-codes hexes.
- The caveat component is the only place the ⚠/absence markup is authored; the six sites call it.
- Missing fields surface via the caveat/absence pattern — they never silently vanish (carried from Phase 1).

## Component Overview

- **`resolve_identity(concept_id)`** (server.py) — returns `{code, name, fuel}` from the registry; the single identity authority. Stamps both payloads at load.
- **`conceptLabel(conceptLike)`** (new small JS module) — returns `{code, name}` and/or renders the `#NN Name (Fuel)` element; imported by every naming surface.
- **Ontology palette** — extended `:root` tokens in `explorer.css` + one shared JS color map (`ontology_palette.js` or similar) replacing `constellation.js`'s `FAMILY_COLORS`.
- **Facet + filter-state model** (new JS/Python shared data) — the list of facetable dimensions with value→{label,color}, and the selected-facets schema. Exported, unconsumed-by-widget in Theme A.
- **`caveatMarker(inputs)`** (new JS module) — the one caveat component; `fit_grade` newly added to `ConceptData`.

## Non-Goals

- The ontology matrix (B1), constellation rebrand (C1), parcats (B2), filter widget — Theme A is their spine.
- The design-point/plant name (Theme D2) — not part of identity.
- Editing `analysis.md` / CSV content; we reconcile at the explorer's data/render layer.
- A layered maturity panel (Theme D3) — A3 is one marker, not the full maturity surface.

## Implementation Notes

- **Fuel-missing / `N/A`:** some concepts may have no fuel or `N/A` in the CSV — render the base name with no `(Fuel)` parenthetical; never `(None)`. The CSV name already omits the suffix in those rows, so adopting the CSV name handles this for free under Option B.
- **Suffix variants** (`17a`, `20b`): `concept_id` already carries the letter; `code` = `concept_id`. No special-casing beyond display.
- **PNG palette extraction** is a small real task (the PNG is an image) — sample its cell colors into documented hex tokens; this is plan/impl work, not design.
- **Family color key:** the palette's family colors key off the `ConfinementFamily` enum (what's rendered today); the richer ontology subfamily is a *separate* facet, not the family color — avoids the enum-vs-subfamily disagreement noted in the epic.
- **Don't let A2.3 drift:** "apply colors to existing surfaces" means *re-source* the family colors from the token authority, not build new colored surfaces.

## Potential Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Server-overlay leaves stale `name` in `data/NN.json`, confusing future readers | Low | Doc-comment the overlay; the JSON `name` is explicitly "raw analyst phrasing, not the display name". |
| A registry/CSV name *isn't* clean `Name (Fuel)` for some row | Med | Audit all rows during impl; honest fallback to the row's name as-authored. |
| Consolidating 6 caveat sites regresses one surface's markup | Med | One component, snapshot/visual check each site via browser-inspect (Phase-1 practice). |
| A2 ships invisibly → reads as "did nothing" | Low | Frame in the plan as groundwork; the verifiable output is the token authority + deleted duplication, not a pixel change. |

## Integration Strategy

Replaces: the per-surface `.name` reads, the `constellation.js` `FAMILY_COLORS` duplication, and the six copy-pasted low-grounding markers. Complements: the existing `:root` token system (extended, not replaced) and the existing `asterisk_in_comparison` signal (reused, not re-derived). Sets up: B1's matrix and C1's constellation, which import the facet model, palette, `conceptLabel()`, and `caveatMarker()` directly.

## Validation Approach

- **A1:** for 01 / 24 / 17a (and a fuel-`N/A` concept), assert identical `#NN Name (Fuel)` on landing, concept, compare, constellation (browser-inspect); unit test `resolve_identity` for normal / suffix-variant / fuel-missing / not-in-registry.
- **A2:** assert one color authority (grep: no hard-coded family hexes left in JS); palette↔PNG mapping documented; family badges/constellation visually unchanged.
- **A3:** the same component renders on all four surface types; an absent field shows an explicit "not recorded" rather than vanishing; `fit_grade` present in re-extracted/​overlaid payload.
- Existing test suite passes; new tests for the helper and identity resolution.

## Next-Stage Handoff

**Fixed:** canonical name = CSV `Name (Fuel)`; one identity authority + one render helper; extend (not replace) the `:root` tokens; one caveat component folding single-source into the asterisk; honest degradation mandatory.

**Settled (2026-06-06):** D1 = **Option B, server-load overlay**; D2 = **Option A, minimal `fit_grade` add** (single-source folded into the existing asterisk); D4 = **one work item, three slices** (A1 identity → A3 caveat → A2 palette/facets).

**De-risk first:** audit that every served concept's CSV/registry name is clean `Name (Fuel)` (Decision-1 correctness rests on it) before wiring surfaces.

---
Next Step: After you confirm Decisions 1, 2, 4 → `/_my_plan`.
