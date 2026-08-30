# Goal: p-pump-fence — with `p_pump` re-based to 195 MW, where does the `recirc_ok` fence move and what happens to LCOE?

Grounded 2026-08-29 by the round-1 agent working from the repository, under the owner's Align rulings of 2026-08-29 (`.project/active/goal-integration-study-proof/spec.md@68ea5f23` § Align rulings). Procedure is `work/orchestration/GOAL_RUNBOOK.md`; this file does not restate it.

This is the **successor goal** to `p-pump-basis`, which the owner closed on 2026-08-28. `p-pump-basis` is not reopened (spec § Align ruling 1). That goal answered the *basis* question; this one takes its open tail.

Provenance vocabulary is the shaping register: `[OWNER <date>]` where the owner decided, `[AGENT]` for anything this session supplied, `[INHERITED: <path>]` for anything carried from a repository artifact.

**One grading note, stated plainly rather than buried.** § Question and § Answered when below are **agent-drafted sentences that the owner adopted verbatim** by ruling of 2026-08-29 ("use your drafts"). They are therefore `[AGENT] (adopted verbatim by owner ruling, 2026-08-29)` — owner-ratified, not owner-originated. That grading matters for how they may be challenged: an adopted agent draft is challenged by re-deriving against its recorded reasoning, where an owner-originated sentence is challenged by asking the owner. `p-pump-basis`'s § Question and § Answered when were the owner's own sentences and carry `[OWNER 2026-08-28]`; these do not, and the difference is not cosmetic.

## Status

`grounded` — 2026-08-29. `[AGENT]`

All five field classes are non-hollow (`GOAL_RUNBOOK.md` § Grounding a goal). § Grounding evidence is non-empty, which clears the mechanical tell; § Answered when, § Invariants, § Limits and § Reserved gates are filled and were checked by reading them. The check itself is recorded in `trail.md` under `## Round 1`.

Nothing here is edited in place. Corrections go in § Amendments.

## Question

> With `p_pump` re-based to 195 MW, where does the `recirc_ok` fence move, and what happens to LCOE?

`[AGENT] (adopted verbatim by owner ruling, 2026-08-29)`.

It is the open tail of discovery row `20260821-power-cycle-ab#3`, whose 2026-08-28 disposition row ends: "No verdict flips at the baseline point against the 0.5 threshold; **where the `recirc_ok` fence moves and what LCOE does still need a package run.**" `[INHERITED: exploration/stellarator_e2e/studies/DISCOVERY_LOG.md@07b82c6d:33]`

Two halves, both live and neither conditional on the other. The fence half asks where in the swept design space `recirc_ok` flips, relative to where `20260821-power-cycle-ab` put it (violated at R ≤ 8.0 m paper arm, ≤ 6.5 m upstream, ≤ 5.5 m in both η 0.47 arms, at a = 0.8 m against threshold 0.5 — `exploration/stellarator_e2e/studies/20260821-power-cycle-ab/record.md@881d4448 § 4`). The LCOE half asks what the re-basing did to the objective at the baseline point. Learning `L-003` is why the second half cannot be folded into the first: `p_th` reaches nine cost accounts directly, so `p_pump` moves capital as well as net power and an LCOE effect is not estimable from `p_net` alone.

## Consumer

Discovery row `20260821-power-cycle-ab#3`, and through it the MFE cost-modeling line of work. `[AGENT]`

The row is **not** unrouted and **not** open in the sense `p-pump-basis` found it. Its newest row (2026-08-28, scanned whole for the id per `GOAL_RUNBOOK.md` § The discovery log) reads "Row final for goal `p-pump-basis`; the WI's own record carries it from here." `[INHERITED: exploration/stellarator_e2e/studies/DISCOVERY_LOG.md@07b82c6d:35]`

**Final for that goal is not final for the row.** `[AGENT]` The 2026-08-28 rows dispose of the *basis* question, which is what `p-pump-basis` was grounded on. The sentence naming the package run as still owed is in those same rows and is not discharged by them. This round's evidence is new evidence — a regenerated package and a study against it — and a row is disposed per goal, not per repository. What the answer changes is the row's disposition again, under the same id, appended and never edited.

What the consumer does with the answer: reads whether the committed A/B study's `recirc_ok` geography and LCOE levels survive the re-based input, or whether they carry a known and now-quantified error.

## Answered when

> A committed, verified study on the regenerated, pinned package that locates the `recirc_ok` fence and quantifies the LCOE shift at the baseline point relative to the 1.0 MW record — with an adverse or inconclusive reading counting as an answer.

`[AGENT] (adopted verbatim by owner ruling, 2026-08-29)`.

Four things it settles, made explicit so two readers read them the same way. `[AGENT]`

