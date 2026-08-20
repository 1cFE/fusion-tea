# Spec: Indicator Tool and Package Manifest

**Status:** Implementation Complete (2026-08-19) — accepted at orchestrated review, built in `plan.md` Phases 1–7
**Owner:** Reid W
**Created:** 2026-08-19
**Complexity:** MEDIUM
**Branch:** `feat/stellarator-mbse-demo`
**Epic:** RUN-STUDY, Item 3

---

## Problem

Before any study point runs, the agent needs deterministic facts about what in the model can push back on each proposed axis. Today nothing supplies them. The availability sweep in the proof-of-life study ran to completion, came out entirely feasible with a monotone cost response, and only afterwards was it clear that no constraint in the model responds to availability at all — a sensitivity analysis presented as a design search. **[INHERITED: `.project/concepts/run-study-skill-design.md` Problem, ¶4]** The information was always there: the generated package records its own dataflow, its constraint operands, and which operands are bound inputs versus computed values. No step asked for it.

Item 1 proved the derivation works. A throwaway trace over the real package reproduced all five known answers from the design's Appendix A, on package semantic fingerprint `c9bc164050f0aac8a2009befb34497426d68923066ca1c1783a0b80e8048c261`, with no premise conflict. **[INHERITED: `.project/active/run-study-reachability-spike/findings.md`, CONFIRMED 2026-08-19]** What exists now is a spike script that hard-codes the objective catalog, lives in a PM directory, and is explicitly throwaway.

What is missing is the durable pair the design names: a generic tool that any package can use, and a data-only catalog of the stable facts a package supplies to it. **[INHERITED: design, Design Principle 4 — "Generic and package-specific never share a file"]** Neither `scripts/study/` nor `exploration/stellarator_e2e/studies/manifest.json` exists.

The obligation this work carries has decision force and comes from the owner: **[OWNER]** interpretive facts never gate a study, while mechanical failures must fail closed. A broken analysis and an empty one must never produce the same exit code — that is what makes `no_constraint_response` trustworthy enough to hand a user for a ruling.

## Success Criteria

- [ ] Known-answer tests pass for `availability`, `interest_rate`, `R`, `R`+tie, `a`, and `beta`, matching the Item 1 fixture contract field for field — constraints reached, operand class per reached operand, operator, `bound_vs_bound`, objectives reachable and unreachable, sibling candidates, and the module/channel trace counts.
- [ ] A valid empty result exits 0 with `no_constraint_response: true` and `group_valid: true`. A missing declared key, an indicator-input fingerprint mismatch, an unparseable reference, a corrupt pipeline line, and an objective channel produced by no module each exit non-zero and emit no partial indicator output.
- [ ] A declared key that names a produced channel rather than an entry key exits non-zero with a message that says so, distinct from the absent-key message.
- [ ] Each declared key's `fan_out | tie` provenance survives from input to output, so the record can snapshot it.
- [ ] Every mechanical failure message locates the fault: the absent key by name, the computed quantity by name and by what it is, the reference quoted verbatim, the corrupt construct by file and position, the ghost objective channel by name.
- [ ] Suffix-sibling matches and manifest tie candidates appear as warnings in the output and never change which keys are traced.
- [ ] `scripts/study/indicators.py` contains no stellarator-specific name and imports no adapter; grepping the file for the package name, its key prefix, and `era_adapter` returns nothing.
- [ ] `manifest.json` parses as data, contains no executable content, and separates stable package catalog facts from per-study choices — no axes, no windows, no selected objectives.
- [ ] Every report states, in its own output, that monotonicity or sign of response, same-quantity identity across differing key names, and intra-module operand dependency are not derivable, and that a reachable positive is a possible path and never "responds".
- [ ] The output JSON schema is documented and versioned, so Items 2 and 4 can consume it as a fixed seam.
- [ ] Tests run under `uv run python -m pytest`.

## Known Requirements

### The seam between the tool and the package

