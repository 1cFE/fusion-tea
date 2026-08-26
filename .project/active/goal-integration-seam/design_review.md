# Design Review: Verified Package Integration Seam (GSTH Item 3)

**Design:** `.project/active/goal-integration-seam/design.md` (commit `5c2f73d5`)
**Spec:** `.project/active/goal-integration-seam/spec.md` (revised through spec review)
**Review File:** `.project/active/goal-integration-seam/design_review.md`
**Date:** 2026-08-26
**Reviewer:** fresh stage session; did not author the design. Every code claim below was run or read in this worktree.

---

## The Point

Integration is the hop between an audited model change and a study that can run against it. Every gate the hop needs already exists and already fails closed — the toolchain pin test, `sysml-codegen generate`, the model-family spine suite, `manifest.py`, `preflight.py gates`, `verify.py`, `identity.py`. What does not exist is a boundary that owns them together. The sequence lives in two work-item plans and a pile of shell commands, so a goal task cannot request integration without reconstructing the hand pattern. The cost has been paid once: Item 6 opened with eleven red tests because a scaffold commit added an objective to the manifest without re-pinning the fixtures. The check existed; nothing bound it to the hop, so it fired far from the commit that broke it.

The obligation: turn audited model work into exactly one verified, study-ready candidate pin and fingerprint, or a named blocker. Two things make the return usable rather than merely correct. A goal agent reading a `BLOCKER` must be able to tell an operational accident it may retry from a semantic result that changes what work is justified. And a person who did not build the seam must be able to operate the whole thing from its own documentation.

---

## Fundamental Assessment

**Sound, with one structural crack.**

The right piece of work, and the right approach. The prove-don't-perform derivation is correct and honestly argued: `SC4` requires the stock preflight route to accept the candidate, `check_package_clean` refuses a non-git-clean tree (`preflight.py:300`), and `R-F1` forbids committing — so a candidate can only exist for a package that is already a fixed point of the whole sequence. That is forced, not chosen, and the design says so plainly instead of burying it. The orchestrator's ruling is honored, the derivation holds, and the consequence ("the seam refuses model work not yet regenerated and committed") is stated in the open rather than discovered at implement. The rejected-alternative discipline across D1–D12 is real — every rejection names a specific cost, not a vibe.

The crack is in the genericity claim. The design says twice that "the seam names no package," matching every module it sits above. That is true for seven of the nine gate rows and false for gate 5. `pytest tests/models/test_model_family_spines.py` takes no package argument: it generates from the repo's canonical `models/` tree through `materialize_canonical_subset` (`:216`) and compares against the tracked `tests/models/data/mfe_census.json` (`:353`). It judges the repository, not `--package`. Inside the gitignored `integration_workspace` it judges the real repo while every other gate judges the workspace. That is not a detail the plan can settle — it changes what gate 5 means and it breaks one of the five named test fixtures.

That is a **Revise**, not a Rework. The shape survives; three gates need their detection and scoping restated, and the return needs two fields it does not have.

**Product-lens.** `~/.claude/scripts/product-lens.md` is unreadable from this worktree (it resolves outside the allowed working directory; non-interactive, so no grant was possible) — the same limitation the Item 2 and the spec-hop ledgers record. The lens was therefore run inline against the design and the durable product statements (`.project/adr/006-goal-evidence-seam.md`, `003-lean-first-persistence.md`, the epic, the concept-design), and the block is appended to `product-lens.md` in the §3 format the existing blocks evidence. Verdict: **BLOCKED on M1 and M7** — the seam's genericity claim does not hold at gate 5, and the return cannot carry the `PREREQUISITE` class the accepted ruling makes the seam's most common outcome.

**The two design-level smells.**

- **A consumer compensating for a producer or platform guarantee — FIRES, twice.** Gate 5's producer is not parameterizable by package, and gate 8's producer collapses refusal and could-not-run into one exit code with no document. In both cases the seam absorbs the shortfall silently. Escalated into M1 and M4 rather than left in the rubric; both need an R-F5 filing against the producer's own home, which the design's Integration Strategy currently lists only two of.
- **Ownership change without saying so — does not fire.** R-B2 is honored: `scripts/study/`, `tests/models/` and `tests/test_dependency_provenance.py` are untouched, and the one file the design does extend (`tests/study/conftest.py`) is test infrastructure, not a gate producer. The design says so and states the empty-diff invariant.

