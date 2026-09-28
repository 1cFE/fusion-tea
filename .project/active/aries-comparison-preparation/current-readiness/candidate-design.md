# Separate current-model comparison candidate

[AGENT] Design, 2026-09-19. Authority: `spec.md`, verified `scope.md`, and the existing r2 scientific contract. This document specifies implementation; it neither implements a candidate nor approves its adoption. The coordinator owns final integration and file assignments. Physical interface conclusions remain subject to the fresh source review and native modeling work. No barred material was consulted.

## Directory and custody

[AGENT] Use `.project/active/aries-comparison-preparation/current-readiness/candidate/` as the only new preparation package. Keep `../package/`, its live rules/results and all r2 archives unchanged. The new package continues referring to repository-relative canonical execution paths such as `exploration/stellarator_e2e/generated`; the archive restores those exact paths in an isolated tree. Do not create another generated-package fork inside the candidate.

```text
current-readiness/
  spec.md, scope.md, candidate-design.md, validation receipts
  candidate/
    manifest.json, input-rules.json, diagnostic-inventory.json
    candidate-identity.json, runtime-requirements.json
    archive-members.json, base-required-files.json
    execute_frozen.py, export_model_values.py
    check_lineage.py, check_accounting.py, check_selected_mode.py
    build_freeze.py, compare_candidate.py
    input-applicability.md, accounting-normalization.md
    reporting.md, freeze-procedure.md, limitations.md
    requests/selected-forward.json, table5-conditioned.json
    evidence/selected-forward/       # completed request, native result, closed store and artifacts
    evidence/table5-conditioned/     # separate completed supplied control
    evidence/checks/                 # accepted receipts plus named raw failed attempts
    evidence/reused-index.json       # exact historical paths, revisions, digests and reuse limits
  candidate-archives/<candidate-id>-a/
  candidate-archives/<candidate-id>-b/
  independent-review/<review-id>/   # post-build review, outside the frozen byte set
```

[AGENT] Candidate preparation evidence is a fixed archive input only after execution finishes and its database is closed/checkpointed. New post-freeze executions use a caller-provided fresh directory outside `candidate/`, for example `/tmp/current-comparison-review/runs/selected-forward`; they never append to archived stores. Every result directory is exclusive-create. Existing r2 native stores and historical studies stay where they are and are cited rather than recursively copied. Preserve one immutable failed attempt per failure, then write a new directory for the correction.

## Minimal code ownership

[AGENT] Adapt the six existing package scripts listed above into `candidate/`; avoid a repository-wide refactor. Each accepts `--root` and/or resolves the repository from an explicit recorded root marker, not `parents[3]` or `parents[4]`, because the new path has different depth. Keep the shared reporter `scripts/compare_fixed_point.py` and existing numeric/role/accounting semantics unchanged. `compare_candidate.py` is a thin candidate wrapper: invoke the shared comparator, validate/export the separately declared diagnostics, and append clearly separate engineering evidence. Add candidate tests in `tests/test_current_comparison_candidate.py`; preserve historical r2 tests and fixtures. Reuse meaningful shared reporter tests.

[AGENT] Candidate exporter and report wrapper own write protection; never invoke the shared reporter's overwrite-capable CLI writer. Compute through its `compare` function, preserving historical shared behavior. Each candidate export/report call reserves its destination with exclusive file creation before parsing/validation/comparison; reject an existing destination before invoking the shared comparator or any writer. Use the exclusive handle for the successful document or a structured error document, preserving raw observations/request bytes and an attempt receipt in a fresh exclusive sidecar attempt directory. On overwrite refusal, retain the refusal in a new exclusive sidecar attempt directory and leave all original output bytes unchanged. Do not unlink a failed destination to reuse its name; corrected attempts use a new destination. Exclusive creation, not an existence check followed by `write_text`, owns the race condition. Apply the same rule to every candidate checker receipt destination.

[AGENT] After the first completed post-reveal forward report is written, an exclusive sidecar identity receipt records the candidate archive/rules/request/native-result/model-export/report hashes; the report does not embed its own hash. Subsequent conditioned or corrected reports carry an explicit `original_forward_result` reference to that identity and their own run kind; pre-reveal verification/Table5 controls are labeled preparation evidence instead. Test successful overwrite, malformed-report overwrite, malformed-export overwrite and concurrent/existing destination refusal against byte-identical original files. Fresh malformed inputs must produce retained error evidence and nonzero status, never a success report. This is candidate-wrapper behavior only; existing historical reporter/exporter behavior is unchanged.

