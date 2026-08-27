# Brief → /_my_plan — goal-research-seam (GSTH Item 2)

Write the phased implementation plan for the approved spec and design.

## Authoritative inputs (read in this order)

- `.project/active/goal-research-seam/design.md` — approved after review + revision; its decisions D1–D14, architecture, failure ladder, vocabulary mapping, and validation table are settled. Do not redesign.
- `.project/active/goal-research-seam/spec.md` — the requirement contract (R-*, SC1–SC9).
- `.project/active/goal-research-seam/design-review.md` — context for why decisions read as they do.
- `.project/active/goal-research-seam/align.md` — owner rulings.

## Sequencing constraints the plan must honor

1. **De-risk first** (design § Next-Stage Handoff): the `zotero_lib` loader key-tolerance change plus `test_zotero_path_contract.py` (the characterization test pinning today's Zotero and local-PDF output) land **before** any non-Zotero manifest row can exist. The characterization test is written against the *current* code before the refactor touches it.
2. Build order after that should follow dependency: holdout guard (`holdout_guard.py`, parse-pinning test) → registration op (`source_registry.py`: staging, capture, provenance verification, commit/rollback ladder, receipts, `verify` + legacy baseline) → bookkeeper (`research_seam.py`: request/negative/run/close) → command (`.claude/commands/research-acquire.md`) → operator guide (`docs/research_seam_operator_guide.md`) → upstream filings (R-F1).
3. Each phase ends with its tests green and a commit; name the exact test files from the design's validation table and the command to run them (`uv run python -m pytest tests/research/ ...`). The PDF-chain test is marked slow — note how it runs in CI vs locally.
4. The final phase runs the full affected set: `tests/research/`, `tests/test_dependency_provenance.py`, and any suite touching `SOURCE_INDEX.md`/`MANIFEST.jsonl` readers; plus a checklist mapping each SC1–SC9 to its verifying test or (for SC9) the audit-stage walk.

## Plan rules

- Checkbox phases with concrete deliverables per phase; each phase independently commit-able; implementation notes slots for deviations.
- No scope beyond the design: no crash recovery, no search counting in code, no DI minting, no edits to pinned `agentic-mbse`, no touches to Item 1's files (CLAUDE.md, run-study runbook, DISCOVERY_LOG, GOAL_RUNBOOK, ADR home).
- The `.gitignore` addition for `knowledge/.staging/` and the checked-in `verify` legacy baseline are explicit deliverables — put them in a phase.
- ADR candidate (design Appendix A) is *not* filed by this plan — R-F2 coordination happens when Item 1's ADR home exists; note it as a handoff line.
- Estimate per phase; the epic allocated ~10h execute for this item.

Write `plan.md` at `.project/active/goal-research-seam/plan.md`. End with `ARTIFACT: <path>`.
