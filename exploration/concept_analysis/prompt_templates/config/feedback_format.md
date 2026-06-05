# Feedback Format

Both the assessment agent and the interactive manage-concept agent produce
feedback in this format. The analysis agent (and, for model-category findings,
the model-setup agent) consume it in feedback-pass mode.

This format is machine-parsed by simple line-anchored scanning. Emit it exactly
as specified — the verdict line and the finding headers are read literally.

## Structure

Each feedback file contains, in order:
1. A **verdict line** — a line reading exactly `VERDICT: PASS` or
   `VERDICT: FINDINGS`, on its own line, with nothing after the token.
   (`VERDICT: PASS — all good` is NOT accepted; put any commentary on a
   separate line.)
2. Zero or more findings (maximum 3 per pass).

## Finding Format

Each finding is a block that begins with a `### F-N:` header (N is an integer:
`### F-1:`, `### F-2:`, …) followed by bold-key bullet lines:

```
### F-N: [Short title]
- **Target:** [Section or artifact the fix lands in — e.g. "Section 5b (Override
  Candidates)" or "model_setup.py overrides list"]
- **Category:** analysis | model
- **Finding:** [What is insufficient, missing, or incorrectly framed]
- **Recommendation:** [What the agent should do differently — specific enough to
  act on without seeing your reasoning]
- **Priority:** blocking | important | minor
```

## Category — exactly two values

Each finding MUST carry a `Category` field whose value is `analysis` or `model`:
- **`analysis`** — the fix lands in `analysis.md` (Design Point block, Section 5
  parameters, Section 5b Override Candidates, family-delta prose, framing).
- **`model`** — the fix lands in `model_setup.py` (the `overrides` list, the
  `spec` dict, sweeps/scenarios, or the two-knob helper call).

There is **no third category.** The new contract's cross-artifact failure modes
route by where the fix lives:
- `P_native` mismatch between the Design Point block and `model_setup.py` →
  `analysis` if the analysis text is wrong, `model` if the model constant is wrong.
- Override `provenance` drift (analysis YAML says `direct`, model says `derived`,
  or vice-versa) → the artifact carrying the wrong label.
- Account-namespace miss (an invented or wrong canonical code) → wherever the bad
  code appears.

## Rules
- Maximum 3 findings per pass — focus on the most impactful issues.
- Findings about numbers focus on *plausibility* (order of magnitude, physical
  reasonableness, design-point coherence), not on re-deriving calculations.
- Each finding must be specific enough to act on without access to your reasoning.
- If the analysis adequately addresses all goals: `VERDICT: PASS` with no findings.

## Example

VERDICT: FINDINGS

### F-1: Override count exceeds the High-fit band without justification
- **Target:** Section 5b (Override Candidates)
- **Category:** analysis
- **Finding:** The concept is graded High archetype-fit (expected 0–4 enabled
  overrides) but the registry enables 7, and three of them re-state the library
  default with no company-published quantity or unit cost in `rationale`.
- **Recommendation:** Disable or remove the three un-evidenced overrides
  (C220105, C220110, CAS24) so the library default stands, leaving only the
  company-grounded departures.
- **Priority:** important
