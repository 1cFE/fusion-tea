# Audit: Stellarator Model Migration

**Verdict:** Certify
**Audited:** 2026-08-21
**Branch:** `feat/stellarator-model-migration`
**Commit:** worktree repairs atop `c4c48ebe`

---

## The Point

RUN-STUDY Item 6, the first A/B consumer, must run on the stock teax route rather than an identity this migration retires. This item therefore has to repair and regenerate the stellarator model on pinned sysml-codegen, seal and execute it at runtime contract 2.0.0 without numerical drift, close the CAS27 verification hole, promote the MFE sources without weakening the IFE regression proof, delete the era route whole, and file every temporary toolchain workaround upstream. The owner has kept the upstream commit as a separate task. Every model edit must remain classified and traceable; only a Class C finding may stop the cutover.

## Summary

The migration and its audit repairs work. The package seals and strict-loads on stock teax, CAS27 is independently verified, both model families retain their census and mutation proofs, and all SC1–SC11 criteria are now checked. The repaired evidence route resolves verdict names through the emitted contract, refuses incomplete data before publishing either study CSV, and returns a failing status when any single-point numerical gate fails. Real reruns completed the 948-point grid and 19-point sweep; both regenerated CSVs were byte-identical to their committed records.

## Product Judgment

This is the right piece of work: it establishes the stock-route model needed by RUN-STUDY Item 6 and removes the primary era adapter. The fresh product-lens pass is **CLEAR**. Its re-derived falsifier is that missing data, a failed study case, or a failed single-point comparison must not publish evidence or report success; the repaired commands satisfy that boundary.

- **Smell 1 — manually synchronized representations.** The owner retains the byte-identical exploration copies until the demo epics finish. B1 records that deferral and the equality test remains the interim guard.
- **Smells 3 and 5 — special category and compatibility against purpose.** The owner accepts the historical handshake exception for this item's scope and defers its rewrite to the demo epic.
- **Smell 4 — downstream internal knowledge.** B2 is fixed: verdict meaning now comes from the emitted contract's `source_local_identity`. The separate handwritten operand table remains owner-accepted under B3 for demo verification only.
- **Smell 6 — route-selecting tests.** B4 is fixed: the helpers and both user-facing command paths now share the same completion and pre-publication validation boundary, with command-level failure tests.

No unresolved product smell blocks certification. The prior owner dispositions remain recorded rather than being regraded by this audit.

## Blocking Resolution Record

These IDs record the owner decisions and final repair status. Later corrections must amend the matching entry rather than creating a second version of the same decision.

**Walkthrough provenance:** `[OWNER-VERBATIM 2026-08-21]` “ONE BY ONE -- do not dump them all at once” and “I need more context. no loaded terms. do not assume I know what is going on -- explain it.” This governed the completed blocker walkthrough.

### B1 — Give each model file one source of truth

**Context.** A model file is a `.sysml` text file that sysml-codegen reads to build the executable Python package. The repository stores the complete 22-file model collection under `models/`. It also stores family-specific copies for the two runnable examples:

- Complete collection: `models/library/**` and `models/designs/**` (22 files).
- IFE example copy: `exploration/ife_e2e/models/**` (11 of those files).
- MFE/stellarator example copy: `exploration/stellarator_e2e/models/**` (14 of those files).

Most files therefore have two committed locations. For example, `models/library/analyses/mfe_power_balance.sysml` is repeated at `exploration/stellarator_e2e/models/analyses/mfe_power_balance.sysml`. Three shared files have three locations. For example, `economic_parameter.sysml` exists at `models/library/foundation/economic_parameter.sysml`, `exploration/ife_e2e/models/foundation/economic_parameter.sysml`, and `exploration/stellarator_e2e/models/foundation/economic_parameter.sysml`. The audit verified that these copies currently have identical hashes. `exploration/stellarator_e2e/STAGED_MODELS.md:3-5` says the copies exist so each example has a self-contained input directory for package generation.

