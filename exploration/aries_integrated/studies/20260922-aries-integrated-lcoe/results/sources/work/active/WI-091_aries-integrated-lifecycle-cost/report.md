# Native lifecycle implementation and development evidence

[AGENT] The existing integrated package now calculates complete conditional lifecycle cost using the independently reviewed convention in [design.md](design.md). Implementation checkpoint: `e44a0ded`. Native development checks pass; native integration, committed studies and their interpretation remain coordinator-owned work. This report does not certify a completed study or scientifically qualified plant.

## Results

Both named cases retain the assumed integrated baseline of 423.10679410931664 MW net and 3,150,453.1889379714 MWh/year. Finance assumes constant USD2004, 5% real discount, six-year midpoint construction, 40 calendar operating years and 85% availability. All assumptions and their ranges remain in design.md; they are not recovered source finance.

| Contribution, USD2004/MWh | No breeding/new-supply credit | Assumed new usable breeder feed, 100 kg/year |
|---|---:|---:|
| Financed initial capital | 93.155988 | 93.155988 |
| Routine O&M | 22.219026 | 22.219026 |
| External T shortfall purchase | 996.691911 | 44.447958 |
| Deuterium | 0.022061 | 0.022061 |
| Consumables | 1.587073 | 1.587073 |
| New-feed incremental service | 0 | 9.522440 |
| Dated blanket/divertor/LiPb replacement | 3.301126 | 3.301126 |
| Other equipment overhaul | 1.516446 | 1.516446 |
| Gross terminal decommissioning/disposal | 1.143065 | 1.143065 |
| Salvage credit | -0.228613 | -0.228613 |
| Imported electricity | 0 | 0 |
| **Total LCOE** | **1119.4080833905023** | **176.68656941009704** |

Gross makeup is 104.66770702324638 kg T/year, already net of the internal 99% exhaust recycling. Added new usable breeder feed reduces purchased shortfall to 4.66770702324638 kg/year and has a separate 30 million USD2004/year incremental allowance. The supplied feed is unsupported breeding/extraction performance, not free recovery equipment or a third-party purchase. Both supply and breeding flags remain zero. No recovery optimum is claimed.

The source-conditioned capital/denominator substitution gives 473.9514539717135 and 75.0795764535829 USD2004/MWh for these two supply cases. These are native comparison outputs using supplied 1,000 MW and already-financed source capital, held recurring/blanket replacement amounts and held terminal/overhaul/salvage fractions. Absolute fraction-based allowances change with capital. These outputs do not reconstruct the published 77.6 USD2004/MWh convention; apparent closeness in the new-feed case is not validation. The original source terminal amount is USD1992 and remains unmatched.

## Implementation and interfaces

Additive definitions are in `models/library/analyses/integrated_lifecycle_costs.sysml`: cashflow accounts, supplied annual energy and an already-financed duration guard. The assembly adds finance assumptions, operating levelization, integrated lifecycle accounts/price and separately labeled source-comparison accounts/price. Existing `LCOE DCF` and `Levelized Annual Cost` definitions/completions are reused unchanged apart from package import prefixes. The existing selected hardware, fuel equations and replacement schedule are unchanged. No Stellaris-consumed file was edited.

The source financing guard accepts exactly zero duration and rejects nonzero/nonfinite values. Both source financial consumers bind its native producer channel. A literal-zero experiment was insufficient because generation promotes literal bindings into mutable entry keys; its reviewed correction is this shared native guard. The source duration is a validation input with domain {0}, not a sensitivity axis.

[interface-handoff.json](evidence/interface-handoff.json) gives exact new public keys, entry groups, output IDs, fingerprints and canonical values. [development-cases.json](evidence/development-cases.json) retains all 34 full effective maps/groups and successful scalar/constraint outputs or failure traces. The advertised price is `aries_integrated_plant__lifecycle_price__evaluate__lcoe`; contributions are `aries_integrated_plant__lifecycle_accounts__evaluate__<name>`. The source comparison uses the corresponding `source_lifecycle_*` owners. Existing new-feed input remains `aries_integrated_plant__fuel_inventory__annual_recovery_kg`; its meaning is now explicit beside the binding.

