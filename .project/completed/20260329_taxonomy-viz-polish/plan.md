# Plan: Replace SVG Neighborhood Graph with Cytoscape.js

## Context

The taxonomy page's neighborhood graph was built as hand-rolled SVG with static radial layout. The result is unreadable labels, zero interactivity (no drag/zoom/pan), and no label collision avoidance. The comparison panel crams bridge references into divs that overlap. The constellation legend is illegible.

The fix: vendor Cytoscape.js (already done), rewrite `neighborhood_graph.js`, rewrite the comparison rendering as a `<table>`, fix the constellation legend, and make the detail panel width responsive.

## What Changes

### 1. `templates/taxonomy.html.j2` (1 line)
Add Cytoscape vendor script before the page scripts:
```html
<script src="/static/vendor/cytoscape.min.js"></script>
```
Added inside `{% block scripts %}` (NOT in `base.html.j2` — Cytoscape is taxonomy-only).

### 2. `static/js/neighborhood_graph.js` (full rewrite)
Replace 625 lines of hand-rolled SVG with ~300 lines of Cytoscape.

**Same public API** — no orchestrator changes needed:
- `render(container, focusedConcept, neighbors, registry, callbacks)`
- `showBridges(neighborId, bridges)`
- `clearBridges()`
- `highlightBridge(conceptId)`
- `destroy()`
- NEW: `resize()` — called on sidebar toggle

**Layout**: `cose` (force-directed, built into Cytoscape core). Nodes settle into position with spring physics over ~500ms. Initial positions seeded as radial arrangement so the simulation starts clean, not random.

**Nodes**:
- Center: circle, 64px, family-colored, bold 14px label with dark text outline
- Neighbors: circle, 44px, family-colored, 13px label, similarity % on edge
- Bridges: diamond, 36px, family-colored, dashed border, 12px label — fade in/out with animation

**Edges**:
- Similarity: solid, width proportional to score (1.5-4.5px), label shows %
- Bridge: dashed, colored by dimension (plasma=blue, engineering=green, fuel=amber, ops=purple), label shows shared value

**Interactivity** (all free with Cytoscape):
- Drag nodes to rearrange
- Scroll to zoom, click-drag to pan
- Hover tooltips on nodes and edges (using existing HTML tooltip pattern)
- Single-click neighbor → compare (with 300ms debounce to avoid double-click conflict)
- Double-click neighbor/bridge → re-center graph on that concept

**Bridge positioning**: Computed relative to center and compared neighbor (1.4x distance, angularly spread). No layout re-run — bridges are positioned manually and locked.

**Text readability**: Cytoscape renders to canvas at native resolution. Labels use 12-14px with `text-outline-width: 2` against `#0d1117` background. No viewBox scaling.

### 3. `static/js/constellation.js` (legend fix)
Change the Plotly legend config from horizontal to vertical orientation with larger font:

```javascript
legend: {
  orientation: "v",
  x: 1.02,
  y: 1,
  font: { size: 13 }
},
```

Increase right margin from 20 to 120 to make room:
```javascript
margin: { l: 30, r: 120, t: 30, b: 30 },
```

Remove or reposition the annotation that sits at `y: -0.12` (it crowds the legend area). Move it to the graph header subtitle instead (already exists in the template as `#graph-subtitle`).

### 4. `static/js/taxonomy_card.js` — comparison table rewrite

Rewrite `renderComparison()` to produce a proper `<table>`:

```
┌─────────────┬──────────────────┬──────────────────┐
│ Attribute   │ HTS Compact Tok  │ SPARC            │
├─────────────┼──────────────────┼──────────────────┤
│ Fuel        │ D-T            ✓ │ D-T              │
│ Heating     │ ICRH + NBI     ✗ │ ECRH             │
│             │ ↳ Also: ARC (MFE)                   │
│ Energy Cap  │ Hybrid         ✗ │ Thermal          │
│             │ ↳ Also: DEMO (MFE)                  │
│ Plasma      │ Burning        ✓ │ Burning          │
│ Magnets     │ HTS            ✓ │ HTS              │
│ Tritium     │ Blanket        ✓ │ Blanket          │
│ Operation   │ Pulsed         ✓ │ Pulsed           │
└─────────────┴──────────────────┴──────────────────┘
```

