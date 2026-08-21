# Spec: Portfolio-Audit Stage

**Status:** Implemented
**Owner:** Reid W
**Created:** 2026-06-07
**Complexity:** MEDIUM
**Branch:** feat/portfolio-audit-stage

---

## Work Item Summary

A new pipeline stage, `portfolio-audit`, that runs an Opus-driven reviewer over a cohort of concepts in their **post-assess** state and produces a cross-concept physics / first-principles sanity check. Today the pipeline checks each concept in isolation; this stage checks whether the answers across concepts hang together — family-internal coherence, cross-family magnitude ordering, source traceability on dominant cost drivers, and sensitivity behavior under perturbation. Output lands under a new `exploration/concept_analysis/reviews/<timestamp>/` location and consists of a state manifest, a main cross-concept report, and per-concept audit docs for concepts the reviewer flags as suspect.

## Why This Matters Now

Per-concept `assess` can pass every concept individually while the portfolio still makes no physical sense — wrong family ordering, an outlier that looks defensible in isolation but is indefensible against its neighbours, sensitivities that are locally smooth but globally suspect. There is currently no stage whose job is to reason about the cohort as a whole, and synthesis is the wrong vehicle (it is editorial, per-concept, and frequently stale). Without this, downstream consumers of the LCOE numbers have no audit trail demonstrating the cross-concept results are internally coherent.

## Key Bets / Constraints

- **Bet:** A capable reviewer (Opus) given the right cross-concept digest can spot family-internal and cross-family incoherence that no per-concept stage can. The agent is trusted to direct its own investigation rather than executing a pre-scripted set of checks.
- **Bet:** The agent should be able to interact with each concept's `model_setup.py` directly (import it, perturb inputs, re-run) rather than being limited to whatever sensitivity output was already serialized.
- **Constraint:** This stage MUST NOT depend on `synthesis.md` or `review.md` — both are downstream of assess and may be stale, missing, or contradicted by a later iter.
- **Constraint:** This stage is advisory. It does NOT gate `approve` and does NOT mutate any concept's artifacts.
- **Constraint:** The audit is per-cohort and immutable once written: a run folder records what state was audited (via the manifest), and future runs create new timestamped folders rather than overwriting.
- **Non-goal:** Auto-routing findings back into individual concepts' `analyze --feedback` queues. Findings are emitted in a form that's consumable by a human triaging which concepts to kick back, but the routing itself is out of scope.
- **Non-goal:** A per-concept local physics-audit stage (option C from scoping). Only the portfolio-level stage.
- **Non-goal:** Any change to existing stages (`analyze`, `model-setup`, `assess`, `review`, `synthesize`, `approve`).

---

## Business Goals

### Why This Matters

Today the pipeline produces N independently-audited concept analyses, but nothing ever asks "do they make sense together?" The user has identified this as a real gap: families where the numbers should cluster don't, magnitudes that should be ordered by physics aren't, and outliers slip through because per-concept assess only sees the concept it's looking at. Fixing this is the difference between a portfolio that's defensible to an external reviewer and one that is only defensible concept-by-concept.

### Success Criteria

- [ ] After a run, the main report either gives confidence the portfolio is coherent, or names specific concepts and specific numbers to look at, with reasoning.
- [ ] Per-concept audit docs for flagged concepts cite the specific LCOE values, override entries, or source claims that drove the flag — traceable enough that a human can act on them.
- [ ] The state manifest is rich enough that, given two run folders, a human (or future tooling) can tell which concepts changed between runs.
- [ ] The stage is re-runnable cheaply: it does not require any other stage to be re-run as a precondition.

### Priority

P1. Closes a real gap, but unblocks no other in-flight work. Should land before any external presentation of LCOE results.

---

## Problem Statement

### Current State

- `assess` (per concept) checks design-point coherence, override discipline, override-count vs. archetype-fit grade, and a *local* numerical sanity check (`sanity_check_comparables.py`) that compares per-account `result_1gw` against the median of a hand-picked comparables list with a 2×/0.5× threshold.
- `review` (per concept) is a strategic quality review of one concept's artifacts.
- `synthesize` (per concept) is editorial; it is not a sanity check, and it is frequently stale relative to the latest iter.
- Nothing in the pipeline reasons across the full cohort. Nothing applies first-principles reasoning to the headline LCOE numbers. Nothing exercises the models' sensitivities to ask "is this robust?"

