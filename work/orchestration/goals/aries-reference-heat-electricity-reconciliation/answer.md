# Answer — ARIES reference heat-to-electricity reconciliation

Goal: `work/orchestration/goals/aries-reference-heat-electricity-reconciliation/` (grounded `52e01b48`; round 1 sealed `581e3c1a`, closed `53717509`, reviewed `e204afed`; round 2 implemented `49668453`, re-pinned `6828df18`, accepted `4f5991a5`, sealed `352ecee4`, record completed `b6d24a64`). Written by the round-2 coordinator on 2026-09-25; formal goal and item closure are reserved for the owner. Every number below is a stored native output of one of the two sealed studies or a graded source value from `evidence/reference-case-contract.md`; presentation arithmetic is in the studies' `results/attribution.md`.

## 1. The question and the short answer

**Question.** When supplied the published ARIES fusion power (2436 MW), why does the model calculate about 796 MW net instead of the reported 1000 MW, and why can it not remove all the heat?

**Answer.** Two separate things were wrong with the original case, and one thing is a property of the published description rather than of the model.

1. The heat could not be removed (158.7 MW left in the PbLi stage) because the inherited model connected the three primary-side exchangers in series in one cycle stream (helium, then divertor, then PbLi), so the PbLi stage received cycle helium already heated by the divertor stage, and the PbLi capacity rate (5.10 MW/K) was too small to cool the PbLi against it. The published plant (Raffray Fig. 12) puts the PbLi and divertor exchangers in parallel after the blanket-helium exchanger. Representing that network (WI-092, reviewed for MR-7 before implementation) removes this mechanism: at the source-supported inputs it takes 41.125 MW off the 151.002 MW shortfall with no hardware change. What is left (109.876 MW at the 1600 kg/s cycle-flow convention) is a different mechanism: with the source's 0.95 recuperation, the whole cycle flow enters the blanket-helium stage at 309 °C and can only be heated to 452.4 °C against the 456 °C helium hot inlet, so the helium stage itself cannot carry its duty at that flow. That residual disappears with 1700 kg/s of cycle flow (which needs a compressor rated above the assumed 1600 MW; the declared resized alternative at 1700 MW is the best steady point, net 891.003 MW) or with the inherited 0.8 recuperation at 1600 kg/s (net 759.886 MW). Both are operating or hardware choices the sources do not state.
2. The original 796 MW was low for input-level reasons that round 1 quantified and corrected from the sources: assumed 0.8 recuperation (source 0.95), 1400 kg/s cycle flow (1600 derived from Lyon's 2916 MW over Raffray's cycle temperatures), 500 kg/s divertor flow (source 283), a deposition partition that sent about 218 MW too much heat to the divertor and 198 MW too little to the blanket circuits, and an auxiliary itemisation 20 MW below Lyon's 252 MW. Together these are worth +46.727 MW net on the series arrangement; with the network the combined correction is +83.687 MW (order interaction +7.6 MW).
3. The remaining gap to the reference is not reproducible from the published hardware description. At the best steady point the model is 109.987 MW gross and 108.997 MW net short, and all of it is thermal efficiency (0.3907 against the reference 0.43), which is the turbine inlet (628 °C against the published 708 °C). The published 43% needs a 708 °C turbine inlet, and with the published duties the published network cannot reach it at any split (the PbLi stream leaves at 655 °C at the 0.85 split and mixes with a cooler divertor stream). This is the independently checked source-reading Q1 in the contract: the published temperatures, duties and arrangement cannot all hold, and the reference 2916 → 43% → 1253 → −253 → 1000 is a systems-code chain, not an exchanger result.

So: the original case was a thermally inadequate scenario, not a steady operating point; its two causes are corrected (one by the reviewed architecture change, one by a declared operating or hardware choice); and the model's steady result disagrees with the published 1000 MW by about 108.997 MW for a reason that is explained and bounded but cannot be settled from the retained sources. Net 1000 was never a target and is not reached at any steady point.

## 2. Source case definition

