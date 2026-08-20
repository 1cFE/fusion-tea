# Design: Indicator Tool and Package Manifest

**Status:** Draft
**Owner:** Reid W
**Created:** 2026-08-19
**Updated:** 2026-08-19
**Branch:** `feat/stellarator-mbse-demo` · **Commit at design:** `573c7c79`
**Epic:** RUN-STUDY, Item 3

---

## Overview

`scripts/study/indicators.py` reads a generated teax package's own artifacts and reports, per author-declared axis group, which constraints and objectives a conservative path can reach. `exploration/stellarator_e2e/studies/manifest.json` is the data-only catalog of the stable package facts the tool needs.

## Related Artifacts

- **Spec:** `.project/active/run-study-indicators/spec.md` (accepted — the contract)
- **Epic:** `.project/backlog/epic_run_study_capability.md` — Item 3
- **Item 1 spike:** `.project/active/run-study-reachability-spike/findings.md` (R1–R12, fixture contract), `trace.py`, `cases.py`
- **Concept design:** `.project/concepts/run-study-skill-design.md` — indicator builder, package manifest, Appendix A, Design Principles 1–2/4
- **Downstream seam:** `.project/active/run-study-contract/spec.md` — the record contract that snapshots this tool's output
- **Product-lens:** `.project/active/run-study-indicators/product-lens.md` (gate CLEAR)
- **Design probe (throwaway):** `.project/active/run-study-indicators/probe_lineno.py`
- **Decision records:** `.project/adr/` is absent and `adr.sh` is absent. No ids hand-minted; the decisions this design settles are recorded in Key Decisions below, as the concept design did.

## The Point

