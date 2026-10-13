# Operating the integration seam

`sysml-codegen study integrate` answers one question: **is there exactly one verified, study-ready candidate for this package — and if not, what stopped it?**

You give it an audited model change, the package that claims to be its integrated form, and the lineage you expect. It runs ten gates in the producers' own order and writes one JSON document. Either you get a `CANDIDATE` naming the package, its manifest, its pin and both fingerprints, or you get a `BLOCKER` naming the one producer that stopped the sequence and where its own output sits.

You do not need to have built the seam to run it. This page is everything you need.

---

## The one thing to know first

**The seam proves; it does not perform.**

It re-runs every producing step *in place* and requires each one to change nothing. It regenerates the package into itself and demands zero moved bytes. It recaptures the snapshot and demands the tracked file back. It recomputes the manifest's pin and demands the recorded value.

So the seam **refuses model work that has not yet been regenerated and committed.** If you get a refusal at the regeneration gate, that is not a bug in the seam and re-running it will not help. It means the modeling item that made the change is not finished: go back and regenerate, recapture, re-pin and commit there. Then run the seam.

The seam is the gate on the hop. It is not the hand that performs it.

---

## The full invocation, first

Read this before anything else, so you do not discover `--census-file` late. Every `<...>` is yours to fill.

```bash
sysml-codegen study integrate \
    --audited-work <work item path>@<commit> \
    --models-root  <models root> \
    --package      <package root> \
    --manifest     <studies-dir>/manifest.json \
    --groups       <axis declaration> \
    --census-file  <tracked entry-point census> \
    --expected-semantic-fingerprint   <hex> \
    --expected-executable-fingerprint <hex> \
    --expected-teax-revision          <sha> \
    --route-sys-path <directory holding the route module> \
    --route-module   <route module> \
    --route-callable execute_baseline \
    --out-dir        /tmp/integration-run
```

Run it from inside the project, or from a directory outside every git work tree, with the environment below. `python -m sysml_codegen.study.integrate` is the same command.

---

## Where each input comes from

Four inputs are optional to the request but **not** optional to the answer: leave one out and its gate reports *could not run*, which is a `BLOCKER`, not a pass.

| Flag | Where you get it | Required? |
|---|---|---|
| `--audited-work` | The work item you are integrating, cited `PATH@COMMIT`. Repeat it for several items. | Yes |
| `--models-root` | The SysML tree the package was generated from. Beside it there must be exactly one tracked `*.snapshot.json`: the snapshot gate 4 recaptures (§ The snapshot rule). | Yes |
| `--package` | The generated package root. Supply it **once**; two values refuse as ambiguous lineage. Its git work tree is the project root (§ Where the project root is). | Yes |
| `--manifest` | The study-package manifest in the package's studies directory, `<studies-dir>/manifest.json`. Once, same rule. | Yes |
| `--groups` | The axis declaration `preflight gates` reads as `--groups`. | Yes |
| `--out-dir` | Anywhere you like, as long as it resolves **outside** the package root. Everything the run produces lands here. A directory outside the project works, and is cited with `../` segments that resolve from the project root — see "Reading the answer". | Yes |
| `--route-sys-path`, `--route-module`, `--route-callable` | The package's own study route — the module holding `execute_baseline`. The seam invokes it rather than importing it, so it stays generic. | Yes |
| `--census-file` | The project's tracked entry-point census for this package. **Reaches gate 4 and nothing else** — see below. | Gate 4 cannot judge without it |
| `--expected-semantic-fingerprint` | `contracts/model_contract.json` → `semantic_fingerprint`, as recorded by the audited work. | Gate 9 cannot judge without it |
| `--expected-executable-fingerprint` | `contracts/package_contract.json` → `executable_fingerprint`. | Gate 9 cannot judge without it |
| `--expected-teax-revision` | `git -C "$TEAX_SIMKIT_PATH" rev-parse HEAD` at the revision the audited work ran under. **You** supply it; the seam does not record a pin of its own, because a self-recorded pin re-records itself on drift and could never refuse. | Gate 1b cannot judge without it |

