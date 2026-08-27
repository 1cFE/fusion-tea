# Brief: implement stage — goal-harness-contract

**From**: orchestrator (Fable), `/_my_orchestrate`, 2026-08-25.

**Execute**: `.project/active/goal-harness-contract/plan.md`, phase by phase, checking boxes and adding implementation notes as you go. The plan, `design.md` (rev 2), and `spec.md` are approved — build what they say; provenance grades are copied, never re-derived.

## Leg 1: Phase 1 ONLY, then stop and report

Do Phase 1 (the ADR home, complete, one commit), run its validation checklist, check its boxes, commit, and **stop — report the commit sha and any surprises back to me**. The parallel Item 2 agent is waiting on this commit to file its own decisions; I relay the sha. Do not start Phase 2 in this leg; I will resume you for Phases 2–7.

## Standing rules for the whole stage

- Branch: `feat/run-study-first-consumer` (you are on it). One commit per phase, subject leading with what the phase delivered. Never push; never merge.
- Honor the plan's surfacing stops literally: if a record can't be filed without inventing content, or a Phase 5 edit would displace a landed Item 6 sentence, STOP and ask me — do not resolve silently.
- `uv run python -m pytest` for all tests; `tests/study` must stay green in every phase that touches it.
- Do not touch `scripts/zotero_*`, research entry surfaces, or `knowledge/` registry files (Item 2's territory).
- No hardening-path mechanism, no goal-agent executable code beyond `adr.sh` as designed.
- Don't hard-wrap markdown prose; match each file's existing convention.
- Quality bar: the referent is `work/orchestration/handshake-lcoe-construction.md` — the runbook and templates must read at that bar for a non-builder. Do the plan's cold-read validations honestly; they are the point, not ceremony.
