Answers to your three questions plus one ruling. Continue Phases 4–10.

**1. Wheels restored — YES.** The recorded sealed wheels were on disk in stop-parser artifact dirs under /tmp; I copied the complete matching set to a durable home and verified all three sha256s equal WHEEL_HASHES, then ran the producer: `pytest tests/test_dependency_provenance.py` → **3 passed** with these exports:

```
export STOP_PARSER_WHEEL_TARGET=/home/reid/1cfe/fusion-tea/.venv/lib/python3.12/site-packages
export STOP_PARSER_AGENTIC_WHEEL=/home/reid/1cfe/stop-parser-sealed-wheels/agentic_mbse-0.1.3-py3-none-any.whl
export STOP_PARSER_CODEGEN_WHEEL=/home/reid/1cfe/stop-parser-sealed-wheels/sysml_codegen-0.1.1-py3-none-any.whl
export STOP_PARSER_COSTINGFE_WHEEL=/home/reid/1cfe/stop-parser-sealed-wheels/1costingfe-0.1.0-py3-none-any.whl
```

Use exactly these for every phase. Phases 4–10 run as written — no SC-map change, no skip pattern. Record the wheel home (`/home/reid/1cfe/stop-parser-sealed-wheels/`, outside the repo, sha256-verified against `tests/test_dependency_provenance.py::WHEEL_HASHES`) in the operator guide's environment section so the next operator can reconstruct it.

**2.** Moot given 1. Do not add the skip pattern.

**3. Budget raised** — this resume carries a larger cap. Continue in this session; if you approach the cap again, stop at a phase boundary with a status message rather than mid-phase.

**Snapshot ruling (accepted):** gate 4 finds the tracked snapshot as the single `*.snapshot.json` beside the models root — the found-rather-than-named pattern `study_route.spec_path` already uses. Keep the pinning test. Record it as a design note (D-numbered addendum or inline note at the gate-4 row), including the refusal shape when zero or several snapshot files are found (that ambiguity is `input-invalid`/R-C5 territory — say which and be consistent).

Your phase-boundary commit discipline is exactly right — keep it. Also right to stop rather than thin the gate; the same bar applies through Phase 10.
