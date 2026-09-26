# Review brief: round 2 of goal `design-study-parameters` (fresh, bounded)

You are a fresh reviewer with no prior context. Read only the files named here; do not read the goal's other evidence, other goals, the runbook or prior reviews beyond what is named; do not run anything; do not delegate. Budget: about ten tool calls and a 450-word return. If named evidence is missing or the budget cannot establish coverage, return the specific missing evidence and your uncertainty without a passing verdict. Return PASS, FINDINGS (each marked `correct-before-close` or `note`) or OWNER_GATE.

## The question

After a round-1 review and an owner ruling, a goal round sealed its study and revised its answer on four owner directions. Check the revised answer against the sealed record and the owner's directions. Five questions:

1. **Directions applied.** Read `evidence/owner-ruling-g001.md` (the owner's four numbered directions and the factual correction) and `answer.md`. Is each direction applied in substance: (1) the tolerance treated as a verification tolerance only, with re-verification and a seal; (2) the conclusion stated as "operating choices improve performance with existing equipment; exchanger capacity limits further improvement" and no longer as "hardware, not operation, is the lever"; (3) electricity and the nonfuel cost contribution leading, with the tritium term identified as the assumed price spread over more electricity, and the exchanger's "74 MW" priced as an added capital contribution, not a total cost of electricity; (4) the helium return condition resolved as deliberately permitted or missing, with the leading cases checked; (5) the 426.6 MW starting case kept distinct from the 423 MW ARIES nominal?
2. **Numbers.** Compare the answer's § 2 table (net, Δnet, unmet, nonfuel LCOE, tritium term, total, return residual) against `…/20260926-design-study-parameters/results/readout.md` § 2, § 6 and `evidence/return-condition-check.md`. Check at least ten numbers. Nonfuel LCOE = total − tritium − deuterium − supply; the readout calls it "plant-side".
3. **Return condition.** Read `evidence/return-condition-check.md` and the record's addendum in `…/20260926-design-study-parameters/record.md` (the end of the file). Does the answer's § 4 state the condition, its source and its status (missing as a check) as the check file does, and are the residuals and bypass-equivalent fractions quoted correctly? Is the claim "residual equals the hot-bound margin wherever all heat is removed" stated as the check found it (163 of 163)?
4. **Seal.** Does the record addendum state a passing re-verification on all 272 points under a verification manifest that is the executed manifest plus the three ruled classes only, with the snapshot digest, and does `snapshot.json` exist with that digest (compute `sha256sum` mentally is not required: check the addendum's stated digest against `trail.md`'s T-006 return)?
5. **Scope.** Read `trail.md` from `## Round 2` to the end. Did T-006, T-007 and T-008 stay inside their scopes (no edit to committed `results/` files other than additions, no package or model change, the live manifest gaining only the three classes)?

## Entry files

- `work/orchestration/goals/design-study-parameters/{answer.md, candidate-ledger.md, proposed-passage.md, trail.md (from "## Round 2"), evidence/owner-ruling-g001.md, evidence/return-condition-check.md}`
- `exploration/costed_loop_brayton/studies/20260926-design-study-parameters/{record.md (§ 13 and the addendum at the end), results/readout.md (§ 2, § 6), snapshot.json (existence and the "study_id" field only)}`

## Exclusions

Do not evaluate the physics beyond the record's and the check's own statements; do not re-verify the package; do not read the owner brief, round 1 of the trail or earlier reviews; do not propose new studies.
