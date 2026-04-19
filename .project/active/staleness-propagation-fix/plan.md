# Implementation Plan: Staleness Propagation Fix

**Status:** Complete
**Created:** 2026-04-19
**Last Updated:** 2026-04-19

## Source Documents
- **Spec:** `.project/active/staleness-propagation-fix/spec.md`
- **Design:** `.project/active/staleness-propagation-fix/design.md` — See here for component details, signatures, invariants, and architecture

## Implementation Strategy

**Phasing Rationale:**
Strip helpers first (Phase 1) because every subsequent change depends on them. Then the two public API surfaces (Phase 2), then wiring into producers and call sites (Phase 3), then data cleanup (Phase 4). Each phase is independently testable and the build order means a bug in helpers is caught before it can propagate through the dispatcher or producers.

**Critical Path:**
Phase 1 (strip helpers) → Phase 2 (`clear_staleness` + `propagate_staleness` signature) → Phase 3 (wire call sites) → Phase 4 (data cleanup)

**First Proof Point:**
Phase 1 unit tests passing — `_strip_py_stale_marker` and `_strip_md_stale_marker` produce exact expected output on fixture inputs covering all edge cases from `design.md#implementation-notes`.

**Overall Validation Approach:**
- Each phase starts with tests
- Each phase has automated validation via pytest
- Existing `test_failure_chains.py` suite runs green throughout

---

## Phase 1: Strip Helpers + `remove_frontmatter_field`

### Goal
Build and test the three marker-stripping primitives. This is the design's identified first risk — every subsequent phase depends on these behaving exactly right.

### Assumption Under Test
We can reliably strip `# STALE:` from `.py` first lines and `Stale`/`Stale-Reason` from `.md` frontmatter without damaging surrounding content.

### Test Stencil (Write This First)
```python
# scripts/test_staleness.py — Phase 1 tests

import pytest
from lib.frontmatter import remove_frontmatter_field
from lib.state import _strip_py_stale_marker, _strip_md_stale_marker

class TestStripPyStaleMarker:
    def test_removes_stale_first_line(self, tmp_path):
        p = tmp_path / "model_setup.py"
        p.write_text("# STALE: analysis-updated-iter-3\nimport numpy\n")
        _strip_py_stale_marker(p)
        assert p.read_text() == "import numpy\n"

    def test_preserves_file_without_marker(self, tmp_path):
        p = tmp_path / "model_setup.py"
        original = "import numpy\nprint('hello')\n"
        p.write_text(original)
        _strip_py_stale_marker(p)
        assert p.read_text() == original

    def test_idempotent(self, tmp_path):
        p = tmp_path / "model_setup.py"
        p.write_text("# STALE: reason\nimport numpy\n")
        _strip_py_stale_marker(p)
        _strip_py_stale_marker(p)
        assert p.read_text() == "import numpy\n"

    def test_preserves_docstring_after_marker(self, tmp_path):
        p = tmp_path / "model_setup.py"
        p.write_text('# STALE: reason\n"""Module doc."""\nimport numpy\n')
        _strip_py_stale_marker(p)
        assert p.read_text() == '"""Module doc."""\nimport numpy\n'

    def test_preserves_blank_line_after_marker(self, tmp_path):
        p = tmp_path / "model_setup.py"
        p.write_text("# STALE: reason\n\nimport numpy\n")
        _strip_py_stale_marker(p)
        assert p.read_text() == "\nimport numpy\n"

class TestStripMdStaleMarker:
    def test_removes_both_fields(self, tmp_path):
        p = tmp_path / "review.md"
        p.write_text("---\nTitle: Review\nStale: true\nStale-Reason: updated\n---\nBody\n")
        _strip_md_stale_marker(p)
        text = p.read_text()
        assert "Stale" not in text
        assert "Title: Review" in text
        assert "Body" in text

    def test_removes_stale_without_reason(self, tmp_path):
        p = tmp_path / "review.md"
        p.write_text("---\nTitle: Review\nStale: true\n---\nBody\n")
        _strip_md_stale_marker(p)
        assert "Stale" not in p.read_text()

    def test_preserves_file_without_stale(self, tmp_path):
        p = tmp_path / "review.md"
        original = "---\nTitle: Review\n---\nBody\n"
        p.write_text(original)
        _strip_md_stale_marker(p)
        assert p.read_text() == original

    def test_idempotent(self, tmp_path):
        p = tmp_path / "review.md"
        p.write_text("---\nStale: true\nStale-Reason: r\n---\nBody\n")
        _strip_md_stale_marker(p)
        _strip_md_stale_marker(p)
        assert "Stale" not in p.read_text()

class TestRemoveFrontmatterField:
    def test_removes_existing_field(self):
        text = "---\nTitle: X\nStale: true\n---\nBody"
        result = remove_frontmatter_field(text, "Stale")
        assert "Stale" not in result
        assert "Title: X" in result

    def test_noop_when_field_absent(self):
        text = "---\nTitle: X\n---\nBody"
        assert remove_frontmatter_field(text, "Stale") == text

    def test_preserves_field_order(self):
        text = "---\nA: 1\nStale: true\nB: 2\n---\n"
        result = remove_frontmatter_field(text, "Stale")
        assert result.index("A: 1") < result.index("B: 2")
```

