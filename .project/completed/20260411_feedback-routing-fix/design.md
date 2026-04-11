# Design: Feedback Routing Fix — Target Categories + Assess Finding Preservation

**Status:** Complete
**Owner:** Reid W
**Created:** 2026-04-06 06:50 PDT
**Updated:** 2026-04-06
**Branch:** `design-space-explore`
**Commit:** 619efb9

---

## Overview

Two feedback routing bugs in the iteration loop:

**Problem A**: Assessment findings that target model code (e.g., "add REBCO to sensitivity sweep") bounce indefinitely because the model-setup agent never sees them. Fix: add a `Category` field to feedback, parse it in `loop.py`, inject model-targeted findings into the model-setup prompt.

**Problem B**: When `--research` acquires sources, the research→source-integration chain replaces the prior iteration's assess feedback entirely. The analysis agent sees "integrate these sources" but never "fix nearest-neighbor designations." Fix: merge carried-forward assess findings with source-integration output into a single feedback file.

## Related Artifacts

- **Spec:** `.project/active/feedback-routing-fix/spec.md`
- **Batch plan:** `.project/active/batch-pipeline-run/plan.md`
- **Evidence (A):** Concept 01 iter 4-7 — F-2 "REBCO cost absent" repeats because model-setup never sees it
- **Evidence (B):** Concept 07 iter 3-6 — assess findings dropped every iteration by research→source-integration; concept 09 iter-6 only made progress because research found nothing that iteration

## Research Findings

### Current Data Flow

The iteration loop runs: `[feedback-producer] → analyze → model-setup → assess`.

- **Analysis agent** receives `feedback_path` via the `analysis_v2.md` template (`loop.py:310-315`). It reads findings and edits `analysis.md`.
- **Model-setup agent** receives `analysis_path` via `build_model_vars()` (`loop.py:427-478`). It reads `analysis.md` and generates `model_setup.py`. **It never sees the feedback file.**
- **Assessment agent** evaluates both `analysis.md` and `model_output.txt`, writing findings to `feedback.md` via `_run_assess()` (`loop.py:481-534`).

### Feedback-Producer Priority Chain (Problem B Root Cause)

The feedback-producer selection (`loop.py:105-161`) is an `elif` cascade:

```
1. Cold start (iter 1, not resume)
2. Review kick-back (one-shot via used_review_feedback guard)
3. Source-integration on resume (one-shot via used_source_integration guard)
4. Research (--research flag, iter > 1)     ← NO one-shot guard, fires every iter
5. Normal assess feedback                   ← fallback, only reached if above don't match
```

When research acquires sources (line 146 `if acquired:`), it chains to `_run_source_integration()` which writes `source_integration_output.md` containing findings about the new sources. This path is returned as `feedback_path` and passed to `_run_feedback_pass()` — the analysis agent reads it instead of the prior iteration's `feedback.md`.

**Key insight**: the bug is not just "research fires too often" — even if research were one-shot, the source-integration feedback would still **replace** rather than **supplement** the assess findings. Both sub-bugs must be fixed:
1. The research branch always preempts assess feedback (structural)
2. Source-integration output replaces rather than merges with assess findings (data loss)

### Source-Integration Output Format

`_run_source_integration()` (`loop.py:537-592`) writes to `iter-N/source_integration_output.md`. The file uses the standard feedback format (VERDICT + F-N findings), making it structurally compatible with assess feedback. Example from concept 07 iter-4:

```
VERDICT: FINDINGS

### F-1: DS machine gain target is net facility gain...
- **Target:** Section 3...
- **Finding:** ...
- **Recommendation:** ...
- **Priority:** important
```

This means merging is straightforward: both files are the same format. We can concatenate findings under appropriate headers.

### Assessment Output Path

`_run_assess()` (`loop.py:481-534`) always writes to `iter_dir / "feedback.md"` (line 494). This is the file that gets read by the next iteration's feedback-producer selection. The assess agent writes the verdict and findings here. For Problem B, we need the **prior** iteration's `feedback.md` — the one the current iteration's analysis agent should have seen.

### Feedback Format

Current format per finding (`config/feedback_format.md`):
```
### F-N: [Short title]
- **Target:** ...
- **Finding:** ...
- **Recommendation:** ...
- **Priority:** blocking | important | minor
```

Parsing: `parse_verdict_from_feedback()` in `iteration.py:132-140` uses `re.findall(r"^### F-\d+:", ...)` to count findings and `re.search(r"^VERDICT:\s*PASS", ...)` for the verdict. Category parsing will follow this pattern.

