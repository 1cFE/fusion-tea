# Source Integration Assessment: Spherical Tokamak - CS-free p-B11 (p-B11)

You are evaluating new source documents that have been added to a concept
that already has a completed analysis. Your job is to identify what material
information from the new sources should be incorporated into the existing
analysis, and produce structured feedback for the analysis agent.

## Existing Analysis
Read this file completely:
`/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/39-spherical-tokamak-cs-free-p-b11/analysis.md`

## New Source Documents (use subagents)

Spawn one subagent per new source document. Ask each subagent:
- What new technical, economic, or performance data does this source contain?
- Does it contain information that contradicts or updates claims in the analysis?
- What LCOE-relevant parameters or cost data are present?
- What risk, timeline, or TRL information is relevant?

New sources:
- `/home/reid/1cfe/fusion-tea/knowledge/concept_research/39-spherical-tokamak-cs-free-p-b11/iter-02/sources/arxiv-2406-15495.md` (4 KB)
- `/home/reid/1cfe/fusion-tea/knowledge/concept_research/39-spherical-tokamak-cs-free-p-b11/iter-02/sources/frontiersin-journals-nuclear-engineering-articles-10-3389.md` (42 KB)

## Analysis Goals (for reference)

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


## Instructions

1. Read the existing analysis completely
2. Spawn subagents to read each new source
3. Compare the new information against what the analysis already covers
4. Identify material gaps — information that would change the analysis's
   conclusions, parameter values, risk assessment, or modeling recommendations
5. Do NOT flag information the analysis already covers adequately
6. Do NOT flag minor/cosmetic additions — focus on material impact

## Output

Write structured feedback to this file using the Write tool:
`/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/39-spherical-tokamak-cs-free-p-b11/iter-3/source_integration_output.md`

Use this exact format:

# Feedback Format

Both the assessment agent and the interactive manage-concept agent produce
feedback in this format. The analysis agent consumes it in feedback-pass mode.

## Structure

Each feedback file contains:
1. A verdict line: `VERDICT: PASS` or `VERDICT: FINDINGS`
2. Zero or more findings (max 3 per assessment pass)

## Finding Format

### F-N: [Short title]
- **Target:** [Section number or aspect of analysis, e.g., "Section 2" or
  "Cross-concept comparison"]
- **Category:** analysis | model
- **Finding:** [What is insufficient, missing, or incorrectly framed — in
  terms of shape/framing, NOT numerical accuracy]
- **Recommendation:** [What the analysis agent should do differently —
  specific enough to act on]
- **Priority:** blocking | important | minor

## Rules
- Maximum 3 findings per pass (focus on the most impactful issues)
- Each finding must include a `Category` field:
  - `analysis` — the fix requires changes to the analysis text
  - `model` — the fix requires changes to the model code or parameters
    (sensitivity sweeps, scenario branches, parameter values in model_setup.py)
- Findings must reference specific analysis goals from analysis_goals.md
- Findings about numerical accuracy should focus on plausibility (order of
  magnitude, physical reasonableness), not verification (re-deriving calculations
  or matching citations to source text)
- Each finding must be specific enough that the analysis agent can address
  it without access to the assessment agent's reasoning
- If the analysis adequately addresses all goals: `VERDICT: PASS`

## Example

VERDICT: FINDINGS

### F-1: Missing cost implication for direct energy conversion
- **Target:** Section 2 (Challenges) and Section 5 (Parameters)
- **Category:** analysis
- **Finding:** The analysis identifies direct energy conversion as a key
  differentiator (Goal 2) but does not state the cost implication (Goal 3).
  No parameter row exists for direct conversion efficiency or its impact on
  balance-of-plant costs.
- **Recommendation:** Add a paragraph in Section 2 explaining how direct
  conversion changes the BOP cost structure (eliminates thermal cycle but
  adds conversion hardware). Add conversion efficiency and BOP cost delta
  to the Section 5 parameter table.
- **Priority:** blocking


**Adaptation for source integration**: The "Finding" field should describe
what new information the source provides. The "Recommendation" field should
specify exactly where and how to incorporate it into the analysis (which
section, what to add/update). The "Target" field should reference the analysis
section that needs updating.

If the new sources contain no material information beyond what the analysis
already covers, return `VERDICT: PASS`.