### Changes Required

**See `design.md` for:**
- Strip helper edge cases → `design.md#implementation-notes`
- Helper location decision → `design.md#key-bets--decisions`

**Specific file changes:**

#### 1. Test File
**File:** `exploration/concept_analysis/scripts/test_staleness.py` (NEW — write first)
- [ ] Create test file with Phase 1 test classes above
- [ ] Tests for `_strip_py_stale_marker`: marker present, absent, idempotent, docstring after, blank line after
- [ ] Tests for `_strip_md_stale_marker`: both fields, stale-only, absent, idempotent, field order preserved
- [ ] Tests for `remove_frontmatter_field`: present, absent, order preserved

#### 2. `remove_frontmatter_field`
**File:** `exploration/concept_analysis/scripts/lib/frontmatter.py` (MODIFY)
- [ ] Add `remove_frontmatter_field(text, key) -> str` — companion to `update_frontmatter_field` at line 56

#### 3. Strip Helpers
**File:** `exploration/concept_analysis/scripts/lib/state.py` (MODIFY)
- [ ] Add `_strip_py_stale_marker(path)` — removes `# STALE:` first line iff present
- [ ] Add `_strip_md_stale_marker(path)` — removes `Stale` and `Stale-Reason` fields via `remove_frontmatter_field`

### Validation

**Automated:**
- [ ] `cd exploration/concept_analysis && uv run python -m pytest scripts/test_staleness.py -v` → All Phase 1 tests pass
- [ ] `uv run python -m pytest scripts/test_failure_chains.py -v` → No regressions

**What We Know Works After This Phase:**
Strip helpers correctly handle all edge cases. `remove_frontmatter_field` works as a general-purpose frontmatter field remover. The foundation for `clear_staleness` is solid.

---

## Phase 2: `clear_staleness` Dispatcher + `propagate_staleness` Signature

### Goal
Add the two public API surfaces: `clear_staleness` (dispatches to strip helpers by artifact name) and the `regenerated` parameter on `propagate_staleness`.

### Assumption Under Test
`clear_staleness` correctly routes to the right strip helper based on file extension. `propagate_staleness` skips members of the `regenerated` set while still stamping others.

