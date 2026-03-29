[1;33m  → Generating: AGENTS.md[0m
The content is ready. Here's what I wrote — awaiting your approval to write:

```
AGENTS.md (~70 lines)

## Build & Run
- uv sync, then extract → build → serve (port 8421)
- Partial build flags: --data-only, --html-only, --concept 01 04

## Validation  
- pytest, mypy, ruff check/format — all scoped to exploration/concept_explorer/
- curl health check

## Codebase Patterns
- Directory layout (concept_explorer/ + concept_analysis/analyses/)
- Key conventions: M$ units, typed models, no raw dicts, atomic JSON writes
- Sensitivity method distinction (autodiff vs finite_difference)
- All 7 API routes

## Known Gotchas
- Never modify ../1costingfe
- Don't parse model_output.txt
- dist/ must exist before server start
- CAS10-CAS90 all required even if zero cost
- Port 8421 fixed
- Always uv run python
```

Once you approve the write, it'll land at `AGENTS.md` in the project root.
