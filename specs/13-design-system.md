
## Purpose
Define the visual language — color palette, typography, spacing, and confidence/category encoding rules — that all UI components must follow.

## Requirements
- Parameter category colors: shared-baseline `#6B7280`, well-established `#3B82F6`, key-innovation `#10B981`, concept-unique `#F59E0B`, high-risk `#EF4444`
- Confidence opacity: high = 100%, medium = 80%, low = 60%
- Low-confidence values additionally use a hatched fill pattern and a `?` badge
- Medium-confidence values use a `~` badge
- Dark background theme (Bloomberg-terminal aesthetic): high-contrast type, compact spacing, data-to-ink ratio prioritized
- Typography and spacing are defined as CSS custom properties (variables) in `explorer.css`

## Acceptance Criteria
- A tornado bar for a `key-innovation` parameter renders with fill color `#10B981`
- A tornado bar for a `low` confidence parameter renders at 60% opacity with a hatched pattern
- A tornado bar for a `high` confidence parameter renders at 100% opacity with no badge
- CSS custom properties for all category colors and confidence opacities are defined in `explorer.css` (grep-verifiable)
- No component hardcodes color hex values — all reference CSS variables

## Interfaces
- **File**: `exploration/concept_explorer/static/css/explorer.css`
- **CSS variables consumed by**: `14-tornado-chart.md`, `15-cas-breakdown.md`, `16-comparison-view.md`, `17-concept-profile-page.md`, `18-entry-view.md`
- **Encoding values from**: `ParameterCategory` and `Confidence` enums in `01-data-models.md`

## Constraints
- NEVER hardcode hex color values in JS components — always reference CSS variables or a shared constants object
- Confidence encoding MUST be visually prominent — uncertainty must be impossible to ignore at a glance
- Dark background MUST be maintained across all pages — no light-mode default

## Out of Scope
- Responsive / mobile layout
- Print stylesheet
- Accessibility compliance (WCAG) — noted as future work only

