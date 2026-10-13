# Runbook

This runbook names study obligations and their record deposits. Stages may be brief, combined, or skipped when their responsibility is already satisfied or does not apply; record the reason or valid evidence in the existing record section. This does not waive executable gates, required record fields, original source checks, owner-reserved scientific decisions, or immutable results/runtime contracts. Reuse prior verification only after confirming its revision, scope, and environment remain valid. Changed inputs invalidate affected evidence.

**The rulebook** is `modeling_project/STUDY_POLICY.md`. This runbook does not restate it. Where a step must satisfy a rule, the step names the rule and the policy says what it is.

**The studies directory**, written `<studies-dir>`, is the one directory per studied package that the study policy's § Locations names. It holds the package's annex, its discovery log, and one directory per record.

**The record** is `<studies-dir>/<study-id>/`, named by `SKILL.md` before step 1 runs. `record-template.md` is copied to `record.md` there; section numbers below are that file's headings.

**The annex** is `<studies-dir>/ANNEX.md` — everything package-specific. `annex-template.md` beside this file is its starting shape, and § What a package annex supplies, at the end of this file, lists what the project provides. A step carrying an `**Annex:**` line cannot be executed from this file alone; the annex supplies the package's own facts for it. Steps without that line are package-free by construction, and that is what makes this runbook reusable.

**Fails closed** means the study stops. Only mechanical conditions gate: a missing key, a fingerprint mismatch, an unparseable artifact, a dirty package. An interpretive condition — an axis that looks uninteresting, a result that looks wrong — never gates. It is recorded and argued.

**Indicator vocabulary**, used exactly as fixed and never blurred:

- `no_constraint_response` is a **sound negative**: nothing in the model pushes back on this axis.
- `constraints_reachable` is a **possible path** to a constraint. It is never a claim that a constraint responds.
- `unresisted` is the **agent's recorded judgment**, never a tool output.

Not derivable from any indicator run, and disclosed in every record: monotonicity of a channel in an axis, identity of the same physical quantity across differing key names, and intra-module operand dependency.

---

## Execute

### 1. Open the record and deposit the captured intake

Copy `record-template.md` to the record path `SKILL.md` named, stamp the study header, and write the owner's goal and scope there in their own words. What the executor adds to make the goal executable is marked as the executor's own and kept separate from the quote.

**Calls:** none
**Deposits:** record.md § 1 Study header + § 2 Intake
**Fails closed when:** nothing mechanical
**Annex:** none

### 2. Declare each candidate axis as a qualified entry-key group

Every axis is declared at the attribute level and expanded to its complete entry-key set, with per-key provenance `fan_out | tie`. A tie is declared, never derived: it names the physical identity claimed and who claimed it. Sweeping a subset of a group is what this step exists to prevent.

**Calls:** the axis-declaration file `sysml-codegen study indicators` reads
**Deposits:** record.md § 7 Axis groups + the axis-declaration file
**Fails closed when:** a declared key is absent from the package's entry keys; an axis is declared empty; a key is duplicated inside a group
**Annex:** `§ Declared ties`

### 3. Run indicators for every proposed axis, including declined ones

An axis proposed and then declined is still traced, and its indicator and the reason it was declined both reach the record. `indicators.json` is copied into the record directory. The not-derivable disclosure is written out whether or not it bites.

**Calls:** `sysml-codegen study indicators`
**Deposits:** record.md § 8 Indicators and rulings + `indicators.json`
**Fails closed when:** the manifest fails validation; the indicator-input fingerprint does not match the package on disk; a declared key is not traceable; the run was narrowed to a subset of groups
**Annex:** none

### 4. Argue the framing, and obtain the user's ruling before any point runs

State each axis's framing as `search | sensitivity` and why. For every axis reported `no_constraint_response`, the user rules before execution and the record carries a model-development finding alongside the ruling: what should push back on this axis and is not modeled. The ruling does not discharge the finding. Assess the review triggers in the installed goal runbook, § Review scope and evidence reuse; a project without the goal layer applies the study policy's § Process sizing. Obtain focused independent review before dependent execution when triggered; otherwise record the coordinator check or valid reused coverage. New or reinterpreted source/math needs an independent check against original evidence. Owner-reserved framing decisions stay with the owner.

**Calls:** none
**Deposits:** record.md § 5 Framing (as proposed) + § 8 Indicators and rulings (rulings and findings) + § 14 Review outcomes (review verdict, reused coverage, or reason an independent critique was unnecessary)
**Fails closed when:** an axis reported `no_constraint_response` reaches execution with no user ruling recorded
**Annex:** none

