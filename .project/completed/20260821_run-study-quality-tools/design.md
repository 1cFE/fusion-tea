# Design: Quality Tools and Era Adapter Promotion (RUN-STUDY Item 4)

**Status:** Draft (rev 2 — design-review L1–L6, S1–S5, N1–N3 folded)
**Owner:** Reid W
**Created:** 2026-08-19
**Updated:** 2026-08-19
**Branch:** `feat/stellarator-mbse-demo` · **Commit at design:** `c34561fb` · **Commit at rev 2:** `becee37c`
**Epic:** RUN-STUDY, Item 4

---

## Overview

Promote the proof-of-life's generic mechanical gates into `scripts/study/preflight.py` and `scripts/study/verify.py`, isolate the era workarounds in a package-local, self-checking `era_adapter.py` that binds teax to an honest executable identity, and write the package annex the runbook links per step.

## Related Artifacts

- **Spec:** `.project/active/run-study-quality-tools/spec.md` (Accepted — the contract)
- **Design review:** `.project/active/run-study-quality-tools/design-review.md` — APPROVE-WITH-FIXES, 2026-08-19. L1–L6, S1–S5, N1–N3 are folded into this revision; the disposition list is in Next-Stage Handoff.
- **Epic:** `.project/backlog/epic_run_study_capability.md` — Item 4
- **Concept design:** `.project/concepts/run-study-skill-design.md` (Tools, manifest/adapter, Required Invariants, Validation Strategy) · **review:** `run-study-skill-design-review.md` (C4, C5, M6, m3)
- **Upstream seams — now DELIVERED, and this revision binds to the code and files on disk, not to the designs:** `scripts/study/manifest.py`, `scripts/study/indicators.py`, `scripts/study/schemas/*.json`, `tests/study/*`, `exploration/stellarator_e2e/studies/manifest.json` (Item 3) · `.claude/skills/run-study/{SKILL.md, runbook.md, record-template.md}` (Item 2)
- **Evidence promoted from:** `exploration/stellarator_e2e/study/run_design_search.py`, `verification_summary.json`, the two committed CSVs
- **Design probe (throwaway):** `.project/active/run-study-quality-tools/probe_effective_fingerprint.py` — results in the Appendix
- **Decision records:** `.project/adr/` and `adr.sh` are absent. No ids hand-minted; decisions are recorded below, as Items 2 and 3 did.

---

## The Point

**[INHERITED: `.project/concepts/run-study-skill-design.md` Goals; grade: owner]** One good study exists, and every mechanical gate that made it trustworthy is welded to one 450-line package-specific file. The next study on this package — or the first on any other — starts from zero.

Two of those welds are not merely unshared; they are wrong. **[HARD]** The loader accepts a package whose two glue-edited files differ from their sealed hashes and then hands teax the *sealed* fingerprint as the identity of what ran (`run_design_search.py:184`). teax's whole lineage discipline rests on that identity, so today a glue edit changes what executes and changes nothing about what teax thinks executed. And a preflight gate that asserts "manifest fingerprint matches the package" cannot be honest while those two files differ — verified on disk, and re-verified by this design's probe: 2 of 139 sealed artifacts mismatch.

So this item owes the capability three things: generic gates that name no package, a package-local adapter that tells the truth about what it bypassed and states the condition under which it is deleted whole, and proof that the promoted route still produces exactly what the proof-of-life produced.

---

## Research Findings

**The identity plan is a one-line change at exactly one seam, and the probe proves it end to end.** `PreparedEvaluator.__init__` does `self.package, self.fingerprint = loader.load()` (`teax-v1-era/.../simkit/evaluation/evaluator.py:131`), and that fingerprint is the only source of executable identity downstream: the study definition binds it (`definition.py:41,57`), the store's compatibility row carries it (`store.py:43`), and every evidence record stamps it as provenance (`evaluator.py:179`). Nothing anywhere cross-checks it against the seal — `StudyQuery` reads the store's value and the evidence's value and never consults `package_contract.json` (`query.py:92,114`). The probe ran three real points through `StudyRunner` under a synthetic effective fingerprint: 3/3 completed, baseline LCOE `275.2642200420774` at rel 2.8e-13 with 5/5 verdicts satisfied, and the evidence provenance carried the effective value.

**Lineage refusal is already built; it just needs an honest input.** `StudyStore.create_or_open` binds the compatibility tuple on create and raises `IncompatibleStore` on mismatch (`store.py:126-151`). The probe changed only the adapter's source bytes, recomputed the effective fingerprint, and the pre-existing store refused — the concept design's unowned proof 5, mechanically.

**Predicate operands do not resolve to keys by name, and this is the finding that changed the design.** In `contracts/model_contract.json`, `predicate_ir` is a JSON *string* whose operands are `feature_ref`s carrying a short `source_name` and a SysML qualified name, with `chain_segments: []`. The contract's 204 `parameters` and 71 `outputs` carry no back-reference to those qualified names. Checked against all five real constraints, the three resolutions that are even possible use three different composition rules — `recirc_ok`'s `threshold` is constraint-id-prefixed (`…recirc_ok__afc3be66f0a3421b__threshold`), `beta_ok`'s `beta_limit` is owner-instance-prefixed (`…__beta_limit`), and `wall_load_ok`'s `wall_load` is a channel whose producing block name appears nowhere in the operand. The fourth, `net_positive`'s `net_electric`, resolves to nothing at all: no parameter and no channel contains the string, and its value is `…__pb__p_net`, which the proof-of-life knew only because it knew the package. So generic name matching cannot re-derive one constraint of five and can only guess at three others. **Operand resolution is a producer obligation, not a consumer's inference** — see D12.

**`source_local_identity` is in the contract, not in the query API.** The era's `EmbeddedCatalogView` exposes `predicate_ir` and `definition_qn` but not `source_local_identity` (`query.py:36-49`); it is on every `constraint_catalog.concrete_entries` entry, alongside `constraint_id` and `definition_qualified_name`. Both the baseline result document and preflight's verdict comparison key on it, and both read it there **[S3]**.

**The store speaks the generic vocabulary; the CSV does not.** `CaseView.inputs` is keyed by qualified entry keys and `.outputs` by qualified channel names (`query.py:120-134`); `.verdicts` is `constraint_id → status`; `.executable_fingerprint` comes from evidence provenance and falls back to the store's compatibility row, which is what Invariant 5 needs. The committed CSVs are keyed by study-chosen short names (`R`, `a`, `lcoe`), which no generic tool can resolve without being told the mapping.

