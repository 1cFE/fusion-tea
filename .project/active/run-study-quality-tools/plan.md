# Implementation Plan: Quality Tools and Era Adapter Promotion (RUN-STUDY Item 4)

**Status:** Draft
**Created:** 2026-08-20
**Last Updated:** 2026-08-20
**Branch:** `feat/stellarator-mbse-demo`
**Epic:** RUN-STUDY, Item 4

## Source Documents

- **Spec:** `.project/active/run-study-quality-tools/spec.md` (Accepted)
- **Design:** `.project/active/run-study-quality-tools/design.md` rev 2 (Accepted; review L1–L6, S1–S5, N1–N3 folded) ← component details, schemas, decisions D1–D13, Invariants 1–11 live there and are **not** restated here
- **Design review:** `.project/active/run-study-quality-tools/design-review.md` (APPROVE-WITH-FIXES; disposition in `design.md#next-stage-handoff`)
- **Probe:** `.project/active/run-study-quality-tools/probe_effective_fingerprint.py` — already proved the identity/lineage mechanics (`design.md#appendix-design-probe-results`). This plan **turns the probe into committed tests, it does not re-derive it.**

---

## The Point

One good study exists. Every mechanical gate that made it trustworthy — baseline reproduction, package cleanliness, oracle parity at rel < 1e-9, re-derived verdicts, declared-key validation, dead-filler assertions — is welded into one 450-line package-specific file, `exploration/stellarator_e2e/study/run_design_search.py`. The next study on this package, or the first study on any other package, starts from zero.

Two of those welds are not merely unshared; they are wrong.

- **The loader returns a fingerprint it did not earn.** It accepts a package whose two glue-edited files differ from their sealed hashes, then hands teax the *sealed* fingerprint as the identity of what ran (`run_design_search.py:184`). teax's lineage discipline rests on that identity — a store refuses to resume under a different executable. So today a glue edit changes what runs and changes nothing about what teax thinks ran.
- **A sealed-hash preflight gate cannot be honest while that is true.** Of 139 sealed artifacts, exactly two mismatch on disk. A "manifest fingerprint matches package" gate could only pass by looking away.

This item owes the capability three things: generic gates that name no package, a package-local adapter that tells the truth about what it bypassed and states the condition under which it is deleted whole, and proof that the promoted route still produces exactly what the proof-of-life produced — both CSVs, byte-for-byte.

That is what makes this a *capability* rather than one lucky study: after this item, the gates are reusable, the identity is earned, and the era workarounds are quarantined behind a stated expiry.

---

## Implementation Strategy

### Phasing rationale

The design fixed the de-risk order (`design.md#next-stage-handoff`), and this plan follows it literally:

1. **Operand bindings first** (Phase 1). L1 is the one belief that broke under review: a generic tool *cannot* resolve predicate operands by name — one of five constraints resolves to nothing, and three others are guesses among three composition rules. B4 now rests on the package *publishing* bindings. If publication turns out to be impossible for some constraint, `verify.py`'s whole verdict-re-derivation design changes, so this is proved before `verify.py` exists.
2. **Promotion equivalence's 19-point sweep second** (Phase 4). It is the smallest complete exercise of the promoted route — adapter, shim, identity document, definition, export. If those 19 rows do not reproduce byte-for-byte, every later gate is being built on a route that is not the proof-of-life's.
3. **The read-only open of the committed store third** — pulled *earlier*, into Phase 0, because it costs minutes and removes the last unprobed assumption behind D7 (store sampling). Doing it in Phase 0 means Phase 6's `verify.py` is never speculative.

Everything else is ordered by dependency: the shim before the adapter (D13 — `g3` goes through the shim), `identity.py` before the adapter (the adapter computes the fingerprint through the recipe), the route before `preflight.py` (D1 — preflight consumes `baseline_result.json`, which only an executed point produces), and the manifest oracle-block edit before `verify.py` runs against the real package.

### Critical path

```
probe + fixtures → oracle_entry.py (bindings proved) → identity.py + common.py
  → era_adapter.py → route + promotion equivalence (19-pt) → preflight.py
  → manifest oracle values → verify.py → annex + full-grid + end-to-end
```

### First proof point

`tests/study/test_operand_bindings.py` green: all five catalog constraints resolve every `feature_ref` operand through `oracle_entry.operand_bindings()`, and every resolved key exists in the package's inputs or is returned by `evaluate()`. That is Phase 1, and it is the earliest thing that can invalidate the design.

### Standing rules for every phase

