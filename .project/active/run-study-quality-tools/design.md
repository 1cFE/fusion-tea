# Design: Quality Tools and Era Adapter Promotion (RUN-STUDY Item 4)

**Status:** Draft
**Owner:** Reid W
**Created:** 2026-08-19
**Branch:** `feat/stellarator-mbse-demo` · **Commit at design:** `c34561fb`
**Epic:** RUN-STUDY, Item 4

---

## Overview

Promote the proof-of-life's generic mechanical gates into `scripts/study/preflight.py` and `scripts/study/verify.py`, isolate the era workarounds in a package-local, self-checking `era_adapter.py` that binds teax to an honest executable identity, and write the package annex the runbook links per step.

## Related Artifacts

- **Spec:** `.project/active/run-study-quality-tools/spec.md` (Accepted — the contract)
- **Epic:** `.project/backlog/epic_run_study_capability.md` — Item 4
- **Concept design:** `.project/concepts/run-study-skill-design.md` (Tools, manifest/adapter, Required Invariants, Validation Strategy) · **review:** `run-study-skill-design-review.md` (C4, C5, M6, m3)
- **Upstream seams (design against these, not their in-flight code):** `.project/active/run-study-indicators/design.md` (Item 3 — `manifest.py`, schemas, both digest recipes, typed oracle object) · `.project/active/run-study-contract/design.md` + `plan.md` Phase 3 (Item 2 — record §9, snapshot `arms[].verification`, annex path D9)
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

**Lineage refusal is already built; it just needs an honest input.** `StudyStore.create_or_open` binds the compatibility tuple on create and raises `IncompatibleStore` on mismatch (`store.py:126-151`). The probe changed only the adapter's source bytes, recomputed the effective fingerprint, and the pre-existing store refused — which is the concept design's unowned proof 5, mechanically.

**The store speaks the generic vocabulary; the CSV does not.** `CaseView.inputs` is keyed by qualified entry keys and `CaseView.outputs` by qualified channel names (`query.py:123-134`), which is exactly the vocabulary the manifest, the contract's `predicate_ir`, and the oracle seam all use. The committed CSVs are keyed by study-chosen short names (`R`, `a`, `lcoe`), which no generic tool can resolve without being told the mapping.

**The oracle has no seam today.** `verify_stellaris.compute()` reads a module-global `IN` dict and returns 60-odd oracle-named channels (`verify_stellaris.py:49,379`); `__main__` prints the fixed baseline. The mapping the proof-of-life supplied by hand — CSV column → oracle input, oracle name → package channel (`run_design_search.py:372-374,391-392`) — is package knowledge with no home.

**Namespace imports reach the package directory.** With the repo root on `sys.path`, `importlib.import_module("exploration.stellarator_e2e.studies.oracle_entry")` resolves through implicit namespace packages (probed). So the manifest's existing `python_callable` oracle object can name a shim beside the manifest with no new schema field.

