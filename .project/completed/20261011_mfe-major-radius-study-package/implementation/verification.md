# Current radius consumer implementation evidence

[AGENT] The bounded implementation is complete under T-024 at `54148a77`, with the parent’s SC-1 correction at `dbba6262`. This is implementation evidence for a fresh independent coding audit, not certification. The audit gate remains open. Exact principal runtime commands and retained failed attempts are in [commands.md](commands.md).

## Implemented behavior

The independent oracle now uses plant R for sustainment, axis field, peak-field bore factor, stored energy, winding length and conductor procurement. The retired operational default is removed. The adapter rejects the retired flat key before conversion, and both its local override boundary and the direct oracle reject `magnet_R0`. The current route rejects retired proposals and constructs proposals without a radius tie or injection. Fixed magnet, wall and divertor reference radii retain their values and roles.

The native contract has exactly 246 inputs. The adapter preserves its existing supported subset: exactly 100 entering mappings become 99, with only the radius mapping removed, no additions and unchanged surviving mappings. All 147 unmapped native inputs are enumerated in [contract-coverage.json](contract-coverage.json) and individually tested for continued explicit refusal. The parent corrected its initial conflation of native support with adapter support in [parent-disposition.md](../parent-disposition.md). The original failing full-coverage test and its output remain in `original-full-coverage-test.txt`, `radius-first.log`, `radius-second.log` and `final-targeted.log`.

Current generic tie tests use explicitly artificial declarations over valid inputs in temporary package copies. They still verify advisory-only tracing, warning removal when a tie is declared, provenance round trips, and identical tracing under changed provenance. The current physical radius tie and its obsolete `R+tie` fixture are removed. Historical declarations and records retain their own bytes.

## Complete numerical controls

[INHERITED, REFERENT] Expectations are WI-051’s immutable pre-repair coordinated controls, frozen from T-021 at `2f8856b7`. `frozen-integrity.json` checks all four recorded expectation-source digests and equality with entering git objects. The capture chronology caveat remains as recorded in WI-051’s handoff; this work does not claim an old successful helper baseline.

`controls-complete/controls.json` records actual current-route execution for `{}` and the ordinary single-key proposal `{"stellarator_09__stellaris__R": 14.0}`. Each case compares every one of the 158 native scalar outputs with the frozen baseline or coordinated R14 control. Baseline is exact; R14 uses the inherited relative and absolute `1e-9` tolerances. All 141 declared oracle channels are independently recomputed and individually checked using the existing verifier’s relative-deviation function and strict tolerance below `1e-9`. The greatest deviation across those 282 comparisons is `2.209043823690201e-16`. `controls-complete/verification_summary.json` additionally rederives all eighteen authored predicates through the stock verifier and retains the exact channels its publication contract requires.

| Control | Primary LCOE ($/MWh) | 1cfe-form LCOE ($/MWh) | Violated authored predicates |
|---|---:|---:|---|
| Baseline | 224.26923288439 | 220.0125640803369 | divertor_heat_ok |
| R-only14 | 250.89832244487582 | 246.2018206142481 | divertor_heat_ok, wall_load_ok, sustainment_ok, loop_capacity_ok |

The separate unchanged WI-051 native probe was executed into this item’s `native/` directory. `native/results.json` and `native/checks.json` prove the full 158-scalar/19-response comparator, exact response maps and baseline serialized report, all nine radius producer/formal edges, fixed anchors and adverse component outcomes. The nineteenth response is the aggregate, not another authored constraint.

Independent R14/baseline ratios are retained in `controls-complete/ratios.json`: volume and winding length are `14/12.7`; axis field and stored energy are `12.7/14`; peak field is `(12.7-c)/(14-c)` at fixed `c=3.1500000000000004`; conductor procurement is invariant because B×R cancels at fixed current. No total-magnet-capital ratio is assumed. Complete cost and financial output comparisons remain in the frozen comparator.

The current ANNEX’s Oracle section explicitly lists all seventeen native scalar channels outside the 141-channel independent map. They remain checked by the full native comparator. Neither that omission nor the 147-input adapter limit is represented as resolved or as permission to sweep unsupported inputs.

## Native metadata and graph reproduction

`refresh_metadata.py` calls the stock manifest fingerprint APIs, current baseline executor and existing indicator CLI. It refreshes the current manifest and all five remaining graph fixtures, then restates their measured graph contract in the kept tests. It neither generates a model nor promotes a pin. Three fresh executions succeeded. `metadata-final-fixedpoint.json` proves exact reproduction of the final manifest, fixtures and graph expectations; `metadata-known-answers.json` retains the complete native graph report and `metadata-baseline_result.json` retains the native baseline metadata.

| Measured identity | Value |
|---|---|
| Semantic | `15ed665c374729a984f29fa753f444677805939ffb195933419b3489debbd47e` |
| Executable, strict native load | `cbdb2a365f39c7863a038a48ba10356a783d3af3ab61b020c8bbba50cfcab37c` |
| Indicator inputs | `609e6cca0a4f329e834b52369a425541ca167bfdfe8608879d900a27ccedf06d` |

The current manifest retains fourteen objective entries. The constraint catalog retains eighteen authored predicates and 28 resolved feature-reference operands. R now fires 87 modules and taints 165 channels, versus the entering plain-R trace of 82/160. Its former externally coordinated trace already measured 87/165. Coil current remains 84/155; minor radius remains 82/160; availability remains 6/18; discount rate remains 9/22. R, a and coil current reach the same thirteen constraints and retain the operating-heat objectives. The five fixtures are regenerated from the actual package, not edited to guessed counts.

