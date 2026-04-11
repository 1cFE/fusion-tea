# Spec: Concept Analysis Enhancement Pipeline

**Status:** Draft
**Owner:** Reid W
**Created:** 2026-03-22
**Complexity:** HIGH
**Branch:** design-space-explore
**Parent:** `.project/active/automated-concept-analysis/` (extends existing pipeline)

---

## Business Goals

### Why This Matters

The automated concept analysis pipeline (Phases 1-5, now complete) produces comprehensive, well-sourced D1+ analyses — but holdout testing against handwritten expert analyses (holdout-report-08.md) revealed three systematic gaps:

1. **Claims are cited but not directly verifiable** — inline `[source.md]` tags require a reader to open the source and search for the claim. No direct quotes, no section-level references, no way to spot-check without significant effort.
2. **No cost model output** — the analysis inventories LCOE parameters but never synthesizes them into a runnable model. The handwritten expert analyses include actual 1costingfe model runs (e.g., 4 cents/kWh for Helion FRC) that the automated pipeline cannot match.
3. **No synthesis or editorial judgment** — the analysis documents but does not judge. The handwritten analyses contain verdicts ("I'm not convinced the fusion works"), sensitivity insights (4 → 20 cents/kWh if coil assumptions change), and priority rankings that are more useful for decision-making than the automated output.

A secondary gap: no systematic quality gate exists between "drafted" and "approved." Currently, approval is a human eyeball check with no structured verification.

### Success Criteria

- [ ] Analysis citations are directly verifiable: a reader can trace any claim to a specific quote or section in a source document without opening additional files
- [ ] Each concept analysis includes a runnable 1costingfe model setup with traceable parameter assumptions
- [ ] A structured review process catches factual errors, citation gaps, and model bugs before approval
- [ ] The review process supports iterative human-in-the-loop decision-making
- [ ] A synthesis section provides editorial judgment, sensitivity insights, and decision support — cleanly separated from the objective analysis
- [ ] The pipeline ordering enforces: model-setup → review → synthesis (synthesis uses model output; review catches errors before synthesis runs)

### Priority

High — this is the quality gate between "batch-produced analyses" and "analyses trustworthy enough to inform cost modeling decisions." Without this, the 29 remaining concept analyses are reference documents only, not decision-support tools.

---

## Problem Statement

### Current State

The pipeline produces `analysis.md` files with:
- 8-section D1+ structure following the output template
- Inline citations like `[helion-website-technology.md]` — file-level, not section/quote-level
- 25+ row parameter tables with Source and Confidence columns
- No modeled LCOE output
- No synthesis, verdicts, or editorial judgment
- No structured review step between "draft" and "approved"

State progression: `not-started → gap-checked → drafted → approved`

### Desired Outcome

Three new pipeline stages between "drafted" and "approved":

```
gap-check → analyze → model-setup → review (iterative) → synthesize → approved
```

Each produces a distinct artifact. The review stage is iterative with the user in the loop.

---

## Scope

### In Scope

1. **Citation traceability upgrade** — improve the analysis prompt to produce directly verifiable citations (direct quotes, section references, derivation chains)
2. **Model setup stage** — new `model-setup` command producing a 1costingfe Python script per concept
3. **Review stage** — new `review` command producing a structured review report with proposed actions; new `address-review` command to apply user decisions; supports multiple iterations
4. **Synthesis stage** — new `synthesize` command producing editorial judgment, sensitivity insights, and decision support

### Out of Scope

- Modifying existing approved analyses (01, 07, 21) — enhancements apply to future analyses only
- Running 1costingfe models automatically (the script is produced; the user runs it)
- Automated re-analysis if review finds issues (user decides whether to re-run `analyze --force` or just fix manually)
- Changes to the gap-check stage
- Batch orchestration of the full enhanced pipeline (individual commands first; composite command deferred)

### Edge Cases & Considerations

- Some concepts may not map cleanly to any 1costingfe ConfinementConcept. The model-setup pass MUST flag this rather than force-fitting.
- Some concepts have very thin data (Limited/Opaque rating). The model-setup pass should produce a script with clearly marked speculative assumptions rather than skipping entirely.
- The review loop must handle the case where the user wants to re-run the analysis (not just patch it) — the review report should support a "re-analyze" action type.
- Synthesis must not run on un-reviewed analyses. The pipeline should enforce ordering.

---

## Requirements

### FR-1: Citation Traceability (Analysis Prompt Upgrade)

