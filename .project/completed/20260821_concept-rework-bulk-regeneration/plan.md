# Implementation Plan: Parallel Subprocess Dispatch + Archive + Status Stats (Item 11)

**Status:** Draft
**Created:** 2026-05-31
**Last Updated:** 2026-05-31

## Source Documents
- **Spec:** `.project/active/concept-rework-bulk-regeneration/spec.md`
- **Design:** none — mechanism decisions are settled inline below (operator: "simple enough, no design needed").

## Mechanism Decisions (would normally live in design.md)

1. **Parallel runner** — Generalize `run_scoring_pipeline.py:run_for_concept` to build its
   subprocess flags via a per-stage `stage_flags(stage, args)` helper instead of the current
   hardcoded `--force` + synthesize-only `--skip-review-gate`. Scoring stages keep their exact
   existing flag output (zero behavior change). New stages: `analyze` → `--force --max-passes N`,
   `model-critic` → none (it rejects `--force`). Add a **thin sibling** `run_regen_batch.py` that
   imports `run_parallel_stage` and runs `analyze` then `model-critic` over an explicit concept
   list, stopping after the critic. No run-all default; concept IDs are required positionals.
2. **Archive** — No helper script. A **documented git-mv procedure** (below), executed and verified
   against the concept(s) being regenerated. Explicit **include allowlist** of pipeline-produced
   artifacts; `design-points/` and `review.md` are never moved.
3. **Status LCOE** — Module-load `model_setup.py` (replicate the explorer's ~10-line
   `load_module_from_path` in `lib/`, with stdout redirect; no cross-package import of
   `concept_explorer`). Read `native.costs.lcoe` and `result_1gw.costs.lcoe`; `P_native` from
   frontmatter `P-Native`. Per-concept try/except → blank cell on any failure (un-migrated concepts,
   import errors), exactly as the explorer tolerates.

## Implementation Strategy

**Phasing Rationale:** Phase 1 is the only genuinely *missing* capability and carries the only real
regression risk (refactoring `run_for_concept`, which the scoring pipeline depends on) — so it goes
first and is proven against the existing scoring tests. Phase 2 (archive) and Phase 3 (status stats)
are independent conveniences that touch disjoint code; either order works, archive is placed second
because it's the prerequisite habit before a regen batch is actually run.

**Critical Path:** `stage_flags()` refactor (keeps scoring green) → `run_regen_batch.py` sibling →
archive procedure → status columns.

**First Proof Point:** Phase 1 — two concept IDs run `analyze`+`model-critic` concurrently with
`[i/total] cid: OK|FAILED` output, **and** `run_scoring_pipeline.py`'s existing tests still pass.

**Overall Validation Approach:** Each phase starts with tests; the whole
`exploration/concept_analysis/scripts/` suite must stay green (spec Quality gate); manual smoke per
phase.

---

## Phase 1: Parallel batch runner (`analyze` + `model-critic`)

### Goal
Deliver FR-1/FR-2/FR-3/FR-4: a runner the operator points at an explicit concept list to fan out
`analyze --max-passes N` then `model-critic` as parallel subprocesses, reusing the scoring pool.

### Assumption Under Test
The scoring pool machinery generalizes to `analyze`/`model-critic` with only a per-stage flag change
— and doing so does **not** alter scoring's subprocess invocation.

### Test Stencil (Write This First)
```python
# test_regen_batch.py
def test_stage_flags_preserves_scoring_behavior():
    # synthesize keeps --force and --skip-review-gate; calibrate/heatmap unchanged
    assert "--force" in stage_flags("synthesize", _args(max_passes=3))
    assert "--skip-review-gate" in stage_flags("synthesize", _args(max_passes=3))

def test_stage_flags_analyze_carries_max_passes():
    flags = stage_flags("analyze", _args(max_passes=5))
    assert flags == ["--force", "--max-passes", "5"]

def test_stage_flags_model_critic_has_no_force():
    # model-critic's argparser rejects --force; flags must be empty of it
    assert "--force" not in stage_flags("model-critic", _args())

def test_regen_batch_requires_explicit_concepts():
    # no concepts → argparse error / non-zero; no run-all default
    with pytest.raises(SystemExit):
        parse_args([])  # no positional concept IDs
```

