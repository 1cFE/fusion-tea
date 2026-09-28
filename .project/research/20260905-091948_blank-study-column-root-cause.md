---
date: 2026-09-05T09:19:48-07:00
researcher: Codex
topic: "Silent blank study columns across fusion-tea, sysml-codegen, and TEAx"
tags: [research, study, evidence, codegen, teax]
status: complete
last_updated: 2026-09-05
---

# Research: Silent blank study columns

**Date:** 2026-09-05, America/Los_Angeles

**Researcher:** Codex, with separate codegen, TEAx, and study-tool investigations.

**Research Type:** Codebase / Integration

## Research Question

[INHERITED: `/tmp/handoff-20260905-091138.md`, Focus] Why does a study that declares a package channel which is one field of a multi-output calculation come back with that column silently blank, and what are the alternatives for fixing it and for hardening the seam so it cannot recur? The handoff requests research and a reproduction only; upstream filings remain owner-held.

## Summary

- **Verified by run:** TEAx drops already-extracted plain floats at the evidence projection. Heating returns four values; all four reach the pipeline exit under their correct channel names. None reaches `ModelEvidence.outputs`. The store and query preserve exactly the incomplete evidence they receive.
- **Verified by run:** The study-local exporter converts the missing value to a blank CSV cell. The shared route exporter refuses the same case. **Read from code:** the study-local column map is never passed to TEAx, so the store has no declaration against which to detect the omission.
- **Read from code:** Codegen already emits separate scalar channels. The relevant output emission is unchanged between the production pin and local HEAD. Re-flattening outputs or merely updating the codegen pin does not address the cause.
- **Verified by run:** The oldest power-cycle CSV still contains five fully blank columns across 3,792 rows. The later three committed CSVs contain no blanks; their first blank exports are documented historical events. Verification also skips missing channels, so a passing parity result does not establish coverage of these quantities.
- **[AGENT] Recommendation:** Repair numeric publication in TEAx, share required-column validation across fusion-tea exporters, and add an explicitly asserted mixed-output store round trip. Define evidence compatibility when the projection changes. Treat codegen work as contract/acceptance coverage unless its owner chooses a broader representation migration.

## Evidence and Revision Conventions

**Verified by run** means executed in this session. **Read from code** includes source, tests, and documentation inspected at the revisions below. **Carried historical** means a committed account of a previous execution; it does not mean that execution was repeated. **[AGENT]** marks recommendations and ownership judgments, not owner-settled requirements.

| Reference prefix | Repository and inspected revision |
|---|---|
| `F:` | `/home/reid/1cfe/fusion-tea` at `e0f66f7a5edc4a6b2128d8409247e1c8435816bb`, branch `feat/demo-maturation` |
| `T:` | `/home/reid/1cfe/teax` at `744745f895677f3344b9884627369a6a47ed987f`; source paths beginning `simkit/` are under `packages/teax-simkit/` |
| `C-pin:` | `/home/reid/1cfe/sysml-codegen` at `8a758e9240707b58fe32a509c3b509941ca4fa01`, the fusion-tea dependency pin |
| `C-head:` | The same codegen checkout at `3edbe819e43fe0db7b2485dc383aa209dea67e6a` |

The run used the existing sealed package at `F:exploration/stellarator_e2e/generated/`, imported through the `pkg/stellarator_tea` symlink. Its executed fingerprint was `d4be395197a060590238ff74aa0c5e30fa65c94f0c9390055697da61d62be708`, evidence schema `v2`, evaluator version `v1`. Full provenance, inputs, and boundary keys are retained in [trace.json](20260905-091948_blank-study-column-evidence/trace.json). No model, generated package, manifest, census, study fixture, or upstream source was changed. Existing unrelated working-tree edits were left alone.

## Detailed Findings

### 1. The value disappears after execution, before persistence

**Verified by run:** One baseline proposal passed through `study_route.run_points`, the stock strict package loader, `PreparedEvaluator`, `StudyRunner`, a fresh SQLite store, and `StudyQuery`. The probe observes the real module and executor with temporary in-process wrappers that return their original results unchanged. It restores one heating column only in the historical exporter's in-memory `CHANNELS` map. It does not regenerate or reseal anything.

