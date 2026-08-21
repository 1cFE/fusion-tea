# Implementation Plan: Stellarator Model Migration

**Status:** Complete (all six phases, 2026-08-21) — next `/_my_audit`
**Created:** 2026-08-21
**Last Updated:** 2026-08-21
**Branch:** `feat/stellarator-model-migration` (one PR; see design D5)

## Source Documents
- **Spec:** `.project/active/stellarator-model-migration/spec.md`
- **Design:** `.project/active/stellarator-model-migration/design.md` ← component details, decisions D1–D15, invariants I1–I12
- **Acceptance oracle:** `exploration/stellarator_e2e/studies/BEFORE_MIGRATION_RECORD.md` § 7

## The Point

RUN-STUDY Item 6, the first A/B consumer, must run on the stock teax route. Today the stellarator package only runs on a frozen teax worktree through `studies/era_adapter.py`, which hand-feeds five things the old codegen could not produce, and one of them (CAS27) is fed identically to the package and to the oracle, so the verification has a disclosed hole. The pinned codegen (`8a758e92`) can now produce all five, but it refuses the **model** for four known reasons (99 self-named bindings, six scalar function calls, unit text scraped from trailing comments, four positional usages that skip a defaulted formal).

This item repairs the model so it generates clean at runtime contract `2.0.0`, proves the regenerated package gives the same numbers as the before-record (by value, rel < 1e-9), closes the CAS27 hole, deletes the adapter whole, and returns the MFE models to `models/` with the IFE regression proof intact. Every model edit is ledgered and classified (`[OWNER-VERBATIM 2026-08-21]` "track them, classify the change, provide rationale … but I don't want to let this slow us down"). The only stop is a Class C finding: a refusal with no equivalent form.

## Implementation Strategy

**Phasing Rationale:**
The six phases are the design's six integration boundaries (`design.md#integration-strategy`). Phase 1 is first because it holds the only unknown: whether a fifth refusal class hides behind the four known ones. Nothing after it is worth doing until the pinned codegen accepts the repaired tree. Phases 2–3 earn the sealed identity and the numerical proof before any promotion or deletion touches `models/` or the study route. Phase 4 (promotion) and Phase 5 (retirement) are independent of each other but both depend on Phase 3; promotion goes first because its family tests are what make Phase 5's deletions safe to verify. Phase 6 closes the branch.

**Critical Path:**
repair staged tree → `generate` reports zero diagnostics → in-place regen seals at 2.0.0 and stock `strict=True` load passes → baseline LCOE = 275.2642200420774 on the stock route → 948 + 19 points match by value → promote + family spine green → delete adapter → suites green.

**First Proof Point:**
`uv run sysml-codegen generate --models exploration/stellarator_e2e/models --output <scratch> --package-name stellarator_tea --overwrite` exits 0 with zero readiness diagnostics. Everything before that is edits; that command is the first fact.

**One ordering resolution the plan makes.** The design lists "switch the study entry points to the strict stock loader" under boundary 5 (retirement), but boundary 3's grid and sweep cannot run without a stock route. So Phase 3 builds the stock route in `study/run_design_search.py` (that is also where its glue is removed), and Phase 5 only deletes what is left: the adapter modules, era fixtures and tests, the `run_stellaris*.py` glue, and the annex sections.

**Overall Validation Approach:**
- Each phase starts with a test stencil; model-generating tests need a SysIDE license and fail (never skip) without it, matching the existing spine test.
- Each phase ends with automated checks plus a manual read of the evidence it produced.
- Numerical drift is a finding to explain, never a tolerance to widen (`design.md#implementation-notes`).

---

## Environment Setup

**See CLAUDE.md for `uv` rules.** Every command below is `uv run …`.

```bash
source /home/reid/1cfe/agentic-mbse/.env            # SYSIDE_LICENSE_KEY (licensed model tests fail without it)
export STOP_PARSER_TEAX_ROOT=/home/reid/1cfe/teax   # stock teax; HEAD must be 744745f (design D4, I2)
export STOP_PARSER_WHEEL_TARGET=$PWD/.venv/lib/python3.12/site-packages   # root acceptance tests only
git -C "$STOP_PARSER_TEAX_ROOT" rev-parse --short HEAD   # → 744745f, or stop (design#potential-risks)
```

- Pinned codegen is the installed one (`.venv/…/sysml_codegen`, from `pyproject.toml:37` rev `8a758e92`). The local checkout `/home/reid/1cfe/sysml-codegen` is at `84bb83b`, **not** the pin. Never generate through the checkout (I2).
- The D-5 transformer is run from the pinned blob, not the checkout HEAD: `git -C /home/reid/1cfe/sysml-codegen show 8a758e92:scripts/make_d5_variant.py > <scratch>/make_d5_variant.py`. Record the blob hash in the ledger header.
- Scratch: `/tmp/claude-1000/-home-reid-1cfe-fusion-tea/<session>/scratchpad/` or `exploration/stellarator_e2e/study/_work/` (gitignored). Nothing migration-only is committed except the ledger and the after-record.

---

## Phase 1: Repair the staged source until the pinned codegen accepts it

### Goal
Apply the four known repair classes to `exploration/stellarator_e2e/models/` (the D-5 workbench, design D1), ledger every site, and iterate `sysml-codegen generate` to a scratch output until it reports zero readiness diagnostics. This phase holds the only anticipated owner stop, so it runs first and alone.

### Assumption Under Test
Past the four known refusal classes there is nothing else (spec: "Past those four classes, unknown"). If a fifth class appears and has an equivalent form, it is Class A or B and ledgered; if it has none, it is Class C: stop, surface, park Phases 2–6.

### Test Stencil (Write This First)
```python
# tests/models/test_model_family_spines.py  (NEW — Phase 4 grows it into the full family registry, design D6)
# Phase 1 lands only the MFE generation row. Licensed; fails without SYSIDE_LICENSE_KEY.

FAMILIES = {
    "mfe": {"tree": "exploration/stellarator_e2e/models", "package": "stellarator_tea"},
}

@pytest.mark.parametrize("family", sorted(FAMILIES))
def test_family_tree_generates_with_zero_readiness_diagnostics(family, tmp_path):
    copy = _copy_tree(tmp_path, FAMILIES[family]["tree"])
    assert _generate(copy, tmp_path / "package", FAMILIES[family]["package"]), family

def test_staged_mfe_tree_has_no_self_named_binding_and_no_trailing_unit_comment():
    # license-free: the two mechanical repairs are complete
    for path in STAGED.rglob("*.sysml"):
        for line in path.read_text().splitlines():
            assert not re.match(r"\s*in (\w+) = \1\b", line), (path, line)
            assert not re.match(r"\s*in attribute .*//", line), (path, line)
```

### Changes Required

**See `design.md` for:**
- Edit classes and forms → `design.md#key-decisions` D1, D2, D13, D14
- Handwritten accessor order-of-operations → `design.md#implementation-notes`
- Ledger columns → `design.md#component-overview` "Migration ledger" and spec SC8

**Specific changes:**

#### 1. Test file
**File:** `tests/models/test_model_family_spines.py` (NEW, MFE generation row + the two license-free structural checks)
- [x] Create with the stencil above; confirm it **fails** on the unrepaired tree (generation refused)

#### 2. D-5 rename — 99 sites, Class A
- [x] Extract the transformer from the pinned blob (see Environment); run `--root exploration/stellarator_e2e/models --scratch <scratch>/d5` with the formals census; confirm "preconditions: clear" and the site census is 94 (`mfe_plant.sysml`) + 5 (`stellarator_plant.sysml:870-879`)
- [x] Strip-check passes; replace the staged files with the variant
- [x] Save the tool's census output to scratch — it seeds the ledger's 99 mechanical rows

