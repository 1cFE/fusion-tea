# Fresh review brief — round 2 assurance and the independent review of `answer.md`

You are a fresh reviewer for the goal `design-space-combinations` (`work/orchestration/goals/design-space-combinations/`). You did not do the work. Two jobs in one return: (A) round-2 assurance in the goal runbook's sense (`work/orchestration/GOAL_RUNBOOK.md` § The fresh review), and (B) the independent review of `answer.md` that the goal's completion condition (6) requires. Return findings, not fixes; do not edit any file; never read `knowledge/holdout/`.

## Entry files

- `goal.md` (the contract: Question, Consumer, Answered when (1)–(6), Invariants, Reserved gates, Close rule).
- `trail.md`: read "## Round 2" to the end (strategy, T-004 and T-005 scopes, starts and returns, the T-005 commit note, the amendment of 2026-09-26, the Round 2 result). Round 1's result and its accepted review are context only (`evidence/round1-review.md`).
- `answer.md` (the deliverable under review).
- `evidence/round2-learnings-proposed.md` (L-009–L-013 as proposed; `learnings.md` holds L-001–L-008 accepted).
- Native evidence by citation: `work/active/WI-093_combination-assemblies/{design,report}.md` and `evidence/{cases-summary.json, verification-summary.json, build-hashes.json, native_runs/summary.json}`; `evidence/design-review.md`, `implementation-review.md` (both with dispositions); `evidence/compatibility-map.md` § 2–3; `exploration/aries_integrated/studies/20260926-aries-design-choice-interactions/results/interactions.md` (round 1's sealed study reading).

## Questions

1. **Answer against the contract.** For each of (1)–(6) in `goal.md` § Answered when, is the answer's claim of met / pending supported by the cited evidence? Spot-check at least six numbers in `answer.md` § 3 and § 5 against `cases-summary.json` and `interactions.md`. Is the "three previously untested, compatible combinations satisfy every evaluated check" claim exactly supported (which cases, which counts)?
2. **Overstatement.** Does the answer claim anything the receipts do not carry: design adequacy, interactions "established" from single evaluations (the answer says these are observations), steam-path reuse, agreement of the two costing laws, or anything about C-3 beyond "compatible by the map, not demonstrated"?
3. **The consumer's question.** Does § 6 answer the owner's verbatim test in `goal.md` § Consumer plainly, with the limit of reuse named as specific relationships, and without a coined phrase the write-up would have to decode?
4. **Round assurance.** Task scopes vs returns for T-004 and T-005 (inside scope? deviations recorded?); the retry count (2 mechanical retries claimed as the cap; were they mechanical, and is anything else a retry in disguise?); the review triggers (design and implementation reviews obtained, findings applied, dispositions honest); the Round 2 result's stop reason; cited refs live (`git show` the commits named).
5. **Learning delta.** Are L-009–L-013 supported by the cited evidence, scoped, and not overstated? Propose rewrites where needed.
6. **The constraint violation.** The amendment records that round-1 commit `b74dcc5e` included two of the owner's write-up files. Verify with `git show --stat b74dcc5e` and `evidence/entry-state.txt`. Is the record honest and complete (mechanism, what was and was not rewritten, the owner decision named in the answer § 11)? Is anything else in the goal's commits outside "goal files and native artifacts" (`git show --stat` on `428392d0`, `b74dcc5e`, `c745a6eb`, `bf40cfcf`, `6e048817`, `918372d1`, `5723dfa6` and HEAD)?
7. **Replay.** Are the commands in `answer.md` § 10 exact and do they write outside the frozen study and the sealed evidence? You may run `exploration/combinations/verify.py` (read-only apart from the two receipts it owns) and the preservation check with `--output /tmp/...`; do not run `build.py`, `run.py`, the study executor or the scratch screens.

## Return format

`Verdict: PASS | FINDINGS | FAIL` for (A) and for (B) separately; one line per question; numbered findings with severity (blocking / note), path:line evidence and the sentence to correct; what you did not check. Under 70 lines.
