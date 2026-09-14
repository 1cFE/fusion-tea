# Spike: dagre layout and expand-collapse on the real calc DAG

**Date:** 2026-09-13 · **Branch:** feat/model-viz · **Commit:** 94f970bd · **Serves:** `.project/concepts/model-viz-design.md` § Architectural Bets ("Cytoscape.js with dagre layout") and § Next-Stage Handoff ("First risk to de-risk")

## Summary of Findings

**Verdict: the bet holds, with three things design must handle.** Cytoscape.js 3.28.1 with dagre and `cytoscape-expand-collapse` 4.1.0 draws the full stellarator calc DAG. Layout is fast: under half a second for everything expanded, under 0.1 s for the collapsed or one-group views. The collapse round trip is exact. LR reads better than TB. But the concept design's picture of how the extension works is wrong in two places, and the default collapsed view is not readable without edge bundling.

What design needs to know:

1. **The extension does rewrite edge `source`/`target`.** This contradicts the concept design's invariant "the original source/target data is not mutated" (§ Required Invariants › Collapse and Navigation). On collapse, the extension calls `edge.move()`. That points every crossing edge at the group node and stores the old endpoints in `data('originalEnds')` as element references. All 119 crossing edges were rewritten when collapsed. All 119 went back to their original endpoints after expand-all. The invariant's *intent* still holds: nothing is lost, and the round trip is exact. But the viewer cannot read `edge.data('source')` and trust it. The fix is cheap: the projection stamps its own immutable `origSource`/`origTarget` on each edge (the spike does this), and the detail panel reads those, or reads the projection directly. **This is a premise conflict with a recorded invariant, surfaced here, not resolved.** The invariant's wording needs amending in spec/design.
2. **Collapsed groups draw one edge per underlying producer edge, not one per group pair.** With everything collapsed there are 119 visible edges across 35 directed group pairs. `mfe_account_costs → mfe_plant` alone is 32 stacked curves. The result is a hairball of fans (`out/LR_1_all_collapsed.png`). The extension's `collapseAllEdges()` bundles them down to 31 edges and the picture becomes readable (`out/LR_1c_collapsed_edges_bundled.png`).
3. **Bundling merges both directions of a pair into one edge.** The 4 bidirectional group pairs each become a single edge tagged `data('directionType') === 'bidirection'`, drawn with one arrowhead by default. So 35 directed pairs become 31 edges. This breaks the concept's invariant "bidirectional edges between collapsed groups are rendered faithfully" unless design either styles `bidirection` edges with arrowheads on both ends, or does its own aggregation into one edge per *directed* pair.

Answers to the six questions, in short:

| # | Question | Answer |
|---|---|---|
| 1 | All collapsed readable? Bidirectional pairs? | Unbundled: no, fans of parallel edges. Bundled: yes. Unbundled draws both directions (32 edges one way, 7 back for account-costs ↔ plant). Bundled draws **one** edge per unordered pair. |
| 2 | `mfe_account_costs` expanded readable? | LR: yes. 21 first-rank cost calcs stack in a labeled column, the roll-ups sit to the right. Long cross-group edges pass through the box. TB: no. The same 21 calcs sit in one row and their labels overlap. |
| 3 | All expanded: time and usability? | 220–300 ms on a fresh page, about 400 ms right after expand-all. LR is usable as an overview, but labels are unreadable at fit-to-screen zoom and a few small group boxes overlap. TB is worse: the `mfe_plant` box overlaps the `mfe_account_costs` box. |
| 4 | Round trip identical? Endpoints mutated? | Identical: 119 crossing edges and 35 directed pairs with the same counts, before and after, for both `mfe_account_costs` and `mfe_plant`. Endpoints are mutated while collapsed and restored on expand (see finding 1). |
| 5 | Mechanics | `api.expand(cy.getElementById(groupId))`, synchronous. `cy.center(node)` works on the same tick. `cy.animate` needs its `complete` callback. A hidden calc is *absent* from `cy`, so the group must come from the projection. 4.1.0 loads with 3.28.1 with no console errors. |
| 6 | LR vs TB | LR. It keeps the large group's first rank legible and avoids the compound-box overlap TB produces. |

Also: this machine reaches unpkg (HTTP 200), so the spike loads the libraries from there. That says nothing about the modelers' machines. Whether to vendor copies is a design call.

## Question / Goal

**Assumption under test:** Cytoscape.js with dagre and `cytoscape-expand-collapse` can render the stellarator calc DAG navigably. The DAG is 76 calcs in 17 source-file groups with 150 producer edges. One group (`mfe_account_costs`) holds 33 calcs, and some group pairs have edges in both directions.

