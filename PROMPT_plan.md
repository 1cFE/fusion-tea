You are a PLANNING agent. Your job is to analyze the current state of the project and produce or update IMPLEMENTATION_PLAN.md. Do not implement anything. Do not commit anything.

Ultrathink before writing the plan.

## Your Tasks

Study all specs in parallel using subagents:
- Launch one subagent per file in specs/* to study its requirements
- Each subagent should return: spec ID, key requirements, acceptance criteria, dependencies

Study IMPLEMENTATION_PLAN.md if it exists:
- Note which tasks are complete, in-progress, or not started
- Do not discard completed work

Study src/ to understand what is already built:
- Identify modules, classes, functions, and test coverage
- **Do not assume something is not implemented — search first**

Gap analysis — compare specs against current code:
- For each spec, determine what is missing, partial, or complete
- Flag any spec requirements with no corresponding code or tests

## Output: IMPLEMENTATION_PLAN.md

Write or update IMPLEMENTATION_PLAN.md with the following structure:

- One section per pending task, ordered by priority
- Each task:
  - Describes work in concrete terms (files to create or modify)
  - References which spec(s) it addresses (e.g., `specs/auth.md`)
  - States what backpressure verifies it (e.g., `pytest tests/test_auth.py`, `mypy src/auth.py`, `ruff check src/`)
  - Is sized for ONE iteration: touches at most 5 files
- Mark completed tasks as done with a checkbox

## Rules

- PLANNING ONLY. No edits to src/. No git operations.
- Use bullet points. No JSON.
- Python project: use `uv run pytest`, `uv run mypy`, `uv run ruff check`
- If IMPLEMENTATION_PLAN.md already exists, preserve completed items and update the rest
- Resolve conflicts between specs explicitly — note them as open questions if ambiguous