#### 3. Positional usages — 4 sites, Class A (design D13)
- [x] Reorder defaulted formals last in the four calc defs: `'Plasma Geometry'` and `'MFE Radial Build'` (`mfe_plasma_scaling.sysml:30,71`, `pi`), the supplementary-cost def (`mfe_account_costs.sysml:559-590`, four rate formals), `'Neutron Wall Load'` (`mfe_plasma_scaling.sysml:231`, `ash_frac`)
- [x] Check every other usage of those four defs still binds by name or in the new order (grep the usages: `mfe_plant.sysml:116,141,530`, `stellarator_plant.sysml:855`, plus any others)

#### 4. Trailing unit comments — 101 sites, Class A (design D14)
- [x] Move each `in attribute … // text` comment to the line above the declaration; no text deleted (`grep -rnE '^\s*in attribute .*//' exploration/stellarator_e2e/models | wc -l` → 0)

#### 5. Scalar-function sites — 2 calc defs, 6 sites, Class B, marked for revert (design D2)
- [x] `mfe_plasma_scaling.sysml:194` (`RealFunctions::sqrt` in `'DT Fusion Power'`): keep formals, formula, sources, guards in the doc comment; make the output opaque (no executable expression)
- [x] `mfe_account_costs.sysml:816,820,830-832` (`max`/`min`/`floor` in `'Levelized Replacement Cost'`): same treatment; the intermediate attributes `fpy_raw`, `core_lifetime_*`, `n_rep` go into the doc as the normative formula
- [x] Ledger rows carry the exact pre-rewrite text (also in git at the PR parent `7ee0c22a`)

#### 6. Handwritten accessors (before any regeneration — `design.md#implementation-notes`)
- [x] `generated/handwritten/mfe_plasma_scaling/dt_fusion_power_impl.py`: eight input field reads move to `<name>_in`; `V` unchanged
- [x] `generated/handwritten/mfe_account_costs/levelized_replacement_cost_impl.py:96-106`: `ash_frac`, `fluence_limit`, `availability`, `operational_years` reads move to `_in`
- [x] Both keep `AUTO_IMPLEMENTED = False` and their normative bodies byte-for-byte otherwise

#### 7. Migration ledger
**File:** `models/stellarator_migration_ledger.md` (NEW; canonical paths become authoritative in Phase 4, staged paths are fine until then)
- [x] Header: toolchain revisions (codegen pin, D-5 blob hash, teax), date, R5 class key, revert rule
- [x] One row per site: `#`, file:line, trigger (diagnostic or rule), class, replaced form, new form, rationale, revert marker, `Source`/`Ref`/`Basis` (only where a value is introduced or relocated — none expected in this phase; say so per row or in a column note)
- [x] Mechanical rows (99 D-5, 101 comments) are generated by a scratch script from the tool census and `git diff`, then reviewed; the 4 + 2 judgement rows are hand-written

#### 8. Iterate generation
- [x] `uv run sysml-codegen generate --models exploration/stellarator_e2e/models --output <scratch>/gen1 --package-name stellarator_tea --overwrite` until zero diagnostics
- [x] Any new diagnostic: classify (A/B → fix + ledger row; C → **stop**, ledger row, file upstream, report to owner, do not proceed)

### Validation

**Automated:**
- [x] `uv run python -m pytest tests/models/test_model_family_spines.py -q` → MFE row passes, structural checks pass
- [x] `uv run python -m pytest tests/models -q` → IFE spine still 10/10 (nothing in `models/` changed yet)
- [x] D-5 strip check printed "identical" for all 14 files

**Manual:**
- [x] Read the generation log: zero readiness diagnostics, no `SI_SELF_BINDING`, no `SI_RENDERING_COLLISION`, no unit collision
- [x] Ledger row count equals changed-site count (`git diff --stat exploration/stellarator_e2e/models` as the cross-check); no Class C row
- [x] Count the two manual-interface calc defs in the scratch package's `IMPLEMENTATION_BACKLOG.md` — exactly 2 functions listed, both the expected ones

**What We Know Works After This Phase:**
The repaired MFE tree is accepted by the pinned codegen. Every edit is classified. Either there is no Class C finding and Phases 2–6 are unblocked, or there is one and the owner has it.

---

## Phase 2: Regenerate in place, seal at 2.0.0, stock strict load

### Goal
Replace the sealed `1.0.0` package under `exploration/stellarator_e2e/generated/` with a `2.0.0` package generated from the repaired tree, preserving only the two normative handwritten implementations, and prove the stock teax loader accepts it with `strict=True` and that the five formerly glued shapes are present from model source.

### Assumption Under Test
B2 and the handwritten-preservation bet: smart regeneration keeps the two `AUTO_IMPLEMENTED = False` files by signature match, and the regenerated inputs/pipeline carry CAS28, `n_mod`, the BOP repoint, and cross-part CAS27 without any injection, with the three dead fillers gone.

### Test Stencil (Write This First)
```python
# tests/study/test_stock_route.py  (NEW — replaces the era loader tests' job on the stock route)
# Needs STOP_PARSER_TEAX_ROOT (design D4). Skips with the resolved path in the reason if absent;
# STUDY_REQUIRE_TEAX=1 turns that skip into a failure (same pattern the era fixture used).

def test_stock_strict_loader_accepts_the_sealed_package(stock_simkit_path, real_package_path):
    from simkit.evaluation.package_load import ProvisionalPackageLoader
    loaded = ProvisionalPackageLoader(real_package_path, "stellarator_tea", strict=True).load()
    contract = json.loads((real_package_path / "contracts/package_contract.json").read_text())
    assert contract["runtime_contract_version"] == "2.0.0"
    assert _artifacts_differing_from_seal(real_package_path) == []

def test_sealed_identity_is_the_executable_fingerprint(real_package_path):
    doc = identity.build_sealed(package_name="stellarator_tea", package_root=real_package_path)
    assert doc["identity"]["digest"] == doc["identity"]["sealed_executable_fingerprint"]
    assert doc["identity"]["allowed_modified_files"] == [] and doc["glue_ledger"] == []

def test_formerly_glued_shapes_come_from_model_source(real_package_path):
    inputs, pipeline = _entry_sources(real_package_path), _pipeline(real_package_path)
    assert _one_supplier(inputs, suffix="__cas28_capital") == 5_000_000.0         # g2
    assert _one_supplier(inputs, suffix="__replacement_cost_per_event__n_mod") == 1.0
    assert not any(k in DEAD_FILLERS for (_g, k) in inputs)                        # fillers gone
    assert _wired_from_module(pipeline, "linear power cost", "power") == "power balance output"  # g1 repoint
    assert _wired_from_module(pipeline, "cas23_to_28_capital", "special_materials_capital")     # g3 CAS27
```

### Changes Required

**See `design.md` for:**
- Generation command and seal checks → `design.md#validation-approach` SC1
- Preservation sequencing and symlink conversion → `design.md#implementation-notes`
- Stock runtime integration (`expects_constraint_report`, `semantic_fingerprint`) → `design.md#architecture` § 3

**Specific changes:**

#### 1. Test file + fixture
- [x] `tests/study/test_stock_route.py` (NEW) with the stencil
- [x] `tests/study/conftest.py`: add `stock_simkit_path` (reads `STOP_PARSER_TEAX_ROOT`, puts `packages/teax-simkit` on `sys.path`, asserts the imported `simkit.__file__` is under that root; skip/fail rule as above). Leave the era fixtures in place until Phase 5.