**Issue.** Nothing is out of sync today. The concern is the editing process: the project tells a developer to edit one copy and manually copy the same change to the other location. `tests/models/test_model_family_spines.py:265-291` catches a missed copy when that test runs, but both files remain independently editable in Git.

**Risk if unresolved.** Someone can edit `models/` and then generate the stellarator package from the unchanged exploration directory before running the equality test. That run would use the old model. The test reduces the chance of merging mismatched copies, but it does not prevent a stale local generation or remove the repeated maintenance step.

**Required action.** No structural change during this migration. Keep the committed exploration copies and their equality test until the demo epics finish. Treat `models/` as the long-term home. When the demo epics finish, revisit removal of the exploration copies and generation of family-specific input trees from `models/`; that later cleanup is not part of this item.

**Discussion status:** **DEFERRED — owner, 2026-08-21.** `[OWNER-VERBATIM]` “the reality is that `models/` is the long-term home. `exploration` was just for our rapid iteration for the demo. we need to leave them as-is until we finish the demo epics.” B1 is resolved for this migration and does not block certification.

### B2 — Do not write a valid-looking study row from missing data

**Context.** A study runs the reactor model at many proposed designs. Each completed design becomes one CSV row. The row contains the proposed dimensions, eight calculated results such as energy cost and fusion power, five model checks, and one final `feasible` value. Here, `feasible` means all five model checks returned `satisfied`.

The runtime identifies a model check with a generated value such as `stellarator_09__stellaris__beta_ok__82b78aad420730d5`. The generated package also contains a JSON description of that check at `generated/contracts/model_contract.json:22-35`. That description gives its stable, human-facing name: `beta_ok`. The migration's second acceptance checkbox, SC2, says before/after results must match using this stated name rather than by assuming how the longer generated value is formatted.

**Issue found by the audit.** The old CSV writer had three separate gaps:

1. It did not read the stated name from the generated JSON description. It split the long generated value on `__` and assumed the second-to-last piece was the name.
2. For each of the eight required calculated results, it used `case.outputs.get(channel)`. A missing result therefore became a blank cell instead of stopping publication.
3. It set `feasible` with Python's `all(...)`, so an empty verdict set was marked feasible.

The recorded successful runs did not contain missing data. This finding concerned how the evidence writer behaved when upstream execution was incomplete or its generated naming format changed.

**Risk closed.** A partial row can no longer look valid or influence the selected optimum. Missing channels and any verdict-set mismatch raise `RouteError`, and generated IDs are never parsed for their meaning.

**Action taken.** `study_route.py:214-296` loads the emitted catalog, requires exactly five checks with unique nonempty `source_local_identity` values, requires the case's verdict IDs to match that catalog exactly, and requires all eight output channels before it builds rows or writes bytes. `test_study_publication_fail_closed.py:37-97` covers opaque generated IDs, one missing result, no checks, a missing check, and an unexpected check without replacing prior evidence. Real regeneration produced byte-identical radius and availability CSVs.

**Discussion status:** **FIXED AND VERIFIED — 2026-08-21.** `[OWNER-VERBATIM]` “this is not related to the current item, but should be fixed now.” The owner-added scope is complete.

### B3 — The independent checker needs a handwritten wiring table

**Context.** The model itself reports whether each of its five checks passed. The verification step does not simply trust that answer. It reads the check's formula from the generated package, obtains the required numbers from the recorded run, calculates the answer again, and compares that independently calculated answer with the model's answer.

**Lifecycle clarification from the owner walkthrough.** This is not a production verifier. It is temporary demo verification infrastructure. `scripts/study/verify.py` was written as reusable code and the current runbook still calls it, but the later owner Align recorded at `.project/backlog/epic_run_study_capability.md:392` says: “oracle verification runs for this demo only, then leaves the study contract.” The migration used it once, and the remaining demo study may use it again. Future production studies are not required to use it. In plain terms: it is not literally single-execution code, but it belongs on the one-time/demo side of the boundary rather than the production side.

