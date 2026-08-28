# Brief to /_my_spec_review — GSTH Item 5 spec

Review `.project/active/goal-research-model-proof/spec.md` (Draft, 2026-08-27). You are a
fresh, non-author reviewer. Do NOT edit the spec and do NOT run git commits — return your
findings; the orchestrator routes them. Finish with `ARTIFACT: <path>` if you write a
review artifact, else return findings in prose.

## Context

- Requirements source: `.project/backlog/epic_goal_strategy_task_harness.md` § Item 5
  (line ~364). The spec must cover that section's scope, out-of-scope, and success
  criteria without narrowing or widening them.
- Owner rulings at Align (settled, verify the spec carries them faithfully — see
  `.project/active/goal-research-model-proof/align.md`): live need = p_pump re-source
  (row `20260821-power-cycle-ab#3`), taken off Run-Study Item 6 Phase 4's list; reserved
  gates (a) grounding terms, (b) mutations beyond the goal directory, (c) judgment-call
  close; runbook `research`-row flip in scope; `close`/`pre_pr` owner-held.
- Operating contract: `work/orchestration/GOAL_RUNBOOK.md`. Item 2 seam:
  `docs/research_seam_operator_guide.md`, `scripts/research_seam.py`. Prior proof shape:
  `.project/completed/20260827_goal-cold-pickup-proof/`.

## Review priorities (beyond your command's own checklist)

1. **Provenance fidelity** (capture-fidelity rules): every `[NEED]` traces to a real owner
   ruling; no `[INFERRED]` promoted; settled items owner-originated only.
2. **R-C2** — the spec surfaces a trigger-phrase tension (runbook checkpoint fires "after
   a study reading"; this round reads a committed record). Judge whether the spec's
   reading is sound and whether it is surfaced loudly enough, or whether it needs an
   owner ruling before design.
3. **Honest-outcome integrity** — could any requirement pair force a manufactured
   positive or a manufactured prerequisite? (R-B3 vs the first success criterion.)
4. **Verifiability** — can every criterion be checked against disk by a later audit?
5. **Cross-references** — spot-check the cited paths/anchors exist at the cited commits.

Classify findings must-fix vs advisory.
