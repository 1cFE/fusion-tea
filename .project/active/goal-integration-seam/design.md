# Design: Verified Package Integration Seam

**Status:** Draft
**Owner:** Reid W
**Created:** 2026-08-26
**Updated:** 2026-08-26
**Branch:** `feat/goal-integration-seam` (commit `a4b45a85`)
**Epic:** Goal Strategy and Task Harness (GSTH), Item 3

## Overview

One fusion-tea-side CLI runs the eight producer-owned gates in the spec's order against a named package and emits exactly one `CANDIDATE` or `BLOCKER` document. It writes nothing into the tracked tree: every producing step is invoked in place and required to be a no-op, and anything that moves is the refusal.

## Related Artifacts

- **Spec:** `.project/active/goal-integration-seam/spec.md` (revised through spec review, 2026-08-26)
- **Spec review:** `.project/active/goal-integration-seam/spec_review.md` · **Lens:** `product-lens.md` · **Align:** `align.md`
- **Spike:** `.project/active/goal-integration-seam/spike_regen_determinism.md` — R-D4 CONFIRMED
- **Spike:** `.project/active/goal-integration-seam/spike_snapshot_stability.md` — B2 CONFIRMED; snapshot recapture is byte-identical to the tracked file and there is no `captured_at` key
- **Epic:** `.project/backlog/epic_goal_strategy_task_harness.md` § Item 3
- **Sibling precedent:** `.project/active/goal-research-seam/design.md` (Item 2)
- **Referents:** `work/completed/20260822_WI-030_computed-beta-peak-field/plan.md` Phases 3–5; `.project/completed/20260821_stellarator-model-migration/plan.md` Phases 2–3; `.project/active/run-study-first-consumer/plan.md` Phase 3
- **Decision records read:** `.project/adr/INDEX.md`, all eight entries. `006-goal-evidence-seam.md` binds this design: the return cites native artifacts by path, never mirrors their state. `003-lean-first-persistence.md` binds it too: prose files and native facts, hardening only on an observed failure. No entry is contradicted; one new entry is proposed (Appendix A).

## The Point

`[INHERITED: epic Item 3 Objective, agent decomposition ratified by owner 2026-08-25]` Turn audited model work into exactly one verified, study-ready candidate pin and fingerprint, or a named blocker.

`[INHERITED: .project/concepts/goal-strategy-task-harness-design.md § Native seams]` Integration is the hop between an audited model change and a study that can run against it. Every gate that hop needs already exists and already fails closed. What does not exist is a boundary that owns them together: the sequence lives in two work-item plans and a pile of shell commands, and a goal task cannot request integration without reconstructing the hand pattern. The cost has been paid once already — Item 6 opened with eleven red tests because a scaffold commit added an objective to the manifest without re-pinning the fixtures. The check existed; no gate was bound to the hop, so it fired far from the commit that broke it and only when a human happened to run the suite.

Two things make the return usable rather than merely correct. `[INHERITED: concept-design § Problem, § Task-grain invocation]` A goal agent reading a `BLOCKER` must be able to tell an operational accident it may retry from a semantic result that changes what work is justified — an unexported licence key is not a refusal. `[INHERITED: epic Item 3 Deliverables]` And a person who did not build the seam must be able to operate the whole thing from its own documentation.

## Research Findings

Everything below was read or run in this worktree.

**Every producing step already has a checking form, and the checks are the same code.** `preflight.check_manifest_currency` (`preflight.py:233`) compares the manifest's recorded fingerprints against the live contracts — that is the re-pin, read backwards. `manifest.assert_pin_matches` (`manifest.py:451`) recomputes `indicator_input_fingerprint` over the live package and compares it to the manifest's pin — the read-set half of the re-pin, read backwards. `test_mfe_census_is_the_one_captured_from_the_first_clean_package` (`test_model_family_spines.py:349`) compares `data/mfe_census.json` against a fresh canonical-subset generation, and fails with "model meaning moved — re-derive" when the census is stale (WI-030 saw exactly this, `WI-030 plan:129`). `identity.assert_matches` (`identity.py:288`) recomputes rather than trusts.

**The spine test is already hermetic and already generates.** `baselines` (`test_model_family_spines.py:243`) generates each family from a materialized canonical subset into `tmp_path`; `test_family_subset_generates_and_live_equals_snapshot` (`:308`) captures a snapshot into `tmp_path` and compares. Nothing in that suite writes into `exploration/`. It needs `SYSIDE_LICENSE_KEY` (`license_must_be_loaded`, `:114`) and errors rather than judges without it — the R-A6 live instance the spec names.

