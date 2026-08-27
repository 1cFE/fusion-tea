# Trail: cryo-volume-basis

What happened, and what was decided. Append-only, newest entry last, ISO dates. **No entry is ever edited in place.** A correction is `### Amendment YYYY-MM-DD — amends <entry heading>`, stating what changed and why.

This file logs judgment, not routine stage motion. Native workflows keep their own stage records; entries here cite them by path or native id and never restate their content. Procedure is in `work/orchestration/GOAL_RUNBOOK.md`; the question and its gates are in `goal.md`, which this file does not restate.

## Round 1 — route-then-derive

### Strategy revision — 2026-08-26

- **Approach:** put the question where the repository can audit it before arguing it in the trail. The discovery row already names its home — a modeling item under the MFE cost-modeling epic — so the round's first move is to make that item exist natively and take the row out of `unrouted`. The derivation itself (is there a defensible route from the ampere-turns the package already carries to the 136.56 m³ anchor, and at what tolerance) then happens inside that item's own spec/design stages, under WI-030's precedent for turning a typed-in input into a computed one, rather than as prose in this file. The round reads the item's native evidence and decides at goal level what it establishes.
- **Assumptions:** (1) the MFE cost-modeling epic is the right and live home for the item (`work/backlog/epic-mfe-cost-modeling.md@f22bd288`, `Status: active`); (2) `total_kAm` in `models/library/analyses/mfe_magnet_cost.sysml@8f3b510c` is the only ampere-turn quantity the package carries, so it is the only candidate left side of the identity; (3) the 27–41 % gap `goal.md` § Grounding evidence recorded is a form-factor question about what `G * B * R0 * r_coil / mu0` physically is, not an arithmetic or data error.
- **Abandonment conditions:** the strategy is abandoned if the modeling item's own derivation shows no route from quantities the package already carries to the anchor without a new sourced input — at which point the round's honest product is a reasoned "keep it held", not a landed computation. It is also abandoned if closing the gap turns out to require coil thickness or radial build (discovery row `#3`) or a re-basing of `f_carnot_cryo`; both are reserved gates in `goal.md` § Reserved gates and neither is this round's to open.
- **Intended model increment:** `vol_cold_cryo` in `models/designs/stellarator_09/stellarator_plant.sysml` computed from the carried ampere-turns and a concept-specific `J_eng`, with the per-conductor value living in `designs/` and not in the library calc (MR-3, restated in the epic file). Nothing in `models/library/` is intended to move.
- **Intended study question:** none committed this round. A study would need a regenerated, verified, pinned package, and the `integrate` seam has no native procedure and no documented hand pattern (`GOAL_RUNBOOK.md` § The native seams), so reaching it is a `PREREQUISITE` return to the operator. If the seam were open the question would be whether a computed volume moves the arm-B headline off the ceiling where the committed study's result is exact.

**No future task list.** The next task is chosen from evidence after the previous one returns.

### T-001 scope

- **Objective:** route discovery row `20260823-magnet-technology-ab#2` to the home its own row names — the native modeling work item must exist under the MFE cost-modeling epic, and the row must carry a disposition that is not `unrouted`.
- **Why now:** it is the strategy's first move, and it is load-bearing for the goal in both directions: `goal.md` § Answered when requires a non-`unrouted` disposition on this row whether the answer is yes or no. The triggering evidence is the row itself — `exploration/stellarator_e2e/studies/DISCOVERY_LOG.md@31f9eb0b:20`, disposition `unrouted`, home "modeling item under the MFE cost modeling epic", with nothing appended under the id since the sighting.
- **Scope:** authorized — mint one work item through the modeling PM's own operation (`agentic-mbse pm add-item`) under the epic, and append one joined disposition row under the existing id per `GOAL_RUNBOOK.md` § The discovery log. Explicitly excluded — writing the item's spec, design, or plan; any edit under `models/`; any DI mint or amendment to DI-010; any change to `f_carnot_cryo`; discovery row `#3`; closing or archiving any item; `git commit`, push, or merge.
- **Inputs:** `goal.md` (this task adds no constraint narrower than what it already carries), `exploration/stellarator_e2e/studies/DISCOVERY_LOG.md@31f9eb0b`, `exploration/stellarator_e2e/studies/20260823-magnet-technology-ab/record.md@e204aee7` § 15, `work/backlog/epic-mfe-cost-modeling.md@f22bd288`, `work/BACKLOG.md@ffa5c54c`.
- **Done when:** a work item id for the cold-volume basis exists in `work/BACKLOG.md` under the MFE Cost Modeling epic, and `DISCOVERY_LOG.md` carries a new row under `20260823-magnet-technology-ab#2` naming that item, with a disposition category from ADR-004's four and a status, responsible party, and next reference.
- **Stop when:** the modeling PM operation refuses the mint or the epic is not addressable by name (prerequisite); or minting turns out to require a decision `goal.md` § Reserved gates holds for the owner.

### T-001 start — 2026-08-26

Route discovery row `20260823-magnet-technology-ab#2` · native target: the modeling PM, epic "MFE Cost Modeling — Tokamak & Stellarator" in `work/BACKLOG.md`, plus `exploration/stellarator_e2e/studies/DISCOVERY_LOG.md` · expected artifact: one minted work item (next id, expected `WI-032`) registered under that epic, and one appended disposition row under the existing finding id.

### Stop — 2026-08-26

Kind: interruption