- **[HARD]** The manifest must pin an **indicator-input fingerprint** that the generic tool computes over exactly the artifacts it reads — `pipelines/*.yaml`, `inputs/*.json`, and `contracts/model_contract.json` — as they exist on disk. Neither existing fingerprint can serve. The package contract's `executable_fingerprint` is a sealed stored value, and the two artifacts the trace walks are precisely the two files the era adapter is allowed to modify: `pipelines/mfe_stellarator.yaml` and `inputs/system_design.json` both differ on disk from their sealed `artifact_hashes` entries (verified 2026-08-19). The model contract's `semantic_fingerprint` matches but covers neither the pipeline wiring nor the inputs — the trace's whole subject. A gate on either would be false: one always fails, the other never notices the change that matters.
- **[INFERRED]** The same evidence has a consequence for Item 4 that this item does not fix but does hand forward: the design gives `preflight.py` a "manifest-fingerprint match" gate, and while the era adapter exists that gate cannot be a match against the sealed `executable_fingerprint`, because the two glue-edited files always differ from their sealed hashes. Item 4 needs its own answer; it should not inherit the assumption.
- **[INFERRED]** The manifest also carries the sealed `executable_fingerprint` and the `semantic_fingerprint` as recorded provenance, so a record can state which package revision the indicators were derived against. The tool does not gate on them.
- **[HARD]** The manifest is data only. **[INHERITED: design review m3, accepted]** No executable content, no import hooks, no computed defaults.
- **[NEED]** **[OWNER, via epic Item 3 scope]** The manifest holds the package catalog and nothing else: declared ties, the objective-channel catalog, the pinned baseline point and headline, the package-owned oracle entry point, and the fingerprints above. Per-study choices — which axes, which window, which objectives are selected — belong to the study definition and the record, not here.
- **[INHERITED: epic Item 3 scope]** The pinned baseline is `R = 12.7`, `a = 1.3`, `availability = 0.85` with headline LCOE `275.2642200420774` and all five verdicts satisfied. Recorded as data; `indicators.py` never reads it. Item 4's baseline gate is its only consumer.

### What the tool derives

