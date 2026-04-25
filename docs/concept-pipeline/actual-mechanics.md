# How the analyze loop actually works

A walkthrough of what `uv run python exploration/concept_analysis/scripts/run_analysis.py analyze <concept>` does, line by line, file by file. No abstractions, no diagrams — just what the code does.

All file references are relative to `exploration/concept_analysis/`.

---

## The big picture

`analyze 11` runs a loop. The loop body is three steps in order:

1. `analyze` — write/edit `analysis.md`
2. `model-setup` — write `model_setup.py`, run it, capture stdout to `model_output.txt`
3. `assess` — write `post_feedback.md` and `verdict.json`

The loop runs at most `--max-passes` times (default 3). It exits early when `assess` writes `VERDICT: PASS` into `post_feedback.md`.

Each pass is one **iteration** and produces an `iter-N/` directory with all its prompts and outputs. Iteration 1 is a "cold start" — analyze writes from scratch. Iteration 2+ is a "feedback pass" — analyze reads a feedback file and edits the existing `analysis.md` in place.

The interesting question is: **on iteration 2+, which feedback file does analyze read?** That decision is the *dispatch*, and that's most of what makes this loop more than a simple retry.

---

## Where everything lives on disk

```
analyses/11-magnetic-mirror/                 ← one directory per concept
├── analysis.md                              ← canonical analysis (frontmatter + body)
├── model_setup.py                           ← canonical cost model (copied from latest good iter)
├── model_output.txt                         ← canonical model stdout
├── review.md                                ← Stage 2 reviewer's verdict (if review has run)
├── synthesis.md                             ← Stage 3 editorial synthesis (if it has run)
├── iter-1/
│   ├── analyze_prompt.md                    ← rendered prompt sent to claude
│   ├── analysis_output.md                   ← analysis.md body for this iter (frontmatter stripped)
│   ├── model_setup_prompt.md
│   ├── model_setup.py                       ← per-iter model
│   ├── model_output.txt                     ← per-iter model stdout
│   ├── assess_prompt.md
│   ├── pre_feedback.md                      ← input to analyze (iter > 1 only; absent for cold start)
│   ├── post_feedback.md                     ← assess's output: VERDICT + ### F-N findings
│   ├── verdict.json                         ← machine-readable summary of this iter
│   └── validation_log.json                  ← retries/validation history
├── iter-2/                                  ← same shape; analyze ran in feedback-pass mode
│   ├── ...
│   ├── source_integration_prompt.md         ← (only if Case 3 fired)
│   ├── source_integration_output.md         ← (only if Case 3 fired)
│   ├── research_prompt.md                   ← (only if Case 4 fired)
│   └── research_output.json                 ← (only if Case 4 fired)
└── ...
```

Sources for the concept live in a different tree:

```
knowledge/concept_research/11-magnetic-mirror/
├── dossier.md                               ← Phase 1a research dossier
└── iter-01/sources/
    ├── arxiv-1234.md                        ← extracted source documents
    ├── arxiv-1234/                          ← companion dir (PDF, images, etc.)
    └── ...
```

`add-source` drops new files into `iter-NN/sources/` over there.

---

## One iteration in detail