**`preflight.py` is the blocker-taxonomy shape to match.** `run_gates` (`:333`) loads four documents first, records each load error, and `unavailable()` (`:368`) turns a load error into the named condition a check could not run under. `PASS` / `FAIL` / `DID_NOT_RUN` are module constants (`:85-87`); the seam imports them rather than re-spelling them.

**Verification needs an executed store, and the route is package-specific.** `verify.build_summary` (`:414`) opens each `--store` and `verify_store` (`:343`) refuses a store with no completed cases. `preflight gates` needs `package_identity.json` and `baseline_result.json`. Both documents are deposited by `study_route.execute_baseline(out_dir, *, package_dir, manifest_path)` (`exploration/stellarator_e2e/studies/study_route.py:358`), which runs the manifest's own pinned baseline point. That module names the package; `scripts/study/` never does ("generic by construction … names no package", every producer's module docstring). `execute_baseline` returns the identity and baseline-result paths but **not** the store path; the store is named in `baseline_result.executed_under.store_id` (`study_route.py:381`), repo-relative when the output directory is under the repo root and a bare filename otherwise.

**`git status` cannot be the byte-movement gate on its own.** `common.git_status_porcelain` (`common.py:60`) runs from `manifest.repo_root()` — `scripts/study/`'s own grandparent, i.e. the fusion-tea worktree — with `-- <resolved path>`. A package outside the repo makes git error; a package inside the repo but gitignored reports clean whatever its bytes do. So the seam computes its own before/after content digest over the package tree (the spike's technique, `spike_regen_determinism.md` Step 2) and lets `preflight.check_package_clean` remain the producer's own git gate on the real tree. The two are complementary, not redundant.

**The stellarator package root is a tracked symlink.** `exploration/stellarator_e2e/pkg/stellarator_tea` → `../generated`; git operations resolve through it.

**A package-copy factory already exists** — `package_copy` (`tests/study/conftest.py:191`) copies a package, manifest and axes into `tmp_path` and rewrites `package.path` to a repo-relative path. It does not exercise `package_clean`, and `tmp_path` is outside the repo, so it cannot carry the seam's git-backed gates unchanged. `stock_route_run` (`:274`) and the `STOP_PARSER_TEAX_ROOT` / `STUDY_REQUIRE_TEAX` skip machinery (`:239-270`) are directly reusable.

**Snapshot recapture is byte-stable, and the tracked snapshot carries no `captured_at`.** Measured by spike (`spike_snapshot_stability.md`): three recaptures — twice from the real `models/` root, once from a `/tmp` copy — all produced a file byte-identical to the tracked `stellarator.snapshot.json`, with **zero** differing key paths on a fully recursive comparison, in 1.65 s each. The `captured_at` key does not exist in the file: it belonged to the pre-v6 flat format, and the v6 envelope dropped the whole `capture` block as unverifiable (`sysml_codegen/snapshot/envelope.py:38-46`). The WI-029 comparison this used to rest on (`work/analysis/20260725-091831_audit_WI-029_handshake-lcoe-construction.md:190`) measured that older format; the migration commit `89f78130` replaced it. The models path does not leak either — v6 records root-relative referents, so the absolute-vs-relative `document_path` hazard WI-027 recorded is gone. Gate 4 therefore compares **whole-file bytes**, with no exclusion.

**There is no teax pin anywhere.** Confirmed by the spec (R-B1.1b) and re-checked: `simkit` exposes no `__version__`, and `verify.py:441` writes `getattr(simkit, "__version__", "unrecorded")`.

## Core Concept

**Integration is a proof, not a transformation.** The seam takes a package that someone claims is the integrated form of some audited model work and proves it, by re-running every producing step in place and requiring each one to change nothing. Regenerate on the pin: zero bytes move. Recapture the snapshot and re-derive the census: they match what is tracked. Recompute the manifest's pin and fingerprints: they match what is recorded. Then run the producers that only ever judged — the spine tests, preflight, verify — against that fixed point. Eight gates, in the spec's order, stopping at the first one that is not a no-op or not a pass. One `CANDIDATE` naming the package, manifest, pin and both fingerprints, or one `BLOCKER` naming the producer, whether it refused or could not run, and where its own output sits.