| Boundary | Observed heating value / shape | Read-from-code location |
|---|---|---|
| Module return | `Heating_Power_ChainOutput`: `p_wallplug_total=100.0`, `p_delivered=50.0`, `p_coupled=50.0`, `eta_pin_eff=0.5` | `F:exploration/stellarator_e2e/generated/modules/mfe_heating_chain/heating_power_chain.py:272`; fields at `F:exploration/stellarator_e2e/generated/schemas/heating_power_chain_output.py:55` |
| Pipeline channel state | Four separately named channels containing plain `float` values | `T:simkit/config/schema.py:97`; `simkit/core/pipeline_executor.py:216` |
| Pipeline `RunResult.outputs` | Same four names and values, including `stellarator_09__stellaris__heat__p_coupled: 50.0` | `T:simkit/core/pipeline_executor.py:138`; emitted exit bindings at `F:exploration/stellarator_e2e/generated/pipelines/pipeline.yaml:1026` |
| `ModelEvidence.outputs` | All four keys absent | `T:simkit/evaluation/projection.py:25` and `:74` |
| Stored case | State `completed`; SQL row holds an `evidence_digest`, not SQL columns for each output | `T:simkit/study/store.py:62` and `:374` |
| Stored evidence JSON | Same absent keys; encoder/store make no additional selection | `T:simkit/study/evidence_io.py:38`; `simkit/study/store.py:332` |
| `CaseView.outputs` | Same absent keys | `T:simkit/study/query.py:105` and `:113` |
| Historical study exporter | Requested `p_coupled_probe` becomes an empty CSV cell | `F:exploration/stellarator_e2e/studies/20260903-wall-and-heating/study.py:409` |
| Shared route exporter | Raises `RouteError: case is missing required result channels: ['p_coupled_probe']` | `F:exploration/stellarator_e2e/studies/study_route.py:262` |

**Verified by run:** There were 115 context channels, 108 exit outputs, and 60 evidence outputs. The 108 exit values comprise 60 `RootModel[float]`, 38 plain floats, nine `ConstraintEvaluation` objects, and one `ConstraintReport`. All 38 plain floats are omitted by numeric projection. The nine evaluations and aggregated report are structured constraint evidence, not 10 missing numeric channels. The 60 evidence keys exactly match the persisted payload and query keys. The single-output LCOE control survives as `313.5134115016116`.

**Read from code:** The specific loss is the predicate `hasattr(value, 'root') and isinstance(value.root, (int, float))`, followed by `float(value.root)`. Plain floats have no `.root`. Both prepared and file-backed evaluators use this projector (`T:simkit/evaluation/evaluator.py:165`, `:260`). Comparing the two backends can therefore agree while both omit the same values.

**Read from code:** ExitPoint selection is a distinct boundary. The executor returns only exit-selected values and keys them by the ExitPoint field, which may differ from the internal channel name (`T:simkit/core/pipeline_executor.py:138`). In this generated package those names agree. A repair must preserve the existing result keys; synthesizing `module__field` names in projection would be unnecessary and could mishandle aliases.

### 2. The codegen output shape is intentional and already supported by TEAx core

**Read from code:** Codegen gives each declared output a qualified channel. Single-output modules return the numeric wrapper `Float`; multi-output modules return a `MultiOutput` subclass whose fields have ordinary Python types. The executor extracts those fields using the YAML output bindings. The generated heating wrapper explicitly says that TEAx extracts its fields into separate channels (`F:exploration/stellarator_e2e/generated/modules/mfe_heating_chain/heating_power_chain.py:224`).

