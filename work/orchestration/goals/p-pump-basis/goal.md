# Goal: p-pump-basis — is `p_pump` = 1.0 MW defensible for a helium-primary loop at this plant scale, and what sourced value should the model carry?

Drafted 2026-08-27 by a grounding session working from the repository. Procedure is `work/orchestration/GOAL_RUNBOOK.md` § Grounding a goal; this file does not restate it.

Provenance vocabulary is the shaping register: `[AGENT]` for anything this session or the operator supplied, `[INHERITED: <path>]` for anything carried from a repository artifact. **The operator acts under authority the owner delegated, so nothing the operator said is `[OWNER]`.** Where a repository artifact records the owner deciding something, that item carries `[OWNER <date>]` at its point of use and cites the artifact.

## Status

`draft` — 2026-08-27. `[AGENT]`

§ Grounding evidence is non-empty, which clears the mechanical tell. The goal is **not** grounded, and **authorizes no task**, because the answer contract is not settled: § Question is this session's restatement rather than the operator's sentence, § Answered when is unwritten, and § Close rule is unwritten. Those three are owner-held and this was a headless exchange with no channel to ask (`GOAL_RUNBOOK.md` § Grounding a goal: a goal hollow in any of the five field classes authorizes no task, not one, not a small one). The open questions are in the grounding session's handback, numbered.

§ Invariants, § Limits, § Reserved gates and § Grounding evidence are filled and are the operator's or the repository's, marked at each point of use. When the owner's answers arrive, the three unsettled headings are filled and this line changes to `grounded`. From that point nothing here is edited in place; corrections go in § Amendments.

## Question

**Unsettled — needs the operator's own sentence.** `[AGENT]`

The operator's question as it reached this session, verbatim:

> Is `p_pump` = 1.0 MW defensible for a helium-primary loop at this plant scale, and what sourced value should the model carry? `[AGENT]` — operator, 2026-08-27

It restates discovery row `20260821-power-cycle-ab#3`, whose own wording is: "`p_pump` = 1.0 MW (held, cycle-independent in every arm) is roughly 100× below helium-primary circulator figures (2–6 % of blanket thermal power), per DI-008. It suppresses the recirculating fraction in every arm equally, so it does not bias the A/B, but it understates `rec_frac` everywhere." `[INHERITED: exploration/stellarator_e2e/studies/20260821-power-cycle-ab/record.md@881d4448 § 15]`

Why this is left unsettled rather than adopted as written: the sentence carries two questions, and which one the goal ends on decides what "answered" means. The first ("is 1.0 MW defensible?") can end on a reasoned no with the value still held. The second ("what sourced value should the model carry?") ends only on a value, or on a recorded finding that no admissible value exists. § Answered when has to say which, and that is the operator's call. See handback question 1.

## Consumer

Discovery row `20260821-power-cycle-ab#3`, an open finding in a committed A/B study. `[AGENT]` — operator, 2026-08-27.

The row is a first sighting and nothing has appended under the id since (`exploration/stellarator_e2e/studies/DISCOVERY_LOG.md@e891b23a`, scanned whole for the id per `GOAL_RUNBOOK.md` § The discovery log). Its `Home` column reads "`knowledge/research/approved/20260821-165616_wi031-item6-second-arm-values.md` (follow-up R4); item not yet minted" — so the row is routed to a research finding and to **no work item**. `[INHERITED: exploration/stellarator_e2e/studies/DISCOVERY_LOG.md@e891b23a]`

**There is no work item for this.** `[AGENT]` — operator, 2026-08-27. What the answer changes is the row's disposition, and the runbook requires that a touched row not return as `unrouted` (ADR-004). Whether the goal mints a work item under the MFE Cost Modeling epic (`work/backlog/epic-mfe-cost-modeling.md@f22bd288`, `Status: active`) is a step the round would take, not a premise of the goal. See handback question 4.

## Answered when

**Unsettled — owner-held. This is why § Status is `draft`.** `[AGENT]`