**Item 3 as delivered differs from Item 3 as designed, in three ways that change this item's work [L5].**
- The manifest's oracle block **requires `sys_path`** and is closed: `{kind (const "python_callable"), module, callable, sys_path, note?}`, `additionalProperties: false` (`scripts/study/schemas/study_package_manifest.v1.schema.json`). The delivered manifest carries `sys_path: "exploration/stellarator_e2e"`, `module: "verify_stellaris"`, `callable: "compute"`. So `module` is a bare importable name resolved under a declared `sys_path` — which also makes this design's earlier namespace-import finding moot and removes any need for a dotted package path.
- `tests/study/test_generic.py` already exists and asserts that `scripts/study/*.py` is exactly `["indicators.py", "manifest.py"]` and that `schemas/*.json` is exactly the three committed files. Both assertions fail the moment this item lands.
- `manifest.tool_source_digest()` is delivered as `{recipe, digest}` over a fixed five-file tuple, with no `files` field (`scripts/study/manifest.py:34-39,148-157`).

**Item 2 as delivered pins the annex's section names and the record's gate rows.** The runbook links six annex sections — `§ Declared ties`, `§ Baseline pin`, `§ Oracle`, `§ Validity masks`, `§ Loader exception and glue`, `§ Era pin` — and runs preflight at step 5, chooses the route at step 7, and executes at step 8. Record §9's table has five rows including a standalone suffix-sibling row and one combined fingerprint row, and it takes `pass | fail | did not run — <condition>` per gate. The snapshot's `arms[].effective_executable_fingerprint.inputs` carries `allowed_modified_files` as a list and `adapter_source_digest` as a **single** sha256.

**Repo conventions.** Tests under `tests/study/` with a `package_copy` factory in `conftest.py`; pytest `pythonpath = ["."]`; no `__init__.py` under `scripts/study/`; ruff line length 100.

---

## Core Concept

Everything here follows from one move: **the adapter stops reporting an identity it did not earn, and starts publishing a small document that says exactly what it bypassed and what identity that produces.** The document is the seam. The adapter writes it; teax binds the identity in it; generic preflight gates on it by recomputation; generic verify copies its glue disclosure into the verification summary; the record snapshots it. No generic tool imports the adapter, and no package fact leaks into a tool — the tools handle a typed document, not knowledge.

That one document makes the rest fall out. The identity gate becomes honest by construction because it recomputes rather than trusts: from the document's own declared inputs plus the files on disk. It works unchanged when the adapter is gone, because the document carries a `kind` discriminator and the no-adapter case is the degenerate one — an empty allowed-modified set, which turns the same gate into a full seal check. Gate the manifest's currency separately, against the two contract fingerprints that glue edits cannot touch, and the two halves together are complete without either one lying.

The same rule settles the verification side, and it is where the first draft of this design was wrong. A generic tool cannot infer which flat key a predicate operand means; the package must **publish** that binding, exactly as it publishes its oracle. So the package-owned shim beside the manifest exposes two things — an evaluator that turns a point into named channels, and a binding table that says which key or channel each operand is — and `verify.py` consumes both as data and fails closed on anything it cannot resolve. A generic tool that guesses is worse than one that refuses.

The tools then stay small and boring. Preflight is six named mechanical checks over documents, package files, and git; it never executes and never imports teax. Verify samples the store (the only source whose vocabulary is package-qualified), calls the shim, re-derives every verdict through the published bindings, and writes one summary document. The adapter keeps everything else: the loader exception, the glue rungs, the self-checks, the era-pin assertion, and its own deletion condition.

---

## Key Bets

- **B1.** Returning a computed fingerprint from `loader.load()` is accepted by the whole era stack, and no component cross-checks executable identity against the seal. *If false → the effective-fingerprint plan needs a teax change, which is a Non-Goal, and the item stalls on an upstream dependency.* **Probed and confirmed** (Appendix, P1).
- **B2.** A store bound to one effective fingerprint refuses to open under another, so glue drift and adapter drift are refused rather than silently mixed. *If false → the review's C4 is only half-fixed: identity is honest but nothing enforces it.* **Probed and confirmed** (Appendix, P2).
- **B3.** The set of files whose content can change a glue value or the loader's accept-set is enumerable by the adapter and stable enough to declare. *If false → the effective fingerprint is honest about the files it names and blind to the one that actually moved a number, which is worse than the sealed fingerprint because it looks earned.* This is why the declared source set covers the shim and the oracle module (Invariant 4, D13).
- **B4 (restated after review L1).** A package can publish, for every constraint in its catalog, a binding from each predicate operand to a qualified input key or channel — and doing so is cheap, because the package author already knows it. *If false → verdicts cannot be re-derived for that package at all, and `verify.py` must say so rather than emit `verdicts_rederived: true` on weaker evidence.* The earlier form of this bet — that a generic tool could resolve operands by name — is **false on this package** and is the review's L1; the design now rests on publication, not inference. **De-risked first in the plan** (all five constraints resolved against the real contract before `verify.py` is written).
- **B5.** Sampling the store rather than the exported CSV does not weaken the verification claim, because the export is a deterministic function of the store produced in the same run. *If false → the record ships a CSV that nothing checked, and "verified" means less than a reader assumes.* Mitigated for this package by promotion equivalence, which compares the exported CSVs byte-for-byte.

---

## Key Decisions

