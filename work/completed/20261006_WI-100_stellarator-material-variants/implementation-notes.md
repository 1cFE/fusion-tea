# WI-100 implementation notes

Implementer: T-015 (2026-09-30). Authority: `design.md` §§ 0–9 (with the review's R1–R6 and the coordinator's A1–A8), `spec.md`, contract r4. Nothing was committed.

## Summary

- The package builds, regenerates to a fixed point, and runs on stock TEAx.
- The reference instance reproduces the WI-080 pin bit for bit, with only the declared delta.
- All 29 WI-100 tests pass, and the spine suite passes with the one registry addition.
- The largest deviation is structural. Codegen refuses two plants in one package (probe P2), so the design's three instances are three packages built from one staged source set (the design's K21 fallback).
- The Nb₃Sn default design refuses to evaluate (design K22). It has no manifest or baseline record yet. The offer policy has to supply the first Nb₃Sn design that evaluates.

## What exists

Model and build (all new):

- `exploration/stellarator_materials/seams/seam_hunks.json`: the 15 value-neutral hunks of § 1.3 (H1a–c, H2a–c, H3, H4a–b, H5a–f) on five staged files. Contingent H6a–b is recorded but not applied, because P1 passed.
- `exploration/stellarator_materials/models/library/analyses/magnet_material_variants.sysml`: the glue calcs, `'Ampere Floor'`, `'Round1 REBCO Magnet System'`, `'Nb3Sn Magnet System'` and `'Staged Cryoplant'` (with A1's `nist_k_a` … `nist_k_i` and A2's `q_nuc_structure` term).
- `exploration/stellarator_materials/models/designs/stellarator_09_materials/{rebco_material.sysml, nb3sn_material.sysml}`: package `stellarator_09_materials`, one material part per file (deviation 2).
- `exploration/stellarator_materials/author_materials_design.py` derives both design files from the staged Stellaris file (`--check` is the drift check). `make_reference_designs.py` writes `reference_designs.json` (the contract § 5 default designs).
- `exploration/stellarator_materials/bodies/`: B1 (`mfe_conductor_current/rebco_conductor_current_impl.py`, the gate), B2 (`mfe_plasma_scaling/conductor_peak_field_impl.py`, the arm slot) and the shape-branch fallback body (`magnet_material_variants/rebco_shape_branch_impl.py`, P4).
- `exploration/stellarator_materials/build.py`: staging, hunks, `syside check`, positional-binding check, generation, body installation, fixed point, snapshot, census and receipts.
- `exploration/stellarator_materials/units/<reference|rebco|nb3sn>/`: `input_models/` (the staged models root), the generated package `stellarator_materials_<unit>_tea/`, one `*.snapshot.json` and `census.json`.

Route, interface and regression (all new):

- `exploration/stellarator_materials/studies/study_route.py`: the unit-scoped route (§ 5.3), `material_flags` (A4) and `failure_texts` (K25).
- `studies/prepare_interface.py` writes `studies/interface_data.py`, `studies/reference/manifest.json` and `studies/rebco/manifest.json`.
- `exploration/stellarator_materials/regression.py` writes the § 1.5 parity check, the baseline points and the preservation receipt.
- `studies/{reference,rebco}/baseline/{package_identity.json, baseline_result.json}`.
- `studies/.gitignore` ignores `**/_work/`, the route's sqlite stores and staging (precedent `exploration/stellarator_e2e/studies/.gitignore`).

Tests and registration:

- `tests/models/test_stellarator_materials.py`: 29 tests (see Tests).
- `tests/model_families.py`: one additive entry, `SOURCE_COLLECTIONS["stellarator_materials"]` (deviation 9).

Evidence:

- `prototype/`: P1–P5 write-ups, sources and generation logs.
- `build/`: per-unit generation, fixed-point, census, snapshot and `syside` logs, `build-hashes.json`, `bodies/B1.diff`, `bodies/B2.diff`, `design-drift-check.log` and `regression/{baseline-parity.json, baselines.json, preservation.json}`.
- `build/` is matched by `.gitignore:4 build/`. It must be force-added, as § 1.2 states (WI-096 precedent). Leave `build/regression/_work/` out; it holds the regression store.

