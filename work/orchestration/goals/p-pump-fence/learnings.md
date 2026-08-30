# Learnings: p-pump-fence

What this run now knows.

Append-only, newest last, ISO dates, never edited in place. An entry is appended **only after** a round review has accepted or corrected the delta the round result proposed (`GOAL_RUNBOOK.md` § The fresh review). Mechanical failures produce no learning.

Each entry is one claim.

*(No entries yet. Round 1 is open; its result proposes a delta and the fresh review accepts, corrects or rejects it before anything lands here.)*

**Carried in, not restated.** Three learnings of the closed predecessor goal bear directly on this one and are cited rather than copied: `work/orchestration/goals/p-pump-basis/learnings.md@104a68b5` L-001 (the sourced band is ~4–6 % for helium-primary blankets, and better than one significant figure is false precision), L-002 (`rec_frac` and `p_net` are recoverable post hoc from a committed record when every other recirculating term is bound), L-003 (`p_th` reaches nine cost accounts, so an LCOE effect needs a package run). They are that goal's, and they stay there.

---

## Round 1 — accepted 2026-08-29 by the fresh round review (session `88437945`)

Four claims, proposed at `trail.md` `### Round 1 result — 2026-08-29` and accepted with corrections to L-001, L-003 and L-004. The corrections and their reasons are in `trail.md` `### Round 1 review — 2026-08-29`.

**L-001. An audited held-input change reaches the package by regeneration, but every hand-maintained expectation of the package's output is invisible to the model layer. Only the integrate seam and the battery find them, one class at a time — and not all of them.**

Counted by artifact, the class had five members this round, each carrying a stale pre-WI-033 value and each repaired in its own commit: the manifest's `baseline.headline.value` (`cc249b89`), the independent oracle's held `p_pump` in `exploration/stellarator_e2e/verify_stellaris.py` (`2f0f5133`), the nine-anchor gate in `exploration/stellarator_e2e/run_stellaris_single.py` and `PINNED_LCOE` in `tests/study/test_operand_bindings.py` (both `6e05c12f`), and the `ANNEX.md § Baseline pin` literal (`0534c77b`). Four mechanisms found them: integrate gate 7 `preflight` (`evidence/integration-run-3/preflight_results.json`), integrate gate 8 `verification` (`evidence/integration-run-4/verify_stderr.txt`), the `tests/study` battery twice, and no mechanism at all for the fifth.

The tail matters more than the count. The fifth surfaced because the study executor read `ANNEX.md` for the package's ties, baseline pin, oracle and validity mask — a declared T-004 input — which is to say a reader went to the exact section that had gone stale, for a different purpose. That is a sharper bound than luck: the four mechanisms enumerate what they were built to enumerate, and nothing enumerates the rest.

Evidence: `trail.md` `### Amendment 2026-08-29`, `### T-002 return`, `### T-003 return`, and the counting rule at `### Checkpoint C-001.r2 submission` (by artifact five, by mechanism four; both committed statements stand unedited).

**L-002. An inherited window buys comparability and can silently cost containment.**

Adopting the comparand's grid was right and is what makes the fence positions subtractable — `study.py` reuses `study_route`'s own `R_VALUES`, `A_VALUES` and `BUILD_STACK_M`, so the two grids are the same object and not merely the same numbers. It also carried a frame built for a 1.0 MW machine to a 195 MW one, where it no longer holds the fence it was adopted to measure: at a = 0.80 every R from 4.0 to 20.0 m violates `recirc_ok`. Adopting a window is a decision that owes a re-check, not a free ride.

Evidence: `20260829-p-pump-fence/record.md` §§ 3, 6, 11, 17 and finding `#2`; `synthesis.md` § 5 `#2`; routed to `.claude/skills/run-study/runbook.md` step 7 by the disposition row for `20260829-p-pump-fence#2`.

**L-003. At this pin the model's unevaluable region overlaps the window studies actually sweep, so a study's proposed point count is no longer its evaluated point count.**

948 proposed, 42 unevaluable, 906 evaluated. The exclusion gives `net_positive` a clean sheet across all 906 that it did not earn: the comparand recorded `p_net` = +8.3 MW at the (4.0, 0.80) corner, and that same corner is −154.4 MW here. The record's § 4 does disclose this, in the same table cell; its § 15 finding text does not, which is where the reading travels from. A verdict that reads satisfied everywhere is worth checking against what could not be evaluated, and the check belongs with the finding, not only with the table.

Evidence: `record.md` §§ 4, 11 and finding `#1`; `results/excluded_points.csv`; `addendum/excluded_points_rec_frac.csv` (`rec_frac` above 1.0 at all 42, range 1.0027–1.8787); `synthesis.md` § 5 `#1`.

**L-004. A record can be arithmetically perfect and still fail its own contract — and so can the documents written to correct it.**

Every headline number in this record recomputed from committed artifacts, twice: once by the fresh administrator and once by this review directly from `results/points.csv`. A fresh administrator still found three places where prose carried numbers no artifact held (items 7, 9, 11). Recomputation checks the numbers that are there; nothing was checking for the numbers that were not.

The round review found the same shape three more times, twice inside the corrective documents themselves: the record's § 15 `#3` sighting was already stale when it was committed, the addendum's item-10 correction over-corrected two cells and left a third un-attributed when all three trace to committed artifacts, and the addendum described as "four grid points § 6 names" a set of which § 6 named two. Corrections are prose about numbers, and nothing checks them either.

Evidence: `synthesis.md` § 6 and its closing process finding, routed to `.claude/skills/run-study/runbook.md` steps 13 and 15 with no log id per `GOAL_RUNBOOK.md:248`; `trail.md` `### Round 1 review — 2026-08-29` findings 2, 3 and 4.
