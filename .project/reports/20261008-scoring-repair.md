# Scoring acceptance repair — 2026-10-08

[OWNER] Authorized proceeding with the scoring repair provided the explorer API is unchanged, and requested reading updated `CLAUDE.md`. [AGENT] Read its live-deployment guidance and Concept Explorer README §9. The Concept Explorer live API, CORS, served IDs and deployment files are protected. Existing owner edits to `CLAUDE.md` and that README are preserved and excluded from the repair commit.

[AGENT] **Complete scoring suite PASS, independently reviewed:** 357 passed, 41 existing skips, no failures/errors in 332.75 seconds. Of the 44 original failures, 42 now pass and two obsolete corpus-calibration tests are retired under the owner's direction. No historical replay test was added. [Final node attribution](20261008-scoring-attribution.json) verifies all outcomes, tested source hashes and protected bytes; [independent final review](20261008-scoring-review.md) passes.

## Requirements and scope

- [OWNER] Preserve the explorer API.
- [INFERRED] Repair the 44 recorded scoring failures against documented scoring changes without changing scoring formulas, weights, rankings, feature data, published explorer data or source evidence.
- [INHERITED: 20261008-model-codegen-repair.md] Preserve models, independent oracles, generated model packages, sealed studies, historical receipts and `.venv`; use `uv run --no-sync` only.
- [INFERRED] Distinguish raw formula calibration from corpus-normalized scores and preserve independently derived expectations, rather than copying current outputs into fixtures.
- [INFERRED] Run scoring/build tests against temporary outputs so qualification does not regenerate deployed data in place.
- [OWNER] Escalate important judgment calls about API or intended scoring changes and public data.
- [OWNER] Authorized clearing out old useless tests after discussing the limited value of historical calibration: “yeah I do not mind clearing out old useless tests”.
- [INFERRED] Retire obsolete normalized modularity calibration comparisons and assertions about old drift nominees. Retain independent current arithmetic, lookup coverage, normalization properties, determinism and explorer output compatibility. Record retired failures as retired, not passing.

## Plan and ownership

- [x] Reproduce the 44 failures and trace expectations to approved scoring changes.
- [x] Repair modularity/cost checks (worker), capacity-factor conformance (worker), and build/normalization isolation (coordinator).
- [x] Run the full scoring suite together and reconcile the original 44 nodes.
- [x] Obtain independent review, verify protected bytes, update reports and commit only repair files.

[AGENT] Workers own disjoint test files. Coordinator owns build/normalization tests, shared fixture changes if necessary, this report and final attribution/status. Any shared edit needs coordination. A non-author reviews the final repair and API/data preservation independently.

## Progress

[AGENT] Entry repair commit is `998a67e98`; two owner-authored instruction files are already modified. Modularity/cost workers reproduced their six failures. June 13 normalization (`298b7cc54`) separates raw calibration from normalized CSV scores; June 17 (`22d61f2bf`) explicitly converts the modularity prediction fixture to normalized values and adds IFE/MIF two-slot scoring. Later cleanup (`c8b0e11ee`) removes unreachable legacy lookup entries. Capacity-factor predictions remain raw and are now compared at that stage, with a separate normalized-output contract check. No prediction fixture or scoring weight changed.

[AGENT] Coordinator build/normalization checks pass twelve tests in 6.78 seconds. The builder executes unchanged against its retained inputs, with only output/printing globals temporarily redirected into pytest directories. Tests require all 38 current Score Explorer IDs, the exact documented exclusion set and surviving concept 30. The live Concept Explorer API and served concepts are unaffected. Normalization now compares fresh scores with raw values evaluated from the same inputs; it retains equal-tier checks and additionally requires monotone ordering and full 40-concept coverage. The retained diagnostic/JSON snapshots are not regenerated.

[AGENT] Capacity-factor conformance full-module qualification passes 197 tests with 44 existing skips in 359.09 seconds. All 34 original failed node identities now pass. The fixed prediction values, 0.55 tolerance, prediction expansion and pre-existing known-drift behavior are preserved; the normalized-stage invariant also passes. [Worker report](20261008-scoring-conformance-repair.md). This module result is separate from the unresolved tighter modularity contract.

[AGENT] Build/normalization component qualification passed twelve tests in 4.80 seconds with JUnit `/tmp/20261008-scoring-build-normalization.xml` and output `/tmp/20261008-scoring-build-normalization.log`. It covered four original failed identities. The initial independent modularity/cost selection passed nineteen tests, covering the other four original failed identities outside the two dependent whole-corpus tests. Later owner-authorized cleanup removed all obsolete drift bookkeeping. The final coherent qualification reruns every remaining test after that cleanup.

[AGENT] [Partial node attribution](20261008-scoring-partial-attribution.json) retains the earlier component-stage receipt: 42 original identities passed and two whole-corpus tests awaited a decision. The final receipt below supersedes that partial disposition. [Modularity/cost report](20261008-scoring-modularity-cost-repair.md) records current source arithmetic and the owner-authorized removals. Owner instruction and parallel API-contract-gate changes are excluded from the repair commit.

[AGENT] Eight recorded comparison-candidate failures and repository-wide style policy remain outside this batch. No fresh full-repository PASS, PR or push is claimed.

## Calibration disposition

[AGENT] Correct-stage comparison exposes two current modularity results outside the old normalized reference table's 0.20 tolerance: concept 23 is approximately 3.192 versus 3.42, and concept 37 is approximately 4.133 versus 3.73. Later approved capex population changed the corpus. These values are evidence that the reference is stale, not proposed new expectations.

[OWNER] Accepted clearing out old useless tests after asking what historical calibration contributes to current correctness. [AGENT] Retired the obsolete historical comparisons and drift bookkeeping; preserved current scoring arithmetic and normalization checks. No historical replay test was added. Final qualification accounts for the two original corpus-calibration failures as retired by this disposition.

[AGENT] All five touched test files pass lint and formatting. Four obsolete modularity functions and forty stale normalized prediction parameters are removed. Seven current raw arithmetic cases, independent cost sums, active lookup/bracket checks, fresh 40-concept normalization, full-scorer determinism and explorer JSON/ID/composite checks remain. Final modularity/cost modules pass seventeen tests. Independent code inspection finds no coverage gap. Protected hashing covers 84 files, including the parallel owner-authored API-contract-gate records. The shared current-work section is staged separately from that owner's uncommitted section.

## Final qualification

```bash
bash /tmp/fusion-tea-study-repair-tests.sh -q -ra --tb=short --junitxml=/tmp/20261008-scoring-suite.xml tests/scoring_v2
```

[AGENT] Exit 0, **357 passed and 41 existing skips in 332.75 seconds**. No exclusions, additional skip/expected-failure markers or tolerance relaxation were introduced. The runner uses the retained runtime with `uv run --no-sync`, project license initialization before imports and serialized archive-reader aliases; aliases are removed after completion. [Receipt](20261008-scoring-attribution.json) matches all fifteen captured Python source hashes and all 84 protected hashes. It records 42 passing original identities, two retired original identities, two additional obsolete test functions and forty retired prediction cases. Retired nodes are absent from collected output and are never reported as passes.

[AGENT] Log `/tmp/20261008-scoring-suite.log`, JUnit `/tmp/20261008-scoring-suite.xml`. Published JSON, scoring weights/features/formulas, Concept Explorer API/CORS/served IDs, model/oracle/package/sealed evidence and dependencies are unchanged. `git diff --check` passes. Only scoring repair files and its status section are staged; owner instruction, backlog and parallel API-contract-gate records remain outside this commit. The wider PR gate remains FAILED until the other recorded tests and style disposition are resolved.
