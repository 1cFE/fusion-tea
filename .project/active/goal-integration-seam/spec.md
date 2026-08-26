# Spec: Verified Package Integration Seam

**Status:** Draft
**Owner:** Reid W
**Created:** 2026-08-26
**Complexity:** MEDIUM
**Branch:** `feat/goal-integration-seam` (worktree, cut from `990501af`)
**Epic:** Goal Strategy and Task Harness (GSTH), Item 3

---

## Problem

Integration is the hop between an audited model change and a study that can run against it. Every gate that hop needs already exists and already fails closed: `sysml-codegen generate` seals the package, `tests/models/test_model_family_spines.py` proves the canonical tree and the census, `scripts/study/manifest.py` re-pins and validates, `scripts/study/preflight.py gates` runs the six checks, `scripts/study/verify.py` re-derives channels and verdicts against the oracle, `scripts/study/identity.py` seals and re-checks package identity, and `tests/test_dependency_provenance.py` pins the toolchain.

What does not exist is a boundary that owns them together. The sequence lives in two work-item plans and a pile of shell commands: `.project/completed/20260821_stellarator-model-migration/plan.md` Phases 2–3 (delete the auto stubs, regenerate with `--smart-regen --preserve-handwritten`, recapture the snapshot, re-pin `manifest.json`, run preflight, run verify) and `.project/active/run-study-first-consumer/plan.md` Phase 3's gate (re-run preflight 6/6 on the regenerated package with the re-pinned manifest). Both plans ran the same sequence correctly; neither is callable.

The cost is concrete and already paid once. Item 6's Phase 2 opened with eleven red tests because a scaffold commit added a `magnet_capital` objective to the manifest without re-pinning the fixtures (`run-study-first-consumer/plan.md:305`). A check did exist — the known-answer fixtures are that check, and they were already red. What was missing is a gate bound to the hop: the check fired nowhere near the commit that broke it, and only when a human happened to run the suite. The step existed in a plan; there was no gate that ran it at the boundary.

`[INHERITED: .project/concepts/goal-strategy-task-harness-design.md § Native seams]` The goal layer this epic builds invokes `integrate` as a seam — audited item(s) and expected lineage in, one verified candidate pin and fingerprint out — and the concept-design states that until this repair exists a goal round may not silently absorb it. `[INHERITED: epic Item 3 Current State]` Today a goal task cannot request integration and receive one authoritative candidate reference without reconstructing the hand pattern.

`[INHERITED: epic Item 3 Objective]` The obligation: turn audited model work into exactly one verified, study-ready candidate pin and fingerprint, or a named blocker.

## The two return classes

Every invocation ends in exactly one of these. They are named throughout this spec, so they are defined once here.

| Class | Meaning | Decided when |
|---|---|---|
| **CANDIDATE** | One verified, study-ready package identity exists and is named. | Every gate in the sequence returned pass, and the return resolves to exactly one package, manifest, pin, semantic fingerprint, and executable fingerprint. |
| **BLOCKER** | No candidate is promoted. The obstacle is named with the producer involved and where its evidence sits. | Any gate in the sequence refused, any gate could not be run, any precondition was unmet, or the sequence could not resolve to exactly one candidate identity. |

There is no partial or provisional return. `[INFERRED]` A run that regenerated a package but failed at verification returns `BLOCKER`, not a candidate carrying a caveat — the goal question the seam answers is "Is there **one** study-ready candidate?" and a caveated yes is a no.

**Every `BLOCKER` says which of two things happened** (R-A6): a gate **refused** — it ran and returned a negative verdict — or a gate **could not run** — its preconditions, environment, or tooling stopped it before it could judge anything. `[INHERITED: .project/concepts/goal-strategy-task-harness-design.md § Problem, § Task-grain invocation]` The concept-design turns on this distinction: an operational accident deserves an identical retry (`MECHANICAL_FAILURE`, which permits a `RetryCheck`), while a semantic refusal changes what work is justified and may close the round. A caller cannot make that call from undifferentiated prose. This is not hypothetical for these gates — `tests/models` errors rather than judges when `SYSIDE_LICENSE_KEY` is not exported (`run-study-first-consumer/plan.md:306`). One producer already draws this line natively: `preflight.py gates` emits a per-gate `DID_NOT_RUN` status distinct from `FAIL`, with the blocking condition named by its `unavailable()` helper (`preflight.py:368-377`).

