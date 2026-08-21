# Spec: feedback-dispatch file naming symmetry

**Status:** Draft
**Owner:** Reid W
**Created:** 2026-04-25
**Complexity:** LOW (mechanical refactor, no semantic changes if Option B chosen)
**Branch:** concept-analysis-runs (parent); fix branch TBD

---

## Business Goals

### Why this matters

The Stage 1 analysis loop's feedback-producer dispatch (`lib/loop.py:115-178`) has grown five cases (cold-start, review kick-back, source-integration, research, default-assess). Each case decides where to put the feedback file that the next `analyze` step reads. Today those decisions are inconsistent in two visible ways:

1. **Filename collision with assess's output.** Case 2 (review kick-back) writes its extracted review findings to `iter-(N+1)/feedback.md`. Case 4 (research+merge) does the same. But `iter-(N+1)/feedback.md` is *also* the path that `_run_assess` writes to at the end of iter N+1 (`lib/loop.py:717`) — so the input feedback gets clobbered by the output feedback within the same iteration. After the iter completes, you cannot tell from disk what fed analyze; you have to read `verdict.json`'s `feedback_source` field and reverse-engineer.

2. **No symmetry across cases.** Case 3 writes to a distinctly-named `iter-(N+1)/source_integration_output.md` (no collision). Cases 2 and 4 collide. Case 5 (default) reads `iter-N/feedback.md` (the prior iter's assess output) and writes nothing new. There is no consistent "where does input feedback live" rule.

This isn't a correctness bug — the loop runs fine — but it's a debuggability and maintainability tax. Operators have to read `verdict.json` to figure out what drove an iteration. New contributors can't apply pattern-match reasoning ("oh, all feedback files live at `iter-N/X`") because the pattern is broken in two of five cases. The actual-mechanics doc (`docs/concept-pipeline/actual-mechanics.md`) had to dedicate an entire "So which `feedback.md` is which?" section to walking through the table case-by-case — that section exists *because of* this asymmetry.

### Success criteria

- [ ] A consistent, single rule governs where input feedback files live across all five dispatch cases. The rule is documentable in one sentence.
- [ ] Looking at `iter-N/` on disk after a completed iteration, an operator can determine what feedback fed iter N's analyze step *without* reading `verdict.json`.
- [ ] `iter-N/feedback.md` (or whatever the chosen "assess output" filename ends up as) is never overwritten within the same iteration. Producer-clears-on-write semantics are preserved.
- [ ] No regression in the `--resume` cross-iteration handoff: iter N+1's default-case analyze still reads what iter N's assess produced.
- [ ] `actual-mechanics.md`'s "which `feedback.md` is which?" table either disappears or shrinks to one row per case with no exceptions.

### Priority

Low urgency, low complexity. This is a developer-experience cleanup. Schedule when there is no in-flight work touching `lib/loop.py` (currently active items: `loop-dry-run-symmetry`, `model-feedback-starvation`, `power-standardization` — check before starting).

**Dependencies:**
- Blocks on: `power-standardization` and `model-feedback-starvation` reaching at least implementation if either touches dispatch logic. (Verify via `grep` against their plan.md before starting.)
- Blocked by: nothing else.

---

## Problem Statement

### Current state

`lib/loop.py:115-178` is the dispatch chain. Per-case behavior:

| Case | Trigger | Where input feedback is written | Filename collision with assess output? |
|------|---------|-------------------------------|----------------------------------------|
| 1. cold-start | `iter == 1 and not resume` | (no input feedback) | n/a |
| 2. review kick-back | `Review-Status: revise` (one-shot) | `iter-(N+1)/feedback.md` (line 129-130) | **YES** — overwritten by `_run_assess` at end of iter |
| 3. source-integration | new sources detected (one-shot) | `iter-(N+1)/source_integration_output.md` (`loop.py:792`) | No — distinct filename |
| 4. research+merge | `--research` and sources acquired | `iter-(N+1)/feedback.md` (via `_merge_feedback`, `loop.py:165-166`) | **YES** — overwritten by `_run_assess` at end of iter |
| 5. default | else | (reads `iter-N/feedback.md`; writes nothing) | n/a |

The assess step at end of every iter writes `iter-N/feedback.md` (`loop.py:717, 738-742`). This is the "iteration's verdict feedback" file — it captures what the in-loop assessor thought.

In Cases 2 and 4, that same path is *also* used as the input-feedback drop point. The input file is created at the start of the iteration, read by analyze in the middle, then overwritten by assess at the end. After iter completion, only the overwritten (assess) version exists on disk.

### Concrete observable problems

**Problem A: Cannot reconstruct what fed iter N from disk alone.**

After running `analyze 11 --resume` (where iter N+1 fired Case 2), the on-disk state of `iter-(N+1)/` contains a `feedback.md` that says *what assess produced*, not what fed analyze. The original review-extracted findings are gone. To know that Case 2 fired, you must open `iter-(N+1)/verdict.json` and read `"feedback_source": "review"`.

**Problem B: Inconsistent mental model.**

When teaching the system to a new contributor (see commit history of `docs/concept-pipeline/actual-mechanics.md`), the dispatch requires a special-case table because the rule "input feedback lives at `iter-(N+1)/feedback.md`" is true for Cases 2 and 4 but false for Cases 3 and 5. Case 3 has its own filename; Case 5 has no input file. There is no single rule.

**Problem C: Asymmetric assess preservation.**

Case 4 has explicit logic (`_merge_feedback`, `loop.py:293-333`) to preserve prior assess findings when source-integration takes over the feedback channel ("FR-8 so they aren't dropped"). Case 2 has *no* such logic — review-extracted findings replace prior assess findings entirely with no merge. The implicit assumption is "a human review supersedes the automated assessor" but this is undocumented and not justified in code. Whether or not we merge in Case 2 is out of scope for this spec, but the asymmetry should be either fixed or explicitly noted.

### Why this isn't a critical bug

The pipeline produces correct outputs. `verdict.json` captures the metadata needed for `--resume`. No data corruption happens. This is a debuggability and readability issue — important for sustaining the codebase but not blocking analysis runs.

---

## Proposed Designs

Two viable designs. The spec records both; selection happens at /_my_design time.

### Option A: Forward-looking semantic for `feedback.md`

**Rule:** `iter-N/feedback.md` is "what should drive iter N+1's analyze." It is mutable within iter N — assess writes to it at the end, and on resume the dispatch may overwrite it (e.g., Case 2 replaces it with review-extracted findings).

**Per-case behavior:**

| Case | Behavior under Option A |
|------|-------------------------|
| 1 (cold-start) | No file; analyze runs cold |
| 2 (review kick-back) | Overwrite `iter-N/feedback.md` with review-extracted findings *before* iter N+1 begins |
| 3 (source-integration) | Overwrite `iter-N/feedback.md` with source-integration output *before* iter N+1 begins |
| 4 (research+merge) | Overwrite `iter-N/feedback.md` with merged content *before* iter N+1 begins |
| 5 (default) | No-op; `iter-N/feedback.md` already contains what's needed |

**Pros:**
- Collapses dispatch logic. All non-cold-start cases boil down to "produce the right `iter-N/feedback.md`, then run analyze in feedback-pass mode reading that file." The `feedback_path` variable disappears — analyze always reads `iter-N/feedback.md`.
- Single rule: "the file that drives iter N+1's analyze is always `iter-N/feedback.md`."

**Cons:**
- **Destroys per-iteration audit trail.** After a Case 2/3/4 fires, `iter-N/feedback.md` no longer reflects what assess said at the end of iter N. The historical record is gone unless reconstructed from `verdict.json` (which only captures `verdict` and `finding_count`, not the actual finding text).
- **Mutates a prior iteration's directory from a later iteration.** Today, iter-N/ is a transcript of what happened during iter N. Option A breaks this — iter N+1 reaches into iter-N/ and mutates its contents.
- Confusing semantic: `iter-N/feedback.md` means two different things at different times.

### Option B: Sacred `feedback.md`, distinctly-named input feedback

**Rule:** `iter-N/feedback.md` is always assess's output for iter N (immutable transcript). Input feedback that drives iter N's analyze gets a distinctly-named file in `iter-N/` (the iter it actually drives).

**Per-case behavior:**

| Case | Input file written for iter N+1's analyze |
|------|-------------------------------------------|
| 1 (cold-start) | None; analyze runs cold |
| 2 (review kick-back) | `iter-(N+1)/review_feedback.md` |
| 3 (source-integration) | `iter-(N+1)/source_integration_feedback.md` (renamed from existing `source_integration_output.md` for consistency) |
| 4 (research+merge) | `iter-(N+1)/merged_feedback.md` (instead of clobbering `feedback.md`) |
| 5 (default) | None; `feedback_path` points at `iter-N/feedback.md` (the prior iter's assess output, no new file written) |

**Pros:**
- Preserves all transcripts — `iter-N/feedback.md` always = "what assess said at end of iter N."
- Each iter directory is self-contained; no cross-iter mutation.
- `ls iter-N/` immediately shows what fed analyze (presence of `*_feedback.md`) and what assess produced (`feedback.md`).
- Smaller scope of change: only the two `feedback_path = ...` assignments in Cases 2 and 4 plus the rename in Case 3.

**Cons:**
- Five filenames to remember (`feedback.md`, `review_feedback.md`, `source_integration_feedback.md`, `merged_feedback.md` — and analyze reads whichever exists).
- Doesn't reduce the dispatch from 5 cases to fewer.
- Slight duplication: Case 5 reads `iter-(N-1)/feedback.md` directly with no copy in `iter-N/` documenting "this is what fed me." (Mitigation: `verdict.json` already records `feedback_source: "assess"`, which implies "I read the prior iter's feedback.md.")

### Recommendation

**Lean toward Option B** because:
- The audit-trail loss in Option A undermines a core property of the design (iter-N/ as transcript) that the rest of the codebase relies on (e.g., bisecting regressions via `diff iter-3 iter-4`).
- Option B's "more files" cost is smaller than Option A's "mutating prior iters" cost. File-naming complexity stays inside the iter directory; cross-iteration mutation is a bigger smell.
- Option B is implementable with small, surgical changes. Option A requires verifying that no downstream consumer of `iter-N/feedback.md` depends on it being assess's output (likely safe but needs audit).

Final selection happens at `/_my_design` time.

---

## In Scope

- Modify `lib/loop.py:115-178` (dispatch chain) to implement the chosen rule consistently across Cases 2, 3, 4.
- Update `_run_source_integration` (`lib/loop.py:777-843`) if the chosen design renames its output file.
- Update `_merge_feedback` (`lib/loop.py:293-333`) to write to the chosen filename.
- Update `_run_assess` (`lib/loop.py:703-774`) if the chosen design changes its output filename (Option A: no change; Option B: no change).
- Update `actual-mechanics.md`'s "which `feedback.md` is which?" table.

## Out of Scope

- Changing the dispatch *priority order* — that's a separate question.
- Changing whether Case 2 merges with prior assess findings (the asymmetry-with-Case-4 question is real but is its own design discussion).
- Renaming `feedback.md` itself (the assess output filename).
- Touching the verdict.json schema.
- Touching `--add-passes` or `--resume` semantics.
- Migrating existing concept directories that already have iter-N/ contents in the old layout (the current codebase has 38 concepts with completed iter-*/ dirs; we should be able to leave those alone since the old format is forward-compatible — but verify in /_my_design).

---

## Acceptance Criteria

- [ ] All five dispatch cases follow one documentable rule for where input feedback lives.
- [ ] No filename collisions within an iteration directory (no file is written twice during one iter, except via the producer-clears-on-write contract that already exists).
- [ ] `iter-N/feedback.md` semantic is documented in code (one-line comment near the assess output write).
- [ ] After a `Case 2` (review kick-back) iteration, `iter-(N+1)/` contains both the review-extracted feedback file AND assess's per-iter output file as separate readable artifacts (Option B), OR the design choice to overwrite is justified in code with an explicit comment (Option A).
- [ ] `actual-mechanics.md` "which `feedback.md` is which?" section updated; ideally collapsed to a single rule.
- [ ] Existing 38 concept directories are not touched; the new layout is created for new iterations only. Pipeline reads either layout for backward compatibility (or migration is performed if simple — verify in design phase).
- [ ] Tests (if any cover dispatch) pass; otherwise smoke-test by running `analyze NN --add-passes 1 --dry-run` on at least one concept in each of these states: post-revise (triggers Case 2), with-new-sources (triggers Case 3), and default (triggers Case 5). Verify the prompts saved to disk reference the expected feedback file paths.

## Out of Scope (acceptance)

- Performance changes (none expected; this is a naming refactor).
- Changes to template content or feedback schema.