### Test Stencil (Write This First)
```python
# Add to scripts/test_staleness.py — Phase 2 tests

from lib.state import clear_staleness, propagate_staleness

class TestClearStaleness:
    def test_clears_py_artifact(self, tmp_path):
        (tmp_path / "07-test" / "model_setup.py").parent.mkdir()
        p = tmp_path / "07-test" / "model_setup.py"
        p.write_text("# STALE: reason\nimport numpy\n")
        result = clear_staleness("07-test", "model_setup.py", analyses_dir=tmp_path)
        assert result is True
        assert "STALE" not in p.read_text()

    def test_clears_md_artifact(self, tmp_path):
        # similar for review.md with frontmatter

    def test_returns_false_when_no_marker(self, tmp_path):
        # clean file → returns False

class TestPropagateStalenessRegenerated:
    def test_skips_regenerated_member(self, tmp_path, monkeypatch):
        # seed concept dir with model_setup.py and review.md
        # call propagate_staleness(..., regenerated={"model_setup.py"})
        # assert model_setup.py is NOT stamped, review.md IS stamped

    def test_stamps_all_when_regenerated_empty(self, tmp_path, monkeypatch):
        # regenerated=set() → all downstream stamped
```

### Changes Required

**See `design.md` for:**
- Function signatures → `design.md#implementation-notes`
- Dispatcher scope (`.py` and `.md` only, not explorer) → `design.md#key-bets--decisions`
- Required invariants → `design.md#required-invariants`

**Specific file changes:**

#### 1. Tests
**File:** `exploration/concept_analysis/scripts/test_staleness.py` (MODIFY)
- [ ] Add `TestClearStaleness` class: clears `.py`, clears `.md`, returns False on clean, idempotent
- [ ] Add `TestPropagateStalenessRegenerated` class: skips regenerated, stamps non-regenerated, empty set stamps all

#### 2. `clear_staleness`
**File:** `exploration/concept_analysis/scripts/lib/state.py` (MODIFY)
- [ ] Add `clear_staleness(concept_id, artifact, analyses_dir) -> bool` dispatching to `_strip_py_stale_marker` for `.py` and `_strip_md_stale_marker` for `.md`

#### 3. `propagate_staleness` signature
**File:** `exploration/concept_analysis/scripts/lib/state.py` (MODIFY — line 59)
- [ ] Add `regenerated: Iterable[str]` parameter (required, no default)
- [ ] Skip stamping any path whose `.name` is in `regenerated`

### Validation

**Automated:**
- [ ] `uv run python -m pytest scripts/test_staleness.py -v` → All Phase 1 + Phase 2 tests pass
- [ ] `uv run python -m pytest scripts/ -v` → Full suite green (note: `propagate_staleness` callers will break until Phase 3 — tests that call them need the new arg. Check if any existing test calls `propagate_staleness` directly and patch if needed.)

**What We Know Works After This Phase:**
The two public APIs are correct in isolation. `clear_staleness` dispatches by artifact type. `propagate_staleness` respects the regeneration set. Ready to wire into the pipeline.

---

## Phase 3: Wire Call Sites + Producer Clearing

### Goal
Connect `clear_staleness` and the updated `propagate_staleness` to all producers and call sites. Add in-loop regression tests.

### Assumption Under Test
End-to-end loop behavior produces correct marker state: PASS leaves canonical `model_setup.py` clean; `model_ok=False` leaves it stamped.

### Test Stencil (Write This First)
```python
# Add to scripts/test_staleness.py — Phase 3 regression tests

class TestLoopStalenessRegression:
    """Drive run_stage1_loop with scripted Claude, assert marker state."""

    def test_pass_iteration_leaves_canonical_clean(self, tmp_path):
        # Seed concept with analysis.md
        # Drive loop with _fake_claude returning PASS-worthy responses
        # Assert: canonical model_setup.py does NOT start with "# STALE:"

    def test_model_fail_stamps_canonical(self, tmp_path):
        # Drive loop with model_ok=False scenario
        # Assert: canonical model_setup.py DOES start with "# STALE:"

    def test_pass_stamps_preexisting_review_synthesis(self, tmp_path):
        # Pre-seed review.md and synthesis.md
        # PASS run → both carry Stale: true
```

### Changes Required