- **Test-first.** Each phase writes its test file(s) before the module it exercises.
- **Suite gate.** `uv run python -m pytest tests/study -q` is green — the **whole** study suite, so Item 3's delivered 134 tests stay green — before any phase box is ticked.
- **Never run the full repo suite.** `tests/scoring_v2/test_score_explorer_build.py` regenerates live data files as a side effect. Every pytest invocation in this item is scoped to `tests/study` (and `-k`/`-m` within it).
- **Package read-only.** The committed package under `exploration/stellarator_e2e/pkg/` and the proof-of-life directory `exploration/stellarator_e2e/study/` are read, never written. Mutation tests go through Item 3's `package_copy` factory (extended, not forked — `design.md#implementation-notes`).
- **Lint.** `uv run ruff check scripts/study exploration/stellarator_e2e/studies tests/study` clean before commit (line length 100).
- **Commit per phase**, message prefixed `RUN-STUDY Item 4 Phase N:`.

### Environment and the era dependency

The era teax worktree `/home/reid/1cfe/teax-v1-era` at `fa0e06a` (`packages/teax-simkit` on `sys.path`) is a **read-only external dependency**. It is not in this repo and is not installed by `uv`.

The design fixes the production rule: the era path is the caller's, never the tool's (`design.md#implementation-notes`); `verify.py` imports `simkit` from the ambient environment and records where it came from; the **adapter** asserts the pin and fails closed. The design does **not** say what tests do when the worktree is absent. **Decision for this plan, recorded here because the design left it open:**

- `tests/study/conftest.py` gains an `era_simkit_path` fixture. It resolves `$TEAX_V1_ERA` if set, else `/home/reid/1cfe/teax-v1-era`, and requires `packages/teax-simkit` to exist and the worktree HEAD to be `fa0e06a`.
- **Absent or wrong commit → `pytest.skip` with a loud reason** naming the resolved path, the expected commit, what was found, and the env var that overrides it. A skip, not a failure: the dependency is external and legitimately unavailable on another machine, and turning that into a red suite would train people to ignore red.
- **Silence is the real risk, so the skip is made impossible to miss two ways.** (a) `STUDY_REQUIRE_ERA=1` in the environment turns every such skip into a hard failure — this item's own validation runs set it, and it is the flag CI would use. (b) One test that *never* skips, `test_era_pin_is_declared_consistently`, asserts the pin string agrees across `conftest.py`, `era_adapter.py`, and `ANNEX.md § Era pin`, so a drifting pin fails even with no worktree present.
- Era-dependent files: `test_accept_set.py`, `test_lineage_refusal.py`, `test_glue_mapping_agreement.py`, `test_committed_store.py`, `test_verify.py`, `test_promotion_equivalence.py`. Phase 8 records the era-dependent test count in the plan's Implementation Notes so a future silent skip is visible as a number that changed.

Verified 2026-08-20: the worktree and `packages/teax-simkit` are present.

### Two coordination asks are already discharged on disk

The design's Coordination section owes Item 3 three things. Two are already satisfied by Item 3 as delivered, verified 2026-08-20 — no action, and **no edit to Item 3's files** is needed for them:

- Ask 2 (`test_generic.py` file-set assertions): the delivered file already uses subset assertions (`{...} <= set(found)`) and names Item 4's four modules in its docstring (`tests/study/test_generic.py:47-63`).
- Ask 3 (`files` on `manifest.tool_source_digest()`): delivered as a list of `{path, sha256}` (`scripts/study/manifest.py:157-161`). `common.py`'s per-tool digest **mirrors that shape**, so one recipe id reads the same across all three tools.

Ask 1 — the stellarator manifest's oracle-block **values** — is live and is Phase 6.

---

## Phase 0: Test scaffolding, probe re-run, and the store assumption

### Goal

Put the era locator, the marker registration, and the extended `package_copy` in place, re-run the item-start probe against the package as it stands today, and close D7's last unprobed assumption with a read-only open of the committed store. Nothing in `scripts/` changes.

### Assumption under test

That the adapter branch is still live (the package may have been regenerated since the design), and that `StudyQuery` over the committed proof-of-life store really does expose `inputs`, `verdicts`, and `catalog` in the qualified vocabulary D7 assumes.

### Test stencil (write this first)