- **D1. The baseline gate consumes an already-executed result document, never a prepared-evaluator handle.** The route executes exactly the manifest's pinned baseline point and writes `baseline_result.json`; preflight reads it as data. *Rejected: preflight takes a prepared-evaluator handle (it would make preflight a library imported by the adapter-importing definition, put typed-input construction — package knowledge — inside a generic tool, and give the tool a live execution path the spec says it must not own).*
- **D2. The adapter emits one document with two blocks — `identity` and `glue_ledger` — not two documents.** One write, one digest, one path in the record; preflight reads only `identity`, verify reads only `glue_ledger`, and the glue ledger is never wanted without the identity that scopes it. *Rejected: two documents (doubles the plumbing and lets the two drift out of step for the same run).*
- **D3. The identity document is typed by `kind`, and the no-adapter case is the degenerate member.** `{"kind": "sealed"}` has an empty allowed-modified set and the sealed fingerprint as its digest; `{"kind": "effective"}` carries the three inputs and the recipe. One gate covers both. *Rejected: an adapter-only document with preflight branching on its absence (an optional gate input is how gates rot, and the deletion condition would then change preflight's behavior).*
- **D4. `scripts/study/identity.py` is a new generic sibling module** owning the identity-document schema, the `effective-executable-fingerprint/v1` recipe, the sealed-case emitter, and the recompute-and-compare logic. Imported by `preflight.py`, `verify.py`, and the adapter. *Rejected: putting the recipe in Item 3's `manifest.py` (it is not a manifest fact, and the spec forbids editing Item 3's files beyond one pre-authorized amendment); rejected: implementing it inside the adapter (preflight could then only trust, not recompute).*
- **D5. The oracle entry point is a package-owned shim module beside the manifest, `exploration/stellarator_e2e/studies/oracle_entry.py`; `verify_stellaris.py` is untouched.** The shim owns everything the seam needs on the package side: the entry-key → oracle-input mapping, the oracle-output → qualified-channel mapping, the `IN` save/restore, the `_profile_integral` memoization, the operand bindings (D12), and the glue-value entry point the adapter calls (D13). *Rejected: a CLI on `verify_stellaris.py` (edits the independent oracle for study-seam reasons, invents a wire format for one consumer, and pays a subprocess per sampled point).*
- **D6. The manifest's oracle block stays `kind: "python_callable"` and changes only its values, within the delivered closed schema [L5a]:** `sys_path: "exploration/stellarator_e2e/studies"`, `module: "oracle_entry"`, `callable: "evaluate"`, `note` stating the generic signature. `verify.py` puts the declared `sys_path` on `sys.path` and imports the bare module name, exactly as the delivered schema intends. The `{"kind": "cli"}` amendment is declined and stays unused — the delivered validator rejects it anyway (`kind` is `const`), which makes the decision moot as well as right. *Rejected: `{"kind": "cli"}` (Item 3's D6 rejected inventing a CLI protocol for a single future consumer; nothing about this consumer changed that).*
- **D7. `verify.py` samples the study store through `StudyQuery`, not the exported CSVs.** The store is the primary evidence and the only source keyed by qualified names; a CSV sampler would need a column→key map that is study knowledge a generic tool may not hold. *Rejected: sampling the CSVs as the proof-of-life did (it verified the shipped artifact, which is the one thing this loses — recovered for this package by promotion equivalence, and named as B5).*
- **D8. Sampling is scoped per store, `K = 12` by default with stratification as a floor, and the seed defaults to a derivation that is written down [N2]:** `seed = int(sha256(f"{study_id}\n{compatibility_digest}\n").hexdigest()[:16], 16)`, where `compatibility_digest` is the sha256 of the store's compatibility tuple serialized as sorted `key=value` lines. `--seed` overrides; the effective seed and its `seed_source` are always recorded, so a reader with the record can reproduce the draw. *Rejected: a fixed default seed (every study then samples the same stratum positions, and the number is magic); rejected: a required `--seed` (invites an arbitrary choice where a deterministic one exists).*
- **D9 (rewritten after review L4). Preflight always runs every check and always writes a complete results document; the exit code carries the verdict.** A failed check is recorded as `fail` with its detail, a check that could not run is recorded as `did not run` with its condition, and the process exits non-zero. This is what the delivered runbook step 5 and record §9 require — "a cold reader must be able to see that the gates ran, not only that the study proceeded" — and it does not weaken no-partial-output, which bars *torn* writes, not complete failure reports (Invariant 6, narrowed). *Rejected (the first draft's position): writing zero bytes on any failure — it makes §9 fillable only by hand from stderr, which is the hand-copying the snapshot rule exists to prevent, and it loses the outcome of every check after the failing one.*
- **D10. Preflight and verify share one small internal module, `scripts/study/common.py`** — the git-clean gate, atomic deterministic document writing, the tool-source digest over a per-tool file list, and the exit/error convention. The teax import and store access stay inside `verify.py`, so `preflight.py` never imports teax. *Rejected: two independent scripts (two implementations of "clean" can disagree about what clean means, and that disagreement is invisible).*
- **D11. Promotion equivalence lives at `exploration/stellarator_e2e/studies/promotion_equivalence.py` and is kept as a marker-gated regression, not retired as one-time evidence.** The 19-point availability sweep runs in the default suite; the 948-point grid runs behind `-m slow`. It is deleted with the adapter. *Rejected: running it once and deleting it (it is the only thing that would catch a silent behavior change in the adapter or the promoted definition while the adapter exists).*
- **D12 (new, review L1). Operand resolution is published by the package, consumed by the tool as data, and fails closed.** The module the manifest's oracle block names exposes, besides its declared `callable`, a fixed-name `operand_bindings()`; `verify.py` requires both and treats a missing `operand_bindings` as a mechanical failure. The binding contract:

  ```python
  operand_bindings() -> {constraint_id: {source_name: {"kind": "input" | "channel", "key": "<qualified>"}}}
  ```

  `kind: "input"` resolves from `case.inputs` when the study swept the key and from the package's `inputs/*.json` otherwise; `kind: "channel"` resolves from the oracle's returned channel map — which is how `net_positive`'s `net_electric` reaches `…__pb__p_net`, a value the era store does not record but the oracle does return. Literal operands come from `predicate_ir` and are never bound. `verify.py` fails closed, naming the constraint and the operand, when a catalog constraint has no entry, an operand has no binding, a binding's key resolves to nothing, or two bindings resolve one operand differently. *Rejected: generic name matching (false on this package for one of five constraints, and a guess among three composition rules for three others — a silent-wrong risk, not a coverage gap); rejected: hosting the bindings in the manifest's oracle block (it is `additionalProperties: false` and is Item 3's file, which the spec forbids editing locally) — which is why the binding travels as a second callable on the module the manifest already names.*
- **D13 (new, review L2). The adapter's `g3` glue goes through the shim, not around it.** `oracle_entry.py` exposes a second package-owned entry point returning the glue-fed values the adapter needs per point, and the adapter calls it. One mapping, one `IN` save/restore, one home. The glue values `g3` needs — `special_materials`, `p_th`, `p_the`, `p_et` — are parameters, not output channels, so they cannot come through `evaluate()`'s channel-keyed return; the shim exposes them under their qualified *entry-key* names on a separate call. *Rejected: the adapter calling `verify_stellaris` directly (the entry-key → oracle-input mapping and the `IN` save/restore would then exist in two files with nothing keeping them in step, and a drift there makes verify check a different point than the one that ran).* **Consequence:** `oracle_entry.py` joins the adapter's declared source set, so editing the shim retires existing stores exactly as editing the oracle module does.

