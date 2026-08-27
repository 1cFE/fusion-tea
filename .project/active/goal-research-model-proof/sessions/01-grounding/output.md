`work/orchestration/goals/p-pump-basis/goal.md` is written. `trail.md` and `learnings.md` are untouched templates — grounding writes neither. No commit made.

## What I grounded

**Status is `draft`, deliberately.** § Grounding evidence is non-empty, which clears the mechanical tell, but the runbook says a goal hollow in any of the five field classes authorizes no task. The answer contract isn't settled, so I marked the goal as authorizing nothing and said why in § Status.

**Filled from the repository and your brief:** § Consumer, § Invariants, § Grounding evidence, § Limits, § Reserved gates. All operator-supplied content is `[AGENT]`; repository-carried content is `[INHERITED: path@sha]`. Two items carry a real `[OWNER <date>]` because a committed artifact records the owner deciding them (the economic-axes ruling, the `vol_cold_cryo` ruling).

**§ Invariants** states the channel (`p_pump` → the two power-balance terms at `mfe_power_balance.sysml:119,135` → `rec_frac`/`p_net` → verdicts and LCOE) and the equal-input/unequal-effect distinction with the fence radii and per-arm fractions, then stops. It says explicitly that whether comparison meaning survives is a round's judgment, not grounding's.

**Three things I checked that the brief didn't hand me:**

1. **No external mutation.** All three cited shas are the latest commit touching their path. Same for every model path I cite.
2. **The sourced figures are less available than DI-008 reads.** Cismondi and ARIES-ACT are ingested inside concept dossiers but **not registered in `SOURCE_INDEX.md`**; Moscato — the only helium-primary *pumping-system design* in the set — is an open PDF, not in the repository. The `research` seam is unrepaired, so registering a source or amending a DI runs the WI-031 hand pattern.
3. **A band discrepancy.** DI-008 says "~60–190 MW for Stellaris"; the research file it was minted from says the same three sources "bracket 30–190 MW." Which band applies decides whether ARIES-ACT's ~1 % is inside the sourced range. Amending a DI is a reserved gate, so I recorded it rather than resolving it (question 2 below).

I also recorded one arithmetic check from the study's own oracle scan: 2–6 % of the back-derived ~3240 MWth is 65–194 MW, against a whole existing recirculating sum of ~163 MW (paper arm) / ~177 MW (η 0.47). The re-basing is of the same order as everything already in the sum. I stated explicitly what that does *not* establish — it's five oracle points, it ignores the `eta_p·Δp_pump` feedback, and `rec_frac` has no per-point package evidence at all (finding `#10`). It rules out "negligible, leave it held" as an answer available without measuring. It settles nothing else.

## Questions for the owner

1. **§ Question — which question ends the goal?** Your sentence carries two. "Is 1.0 MW defensible?" can end on a reasoned no with the value still held. "What sourced value should the model carry?" ends only on a value or on a finding that no admissible one exists. Give me the one sentence you want in § Question.

2. **DI-008's band — 60–190 MW or 30–190 MW?** DI-008 and its source research file disagree. Does this goal work against DI-008 as written, or is reconciling the two part of its work?

3. **§ Answered when — scalar or fraction?** DI-008's basis is a *fraction of blanket thermal power*, and `p_th` is computed and moves with swept geometry. A re-based scalar in MW is a value change. A fraction of `p_th` retires `p_pump` as a settable input (reserved gate 2) and is algebraically self-referential, since `p_th` already contains `eta_p·p_pump`. Does § Answered when require a specific shape, or is choosing the shape the goal's work?

4. **Does the answer have to land in the model, or only in the trail?** The `cryo-volume-basis` precedent closed with the value still held and the row dispositioned. Is "1.0 MW stays, optimism disclosed, reversal condition recorded, row not `unrouted`" a complete answer here — and does the goal mint a work item under the MFE Cost Modeling epic, or is minting itself a gate?

5. **§ Close rule — who closes, on what?** The precedent had the owner close on the fresh round review's recommendation. I won't write an owner's rule from a precedent. State it.