---
Status: implemented (pending /audit-models)
Created: 2026-08-21
Updated: 2026-08-21
Related Artifacts:
  Spec: ./spec.md
  Design: ./design.md
---

# WI-030 Plan: Computed Beta and Conductor Peak-Field Limit

## Source Documents

- **Design (primary):** `./design.md` — approved 2026-08-21. Elements 1–7, decisions D1–D10, Validation Plan, Validation Report.
- **Spec:** `./spec.md` — MR-WI030-1…6, Success Criteria, SV-036 (pending in `modeling_project/VALIDATION_MATRIX.md`).
- **Research:** `knowledge/research/approved/20260821-152108_wi030-computed-beta-peak-field.md`.
- **Epic:** `work/backlog/epic-mfe-cost-modeling.md` (Item 4 lineage).
- **Required Reading:** `knowledge/holdout/aries-cs/PROTOCOL.md` — sealed; no barred path in any phase.

## Design Summary

Two library calcs (`'Volume-Averaged Beta'`, `'Conductor Peak Field'`) and one library constraint (`'Conductor Peak Field Limit'`) are added; the magnet part def gains `peak_ratio` and `B_max`; the generic plant wires both calcs from `magnet.B` and asserts `peak_field_ok`; the Stellaris instance binds six values, rewires `beta_ok` to the computed beta, and drops the bound `beta`. Then the package is regenerated, the oracle and study capability re-pinned, and SV-036 executed. Rationale, sources, and alternatives: design "Design Decisions" and "Research Findings".

**Branch:** this work stays on `feat/run-study-first-consumer` with Item 6's edits `[OWNER 2026-08-21]`. Item 6's design table is settled up at the end; **the model is the source of truth** for the key names (`magnet__peak_ratio`, `magnet__B_max`) and the 4.69 T point `[OWNER 2026-08-21]`.

## Prototype Baseline

The design's prototype lived in the session scratchpad (gone); it is reproduced here from the design's Elements 1–6, which were proven verbatim except for the full doc blocks. Recorded prototype state (design "Validation Report"):

| fact | prototype |
|---|---|
| Generation | exit 0, zero diagnostics, 61 modules |
| Contract | 173 parameters, 75 outputs, 6 constraints / 0 excluded, `beta` absent, `beta_ok` id `82b78aad420730d5` unchanged, `peak_field_ok` id `49c6b8228a73cac5` |
| Study tools | all six predicates parse in `indicators.predicate_operands` |
| Numbers | beta A `0.026834157382368398`, B `0.028690626389808137`; `B_peak(9.0) = 24.9` exactly; margins `0.0` / `−11.9` / `+0.02433` / `−0.00333` |
| Validation | L1 0; L2 5 WARN, L6 5 ERROR — all pre-existing, zero introduced |

Level 4–6 issues to address: **none introduced.** The five L6 errors and five L2 warnings are the migration's standing offenders (capital rollups `mfe_plant.sysml:423/429/540/689`, `.`-operator `:101`, literal-bound `waste`/`fuel_handling`/`other_rpe` inputs); the gate in every phase is "offender list unchanged", not "clean".

## Phasing Approach

Five phases along the item's dependency chain: library definitions → plant and instance usages → regenerated package → oracle, runner, manifest and fixtures → verification record. Library before instances because the plant binds to the new formals; regeneration before the oracle because the constraint ids and channel names come from the contract, never from a guess; fixtures last because every one of them is bound to the new semantic fingerprint and fails first by design. Each phase ends with Levels 1–3 (and the L2/L6 offender diff from Phase 2 on) and the `tests/models` spine tests where they apply.

