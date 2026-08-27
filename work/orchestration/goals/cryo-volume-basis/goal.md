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

So the two quantities the question proposes to multiply together are not, as they stand, the same physical quantity: `G * B * R0 * r_coil / mu0` is a cost proxy whose geometry factor `G = 8π²` is a stellarator family constant, not a measured conductor length. This does not answer the question either way — a form factor calibrated at the design point, a different ampere-turn expression, and "the gap is itself the reason to keep the value held" are all live routes. What it rules out is one answer: "the identity already holds, just wire it up."

Choosing among those routes is the goal's own work and is deliberately not settled here. `[AGENT]` — operator, 2026-08-26.

**The rules the work would run under.**

- `modeling_project/STUDY_POLICY.md@ad2fb4ea` § 2 rule 1 (computed quantities are not sweep axes), § 3 (the guard pattern — physics lives once, an assert only compares two things the calc already computed), § 4 R1 (the coil-thickness ⇄ radial-build ⇄ field loop, which is discovery row `#3`, adjacent to this goal and explicitly *not* inside it unless the operator says otherwise).
- `work/backlog/epic-mfe-cost-modeling.md@f22bd288` — the named home; `Status: active`, MR-3 constraint restated there (library concept-agnostic, concept values in `designs/`). A per-conductor `J_eng` is a concept-specific value and belongs in `designs/`, not in the library calc.
- `work/completed/20260822_WI-030_computed-beta-peak-field@ffa5c54c` — the precedent for exactly this move: a quantity that was a typed-in input (beta) became computed, with a verification record against the source's printed value. Whatever tolerance and cross-check shape that item used is the shape a `vol_cold_cryo` item should be argued against.

**The seam that will bite.** `GOAL_RUNBOOK.md § The native seams` — `integrate` has no native tracked procedure and **no documented hand pattern anywhere in the repository**. Any round of this goal that lands a model change will then need a regenerated, verified, pinned package before a study can run against it, and the runbook is explicit that this is a `PREREQUISITE` return handed to the operator, never an improvised procedure.

The goal runs under that ceiling. Repairing the seam is not this goal's work, and a round that lands a model change and stops at `PREREQUISITE` is an honest stop, not a failure. `[AGENT]` — operator, 2026-08-26.

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
