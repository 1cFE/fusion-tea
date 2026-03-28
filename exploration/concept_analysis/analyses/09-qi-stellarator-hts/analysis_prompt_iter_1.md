# D1+ Concept Analysis: QI Stellarator - HTS

You are producing a D1+ analysis for the fusion concept **QI Stellarator - HTS** (Proxima Fusion).

## Analysis Goals

# Analysis Goals

These are the objectives the analysis agent works toward. Every section of the
analysis should contribute to answering these questions.

1. **Concept Positioning**: How does this concept relate to and compare with
   other fusion approaches? What family does it belong to, and what are the
   nearest neighbors?

2. **Key Differentiators**: What are the key differences from the mainstream
   approach (conventional tokamak)? What is novel, what is borrowed, what is
   shared?

3. **TEA Implications**: How do those differences affect techno-economic
   analysis? Which differences create cost advantages, which create cost
   penalties, and which are cost-neutral?

4. **Modeling Approach**: What is the right way to model those differences?
   What are the key hypotheses that the cost model should test? What parameters
   have the most leverage?

5. **Risks and Assumptions**: Are the key risks and assumptions called out?
   How do we capture them in the TEA — as sensitivity parameters, scenario
   branches, or explicit flags?


## Quality Standards

# Quality Standards

## Citation Standards
Follow the Citation Format section in the output template exactly. Key rules:
- Parameter table Source column: `filename.md §Section Heading` (not bare filenames)
- 3-5 direct block quotes per section for critical claims
- Derivation chains for all [inferred] values
- Footnote-style references in prose with source path and section

## Anti-Hallucination Rules
- If data does not exist in the provided sources, say "No data found in
  available sources"
- Do NOT invent plausible-sounding technical facts, cost figures, or
  performance numbers
- Do NOT cite papers or sources not in the provided materials unless they
  are well-known landmark publications you are certain exist
- When a section has thin data, write a shorter section that honestly states
  what is and isn't known
- Prefer "unknown" over "likely" when evidence is absent

## Depth Expectations
- Match the analytical depth of the handwritten exemplars
- TRL assessments: Demonstrated / On paper only / Missing at scale
- LCOE challenges ranked by impact, not listed randomly
- Materials/supply chain: quantify demand vs. supply where possible
- The analysis should be useful to an engineer building an LCOE model


## Per-Source Reading Pattern

For each source document you need to read, spawn a **separate subagent** using the Agent tool. Do NOT read all sources in your main thread — delegate each source to a subagent for context efficiency.

Each subagent call should follow this pattern:

**Subagent prompt template:**
# Source Reader

Read the source document and answer the provided questions.

## Instructions
1. Read the entire source document
2. For each question, provide a focused answer with:
   - The relevant information from the source
   - The section heading or location where you found it (e.g., §Results, §Table 3)
   - Direct quotes for the most important claims
3. If the source does not contain information relevant to a question,
   say "Not addressed in this source"
4. Keep answers concise — focus on facts and data, not interpretation


Construct each subagent call as follows:
- Give the subagent the path to ONE source document
- Provide 3-5 specific questions (see your mode instructions below for what to ask)
- The subagent reads the source and returns answers with section references

After receiving subagent responses, **read the cited sections yourself** to confirm the subagent's characterization before incorporating claims into the analysis. Do not blindly trust subagent summaries for critical claims.


## Mode: Cold Start

You are producing a D1+ analysis from scratch. No prior analysis exists for this concept.

### Required Reading

Read these files in this order before writing:

#### 1. Output Template (defines the section structure you must follow)
`/home/reid/1cfe/fusion-tea/exploration/concept_analysis/prompt_templates/output_template.md`

#### 2. Analysis Brief (defines the purpose and quality expectations)
`/home/reid/1cfe/fusion-tea/exploration/concept_analysis/concept_analysis_brief.md`

#### 3. Handwritten Exemplars (calibrate your depth and style against these)
- `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/handwritten/01-hts-compact-tokamak.md`
- `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/handwritten/07-maglif.md`
- `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/handwritten/08-frc-w-direct-conversion.md`
- `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/handwritten/11-magnetic-mirror-comparison.md`
- `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/handwritten/11-magnetic-mirror.md`
- `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/handwritten/26-laser-icf-indirect-drive.md`

