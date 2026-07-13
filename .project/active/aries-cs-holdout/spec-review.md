# Spec Review: ARIES-CS Hold-Out Ingestion and Quarantine Protocol

**Spec:** `.project/active/aries-cs-holdout/spec.md`
**Contract:** `/home/reid/.agents/skills/my-spec/SKILL.md`
**Review File:** `.project/active/aries-cs-holdout/spec-review.md`
**Date:** 2026-07-12

---

## Reality Check

**Fail.** The work item is the right one, but the spec's premise and contamination inventory are materially incomplete. Existing active 09 artifacts already contain detailed ARIES-CS design comparisons, and the existing review says the stellarator cost baseline was calibrated with ARIES-CS. A design that treats this spec as the contract could quarantine the four new PDFs perfectly while preserving a model-development path that has already absorbed the hold-out.

---

## Audit

Deeper lens review was skipped because the premise fails Stage 0. **L1-1 · Direct claim:** The spec describes the current holdings as two OSTI abstracts (`spec.md:13`) and limits the contamination inventory to those abstracts, one synthesis quote, library defaults, and model priors (`spec.md:23`). The live 09 artifacts show broader and already-derived exposure: the analysis uses detailed ARIES-CS manufacturing and maintenance facts (`exploration/concept_analysis/analyses/09-qi-stellarator-hts/analysis.md:311`); the synthesis compares field, size, maintenance, and LCOE against ARIES-CS (`exploration/concept_analysis/analyses/09-qi-stellarator-hts/synthesis.md:119`); the review states that ARIES-CS calibrated the stellarator cost baseline (`exploration/concept_analysis/analyses/09-qi-stellarator-hts/review.md:24`); and the analysis prompt explicitly required both ARIES-CS abstracts plus the Helios source that carries detailed ARIES-CS comparisons (`exploration/concept_analysis/analyses/09-qi-stellarator-hts/iter-1/analyze_prompt.md:528`). This is not a passive source-placement leak. It is prior use in artifacts that a later model-development session could reuse. The strict public claim at `spec.md:35` is therefore unsupported until the owner chooses either a clean-room path that bars all ARIES-informed 09 artifacts or a weaker, explicitly partial-blind claim.

---

## Engagement Summary

**Overall take:** Quarantining the four PDFs is useful, but it does not establish the strict hold-out described here. The spec needs premise-level rework before design because it understates prior contamination and never decides whether existing 09 analysis and model artifacts are admissible.

**Here's what I need you to weigh in on:**

1. **[L1-1]** Choose the validation claim: a clean-room demo that bars every ARIES-informed 09 source and derived artifact from model-development context, or a partially blind demo whose public claim explicitly admits prior ARIES-CS-informed modeling.
2. **[L1-1]** Decide whether the existing 09 model, analysis, synthesis, review, prompts, and Helios comparison may be reused. Under the strict claim, they cannot be treated as clean inputs.
3. **[L1-1]** Require the rewritten contamination inventory to cover derived artifacts and concrete ARIES-CS details already in the active 09 pipeline, not only the two abstract pages and one synthesis quote.

---

## Resolutions

**[L1-1] — Resolved by owner, 2026-07-12: clean-room.**

1. Validation claim: **clean-room**. Demo model-development sessions may not have any ARIES-CS-informed material in context — neither the held-out papers nor the existing repo artifacts that carry ARIES-CS-derived content.
2. Existing 09 artifacts: **not admissible** as demo model-development inputs. Barred: all of `exploration/concept_analysis/analyses/09-qi-stellarator-hts/` (analysis, synthesis, review, prompts, model_setup, outputs), the two ARIES-CS abstract stubs in `iter-02/sources/`, and the Helios comparison extraction (the carrier of the detailed ARIES-CS facts). The Waganer ARIES cost-account doc and the Araiinejad/Shirvan TEA paper (general costing sources containing ARIES-CS-specific data points) are barred by default, with a documented-exception path if the demo turns out to need one. The modeling basis is the clean set: Stellaris design paper, W7-X material, QI-configuration/HELIAS sources, the 1costingFE library (lineage exception already scoped in the concept), WI-009 cost-structure library, PyFECONS.
3. Contamination inventory: rewritten in the spec to name the derived artifacts and concrete exposure this review cited, not only the abstract pages and one synthesis quote.

Spec reworked accordingly (same session, 2026-07-12). Owner's deciding rationale, verbatim: "ok fine, let's do clean room" — after the trade (what clean-room bars is commentary artifacts, not the modeling basis; ARIES-CS is the grading key, not a modeling input) was laid out.

---

**Verdict:** Rework
**Next Steps:** Resolve **[L1-1]** in this review, then re-run `my-spec` (or return to the spec-agent session) and point it at this file. The reviewer does not edit the spec.
