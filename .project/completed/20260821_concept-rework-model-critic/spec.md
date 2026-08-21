# Spec: `model_critic` Standalone Tool

**Status:** Draft
**Owner:** reid
**Created:** 2026-05-31
**Complexity:** LOW
**Branch:** concept-analysis-rework
**Epic:** [CONCEPT-REWORK](../../backlog/epic_concept_analysis_rework.md) — Item 9

---

## Work Item Summary

Productionize the Phase 0 prototype critic into a standalone tool — `model_critic` — that can be invoked by name against any concept directory (active or archived) at any time, with no dependency on pipeline loop state. It reads the concept's artifacts (`analysis.md`, `model_setup.py`, model output) **plus the pre-computed outputs of the Item 5 and Item 7 deterministic checks** (design-point coherence flags, override-count-vs-fit-grade flag, model-setup contract flags, per-account comparables outlier flags), reasons through a fixed spine focused on the new pipeline contract (design-point coherence, override discipline, two-knob projection), and writes one review document next to the artifacts. The deterministic flags are pre-computed fixed inputs the critic reasons *on top of* — not problems it has to re-derive cold; its value-add is the judgment layer, not the structural detection. Downstream use of the review document is the reviewer's call — the critic does not feed back into the loop automatically.

## Why This Matters Now

Today the critic only runs in-loop (`assess`, `review`), entangled with loop state — it cannot be applied to archived concepts and gates on pipeline phase. The rework's accountability story rests on independent review being available *on demand*, against *any* concept, at *any* time. Item 1 cleared the critic-acuity bet (caught the operator's real `P_native` mismatch cold) and saved a hand-drafted prompt as the content starting point; Item 5 ships the upstream tables the critic reads as fixed metadata. Both gates are now passed, so this item turns the prototype into a tool. It also needs to land before Item 10 (pilot regeneration) so reviewers can use it on the pilot artifacts before bulk rollout.

## Key Bets / Constraints

- **Bet:** the Phase 0 critic prompt, *reshaped* (not copied) to add the artifact-vs-source scope boundary, aligned with the post-2026-05-31 selection/extraction split, and **rebuilt around pre-computed deterministic flags as fixed inputs** (per Item 7 design line 84: validators were built precisely so the critic consumes their outputs), will produce stronger output than the prototype — deterministic detection where it's available, judgment reasoning on top.
- **Constraint:** the critic MUST read everything from the concept directory plus upstream tables and pre-computed check outputs — never from runtime loop state, intermediate iteration files, or session memory.
- **Constraint:** "archived concept" means: `analyses/{cid}/` still exists with `analysis.md` and `model_setup.py`, but the loop's iteration state (`iter-*/` subdirectories under the concept) is absent. An archived concept must run identically to an active one. (No physical archive directory exists or is created by this work; archival is the *absence* of iteration state, not relocation.)
- **Constraint:** the critic writes exactly one document and nothing else; no side effects on iteration state, no feedback-loop injection, no validator state changes.
- **Non-goal:** wiring the critic into the loop or any automated trigger (it is on-demand by design — that is the whole point of standalone).
- **Non-goal:** freeform concepts (`fit_grade=None` or no-`P_native` route) — those don't have the three-forward `model_setup.py` shape the reasoning spine assumes.
- **Non-goal:** modifying or extending the existing in-loop `assess` / `review` stages.

---

## Business Goals

### Why This Matters

The rework's accountability layer depends on three things being independently checkable: (1) does this `analysis.md` describe one coherent named plant; (2) are the overrides honest provenance not dressed-up library defaults; (3) does `result_1gw` come from the standardized two-knob call. None of those are mechanical validator checks — they need a reasoning agent reading the artifacts cold. `model_critic` is that agent, decoupled from the loop so it stays available against any concept the reviewer wants to scrutinize — fresh pilot output, archived concept under suspicion, neighbor of one that turned out wrong.

### Success Criteria

