# Spawn prompt — T-004 pre-execution framing critique (fresh, non-author)

Deposited before spawning. Agent type: `general-purpose`, fresh (never a fork — a fork inherits context and is not fresh). Goal `wall-and-heating`, round 1, task T-004. This discharges runbook step 4's obligation: *"submit the framing and the plan to a critique before any point runs, and record that critique's verdict as a named review outcome."*

---

You are the **pre-execution framing critique** for a parameter study in `/home/reid/1cfe/fusion-tea` (branch `feat/demo-maturation`). Nothing has been executed through the sealed package yet. Your job is to find what is wrong with the study **before** 503 points run, when fixing it is still cheap.

You did not design this study and you are not here to approve it. The last critique in this series returned MAJOR with eight findings, two of which reshaped the study entirely — one of them caught a fence conclusion that was an artifact of holding an axis fixed. That is the standard.

## What to read

- `exploration/stellarator_e2e/studies/20260903-wall-and-heating/study.py` — the study definition, its docstring, its three arms, its windows, and its held keys. **Start here.**
- `exploration/stellarator_e2e/studies/20260903-wall-and-heating/axes.json` — the nine declared axes, five swept and four declined, each with its reasoning.
- `exploration/stellarator_e2e/studies/20260903-wall-and-heating/scan.py` and `results/window_scan.json` — the oracle scan the windows were fixed from (6160 candidates, 0 errors).
- `exploration/stellarator_e2e/studies/20260903-wall-and-heating/indicators.json` — what each axis reaches in the module graph.
- `exploration/stellarator_e2e/studies/20260903-wall-and-heating/pre_wi039_indicators.json` — the same measurement on the **pre-change** package, used to support the study's central structural claim.
- `modeling_project/STUDY_POLICY.md` — the rulebook for what a legitimate axis is and what a study may claim.
- `.claude/skills/run-study/runbook.md` — the obligations, especially steps 2, 3, 4, 7 and 11.
- `work/orchestration/goals/wall-and-heating/trail.md` § T-004 scope — the goal-level scope this study must stay inside, including two narrower constraints.
- `work/orchestration/goals/wall-and-heating/goal.md` § Invariants.
- Context for what changed in the model: `work/active/WI-039_heating-system-structure/design.md`.

## What to attack

Be specific and be adversarial. In particular:

1. **Is any conclusion this study will draw an artifact of an axis it holds?** This is the failure mode that bit the predecessor: holding `T_i0` at 14.63 produced a fence conclusion the freed axis contradicted. Check every held key in `study.py`'s `HELD` dict against every claim the docstring says the study will make. `j_wp` and `eta_couple_heat` are the two to look at hardest.
2. **Can each swept axis actually reach the thing the study says it tests?** An axis whose window cannot reach a limit cannot test that limit. The predecessor's density window could not reach the beta limit and was widened on exactly this finding. Check the windows against `results/window_scan.json`.
3. **Is the resolution adequate for the claim?** The `arm-search-p220` band is 14.5–15.0 MA at 0.25 MA steps — is that enough to resolve an optimum, or will it produce a "band" that is really three points?
4. **Is the efficiency-optimum claim sound?** The study says 0.55 may beat 0.60 on LCOE, and builds a transect to resolve it. Is that an artifact of the scan's grid, of held `j_wp`, or of something real? What would make it not real?
5. **Are the declined axes honestly declined?** Four axes are declined. Is each reason a real reason, or is one of them a convenience? Pay attention to `eta_couple_heat`: the argument is that sweeping a stated assumption reads as knowledge the model does not have. Is that right, or is it an excuse not to report a sensitivity that matters?
6. **Does the study overclaim about what the heating chain proved?** The central claim is that source efficiency is now a lever that reaches `sustainment_ok` and was not before. Check that against `pre_wi039_indicators.json` and `indicators.json` yourself. Is the comparison fair — same tool, same manifest shape, comparable packages?
7. **The wall-load caveat.** Every fence claim in this study is supposed to carry a caveat that `wall_load_ok` compares a flat-wall average operand to a printed peak limit. Is that caveat actually load-bearing here, or is it decoration? Does it change what the study may conclude at 100 MW wall-plug, where the scan says 46 candidates are blocked by the wall alone?
8. **Anything else.** Arm tagging, baseline membership, the pre-screen, the export, the channel list, the ordering deviation recorded in `scan.py`'s header.

## Rules

- `uv run python ...` only — never bare `python`, `python3` or `pip`.
- **Never read anything under `knowledge/holdout/`.**
- Do not edit any file. Do not run the study. You may run read-only analysis and you may re-run the oracle scan's own arithmetic against `results/window_scan.json` if you want to check a number.
- Do not commit.

## Return

A verdict of **MAJOR**, **MINOR**, or **CLEAN**, then a numbered list of findings. For each: what is wrong, why it matters, what it would take to fix, and how confident you are. Rank them — the author will act on the top ones first. If you believe the study is sound, say so plainly and say what you checked to conclude it; a critique that finds nothing but says what it looked at is a useful result, and an invented finding is not.