### Template Engine

`fill_template()` in `templating.py` supports:
- `{{variable}}` substitution (string values)
- `{{#if var}}...{{/if}}` conditionals (truthy = non-empty string)
- `{{@path}}` config file inclusion

Model templates already use `{{#if}}` for optional sections (e.g., `mapping_notes` in `model_setup_costingfe.md:33`). The `model_feedback` variable fits this pattern: empty string when no model findings exist, populated string when they do.

### build_model_vars() Integration Point

`build_model_vars()` (`loop.py:427-478`) returns `(template_name, vars_dict)`. The `vars_dict` is passed directly to `fill_template()`. Adding `model_feedback` to `vars_dict` is the injection point.

The function has a `standalone` parameter for use from `cmd_model_setup` (outside the loop). The standalone path has no feedback to route, so `model_feedback` will default to `""`.

## Proposed Design

### 1. Feedback Format (`config/feedback_format.md`)

Add `Category` field between `Target` and `Finding`:

```
### F-N: [Short title]
- **Target:** [Section number or aspect of analysis]
- **Category:** analysis | model
- **Finding:** [What is insufficient...]
- **Recommendation:** [What should change...]
- **Priority:** blocking | important | minor
```

Update the rules section to explain the distinction. Update the example to show `Category: analysis`.

### 2. Assessment Template (`assessment.md`)

Add a new section after the existing "## Instructions" block (before "## Scope") with categorization guidance:

```markdown
### Finding Categories

Each finding must include a `Category` field:
- **`analysis`** — the fix requires changes to the analysis text (Section 2 framing,
  Section 5 parameter tables, Section 7 differentiator discussion, etc.)
- **`model`** — the fix requires changes to the model code or parameters:
  sensitivity sweeps, scenario branches, parameter values in model_setup.py,
  model output formatting, or computational methodology

A finding is `model` when the recommendation says to change what the model
*computes or sweeps*. A finding is `analysis` when the recommendation says
to change what the analysis *says or frames*.

When a finding touches both (e.g., "add parameter to Section 5 table AND
to sensitivity sweep"), assign the **primary** target — the one that would
resolve the core issue.
```

### 3. Model-Setup Templates (`model_setup_costingfe.md`, `model_setup_freeform.md`)

Add a conditional section after "## Required Reading" in both templates:

```markdown
{{#if model_feedback}}
## Assessment Feedback (Model-Targeted)

The following findings from the most recent assessment specifically target
the model code. Address each one when generating the script:

{{model_feedback}}
{{/if}}
```

Position after Required Reading so the agent reads its data sources first, then sees what specific issues to fix. This matches the existing pattern where the exemplar and analysis come before task-specific instructions.

### 4. Analysis Template (`analysis_v2.md`, feedback-pass section)

Add a note after line 125 ("Address each finding.") in the feedback-pass section:

```markdown
Findings marked `Category: model` primarily target the model code (sensitivity
sweeps, scenarios, parameters in model_setup.py). You should still update
analysis prose where relevant (e.g., Section 5 parameter tables, modeling
approach descriptions) to support the model change, but do NOT try to resolve
model findings solely through narrative rewording — the model-setup agent
will receive these findings directly.

If the feedback contains a "Carried-Forward Assessment Findings" section,
those are unresolved findings from the prior assessment that were preserved
across a source-integration pass. Treat them with the same priority as
regular findings — they represent issues the assessment flagged that you
haven't yet had a chance to address.
```

### 5. Loop Code (`lib/loop.py`) — Problem A: Model Feedback Extraction

#### 5a. Shared helper: `_split_findings()`

Both `_extract_model_findings` and `_merge_feedback` need to split feedback text into individual finding blocks. Extract the shared regex into a helper:

```python
def _split_findings(text: str) -> list[str]:
    """Split feedback text into individual F-N finding blocks.

    Returns a list of stripped finding blocks (each starting with '### F-N:').
    Non-finding preamble (VERDICT line, etc.) is excluded.
    """
    parts = re.split(r"(?=^### F-\d+:)", text, flags=re.MULTILINE)
    return [p.strip() for p in parts if re.match(r"^### F-\d+:", p)]
```

#### 5b. New helper: `_extract_model_findings()`

