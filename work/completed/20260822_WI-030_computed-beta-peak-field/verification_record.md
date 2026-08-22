# WI-030 verification record (SV-036)

**Date:** 2026-08-21 · **Commit under test:** `ba5c9945` on `feat/run-study-first-consumer` · **Toolchain:** sysml-codegen 0.1.1 at `8a758e92` (fusion-tea pin), stock teax `744745f` (`STOP_PARSER_TEAX_ROOT=/home/reid/1cfe/teax`), 1costingFE `0254385` (cited, not executed) · **Hold-out:** `knowledge/holdout/aries-cs/PROTOCOL.md` sealed; no barred path read.

## 1. Identity

| fact | value |
|---|---|
| semantic fingerprint | `1ca93d0c988c2828bb1ce3fef18be85be86947a296a33b236d77daeb0f1ab860` (was `1be51d89…`) |
| executable fingerprint | `7447efea9f205dc64543a976e6a3c21a9fd468726f2de78aaf8d845e6f2d9a97` (was `bf480f68…`) |
| runtime contract / catalog schema | 2.0.0 / 3.0.0 |
| parameters / outputs / constraints | 173 / 75 / 6 (0 excluded); was 166 / 72 / 5 |
| retired entry point | `stellarator_09__stellaris__beta` |
| new entry points | `n_e0`, `T_e0`, `n_He0`, `alpha_n_e`, `magnet__peak_ratio`, `magnet__B_max` (design attributes); `beta_calc__mu0`, `beta_calc__e_keV` (library defaults) |
| new channels | `beta_calc__beta`, `peak_field_calc__B_peak`, `peak_field_ok__49c6b8228a73cac5__evaluation` |
| constraint ids | `beta_ok__82b78aad420730d5` unchanged; `peak_field_ok__49c6b8228a73cac5` new |
| handwritten impls | `dt_fusion_power_impl.py 30aee9ec…7308`, `levelized_replacement_cost_impl.py 61f4f021…311b` — `sha256sum -c` OK after regeneration |
| snapshot | `instance_graph.fingerprint 3508b4b6c410…` |
| census | `tests/models/data/mfe_census.json`: 173 = 45 library_default + 10 usage_literal + 118 design_attribute |

## 2. Design point (runner `run_stellaris_single.py`, exit 0)

| anchor | executed | expected |
|---|---|---|
| total capital $ | 16,129,706,216.036476 | 16,129,706,216.04 |
| LCOE $/MWh | 275.264220 | 275.264220 |
| p_net MW | 915.081088 | 915.081088 |
| q_eng | 6.606662 | 6.606662 |
| rec_frac | 0.151362 | 0.151362 |
| magnet % / $ | 39.203876 / 6,323,469,946.33 | unchanged |

Verdicts: `beta_ok`, `net_positive`, `peak_field_ok`, `recirc_ok`, `tbr_ok`, `wall_load_ok` — all `satisfied`; `assessed_entry_count = 6`, headline `full_satisfaction`. Oracle bit-exact (rel < 1e-9) on all 16 compared channels including `beta = 0.026834157` and `B_peak = 24.900000000` at reldev 0.00e+00. CAS72 guard-live spot-check PASS.

## 3. SV-036 points (study route `study_route.run_points`, store `study/_work/wi030_sv036/`, oracle parity via `oracle_entry.evaluate`)

| point | overrides | beta | B_peak | LCOE | `beta_ok` (margin) | `peak_field_ok` (margin) | oracle rel (beta, B_peak) |
|---|---|---|---|---|---|---|---|
| A (design) | — | **0.026834157** (−2.77 % vs printed 0.0276) | 24.9 | 275.264220 | satisfied (+0.023166) | satisfied (**0.0**) | 0.0, 0.0 |
| LTS, 9.0 T | `magnet__B_max = 13.0` | 0.026834157 | 24.9 | 275.264220 | satisfied | **violated** (−11.9) | 0.0, 0.0 |
| LTS, 4.69 T | `magnet__B_max = 13.0`, `magnet__B = 4.69` | **0.098816** | 12.975667 | 198.103853 | **violated** (−0.048816) | satisfied (+0.024333) | 0.0, 0.0 |
| LTS, 4.70 T | `magnet__B_max = 13.0`, `magnet__B = 4.70` | 0.098396 | 13.003333 | 198.282880 | violated | violated (−0.003333) — why D6 chose 4.69 | 0.0, 0.0 |
| B (Table 5) | `n_e0 6.89e20`, `T_e0 12.25`, `n_D0 = n_T0 = 2.60e20`, `T_i0 11.64`, `n_He0 0.83e20`, `alpha_n_e 0.6366` | **0.028690626** (+2.10 % vs printed 0.0281) | 24.9 | 274.646940 | satisfied (+0.021309) | satisfied (0.0) | 0.0, 0.0 |

