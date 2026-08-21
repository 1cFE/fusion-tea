# Design: Explorer Extractor — Resilient Batch Extraction

**Status:** Complete (implemented 2026-06-05 on `fix/explorer-extractor-resilience`)
**Owner:** Reid W
**Created:** 2026-06-05 12:49 PDT
**Updated:** 2026-06-05 12:49 PDT
**Branch:** fix/explorer-extractor-resilience
**Commit:** 23f8110f

---

## Overview

Wrap the per-concept body of `run_extraction()` in a single error boundary so one concept's failure is recorded and skipped instead of aborting the batch, then print a clear consolidated failure summary at the end. Keep-going is the default.

## Related Artifacts

- **Spec:** `.project/active/explorer-extractor-resilience/spec.md`
- **Target:** `exploration/concept_explorer/extract_explorer_data.py`
- **Tests:** `exploration/concept_explorer/tests/test_extraction.py`
- **Origin of the strict `result_1gw` contract `17b` violates:** `.project/active/concept-rework-three-forward-contract/`, `.project/active/explorer-rework-unblock/`

---

## Research Findings

- **The abort is structural, not in any single check.** `run_extraction()` (lines 876–969) loops over concepts with no error boundary. Every fatal path inside the loop — missing `result_1gw` (313–320), routing disagreement (922–936), `extract_narrative`'s `claude -p` failure (813–828), a `model_setup.py` import blowup — raises `ExtractionError` (or a bare exception) that unwinds to `main()`'s `except ExtractionError` → `sys.exit(1)` (1011–1013). First failure stops everything; later concepts never run.
- **Failure-classification already half-exists.** The loop already collects planned skips into `skipped: list[tuple[str, str]]` and reports them at the end (873–875, 901–909, 971–975). The new `failed` bucket is a direct parallel — same shape, separate list, separate report block.
- **No external caller depends on exit code or return type.** Grep for `extract_explorer_data` / our `run_extraction` shows only docs plus `scripts/zotero_ingest.py`, whose `run_extraction` (zotero_ingest.py:116) is an unrelated PDF-extraction function. Our extractor is invoked directly by the user via CLI. Changing the exit code and the `run_extraction` return type is safe.
- **The unit/​batch split keeps most tests green.** `extract_costingfe` and `extract_narrative` raise `ExtractionError` as their *unit contract*. Tests assert that contract by calling those functions directly: `test_missing_result_1gw_raises` (354), `test_missing_model_attribute_raises` (336), `test_run_extraction_propagates_extraction_error`'s sibling unit checks. If the raises stay put and only `run_extraction` adds the `try/except`, the unit contracts are untouched.
- **Exactly one test asserts the old batch-abort behavior.** `test_run_extraction_propagates_extraction_error` (1083–1104) wraps a `run_extraction()` call in `pytest.raises(ExtractionError)`. Under keep-going this is the behavior we are deliberately removing, so this test must be rewritten (see Validation).
- **A `.json.stale` sidecar convention already exists** (963–967): on success the loop clears `{id}.json.stale`. This is the existing hook if we ever want to *mark* a failed concept's stale JSON — relevant to one deferred decision below.

---

## Core Concept

`run_extraction` becomes a **fault-tolerant batch runner**: the per-concept work is wrapped in one `try/except` that catches anything, records `(concept_id, short_error)`, and continues. The error-handling is deliberately *generic* — it does not know or care what failed or where. After the loop, the run prints three buckets — extracted, skipped (planned), failed (unexpected) — with the failed block formatted as an unmissable banner. The unit functions (`extract_costingfe`, `extract_narrative`, …) keep raising exactly as today; resilience lives entirely at the batch layer that consumes them. This is the standard batch-tool pattern (`pytest`, `make -k`): keep going, but stay honest — the end-of-run summary is the safeguard against a silently half-stale `data/`.

The key insight: **separate the unit contract (raise on violation) from the batch policy (collect and continue).** That single seam delivers the whole feature without touching any check, any routing logic, or any concept model.

## Key Bets & Decisions