The condition that ends this goal has to be concrete enough that two people read it the same way, and it has to cover both directions, because the evidence in § Grounding evidence makes both live: a sourced re-basing lands, or 1.0 MW stays held with the optimism disclosed and a reversal condition recorded. What it cannot be settled from is the repository — the row's own disposition, the study's § 17, and DI-008 all say "a dedicated modeling item" without saying what would end the question. See handback questions 1, 3 and 4.

## Invariants

What a comparison must preserve for results from different rounds to mean the same thing.

- **Package.** The comparison baseline is the sealed package `exploration/stellarator_e2e/pkg/stellarator_tea` — the committed alias of `exploration/stellarator_e2e/generated` — at the version study `20260821-power-cycle-ab` ran against: `repo_commit` `ffa5c54c9848c0f150ded5136d3f877efb47edd2`, indicator-input fingerprint `00badf7f…9c2141`, executable fingerprint `7447efea…`, model-contract fingerprint `1ca93d0c…`. `[INHERITED: exploration/stellarator_e2e/studies/20260821-power-cycle-ab/snapshot.json@881d4448]` Any round that regenerates the package promotes a new pin, and the runbook bounds a round at one promoted pin.

- **The twin.** The models have two byte-identical homes: canonical `models/library/` and `models/designs/`, and the exploration twin `exploration/stellarator_e2e/models/`. `tests/models/test_model_family_spines.py` fails on any byte difference. A model change that lands in one home and not the other is a broken invariant, not a partial result. `[INHERITED: exploration/stellarator_e2e/STAGED_MODELS.md@ba5c9945]`

- **Comparison — what "better" means.** Results are read as LCOE plus the five viability verdicts (`net_positive`, `recirc_ok`, `beta_ok`, `wall_load_ok`, `tbr_ok`, `models/library/analyses/mfe_viability.sysml`). `[INHERITED: exploration/stellarator_e2e/studies/20260821-power-cycle-ab/record.md@881d4448 § 4]`

- **The channel `p_pump` travels.** `[AGENT]` — operator, 2026-08-27. `p_pump` reaches the verdicts through exactly two terms of the plant power balance and nothing else:

  - the thermal balance, `p_th = mn·p_neutron + p_alpha + p_input + eta_p·p_pump` (`models/library/analyses/mfe_power_balance.sysml@8f3b510c:119`), with `eta_p` = 0.5 for this concept (`models/designs/stellarator_09/stellarator_plant.sysml@ba5c9945:496`);
  - the recirculating sum, `recirculating = p_coils + p_pump + p_sub + p_aux + p_cool + p_cryo + p_input/eta_pin` (`mfe_power_balance.sysml@8f3b510c:135`).

  From there: `rec_frac` = 1/`q_eng` = `recirculating`/`p_et` and `p_net` → the `recirc_ok` and `net_positive` verdicts and LCOE. A round that gives `p_pump` any other reach — a pressure-drop model, a coolant-loop component, a coupling to `a` or to wall load — has widened the channel and changed what "better" means (`GOAL_RUNBOOK.md` § Opening and closing a round, trigger 3).

- **The input shift is equal across arms; the effect is not.** `[AGENT]` — operator, 2026-08-27.

  `p_pump` is cycle-independent by construction (DI-007) and is held at 1.0 MW in all four arms of the A/B, so a re-based value adds the **same megawatts** to every arm's recirculating sum. `[INHERITED: knowledge/KNOWLEDGE.md@ffa5c54c DI-007; exploration/stellarator_e2e/studies/20260821-power-cycle-ab/record.md@881d4448 § 13]`

  The **effect** is not equal, because `rec_frac` is that sum over `p_et`, and `p_et` differs by arm by construction (η 0.333 → 0.47). The arms already sit at different recirculating fractions at the same grid corner — 0.94 / 0.79 / 0.68 by arm (`record.md@881d4448:208`) — and the `recirc_ok` fence already sits at different radii: violated at R ≤ 8.0 m (paper), ≤ 6.5 m (upstream), ≤ 5.5 m (both η 0.47 arms), at a = 0.8 m against threshold 0.5 (`record.md@881d4448:56`).

  **This states the channel and the distinction and stops there.** `[AGENT]` — operator, 2026-08-27. Whether comparison meaning survives a re-based value is **not settled at grounding**: it is a judgment for a round to make on evidence in hand, under the disposition checkpoint and the fresh review. A goal that hands a round the conclusion has not grounded anything.