### 5. Prepare the execution route and execute the pinned baseline point

Load the route and let it emit the package's identity document, then run exactly the manifest's pinned baseline point and deposit its result. Both documents are inputs to the gates in step 6 — the identity gate reads the identity document and the baseline gate reads the baseline result — so they must exist before those gates can read them. Nothing is argued here; the route's rationale is recorded at step 8, after the route has been exercised.

**Calls:** the execution route the study policy's § Execution routes names, supplied by the package annex
**Deposits:** `results/package_identity.json` + `results/baseline_result.json`
**Fails closed when:** the route cannot load the package
**Annex:** `§ Baseline pin`

### 6. Run the preflight gates

Every gate runs and every gate's outcome is recorded, pass or fail. A gate that did not run is recorded as not run, with its condition. The identity and baseline gates read the two documents step 5 deposited; they read them as data and never execute anything themselves. A cold reader must be able to see that the gates ran, not only that the study proceeded. Suffix-sibling findings are warnings and never gate.

**Calls:** `sysml-codegen study preflight gates`
**Deposits:** record.md § 9 Preflight results
**Fails closed when:** declared-group key validation fails; the baseline point does not reproduce the pinned headline; the manifest and package fingerprints disagree; the package is not git-clean
**Annex:** `§ Baseline pin`

### 7. Scan the candidate range with the independent oracle, then fix the window

The window is chosen after a scan, not before. Record what was scanned, what the scan showed, and what that fixed — and record the window's provenance as `engineered` or `sourced`. An engineered window is not a defect; an undisclosed one is. Any validity mask applied to the candidate range is a derived bound from held-fixed inputs, and the derivation is recorded.

A restated window — one inherited from an earlier record and re-run at a changed package — is scanned again here, not inherited as scanned: re-read its edges at the new package from an anchor that is feasible at the new package, and state each edge as caught or not caught before any point runs. The old edges were fixed by the old package's fences, and a package change that moves a fence can move the feasible region across an edge the old scan called caught.

**Calls:** the package-owned oracle, per the annex
**Deposits:** record.md § 11 Study definition and window provenance + snapshot `arms[].window`
**Fails closed when:** the oracle is unavailable or fails to run on the candidate range
**Annex:** `§ Oracle` and `§ Validity masks`

### 8. Choose the execution route and record why

Use a route the study policy's § Execution routes names; nothing else is a route. Record which route and what about this study led there. The rationale is written here, after step 5 first exercised the route and step 6 gated it — so it is an account of a route already known to load, not a prediction. Disclose in the same place anything the harness supplies that the model does not: per rung, what it supplies, why the model cannot, and which claims that scopes. The expected case is that nothing is harness-supplied, and the record says so: "glue ledger: none".

**Calls:** none
**Deposits:** record.md § 10 Execution route and why, including the glue disclosure
**Fails closed when:** nothing mechanical — the route's mechanical conditions gate at step 5
**Annex:** none

### 9. Run every point through the stock teax lifecycle

No hand-rolled sweep loop. Every point goes through the delivered lifecycle so that each one carries its inputs, its channels, and its per-constraint verdict into the store. The objective result and every executing constraint's status come out of this run and into the record by qualified identity — `constraint_id` and `source_local_identity`, not a short display name.

**Calls:** the route prepared at step 5 and argued at step 8
**Deposits:** `results/` + record.md § 3 Objective and result + § 4 Constraint outcomes
**Fails closed when:** any point fails to evaluate; the store rejects the study definition's compatibility tuple; the package is not git-clean after the run
**Annex:** none

### 10. Verify a sample against the package-owned oracle

Sample stratified by verdict combination, so the sample cannot miss a verdict the study produced. Re-derive the verdicts from the oracle's own operands rather than comparing the package's verdicts to themselves. Record the outcome, and record what verification did **not** cover — a value identical by construction on both sides is not independently verified, and saying so is part of the outcome.

**Calls:** `sysml-codegen study verify`
**Deposits:** record.md § 13 Verification + snapshot `arms[].verification` + `results/verification_summary.json`
**Fails closed when:** a sampled point exceeds the tolerance on a named channel; a re-derived verdict disagrees with the recorded one
**Annex:** `§ Oracle`

### 11. Judge each axis's framing against the observed result

The framing proposed at intake is a proposal. After the run, judge each axis's framing against what the run showed, and record it as judged next to it as proposed — with whether it changed and what changed it. Then write the per-axis account the judged framing owes: a search-framed axis owes the feasible structure found, and a sensitivity-framed axis owes the observed response plus an explicit statement that no boundary claim is made.