#### 2. Package symlink (design D10)
- [x] `exploration/stellarator_e2e/pkg/stellarator_tea` → relative `../generated`; `git diff` shows the link target change only; assert `Path(...).resolve()` is inside this worktree

#### 3. Regenerate in place
- [x] Delete the 42 `AUTO_IMPLEMENTED = True` files under `generated/handwritten/` (keep the two normative impls and `__init__.py` files)
- [x] `uv run sysml-codegen generate --models exploration/stellarator_e2e/models --output exploration/stellarator_e2e/generated --package-name stellarator_tea --overwrite --smart-regen --preserve-handwritten`
- [x] Inspect the two preservation decisions in the log: both **retained**, none backed up or stubbed; `sha256sum` of the two impls unchanged from the Phase 1 edit
- [x] Recapture `exploration/stellarator_e2e/stellarator.snapshot.json` from the repaired tree (`capture_instance_graph_snapshot`), so the tracked snapshot matches the sealed package

#### 4. Record
- [x] Start `exploration/stellarator_e2e/studies/AFTER_MIGRATION_RECORD.md` (design D15) § 1 Identity: codegen pin, teax `744745f`, new `executable_fingerprint`, `semantic_fingerprint`, artifact count, `runtime_contract_version 2.0.0`, preservation decisions

### Validation

**Automated:**
- [x] `STUDY_REQUIRE_TEAX=1 uv run python -m pytest tests/study/test_stock_route.py -q` → all pass
- [x] `uv run python -m pytest tests/models/test_model_family_spines.py -q` → still green
- [x] `git status --short exploration/stellarator_e2e/generated` shows regenerated files only; nothing outside `handwritten/**` hand-edited (I1)

**Manual:**
- [x] `python -c` recompute of every `artifact_hashes` entry → 0 differ (before: 2 of 139)
- [x] `generated/IMPLEMENTATION_BACKLOG.md` lists exactly the two manual functions
- [x] Old era tests are now expected to fail against this package (they load `1.0.0` semantics) — note it, do not fix them; Phase 5 deletes them

**What We Know Works After This Phase:**
A sealed `2.0.0` package that stock teax accepts strictly, with its own sealed identity and no injected values. SC1 is met; SC3's deletion condition (`era_adapter.py:3-9`) is satisfied in fact, pending the numerical proof.

---

## Phase 3: One-time equivalence, manifest re-pin, CAS27 closure

### Goal
Run the stellarator on the stock route and prove the regenerated package gives the before-record's numbers by value: baseline, 948-point grid, 19-point sweep, five verdicts. Re-pin the study manifest from the emitted contract, pass all four preflight gates, and run oracle verification with CAS27 now compared for the first time. Commit the verdict in the after-record, not a live comparison test (design D12, D15).

### Assumption Under Test
B1 (every repair is numerically inert at every accepted point, not only the baseline) and B5 (joining on physical coordinates and `source_local_identity` survives the D-5 key movement).

### Test Stencil (Write This First)
```python
# tests/study/test_verify.py — the assertion that flips (line 108 today asserts the glue note SURVIVES)
def test_verification_has_no_undisclosed_rung(summary):
    assert summary["not_independently_verified"] == []          # SC4: CAS27 is compared, not disclosed
    assert {"special_materials_capital", "total_capital", "lcoe"} <= _channels_compared(summary)

# tests/study/test_known_answers.py — re-derived against the new contract, never patched
EXPECTED_SEMANTIC_FINGERPRINT = "<read from the sealed 2.0.0 model_contract.json>"

# tests/study/test_preflight_gates.py — on the stock route, all four gates pass
def test_all_four_gates_pass_on_the_stock_route(stock_baseline_run):
    assert {g["gate"]: g["status"] for g in stock_baseline_run["gates"]} == {
        "identity": "pass", "manifest_currency": "pass", "baseline_headline": "pass", "package_clean": "pass"}
```

### Changes Required

**See `design.md` for:**
- Evidence boundary, join keys, and the no-permanent-oracle rule → `design.md#architecture` § 4, D12, D15
- Key resolution through the contract, never suffix bulk-replace → `design.md#implementation-notes`
- Stock evaluator requirements → `design.md#architecture` § 3

**Specific changes:**

