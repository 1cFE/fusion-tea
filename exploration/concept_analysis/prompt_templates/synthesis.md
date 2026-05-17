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

#### 8. LCOE Downselect Scoring

Score this concept using the scoring framework below. You score C1, C3, C4, C5,
and C8. You also fill the C7 risk matrix (7 functions x 2 subcategories = 14 cells).

**You do NOT score C2, C6, or C7.** These are computed deterministically by Python.
Do not include them in your score table or YAML block.

For each scored criterion, provide:
- The **score** (1-5, where 5 = most favorable)
- **Sub-scores** where the framework defines them
- **2-3 sentences of justification** citing specific data from the analysis,
  model output, CAS breakdown, or gap report. Do not score without evidence.

**Do not double-count between criteria.** C4 measures operational complexity of
the built plant, not physics feasibility. C7 is the sole place where "this might
not work at all" is scored.

**Apply the framework rules strictly. Common synthesizer errors to avoid:**

1. **Do not score Evidence Tier 2 when the framework says Tier 1.** "Subscale
   demonstration" (Tier 2) requires actual experimental hardware running at
   reduced scale. Theoretical models, simulations, design papers, and "company
   claims" without operating hardware are explicitly Tier 1. If a concept has
   been working on a problem for more than 5 years without demonstrated closure,
   the cell is Tier 1 — not Tier 2 — regardless of qualitative progress.

2. **Do not classify a risk as "Degrading" when failure means zero net
   electricity.** If your own cell description says "this would mean Q < 1" or
   "the concept is eliminated" or "no fallback exists," the classification MUST
   be **Binary**. The framework's Binary classification is mandatory whenever
   the failure outcome is no-net-electricity — even if the closure pathway
   feels plausible.

3. **Write out C3 sub-factor B arithmetic explicitly.** List each bottleneck
   with its penalty (–1.0 hard, –0.5 scaling, –0.25 sole-source, –1.5 for He-3
   fuel dependency). Sum the penalties. Compute `B = 5.0 - sum(penalties)`.
   Do not just state "B = X."

4. **Show sub-factor weights summing to 100%.** If you cost-weight components
   for C1 or C3-A, your shares must sum to ~100% of the basis (CAS22 only, or
   total capital — pick one). If they don't, your weighted average is wrong.

Present C1, C3, C4, C5, C8 as a table with sub-factor breakdowns, then fill the
complete 7-function x 2-subcategory risk matrix with all required per-cell fields.
Report function-level means (F1-F7). End with the YAML scores block.

### Gap Report
{{#if gap_report_path}}
`{{gap_report_path}}`
{{/if}}

### Scoring Framework

{{@config/scoring_framework.md}}
