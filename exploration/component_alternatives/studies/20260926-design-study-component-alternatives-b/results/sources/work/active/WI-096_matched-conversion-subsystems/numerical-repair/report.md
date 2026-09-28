---
Status: ready-for-independent-repair-review
Created: 2026-09-26
Related Artifacts:
  - plan.md
  - diagnosis.md
  - ../spec.md
  - ../design.md
---

# WI-096 bounded numerical repair

[AGENT] The repaired executable passes all 15 focused native runs against the unchanged independent oracle: 13,080 scalar comparisons and 1,260 exact predicate comparisons. These comprise the baseline, all six original numerical mismatches and eight neighboring offers. All 14 replayed study points retain their exact 490 inputs and every original predicate verdict. Nine additional local root tuples agree with independently retained high-precision calculations. This handoff requests independent repair review; the coordinator owns the subsequent 498-point replay and study release.

## What changed

The cooler, heater network and primary bypass bisections now continue until the bracket endpoints are adjacent representable floats. Each chooses the endpoint with the smaller equation residual. The former stopping criteria allowed small local heat/UA errors to propagate into water flow, pumping power, net energy, a small hot-side margin and bypass flow. The existing equations, physical domains, infeasibility branches, iteration caps, output schemas and predicates are unchanged. Source power, gas pressure ratios and installed hardware remain selected inputs.

The network and bypass bodies are new local numerical variants copied from their retained originals. The originals remain unchanged. The cooler was already goal-local. [Exact provenance and diffs](preservation-after.json) record original and variant hashes. Only those three generated handwritten files and their package contract hashes differ from the old 199-file executable tree. The build now writes receipts under this supplement's `build/` directory, preserving old live build receipts.

[Diagnosis](diagnosis.md) isolates each case. The reviewer-owned 65-digit probe and [local 70-digit gas probe](gas-root-diagnosis.json) establish that these are native numerical defects. Their separate original-input and oracle-input calculations distinguish upstream propagation from local error. No physical dependency or verification-tolerance exception was found.

## Evidence

| Original case | Dominant mechanism | Largest remaining relative discrepancy among formerly mismatched channels |
| --- | --- | ---: |
| c0035 | Cooler flow error amplified by subtracting from its rating | 2.10e-14 |
| c0040 | Cooler pumping error amplified in net energy and cost denominator | 4.59e-13 |
| c0160 | Cooler flow error amplified in small negative flow margin | 3.35e-13 |
| c0206 | Small water temperature rise amplifies root error into flow, power and negative net energy | 5.86e-16 |
| c0480 | Heater root changes hot margin and controller inlet; smaller local bypass error | 2.12e-11 |
| c0484 | Same gas tuple and mechanism as c0480 | 2.12e-11 |

[Six-case improvement](six-case-improvement.json) retains exact old native, repaired native and oracle values for every formerly mismatched channel. [Focused summary](focused/summary.json) verifies all 872 non-iteration outputs and all 84 predicates for every case. The original failing equipment cases remain failed. The two formerly mismatched efficiency cases remain passing equipment cases. Nearby c0036/c0161/c0205/c0207 retain source, cooler or equipment failures; c0041/c0481/c0482/c0485 retain passing statuses. Root refusal/no-root outputs remain visible in the complete native receipts.

[Local accuracy](local-accuracy.json) checks four cooler tuples against the independent 65-digit integration and five network/controller tuples against the independent 70-digit roots. It checks water flow, temperature, pump power and capacity margin, plus hot-bound margin and bypass flow. The gas local checks also verify adjacent-float brackets. These output checks support the repair more directly than a small residual alone.

The unchanged verification policy requires relative discrepancy below 1e-9 except for its existing named absolute classes on residuals and bypass fraction. No tolerance class or value changed. Four iteration counts remain diagnostics outside numeric agreement. Every constraint verdict is checked exactly. Adjacent-float convergence removes the demonstrated premature stops; it does not guarantee relative accuracy for arbitrary nearly zero differences outside the tested inputs. The full 498-point window still requires the coordinator's fresh verification.

## Identity, census and validation

- New executable fingerprint: `36f653faacc301e76132a9364c1b1024e6d0b3d28742138fcc4759aeef7b3986`.
- Old executable fingerprint: `14dddcfe3b0af047b18064f7c284b6739a633f20777558b304c37f6637a372a3`.
- [Build receipt](build/build-hashes.json) proves regeneration fixed point, all 14 source/staged hash matches and exact generated tree hashes. The semantic snapshot remains `f230e401651b9610a1f9e0302c7bd11bc7f4b8ab10c0899e864c442440f4edd9` because authored SysML is unchanged.
- Fresh integration baseline: [focused/runs/baseline/result.json](focused/runs/baseline/result.json), including `status`, all `effective_inputs`, full outputs/constraint report and fingerprint. It passes all 84 native predicates.
- Interface remains 490 inputs, 876 scalar outputs, 872 independently compared channels and 84 executing predicates.
- [Updated implementation census](implementation-census.json) explicitly counts seven new or modified handwritten definitions across the complete WI-096 implementation, including the two new local numerical variants. The three existing root definitions still have six occurrences: one heater closure, two bypass controls and three water coolers. This repair adds zero physical closures and zero source/ratio outer solves.

Unchanged model source hashes, bindings, generated modules, schemas, constraint metadata and semantic snapshot preserve the scope of earlier structural validation. The earlier complete validator's 72 L2 and 766 L6 diagnostics and their dispositions remain in the original report; no green aggregate validator claim is added. Fresh validation here covers changed numerical bodies, native generation/fixed point, complete focused output/predicate verification and preservation. The coordinator owns fresh stock integration checks and full study execution after independent review.

## Preservation

[Before receipt](preservation-before.json) proves the original 199 executable files agreed byte-for-byte with the sealed archive and git `49c20e69` before changes. [After receipt](preservation-after.json) checks 989 protected study, old evidence, oracle and property entries with zero changes. It also checks the original study snapshot remains `1e8a19872852e19390eba76445e11a866c5da8fb9f791122b6b64d6e16b66641`. [Original preservation](original-preservation-after.json) confirms all 13,215 original files remain unchanged.

The retained `preservation-checker-mismatched-format.json` is a checker-development failure: its symlink comparison incorrectly compared stored link-text SHA256 with raw link text. The final checker compares like formats and passes. The initial expected package-diff list also omitted the generated package contract; its body hash and executable fingerprint changes are now explicitly checked. Neither event changed protected files. The first local-accuracy invocation lacked the documented simkit environment and failed import; the documented command below passes.

## Replay

Use fresh output directories. These commands run focused regressions only.

```bash
.codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" python work/active/WI-096_matched-conversion-subsystems/numerical-repair/regressions.py --out /tmp/wi096-repair-focused'
.codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" python work/active/WI-096_matched-conversion-subsystems/numerical-repair/local_accuracy.py --out /tmp/wi096-repair-local.json'
.codex-test/run python work/active/WI-096_matched-conversion-subsystems/numerical-repair/check_preservation.py --out /tmp/wi096-repair-preservation.json
```

The independent review must assess these changes and evidence. Equipment, cost, pressure-service and off-design qualifications remain exactly as in the accepted design. This numerical repair alone makes no economic recommendation and does not complete the study or close the work item.