**Repo conventions (from Item 3's research, unchanged here):** tests under `tests/study/` with a `package_copy` factory in `conftest.py`; pytest `pythonpath = ["."]`; no `__init__.py` under `scripts/study/`; ruff line length 100.

---

## Core Concept

Everything here follows from one move: **the adapter stops reporting an identity it did not earn, and starts publishing a small document that says exactly what it bypassed and what identity that produces.** The document is the seam. The adapter writes it; teax binds the identity in it; generic preflight gates on it by recomputation; generic verify copies its glue disclosure into the verification summary; the record snapshots it. No generic tool imports the adapter, and no package fact leaks into a tool — the tools handle a typed document, not knowledge.

That one document makes the rest fall out. The identity gate becomes honest by construction because it recomputes rather than trusts: from the document's own declared inputs plus the files on disk. It works unchanged when the adapter is gone, because the document carries a `kind` discriminator and the no-adapter case is the degenerate one — an empty allowed-modified set, which turns the same gate into a full seal check. Gate the manifest's currency separately, against the two contract fingerprints that glue edits cannot touch, and the two halves together are complete without either one lying.

The tools then stay small and boring. Preflight is five named mechanical gates over documents, package files, and git; it never executes and never imports teax. Verify samples the store (the only source whose vocabulary is package-qualified), calls a package-owned oracle through one generic signature, re-derives every verdict from the package's own `predicate_ir`, and writes one summary document. The adapter keeps everything else: the loader exception, the glue rungs, the self-checks, the era-pin assertion, and its own deletion condition.

---

## Key Bets

- **B1.** Returning a computed fingerprint from `loader.load()` is accepted by the whole era stack, and no component cross-checks executable identity against the seal. *If false → the effective-fingerprint plan needs a teax change, which is a Non-Goal, and the item stalls on an upstream dependency.* **Probed and confirmed** (Appendix, P1).
- **B2.** A store bound to one effective fingerprint refuses to open under another, so glue drift and adapter drift are refused rather than silently mixed. *If false → the review's C4 is only half-fixed: identity is honest but nothing enforces it.* **Probed and confirmed** (Appendix, P2).
- **B3.** The set of files whose content can change a glue value or the loader's accept-set is enumerable by the adapter and stable enough to declare. *If false → the effective fingerprint is honest about the files it names and blind to the one that actually moved a number, which is worse than the sealed fingerprint because it looks earned.* This is why the adapter's declared source set includes the oracle module it calls for `g3` — see Invariant 4.
- **B4.** Every verdict in the catalog can be re-derived generically: each `predicate_ir` operand resolves to a literal from the IR, a bound input from the case or the package's inputs files, or a computed channel from the oracle's return. *If false → verify.py needs package-specific threshold knowledge, which the spec forbids, and verdict re-derivation stays welded to the package.*
- **B5.** Sampling the store rather than the exported CSV does not weaken the verification claim, because the export is a deterministic function of the store produced in the same run. *If false → the record ships a CSV that nothing checked, and "verified" means less than a reader assumes.* Mitigated for this package by promotion equivalence, which compares the exported CSVs byte-for-byte.

---

## Key Decisions

- **D1. The baseline gate consumes an already-executed result document, never a prepared-evaluator handle.** The route executes exactly the manifest's pinned baseline point and writes `baseline_result.json`; preflight reads it as data and compares it to the manifest's `baseline` block. *Rejected: preflight takes a prepared-evaluator handle (it would make preflight a library imported by the adapter-importing definition, put typed-input construction — package knowledge — inside a generic tool, and give the tool a live execution path the spec says it must not own).*
- **D2. The adapter emits one document with two blocks — `identity` and `glue_ledger` — not two documents.** One write, one digest, one path in the record; preflight reads only `identity`, verify reads only `glue_ledger`, and the glue ledger is never wanted without the identity that scopes it. *Rejected: two documents (doubles the plumbing and lets the two drift out of step for the same run).*
- **D3. The identity document is typed by `kind`, and the no-adapter case is the degenerate member.** `{"kind": "sealed"}` has an empty allowed-modified set and the sealed fingerprint as its digest; `{"kind": "effective"}` carries the three inputs and the recipe. One gate covers both. *Rejected: an adapter-only document with preflight branching on its absence (an optional gate input is how gates rot, and the deletion condition would then change preflight's behavior).*
- **D4. `scripts/study/identity.py` is a new generic sibling module** owning the identity-document schema, the `effective-executable-fingerprint/v1` recipe, the sealed-case emitter, and the recompute-and-compare logic. Imported by `preflight.py`, `verify.py`, and the adapter. *Rejected: putting the recipe in Item 3's `manifest.py` (it is not a manifest fact, and the spec forbids editing Item 3's files beyond one pre-authorized amendment); rejected: implementing it inside the adapter (preflight could then only trust, not recompute).*
- **D5. The oracle entry point is a package-owned shim module beside the manifest, `exploration/stellarator_e2e/studies/oracle_entry.py`; `verify_stellaris.py` is untouched.** The shim owns both mappings — qualified entry key → oracle input, oracle output name → qualified package channel — and the `_profile_integral` memoization. *Rejected: a CLI on `verify_stellaris.py` (edits the independent oracle for study-seam reasons, invents a wire format for one consumer, and pays a subprocess per sampled point).*
- **D6. The manifest's oracle object stays `{"kind": "python_callable"}`; the pre-authorized `{"kind": "cli"}` amendment is declined and stays unused.** `python_callable` is given a defined generic signature: `evaluate(point: Mapping[str, float]) -> Mapping[str, float]`, point keyed by qualified entry keys, return keyed by qualified channel names. Only the field *values* change in Item 3's manifest (module, callable, note) — no schema change, no new field. *Rejected: `{"kind": "cli"}` (Item 3's D6 rejected inventing a CLI protocol for a single future consumer; nothing about this consumer changed that).*
- **D7. `verify.py` samples the study store through `StudyQuery`, not the exported CSVs.** The store is the primary evidence and the only source keyed by qualified names; a CSV sampler would need a column→key map that is study knowledge a generic tool may not hold. *Rejected: sampling the CSVs as the proof-of-life did (it verified the shipped artifact, which is the one thing this loses — recovered for this package by promotion equivalence, and named as B5).*
- **D8. Sampling is scoped per store, `K = 12` by default with stratification as a floor, and the seed defaults to a value derived from the study id and the store's compatibility digest.** `--seed` overrides for a deliberate re-draw; the effective seed is always recorded. *Rejected: a fixed default seed (every study then samples the same stratum positions, and the number is magic); rejected: a required `--seed` (invites an arbitrary choice where a deterministic one exists).*
- **D9. Preflight writes its results document only on a full pass.** A failed gate exits non-zero with a located stderr message and writes nothing, following Item 3's no-partial-output rule. *Rejected: writing a document with failed gates in it (a record could then snapshot a failed gate set and read as gated).*
- **D10. Preflight and verify share one small internal module, `scripts/study/common.py`** — the git-clean gate, atomic deterministic document writing, and the exit/error convention. The teax import and store access stay inside `verify.py`, so `preflight.py` never imports teax. *Rejected: two independent scripts (two implementations of "clean" can disagree about what clean means, and that disagreement is invisible).*
- **D11. Promotion equivalence lives at `exploration/stellarator_e2e/studies/promotion_equivalence.py` and is kept as a marker-gated regression, not retired as one-time evidence.** The 19-point availability sweep runs in the default suite; the 948-point grid runs behind `-m slow`. It is deleted with the adapter. *Rejected: running it once and deleting it (it is the only thing that would catch a silent behavior change in the adapter or the promoted definition while the adapter exists).*

---

## Architecture

```text
  era_adapter.py  ──loader.load() -> (module, EFFECTIVE fingerprint)──►  PreparedEvaluator
   (package-local)                                                            │
        │  writes                                                             ▼
        ▼                                                        StudyDefinition ─► StudyStore
  package_identity.json  {identity{kind,recipe,inputs,digest}, glue_ledger[]}       (refuses a
        │                                                                            different
        ├───────────────► preflight.py ──► preflight_results.json                    identity)
        │   (recompute,     │  also reads: axis declaration (Item 3), manifest
        │    never trust)   │  (manifest.py), package inputs + both contracts, git
        │                   ▲
        │        baseline_result.json  ◄── one point, executed by the route
        │
        └───────────────► verify.py ──► verification_summary.json
                             │  samples StudyQuery cases; calls the manifest's
                             │  oracle callable; re-derives verdicts from predicate_ir
                             ▼
                       oracle_entry.py (package-owned shim) ──► verify_stellaris (untouched)
```

**Direction of trust.** Every arrow into a generic tool carries data. `preflight.py` and `verify.py` import `manifest.py`, `identity.py`, `common.py`, and — for verify — teax and whatever module the manifest names. Neither imports the adapter, and the adapter importing `identity.py` is the allowed direction.

**Integration points.** *Upstream:* Item 3's `manifest.py`, the three schema files, and the axis-declaration file; the package's `inputs/*.json`, `contracts/model_contract.json`, `contracts/package_contract.json`. *Sideways:* the era teax worktree, resolved from the ambient environment by the caller, never named in a tool. *Downstream:* Item 2's record — `preflight_results.json` into §9, `verification_summary.json` and `package_identity.json` into `results/` and the snapshot's `arms[].verification`, `arms[].effective_executable_fingerprint`, and `glue_ledger`.

---

## Required Invariants

1. **Generic means grep-clean.** `preflight.py`, `verify.py`, `identity.py`, and `common.py` contain no package name, no key prefix, no oracle name, and no adapter import. Tested by grep, as Item 3's Invariant 6 is.
2. **The identity gate recomputes; it never trusts.** Preflight's verdict is a function of the document's declared inputs and the bytes on disk, never of the document's asserted digest alone.
3. **The accept-set is exactly `{TAMPER on the declared allowed-modified files}`.** Any other diagnostic kind, any other path, any era-version mismatch still refuses. Asserted by a negative test that modifies a third sealed artifact.
4. **The adapter's declared source set covers every file whose content can change a glue value or the accept-set.** Today that is `era_adapter.py` plus the oracle module it calls for `g3`. A file that feeds a number into a run and is outside the set makes the effective fingerprint look earned while being blind.
5. **Identity continuity across the run.** The identity preflight gated, the identity the store bound, and the identity present after the run are one value. Verify asserts it and records it.
6. **No partial output.** A non-zero exit from either tool writes zero bytes of result document and leaves no file behind.
7. **Interpretive facts never gate.** Every non-zero exit is one of the enumerated mechanical failures; a valid empty result exits 0.
8. **Adapter-owned facts are checked by the adapter.** The dead-filler assertion, the era-pin prerequisite, and the accept-set run on every adapter-route load and fail closed. No generic tool asserts any of them.
9. **The manifest holds no era, glue, or allowed-modified-file fact.** Deleting the adapter requires no manifest edit.
10. **Every point executes through `StudyRunner`.** Neither tool constructs an evaluator or runs a point.

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
               "digest": "<the effective executable fingerprint>"},
  "glue_ledger": [{"rung": "g3", "keys": ["..."], "supplies": "...",
                   "independently_verified": false, "note": "..."}] }