This shape is not a preference; it is forced, and the derivation is worth stating because the spec's prose reads the other way (see the surfaced conflict below). It is also what makes the seam cheap: it composes producers that all already exist, adds no identity scheme (R-D2, R-F2), and needs no rollback machinery, because on the success path there is nothing to roll back.

The pieces it composes, and what each keeps owning: `tests/test_dependency_provenance.py` owns the pinned-package check; `sysml-codegen generate` owns generation; `sysml_codegen.snapshot.capture` owns snapshot capture; `tests/models/test_model_family_spines.py` owns the canonical tree, the twins and the census; `scripts/study/manifest.py` owns the manifest schema, the two digest recipes and the pin comparison; `scripts/study/identity.py` owns identity recomputation; `preflight.py` owns the six mechanical gates and the refused-versus-could-not-run vocabulary; `verify.py` owns oracle parity and verdict re-derivation; the caller's route module owns baseline execution. The seam owns the order, the stop rule, the two return classes, and the one gate that has no producer — the teax revision comparison (R-B5).

### Surfaced: the spec reads as "perform", the requirements force "prove"

`[AGENT]` R-B1 is written as a list of things the seam does — regenerate, recapture, re-pin. But **SC4** requires the returned candidate to be accepted by the stock preflight route, whose sixth gate `check_package_clean` refuses a package tree that is not git-clean; and **R-F1** forbids the seam from committing. A candidate can therefore exist only when the whole sequence moved zero bytes in the tracked tree. R-C6 says the same thing from the other side: failure is reported, never repaired, and a seam that regenerates to fix a stale package is repairing.

The consequence, stated plainly rather than buried: **the seam refuses model work that has not yet been regenerated and committed.** That work belongs to the modeling item — WI-030 regenerated, recaptured, re-pinned and committed in its own Phases 3–4, *before* audit (`WI-030 plan:146-199`), which is the shape the epic's "audited model work" assumes. The seam is the gate on the hop, not the hand that performs it. If the owner intended the seam to perform the mutations and hand the operator a tree to commit, that is a two-call seam with a human commit between the calls, and R-A2's one-invocation-one-return no longer holds; that is an owner question, not a design call, and it is flagged rather than taken.

## Key Bets

- **B1.** Regeneration on the pin, in place on an already-sealed package, is byte-stable. *If false → gate 2 refuses on every invocation and the seam returns nothing but blockers.* CONFIRMED by spike: zero bytes across two in-place runs, both fingerprints held, 1.8 s (`spike_regen_determinism.md`).
- **B2.** Snapshot recapture from the same models path is byte-identical to the tracked snapshot. CONFIRMED by spike, and stronger than the bet was written: zero bytes and zero key paths differ across three recaptures, 1.65 s each; there is no `captured_at` key to exclude, and the models path does not affect the bytes (`spike_snapshot_stability.md`). The reserved fallback — narrowing to `instance_graph.fingerprint` alone — is not needed and is not carried. One residual: the `authority` block pins the toolchain versions into the file, so gate 4's byte comparison is also a toolchain-lineage check, and gate 1a is what should catch a pin drift first.
- **B3.** By the time model work is audited, its package is regenerated and committed. *If false → the seam's normal return is `BLOCKER` and it is a linter rather than a seam.* Held by WI-030's phase order and by the epic's Item 6 flow (invoke the seam, then run a study).
- **B4.** Executing the manifest's own pinned baseline point produces enough evidence for gates 7 and 8 to judge. *If false → the seam needs a probe set wider than one point, and Open Question 4's boundary gets re-argued.* One completed case carries all six catalog verdicts, which is what `verify_store`'s completeness check demands (`verify.py:388`).
- **B5.** A goal agent can act on `refused` versus `could not run` without further interpretation. *If false → the whole R-A6 distinction is decoration and the retry rule stays a human judgment.*

## Key Decisions