[OWNER] The supplied boundary is Lyon's ARIES-CS systems reference (`reference-case-contract.md` § 2–3; page images `lyon-p703/704/707/715/717.png`): fusion power 2436 MW supplied to the model's producer in source mode; ignited plasma (no deposited heating); thermal power 2916 MW; gross 1253 MW at 43%; recirculating 253 MW printed, itemised 170 (blanket helium pumping) + 27 (divertor pumping) + 55 (balance of plant and cryogenics) = 252; net 1000 MW; 90% of pumping and balance-of-plant power returned as heat. Raffray's engineering case (2365 MW; `raffray-p738/741/742.png`) supplies the hardware description only: helium circuit 1192 MW at 386 → 456 °C and 3261 kg/s with 156 MW pumping; PbLi 1444 MW at 451 → 738 °C; divertor 186 MW at 573 → 700 °C and 283 kg/s (about 67 MW of it unlabelled); Brayton cycle 355 → 707 °C with 0.95 recuperator effectiveness and a 30 °C approach; Fig. 12's series-then-parallel exchanger network. The two cases are never combined without the contract's scaling rule (§ 8), and supplied outputs earn no prediction credit.

Grades and confidence per quantity are in the contract; the materiality budget (`materiality-budget.md`, fixed before any refinement study and reviewed) is net and gross ±15 MW, total thermal ±10 MW, per-circuit heat ±10 MW, unmet heat 0, turbine inlet ±5 K about 708 °C.

## 3. Baseline and revised heat / electricity tables

All values MW unless stated; stored outputs of `20260925-aries-revised-reference-network` (`results/cases.json`), on which the original case and the round-1 series cases replay bit-exactly against the entry package. "All checks" means every one of the 14 evaluated scalar checks is satisfied (capacity screens, ledger balance, heat removal); it is not scientific feasibility.

| Case | Available heat | Accepted | Unmet (He / PbLi / div) | Turbine inlet °C | Efficiency | Gross | Auxiliary | Net | All checks | Failed checks |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| Original failing case (`nominal-source-assumed`) | 2917.808 | 2759.082 | 158.726 (0.000 / 158.726 / 0.000) | 662.6 | 0.3728 | 1028.659 | 232.653 | 796.005 | no | plant_ledger.heat_removal_ok |
| Literal Lyon source-input variant | 2917.808 | 2518.899 | 398.909 (169.870 / 229.039 / 0.000) | 667.0 | 0.4127 | 1039.670 | 232.653 | 807.017 | no | plant_ledger.heat_removal_ok |
| C3: every source-supported input correction, series (round 1) | 2925.762 | 2774.760 | 151.002 (0.000 / 151.002 / 0.000) | 634.7 | 0.3945 | 1094.742 | 252.010 | 842.732 | no | plant_ledger.heat_removal_ok |
| Network alone on the original inputs | 2917.808 | 2799.945 | 117.863 (0.000 / 0.000 / 117.863) | 674.2 | 0.3779 | 1058.067 | 232.653 | 825.414 | no | plant_ledger.heat_removal_ok |
| Revised source-conditioned case: C3 + published network, split 0.85 | 2925.762 | 2815.886 | 109.876 (53.514 / 56.362 / 0.000) | 647.5 | 0.4019 | 1131.703 | 252.010 | 879.693 | no | plant_ledger.heat_removal_ok |
| Same at split 0.90 | 2925.762 | 2818.528 | 107.234 (57.575 / 49.660 / 0.000) | 648.3 | 0.4024 | 1134.077 | 252.010 | 882.067 | no | plant_ledger.heat_removal_ok |
| Steady candidate A: C3 + network, 0.8 recuperation, 1600 kg/s | 2925.762 | 2925.762 | 0.000 (0.000 / 0.000 / 0.000) | 606.2 | 0.3459 | 1011.896 | 252.010 | 759.886 | yes | — |
| Steady candidate B (declared resized compressor): C3 + network, 0.95 recuperation, 1700 kg/s, rating 1700 MW | 2925.762 | 2925.762 | 0.000 (0.000 / 0.000 / 0.000) | 628.2 | 0.3907 | 1143.013 | 252.010 | 891.003 | yes | — |
| Declared resized compressor at 1800 kg/s (network or series) | 2925.762 | 2925.762 | 0.000 (0.000 / 0.000 / 0.000) | 580.8 | 0.3608 | 1055.573 | 252.010 | 803.563 | yes | — |
| Published Lyon reference (Table IV) | 2916 | 2916 | 0 | 708 | 0.43 | 1253 | 253 (252 itemised) | 1000 | — | — |