- **What was in flight:** T-001, opened by the start line above and never returned. The start line named two expected artifacts: a minted work item under the MFE Cost Modeling epic, and one appended disposition row under `20260823-magnet-technology-ab#2`.
- **What the native state shows (read as truth, not from the trail):** the mint landed and the row did not. `work/BACKLOG.md:100-104` carries `WI-032` "Cold-volume basis: vol_cold_cryo computed or held", `scale: standard`, `status: backlog`, inside the `MFE Cost Modeling — Tokamak & Stellarator` epic block (`work/BACKLOG.md:24-28`), and the rendered table row exists at `work/BACKLOG.md:195`. No `work/active/WI-032_*` directory exists, which is correct for a `backlog` item and confirms no spec/design/plan work started. `exploration/stellarator_e2e/studies/DISCOVERY_LOG.md:20` is still the 2026-08-23 sighting with disposition `unrouted`, and no row has been appended under that id.
- **Cited-ref walk (`GOAL_RUNBOOK.md` § When a cited artifact moves):** every ref this round cites is still at the digest it was cited at — `DISCOVERY_LOG.md@31f9eb0b`, `20260823-magnet-technology-ab/record.md@e204aee7`, `epic-mfe-cost-modeling.md@f22bd288`, `stellarator_plant.sysml@ba5c9945`, `mfe_magnet_cost.sysml@8f3b510c`, `KNOWLEDGE.md@ffa5c54c`, `STUDY_POLICY.md@ad2fb4ea`. The one moved path is `work/BACKLOG.md`, moved by T-001's own mint (`a6caab37`), which is the task's work and not an external mutation. No task is voided; the strategy and the comparison meaning stand.
- **Resumed as:** the remaining half of T-001's authorized scope — the disposition row — executed under the scope already recorded, with no re-run of the mint (`GOAL_RUNBOOK.md` § Resuming an interruption: never re-run completed native work). The return follows.

### T-001 return — 2026-08-26

**Outcome:** `COMPLETE`. Both halves of § T-001 scope's "Done when" now hold on disk: the work item exists under the named epic, and the row carries a disposition that is not `unrouted`.

**Evidence refs.**

