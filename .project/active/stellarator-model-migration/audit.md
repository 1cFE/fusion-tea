# Audit: Stellarator Model Migration

**Verdict:** Needs Work
**Audited:** 2026-08-21
**Branch:** `feat/stellarator-model-migration`
**Commit:** `f8bf4f01`

---

## The Point

RUN-STUDY Item 6, the first A/B consumer, must run on the stock teax route rather than an identity this migration retires. This item therefore has to repair and regenerate the stellarator model on pinned sysml-codegen, seal and execute it at runtime contract 2.0.0 without numerical drift, close the CAS27 verification hole, promote the MFE sources without weakening the IFE regression proof, delete the era route whole, and durably file every temporary toolchain workaround upstream. Every model edit must remain classified and traceable; only a Class C finding may stop the cutover.

## Summary

The core migration works: the package seals and strict-loads on stock teax, the model and study suites pass, the recorded baseline/grid/sweep values are unchanged, CAS27 is independently verified, and both model families have census and mutation proofs. Certification is blocked because the owner-required sysml-codegen filings exist only in an uncommitted sibling-worktree diff. The retirement and validation paths also retain fail-open behavior and all five code/test product-drift smells fire.

## Product Judgment

This is the right piece of work: it establishes the stock-route model needed by RUN-STUDY Item 6 and removes the primary era adapter. The product-lens ledger gate is **BLOCKED** by `audit-F1`: a clean sysml-codegen checkout cannot locate the required filings, so the owner-directed “rewrite now, file upstream” obligation is not durably delivered.

All five audit code/test smells fired:

- **Smell 1 — manually synchronized representations.** Canonical, IFE-twin, and MFE-twin source copies must be copied together. Equality tests make drift loud, but project auto-memory explicitly says not to formalize this workaround (`/home/reid/.claude/projects/-home-reid-1cfe-fusion-tea/memory/feedback_workaround_smell_is_bug.md:11-15`). `audit-F2` is lower-authority in the lens ledger, but the hard project feedback keeps the smell unresolved.
- **Smells 3 and 5 — special category and compatibility against purpose.** A runnable glue harness is classified as “historical” so the retired-route guard passes. The owner's deferral in `.project/backlog/BACKLOG.md:26` makes the scope choice visible; it does not make I6/I12 or the test claim true.
- **Smell 4 — downstream internal knowledge.** Verdict meaning is derived from generated constraint-ID text, and the oracle seam hand-authors hash-bearing operand bindings.
- **Smell 6 — route-selecting tests.** Tests exercise the fail-closed helper while the user-facing CLI filters and exports incomplete cases.

The BLOCK and unresolved structural smells independently forbid certification.

## Findings

### Plan completion

- Phases 1–4 are verified. Phase 5 is not certifiable: `tests/study/test_no_retired_identifiers.py:27-37` exempts the runnable handshake, the suite result is 245 passed / 1 skipped rather than the planned zero skips, and the claimed full-tree lint command was not green as written.
- Phase 6 is not certifiable. `/home/reid/1cfe/sysml-codegen/.project/backlog/BACKLOG.md:24-168` contains the required filings only in an uncommitted worktree diff, so a clean checkout loses SC9. `.project/active/stellarator-model-migration/plan.md:450` also claimed the whole dependency-provenance file was green, while the record and this audit ran only two of its three tests.
- `.project/active/stellarator-model-migration/plan.md:485` still contains `[TO BE FILLED DURING IMPLEMENTATION]` above completed phase notes. Remove the stale placeholder when correcting the plan.
- `exploration/stellarator_e2e/generated/IMPLEMENTATION_BACKLOG.md:12-30` still says its two preserved handwritten functions are unimplemented, and its validation/integration checklists remain open at lines 62-65 and 81-94. Correct this through the generator/regeneration path; the sealed artifact must not be hand-edited.

### Spec conformance

