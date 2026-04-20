# Spec: Staleness Propagation Fix

**Status:** Implementation Complete
**Owner:** Reid W
**Created:** 2026-04-19 12:07 PDT
**Complexity:** MEDIUM
**Branch:** fix/stale-tracker

---

## Work Item Summary

The Stage1 concept-analysis loop currently marks canonical `model_setup.py` files as stale on every iteration — including the PASS iteration that just promoted a fresh copy. Regenerating a downstream artifact also never clears an existing marker. The staleness signal carries no information as a result. This work item makes the signal accurate by construction: the propagator takes an explicit regeneration set and exempts members, and every artifact producer clears its own marker on write. When done, `concept_status.md` reflects reality without manual interpretation, and three concepts (07, 09, 10) currently misannotated as stale are cleaned up.

## Why This Matters Now

The bug is actively polluting the one table the user reads to decide which concepts still need work. It has already led to incorrect assumptions about concept 07's state in the current session, and more broadly undermines trust in the pipeline's self-reporting. The fix is small, well-scoped, and unblocks honest status signals across the remaining concept-analysis work.

## Key Bets / Constraints

- **Bet:** The regeneration-set-as-argument contract plus producer-owned clearing is enough to restore signal accuracy. No upstream-identity tracking, no hashing.
- **Constraint:** Marker-on-artifact format is preserved as-is (`# STALE:` line for `.py`, YAML `Stale: true` for `.md`, `.stale` sidecar for explorer JSON). Readers that already parse these stay compatible.
- **Non-goal:** The review→synthesis transitive edge and detection of out-of-band hand-edits to `analysis.md` are deferred.

---

## Business Goals

### Why This Matters

`concept_status.md` is the at-a-glance signal the team uses to triage which concepts need rework, which are settled, and which have stale outputs. When that signal cannot distinguish "just regenerated" from "genuinely out of date," triage breaks down and every status reading requires manual cross-checking against file timestamps and iter-N histories. The concept_analysis loop was supposed to remove that burden, not add to it.

### Success Criteria

- [ ] After a PASS iteration, canonical `model_setup.py` is fresh (no `# STALE:`).
- [ ] After an iteration with `model_ok=False`, canonical `model_setup.py` is stamped stale.
- [ ] Running `model-setup --force`, `review --force`, or `synthesize --force` on a stamped artifact produces a fresh artifact (no marker).
- [ ] Concepts 07, 09, and 10 no longer carry false `# STALE:` markers after this work item lands.
- [ ] `concept_status.md` can be read at face value without external cross-checks.

### Priority

P1 (inferred). The bug is actively corrupting a signal the team relies on, and it blocks clean state reporting for concept-analysis work on the `fix/stale-tracker` branch.

---

## Problem Statement

### Current State

`propagate_staleness()` in `scripts/lib/state.py` stamps a fixed downstream list (`model_setup.py`, `review.md`, `synthesis.md`, explorer JSON) whenever it is called. `loop.py:238` calls it at the end of every iteration, after `_update_canonical_files` has already promoted a clean iter-N `model_setup.py` to canonical. The propagator immediately re-stamps the clean file. On a PASS exit, the canonical ends up stale. Regeneration producers (`cmd_model_setup`, `cmd_review`, `cmd_synthesize`) never clear existing markers — the standalone `model-setup` command even skips stamped files unless `--force` is passed, and `--force` overwrites without touching the marker. The net result: 3 of the 19 concepts on the current branch carry false stale markers with no path back to fresh short of a wholesale rewrite.

### Desired Outcome

The propagator takes a regeneration set and leaves its members alone. Every producer clears its own marker as part of a successful write. The status table becomes trustworthy. Concepts 07, 09, and 10 are cleaned up as the final step, once the loop bug is fixed and the cleanup won't be immediately re-introduced by a subsequent run.

---

## Scope

### In Scope

- Reshape `propagate_staleness(concept_id, reason)` → `propagate_staleness(concept_id, reason, regenerated)` where `regenerated` is a set/iterable of canonical filenames the caller just wrote.
- Rewire the two current call sites:
  - `loop.py:238` — pass `{"analysis.md"}` always, plus `"model_setup.py"` iff the iteration's `model_ok=True`.
  - `run_analysis.py:456` (`cmd_analyze --feedback`) — pass `{"analysis.md"}`.
