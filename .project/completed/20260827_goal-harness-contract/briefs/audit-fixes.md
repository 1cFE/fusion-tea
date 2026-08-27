Orchestrator: the audit is in (`.project/active/goal-harness-contract/audit.md` — read it in full). Verdict Needs Work; two blockers plus a set of cheap confirmed findings. All dispositioned APPLY. Work through them:

**Blockers:**

1. **audit-F1** — ADR-005 frontmatter grade and INDEX.md:11 row: write the split, per the register's own README:45. Frontmatter something like `grade: "[AGENT] inference (topology; owner may override) + [OWNER 2026-08-25] (pre-execution checkpoint placement)"`, index cell to match. Your Phase 1 reasoning was right before the owner half entered the body; it wasn't re-checked after — fix the two scanning surfaces.
2. **audit-F2** — the checkpoint gate needs the owner's actual rule and a defined agent move. In GOAL_RUNBOOK.md (§ the checkpoint, § the fresh review, and wherever "fresh" is defined): state the session boundary verbatim-strength — the critic is never the author's session (source: `goal-driven-model-development-harness.md:47`, [OWNER]) — and define the move for an agent that cannot delegate: a recorded stop (kind: owner gate/handoff) that hands the reading back to the operator to start a fresh session. No dispatch machinery — that stays barred; the prose handoff IS the lean answer. Fix SKILL.md:28-30's overclaim to match what the runbook now actually says.

**Confirmed smaller findings — apply all:**

3. Three uncited pointers in the runbook: add the path to `.claude/skills/run-study/runbook.md` at the seams table; one-line gloss of "pin" with a pointer to where the study layer defines it; replace "the current manual integration pattern" with the honest form — no written pattern exists; treat as a PREREQUISITE return until epic Item 3 lands.
4. Dead cross-refs: `002-round-boundary.md:32` and `005-review-topology.md:40` → cite the live heading "The fresh review".
5. `adr.sh:28` and `template.md:5`: default grade to a placeholder that cannot be left as-is (`[GRADE — copy from source]`), not `[AGENT]`.
6. README prior-art paragraph: one sentence on the loose `ADR-00X` usage in `work/completed/20260303_WI-008.../design.md` meaning `AD-XXX`.
7. audit-F3: one line each — `CLAUDE.md` § Project Structure gets an `adr/` row under `.project/`; `modeling_project/ARCHITECTURE.md` gets a sentence naming the `AD-XXX` vs `ADR-NNN` split and pointing at `.project/adr/`.
8. SKILL.md:42/:46 restatements: replace with pointers (same treatment as the role sentence), and correct `plan.md:685`'s "only such sentence" claim with a dated amendment note.

Then: append the product-lens resolution block dispositioning audit-F1/audit-F2 (and F3) with authority bases so the gate reads CLEAR; re-run `uv run python -m pytest tests/study tests/orchestration -q` (the writer-homes and skill-door tests must still pass — adjust test expectations ONLY if an assertion cited the old wording, and say so); check the remaining plan box state honestly.

If your git wall persists, leave all on disk and report the intended commit slices. For `.claude/` writes, stage under `staging/` as before and I'll apply. ARTIFACT line when done.