**Calls:** none
**Deposits:** record.md § 5 Framing (as judged) + § 6 Per-axis account
**Fails closed when:** nothing mechanical
**Annex:** none

### 12. Record the review outcomes

Record applicable correctness, claim limits, and readability checks with their outcomes and finding dispositions. Distinguish coordinator checks from independent verdicts. One review may cover several questions, including a goal round's dispositions where the goal layer is installed; cite valid coverage rather than repeating it at administration or, under the installed goal runbook, at its checkpoint and round closure. For a scoped independent check, provide the exact question, entry files/sections, original evidence, and a default six-tool-call/300-word return budget. A reviewer stops with named missing evidence instead of recursively loading context. The coordinator broadens scope for concrete uncertainty; coupled architecture, multiple model families, or failed coverage require substantive independent integration review. The same reviewer rechecks corrective diffs.

**Calls:** none
**Deposits:** record.md § 14 Review outcomes
**Fails closed when:** nothing mechanical
**Annex:** none

### 13. Write the report

Every number in the report traces to a committed artifact. A number that cannot be recomputed from something in `results/` does not go in. If the record's `teax.era_pin` is not null, state that pin as a reproduce prerequisite at the claim site, not only in a provenance note — a reader who copies a headline number must see what it takes to reproduce it.

**Calls:** none
**Deposits:** `results/`
**Fails closed when:** nothing mechanical
**Annex:** none

### 14. Register the findings and append the discovery-log rows

Collect every finding the study produced — the model-development findings from step 4, and whatever the run and the reviews turned up — into the record's findings register, each with an id, a kind, a disposition, and a home. `Home` is never blank; `unrouted` is a stated state. Then append one log row per finding, joined to the record by the same `<study-id>#<n>` id. The executor is the sole writer of first-sighting rows. A goal round may later append a joined disposition row under the same `<study-id>#<n>` id; it never edits a first-sighting row and never mints a new id (the installed goal runbook, § The discovery log; in a project without the goal layer, the same rule binds whoever dispositions a finding). This happens before the record is committed, so § 15 is filled when step 15 freezes it.

**Calls:** none
**Deposits:** record.md § 15 Findings + `<studies-dir>/DISCOVERY_LOG.md`
**Fails closed when:** a § 15 finding has no row, or a row names an id that is not in § 15
**Annex:** none
**Check:** from the record directory, run the command below and record it, with what it printed, in record.md § 14. It prints `[]` when every § 15 id has a discovery-log row and every log row for this study names a § 15 id.

```bash
python3 -c "import sys; sid = sys.argv[1] + '#'; bar = chr(124); ids = lambda path, col: {c for line in open(path) if line.startswith(bar) for c in [line.split(bar)[col].strip().strip(chr(96))] if c.startswith(sid)}; print(sorted(ids('record.md', 1) ^ ids('../DISCOVERY_LOG.md', 3)))" <study-id>
```

### 15. Resolve the snapshot and commit the record

Every snapshot value is resolved at this moment and copied in. Nothing in the record cites a live file for content: deleting or editing the manifest, the route, or the package must not change what the committed record says. State the cross-fingerprint correlation or its nil, and state what the record does not contain — gaps in the record itself, plainly, rather than left to inference. Then commit. From here the evidence is immutable: corrections are addenda, and `snapshot.json`, `indicators.json`, and `results/` are never edited.

**Calls:** none
**Deposits:** `snapshot.json` + record.md § 12 Cross-fingerprint correlation + § 16 Snapshot + § 17 What this record does not contain
**Fails closed when:** an unreplaced `<...>` placeholder remains in `record.md` (the § 15 findings register from step 14 included); a name under `manifest.content_used.fingerprint_names` has no key under `fingerprints`; an `arms[].store_id` does not resolve into `stores[]`; a result artifact has no digest
**Annex:** none
**Check:** from the record directory, run each command below and record it, with what it printed, in record.md § 14. The commands avoid a literal `<` so that recording them leaves the first check true.

```bash
# 0: no unreplaced placeholder (chr(60) is the opening angle bracket)
python3 -c "print(open('record.md').read().count(chr(60)))"
# []: every fingerprint name has a key under fingerprints
python3 -c "import json; s = json.load(open('snapshot.json')); print(sorted(set(s['manifest']['content_used']['fingerprint_names']) - set(s['fingerprints'])))"
# []: every arm's store id resolves into stores[]
python3 -c "import json; s = json.load(open('snapshot.json')); print(sorted({a['store_id'] for a in s['arms']} - {t['store_id'] for t in s['stores']}))"
# []: every result artifact has a digest
python3 -c "import json; s = json.load(open('snapshot.json')); print([f['path'] for a in s['arms'] for f in a['artifacts'] if not f.get('sha256')])"
```

