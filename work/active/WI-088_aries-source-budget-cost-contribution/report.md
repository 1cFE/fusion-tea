# Partial source-budget accounting: reviewed results

[AGENT] Eight native cases pass 112 independent Decimal comparisons and eight exact comparisons with the existing cost-per-energy implementation. Twenty invalid cases refuse execution. This establishes supplied-account aggregation and explicit period arithmetic. It does not reproduce or independently predict plant LCOE. Missing annual amortization and expense conventions prevent reconciliation with the source CoE.

## Partial results

| Case | Comparison period | Partial annual allocated cost USD2004 | Partial capital + replacement contribution USD2004/MWh |
|---|---:|---:|---:|
| Literal printed expression | 40 | 150544349.000 | 20.218150551 |
| Inferred 40 FPY/calendar conversion | 47.058823529 | 127962696.650 | 17.185427968 |
| Land account increased 1 million | 40 | 150592599.000 | 20.224630540 |
| Literal expression, availability 0.70 | 40 | 150544349.000 | 24.550611383 |
| Inferred FPY/calendar, availability 0.70 | 57.142857143 | 105381044.300 | 17.185427968 |
| Rounded replacement 975 million | 40 | 150769349.000 | 20.248368117 |
| Supplied net power 900 MW | 40 | 150544349.000 | 22.464611723 |
| Capital-only sub-boundary | 40 | 126394349.000 | 16.974798415 |

[AGENT] The source Table III eight top-level accounts total 2619.572 million USD2004. Applying its inclusive 1.93 multiplier once gives 5055.77396 million. No further contingency or construction interest enters. This total is not overnight capital. Only source parents 20–27 are summed; their descendants and Table VI component totals are excluded from aggregation.

[AGENT cross-page interpretation] The primary 966-million replacement budget comes from Table VII's “Replaced components” row, mapped to a lifetime operating expense through p709's repeated-replacement discussion and Eq. 7's separate replacement term. The table row alone does not say lifetime. Rounded 75 million times 13 replacements gives 975 million; the separate scenario retains the 9-million difference. Neither input predicts a replacement schedule.

[AGENT] Literal mode preserves the printed availability-times-40 denominator despite the text calling 40 full-power years. Inferred mode divides 40 FPY by availability to obtain calendar years, giving 350.4 million lifetime MWh. This alternative is an agent interpretation, not an established source correction. Changing availability therefore changes the literal contribution but leaves the inferred fixed-FPY lifetime contribution unchanged. Availability remains supplied, with no reliability prediction.

[AGENT] The literal capital-only contribution is 16.974798415 USD2004/MWh. Published 77.6 times approximate capital share 82% gives 63.632. That large discrepancy remains unreconciled; no target value or cost share is a model input. Full O&M, fuel and decommissioning remain unquantified. The excluded annual channel is zero only because those costs are outside this partial boundary, not because they are physically free.

## Actual reuse and guards

[AGENT] Two new generic calculations execute once each: an eight-account inclusive-capital budget and guarded period allocation. Eight source account owners supply the former; its calculated inclusive capital and a separately owned replacement budget feed the latter. One unchanged `1cfe-Form LCOE` usage consumes six allocation outputs. In this case its annual numerator positions hold allocated capital and replacement rather than CRF capital charge and full O&M. Exposed output is explicitly named `partial_capital_replacement_cost_per_mwh`.

[AGENT] Reuse is one unchanged model definition and its existing generated completion, carried with only the package import prefix remapped. [Hashes and exact carry receipt](evidence/build-hashes.json) use `reused_formula_*` labels. For each native case, identical annual inputs were also passed to the original implementation under that import remap; all eight outputs agree exactly. Independent 50-digit Decimal arithmetic separately verifies 14 outputs per case, so executable parity is accompanied by dimensional accounting checks.

[AGENT] Every reused-formula input comes from guarded allocation outputs. Power and availability cannot bypass validation. The module count 1 and excluded channel 0 are calculation outputs absent from the public schema; attempted overrides refuse execution at the generated entry. The guard checks finite nonnegative costs, positive multiplier/period/power, availability in(0,1], discrete mode, finite outputs, positive annual/lifetime energy and finiteness of the exact downstream quotient. The downstream unchanged formula still performs the cost-per-energy calculation.

## Verification and limitations

[AGENT] [Native results](evidence/results.json) retain all effective inputs, outputs, source diagnostics and 20 refusals. [First execution log](evidence/execution-attempt-01.log) records the passing suite. Tests perturb one disjoint account, both availability conventions, replacement budget and power while preserving other selections. Refusals cover invalid/nonfinite costs and financial/energy inputs, budget/period overflow, energy underflow, finite-input quotient overflow and forbidden extra public inputs.

[AGENT] L1–L5 pass. Complete validation exits 1 with 14 plain EXPOSE dot-operator diagnostics; [exact locations](evidence/expose-locations.txt) and [validator output](evidence/validation.log) are retained. Native generation and execution resolve those producer dependencies. Independent review accepts this scoped static-tool exception, not a complete-validator pass. First generation rejected the reserved identifier `allocation`; renaming the owner `budget_period` resolved it. The [failed attempt](evidence/generation-attempt-01.log) is preserved. No failed numerical attempt was discarded.

[AGENT] T10 equipment prices and T11 facilities takeoffs remain data-required. T12 is advanced only for this source's disjoint top-level budget, not model/source subaccount reconciliation. T13 is advanced for partial accounting and convention visibility, not full financial reconciliation. Original model libraries, financial conventions and plant outputs remain unchanged.

```bash
.codex-test/run python exploration/aries_transfer/source_budget/build.py
PYTHONPATH=/home/reid/1cfe/teax/packages/teax-simkit:/home/reid/1cfe/fusion-tea .codex-test/run python exploration/aries_transfer/source_budget/run.py
.codex-test/run agentic-mbse validate --complete exploration/aries_transfer/source_budget/input_models
```

[AGENT] The isolated package uses normal code generation, typed completions, resealing and real TEAx execution. Runtime stores and staged inputs are ignored. Primary image copies and hashes, generated contracts, code and compact results are retained.
