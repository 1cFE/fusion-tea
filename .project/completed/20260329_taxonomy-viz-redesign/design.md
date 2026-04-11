# Design: Taxonomy Visualization Redesign

**Status:** Draft
**Owner:** Reid W
**Created:** 2026-03-29 16:49 PDT
**Last Updated:** 2026-03-29 16:49 PDT
**Complexity:** HIGH
**Branch:** ralph/concept-explorer

---

## Overview

Replace the static constellation scatter and abstract dimension bars with a dynamic SVG neighborhood graph, field-level comparison panel, and bridge concept nodes. Restructure the page layout into a three-column design with collapsible tree sidebar, central graph area, and independently scrollable detail panel.

## Related Artifacts

- **Spec:** `.project/active/taxonomy-viz-redesign/spec.md`
- **Prior implementation:** `.project/active/concept-taxonomy-and-similarity/design.md`
- **Current JS:** `exploration/concept_explorer/static/js/{constellation,taxonomy,taxonomy_card,tree_view}.js`
- **Current CSS:** `exploration/concept_explorer/static/css/explorer.css` (lines 1200-1540)
- **Similarity API:** `exploration/concept_explorer/similarity.py` (result models lines 39-112)
- **Server endpoints:** `exploration/concept_explorer/server.py` (taxonomy routes lines 450-540)

---

## Research Findings

### Current Architecture

**Module pattern**: Each JS file is an IIFE exporting a public API object (`TreeView`, `Constellation`, `TaxonomyCards`). No build tools, no imports — script tag load order matters. Each module defines its own `el(tag, class, text)` DOM helper. (`taxonomy_card.js:5-10`, `tree_view.js:5-10`)

**Orchestrator**: `taxonomy.js` owns all state (`_registry`, `_selectedId`, `_similarityCache`) and wires components via a central `onConceptClick(conceptId)` callback. Components communicate through this single hub — no direct cross-component calls. (`taxonomy.js:10-14`, `71-115`)

**Plotly integration**: Constellation uses `Plotly.newPlot()` into a container div. Plotly owns that div's innerHTML. Click events via Plotly-specific `container.on("plotly_click", ...)`. Highlight updates via `Plotly.restyle()`. (`constellation.js:107-118`)

**No existing SVG**: Zero native SVG creation in the codebase. All graphical rendering is Plotly-internal. This is a blank slate for SVG work.

**CSS transitions**: Codebase uses conservative 0.15s transitions for hover states and 0.3s for layout changes. No fade-in/opacity transitions exist yet. Animations limited to spinner keyframes. (`explorer.css:154`, `230`, `1266`)

**Tooltip infrastructure**: A `.tooltip` CSS class exists (`explorer.css:599-611`) with absolute positioning, dark theme, and `pointer-events: none` — but it's never used in JS. The parameter card popover (`parameter_card.js:292-320`) is the only JS-driven overlay, using fixed positioning and click-outside dismissal.

**Layout**: Current taxonomy page is a 2-column CSS grid (`300px 1fr`) with sticky sidebar. (`explorer.css:1205-1227`). Main area is a vertical flex stack: constellation → taxonomy card → similarity card.

### API Data Available (No Changes Needed)

The existing `/api/taxonomy/similarity/{id}` endpoint returns everything needed for the comparison table:

- `comparison.dimensions[].matched_fields` / `mismatched_fields` — field names for matches and mismatches
- `bridges[].mismatched_field`, `query_value`, `similar_value` — actual values for differences
- `bridges[].bridge_concept_id`, `bridge_concept_name` — the cross-cutting connection

For matched field values, the client looks up both concepts in the already-loaded `_registry`. All 10 comparable fields are accessible as `concept[field_name]` on the ConceptTaxonomy object.

### One Small API Enhancement Needed

The bridge data currently lacks the overall similarity between the focused concept and the bridge concept. FR-10 requires prioritizing bridges by similarity. Since the similarity matrix is precomputed at server startup, this is a trivial lookup — add `bridge_overall_similarity: float` to the `DifferenceBridge` model. (~5 lines of server change.)

---

## Design Decisions

### DD-1: SVG with CSS Transitions (Not Plotly, Not D3)

**Decision:** Build the neighborhood graph as native SVG with CSS transitions for animation. No new libraries.

**Rationale:** Plotly is designed for charts, not interactive node-link graphs — it can't render heterogeneous node shapes, labeled edges, or dynamic node addition/removal. D3 would work but adds a ~90KB dependency for features we don't need (force simulation, complex scales). The graph has at most ~13 nodes (1 center + 5 neighbors + up to ~7 bridges) — native SVG with deterministic radial positioning is trivial. CSS `transition` on `transform` and `opacity` handles all animation needs.

**Pattern:** Create an `svgEl(tag, attrs)` helper using `document.createElementNS()`, following the existing `el()` convention.

### DD-2: Three-Column Layout

