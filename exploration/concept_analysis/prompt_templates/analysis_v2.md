# D1+ Concept Analysis: {{concept_name}}

You are producing a D1+ analysis for the fusion concept **{{concept_name}}** ({{company}}).

## Analysis Goals

{{@config/analysis_goals.md}}

## Quality Standards

{{@config/quality_standards.md}}

---

## Fixed Contract Inputs (orchestrator-supplied — do NOT re-decide)

The upstream tables have already fixed this concept's design point, archetype, and
comparables. They reach you below as rendered blocks. Treat every one as a **read-
only input**: copy it where instructed, extract against it, and build on it — but
never re-choose, re-derive, or edit it.

### Design Point (selection — copy verbatim to the top of the analysis body)

{{design_point_block}}

### Canonical 1costingFE Account Schema (this archetype)

These are the **only** account codes you may use in Override Candidates. Do not
invent codes (no `CAS22.1.3`-style strings). Each row says, in one line, what the
account costs — enough to judge whether the dossier justifies an override.

{{canonical_accounts}}

### Comparables (fixed — for the Section 7 family-delta)

{{comparables_block}}

### Override-Count Rubric (from Archetype-Fit grade)

{{fit_grade_band}}

## Override Candidate Discovery

Before proposing any relative override, read the override-semantics policy below.
It carries the single headline invariant (`account = M × the library's 1 GWe
fleet cost for that account`), the S/U/P cost classes, and the modular-fleet
rationale baseline. The model-setup agent that transcribes your Section 5b reads
the same policy, so your override values and rationales must already be in this
frame.

{{@config/override_semantics.md}}

{{@config/account_walkthrough.md}}

---

## Per-Source Reading Pattern

For each source document you need to read, spawn a **separate subagent** using the
Agent tool. Do NOT read all sources in your main thread — delegate each source to a
subagent for context efficiency.

**Subagent prompt template:**
{{@agents/source_reader.md}}

Construct each subagent call as follows:
- Give the subagent the path to ONE source document
- Provide 3–5 specific questions (see your mode instructions below for what to ask)
- The subagent reads the source and returns answers with section references

After receiving subagent responses, **read the cited sections yourself** to confirm
the subagent's characterization before incorporating claims. Do not blindly trust
subagent summaries for critical claims.

