
## Purpose
Show a popover detail card for a sensitivity parameter, displaying source, range, confidence, modeling note, and cross-concept links.

## Requirements
- `showParameterCard(anchor, options)` renders a popover anchored to the clicked tornado bar element
- Card shows: display name + baseline value (with unit), source citation, assumed range, confidence badge, modeling note, category badge
- Card includes an "Also sensitive in:" section listing other concepts where this parameter appears in sensitivity data, sorted by `|elasticity|` descending
- The "Also sensitive in:" links are populated via a `GET /api/parameters/{paramName}` call (US-14)
- The card dismisses on click-outside or Escape key
- Only one card is shown at a time (opening a new card closes the previous)

## Acceptance Criteria
- Clicking a tornado bar shows a card containing the parameter's `display_name` and `baseline` value
- The `source` field from `ParameterMetadata` is shown in the card
- The card's "Also sensitive in:" section lists at least one other concept when that parameter has `|elasticity| > 0` in another concept's data
- Pressing Escape dismisses the card
- Opening a second card closes the first
- The card renders without crashing when `metadata.source` is an empty string

## Interfaces
- **File**: `exploration/concept_explorer/static/js/parameter_card.js`
- **Inputs**: `{ anchor, paramName, sensitivity: { elasticity, baseline }, metadata: ParameterMetadata }`
- **API call**: `GET /api/parameters/{paramName}` (see `09-parameter-index.md`)
- **Used by**: `17-concept-profile-page.md` (as `onParameterClick` handler)

## Constraints
- NEVER show more than one card at a time
- The card MUST degrade gracefully if `/api/parameters/{name}` returns 404 (show "No other concepts analyzed for this parameter")
- NEVER block chart interaction while the card API call is in flight — show a loading state in the "Also sensitive in:" section

## Out of Scope
- Slider controls in the card (sliders are on the main page, see `17-concept-profile-page.md`)
- Editing parameter metadata