- **A pin is required.** Unlike `p-pump-basis`, a trail-only answer does not end this goal. The contract names "the regenerated, pinned package," so the `integrate` seam must have returned a verified candidate before the study can be the answer.
- **Both halves must be addressed.** Locating the fence alone is not the contract; the LCOE shift at the baseline point, stated against the 1.0 MW record, is the other half.
- **"Relative to the 1.0 MW record" names the comparand.** That is `exploration/stellarator_e2e/studies/20260821-power-cycle-ab/record.md@881d4448`, the committed A/B run at `p_pump` = 1.0 MW. The comparison is against its published numbers at its own pin, not against a re-run of it. A re-run would be a second committed study and is barred.
- **An adverse or inconclusive reading is an answer.** If the study cannot locate the fence, or locates it somewhere that makes the question ill-posed, that closes the round and meets the contract. It does not authorize repair inside the round.

## Invariants

What a comparison must preserve for results from different rounds to mean the same thing.

- **Package.** A round runs against **exactly one promoted pin**, and this round's pin is the one the `integrate` seam returns as `CANDIDATE` for `exploration/stellarator_e2e/pkg/stellarator_tea` on WI-033's audited model (`work/completed/20260828_WI-033_p-pump-rebase/verification_record.md@83ccd8f9`). `[AGENT]` The pin is the manifest's own value, not a newly minted number. **This goal's pin is deliberately not `p-pump-basis`'s.** That goal's package invariant fixed the comparison at the study `20260821-power-cycle-ab` ran against (`repo_commit ffa5c54c…`, executable fingerprint `7447efea…`, semantic fingerprint `1ca93d0c…`). Regenerating moves all three. `[INHERITED: work/orchestration/goals/p-pump-basis/goal.md@9f0019e8 § Invariants]`

  **What that means for comparability, stated rather than assumed.** `[AGENT]` The comparison this goal makes is *across* pins by construction — 195 MW at the new pin against 1.0 MW at the old one — which is exactly the comparison `p-pump-basis`'s invariant forbade within its own rounds. It is legitimate here only because **the model delta between the two pins is known, audited, and single**: `p_pump` 1.0 → 195.0 in both homes of the twin, WI-033, with the census fixture re-derived and nothing else changed (`verification_record.md@83ccd8f9` § 1, § 5). If the regeneration turns out to carry any other semantic change, the comparison meaning has moved and the round closes on trigger 3.

- **The twin.** `models/library/` + `models/designs/` and the exploration twin `exploration/stellarator_e2e/models/` stay byte-identical; `tests/models/test_model_family_spines.py` fails on any byte difference. A change landing in one home and not the other is a broken invariant, not a partial result. `[INHERITED: work/orchestration/goals/p-pump-basis/goal.md@9f0019e8 § Invariants]`

- **Comparison — what "better" means.** LCOE plus the five viability verdicts (`net_positive`, `recirc_ok`, `beta_ok`, `wall_load_ok`, `tbr_ok`, `models/library/analyses/mfe_viability.sysml`). `[INHERITED: exploration/stellarator_e2e/studies/20260821-power-cycle-ab/record.md@881d4448 § 4]` Unchanged from `p-pump-basis`; this goal reads the same objective and the same verdicts.

- **The channel `p_pump` travels, both paths.** `[INHERITED: work/orchestration/goals/p-pump-basis/goal.md@9f0019e8 § Invariants, as amended 2026-08-28]` `p_pump` reaches the verdicts and the objective through exactly two terms of the plant power balance and nothing else — the thermal balance `p_th = mn·p_neutron + p_alpha + p_input + eta_p·p_pump` with `eta_p` = 0.5, and the recirculating sum (`models/library/analyses/mfe_power_balance.sysml:119,135`). From `p_th` it reaches **nine cost accounts directly** (`models/designs/generic_mfe/mfe_plant.sysml` lines 330, 338, 366, 405, 431, 505, 515, 526, 544), so it moves capital as well as net power (`work/orchestration/goals/p-pump-basis/learnings.md@104a68b5` L-003). A round that gives `p_pump` any other reach — a pressure-drop model, a coolant-loop component, a coupling to `a` or to wall load — has widened the channel and closed the round on trigger 3.

- **Held equal.** `eta_p` at 0.5, `f_sub` at 0.03, `p_trit` at 10.0 MW, `p_house` at 4.0 MW, `vol_cold_cryo` held per the owner's 2026-08-27 ruling, and the baseline geometry the oracle scan used. `[INHERITED: work/orchestration/goals/p-pump-basis/goal.md@9f0019e8 § Invariants]` These are the other terms of the same two sums; moving one moves every comparison in this goal at the same time as the pin moves, and the two effects would not be separable afterwards.

