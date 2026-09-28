# Design-point cost after each frame

Evidence note for [Part 4, support 1: Modeling Stellaris](../stellaris-evolution.md). The evolution viewer shows no cost, because the model snapshots it reads carry no computed values; the cost figures in each frame's result text come from the goal's own record. This note lists, for every frame, the model's headline levelized cost at the reference geometry (major radius 12.7 m, minor radius 1.3 m) before and after the goal's model change, with the record each number comes from. Paths are relative to `work/orchestration/goals/<slug>/` unless they start with `work/`, `exploration/` or `.project/`.

Two cautions when reading the column:

- The reference point splits at frame 22. The cooling goal headlined a separately retained 18-circuit study case (150.430 before, 310.633 after), while the model's default plant has 14 circuits (270.824 after; its value before the change is not printed in that goal's records, and 144.747 is the last printed default, at frames 20 and 21). Every later frame reports the 14-circuit default.
- A cost that did not move is not a goal that did nothing. Frames 5, 8, 9, 16, 17, 19, 20, 21, 24, 26 and 29 added calculations or checks that leave the design point's cost unchanged and change which designs pass.

| Frame | Goal | Closed | Before ($/MWh) | After ($/MWh) | Source | Note |
|---|---|---|---|---|---|---|
| 2 | p-pump-fence | 2026-08-29 | 275.264 | 333.067 | trail.md:114; trail.md:206, :451 | The regenerated package carries the 195 MW pumping power (WI-033, landed under p-pump-basis); no equation changed. Six checks. |
| 3 | magnet-closure | 2026-09-01 | 333.067 | 304.482 | trail.md:161 | Capital $16.090B to $14.574B. |
| 4 | operating-point-closure | 2026-09-02 | 304.482 | 307.087 | trail.md:192 | Sustainment check violated at the design point, disclosed not fitted (trail.md:104). |
| 5 | priced-levers | 2026-09-03 | 307.087 | unchanged | trail.md:153 | Design point reproduces all nine anchors exactly. |
| 6 | wall-and-heating | 2026-09-05 | 307.087 | 313.513 | trail.md:68; trail.md:285, :313 | Round 1's heating chain did not move the baseline; round 2's peak wall load did, through the replacement count. |
| 7 | stored-energy-basis | 2026-09-06 | 313.513 | 322.318 | trail.md:200, :231 | Fusion power fell 2.7 percent; all nine checks satisfied. |
| 8 | burn-control | 2026-09-07 | 322.318 | unchanged | trail.md:36, :139 | Tenth check added; 102 channels, none differing. |
| 9 | minor-radius | 2026-09-08 | 322.318 | unchanged | trail.md:37, :61 | All 102 channels bit-identical. |
| 10 | plant-closure | not formally closed; owner accepted the grading packet 2026-09-12 | 322.318 | 224.610 | trail.md:100; trail.md:121, :163 | Three items at one pin: the primary loop and cycle moved it to 237.253, the maintenance calendar to 224.610, the flows not at all. Fourteen checks, divertor heat violated by design. |
| 11 | fusion-audit-remediation | not formally closed; unanswered after round 12 | 224.610 | 224.269 | trail.md:602; trail.md:868 | The stellarator move lands in round 4 (WI-050, coherent operating heating). |
| 12 | structural-decomposition | not formally closed | 224.269 | unchanged | trail.md:112 | Neutral on all 158 channels and 18 checks. |
| 13 | magnet-design-transfer | 2026-09-14 | 224.269 | 142.507 | work/analysis/20260914-045431_audit_WI-040.md:49; transfer-claim.md:21 | The unsplit winding estimate replaced; "not demonstrated cost savings". |
| 14 | magnet-coil-realism | agent completion 2026-09-15 under owner delegation | 142.51 | 146.31 | answer.md:9 | Refrigeration power 0.864 to 2.138 MW. |
| 15 | tape-procurement-consistency | not formally closed; review recommends closure | 146.31 | 144.74 | answer.md:31 | Tape $804.00M to $731.57M. |
| 16 | winding-pack-casing-fit | not formally closed | 144.74 | unchanged | answer.md:27 | Fit check added; the reference fails it. |
| 17 | absolute-conductor-current-margin | not formally closed | 144.74 | unchanged | answer.md:43 | Current-margin check added; the reference fails it. |
| 18 | magnet-manufacturing-cost-completeness | not formally closed | 144.738 | 144.747 | answer.md:39 | Insulation stock charge only. |
| 19 | joint-magnet-sizing-feasibility | not formally closed | 144.747 | unchanged | answer.md:9, :70 | Legacy mode stays the default; the optional current-sizing mode reads 163.194. |
| 20 | divertor-peak-heat-load | not formally closed | 144.747 | unchanged | answer.md:61 | Diagnostic outputs only. |
| 21 | computed-tritium-breeding | 2026-09-18 | 144.747 | unchanged | answer.md:28; exploration/stellarator_e2e/studies/20260918-computed-tritium-breeding/record.md:25 | Breeding check fails at the 0.80 m reference. |
| 22 | installed-cooling-equipment-costs | 2026-09-18 | 150.430 (18-circuit case); default not printed | 310.633 (18-circuit case); 270.824 (14-circuit default) | answer.md:63, :65; exploration/stellarator_e2e/studies/20260918-installed-cooling-equipment-costs/record.md:21 | Reference definition splits here; see the caution above. |
| 23 | layout-based-facilities | 2026-09-19 | 270.824 | 273.455 | answer.md:11 | 14-circuit default. The 18-circuit scenario is retained separately: 310.633 to 314.182 (answer.md:12). |
| 24 | fuel-inventory-and-startup | 2026-09-19 | 273.455 | unchanged | answer.md:45 | |
| 25 | throughput-based-fuel-processing-costs | 2026-09-19 | 273.455 | 271.584 | answer.md:23 | Capital down $141.271M. |
| 26 | cost-estimate-maturity-and-uncertainty | 2026-09-19 | 271.584 | unchanged | answer.md:3, :44 | The new input's nominal value preserves all 956 outputs. |
| 27 | current-model-comparison-readiness | 2026-09-20 | 271.584 | 318.737 | answer.md:6 | Steam cycle at the salt temperature; published as r3. |
| 28 | preserve-model-design-choices | 2026-09-20 | 318.7372 | 318.7377 | evidence/entering-native-baseline.json:1052; work/active/WI-080_supplied-thermal-equipment-capability-and-demand-checks/integration/seam/baseline_result.json:1053 | All 1,095 prior non-cost channels unchanged (answer.md:20). |
| 29 | model-evaluation-domain-readiness | 2026-09-20 | 318.7377 | unchanged | work/analysis/model-evaluation-domain-readiness/summary.json:115 | 67 checks: 61 satisfied, 6 violated (answer.md:13). |

