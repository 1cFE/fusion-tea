# Spawn prompt — round 1 pre-execution disposition checkpoint C-001 (fresh, non-author)

Deposited 2026-09-07 before spawning, after the record's commit and the administrator's synthesis. Agent type: `general-purpose`, fresh (never a fork). Goal `minor-radius`, round 1, task T-003. This discharges `work/orchestration/GOAL_RUNBOOK.md` § The pre-execution disposition checkpoint: a fresh non-author reads the study reading and the proposed dispositions before any semantic follow-up executes, and returns `PASS` or `REVISE` (revision cap 2).

---

You are the **disposition checkpoint** for goal `minor-radius` round 1 in `/home/reid/1cfe/fusion-tea` (branch `feat/demo-maturation`). A study has been executed and committed; its executor wrote a reading and proposed how every finding is dispositioned; a fresh administrator wrote an independent synthesis. You did none of that. Your job is to say whether the reading is what the evidence supports and whether each proposed disposition is the right one — before anything downstream is acted on.

## What to read, in this order

1. `work/orchestration/GOAL_RUNBOOK.md` § The pre-execution disposition checkpoint and § The discovery log (the rules you enforce).
2. `work/orchestration/goals/minor-radius/goal.md` (§ Question facts 1–7, § Answered when, § Invariants, § Limits, § Reserved gates) and `trail.md` (§ Round 1 strategy revision; § T-001, § T-002 returns; § T-003 scope and any amendment).
3. `work/orchestration/goals/minor-radius/evidence/T-003_proposed_dispositions.md` — the reading and the proposed dispositions, the object of your review.
4. `exploration/stellarator_e2e/studies/20260907-minor-radius/record.md` (all of it; §§ 3, 4, 6, 11, 13, 14, 15, 17 closely) and `synthesis.md` (the fresh administrator's recount and every disagreement it lists); `results/points.csv`, `results/excluded_points.csv` and `results/window_edges.json` for your own recount where you doubt a number (`work/orchestration/goals/minor-radius/evidence/T-003_recount.py` is the executor's recount script — run it, and check it against the CSVs rather than trusting it).
5. The rows the dispositions touch in `exploration/stellarator_e2e/studies/DISCOVERY_LOG.md`: `20260904-wall-and-heating#2`, `#3` (every row under each), `20260905-stored-energy-basis#2`, `#8`, `20260907-burn-control#3`, and this record's own `20260907-minor-radius#n` first-sighting rows.
6. `modeling_project/VALIDATION_MATRIX.md` SV-060, SV-061, SV-062; `work/active/WI-044_magnet-chain-sees-coil-bore/plan.md` § MR-WI044-11 restatement and § Predictions; `design.md` § Off-design predictions.
7. The predecessor checkpoints as the form: `work/orchestration/goals/burn-control/evidence/round1_C-001_checkpoint.md` and `_r2.md`, and that goal's `trail.md` § Checkpoint C-001.r1 / r2.

## What to check

- **Does the reading say what `results/` supports, in the record's own bases?** Every count states its verdict set and which sense of "feasible" and "ignited" it uses; every geometry claim declares the transport facts and the wall-peak calibration it holds constant; the flips are stated by constraint and direction; the physics identity is stated as measured with any disagreement named; the edge question ("did the optimum's `a` leave 2.2, and if so what moved it") is answered from the executed grid and the transect arm, not from the oracle transects alone; a "bounded negative" is called that.
- **Is each proposed disposition the right class** (`model fix`, `declared seam`, `research`, `runbook step`, `none owed`, `captured`, `closed`, `discharged`), **the right home, and the right responsible party**, and does it follow from the row's evidence rather than from the goal's wish? A row touched by this record's evidence must get a joined disposition row; a row it did not touch must not. Watch the `closed` / `discharged` distinction (`discharged` at the pin, `closed [OWNER]` at the item's archive — the `20260904-wall-and-heating#6` precedent) and the research request's closure as a bounded negative (`#2`, `#8`: does the record's evidence support closing it, or only the grounding's reading?).
- **The demo statement's restatement** (§ Answered when (c)): does the proposed text claim only what the record and the pin support? Watch for a bound on `a` claimed from the fence-catching (the goal's invariant forbids it), for the paper's aspect ratio 9.8 read as a target, for the coil–plasma distance or the transport facts presented as modelled, and for the casing seam (a lower bound) presented as a price.
- **Anything the administrator flagged** and the executor's response to it.

## Rules

- `uv run python` only (never bare `python`, `python3`, `pip`). **Never read anything under `knowledge/holdout/`.** Do not edit any file. Do not run the study. Do not commit. The scratchpad `/tmp/claude-1000/-home-reid-1cfe-fusion-tea/0076b1af-4e84-495f-b624-8caacaaed292/scratchpad/` is shared; write only under a `checkpoint_minor_radius/` subdirectory there, and say in your return what you wrote there.

## Return

A verdict of **PASS** or **REVISE**, then a numbered list of findings, each with: what is wrong or right, the evidence (path and, for a number, the recount), what the executor must change (for REVISE), and your confidence. Write the full checkpoint to `/tmp/claude-1000/-home-reid-1cfe-fusion-tea/0076b1af-4e84-495f-b624-8caacaaed292/scratchpad/checkpoint_minor_radius/checkpoint.md` and return a summary.