- `work/BACKLOG.md:100-104` and the rendered row at `:195` — `WI-032`, `scale: standard`, `status: backlog`, inside the `MFE Cost Modeling — Tokamak & Stellarator` epic block (`:24-28`). Minted by the modeling PM's own operation before the interruption (`a6caab37`); this session did not re-run the mint.
- `exploration/stellarator_e2e/studies/DISCOVERY_LOG.md` — one row appended under the existing id `20260823-magnet-technology-ab#2`, dated 2026-08-26, category `model fix`, status "routed, not yet answered", responsible party "goal `cryo-volume-basis`, round 1, task T-001", next reference `WI-032`. The 2026-08-23 sighting at `:20` is untouched. This is the round's one write outside the goal directory (`GOAL_RUNBOOK.md` § The discovery log).
- `tests/study/test_records.py` — 7 passed after the append, so the multi-row join under one id holds (ADR-004's stated failure mode did not fire).

**Goal-level reading.** The row's routing is now real, which is what `goal.md` § Answered when requires in *both* directions. It does not move the question itself one inch: the row is routed, not answered, and the disposition says so in words. The 27–41 % gap recorded in `goal.md` § Grounding evidence is untouched by this task and is still the crux the item has to argue.

**Decision fields.**

1. *Finding or trigger:* the interruption — `T-001 start` with no return, mint landed, row still `unrouted`.
   *Decision and reason:* finish T-001 under its already-recorded scope rather than re-scope or re-mint, because the native artifacts show exactly which half was outstanding and the runbook bars re-running completed native work.
   *Tier:* execution detail. *Who decided:* the resuming round agent, 2026-08-26. *What changed:* `exploration/stellarator_e2e/studies/DISCOVERY_LOG.md` (one appended row); `work/orchestration/goals/cryo-volume-basis/trail.md`.
2. *Finding or trigger:* the disposition category had to be one of ADR-004's four, while the item's answer may yet be "keep it held".
   *Decision and reason:* record `model fix` for the *routing* and state in the row that the item may return a reasoned "keep it held" without reopening the row. The category names where the finding went, not what it will conclude; ADR-004 offers no "routed, undecided" category and minting one would be a quiet procedure change.
   *Tier:* execution detail. *Who decided:* the resuming round agent, 2026-08-26. *What changed:* the wording of the appended row.
3. *Finding or trigger:* `learnings.md` in this goal directory is still the unfilled template, headings and placeholder text included.
   *Decision and reason:* left as is. `GOAL_RUNBOOK.md` § The five surfaces gives that file only one writer — the fresh review, appending an accepted delta — and T-001 produced no accepted learning. Tidying the template from inside a task would be this session writing a surface that is not its to write.
   *Tier:* execution detail. *Who decided:* the resuming round agent, 2026-08-26. *What changed:* `none`.

**Next task:** not chosen by this session. The reason is in the stop entry that follows.

### Stop — 2026-08-26

Kind: handoff

**What is true on disk.** Round 1 is open — a strategy revision, T-001 scope, T-001 start, an interruption stop, and now a T-001 `COMPLETE` return, with no round result. `WI-032` sits at `status: backlog` under the MFE Cost Modeling epic with no spec, design, or plan. Discovery row `20260823-magnet-technology-ab#2` is routed and no longer `unrouted`. Nothing under `models/`, `knowledge/`, or any other native surface moved, and nothing is committed — the operator holds commits.

**What the owner must see — a premise this session will not resolve silently.** The strategy, the T-001 scope, and the T-001 start were authored by a session that no longer exists. This session's authority to touch round 1 comes from `GOAL_RUNBOOK.md` § Resuming an interruption, and that section grants exactly two writes: the missing return, or an interruption stop. It does not say the resumer then picks the next task. ADR-002 pulls the same way from the other side — "a round is one agent's bounded pursuit of one strategy," with the round agent's last act being the round result. Authoring T-002 here would make round 1 a two-agent round on the strength of a licence that was written to re-anchor a trail, not to inherit a strategy.

Reading it the other way is not unreasonable — an open round with work left is `round` mode in `.claude/skills/run-goal/SKILL.md`, and someone has to carry it. The two readings lead to different work, so the choice is the operator's, not this session's (`GOAL_RUNBOOK.md`: the goal layer is not an automation of the owner's judgment).

**The two options, concretely.**

1. **Round 1 continues** — the operator names a round agent for it. The strategy's own next move is already stated and needs no re-derivation: open T-002 to take `WI-032` through the modeling PM's spec stage, where the 27–41 % gap in `goal.md` § Grounding evidence gets argued against WI-030's precedent (`work/completed/20260822_WI-030_computed-beta-peak-field@ffa5c54c`), and where the tolerance against the 136.56 m³ anchor is stated. Reserved gates 1–5 still bind; nothing in a spec stage reaches them, but landing the change does.
2. **Round 1 closes here** — the round agent writes `### Round 1 result` with T-001 as the single task, intent partly met (the row routed; the basis question untouched), and a fresh session reviews it and authors round 2. This costs a round against the limit of 6 for one routing task, which is why it is the operator's call and not a default.

This session cannot pick, and it also cannot review its own work under either option: it wrote the T-001 return, so `GOAL_RUNBOOK.md` § What "fresh" means bars it from the round review.

**The material to review:** this goal directory; `work/BACKLOG.md:100-104,195`; `exploration/stellarator_e2e/studies/DISCOVERY_LOG.md` (newest row, id `20260823-magnet-technology-ab#2`). Uncommitted; the operator owns the commit.

**Resume at:** `GOAL_RUNBOOK.md` § Running one task (option 1) or § Opening and closing a round, then § The fresh review (option 2).

### Resumption note — 2026-08-26

The handoff stop above put a choice to the operator: continue round 1, or close it. The operator's continuation brief names this session the round agent and directs it to take the open round from where the trail stands and decide what it needs next. That is option 1. Round 1 continues under its existing strategy revision, which this session does not re-author.

**Cited-ref walk (`GOAL_RUNBOOK.md` § When a cited artifact moves), run before any work.** Every ref round 1 cites still stands at the digest it was cited at: `20260823-magnet-technology-ab/record.md@e204aee7`, `epic-mfe-cost-modeling.md@f22bd288`, `stellarator_plant.sysml@ba5c9945`, `mfe_plant.sysml@ba5c9945`, `mfe_magnet_cost.sysml@8f3b510c`, `mfe_cryo_plant.sysml@8f3b510c`, `KNOWLEDGE.md@ffa5c54c`, `STUDY_POLICY.md@ad2fb4ea`. The one moved path is `exploration/stellarator_e2e/studies/DISCOVERY_LOG.md`, now at `@4464c354`, moved by T-001's own append — the round's work, not an external mutation. No task is voided; the strategy and the comparison meaning stand. The working tree is clean, so T-001's writes are committed.

### T-002 scope

- **Objective:** does a defensible route exist from quantities the package already carries to the 136.56 m³ anchor, and at what tolerance — argued natively, in `WI-032`'s spec stage, not as prose in this trail.
- **Why now:** it is the strategy's stated next move and the goal's crux. T-001 routed the row without touching the question. The triggering evidence is `goal.md` § Grounding evidence: dividing the model's own `total_kAm` by DI-010's REBCO band gives 173.8–192.4 m³ against a held 136.56 m³, so "the identity already holds, just wire it up" is ruled out and something has to explain the 27–41 % gap before any requirement can be written.
- **Scope:** authorized — take `WI-032` through the modeling PM's spec stage per `.claude/commands/spec-model.md`, producing `work/active/WI-032_cold-volume-basis/spec.md`. Explicitly excluded — any edit under `models/`, `knowledge/`, or `exploration/`; design or plan stages; minting an SV-XXX in `modeling_project/VALIDATION_MATRIX.md`; any DI mint or amendment to DI-010; any change to `f_carnot_cryo`; discovery row `#3`; hand-editing `work/BACKLOG.md`; closing or archiving any item; `git commit`, push, or merge.
- **Inputs:** `goal.md` (this task adds no constraint narrower than what it already carries), `work/completed/20260822_WI-030_computed-beta-peak-field/spec.md@ffa5c54c` as the precedent shape, `models/library/analyses/mfe_magnet_cost.sysml@8f3b510c`, `models/designs/stellarator_09/stellarator_plant.sysml@ba5c9945`, `models/library/analyses/mfe_cryo_plant.sysml@8f3b510c`, `knowledge/KNOWLEDGE.md@ffa5c54c` DI-009/DI-010, `modeling_project/STUDY_POLICY.md@ad2fb4ea`, `exploration/stellarator_e2e/studies/20260823-magnet-technology-ab/record.md@e204aee7`.
- **Done when:** `work/active/WI-032_cold-volume-basis/spec.md` exists and states either a derivation route with a stated tolerance against the 136.56 m³ anchor, or the bounded negative that no route reaches the anchor from carried quantities without a further sourced input, with the arithmetic shown either way.
- **Stop when:** the spec's own load-bearing requirement turns out to need a decision `goal.md` § Reserved gates holds for the owner (owner gate); or closing the gap requires coil thickness, radial build, or a re-basing of `f_carnot_cryo` (strategy blocker — the strategy's declared abandonment condition).

### T-002 start — 2026-08-26

Argue the cold-volume derivation in `WI-032`'s spec stage · native target: the modeling PM, `work/active/WI-032_cold-volume-basis/` · expected artifact: `spec.md` carrying the derivation, the route or the bounded negative, and the tolerance.

### T-002 return — 2026-08-26

**Outcome:** `OWNER_GATE`. The spec exists and the derivation is argued, so § T-002 scope's "Done when" is met — but the spec's load-bearing requirement is reserved gate 2, and § T-002 scope's "Stop when" names exactly that. The task stops until the owner rules.

**Evidence refs.**

- `work/active/WI-032_cold-volume-basis/spec.md` — the native artifact. Carries the derivation, three assessed routes, five proposed-and-gated modeling requirements, scope boundaries, and three open decisions for the owner. Its banner states the item stops at spec; no design, no plan, nothing under `models/`.
- `models/library/analyses/mfe_magnet_cost.sysml@8f3b510c:44`, `models/designs/stellarator_09/stellarator_plant.sysml@ba5c9945:138-139,570`, `knowledge/KNOWLEDGE.md@ffa5c54c` DI-010 — the three quantities the derivation works from.
- `exploration/stellarator_e2e/generated/contracts/model_contract.json:1832` and `exploration/stellarator_e2e/studies/20260823-magnet-technology-ab/study.py:44-47` — read this task, and the reason the gate is real rather than formal: `vol_cold_cryo` is a package entry point *and* an arm-definition key of the committed study.
- `exploration/stellarator_e2e/studies/20260823-magnet-technology-ab/record.md@e204aee7` certification addendum — the sensitivity the tolerance has to be read against.
- `uv run agentic-mbse status` — one new warning, `spec.md Status='active' overrides BACKLOG.md status='backlog' for WI-032`, which is the tooling resolving the transition itself. The other warnings are on `work/BACKLOG.md` epic statuses and `modeling_project/VALIDATION_MATRIX.md`, neither touched by this task.

**Goal-level reading.** The question is now sharper than `goal.md` § Grounding evidence could make it, and in a way that bears on the answer.

The 27–41 % gap is explained and it decomposes. `G` is `8π²` exactly, so the magnet calc factorises into `I_link × L_proxy` where `I_link = 2πR₀B/μ₀` is the Ampère's-law current and `L_proxy = 4π r_coil = 37.699 m` is a cost-proxy length built from the coil *bore* radius, which falls out of the radial build and is not a winding length. Substituting Stellaris's actual winding geometry — 48 coils × 25 m — leaves a residual: DI-010's 112–124 A/mm² gives 115.2–127.6 m³ against the held 136.56 m³, and reproducing the anchor needs 104.6 A/mm², below the sourced band. Read the other way, the real winding packs carry 7–18 % more ampere-turn-metres than Ampère's law on the magnetic axis accounts for, which is what a modular quasi-isodynamic coil set should do: the shaping currents largely do not link the axis. **Ampère's law on axis is a lower bound on modular-coil current, not an estimate of it.**

Two consequences for the goal.

1. **The finding's identity is false as stated.** "Volume should follow from the two" needs a third input — a winding length. Neither the coil count nor the circumference is anywhere in the models; both are sourced and citable but live in a doc comment. This does not trip the strategy's abandonment condition, because the route reaches the anchor from *sourced* quantities rather than needing new evidence, but it does mean the change is a modelling addition and not a wiring-up.
2. **The case for computing is arm B, not arm A.** For arm A the held value is the better basis on its own terms — it is cross-checked twice, against turns × (20 mm)² and against the Table 8 masses. What computing buys is that arm B's 390 m³ stops being a hand ratio taken off arm A's held number (`study.py:38-42`) and becomes the same formula at Nb₃Sn's own `J_eng` and ceiling field. That is the honest reason to open the gate, and the spec says so.

The goal is not answered. `goal.md` § Answered when needs a decision with its reasoning, in either direction; the reasoning is now on the record natively and the decision is the owner's.

**Decision fields.**

1. *Finding or trigger:* the handoff stop closing T-001 put the continue-or-close choice to the operator.
   *Decision and reason:* round 1 continues under its existing strategy revision, which this session did not re-author. The operator's continuation brief names this session the round agent and directs it to take the open round as it stands — that is the first of the two options the handoff laid out.
   *Tier:* reserved gate, resolved by the operator. *Who decided:* the operator, 2026-08-26. *What changed:* `work/orchestration/goals/cryo-volume-basis/trail.md` (resumption note, T-002 scope and start).
2. *Finding or trigger:* the spec's central requirement is reserved gate 2, so the task could have stopped before writing the spec.
   *Decision and reason:* write the spec first, then surface the gate. The gate is only decidable once the derivation route and its tolerance are on the table; stopping earlier would have handed the owner a decision with no evidence under it. Writing a spec mutates neither `models/` nor `knowledge/`, and the banner blocks the stages that would.
   *Tier:* execution detail. *Who decided:* the round agent, 2026-08-26. *What changed:* `work/active/WI-032_cold-volume-basis/spec.md`.
3. *Finding or trigger:* `.claude/commands/spec-model.md:69` has the spec stage mint `SV-XXX` entries in `modeling_project/VALIDATION_MATRIX.md`.
   *Decision and reason:* not done, and scoped out. An `SV` entry is a verification contract for a change that is not authorized; minting one would put a pending obligation in a project-wide matrix for work the owner may rule against. If gate 2 opens, the entries are minted then.
   *Tier:* execution detail. *Who decided:* the round agent, 2026-08-26. *What changed:* `none`.
4. *Finding or trigger:* `work/BACKLOG.md` still reads `status: backlog` for `WI-032` while the spec reads `active`, and there is no `agentic-mbse pm` operation for that transition.
   *Decision and reason:* left alone. `CLAUDE.md` bars hand-editing `BACKLOG.md` for state transitions, and the dashboard resolves the precedence itself rather than reporting a defect. Not a goal-level problem.
   *Tier:* execution detail. *Who decided:* the round agent, 2026-08-26. *What changed:* `none`.
5. *Finding or trigger:* a form factor fitted at the design point would reproduce 136.56 m³ exactly and make the tolerance look tight.
   *Decision and reason:* rejected in the spec and recorded there as a rejected alternative. A value calibrated to the point it is validated against cannot be validated, and it would bury the modular-coil discrepancy — the one physically interesting thing the derivation found — inside a fudge factor.
   *Tier:* execution detail. *Who decided:* the round agent, 2026-08-26. *What changed:* the spec's § The three routes.

**Next task:** none. The task stops on the gate, and the gate is the operator's to take to the owner. Round 1 remains open with no round result: `GOAL_RUNBOOK.md` § Opening and closing a round closes a round on an owner gate *that is not resolved*, and whether this one resolves is not this session's to decide.

### Round 1 result — 2026-08-26

**Intent: unmet.** The strategy revision declared one model increment — `vol_cold_cryo` computed in `models/designs/stellarator_09/stellarator_plant.sysml` — and it did not land. Nothing under `models/`, `knowledge/`, or `exploration/models/` moved this round. It also declared no committed study, and none was committed, so that half of the intent is met vacuously rather than by achievement.

What the round did produce, against the goal rather than against the strategy: the discovery row is routed and stays routed, and the question the goal exists to answer is now argued on the record with its arithmetic shown. `goal.md` § Answered when is **not** met in either direction, because it requires a decision, and the decision is owner-held and was not available.

**Task sequence.** Two tasks, no retries, no checkpoints.

1. `T-001` — route discovery row `20260823-magnet-technology-ab#2` to a native home. Interrupted after the mint landed and before the row was appended; resumed under the same scope by a second session; returned `COMPLETE`.
2. `T-002` — argue the derivation in `WI-032`'s spec stage. Returned `OWNER_GATE`.

No pin was promoted and no study was committed, so the round stayed inside its bound (`GOAL_RUNBOOK.md` § Opening and closing a round) with room to spare. No pre-execution disposition checkpoint was owed: a checkpoint is triggered by a study reading, and this round produced none.

**Last semantic outcome.** `T-002` → `OWNER_GATE` on reserved gate 2, retiring `vol_cold_cryo` as a settable input.

**Stop reason, derived.** Read off the last semantic outcome plus `goal.md` § Limits, not maintained separately.

- Limits: retry cap not approached (zero retries); checkpoint revision cap not engaged (no checkpoint was owed); round limit 6 not reached (this is round 1); no time or iteration limit declared. **No declared limit fired**, so trigger 5 is not the reason.
- The last semantic outcome is an owner gate. The operator ruled on 2026-08-26 that gate 2 is **not granted in this round**: `goal.md` § Reserved gates makes any model or knowledge mutation beyond the goal directory owner sign-off, the owner was not present in this round, and the operator does not hold that authority on the owner's behalf. The gate therefore stands unresolved.
- Derived stop reason: **close trigger 4 — an owner gate that is not resolved.**

The round did not close on a strategy blocker. The strategy's own abandonment condition — no route to the anchor from carried quantities without a new sourced input — was tested and did *not* fire: a route exists and reaches the anchor from quantities that are sourced and citable (48 coils × 25 m, raw.pdf sec. 2.9, already cited in the held value's own doc), even though the model does not carry them yet. The strategy survives the round intact and is available to round 2 if the owner opens the gate.

