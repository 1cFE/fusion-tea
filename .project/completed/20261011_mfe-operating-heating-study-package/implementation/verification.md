# Current package implementation evidence

[INHERITED] Approved scope is spec/design/plan at `6cf3649e`, routed by T-017 at `392219a8`, after the bounded WI-050 model audit at `55456198`. [AGENT] This report records implementation checks. It is not an independent certificate. The parent must freeze this implementation and dispatch a fresh coding audit before integration.

## Implemented interface

The current oracle adapter maps the audited three signed operating outputs to `operating_heat__p_coupled`, `operating_heat__p_delivered` and `operating_heat__p_wallplug`. The current route requires their numeric publication and exports all 18 individual assertions. The manifest adds those three outputs to its objective catalog so the generic verifier compares the stored native values against the independent oracle. The adapter reuses the unchanged audited `verify_stellaris.py` arithmetic.

The four new scalar assertions bind their exact generated IDs and formal `efficiency` to the corresponding `eta_source_heat` or `eta_couple_heat` input. Tests require exact catalog/binding identity equality, 247 actual public inputs, 18 assertions and 28 resolved feature references. Installed sustainment remains `sustain__p_aux_required <= heat__p_coupled`; burn hold remains the signed demand compared with zero. No threshold, efficiency assumption, finance relation or supported concept changed. Existing study axes and windows remain intact; additional heating-axis declarations exist only in tests and implementation evidence.

The annex replaces its stale current-baseline and heating-tie paragraphs with this interface and its limits. Historical study files and original model evidence retain their own identities.

## Native metadata and fixed point

`refresh_metadata.py` is an item-local reproducible caller. It uses `scripts.study.manifest` fingerprint APIs, the package route's native `execute_baseline`, and the existing indicator CLI through the test harness. It changes no producer. Run from repository root, giving a fresh work directory:

```bash
.codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1 python .project/active/mfe-operating-heating-study-package/implementation/refresh_metadata.py /tmp/wi050-package-metadata-fresh'
```

Three fresh executions produced identical metadata summaries (`metadata-first.log`, `metadata-second.log`, `metadata-third.log`). `metadata-fixedpoint.json` records exact unchanged SHA256 hashes for the manifest and all six regenerated expectation files on the final execution. The metadata identities are preparation, not candidate promotion:

- Semantic: `8f4912c20870b8e0090f9836292403d9d05b0b0e6d46dabf53713772737666cf`.
- Executable: `a9514eb6505dea1589f47cb20bd004e480d61b3be98e7d793bf195b1b2d773b0`.
- Indicator input: `0e61f19061132204911763b142f203d5064e13589b7582c3ef0037d101503204`.

## Graph-derived expectations

The six fixtures were regenerated from the current native graph, then their qualitative sets and measured census were restated in `test_known_answers.py`. R and a fire 82 modules and taint 160 channels; tied R fires 87/165; coil current fires 84/155. Each reaches the same 13 existing assertions and the three operating objectives. Availability remains 6/18 and discount rate 9/22; both leave all 18 assertions unreachable. The valid empty land-cost group retains all 18 bounds and correctly reports the added operating objectives as unreachable.

`heating-reachability.json` retains the independent diagnostic declaration's full report. Installed wallplug reaches `sustainment_ok` and `divertor_heat_ok` structurally (21 modules, 32 channels); its reachable objectives are exactly `lcoe`, `lcoe_1cfe` and `total_capital`. The divertor reach is module-level taint through its installed-capacity diagnostic, not an observed physical heat-flow change. Each efficiency reaches its own two bounds plus seven operating predicates (62/112), including all three operating objectives. A possible dependency path does not prove an executed response.

## Stored native controls

`check_controls.py` executes baseline, installed reserve (120 MW wallplug) and physical demand (`f_alpha_fast = 0.96`) through stock strict-loader TEAx, persists the cases and verifies them with the generic independent verifier. Reproduce with the same environment prefix as above and a fresh output directory:

```bash
.codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1 python .project/active/mfe-operating-heating-study-package/implementation/check_controls.py /tmp/wi050-package-controls-fresh'
```

`controls.json`, `verification_summary.json`, `package_identity.json` and `controls.log` retain inputs, outputs, individual verdicts and parity. The actual store is `/tmp/wi050-package-controls/_work/operating-controls.db`; it is temporary execution evidence, not a committed study record. All three sampled cases compare at worst relative deviation `1.3031089676201858e-16`, below the existing `1e-9` tolerance, and all 18 predicates are independently rederived. `baseline_result.json` is a separate native baseline execution.

Baseline is 224.26923288439 $/MWh with 17 satisfied assertions and `divertor_heat_ok` violated. Installed reserve raises heating procurement from $264145000 to $316974000, leaves all three operating channels unchanged and changes required-minus-installed from −0.920399212073221 to −10.920399212073221 MW. Physical demand changes operating power and holds heating procurement at $264145000. Tests inspect actual stored cases and CSV row publication, not fabricated outputs.

