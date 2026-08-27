# Goal: cryo-volume-basis — should the winding-pack cold volume be computed rather than held?

Drafted 2026-08-26 by a grounding session working from the repository. Procedure is `work/orchestration/GOAL_RUNBOOK.md` § Grounding a goal; this file does not restate it.

Provenance vocabulary is the shaping register: `[AGENT]` for anything this session or the operator supplied, `[INHERITED: <path>]` for anything carried from a repository artifact. The operator acts under delegated authority, so nothing here is `[OWNER]`. Two items below carry a genuine owner grade because a repository artifact records the owner deciding them, and they are marked at their point of use.

## Status

`grounded` — 2026-08-26. `[AGENT]`

§ Grounding evidence is non-empty and the operator has agreed it is there. § Consumer, § Answered when, § Limits, § Reserved gates and § Close rule are the operator's answers of 2026-08-26, not agent proposals. Nothing in this file is edited in place from here; corrections go in § Amendments.

## Question

Should `vol_cold_cryo` be computed from the ampere-turns the model already carries plus DI-010's `J_eng`, instead of held? `[AGENT]` — the operator's question, verbatim, 2026-08-26.

It restates discovery row `20260823-magnet-technology-ab#2`, whose own wording is: "The model already computes the coil ampere-turns (Ampère's law in the magnet-cost calc), and DI-010 gives the engineering current density per conductor; volume should follow from the two." `[INHERITED: exploration/stellarator_e2e/studies/20260823-magnet-technology-ab/record.md@e204aee7 § 15]`

## Consumer

The MFE cost-modeling epic (`work/backlog/epic-mfe-cost-modeling.md@f22bd288`, `Status: active`). The answer decides whether a modeling work item opens under it to make the cold volume a computed quantity, and how discovery row `20260823-magnet-technology-ab#2` is dispositioned. `[AGENT]` — operator, 2026-08-26, confirming this session's reading.

The row already names that destination — "modeling item under the MFE cost modeling epic (cold volume from kA·m and J_eng); unrouted" — so the row's disposition is what the answer changes. `[INHERITED: exploration/stellarator_e2e/studies/DISCOVERY_LOG.md@31f9eb0b:20]`

## Answered when

`[AGENT]` — operator, 2026-08-26.

> The goal is answered when the trail carries a decision, with its reasoning, on whether `vol_cold_cryo` becomes a computed output of the model — **and the two directions end the goal on the same terms**:
>
> - **Yes** — a modeling work item has landed the computation, reproducing the Stellaris anchor (136.56 m³, `models/designs/stellarator_09/stellarator_plant.sysml@ba5c9945:570`) within a tolerance the item states; and discovery row `20260823-magnet-technology-ab#2` carries a disposition that is not `unrouted`.
> - **No, keep it held** — the recorded reasoning stands as the answer, and row `#2` carries a disposition that is not `unrouted`.

The tolerance number is the modeling item's to state, not this goal's. The goal requires only that one is stated. `[AGENT]` — operator, 2026-08-26.

A reasoned "no" is a first-class answer, the runbook's `BOUNDED_NEGATIVE`. § Grounding evidence makes it a real possibility rather than a formality, so nothing here presumes the change lands.

## Invariants

What a comparison must preserve for results from different rounds to mean the same thing.

