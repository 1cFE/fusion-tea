# Deposited spawn prompt — fresh review of Round 1, goal structural-decomposition (2026-09-13)

You are the fresh reviewer of a closed goal round in the fusion-tea repository at /home/reid/1cfe/fusion-tea. You did not do the round's work. You edit exactly two files, named below. Never read anything under knowledge/holdout/.

Read first: work/orchestration/GOAL_RUNBOOK.md § The fresh review, § When a cited artifact moves, § What "fresh" means; .project/adr/INDEX.md (skim the records the runbook cites). Then the goal directory work/orchestration/goals/structural-decomposition/ in full: goal.md, trail.md (the strategy revision, T-001 through T-004 with their scopes, starts and returns, the checkpoint entries, the Round 1 result), learnings.md, and every file under evidence/.

Check, and write down what you checked:
1. Native evidence by citation: every ref in trail.md resolves and says what the trail claims. Open the cited commits (git show), the work item work/active/WI-057_stellaris-structural-decomposition/ (spec, design, design-review, plan, audit, evidence/), the pin evidence evidence/T-003_pin/, the study record exploration/stellarator_e2e/studies/20260913-structural-decomposition/ (record.md with its Addendum, synthesis.md, snapshot.json, results/), the discovery log rows under 20260913-structural-decomposition#.
2. Goal and strategy fidelity: did the round pursue the strategy it declared, and is the proposed close (trigger 1 and trigger 6) what the evidence supports?
3. Every task scope: did each task stay inside its scope? Name any drift.
4. Retries: were there any, and were they mechanical?
5. Every discovery row the round touched: did its disposition land, and did the finding actually move? Read exploration/stellarator_e2e/studies/DISCOVERY_LOG.md.
6. Did any cited artifact move outside its task? Walk the refs against git log on their paths.
7. The learning delta proposed in the Round 1 result: accept, correct, or reject each item.
8. The constraints to carry into any next strategy, and the reserved gates left for the owner.

Also verify independently, without trusting the trail: the baseline LCOE on the pinned package equals the entering pin's (evidence/T-003_pin/baseline_result.json against goal.md § Invariants); the study's comparison_summary.json says what the Round 1 result says; the branch is feat/model-viz and nothing was pushed.

Write two things. (1) Append to work/orchestration/goals/structural-decomposition/trail.md a section `### Round 1 review — 2026-09-13` with: Reviewer (a fresh non-author general-purpose session from the deposited prompt evidence/round1_review_prompt.md), Verdict (PASS, FINDINGS, or OWNER_GATE), Checks (each of 1–8 with what you found), Recommendation (the owner-held close with what the owner must decide, or the next strategy revision). Append only; edit nothing above. (2) Append the accepted learning delta to work/orchestration/goals/structural-decomposition/learnings.md as L-00N entries, each one line, only what you accepted. Do not commit. Plain language, unwrapped paragraphs. Reply with the verdict line and the count of findings.
