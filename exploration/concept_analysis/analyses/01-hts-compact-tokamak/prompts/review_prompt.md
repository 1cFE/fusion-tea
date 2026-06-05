# Strategic Review: HTS Compact Tokamak (Commonwealth Fusion / ARC)

You are performing a strategic quality review of the concept analysis for
**HTS Compact Tokamak (Commonwealth Fusion / ARC)** (Commonwealth Fusion Systems). Produce a structured review with a clear
PROCEED or REVISE verdict.

## Your Task

Evaluate the strategic quality of this analysis under the new pipeline contract:
design-point coherence, override discipline, family-delta against the fixed
comparables, two-knob projection correctness, risk framing, and data sufficiency.

## Files to Review

### Analysis
`/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/01-hts-compact-tokamak/analysis.md`


### Model Setup
`/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/01-hts-compact-tokamak/model_setup.py`



### Model Output
`/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/01-hts-compact-tokamak/model_output.txt`


### Source Documents
- `/home/reid/1cfe/fusion-tea/knowledge/concept_research/01-hts-compact-tokamak/iter-03/sources/arc-reactor-specifications.md` (172 KB)
- `/home/reid/1cfe/fusion-tea/knowledge/concept_research/01-hts-compact-tokamak/iter-03/sources/sparc-icrf-heating-paper.md` (65 KB)
- `/home/reid/1cfe/fusion-tea/knowledge/concept_research/01-hts-compact-tokamak/iter-04/sources/arc-power-conversion-studies.md` (35 KB)
- `/home/reid/1cfe/fusion-tea/knowledge/concept_research/01-hts-compact-tokamak/iter-04/sources/arxiv-2405-01514.md` (61 KB)
- `/home/reid/1cfe/fusion-tea/knowledge/concept_research/01-hts-compact-tokamak/iter-04/sources/arxiv-2503-23048.md` (59 KB)
- `/home/reid/1cfe/fusion-tea/knowledge/concept_research/01-hts-compact-tokamak/iter-04/sources/arxiv-2601-21724.md` (165 KB)
- `/home/reid/1cfe/fusion-tea/knowledge/concept_research/01-hts-compact-tokamak/iter-04/sources/arxiv-2602-19389.md` (249 KB)
- `/home/reid/1cfe/fusion-tea/knowledge/concept_research/01-hts-compact-tokamak/iter-04/sources/cfs-2025-2026-updates.md` (6 KB)
- `/home/reid/1cfe/fusion-tea/knowledge/concept_research/01-hts-compact-tokamak/iter-04/sources/osti-etdeweb-servlets-purl-10149275.md` (164 KB)
- `/home/reid/1cfe/fusion-tea/knowledge/concept_research/01-hts-compact-tokamak/iter-04/sources/osti-etdeweb-servlets-purl-20261446.md` (11 KB)
- `/home/reid/1cfe/fusion-tea/knowledge/concept_research/01-hts-compact-tokamak/iter-04/sources/osti-servlets-purl-1305833.md` (48 KB)
- `/home/reid/1cfe/fusion-tea/knowledge/concept_research/01-hts-compact-tokamak/iter-04/sources/osti-servlets-purl-1820946.md` (14 KB)
- `/home/reid/1cfe/fusion-tea/knowledge/concept_research/01-hts-compact-tokamak/iter-04/sources/sciencedirect-science-article-pii-s092037961930835x.md` (2 KB)
- `/home/reid/1cfe/fusion-tea/knowledge/concept_research/01-hts-compact-tokamak/iter-04/sources/sciencedirect-science-article-pii-s2772830725000390.md` (2 KB)

### Approved Prior Syntheses (context for the family-delta)
- `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/21-spherical-tokamak-hts/synthesis.md`

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

Write the review to: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/01-hts-compact-tokamak/review.md`

Use this exact format (the verdict line and finding headers are machine-parsed):

```
# Review: HTS Compact Tokamak (Commonwealth Fusion / ARC)

**Iteration:** 1
**Date:** 2026-05-31
**Files reviewed:** analysis.md, model_setup.py
**Source documents:** 14 files

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
