# Operating the integration seam

`scripts/integrate.py` answers one question: **is there exactly one verified, study-ready candidate for this package — and if not, what stopped it?**

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

Read this before anything else, so you do not discover `--census-file` late.

```bash
uv run --env-file ~/1cfe/agentic-mbse/.env --env-file .venv/integration.env \
  python scripts/integrate.py \
    --audited-work work/completed/20260822_WI-030_computed-beta-peak-field@ba5c9945 \
    --models-root  exploration/stellarator_e2e/models \
    --package      exploration/stellarator_e2e/pkg/stellarator_tea \
    --manifest     exploration/stellarator_e2e/studies/manifest.json \
    --groups       tests/study/data/axes.known_answers.json \
    --census-file  tests/models/data/mfe_census.json \
    --expected-semantic-fingerprint   1ca93d0c988c2828bb1ce3fef18be85be86947a296a33b236d77daeb0f1ab860 \
    --expected-executable-fingerprint 7447efea9f205dc64543a976e6a3c21a9fd468726f2de78aaf8d845e6f2d9a97 \
    --expected-teax-revision          744745f895677f3344b9884627369a6a47ed987f \
    --route-sys-path exploration/stellarator_e2e/studies \
    --route-module   study_route \
    --route-callable execute_baseline \
    --out-dir        /tmp/integration-run
```

A full run takes about 15–20 seconds. Most of it is the model-family spine suite and the baseline execution.

---

## Where each input comes from

Nine inputs. Four of them are optional to `argparse` but **not** optional to the answer: leave one out and its gate reports *could not run*, which is a `BLOCKER`, not a pass.

| Flag | Where you get it | Required? |
|---|---|---|
| `--audited-work` | The work item you are integrating, cited `PATH@COMMIT` — ADR-006's citation form. Repeat it for several items. | Yes |
| `--models-root` | The SysML tree the package was generated from. For the stellarator package: `exploration/stellarator_e2e/models`. | Yes |
| `--package` | The generated package root. Supply it **once**; two values refuse as ambiguous lineage. | Yes |
| `--manifest` | The study-package manifest beside the route, `studies/manifest.json`. Once, same rule. | Yes |
| `--groups` | The axis declaration `preflight.py` calls `--groups`. The known-answer declaration under `tests/study/data/` is the usual one. | Yes |
| `--out-dir` | Anywhere you like, as long as it resolves **outside** the package root. Everything the run produces lands here. | Yes |
| `--route-sys-path`, `--route-module`, `--route-callable` | The package's own study route — the module holding `execute_baseline`. The seam invokes it rather than importing it, so it stays generic. | Yes |
| `--census-file` | `tests/models/data/mfe_census.json`. **Reaches gate 4 and nothing else** — see below. | Gate 4 cannot judge without it |
| `--expected-semantic-fingerprint` | `contracts/model_contract.json` → `semantic_fingerprint`, as recorded by the audited work. | Gate 9 cannot judge without it |
| `--expected-executable-fingerprint` | `contracts/package_contract.json` → `executable_fingerprint`. | Gate 9 cannot judge without it |
| `--expected-teax-revision` | `git -C "$STOP_PARSER_TEAX_ROOT" rev-parse HEAD` at the revision the audited work ran under. **You** supply it; the seam does not record a pin of its own, because a self-recorded pin re-records itself on drift and could never refuse. | Gate 1b cannot judge without it |

---

## The environment

Every producer the seam invokes needs this, and so does any study consuming the candidate afterwards. Copy-pasteable:

```bash
# The SysIDE licence. Generation and snapshot capture will not run without it.
export SYSIDE_LICENSE_KEY=...          # in ~/1cfe/agentic-mbse/.env, which does not export it itself

# The sealed toolchain artifacts. tests/test_dependency_provenance.py reads all four.
export STOP_PARSER_WHEEL_TARGET=/home/reid/1cfe/fusion-tea/.venv/lib/python3.12/site-packages
export STOP_PARSER_AGENTIC_WHEEL=/home/reid/1cfe/stop-parser-sealed-wheels/agentic_mbse-0.1.3-py3-none-any.whl
export STOP_PARSER_CODEGEN_WHEEL=/home/reid/1cfe/stop-parser-sealed-wheels/sysml_codegen-0.1.1-py3-none-any.whl
export STOP_PARSER_COSTINGFE_WHEEL=/home/reid/1cfe/stop-parser-sealed-wheels/1costingfe-0.1.0-py3-none-any.whl

# The teax checkout. verify.py imports simkit from under this root and does no sys.path work.
export STOP_PARSER_TEAX_ROOT=/home/reid/1cfe/teax
```