| Contract layer | Inspected implementation |
|---|---|
| Channel naming | `C-head:src/sysml_codegen/core/qualified_names.py:30`; output projection at `elaboration/project.py:396` and `:835` (`C-pin` locations are one line earlier in `project.py`) |
| Wrapper and field generation | `C-pin` / `C-head:src/sysml_codegen/generation/modules.py:444`; `generation/schemas.py:65`; `templates/teax_module.py.jinja2:104`; `templates/multioutput_model.py.jinja2:1` |
| Binding shape | `C-pin` / `C-head:src/sysml_codegen/generation/pipeline.py:174` extracts `.root` only for single-output producers; `:204` emits named multi-output fields; `:291` emits their exit bindings |
| TEAx routing | `T:simkit/config/schema.py:66` documents separate field routing; `simkit/core/pipeline_executor.py:216` implements it; `simkit/core/module_introspector.py:154` preserves the single-output wrapper type |
| Semantic output inventory | `C-pin` / `C-head:src/sysml_codegen/contracts/models.py:37` records channel, Python type, and field name; `contracts/model_contract.py:50` includes every output in the semantic fingerprint |
| Package verification | `C-pin` / `C-head:src/sysml_codegen/contracts/verify.py:332` checks package integrity and runtime marker compatibility; it does not execute evidence publication |

**Read from code and revision diff:** `generation/pipeline.py`, `generation/schemas.py`, `generation/registry.py`, the emitting templates, and `contracts/` are unchanged between `C-pin` and `C-head`. Relevant changes to `generation/modules.py` and `elaboration/project.py` are comments/docstrings. This is a scoped output-shape comparison; other generator areas changed. Moving to local HEAD alone does not correct this omission.

**Read from code:** This mismatch was already visible in a pinned acceptance test. `C-pin:tests/execution/test_fusion_tea_mutation_teax.py:28` explicitly excludes two multi-output driver-cost modules from the runtime evidence comparison and covers them structurally. The real executor helper separately handles raw numeric values (`C-head:tests/execution/test_fusion_tea_real_teax.py:70`). Structural coverage verifies wiring; it does not establish that a study can retrieve the calculated values.

**Read from code:** The evidence assumption is written down, but it is narrower than the core pipeline contract. `T:simkit/evaluation/evidence.py:113` describes selected numeric outputs unwrapped from `RootModel[float]`; `projection.py:25` repeats that restriction. There is no inspected, shared contract promising evidence publication of all supported numeric ExitPoint values. **[AGENT]** The defect is a missing capability and contract mismatch between TEAx layers, rather than evidence that codegen violated TEAx's supported module format.

**Read from code / [AGENT] conclusion:** Generated numeric single-output modules survive intentionally because their wrapper representation matches the projector, provided they are selected at ExitPoint. Safety follows representation and selection, not the number of fields alone. A one-field `MultiOutput` would still be extracted; a non-exit channel is not returned at all. Do not use the handoff's wall-calibration example: `wall_peak_cal` currently has one wrapped output (`F:exploration/stellarator_e2e/generated/pipelines/pipeline.yaml:76`).

### 3. Fusion-tea requests columns after the store has completed

**Read from code:** `study_route.definition` passes an empty objective policy and a proposal-only definition fingerprint into `StudyDefinition` (`F:exploration/stellarator_e2e/studies/study_route.py:153`). Neither it nor `run_points` receives the study-local `CHANNELS` map. Those maps are exporter configuration. The historical phrase “the store accepted the declaration” misidentifies the API boundary: no such declaration reached the store.

**Read from code:** Eight local exporters use `.get(channel)` instead of the shared required-output check: power-cycle `study.py:118`, magnet-technology `:113`, p-pump-fence `:207`, stress-fence `:171`, sustainment-fence `:208`, priced-levers `:259`, 20260903 wall-and-heating `:410`, and 20260904 wall-and-heating `:418`, all under `F:exploration/stellarator_e2e/studies/<study-id>/`. **Verified by run:** the actual 20260903 exporter writes the missing restored column as blank. Its existing other checks and verdict export still pass.

**[AGENT] Ownership conclusion:** There are two direct defects: TEAx's projection omits supported numeric pipeline values; fusion-tea's local exporters silently publish missing required values. Store and query faithfully transport incomplete evidence. There is also a separate coverage gap in verification, described below. Codegen needs shared contract and acceptance coverage; the evidence does not justify assigning it a missing-flattening defect.

### 4. The four sightings are not all preserved in the same form

**Verified by run:** [csv-audit.json](20260905-091948_blank-study-column-evidence/csv-audit.json) was produced by [audit_csvs.py](20260905-091948_blank-study-column-evidence/audit_csvs.py), reading the retained CSVs without rerunning their studies.

