# Spec: Categorical & Summary Views

**Status:** Complete
**Owner:** Reid W
**Created:** 2026-04-05 20:00 PDT
**Complexity:** MEDIUM
**Branch:** ralph/concept-explorer
**Epic:** EXPLORER-UX-V2, Item 3a

---

## Business Goals

### Why This Matters

The comparison shell (Item 2) is live but renders placeholder panels. Categorical and Summary are the highest-value views for the immediate sanity-checking use case: Categorical lets users correlate taxonomy differences (fuel, magnet type, energy capture) with economic differences, and Summary lets users compare headline economics across concepts. Together they answer the question "how do these concepts differ and what does that mean for cost?"

### Success Criteria

- [ ] Categorical view renders taxonomy attributes in a readable comparison format in both modes
- [ ] Summary view renders headline economics comparison in both modes
- [ ] Summary view degrades gracefully for concepts without cost models (placeholder, no JS error)
- [ ] Landscape mode synchronizes axes/scales across concept panels
- [ ] View rendering API contract is established and documented for Item 3b to follow

### Priority

Next on the critical path: Item 2 (complete) → **Item 3a** → Item 3b → Item 4.

---

## Problem Statement

### Current State

The comparison page shell renders placeholder cards that say "View renderer not yet registered" for all four view types. The `VIEW_REGISTRY` in `comparison.js` has null render functions for `categorical` and `summary`. No Categorical or Summary view exists anywhere in the explorer.

### Desired Outcome

Selecting "Categorical" or "Summary" from a view dropdown renders real content — taxonomy attribute comparisons and headline economics charts — in both Integrated and Landscape modes.

---

## Scope

### In Scope

- **Categorical View** (`view_categorical.js`): taxonomy attribute comparison table/cards
- **Summary View** (`view_summary.js`): headline economics comparison chart + metrics table
- **View rendering API contract**: `renderIntegrated(container, conceptDataArray)` and `renderLandscape(container, conceptData, syncContext)` registration on `window.VIEW_REGISTRY`
- **Axis synchronization utility**: shared scale computation for Landscape mode panels (reusable by Item 3b)
- **CSS** for table and chart layouts
- **Script tag additions** to `compare.html.j2`

### Out of Scope

- CapEx and Sensitivity views (Item 3b)
- HeadlineEconomics data model changes — current 5 scalar fields are sufficient for v1
- LCOE decomposition chart (requires HeadlineEconomics refinement; deferred)
- Slider-driven recomputation on comparison page
- Changes to `comparison.js` (shell is complete; views register on the existing `VIEW_REGISTRY`)
- Server-side changes

### Edge Cases & Considerations

- Concepts without cost models (`has_cost_model === false`): Summary view must show a clear placeholder, not crash
- Concepts with partial data (e.g., `cost_model` exists but some CAS accounts are zero): render what's available
- Mixed selection (some concepts with cost models, some without): Summary Integrated mode must handle the mix gracefully
- Taxonomy fields with null/TBD values: display as "—" or "TBD", don't omit the row

---

## Requirements

### Functional Requirements

#### Categorical View

1. **FR-1**: Categorical view MUST render all taxonomy fields from the concept data as a comparison. Fields (from `concept_registry.json` taxonomy):
   - **Hierarchical**: confinement_family, mfe_topology, ife_driver, mif_method, non_standard_mechanism, tokamak_shape, stellarator_type, laser_approach
   - **Cross-cutting**: fuel, primary_heating, energy_capture, plasma_state, magnet_type, tritium_breeding, neutron_management, operation_mode, repetition_rate, driver_technology
   - **Metadata**: confidence

2. **FR-2**: In Integrated mode, Categorical MUST render a single merged comparison table with taxonomy fields as rows and concepts as columns.

3. **FR-3**: In Landscape mode, Categorical MUST render per-concept attribute cards showing all taxonomy fields.

4. **FR-4**: Null or TBD taxonomy values MUST display as readable placeholders ("—" or "TBD"), not be omitted or cause errors.

5. **FR-5**: [INFERRED] Hierarchical fields that don't apply to a concept's confinement family (e.g., `mfe_topology` for an IFE concept) SHOULD be visually distinguished from fields that apply but are unknown — e.g., show "—" for inapplicable vs. "TBD" for applicable-but-unknown.

