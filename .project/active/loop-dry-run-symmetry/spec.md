# Spec: `_run_model_in_iteration` dry-run prompt symmetry

**Status:** Draft
**Owner:** Reid W
**Created:** 2026-04-10 09:01 PDT
**Complexity:** LOW
**Branch:** design-space-explore (parent); fix branch TBD

---

## Business Goals

### Why This Matters

Operator debuggability. `--dry-run` exists so operators can inspect what the pipeline *would* send to Claude before committing to a real, billable, multi-minute invocation. After the Phase 4 pipeline-hardening migration, two of the three Claude call sites in `lib/loop.py` write their fully-filled prompt to disk under dry-run (`analyze_prompt.md` for cold-start/feedback-pass, `assess_prompt.md` for assess), but the third — `_run_model_in_iteration` — does not. An operator inspecting a dry-run iter dir today sees only two of the three Claude prompts, silently.

This is not a correctness bug; the pipeline still behaves correctly. It is a *discoverability* gap that undermines the contract `--dry-run` implicitly offers ("show me every prompt you would send"). It also introduces an asymmetry in the three migrated sites that future readers of `loop.py` will notice and ask about — exactly as happened during the Phase 4 audit conversation on 2026-04-10.

### Success Criteria

- [ ] A decision is recorded about whether to keep or close the asymmetry. If kept, the reason is captured in `loop.py` as a code comment so the next reader does not have to re-derive it from the plan's deviation note.
- [ ] If closed: a dry-run on a fresh concept leaves `model_setup_prompt.md` in every iter dir alongside `analyze_prompt.md` and `assess_prompt.md`.
- [ ] Either way, the `(model_ran=False, model_ok=False)` return contract of `_run_model_in_iteration` is preserved under dry-run (the iteration loop depends on it).
- [ ] The dry-run console output remains informative (it currently prints `"dry-run {cid}: model-setup would run in {iter_dir}"`; any replacement must still tell the operator what did not run and where).

### Priority

Low urgency, low cost. This is follow-up polish for pipeline-hardening, not a bug fix. It should be scheduled after `pipeline-hardening` closes (Phase 5-7 complete) so the two work items don't conflict on the same files.

**Dependencies:**
- Blocks on: `.project/active/pipeline-hardening/` reaching at least Phase 5 completion (Phase 5 deletes the legacy `run_claude_step` surface; any fix here should land against the post-Phase-5 shape of `loop.py` to avoid merge churn).
- Blocked by: nothing else.

---

## Problem Statement

### Current State

In `exploration/concept_analysis/scripts/lib/loop.py`, three functions invoke Claude via `invoke_claude_validated` and were migrated in Phase 4 of `pipeline-hardening` to share the `prepare_step` pre-invocation helper:

1. **`_run_cold_start`** (`loop.py:326-394`) — calls `prepare_step(..., dry_run=args.dry_run)`. Under dry-run, `prepare_step` writes the prompt file to disk (by design, so operators can inspect it) and returns `StepContext(proceed=False, ...)`. `_run_cold_start` then returns `True` without invoking Claude.

2. **`_run_feedback_pass`** (`loop.py:397-461`) — same pattern, same behavior.

3. **`_run_model_in_iteration`** (`loop.py:484-561`) — has an *early return* at lines 500-502 that fires **before** `prepare_step` is called:
   ```python
   if args.dry_run:
       print(f"  dry-run {cid}: model-setup would run in {iter_dir}")
       return False, False
   ```
   Then, later in the function, `prepare_step` is called with a hard-coded `dry_run=False`. So under dry-run, the model-setup prompt is **never** written to disk and the operator has no artifact to inspect.

**Empirical evidence** (dry-run on `13-electrostatic-hybrid`, captured 2026-04-10 during Phase 4 audit):

```
iter-1/  analyze_prompt.md  assess_prompt.md  verdict.json
iter-2/  analyze_prompt.md  assess_prompt.md  verdict.json
iter-3/  analyze_prompt.md  assess_prompt.md  verdict.json
```

No `model_setup_prompt.md` in any iter dir. The three iter dirs each contain two of the three Claude prompts.

### Why The Phase 4 Implementation Left It This Way (Verbatim Rationale)