The analysis prompt template (`prompt_templates/analysis.md`) and output template (`prompt_templates/output_template.md`) MUST be updated to require:

1. **Direct quotes** for key factual claims: `> "quoted text" — source_file.md, §Section Name`
2. **Section-level references** in parameter tables: Source column entries MUST include the section or heading within the source document, not just the filename (e.g., `docslib-helion-arpa-e-presentation.md, §Plasma Parameters` instead of `[docslib-helion-arpa-e-presentation.md]`)
3. **Derivation chains** for inferred values: `[inferred: 50 MJ × $5/J = $250M; 50 MJ from helion-website.md §Polaris Specs; $5/J from 07-maglif analysis §Capacitor Costs]`
4. **Footnote-style references** for claims in prose: numbered footnotes `[1]` with a footnote block at the end of each section, each footnote containing the source path, section, and optionally a direct quote

The analysis body SHOULD use footnote-style references for prose and section-level references in tables. Direct quotes SHOULD be used for the most critical or surprising claims (those a reader would most want to verify). Not every sentence needs a direct quote — the goal is verifiability, not verbosity.

### FR-2: Model Setup Stage

A new `model-setup` subcommand MUST:

1. Accept concept IDs (same resolution as `analyze`)
2. Read the concept's `analysis.md` — specifically the Section 5 parameter tables and Section 2 challenges
3. Read 1costingfe reference materials:
   - The closest existing example from `/home/reid/1cfe/1costingfe/examples/` (e.g., `dhe3_pulsed_frc.py` for FRC concepts, `dt_tokamak.py` for tokamaks)
   - The concept-appropriate YAML defaults from `/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/`
   - The README at `/home/reid/1cfe/1costingfe/README.md`
4. Produce a prompt and invoke Claude to generate `model_setup.py`
5. Save the prompt to `model_setup_prompt.md` and the output to `model_setup.py`

The generated `model_setup.py` MUST:

- Be a self-contained, runnable Python script following the pattern of existing 1costingfe examples
- Include a docstring explaining the modeling approach, what ConfinementConcept is used as the base, and what cost_overrides are applied and why
- Have inline comments tracing every parameter and cost override back to the analysis (e.g., `# eta_th=0.90 — direct EM recovery; analysis.md §Section 2, Challenge 4`)
- Flag speculative or uncertain assumptions with `# UNCERTAIN:` prefix comments
- Include sensitivity analysis via `model.sensitivity()`
- Print results in the standard 1costingfe tabular format (LCOE, CAS breakdown, CAS22 detail, sensitivity)
- Include a "Key Assumptions" summary section in the output matching the pattern in `dhe3_pulsed_frc.py`

The model-setup pass SHOULD select the closest ConfinementConcept and explain the mapping rationale. If no concept maps well, it MUST document why and what approximations are being made.

The model-setup prompt MUST include anti-hallucination instructions: cost overrides must be justified from the analysis, not invented. Unknown costs should use the framework defaults with a comment noting the default is unvalidated for this concept.

### FR-3: Review Stage

#### FR-3a: Review Command

A new `review` subcommand MUST:

1. Accept concept IDs
2. Read the concept's `analysis.md` AND `model_setup.py` (if it exists)
3. Read all source documents for the concept (same source discovery as `analyze`)
4. Produce a prompt and invoke Claude to generate `review.md`
5. Save the prompt to `review_prompt.md`

The generated `review.md` MUST contain:

**Header section:**
- Review iteration number (1, 2, 3...)
- Date
- Files reviewed (analysis.md, model_setup.py, source list)

**Findings section**, organized by category:
- **Citation Verification**: For each direct quote in the analysis, verify it appears in the cited source. Report: quote, cited source, FOUND/NOT FOUND, and the actual text if different.
- **Calculation Verification**: For each derived/inferred value, re-derive it and report: claimed result, re-derived result, MATCH/MISMATCH, derivation shown.
- **Model Setup Review** (if model_setup.py exists): Check that each parameter and cost override traces to a value in analysis.md. Flag any parameters that appear invented or unjustified. Check for obvious bugs (wrong units, wrong ConfinementConcept, impossible values).
- **Consistency Check**: Cross-check between sections — do Section 5 parameters match Section 2 narrative? Do Section 3 TRL ratings align with the challenges described?
- **Factual Concerns**: Any claims that appear unsupported or potentially hallucinated.

**Proposed Actions section**, formatted as a structured list:

```markdown
### Proposed Actions

#### PA-1: [Short description]
- **Category:** citation-error | calculation-error | model-bug | inconsistency | factual-concern | improvement
- **Severity:** blocking | important | minor
- **Location:** analysis.md §Section N / model_setup.py line N
- **Finding:** [What the review found]
- **Proposed Fix:** [What should change]
- **Decision:** _[USER FILLS IN: agree | reject | alternative]_
- **User Notes:** _[USER FILLS IN: free text]_

#### PA-2: ...
```

The `Decision` and `User Notes` fields MUST be left blank (with the italic placeholder text) for the user to fill in. The user reads the review, fills in their decisions, and saves the file.

#### FR-3b: Address-Review Command

A new `address-review` subcommand MUST:

1. Accept concept IDs
2. Read the concept's `review.md` — parse the Proposed Actions to find user decisions
3. For each action where `Decision:` is filled in:
   - `agree` → apply the proposed fix (edit analysis.md and/or model_setup.py)
   - `reject` → skip (log that it was rejected)
   - `alternative` → read `User Notes` for the alternative action and apply it
4. Produce an updated `analysis.md` and/or `model_setup.py`
5. Log all changes made to an `address_log.md` (append-only, one section per iteration)
6. Save the prompt to `address_review_prompt.md`

After addressing, the user MAY run `review` again to verify the fixes. The review iteration number increments. This loop continues until the user is satisfied.

#### FR-3c: Review State Tracking

The review state MUST be tracked in the analysis.md frontmatter:

```yaml
Review-Iterations: 2
Last-Review: 2026-03-22
Review-Status: clean | has-actions | addressed
```

- `has-actions`: review.md exists with unaddressed proposed actions
- `addressed`: all proposed actions have been addressed
- `clean`: most recent review found no blocking or important issues

### FR-4: Synthesis Stage

A new `synthesize` subcommand MUST:

1. Accept concept IDs
2. MUST refuse to run if the concept has not been reviewed (Review-Status not `addressed` or `clean`). Print an error directing the user to run `review` first.
3. Read the concept's `analysis.md`, `model_setup.py`, and model output (if the user has run the model and saved output)
4. Read approved prior syntheses for cross-concept perspective
5. Produce a prompt and invoke Claude to generate `synthesis.md`
6. Save the prompt to `synthesis_prompt.md`

The generated `synthesis.md` MUST contain:

1. **Executive Summary** (3-5 bullets): The single most important risk, the single most important advantage, the LCOE ballpark from the model, and a confidence-level verdict.

2. **What Matters Most for LCOE**: Rank the top 3-5 parameters by LCOE sensitivity. For each, state the assumed value, the sensitivity magnitude (from model output if available), and what would change the answer. Use language like "If X changes by Y%, LCOE moves by Z%."

3. **Risk Verdicts**: For each major challenge from Section 2 of the analysis, render a judgment:
   - "Likely resolvable" / "Unlikely resolvable" / "Genuinely uncertain"
   - One-sentence rationale
   - What evidence would retire the risk

4. **Structural Advantages and Disadvantages**: Compare this concept's cost structure against the conventional D-T tokamak baseline. Quantify where possible (e.g., "eliminates ~20% of direct capital by removing the tritium breeding blanket").

5. **Cross-Concept Positioning**: Where does this concept sit in the landscape? What other concepts share similar risks or advantages? What makes this concept's economics fundamentally different?

6. **Modeling Confidence**: Rate the overall modeling confidence (High/Medium/Low) with a 2-3 sentence justification. Note which parameter assumptions are anchored to data vs. speculative.

7. **What Would Change My Mind**: List 2-3 future developments or data releases that would materially improve or degrade the LCOE estimate.

The synthesis MUST use model output numbers (LCOE, CAS breakdown, sensitivity elasticities) in its conclusions. It SHOULD NOT simply restate the analysis — it should interpret, judge, and prioritize.

The synthesis SHOULD adopt an editorial voice: clear opinions, direct language, no excessive hedging. The objectivity of the underlying analysis is preserved by keeping synthesis in a separate artifact.

### FR-5: Pipeline Ordering and State Management

The state machine MUST enforce this ordering:

```
not-started → gap-checked → drafted → model-setup → reviewed → synthesized → approved
```

- `model-setup` MUST refuse to run on concepts without `analysis.md` (state < drafted)
- `review` MUST refuse to run on concepts without `analysis.md` (state < drafted). It SHOULD warn but proceed if `model_setup.py` does not exist (review the analysis alone).
- `synthesize` MUST refuse to run on concepts with Review-Status not in {`addressed`, `clean`}
- `approve` SHOULD refuse to run on concepts without `synthesis.md` (state < synthesized). MAY be overridden with `--force` for cases where synthesis is intentionally skipped.

