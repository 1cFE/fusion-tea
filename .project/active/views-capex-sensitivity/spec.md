# Spec: CapEx & Sensitivity Views

**Status:** Complete
**Owner:** Reid W
**Created:** 2026-04-05 22:20 PDT
**Complexity:** MEDIUM
**Branch:** ralph/concept-explorer
**Epic:** EXPLORER-UX-V2, Item 3b

---

## Business Goals

### Why This Matters

The comparison shell is live with Categorical and Summary views rendering real content. CapEx and Sensitivity are the remaining two view types — they provide deeper drill-down into capital cost structure (which CAS accounts drive cost?) and parameter sensitivity (which parameters matter most for LCOE?) that the Summary view's headline metrics don't cover. Together with Categorical and Summary, they complete the four-view analysis workflow: taxonomy context -> headline economics -> capital drill-down -> sensitivity ranking.

### Success Criteria

- [ ] CapEx view renders grouped horizontal bar charts in both modes, improving on current stacked bars for cross-concept comparison
- [ ] CAS22 sub-accounts are expandable in both modes
- [ ] Sensitivity view renders filtered tornado charts in both modes with shared parameters emphasized
- [ ] Both views degrade gracefully for concepts without cost models or sensitivities
- [ ] Both views follow the VIEW_REGISTRY rendering contract from Item 3a

### Priority

Next on critical path: Item 2 (done) -> Item 3a (done) -> **Item 3b** -> Item 4.

---

## Problem Statement

### Current State

The comparison page view dropdowns offer "CapEx" and "Sensitivity" but render placeholder cards ("View renderer not yet registered"). The existing `cas_breakdown.js` and `tornado.js` are designed for single-concept profile pages — they don't support cross-concept comparison on shared axes, integrated grouping, or the `VIEW_REGISTRY` rendering contract.

### Desired Outcome

Selecting "CapEx" or "Sensitivity" from any view dropdown renders real Plotly charts in both Integrated and Landscape modes, with cross-concept comparison on shared axes and consistent visual treatment.

---

## Scope

### In Scope

- **CapEx View** (`view_capex.js`): grouped horizontal bar chart comparing CAS accounts across concepts, with CAS22 sub-account drill-down
- **Sensitivity View** (`view_sensitivity.js`): tornado charts with top-N filtering, shared-parameter emphasis in Integrated mode, synced axes in Landscape mode
- **CSS** for chart layouts and drill-down controls
- **Script tag additions** to `compare.html.j2`

### Out of Scope

- Changes to `comparison.js` — views register on existing `VIEW_REGISTRY`
- Changes to data models (`CostModelData`, `SensitivityAnalysis`, `CASAccount`) or API endpoints
- Parameter metadata popovers in comparison context (concept profile feature)
- Population whiskers (concept profile feature, not comparison)
- Slider-driven recomputation on comparison page
- Server-side changes

### Edge Cases & Considerations

- Concepts without cost models (`has_cost_model === false`): both views MUST show placeholder, not crash
- Concepts with zero-cost CAS accounts: render as zero-width bars, don't omit
- Concepts with `overridden: true` CAS accounts: carry over the star annotation from `cas_breakdown.js`
- Mixed selection (some concepts with cost models/sensitivities, some without): render what's available, placeholder the rest
- Sensitivity parameters unique to one concept: still shown in Integrated mode, just with a single bar
- CAS22 sub-accounts with all-zero values: still show the drill-down toggle, render empty state

---

## Requirements

### Functional Requirements

#### CapEx View

1. **FR-1**: CapEx view MUST render grouped horizontal bar charts comparing the 17 top-level CAS accounts (cas10 through cas90) across selected concepts.

2. **FR-2**: Chart type MUST be grouped horizontal bars — CAS accounts as y-axis categories, cost (M$) as x-axis, concepts grouped side-by-side per account. This is the best format for cross-concept comparison.

