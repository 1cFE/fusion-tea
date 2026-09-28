# Round 1 fresh review — spawn prompt (deposited verbatim; independence is evidence, not attestation)

You are a fresh reviewer for goal round 1 of `work/orchestration/goals/operating-point-closure/` in the repo at `/home/reid/1cfe/fusion-tea`. You did not author any part of this goal, its work item, or its evidence; you inherit no conversation context. Work only from the repository.

Read, in order:
1. `work/orchestration/GOAL_RUNBOOK.md` § The fresh review (your contract), § What "fresh" means, § Opening and closing a round.
2. `work/orchestration/goals/operating-point-closure/goal.md` (the grounded question, invariants, delegation, limits).
3. `work/orchestration/goals/operating-point-closure/trail.md` end to end.
4. `work/orchestration/goals/operating-point-closure/evidence/T-002_prototype/` — NOTES.md, scripts, outputs.
5. The cited native artifacts, by citation — at minimum: `work/active/WI-037_operating-point-closure/spec.md`; the WI-037 row in `work/BACKLOG.md`; SV-041..043 in `modeling_project/VALIDATION_MATRIX.md`; rubric Row 1 in `.project/active/demo-depth-rubric/rubric.md`; the R1.P cell in `.project/active/demo-depth-rubric/grading.md`; discovery row `20260823-magnet-technology-ab#4` in `exploration/stellarator_e2e/studies/DISCOVERY_LOG.md`.

Your checks (runbook § The fresh review): every ref resolves and says what the trail claims; goal and strategy fidelity; every recorded task scope (did T-001/T-002 stay inside?); retry classification (there were none — confirm); every discovery row the evidence touched (#4 — is "no disposition row appended, round landed no change" the correct handling per § The discovery log?); the learning delta L-001..L-003 (accept, correct, or reject each — spot-check the prototype's claims against its own outputs and the cited images/PDF where feasible: you may run `uv run python` on the deposited scripts, read the page images under `knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details/images/`, and the iter-02 raw PDF); constraints carried into the next strategy. Clean-room note: NEVER read anything under `knowledge/holdout/` — the four sealed papers stay sealed.

Verify specifically: (a) the STRATEGY_BLOCKER classification — does the round's own declared abandonment condition genuinely fire on the deposited evidence? (b) the spec/SV-042 tension the round leaves behind: MR-WI037-2 and SV-042 encode the refuted solved-T form; the next round must amend them before implementing — confirm this is recorded nowhere as silently resolved, and carry it as a constraint. (c) the trail's cross-check table against `op_solve_final_output.txt` numbers.

Then, per the runbook: on PASS (or FINDINGS with corrections you can state), you author the next strategy revision (ADR-0002 — the fresh agent authors the next round's strategy). Input: NOTES.md § Consequence proposes forward sustainment (T stays a lever; required sustained heating computed from the validated chain and asserted against installed heating as a power limit; ash + quasi-neutral fuel computed forward from A.5/A.6, retiring n_D0/n_T0/n_He0). Weigh it on the merits against the Row-1 P3 anchor's exact text; you may adopt, amend, or replace it.

Return (as your final message, markdown):
1. `Verdict: PASS | FINDINGS | OWNER_GATE` with one paragraph of grounds.
2. The checks, each with what you actually opened and what you found (cite path:line where it matters).
3. Learning delta: accepted / corrected / rejected, per entry, with corrections stated.
4. Constraints carried forward.
5. If verdict permits: the full `### Strategy revision` block for Round 2 (approach, assumptions, abandonment conditions, intended model increment, intended study question — no future task list).
Do not edit any file. Your text return is the review; the round agent appends it to the trail verbatim-in-substance with your attribution.
