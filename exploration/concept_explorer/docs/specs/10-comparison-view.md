# Comparison View

## Purpose
Display side-by-side sensitivity and cost breakdowns for up to 4 selected concepts, with shared parameters aligned horizontally across concepts.

## Requirements
- Page is an HTML shell (`compare.html.j2`); concept data loaded lazily as concepts are added
- Concept selector: add/remove concepts up to 4; shows name, confinement family, company
- Only concepts with `has_cost_model: true` AND `has_sensitivities: true` available for sensitivity tab; all cost-model concepts available for CAS and headline tabs
- Three tabs: Sensitivity | CAS | Headline
- **Sensitivity tab**: tornado charts aligned horizontally; each row is one parameter; missing values shown as gap markers (not zero bars)
  - Shared parameters (≥2 selected concepts) sorted by max `|elasticity|` across the set
  - Concept-unique parameters (exactly 1 concept) in a separate section below
- **CAS tab**: side-by-side stacked bars with shared x-axis scale
- **Headline tab**: table comparing LCOE, overnight cost ($/kW), P_net (MW), Q_eng, confidence for all selected concepts
- Reports `ExplorerState` (including `comparison_set`) to `POST /api/state` when comparison set changes

## Acceptance Criteria
- Given 2 concepts are selected, when the sensitivity tab is active, then parameters shared by both appear in aligned rows at the top, with concept-unique parameters in a separate section below
- Given concept A has `availability` with elasticity -0.85 and concept B has `availability` with elasticity -0.60, when the sensitivity tab renders, then both bars appear in the same row with the same zero-axis reference
- Given concept A has parameter `p_cryo` but concept B does not, when the sensitivity tab renders, then concept A shows a bar for `p_cryo` and concept B shows a gap marker (not a zero bar)
- Given a standalone concept (no sensitivities) is selected, when the user tries to add it to the sensitivity tab, then it is unavailable or shows an explanatory note
- Given 2 concepts are selected in the CAS tab, when both CAS charts render, then they share the same x-axis maximum value
- Given the comparison set changes (concept added or removed), when `POST /api/state` is called, then `comparison_set` in the body reflects the current set
- Given 0 concepts are selected, when the page loads, then the selector is shown with an invitation to add concepts; no charts rendered

## Interfaces
- **Template**: `templates/compare.html.j2` — extends `base.html.j2`
- **JS**: `static/js/comparison.js` — alignment logic and concept selector
- **Components used**:
  - `renderTornado()` from `specs/05-tornado-chart.md` (per-concept, constrained to shared rows)
  - `renderCASBreakdown()` from `specs/06-cas-breakdown.md` (with `sharedScale`)
- **API calls**: `GET /api/concepts/{id}` (lazy, per concept added), `POST /api/state`
- **Route**: `GET /compare` → `dist/compare.html`

## Constraints
- NEVER show a zero bar for a parameter a concept doesn't have — use a gap marker
- NEVER allow >4 concepts in the comparison set
- Shared parameter alignment: sorted by max `|elasticity|` across the selected set, not by any single concept's ranking
- Concept data must be fetched lazily (on add), not preloaded for all concepts on page load

## Out of Scope
- Comparison of standalone-only concepts in the sensitivity tab (they lack sensitivity data)
- Saving or sharing comparison configurations
- Exporting comparison data to CSV or image
