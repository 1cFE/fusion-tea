# Goal: magnet-closure — can the magnet system be derived from its own engineering design instead of cited constants?

Drafted and grounded 2026-08-30 in an owner-present session. Procedure is `work/orchestration/GOAL_RUNBOOK.md` § Grounding a goal; this file does not restate it.

Provenance: `[AGENT]` for what this session supplied, `[INHERITED: <path>]` for what a repository artifact carries. The owner was present in this session: items the owner ratified carry `[AGENT] (ratified by owner 2026-08-30)`; items a repository artifact records the owner deciding carry `[OWNER <date>]` with the citation.

## Status

`grounded` — 2026-08-30. All five field classes are non-hollow (`GOAL_RUNBOOK.md` § Grounding a goal): § Grounding evidence is non-empty (the mechanical tell), and § Answered when, § Invariants, § Limits, § Reserved gates are filled below. § Question, § Answered when, and § Close rule were drafted by the agent and ratified by the owner in-session ("go", 2026-08-30). Nothing here is edited in place; corrections go in § Amendments.

## Question

> Can the magnet system's field, feasibility, and cost be derived from its own engineering design — coil geometry and current giving the peak field, a stress or current-density limit that pushes back on coil sizing, and magnet cost split into separately sized winding-pack / structure / cryoplant accounts — instead of cited constants?

`[AGENT] (ratified by owner 2026-08-30)`. This is rubric v1 Row 3's target state (P3/S3) phrased as a question; the rubric's anchors are the operative meaning of every term (`.project/active/demo-depth-rubric/rubric.md@dc0f0b6d`, Row 3).

## Consumer

The methodology owner, through demo epic Item 10 (`.project/backlog/epic_stellarator_mbse_demo.md@fc80e5b2`): the answer is the first measured maturation delta — a fresh re-grade of Row 3 against the frozen rubric — feeding the eventual reveal-readiness condition. `[INHERITED: .project/concepts/stellarator-demo-maturation.md@dc0f0b6d SC-3/SC-4]`

Secondary consumers: the open magnet-study findings — DISCOVERY_LOG rows joined to `20260823-magnet-technology-ab` § 15 (no coil/stress coupling; field unrewarded) — any round whose evidence touches those rows owes dispositions (`GOAL_RUNBOOK.md` § The discovery log). `[INHERITED: exploration/stellarator_e2e/studies/DISCOVERY_LOG.md@00bc1928]`

## Answered when

> A fresh re-grade against rubric v1 (`rubric.md@dc0f0b6d`) scores R3.P = 3 and R3.S = 3 with the anchors' full conjunctions evidenced, the validation battery green and affected studies re-run clean — or a round shows with sourced evidence that a target cannot be met without reopening an owner ruling, and the owner rules.

`[AGENT] (ratified by owner 2026-08-30)`. Made explicit so two readers agree:

- **Both directions end the goal.** Reaching P3/S3, or a sourced, written showing that the target needs an owner-gated reopening (with the ruling then made) — either is an answer. A bounded negative is a first-class result.
- **The re-grade is by a fresh non-author grader against the same rubric sha** (grading protocol, `rubric.md@dc0f0b6d` § Grading protocol) — the delta claim rests on the frozen yardstick, not the round's own reading.
- **"Clean" for study re-runs:** re-run without crashes or unexplained constraint-verdict flips; explained flips are findings, not failures. `[INHERITED: .project/concepts/stellarator-demo-maturation.md@dc0f0b6d SC-3]`

## Invariants

- **Package:** at most one promoted pin per round; every comparison inside a round runs against that pin's package identity (`modeling_project/STUDY_POLICY.md`; `.claude/skills/run-study/runbook.md`). The executed baseline entering this goal: package `f97f0848…`, case `stellarator-baseline-point-v1:c0000`, model `dc0f0b6d` (`exploration/stellarator_e2e/studies/20260829-p-pump-fence/results/baseline_result.json@fc80e5b2`).
- **Comparison:** "better" means rubric v1 Row-3 anchor tests at `rubric.md@dc0f0b6d`. Re-grades cite the same rubric sha; a rubric revision (owner-gated, concept OQ6) re-scores both model states before any delta claim. Headline capital/LCOE moves are expected and honest — no fitting to prior headlines; SV-016 (Q_eng band) stays `pending`, record against it, never fit it `[OWNER standing, work/orchestration/stale-basis-recompute.md@00bc1928]`.
- **The 1costingFE handshake is NOT an invariant.** Anchor A is closed evidence at the pin (`f22bd288`); this goal neither re-runs nor preserves it `[OWNER 2026-08-30, pin addendum work/orchestration/stale-basis-recompute.md@00bc1928]`.
- **Clean room binds.** This is model-facing work: PROTOCOL §2/§3 apply in full; the §8 yardstick exemption does not extend here; the four sealed PDFs stay unread; physics from admissible sources, engineering/cost from 1costingFE (pinned `0254385`) `[INHERITED: knowledge/holdout/aries-cs/PROTOCOL.md@dc0f0b6d]`.

