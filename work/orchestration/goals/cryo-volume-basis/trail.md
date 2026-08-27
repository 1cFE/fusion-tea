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