Code: `lib/loop.py:107-258` (`run_stage1_loop`'s `for iter_num in range(...)` body).

### Pre-step: pick a feedback source

Before analyze runs, the loop decides what feedback drives this iteration. This is the **dispatch** — see the next section.

The dispatch produces:
- `feedback_source` — a string label that goes into `verdict.json` (`"cold_start"`, `"review"`, `"source_integration"`, `"research"`, `"assess"`)
- `feedback_path` — a `Path` to the feedback file that analyze will read, or `None` for cold-start

### Step 1: analyze

If `feedback_source == "cold_start"`:
- `_run_cold_start` (`lib/loop.py:336-409`) renders the cold-start branch of `prompt_templates/analysis_v2.md` (which has a `{{#if cold_start}}` block).
- Pre-writes `analysis.md` with frontmatter only (so claude can read the file path it's about to write to).
- Invokes claude. Claude writes the analysis body to `iter-N/analysis_body.md`.
- After claude returns, the script concatenates frontmatter + body into the canonical `analysis.md`.

Otherwise (any feedback-pass case):
- `_run_feedback_pass` (`lib/loop.py:412-479`) renders the feedback-pass branch of `analysis_v2.md` with `feedback_path` filled in.
- Snapshots the SHA-256 of `analysis.md` *before* invoking claude.
- Invokes claude. Claude reads `feedback_path` and edits `analysis.md` in place via the Edit tool.
- After claude returns, the validator (`make_file_modified_validator` from `lib/validators.py`) re-hashes `analysis.md`. If unchanged, the iteration FAILs.

Either way, after step 1: `analysis.md` exists at the concept root (canonical), and a copy of just the body is saved to `iter-N/analysis_output.md` by `_capture_analysis_output` (`lib/loop.py:482-499`).

### Step 2: model-setup

`_run_model_in_iteration` (`lib/loop.py:531-636`).

- Reads `analysis.md`.
- For iter > 1, finds the most recent prior iter that succeeded (`model_ok=True` in its `verdict.json`) via `_find_best_prior_model` (`lib/loop.py:502-528`), and copies that `model_setup.py` into the current iter dir. This puts claude into "edit mode" — it will modify the prior model rather than rewrite from scratch.
- Renders one of four templates (chosen by `build_model_vars`, `lib/loop.py:642-700`):
  - `model_setup_costingfe.md` (cold) or `model_setup_costingfe_edit.md` (edit) — for concepts that map onto the 1costingfe library
  - `model_setup_freeform.md` (cold) or `model_setup_freeform_edit.md` (edit) — standalone Python LCOE models
- Invokes claude. Output is `iter-N/model_setup.py`.
- After claude returns, the script runs the script (`run_model` in `lib/claude.py`) and captures stdout to `iter-N/model_output.txt`.
- The script's syntax is validated (`validate_python_syntax`). If it errors at runtime, the iteration continues but `model_ok=False` is recorded.

If `model_ok=True`, `_update_canonical_files` (`lib/loop.py:900-926`) copies `iter-N/model_setup.py` and `model_output.txt` to the concept root. If `model_ok=False`, the canonical copies stay as the last known-good version.

### Step 3: assess

`_run_assess` (`lib/loop.py:703-774`).

- Renders `prompt_templates/assessment.md` with paths to `analysis.md`, `model_output.txt`, and the to-be-written feedback file.
- Invokes claude. Claude writes `iter-N/post_feedback.md` with this format:

```
VERDICT: PASS
```
or
```
VERDICT: FINDINGS

### F-1: [title]
- **Target:** [section]
- **Category:** analysis | model
- **Finding:** [what's wrong]
- **Recommendation:** [what to fix]
- **Priority:** blocking | important | minor

### F-2: ...
```

The format is enforced by `validate_feedback_verdict` (`lib/validators.py:61-119`). Findings can be `Category: analysis` (changes to `analysis.md` text) or `Category: model` (changes to `model_setup.py`). The cap is 3 findings per pass — see `prompt_templates/config/feedback_format.md`.

After claude returns, `parse_verdict_from_feedback` (`lib/iteration.py:134-145`) scans the file for `VERDICT: PASS` (regex: `^VERDICT:\s*(PASS|FINDINGS)\s*$`) and counts `### F-N:` headers.

### After step 3: write verdict.json and decide

`write_verdict` (`lib/iteration.py:103-131`) writes `iter-N/verdict.json`:

```json
{
  "iteration": 2,
  "verdict": "FAIL",
  "finding_count": 2,
  "feedback_source": "assess",
  "model_ran": true,
  "model_ok": true,
  "research_ran": false,
  "merged_assess": false,
  "sources": ["...", "..."],
  "timestamp": "2026-04-25T..."
}
```

Then the loop:
- If `verdict == "PASS"` → `return "PASS"`. Loop exits. (`lib/loop.py:250-251`)
- If `iter_num >= max_passes` → return current verdict with a "did not converge" warning. (`lib/loop.py:254-256`)
- Otherwise → next iteration starts. Back to dispatch.

---

## The dispatch in detail

Code: `lib/loop.py:115-178`. This is the if/elif chain that picks `feedback_source` and `feedback_path`.

The dispatch is checked **fresh at the top of every iteration**. The cases are checked in priority order — first match wins. Two of them are *one-shot* (they fire at most once per `analyze` invocation, gated by boolean flags `used_review_feedback` and `used_source_integration` declared at lines 102-103).

### Case 1: cold start (iter 1, no resume)

```python
if iter_num == 1 and not resume:
    feedback_source = "cold_start"
```

`feedback_path = None`. analyze runs in cold-start mode (writes `analysis.md` from scratch). This case only fires on the very first iteration of a fresh run.

### Case 2: review kick-back (one-shot)

```python
elif not used_review_feedback and _has_revise_status(analysis_path):
    used_review_feedback = True
    feedback_text = _get_review_feedback(concept_dir)
    if feedback_text is not None:
        feedback_source = "review"
        feedback_path = iter_dir / "pre_feedback.md"
        feedback_path.write_text(feedback_text, encoding="utf-8")
    else:
        feedback_source = "assess"
        # copies prior iter's post_feedback.md → iter-N/pre_feedback.md
        feedback_path = _get_prior_feedback(concept_dir, iter_num)
```

#### What does "Review-Status: revise" mean?

`Review-Status` is a **frontmatter field on `analysis.md`** (the canonical one at the concept root). It's set by the `review` command. Code: `run_analysis.py:642-665`.

When you run `review 11`, claude writes `review.md` containing either `VERDICT: PROCEED` or `VERDICT: REVISE`. The `review` command then reads that, decides whether the verdict is PROCEED or REVISE, and updates `analysis.md`'s frontmatter:

```yaml
---
ID: 11-magnetic-mirror
Status: draft
Review-Status: revise         ← set here by run_analysis.py:663
Review-Iterations: 1
Last-Review: 2026-04-25
---
```

`_has_revise_status` (`lib/loop.py:855-860`) reads that frontmatter and returns `True` iff `Review-Status == "revise"`. So this case fires when **a human reviewer rejected a prior analysis with VERDICT: REVISE, and `analyze --resume` is now picking it back up**.

#### What does "extract F-N" mean?

`_get_review_feedback` (`lib/loop.py:863-897`) reads `review.md` and extracts the `## Corrective Actions` section. That section is templated to contain `### F-N:` blocks in the same `feedback_format.md` schema that `assess` uses. See `prompt_templates/review.md:114-123` for the template.

The function:
1. Confirms `review.md` says `VERDICT: REVISE` (regex `REVIEW_VERDICT_RE` at `lib/validators.py:36`).
2. Finds the `## Corrective Actions` heading (regex `CORRECTIVE_ACTIONS_RE` at `lib/validators.py:37`).
3. Slices out everything between that heading and the next `## ` heading (or end of file).
4. Prepends `VERDICT: FINDINGS\n\n` so the result parses as a normal feedback file.

The result is written to `iter-N/pre_feedback.md` (`lib/loop.py:130`). This is the input to analyze — distinct from `post_feedback.md`, which assess writes at the end of the iteration.

#### "One-shot" — what does that actually mean?

`used_review_feedback` is set to `True` on the line that fires this case (`lib/loop.py:125`). It stays `True` for the rest of the `analyze` invocation. So if you run `analyze 11 --resume --max-passes 4` and Case 2 fires on iter 2, then iter 3 and iter 4 will skip Case 2 and fall through to other cases (most likely Case 5 / assess).

This prevents the loop from re-extracting the same review findings every iteration. The reviewer's findings are a one-time injection; after that, the assessor takes over.

#### What if `review.md` has no extractable F-N findings?

The `else` branch at `lib/loop.py:132-135` falls through to the assess case (Case 5). This handles the edge case where `Review-Status: revise` is set but `review.md` doesn't have a properly formatted Corrective Actions section.

### Case 3: source-integration (one-shot)

```python
elif new_sources and not used_source_integration:
    feedback_source = "source_integration"
    si_result = _run_source_integration(...)
    if si_result is not None:
        feedback_path = iter_dir / "pre_feedback.md"
        shutil.copyfile(si_result, feedback_path)
    else:
        feedback_source = "assess"
        # copies prior iter's post_feedback.md → iter-N/pre_feedback.md
        feedback_path = ...
    used_source_integration = True
```

#### How are "new source files" checked, and by whom?

`new_sources` is computed once at the top of `run_stage1_loop` (`lib/loop.py:99-101`):

```python
current_sources = find_sources(rid)
new_sources = detect_new_sources(loop_state, current_sources) if resume else []
```

- `find_sources(rid)` (`lib/sources.py:9-24`) globs `knowledge/concept_research/{rid}/iter-*/sources/*.md` and returns the sorted list.
- `detect_new_sources(loop_state, current_sources)` (`lib/iteration.py:148-154`) takes the union of `sources` arrays from all prior iterations' `verdict.json` files and returns paths in `current_sources` that aren't in that union.

So "new source files" = `.md` files in the sources directory that weren't recorded in any prior iteration's `verdict.json`. The check happens **at the start of the analyze invocation**, on resume only. The most common way new sources appear is `add-source 11 <path-or-url>` between two `analyze --resume` calls.

#### What does source-integration do?

`_run_source_integration` (`lib/loop.py:777-843`):

1. Renders `prompt_templates/source_integration.md` with the new source paths and `analysis.md`.
2. Invokes claude. Claude reads `analysis.md` and the new sources, then writes `iter-N/source_integration_output.md` in the standard `VERDICT + F-N:` format.
3. If claude returns `VERDICT: PASS` (no material new info), the function returns `None` — the dispatch then falls through to Case 5 (use prior assess feedback).
4. Otherwise, the function returns the path `iter-N/source_integration_output.md`. The dispatch then copies it to `iter-N/pre_feedback.md`, which is what analyze reads. The original `source_integration_output.md` is preserved as the raw producer artifact.

#### Why "one-shot"?

`used_source_integration = True` at `lib/loop.py:146`. Same reason as Case 2 — once the new sources have been integrated into the analysis, you don't want to re-run the same integration step every subsequent iteration.

### Case 4: --research

```python
elif getattr(args, "research", False) and iter_num > 1:
    feedback_source = "research"
    from lib.research import run_research_step
    acquired = run_research_step(concept, iter_dir, args)
    # refresh sources after research (so source-integration sees them)
    current_sources = find_sources(rid)
    if acquired:
        si_path = _run_source_integration(...)
        if si_path is not None:
            assess_fb = _get_prior_feedback(concept_dir, iter_num)
            merged_assess = assess_fb is not None and assess_fb.exists()
            feedback_path = _merge_feedback(assess_fb, si_path, iter_dir / "pre_feedback.md")
        else:
            feedback_source = "assess"
            # copies prior iter's post_feedback.md → iter-N/pre_feedback.md
            feedback_path = ...
    else:
        feedback_source = "assess"
        # copies prior iter's post_feedback.md → iter-N/pre_feedback.md
        feedback_path = ...
```

#### What does the research agent do?

`run_research_step` (`lib/research.py`) reads `analysis.md`'s "Section 6 — Data Gap Inventory" to find unfilled gaps, runs WebSearch to find candidate sources, calls `add-source` to extract them. Return value is the list of newly acquired source paths (could be empty).

Capped by `--max-research-searches` (default 5) and `--max-research-extractions` (default 3) to bound cost — each `add-source` runs `agentic-mbse extract` which costs $5–$50.

#### What does "merged with prior" mean?

If research acquired sources AND source-integration produced findings (didn't return PASS), the loop merges those findings with the prior iteration's assess feedback. Code: `_merge_feedback` at `lib/loop.py:293-333`.

The reasoning (FR-8 in the design): the prior assess raised some findings. Then research happened and added new sources. The new feedback file pointed at by `feedback_path` would be JUST the source-integration findings — meaning the prior unfixed assess findings would be DROPPED on this iteration. To prevent that, the merger:

1. Takes the source-integration output as primary content.
2. Reads the prior iter's `post_feedback.md` (assess output).
3. If it had `VERDICT: FINDINGS` with at least one `### F-N:` block, appends those findings under a `## Carried-Forward Assessment Findings` header.
4. Writes the merged result to `iter-N/pre_feedback.md`.

So in Case 4, the file analyze reads is `iter-N/pre_feedback.md` — it contains both source-integration findings AND prior assess findings.

`merged_assess: true` is recorded in `verdict.json` so you can see this happened.

#### Research with no acquisitions

If `run_research_step` returns no acquired sources (the agent searched but found nothing useful, or all candidates were paywalled, etc.), the dispatch falls through to Case 5 — use the prior iteration's assess feedback. The research step still ran and is recorded in `verdict.json` as `feedback_source: research`, `research_ran: true`.

### Case 5: default (the assess feedback loop)

```python
else:
    feedback_source = "assess" if iter_num > 1 else "cold_start"
    prior = _get_prior_feedback(concept_dir, iter_num) if iter_num > 1 else None
    if prior is not None:
        feedback_path = iter_dir / "pre_feedback.md"
        shutil.copyfile(prior, feedback_path)
```

`_get_prior_feedback` (`lib/loop.py:875-879`):

```python
def _get_prior_feedback(concept_dir: Path, iter_num: int) -> Path | None:
    if iter_num <= 1:
        return None
    prior = concept_dir / f"iter-{iter_num - 1}" / "post_feedback.md"
    return prior if prior.exists() else None
```

Case 5 copies the prior iteration's `post_feedback.md` (assess output) into `iter-N/pre_feedback.md` (input to analyze). The copy means every `iter-N/` directory is self-contained — `ls iter-N/` shows both what fed analyze (`pre_feedback.md`) and what assess concluded (`post_feedback.md`).

This is also the case that fires after Case 2 / Case 3 have used their one-shot. Once the human's REVISE findings or new sources have been integrated, subsequent iterations fall through to Case 5 and the loop just keeps polishing based on assess findings.

---

## Where input and output feedback live

**One rule:** analyze's input is always `iter-N/pre_feedback.md`; assess's output is always `iter-N/post_feedback.md`. They never collide. For iter > 1 in a completed run, both files exist in every `iter-N/` directory.

| Case | What analyze reads (`pre_feedback.md` contains) | Where the content originates |
|------|--------------------------------------------------|------------------------------|
| 1 (cold start) | — (no `pre_feedback.md`) | — |
| 2 (review) | findings extracted from `review.md` | `_get_review_feedback` → writes directly |
| 3 (source-integration) | source-integration findings | copied from `source_integration_output.md` |
| 4 (research, w/ sources acquired) | merged source-integration + prior assess | `_merge_feedback` → writes directly |
| 4 (research, nothing acquired) | prior iter's assess output | copied from `iter-(N-1)/post_feedback.md` |
| 5 (default) | prior iter's assess output | copied from `iter-(N-1)/post_feedback.md` |

Assess writes `iter-N/post_feedback.md` at the end of every iteration. It is an immutable transcript — nothing else writes to that path.

> **Historical note:** Prior to this change, both input and output were called `feedback.md`, and Cases 2 and 4 would overwrite the input with the output within the same iteration. The rename was done in commit `TBD` on branch `pipeline-cleanup`.

---

## Verdict semantics

`post_feedback.md` content drives the loop's exit decision. `parse_verdict_from_feedback` (`lib/iteration.py:134-145`) parses:

- `^VERDICT:\s*(PASS|FINDINGS)\s*$` → if PASS, verdict is `"PASS"`. Otherwise `"FAIL"`.
- `^### F-\d+:` → counts findings.

Note the asymmetry: the file says `VERDICT: PASS` or `VERDICT: FINDINGS`, but the loop normalizes to `"PASS"` or `"FAIL"` (via `parse_verdict_from_feedback`). FAIL just means "not PASS" — it doesn't mean the iteration errored.

Other verdict strings written to `verdict.json`:
- `"ERROR"` — claude returned non-zero, or a step failed before assess could run (`lib/loop.py:185, 194`)
- `"SINGLE_PASS"` — `--max-passes 1` was set, so assess was skipped entirely (`lib/loop.py:213-219`)
- `"INTERRUPTED"` — has artifacts but no verdict.json (the loop crashed mid-iteration). Detected by `read_loop_state` at `lib/iteration.py:96-98`.

---

## What `--resume` actually does

`run_stage1_loop` checks `args.resume` at line 91-95:

```python
if resume:
    start_iter = loop_state.next_iteration
    if start_iter > max_passes:
        print(f"  {cid}: max passes reached ({max_passes})")
        return ...
```

`loop_state.next_iteration` (`lib/iteration.py:42-46`):

```python
@property
def next_iteration(self) -> int:
    if self.last_incomplete is not None:
        return self.last_incomplete  # resume the partial one
    return self.last_complete + 1    # start the next one
```

`last_complete` is the highest `iter-N/` directory that has a `verdict.json`. `last_incomplete` is the highest `iter-N/` that has artifacts but no `verdict.json`. Computed by `read_loop_state` at `lib/iteration.py:57-100`.

So `--resume` does not consult any journal — it just `glob`s for `iter-*/verdict.json` and decides what's done. To "reset" you can just `rm -rf iter-3/` and the next resume will start at iter 3.

`--force` calls `clear_iterations` (`lib/iteration.py:157-169`) which deletes all `iter-*/` dirs and also deletes `research_log.json`. Sources in `knowledge/concept_research/.../sources/` are NOT touched.

---

## Glossary

| Term | What it actually is |
|------|---------------------|
| `pre_feedback.md` | Input to analyze for iter > 1. Contains `VERDICT: ...` and `### F-N:` findings in the same format as `post_feedback.md`. Written by the dispatch chain at the start of each iteration. Content varies by case (review extract, source-integration copy, merge, or copy of prior `post_feedback.md`). Absent for cold-start (iter 1). |
| `post_feedback.md` | Assess's output. Contains `VERDICT: ...` and zero or more `### F-N:` finding blocks. Format defined in `prompt_templates/config/feedback_format.md`. Written by assess at the end of every iteration. Immutable transcript — never overwritten. (Previously called `feedback.md`.) |
| `verdict.json` | Per-iteration machine-readable summary written by `write_verdict` (`lib/iteration.py:103-131`). Records iteration number, verdict, finding count, which feedback source fed analyze, whether model ran/succeeded, source list, etc. Used by `--resume` to figure out where to pick up. |
| `Review-Status: revise` | A frontmatter field on `analysis.md`. Set by `cmd_review` (`run_analysis.py:642-665`) when the human reviewer's `review.md` says `VERDICT: REVISE`. Read by `_has_revise_status` (`lib/loop.py:855`) to gate Case 2 of the dispatch. |
| `### F-N:` | A "finding" header in feedback files. N is just a counter (F-1, F-2, F-3). Each finding has Target, Category (analysis|model), Finding, Recommendation, Priority. Counted by `FINDING_HEADER_RE` (`lib/validators.py:23`). Cap of 3 per pass. |
| "extract F-N" | The action `_get_review_feedback` performs (`lib/loop.py:863-897`): finds `## Corrective Actions` in `review.md`, slices the section out, prepends `VERDICT: FINDINGS`, returns the text. The caller writes it to `iter-N/pre_feedback.md`. |
| "one-shot" (Case 2 / Case 3) | A boolean flag (`used_review_feedback` / `used_source_integration` at `lib/loop.py:102-103`) that gets set the first time the case fires and prevents it from firing again in the same `analyze` invocation. The flag does NOT persist across invocations. |
| "merged with prior" (Case 4) | `_merge_feedback` (`lib/loop.py:293-333`) appends the prior iter's assess findings (from `post_feedback.md`) to the source-integration output under a `## Carried-Forward Assessment Findings` heading, writes the result to `pre_feedback.md`, so unfixed findings aren't dropped when research+source-integration takes over the feedback channel. |
| "new sources detected" | `detect_new_sources` (`lib/iteration.py:148-154`) returns the set difference: `find_sources()` minus the union of source paths recorded in all prior iterations' `verdict.json`. |
| "cold start" | Iter 1 of a fresh (`not resume`) run. analyze writes `analysis.md` from scratch using the cold-start branch of `analysis_v2.md`. Pre-writes only the YAML frontmatter so claude has something to point at. |
| "feedback pass" | Iter ≥ 2 (or any resume iter ≥ 2). analyze reads a feedback file via the `feedback_path` template variable and edits `analysis.md` in place. The validator (`make_file_modified_validator`) verifies `analysis.md` actually changed. |
| `model_ok` | Boolean in `verdict.json`. True iff `model_setup.py` parsed AND ran AND its stdout contained "lcoe" (case-insensitive). False = the model is broken; the canonical `model_setup.py` at the concept root won't be updated this iter. |
| `research_log.json` | At the concept root. Per-concept history of what the research agent has tried, used to avoid repeating dead-end queries. Deleted by `--force`. |
| Stage 0/1/2/3 | Conceptual labels for the four phases (Bootstrap / Automated loop / Human review / Synthesis). Not in the code; they're a documentation framing. The CLI commands map roughly: `gap-check` is Stage 0 verification, `analyze` is Stage 1, `review` + `address-review` is Stage 2, `synthesize` + `approve` is Stage 3. |

---

## Reading list (in code-walkthrough order)

If you want to follow the loop end-to-end:

1. `run_analysis.py:263-345` — `cmd_analyze` (CLI handler, calls `run_stage1_loop`)
2. `lib/loop.py:55-258` — `run_stage1_loop` (the for-loop)
3. `lib/loop.py:115-178` — the dispatch chain
4. `lib/loop.py:336-409` — `_run_cold_start`
5. `lib/loop.py:412-479` — `_run_feedback_pass`
6. `lib/loop.py:531-636` — `_run_model_in_iteration`
7. `lib/loop.py:703-774` — `_run_assess`
8. `lib/loop.py:777-843` — `_run_source_integration`
9. `lib/loop.py:847-897` — `_get_prior_feedback`, `_has_revise_status`, `_get_review_feedback`
10. `lib/loop.py:293-333` — `_merge_feedback`
11. `lib/iteration.py:55-100` — `read_loop_state` (how resume figures out where to start)
12. `lib/iteration.py:103-145` — `write_verdict`, `parse_verdict_from_feedback`
13. `lib/sources.py:9-24` — `find_sources`
14. `lib/validators.py:1-100` — regex constants and `validate_feedback_verdict`
15. `lib/state.py:64-122` — `propagate_staleness` (downstream artifact stamping)