Files in `exploration/stellarator_materials/` that are not mine and that I did not read: `oracle_glue.py`, `oracle-reuse.json`, `oracle-notes.md` and `tests/models/test_stellarator_materials_oracle.py` (the oracle author's); `studies/offer_policy.py`, `studies/declare_cases.py`, `studies/policy-notes.md` and `tests/study/test_stellarator_materials_policy.py` (the policy task's).

## Commands

All commands run from the repository root. `T` stands for `PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit"`.

- Default designs: `.codex-test/run python exploration/stellarator_materials/make_reference_designs.py`
- Design files: `.codex-test/run python exploration/stellarator_materials/author_materials_design.py [--check]`
- Build: `.codex-test/run python exploration/stellarator_materials/build.py [reference] [rebco] [nb3sn]` (all three if none are named)
- Interface and manifests: `.codex-test/run bash -c 'T python exploration/stellarator_materials/studies/prepare_interface.py'`
- Regression and baselines: `.codex-test/run bash -c 'T python exploration/stellarator_materials/regression.py'`
- Tests: `.codex-test/run bash -c 'T python -m pytest tests/models/test_stellarator_materials.py'` (about 5 min)

## Probe outcomes (`prototype/README.md`)

- **P1, cross-part seams: pass.** On all five reads, `pb.p_cryo`, the TF drive, the cold and intercept demands and the rollup's `winding_cost` read the staged producers. H6 is not needed.
- **P2, double retype.** The two sub-part retypes pass. A package holding two or more `'MFE Power Plant'` instances is refused (`REGISTRY_CLASS_NAME_COLLISION`). I took fallback K21: per-instance packages.
- **P3, def-level literals: emitted as entry keys.** These are `rebco_law_enabled`, `inventory_enabled` and K10's `intercept_demand_available`. The route refuses the two final ones (K11).
- **P4, conditional calc: the `if` form is refused** at exact-route validation. I took the design's fallback: an output-only def plus a handwritten body.
- **P5, per-case time: about 1.5 s per plant.**

## Build

- The twin equals canonical for all 42 files (40 SysML and 2 JSON).
- All 15 hunks apply exactly once and reverse to the source bytes.
- `syside check` passes on all three staged trees.
- The positional-binding check finds no out-of-order binding. The only unbound trailing formals in the material units are `(conductor, eps_intrinsic_in)` and `(pack_field, mu0_in)`.
- Each unit regenerates with `--smart-regen --preserve-handwritten` to a fixed point.

Installed bodies per unit:

| Unit | Bodies | Stellarator stubs | Preserved stellarator bodies | Round 1 bodies | Shape branch |
|---|---|---|---|---|---|
| reference | 52 | 44 | 7 + `financial_factors.py` | 0 | 0 |
| rebco | 58 | 44 | 7 + `financial_factors.py` | 5 | 1 |
| nb3sn | 57 | 44 | 7 + `financial_factors.py` | 5 | 0 |

- The 7 preserved stellarator bodies are 3 manual overrides of auto-implementable calcs and 4 inert orphans. Their reasons are in `build-hashes.json`.
- The 5 Round 1 bodies are the unit's own law plus the four common bodies, each with the WI-099 typed adapter.
- The B1 and B2 diffs remove only the old return annotation (B1) and the old return line (B2).

## Regression (`build/regression/baseline-parity.json`)

- **Bit for bit: yes.** The reference was run at the pin's 704 inputs plus the three new keys at their neutral values (`arm_slope 0`, `arm_x_ref 0`, `rebco_law_enabled 1`).
- All 1,352 pin outputs are equal, and none are missing.
- All 67 verdicts are equal, the constraint ids are identical, and the headline is violated in both.
- The one added output is `magnet__conductor_current__evaluation_defined = 1.0`.
- Protected paths are unchanged: 76,581 files hashed before and after (`preservation.json`), and `git diff --stat` on `models/`, `exploration/stellarator_e2e/` and `exploration/magnet_materials/` is empty.

