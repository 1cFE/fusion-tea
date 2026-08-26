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

The cost is concrete and already paid once. Item 6's Phase 2 opened with eleven red tests because a scaffold commit added a `magnet_capital` objective to the manifest without re-pinning the fixtures (`run-study-first-consumer/plan.md:305`). Nothing checked the manifest against the package until a study run tripped over it. The step existed in a plan; there was no gate that ran it.

`[INHERITED: .project/concepts/goal-strategy-task-harness-design.md § Native seams]` The goal layer this epic builds invokes `integrate` as a seam — audited item(s) and expected lineage in, one verified candidate pin and fingerprint out — and the concept-design states that until this repair exists a goal round may not silently absorb it. `[INHERITED: epic Item 3 Current State]` Today a goal task cannot request integration and receive one authoritative candidate reference without reconstructing the hand pattern.

`[INHERITED: epic Item 3 Objective]` The obligation: turn audited model work into exactly one verified, study-ready candidate pin and fingerprint, or a named blocker.

## The two return classes

Every invocation ends in exactly one of these. They are named throughout this spec, so they are defined once here.

| Class | Meaning | Decided when |
|---|---|---|
| **CANDIDATE** | One verified, study-ready package identity exists and is named. | Every gate in the sequence returned pass, and the return resolves to exactly one package, manifest, pin, semantic fingerprint, and executable fingerprint. |
| **BLOCKER** | No candidate is promoted. The obstacle is named with the gate involved and where its evidence sits. | Any gate in the sequence refused, any gate could not be run, any precondition was unmet, or the sequence could not resolve to exactly one candidate identity. |

There is no partial or provisional return. `[INFERRED]` A run that regenerated a package but failed at verification returns `BLOCKER`, not a candidate carrying a caveat — the goal question the seam answers is "Is there **one** study-ready candidate?" and a caveated yes is a no.

**Every `BLOCKER` says which of two things happened** (R-A6): a gate **refused** — it ran and returned a negative verdict — or a gate **could not run** — its preconditions, environment, or tooling stopped it before it could judge anything. `[INHERITED: .project/concepts/goal-strategy-task-harness-design.md § Problem, § Task-grain invocation]` The concept-design turns on this distinction: an operational accident deserves an identical retry (`MECHANICAL_FAILURE`, which permits a `RetryCheck`), while a semantic refusal changes what work is justified and may close the round. A caller cannot make that call from undifferentiated prose. This is not hypothetical for these gates — `tests/models` errors rather than judges when `SYSIDE_LICENSE_KEY` is not exported (`run-study-first-consumer/plan.md:308`).

`[INFERRED]` A re-run on unchanged inputs is not a third class. It returns `CANDIDATE` naming the **same** identity as the prior run (see R-D1), which is what makes the seam safe to call twice.

## Ordering note (recorded, not a conflict)

`[INHERITED: .project/concepts/goal-strategy-task-harness-design.md:156]` The concept-design writes the seam as "regeneration → verification → pin". The proven manual sequence pins before it verifies: the manifest re-pin is what preflight and verify read (`migration plan:269-291`, `preflight.py:233` `check_manifest_currency`). `[INFERRED]` The concept-design line is shorthand for the boundary, not an ordering ruling; the authoritative order is the producers' own (R-B1). Recorded here so a downstream reader does not treat the shorthand as a constraint.

## Success Criteria

The first five are epic Item 3's checkboxes, restated as testable outcomes. SC6 covers the item's operator-documentation deliverable.