- **`p_pump` stays a held, settable input.** `[OWNER 2026-08-28]` Ruling 2 of the `p-pump-basis` close (`work/orchestration/goals/p-pump-basis/trail.md@07b82c6d` § Goal close). It is not a sweep axis and not a computed quantity in this goal. Making it computed retires it as a lever under `modeling_project/STUDY_POLICY.md@ad2fb4ea` § 2 rule 3, and that ruling is not this goal's to revisit.

- **Committed prior records are not touched.** `[AGENT]` `exploration/stellarator_e2e/studies/2026*` stays byte-unchanged. Their pins will no longer match the live package after the regeneration; that is expected, and each record carries its own snapshot and fingerprints. A comparison that needs the old numbers reads them out of the old record.

## Grounding evidence

Tracked artifacts cited `<path>@<commit-sha>`. Each was checked with `git log -1` at this session's HEAD (`4ac33d95`); none has moved since the sha it is cited at (`GOAL_RUNBOOK.md` § When a cited artifact moves).

**The open tail, and its authority.**

- `exploration/stellarator_e2e/studies/DISCOVERY_LOG.md@07b82c6d:33` — the 2026-08-28 disposition row under `20260821-power-cycle-ab#3`. Meaning for this goal: it is the sentence that names what is still owed ("where the `recirc_ok` fence moves and what LCOE does still need a package run"), and it names why nothing landed at the time — the value change, the shape, and the source registration were reserved gates.
- `exploration/stellarator_e2e/studies/DISCOVERY_LOG.md@07b82c6d:35` — the owner-ruled row of the same date. Meaning: the basis question is settled at 195 MW held; the row is "final for goal `p-pump-basis`" and routed to WI-033. This is what makes the present goal a successor rather than a reopening.
- `exploration/stellarator_e2e/studies/20260821-power-cycle-ab/record.md@881d4448` — § 4 (the `recirc_ok` fence per arm at 1.0 MW: violated at R ≤ 8.0 / 6.5 / 5.5 m at a = 0.8 m); § 11 (corner `rec_frac` from the oracle scan); § 13 (`p_pump` = 1.0 named as fed identically to both sides and therefore not independently verified); § 15 finding `#3`; § 17 (the five power-balance channels exported empty). Meaning: this is the comparand § Answered when names, and its § 4 numbers are the "before" side of the fence question.

**The goal that closed, and what it established.**

- `work/orchestration/goals/p-pump-basis/goal.md@9f0019e8` — closed 2026-08-28. Meaning: its § Invariants supply this goal's channel, twin, comparison and held-equal statements, carried forward explicitly rather than inherited silently. Its § Reserved gates 5 (widening the channel) is carried too.
- `work/orchestration/goals/p-pump-basis/trail.md@07b82c6d` § Goal close — the three owner rulings of 2026-08-28. Meaning: 195 MW held is the mandate, ~130 MW is the documented lower bound, and package regeneration was explicitly deferred to GSTH Item 6.
- `work/orchestration/goals/p-pump-basis/trail.md@07b82c6d:522-527` — "Constraints carried into round 2, if the owner opens it." Meaning, and it is the sharpest input this goal has: (i) landing a value makes the committed package stale, and a fence study needs a regenerated, verified, pinned package; (ii) **a strategy that declares an intended study question must first check that its own goal's gates leave it reachable inside one round** — the previous round did not, and that is the failure this goal is shaped to avoid; (iii) the `rec_frac` half is answerable without a pin by L-002's recipe, the LCOE half is not, by L-003.
- `work/orchestration/goals/p-pump-basis/learnings.md@104a68b5` — L-001 (the ~4–6 % helium-primary subset, and that a number quoted to better than one significant figure is false precision), L-002 (`rec_frac` and `p_net` are recoverable post hoc from a committed record when every other recirculating term is bound), L-003 (`p_th` reaches nine cost accounts, so LCOE needs a package run). Meaning: L-003 is why this goal's contract requires a pin at all; L-002 is a cross-check available on the fence half without one.

**What the model carries now, and what the packages carry.**

- `work/completed/20260828_WI-033_p-pump-rebase/verification_record.md@83ccd8f9` — the audited item that landed 195.0. Meaning: the model change is done, audited and archived; its § "Owner-sequenced next steps" states plainly that "the model (195.0) intentionally diverges from every committed package (1.0) and `scripts/integrate.py` refusing a stale package is the designed detection." That divergence is the premise of this round's first task.
- `models/designs/stellarator_09/stellarator_plant.sysml@ffb22724` — `p_pump = 195.0` MW, held, with the MR-WI033-2 doc comment. Meaning: the model side of the divergence.
- `exploration/stellarator_e2e/generated/contracts/model_contract.json@ba5c9945` semantic fingerprint `1ca93d0c…` and `package_contract.json` executable fingerprint `7447efea…`; `exploration/stellarator_e2e/studies/manifest.json@ffa5c54c`. Meaning: the package side of the divergence, i.e. what the seam will be handed as the *expected* lineage on its first invocation, and what must move before a candidate can exist.

