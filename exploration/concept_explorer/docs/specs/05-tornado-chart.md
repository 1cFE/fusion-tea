# Tornado Chart Component

## Purpose
Render a horizontal bar chart of parameter sensitivity elasticities, with category color encoding, confidence opacity, population whiskers, and a click handler for parameter detail.

## Requirements
- Horizontal bars: left = LCOE decreases with parameter increase, right = LCOE increases
- Show top N parameters sorted by `|elasticity|` (default N=15)
- Bar color encodes `ParameterMetadata.category` per design system colors
- Bar opacity encodes `ParameterMetadata.confidence` per design system rules
- Population whiskers: for each parameter, show a range marker indicating [min, max] elasticity across all other concepts with that parameter in the parameter index; absent for concept-unique parameters
- Engineering and financial sensitivities merged into one ranked list; filterable by the user
- Click on a bar fires `onParameterClick(paramName, metadata)` callback
- If `sensitivities` is null (standalone concept), render an informative placeholder: "No sensitivity data available — this concept uses a standalone cost model"
- Category legend visible below the chart

## Acceptance Criteria
- Given 20 parameters in sensitivity data, when the chart renders with default `topN=15`, then exactly 15 bars are shown
- Given a parameter with `elasticity: -0.91`, when rendered, then its bar extends to the left of the zero axis
- Given a parameter with `category: "key-innovation"`, when rendered, then its bar color is `#10B981`
- Given a parameter with `confidence: "low"`, when rendered, then its bar has hatched fill and 60% opacity
- Given a parameter that appears in 3 other concepts in the parameter index, when the chart renders, then a whisker marker shows the [min, max] elasticity range behind that bar
- Given a parameter unique to this concept (not in parameter index), when rendered, then no whisker marker appears
- Given `sensitivities: null`, when `renderTornado()` is called, then the container shows the standalone placeholder text, not an empty chart
- Given a user clicks on a bar, when `onParameterClick` is defined, then it is called with the parameter name and its metadata object

## Interfaces
```javascript
renderTornado(container: HTMLElement, options: {
  sensitivities: { engineering: Record<string, {elasticity: number, baseline: number}>,
                   financial:   Record<string, {elasticity: number, baseline: number}> } | null,
  parameterMetadata: Record<string, ParameterMetadata>,
  populationContext?: ConceptManifest,   // for whisker marks; null omits whiskers
  topN?: number,                         // default 15
  onParameterClick?: (paramName: string, metadata: ParameterMetadata) => void
})
```
- **Depends on**: `specs/04-design-system.md` (colors, confidence encoding), `specs/01-data-models.md` (data shapes)
- **Used by**: `specs/08-concept-profile.md`, `specs/09-comparison-view.md`
- **Requires**: Plotly.js vendored at `static/vendor/plotly-basic.min.js`

## Constraints
- NEVER show a zero bar for a missing parameter — absence means no data, not zero elasticity
- NEVER render the chart without a category legend
- NEVER proceed silently if `parameterMetadata` is missing keys present in `sensitivities` — log a console warning per missing key
- Population whiskers must be visually secondary to the primary bar (different opacity/weight)

## Out of Scope
- Slider controls (see `specs/12-slider-controls.md`)
- The parameter detail card contents (see `specs/07-parameter-card.md`)
- Cross-concept comparison alignment (see `specs/09-comparison-view.md`)
