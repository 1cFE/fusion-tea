# WI-085: Calculated plasma demand reaches unchanged fuel components

[AGENT] The existing calculated plasma-power output now drives unchanged fuel balances and a fixed processing-capacity check through the actual generated TEAx graph. Six native cases pass their intended outcomes, including a plasma-domain refusal; 35 exact baseline fuel-output comparisons pass. No physical equation or existing library/case/completion was changed. Independent design review accepted the binding; final integrated review accepted this bounded result.

## Observed behavior

| Native case | Calculated fusion power MW | Calculated tritium exhaust atoms/s | Supplied processing rating atoms/s | Result |
|---|---:|---:|---:|---|
| Selected plasma profile | 1835.4512830147435 | 1.2381327129390006e22 | 2e22 | Adequacy satisfied |
| Density amplitude multiplied by 1.5 | 4129.765386783165 | 2.7857986041127463e22 | 2e22 | Adequacy violated; hardware unchanged |
| Selected profile, lower rating | 1835.4512830147435 | 1.2381327129390006e22 | 1e22 | Adequacy violated |
| Selected profile, higher rating | 1835.4512830147435 | 1.2381327129390006e22 | 3e22 | Adequacy satisfied |
| Unsupported processing conditions | 1835.4512830147435 | 1.2381327129390006e22 | 2e22 | Definedness 0; no supported adequacy pass |
| Plasma edge temperature 0.023 keV | Unavailable | Unavailable | 2e22 retained | Upstream domain refusal |

[AGENT] Plasma and fuel assumptions remain exactly those recorded in WI-083 and WI-082. In particular, density amplitude and local helium/temperature/measure choices define a conditioned scenario; 5% burn fraction, 99% recovery and the scalar processing rating are supplied assumptions rather than verified ARIES equipment. No inventory, cost or achieved-breeding claim is made. Dormant breeding placeholders remain in the unchanged calculation contract but are excluded from physical conclusions.

## Actual binding and reuse

[AGENT] The new design assembly is `models/designs/aries_cs_transfer/plasma_fuel.sysml`. Its fuel calc binds `p_fus_in = plasma.fusion_power_MW` from the imported unchanged WI-083 plasma occurrence. Generated pipeline evidence resolves that source to `float aries_cs_plasma_integration__plasma__integration__fusion_power_MW`; the capacity demand resolves to `float aries_plasma_fuel__fuel_system__flows__exhaust_rate`. The verification script asserts the actual producer channel and checks that no fusion-load or `p_fus_in` entry parameter is exposed. Thus a user-supplied source fusion-power result cannot bypass the upstream calculation in this assembly.

[AGENT] The composed package reuses five existing calc definitions: supplied-profile integration, radial density, thermal beta, fuel flows and offered capacity; it also reuses the existing offered-equipment constraint. The incremental change joins the two accepted subsystems using one new assembly and adds no physical definitions. Three typed completions are copied with import-prefix changes only; the reaction helper's original AST identity is retained. `evidence/reuse-identity.json` verifies source-to-staging equality and each completion identity. Existing models and earlier packages remain untouched.

## Verification and reproduction

```bash
PYTHONPATH=/home/reid/1cfe/teax/packages/teax-simkit:/home/reid/1cfe/fusion-tea .codex-test/run python exploration/aries_transfer/plasma_fuel/verify.py
.codex-test/run agentic-mbse validate exploration/aries_transfer/plasma_fuel/staged_models --complete
```

[AGENT] The first command stages the existing sources and new assembly, checks syntax/semantic diagnostics, generates the new package, copies accepted completions, reseals and executes actual TEAx. `evidence/verification.json` retains the package fingerprint, actual producer binding, selected input values, all output channels, executable predicate reports and refusal record. `evidence/native-attempt-1.log` records the successful first attempt. Generated packages and runtime/link stores are ignored locally; the script and receipts remain durable.

[AGENT] For all five evaluated cases, the seven fuel outputs exactly equal the unchanged baseline function at the calculated fusion power. An independent 50-digit decimal energy conversion verifies burn rate. Separate checks verify injection equals burn plus exhaust, unrecovered loss, margin equals selected rating minus demand, definedness and actual predicate status. The amplitude perturbation proves quadratic power/demand response at unchanged rating; independently changing the rating leaves calculated plasma power and fuel demand unchanged. Input artifacts remain unchanged after execution. This supplies the applicable MR-7 insufficient/sufficient and fixed-hardware/varying-demand evidence; price/inventory behavior is unmodeled and receives no credit.

[AGENT] Complete scoped validator actual exit is **1**. Levels 1–5 pass, including one admitted numerical constraint and no malformed constraints. Level 6 reports 12 EXPOSE dot-expression diagnostics: three on the new fuel/capacity interfaces and nine inherited from the unchanged staged plasma case. Actual native execution resolves these interfaces, including the new pressure-independent fusion-to-fuel edge and exhaust-to-capacity edge. The scoped exception is proposed for independent review; the aggregate is not a pass. `evidence/validation-complete.log` retains the result. No failed implementation attempt or broad regression run occurred.

## Tracking handoff

[AGENT] New traceable binding element: `aries_plasma_fuel::fuel_system::flows`, file `models/designs/aries_cs_transfer/plasma_fuel.sysml`; capacity occurrence `aries_plasma_fuel::processing::capacity`. Verification identifier: `WI-085-native-calculated-plasma-fuel`; executable `exploration/aries_transfer/plasma_fuel/verify.py`; receipt `evidence/verification.json`. Coordinator owns native tracking and commits. Final independent review remains open.

[AGENT] Final acceptance: independent review accepted the actual producer/consumer path, unchanged implementations and twelve named L6 EXPOSE exceptions; see `work/orchestration/aries-transfer-experiment/evidence/plasma-fuel-review.md`. SV-129 and the fuel-system occurrence trace are registered.