---

## Architecture

```text
  era_adapter.py ──loader.load() -> (module, EFFECTIVE fingerprint)──►  PreparedEvaluator
   (package-local) │                                                          │
        │          └──g3 glue values──► oracle_entry.py ◄──┐    StudyDefinition ─► StudyStore
        │  writes                        (package-owned)   │        (refuses a different identity)
        ▼                                       │          │
  package_identity.json                         ▼          │
   {identity{kind,recipe,inputs,digest},  verify_stellaris  │
    glue_ledger[]}                        (untouched)       │
        │                                                   │
        ├──► preflight.py ──► preflight_results.json        │ evaluate(point) -> channels
        │      also reads: axis declaration, manifest        │ operand_bindings() -> table
        │      (manifest.py), package inputs + both          │
        │      contracts, baseline_result.json, git          │
        │                                                    │
        └──► verify.py ──► verification_summary.json ────────┘
               samples StudyQuery cases; re-derives verdicts from predicate_ir
               through the published bindings; fails closed on any unresolved operand
```

**Direction of trust.** Every arrow into a generic tool carries data. `preflight.py` and `verify.py` import `manifest.py`, `identity.py`, `common.py`, and — for verify — teax and whatever module the manifest names under its declared `sys_path`. Neither imports the adapter, and the adapter importing `identity.py` and `oracle_entry.py` is the allowed direction.

**Integration points.** *Upstream:* Item 3's `manifest.py`, its three schema files, and the axis-declaration file; the package's `inputs/*.json`, `contracts/model_contract.json`, `contracts/package_contract.json`. *Sideways:* the era teax worktree, resolved from the ambient environment by the caller, never named in a tool. *Downstream:* Item 2's record — `preflight_results.json` into §9, `verification_summary.json` and `package_identity.json` into `results/` and the snapshot's `arms[].verification`, `arms[].effective_executable_fingerprint`, and `glue_ledger`.

---

## Required Invariants

1. **Generic means grep-clean.** `preflight.py`, `verify.py`, `identity.py`, and `common.py` contain no package name, no key prefix, no oracle name, and no adapter import. Tested by grep, as Item 3's Invariant 6 is.
2. **The identity gate recomputes; it never trusts.** Preflight's verdict is a function of the document's declared inputs and the bytes on disk, never of the document's asserted digest alone.
3. **The accept-set is exactly `{TAMPER on the declared allowed-modified files}`.** Any other diagnostic kind, any other path, any era-version mismatch still refuses. Asserted by a negative test that modifies a third sealed artifact.
4. **The adapter's declared source set covers every file whose content can change a glue value or the accept-set.** Under D13 that is `era_adapter.py`, `oracle_entry.py`, and `verify_stellaris.py`. A file that feeds a number into a run and sits outside the set makes the effective fingerprint look earned while being blind.
5. **Identity continuity across the run.** The identity preflight gated, the identity the store bound, and the identity present after the run are one value. Verify asserts it and records it.
6. **No torn writes.** A non-zero exit never leaves a partially written document. Preflight's results document is always complete (D9); verify writes its summary only on a completed pass, and never a fragment.
7. **Interpretive facts never gate.** Every non-zero exit is one of the enumerated mechanical failures; a valid empty result exits 0.
8. **Adapter-owned facts are checked by the adapter.** The dead-filler assertion, the era-pin prerequisite, and the accept-set run on every adapter-route load and fail closed. No generic tool asserts any of them.
9. **Unresolved is never assumed.** `verify.py` emits `verdicts_rederived: true` only when every operand of every catalog constraint resolved through a published binding; anything unresolved or ambiguous is a mechanical failure naming the constraint and the operand.
10. **The manifest holds no era, glue, allowed-modified-file, or operand-binding fact.** Deleting the adapter requires no manifest edit.
11. **Every point executes through `StudyRunner`.** Neither tool constructs an evaluator or runs a point.

---

## Component Overview

### `scripts/study/identity.py` — the identity seam

*The document*, `schema_version: "study-package-identity/v1"`, schema file `scripts/study/schemas/package_identity.v1.schema.json` following Item 3's D9 convention:

```jsonc
{ "schema_version": "study-package-identity/v1",
  "package": {"name": "...", "path": "<repo-relative>"},
  "identity": {"kind": "effective",            // or "sealed"
               "recipe": "effective-executable-fingerprint/v1",
               "sealed_executable_fingerprint": "<from package_contract.json>",
               "allowed_modified_files": [{"path": "<pkg-relative>", "sha256": "..."}],
               "adapter_sources": [{"path": "<repo-relative>", "sha256": "..."}],
               "adapter_source_digest": "<sha256 over the sorted adapter lines>",
               "digest": "<the effective executable fingerprint>"},
  "glue_ledger": [{"rung": "g3", "keys": ["..."], "supplies": "...",
                   "independently_verified": false, "note": "..."}] }
```

*The recipe*, `effective-executable-fingerprint/v1`, is Item 3's canonical-text pattern under its own id: line 1 the recipe id, then `sealed <hex>`, then one `modified <path> <sha256>` line per allowed-modified file sorted by path, then one `adapter <path> <sha256>` line per declared adapter source sorted by path; the digest is sha256 of that UTF-8 text. For `kind: "sealed"` both lists are empty and the digest is defined to be the sealed fingerprint itself, so the recipe reduces to identity rather than inventing a second value.

**Snapshot mapping [S1].** Item 2's delivered snapshot takes `allowed_modified_files` as a list (one-to-one) but `adapter_source_digest` as a single sha256, while D13 gives the adapter three declared sources. So the document carries both: the `adapter_sources` list for audit, and `adapter_source_digest` — sha256 over just the sorted `adapter <path> <sha256>` lines — as the single value the snapshot field copies. No ask of Item 2 is needed.

*The gate*, used by preflight and re-asserted by verify: recompute the digest from the document's declared inputs and the current bytes; require equality with `identity.digest`; require every sealed artifact **outside** `allowed_modified_files` to match `artifact_hashes`; require every declared file to exist. Each failure names the file.

*The sealed emitter*, one call for the no-adapter route, so deleting the adapter does not leave a route with no way to publish its identity.

### `scripts/study/preflight.py` — six named checks

*The baseline result document* the route hands it (D1), `study-baseline-result/v1` — the smallest thing that can discharge the gate. `source_local_identity` and `definition_qualified_name` are read from `contracts/model_contract.json` `constraint_catalog.concrete_entries`, not from the era's catalog view, which does not expose the first **[S3]**.

