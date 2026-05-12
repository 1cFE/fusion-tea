# Methodology Findings from the Calibration Pass

**Source:** Bootstrap worked examples for 01-hts-compact-tokamak and 18-p-b11-frc per `concept_part2.md` §workflow item 4 ("calibration pass").
**Date:** 2026-05-11
**Status:** Open findings — to be folded into the next revision of `concept_part2.md`.

The two end-to-end traces and their critiques surfaced two structural frictions with the methodology as written. Both are real — they recurred across concepts and across the original-draft → critique → revise cycle. Recording here so they can be considered before the methodology is applied at scale.

---

## Finding 1 — Ecosystem-relational F-factors that aggregate over multiple critical components cannot always commit to a single pole

**Where it bit:** F2.d (critical component supply maturity), F3.a (supply-chain maturity at chasm scale), and F4.c (specialty-input external-market position) — each spans multiple critical components with structurally different external-market positions.

**Example (concept 01):** F2.d covers REBCO (leverage pole, ~$30–50/kA-m delivered via MRI/grid/accelerator demand) *and* tritium / Li-6 / Be (failure pole, no external commercial market beyond declining CANDU supply). REBCO dominates Stage-2 CAPEX; tritium dominates Stage-2 *feasibility* if unsolved. Forcing a single F2.d pole-commit either loses the REBCO leverage signal or the tritium failure signal — both are decision-relevant.

**Why the critique flags it:** The pole-commit discipline is what prevents traces from degenerating into hedged narratives. Allowing sublines without rules creates a back-door for hedging.

**Why the trace authors keep doing it:** The underlying reality genuinely has different poles for different critical components. The traces are not dodging; the methodology is asking the wrong question.

**Candidate resolutions** (for discussion, not yet decided):

1. **Per-component sublining as a first-class construct.** Allow F2.d / F3.a / F4.c to be assessed once per critical component, with each subline carrying its own pole + slack/bottleneck tag. The dominant-coordinate machinery then picks the *subline* (concept × stage × factor × component) most likely to kill or save the concept. Costs a small amount of trace verbosity; gains correct discrimination.
2. **Forced weighted pole-commit with explicit weighting rule.** Pick the pole that dominates by CAPEX share (or by Stage-N criticality — different rules for different stages). State the weighting and the losing subline in one clause. Preserves single-pole discipline; demotes the secondary subline to a rationale footnote.
3. **Split the factor.** Replace F2.d / F3.a / F4.c with one factor per major component class (F2.d-REBCO, F2.d-fuel-cycle, F2.d-laser-optics, etc.). Most heavyweight; tracks reality most cleanly; works best if the concept set genuinely clusters on a small fixed set of components.

Trace 01's existing prose effectively did (1) under duress. Trace 18 used (2) implicitly by always picking the dominant component. The choice between these affects how the spanning algorithm reads the 2D coordinates downstream.

---

## Finding 2 — The Stage-1 "discount, not gate" treatment leaves no rubric vocabulary for physics-viability cliffs at Stage 2

**Where it bit:** Concept 18 (p-B11 FRC). The dominant failure mode for this concept is unambiguously a physics-viability binary: sustained T_i >> T_e at commercial ion temperature and Q_plasma > 1 in the aneutronic regime, neither demonstrated at relevant scale. Below this threshold the concept has no LCOE — not a degraded one. The trace author had to map this onto F2.b (build-time risk) because the rubric has no native code for "physics-viability cliff that surfaces at Stage 2 commissioning."

**Why the critique flagged it:** F2.b is build-time-and-engineering-risk, not physics-binary risk. Using F2.b as a proxy obscures what the concept's actual failure mode is and makes the trace less discriminating in the 2D landscape against engineering-gated concepts.

**Why concept_part2.md is the way it is:** §Stage 1 explicitly chose not to evaluate physics as a selection gate — the project lacks expertise to adjudicate competing physics claims, and treating it as a discount on downstream value (calibrated by paradigm co-development depth, scientific heritage, workforce depth) was the chosen handle.

**The friction:** "Discount on downstream value" works when the physics question is one of *speed-to-Stage-2* (a more validated paradigm reaches Stage 2 faster and cheaper). It does not work when the physics question is one of *whether Stage 2 is reachable at all* under the concept's commercial-target parameters. Concept 18's commissioning campaign is precisely a coin flip on whether the regime exists at commercial scale — that is qualitatively a different kind of risk than "ITER's tritium retention numbers are still being argued."

**Candidate resolutions:**

1. **Add a new Stage-2 intrinsic F-factor: F2.e — physics-viability cliff at commissioning.** Distinct from F2.b (engineering build-time) and from the Stage-1 discount (paradigm immaturity → cost/time penalty). Only triggers for concepts whose commercial-target parameters require an unmeasured plasma regime; usually maps to aneutronic concepts, ICF-net-energy-margin concepts, and exotic-confinement concepts.
2. **Promote Stage 1 from discount to optional gate.** For concepts where the trace identifies an unresolved physics binary, escalate Stage 1 from a discount factor to the dominant failure mode in its own right. Requires adding "Stage 1 / physics binary" as a possible value of the dominant-failure axis in the 2D landscape.
3. **Keep the current rubric; document the F2.b proxy convention.** Concede that F2.b absorbs physics-commissioning risk for early-physics-gate concepts, and document this convention so traces don't have to invent it. Lowest-friction; weakest discrimination.

Resolution (1) seems cleanest — it preserves the project's "don't adjudicate competing physics claims" stance while giving the rubric a place to *acknowledge* a physics binary without scoring its outcome. The trace assesses "is the concept's commercial target above or below an unmeasured regime boundary?" without claiming to know which side of the boundary the regime actually sits.

---

## Lower-priority observations

- **Slack/bottleneck "likely" softening.** Trace authors instinctively want to qualify slack/bottleneck tags ("bottleneck-likely," "slack-for-now"). The rubric expects committed tags. Either tighten the rubric (committed only, no hedges) or formalize the qualifier (e.g., a third tag: "transitional" for time-bounded slack that converts to bottleneck).
- **"Mixed" as F4.b value.** Both traces used "Mixed-leaning-X" instead of the rubric's clean "mixed." The rubric should either drop "mixed" (force volume vs. R&D) or accept "mixed" but explicitly disallow "leaning" softening.
- **Cross-stage carrier-vs-F-factor double-counting.** Trace 01 listed tritium under F2.d (component supply), F3.a (chasm-scale supply), and the tritium F-carrier. Three appearances for one concern. The methodology says carriers are "F-factors that recur across stages with different bite," so triple-listing is correct — but the trace reader experiences it as repetition. Worth a §Evaluation-procedure note about how to compress this in prose.

---

## Recommended action

Fold Findings 1 and 2 into a revision of `concept_part2.md` before applying the trace methodology to the remaining ~36 concepts. The lower-priority observations can be handled as inline clarifications in the §Evaluation procedure template.