- **D1. One CLI script, `scripts/integrate.py`, is the only entry surface.** A script is callable from an operator shell, from another script, and from an agent's Bash tool, and is the only form testable offline — the sibling's D3 reasoning, unchanged. `[AGENT]`, settling the spec's entry-surface Open Question under orchestrator ruling 2. *Rejected: a slash command or skill* (not callable from code, no deterministic contract). *Rejected: a second operator surface* (ruling 2; R-A4 asks only that a human reach the same seam).
- **D2. Inputs are flags, and every one of them is optional to argparse.** The producers under `scripts/study/` all take flags; a human types the same line the goal agent's Bash tool runs. Required-ness is enforced *in the seam*, not by argparse, so a missing input produces a `BLOCKER` return document rather than a usage error on exit 2 — which is what R-A1 asks for and what makes "every invocation ends in exactly one return class" mechanically true. *Rejected: a request JSON* (a second schema to define and validate for eight scalars).
- **D3. The return is one atomic JSON document, `integration-seam-return/v1`, written into a caller-supplied `--out-dir`, plus a `preflight`-style human summary on stderr.** Written with `common.write_document` (`common.py:96`), so the seam's document has the same atomicity and canonical bytes as every other document in the family and is digestible by one recipe. The seam owns no tracked directory: `--out-dir` is the caller's, every reference inside the return is repo-relative, and the document is self-contained, so a goal trail or a study record cites it wherever the caller keeps it (ADR-006). *Rejected: a fixed home under `exploration/` or `work/`* (the producers name no package and neither may the seam; and a tracked home would make the seam a writer into one of the two PM systems). *Rejected: markdown* (R-A5 wants a test to check it).
- **D4. The blocker taxonomy is `preflight.py`'s, imported.** Every gate result carries `status` from `preflight.PASS` / `FAIL` / `DID_NOT_RUN`, and the blocker's `mode` is `refused` for `fail` and `could_not_run` for `did not run` — one distinction, R-A6's, with the producer-native condition text as its detail. Gates after the stop get a fourth status, `not reached`, so a reader never mistakes a skipped gate for a licence failure. Per-producer detection is in Architecture. *Rejected: typed codes for R-C1–C5 and R-C9* (six codes the caller's retry rule does not read; the producer name plus its own message is the evidence R-B3 wants).
- **D5. The expected teax revision is caller-supplied (`--expected-teax-revision`), and absent means could-not-run.** The seam recording its own expectation would be the seam minting a pin — a new identity scheme R-D2 and R-F2 forbid — and a self-recorded value re-records itself on drift, so it could never refuse. The caller is the one who knows the lineage. *Rejected: a seam-side pin file* (that file is the missing producer R-B5 files as a gap; building it here is the seam growing a producer).
- **D6. The seam executes the manifest's pinned baseline point through a caller-named route, and verifies against that store.** Orchestrator ruling 1. The route is named the way the manifest already names its oracle — a sys-path directory, a module, a callable (`manifest.oracle`, consumed as data by `verify.py:419`) — so the seam stays generic and invokes rather than imports a package. Contract: `callable(out_dir, *, package_dir, manifest_path) -> {"identity": Path, "baseline_result": Path}`, which is `study_route.execute_baseline`'s existing signature. *Rejected: a caller-supplied store* (the seam's verdict would rest on evidence it did not produce, and SC4 wants the stock route). *Rejected: hard-coding `study_route`* (breaks the family's no-package-names invariant for the one tool that sits above all of them).
- **D7. R-C8 is answered by ordering, not rollback — with one bounded restore.** No gate writes a promoting artifact: the identity document, baseline result, store, junit files, producer documents and the return all land under `--out-dir`. The only in-repo writes are the ones the byte-stability gates require to be no-ops. When gate 2 or 4 does move bytes, the seam restores the package tree — `git checkout --` over the resolved package root for tracked modifications, and an explicit `unlink` of exactly the untracked paths `git status --untracked-files=all` names. The restore is exact because gate 0 already required that tree to be clean, so everything that moved is the seam's own. *Rejected: `git clean -fd`* (a hammer that can reach files the seam did not create). *Rejected: copy-the-tree-and-restore-from-the-copy* (a second full copy per invocation to protect a path the entry gate already proved clean).
- **D8. Byte movement is judged by the seam's own content digest, and git-cleanliness stays preflight's.** A per-file sha256 manifest over the package tree before and after each mutating producer, compared exactly (the spike's Step 2 technique). This is what makes the gates real inside a gitignored test workspace, where `git status` reports clean whatever the bytes do. `check_package_clean` is still invoked, unchanged, as preflight's own sixth gate. *Rejected: git status alone* (silently vacuous in the test harness — the failure mode where a green suite proves nothing). *Rejected: mtimes* (the spike measured 95 of 153 files moving mtime on a byte-identical run; any mtime detector reports a false positive on every re-run).
- **D9. The census gate re-derives through the spine test's own helper.** `_by_entry_type` (`test_model_family_spines.py:169`) run against the sealed package, compared to `--census-file`'s `by_entry_type`, `entry_points`, and `derived_against_semantic_fingerprint` versus the package's live semantic fingerprint. WI-030's plan says to run that helper rather than hand-edit (`plan.md:157`). Importing a private helper out of a test module is a smell whose cause is that the census derivation has no importable home; that is filed per R-F5, not fixed here (Integration Strategy). *Rejected: reimplementing the classification* (R-B1's `[HARD]` half). Note the two census checks are different and both are wanted: gate 4 binds the census to the *sealed package*, gate 5 binds it to a *fresh canonical-subset generation*, and the twin-equality test binds the staged tree to the canonical one — together they close the lineage chain.
- **D10. The SC1 fixture is the committed stellarator package as it stands, materialized into a gitignored in-repo workspace.** It is WI-030's audited model change, already integrated, so no new modeling work is minted; its recorded fingerprints are the expected lineage. The workspace has to be *inside* the worktree because `repo_root()`-relative machinery (`repo_relative_posix`, `identity.recompute`'s adapter paths, `git_status_porcelain`) resolves against it, and gitignored so R-G3 holds — no test writes a tracked file. Removed in a `finally`. *Rejected: running the seam against the real tracked package* (the spike proves it is safe and Item 2's F3 finding still says don't). *Rejected: `tmp_path` via the existing `package_copy`* (outside the repo; git errors instead of judging).
- **D11. SC4 needs no hand-off step in the seam.** Gates 7 and 8 *are* the stock preflight and verify invocations, run with the arguments a study runs them with. R-G1a's test reads `integration_return.json` and rebuilds those two command lines from its fields alone, with no seam code in the loop. *Rejected: a `--handoff` step* (machinery for something two gates already do).
- **D12. No lock, no ledger, no retry, no idempotency wrapper.** R-F2 and the epic's hardening rule: nothing enters the first build without a recorded run failure that promotes it.

## Architecture

**One invocation, in order.** Gate 0 is the seam's own precondition sweep (inputs present and resolvable; package resolves to exactly one root and one manifest, else R-C5/R-A3; package tree git-clean, else R-C1). Then the eight gates of R-B1. The seam stops at the first non-pass, restores if it has to, and writes one return.

| # | Gate | Producer, invoked as | `could not run` when | `refused` when |
|---|---|---|---|---|
| 1a | pinned packages | `pytest tests/test_dependency_provenance.py --junitxml` | exit 2/3/4/5, or any `<error>` element | exit 1 with `<failure>` |
| 1b | teax revision | the seam: `git -C $STOP_PARSER_TEAX_ROOT rev-parse HEAD` (R-B5) | env unset/unreadable, or `--expected-teax-revision` absent | revision differs |
| 2 | regeneration | `sysml-codegen generate --smart-regen --preserve-handwritten`, in place | `SYSIDE_LICENSE_KEY` unset, or non-zero exit | exit 0 and any package byte moved (D8) |
| 3 | handwritten preservation | the same digest comparison, scoped to `generated/handwritten/` | gate 2 could not run | any byte under that subtree moved |
| 4 | census / snapshot | `capture_instance_graph_snapshot` to `--out-dir`; `_by_entry_type` on the sealed package (D9) | capture or import raises; `SYSIDE_LICENSE_KEY` unset; `--census-file` absent | recaptured snapshot differs from the tracked one in any byte (B2); census counts, classes, or bound fingerprint differ |
| 5 | model-family spine | `pytest tests/models/test_model_family_spines.py --junitxml` | as 1a (licence failures land as `<error>`) | as 1a |
| 6 | manifest | `manifest.load` → `validate` → `assert_package_identity` → `assert_pin_matches` over the live `indicator_input_fingerprint` | `ManifestError` from `load` (unreadable/not JSON) | `ManifestError` from any of the three assertions |
| 7 | preflight | `preflight.py gates --package --manifest --groups --identity --baseline-result --out` | its own `DID_NOT_RUN` on the stopping gate | its own `FAIL` |
| 8 | verification | `verify.py --package --manifest --identity --store --out` | `simkit` not importable / `STOP_PARSER_TEAX_ROOT` unusable | non-zero exit with a produced summary or a `VerifyError` message |

Baseline execution (D6) sits between gates 6 and 7, because both 7 and 8 read what it deposits and neither can run without it. Its own failure is a `could not run` on gate 7, named as such.

**Refusal is producer-grain, not sub-gate-grain** (R-B4). `preflight gates` reports all six of its checks whatever happened; a blocker from gate 7 names the producer and cites the whole results document, which may carry several failures at once. Gates after the stop are recorded `not reached`.

**Data flow.** In: audited work references (repo-relative path plus commit sha, ADR-006's citation form), models root, package root, manifest, axis declaration, census file, expected lineage (semantic and executable fingerprints, teax revision), route triple, out-dir. Out, under `--out-dir`: `integration_return.json`, `package_identity.json`, `baseline_result.json`, `_work/<baseline>.db`, `preflight_results.json`, `verification_summary.json`, `recaptured.snapshot.json`, `junit/*.xml`, and on a byte-movement refusal `moved_files.txt`. In the tracked tree: nothing, ever.

**The lineage check (R-C9)** is a comparison, not a gate the producers own: after gate 8 passes, the package's live semantic and executable fingerprints are compared to the request's expected lineage. A mismatch is a `BLOCKER` naming expected and actual. It is last because a package that fails a gate has no lineage worth reporting.

**Return shape** (R-A2, R-A5, R-E2, R-E3):

```jsonc
{"schema_version":"integration-seam-return/v1","tool":{"path","source_digest"},"command":[],
 "request":{"audited_work":[{"path","commit"}],"models_root","package","manifest","groups",
            "census","expected":{"semantic_fingerprint","executable_fingerprint","teax_revision"}},
 "class":"CANDIDATE|BLOCKER",
 "candidate":{"package","manifest","pin","semantic_fingerprint","executable_fingerprint",
              "identity_document","baseline_result","verification_summary"},   // or null
 "blocker":{"gate","producer","mode":"refused|could_not_run","detail","evidence":[]}, // or null
 "gates":[{"gate","producer","status","checked","detail","evidence":[]}],
 "toolchain":{"agentic_mbse","sysml_codegen","costingfe","teax_revision","teax_module_path"}}
```

`pin` is the manifest's `fingerprints.indicator_inputs.digest` — the value `assert_pin_matches` compares, not a new number.

## Required Invariants

- No tracked file's bytes differ before and after an invocation, whatever its return class.
- Every one of the eight gates appears in the return with a status. `CANDIDATE` exists only when all eight are `pass` and the lineage comparison agrees.
- A `BLOCKER` names exactly one producer — the first non-pass in R-B1 order — with `mode` set from that producer's own status vocabulary. Every later gate is `not reached`, never `could not run`.
- Every path, digest and identity in the return resolves to a repo path, a commit, or a file under `--out-dir` (R-E3).
- No gate is skipped because a prior run passed it (R-B4), and no gate runs after an earlier one refused.
- Nothing under `scripts/study/`, `tests/models/`, or `tests/test_dependency_provenance.py` is edited (R-B2): `git diff --stat` over those paths is empty at close.
- A re-run on unchanged inputs returns the same `candidate` block byte-for-byte, modulo `command` and paths under `--out-dir` (R-D1).

## Component Overview

- **`scripts/integrate.py`** — the seam. Argument handling and input validation, the eight-gate sequence with its stop rule, the package content-digest helper and the bounded restore, per-producer status detection, the lineage comparison, the return document and the human summary. Imports `preflight`, `manifest`, `identity`, `common` for constants, digests and document writing; invokes `pytest`, `sysml-codegen`, `preflight.py` and `verify.py` as subprocesses so each producer's own exit code and output document are the evidence.
- **`tests/study/conftest.py` (extended)** — one new fixture, `integration_workspace`: materializes package, models, manifest, axes and census into a gitignored in-repo directory, rewrites `package.path` to its repo-relative form the way `package_copy` does (`:207`), and removes it in a `finally`. It lives here to reuse the teax and licence skip machinery (`:239-270`) rather than duplicate it; it is test infrastructure, not a gate producer, so R-B2 is untouched.
- **`tests/study/test_integrate_*.py`** — the five shapes in Validation Approach.
- **`docs/integration_seam_operator_guide.md`** — R-E1/SC6: assembling a request, invoking the seam, reading `CANDIDATE` versus `BLOCKER`, citing a candidate in a study, and acting on each blocker mode. States the surfaced boundary above in the operator's words: the seam refuses work that has not been regenerated and committed, and what to do about it.
- **`.gitignore`** — the workspace root.

## Non-Goals

- Performing the integration. The seam proves a package is the integrated form; regenerating, recapturing and re-pinning stay in the modeling item that made the change (surfaced above; R-C6).
- An `--apply` mode that leaves mutations in place for an operator to commit. It is the two-call shape the surfaced conflict describes, and it is an owner question.
- Committing, pushing, closing modeling work, or choosing among model designs (R-F1).
- A goal-side effects ledger, idempotency wrapper, or second verification implementation (R-F2).
- Fixing the calc-then-compare parser limitation, or `verify.py`'s `teax.revision: "unrecorded"`. Both stay filed against their own homes (R-F4, R-F5).
- Running or interpreting a study. Baseline execution is a gate's own input, not a study (Non-Goals boundary note; ruling 1).

## Implementation Notes

- **The baseline store path is not returned by `execute_baseline`.** Resolve it from `baseline_result.executed_under.store_id`, which is repo-relative when `--out-dir` is under the repo root and a bare filename otherwise; fall back to `<out-dir>/_work/<name>`.
- **The package root is a symlink** (`pkg/stellarator_tea` → `../generated`). Resolve before digesting, before `git checkout --`, and before comparing paths.
- **Never build mtime-based change detection.** 95 of 153 files move mtime on a byte-identical regeneration (spike Step 4).
- **`--junitxml` is what separates `<error>` from `<failure>`.** Parsing pytest's terminal output for that distinction is not reliable enough to carry R-A6.
- **`SYSIDE_LICENSE_KEY` is checked before invoking generate or the spine tests**, so the could-not-run condition is named by the seam rather than inferred from a stack trace.
- **The seam names no package and no key prefix**, matching every module it sits above (`preflight.py:44`, `manifest.py:16`, `identity.py:29`).
- **Reuse `common.write_document`, `common.tool_source_digest`, `manifest.sha256_file`, `manifest.repo_relative_posix`.** One recipe id must mean one algorithm (`common.py:50-52`).

## Potential Risks

- **B2 measured and closed.** Snapshot recapture is byte-identical to the tracked file (`spike_snapshot_stability.md`); gate 4 compares whole-file bytes and the weaker `instance_graph.fingerprint` fallback is dropped. What remains is that the snapshot's `authority` block pins the toolchain, so a version bump moves the bytes and refuses gate 4 — correct behavior, but a refusal there reads as model drift unless the return names the cause.
- **The gitignored workspace makes `check_package_clean` vacuous in tests.** D8's own digest is what keeps the byte gates real there; the risk is that a future edit removes the digest comparison believing git covers it. The invariant is stated and one test asserts movement is caught inside the workspace.
- **Wall clock.** Two pytest suites, a generation, a snapshot capture and a baseline execution per invocation. Generation is 1.8 s; the spine suite and the baseline run dominate. Acceptable for a hop that happens once per model change, and a reason not to call the seam in a loop.
- **The restore path is exercised rarely and matters most.** It is covered by its own test (a deliberately stale package), not left to the success path.
- **A `--census-file` that is absent silently weakens nothing** — it is a could-not-run blocker, by design — but an operator who does not know to pass it will read the seam as broken. The guide leads with the full invocation.

## Integration Strategy

The seam sits above `scripts/study/` and beside it, invoking the same command lines the referent plans typed by hand (`WI-030 plan:213-217`, `migration plan:289-290`). Item 6 becomes its first goal-side consumer: invoke, accept one candidate pin, run a study against it. Nothing about the study route changes.

Two gap filings during implementation (R-F5, R-F3), as BACKLOG rows against their existing homes: the census derivation has no importable home outside a test module (D9), and fusion-tea has no automated teax revision pin — home `tests/test_dependency_provenance.py` (R-B5). The open `verify.py` `teax.revision: "unrecorded"` row (`DISCOVERY_LOG.md 20260821-power-cycle-ab#8`) is cited as still open and explicitly not discharged by the seam recording the revision (R-E4).

## Validation Approach

New tests under `tests/study/`, reusing that suite's teax and licence machinery. All five run inside `integration_workspace`; none writes a tracked file (R-G3).

| Requirement | Test | Shape |
|---|---|---|
| SC1, R-A2, R-E3 | `test_integrate_success.py` | the committed package through all eight gates → `CANDIDATE`; every field resolves; both fingerprints equal the request's expected lineage; the tracked tree is byte-identical before and after |
| SC2, R-G4, R-A6 | `test_integrate_refusals.py` | four real refusals from real producers — a stale census (gate 5 refuses, "model meaning moved"), a manifest with a drifted `recorded_provenance` (gate 7 refuses), a wrong `--expected-teax-revision` (gate 1b refuses), a package byte edited so regeneration moves it back (gate 2 refuses **and** the tree is restored). Each names its producer, cites its own output, and carries `mode: refused`; later gates read `not reached`; no candidate |
| R-A6 could-not-run | same file | `SYSIDE_LICENSE_KEY` unset → gate 2 `could_not_run` with the condition named, not `refused`; a missing required input → `BLOCKER`, not a usage error |
| SC3, R-D1, R-D3 | `test_integrate_rerun.py` | two invocations, same inputs → identical `candidate` blocks; the second names the same identity, never a second one |
| SC4, R-G1a | `test_integrate_stock_route.py` | rebuild the `preflight.py gates` and `verify.py` command lines from `integration_return.json`'s fields alone, run them as a study would, both pass, no seam import |
| R-C9 | `test_integrate_lineage.py` | a request whose expected fingerprints are a digit off → `BLOCKER` naming expected and actual, after all eight gates passed |
| R-G2, R-B2 | regression | `pytest tests/models tests/study tests/test_dependency_provenance.py` green; `git diff --stat -- scripts/study/ tests/models/ tests/test_dependency_provenance.py` empty |

SC6 is verified at `/_my_audit` by a fresh session that did not build the seam, walking `docs/integration_seam_operator_guide.md` and recording every point where it had to read source or guess — the evidence form the spec fixes (SC6 Evidence form), learned from Item 2's audit.

**Effort.** The epic estimates 8 h to execute; this design is closer to **12 h**, and the driver is the harness, not the seam. `scripts/integrate.py` is roughly a day's smaller half — the eight gates are subprocess calls with one status rule each. The other half is `integration_workspace` (a git-meaningful, gitignored, in-repo materialization of package plus models plus four documents, with teax and licence preconditions), the four real-refusal fixtures, and the operator guide. Thinning any of those hits R-G3, R-G4 or SC6 directly, so the estimate is reported rather than absorbed.

## Next-Stage Handoff

- **Fixed:** the prove-don't-perform shape and its derivation; one CLI, flags-optional, one JSON return; `preflight`'s status vocabulary imported; the per-producer detection table; caller-supplied teax revision; caller-named baseline route; seam-owned content digests plus the bounded restore; the gitignored in-repo workspace.
- **Open for the plan:** exact flag spellings and return field names; the workspace directory's name and `.gitignore` line; the wording of the operator guide; whether the four refusal fixtures share one workspace or take one each.
- **B2 is done, no de-risking left.** The snapshot comparison was measured (`spike_snapshot_stability.md`): recapture is byte-identical to the tracked file, so gate 4 is written as a whole-file byte comparison. Gate 4's `could not run` set gains `SYSIDE_LICENSE_KEY` unset, which capture needs and generate needs too.

---

## Appendix A — ADR candidate

To file after approval, per `.project/adr/README.md`, in Item 1's home.

**Title:** Integration is a fixed-point proof, not a transformation.
**Grade:** `[AGENT]`, delegated by the owner at Align (`align.md:8`, "just get it done — you are responsible for quality and alignment").
**Context:** The integration hop's producers include mutating steps (regenerate, recapture, re-pin). The stock preflight route refuses a package tree that is not git-clean, and the seam may not commit.
**Decision:** The seam invokes every producing step in place and requires each to change nothing; a candidate exists only for a package that is already a fixed point of the whole sequence. Byte movement is a `BLOCKER` naming the producer, with the tree restored.
**Consequences:** no rollback machinery and no new identity scheme; the seam refuses model work not yet regenerated and committed, which stays the modeling item's job; the return is safe to call twice; a two-call perform-then-gate seam would need an owner ruling because it breaks one-invocation-one-return.
**Rejected:** the seam performing the mutations and leaving a dirty tree for the operator to commit (no invocation can then return a candidate); the seam committing (R-F1).

---

**Next Step:** After approval → `/_my_plan`.
