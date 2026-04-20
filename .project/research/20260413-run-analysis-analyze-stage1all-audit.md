---
date: 2026-04-13T00:00:00-07:00
researcher: Claude
topic: "Full audit of run_analysis.py analyze and stage1-all commands"
tags: [research, concept-analysis, pipeline]
status: complete
last_updated: 2026-04-13
---

# Research: Audit of `analyze` and `stage1-all` Commands

**Date**: 2026-04-13
**Researcher**: Claude
**Research Type**: Codebase

## Research Question

Full audit of `run_analysis.py` `analyze` and `stage1-all` — what each loop does exactly, what prompts are used, how they're formed, what actions they take, what validations they perform, and what flags/features each supports.

## Summary

- **`analyze`** is the core command. It resolves concepts, then delegates to `run_stage1_loop()` in `lib/loop.py` which runs an iterative assess↔analyze loop with in-loop model-setup.
- **`stage1-all`** is a thin orchestrator that calls `cmd_gap_check` (optional) → `cmd_analyze` → `cmd_model_setup` → `cmd_review` sequentially, passing the same args to each.
- The loop body per iteration is: **[feedback-producer] → analyze → model-setup → assess**
- There are 5 feedback-producer sources: cold_start, assess, review, source_integration, research
- All Claude invocations use `invoke_claude_validated()` which provides retry-via-resume (up to 2 retries = 3 total attempts)

---

## `analyze` Command — Detailed Breakdown

### Entry Point: `cmd_analyze()` (run_analysis.py:263)

**Concept resolution**: `resolve_concepts()` with `target_state="approved"` — filters to concepts not yet approved.

**Skip logic**: If `analysis.md` exists and neither `--force` nor `--resume`, skip the concept.

**Special mode — `--feedback`**: If a feedback file is provided, calls `_apply_external_feedback()` instead of the loop. This is a one-shot feedback-pass that edits an existing `analysis.md` using the `analysis_v2.md` template in feedback-pass mode. Validated with `make_file_modified_validator` (SHA-256 changed). Archives the feedback file on success.

**Normal mode**: Loads templates, builds common vars, delegates to `run_stage1_loop()`.

### Common Template Variables (`_build_common_vars()`, run_analysis.py:347)

Built once per concept:

| Variable | Source |
|----------|--------|
| `concept_id` | Concept's `_id` |
| `concept_name` | From CSV table |
| `company` | From CSV table |
| `dossier_path` | Phase 1a dossier path |
| `source_paths` | All extracted source `.md` files for this concept |
| `brief_path` | Analysis brief document |
| `schema_path` | Controlled vocabulary/column definitions |
| `exemplar_paths` | Handwritten exemplar analyses |
| `approved_analyses` | List of already-approved analysis.md files |
| `output_template_path` | Section structure template |
| `analysis_path` | Target `analysis.md` path |
| `memory_context` | Cross-concept memory (from prior analyses) |
| `concept_landscape` | Compact status table of all other concepts |

### The Stage 1 Loop: `run_stage1_loop()` (lib/loop.py:52)

**Loop structure**: `for iter_num in range(start_iter, max_passes + 1)`

Each iteration creates `iter-N/` directory and runs these steps:

#### Step 1: Feedback-Producer Selection (priority order)

| Priority | Condition | Source | What it does |
|----------|-----------|--------|--------------|
| 1 | `iter_num == 1` and not resume | `cold_start` | No feedback — fresh analysis |
| 2 | `analysis.md` has `Review-Status: revise` (one-shot) | `review` | Extracts `### F-N:` findings from `review.md`'s "Corrective Actions" section → writes to `iter-N/feedback.md` |
| 3 | New sources detected + not yet used source-integration | `source_integration` | Runs `source_integration.md` template prompt. Produces VERDICT:PASS or VERDICT:FINDINGS. If PASS, falls through to assess. |
| 4 | `--research` flag + `iter_num > 1` | `research` | Runs web search for data gaps → extracts sources → chains to source-integration → merges with prior assess feedback |
| 5 | Default (`iter_num > 1`) | `assess` | Uses prior iteration's `feedback.md` |

#### Step 2: Analyze

Two modes based on feedback source:

**Cold Start** (`_run_cold_start`, loop.py:317):
- **Template**: `analysis_v2.md` with `cold_start=true`
- **Action**: Claude **writes a new file** (`iter-N/analysis_body.md`) using Write tool
- **Pre-step**: Pipeline pre-writes `analysis.md` with YAML frontmatter
- **Post-step**: Pipeline concatenates frontmatter + body → `analysis.md`, deletes body file
- **Validation**: `validate_non_empty` (body file must have content)
- **Prompt vars**: `output_path=iter-N/analysis_body.md`, `cold_start=true`, `feedback_pass=""`, `feedback_path=""`

**Feedback Pass** (`_run_feedback_pass`, loop.py:388):
- **Template**: `analysis_v2.md` with `feedback_pass=true`
- **Action**: Claude **edits existing** `analysis.md` using Edit tool
- **Validation**: `make_file_modified_validator` — SHA-256 of `analysis.md` must change
- **Prompt vars**: `output_path=""`, `cold_start=""`, `feedback_pass=true`, `feedback_path=iter-N/feedback.md`

#### Step 3: Capture Analysis Output (loop.py:455)

Copies body of `analysis.md` (sans frontmatter) to `iter-N/analysis_output.md` for audit trail.

#### Step 4: Model Setup (`_run_model_in_iteration`, loop.py:475)

- **Template selection**: `model_setup_costingfe.md` if concept maps to a 1costingfe ConfinementConcept, else `model_setup_freeform.md`
- **Action**: Claude **writes** `iter-N/model_setup.py` using Write tool
- **Feedback integration**: Assessment findings (all `### F-N:` blocks) from the current iteration's feedback are passed as `model_feedback` in the template
- **Validation**: `validate_python_syntax` — `compile(..., 'exec')` must succeed
- **Post-step**: If validation passes, runs the model script (`uv run python model_setup.py`) and captures output to `iter-N/model_output.txt`
- **Non-fatal**: Model failures leave `model_ok=False` but the loop continues (FR-7)

**Canonical file promotion** (`_update_canonical_files`, loop.py:809):
- Only copies `model_setup.py` and `model_output.txt` from `iter-N/` to concept root when `model_ok=True` (H-16 guard)

#### Step 5: Assess (`_run_assess`, loop.py:612)

- **Template**: `assessment.md`
- **Action**: Claude **writes** `iter-N/feedback.md` using Write tool
- **Prompt vars**: `concept_name`, `analysis_path`, `feedback_path=iter-N/feedback.md`, `model_output_path` (if model output exists), `concept_landscape`
- **Validation**: `validate_feedback_verdict` — requires:
  - `VERDICT: PASS` or `VERDICT: FINDINGS` line
  - If FINDINGS: at least one `### F-N:` block
  - If FINDINGS: each finding has `- **Category:** analysis|model`
- **Verdict parsing**: `parse_verdict_from_feedback()` extracts verdict and finding count
- **Loop exit**: If `PASS`, loop returns immediately. If `FINDINGS` and more passes remain, continues.

**Skipped if `max_passes <= 1`**: Writes `SINGLE_PASS` verdict, returns.

#### Step 6: Verdict & Staleness

Each iteration writes `iter-N/verdict.json` containing: iteration number, verdict, finding count, feedback source, model_ran, model_ok, research_ran, sources list, merged_assess flag. `propagate_staleness()` marks downstream artifacts (extraction, etc.) as stale.

### Source Integration (`_run_source_integration`, loop.py:686)

- **Template**: `source_integration.md`
- **Action**: Claude **writes** `iter-N/source_integration_output.md`
- **Validation**: `validate_feedback_verdict` (same as assess)
- **Returns**: `None` if PASS (no material additions), else the output path
- **When used with research**: Output is merged with prior assess findings via `_merge_feedback()` which appends a "Carried-Forward Assessment Findings" section

---

## `stage1-all` Command — Detailed Breakdown

### Entry Point: `cmd_stage1_all()` (run_analysis.py:994)

**Extremely thin orchestrator.** Resolves concepts once for display, then calls each stage handler sequentially:

```python
stages = []
if args.include_gap_analysis:
    stages.append(("Gap Check", cmd_gap_check))
stages.extend([
    ("Analyze", cmd_analyze),
    ("Model Setup", cmd_model_setup),
    ("Review", cmd_review),
])

for stage_name, handler in stages:
    handler(concepts, args)
```

**Key behavior**: Passes the **same `args`** namespace to all handlers. This means all shared flags (--model, --dry-run, --timeout, --force, --max-passes, --resume, etc.) propagate to every stage.

**IMPORTANT subtlety**: `cmd_model_setup` and `cmd_review` are called as standalone stages AFTER `cmd_analyze`. But `cmd_analyze` already runs model-setup inside the loop (Step 4 above). The standalone `cmd_model_setup` call will **skip** if `model_setup.py` already exists (unless `--force`), so it's a safety net / catch-up for concepts that didn't get model-setup in the loop (e.g., single-pass mode or errors).

Similarly, `cmd_review` runs after analyze completes — it reads the final `analysis.md` and `model_output.txt`.

### Final status: Prints per-concept state after all stages complete.

---

## Flag/Feature Summary Table

### `analyze` Flags

| Flag | Default | What it does |
|------|---------|-------------|
| `concepts` | `[]` | Positional concept IDs to process |
| `--all` | `false` | Process all remaining (not-yet-approved) concepts |
| `--family` | `None` | Filter by confinement family (MFE, IFE, MIF, Non-Standard) |
| `--model` | `sonnet` | Claude model to use (sonnet, opus, haiku) |
| `--dry-run` | `false` | Generate prompts to disk without calling Claude |
| `--timeout` | `900` | Per-invocation timeout in seconds |
| `--force` | `false` | Clear all prior iterations and restart from scratch |
| `--max-passes` | `3` | Max analyze→assess iterations (1 = no assessment step) |
| `--add-passes N` | `None` | Run N additional passes from current iteration (implies --resume) |
| `--feedback PATH` | `None` | Apply external feedback file to existing analysis (single concept only, skips loop) |
| `--resume` | `false` | Continue from last iteration rather than starting fresh |
| `--research` | `false` | Enable autonomous web-search research step between iterations |
| `--max-research-searches` | `5` | Max WebSearch calls per research step |
| `--max-research-extractions` | `3` | Max source extractions per research step |

**Mutual exclusions**:
- `--resume` and `--force` are mutually exclusive
- `--feedback` and `--resume` are mutually exclusive
- `--feedback` and `--force` are mutually exclusive
- `--feedback` requires single concept

### `stage1-all` Flags

| Flag | Default | What it does |
|------|---------|-------------|
| `concepts` | `[]` | Positional concept IDs to process |
| `--all` | `false` | Process all remaining concepts |
| `--family` | `None` | Filter by confinement family |
| `--model` | `sonnet` | Claude model to use |
| `--dry-run` | `false` | Generate prompts without calling Claude |
| `--timeout` | `900` | Per-invocation timeout in seconds |
| `--force` | `false` | Re-run even if output exists (propagates to ALL stages) |
| `--max-passes` | `3` | Max analyze→assess iterations |
| `--add-passes N` | `None` | Run N additional passes (implies --resume, propagates to analyze) |
| `--include-gap-analysis` | `false` | Include gap-check stage before analyze |
| `--resume` | `false` | Resume analysis from last iteration |
| `--research` | `false` | Enable autonomous research step |
| `--max-research-searches` | `5` | Max WebSearch calls per research step |
| `--max-research-extractions` | `3` | Max source extractions per research step |

**Note**: `stage1-all` does NOT have `--feedback` — that's analyze-only.

---

## Prompt → Action → Validation Summary Table