Heat by circuit and stage temperatures for the same cases:

| Case | He circuit delivered | PbLi delivered | Divertor delivered | He transferred | PbLi transferred | Divertor transferred | Cycle inlet to first stage °C | After He stage °C | PbLi stream out °C | Divertor stream out °C | PbLi return °C |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Original failing case (`nominal-source-assumed`) | 1143.755 | 1379.653 | 394.400 | 1143.755 | 1220.927 | 394.400 | 283.1 | 440.4 | 662.6 | 494.7 | 498.8 |
| Literal Lyon source-input variant | 1143.755 | 1379.653 | 394.400 | 973.885 | 1150.614 | 394.400 | 320.5 | 454.5 | 667.0 | 508.7 | 512.5 |
| C3: every source-supported input correction, series (round 1) | 1248.568 | 1485.785 | 191.410 | 1248.568 | 1334.783 | 191.410 | 300.8 | 451.1 | 634.7 | 474.1 | 476.5 |
| Network alone on the original inputs | 1143.755 | 1379.653 | 394.400 | 1143.755 | 1379.653 | 276.537 | 289.1 | 446.4 | 669.7 | 700.0 | 456.9 |
| Revised source-conditioned case: C3 + published network, split 0.85 | 1248.568 | 1485.785 | 191.410 | 1195.054 | 1429.422 | 191.410 | 308.6 | 452.4 | 654.8 | 606.0 | 457.9 |
| Same at split 0.90 | 1248.568 | 1485.785 | 191.410 | 1190.993 | 1436.125 | 191.410 | 309.1 | 452.4 | 644.5 | 682.8 | 456.6 |
| Steady candidate A: C3 + network, 0.8 recuperation, 1600 kg/s | 1248.568 | 1485.785 | 191.410 | 1248.568 | 1485.785 | 191.410 | 254.0 | 404.3 | 614.7 | 557.9 | 410.0 |
| Steady candidate B (declared resized compressor): C3 + network, 0.95 recuperation, 1700 kg/s, rating 1700 MW | 1248.568 | 1485.785 | 191.410 | 1248.568 | 1485.785 | 191.410 | 296.8 | 438.2 | 636.2 | 582.8 | 442.5 |
| Declared resized compressor at 1800 kg/s (network or series) | 1248.568 | 1485.785 | 191.410 | 1248.568 | 1485.785 | 191.410 | 267.8 | 401.4 | 588.4 | 537.9 | 404.6 |
| Raffray engineering case scaled to 2436 MW (contract § 8) | 1223.6 | 1487.4 | 190.9 | — | — | — | 355 | 456 (He outlet) | 708 (738 − 30) | 700 | 451 |

Split sensitivity of the revised source-conditioned case at C3 (0.95 recuperation, 1600 kg/s):

| Split | Unmet (He / PbLi / div) | Turbine inlet °C | Gross | Net |
|---:|---:|---:|---:|---:|
| 0.50 | 246.223 (0.000 / 246.223 / 0.000) | 605.2 | 1009.163 | 757.153 |
| 0.60 | 162.079 (0.000 / 162.079 / 0.000) | 631.3 | 1084.786 | 832.776 |
| 0.70 | 127.467 (26.473 / 100.994 / 0.000) | 642.0 | 1115.893 | 863.883 |
| 0.80 | 113.678 (47.669 / 66.009 / 0.000) | 646.3 | 1128.286 | 876.276 |
| 0.85 | 109.876 (53.514 / 56.362 / 0.000) | 647.5 | 1131.703 | 879.693 |
| 0.90 | 107.234 (57.575 / 49.660 / 0.000) | 648.3 | 1134.077 | 882.067 |
| 0.95 | 139.926 (7.321 / 44.110 / 88.495) | 638.2 | 1104.696 | 852.686 |
| 0.98 | 168.484 (0.000 / 18.993 / 149.491) | 629.3 | 1079.030 | 827.020 |

## 4. Quantitative attribution

From the original 796.005 MW net (ledger v2, `evidence/discrepancy-ledger.md`; `results/attribution.md`):

