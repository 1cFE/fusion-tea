# Design System

## Purpose
Define the visual language — colors, typography, layout, and uncertainty encoding — that all pages and chart components must follow.

## Requirements
- Dark background, high-contrast type, compact spacing ("Bloomberg terminal, not marketing dashboard")
- Data-to-ink ratio over whitespace — every number earns its space
- Uncertainty must be as visually prominent as the values themselves
- Parameter categories encoded by color (5 fixed colors, no deviation):
  - Shared baseline: `#6B7280` (gray)
  - Well-established: `#3B82F6` (blue)
  - Key innovation: `#10B981` (green)
  - Concept-unique: `#F59E0B` (amber)
  - High-risk: `#EF4444` (red)
- Confidence levels encoded by opacity and texture:
  - High: full opacity, solid fill, no badge
  - Medium: 80% opacity, `~` badge
  - Low: 60% opacity, hatched fill pattern, `?` badge
- Confinement family badges (MFE / IFE / MIF / Non-Standard) visually distinct
- Navigation bar: "All Concepts" and "Compare" links; breadcrumb slot for inner pages
- Responsive layout sufficient for 1280px+ desktop (primary use case)

## Acceptance Criteria
- Given any page is opened, when the CSS loads, then the background is dark and text is high-contrast (WCAG AA minimum contrast ratio 4.5:1 for body text)
- Given a tornado bar with `confidence: "low"`, when rendered, then the bar has hatched fill and a `?` badge
- Given a tornado bar with `confidence: "medium"`, when rendered, then the bar has 80% opacity and a `~` badge
- Given a parameter with `category: "high-risk"`, when its tornado bar is rendered, then the bar color is `#EF4444`
- Given any page, when viewed at 1280px width, then no horizontal overflow occurs and all content is readable
- Given the navigation bar, when the current page is `/`, then the "All Concepts" link is visually active

## Interfaces
- **Provides**:
  - `static/css/explorer.css` — design system tokens, layout, component styles
- **Consumed by**: All HTML templates and JS chart components
- **Defines constants used by**:
  - `specs/05-tornado-chart.md` (category colors, confidence encoding)
  - `specs/06-cas-breakdown.md` (color palette for CAS segments)
  - `specs/07-parameter-card.md` (card styling, badge styles)
  - All page templates

## Constraints
- NEVER use a category color for a purpose other than its defined category
- NEVER represent confidence visually without both an opacity change AND a badge/pattern
- NEVER add CDN dependencies — all vendor assets must be in `static/vendor/`
- The `base.html.j2` template owns the shared layout (nav, head, footer); individual pages must extend it

## Out of Scope
- Mobile/phone layout optimization
- Dark/light mode toggle
- Illustration content strategy (images in `static/images/concepts/` are manually curated, not designed here)
- Accessibility beyond WCAG AA contrast minimum