Margins are the generated predicates' `source_margin` evaluated on the recorded channel values (`modules/constraints/predicates.py`); the route's stored verdict objects carry status only. Both beta checks sit inside the ±3.5 % band with the recorded tolerance (helium on the electron exponent: −3.3 %) unexercised. The LTS arm's LCOE drop (275 → 198 $/MWh) at a violated beta is the cost-only illusion this item exists to expose: the cheap magnet set buys a plasma the configuration cannot hold.

## 4. Study capability (after commit `ba5c9945`)

- `preflight.py gates` → `outcome: pass`, 6/6 (`declared_keys`, `sibling_scan`, identity, `manifest_currency` both fingerprints match, `baseline_headline` LCOE reproduces at 0.000e+00 with 6/6 pinned verdicts, `package_clean` git-clean). Document: `study/_work/wi030/preflight_gates.json`.
- `verify.py` → `outcome: pass`; 9 channels at rel < 1e-9 (`beta`, `cas72`, `fuel`, `lcoe_1cfe`, `lcoe`, `B_peak`, `cas27`, `total_capital`, `wall_load`), worst 4.13e-16; six verdicts re-derived (`beta_ok` 2 operands, `net_positive` 1, `peak_field_ok` 2, `recirc_ok` 2, `tbr_ok` 2, `wall_load_ok` 2); `not_independently_verified: []`. Document: `study/_work/wi030/verification_summary.json`.
- Known-answer fixtures re-derived at the new fingerprint; the `B` axis (replacing `beta`) reaches `beta_ok` and `peak_field_ok` as computed-vs-bound, objectives `beta, lcoe, lcoe_1cfe, total_capital`, 21 modules / 21 channels.

## 5. Suites and validation

- `pytest tests/study tests/models tests/test_dependency_provenance.py`: **317 passed, 14 skipped, 1 failed** — the failure is `test_dependency_provenance::test_installed_artifacts_are_the_recorded_wheels_and_public_apis`, `KeyError: 'STOP_PARSER_WHEEL_TARGET'` (an environment variable that test requires; not set in this session; unrelated to WI-030). `tests/study` alone: 262 passed, 1 skipped. `tests/models`: 48 passed, 13 skipped (IFE census 23/18 untouched).
- `agentic-mbse validate --complete models`: L1 0 errors; L2/L6 offender list identical to the Phase 0 baseline (`baseline_validate.txt` vs `phase2_validate.txt`: empty diff). Zero introduced offenders.
- `agentic-mbse status`: SV-036 row parses; only the two pre-existing SV-034/035 `rel dev` warnings.
- MR-3: the new library defs carry only `1.0`/`2.0` arithmetic literals and the two defaulted constants (test `test_new_library_definitions_carry_no_concept_value`); `mfe_plant.sysml` carries no Stellaris value (grep). MR-4: every new Ref resolves — the Table 5 / Table 2 / Fig. 16 image files exist; `defaults.py:605-614`, `tokamak.py:36-40`, `tokamak.py:117-126` carry the cited symbols at pin `0254385`; `analyst-patch-spec-anchors.md line 44` cited only as the retired source.

## 6. Disclosures

- The REBCO ceiling is bound to the Stellaris design value 24.9 T `[OWNER 2026-08-21]`, not 1costingFE's 23.0 T engineering ceiling; the instance doc says so.
- Thermal beta only; the printed ⟨β⟩ may include fast-particle pressure (Table 4 `f_p`), which is the expected sign of the −2.8 % residual.
- 1costingFE's `compute_beta_N` (`tokamak.py:117-126`) is half the standard form; cited as a cross-check with the factor disclosed, not as the Basis.
- `peak_ratio` is the float64 of 24.9/9.0 so the design-point margin is exactly 0.0; the LTS check point is 4.69 T (4.70 T is violated).