```

*The recipe*, `effective-executable-fingerprint/v1`, is Item 3's canonical-text pattern under its own id: line 1 the recipe id, then `sealed <hex>`, then one `modified <path> <sha256>` line per allowed-modified file sorted by path, then one `adapter <path> <sha256>` line per declared adapter source sorted by path; the digest is sha256 of that UTF-8 text. For `kind: "sealed"` both lists are empty and the digest is defined to be the sealed fingerprint itself, so the recipe reduces to identity rather than inventing a second value.

*The gate*, used by preflight and re-asserted by verify: recompute the digest from the document's declared inputs and the current bytes; require equality with `identity.digest`; require every sealed artifact **outside** `allowed_modified_files` to match `artifact_hashes`; require every declared file to exist. Three failure messages, each naming the file.

*The sealed emitter*, one call for the no-adapter route, so deleting the adapter does not leave a route with no way to publish its identity.

### `scripts/study/preflight.py` — five named gates

*The baseline result document* the route hands it (D1), `study-baseline-result/v1`, is the smallest thing that can discharge the gate: the identity it executed under, the point it executed (qualified entry keys), the resolved channel values, and the verdicts by their three identities.

```jsonc
{ "schema_version": "study-baseline-result/v1",
  "executed_under": {"identity_digest": "...", "store_id": "...", "case_id": "..."},
  "point": {"<qualified entry key>": 12.7},
  "channels": {"<qualified channel>": 275.2642200420774},
  "verdicts": [{"constraint_id": "...", "definition_qualified_name": "...",
                "source_local_identity": "wall_load_ok", "status": "satisfied"}] }
