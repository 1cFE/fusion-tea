# Audit: Verified Package Integration Seam (GSTH Item 3)

**Verdict:** POSITIVE — Certify
**Audited:** 2026-08-26
**Branch:** `feat/goal-integration-seam`
**Commit:** `30f10847` (implementation head `9151f853`)
**Auditor:** fresh session; did not build any of this

---

## The Point

Integration is the hop between an audited model change and a study that can run against it. Every gate that hop needs already existed and already failed closed — the provenance suite, `sysml-codegen generate`, the model-family spine suite, `manifest.py`, `preflight.py`, `verify.py`, `identity.py`. What did not exist was a boundary that owned them together. The sequence lived in two work-item plans and a pile of shell commands; neither was callable, and the cost was already paid once, when Item 6's Phase 2 opened with eleven red tests because a scaffold commit changed a manifest without re-pinning the fixtures. The check existed; no gate was bound to the hop.

The obligation: turn audited model work into exactly one verified, study-ready candidate pin and fingerprint, or a named blocker — and make the blocker say whether a gate *refused* or *could not run*, because a goal caller's retry rule reads that distinction and a goal round closes or continues on it.

## Summary

The seam does what it was specified to do. Ten gates run in the producers' own order, stop at the first non-pass, and every one of them is the producer's own — invoked as a subprocess, never mocked, never thinned, never reimplemented. Both frozen-producer checks hold: `git diff --stat fa5245f0^..HEAD` over `scripts/study/`, `tests/models/` and `tests/test_dependency_provenance.py` is empty. Both claimed test counts reproduce exactly. The SC6 operator-guide walk succeeded from the guide alone, with zero source reads — which is the criterion the sibling seam failed.

What is wrong is confined to how the return *reports* a stop, not to what it decides. The gate that stops the sequence is recorded `not reached` — literally "the sequence stopped before this gate" — for a gate that ran and refused, and the guide asserts that label "tells you nothing about that gate." That is one undocumented deviation from design D4 and one false sentence in the guide. No candidate is ever promoted wrongly by it; the `blocker` block carries the truth. Four smaller items sit under it.

## Product Judgment

**Is this the right piece of work? Yes.**