---

## Administer

Synthesis is optional unless requested or needed to answer the task. The executor may synthesize directly, labeled as an executor reading. A separate administrator is used for a requested cold-record reading or uncovered independent review need, with a fresh self-contained brief and no inherited conversation. For either reading, evidence comes only from the committed record directory. Missing facts are reported as missing, never recovered from the live package, manifest, discovery log, or work items. An independent source/math review may separately inspect original evidence under its own brief; it does not repair missing historical facts in the record.

1. **Read the record directory only.** `record.md`, `snapshot.json`, `indicators.json`, and `results/`. The administrator is not given `<pkg>` and does not resolve paths outside the directory.
2. **Recover the recorded facts.** The framing per axis, the objective result, every named constraint outcome, and every finding — each traced to a committed artifact in the directory. Keep recorded facts, missing facts, and the administrator's interpretations distinct. The administrator may state an evidence-backed interpretation when it is labeled as the administrator's reading and cites the supporting record evidence. It must not attribute that interpretation to the executor or use it to claim that a missing historical fact was recorded. A fact that cannot be recovered is noted as it is found.
3. **Write `synthesis.md`** in the same directory. It is the administrator's only output; the executor's files are never touched.
4. **State what the record does not support.** Every fact that could not be recovered, and every claim the evidence in the directory does not carry. This section is mandatory and is empty only when nothing was missing.

The sequence ends there. An administrator does not append to `DISCOVERY_LOG.md` — a finding from a synthesis is filed by whoever acts on the synthesis. The goal round's joined disposition append is not an administrator act — the administrator stays read-only.

#### `synthesis.md`

The first synthesis of a record is `synthesis.md`. A later one is `synthesis-<YYYYMMDD>-<slug>.md` and never edits a prior one: a second administrator's read is a separate opinion, not a revision of someone else's.

Header stamps the administrator, the date, and the `snapshot.json` digest it read. Sections: what the study set out to do; what it found; the framing verdict per axis; the constraint structure; findings carried forward; and **What the record does not support**. Only paths inside the record directory may be cited. A fact the administrator cannot recover from the record is a defect in the record contract, not in the synthesis — file it as a process finding against the contract, not as a weakness of the read.

---

## `DISCOVERY_LOG.md`

One file per package, in its studies directory: `<studies-dir>/DISCOVERY_LOG.md`. An append-only index, newest row last — one row per finding *sighting*, plus any joined disposition rows a goal round later appends under the same id — never a second copy of the finding's account.

| Date | Kind | Record | Finding | Disposition | Home |
|---|---|---|---|---|---|
| YYYY-MM-DD | `model` \| `process` | `<study-id>#<n>` | one line | one line | path, or `unrouted` |

`<study-id>#<n>` is the id the record's § 15 uses, so log and record join without ambiguity. A row is either a first sighting, written by the executor at step 14, or a joined disposition update, written by a goal round (the installed goal runbook, § The discovery log) or, in a project without the goal layer, by whoever dispositions the finding. `Disposition` and `Home` carry that row's own state; for an id with more than one row, the newest row is its current state — scan for the id rather than stopping at the first row that matches.

---

## Naming

**Study id:** `<YYYYMMDD>-<goal-slug>`. The date sorts the studies directory chronologically and the slug makes it recognizable. On a same-day collision the first study is unsuffixed and the next ones append `-b`, `-c`.

**Arms:** `arm-<slug>`. A/B arms share one record directory and one `record.md`, and the same arm id is used in record subsections, in snapshot `arms[]` and `stores[]` entries, and in result filenames.

---

## The tools

The study tools ship with sysml-codegen. Run each as `sysml-codegen study <tool>`; `python -m sysml_codegen.study.<tool>` is the same command.

| Used at | Command |
|---|---|
| steps 2 and 3 | `sysml-codegen study indicators --package DIR --manifest FILE --groups FILE [--group NAME]... [--out FILE]` |
| pinning a manifest | `sysml-codegen study indicators --package DIR --print-fingerprint` |
| step 6 | `sysml-codegen study preflight gates --package DIR --manifest FILE --groups FILE --identity FILE --baseline-result FILE [--out FILE]` |
| any time | `sysml-codegen study preflight clean --package DIR [--out FILE]` |
| step 10 | `sysml-codegen study verify --package DIR --manifest FILE --identity FILE --store FILE... [--sample-size N] [--seed HEX] [--out FILE]` |
| before a study cites a package | `sysml-codegen study integrate`, documented in `integration-guide.md` beside this file |