- **Package.** The comparison baseline is the sealed package `exploration/stellarator_e2e/pkg/stellarator_tea` — the committed alias of `exploration/stellarator_e2e/generated`, at the version study `20260823-magnet-technology-ab` ran against (`repo_commit` `317b5bcd18df454a884a896c7dbe2531866b7622`, indicator-input fingerprint `00badf7f…9c2141`). `[INHERITED: exploration/stellarator_e2e/studies/20260823-magnet-technology-ab/snapshot.json@e204aee7]` Any round that regenerates the package promotes a new pin, and the runbook bounds a round at one promoted pin.
- **The twin.** The models have two byte-identical homes: canonical `models/library/` and `models/designs/`, and the exploration twin `exploration/stellarator_e2e/models/`. `tests/models/test_model_family_spines.py` fails on any byte difference. A model change that lands in one home and not the other is a broken invariant, not a partial result. `[INHERITED: exploration/stellarator_e2e/STAGED_MODELS.md@ba5c9945]`
- **Comparison — what "better" means.** Results are read as LCOE plus the five viability verdicts (`net_positive`, `recirc_ok`, `beta_ok`, `wall_load_ok`, `tbr_ok`, `models/library/analyses/mfe_viability.sysml`). The cold volume reaches all of them only through one channel: `vol_cold_cryo` → cryoplant heat load → cryoplant electrical → the power balance → `rec_frac` and `p_net` (`models/designs/generic_mfe/mfe_plant.sysml@ba5c9945:265-280`; `models/library/analyses/mfe_cryo_plant.sysml@8f3b510c`). A round that widens that channel — coil thickness into the radial build, for instance — has changed what "better" means and closes on the runbook's trigger 3.
- **Held equal across arms, and to be held equal across rounds unless the operator rules otherwise.** `f_carnot_cryo` at 0.20, `q_nuc_cryo` at 35.5 W/m³, the coil markup at 5.87, `p_tf` at 0, and the geometry (`R` 12.7 m, `a` 1.3 m). DI-009 puts large-cryoplant fraction-of-Carnot at 0.22–0.30, so the held 0.20 sits below the sourced band, and DI-009's own model implication is that a re-basing "should be applied to all arms at once." `[INHERITED: knowledge/KNOWLEDGE.md@ffa5c54c DI-009]` Moving it inside this goal would move every comparison in it.
- **The axis rule.** `modeling_project/STUDY_POLICY.md@ad2fb4ea § 2` rule 1: "Sweep axes are causal design levers only … Never a quantity any calc in the package computes." This is the invariant with teeth for this goal. If `vol_cold_cryo` becomes computed, it **retires as a settable input** and can no longer be an arm-definition value. Study `20260823-magnet-technology-ab` defines its two arms partly by that value (`study.py:44-47`), so a computed volume makes that study's arms non-reproducible as written. That is a comparison-meaning change the operator should see before, not after, a round runs.

## Grounding evidence

## Limits

Restated explicitly. These are the runbook defaults, kept exactly, by operator decision of 2026-08-26. `[AGENT]` Nothing is inherited silently.

| Limit | This goal |
|---|---|
| Retry cap | 2 retries (3 attempts) |
| Checkpoint revision cap | 2 revisions (3 submissions) |
| Round limit | 6 rounds |
| Time or iteration limit | none |

The round limit is deliberately **not** tightened: this goal ends on its gates and its answer, not on a countdown, and a tighter limit would manufacture a close the evidence did not earn. `[AGENT]` — operator, 2026-08-26.

## Reserved gates

**The general rule, above every named instance:** merge, push, work-item close and archive are owner-held per the runbook, and **any model or knowledge mutation beyond this goal directory needs owner sign-off**. `[AGENT]` — operator, 2026-08-26.

The five below are named instances of that rule, not a closed list. An unnamed mutation is still gated. `[AGENT]` — operator, 2026-08-26.

1. **Promoting a pin.** The `integrate` seam is unrepaired, so any regeneration-and-pin is a `PREREQUISITE` return to the operator, not a task the round completes. Confirmed by the operator, 2026-08-26, as the ceiling this goal runs under.
2. **Retiring `vol_cold_cryo` as a settable input.** It is an arm-definition value of a committed study (§ Invariants, the axis rule). Making it computed changes what that study's arms mean.
3. **Re-basing `f_carnot_cryo` from 0.20.** DI-009 says a re-basing applies to all arms at once, so it moves every comparison in this goal.
4. **Minting a DI, or amending DI-010.** The research seam is also unrepaired; the runbook's hand pattern (WI-031) mints DIs at work-item close.
5. **Widening scope to discovery row `#3`** (coil thickness / radial build / stress, policy § 4 R1). Adjacent, tempting, and a different goal.

Two decisions in this area are already on the record as the owner's and are not re-openable by a round of this goal: the REBCO peak-field ceiling of 24.9 T over the upstream 23.0 T (`[OWNER 2026-08-21]`, cited at `exploration/stellarator_e2e/studies/20260823-magnet-technology-ab/record.md@e204aee7 § 2`), and the ruling that the economic axes carry no sensitivity for this package (owner, 2026-08-22, same section).

## Close rule

The owner closes this goal, on the fresh round review's recommendation, once § Answered when is met in either direction. The operator may recommend close; the close itself is owner-held. `[AGENT]` — operator, 2026-08-26.

## Amendments

None.