**The sealed wheels.** `/home/reid/1cfe/stop-parser-sealed-wheels/` holds the three wheel files whose sha256 values are pinned in `tests/test_dependency_provenance.py::WHEEL_HASHES`. They are outside the repository and are not installed by `uv`. If gate 1a refuses with a hash mismatch, check that these three paths point at those files before reading it as toolchain drift — verify with `sha256sum` against `WHEEL_HASHES`.

**Two `--env-file` flags instead of `export`.** The repository keeps the six `STOP_PARSER_*` values in `.venv/integration.env` (gitignored), so the whole environment is two flags on `uv run`:

```bash
uv run --env-file ~/1cfe/agentic-mbse/.env --env-file .venv/integration.env python scripts/integrate.py ...
```

The seam adds two things to whatever it inherits, for every subprocess it launches: the repository root and `$STOP_PARSER_TEAX_ROOT/packages/teax-simkit` on `PYTHONPATH`, and `STUDY_REQUIRE_TEAX=1` so a teax-dependent producer fails loudly instead of skipping and reporting green. If you invoke a producer by hand, do the same.

**All six variables are checked before any producer runs.** That is deliberate. `tests/test_dependency_provenance.py` reads the four wheel variables inside its *test body*, so an absent one raises a `KeyError` that pytest records as a test failure — which any seam that let gate 1a run first would report as a genuine toolchain refusal. Checking first is what keeps "you forgot to export a variable" from reading as "your toolchain drifted".

---

## Reading the answer

The return is at `<out-dir>/integration_return.json`, and a human-readable summary goes to stderr. If your request was rejected before it could be accepted at all — a missing input, an `--out-dir` inside the package — the document goes to **stdout** instead, because there was nowhere to write it.

### Exit codes

| Code | Meaning | What to do |
|---|---|---|
| **exit 0** | `CANDIDATE`. One verified, study-ready identity. | Cite it in your study. |
| **exit 1** | `BLOCKER`. The seam judged and stopped. | Read `blocker.condition` and act on the table below. |
| **exit 2** | The seam itself broke. It did **not** judge the package. | Read `seam_traceback.txt` in the out-dir. This is a defect in the seam, not a result about your package. |

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

Every path is repo-relative. `pin` is the manifest's own `fingerprints.indicator_inputs.digest` — the seam mints no identity of its own, it names the ones the producers already compute.

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
- **`condition`** — one of fourteen stable slugs. The table below is what to do about each.
- **`scope`** — `repo` or `request`. See the next section; on a gate-1a or gate-5 refusal this is the first thing to check.

Gates after the stop read **`not reached`**, never `did not run`. That distinction matters: `not reached` means the seam never got there, and tells you nothing about that gate.

---

## The ten gates, in order

The sequence stops at the first gate that is not a pass. The numbering is the requirements' — step 1 splits into two producers, so ten rows carry nine step numbers. `gate` in the return is the slug in the second column.

| # | `gate` | `scope` | Who judges it |
|---|---|---|---|
| 0 | `preconditions` | request | The seam: inputs resolve, all six environment variables are exported, `simkit` imports, the package tree is git-clean. Not one of the ten; it runs before any producer. |
| 1a | `pinned-packages` | repo | `tests/test_dependency_provenance.py` — the pinned revisions and the installed wheel artifacts. |
| 1b | `teax-revision` | request | The seam: `git -C $STOP_PARSER_TEAX_ROOT rev-parse HEAD` against `--expected-teax-revision`. No producer exists for this anywhere; the gap is filed. |
| 2 | `regeneration` | request | `sysml-codegen generate --smart-regen --preserve-handwritten`, in place, required to rewrite no byte outside `handwritten/`. |
| 3 | `handwritten-preservation` | request | The same comparison over `handwritten/`, which regeneration must never open. |
| 4 | `census-snapshot` | request | Snapshot recapture against the tracked file, byte for byte; and the entry-point census re-derived from the sealed package against `--census-file`. |
| 5 | `model-family-spine` | repo | `tests/models/test_model_family_spines.py` — the canonical tree, the family twins, the tracked census. |
| 6 | `manifest` | request | `scripts/study/manifest.py` — the manifest is this package's and its pin recomputes over the live package. |
| 7 | `preflight` | request | `scripts/study/preflight.py gates` — the six mechanical gates a study passes. Baseline execution happens just before this, and its failure is reported here as *could not run*. |
| 8 | `verification` | request | `scripts/study/verify.py` — oracle parity and re-derived verdicts, over the store this run executed. |
| 9 | `lineage` | request | The seam: the live fingerprints against the pair the request named. Last, because a package that failed an earlier gate has no lineage worth reporting. |

