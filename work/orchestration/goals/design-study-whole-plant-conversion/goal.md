# Goal: Whole-plant steam versus helium Brayton conversion

## Status

grounded — 2026-09-27. [OWNER] Invoked run-goal with the retained owner brief, authorizing grounding and execution with this slug without reconfirmation.

## Question

[OWNER] For one consistently specified reactor concept, how does choosing the modeled steam or helium Brayton conversion system change net exported electricity, whole-plant LCOE, and the conditions under which each is preferable?

## Consumer

[OWNER] The project owner needs an understandable engineering study for the one-year project write-up. See evidence/owner-brief.md for verbatim emphasis, detailed endpoint, and execution authorization.

## Answered when

[OWNER] A verified, reproducible whole-plant comparison includes at least one common supported condition, an explicit complete reactor/conversion power and lifecycle account inventory, reranked compatible equipment, and sensitivities establishing a quantified conditional preference or no material difference. Seek the predecessor's 2500/2800/3000 MW source loads without claiming unsupported points. Deliver assembly diagrams, currency-consistent baseline table, power/cost and preference figures, proposed article passage, full attempted-case ledger and check status, SVG/PNG files, renderer, replay commands, sealed verification, and independent final assurance of the plant boundary and conclusion. A missing material prerequisite means partial completion.

## Invariants

- [OWNER] One common reactor inventory and upstream operating assumptions within each pair, with any conversion-dependent upstream consequences modeled or bounded. Source heat must be distinguished from fusion heat, deposited heating and recovered primary work. Across loads, distinguish operation from hardware selection.
- [OWNER] Whole-plant net export subtracts every applicable upstream and conversion electrical load exactly once; lifecycle cost includes explicit major capital accounts, annual expenses, replacements and terminal items. Remove replaced conversion allowances. Common unknown costs remain labeled and bounded. Model-owned calculations produce power and LCOE.
- [OWNER] Preserve existing baselines, source evidence, historical studies and failures. Use an additive isolated package. Preserve other agents' files and owner write-ups; explicit-path local commits only, no push or merge.
- [INHERITED: modeling_project/REQUIREMENTS.md] MR-1–7 and applicable process requirements. MR-7: source condition, reactor inventory, equipment offers, operating choices, prices and service assumptions remain supplied choices. Balance/controller states may be solved under explicit reviewed relationships. Insufficient supplied hardware fails rather than being automatically purchased. Record actual bindings and affected consumers, and test sufficient/insufficient and unsupported cases.
- [OWNER] Apply return conditions, temperature approaches, finite cooling and property/capacity limits. Rank supported passing cases only. Retain all attempted cases. Reuse valid predecessor numerical evidence; unchanged oracle and tolerances for implementation repairs.
- [OWNER] Independent complete power/cost boundary and variable-role review precedes dependent main study; independent final review checks actual whole-plant reranking and remaining assumptions.

## Grounding evidence

- evidence/owner-brief.md — unpinned; no native digest at grounding; retained owner instruction with agent-proposed strategy distinguished.
- work/orchestration/goals/design-study-component-alternatives/answer.md@4f724f3378e97d80e34da5af883f83b8c9b2ec7f and learnings.md at the same commit: verified 498-case subsystem comparison, explicitly excludes reactor/fuel/primary circulation costs and electricity.
- work/active/WI-096_matched-conversion-subsystems/spec.md@4f724f3378e97d80e34da5af883f83b8c9b2ec7f: existing matched conversion work item; design/report and sealed repaired record are entry evidence for boundary reuse.
- exploration/component_alternatives/studies/20260926-design-study-component-alternatives-b/record.md@4f724f3378e97d80e34da5af883f83b8c9b2ec7f: native predecessor study identity and numerical evidence.
- models/designs/stellarator_09/stellarator_plant.sysml@4f724f3378e97d80e34da5af883f83b8c9b2ec7f and models/designs/component_alternatives/plant.sysml at the same commit: candidate upstream inventory and verified conversion interfaces to investigate, not yet approved as a combined boundary.

## Limits

[AGENT] Runbook defaults applied explicitly; reaching a cap requires owner ruling rather than task renaming.

| Limit | This goal |
|---|---|
| Mechanical retry cap | 2 retries (3 attempts), same scope/meaning/inputs |
| Checkpoint/design-review revision cap | 2 revisions (3 submissions) per submitted decision |
| Round limit | 6 rounds |
| Promoted pins and committed studies | At most one of each per round |
| Time or iteration limit | No additional time cap; finite study catalog declared before execution |

## Reserved gates

[OWNER] Formal goal/item closure, changes to requested endpoint, declared cap exceptions, purchases and external messages. [AGENT] Unresolved scientific interpretation changing the comparison meaning or a material premise conflict is surfaced to the owner; dependent work parks. Explicit conditional modeling assumptions and bounded justified repairs are already authorized by the brief.

## Close rule

[OWNER] Only the owner formally closes the goal or item. Recommend closure only on the complete declared endpoint and independent assurance. Partial completion remains partial.

## Amendments

### Engineering endpoint — 2026-09-27

[AGENT] The verified conditional engineering endpoint is met; [answer.md](answer.md) and the sealed study at a7bd94ed record the result. Independent final review passes. Round 2 is closed by the answered-goal trigger. Formal goal and WI-098 closure remain reserved to the owner; closure is recommended.
