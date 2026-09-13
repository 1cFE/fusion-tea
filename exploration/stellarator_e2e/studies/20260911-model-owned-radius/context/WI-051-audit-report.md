# Independent native audit: WI-051

**Verdict: POSITIVE for the accepted bounded preservation contract. No material blocker.** MR-051-01–09 and SV-083–089 are satisfied. This is an independent item audit of committed production `641c1051`, not model-wide certification, a goal checkpoint, current-study certification, or item closure.

[AGENT] Fresh auditor, supplied no inherited execution context; did not author the implementation. Governing authority: immutable alignment `work/orchestration/mfe-model-owned-major-radius.md@b847558b`, accepted spec, revised design, original concerns review and its R1/R2 dispositions, approved plan `45003717`, and implementation return. Parent-held routine approval and the explicit audit instruction authorize this review. The bounded contract is agent-originated; no owner waiver or new settled physical premise is inferred.

[AGENT] Native replay produced **428 passed / 13 inherited skips**, including all **64 new executed tests**. Complete native quality validation still **FAILS**: L1/L3/L4/L5 pass, L2 has ten inherited findings, and L6 has 229 inherited errors. Individual location-aware diagnostics and per-test outcomes show no introduced regression. The accepted spec requires this preservation assessment; these failing levels have not been relabeled as passing.

## Evidence and execution

All paths below resolve in [audit-evidence](../active/WI-051_mfe-model-owned-major-radius/audit-evidence/), unless otherwise stated. All Python, native model, PM, and Python subprocess execution used `.codex-test/run`. TEAx execution used launcher-contained `PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1`. No installation, environment dump, quarantine read, production repair, study, integration, pin, commit, archive, or goal-state operation occurred.

| Independent operation | Result and evidence |
|---|---|
| Generate from current canonical family and a newly captured snapshot | Both native generations succeeded; full 246-file package byte equality with production, including schemas, pipeline, seal and all bodies. `replay.py`, `replay.log`, `generation.json`, `source-seeds.json`, `snapshot-seeds.json`, `fresh.snapshot.json`. |
| Complete native quality, entering and current | Both CLI invocations exited 1. `entering-validation.log`, `current-validation.log`, associated command JSON, and `diagnostic-delta.json` retain every API diagnostic. |
| Kept model regression | Exit 0; 428 passed / 13 skipped. `run_tests.py`, `tests.log`, `tests.xml`, `regression.json`. Three deterministic evidence writes were redirected after asserting exact equality with retained bytes; `test-redirects.txt` records them. |
| Production acceptance in a new destination | Exit 0; actual strict native evaluator, generated schema, both production functions, standalone components and production CLI. `acceptance.log`, `acceptance/commands.jsonl`, full JSON results and per-case input/pipeline copies. |
| Independently assess actual results against original git controls | Exit 0. `check.py`, `check.log`, `comparison.json`, `numerics.md`, `protection.json`. This separately re-derives ratios, input records/defaults, all edges, all 50 cost/finance modules and per-node regression. |
| Replay original direct callers and package | Exit 0. Copied original package and callers verified against `45003717` git bytes; `old_runner.py`, `old-runner.log`, `old-runner-results.json`. Original single runner exactly reproduced 177 raw outputs for baseline/coordinated R14; original helper failed with `PipelineValidationError` in both cases. |
| Inspect native citation attachments and original source meaning | Exit 0. `citations.py`, `citations.log`, `citations.json`; Table 2 image independently viewed. |

The independent generation script copies exactly four manual implementations from pre-implementation git objects into absent destinations, verifies the entire seed inventory, and invokes native source/snapshot generation separately. It does not use the author's regeneration helper or copy the other 65 bodies. The kept tests independently exercise that helper's refusal of visible/hidden entries, ordinary files, live/dangling symlinks and reused destinations, and missing/extra/mismatched seeds, checking no generator call and no unauthorized mutation. Absent and genuinely empty directories are accepted as the approved design specifies.

## Requirement findings