The seam mints nothing of its own except the two comparisons it has no producer for — the teax revision and the lineage — and both are against values **you** supply.

---

## Two gates judge the repository, not your package

`pinned-packages` (gate 1a) and `model-family-spine` (gate 5) carry `scope: repo`. Their producers accept no package argument by construction: the provenance suite reads `pyproject.toml`, `uv.lock` and the installed wheels, and the spine suite generates from the repository's canonical `models/` tree and compares against the tracked `tests/models/data/mfe_census.json`.

**Consequence you will meet in practice:** a dirty or mid-edit working tree can refuse gate 5 for reasons that have nothing to do with `--package`. If gate 5 refuses, check `scope` first, then check whether your working tree is clean, before you go looking at the package.

This is not a defect. Those two gates close the *other* end of the lineage chain that gates 4, 6 and 7 close at the package end.

## `--census-file` reaches gate 4 and nothing else

Gate 4 compares the file you pass against the sealed package: its entry-point count, its classification, and the semantic fingerprint it was derived against.

Gate 5 reads the **tracked** `tests/models/data/mfe_census.json` whatever you passed. It is the spine suite's own input and the flag does not reach it. If you pass a census from somewhere else, gate 4 judges that one and gate 5 still judges the tracked one.

---

## The fourteen conditions, and what to do about each

The right-hand column is the class a goal-layer caller maps the slug to. That mapping lives here, not in the seam: it is the goal layer's vocabulary and a native tool should not depend on it.

| `condition` | What happened | What you do | Goal class |
|---|---|---|---|
| `input-missing` | A required flag was absent, or an optional one its gate needed. | Add the flag. `detail` names it. | `STRATEGY_BLOCKER` |
| `input-invalid` | Something you supplied is unusable: `--out-dir` inside the package, a path that does not resolve, two `--package` values, or zero-or-several `*.snapshot.json` beside the models root. | Fix the value. You supplied it; do not re-supply the same thing. | `STRATEGY_BLOCKER` |
| `env-missing` | A variable was not exported, or a producer could not run past the environment sweep. | Export the variable from the block above, or read `detail` for the producer that could not run. | `MECHANICAL_FAILURE` |
| `toolchain-drift` | A pinned wheel, an installed revision, or the teax checkout is not what was expected. | Check the sealed-wheel paths first. If they are right, the toolchain genuinely moved and the audited work's lineage no longer holds. | `STRATEGY_BLOCKER` |
| `package-not-integrated` | Regenerating on the pin rewrote the package, or the tree was not git-clean. | **Go back to the modeling item.** Regenerate, recapture, re-pin, commit there. Re-running the seam will not change this. | `PREREQUISITE` |
| `handwritten-lost` | Regeneration did not preserve a hand-written implementation. | Same: the modeling item's work. A stubbed normative file is a failed gate even when the seal is clean. | `PREREQUISITE` |
| `census-stale` | The census does not match the sealed package, or is bound to a different semantic fingerprint. | Re-derive `tests/models/data/mfe_census.json` from the new package. Never hand-patch it to match. | `PREREQUISITE` |
| `snapshot-drift` | The recaptured snapshot is not the tracked one, byte for byte. | Check the toolchain-pin gate's result first — the snapshot pins toolchain versions as well as model content. If the pin is clean, the model state moved and the snapshot needs recapturing in the modeling item. | `PREREQUISITE` |
| `repo-lineage-broken` | The model-family spine suite refused: the canonical tree, the twins, or the tracked census. | Read the junit file the blocker cites. Check `scope` — this is about the repository, not your package. | `STRATEGY_BLOCKER` |
| `manifest-stale` | The manifest is not this package's, or its pin does not recompute over the live package. | Re-pin the manifest against the package, in the modeling item that changed it. | `STRATEGY_BLOCKER` |
| `preflight-refused` | One or more of preflight's six checks failed. | Open the whole `preflight_results.json` the blocker cites — it reports all six whatever happened, and more than one may have failed. | `STRATEGY_BLOCKER` |
| `verification-refused` | `verify.py` returned non-zero. | Read `verify_stderr.txt` in the out-dir. See the caveat below. | `STRATEGY_BLOCKER` |
| `lineage-mismatch` | The package verifies cleanly but is not the lineage you named. | Compare `expected` and `actual` in the blocker. Either you named the wrong lineage or you are integrating the wrong package. | `STRATEGY_BLOCKER` |
| `seam-internal-error` | The seam raised. It did not judge anything. | Read `seam_traceback.txt`. File it against the seam. | `MECHANICAL_FAILURE` |