For example, the beta check is the comparison `beta <= beta_limit`. To calculate it again, the verifier must know where the recorded run stored `beta` and `beta_limit`. For the net-positive check, the formula calls its value `net_electric`, while the recorded run stores that value under the power-balance result `pb__p_net`.

The generated JSON describes the formula and its operand names, but it does not state where every operand's runtime value is stored. A handwritten table at `oracle_entry.py:120-157` supplies the missing connections. It covers nine values used by the five checks. The table is indexed by long generated check identifiers such as `stellarator_09__stellaris__beta_ok__82b78aad420730d5`.

**Issue.** The code generator determined these connections when it built the executable package, but it did not include them in the generated JSON description. A person therefore reconstructed and recorded the same connection knowledge in the verification adapter. This is the only reason the independent checker can find the right values.

The current table is not known to be wrong. It has useful safeguards: a missing table entry stops verification; tests confirm all five checks and all nine values resolve; a bad key stops verification; and the verification record includes a hash of the whole table. A regenerated identifier would normally cause a loud missing-entry failure. The remaining concern is a human changing the table to a different key that exists but represents the wrong value.

**Risk if unresolved.** During the remaining demo work, a package regeneration requires a person to inspect and possibly update this table. If they connect an operand to the wrong existing value, the structural tests can still pass. If both values happen to produce the same pass/fail answer at the sampled designs, the independent check can also appear to pass. This can weaken the demo's verification evidence. It is not a continuing production-runtime risk once oracle verification leaves the study contract.

**Required action.** Keep the current handwritten table and its existing safeguards for the remaining demo work. Do not expand this migration into sysml-codegen changes, a codegen re-pin, or extra production-verification work. When the demo ends, oracle verification leaves the general study contract under the existing owner decision; this audit creates no implied production follow-up.

**Discussion status:** **ACCEPTED FOR THE REMAINING DEMO — owner, 2026-08-21.** `[OWNER-VERBATIM]` “production model verification is a massive thing, not in scope” and “accept the current table for the remaining demo.” B3 is resolved and does not block certification.

### B4 — The demo command writes a smaller CSV when some designs fail

**Context.** The stellarator demo contains a command at `exploration/stellarator_e2e/study/run_design_search.py`. It runs 948 proposed reactor designs for the radius search and 19 proposals for the availability sweep. Teax records a state for every proposal, such as `completed` or `failed`. A complete study should write a CSV only when every expected proposal completed.

This is demo infrastructure, not a production study runner. The command writes new stores and CSVs under `study/_work/`, which Git ignores. It does not overwrite the committed July proof-of-life CSVs beside the command. The package also has direct helper functions at `studies/study_route.py:252-281` that already stop when any proposal failed; the tests use those safer helpers.

**Issue found by the audit.** The old `run` and `export` paths selected only completed cases and published the smaller set. The `run` path also wrote the radius CSV before its baseline gate.

**Risk closed.** A failed case in either study now stops the command before either CSV is created or replaced, so a partial design space cannot be presented as new demo evidence.

**Action taken.** `run_design_search.py:111-155` makes both commands validate completion for both studies, the baseline, package cleanliness, and both in-memory row sets before either write. `test_study_publication_fail_closed.py:107-171` plants a failed case in the second study while an old radius CSV exists and the availability CSV does not; both command paths raise without changing either publication. The real `run` and `export` paths completed 948/948 and 19/19 cases.

**Discussion status:** **FIXED AND VERIFIED — 2026-08-21.** `[OWNER-VERBATIM]` “fix it with B2.” The shared implementation and command-level tests are complete.

### B5 — Make the single-point gate's exit status truthful

