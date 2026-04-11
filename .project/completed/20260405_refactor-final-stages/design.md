# Design: Final Stages Rescope (Work Item #3)

**Status:** Draft
**Owner:** reid
**Created:** 2026-04-05
**Branch:** design-space-explore
**Commit:** cfbff65

---

## Overview

Refocus the review step from numerical QA to strategic/qualitative assessment, add a PROCEED/REVISE verdict with kick-back to stage1, strengthen assess with numerical plausibility checks, and add a review gate on approve.

## Related Artifacts

- **Spec:** `.project/active/refactor-final-stages/spec.md`
- **Prereq:** `.project/active/refactor-stage1-loop/` (WI#2 — stage1 loop refactor, implemented in cfbff65)
- **Design concept:** `.project/active/refactor-run-analysis/design-concept.md`
- **Current prompts:** `prompt_templates/review.md`, `prompt_templates/assessment.md`, `prompt_templates/address_review.md`
- **Feedback format:** `prompt_templates/config/feedback_format.md`

---

## Research Findings

### Current Review Pipeline (run_analysis.py:422-493)

The review command:
1. Builds a prompt from `prompt_templates/review.md` with analysis, model, and source paths
2. Runs Claude, writes output to `review.md`
3. Post-hook: regex-detects `**Overall:** CLEAN` → sets `Review-Status: clean`, else `has-actions`
4. Increments `Review-Iterations`, sets `Last-Review` date

The output format uses CV-N (citation), CALC-N (calculation), MSA-N (model audit), and PA-N (proposed action) sections. PA-N actions have user-fillable `Decision: _[agree | reject | alternative]_` fields.

### Address-Review (run_analysis.py:496-599)

Parses PA-N actions from `review.md` via `parse_proposed_actions()` (lib/sources.py:164-214). Filters to actions with filled Decision fields. Runs Claude with `address_review.md` template in `output_mode="no_output"` (Claude edits files directly). Post-hook re-runs model if exists, sets `Review-Status: addressed`.

### Synthesize Gate (run_analysis.py:629-635)

```python
if review_status not in ("addressed", "clean"):
    print(f"  skip {cid} (Review-Status is '{review_status}'; ...")
    continue
```

### Approve Gate (run_analysis.py:736-777)

Only checks: `synthesis.md` exists OR `--force`. Does NOT check `Review-Status`.

### Stage1 Feedback-Producer Selection (lib/loop.py:96-198)

Priority order in the loop:
1. Cold start (iter 1, no resume)
2. Source-integration (resume + new sources, one-shot via `used_source_integration` flag)
3. Research (`--research`, iter > 1, stub)
4. Assess (default, iter > 1)

Key pattern: `used_source_integration` is a boolean flag set `True` after source-integration runs once. Prevents re-firing on subsequent iterations.

### Assessment Prompt (prompt_templates/assessment.md:37-46)

Explicit exclusion block:
```markdown
## What You Are NOT Checking
Do NOT evaluate any of the following — they are the review stage's responsibility:
- Numerical accuracy of parameter values
- Citation correctness (whether quotes match sources)
- Calculation verification (whether inferred values are derived correctly)
- Formatting or style consistency
- Whether the analysis matches the output template structure exactly
```

Model output conditional (lines 27-35) already passes model data to assess when available — it checks "consistency with analysis" but not numerical plausibility.

### Feedback Format (config/feedback_format.md)

F-N findings with Target, Finding, Recommendation, Priority. Rules section (line 26) explicitly says "Findings must NOT address numerical accuracy" — this needs updating alongside FR-8.

### State Detection (lib/state.py:10-57)

`get_concept_state()` maps `Review-Status` frontmatter to states:
- `has-actions` → falls through to `"drafted"` (not in the reviewed set)
- `clean` or `addressed` → `"reviewed"`

### Existing Analyses with Review-Status

Need backward compat for existing concepts with `has-actions`, `clean`, or `addressed` values.

### Config Files That Reference Review Exclusion

- `prompt_templates/config/feedback_format.md` line 26: "Findings must NOT address numerical accuracy, citation correctness, or calculations (those are the review stage's responsibility)"
- `prompt_templates/config/review_checklist.md`: 25-line checklist of verification checks

---

## Proposed Design

### Component 1: New Review Prompt Template

**File:** `prompt_templates/review.md` (replace current 144-line template)

**Approach:** Complete rewrite. The current template is structured around verification checklists (CV-N, CALC-N, MSA-N). The new template is structured around strategic assessment dimensions.

**New prompt structure:**

```
# Strategic Review: {{concept_name}}

## Task
Evaluate the strategic quality of this analysis — modeling approach, positioning,
risk framing, data sufficiency, and cross-concept consistency.

## Files to Review
- Analysis: {{analysis_path}}
- Model Setup: {{model_setup_path}} (if exists)
- Model Output: {{model_output_path}} (if exists)  ← NEW: pass model output
- Source Documents: {{source_paths}}
- Approved Prior Syntheses: {{approved_syntheses}}   ← NEW: for cross-concept

## Strategic Assessment Dimensions

1. **Modeling Approach**
   - Are the key cost drivers and differentiators captured?
   - Is the concept being modeled at the right level of abstraction?
   - Are the CAS mapping choices defensible?

2. **Strategic Positioning**
   - Does the analysis correctly characterize where this concept sits?
   - Are comparison axes meaningful for this concept type?
   - Is the cross-concept framing consistent with approved analyses?

3. **Risk and Uncertainty Framing**
   - Are the right risks highlighted (not just technical — also economic, supply chain)?
   - Is the confidence assessment realistic given data availability?
   - Are TRL ratings defensible?

4. **Data Sufficiency**
   - Are there critical gaps that should trigger more research?
   - Are the sources adequate for the claims being made?
   - Is the analysis honest about what it doesn't know?

5. **Cross-Concept Consistency**
   - Are assumptions consistent with approved analyses of related concepts?
   - Are shared subsystem cost estimates aligned?
   - Are differentiator claims supported by the comparison?

## Output Format

Write to: {{output_path}}

### Strategic Assessment
[Narrative assessment organized by the 5 dimensions above.
 Not a checklist — a reasoned evaluation.]

### Verdict

VERDICT: [PROCEED | REVISE]
<!-- MACHINE-PARSED: emit exactly "VERDICT: PROCEED" or "VERDICT: REVISE" on its own line -->

[If PROCEED]: This analysis is strategically sound.
[If REVISE]: The following issues require another pass through stage1.

### Minor Fixes (PROCEED only)
<!-- MACHINE-PARSED: use exactly "### Minor Fixes" as the heading -->
[Optional PA-N format actions for address-review. Same format as current:]

### PA-N: [title]
- **Category:** ...
- **Severity:** minor
- **Location:** ...
- **Finding:** ...
- **Proposed Fix:** ...
- **Decision:** _[USER FILLS IN]_
- **User Notes:** _[USER FILLS IN]_

### Corrective Actions (REVISE only)
<!-- MACHINE-PARSED: use exactly "### Corrective Actions" as the heading -->
[F-N format findings per config/feedback_format.md. These feed back into
 stage1-all --resume as the feedback source.]

### F-N: [title]
- **Target:** [Section or aspect]
- **Finding:** [Strategic issue]
- **Recommendation:** [What stage1 should do differently]
- **Priority:** blocking | important | minor
```

**Template variables — changes from current:**
- ADD `model_output_path`: path to model_output.txt (for review to assess model results)
- ADD `approved_syntheses`: formatted list of approved synthesis files (for cross-concept consistency)
- KEEP: `concept_name`, `company`, `analysis_path`, `model_setup_path`, `source_paths`, `source_count`, `output_path`, `iteration`, `date`

**Why this structure:** The current review produces ~100 lines of verification checklist output. The new review produces a narrative assessment with a clear binary verdict. The PA-N and F-N sections are conditional on the verdict, so the parser can detect which format to expect.

### Component 2: Verdict Detection in cmd_review Post-Hook

**File:** `scripts/run_analysis.py:468-478` (the `_post` closure inside `cmd_review`)

**Current detection:**
```python
review_status = "has-actions"
if re.search(r"\*\*Overall:\*\*\s*CLEAN", r.output_text, re.MULTILINE):
    review_status = "clean"
```

**New detection:**
```python
if re.search(r"^VERDICT:\s*PROCEED", r.output_text, re.MULTILINE):
    review_status = "proceed"
elif re.search(r"^VERDICT:\s*REVISE", r.output_text, re.MULTILINE):
    review_status = "revise"
else:
    # Fallback for legacy format
    if re.search(r"\*\*Overall:\*\*\s*CLEAN", r.output_text, re.MULTILINE):
        review_status = "clean"
    else:
        review_status = "has-actions"
```

**Why the fallback:** During migration, if someone re-runs review on a concept that somehow produces old-format output (e.g., cached prompt), the fallback ensures the frontmatter is still set correctly. This can be removed after all concepts have been through the new review.

**Preserved from current post-hook:** The `Review-Iterations` increment and `Last-Review` date update remain unchanged. Only the verdict detection logic changes — the frontmatter update block that writes `Review-Iterations`, `Last-Review`, and `Review-Status` stays as-is, with `Review-Status` now set to the new verdict-derived value.

### Component 3: Template Variable Additions for cmd_review

**File:** `scripts/run_analysis.py:441-460` (the `_build_vars` closure)

Add two new variables:

```python
# Model output path (if exists)
model_output_path = out_dir / "model_output.txt"

# Approved syntheses (for cross-concept consistency)
approved_syntheses = find_approved_syntheses(concepts)

def _build_vars(c, ...):
    return {
        # ... existing vars ...
        "model_output_path": str(_mop) if _mop.exists() else "",
        "approved_syntheses": format_approved_syntheses(_approved),
    }
```

`find_approved_syntheses()` already exists in `lib/memory.py:27-39` — it's used by `cmd_synthesize` (run_analysis.py:615). Reuse it directly. Format with the existing `format_path_list()` helper (`lib/memory.py:52-56`), which produces markdown bullet-point paths — the same format `cmd_synthesize` uses (run_analysis.py:666). No new helper needed.

```python
synth_list = [s for s in find_approved_syntheses() if s.parent.name != cid]
approved_syntheses = format_path_list(synth_list,
    empty_msg="(none yet — this is among the first reviews)")
```

### Component 4: Feedback-Producer Selection — Review Kick-Back

**File:** `scripts/lib/loop.py` — feedback-producer selection block (~lines 100-145)

**Current priority order:**
1. Cold start
2. Source-integration (one-shot)
3. Research (stub)
4. Assess (default)

**New priority order (insert at position 2):**
1. Cold start (iter 1, no resume)
2. **Review corrective actions** (resume + `Review-Status: revise`) — NEW, one-shot
3. Source-integration (resume + new sources, one-shot)
4. Research (`--research`, iter > 1)
5. Assess (default, iter > 1)

**Implementation:**

```python
# NEW: Review kick-back (FR-6)
# Check Review-Status before source-integration check
used_review_feedback = False  # init alongside used_source_integration

# In the selection block, after cold_start check:
elif not used_review_feedback and _has_revise_status(analysis_path):
    feedback_text = _get_review_feedback(concept_dir)
    used_review_feedback = True
    if feedback_text is not None:
        feedback_source = "review"
        # Caller writes feedback — loop owns file I/O
        feedback_path = iter_dir / "feedback.md"
        feedback_path.write_text(feedback_text, encoding="utf-8")
    else:
        # review.md exists but has no F-N findings — fall through
        feedback_source = "assess"
        feedback_path = _get_prior_feedback(concept_dir, iter_num)
```

**New helper functions in loop.py:**

```python
def _has_revise_status(analysis_path: Path) -> bool:
    """Check if analysis.md has Review-Status: revise."""
    fm = parse_frontmatter(analysis_path)
    return fm.get("Review-Status") == "revise"

def _get_review_feedback(concept_dir: Path) -> str | None:
    """Extract F-N findings from review.md as feedback text for stage1.

    Returns feedback text content (caller writes to iter-N/feedback.md),
    or None if review.md has no extractable F-N findings.
    """
    review_path = concept_dir / "review.md"
    if not review_path.exists():
        return None

    text = review_path.read_text(encoding="utf-8")

    # Extract the Corrective Actions section (F-N findings)
    # Look for ### F-N: pattern after VERDICT: REVISE
    verdict_match = re.search(r"^VERDICT:\s*REVISE", text, re.MULTILINE)
    if not verdict_match:
        return None

    # Extract everything from "### Corrective Actions" to end or next ## section
    ca_match = re.search(r"^### Corrective Actions.*$", text[verdict_match.end():],
                         re.MULTILINE)
    if not ca_match:
        return None

    ca_start = verdict_match.end() + ca_match.end()
    # Find next ## header or end of file
    next_section = re.search(r"^## ", text[ca_start:], re.MULTILINE)
    ca_text = text[ca_start:ca_start + next_section.start()] if next_section else text[ca_start:]

    # Prepend verdict line for the analysis agent's feedback-pass parser
    return f"VERDICT: FINDINGS\n\n{ca_text.strip()}\n"
```

**Contract:** Returns feedback text content (`str`), not a path. The caller in loop.py writes the text to `iter-N/feedback.md`. This matches the pattern where the loop owns file I/O and feedback-producers supply content.

**verdict.json update:** The `feedback_source` field already supports arbitrary strings. Adding `"review"` requires no schema change — just a new enum value in documentation.

### Component 5: Assessment Prompt Update

**File:** `prompt_templates/assessment.md` — two changes

**Change 1: Remove exclusion block (lines 37-46)**

Replace:
```markdown
## What You Are NOT Checking

Do NOT evaluate any of the following — they are the review stage's responsibility:
- Numerical accuracy of parameter values
- Citation correctness (whether quotes match sources)
- Calculation verification (whether inferred values are derived correctly)
- Formatting or style consistency
- Whether the analysis matches the output template structure exactly

Focus exclusively on whether the analysis captures the **shape** of the concept:
positioning, differentiators, TEA implications, modeling approach, and risks.
```

With:
```markdown
## Scope

Focus on whether the analysis captures the **shape** of the concept:
positioning, differentiators, TEA implications, modeling approach, and risks.

Additionally, check **numerical plausibility**:
- Are parameter values the right order of magnitude for this concept type?
- Does the model output LCOE align with the analysis narrative's claims?
- Are physical parameters (temperatures, pressures, efficiencies) within
  physically plausible ranges for the stated technology?

You are NOT checking formatting, style consistency, or template structure compliance.
```

**Change 2: Update model output conditional (lines 27-35)**

Strengthen the model consistency check to include plausibility:
```markdown
{{#if model_output_path}}
## Model Output

The concept also has a quantitative LCOE model. The model output is at:
`{{model_output_path}}`

Evaluate whether:
1. The model's assumptions and parameter values are consistent with the analysis.
2. The LCOE result is plausible for this concept type (order of magnitude).
3. Key cost drivers in the model match the analysis narrative's emphasis.
Note any discrepancies in your findings.
{{/if}}
```

### Component 6: Feedback Format Config Update

**File:** `prompt_templates/config/feedback_format.md` — line 26

**Current:**
```markdown
- Findings must NOT address numerical accuracy, citation correctness, or
  calculations (those are the review stage's responsibility)
```

**Replace with:**
```markdown
- Findings about numerical accuracy should focus on plausibility (order of
  magnitude, physical reasonableness), not verification (re-deriving calculations
  or matching citations to source text)
```

### Component 7: Address-Review Guard

**File:** `scripts/run_analysis.py:496-510` (early in `cmd_address_review`)

Add a guard after the `review_path.exists()` check:

```python
# NEW: Check Review-Status — address-review only valid for PROCEED verdict
fm = parse_frontmatter(analysis_path)
review_status = fm.get("Review-Status", "")
if review_status == "revise":
    print(f"  skip {cid} (Review-Status is 'revise' — "
          f"run stage1-all --resume to address review findings, "
          f"not address-review)")
    continue
```

No other changes to address-review mechanics — PA-N parsing, decision application, and `Review-Status: addressed` setting all work as-is for the PROCEED path.

### Component 8: Approve Gate

**File:** `scripts/run_analysis.py:754-762` (in `cmd_approve`, after the already-approved check)

Add review gate before the existing synthesis gate:

```python
# NEW: Review gate (FR-11)
review_status = fm.get("Review-Status", "")
if review_status not in ("proceed", "addressed", "clean") and not args.force:
    print(f"  skip {cid} (Review-Status is '{review_status}' — "
          f"run review first, or use --force)")
    continue

# Existing synthesis gate
synthesis_path = ANALYSES_DIR / cid / "synthesis.md"
if not synthesis_path.exists() and not args.force:
    print(f"  skip {cid} (no synthesis.md — run synthesize first, or use --force)")
    continue
```

Note: `clean` included for backward compat with existing reviewed concepts.

### Component 9: State Detection Update

**File:** `scripts/lib/state.py:33`

**Current:**
```python
elif fm.get("Review-Status", "") in ("addressed", "clean"):
    state = "reviewed"
```

**New:**
```python
elif fm.get("Review-Status", "") in ("addressed", "clean", "proceed"):
    state = "reviewed"
```

Add `"proceed"` to the set of statuses that map to the `"reviewed"` state. `"revise"` deliberately falls through to `"drafted"` — a concept with a REVISE review needs more work before it's considered reviewed.

### Component 10: Synthesize Gate Update

**File:** `scripts/run_analysis.py:631-632`

**Current:**
```python
if review_status not in ("addressed", "clean"):
```

**New:**
```python
if review_status not in ("addressed", "clean", "proceed"):
```

Add `"proceed"` so concepts with the new verdict format can proceed to synthesis. A PROCEED review with no PA-N actions can go straight to synthesis without address-review.

---

## Data Flow Summary

### PROCEED Path (happy path)
```
stage1 loop converges (PASS verdict)
  → cmd_review: new prompt → VERDICT: PROCEED
    → Review-Status: proceed
    → [optional] PA-N minor fixes → user fills decisions
      → cmd_address_review → Review-Status: addressed
  → cmd_synthesize (gates on: proceed | addressed | clean)
  → cmd_approve (NEW gate: proceed | addressed | clean + synthesis exists)
```

### REVISE Path (kick-back)
```
stage1 loop converges (PASS verdict)
  → cmd_review: new prompt → VERDICT: REVISE
    → Review-Status: revise
    → F-N corrective actions in review.md
    → user confirms/edits verdict
  → stage1-all --resume
    → _has_revise_status() → True
    → _get_review_feedback() extracts F-N from review.md
    → writes feedback.md to iter-N/
    → feedback_source: "review" in verdict.json
    → used_review_feedback = True
    → subsequent iterations use assess feedback
  → loop converges again
  → cmd_review (Review-Iterations increments)
    → VERDICT: PROCEED or REVISE again
```

### Legacy Path (backward compat)
```
Existing concepts with Review-Status: has-actions | clean | addressed
  → address-review still works (PA-N format unchanged)
  → synthesize still works (clean | addressed in gate set)
  → approve still works (clean | addressed in new gate set)
  → get_concept_state still returns "reviewed" for clean | addressed
```

---

## Potential Risks

1. **Review prompt quality.** The new review prompt is a complete rewrite. Its effectiveness depends on prompt tuning — the strategic dimensions may need iteration to produce consistently useful output. Mitigation: the prompt structure is modular (5 dimensions), so individual dimensions can be refined without rewriting the whole template.

2. **Verdict detection robustness.** Regex `^VERDICT:\s*PROCEED` on LLM output. If the agent buries the verdict in a quote block or doesn't emit it, detection fails. Mitigation: the legacy fallback catches old-format output; for new format, the prompt makes the verdict line a required output element with explicit formatting. If neither pattern matches, the default `has-actions` is safe (blocks synthesis until human intervenes).

3. **F-N extraction from review.md.** The `_get_review_feedback()` function parses review.md to extract corrective actions. If the agent formats the section differently than expected, extraction fails. Mitigation: the function returns `None` on parse failure, and the loop falls through to assess feedback — the concept still gets iterated, just without review-specific guidance.

4. **Review-assess scope overlap.** With FR-8 adding numerical plausibility to assess and the review moving to strategic assessment, there's overlap in "modeling approach" evaluation. This is acceptable — assess checks it on every iteration inside the loop, review checks it once after convergence with full context (approved syntheses, human judgment). The perspectives differ: assess asks "is this good enough to converge?" while review asks "is this good enough to ship?"

---

## Integration Strategy

This refactor touches 6 files in the existing pipeline:

| File | Changes | Risk |
|---|---|---|
| `prompt_templates/review.md` | Complete rewrite | Low — prompt only, no code deps |
| `prompt_templates/assessment.md` | Remove exclusion, add plausibility | Low — additive |
| `prompt_templates/config/feedback_format.md` | Relax numerical accuracy rule | Low — config only |
| `scripts/run_analysis.py` | Verdict detection, vars, guards, gate | Medium — core pipeline |
| `scripts/lib/loop.py` | Review feedback-producer, helpers | Medium — loop logic |
| `scripts/lib/state.py` | Add `"proceed"` to reviewed set | Low — one-line change |

No new files needed. No new dependencies. No changes to the stage1 loop's core iteration mechanics — only a new feedback-producer slot.

The changes are backward compatible: existing concepts with old Review-Status values continue to work through all pipeline stages. The new values (`proceed`, `revise`) only appear on concepts processed with the new review prompt.

**Review-Status consumers audit:** Only two Python files read `Review-Status`: `run_analysis.py` (cmd_review post-hook, cmd_synthesize gate, cmd_address_review) and `lib/state.py` (get_concept_state). `README.md` documents the field but contains no logic. No prompt templates or config files consume the value. All consumers are covered by Components 2, 7, 8, 9, and 10.

---

## Validation Approach

### Manual Testing

1. **New review on a fresh concept:** Run `review <concept>` → verify output has VERDICT line, Review-Status set correctly.
2. **PROCEED path:** Review(PROCEED) → address-review (if PA-N actions) → synthesize → approve. Verify gates pass.
3. **REVISE path:** Review(REVISE) → stage1-all --resume → verify review.md F-N findings appear as iter-N/feedback.md → verify verdict.json has `feedback_source: "review"` → verify loop converges → run review again → verify Review-Iterations increments.
4. **Address-review guard:** Run `address-review` on a concept with `Review-Status: revise` → verify redirect message.
5. **Approve gate:** Run `approve` on a concept without review → verify refusal. Run with `--force` → verify override.
6. **Backward compat:** Run `synthesize` and `approve` on an existing concept with `Review-Status: addressed` → verify gates pass unchanged.

### Automated Checks

The `get_concept_state()` function is pure (filesystem → string). Can add unit tests for:
- `Review-Status: proceed` → state `"reviewed"`
- `Review-Status: revise` → state `"drafted"`
- `Review-Status: has-actions` → state `"drafted"` (legacy, unchanged)

---

**Next Step:** After approval → `/_my_plan` for phased implementation, or `/_my_implement` directly (scope is manageable as a single implementation pass).
