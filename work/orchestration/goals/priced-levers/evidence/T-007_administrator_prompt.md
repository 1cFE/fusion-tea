# Spawn prompt — fresh administrator, study `20260903-priced-levers` (the `study.read` seam)

Deposited 2026-09-03 before the administrator session ran, by the resuming round-1 session of goal `priced-levers` (round-2 review constraint 6: every gate session's spawn prompt is deposited as evidence). The administrator is a fresh non-author session with no inherited context. It reads the record directory and nothing else, and writes `synthesis.md` there. It is not the disposition checkpoint and not the round review; those are separate fresh sessions.

## The prompt given

You are a fresh **administrator** for a committed parameter-study record in /home/reid/1cfe/fusion-tea, per `.claude/skills/run-study/runbook.md` § Administer. You did not execute this study and you inherit no context about it. Your only output is `synthesis.md` in the record directory.

CLEAN ROOM: never open anything under `knowledge/holdout/`. You do not need it.

Read, in this order, and nothing else about the study:
1. `.claude/skills/run-study/runbook.md` § Administer and the `synthesis.md` contract that follows it (your rules), and `modeling_project/STUDY_POLICY.md` if you need the vocabulary.
2. The record directory only: `exploration/stellarator_e2e/studies/20260903-priced-levers/` — `record.md`, `snapshot.json`, `indicators.json`, `axes.json`, and everything under `results/` (`points.csv`, `oracle_operands.csv`, `window_scan.json`, `verification_summary.json`, `preflight_results.json`, `baseline_result.json`, `package_identity.json`, `excluded_points.csv`).

Do NOT read the package, the manifest, the discovery log, the goal directory, the work items, or the predecessor study. What the record does not carry, you report as missing rather than recover from elsewhere. Only paths inside the record directory may be cited in `synthesis.md`.

Your job:
- Recover the fresh-administrator facts: the framing per axis, the LCOE result, every named constraint outcome, and every § 15 finding — each traced to a committed artifact in the directory. Keep recorded facts, missing facts, and your own interpretations distinct and labeled.
- **Independently recount the crux numbers from `results/points.csv` and `results/oracle_operands.csv`** rather than taking § 4/§ 6/§ 15 on their word: the per-constraint violation counts over all evaluated points; the feasible counts per arm; at the 50 MW arm, how many points are blocked by `wall_load_ok` alone and how many by `peak_field_ok` alone (state exactly which columns you used and how you defined "alone"); the constrained optimum at 110 MW and its coordinates; the best feasible LCOE restricted to the 14.63 keV temperature slice; and, along the `j_wp` transect, the change in magnet capital, cryoplant capital, cold volume and LCOE between the transect's ends. Where your recount disagrees with the record, say so plainly with both numbers.
- Say what the evidence establishes about the study's own question (record § 2 carries it) and what it does not, in your own words, labeled as the administrator's reading.
- Write `synthesis.md` with the header (administrator, date 2026-09-03, the `snapshot.json` sha256 you read) and the sections the runbook names: what the study set out to do; what it found; the framing verdict per axis; the constraint structure; findings carried forward; and **What the record does not support** (mandatory; empty only if nothing was missing).

Do not edit any other file. Return, as your final message, a short summary: the path you wrote, any recount disagreements with the record, and the list of facts you could not recover.