| Step | Template | Mode | Action (what Claude does) | Output File | Validator | Retry? |
|------|----------|------|--------------------------|-------------|-----------|--------|
| Analyze (cold start) | `analysis_v2.md` | `cold_start=true` | **Write** new file | `iter-N/analysis_body.md` | `validate_non_empty` | Yes (2 retries) |
| Analyze (feedback pass) | `analysis_v2.md` | `feedback_pass=true` | **Edit** existing `analysis.md` | `analysis.md` (in-place) | `make_file_modified_validator` (SHA-256 changed) | Yes (2 retries) |
| Model Setup (costingfe) | `model_setup_costingfe.md` | — | **Write** new file | `iter-N/model_setup.py` | `validate_python_syntax` (compile check) | Yes (2 retries) |
| Model Setup (freeform) | `model_setup_freeform.md` | — | **Write** new file | `iter-N/model_setup.py` | `validate_python_syntax` (compile check) | Yes (2 retries) |
| Model Run | N/A (subprocess) | — | `uv run python model_setup.py` | `iter-N/model_output.txt` | Runtime success (rc=0) | No |
| Assess | `assessment.md` | — | **Write** new file | `iter-N/feedback.md` | `validate_feedback_verdict` (VERDICT line + F-N format + Category fields) | Yes (2 retries) |
| Source Integration | `source_integration.md` | — | **Write** new file | `iter-N/source_integration_output.md` | `validate_feedback_verdict` | Yes (2 retries) |
| External Feedback | `analysis_v2.md` | `feedback_pass=true` | **Edit** existing `analysis.md` | `analysis.md` (in-place) | `make_file_modified_validator` | Yes (2 retries) |
| Gap Check (stage1-all only) | `gap_check.md` | — | **Stdout** (no file write) | `gap_report.md` (pipeline writes) | `validate_non_empty` | Yes (2 retries) |
| Review (stage1-all only) | `review.md` | — | **Write** new file | `review.md` | `validate_review_verdict` (VERDICT: PROCEED/REVISE) | Yes (2 retries) |

---

## Iteration Lifecycle Diagram

```
analyze 01 --max-passes 3
│
├─ iter-1/
│   ├─ [cold_start] → analyze_prompt.md (saved)
│   │   → Claude writes analysis_body.md (validated: non-empty)
│   │   → Pipeline assembles: frontmatter + body → analysis.md
│   ├─ analysis_output.md (captured snapshot)
│   ├─ model_setup_prompt.md → Claude writes model_setup.py (validated: Python syntax)
│   │   → Pipeline runs model → model_output.txt
│   ├─ assess_prompt.md → Claude writes feedback.md
│   │   (validated: VERDICT line + F-N blocks + Category fields)
│   └─ verdict.json {verdict: "FINDINGS", finding_count: 2, ...}
│
├─ iter-2/
│   ├─ [assess feedback from iter-1] → analyze_prompt.md
│   │   → Claude EDITS analysis.md (validated: SHA-256 changed)
│   ├─ analysis_output.md (captured snapshot)
│   ├─ model_setup_prompt.md → Claude writes model_setup.py
│   │   → Pipeline runs model → model_output.txt
│   ├─ assess_prompt.md → Claude writes feedback.md
│   └─ verdict.json {verdict: "PASS", finding_count: 0, ...}
│
└─ returns "PASS"
```

---

## Resume Semantics

When `--resume` is used:
1. `read_loop_state()` scans existing `iter-N/verdict.json` files
2. `start_iter` is set to `loop_state.next_iteration` (first iteration without a verdict)
3. `detect_new_sources()` compares sources in the last verdict's source list against current filesystem
4. If new sources found, the source-integration feedback-producer fires on the next iteration

When `--add-passes N` is used:
1. Implies `--resume`
2. `max_passes` is dynamically set to `current_iteration + N` per concept
3. Allows different concepts at different iterations to all get N more passes

---

## Code References

- `cmd_analyze`: `run_analysis.py:263-344`
- `cmd_stage1_all`: `run_analysis.py:994-1036`
- `run_stage1_loop`: `lib/loop.py:52-239`
- `_run_cold_start`: `lib/loop.py:317-385`
- `_run_feedback_pass`: `lib/loop.py:388-452`
- `_run_model_in_iteration`: `lib/loop.py:475-552`
- `_run_assess`: `lib/loop.py:612-683`
- `_run_source_integration`: `lib/loop.py:686-752`
- `_build_common_vars`: `run_analysis.py:347-386`
- `build_model_vars`: `lib/loop.py:555-609`
- `_apply_external_feedback`: `run_analysis.py:389-464`
- `invoke_claude_validated`: `lib/claude.py:228-340+`
- Validators: `lib/validators.py`
- Templates: `exploration/concept_analysis/prompt_templates/`
- CLI parser: `run_analysis.py:1148-1283`
