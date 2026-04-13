# Design: Taxonomy Graph Spacing & Label Fix

**Status:** Draft
**Owner:** Reid W
**Created:** 2026-04-12 18:30 PDT
**Updated:** 2026-04-12 18:30 PDT
**Branch:** taxonomy-fix
**Commit:** 830edec

---

## Overview

Adjust layout parameters, node dimensions, and font sizes in the Cytoscape neighborhood graph to produce a well-spaced, readable visualization without changing any interaction behavior.

## Related Artifacts

- **Spec:** `.project/active/taxonomy-graph-spacing/spec.md`
- **File:** `exploration/concept_explorer/static/js/neighborhood_graph.js`

## Research Findings

Single-file change. All relevant parameters are in `neighborhood_graph.js`:

- **Layout hints** (`buildElements`): `radius` (line 471) controls initial neighbor placement circle; `bDist` (line 506) controls bridge node placement distance.
- **CoSE layout** (`render`): `nodeRepulsion`, `idealEdgeLength`, `gravity`, `numIter`, `initialTemp` (lines 603-613) control force-directed simulation.
- **Stylesheet** (`buildStylesheet`): Node `width`/`height`, `font-size`, `text-outline-width`, `text-margin-y`, `text-max-width` for center/neighbor/bridge nodes and similarity/bridge edges (lines 318-461).

No other files reference these values. No tests exercise specific pixel values.

## Proposed Design

All changes are in `neighborhood_graph.js`. Three coordinated parameter groups:

### 1. Layout Spacing (FR-1) — ~3x expansion

| Parameter | Old | New | Ratio | Purpose |
|-----------|-----|-----|-------|---------|
| `radius` | 200 | 600 | 3.0x | Initial neighbor circle |
| `bDist` | 160 | 480 | 3.0x | Bridge node placement |
| `nodeRepulsion` (regular) | 8000 | 24000 | 3.0x | Force-sim repulsion |
| `nodeRepulsion` (bridge) | 4000 | 12000 | 3.0x | Bridge repulsion |
| `idealEdgeLength` (regular) | 180 | 540 | 3.0x | Target edge length |
| `idealEdgeLength` (bridge) | 140 | 420 | 3.0x | Bridge edge length |
| `gravity` | 0.25 | 0.08 | 0.32x | Reduced pull-to-center |
| `numIter` | 200 | 300 | 1.5x | More iterations for convergence |
| `initialTemp` | 200 | 600 | 3.0x | Higher initial energy for larger space |

Rationale: Consistent 3x multiplier on distance parameters. Gravity reduced to prevent the stronger repulsion from being overwhelmed. Higher initialTemp and numIter let the simulation settle in the larger space.

### 2. Font Sizes (FR-2) — proportional reduction

| Element | Old | New |
|---------|-----|-----|
| Center label | 14px | 10px |
| Neighbor label | 13px | 9px |
| Bridge label | 12px | 8px |
| Similarity edge label | 10px | 7px |
| Bridge edge label | 10px | 7px |

Supporting changes: `text-outline-width` reduced (2→1.5 or 1.5→1), `text-margin-y` tightened, `text-max-width` reduced to match smaller labels.

### 3. Node Dimensions (FR-3) — proportional reduction

| Node Type | Old | New |
|-----------|-----|-----|
| Center | 64px | 40px |
| Neighbor | 44px | 28px |
| Bridge | 36px | 22px |

Approximately 0.6x scale — nodes shrink but remain clearly visible with the increased spacing.

## Potential Risks

- **Low risk**: Parameters are purely visual. No data, interaction, or API changes.
- **CoSE convergence**: The 3x parameter space could produce different topologies on edge cases (many bridges). Mitigated by increased `numIter` and `initialTemp`.

## Validation Approach

- Visual inspection: load the explorer, navigate to a concept with neighbors + bridges
- Verify: nodes ~3x more spread out, labels readable but not dominating
- Verify: click, double-click, Ctrl+click, tooltip interactions all work unchanged
- Verify: bridge nodes appear correctly on comparison

---

Next Step: After approval → `/_my_implement` (changes already on branch — just needs review and commit)