- Real `<table>` with three columns: attribute label, focused value, neighbor value
- Match/mismatch indicator (✓/✗) in each row
- Mismatched rows: highlighted background, full contrast text
- Matched rows: muted text, no highlight
- Bridge references as sub-rows below mismatched attributes: "Also uses [value]: [Concept] [family badge]" — clickable, triggers `onBridgeHighlight`
- N/A and TBD fields excluded (same logic as current `buildComparison()`)
- Header row shows both concept names with family badges and score badge
- The `buildComparison()` helper returns the right row data — only the rendering changes

### 5. `static/css/explorer.css`

**Layout grid — responsive detail panel**:
```css
.taxonomy-layout {
  display: grid;
  grid-template-columns: var(--tree-width, 280px) auto 1fr minmax(340px, 25vw);
  gap: 0;
  min-height: calc(100vh - 120px);
}
```

The detail panel is now `minmax(340px, 25vw)` — scales with viewport, never smaller than 340px. At 1440px = 360px. At 1920px = 480px. At 1280px = 340px (floor).

**Remove**: Lines ~1627-1733 (`.neighborhood-graph`, `.ng-node`, `.ng-edge`, `.ng-node--highlighted`, bridge-pulse keyframe — all SVG-specific, dead code with Cytoscape).

**Add**: Container sizing for Cytoscape canvas:
```css
#neighborhood-container {
  flex: 1;
  min-height: 400px;
  position: relative;
}
```

**Add**: Comparison table styles (replaces `.comparison-row`/`.comparison-section` div styles):
```css
.comparison-table { width: 100%; border-collapse: collapse; font-size: var(--font-size-sm); }
.comparison-table th { text-align: left; padding: var(--space-2); ... }
.comparison-table td { padding: var(--space-2); border-bottom: 1px solid var(--color-border); }
.comparison-table tr.diff { background: rgba(248, 113, 113, 0.06); }
.comparison-table .bridge-row td { padding-top: 0; font-size: var(--font-size-xs); color: var(--color-text-muted); }
```

### 6. `static/js/taxonomy.js` (2-line change)
Add `NeighborhoodGraph.resize()` call in the sidebar toggle handler:
```javascript
} else if (_viewMode === "neighborhood") {
  NeighborhoodGraph.resize();
}
```

### 7. What does NOT change
- `server.py` — no API changes
- `similarity.py` — no computation changes
- `tree_view.js` — unchanged
- Tests — no new tests (frontend JS, no test infra)

## Key Design Decisions

**Why Cytoscape.js**: Purpose-built for interactive graph exploration. Built-in force-directed layout, zoom/pan/drag, animated transitions, canvas rendering (sharp text at any zoom), rich event system. 413KB vendored — same pattern as Plotly (already 830KB).

**Why `cose` layout**: Built into Cytoscape core (no extra downloads). Force-directed gives organic spacing. With only 6-9 nodes, layout converges instantly. Fallback: if `cose` produces bad layouts with few nodes, switch to `preset` (computed radial) while keeping all Cytoscape interactivity.

**Why `minmax(340px, 25vw)` for detail panel**: Scales naturally — gives more room on larger screens where it matters. The 340px floor prevents collapse on smaller viewports. 25vw cap prevents the panel from eating the graph area.

**Bridge positioning without re-layout**: Adding 3 bridge nodes to a 6-node force simulation would disturb settled neighbor positions. Instead, compute bridge positions geometrically and lock them. Animation handles the visual transition.

## Edge Cases

