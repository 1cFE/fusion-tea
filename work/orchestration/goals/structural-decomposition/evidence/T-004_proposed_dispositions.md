# T-004 proposed dispositions — r1, 2026-09-13

The round agent's reading of the study `20260913-structural-decomposition` (committed at `ff6fdd76`) and the dispositions it proposes, for the pre-execution disposition checkpoint (`GOAL_RUNBOOK.md` § The pre-execution disposition checkpoint). No semantic follow-up task is proposed in this round; the checkpoint gates the round result's finding dispositions and the reading the round result will carry.

## 1. The reading

The restructured lineage (WI-057, pin `7f6882b7…`, executable `e800de67…`) reproduces the entering lineage (plant-closure T-007, executable `234d0b27…`) at every one of the 3,751 points of the inherited `20260907-minor-radius` `arm-fence-p100` window. 3,648 points completed on both arms with all 155 store channels equal through the contract-derived ledger — equal, not within a tolerance; `channel_difference_magnitudes` is empty — and all fourteen verdicts equal by local identity. 103 points failed to evaluate on both arms with the same phase (`module_execution`), the same cause string, and the same module read through the ledger's host paths (56 in fuel handling where net electric power goes complex, 47 in sustainment on non-positive fuel density). The baseline point reads `224.60952472804465` on both. The two contracts' constraint catalogs are byte-identical, including the catalog fingerprint and all fourteen predicate IRs. Verification passes on both arms: 54 sampled rows each, one per verdict combination, 22 channels at relative deviation below 1e-9 (worst 6.50e-16), fourteen verdicts re-derived, no mismatch. (record §§ 3, 4, 12, 13; `results/comparison_summary.json`.)

What the reading does not say: nothing about either lineage against the committed `20260907-minor-radius` values (availability ran live, no join made; record § 2); no boundary claim on any axis; nothing about the two lineages away from this window.

## 2. What the reading means for the goal

`goal.md` § Answered when: (a) landed natively — T-002 (WI-057 spec, design, review, plan, implement, audit PASS WITH FINDINGS fixed; commits `c2cd3ca9`…`b46decb0`); (b) number-neutral channel by channel via the ledger — this study, at the breadth the contract asked for (one committed sweep's window), on top of the per-commit baseline identity WI-057's plan recorded; (c) structured where the source is — WI-057's audit and SV-098 (23 occurrences, depth 3, 76 of 375 attributes at the root where 194 of 292 were, 28 ports, 15 connections; `work/active/WI-057_stellaris-structural-decomposition/evidence/`); (d) swappable — the swap demonstration (retyping `magnet` to a variant definition moves the structure cost by the markup and LCOE `224.60952472804465` → `224.72756193786321`, 17 channels move, the base calc dormant; `prototype/swap/results/summary.json`).

Proposed: the round closes on trigger 1 (a valid study reading — the useful positive). The round agent proposes to the fresh reviewer that (a)–(d) are met and that the goal is answered (trigger 6), with the goal's close and WI-057's `pm close-item` owner-held as the reserved gates say. The one reserved gate still open — gate 6, the blanket coolant premise (goal fact 6) — does not bear on (a)–(d): the item's limits forbade changing it, and this study's numbers are read with the premise as stated.

## 3. The finding dispositions proposed (record § 15, ids `20260913-structural-decomposition#n`)

| Id | Kind | Proposed disposition | Home |
|---|---|---|---|
| #1 | model | `model fix — none owed`: the useful positive; the item's close owner-held | goal § Answered when (b); WI-057 |
| #2 | model | `declared seam — standing, newly witnessed on this window`: the plant-closure lineage's evaluability exclusion (47 the committed pre-screen's non-positive-fuel coordinates; 56 complex-power coordinates new since the WI-044 pin; the committed 9 complex-power exclusions complete here); a sighting for the plant-closure goal, no disposition here | plant-closure goal; `20260829-p-pump-fence` § evaluability exclusion |
| #3 | process | `runbook step` candidate: a comparison study defines identity at non-evaluating points before the run; `CaseView` to carry `failure_json`; not edited | runbook §§ 9, 13; teax `simkit/study/query.py` |
| #4 | process | `tool` candidate: preflight cleanliness on an out-of-tree package (blob-hash against a commit, or `not_applicable`); not edited | `scripts/study/preflight.py`; runbook § 6 |
| #5 | process | `tool` candidate: `verify.py` oracle root from the manifest's root or `--root`; cleanliness accepting blob-hash evidence; not edited | `scripts/study/verify.py`; `manifest.py` `repo_root()` |
| #6 | process | `runbook step` candidate: one package per interpreter; not edited | runbook § 9; WI-057 swap README |
| #7 | process | `runbook step` candidate: a cross-lineage scan through one oracle module proves map consistency only; not edited | runbook § 7 |
| #8 | process | `tool` candidate: the Level 6 checker reads a definition-level EXPOSE (243 vs 227, 38 lines); not tuned | agentic-mbse Level 6; WI-057 audit F1 |
| #9 | process | `unrouted` — stated: committed study scripts against a later package (44 `KeyError` among the 86 already-failing fail-closed tests); the route is the owner's policy call | `tests/study/test_study_publication_fail_closed.py`; STUDY_POLICY § 6 |
| #10 | process | `tool` candidate: `pm register-decision` and the "Key Decisions" section; AD-008 appended by hand | agentic-mbse pm; ARCHITECTURE.md AD-008 |
| #11 | model | `owner gate` — parked as reserved gate 6; the loop fences read with the premise as stated | goal § Reserved gates (6), fact 6; WI-045 |

## 4. What is not touched

No committed record edited (STUDY_POLICY § 6). No tool, runbook, policy or skill edited; every candidate is a note for the owner to mint or not. No sighting row edited in `DISCOVERY_LOG.md`; eleven new rows appended under this record's ids. No reserved gate crossed: branch, scope, placement, renames, slug and swap form were ruled at grounding; gate 6 stays parked. WI-057 stays in `work/active/` until the owner closes it. `feat/model-viz` is not pushed.
