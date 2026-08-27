# Staged edit — `.claude/skills/run-goal/SKILL.md`

One line, from Phase 3's manual check "Confirm `SKILL.md` states no rule the runbook owns". Written here because this session cannot write under `.claude/`.

## The finding

The skill closes its § Three roles with a normative sentence:

```text
An agent never fills two of these roles for the same round.
```

That is a rule, and it is the runbook's — `GOAL_RUNBOOK.md` states freshness at each place it applies (§ The pre-execution disposition checkpoint: "a fresh agent who did not do the work"; § The fresh review: "a fresh agent — one who did not do the round's work"). Two homes for one rule is the drift the design's cite-don't-restate discipline exists to prevent, and the skill's own preamble promises it restates nothing (D7).

**Correction, 2026-08-25:** an earlier version of this file claimed it was the only such sentence. It is not — `SKILL.md:42` and `:46` also restate runbook rules, and are handled in `skill-edit-2.md`. The keyword grep behind the original claim could not see restatements phrased as description.

## The edit

**Find:**

```text
An agent never fills two of these roles for the same round.
```

**Replace with:**

```text
Which role you are in decides which section you read. The runbook says what
"fresh" means at each place it matters.
```

## After applying

- `uv run python -m pytest tests/orchestration -q` → 24 passed. `test_the_skill_is_a_door_and_not_a_second_copy` asserts the frontmatter and the three pointers, none of which this touches.
- Re-run the check by hand: `grep -nE 'must|never|always|at most|only when' .claude/skills/run-goal/SKILL.md` → no hits.

Low severity. The rule is correct as stated and an operator following it does the right thing; the cost is a second home that can drift from the first.