- [ ] **SC1** `[INHERITED: epic Item 3]` — A known audited model change, put through the seam, produces one `CANDIDATE` return whose package root, manifest path, pin, semantic fingerprint, executable fingerprint, and verification evidence each resolve to something that exists on disk, matches the package it names, and matches the lineage the request named.
- [ ] **SC2** `[INHERITED: epic Item 3]` — Every gate in the sequence is invoked through its existing producer, not reimplemented; and a deliberately failed gate produces a `BLOCKER` that names that gate, says whether it refused or could not run, and cites its native evidence, with no candidate promoted.
- [ ] **SC3** `[INHERITED: epic Item 3]` — Re-running against unchanged inputs does not produce a second conflicting candidate identity.
- [ ] **SC4** `[INHERITED: epic Item 3]` — A candidate returned by the seam is accepted by the stock study preflight and verification route, invoked as a study invokes them, with no seam-specific accommodation.
- [ ] **SC5** `[INHERITED: epic Item 3]` — Focused integration tests pass, and the model-family spine, dependency-provenance, and affected study regressions stay green.
- [ ] **SC6** `[INHERITED: epic Item 3 Deliverables]` — A non-author walks the seam's operator documentation and can, from it alone, assemble an integration request, invoke it, tell `CANDIDATE` from `BLOCKER`, cite the returned candidate in a study, and act on a named blocker.

## Known Requirements

### A. Request and return contract

- **R-A1** `[INHERITED: epic Item 3 Scope 1]` The seam accepts audited native work references, the canonical model inputs, the target package and manifest, and the expected lineage. An invocation missing any of these is a `BLOCKER`, not a best-effort run.
- **R-A2** `[INHERITED: epic Item 3 Scope 1]` A `CANDIDATE` return names one package, one manifest, one pin, a semantic fingerprint, an executable fingerprint, and the verification evidence. A `BLOCKER` return names the gate involved, why, and the path to that gate's own output. Where the obstacle is a lineage mismatch (R-C9), it names the expected lineage and the actual one.
- **R-A3** `[INHERITED: concept-design § Native seams]` One invocation yields at most one candidate identity. If the inputs resolve to more than one package or manifest, that ambiguity is itself a `BLOCKER` (R-C5).
- **R-A4** `[INFERRED]` The seam is callable on its own — by an operator at a terminal or by another surface — not only from inside a goal round. Item 6 is one consumer, not the only one, and the epic requires hand-operated and agent-operated paths to reach the same end state (epic Success Criteria, `[AGENT]` route-equivalence row).
- **R-A5** `[INFERRED]` The return is machine-readable enough to be checked by a test and readable enough to be pasted into a study record or a goal trail entry. Format and home are design's (see Open Questions).
- **R-A6** `[INHERITED: concept-design § Problem and § Task-grain invocation]` A `BLOCKER` states whether the gate **refused** or **could not run**. The caller's retry rule reads this: an inability to run is the operational accident an identical retry may fix; a refusal is a result about the candidate. The seam classifies; it does not decide whether to retry.

### B. Producer-owned sequence

- **R-B1** `[HARD]` Each gate is invoked, never reimplemented. The producers and their authoritative order, as proven by the manual referents:
  1. **Toolchain pin check** — the installed sysml-codegen and teax revisions are the pinned ones (`tests/test_dependency_provenance.py`; migration plan I2 at `:50-51`: never generate through a local checkout).
  2. **Regeneration** — `sysml-codegen generate ... --smart-regen --preserve-handwritten` in place (migration plan `:201`).
  3. **Handwritten preservation** — the `AUTO_IMPLEMENTED = False` implementations survive regeneration byte-for-byte (migration plan `:511`, risk note `:475`: a stubbed normative file is a failed gate even when the seal is clean).
  4. **Model-family spine** — `tests/models/test_model_family_spines.py`: twins byte-identical, generation seals with zero diagnostics, census exact, mutations reach every and only their bound consumers.
  5. **Census / snapshot** — the tracked instance-graph snapshot is recaptured so it matches the sealed package (migration plan `:203`), and the census stays bound to the semantic fingerprint it was derived against.
  6. **Manifest re-pin** — `scripts/study/manifest.py`: `indicator_input_fingerprint`, `recorded_provenance`, baseline point keys, ties, objective catalog; then `validate`, `assert_package_identity`, `assert_pin_matches`, `assert_read_set_covered`.
  7. **Preflight** — `scripts/study/preflight.py gates` over the package, manifest, groups, identity document, and baseline result.
  8. **Verification** — `scripts/study/verify.py` against the package, manifest, and identity.