**Evidence refs.**

- `work/active/WI-032_cold-volume-basis/spec.md` — the round's substantive product. Derivation, three assessed routes, five proposed-and-gated modeling requirements, scope boundaries, three open decisions for the owner.
- `work/BACKLOG.md:100-104,195` — `WI-032` under the MFE Cost Modeling epic, minted by the modeling PM's own operation at `a6caab37`.
- `exploration/stellarator_e2e/studies/DISCOVERY_LOG.md` — two joined rows under `20260823-magnet-technology-ab#2`, dated 2026-08-26, the later superseding the earlier. `tests/study/test_records.py` 7 passed after the second append, so the multi-row join under one id holds.
- `models/library/analyses/mfe_magnet_cost.sysml@8f3b510c:44`, `models/designs/stellarator_09/stellarator_plant.sysml@ba5c9945:138-139,570`, `knowledge/KNOWLEDGE.md@ffa5c54c` DI-010 — the three quantities the derivation works from.
- `exploration/stellarator_e2e/generated/contracts/model_contract.json:1832`, `exploration/stellarator_e2e/studies/20260823-magnet-technology-ab/study.py:38-42,44-47` — why gate 2 is a real gate: the value is a package entry point and an arm-definition key, and arm B's 390 m³ is derived from arm A's held number.
- `exploration/stellarator_e2e/studies/20260823-magnet-technology-ab/record.md@e204aee7` § 15 `#2` and the 2026-08-23 certification addendum — the finding as sighted, and the sensitivity band the tolerance is read against.
- Cited-ref walk at round close: every ref above still stands at the digest it is cited at. The paths that moved this round — `work/BACKLOG.md`, `DISCOVERY_LOG.md`, and the new `work/active/WI-032_cold-volume-basis/` — moved by this round's own tasks. No external mutation; no task is voided.

