# CAS Breakdown Component

## Purpose
Render a CAS cost breakdown as a stacked bar chart with drill-down into CAS22 sub-accounts and override markers.

## Requirements
- Stacked horizontal bar: one segment per top-level CAS account (CAS10 through CAS90)
- CAS22 can expand to show sub-accounts (C220101-C220700) on click
- Overridden accounts flagged with a visible marker (e.g., asterisk or hatching)
- Hover on each segment shows: account name, cost in M$, percentage of total, override status
- Zero-value accounts are not rendered (no empty segments)
- Total capital cost shown as a label above the bar
- In multi-concept comparison view, all charts share the same x-axis scale

## Acceptance Criteria
- Given a `CostModelData.cas` with all accounts, when the chart renders, then only accounts with `cost_m_usd > 0` appear as segments
- Given a user clicks a CAS22 segment, when `cas22_detail` is provided, then the CAS22 segment expands inline to show sub-account breakdown
- Given a segment with `overridden: true`, when rendered, then it displays a visual override marker distinguishable from non-overridden segments
- Given a user hovers over any segment, then a tooltip shows: name, cost in M$, percentage of total, and whether it was overridden
- Given two concepts rendered side-by-side in comparison mode with `sharedScale: true`, when the charts render, then both x-axes have the same maximum value
- Given `cas22_detail` is empty, when the user clicks the CAS22 segment, then no drill-down occurs (click does nothing)

## Interfaces
```javascript
renderCASBreakdown(container: HTMLElement, options: {
  cas: Record<string, {name: string, cost_m_usd: number, overridden: boolean}>,
  cas22_detail?: Record<string, {name: string, cost_m_usd: number, overridden: boolean}>,
  showSubAccounts?: boolean,   // initial state; default false
  sharedScale?: number,        // if set, use this as x-axis max (for comparison alignment)
  onAccountClick?: (casCode: string, accountData: CASAccount) => void
})
```
- **Depends on**: `specs/04-design-system.md` (color palette for segments)
- **Used by**: `specs/08-concept-profile.md`, `specs/09-comparison-view.md`
- **Requires**: Plotly.js vendored at `static/vendor/plotly-basic.min.js`

## Constraints
- NEVER show CAS10-CAS90 hierarchy in the wrong order — display in ascending CAS number order
- NEVER omit the override marker when `overridden: true`; reviewers must be able to distinguish real vs. overridden costs
- All cost values MUST be treated as M$ (no unit conversion in the component)

## Out of Scope
- Computing or modifying CAS values (the component is display-only)
- The tornado chart sensitivity view (see `specs/05-tornado-chart.md`)
- Inline editing of cost overrides
