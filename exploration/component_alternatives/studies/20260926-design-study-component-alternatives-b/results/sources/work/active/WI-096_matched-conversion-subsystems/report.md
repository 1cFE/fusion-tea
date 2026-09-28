---
Status: implementation-ready-for-integration-review
Created: 2026-09-26
Updated: 2026-09-26
Related Artifacts:
  - spec.md
  - design.md
  - plan.md
---

# WI-096 implementation handoff

[AGENT] The additive component-alternatives package executes the approved fourth-submission design. The baseline satisfies all 84 native constraints. All 17 evaluated development cases agree with the independent oracle on 872 scalar outputs and every constraint verdict. One additional case correctly refuses unsupported water properties. This is implementation evidence for independent integration review; it does not release a main study or qualify the hypothetical equipment offers.

## Native interface

- Package: `exploration/component_alternatives/component_alternatives_tea`; Python name `component_alternatives_tea`.
- Authored assembly: `models/designs/component_alternatives/plant.sysml`; qualified source prefix `component_alternatives::plant`; channel prefix `component_alternatives__plant__`.
- Inputs: 490 across `plant_params` (418) and `mfe_viability_params` (72 literal Boolean-screen adapter inputs). The complete input map must retain both groups.
- Outputs: 876 scalar channels, including Boolean results. Four iteration counts are numerical diagnostics. The other 872 channels have independently calculated counterparts; all 84 native constraint operands and verdicts are checked.
- Oracle API: `exploration/component_alternatives/verify.py` exposes `evaluate(point)`, `comparison_catalog()` and `operand_bindings()`. It reads authored bindings and native constraint identities; it imports no native calculation body. All oracle code and property assets are package-local `oracle_*.py` and `oracle_matched_cycle_properties.json`.
- Build identity: fixed-point snapshot SHA256 `f230e401651b9610a1f9e0302c7bd11bc7f4b8ab10c0899e864c442440f4edd9`. [Build hashes](evidence/build-hashes.json) contain all 14 source hashes, the identical staged copies, completion origins/transformations, the entire generated package tree and census hash.

## Executed behavior

The baseline independently chooses 2500 MW reactor-side source heat, 14 installed IHX circuits, four salt pumps per circuit with a 250 kg/s design offer, Brayton flow 2000 kg/s, three stage ratios 1.5, recuperator UA 60 MW/K and three cooler UAs 25 MW/K. The unchanged source loop delivers 2598.4236983110704 MW at 773.15 K with a required 565.2761041351143 K return. Both branches receive those exact source outputs. Source power and pressure ratios remain selections; there is no outer matching solve.

| Baseline output | Steam | Brayton |
|---|---:|---:|
| Gross electric MW | 960.274891 | 566.910745 |
| Included electric loads MW | 22.695935 | 7.417582 |
| Net electric MW | 937.578956 | 559.493163 |
| Rejected heat MW | 1660.844742 | 2038.930535 |
| Source/net/rejection residual MW | 4.55e-13 | 4.65e-9 |

The three gas coolers have finite roots within the supported water range: 44.257831 °C, 44.257831 °C and 39.726382 °C, at 7890.631170, 7890.631170 and 12292.914906 kg/s. The selected offers cover these demands. The baseline's cost-per-net-MWh values are conditional hypothetical-account results, not a technology recommendation; the subsequent study owns comparison and cost-correction reporting.

[Native receipts](evidence/native_runs) retain every input, output, predicate and refusal. Successful complete cases include the baseline, independently priced recuperator-UA80 offer, fixed-UA flow2250 and zero-discount financial check. Adverse cases preserve source/controller insufficiency, two-pump demand overload, the three-pump 300 kg/s design horsepower failure, the 225 kg/s offer's overload, insufficient cooler flow/power/duty and both 20/40 MW/K precooler no-root cases. A 61 °C water-inlet case refuses the property domain. Calculated downstream values in failed cases remain labeled by failed guards; they are not passing equipment performance.

## Verification and repairs

[Independent verification](evidence/independent-verification-final.json) records 14,824 scalar comparisons and 1,428 exact predicate comparisons across 17 evaluated cases. The retained gas oracle uses Brent's method against the native gas/bypass bisections. The cooler oracle integrates in water temperature using independently transcribed water properties and Brent's method; production integrates in transferred heat and bisects. The ledger oracle uses Decimal cashflows. The salt oracle extends the retained source-derived oracle for selected pump count. These checks share the physical assumptions and documented property values; they do not independently qualify equipment, procurement scope, hydraulics or site conditions.

[Numerical tolerances](evidence/numerical-tolerances-indicator.json) names every absolute-tolerance channel. All other values use relative disagreement below 1e-9. Absolute classes cover near-zero root, energy and control residuals and bypass fraction only. Every numerical capacity predicate retains its exact native inequality. No tolerance changes an insufficient offer into a passing one. Solver iteration counts are excluded from value agreement because the independent algorithms differ.

[Four-body checks](evidence/four-body-check.md) independently check piecewise cooler integration, pump-heat/source joins, Decimal replacement/cashflow sums and negative-net accounting. [Salt-variant checks](evidence/salt-variant-implementation.md) prove original k=2 parity, selected-count behavior and invalid-count refusal; the complete modified body and SysML diffs are retained.