## Refusals and regression evidence

The kept radius tests execute old-key-alone, equal, conflicting and zero proposals through the current route and oracle, plus a non-convertible old-key value at both pre-conversion boundaries. Local alias tests reject equal, different and zero values. Native strict execution and generated schema refusals are retained in `native/results.json` and `native/schema-refusals.json`.

Current execution retains `execution_failed` for unified R of 4, 3, exact coil centre, zero and −1; publication refuses those cases. The unchanged native probe independently records all five as `EvaluationFailed`. The original negative peak-component cases still yield their finite negative fields and satisfy the upper-bound comparison; live/reference equality still divides by zero. These are preservation checks, not a physical-domain repair. No clipping or fallback was added.

| Retained run | Outcome |
|---|---|
| `entering.log` / `entering.xml` | 140 failed, 331 passed, 56 errors. Captured before consumer edits. |
| `current-first.log` / `current-first.xml` | 98 failed, 434 passed, one skipped. Ninety-seven failures are inherited historical publication defects; the other was the initial full-adapter requirement test. |
| `radius-first.log` | Nine passed, one failed on the initial full-adapter assertion. |
| `radius-second.log` | Eighteen passed, the same full-adapter assertion failed. Includes actual retired and invalid execution controls. |
| `final-targeted.log` | 84 passed, two failed: the full-adapter assertion and an added fifth ANNEX section conflicting with its existing four-section contract. |
| `final-corrected.log` / `final-corrected.xml` | 233 passed. Parent-corrected mapping contract, all 147 unmapped refusals, current radius execution, fixed anchors, graph fixtures, binding census, generic tie behavior and ANNEX contract. |
| `lint-final-corrected.log` | Changed adapter/route/tests and local callers pass. All sixteen entering oracle line-length findings remain identical by code, message and source line in `oracle-lint-preservation.json`. |

The ANNEX correction moved the coverage material beneath its existing Oracle section. It did not weaken the four-section test. The original failure remains retained. `test-delta.json` lists every entering/current-first node and failure message; `final-targeted-outcomes.json` lists all 233 final passes. Ninety-five current outcomes were restored, and an existing optional historical-store check now reaches its documented skip because that store is absent. No required TEAx capability was skipped.

Every one of the 97 historical failures has the same node, failure status and exact failure message in entering and current-first runs: 20 missing-result rejection failures; 22 exporter calls missing `path`; 44 missing `oracle` and `path`; eleven operating-heating historical cases whose module exposes no `proposals`. Historical file hashes also remain unchanged. These failures are individually reproduced, not inferred solely from unchanged source bytes. They remain outside this migration; the broad study battery is not all green.

Existing current publication and verifier tests passed in the broad replay, including missing/altered bindings, numeric channels and verdicts, invalid output publication, preserved prior CSV bytes, malformed native evidence, identity drift and stock baseline/preflight behavior. Integration tests that regenerate packages or create candidate results were excluded explicitly in `commands.md`.

## Preservation and audit handoff

`protected-before.json`, `protected-after.json` and the empty `protected-delta.json` prove exact preservation across 14,363 permitted tracked protected files and package files. This includes canonical and twin models, snapshot, generated package, direct callers, model tests, original WI-051 evidence, shared tooling, source/history records, goal state and CURRENT_WORK. Parent’s concurrent SC-1 correction is inside this item and was preserved. This author made no commit.

`audited-package-equality.json` separately proves all 246 generated package files match WI-051’s exact audited final manifest, including seal, model contract and all manual bodies. The package is unchanged from the independently audited bytes. Model regeneration, integration, pin promotion, committed study execution, source/physics/finance edits and self-audit were not performed.

[AGENT] Return to parent for a fresh `$my-audit`, including its required fresh product-lens stage and assessment of the quarantine incident below. The adapter scope blocker is resolved by the parent’s correction. The bounded implementation is ready for that assessment; the fresh audit has not run or passed. Fixed-target divertor, engineering/financial assumptions, unsupported oracle inputs and channels, and unresolved component behavior retain the limits stated above. The pending STEP reading supplied no new interpretation.

## Quarantine read violation and corrected guard

[AGENT] The initial implementation-owned preservation helper read seven quarantined files while computing SHA256. This violated the explicit no-read instruction. It emitted only opaque digests and did not emit source text or use scientific content in the model/oracle changes; that does not make the reads authorized. Parent identified the issue and recorded it at `56b06a58` in [parent-disposition.md](../parent-disposition.md). Do not treat this implementation as having complied fully with the quarantine rule.

[AGENT] Parent preserved the original helper as `protect-before-quarantine-fix.py`, preserved the original after/delta manifests under distinct names, and added an exclusion before file reads. The original before manifest remains unchanged. Comparisons filter its existing metadata to the permitted set without reopening any quarantined file. The original 14,370 count included seven quarantined entries; the corrected permitted count is 14,363.

[AGENT] Both parent’s `quarantine-guard-check.json` and this stage’s subsequent `quarantine-guard-implementation.json` record guarded corrected execution. `Path.read_bytes` was wrapped to raise before any resolved quarantine path could be opened: 14,363 permitted reads, zero quarantined attempts, empty permitted-surface delta. The seven-entry count comes only from existing metadata. The original helper must not be rerun. The independent audit must assess this incident; this author does not certify its disposition.