**Owner checkpoints:** after Phase 2 (the model text, before the package moves) and after Phase 4 (the first commit on the branch is needed before `preflight.py`'s `package_clean` and `verify.py`'s `assert_tree_clean` can pass — commits are the owner's call).

## Validation Strategy

- **Every phase:** `uv run agentic-mbse validate models --level 1` → 0 errors; `uv run agentic-mbse validate --complete models` → L2/L6 offender list equal to the baseline captured in Phase 0 (line numbers may shift; compare messages).
- **Phases 2–3:** `uv run pytest tests/models -q` (twin byte-identity, per-family generation, census).
- **Phase 4:** `STUDY_REQUIRE_TEAX=1 STOP_PARSER_TEAX_ROOT=/home/reid/1cfe/teax uv run pytest tests/study -q`; `preflight.py gates` 6/6; `verify.py` pass.
- **Phase 5:** SV-036 executed row by row; spec Success Criteria ticked with evidence.

Environment: stock teax at `/home/reid/1cfe/teax` (`744745f`); export `STOP_PARSER_TEAX_ROOT=/home/reid/1cfe/teax` for anything that executes the package. Codegen pin `8a758e92` (sysml-codegen 0.1.1 in the fusion-tea venv; `tests/test_dependency_provenance.py` guards it).

---

## Phase 0: Baseline capture (10 minutes)

**Overview.** Freeze the "before" facts every later gate compares against.

**Checklist**
- [x] `uv run agentic-mbse validate --complete models 2>&1 | grep -E "WARN|ERROR" > work/active/WI-030_computed-beta-peak-field/baseline_validate.txt` (expect 5 WARN + 5 ERROR)
- [x] `uv run pytest tests/models tests/study -q` with the teax env exported → record the pass/skip tally (the study tests need `STUDY_REQUIRE_TEAX=1` to not skip)
- [x] `sha256sum exploration/stellarator_e2e/generated/handwritten/mfe_plasma_scaling/dt_fusion_power_impl.py exploration/stellarator_e2e/generated/handwritten/mfe_account_costs/levelized_replacement_cost_impl.py > work/active/WI-030_computed-beta-peak-field/handwritten.sha256` (expect `8d2357…794a9f` and `06fb1a6e…704c`)
- [x] Record the current contract facts: `semantic_fingerprint 1be51d89…`, 166 parameters, 72 outputs, 5 constraints (`contracts/model_contract.json`)
- [x] `git status --short` saved to the implementation notes: the branch already carries Item 6's uncommitted edits; WI-030's file set is listed per phase below so the owner can commit them distinctly

**Gate:** baseline file written; tallies recorded in this plan's Implementation Record.

---

## Phase 1: Library definitions (1 hour)

**Overview.** Add the two calc defs, the constraint def, and the two magnet attributes. No usage changes yet, so the plant still binds the old shape and everything still parses.

**Design reference.** Design "Element 1 — `calc def 'Volume-Averaged Beta'`", "Element 2 — `calc def 'Conductor Peak Field'`", "Element 3 — `constraint def 'Conductor Peak Field Limit'`", "Element 4 — `'Magnet System'` gains two attributes". Use the stencils verbatim (they are the MR-4 text). Key decisions: D1 (calc-then-compare), D7 (exponent semantics in the beta doc), D9 (formal naming, defaults last).

**Files to modify**
- REFINE `models/library/analyses/mfe_plasma_scaling.sysml` — append Elements 1 and 2 after `'Neutron Wall Load'` (before the package's closing brace)
- REFINE `models/library/analyses/mfe_viability.sysml` — append Element 3 after `'TBR Floor'`
- REFINE `models/library/cost_structure/mfe_power_core.sysml` — Element 4 after `cost_per_kAm` (line 90); extend the `'Magnet System'` doc's parameter list with `peak_ratio` and `B_max`
- REFINE `data/traceability_matrix.csv` — three rows
- NEW `tests/models/test_beta_peak_field.py`

**Checklist**
- [x] `'Volume-Averaged Beta'`: doc block (Source/Ref/Basis as in the stencil), 10 bound formals in the stencil order, `mu0` then `e_keV` last with defaults, intermediates `p_e`, `p_fuel`, `p_He`, `p_avg`, `out beta`
- [x] `'Conductor Peak Field'`: doc block, `B_axis_in`, `peak_ratio_in`, `out B_peak`
- [x] `'Conductor Peak Field Limit'`: doc block, `B_peak`, `B_max_in`, predicate `B_peak <= B_max_in`
- [x] `'Magnet System'`: `attribute peak_ratio : Real;`, `attribute B_max : Real;` with their one-line comments above the declaration (not trailing — the unit-scrape rule in `models/stellarator_migration_ledger.md` F3); doc parameter list extended
- [x] MR-3 grep: `grep -nE "[0-9]\.[0-9]" models/library/analyses/mfe_plasma_scaling.sysml` shows, in the two new defs, only `1.0`/`2.0` arithmetic literals and the two defaults; `mfe_viability.sysml` new def has no numeric literal; `mfe_power_core.sysml` none
- [x] Comments and docs ASCII-only (`—`, `Σ`, `≤` are refused by the pinned codegen's unit scrape; write `--`, `Sigma`, `<=`): `grep -nP "[^\x00-\x7F]" <the three files>` → no hits in the new text
- [x] `data/traceability_matrix.csv`: rows for `'Volume-Averaged Beta'` (Source_Document "Stellaris design details (FED 2025) + 1costingFE tokamak.py", Source_Location "Table 5 image page_009_table_0.png; tokamak.py:36-40,117-126", Requirement `MR-WI030-1`, Confidence high), `'Conductor Peak Field'` (Table 2 image; `MR-WI030-2`), `'Conductor Peak Field Limit'` (`defaults.py:605-614`; `MR-WI030-2`), Last_Verified 2026-08-21
- [x] `tests/models/test_beta_peak_field.py` (pattern: `tests/models/test_power_balance.py:95-150`, syside model load + `CalculationDefinition` members): the two calc defs exist in `mfe_plasma_scaling` with exactly the design's formal names in order and `mu0`/`e_keV` declared last; the constraint def exists in `mfe_viability` with formals `B_peak`, `B_max_in`; `'Magnet System'` owns `peak_ratio` and `B_max`
- [x] Copy the three files to the twin: `cp models/library/analyses/mfe_plasma_scaling.sysml exploration/stellarator_e2e/models/analyses/`, same for `mfe_viability.sysml`, and `models/library/cost_structure/mfe_power_core.sysml` → `exploration/stellarator_e2e/models/cost_structure/`

**Validation checkpoint**
- [x] `uv run agentic-mbse validate models --level 1` → 0 errors
- [x] `uv run agentic-mbse validate --complete models` → offender diff vs `baseline_validate.txt` empty
- [x] `uv run pytest tests/models/test_beta_peak_field.py tests/models/test_model_family_spines.py -q` → green (generation still succeeds: the new defs are unused, the plant unchanged)

**Gate:** L1 0, offender diff empty, new test green, twin byte-identical.

---

## Phase 2: Plant wiring and the Stellaris instance (1.5 hours)

**Overview.** Wire the calcs and the sixth assert into the generic plant; bind the Stellaris values; rewire `beta_ok`; delete the bound `beta`. After this phase the model text is final.

**Design reference.** Design "Element 5 — generic plant wiring", "Element 6 — Stellaris instance", "Cross-File Bindings". Key decisions: D2 (magnet-part placement, plant-level assert), D5 (the 16-digit `peak_ratio` literal and why), D7 (exponents), D10 (no defaults on the four new plant attributes).

**Files to modify**
- REFINE `models/designs/generic_mfe/mfe_plant.sysml` — after `alpha_T` (line 182): four attributes, `calc beta_calc`, `calc peak_field_calc`; after `recirc_ok` (line 796): `assert constraint peak_field_ok`
- REFINE `models/designs/stellarator_09/stellarator_plant.sysml` — magnet block (after `coil_markup`, line 147): `peak_ratio`, `B_max` with docs; profile block (after `alpha_T`, line 447): `n_e0`, `T_e0`, `n_He0`, `alpha_n_e` with docs and the block comment; viability block: delete `attribute beta : Real = 0.0276 {…}` (lines 826-830), replace the `// Beta.` comment with the cross-check note, rewire `beta_ok` (`in beta_in = beta_calc.beta;`)
- REFINE the two twins by `cp`

**Checklist**
- [x] `mfe_plant.sysml`: attributes `n_e0`, `T_e0`, `n_He0`, `alpha_n_e` (no defaults; comment above each); `calc beta_calc` with the ten bindings (`_in` names, `in B_in = magnet.B;`); `calc peak_field_calc` (`in B_axis_in = magnet.B; in peak_ratio_in = magnet.peak_ratio;`); `assert constraint peak_field_ok` (`in B_peak = peak_field_calc.B_peak; in B_max_in = magnet.B_max;`)
- [x] MR-WI030-3 grep: no Stellaris value in `mfe_plant.sysml` (`grep -n "5.06e20\|15.40\|0.56e20\|0.596\|2.7666\|24.9" models/designs/generic_mfe/mfe_plant.sysml` → nothing)
- [x] `stellarator_plant.sysml` magnet block: `:>> peak_ratio = 2.7666666666666666 { doc … }` and `:>> B_max = 24.9 { doc … }` with the design's comment blocks (the float64 note; the `[OWNER 2026-08-21]` 23.0 T disclosure)
- [x] `stellarator_plant.sysml` profile block: the four bindings with the design's docs (Table 5 image refs; the `alpha_n_e` derivation; the Fig. 16 corroboration; the Point-B 0.637 note) and the block comment (computed 0.026834 vs printed 2.76 %, tolerance −3.3 %, quasineutrality at the peak)
- [x] `stellarator_plant.sysml` viability block: bound `beta` deleted (`grep -n "attribute beta " …` → nothing); cross-check comment in place citing `analyst-patch-spec-anchors.md line 44` as the retired source; `beta_limit` untouched; `beta_ok` reads `beta_calc.beta`
- [x] Trailing-comment check: every new `:>>` line that carries a value has its comment above or in a `{ doc }` block, never a trailing `//` that names a unit word first (ledger F3)
- [x] ASCII check on both files' new text (as Phase 1)
- [x] `cp` both files to `exploration/stellarator_e2e/models/designs/generic_mfe/` and `…/designs/stellarator_09/`

**Validation checkpoint**
- [x] `uv run agentic-mbse validate models --level 1` → 0
- [x] `uv run agentic-mbse validate --complete models` → offender diff vs baseline empty (the new calcs add no L2 literal-binding warnings because every input is an attribute or chain; the plant adds no derived expression)
- [x] `uv run pytest tests/models -q` → everything green **except** `test_mfe_census_is_the_one_captured_from_the_first_clean_package`, which must fail with "model meaning moved — re-derive" (the designed failure; recaptured in Phase 3). The two MFE mutation tests must stay green
- [x] Scratch generation to confirm the contract before touching the committed package: `uv run sysml-codegen generate --models exploration/stellarator_e2e/models --output <scratchpad>/gen --package-name stellarator_tea --overwrite` → exit 0, no diagnostics; `contracts/model_contract.json`: 173 parameters, 75 outputs, 6 concrete / 0 excluded, `…__beta` absent, the eight new names present, `beta_ok` id `82b78aad420730d5`

**Owner checkpoint:** present the model diff (`git diff -- models/`) before Phase 3.

**Gate:** L1 0; offender diff empty; spine tests green except the census (expected); scratch contract matches the design's Validation Plan.

---

## Phase 3: Regenerate the committed package (1 hour)

**Overview.** Regenerate `exploration/stellarator_e2e/generated/` in place on the pin, preserving the two normative handwritten impls, and recapture the snapshot and census.

**Design reference.** Design "Validation Plan" rows Generation and Contract; "Implementation Checklist" step 3; D4 note (verdict-identity contract closed by the migration audit — read `.project/completed/20260821_stellarator-model-migration/audit.md` SC2 before regenerating and note anything that binds the catalog shape).

**Files to modify**
- REFINE `exploration/stellarator_e2e/generated/**` (regenerated; `pkg/stellarator_tea` is a tracked symlink to `../generated`, unchanged)
- REFINE `exploration/stellarator_e2e/stellarator.snapshot.json`
- REFINE `tests/models/data/mfe_census.json`

**Checklist**
- [x] Read migration audit SC2 (verdict-identity contract); record in the Implementation Record whether it constrains anything here (expected: no — one more row of the same shapes)
- [x] `uv run sysml-codegen generate --models exploration/stellarator_e2e/models --output exploration/stellarator_e2e/generated --package-name stellarator_tea --overwrite --smart-regen --preserve-handwritten` → exit 0, zero readiness diagnostics; note the stencil summary (`New: 2` for the two auto-implemented calcs, `Preserved` includes the two normative impls)
- [x] `sha256sum -c work/active/WI-030_computed-beta-peak-field/handwritten.sha256` → both OK
- [x] `contracts/model_contract.json`: `runtime_contract_version 2.0.0`; 173 parameters; 75 outputs; `constraint_catalog` 6 concrete / 0 excluded; record the new `semantic_fingerprint`, `executable_fingerprint`, and the `peak_field_ok` constraint id (expect `…__peak_field_ok__49c6b8228a73cac5`; if the hash differs, the contract wins)
- [x] `grep -n "AUTO_IMPLEMENTED = True" exploration/stellarator_e2e/generated/handwritten/mfe_plasma_scaling/volume_averaged_beta_impl.py …/conductor_peak_field_impl.py` → both
- [x] `modules/constraints/predicates.py`: `constraint_pred_definition_mfe_viability__conductor_peak_field_limit(B_peak, B_max_in)` present with `_cmp('<=', B_peak, B_max_in)`
- [x] Snapshot: `uv run python -c "from pathlib import Path; from sysml_codegen.snapshot.capture import capture_instance_graph_snapshot; capture_instance_graph_snapshot([Path('exploration/stellarator_e2e/models')], Path('exploration/stellarator_e2e/stellarator.snapshot.json'))"` (the call `tests/models/test_model_family_spines.py:317` makes); confirm `instance_graph.fingerprint` changed and the file is valid JSON
- [x] Census: regenerate `tests/models/data/mfe_census.json` from the new contract — `derived_against_semantic_fingerprint` = new fingerprint, `entry_points` = 173, `by_entry_type` = the classification the test's `_by_entry_type` helper produces (run the helper on the regenerated package rather than hand-editing; the eight new names land under `design_attribute` ×6 and `library_default` ×2)
- [x] Regeneration stability: run the generate command a second time to a scratch dir and `diff -r` against `generated/` ignoring `captured_at`-style timestamps → no semantic difference

**Validation checkpoint**
- [x] `uv run pytest tests/models -q` → all green (census now bound to the new fingerprint; IFE census 23/18 untouched)
- [x] `STOP_PARSER_TEAX_ROOT=/home/reid/1cfe/teax uv run python exploration/stellarator_e2e/run_stellaris_single.py` → anchors GREEN (LCOE 275.264220, total capital 16,129,706,216.04, p_net 915.081088, q_eng 6.606662, rec_frac 0.151362, magnet capital unchanged); the verdict assertion will **fail on the sixth verdict** until Phase 4 updates `EXPECTED_VERDICTS` — record the failure text as evidence that the runner is strict

**Gate:** package regenerated on the pin with the contract facts above; snapshot and census recaptured; `tests/models` green; headline anchors unchanged.

---

## Phase 4: Oracle, runner, manifest, and study fixtures (2 hours)

**Overview.** Make the independent oracle compute the two new channels, teach the operand-binding seam the sixth constraint, re-pin the manifest, and re-derive every fixture bound to the old fingerprint. Ends with the study capability green on the regenerated package.

**Design reference.** Design "Implementation Checklist" steps 4–5; D8 (the `B` axis replaces `beta`); "Validation Plan" rows Study capability and Verdicts.

**Files to modify**
- REFINE `exploration/stellarator_e2e/verify_stellaris.py` — `compute()` adds the beta closed form and `B_peak`; the parameter table gains `n_e0`, `T_e0`, `n_He0`, `alpha_n_e`, `peak_ratio`, `B_max`, `mu0_beta`, `e_keV`
- REFINE `exploration/stellarator_e2e/studies/oracle_entry.py` — `ORACLE_OUTPUT_TO_CHANNEL` + `beta`, `B_peak`; `OPERAND_BINDINGS`: `beta_ok.beta_in` → channel `…beta_calc__beta`; new `peak_field_ok__<id>` row (`B_peak` channel `…peak_field_calc__B_peak`, `B_max_in` input `…magnet__B_max`); `_oracle_overrides` accepts the six new qualified keys
- REFINE `exploration/stellarator_e2e/run_stellaris_single.py` — `EXPECTED_VERDICTS` + `peak_field_ok`; oracle gate list + the two channels
- REFINE `exploration/stellarator_e2e/studies/manifest.json` — `recorded_provenance` (both fingerprints), `indicator_inputs` (digest over the read set, via `scripts/study/manifest.indicator_input_fingerprint`), `baseline.verdicts` + `{"source_local_identity": "peak_field_ok", "expected": "satisfied"}`, `objective_catalog` + `{"name": "beta", "channel": "stellarator_09__stellaris__beta_calc__beta", "note": …}`
- REFINE `tests/study/data/axes.known_answers.json` — `beta` group → `B` group on `stellarator_09__stellaris__magnet__B` (note: reaches `beta_ok` through `beta_calc`, `peak_field_ok` through `peak_field_calc`, and the magnet cost)
- REFINE `tests/study/data/*.expected.json` — re-derive all; `beta.expected.json` → `B.expected.json`
- REFINE `tests/study/test_known_answers.py` — `CASES`, `FIXTURE_CONTRACT` (the `B` row: `no_constraint_response False`, reachable `["beta_ok", "peak_field_ok"]`, objectives `["lcoe", "lcoe_1cfe", "total_capital", …]` as the tool reports, module/channel counts as reported), `EXPECTED_SEMANTIC_FINGERPRINT`, `:112` unreachable count 5 → 6 for the no-response axes, `test_beta_is_a_bound_versus_bound_comparison` → `test_B_reaches_both_field_constraints_through_calcs` (operand classes `["computed", "bound"]`, `bound_vs_bound False`)
- REFINE `tests/study/test_provenance.py:77` — replace the `…__beta` design-attribute assertion with `…__magnet__B_max` (and `…__beta_calc__mu0` as `library_default`)
- REFINE `tests/study/test_verify.py:100` — the re-derived set gains `peak_field_ok`; `:217` keep `beta_ok`'s id
- REFINE `tests/study/test_operand_bindings.py:68,89` — six constraints, eleven `feature_ref` operands
- REFINE `tests/study/test_valid_empty.py:39-40` — six bounds / six unreachable
- CHECK `tests/study/test_single_point_gate.py`, `test_study_publication_fail_closed.py`, `test_policy_path.py` (Item 6's new tests on this branch) for any hard-coded five-verdict or `beta` key assumption; adjust only if they assert on the catalog count

**Checklist**
- [x] `verify_stellaris.py`: `beta = 2*mu0*e_keV*(n_e0*T_e0/(1+alpha_n_e+alpha_T) + (n_D0+n_T0)*T_i0/(1+alpha_n+alpha_T) + n_He0*T_i0/(1+alpha_n+alpha_T))/B**2` with `mu0 = 1.25663706212e-6`, `e_keV = 1.602176634e-16`; `B_peak = B*peak_ratio`; both returned under the names the runner and `oracle_entry` map; Point-A value `0.026834157382368398`, `B_peak = 24.9`
- [x] `oracle_entry.py`: the three edits above; `operand_bindings()` publishes six constraint ids read from the regenerated contract (never composed by suffix)
- [x] `run_stellaris_single.py`: six expected verdicts; oracle gate compares `beta_calc__beta` and `peak_field_calc__B_peak` at rel 1e-9
- [x] `STOP_PARSER_TEAX_ROOT=… uv run python exploration/stellarator_e2e/run_stellaris_single.py` → ANCHORS GREEN, six verdicts satisfied, `peak_field_ok` margin `0.0`, BIT-EXACT PASS on every channel incl. the two new ones
- [x] Manifest re-pin exactly as the migration did (`.project/completed/20260821_stellarator-model-migration/plan.md:269-290`, "3. Manifest re-pin"): fingerprints from the sealed contract, read-set digest recomputed, baseline point unchanged (`R`, `magnet__R0`, `a`, `availability`), headline unchanged, verdicts six, objective catalog + `beta`; `uv run python -c "from scripts.study import manifest; manifest.validate(__import__('json').load(open('exploration/stellarator_e2e/studies/manifest.json')))"` → ok
- [x] Baseline execution: `study_route.execute_baseline(<_work>)` deposits `package_identity.json` and `baseline_result.json`; headline deviation 0.0; six verdicts
- [x] Fixtures: run the indicator tool on the new package with the updated axes file and write each `*.expected.json` from the report (the migration's procedure, `plan.md:532`): `derived_against_semantic_fingerprint` = new fingerprint on every file; `B.expected.json` added; `beta.expected.json` deleted
- [x] Test edits listed above; `grep -rn "stellaris__beta\b" tests/ exploration/stellarator_e2e/studies/ exploration/stellarator_e2e/study/` → no live reference to the retired key (docstrings that describe history may stay)
- [x] `STUDY_REQUIRE_TEAX=1 STOP_PARSER_TEAX_ROOT=… uv run pytest tests/study -q` → green except the two checks that need a git-clean package tree (`package_clean`, `assert_tree_clean`) — they pass only after the owner's commit (migration `plan.md:538`)

**Owner checkpoint:** commit point. The WI-030 file set for the commit: the five model files and their twins, `generated/**`, `stellarator.snapshot.json`, `tests/models/data/mfe_census.json`, `tests/models/test_beta_peak_field.py`, `verify_stellaris.py`, `oracle_entry.py`, `run_stellaris_single.py`, `studies/manifest.json`, `tests/study/data/*`, the edited `tests/study/*.py`, `data/traceability_matrix.csv`, this plan. Item 6's files are not part of it.

**Validation checkpoint (after the commit)**
- [x] `uv run python scripts/study/preflight.py gates --package exploration/stellarator_e2e/pkg/stellarator_tea --manifest exploration/stellarator_e2e/studies/manifest.json --groups tests/study/data/axes.known_answers.json --identity <_work>/package_identity.json --baseline-result <_work>/baseline_result.json` → 6/6
- [x] `uv run python scripts/study/verify.py --package … --manifest … --identity … --store <_work>/<baseline store>.db --out <_work>/verification_summary.json` → `outcome: pass`, `not_independently_verified: []`, six verdicts re-derived, `beta` among the compared channels
- [x] `STUDY_REQUIRE_TEAX=1 … uv run pytest tests/study tests/models -q` → green; IFE anchors untouched (`tests/models` IFE census 23/18)

**Gate:** runner six-for-six at the unchanged headline; manifest validates; preflight 6/6; verify pass; both suites green.

---

## Phase 5: SV-036 verification and close-out record (1 hour)

**Overview.** Execute SV-036 row by row, record the evidence, tick the spec's Success Criteria, and leave the hand-offs where the next sessions will look.

**Design reference.** Design "Validation Plan" (every row), D6 (4.69 T), D3 (DI at close).

**Files to create/modify**
- NEW `work/active/WI-030_computed-beta-peak-field/verification_record.md` — SV-036 evidence in the `AFTER_MIGRATION_RECORD.md` style (identity, baseline point, verdicts, oracle parity, LTS points, suites)
- REFINE `modeling_project/VALIDATION_MATRIX.md` — SV-036 status `pending` → `passing` with the executed numbers appended to the description (as SV-033/035 do), or `failing` with the reason
- REFINE `./spec.md` — Success Criteria checkboxes ticked with evidence pointers
- REFINE `.project/CURRENT_WORK.md` — WI-030 implemented; next `/audit-models`; Item 6 settle-up note (key names and 4.69 T come from the model)

**Checklist**
- [x] **Beta at Points A and B.** Oracle: Point A `0.026834` (−2.77 % of 0.0276); Point B by overriding the eleven Table-5 keys (`n_e0 6.89e20`, `T_e0 12.25`, `n_D0 = n_T0 = 2.60e20`, `T_i0 11.64`, `n_He0 0.83e20`, `alpha_n_e 0.6366`, `n_e 4.21e20`, `p_input 14.77` for the record) → `0.028691` (+2.10 % of 0.0281). Package: one study point per Point through `study_route.run_points` (a proposal dict is any numeric-keyed mapping, `study_route.py:101-106`) → `beta_calc__beta` rel 1e-9 vs the oracle
- [x] **Headline unchanged.** `run_stellaris_single.py` anchors at the design point, to the cent (Phase 4 evidence, re-stated)
- [x] **Six verdicts.** all satisfied; `peak_field_ok` margin `0.0`; `beta_ok` margin `0.05 − 0.026834 = 0.023166`
- [x] **LTS points** through `study_route.run_points` on the committed package: baseline point + `magnet__B_max = 13.0`, `magnet__B = 9.0` → `peak_field_ok` violated (margin −11.9); baseline point + `magnet__B_max = 13.0`, `magnet__B = 4.69` → `peak_field_ok` satisfied (+0.0243) and `beta_ok` violated (beta 0.0988, margin −0.0488); oracle agrees on both at rel 1e-9; also record `4.70` → violated (−0.0033) as the reason for D6
- [x] **Contract facts.** `beta` absent; the six design attributes + two library defaults present; `beta_calc__beta` and `peak_field_calc__B_peak` channels; 173 / 75 / 6
- [x] **Study tools.** preflight 6/6 and verify pass (Phase 4 evidence, re-stated with the run ids)
- [x] **Suites.** `pytest tests/study tests/models` tallies; IFE census and anchors unchanged
- [x] **MR-3 / MR-4 read.** citation-by-citation read of the six instance docs and three library docs: every Ref resolves to an image path or a pinned upstream line; no typical-literature value
- [x] `verification_record.md` written; SV-036 row updated; spec Success Criteria ticked; `CURRENT_WORK.md` updated
- [x] Hand-offs recorded (not executed here): Item 6 design table settle-up (`magnet__peak_ratio`, `magnet__B_max`, 4.69 T — the model is the source of truth); DI candidate text for close (design D3); the `.project/backlog/BACKLOG.md` run-study row already filed

**Validation checkpoint (final, comprehensive)**
- [x] `uv run agentic-mbse validate --complete models` → L1 0; L2/L6 offender list identical to `baseline_validate.txt`
- [x] `uv run pytest tests/models -q` green; `STUDY_REQUIRE_TEAX=1 STOP_PARSER_TEAX_ROOT=… uv run pytest tests/study -q` green
- [x] `uv run pytest tests/test_dependency_provenance.py -q` green (pins untouched)
- [x] `uv run agentic-mbse status` → SV-036 row parses (no new matrix warning beyond the pre-existing SV-034/035 `rel dev` ones)
- [x] Spec acceptance criteria, verified explicitly:
  - [x] `'Volume-Averaged Beta'` and `'Conductor Peak Field Limit'` exist in the library with MR-4 docs; wired in `mfe_plant.sysml`; bound in `stellarator_plant.sysml`
  - [x] `beta` is no longer an entry point; `beta_calc__beta` is a channel; `peak_field_ok` is the sixth constraint
  - [x] Level 1 passes; Levels 2 and 6 offender list unchanged
  - [x] Generation exit 0, zero readiness diagnostics, `runtime_contract_version 2.0.0`
  - [x] `tests/models` and `tests/study` green; IFE census and anchors unchanged
  - [x] Computed beta within ±3.5 % at Points A and B; oracle bit-exact rel 1e-9
  - [x] Design-point headline unchanged to the cent; six verdicts satisfied, `peak_field_ok` margin 0.0
  - [x] `B_max = 13.0`: `B = 9.0` violated; `B = 4.69` satisfied with `beta_ok` violated
  - [x] `preflight.py gates` 6/6 and `verify.py` pass on the regenerated package with the re-pinned manifest

**Gate:** SV-036 `passing` with evidence; spec criteria all ticked; suites green. Then `/audit-models` (do not self-certify), then `/status close WI-030` with the DI.

---

## Feasibility Concerns

| concern | mitigation |
|---|---|
| The prototype is gone with the session scratchpad; Phase 1–2 re-type the stencils | The stencils in the design are the proven text; Phase 2's scratch generation re-proves the contract before the committed package is touched |
| `beta_ok`'s catalog id could move (its `beta_in` binding changed from an attribute to a chain) | Prototype kept `82b78aad420730d5`; Phase 3 reads the id from the contract and Phase 4 writes it into `oracle_entry.py` from there, never by assumption |
| Item 6's uncommitted edits share the working tree (`.claude/skills/run-study/*`, `modeling_project/STUDY_POLICY.md`, `tests/study/test_policy_path.py`, …) | WI-030 touches none of those files; the Phase 4 commit list names WI-030's set so the owner can stage it distinctly. If a `tests/study` test of Item 6's asserts on five verdicts, Phase 4's CHECK row catches it |
| `preflight`/`verify` refuse an uncommitted package tree | Known from the migration; the owner's commit is the Phase 4 checkpoint, and both tools re-run after it |
| A study point on `magnet__B`/`magnet__B_max` might be refused by the teax runner if the key is not in the contract's parameter set | Both are design-attribute entry points in the contract (Phase 3 fact); `validate_proposal` accepts any numeric mapping |
| Floating boundary at the design point | D5; margin `0.0` is produced by `_norm0`; verified on the generated predicate in the prototype |
| The unit-scrape defect (ledger F3) projects a trailing comment word as a unit and collides at generation | Phase 1–2 comment-placement rule; the scratch generation in Phase 2 surfaces any collision before Phase 3 |

## Implementation Record

### Phase 0 (2026-08-21)
- `baseline_validate.txt`: 5 WARN (L2 literal-bound `waste`/`fuel_handling`/`other_rpe` inputs) + 5 ERROR (L6 capital rollups `mfe_plant.sysml:423/429/540/689`, `.`-operator `:101`). Note: the validator lists at most five WARN lines per level even with `--verbose`; the gate compares the listed set.
- Baseline tally `pytest tests/models tests/study` (teax env exported): 310 passed, 14 skipped.
- Handwritten sha256 (`handwritten.sha256`): `dt_fusion_power_impl.py 30aee9ec…7308`, `levelized_replacement_cost_impl.py 61f4f021…311b`. **Deviation from the plan text:** the plan quoted the pre-migration values (`8d2357…`, `06fb1a6e…`); the D-5 rename changed both files (ledger "Package-side edits"). The values captured here are the ones to guard.
- Contract before: semantic `1be51d89…`, 166 parameters, 72 outputs, 5 constraints.

### Phase 1 (2026-08-21)
- `mfe_plasma_scaling.sysml`: `'Volume-Averaged Beta'` (12 formals, `mu0`/`e_keV` last) and `'Conductor Peak Field'` appended; `mfe_viability.sysml`: `'Conductor Peak Field Limit'`; `mfe_power_core.sysml`: `peak_ratio`, `B_max` on `'Magnet System'` with the doc list extended. Twins copied. Three traceability rows.
- `tests/models/test_beta_peak_field.py`: 5 tests green. Two adjustments while writing it: the whole library must be loaded (`try_load_model` over `models/library/**`, the `test_power_balance.py` pattern), and a constraint def's formals are not named owned members in syside's view, so that check reads the source text.
- Validation: L1 0; full offender listing = baseline + the two transient "Unused calc def" warnings (expected until Phase 2 wires them; two baseline lines fell out of the five-line display, not out of the tree).
- Pre-existing `—` characters remain in `mfe_viability.sysml:26,31,51` (not in the new text; generation has always passed with them).

### Phase 2 (2026-08-21)
- `mfe_plant.sysml`: `n_e0`, `T_e0`, `n_He0`, `alpha_n_e` (no defaults), `calc beta_calc`, `calc peak_field_calc`, `assert constraint peak_field_ok`. `stellarator_plant.sysml`: `magnet.peak_ratio = 2.7666666666666666`, `magnet.B_max = 24.9`, the four beta referents with docs, bound `beta` deleted and replaced by the cross-check comment, `beta_ok` rewired to `beta_calc.beta`. Twins copied. MR-WI030-3 greps empty.
- Validation: L1 0; offender diff vs baseline **empty** (the unused-calc warnings are gone). `pytest tests/models`: 47 passed, 13 skipped, 1 failed = `test_mfe_census…` with "model meaning moved — re-derive" (the designed failure; Phase 3 recaptures).
- Scratch generation from the twin: exit 0, zero diagnostics; contract 173 parameters / 75 outputs / 6 constraints, 0 excluded; `beta` absent; the eight new names present; channels `beta_calc__beta`, `peak_field_calc__B_peak`; `beta_ok` id `82b78aad420730d5` unchanged; `peak_field_ok` id `49c6b8228a73cac5`; semantic fingerprint `1ca93d0c988c2828bb1ce3fef18be85be86947a296a33b236d77daeb0f1ab860` (identical to the design prototype: the doc text does not enter the fingerprint). All six predicates parse in `indicators.predicate_operands`.
- **Owner checkpoint reached** (model diff presented before Phase 3); owner: "go".

### Phase 3 (2026-08-21)
- Migration audit SC2 read: verdicts are resolved through the catalog's `source_local_identity` (`study_route.py:214-248`) and the route refuses a catalog whose size differs from `EXPECTED_CONSTRAINT_COUNT` — a hard-coded 5 the plan had not listed; bumped to 6 in Phase 4.
- `sysml-codegen generate … --overwrite --smart-regen --preserve-handwritten`: exit 0, zero diagnostics, 62 modules, `Stencils - New: 2, Preserved: 53, Regenerated: 0`; `sha256sum -c handwritten.sha256` OK for both normative impls.
- Contract: catalog schema 3.0.0, runtime contract 2.0.0, 173 parameters, 75 outputs, 6 concrete / 0 excluded; semantic `1ca93d0c988c2828bb1ce3fef18be85be86947a296a33b236d77daeb0f1ab860`, executable `7447efea9f205dc64543a976e6a3c21a9fd468726f2de78aaf8d845e6f2d9a97`; `peak_field_ok` id `…__49c6b8228a73cac5`, `beta_ok` id unchanged. Both new impls `AUTO_IMPLEMENTED = True`.
- Snapshot recaptured (`instance_graph.fingerprint 024f6090… → 3508b4b6…`); census recaptured via the spine test's own helpers: 173 entry points = 45 library_default + 10 usage_literal + 118 design_attribute.
- Regeneration stability vs a fresh scratch generation: only (a) `package_contract.json` sha entries for the preserved normative impls vs scratch stubs, and (b) `SysML Source:` line numbers inside *preserved* stubs (they keep their pre-WI-030 line refs; cosmetic, the migration saw the same). No semantic difference.
- `pytest tests/models`: 48 passed, 13 skipped. Runner: anchors GREEN to the cent (total 16,129,706,216.04; LCOE 275.264220; p_net 915.081088; q_eng 6.606662; rec_frac 0.151362; magnet 39.203876 % / $6,323,469,946.33), six verdicts satisfied, then the runner's own `assessed_entry_count == 5` tripped as predicted.

### Phase 4, up to the commit checkpoint (2026-08-21)
- `verify_stellaris.py`: six new `IN` entries + `beta_mu0`/`beta_e_keV`; `beta` and `B_peak` computed operation-for-operation as the calcs; both returned. `oracle_entry.py`: `ENTRY_KEY_TO_ORACLE_INPUT` + ten keys (the six new ones plus `magnet__B`, `n_D0`, `n_T0`, `T_i0` so Item 6's arm and density keys translate); `ORACLE_OUTPUT_TO_CHANNEL` + `beta`, `B_peak`; `OPERAND_BINDINGS`: `beta_ok.beta_in` → channel, new `peak_field_ok__49c6b8228a73cac5` row. `run_stellaris.py` `CH` + `beta`, `B_peak`; `run_stellaris_single.py`: six verdicts, count 6, two new oracle channels. `study_route.py` `EXPECTED_CONSTRAINT_COUNT = 6`; `run_design_search.py` docstring.
- Runner: ANCHORS GREEN, VERDICT PARITY PASS (6/6), BIT-EXACT PASS incl. `beta` 0.026834157 and `B_peak` 24.9 at reldev 0.00e+00, CAS72 guard PASS, exit 0.
- Manifest re-pinned from the sealed contracts (`recorded_provenance` both fingerprints; `indicator_inputs` digest `00badf7f…` over the seven read-set files — note `manifest.indicator_input_fingerprint` returns `files` as path+sha dicts while the manifest stores paths; converted); `baseline.verdicts` + `peak_field_ok`; `objective_catalog` + `beta`; `manifest.validate` ok. Baseline executed on the stock route (`study/_work/wi030/`): six verdicts satisfied, `beta_calc__beta = 0.026834157382368398` in the channels.
- Fixtures: `axes.known_answers.json` `beta` → `B` (`magnet__B`); all six `*.expected.json` re-derived from the indicator report at the new fingerprint; `beta.expected.json` deleted, `B.expected.json` added. `B` row of the fixture contract: reaches `beta_ok` + `peak_field_ok` (both computed-vs-bound, `bound_vs_bound False`), objectives `beta, lcoe, lcoe_1cfe, total_capital`, 21 modules / 21 channels. No-response axes now see 6 unreachable.
- Tests re-targeted: `test_known_answers.py` (CASES, contract row, fingerprint, `== 6`, `test_B_reaches_both_field_constraints_through_calcs`), `test_provenance.py:77` (`magnet__B`), `test_verify.py:100`, `test_operand_bindings.py` (6 / 11), `test_valid_empty.py` (6 bounds; `beta` joins `objectives_unreachable` for `land_cost`), `test_mechanical_failures.py` (`pipeline.yaml:49` → `:77`, the `rb.inputs.R_in` line moved when two modules were added), `test_output_contract.py` (`B`), `test_subset_flag.py` (`B` sorts first; group selections). Item 6's three new tests needed nothing.
- `pytest tests/study`: **246 passed, 1 skipped, 5 failed, 16 errors — every failure/error is the git-clean gate** (`test_common::git_clean_gate`, `test_preflight_gates::clean_subcommand` + 7 fixture errors, `test_verify` 3 + 9 fixture errors), exactly the pre-commit state the migration recorded (`plan.md:538`). `grep -rn "stellaris__beta\b"` over `tests/`, `studies/`, `study/`: only the retired-key mention in the `B` axis note.
- **Commit checkpoint reached.** File set listed in the turn's report; Item 6's own uncommitted edit (`run_design_search.py` — the docstring line WI-030 also touched) is the one overlap.

### Phase 4, after the commit (2026-08-21, `ba5c9945`)
- Owner committed WI-030's 74-file set (the one overlap, `run_design_search.py`, carried only the docstring line). `preflight.py gates` → pass 6/6 incl. `package_clean` and `baseline_headline` 0.000e+00 with 6/6 verdicts; `verify.py` → pass, 9 channels incl. `beta` and `B_peak`, worst rel 4.13e-16, six verdicts re-derived, nothing undisclosed (note: `verify.py` imports `simkit` at `build_summary`, so it needs `packages/teax-simkit` on `sys.path` — run it with the teax root exported, as the tests do).
- `pytest tests/study tests/models tests/test_dependency_provenance.py`: 317 passed, 14 skipped, 1 failed — `test_installed_artifacts_are_the_recorded_wheels_and_public_apis` needs `STOP_PARSER_WHEEL_TARGET` in the environment (unset here); unrelated to the model.

### Phase 5 (2026-08-21)
- SV-036 executed through the study route at five points (design, LTS 9.0 / 4.69 / 4.70 T, Point B) with oracle parity 0.0 on `beta` and `B_peak` at every point; margins from the generated predicates. Record: `./verification_record.md`. `VALIDATION_MATRIX.md` SV-036 → passing. Spec Success Criteria all ticked.
- MR-4 read: every new Ref resolves (image files present; `defaults.py:605-614`, `tokamak.py:36-40`, `:117-126` at pin `0254385`).
- Hand-offs: Item 6 settle-up (the model is the source of truth: `magnet__peak_ratio`, `magnet__B_max`, LTS point 4.69 T) and the DI at close are recorded in `.project/CURRENT_WORK.md`; the run-study operand-parsing row is in `.project/backlog/BACKLOG.md`.
- Next: `/audit-models WI-030`, then `/status close WI-030` with the DI.
