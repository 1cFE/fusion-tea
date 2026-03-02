# Design: Visualization Options

**Status:** Draft
**Owner:** Reid Westwood
**Created:** 2026-01-19 02:27:24 UTC
**Branch:** visualization
**Commit:** 1162372

---

## Overview

Add configurable visualization options to improve diagram readability: inside-box labels, tree layout alternative, and percentage-of-parent cost coloring with swappable strategy support.

## Related Artifacts

- **Spec:** `.project/active/visualization-options/spec.md`
- **POC Code:** `proof_of_concept/`
- **Frontend:** `proof_of_concept/web/static/index.html`

---

## Research Findings

### Current Implementation Analysis

**File:** `proof_of_concept/web/static/index.html`

1. **Label Positioning** (lines 259-270, 283-291)
   - Container nodes use `text-valign: 'top'` with `text-margin-y: 8` - positions label on border
   - Leaf nodes (`:childless` selector) override to `text-valign: 'center'` - positions inside
   - Switching requires changing these style properties dynamically

2. **Layout** (lines 327-335, 338-351)
   - Uses Dagre layout with `rankDir: 'TB'` (top-to-bottom)
   - Compound nodes (parent property) create nested boxes automatically
   - Expand-collapse extension configured with same Dagre layout for animations

3. **Cost Coloring** (lines 563-593)
   - `applyCostStyling(enabled)` function toggles coloring on/off
   - Global min/max normalization: `t = (cost - minCost) / (maxCost - minCost)`
   - Gradient: `#e3f2fd` (light blue) → `#ff5252` (red)
   - Uses `capital_cost` attribute only

### Cytoscape.js Capabilities

**Label Positioning:**
- `text-valign`: `'top'` | `'center'` | `'bottom'`
- `text-halign`: `'left'` | `'center'` | `'right'`
- `text-margin-y`: pixel offset for fine-tuning
- Can be changed dynamically via `node.style('text-valign', 'center')`

**Tree/Hierarchy Layouts:**
- **Dagre** (current): Best for DAGs/trees, supports compound nodes
- **Breadthfirst**: Built-in, organizes nodes in BFS levels, supports `roots` option
- Both can be switched dynamically via `cy.layout({ name: 'breadthfirst', ... }).run()`

**Key Insight:** For tree layout, we need to either:
1. Keep compound nodes but use breadthfirst layout (may not work well with nesting)
2. Remove parent relationships and draw explicit edges for tree view

