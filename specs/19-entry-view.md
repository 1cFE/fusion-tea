
## Purpose
Render the concept grid index page, grouping concepts by status and showing summary cards that invite exploration.

## Requirements
- The page fetches the manifest via `GET /api/manifest` on load
- Concepts are displayed in two groups: "Approved" and "In Progress"
- Each concept card shows: name, confinement family badge, company, LCOE (if cost model exists), confidence badge
- Concepts with cost models have richer cards (LCOE value, confidence badge) than analysis-only concepts
- Clicking a card navigates to `/concept/{id}`
- No comparison selection on this page — comparisons are initiated from within concept profile pages

## Acceptance Criteria
- The page loads and renders the concept grid without error
- Concepts with `status=approved` appear in the "Approved" group
- Concepts with `has_cost_model=false` render cards without LCOE or confidence badge
- Clicking a concept card navigates to the correct `/concept/{id}` URL
- The page renders with at least a loading state when the manifest fetch is in flight

## Interfaces
- **Template**: `exploration/concept_explorer/templates/index.html.j2`
- **JS**: part of `exploration/concept_explorer/static/js/explorer_app.js`
- **API calls**: `GET /api/manifest`
- **Navigates to**: `/concept/{id}` (see `17-concept-profile-page.md`)

## Constraints
- NEVER add comparison checkboxes to this page — entry view is single-concept focus
- NEVER inline manifest data in the HTML shell — always fetch via API

## Out of Scope
- Filtering or searching concepts
- Sorting by LCOE or other fields
- Pagination (≤20 concepts total)