- **Held equal across rounds unless the operator rules otherwise.** `eta_p` at 0.5, `f_sub` at 0.03, `p_trit` at 10.0 MW, `p_house` at 4.0 MW, and the baseline geometry the oracle scan used. `[INHERITED: models/designs/stellarator_09/stellarator_plant.sysml@ba5c9945:496,505,548,551]` These are the other terms of the same two sums; moving one moves every comparison in this goal at the same time as `p_pump` moves, and the two effects would not be separable afterwards.

- **The axis rule.** `modeling_project/STUDY_POLICY.md@ad2fb4ea` § 2 rule 1: "Sweep axes are causal design levers only … Never a quantity any calc in the package computes," and rule 3: "If a refinement internalizes a quantity that was previously a lever, the axis retires." `p_pump` is a settable input today and is a held (not swept) value in both committed studies. If the answer makes it computed — a fraction of `p_th`, say — it retires as a settable input. That is a reserved gate (§ Reserved gates 2), and it is a comparison-meaning change the operator should see before a round runs, not after.

## Grounding evidence

Tracked artifacts cited `<path>@<commit-sha>`. Every path below was checked with `git log -1` at this session's HEAD; **none has moved since the sha it is cited at** (`GOAL_RUNBOOK.md` § When a cited artifact moves).

**The finding, and its full statement.**

- `exploration/stellarator_e2e/studies/DISCOVERY_LOG.md@e891b23a` — row `20260821-power-cycle-ab#3`. Sighting only; no disposition row has been appended under the id. Its stated home is the WI-031 research follow-up, and it says the modeling item is "not yet minted."
- `exploration/stellarator_e2e/studies/20260821-power-cycle-ab/record.md@881d4448` — § 15 finding `#3` (the full statement, and why it was not changed in the A/B); § 4 (the `recirc_ok` fence per arm); § 11 (the corner `rec_frac` values, from the oracle scan); § 13 (`p_pump` = 1.0 named as a value fed identically to both sides and therefore *not* independently verified — "oracle parity verifies the package's arithmetic given those values, not the values"); § 17 (a sourced `p_pump` listed as an open limitation).

**The knowledge the question rests on.**

- `knowledge/KNOWLEDGE.md@ffa5c54c` **DI-008** — "Helium primary-loop circulator power is 2-6% of blanket thermal power; the stellarator default understates it ~100x." Its model implication is the shape of this goal, stated already: "Re-source the stellarator `p_pump` from a helium-circulator basis (2-6% of blanket thermal power, ~60-190 MW for Stellaris) **through a dedicated modeling item; do not fold it into an A/B study, because it moves the baseline and every arm equally.**" Its analysis implication: absolute LCOE and `recirc_ok` verdicts from the current package "carry a known optimism of order 60-190 MW recirculating power."
- `knowledge/KNOWLEDGE.md@ffa5c54c` **DI-007** — "Power-cycle choice does not reach primary-coolant pumping power." This is why the A/B held the value rather than varying it, and why a re-basing is arm-independent. Its model implication also carries a standing instruction: "Any study that varies another value 'by cycle' is inventing a dependency the upstream model does not have and must say so."

**What the model does today.**