- **R-B2** `[HARD]` `scripts/study/` and the other producers are not edited to make the sequence callable. The seam is a fusion-tea-side caller. (`[INHERITED: epic Item 3 Out of Scope]`; migration plan invariant I11 / `:291` `git diff --stat -- scripts/study/` empty.)
- **R-B3** `[INHERITED: epic Item 3 Scope 2]` Native artifacts are read as truth. The seam does not copy a producer's stage state into its own record; it cites the producer's output by path.
- **R-B4** `[INFERRED]` The order in R-B1 is the contract. A gate is not skipped because a prior run passed it, and a later gate does not run after an earlier one refused — the seam stops at the first refusal and reports it.

### C. Fail-closed behaviour

`[INHERITED: epic Item 3 Scope 3]` Each of these produces a `BLOCKER` with no candidate promoted:

- **R-C1** Dirty inputs — the package tree is not git-clean, or working-tree state would make the sealed identity unreproducible (`preflight.py:300` `check_package_clean`).
- **R-C2** Drifted tool inputs — an installed toolchain revision differs from its pin, or generation would run through a local checkout rather than the pinned artifact.
- **R-C3** Unverifiable output — verification does not pass, or leaves a declared channel or verdict not independently verified.
- **R-C4** Fingerprint mismatch — the manifest's recorded pin, the sealed identity document, and the package's own contract do not agree (`manifest.py:442,453`; `identity.py:288`).
- **R-C5** Missing declared keys or constraints, or ambiguous candidate lineage — a declared axis key, objective channel, or constraint identity is absent from the package (`preflight.py:161`), or the request does not resolve to exactly one candidate.
- **R-C6** `[HARD]` Failure is reported, never repaired. `[INHERITED: epic Item 3 Out of Scope]` The seam does not change the model, sysml-codegen, teax, or study semantics to make a candidate pass, and does not relax a threshold or a tolerance.
- **R-C7** `[INHERITED: epic Item 3 Scope 3]` No in-place mutation of a committed study record or its evidence. A committed record is immutable; corrections go to an addendum, which is the study's own procedure and not this seam's business.
- **R-C8** `[INFERRED]` A refused run leaves no half-promoted state: no manifest re-pinned to a package that failed a later gate, no candidate reference a reader could mistake for verified. Whether that is achieved by ordering, by staging, or by rollback is design's.
- **R-C9** `[INHERITED: concept-design § Native seams; epic Item 3 Scope 1]` Lineage mismatch — the candidate that comes out is not the lineage the request named. Expected lineage is a required input (R-A1); a candidate that is internally consistent and verifies cleanly but does not correspond to the audited work the caller named is a `BLOCKER`, not a candidate. This is the Problem section's Item 6 failure one level up: a manifest and a package that agreed with themselves and not with each other, caught only when a study tripped over it.

### D. Identity stability

- **R-D1** `[INHERITED: epic Item 3 SC3]` Re-running on unchanged inputs returns the same candidate identity. The seam does not mint a second, conflicting one.
- **R-D2** `[INFERRED]` "Unchanged inputs" is defined by what the producers already digest — package contents, indicator-input read set, tool source digest, toolchain revisions — not by a new identity scheme invented here. If a digest the producers already compute moves, the inputs changed and a new identity is correct.
- **R-D3** `[INFERRED]` If a re-run produces a different identity while the recorded inputs claim to be unchanged, that is a `BLOCKER` (it is R-C4, fingerprint mismatch, seen from the other side), not a silently accepted new candidate.

### E. Evidence and citability