- Add producer-owned clearing to every producer that writes a tracked artifact:
  - `_update_canonical_files` (clears canonical `model_setup.py` marker when promoting iter-N copy with `model_ok=True`).
  - `cmd_model_setup` (clears `# STALE:` on write, both with and without `--force`).
  - `cmd_review` (clears `Stale:` frontmatter on write).
  - `cmd_synthesize` (clears `Stale:` frontmatter on write).
  - Explorer extractor (deletes `.stale` sidecar on successful extraction).
- Marker-stripping helpers in `scripts/lib/state.py` (or a sibling module):
  - Strip `# STALE:` first line from a `.py` text.
  - Strip `Stale:` / `Stale-Reason:` fields from YAML frontmatter.
  - Delete the `.stale` sidecar for a given explorer JSON.
  - Each helper has its own unit test battery — built first (de-risking step).
- Regression tests in the style of `scripts/test_failure_chains.py`:
  - PASS iteration leaves canonical `model_setup.py` fresh.
  - `model_ok=False` iteration leaves canonical `model_setup.py` stamped.
  - PASS iteration stamps pre-existing `review.md` / `synthesis.md`.
  - `--force` on each standalone producer clears the marker.
  - `analyze --feedback` stamps all four downstream artifacts.
- Final data cleanup: strip the false markers from concepts 07, 09, 10 on `fix/stale-tracker` as the last change in the branch, after the code fix is verified.

### Out of Scope

- Review→synthesis transitive staleness (if `review.md` changes, `synthesis.md` should arguably become stale — deferred).
- Detecting out-of-band hand-edits to `analysis.md` outside the sanctioned commands.
- Automatic regeneration triggered by the stale signal.
- Refactoring the marker formats themselves.
- Changes to the generator of `concept_status.md` beyond what the invariants already imply.

### Edge Cases & Considerations

- An iteration with `model_ok=False` where the canonical `model_setup.py` does not yet exist: the propagator's idempotent skip should leave things alone (no file to stamp).
- Frontmatter files where `Stale-Reason` exists but `Stale: false` (historically, the clearing path never existed): the stripping helper must handle both fields and leave well-formed YAML.
- `# STALE:` line followed by blank line vs. followed by the module docstring directly: the strip helper must not eat the first line of real content.
- Explorer JSON missing: skip.
- A producer whose write fails mid-operation: marker state is undefined; acceptable, same as any other partial-write failure in the pipeline.

---

## Requirement Selection Notes

Requirements below cover the contract changes and testable obligations that must hold for the signal to be trustworthy. Questions of exact function signatures (positional vs keyword arg, filenames-as-strings vs paths), where the strip helpers live (same module or new), and whether the propagator accepts `Path` or `str` members are intentionally left to design. The shape of the regression harness (pytest vs bespoke) is also design's call.

---

## Requirements

### Functional Requirements

> Requirements are from the approved concept design and the user's `/_my_spec` invocation unless marked [INFERRED].

1. **FR-1**: `propagate_staleness` MUST accept an explicit set of "just-regenerated" canonical artifact names and MUST NOT stamp members of that set. There MUST be no implicit default for this argument.
2. **FR-2**: Inside `run_stage1_loop`, the staleness call MUST include `analysis.md` in the regeneration set, and MUST include `model_setup.py` in the regeneration set if and only if the iteration's `model_ok` is `True`.
3. **FR-3**: The `cmd_analyze --feedback` call site MUST call the propagator with a regeneration set containing `analysis.md` only.
4. **FR-4**: Every producer of a tracked artifact MUST clear that artifact's stale marker as part of a successful write. This applies to `_update_canonical_files` (on promotion), `cmd_model_setup`, `cmd_review`, `cmd_synthesize`, and the explorer extractor.
5. **FR-5**: The three marker-stripping operations (`.py` first-line comment, `.md` YAML fields, `.stale` sidecar deletion) MUST be implemented as discrete helpers with unit-test coverage, and these helpers MUST land before the producers that depend on them.
6. **FR-6**: A regression test MUST assert that after a PASS iteration of `run_stage1_loop`, the canonical `model_setup.py` does not begin with `# STALE:`. A regression test MUST assert that after an iteration with `model_ok=False`, the canonical `model_setup.py` does begin with `# STALE:`.
7. **FR-7**: Once the code fix is verified, the false `# STALE:` markers on concepts 07, 09, and 10 MUST be stripped as a final change on `fix/stale-tracker`, with the strip verified against the corresponding iter-N clean copies before committing.
8. **FR-8**: [INFERRED] The propagator MUST remain idempotent — calling it twice with the same arguments on the same directory state MUST NOT produce different results than calling it once.

