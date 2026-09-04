# Plan: Goal Narrative Snapshots

**Status:** Implementation Complete — Pending Audit
**Owner:** Reid W
**Created:** 2026-09-04
**Spec:** `.project/active/goal-narrative-snapshots/spec.md`
**Design:** Intentionally skipped by owner-approved specification; this change adds no runtime architecture or cross-component interface.

---

## Phase 1 — Extract and validate the narrator

- [x] Add the narrative contract test stencil before changing implementation surfaces.
- [x] Restore the five-surface goal runbook and keep `/run-goal` unchanged.
- [x] Add the discoverable, user-invocable `/narrate-goal` skill as the sole authoring contract.
- [x] Move and relink the three worked examples under `work/narratives/` with UTC migration timestamps.
- [x] Bring the wall-and-heating snapshot to a coherent, visibly provisional working-tree cutoff.
- [x] Make goal-level closure status visible and add an honestly labeled close-time proxy without changing the goal contract.
- [x] Run focused validation, fix failures, and record the results.
- [x] Synchronize the spec and current-work status.

## Implementation Notes

### Phase 1 Completion

**Completed:** 2026-09-04T18:53:01Z

**Changes Made:**

- Added `.claude/skills/narrate-goal/SKILL.md` as the discoverable, user-invocable authoring contract. It creates one UTC-stamped snapshot, preserves the authority boundary, labels dirty inputs provisional, requires the eight-section shape and visual/skim quality, and runs focused validation.
- Added the narrow `.gitignore` exception that makes the project-owned narrator skill committable alongside the existing project-owned Claude skills.
- Restored `work/orchestration/GOAL_RUNBOOK.md` to its five-surface contract and left `.claude/skills/run-goal/SKILL.md` byte-unchanged.
- Moved and relinked the three worked examples to `work/narratives/20260904-184254Z-<goal-slug>.md`; all local links resolve from the new home.
- Updated the wall-and-heating example to a coherent provisional cutoff covering round-2 T-001 complete and T-002 started, including the corrected 2.87/4.95 extraction-artifact reading and peak-driven lifetime result.
- Extended `tests/orchestration/test_goal_contract.py` to check narrative separation, skill discovery and contract, sortable names, repeated-snapshot compatibility, exact section order, metadata, authority warning, purposeful visual presence, paragraph and file limits, and local links.
- Repaired live `.project/CURRENT_WORK.md` and specification pointers to the migrated snapshots.

**Validation:**

- `uv run pytest tests/orchestration/test_goal_contract.py -q` — 29 passed.
- `git diff --check` and `git diff --cached --check` — passed.
- `.claude/skills/run-goal/SKILL.md` — no diff.
- `.claude/skills/narrate-goal/SKILL.md` — visible to Git through the narrow project-owned skill exception.
- Narrative line counts — 161, 201, and 246; all below 250.

**Issues Encountered:**

- The generic Codex skill validator rejects Claude's valid `user-invocable` frontmatter key, so the repository's YAML contract test validates that field instead.
- The repository's tool-owned skill ignore pattern initially hid the new skill; a directory-specific exception now exposes only `narrate-goal`.
- The first quality run found prose blocks over the 60-word ceiling in the evolving wall example; those claims were split or tightened and the suite rerun to green.

**Deviations from Plan:**

- No technical design was created, as explicitly approved in the specification.
- No separate generator or validator script was added. The skill writes Markdown directly and reuses the existing orchestration contract test, keeping one procedural surface.
- Unrelated concurrent changes under the round-2 modeling work, backlog, and goal trail were preserved and not folded into this coding item.

### Closure Metadata Follow-up

**Completed:** 2026-09-04T21:43:15Z

- Amended the narrator contract and examples so `Goal status` begins with `Open` or `Closed`, only an owner close entry counts as goal closure, and closed goals show the authoritative date plus an explicitly labeled Git commit-time proxy when the trail has no time.
- Filed the missing machine-readable goal status and closure timestamp contract as a P2 item in `.project/backlog/BACKLOG.md`; `GOAL_RUNBOOK.md`, the goal templates, and `/run-goal` remain unchanged.
- Extended the focused contract checks for open/closed wording and conditional close metadata. `UV_CACHE_DIR=/tmp/fusion-tea-goal-narrative-uv-cache uv run pytest tests/orchestration/test_goal_contract.py -q` passed: 29 tests. `git diff --check` passed; narrative line counts are 162, 202, and 246.