**Confirmed if:** layouts finish in interactive time, the collapsed and one-large-group-expanded views are readable, and collapse/expand preserves the inter-group edge set.

**Disproved if:** dagre is slow or unusable on the full graph, or the extension drops, duplicates, or reverses edges.

## Log

### Step 1: verify snapshot field paths

Script: `spike/probe_snapshot.py`.

- Paths confirmed. `snap.instance_graph.schema_version` is `instance-graph/v3`. `snap.instance_graph.graph.calcs` is a list of 76. Each calc has `node_id`, `display_name`, `source_file`, and `inputs[].edge`.
- **Correction to the research doc.** `node_id` is *already* a JSON-encoded string, the same string that appears in `edge.target.calculation`. The lookup key is the raw `node_id` string. The research doc's recipe `json.dumps(c['node_id'])` (`.project/research/20260912-004633_calc-dag-visualization.md:48`) double-encodes it and resolves 0 of 150 edges. In JS: `new Map(calcs.map(c => [c.node_id, c]))`, with no `JSON.stringify`.
- Edge kinds: 150 producer, 234 node, 52 null, 10 literal. All 150 producer edges resolve; 0 unresolved.
- Group sizes: 33, 10, 8, 7, 5, 2, and eleven groups of 1.
- The 150 edges split into 119 that cross groups (35 distinct directed pairs) and 31 inside a group.
- The 4 bidirectional pairs are `mfe_account_costs ↔ mfe_plant`, `mfe_magnet_field ↔ mfe_plasma_scaling`, `mfe_plasma_scaling ↔ mfe_plasma_sustainment`, and `mfe_power_balance ↔ mfe_primary_loop`.

### Step 2: library reachability and extension source

- `curl -sI https://unpkg.com/cytoscape@3.28.1/dist/cytoscape.min.js` returned HTTP 200.
- `cytoscape-expand-collapse@4.1.0` declares peer `cytoscape ^3.3.0`. The latest on unpkg is 4.1.1.
- Reading the 4.1.0 source:
  - `barrowEdgesOfcollapsedChildren` adds class `cy-expand-collapse-meta-edge`, stores `data('originalEnds') = {source, target}` as element refs, and calls `edge.move(...)` onto the collapsed node.
  - `repairEdges` moves edges back on expand.
  - `collapseEdges` replaces parallel edges with one new edge. That edge has class `cy-expand-collapse-collapsed-edge`, `data.collapsedEdges` (the originals), and `data.directionType` of `unidirection` or `bidirection`.
  - Events `expandcollapse.beforeexpand`/`afterexpand`/`beforecollapse`/`aftercollapse` fire on the node.

### Step 3: build the page

- `spike/build_page.py` inlines a trimmed copy of the snapshot (calcs with `node_id`, `display_name`, `source_file`, `inputs[].edge`) into `spike/page_template.html`. The output is `spike/dag_spike.html`.
- The page does the projection in JS, the way the real tool will:
  - Group nodes `g0…g16` hold calc nodes `c0…c75`, parented by `source_file`.
  - 150 edges `e0…e149` each carry their own `origSource`/`origTarget`.
  - Short index IDs are used because `node_id` strings contain quotes, which are awkward in Cytoscape selectors.
- Dagre options: `nodeSep 20, rankSep 60, edgeSep 5, animate false, fit true`.
- Expand-collapse options: `layoutBy null` (layout is run explicitly and timed), `fisheye false, animate false, undoable false, cueEnabled false`.

### Step 4: drive it under Playwright

Script: `spike/run_spike.py`. It uses headless Chromium at a 1600×1000 viewport and runs the whole sequence once for `rankDir=LR` and once for `rankDir=TB`. Raw output is in `spike/out/results.json`. The console and page-error logs are both empty for both runs.

- Timings are measured inside the page with `performance.now()` around the synchronous `cy.layout(...).run()`.
- The full driver took about 3 minutes wall time. I did not diagnose why. It is outside the measured layout calls (likely page load from unpkg plus headless canvas screenshots), so it does not bear on interactive time.

**Q3, all expanded (fresh page, initial state).**

| rankDir | 3 runs (ms) | expand-all after collapse, then layout (ms) |
|---|---|---|
| LR | 299, 245, 221 | 408 |
| TB | 288, 254, 249 | 396 |

- Screenshots: `out/LR_3_all_expanded.png`, `out/TB_3_all_expanded.png`, `out/LR_3b_expandAll_from_collapsed.png`, `out/TB_3b_expandAll_from_collapsed.png`.
- Edge audit while expanded: 150 visible edges, 0 with rewritten endpoints, 0 carrying `originalEnds`.
- LR observations:
  - `mfe_account_costs` takes about half the canvas.
  - Every calc label is roughly 6 px at fit zoom, so you have to zoom in to read anything.
  - The `mfe_fuel_cycle`, `mfe_divertor_heat`, and `mfe_vacuum` boxes overlap one another.
  - `stellarator_plant` touches the top of `mfe_plant`.
