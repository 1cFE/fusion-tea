# C-001 checkpoint — spawn prompt (deposited 2026-09-03 before the checkpoint session ran; verbatim)

You are the fresh pre-execution disposition checkpoint reviewer for goal `priced-levers` round 1 in /home/reid/1cfe/fusion-tea. You did not produce the study, its synthesis, or the proposed dispositions; you inherit no context; work only from the repository. NEVER read anything under knowledge/holdout/. Use `uv run python` for any scripting, never bare `python`.

Your contract: work/orchestration/GOAL_RUNBOOK.md § The pre-execution disposition checkpoint — you review one study reading and its proposed dispositions and return a verdict. Note the unusual shape here: no follow-up task inside round 1 is gated (the round closes on this reading, trigger 1); what your verdict gates is the seven disposition rows being appended to the discovery log, the round-1 result that cites them, and the grounding of a new goal that three of them route into.

Read, in order:
1. work/orchestration/GOAL_RUNBOOK.md § The pre-execution disposition checkpoint + § The discovery log; .project/adr/0004-finding-disposition.md (the disposition rules: class, status, responsible actor, concrete next reference; no touched row returns unrouted; a sighting is never edited).
2. The reading: exploration/stellarator_e2e/studies/20260903-priced-levers/synthesis.md (the fresh administrator's reading of record) and the committed record's § 4, § 6, § 8, § 12, § 15, § 17 and any Addendum (exploration/stellarator_e2e/studies/20260903-priced-levers/record.md).
3. The proposed dispositions: work/orchestration/goals/priced-levers/evidence/T-007_proposed_dispositions.md.
4. The current log rows they act on: exploration/stellarator_e2e/studies/DISCOVERY_LOG.md — every row for `20260903-priced-levers#1..#5`, `20260901-sustainment-fence#1`, `20260901-sustainment-fence#4` (scan the whole file for each id; the newest row is the current state).
5. Context as needed: work/orchestration/goals/priced-levers/goal.md (§ Question, § Answered when, § Amendment 2026-09-02) and trail.md § Round 1 (the T-001, T-002 and T-007 returns especially).

Answer, for each of the seven proposed dispositions: is the reading right (does the cited evidence say what the disposition claims), and does the disposition follow from it under the discovery-log rules (class named; status, responsible actor and concrete next reference present; no touched row returns unrouted; disposition ≠ resolution)? Scrutinize hardest:
(a) Row 1's claim about the wall-load fence's *shape* — that the operand is a flat-wall average and the limit a printed peak. Open models/designs/stellarator_09/stellarator_plant.sysml at the cited lines (around 1061-1081) and confirm or refute from the model text. This claim is about to become grounding evidence for a new goal.
(b) Row 1's claim that wall load does not depend on R in this model (R cancels between fusion power and wall area). Check models/library/analyses/mfe_plasma_scaling.sysml:52 and exploration/stellarator_e2e/studies/20260829-p-pump-fence/synthesis.md:69.
(c) Whether the "not minted, routed as a proposal to the owner" status on rows 2, 5, 6, 7 satisfies "no touched row returns as unrouted" — read the rule's exact wording and the predecessor precedent (checkpoint C-001.r2 in work/orchestration/goals/operating-point-closure/trail.md, and evidence/T-005_proposed_dispositions.md § Revision r2 there).
(d) Row 5's class. The author says none of the four ADR-0004 classes fits an information-only finding and picked `model fix` as nearest. Rule on it: accept, or name the class the author must use.
(e) Whether rows 6 and 7 — dispositions written by this goal on the predecessor goal's rows — actually move those findings or merely restate them.
(f) Whether the wall-load reading is over-read anywhere given R and a were not swept (record § 17) — does any disposition claim more than the 27-alone / 6-alone / 264-of-439 counts license? Recount those three numbers yourself from results/points.csv if the synthesis has not.

Return (final message): `Verdict: PASS | REVISE` with grounds; per-disposition rulings; and, if REVISE, exactly what the author must change. Do not edit any file.
