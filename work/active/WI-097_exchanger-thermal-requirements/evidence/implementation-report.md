# WI-097 native implementation evidence

2026-09-27. Implemented the independently approved [design](../design.md) in `exploration/exchanger_architecture/thermal_requirements/`. The original model/package and sealed Round 1 study were preserved. This report covers implementation and development controls; it makes no refined-study winner claim.

## Implemented behavior

The isolated SysML library defines `Controlled Network Heat Driven Closure`; the cloned assembly supplies its operating choices and requirement inputs. Mode 0 executes the original closure arithmetic. Mode 1 calculates source hot temperature from full delivered duty and target return, then solves primary bypass inside the coupled cycle closure. Installed UA remains fixed. Actual exchanger outlet, mixed return, active primary flow, bypass fraction, terminal differences and failure margins are separate outputs.

Inadequate conductance reduces accepted heat, alters the cycle/electric state and exposes unmet duty and mixed-return error. A source hot-cap or bypass-authority violation remains an explicitly failed candidate, without clipping the requested state. Zero area gives a finite, undefined terminal state and failed state/heat checks. High-NTU terminal cancellation retains finite transferred heat and a defined active state; it fails approach adequacy rather than disappearing from execution.

The interface adds 14 supplied inputs, 37 scalar outputs and 21 asserted constraints. The generated native interface contains 438 numeric inputs, 588 numeric outputs and 35 predicates. Exact new names/defaults/bindings are in [implementation-interface.json](implementation-interface.json). Constant U under changed active flow, ideal branch mixing, retained pump/pressure assumptions and unpriced control/topology scope remain the reviewed conditional boundaries.

## Generation and preservation

The stock generator completed initial generation, completion reuse, smart regeneration and a repeated-generation fixed point. The build staged 18 source files and retained 38 completion/helper receipts. Snapshot and census were freshly derived. See [build-hashes.json](build-hashes.json), [generation log](generation.log), [completion generation](generation-completions.log), [fixed-point generation](generation-fixed-point.log), [snapshot log](build-snapshot.log) and [census log](build-census.log).

The stock generator omits schemas for unbound calculations. The preserved legacy closure therefore uses a small native data adapter that returns named outputs to the new wrapper rather than importing an absent old schema. The legacy function's full AST, including arithmetic and solve logic, is checked against the historical source by the build. Only its helper import changes. This is an output-container adaptation, not a changed thermal calculation.

Seven assembled legacy replays match all 551 original scalar outputs exactly and preserve all 14 old predicate statuses. Controls include calculated/supplied N, both 2300 MW leaders, the lower-flow series heat failure, failed fixed-split network and the 2600 MW network extension. [native-legacy-preservation.json](native-legacy-preservation.json) records each authoritative predecessor. New requirement verdicts are reported separately and can reject a legacy case.

## Native controls and independent verification

All 18 declared assembled controls executed and returned full constraint reports. [native-controls.json](native-controls.json) contains their complete effective inputs, outputs, verdicts and executable fingerprint; per-case pipeline/input/result receipts are under [native-runs](native-runs). [native-controls.log](native-controls.log) gives the short execution summary.

| Development control | Native result |
|---|---|
| Original 50/50/50 MW/K, controlled series and network | Full duty accepted, but cold-terminal approach checks fail. |
| Offered A, series/network | Both pass all 35 engineering predicates with positive net output. |
| Offered B, series/network | Both pass all 35 engineering predicates with positive net output. |
| Reduced PbLi conductance | 117.175171 MW unmet; lower turbine temperature and 407.136772 MW net; heat-removal and return checks fail. |
| Zero divertor area | 304.317692 MW unmet and 272.450236 MW net; undefined divertor state cannot pass. |
| Increased source duty | Required/actual divertor hot state exceeds its unchanged cap; failure retained. |
| Restricted bypass authority | Required He bypass exceeds the supplied limit; control predicate fails without rewriting temperatures or accepted heat. |
| Offered B with linear extrapolated prices | Thermal states unchanged; cost difference enters the native purchase/lifecycle route. |