- TB observations:
  - The `mfe_plant` box overlaps the `mfe_account_costs` box.
  - Several rows of calc labels overprint.
- Dagre's compound-node support does not guarantee that group boxes don't overlap. This is the known weak spot the concept names ELK.js as the upgrade for.

**Q1, all collapsed.**

- `collapseAll()` took 17 ms; layout took 62 ms (LR) and 75 ms (TB).
- 17 visible nodes and 119 visible edges. All 119 have rewritten endpoints and carry `originalEnds`.
- Screenshots: `out/LR_1_all_collapsed.png`, `out/TB_1_all_collapsed.png`.
- Readability: poor. Every producer edge draws as its own bezier, so busy pairs become wide fans that cover other groups. The 32-edge `mfe_account_costs → mfe_plant` bundle loops far off the bottom of the frame.
- Bidirectional pair `mfe_account_costs ↔ mfe_plant`: 32 edges forward and 7 back, all visible, arrowheads at both boxes (`out/LR_1b_bidir_acc_plant_zoom.png`). So unbundled, the extension draws **both directions, as many edges as there are producer edges**.
- Bundled variant, `api.collapseAllEdges()` after `collapseAll()`: 119 edges became 31 (`out/LR_1c_collapsed_edges_bundled.png`, `out/TB_1c_collapsed_edges_bundled.png`).
  - The picture is readable: 17 boxes and single lines.
  - The directed pairs missing afterwards were exactly one direction of each bidirectional pair: `g0→g15` (account-costs→plant), `g4→g3`, `g9→g7`, `g4→g8`.
  - The merged edges carry `directionType: 'bidirection'`. In the screenshot, account-costs ↔ plant shows as one line with a single arrowhead pointing into account-costs.
  - Bundled edges carry class `cy-expand-collapse-collapsed-edge`, not `…-meta-edge`, so they need their own style rule. They render grey in the spike.

**Q2, `mfe_account_costs` expanded (others collapsed).**

- Layout took 86 ms (LR) and 89 ms (TB).
- Screenshots: `out/LR_2_account_costs_expanded.png`, `out/LR_2b_account_costs_zoom.png`, `out/TB_2_account_costs_expanded.png`, `out/TB_2b_account_costs_zoom.png`.
- LR:
  - The 21 leaf cost calcs (`blanket_cost` … `electric_cost`) form one vertical column with clean, non-overlapping labels.
  - The roll-ups (12 calcs: `om_cost`, `idc`, `installation`, `contingency`, `indirect`, `supplementary`, `fuel_calc`, `cas71/80/70/90`, `lcoe_1cfe_calc`) sit in 2–3 further ranks to the right.
  - No node overlap.
  - Crossings come from the other groups' incoming fans. Those edges cut straight through the box to reach the column.
  - Readable, once the unbundled fans from collapsed neighbours are dealt with.
- TB:
  - The same 21 calcs lie in one row, and their labels overprint into an unreadable strip.
  - Several roll-up labels also collide (`installation`/`contingency`/`indirect`).
  - Not readable at this spacing.

**Q4, collapse round trip.**

- Baseline, all collapsed: 119 crossing edges across 35 directed group pairs, with per-pair counts recorded.
- For each of `mfe_account_costs` and `mfe_plant` (the two ends of the busiest bidirectional pair): expand, layout, collapse, layout, recompute.

| group | crossing before / while expanded / after | distinct pairs before / after | per-pair counts identical | originals-based set identical |
|---|---|---|---|---|
| account_costs | 119 / 119 / 119 | 35 / 35 | yes | yes |
| mfe_plant | 119 / 119 / 119 | 35 / 35 | yes | yes |

Identical in LR and TB.

- While `mfe_account_costs` was expanded, there were 129 visible edges: its 10 internal edges came back with clean endpoints, and all 119 crossing edges stayed rewritten (their far end is still a collapsed group).
- After `expandAll()` from collapsed, all 150 edges were back to their original endpoints and `originalEnds` was gone. Restoration is exact.
- The "originals-based set" recomputes group pairs from the spike's own `origSource`/`origTarget` over visible edges plus edges held inside `collapsedChildren`.

**Q5, navigation mechanics.**

Target: `c65`, a calc in collapsed `mfe_plant`.

- While collapsed, `cy.getElementById('c65').length === 0`, because the extension removes children from the graph. `api.getCollapsedChildren(groupNode)` does contain it. The viewer must find the target's group from the projection (calc → group map), not from `cy`.
- `api.expand(groupNode)` is synchronous:
  - `expandcollapse.afterexpand` fired before `expand` returned.
  - Immediately after, `cy.getElementById('c65')` was present, `inside()`, and `visible()`.
