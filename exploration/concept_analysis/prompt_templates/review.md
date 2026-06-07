# Strategic Review: {{concept_name}}

You are performing a strategic quality review of the concept analysis for
**{{concept_name}}** ({{company}}). Produce a structured review with a clear
PROCEED or REVISE verdict.

## Your Task

Evaluate the strategic quality of this analysis under the new pipeline contract:
design-point coherence, override discipline, family-delta against the fixed
comparables, two-knob projection correctness, risk framing, and data sufficiency.

## Files to Review

### Analysis
`{{analysis_path}}`

{{#if model_setup_path}}
### Model Setup
`{{model_setup_path}}`
{{/if}}

{{#if model_output_path}}
### Model Output
`{{model_output_path}}`
{{/if}}

### Source Documents
{{source_paths}}

### Approved Prior Syntheses (context for the family-delta)
{{approved_syntheses}}

## Strategic Assessment Dimensions

### 1. Design-Point Coherence
- Does the top-of-body Design Point block match the frontmatter selection (name,
  maturity, `P_native`, grounding), unedited?
- Does Section 5 describe that *one* named plant at native scale, with `P_native`
  consistent across the Design Point block, Section 5, and `model_setup.py`?
- Are physics-characteristic params (`eta_th`, `eta_de`) overridden only when the
  design point's physics genuinely differs from the archetype default?

### 2. Override Discipline
- Are Override Candidates six-field entries with canonical account codes (no
  invented `CAS22.1.3`-style codes)?
- Is `provenance` honest (`direct` vs `derived`), with derivation arithmetic and
  any CPI factor shown in `rationale`?
- Does the same override `account` carry the same `provenance` in the analysis
  Section 5b YAML and the `model_setup.py` `overrides` list?
- Is the enabled-override count consistent with the archetype-fit grade band, and
  free of un-evidenced re-passes of library defaults?
- **Rationale baseline frame:** Is every enabled relative override's `rationale`
  written in the **modular-fleet frame** — anchored to "the library's default for
  a 1 GWe fleet of this device" — and NOT against a "conventional / monolithic
  1 GWe plant"? The 1 GWe headline is always the replicated fleet, so a monolithic
  baseline does not exist. **Distinguish carefully:** an analyst citing a
  monolithic plant from the literature as a *comparable* (ARC, STEP, a published
  1 GWe study) is legitimate and not a finding; using a monolithic plant as the
  override's *anchor baseline* (e.g. "5% of a conventional 1 GWe plant's
  buildings") is the finding.
- **Value↔class consistency:** Does each relative override's value anchor match the
  account's cost class? A CAS22 reactor-island sub-account (Class U) anchors to
  `generic.cas22_detail["C2201xx"]` (per-module M$); a top-level Class-S or
  Class-P account anchors to `generic.costs.<rollup>` (whole-plant M$). A
  sub-account valued against a top-level rollup — or vice-versa — is a value↔class
  mismatch. **Do NOT infer a scaling failure from the CAS22 sub-account detail
  table:** that table shows per-module M$ at every scale, so a `C2201xx` row reading
  the same at native and 1 GWe is *expected* (the ×`n_mod` fleet multiplication
  lands in the `C220000` / `CAS22` rollup, not the detail row). Only flag a Class-U
  override as not reaching the fleet if the **`CAS22` rollup** fails to move by
  roughly `Δ(per-module value) × n_mod`.

### 3. Family-Delta vs Fixed Comparables
- Is the Section 7 family-delta prose specific and correct against the **fixed**
  Comparables list (named subsystems, cost direction) — not generic novelty
  claims or an arbitrary neighbour?

### 4. Two-Knob Projection & Model Integrity
- Does `model_setup.py` use the four-step helper form (`result, result_1gw =
  run_native_and_1gw(...)`), with module-level `model` / `result` / `result_1gw`
  and no inline two-knob `forward()` and no `# DEFAULT:` re-passes?
- Is the projection LCOE (`result_1gw`) plausible, and the native LCOE coherent
  with it?

### 5. Risk, Uncertainty & Data Sufficiency
- Are the right risks highlighted (technical, economic, supply-chain, regulatory)?
- Is the confidence assessment realistic, are TRL ratings defensible, and is the
  analysis honest about what it doesn't know?
- Are there critical gaps that should trigger more research before proceeding?

## Output Format

Write the review to: `{{output_path}}`

Use this exact format (the verdict line and finding headers are machine-parsed):

```
# Review: {{concept_name}}

**Iteration:** {{iteration}}
**Date:** {{date}}
**Files reviewed:** analysis.md{{#if model_setup_path}}, model_setup.py{{/if}}
**Source documents:** {{source_count}} files

---

## Strategic Assessment

[Narrative assessment organized by the 5 dimensions above. Not a checklist —
 a reasoned evaluation. Address each dimension but focus depth where this
 concept has notable strengths or concerns.]

---

## Verdict

VERDICT: [PROCEED | REVISE]

[If PROCEED]: This analysis is strategically sound. [Brief justification.]
[If REVISE]: The following issues require another pass through stage1. [Brief justification.]

---

## Minor Fixes (PROCEED only)
[Optional PA-N actions for address-review — only small fixes that don't warrant a
 full stage1 re-run. Omit this section entirely if there are none.]

### PA-1: [title]
- **Category:** improvement | inconsistency | factual-concern
- **Severity:** minor
- **Location:** [file §section]
- **Finding:** [what the review found]
- **Proposed Fix:** [what should change]
- **Decision:** _[USER FILLS IN: agree | reject | alternative]_
- **User Notes:** _[USER FILLS IN]_

---

## Corrective Actions (REVISE only)
[F-N findings. These feed back into analyze --resume as the feedback source.
 Only include for a REVISE verdict.]

### F-1: [title]
- **Target:** [Section or artifact the fix lands in]
- **Category:** analysis | model
- **Finding:** [Strategic issue — what is wrong with the current approach]
- **Recommendation:** [What stage1 should do differently]
- **Priority:** blocking | important | minor
```
