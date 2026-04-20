# Synthesis: {{concept_name}}

You are producing an editorial synthesis for the fusion concept **{{concept_name}}**
({{company}}). Your role is to INTERPRET, JUDGE, and PRIORITIZE — not to document.

The underlying analysis has been reviewed and verified. You may trust its factual
claims. Your job is to synthesize them into decision-support guidance.

## Required Reading

### 1. Reviewed Analysis
`{{analysis_path}}`

### 2. Model Setup and Output
{{#if model_setup_path}}
`{{model_setup_path}}`
{{/if}}
{{#if model_output_path}}
Model output (user-generated): `{{model_output_path}}`
{{/if}}

### 3. Approved Prior Syntheses
{{approved_syntheses}}

## Writing Instructions

### Voice and Style
- **Be opinionated.** State what you think, not just what the data shows.
- **Be direct.** "This concept is unlikely to achieve commercial LCOE" is better
  than "There are significant uncertainties regarding commercial viability."
- **Quantify.** "Eliminates ~20% of direct capital" is better than "Significantly
  reduces capital cost."
- **Use model output.** Reference specific LCOE numbers, CAS breakdowns, and
  sensitivity elasticities from the model setup.

### Mandatory Sections

Write to: `{{output_path}}`

#### 1. Executive Summary (3-5 bullets)
- The single most important risk
- The single most important advantage
- LCOE ballpark from the model (or "no model available" with reasoning)
- Confidence verdict: High / Medium / Low with one-sentence justification

#### 2. What Matters Most for LCOE
Rank the top 3-5 parameters by LCOE sensitivity. For each:
- The assumed value and its source
- The sensitivity magnitude (elasticity from model, or qualitative if no model)
- What change in this parameter would flip the economic conclusion

#### 3. Risk Verdicts
For each major challenge from the analysis Section 2:
- **Verdict:** Likely resolvable | Unlikely resolvable | Genuinely uncertain
- **Rationale:** One sentence
- **What would retire this risk:** Specific evidence or milestone

#### 4. Structural Advantages and Disadvantages
Compare against the conventional D-T tokamak cost structure baseline.
Quantify eliminated or added cost items where possible.

#### 5. Cross-Concept Positioning
Where does this concept sit in the landscape? What concepts share similar
economics? What makes this one fundamentally different?

#### 6. Modeling Confidence
Rate: High / Medium / Low
- How many parameters are data-anchored vs. speculative?
- What is the dominant source of LCOE uncertainty?

#### 7. What Would Change My Mind
2-3 specific future developments or data releases that would materially
change the LCOE estimate (in either direction).

#### 8. Long-Term LCOE Potential (Downselect Scoring)

Score this concept on its long-term cost reduction potential using the seven
criteria defined in the LCOE Downselect Potential Framework below. C1–C6
measure how fast LCOE can improve with deployment experience. C7 measures
how likely the concept is to reach a working plant at all. Both dimensions
matter and are equally weighted.

For each criterion, provide:
- The **score** (1–5, where 5 = most favorable)
- **Sub-scores** where the framework defines them (e.g., per-CAS modularization
  mode, per-component learning rates, complexity sub-drivers, per-gate
  feasibility penalties)
- **2–3 sentences of justification** citing specific data from the analysis,
  model output, CAS breakdown, or taxonomy. Do not score without evidence.

**Important**: Do not double-count between criteria. C4 measures operational
complexity of the built plant, not physics feasibility. C6 uses the physical
availability budget, not TRL-adjusted penalties. C7 is the sole criterion
where "this might not work at all" is scored.

For C7, explicitly enumerate each feasibility gate with its severity
(binary/degrading/schedule), evidence level, and penalty calculation.

Present as a table:

| Criterion | Score | Key justification |
|-----------|-------|-------------------|
| C1: Modularization | X.X | ... |
| C2: Scalability | X.X | ... |
| C3: Supply Chain Learning | X.X | ... |
| C4: Plant Complexity | X.X | ... |
| C5: Customization Needs | X.X | ... |
| C6: Upper Capacity Factor | X.X | ... |
| C7: Technical Feasibility | X.X | ... |
| **Composite** | **X.X** | |

After the table, write a **one-paragraph verdict** interpreting the composite
score: what it means for this concept's long-term competitiveness, which
criteria are the strongest levers for improvement, and what would need to
change to materially raise the score.

### LCOE Downselect Potential Framework (Full Rubric)

{{@config/lcoe_downselect_framework.md}}