`[INFERRED]` A re-run on unchanged inputs is not a third class. It returns either `CANDIDATE` naming the **same** identity as the prior run, or a `BLOCKER` (see R-D1, R-D3). What it never does is silently mint a second, conflicting identity — that is what makes the seam safe to call twice. It is *not* a claim that a second call always succeeds; see R-D4 for the determinism assumption underneath.

## Ordering note (recorded, not a conflict)

`[INHERITED: .project/concepts/goal-strategy-task-harness-design.md:156]` The concept-design writes the seam as "regeneration → verification → pin". The proven manual sequence pins before it verifies: the manifest re-pin is what preflight and verify read (`migration plan:269-291`, `preflight.py:233` `check_manifest_currency`). `[INFERRED]` The concept-design line is shorthand for the boundary, not an ordering ruling; the authoritative order is the producers' own (R-B1). Recorded here so a downstream reader does not treat the shorthand as a constraint.

**What "authoritative order" rests on** `[AGENT]`. It is not "the order the referents happened to run in" — a plan's sequence is partly its own scope. R-B1's order is graded per edge on one of two bases: a **data dependency** (a gate reads a file an earlier step writes, so the order is forced) or an **inference** from the epic's producer list plus the referents' agreement. The edges are labelled in R-B1. Where the basis is inference, R-B4's no-reorder rule still binds design, but the grade says design may raise it rather than treat it as physics.

## Success Criteria

The first five are epic Item 3's checkboxes, restated as testable outcomes. SC6 covers the item's operator-documentation deliverable.

- [ ] **SC1** `[INHERITED: epic Item 3]` — A known audited model change, put through the seam, produces one `CANDIDATE` return whose package root, manifest path, pin, semantic fingerprint, executable fingerprint, and verification evidence each resolve to something that exists on disk, matches the package it names, and matches the lineage the request named.
- [ ] **SC2** `[INHERITED: epic Item 3]` — Every gate that has an existing producer is invoked through it, not reimplemented (the one gate with no producer is R-B1.1b, and R-B5 records why and files the gap); and a deliberately failed gate produces a `BLOCKER` that names the producer involved, says whether it refused or could not run, and cites its native evidence, with no candidate promoted.
- [ ] **SC3** `[INHERITED: epic Item 3]` — Re-running against unchanged inputs does not produce a second conflicting candidate identity.
- [ ] **SC4** `[INHERITED: epic Item 3]` — A candidate returned by the seam is accepted by the stock study preflight and verification route, invoked as a study invokes them, with no seam-specific accommodation.
- [ ] **SC5** `[INHERITED: epic Item 3]` — Focused integration tests pass, and the model-family spine, dependency-provenance, and affected study regressions stay green.
- [ ] **SC6** `[INHERITED: epic Item 3 Deliverables]` — A non-author walks the seam's operator documentation and can, from it alone, assemble an integration request, invoke it, tell `CANDIDATE` from `BLOCKER`, cite the returned candidate in a study, and act on a named blocker.
  **Evidence form** `[AGENT]`: a fresh session that did not build the seam performs the walk against the shipped operator doc, working only from it, and records the walk — what it ran, what it got back, and every point where it had to read source or guess — in this item's audit artifact. The sibling seam failed exactly this criterion shape at audit for want of a stated form (Item 2 audit 2026-08-26, SC7/SC9, `CURRENT_WORK.md`), and its fix pass had to reconstruct one. Naming it now is the cheap version.

## Known Requirements

### A. Request and return contract