| Requirement | Verdict | Specific evidence |
|---|---|---|
| MR-051-01 | PASS | Generic source binding at `models/designs/generic_mfe/mfe_plant.sysml:59`; all nine exact producer/formal edges independently enumerated below and exercised through native execution. `comparison.json:nine_edges`. |
| MR-051-02 | PASS | Unchanged reusable `R0` at `models/library/cost_structure/mfe_power_core.sysml:89`; four generated standalone schemas/functions accept and respond to explicit R0; peak retains R_in. Exact anchors and minor geometry below. `acceptance/standalone.json`, `comparison.json:anchors`; kept standalone and geometry tests. |
| MR-051-03 | PASS | Complete contract/default enumeration proves sole removal of `(stellarator_plant_params, stellarator_09__stellaris__magnet__R0)`; 247→246 with no additions and every surviving complete record/default exact. Four obsolete proposals rejected through five exercised paths. `comparison.json`, `acceptance/schema-refusals.json`, actual direct/native/CLI records. |
| MR-051-04 | PASS | All 158 scalar outputs, 19 responses, complete report/operands/margins and 177 single-runner raw outputs equal the pre-repair controls exactly. All 50 classified cost/finance modules and their 65 output channels covered, including both LCOEs. `numerics.md`, `comparison.json:cost_finance_modules`, `old-runner-results.json`. |
| MR-051-05 | PASS | Only plant R changes to 14 in complete input JSON groups; generated pipeline bytes are unchanged. Every native/direct result matches retained coordinated R14, including full structured reports. Required tolerance 1e-9 relative/absolute; actual complete values were exact. Ratios independently re-derived below. |
| MR-051-06 | PASS, F07 open | All five required invalid plant cases fail on all three execution paths. Old magnet-zero fails contract validation. All five peak controls reproduce original behavior, including negative peaks accepted by the upper comparison. No equation/guard change or clipping. `acceptance/results.json`, `direct-production.json`, `checks.json`. |
| MR-051-07 | PASS | Source/snapshot/production bytes match; all 23 twins equal; only two logical source files changed. Four manual bodies exact; 65 regenerated; current snapshot and complete classified census match. Kept tests execute production code. `generation.json`, `regression.json`, `comparison.json`. |
| MR-051-08 | PASS for preservation | Native structured ownership citation attached and resolves; inherited radius source checked against Table 2. Native trace rows present. Full diagnostics, cost classifications, operating/procurement separation, finance/alpha and protected surfaces preserved. `citations.json`, `diagnostic-delta.json`, `protection.json`; project findings below. |
| MR-051-09 | PASS | [Consumer handoff](../active/WI-051_mfe-model-owned-major-radius/implementation/consumer-handoff.md) supplies full contract/census, nine edges, fixed anchors, exact identities, numeric controls, refusal behavior, invalid/F07 limitations and correct comparator chronology. It explicitly denies current-study completion and specifies the later migration. Independently checked against actual excluded code, not credited as completed. |

SV-083–088 passing statuses are independently supported and unchanged. SV-089 is earned by this audit and updated through native PM; see `SV-089.log`. No row expectation, project requirement, or knowledge record changed.

## Exact wiring and input preservation

Every edge below originates at **`(stellarator_plant_params, stellarator_09__stellaris__R)`**. Module names carry prefix `stellarator_09__stellaris__`.

| Module suffix | Formal | Change from entering graph |
|---|---|---|
| rb | R_in | None |
| geom | R_in | None |
| sustain | R_in | None |
| divheat | R_in | None |
| coil_length | R0 | Retired magnet entry → plant R |
| field_calc | R0 | Retired magnet entry → plant R |
| peak_field_calc | R_in | Retired magnet entry → plant R |
| magnet_cost | R0 | Retired magnet entry → plant R |
| stored_energy | R0 | Retired magnet entry → plant R |

The entire binding key set is unchanged. Exactly those five operands differ; every other operand, including all six fixed-reference edges, is exact. `comparison.json` lists the complete old/new census and changed edges; `complete-input-records.json` retains all old/new records and defaults. The current classified census is independently derived from the actual current contract, including its semantic fingerprint; it is not accepted from the predicted count.