**Context.** `run_stellaris_single.py` is a demo/regression command, not part of the production model runtime. It runs one fixed stellarator design and checks four groups of results at `run_stellaris_single.py:63-181`: nine familiar headline values (the anchors), the model's five constraint verdicts, detailed numeric agreement with the demo's separate calculation, and three synthetic CAS72 boundary cases. The five verdict checks already use assertions and therefore make the command fail when they are wrong. Separate assertions also prove that the synthetic inputs actually reach the intended CAS72 boundary cases.

**Issue found by the audit.** Three result groups only affected terminal text. Anchor, detailed numeric, and CAS72 comparison failures could still leave Python with a zero exit status.

**Risk closed.** CI and calling scripts now receive a nonzero status whenever any accumulated numerical gate fails. This remains a demo/regression command and creates no production verification requirement.

**Action taken.** `run_stellaris_single.py:272-290` runs all three boolean gate families, combines them in `main()`, and exits 1 unless all three pass. The existing generated-verdict and guard-live assertions remain at `run_stellaris_single.py:106-133,243-267`. `test_single_point_gate.py:22-50` proves each false family exits nonzero and the real green subprocess exits zero.

**Owner decision — FIXED AND VERIFIED (2026-08-21).** The owner kept this as a demo/regression gate. Its exit status is now truthful, and the green path plus each failure family are covered.

### B6 — Keep closeout validation inside the migration's scope

**Owner correction — NOT A STANDALONE BLOCKER (2026-08-21).** The owner rejected expanding “update these models” into “fully reproduce the entire environment.” The audit had improperly elevated inherited release-environment checks and unrelated historical-tree cleanup into migration requirements.

The recorded model, study, root-acceptance, lock, and Level 1 validation results remain accepted. The optional pre-migration `_work/availability_sweep.db` test may remain skipped; reconstructing the sealed wheel-runner environment is out of scope; the existing explicit retired-identifier test is sufficient; and the migration does not owe cleanup of the old/generated demo tree's 904 lint findings. Post-repair validation is limited to the affected tests and linting the hand-authored files changed by B2/B4/B5.

**Disposition:** Owner-resolved for this migration. B6 does not block certification independently. SC11 closes on the targeted post-repair validation, not on recreating the prior release environment.

### B7 — Make the durable artifacts describe the delivered state

**Context.** The code has been implemented, but three local workflow documents still contain text written before implementation began. A generated package document also looks stale at first glance, but it has a different meaning.

**Actual stale text found by the audit.** The design was marked `Draft` and ended with “Do not begin implementation from this draft” even though implementation was complete. The plan had `[TO BE FILLED DURING IMPLEMENTATION]` immediately above six completed phase records. The spec's related-artifact list said the already-existing design was “to be created.”

**What is not stale implementation state.** `generated/IMPLEMENTATION_BACKLOG.md` lists DT Fusion Power and Levelized Replacement Cost as two “functions to implement.” The pinned generator creates that list solely from calculations it cannot implement automatically (`sysml-codegen/generation/stencils.py:223-262`); it never reads the preserved handwritten files to determine whether a human already completed them. Both listed files contain working implementations, were preserved intentionally, and pass the strict-load and numerical gates. Changing the generator and re-pinning it only to improve this generic wording would be scope creep, while hand-editing the sealed document would invalidate the package hash. No change to that generated file is required for this migration.

**Risk if unresolved.** A later agent can mistake the design for unfinished work or believe the plan still lacks its implementation record. This is a handoff/documentation problem, not a model-runtime risk.

**Action taken.** Local workflow documents only: `design.md` is marked implemented while recording that it was not separately approved/reviewed before implementation, and its obsolete next-stage instruction is replaced by an as-built handoff; the plan placeholder is deleted; and “to be created” is removed from the spec's design link. The generated backlog and sealed package are unchanged.

**Owner decision — FIXED LOCALLY (2026-08-21).** The owner directed: “yes just make the local documentation corrections.” B7 is resolved. This decision does not authorize a `sysml-codegen` change, package regeneration, or a hand-edit to the sealed generated backlog.

