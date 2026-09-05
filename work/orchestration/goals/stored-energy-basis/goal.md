# Goal: stored-energy-basis — does the sustainment verdict rest on the model's stored-energy form, and is the paper's printed 504.65 MJ the right target?

Drafted 2026-09-04 from the previous session's handoff (`evidence/handoff_20260904-170919.md`), **owner not present**. Procedure is `work/orchestration/GOAL_RUNBOOK.md` § Grounding a goal; this file does not restate it.

Provenance: `[AGENT]` for what this session supplied, `[OWNER]` for what the owner said (here only as relayed by the handoff, and marked so), `[INHERITED: <path>]` for what a repository artifact carries. Nothing in this file has been ratified.

## Status

`draft` — 2026-09-04. All five field classes are filled below, but the owner was not in session: § Question and § Answered when are agent wording awaiting ratification, and the rulings § Reserved gates names are unresolved. **A draft goal authorizes no task.** The diagnostic the handoff scoped as T-001 was run instead as **grounding evidence** (`evidence/w_counterfactual/NOTES.md`): it is oracle-side, cheap, and touches nothing § Invariants protects, and `GOAL_RUNBOOK.md` § Grounding a goal exists to stop a run spending a round on a question the repository can already answer. The owner therefore grounds this goal knowing that the first half of § Question is answered and the second half has a first pass with a named residual. The owner may close at grounding on that evidence, or ground it and open round 1 for what remains.

## Question

> Does the pinned baseline's `sustainment_ok` violation, and the committed "no feasible driven point at the printed 100 MW wall-plug on the design geometry" result, survive when the model's stored thermal energy is set to the paper's printed 504.65 MJ? If not, what in the profile integral produces the +9.2 % — and is the printed value the right target?

`[AGENT] — proposed wording: the handoff's draft with the last clause added on the grounding evidence.` The owner's ask, as relayed: the gap has been carried as an invariant by two later goals and nobody owns it, and every study reading since 2026-09-01 sits on the biased balance `[OWNER, relayed by evidence/handoff_20260904-170919.md § Focus; recorded nowhere else]`.

The gap, as the repository records it `[INHERITED]`: the model integrates assumed power-law profiles for W (`models/library/analyses/mfe_plasma_sustainment.sysml:25`; exponents bound at `models/designs/stellarator_09/stellarator_plant.sysml:578,581,602`), finds 551.4 MJ against the printed 504.65 (+9.2 %) with every other balance term within 4 % of the paper, and because conducted loss goes as W^2.56 in the closed ISS04 form the baseline needs 90.6 MW coupled against 50 installed (`operating-point-closure/evidence/T-002_prototype/NOTES.md@2df2c548`, L-001/L-005 at `learnings.md@f9663df8`). Two later goals inherited "not a defect and not this goal's to fix" (`priced-levers/goal.md:52`, `wall-and-heating/goal.md:52`), on an agent-grade rule that W is never tuned; no owner ruling and no backlog item owns it.

**What the grounding evidence says** (`evidence/w_counterfactual/NOTES.md`, all oracle-side): with W scaled to the printed value and the closure left live, the baseline needs 37.5 MW, not 90.6, and *both* baseline violations flip to satisfied (the wall one through fusion power, which falls 5.6 % as the ash re-closes); at 100 MW the design geometry opens (six driven points; the baseline itself feasible at 332.6) while the cheapest driven point barely moves (212.46 → 212.31) and 347 of the record's 257 + 400 driven points lose driven status, 305 of them by igniting. And the target itself is in question: no reading of the paper's plotted profiles with its printed peaks reaches 504.65 MJ — the caption's exponents on every species give 575, a figure-consistent family with the ash peaked gives 527–559, the model's 551 is a fair read of the figure (the WI-022 digitization), and the printed β implies 567 at the axis field. Every reading reproduces the printed fusion power; none reproduces the printed energy. The +9.2 % is not a misread of the figure; the printed 504.65 MJ is the value the paper's own profiles and peaks come furthest from. That undercuts L-001's premise and is surfaced here, not resolved.

## Consumer

