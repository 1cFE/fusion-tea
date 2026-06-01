# Assessment Checklist

Evaluate the analysis (and `model_setup.py`, when present) against each criterion
below. A finding means the artifact does not adequately satisfy the criterion.
Group your judgment under the five areas; emit at most 3 findings total, on the
most impactful gaps.

## 1. Design-Point Coherence
- [ ] The top-of-body Design Point block copies the selection fields verbatim
      from frontmatter — name, maturity, `P_native`, grounding — and the analysis
      has **not** silently substituted a different plant or power level.
- [ ] Every quantitative parameter in Section 5 describes that one named plant at
      its native scale. No roadmap aspiration, no different machine, no 1 GWe
      figure smuggled into the native parameter table.
- [ ] `P_native` is identical across the Design Point block, Section 5, and (if
      present) the `model_setup.py` `P_native` constant. The coherence flags
      provided to you report cross-artifact drift — read them.

## 2. Override Discipline
- [ ] Every Override Candidate is a six-field entry with a **canonical** account
      code (no invented `CAS22.1.3`-style codes).
- [ ] Each `enabled` override is evidence-backed: `provenance` honestly reflects
      whether the dollar figure was company-published (`direct`) or analyst-
      assembled (`derived`), and `derived` entries show their arithmetic
      (including any CPI factor) in `rationale`.
- [ ] No override merely re-states a library default, and no uniform financial /
      operating parameter (`availability`, `lifetime_yr`, `interest_rate`,
      `inflation_rate`) appears in `spec` or the registry.
- [ ] The same override `account` appears in the analysis Section 5b YAML and the
      `model_setup.py` `overrides` list with the **same** `provenance` label.

## 3. Override Count vs. Archetype-Fit Grade
- [ ] The count of `enabled` overrides is consistent with the concept's
      archetype-fit grade band (the override-count rubric is given to you):
      `High → 0–4`, `Med → 3–8`, `Low → 6–12`. A High-fit concept with many
      enabled overrides, or a Low-fit concept with zero, is a flag. The count-vs-
      grade check in the coherence flags reports this — corroborate it against
      what you read.

## 4. Family-Delta Concreteness
- [ ] The family-delta prose (Section 7) compares the design point against the
      **fixed** comparables list, not an arbitrary neighbour, and names specific
      subsystems with a cost direction — not generic "this is novel" framing.
- [ ] Each claimed differentiator carries a stated TEA consequence (advantage,
      penalty, neutral, or honestly "unknown").

## 5. Two-Knob Projection & Model Integrity
- [ ] If `model_setup.py` exists: it uses the four-step helper form
      (`result, result_1gw = run_native_and_1gw(...)`), with `model`, `result`,
      `result_1gw` at module level — not an inline two-knob `forward()`.
- [ ] `result` reflects real parameter-driven computation (CAS values are not
      hardcoded constants or all-zero placeholders); sensitivity results, if
      present, show non-trivial variation.
- [ ] The model's LCOE is plausible (right order of magnitude) for this concept
      type, and its dominant cost drivers match the analysis narrative's emphasis.

You are NOT checking formatting, style consistency, or template-structure
compliance. Focus on coherence, accountability, and numerical plausibility.