## Interface and baselines

- **Reference:** 707 entry keys (the 704 pin keys plus the 3 new keys), 1,353 channels and 67 constraints. A proposal can only restate the pinned baseline.
- **REBCO:** 764 entry keys, 762 in the baseline point. The partition classes are: removed (final) 2, named calc-usage 1, varied 200, new variant 40, new administrative 2, held plant 519. 4 constants are not keys. The package has 1,429 channels and 73 constraints.
- **Nb₃Sn:** the same classes, with named 2, new variant 39 and 5 constants.
- The route refuses keys outside the unit, other-unit prefixes, changed reference values, the final keys, and a Nb₃Sn proposal without `eps_intrinsic_in` (K6).

Baseline LCOE at the manifest point:

- **Reference:** 318.7377471541504 (the pin value). Violated checks: divertor_heat, facility_occupancy, reference_conductor_current, tbr, water_electric_capacity and wp_fit, as pinned.
- **REBCO basis bridge:** 412.4334208430638. Violated checks: the six above plus acceptance_ok (expected at the bridge) and pack_area_ok (K15 boundary; see deviation 5).
- **Nb₃Sn default:** it refuses with `EvaluationFailed: module_execution: ValueError: nonpositive IHX terminal approach`. The 4.3 T axis with the Stellaris plasma raises fusion and thermal power until the IHX has no terminal approach. This is design K22.

## Tests

`tests/models/test_stellarator_materials.py`: **29 passed** (287 s). The spine suite `tests/models/test_model_family_spines.py` passed 15 of 15 with the registry addition (507 s).

Design test to test functions:

- **1:** reference bit for bit, and protected paths (2).
- **2:** gate at 0 and at 0.5, both [direct] on the reference, and the route's refusals (3).
- **3:** arm at slope 0, [direct], bitwise over 3 random (R, wp_side) draws × arm_x_ref ∈ {0, 35.278, 1e3}; and the arm on REBCO, 24.89987 T with the sign check (2).
- **4:** (a) pipeline wiring and values; (b) the pin map at η 0.20, with A1's conduction at 590.28 W; (c) Green η; (d) bridge parity (4).
- **5:** acceptance for both materials, pack area, fit, capacity (one list step), copper and steel, and the Ampère pair at R 22 m and peak_ratio 2.12 with wp_side 0.46 violated and 0.50 satisfied, binding at about 0.48 m (6).
- **6:** turn current ±10 % (1).
- **7:** unsupported status for Nb₃Sn at 15.03 T and REBCO at 26.03 T, and the domain refusal as a failed case with its text (2).
- **8:** Stellaris Table 7, and EU DEMO layer 1 with all outputs finite (2).
- **9:** pack-share identity (1).
- **10:** build receipts (1).
- **11:** REBCO band edges, Nb₃Sn strain separation, and the Nb₃Sn 13.08 T envelope flag, which also checks A4 `extrapolated` (3).
- **12:** isolation and baseline replay (1; deviation 7).
- **13:** decomposition closure on all three units, with each rollup's operand set checked against the generated pipeline (1).

Test 4(d) compares 1,266 REBCO channels bit for bit against the reference. It skips channels whose producer descends in the generated pipeline from an edited producer or a changed supplied value: 126 of 290 modules (review R6). None of the compared channels moved.

## Coordinator amendments

None conflicted with what was built.

- **A1 (applied):** `nist_k_a` … `nist_k_i` on `'Staged Cryoplant'`; `Cryoplant::k_c` stays on `'Staged Static Loads'`. Test 4(b) asserts 590.28 W conduction.
- **A2 (applied):** the static loads take `q_nuc_structure_in`, `m_support_in` and `rho_structure_in` from the plant attributes the reference cryoplant reads. The staged cold stage reads the effective nuclear density. The term is zero at the pin.
- **A3:** the structure-mass tolerance is a recorded-design check owned by the glue oracle and policy. The package does not assert it.
- **A4 (applied):** in `material_flags`, Nb₃Sn `extrapolated` is status 2 or 3 and `unsupported` is status 0. REBCO bands come from B_peak.
- **A5:** the B2 `ratio ≤ 0` guard is as built.
- **A6 (applied):** the REBCO bridge count is `1.5 × parallel_tapes_set` = 170.6090085287847.
- **A7, A8:** ownership notes; nothing to build.

