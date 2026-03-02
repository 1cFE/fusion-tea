# Spec: Visualization Options

**Status:** Draft
**Owner:** Reid Westwood
**Created:** 2026-01-19 02:06:57 UTC
**Complexity:** MEDIUM
**Branch:** visualization

---

## Business Goals

### Why This Matters
The visualization system from the POC sprint produces containment diagrams that are functional but have usability issues. Labels on borders are hard to read, the nested-box style doesn't scale well to large models, and the cost coloring feature isn't working correctly. These issues reduce the visualization's value for understanding and communicating model structure.

### Success Criteria
- [ ] Users can choose between visualization styles suited to their model size
- [ ] Labels are clearly readable without cluttering the diagram
- [ ] Cost-based coloring accurately distinguishes cost levels across elements

### Priority
Follow-on work to the completed POC sprint. Addresses usability feedback before broader adoption.

---

## Problem Statement

### Current State
- **Labels**: Subsystem names are positioned on container borders (`text-valign: 'top'`), making them hard to read, especially when boxes are small or densely packed
- **Layout**: Only nested-box (compound node) layout is available; deep hierarchies become visually overwhelming
- **Color Coding**: Cost-based gradient uses global min/max normalization, which causes parent containers (with aggregated costs) to dominate the color scale. Children cluster in the low end of the gradient, making distinctions hard to see.

### Desired Outcome
- **Labels**: Option to position labels inside boxes for better readability
- **Layout**: Tree/hierarchy view alternative for better scalability with large models
- **Color Coding**: Percentage-of-parent coloring that shows cost distribution within each subsystem

---

## Scope

### In Scope
1. **Label positioning option**: Inside-box labels vs border labels (user toggle)
2. **Tree layout alternative**: Hierarchical tree diagram as alternative to nested boxes
3. **Cost coloring fix**: Debug and fix the cost gradient to work correctly

### Out of Scope
- Changes to data extraction or SysML model parsing
- New cost metrics or attributes
- Complete UI redesign
- Other layout styles (radial, sunburst, etc. - future work)
- External legend system (future work)

### Edge Cases & Considerations
- Deep hierarchies (5+ levels) should remain readable in tree view
- Label truncation for long names in inside-box mode
- Cost coloring behavior when some nodes lack cost data
- Switching between layouts should preserve selection/expansion state if possible

---

## Requirements

### Functional Requirements

> Requirements below are from user's request unless marked [INFERRED]

1. **FR-1**: Provide option to position subsystem labels inside the container box rather than on the border
2. **FR-2**: Provide tree/hierarchy layout as an alternative to nested-box (compound node) layout
3. **FR-3**: Implement percentage-of-parent cost coloring - each node colored by `node_cost / parent_cost`
4. **FR-4**: [INFERRED] User can toggle between layout styles via UI control
5. **FR-5**: [INFERRED] User can toggle between label positioning styles via UI control

### Non-Functional Requirements

- Layout switching should be responsive (< 500ms for models with 100 nodes)
- Visual consistency: both layouts should use same color scheme and selection behavior

---

## Acceptance Criteria

### Core Functionality
- [ ] Inside-box label option exists and is toggleable
- [ ] When enabled, labels appear centered inside containers, not on borders
- [ ] Tree layout option exists and is toggleable
- [ ] Tree layout displays same hierarchy as nested-box view
- [ ] Cost coloring uses percentage-of-parent calculation
- [ ] Cost drivers are visually distinguishable within each subsystem
- [ ] Root node displays with neutral color (no parent reference)
- [ ] Coloring strategy is implemented as swappable (enum/flag)

### Quality & Integration
- [ ] Existing tests continue to pass
- [ ] Both layouts work with expand/collapse functionality
- [ ] Export to PNG works for both layouts
- [ ] No regression in load time for coffee_maker test model

---

## Technical Notes

### Relevant Files (from investigation)
- `proof_of_concept/web/static/index.html` - Frontend rendering, Cytoscape.js configuration
  - Lines 260-270: Label positioning styles
  - Lines 327-335: Dagre layout configuration
  - Lines 563-593: Cost coloring logic
- `proof_of_concept/extraction/visualization.py` - Data extraction (likely unchanged)

### Cost Coloring Analysis

Investigation revealed the current implementation is working correctly but uses **global min/max normalization**. With the coffee maker test data:
- Root (`coffee_maker`) has highest cost (113.96) → full red
- Children cluster in 0.02-0.27 normalized range → subtle color differences
- Parent containers visually dominate due to size + intense color

**Solution: Percentage-of-parent coloring**

Each node colored by `child_cost / parent_cost`:
- Shows cost distribution within each subsystem
- Highlights cost drivers at each level (e.g., `panel` is 86% of `housing` cost)
- Root node gets neutral color (no parent to compare against)

Example from test data:
| Element | Cost | % of Parent | Visual |
|---------|------|-------------|--------|
| brewing | 55.35 | 48.6% of coffee_maker | Medium |
| panel | 29.60 | 86.0% of housing | High - cost driver! |
| shell | 4.80 | 14.0% of housing | Low |

### Design Constraint

**The coloring method MUST be implemented as a swappable strategy** (hard flag/enum) to allow future alternatives:
- `percent_of_parent` (initial implementation)
- `global_minmax` (current behavior, for reference)
- `per_level` (normalize within each depth level - future)

This enables experimentation and user preference without restructuring.

---

## Related Artifacts

- **POC Code:** `proof_of_concept/` directory
- **Test Fixtures:** `proof_of_concept/golden_references/`
- **Design:** `.project/active/visualization-options/design.md` (to be created)

---

**Next Steps:** After approval, proceed to `/_my_design`
