# Design Review: Indicator Tool and Package Manifest (RUN-STUDY Item 3)

**Design:** `.project/active/run-study-indicators/design.md`
**Spec:** `.project/active/run-study-indicators/spec.md` (accepted)
**Review File:** `.project/active/run-study-indicators/design-review.md`
**Date:** 2026-08-19
**Reviewer posture:** fresh, skeptical; claims checked against the committed package and by running code (read-only).

---

## The Point

Before any study point runs, the agent must be handed deterministic, package-derived facts about what in the model can push back on each proposed axis — so a sweep that can only say "more is better" is surfaced as a model gap instead of published as a design search. The availability sweep in the proof-of-life ran to completion, came out entirely feasible with a monotone cost response, and only afterwards was it clear that no constraint in the model responds to availability at all. **[INHERITED: `.project/concepts/run-study-skill.md` Owner's Words; concept design Goals — grade: owner]**

Two owner-grade constraints govern every choice: interpretive facts never gate a study and mechanical failures fail closed, so a broken analysis and an empty one never share an exit code; and generic and package-specific never share a file. **[OWNER]**

## Fundamental Assessment

**Sound.** This is the right piece of work and the right approach.

The core concept — a pedantic reader underneath, the Item 1 trace on top, and a report that is a document assembled in memory and written once — is the smallest structure that delivers the owner's exit-code rule *mechanically* rather than by discipline. "There is no code path that can produce a partial report" (design.md:65) is a real argument, not a slogan. The two-module split (`indicators.py` / `manifest.py`) earns itself: without it Item 4 reimplements the fingerprint recipe, and two implementations of a digest recipe are a false gate waiting to happen (D3, design.md:80).

I looked for over-engineering and did not find it. The abstraction count is three (reader, closure, report) plus one seam module, against a spec that names nine invariants and two downstream consumers. `--print-fingerprint` is one mode, not a subcommand tree. The oracle is a two-field typed object, not a plugin protocol. Nothing here is built for a hypothetical.

**Product-lens.** The item's ledger (`.project/active/run-study-indicators/product-lens.md`) is **CLEAR** at the spec revision; the epic gate is CLEAR (`epic-F1`/`epic-F2` FIXED on owner authority). I re-derived the point independently above and reach the same place. Neither design-level smell fires: no consumer compensates for a producer guarantee (the design explicitly *refuses* to normalize bytes so the trace can see what changed, design.md:155), and no invariant changes owner silently — the annex, preflight, and oracle-consumption ownership are each named and routed (design.md:37, 242).

One capture-fidelity regression does surface and it belongs in the must-fix list, not here: an owner-side settled payload (Appendix A's `sibling_candidates`) has been softened into a generic `warnings` bag. That is a Compression-law violation, correctable in one line, not a foundation problem. See **M2**.

Proceeding to the detailed review.

---

## Answers to the six briefed questions

**Q1 — Can the trace read a file the recipe did not digest? Yes. This is a real false gate.**
The recipe's file set is `pipelines/*.yaml`, `inputs/*.json`, `contracts/model_contract.json` (design.md:155). The reader resolves inputs files from the EntryPoint block's declared relative paths (design.md:161, design.md:224 — "Do not reconstruct `inputs/<group>.json`"). Today the two agree: the EntryPoint declares exactly `../inputs/mfe_plant_params.json`, `../inputs/stellarator_plant_params.json`, `../inputs/system_design.json` (`pipelines/mfe_stellarator.yaml:13-17`) and those are exactly the three `.json` files in `inputs/`. But nothing *enforces* the agreement. A regenerated pipeline whose entry ref points at `../handwritten/params.json`, or at `../inputs/params.yaml`, is read by the trace and digested by nobody — the pin passes while the trace's actual input changed. That is the silent direction of failure, which is the one the fingerprint exists to prevent. Fix in **M3**.

**Q2 — Appendix A conformance: one field is dropped.**
`entry_type` (design.md:188, inside `declared_keys`), `constraints_reachable`, `bounds`, `objectives_reachable`, `no_constraint_response` all survive with their exact names. D10's identity triple is purely additive and verified correct: all five `concrete_entries` in `contracts/model_contract.json` carry `constraint_id`, `definition_qualified_name` (e.g. `mfe_viability::'Neutron Wall Load Limit'`), and `source_local_identity` (`wall_load_ok`). **`sibling_candidates` is the casualty** — it does not appear in the group field list and is folded into `warnings` (design.md:170, 188). Fix in **M2**.

**Q3 — Does the real pipeline contain tags beyond `str`/`map`? No.**
I composed the committed file and counted every node: **1220 `tag:yaml.org,2002:str`, 181 `tag:yaml.org,2002:map`, zero sequences, zero other tags.** The walker's accept-set is correct against the package as it stands. One prospective edge remains — the codegen quotes `output_folder: "stellarator_tea_results"` today, but an unquoted numeric or boolean in `metadata` would arrive tagged `int`/`bool` and raise inside a block the trace never reads. Fail-closed is the right default; the design should just say which block the accept-set governs. See **S6**.

**Q4 — Does `--group NAME` create a fragmented-digest hazard? Yes, a mild one, and the design should close it structurally.**
Item 2 snapshots one `indicators.json` with its digest (`.project/active/run-study-contract/spec.md:98`). The design states the full-document invocation in prose (design.md:240) and asserts it as B4 (design.md:74), but nothing in the *output* distinguishes a full run from a subset, so a record can snapshot a subset and look complete to a cold reader. Fix in **S1**.

**Q5 — Is the D8 gate order consistent and safe with an identity check over an undigested file? Yes.**
The digest is scoped to "what the trace reads", and `contracts/package_contract.json` is not read by the trace. The identity check is a string equality on `package.name` vs `package_name` (verified: `package_name` is `stellarator_tea`), so tampering with that file can only cause a *refused* run, never a passing trace over unreviewed artifacts. The scoping is principled and the ordering is right. One caveat, not a defect: the report republishes `recorded_executable_fingerprint` read live from that same undigested file (design.md:178). See **N1**.

**Q6 — Invariant 5 vs the spike fixture: the intent is right, the shape is not written down.**
I read the spike's real output. `bounds` is per-group and **axis-varying** — it carries all five constraints every time, with a per-operand `reached` flag that differs by axis. So "every catalog constraint appears in reachable/unreachable **and** in bounds" (design.md:125) is meaningful, not a constant block bolted on. The ambiguity is that the design never states `bounds`'s shape, its sort key, or that it carries `reached` — and D4 forbids the map-keyed-by-`source_local_identity` shape the spike actually used, so it must become a list that the design has not described. Fix in **S2**.

---

## Must-Fix

Each of these would produce a wrong or non-conformant implementation.

### M1 — The `pipelines/` strictness rule fails on the committed package on day one

**Evidence.** design.md:155: "any non-`.yaml` file inside `pipelines/` is a mechanical failure rather than a silent skip." design.md:261 makes it an asserted test (`a .yml file in pipelines/ is a mechanical failure`).

The committed package contains `exploration/stellarator_e2e/pkg/stellarator_tea/pipelines/__init__.py`. It is not incidental — it is a *sealed* artifact, listed in `contracts/package_contract.json` `artifact_hashes` alongside `pipelines/mfe_stellarator.yaml`, `inputs/__init__.py`, and the three input JSONs. Every generated teax package will have it, because the pipelines directory is an importable Python package.

As written, `indicators.py` refuses to run against the only package that exists. Every known-answer test fails at the first gate.

**Smallest correct fix.** Narrow the rule to the class it is actually defending against — a YAML file the glob missed. A file in `pipelines/` whose suffix is a YAML suffix other than `.yaml` (`.yml`, `.YAML`, `.Yaml`) is a mechanical failure; anything else is ignored. The recipe file set is untouched (`pipelines/*.yaml` already excludes `__init__.py`), and the `.yml` test case at design.md:261 stays exactly as written.

### M2 — `sibling_candidates`, an Appendix A field, is dropped into `warnings`

**Evidence.** The group field list (design.md:188) enumerates `axis`, `declared_keys`, `group_valid`, `constraints_reachable`/`constraints_unreachable`, `bounds`, `objectives_reachable`/`objectives_unreachable`, `no_constraint_response`, `trace_size`, `warnings`, `not_derivable` — no `sibling_candidates`. design.md:170 routes suffix siblings into `warnings` instead.

Against three authorities:
- Appendix A names the field: "`sibling_candidates`: keys outside the group sharing an attribute suffix" (`.project/concepts/run-study-skill-design.md:259) — settled, owner-side.
- The spec requires it verbatim in the per-group field list (spec.md:50) and requires the known-answer tests to match "sibling candidates" field for field (spec.md:24).
- The spike emits it as a first-class per-group key. I read `.project/active/run-study-reachability-spike/indicators.json`: every group object carries `sibling_candidates`, `[]` in all five cases, and the fixture contract records that value per case (findings.md:120, 129, 142, 163).

This is the Compression law failing: an owner-side settled name softened into a generic bag. A consumer written against Appendix A looks up `sibling_candidates` and gets nothing.

**Smallest correct fix.** Restore `sibling_candidates` as its own group field — a list of qualified keys, sorted. Leave tie candidates in `warnings` (they are this design's addition, not Appendix A's). If a mirror warning is wanted for the human summary, that is additive and fine; the named field is what may not be dropped.

### M3 — The fingerprint recipe does not cover what the reader actually reads (Q1)

**Evidence.** design.md:155 (glob-based file set) vs design.md:161 and design.md:224 (resolve inputs from the EntryPoint refs). See Q1 above for the full argument.

The gap is not present in today's package but the design's own B1 bet (design.md:71) is explicitly about what a *regeneration* may change, and the strict reader exists precisely because regeneration is expected to surprise it. A pin that silently stops covering the read set is worse than no pin: it reports "verified" over changed inputs.

**Smallest correct fix.** Keep D8's pre-parse gate exactly as it is, and add one post-parse coverage check: every inputs path resolved from the EntryPoint block must be a member of the manifest's pinned `files` list; any that is not is a mechanical failure naming the file. Also state that a ref resolving outside the package root is a mechanical failure. Two conditions, both fail-closed, neither disturbs the gate order.

### M4 — The report's path fields have no normalization rule, so the digest Item 2 snapshots is invocation-dependent

**Evidence.** The report carries `tool.path` (design.md:176), `package.path` (design.md:177), `manifest.path` (design.md:181). Invariant 2 says "no absolute paths" (design.md:122) and D4 repeats it (design.md:81), but nothing says how `--package /home/reid/.../pkg/stellarator_tea` or `--package ../pkg/stellarator_tea` becomes the emitted string. Two agents invoking the tool from different working directories, on identical inputs, produce different bytes — and therefore a different digest for the same facts. Item 2 snapshots that digest into every record.

This defeats Invariant 2 in the exact situation Invariant 2 exists for.

**Smallest correct fix.** State the rule: `package.path` is copied from the manifest's `package.path` field (already repo-relative by schema, design.md:141); `manifest.path` and `tool.path` are emitted as repo-relative POSIX paths from the repository root. CLI arguments are used to locate files and are never echoed into the document.

### M5 — `tool.source_digest` has no recipe

**Evidence.** design.md:176: `"source_digest": "<sha256 of the two tool modules>"`. Concatenation order, separator, and whether `scripts/study/schemas/*.json` are included are all unspecified. Item 2 snapshots this value as tool provenance, so two implementers producing different-but-plausible digests for the same source tree is a real cost.

The design already solved this problem once, well, for the indicator inputs — a recipe id line plus sorted `<path> <sha256hex>` lines (design.md:155). Not reusing it here is an omission, not a decision.

**Smallest correct fix.** Give it the same canonical-text recipe under its own id (`tool-source-digest/v1`) over an explicitly named file list, and emit `{"recipe": ..., "digest": ...}` rather than a bare hash.

---

## Should-Fix

### S1 — `--group` subset runs are indistinguishable from full runs in the output (Q4)

D1 offers `--group NAME` (repeatable) as a subset selector (design.md:78); B4 asserts one invocation per study covering every axis (design.md:74); Integration Strategy states the full invocation in prose (design.md:240). None of that reaches the document, so a subset's `indicators.json` and digest can be snapshotted into a record that claims to cover every proposed axis — including declined ones, which Item 2's runbook explicitly requires (`.project/active/run-study-contract/spec.md:65`).

**Fix.** Emit the axis-declaration file's digest and `groups_declared` (every axis name in the file) alongside `groups`, and add an invariant: the record-feeding invocation traces every declared group; `--group` is a debugging aid. Item 2 can then check `groups` covers `groups_declared` mechanically instead of trusting the runbook.

### S2 — `bounds` shape is unspecified and conflicts with D4 (Q6)

design.md:188 names `bounds` with no shape, sort key, or statement that it carries per-operand `reached`. The spike's real shape is a map keyed by `source_local_identity`, which D4 explicitly rejects (design.md:81) — so `bounds` must become a list the design never describes, and `test_output_contract.py` plus an `additionalProperties: false` JSON Schema both need that shape now, not at implementation time.

**Fix.** Pin it: a list sorted by `constraint_id`, each entry carrying the D10 identity triple, `operator`, and `operands[]` with `class | operand | ref | reached | entry_type`, plus `value` for literal operands. Note explicitly that `reached` is what makes `bounds` axis-varying rather than a constant block.

### S3 — Group-level `warnings` has no stated shape

Document-level warnings are `{kind, detail}` with an enumerated kind (design.md:184). The group-level list (design.md:188) gets no shape at all, yet it is what `test_warnings.py` asserts on (design.md:259) and what the JSON Schema must close over.

**Fix.** Same `{kind, detail}` shape, kinds `suffix_sibling | tie_candidate`. (With M2 applied, `suffix_sibling` is a mirror of `sibling_candidates`, or is dropped — either is fine, but say which.)

### S4 — Invariant 5 and its test disagree

Invariant 5 requires each catalog constraint to appear in reachable/unreachable **and** in `bounds` (design.md:125). `test_output_contract.py` asserts only "every contract constraint appears exactly once across reachable/unreachable" (design.md:262) — the `bounds` half is untested.

**Fix.** Extend that test line to cover `bounds`.

### S5 — The provenance-drift rationale argues against itself, and covers only one of the two recorded fingerprints

design.md:236: "The fingerprint gate cannot catch this (the contract file is inside the digested set, so a real contract change would already have fired)." The parenthetical supports the opposite of the sentence — if the contract is digested, a contract change *does* fire the gate; the drift case is a human re-pinning the indicator digest while leaving the recorded `semantic_fingerprint` stale. The warning is right; the reasoning as written will confuse the implementer about when it fires.

The same drift can happen to the recorded `executable_fingerprint`, which the report publishes (design.md:178) and which no gate or warning covers.

**Fix.** Reword the rationale to the re-pinning scenario, and either extend `provenance_drift` to both recorded fingerprints or state why only the semantic one is checkable.

### S6 — Say which block the `str`/`map` accept-set governs (Q3)

Verified: the committed file is 1220 `str` + 181 `map` nodes and nothing else, so the accept-set is correct today. But `metadata` is a block the trace never reads, and a future unquoted scalar there (`enabled: true`, a bare number in `run_description`) raises on content that is irrelevant to the trace.

**Fix.** One clause: either the accept-set governs the `modules` subtree and `metadata` gets a shape check only, or the standard scalar tags are accepted and string-ness is enforced where the `<type> <ref>` micro-syntax is parsed. Fail-closed remains the default; the design just needs to say which of the two it means, because the implementer will otherwise pick one silently.

---

## Notes

- **N1 — Label the uncovered provenance field.** `recorded_executable_fingerprint` (design.md:178) is read live from `contracts/package_contract.json`, which is deliberately outside the digested set (see Q5). Correct, but a record reader will assume digest coverage. One schema description line closes it.
- **N2 — D10 verified.** All five `concrete_entries` carry all three identities; the `constraint_id` hash suffix and the `mfe_viability::'...'` qualified names are exactly as the design describes (design.md:51). Additive, no Appendix A field harmed.
- **N3 — `constraints_reachable` map → list is an improvement, and the risk is prospective.** D4's uniqueness argument is sound in principle; note for honesty that the five real entries do have unique `source_local_identity` values, so the map is not broken today — the list is the better shape anyway.
- **N4 — `constraints_unreachable` is new relative to the spike** (which reported only the reachable map). Additive, and Invariant 5 needs it. Good.
- **N5 — `exploration/stellarator_e2e/studies/` does not exist.** The manifest's parent directory is a new directory; worth one line in the plan so it is created deliberately rather than by a stray `mkdir -p`.
- **N6 — Repo-convention claims check out.** `pyproject.toml:39` line-length 100, `pyproject.toml:51` `pythonpath = ["."]`, `jsonschema` 4.26.0 resolved in `uv.lock` transitively. `tests/conftest.py` exists with `tests/<area>/` subdirectories. All as design.md:55 states.
- **N7 — `verify_stellaris.compute()` verified.** `exploration/stellarator_e2e/verify_stellaris.py:168` defines `compute()` and the module has no CLI, so D6's typed `python_callable` oracle records what exists. As briefed, not relitigated.

---

## Dimensional Review

### 1. Spec Compliance
**Assessment:** Concerns

Every spec success criterion has a design element, and the design goes past the spec where the spec invited it: line numbers (spec.md:92 asked, design.md:45 delivered with probe evidence), the JSON Schema files (spec.md:91), the not-derivable carriage at both levels (spec.md:94, D5).

Capture-fidelity check: the design correctly treats `[INFERRED]` spec items as challengeable rather than fixed — D2 revisits the spec's recorded `safe_load` decision on probe evidence, which the spec explicitly permitted (spec.md:73), and D10 widens the identity set past the spec's two-field list with its reasoning stated. Both are legitimate.

The concern is the other direction: **M2** is an owner-side settled name dropped, which is the Compression law failing, and **M4**/**M5** leave two of the values Item 2 snapshots underspecified. Also worth noting the design silently promotes the spec's `[INFERRED]` "objective channel produced by no module is a mechanical failure" into a mechanical failure without re-marking it — harmless, since Item 1 probe 5 backs it.

### 2. Pattern Consistency
**Assessment:** Pass

Tests under `tests/<area>/` with a root `conftest.py` matches the repo (verified). No `__init__.py` under `scripts/study/` is correct given `pythonpath = ["."]`. Adding `jsonschema` explicitly rather than leaning on a transitive resolution is the right call. The `manifest.py`-as-seam pattern mirrors how the concept design already splits data-only manifest from tools.

### 3. Abstraction Quality
**Assessment:** Pass

Three layers and one seam module for a spec with nine invariants and two downstream consumers. I tried to delete each: removing `manifest.py` recreates the recipe in Item 4 (D3's rejection is right); removing the document-assembly discipline reintroduces partial output; removing the typed oracle object forces a string protocol that cannot be extended. Nothing survives deletion. The "strict reader with a conservative closure on top" framing is the design's strongest sentence — it makes the exit-code honesty a structural property rather than a rule to remember.

### 4. Duplication Avoidance
**Assessment:** Concerns

D9's deliberate double documentation (prose + JSON Schema) is justified — the schema files are the citable seam, the prose is the mental model, and a test binds them. Fine.

The real duplication is `bounds` versus `constraints_reachable`: both carry `operator`, `operands` with class/ref/reached, per group (design.md:188). This is inherited from Appendix A and from the spike, so it is not the design's invention, but the design should say the duplication is deliberate and which one is authoritative — otherwise the implementer will build one from the other and they will drift on the unreachable entries. Folded into **S2**.

### 5. Data Structure Clarity
**Assessment:** Concerns

The document skeleton (design.md:174-186) is explicit and good. The group object (design.md:188) is a prose sentence carrying eleven fields, three of which have no stated shape (`bounds`, group `warnings`, `trace_size`'s exact keys are given but its container is not) and one of which is missing (`sibling_candidates`). Since D9 commits to `additionalProperties: false` JSON Schemas and a test that validates real output against them, every one of these has to be pinned before the plan, not during it. **M2**, **S2**, **S3**.

The manifest schema (design.md:139-151) is by contrast fully explicit, down to worked example values. The group object should be rendered the same way — as a JSONC block, not a sentence.

### 6. Route Safety
**Assessment:** Pass

Not a routed service, so this reads as gate/dispatch safety. The gate order is fixed and justified (D8), there is no catch-all, and every fallback is a raise. The one place a wildcard could mask an error is the `pipelines/*.yaml` glob — and the design's instinct to close it was right, it just closed it too far (**M1**). The stdout/stderr split (report on stdout, human summary on stderr, design.md:199) is exactly right and prevents the most likely contamination path.

### 7. Bets & Decisions Integrity
**Assessment:** Concerns

B1, B2, B3 are genuine claims about reality with honest "if false" consequences, and B3 is admirably unflattering to the work (`R` fires 54 of 60 modules; the spec makes measuring it a non-goal, so it is watched, not fixed). B2's mitigation — per-file digests so a mismatch names the file — is a real mitigation, not a hedge.

Two problems:

- **B4 is a decision wearing a bet's clothes.** "One invocation per study, producing one document covering every proposed axis, matches how the record consumes indicators" is not a claim about reality that could turn out false — it is a choice the design makes, and the design also ships `--group` which contradicts it. Either make it an invariant and constrain the CLI (**S1**), or restate it as D-something with `--group` named as the rejected-in-the-record-path alternative.
- **One hidden bet.** The design rests on *the recipe's file set equalling the reader's file set*, and never states it. That equality holds today by coincidence of the EntryPoint's declared paths, not by construction. It is the load-bearing belief under the entire fingerprint gate, and it is unstated — which is the most expensive failure mode. **M3** converts it from a bet into an enforced invariant, which is the right resolution: do not state it as a bet, close it.

D1–D10 each name their rejected alternative with a reason, and the reasons are specific (D6's "a string cannot be extended without reinterpreting old manifests"; D3's "two implementations of a digest recipe drift into a false gate"). That part is well done.

### 8. Reader Comprehension
**Assessment:** Pass

"The Point" leads with the problem, not the mechanism. Core Concept gives a two-layer mental model and then states plainly why the split matters ("the split is what makes the exit codes honest"). The report-is-a-document insight is stated once, in plain words, and everything downstream hangs off it. A reader unfamiliar with Item 1 can skim this and come away with the system, the bets, and the decisions.

Two small drags, not blockers: the Research Findings section front-loads verified minutiae before the Core Concept explains what any of it is for — a reader hits `c9bc…c261` and per-file digests before they know the tool has two layers. And the group object being a run-on sentence (design.md:188) is the one place the prose hides structure the reader needs (see Dimension 5).

---

## Issues by Severity

### Critical
- **M1** `pipelines/__init__.py` is a sealed package artifact; the "any non-`.yaml` in `pipelines/`" rule fails on the real package at the first gate — design.md:155, 261 · Route Safety
- **M2** Appendix A's `sibling_candidates` dropped into `warnings`; spec.md:50 and the spike fixture both require the named field — design.md:170, 188 · Spec Compliance
- **M3** Fingerprint recipe does not provably cover the reader's file set; a regenerated entry ref outside `inputs/*.json` is read but not digested — design.md:155 vs 161/224 · Bets & Decisions
- **M4** Report path fields have no normalization rule, so identical facts can yield different digests — design.md:122, 176-181 · Data Structure Clarity
- **M5** `tool.source_digest` has no recipe, and Item 2 snapshots it — design.md:176 · Data Structure Clarity

### Major
- **S1** `--group` subset runs are indistinguishable from full runs in the output — design.md:74, 78, 240
- **S2** `bounds` shape unspecified and in conflict with D4 — design.md:81, 188
- **S3** Group-level `warnings` has no stated shape — design.md:188
- **S4** Invariant 5 requires `bounds` coverage; its test does not assert it — design.md:125, 262
- **S5** Provenance-drift rationale argues against itself; covers only one recorded fingerprint — design.md:236

### Minor
- **S6** Say which YAML block the `str`/`map` accept-set governs — design.md:161, 222
- **N1** Label `recorded_executable_fingerprint` as outside the digested set — design.md:178
- **N5** `exploration/stellarator_e2e/studies/` is a new directory — design.md:207
- Render the group object as a JSONC block rather than a prose sentence — design.md:188
- Consider moving Research Findings after Core Concept so the reader has the frame first

---

## Recommendations

1. **Fix M1 before anything else.** It is one clause and it is the difference between a tool that runs on the committed package and one that does not.
2. **Restore `sibling_candidates` (M2).** Appendix A field names are settled owner-side; additive is allowed, dropping is not.
3. **Close the recipe/reader coverage gap as an invariant, not a bet (M3).** A post-parse check that every resolved inputs path is in the pinned `files` list, plus a package-root containment rule. Keeps D8's ordering intact.
4. **Pin every value Item 2 snapshots (M4, M5).** Path normalization and a named `tool-source-digest/v1` recipe. Both reuse machinery the design already has.
5. **Pin the remaining output shapes before the plan (S2, S3), and add `groups_declared` (S1).** D9's `additionalProperties: false` schemas make these blocking for the schema files, and S1 lets Item 2 check subset-completeness mechanically instead of trusting the runbook.
6. **Sweep the small ones (S4-S6, N1, N5) in the same edit.** None needs discussion.

Nothing here touches the two-layer architecture, the gate order, the module split, the trace core, or any settled item. The must-fix list is five localized edits.

---

## Resolutions

_To be filled in as the owner resolves each issue. This section is what the design agent reads to incorporate the review._

---

**Overall:** Revise
**Verdict:** **APPROVE-WITH-FIXES** — M1 (`pipelines/` strictness fails on the real package), M2 (restore `sibling_candidates`), M3 (enforce recipe/reader file-set coverage), M4 (path normalization), M5 (`tool.source_digest` recipe); then S1-S6 as listed.

**Next Steps:** Record the owner's resolutions above, then re-run `/_my_design` (or return to the design-agent session) and point it at this review to incorporate. The reviewer does not edit the design.
