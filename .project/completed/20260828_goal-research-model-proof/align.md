# Align — GSTH Item 5: Research-to-Model Round Proof

**Held**: 2026-08-27, at `/_my_orchestrate` launch. Owner present and ruling.

## Rulings

- **Live need**: `[OWNER 2026-08-27]` Option 1 — the `p_pump` re-source, discovery row
  `20260821-power-cycle-ab#3` (`p_pump` = 1.0 MW is ~100× below helium-primary circulator
  figures, DI-008; "re-sourcing is a separate modeling item; item not yet minted").
  The Item 5 goal grounds a new goal on this need. Ruled with the conflict surfaced:
  `CURRENT_WORK.md` lists the `p_pump` re-source under Run-Study Item 6 Phase 4's
  owner-sequenced close list; taking it here removes it from that list. Owner accepted.
- **Reserved gates**: `[OWNER 2026-08-27]` confirmed as proposed:
  - (a) the goal question and its "answered when" terms at grounding;
  - (b) any model or knowledge mutation beyond the goal directory — the WI lands through
    the modeling PM as usual, but the go/no-go is the owner's;
  - (c) the close ruling if the round ends on a judgment call.
  Everything else (spec/design/plan content, critic selection, proposed discovery-row
  dispositions) is orchestrator execution detail, recorded loudly.
- **Runbook seam row**: `[OWNER 2026-08-27]` flipping `GOAL_RUNBOOK.md` § The native seams
  `research` row from "pending native repair" to repaired is in Item 5 scope (Item 6 owns
  the `integrate` flip).
- **Branch and pipeline**: `[OWNER 2026-08-27]` `feat/goal-research-model-proof` off
  `main`; `spec → spec_review → design → design_review → plan → implement → audit`;
  `close` and `pre_pr` stay with the owner.

## Reading of the work (agent, ratified by launch)

`[AGENT]` A proof item: one real goal round, `model → PREREQUISITE → fresh critic →
research (Item 2 native seam) → model`, one unchanged strategy, every touched discovery
row dispositioned, fresh `RoundReview` at close. Honest outcomes are first-class: a
`STRATEGY_BLOCKER` close is a valid result.
