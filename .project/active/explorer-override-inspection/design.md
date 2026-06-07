# Design: Override-Inspection Surface

**Status:** Implemented (2026-06-06)
**Owner:** Reid W
**Created:** 2026-06-06 12:53 PDT
**Branch:** feat/concept-explorer-omit-list
**Commit:** 1c7e1f53
**Epic:** EXPLORER-UX-V3 (Phase 1, Item 2)

> **Implementation note (2026-06-06):** Built as designed. Open decisions resolved
> in favor of the recommendations: **Decision 1 = fixed drawer**, **Decision 3 =
> `source` as plain text** (link-ification deferred). One change vs the design's
> first pass came out of code review: the `/compare` CapEx-bar trigger matches the
> clicked account by a **CAS code carried in Plotly `customdata`**, not by the
> display-name string — this removes the Python/JS name-map coupling the design's
> watch-out flagged (matching is code-based; the panel's `account_name` display
> still uses the single Python source, so INV-4 holds). Files touched:
> `models.py`, `extract_explorer_data.py`, `override_panel.js` (new),
> `cas_breakdown.js`, `concept_page.js`, `view_capex.js`, `explorer.css`,
> `concept.html.j2`, `compare.html.j2`, `test_extraction.py` (+5 tests), and a
> re-extraction of 17 registry-bearing concepts. Validated end-to-end with
> browser-inspect (console clean across all triggers).

---

## Overview

Carry each concept's full override registry through to the explorer payload, and surface it as one reusable inspection panel opened from any ★ (CAS rows, treemap tiles, CapEx compare bars) or from the hero's "(N entries)" count — so a researcher can read *what* the analyst changed, *to what*, and *why*, without leaving the page.

## Related Artifacts

- **Spec:** `.project/active/explorer-override-inspection/spec.md`
- **Epic:** `.project/backlog/epic_explorer_ux_v3.md` (Item 2)
- **Predecessor (Item 1):** `.project/active/explorer-slider-override-semantics/` — ships the hero toggle + inert "(N entries)" count this item makes clickable.
- **Research:** `.project/research/20260605-150329_concept-explorer-ux-user-journeys.md` (J3 provenance journey)
- **Registry shape:** `exploration/concept_analysis/scripts/lib/model_setup_helpers.py:46-83` (`Override` TypedDict)

## Research Findings

**Data already loads; only the carry-through is missing.** The extractor already imports each `model_setup.py` and reads its `overrides` list — but only to count enabled entries (`extract_explorer_data.py:380,426` → `analyst_override_count`). The per-entry content is dropped at `ConceptData` construction. No new IO is needed; we copy from a list already in hand.

**Both pages use the same payload route.** `concept_page.js:345` and `comparison.js:141` (`fetchConcept`) both hit `/api/concepts/{id}`, which returns the full `ConceptData` (`server.py:434`). **Adding `overrides` to `ConceptData` makes it available on the concept page *and* the `/compare` page with no extra wiring** — the spec's heaviest watch-out (compare may not carry the records) does not hold. `view_capex.js` already reads `concept.data.cost_model`; it will see `concept.data.overrides` for free.

**An established panel pattern exists.** `parameter_card.js` is a self-contained dismissible popover: module-level singleton (one at a time), `show…`/`hide…`, dismiss on Escape + outside-click, omit-when-absent field rendering (`:221` omits source when missing). It is the template for this item's lifecycle — the open question is only whether to *anchor* (popover) or *fix* (drawer) the panel.

**The ★ trigger surfaces are heterogeneous and partly unwired:**
- CAS **table top-level rows** already accept `onAccountClick(casKey, account)` (`cas_breakdown.js:270-272`) — but `concept_page.js` currently passes no callback, so they are inert today.
- CAS **table CAS22 sub-rows** have **no** click handler (`:288-304`) — they only render the ★.
- **Treemap top-level tiles** accept `onAccountClick` (`:395-397`), but only when *not* drilled in.
- **Treemap drilled-in CAS22 sub-tiles** have **no** click handler (the `else if` requires `drilledInto === null`, `:395`).
- **CapEx compare bars** are Plotly traces; the ★ lives only in hovertext (`view_capex.js:208,222`). No DOM element per account — a click needs a `plotly_click` handler mapping `curveNumber`→concept and `y`-label→account.

**This matters for concept 01 specifically.** Its one *enabled* override is `C220103` — a **CAS22 sub-account**, exactly the surface with no current click handler. Its *disabled* override is `CAS27` (top-level). So the acceptance demo (FR-3 on concept 01) exercises precisely the sub-row/sub-tile wiring gap. The design must close it.

**Account-code casing.** Override `account` fields are `"C220103"` (sub, matches `CAS22_NAMES`) and `"CAS27"` (top-level). The CAS table's top-level keys are lowercase (`"cas27"`). Matching an override record to a clicked account needs case-normalization for top-level codes.

