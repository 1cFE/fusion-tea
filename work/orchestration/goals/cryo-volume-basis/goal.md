# Goal: cryo-volume-basis — should the winding-pack cold volume be computed rather than held?

Drafted 2026-08-26 by a grounding session working from the repository. Procedure is `work/orchestration/GOAL_RUNBOOK.md` § Grounding a goal; this file does not restate it.

Provenance vocabulary is the shaping register: `[AGENT]` for anything this session or the operator supplied, `[INHERITED: <path>]` for anything carried from a repository artifact. The operator acts under delegated authority, so nothing here is `[OWNER]`. Two items below carry a genuine owner grade because a repository artifact records the owner deciding them, and they are marked at their point of use.

## Status

`draft`

§ Grounding evidence is non-empty, so the evidence bar is met on its face. The status stays `draft` because the runbook makes the change the operator's, not the drafting session's: "Change to `grounded` only when the operator agrees the evidence is there." Four sections below — § Consumer, § Answered when, § Reserved gates, § Close rule — carry agent proposals that need the operator's answer before they mean anything. **A draft goal authorizes no task**, so nothing runs until that answer lands.

## Question

Should `vol_cold_cryo` be computed from the ampere-turns the model already carries plus DI-010's `J_eng`, instead of held? `[AGENT]` — the operator's question, verbatim, 2026-08-26.

It restates discovery row `20260823-magnet-technology-ab#2`, whose own wording is: "The model already computes the coil ampere-turns (Ampère's law in the magnet-cost calc), and DI-010 gives the engineering current density per conductor; volume should follow from the two." `[INHERITED: exploration/stellarator_e2e/studies/20260823-magnet-technology-ab/record.md@e204aee7 § 15]`

## Consumer

**Needs the operator.** See question 2 in the handback.

The repository supports one reading and this session proposes it, unconfirmed: the consumer is the MFE cost-modeling epic (`work/backlog/epic-mfe-cost-modeling.md@f22bd288`, `Status: active`), and the answer decides whether a modeling work item is opened under it to make the cold volume a computed quantity. The discovery row already names that destination — "modeling item under the MFE cost modeling epic (cold volume from kA·m and J_eng); unrouted" — so the row's disposition is what the answer changes. `[INHERITED: exploration/stellarator_e2e/studies/DISCOVERY_LOG.md@31f9eb0b:20]`

A second consumer is plausible and this session cannot confirm it: any future magnet-technology A/B study, which today has to hold a per-arm cold volume that is exact at only one point of its own sweep.

## Answered when

**Needs the operator.** See question 3 in the handback.

This session's proposal, unconfirmed, in the shape the runbook asks for — concrete enough that two people would read it the same way:

> The goal is answered when the trail carries a decision, with its reasoning, on whether `vol_cold_cryo` becomes a computed output of the model; and, if the decision is yes, when a modeling work item has landed the computation with the Stellaris design point reproduced inside a stated tolerance, and discovery row `20260823-magnet-technology-ab#2` carries a disposition that is not `unrouted`.

A "no" is a first-class answer here and would end the goal the same way — the runbook's `BOUNDED_NEGATIVE`. The evidence in § Grounding evidence is enough to make a "no" a real possibility rather than a formality, so the answered-when condition must not presume the change lands.

## Invariants

What a comparison must preserve for results from different rounds to mean the same thing.

