# Manual layout walk — model-viz viewer

**Date:** 2026-09-13
**Script:** `manual_walk.py` (beside this file), headless Chromium 145, viewport 1600×1000, fixture `exploration/stellarator_e2e/stellarator.snapshot.json` loaded through the file input. Page problems captured during the walk: none (no page error, no console error, no network request).
**Walk:** load (all collapsed) → real click on `mfe_account_costs (33)` → real click on the calc `fuel_handling` → real click on its first upstream link (`pb`) → Expand all.

The plan's walk named `cas22_capital` as the cost calc. It lives in `mfe_plant.sysml`, which is still collapsed at step 3, so it cannot be clicked on the canvas there. The walk uses `fuel_handling`, a calc inside the group opened at step 2.

## 01_all_collapsed.png

- 17 boxes, all labels legible at the fit zoom (`mfe_account_costs (33)`, `mfe_plant (10)`, and so on).
- Design-file boxes (`mfe_plant`, `stellarator_plant`) stand out as the only dashed warm boxes.
- Two-way pairs show as two curved edges with separate arrowheads. `mfe_account_costs` ↔ `mfe_plant` is the clearest: two thick curves, one each way. `mfe_magnet_field` ↔ `mfe_plasma_scaling` and `mfe_power_balance` ↔ `mfe_primary_loop` also show two curves.
- Thicker edges carry more bindings, which points the eye at the heavy flows (`mfe_plasma_scaling` → `mfe_account_costs`, `mfe_account_costs` ↔ `mfe_plant`).
- The graph uses the middle of the pane; there is empty space above and below because dagre's LR layout is wide and short here. Fit button restores this view.

## 02_account_costs_expanded.png

- The 33 calcs open in a large box on the right; the other 16 boxes stay collapsed around it. The result lands where the eye expects: the clicked box grew in place of itself, and the rest rearranged around it.
- At the fit zoom the calc labels inside the big box are small (about 5–6 px). They are readable in the screenshot but need a zoom-in in real use. Layout is comparable to the spike's `spike/out/LR_2_account_costs_expanded.png`: the same two columns of cost calcs on the left of the group, the capital roll-up chain on the right, and the heavy fan-in from `mfe_power_balance` and `mfe_plasma_scaling`. The viewer draws one edge per box pair instead of the spike's parallel orange lines, so the fan into the group is less of a hairball.

## 03_cost_calc_selected.png

- `fuel_handling` has an orange 3 px border, and the panel shows it (formula lines, the doc repeat note on entry 3, documentation).
- Its drawn edges are orange, and so is the border of the box at their other end (`mfe_power_balance (2)`, which holds its producer `pb`). The selection and its neighbourhood stand out against the grey graph.

## 04_after_upstream_link.png

- Clicking `pb` in the Inputs section opened `mfe_power_balance`, selected `pb`, zoomed to 1.0 and centred it. `pb` sits in the middle of the pane with all 27 outgoing bindings highlighted; the labels of its consumers in `mfe_account_costs` are fully legible at this zoom.
- Every box moved in the re-layout, but the target is centred and highlighted, so there is nothing to search for.
- One cosmetic collision: the collapsed `mfe_primary_loop (1)` box sits on top of the `mfe_power_balance` group label at the top left.

## 05_all_expanded.png

- 76 calcs in 17 group boxes. At the fit zoom calc labels are too small to read; this view is for shape, not reading.
- `pb` stays selected with its edges highlighted after the rebuild.
- Checked at 2× resolution (`/tmp` crop, not kept) and by comparing container bounding boxes in `cy`: no two group boxes overlap in this layout, unlike the rebuild check's `mfe_plant` / `mfe_account_costs` overlap. The readability cost shows up differently: `mfe_power_balance` holds only 2 calcs but is drawn as a large, mostly empty box because dagre puts its two calcs in far-apart ranks, and many edges cross it and the big `mfe_account_costs` box. Small group labels (`mfe_fuel_cycle`, `mfe_divertor_heat`) sit close enough to touch.

## Bets

- **B3 (a modeler can orient from 17 collapsed boxes with 35 edges): held.** Screenshot 01 is readable at a glance; the heavy flows and the four two-way pairs are visible without zooming.
- **B4 (compound layout problems are a readability cost, not a correctness one): held.** No box overlap on this fixture, but sparse oversized groups and edges crossing boxes make the all-expanded view hard to read. The edge tests pass in every collapse state, so what is drawn is still right. ELK.js remains the recorded upgrade path if this becomes the working view.
- **B5 (full re-layout with fit on every expand does not disorient): held, with a caveat.** Opening one group (02) and navigating (04) both move every box, but the opened group or the centred, highlighted target is where the eye goes. The caveat: after a plain toggle there is no highlight to anchor on, so a modeler who toggles several groups in a row has to re-find their place each time. Recorded for the owner; no architecture change in this item.
