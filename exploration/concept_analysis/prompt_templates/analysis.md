# D1+ Concept Analysis: {{concept_name}}

You are producing a comprehensive qualitative and quantitative concept analysis for the fusion concept **{{concept_name}}** ({{company}}).

## Your Task

Write a complete D1+ analysis following the output template structure. The analysis must synthesize all available data from the Phase 1a dossier and extracted source documents, extract LCOE-relevant parameters, and honestly document data gaps.

## Required Reading

Read these files in this order before writing:

### 1. Output Template (defines the section structure you must follow)
`{{output_template_path}}`

### 2. Analysis Brief (defines the purpose and quality expectations)
`{{brief_path}}`

### 3. Handwritten Exemplars (calibrate your depth and style against these)
{{exemplar_paths}}

Study the exemplars carefully. They show the expected level of technical depth, citation practice, and analytical rigor. Your output should match their quality. Note that exemplars may vary in structure — follow the output template for section structure, but match the exemplars for analytical depth and style.

### 4. Phase 1a Dossier (structured research summary for this concept)
`{{dossier_path}}`

The dossier contains per-column values with confidence ratings, citations, and notes from prior research iterations. This is your factual foundation.

### 5. Extracted Source Documents (primary technical sources)
Read ALL of these — they contain the detailed technical content the dossier was derived from:

{{source_paths}}

### 6. Schema (controlled vocabulary and column definitions)
`{{schema_path}}`

### 7. Approved Prior Analyses (reuse pool — read all of these)
{{approved_analyses}}

## Writing Instructions

### Content Requirements
- Follow the output template section structure exactly (Sections 1-8)
- Start with the YAML frontmatter as specified in the output template
- Every factual claim must cite a specific source (Phase 1a source document, dossier citation, or extracted document)
- Every quantitative value in Section 5 must have a Source and Confidence column entry
- Values without sources must be flagged as `[inferred]`, `[analogue]`, or `[estimated]` with reasoning

### Anti-Hallucination Rules (CRITICAL)
- If data does not exist in the provided sources, say "No data found in available sources"
- Do NOT invent plausible-sounding technical facts, cost figures, or performance numbers
- Do NOT cite papers or sources that don't appear in the Phase 1a materials or dossier unless they are well-known landmark publications you are certain exist
- When a section has thin data, write a shorter section that honestly states what is and isn't known
- Prefer "unknown" over "likely" when evidence is absent

### Cross-Concept Reuse (if approved analyses are available)
- Read all approved prior analyses listed above
- Identify shared subsystems, materials, cost structures, or physics
- Reuse consistent assumptions where appropriate — cite the source concept
- Note divergences in Section 7 (Cross-Concept Notes)
- Do NOT copy text verbatim — synthesize and adapt to this concept's specifics
- Record which concept IDs you referenced in the frontmatter `Reuses` list

### Quality Calibration
- Match the analytical depth of the handwritten exemplars
- TRL assessments should follow the pattern: Demonstrated / On paper only / Missing at scale
- LCOE challenges should be ranked by impact, not listed randomly
- Materials/supply chain should quantify demand vs. supply where possible
- The analysis should be useful to an engineer building an LCOE model — not just a literature review

## Output

Output the complete analysis as a single markdown document. Start with the YAML frontmatter (`---` delimited), then all 8 sections. Do NOT use any tools to write files — just output the full document text directly as your response.