State detection (`get_concept_state()`) MUST be updated to recognize the new states based on file existence and frontmatter fields.

The `status` subcommand MUST display the new states with appropriate symbols.

### FR-6: Script and CLI Changes

New subcommands added to `run_analysis.py`:

| Subcommand | Arguments | Description |
|------------|-----------|-------------|
| `model-setup` | `<concepts> [--dry-run] [--model] [--force] [--timeout]` | Generate 1costingfe model setup script |
| `review` | `<concepts> [--dry-run] [--model] [--force] [--timeout]` | Generate structured review report |
| `address-review` | `<concepts> [--dry-run] [--model] [--timeout]` | Apply user decisions from review report |
| `synthesize` | `<concepts> [--dry-run] [--model] [--force] [--timeout]` | Generate editorial synthesis |

All new subcommands MUST support `--dry-run` (save prompt only) and `--model` (default: sonnet).

New prompt templates:

| Template | Purpose |
|----------|---------|
| `prompt_templates/model_setup.md` | Instructions for generating 1costingfe script |
| `prompt_templates/review.md` | Instructions for structured review with proposed actions |
| `prompt_templates/address_review.md` | Instructions for applying user decisions |
| `prompt_templates/synthesis.md` | Instructions for editorial synthesis |

### FR-7: Output Structure

Each concept's analysis directory MUST support this full file set:

```
analyses/{concept-id}/
├── gap_check_prompt.md       # (existing)
├── gap_report.md             # (existing)
├── analysis_prompt.md        # (existing)
├── analysis.md               # (existing, with improved citations per FR-1)
├── model_setup_prompt.md     # NEW
├── model_setup.py            # NEW — runnable 1costingfe script
├── review_prompt.md          # NEW
├── review.md                 # NEW — structured review with proposed actions
├── address_review_prompt.md  # NEW (per iteration)
├── address_log.md            # NEW — append-only log of review iterations
├── synthesis_prompt.md       # NEW
└── synthesis.md              # NEW — editorial judgment and decision support
```

---

## Acceptance Criteria

### Core Functionality

- [ ] `model-setup 08 --dry-run` produces a prompt that references the analysis parameters, 1costingfe examples, and concept YAML defaults
- [ ] `model-setup 08` produces a runnable `model_setup.py` that imports from `costingfe` and prints LCOE results
- [ ] The generated `model_setup.py` has inline comments tracing each parameter to the analysis
- [ ] `review 08 --dry-run` produces a prompt that references the analysis, model setup, and all source documents
- [ ] `review 08` produces a `review.md` with structured Proposed Actions including blank Decision/User Notes fields
- [ ] After the user fills in decisions, `address-review 08` reads and applies them
- [ ] `address-review 08` logs changes to `address_log.md`
- [ ] Running `review 08` again produces iteration 2 with updated findings
- [ ] `synthesize 08` refuses to run if review hasn't been completed
- [ ] `synthesize 08` (after review) produces a `synthesis.md` with executive summary, risk verdicts, and model-backed sensitivity insights
- [ ] `status` displays the new states correctly
- [ ] The updated analysis prompt produces citations with direct quotes and section-level references

### Quality & Integration

- [ ] Existing `analyze`, `gap-check`, and `approve` commands continue to work unchanged
- [ ] The `--dry-run` flag works for all new subcommands
- [ ] State detection correctly identifies all new states
- [ ] Pipeline ordering is enforced (model-setup requires drafted, synthesize requires reviewed)

---

## Related Artifacts

- **Parent work item:** `.project/active/automated-concept-analysis/`
- **Existing design:** `.project/active/automated-concept-analysis/design.md`
- **Existing plan:** `.project/active/automated-concept-analysis/plan.md` (Phases 1-5 complete)
- **Holdout report:** `.project/active/automated-concept-analysis/holdout-report-08.md` (motivating evidence)
- **1costingfe examples:** `/home/reid/1cfe/1costingfe/examples/` (reference for model-setup)
- **1costingfe FRC example:** `/home/reid/1cfe/1costingfe/examples/dhe3_pulsed_frc.py` (closest existing model)
- **Current script:** `exploration/concept_analysis/scripts/run_analysis.py`
- **Current templates:** `exploration/concept_analysis/prompt_templates/`

---

**Next Steps:** After approval, proceed to `/_my_design` for the technical design of each new stage.