---

## Dimensional Review

### 1. Spec Compliance
**Assessment:** Concerns

Coverage is close to complete. Walking R-A1 → R-G4: A1/A2 land in D2 and the return schema; A3 in gate 0; A4/A5 in D1/D3; A6 in D4 and the detection table; B1 in the Architecture table; B2 in the Required Invariants; B3 in D3 (cite by path, ADR-006); B4 in the stop rule and the `not reached` status; B5 in gate 1b and D5; C1–C5 across gate 0, gate 6 and gate 7; C6 in Non-Goals; C7 by construction (the seam writes only under `--out-dir`); C8 in D7; C9 in the lineage comparison; D1–D4 in the invariants and B1; E1–E4 in D3 and the schema's `toolchain` block; F1–F5 in Non-Goals and Integration Strategy; G1–G4 in the Validation table. SC1–SC6 each have a named test or a named evidence form.

Three gaps.

- **`assert_read_set_covered` is dropped without a word** (M5). R-B1.6 enumerates four manifest assertions; the design's gate 6 runs three. The omission is defensible — its only caller is `scripts/study/indicators.py:808` and it needs the reader's resolved paths, which the seam does not have — but the design records neither the omission nor where the obligation goes. Nothing downstream covers it: preflight's six gates do not, and `verify.build_summary` does not call it.
- **Gate 5 does not check the package the request names** (M1). SC1 says the returned candidate must "match the package it names"; gate 5 contributes nothing to that.
- **The lineage blocker has no schema home** (M6). R-A2 requires a blocker to name expected versus actual lineage, and R-A5 requires the return to be checkable by a test. The `blocker` object has `gate`, `producer`, `mode`, `detail`, `evidence` — and the design says outright that the lineage check "is not a gate the producers own," so it has neither a gate nor a producer.

**Capture fidelity.** Provenance is carried faithfully. `[INHERITED: epic Item 3 Objective, agent decomposition ratified by owner 2026-08-25]` on The Point is the correct grade and correctly marks the ratification rather than promoting it to owner-originated. No `[INFERRED]` spec item is silently hardened into a fixed constraint; R-B1's per-edge ordering grade is respected (the design follows the order without claiming it as physics). The one owner-given referent chain — the three referent plans — survives by path at the spec's emphasis. The § Surfaced section is a correct Law 4 surfacing: it states the conflict, parks the dependent conclusion as an owner question, and does not resolve it in either direction.

### 2. Pattern Consistency
**Assessment:** Pass

This is the design's strongest dimension. It reuses `preflight.py`'s status vocabulary as imported constants rather than re-spelling them (`PASS`/`FAIL`/`DID_NOT_RUN`, `preflight.py:85-87` — confirmed), `common.write_document` for atomicity and canonical bytes (`common.py:96` — confirmed atomic via `mkstemp` + `os.replace`), `common.tool_source_digest`, `manifest.sha256_file`, `manifest.repo_relative_posix`. The return document's shape (`schema_version`, `tool: {path, source_digest}`, `command`) is the family's own shape, matching `verify.py:441` and `preflight.py`'s results document. The `unavailable()`-style named-condition pattern is matched rather than reinvented. D6's route-as-data contract mirrors how `manifest.oracle` is already consumed (`verify.py:419`).

Cite accuracy is high. Spot-checked and correct: `preflight.py:233` `check_manifest_currency`, `:300` `check_package_clean`, `:333` `run_gates`, `:368` `unavailable`; `verify.py:343` `verify_store`, `:388` the missing-verdict check, `:414` `build_summary`; `common.py:60` `git_status_porcelain`; `identity.py:288` `assert_matches`; `study_route.py:358` `execute_baseline` and `:381` `store_id`; `test_model_family_spines.py:114`, `:169`, `:243`, `:308`, `:317`, `:349`; `conftest.py:191`, `:207`, `:239-270`, `:274`. One drift: `assert_pin_matches` is `manifest.py:453`, not `:451` (A10).

One missed reuse: `preflight.py` has a `clean` subcommand (`:488`) that is exactly gate 0's git-clean check. The design implements gate 0's clean check itself and never mentions the subcommand (A9).

### 3. Abstraction Quality
**Assessment:** Pass