### Changes Required

**Specific file changes:**

#### 1. Test file (write first)
**File:** `exploration/concept_analysis/scripts/test_regen_batch.py` (NEW)
- [x] `stage_flags()` correctness for `synthesize` (scoring parity), generic scoring stage,
      `analyze` (carries `--max-passes`), `model-critic` (no `--force`/`--max-passes`).
- [x] `run_regen_batch` CLI requires ≥1 concept positional (no run-all); `--workers` default
      matches the scoring runner (3); only `analyze` + `model-critic` stages are dispatched.

#### 2. Generalize the pool runner
**File:** `exploration/concept_analysis/scripts/run_scoring_pipeline.py`
- [x] Add `stage_flags(stage, max_passes=None)` returning the per-stage flag list. Moved the
      existing `--force` + synthesize `--skip-review-gate` logic into it unchanged; added `analyze`
      (`--force`, `--max-passes`) and `model-critic` (no flags) branches.
- [x] `run_for_concept(...)`: replaced the hardcoded `cmd.append("--force")` / synthesize block
      with `*stage_flags(stage, max_passes)`; added optional `max_passes` param. Threaded
      `max_passes` through `run_parallel_stage` → `executor.submit`.
- [x] Left `STAGES`, `main()`, and the scoring stage sequence untouched.

#### 3. Sibling batch runner
**File:** `exploration/concept_analysis/scripts/run_regen_batch.py` (NEW)
- [x] Imports `run_parallel_stage` from `run_scoring_pipeline`.
- [x] CLI: required `concepts` positional (`nargs="+"`), `--workers` (default 3), `--max-passes`
      (default 3), `--model`, `--timeout`.
- [x] Runs `analyze` parallel stage, then `model-critic` parallel stage, over the given list.
      Per-concept `[i/total] cid: OK|FAILED` emitted by `run_parallel_stage`. **Stops after
      `model-critic`** — no review/synthesize/score/approve. Returns non-zero if any concept failed.

### Validation
**Automated:**
- [x] `uv run python -m pytest test_regen_batch.py` → 7 passed
- [x] `uv run python -m pytest` (full scripts suite) → 419 passed, 5 skipped, 4 failed. The 4
      failures are pre-existing `test_concepts_v2.py` `StopIteration` (no "pending" concept in
      current data) — confirmed identical with `run_scoring_pipeline.py` reverted; not a Phase 1
      regression.
**Manual:**
- [x] `run_regen_batch.py` (no args) → argparse error, lists `concepts` as required (no run-all).
- [x] `stage_flags` sanity: synth `['--force','--skip-review-gate']`, analyze
      `['--force','--max-passes','5']`, critic `[]`.
- [ ] Live 2-concept concurrent `analyze`+`model-critic` run — deferred (calls Claude / costs;
      operator to run on a real batch).

**What We Know Works After This Phase:** The reuse claim (FR-3), per-stage flags incl.
`--max-passes` (FR-1), `model-critic` parallel dispatch wiring (FR-2), no run-all / stop-after-critic
(FR-4), and scoring pipeline parity (unit-tested + existing suite green).

---

## Phase 2: Archive old artifacts correctly

### Goal
Deliver FR-5/FR-6: move a concept's old **pipeline-produced** artifacts to
`archive/concept_analysis_pre_rework/{cid}/` via `git mv` (history retained), leaving regeneration
inputs and hand-written content in place. Done as a documented, repeatable procedure — no helper.

### Assumption Under Test
A plain `git mv` of the allowlisted artifacts retains `git log --follow` history and leaves a clean
empty path that `analyze --force` cold-starts into; `design-points/` and `review.md` are correctly
excluded.