- **R-A1** `[INHERITED: epic Item 3 Scope 1]` The seam accepts audited native work references, the canonical model inputs, the target package and manifest, and the expected lineage. An invocation missing any of these is a `BLOCKER`, not a best-effort run.
- **R-A2** `[INHERITED: epic Item 3 Scope 1]` A `CANDIDATE` return names one package, one manifest, one pin, a semantic fingerprint, an executable fingerprint, and the verification evidence. A `BLOCKER` return names the **producer** that stopped the sequence, why, and the path to that producer's own output — which may itself report several failed sub-gates (R-B4). Where the obstacle is a lineage mismatch (R-C9), it names the expected lineage and the actual one.
- **R-A3** `[INHERITED: concept-design § Native seams]` One invocation yields at most one candidate identity. If the inputs resolve to more than one package or manifest, that ambiguity is itself a `BLOCKER` (R-C5).
- **R-A4** `[INFERRED]` The seam is callable on its own — not only from inside a goal round. Item 6 is one consumer, not the only one. Provenance, stated exactly: the epic's route-equivalence row is itself `[AGENT]`-grade, sits at epic level, and says hand-operated and goal-agent-operated paths produce equivalent goal artifacts and native end states in a documented comparison (`epic_goal_strategy_task_harness.md:57`). It does not name Item 3 and does not by itself require this item to ship a separate human entry surface. What it does require is that a human can reach the same seam a goal task reaches. Whether that means a distinct operator surface or the same entry point invoked by hand is design's (see Open Questions) — and it is a real sizing question against the epic's 8h execute estimate.
- **R-A5** `[INFERRED]` The return is machine-readable enough to be checked by a test and readable enough to be pasted into a study record or a goal trail entry. Format and home are design's (see Open Questions).
- **R-A6** `[INHERITED: concept-design § Problem and § Task-grain invocation]` A `BLOCKER` states whether the gate **refused** or **could not run**. The caller's retry rule reads this: an inability to run is the operational accident an identical retry may fix; a refusal is a result about the candidate. The seam classifies; it does not decide whether to retry. `[AGENT]` One producer already implements this distinction natively and is the shape to match: `preflight.py run_gates` emits a per-gate `DID_NOT_RUN` status distinct from `FAIL`, with the blocking condition named by `unavailable()` (`preflight.py:368-370`, gates at `:375-424`). Design matches that existing shape rather than inventing one, and only has to work out detection for the producers that lack it.

### B. Producer-owned sequence