- **Catch broadly (`except Exception`), not just `ExtractionError`.** The user's directive — "you should not need to worry/care about what that error was, or where it came from" — means an import error, a `compute()` blowup, or a Pydantic `ValidationError` must be trapped the same as an `ExtractionError`. We capture a short string form of the error for the summary but never branch on its type. *Alternative rejected:* catching only `ExtractionError` would let an unmigrated concept that blows up on import still kill the batch — exactly the brittleness we're removing.
- **Resilience lives only in `run_extraction`; unit functions are untouched.** Keeps the unit-contract tests green and keeps the strict three-forward contract intact for callers that invoke `extract_costingfe` directly. *Alternative rejected:* softening the raises inside `extract_costingfe` would erode the contract and ripple into many tests.
- **`failed` is a third bucket parallel to the existing `skipped`.** Reuses the established list-and-report shape; planned skips (`pending-design-point`) and genuine failures stay visibly distinct (FR-5). *Alternative rejected:* merging skips and failures into one list — loses the planned-vs-crashed distinction the spec requires.
- **Whole-run fatals still abort.** `run_extraction`'s own pre-loop guard (`analyses_dir` not found, 864) is not per-concept and stays a hard `ExtractionError` that `main()` surfaces. The boundary wraps only the per-concept body.
- **Exit non-zero when any concept failed (recommended — confirm).** No caller depends on the exit code, so the honest default is: complete the batch, then exit `1` if the `failed` bucket is non-empty, `0` otherwise. Keep-going governs *control flow within the run*; the exit code governs *whether the run is reported as clean to a wrapper/CI*. This is the one open policy choice — see Next-Stage Handoff.
- **No `--strict` flag (deferred).** The user asked only for keep-going; adding a fail-fast toggle is unrequested surface. Easy to add later if wanted. Recorded as a non-goal.
- **Failed concepts' existing JSON is left untouched, report-only (no stale marker).** The summary is the visibility mechanism the spec calls for; writing `.json.stale` sidecars on failure is a heavier, separate behavior. Deferred, with the existing sidecar convention noted as the natural hook if revisited.

## Architecture

Single function changes shape; nothing else moves.

```
run_extraction(analyses_dir, data_dir, ...)
  ├─ pre-loop guards (analyses_dir exists, mkdir data_dir)   ← unchanged, still fatal
  ├─ extracted: []   skipped: []   failed: []                ← add `failed`
  └─ for concept_dir in concept_dirs:
        try:
            <existing per-concept body: frontmatter → routing
             → narrative → extract_* → write JSON → clear stale>
            extracted.append(...)                            ← on the success path
        except Exception as exc:                             ← NEW boundary
            failed.append((concept_id, _short(exc)))
            print one-line "FAILED {id}" marker
            continue
     ── after loop ──
     report skipped   (existing block)
     report failed    (NEW banner block)                     ← unmissable
     report extracted count
     return len(failed)                                      ← main() maps to exit code
```

`main()` calls `run_extraction`, keeps its `except ExtractionError` for whole-run fatals, and adds `sys.exit(1 if failures else 0)` (subject to the exit-code decision).

**Data flow:** unchanged for successful concepts — same JSON, same path, same stale-marker clearing. The only new flow is the failure path: exception → `(id, short_error)` → `failed` list → end-of-run banner → return count → exit code.

## Required Invariants

- A failure in concept *N* MUST NOT prevent processing of concepts *N+1…*. (FR-1)
- Every concept that reaches its JSON-write without raising MUST still produce identical JSON to today. (FR-2; happy-path no-regression)
- The `pending-design-point` skip path MUST remain a `skipped` entry, never a `failed` one. (FR-5) — it `continue`s *before* any raising work, so it never enters the failure path.
- The failure summary MUST identify each failed concept by ID and be visually distinct from the skip and success output. (FR-3)
- The failure path MUST NOT branch on exception type or origin. (FR-4)
- Whole-run fatal conditions (missing analyses dir) MUST still abort with a non-zero exit.

## Component Overview

Everything is inside `exploration/concept_explorer/extract_explorer_data.py`:

- **`run_extraction()` loop body (≈876–969):** gains the `try/except Exception` boundary and the `failed` accumulator. This is the substantive change.
- **End-of-run reporting (≈971–979):** gains a `failed` banner block alongside the existing `skipped` block; `run_extraction` returns the failure count.
- **`main()` (≈987–1013):** maps the returned failure count to the process exit code; keeps the existing whole-run `ExtractionError` handler.
- **A tiny error-shortener helper** (e.g. `_short(exc) -> str`): first line / truncated `repr` of the exception for one-line summary rows. Generic; type-agnostic.

No changes to `extract_costingfe`, `extract_standalone`, `extract_narrative`, routing, or any concept file.

## Non-Goals

- Fixing or migrating `17b` (or any concept) — purely extractor batch behavior.
- A `--strict` / fail-fast toggle.
- Marking or deleting a failed concept's stale `data/` JSON.
- Changing the strict-consumer contract, `verify_two_knob`, or routing detection.
- Interpreting, categorizing, or grouping failures by cause.