### The Procedure (documented here = the deliverable)
For a concept `{cid}` under `exploration/concept_analysis/analyses/{cid}/`. The allowlist below was
validated against all 41 real concept dirs (see Phase 2 Completion note).

**MOVE — the allowlist (pipeline-produced):**
`analysis.md`, `model_setup.py`, `model_output.txt`, `synthesis.md`, `gap_report.md`,
`address_log.md`, `research_log.json`, `iter-*/`, `prompts/`, `critic_review_*`. Move only paths
that exist.

**NEVER MOVE (regen inputs / hand-authored / untracked):**
- `design-points/` — regeneration **input** (FR-6).
- `review.md` — **human-authored** (FR-6).
- `__pycache__/` — untracked build artifact (`git mv` would error anyway).
- **Anything not on the allowlist** — left in place by default. This deliberately includes
  ambiguous, possibly hand-authored one-offs seen in a few dirs (`change_requests_*.md`,
  `*_parameter_audit.md`, `*_concept_downselect.md`). The safe failure mode is leaving an extra
  reference file at the live path; they do not interfere with a cold-start `analyze --force`.

```bash
# from repo root. ALWAYS preview the move set first.
cid=07-maglif                                    # the concept about to be regenerated
src=exploration/concept_analysis/analyses/$cid
dst=archive/concept_analysis_pre_rework/$cid
mkdir -p "$dst"
for p in analysis.md model_setup.py model_output.txt synthesis.md gap_report.md \
         address_log.md research_log.json iter-* prompts critic_review_*; do
  for match in $src/$p; do                        # inner loop: expands iter-*/critic_review_* globs
    [ -e "$match" ] && git mv "$match" "$dst/"     # skips non-matching globs cleanly
  done
done
git commit -m "archive $cid pre-rework artifacts"
# CONFIRM exclusions survived (must list design-points/ and review.md, nothing pipeline-produced):
ls -A "$src"
git log --follow --oneline -- "$dst/analysis.md" | head    # history retained across the move
```

> The inner `for match in $src/$p` loop is required: `[ -e "$src/iter-*" ]` tests the literal glob
> string and silently moves nothing. The inner loop expands the glob and the `-e` test skips the
> unexpanded pattern when a class (e.g. `critic_review_*`) has no match.

### Changes Required
- [x] Canonical procedure + allowlist documented above ("The Procedure"); allowlist validated
      against all 41 real concept dirs.
- [x] **Bulk-archived all 30 regeneratable old-pipeline concepts** (324 artifacts, 1318 tracked
      files counting iter-* contents), committed as `3f28671`. Excluded concept 01 (already on the
      new pipeline) and the 9 freeform concepts (spec non-goal).

### Validation
**Real bulk run (committed):**
- [x] 1318 staged changes were **all** git renames (`R`, zero add/delete pairs) → history fully
      preserved. Post-commit, `git log --follow archive/concept_analysis_pre_rework/07-maglif/analysis.md`
      shows the pre-move commits `45c9db5`/`ebcf1c3`/`e5a2cb2` (FR-5). ✓
- [x] `design-points/` and `review.md` remain tracked at the live path for archived concepts (FR-6).
      Live dirs now contain only `design-points/`, `review.md` (where present), `__pycache__/`, and
      ambiguous one-offs — cold-start ready (spec §Edge Cases). ✓
- [x] Mechanism cross-checked beforehand on a scratch git repo (history retention + exclusion
      boundary + cold-start), and the glob-handling fix verified there.

**What We Know Works After This Phase:** All 30 old-pipeline concepts archived with git history
retained and the correct include/exclude boundary; the live paths are cold-start ready for the
Phase 1 regen runner.

---

## Phase 3: Status stats columns

### Goal
Deliver FR-7: `status` shows `P_native`, native LCOE, and `result_1gw` LCOE per concept alongside
the existing state/iteration columns.

### Assumption Under Test
Module-loading `model_setup.py` (explorer pattern) yields `native.costs.lcoe` / `result_1gw.costs.lcoe`,
and failures (un-migrated concepts) degrade to blank cells without breaking the table.

