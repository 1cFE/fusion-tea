# Goal: operating-point-closure — can the plasma operating point be solved from the machine instead of prescribed?

Drafted and grounded 2026-09-01 in an owner-present session. Procedure is `work/orchestration/GOAL_RUNBOOK.md` § Grounding a goal; this file does not restate it.

Provenance: `[AGENT]` for what this session supplied, `[INHERITED: <path>]` for what a repository artifact carries. The owner was present in this session: the slug and § Reserved gates were ruled `[OWNER-VERBATIM 2026-09-01]`; the drafted § Question, § Answered when, and § Close rule were presented as explicit proposals and adopted under the owner's same-session delegation — "you must use your best engineering and modeling judgement" — and carry `[AGENT] (delegated by owner 2026-09-01)`. The owner may amend any of them.

## Status

`grounded` — 2026-09-01. All five field classes are non-hollow (`GOAL_RUNBOOK.md` § Grounding a goal): § Grounding evidence is non-empty (the mechanical tell), and § Answered when, § Invariants, § Limits, § Reserved gates are filled below. Nothing here is edited in place; corrections go in § Amendments.

## Question

> Can the plasma operating point be solved from the machine — a confinement or transport relation linking field and heating power to density and temperature, with a beta, density, or power limit pushing back on the choice — instead of prescribed as typed-in density, temperature, and profile inputs?

`[AGENT] (delegated by owner 2026-09-01)`. This is rubric v1 Row 1's target state (P3) phrased as a question; the rubric's Row-1 anchor text is the operative meaning of every term (`.project/active/demo-depth-rubric/rubric.md@dc0f0b6d`, Row 1).

## Consumer

The methodology owner, through demo epic Item 10 (`.project/backlog/epic_stellarator_mbse_demo.md`): the answer is the second measured maturation delta — a fresh non-author Row-1 re-grade against the frozen rubric — feeding the eventual reveal-readiness condition. `[INHERITED: .project/concepts/stellarator-demo-maturation.md@81a4fee8 SC-3/SC-4]`

Secondary consumer: discovery row `20260823-magnet-technology-ab#4` (no confinement closure — field reaches no plasma channel but beta, so field is never rewarded and the optimum drives to the lowest B the beta limit allows), open and unrouted in `exploration/stellarator_e2e/studies/DISCOVERY_LOG.md@81a4fee8`. This goal is its natural routing target; any round whose evidence touches it owes a disposition (`GOAL_RUNBOOK.md` § The discovery log).

## Answered when

> A fresh non-author re-grade against rubric v1 (`rubric.md@dc0f0b6d`) scores R1.P = 3 with the anchor's full conjunction evidenced — a confinement/transport relation links field and heating to density and temperature, **and** a beta, density, or power limit pushes back on the choice — with the validation battery green and affected studies re-run clean; or a round shows with sourced evidence that the target cannot be met without an owner ruling, and the owner rules.

`[AGENT] (delegated by owner 2026-09-01)`. Made explicit so two readers agree:

- **Both directions end the goal.** Reaching P3, or a sourced, written showing that the target is unreachable without an owner decision (with the ruling then made) — either is an answer. A bounded negative is a first-class result.
- **The re-grade is by a fresh non-author grader against the same rubric sha** (grading protocol, `rubric.md@dc0f0b6d` § Grading protocol) — the delta claim rests on the frozen yardstick, not the round's own reading.
- **"Clean" for study re-runs:** re-run without crashes or unexplained constraint-verdict flips; explained flips are findings, not failures. `[INHERITED: .project/concepts/stellarator-demo-maturation.md@81a4fee8 SC-3]`

## Invariants

- **Package:** at most one promoted pin per round; every comparison inside a round runs against that pin's package identity (`modeling_project/STUDY_POLICY.md`; `.claude/skills/run-study/runbook.md`). The executed baseline entering this goal: package identity `75f90a24…`, case `stellarator-baseline-point-v1:c0000`, model `ffa38c05` — LCOE 304.482, seven verdicts satisfied (`exploration/stellarator_e2e/studies/20260830-stress-fence/results/baseline_result.json@04b258d4`).
- **Comparison:** "better" means rubric v1 Row-1 anchor tests at `rubric.md@dc0f0b6d`. Re-grades cite the same rubric sha; a rubric revision (owner-gated, concept OQ6) re-scores both model states before any delta claim. Headline LCOE/feasibility moves are expected and honest — no fitting to prior headlines; SV-016 (Q_eng band) stays `pending`, record against it, never fit it `[OWNER standing, work/orchestration/stale-basis-recompute.md]`.
- **Comparison-meaning stake, named up front:** solving the operating point retires held quantities (densities, temperature, possibly profile exponents) as settable entry points — the magnet-closure inversion precedent (WI-035 checkpoint decision 1). Committed studies that swept or held those axes are restated, never silently broken. Which levers retire is the round agent's call under the 2026-09-01 delegation; the restatement duty is not waivable.
- **The 1costingFE handshake is NOT an invariant.** Anchor A is closed evidence at its pin; this goal neither re-runs nor preserves it `[OWNER 2026-08-30, pin addendum work/orchestration/stale-basis-recompute.md]`.
- **Clean room binds.** This is model-facing work: PROTOCOL §2/§3 apply in full; the four sealed PDFs stay unread; physics from admissible sources; engineering and cost from 1costingFE (pinned `0254385`) `[INHERITED: knowledge/holdout/aries-cs/PROTOCOL.md; restated by the owner in the 2026-09-01 grounding instruction]`.

