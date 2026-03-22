# Review: {{concept_name}}

You are performing a structured quality review of the concept analysis and model
setup for **{{concept_name}}** ({{company}}).

## Your Task

Verify factual claims, check calculations, audit model parameters, and identify
issues. Produce a structured review report with Proposed Actions.

## Files to Review

### Analysis
`{{analysis_path}}`

### Model Setup (if exists)
{{#if model_setup_path}}
`{{model_setup_path}}`
{{/if}}

### Source Documents (for citation verification)
{{source_paths}}

## Review Checklist

### 1. Citation Verification
For each direct quote in the analysis:
- Search the cited source file for the quoted text
- Report: FOUND (exact or near-match) or NOT FOUND
- If NOT FOUND, search other source files for the claim

For section-level references in the parameter table:
- Verify the cited section exists in the source file
- Verify the claimed value appears in that section

### 2. Calculation Verification
For each derived/inferred value (marked with [inferred] or derivation chain):
- Re-derive the calculation independently
- Report: MATCH or MISMATCH with your derivation shown
- Check units and order of magnitude

### 3. Model Setup Audit (if model_setup.py exists)
For each `model.forward()` parameter:
- Verify it traces to a value in analysis.md
- Check the comment citation is accurate
- Flag any parameter without a source citation
For each cost_override:
- Verify the override value is justified
- Check that eliminated cost items (=0) are appropriate for this concept
For the ConfinementConcept choice:
- Is it the right base concept for this fusion approach?
- Are the override notes adequate?

### 4. Internal Consistency
- Do Section 5 parameter values match Section 2 narrative claims?
- Do TRL ratings in Section 3 align with the challenges in Section 2?
- Does the model setup use values consistent with the parameter table?

### 5. Factual Concerns
- Any claims that appear unsupported by the cited sources?
- Any numbers that seem physically implausible?
- Any potential hallucinations (specific claims with no traceable source)?

## Output Format

Write the review to: `{{output_path}}`

Use this exact format:

```
# Review: {{concept_name}}

**Iteration:** {{iteration}}
**Date:** {{date}}
**Files reviewed:** analysis.md{{#if model_setup_path}}, model_setup.py{{/if}}
**Source documents:** {{source_count}} files

---

## Citation Verification

[For each verified citation:]

### CV-N: [quoted claim or parameter]
- **Source cited:** [filename §section]
- **Status:** FOUND | NOT FOUND | PARTIAL MATCH
- **Actual text:** "[text found in source, or 'not found']"
- **Notes:** [any discrepancy]

---

## Calculation Verification

### CALC-N: [inferred value]
- **Claimed:** [value with derivation]
- **Re-derived:** [your independent calculation]
- **Status:** MATCH | MISMATCH
- **Notes:** [explanation if mismatch]

---

## Model Setup Audit

### MSA-N: [parameter or override]
- **Value:** [from model_setup.py]
- **Source:** [cited analysis section]
- **Status:** TRACED | UNTRACED | INCORRECT
- **Notes:** [issues found]

---

## Consistency Check

[Narrative of consistency findings]

---

## Proposed Actions

### PA-1: [Short description]
- **Category:** citation-error | calculation-error | model-bug | inconsistency | factual-concern | improvement
- **Severity:** blocking | important | minor
- **Location:** [file §section or line]
- **Finding:** [what the review found]
- **Proposed Fix:** [what should change]
- **Decision:** _[USER FILLS IN: agree | reject | alternative]_
- **User Notes:** _[USER FILLS IN]_

### PA-2: ...
[Continue for all issues found]

---

## Summary

- **Total citations checked:** N
- **Citations verified:** N
- **Citations not found:** N
- **Calculations checked:** N
- **Calculations matched:** N
- **Model parameters audited:** N
- **Proposed Actions:** N (blocking: N, important: N, minor: N)
- **Overall:** CLEAN | HAS ISSUES
```