### Test Stencil (Write This First)
```python
# test_status_stats.py
def test_load_lcoe_from_three_forward_module(tmp_path):
    # fixture: tests/fixtures/concept01_model_setup.py (three-forward, already present)
    stats = load_concept_stats(FIXTURE_CONCEPT_DIR)  # dir with model_setup.py + analysis.md
    assert stats.native_lcoe == pytest.approx(stats.native_lcoe)  # numeric, finite
    assert stats.result_1gw_lcoe > 0
    assert stats.p_native == 233.0  # from frontmatter P-Native

def test_stats_blank_when_no_model_setup(tmp_path):
    stats = load_concept_stats(tmp_path)  # empty dir
    assert stats.native_lcoe is None and stats.result_1gw_lcoe is None
```

### Changes Required

#### 1. Module loader helper
**File:** `exploration/concept_analysis/scripts/lib/model_stats.py` (NEW)
- [x] `_load_module(path)` — copy of the explorer's loader (stdout redirected via
      `redirect_stdout(StringIO())`). Does **not** import `concept_explorer`.
- [x] `load_concept_stats(concept_dir) -> ConceptStats(p_native, native_lcoe, result_1gw_lcoe)` —
      reads `P-Native` from frontmatter, loads `model_setup.py`, reads `native.costs.lcoe` /
      `result_1gw.costs.lcoe`; returns `None`s on any exception (never raises).

#### 2. Wire into status
**File:** `exploration/concept_analysis/scripts/run_analysis.py` (`cmd_status`)
- [x] Added `P_nat` / `Native` / `1GWe` columns to the header and per-row print; blank (`-`) when
      a stat is `None`. Truncated the Concept Name to 40 chars so the numeric columns stay aligned.
- [x] Kept the existing summary line; extended the legend with a Stats line.

### Validation
**Automated:**
- [x] `uv run python -m pytest test_status_stats.py` → 4 passed
- [x] `uv run python -m pytest` (full suite) → 423 passed, 5 skipped, 4 failed (same pre-existing
      `test_concepts_v2.py` data-driven `StopIteration`; no new regressions).
**Manual:**
- [x] `status 01-hts-compact-tokamak` → `P_nat=233  Native=592  1GWe=544` ($/MWh).
- [x] `status 07-maglif 03-...` (archived → no live `model_setup.py`) → blanks (`-`), table aligned.

**What We Know Works After This Phase:** FR-7 columns resolve from the three-forward
`model_setup.py` (`native`/`result_1gw`) and frontmatter (`P-Native`), with graceful blank
degradation for concepts without a live three-forward model.

---

## Environment Setup
**See CLAUDE.md** — all Python via `uv run python ...`. Tests:
`uv run python -m pytest exploration/concept_analysis/scripts/`.

## Risk Management
- **Phase 1 — scoring regression:** `stage_flags()` must reproduce scoring's current flag output
  byte-for-byte; covered by a parity test + the existing suite.
- **Phase 1 — `model-critic` flag mismatch:** it rejects `--force`; `stage_flags("model-critic")`
  returns no `--force`; covered by a unit test.
- **Phase 2 — destructive `git mv`:** allowlist-only (never a denylist); confirm exclusions after;
  the spec's R2 mirror caveat does not apply (moving within git, not touching R2 binaries).
- **Phase 3 — executing arbitrary module code in `status`:** stdout redirected + per-concept
  try/except → blank on failure (explorer-proven).

## Implementation Notes

### Phase 1 Completion
**Completed:** 2026-05-31
**Changes Made:**
- `run_scoring_pipeline.py`: added `stage_flags(stage, max_passes=None)`; refactored
  `run_for_concept` to append `*stage_flags(...)` (new optional `max_passes` param) instead of
  hardcoding `--force`/`--skip-review-gate`; threaded `max_passes` through `run_parallel_stage`'s
  `executor.submit`.