[AGENT] Oracle exposure and historical regression fixes belong to their separately assigned current code surfaces, not copied candidate forks. Freeze their final versions. Candidate checks must require coverage of the contract's actual output/predicate inventory, with explicit disposition of any remaining exclusions; no hard-coded 242/956 output count or 20/25 predicate count substitutes for set equality.

## Exact input capture and selections

[INHERITED] Keep the seven independent keys, source precedence, matched-definition requirements, missing-input fallback, profile policy and conditioned groups unchanged. Forward overrides remain sizing 1, reserve 1 and profile exponents 0.35/1.2. Fourteen circuits and the reviewed current live subsystem defaults remain held. The fresh current default baseline and selected forward point are separately labeled results.

[AGENT] `input-rules.json` freezes an exact per-key declaration map containing qualified key, entry group, declared `python_type`, input-file path and raw-default provenance, alongside each pipeline-resolved input path and SHA256. Obtain types from model-contract parameter declarations and generated entry-schema declarations; never infer them from defaults. Require declaration agreement and exact coverage of actual entry keys before admission. At present there are eleven files and 490 values; capture the final candidate's actual set. Preserve raw per-file maps and bytes/digests separately from typed canonical defaults and effective inputs. Flatten only after validating every value and duplicate declaration: duplicate occurrences require the same declared type and equal canonical value, and retain every origin. Unknown/missing keys, mismatched declarations or malformed rule fields fail closed. Resolve pipeline-declared paths, check package containment/read-set coverage, verify hashes and validate schema before execution. Freeze pipeline/model-contract/schema hashes; fixed overrides and all requested values must satisfy the same declared type map and the unchanged override allowlist.

[AGENT] The six declared Boolean suffixes are `buildings__facilities_enabled`, `cryoplant__inventory_enabled`, `fuel_cycle__inventory_enabled`, `fuel_cycle__processing_enabled`, `fuel_cycle__processing_source_conditions`, and `heat_transport__equipment_enabled`, all under `stellarator_09__stellaris__`. Their stored numeric `1.0` defaults do not make them numerical inputs. Canonicalization accepts actual JSON Booleans; for stored input files or explicitly identified legacy stored evidence only, exact finite numeric zero/one may normalize to false/true with the raw representation retained. New Boolean request/fixed-override values must be JSON Booleans. Reject all other Boolean-field numbers, strings, nulls, containers and nonfinite values. Numeric fields reject Boolean values before integer/float handling; declared integers require integer JSON values, while declared floats accept finite JSON integers/floats without accepting numeric strings. Never silently drop an invalid value or rely on permissive schema coercion. Validate rule structure and declared type names themselves; malformed rules cannot supply a fallback type. These six controls remain held and do not become permitted independent comparison inputs.

[AGENT] Candidate tests cover both truth values for all six declarations through canonical capture, effective-input construction and native transport, plus numeric-zero/one stored normalization, conflicting duplicate types/values, unknown declaration types, nonbinary numbers, numeric strings, nonfinite values and Boolean-to-numeric leakage. Keep requested and admitted/refused case counts explicit; invalid requests produce a retained typed refusal rather than disappearing. The shared route's mixed valid/invalid batch behavior remains covered by the separately owned regression repairs.

[AGENT] The executor first exclusively creates the requested attempt directory, before reading/parsing request JSON, loading rules, selecting inputs or checking identity/hashes. Retain original request bytes as `request.raw` and their digest; if reading fails, retain the source path and read-stage error. Strict JSON decoding rejects duplicate object keys and nonfinite literals. Store any parsed representation separately. Enclose every following stage in the attempt recorder: request read/decode, request schema, rule schema, type/declaration checks, input selection, package/read-set/hash/identity verification, and native execution. Each refusal writes an exclusive error receipt with attempt ID, failure stage, named error, raw-request identity when available, and `native_execution_started: false` for pre-execution failures; return nonzero and do not proceed. Do not require valid candidate fingerprints to retain a malformed request. If the requested directory already exists, leave it unchanged, return nonzero, and retain an overwrite-refusal receipt in a freshly exclusive-created sibling rejection directory without loading or executing that old attempt.

