# Spec: Quality Tools and Era Adapter Promotion

**Status:** Accepted (orchestrated review, 2026-08-19)
**Owner:** Reid W
**Created:** 2026-08-19
**Complexity:** HIGH
**Branch:** `feat/stellarator-mbse-demo`
**Epic:** RUN-STUDY, Item 4

---

## Problem

The proof-of-life study passed real mechanical gates: the baseline point reproduced the pinned headline, the committed package was byte-untouched after every run, sampled points matched an independent oracle at rel < 1e-9 with verdicts re-derived, the declared axis expansions were checked against the package's own input keys, and the three dead schema fillers were asserted dead. All of it lives in one 450-line file, `exploration/stellarator_e2e/study/run_design_search.py`, mixed with stellarator-specific glue, proposal construction, CSV export, and execution. The next study on this package — or the first study on any other — starts from zero. **[INHERITED: `.project/concepts/run-study-skill-design.md` Problem; grade: owner]**

Two things in that file are not merely unshared, they are wrong in a way that matters.

**The loader returns a fingerprint it did not earn.** `GlueAwareLoader` accepts a package whose two glue-edited files differ from their sealed hashes, then returns `seal["executable_fingerprint"]` — the sealed value — as the study definition's executable identity (`run_design_search.py:184`). teax's whole lineage discipline rests on that identity: a store refuses to resume under a different executable. Today a glue edit changes what runs and changes nothing about what teax thinks ran. This is the concept design review's C4, and the concept design already names the fix: an **effective executable fingerprint** over the sealed fingerprint, the actual digests of the allowed-modified files, and the adapter's own source. **[INHERITED: `run-study-skill-design-review.md` C4; `run-study-skill-design.md` Required Invariants → Adapter → lineage; grade: owner-accepted]**

**A sealed-hash preflight gate cannot be honest while the adapter exists.** The concept design lists "manifest-fingerprint match" among preflight's gates (`run-study-skill-design.md:118`). Verified on disk 2026-08-19: of 139 sealed artifacts in `contracts/package_contract.json`, exactly two mismatch — `inputs/system_design.json` and `pipelines/mfe_stellarator.yaml` — and the model contract's `semantic_fingerprint` covers neither. Item 3's manifest pins an *indicator-input* fingerprint over the artifacts its trace reads, which is a different question. So this item owes preflight its own gate design, and the honest version of the gate is the effective-fingerprint machinery above rather than a hash match that can only pass by lying. **[HARD]** — forced by the package on disk, not by a document.

The rest is promotion: pull the generic checks out into `scripts/study/preflight.py` and `scripts/study/verify.py`, which name no package and import no adapter; push the era workarounds into a package-local `era_adapter.py` that checks itself and states the condition under which it is deleted whole; and write the package annex the runbook links per step. The gate on all of it is that the promoted route still produces exactly what the proof-of-life produced.

### Item-start probe — the adapter is retained (2026-08-19)

The epic requires probing, at item start, whether the stock teax loader accepts the current package; if yes, the adapter path is deleted from the capability rather than kept dormant. **Probe result: it does not.** Recomputing sha256 over all 139 entries of `artifact_hashes` against the committed tree yields exactly two TAMPERs, the two documented glue-edited files. `runtime_contract_version` is `1.0.0`. A stock `ProvisionalPackageLoader` verifying `strict=True` refuses on those two regardless of which teax revision runs it, so the adapter branch of this item is live and the "absent, not dormant" criterion is discharged by the adapter's stated deletion condition rather than by deleting it now. The probe is cheap and is re-run at implementation, because the package may be regenerated before then (`run-study-skill-design.md:191`, package regeneration is the expected fix path).

## Success Criteria

