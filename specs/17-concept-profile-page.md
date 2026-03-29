
## Purpose
Render the single-concept profile: identity hero, key bets, tornado chart, CAS breakdown, and risk table, with optional interactive sliders when the server is available.

## Requirements
- The page fetches concept data via `GET /api/concepts/{id}` on load (no inline JSON in HTML)
- Layout sections: identity hero (name, company, family badge, thesis, illustration slot), key bets & differentiators, sensitivity tornado chart, CAS breakdown, top risks table
- Population context marks appear on the tornado chart (whiskers showing distribution across all concepts)
- If the server is available (`GET /api/health` returns 200), sliders are shown for parameters with a defined `range` in metadata
- Slider changes debounce 200ms then call `POST /api/compute`; the tornado, CAS breakdown, and headline update with the response
- The page pushes its state to `POST /api/state` on load and on each slider change
- Navigation breadcrumb shows: "All Concepts > {concept name}"
- An "Add to comparison" button pushes the concept ID to the comparison set

## Acceptance Criteria
- The page loads and renders without error when accessed at `/concept/01-hts-compact-tokamak`
- The tornado chart renders with correct category colors from `13-design-system.md`
- Clicking a tornado bar shows a parameter detail card (via `15-parameter-detail-card.md`)
- Adjusting a slider and waiting 200ms triggers a `POST /api/compute` call and updates the tornado chart
- When the server is unreachable, sliders are hidden and the page renders using pre-fetched static data only
- `GET /api/state` after page load returns `current_concept_id` matching the concept being viewed

## Interfaces
- **Template**: `exploration/concept_explorer/templates/concept.html.j2`
- **JS**: `exploration/concept_explorer/static/js/explorer_app.js` (page orchestration)
- **API calls**: `GET /api/concepts/{id}`, `GET /api/health`, `POST /api/compute`, `POST /api/state`
- **Components used**: `renderTornado` (`14-tornado-chart.md`), `renderCASBreakdown` (CAS breakdown), `showParameterCard` (`15-parameter-detail-card.md`)

## Constraints
- NEVER embed concept data in the HTML shell — always fetch via API
- Sliders MUST be hidden (not just disabled) when the server is unavailable
- The page MUST render correctly even if narrative data is null (concept without `analysis.md`)

## Out of Scope
- The CAS breakdown component implementation (see dedicated spec)
- Comparison rendering (see `16-comparison-view.md`)