One script, one JSON return, one fixture, no new class hierarchy. Every abstraction earns its place by removal test: strip the content-digest helper and the byte gates go vacuous inside the workspace; strip the workspace and the tests write into a tracked package; strip the return document and there is nothing for Item 6 to cite. The seam owns exactly four things — the order, the stop rule, the two return classes, and the one gate with no producer — and the design names them explicitly. That list is the right size.

D12's refusal to build a lock, a ledger, a retry or an idempotency wrapper is correct and matches R-F2 and the epic's hardening rule. No hardening machinery is smuggled in. D7's bounded restore is not hardening — R-C8 asks for it and the design chooses the narrowest form — but see M3 on whether the chosen form works where it is tested.

### 4. Duplication Avoidance
**Assessment:** Pass

D8's second change-detector alongside git is the one place duplication could be argued, and the design defends it correctly: `git_status_porcelain` runs from `manifest.repo_root()` with a resolved pathspec (`common.py:60-73` — confirmed), so a gitignored workspace reports clean whatever its bytes do. The two detectors are complementary, and the design says which failure mode each covers. D8's rejection of mtimes is backed by the spike's measurement (95 of 153 files move mtime on a byte-identical run), which is exactly the kind of duplication-that-would-drift the dimension exists to catch.

### 5. Data Structure Clarity
**Assessment:** Concerns

The return schema is legible and mostly sufficient. `gates[]` carries `{gate, producer, status, checked, detail, evidence}` — enough for R-E2 (which gates ran, what each returned, where the output sits) and R-E3 (every reference is a repo path, a commit, or a file under `--out-dir`). `candidate` carries all six things R-A2 names. `toolchain` covers R-E4.

What is missing or ambiguous:

- No home for the lineage blocker's expected-versus-actual (M6).
- No process exit code contract (A2). The primary caller is an agent's Bash tool, which reads the exit code before it reads anything else. `CANDIDATE` → 0, `BLOCKER` → what, and is an internal crash distinguishable from a blocker? The plan will have to invent this.
- The R-D1 invariant is self-contradictory as phrased (A8): "the same `candidate` block byte-for-byte, modulo `command` and paths under `--out-dir`" — but three of the eight `candidate` fields (`identity_document`, `baseline_result`, `verification_summary`) *are* paths under `--out-dir`. What is actually invariant is the pin, both fingerprints, the package and the manifest. Say that.
- "Eight gates" versus nine rows (A1). The Required Invariants say every one of the eight gates appears with a status; the table has nine (1a and 1b are separate producers with separate detection). Harmless but the plan has to pick one, and the invariant is meant to be mechanically checkable.

### 6. Route Safety
**Assessment:** Concerns

Read here as "are the seam's invocation paths explicit and non-vacuous," since there are no HTTP routes.

- **D6's caller-named route is safe and well-shaped.** The contract `callable(out_dir, *, package_dir, manifest_path) -> {"identity": Path, "baseline_result": Path}` matches `execute_baseline`'s actual signature exactly (`study_route.py:358-399` — confirmed, including that the store path is *not* returned and must come from `baseline_result.executed_under.store_id`). Naming it the way `manifest.oracle` is already named keeps the no-package-names invariant. Rejecting a caller-supplied store is right: the seam's verdict must not rest on evidence it did not produce.
- **The subprocess environment is undefined** (M8). The design invokes `verify.py` as a subprocess "so each producer's own exit code and output document are the evidence" — but `verify.py` imports `simkit` inside `build_summary` (`:415`) and does no `sys.path` work of its own. Every existing invocation gets teax from `tests/study/conftest.py`'s in-process insertion or from a hand-exported path; WI-030's plan records exactly this trap (`plan.md:304`). The plan will have to invent the environment the seam hands its subprocesses.
- **`--census-file` is a flag with no effect on gate 5** (part of M1). An operator who passes it will reasonably believe it scoped the census check. It scopes gate 4 only.

### 7. Bets & Decisions Integrity
**Assessment:** Concerns

B1 is genuine and CONFIRMED by the spike. B2 is genuine, honestly marked as resting on one recorded comparison rather than a measurement, and is being measured by the parallel spike — **noted as pending, not re-argued**. B3 and B5 are real claims about reality with honest "if false" consequences.

B4 is understated rather than wrong. It is presented as a bet, but the evidence already exists and the design did not find it: WI-030 ran `verify.py` against the **baseline** store — not the availability sweep — and got `outcome: pass`, `not_independently_verified: []`, six verdicts re-derived, `beta` among the compared channels (`WI-030 plan:203`). That is B4, measured. Cite it and downgrade (A3).