- `models/designs/stellarator_09/stellarator_plant.sysml@ba5c9945:502-503` — `p_pump = 1.0` MW, a bound input, cited to 1costingFE `steady_state_stellarator.yaml:21` with **Basis** "1costingFE stellarator primary-coolant pumping power." The citation is a provenance chain to an upstream default, not a derivation; the upstream file carries no justification document for it (see the research finding below).
- `models/library/analyses/mfe_power_balance.sysml@8f3b510c:66,119,135` — `p_pump_in` is a plain `in attribute`; the two terms named in § Invariants are its only uses in the file.
- `models/designs/generic_mfe/mfe_plant.sysml@ba5c9945:242,290` — `p_pump` is a plain concept-level attribute bound through to the power balance. There is no calc that computes it.
- MR-3 applies: the library stays concept-agnostic and concept values live in `designs/`. A helium-circulator fraction is a coolant-specific value and belongs in `designs/`, not in the library calc. `[INHERITED: work/backlog/epic-mfe-cost-modeling.md@f22bd288]`

**The sourced figures, and how admissible each is.** This is the part that decides whether the second half of the question can be answered at all.

- `knowledge/research/approved/20260821-165616_wi031-item6-second-arm-values.md@ffa5c54c` § 1 — the WI-031 R4 follow-up the discovery row names as its home. It states the physics (the cycle working fluid is secondary-side; primary circulator power is set by helium mass flow and loop pressure drop), records the disposition that made 1.0 MW correct *for that study*, and surfaces the premise conflict as a table of three figures with their admissibility marked:
  - **Cismondi et al. 2017**, EUROfusion WPPMI-CPR(17) 17709 — "In case of helium the pumping power is ~150MW, one order of magnitude higher than in case of water (~15MW)" for a 2389 MW HCPB blanket → **6.3 %**. Ingested at `knowledge/concept_research/31-laser-icf-oec-architecture/iter-02/sources/scipub-wp-content-uploads-eurofusion-wppmicpr17-17709.md@0bf791d1:176` (verified by this session at that line). **Not registered in `knowledge/SOURCE_INDEX.md@ffa5c54c`** — a grep for "Cismondi", "Moscato" and the OSTI id returns nothing.
  - **Kessel et al., ARIES-ACT overview** — "a pumping power requirement of ~1% of the total thermal power"; "12 MW for He in the divertor and Ppump/Pthermal ≈ 2% for ACT2" → **1–2 %**. Ingested at `knowledge/concept_research/33-state-backed-tokamak-best/iter-02/sources/osti-servlets-purl-1178069.md@aff7a2f9:175,290` (verified at those lines). Also unregistered. Note this is a DCLL / He+LiPb machine, not a helium-primary blanket — it is the low end of the band for a reason a round has to weigh.
  - **Moscato et al., SOFT 2018** (EUROfusion WPBOP-CPR(18) 20276) — 2101.7 MWth, 9 loops × 2 compressors, ≈131 MW total (**6.2 %**); an 8-loop near-term design at 83–94 MW (**~4 %**). **Open PDF, not ingested.** This is the only source in the set that is a helium-primary *pumping-system design* rather than a single reported figure, and it is the one not in the repository.
- **A band discrepancy this session found, unresolved.** DI-008 states "~60-190 MW for Stellaris"; the research file it was minted from states the same three sources "bracket 30–190 MW" (`…wi031-item6-second-arm-values.md@ffa5c54c:47`), the lower end coming from ARIES-ACT's 1 %. `[AGENT]` The two numbers are not the same band, and which one the goal works against changes whether ~1 % is inside the sourced range. Neither figure is this session's to correct — amending a DI is a reserved gate (§ Reserved gates 4). See handback question 2.

**A check this session ran, and what it found.** `[AGENT]`

Whether the re-basing is small or large relative to what is already in the recirculating sum is answerable from the committed evidence, so it is recorded here rather than left for a round to rediscover. From the study's own oracle scan at baseline geometry (`exploration/stellarator_e2e/studies/20260821-power-cycle-ab/results/oracle_scan.json@881d4448`): the paper arm reads `p_net` 915.1 MW at `rec_frac` 0.1514, so `p_et` = 915.1/(1 − 0.1514) ≈ 1078 MWe and the whole recirculating sum ≈ 163 MW; at η 0.47, `rec_frac` 0.116 and `p_net` 1345.2 give `p_et` ≈ 1521 MWe and a sum ≈ 177 MW. Back out `p_th` ≈ 1078/0.333 ≈ 3240 MWth, which sits beside the paper's own ~3150 MWth and is a sanity check on the arithmetic, not an independent figure.