Each tool either writes its one document and exits 0, or exits non-zero and writes nothing. `integrate` is the exception: once it starts, it writes a return on every exit. `--group` narrows an indicator run for debugging and marks the report `subset: true`; no record uses such a run.

**teax.** `verify` and `integrate` run teax and need its `simkit` package importable. Set `TEAX_SIMKIT_PATH` to the simkit root, the directory that holds `simkit/`. `integrate` puts that root on its producers' `PYTHONPATH` and reads the teax revision there, and a route under `integrate` may read teax's files only under it. Without teax, `verify` exits non-zero with a message naming teax and writes nothing.

**The project root.** Every path a document cites is relative to the project root, and a document's bytes are the same whichever directory the tool runs from. On the command line the root is, first match wins:

1. `SYSML_CODEGEN_PROJECT_ROOT`, when it is set;
2. otherwise, the git work tree that contains `--package`.

A tool refuses with exit 2, and writes nothing, when the package is in no git work tree and the variable is unset, or when the working directory is inside a different work tree from the package. A working directory outside every work tree is fine. Set the variable when the package's work tree is not the project, for example in a monorepo whose top level is not the modeling project. Without it, the tools there cite paths from the top level and read the top level's `pyproject.toml`.

A route or oracle that imports the tools as a library finds the root the same way, except that rule 2 uses the working directory's work tree. When neither rule applies, the library raises `RootError` (`sysml_codegen.study.roots`).

**A route under read coverage** (gate 7 of `integrate`, or `sysml_codegen.study.read_coverage.run_route` called directly) resolves the root by the command-line rules above, anchored on the package, before it starts observing. So a package in a git work tree needs no variable. A package in no work tree, with the variable unset, is refused before any route code runs: the receipt's `outcome` is `fail`, and its `route_error` is the `RootError` message, which names `SYSML_CODEGEN_PROJECT_ROOT`.

---

## What a package annex supplies

A study needs five pieces this runbook cannot supply, because only the package's owner knows them. The project writes them once per package, in the package's studies directory.

| Piece | What it is | Read at |
|---|---|---|
| The annex, `ANNEX.md` | The package's own facts, in the four sections below. Start from `annex-template.md`. | steps 2, 5, 6, 7 and 10 |
| The manifest | The study-package manifest: the package's identity, its pinned fingerprints, the objective catalog, the ties, the baseline point and the oracle. It validates against `study_package_manifest.v1`. `sysml-codegen study indicators --package DIR --print-fingerprint` prints its pin. | steps 3, 5, 6 and 10 |
| The axis declaration | The candidate axes as qualified entry-key groups. It validates against `axis_declaration.v1`. | steps 2, 3 and 6 |
| The route | A module whose `execute_baseline(out, *, package_dir, manifest_path)` runs the manifest's baseline point, writes `package_identity.json` and `baseline_result.json` under `out`, and returns a mapping whose `identity` and `baseline_result` entries are their paths; and whatever runs the study's points. The study policy's § Execution routes names it. | steps 5 and 9 |
| The oracle | An independent module the manifest's `oracle` block names. Its callable takes a point (entry key to value) and returns the package's channels by name. Its `operand_bindings()` says where each constraint operand takes its value: `{constraint_id: {operand: {"kind": "input" or "channel", "key": ...}}}`. | steps 7 and 10 |

The annex's four sections, cited by name in the steps above:

- `§ Declared ties`: which entry keys are one physical quantity, and who declared it (step 2).
- `§ Baseline pin`: the baseline point, its headline value and its verdicts, and where they came from (steps 5 and 6).
- `§ Oracle`: what the oracle computes, what it covers, and what it does not (steps 7 and 10).
- `§ Validity masks`: every bound applied to a candidate range, stated as a derivation from held-fixed inputs (step 7).

**The library surface a route or oracle may call:**

- `sysml_codegen.study.identity.build_sealed(package_name=..., package_root=...)` builds the package identity document from the sealed package;
- `sysml_codegen.study.common.write_document(document, path)` writes a document the way the tools do, whole or not at all;
- `sysml_codegen.study.common.tool_source_digest(files, root=<project root>)` digests the oracle's source files for the record's `oracle.source_digest`.

The seven document schemas ship at `sysml_codegen/study/schemas/`.