3. **FR-3**: In Integrated mode, concepts MUST be distinguished by family-based colors with opacity stepping (same scheme as Summary view). In Landscape mode, bars SHOULD use the `CAS_COLORS` palette from `cas_breakdown.js` for CAS account identity (single concept per panel, so no grouping ambiguity).

4. **FR-4**: CAS22 ("Reactor Plant Equipment") MUST be expandable to show the 14 sub-accounts (C220101 through C220700). A dedicated toggle button below the chart controls expand/collapse (not click-on-bar, which is ambiguous in grouped mode with multiple concepts).

5. **FR-5**: Overridden CAS accounts (`overridden: true`) MUST be annotated with a visual indicator (star/asterisk), consistent with `cas_breakdown.js`.

6. **FR-6**: In Integrated mode, CapEx MUST render a single grouped chart with all concepts on shared axes. Concepts are distinguished by color (using family colors or a concept color scale).

7. **FR-7**: In Landscape mode, CapEx MUST render per-concept horizontal bar charts with synced x-axis scale (same range across all panels).

8. **FR-8**: CapEx MUST degrade gracefully for concepts without cost models — show "No cost model available" placeholder in that concept's position, no JS error.

9. **FR-9**: Zero-cost CAS accounts MUST be included in the chart (zero-width bar), not omitted.

#### Sensitivity View

10. **FR-10**: Sensitivity view MUST render tornado charts showing parameter elasticities (dimensionless, from `SensitivityEntry.elasticity`) ranked by absolute magnitude.

11. **FR-11**: Filtering MUST use top-N = 8 per concept. In Integrated mode, the parameter set is the **union** of all concepts' top-8 parameters.