```

Two subcommands. `preflight.py gates` runs all five and needs `--package`, `--manifest`, `--groups`, `--identity`, `--baseline-result`. `preflight.py clean` runs the cleanliness gate alone, for the post-run and post-verify sites the proof-of-life used (`run_design_search.py:358,414,443`). Both emit `study-preflight-results/v1`: a list of `{gate, status, checked, detail}` plus the digests of every input document, written once at the end (D9).

| Gate | What it checks | Fails when |
|---|---|---|
| `declared_keys` | Every key in Item 3's axis declaration exists in the package's inputs and classifies against `contract.parameters`; suffix siblings reported advisory only | key absent; key names a produced channel (reported as a **computed quantity**, policy §2.1); key unclassifiable |
| `identity` | `identity.py`'s gate, plus equality with the identity the baseline result was executed under | recompute mismatch; a sealed artifact outside the allowed set differs; the document is missing or malformed; the baseline ran under a different identity |
| `manifest_currency` | The manifest's `fingerprints.recorded_provenance.{executable_fingerprint, semantic_fingerprint}` against the live `package_contract.json` and `model_contract.json` | either differs — the manifest's baseline, ties, oracle, and objective catalog were pinned against a different package generation and must be re-declared |
| `baseline_headline` | The baseline result's headline channel against the manifest's pinned value at rel < 1e-9, and its verdicts against the manifest's pinned verdicts by `source_local_identity` | value off tolerance; any verdict differs; the pinned channel is absent from the result |
| `package_clean` | `git status --porcelain` over the package tree | any output |

The two contract fingerprints in `manifest_currency` are the honest choice precisely because glue edits cannot touch them: neither contract file is in the allowed-modified set, so this gate can only refuse a stale manifest, never pass one by looking the other way. Item 3 reports the same drift as a non-gating warning; the asymmetry is deliberate and stated in the spec.

### `scripts/study/verify.py` — the generic sampler

Reads `--package`, `--manifest`, `--identity`, `--store` (repeatable), `--sample-size`, `--seed`, `--out`. Per store: load cases through `StudyQuery`, keep `completed` ones, stratify by the observed verdict combination, take one case per stratum, fill the remainder randomly to `K` (stratification is a floor, never a cap), then per sampled case —

1. Call the manifest's oracle callable with `case.inputs` and receive qualified channel values.
2. Compare every channel the manifest's objective catalog names plus every channel a `predicate_ir` operand references, at rel < 1e-9, tracking the worst deviation and where it occurred.
3. Re-derive each verdict from `predicate_ir`: a literal operand comes from the IR, a bound operand from `case.inputs` when the study swept it and from the package's `inputs/*.json` otherwise, a computed operand from the oracle's return. Compare to the recorded verdict.
4. Copy the identity document's `glue_ledger` entries with `independently_verified: false` into the summary as the named not-independently-verified inputs.

The bound-operand rule is the one place this improves on what it promotes: the proof-of-life read `recirc_ok`'s threshold and the wall-load limit by literal key name (`run_design_search.py:367-370`), which a generic tool cannot do and does not need to.

`verification_summary.json`, `study-verification-summary/v1`, is a superset of the committed file and of Item 2's `arms[].verification` block (`run-study-contract/design.md:254`, plan Phase 3):

```jsonc
{ "schema_version": "study-verification-summary/v1",
  "tool": {"path": "scripts/study/verify.py",
           "source_digest": {"recipe": "tool-source-digest/v1", "digest": "...", "files": ["..."]}},
  "command": ["scripts/study/verify.py", "..."],       // repo-relative, no absolute paths
  "teax": {"module_path": "<repo-relative or absolute-outside>", "revision": "..."},
  "package": {"path": "...", "package_name": "...", "git_clean": true},
  "identity": {"kind": "...", "digest": "...", "matches_preflight": true},
  "manifest": {"path": "...", "schema_version": "...", "digest": "..."},
  "oracle": {"kind": "python_callable", "module": "...", "callable": "evaluate"},
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
  "verdict_mismatches": [],
  "not_independently_verified": [{"rung": "g3", "keys": ["..."], "note": "..."}],
  "worst_channel_rel_dev": 5.67e-16,
  "outcome": "pass" }
```

Every field of the committed `verification_summary.json` survives by name or by a named generalization: `sampled_rows_per_study` → per-store `sampling.sampled_rows`; `sampling` → `sampling.scheme`; `package_git_clean` → `package.git_clean`; `glue_note` → `not_independently_verified`. The record needs no field this does not carry.

### `exploration/stellarator_e2e/studies/era_adapter.py` — the temporary adapter

Package-local, named temporary in its first line, and the only home for six things: the loader exception (the `GlueAwareLoader` accept-set, Invariant 3); the glue rungs g1–g3 exactly as the proof-of-life documented them; the self-checks, above all the dead-filler assertion, which moves *into* the adapter and runs on every load rather than in a tool; the era-pin prerequisite, asserted not merely recorded — the adapter checks it is running under the pinned worktree at `fa0e06a` and fails closed otherwise; the effective-fingerprint computation via `identity.py`'s recipe; and the identity-document emission.

Its declared source set (Invariant 4) is `era_adapter.py` and `verify_stellaris.py`, because `g3` recomputes CAS27 per point from the oracle's `special_materials` (`run_design_search.py:188-201`). A change to the oracle therefore changes the executable identity and retires existing stores — correct, and costly enough to name in Risks.

**Deletion condition, stated in the adapter and in the annex:** the stock `ProvisionalPackageLoader` accepts the regenerated package with `strict=True`. When it does, the adapter is deleted whole, the study-local definition swaps the adapter's loader for the stock one and `identity.py`'s sealed emitter, the sealed fingerprint becomes the identity again, `promotion_equivalence.py` is deleted with it, and nothing else changes. No partial retirement, no dormant compatibility branch.

### `exploration/stellarator_e2e/studies/oracle_entry.py` — the package-owned oracle seam

`evaluate(point) -> channels`, per D6. Owns the two mappings and nothing else: qualified entry key → `verify_stellaris.IN` name, and oracle output name → qualified channel name. Saves and restores `IN` around each call as the proof-of-life did (`run_design_search.py:144-152`), and memoizes `_profile_integral`. It imports `verify_stellaris` and modifies nothing in it.

### `exploration/stellarator_e2e/studies/ANNEX.md` — the package annex

One section per runbook step that links it (Item 2's D9 pins the path and the per-step link; this item writes the content): the era pin and why it exists, including that current teax main's refusal of the v1.0.0 seal is principled and is not to be chased upstream; the oracle's parameterization — how a point becomes oracle inputs and what the oracle returns; the glue ledger rungs g1–g3 and what each supplies that the model does not; the loader exception and its exact accept-set; the package-specific validity masks, of which `R > a + 2.25 m` is one and is a derived geometric bound from held-fixed inputs, not a design screen (`run_design_search.py:113-118`); and the adapter's deletion condition verbatim. Nothing in it is a rule; it is package fact, linked and never inlined.

### `exploration/stellarator_e2e/studies/promotion_equivalence.py` — the equivalence harness

A study-local direct-API definition (`StudyRunner` + `PreparedListStrategy`, the same route the proof-of-life used and the only one the era supports for coordinated blocks) that reproduces both proof-of-life studies under the promoted structure and exports both CSVs to a scratch directory. Driven by `tests/study/test_promotion_equivalence.py`, which diffs them byte-for-byte against the committed files. The committed proof-of-life directory is read, never written.

---

## Non-Goals

- A second execution facade, a generic runner, or any hand-rolled sweep loop.
- Package knowledge — names, key prefixes, thresholds, oracle field names — inside the generic tools.
- Upstream teax or sysml-codegen changes, and any attempt to make current teax main accept the v1.0.0 seal.
- Interpretive gating of any kind.
- Authoring `manifest.py`, the manifest schema, Item 3's JSON Schemas, `indicators.py`, or the stellarator `manifest.json` — Item 3. This item asks Item 3 for two value changes and one additive schema file, listed in the handoff.
- Authoring `SKILL.md`, `runbook.md`, the record template, or the annex *link* — Item 2.
- Migrating `verify_stellaris.py`'s or `run_stellaris.py`'s oracle knowledge into the manifest.
- Running a new study, plotting, or reporting.

---

## Implementation Notes

- **The only identity seam is `loader.load()`'s second return value.** Do not thread the effective fingerprint anywhere else; everything downstream picks it up (Appendix, P1).
- **Do not `db.unlink()` in the promoted definition.** The proof-of-life deleted the store on every run (`run_design_search.py:288-289`), which would make the lineage-refusal test unable to find a store to refuse. Deleting is a caller's choice, not the definition's.
- **`pkg/stellarator_tea` is a symlink to `generated/`.** The package root is `exploration/stellarator_e2e/generated`; both paths reach the same tree.
- **The era teax path is the caller's, never the tool's.** `verify.py` imports `simkit` from the ambient environment and records where it came from. The pin lives in the annex and the invocation.
- **Byte-for-byte CSV reproduction depends on proposal construction, not only on physics.** The glue values are computed per point from the oracle, so the promoted definition must build proposals from the same rungs in the same order; float text is `repr`-stable but the values must be identical, not merely close.
- **Extend Item 3's `package_copy` factory; do not fork it.** Its two rules — assert before mutating, re-pin unless the test is about the pin — apply here verbatim, and the mutation tests below need a third convenience: mutate a glue file *and* re-emit the identity document, or not, depending on which gate the test is aiming at.

---

## Potential Risks

- **A change to `verify_stellaris.py` retires every existing store.** That is the correct consequence of Invariant 4 — the oracle feeds numbers into the run — but it is a sharp edge for anyone editing the oracle for unrelated reasons. Mitigation: the annex states it, and the refusal message names the file whose digest moved.
- **Promotion equivalence may fail on a float-text difference rather than a physics difference.** Mitigation: the test reports the first differing line with both values, so a formatting difference is distinguishable from a numeric one in one look; and the availability sweep (19 rows) fails first and cheaply.
- **The CSV the record ships is not what verify samples (B5).** Mitigation for this package is promotion equivalence; going forward it rests on the export being produced from the store in the same run. Named here rather than papered over.
- **Item 3's `tool-source-digest/v1` file list names three schema files.** This item adds a fourth schema file and three tool modules. If tool revision is reported over Item 3's fixed list, a record's "tool revision" silently means "indicators' revision". Mitigation: this item's tools emit `{recipe, digest, files[]}` with the file list included, and the handoff asks Item 3 to do the same.
- **Preflight's baseline gate costs one executed point before the cheap gates run.** A broken axis declaration is caught earlier by `indicators.py`, so the wasted work is one point. Accepted rather than designed around with a two-stage preflight.
- **The adapter and the tools are being built against Items 2 and 3 in flight.** Every consumed name is cited to an accepted design, not to code. The plan stage binds to the real files and re-runs the item-start probe, because the package may be regenerated before then.

---

## Integration Strategy

The tools slot into the runbook's steps 5 and 9, and the cleanliness gate additionally after step 8 and after step 9 — the proof-of-life's three sites, preserved. The runbook's preflight step gains one precondition Item 2's plan should record: **the route executes the manifest's pinned baseline point and hands preflight the result** (D1). That is a one-line addition to step 5's `**Calls:**` block, not a re-ordering.

Nothing is replaced. `exploration/stellarator_e2e/study/` stays as the pre-capability record, unedited. `verify_stellaris.py` and `run_stellaris.py` keep their own knowledge. Execution stays on the stock teax lifecycle through the two named routes.

---

## Validation Approach

Tests under `tests/study/`, on Item 3's `package_copy` factory.

| File | Covers |
|---|---|
| `test_identity.py` | The recipe's canonical text byte for byte; `kind: "sealed"` reduces to the sealed fingerprint; recompute-vs-declared mismatch fails; a missing declared file fails |
| `test_preflight_gates.py` | Each of the five gates passes on the real package copy; the results document validates against its schema and carries every input digest |
| `test_preflight_negatives.py` | **Missing declared key** → non-zero, message names the key; **key naming a produced channel** → non-zero, message says *computed quantity*; **dirty package** → non-zero, message names the file; **wrong fingerprint** → non-zero, message names the recomputed and declared values; **stale manifest** (recorded provenance edited) → non-zero naming which fingerprint drifted. Each asserts no document was written |
| `test_accept_set.py` | Modifying a **third** sealed artifact makes the adapter's loader refuse with `SealVerificationError`; modifying either declared glue file still loads. This is Invariant 3 |
| `test_lineage_refusal.py` | Create a store over 2 points; touch an allowed glue file → recomputed effective fingerprint changes → `create_or_open` raises `IncompatibleStore`. Repeat changing only the adapter's source. Both halves of the effective-fingerprint definition (probe-confirmed mechanism, Appendix P2) |
| `test_verify.py` | Stratification covers every observed verdict combination; the derived seed is reproducible and recorded; a planted channel deviation above tolerance fails non-zero naming the case and channel; a planted verdict mismatch fails naming the constraint; the summary validates against its schema and is a superset of the committed file's field set |
| `test_promotion_equivalence.py` | The availability sweep reproduces `availability_sweep.csv` byte-for-byte in the default suite; the 948-point grid reproduces `design_search_R_a.csv` byte-for-byte behind `-m slow`. The committed files are read only |
| `test_generic.py` | Grep-clean: no package name, key prefix, oracle name, or adapter import in the four generic modules |

Manual verification at implementation: re-run the item-start probe (the package may have been regenerated); run `preflight.py gates` and `verify.py` against the real package and diff the summary against the committed one field by field.

---

## Next-Stage Handoff

**Fixed for the plan.** The identity document, its `kind` discriminator, and the `effective-executable-fingerprint/v1` recipe including its canonical text (D2, D3, D4); the single identity seam at `loader.load()` (probe-confirmed); the five preflight gates, their failure conditions, and the two subcommands (D9); store sampling with the four-step per-case procedure and the bound-operand resolution rule (D7, B4); the oracle shim and the generic `evaluate(point) -> channels` signature (D5, D6); the summary field list above; per-store sampling with `K=12` and a derived recorded seed (D8); the shared `common.py` and preflight's freedom from teax (D10); the adapter's six responsibilities, its declared source set, and its deletion condition; the annex's six sections; promotion equivalence as a marker-gated regression (D11); the ten invariants; the eight test files.

**Open for the plan.** Exact error-message wording, each of which must locate its fault; whether the derived seed is a truncated hex string or an int; the annex's section-to-runbook-step mapping, which needs Item 2's finished runbook; whether `promotion_equivalence.py` exports to `tmp_path` or a gitignored scratch directory.

**Coordination owed to Item 3, all additive, none a schema change to existing files.**
1. The stellarator `manifest.json` oracle object's *values* point at `exploration.stellarator_e2e.studies.oracle_entry.evaluate`, with the note stating the generic signature. Kind stays `python_callable`; the pre-authorized `cli` amendment is declined.
2. Four new schema files in Item 3's `scripts/study/schemas/` directory, under Item 3's D9 convention and authored by this item: `package_identity.v1.schema.json`, `baseline_result.v1.schema.json`, `preflight_results.v1.schema.json`, `verification_summary.v1.schema.json`. Additive files only; none of Item 3's three is edited.
3. `tool-source-digest/v1` emissions should carry their `files[]` list, so a record can tell whose revision it is reading (see Risks).

**Coordination owed to Item 2.** The preflight runbook step gains the baseline-execution precondition (D1). The annex path Item 2 pinned is accepted unchanged.

**De-risk first.** Promotion equivalence's availability sweep. It is the smallest complete exercise of the whole promoted route — adapter, identity document, definition, export — and if the 19 rows do not reproduce byte-for-byte, every later gate is being built on a route that is not the proof-of-life's.

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

**P3** re-runs the item-start probe: the adapter branch is live, and its accept-set is exactly the two documented files. **P1** confirms B1 — the era stack accepts a computed identity at `loader.load()` and carries it into evidence provenance, with the baseline point reproducing the pinned headline. **P2** confirms B2 — changing only the adapter's source bytes makes the pre-existing store refuse, which is the concept design's unowned proof 5 demonstrated on real code.

---

**Next Step:** After approval → `/_my_plan`.
