# Fragile Control Flow in the Concept Analysis Pipeline

**Date**: 2026-04-06
**Topic**: Audit of all locations where the pipeline uses fragile parsing (regex, substring matching, string comparisons) for control flow decisions
**Scope**: `exploration/concept_analysis/scripts/` — all lib modules and `run_analysis.py`

## Summary

The pipeline has **7 distinct fragility zones** where program behavior depends on parsing free-text LLM output or loosely-typed string conventions. These form a dependency chain: LLM writes markdown → regex extracts verdicts/findings → control flow branches on the result. Any formatting deviation silently degrades to a default behavior (usually "FAIL" or "no findings found"), which is safe but opaque.

The fragilities fall into two tiers:
- **Tier 1 (LLM output parsing)** — regex on text that a language model wrote. This is the highest-risk category because the producer (Claude) has no formal contract enforcement and can vary output format across runs.
- **Tier 2 (Convention parsing)** — regex/string matching on data that the pipeline itself previously wrote. Lower risk because the producer is deterministic, but still fragile if conventions evolve.

---

## Fragility 1: Verdict Detection — `parse_verdict_from_feedback()`

**File**: `lib/iteration.py:134-142`
**Producer**: Claude (assessment step, source-integration step)
**Consumer**: `lib/loop.py` (loop continuation decision)

### Control Logic
```python
is_pass = bool(re.search(r"^VERDICT:\s*PASS", feedback_text, re.MULTILINE))
finding_count = len(re.findall(r"^### F-\d+:", feedback_text, re.MULTILINE))
return ("PASS" if is_pass else "FAIL", finding_count)
```

### Failure Modes
| Scenario | LLM writes | Regex sees | Pipeline does |
|----------|-----------|------------|---------------|
| Normal PASS | `VERDICT: PASS` | Match | Exits loop |
| Normal FAIL | `VERDICT: FINDINGS` + `### F-1:` blocks | No PASS match → FAIL | Continues loop |
| Indented verdict | `  VERDICT: PASS` | No match (not at line start) | **Wrongly FAILs** → extra iteration |
| Extra text on line | `VERDICT: PASS - all goals met` | Match (no `$` anchor) | Correct |
| Typo | `VERDICT: PAS` | No match | **Wrongly FAILs** → extra iteration |
| Missing verdict line | (LLM omits it) | No match | **Wrongly FAILs** → extra iteration |
| Findings without headers | Prose findings, no `### F-N:` | finding_count = 0 | FAIL with 0 findings (confusing but safe) |

### Consequences
Low severity. False-FAIL costs one extra iteration (~$0.50 Sonnet, ~$5 Opus) but converges on next pass. False-PASS (not possible with current regex — it only checks for PASS, never for FINDINGS) cannot happen.