**Caveat on `verification-refused`.** `verify.py` returns 1 for every cause and writes no summary when it refuses, so the seam cannot separate "verification failed" from "verify could not run" from its output. The seam checks verify's one environmental precondition itself at gate 0 — that `simkit` imports under the environment the subprocess will get — so past that a non-zero exit is read as a refusal. A teax import failure that probe did not predict will therefore arrive labelled `refused`. That shortfall is filed against `scripts/study/verify.py`.

---

## Citing a candidate in a study

The candidate's fields are the study's inputs. Nothing else is needed, and no seam code is involved:

```bash
uv run --env-file ~/1cfe/agentic-mbse/.env --env-file .venv/integration.env \
  python scripts/study/preflight.py gates \
    --package  "$(jq -r .candidate.package  <out-dir>/integration_return.json)" \
    --manifest "$(jq -r .candidate.manifest <out-dir>/integration_return.json)" \
    --groups   "$(jq -r .request.groups     <out-dir>/integration_return.json)" \
    --identity "$(jq -r .candidate.identity_document <out-dir>/integration_return.json)" \
    --baseline-result "$(jq -r .candidate.baseline_result <out-dir>/integration_return.json)"
```

**The one thing you derive rather than read: the store path.** `verify.py` needs `--store`, and the return does not carry it, because the route does not return one — it records a `store_id` inside the baseline result. Resolve it in two lines: read `executed_under.store_id` from the `baseline_result` the candidate cites; it is repo-relative when the run's output directory was under the repo root, and a bare filename otherwise, in which case the store is at `<out-dir>/_work/<that filename>`.

Record the candidate's `pin` and both fingerprints in the study record. They are the lineage that study's results belong to.

---

## What the seam writes, and where

Everything lands under `--out-dir`. **Nothing is ever written into the tracked tree**, whatever the return class.

| File | What it is |
|---|---|
| `integration_return.json` | The return. |
| `clean.json` | `preflight.py clean`'s own result over the package tree. |
| `junit/*.xml` | The two pytest producers' junit reports, one per gate. |
| `recaptured.snapshot.json` | Gate 4's recapture. |
| `package_identity.json`, `baseline_result.json`, `_work/*.db` | What executing the manifest's pinned baseline point deposited. |
| `preflight_results.json`, `verification_summary.json`, `verify_stderr.txt` | The two stock study gates' own output. |
| `_backup/` | The package tree as it stood before the first mutating gate. |
| `moved_files.txt` | Only on a byte-movement refusal: every path that moved. |
| `seam_traceback.txt` | Only on exit 2. |

---

## What the seam does not check

Stated so you do not assume otherwise.

- **`assert_read_set_covered` is not run.** Gate 6 runs three of the manifest's four assertions. The fourth needs the paths the indicator reader opened from the pipeline's own refs, which exist only inside that reader — so the seam cannot run it, and **nothing else in the repository runs it either**. The gate's own passing detail says so. Filed.
- **Gate 5's refusal path is not covered by a test.** Its pass path and its could-not-run path are; driving a real refusal out of it would need an edit to a tracked file or to a frozen producer. The shared junit-to-refusal mapping *is* proven, by gate 1a's wheel-hash fixture.
- **`verify.py` records `teax.revision: "unrecorded"`.** Stock teax exposes no `__version__`. The seam records the checkout's git revision in the return's `toolchain` block, but that does **not** discharge the open row against `verify.py`.

---

## Related

- `.project/adr/009-integration-is-a-fixed-point-proof.md` — why the seam proves rather than performs.
- `scripts/study/preflight.py`, `scripts/study/verify.py`, `scripts/study/manifest.py` — the producers, each with its own module docstring.
- `tests/study/test_integrate_*.py` — the seam's own tests, including five real refusals from real producers.