### Desired Outcome

A new `portfolio-audit` command that:
- Operates on a user-selected cohort of concepts in their post-assess state.
- Builds a structured cross-concept digest (so Opus can fit the cohort in context).
- Hands the digest to Opus with criteria-driven prompting, and lets Opus direct its own investigation — including importing concepts' `model_setup.py` to perturb inputs and re-run when it wants to.
- Produces a timestamped run folder with a manifest, a main report, and per-concept audit docs for any concept the reviewer flagged as suspect — all in a single command, with no human stop in between.

---

## Scope

### In Scope

- New CLI subcommand `portfolio-audit` under `exploration/concept_analysis/scripts/run_analysis.py`, following the same concept-selection conventions as every other command (numeric prefix, full ID, partial name, `--all`, `--family`).
- A `--passed-only` flag that restricts the cohort to concepts whose latest iter recorded `verdict: PASS`.
- Inputs per concept (read-only): `analysis.md`, `model_setup.py`, `model_output.txt`, latest `iter-N/verdict.json`, and source paths.
- Construction of a cross-concept digest suitable for an Opus context window.
- Opus-driven main pass producing a cross-concept report; same command produces per-concept audit docs for concepts the main pass flagged.
- Output directory: `exploration/concept_analysis/reviews/<timestamp>/` with `manifest.json`, `report.md`, and `concepts/<concept-id>.md` for each flagged concept.
- State manifest containing, per concept: iteration count, last-iter timestamp, SHA of `analysis.md`, SHA of `model_setup.py`, SHA of `model_output.txt`, and the sources list.

### Out of Scope

- Any read of, dependency on, or write to `synthesis.md`, `review.md`, or `address_log.md`.
- Auto-routing flagged findings back into `analyze --feedback` for individual concepts.
- Hard gating on `approve` or any other stage.
- A per-concept local physics-audit (option C from scoping).
- Changes to any existing stage's behavior or outputs.
- A UI for browsing run folders (filesystem only for v1).

### Edge Cases & Considerations

- A concept selected for the cohort whose `model_setup.py` is missing or import-fails — stage must handle without crashing the whole run.
- A cohort small enough (e.g., 2 concepts) that "cross-concept" reasoning is degenerate — should still produce a report, even if mostly a no-op.
- A re-run very shortly after a prior run with no concept changes — allowed; produces a new timestamped folder; deduplication is out of scope for v1.
- Reviewer wants to import a `model_setup.py` whose runtime errors at import time — agent must be able to see and reason about the failure, not have it silently swallowed.
- Concepts in mixed verdict states (some PASS, some FAIL) in the same cohort — allowed by default; `--passed-only` is the user's opt-in to filter.

---

## Requirement Selection Notes

Requirements below capture decisions that are firm: where outputs go, what the manifest must contain, what's read vs. not read, that the stage is advisory and single-command. Design decisions intentionally deferred: the exact shape of the cross-concept digest, the prompt and criteria handed to Opus, the mechanism by which the agent invokes `model_setup.py` (subprocess vs. tool call vs. import), how main-pass and per-concept-pass work is parallelized, and the per-concept "suspect" criteria themselves (which will be tuned over time).

---

## Requirements

### Functional Requirements

1. **FR-1**: The stage SHALL be invoked as a new subcommand `portfolio-audit` under `run_analysis.py`.
2. **FR-2**: The stage SHALL accept the same concept-selection conventions as existing commands (numeric prefix, full ID, partial name, `--all`, `--family`).
3. **FR-3**: The stage SHALL accept a `--passed-only` flag that restricts the cohort to concepts whose latest `iter-N/verdict.json` records `verdict: PASS`.
4. **FR-4**: The stage MUST NOT read, depend on, or be blocked by `synthesis.md`, `review.md`, or `address_log.md`.
5. **FR-5**: The stage SHALL write output to `exploration/concept_analysis/reviews/<timestamp>/`, where `<timestamp>` is a sortable timestamp generated at run start.
6. **FR-6**: Each run folder SHALL contain a `manifest.json` recording, per concept in the cohort: iteration count, last-iter timestamp, SHA of `analysis.md`, SHA of `model_setup.py`, SHA of `model_output.txt`, and the sources list. Plus run-level metadata: timestamp, CLI invocation, model used, and the cohort selection.
7. **FR-7**: Each run folder SHALL contain a `report.md` produced by the main Opus pass covering family-internal coherence, cross-family magnitude reasoning, source-traceability spot-checks, and sensitivity reasoning.
8. **FR-8**: For each concept flagged as suspect by the main pass, the run folder SHALL contain a `concepts/<concept-id>.md` audit doc produced in the same command invocation. There is no human stop between the main pass and the per-concept passes.
9. **FR-9**: The reviewer agent MUST be able to interact with each concept's `model_setup.py` at its discretion (including importing and re-running with perturbed inputs) — not be limited to reasoning over pre-serialized model output.
10. **FR-10**: The stage SHALL NOT mutate any artifact outside `exploration/concept_analysis/reviews/<timestamp>/`.
11. **FR-11**: The stage SHALL NOT gate `approve` or any other existing stage.
12. **FR-12**: If a concept's `model_setup.py` is missing or fails to import, the stage SHALL record the failure in the manifest and continue rather than aborting the run.
13. **FR-13**: The reviewer agent SHALL use Opus.