Executable fingerprint: `d13f4153accc48a3d6533a2d29a8e8b6b7cecd86644c322bb64f59fa402e419b`. Semantic fingerprint: `419e6e3d7ba46320a1f88b5f478d36abb5ead85d2ecb6fcdb7aff5fcb2c1e131`.

## Verification and actual refusals

[verification.json](evidence/verification.json) records 34 native development cases: 23 evaluated and 11 expected refusals. An independent 60-digit Decimal oracle sums explicit yearly costs/energy and individually dated events; it does not call production finance helpers. It agrees with both native prices, their PV energy and every cost contribution. Checks cover zero discount/construction, terminal/salvage changes, event exclusion at the horizon, additional supply and curtailment, all inherited source physical controls, fixed-hardware electric/plasma demand changes, and insufficient/sufficient supplied heat-duty capacity. Engineering failure remains visible beside finite financial arithmetic.

Ordinary native execution is fail-fast and does not flush partial files on refusal. The 11 ordinary receipts therefore establish their actual failure and full inputs, not upstream output retention. [diagnostic-verification.json](evidence/diagnostic-verification.json) fills that evidence through the existing independently reviewed isolated native diagnostic runtime, without changing the package or shared runtime. It retains actual nonpositive-power, negative-rate and source-double-financing diagnostics. The nonpositive case has -571.8932058906834 MW net, 505 finite available outputs and blocked integrated LCOE. The diagnostic baseline's 546 numeric results exactly equal ordinary native results. Native engineering predicate publications, unavailable price publications and runtime/input/package digests are retained. Diagnostic source-comparison prices can remain independently evaluable when only integrated power fails; they are not the integrated plant's LCOE.

The first probe invocation omitted the documented `simkit` runtime path and failed before execution. Its corrected invocation used the predecessor's documented environment and succeeded; `probe.log` and `probe-retry.log` retain both. Subsequent native development and diagnostic runs completed as recorded. Raw redundant execution files remain under the temporary locations recorded in `raw-execution-location.json`; the compact tracked receipts retain full effective inputs/results and replay scripts.

## Validator limitations and preservation

The final complete validator exits 1: L1/L3/L4/L5 pass; L2/L6 fail. Full diagnostics and comparison to WI-090 are in [validation-diagnostics.json](evidence/validation-diagnostics.json) and [validation-comparison.json](evidence/validation-comparison.json).

L2 has 105 literal-binding warnings: the 103 predecessor warnings plus explicit zero escalation and project time in the reused levelization calculation. There are zero unbound inputs, undefined bindings, self-named bindings or orphan elements. L6 has 493 static findings: all 407 predecessor findings plus 86 unsupported dot-operator findings on the new pure EXPOSE attributes. No prior finding disappeared. These are the same static-checker limitation exercised by exact-route generation, fixed-point regeneration, native execution and explicit binding review. The staged-path design filter examines zero canonical design attributes, so this is not a general architecture certification. Passing native execution does not turn the complete validator into a pass.

The coordinator confirms 9,104 protected original/frozen files unchanged after the increment and entry Stellaris replay matching 1,352 numeric outputs and 68 responses. Those preservation receipts are separate from these lifecycle checks. No formal item/goal closure is performed by this task.

## Replay

Development verification writes a fresh temporary native execution root and refreshes this item's compact receipts. Preserve accepted receipts before choosing to refresh them. The diagnostic replay uses the reviewed isolated runtime and does not write a study record.

```bash
.codex-test/run bash -c '
  export PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit"
  python work/active/WI-091_aries-integrated-lifecycle-cost/evidence/verify_lifecycle.py
'
.codex-test/run python work/active/WI-091_aries-integrated-lifecycle-cost/evidence/diagnose_refusals.py
.codex-test/run agentic-mbse validate --complete exploration/aries_integrated/input_models
```
