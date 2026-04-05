# Spec: Taxonomy Visualization Polish

**Status:** Draft
**Owner:** Reid W
**Created:** 2026-03-29
**Complexity:** MEDIUM
**Branch:** ralph/concept-explorer

---

## Business Goals

### Why This Matters

The taxonomy visualization was implemented but the visual output is broken. The neighborhood graph is hand-rolled SVG with static radial positioning — it doesn't behave like a graph, it behaves like a diagram with overlapping labels. The comparison panel crams bridge references into a 360px column where they stack on each other. The constellation legend is illegible. A user opening this page cannot read what they're looking at.

The underlying data, API, and interaction model are sound. The graph rendering and comparison layout need to be replaced with proper tools.

### Success Criteria

- [ ] SC-1: All text on the taxonomy page is legible at 1440x900 — no overlapping, no truncation that hides meaning
- [ ] SC-2: The comparison panel displays attribute values, match/mismatch indicators, and bridge references in a clear table layout — nothing stacks on top of anything else
- [ ] SC-3: The constellation legend is readable — category names don't overlap
- [ ] SC-4: The neighborhood graph uses a real graph library with force-directed layout, drag/zoom/pan, and automatic label placement
- [ ] SC-5: The detail panel scales with viewport width (percentage-based) so it has enough room for comparison data
- [ ] SC-6: Visual verification via screenshot capture (shot-scraper/Playwright) at each implementation phase

### Priority

High — the page is unusable in its current state.

---

## Problem Statement

### Current State

Screenshot-verified defects (captured via shot-scraper + Playwright at 1440x900):

1. **Neighborhood graph (hand-rolled SVG)**:
   - Static radial layout with no physics — nodes placed at fixed positions
   - Labels truncated at 25 chars, still overlap each other and edge labels
   - No drag, zoom, or pan — zero interactivity beyond click handlers
   - Bridge nodes add label clutter between center and neighbor ring
   - 625 lines of manual SVG positioning code that produces unreadable output

2. **Comparison panel (360px right sidebar)**:
   - Bridge references ("Also uses NBI: Compact Liquid-Wall HTS Stellarator [MFE]") overlap next row
   - "vs" value comparisons cramped inline with no structure
   - Div-based layout when a table would give proper column alignment
   - Panel width fixed at 360px regardless of viewport

3. **Constellation plot legend**:
   - Horizontal orientation with 11px font at y=-0.05 — 4 family names run together
   - Annotation text at y=-0.12 adds to the cramping

4. **General layout**:
   - 280px + 360px fixed sidebars = 640px, leaving ~800px for graph at 1440px
   - Detail panel doesn't scale with viewport

### Desired Outcome

Replace the SVG graph with Cytoscape.js (already vendored at `static/vendor/cytoscape.min.js`). Rewrite the comparison panel as a proper `<table>`. Fix the constellation legend. Make the detail panel width responsive. Same interaction model, readable output.

---

## Scope

### In Scope

1. **Replace neighborhood graph** — rewrite `neighborhood_graph.js` from hand-rolled SVG to Cytoscape.js with force-directed layout, preserving the existing public API
2. **Rewrite comparison table** — replace div-based comparison rendering in `taxonomy_card.js` with a 3-column `<table>` (attribute, focused value, neighbor value)
3. **Fix constellation legend** — Plotly legend config change to prevent overlap
4. **Responsive detail panel** — percentage-based width with minimum pixel floor
5. **Screenshot verification** at each phase
6. **CSS cleanup** — remove dead SVG styles, add Cytoscape container and table styles

### Out of Scope

- Other pages (concept detail, index, compare)
- New API endpoints or data model changes
- Mobile/responsive design beyond the detail panel width
- Changes to the interaction state machine (overview → focused → comparing)

---

## Requirements

### Functional Requirements