The independent oracle author verified all 18 controls against 435 scalar channels and all 35 predicates, with no mismatches or tolerance changes: [oracle-native-verification.json](oracle-native-verification.json). That verification includes original-UA failures, inactive states, legacy controls and offered passes. The oracle's distinct LMTD/logarithmic-domain equations and precision evidence belong to [oracle-implementation.md](oracle-implementation.md).

Three additional native requirement fixtures set the He hot-terminal requirement just below, exactly equal to, and just above the unchanged reported gap. The actual gap remains identical while the native predicate changes as expected. These are binding/comparison regression fixtures, not scientific candidates or added oracle-certified operating points. Receipts are [native-boundaries.json](native-boundaries.json).

## Tests and procurement invariants

Twenty-nine author-owned tests pass: [native-tests.log](native-tests.log). They cover analytical equal-capacity and bypass identities, no-bypass operation, matched offered cases, partial transfer and return error, invalid-domain refusal, inactive/saturated-terminal states, exact legacy preservation, assembled failures, native threshold bindings and procurement invariants. The independent oracle tests are separately owned and reported.

Both architectures receive the same supplied area/price offer. Selected areas and equipment ratings remain unchanged by operating flow/split. Main offer A and B book 174,977,100 USD2004 for the three HX accounts; the linear B sensitivity books 44,327,532 USD2004. All smaller-area extrapolation flags remain visible. Purchased quantities follow supplied area, and every purchase channel is identical within each matched architecture pair. See [native-purchase-invariants.json](native-purchase-invariants.json). The retained-budget prices remain agent-selected assumptions; these checks establish native accounting behavior, not vendor availability or complete control-system pricing.

## Model validator disposition

The installed complete validator exits 1. Levels 1, 3, 4 and 5 pass: syntax, dependency integrity, all 35 numerical assertions admitted with full execution coverage, and documentation coverage. Levels 2 and 6 retain known checker limitations; the result must not be described as an all-level validator pass.

- Level 2: all 105 literal-binding warnings exactly match the baseline identities after path/line normalization. No warnings were added or removed. There are zero unbound, undefined, self-named or orphaned bindings.
- Level 6: all 498 baseline diagnostic identities remain. The only additions are 37 `Unsupported operator '.'` diagnostics, one for each new pure EXPOSE binding `attribute x : Real = evaluate.x;`. There are no removals or other additions. This exact form is accepted by the project's EXPOSE/ADR-002 guidance and by stock code generation. Generated/native execution and the independent channel checks verify the affected data paths. These diagnostics do not identify a new unsupported calculation or hidden design formula.

The baseline/current complete logs and full machine-readable identities are retained in [native-model-validation-baseline.log](native-model-validation-baseline.log), [native-model-validation-full.log](native-model-validation-full.log), [native-validation-baseline.json](native-validation-baseline.json), [native-validation-current.json](native-validation-current.json) and [native-validation-comparison.json](native-validation-comparison.json). [native-validation-capture.py](native-validation-capture.py) reproduces the comparison. This disposition is supported by issue identities and executable evidence, not unchanged aggregate counts alone.

## Reproduction and handoff

```bash
PYTHONDONTWRITEBYTECODE=1 .codex-test/run python exploration/exchanger_architecture/thermal_requirements/build.py
.codex-test/run bash -c 'PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" python exploration/exchanger_architecture/thermal_requirements/run.py'
.codex-test/run bash -c 'PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" python -m pytest exploration/exchanger_architecture/thermal_requirements/tests/test_controlled_closure.py exploration/exchanger_architecture/thermal_requirements/tests/test_native_controls.py exploration/exchanger_architecture/thermal_requirements/tests/test_native_boundaries.py -q'
PYTHONDONTWRITEBYTECODE=1 .codex-test/run python work/active/WI-097_exchanger-thermal-requirements/evidence/native-validation-capture.py
```

The generated package is stable for the coordinator's explicit-path commit and integration workflow. The independent study interface/oracle, metadata pinning, final integration/audit and main study are separate coordinated tasks. No author commit or main-study execution was performed. Source/price qualification and control/hydraulic uncertainty remain visible for the later conditional study interpretation.