```python
def _extract_model_findings(feedback_path: Path | None) -> str:
    """Extract model-targeted findings from a feedback file.

    Returns formatted text of model-targeted findings, or empty string
    if none exist. Findings without a Category field default to 'analysis'
    (backward compatibility).
    """
    if feedback_path is None or not feedback_path.exists():
        return ""

    text = feedback_path.read_text(encoding="utf-8")
    finding_blocks = _split_findings(text)

    model_findings = []
    for block in finding_blocks:
        # Check for Category: model (permissive regex — tolerates missing
        # bold markers since this is a new field the LLM hasn't been trained on)
        cat_match = re.search(
            r"^\-\s+\**Category\**:?\s*(analysis|model)",
            block, re.MULTILINE,
        )
        if cat_match and cat_match.group(1) == "model":
            model_findings.append(block.strip())

    return "\n\n".join(model_findings)
```

Key behaviors:
- Uses `_split_findings()` shared helper for finding extraction
- Permissive regex for `Category`: tolerates `- **Category:** model`, `- Category: model`, `- **Category**: model`
- Missing `Category` field → not matched → defaults to `analysis` (FR-6 backward compat)
- Returns empty string when no model findings → `{{#if model_feedback}}` evaluates falsy

#### 5c. Wire into `_run_model_in_iteration()`

The loop already resolves `feedback_path` before calling `_run_model_in_iteration()` (set by the feedback-producer selection block at `loop.py:106-161`). Pass it through as a parameter rather than re-deriving it — this guarantees the model agent sees the exact same feedback the analysis agent acted on.

```python
def _run_model_in_iteration(
    concept: dict,
    iter_dir: Path,
    args: argparse.Namespace,
    feedback_path: Path | None = None,
) -> tuple[bool, bool]:
    # ... existing code ...

    model_feedback = _extract_model_findings(feedback_path)

    result = build_model_vars(concept, model_script, iter_dir,
                              model_feedback=model_feedback)
    if result is None:
        return False, False
    template_name, vars_dict = result
    # ... rest unchanged ...
```

The call site in `run_stage1_loop()` passes `feedback_path`:

```python
model_ran, model_ok = _run_model_in_iteration(concept, iter_dir, args, feedback_path)
```

#### 5d. Update `build_model_vars()` signature

```python
def build_model_vars(
    concept: dict,
    model_path: Path,
    iter_dir_or_out_dir: Path,
    *,
    standalone: bool = False,
    model_feedback: str = "",
) -> tuple[str, dict] | None:
```

Add `"model_feedback": model_feedback` to both the costingfe and freeform `vars_dict` branches. When called from standalone `cmd_model_setup`, the default empty string means the `{{#if model_feedback}}` block is suppressed.

### 6. Loop Code (`lib/loop.py`) — Problem B: Assess Finding Preservation

#### 6a. New helper: `_merge_feedback()`

When research acquires sources and chains to source-integration, the prior assess findings must be carried forward. The merge produces a single feedback file in `iter-N/feedback.md` that the analysis template's `{{feedback_path}}` points to.

```python
def _merge_feedback(
    assess_feedback_path: Path | None,
    source_integration_path: Path,
    output_path: Path,
) -> Path:
    """Merge carried-forward assess findings with source-integration output.

    Writes a combined feedback file to output_path. The source-integration
    output is the primary content; assess findings are carried forward
    under a separate header so the analysis agent can distinguish them.

    Returns output_path (always — even if no assess findings to carry).
    """
    si_text = source_integration_path.read_text(encoding="utf-8")

    # Check if there are assess findings to carry forward (FR-11)
    if assess_feedback_path is None or not assess_feedback_path.exists():
        output_path.write_text(si_text, encoding="utf-8")
        return output_path

    assess_text = assess_feedback_path.read_text(encoding="utf-8")
    assess_verdict, assess_count = parse_verdict_from_feedback(assess_text)

    if assess_verdict == "PASS" or assess_count == 0:
        # No findings to carry forward — use source-integration as-is
        output_path.write_text(si_text, encoding="utf-8")
        return output_path

    # Extract just the finding blocks from assess feedback (skip the VERDICT line)
    assess_findings = _split_findings(assess_text)

    # Build merged file:
    # 1. Source-integration content (with its own VERDICT line)
    # 2. Separator + carried-forward assess findings
    merged = si_text.rstrip() + "\n\n"
    merged += "---\n\n"
    merged += "## Carried-Forward Assessment Findings\n\n"
    merged += (
        "The following findings were flagged by the prior assessment but have not "
        "yet been addressed (they were carried forward across a source-integration "
        "pass). Address these alongside the source-integration findings above.\n\n"
    )
    merged += "\n\n".join(assess_findings)
    merged += "\n"

    output_path.write_text(merged, encoding="utf-8")
    return output_path
```

