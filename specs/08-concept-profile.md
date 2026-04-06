# Concept Profile Page

## Purpose
Display a single concept's identity, headline economics, narrative context, sensitivity analysis, and CAS cost breakdown on one information-dense page.

## Requirements
- Page is an HTML shell (`concept.html.j2`); all data fetched at runtime via `GET /api/concepts/{id}`
- Also fetches `GET /api/manifest` (for population context whiskers)
- Identity hero: concept name, company, confinement family badge, thesis one-liner, illustration (or placeholder)
- Headline summary card: LCOE ($/MWh), overnight cost ($/kW), P_net (MW), Q_eng, confidence badge
- Narrative sections: key bets, eliminated costs, novel costs (rendered only if `narrative` is non-null)
- Sensitivity section: tornado chart (top 15 params); if `sensitivities` is null, show standalone placeholder
- CAS breakdown section: stacked bar, always shown if cost model present
- Risks section: table of top risks with severity and retirement path
- "Add to comparison" button at bottom of page
- Breadcrumb in nav shows concept name
- Reports `ExplorerState` to `POST /api/state` on page load

## Acceptance Criteria
- Given concept ID in the URL, when the page loads, then `GET /api/concepts/{id}` is called and all sections populated before the user sees empty containers (loading state shown during fetch)
- Given `narrative: null`, when the page renders, then narrative sections are absent (not shown as empty)
- Given `cost_model.sensitivities: null` (standalone concept), when the page renders, then the tornado container shows the placeholder text, not an empty chart or error
- Given `cost_model: null` (analysis-only concept), when the page renders, then both tornado and CAS sections are absent
- Given `narrative.top_risks` has 3 entries, when the risks section renders, then all 3 appear with severity badges
- Given page loads, when `POST /api/state` is called, then the body contains `{ current_concept_id: "{id}", slider_overrides: {}, comparison_set: [] }`
- Given the concept has an `illustration` filename, when the hero renders, then `<img src="/static/images/concepts/{filename}">` is present
- Given a user clicks a tornado bar, then `showParameterCard()` is called with that parameter's data and cross-concept data fetched from `GET /api/parameters/{paramName}`

## Interfaces
- **Template**: `templates/concept.html.j2` — extends `base.html.j2`, injects `CONCEPT_ID` constant
- **JS**: `static/js/concept_page.js` — orchestrates fetches and component mounting
- **Components used**:
  - `renderTornado()` from `specs/05-tornado-chart.md`
  - `renderCASBreakdown()` from `specs/06-cas-breakdown.md`
  - `showParameterCard()` from `specs/07-parameter-card.md`
- **API calls**: `GET /api/concepts/{id}`, `GET /api/manifest`, `GET /api/parameters/{name}`, `POST /api/state`
- **Route**: `GET /concept/{concept_id}` → `dist/concept/{concept_id}.html`

## Constraints
- NEVER embed concept data in the HTML template — data comes from the API at runtime
- NEVER show an empty chart in place of the standalone placeholder — the user must understand why there's no tornado chart
- The fetch of concept data and manifest must be parallel (`Promise.all`), not sequential

## Out of Scope
- Slider controls for parameter what-if (see `specs/12-slider-controls.md`)
- The comparison view itself (see `specs/09-comparison-view.md`)
- Managing the comparison set state across pages
