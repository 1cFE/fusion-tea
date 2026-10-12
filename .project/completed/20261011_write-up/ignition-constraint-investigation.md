# Item 1: what the ignition constraint actually establishes

Date: 2026-09-29. Examined checkout: `55cc001c2`, current model text, historical study records, and the original Stellaris paper. [AGENT] Findings and recommendations below; owner resolution remains open. This is a focused investigation for the write-up, not plant qualification or a new study run.

## Finding

The implemented constraint permits exact ignition. It rejects a negative required auxiliary heating power at a prescribed operating point. This is defensible as a check that the modeled steady-state power balance can close using the available auxiliary heating. It does not establish that an actual plant is controllable, or that excluded designs cannot operate with other settings or control mechanisms.

The original passage compresses three different things into “ignited plasmas the model had no way to control”: excess self-heating at a selected point, an ignited equilibrium, and dynamic controllability. The study's historical label “ignited” contributes to the confusion: it means strictly negative required auxiliary heating, whereas exact zero passes the new constraint.

## Evidence

1. **The arithmetic checks both ends of the heating range.** The model calculates `P_aux_required = P_radiation + W/tau_E − P_alpha_heat`. The existing upper check requires this demand to be no larger than installed coupled heating; WI-043 added `P_aux_required >= 0`. Zero passes both. See [balance definition](../../../../models/library/analyses/mfe_plasma_sustainment.sysml), [constraint definitions](../../../../models/library/analyses/mfe_viability.sysml:368), and [plant bindings](../../../../models/designs/stellarator_09/stellarator_plant.sysml:2406).

2. **The quoted count concerns sampled operating points.** The stored-energy study reports 7,712 evaluated points, of which 1,839 pass its nine existing checks. Of those, 1,113 have negative required heating and 726 have nonnegative required heating. The count aggregates four study arms, including different installed heating levels; it should be described as sampled points, not 1,839 distinct plant designs. See [definitions and count table](../../../../exploration/stellarator_e2e/studies/20260905-stored-energy-basis/synthesis.md:45).

3. **The source explicitly intends ignition.** Table 5 of the original Stellaris paper gives Point A zero operating auxiliary heating and infinite fusion gain. The same page discusses additional burn control for thermally unstable points, including changes to confinement and tritium fraction. Verified against the [retained page image](../../../../work/orchestration/goals/stellaris-plasma-power-balance/evidence/source-pages/stellaris-p10.png) and the [original paper, p. 10](https://publikationen.bibliothek.kit.edu/1000179851/172386752#page=10). Our model does not quantify these control mechanisms.

4. **The historical rationale knew this distinction, but overstated control capability.** The [burn-control goal](../../../../work/orchestration/goals/burn-control/goal.md) explicitly says its lower bound is not a physics limit on ignition. It considered density changes and higher-temperature equilibria before choosing the restriction. However, saying positive heating demand means a point “can be held” assumes suitable heating feedback. The code checks a static power range; it does not demonstrate a controller's response, margins, or stability. The probe calculates finite-difference slopes and searches static roots, rather than simulating a controlled transient; see [probe](../../../../work/orchestration/goals/burn-control/evidence/grounding_probe/probe.py:145).

5. **An early stability generalization was already corrected.** The original grounding extrapolated from nine probe points to the full operating window. Later investigation found rising-branch driven points; the goal amendment and current model comment narrow that claim. This does not invalidate the nonnegative-heating bound, whose justification is the balance equation. It limits what we should claim about the broader control investigation. See the [goal amendments](../../../../work/orchestration/goals/burn-control/goal.md) and [current explanation](../../../../models/library/analyses/mfe_viability.sysml:416).

6. **Reproducing the source's ignition remains a separate unresolved issue.** The later plasma-balance reconciliation found 44.0038 MW of required auxiliary heating at the Table 5-conditioned point and did not reproduce published ignition. It explicitly checked that zero is admitted by both predicates. Removing the lower bound would not resolve this positive-demand discrepancy. See [reconciliation answer](../../../../work/orchestration/goals/stellaris-plasma-power-balance/answer.md:3).

The independent historical investigation also located an explicit warning in the original review: the slope calculation re-converges helium ash at every temperature, so it is not a linearised thermal-stability derivative with composition held fixed. The review specifically disallows conclusions about closed-loop dynamics or whether a driven point is held. See [review finding F4](../../../../work/orchestration/goals/burn-control/evidence/T-003_precritique.md:64). This strengthens the recommendation to remove the control claim rather than merely soften its wording.

## Recommended characterization

[AGENT] Describe the improvement as catching operating points whose power balance did not close under the represented physics and controls. Retain the count as a historical result, with its sampled-point meaning. Acknowledge that the agents addressed the missing coverage by restricting the accepted operating points; they did not build burn control or establish that ignited stellarators are infeasible.

[AGENT] Proposed replacement, for discussion:

> **Check that operating points balance.** In one sweep, 1,113 of the 1,839 points passing the existing checks produced more plasma self-heating than the modeled losses could remove at their selected temperature and density. A new power-balance check marked those points as failing. Ignition itself is an intended condition in Stellaris; evaluating those points with burn control would require mechanisms our model did not represent.

[OWNER] Follow-up: the points are marked as not passing, rather than excluded. Asked whether the check includes margin for error or relaxation. [AGENT] The study retains the cases and their verdicts. The lower bound is a literal `>= 0.0`, with no uncertainty allowance. It checks a range of permissible auxiliary heating, not whether every sample lands exactly on zero: a computed requirement between zero and installed capacity passes. The original review found no exact-zero cases and a minimum absolute required heating of about 0.119 MW over all 7,712 cases ([F5](../../../../work/orchestration/goals/burn-control/evidence/T-003_precritique.md:74)). Numerical verification tolerances compare implementations; they do not relax this physical predicate. Model uncertainty near the boundary remains a separate assessment, not an implemented margin.

## Suggested resolution scope

- [AGENT] Correct the write-up first. The present evidence supports retaining the nonnegative-demand check, described as a necessary power-balance condition within the model's scope.
- [AGENT] Consider a small follow-up to the model documentation and reporting vocabulary: describe the check as power-balance admissibility; identify negative demand as excess self-heating at the prescribed point; qualify claims that a passing point can be held by feedback. Preserve historical records and explain their labels when citing them.
- [AGENT] A study repair would be warranted if the intended claim is performance or economics of an ignited, controlled Stellaris plant. That requires selecting consistent equilibrium points and representing the relevant control assumptions, alongside the unresolved source-balance discrepancy. Changing or deleting this inequality alone would not supply that evidence.

Decision: [AGENT] Recommendation ratified by owner on 2026-09-29: correct the characterization, retain the constraint without relaxation, and say points are marked as failing under the model's assumptions. [OWNER] Points remain in the results rather than being excluded. Article edit pending; no model equations, predicates, or study results changed.