- **The `wall-and-heating` round-2 fresh review and the owner's close-packet rulings.** During this session that round closed on trigger 1 as a conditional positive (`work/orchestration/goals/wall-and-heating/trail.md` § Round 2 result at `f51b2915`; C-001.r2 `PASS` with seventeen disposition rows landed at `8906d4e7`); the fresh review is pending. Three of the result's four stated conditions — the design geometry closed at 100 MW (#1), the ash knife-edge (#2), the one-sided fence passing ignited points (#4) — are exactly the readings the counterfactual moves, and #6 (round 1's 26 survivors) moves with them; #7 stands (`NOTES.md` § 5, § 8). The owner leaned, in the previous session, toward putting this result in front of that round before its dispositions were accepted `[OWNER, relayed by the handoff § Open questions; unrecorded]`; the dispositions have since landed, so the live call is whether it goes in front of the review and the close-packet rulings — § Reserved gates.
- **The next-goal selection**, and whatever work item the owner mints if the model's stored-energy basis is to change.
- **The two inherited invariants** and L-001's implication line ("any residual at the printed point is attributed first to the W-form, and W is never tuned to the printed value"), all agent-grade `[INHERITED: priced-levers/goal.md:52; wall-and-heating/goal.md:52; operating-point-closure/learnings.md@f9663df8 L-001]`.
- **Discovery rows** `20260904-wall-and-heating#1`, `#2`, `#4`, `#6` (`exploration/stellarator_e2e/studies/DISCOVERY_LOG.md@8906d4e7`, now carrying round 2's dispositions): any round of this goal whose evidence touches them owes a disposition (`GOAL_RUNBOOK.md` § The discovery log). Grounding evidence is not a round and writes no row.

## Answered when

> **(a) The counterfactual, deposited.** An oracle-side evaluation at the reference point and over the `20260904-wall-and-heating` window with W scaled to 504.65 MJ, every verdict flip counted case by case against the committed record, the constant-scale assumption stated. — **Met at grounding** (`NOTES.md` §§ 3–5), subject to ratification.
>
> **(b) The attribution, written or bounded.** Either a written attribution of the +9.2 % or a bounded negative naming what was ruled out. — **First pass at grounding** (`NOTES.md` § 7): about two points are the model's ash shape against a figure-consistent family; the remaining seven no reading of the paper's profiles and peaks reaches; the residual is the source's definitions (its volume average, β's reference field, what its 0.5-D code integrated, which n19 entered its ISS04). (b) closes when the owner accepts the first pass as the attribution, or a research-seam request against the source returns those definitions or a bounded negative.
>
> **(c) The basis, ruled.** The owner rules what stored-energy basis the model carries — the present family, the paper's stated exponents, or a sourced alternative — and any model change returns to the owner as a minted work item through the modelling PM. A trail-only answer that leaves the model as it is counts.

`[AGENT] — (a) and (b) from the handoff's draft, (c) added because the evidence shows the target is in question and a change to it is owner-gated.`

## Invariants

- **Package:** nothing is written under `models/`, `exploration/stellarator_e2e/generated/`, or `exploration/stellarator_e2e/studies/manifest.json` by this goal; the pin stays indicator `c1b0f0d1…`, semantic `d468f3b6…`, executable `d4be3951…` (WI-041). The baseline of record is LCOE 313.513 with `sustainment_ok` and `wall_load_ok` violated (`exploration/stellarator_e2e/studies/20260904-wall-and-heating/results/baseline_result.json`, record dir at `a5b0b96a`).
- **Every number this goal produces is labelled oracle-side, not package evidence**, until a model change lands through the modelling PM and a study runs at a new pin.
- **W is not tuned in the model.** A counterfactual in an in-memory copy of one oracle function is a diagnostic; a change to the W form or to the exponents is a reserved gate.
- **The constant-scale assumption travels with every claim** (`NOTES.md` § 6): multiplicative, geometry-independent; the sign of each move is robust, the location of any boundary is not a claim.
- **Comparison:** flips are counted against the committed record's verdict columns by case id, never against a re-run of the record; "feasible", "ignited" and "driven" keep the record's definitions.
- **Clean room binds.** `knowledge/holdout/` is never read; the Stellaris paper (concept research 09) is admissible; any research subagent carries the screen in its own instructions before any fetch `[INHERITED: knowledge/holdout/aries-cs/PROTOCOL.md; wall-and-heating/goal.md § Invariants]`.
- **A missing input is surfaced with options, never defaulted** `[OWNER 2026-09-02, priced-levers/goal.md § Invariants]`.

## Grounding evidence

- `evidence/w_counterfactual/NOTES.md` with its scripts and raw outputs (this goal directory; unpinned until this goal's first commit, then cited at that sha) — Basis A (the oracle, constant scale), Basis B (the operating-point prototype), the 6,311-point window re-evaluation, the attribution arithmetic, and the printed values read from the pages.
- `evidence/handoff_20260904-170919.md` — the previous session's handoff: the owner's ask, the drafted question, the open questions.
- `work/orchestration/goals/operating-point-closure/evidence/T-002_prototype/NOTES.md@2df2c548` — the cross-check table (W 551.3 vs 504.65, +9.2 %; τ_E, radiation, fusion within 4 %), findings 1–3, and `op_solve_final.py`, the prototype Basis B patches.
- `work/orchestration/goals/operating-point-closure/learnings.md@f9663df8` — L-001 (the never-tune implication, agent-written 2026-09-01, accepted by a fresh reviewer the same day), L-002, L-005; `trail.md@a5b0b96a` § Goal close — the owner's five 2026-09-02 rulings, none of which mentions W.
- `work/orchestration/goals/priced-levers/goal.md:52@a5b0b96a` and `work/orchestration/goals/wall-and-heating/goal.md:52@a5b0b96a` — the inherited invariant, both `[INHERITED]` from L-001/L-005 and `round2_review.md § 4 constraint 3`.
- `exploration/stellarator_e2e/studies/20260904-wall-and-heating/` record dir at `a5b0b96a` — `record.md` § 3 (212.460 at `c1721`; nothing feasible at the design geometry at 100 MW), § 4 (458 / 787 / 257 at 100 MW; the one-sided fence), § 15 #1, #2, #4, #6, #7, #8; `results/points.csv` (the 6,311 inputs and verdicts the counterfactual re-evaluates) and `results/oracle_operands.csv` (the record's own W_th per case).
- `exploration/stellarator_e2e/studies/DISCOVERY_LOG.md@8906d4e7` rows `20260904-wall-and-heating#1`, `#2`, `#4`, `#6`, sightings and round-2 dispositions.
- `work/orchestration/goals/wall-and-heating/trail.md@f51b2915` § Checkpoint C-001.r2 (round 2) `PASS`, § T-004 return, § Round 2 result (closed on trigger 1, a conditional positive with four conditions; the fresh review pending) — and `evidence/round2_T-004_proposed_dispositions.md`, the dispositions written on the record's readings, landed in the log at `8906d4e7`.
- `models/library/analyses/mfe_plasma_sustainment.sysml:25-48@a5b0b96a` — the W form, the closed τ_E, the requirement; `models/designs/stellarator_09/stellarator_plant.sysml:562-602@a5b0b96a` — the exponents and the doc comment that records their digitization and the extraction's wrong caption; `work/completed/20260718_WI-022_predictive-confinement/prototype/fig16_curves.json@a5b0b96a` — the digitized Fig. 16 curves (electrons 0.617, fuel 0.33, temperatures 1.19; no helium points).
- `exploration/stellarator_e2e/verify_stellaris.py:97-158@a5b0b96a` (`_sustainment`, W at :123 inside `state()`) and `studies/oracle_entry.py:200-207@a5b0b96a` (the sustainment channels) — the seam the diagnostic drives.
- The Stellaris source, concept research 09, iter-02 `publikationen-1000179851-172386752/tmpissrtbos/`: `raw.pdf` p. 8 (Eqs. 2–3), p. 10 (Table 5 and Fig. 16 with its caption α_T = 1.2, α_n = 0.35), p. 32 (Appendix A: A.3, A.5–A.8); page images `images/page_009_table_0.png` (Table 5), `images/page_002_table_0.png` (Table 2). The extracted `output.md` mis-states the Fig. 16 caption and carries phantom Table 5 rows; read the pages.
- `work/BACKLOG.md@a5b0b96a` — no item owns the gap; the open modelling items are WI-034, WI-038, WI-040, WI-041.

## Limits

| Limit | This goal |
|---|---|
| Retry cap | 2 retries (3 attempts) |
| Checkpoint revision cap | 2 revisions (3 submissions) |
| Round limit | 6 rounds |
| Time or iteration limit | none |

The defaults, restated. The goal is small: (a) is met at grounding and (b) needs at most one research round, so the round limit will not bind; it is not tightened without the owner.

## Reserved gates

Owner-held; none resolved:

- **Ratification of this draft** — § Question and § Answered when as worded, or reworded.
- **Changing the W_th form or the profile exponents in `models/`** (`stellarator_plant.sysml:578,581,602`; `mfe_plasma_sustainment.sysml:25`), including adopting the paper's stated exponents or a quasi-neutral family. Any such change is a minted work item through the modelling PM, never a tuning.
- **Re-ruling the inherited invariants** at `priced-levers/goal.md:52` and `wall-and-heating/goal.md:52`, and L-001's never-tune implication. All three are agent-grade; the owner said in the previous session that the rule is theirs to keep or overturn `[OWNER, relayed by the handoff § Context; unrecorded]`.
- **Whether this evidence goes in front of the `wall-and-heating` round-2 fresh review and the owner's close-packet rulings** (the checkpoint passed and the dispositions landed during this session).
- **Any rubric Row 1 consequence** (the sustainment architecture's P3 grade rests on the balance this goal questions).

Structural, restated from their standing homes: merge, push, and work-item close stay the owner's (`GOAL_RUNBOOK.md` § What this is, and what it is not); the fold-back of `goal/stored-energy-basis` into `feat/demo-maturation` is the owner's act.

## Close rule

The owner closes — at grounding on the deposited evidence, on § Answered when, or by redirect at any round boundary. `[AGENT] — proposed.`

## Amendments

None.