12. **FR-12**: In Integrated mode, Sensitivity MUST render a single grouped tornado chart with parameters as y-axis categories, elasticity as x-axis, and concepts grouped side-by-side per parameter. Parameters MUST be sorted with shared parameters (appearing in multiple concepts' top-8) at the top, then unique parameters below.

13. **FR-13**: In Landscape mode, Sensitivity MUST render per-concept tornado charts with synced x-axis scale (same elasticity range across all panels). Each panel shows that concept's own top-8 parameters.

14. **FR-14**: Sensitivity MUST combine engineering and financial parameter groups into a single ranked list (no separate sections by group).

15. **FR-15**: Confidence encoding SHOULD be carried over from `tornado.js` — opacity levels (high=1.0, medium=0.8, low=0.6) and diagonal hatch fill for low-confidence parameters — when `parameter_metadata` is available.

16. **FR-16**: Sensitivity MUST degrade gracefully for concepts without sensitivity data (`has_sensitivities === false` or `sensitivities === null`) — show "No sensitivity data available" placeholder, no JS error.

17. **FR-17**: Parameters unique to one concept in Integrated mode MUST still be shown (single bar), not filtered out.

#### View Rendering Contract

18. **FR-18**: Both views MUST register on `window.VIEW_REGISTRY` using the established contract:
    - `VIEW_REGISTRY.capex.renderIntegrated(container, conceptDataArray)`
    - `VIEW_REGISTRY.capex.renderLandscape(container, conceptData, syncContext)`
    - `VIEW_REGISTRY.sensitivity.renderIntegrated(container, conceptDataArray)`
    - `VIEW_REGISTRY.sensitivity.renderLandscape(container, conceptData, syncContext)`
    - Where `conceptDataArray` is `Array<{concept_id, name, confinement_family, data: ConceptData}>`
    - Where `conceptData` is a single such object
    - Where `syncContext` is `{allConcepts, sharedScales}`

19. **FR-19**: View scripts MUST be loaded after `comparison.js` (which defines `window.VIEW_REGISTRY`) and register their functions on DOMContentLoaded or immediately if DOM is ready.

#### Axis Synchronization

20. **FR-20**: CapEx Landscape mode MUST compute a shared x-axis max across all concepts' maximum single-account cost (not total capital cost, since bars represent individual accounts) and apply it to all panels.

21. **FR-21**: Sensitivity Landscape mode MUST compute a shared x-axis range (symmetric around zero) across all concepts' maximum absolute elasticity and apply it to all panels.

22. **FR-22**: Axis sync MUST exclude concepts without cost models/sensitivities from scale computation (not treated as zero).

---

## Acceptance Criteria

### Core Functionality

- [ ] Selecting "CapEx" in any view dropdown renders grouped horizontal bars (not a placeholder)
- [ ] Selecting "Sensitivity" in any view dropdown renders tornado charts (not a placeholder)
- [ ] CapEx Integrated: single grouped chart, concepts side-by-side per CAS account, shared axis
- [ ] CapEx Landscape: per-concept bar charts with synced x-axis scale
- [ ] CapEx CAS22 drill-down: toggle button expands to show 14 sub-accounts in both modes
- [ ] Sensitivity Integrated: grouped tornado, union of top-8, shared params sorted to top
- [ ] Sensitivity Landscape: per-concept top-8 tornado charts with synced axis
- [ ] CapEx with concept that has no cost model: shows placeholder, no console errors
- [ ] Sensitivity with concept that has no sensitivities: shows placeholder, no console errors
- [ ] Mixed concepts (some with data, some without): renders what's available

### Quality & Integration

- [ ] No changes to `comparison.js` — views register on existing `VIEW_REGISTRY`
- [ ] Existing comparison shell behavior unchanged (mode toggle, concept picker, URL state)
- [ ] Existing Categorical and Summary views unaffected
- [ ] Existing concept profile page charts (`tornado.js`, `cas_breakdown.js`) unaffected
- [ ] No new API endpoints required — data from existing `/api/concepts/{id}` and `/api/parameter_index`

---

## Data Contracts (Reference)

### CapEx Input Data

Per concept (from `conceptData.data.cost_model`):
- `cas10` through `cas90`: `{name: string, cost_m_usd: number, overridden: boolean}`
- `cas22_detail`: `Record<string, {name: string, cost_m_usd: number, overridden: boolean}>` (14 sub-accounts, keys C220101–C220700)

### Sensitivity Input Data

Per concept (from `conceptData.data.cost_model`):
- `sensitivities.engineering`: `Record<paramName, {elasticity: number, baseline: number}>`
- `sensitivities.financial`: `Record<paramName, {elasticity: number, baseline: number}>`

Per concept (from `conceptData.data`):
- `parameter_metadata`: `Record<paramName, {display_name: string, category: string, confidence: string, ...}>`

Cross-concept (from `/api/parameter_index`):
- Population elasticity ranges for whisker display (optional, deprioritized for comparison views)

### Existing Reusable Patterns

- `CAS_COLORS` palette (17 colors) from `cas_breakdown.js`
- Confidence opacity/hatch encoding from `tornado.js`
- `computeSharedScales()` pattern from `view_summary.js` (view-local, not a shared import)
- Concept color assignment via `FAMILY_COLORS` from `comparison.js`

---

## Related Artifacts

- **Concept:** `.project/active/explorer-ux-v2/concept.md`
- **Epic:** `.project/backlog/epic_explorer_ux_v2.md` (Item 3b)
- **Item 3a spec:** `.project/active/views-categorical-summary/spec.md` (rendering contract reference)
- **Item 3a design:** `.project/active/views-categorical-summary/design.md` (implementation patterns)
- **Shell code:** `exploration/concept_explorer/static/js/comparison.js`
- **Existing CAS chart:** `exploration/concept_explorer/static/js/cas_breakdown.js`
- **Existing tornado chart:** `exploration/concept_explorer/static/js/tornado.js`
- **Design:** `.project/active/views-capex-sensitivity/design.md` (to be created)

---

**Next Steps:** After approval, proceed to `/_my_design`