- `run_regen_batch.py` (NEW): sibling runner — explicit `concepts` positional, `analyze` →
  `model-critic` over the scoring pool, stops after critic, non-zero exit on any failure.
- `test_regen_batch.py` (NEW): 7 tests — `stage_flags` parity/analyze/critic + CLI contract.

**Issues Encountered:** None. Full suite has 4 pre-existing `test_concepts_v2.py` failures
(data-driven `StopIteration`, no "pending" concept) confirmed unrelated by reverting my edits.

**Deviations from Plan:** `stage_flags` takes `(stage, max_passes)` rather than an argparse
`args` object (simpler/more testable); tests adapted to that signature. `analyze`-failure
detection relies on the existing `"validation exhausted"` stdout heuristic + returncode, and
`model-critic` on its `sys.exit(rc)` — no new failure-parsing needed.

### Phase 2 Completion
**Completed:** 2026-05-31
**Changes Made:**
- Finalized the canonical archive procedure in this plan's "The Procedure" section — no helper
  script, per operator direction.
- Validated the MOVE allowlist against all 41 real concept dirs. Added `address_log.md` (8 dirs)
  and `research_log.json` (30 dirs) to the allowlist as pipeline-produced logs. Confirmed
  `design-points/` (31 dirs) and `review.md` (17 dirs) as excludes. Classified ambiguous one-offs
  (`change_requests_*.md`, `*_parameter_audit.md`, `*_concept_downselect.md`) as
  leave-in-place (not on allowlist; safe failure mode).
- Fixed a glob bug in the draft procedure: `[ -e "$src/iter-*" ]` tests the literal glob and moves
  nothing — replaced with an inner `for match in $src/$p` loop that expands globs and skips
  unmatched patterns.

**Bulk execution:** Archived all 30 regeneratable old-pipeline concepts in one pass (commit
`3f28671`). Archive set computed from concept records: all non-freeform concepts except 01
(already regenerated). Excluded the 9 freeform (4 `fit_grade=None`: 02/16/35/38; 5 freeform-routed:
17b/19/27/28/39) per the spec non-goal. 8 files were untracked (newly generated, never committed) →
plain-moved; the rest were git-mv renames. Final index: 1318 renames, history preserved.

**Issues Encountered:** I initially mis-scoped this phase as a per-concept just-in-time operator
action and deferred it — wrong. The spec/operator intent is a bulk sweep of all old-pipeline
concepts now; corrected and executed.

**Deviations from Plan:** Allowlist expanded beyond the spec's illustrative `e.g.` list (added
`address_log.md` + `research_log.json`) based on the real-dir inventory. The archive was committed
as its own isolated commit (Phase 1 code changes remain unstaged).

### Phase 3 Completion
**Completed:** 2026-05-31
**Changes Made:**
- `lib/model_stats.py` (NEW): `ConceptStats` + `load_concept_stats(concept_dir)` — module-loads
  `model_setup.py` (explorer pattern, stdout-redirected, no `concept_explorer` import) for
  `native.costs.lcoe` / `result_1gw.costs.lcoe`, reads `P-Native` from frontmatter. Never raises.
- `run_analysis.py` `cmd_status`: three new columns (`P_nat` / `Native` / `1GWe`), name truncation
  for alignment, extended legend; import of `load_concept_stats`.
- `test_status_stats.py` (NEW): 4 tests — real three-forward concept resolves all stats; blank on
  missing `model_setup.py`; `P_native` read without a model; un-loadable module degrades to blank.

**Issues Encountered:** Long concept names overflowed the name column and misaligned the new numeric
columns (latent in the original, exposed by adding trailing numeric fields) — fixed with a 40-char
truncation + ellipsis.

**Deviations from Plan:** None of substance. The module loader is `_load_module` (private) returning
the module; `load_concept_stats` returns a frozen `ConceptStats` dataclass rather than a dict.

---

**Status**: Draft → In Progress → **Complete** (all 3 phases)