**Proposed learning delta.** Three claims, for the fresh review to accept, correct, or reject. Not appended to `learnings.md` by this session — that write belongs to the review (`GOAL_RUNBOOK.md` § The five surfaces).

- **Proposed L-001 — `total_kAm` is a cost proxy, not a count of winding ampere-turn-metres.** `G = 78.95683520871486` is `8π²` exactly, so `mfe_magnet_cost.sysml@8f3b510c:44` factorises into `I_link × L_proxy` with `I_link = 2πR₀B/μ₀` and `L_proxy = 4π r_coil = 37.699 m`, and `r_coil` is the coil *bore* radius falling out of the radial build (`stellarator_plant.sysml@ba5c9945:138-139`), not a winding length. *Scope:* the MFE magnet cost calc as built, at any design point; the factorisation is algebraic, not a fit. *Implication:* any strategy wanting a conductor volume or conductor length out of this package must supply a winding length; the package carries none, and neither coil count nor circumference appears anywhere under `models/`.
- **Proposed L-002 — Ampère's law on the magnetic axis is a lower bound on modular-stellarator coil current, not an estimate of it.** At Stellaris's own geometry (48 × 25 m) the sourced `J_eng` band 112–124 A/mm² gives 115.2–127.6 m³ against the 136.56 m³ geometric anchor; reproducing the anchor needs 104.6 A/mm², below the band. Read the other way, the winding packs carry 7–18 % more ampere-turn-metres than the axis-linking law accounts for — the shaping currents of a modular quasi-isodynamic coil set largely do not link the axis. *Scope:* modular stellarator coil topology; not established for tokamak TF coils, where the axis-linking law is closer to the whole story. *Implication:* a computed cold volume from carried quantities lands *below* a geometric anchor by roughly the size of the effect being modelled, so the tolerance must be wide. A tight tolerance is obtainable only by calibrating a form factor at the design point, and a value calibrated to the point it is validated against cannot be validated.
- **Proposed L-003 — the case for computing this volume is arm B, not arm A.** Arm A's held 136.56 m³ has an independent double cross-check (each side² equals turns × (20 mm)² against the Table 8 turns row; the no-casing masses imply ~7540 kg/m³, consistent with the Table 7 mix), where the ampere-turn route is a provable lower bound. Arm B's 390 m³ is a hand ratio taken off arm A's held number (`study.py:38-42`). *Scope:* this comparison and this package. *Implication:* the goal's answer should be argued on what computing does for the comparison, not on arm A's accuracy — and a round that argues it on arm A's accuracy is arguing the weaker case.

