# Round 3 execution-failure and repair scope review

2026-09-27. [AGENT] Continuing independent reviewer. Reused the source, design, protocol and WI-097 implementation reviews. This review initially addresses goal disposition; the numerical remedy requires a separate narrow recheck below once its evidence is ready.

## Goal disposition

**PASS: close Round 3 at PREREQUISITE and use Round 4 for a reviewed numerical repair and exact candidate replay.** I checked the attempted study's `results/cases.json`: it contains 1277 supplied cases, with 1275 completed and exactly two `execution_failed` rows, `c0621` and `c1085`. Both retain the original executable fingerprint and exact input-map equality, with no evidence digest or engineering verdict. The reported error is “bypass solve did not converge.” A solver exception is an execution failure, not a thermal inadequacy verdict or a basis for silently excluding a candidate from the comparison.

The goal limits each round to one promoted pin and one committed study. Round 3 already promoted the controlled package and attempted the study against it. Preserve that package identity, attempted study, original candidate maps, failure traces and verification state. Do not replace its executable in place or label a changed-pin replay as an unchanged mechanical retry. Record the unmet execution prerequisite and leave architecture ranking unaccepted.

The fourth round is the final available round under the goal's recorded limit. A bounded numerical evaluation repair is within the owner's delegated judgment when it preserves the thermal equations, physical requirement thresholds, selected inventory, prices, operating choices and independent oracle. It does not require a new owner gate merely because the two failures were not exposed by development controls. Any change to physical meaning or verification tolerances must be surfaced and reviewed before dependent results proceed.

## Repair boundary

- Reproduce both exact failed input maps and retain their original exception traces before editing the native evaluator.
- State the numerical cause and stable algebra or solve correction. Demonstrate that it evaluates the accepted equations, including their capacity-equality limits, rather than relaxing the engineering requirements or hiding finite-transfer states.
- Add focused regressions for both failures and relevant neighboring/equality cases. Reuse the unchanged independent oracle and declared comparison tolerances. Preserve existing legacy behavior and fixed equipment/accounting invariants.
- Promote one reviewed repaired pin in Round 4, then replay the same 1277 candidate maps with explicit identity correspondence. Record any genuinely non-evaluable point rather than replacing it with a new candidate or a favorable verdict.
- Require complete native execution classification and independent numerical verification before comparing architectures. Retain the existing refinement, paired-acceptance, omitted-cost and uncertainty obligations. If the final round cannot meet them, report the bounded result and unmet criteria; do not imply the goal is complete.

Formal work-item and goal closure remain owner-held. The coordinator may close the failed round and open the authorized final repair round. Numerical-remedy approval is pending the author's bounded proposal and independent failure evidence.