Product-lens ledger gate: **CLEAR**. Four blocks were raised across the spec and design passes (spec-F1 unchecked expected lineage, spec-F2 no refused/could-not-run distinction, design-F1 gate 5's false "names no package" claim, design-F2 the return cannot carry `PREREQUISITE`). All four are resolved by citation in later ledger blocks — spec-F1 → R-C9 + gate 9, spec-F2 → R-A6 + the two modes, design-F1 → D13's per-gate `scope`, design-F2 → D14's fourteen condition slugs with the goal-class mapping in the guide. I re-checked each resolution against the shipped code: gate 9 exists and refuses (`scripts/integrate.py:1301`, proven live below), `mode` is `refused`/`could_not_run` and never anything else (`:211`), every gate row carries `scope` (`:1382`), and the closed slug set is enforced by the constructor (`:209`). No unresolved BLOCK. No epic-level block recorded.

No structural smell fired. Specifically checked, since the fusion-tea acceptance-test signature is exactly this shape:

- No test passes by selecting one of two representations. The success path and the refusal paths run the *same* seam CLI as a subprocess against the *same* workspace, and the workspace's equality with the committed state is asserted file-by-file before any test runs (`tests/study/conftest.py:436-437`).
- Nothing is kept manually in sync. The guide is pinned to the code by a contract test that reads `CONDITIONS`, `REQUIRED_ENV`, `GATES` and the argparse flags out of `scripts/integrate.py` and asserts each appears in the guide (`tests/study/test_integrate_guide_contract.py`).
- No special category exempts a case. The two uncovered things — gate 5's refusal path and `assert_read_set_covered` — are stated in the guide's "What the seam does not check", stated in gate 6's own *passing* detail text at runtime, and filed as BACKLOG rows. I saw gate 6's disclosure fire in my own run.
- No compatibility shim preserves behaviour the seam exists to refuse. `D12` refuses lock, ledger, retry and idempotency wrapper, and I found none in the source (R-F2 holds).

The one judgment worth naming: ADR-009's "the seam proves, it does not perform" is a real product decision, not a scoping dodge. It means the seam refuses model work that has not been regenerated and committed, and hands that work back to the modeling item. That is more useful than a seam that silently performs the hop, because the mutation then happens where it can be reviewed and committed. The guide leads with it, which is the right call.

---

## SC6 — the operator-guide walk

This is the criterion I own by construction, so it is recorded in full: what I ran, what came back, and **every point where I had to read source or guess.**

I read `docs/integration_seam_operator_guide.md` and nothing else before starting. Source reads during the walk: **zero.**

### 1. Assemble and invoke

The guide's § "The full invocation, first" carries a complete, copy-pasteable command with all thirteen flags and the two `--env-file` values. I ran it verbatim.

**Result: exit 0, `CANDIDATE`, all ten gates pass, ~20 s.** First attempt, no iteration.

Environment: the guide named both files (`~/1cfe/agentic-mbse/.env` and `.venv/integration.env`) and the exact `uv run --env-file ... --env-file ...` form, so the brief's "if it doesn't, that's a finding" does not fire. It also explains *why* two flags rather than `export`, and separately lists all six variables with what reads each — so a reader whose `.venv/integration.env` is missing can rebuild it.

### 2. Read the return

`<out-dir>/integration_return.json`, as documented. `class: "CANDIDATE"`, `exit_code: 0`, `blocker: null`, ten gate rows all `pass`, a `candidate` block with all eight documented fields. The stderr summary is a `preflight`-style per-gate read. Nothing here needed source.

### 3. CANDIDATE vs BLOCKER

Decided from `class` and the exit-code table. Both are documented and both agreed with what I got, on all three runs.

### 4. Act on a blocker — the full loop, from the guide alone

The guide's input table says `--expected-teax-revision` is one of four flags "optional to `argparse` but **not** optional to the answer: leave one out and its gate reports *could not run*, which is a `BLOCKER`, not a pass." So I dropped it.

Got: exit 1, `mode: could_not_run`, `condition: input-missing`, `gate: teax-revision`, with `detail` naming the flag. The condition table's row for `input-missing` says "Add the flag. `detail` names it." I added it back — that is run 1 above, which returned the candidate. **The loop closes entirely inside the guide.**

I also drove a semantic refusal to check the other mode: a wrong `--expected-semantic-fingerprint`. Got exit 1, `mode: refused`, `condition: lineage-mismatch`, with `expected` and `actual` both populated — which is what the condition table told me to compare. The two modes are genuinely distinguishable by a caller.

### 5. Cite the candidate in a study

The guide's § "Citing a candidate in a study" `jq` block ran verbatim from the repo root: `preflight.py gates` → exit 0, six of six.

The store-path derivation — the one thing the guide says you derive rather than read — was exactly right: `executed_under.store_id` in the baseline result was the bare filename `stellarator-baseline-point-v1.db`, and the store was at `<out-dir>/_work/` under that name, as documented.

### Every point where I had to read source or guess

Two, both minor, neither defeating:

1. **`candidate.package` came back as a path I did not type.** I passed `--package exploration/stellarator_e2e/pkg/stellarator_tea`; the return named `exploration/stellarator_e2e/generated`. I did one filesystem read (`ls -la` on the `pkg/` directory — not a source read) and found the tracked symlink. The guide never says the returned package path is the *resolved* target rather than what you supplied. **Guide gap, low severity** — see finding 4.
2. **The guide misled me once, and the return corrected it.** On the lineage-mismatch run, the stderr summary printed `not reached  request  lineage: the sequence stopped before this gate` for the gate that had just refused, and the JSON gates array said the same. The guide's § "Reading the answer" states that `not reached` "means the seam never got there, and tells you nothing about that gate." I believed it for about ten seconds, then read the `blocker` block, which named `gate: "lineage"` correctly. **This is finding 1** and it is a defect in the return, not only in the guide.

**SC6 verdict: MET.** A non-author assembled a real request, invoked the seam, read the return, told CANDIDATE from BLOCKER, cited the candidate in a study, and acted on a named blocker, working from the shipped guide alone. The guide is accurate on every operational point except the one sentence in finding 1 and the omission in finding 4.

---

## Verification of the implement report's claims

Every claim reproduced. Nothing drifted.

| Claim | Result |
|---|---|
| Focused suite `pytest tests/study -q` → 341 passed, 1 skipped | **341 passed, 1 skipped** in 323 s. Exact. |
| Regression gate `pytest tests/models tests/study tests/test_dependency_provenance.py -q` → 392 passed, 14 skipped, 0 failed | **392 passed, 14 skipped** in 331 s, exit 0. Exact. |
| R-B2: `git diff --stat fa5245f0^..HEAD -- scripts/study/ tests/models/ tests/test_dependency_provenance.py` empty | **Empty.** |
| R-G3 hermeticity: no test writes a tracked file | **Verified, not trusted.** `git status --porcelain` empty before and after both suite runs. `.integration_workspace/` does not survive either run and is gitignored (`.gitignore:40`). |
| The seam-internal-error bug is fixed | **Verified by inducing it** — see finding 3. |

---

## Findings

Ranked. **None is a blocker.** All six are reporting, coverage or documentation issues; none causes a wrong candidate to be promoted or a refusal to be missed.

### 1. The gate that stops the sequence is recorded `not reached`, which is false — and the guide asserts the opposite

`scripts/integrate.py:610-612`, `:597-607`, `:1382-1391`; `docs/integration_seam_operator_guide.md:144`.

`fill_not_reached` fills every gate from `len(results)` onward with `status: "not reached"` and `detail: "the sequence stopped before this gate"`. `results` holds only the gates that *passed*, so the blocking gate is in the filled range. `gate_result` hard-codes `status: PASS`, so `FAIL` and `DID_NOT_RUN` are imported (`:102-103`) but never written into a seam gate row — they are used only to *read* preflight's own document (`:1249-1250`). The seam's gate vocabulary is two-valued in practice: `pass` and `not reached`.

**Failure scenario, observed live:** a lineage refusal. Gate 9 ran, read both fingerprints off the package, compared them and refused. Its row reads `not reached — the sequence stopped before this gate`. A reader following the guide's rule that `not reached` "tells you nothing about that gate" would conclude the lineage was never checked, when it was checked and it failed.

**Design deviation, undocumented.** D4 (`design.md:96`) says every gate result carries `status` from `preflight.PASS`/`FAIL`/`DID_NOT_RUN`, with `not reached` as a *fourth* status for gates after the stop. `design.md:168` says "Every **later** gate is `not reached`." The implementation gives the blocking gate the later-gate treatment. Nothing in `plan.md` records this as a deviation.

**What should change:** the blocking gate's own row carries `fail` (for `refused`) or `did not run` (for `could_not_run`) with the blocker's `detail`; `not reached` stays for the gates strictly after it. The guide's line 144 then becomes true as written.

**Test note:** the refusal tests step over the blocking gate's index rather than asserting it — `document["gates"][2:]` at `tests/study/test_integrate_refusals.py:44`, `[1:]` at `:93`, `[3:]` at `:136`. Whatever the intent, the effect is that no test pins the blocking row's status, so the current behaviour is unasserted in either direction.

### 2. A seam-internal error mid-sequence names the wrong gate

`scripts/integrate.py:1441-1446`.

The top-level handler builds its blocker with `gate=PRECONDITIONS` regardless of where the fault occurred.

**Failure scenario, proven:** I induced a `ValueError` inside gate 3 (`handwritten-preservation`) with the sequence otherwise untouched. The return carried `blocker.gate == "preconditions"` and `scope == "request"`, while the gates array showed gates 1a, 1b and 2 passing. The guide's BLOCKER schema (`:131`) presents `gate` as the gate that stopped the run, so a reader files this against gate 0 and looks at their inputs, when the fault is at gate 3.

**What should change:** carry the gate that was executing when the exception escaped, or a sentinel that is not another real gate's name.

### 3. The exit-2 path has no test, and it is the path a real bug was found in

`scripts/integrate.py:1437-1454`; `plan.md:934-937`.

The plan records a genuine bug found and fixed here during Phase 7: the seam-internal-error return discarded the partial sequence, so a reader saw nothing had run when several gates had passed. **I verified the fix is real** — inducing a fault at gate 3 returns exit 2, `class: BLOCKER`, `condition: seam-internal-error`, `seam_traceback.txt` written and cited by path, and the three passed gates preserved in the array. It works.

But `grep` over `tests/study/` finds no assertion on exit code 2, on `seam-internal-error`, on `seam_traceback.txt`, or on partial-result preservation. A fixed bug with no regression test is a bug with a return ticket.

**What should change:** one test that monkeypatches a gate implementation to raise and asserts exit 2, the condition slug, the traceback file, and that the earlier gates' `pass` rows survive.

### 4. `--out-dir` outside the repo yields `../`-escaping citations, and the guide does not say what they resolve against

`docs/integration_seam_operator_guide.md:125`, `:60`; `scripts/integrate.py:1355-1359`.

The guide says "Every path is repo-relative" and tells the operator to put `--out-dir` "anywhere you like, as long as it resolves outside the package root." Following both, with `--out-dir /tmp/integration-run`, the candidate cites `identity_document: "../../../../tmp/integration-run/package_identity.json"`.

**Failure scenario:** the guide's own study-citation `jq` block works from the repository root and silently breaks from any other working directory, with a path-not-found from `preflight.py` that says nothing about cwd. The guide never states the resolution base.

**What should change:** state that repo-relative means relative to the repository root, or emit an absolute path when the target resolves outside the repo. Also add one line to the input table or the CANDIDATE section noting that `candidate.package` is the resolved target, which is what defeated me at walk point 1 (the tracked package root is a symlink).

### 5. `clean.json` is computed, written, and never cited

`scripts/integrate.py:530-551` returns the repo-relative path of gate 0's `clean.json`; the call site at `:1428` discards it. The guide lists `clean.json` among what the seam writes (`:238`), so an operator can find it, but the return does not point at it. Gate 0 is not one of the ten rows, so no requirement is violated — this is a computed-and-thrown-away value, and either the return should cite it or the function should not build it.

### 6. `plan.md` still shows an environment recipe its own Phase 4 note rejected

`plan.md:670-675` gives `set -a; source ~/1cfe/agentic-mbse/.env; set +a` plus five `export` lines. `plan.md:841` records that the sandbox rejects `set -a; source` and that the shipped delivery is `.venv/integration.env` + `uv run --env-file`. The guide has it right; the plan's block is stale and would send a reader down the path that does not work.

---

## Spec conformance

Every success criterion and every R-clause landed, or its absence is recorded where the spec said it would be.

### Success criteria

- **SC1 — MET.** One invocation, one candidate. Verified live and by `tests/study/test_integrate_success.py`: ten gates pass, all eight candidate fields resolve on disk, `pin` equals the manifest's own `fingerprints.indicator_inputs.digest` read independently (`:70-75`), both fingerprints equal the lineage the request named, the package is byte-identical before and after (`:78-82`), and the cited `verification_summary.json` reads `outcome: pass` with `verdicts_rederived: true`.
- **SC2 — MET.** Six real refusals from six real producers in `test_integrate_refusals.py`, each driven by a caller-supplied input, each asserting producer, scope, mode, condition slug and evidence path. Plus four could-not-run fixtures. R-B5's one producerless gate (1b) is the seam's own comparison and its absence is filed. I independently drove two more refusals by hand.
- **SC3 — MET.** `test_integrate_rerun.py` asserts the five package-describing fields are identical across two runs and that the three `--out-dir` fields differ — the exclusion proven rather than assumed. It also pins that the second run is a `CANDIDATE`, not a refusal, which is R-D4's confirmed branch. My own two full runs produced the same pin and fingerprints.
- **SC4 — MET.** `test_integrate_stock_route.py` rebuilds both stock command lines from `integration_return.json` and the documents it cites, imports no seam code, and proves it by reading its own import lines (`:88-96`). I reproduced this by hand from the guide.
- **SC5 — MET.** 392 passed / 14 skipped / 0 failed on the regression gate; the three frozen paths untouched.
- **SC6 — MET.** See the walk above.

### Requirements

- **R-A1/A2/A3** — met. Missing required input → `input-missing` before any producer (`:446-451`); two `--package` values → `input-invalid` (`:420-428`), tested; the CANDIDATE names one of everything and the BLOCKER names producer, why, and evidence path, with `expected`/`actual` on a lineage mismatch.
- **R-A4** — met. One CLI script (D1), reachable by hand and by an agent's Bash tool. I reached it by hand.
- **R-A5** — met. `integration-seam-return/v1`, machine-readable and pasteable.
- **R-A6** — met, and this is the clause the concept-design turns on. `mode` is constructor-enforced to `refused` or `could_not_run` (`:211-212`). Six variables swept at gate 0 *before* any producer (`:493-506`) so a missing wheel variable can never be reported as toolchain drift — the exact misreport this clause exists to prevent, tested six ways (`test_integrate_preconditions.py:79`).
- **R-B1** — met, in order. `GATES` (`:179-200`) is 1a, 1b, 2, 3, 4, 5, 6, 7, 8, lineage; `run_sequence` iterates `GATES`, never the dispatch mapping (`:1402`), so the order cannot drift from the table. Every index reference checked against its gate.
- **R-B2** — met. Diff empty over all three frozen paths.
- **R-B3** — met. The return cites producer output by path; no producer's stage state is mirrored.
- **R-B4** — met. Stop at first non-pass, producer-grain. The preflight blocker cites the whole six-gate results document rather than one row, and a test asserts exactly that (`test_integrate_refusals.py:225-232`).
- **R-B5** — met. Gate 1b is the seam's own `rev-parse` comparison against a caller-supplied expectation, fail-closed when absent (`:905-910`), and the producer gap is filed as BACKLOG row 30.
- **R-C1–C5, C9** — met, each with a condition slug and a real refusal fixture, except gate 5's refusal content (recorded boundary, below).
- **R-C6** — met. Nothing repairs. Byte movement is refused, and the tree is restored to what it was, which is the opposite of repair (`:809-826`).
- **R-C7** — met. Nothing writes into a committed study record.
- **R-C8** — met, by ordering plus D7's copy-restore. Verified live: the tree was clean after a candidate run, after two refusal runs, and after the induced exit-2.
- **R-D1–D4** — met. The pin is the manifest's own value, not a minted one; SC3's test pins the same-identity branch.
- **R-E1–E4** — met. The return is one document; it carries which gates ran, in what order, what each returned and where each producer's output sits; every digest resolves; the `toolchain` block records all four revisions and is asserted (`test_integrate_success.py:94-98`).
- **R-F1–F5** — met. No commit/push/close. No hardening machinery — I looked for a lock, ledger, retry or idempotency wrapper and found none. No pinned-tool edits. The calc-then-compare limitation is untouched. Six R-F5 filings exist (BACKLOG rows 29–34).
- **R-G1, G1a, G2, G4** — met. Success, refusal and re-run shapes all covered; SC4's fourth shape covered by a module that imports no seam code; every refusal is a real producer's, no mocks anywhere in the gate path.
- **R-G3** — met, verified rather than trusted (see the claims table).

### Recorded non-coverage — both stated where the spec said they would be

- **Gate 5's refusal content is untested**, on purpose. `tests/models/test_model_family_spines.py` takes no package argument; driving a real refusal needs an edit to the tracked census (breaks R-G3), to the canonical `models/` tree (a model change), or to the suite (frozen by R-B2). The shared junit-`<failure>`-to-`refused` mapping *is* proven, by gate 1a's real wheel-hash refusal. Stated in `plan.md:63`, in the guide's "What the seam does not check", and filed as BACKLOG row 31. **Not papered over with a mock**, which R-G4 forbids.
- **`assert_read_set_covered` is out of reach** and covered by nothing else in the repository. Stated in D17, in the guide, in BACKLOG row 33 — and, unusually and correctly, in gate 6's own *passing* detail at runtime, so a reader of a green return sees the shortfall. I saw it fire in my own run.

## Design conformance

Implementation follows the design, with one undocumented deviation.

- The ten-gate table, the order, the stop rule, the two return classes, the two modes, the fourteen condition slugs, the per-gate `scope`, the single subprocess environment (D16), the caller-named route driver (D6), the content-digest byte judgment (D8), the copy-restore (D7), the exit-code contract (D18) — all present and matching.
- **D19, D20, D21 are sound and honestly graded.** Each is marked `[AGENT]`, dated at implement, states what was rejected and why. D21 in particular records a *measured* false refusal (60+ `.pyc` files) as its cause rather than asserting a principle — that is the right shape for a mid-implementation deviation. D20's reasoning is correct and load-bearing: had gate 2 compared the whole tree, gate 3's `handwritten-lost` condition would have been unreachable, which is dead code wearing a gate's name.
- **D4 is deviated from, undocumented** — finding 1.

## Code integrity

`scripts/integrate.py` is 1477 lines and reads as one thing. No god functions, no sentinel-mode parameters, no policy hiding in a utility, no copy-paste siblings, no nesting past two levels. Every gate's contract is readable from its signature and its docstring says what it judges and why it is its own gate.

- **Placeholders/TODOs:** none. `grep` over the seam and all eight test modules for `TODO`, `FIXME`, `XXX`, `NotImplementedError`, `placeholder` returns nothing.
- **Dead code:** none. Every module-level `def` has a caller in the seam or in the tests. The `state` parameter unused by three gate functions is dispatch-table uniformity, not sprawl. The one genuinely discarded value is finding 5.
- **Failure honesty:** good. The two broad excepts are both honest and both documented at the point of use — `recapture_snapshot` (`:1028`) converts the producer's own failure into a named `could_not_run` carrying the exception type and message, and the top-level handler (`:1437`) converts an escaped exception into exit 2 with a traceback file rather than swallowing it. Neither returns a safe default. `build_return` goes the other way and *raises* when it finds no blocker and an unpassed gate (`:626-631`) — the seam refusing to emit a candidate it cannot justify, which is the right instinct.
- **No optional parameters papering over missing data.** The four flags that are optional to argparse are optional *by design* (D2) and each one's absence produces a named `could_not_run` at the gate that needed it, never a pass. Four tests pin exactly this.
- **One smell, named rather than absorbed.** Gate 4 imports `_by_entry_type`, a private helper inside a test module (`:1043`). The docstring calls it "a real smell", says the cause is that the census derivation has no importable home, and files it against that module. Filed as BACKLOG row 29. Reaching into a test module from a production tool is genuinely wrong — but the alternative was a second implementation of the classification, which R-B1 forbids and which is the exact drift the gate exists to catch. Correct call, correctly recorded.
- **Auto-memory constraints respected.** No fallbacks for missing inputs (`feedback_no_fallbacks`) — every absent input fails closed. No workaround formalizes an invariant the platform declares (`feedback_workaround_smell_is_bug`) — every workaround has a filed row against its producer's own home.

## Filings

All present and correctly placed.

- **ADR-009** (`.project/adr/009-integration-is-a-fixed-point-proof.md`) exists with complete frontmatter — `status: accepted`, date, deciders, `grade: "[AGENT] 2026-08-26"`, `supersedes`/`amends: none`. Indexed in `.project/adr/INDEX.md:15`, which is where `README.md:57` says the register lives. Cited from the guide. A test pins all three (`test_integrate_guide_contract.py:80-84`).
- **Six BACKLOG rows** under `.project/backlog/BACKLOG.md` § Flagged, exactly where `plan.md:1093` says: census derivation has no importable home (29), no automated teax revision pin (30), the spine suite is not parameterizable by package (31), `verify.py` collapses both failure modes (32), `assert_read_set_covered` has no caller (33), `verify.py` records `teax.revision: "unrecorded"` (34).
- **The unrelated `tests/scoring_v2` failures are filed and not absorbed.** Row 35 records both halves — the non-hermetic explorer-build test that rewrites `tools/score_explorer/data/concepts.json`, and the 44 failures in `TestSpecPredictedScoresLand` — and states plainly that they were surfaced by this item's sweep and **not caused by it** (that item touches nothing under `exploration/scoring_v2/` or `tools/`), with the prior baseline of 34 cited so the growth is visible. Out of scope here. I confirmed by inspection that nothing in the seam, its tests or the guide silently absorbs them.

---

## Certification

**Certify.** Product-lens ledger gate is CLEAR with no unresolved BLOCK; no structural smell fired.

Checked and verified this pass:

- The SC6 walk, performed from the shipped guide alone, end to end, including a full blocker→act→candidate loop and a study citation.
- Both test claims, reproduced exactly (341/1 and 392/14/0).
- R-B2 frozen-producer diff, empty.
- R-G3 hermeticity, empirically — `git status --porcelain` clean before and after both suite runs, workspace torn down.
- The ten-gate sequence and stop rule against the design table, index by index.
- The fourteen condition slugs against D14, the plan and the guide — all three agree, and the set is closed at the constructor.
- Every R-clause and every SC.
- The seam-internal-error fix, by inducing a real fault mid-sequence.
- All seven filings (ADR-009 + six BACKLOG rows) and the scoring_v2 row.
- Placeholder hunt, dead-code sweep, error-path honesty over all 1477 lines of `scripts/integrate.py` and all eight test modules.

Marked as a result: spec SC1–SC6, plan Phases 1–10, and the epic Item 3 success checkboxes.

Findings 1–6 are recorded for a follow-up pass, not held against certification. Finding 1 is the one worth doing first: it is a false sentence in a shipped operator guide and a false `detail` string in a shipped return, and the fix is small.

**Not checked:**

- **The whole-repo suite.** I ran `tests/models`, `tests/study` and `tests/test_dependency_provenance.py` — the R-B2/R-G2 gate as written. I did **not** run `pytest tests/`, so the 44 `tests/scoring_v2` failures and the tracked-file write recorded in BACKLOG row 35 are taken from the plan's Phase 10 record, not independently reproduced.
- **Gate 5's refusal content.** Untestable by construction and recorded as such. I verified the boundary is stated in three places and filed; I did not attempt to drive a spine-suite refusal.
- **Gate 3's refusal content in production.** The `handwritten-lost` path is covered by the design's reasoning (D20) and by the gate-2/gate-3 partition, and gate 3's pass path ran in every one of my invocations. No fixture drives a real handwritten-preservation loss; `test_integrate_refusals.py` covers gate 2's byte-movement refusal, not gate 3's.
- **`verify.py`'s refusal path through the seam.** No fixture drives gate 8 to refuse. Its `verification-refused` slug and the D15 residual are reasoned about in the design and filed as BACKLOG row 32, but I saw only gate 8's pass path.
- **Longer-horizon identity stability.** SC3 is two runs in one session under one toolchain. I did not test across a toolchain bump or a fresh checkout.
- **The goal-layer consumption of this return.** Item 6 is the consumer; the `condition` → goal-class mapping lives in the guide and no goal-side code reads it yet. I verified the mapping is documented and complete, not that a goal agent uses it correctly.
- **Upstream producer correctness.** I audited that the seam invokes each producer and reports its verdict faithfully. I did not re-audit what `preflight.py`, `verify.py`, `manifest.py` or the two pytest suites themselves check.