- **R-E1** `[INHERITED: epic Item 3 Scope 4]` The seam deposits one concise integration return that a human or a goal agent can cite, and that a study can consume without re-deriving the sequence.
- **R-E2** `[INFERRED]` The return carries what a downstream reader needs to check it without re-running: which gates ran, in what order, what each returned, and where each producer's own output sits. It carries this by reference, per R-B3.
- **R-E3** `[INHERITED: MR-4 / CLAUDE.md § Traceability]` Every identity and digest in the return resolves — to a repo path, a commit, or a producer's output file. A bare number with no home is not evidence.
- **R-E4** `[INFERRED]` The return records the toolchain revisions it ran under, because a candidate's meaning depends on them. This also stands in for a known producer defect: `verify.py` writes `teax.revision: "unrecorded"` (`DISCOVERY_LOG.md` `20260821-power-cycle-ab#8`, still open, home `scripts/study/verify.py`). The seam recording the revision does not discharge that row (R-F5).

### F. Boundaries the seam observes

- **R-F1** `[INHERITED: epic Item 3 Out of Scope]` The seam does not commit, push, or close modeling work, and does not choose among multiple valid model designs. Those stay with the owner and the modeling PM.
- **R-F2** `[INHERITED: epic Item 3 Out of Scope]` No goal-side effects ledger, no idempotency wrapper, no second verification implementation. R-D1 is satisfied by producer-computed identity, not by a new control-plane mechanism. `[OWNER, epic § Hardening rule]` No hardening-path mechanism enters the first build without a recorded run failure that promotes it.
- **R-F3** `[INHERITED: align.md — AGENT-grade orchestrator reading]` Changes needed inside pinned sysml-codegen, teax, or agentic-mbse are upstream filings, never in-repo edits.
- **R-F5** `[INFERRED]` A defect in an in-repo producer under `scripts/study/` that the seam works around is recorded against that producer's existing home — an open `DISCOVERY_LOG.md` row or a BACKLOG row — not absorbed silently into the seam. R-B2 freezes those files; R-F3 routes pinned-tool defects upstream; without this clause an in-repo producer defect has no route back to its owner and the workaround becomes permanent by omission.
- **R-F4** `[INHERITED: align.md — AGENT-grade orchestrator reading]` The calc-then-compare constraint form that `scripts/study/indicators.py:469` and `verify.py:193` cannot parse (BACKLOG Flagged row) is not fixed here. The seam surfaces the native gate's result as-is.

### G. Testing

- **R-G1** `[INHERITED: epic Item 3 Deliverables]` Integration fixtures and tests cover three shapes: a successful candidate, a gate failure, and identity stability across a re-run.
- **R-G2** `[INHERITED: epic Item 3 SC5]` Model-family, dependency-provenance, and affected study regressions pass alongside the new tests.
- **R-G3** `[INFERRED]` Tests are hermetic: no test writes into a tracked package, a tracked manifest, or a committed study record. This is Item 2's F3 finding, learned on the sibling seam (`CURRENT_WORK.md:18`), applied before it is repeated.
- **R-G4** `[INFERRED]` The gate-failure test drives a real refusal from a real producer, not a mocked one. A seam that only knows how to report simulated failures has not been shown to fail closed.

## Non-Goals

- Changing sysml-codegen, teax, the model, or study semantics so a candidate passes. `[INHERITED: epic Item 3]`
- Automatic commit, push, or modeling-item close. `[INHERITED: epic Item 3]`
- Selecting among multiple valid model designs. `[INHERITED: epic Item 3]`
- A goal-side effects ledger, idempotency wrapper, or duplicate verification implementation. `[INHERITED: epic Item 3]`
- Fixing the calc-then-compare parser limitation. Out of scope: it stays flagged in BACKLOG and is surfaced as-is, because the seam's job is to invoke the producers' gates and report them, not to extend what they can parse. `[INHERITED: align.md]`
- Running or interpreting a study. The seam hands over a candidate; `study.execute` and `study.read` are separate seams. **Boundary note** `[INFERRED]`: executing the baseline point and any probe run that `preflight.py gates` and `verify.py` themselves require is *inside* the seam, not a study. A study is a declared question with axes, arms, a record, and findings; running a gate's own input is none of those. Item 6 invokes the seam and then runs a study against the returned contract (epic Item 6 Scope 1–2), and that split holds under this reading. Stated so design chooses against a boundary rather than inventing one; if the owner reads it the other way, R-B1.7–8 need a caller-supplied baseline instead and Open Question 4 becomes an owner question.
- Editing GOAL_RUNBOOK, DISCOVERY_LOG, or the run-study runbook. Item 1 owns those; this item's operator doc is its own deliverable. `[INHERITED: align.md]`