[AGENT] Successful admission retains dynamic numeric output discovery, all native verdicts, execution failures, source metadata, supplied roles and canonical effective inputs. Validate candidate identity/seal before native execution, after attempt creation. `verification` means the frozen selected forward controls without reference values, not current raw defaults. Give a raw-default smoke test a separately labeled diagnostic request owned by the validation harness. Tests prove raw retention and no native calls for malformed JSON/schema, malformed rules/types, unlisted/overlapping overrides and tampered input files; attempt reuse never changes original bytes.

[AGENT] Conditioned seams keep their exact allowed keys and disclose what those keys actually control. Held cycle supplies efficiency through the existing cycle switch; it does not remove an adverse salt/cycle interface or waive cycle guards. Held pump controls the primary-loop direct pump/recovery terms; new secondary salt-pump electricity and shaft heat remain active when their held energy mode is active. Describe it as a primary-pump condition, not total-plant pump replacement. Loop accommodation changes circuit count and reruns current equipment/layout consequences. Legacy inventory selects only magnet sizing 0; cooling, facilities and fuel stay live. Held calendar changes availability through the existing positive-domain interface. Finance scenarios remain distinct from currency normalization. Table5 remains a separate fixed supplied control with empty independent/dynamic values and overlap rejection. A full historical all-subsystem-off replay is a regression fixture, not an added comparison seam. If a scientific equivalent of any existing seam cannot execute, report incompatible/refused; adding override permissions requires owner judgment.

## Manifest and account mapping

[AGENT] Preserve existing formal row identifiers and meanings wherever the represented quantity still exists. Add detailed children and diagnostics without inventing additional formal acceptance tests. Preserve all three structural evidence rows, absent complete-manufacturing/vacuum scope and reference nulls. Use prefix `stellarator_09__stellaris__` for the channel suffixes below.

| Existing row | Candidate producer and interpretation |
|---|---|
| `achieved_tbr` | `blanket__breeding__tbr_mean`; role becomes derived, with independent transport uncertainty/lower-bound diagnostics and current breeding adequacy. Remove obsolete held-anchor claims. |
| `coolant` | `heat_transport__cooling_selection__cost`; active total, with seven disjoint equipment children. |
| `fuel_handling` | `fuel_cycle__processing_cost__cost`; active total includes specified equipment/direct installation. |
| `CAS21` | `buildings__facility_accounts__cost`; layout civil/ventilation/site children. |
| `CAS10` | `facility_preconstruction__cost`; current land/preconstruction selection. |
| `CAS72` | `cooling_annual__cas72_total`; separate in-vessel calendar and cooling replacements. |
| `additional_loop_installed` | Preserve the unresolved complete-installed-scope meaning. Add represented equipment rows; do not map a partial installed subtotal into a complete-scope promise. |

[AGENT] Keep inactive power-scaled cooling, legacy facilities, preconstruction and fuel costs as labeled diagnostics only. Bind every active cost row to the selected branch rather than a familiar legacy channel that still happens to exist. Conditioned legacy magnet sizing still uses the active magnet account rollup for its selected physical inventory; it does not authorize switching to a historical procurement convention.

[AGENT] Rebuild disjoint equations from current active producers: seven cooling children; existing magnet constituents; 25 facility civil children plus ventilation/site; fuel equipment/direct installation children; CAS22, direct subtotal, contingency, indirect/owner/supplementary, overnight, annual replacement/O&M/fuel totals and both financing conventions. Use current shipping exclusions for delivered cooling, installed facilities and fuel installation. Validate the native 23-row direct map and each represented child sum against fresh selected-forward and Table5 evidence. Preserve existing arithmetic tolerances. Historical cases belong only to the equation/model version they executed; do not run the new account manifest over incompatible older stored outputs. Source uncertainty and mixed years remain limitations, not arithmetic corrections. CAS23 owns possible steam generation; record price-inclusion evidence or explicit missing scope without introducing a second charge.

## Predicates, engineering diagnostics and claims

[AGENT] Derive `required_constraints` and diagnostic predicate rows from the final model contract, retaining all original twenty and the five facility additions: `facility_capacity_ok`, `facility_outage_ok`, `facility_routes_ok`, `facility_replacement_ready`, `facility_initial_ready`. Freeze exact IDs and expressions; compare the native set against them. Export each native verdict independently of its display value. Preserve raw boundary failures and separate oracle/native-operand rederivations; no acceptance-band or reserve adjustment.