```python
# tests/study/test_committed_store.py  — S4, read-only
def test_the_committed_store_speaks_the_generic_vocabulary(era_simkit_path, repo_root):
    store = repo_root / "exploration/stellarator_e2e/study/_work/availability_sweep.db"
    cases = list(open_query(store).cases())          # read-only open, never written
    done = [c for c in cases if c.status == "completed"]
    assert done, "no completed cases in the committed store"
    c = done[0]
    assert any(k.count("__") >= 2 for k in c.inputs)       # qualified entry keys
    assert any(k.count("__") >= 2 for k in c.outputs)      # qualified channels
    assert c.verdicts and all(isinstance(v, str) for v in c.verdicts.values())
    assert c.executable_fingerprint
```

### Changes required

**See `design.md` for:** the store's vocabulary (`design.md#research-findings`), D7, the `package_copy` rules (`design.md#implementation-notes`).

- [ ] `tests/study/conftest.py`: add `era_simkit_path` fixture per the era policy above (skip-with-loud-reason; `STUDY_REQUIRE_ERA=1` promotes to failure), and extend the `package_copy` factory with the third convenience the design names — mutate a glue file *and* optionally re-emit the identity document.
- [ ] `pyproject.toml` `[tool.pytest.ini_options]`: register `markers = ["slow: long-running equivalence runs (948-point grid)"]`. Needed by D11's `-m slow` gate; `pythonpath = ["."]` is already correct.
- [ ] `tests/study/test_committed_store.py` (NEW) — the stencil above. Read-only; assert the store file is unmodified afterwards.
- [ ] `tests/study/test_era_pin.py` (NEW) — `test_era_pin_is_declared_consistently`, never skips. Asserts the conftest constant only for now; the adapter and annex assertions are enabled in Phases 3 and 8 (marked `xfail(strict=False)` until then is **not** acceptable — instead the test parametrizes over files that exist, so it grows as they land).
- [ ] Re-run `.project/active/run-study-quality-tools/probe_effective_fingerprint.py` and paste its `[P3]` line into this plan's Implementation Notes.

### Validation

**Automated:**
- [ ] `uv run python -m pytest tests/study -q` → green (134 + new)
- [ ] `uv run python -m pytest tests/study -q` with `TEAX_V1_ERA=/nonexistent` → the store test **skips with a message naming the path and commit**, suite still green
- [ ] same with `STUDY_REQUIRE_ERA=1 TEAX_V1_ERA=/nonexistent` → that test **fails** loudly

**Manual:**
- [ ] Probe `[P3]` reports `artifacts=139 differing=2` on exactly `inputs/system_design.json` and `pipelines/mfe_stellarator.yaml`.
  **If it reports 0 differing**, the package was regenerated and the stock loader may now accept it: **STOP and surface it** — spec §"Item-start probe" says the adapter is then *absent*, not retained, and Phases 3, 4, and the promotion-equivalence gate retire with it. Do not proceed to Phase 1 under a stale premise.
- [ ] `git status --porcelain exploration/stellarator_e2e` → empty.

**What we know works after this phase:** the adapter branch is live; the store exposes what D7 needs; era-absent behaviour is defined, loud, and testable.

**Commits:** `conftest.py` + `pyproject.toml` marker + `test_committed_store.py` + `test_era_pin.py`, and the probe result recorded in this plan.

---

## Phase 1 (DE-RISK 1): The package-owned oracle shim and the published operand bindings

### Goal

Author `exploration/stellarator_e2e/studies/oracle_entry.py` with its three published surfaces (`design.md#exploration-stellarator_e2e-studies-oracle_entry-py`), and prove the operand-binding table against all five real catalog constraints **before anything consumes it**.

### Assumption under test

**B4 as restated after review L1:** the package can publish, for every constraint in its catalog, a binding from each predicate operand to a qualified input key or channel. The review killed the earlier form of this bet — that a generic tool could resolve operands by name. If publication fails for any constraint, `verify.py` cannot emit `verdicts_rederived: true` and the design must change before a line of it is written.

### Test stencil (write this first)

```python
# tests/study/test_operand_bindings.py — the L1 de-risk
def test_every_constraint_operand_resolves(real_package_path, oracle_entry):
    catalog = json.loads((real_package_path / "contracts/model_contract.json").read_text())
    entries = catalog["constraint_catalog"]["concrete_entries"]
    bindings = oracle_entry.operand_bindings()
    channels = oracle_entry.evaluate(BASELINE_POINT)
    inputs = load_package_inputs(real_package_path)
    for entry in entries:                                   # all five, no sampling
        ir = json.loads(entry["predicate_ir"])              # IR is a JSON *string*
        for operand in feature_refs(ir):
            b = bindings[entry["constraint_id"]][operand["source_name"]]
            assert b["key"] in (inputs if b["kind"] == "input" else channels), (
                f"{entry['constraint_id']}/{operand['source_name']} -> {b['key']}")
```

