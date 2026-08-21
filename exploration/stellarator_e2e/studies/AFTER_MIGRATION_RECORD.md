# After-migration record — `stellarator_tea` on the stock route

**Captured:** 2026-08-21, on branch `feat/stellarator-model-migration` (base `main` `7ee0c22a`, working tree at `d04ed5bb` plus the uncommitted migration edits), in `~/1cfe/fusion-tea`. Every number below was produced in that session by the command shown beside it. This is the "after" half of `BEFORE_MIGRATION_RECORD.md`; § 7 of that file lists the bars. Comparison is **by value** (entry keys moved with the D-5 rename).

**Not a live oracle.** This file is committed evidence for the migration (design D12, D15). No test loads it as the expected output of the living `models/` tree.

---

## 1. Identity (plan Phase 2)

```
git -C /home/reid/1cfe/teax rev-parse --short HEAD           → 744745f
sysml-codegen                                                 → 8a758e92 (fusion-tea pin, pyproject.toml:37; the installed package)
uv run sysml-codegen generate --models exploration/stellarator_e2e/models --output exploration/stellarator_e2e/generated \
    --package-name stellarator_tea --overwrite --smart-regen --preserve-handwritten   → exit 0, zero readiness diagnostics
```

| Fact | Value | Source |
|---|---|---|
| `runtime_contract_version` / `generator_version` | `2.0.0` / `0.1.1` | `generated/contracts/package_contract.json` |
| Package `executable_fingerprint` (sealed) | `bf480f687963b7f89a70fb3d36cfca230745f3ec8bd0755a28cc5212782c7049` | same |
| Sealed artifacts | 147 | same, `len(artifact_hashes)` |
| Artifacts differing from their sealed hash (recomputed) | **0** (before: 2) | sha256 of each artifact vs `artifact_hashes` |
| Model `semantic_fingerprint` | `1be51d890e5e2f973da919a9ff3cb5ef04a75652e5f906f13cea2a519f97b3aa` | `generated/contracts/model_contract.json` |
| `catalog_schema_version` | `3.0.0` | same |
| Entry points | 166 (113 design attributes / 43 library defaults / 10 usage literals) | same, `parameters` |
| Manual functions | 2 — `'DT Fusion Power'`, `'Levelized Replacement Cost'` | `generated/IMPLEMENTATION_BACKLOG.md` |
| Smart-regen preservation | `Stencils - New: 43, Preserved: 10, Regenerated: 0`; the two normative impls byte-identical to their pre-regeneration state (`dt_fusion_power_impl.py` sha256 `30aee9ecd9820a24…`, `levelized_replacement_cost_impl.py` `61f4f02147ee90b5…`), `AUTO_IMPLEMENTED = False` | generation log; `sha256sum -c` |
| Stock strict load | `ProvisionalPackageLoader(package_dir=<resolved generated/>, package_name="stellarator_tea", strict=True).load()` returns the sealed fingerprint; the verifier refuses a symlink as package root, so the loader takes the resolved directory and `pkg/stellarator_tea` (now relative, `../generated`) stays the manifest/test alias | `tests/study/test_stock_route.py` |
| Study identity | `scripts.study.identity.build_sealed(...)` digest == sealed executable fingerprint; no allowed-modified files, no adapter sources, empty glue ledger | same |
| Formerly injected values | CAS28 `5000000.0` and plant `n_mod` `1.0` are shipped inputs from model source; `special_materials_capital` (CAS27) is an in-package computed module feeding both CAS2x rollups and is not an input; the four BOP `power` inputs read `pb` outputs; no plant-level `p_th`/`p_the`/`p_et` fillers | same |
| Package layout changes vs the `1.0.0` seal | pipeline file is `pipelines/pipeline.yaml` (codegen default; was `mfe_stellarator.yaml`); input groups are `mfe_plant_params`, `stellarator_plant_params`, `mfe_account_costs_params`, `mfe_magnet_cost_params`, `mfe_plasma_scaling_params` (`system_design.json` is gone); the generic-plant capital rollups moved from `modules/stellarator_09/stellaris/` to `modules/mfe_plant/mfe_power_plant/` | `git status exploration/stellarator_e2e/generated` |
| Snapshot | `exploration/stellarator_e2e/stellarator.snapshot.json` recaptured from the repaired tree (`capture_instance_graph_snapshot`) | same |
| Model edits | `models/stellarator_migration_ledger.md` (A 365 / B 141 / C 0) | ledger |

## 2. Baseline point (plan Phase 3)

Command (repository root, `STOP_PARSER_TEAX_ROOT=/home/reid/1cfe/teax`, teax `744745f`):
```python
import study_route; study_route.execute_baseline(out_dir)   # writes package_identity.json + baseline_result.json
```