| Quantity | Model / baseline evidence | Numerical discrepancy |
|---|---|---|
| Authoritative major radius | `stellarator_plant.sysml:525`: 12.7 m; independently viewed registered Table 2 image says major plasma radius 12.7 m | 0%, PASS |
| Minor plasma radius | `stellarator_plant.sysml:528`: 1.3 m; same image says 1.3 m | 0%, PASS |
| Magnet R_ref | 12.7 m, exact entering input and fixed generated edges | 0%, PASS preservation |
| Magnet a_coil_ref | 3.1500000000000004 m, exact entering input | 0%, PASS preservation |
| wall_peak_R_ref / R_ref_divertor | Both 12.7 m, exact entering inputs and fixed edges | 0%, PASS preservation |
| Coil bore / centre / outer build | 3.0000000000000004 / 3.1500000000000004 / 3.5500000000000003 m; unchanged radial-build outputs and outer-layer sum under baseline and R14 | 0%, PASS preservation |

Every surviving input/default and all 158 outputs are compared completely in the machine-readable evidence and numerical table. Their pre-existing units, sources and calibrations are preserved; this audit does not claim a new physical-source validation of every historical parameter. No new quantitative calibration was added. The only new model statement is a pure ownership binding.

## Numerical and adverse controls

| Channel | Baseline | Ordinary R14 |
|---|---:|---:|
| Headline LCOE [$/MWh] | 224.26923288439 | 250.89832244487582 |
| Comparison LCOE [$/MWh] | 220.0125640803369 | 246.2018206142481 |
| Decomposed magnet capital [$] | 5401032000.0 | 5944337458.631255 |
| Conductor procurement comparison [$] | 6323469946.334224 | 6323469946.334224 |

All channels, not just these examples, appear in [numerics.md](../active/WI-051_mfe-model-owned-major-radius/audit-evidence/numerics.md). The 50-module coverage is re-enumerated from the current emitted graph using WI-050's retained classification; all 65 associated output channels are included. Complete baseline and R14 report equality includes observed operands, margins and every exact verdict ID.

The independent ratios are volume and winding length `14/12.7 = 1.1023622047244095`, axis field and stored energy `12.7/14 = 0.9071428571428571`, and peak field `(12.7-c)/(14-c) = 0.880184331797235`, where the emitted coil centre is `c=3.1500000000000004`. Actual peak ratio is `0.8801843317972349`. All satisfy the required tolerance. Plant conductor procurement remains invariant because computed B×R cancels; standalone procurement scales by 14/12.7 when B is held fixed. Decomposed capital follows the full frozen controls, not an invented universal ratio.

Baseline violates `divertor_heat_ok`. R14 additionally violates `wall_load_ok`, `sustainment_ok`, and `loop_capacity_ok`. Both aggregate responses are violations. There are 18 authored assertions plus one aggregate response; neither case is a feasible plant.

| Required probe | Actual outcome |
|---|---|
| Retired key alone, equal alongside R, conflicting alongside R, magnet-zero | Strict evaluator and generated schema refuse; both direct functions refuse; CLI refuses unsupported submitted arguments. Exact obsolete key appears in errors. No ignored override. |
| Unified R=4 and R=3 | Both direct functions raise SustainmentError; strict evaluator raises EvaluationFailed. |
| Unified exact coil centre and R=0 | Both direct functions raise ZeroDivisionError; strict evaluator raises EvaluationFailed. |
| Unified R=−1 | Both direct functions raise complex-arithmetic TypeError; strict evaluator raises EvaluationFailed. |
| Peak `valid` | Exact retained component result. |
| Peak `original_negative` | −792.6499999999979 T; upper-bound comparison remains satisfied. |
| Peak `equality` / `reference_equal` | ZeroDivisionError. |
| Peak `reference_inverted` | −0.7821989528795832 T; upper-bound comparison remains satisfied. |

Original `plant_zero` and `magnet_zero` records and failed attempts remain byte-preserved. The unified zero's failing arithmetic need not follow the old scheduler order. **F07 remains open**, and these finite controls establish no general geometry domain.

## Generation, identities and chronology