**Hidden bets, hunted.**

- **Gate 4's census comparison against the sealed package.** The design compares `_by_entry_type` over the sealed package to a census file derived from a *fresh canonical-subset generation*. Those are different trees; nothing in the design says why they should agree. Checked: they do — `mfe_census.json` records `entry_points: 173` and `derived_against_semantic_fingerprint: 1ca93d0c…`, which is the sealed stellarator package's own semantic fingerprint and its 173-parameter count. So the bet holds today. But it is load-bearing, unstated, and it is exactly the thing that breaks when a second package enters the picture. State it.
- **Gate 5 judges the repo, not the request** (M1). This is the unstated bet that costs the most: the design assumes gate 5 is package-scoped like its neighbours, and it is not.
- **Gate 1a passes in the environment the seam will actually run in** (M2). It does not, today, and the repo's own records say so.

**Decisions.** D1–D12 each name a rejected alternative with a stated cost, and the rejections are honest rather than strawmen — D8's "git status alone is silently vacuous in the test harness," D7's "`git clean -fd` is a hammer that can reach files the seam did not create," D5's "a self-recorded value re-records itself on drift, so it could never refuse." That last one is the sharpest argument in the document. D4's rejection of typed codes is the right call for the same reason: six codes the caller's retry rule does not read are six codes that drift.

One decision is under-derived: **D4's two modes are not the caller's three** (M7). The concept-design's return vocabulary has `PREREQUISITE`, `STRATEGY_BLOCKER` and `MECHANICAL_FAILURE`, and only `PREREQUISITE` both ends the task and preserves strategy so another scoped task may follow. Prove-don't-perform makes "this package has not been regenerated and committed yet" the seam's most common blocker — and that is a textbook `PREREQUISITE`. Under D4 it arrives as `refused`, the mode that closes the round. This is a consequence of the accepted ruling, not a challenge to it.

### 8. Reader Comprehension
**Assessment:** Pass

A tired engineer can read this once and know what the seam is. "Integration is a proof, not a transformation" is the right one-line mental model and it arrives before any mechanism. The § Surfaced section states the conflict, the consequence in plain words ("the seam refuses model work that has not yet been regenerated and committed"), and the owner question, in that order. The gate table is the right form for nine heterogeneous producers. Research Findings leads each paragraph with a plain claim and puts the cite at the end.

Two comprehension nits worth fixing because they mislead rather than merely read awkwardly: the repeated "the seam names no package" (false at gate 5), and "eight gates" against a nine-row table.

---

## Issues by Severity

### Must-fix (blocks plan)

- **M1 · Gate 5 does not judge the package under test — and its refusal fixture cannot be built hermetically.** `pytest tests/models/test_model_family_spines.py` takes no package argument. Its `baselines` fixture generates each family from the repo's canonical `models/` tree via `materialize_canonical_subset` (`:216`, `:243`), and the MFE census test compares against the tracked `tests/models/data/mfe_census.json` (`DATA / "mfe_census.json"`, `:353`). So gate 5 says nothing about `--package`, `--models-root`, or `--census-file`; inside the gitignored `integration_workspace` it judges the real repo while every other gate judges the workspace. Two consequences: the "names no package" invariant is false in the opposite direction (gate 5 is hard-wired to one tree), and the Validation table's first refusal fixture — "a stale census (gate 5 refuses, 'model meaning moved')" — can only be driven by editing the tracked census file, which R-G3 forbids. **Resolution:** state what gate 5 actually binds (the repo's canonical tree and its tracked census, i.e. the lineage chain's other end, which D9's note half-recognises), stop implying it is package-scoped, and either move the census refusal fixture to gate 4 (which *is* package-scoped) or say how gate 5's refusal is driven without writing a tracked file. File the "the spine suite is not parameterizable by package" gap per R-F5 alongside the two already listed.

- **M2 · Gate 1a misclassifies its most likely failure, and the success path cannot run today.** `test_installed_artifacts_are_the_recorded_wheels_and_public_apis` reads `os.environ["STOP_PARSER_WHEEL_TARGET"]` and three wheel-path variables *in the test body* (`tests/test_dependency_provenance.py:83-87`). Unset → `KeyError` → pytest records a `<failure>`, exit 1. Under the design's table that is `refused`. It is a could-not-run. This is the repo's documented standing state, not a hypothetical: `WI-030 verification_record.md:54`, `goal-research-seam/audit.md:62`, and `goal-research-seam/plan.md:589` all record the same `KeyError` as a pre-existing environmental failure. As designed, the seam returns `BLOCKER / gate 1a / refused` on every invocation in a default environment and SC1 can never produce a `CANDIDATE`. **Resolution:** add the four wheel-path variables to the pre-checked could-not-run preconditions beside `SYSIDE_LICENSE_KEY`, and retire the Implementation Note's claim that `--junitxml`'s `<error>`/`<failure>` split carries R-A6 on its own — it does not, for this producer.

- **M3 · D7's bounded restore cannot execute inside D10's workspace.** D7 restores with `git checkout --` over the resolved package root plus an explicit `unlink` of the paths `git status --untracked-files=all` names. D10 puts that package in a **gitignored** directory. `git status --untracked-files=all` does not report ignored paths, and `git checkout -- <ignored path>` matches no pathspec — so the restore is a silent no-op exactly where it is tested. The Validation table's fourth refusal asserts "gate 2 refuses **and** the tree is restored" inside `integration_workspace`, and that assertion cannot pass on its merits. The design already makes this argument for *detection* (D8's digest is what keeps the byte gates real in a gitignored tree) and does not carry it to *restore*. **Resolution:** either make the restore digest-driven from a pre-gate content snapshot (which means keeping the content D7 rejected keeping — say so and bound the cost), or give the workspace its own git repo the way the spike's Step 2 probe did, or state that the restore path is proven outside the workspace and how.