## Preservation and limits

`preserved-hashes.json` and `preservation.json` establish 642 unchanged file hashes, including canonical/twin models, generated code, snapshot, shared study tooling, WI-050 evidence and historical study records. A diff against `6cf3649e` across models, the entire stellarator package area, shared study tooling and WI-050 records identifies only the four authorized current package files. In particular the direct oracle, direct runner and generation producers remain unchanged. No integration, pin promotion, committed study, history regrade, model edit or dependency installation occurred.

This implementation does not resolve the audited model's broader engineering and financial premises. Baseline remains infeasible on the divertor limit. Source/coupling efficiencies remain held approximations, installed procurement remains distinct from online operation, and design-point equipment scaling remains an approximation. Native L2 retains ten inherited findings; L6 retains 227 inherited plus two accepted introduced limitations. Those model checks are inherited evidence, not newly passing package checks. Independent coding audit remains pending.

## Tests and scoped regression findings

Every Python command used `.codex-test/run`. Test commands below used the common prefix `.codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1 python -m pytest ...'`; the ellipsis is replaced with each exact argument list below. No required TEAx execution was skipped.

| Log | Pytest arguments after `pytest` | Result |
|---|---|---|
| `graph-tests.log` | `tests/study/test_operand_bindings.py tests/study/test_known_answers.py tests/study/test_valid_empty.py tests/study/test_indicator_operands.py tests/study/test_verify_operands.py tests/study/test_annex.py -q` | 79 passed in 8.27 s. Covers the final scalar bindings, graph-derived known answers and corrected empty objective set. |
| `consumer-tests.log` | `tests/study/test_verify.py tests/study/test_stock_route.py tests/study/test_numeric_evidence.py tests/study/test_output_contract.py tests/study/test_study_publication_fail_closed.py tests/study/test_preflight_gates.py tests/study/test_indicator_operands.py tests/study/test_verify_operands.py -q -rs` | 150 passed, 86 historical-export failures, one historical-store skip in 199.47 s. All failures are the excluded historical local-export surface described below; current verifier, route, numeric evidence and preflight checks passed. |
| `controls-tests.log` | `tests/study/test_verify.py::test_stored_operating_controls_preserve_procurement_and_signed_capacity -q` | One passed in 8.00 s; also included in the later consumer run. |
| `zero-efficiency-tests.log` | `tests/study/test_verify.py::test_zero_efficiency_is_a_recorded_native_execution_failure -q` | Two passed in 1.17 s. Added after the consumer run started, so these final tests were run separately. |

Counts overlap and are not summed. After these semantic edits, only line wrapping changed the four test files; exact parsed AST equality was asserted before writing each formatted file. `lint.log` records a passing `python -m ruff check` for both changed package Python files and the four changed test modules. `git diff --check` also passed.

The single skipped test is `test_a_store_bound_to_another_identity_is_refused` in `test_verify.py`: its optional historical proof-of-life store `exploration/stellarator_e2e/study/_work/availability_sweep.db` is absent. The current native store, identity and verifier tests ran. No stale metadata fixture substituted for them.

The broader publication regression exposes 86 inherited failures in unchanged historical local exporters: 20 cases do not reject missing/nonfinite values, 22 calls lack the old exporter's required `path` argument, and 44 calls lack its required `oracle` and `path` arguments. They comprise 80 malformed-result cases across eight historical studies plus six complete-value API mismatch cases. `historical-failures.json` lists every failing case and proves the historical exporter/test bytes equal entering revision `6cf3649e`. `historical-isolated.log` separately reproduces one missing-value guard failure and one API mismatch without the combined suite, ruling out a combined-suite import collision for those examples. The publication issues were already noted in `.project/CURRENT_WORK.md` under the numeric evidence repair; later historical exporters expand that earlier failure count. Repairing this historical surface is outside T-017 and would require separately authorized follow-up. No assertion was weakened, no historical code or results changed, and the broad battery is not claimed green.

Two implementation test expectations needed correction. The initial run (`first-tests.log`: 55 passed, one skipped, one failed) still had the former empty group's objective set; `graph-tests.log` verifies its current graph-derived set. The first zero-efficiency test guessed state `failed`; native evidence uses `execution_failed`. `zero-efficiency-first.log` retains that failure, and the final two-case test verifies the actual failure state plus export refusal. These were test capture errors, not changes to runtime behavior.

## Parent freeze check

[AGENT] Staged whitespace inspection includes the new evidence files omitted by the unstaged check above. Four retained logs contain original pytest blank-line whitespace: `consumer-tests.log`, `first-tests.log`, `historical-isolated.log` and `zero-efficiency-first.log`. Preserve those original bytes. The staged check passes with only these exact logs excluded; all code, metadata, fixtures and authored prose pass without exceptions.