**The census file** is a JSON object with three keys: `derived_against_semantic_fingerprint` (the package's `semantic_fingerprint`), `entry_points` (the number of parameters in `contracts/model_contract.json`) and `by_entry_type` (each `entry_type` to the sorted list of its parameter names, as `sysml_codegen.study.census.by_entry_type` groups them). Derive it from the package once and track it; gate 4 re-derives it and compares.

---

## The environment

Every producer the seam invokes needs this, and so does any study consuming the candidate afterwards:

```bash
# The SysIDE licence. Generation and snapshot capture will not run without it.
export SYSIDE_LICENSE_KEY=...

# teax's simkit root: the directory that holds simkit/, for a teax checkout
# <teax checkout>/packages/teax-simkit. Gate 1b reads the teax revision here.
export TEAX_SIMKIT_PATH=...

# Every variable the project's declaration lists under `environment`.
export ...
```

A file holding these lines works as well: `uv run --env-file <file> sysml-codegen study integrate ...`.

The seam adds four things to whatever it inherits, for every subprocess it launches: the project root and `$TEAX_SIMKIT_PATH` on `PYTHONPATH`; the project root it judged as `SYSML_CODEGEN_PROJECT_ROOT`, so every producer cites paths against the same root; and `STUDY_REQUIRE_TEAX=1`, so a teax-dependent producer fails loudly instead of skipping and reporting green. If you invoke a producer by hand, put the same two roots on `PYTHONPATH` and set `STUDY_REQUIRE_TEAX=1`. The project-root variable is needed by hand only where § Where the project root is says so.

**The seam's interpreter is every producer's interpreter.** It launches each producer, and the generator, as `<its own interpreter> -m ...`. Run it with the Python of the environment that holds sysml-codegen and teax's dependencies. A different environment does not run the producers just because it is the one your shell would pick.

**Every variable is checked before any producer runs:** `SYSIDE_LICENSE_KEY`, then each variable the declaration lists, then teax. That is deliberate. A repo-scope gate's test may read a variable inside its *test body*, so an absent one raises a `KeyError` that pytest records as a test failure — which any seam that let the gate run first would report as a genuine refusal. Checking first is what keeps "you forgot to export a variable" from reading as "your toolchain drifted".

**teax at gate 0.** With `TEAX_SIMKIT_PATH` set, it must hold `simkit/__init__.py`, and `import simkit` under the seam's environment must land inside it. Unset, that import must still succeed from wherever the environment provides it, because `verify` needs it; gate 1b then cannot run.

---

## The project's declaration

`integrate` judges any project, so the few facts that are the project's own are a table the project writes in the `pyproject.toml` at its project root:

```toml
# Example: a project with one wheel-directory variable and two repo-scope tests.
[tool.sysml-codegen.integrate]
environment = ["MYPROJ_WHEEL_DIR"]
backup-prefix = "myproj-integration-backup-"
record-distributions = { costing = "my-costing-lib" }
[tool.sysml-codegen.integrate.gates.pinned-packages]
target = "tests/test_toolchain_pins.py"
checked = "the toolchain revisions this project pins"
[tool.sysml-codegen.integrate.gates.model-family-spine]
target = "tests/test_model_tree.py"
checked = "the model tree generates and matches the tracked census"
```

- **`gates.pinned-packages`** (gate 1a) is meant to establish that the toolchain the project pins is the one installed: the revisions in its lock file and the artifacts actually present.
- **`gates.model-family-spine`** (gate 5) is meant to establish that the project's model tree still generates and agrees with what the project tracks about it, such as its census.
- Each gate has exactly two keys. `target` is the pytest target that judges it, relative to the project root, optionally `path::node`; it may not be absolute or lead outside the project. `checked` is the sentence the return states that gate examined. **`checked` has no default**, because a default would claim a check nobody declared.
- **`environment`** lists the variables the declared targets read. Gate 0 sweeps them with `SYSIDE_LICENSE_KEY`.
- **`record-distributions`** maps a key of the return's `toolchain` block to an installed distribution whose version is recorded there, beside the fixed keys `agentic_mbse`, `sysml_codegen`, `teax_revision` and `teax_module_path`.
- **`backup-prefix`** names the temporary directory the package is copied aside into (§ What the seam writes). It defaults to `sysml-codegen-integration-backup-`.

**A gate the project did not declare blocks.** Its row reads `not declared` for both `producer` and `checked`, and the seam returns a `BLOCKER` at that gate: `could_not_run`, `input-missing`. A `CANDIDATE` means all ten gates passed, so a project that wants one declares both. A malformed table (an unknown key, a gate without `checked`, a target outside the project) blocks at gate 0 with `input-invalid`.

## Where the project root is

Every path in the return is relative to the project root. The root is `SYSML_CODEGEN_PROJECT_ROOT` when it is set, and otherwise the git work tree that contains `--package`. The declaration is read from that root's `pyproject.toml`.

- **Refused, exit 2, no document:** the package is in no work tree and the variable is unset; or your working directory is inside a different work tree from the package. Run from inside the project, or from a directory outside every work tree.
- **Absent or repeated `--package`:** gate 0 rejects the request as usual, and the working directory's work tree anchors only the paths in that rejection.
- **A monorepo whose top level is not the modeling project:** nothing refuses, but the tools would cite paths from the top level and read its `pyproject.toml`. Set `SYSML_CODEGEN_PROJECT_ROOT` to the modeling project.
- **The route under read coverage.** Gate 7 runs the route with the root the seam judged. Run outside `integrate`, the read-coverage driver (`sysml_codegen.study.read_coverage.run_route`) resolves the root from the package by the rules above, before it starts observing. A package in a git work tree needs no variable. A package in no work tree, with the variable unset, is refused before any route code runs, and the receipt's `route_error` names `SYSML_CODEGEN_PROJECT_ROOT`.

## The snapshot rule

Gate 4 recaptures the snapshot and compares it with the tracked one, so it needs exactly one `*.snapshot.json` beside `--models-root`, in the models root's parent directory. Zero or several refuse as `input-invalid`. sysml-codegen's usual snapshot name, `instance_graph_snapshot.json`, does not match the pattern: name the tracked snapshot `<name>.snapshot.json`.

---

## Reading the answer

The return is at `<out-dir>/integration_return.json`, and a human-readable summary goes to stderr. If your request was rejected before it could be accepted at all — a missing input, an `--out-dir` inside the package — the document goes to **stdout** instead, because there was nowhere to write it.

### Exit codes

| Code | Meaning | What to do |
|---|---|---|
| **exit 0** | `CANDIDATE`. One verified, study-ready identity. | Cite it in your study. |
| **exit 1** | `BLOCKER`. The seam judged and stopped. | Read `blocker.condition` and act on the table below. |
| **exit 2** | The seam did **not** judge the package. Either it broke, or it never started: an argparse usage error, or no project root (§ Where the project root is). | If it broke, read `seam_traceback.txt` in the out-dir: a defect in the seam, not a result about your package. If it never started, no document was written; the message is on stderr. |

### A `CANDIDATE`

```json
{ "class": "CANDIDATE", "exit_code": 0,
  "candidate": { "package": "...", "manifest": "...", "pin": "...",
                 "semantic_fingerprint": "...", "executable_fingerprint": "...",
                 "identity_document": "...", "baseline_result": "...",
                 "verification_summary": "..." },
  "blocker": null,
  "gates": [ /* ten entries, all "pass" */ ] }
```

**Every path is relative to the project root**, not to your working directory and not to `--out-dir`. An `--out-dir` outside the project is cited with leading `../` segments, one per level of the project root's path — `--out-dir /tmp/integration-run` gives `identity_document: "../../…/tmp/integration-run/package_identity.json"` — which resolves correctly *from the project root and nowhere else*. Run the citation commands below from the project root, or join each path onto it yourself.

**`candidate.package` is the path the package root resolves to, which may not be the one you typed.** If the package root you pass is a symlink, the candidate names its target. That is deliberate — every gate digests, backs up and compares the real tree — and both paths name the same package.

`pin` is the manifest's own `fingerprints.indicator_inputs.digest` — the seam mints no identity of its own, it names the ones the producers already compute.

### A `BLOCKER`

```json
{ "class": "BLOCKER", "exit_code": 1, "candidate": null,
  "blocker": { "gate": "...", "producer": "...", "scope": "repo|request",
               "mode": "refused|could_not_run", "condition": "...",
               "detail": "...", "expected": null, "actual": null,
               "evidence": ["..."] },
  "gates": [ /* every gate before the stop, then "not reached" */ ] }
```

Three fields carry the weight:

- **`mode`** — `refused` means the producer ran and returned a negative verdict. `could_not_run` means something stopped it before it could judge anything. A goal caller's retry rule reads this: an inability to run may be an operational accident worth an identical retry; a refusal is a result about the candidate.
- **`condition`** — one of fifteen stable slugs. The table below is what to do about each.
- **`scope`** — `repo` or `request`. See the next section; on a gate-1a or gate-5 refusal this is the first thing to check.

Each row in `gates` carries one of four statuses, and the difference between the last two is the one to get right:

- **`pass`** — the gate ran and said yes.
- **`fail`** — the gate ran and refused. The stopping gate's own row says this, with the blocker's detail.
- **`did not run`** — the gate was reached and could not judge. The stopping gate's row says this when `mode` is `could_not_run`.
- **`not reached`** — the sequence never got to this gate. It tells you nothing about it, one way or the other.

So the gate that stopped the run always carries its own verdict. Only the gates strictly after it read `not reached`.

---

## The ten gates, in order

The sequence stops at the first gate that is not a pass. The numbers are the seam's step numbers. Step 1 has two producers, so ten rows carry nine step numbers. `gate` in the return is the slug in the second column.

| # | `gate` | `scope` | Who judges it |
|---|---|---|---|
| 0 | `preconditions` | request | The seam: the declaration is well formed, inputs resolve, `SYSIDE_LICENSE_KEY` and every declared variable are exported, `simkit` imports, the package tree is git-clean. Not one of the ten; it runs before any producer. |
| 1a | `pinned-packages` | repo | The pytest target the project declares under `gates.pinned-packages`, judging what its `checked` text states. |
| 1b | `teax-revision` | request | The seam: `git -C $TEAX_SIMKIT_PATH rev-parse HEAD` against `--expected-teax-revision`. No producer exists for this anywhere. Without `TEAX_SIMKIT_PATH` it could not run. |
| 2 | `regeneration` | request | `sysml-codegen generate --smart-regen --preserve-handwritten`, in place, required to rewrite no byte outside `handwritten/`. |
| 3 | `handwritten-preservation` | request | The same comparison over `handwritten/`, which regeneration must never open. |
| 4 | `census-snapshot` | request | Snapshot recapture against the tracked file, byte for byte; and the entry-point census re-derived from the sealed package against `--census-file`. |
| 5 | `model-family-spine` | repo | The pytest target the project declares under `gates.model-family-spine`, judging what its `checked` text states. |
| 6 | `manifest` | request | The manifest check (`sysml_codegen/study/manifest.py`) — the manifest is this package's, its pin recomputes, and resolved pipeline references are covered. |
| 7 | `preflight` | request | `sysml-codegen study preflight gates` — the six mechanical gates a study passes. Baseline execution happens just before this, and its failure is reported here as *could not run*. |
| 8 | `verification` | request | `sysml-codegen study verify` — oracle parity and re-derived verdicts, over the store this run executed. |
| 9 | `lineage` | request | The seam: the live fingerprints against the pair the request named. Last, because a package that failed an earlier gate has no lineage worth reporting. |

The seam mints nothing of its own except the two comparisons it has no producer for — the teax revision and the lineage — and both are against values **you** supply.

---

## Two gates judge the repository, not your package

`pinned-packages` (gate 1a) and `model-family-spine` (gate 5) carry `scope: repo`. Their producers are the pytest targets the project declares (§ The project's declaration), and they accept no package argument by construction. For example, a pin test reads the project's `pyproject.toml`, its lock file and the installed distributions, and a model-tree test generates from the project's canonical models and compares against a tracked census.

**Consequence you will meet in practice:** a dirty or mid-edit working tree can refuse gate 5 for reasons that have nothing to do with `--package`. If gate 5 refuses, check `scope` first, then check whether your working tree is clean, before you go looking at the package.

This is not a defect. Those two gates close the *other* end of the lineage chain that gates 4, 6 and 7 close at the package end.

## `--census-file` reaches gate 4 and nothing else

Gate 4 compares the file you pass against the sealed package: its entry-point count, its classification, and the semantic fingerprint it was derived against.

Gate 5 runs the declared target, which reads whatever census the project tracks for it, whatever you passed. The flag does not reach it. If you pass a census from somewhere else, gate 4 judges that one and gate 5 still judges the tracked one.

---

## The fifteen conditions, and what to do about each

The right-hand column is the class a goal-layer caller maps the slug to. That mapping lives here, not in the seam: it is the goal layer's vocabulary and a native tool should not depend on it.

| `condition` | What happened | What you do | Goal class |
|---|---|---|---|
| `input-missing` | A required flag was absent, an optional one its gate needed, or a repo-scope gate the project did not declare. | Add the flag, or declare the gate (§ The project's declaration). `detail` names it. | `STRATEGY_BLOCKER` |
| `input-invalid` | Something you supplied is unusable: `--out-dir` inside the package, a path that does not resolve, two `--package` values, zero-or-several `*.snapshot.json` beside the models root, or a malformed `[tool.sysml-codegen.integrate]` table. | Fix the value. You supplied it; do not re-supply the same thing. | `STRATEGY_BLOCKER` |
| `env-missing` | A variable was not exported, or a producer could not run past the environment sweep. | Export the variable from the block above, or read `detail` for the producer that could not run. | `MECHANICAL_FAILURE` |
| `toolchain-drift` | A pinned distribution, an installed revision, or the teax checkout is not what was expected. | Check the inputs the declared pin gate reads first — an environment variable naming the wrong file or the wrong interpreter's `site-packages` is misconfiguration, not drift — **and** that `TEAX_SIMKIT_PATH` names the checkout you meant. Only if both are right has the toolchain genuinely moved and the audited work's lineage no longer held. | `STRATEGY_BLOCKER` |
| `package-not-integrated` | Regenerating on the pin rewrote the package, or the tree was not git-clean. | **Go back to the modeling item.** Regenerate, recapture, re-pin, commit there. Re-running the seam will not change this. | `PREREQUISITE` |
| `handwritten-lost` | Regeneration did not preserve a hand-written implementation. | Same: the modeling item's work. A stubbed normative file is a failed gate even when the seal is clean. | `PREREQUISITE` |
| `census-stale` | The census does not match the sealed package, or is bound to a different semantic fingerprint. | Re-derive the tracked census from the new package (§ Where each input comes from). Never hand-patch it to match. | `PREREQUISITE` |
| `snapshot-drift` | The recaptured snapshot is not the tracked one, byte for byte. | Check the toolchain-pin gate's result first — the snapshot pins toolchain versions as well as model content. If the pin is clean, the model state moved and the snapshot needs recapturing in the modeling item. | `PREREQUISITE` |
| `repo-lineage-broken` | The declared model-family-spine target refused. | Read the junit file the blocker cites. Check `scope` — this is about the repository, not your package. | `STRATEGY_BLOCKER` |
| `manifest-stale` | The manifest is not this package's, or its pin does not recompute over the live package. | Re-pin the manifest against the package, in the modeling item that changed it. | `STRATEGY_BLOCKER` |
| `read-coverage-refused` | Baseline Python-observable file reads lacked a fresh successful receipt, read an undeclared dependency, changed a dependency, or attempted unsupported child/descriptor access. | Inspect `read_coverage.json`; repair dependency declarations or route behavior. Do not bypass the check. | `STRATEGY_BLOCKER` |
| `preflight-refused` | One or more of preflight's six checks failed. | Open the whole `preflight_results.json` the blocker cites — it reports all six whatever happened, and more than one may have failed. | `STRATEGY_BLOCKER` |
| `verification-refused` | `verify` returned non-zero. | Read `verify_stderr.txt` in the out-dir. See the caveat below. | `STRATEGY_BLOCKER` |
| `lineage-mismatch` | The package verifies cleanly but is not the lineage you named. | Compare `expected` and `actual` in the blocker. Either you named the wrong lineage or you are integrating the wrong package. | `STRATEGY_BLOCKER` |
| `seam-internal-error` | The seam raised. It did not judge anything. | Read `seam_traceback.txt`. File it against the seam. | `MECHANICAL_FAILURE` |

**Caveat on `verification-refused`.** `verify` returns 1 for every cause and writes no summary when it refuses, so the seam cannot separate "verification failed" from "verify could not run" from its output. The seam checks verify's one environmental precondition itself at gate 0 — that `simkit` imports under the environment the subprocess will get — so past that a non-zero exit is read as a refusal. A teax import failure that probe did not predict will therefore arrive labelled `refused`; `verify_stderr.txt` names teax when that is the cause.

---

## Citing a candidate in a study

The candidate's fields are the study's inputs. Nothing else is needed, and no seam code is involved:

```bash
sysml-codegen study preflight gates \
    --package  "$(jq -r .candidate.package  <out-dir>/integration_return.json)" \
    --manifest "$(jq -r .candidate.manifest <out-dir>/integration_return.json)" \
    --groups   "$(jq -r .request.groups     <out-dir>/integration_return.json)" \
    --identity "$(jq -r .candidate.identity_document <out-dir>/integration_return.json)" \
    --baseline-result "$(jq -r .candidate.baseline_result <out-dir>/integration_return.json)"
```

**The one thing you derive rather than read: the store path.** `verify` needs `--store`, and the return does not carry it, because the route does not return one — it records a `store_id` inside the baseline result. Resolve it in two lines: read `executed_under.store_id` from the `baseline_result` the candidate cites; it is project-relative when the run's output directory was under the project root, and a bare filename otherwise, in which case the store is at `<out-dir>/_work/<that filename>`.

Run these **from the project root**: every path in the return resolves against it.

Record the candidate's `pin` and both fingerprints in the study record. They are the lineage that study's results belong to.

---

## What the seam writes, and where

Evidence lands under `--out-dir`. Rollback copies use the system temporary directory, under the declared `backup-prefix`; `backup-location.json` records their location. They remain available after the invocation for recovery, subject to system temporary-file cleanup. Keep `TMPDIR` outside the project. Native result stores and reports remain under `--out-dir`.

| File | What it is |
|---|---|
| `integration_return.json` | The return. |
| `clean.json` | `preflight clean`'s own result over the package tree. |
| `junit/*.xml` | The two pytest producers' junit reports, one per gate. |
| `recaptured.snapshot.json` | Gate 4's recapture. |
| `manifest_read_coverage.json`, `read_coverage.json` | Static resolved-reference membership and the baseline Python read receipt, respectively. The latter includes source declarations, observed hashes, violations and limits. |
| `package_identity.json`, `baseline_result.json`, `_work/*.db` | What executing the manifest's pinned baseline point deposited. |
| `preflight_results.json`, `verification_summary.json`, `verify_stderr.txt` | The two stock study gates' own output. |
| `backup-location.json` | Location of the external package copy made before the first mutating gate. |
| `moved_files.txt` | Only on a byte-movement refusal: every path that moved. |
| `seam_traceback.txt` | Only on exit 2. |

---

## What the seam does not check

Stated so you do not assume otherwise.

- **File coverage is scoped to the baseline's Python-observable opens.** Gate 6 resolves pipeline references and calls `assert_read_set_covered`; the indicator report also calls this assertion. Gate 7 observes the route from import through baseline execution and requires a fresh successful `read_coverage.json` before preflight. Package seal and manifest identities cover package artifacts; exact declarations cover the Python sources of the route directory, of the installed study tools and of teax under `TEAX_SIMKIT_PATH`, and teax's installation metadata. Reads under the interpreter's own installation and its time-zone search path, and of `/dev/urandom` and `/dev/random`, are runtime reads. The receipt has a canonical `dependency_digest` over declared and observed identities, also recorded in gate 7 detail; it is separate from the sealed executable and indicator pin. Baseline scratch files use a fresh `TMPDIR` under the output directory. Atomic rename admission follows only newly created regular files to absent output destinations. Moves and deletions revoke admission at the source and descendants; incoming undeclared contents revoke destination admission. Hardlinks do not establish new-output admission. SQLite connections must start with an absent output database and absent WAL/SHM/journal sidecars; reconnects may use only that invocation's newly admitted store. This prevents stock baseline reuse of old cases without claiming observation of native SQLite bytes. Actual imported bytecode hashes are recorded alongside source identity; this does not prove source equivalence. Runtime files are hashed at first observed access and rechecked, not attested as an installation image. Newly created output files may be reread; pre-existing outputs are not automatically admitted. Audited subprocess/fork/exec attempts and integer-descriptor read-opens refuse. Native C/SQLite reads, directory metadata, mmap/direct syscalls, pre-opened handles, environment/network reads and post-observer execution remain outside observation. Hash checks have TOCTOU gaps, including transient restored mutations. One baseline establishes no coverage for other points or unexecuted branches. This is a cooperative check, not a sandbox.
- **`verify` records `teax.revision: "unrecorded"`.** Stock teax exposes no `__version__`. The seam records the revision `TEAX_SIMKIT_PATH` names in the return's `toolchain` block; that does not change what `verify` records.

---

## Related

- `runbook.md`, beside this guide — where a candidate enters a study, and § The tools for every tool's command line.
- The producers, `sysml-codegen study preflight` and `verify` and the manifest check — each module's docstring states what it checks and how it fails closed.

## Keep disposable execution files outside the project

Run pytest with its default temporary directory, or set `--basetemp` to a fresh external directory. Do not point it into an evidence directory. Keep JUnit XML and useful logs with the evidence. Retain native stores, artifact JSON and verification receipts deliberately, rather than committing copied package or tool trees.