- **Package.** The comparison baseline is the sealed package `exploration/stellarator_e2e/pkg/stellarator_tea` — the committed alias of `exploration/stellarator_e2e/generated`, at the version study `20260823-magnet-technology-ab` ran against (`repo_commit` `317b5bcd18df454a884a896c7dbe2531866b7622`, indicator-input fingerprint `00badf7f…9c2141`). `[INHERITED: exploration/stellarator_e2e/studies/20260823-magnet-technology-ab/snapshot.json@e204aee7]` Any round that regenerates the package promotes a new pin, and the runbook bounds a round at one promoted pin.
- **The twin.** The models have two byte-identical homes: canonical `models/library/` and `models/designs/`, and the exploration twin `exploration/stellarator_e2e/models/`. `tests/models/test_model_family_spines.py` fails on any byte difference. A model change that lands in one home and not the other is a broken invariant, not a partial result. `[INHERITED: exploration/stellarator_e2e/STAGED_MODELS.md@ba5c9945]`
- **Comparison — what "better" means.** Results are read as LCOE plus the five viability verdicts (`net_positive`, `recirc_ok`, `beta_ok`, `wall_load_ok`, `tbr_ok`, `models/library/analyses/mfe_viability.sysml`). The cold volume reaches all of them only through one channel: `vol_cold_cryo` → cryoplant heat load → cryoplant electrical → the power balance → `rec_frac` and `p_net` (`models/designs/generic_mfe/mfe_plant.sysml@ba5c9945:265-280`; `models/library/analyses/mfe_cryo_plant.sysml@8f3b510c`). A round that widens that channel — coil thickness into the radial build, for instance — has changed what "better" means and closes on the runbook's trigger 3.
- **Held equal across arms, and to be held equal across rounds unless the operator rules otherwise.** `f_carnot_cryo` at 0.20, `q_nuc_cryo` at 35.5 W/m³, the coil markup at 5.87, `p_tf` at 0, and the geometry (`R` 12.7 m, `a` 1.3 m). DI-009 puts large-cryoplant fraction-of-Carnot at 0.22–0.30, so the held 0.20 sits below the sourced band, and DI-009's own model implication is that a re-basing "should be applied to all arms at once." `[INHERITED: knowledge/KNOWLEDGE.md@ffa5c54c DI-009]` Moving it inside this goal would move every comparison in it.
- **The axis rule.** `modeling_project/STUDY_POLICY.md@ad2fb4ea § 2` rule 1: "Sweep axes are causal design levers only … Never a quantity any calc in the package computes." This is the invariant with teeth for this goal. If `vol_cold_cryo` becomes computed, it **retires as a settable input** and can no longer be an arm-definition value. Study `20260823-magnet-technology-ab` defines its two arms partly by that value (`study.py:44-47`), so a computed volume makes that study's arms non-reproducible as written. That is a comparison-meaning change the operator should see before, not after, a round runs.

## Grounding evidence

Tracked artifacts cited `<path>@<commit-sha>`.

**The finding, and its full statement.**