- **M4 · Gate 8's refused-versus-could-not-run detection describes a state that never occurs.** `verify.py main` catches `common.ToolError` and `manifest_mod.ManifestError` and returns 1 (`:526-529`); `VerifyError` is a `ToolError` subclass (`:80`). So a parity refusal, an empty store, an unreadable manifest and a failed `import simkit` (inside `build_summary`, `:415`) all exit 1 — and on every one of them `common.write_document` is never reached, so **no summary is written**. The design's rule, "non-zero exit with a produced summary or a `VerifyError` message," has no reachable first branch and an unspecified second. The only available discriminator is stderr text. **Resolution:** name the strings, or accept that gate 8 has one mode and say which, and file the "verify.py collapses two R-A6 modes into one exit code" gap against `scripts/study/verify.py` per R-F5.

- **M5 · `assert_read_set_covered` is dropped from gate 6 with no note.** R-B1.6 enumerates four assertions; the design runs three. Nothing else covers it — its only caller is `scripts/study/indicators.py:808`, which needs the reader's resolved paths. The omission is probably correct; the silence is not. One line: covered here, covered elsewhere, or out of reach and why.

- **M6 · The return schema has no home for the R-C9 lineage blocker.** `blocker` is `{gate, producer, mode, detail, evidence}`, and the design says the lineage comparison "is not a gate the producers own" — so it has neither a `gate` nor a `producer`. R-A2 requires that blocker to name expected versus actual lineage, and R-A5 requires the return to be checkable by a test; `test_integrate_lineage.py` in the Validation table has nothing structured to assert against. **Resolution:** add `blocker.expected` / `blocker.actual`, or a distinct `lineage` block, and say what `gate` and `producer` carry when the seam itself is the judge (the same question gate 1b raises and the design does answer there).

- **M7 · Prove-don't-perform's own consequence does not reach the return, so Item 6 will act on it wrongly.** The design correctly derives that the seam refuses model work not yet regenerated and committed, and correctly flags the two-call alternative as an owner question. But in the concept-design's return vocabulary that refusal is a `PREREQUISITE`: it ends the task, preserves strategy and comparison meaning, and another scoped task may follow. The design's two modes are `refused` and `could_not_run`, and `refused` is the one that maps to `STRATEGY_BLOCKER` and closes the round. So the accepted ruling's single most common outcome arrives at Item 6 wearing the label that stops the goal. **Resolution:** not a third mode necessarily — but the return contract and the operator guide must say how a `refused` on gates 2/3/4 maps to `PREREQUISITE` rather than `STRATEGY_BLOCKER`, and a test should pin it. This is the ruling's consequence, reviewed as the brief asks, not a re-litigation.