- Input-level corrections, series arrangement (C1 thermal inputs +81.075; Lyon auxiliaries -17.586; source-informed partition -16.762): +46.727 MW to 842.732 MW, unmet 158.726 → 151.002.
- Published network alone on the original inputs: +29.409 MW; on C3: 36.961 MW (unmet 151.002 → 109.876). Combined corrections and network: +83.687 MW to 879.693 MW; the sum of the two separate effects is +76.135 MW, so the order interaction is +7.552 MW net and -0.263 MW unmet. The network step by position in the change order:

| Position in the change order | Series unmet → network unmet | Series net → network net | Network step (net) |
|---|---:|---:|---:|
| original | 158.726 → 117.863 | 796.005 → 825.414 | +29.409 |
| C1 | 126.367 → 82.769 | 877.080 → 916.263 | +39.183 |
| C2 | 132.350 → 83.417 | 859.494 → 903.473 | +43.979 |
| C3 | 151.002 → 109.876 | 842.732 → 879.693 | +36.961 |

- Reaching a steady point: 0.8 recuperation at 1600 kg/s costs -119.807 MW (to 759.886); the declared resized compressor at 1700 kg/s with the network gains 11.310 MW (to 891.003); 1800 kg/s gives 803.563 in either arrangement.
- Against the reference at the best steady point: gross 1143.013 versus 1253 (-109.987), net 891.003 versus 1000 (-108.997), auxiliary 252.010 versus 253 (-0.990, inside budget), available heat 2925.762 versus 2916 (+9.762, inside budget), efficiency 0.3907 versus 0.43, turbine inlet 628.2 versus 708 °C (outside the ±5 K budget). The net and gross gaps are outside the ±15 MW budget everywhere.

## 5. Status of every material discrepancy

| Discrepancy | Status | How |
|---|---|---|
| 158.7 MW unremoved heat | **Corrected** in two parts | Series-order PbLi limit removed by the reviewed network increment (WI-092); helium-stage bound at 1600 kg/s with 0.95 recuperation removed by a declared choice the sources do not state: 1700 kg/s with a 1700 MW compressor (resized alternative, all checks) or 0.8 recuperation at 1600 kg/s (all checks). No case with unremoved heat is presented as a steady reconstruction. |
| Recirculating power (232.7 vs 253) | **Corrected** | Accounting alignment to Lyon's itemisation (252.010; inside ±15). |
| Heat by circuit (He −80, PbLi −108, divertor +204) | **Corrected** | Source-informed deposition partition (0.657 radiated, 0.0469 exchanged); residual He +25 MW bounded by the pump-heat return fraction (Lyon 170 versus Raffray 141). |
| Thermal power composition | **Bounded** (≈ 60 MW thermal, ≈ 26 MW gross) | No model input for the source's 90% return of balance-of-plant power; inside the ±10 MW total-thermal budget at every revised case (+9.8). |
| Gross and net shortfall at the best steady point (−110 / −109) | **Explained**, not corrected | Entirely the efficiency shortfall at the heat-limited turbine inlet; the published 708 °C and 43% are unattainable with the published duties and arrangement in this model (Q1); bounded above by the resized alternative. |
| Whether ARIES's 43% was attainable in the actual design | **Unresolved** (owner-visible premise) | The retained papers do not describe the cycle arrangement in enough detail to decide; the contract's Q1 was independently confirmed by the source-check reviewer and is surfaced to the owner rather than resolved. |

## 6. Remaining uncertainty

- Q1 (owner gate): the published temperatures, duties and arrangement cannot all hold; either a temperature, a duty, or the arrangement in the retained description is not what the design used. Resolving it needs source evidence beyond the retained papers; the prescribed research route applies if the owner wants it pursued.
- The supplied split between the parallel stages (design default 0.85, broad low 0.80–0.90 at C3) stands in for an unmodelled branch hydraulic balance; nothing redistributes flow, and the 0.85 default is not the best sampled value.
- Cycle flow (1600 kg/s) is a cross-source derived convention, not a printed value; the compressor rating (1600 MW) is an inherited assumption (A6); the resized alternative's cost consequences were not evaluated.
- Thermal composition (≈ 60 MW), the unlabelled ≈ 67 MW divertor share and the 253/252 itemisation are bounded ledger items, never tolerance.
- The model's efficiency-versus-turbine-inlet relation is its own cycle model (inherited from WI-089) and was not qualified against the source's cycle beyond the recuperation and approach values.