```jsonc
{ "schema_version": "study-baseline-result/v1",
  "executed_under": {"identity_digest": "...", "store_id": "...", "case_id": "..."},
  "point": {"<qualified entry key>": 12.7},
  "channels": {"<qualified channel>": 275.2642200420774},
  "verdicts": [{"constraint_id": "...", "definition_qualified_name": "...",
                "source_local_identity": "wall_load_ok", "status": "satisfied"}] }
```

Two subcommands. `preflight.py gates` runs all six checks and needs `--package`, `--manifest`, `--groups`, `--identity`, `--baseline-result`. `preflight.py clean` runs the cleanliness gate alone, for the post-run and post-verify sites the proof-of-life used (`run_design_search.py:358,414,443`). Both emit `study-preflight-results/v1`: a list of `{gate, status, checked, detail}` plus the digests of every input document, always complete (D9).

| Check | What it checks | Fails when | Record §9 row **[S2]** |
|---|---|---|---|
| `declared_keys` | Every key in Item 3's axis declaration exists in the package's inputs and classifies against `contract.parameters` | key absent; key names a produced channel (reported as a **computed quantity**, policy §2.1); key unclassifiable | Declared-group key validation |
| `sibling_scan` | Suffix-sibling candidates outside the declared groups | never — status is `pass` or `warnings: <n>` | Suffix-sibling scan (warnings only) |
| `identity` | `identity.py`'s gate, plus equality with the identity the baseline result was executed under | recompute mismatch; a sealed artifact outside the allowed set differs; the document is missing or malformed; the baseline ran under a different identity | Manifest / package fingerprint match |
| `manifest_currency` | The manifest's `fingerprints.recorded_provenance.{executable_fingerprint, semantic_fingerprint}` against the live `package_contract.json` and `model_contract.json` | either differs — the manifest's baseline, ties, oracle, and objective catalog were pinned against a different package generation and must be re-declared | Manifest / package fingerprint match |
| `baseline_headline` | The baseline result's headline channel against the manifest's pinned value at rel < 1e-9, and its verdicts against the manifest's pinned verdicts by `source_local_identity` | value off tolerance; any verdict differs; the pinned channel is absent | Baseline gate against the pinned headline |
| `package_clean` | `git status --porcelain` over the package tree | any output | Package cleanliness |

The sibling scan is a named result rather than a fold into `declared_keys` because the epic's scope 1 and record §9 both treat it as its own line, and because it can never fail — keeping it separate is what stops an advisory from ever reading as a gate. The two fingerprint checks share one §9 row, and the row's Detail carries both outcomes.

The two contract fingerprints in `manifest_currency` are the honest choice precisely because glue edits cannot touch them: neither contract file is in the allowed-modified set, so this gate can only refuse a stale manifest, never pass one by looking the other way. Item 3 reports the same drift as a non-gating warning; the asymmetry is deliberate and stated in the spec. **Residual [S5]:** a package file that is in neither `artifact_hashes` nor the two contracts moves neither check; `package_clean` is its only backstop, and it is a different kind of check — a working-tree gate, not an identity one.

### `scripts/study/verify.py` — the generic sampler

Reads `--package`, `--manifest`, `--identity`, `--store` (repeatable), `--sample-size`, `--seed`, `--out`. Puts the manifest's declared `sys_path` on `sys.path`, imports the named module, and requires both the declared `callable` and `operand_bindings` (D12). Per store: load cases through `StudyQuery`, keep `completed` ones, stratify by the observed verdict combination, take one case per stratum, fill the remainder randomly to `K` (stratification is a floor, never a cap), then per sampled case —

1. Call `evaluate(case.inputs)` and receive qualified channel values.
2. Compare every channel the manifest's objective catalog names plus every channel a binding resolves, at rel < 1e-9, tracking the worst deviation and where it occurred.
3. Re-derive each verdict from the entry's `predicate_ir` (parsed from its JSON string): each `feature_ref` operand is resolved through `operand_bindings()[constraint_id][source_name]`, each literal from the IR. Compare to the recorded verdict. Anything unresolved or ambiguous is a mechanical failure (Invariant 9).
4. Copy the identity document's `glue_ledger` entries with `independently_verified: false` into the summary as the named not-independently-verified inputs.

`verification_summary.json`, `study-verification-summary/v1`, is a superset of the committed file and of Item 2's delivered `arms[].verification` block:

```jsonc
{ "schema_version": "study-verification-summary/v1",
  "tool": {"path": "scripts/study/verify.py",
           "source_digest": {"recipe": "tool-source-digest/v1", "digest": "...", "files": ["..."]}},
  "command": ["scripts/study/verify.py", "..."],       // repo-relative, no absolute paths
  "teax": {"module_path": "...", "revision": "..."},
  "package": {"path": "...", "package_name": "...", "git_clean": true},
  "identity": {"kind": "...", "digest": "...", "matches_preflight": true},
  "manifest": {"path": "...", "schema_version": "...", "digest": "..."},
  "oracle": {"kind": "python_callable", "sys_path": "...", "module": "...", "callable": "evaluate",
             "operand_bindings_digest": "<sha256 of the canonicalized binding table>"},
  "stores": [{"path": "...", "study_id": "...", "compatibility": { ... },
              "cases_total": 949, "cases_completed": 949,
              "sampling": {"scheme": "stratified-by-verdict-combination/v1",
                           "seed": "...", "seed_source": "derived|explicit",
                           "sample_size_requested": 12, "strata_observed": 4,
                           "sampled_rows": 12, "sampled_case_ids": ["..."]},
              "worst_channel_rel_dev": 5.67e-16,
              "worst_at": {"case_id": "...", "channel": "...", "got": ..., "expected": ...}}],
  "tolerance": 1e-9,
  "channels_checked": [{"channel": "<qualified>", "oracle_name": "..."}],
  "verdicts_rederived": true,
  "constraints_rederived": [{"constraint_id": "...", "source_local_identity": "...",
                             "operands_resolved": 2}],
  "verdict_mismatches": [],
  "not_independently_verified": [{"rung": "g3", "keys": ["..."], "note": "..."}],
  "worst_channel_rel_dev": 5.67e-16,
  "outcome": "pass" }
```

Every field of the committed `verification_summary.json` survives by name or by a named generalization: `sampled_rows_per_study` → per-store `sampling.sampled_rows`; `sampling` → `sampling.scheme`; `package_git_clean` → `package.git_clean`; `glue_note` → `not_independently_verified`. `constraints_rederived` is new and is what makes `verdicts_rederived: true` auditable rather than asserted.