So DI-008's 60–190 MW is of the **same order as the entire existing recirculating sum**, and 2–6 % of ~3240 MWth is 65–194 MW. The re-basing roughly doubles to triples that sum. It does not follow from this that any verdict flips: at baseline geometry the paper arm's `rec_frac` would still land well under the 0.5 threshold on a first-order estimate. Where it plainly matters is the fence — `recirc_ok` is already violated out to R ≤ 8.0 m in the paper arm, and a sum of that size moves that fence outward.

**What this establishes and what it does not.** It establishes that the shift is not a small perturbation, so "the effect is negligible, leave it held" is not available without measuring. It does **not** establish where any fence lands, and it must not be read as one: it is a hand derivation from five oracle-scan points, it ignores the second-order feedback (a larger `p_pump` raises `p_th` by `eta_p·Δp_pump`, which raises `p_et` and `p_sub` in turn), and the governing quantity `rec_frac` has no per-point package evidence at all — that is finding `20260821-power-cycle-ab#10`, and the study's own § 17 says the five power-balance channels exported empty. Measuring the fence needs a package run, which needs a pin, which is a `PREREQUISITE` (below). **This settles nothing about whether comparison meaning survives.** `[AGENT]`

**A modelling question the evidence raises and does not answer.** `[AGENT]` DI-008's basis is a *fraction of blanket thermal power*, and `p_th` is a quantity the model computes and that moves with the swept geometry. So "carry a sourced value" has at least two shapes: a re-based scalar in MW held at the design point, or a fraction of computed `p_th`. The second is an internalization: it retires `p_pump` as a settable input (§ Invariants, the axis rule; § Reserved gates 2), and it is algebraically self-referential, because `p_th` already contains `eta_p·p_pump` — closed-form solvable, but a real design question, and `STUDY_POLICY.md@ad2fb4ea` § 1 is the file that governs when an equality may be internalized as a calc. Choosing between the shapes is the goal's own work and is deliberately not settled here. See handback question 3.

**The rules the work would run under.**

- `modeling_project/STUDY_POLICY.md@ad2fb4ea` § 1 (equalities belong inside the forward computation, not as asserts over swept axes), § 2 rules 1 and 3 (the axis rule and axis retirement), § 3 (the guard pattern).
- `work/backlog/epic-mfe-cost-modeling.md@f22bd288` — `Status: active`; the named home for a modeling item, with MR-3 restated there.
- `work/completed/20260822_WI-030_computed-beta-peak-field@ffa5c54c` — the precedent for turning a typed-in input into a computed quantity with a verification record against the source's printed value.
- `work/completed/20260827_WI-032_cold-volume-basis` (closed `BOUNDED_NEGATIVE` 2026-08-27) and goal `cryo-volume-basis` — the nearest precedent for *this goal's shape*: a discovery row questioning a held input, run as a goal, closed on an owner ruling that the value **stays held**, with a reversal condition recorded. `[INHERITED: exploration/stellarator_e2e/studies/DISCOVERY_LOG.md@e891b23a, row 20260823-magnet-technology-ab#2, 2026-08-27]` A reasoned "keep 1.0 MW held, with the optimism disclosed" is a first-class outcome of this goal, not a failure of it.

**The two seams that will bite.** `GOAL_RUNBOOK.md` § The native seams.

- **`research` is unrepaired.** Two of the three figures are ingested but unregistered in `SOURCE_INDEX.md`, and the best one (Moscato) is not in the repository at all. Registering a source or minting a DI runs the hand pattern (WI-031: a modeling-PM work item runs the round, insights land in `knowledge/research/approved/`, DIs mint at close), never an improvised procedure.
- **`integrate` is unrepaired and has no documented hand pattern anywhere in the repository.** Any round that lands a model change then needs a regenerated, verified, pinned package before a study can measure where the fence moved. The runbook is explicit: that is a `PREREQUISITE` return handed to the operator. The goal runs under that ceiling, and a round that lands a model change and stops at `PREREQUISITE` is an honest stop.