**See `design.md` for:**
- In-loop data flow diagrams → `design.md#architecture`
- Ordering rule (copy first, then clear) → `design.md#implementation-notes`
- Call site locations → `design.md#research-findings`

**Specific file changes:**

#### 1. Regression Tests
**File:** `exploration/concept_analysis/scripts/test_staleness.py` (MODIFY)
- [ ] Add `TestLoopStalenessRegression` class with PASS/fail/pre-existing-artifacts tests
- [ ] Reuse `_fake_claude.py` pattern from `test_failure_chains.py`

#### 2. Loop Call Site
**File:** `exploration/concept_analysis/scripts/lib/loop.py` (MODIFY)
- [ ] Line 238: Change `propagate_staleness(cid, f"analysis-updated-iter-{iter_num}")` → `propagate_staleness(cid, f"analysis-updated-iter-{iter_num}", regenerated={"analysis.md", "model_setup.py"} if model_ok else {"analysis.md"})`
- [ ] Import `clear_staleness` from `lib.state`

#### 3. `_update_canonical_files` Clearing
**File:** `exploration/concept_analysis/scripts/lib/loop.py` (MODIFY — line 882)
- [ ] After `shutil.copy2(iter_model, concept_dir / "model_setup.py")` (line 897), add `clear_staleness(concept_dir.name, "model_setup.py")` when `model_ok=True`

#### 4. Loop Analysis Producers
**File:** `exploration/concept_analysis/scripts/lib/loop.py` (MODIFY)
- [ ] In `_run_cold_start` / `_run_feedback_pass`: call `clear_staleness(cid, "analysis.md")` after successful analyze write

#### 5. `cmd_analyze --feedback` Call Site
**File:** `exploration/concept_analysis/scripts/run_analysis.py` (MODIFY — line 456)
- [ ] Change to `propagate_staleness(cid, "feedback-applied-from-change-requests", regenerated={"analysis.md"})`

#### 6. Standalone Producers
**File:** `exploration/concept_analysis/scripts/run_analysis.py` (MODIFY)
- [ ] `cmd_model_setup`: after successful write, call `clear_staleness(cid, "model_setup.py")`
- [ ] `cmd_review`: after successful write, call `clear_staleness(cid, "review.md")`
- [ ] `cmd_synthesize`: after successful write, call `clear_staleness(cid, "synthesis.md")`
- [ ] Add `clear_staleness` to the import from `lib.state`

#### 7. Explorer Extractor (verification only)
**File:** `exploration/concept_explorer/extract_explorer_data.py` (READ ONLY)
- [ ] Verify lines 812-816 still contain the inline `.stale` sidecar unlink — no edit needed

### Validation

**Automated:**
- [ ] `uv run python -m pytest scripts/test_staleness.py -v` → All tests pass including regression
- [ ] `uv run python -m pytest scripts/ -v` → Full test suite green
- [ ] `uv run python -m pytest scripts/test_failure_chains.py -v` → No regressions

**What We Know Works After This Phase:**
The full pipeline produces correct staleness markers. PASS iterations leave clean canonicals. Failed model iterations stamp correctly. Standalone producers clear their markers. The bug is fixed.

---

## Phase 4: Data Cleanup for Concepts 07, 09, 10

### Goal
Strip the false `# STALE:` markers from the three misannotated concepts. Separate commit, independently revertable.

### Assumption Under Test
The canonical `model_setup.py` content for each concept matches its last clean iter-N copy (minus the stale marker).

### Test Stencil (Write This First)
```bash
# Pre-cleanup verification — run manually
for cid in 07-maglif 09-field-reversed-configuration 10-dense-plasma-focus; do
    echo "=== $cid ==="
    head -1 exploration/concept_analysis/analyses/$cid/model_setup.py
done
# Expect: all three show "# STALE: ..."
```

### Changes Required

**Specific file changes:**