The audit retained all 28 generated-body text diffs under `body-diffs/`. All 69 body ASTs match entering bodies **after removing docstrings only**. Changed text consists of generated documentation/source-location material; this is not a byte-equality claim for old bodies. Source bindings intentionally change, and their five changed emitted operands are independently verified. The four manual implementations are exact. Snapshot, source and current production packages agree as full bytes/file sets, excluding runtime caches only.

| Identity | Independently measured value |
|---|---|
| Semantic fingerprint | `15ed665c374729a984f29fa753f444677805939ffb195933419b3489debbd47e` |
| Strict executable fingerprint | `cbdb2a365f39c7863a038a48ba10356a783d3af3ab61b020c8bbba50cfcab37c` |
| Package seal SHA256 | `7afe83954c8b591c7b30c94b64940f9904d9f25ea9cf4fc6da5bbb87f171c9f7` |
| Model contract SHA256 | `d2ee3c18e6d087149f55699dd7cdce59f074abcbd861b7824b9310e770b07bc2` |
| Current snapshot SHA256 | `5de752af13561c6e8c7f3e5f5abd2cad08a082564039afd32bf622a1c6d24ce6` |

These match the handoff. Full source/package/manual identities and seed inventories are retained separately. The revised documentation preserves the prototype's semantic fingerprint but changes sealed executable identity; the audit measures those values rather than adopting prototype identities.

The original four frozen controls match T-021 git objects at `2f8856b7`. Numeric expectations were frozen at `2026-09-11T23:28:01.937500+00:00`, before generation started at `23:29:16.675810`. Original single-runner raw capture is timestamped `23:30:25.300477`, after generation but before repaired execution. The incorrect “before generation” description in immutable expectations is preserved and corrected in the handoff's explanation. Independently rerunning the original package confirms the successful single runner and the broken helper; there is no invented successful helper baseline.

## Six-level validation and project obligations

| Level | Actual current result | Entering comparison |
|---|---|---|
| L1 Syntax | PASS; 23 files, zero errors/warnings | Preserved |
| L2 Structure | FAIL; ten literal-placeholder findings | Same ten warnings on unchanged source statements; no unbound/undefined/self-named binding |
| L3 Dataflow | PASS; zero cycles | Preserved |
| L4 Coverage | PASS; 18 admitted numerical assertions | Preserved |
| L5 Documentation | PASS; 86/86 documented, zero missing | Preserved; documentation presence is not universal source certification |
| L6 Architecture/readiness | FAIL; 229 errors | Same individual messages, multiplicities and mapped unchanged-source locations |

The ten L2 findings are ref_power/alpha literal pairs in `waste`, `fuel_handling`, `other_rpe`, `inc_cost`, and `owner`. L6 retains design-expression and extraction findings, including 101 incomplete design attributes and 58 unextractable design attributes. The complete 229 diagnostics are in `diagnostic-delta.json`; CLI excerpts alone truncate them. Line mapping uses matching source lines; an error on a changed line cannot be normalized away. Added and removed diagnostic multisets are empty.

Per-node comparison preserves every one of the 364 entering passes and all 13 skip reasons. Added nodes are exactly 64 passing WI-051 cases. The skips comprise one explicit example-template test and twelve optional legacy foundation tests for absent types/units/materials fixtures. They are not unexecuted WI-051 checks. Native dependencies were available and required tests did not skip.