## Deviations from the design, with reasons

1. **Three packages, not one (K21, P2).** The units are `stellarator_materials_{reference,rebco,nb3sn}_tea`, from one staged source set. A case names one unit and evaluates one plant. This produces three snapshots, censuses and seam pins; the coordinator's integration runs once per unit.
2. **Two design files, not `materials_plant.sysml`.** Both parts in one file would put two plants in each material package. Each file is package `stellarator_09_materials` holding one part, and each material unit stages the twin without the Stellaris file (41 twin files plus 3 added).
3. **The Nb₃Sn default uses 147 turns, not 149.** The contract § 5 rules reach a fixed point. At `coil_t` 0.3 m they give 149 turns and `coil_t` 0.6 m. At 0.6 m the bore factor gives 147 turns, and `coil_t` stays 0.6 m. B_peak is 12.074 T (`reference_designs.json` diagnostics).
4. **The Nb₃Sn default refuses (K22), so there is no Nb₃Sn manifest or baseline record.** The interface was discovered at the Stellaris 308 turns (`discovery_point_overrides`) and records `baseline_refusal`. K22's regeneration from the first policy-recorded design is left to the policy and study. The K21 split removes K22's coupling, so REBCO cases run regardless. The Nb₃Sn tests use a test plasma density `n_e0 = 4.0e20`, at which the default plant evaluates. It is a test setting, not a design.
5. **The REBCO bridge count follows A6 (170.61), not § 2.10's 169.06.** The Table 7 test runs at 169.06 (1.5 × `parallel_tapes_reference`) and reproduces 420.779220779 mm² to 1e-6. At the bridge default, the gross area is 421.1255 mm², so `pack_area_ok` is violated by 0.35 mm² per turn. This is the 0.991 factor, reported, not absorbed.
6. **No `oracle_entry.py`.** The oracle is the separate author's. Both manifests name `exploration.stellarator_materials.studies.oracle_entry.evaluate`, with a note that the coordinator binds it (WI-099 precedent, L-004 finding #2).
7. **Test 12 (D4 witness) is replaced.** With one plant per case, the unselected instance never runs. The test asserts that a REBCO proposal carrying an Nb₃Sn key is refused, and that the REBCO baseline record replays bit for bit.
8. **Test 8 uses 7.3465 MA.** With 70 turns × 104,950 A at the Nb₃Sn geometry, B_peak is 12.068 T, not the design's "about 11.9 T". The layer 1 figure is asserted on `area__net_area` = 68 × 37.9 = 2,577.2 mm² to 1e-6, with the copper and steel supplied at their rule values, the steel B-scaling at 0 and misc 1.1077 mm²/kA.
9. **Registry.** § 1.1 says `tests/model_families.py` needs no registration, and § 1.4 lists it as protected. The brief directs one additive registration. `SOURCE_COLLECTIONS` paths must exist under `models/` (`assert_canonical_ownership`). So the entry lists only the canonical inputs the build stages: `MFE.owned` plus `analyses/magnet_conductor_alternatives.sysml`. The two new SysML files live in the package tree and cannot be registered there without failing gate 5. Test 1 accepts only this additive diff.
10. **`build.py` has no `--regression` flag.** Step 5 is `prepare_interface.py` followed by `regression.py`, because both need the sealed teax path.

## Unverified

- The glue oracle and the downstream composition (§ 6.3) are not run here, because they belong to the oracle author.
- The integration seam is not run, so no CANDIDATE pin exists for any unit.
- There is no evaluating Nb₃Sn design at the Stellaris plasma. Any Nb₃Sn result depends on the policy's first recorded design.
- Policy acceptance (§ 6.2) and the policy test module are not run.
- `tests/models/test_magnet_materials.py` (Round 1) was not re-run. The regression's preservation hashes show `exploration/magnet_materials/**` unchanged.