[AGENT] `diagnostic-inventory.json` records exact channel, meaning, unit, selected-mode applicability, existing authored interpretation and affected comparison rows. Include all ten cooling flags identified in `scope.md`, interface temperatures and approach/gap, exchanger/machine/pump/salt applicability quantities, coil-life margin and the underlying breeding, divertor, conductor, winding-fit and facility margins. Discover the final available channel set, then review membership explicitly; a substring search is not a scientific inventory. Add physical-review-required channels after the native interface repair.

[AGENT] Preserve the shared reporter's existing numerical verdict and authored-constraint result for compatibility. The wrapper reports their scope explicitly as numerical comparison and authored predicate conjunction, alongside diagnostic evidence. It adds no new ratio band. It must not present the shared `physical_feasibility` field as complete plant qualification: engineering acceptance remains withheld for adverse relevant physical/applicability diagnostics or unresolved essential evidence. Report the exact blocking diagnostics and unknowns. This applies even when all authored predicates pass. Keep flags that describe source transfer separate from hard physical inequalities rather than blindly treating every zero-valued diagnostic as the same type of failure.

[AGENT] Extend the independent oracle exposure as described in `scope.md` to cover all 22 omissions, then assert exact numeric channel coverage. Guard selectors are held-input identity checks and receive no independent physics credit; duplicate aliases are checked against existing independent quantities. Receipts distinguish scalar arithmetic, input identities, predicates, static/tool coverage and physical-source evidence.

## Archive membership and dependencies

[AGENT] Replace recursive historical `TRACKED_PATHS` collection with reviewed explicit `archive-members.json`. The builder reads only that finite path list; rejects duplicates, absolute/traversal paths, symlinks, missing members, barred paths and credential/cache/import-link artifacts; and excludes output archives and post-build review directories. Membership includes the candidate files and closed selected/control evidence, complete sealed generated package, current study manifest/route/oracle and imported local oracle helper files, required `scripts/study` sources/schemas, current comparator, selected tests/conftests, exact native integration/generation receipts, admissible physical/cost evidence needed for the claim, governing acceptance/protocol and runtime reproduction documents. Include local oracle helpers such as finance, cooling, facilities, fuel inventory, fuel processing and breeding; the old builder's single `verify_stellaris.py` selection is insufficient.

[AGENT] Record canonical and staged SysML input closure from the actual candidate generation/integration request and verify every included source hash. Include the stellarator entry and required MFE definitions/ancestors/imports; do not freeze unrelated confinement designs or recursively include `models/`. If the generator supplied a wider root, record what it actually consumed and justify the necessary closure rather than claiming an unverified minimal set. The sealed generated package is the execution artifact; canonical source and generation receipts establish lineage, not a promise of unrestricted regeneration without toolchain prerequisites.

[AGENT] The recorded Git base supplies unchanged repository infrastructure. `base-required-files.json` indexes every required base-only script/test fixture by path and digest, and the archive index covers every overlay member. Verify both before execution. Full regression receipts identify the tested commit; archive replay need not re-bundle every historical study used during regression. Any frozen check that reads old evidence must either have its finite required bytes included or verify/retrieve them from the declared base/revision. Prefer removing obsolete historical reads from candidate checks. Reused studies are path+commit+digest evidence references with bounded claims, not nested copies of their packages and histories.

[AGENT] `runtime-requirements.json` records Python/SysIDE/runtime versions, sealed agentic/codegen/costing wheel SHA256 identities, actual installed import roots, required teax commit and dirty-tree status, and necessary environment-variable names without values that contain secrets. `tests/test_dependency_provenance.py` checks the three sealed wheels/imports; candidate lineage adds teax and actual interpreter checks. A generic receipt containing teax `unrecorded` is insufficient. Licensed runtime, wheels and permitted external source installations remain external prerequisites; never resolve floating replacements or package credentials. Fail with a named missing prerequisite if independent restoration lacks them.

## Build and fresh restoration