- **M8 · The subprocess environment is undefined.** The seam invokes `verify.py` as a subprocess, but `verify.py` does no `sys.path` work and imports `simkit` from wherever the environment provides it. Existing invocations get it from `tests/study/conftest.py`'s in-process insertion or a hand-exported path; WI-030 recorded the trap explicitly (`plan.md:304`). Say what environment the seam hands each subprocess — at minimum `PYTHONPATH` including `$STOP_PARSER_TEAX_ROOT/packages/teax-simkit`, and whether `SYSIDE_LICENSE_KEY` and `STUDY_REQUIRE_TEAX` are passed through or asserted.

### Advisory

- **A1 · "Eight gates" versus nine rows.** The Required Invariants make a mechanically checkable claim about eight; the table has nine. Pick one.
- **A2 · No process exit-code contract.** The primary caller is an agent's Bash tool. State `CANDIDATE` → 0, `BLOCKER` → N, and whether an internal crash is distinguishable from a blocker.
- **A3 · B4 is already measured.** WI-030 ran `verify.py` against the baseline store: `outcome: pass`, `not_independently_verified: []`, six verdicts re-derived (`WI-030 plan:203`). Downgrade from bet to recorded evidence and cite it.
- **A4 · Gate 6's `load → validate` is redundant.** `manifest.load` calls `validate` before returning (`manifest.py:398`).
- **A5 · `_by_entry_type` returns sets; the census file stores sorted lists.** The producer's own test normalizes with `{k: sorted(v) …}` (`:358`). Say so, or the plan re-derives it from a failing assertion.
- **A6 · Teax revision form is unspecified.** `git rev-parse HEAD` yields 40 chars; the only recorded expected value is short (`744745f`, migration plan `:47`). Say which form the caller supplies and whether a prefix match is legal. A fail-closed gate that can never match is worse than one that refuses.
- **A7 · The request surface is much wider than the seam contract the concept-design promises.** The `integrate` row's invoke-with is "audited item(s), expected lineage." The design needs models root, package, manifest, groups, census, route triple, expected teax revision and out-dir. Nothing says where a goal agent gets them. One line in the operator guide, or a caller-owned request preset (owned by the caller, not the seam — a seam-side preset would name a package).
- **A8 · The R-D1 invariant contradicts itself.** Three of eight `candidate` fields are paths under `--out-dir`, which the invariant excludes. State the real invariant: same pin, both fingerprints, same package and manifest.
- **A9 · `preflight.py clean` exists (`:488`) and gate 0 reimplements it.** Using it keeps invoke-don't-reimplement honest at the entry gate too.
- **A10 · Cite drift:** `assert_pin_matches` is `manifest.py:453`, not `:451`.
- **A11 · The estimate will move again.** 12h versus the epic's 8h is honestly reported and correctly refuses to absorb the difference. M1 and M3 add to it; restate at plan rather than at implement.
- **A12 · The conftest extension needs a no-regression assertion.** `tests/study/conftest.py` is not a producer and R-B2 does not name it, so extending it is legal — but 262 existing tests depend on that file. Add "existing `tests/study` fixtures unchanged in behaviour" to the Required Invariants alongside the `git diff --stat` check.

### Noted, not a finding

- **B2 is pending a parallel spike** and is not re-argued here. The design's fallback (narrow gate 4's comparison to `instance_graph.fingerprint`, recorded as weaker if taken) is the right shape.
- **No hardening machinery is smuggled in.** D12 is explicit, and nothing elsewhere contradicts it. D7's restore is R-C8's answer, not hardening.
- **No producer edit against R-B2.** `scripts/study/`, `tests/models/` and `tests/test_dependency_provenance.py` are read and invoked only.

---

## Recommendations

1. **Fix gate 5 first (M1).** It is the one finding that changes what a gate means rather than how it is detected, and it invalidates a named test fixture. Everything else is local.
2. **Make the R-A6 detection table survive contact with the real environment (M2, M4, M8).** Three of the nine rows classify by a signal the producer does not actually emit. Rewrite the table with the precondition checks the seam performs *before* invoking, and reserve the exit-code/junit rules for what they genuinely discriminate.
3. **Reconcile D7 with D10 (M3).** They are individually well-argued and jointly inoperative. The spike's own Step 2 technique — give the scratch tree its own git repo — is the cheapest reconciliation and is already proven in this item.
4. **Close the return schema's two holes (M6, M7) and its two contract silences (A2, A8).** Item 6 is the consumer; every one of these is something Item 6 would otherwise have to guess or work around.
5. **Add the one-line disposition for `assert_read_set_covered` (M5)** and the two extra R-F5 filings M1 and M4 imply.