#### 1. Stock route in the study runner
**File:** `exploration/stellarator_e2e/study/run_design_search.py`
- [x] Drop the era `sys.path` insert (`:72`), `GlueAwareLoader` (`:155-180`), and every g1/g2/g3 injection; construct `ProvisionalPackageLoader(..., strict=True)`; derive `expects_constraint_report` from the embedded contract; pass `semantic_fingerprint` to the study config; emit identity via `scripts.study.identity.build_sealed`
- [x] Resolve the renamed entry keys (`AXES`, baseline point) from `contracts/model_contract.json`, recording each qualified identity; `run`/`verify`/`export` subcommands keep their contract
- [x] Run the baseline, grid, and sweep into `study/_work/` (gitignored). **Do not overwrite** the tracked proof-of-life CSVs `study/design_search_R_a.csv` and `study/availability_sweep.csv` — they are the before-evidence; export the after CSVs beside them under `_work/` (their future home is the "generated artifacts" BACKLOG row's call)

#### 2. Oracle seam
**File:** `exploration/stellarator_e2e/studies/oracle_entry.py`
- [x] Remove `GLUE_FED` sentinels (`:71-72`), `GLUE_VALUE_KEYS` (`:140`), `glue_values()` (`:249`); map `special_materials_capital` as an oracle-computed channel so the verifier compares it; update `ENTRY_KEY_TO_ORACLE_INPUT` and `operand_bindings()` to the renamed keys (resolved from the contract)
- [x] `verify_stellaris.py` is imported, never modified (manifest `oracle.note`)

#### 3. Manifest re-pin
**File:** `exploration/stellarator_e2e/studies/manifest.json`
- [x] `fingerprints.indicator_inputs` (recompute via `scripts.study.manifest.indicator_input_fingerprint`), `recorded_provenance` (new executable + semantic fingerprints), `baseline.point` keys, `ties`, `objective_catalog` channels (add `total_capital` and `special_materials_capital` if not present so CAS27 coverage cannot be masked — design § 4), `baseline.headline` unchanged at `275.2642200420774`, verdict identities unchanged
- [x] `tests/study/data/axes.known_answers.json` and the six expectation files: re-derive from the new package; `test_fixture_binding` must fail first, then pass

#### 4. One-time comparison harness (scratch, deleted in Phase 5)
- [x] Script joins before CSVs (tracked) and after CSVs (`_work/`) on `(R, a)` / `availability`; asserts rel dev < 1e-9 on `lcoe` (and reports `total_capital`, `lcoe_1cfe`, `p_fus`, `wall_load`) and identical `beta_ok … feasible` per point; prints worst deviation per channel
- [x] Any drift: stop, explain in the after-record, no tolerance change

#### 5. Executed mutation probe (SC10's runtime half; the structural half is Phase 4)
- [x] At the baseline, move `cas28_capital` by a known amount in a `package_copy` and assert `total_capital` moves by exactly that amount, LCOE moves, `p_fus` and `wall_load` do not
- [x] Move one radial-build thickness and assert the blanket-volume-fed channels (CAS27, blanket cost) move and the plasma channels do not

#### 6. After-record
- [x] § 2 Baseline (LCOE, `total_capital`, `cas90`, channel count, five verdicts by identity), § 3 Grid/sweep verdict (point counts, worst rel dev per channel, after-CSV sha256s, command lines), § 4 Verification summary (`channels_checked`, `worst_channel_rel_dev`, `not_independently_verified: []`), § 5 Preflight 4/4, § 6 Mutation probes

### Validation

**Automated:**
- [x] `STUDY_REQUIRE_TEAX=1 uv run python -m pytest tests/study/test_known_answers.py tests/study/test_verify.py tests/study/test_preflight_gates.py tests/study/test_stock_route.py -q` → pass
- [x] `uv run python scripts/study/preflight.py gates --package exploration/stellarator_e2e/pkg/stellarator_tea --manifest exploration/stellarator_e2e/studies/manifest.json --groups tests/study/data/axes.known_answers.json --identity <_work>/package_identity.json --baseline-result <_work>/baseline_result.json` → 4/4 pass
- [x] `uv run python scripts/study/verify.py --package … --manifest … --identity … --store <_work>/design_search_R_a.db --store <_work>/availability_sweep.db --out <_work>/verification_summary.json` → `not_independently_verified: []`, tolerance 1e-9
- [x] `git diff --stat -- scripts/study/` → empty (I11, SC5)
- [x] `uv run ruff check scripts/study tests/study exploration/stellarator_e2e/study` → clean

**Manual:**
- [x] Comparison harness output: 948 + 19 joined rows, zero unmatched coordinates, worst LCOE rel dev recorded
- [x] Baseline LCOE printed equals `275.2642200420774` to all digits (or the deviation is explained)

**What We Know Works After This Phase:**
SC2, SC4, SC5 and SC10's runtime half are met on the stock route. The migration is numerically proven; nothing yet is deleted or promoted.

---

## Phase 4: Promote MFE into `models/` and reshape the spine into family tests

### Goal
Copy the final MFE source into `models/library/` and `models/designs/` (22 canonical SysML files), synchronize the shared CAS-scope enum to all three homes (design D9), replace `test_self_binding_replacement.py` with a family registry (D6–D8), add the MFE census and two named mutations, re-scope the two root acceptance tests to an IFE subset, and repoint `test_power_balance.py`.

### Assumption Under Test
B3: the staged MFE tree is self-contained, so a canonical subset built from the MFE family's owned paths generates identically to the twin; and the three-member enum is inert for IFE (23/18 census and both IFE mutations unchanged).

### Test Stencil (Write This First)
```python
# tests/models/test_model_family_spines.py (replaces test_self_binding_replacement.py; design D6–D8)
FAMILIES = {
    "ife": Family(twin="exploration/ife_e2e/models", owned=IFE_PATHS, package="self_binding_check",
                  entry_points=23, design_attributes=18, library_defaults=..., usage_literals=...),
    "mfe": Family(twin="exploration/stellarator_e2e/models", owned=MFE_PATHS, package="stellarator_tea",
                  entry_points=<read from the first clean 2.0.0 package>, design_attributes=<same>, ...),
}

@pytest.mark.parametrize("family", sorted(FAMILIES))
def test_canonical_subset_equals_twin_byte_for_byte(family): ...
@pytest.mark.parametrize("family", sorted(FAMILIES))
def test_family_generates_and_live_equals_snapshot(family, tmp_path): ...
@pytest.mark.parametrize("family", sorted(FAMILIES))
def test_family_census_is_exact(family, baseline_package): ...       # IFE: neutral 18-set = the old 11 ∪ 7 (D7)
def test_owned_paths_cover_every_canonical_sysml_file_and_shared_paths_agree(): ...   # D8
def test_ife_gain_mutation_reaches_every_and_only_its_three_consumers(...): ...        # unchanged
def test_ife_beam_energy_mutation_reaches_its_nested_consumer_and_nothing_else(...): ...  # unchanged
def test_mfe_cas28_capital_mutation_reaches_every_and_only_its_consumers(...): ...     # SC10 structural
def test_mfe_blanket_thickness_mutation_reaches_every_and_only_its_consumers(...): ... # SC10 nested
```

### Changes Required

**See `design.md` for:**
- Family registry, subsets, enum promotion → `design.md#key-decisions` D6–D9
- Canonical file count and twin invariants → `design.md#validation-approach` SC6, I9, I10
- Root acceptance tests need an IFE subset → `design.md#research-findings` (the two-plant assumption)

**Specific changes:**

#### 1. Promote source
- [x] Copy the 14 staged files into `models/library/{foundation,cost_structure,analyses}/` and `models/designs/{generic_mfe,stellarator_09}/` (logical-path mapping = the existing `strip_library` rule)
- [x] `economic_parameter.sysml` (3-member enum): canonical ← staged; copy to `exploration/ife_e2e/models/foundation/` too
- [x] Confirm `cas_hierarchy.sysml` and `costed_component.sysml` are byte-identical across canonical, IFE twin, MFE twin (if not, that is a finding: resolve to one file in all three and ledger it)
- [x] Canonical now has 22 `.sysml` files

#### 2. Family spine
- [x] `tests/models/test_model_family_spines.py`: grow the Phase 1 file into the stencil; port `_entry_sources`, `_consumers_of`, `_predicate_feature_refs`, `_model_files_by_logical_path` unchanged from the old module
- [x] MFE census numbers and consumer sets: read from the Phase 2 sealed package (`contracts/model_contract.json`, `pipelines/*.yaml`), never from the retired `1.0.0` contract (`design.md#implementation-notes`)
- [x] IFE: the 11 + 7 identity sets merge into one 18-set; 23/18 classification, `LIBRARY_DEFAULTS`, `USAGE_LITERALS`, both mutations unchanged (D7 — record the choice in the module docstring and in SC7's ledger line)
- [x] Delete `tests/models/test_self_binding_replacement.py`

#### 3. Root acceptance tests
- [x] `tests/test_codegen_teax_acceptance.py:16-32` and `tests/test_occurrence_mutation_teax.py:18-28`: `MODEL_TREES["primary"]` becomes a materialized IFE canonical subset (reuse the family registry's owned-path list), expectations unchanged

#### 4. Power-balance test and notes
- [x] `tests/models/test_power_balance.py:20-30`: `LIBRARY_DIR = models/library`, delete the TEMPORARY note
- [x] `exploration/stellarator_e2e/STAGED_MODELS.md` → rewrite as the twin's note (mirror of `models/`, kept byte-identical by the family spine), or delete if `exploration/ife_e2e/` carries no equivalent; record the choice
- [x] Ledger: switch file:line references to canonical paths (design "Finalize ledger line references")

### Validation

**Automated:**
- [x] `uv run python -m pytest tests/models -q` → green; family spine: both families generate, censuses exact, four mutations pass
- [x] `STOP_PARSER_TEAX_ROOT=… STOP_PARSER_WHEEL_TARGET=… uv run python -m pytest tests/test_codegen_teax_acceptance.py tests/test_occurrence_mutation_teax.py -q` → green on the IFE subset
- [x] `uv run agentic-mbse validate models --level 1` → pass (the current project bar; `design.md#research-findings`)

**Manual:**
- [x] `find models -name '*.sysml' | wc -l` → 22; `diff -r` canonical logical paths vs each twin → empty
- [x] IFE census unchanged: 23 entry points / 18 design attributes (proves the enum member is inert, D9)

**What We Know Works After This Phase:**
SC6, SC7, SC10 (structural) met. `models/` is a two-family source collection with byte-identical twins, and each family generates alone. The "Test cleanup" BACKLOG row is discharged in substance.

---

## Phase 5: Retire the era route whole

### Goal
Delete the adapter and everything that exists only for it. No dormant branch, no partial retirement (`era_adapter.py:3-9`). Retired identifiers survive only in the before-record and historical project records (I12).

### Assumption Under Test
Nothing on an executable, test, or runbook path still needs the era route. The Phase 2–4 tests are the safety net: if a deletion breaks one of them, something was still load-bearing.

### Test Stencil (Write This First)
```python
# tests/study/test_no_retired_identifiers.py (NEW, license-free, fast)
RETIRED = ("era_adapter", "promotion_equivalence", "fa0e06a", "teax-v1-era", "GlueAwareLoader", "GLUE_FED", "glue_values")
HISTORICAL = {"exploration/stellarator_e2e/studies/BEFORE_MIGRATION_RECORD.md",
              "exploration/stellarator_e2e/study/synthesis.md", "exploration/stellarator_e2e/study/report.html"}

def test_retired_identifiers_appear_only_in_historical_records(repo_root):
    hits = _grep(repo_root, RETIRED, roots=("exploration", "scripts", "tests", ".claude/skills"))
    assert {h.path for h in hits} <= HISTORICAL, sorted(set(h.path for h in hits) - HISTORICAL)
```

### Changes Required

**See `design.md` for:**
- Retirement inventory → `design.md#architecture` § 6 and `#validation-approach` SC3
- Annex/runbook handling → D11

**Specific changes:**
- [x] Delete `exploration/stellarator_e2e/studies/era_adapter.py`, `studies/promotion_equivalence.py`
- [x] `tests/study/conftest.py`: delete the era section (`ERA_PIN_COMMIT`, `_era_worktree`, `era_simkit_path`, `PackageCopy.emit_identity`/`edit_glue`); `committed_store_path` points at stock-route stores or is deleted with its users
- [x] Delete or rewrite against the stock route (inventory by `grep -ln "era\|glue" tests/study/*.py`, not the spec's count): `test_era_pin.py` (delete), `test_promotion_equivalence.py` (delete — D12), `test_glue_mapping_agreement.py` (delete), `test_accept_set.py`, `test_committed_store.py`, `test_lineage_refusal.py`, `test_identity.py` (era-named fixture data only → rename), `test_preflight_gates.py:46-51`, `test_verify.py:46-82` (stock fixture). Keep `test_generic.py:21`'s "no `era_adapter` in `scripts/study`" needle — it is the package-agnostic gate.
- [x] `exploration/stellarator_e2e/run_stellaris.py:128-154` (`patch_bop_wiring`, glue-1) and `run_stellaris_single.py:25-44` (`CAS28_CAPITAL`, `N_MOD` injection): delete the glue; the runners load the sealed package strictly or are reduced to the helpers that `verify_stellaris.py`/`build_verdict_report.py` still import (check importers first)
- [x] `exploration/stellarator_e2e/study/make_report.py:420-431`: the glue caveat text describes the proof-of-life run (historical); leave as a dated statement or mark it as describing the before-run — do not let it claim the current route has glue
- [x] `studies/ANNEX.md`: remove `§ Loader exception and glue` (`:140-195`, incl. the deletion-condition note, now met) and `§ Era pin` (`:196-`); `.claude/skills/run-study/runbook.md:103,147,160,213` → conditional reads ("when the annex has such a section")
- [x] Delete the Phase 3 comparison harness from wherever it lived; keep the after-record
- [x] `pyproject.toml:53-55`: drop the `slow` marker if no test uses it after `test_promotion_equivalence.py` goes

### Validation

**Automated:**
- [ ] `uv run python -m pytest tests/study/test_no_retired_identifiers.py -q` → pass
- [ ] `STUDY_REQUIRE_TEAX=1 uv run python -m pytest tests/study -q` → green, 0 skipped (record the new count; before: 273)
- [x] `uv run python -m pytest tests/models -q` → still green
- [ ] `uv run ruff check scripts/study tests/study exploration/stellarator_e2e` → clean

**Manual:**
- [ ] `grep -rn "fa0e06a\|teax-v1-era\|era_adapter\|promotion_equivalence" exploration scripts tests .claude docs` → only the historical files
- [x] `git -C /home/reid/1cfe/teax-v1-era` is **not** touched (tidy pass is a Non-Goal)

**What We Know Works After This Phase:**
SC3 met. The study and test paths have one route: stock teax, sealed identity.

---

## Phase 6: Close the branch gates

### Goal
Run every suite the spec names, finish the after-record, make the upstream filings, update the BACKLOG rows and CURRENT_WORK, and leave the branch ready for `/_my_audit` and `/_my_pre_pr`.

### Assumption Under Test
Nothing. This phase produces the record; a failure here is a regression from Phases 1–5 and goes back to its phase.

### Test Stencil
No new tests. The gate list below is the checklist.

### Changes Required

**See `design.md#validation-approach` for the per-SC proof table.**

- [x] `source …/.env; uv run python -m pytest tests/models -q` → record counts
- [x] `STUDY_REQUIRE_TEAX=1 uv run python -m pytest tests/study -q` → record counts
- [x] Root acceptance pair with both `STOP_PARSER_*` vars → green
- [ ] `uv run python -m pytest tests/test_dependency_provenance.py -q` → green; `uv lock --check` → passes
- [x] `uv run agentic-mbse validate models --level 1` → pass; `uv run agentic-mbse validate models --complete` → record offender delta vs `main` (Levels 2 and 6 already red on `main`; the delta must be zero new offenders)
- [x] MR-4 review: every value the ledger marks "introduced or relocated" has `Source`/`Ref`/`Basis`; the two manual-interface docs keep their citations (I4)
- [x] `AFTER_MIGRATION_RECORD.md` complete: § 1–6 from Phases 2–3 plus § 7 suites table and § 8 "what changed and why" (ledger summary by class: A count, B count, C none)
- [ ] Upstream filings (SC9) in `/home/reid/1cfe/sysml-codegen/.project/backlog/BACKLOG.md`: (a) new row — positional parameter redefinition skipping a leading defaulted formal, the four sites with file:line, the research note that the legacy route matched by name; (b) attach the six scalar-function sites to `[SCALAR-FUNCTION-VOCABULARY]` (`:36-41`) as the motivating case; (c) close `[STELLARATOR-D5-MIGRATION]` (`:403-412`) as done by this item; (d) any Phase 1 Class A/B class not in the spec. Committing in that repo is the owner's call; record the diff hunk in the after-record.
- [x] `.project/backlog/BACKLOG.md`: "Test cleanup" row → discharged (link the family spine); "Revert the six scalar-function rewrites" row → point at `models/stellarator_migration_ledger.md` rows and the two calc defs' canonical paths; note to the "generated artifacts" row that the package was regenerated and the after-CSVs sit in `_work/`
- [x] `.project/CURRENT_WORK.md`: package state (2.0.0, stock route), MFE models in `models/`, Item 6 unblocked
- [x] `plan.md` Implementation Notes filled for every phase

### Validation
- [x] Every SC1–SC11 line in `design.md#validation-approach` has a pointer to its evidence (test name, record section, or command output)
- [x] `git status` clean apart from intended changes; no scratch files committed

**What We Know Works After This Phase:**
The item is auditable end to end. Next: `/_my_audit`, then `/_my_pre_pr`.

---

## Risk Management

**See `design.md#potential-risks` for the full list.**

**Phase-Specific Mitigations:**
- **Phase 1** — *unknown refusal class.* Generate to scratch after each repair class, not once at the end, so the first new diagnostic is attributable. A Class C finding stops the item; the ledger row and upstream filing are written before reporting to the owner.
- **Phase 1** — *D-5 tool drift.* Run the transformer from the pinned blob (`git show 8a758e92:…`), not the `84bb83b` checkout; the strip check is the proof either way.
- **Phase 2** — *preservation stubs an impl.* Accessors are edited before regeneration; the log's two preservation decisions are read, and the impl hashes are compared. A stubbed normative file is a failed gate even if the seal is clean.
- **Phase 2** — *symlink resolves into the old worktree.* Convert to relative first; `package_clean` and the `git status` read are meaningless otherwise.
- **Phase 3** — *suffix matching picks the wrong renamed key.* Keys come from `model_contract.json` qualified identities; the manifest records them; `test_known_answers` fixture binding fails first on the new fingerprint, by design.
- **Phase 3** — *drift at a non-baseline point.* The grid join reports the worst deviation per channel; any drift is a finding in the after-record, not a widened tolerance.
- **Phase 4** — *enum change moves the IFE surface.* Three-home sync then exact 23/18 census and both IFE mutations; any change blocks promotion.
- **Phase 5** — *a deletion was load-bearing.* Delete in the order listed and run `tests/study` after each group; the no-retired-identifiers test is the final sweep.
- **Cross-cutting** — *a historical value escapes into a permanent test.* The before CSVs and after-record are documentary; Phase 6's review confirms no test loads them as the expected output of live `models/`.

## Implementation Notes

[TO BE FILLED DURING IMPLEMENTATION]

### Phase 1 Completion
**Completed:** 2026-08-21
**Actual Changes:**
- `tests/models/test_model_family_spines.py` (NEW): MFE generation row + two license-free structural checks (no `in x = x`, no trailing `//` on a formal). 3/3 pass; confirmed failing on the unrepaired tree first.
- `exploration/stellarator_e2e/models/` (13 of 14 files; the three shared files `cas_hierarchy`, `costed_component`, `economic_parameter` untouched): D-5 rename of 66 formals (99 binding sites, 95 declaring formals; transformer run from the pinned blob `765dccad`, preconditions clear, strip check 0 problems); 4 formal reorders (D13); 174 declaration-line comments moved above their declaration (101 formals + 73 plant/design attributes); `'DT Fusion Power'` and `'Levelized Replacement Cost'` bodies made opaque with the formulas carried in the calc docs (D2); `—`→`--` and `Σ`→`Sigma` in comment/doc text of the 8 files that contain `//` comments (155 characters).
- `generated/handwritten/…/dt_fusion_power_impl.py`, `…/levelized_replacement_cost_impl.py`: 8 + 4 input reads moved to `_in`; bodies otherwise unchanged, `AUTO_IMPLEMENTED = False`.
- `models/stellarator_migration_ledger.md` (NEW): 11 hand rows + 495 generated rows (A 365 / B 141 / C 0), upstream findings F1–F3, verbatim pre-rewrite bodies (Appendix A/B).
- `tests/models/test_power_balance.py:282-289`: expected formal names follow the rename (the only regression in `tests/models`; 43 passed / 13 skipped after).
- Scratch generation (`gen3`): exit 0, zero diagnostics, `runtime_contract_version 2.0.0`, 147 artifacts, 166 entry points (113 design attributes / 43 library defaults / 10 usage literals), 2 manual functions. Generated input fields carry the `_in` names the handwritten impls now read. CAS28 (`5000000.0`) and `n_mod` (`1.0`) arrive from model source; BOP `power` inputs wire to `pb` outputs; `special_materials_capital` is an in-package computed module feeding both consumers.

**Issues Encountered:**
- Generation fails fast on the first diagnostic class, so each repair class needed its own `generate` run (expression → self-binding → positional → metadata).
- The D-5 transformer's `--formals` input is the list of refused formal names, not sites; derived from codegen's own `SI_SELF_BINDING` census on a scratch copy with the six expression sites neutered (94 in `mfe_plant.sysml` incl. five on one-line multi-binding usages, 5 in `stellarator_plant.sysml`). The earlier textual census of 94 was the regex missing those five.
- **A fifth refusal class, not in the spec's four (ledger F3).** After D14's comment move, `SI_RENDERING_COLLISION` "conflicting projected metadata" persisted. Instrumenting `_Projection._entry_source` showed the CAS72 formal projecting `unit='Manual'` — the first word of a comment two lines *below* it. Root cause in codegen `extraction/feature_metadata.py::_unit_from_source`: the declaration line is located by `cst_node.start_byte` but the file is walked by character count, so multi-byte characters earlier in the file (153 `—`, 2 `Σ`) shift the scanned line by 42–62 bytes. Second mechanism: the first word after `//` on a declaration line is projected as the unit (`'module'`, `'operating'`), so plant/design attributes with trailing comments collide with their consumers too.
- Handled as Class B (toolchain limitation with an equivalent form, filed upstream, revert optional): ASCII punctuation in comment/doc text of the 8 files that contain `//` comments, guarded so no non-ASCII character outside a comment/doc is touched; and D14's move extended from formals to every declaration line. Shared files were left untouched so Phase 4's twin equality is unaffected. **Ruled 2026-08-21 (`/_my_ask_me` Q1): accepted as Class B**; filed upstream as `[UNIT-SCRAPE-BYTE-OFFSET]`, revert row in fusion-tea `BACKLOG.md`. Not an open question.

**Deviations from Plan:**
- D14's premise (trailing comments on formals are the collision source) was incomplete: the source is the scraper's byte/char drift plus its first-word heuristic, on formals *and* attributes. The move was extended to all 174 declaration lines and the ASCII normalization added; design D14 carries a dated note.
- Ledger rows: the plan said 99 D-5 rows; the ledger carries 99 binding rows + 95 declaring-formal rows (the transformer's full write surface), and one row per ASCII-changed line (134) rather than per character.
- The plan's "ledger row count equals changed-site count" check is satisfied as: every non-equal hunk between the post-rename scratch variant and the final tree is either a generated row or one of the 11 hand rows (the generator reports 0 unclassified hunks after the 14 hand hunks are assigned).
- Scratch instrumentation script `dbg_generate.py` and the ledger generators stayed in the scratchpad; nothing migration-only was committed besides the ledger.

### Phase 2 Completion
**Completed:** 2026-08-21
**Actual Changes:**
- `exploration/stellarator_e2e/pkg/stellarator_tea` → relative `../generated` (D10).
- 42 `AUTO_IMPLEMENTED = True` stubs deleted, then `sysml-codegen generate … --overwrite --smart-regen --preserve-handwritten` in place: `Stencils - New: 43, Preserved: 10, Regenerated: 0`; both normative impls byte-identical (`sha256sum -c`). Seal: `2.0.0`, 147 artifacts, 0 differing, `executable_fingerprint bf480f687963…`, `semantic_fingerprint 1be51d890e5e…`, catalog schema 3.0.0. 88 modified / 23 deleted / 20 new files under `generated/` (inventory in the after-record § 1).
- `exploration/stellarator_e2e/stellarator.snapshot.json` recaptured.
- `tests/study/conftest.py`: `stock_simkit_path` fixture (`STOP_PARSER_TEAX_ROOT`, skip-with-reason / `STUDY_REQUIRE_TEAX=1` fails). Era fixtures left in place until Phase 5.
- `tests/study/test_stock_route.py` (NEW, 4 tests): strict stock load returns the sealed fingerprint; relative link inside the worktree; sealed identity == fingerprint with empty glue ledger; the five formerly injected shapes come from model source. 4/4 with `STUDY_REQUIRE_TEAX=1`.
- `exploration/stellarator_e2e/studies/AFTER_MIGRATION_RECORD.md` (NEW): § 1 Identity written; § 2–7 pending.

**Issues Encountered:**
- Stock teax's strict verifier refuses a symlink as the package root (`INVALID_PATH(.)`). The loader therefore takes the resolved `generated/` directory; the relative `pkg/` alias stays for the manifest path and the file-reading tests. Phase 3's study runner must do the same.
- The replacement-cost def's `n_mod` formal keeps its bare name (it was glue-fed, never self-bound); the test's first draft guessed `n_mod_in`.

**Deviations from Plan:**
- The regenerated pipeline file is `pipelines/pipeline.yaml` (codegen's default, same as the IFE package), not the old `mfe_stellarator.yaml`; the design's SC1 command has no `--pipeline-name`, so this is the designed outcome, recorded because manifests and the study runner reference the old name until Phase 3.
- The old era-route tests under `tests/study` now fail against this package by construction (they load `1.0.0` glue semantics); they are deleted or rewritten in Phases 3 and 5, not patched here.

### Phase 3 Completion
**Completed:** 2026-08-21 (two checks deferred to the first commit, see Issues)
**Actual Changes:**
- `exploration/stellarator_e2e/studies/study_route.py` (NEW): the package-owned stock route -- strict loader on the resolved package dir, `expects_constraint_report` from teax's `ships_constraint_report(load_model_contract(...))`, `model_contract_fingerprint` = the contract's `semantic_fingerprint`, sealed identity via `identity.build_sealed`, axes/tie/windows/validity mask/exported columns, `execute_baseline`, `run_design_search`, `run_availability_sweep`. Successor to `promotion_equivalence.py` (deleted in Phase 5).
- `exploration/stellarator_e2e/study/run_design_search.py`: rewritten as a thin `run`/`export` CLI over `study_route`; era `sys.path`, `GlueAwareLoader`, g1/g2/g3 injection, `preflight_checks`, and the pre-capability `verify` subcommand are gone (generic `scripts/study/verify.py` is the verifier). Outputs go to `study/_work/`; the tracked proof-of-life CSVs are never written.
- `exploration/stellarator_e2e/studies/oracle_entry.py`: four entry keys (`R`, `magnet__R0`, `a`, `availability`); CAS27 mapped as an oracle-computed channel; operand bindings follow the catalog's renamed formals; glue surfaces removed.
- `exploration/stellarator_e2e/studies/manifest.json`: re-pinned from the sealed contracts (fingerprints, read set, baseline point, tie, `cas27` objective).
- `tests/study/data/axes.known_answers.json`, `axes.extras.json`, six `*.expected.json`: re-derived on the 2.0.0 package (`test_fixture_binding` failed first on the old fingerprint, as designed); `test_known_answers.py` contract: R/a now 55 modules / 68 channels with `cas27` reachable, availability and interest_rate still reach no constraint, beta still bound-vs-bound.
- `tests/study/conftest.py`: `stock_simkit_session_path`; `test_preflight_gates.py`, `test_verify.py`: fixtures on `study_route` + stock teax; `test_verify.py`: the disclosure assertion flipped to `== []` and `test_cas27_is_compared_and_nothing_is_undisclosed` added.
- Re-targeted to the regenerated package's names: `test_mechanical_failures.py`, `test_read_set_coverage.py`, `test_identity.py`, `test_output_contract.py`, `test_operand_bindings.py` (glue test deleted; the disagreeing-keys rule now exercised through a declared alias, since no two real keys share an oracle input any more), `test_provenance.py`, `test_warnings.py` (3 `__n_mod_in` siblings, not 18 `__n_mod`), `test_valid_empty.py`.
- Evidence: `AFTER_MIGRATION_RECORD.md` § 2–6. Baseline LCOE `275.2642200420774` to all digits, 5/5 verdicts; grid (948) and sweep (19) **byte-identical** to the before CSVs (rel dev 0 on every channel, 0 verdict mismatches); preflight 5/6 (only `package_clean`, see Issues); CAS28 probe moves exactly 12 downstream capital channels, blanket-thickness probe moves 24 incl. CAS27 and leaves `p_fus`/`wall_load` alone.

**Issues Encountered:**
- **Two checks need a git-clean package tree**: preflight's `package_clean` and `verify.py`'s `assert_tree_clean` both refuse while the regenerated package is uncommitted. Everything else in both tools passes (identity, manifest currency, baseline headline 0.0 deviation). Both are re-run after the first commit on the branch and recorded in the after-record § 5/§ 7. Tests that exercise those tool paths (`test_preflight_gates`, most of `test_verify`, `test_common`, `test_generic::untouched`) fail for the same single reason until then.
- Era and stock fixtures cannot share one pytest process: the era tests import `simkit` from the era worktree first, so the stock fixture's module-origin assertion trips (35 errors in a full run). Until Phase 5 deletes the era tests, the stock-route files are run in their own invocation (142 passed across the eleven re-targeted files).
- The D-5 rename changed the *entry-point shape*: one plant-level key per swept attribute (`stellarator_09__stellaris__R` etc.) instead of per-usage fan-out, `discount_rate` instead of four `interest_rate` keys, `recirc_ok__threshold` without the hash infix, and renamed predicate operands. Every consumer (route, oracle seam, manifest, declarations, tests) was resolved from the contract, not by suffix rewriting.
- Stock teax's strict verifier refuses a symlinked package root; the route resolves the path (Phase 2 finding, applied).

**Deviations from Plan:**
- The stock route lives in a new module `studies/study_route.py` rather than inside `run_design_search.py`: the preflight/verify tests need an importable `execute_baseline`/`run_availability_sweep`, which a script cannot offer cleanly. `run_design_search.py` is the CLI over it.
- `run_design_search.py`'s `verify` subcommand was removed rather than rewritten: it read the deleted `system_design.json`, embedded the glue note, and is superseded by the generic verifier the suite already tests.
- The after CSVs turned out byte-identical to the before CSVs, so the "by value" join is stronger than required; the record states both.

### Phase 4 Completion
**Completed:** 2026-08-21
**Actual Changes:**
- Phase 1–3 committed first as `89f78130` (owner: "commit"); then preflight 6/6 (`package_clean` included) and `verify.py` `outcome: pass` -- 7 channels incl. `cas27`, worst 6.3e-16, `not_independently_verified: []`, 5 verdicts re-derived -- recorded in `AFTER_MIGRATION_RECORD.md` § 4/§ 5 (SC4, SC5).
- Promotion: the 14 staged files copied into `models/library/{foundation,cost_structure,analyses}/` and `models/designs/{generic_mfe,stellarator_09}/`; the three-member `economic_parameter.sysml` synchronized into `exploration/ife_e2e/models/` (D9). Canonical now has 22 SysML files; the three shared files are byte-identical in all three homes.
- `tests/model_families.py` (NEW): the family registry -- owned logical paths per family, shared paths, canonical↔twin layout mapping, `materialize_canonical_subset` (D6/D8).
- `tests/models/test_model_family_spines.py`: the full spine (13 tests) -- owned-path coverage, per-family twin equality, shared-file agreement in three homes, layout-collision falsifier, per-family generation + live==snapshot, IFE census (23/18 with the 11+7 sets merged into one, D7; library defaults and usage literals unchanged), MFE census from `tests/models/data/mfe_census.json` (NEW, captured from the sealed 2.0.0 contract and bound to its semantic fingerprint), the two IFE mutations unchanged, two MFE mutations (`cas28_capital` → exactly the two CAS2x rollups; `blanket_t` → exactly `rb.blanket_t_in`). `tests/models/test_self_binding_replacement.py` deleted.
- `tests/test_codegen_teax_acceptance.py`, `tests/test_occurrence_mutation_teax.py`: "primary" is the IFE canonical subset materialized per module through the registry; expectations unchanged; 20/20 with `STOP_PARSER_*` set.
- `tests/models/test_power_balance.py`: `LIBRARY_DIR = models/library`, TEMPORARY note deleted.
- `exploration/stellarator_e2e/STAGED_MODELS.md`: rewritten as the twin's note.
- `tests/study/test_verify.py`: the unresolvable-binding test uses the renamed operand `beta_limit_in` (last stock-route failure).
- Checks: `tests/models` 43 passed / 13 pre-existing skips; `validate models --level 1` passes; ruff clean on all new/changed files (the three pre-existing findings in `test_power_balance.py` untouched).

**Issues Encountered:**
- The IFE census is unchanged by the enum promotion (23/18, same sets), so the new `mfe_divergent` member is inert for IFE (D9 proved).
- The sealed model contract carries no unit field, so the 73 `:>>` redefinition lines in `stellarator_plant.sysml` that still have trailing comments (the Phase 1 move matched `attribute` lines only -- a `\b` after `:>>` never matches) affect nothing sealed; left as is and noted in the ledger header.

**Deviations from Plan:**
- The family registry is a module under `tests/` (`tests/model_families.py`) imported by both the spine and the root acceptance tests, rather than living inside the spine module: the root tests need the same owned-path list and materializer.
- The MFE census is a JSON fixture rather than inline sets: 166 qualified names inline would bury the test; the fixture is bound to the semantic fingerprint exactly like the study known answers.

### Phase 5 Completion
**Completed:** 2026-08-21
**Actual Changes:**
- Deleted whole: `studies/era_adapter.py`, `studies/promotion_equivalence.py`, `tests/study/test_era_pin.py`, `test_accept_set.py`, `test_glue_mapping_agreement.py`, `test_promotion_equivalence.py`, `test_lineage_refusal.py` (era-API mechanism; the stock-route refusal of a store bound to another identity is `test_verify.py::test_a_store_bound_to_another_identity_is_refused`).
- `tests/study/conftest.py`: era section, `emit_identity`/`edit_glue`, `committed_store_path` gone; one session fixture `stock_route_run` (availability sweep + baseline on the stock route) shared by `test_verify.py`, `test_preflight_gates.py`, and the rewritten `test_committed_store.py` (S4 on a stock store). `test_identity.py` synthetic data renamed (`a/route_adapter.py`).
- `run_stellaris.py`: helpers only -- glue-1 (`patch_bop_wiring`), `SYS_DESIGN`/`MFE_PARAMS`, the unused contingency/indirect imports gone; the package is now strict-loaded through `ProvisionalPackageLoader` (link in a scratch dir) with teax from `STOP_PARSER_TEAX_ROOT`; `PIPELINE = pipelines/pipeline.yaml`. `run_stellaris_single.py`: the `[inject]` loop and the glue-1 call gone; 2.0.0 report vocabulary (`full_satisfaction`, `assessed_entry_count`). Run on the sealed package: anchors GREEN, verdict parity PASS, bit-exact vs oracle PASS, CAS72 guard-live PASS.
- `studies/ANNEX.md`: `§ Loader exception and glue` (incl. the deletion condition, now met) and `§ Era pin` removed; "Four sections" with the reason the two optional ones do not exist; `§ Declared ties` and `§ Oracle` re-keyed (one `R` entry point, two published surfaces, 52 mapped / 46 recorded channels, CAS27 compared, usage-prefixed threshold, `_in` operand names). `.claude/skills/run-study/runbook.md`: the four links to the two sections read "when the annex has one".
- `tests/study/test_annex.py`: four-section contract, optional sections must be absent and explained, runbook links to them must be conditional, oracle section must publish two surfaces and compare CAS27.
- `tests/study/test_no_retired_identifiers.py` (NEW): retired identifiers survive only in the named historical records and absence-guards. `pyproject.toml`: `slow` marker removed with the grid test.
- Suites: `tests/study` 245 passed / 1 skipped in one invocation (era and stock fixtures no longer collide); `tests/models` 43/13; root acceptance 20/20; ruff clean on `scripts/study`, `tests/study`, `studies/`, `run_stellaris.py` (`run_stellaris_single.py` keeps its pre-existing E501/E702 style; only the lines I wrote are clean).

**Issues Encountered:**
- **Surfaced, not touched: `exploration/stellarator_e2e/handshake_1costingfe.py`.** The Item 1–4 handshake harness carries its own `patch_bop_wiring(o)` and a 1costingFE injection map (incl. the old CAS27/CAS28/`n_mod` glue keys) and reads `pipelines/mfe_stellarator.yaml` / `inputs/system_design.json`, so it cannot run on the 2.0.0 package and, if it did, would mutate the sealed tree (I6). It is named in neither the spec's SC3 inventory nor the design's retirement boundary, and it belongs to the on-hold Stellarator Demo epic's evidence (`HANDSHAKE_REPORT.md`). Left as is and listed in the sweep's HISTORICAL set. **Ruled 2026-08-21 (`/_my_ask_me` Q2): leave it**, with a HISTORICAL header note and the P3 BACKLOG row "Rewrite handshake_1costingfe.py" for if the demo epic resumes. Not an open question.
- `make_report.py`, `report.html`, `synthesis.md` under `study/` describe the July proof-of-life run (era pin, glue caveats) and are kept as historical evidence, also in the sweep's HISTORICAL set.

**Deviations from Plan:**
- `test_lineage_refusal.py` was deleted rather than rewritten: its claim (a store bound to one identity refuses another) is already held on the stock route by `test_verify.py`, and its mechanism (adapter-source digests) no longer exists.
- The sweep allow-lists three tests that name a retired identifier only to assert its absence (`test_annex.py`, `test_generic.py`, `test_preflight_gates.py`).

### Phase 6 Completion
**Completed:** 2026-08-21
**Actual Changes:**
- Gates run and recorded in `AFTER_MIGRATION_RECORD.md` § 7: `tests/models` 43/13, `tests/study` 245/1 in one invocation, root acceptance 20/20, `uv lock --check` passes, `validate models --level 1` passes, `--complete` Levels 2 and 6 red exactly as on `main` with the offender delta equal to the pre-migration twin's own offenders (zero introduced), lint clean on everything this item wrote, single-point runner green.
- MR-4 review: no ledger row introduces or relocates a value; the two opaque calcs keep Source/Ref/Basis and carry their formulas verbatim.
- Upstream filings written in `/home/reid/1cfe/sysml-codegen/.project/backlog/BACKLOG.md` — left uncommitted **by owner ruling (`/_my_ask_me` Q3: "fine to just write the rows")**; the commit there is the owner's: `[POSITIONAL-FORMAL-REDEFINITION]`, `[UNIT-SCRAPE-BYTE-OFFSET]`, the motivating case on `[SCALAR-FUNCTION-VOCABULARY]`, `[STELLARATOR-D5-MIGRATION]` closed.
- `.project/backlog/BACKLOG.md`: "Test cleanup" discharged; revert row widened to the ASCII normalization and pointed at the ledger rows and appendices; generated-artifacts row annotated; new P3 row for `handshake_1costingfe.py`. The harness itself got a HISTORICAL header note.
- After-record § 8 (ledger by class, SC→evidence map, what is left for the owner); `CURRENT_WORK.md` and spec status updated.

**Issues Encountered:**
- `tests/test_dependency_provenance.py::test_installed_artifacts_are_the_recorded_wheels_and_public_apis` cannot run outside the sealed-runner environment (`STOP_PARSER_AGENTIC_WHEEL` etc.); the other two pass. Not a regression -- the test reads the env and this item touched no dependency.

**Deviations from Plan:**
- Owner decisions taken during `/_my_ask_me` (2026-08-21): F3 accepted as Class B with filings both sides; `handshake_1costingfe.py` left with a note and a BACKLOG row; fusion-tea commits at each phase end, sysml-codegen rows written but not committed.

---

**Status**: Complete