- [ ] Every mechanical gate the proof-of-life ran survives promotion, each in its designed home: the generic gates in `scripts/study/preflight.py` and `scripts/study/verify.py`, which contain no package name, no key prefix, and no adapter import (grep-checkable); the adapter-owned checks in the adapter.
- [ ] The adapter's self-checks run on every adapter-route execution and fail closed — the dead-filler assertion above all, which is the one proof-of-life gate that moves *into* the adapter rather than into a tool.
- [ ] Preflight refuses to gate a study against a manifest whose declared package facts were pinned to a package generation that is no longer on disk.
- [ ] The promoted route reproduces both committed proof-of-life CSVs — `design_search_R_a.csv` and `availability_sweep.csv` — byte-for-byte, with the committed files themselves unedited.
- [ ] Verification stays stratified by verdict combination, re-derives every verdict, compares channels at rel < 1e-9, and writes a `verification_summary.json` that carries everything the record's `arms[].verification` block needs.
- [ ] The study definition binds to the effective executable fingerprint, never to the bypassed seal. Touching an allowed glue file, or changing the adapter's source, changes the effective fingerprint and the pre-existing store refuses to resume.
- [ ] Four negative cases each fail closed with a message that locates the fault: missing declared key, dirty package, wrong fingerprint, modified-glue resume refusal. A fifth holds the loader's accept-set: a third modified sealed artifact is refused, not accepted.
- [ ] `exploration/stellarator_e2e/studies/ANNEX.md` exists at the path Item 2 pinned and carries the era pin, the oracle parameterization, the glue rungs, the loader exception, the package-specific validity masks, and the adapter's exact deletion condition.
- [ ] Every point still executes through `StudyRunner`; neither tool owns execution.
- [ ] No tool exits non-zero on an interpretive condition; every mechanical failure exits non-zero.

## Known Requirements

### Generic tools — what makes them generic

- **[INHERITED: `run-study-skill-design.md` Required Invariants → Tools; grade: owner-accepted]** No tool exits non-zero on an interpretive condition. Mechanical failures — missing key, identity mismatch, unparseable artifact, absent oracle, incomplete result — always exit non-zero. A broken check and a clean pass never share an exit code, and neither does a broken check and an empty result.
- **[INHERITED: same]** Neither tool contains a package name, a key prefix, or an import of the adapter. Adapter-owned checks run in the adapter. This mirrors Item 3's Invariant 6 and is tested the same way.
- **[HARD]** Both tools read the manifest through `scripts/study/manifest.py` and cite the JSON Schemas under `scripts/study/schemas/` by path plus `schema_version` string. Item 3 owns those files (`run-study-indicators/design.md` D3, D9). This item does not fork, copy, or re-implement the manifest schema, the `indicator-input-fingerprint/v1` recipe, or the `tool-source-digest/v1` recipe.
- **[HARD]** Any manifest change this item needs is an **additive amendment coordinated with Item 3**, not a local edit. Exactly one amendment is pre-authorized: the oracle object's `{"kind": "cli", …}` variant, which Item 3's D6 anticipates and which leaves existing `python_callable` manifests valid.
- **[HARD]** No era, glue, or allowed-modified-file fact enters the manifest. Design Principle 4 splits package facts by kind: stable declarative facts to the manifest, era workarounds to the adapter (`run-study-skill-design.md:65,126`). The manifest must stay deletable-adapter-proof — deleting the adapter must not require a manifest edit.
- **[INFERRED]** Both tools emit machine-readable results the record can snapshot without re-running them: preflight emits a pass/fail result per named gate (record §9 requires it — `run-study-contract/design.md:210`), and verify emits `verification_summary.json` plus the command, tool revision, sampling scheme, and tolerance the snapshot's `arms[].verification` block carries (`run-study-contract/design.md:254`, MF5).
- **[INFERRED]** Tool revision is reported the way Item 3 reports it — a named digest recipe over a named file list, never a bare hash — so a record's tool revision means the same thing across all three tools.

### `preflight.py` — the four gates