{{#if memory_context}}
## Cross-Concept Memory

The following insights were captured from prior concept analyses. Use them to avoid
known pitfalls and apply established patterns. Do not cite these memories as
sources — they are guidance, not evidence. Verify any specific claims against the
actual source documents.

{{memory_context}}
{{/if}}

{{#if concept_landscape}}
## Concept Landscape

The taxonomy of all fusion concepts under investigation, grouped by pipeline
maturity. The comparables for *this* concept are already fixed (above) — use the
landscape only for context, not to re-select neighbours.

{{concept_landscape}}
{{/if}}

{{#if cold_start}}
## Mode: Cold Start

You are producing a D1+ analysis from scratch. No prior analysis exists for this
concept.

### Required Reading

Read these files in this order before writing:

1. **Output Template** (canonical section structure you must follow): `{{output_template_path}}`
2. **Analysis Brief** (purpose and quality expectations): `{{brief_path}}`
3. **Handwritten Exemplars** (calibrate depth and style): {{exemplar_paths}}
4. **Dossier** (structured research summary — your factual foundation): `{{dossier_path}}`
5. **Extracted Source Documents** (use subagents — see Per-Source Reading Pattern).
   For cold start, ask each subagent:
   - What does this source say about the concept's cost structure and unique subsystems?
   - What LCOE-relevant parameters or performance targets for the **named design point** are stated?
   - What cost advantages or penalties relative to the comparables are discussed?
   - What technical risks, assumptions, or data gaps are mentioned?
   - What materials, supply-chain, or manufacturing considerations are relevant?

   Sources to read via subagents:
   {{source_paths}}
6. **Schema** (controlled vocabulary and column definitions): `{{schema_path}}`

### Content Requirements
- Follow the canonical section structure from the output template exactly:
  the `## Design Point` block at the top, then Sections 1–8 (including Section 5
  "Design Point Parameters" and Section 5b "Override Candidates").
- **Copy the rendered Design Point block verbatim** to the top of the body. Do not
  edit its selection fields.
- Every quantitative value in Section 5 must describe the **named design point at
  native scale** and carry a Source and Confidence entry.
- Section 5b Override Candidates must come from the per-account walkthrough above —
  six-field entries, canonical account codes only.
- Section 7 articulates the family-delta against the fixed Comparables list.
- Values without sources must be flagged `[inferred]`, `[analogue]`, or
  `[estimated]` with reasoning.

### Output

Write the complete analysis **body** to this file using the Write tool:
`{{output_path}}`

Write ONLY the analysis content (the `## Design Point` block followed by Sections
1–8). Do NOT include:
- YAML frontmatter (the pipeline adds it automatically)
- Preamble, commentary, or code fences wrapping the document

Start the file with the `## Design Point` block (copied verbatim) and end after
Section 8.

### Frontmatter is orchestrator-owned — do not edit it

The pipeline pre-populates the analysis frontmatter from the signed-off upstream
tables. The fields `Comparables`, `Confinement-Family`, `Archetype`,
`Archetype-Fit`, `Comparison-Status`, and the four `Design-Point-*` fields are
determined upstream and are **not** analyzer-editable. Do not add, edit, or remove
frontmatter fields — write only the analysis body.
{{/if}}

{{#if feedback_pass}}
## Mode: Feedback Pass

You are improving an existing analysis based on specific feedback from the
assessment agent.

### Existing Analysis
Read this file completely first: `{{analysis_path}}`

### Feedback to Address
Then read the feedback: `{{feedback_path}}`

The feedback contains `### F-N:` findings with a Target, Category, Finding,
Recommendation, and Priority. Address each finding.

Findings marked `Category: model` primarily target the model code
(`model_setup.py` — the `overrides` list, `spec` dict, sweeps). You should still
update analysis prose where it supports the model change (e.g. a Section 5b
override entry or a Section 5 parameter row), but do NOT try to resolve model
findings by narrative rewording alone — the model-setup agent receives them too.

If the feedback contains a "Carried-Forward Assessment Findings" section, treat
those unresolved findings with the same priority as regular findings.

### Preserve the fixed contract
- Do **not** edit the `## Design Point` selection block — its fields are
  orchestrator-fixed. Targeted edits only; do not re-write conforming sections.
- Any Override Candidate you add or change uses a **canonical** account code from
  the schema above and the six-field shape.

### Source Documents (use subagents for targeted evidence)
For each finding, spawn subagents with questions specific to that finding.

Sources available: {{source_paths}}
Dossier (read directly — short and structured): `{{dossier_path}}`

### Instructions
1. Read the existing analysis completely
2. Read the feedback findings
3. For each finding, gather targeted evidence via the per-source subagent pattern
4. Use the Edit tool to make targeted improvements to `{{analysis_path}}`
5. Do NOT rewrite sections the feedback doesn't address; maintain existing citations
6. If a finding asks for parameter rows, add them in the correct table position
   with Source and Confidence columns
7. After editing, re-read the modified sections to verify coherence
{{/if}}

{{#if self_advance}}
## Mode: Self-Advance

You are reviewing and improving an existing analysis on your own initiative. No
external feedback is provided — assess the analysis yourself against the goals.

### Existing Analysis
Read this file completely: `{{analysis_path}}`

### Source Documents (use subagents for targeted evidence)
{{source_paths}}

Dossier: `{{dossier_path}}`

### Instructions
1. Read the existing analysis and the analysis goals above
2. Evaluate against each goal — identify the most significant gaps (design-point
   coherence, override discipline, family-delta concreteness are common ones)
3. Pick the top 3 most impactful improvements
4. Gather targeted evidence via the per-source subagent pattern
5. Use the Edit tool to make targeted improvements to `{{analysis_path}}`
6. Do **not** edit the `## Design Point` selection block. Focus on substance, not
   cosmetics.
{{/if}}

## Output Template Structure

`{{output_template_path}}` defines the canonical sections. The analysis must follow
this structure regardless of mode.

## Comparables and Cross-Concept Context

{{approved_analyses}}

If approved prior analyses are available:
- Read them to keep shared-subsystem assumptions and cost structures consistent —
  cite the source concept when you reuse an assumption.
- Articulate divergences in Section 7 (Family-Delta vs Comparables), measured
  against the fixed Comparables list — not an arbitrary neighbour.
- Do NOT copy text verbatim — synthesize and adapt to this concept's specifics.