Two implementation defects were repaired with failed evidence retained. The unused DCF helper's generated input-type import initially refused because no direct DCF occurrence generates that schema; the copied helper now uses a type-only import without changing its reviewed arithmetic. Eighteen bare Boolean predicates initially disappeared from the executable constraint set. They now pass their actual Boolean result into reused Offered Capacity Screen calculations and execute the existing numerical defined/margin predicate. [Guard regression](evidence/guard-regression.json) records 84 expected guards, 66 before repair and 84 afterward; the retained raw-false three-pump case changes from zero violations to its executing horsepower violation. No guard was relaxed.

The stock indicator also rejected the nested unary minus in the original residual predicate. The existing ledger now exposes the absolute conversion-energy residual, and the same constraint compares that magnitude directly with tolerance. [Indicator regression](evidence/indicator-regression.json) checks bit-exact preservation of all 874 prior scalar channels and every verdict on all evaluated cases; the only added channels are the two residual magnitudes. [Current four-body replay](evidence/four-body-check-indicator.json) checks the repaired ledger revision. The coordinator retained the original indicator refusal.

The second stock-indicator refusal identified two uppercase UA assertion labels whose generated module keys were lowercase. Only those assertion labels were changed. [Constraint identity check](evidence/constraint-identity-check.json) records the exact two-ID map, proves all 84 catalog IDs now match pipeline module IDs, and checks all 876 scalar outputs and every predicate verdict remain unchanged. Inputs and physical Boolean output names are unchanged. The coordinator reports the stock indicator passes all 43 indicator groups on commit `d323fc07`; the coordinator owns that seam receipt.

## Scope and solver census

[Implementation census](evidence/implementation-census-final.json) names every calculation occurrence, dependency and oracle hash. Five substantive definitions are new or modified: selected-count salt cooling, controlled boundary bookkeeping, installed-UA recuperator effectiveness, finite water cooler and conversion ledger. Three new numerical constraint definitions express nonnegative margin, required numerical flag and bounded numerical residual. Existing physical definitions and bodies are reused with the recorded package/type adapters; all originals remain unchanged.

Only the finite water cooler adds an iterative physical closure definition, instantiated three times. The complete assembly has six root instances: one reused gas thermal root, two reused primary bypass roots and three water roots. Source heat and pressure ratio have zero outer solves. Finite replacement-date sums and oracle DAG evaluation are not physical root solves. The cooler instances and copied-but-modified salt body are counted explicitly rather than hidden under reuse.

The ledgers retain gross generation, each included electric load, actual heat, unrecovered source heat, rejection, capital accounts, replacement dates, annual service/makeup, discounted energy and accounted/corrected PV cost. Salt inventory is excluded from recurring equipment allowances. Separately scheduled salt-machine/bundle initial costs are excluded from the generic replacement/service base; other salt equipment remains in that explicitly hypothetical allowance. Gas slots reserved for salt equipment/stock are zero. Imported shaft-motor loss is included in rejection for failed negative-shaft cases.

The correction frontier can be calculated transparently from native accounted PV and discounted-energy channels: `X_S = (E_S/E_B)(K_B+X_B) − K_S`. Dedicated cross-branch coefficient channels were not added. The coordinator's study/report layer owns emitting those accounting coefficients and any common source-service-cost sensitivity.

## Validation and preservation

The complete validator exits with failure: L1, L3, L4 and L5 pass; L2 reports 72 intentional literal screen constants and L6 reports 766 alias/readiness diagnostics. [Corrected six-level log](evidence/validation-six-level-indicator.log) preserves the actual result. [Detailed validation disposition](evidence/validation-detail.md) retains each identity and checks its authored binding against native producer/output evidence. The independent reviewer must assess that evidence; this report does not claim a green aggregate validator.

[Source registration tests](evidence/source-registration-tests.log) pass all three selected ownership checks. Registration appends only the new source collection. [Original preservation](evidence/original-preservation-after.json) checks all 13,215 protected original files with zero changes. The earlier matched-root diagnostic receipts, failed generations and native attempts remain retained. No original model/package, dated study or external source was edited.

## Limits on use

This compares the supplied steam offer with tested Brayton offers. Steam temperature, pressure and condenser conditions remain fixed by its inherited equipment ratings; the available operating freedom is unequal. The source-loop law is an imposed total-resistance scenario across changed exchanger topology, including the hypothetical controller allowance. It is not a valve curve, branch-loss qualification or demonstrated reactor/plasma turndown. Generator/motor heat rejection uses the reviewed conditional water service. Cooler and bypass offers and several price/scope allocations remain hypothetical. Primary circulation, source fuel and upstream costs are excluded equally, so the metric is conversion-subsystem cost per net MWh rather than whole-plant LCOE.

## Replay

```bash
.codex-test/run python exploration/component_alternatives/build.py
.codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" python exploration/component_alternatives/run.py --root /tmp/wi096-replay'
.codex-test/run python exploration/component_alternatives/verify.py --runs /tmp/wi096-replay --out /tmp/wi096-independent-replay.json
.codex-test/run python work/active/WI-096_matched-conversion-subsystems/evidence/guard-regression.py --out /tmp/wi096-guard-replay.json
.codex-test/run agentic-mbse validate --complete exploration/component_alternatives/input_models
.codex-test/run python work/orchestration/goals/design-study-component-alternatives/evidence/verify-preservation.py --out /tmp/wi096-originals-replay.json
```

Independent integration review is the next gate. Coordinator-owned study preparation remains outside this author's files; no main study was run here.
