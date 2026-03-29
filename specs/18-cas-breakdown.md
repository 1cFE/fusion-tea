
## Purpose
Render the CAS cost breakdown as a stacked bar chart with CAS22 drill-down, override markers, and hover details.

## Requirements
- `renderCASBreakdown(container, options)` renders a Plotly.js stacked horizontal bar from `CostModelData.cas`
- One segment per CAS account (CAS10–CAS90), colored by account group
- Zero-cost accounts are hidden (not rendered as zero-width segments)
- Clicking the CAS22 segment expands it to show `cas22_detail` sub-accounts
- Accounts with `overridden=true` display a visual override marker (e.g., a small icon or border)
- Hover tooltip shows: account name, cost in M$, percentage of total capital, override status
- When used in comparison view, x-axis scale is shared across all concept bars

## Acceptance Criteria
- A concept with `cas22_detail` containing 5 sub-accounts renders 5 segments when CAS22 is clicked
- An account with `overridden=true` shows a visual marker distinct from non-overridden accounts
- Hover on CAS22 shows cost and percentage of total
- Zero-cost CAS accounts do not appear as segments in the stacked bar
- Clicking CAS22 a second time collapses back to the top-level view

## Interfaces
- **File**: `exploration/concept_explorer/static/js/cas_breakdown.js`
- **Inputs**: `{ cas: dict[str, CASAccount], cas22_detail?: dict[str, CASAccount], showSubAccounts?: bool, onAccountClick? }`
- **Depends on**: `vendor/plotly-basic.min.js`, CSS variables from `13-design-system.md`
- **Used by**: `17-concept-profile-page.md`, `16-comparison-view.md`

## Constraints
- NEVER render zero-cost accounts as visible segments
- Override marker MUST be visually distinct without relying on color alone (accessible encoding)
- CAS22 drill-down MUST be togglable (expand and collapse)

## Out of Scope
- Waterfall chart variant (stacked bar only for now)
- Exporting chart data