[AGENT] Design new script interfaces to support the following commands. Here `candidate-id` is a new draft identifier, not r2 or an adopted r3. Fill the actual base, archive hash and candidate fingerprints only after the final accepted scientific/tool changes. Use `.codex-test/run` in the working checkout; restored trees use the documented sealed-interpreter exception.

```bash
.codex-test/run python .project/active/aries-comparison-preparation/current-readiness/candidate/check_lineage.py --root . --out /tmp/candidate-lineage.json
.codex-test/run python .project/active/aries-comparison-preparation/current-readiness/candidate/build_freeze.py --out-dir .project/active/aries-comparison-preparation/current-readiness/candidate-archives/candidate-id-a
.codex-test/run python .project/active/aries-comparison-preparation/current-readiness/candidate/build_freeze.py --out-dir .project/active/aries-comparison-preparation/current-readiness/candidate-archives/candidate-id-b
cmp .project/active/aries-comparison-preparation/current-readiness/candidate-archives/candidate-id-a/comparison-freeze.tar.gz .project/active/aries-comparison-preparation/current-readiness/candidate-archives/candidate-id-b/comparison-freeze.tar.gz
.codex-test/run python .project/active/aries-comparison-preparation/current-readiness/candidate/build_freeze.py --verify .project/active/aries-comparison-preparation/current-readiness/candidate-archives/candidate-id-a/comparison-freeze.tar.gz
```

[AGENT] Freeze record contains the base revision, explicit member-list digest, archive/index hashes, predecessor r2 hash, exact scientific/executable/input identities and `status: draft_candidate`. Independent reviewer first verifies archive bytes and member safety, creates an isolated checkout of that base, overlays the actual verified archive, and verifies `COMPARISON-SHA256SUMS` plus base-only file digests. Do not reconstruct an archive from today's source and call that restoration.

```bash
# After restoring the verified archive over its recorded base; cwd is restored root.
set -a
source /home/reid/1cfe/agentic-mbse/.env
source /home/reid/1cfe/fusion-tea/.venv/integration.env
set +a
export PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit"
export STUDY_REQUIRE_TEAX=1
sha256sum -c COMPARISON-SHA256SUMS
/home/reid/1cfe/fusion-tea/.venv/bin/python -m pytest tests/test_compare_fixed_point.py tests/test_current_comparison_candidate.py tests/test_dependency_provenance.py tests/study/test_read_set_coverage.py -q
/home/reid/1cfe/fusion-tea/.venv/bin/python .project/active/aries-comparison-preparation/current-readiness/candidate/check_lineage.py --root . --out /tmp/current-comparison-review/lineage.json
/home/reid/1cfe/fusion-tea/.venv/bin/python .project/active/aries-comparison-preparation/current-readiness/candidate/execute_frozen.py --root . --request .project/active/aries-comparison-preparation/current-readiness/candidate/requests/selected-forward.json --out-dir /tmp/current-comparison-review/runs/selected-forward
/home/reid/1cfe/fusion-tea/.venv/bin/python .project/active/aries-comparison-preparation/current-readiness/candidate/check_selected_mode.py --root . --native-result /tmp/current-comparison-review/runs/selected-forward/native-result.json --out /tmp/current-comparison-review/selected-check.json
/home/reid/1cfe/fusion-tea/.venv/bin/python .project/active/aries-comparison-preparation/current-readiness/candidate/check_accounting.py --root . --native-result /tmp/current-comparison-review/runs/selected-forward/native-result.json --out /tmp/current-comparison-review/accounting.json
```

[AGENT] Repeat execution/checks/export for the frozen Table5 request in a separate path. Compare reproduced scientific inputs, every output and every verdict against frozen evidence using the declared exact/numerical policy; never compare timestamp/store-path metadata as physical results. Preserve zero-boundary differences in raw comparison receipts and require their explicit disposition. Independently join native store/evidence digests, reproduce exports and synthetic reporter output, rebuild the archive byte-identically from its extracted finite member list, and prove a one-byte tamper is rejected on a disposable copy. Open archived SQLite stores with `immutable=1` to avoid reviewer-created WAL/SHM contamination. Review outputs stay outside membership so this rebuild is not circular.

[OWNER: spec.md] Final independent acceptance supplies an approval packet. It does not adopt or publish the candidate, authorize reveal, overwrite saved r2, close the native goal, merge or push. The first eventual post-reveal forward result/report is immutable; later conditioned runs and corrections retain separate identities.