- [ ] Identify the exact concept directory names for 07, 09, 10
- [ ] For each: verify canonical `model_setup.py` content (minus `# STALE:` line) matches the last clean iter-N `model_setup.py`
- [ ] Strip the `# STALE:` first line from each canonical `model_setup.py`
- [ ] Verify no other false markers exist across the analyses directory

### Validation

**Automated:**
- [ ] `grep -rc '^# STALE:' exploration/concept_analysis/analyses/*/model_setup.py` → 0 matches for 07, 09, 10

**Manual:**
- [ ] Diff each cleaned canonical against its iter-N source — should be identical
- [ ] `uv run python -m pytest scripts/ -v` → Full suite still green

**What We Know Works After This Phase:**
`concept_status.md` can be read at face value. No false stale markers remain in the repo. The branch is ready for PR.

---

## Risk Management

**See `design.md#potential-risks` for detailed risk analysis**

**Phase-Specific Mitigations:**
- **Phase 1**: Exact byte-level assertions on strip helper output catch content corruption immediately
- **Phase 2**: Existing tests that call `propagate_staleness` may need the new `regenerated` arg — fix these as part of the signature change to keep the suite green
- **Phase 3**: Regression tests modeled on `test_failure_chains.py` TestH01 pattern, using `_fake_claude.py` — proven approach
- **Phase 4**: Verify-before-strip protocol ensures we only remove markers, not content

## Implementation Notes

### Phase 1 Completion
**Completed:** 2026-04-19
**Actual Changes:**
- Created `exploration/concept_analysis/scripts/test_staleness.py` with `TestStripPyStaleMarker` (7 cases), `TestStripMdStaleMarker` (6 cases), `TestRemoveFrontmatterField` (5 cases).
- Added `remove_frontmatter_field(text, key) -> str` in `lib/frontmatter.py` — regex matches the full line including trailing newline so removal leaves no blank line. Handles values containing colons (e.g. `Stale-Reason: reason: with: colons`).
- Added `_strip_py_stale_marker(path)` and `_strip_md_stale_marker(path)` helpers in `lib/state.py`. Both return `bool` (True if a marker was removed). Missing-file is a safe no-op.
- Imported `remove_frontmatter_field` and `Iterable` into `lib/state.py`.

**Issues:** None.

**Deviations:** Added two extra edge cases beyond plan minimum — `test_missing_file_is_noop` and `test_no_trailing_newline_preserved` for .py, and `test_removes_field_with_colon_in_value` for frontmatter. These are cheap and guard against the exact subtle failure modes design.md calls out.

---

### Phase 2 Completion
**Completed:** 2026-04-19
**Actual Changes:**
- Added `TestClearStaleness` (7 cases: .py, .md, returns False on clean, missing, idempotent, unsupported-suffix raises ValueError).
- Added `TestPropagateStalenessRegenerated` (3 cases: skips member, stamps all when empty, idempotent).
- Added `clear_staleness(concept_id, artifact, analyses_dir=None)` dispatcher in `lib/state.py` — raises `ValueError` for unsupported suffixes (explicitly rejecting explorer JSON since its producer handles sidecars inline).
- Changed `propagate_staleness` signature: added required `regenerated: Iterable[str]` parameter; skips any downstream whose `.name` is in the regenerated set.

**Issues:** The existing default `analyses_dir: Path = ANALYSES_DIR` captures the module-level constant at def-time, so test patches on `lib.state.ANALYSES_DIR` were not taking effect. Fixed in Phase 3 by switching to `analyses_dir: Path | None = None` with inline resolution.

**Deviations:** None.

---

### Phase 3 Completion
**Completed:** 2026-04-19
**Actual Changes:**
- Added `TestLoopStalenessRegression` with 3 regression tests (PASS leaves canonical clean; model_ok=False stamps canonical; PASS stamps pre-existing review/synthesis).
- `lib/loop.py`:
  - Line 238: Call site now passes `regenerated = {"analysis.md"}` plus `"model_setup.py"` iff `model_ok`.
  - `_update_canonical_files`: after `shutil.copy2` on successful promotion, calls `clear_staleness(concept_dir.name, "model_setup.py", analyses_dir=concept_dir.parent)` — ordering is copy-then-clear per design.md#implementation-notes.
  - `_run_cold_start` / `_run_feedback_pass`: both call `clear_staleness(cid, "analysis.md", analyses_dir=analysis_path.parent.parent)` after a successful write.
  - Imported `clear_staleness` from `lib.state`.
