# Design Review: Quality Tools and Era Adapter Promotion (RUN-STUDY Item 4)

**Design:** `.project/active/run-study-quality-tools/design.md`
**Spec:** `.project/active/run-study-quality-tools/spec.md` (Accepted)
**Review File:** `.project/active/run-study-quality-tools/design-review.md`
**Date:** 2026-08-19
**Reviewed at commit:** `becee37c` (branch `feat/stellarator-mbse-demo`)

---

## The Point

One good study exists. Every mechanical gate that made it trustworthy — baseline reproduction, package cleanliness, stratified oracle sampling at rel < 1e-9, verdict re-derivation, declared-key validation, dead-filler assertion — is welded into one 450-line package-specific file. The next study on this package, or the first on any other, starts from zero.

Two of those welds are also wrong. The loader accepts a package whose two glue-edited files differ from their sealed hashes and then hands teax the *sealed* fingerprint as the identity of what ran. teax's lineage discipline rests on that identity, so a glue edit changes what executes and changes nothing about what teax thinks executed. And a preflight gate asserting "the manifest fingerprint matches the package" cannot be honest while those two files differ.

So this item owes three things: generic gates that name no package, a package-local adapter that tells the truth about what it bypassed and states the condition under which it is deleted whole, and proof that the promoted route still produces exactly what the proof-of-life produced.

---

## Fundamental Assessment

**Sound, with one component that does not work as designed.**

The core move is right and is the simplest thing that could work: the adapter stops reporting an identity it did not earn and publishes one typed document saying what it bypassed and what identity that produces; generic tools handle that document as data and never import the adapter. The `kind` discriminator making the no-adapter case the degenerate member (D3) is the detail that earns the design its keep — the gate does not rot into an optional branch when the adapter is deleted. Splitting currency (contract fingerprints, which glue edits cannot touch) from identity (recomputed effective fingerprint) is the right decomposition, and it is the honest answer to the gate the spec proved could not be a sealed-hash match. Two of the five bets are probe-confirmed end to end on real era code, which is more evidence than most designs at this stage carry.