**Finding dispositions.** One discovery row was touched.

- `20260823-magnet-technology-ab#2` — dispositioned `model fix`, routed to `WI-032`, status "spec landed; blocked on an unresolved owner gate". Two joined rows under the id, the 2026-08-26 T-002-close row superseding the 2026-08-26 T-001 row whose "routed, not yet answered" and `status: backlog` reference went stale when the spec landed. **Not left `unrouted`** (ADR-004).

Two rows were read but not touched, and the reasoning is recorded so the review can disagree:

- `20260823-magnet-technology-ab#3` (no coil-thickness / radial-build / stress coupling) is still `unrouted`. This round produced no evidence bearing on it. L-001 states that `r_coil` is the bore radius from the radial build, which is adjacent, but it neither confirms nor changes `#3`'s claim about the missing coupling. `goal.md` § Reserved gates item 5 bars this goal from widening to `#3`, so routing it here would be acting through a gate, not discharging an obligation.
- `20260823-magnet-technology-ab#11` (headline sensitivity to held cryo assumptions) was cited for its certification-addendum numbers, which are the quantification its own disposition already points to. The row is dispositioned, its home is executor practice at runbook step 11, and it is not this goal's to move.

**Round 1 is closed.** It is unreviewed. The round agent's last act is the round result, and this session wrote both task returns, so it cannot review the round (`GOAL_RUNBOOK.md` § What "fresh" means).

### Stop — 2026-08-26

Kind: handoff

**What is true on disk.** Round 1 is closed: strategy revision, T-001 (scope, start, interruption stop, `COMPLETE` return), a resumption note, T-002 (scope, start, `OWNER_GATE` return), and the round result above. `WI-032` exists under the MFE Cost Modeling epic with a spec and nothing further — no design, no plan, no edit under `models/`, `knowledge/`, or `exploration/`. Discovery row `20260823-magnet-technology-ab#2` carries two joined disposition rows and is not `unrouted`. `learnings.md` is still the unfilled template; the round result proposes three claims and does not append them. Nothing is committed — the operator owns commits.

**What the owner must see:** a fresh session is needed to review round 1, and separately, reserved gate 2 is unresolved and is what closed the round. The gate is the owner's, not the operator's, and round 2 has nothing to pursue until it is ruled on — the strategy survived intact but its next move is the gated one.

**The material to review:** this goal directory; `work/active/WI-032_cold-volume-basis/spec.md`; `work/BACKLOG.md:100-104,195`; `exploration/stellarator_e2e/studies/DISCOVERY_LOG.md` (the two newest rows under `20260823-magnet-technology-ab#2`). Resume at `GOAL_RUNBOOK.md` § The fresh review.