---

## Resolutions

Recorded 2026-08-26 by the design agent, after orchestrator steering (`[AGENT]`). Every code claim below was re-verified in this worktree before acting; all eight must-fix findings were confirmed, none was disputed.

| Finding | Disposition |
|---|---|
| **M1** gate 5 repo-scoped | **Accepted, confirmed.** `_subset` (`:216`) calls `materialize_canonical_subset(family, …)` from `tests/model_families` — family only, no package argument — and the census test reads `DATA / "mfe_census.json"` (`:353`). New **D13**: every gate row declares `scope` (`repo` \| `request`); 1a and 5 are `repo` and that is stated as correct rather than hidden, because they close the lineage chain's other end. The "seam names no package" claim is narrowed in Core Concept, Implementation Notes and D13. **D10** gains the precondition the steering asked for: the workspace asserts every materialized file's digest equals the tracked one before the seam runs, so repo-scoped gates are meaningful by assertion, not by accident. The stale-census fixture **moved to gate 4** (`--census-file`, caller-supplied, workspace-owned). Gate 5's own refusal is recorded as a **stated test-coverage boundary** in Validation Approach, loudly, with the reason (any driver needs a tracked-file edit → R-G3, or a suite edit → R-B2) and with what *is* covered instead. A fifth fixture was found that exercises the shared junit-`<failure>` mapping hermetically: a doctored `STOP_PARSER_CODEGEN_WHEEL` makes gate 1a's hash assertion fail for real (`:88-89`). R-F5 filing added. |
| **M2** gate 1a misclassifies | **Accepted, confirmed.** `os.environ["STOP_PARSER_WHEEL_TARGET"]` and three `STOP_PARSER_<NAME>_WHEEL` reads sit in the test body (`:31-35`, `:82-87`); a `KeyError` there is a junit `<failure>`. Per steering, **gate 0 now owns every environment precondition in one place** — the licence, the four wheel variables, and teax root/importability — and classifies absence as `could_not_run` before any producer is invoked. The Implementation Note claiming `--junitxml` carries R-A6 is retired and replaced with what junit actually does. A test pins each of the six variables unset in turn. |
| **M3** restore inoperative in the workspace | **Accepted, confirmed** (`git checkout -- <ignored path>` matches no pathspec; `--untracked-files=all` does not report ignored paths). **D7 re-derived, not patched**, per steering: one mechanism — backup the resolved package tree to `--out-dir/_backup/` before the first mutating gate, restore by copy driven by D8's before-digest. Works identically in the tracked tree and in the gitignored workspace. The rejection list now includes the git mechanism (the M3 finding) and the give-the-workspace-its-own-git-repo option, with the reason that it would leave two restore mechanisms and change what gate 7's `check_package_clean` judges. |
| **M4** gate 8 detection unreachable | **Accepted, confirmed.** `main` catches `ToolError`/`ManifestError` → `return 1` at `:527-529`, before `write_document`; `VerifyError` subclasses `ToolError` (`:80`); `import simkit` is inside `build_summary` (`:415`). Per steering, mechanism is mine: **D15** — gate 0 probes verify's preconditions itself (teax root, `packages/teax-simkit`, `simkit` importable under D16's environment) and owns the `could_not_run` decision; past gate 0 a non-zero exit is `refused`, full stop, with stderr captured to `--out-dir/verify_stderr.txt`. Stderr string-matching is rejected explicitly (brittle coupling to messages R-B2 freezes). The residual — an unpredicted import failure landing as `refused` — is stated, not hidden. R-F5 filing added. |
| **M5** `assert_read_set_covered` dropped | **Accepted.** **D17** records it as out of reach with the reason (`resolved_paths` exists only inside `indicators.py:808`; synthesizing it would reimplement the reader, which R-B1 `[HARD]` forbids) and states plainly that **nothing else covers it either**. Both alternatives are rejected in writing. R-F5 filing added. Steering said restore-or-record; the honest answer is record. |
| **M6** lineage blocker has no schema home | **Accepted, taken as the ninth gate** per steering, which also settles A1. Lineage is now **gate 9** in the table with a producer (`scripts/integrate.py`, the same answer gate 1b already gave), a scope, and its own `could not run` / `refused` rules. `blocker` gains `expected` and `actual`. The invariant now says **ten** gate entries — R-B1's eight steps expand to nine rows, plus lineage — and says why. |
| **M7** refused vs `PREREQUISITE` | **Accepted, resolved per steering without importing the goal vocabulary.** **D14**: the blocker carries a stable `condition` slug from a closed, enumerated set; the seam stays two-class and two-mode. The `condition` → `PREREQUISITE`/`STRATEGY_BLOCKER`/`MECHANICAL_FAILURE` mapping lives in the operator guide, where the goal layer owns it, and the reasoning for that boundary is recorded in D14. A test pins the slug for every refusal fixture so Item 6 has something stable to key on. A Non-Goal says the vocabulary stays out of `scripts/integrate.py`. |
| **M8** subprocess environment undefined | **Accepted.** **D16** defines it once: inherit `os.environ`, prepend the repo root and `$STOP_PARSER_TEAX_ROOT/packages/teax-simkit` to `PYTHONPATH`, pass the licence and four wheel variables through, and set `STUDY_REQUIRE_TEAX=1` so a teax-dependent producer fails loudly instead of skipping green (`conftest.py:239-242`). The guide lists the same variables so a hand invocation matches the seam's. |
| **A1** eight vs nine | Fixed by M6's ninth gate: ten entries, stated once with the arithmetic. |
| **A2** exit codes | **D18**: `CANDIDATE` → 0, `BLOCKER` → 1, internal error → 2 with a `seam-internal-error` blocker written anyway, so a return document always exists. |
| **A3** B4 already measured | Accepted. B4 downgraded from bet to recorded evidence, citing `WI-030 plan:203` (verify against the **baseline** store: pass, `not_independently_verified: []`, six verdicts). |
| **A4** `load` validates | Confirmed (`manifest.py:384-398`). Gate 6's chain drops the redundant `validate`. |
| **A5** sets vs sorted lists | Accepted. D9 and Implementation Notes carry the `{k: sorted(v)}` normalization the producer's own test uses (`:358`). |
| **A6** teax revision form | Accepted. Gate 1b compares casefolded with expected matched as a **prefix** of actual, both recorded in full — so the recorded short `744745f` works. |
| **A7** request surface wider than the seam row | Accepted. The operator guide gains a "where each input comes from" section. No seam-side preset (it would name a package). |
| **A8** R-D1 invariant self-contradictory | Accepted. The invariant now names what is actually invariant — pin, both fingerprints, package, manifest — and says the three `--out-dir` paths differ by construction. The re-run test asserts that, not byte equality. |
| **A9** `preflight.py clean` exists | Accepted. Gate 0's cleanliness check invokes the subcommand (`:487`) instead of reimplementing it. |
| **A10** cite drift | Fixed: `assert_pin_matches` is `manifest.py:453`. |
| **A11** estimate moves again | Accepted. Restated at design: **14–15 h**, with the five additions that moved it itemized. |
| **A12** conftest no-regression | Accepted. Added to Required Invariants and to the regression row: existing `tests/study` fixtures unchanged in behaviour, pre-existing tally unmoved. |
| B2 noted-as-pending | The spike returned CONFIRMED and **stronger**: recapture is byte-identical, and the tracked snapshot has no `captured_at` at all (v6 envelope dropped it; the WI-029 premise was measured on the dead format). Gate 4 compares whole-file bytes with no exclusion; the `instance_graph.fingerprint` fallback is struck rather than carried. New bet **B6** records the load-bearing census/package co-derivation the review hunted out. |

**Not disputed, not deferred.** Every must-fix is resolved in `design.md`; nothing was pushed to the plan. One finding produced a stated *boundary* rather than a fix — M1's gate-5 refusal coverage — because every available driver breaks R-G3 or R-B2; it is recorded in Validation Approach and in Non-Goals rather than mocked away.

---

**Overall:** **Revise**
**Must-fix (blocks plan):** M1, M2, M3, M4, M5, M6, M7, M8
**Advisory:** A1–A12
**Next Steps:** Record resolutions above, then return to the design-agent session (or re-run `/_my_design`) pointed at this file. The core shape — prove-don't-perform, one CLI, one JSON return, producers invoked not reimplemented — survives intact; what needs work is three gates' scoping and detection, and two fields in the return.
