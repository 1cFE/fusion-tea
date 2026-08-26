# Brief → /_my_spec_review — goal-research-seam (GSTH Item 2)

Review the spec at `.project/active/goal-research-seam/spec.md`. You are a fresh session; the authoring session is separate.

Context: this is Item 2 of the Goal Strategy and Task Harness epic — the native research acquisition/registration seam. The authoritative contract is `.project/backlog/epic_goal_strategy_task_harness.md` § Item 2. Owner rulings at `.project/active/goal-research-seam/align.md`. Evidence base: `.project/research/20260822-120756_research-extraction-harness.md`.

Review against:
1. **Fidelity to the epic contract** — do the requirements cover all four scope areas and map to the epic's six success-criterion checkboxes? Is anything from the epic's out-of-scope list smuggled in, or anything in-scope dropped?
2. **Provenance discipline** — grades (`[HARD]`/`[NEED]`/`[INFERRED]`/`[INHERITED]`) correctly assigned per capture-fidelity rules; owner rulings not over- or under-read (especially the DI-gate ruling at align.md and the deliberately deferred manifest-identity mechanism).
3. **Spec vs design boundary** — the spec should state requirements, not mechanisms; check nothing design-shaped leaked in and nothing requirement-shaped was deferred out.
4. **Testability** — are the success criteria and R-E requirements verifiable without the network, as the align ruled? Any criterion that cannot be objectively checked?
5. **Real-world fit** — the spec must be implementable against the actual code: `scripts/zotero_ingest.py`, `scripts/zotero_lib.py`, `agentic-mbse extract` (pinned), `knowledge/holdout/aries-cs/PROTOCOL.md`. Flag any requirement the existing code makes incoherent.

Do not read or depend on Item 1's in-flight artifacts (`goal-harness-contract/`); it runs in parallel and owns CLAUDE.md/runbook/GOAL_RUNBOOK/ADR files.

Deliver your verdict and findings (must-fix vs advisory). End with `ARTIFACT: <path>` for the review record.