I am not recommending Rework. The failures below are in one component (verify's verdict re-derivation) plus a set of contract mismatches with artifacts that were in flight when the design was written and are now delivered. That is revision, not a new foundation.

But one structural smell fires, and it controls the verdict on `verify.py`:

> **A consumer compensating for a producer guarantee.** The design assigns generic `verify.py` the job of resolving each `predicate_ir` operand to a value (B4, design.md:68; procedure step 3, design.md:188). codegen does not emit any binding from a predicate operand to a flat entry key or channel. The design does not say this, and does not say who should own the gap — it quietly hands it to the tool that is forbidden from holding package knowledge. Checked against the package on disk, the job is not doable by name matching, and for one of the five real constraints it is not doable at all. See L1.

That smell escalates into the judgment as a design-changing must-fix, not a rubric line. Everything else on the page survives it.

**Product-lens.** The item's ledger (`product-lens.md`) ran against the spec and closed CLEAR after F1/F2 were fixed. Re-derived against this design: F1 (manifest staleness) is discharged by the `manifest_currency` gate; F2 (dead-filler gate has no home) is discharged by Invariant 8 and the adapter's six responsibilities. One new item-local finding at this revision, recorded in the ledger and equal to L1: a record can carry `verdicts_rederived: true` on evidence weaker than a reader will assume, because the design does not say what verify does with an operand it cannot resolve. The epic's live gate stays CLEAR; nothing here reopens `epic-F1` or `epic-F2`.

---

## Dimensional Review

### 1. Spec Compliance
**Assessment:** Concerns

Every spec requirement has a design element, and the two spec-deferred Open Questions that mattered most (the identity seam's shape, where the baseline point comes from) are answered with stated rejections. Provenance is carried faithfully: `[HARD]` items land as invariants, `[INHERITED]` items keep their source, and the design does not harden an `[INFERRED]` item into a fixed constraint anywhere I could find.

Two gaps against the spec:

- The spec's `[HARD]` verdict requirement — "verdicts are re-derived from the package's own predicate declarations, not from thresholds hard-coded in the tool" (spec.md:66) — is stated as satisfied by B4 but is not achievable as designed (L1). The spec is right that the tool cannot hold the thresholds; the design's answer to *where they come from instead* does not hold up against the contract on disk.
- The spec's `[HARD]` "read the manifest through `scripts/study/manifest.py` and cite the schemas by path plus `schema_version`" (spec.md:47) is honoured, but the design was written against Item 3's *design* rather than its now-delivered code, and the delivered seam differs in ways that change this item's work (L5).

### 2. Pattern Consistency
**Assessment:** Concerns

The design follows Item 3's conventions deliberately and correctly: canonical-text digest recipes under named ids, schema files under `scripts/study/schemas/` with a `schema_version` string, no-partial-output, `package_copy` extended rather than forked, grep-clean invariant tested the way Item 3 tests it. `common.py` as a shared internal module (D10) is the right call, and the reason given — two implementations of "clean" can disagree invisibly — is a real reason, not a tidiness preference.

The consistency problem is with delivered reality rather than with the pattern: three of Item 3's committed assertions about the shape of `scripts/study/` are now wrong under this item, and the design does not name them (L5b).

### 3. Abstraction Quality
**Assessment:** Pass

Four new modules, and each earns its place. `identity.py` exists because preflight must *recompute* rather than trust, which is impossible if the recipe lives in the adapter — that is a genuine justification, not a layering preference. `common.py` is small and has one stated reason. `oracle_entry.py` is the seam the spec demanded and puts package mapping knowledge on the package side. The adapter's six responsibilities are a list of things that must exist somewhere, not an invented structure.

I looked for the cheaper design and could not construct one that satisfies the spec. Removing `identity.py` breaks recomputation. Removing the identity document forces preflight to import the adapter. Removing the shim puts oracle field names in the tool.

### 4. Duplication Avoidance
**Assessment:** Concerns

One real duplication risk, and it is the same unruled path as L2: if the adapter reaches `verify_stellaris` directly for `g3` while `verify.py` reaches it through `oracle_entry.py`, the entry-key → oracle-input mapping and the `IN` save/restore exist twice, in two files, with nothing keeping them in step. That is not a style issue — if the two mappings drift, verify checks a different point than the one that ran, and every deviation reads as zero.

### 5. Data Structure Clarity
**Assessment:** Concerns

The four documents are explicitly shaped, versioned, and schema-backed, and the `verification_summary.json` field list is traced field-by-field to the committed file it generalizes. Good work.

Two shape problems: the identity document's `adapter_sources` list does not map one-to-one onto the delivered snapshot's single `adapter_source_digest` (S1), and the design's five gate names do not map onto the delivered record §9's five rows (S2). Both are small and both are contract-level, so they will be discovered by whoever writes the record rather than by whoever writes the tool.

### 6. Route Safety
**Assessment:** Concerns

Invariant 7 ("interpretive facts never gate") and Invariant 6 ("no partial output") are the right rules, and the exit-code discipline is unambiguous. The accept-set is precisely scoped and negatively tested (Invariant 3), which is the safety property that matters most here.

The unsafe route is the failure path, not the success path: D9's write-nothing-on-failure makes the failed-gate case unrecordable through the intended seam, so the record's mandatory §9 gets filled by hand from stderr (L4). A gate whose failure evidence is hand-copied is a gate that can be misreported.

### 7. Bets & Decisions Integrity
**Assessment:** Fail

B1 and B2 are genuine bets, and they were probed on real era code — the design did the expensive thing rather than asserting. B3 is a real bet and the design names its consequence honestly ("worse than the sealed fingerprint because it looks earned"). B5 is honest about what store sampling loses and does not paper over it.

The failure is proportion. **B4 is the riskiest bet on the page and is the only one nobody probed**, while the two cheapest bets got a full end-to-end probe. Checked against the package on disk, B4 is false (L1). The design's own "if false" clause is also too soft: it says verify would need package-specific threshold knowledge, when the actual consequence is that verify cannot resolve one of the five operands *at all*, by any means available to a generic tool.

The decisions are otherwise well formed — each names its alternative and why it was rejected, and D1/D5/D7's rejections are argued from consequences rather than taste.

**Hidden bet surfaced:** the design assumes `package_identity.json` is on disk when preflight runs, but the adapter emits it at load time. Nothing states who produces it or when. It is the same ordering hole as the baseline result (L3), and it is unstated where the baseline one is at least half-stated.

### 8. Reader Comprehension
**Assessment:** Pass

"Core Concept" gives the mental model in one paragraph before any mechanism, and the rest hangs off it. The architecture diagram plus "Direction of trust" answers the question a reader will actually have (who imports whom) in two lines. Terms are anchored where introduced. A tired engineer can skim this once and know what is being built and why.

---

## Answers to the six specific questions

**Q1 — Is Invariant 4's source set complete?** **No, or at least unruled — this is a must-fix (L2).**

Trace the `g3` path as the design leaves it: `g3` recomputes CAS27 per point from the oracle's `special_materials` (design.md:228). But `special_materials` corresponds to **no package output channel** — zero hits in `contracts/model_contract.json` `outputs` (71 entries); it appears only as two `parameters`, `stellarator_09__stellaris__cas23_to_28_capital__special_materials_capital` and `..._cas2x_pre_contingency__special_materials_capital`. So the shim's declared signature `evaluate(point) -> Mapping[qualified channel, float]` (D6, design.md:80) **cannot** deliver the value `g3` needs. The same holds for `p_th`/`p_the`/`p_et` on the other rungs. So one of two things is true, and the design says neither:

- The adapter calls `verify_stellaris` directly. Then `oracle_entry.py` is correctly outside the source set — but the entry-key → oracle-input mapping and the `IN` save/restore now exist in two files with no mechanism keeping them identical (Dimension 4).
- The adapter goes through a second, package-internal entry point in `oracle_entry.py`. Then that module's mappings can change a fed value, Invariant 4's own wording requires it in the declared source set, and design.md:228's enumeration is incomplete.

**Ruling:** if any part of `oracle_entry.py` sits in the `g3` path, it must be in the declared source set and get its own `adapter <path> <sha256>` line in the recipe. Smallest fix: state the path in the adapter's section, extend the declared source set to match, and — whichever path is chosen — add a test that the adapter's and the shim's entry-key mappings agree.

**Q2 — Does the era `StudyQuery` support what D7 needs?** **Yes; the API is not the risk.** Read read-only at `/home/reid/1cfe/teax-v1-era/packages/teax-simkit/simkit/study/query.py`: `cases(state=...)` filters (query.py:135-158); `CaseView.inputs` is the proposal as fed, keyed by qualified entry keys (query.py:120, decoded from `inputs_json`); `.outputs` is qualified channels; `.verdicts` is `constraint_id → status`; `.executable_fingerprint` comes from evidence provenance and falls back to the store's compatibility row (query.py:100-110), which is what Invariant 5 needs; `.catalog[constraint_id].predicate_ir` and `.definition_qn` are joined from the model contract (query.py:36-49, 66-82).

One gap worth pinning: `EmbeddedCatalogView` does **not** expose `source_local_identity` (query.py:36-49), and D1's baseline result and preflight's verdict comparison both key on it (design.md:167,177). It is present in `contracts/model_contract.json` `constraint_catalog.concrete_entries`, so the fix is to read it there — but the design should say so rather than leave it implied (S3).

I am not demanding a plan de-risk step for the API itself. I am demanding one for the thing that actually is unprobed on this revision — operand resolution (L1) — plus one cheap read-only open of the *committed* store through `StudyQuery`, since P1 only exercised a store the probe built itself (S4).

**Q3 — Is a one-line runbook precondition honestly enough?** **No — must-fix (L3).** The delivered runbook runs preflight at step 5 (`runbook.md:91-101`), chooses the execution route at step 7 (`runbook.md:116-129`), and runs points at step 8 (`runbook.md:131-142`). D1 requires "the route" to have executed the pinned baseline point before step 5, which is two steps before the route exists. Worse, step 7's own fail-closed conditions are "the chosen route cannot load the package; the adapter's own self-check fails" — conditions that presuppose the load has *not* happened yet. And `package_identity.json` has the same problem: the adapter emits it at load, preflight's identity gate reads it, and no one is named as producing it.

A `**Calls:**` line cannot carry that. Smallest fix: name an explicit pre-step — "prepare the route and execute the manifest's pinned baseline point", producing both `baseline_result.json` and `package_identity.json` — and hand Item 2 a *step insertion* before step 5, saying plainly that step 7's route-choice rationale is recorded later than the route is first exercised.

**Q4 — Is D6 consistent with Item 3, and do Item 3's tests break?** **Consistent in principle; the tests break, but not on the values.**

Item 3's D6 records "the entry point that exists today" and anticipates Item 4 consuming the seam (`run-study-indicators/design.md:39,85`). `oracle_entry.evaluate` will exist by then, so changing the values is faithful to that principle, and declining the `cli` kind is squarely inside the spec's Open Question. Note in passing that the "pre-authorized `cli` amendment" is not actually live: the delivered validator *rejects* `kind: "cli"` (`tests/study/test_output_contract.py:101`, schema `kind: {"const": "python_callable"}`). Declining it makes that moot.

No delivered test pins the oracle's module or callable values. But three delivered assertions in `tests/study/test_generic.py` break under this item, and the design does not mention them (L5b).

**Q5 — Is currency-vs-identity separation complete?** **The claim holds; one residual gap should be named.** Verified: the glue-edited files are `inputs/system_design.json` and `pipelines/mfe_stellarator.yaml`; neither is `contracts/package_contract.json` nor `contracts/model_contract.json`, so a glue edit cannot move either fingerprint the `manifest_currency` gate compares. The gate can therefore only refuse a stale manifest, never pass one by looking away. That is the design's claim and it is correct.

The residual: a package file that is not in `artifact_hashes` at all is covered by neither gate — the identity gate only checks sealed artifacts, and `manifest_currency` only checks two contract values. The catch is `package_clean` (`git status --porcelain` over the package tree), which is a real backstop but a different kind of check. Worth one sentence naming it as the backstop rather than leaving the reader to notice (S6).

**Q6 — Does D9 work against the delivered record contract?** **No — must-fix (L4).** Runbook step 5: "Every gate runs and every gate's outcome is recorded, pass or fail. A gate that did not run is recorded as not run, with its condition. A cold reader must be able to see that the gates ran, not only that the study proceeded" (`runbook.md:93-96`). Record §9's table takes `pass | fail | did not run — <condition>` per gate (`record-template.md:140-151`). D9 writes zero bytes on any failure (design.md:83), so a failed-gate study's §9 can only be filled by hand from stderr — precisely the hand-copying the snapshot rule exists to prevent, and it also loses "which gates ran" for the gates after the failing one.

Item 3's no-partial-output rule bars *torn* writes, not a complete failure report. Smallest fix: preflight runs all five gates, always writes a complete `preflight_results.json` with per-gate status, and signals pass/fail through the exit code. Invariant 6 then reads "a non-zero exit never leaves a partially written document", which is the property that was actually wanted.

---

## Issues by Severity

### Must fix (before `/_my_plan`)

**L1 — B4 is false on this package; generic verdict re-derivation cannot resolve its operands.** *(design.md:68, 187-188; Dimension 7; structural smell)*

The design says each `predicate_ir` operand resolves to a literal, a bound input, or a computed channel. Checked against `exploration/stellarator_e2e/generated/contracts/model_contract.json`:

- Operands are `feature_ref`s carrying a short `source_name` and a SysML qualified name (`mfe_viability::'Net Power Positive'::net_electric`), with `chain_segments: []`. Nothing binds them to a flat key.
- The contract's `parameters` (204 entries) and `outputs` (71 entries) carry **no** back-reference to those qualified names.
- The three resolutions that *are* possible use three different composition rules: `recirc_ok`'s `threshold` → `stellarator_09__stellaris__recirc_ok__afc3be66f0a3421b__threshold` (constraint-id-prefixed, in `system_design.json`); `beta_ok`'s `beta_limit` → `stellarator_09__stellaris__beta_limit` (owner-instance-prefixed, in `stellarator_plant_params.json`); `wall_load_ok`'s `wall_load` → channel `stellarator_09__stellaris__wall_load_calc__wall_load`, whose producing block name (`wall_load_calc`) appears nowhere in the operand.
- `net_positive`'s `net_electric` resolves to **nothing** by name. No parameter and no channel contains the string. Its value is `stellarator_09__stellaris__pb__p_net`; the proof-of-life used the oracle's `p_net` because it knew the package.

So a generic name-matching tool cannot re-derive one of the five constraints, and can only re-derive three others by guessing among composition rules — which is a silent-wrong risk, not just a coverage gap.

*Smallest fix:* move operand resolution to a package-owned declaration published beside the shim — e.g. `operand_bindings()` in `oracle_entry.py` returning `{constraint_id: {source_name: {"kind": "input"|"channel"|"oracle", "key": "..."}}}` — and make `verify.py` **fail closed** on any operand that is unresolved or resolves ambiguously. Note the manifest's oracle block cannot host this: it is `additionalProperties: false` and is Item 3's file (`scripts/study/schemas/study_package_manifest.v1.schema.json`), which the spec forbids editing locally. Add a plan de-risk step that resolves all five constraints against the real contract *before* `verify.py` is built, and re-state B4 as a bet about the package publishing its bindings, not about generic resolvability.

**L2 — The `g3` oracle path is unruled and Invariant 4's enumeration may be incomplete.** *(design.md:122, 228; Q1 above)* Rule the path; if any part of `oracle_entry.py` is in it, add it to the declared source set and to the recipe's adapter lines. Whichever path is chosen, add a test that the adapter's and the shim's entry-key mappings agree, since a drift there makes verify check a different point than the one that ran.

**L3 — The baseline execution and the identity document have no home in the delivered runbook's step order.** *(design.md:75, 283; runbook.md:91-101, 116-129, 131-142; Q3 above)* Name an explicit pre-step producing both documents; hand Item 2 a step insertion, not a one-line precondition.

**L4 — D9 makes a failed gate unrecordable through the record's mandatory §9.** *(design.md:83; runbook.md:93-96; record-template.md:140-151; Q6 above)* Always write a complete per-gate results document; carry pass/fail on the exit code; narrow Invariant 6 to "no torn writes".

**L5 — Item 3 is delivered and three of its seams differ from what the design assumed.** The design says to bind to Item 3's *designs*, "not their in-flight code" (design.md:20). That was right when written; it is now stale, and the differences change the work:

- **(a) The oracle block requires `sys_path` and is closed.** `scripts/study/schemas/study_package_manifest.v1.schema.json` requires `kind, module, callable, sys_path`, sets `additionalProperties: false`, and `kind` is `const: "python_callable"`; the delivered manifest carries `sys_path: "exploration/stellarator_e2e"`. So D6's "only module, callable, note change" (design.md:80) is incomplete, and the handoff's dotted module name `exploration.stellarator_e2e.studies.oracle_entry` (design.md:315) contradicts the delivered seam's bare-module-plus-`sys_path` design. *Fix:* `sys_path: "exploration/stellarator_e2e/studies"`, `module: "oracle_entry"`, `callable: "evaluate"`; drop the namespace-import research finding (design.md:47) as moot, and say verify resolves the module under the declared `sys_path`.
- **(b) `tests/study/test_generic.py` already exists and will fail.** It asserts `scripts/study/*.py == ["indicators.py", "manifest.py"]` (test_generic.py:44-46) and that `schemas/*.json` is exactly the three committed files (test_generic.py:51-57). This item adds four modules and four schema files, and design.md:302 proposes creating a file of that name. *Fix:* name it as an extension of the delivered file and list the two assertions this item updates.
- **(c) `manifest.tool_source_digest()` is delivered without `files`.** It returns `{recipe, digest}` over a fixed five-file tuple (`scripts/study/manifest.py:34-39, 148-157`). Risk 4's mitigation is therefore a request to change *delivered* code, not an ask of an in-flight item. *Fix:* state that this item's tools compute their own digest over their own declared list and never call `manifest.tool_source_digest()`, and decide explicitly whether reusing the recipe id with a different file list is acceptable or needs its own id — one recipe id meaning two things across three tools is the drift the "never a bare hash" rule exists to prevent.

**L6 — The annex's six sections do not match the delivered runbook's six annex links.** The runbook links `§ Declared ties` (runbook.md:64), `§ Baseline pin` (:101), `§ Oracle` (:114, :155), `§ Validity masks` (:114), `§ Loader exception and glue` (:129), `§ Era pin` (:142, :195). The design's list (design.md:238) omits **Declared ties** and **Baseline pin** — neither has an author anywhere in the epic — and adds "deletion condition", which no step links. design.md:312 defers the mapping pending "Item 2's finished runbook"; the runbook is finished. *Fix:* adopt the runbook's six section names verbatim and say where the deletion condition lives inside them.

### Should fix

**S1 — The identity document's `adapter_sources` list does not map onto the delivered snapshot field.** `record-template.md:311-315` gives `inputs.allowed_modified_files` as a list of `{path, sha256}` (matches) but `inputs.adapter_source_digest` as a **single** sha256; the design declares `adapter_sources: [{path, sha256}]` (design.md:145). With L2 potentially adding a third source this is not a one-to-one copy. *Fix:* state the mapping — a digest over the sorted adapter lines, with the list carried alongside — or ask Item 2 for a list-shaped field.

**S2 — The five gate names do not map onto record §9's five rows.** `record-template.md:145-151` has a standalone "Suffix-sibling scan (warnings only)" row and one combined "Manifest / package fingerprint match" row; the design folds siblings into `declared_keys` and splits fingerprints into `identity` + `manifest_currency` (design.md:170-180). The epic's scope 1 also names the sibling scan as its own preflight item. *Fix:* state the gate → §9 row mapping explicitly.

**S3 — Say where `source_local_identity` and `predicate_ir` come from.** The era's `EmbeddedCatalogView` exposes `predicate_ir` and `definition_qn` but **not** `source_local_identity` (query.py:36-49); it is in `contracts/model_contract.json` `constraint_catalog.concrete_entries`. D1's baseline result and preflight's verdict comparison both key on it (design.md:167,177). Name the source.

**S4 — Add a cheap read-only de-risk step on the committed store.** P1 sampled a store the probe built itself. One read-only `StudyQuery` open of the committed proof-of-life store, checking that `inputs`/`verdicts`/`catalog` are populated as expected, costs minutes and removes the last unprobed assumption in D7 that is not L1.

**S5 — Name the residual staleness case the two gates do not catch.** A package file outside `artifact_hashes` moves neither the identity recompute nor either contract fingerprint; `package_clean` is the only backstop. One sentence.

### Notes

**N1 — Probe spot-check.** I read `probe_effective_fingerprint.py` against the Appendix rather than re-running it. Every claim matches the script: P3's seal walk (probe:53-58), P1's loader swap and the three-point run through `StudyRunner` with the provenance check (probe:71-101, 166-196), P2's adapter-source change and store refusal (probe:198-211). One difference worth a line in the design: the probe's canonical text emits a single `adapter <digest>` line (probe:92), while the design's recipe emits one `adapter <path> <sha256>` line per declared source (design.md:151). The refinement is right, but it means the probed canonical text is not the designed one — nothing rests on it, and saying so keeps the Appendix honest.

**N2 — State the derived seed's derivation.** D8 derives the seed from the study id and the store's compatibility digest (design.md:82). Write the derivation down, or a reader with the record cannot reproduce the draw.

**N3 — Script-vs-import path for the new modules.** `preflight.py` runs as a script and imports `identity.py`/`common.py`, while tests import them as `scripts.study.*` under `pythonpath = ["."]`. `indicators.py` already solved this; say the new modules follow it, so nobody invents a second answer.

---

## Recommendations

1. **Fix L1 first — it changes the design, not just the plan.** Give operand resolution a package-owned home, make verify fail closed on anything unresolved, and de-risk it against all five real constraints before `verify.py` is written.
2. **Rule the `g3` oracle path (L2)** and settle Invariant 4's enumeration with it. These two are one decision about where package oracle knowledge lives.
3. **Re-bind to Item 3 and Item 2 as delivered (L3, L4, L5, L6).** Item 3's tools and schemas and Item 2's runbook and record template are on disk now. Read them and correct the four asks. This is mechanical and cheap, and it is the difference between a plan that starts and a plan that stalls on its first import.
4. **Then the shape fixes (S1–S5).** Each is a sentence or two, and each is something a downstream author would otherwise discover the hard way.

---

## Resolutions

*(Stage 4 — filled in as the owner resolves each issue. Empty at first write.)*

---

**Overall:** APPROVE-WITH-FIXES
**Verdict list:** must-fix L1, L2, L3, L4, L5(a/b/c), L6; should-fix S1–S5; notes N1–N3. **L1 is design-changing** and should be re-checked against this review before `/_my_plan` runs.
**Next Steps:** Record resolutions above, then return to the design agent (or re-run `/_my_design`) pointed at this file to incorporate. The reviewer does not edit the design.
