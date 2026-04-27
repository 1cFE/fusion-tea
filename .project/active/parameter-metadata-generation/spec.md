# Spec: Concept Page Sensitivity Restructure

**Status:** In Progress
**Owner:** Reid W
**Created:** 2026-04-26 14:34 PDT
**Updated:** 2026-04-26 (scope shifted — see "History" below)
**Complexity:** MEDIUM
**Branch:** sensitivity-sliders

---

## Work Item Summary

Restructure the concept profile page so the parameter sliders that drive `POST /api/compute` are actually usable. The slider data plumbing was completed earlier in this work item (Phase 1, see History); the slider rendering is functional end-to-end but visually unusable — 47 undifferentiated sliders below the fold, decoupled from the LCOE they drive, with raw Python identifiers as labels.

This spec covers the UI restructure that makes those sliders ship-quality:

- **Co-locate sliders with tornado bars** so each sensitivity parameter shows `name | impact | what-if slider | current value` on a single row.
- **Sticky compact headline** with LCOE / Overnight / Net Power / Capacity Factor pinned at the top, updating live as sliders move.
- **Collapsible sections** for Narrative, Risks, CAS, Sources — Sensitivity & What-If expanded by default.
- **Curated display registry** for the ~25 parameters that appear in tornado top-15 across concepts (human-readable names + units).

The canonical visual reference is `mockup_v2.html` in this work item folder. Treat the mockup as the spec for layout and interaction.

## Why This Matters Now

Phase 1 made the sliders *exist*. They don't yet help anyone. The current page surface is:

- 47 sliders all at the same width and styling
- LCOE feedback ~6 viewport-heights above where the user is dragging
- Labels like "Mn", "Eta Th", "Dhe3 Dd Frac" — Python identifiers, not parameter names
- Values without units (`P Coils 2.000` could be MW, kW, or a count)

A what-if tool only earns its place when the user can connect cause to effect at a glance. That requires the sliders, the LCOE result, and the impact ranking to be co-visible.

## Key Bets / Constraints

- **Bet:** Co-locating sliders with tornado bars is worth a `tornado.js` refactor from Plotly to native DOM. The user has explicitly chosen this path over the cheaper "keep Plotly, link sliders separately" alternative.
- **Bet:** A small shared display registry (~25 params) covers ≥80% of tornado top-15 occurrences across concepts. Per-concept yaml stays as the override path.
- **Constraint:** Backend (`/api/compute`) and `ParameterMetadata` model do not change. This is purely frontend + a registry-loading step in the extractor.
- **Constraint:** Standalone (non-costingfe) concepts must continue to render — they have no sliders, but the page should not break. Sticky headline still shows static values, no Reset.

---

## Business Goals

### Why This Matters

The slider system was the headline interactive feature of the concept explorer. Phase 1 connected the data; the page now renders them but flattens the user's mental model: "which lever should I pull, and what happens when I pull it?" should be answerable in one glance, not by scrolling between sections.

### Success Criteria

- [ ] On `/concept/{id}` for a costingfe concept, the user sees: a sticky headline at top, a single Sensitivity & What-If section showing the top-15 parameters in `name | bar | slider | value` rows.
- [ ] Dragging any slider updates the sticky LCOE within ~250 ms (existing `/api/compute` debounce).
- [ ] The sticky headline shows a delta indicator (▲ / ▼ / no change) on each modified stat.
- [ ] Reset button clears all overrides and removes deltas.
- [ ] Narrative / Risks / CAS / Sources are collapsed by default and expand on click.
- [ ] The top ~25 most-impactful parameters across all concepts have human-readable display names and correct units (e.g., "Thermal Efficiency 46.0%" not "Eta Th 0.460").
- [ ] Standalone concepts still load successfully — they show the static page without sliders.

### Priority

P1 — finishes a started feature that's been visible-but-broken to anyone clicking through the explorer.

---

## Problem Statement

### Current State

- `parameter_metadata` is populated for all 19 costingfe concepts (Phase 1 — done).
- 47 sliders render for concept 01 with auto-generated labels.
- LCOE / Overnight scroll out of view as the user moves down to the slider section.
- `tornado.js` and `concept_page.js` render two separate sections that show the same parameter list — once as Plotly bars, once as `<input type=range>` controls.
- Display names are `key.replace("_", " ").title()`, no units, no display multipliers.

### Desired Outcome

