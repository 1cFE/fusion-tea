# Parameter Detail Card

## Purpose
Show a popover card with full parameter metadata when a user clicks a tornado chart bar, including cross-concept "Also sensitive" discovery.

## Requirements
- Appears as a popover/modal anchored near the clicked bar
- Displays all metadata fields:
  1. Display name + baseline value (with unit, applying `display_multiplier`)
  2. Source citation string
  3. Assumed range (`[low, high]` with unit)
  4. Confidence level (visual badge per design system)
  5. Modeling note (how the parameter flows through the cost model)
  6. Category badge (color-coded per design system)
- "Also sensitive" section: list of other concepts that have elasticity for this parameter (from cross-concept data), sorted by `|elasticity|` descending
- Each "Also sensitive" entry is a clickable link that navigates to that concept's profile page
- Card must be dismissible (click outside or press Escape)
- If `crossConceptData` is not provided or the parameter has no other concepts, "Also sensitive" section is omitted

## Acceptance Criteria
- Given parameter `availability` with `baseline: 0.70`, `display_unit: "%"`, `display_multiplier: 100`, when the card renders, then the displayed value is "70%"
- Given `confidence: "low"`, when the card renders, then a `?` badge appears in the confidence field
- Given `crossConceptData` with 3 other concepts, when the card renders, then all 3 appear in the "Also sensitive" section sorted by descending `|elasticity|`
- Given the user clicks outside the card, then the card is dismissed
- Given the user presses Escape, then the card is dismissed
- Given a parameter with no `source` string, when the card renders, then the source field is absent (not shown as empty)
- Given `crossConceptData` is null, when the card renders, then no "Also sensitive" section appears

## Interfaces
```javascript
showParameterCard(anchor: HTMLElement, options: {
  paramName: string,
  sensitivity: { elasticity: number, baseline: number },
  metadata: {
    display_name: string,
    display_unit?: string,
    display_multiplier?: number,
    category: ParameterCategory,
    confidence: Confidence,
    range?: [number, number],
    source?: string,
    source_quote?: string,
    modeling_note?: string
  },
  crossConceptData?: {
    display_name: string,
    concepts: Array<{ concept_id: string, concept_name: string, elasticity: number }>
  }
})

hideParameterCard()   // programmatic dismiss
```
- **Depends on**: `specs/04-design-system.md` (badge styles, category colors, confidence encoding)
- **Used by**: `specs/08-concept-profile.md` (concept page tornado click handler)
- **Data source for `crossConceptData`**: `GET /api/parameters/{param_name}` (see `specs/03-server.md`)

## Constraints
- NEVER show the card without applying `display_multiplier` to the baseline value
- NEVER show an empty "Also sensitive" section — omit the section entirely when there are no entries
- The card must not obstruct the tornado chart bars; position to avoid overflow outside the viewport
- Only one card may be visible at a time; opening a new card dismisses the previous

## Out of Scope
- Editing parameter values (display only)
- Showing the full source document (linking to the citation string is sufficient)
- The slider controls tied to parameter range (see `specs/12-slider-controls.md`)
