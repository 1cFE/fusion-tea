# Brief: audit "Quality Tools and Era Adapter Promotion" (RUN-STUDY Item 4)

Audit the completed implementation against `.project/active/run-study-quality-tools/`
(spec.md, design.md rev 2, plan.md 9 phases with notes). Deliverables:
scripts/study/{identity,common,preflight,verify}.py, four new schema files,
exploration/stellarator_e2e/studies/{era_adapter,oracle_entry,promotion_equivalence}.py,
ANNEX.md, the manifest oracle-block value edit, tests.

The orchestrator already re-ran the full suite independently: 272 passed +1 slow
(948-point byte-equality, 130s) under STUDY_REQUIRE_ERA=1; generic modules grep-clean.
Do not repeat the slow test; run the fast suite once yourself.

Standard audit (plan-vs-reality, TODOs, silent gaps, invariant violations), plus:
1. Map all design-rev-2 invariants (1-10 + the extended source-set Invariant 4) to enforcing
   tests; read the test bodies for the load-bearing ones (lineage refusal, accept-set
   negative, read-set coverage of the identity gate).
2. The four recorded deviations + two surfaced findings: each honestly recorded, none a
   silent scope change. Specifically judge: (a) proof-of-life stores refused by verify.py -
   is the recorded treatment right per the epic's temporary-route integrity criterion?
   (b) the p_fus/magnet_capital coverage delta - correctly flagged as an Item 3 manifest
   question rather than absorbed?
3. The annual_om levelized-vs-unlevelized catch: verify the shipped channel map is the
   CORRECT one (against verify_stellaris.py and the package channel), not just documented.
4. ANNEX.md: six sections match the runbook's per-step annex links (runbook.md as amended,
   15 steps); deletion condition stated exactly; era pin recorded with the not-to-chase
   upstream note.
5. era_adapter.py self-checks: dead-filler assertion, era-pin prerequisite, accept-set -
   all fail closed and none asserted by generic tools.
6. The epic's Item 4 success criteria and temporary-route integrity criterion: tick what is
   verified with evidence paths; name anything unmet.
7. The manifest edit: exactly the oracle-block values, nothing else (git show the commit).

Write `.project/active/run-study-quality-tools/audit.md`, verdict PASS / PASS-WITH-FIXES /
FAIL. Do not edit deliverables.
