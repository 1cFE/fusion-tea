# D1+ Concept Analysis: MagLIF (D-T)

You are producing a D1+ analysis for the fusion concept **MagLIF (D-T)** (Pacific Fusion, Fuse Energy Technologies).

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


## Cross-Concept Memory

The following insights were captured from prior concept analyses. Use them
to avoid known pitfalls and apply established patterns. Do not cite these
memories as sources — they are guidance, not evidence. Verify any specific
claims against the actual source documents.

## Assessment Repeatedly Flags Missing O&M Breakdown
Date: 2026-03-29 | Concepts: all

The assessment agent flags missing O&M cost breakdown (fixed vs variable,
scheduled maintenance, unplanned outage costs) in >80% of first-pass
analyses. Cold-start analyses should include a placeholder O&M subsection
in Section 3 even when source data is sparse, to avoid a guaranteed
feedback finding.





## Mode: Feedback Pass

You are improving an existing analysis based on specific feedback from the assessment agent.

### Existing Analysis
Read this file completely first:
`/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/07-maglif/analysis.md`

### Feedback to Address
Then read the feedback:
`/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/07-maglif/iter-6/source_integration_output.md`

The feedback contains specific findings (F-1, F-2, etc.) with targets, findings, and recommendations. Address each finding.

### Source Documents (use subagents for targeted evidence gathering)

For each finding in the feedback, spawn subagents to gather targeted evidence from the relevant sources. Ask questions specific to the feedback — e.g., if the feedback says "missing cost implication for direct energy conversion", ask subagents: "Does this source contain evidence about direct energy conversion costs, BOP impact, or conversion efficiency?"

Sources available for subagent queries:
- `/home/reid/1cfe/fusion-tea/knowledge/concept_research/07-maglif/iter-01/sources/arxiv-2408-15206-pulsed-magnetic-fusion.md` (84 KB)
- `/home/reid/1cfe/fusion-tea/knowledge/concept_research/07-maglif/iter-01/sources/fuse-energy-technology.md` (2 KB)
- `/home/reid/1cfe/fusion-tea/knowledge/concept_research/07-maglif/iter-01/sources/pacific-fusion-website-technology.md` (2 KB)
- `/home/reid/1cfe/fusion-tea/knowledge/concept_research/07-maglif/iter-01/sources/pacific-fusion-website-technology.orig.md` (3 KB)
- `/home/reid/1cfe/fusion-tea/knowledge/concept_research/07-maglif/iter-01/sources/z-ife-power-plant-concept.md` (3 KB)
- `/home/reid/1cfe/fusion-tea/knowledge/concept_research/07-maglif/iter-02/sources/fuse-energy-not-boring-details.md` (91 KB)
- `/home/reid/1cfe/fusion-tea/knowledge/concept_research/07-maglif/iter-02/sources/pacific-fusion-interview-fusion-report.md` (8 KB)
- `/home/reid/1cfe/fusion-tea/knowledge/concept_research/07-maglif/iter-02/sources/z-ife-sand2006-7148-thermal-cycles.md` (277 KB)
- `/home/reid/1cfe/fusion-tea/knowledge/concept_research/07-maglif/iter-03/sources/ans-news-2025-04-24-article-6980-pacific-fusion-fusing.md` (10 KB)
- `/home/reid/1cfe/fusion-tea/knowledge/concept_research/07-maglif/iter-03/sources/arxiv-2504-10680.md` (5 KB)
- `/home/reid/1cfe/fusion-tea/knowledge/concept_research/07-maglif/iter-03/sources/frontiersin-journals-nuclear-engineering-articles-10-3389.md` (91 KB)
- `/home/reid/1cfe/fusion-tea/knowledge/concept_research/07-maglif/iter-03/sources/globenewswire-news-release-2025-04-24-3067836-0-en-pacific.md` (5 KB)
- `/home/reid/1cfe/fusion-tea/knowledge/concept_research/07-maglif/iter-03/sources/osti-biblio-895981.md` (5 KB)
- `/home/reid/1cfe/fusion-tea/knowledge/concept_research/07-maglif/iter-03/sources/pacificfusion-updates-crada-sandia-national-laboratories.md` (3 KB)
- `/home/reid/1cfe/fusion-tea/knowledge/concept_research/07-maglif/iter-03/sources/pacificfusion-updates-experimental-breakthrough-by-pacific.md` (8 KB)
- `/home/reid/1cfe/fusion-tea/knowledge/concept_research/07-maglif/iter-03/sources/pacificfusion-updates-founders-letter.md` (7 KB)

Dossier (read directly — it's structured and short):
`/home/reid/1cfe/fusion-tea/knowledge/concept_research/07-maglif/dossier.md`

### Instructions
1. Read the existing analysis completely
2. Read the feedback — it contains specific findings to address
3. For each finding, use the per-source subagent pattern to gather targeted evidence from the sources
4. Use the Edit tool to make targeted improvements to `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/07-maglif/analysis.md`
5. Do NOT rewrite sections that aren't addressed by the feedback
6. Maintain all existing citations — only add/modify what the feedback requires
7. If a finding recommends adding parameter rows, add them in the correct table position with Source and Confidence columns
8. After making edits, re-read the modified sections to verify coherence




## Output Template Structure

`/home/reid/1cfe/fusion-tea/exploration/concept_analysis/prompt_templates/output_template.md` defines the 8 required sections. The analysis must follow this structure regardless of mode.

## Cross-Concept Reuse

- `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/21-spherical-tokamak-hts/analysis.md`

If approved prior analyses are available:
- Read all approved prior analyses listed above
- Identify shared subsystems, materials, cost structures, or physics
- Reuse consistent assumptions where appropriate — cite the source concept
- Note divergences in Section 7 (Cross-Concept Notes)
- Do NOT copy text verbatim — synthesize and adapt to this concept's specifics
