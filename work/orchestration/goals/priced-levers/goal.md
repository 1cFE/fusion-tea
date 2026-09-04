# Goal: priced-levers — can the two levers that would escape the deadlock be made to carry their real consequences?

Drafted and grounded 2026-09-02 in an owner-present session, straight off the close of `operating-point-closure`. Procedure is `work/orchestration/GOAL_RUNBOOK.md` § Grounding a goal; this file does not restate it.

Provenance: `[AGENT]` for what this session supplied, `[OWNER]` / `[OWNER-VERBATIM]` for what the owner ruled here, `[INHERITED: <path>]` for what a repository artifact carries. The owner was present: the framing correction, the slug latitude, and the no-gates ruling are the owner's; § Question, § Answered when, and § Close rule were presented as explicit proposals and adopted.

## Status

`grounded` — 2026-09-02. All five field classes are non-hollow (`GOAL_RUNBOOK.md` § Grounding a goal): § Grounding evidence is non-empty (the mechanical tell), and § Answered when, § Invariants, § Limits, § Reserved gates are filled below. Nothing here is edited in place; corrections go in § Amendments.

## Question

> Can the two levers the machine would use to escape the deadlock — conductor grade and heating power — be made to carry their real consequences, so the model charges honestly for using them?

`[AGENT] (adopted by the owner 2026-09-02, after the owner corrected an earlier "which escape does the machine buy" framing as a design question rather than a realism question)`.

The deadlock is measured, not assumed: at the printed 50 MW of installed heating the baseline machine has no feasible operating point anywhere in the swept space — below the conductor ceiling nothing sustains, and every field that sustains is over the ceiling. Both levers that could relieve it are presently unpriced in the model:

- **Conductor grade is free.** `B_max = 24.9` is a lone held literal with no consequence chain (`models/designs/stellarator_09/stellarator_plant.sysml:158-165`). Raise it and nothing in the model costs more, weighs more, or breaches a stress limit.
- **Heating is structureless.** The heating account is one linear line at $5,282,900/MW installed, and `eta_pin = 0.5` is held (`stellarator_plant.sysml:594`), so buying installed power buys a verdict plus a linear recirculation burden and nothing else. Its price is a straight line by construction.

The work is making both real. Whatever the model then says about which escape is cheaper is a **result**, not the goal.

## Consumer

The methodology owner, through demo epic Item 10 (`.project/backlog/epic_stellarator_mbse_demo.md`): the heating half is the next measured maturation delta — a fresh non-author Row-4 re-grade against the frozen rubric — feeding the eventual reveal-readiness condition. `[INHERITED: .project/concepts/stellarator-demo-maturation.md@81a4fee8 SC-3/SC-4]`

Secondary consumers: the two backlog items the previous goal's close minted but did not ground — **WI-038** (Conductor-Grade Lever: B_max Consequence Chain) and **WI-039** (Heating System Structure: Sources, Transmission, Launchers), `work/BACKLOG.md@dd0b5896` — and the two discovery rows they were minted from, `20260901-sustainment-fence#1` and `#4` (`exploration/stellarator_e2e/studies/DISCOVERY_LOG.md@dd0b5896`). Any round whose evidence touches those rows owes a disposition (`GOAL_RUNBOOK.md` § The discovery log).

## Answered when

> **Both halves land.**
>
> **(a) The heating half, graded.** A fresh non-author re-grade against rubric v1 (`rubric.md@dc0f0b6d`) scores **R4.P = 2** — the row's written physics target — with the anchor's full text evidenced: a wall-plug → coupled-power chain computed with a stated deposition assumption, verified. Validation battery green, affected studies re-run clean.
>
> **(b) The conductor half, studied.** One committed study at a promoted pin exhibits the `B_max` lever with its cost and stress consequence chain active, and reports what that does to the fences — whether a feasible region opens at the printed 50 MW installed, and where the binding constraints move. **Or** a round shows with sourced evidence that no admissible basis exists for a conductor grade above the printed 24.9 T, surfaces the options, and the owner rules.
>
> Either half may also end by the owner ruling on a written, sourced showing that its target cannot be met.

`[AGENT] (adopted by the owner 2026-09-02)`. Made explicit so two readers agree:

- **The two halves have deliberately different answer shapes**, because their yardsticks differ. Row 4 has a written physics gap to close and grades against it. Row 3 is already at target (3/3, `grading-r3-regrade.md@0cf0cf41`), so the conductor half **cannot** close on a Row-3 re-grade delta and does not try to; its honest answer is study-shaped.
- **Row 4's bar is the written P2 and nothing more.** R4.S already grades 2 at its written target (`grading.md@fc80e5b2`, cell R4.S), and the P3 raise was deliberately deferred to the next rubric version `[OWNER 2026-09-02]`. WI-039's minted title names S3-anchor content ("sources, transmission, launchers costed separately"); S3 structure may be built where the engineering wants it, but it does not enter this condition, and **no answered-when is written against an unwritten bar**.
- **"The conductor escape cannot be priced from admissible sources" is a full answer**, not a failure. Under (b) the goal ends on a sourced negative with the options surfaced, as readily as on a study.
- **The re-grade is by a fresh non-author grader against the same rubric sha** (grading protocol, `rubric.md@dc0f0b6d` § Grading protocol) — the delta claim rests on the frozen yardstick, not the round's own reading.
- **"Clean" for study re-runs:** re-run without crashes or unexplained constraint-verdict flips; explained flips are findings, not failures. `[INHERITED: .project/concepts/stellarator-demo-maturation.md@81a4fee8 SC-3]`

## Invariants