**Decision:** Restructure from 2-column (sidebar + main) to 3-column (tree | graph | detail panel).

**Rationale:** The user explicitly requires the similar-concepts panel to scroll independently without losing the graph. A right-side detail panel achieves this naturally — it's a fixed-height overflow-y container in its own grid column. The graph takes the fluid center column.

**Grid:** `grid-template-columns: var(--tree-width, 280px) auto 1fr 360px`
Four columns: sidebar | toggle button (`auto`) | graph (`1fr`) | detail panel.
When tree is collapsed: `--tree-width: 0px` with transition; toggle button column stays visible.

### DD-3: Fade Transition Between Views

**Decision:** Use opacity crossfade (constellation fades out, graph fades in) rather than animating nodes from MDS positions to radial positions.

**Rationale:** The user said "animate if possible, but whatever is more stable." The MDS coordinates and radial layout have no semantic mapping — animating between them would be visually confusing (nodes moving to arbitrary positions). A clean crossfade clearly communicates "you are now in a different view mode." Simpler to implement, more stable, less visual noise.

### DD-4: Tree Single-Click Focuses, Constellation Double-Click Focuses

**Decision:** In the tree, single-click focuses a concept (becomes graph center). In the constellation, double-click focuses. In the neighborhood graph, single-click compares, double-click re-centers.

**Spec override note:** FR-4 says "double-clicking a concept (in the graph, tree, or constellation)" — this decision deliberately changes tree interaction to single-click. Tree items are conventionally single-click targets; requiring double-click would feel broken and conflict with the existing tree behavior. The constellation keeps double-click to disambiguate from Plotly's pan/zoom. The neighborhood graph uses both: single-click is the lighter action (compare), double-click is the heavier action (re-center).

---

## Proposed Design

### Interaction State Machine

```
States:
  OVERVIEW     — Constellation visible, no concept focused
  FOCUSED      — Neighborhood graph visible, center concept selected, detail panel shows taxonomy card
  COMPARING    — FOCUSED + a neighbor is selected, comparison visible, bridge nodes visible

Transitions:
  OVERVIEW → FOCUSED:     Double-click concept in constellation, OR single-click in tree
  FOCUSED → COMPARING:    Single-click a neighbor node in graph
  COMPARING → COMPARING:  Single-click a different neighbor (bridges swap)
  COMPARING → FOCUSED:    Single-click center node or empty graph area (deselect neighbor)
  FOCUSED → FOCUSED:      Double-click a neighbor or bridge (re-center on new concept)
  COMPARING → FOCUSED:    Double-click a neighbor or bridge (re-center on new concept)
  Any → OVERVIEW:         Click "← Overview" button, OR press Escape key

  Tree interaction (any state):
    Single-click leaf → always focuses that concept (enters FOCUSED or re-centers)
```

### Component 1: Layout Restructure

**Files changed:** `templates/taxonomy.html.j2`, `templates/base.html.j2`, `static/css/explorer.css`

#### Template Structure (`taxonomy.html.j2`)

```html
<div class="taxonomy-layout">
  <!-- Column 1: Collapsible tree -->
  <aside class="taxonomy-sidebar" id="tree-panel">
    <div class="taxonomy-sidebar__header">
      <span class="taxonomy-sidebar__title">Decision Tree</span>
    </div>
    <div id="tree-container"><!-- TreeView renders here --></div>
  </aside>

  <!-- Collapse/expand toggle (positioned on sidebar edge) -->
  <button class="sidebar-toggle" id="sidebar-toggle"
          aria-label="Toggle decision tree" title="Toggle decision tree">
    ‹ <!-- chevron, flips on collapse -->
  </button>

  <!-- Column 2: Graph area -->
  <section class="taxonomy-graph" id="graph-area">
    <!-- View mode indicator + back button -->
    <div class="graph-header" id="graph-header">
      <button class="graph-header__back" id="back-to-overview"
              title="Return to design space overview (Esc)">← Overview</button>
      <span class="graph-header__title" id="graph-title">
        Design Space Overview
      </span>
      <span class="graph-header__subtitle" id="graph-subtitle">
        Concepts positioned by design attribute similarity
      </span>
    </div>
    <!-- Constellation (default, Plotly) -->
    <div id="constellation-container"></div>
    <!-- Neighborhood graph (on focus, SVG) -->
    <div id="neighborhood-container" style="display:none"></div>
  </section>

  <!-- Column 3: Detail panel (scrollable) -->
  <aside class="taxonomy-detail" id="detail-panel">
    <div id="detail-content">
      <!-- Taxonomy card renders here when concept focused -->
      <div id="taxonomy-card-container"></div>
      <!-- Comparison + neighbors render here -->
      <div id="comparison-container"></div>
    </div>
  </aside>
</div>
```

#### Nav Reordering (`base.html.j2`)

Move Taxonomy link to first position (before "All Concepts" and "Compare").

#### CSS Layout