- **[NEED]** **[OWNER, via epic Item 3 scope]** A declared group is a set of qualified entry keys each carrying its own provenance, `fan_out` or `tie`. The tool takes provenance as input and carries it through to the output, per key. The record snapshots declared groups with per-key provenance, so the tool must not flatten a group to a bare key list. Provenance never changes what is traced — a tie key and a fan-out key are traced identically; what it changes is what a cold reader can tell about why the key is in the group.
- **[INHERITED: design Appendix A; Item 1 fixture contract]** Per declared group the report carries: `group_valid`; `entry_type` per key (`usage_literal | library_default | design_attribute`); `sibling_candidates`; `constraints_reachable` with, per reached constraint, its `constraint_id` and its `source_local_identity` (R9 — both forms; the record's cross-fingerprint correlation matches on qualified name plus local identity, so neither may be dropped), the operand reached, its class (`computed | bound`), the other operand, the operator, and `bound_vs_bound`; `bounds` from `predicate_ir` including literal operands; `objectives_reachable` and `objectives_unreachable`; and `no_constraint_response`. Appendix A's field names are used exactly.
- **[INHERITED: design Appendix A, `entry_type`; design Edge Cases, "Declared key does not exist"]** A declared key that resolves only to a produced channel is reported as its own outcome, distinct from an absent key. It is still a mechanical failure with a non-zero exit — a computed quantity is not an axis (policy §2.1) — but the message must say the key names a computed quantity, not that the key does not exist. Telling an author their key is missing when the real problem is that they picked a model output sends them looking in the wrong place.
- **[INHERITED: design review C1, accepted]** Axis membership comes only from the declared group. The suffix scan is advisory and computed after the fact; it is never merged into the group. The concrete demonstration is in the package: the design's declared tie `magnet__R0` has suffix `R0`, not `R`, so no suffix scan will ever surface it.
- **[INHERITED: design review M8, accepted]** `no_constraint_response` is a sound negative — the trace is deliberately over-approximate, so if it finds no path, no finer analysis can. A positive is only "a path exists". The tool never emits "responds" or "unresisted".
- **[INFERRED]** The manifest's tie catalog is advisory in exactly the way the suffix scan is. A tie entry names a key and the keys it rides with; when a declared group contains a tie's partners but omits the tie key, the tool emits a `tie_candidates` warning. It never adds the key. This is the only reading that gives the catalog a job without contradicting declared-only membership.
- **[INHERITED: Item 1 findings, R1–R12]** The twelve proven parsing and normalization rules are the required behavior: entry-prefixed refs are bound inputs; bare refs are produced channels; a trailing `.root` is stripped (65 edges depend on it, and `R` loses `net_positive` without it); any other dotted ref is a hard failure; channels are keyed on the fully qualified channel name, never the local port; exit-point renames are output filenames, not channel renames; predicate operand names join to the constraint module's input port names; literal operands come only from `predicate_ir`; the constraint id is the pipeline module name and `source_local_identity` is what gets reported; a module fires if any declared key or tainted channel is among its inputs and firing taints all its outputs, iterated to fixpoint; exactly one EntryPoint per pipeline file and the ExitPoint is a sink, neither participating in the closure; the suffix scan is separate and advisory.

### Mechanical behavior

- **[NEED]** **[OWNER]** Interpretive facts never gate — exit 0. Mechanical failures — missing declared key, fingerprint mismatch, unparseable artifact, objective channel produced by no module — exit non-zero. A valid empty result exits 0. A broken analysis must never look like an empty one.
- **[INFERRED]** On any mechanical failure the tool emits no indicator output at all, not even a partial report. A half-written report that a downstream reader might treat as a result is the failure mode the exit-code rule exists to prevent.
- **[INFERRED]** Every construct the tool does not recognize raises. This is the property that makes the parser trustworthy, and it is the property the design must preserve whichever parsing mechanism it picks.
- **[INFERRED]** The tool validates the manifest against the full schema even though it uses only the ties, the objective catalog, and the indicator-input fingerprint. A malformed baseline block is a mechanical failure at the first tool that reads the file, rather than a surprise for Item 4.

### Tests

- **[NEED]** **[OWNER, via epic Item 3 scope]** Known-answer tests for every case in the Item 1 fixture contract, plus missing-key, malformed-pipeline, valid-empty, and suffix-warning tests.
- **[INFERRED]** Two cases the Item 1 fixture contract does not cover, added here because the spec added the obligations: a declared key that names a produced channel, and a declared group whose per-key provenance round-trips to the output. The computed-quantity case has a real target in the package — any channel name from the trace, for instance `«P»pb__p_net` — so it needs no synthetic fixture.
- **[HARD]** Every negative test asserts that its mutation target exists before mutating. Item 1's probe 4 initially passed against an uncorrupted file because the target string was wrong — a negative test that corrupts nothing looks exactly like a passing one. **[INHERITED: Item 1 findings, log entry 7]**
- **[INFERRED]** Known-answer fixtures are bound to the semantic fingerprint they were derived against. If the package is regenerated they are re-derived from the new package, never patched to match.

### Recorded decisions on the questions Item 1 handed forward

- **[INFERRED] Parsing mechanism: `yaml.safe_load` plus exhaustive strict validation.** The property that must survive is "every unexpected construct raises", and a strict validator delivers it: unknown keys at any level, unknown module types, a value string that does not split into exactly `<type> <ref>`, and a reference outside the three proven forms all raise. The hand parser earns nothing beyond that property and is brittle to formatting changes a regenerated package may introduce. One cost is real and is accepted here: `safe_load` discards line numbers, so the corrupt-artifact error locates the fault by file and key path rather than by line, unless the design finds line numbers cheap to keep. The success criterion is written to that weaker bar. Design may revisit the mechanism; it may not weaken the raise-on-everything-unexpected property.
- **[INFERRED] The objective catalog is manifest-owned.** The five channels the spike used are the starting catalog: `lcoe` = `«P»lcoe_calc__lcoe`, `lcoe_1cfe` = `«P»lcoe_1cfe_calc__lcoe`, `cas72` = `«P»cas72_calc__cost`, `fuel` = `«P»fuel_calc__annual_fuel`, `total_capital` = `«P»total_capital__total_capital`, where `«P»` is `stellarator_09__stellaris__`. Catalog entries key on the channel, never on the exit-point output filename (R6). No channel is hard-coded in the tool.
- **[INFERRED] Multi-pipeline stance: trace every file, fail on cross-file collision.** The tool globs `pipelines/*.yaml` and builds one package-scoped channel graph across all of them. A channel name produced by more than one module, in the same file or across files, is a mechanical failure. Each file must carry exactly one EntryPoint. Only `mfe_stellarator.yaml` exists today, so this stance is asserted by a synthetic two-file fixture, not by real package data — and the spec says so rather than letting a single-pipeline assumption pass silently.
- **[INFERRED] The oracle field records what exists, not what Item 4 may want.** `verify_stellaris.py` has no CLI: it is a module with a `compute()` function that the proof-of-life study imports and drives by mutating a module-global input dict. The manifest therefore records the oracle as the importable entry point it actually is. Inventing a command-line protocol for a single future consumer is exactly what design review point 4 warns against; if Item 4 needs a CLI it adds one to the package-owned script and amends the manifest field. `indicators.py` never reads this field.

## Non-Goals

- Deciding whether `lcoe_calc__discount_rate` is the same quantity as the `interest_rate` group. It is a modeling question about attribute identity, and the tool cannot settle it. The key stays out of the group; the question belongs to the axis-declaration review.
- Inferring group membership from suffixes, claiming positive response, or deriving monotonicity, sign, or intra-module operand dependency.
- Preflight baseline and git-clean gates, oracle sampling, verification, adapter behavior, and point execution. Item 4 and the execution routes own those.
- Any package-specific name, key prefix, or adapter import inside the generic tool.
- Building a manifest for the IFE package or any package other than the stellarator.
- Measuring or reducing the cost of conservatism. `R` fires 54 of 60 modules, so on this package the indicator's discriminating power is limited; Item 1 flagged it as worth watching, not worth fixing statically.

## Open Questions / Deferred to design

- The tool's CLI surface: how declared groups are supplied (file, arguments, or both), whether several groups are traced per invocation, and where output is written.
- The manifest schema's exact field names, nesting, and whether it carries its own `schema_version`.
- Where the output schema is documented and in what form — prose, JSON Schema, or both — and how Items 2 and 4 cite it.
- Whether line numbers are cheap enough to keep through the YAML load; if so, the corrupt-artifact error should carry file and line rather than file and key path.
- Test file layout under `tests/`, and how the synthetic multi-pipeline and corrupt-artifact fixtures are built without mutating the committed package.
- How the not-derivable statements are carried in the output — a fixed block, a per-report list, or both — given that they must appear in every report.

---

## Related Artifacts

- **Epic:** `.project/backlog/epic_run_study_capability.md` — Item 3
- **Required Reading:**
  - `.project/active/run-study-reachability-spike/findings.md` — Item 1 findings, R1–R12, fixture contract
  - `.project/concepts/run-study-skill-design.md` — indicator builder, package manifest, Design Principles 1–2 and 4, Appendix A, Required Invariants (Tools)
  - `.project/concepts/run-study-skill-design-review.md` — C1, M8, m3
  - `exploration/stellarator_e2e/pkg/stellarator_tea/` — contracts, pipelines, inputs
- **Product-lens:** `.project/active/run-study-indicators/product-lens.md`
- **Design:** `.project/active/run-study-indicators/design.md` (to be created)

---

**Next Steps:** After approval, proceed to `/_my_design`.