## Limits

Restated explicitly; nothing is inherited silently. These are the `GOAL_RUNBOOK.md` § Limits defaults, kept exactly, by operator decision of 2026-08-27. `[AGENT]`

| Limit | This goal | At the cap |
|---|---|---|
| Retry cap | 2 retries (3 attempts) | The task ends as mechanical failure past cap — a blocker |
| Checkpoint revision cap | 2 revisions (3 submissions) | `### Stop` of kind `cap`; the round stops. Execution is **not** permitted |
| Round limit | 6 rounds | The goal is re-grounded with the operator, or closed |
| Tasks per round | none | Already bounded by one pin, one study, and mandatory close after a valid reading |

**No time limit is declared.** `[AGENT]` — operator, 2026-08-27. The template carries a "Time or iteration limit" row; `GOAL_RUNBOOK.md` § Limits has no such row, and this session was told not to invent one. The row above is dropped rather than filled with a number nothing in the runbook supports.

## Reserved gates

**The general rule, above every named instance:** merge, push, work-item close and archive are owner-held per the runbook, and **any model or knowledge mutation beyond this goal directory needs owner sign-off** — anything landing in `work/`, `models/`, or `knowledge/`. `[AGENT]` — operator, 2026-08-27.

The five below are named instances of that rule, not a closed list. An unnamed mutation is still gated. `[AGENT]` — operator, 2026-08-27.

1. **Promoting a pin.** The `integrate` seam is unrepaired and has no documented hand pattern, so any regeneration-and-pin is a `PREREQUISITE` return to the operator, not a task the round completes.
2. **Retiring `p_pump` as a settable input** — making it computed from `p_th` or from anything else. It is a held input of two committed studies and a named "not independently verified" value of one of them (`record.md@881d4448 § 13`); internalizing it retires it as a lever under `STUDY_POLICY.md` § 2 rule 3.
3. **Changing the value of `p_pump` in `models/designs/stellarator_09/stellarator_plant.sysml`,** in either home of the twin. This is the mutation the question is about, and it is the owner's go/no-go, not the round's.
4. **Minting or amending a DI, or registering a source in `SOURCE_INDEX.md`** — including resolving DI-008's 60–190 vs 30–190 band discrepancy. The `research` seam is unrepaired; the hand pattern mints DIs at work-item close.
5. **Widening the channel `p_pump` travels** — a pressure-drop or coolant-loop model, a coupling to geometry or wall load. Adjacent, tempting, and a different goal. Doing it changes what "better" means (§ Invariants) and closes the round on trigger 3.

**The close ruling, if the round ends on a judgment call, is the owner's.** `[AGENT]` — operator, 2026-08-27.

Two decisions in this area are already on the record as the owner's and are not re-openable by a round of this goal: the ruling that the economic axes (`availability`, `discount_rate`) carry no sensitivity for this package (`[OWNER 2026-08-22]`, cited at `exploration/stellarator_e2e/studies/20260821-power-cycle-ab/record.md@881d4448 § 8`), and the ruling that `vol_cold_cryo` stays a held, settable input (`[OWNER 2026-08-27]`, cited at `exploration/stellarator_e2e/studies/DISCOVERY_LOG.md@e891b23a`, row `20260823-magnet-technology-ab#2`).

## Close rule

**Unsettled — owner-held.** `[AGENT]`

What the repository and the operator's brief establish: the close ruling is the owner's if the round ends on a judgment call (§ Reserved gates), and the `cryo-volume-basis` precedent had the owner close on the fresh round review's recommendation. Neither settles who closes *this* goal or on what, and this session will not write an owner's rule on a precedent. See handback question 5.

## Amendments

None.