## Core Concept

**One payload field, one panel module, four thin triggers.** The override registry is already evaluated and already loaded — the fix is to stop discarding it at the `ConceptData` boundary (`overrides: list[OverrideRecord]`) and render it through a single surface-agnostic panel. Every existing ★ and the hero count become trigger sites that call the same `showOverridePanel(...)`; the panel itself knows nothing about *where* it was opened from — only which records to show and which one to focus.

The key insight: because the panel must serve four structurally different trigger surfaces (DOM table rows, SVG treemap tiles, a Plotly canvas, and a plain text chip) across two pages, the panel must **not depend on its anchor**. A fixed-position drawer is the form that renders identically from all four without per-surface positioning math — which is why it beats the popover pattern here despite the popover being the closer-to-hand precedent.

## Key Bets & Decisions

### Decision 1 — Panel form: fixed drawer (recommend) vs anchored popover **[needs user sign-off]**

The spec defers the form (drawer / popover / inline expand) to design. Inline expand is rejected outright: it cannot serve the hero "all overrides" view, Plotly bars, or SVG tiles, so it breaks the "one reusable panel" requirement.

That leaves:

- **(A) Fixed drawer** — a right-side slide-in panel, fixed position, not anchored to the trigger. Singleton + Escape/outside-click/close-button dismiss (lifecycle mirrors `parameter_card.js`). One `showOverridePanel({records, focusAccount, conceptName})`.
  - *Pros:* renders identically from all four triggers and both pages with zero anchoring math; the awkward cases (Plotly canvas, SVG tiles, long all-overrides list) cost nothing; reads as a deliberate "inspection surface"; comfortably holds multi-paragraph `rationale`.
  - *Cons:* new component + ~40 lines of CSS (slide/overlay); more screen real estate than a popover.

- **(B) Anchored popover** — extend the `parameter_card.js` pattern: anchor near the clicked element, fall back left/right to avoid viewport clip.
  - *Pros:* reuses an existing, proven pattern; least new CSS; contextual to the click.
  - *Cons:* anchoring math must handle four anchor types — including a Plotly click (anchor to cursor coords via the DOM `MouseEvent`) and SVG tiles; a long all-overrides list plus a multi-paragraph `rationale` strains a popover; positioning near edge bars on `/compare` is fiddly.

**Recommendation: (A) fixed drawer.** The reuse-across-four-surfaces requirement is the whole point of the item, and a non-anchored panel is the only form that satisfies it cleanly. The popover saves CSS but spends it back on per-surface anchoring and content-overflow handling.

### Decision 2 — Emit the human-readable name with each record (not a JS reverse-map)

`CAS_NAMES`/`CAS22_NAMES` exist in **both** `models.py` (`:155,175`) and JS (`cas_breakdown.js:41,61`), but the JS top-level keys are lowercase while override codes are upper/`C…`. Rather than add a normalizing reverse-lookup in JS, emit `account_name` on each `OverrideRecord` at extraction time, resolved from the `models.py` maps (single source of truth). The panel renders `account` + `account_name` directly. Unknown codes fall back to the bare code.

### Decision 3 — Render `source` as plain text now (link-ification deferred)

Real sources are free-text citations ("arc-reactor-specifications.md §6 Table 11 (Sorbom et al. 2015) + …"), not resolvable URLs/paths/DOIs. Render as text. The spec's "decide whether source renders as a link" resolves to *no* for this item; a later phase can parse citation shapes. **Asking the user to confirm this deferral** (it's a stated open question, and silently dropping a link affordance would violate the "ask when skipping a spec item" rule).

### Decision 4 — `cas_breakdown` gains an override-specific callback, gated on `overridden`

Rather than repurpose the generic, currently-unused `onAccountClick` (which fires for *any* account and would make non-overridden rows falsely interactive), add `onOverrideClick(accountCode)` fired **only** for accounts where `overridden === true`. Wire it across all four interior surfaces: top-level rows, CAS22 sub-rows, top-level tiles, drilled-in sub-tiles. The ★ glyph (table) / the overridden tile (treemap) is the click target and gets the `is-clickable` affordance. This keeps `cas_breakdown` agnostic about override *content* — it just reports "the ★ for code X was clicked."

## Architecture

```
extract_explorer_data.py ──reads module.overrides──▶ list[OverrideRecord]
        │                                                   │
        ▼                                                   ▼
   ConceptData.overrides  ──serialized to data/{id}.json──▶ /api/concepts/{id}
        │                                                   │
        ├──────────────── concept_page.js ─────────┐        ├── comparison.js
        │                                           │        │
   hero "(N entries)" chip          cas_breakdown.js onOverrideClick   view_capex.js plotly_click
        │                                           │        │
        └──────────── showOverridePanel({records, focusAccount, conceptName}) ◀──────┘
                                   (override_panel.js — singleton drawer)
```