## Grounding evidence

- `.project/active/demo-depth-rubric/rubric.md@dc0f0b6d` — Row 3 anchors and targets; the frozen yardstick.
- `.project/active/demo-depth-rubric/grading.md@fc80e5b2` — R3.P = 1, R3.S = 2 with per-cell evidence; grader note G5 (the computed cryo chain); author dispositions.
- `.project/active/demo-depth-rubric/gap-report.md@fc80e5b2` — Band A entry 2: 39.3% of overnight capital, $1.93B single-errata swing, `peak_field_ok` held×held.
- `exploration/stellarator_e2e/studies/20260823-magnet-technology-ab/synthesis.md@00bc1928` — findings #3/#4: no coil-thickness/stress coupling; field reaches no plasma channel but beta.
- `models/library/analyses/mfe_magnet_cost.sysml@00bc1928` — conductor-quantity cost, markup 5.87 swallowing winding/quench/cryostat/testing; `models/library/cost_structure/mfe_power_core.sysml@00bc1928:65` — the 8-attr part def; `models/designs/stellarator_09/stellarator_plant.sysml@00bc1928` `:133` (B = 9.0 held), `:153` (peak ratio held), `:161` (B_max 24.9 held).
- `work/orchestration/stale-basis-recompute.md@00bc1928` — the pin addendum freeing this goal from the handshake duty.

## Limits

| Limit | This goal |
|---|---|
| Retry cap | 2 retries (3 attempts) |
| Checkpoint revision cap | 2 revisions (3 submissions) |
| Round limit | 6 rounds |
| Time or iteration limit | none |

## Reserved gates

1. **Reopening any owner scope ruling** — Rung C confinement (`mfe_plasma_scaling.sysml:163`), held `p_pump` (WI-033) — a strategy may propose, the owner rules; never assumed. `[INHERITED: .project/concepts/stellarator-demo-maturation.md@dc0f0b6d Non-Goals]`
2. **New source ingestion** — only through the native registration seam (one write door), admissibility vetted under PROTOCOL §3; no fallbacks — a missing input is surfaced with honest options, never defaulted. `[OWNER standing]`
3. **Model changes land through the native modeling PM** with its validation levels; merge, push, and item close stay owner-held. `[INHERITED: GOAL_RUNBOOK.md]`
4. **Rubric revision** (if a Row-3 anchor turns out contestable) — owner-gated; concept open question 6.

## Close rule

The owner closes — on the § Answered when condition, or by redirect at any round boundary. `[AGENT] (ratified by owner 2026-08-30)`

## Amendments

### 2026-09-01 — goal closed by owner ruling

§ Answered when met — a fresh non-author Row-3 re-grade at `rubric.md@dc0f0b6d` reads R3.P = 3 (was 1) and R3.S = 3 (was 2), the validation battery is green, and the "affected studies re-run clean" conjunct is satisfied on the owner's reading (a) of 2026-09-01. Closed per § Close rule on the round 2 review's recommendation. Ruling, the reading against all three affected studies, and the effects are recorded at `trail.md` § Goal close. Operator's pen.

### 2026-09-01 — reserved gate 1 was not an owner ruling (provenance correction)

§ Reserved gates item 1 names "Rung C confinement (`mfe_plasma_scaling.sysml:163`), held `p_pump` (WI-033)" as owner scope rulings a strategy may only propose reopening. Half of that is wrong, and the goal ran two rounds under it.

- **Confinement was never ruled out of scope by the owner.** The owner, in session 2026-09-01: "I'm not sure when I ever ruled anything out of scope"; "nothing is sacred here." The phrase originated as an agent's scope note in a model doc comment — the item then being built did not cover the closure — was recorded honestly as `[AGENT]` in the concept's Non-Goals, and was then promoted here to owner grade. The `[INHERITED]` tag on the gate is accurate about the path and wrong about the authority: an `[AGENT]` item cannot be inherited as an owner ruling. Effect on this closed goal's record: `20260823-magnet-technology-ab#4` was never blocked by an owner gate, and the two rounds' "blocked on the standing Rung C owner gate" statements are to be read as blocked on an agent's scope note that no one had re-derived. Nothing else in the goal's evidence or its scores depends on it — the strategy declined confinement coupling on its own terms, and the re-grade scored what was built.
- **The `p_pump` ruling is real but narrower than the gate implies.** It bars expressing `p_pump` as a fixed fraction of thermal power, for a stated reason `[OWNER-VERBATIM 2026-08-28]`. The owner's context, given 2026-09-01: it was approving a change from a hard-coded wrong value to a hard-coded better one, not settling how pumping power must be represented. Computing pumping power from a loop model is outside what it rejected.

Full correction and its two deliberately-unedited stale homes: `.project/concepts/stellarator-demo-maturation.md` § Corrections — 2026-09-01, which is the authority until they land.