## 7. Engineering statuses

Seven of 27 round-2 points satisfy every evaluated check: the calculated baseline; the three 0.8-recuperation cases at 1600 kg/s; and the three declared resized-compressor cases (1700 kg/s network; 1800 kg/s series and network). The source-conditioned network case at the 1600 kg/s convention fails heat removal (109.876 MW) and is reported as not steady. The two inherited-rating cases at 1700 and 1800 kg/s remove all heat and fail the compressor screen; they are retained as adverse points and not relabelled. The literal Raffray accounting case (retained in round 1) keeps its −182 MW source-energy mismatch. No result was produced by resizing, clipping, target substitution or automatic passing; unsupported scientific checks inherited from WI-089 remain unsupported (`snapshot.json` § science_qualification).

## 8. Reuse and model changes

- **Reused unchanged:** the WI-089 heat-driven closure equations (bound as mode 0 of the new definition and retained as `'Heat Driven Closure'` in the library), the WI-090 equipment bindings, the WI-091 lifecycle chain, the stock study tooling (indicators, preflight, verifier, manifest, integration seam), the round-1 composer and the predecessor executor.
- **Changed (ARIES-only file, WI-092):** `models/library/analyses/integrated_heat_electricity.sysml` gains `calc def 'Network Heat Driven Closure'` (25 inputs, 45 outputs; mode 0 series, mode 1 the published network with a supplied split); `models/designs/aries_cs_integrated/plant.sysml` rebinds `heat_exchangers.evaluate` to it with `network_mode` (default 0) and `pbli_split_fraction` (default 0.85); new completion `native_completions/network_heat_driven_closure_impl.py`; package regenerated on the stock route to a fixed point (executable `f739dbce…`, semantic `78dd23bf…`); live manifest and interface re-pinned (two entry keys and five outputs added, none removed) and later amended with four reviewed absolute comparison tolerances; the package-owned oracle learned mode 1; thin study modules `revised_reference_support.py` and `revised_reference_reporting.py`. No shared-family definition consumed by Stellaris changed. MR-7: the split is an operating choice and the compressor rating a declared purchase; no quantity became an installed capacity or was derived from demand (design review r2 PASS; implementation review PASS, MR-7 compliant on executed evidence).

## 9. Independent reviews

| Review | Verdict | File |
|---|---|---|
| Source check of the reference-case contract (r1, r2, r3) | FINDINGS → FINDINGS → PASS; Q1 confirmed and strengthened | `evidence/source-check-review.md` |
| Materiality budget | accepted (within the source-check r3) | `evidence/materiality-budget.md` |
| Round-1 review (study reading, dispositions, learnings) | FINDINGS, none blocking; corrections applied | `evidence/round1-review.md` |
| WI-092 design review (MR-7) | r1 FINDINGS → r2 PASS | `evidence/design-review.md` |
| WI-092 implementation review (executed behaviour) | PASS, four notes, MR-7 compliant | `evidence/implementation-review.md` |
| Unmet-heat tolerance declaration | PASS, five notes | `evidence/unmet-tolerance-review.md` |
| Round-2 review | see the trail (round result and review) | `evidence/round2-review.md` |

## 10. Stellaris preservation

The entry preservation manifest (`evidence/preservation-entry.json`, 18,725 protected files at `96914299`) passes at entry, after preparation, after the WI-092 increment, after the round-2 study and at delivery (`preservation-entry-check.json`, `preservation-check-t004-prep.json`, `preservation-check-wi092.json`, `preservation-check-t004-r2.json`, `preservation-check-delivery.json`). The documented fixed-design Stellaris diagnostic baseline replays exactly in isolation at entry, after the increment and at delivery (`entry-stellaris-regression-receipt.json`, `wi092-stellaris-regression-receipt.json`, `delivery-stellaris-regression-receipt.json`: 1,352 outputs and 68 responses, original package byte-preserved). Prior ARIES evidence is frozen: the round-1 record (`dae3a465…`) and every earlier sealed study are untouched, and the live assembly evolved only through WI-092.

## 11. Exact replay instructions

All commands from the repository root through the prescribed launcher.