- **[INHERITED: `run-study-skill-design.md:118`]** **Declared-key validation.** Every key in the study's declared axis groups exists in the package's inputs; a key that resolves only to a produced channel is reported as a computed quantity, not as absent (policy §2.1). Suffix-sibling candidates are reported as advisory warnings and never merged into membership. The declaration is Item 3's `study-axis-declaration/v1` file; preflight consumes it, and does not re-derive group membership.
- **[HARD]** **Identity gate, honest by construction.** The gate must never assert a sealed-hash match while allowed-modified files differ on disk. It must fail when any sealed artifact *outside* the declared allowed-modified set differs; fail when the identity the study definition binds to differs from the identity recomputed from the package as it stands; and fail when the package-supplied identity input is missing or malformed. It must reach this without importing the adapter. *(How the identity input reaches preflight is a design decision — see Open Questions.)*
- **[INHERITED: `run-study-skill-design.md:191`, System Confidence "dangerous combinations"; epic Item 4 scope 1]** **Manifest-currency gate.** Preflight fails when the manifest's declared package facts — baseline, ties, oracle, objective catalog — were pinned against a package generation other than the one on disk. This is the half of the epic's "manifest/package fingerprint gate" that the honest identity gate above does not cover, and the design states its consequence directly: after regeneration, ties and baseline are re-declared against the new fingerprint and *preflight fails until they are*. Item 3's tooling does not close it — `indicators.py` pins only the artifacts its own trace reads, and `manifest.py`'s identity check is package-name equality. Note the deliberate asymmetry with Item 3: recorded-provenance drift is a non-gating warning there and a gate here, because indicators report facts while preflight is the gate that stands between a stale declaration and an executed study.
- **[INHERITED: `run-study-skill-design.md` Required Invariants → Tools, marked **now**]** **Baseline headline gate.** An executed baseline point reproduces the manifest's pinned headline channel at rel < 1e-9 and reproduces the manifest's pinned verdicts. Preflight owns the gate; it does not own the execution that produces the point.
- **[INHERITED: same]** **Package-cleanliness gate.** The committed package tree is git-clean, checked after every run and after every verify — not only before. The proof-of-life ran this gate at three sites (`run_design_search.py:358,414,443`) and that placement is deliberate: a mutation introduced by a run is exactly what a pre-run check cannot see.

### `verify.py` — the generic sampler

- **[INHERITED: `run-study-skill-design.md:119`]** **Stratified sampling.** At least one row per observed verdict combination, remainder random, seeded, with the seed and the scheme recorded. The proof-of-life's own note says why: a plain random sample can miss a 32-row stratum entirely (`run_design_search.py:378-380`). This is the lesson the concept design routes into the tool as its default (`run-study-skill-design.md:183`).
- **[HARD]** **The oracle is invoked through a generic contract.** verify.py resolves the oracle from the manifest's typed oracle object (Item 3 D6) and calls it with a point and receives named channel values. The package-side mapping — which qualified entry keys become which oracle inputs, which oracle output names correspond to which package channels — is package-owned and lives on the package side of that seam, never as tool knowledge. Today's oracle has no such seam: `verify_stellaris.py` is a module with `compute()` over a module-global `IN` dict, and its `__main__` prints the fixed baseline only. This item adds the package-owned entry point and amends the manifest's oracle field additively.
- **[INHERITED: `run-study-skill-design.md:119`]** **Channels at rel < 1e-9**, with the worst observed deviation recorded.
- **[HARD]** **Verdicts are re-derived from the package's own predicate declarations**, not from thresholds hard-coded in the tool. The proof-of-life read `recirc_ok`'s threshold and the wall-load limit by literal key name (`run_design_search.py:367-370`); a generic tool cannot. The operator, operand classes, and literal bounds are in `contracts/model_contract.json` `predicate_ir`, which Item 3 already reads and reports.
- **[INFERRED]** **The summary is a superset of what worked.** Every field in the committed `verification_summary.json` survives — sampled rows, seed, worst channel relative deviation, sampling scheme, channels checked, tolerance, verdicts-re-derived, package git-clean, and the glue note — plus whatever `arms[].verification` additionally needs.
- **[INHERITED: `run_design_search.py:411-413`, `run-study-skill-design.md:203`]** **Glue honesty is mandatory output, not a comment.** Any input fed identically to both the package and the oracle is named in the summary as not independently verified. The CAS27 `special_materials` rung is the live case: it is glue-fed on both sides, so oracle parity verifies the package's arithmetic *given* that value and says so.

### The era adapter — `exploration/stellarator_e2e/studies/era_adapter.py`