Sources: [Cytoscape.js Layouts](https://blog.js.cytoscape.org/2020/05/11/layouts/), [Dagre Layout](https://github.com/cytoscape/cytoscape.js-dagre), [Style Documentation](https://js.cytoscape.org/)

---

## Design Alternatives

### Tree Layout Approach

**Context:** The current implementation uses Cytoscape compound nodes (parent property) which automatically renders containment as nested boxes. For a tree view, we need a different approach.

**Option A: Breadthfirst Layout with Edge-Based Hierarchy**
- Remove `parent` property from node data when in tree mode
- Add explicit containment edges between nodes
- Use breadthfirst layout with root specified
- Pros: Clean tree visualization, no nesting
- Cons: Requires transforming data structure, losing compound node features

**Option B: Dagre Layout with Flattened Hierarchy**
- Same approach as Option A but stick with Dagre
- Dagre handles edge-based DAGs well
- Pros: Consistent with current codebase, good tree rendering
- Cons: Same data transformation needed

**Option C: Keep Compound Nodes, Different Visual Rendering**
- Keep parent relationships but style containers to look more tree-like
- Use minimal padding, no background fill on containers
- Pros: Minimal code change
- Cons: Still visually nested, may not achieve desired "tree" look

**Recommendation:** Option B (Dagre with flattened hierarchy). It reuses the existing Dagre dependency and provides a true tree visualization. The data transformation can be done client-side when switching layouts.

---

## Proposed Design

### 1. UI Controls

Add toggle controls to the control bar:

```html
<!-- After cost-styling-toggle -->
<label class="toggle-label">
  <input type="checkbox" id="labels-inside-toggle" disabled>
  Labels Inside
</label>

<select id="layout-select" disabled>
  <option value="containment">Containment</option>
  <option value="tree">Tree</option>
</select>
```

**Location:** `index.html:234-237` (after cost styling toggle)

### 2. Label Positioning Toggle

**Function:** `applyLabelStyle(labelsInside: boolean)`

```javascript
function applyLabelStyle(labelsInside) {
  if (!cy) return;

  // Update container nodes (non-leaf)
  cy.nodes().not(':childless').forEach(node => {
    if (labelsInside) {
      node.style({
        'text-valign': 'center',
        'text-margin-y': 0
      });
    } else {
      node.style({
        'text-valign': 'top',
        'text-margin-y': 8
      });
    }
  });
}
```

**Location:** Add after `applyCostStyling()` function (~line 593)

### 3. Tree Layout

**Approach:** Transform data to edge-based representation when tree layout selected.

**Function:** `transformToTreeData(elements)`

```javascript
function transformToTreeData(elements) {
  // Extract parent-child relationships as edges
  const nodes = [];
  const edges = [];

  elements.forEach(el => {
    const data = { ...el.data };
    const parentId = data.parent;
    delete data.parent;  // Remove compound relationship
    nodes.push({ data });

    if (parentId) {
      edges.push({
        data: {
          id: `${parentId}->${data.id}`,
          source: parentId,
          target: data.id
        }
      });
    }
  });

  return [...nodes, ...edges];
}
```

**Function:** `switchLayout(layoutType: 'containment' | 'tree')`

```javascript
function switchLayout(layoutType) {
  if (!cy || !originalElements) return;

  if (layoutType === 'tree') {
    const treeElements = transformToTreeData(originalElements);
    cy.json({ elements: treeElements });
    cy.layout({
      name: 'dagre',
      rankDir: 'TB',
      nodeSep: 80,
      rankSep: 100,
      fit: true,
      padding: 30
    }).run();
  } else {
    // Restore compound node structure
    cy.json({ elements: originalElements });
    cy.layout({
      name: 'dagre',
      rankDir: 'TB',
      nodeSep: 50,
      rankSep: 80,
      fit: true,
      padding: 30
    }).run();
  }

  // Re-apply current styling options
  applyCostStyling(document.getElementById('cost-styling-toggle').checked);
  applyLabelStyle(document.getElementById('labels-inside-toggle').checked);
}
```

**State:** Store original elements after load:
```javascript
let originalElements = null;  // Add to global state (line 313)

// In loadModel(), after successful fetch:
originalElements = data.elements;
```

**Location:** Add after label style function

### 4. Cost Coloring Strategy System

**Design Constraint from Spec:** Must be swappable via enum/flag.

**Strategy Enum:**
```javascript
const CostColorStrategy = {
  GLOBAL_MINMAX: 'global_minmax',
  PERCENT_OF_PARENT: 'percent_of_parent',
  // Future: PER_LEVEL: 'per_level'
};

let currentCostStrategy = CostColorStrategy.PERCENT_OF_PARENT;
```

**Strategy Functions:**

```javascript
// Strategy: Global min/max (existing behavior)
function computeGlobalMinMax(nodes, costAttr) {
  const costs = nodes
    .map(n => n.data(costAttr))
    .filter(v => typeof v === 'number');

  if (costs.length === 0) return null;

  const minCost = Math.min(...costs);
  const maxCost = Math.max(...costs);

  const result = new Map();
  nodes.forEach(node => {
    const cost = node.data(costAttr);
    if (typeof cost === 'number') {
      const t = maxCost > minCost ? (cost - minCost) / (maxCost - minCost) : 0;
      result.set(node.id(), t);
    }
  });
  return result;
}

// Strategy: Percentage of parent
function computePercentOfParent(nodes, costAttr) {
  const result = new Map();

  // Build parent lookup
  const nodeMap = new Map();
  nodes.forEach(n => nodeMap.set(n.id(), n));

  nodes.forEach(node => {
    const cost = node.data(costAttr);
    const parentId = node.data('parent');

    if (typeof cost !== 'number') return;

    if (!parentId) {
      // Root node - neutral color (t = 0)
      result.set(node.id(), 0);
      return;
    }

    const parent = nodeMap.get(parentId);
    const parentCost = parent ? parent.data(costAttr) : null;

    if (typeof parentCost === 'number' && parentCost > 0) {
      // Percentage of parent (capped at 1.0)
      const t = Math.min(cost / parentCost, 1.0);
      result.set(node.id(), t);
    } else {
      result.set(node.id(), 0);
    }
  });

  return result;
}
```

**Refactored applyCostStyling:**

```javascript
function applyCostStyling(enabled) {
  if (!cy) return;

  if (enabled) {
    let intensities;

    switch (currentCostStrategy) {
      case CostColorStrategy.GLOBAL_MINMAX:
        intensities = computeGlobalMinMax(cy.nodes(), 'capital_cost');
        break;
      case CostColorStrategy.PERCENT_OF_PARENT:
        intensities = computePercentOfParent(cy.nodes(), 'capital_cost');
        break;
      default:
        intensities = computePercentOfParent(cy.nodes(), 'capital_cost');
    }

    if (!intensities) return;

    cy.nodes().forEach(node => {
      const t = intensities.get(node.id());
      if (t !== undefined) {
        const color = lerpColor('#e3f2fd', '#ff5252', t);
        node.style('background-color', color);
      }
    });
  } else {
    cy.nodes().forEach(node => {
      node.style('background-color', '#e3f2fd');
    });
  }
}
```

**Location:** Replace existing `applyCostStyling` function (lines 563-593)

### 5. Edge Styling for Tree View

Add edge styles to stylesheet (currently none exist):

```javascript
// Add to stylesheet array (line 310)
{
  selector: 'edge',
  style: {
    'width': 2,
    'line-color': '#1976d2',
    'target-arrow-color': '#1976d2',
    'target-arrow-shape': 'triangle',
    'curve-style': 'bezier'
  }
}
```

### 6. Event Handlers

Add to DOMContentLoaded handler (after line 637):

```javascript
// Labels inside toggle
document.getElementById('labels-inside-toggle').addEventListener('change', function() {
  applyLabelStyle(this.checked);
});

// Layout select
document.getElementById('layout-select').addEventListener('change', function() {
  switchLayout(this.value);
});
```

Update `setButtonsEnabled()` to include new controls.

---

## File Changes Summary

| File | Changes |
|------|---------|
| `proof_of_concept/web/static/index.html` | Add UI controls, cost strategy system, label toggle, layout switching |

All changes are contained within a single file.

---

## Potential Risks

1. **Expand/collapse in tree mode**: The expand-collapse extension may not work with edge-based hierarchy.
   - Mitigation: Disable expand/collapse when in tree mode, or test compatibility.

2. **Selection state on layout switch**: Switching layouts rebuilds the graph, losing selection.
   - Mitigation: Store selected node ID, reselect after layout change.

3. **Performance with large models**: Rebuilding elements on layout switch adds overhead.
   - Mitigation: Only transform when needed; cache tree representation.

4. **Parent cost = 0 edge case**: Division by zero in percent-of-parent.
   - Mitigation: Already handled with `parentCost > 0` check.

---

## Validation Approach

1. **Manual Testing:**
   - Load coffee_maker model
   - Toggle "Labels Inside" - verify labels move inside container boxes
   - Switch to "Tree" layout - verify edges appear, hierarchy preserved
   - Enable "Color by Cost" - verify gradient shows cost distribution
   - Verify panel (86% of housing) appears more intense than shell (14%)

2. **Acceptance Criteria Verification:**
   - [ ] Inside-box label toggle works
   - [ ] Tree layout shows same hierarchy as containment view
   - [ ] Cost coloring uses percentage-of-parent
   - [ ] Root node is neutral color
   - [ ] Strategy is swappable (change `currentCostStrategy` constant)

3. **Regression:**
   - Existing tests in `proof_of_concept/tests/` should still pass (data extraction unchanged)
   - PNG export works in both layouts

---

**Next Steps:** After approval, proceed to `/_my_implement`
