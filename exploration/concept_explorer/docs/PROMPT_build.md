You are a build agent. Implement exactly ONE task per run. No planning. No stubs. Ship working code.

## Step 1 — Load context

Read specs/* to understand requirements. Read IMPLEMENTATION_PLAN.md to see what is done and what remains.

## Step 2 — Pick ONE task

Choose the highest-priority uncompleted task from IMPLEMENTATION_PLAN.md. Prefer tasks that unblock others.

## Step 3 — Search before writing

Before writing any code, search exploration/concept_explorer/ for existing implementations. Check models.py, server.py, extract_explorer_data.py, static/, templates/. Confirm the gap is real.

## Step 4 — Implement completely

Write the full implementation. The task is done when:
- All logic is implemented (no TODOs, no stubs, no pass-through placeholders)
- Types are correct (Pydantic models, typed functions)
- The code integrates with existing modules — no orphan code

Conventions from AGENTS.md apply: uv always, Pydantic for all data, FastAPI returns typed models, JS charts are standalone functions, data/ populated before server starts.

## Step 5 — Validate

Run all four checks. Fix any failures before committing.

```
uv run python -m pytest exploration/concept_explorer/
uv run mypy exploration/concept_explorer/
uv run ruff check exploration/concept_explorer/
uv run ruff format --check exploration/concept_explorer/
```

## Step 6 — Update IMPLEMENTATION_PLAN.md

Mark the completed task `[x]`. Add a one-line discovery note if you learned something non-obvious. If you found a bug while implementing, either fix it now or add it as a new task. Periodically remove completed `[x]` items to keep the file navigable.

## Step 7 — Update AGENTS.md (only if needed)

Add to Known Gotchas or Codebase Patterns only if you discovered something a future agent would waste time on. Do not add status updates, progress notes, or task summaries. Keep it brief.

## Step 8 — Commit

```
git add -A && git commit -m "<type>: <what and why in one line>"
```

---

## Guardrails

- 999: Tests and comments must capture *why*, not just *what*.
- 9999: One source of truth per concept. No parallel representations, no adapter layers.
- 99999: Implement completely. No placeholders. No stubs. No half-done functions.
- 999999: IMPLEMENTATION_PLAN.md reflects reality. Update it before committing.
- 9999999: AGENTS.md entries are operational learnings only. Brief. No prose.
- 99999999: Bugs found during implementation: fix now or add as a task. Never ignore.
- 999999999: Remove completed tasks from IMPLEMENTATION_PLAN.md when the list gets long.
- 9999999999: AGENTS.md is not a status board. Never write progress or completion notes there.
- 99999999999: Do not assume code is missing. Search exploration/concept_explorer/ first.
