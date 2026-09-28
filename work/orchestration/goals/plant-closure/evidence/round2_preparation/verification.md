# Preparation checks

[AGENT] 2026-09-11, this worktree. No Python modeling, package generation, integration, oracle probe or study execution was run.

- `.codex-test/run python -B -m pytest tests/study/test_records.py -q -p no:cacheprovider`: 37 passed in 1.00s after six joined discovery rows were appended.
- `.codex-test/run python -B -m pytest tests/study/test_records.py tests/orchestration/test_goal_contract.py -q -p no:cacheprovider`: 65 passed, one failed in 0.96s. The failure is the previously recorded `test_narratives_are_separate_from_the_goal_contract`, which finds `work/narratives/` in unchanged `work/orchestration/goals/wall-and-heating/trail.md`. It is not a plant-closure preparation regression; remediation Round 4 review records the same failure. No unrelated trail or checker was changed.
- A read-only Python consistency check found 141 unique qualified channel values and exact equality to the inherited operating-heating map; twelve proposed cell dispositions; twenty-three numeric cell evidence rows; and six appended discovery rows after a byte-identical original prefix.
- `git diff --check`: passed for tracked edits at this check. The preparation markdown is authored one paragraph/bullet/table row per source line.
- Read native path histories: WI-046's cited phase/evidence record and T-007's integration return have no later changes in this checkout. This preparation does not resume a historical task or adopt the moving remediation working tree as execution authority.

The full model/study batteries are not run for this documentation-only change. Their historical failures, skips and checker limitations remain attached to native evidence, not asserted green by this packet. Final candidate checks, qualified-key mapping, study critique and final grading remain future work.
