# Implementation Plan: Indicator Tool and Package Manifest

**Status:** In Progress
**Created:** 2026-08-19
**Last Updated:** 2026-08-19
**Branch:** `feat/stellarator-mbse-demo`
**Epic:** RUN-STUDY, Item 3

## Source Documents

- **Spec:** `.project/active/run-study-indicators/spec.md` (accepted)
- **Design:** `.project/active/run-study-indicators/design.md` (accepted, rev 2 — all review fixes folded) ← component details, schemas, invariants, digest recipes, CLI, gate order
- **Item 1 evidence:** `.project/active/run-study-reachability-spike/findings.md` (R1–R12, fixture contract), `trace.py`, `cases.py`, `indicators.json`
- **Design review:** `.project/active/run-study-indicators/design-review.md` (APPROVE-WITH-FIXES; dispositions in design's Next-Stage Handoff)

## The Point

Before any study point runs, the agent needs deterministic, package-derived facts about what in the model can actually push back on each proposed axis. The proof-of-life availability sweep ran to completion, came out entirely feasible with a monotone cost response, and only afterwards was it clear that **no constraint in the model responds to availability at all** — a sensitivity analysis published as a design search. The facts were always in the generated package: it records its own dataflow, its constraint operands, and which operands are bound inputs versus computed values. No step asked for it.

This item builds the durable pair that asks: a generic tool (`scripts/study/indicators.py` + `scripts/study/manifest.py`) that any teax package can use, and a data-only catalog (`exploration/stellarator_e2e/studies/manifest.json`) of the stable facts the stellarator package supplies to it.

Two owner-grade constraints govern everything below. **Interpretive facts never gate a study; mechanical failures fail closed.** A broken analysis and an empty one must never share an exit code — that is exactly what makes `no_constraint_response: true` trustworthy enough to hand a user for a ruling. And **generic and package-specific never share a file**: the tool names no package, the manifest holds no logic.

It ladders up to the run-study capability's one new capability. Item 2's record snapshots `indicators.json` with its digest and schema version; Item 4's `preflight.py`/`verify.py` read the same manifest through the same loader. Both consume this output as a fixed seam, so the schema is versioned from v1 and carries its version inside the output.

## Implementation Strategy

**Phasing Rationale**

Four forces set the order.

1. **The fingerprint comes before the manifest.** The real `manifest.json` cannot be authored until `--print-fingerprint` exists to compute the `indicator_inputs` digest by hand-free means (design D7). So `manifest.py` and the fingerprint mode ship first, as a working CLI that traces nothing.
2. **Known answers come early.** The Item 1 spike already proved the trace is correct on the real package. Getting the six known-answer cases green against the committed package — diffed field by field against the spike's `indicators.json` — is the earliest strong signal that the rewrite preserved the trace core. That lands in Phase 3, right after the manifest exists to feed it.
3. **De-risk the unbacked assertion before the failure suite.** The design says so explicitly (Next-Stage Handoff, "De-risk first"): the synthetic two-pipeline package is the only asserted behavior with no real package data behind it. Package-scoped channels, cross-file collision, one-EntryPoint-per-file, and the `.yml` gate are all asserted against a fixture we invent. Building it *before* the mechanical-failure suite means a wrong assumption about the fixture surfaces on its own, not buried in a suite of nine other negatives.
4. **The `package_copy` factory gates every negative test.** Its two rules (assert-before-mutating, re-pin-unless-testing-the-pin) are what make negative tests trustworthy. It is built alongside the synthetic fixture in Phase 4, before any mutation test in Phase 5.

**Critical Path**

`uv add jsonschema` → `manifest.py` + `--print-fingerprint` → author `manifest.json` → strict reader + trace + report → known answers green → synthetic fixture + `package_copy` → mechanical failures → contract/determinism/warnings polish.

**First Proof Point**

Phase 3: `uv run python -m pytest tests/study/test_known_answers.py` green — all six Item 1 cases (`availability`, `interest_rate`, `R`, `R`+tie, `a`, `beta`) matching the fixture contract field for field, on semantic fingerprint `c9bc…c261`, against the real committed package. Until that passes, nothing else about the tool is worth building on.

**Overall Validation Approach** (design § Validation Approach, made per-phase below)

- **Every phase runs `uv run python -m pytest tests/study` before its checkbox is ticked.** Not just the phase's own file — the whole directory, every phase, no regressions.
- **Every phase runs `uv run ruff check scripts/study tests/study`** (line length 100).
- Four standing checks accumulate across phases and are all green by Phase 7: pytest green (every phase), the grep-clean test (`test_generic.py`), the byte-determinism test including different working directories (`test_output_contract.py`), and JSON Schema validation of real output and the real manifest (`test_output_contract.py`).
- Tests live under `tests/study/`, run by `uv run python -m pytest tests/study`. `scripts/study/` gets no `__init__.py` — implicit namespace packages plus `pythonpath = ["."]` make `from scripts.study import indicators` work.
- **The committed package is never mutated in place.** All mutation goes through the `package_copy` factory into `tmp_path`.

**Test file inventory** (the design's ten files, fixed — do not invent an eleventh; new assertions go into the file that already owns the concern):

| File | First written in |
|---|---|
| `test_output_contract.py` | Phase 1 (recipes + validator), extended Phases 2, 3, 7 |
| `test_known_answers.py` | Phase 3 |
| `test_multipipeline.py` | Phase 4 |
| `test_mechanical_failures.py` | Phase 5 |
| `test_read_set_coverage.py` | Phase 5 |
| `test_valid_empty.py` | Phase 6 |
| `test_warnings.py` | Phase 6 |
| `test_provenance.py` | Phase 6 |
| `test_subset_flag.py` | Phase 6 |
| `test_generic.py` | Phase 7 |

---

## Phase 1: Dependency, module skeleton, `manifest.py`, `--print-fingerprint`

### Goal

Ship `scripts/study/manifest.py` complete — manifest schema validator, both digest recipes, the identity check — plus an `indicators.py` that supports only `--print-fingerprint`. Nothing traces yet. This exists first because the real manifest cannot be authored without it.

### Assumption Under Test

That the `indicator-input-fingerprint/v1` recipe is well defined on the real package as it sits on disk: the three-leg glob (`pipelines/*.yaml`, `inputs/*.json`, `contracts/model_contract.json`) finds a non-empty set on each leg, `pipelines/__init__.py` and `inputs/__init__.py` are ignored without incident (M1), and the canonical text hashes stably across runs and working directories.

### Test Stencil (Write This First)

```python
# tests/study/test_output_contract.py
def test_fingerprint_recipe_is_stable_and_path_sorted(real_package_path):
    a = manifest.indicator_input_fingerprint(real_package_path)
    b = manifest.indicator_input_fingerprint(real_package_path)
    assert a["recipe"] == "indicator-input-fingerprint/v1"
    assert a == b
    paths = [f["path"] for f in a["files"]]
    assert paths == sorted(paths)
    assert not any(p.endswith("__init__.py") for p in paths)   # M1

def test_manifest_validator_raises_on_unknown_key(minimal_manifest_dict):
    minimal_manifest_dict["surprise"] = 1
    with pytest.raises(manifest.ManifestError) as e:
        manifest.validate(minimal_manifest_dict)
    assert "surprise" in str(e.value)
```

### Changes Required

**See `design.md` for:** the manifest schema block-by-block (`design.md#componentscriptsstudymanifestpy--the-package-catalog-seam`), both digest recipes byte for byte, the M1 glob strictness rules, the identity check, path normalization (M4), and the `--print-fingerprint` decision (D7).

- [x] `uv add jsonschema` (already resolved transitively in `uv.lock`; this makes it explicit — nothing new downloads)
- [x] `scripts/study/` created, **no `__init__.py`**
- [x] `tests/study/` created with `conftest.py` (path fixtures only at this phase: repo root, real package path)
- [x] `scripts/study/manifest.py` (NEW): manifest schema validator (hand-rolled, raise on unknown keys anywhere — per-block functions or one table-driven walk, implementer's call per the design's "Open for the plan"); `indicator-input-fingerprint/v1`; `tool-source-digest/v1` (M5); read-set coverage helper (M3, called in Phase 5); identity check; repo-relative POSIX path normalization (M4)
- [x] `scripts/study/indicators.py` (NEW): argparse surface for both invocation forms per `design.md#the-cli`; only `--print-fingerprint` implemented, prints the fingerprint plus every per-file digest and exits 0
- [x] `tests/study/test_output_contract.py` (NEW): the two stencil tests plus a `tool-source-digest/v1` recomputation test over the named file list

### Validation

**Automated:**
- [x] `uv run python -m pytest tests/study` → green
- [x] `uv run ruff check scripts/study tests/study` → clean

**Manual:**
- [x] `uv run python scripts/study/indicators.py --package exploration/stellarator_e2e/pkg/stellarator_tea --print-fingerprint` → prints a digest plus per-file lines; exits 0
- [x] Run the same command from a different working directory → byte-identical output (M4)
- [x] Confirm the file list contains `pipelines/mfe_stellarator.yaml`, the three `inputs/*.json`, and `contracts/model_contract.json` — and **not** either `__init__.py`

**What We Know Works After This Phase:** the fingerprint recipe on the real package, the manifest validator's raise-on-unknown behavior, and the CLI skeleton.

**Commits:** `uv add jsonschema` (pyproject.toml + uv.lock), `scripts/study/manifest.py`, `scripts/study/indicators.py` (fingerprint mode only), `tests/study/conftest.py`, `tests/study/test_output_contract.py`.

---

## Phase 2: Author the stellarator `manifest.json` and the schema files

### Goal

Create `exploration/stellarator_e2e/studies/` deliberately as the manifest's home, author `manifest.json` by hand with the digest from Phase 1's `--print-fingerprint`, and commit the three JSON Schema files that Items 2 and 4 cite.

### Assumption Under Test

That the manifest schema as designed can actually hold the real package's facts without a field the design didn't anticipate — the five objective channels keyed on channels not exit-point filenames (R6), the one declared tie, the pinned baseline, and `verify_stellaris`'s importable `compute()` as a typed oracle object (D6).

### Test Stencil (Write This First)

```python
# tests/study/test_output_contract.py  (extend)
def test_real_manifest_validates(real_manifest_path):
    data = json.loads(real_manifest_path.read_bytes())
    manifest.validate(data)                                    # hand-rolled, strict
    jsonschema.validate(data, load_schema("study_package_manifest.v1"))

def test_real_manifest_pin_matches_live_package(real_package_path, real_manifest_path):
    pinned = json.loads(real_manifest_path.read_bytes())["fingerprints"]["indicator_inputs"]
    assert pinned["digest"] == manifest.indicator_input_fingerprint(real_package_path)["digest"]
```

### Changes Required

**See `design.md` for:** the manifest instance contents (`design.md#explorationstellarator_e2estudiesmanifestjson--the-stellarator-instance`), the schema files and their two load-bearing `description` lines (D9, N1), and the oracle shape (D6).

- [x] `exploration/stellarator_e2e/studies/` created (N5 — deliberately, not as a side effect)
- [x] `exploration/stellarator_e2e/studies/manifest.json` (NEW), authored by hand:
  - `package.name` copied from `contracts/package_contract.json` `package_name`; `package.path` repo-relative
  - `fingerprints.indicator_inputs` — digest and `files` list pasted from `--print-fingerprint`
  - `fingerprints.recorded_provenance` — sealed `executable_fingerprint`, contract `semantic_fingerprint`
  - `objective_catalog` — the five spike channels (`lcoe`, `lcoe_1cfe`, `cas72`, `fuel`, `total_capital`)
  - `ties` — `magnet__R0` rides with `geom__R`, `rb__R`
  - `baseline` — `R = 12.7`, `a = 1.3`, `availability = 0.85`, headline LCOE `275.2642200420774`, five verdicts satisfied
  - `oracle` — `{"kind": "python_callable", …}` for `verify_stellaris.compute()`
- [x] `scripts/study/schemas/indicators.v1.schema.json`, `study_package_manifest.v1.schema.json`, `axis_declaration.v1.schema.json` (NEW) — `additionalProperties: false` throughout, plus the N1 and S1 `description` lines
- [x] `tests/study/conftest.py`: add the `real_manifest_path` fixture and a `load_schema` helper
- [x] `tests/study/test_output_contract.py`: the two stencil tests

### Validation

**Automated:**
- [x] `uv run python -m pytest tests/study` → green
- [x] `uv run ruff check scripts/study tests/study` → clean
- [x] Real manifest validates against `study_package_manifest.v1.schema.json` (standing check #4, first half)

**Manual:**
- [x] Re-run `--print-fingerprint` and eyeball that the pasted digest and `files` list match exactly
- [x] Confirm the manifest holds **no** per-study choices — no axes, no windows, no selected objectives (spec, `[NEED][OWNER]`)

**What We Know Works After This Phase:** the manifest schema holds the real package's facts, and the pin is live.

**Commits:** `exploration/stellarator_e2e/studies/manifest.json`, `scripts/study/schemas/*.json`, test/conftest additions.

---

## Phase 3: Strict reader, trace, report — known answers green

### Goal

Implement the substance of `indicators.py`: the strict `yaml.compose` node reader, the channel graph, the conservative closure, declared-key resolution, the constraint-operand join, and the assembled report document. Get the six Item 1 known-answer cases green against the real package.

### Assumption Under Test

That the Item 1 trace core survives the rewrite intact — the strict reader over composed nodes reproduces the same graph the spike's hand parser built, and the report reproduces all five Appendix A answers on semantic fingerprint `c9bc…c261`.

This is the **first proof point**. If it fails, everything after it is premature.

### Test Stencil (Write This First)

```python
# tests/study/test_known_answers.py
CASES = ["availability", "interest_rate", "R", "R+tie", "a", "beta"]

def test_fixture_binding(real_package_path):
    # Fixtures are bound to the fingerprint they were derived against (spec).
    live = read_semantic_fingerprint(real_package_path)
    assert live == EXPECTED_SEMANTIC_FINGERPRINT, "package regenerated — re-derive, never patch"

@pytest.mark.parametrize("axis", CASES)
def test_known_answer(axis, real_package_path, real_manifest_path, tmp_path):
    doc = run_tool(package=real_package_path, manifest=real_manifest_path,
                   groups=KNOWN_ANSWER_DECLARATION, out=tmp_path / "indicators.json")
    got = group_by_axis(doc, axis)
    expected = json.loads((DATA / f"{axis}.expected.json").read_text())
    assert got == expected     # field for field: operand classes, operator,
                               # bound_vs_bound, both objective lists,
                               # sibling_candidates, trace_size counts
```

### Changes Required

**See `design.md` for:** the strict reader and its accept-set scoping (`design.md#componentscriptsstudyindicatorspy--the-reader-the-trace-the-report`, D2, S6), declared-key resolution order, the constraint-entry shape and `bounds` authority (S2, D10), the report document shape, the not-derivable constant (D5), and the gate order (D8). Implementation gotchas: `design.md#implementation-notes` — `.root` stripping is load-bearing (65 edges), line numbers are 0-based on `start_mark` (report `line + 1`), resolve inputs paths from the EntryPoint block's refs, assemble-then-write.

- [x] `tests/study/data/axes.known_answers.json` (NEW): the axis-declaration file covering all six cases with per-key `fan_out | tie` provenance
- [x] `tests/study/data/{availability,interest_rate,R,R+tie,a,beta}.expected.json` (NEW): expectation files, each recording the semantic fingerprint it was derived against
- [x] `tests/study/test_known_answers.py` (NEW): stencil above
- [x] `scripts/study/indicators.py`: strict node reader (file, line, key path on every raise; `str`/`map` accept-set scoped to the `modules` subtree; null-tagged empty `inputs:`/`outputs:` treated as empty map, not a raise)
- [x] `scripts/study/indicators.py`: reference classification R1–R4 verbatim from the spike; channel graph keyed on fully qualified names (R5); cross-file/same-file duplicate producer is a mechanical failure
- [x] `scripts/study/indicators.py`: conservative closure to fixpoint (R10); EntryPoint/ExitPoint excluded (R11)
- [x] `scripts/study/indicators.py`: contract reader; constraint-operand join through `predicate_ir` (R7, R8); the three identities (D10)
- [x] `scripts/study/indicators.py`: axis-declaration file reader (strict; duplicate axis, duplicate key in group, empty group, unknown key all mechanical failures)
- [x] `scripts/study/indicators.py`: report assembly in memory, single write at the end; `--out` atomic (temp file in the same directory, then rename); human summary to stderr only
- [x] `scripts/study/indicators.py`: `not_derivable` module-level constant, emitted at document and group level

### Validation

**Automated:**
- [x] `uv run python -m pytest tests/study` → green, including all six known-answer cases
- [x] `uv run ruff check scripts/study tests/study` → clean

**Manual:**
- [x] Run the tool against the committed package with all six groups, `--out /tmp/indicators.json`
- [x] **Diff against the spike:** compare each group object to `.project/active/run-study-reachability-spike/indicators.json` for the fields both carry (constraints reached, operand classes, operator, `bound_vs_bound`, objective lists, sibling candidates, trace counts). Any difference is a regression against Item 1's evidence and must be explained before proceeding.
- [x] Confirm `availability` comes back `no_constraint_response: true` — the original finding, now mechanical

**What We Know Works After This Phase:** the trace core is preserved through the rewrite, verified against the real package and the Item 1 evidence.

**Commits:** `scripts/study/indicators.py` (full reader + trace + report), `tests/study/test_known_answers.py`, `tests/study/data/` expectation files and the known-answer declaration.

---

## Phase 4: De-risk — the synthetic two-pipeline fixture and the `package_copy` factory

### Goal

Build the committed synthetic two-pipeline package and the `package_copy` factory, then assert the multi-pipeline stance against them.

### Assumption Under Test

The design names this the one thing to de-risk first: **package-scoped channels across files** is the only asserted behavior with no real package data behind it. Only `mfe_stellarator.yaml` exists in the real package, so a wrong assumption here would go unnoticed for as long as the stellarator is the only consumer. Building the fixture before the mechanical-failure suite means a wrong assumption surfaces on its own rather than buried among nine other negatives.

### Test Stencil (Write This First)

```python
# tests/study/test_multipipeline.py
def test_graph_is_package_scoped_across_files(synthetic_pkg):
    doc = run_tool(package=synthetic_pkg.path, manifest=synthetic_pkg.manifest,
                   groups=synthetic_pkg.axes)
    # a key declared in file A reaches a constraint defined in file B
    assert reached_ids(doc, "cross") == ["c_in_file_b"]

@pytest.mark.parametrize("mutate,expect", [
    (dup_channel_across_files, "produced by more than one module"),
    (second_entrypoint_in_one_file, "exactly one EntryPoint"),
    (add_yml_file_to_pipelines, ".yml"),
])
def test_mechanical_failure(synthetic_pkg, mutate, expect, tmp_path):
    copy = package_copy(synthetic_pkg, tmp_path)   # asserts target exists, then re-pins
    mutate(copy)
    rc, out, err = run_tool_raw(copy)
    assert rc != 0 and expect in err
    assert out == "" and not (copy.path / "indicators.json").exists()
```

### Changes Required

**See `design.md` for:** the multi-pipeline stance (spec's recorded decision, carried into `design.md#the-graph-and-the-closure`), the M1 glob strictness rules, and the `package_copy` factory's two rules (`design.md#validation-approach`).

- [x] `tests/study/data/synthetic_pkg/` (NEW): two pipeline files with a handful of modules each, its own `inputs/*.json`, a minimal `contracts/model_contract.json` with a small constraint catalog, a minimal `contracts/package_contract.json`, its own `manifest.json`, and an axis-declaration file. Module list is the implementer's call ("Open for the plan") — smallest set that exercises a cross-file channel and one constraint per file.
- [x] `tests/study/conftest.py`: the `package_copy` factory — copies the package tree plus the manifest into `tmp_path`, returns both paths, and carries **both rules**: (a) every mutation helper asserts its target substring exists in the copy before replacing (Item 1's probe 4 passed against an uncorrupted file because the target string was wrong), and (b) re-pins the copy's `indicator_inputs` digest by default, with re-pinning switchable off for the fingerprint-mismatch test
- [x] `tests/study/test_multipipeline.py` (NEW): the four cases — package-scoped graph, cross-file duplicate producer, two EntryPoints in one file, a `.yml` file in `pipelines/`

### Validation

**Automated:**
- [x] `uv run python -m pytest tests/study` → green
- [x] `uv run ruff check scripts/study tests/study` → clean

**Manual:**
- [x] Run the tool against the synthetic package by hand and read the output — confirm the cross-file reach is real and not an artifact of how the fixture was written
- [x] Deliberately break one mutation helper's target string and confirm the assert-before-mutating rule fires (then restore) — the factory's own guard, proven once

**What We Know Works After This Phase:** package-scoped channels across files, the three multi-pipeline mechanical failures, and a trustworthy mutation harness for Phase 5.

**Commits:** `tests/study/data/synthetic_pkg/`, `tests/study/conftest.py` (`package_copy` factory), `tests/study/test_multipipeline.py`.

---

## Phase 5: Mechanical failures and read-set coverage

### Goal

Every mechanical failure exits non-zero with a message that locates the fault, and writes nothing. Add the post-parse read-set coverage check (M3, Invariant 10).

### Assumption Under Test

That "assemble, then write" delivers Invariant 1 mechanically — there is no code path that can produce a partial report, so a broken analysis cannot look like an empty one. Every test in this phase asserts stdout is empty *and* no output file exists, not just that the exit code is non-zero.

### Test Stencil (Write This First)

```python
# tests/study/test_mechanical_failures.py
CASES = [
    ("missing_declared_key",     lambda m: m, "no_such_key"),
    ("key_names_produced_channel", ..., "computed quantity"),   # distinct from absent
    ("unclassifiable_key",       ..., "not in contract parameters"),
    ("fingerprint_mismatch",     ..., "indicator-input fingerprint"),  # re-pin OFF
    ("unparseable_reference",    ..., "geom.R.bad.path"),        # quoted verbatim
    ("corrupt_pipeline_line",    ..., "mfe_stellarator.yaml:"),  # file, line, key path
    ("ghost_objective_channel",  ..., "produced by no module"),
    ("wrong_manifest_for_package", ..., "package_name"),
    ("malformed_manifest_baseline", ..., "baseline"),
]

@pytest.mark.parametrize("name,mutate,expect", CASES)
def test_fails_closed(name, mutate, expect, real_package_path, tmp_path):
    copy = package_copy(real_package_path, tmp_path)   # asserts, then re-pins
    mutate(copy)
    rc, out, err = run_tool_raw(copy, out=tmp_path / "indicators.json")
    assert rc != 0
    assert expect in err
    assert out == ""
    assert not (tmp_path / "indicators.json").exists()     # Invariant 1
```

### Changes Required

**See `design.md` for:** declared-key resolution order and its three distinct messages, the gate order (D8) and its test consequence (a corrupt-artifact fixture must re-pin its copy or it fails at the fingerprint gate instead), the read-set coverage check (M3), and Invariant 1. Error message wording is "Open for the plan" — each must locate its fault per the spec's success criterion: the absent key by name, the computed quantity by name **and by what it is**, the reference quoted verbatim, the corrupt construct by file and position, the ghost objective channel by name.

- [ ] `tests/study/test_mechanical_failures.py` (NEW): the nine cases above. The computed-quantity case uses a real channel from the trace (e.g. a `pb__p_net`-style channel) — no synthetic fixture needed.
- [ ] `tests/study/test_read_set_coverage.py` (NEW): an EntryPoint ref rewritten to a file outside the pinned `files` list (re-pinned so the pre-parse gate passes) exits non-zero naming that file; a ref resolving outside the package root exits non-zero; `pipelines/__init__.py` in the real package does **not** fail gate one (M1)
- [ ] `scripts/study/indicators.py`: wire the read-set coverage check as one post-parse assertion (it does not disturb the D8 gate order)
- [ ] `scripts/study/indicators.py`: finalize every mechanical-failure message to locate its fault; ghost-objective check (a catalog channel produced by no module)
- [ ] `tests/study/conftest.py`: mutation helpers for the nine cases, each asserting its target first

### Validation

**Automated:**
- [ ] `uv run python -m pytest tests/study` → green
- [ ] `uv run ruff check scripts/study tests/study` → clean
- [ ] Every failure test asserts non-zero exit **and** empty stdout **and** no output file (Invariant 1)

**Manual:**
- [ ] Trigger the corrupt-pipeline case by hand and read the message — confirm it carries file, line, and key path (the design's probe showed `…/p.yaml:24 (key path modules.…geom.inputs.R)`)
- [ ] Trigger the computed-quantity case and confirm the message says the key names a **computed quantity**, visibly distinct from the absent-key message — an author told "your key is missing" when they picked a model output goes looking in the wrong place

**What We Know Works After This Phase:** the fail-closed half of the owner's rule, end to end, with located messages.

**Commits:** `tests/study/test_mechanical_failures.py`, `tests/study/test_read_set_coverage.py`, conftest mutation helpers, `indicators.py` read-set check and message finalization.

---

## Phase 6: The exit-0 half — valid empty, warnings, provenance, subset

### Goal

The interpretive side: a valid empty result exits 0, advisory scans warn without changing membership, per-key provenance round-trips, and `--group` is visibly a subset.

### Assumption Under Test

That advisory really is advisory — Invariant 3, declared-only membership. A group with warnings and the same group with the manifest tie removed must produce **identical** trace fields.

### Test Stencil (Write This First)

```python
# tests/study/test_warnings.py
def test_advisory_never_changes_the_trace(real_package_path, tmp_path):
    with_tie    = run_tool(real_package_path, manifest=real_manifest)
    copy        = package_copy(real_package_path, tmp_path)  # asserts, re-pins
    remove_tie_from_manifest(copy)
    without_tie = run_tool(copy)
    assert trace_fields(with_tie, "R") == trace_fields(without_tie, "R")   # Invariant 3
    assert warning_kinds(with_tie, "R") == ["tie_candidate"]
    assert siblings(with_tie, "R")                    # M2: named field, not warnings
    assert "sibling" not in json.dumps(warning_kinds(with_tie, "R"))
```

### Changes Required

**See `design.md` for:** the advisory scans and where each lands (M2, S3), the `axis_declaration` block and `subset` (S1, D11, Invariant 11), provenance round-trip (Invariant 8), and `no_constraint_response` (Invariant 4).

- [ ] `tests/study/test_valid_empty.py` (NEW): a group with genuinely no constraint reach exits 0 with `no_constraint_response: true`, `group_valid: true`, and the expected objective lists
- [ ] `tests/study/test_warnings.py` (NEW): the stencil above — suffix siblings in `sibling_candidates` (M2), tie candidates in group `warnings` as `{kind: "tie_candidate", detail}`, neither changing the trace
- [ ] `tests/study/test_provenance.py` (NEW): per-key `fan_out | tie` round-trips declaration → output; a tie key traces identically to a fan-out key
- [ ] `tests/study/test_subset_flag.py` (NEW): a full run emits `subset: false` with `groups` covering `groups_declared`; a `--group` run emits `subset: true` and the narrower list; the `axis_declaration` digest matches the declaration file's bytes
- [ ] `scripts/study/indicators.py`: suffix-sibling scan (R12) and tie-candidate scan, both computed after the trace, never merged into the group
- [ ] `scripts/study/indicators.py`: `axis_declaration` block with `groups_declared` + `subset`; `--group` forces `subset: true`
- [ ] `scripts/study/indicators.py`: document-level `duplicate_key_across_groups` warning; `provenance_drift` warning covering **both** recorded fingerprints (S5) — neither gates

### Validation

**Automated:**
- [ ] `uv run python -m pytest tests/study` → green
- [ ] `uv run ruff check scripts/study tests/study` → clean

**Manual:**
- [ ] Run with `--group R` and confirm `subset: true` plus the narrower `groups` list — a subset cannot be snapshotted into a record and pass for complete
- [ ] Read a report's `not_derivable` block and confirm all four disclosure statements are present, including the positive reading ("a possible path exists", never "responds")

**What We Know Works After This Phase:** interpretive facts never gate, advisory stays advisory, and Item 2 can check axis coverage mechanically.

**Commits:** the four test files, `indicators.py` advisory scans + `axis_declaration` block + document warnings.

---

## Phase 7: Contract, determinism, grep-clean, cleanup

### Goal

Close the four standing checks and the remaining invariants, then clean up the throwaway.

### Assumption Under Test

That the output is a stable seam: byte-identical from different working directories, carrying no absolute path, validating against its committed JSON Schema, with the constraint catalog fully accounted for.

### Test Stencil (Write This First)

```python
# tests/study/test_output_contract.py  (extend)
def test_byte_determinism_across_working_directories(real_package_path, tmp_path):
    a = run_tool_in_cwd(repo_root, real_package_path)
    b = run_tool_in_cwd(tmp_path,  real_package_path)
    assert a == b                                   # Invariant 2 / M4
    assert "/home/" not in a and not re.search(r'"/', a)   # no absolute paths

def test_constraint_completeness(doc):               # Invariant 5 / S4
    for group in doc["groups"]:
        ids = [c["constraint_id"] for c in group["bounds"]]
        assert sorted(ids) == sorted(catalog_ids)
        partition = group["constraints_reachable"] + group["constraints_unreachable"]
        assert sorted(c["constraint_id"] for c in partition) == sorted(catalog_ids)

def test_not_derivable_is_byte_equal(doc):           # Invariant 7 / D5
    doc_block = json.dumps(doc["not_derivable"], sort_keys=True)
    for group in doc["groups"]:
        assert json.dumps(group["not_derivable"], sort_keys=True) == doc_block

# tests/study/test_generic.py                        # Invariant 6
@pytest.mark.parametrize("needle", [PACKAGE_NAME, KEY_PREFIX, "era_adapter"])
def test_tool_modules_are_generic(needle):
    for path in ["scripts/study/indicators.py", "scripts/study/manifest.py"]:
        assert needle not in Path(path).read_text()
```

### Changes Required

**See `design.md` for:** all twelve invariants (`design.md#required-invariants`), D4 determinism, M4 path normalization, M5 tool-source digest, and `design.md#implementation-notes` for the `probe_lineno.py` disposition.

- [ ] `tests/study/test_output_contract.py`: extend with byte-determinism across working directories, JSON Schema validation of real output, `not_derivable` byte-equality, constraint completeness on **both** halves (S4), `tool.source_digest` recipe id + recomputation (M5)
- [ ] `tests/study/test_generic.py` (NEW): grep-clean for the package name, the key prefix, and `era_adapter` in both tool modules
- [ ] `scripts/study/indicators.py` / `manifest.py`: fix anything the above surfaces (sort keys, path normalization, removed timestamps)
- [ ] Sweep all twelve invariants against the test suite; note in Implementation Notes which test asserts each
- [ ] `.project/active/run-study-indicators/probe_lineno.py`: leave in the work-item folder as the throwaway it is, or delete — it never moves to `scripts/`

### Validation

**Automated:**
- [ ] `uv run python -m pytest tests/study` → green, full suite
- [ ] `uv run ruff check scripts/study tests/study` → clean
- [ ] All four standing checks green: pytest, grep-clean, byte-determinism, schema validation of real output and real manifest

**Manual:**
- [ ] Run the tool from two different directories and `diff` the two outputs → no differences
- [ ] Read the committed `indicators.v1.schema.json` and confirm the two load-bearing `description` lines are there: `recorded_executable_fingerprint` is read live from `contracts/package_contract.json` and is **outside** the digested set (N1); `axis_declaration.subset` tells whether `groups` is the whole declaration (S1)
- [ ] Confirm the twelve-invariant sweep leaves none unasserted

**What We Know Works After This Phase:** the output is a citable, versioned, deterministic seam that Items 2 and 4 can build on.

**Commits:** `tests/study/test_generic.py`, `test_output_contract.py` extensions, any tool fixes, probe disposition.

---

## Environment Setup

**See CLAUDE.md for full environment rules.** Everything runs through `uv` — `uv run python -m pytest tests/study`, `uv run ruff check`, `uv add jsonschema`. Never bare `python`/`pip`.

## Risk Management

**See `design.md#potential-risks` for the full analysis.**

**Phase-Specific Mitigations:**

- **Phase 1 (fingerprint churn, B2):** report per-file digests so a mismatch names the file in one look; `--print-fingerprint` makes re-pinning a one-line edit.
- **Phase 3 (fixture binding):** the expectation files record the fingerprint they were derived against and `test_fixture_binding` asserts the live one matches — so a regenerated package fails the binding assert **first**, with a message that says re-derive. Fixtures are never patched to match.
- **Phase 3 (trace regression):** the manual diff against the spike's `indicators.json` is the guard. Any field difference is explained before the phase closes.
- **Phase 4 (fixture invents its own truth):** the synthetic package asserts behavior no real data backs. Mitigation is the manual read-through plus deliberately breaking one mutation target to prove the assert-before-mutating rule fires.
- **Phase 5 (gate order surprise, D8):** every mutation test re-pins its copy by default, or it fails at the fingerprint gate instead of the failure it means to test. The one exception is the fingerprint-mismatch test, which is the same helper with re-pinning off.
- **Phase 7 (strict reader brittleness):** accepted and intended. A regenerated package with a new construct fails closed and needs a code change; the spec forbids weakening it.

## Implementation Notes

[TO BE FILLED DURING IMPLEMENTATION]

### Phase 1 Completion
**Completed:** 2026-08-19
**Actual Changes:**
- `pyproject.toml` + `uv.lock`: `jsonschema>=4.26.0` added as an explicit dependency (two lock lines, nothing downloaded).
- `scripts/study/manifest.py` (NEW, no `__init__.py` in the package dir): strict hand-rolled manifest validator (per-block functions), both digest recipes, the read-set coverage helper (`assert_read_set_covered`, wired in Phase 5), the identity check, the pin gate (`assert_pin_matches`), and path normalization.
- `scripts/study/indicators.py` (NEW): full argparse surface for both invocation forms; `--print-fingerprint` implemented.
- `tests/study/conftest.py` (NEW): repo-root, real-package, real-manifest, `load_schema`, and `minimal_manifest_dict` fixtures.
- `tests/study/test_output_contract.py` (NEW): 12 tests — recipe stability and path sorting, the three-leg read set, working-directory independence via the CLI, and seven validator cases (unknown key, four located missing keys, malformed baseline, duplicate objective name, unknown oracle kind).

**Issues:**
- Running `indicators.py` as a script puts `scripts/study/` on `sys.path`, not the repo root, so `from scripts.study import manifest` fails. Added a three-line `sys.path` bootstrap guarded on `__package__ in (None, "")`, so both `uv run python scripts/study/indicators.py` and the pytest import path work.

**Deviations:**
- **Fingerprint paths are package-relative, not repo-relative.** The design's recipe prose says "sorted by repo-relative POSIX path" but its own manifest schema example pins `files: ["pipelines/mfe_stellarator.yaml", ...]` — package-relative. Resolved in favour of the schema example, because the pinned `files` list is what Invariant 10 compares resolved reads against, and a package-relative pin stays valid if the package moves inside the repo. Sort determinism (the point of the prose) is unaffected. Every *other* path in the report stays repo-relative POSIX per M4.
- **The `tool-source-digest/v1` recomputation test moved to Phase 2.** The recipe's file list includes the three `scripts/study/schemas/*.json` files, which Phase 2 authors; the test cannot pass before they exist. `tool_source_digest()` itself shipped in this phase.

### Phase 2 Completion
**Completed:** 2026-08-19
**Actual Changes:**
- `exploration/stellarator_e2e/studies/` created deliberately as the manifest's home (N5).
- `exploration/stellarator_e2e/studies/manifest.json` (NEW): package identity (`stellarator_tea`), the live indicator-input pin `612edfc9…bbb9` over five files, recorded provenance (sealed `executable_fingerprint` `ad912041…fa2d`, contract `semantic_fingerprint` `c9bc1640…c261`), the five spike objective channels, the one declared tie, the pinned baseline (nine qualified keys read from the live inputs; headline LCOE `275.2642200420774`; five verdicts satisfied), and the oracle entry point.
- `scripts/study/schemas/{study_package_manifest,axis_declaration,indicators}.v1.schema.json` (NEW): `additionalProperties: false` throughout, carrying the N1 and S1 descriptions plus the soundness note on `no_constraint_response` and the `bounds`-is-authoritative note.
- `tests/study/test_output_contract.py`: ten more tests — real manifest validates against both the hand-rolled validator and its JSON Schema, the pin matches the live package file-for-file, package identity, no per-study choices in the manifest, manifest digest is over its own bytes, `tool-source-digest/v1` recomputation (M5), the two load-bearing schema descriptions, and a walk asserting every schema object is closed.

**Issues:**
- The oracle's importable name is bare `verify_stellaris`, which only resolves with `exploration/stellarator_e2e` on `sys.path` (that is how `run_design_search.py` imports it). Recording only `module` + `callable` would force Item 4's `verify.py` to hard-code a package-specific directory — the exact thing Design Principle 4 forbids.

**Deviations:**
- **The `python_callable` oracle carries a required `sys_path` field** (repo-relative POSIX directory), beyond the design's rendered `{kind, module, callable, note}`. It keeps the package-specific path in the data where it belongs. This is additive within D6's typed-object shape, not a change of kind.
- The manifest's `baseline.point` records **nine qualified keys**, not three axis names: the two `R` keys plus the tie `magnet__R0`, the two `a` keys, and the four `availability` keys, each with the value read from the live inputs. The design's `{"<key>": 12.7}` rendering asks for keys; three bare axis names would not be a point a gate can set.

### Phase 3 Completion
**Completed:** 2026-08-19
**Actual Changes:**
- `scripts/study/indicators.py`: the substance. Strict `yaml.compose` node reader (`read_pipeline`) with file, line, and key path on every raise, the `str`/`map` accept-set scoped to the `modules` subtree, `metadata` shape-checked only, and null-tagged empty `inputs:`/`outputs:` read as empty maps. Reference classification R1–R4 (`classify_ref`); package-scoped channel graph across every pipeline file (`build_graph`) with duplicate producer and duplicate module name as mechanical failures; conservative closure to fixpoint (`reachable_channels`, R10) with EntryPoint/ExitPoint excluded (R11); model contract reader and the `predicate_ir` operand join (R7, R8) carrying all three constraint identities (D10); strict axis-declaration reader; declared-key resolution in the three-message order; report assembly in memory with a single write, `--out` atomic via temp-file rename, human summary to stderr only; `NOT_DERIVABLE` emitted at document and group level.
- `tests/study/data/axes.known_answers.json` (NEW): the six cases with per-key `fan_out | tie` provenance.
- `tests/study/data/{availability,interest_rate,R,R+tie,a,beta}.expected.json` (NEW): frozen group objects, each recording the semantic fingerprint it was derived against and a note saying to re-derive rather than patch.
- `tests/study/test_known_answers.py` (NEW): 24 tests — fixture binding, per-axis expectation-file comparison, a `FIXTURE_CONTRACT` table restated from Item 1's findings so the frozen files are not the only guard, plus the availability, beta bound-vs-bound, `net_positive`-through-`.root`, tie-changes-nothing, and three-identity cases.
- `tests/study/conftest.py`: `run_tool` / `run_tool_raw` subprocess helpers (a subprocess is the honest check for Invariant 1).

**Issues:**
- None. The trace core survived the rewrite unchanged.

**Deviations:**
- None in substance. Two items the plan schedules for Phase 6 shipped here because the report cannot validate against its own schema without them: the `axis_declaration` block (with `groups_declared` and `subset`) and the two advisory scans. Their tests still land in Phase 6.

**Verification against the Item 1 evidence:** a field-by-field programmatic diff of all six groups against `.project/active/run-study-reachability-spike/indicators.json` — declared keys, entry types, `no_constraint_response`, modules fired, channels tainted, both objective lists, the reachable-constraint set, and per-constraint `constraint_id` / operator / operand classes / `bound_vs_bound` / operand detail — reported **no mismatches**. `availability` comes back `no_constraint_response: true`.

### Phase 4 Completion
**Completed:** 2026-08-19
**Actual Changes:**
- `tests/study/data/synthetic_pkg/` (NEW): package root at `pkg/` (two pipelines, two inputs files, a minimal model contract with two constraints, a minimal package contract) with `manifest.json` and `axes.json` beside it. Pipeline A produces `syn__a__y`; pipeline B consumes it and produces `syn__b__w`; one constraint lives in each file, and B's compares a computed channel against a `predicate_ir` literal.
- `tests/study/conftest.py`: the `PackageCopy` dataclass and the `package_copy` factory, plus `synthetic_copy` and `real_copy` fixtures. `edit` asserts its target substring before replacing; `run` re-pins the copy by default and `run(repin=False)` is the fingerprint-mismatch form.
- `tests/study/test_multipipeline.py` (NEW): 10 tests — the package-scoped cross-file reach, that the reach discriminates (B's key never reaches A), the literal operand, three mechanical failures (cross-file duplicate producer, two EntryPoints in one file, a `.yml` in `pipelines/`), a duplicate module name across files, the named-both-producers message, the factory's own assert-before-mutating guard, and a check that the committed synthetic pin is live.

**Issues:**
- The stray-`.yml` case cannot re-pin: `indicator_input_read_set` raises on the stray file, so the re-pin helper would raise the same error the tool is supposed to raise. That case runs with `repin=False`, which is sound because the mutation changes no digested byte and the glob check fires before any digest comparison. The reason is a comment on the case.

**Deviations:**
- The synthetic package root sits at `data/synthetic_pkg/pkg/` with `manifest.json` and `axes.json` as siblings rather than inside it. The design left the location open; a manifest inside the package root would read as a package artifact, which it is not.

**Manual verification:** ran the tool against the synthetic package by hand and read the output. `cross` (a key entering through pipeline A) reaches both constraints and both objectives via `syn__a__x` → `syn__a_calc` → `syn__a__y` → `syn__b_calc` → `syn__b__w` → `b_ok`; `b_only` reaches only `b_ok` and only the `w` objective, so the cross-file reach is a real edge and not an artifact of everything being reachable. The assert-before-mutating rule is proven by a test rather than by a one-off manual break.

### Phase 5 Completion

### Phase 6 Completion

### Phase 7 Completion

---

**Status**: Draft → In Progress → Complete
**Next Step:** `/_my_implement`