- `run_analysis.py`:
  - `cmd_analyze --feedback` (line 456): now passes `regenerated={"analysis.md"}`.
  - `cmd_model_setup`, `cmd_review`, `cmd_synthesize`: each calls `clear_staleness(cid, "<artifact>")` after successful validated write.
  - Imported `clear_staleness` from `lib.state`.
- Switched `propagate_staleness` and `clear_staleness` to `analyses_dir: Path | None = None` sentinel so module-level ANALYSES_DIR is resolved at call time (enables test patching).
- Verified explorer extractor at `concept_explorer/extract_explorer_data.py:812-816` still contains inline sidecar unlink — read-only check, no edit.

**Issues:**
1. Default-arg capture gotcha — test patches on ANALYSES_DIR did not take effect because Python evaluates default args at def-time. Fixed with `None` sentinel + inline resolution.
2. `max_passes=1` short-circuits to `SINGLE_PASS` before the propagate call fires (loop.py:213). Regression tests needed `max_passes=2` to exercise the propagate path.
3. `run_model` in `lib.claude` shares the patched `subprocess.run` with the Claude CLI call. Followed the existing `TestIntegration_ModelSetup` pattern (test_failure_chains.py:983) and patched `lib.loop.run_model` directly instead.
4. Feedback validator requires `Category: analysis|model` on each finding. Test fixture initially used `Category: other`, causing retry. Switched to PASS verdict with patched `run_model_return=(False, ...)` to exercise the model_ok=False path cleanly — same state transition, fewer scripted invocations needed.

**Deviations:**
- Made the `analyses_dir` parameter accept `None` (with inline resolution) rather than a direct default of `ANALYSES_DIR`. This was not in the design but was the minimum fix needed for test patching to work. The function contract is unchanged from the caller's perspective.

---

### Phase 4 Completion
**Completed:** 2026-04-19
**Actual Changes:**
- Identified concepts: `07-maglif`, `09-qi-stellarator-hts`, `10-large-scale-stellarator`.
- Verified each canonical `model_setup.py` minus the `# STALE:` line matches its last clean iter-N copy (cmp -s):
  - 07-maglif: canonical == iter-9/model_setup.py (last iter with model_ok=True).
  - 09-qi-stellarator-hts: canonical == iter-9/model_setup.py.
  - 10-large-scale-stellarator: canonical == iter-3/model_setup.py.
- Stripped `# STALE:` first line from each canonical via `tail -n +2`.
- Post-strip: canonical files are byte-identical to their iter-N sources.
- `grep -c '^# STALE:' ...` returns 0 for all three.

**Issues:** Repo-wide grep turned up 10 files with `# STALE:` markers (not just 3). Per spec §Scope and plan Phase 4 scope, left the other 7 alone — several belong to in-progress concept work visible in `git status` (02, 13, 16). The design explicitly scoped cleanup to 07/09/10 and the branch tip verification is grep-restricted to those three.

**Deviations:** None.

---

**Status**: Draft → In Progress → **Complete**

## Final Validation Summary

- `uv run python -m pytest scripts/ -q`: **236 passed, 5 skipped** (no regressions)
- Phase 1: 18/18 strip-helper tests passing
- Phase 2: 10/10 dispatcher + regeneration-set tests passing
- Phase 3: 3/3 in-loop regression tests passing (PASS clean, model_ok=False stamps, pre-existing review/synthesis stamped)
- Phase 4: 0 `# STALE:` markers remaining on 07/09/10 canonicals, each matches its last clean iter-N source byte-for-byte
