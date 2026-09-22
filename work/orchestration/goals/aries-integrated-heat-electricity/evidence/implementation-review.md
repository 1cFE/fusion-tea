---
Verdict: pass
Created: 2026-09-22
Related Artifacts:
  Design: ../../../../active/WI-089_aries-integrated-heat-and-electricity/design.md
  Spec: ../../../../active/WI-089_aries-integrated-heat-and-electricity/spec.md
---

# Independent native integration review

[AGENT] **PASS for the bounded WI-089 thermal/electrical implementation. MR-7 compliant for the represented supplied hardware and operating-state evaluation.** One native assembly connects calculated or source-selected fusion power through fuel/deposition, three coolant/exchanger paths, recuperated conversion, generator/auxiliary accounting and net electricity. A calculated-plasma nominal case removes all modeled heat and produces positive net electricity under the declared assumptions. This does not qualify the published plant, unsupported physics or a full inventory/cost model. Native study/integration-seam delivery and formal closure remain outside this implementation verdict.

## Accepted identity and inspected ownership

[AGENT] Accepted executable fingerprint is `469191fd32c624ccf70e0b4ebc1065b34920df8174c37a09e8f45ecfb241a7d7`. Canonical SHA256 identities are `models/library/analyses/integrated_heat_electricity.sysml`: `6a692de868866d48ba463f761e841dbf4666573bf1067a07d74123aeff96b5aa`, and `models/designs/aries_cs_integrated/plant.sysml`: `9c17f0af2306f7bcde34f8e82d05e8d76e6f44a9222834fb1d64d4a6ff083f5d`. All ten canonical/staged source pairs and sixteen completion-copy receipts match the author's `build-hashes.json`; the receipt records fixed-point regeneration. Independent replay and author verification use the same fingerprint.

[AGENT] Inspected the canonical case, generic interfaces, generated entry/pipeline references, all six new native completions and their guard/output helper. The source selector feeds both fuel and deposition. One coolant transfer has opposite signs in the helium/PbLi branches; absent directions consume a generated zero. Supplied flow, primary flow, conductance, compressor ratios and ratings remain independent entries. Actual compressor states determine the closure boundary. The solved turbine inlet feeds the unchanged expander, and its actual work feeds the electrical owner. Comparison targets enter the ledger only. Caller code supplies scenarios and collects native outputs; it does not compute the plant result.

[AGENT] Early findings E1–E3 are resolved. `generator_auxiliaries` now owns actual conversion, shaft import and named auxiliary demands; the ledger consumes those EXPOSE terms. Fuel base/variable loads, hot-bound margins and both exchanger terminal differences are native outputs. No-transfer/bypass primary states have definedness zero and finite zero carriers, rather than fabricated hot temperatures. The completed source-selector guard also resolves design finding F1 by refusing nonpositive selected fusion power before fuel calculation.

## Independent executed dependency and physical checks

[AGENT] `reviewer-native.py` executes the generated package in a fresh `/tmp/reviewer-aries-native-*` directory; full selected inputs and outputs are retained in `reviewer-native.json`. Reproduction uses `.codex-test/run` with the documented integration environment additions: repository root and `$STOP_PARSER_TEAX_ROOT/packages/teax-simkit` on `PYTHONPATH`, and `STUDY_REQUIRE_TEAX=1`. The initial reviewer invocation omitted that path and failed import before model execution; the corrected documented route passed.

| Native quantity | Calculated baseline | Density amplitude increased by 3% |
|---|---:|---:|
| Selected fusion power, MW | 1835.451283 | 1947.230266 |
| Tritium exhaust, atoms/s | 1.238132713e22 | 1.313534995e22 |
| Delivered/accepted heat, MW | 2240.389047 | 2366.475740 |
| Turbine inlet, K | 788.637518 | 824.406438 |
| Net shaft work, MW | 668.729517 | 761.326084 |
| Net electricity, MW | 423.106794 | 513.776028 |
| Unmet heat, MW | 0 | 0 |

[AGENT] Exactly one effective input changes: plasma amplitude from `5e20` to `5.15e20`. Fusion and exhaust change by the expected density-squared factor, while every equipment, assumption and source-comparison entry remains identical. There is no automatic resize or reference-output substitution. Independent checks use actual outputs to verify cycle/electric/branch energy balances, primary and secondary temperature changes, counterflow `q=UA*LMTD`, and an algebraic temperature solution for the two all-heat-accepted cases. This checks exchanger behavior without duplicating its effectiveness/bisection implementation. Whole-plant residual magnitudes are below `8e-9 MW` in all four reviewer replays.

[AGENT] A separate helium hot-bound change to 200 K produces 896.545166 MW unmet heat, primary state definedness zero and signed negative net electricity. A 600-MW source case retains recuperator bypass, negative shaft work of -110.657966 MW, 116.482070 MW electric motor import and -347.896809 MW net electricity. These results verify adverse-state retention and single-count shaft import. They are diagnostic cases, not proposed qualified operating conditions.

## Native verification and qualification

[AGENT] Inspected `exploration/aries_integrated/verify.py` and the completed WI-089 `evidence/verification.json`: 40 cases, 30 evaluated and 10 intended refusals. Reused those results rather than rerunning the full suite. Each of eight independent heat/shaft/rejection/generator/fuel ratings has insufficient and sufficient cases at fixed demand, with unchanged net output and meaningful constraint transitions. Additional density, ratio, flow and conductance changes exercise demand and interface response. Setting scalar-screen support false preserves `evaluation_defined=0`; its asserted constraint is not satisfied. All magnet, breeding, deposition, hydraulic, material and machine-map support outputs remain zero.

[AGENT] Zero total UA retains the cooling-only precooler refusal; it does not introduce an active heater. The separately exercised generic ledger reports undefined efficiency and a nonclosing balance at zero accepted heat. Invalid producer/fraction/efficiency, negative flow/UA, nonfinite UA and unsupported plasma temperature are refused. The finite/domain guards and bounded root iteration were inspected; the nonconvergence guard is structurally present, not claimed as an exercised physical scenario. Verification-harness import and scalar-channel-resolution failures were repaired without changing the model or executable fingerprint.

[AGENT] Literal failures are retained. The nominal source-conditioned case leaves 158.725848 MW unmet heat. The literal Lyon-source-input case leaves 398.908524 MW unmet heat. The Raffray-accounting case leaves 502.134202 MW unmet heat, retains the -1-MW blanket comparison difference and exposes approximately -182.03 MW whole-plant residual from the declared source-boundary mismatch. Finite cycle output in these cases is conditional diagnostic output, not evidence of a thermally closed operating point. The calculated nominal's success does not erase these failures or establish source agreement.

## Validation and preservation boundaries

[AGENT] Scoped validation passes L1–L5 and fails L6 on 182 dotted-attribute diagnostics. `reviewer-forwarding-census.json` independently locates 182 plain forwarding expressions in the exact staged source set and no other dotted attribute expressions. Actual generated/native consumers execute the consequential forwarding paths. Accept the scoped EXPOSE exception; do not report all-six-level validation success.

[AGENT] `reviewer-preservation.json` independently rehashes all 8,657 entry-protected files with no changes or missing files. This is separate from the retained earlier Stellaris behavioral replay. Source-ownership registration has its own narrow verdict in `ownership-review.md`. No inventory or cost response is introduced or certified. No material implementation finding remains within this accepted thermal/electrical scope.