- **Package:** at most one promoted pin per round; every comparison inside a round runs against that pin's package identity (`modeling_project/STUDY_POLICY.md`; `.claude/skills/run-study/runbook.md`). The executed baseline entering this goal: pin `35e922c5cc15…`, sealed executable fingerprint `41e06ecb430c…`, case `stellarator-baseline-point-v1:c0000` — LCOE 307.087, eight verdicts with `sustainment_ok` **violated** (`exploration/stellarator_e2e/studies/20260901-sustainment-fence/results/baseline_result.json`, record dir `@62a1fa7b`).
- **Comparison:** "better" means rubric v1 anchors at `rubric.md@dc0f0b6d`, Row 4 for the heating half. Re-grades cite the same rubric sha; a rubric revision (owner-gated, concept OQ6 — and Row 4's P3 raise is queued for it) re-scores both model states before any delta claim. Headline LCOE and feasibility moves are expected and honest — no fitting to prior headlines; SV-016 (Q_eng band) stays `pending`, recorded against, never fitted `[OWNER standing, work/orchestration/stale-basis-recompute.md]`.
- **The violated baseline `sustainment_ok` is not a defect and is not this goal's to fix.** 90.6 MW required vs 50 installed is a disclosed, explained fidelity fact — the model's own analytic W-form, +9.2% at the printed point, never tuned `[INHERITED: learnings.md@f9663df8 L-001/L-005; round2_review.md § 4 constraint 3]`. Do not fix it, tune to it, or treat it as a failure. The ~91 MW threshold is oracle-derived; the **committed** resolution is one grid step — the fence flips between p = 90 and 100 MW — so its precision is not overread.
- **Comparison-meaning stake, named up front:** pricing a lever can retire held quantities as settable entry points (the WI-035 / WI-037 precedent). Committed studies that swept or held those axes are **restated, never silently broken** — the MR-WI037-7 shape. Which entry points retire is the round agent's call under the 2026-09-02 delegation; the restatement duty is not waivable. Budget for it: the last retirement cost ~30 fixture re-derivation sites `[INHERITED: learnings.md@f9663df8 L-006]`.
- **The four prior committed studies are not reproducible as written at pin `35e922c5…`**; their records stand at their own pins, and any replay drops the retired keys and re-reads fixed-operating-point findings `[INHERITED: round2_review.md § 4 constraint 2]`.
- **The 1costingFE handshake is NOT an invariant.** Anchor A is closed evidence at its pin; this goal neither re-runs nor preserves it `[OWNER 2026-08-30, pin addendum work/orchestration/stale-basis-recompute.md]`.
- **Clean room binds.** This is model-facing work: PROTOCOL §2/§3 apply in full; the four sealed PDFs stay unread; physics from admissible sources; engineering and cost from 1costingFE, pinned `0254385` `[INHERITED: knowledge/holdout/aries-cs/PROTOCOL.md; restated by the owner in the 2026-09-02 grounding instruction]`.
- **A missing input is surfaced with options, never defaulted** `[OWNER 2026-09-02]`. No family averages, no literature fallbacks, no "reasonable" substitutes for an absent basis.

## Grounding evidence

- `exploration/stellarator_e2e/studies/20260901-sustainment-fence/` record dir `@62a1fa7b` — the measured deadlock. `synthesis.md` (fresh administrator's recount): 0 of 154 evaluated points feasible at p = 50; the 29 that satisfy `sustainment_ok` all violate `peak_field_ok`; at p = 110 a bounded feasible band with the optimum at LCOE 293.468, beta 0.0311 — off the beta floor, bounded by sustainment below and the conductor ceiling above. Findings `#1` (the ISS04-relief-vs-ceiling deadlock; the conductor grade was never an axis, and "presumably a different conductor grade" is explicitly a presumption) and `#4` (installed heating is pure cost once sustainment is met; heating capital exactly linear at 5,282,900 $/MW).
- `work/orchestration/goals/operating-point-closure/learnings.md@f9663df8` — L-005 (the deadlock and its two evidenced escapes), L-001 (the W-form fidelity gap that owns the residual), L-006 (the entry-point retirement cost).
- `work/orchestration/goals/operating-point-closure/trail.md@dd0b5896` § Goal close — the five owner rulings of 2026-09-02, including the mint of WI-038/WI-039 and the deferral of Row 4's P3 raise.
- `work/orchestration/goals/operating-point-closure/evidence/round2_review.md` (record dir `@dd0b5896`) § 4 — the seven carried constraints, adopted here in full (see § Limits and § Invariants).
- `.project/active/demo-depth-rubric/rubric.md@dc0f0b6d` Row 4 — the anchors and the written P2/S2 target; the frozen yardstick. **Its Row-4 note is stale twice over** and governs nothing: it says P3 "rides on row 1's confinement closure, which is owner-gated", but Row 1 closed at target 2026-09-02 and the "owner-gated" framing was the Rung C error — no such gate ever existed. The rubric's **anchors** govern; its **gate notes** do not.
- `.project/concepts/stellarator-demo-maturation.md@81a4fee8` § Corrections — 2026-09-01 — the standing authority on the Rung C error. No agent may cite a Rung C gate, on Row 1 or Row 4, as authority.
- `.project/active/demo-depth-rubric/grading.md@fc80e5b2` cells R4.P and R4.S — R4.P = 1 with the `why_not_next` naming exactly the gap this goal's heating half closes (no heating-chain calc def exists; the only arithmetic is a held ratio inside the recirculating sum, `mfe_power_balance.sysml:117-121`); R4.S = 2, at its written target. Grader note G1 and the author disposition record the judgment call behind the 1.
- `.project/active/demo-depth-rubric/grading-r3-regrade.md@0cf0cf41` — Row 3 at target (3/3). The reason the conductor half is study-shaped and not grade-shaped.
- `.project/active/demo-depth-rubric/grading-r1-regrade.md@6bc81157` — Row 1 at target (R1.P = 3), the state this goal enters at.
- `.project/active/demo-depth-rubric/gap-report.md@fc80e5b2` — Row 4 sits in Band C ("gap with no measured leverage yet") at 1.6% cost share and "no constraint role of its own". **That reading is superseded by the sustainment study**: installed heating is now the axis that decides feasibility. Recorded here because the gap report predates the fence and is not re-run by this goal.
- `models/designs/stellarator_09/stellarator_plant.sysml@728d1263` — the two unpriced levers as bound: `B_max = 24.9` at `:158-165` (with the disclosed 1costingFE disagreement in its own doc comment), `peak_ratio`, `wp_side`, `k_sigma`, `sigma_allow` at `:150-205` (the stress chain a conductor grade would have to move); `p_input = 50.0` at `:582`, `eta_pin = 0.5` at `:594`, `p_ecrh = 50.0` at `:772`.
- `/home/reid/1cfe/1costingfe/src/costingfe/defaults.py` (pin `0254385`) — the pinned engineering and cost source, read at grounding, and it cuts both ways:
  - **For the heating half, it is sufficient.** `:96-101` per-method installed-power rates; `:104-108` `eta_pin = eta_source × eta_couple` with `eta_source_ecrh = 0.50` (gyrotron wall-plug), NBI 0.60, ICRF 0.70, LHCD 0.50. The P2 anchor's computed wall-plug → coupled chain has an admissible basis today; **no research seam is required for the heating half.**
  - **For the conductor half, it is insufficient in the direction that matters.** `:609-617` `MAGNET_TABLE` tops out at `rebco_hts b_max = 23.0`, with `nb3sn` 13.0, `nbti` 9.0, `copper` 8.0 — every grade **below** the model's own printed 24.9 T, which the instance's doc comment already discloses as a live disagreement. The deadlock needs relief **upward**. So the pinned source can price a conductor-grade lever downward and cannot price one upward at all.
- `exploration/stellarator_e2e/studies/DISCOVERY_LOG.md@dd0b5896` rows `20260901-sustainment-fence#1` and `#4` — the sightings and their full disposition lineage through the mint of WI-038 and WI-039.
- `work/BACKLOG.md@dd0b5896` — WI-038 and WI-039, both `backlog`, `standard`, under the MFE Cost Modeling epic. Backlog only; no work started.

## Limits

| Limit | This goal |
|---|---|
| Retry cap | 2 retries (3 attempts) |
| Checkpoint revision cap | 2 revisions (3 submissions) |
| Round limit | 6 rounds |
| Time or iteration limit | none |

The standing one-pin/one-committed-study bound per round means the two halves will span at least two rounds. Six is comfortable for that, and the bound is not relaxed to fit them into one.

**Named risk, not a limit:** the conductor half may find no admissible basis above 24.9 T (see § Grounding evidence on the pinned `MAGNET_TABLE`). The options are then research-seam ingestion of a named source, a parametric `B_max` sweep carrying a sourced cost/stress consequence relation without a grade name, or a sourced bounded negative. Whichever is taken is surfaced in the trail with its reasoning; none of them is a default, and none silently invents a number.

## Reserved gates

> "no gates. USE YOUR BEST JUDGEMENT ALONG THE WAY!" — `[OWNER-VERBATIM 2026-09-02]`, ruling on this session's two proposed gates: the conductor-grade basis fallback, and the Row-4 bar.

The owner reserves no goal-specific gates. Both proposed gates are ruled back to the round agent as execution decisions on its best engineering and modelling judgment — **including** the choice among research-seam ingestion, a parametric consequence relation, and a bounded negative when no upward conductor basis is found. The Row-4 bar is settled in § Answered when as the written P2, per the owner's 2026-09-02 deferral ruling, and needs no gate to hold it there.

What remains held is structural, restated from its standing homes rather than minted here: **merge, push, and work-item close stay the owner's** (`GOAL_RUNBOOK.md` § What this is, and what it is not; owner's grounding instruction 2026-09-02), and model changes still land through the native modelling PM with its validation levels — that is workflow routing, not a gate. The fresh-session gates (disposition checkpoint, round review, the answered-when re-grade) are runbook obligations, not owner gates, and are satisfied by spawned non-author sessions with their spawn prompts deposited as evidence — **every** gate session's prompt, the checkpoint's included `[INHERITED: round2_review.md § 4 constraint 6]`.

## Close rule

The owner closes — on the § Answered when condition, or by redirect at any round boundary. `[AGENT] (adopted by the owner 2026-09-02)`

## Amendments

None.

### Amendment 2026-09-02 — amends § Limits (the named risk) and § Grounding evidence

**What changed.** The named risk was written as "the conductor half may find no admissible basis above 24.9 T," treating the missing upward conductor basis as the obstacle. A recount of the committed study at grounding shows the obstacle is **two fences, not one**, and the conductor ceiling is not the binding half.

**The evidence.** Recounted this session from `exploration/stellarator_e2e/studies/20260901-sustainment-fence/results/points.csv` (record dir `@62a1fa7b`): of the 29 points at p = 50 that satisfy `sustainment_ok`, **zero** violate the conductor ceiling alone — all 29 violate `peak_field_ok` **and** `wp_stress_ok` together. The cheapest (I_coil 18.0 MA) needs B_peak 29.1 T against the 24.9 T ceiling (+17%) and carries σ_wp 888 MPa against the 800 MPa allowable (+11%); at 19 MA it is 30.7 T / 989 MPa, at 20 MA 32.3 T / 1096 MPa. **Raising `B_max` alone opens no feasible region at 50 MW** — the structural fence catches every point.

**Second reading, from the model's own doc comments.** `B_max = 24.9` is not a conductor limit as bound. Its doc comment at `models/designs/stellarator_09/stellarator_plant.sysml:158-165` states it is "the field Stellaris designs to (Table 2), not 1costingFE's REBCO engineering ceiling of 23.0 T," and the `peak_ratio` literal at `:156` was chosen so `9.0 × peak_ratio == 24.9` exactly, giving `peak_field_ok` margin 0.0 at the design point by construction (WI-030). So `peak_field_ok` presently measures "are you standing on the printed design point," not "what can the conductor take" — which is precisely why raising it is free.

**What this changes.** Nothing in § Question, § Answered when, or § Invariants: (b) already requires the lever's "cost **and stress** consequence chain active," and that conjunction is now the load-bearing part rather than a completeness clause. What changes is priority and vehicle:

- The binding lever is **structural** — σ = k_sigma·I_coil·B_peak/wp_side, and `wp_side = 0.36` is held at the printed worst-coil value with no sizing or cost consequence. Relief to 800 MPa at the 18 MA point needs `wp_side ≈ 0.40 m`, which costs conductor, cold mass into the cryoplant load, and radial build. Its natural vehicle is **WI-036** ("Winding-pack sizing chain: winding length from coil geometry, `wp_side` into the sizing and cost chain", `work/BACKLOG.md@dd0b5896`, `backlog`), already minted and not previously named in this goal. L-003 of the predecessor goal flagged it a round ago: "wp_side relief exists."
- The **conductor ceiling stays necessary but not sufficient**, and is not dropped: a feasible point at 50 MW needs structural relief *and* a defensible ceiling at ~29 T. It is researched as an input to the same increment rather than as the lead question.

**Ruling.** Recorded under the owner's standing 2026-09-02 delegation ("no gates. USE YOUR BEST JUDGEMENT ALONG THE WAY!") and the follow-on instruction of the same date authorizing research agents, use of 1costingFE, and unblocking by judgment. Surfaced to the owner in session before any work; not resolved silently. `[AGENT] (delegated by owner 2026-09-02)`

### Amendment 2026-09-03 — amends § Status, § Answered when, § Amendment 2026-09-02, and the WI-036 paths in § Grounding evidence

**Status: closed by redirect, 2026-09-03** `[OWNER 2026-09-03]` — trail § Goal close, on the round-1 review's recommendation (`evidence/round1_review.md`). Round 1 of 6.

**§ Answered when.** (a), the heating half, is redirected verbatim into `work/orchestration/goals/wall-and-heating/goal.md` § Answered when (a) and is that goal's to meet. (b), the conductor half, is **recorded open, not negative**: neither branch was met — the `B_max` consequence chain was not built (the round narrowed to WI-036 after T-001), and a labelled-extrapolation basis exists, so the sourced-negative branch does not apply. Its vehicle is WI-038, sequenced after `wall-and-heating`'s wall half and after WI-040.

**§ Amendment 2026-09-02 is superseded in one sentence.** "Raising `B_max` alone opens no feasible region at 50 MW" was true of the predecessor's grid at T = 14.63 keV and is **false at pin `6262dbf4…` with temperature swept**: three 50 MW points (`20260903-priced-levers` `c0148/c0164/c0180`, I 17 MA, T 17 keV, n 1.0×, B_peak 27.49 T, σ ≤ 789 MPa) fail the conductor ceiling alone and need no stress relief, and read 262.08–262.16 $/MWh against the 110 MW optimum 271.359 (round-1 review F3; `learnings.md` L-001). The amendment's other reading — the stress form is a real relief channel — stands, with the measured qualifier that the relief is nearly free in cost (L-002).

**Paths.** `work/active/WI-036_winding-pack-sizing/` → `work/completed/20260903_WI-036_winding-pack-sizing/` (closed `[OWNER 2026-09-03]`). Every citation to the active path in § Grounding evidence, § Amendment 2026-09-02 and the trail resolves there.
