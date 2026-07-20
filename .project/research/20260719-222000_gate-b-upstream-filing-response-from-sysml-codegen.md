---
date: 2026-07-19 22:20 PDT
author: Claude
topic: "Upstream filing of fusion-tea finding #8 / Gate B — resolution notice"
tags: [filing, gate-b, fusion-tea, wi-027, cross-repo]
status: filed
sysml_codegen_branch: constraint-exec-epic
last_updated: 2026-07-19
---

# Filing: fusion-tea finding #8 / Gate B — received, root-caused, fixed upstream

This is the filing the fusion root-cause report asked for (its recommendation 1: *"File finding
#8/Gate B upstream now"*). Finding #8 was written downstream, marked "file upstream," and never
filed — the report named that non-filing as the real process gap. This closes it, and reports the
resolution in the same document.

**Filed into:** `../fusion-tea-stellarator-mbse-demo` (WI-027). Filing text below is the version
delivered there.

---

## What was reported

Adding any concrete constraint to a model made snapshot capture run a whole-graph V11 coverage
check inside `extend_graph_with_constraints`. That check rejected pre-existing, unrelated coverage
gaps — specifically the three cross-part capital-rollup keys (`contingency__direct_subtotal`,
`indirect__direct_cost`, `lcoe_calc__total_capital`) that the demo's bridge legitimately fills later,
at generation. Turning the five viability asserts on was what switched the check on, so capture
aborted before it could write a snapshot carrying the constraints.

**The report was right, and its root cause was correct.** The check's scope exceeded its own stated
intent (old lowering INV-6 was about the constraint-*minted* entry points), it duplicated a gate
that already runs at the correct moment, and no fixture in the codegen corpus paired a pre-existing
deferred input with constraints, so nothing could have caught it.

## What we did with it

We did not implement the report's recommended repair. We tested its premise first, because the
whole repair — a differential that rejects only *introduced* violations — only makes sense if
extension can introduce one.

It cannot. Constructed, runnable evidence at candidate `3700fee`
(`.project/active/constraint-lifecycle-gate-b/findings.md`):

- Extension copies `fallback_entry_points` verbatim and deep-copies base modules, so only an
  appended module input could be a new offender.
- Appended inputs reach an entry point two ways. The MODELED_DEFAULT mint produces
  `{constraint_id}__{formal}`, where `constraint_id` ends in a 16-hex SHA-256 segment, while every
  fallback key is `{calc_eqn}__{formal}` from a single writer — colliding needs a preimage. The
  DESIGN_ATTRIBUTE mint produces a design-attribute QN, and across 35 live fixture models (60
  fallback QNs, 846 design-attribute QNs) those namespaces never intersect. Both constructible
  collision vectors are blocked at extraction.

So the extension-time check had no reachable job. **We deleted it** rather than replacing it with a
differential that would have been dead code carrying a misleading invariant.

Directly relevant to the report's Section 4.5: the "required negative regression" it specifies — a
pre-existing unwired fallback key newly consumed by a constraint, extension must fail — has no
model that produces it. That regression was not written. Its two constructible siblings were.

## What this means for the demo

- **The Gate B blocker is gone at the source.** Constraint extension no longer rejects pre-existing
  coverage gaps. A lowering-ON capture with the five asserts live no longer aborts on the three
  rollup keys, so it can write a snapshot carrying both the constraint facts and the occurrence
  table. That also removes the `FrozenOccurrenceIndexCorruptionError` dead-end the report
  documented, because deferring lowering is no longer necessary.
- **The generation gate is unchanged and still strict.** `_reconcile_params_coverage` still requires
  zero whole-graph V11 offenders. The bridge's fill still has to happen, and still has to work.
  Regressions pinning this: `tests/conformance/test_gate_b_generation_gate.py`.
- **Option 2 (placeholder defaults in the staged twin) is not needed.** If it was applied as an
  interim measure, the report's own revert path applies: delete the two `= 1.0` defaults and restore
  the bridge's 3-offender expectation.

## Two corrections to the report, for the record

1. **INV-6 was not already narrow.** The report says scoping the check matches INV-6's existing
   intent. INV-6's first sentence literally required the *extended graph* to have zero V11 uncovered
   params. This change therefore supersedes INV-6 as an intentional contract correction, not a
   restoration of prior wording. It is recorded as contract row LC-E02.
2. **The bridge is not a sanctioned upstream seam.** The generation gate tolerating a filled
   placeholder is not the same as codegen offering a late-fill callback. The owner's position is
   explicit: no public late-fill or post-build graph/default mutation seam (contract row LC-E04A).
   The bridge remains a private consumer workaround.

## What the demo still owns

These are unchanged by this fix and are not upstream bugs:

- **The bridge is stale against the current API.** `_generate_modules` now requires a prebuilt
  `ConstraintGenerationPlan`, and the bridge still passes three arguments. It also bypasses current
  preflight, prewrite planning, and sealing. This fix restores context construction; it does not
  make the script compatible.
- **The cross-part capital rollup still cannot be wired** (WI-015 finding #4). That is a separate,
  still-open codegen limitation, tracked as its own epic item. The rollup keys still need a producer
  or a fill; Gate B only stopped them from failing at the wrong moment.

## Process note

The report's recommendation 1 was to file regardless of which demo path was chosen, because the
non-filing is what made finding #8 invisible the first time. Agreed, and worth stating plainly: the
finding was correct, the fix was small, and the only reason it sat unfixed was that it never crossed
the repo boundary.

## References

- Decision record: `.project/active/constraint-lifecycle-gate-b/decision.md`
- Vacuity proof and reproduction: `.project/active/constraint-lifecycle-gate-b/findings.md`
- Independent assessment: `.project/research/20260719-103419_gate-b-independent-assessment.md`
- Fusion root cause: `../fusion-tea-stellarator-mbse-demo/.project/research/20260719-082509_gate-b-root-cause-constraint-lowering-vs-v11-bridge.md`
