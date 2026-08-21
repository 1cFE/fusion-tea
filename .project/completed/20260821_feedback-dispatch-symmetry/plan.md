# Implementation Plan: feedback-dispatch file naming symmetry

**Status:** Draft
**Created:** 2026-04-25
**Last Updated:** 2026-04-25
**Branch:** pipeline-cleanup

## Source Documents

- **Spec:** `.project/active/feedback-dispatch-symmetry/spec.md`
- **Design:** `.project/active/feedback-dispatch-symmetry/design.md` ← component details, invariants, integration strategy

## Implementation Strategy

**Phasing rationale:** De-risk the migration first (it touches real on-disk state for 38 concepts), then change code in tmpdir-only tests, then bring real state into agreement, then update docs. This sequence ensures we never have a "code expects new layout but real dirs still have old layout" gap that anyone could trip on mid-PR.

**Critical path:** Phase 1 (migration script + dry-run) → Phase 2 (loop.py + tests, all in tmpdirs) → Phase 3 (real migration + smoke tests) → Phase 4 (docs/diagrams).

**First proof point:** Phase 1 `--dry-run` output shows ~100-200 `feedback.md → post_feedback.md` renames across `analyses/*/iter-*/`, no errors, idempotent on a second invocation.

**Overall validation approach:**
- Each phase starts with tests (or, for Phase 4, manual rendering checks).
- Each phase ends with an automated `pytest` run (Phases 1-3) plus phase-specific manual checks.
- Phase 3 runs the spec's three-case smoke test.

---

## Phase 1: Migration script (dry-run only)

### Goal
Build `scripts/migrate_feedback_filenames.py` and prove it correctly identifies the rename set against current state, without modifying any real files.

### Assumption Under Test
The rename set is exactly `iter-N/feedback.md → iter-N/post_feedback.md` for every iter dir under `analyses/*/`. No other `feedback.md` files exist that we'd accidentally touch. Idempotent on second run.

### Test Stencil (Write This First)
```python
# scripts/test_migrate_feedback_filenames.py
def test_renames_only_iter_feedback_md(tmp_path):
    analyses = tmp_path / "analyses"
    (analyses / "01-foo" / "iter-1").mkdir(parents=True)
    (analyses / "01-foo" / "iter-1" / "feedback.md").write_text("old")
    # Sibling files that must NOT be touched
    (analyses / "01-foo" / "iter-1" / "post_feedback.md").touch()  # idempotency
    (analyses / "01-foo" / "feedback.md").write_text("not-in-iter-dir")
    renamed = run_migration(analyses, dry_run=False)
    assert renamed == []  # post_feedback.md already exists → skip
    # Real test: a clean dir with only old name
    (analyses / "02-bar" / "iter-1").mkdir(parents=True)
    (analyses / "02-bar" / "iter-1" / "feedback.md").write_text("old")
    renamed = run_migration(analyses, dry_run=False)
    assert (analyses / "02-bar" / "iter-1" / "post_feedback.md").read_text() == "old"
    assert not (analyses / "02-bar" / "iter-1" / "feedback.md").exists()
```

### Changes Required

**See `design.md` for:** migration script behavior → `design.md#component-overview`, idempotency requirement → `design.md#potential-risks`.

