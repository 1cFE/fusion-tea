# Entry View

## Purpose
Display a browsable grid of all concepts grouped by status, so users can find and navigate to individual concept profiles.

## Requirements
- Page is an HTML shell (`index.html.j2`); on load, JS fetches `GET /api/manifest`
- Two groups: "Approved" and "In Progress" (based on `ConceptStatus`)
- Each concept card shows:
  - Name, confinement family badge, company name
  - Illustration thumbnail if `illustration` is non-null
  - LCOE range (if `has_cost_model: true` and `lcoe_per_mwh` is non-null)
  - Confidence badge (if `confidence_rating` is non-null)
  - "Has sensitivity data" indicator (if `has_sensitivities: true`)
- Clicking a card navigates to `/concept/{id}`
- Cards with cost models are visually richer than analysis-only cards (additional LCOE/confidence fields)
- Loading state shown while manifest is fetching

## Acceptance Criteria
- Given the page loads, when `GET /api/manifest` resolves, then concept cards appear grouped under "Approved" and "In Progress" headings
- Given a concept with `status: "approved"`, when the grid renders, then that card appears in the "Approved" group
- Given a concept with `has_cost_model: true` and `lcoe_per_mwh: 120.5`, when the card renders, then "120.5 $/MWh" or equivalent is displayed
- Given a concept with `has_cost_model: false`, when the card renders, then no LCOE field appears
- Given a concept with `illustration: "01-hts-compact-tokamak.png"`, when the card renders, then `<img src="/static/images/concepts/01-hts-compact-tokamak.png">` is present
- Given `GET /api/manifest` returns 8 concepts, when the grid renders, then exactly 8 cards are visible
- Given a user clicks a concept card, then the browser navigates to `/concept/{id}`
- Given manifest is loading, then a loading indicator is visible and no cards are shown prematurely

## Interfaces
- **Template**: `templates/index.html.j2` — extends `base.html.j2`
- **JS**: inline in template or small dedicated script
- **API calls**: `GET /api/manifest`
- **Navigates to**: `/concept/{id}` (see `specs/08-concept-profile.md`)
- **Route**: `GET /` → `dist/index.html`

## Constraints
- NEVER embed concept data in the HTML — all card content comes from manifest API response
- NEVER show partial grids — either loading state or full grid, not a mix
- The "In Progress" group must exist even if empty (with an appropriate empty state message)

## Out of Scope
- Filtering or sorting the concept grid
- Search functionality
- The comparison concept selector (comparison is initiated from the concept profile page)
- Full concept data loading (manifest summary data only)