- **SC1 — verified.** `exploration/stellarator_e2e/generated/contracts/package_contract.json:158-161` records the sealed fingerprint and runtime contract 2.0.0; strict-load and seal checks pass in `tests/study/test_stock_route.py:76-120`.
- **SC2 — verified for revision `f8bf4f01`.** `exploration/stellarator_e2e/studies/AFTER_MIGRATION_RECORD.md:45-67` records the exact baseline, 948-point grid, 19-point sweep, and five verdicts with zero drift. The internal-ID dependency is a design/integrity finding below.
- **SC3 — partial.** The primary adapter modules and era tests are gone. The executable `handshake_1costingfe.py` still contains retired glue and is excluded from the guard as a historical record, so SC3 remains unchecked.
- **SC4 — verified.** `exploration/stellarator_e2e/studies/AFTER_MIGRATION_RECORD.md:79-91` and `tests/study/test_verify.py:135-146` show CAS27 compared with an empty disclosure list.
- **SC5 — verified.** All preflight gates pass in the stock-route suite; the manifest carries current fingerprints at `exploration/stellarator_e2e/studies/manifest.json:22-23`; `scripts/study/` is unchanged by this item.
- **SC6 — technically verified.** Canonical `models/` contains 22 SysML files, and `tests/models/test_model_family_spines.py:259-291` proves canonical/twin equality and shared-file agreement. Smell 1 still blocks the architecture.
- **SC7 — verified.** The licensed family spine passes with the preserved IFE 23/18 census and both families' mutation proofs in `tests/models/test_model_family_spines.py:256-445`.
- **SC8 — verified.** `models/stellarator_migration_ledger.md:1-41` declares 506 rows: 365 Class A, 141 Class B, and no Class C; the two opaque manual interfaces retain source/ref/basis and pre-rewrite formulas.
- **SC9 — failed.** The required sysml-codegen backlog rows are uncommitted external state, not part of a durable revision. Commit them in sysml-codegen, then append a resolving product-lens block citing `audit-F1`.
- **SC10 — verified.** Runtime results are recorded at `exploration/stellarator_e2e/studies/AFTER_MIGRATION_RECORD.md:116-124`; the every-and-only structural mutations pass in the family spine.
- **SC11 — partial.** Reruns passed: `tests/models` 43/13, `tests/study` 245/1, root acceptance 20/20, `uv lock --check`, Level 1 model validation, and scoped lint. `tests/test_dependency_provenance.py` was 2 passed / 1 not runnable because matching sealed production wheels were unavailable. SC11 remains unchecked.
- Tagged requirements and R5 are met except the durable-filing part of `[NEED]` Q3/R5 Class B. The fixed codegen pin, final seal, two handwritten implementations, D-5 rename, edit classification, canonical promotion, Item 6 ordering, numerical identity, and package-agnostic generic tools were verified. Non-goals were respected.

### Design conformance

- The design is still marked **Draft** and says not to implement from it at `.project/active/stellarator-model-migration/design.md:3,218`. Record its approval or amend it to the implemented decisions before treating it as the certification contract.
- The core implementation broadly follows D1–D15 and I1–I11, subject to the exceptions below.
- `exploration/stellarator_e2e/studies/study_route.py:213-225` violates I7's source-local identity boundary and the instruction to resolve generated identities through emitted contracts. It parses a generated constraint ID instead of reading `source_local_identity`.
- `exploration/stellarator_e2e/studies/oracle_entry.py:120-157` hand-authors hash-bearing constraint/operand bindings that its own contract says cannot be inferred. This is smell 4: correctness depends on downstream knowledge of a generated representation. The producer/platform must publish the needed mapping.
- `tests/study/test_no_retired_identifiers.py:27-37` exempts `handshake_1costingfe.py` even though it remains executable and mutates retired package files at `exploration/stellarator_e2e/handshake_1costingfe.py:150-180,460-466`. This violates I6 and I12; the owner-deferred backlog row records, but does not erase, the deviation.
- D8/D9 formalize manual synchronization across model copies at `tests/model_families.py:1-15,37-80`. Byte-equality tests prevent silent drift, but the project feedback requires this to remain a surfaced platform/source-ownership defect rather than an accepted usage pattern.

### Code integrity

- `exploration/stellarator_e2e/studies/study_route.py:213-225` fails open in three ways: it infers verdict names from constraint-ID text, writes a blank field when a required output channel is absent via `.get()`, and treats an empty verdict set as feasible through `all([])`. Required contract channels and verdict identities must fail closed and come from published contract data.
- `exploration/stellarator_e2e/study/run_design_search.py:117-148` filters to completed cases and exports a partial CSV without rejecting failed/incomplete cases. The route already has a completion guard at `exploration/stellarator_e2e/studies/study_route.py:252-258`; both CLI commands must enforce the same invariant before writing evidence.
- `exploration/stellarator_e2e/run_stellaris_single.py:63-78,106,121-125,157-181` prints `*** FAIL ***` for anchor, oracle, or guard mismatches but does not exit nonzero for those accumulated booleans. A gate command must fail when any numerical gate fails.
- `tests/study/test_verify.py:233-242` skips identity-refusal coverage when the ignored old database is absent. Replace the route-dependent ignored artifact with a deterministic fixture if zero-skip coverage remains the plan requirement.
- No god functions, parameter sprawl, broad exception swallowing, or optional-data defaults were found in the new core route.

---

## Certification

Verified and marked SC1, SC2, SC4–SC8, and SC10. Left SC3, SC9, and SC11 open. Reopened the Phase 5 retired-route/zero-skip/full-lint checks and the Phase 6 upstream-filing/dependency-provenance checks. No parent epic is attached to this bridge item, so no epic checkbox was changed. Updated `CURRENT_WORK.md` to `needs work`.

Validation rerun on `f8bf4f01`: `tests/models` 43 passed / 13 skipped; `tests/study` 245 passed / 1 skipped; root acceptance 20 passed; `uv lock --check` passed; `agentic-mbse validate models --level 1` passed on 22 files; scoped ruff passed. The worktree was clean before the audit writes.

**Not checked:** The one-time 948-point grid and 19-point sweep were not rerun; this pass reviewed their committed record and hashes. The complete Level 2–6 offender-delta characterization was not rerun. The sealed-runner wheel-hash provenance test could not run because its exact production wheel artifacts were unavailable. The 506 ledger rows were counted and sampled against source changes, not reconstructed independently site by site.