```css
.taxonomy-layout {
  display: grid;
  grid-template-columns: var(--tree-width, 280px) auto 1fr 360px;
  /* columns: sidebar | toggle button | graph | detail panel */
  gap: 0;
  min-height: calc(100vh - 120px);
}

/* Collapsed state: sidebar width transitions to 0 */
.taxonomy-layout--collapsed {
  --tree-width: 0px;
}

.taxonomy-sidebar {
  overflow: hidden;           /* clips content during collapse animation */
  transition: width 0.3s ease;
  overflow-y: auto;
  max-height: calc(100vh - 120px);
  background: var(--color-surface-1);
  border-right: 1px solid var(--color-border);
  padding: var(--space-3);
}

.taxonomy-layout--collapsed .taxonomy-sidebar {
  width: 0;
  padding: 0;
  border: none;
}

.taxonomy-detail {
  overflow-y: auto;           /* independent scroll */
  max-height: calc(100vh - 120px);
  padding: var(--space-3);
  background: var(--color-surface-1);
  border-left: 1px solid var(--color-border);
}

.taxonomy-graph {
  display: flex;
  flex-direction: column;
  min-height: 0;              /* allow flex children to shrink */
}
```

### Component 2: SVG Neighborhood Graph

**New file:** `static/js/neighborhood_graph.js`
**Exports:** `NeighborhoodGraph.render(container, focusedConcept, neighbors, registry, callbacks)`, `NeighborhoodGraph.showBridges(neighborId, bridges)`, `NeighborhoodGraph.clearBridges()`, `NeighborhoodGraph.highlightBridge(conceptId)`, `NeighborhoodGraph.destroy()`

#### SVG Helper

```javascript
var SVG_NS = "http://www.w3.org/2000/svg";

function svgEl(tag, attrs) {
  var node = document.createElementNS(SVG_NS, tag);
  if (attrs) {
    for (var k in attrs) {
      node.setAttribute(k, attrs[k]);
    }
  }
  return node;
}
```

#### Layout Computation

Deterministic radial layout — no physics:

```javascript
var TOP_N = 5;  // easily configurable constant
var NEIGHBOR_RADIUS_FACTOR = 0.32; // proportion of smallest SVG dimension
var BRIDGE_RADIUS_FACTOR = 0.48;

function computeLayout(width, height, neighborCount) {
  var cx = width / 2, cy = height / 2;
  var radius = Math.min(width, height) * NEIGHBOR_RADIUS_FACTOR;
  var bridgeRadius = Math.min(width, height) * BRIDGE_RADIUS_FACTOR;
  var neighbors = [];
  for (var i = 0; i < neighborCount; i++) {
    var angle = (i / neighborCount) * 2 * Math.PI - Math.PI / 2; // start from top
    neighbors.push({
      x: cx + radius * Math.cos(angle),
      y: cy + radius * Math.sin(angle),
      angle: angle
    });
  }
  return { cx: cx, cy: cy, radius: radius, bridgeRadius: bridgeRadius, neighbors: neighbors };
}
```

Bridge positions: placed at `bridgeRadius`, angularly offset from the neighbor they relate to. If a neighbor at angle θ has 2 bridges, they go at θ-0.15 and θ+0.15 radians.

#### SVG Structure

```
<svg viewBox="0 0 {w} {h}" class="neighborhood-graph">
  <defs>
    <!-- arrowhead marker for bridge edges (optional) -->
  </defs>
  <g class="ng-edges">
    <!-- similarity edges: solid lines, center → neighbor -->
    <g class="ng-edge ng-edge--similarity">
      <line x1="{cx}" y1="{cy}" x2="{nx}" y2="{ny}"/>
      <text class="ng-edge__label">{score}%</text>
    </g>
    <!-- bridge edges: dashed lines, center → bridge (appear on compare) -->
    <g class="ng-edge ng-edge--bridge" style="opacity:0">
      <line x1="{cx}" y1="{cy}" x2="{bx}" y2="{by}" stroke-dasharray="6,4"/>
      <text class="ng-edge__label">{shared attribute}</text>
    </g>
  </g>
  <g class="ng-nodes">
    <!-- center node -->
    <g class="ng-node ng-node--center" transform="translate({cx},{cy})">
      <circle r="32" class="ng-node__shape" fill="{familyColor}"/>
      <text class="ng-node__name" dy="48">{name}</text>
    </g>
    <!-- neighbor nodes -->
    <g class="ng-node ng-node--neighbor" data-concept-id="{id}" transform="translate({x},{y})">
      <circle r="22" class="ng-node__shape" fill="{familyColor}"/>
      <text class="ng-node__name" dy="34">{name}</text>
      <text class="ng-node__score" dy="-30">{score}%</text>
    </g>
    <!-- bridge nodes (hidden until compare) -->
    <g class="ng-node ng-node--bridge" data-concept-id="{id}" style="opacity:0"
       transform="translate({bx},{by})">
      <rect class="ng-node__shape" x="-14" y="-14" width="28" height="28"
            rx="3" transform="rotate(45)" fill="{familyColor}"/>
      <text class="ng-node__name" dy="28">{name}</text>
      <text class="ng-node__attr" dy="-24">{shared attribute}</text>
    </g>
  </g>
</svg>
```