### `exploration/stellarator_e2e/studies/oracle_entry.py` — the package-owned oracle seam

Three published surfaces, and nothing else:

```python
def evaluate(point: Mapping[str, float]) -> Mapping[str, float]: ...   # qualified keys -> qualified channels
def operand_bindings() -> Mapping[str, Mapping[str, Mapping[str, str]]]: ...   # D12
def glue_values(point: Mapping[str, float]) -> Mapping[str, float]: ...        # D13, qualified entry keys
```

It owns the entry-key → oracle-input mapping, the oracle-output → channel mapping, the `IN` save/restore (`run_design_search.py:144-152`), and the `_profile_integral` memoization. It imports `verify_stellaris` — adding `exploration/stellarator_e2e` to `sys.path` itself, since that is package-side knowledge — and modifies nothing in it.

### `exploration/stellarator_e2e/studies/era_adapter.py` — the temporary adapter

Package-local, named temporary in its first line, and the only home for six things: the loader exception (the accept-set, Invariant 3); the glue rungs g1–g3, with `g3`'s values obtained through `oracle_entry.glue_values()` (D13); the self-checks, above all the dead-filler assertion, which moves *into* the adapter and runs on every load rather than in a tool; the era-pin prerequisite, asserted not merely recorded — the adapter checks it is running under the pinned worktree at `fa0e06a` and fails closed otherwise; the effective-fingerprint computation via `identity.py`'s recipe; and the identity-document emission.

Its declared source set (Invariant 4) is `era_adapter.py`, `oracle_entry.py`, and `verify_stellaris.py`. A change to any of the three changes the executable identity and retires existing stores — correct, since all three can move a number that is fed into a run, and costly enough to name in Risks.

**Deletion condition, stated in the adapter and in the annex:** the stock `ProvisionalPackageLoader` accepts the regenerated package with `strict=True`. When it does, the adapter is deleted whole, the study-local definition swaps the adapter's loader for the stock one and `identity.py`'s sealed emitter, the sealed fingerprint becomes the identity again, `promotion_equivalence.py` is deleted with it, and `oracle_entry.py` stays — it is the verification seam, not glue. No partial retirement, no dormant compatibility branch.

### `exploration/stellarator_e2e/studies/ANNEX.md` — the package annex

**Six sections, named verbatim from the delivered runbook's links [L6]**, because the runbook is finished and its links are the contract:

| Section | Linked from | Content |
|---|---|---|
| `§ Declared ties` | step 2 | Why `magnet__R0` rides with `R` — the Ampère's-law current runs on the major radius, so it is the same physical quantity under a separately authored attribute. The tie *data* lives in the manifest; this section explains it and never restates it. |
| `§ Baseline pin` | step 5 | What the pinned baseline point and headline are, that they live in the manifest, and that regeneration requires re-declaring them before preflight can pass. |
| `§ Oracle` | steps 6, 9 | The parameterization: how a point becomes oracle inputs and what the oracle returns, the shim's three surfaces, and the operand-binding table's meaning. |
| `§ Validity masks` | step 6 | `R > a + 2.25 m` and any sibling: a derived geometric bound from held-fixed inputs, not a design screen (`run_design_search.py:113-118`), with the radial-build stack itemized. |
| `§ Loader exception and glue` | step 7 | The exact accept-set, the glue rungs g1–g3 with what each supplies that the model does not, **and the adapter's deletion condition verbatim** — deletion is a fact about the exception, so it lives with it rather than in a seventh section no step links. |
| `§ Era pin` | steps 8, 12 | The worktree and commit, why the pin exists, and that current teax main's refusal of the v1.0.0 seal is principled and is not to be chased upstream. |

Nothing in it is a rule; it is package fact, linked and never inlined.

### `exploration/stellarator_e2e/studies/promotion_equivalence.py` — the equivalence harness

A study-local direct-API definition (`StudyRunner` + `PreparedListStrategy`, the same route the proof-of-life used and the only one the era supports for coordinated blocks) that reproduces both proof-of-life studies under the promoted structure and exports both CSVs to a scratch directory. Driven by `tests/study/test_promotion_equivalence.py`, which diffs them byte-for-byte against the committed files. The committed proof-of-life directory is read, never written.

---

## Non-Goals

- A second execution facade, a generic runner, or any hand-rolled sweep loop.
- Package knowledge — names, key prefixes, thresholds, oracle field names, operand keys — inside the generic tools.
- Upstream teax or sysml-codegen changes, and any attempt to make current teax main accept the v1.0.0 seal.
- Interpretive gating of any kind.
- Editing Item 3's delivered modules, schemas, or manifest, or Item 2's delivered skill files. The changes those files need are recorded as coordination asks below and applied by the orchestrator.
- Migrating `verify_stellaris.py`'s or `run_stellaris.py`'s oracle knowledge into the manifest.
- Running a new study, plotting, or reporting.

---

## Implementation Notes

- **The only identity seam is `loader.load()`'s second return value.** Do not thread the effective fingerprint anywhere else; everything downstream picks it up (Appendix, P1).
- **Import path for the new modules [N3].** `preflight.py` and `verify.py` run as scripts and import `identity.py`/`common.py`/`manifest.py`; tests import them as `scripts.study.*` under `pythonpath = ["."]`. Follow exactly what `indicators.py` already does — do not invent a second answer.
- **`predicate_ir` is a JSON string**, not a nested object. Parse it once per catalog entry.
- **Do not `db.unlink()` in the promoted definition.** The proof-of-life deleted the store on every run (`run_design_search.py:288-289`), which would make the lineage-refusal test unable to find a store to refuse. Deleting is a caller's choice, not the definition's.
- **`pkg/stellarator_tea` is a symlink to `generated/`.** The package root is `exploration/stellarator_e2e/generated`; both paths reach the same tree.
- **The era teax path is the caller's, never the tool's.** `verify.py` imports `simkit` from the ambient environment and records where it came from. The pin lives in the annex and the invocation.
- **Byte-for-byte CSV reproduction depends on proposal construction, not only on physics.** The glue values are computed per point through the shim, so the promoted definition must build proposals from the same rungs in the same order; the values must be identical, not merely close.
- **Extend Item 3's `package_copy` factory; do not fork it.** Its two rules — assert before mutating, re-pin unless the test is about the pin — apply verbatim, plus a third convenience here: mutate a glue file *and* re-emit the identity document, or not, depending on which check the test is aiming at.

