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
