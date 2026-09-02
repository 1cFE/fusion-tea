# Trail: operating-point-closure

What happened, and what was decided. Append-only, newest entry last, ISO dates; no entry is ever edited in place — corrections are `### Amendment` entries. This file logs judgment, not routine stage motion; native workflows keep their own stage records and are cited, never restated. Procedure: `work/orchestration/GOAL_RUNBOOK.md`.

Goal grounded 2026-09-01 (`goal.md`, owner-present session). No round open.

## Round 1 — solve-the-operating-point

### Strategy revision — 2026-09-01

- **Approach:** close the operating point in three linked moves, physics from the admissible Stellaris source, executable through the established Rung-B handwritten codegen seam: (1) an ISS04 confinement-time calc (`stellaris-design-details.md` Eq. A.7 with the `f_ren` multiplier, image `page_031_eq_5.png`) from machine quantities — a, R, ι, the WI-035-derived B, density — and heating power; (2) a steady-state power-balance closure that solves peak temperature from field, density, and external heating (alpha heating from the existing Bosch-Hale machinery plus P_aux, balanced against W/τ_E), retiring held temperature as an entry point so fusion power, beta, and wall load respond to the machine; (3) pushback on computed operands: `beta_ok`'s operand becomes fully machine-responsive through the solved temperature, and a density or confinement-quality limit is added if and only if an admissible printed basis exists — no fallbacks.
- **Assumptions:** Eq. A.7/A.8 and the parameters they need (ι, f_ren) survive image verification in the admissible source; an iterative/fixed-point solve is implementable and oracle-guardable in the handwritten codegen stage (WI-022 `dt_fusion_power` precedent — numerical integration already lives there); P3 is reachable with temperature solved and density kept as a design lever (the Row-1 anchor asks the relation to *link* field and heating to density and temperature, not to solve every quantity); ι and f_ren are held sourced machine/quality facts, the k_link pattern.
- **Abandonment conditions:** the solve cannot be made convergent and verifiable across the study domain; a load-bearing quantitative basis fails image verification with no admissible substitute (surfaced with honest options, never defaulted); or the Row-1 anchor reading proves contestable such that only a rubric revision (owner-gated, concept OQ6) could settle it — that goes to the owner through the close rule, not around them.
- **Intended model increment:** library calc defs for ISS04 τ_E and the power-balance temperature solve; the plasma spine rewired so fusion power, beta, and wall load consume the solved temperature; the beta/density/power pushback asserted on computed operands; instance rebinds in `stellarator_09`; entry-point retirement with the committed-study restatement duty (goal invariants).
- **Intended study question:** with the operating point solved from the machine, is field rewarded — does the constrained optimum leave the beta floor (the `20260823-magnet-technology-ab#4` pathology) — and where do the confinement-linked limits bind over (B, density, P_aux) and (R, a)?

### T-001 scope

- **Objective:** register the modeling work item and produce its spec for the operating-point-closure model increment.
- **Why now:** the goal is grounded (`goal.md`, 2026-09-01 — uncommitted this session, operator holds commits; unpinned until the grounding commit lands); a standard-scale modeling change enters the native modeling PM at the spec stage, and the spec is where the increment's outcome-level shape gets fixed.
- **Scope:** authorized — `pm add-item` under the modeling PM, `work/active/WI-XXX_*/spec.md`, VALIDATION_MATRIX entries through `pm add-validation`; excluded — design/plan/implement stages, any `models/` edit, any source ingestion, discovery-log writes.
- **Inputs:** `goal.md` (no narrower constraint).
- **Done when:** the spec exists, requirements-complete at outcome level, and is presented to the owner in-session; under the 2026-09-01 delegation the round agent may approve progression if the owner does not rule.
- **Stop when:** a discovered prerequisite, a strategy blocker, an owner gate, or a declared limit.

### T-001 start — 2026-09-01

Task T-001 under § T-001 scope: mint the operating-point-closure modeling work item through the modeling PM (`pm add-item`) and write its spec at `work/active/WI-XXX_operating-point-closure/spec.md`. Expected artifacts: one new `work/BACKLOG.md` row, one `spec.md`, SV rows via `pm add-validation`.

### T-001 return — 2026-09-01