| Sighting | Committed evidence checked now | Carried historical account |
|---|---|---|
| `20260821-power-cycle-ab#5` | 3,792 rows; `p_net`, `rec_frac`, `q_eng`, `p_th`, `p_et` blank in every row. No `oracle_operands.csv`. | `F:exploration/stellarator_e2e/studies/DISCOVERY_LOG.md:11`; its `record.md:233` and `:247` explicitly retain the blanks. Disposition at discovery-log `:34` describes a recovery from other committed operands; that recovery was not rerun here. |
| `20260901-sustainment-fence#3` | 334 rows, no empty cells; oracle operands file present. | Discovery-log `:62`; its `record.md:211` and `:225`: six sustainment columns were blank on first export and corrected before commit. |
| `20260903-priced-levers#4` | 439 rows, no empty cells; oracle operands file present. | Discovery-log `:72`; its `record.md:211` and `:230`: `aux_cooling__cryo_cost` blank in all 439 first-export rows, caught by inspection, then moved oracle-side and re-executed. |
| `20260903-wall-and-heating#4` | 639 rows, no empty cells; oracle operands file present. | Discovery-log `:89`; its `record.md:252` and `study.py:359`: all four heating outputs blank on first export, then removed from the export map and exported oracle-side. |

**Carried historical:** Discovery-log `:96` records three repeats after the ANNEX warning. This session did not independently date each ANNEX edit. **Read from code:** the warning remains at `ANNEX.md:104`, and a contradictory stale docstring still describes heating outputs as store-published at `20260903-wall-and-heating/study.py:443`. These are reasons to replace the active workaround guidance with an enforced contract after repair. Historical records should retain their stated limitations.

### 5. Why preflight and parity do not catch this

**Read from code:** Indicators parse pipeline output ports and graph producers (`F:scripts/study/indicators.py:277`), but the declaration format contains axis groups, not required export outputs (`:493`). Unknown-field validation rejects extending that format informally. Axis resolution rejects computed outputs as axes (`:571`). The objective check proves graph membership, not membership in projected evidence (`:780`).

**Read from code:** Preflight's six gates have no export-output gate (`F:scripts/study/preflight.py:76`). Its declared-key check concerns input axes (`:161`); baseline comparison checks the headline result and verdicts, not every requested export column (`:262`). A plain scalar appearing in YAML is insufficient evidence that the current projector publishes it.

**Read from code:** Verification computes `(objectives | predicate binding channels) & oracle_channels`, then skips each key missing from `case.outputs` (`F:scripts/study/verify.py:280`). It fails only when no numeric channel was compared at all. Exporter `CHANNELS` are outside that set. Its `not_independently_verified` list is derived from the glue ledger, not this missing-key coverage (`:489`). An empty list there is not proof that every desired number was checked.

**Read from code:** Verdicts are re-derived from oracle operands and compared to package verdicts (`verify.py:316`). That is an independent verdict check, but a matching inequality result does not establish numeric equality of an omitted operand. Later records disclose oracle-only values (`20260901-sustainment-fence/record.md:197`; `20260903-priced-levers/record.md:210`; `20260903-wall-and-heating/record.md:228`). The original handoff's statement that every record supplies all missing values in `oracle_operands.csv` is too broad, as the power-cycle audit shows.

**Premise conflict, surfaced:** `F:modeling_project/STUDY_POLICY.md:152` says the handwritten oracle retires from the study contract after the first two studies. The runbook still prescribes it (`F:.claude/skills/run-study/runbook.md:119`, `:162`), and later records use it. This research does not decide that policy conflict. Any proposal to make oracle reconstruction a permanent solution remains parked for the owner; the publication repair does not depend on it.

## Architecture Insights

**[AGENT]** Preserve the division of responsibilities: codegen declares truthful output shapes and names; TEAx defines which exit values become durable numeric evidence; study tools declare which of that evidence a particular export requires. A lower-layer integrity check, two equal evaluator outputs, or a store containing some qualified key cannot establish completeness. The expected key set must be asserted explicitly at the consuming boundary.