## Findings

### Plan completion

- The owner narrowed the Phase 5–6 closeout scope under B6. The optional old-store skip, sealed-wheel runner, broad historical-tree lint, and manual grep are not blockers. The required post-repair tests, changed-file lint, and real study reruns are complete.
- The stale plan implementation placeholder, design `Draft`/pre-implementation handoff, and spec “to be created” note were corrected under B7.
- `exploration/stellarator_e2e/generated/IMPLEMENTATION_BACKLOG.md:12-30` is the pinned generator's list of calculations requiring manual rather than automatic implementation. It does not inspect the preserved handwritten bodies and is not a migration completion tracker. The two bodies are implemented and verified; leave this sealed generated file unchanged.

### Spec conformance

- **SC1 — verified.** `exploration/stellarator_e2e/generated/contracts/package_contract.json:158-161` records the sealed fingerprint and runtime contract 2.0.0; strict-load and seal checks pass in `tests/study/test_stock_route.py:76-120`.
- **SC2 — verified.** `exploration/stellarator_e2e/studies/AFTER_MIGRATION_RECORD.md:45-67` records the exact baseline, 948-point grid, 19-point sweep, and five verdicts with zero numerical drift. The repaired route resolves verdicts through the emitted catalog's `source_local_identity` at `exploration/stellarator_e2e/studies/study_route.py:214-248` and rejects missing or unexpected checks. Fresh 948-point and 19-point reruns produced byte-identical CSVs: radius SHA-256 `0f248b83c104ee69b7ffa63c507d0be82be029b7e64def4a3d80e10166b8022b`; availability SHA-256 `9239bbcd7179ee39a9f187470757ae0389b5e9e1a99efd71d888ce0d50111a70`.
- **SC3 — verified under the owner's recorded scope ruling.** The primary adapter modules and era tests are gone. `/_my_ask_me` Q2 explicitly leaves `handshake_1costingfe.py` as historical evidence with a backlog rewrite; the resulting smell is disposed above rather than silently treated as ordinary production code.
- **SC4 — verified.** `exploration/stellarator_e2e/studies/AFTER_MIGRATION_RECORD.md:79-91` and `tests/study/test_verify.py:135-146` show CAS27 compared with an empty disclosure list.
- **SC5 — verified.** All preflight gates pass in the stock-route suite; the manifest carries current fingerprints at `exploration/stellarator_e2e/studies/manifest.json:22-23`; `scripts/study/` is unchanged by this item.
- **SC6 — verified under B1.** Canonical `models/` contains 22 SysML files, and `tests/models/test_model_family_spines.py:259-291` proves canonical/twin equality and shared-file agreement. The owner retains the synchronized exploration copies until the demo epics finish; that recorded deferral does not block this item.
- **SC7 — verified.** The licensed family spine passes with the preserved IFE 23/18 census and both families' mutation proofs in `tests/models/test_model_family_spines.py:256-445`.
- **SC8 — verified.** `models/stellarator_migration_ledger.md:1-41` declares 506 rows: 365 Class A, 141 Class B, and no Class C; the two opaque manual interfaces retain source/ref/basis and pre-rewrite formulas.
- **SC9 — verified under the owner's recorded delivery ruling.** The required sysml-codegen rows exist at `/home/reid/1cfe/sysml-codegen/.project/backlog/BACKLOG.md:24-168`, and `/_my_ask_me` Q3 explicitly permits them to remain uncommitted for the owner's later commit. The product-lens ledger now resolves `audit-F1` by citation.
- **SC10 — verified.** Runtime results are recorded at `exploration/stellarator_e2e/studies/AFTER_MIGRATION_RECORD.md:116-124`; the every-and-only structural mutations pass in the family spine.
- **SC11 — verified under the owner's B6 scope correction.** The accepted existing reruns remain: `tests/models` 43/13, `tests/study` 245/1, root acceptance 20/20, `uv lock --check`, Level 1 model validation, and scoped lint. Post-repair validation added 43 passed / 1 owner-accepted optional-store skip across the affected stock-route tests, 12/12 new regression tests, scoped Ruff on all five changed hand-authored files, and a clean `git diff --check`. Reconstructing the sealed-wheel runner is not required.
- Tagged requirements and R5 are met. The fixed codegen pin, final seal, two handwritten implementations, D-5 rename, edit classification, canonical promotion, Item 6 ordering, numerical identity, and package-agnostic generic tools were verified. Non-goals were respected.