#### Summary View

6. **FR-6**: Summary view MUST render a comparison chart of the 5 HeadlineEconomics metrics: LCOE ($/MWh), overnight cost ($/kW), P_net (MW), Q_eng, capacity factor.

7. **FR-7**: Summary view MUST render a key metrics table below/alongside the chart showing the same 5 values in tabular form with units.

8. **FR-8**: [INFERRED] Summary view SHOULD identify and display the top CAS driver (name + % of total capital cost) per concept as a hint toward the CapEx view.

9. **FR-9**: In Integrated mode, Summary MUST render concepts grouped/overlaid on shared axes for direct comparison.

10. **FR-10**: In Landscape mode, Summary MUST render per-concept panels with synchronized scales (same axis range across all panels).

11. **FR-11**: Summary view MUST degrade gracefully for concepts without cost models — show a clear "No cost model available" placeholder in that concept's position, not a JS error.

12. **FR-12**: In Integrated mode with a mix of concepts (some with cost models, some without), Summary MUST render the chart for concepts that have data and show inline placeholders for those that don't.

#### View Rendering Contract

13. **FR-13**: Each view file MUST register its render functions on `window.VIEW_REGISTRY` using the existing contract:
    - `VIEW_REGISTRY.{viewName}.renderIntegrated = function(container, conceptDataArray) { ... }`
    - `VIEW_REGISTRY.{viewName}.renderLandscape = function(container, conceptData, syncContext) { ... }`
    - Where `conceptDataArray` is `Array<{concept_id, name, confinement_family, data: ConceptData}>`
    - Where `conceptData` is a single such object
    - Where `syncContext` is `{allConcepts, sharedScales}`

14. **FR-14**: View scripts MUST be loaded after `comparison.js` (which defines `window.VIEW_REGISTRY`) and register their functions on DOMContentLoaded or immediately if DOM is ready.

#### Axis Synchronization

15. **FR-15**: An axis synchronization utility MUST compute shared scales (min/max ranges) across all concepts in a Landscape comparison, so that per-concept panels use consistent axes.

16. **FR-16**: The axis sync pattern (per-metric shared scale computation) MUST be established and documented so Item 3b views (CapEx, Sensitivity) can replicate it for their own data. A shared utility is NOT required — each view's scale semantics differ.

17. **FR-17**: The sync utility MUST handle missing data gracefully — concepts without cost models are excluded from scale computation, not treated as zero.

---

## Acceptance Criteria

### Core Functionality

- [x] Selecting "Categorical" in any view dropdown renders the taxonomy comparison (not a placeholder)
- [x] Selecting "Summary" in any view dropdown renders the economics comparison (not a placeholder)
- [x] Categorical Integrated: single table, concepts as columns, all taxonomy fields as rows
- [x] Categorical Landscape: per-concept cards with all taxonomy fields
- [x] Summary Integrated: grouped chart + metrics table on shared axes
- [x] Summary Landscape: per-concept chart panels with synced scales + metrics
- [x] Summary with concept that has no cost model: shows placeholder, no console errors
- [x] Summary with mixed concepts (some with, some without cost models): renders what's available
- [x] Null/TBD taxonomy values display cleanly in Categorical view

### Quality & Integration

- [x] No changes to `comparison.js` — views register on existing `VIEW_REGISTRY`
- [x] Existing comparison shell behavior unchanged (mode toggle, concept picker, URL state)
- [x] Existing taxonomy views, concept profile pages, and index grid unaffected
- [x] No new API endpoints required — Summary uses data from `/api/concepts/{id}`, Categorical uses existing `/api/taxonomy/registry`

---

## Related Artifacts

- **Concept:** `.project/active/explorer-ux-v2/concept.md`
- **Epic:** `.project/backlog/epic_explorer_ux_v2.md` (Item 3a)
- **Shell design:** `.project/active/compare-shell/design.md` (VIEW_REGISTRY contract)
- **Shell code:** `exploration/concept_explorer/static/js/comparison.js`
- **Design:** `.project/active/views-categorical-summary/design.md` (to be created)

---

**Next Steps:** After approval, proceed to `/_my_design`
