# D1+ Concept Analysis: {{concept_name}}

You are producing a D1+ analysis for the fusion concept **{{concept_name}}** ({{company}}).

## Analysis Goals

{{@config/analysis_goals.md}}

## Quality Standards

{{@config/quality_standards.md}}

## Per-Source Reading Pattern

For each source document you need to read, spawn a **separate subagent** using the Agent tool. Do NOT read all sources in your main thread — delegate each source to a subagent for context efficiency.

Each subagent call should follow this pattern:

**Subagent prompt template:**
{{@agents/source_reader.md}}

Construct each subagent call as follows:
- Give the subagent the path to ONE source document
- Provide 3-5 specific questions (see your mode instructions below for what to ask)
- The subagent reads the source and returns answers with section references

After receiving subagent responses, **read the cited sections yourself** to confirm the subagent's characterization before incorporating claims into the analysis. Do not blindly trust subagent summaries for critical claims.

{{#if memory_context}}
## Cross-Concept Memory

The following insights were captured from prior concept analyses. Use them
to avoid known pitfalls and apply established patterns. Do not cite these
memories as sources — they are guidance, not evidence. Verify any specific
claims against the actual source documents.

{{memory_context}}
{{/if}}

{{#if concept_landscape}}
## Concept Landscape

The complete taxonomy of all fusion concepts under investigation, grouped by
pipeline maturity. Use this to identify nearest-neighbor concepts for positioning
(Goal 1). Approved concepts have full analyses available for deep reading.
In-progress concepts (I{N}) have N iterations completed.

{{concept_landscape}}
{{/if}}

{{#if cold_start}}
## Mode: Cold Start

You are producing a D1+ analysis from scratch. No prior analysis exists for this concept.

### Required Reading

Read these files in this order before writing:

#### 1. Output Template (defines the section structure you must follow)
`{{output_template_path}}`

#### 2. Analysis Brief (defines the purpose and quality expectations)
`{{brief_path}}`

#### 3. Handwritten Exemplars (calibrate your depth and style against these)
{{exemplar_paths}}

Study the exemplars carefully. They show the expected level of technical depth, citation practice, and analytical rigor. Your output should match their quality. Note that exemplars may vary in structure — follow the output template for section structure, but match the exemplars for analytical depth and style.

#### 4. Phase 1a Dossier (structured research summary for this concept)
`{{dossier_path}}`

The dossier contains per-column values with confidence ratings, citations, and notes from prior research iterations. This is your factual foundation.

#### 5. Extracted Source Documents (use subagents — see Per-Source Reading Pattern above)

Spawn one subagent per source document. For cold-start analysis, ask each subagent:
- What does this source tell us about the concept's cost structure and unique subsystems?
- What LCOE-relevant parameters or performance targets are stated?
- What cost advantages or penalties relative to conventional approaches are discussed?
- What technical risks, assumptions, or data gaps are mentioned?
- What materials, supply chain, or manufacturing considerations are relevant?

Sources to read via subagents:
{{source_paths}}

#### 6. Schema (controlled vocabulary and column definitions)
`{{schema_path}}`

### Content Requirements
- Follow the output template section structure exactly (Sections 1-8)
- Do NOT include YAML frontmatter — the pipeline generates it automatically
- Every factual claim must cite a specific source (Phase 1a source document, dossier citation, or extracted document)
- Every quantitative value in Section 5 must have a Source and Confidence column entry
- Values without sources must be flagged as `[inferred]`, `[analogue]`, or `[estimated]` with reasoning

### Output

#### Step 1: Write the analysis body

Write the complete analysis to this file using the Write tool:
`{{output_path}}`

Write ONLY the analysis content (Sections 1-8). Do NOT include:
- YAML frontmatter (the pipeline adds it automatically)
- Preamble or commentary
- Code fences wrapping the document

Start the file with `# D1+ Analysis:` and end after Section 8.

#### Frontmatter is orchestrator-owned — do not edit it

The pipeline pre-populates the analysis frontmatter from the signed-off upstream
tables. The fields `Comparables`, `Confinement-Family`, `Archetype`,
`Archetype-Fit`, `Comparison-Status`, and the four `Design-Point-*` fields
(`Design-Point-Name`, `Design-Point-Maturity`, `P-Native`, `Grounding-Confidence`)
are determined upstream and are **not** analyzer-editable. Do not add, edit, or
remove frontmatter fields — write only the analysis body (Step 1).
{{/if}}

{{#if feedback_pass}}
## Mode: Feedback Pass

You are improving an existing analysis based on specific feedback from the assessment agent.

### Existing Analysis
Read this file completely first:
`{{analysis_path}}`

### Feedback to Address
Then read the feedback:
`{{feedback_path}}`

The feedback contains specific findings (F-1, F-2, etc.) with targets, findings, and recommendations. Address each finding.

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

### Source Documents (use subagents for targeted evidence gathering)

For each finding in the feedback, spawn subagents to gather targeted evidence from the relevant sources. Ask questions specific to the feedback — e.g., if the feedback says "missing cost implication for direct energy conversion", ask subagents: "Does this source contain evidence about direct energy conversion costs, BOP impact, or conversion efficiency?"

Sources available for subagent queries:
{{source_paths}}

Dossier (read directly — it's structured and short):
`{{dossier_path}}`

### Instructions
1. Read the existing analysis completely
2. Read the feedback — it contains specific findings to address
3. For each finding, use the per-source subagent pattern to gather targeted evidence from the sources
4. Use the Edit tool to make targeted improvements to `{{analysis_path}}`
5. Do NOT rewrite sections that aren't addressed by the feedback
6. Maintain all existing citations — only add/modify what the feedback requires
7. If a finding recommends adding parameter rows, add them in the correct table position with Source and Confidence columns
8. After making edits, re-read the modified sections to verify coherence
{{/if}}

{{#if self_advance}}
## Mode: Self-Advance

You are reviewing and improving an existing analysis on your own initiative. No external feedback is provided — assess the analysis yourself against the goals above.

### Existing Analysis
Read this file completely:
`{{analysis_path}}`

### Source Documents (use subagents for targeted evidence)
{{source_paths}}

Dossier:
`{{dossier_path}}`

### Instructions
1. Read the existing analysis and the analysis goals above
2. Evaluate the analysis against each goal — identify the most significant gaps
3. Pick the top 3 most impactful improvements
4. Use the per-source subagent pattern to gather targeted evidence for those improvements
5. Use the Edit tool to make targeted improvements to `{{analysis_path}}`
6. Focus on substance — do not make cosmetic changes
{{/if}}

## Output Template Structure

`{{output_template_path}}` defines the 8 required sections. The analysis must follow this structure regardless of mode.

## Cross-Concept Reuse

{{approved_analyses}}

If approved prior analyses are available:
- Read all approved prior analyses listed above
- Identify shared subsystems, materials, cost structures, or physics
- Reuse consistent assumptions where appropriate — cite the source concept
- Note divergences in Section 7 (Cross-Concept Notes)
- Do NOT copy text verbatim — synthesize and adapt to this concept's specifics
