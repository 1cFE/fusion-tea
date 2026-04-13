---
date: 2026-04-12T00:00:00-07:00
researcher: Claude
topic: "Cytoscape.js CoSE layout spacing controls and fit:true interaction"
tags: [research, visualization, cytoscape, concept-explorer]
status: complete
last_updated: 2026-04-12
---

# Research: Cytoscape.js Graph Spacing in Fitted CoSE Layouts

**Date**: 2026-04-12
**Researcher**: Claude
**Research Type**: Domain / Integration

## Research Question

How to increase visual whitespace between nodes in a Cytoscape.js CoSE graph that uses `fit: true`. What levers exist, and how does `fit: true` interact with force-directed layout parameters?

## Summary

- **`fit: true` is a viewport-only operation** (pan + zoom) -- it does NOT modify node positions. Proportionally scaling all force parameters produces identical visual results after fit.
- **Force *ratios* DO matter** -- changing repulsion/gravity ratio changes layout topology (cluster separation, uniformity), which survives fit.
- **`spacingFactor` is the most direct lever** but only works with `animate: 'end'` or `animate: false` in the built-in `cose` layout (it goes through `layoutPositions()` which applies the multiplier before fit).
- **Node/font size reduction** is the simplest approach -- nodes occupy less screen area, so whitespace-to-node ratio increases within the fitted viewport.
- **Recommended approach**: Switch from `animate: true` to `animate: 'end'` and add `spacingFactor: 1.8`. Two-line change.

## Detailed Findings

### 1. How fit:true Interacts with CoSE Parameters

The built-in `cose` layout has two code paths:

**`animate: true` (current config)**: Runs force simulation via `requestAnimationFrame`. On each frame, calls `nodes.positions(getScaledPos)` then `cy.fit(options.padding)`. At completion, `done()` calls `refresh()` which does `cy.fit()` one final time. This path does NOT go through `layoutPositions()`, so **`spacingFactor` and `transform` are ignored**.

**`animate: 'end'` or `animate: false`**: Simulation runs to completion, then calls `nodes.layoutPositions(layout, options, getScaledPos)` which IS the discrete pathway. `layoutPositions()` applies spacingFactor and transform before fit.

**Key implication**: Since `cy.fit()` only adjusts the camera (not node positions), proportional scaling of force parameters (e.g., doubling both repulsion and idealEdgeLength) produces a 2x larger layout in absolute coordinates that fit zooms out to show -- yielding **identical** visual appearance. Only ratio changes (e.g., repulsion up, gravity unchanged) change the layout topology, which does survive fit.

Source: `cytoscape.js/src/extensions/layout/cose.mjs`, `cytoscape.js/src/collection/layout.mjs`

### 2. spacingFactor Support by Layout

| Layout | spacingFactor | Alternative spacing control |
|--------|--------------|---------------------------|
| **cose** (built-in) | Yes, but only with `animate: 'end'` or `false` | Force ratios |
| **fcose** | No | `nodeSeparation: 75`, constraints |
| **cose-bilkent** | No | `idealEdgeLength`, `nodeRepulsion` |
| **cola** | No | `nodeSpacing: function(node){ return 10; }` |
| **elk** | No | ELK's own `spacing.*` parameters |
| **breadthfirst** | Yes (default 1.75) | `spacingFactor` |
| **concentric/circle/grid** | Yes | `spacingFactor` |

**How spacingFactor works in `layoutPositions()`:**
1. Compute position via layout callback
2. Scale each position as a vector from bounding box center by `spacingFactor`
3. Apply `transform` function (if provided)
4. Apply `fit` / `zoom` / `pan` viewport operations

Since positions are scaled before fit, spacingFactor changes the **ratio of inter-node distance to node size** -- which is exactly what produces visible whitespace differences.

### 3. fcose vs cose Spacing Controls

| Parameter | fcose | cose (built-in) |
|-----------|-------|-----------------|
| `quality` | `'draft'`/`'default'`/`'proof'` | No |
| `nodeSeparation` | `75` (spectral phase) | No |
| `idealEdgeLength` | `edge => 50` (function OK) | `edge => 32` (function OK) |
| `nodeRepulsion` | `node => 4500` | `node => 2048` |
| `spacingFactor` | No | Only with animate != true |
| `packComponents` | Yes (needs layout-utilities ext) | `componentSpacing: 40` |
| `nodeDimensionsIncludeLabels` | Yes (proof quality only) | Yes |
| `tilingPaddingVertical/Horizontal` | `10`/`10` | No |
| Constraint support | `fixedNodeConstraint`, `alignmentConstraint`, `relativePlacementConstraint` | No |

fcose's `quality: 'proof'` with `nodeDimensionsIncludeLabels: true` accounts for label bounding boxes in overlap prevention -- directly relevant to the cramped-labels problem.

### 4. Complete Lever Inventory

Ranked by directness of effect on visual whitespace:

1. **spacingFactor** -- Position multiplier before fit. Value of 2.0 doubles inter-node distances relative to node size. Requires `animate: 'end'` or `false` for built-in cose.