- [ ] Reviewer can run `model_critic <concept-id>` against an active concept and get a review doc next to its artifacts.
- [ ] Reviewer can run the same command against an archived concept (loop state long gone) and get an equivalent review doc.
- [ ] The review surfaces issues a careful reviewer would have caught — not boilerplate; Phase 0 critic acuity is preserved.
- [ ] Critic output respects the artifact-vs-source scope boundary (no out-of-scope sourcing critiques an artifact-only reviewer can't act on).

### Priority

P0 — blocks Item 10 (pilot regeneration), which needs the critic on hand to review pilot concepts before bulk rollout.

---

## Problem Statement

### Current State

The existing review/assess stages (`prompt_templates/review.md`, `prompt_templates/assessment.md`) run inside `loop.py` against iteration-numbered artifacts. They depend on loop state files, can't run against archived concepts (those iteration files are gone), and were built against the old free-form pipeline contract — not the rework's design-point + override-registry + two-knob shape. The Phase 0 hand-drafted prompt (`/.project/active/concept-rework-prototype/prompts/model_critic.md`) is the right content starting point — it walks the right reasoning spine for the new contract and demonstrated acuity in Item 1 — but is a one-shot document run manually with `claude -p`, not an installed tool.

### Desired Outcome

A new standalone script — `scripts/agents/model_critic.py` — invokable via `run_analysis.py model_critic <concept-id>` that reads the concept directory plus upstream tables, calls Claude with a productionized version of the Phase 0 prompt, and writes one review document next to the artifacts. Works identically on active and archived concepts.

---

## Scope

### In Scope

- New script `exploration/concept_analysis/scripts/agents/model_critic.py` — invocation entry point. Loads concept artifacts, loads upstream-table rows (archetype-fit grade, comparables) for the concept, renders the prompt, calls Claude, writes output.
- New prompt template `exploration/concept_analysis/prompt_templates/model_critic.md` — productionized from the Phase 0 draft, with the two reshape obligations applied (see "Reshape obligations" below).
- New subcommand on `exploration/concept_analysis/scripts/run_analysis.py` — `model_critic <concept-id>` (single concept; batching is not in scope but the script structure should not preclude it).
- Output document written to the concept directory (active: `analyses/{cid}/`; archived: same — the critic doesn't care which it is).
- Tests covering: archived-concept invocation, missing-artifact handling, output document shape.

### Out of Scope

- Wiring into `loop.py` or any automated trigger.
- Batch invocation across many concepts (single-concept is sufficient for Item 10's pilot needs; batch can be added later if reviewers want it).
- Freeform concepts — the reasoning spine assumes the costingfe three-forward `model_setup.py` shape; freeform concepts don't have that.
- Critic-driven feedback injection into the loop (deferred — reviewer manually feeds back via existing mechanism if they want).
- Modifying the existing in-loop `assess` / `review` stages.
- A "fix this" mode — the critic surfaces issues; it doesn't edit artifacts.

### Edge Cases & Considerations

- **Archived concept with no `model_setup.py`** (early concepts that predate the rework): script should exit with a clear error, not crash. The critic's reasoning spine assumes the new contract; pre-rework artifacts aren't its job.
- **Concept where `model_setup.py` exists but won't import** (broken Python, or archived against a library version that has since moved): the critic falls back to the static `model_output.txt` for per-account values and surfaces the import failure as a headline issue. The point is to find problems, not to require a green-path environment.
- **Live-import vs. static-read policy.** On a happy-path active concept, the critic imports `model_setup.py` to get the live `generic` / `native` / `result_1gw` objects (needed for `sanity_check_comparables.py`'s per-account computation, and to verify the two-knob call shape against the current library). On any concept where import fails, it falls back to the static `model_output.txt` snapshot. For archived concepts the import path may succeed but recompute against *today's* library (not the library version that produced the artifact); when the critic detects a non-trivial drift between recomputed `result_1gw` and `model_output.txt`, that drift becomes a headline flag — the critic must not silently substitute today's numbers for the artifact's record. ("Non-trivial" threshold is a design call.)
- **Routing-based refusal** (use Item 6's predicate, don't re-implement): the critic determines runnability via `lib/concepts.get_comparison_status(record)`. Refuse cleanly on `freeform-deferred` ("this concept is architecturally freeform; `model_critic` doesn't apply"). Also refuse on `pending-design-point` with a *different* message ("design-point row not yet populated for this concept; run after Item 5 batch completes") — these two states feel adjacent but are different problems and must not be conflated (this is the bug Item 6's four-state routing was built to avoid). Both `costingfe` and `costingfe-asterisked` are runnable.
- **Re-running against the same concept**: re-running is the expected workflow (review → fix issue → re-run → see whether the fix landed). Overwriting destroys the prior review the analyst was working against. Spec leans toward versioned output (timestamped or sequence-numbered alongside a `critic_review_latest.md` symlink or convention); exact mechanism is a design call but overwrite-only is rejected.
- **Concept directory missing entirely**: hard error.
- **Claude call fails / hits API error**: surface the failure, do not write a partial review document.

---

## Reshape Obligations (from Phase 0)

The Item 1 hand-drafted critic prompt at `/.project/active/concept-rework-prototype/prompts/model_critic.md` is the *content* starting point — not the structural starting point. Two reshape obligations are carried forward from the Item 1 self-review note:

1. **Artifact-vs-source scope boundary.** Phase 0 surfaced an out-of-scope sourcing critique that wasn't actionable from the artifacts alone. The productionized prompt must explicitly scope the review to the artifacts (`analysis.md`, `model_setup.py`, model output) plus the upstream-table inputs, and instruct the agent NOT to second-guess source selection or quality — the dossier is the upstream layer's responsibility, and source-quality concerns belong in `research`-stage review, not here.
2. **Selection/extraction split alignment.** The Phase 0 prompt predates the design-point-selection-upfront decision. The productionized prompt must treat the design-point *selection* (named plant, `P_native`, sources) as a fixed input from the upstream design-point table — flag *coherence* breaks between table row / analysis.md / model_setup.py (Phase 0 showed this is a real failure mode), not re-debate which plant should have been picked.

---

## Requirement Selection Notes

The functional requirements below cover the contract (standalone invocation, artifact-only inputs, single output document), the two reshape obligations, and — load-bearing — the requirement that the critic *consume* the Item 5 and Item 7 deterministic checks as pre-computed fixed inputs rather than re-derive them. Per Item 7's design, those validators were built specifically as inputs to `model_critic`; under-using them weakens the rework's reliability story (the `P_native` mismatch Phase 0 caught by reasoning is caught deterministically every time by `validate_design_point_coherence` — the critic should reason on top of that flag, not race it). Internal Python structure, output filename convention, drift-detection threshold, and CLI ergonomics remain design calls.

---

## Requirements

### Functional Requirements

1. **FR-1**: `model_critic` MUST be invokable by name (via `run_analysis.py model_critic <concept-id>`) and MUST NOT depend on pipeline loop state, iteration-numbered files, or session/memory state. All inputs come from the concept directory, the upstream tables (`archetype_fit.csv`, `comparables.csv`, `design_point.csv`), and the pre-computed deterministic checks listed in FR-6b.
2. **FR-2**: `model_critic` MUST run identically against active and archived concepts. "Archived" is defined as: `analyses/{cid}/` retains `analysis.md` and `model_setup.py` but the loop's iteration state (`iter-*/` subdirectories) is absent. The test for FR-2 is: delete the `iter-*/` dirs of a passing active-concept run and re-invoke — output structure must be equivalent.
3. **FR-3**: `model_critic` MUST write exactly one review document per invocation, and MUST NOT write a partial or empty document on failure. Re-invocation against the same concept MUST NOT destroy the prior review document; output naming MUST support multiple reviews coexisting (versioned, timestamped, or equivalent — design call).
4. **FR-4**: `model_critic` MUST NOT modify any other artifact, MUST NOT inject into any loop feedback mechanism, and MUST NOT mutate iteration state.
5. **FR-5**: The prompt template MUST be the productionized successor to the Phase 0 draft (`/.project/active/concept-rework-prototype/prompts/model_critic.md`), with the two reshape obligations applied: (a) artifact-vs-source scope boundary explicit in the prompt; (b) design-point *selection* treated as a fixed upstream-table input, with coherence (table ↔ analysis.md ↔ model_setup.py) checked rather than selection re-debated.
6. **FR-6**: The prompt MUST inject upstream-table values (archetype-fit grade, comparables list, design-point row) as fixed inputs rather than asking the agent to look them up.
7. **FR-6b** *(load-bearing — see Requirement Selection Notes)*: The prompt MUST inject the pre-computed outputs of the following deterministic checks as fixed inputs, and the prompt MUST instruct the agent to reason *on top of* these flags rather than re-derive them:
   - `validators.validate_design_point_coherence` (Item 7) — the table ↔ `analysis.md` ↔ `model_setup.py` `P_native` and override-`provenance` coherence flags.
   - `validators.check_override_count_vs_fit_grade` (Item 7) — the override-count-vs-fit-grade flag.
   - `validators.validate_model_setup_contract` (Item 7) — the module-level-attributes and two-knob-call-shape structural flags.
   - `sanity_check_comparables.sanity_check(concept_id)` (Item 5) — the per-account outlier flags computed against the concept's comparables and `result_1gw`.

   Each check's full structured result (flag + supporting detail) is injected; the prompt does not summarize them before the agent sees them. If any check fails to run (e.g., import error), the failure mode itself is injected in place of the result so the agent knows what is and isn't covered deterministically.
8. **FR-7**: Runnability is decided by `lib/concepts.get_comparison_status(record)`. The critic runs on `costingfe` and `costingfe-asterisked`. It MUST refuse with distinct, state-specific messages on:
   - `freeform-deferred` — "this concept is architecturally freeform; `model_critic` doesn't apply"
   - `pending-design-point` — "design-point row not yet populated for this concept; populate via Item 5 batch and re-run"

   The critic MUST NOT re-implement the freeform-vs-pending test (that was Item 6's bug to fix; reusing the predicate preserves the four-state distinction).
9. **FR-8**: For the live `generic` / `native` / `result_1gw` objects, the critic SHOULD import `model_setup.py` (needed by FR-6b's `sanity_check_comparables` call and by the two-knob-shape verification). If import fails for any reason, the critic MUST fall back to the static `model_output.txt` and surface the import failure as a headline issue rather than crashing. When import succeeds against an archived concept, the critic MUST detect non-trivial drift between the recomputed `result_1gw` and the static `model_output.txt` (the artifact's record) and surface that drift as a headline flag — the critic MUST NOT silently substitute today's recomputation for the artifact's original numbers. (Drift threshold and exact comparison surface are design calls.)
10. **FR-9**: The critic's output document MUST follow the structure demonstrated in the Phase 0 draft: headline issues (1–5, brutally specific, cited by line/file where possible) at the top; detailed reasoning per spine step below; an explicit "what I deliberately did not say" section for half-formed concerns the agent can't back up from the artifacts.

### Non-Functional Requirements

- Should run in well under a minute on a single concept (modulo Claude API latency); no expensive pre-processing.
- Output document should be readable in 10 minutes by a triaging analyst (the Phase 0 prompt's stated audience target).

---

## Acceptance Criteria

### Core Functionality

- [ ] `uv run python exploration/concept_analysis/scripts/run_analysis.py model_critic <cid>` produces one review document next to the concept's artifacts.
- [ ] The same command run after deleting the concept's `iter-*/` subdirectories (the archived-concept simulation per FR-2) produces an equivalent review document.
- [ ] Re-running against the same concept does not destroy the prior review document; both reviews coexist on disk.
- [ ] Running against a `freeform-deferred` concept exits with the freeform-specific message and writes nothing.
- [ ] Running against a `pending-design-point` concept exits with the pending-specific message (distinct from the freeform message) and writes nothing.
- [ ] Running against a non-existent concept ID errors clearly.
- [ ] A Claude API failure during invocation surfaces the error and writes no partial review document.
- [ ] The rendered prompt contains the structured outputs of all four FR-6b checks (verifiable by dry-run print).

### Quality & Integration

- [ ] Tests cover: archived-concept (iter-*/-deleted) happy path; `freeform-deferred` refusal; `pending-design-point` refusal (distinct message); broken-`model_setup.py` graceful review with import-failure headline; FR-6b deterministic-flag injection (the rendered prompt contains each check's result); FR-8 drift-flag emission when archived recomputation diverges from `model_output.txt`.
- [ ] Existing tests in `exploration/concept_analysis/scripts/` continue to pass.
- [ ] Manual spot-check on one pilot concept: critic surfaces at least one substantive judgment-shaped issue (not just restating the deterministic flags) or, if it finds none, explicitly says so per the prompt instruction.

---

## Next-Stage Handoff

**Settled in this spec:**
- Standalone tool, on-demand, no loop wiring (FR-1, FR-4, non-goal).
- Multi-review-per-concept; no overwrite (FR-3).
- "Archived" defined as `iter-*/` absent under `analyses/{cid}/` (FR-2 constraint + test).
- Inputs are artifacts + upstream tables + pre-computed deterministic checks; no dossier-quality second-guessing (FR-5a, FR-6, FR-6b).
- Selection is fixed input from the upstream table; coherence-not-selection is what gets checked (FR-5b).
- Runnability decision uses `get_comparison_status` (FR-7); freeform and pending-design-point produce distinct refusal messages.
- Live-import preferred; static-`model_output.txt` fallback on import failure; archived-recomputation drift becomes a headline flag (FR-8).
- Critic *consumes* Item 5 + Item 7 checks rather than re-deriving them; its value-add is judgment on top (FR-6b, Requirement Selection Notes).

**Design must figure out:**
- Module layout: does `scripts/agents/model_critic.py` orchestrate end-to-end, or split into a loader (`lib/`) + agent (`agents/`)? Look at existing pipeline-stage script conventions before picking.
- Output naming scheme that satisfies FR-3's no-destroy requirement (timestamped? sequence-numbered? `critic_review_YYYYMMDD-HHMMSS.md` + a `critic_review_latest.md` convention?).
- Drift threshold for FR-8 — what fractional `result_1gw` change between live re-import and static `model_output.txt` counts as "non-trivial" and triggers the headline flag. Pick a defensible default; expose as a constant.
- Prompt template structure: how to inject the upstream-table values *and* the four FR-6b deterministic check results cleanly (template variables vs. composed sections vs. a single structured-inputs block). Should be consistent with how `analysis_v2.md` consumes the design-point row in Item 8.
- Exactly how each check's result is serialized into the prompt (`ValidationResult` is structured; `sanity_check_comparables.sanity_check()` returns a dict — the prompt rendering needs a uniform shape the agent reads consistently).
- Whether to expose a `--dry-run` mode (consistent with other `run_analysis.py` subcommands) and what it would print — most useful for verifying FR-6b injection without burning a Claude call.
- How the broken-`model_setup.py` path actually surfaces the import error to the agent (raw exception text in the prompt? a synthesized "this file does not import" preamble?).

**Watch-outs for design:**
- The prompt is the load-bearing piece of this item, not the Python wiring. Spend the design budget on the prompt reshape (the two scope boundaries) and the FR-6b injection layout, not on script ergonomics.
- The Phase 0 prototype is the reference baseline for *reasoning quality*; the productionized prompt is structurally different (it now reasons on top of deterministic flags instead of re-deriving them), so don't expect the prompts to look alike — expect output quality to *exceed* the prototype because the deterministic flags backstop the LLM.
- The FR-6b injection makes parts of the Phase 0 reasoning spine (e.g., the manual `P_native` coherence walk in step 1) redundant. The prompt should explicitly redirect the agent at those steps to "the deterministic check already covers this — your job is to reason about *what it means* if a flag fired, not to re-check the flag."
- `sanity_check_comparables.sanity_check()` already returns per-account outlier flags structured for an LLM reviewer — that's its documented purpose. Don't re-compute or paraphrase; pass through.

---

## Related Artifacts

- **Epic:** [`.project/backlog/epic_concept_analysis_rework.md`](../../backlog/epic_concept_analysis_rework.md) — Item 9.
- **Design doc:** [`.project/concepts/concept-analysis-rework-design.md`](../../concepts/concept-analysis-rework-design.md) — see §`model_critic` and §Pipeline invariants.
- **Phase 0 prototype prompt:** [`.project/active/concept-rework-prototype/prompts/model_critic.md`](../concept-rework-prototype/prompts/model_critic.md) — content starting point; reshape obligations apply.
- **Phase 0 findings:** [`.project/active/concept-rework-prototype/findings.md`](../concept-rework-prototype/findings.md) — bet #5 (critic acuity) verdict + the "scope boundary" self-review note.
- **Item 7 validators consumed (FR-6b):** `exploration/concept_analysis/scripts/lib/validators.py` — `validate_design_point_coherence`, `check_override_count_vs_fit_grade`, `validate_model_setup_contract`.
- **Item 5 sanity-check consumed (FR-6b):** `exploration/concept_analysis/scripts/sanity_check_comparables.py` — `sanity_check(concept_id)`.
- **Item 6 routing predicate (FR-7):** `exploration/concept_analysis/scripts/lib/concepts.py` — `get_comparison_status(record)`.
- **Design:** `.project/active/concept-rework-model-critic/design.md` (to be created)

---

**Next Steps:** After approval, proceed to `/_my_design`.