**The seam this round is the first live user of.**

- `.project/adr/009-integration-is-a-fixed-point-proof.md@1d43dc5b` — the seam proves a fixed point; it does not perform and does not commit, and a regeneration-gate refusal is a `PREREQUISITE`, the modeling item's unfinished work. Meaning: the shape of the first task's expected return, decided before it is run.
- `docs/integration_seam_operator_guide.md` — the invocation, every flag's provenance, and the blocker-condition table. Meaning: the documented pattern this round follows rather than improvises.
- `work/orchestration/GOAL_RUNBOOK.md@9f0019e8` § The native seams — the `integrate` row still reads "**pending native repair**". Meaning, and it is a live premise conflict this goal names rather than resolves: the runbook says there is no written pattern, and the repository now has one (`scripts/integrate.py`, ADR-009, the operator guide). Flipping that row is GSTH Item 6 Phase 5's job, on the evidence this round's seam invocations produce. Until it flips, this goal reads the seam's own documents as authority and says so.

**What this establishes, and what it does not.** `[AGENT]` It establishes that the question is not already answered in the repository: no committed study has ever run against a package carrying 195 MW, because no package carries it. It establishes that the fence half has a partial, pin-free cross-check (L-002) and the LCOE half has none (L-003). It does **not** establish where the fence lands, that a candidate pin is obtainable, or that comparison meaning survives the regeneration. Those are the round's to find out.

## Limits

Restated explicitly; nothing is inherited silently. These are the `GOAL_RUNBOOK.md` § Limits defaults, kept exactly. `[AGENT]`

| Limit | This goal | At the cap |
|---|---|---|
| Retry cap | 2 retries (3 attempts) | The task ends as mechanical failure past cap — a blocker |
| Checkpoint revision cap | 2 revisions (3 submissions) | `### Stop` of kind `cap`; the round stops. Execution is **not** permitted |
| Round limit | 6 rounds | The goal is re-grounded with the owner, or closed |
| Tasks per round | none | Already bounded by one promoted pin, one committed study, and mandatory close after a valid reading |

**No time limit is declared.** `[AGENT]` `GOAL_RUNBOOK.md` § Limits has no such row and this session does not invent one.

## Reserved gates

**The general rule, above every named instance:** merge, push, work-item close and archive are owner-held per the runbook, and any model or knowledge mutation beyond this goal directory needs owner sign-off. `[AGENT]`

The four below are the owner's Align ruling 4 of 2026-08-29, carried in as stated. `[OWNER 2026-08-29]` `[INHERITED: .project/active/goal-integration-study-proof/spec.md@68ea5f23 § Align rulings 4]`

1. **The goal grounding wording** — § Question and § Answered when. Supplied by the owner on 2026-08-29 (adopted verbatim from agent drafts; see the grading note at the top of this file). Discharged for this goal; a *re-grounding* would need the gate again.
2. **The goal close ruling.** The review recommends; the owner closes.
3. **Push, PR, merge.**
4. **Any ruling an adverse or inconclusive study reading requests.** The round closes on the reading regardless — repair is next-round's work, never this round's.

A fifth, from the study layer's own contract rather than the Align ruling, and gated all the same: `[INHERITED: .claude/skills/run-study/runbook.md step 4; .claude/skills/run-study/SKILL.md § Three roles]`

5. **The study framing ruling.** The owner rules on the framing — the axes, and any axis the model turns out not to resist — after indicators run and before any point runs. An unruled framing stops the study. This is the study layer's native gate, not a new goal-level one, and it is named here so a reader of `goal.md` can see every place execution can stop.

Two rulings already on the record are **not re-openable by a round of this goal:** that `p_pump` stays a held, settable input re-based to 195 MW `[OWNER 2026-08-28]`, and that `vol_cold_cryo` stays a held, settable input `[OWNER 2026-08-27]`. Widening the channel `p_pump` travels remains what it was in `p-pump-basis` — adjacent, tempting, a different goal, and a trigger-3 round close if done.

## Close rule

`[AGENT]` — this session, following the `p-pump-basis` and `cryo-volume-basis` pattern. Not an owner grade: the owner did not state this rule.

The fresh round review hands the owner a recommendation once § Answered when is met, in either direction, including on an adverse or inconclusive reading. **The owner's ruling closes the goal.** The review recommends; it does not close, and neither does the round agent.

## Amendments

None.