### Round 1 review — 2026-08-26

**Reviewer.** A fresh session. It did none of round 1's work: it did not author the strategy revision, either task scope, either return, or the round result, and it read the round for the first time in this session (`GOAL_RUNBOOK.md` § What "fresh" means).

**Verdict: `FINDINGS`.** The round's evidence is sound — every cited ref resolves and says what the trail claims, and the arithmetic reproduces to the digit. Two things the round did not record are carried to round 2 as constraints. Neither invalidates the round, and the round stays closed.

**Checks.**

- **Native evidence, by citation.** Every ref was opened and read. `total_kAm = G * B * R0 * r_coil / (mu0 * 1000.0)` is at `mfe_magnet_cost.sysml:44` as cited; `vol_cold_cryo = 136.56` with its geometric doc is at `stellarator_plant.sysml:570`; the bore-radius statement is at `:138-139` and the binding it describes is real (`mfe_plant.sysml:51`, `:320` — `r_coil = rb.r_coil`); the cryo chain is at `mfe_plant.sysml:265-282`; DI-010's REBCO band is 112–124 A/mm² and its Nb₃Sn band 14.6–28 (`KNOWLEDGE.md:76-81`); `vol_cold_cryo` is a package entry point (`model_contract.json:1832`, `stellarator_09__stellaris__vol_cold_cryo`, default 136.56) and an arm key with arm B's 390 m³ derived by hand from arm A's held value (`study.py:38-42,44-47`); the finding's wording at `record.md:259` is what `goal.md` quotes; the certification addendum's sensitivity is what the spec reads it as — holding `f_carnot_cryo` at 0.20 and swinging the volume 390 → 285 m³ moves `rec_frac` 0.516 → 0.511, and the arm stays empty in all six sourced combinations. `WI-032` is at `work/BACKLOG.md:100-104` and `:195` under the MFE Cost Modeling epic.
- **The arithmetic, recomputed independently.** `G` is `8π²` to all printed digits. The factorisation is exact: `I_link = 2πR₀B/μ₀ = 5.71500e8 A` and `L_proxy = 4π r_coil = 37.6991 m` multiply back to `2.15450e7 kA·m`. The proxy route gives 192.4 / 182.6 / 173.8 m³ at 112 / 118 / 124 A/mm² and needs 157.77 A/mm² for the anchor — `goal.md` § Grounding evidence reproduces. The winding route (`I_link × 25 m`, the 48 coils cancelling against the per-coil current) gives **127.57 / 121.08 / 115.22 m³**, needs **104.62 A/mm²** for the anchor, and the residual is **7.0 % to 18.5 %**. The spec's table and the disposition row's "6.6–15.6 % short" are exact. `128.7 t × 8 / 136.56 m³ = 7539 kg/m³`, so L-003's density cross-check holds.
- **Goal and strategy fidelity.** The round pursued the strategy it declared: route the row natively first (T-001), then argue the derivation inside the item's own spec stage rather than as trail prose (T-002). It did not pursue anything else. The strategy's abandonment condition was tested honestly and did not fire — a route to the anchor exists from sourced quantities, and the round said so rather than reaching for the easier "blocked" reading.
- **Task scopes.** Both held. T-001's exclusions (no spec, no `models/` edit, no DI, no `f_carnot_cryo`, no row `#3`, no close, no commit) were all observed; the only writes were the PM mint and one appended row. T-002 excluded `models/`, `knowledge/`, and `exploration/` edits, design and plan stages, an `SV-XXX` mint, and hand-editing `BACKLOG.md` — and `git log` confirms T-002's commit (`2e257062`) touched only `spec.md` and `trail.md`. The second disposition row landed at round close (`57129cb9`), not inside T-002, so it is not a T-002 scope breach. No task exceeded its scope.
- **Retry classification.** No retries were taken, so nothing to classify. The interruption was resumed under the recorded scope without re-running the mint, which is what `GOAL_RUNBOOK.md` § Resuming an interruption requires, and the native state confirms one mint and no duplicate.
- **Discovery rows the round's evidence touched.** `20260823-magnet-technology-ab#2` carries two appended rows under its own id, the 2026-08-23 sighting at `:20` byte-untouched (`git diff 31f9eb0b..HEAD` shows two pure additions), the newest row reading `model fix` — routed, spec landed, blocked on an unresolved owner gate, with `WI-032` and the spec path as its next reference. Not `unrouted` (ADR-004). `tests/study/test_records.py` — 7 passed, so the multi-row join holds. Row `#11` was cited for numbers its own disposition already points to and needed no new row; **that is right.** Row `#3` was read and left `unrouted`, and the round's reasoning for that is accepted: L-001 touches `r_coil`'s provenance but establishes nothing about the coil-thickness ⇄ field coupling `#3` names, and `goal.md` § Reserved gates item 5 bars this goal from widening to it. Routing `#3` here would have been acting through a gate.
- **Cited artifacts moving outside their task.** Walked. `record.md@e204aee7`, `epic-mfe-cost-modeling.md@f22bd288`, `stellarator_plant.sysml@ba5c9945`, `mfe_plant.sysml@ba5c9945`, `mfe_magnet_cost.sysml@8f3b510c`, `mfe_cryo_plant.sysml@8f3b510c`, `KNOWLEDGE.md@ffa5c54c`, `STUDY_POLICY.md@ad2fb4ea` — each is still at the commit that last touched it. `snapshot.json`, cited `@e204aee7` in `goal.md` § Invariants, was last *written* at `829dda6d`; the content at the two commits is identical (`git diff` empty for that path), so the citation names the right bytes and nothing moved. The paths that changed — `work/BACKLOG.md`, `DISCOVERY_LOG.md`, and the new `work/active/WI-032_cold-volume-basis/` — changed by this round's own tasks. **No external mutation; no task is voided.**
- **The round's claim that nothing else moved.** Verified. The four round commits touch only `goal.md`, `trail.md`, `work/BACKLOG.md`, `DISCOVERY_LOG.md`, and `spec.md`. Nothing under `models/`, `knowledge/`, `modeling_project/`, or the `exploration/stellarator_e2e/models/` twin moved, so the twin invariant was never at risk.
- **The derived stop reason.** Correct. No declared limit fired (zero retries against a cap of 2; no checkpoint owed, so its cap never engaged; round 1 of 6; no time limit declared), the last semantic outcome is `T-002` → `OWNER_GATE`, and the operator recorded that gate 2 is *not granted in this round* because the owner was absent and the operator does not hold that authority. Not granted is not denied — the gate stands **unresolved**, which is trigger 4 and not trigger 6. The round result did not reach for a strategy blocker it had not earned, and that restraint is the right call.