Plus the three fail-closed cases: a removed binding, an unknown key, and an ambiguous entry each raise naming the constraint **and** the operand.

### Changes required

**See `design.md` for:** D5 (shim location and ownership), D12 (the binding contract and its exact signature), D13 (`glue_values`), Invariant 9, the operand-resolution finding in `design.md#research-findings`.

- [ ] `tests/study/test_operand_bindings.py` (NEW — first)
- [ ] `exploration/stellarator_e2e/studies/oracle_entry.py` (NEW): `evaluate()`, `operand_bindings()`, `glue_values()`; owns the entry-key → oracle-input map, the oracle-output → qualified-channel map, the `IN` save/restore (`run_design_search.py:144-152`), and the `_profile_integral` memoization. It puts `exploration/stellarator_e2e` on `sys.path` itself. `verify_stellaris.py` is **not** touched.
- [ ] Record the binding for `net_positive.net_electric` explicitly — `…__pb__p_net`, `kind: "channel"` — since it is the one that resolves to nothing by name and is the reason D12 exists.

### Validation

**Automated:**
- [ ] `uv run python -m pytest tests/study/test_operand_bindings.py -q` → green, 5/5 constraints
- [ ] `uv run python -m pytest tests/study -q` → green

**Manual:**
- [ ] `uv run python -c "from … import oracle_entry; print(oracle_entry.evaluate(BASELINE))"` reproduces LCOE `275.2642200420774` within rel < 1e-9 (the probe's value).

**What we know works after this phase:** B4 holds on the real package; verdict re-derivation is buildable; the oracle seam exists with `verify_stellaris.py` untouched.

**Commits:** `oracle_entry.py` + `test_operand_bindings.py`.

---

## Phase 2: `identity.py` and `common.py` — the generic seam

### Goal

The identity document, the `effective-executable-fingerprint/v1` recipe, the sealed emitter, the recompute-and-compare gate, and the shared internals both tools need.

### Assumption under test

That the recipe's canonical text is pinnable byte-for-byte and that the sealed case reduces to the sealed fingerprint rather than inventing a second value — the one honest difference the probe did **not** confirm (N1: the probe emitted a single `adapter <digest>` line, the design emits one `adapter <path> <sha256>` line per declared source).

### Test stencil (write this first)

```python
# tests/study/test_identity.py
def test_the_recipe_canonical_text_is_exactly_this(tmp_path):
    doc = identity.build(sealed="ab"*32, modified=[("inputs/x.json", "11"*32)],
                         adapter_sources=[("a/era_adapter.py", "22"*32)])
    assert identity.canonical_text(doc) == (
        "effective-executable-fingerprint/v1\n"
        "sealed " + "ab"*32 + "\n"
        "modified inputs/x.json " + "11"*32 + "\n"
        "adapter a/era_adapter.py " + "22"*32 + "\n")
    assert doc["identity"]["digest"] == sha256(canonical_text.encode()).hexdigest()

def test_the_sealed_kind_reduces_to_the_sealed_fingerprint(): ...
def test_adapter_source_digest_is_over_the_sorted_adapter_lines(): ...   # S1
def test_recompute_mismatch_and_missing_declared_file_both_fail(): ...
```

### Changes required

**See `design.md` for:** D4, D2, D3, S1 (`design.md#scripts-study-identity-py-the-identity-seam`), D10 (`common.py`'s four jobs), the L5c recipe-id note in `design.md#potential-risks`.

- [ ] `tests/study/test_identity.py` (NEW — first)
- [ ] `scripts/study/schemas/package_identity.v1.schema.json` (NEW, additive; Item 3's three schema files untouched)
- [ ] `scripts/study/identity.py` (NEW)
- [ ] `scripts/study/common.py` (NEW): git-clean gate, atomic deterministic document write, per-tool source digest under `tool-source-digest/v1` **carrying `files[]` in the delivered `{path, sha256}` shape**, exit/error convention. No teax import.
- [ ] `tests/study/test_generic.py`: extend `TOOL_MODULES` with `identity.py` and `common.py` (Invariant 1). Delivered subset assertions need no change.

### Validation

**Automated:**
- [ ] `uv run python -m pytest tests/study -q` → green
- [ ] grep-clean tests pass for the two new modules
- [ ] `uv run ruff check scripts/study` clean

**Manual:**
- [ ] Build the effective identity for the real package by hand and confirm the digest is stable across two invocations from different working directories (determinism).

**What we know works after this phase:** the identity seam exists as data, with a pinned canonical text, and both tools can recompute rather than trust.

**Commits:** `identity.py`, `common.py`, the identity schema, `test_identity.py`, the `test_generic.py` extension.

---

## Phase 3: `era_adapter.py` — the temporary adapter

### Goal

The single home for the loader exception, the glue rungs g1–g3, the self-checks (the dead-filler assertion above all), the era-pin prerequisite, the effective-fingerprint computation, and the identity-document emission.

### Assumption under test

**B1 and B2, promoted from probe to committed test:** the era stack accepts a computed fingerprint at `loader.load()` and carries it into evidence provenance, and a store bound to one effective fingerprint refuses another. Also Invariant 3 — the accept-set is *exactly* the two documented files, not a blanket seal bypass.

### Test stencil (write this first)

```python
# tests/study/test_accept_set.py
def test_a_third_modified_sealed_artifact_is_refused(package_copy, era_simkit_path):
    pkg = package_copy()                      # asserts before mutating, per Item 3's rules
    touch_sealed(pkg, "contracts/model_contract.json")   # a THIRD file
    with pytest.raises(SealVerificationError):
        era_adapter.loader(pkg).load()

# tests/study/test_lineage_refusal.py  — three declared sources, three refusals
@pytest.mark.parametrize("source", ["glue_file", "era_adapter.py", "oracle_entry.py"])
def test_touching_a_declared_source_retires_the_store(source, package_copy, tmp_path):
    store = run_two_points(package_copy(), tmp_path)      # do NOT db.unlink()
    mutate(source)
    with pytest.raises(IncompatibleStore):
        StudyStore.create_or_open(store, compatibility_from(recomputed_identity()))
```

### Changes required

**See `design.md` for:** `design.md#exploration-stellarator_e2e-studies-era_adapter-py`, Invariants 3, 4, 8, D13, and the "do not `db.unlink()`" note in `design.md#implementation-notes`.

- [ ] `tests/study/test_accept_set.py`, `tests/study/test_lineage_refusal.py`, `tests/study/test_glue_mapping_agreement.py` (NEW — first)
- [ ] `exploration/stellarator_e2e/studies/era_adapter.py` (NEW): first line names it temporary; declared source set is `era_adapter.py`, `oracle_entry.py`, `verify_stellaris.py`; `g3` values come from `oracle_entry.glue_values()` (D13); era pin **asserted** against the worktree at `fa0e06a` and failing closed; emits `package_identity.json` with `identity` + `glue_ledger` (D2).
- [ ] Deletion condition written verbatim in the adapter's docstring (the same words go into `ANNEX.md § Loader exception and glue` in Phase 8).
- [ ] `tests/study/test_era_pin.py`: enable the `era_adapter.py` half of the pin-consistency assertion.

### Validation

**Automated:**
- [ ] `uv run python -m pytest tests/study -q` → green; era-dependent tests actually **ran** (`-rs` shows no unexpected skips with `STUDY_REQUIRE_ERA=1`)

**Manual:**
- [ ] Load the real package through the adapter and diff the emitted `package_identity.json` against the probe's `[P1] effective` line — the digest **will differ** (N1: the recipe's canonical text changed), and that is expected. What must match is the sealed value and the two allowed-modified paths.
- [ ] Break the era pin deliberately (point `TEAX_V1_ERA` at a different commit) → the adapter fails closed with a message naming the expected and found commits.

**What we know works after this phase:** the identity is earned, drift in any of the three declared sources retires stores, and the exception did not widen.

**Commits:** `era_adapter.py` + its three test files + the pin-test extension.

---

## Phase 4 (DE-RISK 2): The promoted route and promotion equivalence

### Goal

The study-local direct-API definition (`StudyRunner` + `PreparedListStrategy`) that both studies run through, its `baseline_result.json` emission, and `promotion_equivalence.py` — proved first on the 19-point availability sweep, then on the 948-point grid.

### Assumption under test

That the promoted structure — adapter, shim, identity document, definition, export — reproduces the proof-of-life **byte-for-byte**. If the 19 rows differ, every later gate is being built on a route that is not the one that produced the committed evidence.

### Test stencil (write this first)

```python
# tests/study/test_promotion_equivalence.py
def test_the_availability_sweep_reproduces_byte_for_byte(tmp_path, era_simkit_path):
    out = promotion_equivalence.run_availability_sweep(out_dir=tmp_path)   # 19 points
    expected = REPO_ROOT / "exploration/stellarator_e2e/study/availability_sweep.csv"
    assert out.read_bytes() == expected.read_bytes(), first_differing_line(out, expected)

@pytest.mark.slow
def test_the_design_search_grid_reproduces_byte_for_byte(tmp_path, era_simkit_path):
    out = promotion_equivalence.run_design_search(out_dir=tmp_path)        # 948 points
    ...
```

### Changes required

**See `design.md` for:** D11, D1 (the baseline result document and its schema), `design.md#exploration-stellarator_e2e-studies-promotion_equivalence-py`, and the byte-for-byte caution in `design.md#implementation-notes` (proposals must be built from the same rungs in the same order).

- [ ] `tests/study/test_promotion_equivalence.py` (NEW — first)
- [ ] `scripts/study/schemas/baseline_result.v1.schema.json` (NEW, additive)
- [ ] `exploration/stellarator_e2e/studies/promotion_equivalence.py` (NEW): both studies under the promoted structure; **exports to a caller-supplied `out_dir`, defaulting to `tmp_path` in tests** — no gitignore entry, nothing written inside the repo tree. *(This settles the design's open question on export location.)*
- [ ] The route's baseline path: execute the manifest's pinned baseline point and deposit `package_identity.json` + `baseline_result.json`. This is what Item 2's inserted step (Coordination ask 1 to Item 2, applied by the orchestrator) calls.

### Validation

**Automated:**
- [ ] `uv run python -m pytest tests/study -q` → green, including the 19-point sweep in the default suite
- [ ] `uv run python -m pytest tests/study -q -m slow` → the 948-point grid reproduces `design_search_R_a.csv` byte-for-byte

**Manual:**
- [ ] `git status --porcelain exploration/stellarator_e2e` empty after both runs — the committed CSVs and the proof-of-life directory are untouched.
- [ ] `baseline_result.json` validates against its schema and carries `source_local_identity` read from `contracts/model_contract.json` (S3), not from the era catalog view.

**What we know works after this phase:** the promoted route is the proof-of-life's route. Both committed CSVs reproduce exactly.

**Commits:** `promotion_equivalence.py`, the route/baseline emission, the baseline-result schema, `test_promotion_equivalence.py`.

---

## Phase 5: `preflight.py` — six named checks

### Goal

The generic gate tool: `gates` and `clean` subcommands, six checks, an always-complete results document, non-zero exit on any mechanical failure.

### Assumption under test

That all six checks can be answered from documents, package files, and git alone — with no teax import, no adapter import, and no package name in the file (Invariant 1, D10).

### Test stencil (write this first)

```python
# tests/study/test_preflight_negatives.py
@pytest.mark.parametrize("break_it,gate,needle", [
    (remove_declared_key,      "declared_keys",     "<the key>"),
    (point_key_at_a_channel,   "declared_keys",     "computed quantity"),
    (dirty_the_package,        "package_clean",     "<the file>"),
    (corrupt_the_identity,     "identity",          "recomputed"),
    (stale_the_manifest,       "manifest_currency", "semantic_fingerprint"),
])
def test_each_negative_fails_closed_and_still_writes_a_complete_document(...):
    rc, out, err = run_preflight(...)
    assert rc != 0 and needle in err
    doc = json.loads((out_dir / "preflight_results.json").read_text())
    assert {g["gate"] for g in doc["gates"]} == ALL_SIX          # D9: complete, not torn
    assert next(g for g in doc["gates"] if g["gate"] == gate)["status"] == "fail"
```

### Changes required

**See `design.md` for:** the six-check table and its record §9 row mapping (`design.md#scripts-study-preflight-py-six-named-checks`), D1, D9, S2, S5, Invariants 2, 6, 7.

- [ ] `tests/study/test_preflight_negatives.py`, `tests/study/test_preflight_gates.py` (NEW — first)
- [ ] `scripts/study/schemas/preflight_results.v1.schema.json` (NEW, additive)
- [ ] `scripts/study/preflight.py` (NEW): subcommands `gates` and `clean`; `clean` is what the post-run and post-verify sites use (`run_design_search.py:358,414,443`)
- [ ] `tests/study/test_generic.py`: add `preflight.py` to `TOOL_MODULES`
- [ ] Error wording — the design left it open; each message must **locate the fault**: name the key, the file, the drifting fingerprint, or the recomputed-vs-declared pair.

### Validation

**Automated:**
- [ ] `uv run python -m pytest tests/study -q` → green
- [ ] every negative exits non-zero **and** leaves a complete results document

**Manual:**
- [ ] `uv run python scripts/study/preflight.py gates …` against the real package → all six pass, exit 0, and the six results map onto record §9's five rows (the two fingerprint checks share a row).

**What we know works after this phase:** the gates are generic, honest by recomputation, and auditable from their own output.

**Commits:** `preflight.py`, its schema, both preflight test files, the `test_generic.py` extension.

---

## Phase 6: The manifest oracle-block values (Item 3 coordination ask 1)

### Goal

Point the delivered manifest's oracle block at the shim. **Data-only edit, its own step, explicitly authorized by the orchestrator.**

### Assumption under test

That the change is values-only and the delivered closed schema accepts it — `kind` stays `python_callable` (D6; the `cli` amendment is declined and the delivered validator rejects it anyway, `test_output_contract.py:103`).

### Changes required

- [ ] `exploration/stellarator_e2e/studies/manifest.json` — oracle block only: `sys_path: "exploration/stellarator_e2e/studies"`, `module: "oracle_entry"`, `callable: "evaluate"`, and a `note` stating the generic signature and the `operand_bindings` companion. No other key touched. No `scripts/study/*` file touched.

**Digest consequence (stated because it matters downstream):** the manifest's digest is the sha256 of its own bytes (`manifest.py` `load()`), so this edit changes it — currently `bd271da0…`. Verified 2026-08-20: **no committed file references that digest**, and no test pins it (`test_output_contract.py:146` recomputes). So the blast radius is (a) any *future* record snapshot must cite the new digest, and (b) any indicator report generated before this edit is stale. Neither is a code change. Item 3's `indicator_inputs` fingerprint is over package artifacts, not the manifest, and does not move.

### Validation

**Automated:**
- [ ] `uv run python -m pytest tests/study -q` → green (Item 3's manifest tests validate the edited file)
- [ ] `uv run python -m pytest tests/study -q -k manifest` → green

**Manual:**
- [ ] `git diff exploration/stellarator_e2e/studies/manifest.json` shows changes **inside the oracle block only**
- [ ] record the new digest in this plan's Implementation Notes

**What we know works after this phase:** the manifest names the seam `verify.py` will import, and nothing else moved.

**Commits:** the manifest oracle-block edit alone, so the data change is reviewable in isolation.

---

## Phase 7: `verify.py` — the generic sampler

### Goal

Store sampling, oracle parity at rel < 1e-9, verdicts re-derived through the published bindings, and one `verification_summary.json` that is a superset of the committed file and of Item 2's `arms[].verification` block.

### Assumption under test

That stratified store sampling plus published bindings produce a summary at least as strong as the proof-of-life's, with `verdicts_rederived: true` earned rather than asserted (Invariant 9).

### Test stencil (write this first)

```python
# tests/study/test_verify.py
def test_a_planted_channel_deviation_fails_naming_case_and_channel(...): ...
def test_a_planted_verdict_mismatch_fails_naming_the_constraint(...): ...
def test_a_missing_operand_bindings_attribute_fails_closed(...): ...     # Invariant 9
def test_the_derived_seed_reproduces_from_the_recorded_fields(...): ...  # N2 / D8
def test_stratification_covers_every_observed_verdict_combination(...): ...
def test_the_summary_is_a_superset_of_the_committed_field_set(...):
    committed = json.loads(COMMITTED_SUMMARY.read_text())    # 9 fields, by name or generalization
```

### Changes required

**See `design.md` for:** D7, D8/N2 (the written-out seed derivation), D12, the four-step per-case procedure and the full summary field list (`design.md#scripts-study-verify-py-the-generic-sampler`), Invariant 5, B5.

- [ ] `tests/study/test_verify.py` (NEW — first)
- [ ] `scripts/study/schemas/verification_summary.v1.schema.json` (NEW, additive)
- [ ] `scripts/study/verify.py` (NEW)
- [ ] `tests/study/test_generic.py`: add `verify.py` to `TOOL_MODULES`
- [ ] Settle the last open item: `operand_bindings_digest` canonicalization — `json.dumps(sort_keys=True, separators=(",",":"))` over the table, sha256 of the UTF-8 bytes. Recorded in the schema description so it is not re-invented.

### Validation

**Automated:**
- [ ] `uv run python -m pytest tests/study -q` → green

**Manual:**
- [ ] Run `verify.py` against the real package and the committed proof-of-life stores; diff the summary **field by field** against `exploration/stellarator_e2e/study/verification_summary.json`. Every committed field survives by name or named generalization (`sampled_rows_per_study` → per-store `sampling.sampled_rows`, `glue_note` → `not_independently_verified`, etc.). Worst channel deviation should land near `5.67e-16`.
- [ ] The glue disclosure is present: the CAS27 `special_materials` rung named as not independently verified.
- [ ] Committed stores unmodified afterwards (`git status --porcelain` empty; stores opened read-only).

**What we know works after this phase:** verification is generic, fails closed on anything unresolved, and emits everything the record needs.

**Commits:** `verify.py`, its schema, `test_verify.py`, the `test_generic.py` extension.

---

## Phase 8: The annex, the end-to-end pass, and the full-grid gate

### Goal

Write `ANNEX.md` with the six runbook-named sections, run the whole promoted route end to end against the real package, and run the slow grid one final time.

### Assumption under test

That the six annex sections the delivered runbook links are all fillable from what this item built — no seventh section, no orphaned link.

### Changes required

**See `design.md` for:** the annex table with its six sections and their linking steps (`design.md#exploration-stellarator_e2e-studies-annex-md`), L6.

- [ ] `exploration/stellarator_e2e/studies/ANNEX.md` (NEW): `§ Declared ties`, `§ Baseline pin`, `§ Oracle`, `§ Validity masks`, `§ Loader exception and glue` (carrying the deletion condition verbatim), `§ Era pin`. Package fact only, never a rule; nothing inlined into the runbook.
- [ ] `tests/study/test_era_pin.py`: enable the annex half of the pin-consistency assertion (all three files now exist).
- [ ] `tests/study/test_annex.py` (NEW, small): every one of the six section headings exists verbatim, and the `R > a + 2.25 m` mask is stated as a derived geometric bound rather than a design screen.

### Validation

**Automated:**
- [ ] `uv run python -m pytest tests/study -q` → green
- [ ] `STUDY_REQUIRE_ERA=1 uv run python -m pytest tests/study -q -rs` → green with **zero skips**
- [ ] `uv run python -m pytest tests/study -q -m slow` → the 948-point grid reproduces byte-for-byte
- [ ] `uv run ruff check scripts/study exploration/stellarator_e2e/studies tests/study` clean

**Manual:**
- [ ] Full route end to end on the real package: load through the adapter → emit `package_identity.json` + `baseline_result.json` → `preflight.py gates` (all six pass) → execute → `preflight.py clean` → `verify.py` → `preflight.py clean`. Three cleanliness sites preserved.
- [ ] Every spec success-criteria box in `spec.md#success-criteria` checked against evidence, and the count of era-dependent tests recorded in Implementation Notes.
- [ ] `git status --porcelain exploration/stellarator_e2e/study` empty — the pre-capability record is untouched.

**What we know works after this phase:** the whole item, end to end, on the real package, with the annex the runbook links.

**Commits:** `ANNEX.md`, `test_annex.py`, the pin-test completion, and the final plan bookkeeping.

---

## Risk Management

**See `design.md#potential-risks` for the full analysis.** Phase-specific mitigations:

- **Phase 0 — the package may have been regenerated.** The probe re-run is a gate, not a formality: 0 differing artifacts means the adapter is *absent*, not retained, and Phases 3, 4 and the equivalence gate retire. Stop and surface rather than proceeding.
- **Phase 1 — the binding table is hand-authored and unverified.** A wrong key makes verify compare the wrong number and read as a pass. The test resolves all five constraints against the real contract, and `verify.py` (Phase 7) fails closed on anything unresolvable.
- **Phase 3 — editing `verify_stellaris.py` or `oracle_entry.py` retires every existing store.** Correct under Invariant 4, sharp for anyone editing either for unrelated reasons. The refusal message names the file whose digest moved, and `ANNEX.md § Loader exception and glue` states it.
- **Phase 4 — equivalence may fail on float text rather than physics.** The 19-row sweep fails first and cheaply, and the test reports the first differing line with both values.
- **Phase 6 — the manifest edit is data-only but it is Item 3's file.** Its own commit, oracle-block-only diff, and the digest consequence recorded above.
- **Every phase — a silently skipped era test.** `STUDY_REQUIRE_ERA=1` in this item's own validation runs, plus a never-skipping pin test, plus the recorded era-dependent test count.

---

## Implementation Notes

[TO BE FILLED DURING IMPLEMENTATION]

### Phase 0 Completion
**Probe `[P3]` result:**
**Completed:** · **Actual changes:** · **Issues:** · **Deviations:**

### Phase 1 Completion
### Phase 2 Completion
### Phase 3 Completion
### Phase 4 Completion
### Phase 5 Completion
### Phase 6 Completion
**New manifest digest:**
### Phase 7 Completion
### Phase 8 Completion
**Era-dependent test count:**

---

**Status:** Draft → In Progress → Complete
**Next Step:** `/_my_implement`