## Implementation Notes

- **Boundary placement:** wrap from the first per-concept work (frontmatter parse) through the stale-marker clear. `concept_id = parse_concept_id(concept_dir.name)` and the `print("Extracting …")` may sit just inside or just outside the `try`; `concept_id` must be known before the `except` so the failure row can name the concept — compute it first.
- **Keep raises where they are.** Do not soften `extract_costingfe`/`extract_narrative`. The whole feature is the one `try/except` plus the report block.
- **`continue` interplay:** the existing `pending-design-point` `continue` lives inside the new `try` — harmless, `continue` works normally inside `try`. Ensure it appends to `skipped` (as today) and does not fall into the `except`.
- **Return type:** `run_extraction` currently returns `None`; returning an `int` failure count is backward-compatible with all current tests (they ignore the return). 
- **Banner legibility:** the user's bar is "very clear print-out … cannot miss it." Use a delimiter line + `FAILED (n)` header + one `  {id}  {short_error}` row each. Print to stdout with the rest of the run log (the existing skip block uses stdout, not stderr — match it).

## Potential Risks

- **Over-broad `except` hides programmer bugs.** Mitigation: capture and print the short error string for every failure (control flow stays generic, but the message is preserved so a real bug is visible in the summary, not swallowed). A `--strict` escape hatch remains a cheap future add if silent-masking ever bites.
- **Silent half-stale `data/` persists for failed concepts.** By design we leave their JSON untouched. Mitigation: the end-of-run banner names exactly which concepts didn't refresh, converting the previously-invisible drift into an explicit list. (Stale-marking deferred, not lost.)
- **Exit-code change surprises a future wrapper.** Currently no caller depends on it; if one is added later expecting `0`, a non-zero-on-failure exit could trip it. Mitigation: documented here and a one-line change to flip if needed.

## Integration Strategy

Drop-in. The CLI invocation (`uv run python …/extract_explorer_data.py [--concept …] [--skip-narrative]`) is unchanged. A full run now completes and reports instead of aborting at the first bad concept. Complements the existing `skipped` reporting; replaces only the implicit fail-fast that lived in the absence of an error boundary.

## Validation Approach

- **New test — keep-going:** a batch with one deliberately-broken concept (e.g. costingfe-shaped, no `result_1gw`, à la `17b`) plus ≥1 healthy concept → run completes, healthy concept's JSON is written, broken concept appears in `failed`, `run_extraction` returns `1`.
- **New test — error-agnostic:** inject a different failure (e.g. forced narrative `claude -p` non-zero, or an import error) → caught by the same boundary, reported identically, no special-casing.
- **Rewrite `test_run_extraction_propagates_extraction_error` (1083–1104):** it currently asserts `pytest.raises(ExtractionError)` around `run_extraction`. New semantics: `run_extraction` does **not** raise — it returns a failure count and the concept lands in the summary. Rename to reflect collect-and-continue (e.g. `test_run_extraction_collects_narrative_failure`).
- **Preserve unit-contract tests:** `test_missing_result_1gw_raises`, `test_missing_model_attribute_raises` call the unit functions directly and must stay green unchanged.
- **Skip-vs-fail separation test:** a `pending-design-point` concept alongside a failing concept → one in `skipped`, one in `failed`, distinct in output.
- **Manual:** `uv run python exploration/concept_explorer/extract_explorer_data.py --skip-narrative` on the real repo → all extractable concepts written, `17b` named in the failure banner, non-zero exit (per decision).
- **Full suite:** `uv run python -m pytest exploration/concept_explorer/tests/` green.

## Next-Stage Handoff

**Fixed for the plan:**
- One `try/except Exception` boundary in `run_extraction`'s loop + a `failed` bucket + an end-of-run banner. No changes outside `extract_explorer_data.py` except the test file.
- Unit functions keep raising; resilience is batch-layer only.
- Broad catch, error-agnostic reporting, planned-skip path preserved and distinct.

**One decision to confirm before/while planning:**
- **Exit code on a keep-going run with failures.** Recommendation: exit `1` if any failed, else `0` (honest, CI-catchable, no caller depends on it). The alternative is always-`0` (purely advisory summary). Flag for Reid; trivial to flip either way.

**De-risk first:**
- Confirm the `pending-design-point` `continue` sits cleanly inside the new `try` and still routes to `skipped` (write the skip-vs-fail test early).

---

**Next Step:** After approval → `/_my_plan` (or `/_my_implement` for this small, single-file change).