**Node shapes:**
- **Center**: Circle, r=32, family color fill, white stroke, subtle drop shadow
- **Neighbors**: Circle, r=22, family color fill, thinner stroke. On hover: scale(1.12). When comparing: the selected neighbor gets a brighter stroke/glow
- **Bridges**: Rotated square (diamond), 28×28, family color fill, dashed stroke. Visually distinct shape = different relationship type at a glance

**Edge styles:**
- **Similarity edges**: Solid line, stroke-width proportional to similarity (1.5px at 50% → 3px at 100%), color `var(--color-text-muted)` at 40% opacity
- **Bridge edges**: Dashed line (`stroke-dasharray: 6,4`), 1.5px width, colored by dimension group (plasma=blue, engineering=green, fuel_cycle=amber, operations=gray). The color ties the edge to its domain meaning

#### Interaction Handlers

All bound directly to SVG `<g>` elements (matches codebase pattern):

```javascript
// Single-click neighbor → compare
neighborGroup.addEventListener("click", function(e) {
  e.stopPropagation();
  callbacks.onCompare(conceptId);
});

// Double-click neighbor or bridge → re-center
neighborGroup.addEventListener("dblclick", function(e) {
  e.stopPropagation();
  callbacks.onFocus(conceptId);
});

// Single-click SVG background → deselect neighbor
svg.addEventListener("click", function() {
  callbacks.onDeselect();
});

// Hover → show tooltip
neighborGroup.addEventListener("mouseenter", function(e) {
  showTooltip(e, conceptData);
});
neighborGroup.addEventListener("mouseleave", hideTooltip);

// Bridge highlight (called from comparison panel bridge-ref clicks)
// Adds a pulse/glow effect to the bridge node, auto-clears after 1.5s
function highlightBridge(conceptId) {
  var node = svg.querySelector('.ng-node--bridge[data-concept-id="' + conceptId + '"]');
  if (!node) return;
  node.classList.add("ng-node--highlighted");
  setTimeout(function() { node.classList.remove("ng-node--highlighted"); }, 1500);
}
```

#### CSS Transitions for Animation

All animation via CSS on SVG elements:

```css
.ng-node {
  transition: opacity 0.3s ease, transform 0.3s ease;
}
.ng-node--bridge {
  /* bridges start hidden, animated in by setting opacity via JS */
}
.ng-edge {
  transition: opacity 0.3s ease;
}
.ng-node__shape {
  transition: transform 0.15s ease, stroke-width 0.15s, filter 0.15s;
}
.ng-node--neighbor:hover .ng-node__shape {
  transform: scale(1.12);
  filter: brightness(1.15);
}
.ng-node--neighbor.ng-node--comparing .ng-node__shape {
  stroke: var(--color-text-primary);
  stroke-width: 3;
  filter: drop-shadow(0 0 6px rgba(255,255,255,0.3));
}
```

Showing/hiding bridges is done by setting `style.opacity` on the bridge `<g>` elements — CSS `transition: opacity 0.3s` handles the fade.

### Component 3: View Mode Switching

**Managed by the orchestrator (`taxonomy.js`).**

Two sibling containers in the graph area: `#constellation-container` (Plotly) and `#neighborhood-container` (SVG). Only one is visible at a time.

```javascript
function switchToOverview() {
  neighborhoodContainer.style.opacity = "0";
  setTimeout(function() {
    neighborhoodContainer.style.display = "none";
    constellationContainer.style.display = "";
    constellationContainer.style.opacity = "1";
    Plotly.Plots.resize(constellationContainer); // re-fit after display change
  }, 300);
  graphTitle.textContent = "Design Space Overview";
  graphSubtitle.textContent = "Concepts positioned by design attribute similarity. Double-click to explore.";
  backButton.style.display = "none";
  _viewMode = "overview";
}

function switchToNeighborhood(conceptId) {
  constellationContainer.style.opacity = "0";
  setTimeout(function() {
    constellationContainer.style.display = "none";
    neighborhoodContainer.style.display = "";
    neighborhoodContainer.style.opacity = "1";
    // render the graph
    NeighborhoodGraph.render(neighborhoodContainer, concept, neighbors, _registry, {
      onCompare: handleCompare,
      onFocus: handleFocus,
      onDeselect: handleDeselect,
    });
  }, 300);
  graphTitle.textContent = "Neighborhood of " + concept.name;
  graphSubtitle.textContent = "Click a neighbor to compare. Double-click to navigate.";
  backButton.style.display = "";
  _viewMode = "neighborhood";
}
```