- **Outcome:** `COMPLETE`. Both halves of § T-001 scope's done-when hold on disk — the work item exists and its spec is written — and the spec is presented to the owner in-session with the two delegation-ruled decisions surfaced for override.
- **Evidence:**
  - `work/BACKLOG.md` — `WI-037` "Operating-Point Closure: ISS04 Confinement Solve, Machine-Responsive Temperature", `scale: standard`, `priority: P0`, under the MFE Cost Modeling — Tokamak & Stellarator epic; minted by `pm add-item`.
  - `work/active/WI-037_operating-point-closure/spec.md` — seven outcome-level requirements (MR-WI037-1..7): τ_E computed from machine and heating via ISS04 with sourced held f_ren/ι; temperature solved from the steady-state power balance, convergent-or-loud, held temperatures retired; a beta/density/power limit pushing back on a fully machine-responsive operand with the field-reward channel structurally present; library/instance split; image-verified citations, no fallbacks; standing rulings preserved at their real width (no confinement gate — the concept's 2026-09-01 correction cited as authority); entry-point/committed-study restatement before any regeneration. § Open decisions records the two agent rulings under the 2026-09-01 delegation.
  - `modeling_project/VALIDATION_MATRIX.md` — SV-041/042/043 added `pending` via `pm add-validation`, one per functional requirement. The parser's 'Invalid Type' warnings (escaped text in pre-existing rows) predate this task and were not touched.
- **Reading:** the increment has a native, auditable contract and nothing under `models/` moved. The comparison-meaning stake (retiring held temperatures changes what every committed study that held them means) is carried as MR-WI037-7, the WI-035 restatement shape. Discovery row `20260823-magnet-technology-ab#4` is touched as evidence but no disposition row is appended yet: its honest routing ("routed → WI-037") becomes real when the increment lands, and the round owes the disposition before it closes.
- **Decision:** trigger — the spec's two outcome-shaping calls (lever direction; ash treatment) have no owner gate to stop at. Decision and reason — rule them as the round agent under the owner's 2026-09-01 delegation ("no gates. you must use your best engineering and modeling judgement"): (1) solve temperature, keep density as the design lever — temperature is what confinement physics determines at a given machine and density, and the anchor's density-limit pushback presumes density is choosable; held T_i0/T_e0 retire with the restatement duty; (2) ash stays a held, disclosed referent — the source's own ash treatment is a heuristic suppression factor, and coupling it needs a further held-fact chain this increment does not carry. Both surfaced to the owner in-session for override. Tier — execution detail (under recorded delegation). Who decided — the round agent, 2026-09-01. What changed — `work/active/WI-037_operating-point-closure/spec.md` § Open decisions.
- **Decision:** trigger — nothing is committed. Decision and reason — the operator holds commits (round-1 precedent at goals `cryo-volume-basis`/`magnet-closure`); the working tree carries the goal directory, the WI-037 spec, and the two op-written registry files. Tier — execution detail. Who decided — the round agent, 2026-09-01. What changed — `none`.

**Next task:** not chosen — picked after the owner has seen the spec (design is the native next stage; under the delegation the round agent may proceed if the owner does not rule otherwise).

### Owner directive — 2026-09-01

The owner, in session: full execution of the goal is delegated to the round agent ("take ownership and accountability, and execute the entire goal") `[OWNER-VERBATIM 2026-09-01]`. Merge, push, work-item close, and the goal-close ruling remain owner-held (`GOAL_RUNBOOK.md` § What this is, and what it is not). Fresh-session gates (disposition checkpoint, round review, the answered-when re-grade) are satisfied by spawned non-author sessions with spawn prompts deposited as evidence — the magnet-closure round-2 grader precedent (`work/orchestration/goals/magnet-closure/evidence/round2_T-001_grader_prompt.md`). Commits on the working branch are working practice; the operator rules the merge.

### T-002 scope

- **Objective:** produce the WI-037 design — mechanisms for the three moves (ISS04 τ_E calc, steady-state temperature solve, machine-responsive pushback), every quantitative basis image-verified, under the spec's § Open decisions rulings.
- **Why now:** the spec is complete and presented; design is the native next stage and the place the balance form, solve architecture, lever set, tolerances, and the density-limit admissibility question get fixed.
- **Scope:** authorized — `work/active/WI-037_operating-point-closure/design.md`, source/image verification reads, throwaway prototypes outside `models/`; excluded — plan/implement stages, any edit under `models/` or `exploration/`, source ingestion, discovery-log writes.
- **Inputs:** `work/active/WI-037_operating-point-closure/spec.md`, `goal.md` (no narrower constraint).
- **Done when:** design.md exists, requirements-complete against MR-WI037-1..7, values image-verified, solve architecture prototyped enough to state convergence behavior honestly.
- **Stop when:** a discovered prerequisite (e.g. a value failing image verification with no admissible substitute), a strategy blocker, or a declared limit.

### T-002 start — 2026-09-01

Task T-002: write the WI-037 design through the native design stage. Native target: `work/active/WI-037_operating-point-closure/design.md`. Expected artifacts: one design document plus prototype scratch outside the repo trees.

### T-002 return — 2026-09-01

- **Outcome:** `STRATEGY_BLOCKER`. The design was not written: prototyping the solve before fixing mechanisms (the § T-002 scope's stated purpose) fired the strategy's declared abandonment condition — "the solve cannot be made convergent and verifiable across the study domain." No edit under `models/` occurred; WI-037's spec stands as written pending the next round's strategy.
- **Evidence:** `work/orchestration/goals/operating-point-closure/evidence/T-002_prototype/` — `NOTES.md` (findings, with every basis image-verified against the iter-02 raw PDF or page images and cited), scripts, and raw outputs. Uncommitted at write time; committed with this round's close.
- **Reading.** Two-sided result. (a) The forward physics chain validates against the printed Stellaris point A with nothing fitted: ISS04 τ_E −0.1% (with n19 read as line-averaged, its "usual meaning"), composed radiation −0.1% (brems + W-line + Albajar sync vs printed photon power), A.5/A.6 ash chain +3.6%, quasi-neutral p_fus +0.7%; the one outlier is the stored-energy form (+9.2%), amplified ×2.56 by the closure into the dominant balance residual. (b) The solve-T architecture is unworkable here: the printed point is ~90 MW short of self-sustaining and sits on the unstable branch; at the baseline machine no stable feasible burn exists inside the conductor-ceiling/stress/wall/beta limits; and the burn attractor amplifies power residuals ~×3 into temperature. A solved-T baseline is unevaluable at the current machine, and study sweeps would carry large no-burn voids — the p-pump-fence evaluability lesson at scale.
- **Decision:** trigger — prototype findings 3 and 4 (`NOTES.md`) fire the declared abandonment condition. Decision and reason — return `STRATEGY_BLOCKER` and close the round rather than silently re-architecting mid-round: the strategy's intended model increment ("power-balance temperature solve") is refuted by evidence, and the runbook closes a round when the strategy's premise is wrong; the successor architecture (forward sustainment fence) is recorded in `NOTES.md` § Consequence as input to the next strategy, which the fresh reviewer authors, not this session. Tier — premise surprise. Who decided — the round agent, 2026-09-01. What changed — the evidence directory; this trail.
- **Decision:** trigger — the prototype needed ι_{2/3}, absent from every table. Decision and reason — read it from Fig. 11(a) at s = 2/3 on the design-β curve (0.92 ± 0.01), bracketed by the printed axis/edge values 0.86/0.98 — an image-verification act (the WI-022 Fig-16 digitization precedent), not a default; the 0.41 exponent makes the read tolerance ±0.45% in τ_E. Tier — execution detail. Who decided — the round agent, 2026-09-01. What changed — `NOTES.md` § Verified bases.

## Round 1 result — 2026-09-01

- **Intent:** unmet — the round set out to land a solved-T operating-point closure and close Row 1; it lands a bounded negative on the architecture plus a validated forward physics chain. Unmet is a legitimate result.
- **Task sequence:** T-001 (mint WI-037 + spec) `COMPLETE` · T-002 (design, prototype-first) `STRATEGY_BLOCKER`.
- **Last semantic outcome:** `STRATEGY_BLOCKER` (T-002).
- **Stop reason:** last outcome `STRATEGY_BLOCKER` + no limit reached → round closes on trigger 2 (strategy blocker: the premise "P3 is reachable with temperature solved" is refuted at this machine by the round's own evidence).
- **Evidence refs:** `work/active/WI-037_operating-point-closure/spec.md` (T-001); `work/BACKLOG.md` WI-037 row; `modeling_project/VALIDATION_MATRIX.md` SV-041..043 (pending); `work/orchestration/goals/operating-point-closure/evidence/T-002_prototype/` (NOTES.md, scripts, outputs); all committed with this close (this branch, operator holds merge/push).
- **Learning delta (proposed):**
  - L-001: The Stellaris appendix closure (A.3 balance, A.7/A.8 ISS04 with P = W/τ_E, A.5/A.6 ash) is fully admissible and reproduces the printed point-A τ_E, photon power, ash density, and fusion power to ≤4% each with nothing fitted, provided ISS04's n19 is read as line-averaged (vol-av misses τ_E by −23%); the model's analytic W-form (+9.2%) is the dominant fidelity gap and enters conducted loss as W^2.56.
  - L-002: A solved-T operating point is the wrong architecture for this model state: no stable feasible burn exists at the baseline machine inside its own limits, the printed point sits on the unstable branch ~90 MW short of self-sustaining, and near-marginal attractors amplify power error ~×3 into temperature. Forward sustainment (required-aux vs installed, a power limit per the Row-1 anchor) is exact everywhere, keeps studies restatable, and leaves the baseline evaluable.
  - L-003: With confinement in the chain, field is rewarded (loss ∝ B^−2.15 effective) and the reward immediately collides with the conductor ceiling and the WI-035 stress fence — the `magnet-ab#4` pathology becomes a real three-way trade instead of a free descent to the beta floor.
- **Finding dispositions:** discovery row `20260823-magnet-technology-ab#4` was touched as evidence (T-001, T-002). No disposition row is appended: the round landed no model change, so the finding has not moved; its routing target (WI-037) exists but is `backlog`-stage work. The row stays open; the next round owes the disposition when the increment lands. No other open row was touched.
