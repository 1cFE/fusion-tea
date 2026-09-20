# ARIES reveal result and repair baseline

Date: September 20, 2026.

The original ARIES comparison stopped before producing numerical predictions. We are starting repairs from the last pre-reveal code checkpoint, while preserving the completed experiment in Git. These repairs are informed by post-reveal findings. Returning to earlier code does not restore an unexposed holdout.

## What happened

[INHERITED: original report and independent scientific review at `829539f5`] The adopted r3 archive was verified before reveal. Its SHA256 is `34526b8b4587a306453a1f01fa73e6803e4eddf04c3ae0d0f3e647b69a9dbd19`. The agent then opened the reference papers, documented input selection, and executed one frozen forward request. Three reference inputs were supplied; four retained model defaults because their correspondence to published quantities was unresolved. No tuning or altered-input retry was performed.

The run stopped when its calculated peak magnetic field fell outside the conductor-performance approximation's supported 20–32 T range. The recorded error does not provide the exact field. This is a limitation of the represented conductor performance, not evidence that a physical reactor is impossible. The automatic winding-sizing calculation consumed that performance approximation and raised the error.

No completed power, component-cost, LCOE or engineering-predicate results were published. Structural correspondence remained unresolved. All 276 comparison rows were retained as unavailable. Therefore this attempt did not establish numerical agreement or disagreement with the reference, and did not pass the comparison.

The formal reporting mechanism also refused to register failed native execution. No first-forward identity was created. The committed request, failed native result and execution record nevertheless preserve the original attempt; absence of that identity does not make a subsequent attempt the original result. Independent scientific review and reporting replay accepted the accuracy of the failure record, not the scientific adequacy of the model.

## What we learned

[AGENT] The attempted transfer encountered unsupported conductor-performance conditions. Supported operating ranges and input correspondence need examination. The finding alone does not justify extending an empirical law, removing a validity check, or selecting assumptions to obtain agreement.

[OWNER-VERBATIM] “As soon as you start introducing ‘sizing’, then you are basically pre-defining which design parameters are ‘free’ and which are ‘derived’. this is explicitly what we wanted to avoid.”

[AGENT] Investigation exposed model choices inconsistent with that intent: automatic winding inventory/geometry, facility allocation and fuel-processing capacity, with related fixed flow and cost assumptions elsewhere. The architecture problem is visible in pre-reveal code and can be investigated without reference-specific numerical targets. Existing depth and reproduction checks did not establish compliance with this modeling intent. Performance-model validity and design-variable assignment are separate problems; fixing one does not automatically fix the other.

## Exposure and interpretation

[OWNER] The owner described the actionable findings as limited: the supported conditions were insufficient for the attempted transfer, and investigation revealed modeling defects against the intended paradigm. The owner requested a results note and a new branch from before reveal.

[INHERITED: original execution report at `829539f5`] The reveal process read and extracted the four reference papers, selected inputs and transcribed comparison quantities. Thus the information exposure was broader than the small set of findings motivating repairs. A fresh agent using only this note and pre-reveal code can limit further reference influence, but its repair task was still selected after reveal.

[AGENT, recommendation ratified by the owner's instruction to branch] Preserve the first experiment and develop repairs from a pre-reveal code baseline. Document future changes and their basis. Any later ARIES comparison is a post-reveal comparison, not a restored first blind test. No claim of an immaculate original blind is made; earlier protocol disclosures also remain part of the experiment's history.

## Code baseline and preserved evidence

- Repair baseline: `86712a0d080d745802c1bcc57a30d3eca00458c3`, the verified C0 checkpoint immediately before reveal.
- Reveal authorization: `5b7bd83bd5dc747cfc5fa807ea58ff505f7b82b2`.
- Original failed attempt: `b2a860d7dfe3360c17ff5c62be3fb986bc28b17c`.
- Completed experiment and final checkpoint index: `829539f5`, preserved on branch `evidence/aries-r3-comparison-20260920` when the repair branch was created.
- Repair branch: `fix/modeling-intent-after-reveal`.

The completed report, journal, decisions, reviews and replay instructions exist at commit `829539f5` under `.project/active/aries-comparison-preparation/current-readiness/revealed-results/`. For example, retrieve the report with `git show 829539f5:.project/active/aries-comparison-preparation/current-readiness/revealed-results/report.md`. These post-reveal files need not be copied into the repair branch to preserve them.

The restored baseline contains protocol and project-status text saying the holdout is sealed. That text describes the historical checkpoint. It does not reverse the September 20 reveal or certify this repair effort as unexposed. This note records the actual sequence without rewriting the historical checkpoint or the original result.

This note records the outcome and repair starting point. It does not prescribe a solver architecture, authorize arbitrary changes to performance ranges, or constitute a new numerical comparison.