Design decisions:
- **Source-integration content comes first** because it's the "new" information; assess findings are "carried forward" context. This matches the analysis template's instruction ordering (read feedback, then address findings).
- **Findings keep their original F-N numbering** from their respective sources. The analysis agent sees e.g. F-1, F-2 from source-integration, then F-1, F-2, F-3 from assess. Re-numbering would add complexity for no benefit — the agent processes them by content, not by number.
- **The VERDICT line comes from source-integration**, which is always `FINDINGS` (if it were `PASS`, `_run_source_integration` would have returned `None` and this merge path wouldn't execute).
- **The original assess `feedback.md` in `iter-(N-1)/` is never modified** (FR-12) — the merged output is a new file in the current `iter-N/` directory.

#### 6b. Wire into the research branch of the feedback-producer cascade

Replace the current research branch (lines 136-157) with:

```python
elif getattr(args, "research", False) and iter_num > 1:
    feedback_source = "research"
    from lib.research import run_research_step
    acquired = run_research_step(concept, iter_dir, args)

    # Refresh sources after research (FR-15)
    current_sources = find_sources(rid)
    common_vars["source_paths"] = format_source_list(current_sources)

    if acquired:
        # Chain to source-integration for rich feedback (FR-10)
        si_path = _run_source_integration(
            concept, iter_dir, acquired, analysis_path, args)
        if si_path is not None:
            # Merge with prior assess findings so they aren't dropped (FR-8)
            assess_fb = _get_prior_feedback(concept_dir, iter_num)
            merged_assess = assess_fb is not None and assess_fb.exists()
            feedback_path = _merge_feedback(
                assess_fb, si_path, iter_dir / "feedback.md")
        else:
            # Source integration found PASS — use assess feedback as-is
            feedback_source = "assess"
            feedback_path = _get_prior_feedback(concept_dir, iter_num)
    else:
        # Nothing acquired — fall through to assess
        feedback_source = "assess"
        feedback_path = _get_prior_feedback(concept_dir, iter_num)
```

Key changes from current code:
1. **When source-integration produces findings**: instead of returning `si_path` directly as `feedback_path`, we call `_merge_feedback()` to combine it with the prior assess findings. The merged output goes to `iter-N/feedback.md`.
2. **All fallback paths remain unchanged**: when research finds nothing or source-integration finds PASS, we fall through to `_get_prior_feedback()` exactly as before.
3. **`merged_assess` flag**: tracks whether the merge actually carried forward assess findings (i.e., `assess_fb` existed). Initialize to `False` before the cascade; set to `True` in the merge path when prior assess feedback exists.

#### 6c. `verdict.json` metadata

Add `merged_assess: bool` to `write_verdict()` in `lib/iteration.py`. This records whether the iteration's feedback included carried-forward assess findings from a prior iteration, enabling post-hoc audit of which iterations had merged feedback vs. pure source-integration.

```python
def write_verdict(
    iter_dir: Path,
    *,
    iteration: int,
    verdict: str,
    finding_count: int,
    feedback_source: str,
    model_ran: bool,
    model_ok: bool,
    research_ran: bool,
    sources: list[str],
    merged_assess: bool = False,
) -> Path:
```

The call site in `run_stage1_loop()` passes the flag:

```python
write_verdict(iter_dir, iteration=iter_num, verdict=verdict,
              finding_count=finding_count, feedback_source=feedback_source,
              model_ran=model_ran, model_ok=model_ok,
              research_ran=(feedback_source == "research"),
              sources=[str(p) for p in current_sources],
              merged_assess=merged_assess)
```

Default `False` means existing call sites (error paths, single-pass) don't need changes.

#### 6d. File path collision consideration

`_run_assess()` writes to `iter_dir / "feedback.md"` (line 494). The merge also writes to `iter_dir / "feedback.md"` (the merged file). These run in different iterations: the merge writes to `iter-N/feedback.md` using the *prior* iteration's assess output at `iter-(N-1)/feedback.md`. No collision — different directories.

The source-integration output remains at `iter-N/source_integration_output.md` as before — `_merge_feedback` reads from it but doesn't modify it. Both the original source-integration output and the original assess feedback are preserved as audit artifacts.

### Summary of Changes by File

| File | Lines Changed | What | Problem |
|------|--------------|------|---------|
| `config/feedback_format.md` | ~10 | Add `Category` field, update rules, update example | A |
| `assessment.md` | ~15 | Add categorization instructions section | A |
| `model_setup_costingfe.md` | ~8 | Add conditional `{{#if model_feedback}}` section | A |
| `model_setup_freeform.md` | ~8 | Add conditional `{{#if model_feedback}}` section | A |
| `analysis_v2.md` | ~10 | Category semantics note + carried-forward explanation | A+B |
| `lib/loop.py` | ~80 | `_split_findings()`, `_extract_model_findings()`, `_merge_feedback()`, wire both into the loop, update `build_model_vars()` | A+B |
| `lib/iteration.py` | ~3 | Add `merged_assess` parameter to `write_verdict()` | B |

**FR-7 (3-finding cap):** No change needed. The cap is enforced by the assessment template's existing "at most 3 findings" instruction and the `feedback_format.md` rule "Maximum 3 findings per pass." Category is orthogonal — findings are counted across both categories. The merged feedback may temporarily exceed 3 findings (up to 3 from assess + findings from source-integration), which is acceptable per spec edge case: "The first iteration after a research acquisition will receive a larger feedback payload."

## Potential Risks

1. **LLM compliance with Category field**: The assessment agent may forget to include `Category` or use inconsistent formatting. Mitigation: the format spec and example are explicit; the parser falls back to `analysis` for missing categories, so worst case is the old behavior (no regression).

2. **Feedback ordering within iteration**: Model-setup runs *after* the analysis pass within the same iteration. The `feedback_path` passed through from the loop body is the same one the analysis agent just acted on — guaranteed by passing it as a parameter rather than re-deriving it. No race condition.

3. **Merged feedback size**: A merged file with 3 assess findings + 2 source-integration findings is ~5 findings. The analysis agent already handles multi-finding feedback and long source documents. The spec explicitly notes this is acceptable. If it becomes a problem, the spec's guidance is to cap carried-forward findings at 3 (same as a normal assessment pass), which is what we do — we carry all assess findings (which are already capped at 3 by the assessment template).

4. **F-N numbering collision in merged feedback**: Both the source-integration findings and carried-forward assess findings use independent F-N numbering. The analysis agent sees two F-1s (one from each section). This is acceptable — the section headers ("Carried-Forward Assessment Findings") provide disambiguation, and the agent processes findings by content, not by number. Re-numbering would add fragile text manipulation for no benefit.

5. **Source-integration already uses feedback_format.md**: The source-integration template includes `{{@config/feedback_format.md}}` which will now include the `Category` field. Source-integration findings will likely be categorized as `analysis` (they're about incorporating new source data into analysis prose), which is correct. No special handling needed.

6. **Category regex robustness**: The permissive regex tolerates minor LLM formatting variations, but if the LLM omits the Category field entirely, the finding falls back to `analysis`. This is the safe default — worst case is the old behavior (no regression).

## Integration Strategy

Problem A is purely additive — no changes to loop control flow, verdicts, or directory layout. Backward compatible with existing feedback files (missing Category → analysis).

Problem B modifies one branch of the feedback-producer cascade (the research branch) to merge rather than replace. All other branches (cold start, review, source-integration on resume, normal assess) are unchanged. The merged file is written to the same path the analysis template expects (`iter-N/feedback.md`), so no template changes are needed for the merge itself — only the instructional note in the analysis template about carried-forward findings.

## Validation Approach

### Problem A

1. **Unit check**: `--dry-run` on concept 01 → inspect `model_setup_prompt.md` for the `model_feedback` section. (Requires manually adding `Category: model` to an existing feedback file for the dry-run, since the assessment template change hasn't produced categorized feedback yet.)

2. **Live validation**: Run concept 01 for 1-2 iterations. Verify assessment produces categorized findings and model-setup prompt includes model-targeted findings.

3. **Backward compat**: Run on a concept with existing uncategorized feedback files. Verify no errors and `model_feedback` is empty (conditional suppressed).

### Problem B

4. **Unit check**: `--dry-run` on concept 07 with `--research` → inspect `iter-N/feedback.md` for the merged content (both source-integration findings and carried-forward assess findings). Also inspect that `iter-(N-1)/feedback.md` is unmodified.

5. **Live validation**: Run concept 07 for 2-3 iterations with `--research`. Verify:
   - When research acquires sources, the analyze prompt contains both source-integration findings AND prior assess findings (nearest-neighbor, rep-rate table)
   - The assess findings actually get addressed (finding count decreases)
   - When research finds nothing, the normal assess feedback path works unchanged

6. **PASS carry-forward skip**: Run on a concept where the prior assessment was PASS. Verify the merge is skipped and source-integration output is used as-is.

---

**Next Step:** After approval → `/_my_implement`
