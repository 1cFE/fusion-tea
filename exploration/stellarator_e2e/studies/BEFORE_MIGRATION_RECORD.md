# Before-migration record — `stellarator_tea` on the era route

**Captured:** 2026-08-21, on branch `feat/stellarator-mbse-demo` at `d992647f` (after the merge of `main` `ebe4d376`), in the worktree `~/1cfe/fusion-tea-stellarator-mbse-demo`. Every number below was produced in that session by the command shown above it. Nothing is quoted from an older record.

**Purpose.** The "before" half of the migration's before/after evidence. The migration PR regenerates this package on the pinned codegen + teax main and retires `era_adapter.py`; its "after" must match this record **by value** (entry-key names are expected to move with the D-5 rename, so compare by point and channel, not by column name or CSV bytes). The "after" bars are listed in `.project/research/20260820-221835_stellarator-demo-reconciliation-plan.md` § 5.

---

## 1. Identity

```
git rev-parse --short HEAD                                   → d992647f
git -C /home/reid/1cfe/teax-v1-era rev-parse --short HEAD    → fa0e06a
```

| Fact | Value | Source |
|---|---|---|
| Package `executable_fingerprint` (sealed) | `ad9120413ebda3770f0e8de2eef39711b9bc931b5e141748d912b4baa60ffa2d` | `generated/contracts/package_contract.json` |
| `runtime_contract_version` / `generator_version` | `1.0.0` / `0.1.0` | same |
| Sealed artifacts | 139 | same, `len(artifact_hashes)` |
| Artifacts differing from their sealed hash (recomputed this session) | **2**: `inputs/system_design.json`, `pipelines/mfe_stellarator.yaml` | sha256 of each artifact vs `artifact_hashes` |
| Model `semantic_fingerprint` | `c9bc164050f0aac8a2009befb34497426d68923066ca1c1783a0b80e8048c261` | `generated/contracts/model_contract.json` |
| `catalog_schema_version` | `2.0.0` | same |
| Effective executable fingerprint (era adapter, this session) | `cf877bf94dfa3c650d71cb0629f697ce0afa5363cd178a68fa9d77e0bf14f9cf` | `package_identity.json` from `promotion_equivalence.execute_baseline()` |
| Allowed-modified digests | `system_design.json` `b415087d…`, `mfe_stellarator.yaml` `8118a19c…` | same |
| Adapter source digests | `era_adapter.py` `1ccb220a…`, `oracle_entry.py` `d423036c…`, `verify_stellaris.py` `ba98cbf0…` → `adapter_source_digest` `7d7eb379…` | same |
| Generated with (from records, not reproduced) | sysml-codegen `06d95f8`, teax `07eb0ac` (WI-029, 2026-07-25) | `work/completed/20260802_WI-029_handshake-lcoe-construction/plan.md:475-480, 513` |
| Era execution pin | teax `fa0e06a` at `/home/reid/1cfe/teax-v1-era`, asserted on every load | `studies/era_adapter.py`, `ANNEX.md` § Era pin |

## 2. Proof-of-life CSVs

```
sha256sum study/design_search_R_a.csv study/availability_sweep.csv
0f248b83c104ee69b7ffa63c507d0be82be029b7e64def4a3d80e10166b8022b  study/design_search_R_a.csv
9239bbcd7179ee39a9f187470757ae0389b5e9e1a99efd71d888ce0d50111a70  study/availability_sweep.csv
wc -l  → 949 (948 points + header) / 20 (19 points + header)
```

Both reproduced byte-for-byte this session by `tests/study/test_promotion_equivalence.py` (`-m slow`, 948-point grid, 2:15).

## 3. Verification summary (`study/verification_summary.json`)

| Field | Value |
|---|---|
| `sampled_rows_per_study` | 12 |
| `seed` | 20260816 |
| `sampling` | stratified by verdict combination, remainder random |
| `channels_checked` | 5 |
| `tolerance` | 1e-09 |
| `worst_channel_rel_dev` | 5.672432746546722e-16 |
| `verdicts_rederived` | true |
| `package_git_clean` | true |
| `glue_note` | "glue-fed inputs (CAS27 per-point, cas28, n_mod) identical by construction on both sides; not independently verified" |

