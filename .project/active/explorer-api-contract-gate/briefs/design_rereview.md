Focused re-review of the revised design for work item `explorer-api-contract-gate`. This is round 2 of 2. Append a "## Round 2" section to `.project/active/explorer-api-contract-gate/design-review.md`; don't rewrite round 1. Do not edit `design.md` or `spec.md`. Do not commit.

## Where you are

- Git worktree `/home/reid/1cfe/fusion-tea-explorer-api-gate`, branch `feat/explorer-api-contract-gate`. Never touch the main checkout `/home/reid/1cfe/fusion-tea`.
- The pinned frontend is in this repo's history: `git show 10f7b9b:exploration/concept_explorer/static/js/<file>`.
- Skip the product-lens pass. It ran in round 1, and its findings are dispositioned in the round-1 Resolutions.

## Scope

Round 1's Resolutions section (in `design-review.md`) is the checklist. The revised `design.md` claims to apply all of it. Check three things, in this order:

1. **Did each resolution land correctly?** One line per finding ID: landed, landed with a problem (say what), or missing. Don't re-argue a resolution itself unless applying it created a contradiction.
2. **Did the revision introduce a new defect?** Contradictions between rules, a rule that can't be implemented as written, invariants the new rules break, or self-tests that can't fail.
3. **Is it now over-built for the risk?** The code estimate doubled to about 700–800 lines across three modules, with about ten comparison rules. For each rule, name the concrete website break it prevents. Flag any rule whose expected false-block cost outweighs the break it catches, and any piece the plan could defer to a follow-up without weakening criterion 1.

## One question from the orchestrator

The `LITERAL_READS` table (m1) records the value set observed at the pin for `fit_grade` and `overrides[].account`. The design itself notes that this blocks whenever an analyst overrides an account no concept used at the pin. The orchestrator's view: the allowed set should come from the literal values the pinned JS compares against (cited), not from the observed set. Where the JS compares against data-driven values rather than literals, the path doesn't belong in `LITERAL_READS` at all. Check `caveat_marker.js:53` and `override_panel.js:153-155` at the pin, and say whether that view holds and what the table should contain.

Keep it short. End with a verdict: Ready for plan, or Revise with the must-fix list.