2. **Node size reduction** -- Stylesheet change (`width`/`height`). Nodes occupy less screen area; whitespace ratio increases. Works with any animation mode. Most reliable.

3. **Font size reduction** -- Especially effective with `nodeDimensionsIncludeLabels: true`. Smaller labels = smaller effective bounding boxes.

4. **`padding`** -- Layout option (default 50). Increases empty border around graph. Increasing it shrinks the area available for nodes, effectively scaling everything down (including nodes). Quick way to add breathing room at edges.

5. **Force ratio changes** -- Increasing repulsion while decreasing gravity changes layout topology (more uniform spacing, less center-clustering). Changes structure, not whitespace ratio. Effects survive fit.

6. **Post-layout position scaling** -- In the `stop` callback: scale all positions from center of mass, then call `cy.fit()`. Manual version of spacingFactor. Works with any animation mode.

7. **`transform` option** -- `transform: (node, pos) => ({ x: pos.x * 2, y: pos.y * 2 })`. Applied before fit in `layoutPositions()`. Same limitations as spacingFactor (needs `animate: 'end'`).

8. **Manual zoom/pan instead of fit** -- Set `fit: false`, use `cy.zoom()` + `cy.pan()` or `cy.fit(eles, largePadding)`. Full control but requires manual viewport management.

9. **`maxZoom`** -- Prevents fit from zooming in too much on small graphs. Not useful when fit zooms out.

10. **Container sizing** -- Larger container = more pixels. With fit, this doesn't change logical layout but reduces visual crowding at pixel level.

11. **Different layout algorithm** -- fcose's `nodeSeparation` provides explicit minimum gap. Cola's `nodeSpacing` is similar.

### 5. Current Implementation State

File: `exploration/concept_explorer/static/js/neighborhood_graph.js`

Current layout config (lines 597-627):
- `name: "cose"`, `animate: true`, `fit: true`, `padding: 50`
- `nodeRepulsion`: 24000 (regular) / 12000 (bridge) -- already increased from earlier values
- `idealEdgeLength`: 540 (regular) / 420 (bridge) -- already increased
- `gravity: 0.08` -- already low
- Node sizes: center 40px, neighbor 28px, bridge 22px (lines 326, 349, 389)
- Font sizes: center 10px, neighbor 9px, bridge 8px (lines 329, 351, 393)

The force parameters are already quite large, but since `animate: true` means `cy.fit()` runs every frame, making them larger has no visual effect.

## Code Examples

### Approach A: spacingFactor (RECOMMENDED -- 2-line change)

```javascript
// In render(), change layout config:
layout: {
  name: "cose",
  animate: "end",           // was: true
  animationDuration: 500,
  fit: true,
  padding: 50,
  spacingFactor: 1.8,       // NEW -- tune between 1.5-3.0
  nodeRepulsion: function (node) {
    return node.hasClass("bridge") ? 12000 : 24000;
  },
  idealEdgeLength: function (edge) {
    return edge.hasClass("bridge") ? 420 : 540;
  },
  // ... rest unchanged
}
```

Trade-off: Lose progressive "settling" animation. Nodes animate to final positions in one step.

### Approach B: Node/font size reduction (simplest, no behavior change)

```javascript
// In buildStylesheet():
// Center: 40 -> 28, font 10px -> 8px
// Neighbor: 28 -> 20, font 9px -> 7px  
// Bridge: 22 -> 16, font 8px -> 6px
```

Trade-off: Smaller nodes may be harder to click/read.

### Approach C: Post-layout scaling (works with animate: true)

```javascript
// Replace stop callback:
stop: function () {
  if (!_cy) return;
  var nodes = _cy.nodes();
  var bb = nodes.boundingBox();
  var cx = (bb.x1 + bb.x2) / 2;
  var cyCenter = (bb.y1 + bb.y2) / 2;
  var scale = 2.5;
  
  nodes.positions(function (node) {
    var pos = node.position();
    return {
      x: cx + (pos.x - cx) * scale,
      y: cyCenter + (pos.y - cyCenter) * scale
    };
  });
  
  _cy.animate({
    fit: { eles: _cy.elements(), padding: 50 }
  }, { duration: 300 });
  
  _cy.elements(".bridge").hide();
}
```

Trade-off: More code, but preserves progressive animation during layout.

## Recommendations

1. **Start with Approach A** (`animate: 'end'` + `spacingFactor: 1.8`). It's a 2-line change and directly addresses the problem.
2. **Combine with moderate node size reduction** if needed (e.g., center 32px, neighbor 24px -- not as aggressive as Approach B).
3. **If progressive animation is important**, use Approach C instead of A.
4. Consider `padding: 80` (from 50) for additional breathing room at container edges.
5. `nodeDimensionsIncludeLabels: true` may help prevent label overlaps (test with current node count).

## Open Questions

- Does the `stop` callback fire correctly with `animate: 'end'`? (Should be tested -- the bridge-hiding logic depends on it.)
- With ~10-15 visible nodes + bridges, is `spacingFactor: 1.8` enough or does it need to be higher?
- Would switching to fcose with `quality: 'proof'` and `nodeDimensionsIncludeLabels: true` be worth the added dependency?