## 4. Baseline point — executed this session through the era route

Command (from `exploration/stellarator_e2e/`, era simkit on `sys.path`):
```python
import promotion_equivalence as pe; pe.execute_baseline(out_dir)   # writes package_identity.json + baseline_result.json
```

Point (manifest `baseline.point`): `R = 12.7` (`geom__R`, `rb__R`, `magnet__R0`), `a = 1.3` (`geom__a`, `rb__a`), `availability = 0.85` (`cas72_calc`, `fuel_calc`, `lcoe_calc`, `lcoe_1cfe_calc`).

| Channel | Value |
|---|---|
| `stellarator_09__stellaris__lcoe_calc__lcoe` (headline) | **275.2642200420774** — equals the manifest pin to all digits |
| `stellarator_09__stellaris__total_capital__total_capital` | 16129706216.036476 |
| `stellarator_09__stellaris__cas90_1cfe_calc__cas90` | 1667006326.5334673 |
| channels recorded | 47 |

Verdicts (all five `satisfied`):

| `source_local_identity` | definition | `constraint_id` prefix |
|---|---|---|
| `beta_ok` | `mfe_viability::'Beta Limit'` | `…beta_ok__82b78aad420730d5` |
| `net_positive` | `mfe_viability::'Net Power Positive'` | `…net_positive__484521d56c02667a` |
| `recirc_ok` | `mfe_viability::'Economic Recirculating Threshold'` | `…recirc_ok__afc3be66f0a3421b` |
| `tbr_ok` | `mfe_viability::'TBR Floor'` | `…tbr_ok__2cd198f674d413e4` |
| `wall_load_ok` | `mfe_viability::'Wall Load Limit'` | `…wall_load_ok__ab2c790419af…` |

The independent oracle's anchors (`run_stellaris_single.py:77`: total capital 16,129,706,216.04 / LCOE 275.264220) agree with the above to the recorded digits.

## 5. Suites on this tree (Phase 3 of the landing plan)

| Suite | Command | Result |
|---|---|---|
| `tests/models` (licensed) | `uv run python -m pytest tests/models -q` | 40 passed / 13 skipped (13 = pre-existing WI-026 "types/units/materials not found" skips + 1 template) |
| spine test | `tests/models/test_self_binding_replacement.py -v` | 10/10 passed |
| `tests/study`, era required | `STUDY_REQUIRE_ERA=1 uv run python -m pytest tests/study -q` | 273 passed, 0 skipped (3:02) |
| grid lane | `… -m slow` | 1 passed (2:15) |
| lint | `uv run ruff check scripts/study tests/study` | clean |

## 6. Known gaps carried forward

- **g3 CAS27** (`special_materials_capital`) is fed identically to the package and the oracle, so oracle parity verifies the arithmetic *given* that value; the ingredient itself is not independently verified (`ANNEX.md` § Loader exception and glue; `verification_summary.json` `glue_note`). On the regenerated package this is computed in-package, so the "after" is the first independent check of it.
- `p_fus` and `magnet_capital` are not compared by generic `verify.py` (`ANNEX.md` § Oracle).
- The committed proof-of-life stores under `study/_work/` carry the *sealed* fingerprint, which the era route never earned; `verify.py` refuses them by design.

## 7. What "after" must match

By value, on the stock route (codegen `8a758e92` via fusion-tea's pin, teax main `744745f`), with `era_adapter.py` deleted:

1. Stock `ProvisionalPackageLoader(..., strict=True)` accepts; seal reads `runtime_contract_version 2.0.0`; zero artifacts differ from their sealed hashes.
2. Baseline headline within rel 1e-9 of **275.2642200420774**; the same five verdicts `satisfied`, matched by `source_local_identity`.
3. 948-point grid and 19-point sweep: per-point LCOE and verdicts equal to § 2's CSVs by value (rel < 1e-9), keyed by (R, a) / availability.
4. `verify.py` stratified oracle parity at rel < 1e-9 with an empty `not_independently_verified` list.
5. A mutation proof in the spine-test pattern: move one input (e.g. `cas28_capital`), exactly the expected modules react.
