# Implementation Plan: Verified Package Integration Seam

**Status:** In Progress
**Created:** 2026-08-26
**Last Updated:** 2026-08-26
**Branch:** `feat/goal-integration-seam`
**Epic:** Goal Strategy and Task Harness (GSTH), Item 3
**Estimate:** 14–15 h across 10 phases, one commit each

## Source Documents

- **Spec:** `.project/active/goal-integration-seam/spec.md` — requirements R-A1…R-G4, success criteria SC1–SC6
- **Design:** `.project/active/goal-integration-seam/design.md` ← decisions D1–D18, bets B1–B6, the ten-gate table, the return schema, the validation table. **Approved round 2. Do not redesign.**
- **Design review:** `.project/active/goal-integration-seam/design_review.md` — M1–M8 resolutions and the round-2 verdict; the two advisory residuals are absorbed below (Phase 1 for `--out-dir`, Overall Validation Approach for the gate-5 boundary)
- **Spec review:** `.project/active/goal-integration-seam/spec_review.md`
- **Spikes:** `spike_regen_determinism.md` (B1 CONFIRMED), `spike_snapshot_stability.md` (B2 CONFIRMED). Both bets are facts; neither is re-litigated here.
- **Align:** `.project/active/goal-integration-seam/align.md` — owner rulings
- **Sibling precedent:** `.project/active/goal-research-seam/plan.md` (Item 2)

## The Point

Integration is the hop between an audited model change and a study that can run against it. Every gate that hop needs already exists and already fails closed — the toolchain pin test, `sysml-codegen generate`, the model-family spine suite, `manifest.py`, `preflight.py gates`, `verify.py`, `identity.py`. What does not exist is a boundary that owns them together. The sequence lives in two work-item plans and a pile of shell commands, so a goal task cannot request integration without reconstructing the hand pattern.

The cost has been paid once already. Item 6 opened with eleven red tests because a scaffold commit added a `magnet_capital` objective to the manifest without re-pinning the fixtures (`run-study-first-consumer/plan.md:305`). The check existed — the known-answer fixtures *were* the check, and they were already red. What was missing was a gate bound to the hop, so it fired far from the commit that broke it and only when a human happened to run the suite.

The obligation: turn audited model work into exactly one verified, study-ready candidate pin and fingerprint, or a named blocker. Two things make that return usable rather than merely correct. A goal agent reading a `BLOCKER` has to tell an operational accident it may retry from a semantic result that changes what work is justified — an unexported licence key is not a refusal. And a person who did not build the seam has to be able to operate the whole thing from its own documentation.

**The shape, in one line, because it is counter-intuitive:** the seam proves, it does not perform. It re-runs every producing step in place and requires each to change nothing. A candidate exists only for a package that is already a fixed point of the whole sequence. The consequence — the seam refuses model work that has not yet been regenerated and committed — is intended, derived in `design.md#core-concept`, and belongs in the operator guide in the operator's words.

## Implementation Strategy

### Phasing Rationale

Gate 0 goes first because it is where the design's own de-risk instruction points (`design.md#next-stage-handoff`): the accuracy of the `simkit`-importable probe under D16's environment decides whether gate 8's residual is narrow or wide, and it is a ten-minute check. Gate 0 also owns every environment precondition (D15, M2), so nothing downstream can be built correctly until it exists — every later gate's could-not-run classification is defined by what gate 0 already caught.

After that the order is dependency plus risk, not gate number:

- The **workspace fixture** (Phase 2) precedes every gate test, because R-G3 forbids a test writing into a tracked package and there is nowhere else for a gate test to run.
- The **digest and restore mechanism** (Phase 3) precedes every mutating gate, because it is what makes the byte gates real inside a gitignored workspace (D8) and what makes a refusal safe (D7). It is also the mechanism the review had to re-derive once (M3), so it gets its own phase and its own proof rather than riding along inside gate 2.
- **Gates in R-B1 order** across Phases 4–7, each phase ending with its own refusal fixture green, so no phase leaves an unexercised classification path behind it.
- **Composition tests** (Phase 8) after every gate exists, because SC3 and SC4 both need a full successful run.
- **Guide, ADR and filings** (Phase 9) after the behaviour is finished, so the guide documents what shipped.
- **Regression sweep** (Phase 10) last.

### Critical Path

gate 0 + return document → workspace fixture → digest/restore → gates 1a/1b/5 → gates 2/3/4 → gate 6 + baseline route + gates 7/8 → gate 9 + the sequence → SC3/SC4 → guide/ADR/filings → sweep.

### First Proof Point

**Phase 1**: gate 0's probe, run against a real environment, agrees with what the `verify.py` subprocess actually does. Concretely — with `STOP_PARSER_TEAX_ROOT` unset the probe refuses before any producer runs; with it set correctly the probe passes and a subsequent `verify.py` subprocess under D16's environment imports `simkit` from under that root. If the probe and the subprocess disagree, D15's classification rule is wrong and gate 8 will mislabel refusals; stop and report rather than widening the residual silently.

**Second proof point, Phase 5**: regeneration in place *inside the workspace* moves zero bytes. The spikes measured this on the real tree; the workspace has a different models root, and B1 has never been run there. If bytes move in the workspace but not in the tree, the fixture is wrong, not the seam.

### Overall Validation Approach

- Each phase starts by writing its tests, ends with those tests green, and ends with one commit.
- Every phase leaves the tree green: `uv run python -m pytest tests/study -q` passes at every commit point.
- No phase edits `scripts/study/`, `tests/models/`, or `tests/test_dependency_provenance.py` (R-B2). `git diff --stat` over those three paths is empty at every commit.
- No test writes a tracked file (R-G3). All gate tests run inside `integration_workspace`.
- Every refusal fixture drives a **real** producer to a real refusal (R-G4). No mocks anywhere in the gate path.