- `exploration/stellarator_e2e/studies/DISCOVERY_LOG.md@31f9eb0b:20` — row `20260823-magnet-technology-ab#2`, disposition `unrouted`, home "modeling item under the MFE cost modeling epic". The row is a sighting; nothing has appended under the id since.
- `exploration/stellarator_e2e/studies/20260823-magnet-technology-ab/record.md@e204aee7` — § 15 finding `#2` (the full statement and why it was held), § 2 (the 390 m³ derivation), § 14 (the pre-execution critique that corrected an earlier 749 m³), and the 2026-08-23 certification addendum (the headline's sensitivity to the held volume, quantified).

**What the model does today.**

- `models/library/analyses/mfe_magnet_cost.sysml@8f3b510c` — `'Magnet Coil Cost'` computes `total_kAm = G * B * R0 * r_coil / (mu0 * 1000.0)`, sourced to 1costingFE `cas22.py:427`. This is the "ampere-turns the model already carries."
- `models/designs/stellarator_09/stellarator_plant.sysml@ba5c9945:570` — `vol_cold_cryo = 136.56` is a bound input, doc-commented `(COMPUTED)` in the sense that a human computed it from Stellaris geometry (six winding-pack cross-sections × 8 occurrences × 25 m circumference), not that the model computes it. Its doc comment names its own weak link: per-coil circumferences are not printed in the source.
- `models/designs/generic_mfe/mfe_plant.sysml@ba5c9945:265-280` — `vol_cold_cryo` is a plain attribute feeding `calc cryo_elec : 'Cryoplant Electrical Power'`.
- `models/library/analyses/mfe_cryo_plant.sysml@8f3b510c` — the chain the volume feeds: `p_elec = p_cold / COP + p_direct`.
- `work/completed/20260718_WI-024_recirc-power-derivation@72f7d054` — the item that built this chain and made these seven parameters the concept's cryo interface.

**The current density, and its authority.**

- `knowledge/KNOWLEDGE.md@ffa5c54c` DI-010 — Nb₃Sn winding-pack `J_eng` 14.6–28 A/mm² at 12 T class against Stellaris REBCO 112–124 A/mm² at 20 K; 4–8× cold volume at equal ampere-turns. Its model implication states the change this goal asks about, and conditions it: the larger volume "should enter `vol_cold_cryo` … once the EPFL source is ingested; holding the REBCO volume flatters LTS."
- `knowledge/sources/eu_demo_rw_tf_coil_conductor_dematte_bruzzone/output.md@ffa5c54c`, registered at `knowledge/SOURCE_INDEX.md:206-216` — **the EPFL source is ingested.** DI-010's stated condition is met.

**A check this session ran, and what it found.** `[AGENT]`

Dividing the model's own `total_kAm` at the Stellaris design point by DI-010's REBCO band does **not** reproduce the held 136.56 m³. With `G = 78.95683520871486`, `B = 9.0` T, `R0 = 12.7` m, `r_coil = 3.0` m and `mu0 = 1.25663706212e-6` (all read from the two files cited above), `total_kAm = 2.1545e7` kA·m, and `total_kAm × 1000 / J_eng` gives 192.4 m³ at 112 A/mm², 182.6 m³ at 118, and 173.8 m³ at 124 — 27 % to 41 % above the geometric value. Reproducing 136.56 m³ would need `J_eng = 157.8` A/mm², outside DI-010's sourced 112–124 band.

So the two quantities the question proposes to multiply together are not, as they stand, the same physical quantity: `G * B * R0 * r_coil / mu0` is a cost proxy whose geometry factor `G = 8π²` is a stellarator family constant, not a measured conductor length. This does not answer the question either way — a form factor calibrated at the design point, or a different ampere-turn expression, are both live routes — but it means "the identity already holds, just wire it up" is not one of the available answers. It is question 1 in the handback.

**The rules the work would run under.**

- `modeling_project/STUDY_POLICY.md@ad2fb4ea` § 2 rule 1 (computed quantities are not sweep axes), § 3 (the guard pattern — physics lives once, an assert only compares two things the calc already computed), § 4 R1 (the coil-thickness ⇄ radial-build ⇄ field loop, which is discovery row `#3`, adjacent to this goal and explicitly *not* inside it unless the operator says otherwise).
- `work/backlog/epic-mfe-cost-modeling.md@f22bd288` — the named home; `Status: active`, MR-3 constraint restated there (library concept-agnostic, concept values in `designs/`). A per-conductor `J_eng` is a concept-specific value and belongs in `designs/`, not in the library calc.
- `work/completed/20260822_WI-030_computed-beta-peak-field@ffa5c54c` — the precedent for exactly this move: a quantity that was a typed-in input (beta) became computed, with a verification record against the source's printed value. Whatever tolerance and cross-check shape that item used is the shape a `vol_cold_cryo` item should be argued against.

**The seam that will bite.** `GOAL_RUNBOOK.md § The native seams` — `integrate` has no native tracked procedure and **no documented hand pattern anywhere in the repository**. Any round of this goal that lands a model change will then need a regenerated, verified, pinned package before a study can run against it, and the runbook is explicit that this is a `PREREQUISITE` return handed to the operator, never an improvised procedure. This is a structural fact about how far a round of this goal can get, and it is question 5 in the handback.

## Limits

Restated explicitly. These are the runbook defaults; nothing is inherited silently. The operator may tighten or loosen any of them (question 4).

| Limit | This goal |
|---|---|
| Retry cap | 2 retries (3 attempts) |
| Checkpoint revision cap | 2 revisions (3 submissions) |
| Round limit | 6 rounds |
| Time or iteration limit | none |

## Reserved gates

**Needs the operator.** See question 5 in the handback. The runbook's always-owner-held set applies regardless of what the operator adds: merge, push, work-item close, and archive.

This session's proposal for the goal-specific gates, unconfirmed:

1. **Promoting a pin.** The `integrate` seam is unrepaired, so any regeneration-and-pin is a `PREREQUISITE` return to the operator, not a task the round completes.
2. **Retiring `vol_cold_cryo` as a settable input.** It is an arm-definition value of a committed study (§ Invariants, the axis rule). Making it computed changes what that study's arms mean.
3. **Re-basing `f_carnot_cryo` from 0.20.** DI-009 says a re-basing applies to all arms at once, so it moves every comparison in this goal.
4. **Minting a DI, or amending DI-010.** The research seam is also unrepaired; the runbook's hand pattern (WI-031) mints DIs at work-item close.
5. **Widening scope to discovery row `#3`** (coil thickness / radial build / stress, policy § 4 R1). Adjacent, tempting, and a different goal.

Two decisions in this area are already on the record as the owner's and are not re-openable by a round of this goal: the REBCO peak-field ceiling of 24.9 T over the upstream 23.0 T (`[OWNER 2026-08-21]`, cited at `exploration/stellarator_e2e/studies/20260823-magnet-technology-ab/record.md@e204aee7 § 2`), and the ruling that the economic axes carry no sensitivity for this package (owner, 2026-08-22, same section).

## Close rule

**Needs the operator.** See question 6 in the handback. Owner-held by construction; this file cannot state who closes the goal or on what until the operator does.

## Amendments

None.