```bash
# Identity: the sealed round-2 study at commit 352ecee4 (record text completed at b6d24a64)
git show 352ecee4 --stat | head
sha256sum exploration/aries_integrated/studies/20260925-aries-revised-reference-network/snapshot.json   # c6551b71…

# Re-verify every stored point of the sealed store against the package-owned oracle
.codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1 python -m scripts.study.verify --package exploration/aries_integrated/aries_integrated --manifest exploration/aries_integrated/studies/20260925-aries-revised-reference-network/manifest.json --identity exploration/aries_integrated/studies/20260925-aries-revised-reference-network/preparation/package_identity.json --store exploration/aries_integrated/studies/20260925-aries-revised-reference-network/results/native/20260925-aries-revised-reference-network.db --sample-size 27 --out /tmp/reverify.json'

# Re-execute the 27 declared points into a fresh record (copy config.json and canonical-replay-receipt.json to a new record directory <NEW> with study_id changed accordingly)
.codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1 python -m exploration.aries_integrated.studies.revised_reference_support prepare --record <NEW> --config <NEW>/config.json'
.codex-test/run bash -c '... revised_reference_support baseline --record <NEW>'
.codex-test/run bash -c '... python scripts/study/preflight.py gates --package exploration/aries_integrated/aries_integrated --manifest <NEW>/manifest.json --groups <NEW>/axes.json --identity <NEW>/preparation/package_identity.json --baseline-result <NEW>/preparation/baseline_result.json --out <NEW>/preparation/preflight_results.json'
.codex-test/run bash -c '... revised_reference_support execute --record <NEW> --integration-return work/orchestration/goals/aries-reference-heat-electricity-reconciliation/evidence/integration-attempt2/integration_return.json'

# Integration seam (CANDIDATE on the re-pinned identity)
.codex-test/run python work/orchestration/goals/aries-reference-heat-electricity-reconciliation/evidence/integrate.py --out-dir /tmp/seam

# Stellaris baseline in isolation and the entry preservation manifest
.codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" python work/orchestration/goals/aries-reference-heat-electricity-reconciliation/evidence/stellaris-regression-delivery.py'
.codex-test/run python work/orchestration/goals/aries-reference-heat-electricity-reconciliation/evidence/check-preservation.py --output /tmp/preservation.json
```

The seam and the study commands must run under the launcher's own environment (no outer `PYTHONPATH`), as the trail's T-003 return records.

## 12. Plain-language explanation for the write-up

The model was handed the published ARIES fusion power and asked to work out how much electricity comes out. At first it said about 800 MW instead of the published 1000, and it also reported that it could not get all the heat out of the reactor. Investigating that turned up two different problems. The first was a plumbing mistake in the model: it had the three heat exchangers in a line, so the hot lithium-lead loop was trying to hand its heat to helium that was already hot, and could not. The published plant puts two of those exchangers side by side instead. Fixing the model to match the published layout removed most of the trapped heat. The second problem was that, with the published high-performance recuperator, the helium coming back to the reactor is already so warm that the blanket's own helium loop cannot heat it any further at the flow rate we assumed. Pushing more helium around the cycle fixes that, but it needs a bigger compressor than we assumed, and the papers do not say which choice ARIES made. With the plumbing fixed and the compressor enlarged, every heat balance and equipment check in the model passes and the plant makes about 891 MW net. The last 109 MW is not something the model can close: the published 43% efficiency needs turbine inlet gas at 708 °C, and the published exchanger duties and temperatures cannot produce that in the published arrangement. So the published figure is best read as a systems-code assumption rather than a result of the described hardware. That is a well-supported disagreement, not an unexplained one.

## 13. Owner gates and next actions

- **Q1** (reserved): decide whether to pursue source evidence on the actual ARIES cycle arrangement through the research route, or accept the published 43% as a systems assumption in the write-up.
- **Resized-compressor alternative** (reserved): whether the 1700 kg/s / 1700 MW case may stand as the named revised reference case for later cost work; its purpose and changed hardware are explicit in the record.
- **Wording notes on the sealed package** (deferred): the completion docstring and calc-def doc comment say "line for line" where "equation for equation, bit-exact on replay" is accurate; scheduled for the next package edit (`work/active/WI-092_aries-parallel-exchanger-network/evidence/implementation-review-notes.md`).
- WI-092 remains registered `backlog` in `work/BACKLOG.md` (no activate operation exists); its close is the owner's through `pm close-item`.
