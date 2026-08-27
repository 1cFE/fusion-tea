# Staged edits — `.claude/skills/run-goal/SKILL.md`, round 2

Three edits from the audit (`audit.md` § Certification, gaps 1 and 7). Written here because this session cannot write under `.claude/`.

**Apply against:** `.claude/skills/run-goal/SKILL.md` as committed at `21c46dc5`.

Edit 1 is part of `audit-F2` and depends on the runbook's new § What "fresh" means, which is on disk in this session's changes. Apply the runbook first, or together.

---

## Edit 1 — the `fresh` overclaim (audit-F2)

The line told a reader the runbook says what "fresh" means at each place it matters. It did not — it said only "did not do the work," which is weaker than the owner's rule. The runbook now defines it in one place, so the skill can point at that place, and the role description should carry the owner's boundary rather than the weaker paraphrase.

**Find:**

```text
- **Fresh reviewer** — did not do the work. Reads a study's proposed dispositions before follow-up executes, or reviews the closed round and writes the next strategy.

Which role you are in decides which section you read. The runbook says what
"fresh" means at each place it matters.
```

**Replace with:**

```text
- **Fresh reviewer** — a session that did not do the work. Reads a study's proposed dispositions before follow-up executes, or reviews the closed round and writes the next strategy.

Which role you are in decides which section you read. `GOAL_RUNBOOK.md` § What
"fresh" means defines the boundary, says who obtains the reviewer on each path, and
gives the agent its move when it cannot start a session — read it before either
review mode.
```

## Edit 2 — restatement at `:42` (round-open rule)

`GOAL_RUNBOOK.md:72` owns this rule. The skill restated it nearly verbatim.

**Find:**

```text
To tell whether a round is open, read the headings — a round is open exactly when its `## Round N` section carries a `### Strategy revision` and no `### Round N result`.
```

**Replace with:**

```text
To tell whether a round is open, read `trail.md`'s headings — `GOAL_RUNBOOK.md` § Opening and closing a round gives the rule.
```

## Edit 3 — restatement at `:46` (headings are the contract)

`GOAL_RUNBOOK.md:35` owns this one.

**Find:**

```text
Templates are at `work/orchestration/goal-templates/` — copy them; their headings are the contract.
```

**Replace with:**

```text
Templates are at `work/orchestration/goal-templates/`; copy them rather than writing the files from scratch.
```

---

## After applying

- `uv run python -m pytest tests/orchestration -q` → 25 passed (24 plus the new § What "fresh" means stage assertion). `test_the_skill_is_a_door_and_not_a_second_copy` asserts the frontmatter and the three pointers, none of which these touch.
- Re-run the manual check, this time as a restatement check rather than a keyword grep: read each declarative sentence in `SKILL.md` and ask whether `GOAL_RUNBOOK.md` also says it. After these three, the remaining declaratives are role descriptions, mode selection, the directory name, and pointers.

**Note for the plan.** The earlier claim that the role sentence was "the only such sentence in the file" (`plan.md`, `staging/skill-edit-1.md`) was wrong — the check behind it was a keyword grep that cannot see restatements phrased as description. A dated amendment note recording that correction is in `plan.md` § Phase 7.