**[AGENT] Proposed shared contract, not yet ratified:** Numeric evidence preserves supported numeric ExitPoint values under their existing exit keys, regardless of whether their producer returned a wrapper or a multi-output field. Define supported numeric types, Boolean handling, nonfinite handling, exclusions, and absent required values in TEAx's evidence contract. Codegen's acceptance suite consumes that contract. Fusion-tea declares a required subset and refuses missing or null values before publishing a CSV.

## Feasibility Assessment

All options below are **[AGENT] analysis**, grounded in the boundaries above. “Catches all four” refers to their originally requested missing columns; the current later studies removed those requests, so a required-column gate alone would pass them and would not restore lost numeric coverage.

| Layer / alternative | What it achieves and costs | Sightings / records / owner |
|---|---|---|
| Codegen: flatten multi-output fields | Already implemented. Splitting them again does not repair raw-float rejection. Splitting one physical calculation into separate modules would change execution structure without solving the actual contract problem. | No fix from flattening alone. Codegen owner should receive a contract/acceptance filing with all four sightings. |
| Codegen: wrap each field as `RootModel[float]` | Could fit today's projector, but requires coordinated schemas, registry types, YAML bindings, downstream `.root` extraction, and regenerated contracts. Changing YAML type labels alone fails TEAx validation (`T:tests/core/test_pipeline_validator_exit.py:95`). | Could restore all affected values after migration. New generated package/fingerprints and re-pinning; old artifacts stay historical. Codegen and TEAx owners must coordinate. |
| Codegen / TEAx: mark publishable outputs | Existing contract already records output channel/type/field. A publication flag or richer descriptor could express selective evidence policy. Metadata attached only to a container field is lost when projection receives a raw float; it must be carried to the evaluator, including exit aliases. More interface/version work than this numeric repair needs. | Could cover all four with an enforcing consumer. Package-contract metadata changes may alter fingerprints; evidence behavior needs runtime compatibility treatment. Joint owners. |
| TEAx: accept plain numeric exit values | Narrow root fix: admit bare float/int alongside existing numeric wrappers and retain each result key. No recursive flattening is needed. Decide Boolean behavior explicitly; current `.root` predicate accepts bool through int inheritance. Preserve deliberate report handling and nonfinite codec behavior. | Restores the common missing-output class with the current package. Changes persisted evidence even if model fingerprint stays constant. TEAx owner; fusion-tea records the runtime transition. |
| Fusion-tea: shared required-column validation | Validate the entire requested set before opening the destination; reject absent and null values. Reuse the shared route's behavior through a helper accepting each local map. Minimal containment but no restoration of package evidence. | Would refuse all four original exports; current power-cycle still fails. No package regeneration needed. Export tool/source snapshots change. Fusion-tea tooling owner. |
| Fusion-tea: declaration-time gate | Introduce one required-output declaration used by preflight and exporter. Check actual exit selection and runtime publication support, not just graph existence. A version-scoped static gate can reject unsupported plain floats under the old runtime. A baseline execution can instead measure membership without copying TEAx's private predicate. Later-case checks remain necessary. | Would catch all four original requests before a long study. Static rejection of all multi-output modules must expire when support lands. Declaration/tool fingerprinting changes; package need not change. Fusion-tea owner, ideally using TEAx-owned capability information. |
| Study-store contract test | Execute a maintained mixed-output fixture through projection, evidence encoding, store close/reopen, and query; assert all promised keys and values. Test actual exporter refusal while runtime is broken, and successful numeric publication after repair. Tests detect regressions; they are not runtime guards by themselves. | Covers the common mechanism in all four, not only the heating spelling. No automatic historical data repair or re-pin. Shared acceptance responsibility; fusion-tea keeps its export regression. |
| Fusion-tea: explicit verification coverage | Define required numeric comparisons and report missing store/oracle coverage; fail when a required comparison is absent. Do not silently intersect it away. Keep numeric coverage distinct from verdict parity. | Covers wanted channels among the four; to cover every export, the verification declaration must include them explicitly. Changes verification claims and tool snapshots. Fusion-tea owner; permanent oracle obligations remain the parked policy decision. |

### Pins and existing records

