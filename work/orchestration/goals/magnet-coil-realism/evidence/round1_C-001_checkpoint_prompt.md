# Spawn prompt — round 1 pre-execution disposition checkpoint C-001 (fresh, non-author)

Deposited 2026-09-14 before spawning, after the record's commit (`8ad7e913`, Addendum `e44d5e5f`), the administrator's synthesis (`8056ef20`) and the round agent's proposed dispositions (`7bf9b387`). Agent type: `general-purpose`, fresh (never a fork). Goal `magnet-coil-realism`, round 1, task T-003. This discharges `work/orchestration/GOAL_RUNBOOK.md` § The pre-execution disposition checkpoint: a fresh non-author reads the study reading and the proposed dispositions before any semantic follow-up executes, and returns `PASS` or `REVISE` (revision cap 2).

---

You are the **disposition checkpoint** for goal `magnet-coil-realism` round 1 in `/home/reid/1cfe/fusion-tea` (branch `feat/integrated`). A study has been executed and committed; a fresh administrator wrote an independent synthesis; the executor appended an Addendum answering it; the round agent wrote a reading and proposed how every finding and every touched older discovery row is dispositioned. You did none of that. Your job is to say whether the reading is what the evidence supports and whether each proposed disposition is the right one — before anything downstream is acted on.

## What to read, in this order

1. `work/orchestration/GOAL_RUNBOOK.md` § The pre-execution disposition checkpoint and § The discovery log (the rules you enforce).
2. `work/orchestration/goals/magnet-coil-realism/goal.md` (§ Question, § What the model does today, § Answered when, § Invariants, § Limits, § Reserved gates) and `trail.md` (§ Round 1 strategy revision; § T-001, § T-002 returns; § T-003 scope).
3. `work/orchestration/goals/magnet-coil-realism/evidence/T-003_proposed_dispositions.md` — the reading, the proposed dispositions for `20260914-magnet-coil-realism#1`–`#6`, the proposed joined rows for the five older ids, and the proposed learning delta: the object of your review.
4. `exploration/stellarator_e2e/studies/20260914-magnet-coil-realism/record.md` (all of it, the `## Addendum 2026-09-14` included; §§ 3, 4, 6, 10, 13, 15, 17 closely) and `synthesis.md` (§ 7 "What the record does not support" and P-1 to P-4). For your own recount use `results/points.csv`, `results/comparison-transects.json`, `results/comparison-matched-window.json`, `results/a-minima.json`, `results/R-invariance.json`, `results/oracle-all-points.json` and `preparation/before-*` — check the record's numbers against them rather than trusting either the record or the synthesis.
5. The rows the proposed dispositions touch in `exploration/stellarator_e2e/studies/DISCOVERY_LOG.md`: every row under `20260904-wall-and-heating#3`, `20260907-minor-radius#2`, `20260913-magnet-design-transfer#2`, `#3`, `20260903-priced-levers#2`, and this record's own `20260914-magnet-coil-realism#1`–`#6` first-sighting rows.
6. `work/active/WI-058_coil-winding-length-from-bore/design.md` § Research findings and § Off-design predictions, and `audit.md` (verdict and F1), for what the increment claims and what its audit corrected; `work/orchestration/goals/minor-radius/learnings.md` L-002 and L-003 (the claims the reading says stand).
7. The predecessor checkpoints as the form: `work/orchestration/goals/minor-radius/evidence/round1_C-001_checkpoint.md` and `_r2.md`, and that goal's `trail.md` § Checkpoint C-001.r1 / r2.

## What to check

- **Does the reading say what `results/` supports, in the record's own bases?** Every count states its verdict set and its sense of "feasible" (the 18-verdict claim); the `a`-minimum is called a price reading over infeasible points where it is one; the flips are stated by constraint and direction (the record says zero — verify); the before/after on the transects is against the oracle-side entering-pin reference and on the matched window against the committed package-level record, and the reading keeps those two bases apart; the plant-closure anchors are a reference at a different package, never an attribution to WI-058; the physics identity (the bore ratio `(a + 1.85) / 3.15`) is stated as measured; a "bounded negative" is called that.
- **Is each proposed disposition the right class** (`model fix`, `declared seam`, `research`, `upstream filing`, `none owed`, `captured`, `closed`, `discharged`), **the right home, and the right responsible party**, and does it follow from the row's evidence rather than from the goal's wish? A row touched by this record's evidence must get a joined row; a row it did not touch must not (judge `20260903-priced-levers#2` on that rule). Watch the `closed` / `discharged` / `discharged in part` distinction. Watch `#1`: it is a premise conflict the goal contract itself created (the invariant against the question); the proposed disposition is an owner-held amendment — say whether surfacing it as an owner gate with the proposed text is the right handling, and whether anything in the reading silently resolved it.
- **The proposed learning delta L-001–L-004**: does each claim follow from the record's evidence and not beyond it (L-002's "$371M artefact at R 15.7" and its "any committed reading … carries that artefact" clause; L-001's reading of the minor-radius L-002)? A learning is accepted only by the round review, not here — your job is to say whether the delta is honestly derived.
- **The Addendum**: does it correct every item the synthesis raised, from `results/`, without editing frozen text or claiming more than the directory supports?
- **Anything the administrator flagged that the round agent's reading did not carry.**

## Rules

- `uv run python` only (never bare `python`, `python3`, `pip`). **Never read anything under `knowledge/holdout/`.** Do not edit any repository file. Do not run the study. Do not commit. Write only under `/tmp/claude-1000/-home-reid-1cfe-fusion-tea/3a754c07-eb6e-407f-8afd-246f4e8140e4/scratchpad/checkpoint_magnet_coil_realism/` and `work/orchestration/goals/magnet-coil-realism/evidence/round1_C-001_checkpoint.md` (your checkpoint, the one repository file you write; uncommitted).

## Return

A verdict of **PASS** or **REVISE**, then a numbered list of findings, each with: what is wrong or right, the evidence (path and, for a number, the recount), what the round agent must change (for REVISE), and your confidence. Write the full checkpoint to `work/orchestration/goals/magnet-coil-realism/evidence/round1_C-001_checkpoint.md` and return a summary.