**Findings.**

1. **The intended model increment changed shape, and the round result does not say so.** The strategy revision declared the increment as `vol_cold_cryo` computed in `stellarator_plant.sysml` with the concept value in `designs/`, and stated plainly: "Nothing in `models/library/` is intended to move." The spec's MR-WI032-3 now requires a **new `calc def` in `models/library/analyses/`**, with `mfe_plant.sysml` wiring it — which MR-3 makes the correct shape, since the physics must live concept-agnostically and only the values in `designs/`. So the spec is right and the strategy's stated increment is now stale. The round result says "the strategy survives the round intact" without recording this. It survives, but its increment is wider than declared, and round 2 must not inherit the narrower sentence.
2. **Round 1 was carried by four sessions, and the result does not carry that forward as a constraint.** ADR-002 is "a round is one agent's bounded pursuit of one strategy." Round 1 had a strategy author, a resumer, a continuation agent, and a closing agent. This was **not** a silent drift — the T-001 handoff stop surfaced the two readings, parked the choice, and the operator ruled continuation, which is exactly what `GOAL_RUNBOOK.md` asks of an agent facing a premise conflict. The gap is only in the record: the round result reports "two tasks, no retries" without noting that the round crossed three session boundaries under an operator ruling, so a later reader would not know ADR-002's one-agent property was waived here and why.

Neither finding is an evidence error and neither reopens the round.

**Learning delta — settled here, appended to `learnings.md` at the same time and nowhere else.**

- **L-001 — accepted as proposed.** The factorisation is algebra, not a fit, and it reproduces exactly. The "no coil count or circumference anywhere under `models/`" claim was re-checked by grep and holds; `J_eng` is absent too.
- **L-002 — accepted with a correction.** The claim is right and load-bearing. Two things are sharpened. The residual band is **7.0–18.5 %**, not "7–18 %" — the proposal rounds its own upper bound down, and the upper bound is the one that sets how wide the tolerance has to be. And the physical reading — that a modular quasi-isodynamic coil set's shaping currents largely do not link the axis — is **this round's inference from the residual's sign and size**, not a sourced result; it is the most plausible reading and no source in the repository states it. Recorded as an inference so a later round challenges it by re-deriving rather than by asking the owner.
- **L-003 — accepted as proposed.** Arm B's 390 m³ is a hand ratio off arm A's held number at `study.py:38-42`, arm A's double cross-check is in the held value's own doc, and the density figure recomputes to 7539 kg/m³.

**Constraints carried into the next strategy.**

1. **Round 2 has nothing to pursue until the owner rules on gate 2.** The strategy's surviving next move is the gated one, and `goal.md` § Reserved gates puts any model or knowledge mutation beyond the goal directory behind owner sign-off. A round 2 that opened now would either idle or act through the gate.
2. **The increment includes a new library calc def** (finding 1). Round 2's strategy revision states the increment in the spec's shape, not the round 1 sentence's.
3. **Round 2 is one session** (finding 2), or it surfaces and gets a ruling as round 1 did.
4. **The `integrate` seam still has no hand pattern.** Any round that lands the model change stops at `PREREQUISITE` before a study, per `goal.md` § Grounding evidence and `GOAL_RUNBOOK.md` § The native seams.
5. **A pre-existing registry disagreement, noted and not this goal's to fix.** `work/BACKLOG.md` declares the MFE Cost Modeling epic `status: draft` while `work/backlog/epic-mfe-cost-modeling.md@f22bd288` reads `Status: active`; `uv run agentic-mbse status` warns on it. The round's citations are to the epic file and are accurate as written. The warning predates this round and belongs to the modeling PM.

**Recommendation.** Do not open round 2 yet, and do not recommend close — `goal.md` § Answered when is unmet in both directions, because it requires a decision and none is available. **The owner's ask is one decision, and the spec has already laid it out:** § Open decisions for the owner, R1 (compute at a −16 % / +0 % tolerance) against R3 (keep it held, with the round's reasoning as the answer), and gate 2 following automatically from R1. Either ruling ends the goal on `goal.md`'s own terms — R3 answers it immediately as a `BOUNDED_NEGATIVE`, and R1 opens round 2 with the increment in the spec's shape. The round's own recommendation is R1, argued on arm B rather than arm A, and this review finds that argument sound and its arithmetic exact.