### Non-Functional Requirements

- The cohort digest SHOULD be designed so that the typical full-cohort run (~30 concepts) fits in a single Opus context window with room for the agent's working tokens.
- The stage SHOULD support parallelizing per-concept audit passes once the main pass has identified suspects.

---

## Acceptance Criteria

### Core Functionality

- [ ] `portfolio-audit` runs end-to-end on a single concept and produces `manifest.json`, `report.md`, and (if flagged) a per-concept doc in the run folder.
- [ ] `portfolio-audit --all --passed-only` runs over the full PASS cohort and produces a coherent main report plus per-concept docs for every flagged concept, in one command invocation with no intermediate human prompts.
- [ ] `manifest.json` round-trips: re-running with no concept changes between runs produces two manifests with identical per-concept SHA fields.
- [ ] A concept with a broken `model_setup.py` is recorded in `manifest.json` with the failure noted and does not abort the run.
- [ ] No file outside `exploration/concept_analysis/reviews/<timestamp>/` is touched by the run.

### Quality & Integration

- [ ] Existing tests continue to pass.
- [ ] No existing stage's outputs or CLI surface change.
- [ ] The new command appears in the dispatch table in `run_analysis.py` and follows existing flag conventions (`--model`, `--dry-run`, `--timeout`).

---

## Next-Stage Handoff

**Settled in this spec:**
- The stage exists as `portfolio-audit` and is advisory, single-command, non-mutating outside its run folder.
- Output location and the per-concept manifest schema.
- What's read (post-assess artifacts only) and what's NOT read (synthesis, review).
- The reviewer is Opus, can interact with `model_setup.py` directly, and is trusted to direct its own investigation under criteria-guided prompting.
- Per-concept docs are produced in the same command as the main report — no human stop between.

**Design must figure out:**
- The shape of the cross-concept digest fed to Opus (which fields, what level of abstraction per concept, how the LCOE table is summarized) — must satisfy the context-engineering bet.
- The exact prompt and the criteria given to the reviewer for flagging suspects (criteria-guided, agent-discretion; tunable over time).
- The mechanism by which the agent invokes `model_setup.py` for live perturbation (tool call, subprocess, sandboxed import).
- Parallelization strategy for per-concept passes after the main pass identifies suspects.
- How findings in `report.md` reference per-concept docs (cross-linking convention).
- Whether the digest builder reuses anything from `sanity_check_comparables.py` or `critic_inputs.py` or is built fresh.

**Watch-outs for design:**
- Context-window pressure: full-cohort prose won't fit. The digest is the load-bearing piece.
- Live `model_setup.py` invocation is the riskiest surface — design must specify isolation, timeout, and what happens when perturbed inputs produce nonsense or runtime errors.
- Single-command-no-stop means the main pass's flagged-concept list is the contract feeding per-concept passes — its format needs to be machine-parseable, not just prose.
- Per-concept "suspect" threshold lives in the prompt/criteria, not in code — design needs a clear story for where to put it so it can be tuned without touching Python.

---

## Related Artifacts

- **Pipeline overview:** `exploration/concept_analysis/README.md`
- **Existing local sanity check:** `exploration/concept_analysis/scripts/sanity_check_comparables.py`
- **Existing per-concept critic:** `exploration/concept_analysis/prompt_templates/model_critic.md`
- **Design:** `.project/active/portfolio-audit-stage/design.md` (to be created)

---

**Next Steps:** After approval, proceed to `/_my_design`.
