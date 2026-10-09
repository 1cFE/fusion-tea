# Stellarator demo catch-up — 2026-10-04

[AGENT] Read-only catch-up from local records and live GitHub PR metadata. No tests or studies rerun. Current checkout: `goal/magnet-material-comparison`, HEAD `97fabad31`, nine commits ahead of its tracked remote. Untracked artifacts include the Round 2 plant-map study and three integration receipt directories.

## Shipping

GitHub confirms PR #112 merged on 2026-09-28 (demo, ARIES hold-out experiment and write-ups); PR #115 merged on 2026-09-30 (write-up updates and magnet material goal). PR #113 cleanup also merged. The nine local continuation commits are not included in the merged remote branch tip; no new PR for them appears in the latest PR listing.

## Latest evidence

Round 1's sealed magnet subsystem answer is in `work/orchestration/goals/magnet-material-comparison/answer.md`: Nb₃Sn is cheaper at matched supported duty under the declared reference prices; REBCO's refrigeration savings do not offset its tape cost. Round 2 expands the question to whole-plant LCOE over explicit confinement and geometry assumptions.

The committed trail ends at T-017's initial Nb₃Sn numerical verification refusal and the r5a tolerance correction. The untracked `exploration/stellarator_materials/studies/20260930-magnet-material-plant-map/record.md` reports all 2,921 cases executed, 2,917 evaluated and four matching domain refusals; 4,150,085 scalar comparisons with zero disagreements and all 73 verdicts per evaluated case matching. All three integration units report ten-gate CANDIDATE returns. These are deposited executor results, not a completed goal answer or independently reviewed final round. The snapshot SHA remains `@@SNAPSHOT_SHA@@`; goal interpretation, evidence labels, figures and interaction analysis are absent.

The deposit reports lower Nb₃Sn LCOE in all eight comparable assumption cells at 80 USD/m REBCO tape, with break-even prices 5.7–37.7 USD/m. The anchored f_ren=1.0 cell has no supported Nb₃Sn design. “Supported” excludes the open breeding and divertor checks; every evaluated design fails breeding. These are conditional study results, not plant qualification.

Recorded focused checks: material implementation 29 passed, oracle 23 passed, model-family spine 15 passed, offer policy 13 passed. Reference preservation reproduces 1,352 outputs and 67 verdicts bit for bit. Earlier parameter and exchanger studies retain complete fresh replay evidence (272-point verification plus the 22-point return-control continuation; 1,277 exchanger cases respectively).

## Remaining work

[AGENT] Immediate continuation is to reconcile T-017's deposited result with the goal trail, resolve and verify the snapshot, obtain required independent review, and produce the Round 2 answer, figures and evidence-labelled assumption map. Formal closure remains owner-held under the goal contract.

Other recent design goals (parameters, combinations, component alternatives, exchanger architecture and whole-plant conversion) are formally closed; WI-096/WI-097 and other implementation items still have administrative closure outstanding. Older goal headers and `work/BACKLOG.md` are stale and cannot be read as an ordered execution queue. Some technically completed magnet goals await owner closure. Magnet-coil-realism is parked on missing inventory inputs; fusion-audit-remediation ended at an OWNER_GATE after its authorized round limit. No clearly ordered next modeling goal after the material comparison was found.
