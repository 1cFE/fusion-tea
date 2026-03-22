# D1+ Concept Analysis: FRC w/ Direct Conversion

You are producing a comprehensive qualitative and quantitative concept analysis for the fusion concept **FRC w/ Direct Conversion** (Helion Energy).

## Your Task

Write a complete D1+ analysis following the output template structure. The analysis must synthesize all available data from the Phase 1a dossier and extracted source documents, extract LCOE-relevant parameters, and honestly document data gaps.

## Required Reading

Read these files in this order before writing:

### 1. Output Template (defines the section structure you must follow)
`/home/reid/1cfe/fusion-tea/exploration/concept_analysis/prompt_templates/output_template.md`

### 2. Analysis Brief (defines the purpose and quality expectations)
`/home/reid/1cfe/fusion-tea/exploration/concept_analysis/concept_analysis_brief.md`

### 3. Handwritten Exemplars (calibrate your depth and style against these)
- `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/handwritten/01-hts-compact-tokamak.md`
- `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/handwritten/07-maglif.md`
- `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/handwritten/08-frc-w-direct-conversion.md`
- `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/handwritten/26-laser-icf-indirect-drive.md`

Study the exemplars carefully. They show the expected level of technical depth, citation practice, and analytical rigor. Your output should match their quality. Note that exemplars may vary in structure — follow the output template for section structure, but match the exemplars for analytical depth and style.

### 4. Phase 1a Dossier (structured research summary for this concept)
`/home/reid/1cfe/fusion-tea/exploration/phase_1a/research/08-frc-w-direct-conversion/dossier.md`

The dossier contains per-column values with confidence ratings, citations, and notes from prior research iterations. This is your factual foundation.

### 5. Extracted Source Documents (primary technical sources)
Read ALL of these — they contain the detailed technical content the dossier was derived from:

- `/home/reid/1cfe/fusion-tea/exploration/phase_1a/research/08-frc-w-direct-conversion/iter-01/sources/contrary-research-helion.md` (1 KB)
- `/home/reid/1cfe/fusion-tea/exploration/phase_1a/research/08-frc-w-direct-conversion/iter-01/sources/docslib-helion-arpa-e-presentation.md` (1 KB)
- `/home/reid/1cfe/fusion-tea/exploration/phase_1a/research/08-frc-w-direct-conversion/iter-01/sources/helion-website-technology.md` (3 KB)
- `/home/reid/1cfe/fusion-tea/exploration/phase_1a/research/08-frc-w-direct-conversion/iter-02/sources/helion-milestones-feb2026.md` (1 KB)
- `/home/reid/1cfe/fusion-tea/exploration/phase_1a/research/08-frc-w-direct-conversion/iter-02/sources/helion-prototype-generations.md` (2 KB)

### 6. Schema (controlled vocabulary and column definitions)
`/home/reid/1cfe/fusion-tea/exploration/phase_1a/schema.md`

### 7. Approved Prior Analyses (reuse pool — read all of these)
- `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/01-hts-compact-tokamak/analysis.md`
- `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/07-maglif/analysis.md`
- `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/21-spherical-tokamak-hts/analysis.md`

## Writing Instructions

### Content Requirements
- Follow the output template section structure exactly (Sections 1-8)
- Do NOT include YAML frontmatter — the pipeline generates it automatically
- Every factual claim must cite a specific source (Phase 1a source document, dossier citation, or extracted document)
- Every quantitative value in Section 5 must have a Source and Confidence column entry
- Values without sources must be flagged as `[inferred]`, `[analogue]`, or `[estimated]` with reasoning

### Citation Format (CRITICAL — read the Citation Format section in the output template)
- **Parameter tables**: The Source column must include `§Section Name` (e.g., `helion-website.md §Polaris Specifications`), not just a bare filename
- **Key claims**: Use direct block quotes (`>`) for the 3–5 most critical claims per section, with exact source filename and section heading
- **Inferred values**: Show the full derivation chain in the Source column (e.g., `[inferred: 50 MJ × $5/J; bank size from source.md §Section; unit cost from ...]`)
- **Prose claims**: Use numbered footnotes `[1]` with a footnote block at the end of each section; each footnote must include source path and section
- The goal is **direct verifiability** — a reader should be able to confirm any claim without opening files and searching

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
- After writing the body, update the Reuses field in the analysis file (see Output section below)

### Quality Calibration
- Match the analytical depth of the handwritten exemplars
- TRL assessments should follow the pattern: Demonstrated / On paper only / Missing at scale
- LCOE challenges should be ranked by impact, not listed randomly
- Materials/supply chain should quantify demand vs. supply where possible
- The analysis should be useful to an engineer building an LCOE model — not just a literature review

## Output

### Step 1: Write the analysis body

Write the complete analysis to this file using the Write tool:
`/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/08-frc-w-direct-conversion/analysis_body.md`

Write ONLY the analysis content (Sections 1-8). Do NOT include:
- YAML frontmatter (the pipeline adds it automatically)
- Preamble or commentary
- Code fences wrapping the document

Start the file with `# D1+ Analysis:` and end after Section 8.

### Step 2: Update Reuses (if applicable)

If you referenced any approved prior analyses, update the Reuses field in:
`/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/08-frc-w-direct-conversion/analysis.md`

The file already contains `Reuses: []`. Use the Edit tool to replace it with the concept IDs you referenced, e.g.:
`Reuses: [21-spherical-tokamak-hts, 28-hts-tokamak-full-hts]`

If you did not reference any approved analyses, leave Reuses unchanged.
