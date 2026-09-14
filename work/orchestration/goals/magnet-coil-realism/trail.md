# Trail: magnet-coil-realism

What happened, and what was decided. Append-only, newest entry last, ISO dates. **No entry is ever edited in place.** A correction is `### Amendment YYYY-MM-DD — amends <entry heading>`, stating what changed and why.

This file logs judgment, not routine stage motion. Native workflows keep their own stage records; entries here cite them by path or native id and never restate their content. Procedure is in `work/orchestration/GOAL_RUNBOOK.md`.

## Grounding — 2026-09-14

Grounded on the owner's ruling `[OWNER-VERBATIM 2026-09-14]` "ok agreed, draft the goal file and /run-goal" (`goal.md` § Reserved gates; `evidence/grounding_proposal.md`). Evidence deposited: `evidence/grounding_probe/` (the oracle transects at the entering pin), `evidence/grounding_proposal.md`. Entering pin `c95eefd7…` / semantic `2c278866…` / executable `8ff5bb7c…` (`goal.md` § Invariants). Grounding is not a round and writes no discovery row.

## Round 1 — winding-length-from-bore

### Strategy revision — 2026-09-14

- **Approach:** land one model increment — the coil winding length computed from the coil bore instead of the major radius (`goal.md` § Answered when (a)1) — through the modelling PM as a standard-scale item, mirror it in the oracle, prove one candidate pin through the integration seam, and run one study at that pin that reads the `a` and `R` transects and the matched committed points so the reading says what a fatter plasma now costs at the magnet and whether the cheapest feasible machine moved.
- **Assumptions:** (1) the corpus facts on coil size — "7 × 5 × 10 m, with a typical circumference of 25 m" — sit on the bore, so a bore-proportional form anchored at 25 m at the design coil-centre radius 3.15 m is the sourced shape and the `R`-form is the uniform-scaling special case of it (`evidence/grounding_probe/summary.md` § What the corpus says); (2) the winding length is consumed by the cold volume, the ampere-metres and the winding procurement, so one calc change propagates through the existing chains (`verify_stellaris.py@0e3bf944` L703–711; the probe's bit-constant channels); (3) the design point reproduces every printed anchor to the double after the change, because the anchor is taken at the design bore; (4) the oracle and the package can carry the new form without a seam repair (WI-044 changed the same chain's neighbours the same way).
- **Abandonment conditions:** an admissible source establishes that a modular coil's circumference scales with the major radius independently of the bore (then the standing form is right for the wrong reason, and this round closes as a bounded negative on the length question, the doc comment corrected); the item cannot land without repairing a seam (`PREREQUISITE`, naming the seam); the design point cannot be reproduced to the double under any bore-anchored form (a strategy blocker: the anchor is not where the grounding read it).
- **Intended model increment:** a new MFE modelling work item, "Coil winding length from the coil bore", replacing `c_coil = k_coil × R0` with a sourced bore form anchored at the design point, its shape factor named as the one held constant, the `R`-dependence stated (none, or the sourced toroidal excursion), the doc comments carrying the page cites; `verify_stellaris.py` mirrored in step; the consumer handoff to the study layer's oracle map.
- **Intended study question:** at the new pin, how does the magnet capital and each of its three parts respond to `a` on the design column and through the cheapest committed 18-verdict-feasible machine, how does it respond to `R` at fixed bore, which committed cases flip and why, and did the cheapest feasible machine or the `a`-optimum move against the committed `20260912-plant-closure` and `20260913-magnet-design-transfer` records.

**No future task list.** The next task is chosen from evidence after the previous one returns.

### T-001 scope

- **Objective:** land the winding-length-from-bore increment as an audited modelling work item at unchanged design-point numbers, with the oracle mirrored.
- **Why now:** it is the chain that moves the most cost (97 % of the magnet account is proportional to the winding length) and needs no new source — the corpus fact and the anchor are in hand (`evidence/grounding_probe/summary.md`); the round's study cannot ask its question until this lands.
- **Scope:** authorized — the 'Coil Winding Length' calc (or its replacement) and its instance binding in `stellarator_plant.sysml`; the doc comments and page cites; the `k_coil` retirement or re-meaning; the oracle mirror in `verify_stellaris.py`; the item's spec, design, plan, implementation, audit and consumer handoff; the validation-matrix rows the item registers. Excluded — the cryo inventory, the structure mass and rate, the tape price and reference density, the selected envelope, the coil count, the cold-volume distribution factor `f_wp_vol`, any fence, any other account.
- **Inputs:** `goal.md` (§ Answered when (a)1, § Invariants); narrower constraint: none beyond the goal's — the item may choose `r_coil_centre` or `r_coil` as the bore and must say why once.
- **Done when:** the item is audited PASS through the modelling PM; the design point reproduces `c_coil = 25.0 m`, the winding procurement $1,570,369,801.03, the cold volume 136.56 m³ and LCOE 142.50725862880648 to the double; the oracle mirrors the form; the `a` transect shows the winding length, the cold volume and the procurement responding to `a` at fixed `R`, and the `R` transect at fixed bore responding only as the model text says. A bounded negative: a sourced reading that the bore form is not supported (abandonment condition 1), recorded with the source.
- **Stop when:** a seam repair is needed (`PREREQUISITE`, naming it); the design point cannot be reproduced under a bore-anchored form (`STRATEGY_BLOCKER`); a reserved gate is reached (`OWNER_GATE`); the retry cap.

### T-001 start — 2026-09-14

Model item · `uv run agentic-mbse pm add-item` then the native spec → design → plan → implement → audit stages under `work/active/WI-0NN_coil-winding-length-from-bore/` · an audited item whose design point reproduces the entering pin's numbers and whose winding length follows the bore.