## Open Questions / Deferred to design

`[AGENT]` The first three are the orchestrator's Align readings, unchallenged, recorded here as the deferrals they are.

- **Entry-surface shape** — CLI script, Python entry point, slash command, or a combination; and how a goal task and a human each reach it (R-A4).
- **Return-artifact format and home** — what the integration return looks like on disk and where it lives (R-A5, R-E1).
- **SC1 fixture strategy** — how to obtain a "known audited model change" for the success-path test without minting new modeling work. The stellarator package and its migration history are the obvious material; whether the fixture replays a past change, applies a throwaway one, or uses a copy is design's call.
- **What the seam runs verification against.** `verify.py` verifies a *store* of executed cases (`verify.py:343` `verify_store`), and `preflight.py gates` needs a baseline result — so both need execution, not just a sealed package. Whether the seam executes a minimal baseline/probe set itself, reuses one the caller supplies, or splits the boundary differently is a design decision. The requirement (R-B1.7–8, SC4) is that the stock gates are the ones that run.
- **Where the seam stops relative to the study.** SC4 requires the candidate to be accepted by the stock study route; whether the seam demonstrates that itself or leaves it to the study is design's.
- **Blocker taxonomy shape.** R-A6 fixes the one distinction the caller's retry rule needs (refused vs. could-not-run). Beyond that: whether the six refusal causes R-C1–C5 and R-C9 appear as typed codes or as prose naming the gate, and how "could not run" is detected per producer, are design's.
- **Currency of the concept-design's "pending native repair" marker.** `goal-strategy-task-harness-design.md:152,156` still labels `integrate` pending and tells slice 5 to use the manual pattern; both go false when this item lands. Retiring that marker is not this spec's to do — the Non-Goals hand shared files to Item 1 and the proof to Item 6 — but it is owed at epic close and is recorded here so it is not found there.
- **Rollback vs. ordering for R-C8.** Whether "no half-promoted state" is achieved by doing the mutating steps last, by staging, or by an explicit undo.

---

## Related Artifacts

- **Epic:** `.project/backlog/epic_goal_strategy_task_harness.md` § Item 3
- **Align:** `.project/active/goal-integration-seam/align.md` (owner rulings and orchestrator readings, 2026-08-26)
- **Required Reading:**
  - `.project/concepts/goal-strategy-task-harness-design.md` § Native seams, § Validation and Handoff
  - `.project/active/run-study-first-consumer/plan.md` — current manual integration referent
  - `.project/completed/20260821_stellarator-model-migration/plan.md` — sealed-package migration and verification path
  - `scripts/study/manifest.py`, `scripts/study/preflight.py`, `scripts/study/verify.py`, `scripts/study/identity.py` — existing gates
  - `tests/models/test_model_family_spines.py`, `tests/test_dependency_provenance.py` — lineage and generated-tree checks
- **Sibling seam (precedent):** `.project/active/goal-research-seam/spec.md` — Item 2, same contract shape
- **Product-lens:** `.project/active/goal-integration-seam/product-lens.md`
- **Design:** `.project/active/goal-integration-seam/design.md` (to be created)

---

**Next Steps:** `/_my_spec_review` in a fresh session, then `/_my_design`.