**Data flow:** records ride the concept payload (loaded once per concept) → all triggers read from the in-memory `concept.overrides` / `concept.data.overrides`. No trigger fetches. The panel is pure render: given `records` and an optional `focusAccount`, it filters/orders and draws.

**Focus semantics:** a ★ trigger passes `focusAccount = <code>`; the panel shows that one record (matched case-insensitively for top-level codes). The hero chip passes no focus; the panel shows all records — enabled first, then disabled (visually distinct, with `blocked_by`).

## Required Invariants

- **INV-1 (no fetch):** the panel reads only the already-loaded concept payload; opening it issues no network request.
- **INV-2 (★ ⇒ enabled):** a per-line ★ only ever exists for an *enabled* override (not-applied entries leave the library default, so no ★). Disabled entries are reachable **only** via the hero chip. The focus lookup therefore always resolves to an enabled record.
- **INV-3 (honest degradation):** a missing field renders an explicit "not recorded" marker — never a blank, never a hidden entry (FR-6). Mirrors `parameter_card.js`'s discipline but inverts the "omit when absent" choice, per the spec watch-out against silent degradation.
- **INV-4 (single source of names):** `account_name` derives from the `models.py` CAS maps at extraction; the panel never re-derives account semantics.
- **INV-5 (one panel):** at most one panel open at a time (singleton), dismissed by Escape, outside-click, or close button.

## Component Overview

- **`OverrideRecord` (models.py, new):** Pydantic model — `account`, `account_name`, `value`, `enabled`, `provenance`, `source`, `rationale`, `cost_basis`, `blocked_by: str | None = None`. Optional/absent narrative fields typed `str | None` so "not recorded" is representable (don't coerce to `""`).
- **`ConceptData.overrides` (models.py):** `list[OverrideRecord] = Field(default_factory=list)`. Empty for freeform/empty-registry concepts.
- **Extractor step (extract_explorer_data.py):** build the records from `module.overrides` (the same list already read for the count), attach `account_name` from the CAS maps, pass into `ConceptData(...)` alongside the existing `analyst_override_count`.
- **`override_panel.js` (new):** the drawer module — `showOverridePanel({records, focusAccount, conceptName})`, `hideOverridePanel()`, singleton + dismiss lifecycle, "not recorded" rendering, enabled/disabled styling. Page-agnostic (loaded on both concept and compare pages).
- **`cas_breakdown.js` (edit):** add `onOverrideClick` callback; wire it on top-level rows, CAS22 sub-rows, top-level tiles, and drilled-in sub-tiles, gated on `overridden`.
- **`concept_page.js` (edit):** pass `onOverrideClick` into `renderCASBreakdown`; make the hero chip clickable (open panel with all records). The chip lives in `mountOverrideToggle` (`:181`); the count `<span>` becomes the trigger.
- **`view_capex.js` (edit):** add a `plotly_click` handler mapping `curveNumber`→concept and `y`-label→account code (reverse `CAS_NAMES`/`CAS22_NAMES`), open the panel focused on that concept's record.
- **`explorer.css` (edit):** drawer + overlay styles, enabled/disabled (grey/strike) treatment, "not recorded" marker.

## Non-Goals

- Per-account "library said X, analyst said Y, here's the gap" delta decomposition (future phase, idea 9).
- Editing overrides from the UI.
- Family/comparables work; landing-page reframe.
- Link-ifying `source` (Decision 3 — deferred).
- Re-deriving or changing `analyst_override_count` (Item 1 owns it; this item adds records alongside it).

## Implementation Notes

- **Scale label (spec constraint):** the `value` is **native per-module M\$**; the cost tables are the **1 GWe projection**. The panel must label the value's scale explicitly (e.g. "1030 M\$ · native per-module scale") so it doesn't read as contradicting the table. This is a fixed string the panel always shows next to `value`.
- **`blocked_by`** is required iff `enabled is False` (`model_setup_helpers.py:71`); render it only on disabled entries.
- **CAS22 sub-row/sub-tile wiring is the real work in `cas_breakdown.js`** — concept 01's enabled override is exactly there. Don't ship without exercising it.
- **Plotly mapping is the heaviest single piece** — `plotly_click` gives `points[].curveNumber` (concept order) and `points[].y` (account display name). Reverse-map the name to a code; if `showSubAccounts` is on, the name is a CAS22 name. Guard for the not-overridden case (no-op).
- **`OverrideRecord` field types:** keep `value: float`; `source`/`rationale`/`cost_basis`/`blocked_by` as `str | None`. The extractor should pass `None` (not `""`) for a genuinely-absent field so INV-3 can distinguish "not recorded" from "recorded empty".
- Match the file's existing prose/JSDoc conventions; no hard-wrapping in the design or code comments per project convention.

## Potential Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Sub-row/sub-tile wiring missed → concept 01's ★ inert | High (breaks FR-3 demo) | Wire all four surfaces; acceptance test clicks the C220103 sub-row + drilled sub-tile. |
| Plotly click maps to wrong concept/account | Med | Map by `curveNumber` + reverse name lookup; unit-cover the name→code map; no-op when not overridden. |
| Multi-paragraph `rationale` overflows panel | Low | Drawer with internal scroll + max-height (Decision 1 removes the popover overflow risk). |
| `account_name` map drifts from override codes | Low | Single source (models.py maps); fall back to bare code; unknown code is visible, not blank. |
| `overrides` inflates payload | Low | Bounded (≤ a handful per concept); rides existing payload; no per-render fetch (INV-1). |

## Integration Strategy

Strictly additive. `OverrideRecord`/`overrides` default-empty, so existing concept JSON validates and freeform concepts are unaffected. `onOverrideClick` is a new optional callback — `cas_breakdown` behavior is unchanged when it's absent (e.g. on `/compare`'s own CAS widget, if any). The hero chip was already inert text from Item 1; this item only attaches a handler. No change to `model_setup.py` sources, `analyst_override_count`, the compute path, or `/api/compute`.