Before any study point runs, the agent must be handed deterministic, package-derived facts about what in the model can push back on each proposed axis — so a sweep that can only say "more is better" is surfaced as a model gap instead of published as a design search. **[INHERITED: `.project/concepts/run-study-skill.md` Owner's Words; `.project/concepts/run-study-skill-design.md` Goals — grade: owner]**

Two owner-grade constraints shape every choice below. **[OWNER]** Interpretive facts never gate a study; mechanical failures fail closed. A broken analysis and an empty one must never share an exit code — that is what makes `no_constraint_response` trustworthy enough to hand a user for a ruling. And **[INHERITED: design Principle 4]** generic and package-specific never share a file: the tool names no package, the manifest holds no logic.

This item ladders up to the run-study capability's one new capability. Items 2 and 4 consume its output as a fixed seam: the record snapshots `indicators.json` with its digest and schema version, and `preflight.py`/`verify.py` read the same manifest through the same loader.

## Orchestrator rulings folded in (since spec acceptance)

- **The package annex is Item 4's, not this item's.** The runbook's package-specific companion file lands beside the manifest, authored by Item 4. This item's manifest is data-only and stands alone. This supersedes the Item 2 spec's parenthetical routing of the annex file to Item 3 (`.project/active/run-study-contract/spec.md`, Non-Goals — "the annex file itself lands beside the manifest (Item 3)"). **[OWNER, via orchestrator]**
- **The oracle field records the entry point that exists today**, shaped so a later command form is an additive amendment rather than a rewrite — Item 4's `verify.py` consumes this seam and may add a package-owned CLI. **[OWNER, via orchestrator]**
- **The output schema is versioned from v1 and carries its version inside the output**, because Item 2's accepted record contract snapshots `indicators.json` + digest + schema version into every record. **[OWNER, via orchestrator]**

## Research Findings

**The Item 1 spike is the substrate.** `trace.py` proved the twelve parsing and normalization rules (R1–R12) and reproduced all five Appendix A known answers on semantic fingerprint `c9bc…c261`. This design keeps its trace core almost unchanged — the conservative closure (`trace.py:134-153`), the reference classifier (`trace.py:89-110`), and the constraint-operand join through `predicate_ir` (`trace.py:166-179`) — and replaces its three throwaway parts: the hand parser, the hard-coded objective catalog, and the absent manifest/fingerprint/CLI layer.

**Line numbers are cheap to keep — the spec's weaker bar is not needed.** `yaml.compose()` parses without constructing (nothing is instantiated, so no code executes), and every node carries `start_mark.line`. A ~40-line strict walk over the node tree yields both the data and a line per module and per port. The probe (`probe_lineno.py`) parsed the real 60-module pipeline, then raised on a corrupted value with `…/p.yaml:24 (key path modules.…geom.inputs.R)` and on an injected unknown key with `modules.entry_fusion (line 13)`. So corrupt-artifact errors carry **file, line, and key path**, which is stronger than the spec's accepted fallback and matches the Item 1 fixture contract's "error carries file and line number".

One sharp edge the probe found: `compose` preserves node tags, so `a: !!python/object/apply:os.system [...]` arrives as a node tagged `python/object/apply` (nothing executed). The walker must therefore reject any node whose tag is not the standard `str`/`map` tag, rather than reading `.value` and moving on.

**The entry-point block declares its own inputs paths.** `entry_fusion.inputs` maps each group name to `<Type> ../inputs/<file>.json` (`pipelines/mfe_stellarator.yaml:13-17`). The spike guessed `inputs/<group>.json`; the tool resolves the declared relative path instead, so a renamed inputs file is followed rather than mis-reported as a missing group.

**The contract carries a third constraint identity the spike did not report.** `concrete_entries[]` has `definition_qualified_name` alongside `constraint_id` and `source_local_identity` (`contracts/model_contract.json`). `constraint_id` is hash-suffixed and does not survive regeneration, and the record contract correlates cross-fingerprint constraints by "definition qualified name + local identity" (`.project/active/run-study-contract/spec.md:80`). See D10.

**Package provenance field names, verified on disk:** `contracts/package_contract.json` carries `executable_fingerprint`, `artifact_hashes`, `package_name`; `contracts/model_contract.json` carries `semantic_fingerprint`, `parameters[]` (with `entry_type`, `param_group`, `qualified_name`), `constraint_catalog.concrete_entries[]`, `outputs`.

**Repo conventions.** Tests live under `tests/<area>/` with `tests/conftest.py` at the root providing path fixtures; pytest runs with `pythonpath = ["."]` (`pyproject.toml:50-51`), so `scripts.study.indicators` imports as an implicit namespace package with no `__init__.py`. Ruff line length 100. `jsonschema` 4.26.0 is already resolved in `uv.lock` transitively — the plan adds it as an explicit dependency rather than relying on a transitive one.

## Core Concept

The tool is a **strict reader with a conservative closure on top**. Everything it does splits into two layers, and the split is what makes the exit codes honest.

The lower layer is a *pedantic reader* of the package: it loads the manifest, digests the exact artifacts it is about to read and checks that digest against the manifest's pin, then parses the pipeline YAML and the model contract in a mode where every unrecognized construct raises with a location. Nothing in this layer interprets anything. Every failure here is mechanical, exits non-zero, and emits no report.

The upper layer is the Item 1 trace, unchanged in substance: taint the declared keys, fire any module with a tainted input, taint all of its outputs, iterate to fixpoint, then read off which constraint operands and which manifest-catalog objective channels the taint reached. Every outcome here is a fact, exits 0, and is reported — including the empty one.

The key insight is that **the report is a document, not a stream**. It is assembled entirely in memory and written once, at the end, after every gate has passed. That single property delivers the owner's rule mechanically: there is no code path that can produce a partial report, so a broken analysis cannot look like an empty one.

Three seams keep the layers honest. `manifest.py` owns the manifest schema and the fingerprint recipe, so Item 4's tools read the same file through the same code. The declared axis groups arrive as a data file, so per-key `fan_out | tie` provenance survives into the output and then into the record. And the not-derivable statements are a constant emitted at both the document and the group level, so a group excerpted into a record's per-axis framing section still carries them.

## Key Bets

- **B1.** The generated pipeline YAML keeps its shape across regeneration: a mapping of modules, each with `module_type` and `inputs`/`outputs` maps whose values are the `<type> <ref>` micro-syntax. *If false → the strict reader raises on the regenerated package and no study can run until the reader is updated. That is the intended fail-closed direction, but the capability pauses.*
- **B2.** A raw-bytes digest over the artifacts the tool reads is the right change detector: any edit that changes the trace changes those bytes, and edits that don't matter are rare enough that a deliberate re-pin is an acceptable cost. *If false → either formatting-only churn blocks studies with spurious mismatches, or (worse) a meaningful edit slips past. Mitigated by reporting per-file digests, so a mismatch names the file in one look.*
- **B3.** Conservative module-level reachability still discriminates between axes on real packages. On this package `R` fires 54 of 60 modules. *If false → every axis comes back "reachable" and the intake step adds nothing but latency. The spec makes measuring this a non-goal; it is watched, not fixed.*
- **B4.** One invocation per study, producing one document covering every proposed axis, matches how the record consumes indicators. *If false → the record needs per-axis files and a downstream splitter, and the digest that Item 2 snapshots covers more than the section it is cited from.*

## Key Decisions

- **D1. Declared groups arrive only as a data file (`--groups PATH`), never as inline key arguments.** A `--group NAME` flag (repeatable) selects a subset of that file's groups. *Rejected: inline `--group NAME:key,key` (per-key provenance degrades to an afterthought in argv, and the spec forbids flattening a group to a bare key list); groups embedded in the manifest (they are per-study choices, which the manifest may not hold).*
- **D2. Parsing is `yaml.compose()` plus a strict walk over the node tree, keeping line numbers.** Errors carry file, line, and key path. Any node tag outside the standard `str`/`map` tags is a mechanical failure. *Rejected: `yaml.safe_load` + dict validation (loses lines, which the fixture contract asks for and the probe showed cost ~15 extra lines to keep); the Item 1 hand parser (brittle to formatting a regenerated package may introduce, per the spec's recorded decision).*
- **D3. The manifest schema and the fingerprint recipe live in a sibling module, `scripts/study/manifest.py`.** Item 4's `preflight.py` and `verify.py` read the manifest through it. *Rejected: keeping both inside `indicators.py` — Item 4 would reimplement the recipe, and two implementations of a digest recipe drift into a false gate.*
- **D4. The output is deterministic and self-describing: lists sorted by a stated key, no timestamps, no absolute paths, `schema_version` at the root.** *Rejected: maps keyed by `source_local_identity` (not guaranteed unique across owners) and a generation timestamp (it would break the digest stability the record depends on; the record supplies the time).*
- **D5. The not-derivable block is one module-level constant, emitted verbatim at both the document level and inside every group object.** A test asserts the two are byte-equal. *Rejected: document level only (a group excerpted into a per-axis framing section loses the disclosure); separate per-group prose (two texts drift).*
- **D6. The oracle is a typed entry-point object with a `kind` discriminator** — today `{"kind": "python_callable", …}`, recording `verify_stellaris`'s importable `compute()` as it exists. Adding `{"kind": "cli", "argv": [...]}` later is an additive amendment. *Rejected: a bare command string (inventing a CLI protocol for a single future consumer is what the design review warns against, and a string cannot be extended without reinterpreting old manifests).*
- **D7. A `--print-fingerprint` mode computes and prints the indicator-input fingerprint and every per-file digest, then exits 0 without tracing.** It never writes the manifest. *Rejected: the tool self-pinning the manifest (the manifest is data authored by a human; a tool that rewrites its own gate is not a gate).*
- **D8. Gate order is fixed: manifest schema → package-identity check → indicator-input fingerprint → pipeline parse → contract parse → declared-key resolution → trace.** *Rejected: parsing before the fingerprint gate (it would let a study run against artifacts the manifest was never reviewed against). Consequence for tests: a corrupt-artifact fixture must re-pin its temp copy's manifest, or it fails at the fingerprint gate instead — see Validation Approach.*
- **D9. The output, manifest, and axis-declaration schemas are documented twice: prose in this design's Component Overview, and committed JSON Schema files under `scripts/study/schemas/`.** Items 2 and 4 cite the file path plus the `schema_version` string. In-tool validation stays hand-written and strict (raise on unknown keys); the schema files are the citable contract, checked by a test that validates real output and the real manifest against them. *Rejected: prose only (Items 2/4 would each restate the field list, and restatements drift); JSON Schema as the in-tool validator (permissive by default about unknown keys, which contradicts raise-on-everything-unexpected).*
- **D10. Every reported constraint carries all three identities — `constraint_id`, `definition_qualified_name`, `source_local_identity`.** The spec's field list named the first and third; the record correlates across fingerprints by qualified name plus local identity, and `constraint_id`'s hash suffix does not survive regeneration. Carrying all three costs one field and satisfies both readings. **[AGENT]** *Rejected: dropping `constraint_id` (it is the pipeline module name, needed to locate the module) — hence all three, not a choice between them.*

## Architecture

```text
  --groups axes.json ─┐
  --manifest m.json ──┼─► manifest.py: schema validate ─► fingerprint recipe ──┐
  --package pkg/ ─────┘                                                        │
                                                                  gate: pin == computed?
                                                                               │ pass
       pipelines/*.yaml ──► strict node reader (file:line:key-path) ──┐        ▼
       contracts/model_contract.json ──► contract reader ─────────────┼──► channel graph
       inputs/*.json (paths from the EntryPoint block) ───────────────┘        │
                                                                               ▼
                                            declared keys ─► conservative closure (R10)
                                                                               │
                            constraint operands (predicate_ir) ◄───────────────┤
                            manifest objective catalog ◄──────────────────────┤
                            advisory scans: suffix siblings, manifest ties ◄───┘
                                                                               ▼
                                             one report document ─► atomic write / single stdout write
```

Data flows one way. No stage writes anything until the last, and any raise anywhere short-circuits to a stderr message plus a non-zero exit with nothing written.

**Integration points.**
- *Upstream (the package):* `pipelines/*.yaml`, `inputs/*.json` (paths read from the EntryPoint block), `contracts/model_contract.json`, and `contracts/package_contract.json` for the identity check. Read-only, always.
- *Upstream (the study):* the axis-declaration file, authored per study, snapshotted into the record.
- *Sideways (the package catalog):* `manifest.json`, read through `manifest.py`.
- *Downstream (Item 2):* `indicators.json` copied into the record directory with its digest and `schema_version`.
- *Downstream (Item 4):* `manifest.py` for the manifest and the fingerprint recipe; the manifest's baseline block for the baseline gate; the oracle object for `verify.py`. `indicators.py` never reads the baseline or the oracle.

## Required Invariants

1. **No partial output.** A non-zero exit writes zero bytes of report to stdout and creates or modifies no output file. Testable: every mechanical-failure test asserts the target path does not exist and stdout is empty.
2. **Determinism.** Two runs on unchanged inputs produce byte-identical output. No timestamps, no absolute paths, no set-iteration order in the document.
3. **Declared-only membership.** The traced key set equals the declared key set exactly. Suffix-sibling and tie warnings never change it. Testable: a group with warnings and the same group with the manifest tie removed produce identical trace fields.
4. **`no_constraint_response == (constraints_reachable == [])`**, and it is emitted for every group, including groups where it is false.
5. **Constraint completeness.** Every entry in `constraint_catalog.concrete_entries` appears exactly once, in `constraints_reachable` or `constraints_unreachable`, and in `bounds`.
6. **Grep-clean.** `scripts/study/indicators.py` and `scripts/study/manifest.py` contain no package name, no key prefix, and no adapter import. Testable by grep in a test.
7. **Disclosure parity.** The document-level and every group-level `not_derivable` block are byte-equal.
8. **Provenance round-trip.** Every declared key's `fan_out | tie` provenance appears in the output against that key.
9. **Interpretive facts never gate.** The only non-zero exits are the mechanical failures enumerated in Component Overview; a valid empty result exits 0.

## Component Overview

### `scripts/study/manifest.py` — the package-catalog seam

Owns three things and no logic beyond them.

*The manifest schema*, `schema_version: "study-package-manifest/v1"`, four blocks, all required, unknown keys anywhere a mechanical failure:

```jsonc
{ "schema_version": "study-package-manifest/v1",
  "package": {"name": "<contracts/package_contract.json package_name>", "path": "<repo-relative>"},
  "fingerprints": {
    "indicator_inputs": {"recipe": "indicator-input-fingerprint/v1", "digest": "<sha256>",
                          "files": ["pipelines/mfe_stellarator.yaml", "..."]},
    "recorded_provenance": {"executable_fingerprint": "<sealed>", "semantic_fingerprint": "<contract>"}},
  "objective_catalog": [{"name": "lcoe", "channel": "<qualified channel>", "note": "..."}],
  "ties": [{"key": "<qualified key>", "rides_with": ["<key>", "..."], "note": "..."}],
  "baseline": {"point": {"<key>": 12.7}, "headline": {"channel": "...", "value": 275.2642200420774},
               "verdicts": [{"source_local_identity": "wall_load_ok", "expected": "satisfied"}]},
  "oracle": {"kind": "python_callable", "module": "...", "callable": "compute", "note": "..."} }
```

`objective_catalog` and `ties` are lists of objects, not name→value maps, so a field can be added without changing the shape and duplicate names are a validation failure. `baseline` and `oracle` are validated in full but never read by `indicators.py` (spec: a malformed baseline is a failure at the first tool that opens the file, not a surprise for Item 4).

*The fingerprint recipe*, `indicator-input-fingerprint/v1`. The file set is exactly the artifacts the trace reads: every `pipelines/*.yaml`, every `inputs/*.json`, and `contracts/model_contract.json`. Digest of each file is sha256 over **raw bytes** — no text normalization, because a normalizer would hide an edit the trace can see. The recipe assembles one canonical text: a first line naming the recipe id, then one line per file, sorted by repo-relative POSIX path, as `<path> <sha256hex>`; the fingerprint is sha256 of that text, UTF-8. Sorted-by-path makes the order independent of the filesystem. The recipe id in line 1 means a future v2 recipe cannot collide with a v1 pin. Empty file sets (no pipeline, no inputs, missing contract) and any non-`.yaml` file inside `pipelines/` are mechanical failures rather than silent skips.

*The identity check.* The manifest's `package.name` must equal the live `contracts/package_contract.json` `package_name`. Mismatch is "wrong manifest for this package", a mechanical failure — cheap, and it never guesses a path.

### `scripts/study/indicators.py` — the reader, the trace, the report

*The strict reader* (D2). Walks the composed node tree: top level is exactly `metadata` and `modules`; every module has `module_type` and optional `inputs`/`outputs` maps; every port value splits into exactly `<type> <ref>`; exactly one `EntryPoint` and one `ExitPoint`, neither in the closure (R11). Entry-point ports name the input groups, and their refs are the relative paths to the `inputs/*.json` files. Reference classification is R1–R4 verbatim from the spike. Any surprise — unknown key, non-scalar where a scalar belongs, duplicate key, non-standard node tag, unsplittable value, a dotted ref outside the three proven forms, an output ref carrying a field path — raises with file, line, and key path.

*The graph and the closure* are the spike's, unchanged: channels keyed on fully qualified names (R5), a module fires if any declared key or tainted channel is among its inputs and firing taints all its outputs, iterated to fixpoint (R10). A channel produced by more than one module — same file or across files — is a mechanical failure (the spec's multi-pipeline stance).

*Declared-key resolution*, in this order, so each failure says the right thing:
1. Key present in the union of `inputs/*.json` → resolve `entry_type` from `contract.parameters`. A key present in inputs but absent from `parameters` is a mechanical failure (unclassifiable key).
2. Else, key names a produced channel → mechanical failure whose message says the key names a **computed quantity**, not that it is absent (policy §2.1).
3. Else → mechanical failure naming the absent key.

*Advisory scans*, computed after the trace and never merged into the group: suffix siblings (R12) and manifest tie candidates — a tie whose `rides_with` partners are all in the group while the tie `key` is not. Both land in the group's `warnings` list.

*The report*, `schema_version: "study-indicators/v1"`:

```jsonc
{ "schema_version": "study-indicators/v1",
  "tool": {"path": "scripts/study/indicators.py", "source_digest": "<sha256 of the two tool modules>"},
  "package": {"path": "...", "package_name": "...", "semantic_fingerprint": "...",
              "recorded_executable_fingerprint": "...",
              "indicator_input_fingerprint": {"recipe": "...", "digest": "...",
                                              "files": [{"path": "...", "sha256": "..."}]}},
  "manifest": {"path": "...", "schema_version": "...", "digest": "<sha256 of manifest bytes>"},
  "objective_catalog": [{"name": "lcoe", "channel": "..."}],
  "not_derivable": {"statements": ["...", "...", "..."], "positive_reading": "..."},
  "warnings": [{"kind": "provenance_drift|duplicate_key_across_groups", "detail": "..."}],
  "groups": [ /* one object per traced group, below */ ] }
```

Each group object: `axis`; `declared_keys` (list of `{key, provenance, entry_type}`, sorted by key); `group_valid`; `constraints_reachable` and `constraints_unreachable` (sorted by `constraint_id`, each carrying the three identities of D10, `operator`, `operands` with class/ref/reached/entry_type, `operand_classes`, `bound_vs_bound`); `bounds` for every constraint including literal operands from `predicate_ir` (R8); `objectives_reachable` and `objectives_unreachable` (sorted names); `no_constraint_response`; `trace_size` (`modules_fired`, `channels_tainted`); `warnings` (suffix siblings, tie candidates); and its own copy of `not_derivable` (D5).

The four disclosure strings are fixed text, versioned with the schema: monotonicity or sign of any response; same-quantity identity across differing key names; intra-module operand dependency (the trace is module-level); and the positive reading — a reachable constraint or objective means a possible path exists in the module graph, never that the axis responds.

*The CLI.*

```
indicators.py --package DIR --manifest FILE --groups FILE [--group NAME]... [--out FILE]
indicators.py --package DIR --print-fingerprint
```

`--package` and `--manifest` are required and never inferred. `--out` writes the document atomically (temp file in the same directory, then rename); omitted, the whole document goes to stdout in one write. Errors go to stderr. A short human summary per group — axis, `no_constraint_response`, counts, and the positive-reading line — also goes to stderr, so it can never contaminate the report on stdout.

*Axis-declaration file*, `schema_version: "study-axis-declaration/v1"`: `groups` is a list of `{axis, keys: [{key, provenance}]}`, `provenance` one of exactly `fan_out | tie`. Duplicate axis names, duplicate keys inside a group, an empty group, and unknown keys are mechanical failures. The same key in two groups is allowed and emits a document-level `duplicate_key_across_groups` warning.

### `scripts/study/schemas/` — the citable contract

`indicators.v1.schema.json`, `study_package_manifest.v1.schema.json`, `axis_declaration.v1.schema.json`. JSON Schema, `additionalProperties: false` throughout, cited by path + version string from Items 2 and 4 (D9).

### `exploration/stellarator_e2e/studies/manifest.json` — the stellarator instance

The five objective channels from the spike as the starting catalog, keyed on channels never on exit-point filenames (R6); the one declared tie (`magnet__R0` rides with `geom__R`, `rb__R`); the pinned baseline (`R = 12.7`, `a = 1.3`, `availability = 0.85`, headline LCOE `275.2642200420774`, five verdicts satisfied); `verify_stellaris`'s importable `compute()` as the oracle; and the three fingerprints. Authored by hand; the indicator-input digest comes from `--print-fingerprint`.

## Non-Goals

- The package annex file (Item 4), preflight and baseline gates, oracle sampling, verification, adapter behavior, point execution.
- Any package-specific name, key prefix, or adapter import inside the two tool modules.
- A manifest for any package other than the stellarator.
- Measuring or reducing the cost of conservatism.
- Deciding whether `lcoe_calc__discount_rate` is the `interest_rate` quantity.
- Claiming response, sign, or monotonicity; inferring membership from suffixes.

## Implementation Notes

- **`yaml.compose`, not `safe_load`.** Composing does not construct, so no tag can execute; but tags survive on nodes, so the walker must assert `node.tag` is the standard str/map tag. The probe demonstrates both halves.
- **Line numbers are 0-based on `start_mark`.** Report `line + 1`.
- **Resolve the inputs files from the EntryPoint block's refs**, relative to the pipeline file's directory. Do not reconstruct `inputs/<group>.json`.
- **`.root` stripping is load-bearing** (R3): 65 edges and `R`'s path to `net_positive` depend on it.
- **Assemble, then write.** No `json.dump` to stdout before the last statement of a successful run.
- **`scripts/study/` needs no `__init__.py`** — implicit namespace packages plus `pythonpath = ["."]` make `from scripts.study import indicators` work in tests.
- **Add `jsonschema` as an explicit dependency** (`uv add jsonschema`); it is already in `uv.lock` transitively, so nothing new downloads.
- **Delete `probe_lineno.py`** at implementation, or leave it in the work-item folder as the throwaway it is — it never moves to `scripts/`.

## Potential Risks

- **Fingerprint churn blocks studies (B2).** A regenerated or reformatted artifact invalidates the pin and every study stops until a human re-pins. Mitigation: `--print-fingerprint` makes re-pinning a one-line edit, and the mismatch message names which files changed.
- **The strict reader is brittle by design.** A regenerated package with a new construct fails closed, loudly, and needs a code change. That is the intended direction, and the spec forbids weakening it; the cost is that a package upgrade may block on this tool.
- **Known-answer fixtures are bound to fingerprint `c9bc…c261`.** If the package is regenerated they are re-derived from the new package, never patched to match (spec requirement). Risk: a hurried session patches expectations. Mitigation: the expectation files record the fingerprint they were derived against, and a test asserts the live fingerprint matches it — so a regenerated package fails the *fixture-binding* assert first, with a message that says re-derive.
- **Provenance drift in the manifest.** A human re-pins the indicator-input digest but forgets the recorded `semantic_fingerprint`. The fingerprint gate cannot catch this (the contract file is inside the digested set, so a real contract change would already have fired). Mitigation: the output carries a `provenance_drift` warning when the manifest's recorded semantic fingerprint differs from the live one — a warning, not a gate, since gating on it is exactly the false gate the spec ruled out.

## Integration Strategy

The tool slots into the runbook's third step: intake → axis-group declaration → **indicators and framing** → preflight. The executing agent writes the axis-declaration file, runs one invocation covering every proposed axis including declined ones, and copies the resulting `indicators.json` into the record directory. Item 2's record contract then snapshots it with its digest and schema version.

`manifest.py` is the seam Item 4 builds on: `preflight.py` reads the manifest and the baseline block through it, and `verify.py` reads the oracle object. Item 4 also inherits the spec's forwarded finding — while the era adapter exists, the design's "manifest-fingerprint match" preflight gate cannot be a match against the sealed `executable_fingerprint`, because the two glue-edited files always differ from their sealed hashes. Item 4 needs its own answer; the indicator-input fingerprint defined here is available to it but is scoped to the artifacts *this* trace reads.

Nothing is replaced. `trace.py` and `cases.py` stay where they are as the spike's evidence; the tests below supersede them as the live assertions.

## Validation Approach

Tests under `tests/study/`, run by `uv run python -m pytest tests/study`. The package is never mutated in place: `conftest.py` provides a `package_copy` factory that copies the committed package tree plus the manifest into pytest's `tmp_path` and returns both paths.

The factory carries the two rules that make negative tests trustworthy:
- **Assert before mutating.** Every mutation asserts its target substring exists in the copy first, then replaces. Item 1's probe 4 passed against an uncorrupted file because the target string was wrong — a negative test that corrupts nothing looks exactly like a passing one. **[HARD, spec]**
- **Re-pin unless the test is about the pin.** Because the fingerprint gate runs before the parse (D8), a mutation test must recompute and rewrite the copy's pinned digest to reach the failure it is testing. The same helper with re-pinning switched off is the fingerprint-mismatch test.

| File | Covers |
|---|---|
| `test_known_answers.py` | The six Item 1 cases — `availability`, `interest_rate`, `R`, `R`+tie, `a`, `beta` — field by field against expectation files in `tests/study/data/`, including operand class per reached operand, operator, `bound_vs_bound`, both objective lists, sibling candidates, and the module/channel counts. Plus the fixture-binding assert on the semantic fingerprint. |
| `test_mechanical_failures.py` | Missing declared key; declared key naming a produced channel (real target, e.g. a `pb__p_net`-style channel, no synthetic fixture needed); unclassifiable key; fingerprint mismatch; unparseable reference; corrupt pipeline line (asserts file, line, and key path in the message); objective channel produced by no module; wrong manifest for the package; malformed manifest baseline. Each asserts non-zero exit, a located message, **and** that no output file exists and stdout is empty. |
| `test_valid_empty.py` | A group with genuinely no constraint reach exits 0 with `no_constraint_response: true`, `group_valid: true`, and the expected objective lists. |
| `test_warnings.py` | Suffix siblings and manifest tie candidates appear as warnings and change nothing: the traced fields are identical with and without them. |
| `test_provenance.py` | Per-key `fan_out | tie` round-trips from the declaration file to the output; a tie key traces identically to a fan-out key. |
| `test_multipipeline.py` | A committed synthetic two-pipeline package under `tests/study/data/synthetic_pkg/` (a handful of modules, its own inputs, a minimal model contract, its own manifest): the graph is package-scoped across files; a channel produced in two files is a mechanical failure; two EntryPoints in one file is a mechanical failure; a `.yml` file in `pipelines/` is a mechanical failure. |
| `test_output_contract.py` | The output validates against `schemas/indicators.v1.schema.json`; the real manifest validates against its schema; `not_derivable` is byte-equal at document and group level; two runs are byte-identical; every contract constraint appears exactly once across reachable/unreachable. |
| `test_generic.py` | Grep-clean: neither tool module contains the package name, the key prefix, or `era_adapter`. |

Manual verification at implementation: run the tool against the committed package with all six groups and diff the group objects against `.project/active/run-study-reachability-spike/indicators.json` for the fields both carry.

## Next-Stage Handoff

**Fixed for the plan.** The two-module split and their responsibilities (D3); the CLI surface and the two modes (D1, D7); `yaml.compose` + strict node walk with file/line/key-path errors (D2); gate order (D8); the three schema versions and their JSON Schema files (D9); the three constraint identities (D10); the not-derivable constant emitted at both levels (D5); the typed oracle object (D6); the fingerprint recipe, byte for byte (`manifest.py`); the nine invariants; the test file list and the `package_copy` factory's two rules.

**Open for the plan.** Exact wording of error messages (each must locate its fault per the spec's success criterion); the synthetic package's module list; whether `manifest.py`'s validator is hand-rolled per-block functions or one table-driven walk (either satisfies raise-on-unknown).

**De-risk first.** The synthetic two-pipeline fixture. It is the only asserted behavior with no real package data behind it (the spec says so explicitly), and it is the one place where a wrong assumption about package-scoped channels would go unnoticed. Build it before the mechanical-failure suite.

---
Next Step: after approval → `/_my_plan`.