- **[INHERITED: `run-study-skill-design.md:126`]** The adapter is package-local, named temporary, and is the **only** home for: the loader exception, the glue rungs g1–g3, the self-checks over its own glue (the dead-filler assertion above all), and the era-pin prerequisite. Generic tools never assert an adapter-owned fact.
- **[HARD]** **The loader accept-set is exactly `{TAMPER on the two documented glue-edited files}`.** Any other diagnostic — a different file, a different diagnostic kind, an era-version mismatch — still refuses. This is not a relaxation of sealing; it is a precisely scoped exception, and its scope is asserted by a negative test.
- **[HARD, from review C4]** **The adapter computes the effective executable fingerprint** — a digest over the sealed `executable_fingerprint`, the actual digests of the allowed-modified files, and the adapter's own source — and the study definition binds to *that*. The sealed fingerprint is never reused as the identity of a route that bypassed the seal. Any change to a glue file or to adapter behavior is therefore a new teax lineage, refused at store open or resume rather than silently mixed.
- **[INHERITED: `run-study-skill-design.md:126`]** **The deletion condition is stated exactly, in the adapter and in the annex**: the stock loader accepts the (regenerated) package. When it does, the adapter is deleted whole, the sealed fingerprint becomes the identity again, and nothing else changes. There is no partial retirement and no dormant compatibility branch.
- **[INHERITED: epic Item 4 scope 3; grade: owner]** If the item-start probe ever comes back positive, the adapter is **absent**, not retained as dormant code, and the promotion-equivalence check retires with it.
- **[INHERITED: `run-study-skill-design.md:126`]** The era pin is a **prerequisite the adapter asserts**, not merely a fact it records: the adapter checks that it is running under the pinned era teax — worktree `/home/reid/1cfe/teax-v1-era` at `fa0e06a` — and fails closed if it is not. The annex records the pin and states that current teax main's refusal of the v1.0.0 seal is principled and is not to be chased upstream.
- **[INFERRED]** The adapter **emits its own facts as data the record can snapshot** — the effective executable fingerprint with its three inputs, and the glue ledger's rungs. Item 2's snapshot is arm-scoped and carries both (`run-study-contract/design.md:239,254,258`), this item owns both, and neither may enter the manifest. Without an emission seam the executor hand-copies them out of the annex, which is exactly the drift the snapshot rule exists to prevent. *(The document's shape is a design decision — see Open Questions.)*

### The package annex — `exploration/stellarator_e2e/studies/ANNEX.md`

- **[OWNER, via orchestrator 2026-08-19]** This item authors the annex file and its content, at the path Item 2's design D9 pinned (`run-study-contract/design.md:93`). Item 2 owns the per-step link; this item owns what the link points at. This supersedes both the Item 2 spec line routing the annex to Item 3 and Item 3's own non-goal restating it.
- **[INFERRED]** Annex content, one section per runbook step that links it: the era pin and why it exists; the oracle's parameterization (how a point becomes oracle inputs and what the oracle returns); the glue ledger rungs g1–g3 with what each supplies that the model does not; the loader exception and its exact accept-set; the package-specific validity masks — the `R > a + 2.25 m` radial-build stack exclusion is one, and it is a derived geometric bound from held-fixed inputs, not a design screen (`run_design_search.py:113-118`); and the adapter's deletion condition.
- **[INHERITED: `run-study-skill-design.md:65`]** Annex content is linked, never inlined into the universal runbook. Nothing in the annex is a rule; it is package fact.

### Promotion equivalence and the negative proofs

- **[HARD, `run-study-contract/design.md:55`]** The proof-of-life directory `exploration/stellarator_e2e/study/` stays as the pre-capability record. Its CSVs, its `verification_summary.json`, and the script that produced them are executed evidence and are not edited to fit the promoted tools. The promoted route is therefore a **new** study-local definition that reproduces them, not a refactor in place.
- **[INHERITED: `run-study-skill-design.md` Validation Strategy]** **Promotion equivalence (one-time, adapter route only):** the stock lifecycle plus the adapter, driven by the promoted tools, reproduces both committed CSVs byte-for-byte. This gate is valid only for this package and retires with the adapter.
- **[INHERITED: same]** **Preflight negatives:** a missing declared key, a dirty package, and a wrong fingerprint each exit non-zero with a message that names the fault.
- **[INHERITED: same; concept design's unowned proof 5]** **Lineage refusal:** touch one of the allowed glue-edited files, and the pre-existing store refuses to resume because the effective fingerprint changed. The same test in the other direction — change the adapter's source, same refusal — closes the second half of the effective-fingerprint definition.
- **[INFERRED]** **Accept-set negative:** modify a third sealed artifact and the adapter's loader refuses, proving the exception did not widen into a blanket seal bypass.

### Execution stays where it is

- **[INHERITED: `run-study-skill-design.md:116`, review M6; grade: owner-accepted]** Every point executes through the stock teax lifecycle via `StudyRunner`. The route for the adapter case is the study-local direct-API definition (`StudyRunner` + `PreparedListStrategy`), because the era CLI can neither inject a loader nor build coordinated prepared blocks. The tools gate and verify; they never run points, and no second execution facade or hand-rolled sweep loop is introduced.

## Non-Goals

- A second execution facade, a generic runner, or any hand-rolled sweep loop.
- Package knowledge — names, key prefixes, thresholds, oracle field names — inside the generic tools.
- Upstream changes to teax or sysml-codegen, and any attempt to make current teax main accept the v1.0.0 seal. Its refusal is principled.
- Interpretive gating: no tool refuses or re-labels a study on the basis of indicators, framings, or study outcomes.
- Authoring `manifest.py`, the manifest schema, the JSON Schemas, `indicators.py`, or the stellarator `manifest.json` — Item 3.
- Authoring `SKILL.md`, `runbook.md`, the record template, or the annex *link* — Item 2.
- Migrating `run_stellaris.py`'s or `verify_stellaris.py`'s existing oracle knowledge into the manifest. Those scripts keep their own knowledge; this item adds one entry-point seam (`run-study-skill-design.md:193`).
- Running a new study, plotting, or reporting. This item proves the tools against an already-executed study.
- Measuring or reducing the cost of conservatism in the trace (Item 3's non-goal, inherited).

## Open Questions / Deferred to design

- **How an executed baseline point reaches preflight.** The baseline gate is preflight's, but preflight neither executes points nor imports the adapter, and the point must run through `StudyRunner` under the adapter's loader. Candidates: preflight consumes an already-executed result (store or exported row) and compares it to the manifest pin; or preflight takes a prepared-evaluator handle supplied by the caller. The second keeps the gate pre-run but pulls preflight closer to execution. Design decides, along with where the gate sits in the runbook's order.
- **The shape of the package-supplied identity seam.** The adapter computes the effective fingerprint; generic preflight must gate on it without importing the adapter. Likely a small identity document the adapter emits (sealed fingerprint, allowed-modified files with their actual digests, adapter source digest, the resulting effective fingerprint) that preflight reads as data. If so, that document needs a schema and a name, and the question of whether it is Item 3's schema directory or this item's is a coordination call. Open with it: whether the same document also carries the glue ledger the record snapshots, or whether the adapter emits two.
- **Where the package-owned oracle entry point lives** — a CLI added to `verify_stellaris.py`, or a separate shim module beside the manifest — and whether the manifest's oracle field takes the pre-authorized `{"kind": "cli"}` form or stays `python_callable` with a defined generic signature. Weigh keeping the independent oracle untouched against not scattering package oracle knowledge.
- **Whether verify.py samples from the study store (`StudyQuery`) or from exported CSVs.** The proof-of-life sampled CSVs; the store is the primary evidence and the CSV is a derived export. Sampling the store is more direct; sampling the CSV verifies the artifact the record actually ships.
- **The exact `verification_summary.json` field list**, once Item 2's snapshot field list is written out in full at its plan stage.
- **Default sample size and seed, and whether they scope per study, per arm, or per exported artifact.** The proof-of-life used K=12 per CSV with a fixed seed.
- **Where the promotion-equivalence study definition lives, and whether it is kept as a regression test or retired as one-time evidence.** It retires with the adapter either way.
- **Whether preflight and verify share a small internal module** (package loading, store access, result shaping) or stay two independent scripts.

---

## Related Artifacts

- **Epic:** `.project/backlog/epic_run_study_capability.md` — Item 4
- **Required Reading:** `.project/concepts/run-study-skill-design.md` (Tools, manifest and adapter, Architectural Bets, Required Invariants, Validation Strategy, Edge Cases) · `.project/concepts/run-study-skill-design-review.md` (C4, C5, M6, m3) · `exploration/stellarator_e2e/study/run_design_search.py` · `exploration/stellarator_e2e/study/verification_summary.json` · `exploration/stellarator_e2e/pkg/stellarator_tea/contracts/package_contract.json`
- **Upstream seams:** `.project/active/run-study-indicators/design.md` (Item 3 — `manifest.py`, manifest schema, fingerprint recipes, typed oracle object, `scripts/study/schemas/`) · `.project/active/run-study-contract/design.md` (Item 2 — record §9 preflight results, snapshot `arms[].verification`, annex path D9)
- **Item-start probe:** recorded in Problem above; re-run at implementation.
- **Product-lens:** `.project/active/run-study-quality-tools/product-lens.md` — BLOCKED on F1/F2, both fixed in this revision; gate CLEAR. Epic RUN-STUDY's live gate is CLEAR.
- **Design:** `.project/active/run-study-quality-tools/design.md` (to be created)

---

**Next Steps:** After approval, proceed to `/_my_design`.
