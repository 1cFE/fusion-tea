
## Purpose
Render a horizontal tornado chart of parameter sensitivities with category color encoding, confidence opacity, and a click handler that triggers the parameter detail card.

## Requirements
- `renderTornado(container, options)` renders a Plotly.js horizontal bar chart into the provided DOM element
- Bars are sorted by `|elasticity|` descending; the top N (default 15) are shown
- Left bars indicate LCOE decrease (negative elasticity), right bars indicate LCOE increase (positive elasticity)
- Bar color encodes `ParameterCategory` using the colors from `13-design-system.md`
- Bar opacity encodes `Confidence` using the levels from `13-design-system.md`
- Clicking a bar fires `options.onParameterClick(paramName, metadata)` for the host page to show the detail card
- Population context: small whisker marks on each bar indicating the range of that parameter's elasticity across the full concept population (compare-by-default principle)

## Acceptance Criteria
- Given `sensitivities` with 20 entries, only 15 bars render (top 15 by `|elasticity|`)
- Given a `key-innovation` parameter, its bar renders with fill `#10B981`
- Given a `low` confidence parameter, its bar renders at 60% opacity with hatched fill
- Clicking a bar calls `onParameterClick` with the correct `paramName` (matching the key in `sensitivities`)
- Given population data with a known range for `availability`, whisker marks appear on the availability bar at the correct positions
- The chart renders without error when `options.parameterMetadata` is empty (degrades gracefully to uncolored bars)

## Interfaces
- **File**: `exploration/concept_explorer/static/js/tornado.js`
- **Inputs**: `{ sensitivities: { engineering, financial }, parameterMetadata, topN, onParameterClick, populationData }`
- **Output**: Plotly chart rendered into `container`
- **Depends on**: `vendor/plotly-basic.min.js`, CSS variables from `13-design-system.md`
- **Used by**: `17-concept-profile-page.md`, `16-comparison-view.md`

## Constraints
- NEVER import Plotly from CDN — use the vendored `plotly-basic.min.js`
- NEVER render more than `topN` bars (default 15) — caller controls this limit
- The chart MUST render in the absence of parameter metadata (no crash, just no color encoding)

## Out of Scope
- Parameter detail card rendering (see `15-parameter-detail-card.md`)
- Slider controls (see `17-concept-profile-page.md`)
- Comparison alignment (see `16-comparison-view.md`)