### Non-Functional Requirements

- None beyond what the functional requirements imply. No performance, security, or scaling requirements apply.

---

## Acceptance Criteria

### Core Functionality

- [ ] `propagate_staleness` signature requires an explicit regeneration set; call sites updated to supply one.
- [ ] After `uv run python scripts/run_analysis.py` over a fresh test concept through PASS, `grep -c '^# STALE:' model_setup.py` returns 0.
- [ ] After a forced `model_ok=False` iteration (via the fake-Claude harness), the canonical `model_setup.py` starts with `# STALE:`.
- [ ] `uv run python scripts/run_analysis.py model-setup --force <concept>` on a pre-stamped file produces a fresh file.
- [ ] `uv run python scripts/run_analysis.py review --force <concept>` on a frontmatter-stamped file produces a file with `Stale: false` (or no `Stale` field).
- [ ] `uv run python scripts/run_analysis.py analyze --feedback <concept>` stamps all four downstream artifacts where they exist.
- [ ] Concepts 07, 09, 10 in `exploration/concept_analysis/analyses/` do not carry `# STALE:` on their canonical `model_setup.py` at branch tip.

### Quality & Integration

- [ ] Marker-stripping helpers have unit tests covering: first-line marker with module docstring after, first-line marker with blank line after, YAML with both `Stale` and `Stale-Reason`, YAML with only `Stale`, explorer JSON with and without sidecar.
- [ ] `scripts/test_failure_chains.py` (or its equivalent) includes the PASS/fail regression assertions.
- [ ] Existing tests in `scripts/test_*.py` continue to pass.
- [ ] No other callers of `propagate_staleness` beyond the two known sites exist (verified via grep).

---

## Next-Stage Handoff

**Settled in this spec:**
- The regeneration-set contract on the propagator.
- The producer-owned clearing contract.
- The list of producers that must clear.
- The final data cleanup is in scope and is the last change on the branch.
- Review→synthesis transitive edge and hand-edit detection stay deferred.

**Design must figure out:**
- Exact signature of `propagate_staleness` — positional vs keyword, str vs `Path`, whether names are bare or relative to `concept_dir`.
- Where the marker-stripping helpers live — expanded `state.py`, a new `markers.py`, or inline per producer.
- Whether `--force` changes semantics at all, or if it's purely the existing "skip the exists-check" with clearing falling out of the producer rule naturally.
- The exact test harness used for the regression tests — reuse of `_fake_claude.py`, pytest structure, where the assertions plug in.
- Whether a thin helper wraps the "call clear, then write" pattern to prevent drift across producers.

**Watch-outs for design:**
- First-line strip on `.py` files must not corrupt the module docstring or shebang-like constructs.
- YAML field strip must preserve other fields' ordering and handle both presence and absence of `Stale-Reason`.
- `_update_canonical_files` promotion is the one place where clearing must happen as part of the copy itself — not after — so that a crash between copy and clear leaves a consistent state (fresh file, no marker).
- Order of operations in the loop: clearing on promotion happens before propagation, so the regeneration set's exemption is belt-and-suspenders. Both must be correct.

---

## Related Artifacts

- **Concept design:** `.project/concepts/staleness-propagation.md`
- **Research:** `.project/research/20260419-115210_staleness-propagation-in-stage1-loop.md`
- **Design:** `.project/active/staleness-propagation-fix/design.md` (to be created)
- **Plan:** `.project/active/staleness-propagation-fix/plan.md` (to be created)

---

**Next Steps:** After approval, proceed to `/_my_design`.