- **R-B1** `[HARD]` **that each gate is invoked and never reimplemented** (`[INHERITED: epic Item 3 Scope 2]`); `[INFERRED]` **for the order**, graded per edge below. The producers, in order:
  1. **Toolchain pin check** — split, because the two halves have different producer coverage:
     - **1a. Pinned packages** `[HARD]` — `tests/test_dependency_provenance.py` asserts the `pyproject.toml`/`uv.lock` pins and the installed `__version__`/wheel hashes for **agentic-mbse, sysml-codegen, and 1costingfe**, and that each resolves under the installed wheel target rather than a checkout (`:13-35`, `:54-102`). This is the producer for migration-plan invariant I2 (never generate through a local checkout).
     - **1b. teax revision** `[INFERRED]` — **no producer exists.** teax is not a pinned dependency; it is a working checkout reached through `STOP_PARSER_TEAX_ROOT` (`tests/study/conftest.py:230-262`), it exposes no `__version__`, and nothing in `tests/` or `scripts/study/` asserts its git revision. The only teax pin check that has ever run is hand-typed: `git -C "$STOP_PARSER_TEAX_ROOT" rev-parse --short HEAD` → `744745f`, or stop (`migration plan:47`). **The seam performs this comparison itself**, against an expected revision the caller supplies or the seam records (which of the two is design's — Open Questions). See R-B5 for why this is not a violation of R-B2, and where the gap is filed.
  2. **Regeneration** — `sysml-codegen generate ... --smart-regen --preserve-handwritten` in place (migration plan `:201`; WI-030 plan `:151`). *Edge 1→2: data dependency — generating through an unpinned tool invalidates every downstream identity.*
  3. **Handwritten preservation** — the `AUTO_IMPLEMENTED = False` implementations survive regeneration byte-for-byte (migration plan `:511`, risk note `:475`: a stubbed normative file is a failed gate even when the seal is clean; WI-030 checks it with `sha256sum -c`, `:152`). *Edge 2→3: data dependency — it reads regeneration's output.*
  4. **Census / snapshot recapture** — the tracked instance-graph snapshot is recaptured so it matches the sealed package, and `tests/models/data/mfe_census.json` is re-derived from the sealed contract and re-bound to its new semantic fingerprint (migration plan `:203`; WI-030 plan `:156-157`, which does both in one step). *Edge 3→4: data dependency — both are derived from the sealed package.*
  5. **Model-family spine** — `tests/models/test_model_family_spines.py`: twins byte-identical, per-family generation seals with zero diagnostics and live equals snapshot (`:308-327`), census exact (`:333`, `:349-356`), mutations reach every and only their bound consumers. *Edge 4→5: data dependency — the census test reads `tests/models/data/mfe_census.json` (`test_model_family_spines.py:353`), which step 4 writes. Both referents ran it in this order (migration plan `:203` then `:212`; WI-030 plan `:156-157` then `:161`). WI-030 also shows the dependency firing: before recapture, `tests/models` is green **except** the MFE census test, which fails with "model meaning moved — re-derive" by design (`WI-030 plan:129`).*
    - **Correction of record** `[AGENT]`: the epic's Scope 2 enumeration lists "model-family, census/snapshot" in the opposite order (`epic_goal_strategy_task_harness.md:256`). That list names the producers; it is not an ordering ruling, and the data dependency above runs the other way. Recorded rather than silently followed.
  6. **Manifest re-pin** — `scripts/study/manifest.py`: `indicator_input_fingerprint`, `recorded_provenance`, baseline point keys, ties, objective catalog; then `validate`, `assert_package_identity`, `assert_pin_matches`, `assert_read_set_covered`. *Edge 5→6: data dependency — the re-pin writes the sealed package's fingerprints, so the package must be sealed and proven first.*
  7. **Preflight** — `scripts/study/preflight.py gates` over the package, manifest, groups, identity document, and baseline result. *Edge 6→7: data dependency — `check_manifest_currency` (`preflight.py:233`) reads the re-pinned manifest.*
  8. **Verification** — `scripts/study/verify.py` against the package, manifest, and identity. *Edge 7→8: `[INFERRED]` — verify does not read preflight's output, so nothing forces this edge; both referents ran preflight first (migration plan `:289-290`) and it is the cheaper refusal, so it goes first.*
- **R-B2** `[HARD]` `scripts/study/` and the other producers are not edited to make the sequence callable. The seam is a fusion-tea-side caller. (`[INHERITED: epic Item 3 Out of Scope]`; migration plan invariant I11 / `:291` `git diff --stat -- scripts/study/` empty.)
- **R-B3** `[INHERITED: epic Item 3 Scope 2]` Native artifacts are read as truth. The seam does not copy a producer's stage state into its own record; it cites the producer's output by path.
- **R-B4** `[INFERRED]` The order in R-B1 is the contract. A gate is not skipped because a prior run passed it, and a later gate does not run after an earlier one refused — the seam stops at the first refusing producer and reports it. "Stops at the first refusal" is at producer grain, not sub-gate grain: `preflight.py gates` deliberately reports all six of its checks whatever happened (`preflight.py:333-335`, docstring "Every gate appears in the result, whatever happened"), so a `BLOCKER` from preflight names the producer and cites its whole result document (R-B3), which may carry several failures at once.
- **R-B5** `[AGENT]` The teax revision comparison (R-B1.1b) is performed by the seam itself, and the absence of a producer for it is recorded, not papered over.
  - **Why this does not violate R-B2.** R-B2 forbids editing `scripts/study/` and forbids reimplementing a producer's gate. There is no teax pin implementation anywhere in the repo, so there is nothing to duplicate and no verdict to second-guess. The alternative — leaving gate 1b to design — would send design at R-C2 ("an installed toolchain revision differs from its pin") resting on a producer that does not cover it, which is the defect this clause exists to close. A `git rev-parse` compared against a recorded expected revision is the migration plan's own hand pattern (`:47`), lifted, not invented.
  - **Fail-closed default.** If the expected teax revision is not supplied, or `STOP_PARSER_TEAX_ROOT` is unset or unreadable, gate 1b **could not run** (R-A6) and the invocation is a `BLOCKER`. It is never treated as a pass.
  - **The gap is filed, in two places, per R-F5 and R-F3.** That fusion-tea has no automated teax revision pin is a fusion-tea-side gap whose home is `tests/test_dependency_provenance.py` and a BACKLOG row. That stock teax exposes no `__version__` for a tool to read is the upstream half (R-F3), and it is the same root cause as the open `verify.py` `teax.revision: "unrecorded"` row (`DISCOVERY_LOG.md` `20260821-power-cycle-ab#8`, cited in R-E4). The seam doing the comparison discharges neither.

### C. Fail-closed behaviour

`[INHERITED: epic Item 3 Scope 3]` Each of these produces a `BLOCKER` with no candidate promoted:

- **R-C1** Dirty inputs — the package tree is not git-clean, or working-tree state would make the sealed identity unreproducible (`preflight.py:300` `check_package_clean`).
- **R-C2** Drifted tool inputs — a pinned package's installed revision differs from its pin, or generation would run through a local checkout rather than the pinned artifact (both covered by R-B1.1a); or the teax checkout's revision differs from the recorded expected one, or cannot be read (R-B1.1b, R-B5).
- **R-C3** Unverifiable output — verification does not pass, or leaves a declared channel or verdict not independently verified.
- **R-C4** Fingerprint mismatch — the manifest's recorded pin, the sealed identity document, and the package's own contract do not agree (`manifest.py:442,453`; `identity.py:288`).
- **R-C5** Missing declared keys or constraints, or ambiguous candidate lineage — a declared axis key, objective channel, or constraint identity is absent from the package (`preflight.py:162` `check_declared_keys`), or the request does not resolve to exactly one candidate.
- **R-C6** `[HARD]` Failure is reported, never repaired. `[INHERITED: epic Item 3 Out of Scope]` The seam does not change the model, sysml-codegen, teax, or study semantics to make a candidate pass, and does not relax a threshold or a tolerance.
- **R-C7** `[INHERITED: epic Item 3 Scope 3]` No in-place mutation of a committed study record or its evidence. A committed record is immutable; corrections go to an addendum, which is the study's own procedure and not this seam's business.
- **R-C8** `[INFERRED]` A refused run leaves no half-promoted state: no manifest re-pinned to a package that failed a later gate, no candidate reference a reader could mistake for verified. Whether that is achieved by ordering, by staging, or by rollback is design's.
- **R-C9** `[INHERITED: concept-design § Native seams; epic Item 3 Scope 1]` Lineage mismatch — the candidate that comes out is not the lineage the request named. Expected lineage is a required input (R-A1); a candidate that is internally consistent and verifies cleanly but does not correspond to the audited work the caller named is a `BLOCKER`, not a candidate. This is the Problem section's Item 6 failure one level up: a manifest and a package that agreed with themselves and not with each other, with nothing at the hop to catch it — the check that did exist fired far from the commit, and only when someone happened to run the suite.

### D. Identity stability

- **R-D1** `[INHERITED: epic Item 3 SC3]` Re-running on unchanged inputs returns the same candidate identity. The seam does not mint a second, conflicting one.
- **R-D2** `[INFERRED]` "Unchanged inputs" is defined by what the producers already digest — package contents, indicator-input read set, tool source digest, toolchain revisions — not by a new identity scheme invented here. If a digest the producers already compute moves, the inputs changed and a new identity is correct.
- **R-D3** `[INFERRED]` If a re-run produces a different identity while the recorded inputs claim to be unchanged, that is a `BLOCKER` (it is R-C4, fingerprint mismatch, seen from the other side), not a silently accepted new candidate.
- **R-D4** `[AGENT]` **The determinism assumption, stated as an assumption.** R-B4 skips no gate, so a second invocation re-runs regeneration (R-B1.2) in place; R-C1 makes a non-git-clean package tree a `BLOCKER`. So R-D1's "same identity" holds only if regeneration under the pinned toolchain is byte-stable onto an already-regenerated tree. The contract does not depend on that being true:
  - **Whatever the answer, a re-run on unchanged inputs returns the prior identity or a `BLOCKER`.** It never mints a second, conflicting identity and never promotes a candidate off a tree the re-run dirtied. If regeneration is stable, R-D1's `CANDIDATE` path holds. If it is not, the dirtied tree trips R-C1 and the return is a `BLOCKER` naming that gate — a loud stop, which is the correct fail-closed outcome and is what SC3 actually requires.
  - **Evidence so far is favourable but incomplete.** The migration's regeneration reported `Preserved: 10, Regenerated: 0` with both normative impls byte-identical, but that was a first regeneration onto a repaired tree (`migration plan:511`). WI-030 ran the closer check — generate a second time into a scratch directory and `diff -r` against `generated/` ignoring timestamps, no semantic difference (`WI-030 plan:158`, result recorded at `:291` — the only differences were preserved-impl sha entries and cosmetic source-line refs). That is a scratch-target comparison, still not a re-run in place onto its own output.
  - **De-risked — assumption CONFIRMED** `[AGENT]`, 2026-08-26, `spike_regen_determinism.md`. The pinned generate run in place on the sealed stellarator package left the tree byte-identical and both fingerprints unmoved, on the first in-place run and again on the second (`git status --porcelain` empty at every step; semantic `1ca93d0c…`, executable `7447efea…` throughout). Mechanism: `--preserve-handwritten` never opens the 58 files under `generated/handwritten/`, and the 95 files it does rewrite come out byte-identical. **So R-B4 needs no exemption for regeneration**, and R-D1's same-identity `CANDIDATE` path is the one that fires on unchanged inputs rather than the fail-closed `BLOCKER` above. Regeneration costs 1.8s, so re-running it is not a cost question either. The spike also records that `SYSIDE_LICENSE_KEY` must be exported for generate to run at all (an R-A6 could-not-run condition) and that nothing downstream reads mtimes.

### E. Evidence and citability

- **R-E1** `[INHERITED: epic Item 3 Scope 4]` The seam deposits one concise integration return that a human or a goal agent can cite, and that a study can consume without re-deriving the sequence.
- **R-E2** `[INFERRED]` The return carries what a downstream reader needs to check it without re-running: which gates ran, in what order, what each returned, and where each producer's own output sits. It carries this by reference, per R-B3.
- **R-E3** `[INHERITED: MR-4 / CLAUDE.md § Traceability]` Every identity and digest in the return resolves — to a repo path, a commit, or a producer's output file. A bare number with no home is not evidence.
- **R-E4** `[INFERRED]` The return records the toolchain revisions it ran under, because a candidate's meaning depends on them. This also stands in for a known producer defect: `verify.py` writes `teax.revision: "unrecorded"` (`DISCOVERY_LOG.md` `20260821-power-cycle-ab#8`, still open, home `scripts/study/verify.py`). The seam recording the revision does not discharge that row (R-F5).

### F. Boundaries the seam observes

- **R-F1** `[INHERITED: epic Item 3 Out of Scope]` The seam does not commit, push, or close modeling work, and does not choose among multiple valid model designs. Those stay with the owner and the modeling PM.
- **R-F2** `[INHERITED: epic Item 3 Out of Scope]` No goal-side effects ledger, no idempotency wrapper, no second verification implementation. R-D1 is satisfied by producer-computed identity, not by a new control-plane mechanism. `[OWNER, epic § Hardening rule]` No hardening-path mechanism enters the first build without a recorded run failure that promotes it.
- **R-F3** `[INHERITED: align.md — AGENT-grade orchestrator reading]` Changes needed inside pinned sysml-codegen, teax, or agentic-mbse are upstream filings, never in-repo edits.
- **R-F4** `[INHERITED: align.md — AGENT-grade orchestrator reading]` The calc-then-compare constraint form that `scripts/study/indicators.py:469` and `verify.py:193` cannot parse (BACKLOG Flagged row) is not fixed here. The seam surfaces the native gate's result as-is.
- **R-F5** `[INFERRED]` A defect or gap in an in-repo producer — under `scripts/study/` or `tests/` — that the seam works around is recorded against that producer's existing home: an open `DISCOVERY_LOG.md` row or a BACKLOG row. It is not absorbed silently into the seam. R-B2 freezes those files; R-F3 routes pinned-tool defects upstream; without this clause an in-repo producer defect has no route back to its owner and the workaround becomes permanent by omission. Two live instances: the `verify.py` `teax.revision: "unrecorded"` row (R-E4) and the absent teax revision pin check (R-B5).

### G. Testing

- **R-G1** `[INHERITED: epic Item 3 Deliverables]` Integration fixtures and tests cover three shapes: a successful candidate, a gate failure, and identity stability across a re-run.
- **R-G1a** `[INFERRED]` A fourth shape covers SC4: the candidate the seam returns is fed to `preflight.py gates` and `verify.py` exactly as a study feeds them — same arguments, no seam-specific accommodation — and both pass. Without this, SC4 is a checkbox nobody can tick: R-G1's three inherited shapes do not cover it, and Open Question 5 otherwise defers *whether it is demonstrated at all*. The test may reuse the success-path fixture; it does not need a real study.
- **R-G2** `[INHERITED: epic Item 3 SC5]` Model-family, dependency-provenance, and affected study regressions pass alongside the new tests.
- **R-G3** `[INFERRED]` Tests are hermetic: no test writes into a tracked package, a tracked manifest, or a committed study record. This is Item 2's F3 finding, learned on the sibling seam (`CURRENT_WORK.md:18`), applied before it is repeated.
- **R-G4** `[INFERRED]` The gate-failure test drives a real refusal from a real producer, not a mocked one. A seam that only knows how to report simulated failures has not been shown to fail closed.

## Non-Goals

- Changing sysml-codegen, teax, the model, or study semantics so a candidate passes. `[INHERITED: epic Item 3]`
- Automatic commit, push, or modeling-item close. `[INHERITED: epic Item 3]`
- Selecting among multiple valid model designs. `[INHERITED: epic Item 3]`
- A goal-side effects ledger, idempotency wrapper, or duplicate verification implementation. `[INHERITED: epic Item 3]`
- Fixing the calc-then-compare parser limitation. Out of scope: it stays flagged in BACKLOG and is surfaced as-is, because the seam's job is to invoke the producers' gates and report them, not to extend what they can parse. `[INHERITED: align.md]`
- Running or interpreting a study. The seam hands over a candidate; `study.execute` and `study.read` are separate seams. **Boundary note — `[AGENT]`, an agent call awaiting owner ratification, not a settled item like the bullets above**: executing the baseline point and any probe run that `preflight.py gates` and `verify.py` themselves require is *inside* the seam, not a study. A study is a declared question with axes, arms, a record, and findings; running a gate's own input is none of those. The referents put it on this side of the line: WI-030 runs `study_route.execute_baseline` to deposit `package_identity.json` and `baseline_result.json` as part of the re-pin phase, before preflight and before any study (`WI-030 plan:194`). Item 6 invokes the seam and then runs a study against the returned contract (epic Item 6 Scope 1–2), and that split holds under this reading. Stated so design chooses against a boundary rather than inventing one; if the owner reads it the other way, R-B1.7–8 need a caller-supplied baseline instead and Open Question 4 becomes an owner question.
- Editing GOAL_RUNBOOK, DISCOVERY_LOG, or the run-study runbook. Item 1 owns those; this item's operator doc is its own deliverable. `[INHERITED: align.md]`

## Open Questions / Deferred to design

`[AGENT]` The first three are the orchestrator's Align readings, unchallenged, recorded here as the deferrals they are.

- **Entry-surface shape** — CLI script, Python entry point, slash command, or a combination; and how a goal task and a human each reach it (R-A4). Includes the sizing call: whether "a human can reach the same seam" needs a distinct operator surface in the first build, or the same entry point invoked by hand is enough.
- **Where the expected teax revision comes from** (R-B1.1b, R-B5) — a field in the integration request, a value recorded in the seam's own configuration, or a pin file. The fail-closed default is fixed either way: absent or unreadable is a `BLOCKER`.
- ~~**Regeneration determinism de-risk** (R-D4)~~ — **settled 2026-08-26.** Spike confirmed the pinned generate is byte-stable in place: the tree stayed git-clean and both fingerprints unmoved across two in-place runs, so R-B4 needs no regeneration exemption. See `spike_regen_determinism.md`.
- **Return-artifact format and home** — what the integration return looks like on disk and where it lives (R-A5, R-E1).
- **SC1 fixture strategy** — how to obtain a "known audited model change" for the success-path test without minting new modeling work. The stellarator package and its migration history are the obvious material; whether the fixture replays a past change, applies a throwaway one, or uses a copy is design's call.
- **What the seam runs verification against.** `verify.py` verifies a *store* of executed cases (`verify.py:343` `verify_store`), and `preflight.py gates` needs a baseline result — so both need execution, not just a sealed package. Whether the seam executes a minimal baseline/probe set itself, reuses one the caller supplies, or splits the boundary differently is a design decision. The requirement (R-B1.7–8, SC4) is that the stock gates are the ones that run.
- **Where the seam stops relative to the study.** R-G1a settles that SC4 is demonstrated *here*, by a test feeding the returned candidate to the stock preflight and verify route. What stays open is whether the seam's own entry point performs that hand-off as a step, or the test is the only place it happens.
- **Blocker taxonomy shape.** R-A6 fixes the one distinction the caller's retry rule needs (refused vs. could-not-run), and names `preflight.py`'s `DID_NOT_RUN` as the shape to match. Beyond that: whether the six refusal causes R-C1–C5 and R-C9 appear as typed codes or as prose naming the producer, and how "could not run" is detected for the producers that do not already signal it, are design's.
- **Currency of the concept-design's "pending native repair" marker.** `goal-strategy-task-harness-design.md:152,156` still labels `integrate` pending and tells slice 5 to use the manual pattern; both go false when this item lands. Retiring that marker is not this spec's to do — the Non-Goals hand shared files to Item 1 and the proof to Item 6 — but it is owed at epic close and is recorded here so it is not found there.
- **Rollback vs. ordering for R-C8.** Whether "no half-promoted state" is achieved by doing the mutating steps last, by staging, or by an explicit undo.

---

## Related Artifacts

- **Epic:** `.project/backlog/epic_goal_strategy_task_harness.md` § Item 3
- **Align:** `.project/active/goal-integration-seam/align.md` (owner rulings and orchestrator readings, 2026-08-26)
- **Spike:** `.project/active/goal-integration-seam/spike_regen_determinism.md` — R-D4 CONFIRMED: pinned regeneration is byte-stable in place, so R-B4 skips no gate and needs no exemption (2026-08-26)
- **Required Reading:**
  - `.project/concepts/goal-strategy-task-harness-design.md` § Native seams, § Validation and Handoff
  - `.project/active/run-study-first-consumer/plan.md` — current manual integration referent
  - `.project/completed/20260821_stellarator-model-migration/plan.md` — sealed-package migration and verification path
  - `work/completed/20260822_WI-030_computed-beta-peak-field/plan.md` — the most recent steady-state referent: one model change through the whole sequence (Phases 3–4), including the regeneration-stability check
  - `scripts/study/manifest.py`, `scripts/study/preflight.py`, `scripts/study/verify.py`, `scripts/study/identity.py` — existing gates
  - `tests/models/test_model_family_spines.py`, `tests/test_dependency_provenance.py` — lineage and generated-tree checks
- **Sibling seam (precedent):** `.project/active/goal-research-seam/spec.md` — Item 2, same contract shape
- **Product-lens:** `.project/active/goal-integration-seam/product-lens.md`
- **Design:** `.project/active/goal-integration-seam/design.md` (to be created)

---

**Next Steps:** `/_my_spec_review` in a fresh session, then `/_my_design`.
