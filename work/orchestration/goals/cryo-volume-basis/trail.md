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