---

## Potential Risks

- **Editing `verify_stellaris.py` or `oracle_entry.py` retires every existing store.** That is the correct consequence of Invariant 4 and D13 — both feed numbers into a run — but it is a sharp edge for anyone editing either for unrelated reasons. Mitigation: the annex states it, and the refusal message names the file whose digest moved.
- **The operand-binding table is hand-authored and unverified against the package.** A wrong key makes verify compare the wrong number and read as a pass. Mitigation: verify fails closed on an unresolvable key, the summary records `constraints_rederived` with per-constraint operand counts, and the plan's first de-risk step resolves all five constraints against the real contract before `verify.py` exists.
- **One recipe id over two file lists [L5c].** `tool-source-digest/v1` names the algorithm — canonical text over a *named* file list — not one particular list. This item's tools therefore compute their own digest over their own declared list via `common.py` and never call `manifest.tool_source_digest()`. Every emission must carry `files[]`, or one recipe id silently means two things across three tools; that is the ask to Item 3 below. If Item 3 declines, the fallback is a distinct recipe id for this item's tools, which is worse only because it multiplies ids.
- **Promotion equivalence may fail on a float-text difference rather than a physics difference.** Mitigation: the test reports the first differing line with both values, and the 19-row availability sweep fails first and cheaply.
- **The CSV the record ships is not what verify samples (B5).** Mitigation for this package is promotion equivalence; going forward it rests on the export being produced from the store in the same run.
- **Preflight's baseline gate costs one executed point before the cheap checks run.** A broken axis declaration is caught earlier by `indicators.py`, so the wasted work is one point. Accepted rather than designed around with a two-stage preflight.

---

## Integration Strategy

The tools slot into the delivered runbook at steps 5 and 9, with the cleanliness gate additionally after step 8 and after step 9 — the proof-of-life's three sites, preserved.

**One step insertion is owed to Item 2 [L3], and it is a reordering, not a precondition line.** The delivered runbook runs preflight at step 5, chooses the route at step 7, and executes at step 8. But preflight's identity gate reads `package_identity.json`, which the adapter emits *at load*, and its baseline gate reads `baseline_result.json`, which only an executed point produces — so both inputs come into existence two steps after the step that consumes them. Step 7's own fail-closed conditions ("the chosen route cannot load the package; the adapter's own self-check fails") already presuppose a load that has not happened yet. The corrected order:

> **load the route → emit `package_identity.json` + execute the pinned baseline point → preflight gates → … → execute points**

A new step sits before the current step 5: *prepare the execution route and execute the manifest's pinned baseline point*, calling the route, depositing both documents into `results/`, and failing closed when the route cannot load the package or the adapter's self-check fails (those conditions move here from step 7). Step 7 keeps the route-choice **rationale** and the glue disclosure, and states plainly that the rationale is recorded after the route was first exercised.

Nothing is replaced. `exploration/stellarator_e2e/study/` stays as the pre-capability record, unedited. `verify_stellaris.py` and `run_stellaris.py` keep their own knowledge. Execution stays on the stock teax lifecycle through the two named routes.

---

## Validation Approach

Tests under `tests/study/`, on Item 3's delivered `package_copy` factory.

| File | Covers |
|---|---|
| `test_identity.py` | The recipe's canonical text byte for byte; `kind: "sealed"` reduces to the sealed fingerprint; `adapter_source_digest` equals the digest over the sorted adapter lines (S1); recompute-vs-declared mismatch fails; a missing declared file fails |
| `test_operand_bindings.py` | **The L1 de-risk, and the first thing built.** Every one of the five catalog constraints resolves every `feature_ref` operand through `operand_bindings()`; each resolved key exists in the package's inputs or is returned by `evaluate()`; a removed binding, an unknown key, and an ambiguous entry each fail closed naming the constraint and operand |
| `test_preflight_gates.py` | Each of the six checks passes on the real package copy; the results document validates against its schema, carries every input digest, and maps onto record §9's five rows (S2) |
| `test_preflight_negatives.py` | **Missing declared key** → non-zero, message names the key; **key naming a produced channel** → non-zero, message says *computed quantity*; **dirty package** → non-zero naming the file; **wrong fingerprint** → non-zero naming recomputed and declared values; **stale manifest** → non-zero naming which fingerprint drifted. Each asserts the results document was still written complete with the failing check marked `fail` and the others carrying their real outcome (D9) |
| `test_accept_set.py` | Modifying a **third** sealed artifact makes the adapter's loader refuse with `SealVerificationError`; modifying either declared glue file still loads. Invariant 3 |
| `test_lineage_refusal.py` | Create a store over 2 points; touch an allowed glue file → recomputed effective fingerprint changes → `create_or_open` raises `IncompatibleStore`. Repeat changing only `era_adapter.py`, and again changing only `oracle_entry.py` — three declared sources, three refusals (Invariant 4, D13) |
| `test_glue_mapping_agreement.py` | **[L2]** The adapter's `g3` values and `oracle_entry.glue_values()` are the same call — asserted by driving one point through both the adapter's proposal construction and the shim directly and requiring identical values, so the two mappings cannot drift |
| `test_verify.py` | Stratification covers every observed verdict combination; the derived seed is reproducible from the recorded fields (N2); a planted channel deviation above tolerance fails naming case and channel; a planted verdict mismatch fails naming the constraint; a missing `operand_bindings` attribute fails closed; the summary validates against its schema and is a superset of the committed file's field set |
| `test_committed_store.py` | **[S4]** One read-only `StudyQuery` open of the committed proof-of-life store: `inputs`, `verdicts`, and `catalog` are populated as D7 assumes. Read-only; the store is never written |
| `test_promotion_equivalence.py` | The availability sweep reproduces `availability_sweep.csv` byte-for-byte in the default suite; the 948-point grid reproduces `design_search_R_a.csv` byte-for-byte behind `-m slow` |
| `test_generic.py` (**extend the delivered file [L5b]**) | Grep-clean for the four generic modules. Two delivered assertions are updated, not replaced: `scripts/study/*.py` becomes `["common.py", "identity.py", "indicators.py", "manifest.py", "preflight.py", "verify.py"]`, and `schemas/*.json` gains `baseline_result.v1.schema.json`, `package_identity.v1.schema.json`, `preflight_results.v1.schema.json`, `verification_summary.v1.schema.json` |