- Same tick: `layout()`, then `cy.zoom(1.5)`, then `cy.center(node)`. The node's rendered position was (800, 490.25) in a 1600×1000 viewport, so it is centered. The 10 px y offset is the label height included in the bounding box. Screenshot: `out/LR_5_nav_center.png`.
- `cy.animate({center: {eles: node}, zoom: 1.5}, {duration: 300, complete})`:
  - Read on the same tick, the rendered position was not yet centered: (1014, 538) in LR, (894, 611) in TB.
  - In the `complete` callback it was (800, 490.25).
  - So animation is async. Chain any follow-up (selection highlight, panel scroll) on `complete`.
- `api.expand(groupNode, {layoutBy: {name:'dagre', rankDir, animate:false, fit:false}, fisheye:false, animate:false})` followed by `cy.center(node)` on the same tick also centered it (800, 492.6). The extension can run the re-layout itself.
- Version: `cytoscape.version === '3.28.1'` with `cytoscape-expand-collapse@4.1.0`. No console errors, no page errors. **Not tested:** 4.1.1, the current latest on unpkg.

**Q6, rankDir.** Compare `out/LR_1c_collapsed_edges_bundled.png` with `out/TB_1c_collapsed_edges_bundled.png`, `out/LR_2b_account_costs_zoom.png` with `out/TB_2b_account_costs_zoom.png`, and `out/LR_3_all_expanded.png` with `out/TB_3_all_expanded.png`. LR wins on the two views that matter: the expanded large group and the full graph. The deciding factor is the 21 same-rank leaf cost calcs. LR stacks them vertically, so their horizontal labels have room. TB lays them side by side, where the labels collide.

## Reproduction

From the repo root (`/home/reid/1cfe/fusion-tea`), with network access to unpkg.com:

```bash
uv run python .project/active/model-viz/spike/probe_snapshot.py   # field paths, counts, bidirectional pairs
uv run python .project/active/model-viz/spike/build_page.py       # writes spike/dag_spike.html
uv run python .project/active/model-viz/spike/run_spike.py > /tmp/spike_run.log 2>&1   # ~3 min; writes spike/out/*.png and results.json
```

- Expected probe output: `producer resolved: 150 unresolved: 0`, `groups: 17`, `inter-group distinct pairs: 35 inter-group edges: 119 intra: 31`, and 4 bidirectional pairs.
- Expected `results.json`: `roundtrip_*.identical_pairs_and_counts: true`, `collapsed_edge_audit.mutated: 119`, `nav.collapseAllEdges.after: 31`, and empty `console` and `pageerrors`. Timings will vary by machine.
- Redirect output to a file. Piping the driver to `tail` under a short `timeout` shows nothing until exit.
- `dag_spike.html` also opens by hand in a browser. `window.spike` exposes `cy`, `api`, `layout()`, `interGroupEdges()`, and `edgeDataAudit()`, and `?rankDir=TB` switches direction.

## Open Questions / Follow-ups

- **Invariant wording (for spec/design).** "The original source/target data is not mutated" is false for this extension. Suggested amendment: "original endpoints are recoverable and the round trip is exact; the viewer reads endpoints from the projection, not from live edge data." That is a spec/design decision, not settled here.
- **Bidirectional rendering when bundled.** Choose one:
  - Style `edge[directionType='bidirection']` with `source-arrow-shape` so it shows arrows at both ends. Cheapest.
  - Skip `collapseAllEdges` and aggregate into one edge per directed pair in the viewer. Keeps two distinct lines.
  - Accept unbundled fans. Not recommended; see `out/LR_1_all_collapsed.png`.
  Not tested: how bundled edges behave through a later expand (`expandAllEdges` was called before `expandAll` in the spike, and the counts came back right, but a single-group expand with bundled edges present was not exercised).
- **Group-box overlap in the all-expanded view.** Dagre's compound handling let small boxes overlap in LR and big ones overlap in TB. Tuning (`nodeSep`, `rankSep`, padding), a readable-zoom starting viewport instead of fit-all, or ELK.js are the options. None was tried.
- **Long cross-group edges through the expanded box.** Dagre does not route around compound boxes. A usability issue, not a correctness issue.
- **Library delivery.** unpkg is reachable here. Vendored copies are a design call for offline or locked-down machines.
- **Upstream back-reference not written.** The spike skill asks for a back-reference in the concept design at § Architectural Bets / § Next-Stage Handoff. The orchestrator brief restricts this stage to `spike/` and this findings doc, so the concept doc was not edited. The orchestrator or the spec stage should add the link.