Point (manifest `baseline.point`, re-pinned from the sealed contract): `stellarator_09__stellaris__R = 12.7`, `stellarator_09__stellaris__magnet__R0 = 12.7` (declared tie), `stellarator_09__stellaris__a = 1.3`, `stellarator_09__stellaris__availability = 0.85`. One plant-level key per swept attribute since the D-5 rename (the era route's per-usage fan-out keys `geom__R`/`rb__R`, `cas72_calc__availability`, … no longer exist).

| Channel | Value | Before-record |
|---|---|---|
| `stellarator_09__stellaris__lcoe_calc__lcoe` (headline) | **275.2642200420774** | 275.2642200420774 -- equal to all digits |
| `stellarator_09__stellaris__total_capital__total_capital` | 16129706216.036476 | 16129706216.036476 -- equal |
| `stellarator_09__stellaris__cas90_1cfe_calc__cas90` | 1667006326.5334673 | 1667006326.5334673 -- equal |
| `stellarator_09__stellaris__special_materials_capital__special_materials_capital` (CAS27, in-package) | 23815042.059888843 | glue-fed on the era route |
| channels recorded | 48 | 47 (+1: CAS27) |

Identity: `package_identity.json` kind `sealed`, digest `bf480f687963b7f89a70fb3d36cfca230745f3ec8bd0755a28cc5212782c7049` == the sealed `executable_fingerprint`; the baseline case ran under exactly that digest (`executed_under.identity_digest`).

Verdicts (all five `satisfied`, matched by `source_local_identity`): `beta_ok`, `net_positive`, `recirc_ok`, `tbr_ok`, `wall_load_ok`.


## 3. Grid and sweep equivalence (plan Phase 3)

Command: `study_route.run_design_search(out)` (948 points, 132 s) and `study_route.run_availability_sweep(out)` (19 points, 3 s) into a scratch directory; the tracked proof-of-life CSVs under `study/` were not written. Comparison: a one-time scratch script joined before (tracked `study/*.csv`, sha256 as recorded in `BEFORE_MIGRATION_RECORD.md` § 2) and after by physical coordinate -- `(R, a)` for the grid, `availability` for the sweep -- and compared every numeric column and every verdict column per point. The script is not kept (design D12/D15); its output is this table.

| Study | Points joined | Worst rel dev, LCOE | Worst rel dev, any of 8 channels | Verdict mismatches | Byte-identical to the before CSV |
|---|---|---|---|---|---|
| `design_search_R_a.csv` | 948 | 0.0e+00 | 0.0e+00 | 0 | **True** (after sha256 `0f248b83c104…` == before `0f248b83c104…`) |
| `availability_sweep.csv` | 19 | 0.0e+00 | 0.0e+00 | 0 | **True** (after `9239bbcd7179…` == before `9239bbcd7179…`) |

Channels compared per point: lcoe, wall_load, p_fus, plasma_volume, total_capital, magnet_capital, overnight_capital, lcoe_1cfe; verdicts: beta_ok, net_positive, recirc_ok, tbr_ok, wall_load_ok, feasible. The bar was rel < 1e-9 by value; the result is bit-for-bit equality of every exported number and verdict at every point. Every Class A and Class B edit in the ledger is therefore numerically inert over the whole accepted study space, not only at the baseline (bet B1).


## 4. Verification summary (plan Phase 3; run after the Phase 1–3 commit `89f78130`)

```
PYTHONPATH=$STOP_PARSER_TEAX_ROOT/packages/teax-simkit uv run python scripts/study/verify.py \
    --package exploration/stellarator_e2e/pkg/stellarator_tea --manifest exploration/stellarator_e2e/studies/manifest.json \
    --identity <out>/package_identity.json --store <out>/_work/stellarator-design-search-ra-v1.db \
    --store <out>/_work/stellarator-availability-sweep-v1.db --out <out>/verification_summary.json
```

| Field | Value |
|---|---|
| `outcome` | `pass` |
| stores | `stellarator-design-search-ra-v1` (948 completed, 12 sampled over 3 verdict strata), `stellarator-availability-sweep-v1` (19 completed, 12 sampled over 1 verdict strata) |
| `channels_checked` | 7: `cas72`, `fuel`, `lcoe_1cfe`, `lcoe`, `cas27`, `total_capital`, `wall_load` -- CAS27 (`special_materials_capital`), `total_capital` and LCOE among them |
| `tolerance` | 1e-09 |
| `worst_channel_rel_dev` | 6.270e-16 (before-record: 5.67e-16) |
| `verdicts_rederived` / `constraints_rederived` | True / `beta_ok` (2), `net_positive` (1), `recirc_ok` (2), `tbr_ok` (2), `wall_load_ok` (2) |
| **`not_independently_verified`** | **`[]`** (before-record: the g3 CAS27 rung) -- SC4 |
| `identity.kind` / digest | `sealed` / `bf480f687963b7f8…` == sealed executable fingerprint |
| `package.git_clean` | True |

The oracle seam (`studies/oracle_entry.py`) is re-keyed to the renamed entry points and the renamed predicate operands (`beta_in`, `beta_limit_in`, `tbr_in`, `tbr_floor_in`, `wall_load_limit_in`); CAS27 is mapped as an oracle-computed channel; the glue surfaces (`GLUE_FED`, `DEAD_FILLER`, `GLUE_VALUE_KEYS`, `glue_values()`) are gone. `tests/study/test_verify.py::test_cas27_is_compared_and_nothing_is_undisclosed` asserts the empty disclosure and the CAS27 comparison.

## 5. Preflight gates (plan Phase 3; run after the Phase 1–3 commit `89f78130`)

```
uv run python scripts/study/preflight.py gates --package exploration/stellarator_e2e/pkg/stellarator_tea \
    --manifest exploration/stellarator_e2e/studies/manifest.json --groups tests/study/data/axes.known_answers.json \
    --identity <out>/package_identity.json --baseline-result <out>/baseline_result.json --out <out>/preflight_results.json
```

Outcome: **`pass`** -- all six gates.

| Gate | Status | Detail |
|---|---|---|
| `declared_keys` | pass | 7 declared keys across 6 groups, all package inputs |
| `sibling_scan` | pass | pass |
| `identity` | pass | kind sealed, digest bf480f687963b7f89a70fb3d36cfca230745f3ec8bd0755a28cc5212782c7049 recomputed from 0 allowed-modified file(s) and 0 declared source( |
| `manifest_currency` | pass | both recorded package fingerprints match the package on disk |
| `baseline_headline` | pass | stellarator_09__stellaris__lcoe_calc__lcoe reproduces at relative deviation 0.000e+00; 5/5 pinned verdicts match |
| `package_clean` | pass | package tree is byte-untouched (git clean) |

Before the commit, `package_clean` alone refused (the regenerated package was uncommitted) -- the gate doing its job; the other five passed on the working tree.

Manifest re-pin (from the sealed contracts, never by suffix substitution): `recorded_provenance` = new executable + semantic fingerprints; `indicator_inputs` recomputed over `contracts/model_contract.json`, the five `inputs/*.json`, `pipelines/pipeline.yaml`; baseline point re-keyed; tie `magnet__R0 rides_with [R]`; objective catalog + `cas27` so generic verification compares CAS27 against the oracle's recompute. `git diff -- scripts/study/` is empty.

## 6. Mutation probes (plan Phase 3–4)

Executed through the sealed package on the stock route as *proposals* (sealed inputs cannot be edited; entry-point values can be supplied per point), each against the baseline proposal in the same study store. "Moved" = the recorded channel value differs from the baseline's.

**`cas28_capital` 5 000 000 → 6 000 000** (SC10, the spine-test pattern's first probe): 12 of 48 channels moved -- exactly the CAS2x rollups and everything downstream of capital: `cas20_capital__cas20_capital`, `cas23_to_28_capital__cas23_to_28_capital`, `cas2x_pre_contingency__cas2x_pre_contingency`, `cas90_1cfe_calc__cas90`, `contingency__cost`, `idc__cost`, `indirect__cost`, `lcoe_1cfe_calc__lcoe`, `lcoe_calc__lcoe`, `overnight_capital__overnight_capital`, `supplementary__cost`, `total_capital__total_capital`. `total_capital` moved by 1471733.333334 (= 1 000 000 × the contingency/indirect/IDC multiplier chain). Physics and geometry channels (`p_fus`, `wall_load`, `geom__V`, `rb__*`, magnet) did not move; all five verdicts unchanged.

**`blanket_t` 0.8 → 0.9** (the nested radial-build probe): 24 of 48 channels moved: `blanket_cost__cost`, `cas20_capital__cas20_capital`, `cas22_capital__cas22_capital`, `cas23_to_28_capital__cas23_to_28_capital`, `cas2x_pre_contingency__cas2x_pre_contingency`, `cas72_calc__cost`, `cas90_1cfe_calc__cas90`, `contingency__cost`, `idc__cost`, `indirect__cost`, `installation__cost`, `lcoe_1cfe_calc__lcoe`, `lcoe_calc__lcoe`, `magnet_cost__capital_cost`, `overnight_capital__overnight_capital`, `powercore_capital__powercore_capital`, `reactor_equipment_subtotal__reactor_equipment_subtotal`, `replacement_cost_per_event__replacement_cost_per_event`, `shield_cost__cost`, `special_materials_capital__special_materials_capital`, `structure_cost__cost`, `supplementary__cost`, `total_capital__total_capital`, `vessel_cost__cost`. CAS27 moved 23815042.06 → 26760625.49 (blanket volume), the outward layers' costs (shield, structure, vessel), the magnet (coil bore `r_coil`), CAS72 (replacement cost per event) and every capital rollup; `p_fus` and `wall_load` did not move (the first-wall area depends on `a + vacuum_t`, not on the blanket); all five verdicts unchanged. A first probe at `blanket_t = 0.80` moved nothing because 0.80 *is* the Stellaris baseline thickness (the generic-plant default is 0.70); the record keeps that as a reminder to read the instance value, not the library default.

The structural every-and-only proofs (consumer port sets read from the shipped pipeline) are the MFE mutations in `tests/models/test_model_family_spines.py` (plan Phase 4).


## 7. Suites (plan Phase 6)

_pending_
