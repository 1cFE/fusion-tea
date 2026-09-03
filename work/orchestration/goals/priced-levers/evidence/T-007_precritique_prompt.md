# Spawn prompt — pre-execution framing critique, study `20260903-priced-levers`

Deposited before the critique session ran (round-2 review constraint 6: every gate session's
spawn prompt is deposited as evidence). The critique session is a fresh non-author session.

## The prompt given

You are a fresh non-author session performing the **pre-execution framing critique** for a
parameter study in /home/reid/1cfe/fusion-tea, per `.claude/skills/run-study/runbook.md`
step 4. No point has run yet. Your verdict and findings must land before execution.

Read, in this order:
1. `.claude/skills/run-study/runbook.md` and `modeling_project/STUDY_POLICY.md` — the rules.
2. `exploration/stellarator_e2e/studies/ANNEX.md` — the package's own facts.
3. `exploration/stellarator_e2e/studies/20260903-priced-levers/` — `axes.json`, `scan.py`,
   `study.py`, `results/window_scan.json`. This is the study under critique.
4. `work/orchestration/goals/priced-levers/goal.md` and `evidence/R1_deadlock_recount.md` —
   why this study exists and what it was pre-registered to expect.
5. For comparison, the predecessor: `exploration/stellarator_e2e/studies/20260901-sustainment-fence/record.md`
   and `synthesis.md`.

CLEAN ROOM: read `knowledge/holdout/aries-cs/PROTOCOL.md` §§1-3 first and obey it. Do not
open anything under `knowledge/holdout/`, `exploration/concept_analysis/analyses/09-qi-stellarator-hts/`,
or the barred sources §3 names.

## What to critique

- **Are the axes legitimately declared?** Complete entry-key groups, ties declared not
  derived, nothing swept as a subset of a group.
- **Is each framing (`search` vs `sensitivity`) right** for what the arm can actually show?
- **Are the windows honestly fixed from the scan**, and is `engineered` the right provenance?
- **Is the p=50 arm empty by construction?** The executor pre-registered that it expects zero
  feasible points there. Say plainly whether running an arm whose answer is pre-registered as
  empty is worth the points, or whether it should be reshaped. The predecessor study's critique
  made exactly this call in the opposite direction and it changed that study.
- **Is holding `magnet__B_max` defensible?** The executor's argument: WI-036 priced the winding
  pack but gave the conductor GRADE no cost consequence, so sweeping B_max would manufacture
  feasible points that cost nothing. Attack that if it is wrong.
- **Is holding `sigma_allow` defensible**, given the goal's own T-002 research found the
  applicable allowable depends on stress category?
- **What is missing?** Anything the arms cannot answer that the record will be read as
  answering. Density and temperature coverage. Sensitivities not run.
- **Anything the executor is fooling itself about.**

## Return

A verdict — `CLEAN`, `MINOR`, or `MAJOR` — and a numbered finding list, each finding with a
concrete recommended disposition. Be adversarial: this study's author expects a particular
answer, and your job is to find where that expectation has shaped the design.