### Better Way
Have the assessment prompt produce a JSON block (fenced with ````json`) containing `{"verdict": "PASS"|"FINDINGS", "findings": [...]}`. Parse JSON, fall back to current regex. This is a one-template change + ~10 lines of Python.

---

## Fragility 2: Review Verdict Detection — `run_analysis.py:476-487`

**File**: `run_analysis.py:476-487`
**Producer**: Claude (review step)
**Consumer**: `_post` hook → sets `Review-Status` frontmatter on `analysis.md`

### Control Logic
```python
if re.search(r"^VERDICT:\s*PROCEED", r.output_text, re.MULTILINE):
    review_status = "proceed"
elif re.search(r"^VERDICT:\s*REVISE", r.output_text, re.MULTILINE):
    review_status = "revise"
else:
    # Legacy fallback
    if re.search(r"\*\*Overall:\*\*\s*CLEAN", r.output_text, re.MULTILINE):
        review_status = "clean"
    else:
        review_status = "has-actions"
```

### Failure Modes
| Scenario | LLM writes | Pipeline does |
|----------|-----------|---------------|
| Normal PROCEED | `VERDICT: PROCEED` | Sets `proceed` |
| Normal REVISE | `VERDICT: REVISE` | Sets `revise` |
| Typo / missing | Neither pattern | Falls through to legacy → **`has-actions`** |
| Legacy format | `**Overall:** CLEAN` | Sets `clean` |
| Both present | `VERDICT: PROCEED` ... `VERDICT: REVISE` | First match wins → `proceed` |

### Consequences
Medium severity. If `has-actions` is set when it should be `proceed` or `revise`:
- `synthesize` command **rejects** the concept (it requires `Review-Status` in `{addressed, clean, proceed}`)
- `stage1-all --resume` does **not** detect it as a review kickback (it checks for `revise`)
- The concept is stuck until a human manually fixes the frontmatter

### Better Way
Same as Fragility 1: structured JSON verdict block in review output. Or: add a warning when the else branch fires ("WARNING: could not detect PROCEED/REVISE verdict — defaulting to has-actions").

---

## Fragility 3: Review Feedback Extraction — `_get_review_feedback()`

**File**: `lib/loop.py:704-737`
**Producer**: Claude (review step)
**Consumer**: Loop's feedback-producer selection (review kickback path)

### Control Logic
```python
# 1. Find VERDICT: REVISE
verdict_match = re.search(r"^VERDICT:\s*REVISE", text, re.MULTILINE)
# 2. Find ## Corrective Actions section after it
ca_match = re.search(r"^## Corrective Actions.*$", text[verdict_match.end():], re.MULTILINE)
# 3. Extract text until next ## header
next_section = re.search(r"^## ", text[ca_start:], re.MULTILINE)
# 4. Reformat as VERDICT: FINDINGS
return f"VERDICT: FINDINGS\n\n{ca_text.strip()}\n"
```

### Failure Modes
| Scenario | Review.md contains | Result |
|----------|-------------------|--------|
| Normal | `VERDICT: REVISE` + `## Corrective Actions` + `### F-N:` blocks | Extracts correctly |
| Heading variant | `## Corrective actions` (lowercase) | **No match** → returns None |
| Missing section | `VERDICT: REVISE` but findings inline, no `## Corrective Actions` | Returns None |
| Empty section | `## Corrective Actions\n\n## Next Section` | Empty text → returns None |

### Consequences
High severity when it fails. The loop detects `Review-Status: revise` (Fragility 6 below) and calls `_get_review_feedback()`. If it returns None, the loop **silently falls through** to the normal assess feedback path instead of using the review's corrective actions. The human thought the review would be consumed; it was silently discarded.

### Better Way
1. Have the review prompt put its corrective actions in a parseable block (JSON or a fenced section with a machine-readable delimiter).
2. Add a loud WARNING when `_has_revise_status()` is True but `_get_review_feedback()` returns None — this is always a bug.
3. Consider failing hard instead of falling through silently.

---

## Fragility 4: Finding Category Routing — `_extract_model_findings()`

**File**: `lib/loop.py:249-271`
**Producer**: Claude (assessment step)
**Consumer**: Model-setup step (receives only model-targeted findings)

### Control Logic
```python
cat_match = re.search(
    r"^\-\s+\**Category\**:?\s*(analysis|model)",
    block, re.MULTILINE,
)
if cat_match and cat_match.group(1) == "model":
    model_findings.append(block.strip())
```

### Failure Modes
| Scenario | LLM writes | Result |
|----------|-----------|--------|
| Normal | `- **Category:** model` | Match, routed to model step |
| No bold | `- Category: model` | Match (regex handles `\**`) |
| Extra bold | `- ***Category:*** model` | No match (`\**` = 0-or-more `*`, but 3 `*` then `C` works... actually `\**` means zero-or-more `*` so `***Category***` would match `*` consuming first two, then `Category` matches) — this actually works |
| Typo | `- **Categroy:** model` | No match → **finding silently dropped** (defaults to analysis) |
| Different label | `- **Type:** model` | No match → finding silently dropped |
| Missing field | No Category line at all | No match → defaults to analysis (documented behavior) |

### Consequences
Medium. If a model-targeted finding is miscategorized as analysis, the model-setup step won't see it. The analysis step will see it but can't fix model code. The finding persists across iterations until assess re-identifies it.

### Better Way
The feedback format spec (`config/feedback_format.md`) already mandates `Category: analysis | model`. Enforce this at parsing time: if a finding has no recognizable Category, log a warning. Consider JSON output for findings.

---

## Fragility 5: Proposed Actions Parsing — `parse_proposed_actions()`

**File**: `lib/sources.py:164-214`
**Producer**: Claude (review step)
**Consumer**: `address-review` command

### Control Logic
```python
# Header: ### PA-N: description
pa_pattern = re.compile(r"^### (PA-\d+):\s*(.+)$", re.MULTILINE)
# Fields: - **Key:** Value
field_pattern = re.compile(rf"^\-\s*\*\*{re.escape(field_key)}:\*\*\s*(.+)$", re.MULTILINE)
# Placeholder detection
if val.startswith("_[") and val.endswith("]_"):
    val = ""  # unfilled placeholder
```

### Failure Modes
| Scenario | LLM writes | Result |
|----------|-----------|--------|
| Normal | `### PA-1: Fix cost table` + `- **Category:** minor` | Parsed correctly |
| Numbered differently | `### PA-01:` | No match (regex expects `PA-\d+` but `PA-01` matches fine — `\d+` matches `01`) — actually works |
| Bold variant | `- __Category:__ minor` | No match (`__` not `**`) |
| No dash prefix | `**Category:** minor` | No match (requires leading `- `) |
| Multiline value | `- **Finding:** This is a long\nfinding that wraps` | Only captures first line |
| Different header level | `#### PA-1:` or `## PA-1:` | No match |

### Consequences
Medium. If address-review can't parse the PA-N blocks, it has no actions to apply. The command likely produces a minimal or no-op result. The human would need to re-run review or manually apply changes.

### Better Way
Same pattern: JSON output for machine-consumed review actions. Or: a more tolerant parser that warns on unparseable blocks.

---

## Fragility 6: Frontmatter String Conventions

**File**: `lib/state.py:29-51`, `lib/loop.py:696-701`
**Producer**: Pipeline itself (Python code writes these values)
**Consumer**: State detection, loop control flow

### Control Logic
```python
# state.py
fm.get("Status") == "approved"                                    # exact string
fm.get("Review-Status", "") in ("addressed", "clean", "proceed")  # set membership
afm.get("Stale") == "true"                                        # string, not bool

# loop.py
fm.get("Review-Status") == "revise"                               # exact string

# state.py staleness
"# STALE:" in first_line                                          # substring in .py comment
```

### Failure Modes
| Scenario | What happens | Result |
|----------|-------------|--------|
| `Stale: True` (capitalized) | `== "true"` fails | **Staleness not detected** |
| `Review-Status: Revise` (capitalized) | `== "revise"` fails | **Review kickback not triggered** |
| `# STALE: reason` followed by another `#` | Works (substring match) | OK |
| Frontmatter parser returns `True` (bool) | `== "true"` fails | **Staleness not detected** |

### Consequences
Low-medium. These values are written by the pipeline's own `update_frontmatter_field()`, which always writes the exact lowercase strings. The risk is that a human manually edits a frontmatter field with different casing, or the frontmatter parser is changed to return booleans for `true`/`false` strings.

### Better Way
- Use `str(val).lower() == "true"` instead of `val == "true"` for boolean-like fields
- Define constants for status values: `REVIEW_REVISE = "revise"`, `STATUS_APPROVED = "approved"`, etc.
- Consider using the YAML parser for frontmatter (which would return `True` not `"true"` for bare `true` — making this worse, not better, unless you change the comparisons)

---

## Fragility 7: Model Output Validation — `run_model()`

**File**: `lib/claude.py:69`
**Producer**: LLM-generated `model_setup.py` (Python script)
**Consumer**: Loop's model-success decision

### Control Logic
```python
if "lcoe" not in stdout.lower():
    return False, "model output missing LCOE — may be incomplete or broken"
```

And the display extraction in `loop.py`:
```python
lcoe_match = re.search(r"LCOE:\s*([\d.]+)\s*\$/MWh", msg)
```

### Failure Modes
| Scenario | Script prints | Result |
|----------|-------------|--------|
| Normal | `LCOE: 45.2 $/MWh` | Validated, extracted |
| Different format | `LCOE = 45.2 $/MWh` | Validation passes (`"lcoe" in` succeeds), extraction fails (no `: `) |
| Different unit | `LCOE: 45.2 mills/kWh` | Validation passes, extraction fails |
| Error message | `Error calculating LCOE...` | **Validation passes** (word "lcoe" present) |
| Multiple values | `Baseline LCOE: 45.2 $/MWh\nOptimistic LCOE: 30.1 $/MWh` | Validation passes, extraction gets first match |

### Consequences
Low. The validation is a sanity check, not a gate. Even if it passes with an error message, the model output is still saved and human-visible. The LCOE display extraction is cosmetic (used for status printing only).

### Better Way
The model scripts are LLM-generated and there's already a template/exemplar that specifies the output format. A more robust check would be:
- Parse the output as structured key-value pairs
- Validate LCOE is a positive number
- Validate units match expectations

But this is low-priority since the model output is always human-reviewed.

---

## Cross-Cutting Observation: The Fragility Chain

The most dangerous pattern is not any single fragility but the chain:

```
                        Tier 1 (LLM output)                    Tier 2 (pipeline conventions)
                        ─────────────────                      ──────────────────────────────
review.md produced by   →  VERDICT: REVISE detected by regex  →  Review-Status: revise written
Claude (Fragility 2)       (Fragility 2)                         to frontmatter (Fragility 6)
                                                                       ↓
                                                               _has_revise_status() reads it
                                                                       ↓
                                                               _get_review_feedback() extracts
                                                               "## Corrective Actions" by regex
                                                               (Fragility 3)
                                                                       ↓
                                                               Reformatted as "VERDICT: FINDINGS"
                                                                       ↓
                                                               parse_verdict_from_feedback()
                                                               reads it by regex (Fragility 1)
                                                                       ↓
                                                               Loop continues or exits
```

A single formatting variation at the top of this chain (review.md) propagates through 4 fragility zones. The chain is resilient to total failure (returns None / falls through) but not to *partial* failure (e.g., VERDICT detected but Corrective Actions section not found → review consumed as kickback but with no feedback content).

---

## Recommendations Summary

| Priority | Recommendation | Effort | Impact |
|----------|---------------|--------|--------|
| **P0** | Add WARNING when `_has_revise_status()=True` but `_get_review_feedback()` returns None | 5 min | Prevents silent discard of review feedback |
| **P0** | Add WARNING when review verdict detection falls through to `has-actions` | 5 min | Makes mis-detection visible |
| **P1** | Define string constants for all status/verdict values | 30 min | Eliminates typo risk across all comparisons |
| **P1** | Add structured JSON verdict block to feedback_format.md + assessment prompt | 1-2 hr | Eliminates Fragility 1 (verdict parsing) |
| **P2** | Add structured JSON verdict to review prompt | 1-2 hr | Eliminates Fragility 2 + 3 |
| **P2** | Add structured JSON for PA-N actions in review | 2-3 hr | Eliminates Fragility 5 |
| **P3** | Migrate all verdict/finding parsing to JSON-first with regex fallback | 4-6 hr | Systematic fix for all Tier 1 fragilities |

The P0 items are defensive warnings that make failures visible without changing any contracts. The P1-P3 items progressively move toward structured output where machine-consumed data is produced in machine-parseable format.