From `.project/active/pipeline-hardening/plan.md:1017` (Phase 4 Completion § Deviations):

> **`_run_model_in_iteration` keeps its early `dry_run` short-circuit.** The migration sketch in `design.md#migration-3-_run_model_in_iteration` calls `prepare_step` like the others, but `_run_model_in_iteration` had a pre-existing dry-run path that prints `dry-run {cid}: model-setup would run in {iter_dir}` (different message from `prepare_step`'s default) AND returns `(False, False)` so the iteration loop knows the model was not attempted. I preserved that early-return and pass `dry_run=False` to `prepare_step` to avoid printing two dry-run messages or changing the return-tuple semantics. The `prepare_step` indented label `"  model-setup"` matches the previous indent of the legacy `print`. Small but worth noting because this site does NOT follow the exact Migration-3 sketch in design.md.

**Summary of the original rationale's concerns:**

1. **Message-text drift:** The legacy message `"dry-run {cid}: model-setup would run in {iter_dir}"` is semantically distinct from `prepare_step`'s `"dry-run {cid}: model-setup prompt saved to {prompt_path}"`. Preserving the legacy message avoids changing operator-visible output.
2. **Double-print risk:** Routing through `prepare_step` with `dry_run=True` would print the `prepare_step`-default dry-run message, which — without additional suppression — could produce two dry-run messages for one call site if any legacy print path remained.
3. **Return-tuple semantics:** `_run_model_in_iteration` must return `(False, False)` (`model_ran=False, model_ok=False`) under dry-run so the iteration loop's verdict-tracking code (`loop.py:221-226`) correctly records that no model ran. Any refactor must preserve this.

The Phase 4 implementer judged (1) and (2) as sufficient reason to skip the `prepare_step` route, and (3) as the binding constraint that any future fix must honor.

### Desired Outcome

Either:
- **(A)** The asymmetry is consciously kept, with the rationale captured as a code comment in `loop.py` near the early return so the next reader does not have to grep the plan to understand why model-setup differs from cold-start/feedback-pass. **OR**
- **(B)** The asymmetry is closed: `_run_model_in_iteration` routes its dry-run path through `prepare_step` like the other two sites, writing `model_setup_prompt.md` to disk under dry-run, while preserving the `(False, False)` return contract and producing a single coherent console message.

The choice between (A) and (B) is the **first acceptance criterion** — it is a deliberate revisit of the Phase 4 rationale, not a foregone conclusion. If during design or implementation the reasons captured above still look binding, (A) is a valid and cheap outcome.

---

## Scope

### In Scope

- `exploration/concept_analysis/scripts/lib/loop.py` — specifically `_run_model_in_iteration`, lines 484-561.
- A revisit of the Phase 4 deviation rationale (above), with a written decision about whether it still holds.
- If the decision is to fix: the code change itself, plus any needed test adjustments in `test_failure_chains.py::TestIntegration_ModelSetup` and `test_prepare_step.py`.
- If the decision is to keep: a code comment in `loop.py` explaining why model-setup does not route through `prepare_step` under dry-run.
- One regression check under dry-run (on a real concept directory with no existing `analysis.md`) confirming the fix works or the asymmetry is documented in-code.

### Out of Scope

- Any changes to `_run_cold_start`, `_run_feedback_pass`, `_run_assess`, or `_run_source_integration`. All four are already symmetric.
- Any changes to non-dry-run behavior of `_run_model_in_iteration`.
- Any changes to `prepare_step` or `StepContext` in `lib/step_runner.py`. (If the fix needs a new parameter on `prepare_step`, flag this during design review — it would expand scope.)
- Any amendment to `.project/active/pipeline-hardening/plan.md` or `design.md`. This spec is standalone; pipeline-hardening stays frozen as a historical record of the Phase 4 deviation.
- Any live Claude CLI run. Dry-run is the only code path exercised.
- `cmd_model_setup` (the standalone, non-loop model setup command). It is a separate call site with separate semantics and is migrated by pipeline-hardening Phase 5, not here.

### Edge Cases & Considerations

- **Double-print risk (from original rationale):** Any fix that routes through `prepare_step(dry_run=True)` must ensure only one dry-run message is printed per call, not two. The simplest way is to remove the legacy early-return entirely and let `prepare_step` own the message. But that means the operator-visible message text changes from "would run in {iter_dir}" to "prompt saved to {prompt_path}" — a user-visible change that must be called out.
- **Return-tuple contract:** After `prepare_step` returns `proceed=False`, the function must return `(False, False)` — not `(True, False)` or anything else — so the iteration loop records `model_ran=False, model_ok=False` in `verdict.json`. This is the invariant the original deviation flagged as load-bearing.
- **`build_model_vars` may return `None`:** If the concept is missing `analysis.md`, `build_model_vars` returns `None` and `_run_model_in_iteration` returns `(False, False)` at `loop.py:508-509` — **before** the current dry-run early-return. Whatever replaces the dry-run early-return must stay *after* the `build_model_vars` None check, so dry-run does not bypass the "no analysis.md" detection.
- **`prepare_step` needs `out_dir` and `prompt_path`:** Under dry-run, `iter_dir` exists (created by the loop) and `prompt_path = iter_dir / "model_setup_prompt.md"` is a valid path. No new setup required.
- **Indentation of the label:** The current code passes `step_label="  model-setup"` (extra leading spaces) to match legacy indentation in the tail print. Any fix should keep this consistent with the current presentation, or explicitly decide to change it.
- **Phase 5 interaction:** Phase 5 of pipeline-hardening migrates the standalone `cmd_model_setup` (run_analysis.py) through `prepare_step`. The two sites share `build_model_vars` but are otherwise independent. This spec must not block on or conflict with Phase 5's changes to `cmd_model_setup`.

---

## Requirements

### Functional Requirements

> All requirements below are derived from the user-confirmed scoping on 2026-04-10. Marked [INFERRED] where they go beyond what was explicitly stated.

1. **FR-1 — Revisit the Phase 4 rationale.** The design phase (`/_my_design`) MUST begin by re-reading the Phase 4 deviation rationale (captured verbatim above) and producing a written recommendation: **keep** the asymmetry (Option A) or **close** it (Option B). The recommendation MUST name the specific reason(s) from the rationale that are still binding, or explain why each reason no longer applies.

2. **FR-2 — Decision recording.** The decision (A or B) MUST be recorded in this spec's Implementation Notes section (added during `/_my_design`) before any code is written. A design that proceeds straight to code without recording the A-vs-B decision does not satisfy this spec.

3. **FR-3 — If Option A (keep asymmetry):** `lib/loop.py` MUST gain a code comment adjacent to the early-return at lines 500-502 that:
   - States that the site deliberately does not route through `prepare_step` under dry-run.
   - Names the specific reason(s) (message-text drift, double-print risk, return-tuple contract — whichever still apply).
   - References this spec (`.project/active/loop-dry-run-symmetry/spec.md`) so a future reader can find the full rationale.

4. **FR-4 — If Option B (close asymmetry):** Under `args.dry_run=True`, `_run_model_in_iteration` MUST:
   - Write `iter_dir / "model_setup_prompt.md"` with the fully-filled model-setup prompt, so operators can inspect it.
   - Return `(False, False)` — exactly the same tuple it returns today under dry-run.
   - Print exactly one dry-run message to stdout (not two).
   - Run the `build_model_vars` check *before* the dry-run branch, preserving the current ordering (so dry-run still detects missing `analysis.md` via the `None` return).

5. **FR-5 [INFERRED] — Manual smoke verification.** After the fix lands (either A or B), the implementer MUST run `uv run python exploration/concept_analysis/scripts/run_analysis.py analyze <fresh-concept> --dry-run` on a concept with no existing `analysis.md`, confirm the expected artifacts are present (or absent, for Option A), clean up the dry-run artifacts (`iter-*/` dirs) from the concept directory, and record the result in Implementation Notes. The concept `13-electrostatic-hybrid` is a known-good target for this check (it was used during the Phase 4 audit on 2026-04-10).

6. **FR-6 [INFERRED] — Plan independence.** This work item MUST NOT modify `.project/active/pipeline-hardening/plan.md` or `.project/active/pipeline-hardening/design.md`. The Phase 4 deviation note stays intact as a historical record.

### Non-Functional Requirements

- **Non-regression of the iteration loop:** Verdict-tracking, model-ran flags, and all existing non-dry-run paths must remain identical. Full `exploration/concept_analysis/scripts/` pytest suite must remain green (modulo the 6 currently-red tests already scoped to pipeline-hardening Phase 5/6).

- **Respects pipeline-hardening scope boundaries:** Must land against `loop.py` in its post-pipeline-hardening shape (i.e., after at least Phase 5 of pipeline-hardening completes). Scheduling this before pipeline-hardening closes risks merge churn.

---

## Acceptance Criteria

### Decision Recording
- [ ] `/_my_design` produces a written Option-A-vs-Option-B recommendation that names each reason from the Phase 4 deviation rationale (message-text drift, double-print risk, return-tuple contract) and marks each as "still binding" or "no longer applies" with a one-line justification.
- [ ] The chosen option is recorded in this spec's Implementation Notes before any code is written.

### Option A (if chosen)
- [ ] `lib/loop.py` has a comment near the `_run_model_in_iteration` early-return explaining why the site deliberately bypasses `prepare_step` under dry-run.
- [ ] The comment references this spec file path.
- [ ] No behavioral change; no test changes required.

### Option B (if chosen)
- [ ] Under dry-run, `_run_model_in_iteration` writes `iter_dir / "model_setup_prompt.md"` with the filled prompt.
- [ ] Under dry-run, `_run_model_in_iteration` returns `(False, False)`.
- [ ] Under dry-run, exactly one dry-run message is printed per call.
- [ ] The `build_model_vars is None` check still runs before the dry-run branch.
- [ ] `test_failure_chains.py::TestIntegration_ModelSetup` remains green (all existing tests pass).
- [ ] Any new test covering the dry-run prompt-write path is added to `test_prepare_step.py` or `test_failure_chains.py`, following the existing `FakeClaude` / `ConceptFixture` patterns.

### Quality & Integration (both options)
- [ ] `uv run python -m pytest exploration/concept_analysis/scripts/` shows the same pass/fail split as before this work item (189 passed / 6 failed / 6 skipped, modulo any changes merged from pipeline-hardening Phase 5+).
- [ ] Manual smoke: dry-run on `13-electrostatic-hybrid` (or another concept with no `analysis.md`) completes without error. For Option A: `model_setup_prompt.md` is absent from every iter dir (unchanged). For Option B: `model_setup_prompt.md` is present in every iter dir.
- [ ] Dry-run smoke artifacts (`iter-*/` dirs in the test concept) are cleaned up after the smoke check.
- [ ] `.project/active/pipeline-hardening/plan.md` and `design.md` are unmodified by this work item (verified via `git diff`).
- [ ] No changes to `_run_cold_start`, `_run_feedback_pass`, `_run_assess`, or `_run_source_integration`.

---

## Related Artifacts

- **Parent work (frozen):** `.project/active/pipeline-hardening/` — the Phase 4 Deviation note at `plan.md:1017` is the origin of this asymmetry and is the primary input to the design revisit.
- **Audit conversation (context):** The Phase 4 audit on 2026-04-10 confirmed the asymmetry empirically via a dry-run smoke test on concept `13-electrostatic-hybrid`. See that session's audit report (Minor 1 finding).
- **Design:** `.project/active/loop-dry-run-symmetry/design.md` (to be created by `/_my_design`)
- **Plan:** `.project/active/loop-dry-run-symmetry/plan.md` (to be created by `/_my_plan`)
- **Code under change:** `exploration/concept_analysis/scripts/lib/loop.py:484-561` (`_run_model_in_iteration`)
- **Helper (no change expected):** `exploration/concept_analysis/scripts/lib/step_runner.py:58-110` (`prepare_step`)

---

## Implementation Notes

_[To be filled during `/_my_design` — MUST include the Option A vs Option B decision and the per-reason justification required by FR-1 and FR-2.]_

---

**Next Steps:** After approval, proceed to `/_my_design`. The design phase MUST begin with the FR-1 rationale revisit before proposing any code changes.