**Read from code:** Study compatibility binds `evidence_schema_version` but not `evaluator_version` (`T:simkit/study/compatibility.py:13`). The evaluator currently declares schema `v2` and evaluator `v1` (`simkit/evaluation/evaluator.py:109`). The store checks the bound compatibility fields (`simkit/study/store.py:147`). **[AGENT]** A projection fix or evaluator-version bump alone would not prevent resuming an old store with mixed evidence membership. Choose an appropriate bound evidence version change or another explicit compatibility mechanism; begin a new lineage rather than silently adding unlike cases to an old one.

**Read from code:** Model refinements require new lineage under `F:modeling_project/STUDY_POLICY.md:117`; ANNEX `:72` addresses regeneration and baseline/tie pins; the record template requires explaining crossed fingerprints (`F:.claude/skills/run-study/record-template.md:179`). Tool source digests are recorded (`F:scripts/study/manifest.py:148`; `verify.py:449`). **[AGENT]** A TEAx publication fix changes evidence availability and comparison coverage even when arithmetic and generated-package fingerprint remain unchanged. Record that distinction rather than calling it a model-physics change. A codegen representation change additionally regenerates and re-pins the package.

**[AGENT]** Re-querying old evidence cannot recover values that were never persisted. Keep the power-cycle blanks and later oracle provenance visible in their historical records. Any rerun or supplemental export needs its own provenance and comparison scope. Do not fill old cells from oracle values and present them as recovered package evidence. Repairing exporters alone is an acceptable containment option for the owner to choose, but it leaves the publication defect open.

## Recommendations

1. **[AGENT] TEAx repair:** Preserve supported bare numeric exit values using existing names. Keep report behavior intact. Decide bool/nonfinite policy and bound evidence compatibility with the implementation.
2. **[AGENT] Fusion-tea containment:** Share required-output validation across all local exporters and add one declared-output source consumed by preflight and export. Until TEAx is repaired, refusal should explain that a pipeline-produced value is unavailable in the current evidence contract.
3. **[AGENT] Close the coverage gap:** Assert expected numeric membership in acceptance tests and expose missing verification coverage. A successful comparison of the surviving subset is insufficient.
4. **[AGENT] Replace the active ANNEX workaround after gates exist:** Name affected legacy revisions and the enforced publication contract. Amend the stale heating docstring. Preserve historical sighting rows and limitations. Permanent oracle reconstruction awaits the policy ruling above.

### Tests that would have prevented recurrence

| Repository | Existing gap, read from code | [AGENT] Proposed regression |
|---|---|---|
| sysml-codegen | `C-head:tests/conformance/test_output_schema_contract.py:145` checks field shape using a stand-in runtime; the pinned mutation test explicitly excludes multi-output evidence. | Generate/seal a two-output calc plus a dependent single-output calc. Run real TEAx evaluator and study persistence; assert exact keys and distinct values before and after an input perturbation. Cover the emitted contract, not only graph wiring or executor output. |
| TEAx | `T:tests/evaluation/test_projection.py:100` supplies only fake wrappers; `tests/evaluation/test_parity.py:39` compares outputs sharing the same projector. `tests/test_toy_pipeline.py:272` already proves a plain-float MultiOutput reaches pipeline output and JSON. | Extend that primitive fixture across projection and a reopened study store. Assert explicit membership, value equality, internal-channel renaming, and exit aliases. Add numeric type, report exclusion, nonfinite, and compatibility cases. Do not use equality of two incomplete maps as the only assertion. |
| fusion-tea | `F:tests/study/test_study_publication_fail_closed.py:64` protects only the shared exporter; `test_committed_store.py:20` checks that some qualified output exists. | Exercise each local exporter against a missing required key and null value, asserting existing CSV bytes remain unchanged. Add a real store test for heating and a wrapped control. Under the old runtime assert explicit refusal; after repair assert all declared heating values survive and export. |

### Owner-held filing briefs

**[AGENT] TEAx title:** “Evidence projection silently omits supported bare numeric ExitPoint outputs.” Attach this document and reproduction. Expected: all four named heating floats survive projection/persistence/query. Actual: exit has them, evidence does not, case completes. Cite `projection.py:25,74`, executor `:216`, and the existing primitive-exit test. Acceptance: supported numeric forms and names preserved, report behavior maintained, store round trip asserts membership, compatibility migration stated.