Manual verification at implementation: re-run the item-start probe (the package may have been regenerated); run `preflight.py gates` and `verify.py` against the real package and diff the summary against the committed one field by field.

---

## Coordination

**Owed to Item 2 (delivered — the orchestrator applies these to the runbook).**
1. **A step insertion before step 5 [L3]**: *prepare the execution route and execute the manifest's pinned baseline point*, depositing `package_identity.json` and `baseline_result.json` into `results/`. Step 7's two fail-closed conditions move to it; step 7 keeps the route rationale and the glue disclosure and states that the rationale is recorded after the route was first exercised.
2. No other ask. The annex path, the six annex section names, record §9's five rows, and the snapshot's `adapter_source_digest` shape are all adopted as delivered.

**Owed to Item 3 (delivered — the orchestrator applies these; this item edits none of Item 3's files).**
1. The stellarator `manifest.json` oracle block's *values*: `sys_path: "exploration/stellarator_e2e/studies"`, `module: "oracle_entry"`, `callable: "evaluate"`, `note` stating the generic signature and the `operand_bindings` companion. Kind stays `python_callable`; the `cli` amendment is declined.
2. `tests/study/test_generic.py`: relax the two file-set assertions to the extended lists above.
3. `manifest.tool_source_digest()`: add the `files` list to its return, so a record can tell whose revision it is reading. Without it, one recipe id means two things across three tools (Risks).

**Authored by this item, additively, in Item 3's directory under its D9 convention:** `scripts/study/schemas/{package_identity, baseline_result, preflight_results, verification_summary}.v1.schema.json`. None of Item 3's three schema files is edited.

---

## Next-Stage Handoff

**Fixed for the plan.** The identity document, its `kind` discriminator, the `effective-executable-fingerprint/v1` recipe and its canonical text, and the `adapter_source_digest` mapping (D2, D3, D4, S1); the single identity seam at `loader.load()` (probe-confirmed); the published operand-binding contract and verify's fail-closed rule (D12, Invariant 9); `g3` through the shim and the three-file declared source set (D13, Invariant 4); the six preflight checks with their §9 row mapping and the always-complete results document (D9, S2); store sampling with the four-step per-case procedure (D7); the shim's three surfaces and the manifest oracle values under the delivered closed schema (D5, D6); the summary field list above; per-store sampling with `K=12` and the written-out derived seed (D8, N2); the shared `common.py` and preflight's freedom from teax (D10); the annex's six runbook-named sections (L6); promotion equivalence as a marker-gated regression (D11); the eleven invariants; the eleven test files.

**Open for the plan.** Exact error-message wording, each of which must locate its fault; whether `promotion_equivalence.py` exports to `tmp_path` or a gitignored scratch directory; the canonicalization used for `operand_bindings_digest`.

**De-risk first, in this order.**
1. **`test_operand_bindings.py` against all five real constraints, before `verify.py` is written.** This is review L1 and the only design-changing finding; B4 now rests on the package publishing bindings, and the plan proves that publication is possible before anything consumes it.
2. **Promotion equivalence's 19-point availability sweep.** The smallest complete exercise of the promoted route — adapter, shim, identity document, definition, export. If those rows do not reproduce byte-for-byte, every later gate is being built on a route that is not the proof-of-life's.
3. **The read-only open of the committed store (S4).** Minutes, and it removes the last unprobed assumption in D7.

**Review disposition.** All findings from `design-review.md` (APPROVE-WITH-FIXES) are folded. **L1** → D12, B4 restated, Invariant 9, `test_operand_bindings.py` as de-risk 1. **L2** → D13, Invariant 4 extended to three sources, `test_glue_mapping_agreement.py`. **L3** → the step insertion in Integration Strategy and Coordination. **L4** → D9 rewritten, Invariant 6 narrowed to torn writes. **L5** → (a) D6 and the shim's `sys_path`/bare-module form, with the namespace-import finding dropped as moot; (b) `test_generic.py` extended, both assertions named; (c) per-tool digest in `common.py`, `files[]` required, recipe-id decision stated in Risks. **L6** → the annex's six sections taken verbatim from the runbook, with the deletion condition homed inside `§ Loader exception and glue`. **S1–S5** → snapshot mapping, gate→§9 table, contract-sourced `source_local_identity`, `test_committed_store.py`, the residual-staleness sentence. **N1–N3** → the Appendix note below, the written-out seed derivation, the import-path note. Nothing touched the probe-backed core: the identity document, the effective fingerprint, or D1–D11 beyond D6's binding and D9's rewrite.

---

## Appendix: Design probe results

`.project/active/run-study-quality-tools/probe_effective_fingerprint.py`, run 2026-08-19 against the committed package on the era worktree. Throwaway; it never moves to `scripts/`.

```text
[P3] runtime_contract_version=1.0.0 artifacts=139 differing=2
     -> ['inputs/system_design.json', 'pipelines/mfe_stellarator.yaml']
[P1] sealed    = ad9120413ebda3770f0e8de2eef39711b9bc931b5e141748d912b4baa60ffa2d
[P1] effective = badcfeae82991f51e9d51b01ebe228fe165a70255531b42757f913451a2f072e
[P1] 3/3 completed
[P1] baseline LCOE=275.2642200420774 rel=2.81e-13 verdicts={beta_ok: satisfied,
     net_positive: satisfied, recirc_ok: satisfied, tbr_ok: satisfied, wall_load_ok: satisfied}
[P1] evidence provenance fingerprint == effective: True
[P2] effective after adapter-source change = 8a13772aad903d720e9d66650d83c6330c7b2ad2b9849387eb21372187f4e68b
[P2] refused as designed: IncompatibleStore: store bound to Compatibility(...)
```

**P3** re-runs the item-start probe: the adapter branch is live, and its accept-set is exactly the two documented files. **P1** confirms B1 — the era stack accepts a computed identity at `loader.load()` and carries it into evidence provenance, with the baseline point reproducing the pinned headline. **P2** confirms B2 — changing only the adapter's source bytes makes the pre-existing store refuse, the concept design's unowned proof 5 demonstrated on real code.

**One honest difference [N1].** The probe's canonical text emits a single `adapter <digest>` line; the design's recipe emits one `adapter <path> <sha256>` line per declared source. The refinement is right and nothing rests on the probe's exact bytes, but the probed canonical text is not the designed one. The probe confirmed the *mechanism* — that a computed identity is accepted and that changing its inputs makes a store refuse — not the recipe's byte layout, which `test_identity.py` pins.

---

**Next Step:** After approval → `/_my_plan`.