**Stated coverage boundary — gate 5's refusal path is not exercised, on purpose.** Carried here from `design.md#validation-approach` so `/_my_audit` sees it without reading the design. `tests/models/test_model_family_spines.py` accepts no package argument: it generates from the repo's canonical `models/` tree and compares against the tracked `tests/models/data/mfe_census.json` (`:353`). Driving a real refusal out of it needs an edit to that tracked census, an edit to the canonical `models/` tree, or an edit to the suite — which violate R-G3, R-G3-plus-a-model-change, and R-B2 respectively. So gate 5's refusal *content* is untested. What **is** tested: gate 5's pass path (every success-path run invokes it), its could-not-run path (gate 0's env sweep), and the junit-`<failure>`-to-`refused` mapping it shares with gate 1a — proven hermetically by the Phase 4 wheel-hash fixture. This is a recorded boundary, not a gap to be closed by a mock (R-G4 forbids that in letter and spirit). The producer gap is filed in Phase 9, item 3.

**Second recorded boundary:** `assert_read_set_covered` (R-B1.6's fourth assertion) is covered by no gate in this seam and by nothing else in the repo (D17). Filed in Phase 9, item 5.

---

## Field spellings — decided here

The design left these open (`design.md#next-stage-handoff`, "Open for the plan"). Fixed below; implement exactly these.

### CLI surface — `scripts/integrate.py`

Every flag is optional to argparse; required-ness is enforced inside the seam so a missing input is a `BLOCKER`, not an argparse exit 2 (D2).

```
--audited-work PATH@COMMIT        repeatable; ADR-006 citation form
--models-root DIR
--package DIR
--manifest FILE
--groups FILE                     the axis declaration preflight calls --groups
--census-file FILE                reaches gate 4 only (D9)
--expected-semantic-fingerprint HEX
--expected-executable-fingerprint HEX
--expected-teax-revision SHA
--route-sys-path DIR              mirrors manifest.oracle's three keys (D6)
--route-module NAME
--route-callable NAME
--out-dir DIR                     must resolve outside the resolved package root
```

### Return document — `<out-dir>/integration_return.json`

Exactly the schema at `design.md#architecture` ("Return shape"). Field names are that block's, verbatim. `schema_version` is `"integration-seam-return/v1"`.

### Gate names — the `gate` field's closed set

`pinned-packages` (1a), `teax-revision` (1b), `regeneration` (2), `handwritten-preservation` (3), `census-snapshot` (4), `model-family-spine` (5), `manifest` (6), `preflight` (7), `verification` (8), `lineage` (9). Gate 0's own refusals carry `gate: "preconditions"`. Statuses are `preflight.PASS` / `preflight.FAIL` / `preflight.DID_NOT_RUN` imported, plus the literal `"not reached"`.

### `condition` slugs — D14's set, plus one

D14's thirteen, unchanged: `input-missing`, `env-missing`, `toolchain-drift`, `package-not-integrated`, `handwritten-lost`, `census-stale`, `snapshot-drift`, `repo-lineage-broken`, `manifest-stale`, `preflight-refused`, `verification-refused`, `lineage-mismatch`, `seam-internal-error`.

**One addition, recorded rather than smuggled: `input-invalid`.** D14's set has no slug for an input that was supplied but is unusable, and gate 0 has two such cases with different operator actions than "you forgot a flag": `--out-dir` resolving inside the package root (the round-2 residual), and inputs that do not resolve to exactly one package or manifest (R-C5 / R-A3). Folding both into `input-missing` would tell the operator to supply something they already supplied. `input-invalid` maps to `STRATEGY_BLOCKER` on the goal side, the same as `input-missing`, so the mapping table gains a row and no class boundary moves. The guide enumerates **fourteen** slugs.

### Condition → goal-class mapping (guide-owned, D14; not imported into the seam)

| Slug | Goal class |
|---|---|
| `package-not-integrated`, `census-stale`, `snapshot-drift`, `handwritten-lost` | `PREREQUISITE` |
| `env-missing`, `seam-internal-error` | `MECHANICAL_FAILURE` |
| `input-missing`, `input-invalid`, `toolchain-drift`, `repo-lineage-broken`, `manifest-stale`, `preflight-refused`, `verification-refused`, `lineage-mismatch` | `STRATEGY_BLOCKER` |

### Workspace

Directory: `.integration_workspace/` at the repo root — inside the worktree so `repo_root()`-relative machinery resolves (D10), gitignored so R-G3 holds. `.gitignore` line: `/.integration_workspace/`. One workspace per refusal fixture (function-scoped), not shared: the fixtures doctor different files and a shared workspace would couple their assertions. The success-path workspace is function-scoped too; if the suite gets slow, that is a measurement to take in Phase 10, not an assumption to build on now.

---

## Phase 1 — Gate 0: preconditions, the environment probe, and the return document

**Estimate:** 2 h

### Goal

`scripts/integrate.py` exists, parses its flags, validates its inputs, sweeps every environment precondition in one place, and writes one return document with the right exit code. No producer runs yet.

### Assumption Under Test

That gate 0's `simkit`-importable probe, run under D16's environment, predicts what a `verify.py` subprocess under that same environment will do. This is the design's named de-risk (`design.md#next-stage-handoff`) and it decides whether gate 8's residual (D15) is narrow or wide.

### Test Stencil (Write This First)

```python
# tests/study/test_integrate_preconditions.py
ENV_VARS = ["SYSIDE_LICENSE_KEY", "STOP_PARSER_WHEEL_TARGET", "STOP_PARSER_AGENTIC_WHEEL",
            "STOP_PARSER_CODEGEN_WHEEL", "STOP_PARSER_COSTINGFE_WHEEL", "STOP_PARSER_TEAX_ROOT"]

@pytest.mark.parametrize("missing", ENV_VARS)
def test_each_env_var_unset_refuses_at_gate_zero(integration_workspace, missing, monkeypatch):
    monkeypatch.delenv(missing, raising=False)
    ret = run_seam(integration_workspace)                      # exit 1
    assert ret["class"] == "BLOCKER"
    assert ret["blocker"]["gate"] == "preconditions"
    assert ret["blocker"]["mode"] == "could_not_run"
    assert ret["blocker"]["condition"] == "env-missing"
    assert missing in ret["blocker"]["detail"]
    assert all(g["status"] == "not reached" for g in ret["gates"])   # no producer ran

def test_missing_required_input_is_a_blocker_not_a_usage_error(integration_workspace):
    rc, ret = run_seam_raw(integration_workspace, drop="--manifest")
    assert rc == 1 and ret["blocker"]["condition"] == "input-missing"   # never exit 2

def test_out_dir_inside_package_root_is_input_invalid(integration_workspace):
    ret = run_seam(integration_workspace, out_dir=integration_workspace.package / "out")
    assert ret["blocker"]["condition"] == "input-invalid"

def test_simkit_probe_agrees_with_the_verify_subprocess(integration_workspace):
    # the de-risk: probe verdict == what `verify.py --help`-free import path actually does
    assert probe_simkit(seam_env()) == subprocess_can_import_simkit(seam_env())
```

### Changes Required

**See `design.md` for:** gate 0's four steps → `design.md#architecture`; the subprocess environment → D16; exit codes → D18; the return schema → `design.md#architecture` "Return shape"; input validation → D2.

- [x] `tests/study/test_integrate_preconditions.py` (NEW)
- [x] `scripts/integrate.py` (NEW) — argparse surface per *Field spellings*; input validation (present, resolvable, exactly one package root and one manifest, `--out-dir` resolves outside the resolved package root); gate 0's env sweep naming all six variables; the D16 environment builder used by every later subprocess; the `simkit` probe; the return-document builder using `common.write_document`; `common.tool_source_digest` for `tool.source_digest`; the `preflight`-style human summary on stderr; the top-level exception handler writing `seam-internal-error` with the traceback path and exiting 2
- [x] Import `preflight.PASS` / `FAIL` / `DID_NOT_RUN` rather than re-spelling them

### Validation

**Automated:**
- [x] `uv run python -m pytest tests/study/test_integrate_preconditions.py -q` → pass
- [x] `uv run python -m pytest tests/study -q` → no regressions
- [x] `git diff --stat -- scripts/study/ tests/models/ tests/test_dependency_provenance.py` → empty

**Manual:**
- [x] `uv run python scripts/integrate.py --out-dir /tmp/i1` → `BLOCKER`, `input-missing`, exit 1, document written
- [x] With the full environment exported, run the probe standalone and confirm it agrees with a `verify.py` subprocess launched under `seam_env()`

**What We Know Works After This Phase:** every environment precondition is decided in one place, before any producer runs, so the standing wheel-variable `KeyError` can never be reported as a refusal; and a return document exists in every exit path including the crash path.

**Commit:** `integrate(seam): gate 0 preconditions, env probe, return document`

---

## Phase 2 — The `integration_workspace` fixture

**Estimate:** 1.5 h

### Goal

A gitignored in-repo workspace holding package, models, manifest, axes and census, with every materialized file's digest asserted equal to the tracked file's before the seam ever sees it.

### Assumption Under Test

That a materialized copy inside the worktree is byte-equal to the committed state and that `repo_root()`-relative machinery resolves against it — the precondition D13 needs for repo-scoped gates 1a and 5 to mean anything.

### Test Stencil (Write This First)

```python
# tests/study/test_integration_workspace.py
def test_every_materialized_file_matches_the_tracked_digest(integration_workspace):
    for rel, digest in integration_workspace.source_digests.items():
        assert manifest.sha256_file(integration_workspace.root / rel) == digest

def test_repo_is_clean_over_the_source_paths(integration_workspace):
    assert integration_workspace.repo_clean_over_sources is True

def test_manifest_package_path_is_repo_relative(integration_workspace):
    data = json.loads(integration_workspace.manifest.read_text())
    assert not Path(data["package"]["path"]).is_absolute()

def test_workspace_is_gitignored_and_removed(tmp_path):
    assert subprocess.run(["git", "check-ignore", ".integration_workspace"]).returncode == 0
```

### Changes Required

**See `design.md` for:** the fixture's contract and why it lives in `tests/study/conftest.py` → `design.md#component-overview`; the equality assertion → D10; reuse of the teax/licence machinery → `conftest.py:239-270`.

- [x] `.gitignore` — add `/.integration_workspace/`
- [x] `tests/study/test_integration_workspace.py` (NEW)
- [x] `tests/study/conftest.py` — one new fixture `integration_workspace`, materializing from `REAL_PACKAGE`, `REAL_MANIFEST`, `KNOWN_ANSWER_DECLARATION`, `models/`, `tests/models/data/mfe_census.json`; asserts each materialized file's sha256 equals the tracked file's and that the repo is clean over the source paths; rewrites `package.path` repo-relative the way `package_copy` does (`:207`); removes the workspace in a `finally`. Reuses `_stock_simkit_path` and the `STUDY_REQUIRE_TEAX` machinery rather than duplicating it. **No existing fixture's behaviour changes** (A12).

### Validation

**Automated:**
- [x] `uv run python -m pytest tests/study/test_integration_workspace.py -q` → pass
- [x] `uv run python -m pytest tests/study -q` → the pre-existing tally is unmoved except by the new tests. Record the before/after counts in Implementation Notes; A12 is checked by that number, not by assertion.
- [x] `git status --porcelain` → clean after the run (the workspace is removed and ignored)

**Manual:**
- [x] Interrupt a test mid-run (`-x` with a deliberate failure); confirm the `finally` still removes the workspace

**What We Know Works After This Phase:** gate tests have somewhere hermetic to run, and repo-scoped gates 1a and 5 are meaningful by construction rather than by luck.

**Commit:** `integrate(tests): integration_workspace fixture with committed-state assertion`

---

## Phase 3 — Content digest, backup, and restore-by-copy

**Estimate:** 1 h

### Goal

The seam's own before/after per-file sha256 comparison over the package tree, the pre-gate backup copy, and the restore that replaces changed files, deletes added files and restores removed ones.

### Assumption Under Test

That one git-independent restore mechanism works identically in the tracked tree and in the gitignored workspace — the M3 finding, whose first mechanism was a silent no-op exactly where the restore test runs.

### Test Stencil (Write This First)

```python
# tests/study/test_integrate_restore.py
def test_digest_catches_movement_git_reports_clean(integration_workspace):
    before = integrate.package_digests(integration_workspace.package)
    (integration_workspace.package / "contracts" / "model_contract.json").write_text("{}")
    assert subprocess.run(["git", "status", "--porcelain",
                           str(integration_workspace.package)],
                          capture_output=True).stdout == b""     # git is blind here
    assert integrate.moved_paths(before, integrate.package_digests(...))  # the seam is not

def test_restore_covers_changed_added_and_removed(integration_workspace, tmp_path):
    before = integrate.package_digests(pkg); integrate.backup(pkg, tmp_path / "_backup")
    _change_one(); _add_one(); _remove_one()
    integrate.restore(pkg, tmp_path / "_backup", before)
    assert integrate.package_digests(pkg) == before

def test_symlinked_package_root_resolves_before_digesting(integration_workspace):
    assert integrate.resolve_package(integration_workspace.package).is_dir()
```

### Changes Required

**See `design.md` for:** why the seam digests rather than trusting git → D8; the restore mechanism and its rejected alternatives → D7; the symlink and mtime traps → `design.md#implementation-notes`.

- [x] `tests/study/test_integrate_restore.py` (NEW)
- [x] `scripts/integrate.py` — `package_digests()` (per-file sha256 via `manifest.sha256_file`, resolved package root, repo-relative keys); `moved_paths(before, after)`; `backup()` copying to `<out-dir>/_backup/`; `restore()` driven by the before-digest so the restore set is exactly what moved; `moved_files.txt` written on a byte-movement refusal. **No mtime is read anywhere** — 95 of 153 files move mtime on a byte-identical run.

### Validation

**Automated:**
- [x] `uv run python -m pytest tests/study/test_integrate_restore.py -q` → pass
- [x] `uv run python -m pytest tests/study -q` → green

**Manual:**
- [x] `uv run grep -rn "st_mtime\|getmtime" scripts/integrate.py` → no matches

**What We Know Works After This Phase:** byte movement is detected and undone inside a gitignored tree, where `git status` reports clean whatever the bytes do. Every mutating gate can now be built safely.

**Commit:** `integrate(seam): content digests, backup, restore-by-copy`

---

## Phase 4 — Gates 1a, 1b, 5: subprocess producers and the junit mapping

**Estimate:** 1.5 h

### Goal

The three gates whose producers are pytest suites or a bare `git` call: the pinned-package check, the teax revision comparison, and the model-family spine suite — with the junit `<error>`/`<failure>` reading that gates 1a and 5 share.

### Assumption Under Test

That past gate 0's env sweep, a `<failure>` in the junit output is a genuine refusal and an `<error>` or a non-1 exit is a could-not-run — the mapping the design says junit does carry once environment failures have been pre-empted.

### Test Stencil (Write This First)

```python
# tests/study/test_integrate_refusals.py  (first fixtures; more land in Phases 5-6)
def test_wrong_expected_teax_revision_refuses_gate_1b(integration_workspace):
    ret = run_seam(integration_workspace, expected_teax_revision="0" * 40)
    assert ret["blocker"]["gate"] == "teax-revision"
    assert ret["blocker"]["mode"] == "refused"
    assert ret["blocker"]["condition"] == "toolchain-drift"
    assert ret["blocker"]["expected"] and ret["blocker"]["actual"]      # both recorded in full

def test_doctored_wheel_hash_refuses_gate_1a(integration_workspace, tmp_path, monkeypatch):
    # a real <failure> from tests/test_dependency_provenance.py:88-89, touching no tracked file
    monkeypatch.setenv("STOP_PARSER_CODEGEN_WHEEL", str(_wrong_bytes_wheel(tmp_path)))
    ret = run_seam(integration_workspace)
    assert ret["blocker"]["gate"] == "pinned-packages"
    assert ret["blocker"]["mode"] == "refused"
    assert ret["blocker"]["condition"] == "toolchain-drift"
    assert ret["blocker"]["scope"] == "repo"
    assert ret["blocker"]["evidence"]                                   # the junit file
    assert [g["status"] for g in ret["gates"][1:]] == ["not reached"] * 9
```

### Changes Required

**See `design.md` for:** the gate table rows 1a/1b/5 and their two-mode rules → `design.md#architecture`; per-gate scope → D13; why the seam does 1b itself → D5, R-B5; what junit does and does not carry → `design.md#implementation-notes`.

- [ ] `tests/study/test_integrate_refusals.py` (NEW) — the two fixtures above
- [ ] `scripts/integrate.py` — the subprocess runner using D16's environment; `--junitxml` into `<out-dir>/junit/`; the junit reader mapping `<failure>` → `refused` and `<error>`/non-1 exit → `could_not_run`; gate 1a (`pytest tests/test_dependency_provenance.py`, scope `repo`); gate 1b (`git -C $STOP_PARSER_TEAX_ROOT rev-parse HEAD`, compared casefolded with expected matched as a prefix of actual, both recorded in full); gate 5 (`pytest tests/models/test_model_family_spines.py`, scope `repo`); the stop rule and the `not reached` fill for later gates

### Validation

**Automated:**
- [ ] `uv run python -m pytest tests/study/test_integrate_refusals.py -q` → pass
- [ ] `uv run python -m pytest tests/study -q` → green
- [ ] `git status --porcelain` → clean (the wheel fixture touches no tracked file)

**Manual:**
- [ ] Run the seam with the real environment and confirm gates 1a, 1b and 5 all pass and each carries `scope` in the return

**What We Know Works After This Phase:** the junit-to-status mapping is proven by a real `<failure>` from a real producer — which is the only proof gate 5's refusal path will get, per the coverage boundary above. Gates 1a and 5 declare `scope: repo` in the return, so no reader mistakes what a pass covered.

**Commit:** `integrate(seam): gates 1a, 1b, 5 with the junit status mapping`

---

## Phase 5 — Gates 2, 3, 4: regeneration, handwritten preservation, census and snapshot

**Estimate:** 2 h

### Goal

The three mutating-in-place gates, each required to be a no-op, with the restore firing on a byte-movement refusal.

### Assumption Under Test

That B1 holds **inside the workspace**, not only on the real tree. The spikes measured regeneration and recapture against the repo's own `models/` root; the workspace has a different one. B2's spike already recaptured from a `/tmp` copy byte-identically, which is favourable evidence, but B1 in place inside the workspace has never been run. If bytes move here and not in the tree, the fixture is wrong — stop and report, do not relax the gate.

### Test Stencil (Write This First)

```python
# tests/study/test_integrate_refusals.py  (continued)
def test_edited_package_byte_refuses_gate_2_and_is_restored(integration_workspace):
    target = integration_workspace.package / "contracts" / "model_contract.json"
    before = target.read_bytes()
    _doctor(target)                                    # regeneration writes it back
    ret = run_seam(integration_workspace)
    assert ret["blocker"]["gate"] == "regeneration"
    assert ret["blocker"]["condition"] == "package-not-integrated"
    assert target.read_bytes() != before or True       # restore is asserted below, not here
    assert integrate.package_digests(pkg) == integration_workspace.entry_digests  # restored
    assert (out_dir / "moved_files.txt").exists()

def test_doctored_census_refuses_gate_4(integration_workspace):
    _bump_entry_points(integration_workspace.census)
    ret = run_seam(integration_workspace)
    assert ret["blocker"]["gate"] == "census-snapshot"
    assert ret["blocker"]["condition"] == "census-stale"
    assert ret["blocker"]["scope"] == "request"
```

### Changes Required

**See `design.md` for:** the gate table rows 2/3/4 → `design.md#architecture`; the census re-derivation through the producer's own helper and the `--census-file` scope → D9; whole-file snapshot byte comparison and why there is nothing to exclude → B2; the `{k: sorted(v)}` normalization → `design.md#implementation-notes`.

- [x] `tests/study/test_integrate_refusals.py` — the two fixtures above
- [x] `scripts/integrate.py` — gate 2 (`sysml-codegen generate --smart-regen --preserve-handwritten` in place, then the digest comparison; on movement, restore and refuse with `package-not-integrated`); gate 3 (the same comparison scoped to `generated/handwritten/`, `handwritten-lost`); gate 4 (`capture_instance_graph_snapshot` into `<out-dir>/recaptured.snapshot.json` compared whole-file against the tracked snapshot → `snapshot-drift`; `_by_entry_type` on the sealed package, normalized `{k: sorted(v)}`, against `--census-file`'s `by_entry_type` and `entry_points`, plus its `derived_against_semantic_fingerprint` against the live semantic fingerprint → `census-stale`; `--census-file` absent → `could_not_run`)

### Validation

**Automated:**
- [x] `uv run python -m pytest tests/study/test_integrate_refusals.py -q` → pass
- [x] `uv run python -m pytest tests/study -q` → green

**Manual:**
- [x] Run gate 2 alone against an untouched workspace and confirm zero moved paths (the B1-in-workspace proof); record the timing in Implementation Notes
- [x] Confirm the restored workspace's digests equal the entry digests after the gate-2 refusal fixture

**What We Know Works After This Phase:** the three mutating gates are no-ops on an integrated package, a byte that moves is caught and undone, and a stale census refuses at the package-scoped gate rather than the repo-scoped one.

**Commit:** `integrate(seam): gates 2, 3, 4 with byte-movement refusal and restore`

---

## Phase 6 — Gate 6, baseline execution, gates 7 and 8

**Estimate:** 2 h

### Goal

The manifest assertions, the caller-named baseline route that deposits what gates 7 and 8 read, and the two stock study producers invoked as a study invokes them.

### Assumption Under Test

That `execute_baseline`'s deposited `baseline_result.executed_under.store_id` resolves to a real store from `<out-dir>`, and that past gate 0 a non-zero `verify.py` exit is safely read as `refused` (D15).

### Test Stencil (Write This First)

```python
# tests/study/test_integrate_refusals.py  (continued)
def test_drifted_recorded_provenance_refuses_gate_7(integration_workspace):
    _drift_recorded_provenance(integration_workspace.manifest)   # check_manifest_currency
    ret = run_seam(integration_workspace)
    assert ret["blocker"]["gate"] == "preflight"
    assert ret["blocker"]["mode"] == "refused"
    assert ret["blocker"]["condition"] == "preflight-refused"
    assert ret["blocker"]["evidence"] == [".../preflight_results.json"]   # all six gates

def test_baseline_store_resolves_from_the_baseline_result(integration_workspace):
    store = integrate.resolve_store(out_dir / "baseline_result.json", out_dir)
    assert store.is_file()
```

### Changes Required

**See `design.md` for:** the gate table rows 6/7/8 → `design.md#architecture`; the route contract → D6; `assert_read_set_covered` out of reach → D17; gate 8's one discriminating signal → D15; store-path resolution → `design.md#implementation-notes`.

- [x] `tests/study/test_integrate_refusals.py` — the fixtures above
- [x] `scripts/integrate.py` — gate 6 (`manifest.load` → `assert_package_identity` → `assert_pin_matches`; `ManifestError` from `load` is `could_not_run`, from an assertion is `refused` with `manifest-stale`; the return records that `assert_read_set_covered` was **not** run, per D17); baseline execution between gates 6 and 7 via the caller-named route triple, its failure reported as gate 7 `could_not_run`; store resolution from `baseline_result.executed_under.store_id` with the `<out-dir>/_work/<name>` fallback; gate 7 (`preflight.py gates …--out`, `preflight-refused`); gate 8 (`verify.py …--out`, stderr captured to `<out-dir>/verify_stderr.txt`, any non-zero exit → `refused`, `verification-refused`)

### Validation

**Automated:**
- [x] `uv run python -m pytest tests/study/test_integrate_refusals.py -q` → pass
- [x] `uv run python -m pytest tests/study -q` → green

**Manual:**
- [x] With the full environment, run the seam through gate 8 on the untouched workspace and confirm `preflight_results.json` reads 6/6 and `verification_summary.json` reads `outcome: pass`

**What We Know Works After This Phase:** the seam runs the stock study producers with the arguments a study uses, on evidence it produced itself, and a preflight refusal cites the whole results document rather than one sub-gate (R-B4).

**Commit:** `integrate(seam): gate 6, baseline execution, gates 7 and 8`

---

## Phase 7 — Gate 9, the full sequence, and the success path

**Estimate:** 1.5 h

### Goal

The lineage comparison, the assembled ten-gate sequence with its stop rule, and the first `CANDIDATE`.

### Assumption Under Test

That the committed stellarator package passes all ten gates unchanged — B3, the bet that audited work arrives regenerated and committed. If it does not, the seam is a linter and that is a finding to report, not to work around.

### Test Stencil (Write This First)

```python
# tests/study/test_integrate_success.py
def test_committed_package_yields_one_candidate(integration_workspace):
    ret = run_seam(integration_workspace)                         # exit 0
    assert ret["class"] == "CANDIDATE" and ret["blocker"] is None
    assert len(ret["gates"]) == 10 and all(g["status"] == "pass" for g in ret["gates"])
    assert all(g["scope"] in ("repo", "request") for g in ret["gates"])
    for field in ("package", "manifest", "pin", "semantic_fingerprint",
                  "executable_fingerprint", "identity_document",
                  "baseline_result", "verification_summary"):
        assert _resolves(ret["candidate"][field])
    assert integration_workspace.tracked_tree_digest_unchanged()

# tests/study/test_integrate_lineage.py
def test_wrong_expected_fingerprint_refuses_at_gate_9(integration_workspace):
    ret = run_seam(integration_workspace, expected_semantic_fingerprint=_one_digit_off())
    assert ret["blocker"]["gate"] == "lineage"
    assert ret["blocker"]["producer"] == "scripts/integrate.py"
    assert ret["blocker"]["condition"] == "lineage-mismatch"
    assert ret["blocker"]["expected"] != ret["blocker"]["actual"]
    assert [g["status"] for g in ret["gates"][:9]] == ["pass"] * 9
```

### Changes Required

**See `design.md` for:** gate 9's row and why it is last → `design.md#architecture`; the ten-entry invariant → `design.md#required-invariants`; `blocker.producer` on the two self-judged gates → M6.

- [ ] `tests/study/test_integrate_success.py` (NEW), `tests/study/test_integrate_lineage.py` (NEW)
- [ ] `scripts/integrate.py` — gate 9 (live semantic and executable fingerprints against the request's expected pair; absent expected → `could_not_run`); the sequence driver with the stop rule, `not reached` fill, and the `CANDIDATE` assembly; `pin` read from the manifest's `fingerprints.indicator_inputs.digest`, not recomputed as a new number

### Validation

**Automated:**
- [ ] `uv run python -m pytest tests/study/test_integrate_success.py tests/study/test_integrate_lineage.py -q` → pass
- [ ] `uv run python -m pytest tests/study -q` → green
- [ ] `git status --porcelain` → clean after a full success run

**Manual:**
- [ ] Read `integration_return.json` from the success run end to end; every path, digest and identity resolves (R-E3)

**What We Know Works After This Phase:** SC1. One invocation produces one candidate whose every field resolves and matches the lineage the request named, with the tracked tree byte-identical before and after.

**Commit:** `integrate(seam): gate 9 lineage, sequence assembly, candidate return`

---

## Phase 8 — Re-run stability and the stock route

**Estimate:** 1 h

### Goal

SC3 and SC4: a second invocation on unchanged inputs returns the same identity, and the candidate is accepted by the stock preflight and verify route rebuilt from the return document alone.

### Assumption Under Test

That nothing in the seam's own output leaks into the identity — the three `candidate` fields that are `--out-dir` paths differ by construction and are not part of the claim (A8).

### Test Stencil (Write This First)

```python
# tests/study/test_integrate_rerun.py
def test_two_runs_same_identity(integration_workspace, tmp_path):
    a = run_seam(integration_workspace, out_dir=tmp_path / "a")
    b = run_seam(integration_workspace, out_dir=tmp_path / "b")
    for field in ("package", "manifest", "pin",
                  "semantic_fingerprint", "executable_fingerprint"):
        assert a["candidate"][field] == b["candidate"][field]

# tests/study/test_integrate_stock_route.py
def test_return_rebuilds_the_stock_commands(integration_workspace):
    ret = run_seam(integration_workspace)
    assert subprocess.run(_preflight_argv_from(ret)).returncode == 0
    assert subprocess.run(_verify_argv_from(ret)).returncode == 0
    # no import of scripts.integrate anywhere in this module
```

### Changes Required

**See `design.md` for:** the re-run invariant and what is excluded from it → `design.md#required-invariants`, R-D1/A8; why SC4 needs no hand-off step → D11.

- [ ] `tests/study/test_integrate_rerun.py` (NEW)
- [ ] `tests/study/test_integrate_stock_route.py` (NEW) — command lines rebuilt from `integration_return.json` fields only, no seam import
- [ ] `scripts/integrate.py` — only if the tests find a leak; no new machinery is planned here

### Validation

**Automated:**
- [ ] `uv run python -m pytest tests/study/test_integrate_rerun.py tests/study/test_integrate_stock_route.py -q` → pass
- [ ] `uv run python -m pytest tests/study -q` → green

**Manual:**
- [ ] `uv run grep -n "integrate" tests/study/test_integrate_stock_route.py` → only the run helper, no seam-internal import

**What We Know Works After This Phase:** SC3 and SC4. The seam is safe to call twice, and a study can consume its candidate with no seam-specific accommodation.

**Commit:** `integrate(tests): re-run stability and stock-route acceptance`

---

## Phase 9 — Operator guide, ADR, and the five filings

**Estimate:** 1.5 h

### Goal

The documentation SC6 is walked against, the decision of record is filed, and every producer shortfall the seam works around has a row against its own home.

### Assumption Under Test

That the guide is complete enough for a non-author: every input has a stated source, every exit code a stated meaning, every condition slug a stated operator action.

### Test Stencil (Write This First)

```python
# tests/study/test_integrate_guide_contract.py
GUIDE = Path("docs/integration_seam_operator_guide.md")

def test_guide_enumerates_every_condition_slug():
    body = GUIDE.read_text()
    for slug in integrate.CONDITIONS:            # all fourteen
        assert slug in body

def test_guide_lists_every_env_var_and_exit_code():
    body = GUIDE.read_text()
    for var in integrate.REQUIRED_ENV:
        assert var in body
    for code in ("exit 0", "exit 1", "exit 2"):
        assert code in body

def test_guide_states_the_repo_scoped_gates_and_the_census_scope():
    body = GUIDE.read_text()
    assert "--census-file" in body and "gate 4" in body
```

### Changes Required

**See `design.md` for:** the guide's contents → `design.md#component-overview`; the mapping → D14 and *Field spellings* above; the ADR text → `design.md` Appendix A.

- [ ] `tests/study/test_integrate_guide_contract.py` (NEW)
- [ ] `docs/integration_seam_operator_guide.md` (NEW) — assembling a request, with **where each input comes from** (the concept-design's seam row names only two of the eight); the full invocation, led with, so nobody discovers `--census-file` late; the D16 environment an operator must export, spelled as copy-pasteable lines; reading `CANDIDATE` versus `BLOCKER`; the D18 exit-code contract; the fourteen `condition` slugs with the goal-class mapping table above and one operator action each; citing a candidate in a study; that `--census-file` reaches gate 4 only; that gates 1a and 5 judge the **repository**, so a dirty working tree can refuse gate 5 for reasons unrelated to `--package`, and `scope` in the return is what tells them which happened; and the prove-don't-perform boundary in the operator's own words — *the seam refuses model work that has not been regenerated and committed; that work belongs to the modeling item, and the fix is to finish it there, not to re-run the seam.*
- [ ] `.project/adr/009-integration-is-a-fixed-point-proof.md` (NEW) — `design.md` Appendix A, in the six-section form `.project/adr/README.md` fixes, `grade: "[AGENT] 2026-08-26"` per `align.md:8`; add the row to `.project/adr/INDEX.md`
- [ ] `.project/backlog/BACKLOG.md` § Flagged — **five R-F5 rows plus the teax-pin row**, each naming its home and what the seam does instead:
  1. Census derivation has no importable home outside a test module — home `tests/models/test_model_family_spines.py` (`_by_entry_type`, `:169`); the seam imports a private test helper
  2. **fusion-tea has no automated teax revision pin** — home `tests/test_dependency_provenance.py`; the seam does the `rev-parse` comparison itself against a caller-supplied expectation (R-B5)
  3. The model-family spine suite is not parameterizable by package — home `tests/models/test_model_family_spines.py`; consequence: gate 5 is repo-scoped and its refusal path is untestable (the coverage boundary above)
  4. `verify.py` collapses both R-A6 modes into one exit code and writes no summary when it refuses — home `scripts/study/verify.py` (`:527-529`); consequence: gate 8's residual (D15)
  5. `assert_read_set_covered` has no caller outside the indicator reader — home `scripts/study/manifest.py` / `indicators.py:808`; consequence: R-B1.6's fourth assertion is covered by nothing
- [ ] The open `verify.py` `teax.revision: "unrecorded"` row (`DISCOVERY_LOG.md 20260821-power-cycle-ab#8`) — cite as still open in the guide and in row 4; the seam recording the revision does **not** discharge it (R-E4)

### Validation

**Automated:**
- [ ] `uv run python -m pytest tests/study/test_integrate_guide_contract.py -q` → pass
- [ ] `uv run python -m pytest tests/study -q` → green

**Manual:**
- [ ] Read the guide once as a stranger; every command in it is copy-pasteable and every input has a stated source
- [ ] `uv run agentic-mbse status` → no new parser warnings from the BACKLOG edit

**What We Know Works After This Phase:** SC6 has something to be walked against, the decision is challengeable at its root, and no producer shortfall is absorbed silently.

**Commit:** `integrate(docs): operator guide, ADR-009, five R-F5 filings`

---

## Phase 10 — Full sweep and SC map

**Estimate:** 0.5 h

### Goal

Prove no regression anywhere the seam reaches, and map every success criterion to the thing that verifies it.

### Changes Required

- [ ] Run the full affected set (below), all green
- [ ] Fill in the Implementation Notes sections, including the Phase 2 before/after tally and the Phase 5 timings
- [ ] Update `.project/CURRENT_WORK.md`

### Validation

**Automated (the R-B2 / R-G2 regression gate):**
- [ ] `uv run python -m pytest tests/models tests/study tests/test_dependency_provenance.py -q` → green
- [ ] `git diff --stat -- scripts/study/ tests/models/ tests/test_dependency_provenance.py` → **empty**
- [ ] `git status --porcelain` → clean
- [ ] `uv run python -m pytest tests/ -q` → whole suite, no other consumer disturbed

**Environment for this phase and every test phase:**
```bash
set -a; source ~/1cfe/agentic-mbse/.env; set +a     # SYSIDE_LICENSE_KEY (the file does not export it)
export STOP_PARSER_TEAX_ROOT=...                    # per tests/study/conftest.py:239-270
export STUDY_REQUIRE_TEAX=1                         # a teax skip must fail, not report green
export STOP_PARSER_WHEEL_TARGET=... STOP_PARSER_AGENTIC_WHEEL=... \
       STOP_PARSER_CODEGEN_WHEEL=... STOP_PARSER_COSTINGFE_WHEEL=...
```

### SC → verification map

| SC | Verified by |
|---|---|
| SC1 | `test_integrate_success.py` — ten gates pass, every candidate field resolves, both fingerprints match the request's lineage, tracked tree byte-identical |
| SC2 | `test_integrate_refusals.py` — five real refusals from real producers (gates 1a, 1b, 2, 4, 7), each naming producer, scope, mode, condition and its own evidence. **Gate 5's refusal path is a stated boundary, untested** — see Overall Validation Approach |
| SC3 | `test_integrate_rerun.py` — same pin, same both fingerprints, same package and manifest across two runs |
| SC4 | `test_integrate_stock_route.py` — stock commands rebuilt from the return document alone, both pass, no seam import |
| SC5 | The regression gate above |
| SC6 | **Not a test.** A fresh session that did not build the seam walks `docs/integration_seam_operator_guide.md` at `/_my_audit` and records every point where it had to read source or guess (spec SC6 Evidence form) |
| R-A6 could-not-run | `test_integrate_preconditions.py` — six variables unset in turn, all refusing at gate 0 before any producer runs |
| R-C8 / D7 | `test_integrate_restore.py` plus the gate-2 refusal fixture — the workspace is restored to its entry digests |
| R-B1.6 fourth assertion | **Covered by nothing.** D17 boundary, filed in Phase 9 item 5 |

**What We Know Works After This Phase:** the item is auditable against its spec.

**Commit:** `integrate: full sweep, SC map, CURRENT_WORK update`

---

## Risk Management

**See `design.md#potential-risks` for the full analysis.**

**Phase-specific mitigations:**

- **Phase 1** — if the `simkit` probe and the `verify.py` subprocess disagree, D15's classification rule is unsound. Stop and report; do not widen the residual by weakening the probe.
- **Phase 2** — the workspace-equals-committed-state assertion is the mitigation for repo-scoped gates being meaningless. If it cannot be made to hold, gates 1a and 5 prove nothing in tests and that is a finding, not a thing to skip.
- **Phase 3** — the restore path is exercised rarely and matters most. It gets its own test before any mutating gate exists, not after.
- **Phase 5** — B1 has never been measured inside the workspace. If regeneration moves bytes there, the fixture's models root is wrong; fix the fixture, never the gate.
- **Phase 5** — a gate-4 refusal caused by a toolchain version bump moving the snapshot's `authority` block reads as model drift. The return must name the cause; gate 1a is what should catch a pin drift first.
- **Phase 6** — `execute_baseline` does not return the store path. Resolve it from `baseline_result.executed_under.store_id`; if that resolution is ambiguous, report it rather than guessing a filename.
- **Phase 9** — the guide is what SC6 is walked against by a stranger. Write the full invocation first, not last.

## Out of scope — do not add

An `--apply` mode or any two-call perform-then-gate shape (owner question, `design.md#surfaced-the-spec-reads-as-perform-the-requirements-force-prove`); a lock, ledger, retry or idempotency wrapper (D12, R-F2); typed codes for R-C1–C5 beyond the `condition` slug (D4); a `--handoff` step (D11); stderr string-matching to classify `verify.py` (D15); mtime-based change detection (`design.md#implementation-notes`); any edit inside `scripts/study/`, `tests/models/` or `tests/test_dependency_provenance.py` (R-B2 — file instead, Phase 9); the goal layer's `PREREQUISITE` / `STRATEGY_BLOCKER` / `MECHANICAL_FAILURE` vocabulary inside `scripts/integrate.py` (D14); fixing the calc-then-compare parser limitation (R-F4); GOAL_RUNBOOK, DISCOVERY_LOG or the run-study runbook (Item 1's).

## Handoff lines (not this plan's scope)

- **Item 6** is the seam's first goal-side consumer: invoke, accept one candidate pin, run a study against it.
- **The concept-design's "pending native repair" marker** (`goal-strategy-task-harness-design.md:152,156`) goes false when this item lands. Retiring it is owed at epic close, not here.
- **Upstream (R-F3):** teax exposes no `__version__` for a tool to read. Same root cause as the open `verify.py` `teax.revision` row; neither is discharged by this item.

## Implementation Notes


### Phase 1 Completion

**Completed:** 2026-08-26 · **Commit:** see `impl(goal-integration-seam) phase 1:`

**Changes made**
- `scripts/integrate.py` (NEW, 560 lines) — the whole return-document surface plus gate 0's
  input validation and environment sweep. The ten-gate table is declared (`GATES`), the
  fourteen `condition` slugs are a closed set the `SeamBlocker` constructor enforces, and
  `preflight.PASS` / `FAIL` / `DID_NOT_RUN` are imported rather than re-spelled. No producer
  runs yet: every gate fills `not reached`.
- `tests/study/test_integrate_preconditions.py` (NEW) — 14 tests, all green.

**Test counts.** `tests/study` was **274 passed, 1 skipped** before this phase and is
**288 passed, 1 skipped** after. The pre-existing tally is unmoved (A12).

**First Proof Point — the de-risk passed.** `test_simkit_probe_agrees_with_the_verify_subprocess`
compares gate 0's probe with an independently built subprocess that does the bare
`import simkit` `verify.build_summary` opens with. They agree, with the teax root set and
with it unset. **D15's classification rule is sound and gate 8's residual stays narrow.**

**Decisions the plan left to implementation**
- **Where the return goes when `--out-dir` is unusable.** A rejected request answers on
  **stdout** (the convention `preflight.py`/`verify.py` use when `--out` is absent), so a
  return document exists in every exit path even when `--out-dir` is the input that was
  wrong. `--out-dir` inside the package root is refused *before* anything is written, and a
  test asserts the directory does not appear.
- **`--package` and `--manifest` are `action="append"`.** R-A3/R-C5 say ambiguous lineage is
  itself a `BLOCKER`; a plain flag would silently take the last one. Two `--package` values
  refuse with `input-invalid`.
- **Gate 0 step 3 (`preflight.py clean`) and step 4 (digest + backup) are deferred to Phase 3.**
  The plan's Phase 1 goal says "no producer runs yet" and `preflight.py clean` is a producer
  invocation; step 4 is Phase 3's own subject. Both land with the digest mechanism.

**Deviation from the stencil.** The Phase 1 stencil takes `integration_workspace`, which does
not exist until Phase 2. Gate 0 runs no producer and writes nothing outside `--out-dir`, so
these tests build a real request against the **committed** package read-only, with `--out-dir`
under `tmp_path`. R-G3 holds: no test writes a tracked file.

**Named risk, found before Phase 2 — gate 1a cannot pass in this environment.**
`tests/test_dependency_provenance.py::test_installed_artifacts_are_the_recorded_wheels_and_public_apis`
compares each wheel's sha256 against `WHEEL_HASHES`. The recorded wheel artifacts are not on
this machine: the only wheels present are uv's own git-built ones
(`~/.cache/uv/sdists-v9/git/...`), whose hashes differ (`067f749e…` vs the recorded
`7505028f…` for agentic-mbse). Measured, not inferred — the suite was run with all four
variables exported. Consequence for the plan is recorded under Phase 4.
### Phase 2 Completion

**Completed:** 2026-08-26

**Changes made**
- `.gitignore` — `/.integration_workspace/`.
- `tests/study/conftest.py` — one new fixture, `integration_workspace`, plus the
  `IntegrationWorkspace` record. Materializes the resolved package tree, `models/`, the
  tracked snapshot, the manifest, the axis declaration and `mfe_census.json` into a
  gitignored directory at the repo root, asserts every materialized file's sha256 equals the
  tracked file's *before* the one rewrite the schema forces, and removes the tree in a
  `finally`. Reuses `stock_simkit_path`, so a missing teax root fails loudly under
  `STUDY_REQUIRE_TEAX=1` rather than reporting green. No existing fixture changed.
- `tests/study/test_integration_workspace.py` (NEW) — 10 tests.

**Test counts.** `tests/study` 288 → **298 passed, 1 skipped**. Pre-existing tally unmoved.

**Two decisions the stencil did not fix**
- **`source_digests` and `entry_digests` are separate.** The stencil asserts every
  materialized file equals its tracked digest, but the fixture must rewrite
  `package.path` — the schema requires it repo-relative and the workspace is a different
  root. One field would have to lie about one file. So `source_digests` is the tracked
  truth (the materialization proof) and `entry_digests` is what the workspace holds at
  entry (the restore target Phase 3 and Phase 5 compare against). A test asserts the two
  differ in exactly one file, and names it.
- **The layout mirrors the tracked tree.** The package root is a symlink to `../generated`
  and the snapshot sits beside the models root, because gate 4 *finds* the tracked snapshot
  rather than being told it — the request has no `--snapshot` flag, per the design's own
  data-flow list — and the seam must resolve the symlink before digesting. A test pins each.

**Manual check.** A deliberately failing test under `-x` still leaves no
`.integration_workspace/`: the `finally` runs on the fixture's generator teardown, and
`test_the_workspace_is_removed_after_the_fixture` asserts the absence from a later test.
### Phase 3 Completion

**Completed:** 2026-08-26

**Changes made**
- `scripts/integrate.py` — `resolve_package`, `package_digests`, `moved_paths`, `backup`,
  `restore`, `cite_moved`, and the producer subprocess runner `run_producer`. Gate 0's
  step 3 is wired: `assert_package_clean` invokes `preflight.py clean --package --out`
  rather than reimplementing the check, and a dirty tree refuses with
  `condition: package-not-integrated` citing `clean.json`.
- `tests/study/test_integrate_restore.py` (NEW) — 7 tests.

**Test counts.** `tests/study` 298 → **305 passed, 1 skipped**.

**What the tests prove.** Byte movement is caught inside the workspace on the same run
where `git status --porcelain --untracked-files=all` returns empty — the two are asserted
side by side, so the vacuous-in-its-own-harness failure mode is closed by evidence rather
than by comment. The restore covers changed, added and removed in one fixture and puts the
tree back to its entry digests, and a separate test proves it rewrites nothing outside the
moved set (an untouched file's mtime is unchanged after a restore).

**Digest keys are package-relative, not repo-relative** (the plan said repo-relative). The
backup mirrors the package tree, so a repo-relative key would have to be un-mapped on every
copy and unlink. Mechanism uses package-relative keys; `cite_moved` renders the repo-relative
paths the return and `moved_files.txt` cite. One test pins the citation form.

**Gate 0 step 4 (the before-digest and the backup) is not wired into `run()` yet.** Phase 3's
Changes Required lists the mechanism, not the wiring, and there is no sequence for it to hand
its baseline to until Phase 5. `package_digests` and `backup` are called by the gate-2 path
when it lands.

**A guard added, not in the plan.** `build_return` now raises when it is asked to emit a
`CANDIDATE` with any gate not `pass`. That is the ten-gate invariant made mechanical; it also
means that until the sequence exists, a fully valid request exits **2** with
`seam-internal-error` — the seam saying it is incomplete rather than minting an empty
candidate. No test encodes that interim state.
### Phase 4 Completion

**Complete 2026-08-26 — second attempt, after the environment blocker below was resolved by the orchestrator.** Gates 1a/1b/5 implemented (`junit_outcome`, `run_pytest_gate`, `REFUSAL_CONDITION`, `GateOutcome`, `run_sequence` with the stop rule); `tests/study/test_integrate_refusals.py` added (4 tests; the gate-1a refusal is a real hash failure at `tests/test_dependency_provenance.py:89` via a doctored `STOP_PARSER_CODEGEN_WHEEL` — the one proof of the shared junit mapping, per the gate-5 coverage boundary). `tests/study` 309 passed 1 skipped; provenance 3/3 green against the restored sealed wheels. **Wheel home:** `/home/reid/1cfe/stop-parser-sealed-wheels/` (outside the repo, sha256-verified against `WHEEL_HASHES`; recovered from `/tmp/stop-parser-rev2/artifacts-closeout-sealed/wheels/`) — goes in the operator guide env section (Phase 9). Env delivery: `.venv/integration.env` (gitignored) + `uv run --env-file` because the sandbox rejects `set -a; source`. Committed by the orchestrator: the resumed session lost git approval (resume does not inherit implement's bypassPermissions — the known permission wall). The record below is the first attempt's finding, kept as history; its "blocks Phases 4-8" conclusion is superseded by the wheel restoration.

---

**First-attempt record (superseded): stopped here and reported. This is an environment premise problem, not a
plan defect, and it blocks Phases 4 through 8 as written.**

**The finding, measured.** Gate 1a's producer cannot pass on this machine.
`tests/test_dependency_provenance.py::test_installed_artifacts_are_the_recorded_wheels_and_public_apis`
compares each installed wheel's sha256 against `WHEEL_HASHES` (`:88-89`). The recorded wheel
artifacts do not exist here. The only wheels present anywhere on the machine are uv's own
git-built ones under `~/.cache/uv/sdists-v9/git/`, and their hashes differ:

| distribution | recorded in the producer | present on this machine |
|---|---|---|
| agentic-mbse | `7505028f2fc7…54f7` | `067f749ea90e…b7d4` |
| sysml-codegen | `cca661ce1ad5…dbc5` | `b5cbe6713561…5a65` |
| 1costingfe | `970ed533d8fa…fcfd6` | `32be90e7987c…cbc4` |

Run with all four `STOP_PARSER_*` variables exported and the pinned modules resolving under
`STOP_PARSER_WHEEL_TARGET`: **1 failed, 2 passed**, on the hash assertion. The repo's own
records call this the sealed-runner environment's business
(`.project/completed/20260821_stellarator-model-migration/plan.md:598`).

**Why it blocks more than gate 1a.** The stop rule is the contract: no gate runs after an
earlier one refuses. Gate 1a is first, so every invocation in this environment stops there.
That makes unreachable, as written:

- Phase 4's gate-1b fixture (`test_wrong_expected_teax_revision_refuses_gate_1b`)
- Phase 5's gate-2 and gate-4 refusal fixtures
- Phase 6's gate-7 refusal fixture and the baseline-store resolution check
- Phase 7's `CANDIDATE` (SC1) and the gate-9 lineage refusal
- Phase 8's re-run and stock-route tests (SC3, SC4)

What *is* reachable and unaffected: gate 1a's own refusal fixture — the standing state is
already a real `<failure>` from a real producer, so the junit-to-status mapping the coverage
boundary rests on can still be proven without doctoring anything.

**What this is not.** It is not a reason to relax gate 1a, to mock a producer (R-G4 forbids
it in letter and spirit), or to drop gate 1a from the sequence (R-B1 is `[HARD]`: each gate
is invoked). The seam is behaving correctly: in an environment whose toolchain artifacts are
not the recorded ones, the honest return *is* `BLOCKER / pinned-packages / toolchain-drift`.

**The decision the plan cannot make.** Either (a) the recorded wheel artifacts are restored
to this machine and the four variables point at them, after which Phases 4–8 run as written;
or (b) the success-path and past-gate-1a tests take a stated environment precondition and
skip with the resolved reason when it is unmet, on the pattern `tests/study/conftest.py:239-270`
already uses for teax, with an escalation variable so a CI run fails rather than reports
green. (b) changes what SC1/SC3/SC4 are proven by and needs recording in the SC map, so it
is surfaced rather than taken.
### Phase 5 Completion

**Completed:** 2026-08-26

**The second proof point holds. B1 is confirmed inside the workspace.** Regeneration in place
against the workspace's own models root moved **zero** bytes, the snapshot recaptured
byte-identically to the tracked file, and the census re-derived exactly — gates 1a, 1b, 2, 3,
4 and 5 all pass on an untouched workspace, in about 14 s wall for the whole run (the spine
suite dominates; generation is ~2 s and capture ~1.7 s). The fixture needed one correction to
get there, recorded as D21 below; the gate was not relaxed.

**Changes made**
- `scripts/integrate.py` — `SequenceState` (the entry digests and backup the gates hand each
  other), `byte_movement_blocker` (restore, record `moved_files.txt`, refuse — one decision,
  so one function), `PRESERVED_SUBTREE`, `gate_regeneration`, `gate_handwritten_preservation`,
  `tracked_snapshot`, `recapture_snapshot`, `rederived_census`, `gate_census_snapshot`. Gate 0
  step 4 is now wired: the before-digest and the backup are taken before the first mutating
  gate.
- `tests/study/test_integrate_refusals.py` — 4 more fixtures (8 total).
- `tests/study/conftest.py` — the workspace no longer copies `__pycache__`.
- `design.md` — **D19, D20, D21** added, and the gate-4 row now names the snapshot-discovery
  could-not-run.

**Test counts.** `tests/study` 309 → **313 passed, 1 skipped**.

**Three decisions, all recorded in `design.md` rather than left in the code**
- **D19 — the snapshot is found, not named** (the owner's ruling, implemented). Exactly one
  `*.snapshot.json` beside the models root; zero or several is `input-invalid` with
  `mode: could_not_run`, the same slug two `--package` values get. Two tests pin it: the
  workspace layout test from Phase 2 and a new two-snapshot refusal.
- **D20 — gates 2 and 3 partition the package.** Gate 2 compares everything outside
  `handwritten/`, gate 3 everything inside it. If gate 2 compared the whole tree it would
  always refuse first and gate 3's `handwritten-lost` could never fire — an unreachable
  refusal path, which is dead code wearing a gate's name. The union is the whole package, so
  nothing is uncovered.
- **D21 — `__pycache__` is excluded from the seam's digest, and this was measured.** With it
  included, gate 2 refused on 60+ `.pyc` files whose bytes moved because copying the tree
  reset their source mtimes. Nothing authors or seals them and the repository ignores them
  everywhere, so `check_package_clean` never sees them either. Excluding them makes the
  seam's digest judge the same file set the repository's own cleanliness gate judges, which
  is what D8 said the two were for. This is the one place the phase's named risk fired, and
  the answer was to fix what the seam was looking at, not what it demanded.

**One bug found and fixed while proving the above.** The seam-internal-error path built its
return with an empty `results` list, so a crash after six passing gates reported all ten as
`not reached`. Both failure paths now live in `run()` where the partial sequence is in scope.
A `seam-internal-error` return now carries every gate that ran.

**Refusal fixtures added.** A doctored package byte refuses gate 2 with
`package-not-integrated`, cites `moved_files.txt`, and **leaves the tree exactly as it found
it** (asserted against digests taken after the doctoring, not against the pristine state — a
restore that reverted the test's own edit would be the seam performing an integration). A
doctored census refuses gate 4 with `census-stale` *after* gates 1a–3 pass. An absent
`--census-file` and an absent `--expected-teax-revision` each land as `could_not_run` with
`input-missing`.

**A consistency rule the plan did not fix, applied throughout.** Three kinds of non-pass, three
slugs: a caller input that was never supplied is `input-missing` (change the request); a
producer that could not judge past gate 0's sweep is `env-missing` (an operational accident,
which is what a goal caller retries); a producer that judged and said no carries its own gate's
condition. `run_pytest_gate` now takes its refusal condition from the call site rather than a
lookup table, so the policy reads where the gate is declared.
### Phase 6 Completion

**Completed:** 2026-08-26

**Gates 1a through 8 all pass on an untouched workspace.** Preflight reports 6/6 and
`verify.py` returns `outcome: pass` against the store this run executed itself, in about
16 s wall for the whole sequence. Only gate 9 remains.

**Changes made**
- `scripts/integrate.py` — `gate_manifest`, `ROUTE_DRIVER_SOURCE`, `resolve_store`,
  `execute_baseline`, `gate_preflight`, `gate_verification`, and `BaselineEvidence`.
  `SequenceState` gained a `baseline` field, filled by gate 7 and read by gate 8.
- `tests/study/test_integrate_refusals.py` — 4 more fixtures (12 total).

**Test counts.** `tests/study` 313 → **317 passed, 1 skipped**.

**The route is invoked, not imported.** `execute_baseline` runs a six-argument driver in a
subprocess under D16's environment. The seam sits above every package, so importing one would
break the invariant every module below it holds; and the subprocess is also what guarantees
the route gets the same `PYTHONPATH` and `STUDY_REQUIRE_TEAX` every other producer gets.

**Gate 7's mode comes from preflight's own vocabulary, not from its exit code.** `preflight
gates` returns 1 for both a failed check and a check that could not run, so the seam reads the
results document: any `did not run` with no `fail` is could-not-run, anything else is refused.
If preflight wrote no document at all — its unreadable-package path returns before the write —
that is could-not-run too. A refusal cites the **whole** results document, never one row: a
test asserts the evidence list is exactly `preflight_results.json` and that all six checks are
reported in it.

**Gate 8's residual is stated at the point of use.** `verify.py` returns 1 for every cause and
writes no summary when it refuses, so past gate 0's `simkit` probe a non-zero exit is read as
`refused`. Its stderr is captured to `verify_stderr.txt` and cited. The shortfall is filed
against `verify.py` in Phase 9.

**`assert_read_set_covered` is named in the return, not omitted quietly.** Gate 6 runs three of
R-B1.6's four assertions and its passing detail says in words that the fourth was **not** run
and is covered by nothing else. A reader of a `CANDIDATE` sees the boundary without reading
the design.

**Store resolution raises rather than guesses.** `execute_baseline` does not return the store
path; the baseline result names it, repo-relative when the output directory is under the repo
root and a bare filename otherwise. Both spellings resolve, and a `store_id` that resolves to
neither raises with the id and both places it looked — two tests, one per spelling, plus one
for the unresolvable case.

**Ordering invariant, made loud.** Gate 8 reads the evidence gate 7 produced. Reaching gate 8
with no baseline means the sequence ran out of order, which is a fault in the seam rather than
a verdict about the package, so it raises and exits 2 instead of refusing.

**Two refusal fixtures added at these gates.** A doctored `indicator_inputs.digest` refuses
gate 6 with `manifest-stale` after gates 1a–5 pass; a drifted `recorded_provenance` passes gate
6 and refuses at gate 7 with `preflight-refused`, which is the split the two producers actually
own — the pin is `manifest.py`'s and the recorded provenance is `check_manifest_currency`'s.
### Phase 7 Completion
### Phase 8 Completion
### Phase 9 Completion
### Phase 10 Completion

---

**Status**: Draft → In Progress → Complete
**Next Step:** `/_my_implement`
