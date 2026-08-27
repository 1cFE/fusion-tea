# Brief → /_my_spec — goal-research-seam (GSTH Item 2)

You are speccing **Item 2: Native Research Acquisition and Registration Seam** of the Goal Strategy and Task Harness epic. Work item location: `.project/active/goal-research-seam/`.

## The work item (epic text is authoritative — read it)

Read **`.project/backlog/epic_goal_strategy_task_harness.md` § Item 2** in full: objective, current state, required reading, scope (4 areas), out of scope, success criteria, deliverables. That section is the contract this spec operationalizes. Its provenance marks (`[OWNER]`, `[INHERITED: ...]`) must be carried into the spec per the absorb mapping (owner-stated → `[NEED]`, inherited → `[INHERITED]`, agent inference → `[INFERRED]`).

**Objective**: give research one producer-owned request/return boundary that ends in registered, MR-4-citable evidence or an explicit durable bounded negative — no hand-written index steps.

## Intent from the concept layer (why this item exists)

- The whole loop ran once by hand (Item 6 / WI-031): the research hop was bash + hand-written `SOURCE_INDEX.md` blocks. The goal layer being built by this epic needs research to be one callable seam: bounded request in → `registered sources | bounded negative | operator queue | blocker` out, with native references. A goal round may not silently absorb this repair — that is why it is its own item.
- Concept success criterion 4 `[INHERITED: goal-driven-model-development-harness.md]`: when a disposition is "research round," the agent ends with each source registered — citable under MR-4 by repo path, provenance sufficient to re-fetch and verify, holdout-checked before write. Unfetchable source → operator queue with reason. Zero-source search → recorded negative that blocks silent repeats.
- Primary evidence base: `.project/research/20260822-120756_research-extraction-harness.md` — inventory, gap list, reusable patterns P1–P10, feasibility ("mostly assembly"). Its recommendations 1–3 (register-source op first; one request row; fork/wrap `/research` rather than editing the symlinked upstream) are `[AGENT]` recommendations consistent with the epic scope; treat them as strong defaults, not owner mandates.

## Owner rulings at Align (`[OWNER 2026-08-25]`) — settled, carry into spec

1. **DI gate**: registration and insight approval are separate operations with an explicit approval gate. Acquisition may register sources but must not automatically mint DIs. Not to be over-read: an approved DI may be created later in the same broader workflow via the native research-approval operation — no separate session or goal round is required.
2. **Non-Zotero manifest identity** (content hash vs URL vs push-through-Zotero): deliberately deferred to design. The spec should state the requirement (every registered source has a durable manifest identity; duplicates detected) without choosing the mechanism.
3. No other reserved gates. Final quality is on the orchestrator.

## Constraints the spec must hold

- **Extend, don't duplicate**: the registration operation extends the existing writer in `scripts/zotero_ingest.py` / `scripts/zotero_lib.py`; no second registry implementation. `[INHERITED: epic Item 2 scope]`
- **MR-4**: `Source` must resolve to a repo file path (`modeling_project/REQUIREMENTS.md`).
- **Holdout in code**: URL/title checks before capture AND content checks before any registry write (`knowledge/holdout/aries-cs/PROTOCOL.md`); a PreToolUse hook will not see a curl inside a script, so the blocklist must be enforced by the operation itself.
- **WebFetch output is triage-only** and never cited as source content.
- **The existing research approval gate stays** (owner approves research docs/insights).
- **Pinned upstream**: `agentic-mbse` is pinned by SHA (`tests/test_dependency_provenance.py`); any needed change there is an upstream filing, not an in-repo edit. The capture primitive is `agentic-mbse extract <url|pdf> --save-source` as-is.
- **Out of scope** (epic): insight supersession / impact propagation, paywall bypass, Zotero redesign, cross-concept source sharing, automated research approval, goal-layer routing/dispatch, shadow research state.
- **Testing**: live network acquisition proof belongs to epic Item 5. This item's tests use fixtures and local files where possible; a duplicate, a rollback, a barred write, and a bounded negative must each be testable without the network. Follow the project's integration-seam testing preference (failure chains across boundaries, not isolated happy paths).
- **Parallel work**: Item 1 (goal contract/runbook) runs concurrently on another branch and owns CLAUDE.md, the run-study runbook, DISCOVERY_LOG, GOAL_RUNBOOK, and the ADR home. Do not touch those files; cite the epic, not Item 1's in-flight artifacts.

## Required reading (from the epic, plus)

- `.project/backlog/epic_goal_strategy_task_harness.md` § Item 2 (the contract)
- `.project/research/20260822-120756_research-extraction-harness.md` (evidence base; §4 gaps, §5 patterns)
- `.project/concepts/goal-strategy-task-harness-design.md` § Native seams (the seam table row for `research`)
- `.project/concepts/goal-driven-model-development-harness.md` § Research stage, § Success Criteria 4
- `scripts/zotero_ingest.py`, `scripts/zotero_lib.py` (writer to extend; manifest identity today)
- `exploration/concept_analysis/scripts/lib/research.py` + `exploration/concept_analysis/prompt_templates/research.md` (acquisition protocol referent)
- `modeling_project/REQUIREMENTS.md` MR-4; `knowledge/holdout/aries-cs/PROTOCOL.md`
- `knowledge/SOURCE_INDEX.md:190-218` — the two hand-written WI-031 entries; the referent `[REFERENT]` for what a good index block contains (per the research doc)

## What the spec should decide vs defer

Decide: requirement set with acceptance criteria for the four scope areas (contract, registration op, acquisition mode, safety/negatives); the request/return field set at requirement level; what "durable bounded negative" must record; testable success criteria mapping to the epic's six checkboxes.
Defer to design: manifest identity mechanism, where the entry surface lives (command vs skill vs script), file formats/paths of request-return artifacts, holdout content-scan mechanics, rollback implementation.

Write `spec.md` at `.project/active/goal-research-seam/spec.md`. End with `ARTIFACT: <path>`.
