# Trail: Bounded feasibility and design-point transfer

## Round 1 — fixed-assumption-local-search

### Strategy revision — 2026-09-16

- **Approach:** Reuse frozen rejections to locate coupled constraint conflicts, then refine a small supported geometry/current/accommodation search with explicit integer cooling requirements and transfer checks.
- **Assumptions:** Entering package dependencies and independently reviewed original equations remain applicable only within their documented conditional scope.
- **Abandonment conditions:** Unsupported physical improvement, changed comparison meaning, unresolved owner gate or declared evaluation budget.
- **Intended model increment:** None initially; expose current model limits rather than invent dependencies.
- **Intended study question:** Is there a sampled combined pass under fixed default assumptions, and what do smaller/reference/larger cases establish about conditional transfer?

### T-001 scope

- **Objective:** Define the meaningful bounded search and current transfer inventory.
- **Why now:** Prior frozen cases isolate interacting field, fit, burn, divertor and cooling constraints without establishing global infeasibility.
- **Scope:** Read clean existing evidence, inspect current dependencies, write pre-execution protocol and transfer contract draft; no model changes or new scientific equations.
- **Inputs:** `goal.md` and its grounding evidence at entering HEAD.
- **Done when:** Variables/bounds/budget/responses/stopping rules and evidence reuse are explicit, with unsupported transfer claims identified.
- **Stop when:** Unsupported dependency or scientific premise conflict blocks justified framing.

### T-001 start — 2026-09-16

T-001 · current package and frozen study evidence · `evidence/search-protocol.md` and `transfer-contract.md`.

### Parallel scope — 2026-09-16

[AGENT] A bounded transfer-inventory worker may run alongside coordinator search framing: both read unchanged package evidence; neither changes equations or another's files. Worker owns only `transfer-contract.md` and `evidence/transfer-inventory.md`. Coordinator owns trail, goal, search protocol and execution. Results integrate sequentially before final conclusions.

### T-001 return — 2026-09-16

- **Outcome:** COMPLETE.
- **Evidence:** `evidence/search-protocol.md`, study `protocol.md`, `axes.json`, `indicators.json` and `reviews/preexecution-check.md` (unpinned; no native digest).
- **Reading:** Six supported design choices have represented constraint paths. Search can proceed under fixed performance, engineered geometry bounds and explicitly incomplete accommodation economics. Transfer inventory is independently scoped and continues alongside execution.
- **Decision:** Coupled previous rejections warrant bounded refinement; authorize the stated protocol without changing scientific assumptions; execution detail; coordinator; new study directory and protocol.

### T-002 scope

- **Objective:** Execute a bounded native search and explain joint constraint outcomes with transfer checks.
- **Why now:** T-001 established supported inputs and pre-execution limits.
- **Scope:** One unchanged package, one native study, at most 500 oracle coordinates and 80 native cases including baseline; all failures retained.
- **Inputs:** `goal.md`, `evidence/search-protocol.md`, current study protocol and captured preparation.
- **Done when:** Frozen native/oracle-verified results establish a sampled pass/neighborhood or informative bounded rejection and reference/smaller/larger responses.
- **Stop when:** Declared budget, mechanical failure past cap, unsupported premise or owner gate.

### T-002 start — 2026-09-16

T-002 · `exploration/stellarator_e2e/studies/20260916-bounded-feasibility-transfer/` · committed native study and bounded synthesis.

### T-002 return — 2026-09-16

- **Outcome:** MECHANICAL_FAILURE.
- **Evidence:** Baseline invocation failed before evaluation with missing `simkit`; `/tmp/bounded-baseline.log` (unpinned; no native digest).
- **Reading:** Scientific inputs unchanged. The prior study's runtime-command.md supplies the required sealed TEAx import path.
- **Decision:** Retry the identical baseline with the documented runtime import path; execution detail; coordinator; invocation only.

### T-002 start — 2026-09-16

Retry 1 of 2; task, inputs, scope and meaning identical. Operational correction: use `PYTHONPATH=.:/home/reid/1cfe/teax/packages/teax-simkit STUDY_REQUIRE_TEAX=1 .codex-test/run python ...`, as in the preceding frozen study.