Both containers get `transition: opacity 0.3s` in CSS. The `setTimeout` waits for the fade-out before swapping display.

**Back to overview**: Button click or Escape key. Both call `switchToOverview()`.

### Component 4: Comparison Panel

**Modified file:** `static/js/taxonomy_card.js` (rewrite `renderSimilarityCard`)
**Renders into:** `#comparison-container` in the detail panel

#### Neighbor List (FOCUSED state)

When a concept is focused but no neighbor is clicked yet, the comparison container shows a compact neighbor list:

```html
<div class="neighbor-list">
  <h3 class="neighbor-list__title">Similar Concepts</h3>
  <p class="neighbor-list__hint">Click a concept to see how they compare</p>
  <!-- one entry per neighbor -->
  <div class="neighbor-entry" data-concept-id="{id}">
    <span class="badge badge-{family}">{family}</span>
    <span class="neighbor-entry__name">{name}</span>
    <span class="neighbor-entry__score">{score}%</span>
  </div>
</div>
```

Clicking a neighbor entry triggers the same `onCompare` as clicking the graph node.

#### Comparison Table (COMPARING state)

When a neighbor is selected, the comparison container updates to show the field-by-field comparison:

```html
<div class="comparison-panel">
  <div class="comparison-panel__header">
    <h3>Comparing with {neighbor name}</h3>
    <span class="comparison-panel__score">{score}% match</span>
  </div>

  <!-- Differences first (prominent) -->
  <div class="comparison-section comparison-section--diff">
    <h4 class="comparison-section__title">Differences</h4>
    <div class="comparison-row comparison-row--diff">
      <span class="comparison-row__label">Energy Capture</span>
      <div class="comparison-row__values">
        <span class="comparison-row__value comparison-row__value--self">
          Hybrid (thermal + direct)
        </span>
        <span class="comparison-row__vs">vs</span>
        <span class="comparison-row__value comparison-row__value--other">
          Thermal (unspecified)
        </span>
      </div>
      <!-- Bridge reference (if exists) — click highlights bridge node in graph -->
      <div class="comparison-row__bridge">
        Also uses Hybrid capture:
        <a class="bridge-ref" data-concept-id="{id}"
           data-action="highlight-bridge">
          Nanostructured Target (p-B11)
          <span class="badge badge-ife">IFE</span>
        </a>
      </div>
    </div>
  </div>

  <!-- Matches second (de-emphasized) -->
  <div class="comparison-section comparison-section--match">
    <h4 class="comparison-section__title">{N} matching attributes</h4>
    <div class="comparison-row comparison-row--match">
      <span class="comparison-row__label">Fuel</span>
      <span class="comparison-row__value">D-T</span>
      <span class="comparison-row__check">✓</span>
    </div>
    <!-- more matched rows... -->
  </div>

  <!-- Other neighbors (compact list below) -->
  <div class="neighbor-list neighbor-list--compact">
    <h4 class="neighbor-list__title">Other Neighbors</h4>
    <!-- remaining neighbors as compact entries -->
  </div>
</div>
```

#### Field Label Mapping

Human-readable labels for all comparable fields:

```javascript
var FIELD_LABELS = {
  fuel: "Fuel Type",
  primary_heating: "Primary Heating",
  plasma_state: "Plasma State",
  magnet_type: "Magnet Type",
  energy_capture: "Energy Capture",
  tritium_breeding: "Tritium Breeding",
  neutron_management: "Neutron Management",
  operation_mode: "Operation Mode",
  repetition_rate: "Repetition Rate"
};
```

#### Building the Comparison

The client-side comparison builder uses data from two sources:

1. **Similarity report** (`/api/taxonomy/similarity/{id}`) — provides `matched_fields`, `mismatched_fields`, bridge data with actual values for differences
2. **Registry lookup** (`_registry[conceptId]`) — provides actual values for matched fields

```javascript
function buildComparison(focused, neighbor, similarityResult) {
  var comp = similarityResult.comparison;
  var bridges = similarityResult.bridges;
  var rows = [];

  // Collect all fields across dimensions
  comp.dimensions.forEach(function(dim) {
    dim.mismatched_fields.forEach(function(field) {
      var bridge = bridges.find(function(b) { return b.mismatched_field === field; });
      rows.push({
        field: field,
        label: FIELD_LABELS[field],
        match: false,
        focusedValue: String(focused[field]),
        neighborValue: bridge ? bridge.similar_value : String(neighbor[field]),
        bridge: bridge || null,
        dimension: dim.dimension
      });
    });
    dim.matched_fields.forEach(function(field) {
      rows.push({
        field: field,
        label: FIELD_LABELS[field],
        match: true,
        value: String(focused[field]),
        dimension: dim.dimension
      });
    });
  });

  return rows;
}
```

### Component 5: Bridge Selection Algorithm

**FR-10 implementation.** Given a neighbor's bridges from the API, select at most 3:

```javascript
var MAX_BRIDGES = 3;

function selectBridges(bridges) {
  // Sort by overall similarity to focused concept (descending)
  // (requires bridge_overall_similarity field from API)
  var sorted = bridges.slice().sort(function(a, b) {
    return (b.bridge_overall_similarity || 0) - (a.bridge_overall_similarity || 0);
  });

  var selected = [];
  var coveredFields = {};

  for (var i = 0; i < sorted.length && selected.length < MAX_BRIDGES; i++) {
    var b = sorted[i];
    // Each bridge must contribute a different mismatched field
    if (!coveredFields[b.mismatched_field]) {
      coveredFields[b.mismatched_field] = true;
      selected.push(b);
    }
  }

  return selected;
}
```

**Server-side change needed** (minor, ~5 lines): In `similarity.py:explain_difference()`, after finding the best bridge concept for each field, look up the overall similarity between the query and the bridge concept from the precomputed matrix and add it to the `DifferenceBridge` as `bridge_overall_similarity: float`. No new endpoint, no computation change — just a matrix lookup.

### Component 6: Tooltip System

**New utility within `neighborhood_graph.js`.**

Reuses the existing `.tooltip` CSS class (`explorer.css:599-611`) which is already defined but unused.

```javascript
var _tooltipEl = null;

function showTooltip(event, content) {
  if (!_tooltipEl) {
    _tooltipEl = document.createElement("div");
    _tooltipEl.className = "tooltip";
    document.body.appendChild(_tooltipEl);
  }
  _tooltipEl.innerHTML = content;
  _tooltipEl.style.display = "";

  // Position near cursor, avoid viewport overflow
  var x = event.clientX + 12;
  var y = event.clientY - 8;
  var rect = _tooltipEl.getBoundingClientRect();
  if (x + rect.width > window.innerWidth) x = event.clientX - rect.width - 12;
  if (y + rect.height > window.innerHeight) y = event.clientY - rect.height;

  _tooltipEl.style.left = x + "px";
  _tooltipEl.style.top = y + "px";
}

function hideTooltip() {
  if (_tooltipEl) _tooltipEl.style.display = "none";
}
```

#### Tooltip Content by Node Type

**Center node hover:**
```
{Concept Name}
{Company}
{ConfinementFamily} · {topology/driver/method}
```

**Neighbor node hover:**
```
{Concept Name}
{ConfinementFamily} · {score}% similar
Click to compare · Double-click to explore
```

**Bridge node hover:**
```
{Concept Name}
{ConfinementFamily}
Shares {field label}: {value}
Double-click to explore
```

**Bridge edge hover:**
```
Both use {value} for {field label}
```

**Similarity edge hover:**
```
{score}% design similarity
{matches}/{comparable} attributes match
```

### Component 7: Constellation Enhancements

**Modified file:** `static/js/constellation.js`

Minor additions to the existing Plotly constellation:

1. **Double-click handler** (new): `container.on("plotly_doubleclick", ...)` to trigger focus. Note: Plotly doesn't have a native `plotly_doubleclick` event. Implementation: track click timing — if two clicks on the same point within 300ms, treat as double-click. Suppress the single-click action with a `setTimeout` debounce.

2. **Caption**: Add subtitle text to Plotly layout annotations or as HTML below the chart. `"Concepts positioned by design attribute similarity — closer = more similar. Double-click to explore a concept's neighborhood."`

### Component 8: Orchestrator Rewrite

**Modified file:** `static/js/taxonomy.js`

The orchestrator gains significant new responsibilities — view mode management, the compare/focus distinction, and bridge lifecycle.

#### State

```javascript
var _viewMode = "overview";    // "overview" | "neighborhood"
var _focusedId = null;         // concept at graph center
var _comparingId = null;       // neighbor being compared (or null)
var _registry = {};            // concept_id → concept object
var _similarityCache = {};     // concept_id → similarity report
var _sidebarCollapsed = false;
```

#### Key Handlers

