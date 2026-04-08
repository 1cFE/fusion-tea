# Assessment: QI Stellarator - HTS

You are evaluating a D1+ concept analysis for quality of framing, completeness, and numerical plausibility relative to the analysis goals.

## Files to Read

### Analysis
Read this file completely:
`/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/09-qi-stellarator-hts/analysis.md`

### Analysis Goals

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


### Assessment Checklist

# Assessment Checklist

Evaluate the analysis against each criterion below. A finding means the
analysis does not adequately address the criterion.

## Shape and Framing (Goals 1-2)
- [ ] The analysis identifies which concept family this belongs to and names
      the 2-3 nearest-neighbor concepts for comparison
- [ ] Key differentiators from a conventional tokamak are explicitly listed
      (not just implied in the narrative)
- [ ] Novel subsystems or approaches are distinguished from borrowed/shared ones

## TEA Impact (Goal 3)
- [ ] Each key differentiator has a stated cost implication (advantage, penalty,
      or neutral with reasoning)
- [ ] The Section 5 parameter table includes parameters for all identified
      cost-relevant differentiators
- [ ] CAS-level cost structure differences from the reference concept are noted

## Modeling Recommendations (Goal 4)
- [ ] Section 2 identifies the 2-3 parameters with highest LCOE sensitivity
      for this specific concept
- [ ] The analysis states whether 1costingfe or free-form modeling is
      appropriate and why
- [ ] Key hypotheses are stated as testable propositions (not just open questions)

## Risk Identification (Goal 5)
- [ ] Each key technical bet is stated with what happens if it fails
- [ ] Assumptions unique to this concept (vs. shared fusion assumptions) are flagged
- [ ] Section 6 gap table distinguishes blocking vs. non-blocking data gaps

## Modeling (Data Model Integrity)
- [ ] If `model_setup.py` exists, its output interface is genuine: `result`
      (costingfe) or `to_explorer_dict()` (freeform) reflects actual model
      computations, not stub values or passthrough wrappers
- [ ] CAS cost values are the result of parameter-driven calculations, not
      hardcoded constants or placeholder zeros across all accounts
- [ ] Sensitivity results (if present) show non-trivial variation — at least
      3 parameters have |elasticity| > 0.01


## Instructions

1. Read the analysis completely
2. Evaluate against each checklist criterion
3. Identify the most significant gaps — at most 3 findings
4. For each finding, explain what is insufficient and what should change
5. If the analysis adequately addresses all goals, return PASS

### Finding Categories

Each finding must include a `Category` field:
- **`analysis`** — the fix requires changes to the analysis text (Section 2 framing,
  Section 5 parameter tables, Section 7 differentiator discussion, etc.)
- **`model`** — the fix requires changes to the model code or parameters:
  sensitivity sweeps, scenario branches, parameter values in model_setup.py,
  model output formatting, or computational methodology

A finding is `model` when the recommendation says to change what the model
*computes or sweeps*. A finding is `analysis` when the recommendation says
to change what the analysis *says or frames*.

When a finding touches both (e.g., "add parameter to Section 5 table AND
to sensitivity sweep"), assign the **primary** target — the one that would
resolve the core issue.


## Model Output

The concept also has a quantitative LCOE model. The model output is at:
`/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/09-qi-stellarator-hts/iter-9/model_output.txt`

Evaluate whether:
1. The model's assumptions and parameter values are consistent with the analysis.
2. The LCOE result is plausible for this concept type (order of magnitude).
3. Key cost drivers in the model match the analysis narrative's emphasis.
Note any discrepancies in your findings.


## Scope

Focus on whether the analysis captures the **shape** of the concept:
positioning, differentiators, TEA implications, modeling approach, and risks.

Additionally, check **numerical plausibility**:
- Are parameter values the right order of magnitude for this concept type?
- Does the model output LCOE align with the analysis narrative's claims?
- Are physical parameters (temperatures, pressures, efficiencies) within
  physically plausible ranges for the stated technology?

You are NOT checking formatting, style consistency, or template structure compliance.

## Output

Write the assessment to this file using the Write tool:
`/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/09-qi-stellarator-hts/iter-9/feedback.md`

Use the exact format below:

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