**[AGENT] sysml-codegen title:** “Add shared numeric evidence contract and multi-output study acceptance coverage.” Attach the same evidence and `C-pin:tests/execution/test_fusion_tea_mutation_teax.py:28`. State explicitly that current emission is already flattened and core-compatible. Request an agreed consumer contract and a test proving emitted fields reach study evidence, not an unverified flattening fix. File against the pinned behavior with the scoped HEAD comparison included.

**[AGENT] fusion-tea item scope:** Required export-column validation, declaration-time publication check, store acceptance test, and explicit missing verification coverage. Owner: Run-Study Capability tooling owner (`F:.project/backlog/BACKLOG.md:37`). All filings should attach the four sighting IDs and distinguish retained power-cycle blanks from the later historical first exports. No filings were sent and no fixes were applied.

## Reproduction

The retained [reproduce.py](20260905-091948_blank-study-column-evidence/reproduce.py) uses one complete baseline proposal from the historical study's point constructor with the current sealed package. This is a reproduction of the class, not a re-execution of all four studies at their historical pins. Every store, import link, and CSV is written to a fresh `/tmp/blank-study-column-*` directory. [trace.json](20260905-091948_blank-study-column-evidence/trace.json) records every boundary key and the original run's artifact paths; those temporary files need not survive because rerunning creates new ones.

```bash
UV_CACHE_DIR=/tmp/blank-study-uv-cache \
PYTHONPATH=/home/reid/1cfe/fusion-tea:/home/reid/1cfe/teax/packages/teax-simkit:/home/reid/1cfe/fusion-tea/exploration/stellarator_e2e/pkg \
STOP_PARSER_TEAX_ROOT=/home/reid/1cfe/teax \
uv run --no-sync \
  --env-file /home/reid/1cfe/agentic-mbse/.env \
  --env-file .venv/integration.env \
  python .project/research/20260905-091948_blank-study-column-evidence/reproduce.py \
  /tmp/blank-study-trace-rerun.json

UV_CACHE_DIR=/tmp/blank-study-uv-cache uv run --no-sync python \
  .project/research/20260905-091948_blank-study-column-evidence/audit_csvs.py
```

**Verified by run:** The successful probe asserts `completed`, heating coupling `50.0` in module and exit, its absence in query, a surviving wrapped control, an actual blank exported cell, shared-export refusal, and exact evidence/store/query key equality. The initial harness attempt used the manifest's sparse baseline proposal; the historical exporter rejected it because its held-input checks require explicit `discount_rate`. The successful harness uses the study's complete baseline constructor. That harness correction changed no production behavior. The CSV audit separately confirms the retained records. No broad project test suite was run for this research-only change.

## Code References

- `T:simkit/evaluation/projection.py:25` — excludes raw numeric values; `:74` — the exact loss boundary.
- `T:simkit/core/pipeline_executor.py:216` — already extracts MultiOutput fields; `:138` — exit selection and naming.
- `T:simkit/study/evidence_io.py:38`, `study/store.py:374`, `study/query.py:113` — faithful evidence persistence and retrieval.
- `C-pin:src/sysml_codegen/generation/pipeline.py:204` and `:291` — scalar field and exit emission; `contracts/model_contract.py:50` — complete output inventory.
- `F:exploration/stellarator_e2e/studies/study_route.py:153` — no required export set reaches the runner; `:262` — existing shared fail-closed behavior.
- `F:scripts/study/verify.py:280` — missing numeric comparisons are skipped; `scripts/study/preflight.py:76` — current gate inventory.

## Open Questions

- **Owner decision:** Choose TEAx scalar publication repair versus a broader producer representation/metadata contract. This research recommends the narrow TEAx repair with consumer guards.
- **Owner decision:** Choose the rollout and bound evidence compatibility transition; determine which historical studies need new runs and what comparisons those runs license.
- **Owner decision:** Resolve the oracle-retirement policy conflict before making permanent verification obligations. Numeric publication and export refusal can be repaired independently.
- **Implementation design:** Specify raw/wrapped bool and nonfinite semantics, and whether selective evidence publication needs metadata beyond existing exit bindings. The reproduction establishes the float defect without deciding those broader cases.