- **Container sizing**: Cytoscape needs non-zero dimensions. `render()` is called inside a 300ms setTimeout after container becomes visible — verified safe.
- **Click/double-click conflict**: Debounced click pattern (300ms timer) prevents both `onCompare` and `onFocus` firing on double-click. Same pattern already used in `constellation.js`.
- **Bridge concept = existing neighbor**: Gets a separate diamond node with `b-` prefix ID. Intentional — shows it in a different role.
- **Rapid comparison switching**: `showBridges()` calls `clearBridges(true)` (synchronous removal) before adding new bridges.

---

## Implementation Phases

### Phase 1: Graph rewrite + layout fixes

**Changes**:
1. Add Cytoscape script tag to `taxonomy.html.j2`
2. Rewrite `neighborhood_graph.js` — full Cytoscape implementation
3. Update `explorer.css` — responsive detail panel (`minmax(340px, 25vw)`), remove dead SVG styles, add Cytoscape container sizing
4. Add `NeighborhoodGraph.resize()` call in `taxonomy.js`

**Checkpoint**:
- [x] `uv run python -m pytest exploration/concept_explorer/tests/ -v` — 141 passed
- [x] Screenshot: `/tmp/tax_focused.png` — graph renders with Cytoscape, nodes draggable, labels readable
- [x] Screenshot: `/tmp/tax_comparing.png` — bridge diamonds appear, no label overlap
- [ ] Manual: scroll zooms graph, drag pans, nodes settle with animation

### Phase 1 Completion
**Completed:** 2026-03-29
**Changes Made:**
- Added `<script src="/static/vendor/cytoscape.min.js">` to `taxonomy.html.j2`
- Full rewrite of `neighborhood_graph.js` (625→~350 lines): Cytoscape cose layout, radial initial positions, bridge positioning via geometry, fade-in/out animations, debounced click/dblclick, new `resize()` method
- Updated `explorer.css`: `minmax(340px, 25vw)` detail panel, removed 107 lines of dead SVG styles, added `#neighborhood-container` sizing
- Added `NeighborhoodGraph.resize()` call in `taxonomy.js` sidebar toggle handler

### Phase 2: Constellation legend + comparison table

**Changes**:
1. Fix constellation legend in `constellation.js` — vertical orientation, larger font, more right margin
2. Rewrite `renderComparison()` in `taxonomy_card.js` — `<table>` layout with bridge sub-rows
3. Add comparison table CSS to `explorer.css`

**Checkpoint**:
- [x] `uv run python -m pytest exploration/concept_explorer/tests/ -v` — 141 passed
- [x] Screenshot: `/tmp/tax_overview.png` — constellation legend fully legible, no overlap
- [x] Screenshot: `/tmp/tax_detail_panel.png` — comparison table with aligned columns, bridge refs on their own lines
- [ ] Manual: full walkthrough — overview → focus → compare → bridge highlight → back

### Phase 2 Completion
**Completed:** 2026-03-29
**Changes Made:**
- `constellation.js`: Legend switched to vertical (`orientation: "v"`, `x: 1.02`, `y: 1`, `font.size: 13`), right margin 20→120, removed crowding annotation, bottom margin 50→30
- `taxonomy_card.js`: Rewrote `renderComparison()` from div layout to `<table>` with thead (concept names), tbody rows per attribute, match/mismatch indicators (checkmark/x), bridge sub-rows with colspan
- `explorer.css`: Added comparison table styles (`.comparison-table`, `.diff`, `.match`, `.bridge-row`, `.attr-label`, `.val-self`, `.val-other`, `.match-indicator`)

## Verification

After each phase, run:

```bash
# Start server on a test port
uv run python exploration/concept_explorer/server.py --port 8422 &
sleep 3

# Run Playwright capture script (spec.md has the full script)
uv run python /tmp/capture_taxonomy.py

# Review screenshots with Read tool:
#   /tmp/tax_overview.png — constellation + legend
#   /tmp/tax_focused.png — neighborhood graph with labels
#   /tmp/tax_comparing.png — comparison state with bridges
#   /tmp/tax_detail_panel.png — detail panel close-up

# Kill test server
kill %1
```

Phase 1 MUST pass its checkpoint before Phase 2 begins.
