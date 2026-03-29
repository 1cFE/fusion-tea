
## Purpose
Render side-by-side multi-concept comparisons with aligned sensitivity tornado charts, CAS breakdowns, and headline metrics.

## Requirements
- `renderComparison(container, options)` renders one of three views: `"tornado"`, `"cas"`, or `"headline"`
- **Tornado view**: Parameters appearing in >1 selected concept are "shared" and aligned horizontally in rows; parameters unique to one concept appear in a concept-specific section below
- **CAS view**: Stacked bars for each concept with a shared x-axis scale (same $/MWh range)
- **Headline view**: Table with columns per concept, rows for LCOE, capital cost, P_net, Q_eng, confidence
- Concepts are added to the comparison set from the concept profile page (not the entry view)
- Up to 4 concepts can be compared simultaneously
- Concept data is lazy-loaded via `GET /api/concepts/{id}` when a concept is added to the comparison

## Acceptance Criteria
- Given 2 concepts both with `"availability"` in their sensitivities, the tornado view aligns `"availability"` bars in the same row
- Given a parameter appearing in only one concept, it appears in a "Unique to {concept}" section
- The CAS view uses the same x-axis scale across all concept bars
- Adding a 5th concept is rejected (UI disables the add button at 4)
- Removing a concept from the comparison re-renders without that concept's data
- Concept data is fetched lazily — no concept data is loaded until that concept is selected

## Interfaces
- **File**: `exploration/concept_explorer/static/js/comparison.js`
- **Template**: `exploration/concept_explorer/templates/compare.html.j2`
- **Inputs**: `{ concepts: ConceptData[], view: "tornado"|"cas"|"headline", alignmentConfig? }`
- **API calls**: `GET /api/concepts/{id}` for each added concept
- **Reuses**: `renderTornado` from `14-tornado-chart.md`, `renderCASBreakdown` from `15a-cas-breakdown.md`

## Constraints
- NEVER pre-load all concept data on page load — lazy-fetch only
- Maximum 4 concepts in comparison at one time
- Alignment MUST be by exact parameter key match (not display name)

## Out of Scope
- Exporting comparison data to CSV or image
- Saving comparison sets between sessions
- Cross-concept parameter threading (covered by `09-parameter-index.md` + `15-parameter-detail-card.md`)

