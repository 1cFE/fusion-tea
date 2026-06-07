# Spec: Explorer Extractor — Resilient Batch Extraction

**Status:** Complete (implemented 2026-06-05 on `fix/explorer-extractor-resilience`)
**Owner:** Reid W
**Created:** 2026-06-05 12:49 PDT
**Complexity:** LOW
**Branch:** fix/explorer-extractor-resilience

---

## Work Item Summary

The concept-explorer extractor (`exploration/concept_explorer/extract_explorer_data.py`) currently aborts the entire batch the moment any single concept raises an `ExtractionError`. This work item makes the per-concept loop fault-tolerant: a failure in one concept is recorded and the run continues to the next concept, and at the end the script prints a clear, consolidated summary of which concepts failed. "Done" means a user can run the extractor over all ~39 concepts and get every extractable concept's JSON written, plus an unmissable end-of-run report of the ones that didn't.

## Why This Matters Now

Today a single un-migrated or malformed concept (e.g. `17b`, which is costingfe-shaped but defines no `result_1gw`) kills the whole run via `sys.exit(1)` in `main()`. Because the loop processes concepts in order and writes JSON as it goes, an abort mid-batch leaves `data/` **silently half-stale**: concepts before the failure are freshly regenerated, concepts after it keep old output, and nothing flags the inconsistency. The user hit this directly and cannot complete a full extraction. Resilience here unblocks routine re-extraction of the catalog.

## Key Bets / Constraints

- **Bet:** The right model for a batch tool is collect-and-continue with a loud summary — graceful is not the same as silent.
- **Constraint:** A concept that fails MUST NOT have a stale/partial JSON silently presented as fresh; the failure must be surfaced in the summary.
- **Constraint:** The existing planned-skip path (`pending-design-point`) and its reporting behavior are preserved, not replaced.
- **Non-goal:** Fixing or migrating any individual concept (including `17b`). This work item changes only the extractor's batch behavior, not concept models.
- **Non-goal:** Classifying, categorizing, or interpreting *why* a concept failed. Failures are collected generically.

---

## Business Goals

### Why This Matters

The extractor is the bridge from concept analysis artifacts to the explorer UI's `data/` JSON. If it can't complete a full pass, the explorer data set drifts out of sync with the analyses, and the drift is invisible. The user needs to run extraction over the whole catalog and trust that (a) everything that *can* extract *did*, and (b) anything that didn't is reported plainly in one place.

### Success Criteria

- [ ] Running the extractor over the full catalog with one or more failing concepts completes the run (does not abort early) and writes JSON for every concept that extracted successfully.
- [ ] At the end of the run, failed concepts are presented in a single clear summary the user cannot miss.
- [ ] The user does not have to read or interpret the underlying error/stack trace to understand which concepts failed.

### Priority

P1 — blocks routine full-catalog re-extraction.

---

## Problem Statement

### Current State

`run_extraction()` (lines ~876–969) iterates concepts with no per-concept error boundary. Any `ExtractionError` raised inside the loop — missing `result_1gw`, routing disagreement, a `claude -p` narrative failure, a `model_setup.py` import blowup — propagates to `main()`'s `except ExtractionError` handler, which calls `sys.exit(1)`. The batch stops at the first failure; later concepts are never processed; `data/` is left partially updated with no indication of which half is stale.

### Desired Outcome

Each concept is processed inside its own error boundary. A failure records the concept and its error, then the loop moves on. Successful concepts write JSON as before. After the loop, the script prints a consolidated end-of-run report listing every failed concept. The run keeps going by default.

---

## Scope

### In Scope

- `exploration/concept_explorer/extract_explorer_data.py` — the per-concept loop in `run_extraction()` and the end-of-run reporting.
- Per-concept error isolation so one concept's failure does not stop the others.
- A consolidated, clearly formatted failure summary printed at the end of the run.
- Preserving the existing `extracted` / `skipped` reporting alongside the new `failed` reporting.

### Out of Scope

- Any change to individual concept `model_setup.py` files or analysis artifacts.
- Migrating `17b` (or any concept) to the three-forward contract.
- Changing the strict-consumer contract / `verify_two_knob` invariants themselves — only *when the program aborts* changes, not *what counts as a violation*.
- Re-architecting routing (costingfe vs standalone vs freeform detection).

### Edge Cases & Considerations