## Validation Approach

- **Unit/data:** extracted `data/01.json` contains both override records, including the disabled `CAS27` with its `blocked_by`; `account_name` present; absent fields serialize as `null` (FR-1, FR-5, FR-6). Add to `test_extraction.py`/`test_models.py`.
- **Name-map unit:** reverse name→code lookup used by the Plotly handler covers top-level + CAS22 codes.
- **Browser (browser-inspect skill):** on concept 01 — (1) hero "(N entries)" opens the panel showing both entries; (2) ★ on the C220103 **CAS22 sub-row** opens it focused; (3) drill into the treemap, ★ sub-tile opens it focused; (4) the disabled CAS27 renders greyed/struck with `blocked_by`; (5) value shows its native-scale label. On `/compare` with concept 01 selected — ★ CapEx bar opens the focused panel. Read the JSON sidecar for console errors each time.
- **Honest-degradation check:** a record with `source=None`/`rationale=None` shows "not recorded", not a blank/vanished entry.
- **Regression:** existing suite passes (note: 6 pre-existing `test_extract_adapter` failures are unrelated, per Item 1).

## Next-Stage Handoff

**Fixed for the plan:**
- Data: `OverrideRecord` model + `ConceptData.overrides`, populated from `module.overrides`; `account_name` emitted from `models.py` maps; absent fields → `null`.
- One panel module (`override_panel.js`), singleton, page-agnostic; `showOverridePanel({records, focusAccount, conceptName})`.
- `cas_breakdown` gets `onOverrideClick` wired on all four interior surfaces, gated on `overridden`.
- Compare-bar trigger via `plotly_click`; data is already present on `/compare`.
- Value always rendered with a native-per-module scale label; disabled entries show `blocked_by`; missing fields show "not recorded".

**Open (needs user sign-off before plan):**
- **Decision 1** — panel form: fixed drawer (recommended) vs anchored popover.
- **Decision 3** — `source` rendered as plain text this item (link-ification deferred). Confirm.

**De-risk first:** the CAS22 sub-row / drilled sub-tile wiring (concept 01's only enabled ★ lives there) and the Plotly click→record mapping — the two places where "the panel just drops in" is false.

## Appendix — File/line index

| Concern | Location |
|---|---|
| Override registry shape | `model_setup_helpers.py:46-83` |
| Count read today (to sit beside) | `extract_explorer_data.py:380,426` |
| `ConceptData` definition | `models.py:353-400` |
| CAS name maps (extraction-side) | `models.py:155-194` |
| CAS name maps (JS-side) | `cas_breakdown.js:41,61` |
| ★ render — table rows | `cas_breakdown.js:277,294` |
| ★ render — treemap tiles | `cas_breakdown.js:339,351,375-382` |
| `onAccountClick` (existing, unused) | `cas_breakdown.js:114,117,121,270-272,395-397` |
| Hero chip ("(N entries)") | `concept_page.js:181-219` (chip span `:206`) |
| CAS breakdown mount (concept page) | `concept_page.js:584-587` |
| ★ render — CapEx bars (Plotly) | `view_capex.js:208,222,356,382` |
| Popover precedent (lifecycle/positioning) | `parameter_card.js:61-74,105-128,292-319` |
| Concept payload route | `server.py:434-438` |
| Compare data load | `comparison.js:141-145`, `view_capex.js:192` |
| Real not-applied override (CAS27) | `analyses/01-hts-compact-tokamak/model_setup.py:101-120` |

---
Next Step: After sign-off on Decisions 1 & 3 → `/_my_plan`.