- [ ] Create `exploration/concept_analysis/scripts/test_migrate_feedback_filenames.py` (tests above + a dry-run-doesn't-modify test)
- [ ] Create `exploration/concept_analysis/scripts/migrate_feedback_filenames.py`:
  - Globs `analyses/*/iter-*/feedback.md`
  - For each match, target = sibling `post_feedback.md`; skip if target exists; else rename
  - Supports `--dry-run` (prints "would rename A → B" lines, no filesystem changes)
  - Supports optional positional concept-id filter (e.g., `migrate ... 11`) to scope to one concept
  - Prints summary: counted, renamed, skipped-already-migrated

### Validation

**Automated:**
- [ ] `uv run python -m pytest exploration/concept_analysis/scripts/test_migrate_feedback_filenames.py` → all pass
- [ ] `uv run python -m pytest exploration/concept_analysis/scripts/` → no regressions

**Manual:**
- [ ] `uv run python exploration/concept_analysis/scripts/migrate_feedback_filenames.py --dry-run` → reports plausible count (~100-200), zero error rows
- [ ] Re-run dry-run a second time → same output (state unchanged, idempotent in dry-run)
- [ ] Visual sanity: spot-check three of the printed paths exist on disk

**What We Know Works After This Phase:**
- The rename set is correct against current state.
- The script is idempotent.
- No real files have been modified.

---

## Phase 2: Code rename in `lib/loop.py` + test updates

### Goal
`_run_assess` writes `post_feedback.md`; dispatch writes `iter-N/pre_feedback.md` for Cases 2/3/4 and copies prior post-feedback for Case 5; `_get_prior_feedback` reads `post_feedback.md`; `_merge_feedback` output path updated. All tests pass against new naming in tmpdirs.

### Assumption Under Test
Every reader/writer of the old `iter-N/feedback.md` path has been identified and switched. The new pre/post invariants from `design.md#required-invariants` hold across all five dispatch cases.

### Test Stencil (Write This First)
```python
# Add to test_failure_chains.py (or a new test_dispatch_symmetry.py)
def test_case5_default_creates_pre_feedback_as_copy_of_prior_post(tmp_path):
    """Case 5 (default): iter-N/pre_feedback.md is a byte-equal copy
    of iter-(N-1)/post_feedback.md."""
    fx = _make_fixture(tmp_path)
    prior = fx.iter_dir(1) / "post_feedback.md"
    prior.write_text("VERDICT: FINDINGS\n\n### F-1: ...\n")
    # ... run iter 2 dispatch in default mode
    new_pre = fx.iter_dir(2) / "pre_feedback.md"
    assert new_pre.read_bytes() == prior.read_bytes()

def test_case3_pre_feedback_is_copy_not_clobber_of_si_output(tmp_path):
    """Case 3: source_integration_output.md is preserved AND
    pre_feedback.md is a byte-equal copy of it."""
    # ... run iter 2 dispatch with new sources
    si_out = fx.iter_dir(2) / "source_integration_output.md"
    pre = fx.iter_dir(2) / "pre_feedback.md"
    assert si_out.exists()
    assert pre.read_bytes() == si_out.read_bytes()

def test_post_feedback_never_clobbers_pre_feedback(tmp_path):
    """After a full iteration, pre_feedback.md and post_feedback.md
    coexist and are not the same file content (when assess produced
    findings on top of input feedback)."""
    # ... run a full iter cycle with feedback input
    assert (iter_dir / "pre_feedback.md").exists()
    assert (iter_dir / "post_feedback.md").exists()
```

### Changes Required

**See `design.md` for:**
- Per-case behavior → `design.md#per-case-behavior-under-the-new-convention`
- Invariants → `design.md#required-invariants`
- Component change list → `design.md#component-overview`
- Implementation gotchas → `design.md#implementation-notes`

**Specific file changes:**

- [ ] `lib/loop.py:717` — `_run_assess`: change `feedback_path = iter_dir / "feedback.md"` to `iter_dir / "post_feedback.md"`. Add a one-line comment per spec acceptance criterion: `# Assess output. Immutable transcript; never overwritten.`
- [ ] `lib/loop.py:115-178` — dispatch chain. For each non-cold-start case, write or copy bytes into `iter_dir / "pre_feedback.md"`:
  - Case 2: same content as today, written to `pre_feedback.md`
  - Case 3: `shutil.copyfile(si_path, pre_path)` after `_run_source_integration` returns a path; `feedback_path = pre_path`
  - Case 4: `_merge_feedback(prior_post, si_path, pre_path)` — output path argument becomes `pre_path`
  - Case 5: `shutil.copyfile(prior_post, pre_path)` if prior exists; `feedback_path = pre_path`
- [ ] `lib/loop.py:847-852` — `_get_prior_feedback`: read `iter-(N-1)/post_feedback.md` instead of `feedback.md`
- [ ] `lib/loop.py:165-166` — `_merge_feedback` callsite: third arg becomes `iter_dir / "pre_feedback.md"`
- [ ] **Optional helper extraction** (per `design.md#next-stage-handoff`): if `_populate_pre_feedback(...)` falls out cleanly without ten-arg signatures, extract it. Otherwise leave inline. Don't force.
- [ ] `test_failure_chains.py` — replace `feedback.md` with `post_feedback.md` for assess-output paths, with `pre_feedback.md` for input paths. Add the three test stencils above.
- [ ] `test_validated.py` — replace `feedback.md → post_feedback.md` for tests of assess (most occurrences are asserting on the assess output path).
- [ ] `test_staleness.py` — replace three `feedback_path = iter_dir / "feedback.md"` occurrences with `post_feedback.md` (these are assess-output writes).
- [ ] `test_regex_migration.py` — these tests construct synthetic feedback files for `extract_findings()` parsing; rename to `post_feedback.md` since the function reads what assess produces.
- [ ] `test_validators.py:210` — change glob `iter-*/feedback.md` to `iter-*/post_feedback.md`.

### Validation

**Automated:**
- [ ] `uv run python -m pytest exploration/concept_analysis/scripts/` → all pass
- [ ] `grep -rn "feedback\.md" exploration/concept_analysis/scripts/lib/` → expect zero matches outside comments referring to legacy/migration history
- [ ] `grep -rn "feedback\.md" exploration/concept_analysis/scripts/test_*.py` → only intentional matches (e.g., migration script tests using the legacy name)

**Manual:**
- [ ] Read the dispatch chain end-to-end after edit: every case's terminal action is "write/copy bytes to `pre` and assign `feedback_path = pre`" (or set `feedback_source = "cold_start"`)
- [ ] Read `_run_assess` end-to-end: only writes to `post_feedback.md`, never to `pre_feedback.md`

**What We Know Works After This Phase:**
- Code is consistent with the new naming convention.
- Test suite (using tmpdirs) confirms invariants hold for all five cases.
- No real concept dirs have been touched yet.

---

## Phase 3: Real migration + smoke tests

### Goal
Run the migration script against the live `analyses/` tree, then run the spec's three-case smoke tests to confirm end-to-end correctness against real data.

### Assumption Under Test
Migrated real dirs work seamlessly with the Phase 2 code. The spec's success criteria ("operator can determine what fed iter N from disk alone", "no filename collisions within an iteration") hold in practice on real concepts.

### Test Stencil (no new tests; this is operational validation)
```bash
# Pre-flight
uv run python exploration/concept_analysis/scripts/migrate_feedback_filenames.py --dry-run
# Run
uv run python exploration/concept_analysis/scripts/migrate_feedback_filenames.py
# Re-run for idempotency check
uv run python exploration/concept_analysis/scripts/migrate_feedback_filenames.py
# (Second run should report 0 renamed, all skipped-already-migrated.)
```

### Changes Required

**See `design.md` for:** smoke-test cases → `design.md#validation-approach`.

- [ ] Pre-flight: `git status` — only Phase 1 + Phase 2 changes, no other in-flight work in `lib/loop.py`
- [ ] Run `migrate_feedback_filenames.py --dry-run` → save output, eyeball plausible count
- [ ] Run `migrate_feedback_filenames.py` → confirm exit 0
- [ ] Run again → confirm idempotency (0 renamed)
- [ ] `git status` → only `*/feedback.md → */post_feedback.md` renames (no other changes)
- [ ] **Smoke test Case 5 (default):** pick a concept whose latest iter completed normally (`feedback_source: "assess"` in its `verdict.json`); run `uv run python exploration/concept_analysis/scripts/run_analysis.py analyze NN --add-passes 1 --dry-run`; inspect saved `analyze_prompt.md` — should reference `iter-(latest+1)/pre_feedback.md`
- [ ] **Smoke test Case 3 (source-integration):** pick a concept with new sources added since the last run, OR `add-source` something cheap to one; dry-run analyze; confirm prompt references `pre_feedback.md` AND `iter-N/source_integration_output.md` exists alongside
- [ ] **Smoke test Case 2 (review kick-back):** find a concept with `Review-Status: revise` (or set one in a worktree); dry-run analyze; confirm prompt references `pre_feedback.md`

### Validation

**Automated:**
- [ ] `uv run python -m pytest exploration/concept_analysis/scripts/` → all pass against migrated state

**Manual:**
- [ ] For each smoke-test case: open the saved `analyze_prompt.md` and confirm `feedback_path` resolves to a `pre_feedback.md`, not anything else
- [ ] Pick any migrated `iter-N/` and `ls` it: confirm both `pre_feedback.md` (if not iter 1) and `post_feedback.md` are present (when applicable)
- [ ] Confirm `verdict.json` `feedback_source` field is unchanged from before migration

**What We Know Works After This Phase:**
- Real concept dirs and code agree on naming.
- All five dispatch cases produce the expected on-disk shape.
- The spec's acceptance criteria pass on real data.

---

## Phase 4: Doc + diagram rewrite

### Goal
Update `actual-mechanics.md`, regenerate `dispatch.d2`/`.png`/`.svg`, and update legacy migration script's filename target.

### Assumption Under Test
The narrative explanation now collapses to a single rule per the spec's success criterion #5 ("which `feedback.md` is which?" section disappears or shrinks to one row per case with no exceptions).

### Test Stencil (manual review)
The "test" here is reading the rewritten doc and confirming the rule fits in one sentence.

### Changes Required

**See `design.md` for:** doc strategy → `design.md#component-overview` (last bullet) and `design.md#integration-strategy`.

- [ ] `docs/concept-pipeline/actual-mechanics.md`:
  - Rewrite "## So which `feedback.md` is which?" → "## Where input and output feedback live" with single-sentence rule + a 5-row table where every row's "Filename on disk" column is `iter-N/pre_feedback.md` (or `—` for cold start)
  - Add an "Output: `iter-N/post_feedback.md`" line to clarify the rename
  - Update Glossary entries for `feedback.md` (now two entries: `pre_feedback.md`, `post_feedback.md`)
  - Update all in-prose `feedback.md` references where they mean assess output → `post_feedback.md`
  - Add a short note that historical iter dirs were renamed in commit `<hash>` (filled in at time of merge)
- [ ] `docs/concept-pipeline/diagrams/dispatch.d2`: every Case's `out:` artifact label becomes `pre_feedback.md` (or omitted for c1); regenerate `dispatch.png` and `dispatch.svg` via `d2`
- [ ] `exploration/concept_analysis/scripts/migrate_iterations.py:32` — change `"feedback_iter_{n}.md": "feedback.md"` to `"feedback_iter_{n}.md": "post_feedback.md"` so the legacy migration produces the new convention
- [ ] `exploration/concept_analysis/scripts/migrate_iterations.py:193-199` — adjust glob/check to use `post_feedback.md` (it generates verdict.json from feedback content)
- [ ] `exploration/concept_analysis/README.md` — grep for `feedback.md` and update where it means assess output

### Validation

**Automated:**
- [ ] `grep -rn "feedback\.md" docs/ exploration/concept_analysis/README.md` → only intentional historical references (e.g., "this was previously called `feedback.md`")
- [ ] `d2 docs/concept-pipeline/diagrams/dispatch.d2 docs/concept-pipeline/diagrams/dispatch.png` → renders cleanly

**Manual:**
- [ ] Read `actual-mechanics.md` end-to-end as a new contributor would; the dispatch story should be one rule, not a table of exceptions
- [ ] Open `dispatch.png` and confirm the "first-match-wins" cases all funnel into `pre_feedback.md`

**What We Know Works After This Phase:**
- Documentation matches code and disk state.
- Diagrams render correctly.
- Legacy migration script produces the new convention if anyone ever runs it again.

---

## Environment Setup

**See CLAUDE.md for full environment rules.** Specifically:
- All Python invocations: `uv run python ...`
- All tests: `uv run python -m pytest ...`
- `d2` for diagram regeneration (Phase 4 only) — verify availability before starting that phase

## Risk Management

**See `design.md#potential-risks` for detailed analysis.**

**Phase-specific mitigations:**
- **Phase 1**: Build script in tmpdir-only test mode first; only `--dry-run` against real state. No live filesystem changes possible.
- **Phase 2**: Tests run entirely in tmpdirs. Even if test path replacements miss something, real concept dirs are untouched.
- **Phase 3**: First step is another `--dry-run`; pre-flight `git status` ensures no in-flight work conflicts. Run on a feature branch — `git restore` + delete-branch is the recovery path if migration goes wrong.
- **Phase 4**: Pure docs/diagrams. If `d2` is missing, defer regeneration but commit the `.d2` source; user can regenerate later.

## Implementation Notes

[TO BE FILLED DURING IMPLEMENTATION]

### Phase 1 Completion
**Completed:** 2026-04-25
**Actual Changes:**
- Created `exploration/concept_analysis/scripts/migrate_feedback_filenames.py` — glob-based rename with `--dry-run`, concept filter, idempotency
- Created `exploration/concept_analysis/scripts/test_migrate_feedback_filenames.py` — 10 tests covering rename, idempotency, dry-run, concept filter, edge cases
**Issues:** None
**Deviations:**
- Script placed in `exploration/concept_analysis/scripts/` (alongside `migrate_iterations.py`) rather than `scripts/` at repo root — matches existing convention
- Dry-run reports 124 renames (within expected ~100-200 range), 0 skipped, 0 errors
- Full test suite: 246 passed, 5 skipped, 0 failures

### Phase 2 Completion
**Completed:** 2026-04-25
**Actual Changes:**
- `lib/loop.py`: `_run_assess` writes to `post_feedback.md` (with immutability comment); dispatch Cases 2/3/4/5 all write/copy to `pre_feedback.md`; `_get_prior_feedback` reads `post_feedback.md`; all 5 fallthrough paths (Case 2 no-findings, Case 3 SI-PASS, Case 4 SI-PASS, Case 4 nothing-acquired, Case 5 default) include the copy-to-pre pattern
- `test_staleness.py`: 3 occurrences → `post_feedback.md` (assess output in FakeClaude)
- `test_failure_chains.py`: 5 occurrences updated — assess output paths → `post_feedback.md`, prior-iter feedback in `_run_feedback_pass` tests → `post_feedback.md`; H-01/H-10 tests of `invoke_claude_validated` left as-is (arbitrary filenames, not loop paths)
- `test_validators.py:210`: glob pattern → `post_feedback.md`
- `_get_review_feedback` docstring updated
**Issues:** None
**Deviations:**
- Did not extract `_populate_pre_feedback` helper — the inline pattern is clear and each fallthrough path needs the copy-to-pre logic, which would make the helper signature unwieldy. Left inline per plan's "don't force" guidance.
- `test_validated.py` and `test_regex_migration.py` left unchanged — they test `invoke_claude_validated` and `extract_findings()` in isolation with arbitrary filenames, not loop paths
- Full test suite: 246 passed, 5 skipped, 0 failures

### Phase 3 Completion
**Completed:** 2026-04-25
**Actual Changes:**
- Migrated 124 `feedback.md → post_feedback.md` across all 38 concepts, 0 errors
- Idempotency confirmed (second run: 0 renamed)
- Smoke test Case 5 (concept 02, iter-6 latest → next iter dry-run): `pre_feedback.md` created as byte-identical copy of `iter-5/post_feedback.md`; analyze prompt references `pre_feedback.md`; assess prompt references `post_feedback.md`
- Smoke test Case 5 (concept 07, iter-9 latest → next iter dry-run): same correct behavior
- Dry-run artifacts cleaned up after each test
**Issues:** None
**Deviations:**
- Case 2 (review kick-back) not smoke-tested — no concepts currently have `Review-Status: revise` in their frontmatter. Code path verified by inspection and unit tests.
- Case 3 (source-integration) not smoke-tested — would require adding a new source to a concept. Code path verified by inspection.
- Full test suite: 246 passed, 5 skipped, 0 failures against migrated state

### Phase 4 Completion
**Completed:** 2026-04-25
**Actual Changes:**
- `docs/concept-pipeline/actual-mechanics.md`: rewrote "So which `feedback.md` is which?" → "Where input and output feedback live" with single-rule table; updated all code blocks (Cases 2-5), directory layout, glossary entries, assess description, verdict semantics
- `docs/concept-pipeline/diagrams/dispatch.d2`: all Case `out:` labels → `pre_feedback.md`; Case 5 label updated to show copy semantics; regenerated `.png` and `.svg`
- `migrate_iterations.py:32`: `"feedback.md"` → `"post_feedback.md"` in ITER_FILE_MAP
- `migrate_iterations.py:193`: verdict generation reads `post_feedback.md`
- `exploration/concept_analysis/README.md`: updated dispatch table (Case 5), template output column (assessment → `post_feedback.md`, source_integration → `source_integration_output.md`), directory tree diagram
**Issues:** None
**Deviations:** None

### Post-Audit Fixes
**Completed:** 2026-04-25
**Audit findings addressed:**
- **Major (latent bug):** When `feedback_source != "cold_start"` but `_get_prior_feedback` returned None (e.g., previous iter ran `SINGLE_PASS`), four fallthrough paths set `feedback_path = None`, causing `_run_feedback_pass` to render `"None"` as the feedback path string into the analyze prompt template. Fixed via centralized post-dispatch guard that demotes to cold-start with a warning.
- **Major (missing tests):** Plan stencils for Case 5 byte-equal copy, Case 3 SI preservation, and post-doesn't-clobber-pre were verified only by smoke test, leaving no CI regression coverage. Added.
- **Minor (note rot):** Phase 3 notes referenced `iter-7` (concept 02) and `iter-10` (concept 07); actual disk has `iter-6` and `iter-9`. Corrected above.

**Actual changes:**
- `lib/loop.py`: Added `_copy_to_pre_feedback(source, iter_dir)` helper that collapses the 5 inline `if prior is not None: shutil.copyfile(...)` patterns. Each fallthrough path now reads as one line: `feedback_path = _copy_to_pre_feedback(_get_prior_feedback(...), iter_dir)`. The dispatch chain is shorter and the byte-equal copy invariant is now directly unit-testable.
- `lib/loop.py`: Added centralized cold-start fallback after the dispatch chain — if `feedback_source != "cold_start"` and `feedback_path is None`, demote to cold-start with a printed warning. Catches the latent SINGLE_PASS-then-resume scenario.
- `test_failure_chains.py`: Added `TestDispatchSymmetry` class with 4 tests:
  - `test_copy_to_pre_feedback_byte_equal` (Plan stencil 1, Case 5)
  - `test_copy_to_pre_feedback_preserves_source` (Plan stencil 2, Case 3)
  - `test_copy_to_pre_feedback_none_source` (drives the cold-start fallback predicate)
  - `test_assess_does_not_clobber_pre_feedback` (Plan stencil 3, post immutability)
**Deviations from original plan:**
- The plan said "don't force" extracting a `_populate_pre_feedback` helper. The post-audit fix extracts a smaller, focused helper (`_copy_to_pre_feedback` — 4 lines of body) rather than the full dispatch. This makes the byte-equal invariant directly testable without driving the full loop. The full dispatch stays inline as the original plan specified.

---

**Status**: Complete