- A run where **every** concept fails — the summary should still be coherent and the exit behavior sensible.
- A run where failures are mixed with planned skips (`pending-design-point`) — the two categories should remain distinguishable in the output.
- Failures that occur at different stages (narrative extraction vs. cost-model extraction vs. import) should all be caught by the same boundary; the user should not need to know which stage failed.
- A concept that previously wrote JSON in an earlier run and now fails — the run should make clear that this concept did not refresh (its stale JSON, if any, was not regenerated this pass).

---

## Requirement Selection Notes

The normative requirements below fix two things the user explicitly decided: (1) keep-going is the default behavior, and (2) there is a single clear failure summary at the end, with no obligation on the extractor to classify or explain the underlying error. Everything else — exact summary wording, whether to add a `--strict` opt-out flag, exit-code semantics, and which exception types to catch — is intentionally left to design.

---

## Requirements

### Functional Requirements

1. **FR-1**: When a concept fails during extraction, the script MUST record the failure and continue processing the remaining concepts rather than aborting the run. Keep-going is the default behavior (no flag required).
2. **FR-2**: The script MUST write output JSON for every concept that extracts successfully, regardless of whether other concepts in the same run failed.
3. **FR-3**: At the end of the run, the script MUST print a single, clearly delineated summary that lists every concept that failed. The summary MUST be easy to spot in the run output.
4. **FR-4**: The failure-handling path MUST be generic with respect to the error — it MUST catch and report a concept's failure without depending on what the error was or where it originated. [INFERRED from user: "you should not need to worry/care about what that error was, or where it came from."]
5. **FR-5**: The existing planned-skip behavior (`Comparison-Status: pending-design-point`) and its reporting MUST be preserved and MUST remain distinguishable from genuine failures in the output.

### Non-Functional Requirements

- The summary SHOULD include enough identification (at minimum the concept ID) for the user to act on each failure, without requiring the underlying error text to be understood.

---

## Acceptance Criteria

### Core Functionality

- [ ] With `17b` (or any deliberately-broken concept) present, a full run processes all other concepts and writes their JSON (FR-1, FR-2).
- [ ] The run prints a clear end-of-run summary naming `17b` (and any other failures) as failed (FR-3).
- [ ] Injecting a different failure type (e.g. a forced narrative or import error) into a concept is caught by the same boundary and reported the same way, with no special-casing (FR-4).
- [ ] A concept with `Comparison-Status: pending-design-point` still appears under the skip report, not the failure report (FR-5).

### Quality & Integration

- [ ] Existing tests continue to pass.
- [ ] A successful full run with zero failures produces the same JSON outputs as before this change (no regression in the happy path).

---

## Next-Stage Handoff

**Settled in this spec:**
- Default is keep-going; the run does not abort on a single concept's failure.
- There is one clear end-of-run failure summary; the extractor does not classify or interpret the error.
- No concept models are touched; this is purely extractor batch behavior.

**Design must figure out:**
- Exit-code semantics on a keep-going run that had failures (e.g. non-zero-if-any-failed for CI honesty vs. always-zero) — recommend a choice.
- Whether to add a `--strict` flag to restore fail-fast for callers who want it.
- Which exception types the per-concept boundary catches (just `ExtractionError`, or all `Exception` to also trap import/`compute()` blowups) and how broad is safe.
- The exact shape and placement of the failure summary, building on the existing `extracted` / `skipped` reporting at the end of `run_extraction()`.
- Whether anything should be written to mark a failed concept's `data/` JSON as stale (vs. leaving it untouched and only reporting).

**Watch-outs for design:**
- A bare `except Exception` can mask programmer errors — design should decide how much context to retain (e.g. error string/traceback captured for the summary) even though the *control flow* is error-agnostic.
- Don't silently swallow failures: graceful must stay honest — the summary is the safeguard against the half-stale-`data/` problem that motivated this work.
- Keep `pending-design-point` skips and genuine failures in separate buckets so a planned omission never looks like a crash and vice versa.

---

## Related Artifacts

- **Extractor:** `exploration/concept_explorer/extract_explorer_data.py`
- **Design:** `.project/active/explorer-extractor-resilience/design.md` (to be created)
- **Related prior work:** `.project/active/explorer-rework-unblock/`, `.project/active/concept-rework-three-forward-contract/` (origin of the strict `result_1gw` contract that `17b` violates)

---

**Next Steps:** After approval, proceed to `/_my_design`