Study the exemplars carefully. They show the expected level of technical depth, citation practice, and analytical rigor. Your output should match their quality. Note that exemplars may vary in structure — follow the output template for section structure, but match the exemplars for analytical depth and style.

#### 4. Phase 1a Dossier (structured research summary for this concept)
`/home/reid/1cfe/fusion-tea/exploration/phase_1a/research/09-qi-stellarator-hts/dossier.md`

The dossier contains per-column values with confidence ratings, citations, and notes from prior research iterations. This is your factual foundation.

#### 5. Extracted Source Documents (use subagents — see Per-Source Reading Pattern above)

Spawn one subagent per source document. For cold-start analysis, ask each subagent:
- What does this source tell us about the concept's cost structure and unique subsystems?
- What LCOE-relevant parameters or performance targets are stated?
- What cost advantages or penalties relative to conventional approaches are discussed?
- What technical risks, assumptions, or data gaps are mentioned?
- What materials, supply chain, or manufacturing considerations are relevant?

Sources to read via subagents:
- `/home/reid/1cfe/fusion-tea/exploration/phase_1a/research/09-qi-stellarator-hts/iter-01/sources/proxima-fusion-technology-page.md` (1 KB)
- `/home/reid/1cfe/fusion-tea/exploration/phase_1a/research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md` (2 KB)
- `/home/reid/1cfe/fusion-tea/exploration/phase_1a/research/09-qi-stellarator-hts/iter-02/sources/helios-stellarator-comparison.md` (1 KB)
- `/home/reid/1cfe/fusion-tea/exploration/phase_1a/research/09-qi-stellarator-hts/iter-02/sources/proxima-fusion-2026-updates.md` (2 KB)
- `/home/reid/1cfe/fusion-tea/exploration/phase_1a/research/09-qi-stellarator-hts/iter-02/sources/stellaris-paper-details.md` (2 KB)

#### 6. Schema (controlled vocabulary and column definitions)
`/home/reid/1cfe/fusion-tea/exploration/phase_1a/schema.md`

### Content Requirements
- Follow the output template section structure exactly (Sections 1-8)
- Do NOT include YAML frontmatter — the pipeline generates it automatically
- Every factual claim must cite a specific source (Phase 1a source document, dossier citation, or extracted document)
- Every quantitative value in Section 5 must have a Source and Confidence column entry
- Values without sources must be flagged as `[inferred]`, `[analogue]`, or `[estimated]` with reasoning

### Output

#### Step 1: Write the analysis body

Write the complete analysis to this file using the Write tool:
`/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/09-qi-stellarator-hts/analysis_body.md`

Write ONLY the analysis content (Sections 1-8). Do NOT include:
- YAML frontmatter (the pipeline adds it automatically)
- Preamble or commentary
- Code fences wrapping the document

Start the file with `# D1+ Analysis:` and end after Section 8.

#### Step 2: Update Reuses (if applicable)

If you referenced any approved prior analyses, update the Reuses field in:
`/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/09-qi-stellarator-hts/analysis.md`

The file already contains `Reuses: []`. Use the Edit tool to replace it with the concept IDs you referenced, e.g.:
`Reuses: [21-spherical-tokamak-hts, 28-hts-tokamak-full-hts]`

If you did not reference any approved analyses, leave Reuses unchanged.






## Output Template Structure

`/home/reid/1cfe/fusion-tea/exploration/concept_analysis/prompt_templates/output_template.md` defines the 8 required sections. The analysis must follow this structure regardless of mode.

## Cross-Concept Reuse

- `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/01-hts-compact-tokamak/analysis.md`
- `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/07-maglif/analysis.md`
- `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/08-frc-w-direct-conversion/analysis.md`
- `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/21-spherical-tokamak-hts/analysis.md`

If approved prior analyses are available:
- Read all approved prior analyses listed above
- Identify shared subsystems, materials, cost structures, or physics
- Reuse consistent assumptions where appropriate — cite the source concept
- Note divergences in Section 7 (Cross-Concept Notes)
- Do NOT copy text verbatim — synthesize and adapt to this concept's specifics