The three largest single-goal moves at the design point are the cooling equipment (frame 22: +126 on the 14-circuit default, +160 on the 18-circuit case), the plant closure (frame 10: −98) and the winding-pack replacement (frame 13: −82). Next are the pumping-power correction (frame 2: +58), the steam cycle (frame 27: +47) and the magnet derivation (frame 3: −29).

## Model size

The counts in the piece's lead (55 calculations, 6 checks and 14 parts at frame 1; 199, 67 and 76 at frame 29) are the viewer's own tiles, computed by its build from the model snapshots in git (`src/model_viz/evolution/build.py` on branch `feat/model-viz-evolution`; rebuilt 2026-09-26 and identical to the owner's page). They count calculation and part occurrences in the generated package. The goal records give the check count at several points along the way: 6, then 9 (stored-energy-basis trail.md:231), 10 (burn-control trail.md:59), 14 (plant-closure trail.md:142), 18 (structural-decomposition trail.md:112), 20 (magnet-manufacturing-cost-completeness answer.md:39), 25 (layout-based-facilities answer.md:14), 34 and 67 (preserve-model-design-choices trail.md:99, answer.md:16). Counting definitions in the SysML source instead of occurrences, the model went from 42 calculation, 7 constraint and 36 part definitions in 22 files at the 2026-08-21 baseline commit to 114, 27 and 65 in 48 files at the frame 29 close.

## Provenance

[AGENT] Compiled 2026-09-26 by a verification agent reading each goal's trail and answer; the frame result texts in the viewer were not used as a source. Four goals that are not frames ran between frames 21 and 22 (primary-loop-sizing, bounded-feasibility-transfer, stellaris-reference-reconciliation, pre-reveal-feasible-neighborhood) and introduced the 18-circuit scenario.