## Grounding evidence

- `.project/active/demo-depth-rubric/rubric.md@dc0f0b6d` — Row 1 anchors and target (P3 / S not_applicable); the frozen yardstick. Its Row-1 gate note repeats the stale "Rung C" framing; per the concept's § Corrections — 2026-09-01, that note is stale text awaiting the next rubric version, and the concept correction is the authority.
- `.project/concepts/stellarator-demo-maturation.md@81a4fee8` § Corrections — 2026-09-01 — confinement was never ruled out of scope; it is open work, groundable like any other. This grounding, done owner-present, is the owner opening it. No agent may cite a Rung C gate as authority.
- `.project/active/demo-depth-rubric/grading.md@fc80e5b2` — R1.P = 2 with the why_not_next naming exactly this gap: no confinement/transport relation links field and heating to density and temperature; densities, temperatures, and profile exponents are held source referents.
- `.project/active/demo-depth-rubric/gap-report.md@fc80e5b2` — Band A entry 4: the broadest structural gap and the explanation for the field-unrewarded pathology.
- `exploration/stellarator_e2e/studies/20260823-magnet-technology-ab/synthesis.md@d92c5316` finding #4 — the measured, committed pathology; `exploration/stellarator_e2e/studies/DISCOVERY_LOG.md@81a4fee8` — the open row.
- `models/library/analyses/mfe_plasma_scaling.sysml@ba5c9945` — the genuinely-computed P2 spine (profile-integrated fusion power, volume-averaged beta, wall load, peak field) and the held operating-point inputs it hangs from (instance bindings `models/designs/stellarator_09/stellarator_plant.sysml:450-462` region).
- `knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md@e5a2cb23` — the ISS04 confinement scaling, Eq. A.7 with the `f_ren` multiplier and the temperature-rewritten form A.8 (`images/page_031_eq_5.png`); admissible, already screened for model work (WI-022 precedent). Density-limit literature is referenced in the same source's bibliography.
- `.project/active/demo-depth-rubric/grading-r3-regrade.md@0cf0cf41` — the model state and package identity the goal enters at (Row 3 at target; the first maturation delta this goal's chain extends).

## Limits

| Limit | This goal |
|---|---|
| Retry cap | 2 retries (3 attempts) |
| Checkpoint revision cap | 2 revisions (3 submissions) |
| Round limit | 6 rounds |
| Time or iteration limit | none |

## Reserved gates

> "no gates. you must use your best engineering and modeling judgement" — `[OWNER-VERBATIM 2026-09-01]`, ruling on this session's five proposed gates (entry-point retirement, the `p_pump` ruling's width, source ingestion, native-PM routing, rubric revision).

The owner reserves no goal-specific gates: execution decisions — which entry points retire, source admissibility judgment under the standing seams, anchor readings — are the round agent's, on its best engineering and modeling judgment. What remains held is structural, restated from its standing homes rather than minted here: merge, push, and work-item close stay the owner's (`GOAL_RUNBOOK.md` § What this is, and what it is not; owner's grounding instruction 2026-09-01), and model changes still land through the native modeling PM with its validation levels — that is workflow routing, not a gate.

## Close rule

The owner closes — on the § Answered when condition, or by redirect at any round boundary. `[AGENT] (delegated by owner 2026-09-01)`

## Amendments

None.

### 2026-09-02 — goal closed by owner ruling

§ Answered when met in the affirmative direction: a fresh non-author Row-1 re-grade at `rubric.md@dc0f0b6d` reads **R1.P = 3 (was 2), Row 1 at target** (`.project/active/demo-depth-rubric/grading-r1-regrade.md`), the validation battery is green, and the "affected studies re-run clean" conjunct is satisfied on the owner's reading of 2026-09-02 (the magnet-closure (a) analogue). Closed per § Close rule on the round-2 review's recommendation, after two rounds of the six allowed. The five close rulings — anchor stands ("links"); conjunct satisfied; both escape routes minted (WI-038, WI-039), neither grounded; Row 4's target raise deferred to the next rubric version; admin executed with merge/push owner-held — are recorded at `trail.md` § Goal close. Owner present; rulings taken one at a time.