1. **FR-1**: The neighborhood graph MUST use Cytoscape.js with force-directed layout (`cose`). Nodes MUST be draggable. The graph MUST support scroll-to-zoom and click-drag-to-pan.
2. **FR-2**: Graph node labels MUST be rendered at 12-14px with text outline for readability against the dark background. Labels MUST NOT overlap at default zoom.
3. **FR-3**: The comparison panel MUST render as a `<table>` with columns for attribute name, focused concept value, and neighbor concept value. Match/mismatch indicated per row.
4. **FR-4**: Bridge references MUST appear as distinct rows below mismatched attributes with clear spacing — never overlapping adjacent content.
5. **FR-5**: The constellation legend MUST display all 4 family categories without overlap.
6. **FR-6**: The detail panel width MUST be percentage-based (targeting ~25% of viewport) with a minimum floor of 340px.
7. **FR-7**: The `NeighborhoodGraph` public API (`render`, `showBridges`, `clearBridges`, `highlightBridge`, `destroy`) MUST be preserved so `taxonomy.js` requires minimal changes.
8. **FR-8**: Every implementation phase MUST be verified by screenshot capture at 1440x900 showing the fixed state.

### Non-Functional Requirements

- All existing tests MUST continue to pass
- Cytoscape.js loaded only on the taxonomy page (in `taxonomy.html.j2`, not `base.html.j2`)
- No changes to API endpoints or data models

---

## Acceptance Criteria

### Visual Quality
- [ ] No text overlap anywhere on the taxonomy page at 1440x900
- [ ] Graph nodes are draggable and settle via force simulation
- [ ] Scroll zooms the graph, drag pans it
- [ ] Bridge references display on their own lines with clear spacing
- [ ] Constellation legend is fully legible
- [ ] Comparison uses a real table layout with aligned columns

### Regression
- [ ] All 141 existing tests pass
- [ ] Tree sidebar collapse/expand still works
- [ ] Overview → focused → comparing state transitions unchanged
- [ ] Constellation double-click, neighbor click, bridge highlight all still work

---

## Verification Method

Screenshot capture at each phase using Playwright:

```python
# /tmp/capture_taxonomy.py — captures 3 states
from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=2)
    page.goto("http://localhost:8421/taxonomy", wait_until="networkidle")
    time.sleep(2)

    # 1. Overview — constellation + legend
    page.screenshot(path="/tmp/tax_overview.png")

    # 2. Focus — dispatch tree leaf click, wait for similarity API
    page.evaluate("""() => {
        const leaf = document.querySelector('.tree-leaf');
        if (leaf) leaf.dispatchEvent(new MouseEvent('click', {bubbles: true}));
    }""")
    time.sleep(3)
    page.screenshot(path="/tmp/tax_focused.png")

    # 3. Compare — click first neighbor entry
    page.evaluate("""() => {
        const entry = document.querySelector('.neighbor-entry');
        if (entry) entry.dispatchEvent(new MouseEvent('click', {bubbles: true}));
    }""")
    time.sleep(2)
    page.screenshot(path="/tmp/tax_comparing.png")
    page.locator('.taxonomy-detail').screenshot(path="/tmp/tax_detail_panel.png")

    browser.close()
```

Run after each phase:
```bash
uv run python exploration/concept_explorer/server.py --port 8422 &
sleep 3
uv run python /tmp/capture_taxonomy.py
# Then: Read /tmp/tax_overview.png, /tmp/tax_focused.png, /tmp/tax_comparing.png, /tmp/tax_detail_panel.png
kill %1
```

---

## Related Artifacts

- **Prior work:** `.project/active/taxonomy-viz-redesign/` (spec, design, plan — implemented, this fixes the output)
- **Cytoscape.js:** `static/vendor/cytoscape.min.js` (v3.31.0, 413KB, already vendored)
- **CSS:** `exploration/concept_explorer/static/css/explorer.css` (lines 1205-1733)
- **JS:** `neighborhood_graph.js` (625 lines, full rewrite), `taxonomy_card.js` (renderComparison rewrite), `constellation.js` (legend config fix), `taxonomy.js` (resize call)

---

**Next Steps:** Proceed to `/_my_plan`