A concept page where:
1. The user lands on Sensitivity & What-If expanded (because it's the interactive content).
2. They scan a tight, ranked grid of `[parameter | bar | slider | value]` rows.
3. They drag a slider; the sticky LCOE pill updates with a colored delta.
4. They can Reset, collapse other sections, or scroll without losing the LCOE feedback.

---

## Scope

### In Scope

- Refactor of `tornado.js` to render an integrated grid (HTML/CSS/SVG) supporting inline sliders. Same public API (`renderTornado(container, options)`) and color/category encoding; new internal implementation.
- Sticky compact headline component replacing the in-flow `headline-card`.
- Collapsible section component applied to existing sections (Narrative, Risks, CAS, Sources, Sensitivity).
- Removal of the standalone `renderSliders()` path in `concept_page.js` (folded into the integrated grid).
- New file: `exploration/concept_explorer/data/parameter_display_registry.yaml` — shared display names, units, multipliers.
- Extractor change: load and merge the registry between `generate_parameter_metadata()` and per-concept yaml.
- Re-extraction of all costingfe concepts to apply the registry.

### Out of Scope

- Comparison view changes — sliders there were already deferred per spec 12.
- Persistent slider state across reloads or named scenarios — deferred per spec 12.
- Recomputing sensitivity elasticities on slider drag — deferred per spec 12. Tornado bars stay at baseline elasticity.
- Backend / `/api/compute` changes — already shipped and working.
- `ParameterMetadata` Pydantic model changes — current fields are sufficient.
- Animating sticky-bar value transitions, keyboard shortcuts, mobile-specific layout — polish, not needed to ship.

---

## Requirements

### Functional Requirements

1. **FR-1**: The concept profile page MUST render a sticky element at the top of the viewport (below the topnav) containing concept identity (name, family badge, company) and four headline stats (LCOE, Overnight Cost, Net Power, Capacity Factor).
2. **FR-2**: When a slider override is active, the sticky bar MUST display the post-compute value AND a delta indicator showing `(current − baseline) / baseline`.
3. **FR-3**: The Sensitivity & What-If section MUST render parameters as a single grid where each row contains: parameter name, sensitivity bar, slider, current value.
4. **FR-4**: The grid MUST show only the top-N parameters by `|elasticity|` (default N=15, matching tornado's existing default). No separate slider list elsewhere.
5. **FR-5**: Each major section (Narrative, Risks, CAS, Sensitivity, Sources) MUST have a clickable header that toggles its body open/closed. Sensitivity defaults open; the rest default closed.
6. **FR-6**: Section headers MUST show a brief content preview when collapsed (e.g., risk count, total capital, "key bets · eliminated costs").
7. **FR-7**: A Reset button in the sticky bar MUST clear all overrides and revert sliders to baselines. The button MUST be disabled when no overrides exist.
8. **FR-8**: A `parameter_display_registry.yaml` MUST provide curated `display_name`, `display_unit`, and `display_multiplier` for at least the parameters that appear in the tornado top-15 across costingfe concepts. Entries from this registry MUST take precedence over auto-generated names but MUST defer to per-concept `model_metadata.yaml`.
9. **FR-9**: Standalone (non-costingfe) concepts MUST continue to render without errors. They show the same sticky bar and collapsible structure but no sliders or Reset button.

---

## Acceptance Criteria

### Core Functionality
- [ ] Sticky headline visible on `/concept/{id}` for both costingfe and standalone concepts
- [ ] Dragging a slider on a costingfe concept updates the sticky LCOE and shows a green/orange delta
- [ ] Reset button clears overrides and disables itself afterward
- [ ] All five sections collapse/expand on header click; Sensitivity defaults open
- [ ] Top-15 parameters render in a single integrated grid; no separate "Parameter What-If" section exists
- [ ] At least the parameters in concept 01's tornado top-15 show curated names + units (e.g., "Thermal Efficiency 46.0%")

### Quality & Integration
- [ ] `pytest exploration/concept_explorer/tests/` passes (existing tests untouched or updated to match new structure)
- [ ] Browser console shows no errors on concept 01, 04, 19 (representative costingfe), and a standalone concept
- [ ] `model_metadata.yaml` per-concept overrides still take precedence (verified by spot test)
- [ ] Hover tooltip and click→parameter card behavior preserved on the new tornado grid

---

## History

### Phase 1 — Parameter Metadata Generation (2026-04-26, complete)

The original spec for this work item covered generating `ParameterMetadata` from extraction so sliders had ranges and baselines. That work is done:

- `generate_parameter_metadata()` in `extract_explorer_data.py:152-204` derives metadata from `SensitivityAnalysis`.
- Range strategy: `baseline ± 30%`, clamped to `[0, ∞)` and to `[0, 1]` for fractional parameters.
- 47 sliders now render for concept 01 (was 0). Compute pipeline verified end-to-end.
- 8 unit tests added; 52 extraction tests passing.

A live walkthrough after Phase 1 surfaced that data alone wasn't enough — the page needed UI restructure. That's this spec's current scope.

### Phase 2 — UI Restructure (in progress)

This spec, as it stands now, governs phase 2.

---

## Related Artifacts

- **Design:** `.project/active/parameter-metadata-generation/design.md`
- **UI mockup (canonical):** `.project/active/parameter-metadata-generation/mockup_v2.html`
- **UI mockup (initial sketch):** `.project/active/parameter-metadata-generation/mockup.html`
- **Research:** `.project/research/20260426-134728_sensitivity-analysis-state.md`
- **Spec 12:** `exploration/concept_explorer/docs/specs/12-computation-api.md`

---

**Next Steps:** Update plan (`plan.md`) to phase 2 work items, then `/_my_implement`.
