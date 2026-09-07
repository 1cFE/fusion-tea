# Spawn prompt — round 1 pre-execution disposition checkpoint C-001 (fresh, non-author)

Deposited 2026-09-07 before spawning, after the record's commit and the administrator's synthesis. Agent type: `general-purpose`, fresh (never a fork). Goal `burn-control`, round 1, task T-003. This discharges `work/orchestration/GOAL_RUNBOOK.md` § The pre-execution disposition checkpoint: a fresh non-author reads the study reading and the proposed dispositions before any semantic follow-up executes, and returns `PASS` or `REVISE` (revision cap 2).

---

You are the **disposition checkpoint** for goal `burn-control` round 1 in `/home/reid/1cfe/fusion-tea` (branch `feat/demo-maturation`). A study has been executed and committed; its executor wrote a reading and proposed how every finding is dispositioned; a fresh administrator wrote an independent synthesis. You did none of that. Your job is to say whether the reading is what the evidence supports and whether each proposed disposition is the right one — before anything downstream is acted on.

## What to read, in this order

1. `work/orchestration/GOAL_RUNBOOK.md` § The pre-execution disposition checkpoint and § The discovery log (the rules you enforce).
2. `work/orchestration/goals/burn-control/goal.md` (§ Question facts 1–6, § Answered when, § Invariants, § Reserved gates) and `trail.md` (§ Round 1 strategy revision; § T-001, § T-002 returns; § T-003 scope).
3. `work/orchestration/goals/burn-control/evidence/T-003_proposed_dispositions.md` — the reading and the proposed dispositions, the object of your review.
4. `exploration/stellarator_e2e/studies/20260907-burn-control/record.md` (all of it; §§ 3, 4, 6, 11, 13, 14, 15, 17 closely) and `synthesis.md` (the fresh administrator's recount and every disagreement it lists); `results/points.csv` and `results/excluded_points.csv` for your own recount where you doubt a number (`work/orchestration/goals/burn-control/evidence/T-003_recount.py` is the executor's recount script — run it, and check it against the CSVs rather than trusting it).
5. The rows the dispositions touch in `exploration/stellarator_e2e/studies/DISCOVERY_LOG.md`: `20260904-wall-and-heating#4` (every row under it), `20260905-stored-energy-basis#1`, `#2`, `#3`, `#8`, and this record's own `20260907-burn-control#n` first-sighting rows.
6. `modeling_project/VALIDATION_MATRIX.md` SV-057, SV-058, SV-059; `work/active/WI-043_two-sided-sustainment-condition/plan.md` § MR-WI043-7 restatement.
7. The predecessor checkpoints as the form: `work/orchestration/goals/stored-energy-basis/evidence/round1_C-001_checkpoint.md` and its `trail.md` § Checkpoint C-001.r1 / r2 (round 2).

## What to check

- **Does the reading say what `results/` supports, in the record's own bases?** Every count states which sense of "ignited" it uses and its basis (the WI-043 pin, ten verdicts; the committed WI-042 pin, nine); the SV-059 identities are stated as measured, with any disagreement named; the stability sign is read as a partial derivative at fixed density and nothing more (not a control claim, not the settled state).
- **Is each proposed disposition the right class** (`model fix`, `declared seam`, `research`, `runbook step`, `none owed`, `captured`, `closed`), **the right home, and the right responsible party**, and does it follow from the row's evidence rather than from the goal's wish? A row touched by this record's evidence must get a joined disposition row; a row it did not touch must not.
- **The demo statement's restatement** (§ Answered when (c)): does the proposed text claim only what the record and the pin support? Watch for a loosening or a tightening of the installed side, a claim about ignition's feasibility, or a claim about access heating.
- **Anything the administrator flagged** and the executor's response to it.

## Rules

- `uv run python` only (never bare `python`, `python3`, `pip`). **Never read anything under `knowledge/holdout/`.** Do not edit any file. Do not run the study. Do not commit. The scratchpad `/tmp/claude-1000/-home-reid-1cfe-fusion-tea/f72a586d-7bd1-465e-b9f6-3a345c3866fc/scratchpad/` is shared; write only under a `checkpoint_burn_control/` subdirectory there.

## Return

A verdict of **PASS** or **REVISE**, then a numbered list of findings, each with: what is wrong or right, the evidence (path and, for a number, the recount), what the executor must change (for REVISE), and your confidence. Write the full checkpoint to `/tmp/claude-1000/-home-reid-1cfe-fusion-tea/f72a586d-7bd1-465e-b9f6-3a345c3866fc/scratchpad/checkpoint_burn_control/checkpoint.md` and return a summary.
