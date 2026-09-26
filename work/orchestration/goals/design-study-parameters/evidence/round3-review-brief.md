# Review brief: round 3 of goal `design-study-parameters` (fresh, bounded)

You are a fresh reviewer with no prior context. Read only the files named here; do not read the goal's other evidence, other goals, the runbook or prior reviews beyond what is named; do not run anything; do not delegate. Budget: about twelve tool calls and a 450-word return. If named evidence is missing or the budget cannot establish coverage, return the specific missing evidence and your uncertainty without a passing verdict. Return PASS, FINDINGS (each marked `correct-before-close` or `note`) or OWNER_GATE.

## The question

After an owner direction, a goal round added a control model that enforces a loop's return-temperature requirement, ran a second sealed study, and rewrote its answer. Check the revised answer against the two sealed records and the owner's direction. Five questions:

1. **Direction applied.** Read `evidence/owner-direction-round3.md` (four numbered steps and the two conclusions it says went too far) and `answer.md`. Is each step applied in substance: (1) an arrangement chosen and stated; (2) the relationship enforced in the calculation and checks, with no tolerance chosen to admit the residual (check what the answer says the check tolerance is and what the residuals are); (3) the starting configuration and the leading alternatives re-evaluated near the boundary; (4) the comparison recomputed on cases that satisfy the completed model? Are the two overreaching conclusions gone (no "exactly consistent" claim without an executed point; no "without reordering" claim without the enforced requirement)?
2. **Numbers.** Compare the answer's § 2 table and § 6 against `…/20260926-design-study-parameters-b/results/readout.md` § 1–§ 2: net, Δnet, bypass fraction, nonfuel LCOE, tritium term, total LCOE, the matched-exchanger ratios and nets at each flow. Check at least twelve numbers. Nonfuel LCOE = total − tritium − deuterium − supply.
3. **The bypass fractions and the return residuals.** Do the answer's bypass fractions (0.311 at the starting configuration, 0.130 at 2,500 / 1.45, 0.019 at 2,500 / 1.430, 0.039 at the S6 point) and its statement that the residual at every consistent case is of order 1e-11 K match the readout, and does the answer state correctly that round 2's mixing estimates (18.8 %, 6.0 %) were superseded and why?
4. **Seal and identity.** Does `…/20260926-design-study-parameters-b/record.md` § 13 state a passing verification on all 22 points under the record's own manifest with twelve classes declared before execution, and § 16 a snapshot digest; does `snapshot.json` exist with `study_id` `20260926-design-study-parameters-b`? Does § 12 state how the round-1 record's cycle values are licensed on this identity?
5. **Scope and learnings.** Read `trail.md` from `## Round 3` to the end and `evidence/round3-learnings-proposed.md`. Did T-009–T-012 stay inside their scopes (no shared library file edited; one new library file; the WI-094 receipts and the round-1 record untouched)? Does each proposed learning follow from the records? Mark any that overreach.

## Entry files

- `work/orchestration/goals/design-study-parameters/{answer.md, candidate-ledger.md, proposed-passage.md, trail.md (from "## Round 3"), evidence/owner-direction-round3.md, evidence/round3-learnings-proposed.md}`
- `exploration/costed_loop_brayton/studies/20260926-design-study-parameters-b/{record.md, results/readout.md, snapshot.json (existence and "study_id" only)}`
- `work/active/WI-095_loop-return-control/report.md` (the development-case table and the acceptance table only)

## Exclusions

Do not evaluate the physics beyond the records' own statements; do not re-verify the package; do not read the owner brief, rounds 1–2 of the trail or the earlier reviews; do not propose new studies.