```javascript
// Called from: tree single-click, constellation double-click, graph double-click
function handleFocus(conceptId) {
  if (conceptId === _focusedId) return;
  _focusedId = conceptId;
  _comparingId = null;

  // Load similarity if not cached
  fetchSimilarity(conceptId).then(function(report) {
    var concept = _registry[conceptId];
    var neighbors = report.nearest;

    // Update graph
    switchToNeighborhood(concept, neighbors);

    // Update detail panel: taxonomy card + neighbor list
    TaxonomyCards.renderTaxonomyCard(taxonomyCardContainer, concept);
    renderNeighborList(comparisonContainer, neighbors);

    // Sync tree highlight
    TreeView.highlightTreeConcept(conceptId);
  });
}

// Called from: graph single-click on neighbor, neighbor list click
function handleCompare(neighborId) {
  if (neighborId === _comparingId) return;
  _comparingId = neighborId;

  var report = _similarityCache[_focusedId];
  var result = report.nearest.find(function(n) { return n.concept_id === neighborId; });
  var focused = _registry[_focusedId];
  var neighbor = _registry[neighborId];

  // Select bridges (up to 3, one per field, by similarity)
  var bridges = selectBridges(result.bridges);

  // Update graph: highlight neighbor, show bridge nodes
  NeighborhoodGraph.showBridges(neighborId, bridges);

  // Update detail panel: comparison table
  renderComparison(comparisonContainer, focused, neighbor, result, bridges);
}

// Called from: comparison panel bridge-ref clicks
function handleBridgeHighlight(conceptId) {
  NeighborhoodGraph.highlightBridge(conceptId);
}

// Called from: graph background click
function handleDeselect() {
  _comparingId = null;
  NeighborhoodGraph.clearBridges();
  // Restore neighbor list (remove comparison)
  var report = _similarityCache[_focusedId];
  renderNeighborList(comparisonContainer, report.nearest);
}
```

### Component 9: Sidebar Toggle

**Implemented in `taxonomy.js` orchestrator.**

```javascript
var toggleBtn = document.getElementById("sidebar-toggle");
toggleBtn.addEventListener("click", function() {
  _sidebarCollapsed = !_sidebarCollapsed;
  var layout = document.querySelector(".taxonomy-layout");
  layout.classList.toggle("taxonomy-layout--collapsed", _sidebarCollapsed);
  toggleBtn.textContent = _sidebarCollapsed ? "›" : "‹";
  toggleBtn.title = _sidebarCollapsed ? "Show decision tree" : "Hide decision tree";
  // Trigger graph resize after transition
  setTimeout(function() {
    if (_viewMode === "overview") {
      Plotly.Plots.resize(constellationContainer);
    }
    // SVG viewBox handles resize automatically
  }, 350);
});
```

CSS handles the animation — the sidebar column transitions to 0 width and the content clips via `overflow: hidden`.

### Component 10: CSS Additions

**File:** `static/css/explorer.css`

#### New Class Inventory

**Layout:**
- `.taxonomy-layout` — override to 3-column grid (replace current 2-column)
- `.taxonomy-layout--collapsed` — tree column at 0px
- `.taxonomy-detail` — right panel, `overflow-y: auto`, sticky
- `.sidebar-toggle` — positioned button on sidebar edge

**Graph header:**
- `.graph-header` — flex row with back button, title, subtitle
- `.graph-header__back` — button, hidden in overview mode
- `.graph-header__title` — current view label
- `.graph-header__subtitle` — explanatory text (muted)

**SVG graph:**
- `.neighborhood-graph` — SVG element, `width: 100%`, `height: 100%`
- `.ng-node`, `.ng-node--center`, `.ng-node--neighbor`, `.ng-node--bridge` — node group styling
- `.ng-node__shape` — circle/rect fill and stroke
- `.ng-node__name` — text label styling (font, fill, anchor)
- `.ng-node__score` — similarity percentage (smaller, muted)
- `.ng-node__attr` — bridge attribute label (smaller, italic)
- `.ng-node--comparing` — selected neighbor state (glow)
- `.ng-edge`, `.ng-edge--similarity`, `.ng-edge--bridge` — line styling
- `.ng-edge__label` — edge midpoint label

**Comparison panel:**
- `.neighbor-list`, `.neighbor-list__title`, `.neighbor-list__hint` — compact neighbor list
- `.neighbor-entry`, `.neighbor-entry__name`, `.neighbor-entry__score` — single neighbor row
- `.neighbor-entry--active` — currently comparing
- `.comparison-panel`, `.comparison-panel__header`, `.comparison-panel__score`
- `.comparison-section`, `.comparison-section--diff`, `.comparison-section--match`
- `.comparison-section__title`
- `.comparison-row`, `.comparison-row--diff`, `.comparison-row--match`
- `.comparison-row__label`, `.comparison-row__values`, `.comparison-row__value`
- `.comparison-row__value--self`, `.comparison-row__value--other`
- `.comparison-row__vs` — the "vs" separator
- `.comparison-row__check` — checkmark for matches
- `.comparison-row__bridge` — bridge reference line
- `.bridge-ref` — clickable bridge concept link with family badge

**Tooltip:**
- `.tooltip` — already exists (`explorer.css:599-611`), add `transition: opacity 0.15s`
- Note: This is a second tooltip implementation alongside `parameter_card.js`'s popover. Acceptable for this scope; consolidate in a future pass if more tooltip uses emerge.

**Bridge highlight animation:**
- `.ng-node--highlighted .ng-node__shape` — pulse animation (`@keyframes bridge-pulse`, scale 1→1.2→1, 0.5s, ease, 3 iterations). Auto-removed after 1.5s by JS.

#### Color Mapping for Bridge Edges

Bridge edge colors by dimension, using muted versions of existing palette:

```css
.ng-edge--bridge[data-dimension="plasma_physics"]  { stroke: #60a5fa; }  /* blue-400 */
.ng-edge--bridge[data-dimension="engineering"]      { stroke: #34d399; }  /* green-400 */
.ng-edge--bridge[data-dimension="fuel_cycle"]       { stroke: #fbbf24; }  /* amber-400 */
.ng-edge--bridge[data-dimension="operations"]       { stroke: #a78bfa; }  /* purple-400 */
```

---

## File Change Summary

| File | Action | What Changes |
|------|--------|-------------|
| `static/js/neighborhood_graph.js` | **NEW** | SVG graph renderer, radial layout, tooltip system |
| `static/js/taxonomy.js` | **REWRITE** | State machine, view switching, focus/compare/deselect handlers |
| `static/js/taxonomy_card.js` | **MODIFY** | Replace `renderSimilarityCard` with `renderNeighborList` and `renderComparison`; keep `renderTaxonomyCard` mostly intact |
| `static/js/constellation.js` | **MODIFY** | Add double-click handler (debounced), add caption/subtitle |
| `static/js/tree_view.js` | **MINOR** | No changes needed — tree already fires `onConceptClick` on single-click |
| `templates/taxonomy.html.j2` | **REWRITE** | Three-column layout, new containers, graph header |
| `templates/base.html.j2` | **MODIFY** | Move Taxonomy nav link to first position |
| `static/css/explorer.css` | **MODIFY** | Replace `.taxonomy-layout` 2-col with 3-col, add all new classes |
| `similarity.py` | **MINOR** | Add `bridge_overall_similarity` field to `DifferenceBridge` model (~5 lines) |
| `server.py` | **NO CHANGE** | Endpoints already return all needed data |
| `tests/test_similarity.py` | **MINOR** | Update bridge assertions for new field |
| `tests/test_taxonomy_server.py` | **NO CHANGE** | Endpoint shapes unchanged (additive field) |

---

## Potential Risks

### R-1: Plotly Double-Click Conflicts
Plotly intercepts `dblclick` for zoom-reset. Custom double-click on a point requires a debounced single-click pattern (setTimeout, clear on second click). If this proves fragile, fallback: add an explicit "Explore" button on the Plotly hover popup instead.

### R-2: SVG Text Overflow
Long concept names (e.g., "Laser ICF - French National Direct Drive (D-T)") will overflow node labels. Mitigation: truncate to ~25 chars with ellipsis in the label, show full name in tooltip on hover.

### R-3: Bridge Node Overlap
With 3 bridge nodes clustered near one neighbor, labels may overlap. Mitigation: bridges are placed at angular offsets from the neighbor (±0.15 rad per bridge). If 3 bridges bunch on one neighbor, spread them evenly in a ±0.3 rad arc.

### R-4: Bridge Similarity Fallback
The `selectBridges()` function uses `(b.bridge_overall_similarity || 0)` which treats a missing field as 0 similarity. If old cached data is served before the server change is deployed, all bridges get priority 0 and selection degrades to insertion order. This is fine for development — just a deployment ordering note.

### R-5: Transition Timing
The 300ms crossfade between constellation and graph requires careful sequencing (hide one, wait, show other). If the timing feels sluggish, reduce to 200ms. If it causes flickering, switch to immediate swap (no animation).

---

## Validation Approach

### Automated
- `uv run python -m pytest exploration/concept_explorer/tests/ -v` — all existing + updated tests pass
- Bridge selection unit test: verify at most 3 bridges, each covering a different field, sorted by similarity

### Manual Walkthrough
1. **Overview mode**: Page loads with constellation. Title says "Design Space Overview" with subtitle. No back button visible.
2. **Focus via constellation**: Double-click a dot → constellation fades out, neighborhood graph fades in. Center node, 5 neighbors in ring. Header updates to "Neighborhood of {name}". Back button appears.
3. **Focus via tree**: Single-click a leaf → same graph behavior. Tree highlights leaf.
4. **Compare**: Single-click a neighbor → it glows, comparison table appears in detail panel (differences first, matches below). Up to 3 bridge nodes fade into graph with dashed edges.
5. **Bridge tooltips**: Hover a bridge node → tooltip shows shared attribute. Hover bridge edge → tooltip explains relationship.
6. **Navigate**: Double-click a bridge → graph re-centers on that concept. New neighborhood loads.
7. **Back to overview**: Click "← Overview" or press Escape → graph fades out, constellation fades in.
8. **Sidebar toggle**: Click toggle button → tree collapses, graph expands. Click again → tree returns.
9. **Detail panel scroll**: With many matches/differences, scroll the detail panel — graph stays in view.
10. **Domain sanity**: Focus on HTS Compact Tokamak → neighbors are tokamaks. Click one → differences highlight magnets or heating. Bridge shows a non-tokamak with same magnet type.

---

**Next Steps:** After approval → `/_my_plan` to break into implementation phases.