| Applicable project rule / decision | Audit assessment |
|---|---|
| MR-1, MR-2; AD-005 | PASS preservation: typed CAS/costed-component definitions and hierarchy unchanged; all cost/finance output coverage retained. |
| MR-3; AD-004, AD-007 | PASS: binding is in generic plant usage, concrete duplicate removed; reusable library and 23-file family ownership unchanged. No concept calibration enters a library. |
| MR-4 | PASS changed-scope traceability: `mfe_plant.sysml:59–68` carries direct Source/Ref/Basis and inherited provenance, attached natively to R0. Assessment sections resolve. Existing stellarator R's shorthand citation resolves through the parent part's full path at `stellarator_plant.sysml:80`; Table 2 image independently verifies 12.7 m. No new definition lacks a citation. |
| MR-5 | PASS preservation of existing output schema; no new cross-concept schema standard is inferred. |
| MR-6; PR-3 | PASS: approved design/prototype, independent concerns review, bounded revision and generation safeguards precede implementation. |
| PR-1, PR-2 | No new taxonomy/concept-selection act; existing MFE epic/library split is preserved. No claim to re-certify the historical taxonomy. |
| PR-4, PR-5 | PASS bounded process: original findings/failed attempts survive; stage artifacts/dispositions are committed, with fresh audit evidence now supplied. |
| AD-001 | PASS: existing Real/metre quantities, units documented; no unit/type change. |
| AD-002, AD-006 | No new parameter-metadata type or IFE calculation; preservation confirmed. Existing scalar reusable formals remain separate from plant binding. |
| AD-003 | PASS preservation: closed-form DCF, comparison finance, alpha and lifecycle formulas/operands unchanged; both LCOE channels independently compared. No monetary-convention approval. |
| Calculation-placement convention | PASS for this change: pure value binding, no new calc definition or equation in design. Inherited L6 issues remain explicit. |

Native traceability rows 102–103 identify generic magnet R0 ownership and stellarator R with documentation source, medium confidence and bounded assumptions. They put MR-051 references in source-location text, not the registered-PR field; no PR/DI was invented. Project MR-4 makes structured citations primary. Native rows supplement that chain and do not convert the T-021 interpretation into a newly approved physical source.

## Protected scope and consumer handoff

`protection.json` recomputes the retained protected manifest and compares original prototype, review/revision, T-021 evidence, library, current study tree, study tests, source/knowledge registry and owner requirements/architecture against pre-implementation git bytes. The only admitted protected-file test change is the current 247→246 count assertion, verified as that exact text substitution. Other protected differences match concurrent parent paths and exact bytes at `2a55615b` / `4fc05302`. No parent research/goal edit is attributed to model authorship. No STEP source was adopted into physics or used to add an audit requirement.

The handoff correctly names the later work. Exact current locations are `exploration/stellarator_e2e/verify_stellaris.py`, and `exploration/stellarator_e2e/studies/{oracle_entry.py,manifest.json,study_route.py,ANNEX.md}`, plus `tests/study/`. The oracle's sustainment function reads `magnet_R0` at `verify_stellaris.py:111`; its field/peak/energy/winding/procurement operands also use that duplicate. The adapter maps the retired key at `oracle_entry.py:53`; the manifest declares it as a tie and baseline input; route/annex still describe and inject it. The handoff requires plant R consistently, early obsolete-key rejection, retirement of this tie/injection, current metadata/fixtures refresh, and preservation of generic tie tests and historical records. Those changes have **not** been performed or certified here.

Historical pins, studies, failed evidence, fixed reference anchors, operating/procurement separation, classifications, finance/alpha bases, and preservation ruling `dde47316` remain intact. F07, broader engineering/financial residuals and L-001–L-007 are not closed by this audit.

## Corrective findings and limits

No repair is required to satisfy the accepted WI-051 scope. Two nonblocking findings return to a fresh author for ordinary maintenance:

1. **Test evidence write location.** `tests/models/test_mfe_major_radius.py:80` executes `implementation/contract_checks.py`, which rewrites three retained evidence JSON files. This run proved those bytes equal and redirected the writes to audit evidence. Numerical/runtime checks are meaningful and passed. A future cleanup should make the helper return results or accept a scratch destination, so tests cannot overwrite retained history when a comparison changes. This audit makes no production fix.
2. **Native formatting.** `data/traceability_matrix.csv:102–103` retain native CRLF and trigger ordinary `git diff --check` trailing-whitespace diagnostics. They parse correctly and carry the intended source meaning. Preserve the native evidence; any formatting change belongs to a separately authorized author/tool cleanup. No clean-whitespace claim is made.

The pre-existing stellarator R citation uses shorthand, supported by its parent and the explicit T-021 trace chain; it has not been silently represented as a new direct-path citation. Native L2/L6 failures remain failures. This positive verdict establishes the specified radius-ownership repair and exact handoff, with its preservation evidence, and grants no broader model, source, financial, study, or feasible-plant certification.
