# Review brief: round 1 of goal `design-study-parameters` (fresh, bounded)

You are a fresh reviewer with no prior context. Read only the files named here; do not read the goal's other evidence, other goals, the runbook or prior reviews beyond what is named; do not run anything; do not delegate. Budget: about ten tool calls and a 450-word return. If named evidence is missing or the budget cannot establish coverage, return the specific missing evidence and your uncertainty without a passing verdict. Return PASS, FINDINGS (each marked `correct-before-close` or `note`) or OWNER_GATE.

## The question

A goal round ran one study on a costed plant assembly and wrote an answer. Check that the answer's claims are the record's stored numbers, that the round stayed inside its declared scopes, that every discovery-log row it touched has its disposition, and that the proposed learnings follow from the evidence. Five questions:

1. **Numbers.** Open `answer.md` § 2–§ 4 and `…/20260926-design-study-parameters/results/readout.md` § 2, § 3, § 5 and § 6. Do the answer's net, unmet-heat, LCOE and delta figures for the starting point, the two best-passing points, the screen's best (2,500 / 1.45), the electricity-only best (2,500 / 1.425) and the S6 point (2,500 / 1.40 at 75,000 m²) equal the readout's? Check at least eight numbers yourself.
2. **The limiting check.** Does the answer's statement that heat removal bounds the passing band below and the compressor rating bounds it above at 2,250–3,000 kg/s follow from `record.md` § 4 and § 6 (the per-flow bands in `readout.md` § 3)? Is the "ridge one grid step on the failing side" claim supported at every flow in that table?
3. **Owner gate.** Read `evidence/owner-gate-verification-class.md` and `record.md` § 13. Is the refusal described accurately (one channel, one case, 1.466e-9 relative, 5.3e-10 K absolute, no declared class), is the contract's rule (`evidence/comparison-contract.md` § 9, § 12) applied as written (no class added after the result), and is the seal correctly parked rather than claimed?
4. **Scope and dispositions.** Read `trail.md` from `### T-005 scope` to the end. Did T-005 stay inside its scope (new files only under the record directory, the discovery log rows, goal evidence; no package, manifest or library change)? Do the eight rows appended to `exploration/costed_loop_brayton/studies/DISCOVERY_LOG.md` each have a home that matches `record.md` § 15? Was the `flow_ratio_config.py` / `study_support.py` revision before execution (the extra anchor) recorded in the checkpoint and declared in `axis-plan.json`?
5. **Learnings.** Read `evidence/round1-learnings-proposed.md`. Does each proposed learning follow from the record and the readout? Mark any that overreach.

## Entry files

- `work/orchestration/goals/design-study-parameters/{answer.md, candidate-ledger.md, trail.md (from "### T-005 scope"), evidence/owner-gate-verification-class.md, evidence/round1-learnings-proposed.md, evidence/comparison-contract.md (§ 6, § 9, § 12)}`
- `exploration/costed_loop_brayton/studies/20260926-design-study-parameters/{record.md, results/readout.md, axis-plan.json (the "anchors" and "refused_by_oracle_scan" keys)}`
- `exploration/costed_loop_brayton/studies/DISCOVERY_LOG.md`

## Exclusions

Do not evaluate the physics or the economics beyond the record's own statements; do not re-verify the package; do not read the owner brief or the goal's earlier tasks; do not propose new studies.