### Design conformance

- The design now records the truthful history: implemented, but not separately approved/reviewed before implementation. Its decisions remain agent-authored unless individually marked with owner provenance.
- The core implementation follows D1–D15 and I1–I11, subject to the owner-accepted lifecycle exceptions below.
- `exploration/stellarator_e2e/studies/study_route.py:214-296` now follows I7's source-local identity boundary. It resolves generated identities through the emitted contract and validates the complete row before publication.
- `exploration/stellarator_e2e/studies/oracle_entry.py:120-157` hand-authors hash-bearing constraint/operand bindings. Under B3, the owner accepts this table for the remaining demo and rejects expanding this migration into production-verifier or codegen work.
- `tests/study/test_no_retired_identifiers.py:27-37` exempts `handshake_1costingfe.py` even though it remains executable and mutates retired package files at `exploration/stellarator_e2e/handshake_1costingfe.py:150-180,460-466`. This deviates from I6 and I12, but `/_my_ask_me` Q2 explicitly accepts the historical exception for this item and defers the rewrite.
- D8/D9 formalize manual synchronization across model copies at `tests/model_families.py:1-15,37-80`. Under B1, the owner has designated `models/` as the long-term home and retained the byte-identical exploration copies until the demo epics finish.

### Code integrity

- `exploration/stellarator_e2e/studies/study_route.py:214-296` fails closed on catalog cardinality and identity, exact verdict sets, all eight output channels, required axes, and empty row sets before publication.
- `exploration/stellarator_e2e/study/run_design_search.py:111-155` validates both complete case sets, the baseline, package cleanliness, and both row sets before writing either CSV.
- `exploration/stellarator_e2e/run_stellaris_single.py:272-290` combines all accumulated numerical gates into the process status while preserving the assertion gates.
- The fresh explorer audit found no blocker, dishonest abstraction, broad exception swallowing, or failure-hiding default in the repaired surface.

---

## Certification

Verified B2, B4, and B5 and marked SC2 and SC11 complete. All SC1–SC11 criteria are now checked. B1, B3, B6, and B7 remain resolved by the recorded owner decisions; the repairs did not broaden those decisions. No parent epic is attached to this bridge item, so no epic checkbox changed. `CURRENT_WORK.md` now records the migration as certified and RUN-STUDY Item 6 as unblocked.

Post-repair validation on the worktree atop `c4c48ebe`: the new regression tests passed 12/12; the affected stock-route suite passed 43 with 1 owner-accepted optional-store skip; scoped Ruff passed on the five changed hand-authored files; and `git diff --check` passed. The real `run` and `export` commands each accepted 948/948 radius cases and 19/19 availability cases, with baseline LCOE `275.264220042` and 5/5 satisfied checks. Both regenerated CSVs matched the committed records byte for byte. A fresh explorer audit returned **CERTIFY**, and a fresh product-lens pass returned **CLEAR** with no unresolved smell.

**Not rerun:** The full model suite, full study suite, root acceptance pair, lock check, Level 1 model validation, complete Level 2–6 offender-delta characterization, and sealed-wheel provenance environment were not recreated after these scoped repairs. B6 explicitly accepts their recorded results and limits post-repair validation to affected tests and changed-file lint. The 506-row migration ledger was not independently reconstructed site by site in this repair pass.
